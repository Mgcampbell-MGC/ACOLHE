"""Tests for the PNCP client. NOTHING here touches the network.

Every test drives a fake transport, so the suite passes on a plane, during a
PNCP outage, and in CI. A test that needs pncp.gov.br to be up cannot tell you
anything about your own code when it fails.

The four properties under test are the four the business depends on:
  1. a cached URL costs ZERO network calls
  2. retryable statuses are retried with growing, jittered delays -- and
     non-retryable ones are not
  3. a killed harvest resumes without duplicating or losing rows
  4. a failure is RECORDED and surfaced, never silently dropped
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harvest.pncp_client import (  # noqa: E402
    FAMILY_A,
    FAMILY_B,
    Cursor,
    DiskCache,
    PNCPClient,
    Response,
    Unavailable,
    USER_AGENT,
    jsonl_sink,
    keys_in_jsonl,
)


# --------------------------------------------------------------------------
# Fakes
# --------------------------------------------------------------------------

class FakeTransport(object):
    """Scripted transport that counts every call.

    Counting is the whole point: "the cache works" is only believable if we
    can show the socket was never opened.
    """

    def __init__(self, handler):
        self.handler = handler
        self.calls = []

    def get(self, url, timeout=None):
        self.calls.append(url)
        result = self.handler(url, len(self.calls))
        if isinstance(result, Exception):
            raise result
        return result

    @property
    def count(self):
        return len(self.calls)


def listing_payload(total_rows, page, page_size, prefix="X"):
    """A Family A listing page shaped exactly like the live one.

    Field names verified against the live API on 2026-09-19: data,
    totalRegistros, totalPaginas, numeroPagina, paginasRestantes, empty.
    """
    total_pages = max(1, (total_rows + page_size - 1) // page_size)
    start = (page - 1) * page_size
    rows = [
        {"numeroControlePNCP": f"{prefix}-{i:05d}", "objetoCompra": f"obj {i}"}
        for i in range(start, min(start + page_size, total_rows))
    ]
    return {
        "data": rows,
        "totalRegistros": total_rows,
        "totalPaginas": total_pages,
        "numeroPagina": page,
        "paginasRestantes": max(0, total_pages - page),
        "empty": not rows,
    }


def ok(payload):
    return Response(200, json.dumps(payload))


def page_of(url, total_rows, page_size, prefix="X"):
    page = int(url.split("pagina=")[1].split("&")[0])
    return ok(listing_payload(total_rows, page, page_size, prefix))


def make_client(tmp_path, handler, **kw):
    """A client wired to temp dirs and a fake transport, with no real sleeping."""
    kw.setdefault("min_interval", 0)          # tests must not wait on politeness
    kw.setdefault("sleeper", lambda s: None)  # backoff is asserted, not endured
    kw.setdefault("concurrency", 1)
    transport = FakeTransport(handler)
    client = PNCPClient(
        cache_dir=str(tmp_path / "cache"),
        state_dir=str(tmp_path / "state"),
        transport=transport,
        **kw
    )
    return client, transport


# --------------------------------------------------------------------------
# 1. CACHE -- a re-run must cost zero network calls
# --------------------------------------------------------------------------

def test_second_fetch_of_same_url_makes_no_network_call(tmp_path):
    client, transport = make_client(tmp_path, lambda u, n: ok({"data": [], "v": 1}))
    url = "https://pncp.gov.br/api/consulta/v1/x?pagina=1"

    client.fetch_json(url, FAMILY_A)
    assert transport.count == 1

    client.fetch_json(url, FAMILY_A)
    assert transport.count == 1, "cached URL must not reopen a socket"
    assert client.cache_hits == 1


def test_cache_survives_a_new_client_on_the_same_directory(tmp_path):
    """The cache is on DISK. A fresh process must inherit it."""
    client, transport = make_client(tmp_path, lambda u, n: ok({"v": 1}))
    url = "https://pncp.gov.br/api/consulta/v1/y?pagina=1"
    client.fetch_json(url, FAMILY_A)

    client2, transport2 = make_client(tmp_path, lambda u, n: ok({"v": 2}))
    assert client2.fetch_json(url, FAMILY_A) == {"v": 1}
    assert transport2.count == 0


def test_full_day_harvest_twice_second_run_is_zero_network(tmp_path):
    """THE ACCEPTANCE TEST, with the network stubbed.

    Two full passes over modalidades 6/7/8. The second must be free.
    """
    totals = {6: 137, 7: 12, 8: 241}

    def handler(url, n):
        mod = int(url.split("codigoModalidadeContratacao=")[1].split("&")[0])
        return page_of(url, totals[mod], 50, prefix=f"M{mod}")

    client, transport = make_client(tmp_path, handler)
    rows_a = []
    r1 = client.harvest_day("20260915", (6, 7, 8), page_size=50, sink=rows_a.append)
    first_calls = transport.count

    assert first_calls > 0
    assert r1.rows_total == sum(totals.values())
    assert r1.complete, r1.summary()

    client2, transport2 = make_client(tmp_path, handler)
    rows_b = []
    r2 = client2.harvest_day("20260915", (6, 7, 8), page_size=50, sink=rows_b.append)

    assert transport2.count == 0, "second run must make ZERO network calls"
    assert r2.network_calls == 0
    assert r2.rows_total == sum(totals.values())
    assert r2.rows_new == 0, "everything was already held"
    assert r2.complete


def test_failures_are_never_cached(tmp_path):
    """Caching a 503 would freeze an outage into the dataset permanently."""
    state = {"n": 0}

    def handler(url, n):
        state["n"] += 1
        if state["n"] <= 2:
            return Response(503, "<html>503</html>")
        return ok({"v": "good"})

    client, transport = make_client(tmp_path, handler)
    url = "https://pncp.gov.br/api/pncp/v1/z"
    assert client.fetch_json(url, FAMILY_B) == {"v": "good"}
    assert transport.count == 3

    # Only the success is on disk, and it is the success we get back.
    cache = DiskCache(str(tmp_path / "cache"))
    assert cache.get(url)["status"] == 200


def test_a_200_with_unparseable_body_is_not_cached(tmp_path):
    """Caching garbage is worse than refetching it."""
    calls = {"n": 0}

    def handler(url, n):
        calls["n"] += 1
        if calls["n"] == 1:
            return Response(200, "<html>not json</html>")
        return ok({"v": 1})

    client, transport = make_client(tmp_path, handler)
    assert client.fetch_json("https://pncp.gov.br/api/consulta/v1/q", FAMILY_A) == {"v": 1}
    assert transport.count == 2


# --------------------------------------------------------------------------
# 2. BACKOFF
# --------------------------------------------------------------------------

@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_retryable_statuses_are_retried_then_raise(tmp_path, status):
    delays = []
    client, transport = make_client(
        tmp_path, lambda u, n: Response(status, "down"),
        max_attempts=4, sleeper=delays.append)

    with pytest.raises(Unavailable):
        client.fetch_json("https://pncp.gov.br/api/pncp/v1/itens", FAMILY_B)

    assert transport.count == 4, "must spend the whole retry budget"
    assert len(delays) == 3, "sleeps between attempts, not after the last"


@pytest.mark.parametrize("status", [400, 404])
def test_non_retryable_statuses_fail_immediately(tmp_path, status):
    """400/404 cannot be fixed by waiting, and retrying spends the shared
    rate-limit budget the rest of the harvest needs."""
    client, transport = make_client(
        tmp_path, lambda u, n: Response(status, "nope"), max_attempts=5)

    with pytest.raises(Unavailable):
        client.fetch_json("https://pncp.gov.br/api/consulta/v1/bad", FAMILY_A)
    assert transport.count == 1


def test_connection_errors_are_retried_not_treated_as_tls_problems(tmp_path):
    """HTTP 000 means timeout or proxy. The fix is backoff, never verify=False."""
    delays = []
    client, transport = make_client(
        tmp_path, lambda u, n: OSError("connection reset by peer"),
        max_attempts=3, sleeper=delays.append)

    with pytest.raises(Unavailable) as exc:
        client.fetch_json("https://pncp.gov.br/api/pncp/v1/itens", FAMILY_B)

    assert transport.count == 3
    assert len(delays) == 2
    assert all(f.status is None and f.error == "OSError" for f in exc.value.failures)


def test_backoff_grows_exponentially_and_is_jittered(tmp_path):
    client, _ = make_client(tmp_path, lambda u, n: ok({}),
                            backoff_base=1.0, backoff_cap=60.0)

    # Each attempt's window is strictly above the previous one's.
    for attempt in range(5):
        base = 1.0 * (2 ** attempt)
        samples = [client.backoff_delay(attempt) for _ in range(50)]
        assert all(base / 2.0 <= d <= base for d in samples)

    # Jitter is real, not a constant. Without it, parallel workers retry in
    # lockstep and recreate the burst that caused the 429.
    assert len(set(client.backoff_delay(3) for _ in range(50))) > 1


def test_backoff_is_capped(tmp_path):
    client, _ = make_client(tmp_path, lambda u, n: ok({}),
                            backoff_base=1.0, backoff_cap=10.0)
    assert all(client.backoff_delay(20) <= 10.0 for _ in range(50))


def test_a_retry_that_eventually_succeeds_returns_the_data(tmp_path):
    def handler(url, n):
        return Response(503, "down") if n < 3 else ok({"v": "recovered"})

    client, transport = make_client(tmp_path, handler, max_attempts=5)
    assert client.fetch_json("https://pncp.gov.br/api/consulta/v1/r", FAMILY_A) == {"v": "recovered"}
    assert transport.count == 3
    # The two 503s are still on the record even though the call succeeded.
    assert len(client.failures) == 2


# --------------------------------------------------------------------------
# 3. FALLBACK BETWEEN FAMILIES
# --------------------------------------------------------------------------

def test_listing_falls_back_to_the_second_route_when_the_first_dies(tmp_path):
    def handler(url, n):
        if "publicacao" in url:
            return Response(500, "Erro na comunicacao com o banco de dados.")
        return ok(listing_payload(3, 1, 50))

    client, transport = make_client(tmp_path, handler, max_attempts=2)
    payload, family = client.fetch_page("20260915", 6, 1, 50)

    assert len(payload["data"]) == 3
    assert family == FAMILY_A
    assert any("atualizacao" in u for u in transport.calls)
    # The primary's failures survive the successful fallback.
    assert [f.status for f in client.failures] == [500, 500]


def test_family_b_only_calls_raise_loudly_when_b_is_down(tmp_path):
    """Items have no Family A equivalent -- /itens under api/consulta/v1 is a
    404. So when B is down there is nothing to fall back to, and returning []
    would tell the five filters that a tender has no items. It must raise."""
    client, _ = make_client(tmp_path, lambda u, n: Response(503, "no server"),
                            max_attempts=2)

    for call in (
        lambda: client.itens("01599409000139", 2026, 24),
        lambda: client.resultado_item("01599409000139", 2026, 24, 1),
        lambda: client.arquivos("01599409000139", 2026, 24),
    ):
        with pytest.raises(Unavailable) as exc:
            call()
        assert all(f.status == 503 for f in exc.value.failures)
        assert all(f.family == FAMILY_B for f in exc.value.failures)


def test_family_b_urls_are_built_against_the_portal_api(tmp_path):
    client, transport = make_client(tmp_path, lambda u, n: ok({"data": []}))
    client.itens("01599409000139", 2026, 24)
    client.resultado_item("01599409000139", 2026, 24, 7)
    client.arquivos("01599409000139", 2026, 24)

    assert transport.calls[0].startswith(
        "https://pncp.gov.br/api/pncp/v1/orgaos/01599409000139/compras/2026/24/itens")
    assert transport.calls[1].endswith("/itens/7/resultados")
    assert "/arquivos" in transport.calls[2]


# --------------------------------------------------------------------------
# 4. CURSOR RESUME
# --------------------------------------------------------------------------

def test_kill_mid_harvest_then_resume_loses_nothing_and_duplicates_nothing(tmp_path):
    """Kill the process partway through and restart it.

    The sink is a real JSONL file, so 'no duplicates' is checked against what
    actually landed on disk -- not against an in-memory list that a crash
    would have thrown away anyway.
    """
    total = 220
    page_size = 50
    out = str(tmp_path / "rows.jsonl")

    def handler(url, n):
        return page_of(url, total, page_size, prefix="M6")

    class Kill(Exception):
        pass

    # --- run 1: die after 120 rows have been written and fsynced
    client, transport = make_client(tmp_path, handler)
    sink1 = jsonl_sink(out)
    written = {"n": 0}

    def killing_sink(row):
        if written["n"] >= 120:
            raise Kill("process killed mid-page")
        sink1(row)
        written["n"] += 1

    with pytest.raises(Kill):
        client.harvest_day("20260915", (6,), page_size=page_size,
                           sink=killing_sink, reconcile_with=out)
    sink1.close()
    assert written["n"] == 120
    calls_run1 = transport.count

    # --- run 2: fresh client, same dirs, same sink file
    client2, transport2 = make_client(tmp_path, handler)
    sink2 = jsonl_sink(out)
    report = client2.harvest_day("20260915", (6,), page_size=page_size,
                                 sink=sink2, reconcile_with=out)
    sink2.close()

    lines = [json.loads(l) for l in open(out, encoding="utf-8") if l.strip()]
    keys = [r["numeroControlePNCP"] for r in lines]

    assert len(keys) == total, "no rows lost"
    assert len(set(keys)) == total, "no rows duplicated"
    assert report.rows_total == total
    assert report.complete, report.summary()
    # Resume re-read pages from cache rather than refetching them.
    assert transport2.count < calls_run1


def test_resume_refetches_nothing_that_was_already_cached(tmp_path):
    total, page_size = 120, 50
    out = str(tmp_path / "rows.jsonl")
    handler = lambda u, n: page_of(u, total, page_size, prefix="M6")  # noqa: E731

    client, transport = make_client(tmp_path, handler)
    sink = jsonl_sink(out)
    client.harvest_day("20260915", (6,), page_size=page_size, sink=sink,
                       reconcile_with=out)
    sink.close()

    client2, transport2 = make_client(tmp_path, handler)
    sink2 = jsonl_sink(out)
    report = client2.harvest_day("20260915", (6,), page_size=page_size,
                                 sink=sink2, reconcile_with=out)
    sink2.close()

    assert transport2.count == 0
    assert report.rows_new == 0
    lines = [l for l in open(out, encoding="utf-8") if l.strip()]
    assert len(lines) == total, "a resume must not append the rows again"


def test_cursor_state_is_written_atomically_and_reloads(tmp_path):
    path = str(tmp_path / "cur.json")
    c = Cursor(path)
    c.expected_rows[6] = 100
    c.expected_pages[6] = 2
    c.seen_keys.update({"a", "b", "c"})
    c.mark_done(6, 1)
    c.flush()
    assert not os.path.exists(path + ".tmp"), "no temp file left behind"

    again = Cursor(path)
    assert again.is_done(6, 1)
    assert again.seen_keys == {"a", "b", "c"}
    assert again.expected_rows == {6: 100}
    assert again.rows_committed == 3


def test_a_truncated_sink_line_does_not_break_recovery(tmp_path):
    """A process killed mid-write leaves a half line. Refusing to read the
    file because of it would be worse than skipping that one row."""
    out = str(tmp_path / "rows.jsonl")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"numeroControlePNCP": "A-1"}) + "\n")
        fh.write('{"numeroControlePNCP": "A-2"')   # killed here
    assert keys_in_jsonl(out) == {"A-1"}


def test_dedupe_uses_the_tender_key_not_the_page_number(tmp_path):
    """Page numbers are not identity. If a fallback route returns the same
    tenders in a different order, 'page 3' is not the same set twice."""
    out = str(tmp_path / "rows.jsonl")
    page_size = 50

    def handler(url, n):
        # Same 60 tenders, but the pages are sliced differently the second
        # time the harvest runs against a fresh cache.
        return page_of(url, 60, page_size, prefix="SAME")

    client, transport = make_client(tmp_path, handler)
    sink = jsonl_sink(out)
    client.harvest_day("20260915", (6,), page_size=page_size, sink=sink,
                       reconcile_with=out)
    sink.close()

    # A different day key -> a different cursor, but the same tenders.
    client2, transport2 = make_client(tmp_path / "other", handler)
    sink2 = jsonl_sink(out)
    report = client2.harvest_day("20260916", (6,), page_size=page_size,
                                 sink=sink2, reconcile_with=out)
    sink2.close()

    assert report.rows_new == 0, "seen keys recovered from the sink file"
    assert report.rows_duplicate == 60
    lines = [l for l in open(out, encoding="utf-8") if l.strip()]
    assert len(lines) == 60


# --------------------------------------------------------------------------
# 5. FAILURES ARE RECORDED, NOT SWALLOWED
# --------------------------------------------------------------------------

def test_a_dead_page_is_recorded_with_its_status_code(tmp_path):
    """One page of three dies. The harvest keeps the other two AND says so."""
    total, page_size = 150, 50

    def handler(url, n):
        if "pagina=2" in url:
            return Response(503, "no server is available")
        return page_of(url, total, page_size, prefix="M6")

    client, _ = make_client(tmp_path, handler, max_attempts=2)
    rows = []
    report = client.harvest_day("20260915", (6,), page_size=page_size,
                                sink=rows.append)

    assert report.rows_total == 100, "the surviving pages are kept"
    assert report.total_expected == 150
    assert report.missing == 50
    assert report.suspected_outage is True
    assert report.complete is False
    # Both routes for page 2 were tried, twice each, and all four are recorded.
    assert report.failures_by_status() == {503: 4}
    assert "SUSPECTED OUTAGE" in report.summary()


def test_a_short_harvest_is_never_reported_as_a_quiet_market(tmp_path):
    """The business rule: fewer tenders than expected is a SUSPECTED OUTAGE."""
    def handler(url, n):
        payload = listing_payload(500, 1, 50, prefix="M6")
        payload["totalPaginas"] = 1          # server understates the pages
        return ok(payload)

    client, _ = make_client(tmp_path, handler)
    report = client.harvest_day("20260915", (6,), page_size=50, sink=lambda r: None)

    assert report.rows_total == 50
    assert report.total_expected == 500
    assert report.missing == 450
    assert report.suspected_outage is True


def test_an_entirely_unreachable_modalidade_is_loud(tmp_path):
    """The worst case: we do not even learn what we are missing."""
    def handler(url, n):
        mod = int(url.split("codigoModalidadeContratacao=")[1].split("&")[0])
        if mod == 8:
            return Response(503, "down")
        return page_of(url, 20, 50, prefix=f"M{mod}")

    client, _ = make_client(tmp_path, handler, max_attempts=2)
    report = client.harvest_day("20260915", (6, 7, 8), page_size=50,
                                sink=lambda r: None)

    assert 8 not in report.expected_rows, "we never learned modalidade 8's size"
    assert report.suspected_outage is True
    assert report.failures_by_status()[503] == 4
    events = [e["event"] for e in client.events]
    assert "modalidade_unreachable" in events
    assert "SUSPECTED_OUTAGE" in events


def test_every_failure_is_written_to_the_event_log_with_its_status(tmp_path):
    client, _ = make_client(tmp_path, lambda u, n: Response(502, "bad gateway"),
                            max_attempts=3)
    with pytest.raises(Unavailable):
        client.fetch_json("https://pncp.gov.br/api/pncp/v1/itens", FAMILY_B)

    logged = [json.loads(l) for l in open(client.events_path, encoding="utf-8")]
    fails = [e for e in logged if e["event"] == "fetch_fail"]
    assert len(fails) == 3
    assert all(e["status"] == 502 for e in fails)
    assert all(e["family"] == FAMILY_B for e in fails)


def test_the_log_records_which_family_served_each_row(tmp_path):
    """Requirement 5. When the families invert, this is the evidence."""
    client, _ = make_client(tmp_path, lambda u, n: page_of(u, 3, 50, "M6"))
    report = client.harvest_day("20260915", (6,), page_size=50, sink=lambda r: None)

    rows = [e for e in client.events if e["event"] == "row"]
    assert len(rows) == 3
    assert {e["family"] for e in rows} == {FAMILY_A}
    assert report.served_by == {FAMILY_A: 3}


def test_failures_survive_into_the_next_process(tmp_path):
    """An outage recorded on Monday must still be visible on Tuesday."""
    def handler(url, n):
        if "pagina=2" in url:
            return Response(503, "down")
        return page_of(url, 150, 50, prefix="M6")

    client, _ = make_client(tmp_path, handler, max_attempts=1)
    client.harvest_day("20260915", (6,), page_size=50, sink=lambda r: None)

    client2, _ = make_client(tmp_path, handler, max_attempts=1)
    report = client2.harvest_day("20260915", (6,), page_size=50, sink=lambda r: None)
    assert report.failures, "the cursor carries the failure list forward"
    assert report.suspected_outage is True


# --------------------------------------------------------------------------
# 6. THE NON-NEGOTIABLES
# --------------------------------------------------------------------------

def test_a_browser_user_agent_is_always_sent():
    """Several endpoints behave differently without one."""
    import harvest.pncp_client as mod
    assert "Mozilla/5.0" in USER_AGENT

    class FakeSession(object):
        def __init__(self):
            self.headers = {}

        def get(self, url, timeout=None):
            raise AssertionError("not reached")

    real = mod.requests
    try:
        mod.requests = type("R", (), {"Session": FakeSession})
        t = mod.RequestsTransport()
        assert t.session.headers["User-Agent"] == USER_AGENT
    finally:
        mod.requests = real


def test_tls_verification_can_not_be_turned_off():
    """There must be no code path that reaches verify=False. HTTPS here goes
    through a proxy with a CA bundle; a connection error means backoff."""
    source = open(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "harvest", "pncp_client.py"), encoding="utf-8").read()
    code = "\n".join(l for l in source.splitlines()
                     if not l.strip().startswith("#"))
    assert "verify=False" not in code
    assert "verify = False" not in code
    assert "CERT_NONE" not in code


@pytest.mark.parametrize("bad", [0, 1, 9, 51, 100, 500])
def test_page_size_outside_the_measured_window_is_refused(tmp_path, bad):
    """Measured: <10 gives 400 'must be greater than or equal to 10';
    >50 gives 400 'Tamanho de pagina invalido'. Fail before the request."""
    client, transport = make_client(tmp_path, lambda u, n: ok({}))
    with pytest.raises(ValueError):
        client.harvest_day("20260915", (6,), page_size=bad, sink=lambda r: None)
    assert transport.count == 0


def test_paging_fields_match_the_live_api(tmp_path):
    """Guards against someone 'tidying' the field names. Verified live."""
    payload = listing_payload(137, 1, 50)
    assert set(payload) == {"data", "totalRegistros", "totalPaginas",
                            "numeroPagina", "paginasRestantes", "empty"}

    client, _ = make_client(tmp_path, lambda u, n: page_of(u, 137, 50, "M6"))
    report = client.harvest_day("20260915", (6,), page_size=50, sink=lambda r: None)
    assert report.expected_rows == {6: 137}
    assert report.expected_pages == {6: 3}
    assert report.rows_total == 137


def test_max_pages_caps_the_expectation_so_a_smoke_test_is_not_a_fake_outage(tmp_path):
    client, _ = make_client(tmp_path, lambda u, n: page_of(u, 1719, 50, "M6"))
    report = client.harvest_day("20260915", (6,), page_size=50, max_pages=2,
                                sink=lambda r: None)
    assert report.rows_total == 100
    assert report.total_expected == 100
    assert report.complete is True, "a capped descent is not an outage"


def test_rate_limiter_spaces_requests(tmp_path):
    """Measured: ~30 requests in a burst earns a 429 for ~30s, shared across
    both families. The floor delay is what keeps a long descent alive."""
    import time as real_time
    client, _ = make_client(tmp_path, lambda u, n: ok({"v": n}), min_interval=0.05)
    start = real_time.time()
    for i in range(5):
        client.fetch_json(f"https://pncp.gov.br/api/consulta/v1/a?i={i}", FAMILY_A)
    assert real_time.time() - start >= 0.15


def test_cache_directory_comes_from_the_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("ACOLHE_CACHE", str(tmp_path / "from-env"))
    cache = DiskCache()
    assert cache.directory == str(tmp_path / "from-env")
    assert os.path.isdir(cache.directory)
