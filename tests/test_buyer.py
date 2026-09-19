"""
Tests for the SICONFI buyer payment-risk screen.

Nothing here touches the network. The transport is a stub: every test states
exactly what SICONFI returns, including the ugly real-world shapes -- omitted
zero rows, missing periods, timeouts, 429 storms.

The tests that matter most are the ones asserting that a buyer we could not
measure never comes back as passed=True. That is the failure mode that costs
real money.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen.buyer import (  # noqa: E402
    PASS,
    REJECT,
    RISK_DELAY,
    RISK_WRITE_OFF,
    UNSCREENABLE,
    EnteDirectory,
    RestosAPagar,
    RetryPolicy,
    ScreenRequest,
    SiconfiClient,
    SiconfiUnavailable,
    Thresholds,
    parse_anexo07,
    rreo_anexo07_url,
    screen_buyer,
    screen_figures,
)


# --------------------------------------------------------------------------
# Fixtures: SICONFI payloads shaped exactly like the live ones
# --------------------------------------------------------------------------

PREFIX = "RestosAPagarProcessadosENaoProcessadosLiquidados"


def row(cod_conta, valor, conta="TOTAL (III) = (I + II)", coluna="x"):
    return {
        "exercicio": 2026, "demonstrativo": "RREO", "periodo": 3,
        "instituicao": "Prefeitura Municipal de Teste", "cod_ibge": 9999999,
        "uf": "AM", "anexo": "RREO-Anexo 07", "esfera": "M",
        "coluna": coluna, "cod_conta": cod_conta, "conta": conta, "valor": valor,
    }


def anexo07(inscritos_ant=0.0, inscritos_prev=0.0, pagos=None, cancelados=0.0, saldo=None,
            extra_noise=True):
    """Build an Anexo 07 payload. `pagos=None` omits the row, as SICONFI does."""
    items = []
    items.append(row(PREFIX + "InscritosEmExerciciosAnteriores", inscritos_ant))
    items.append(row(PREFIX + "InscritosEmExercicioAnterior", inscritos_prev))
    if pagos is not None:
        items.append(row(PREFIX + "Pagos", pagos))
    items.append(row(PREFIX + "Cancelados", cancelados))
    if saldo is not None:
        items.append(row(PREFIX + "APagar", saldo))
    if extra_noise:
        # Rows the parser must ignore: sub-totals by Poder, and the entirely
        # separate "nao processados" block.
        items.append(row(PREFIX + "APagar", 1_000_000.0, conta="PODER EXECUTIVO"))
        items.append(row(PREFIX + "APagar", 5_000.0, conta="PODER LEGISLATIVO"))
        items.append(row("RestosAPagarNaoProcessadosAPagar", 777_777.0))
        items.append(row("SaldoTotal", 123.0))
    return {"items": items, "hasMore": False, "count": len(items)}


def make_client(responses, retry=None):
    """A SiconfiClient whose transport serves a dict of url -> outcome."""
    calls = []

    def transport(url, timeout):
        calls.append(url)
        outcome = responses.get(url, {"items": [], "count": 0})
        if isinstance(outcome, Exception):
            raise outcome
        if isinstance(outcome, int):
            return (outcome, b"")
        if callable(outcome):
            return outcome(url, len(calls))
        return (200, json.dumps(outcome).encode("utf-8"))

    client = SiconfiClient(
        transport=transport,
        retry=retry or RetryPolicy(attempts=4, base_delay=0, max_delay=0),
        cache_dir=None,
        sleep=lambda _s: None,
    )
    client.seen = calls
    return client


@pytest.fixture(autouse=True)
def isolated_cache(tmp_path, monkeypatch):
    """Never read or write the developer's real cache during tests."""
    monkeypatch.setenv("ACOLHE_CACHE", str(tmp_path / "cache"))


# --------------------------------------------------------------------------
# The rule itself
# --------------------------------------------------------------------------


def test_good_payer_passes():
    figures = RestosAPagar(inscritos=1_000_000, pagos=950_000, cancelados=0, saldo=50_000,
                           ente="Paracatu/MG")
    passed, reason, evidence = screen_figures(figures)
    assert passed is True
    assert evidence["outcome"] == PASS
    assert evidence["risks"] == []
    assert evidence["saldo_ratio"] == pytest.approx(0.05)
    assert "95.0%" in reason


def test_slow_payer_rejected_for_delay_not_write_off():
    """The central distinction: owed-but-not-cancelled is a delay problem."""
    figures = RestosAPagar(inscritos=1_000_000, pagos=500_000, cancelados=0, saldo=500_000,
                           ente="Coari/AM")
    passed, reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == REJECT
    assert evidence["risks"] == [RISK_DELAY]
    assert "DELAY RISK" in reason
    assert "WRITE-OFF RISK" not in reason
    assert "working-capital" in reason


def test_canceller_rejected_for_write_off_even_when_prompt():
    """Pays fast but tears up 5% of invoices: a lost-sale problem, not a slow one."""
    figures = RestosAPagar(inscritos=1_000_000, pagos=950_000, cancelados=50_000, saldo=0,
                           ente="Cancelandia/XX")
    passed, reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["risks"] == [RISK_WRITE_OFF]
    assert "WRITE-OFF RISK" in reason
    assert "DELAY RISK" not in reason
    assert "lost sale" in reason


def test_both_risks_are_reported_separately():
    figures = RestosAPagar(inscritos=1_000_000, pagos=400_000, cancelados=100_000, saldo=500_000)
    passed, reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["risks"] == [RISK_DELAY, RISK_WRITE_OFF]
    assert "DELAY RISK" in reason and "WRITE-OFF RISK" in reason


def test_thresholds_are_boundaries_not_hardcoded():
    at_limit = RestosAPagar(inscritos=1_000_000, pagos=700_000, cancelados=0, saldo=300_000)
    assert screen_figures(at_limit)[0] is True          # exactly 0.30 passes
    over = RestosAPagar(inscritos=1_000_000, pagos=699_000, cancelados=0, saldo=301_000)
    assert screen_figures(over)[0] is False


def test_thresholds_are_configurable():
    figures = RestosAPagar(inscritos=1_000_000, pagos=500_000, cancelados=0, saldo=500_000)
    assert screen_figures(figures)[0] is False
    lenient = Thresholds(max_saldo_ratio=0.60)
    passed, _reason, evidence = screen_figures(figures, lenient)
    assert passed is True
    assert evidence["thresholds"]["max_saldo_ratio"] == 0.60


def test_cancelados_threshold_is_configurable():
    figures = RestosAPagar(inscritos=1_000_000, pagos=970_000, cancelados=30_000, saldo=0)
    assert screen_figures(figures)[0] is False
    assert screen_figures(figures, Thresholds(max_cancelados_ratio=0.05))[0] is True


def test_evidence_carries_every_raw_number_for_audit():
    figures = RestosAPagar(inscritos=1_000_000, pagos=500_000, cancelados=10_000, saldo=490_000,
                           source_url="https://example/x", ente="X/AM", exercicio=2026, periodo=3)
    _passed, _reason, evidence = screen_figures(figures)
    for key in ("inscritos_brl", "pagos_brl", "cancelados_brl", "saldo_brl",
                "saldo_ratio", "cancelados_ratio", "paid_ratio", "source_url",
                "thresholds", "ente", "exercicio", "periodo", "outcome"):
        assert key in evidence, key
    assert evidence["source_url"] == "https://example/x"
    json.dumps(evidence)  # must stay serialisable for the bid log


# --------------------------------------------------------------------------
# Unscreenable is a THIRD outcome. None of these may pass.
# --------------------------------------------------------------------------


def test_zero_inscritos_is_unscreenable_not_a_pass():
    figures = RestosAPagar(inscritos=0, pagos=0, cancelados=0, saldo=0, ente="Vazio/XX")
    passed, reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE
    assert "CANNOT BE SCREENED" in reason
    assert evidence["saldo_ratio"] is None


def test_tiny_base_is_unscreenable():
    figures = RestosAPagar(inscritos=400, pagos=0, cancelados=0, saldo=400)
    passed, _reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE


def test_negative_figures_are_unscreenable():
    figures = RestosAPagar(inscritos=-5, pagos=0, cancelados=0, saldo=0)
    passed, _r, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE


def test_missing_figures_are_unscreenable():
    figures = RestosAPagar(inscritos=None, pagos=None, cancelados=0, saldo=None)
    passed, _r, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE


@pytest.mark.parametrize("figures", [
    RestosAPagar(inscritos=0, pagos=0, cancelados=0, saldo=0),
    RestosAPagar(inscritos=None, pagos=None, cancelados=0, saldo=None),
    RestosAPagar(inscritos=-1, pagos=0, cancelados=0, saldo=0),
    RestosAPagar(inscritos=10, pagos=10, cancelados=0, saldo=0),
])
def test_no_degenerate_input_ever_passes(figures):
    """The money-losing failure mode, asserted directly."""
    assert screen_figures(figures)[0] is False


# --------------------------------------------------------------------------
# Parsing the real payload shape
# --------------------------------------------------------------------------


def test_parser_ignores_poder_subtotals_and_the_nao_processados_block():
    payload = anexo07(inscritos_ant=0, inscritos_prev=1_000_000, pagos=900_000,
                      cancelados=0, saldo=100_000)
    figures = parse_anexo07(payload)
    assert figures.inscritos == 1_000_000
    assert figures.saldo == 100_000       # not the 1,000,000 PODER EXECUTIVO row
    assert figures.pagos == 900_000


def test_inscritos_sums_both_vintage_columns():
    payload = anexo07(inscritos_ant=11_591.36, inscritos_prev=2_901_930.95,
                      cancelados=17_964.48, saldo=2_895_557.83)
    figures = parse_anexo07(payload)
    assert figures.inscritos == pytest.approx(2_913_522.31)


def test_omitted_pagos_row_means_zero_paid_not_missing_data():
    """
    THE TRAP. SICONFI drops zero-valued rows, so a municipality that paid
    nothing has no 'Pagos' row at all. Nhamundá/AM is exactly this shape.
    Reading the absence as 'no data' would quietly excuse the worst payers.
    """
    payload = anexo07(inscritos_ant=11_591.36, inscritos_prev=2_901_930.95,
                      pagos=None, cancelados=17_964.48, saldo=2_895_557.83)
    figures = parse_anexo07(payload, ente="Nhamunda/AM")
    assert figures.pagos == pytest.approx(0.0)
    assert figures.pagos_source == "derived"

    passed, reason, evidence = screen_figures(figures)
    assert passed is False
    assert evidence["outcome"] == REJECT
    assert evidence["paid_ratio"] == pytest.approx(0.0)
    assert evidence["saldo_ratio"] > 0.30
    assert "0.0%" in reason


def test_derived_pagos_matches_published_pagos_when_both_available():
    """The identity the derivation rests on: c = (a + b) - d - e."""
    with_pagos = parse_anexo07(anexo07(inscritos_ant=1_537.24, inscritos_prev=9_359_359.52,
                                       pagos=9_225_149.81, cancelados=0.0, saldo=135_746.95))
    without = parse_anexo07(anexo07(inscritos_ant=1_537.24, inscritos_prev=9_359_359.52,
                                    pagos=None, cancelados=0.0, saldo=135_746.95))
    assert with_pagos.pagos == pytest.approx(without.pagos, abs=0.01)
    assert with_pagos.pagos_source == "published"
    assert without.pagos_source == "derived"


def test_inconsistent_published_figures_are_flagged():
    payload = anexo07(inscritos_prev=1_000_000, pagos=10.0, cancelados=0.0, saldo=100_000)
    figures = parse_anexo07(payload)
    assert figures.pagos_source == "published_inconsistent"


def test_empty_payload_parses_to_none():
    assert parse_anexo07({"items": [], "count": 0}) is None


def test_url_is_built_exactly_as_siconfi_expects():
    url = rreo_anexo07_url(1303007, 2026, 3)
    assert url.startswith("https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?")
    assert "no_anexo=RREO-Anexo+07" in url or "no_anexo=RREO-Anexo%2007" in url
    assert "id_ente=1303007" in url
    assert "co_esfera=M" in url
    assert "an_exercicio=2026" in url and "nr_periodo=3" in url


# --------------------------------------------------------------------------
# Transport: cache, backoff, TLS, User-Agent
# --------------------------------------------------------------------------


def test_disk_cache_means_a_rerun_costs_zero_calls(tmp_path):
    url = "https://example.test/a"
    client = make_client({url: {"items": [1], "count": 1}})
    client._cache_dir = str(tmp_path)

    assert client.get_json(url) == {"items": [1], "count": 1}
    assert client.calls_made == 1

    again = SiconfiClient(transport=client.transport, cache_dir=str(tmp_path), sleep=lambda _s: None)
    assert again.get_json(url) == {"items": [1], "count": 1}
    assert again.calls_made == 0
    assert again.cache_hits == 1


def test_cache_is_keyed_by_url(tmp_path):
    client = make_client({
        "https://example.test/a": {"v": "a"},
        "https://example.test/b": {"v": "b"},
    })
    client._cache_dir = str(tmp_path)
    assert client.get_json("https://example.test/a") == {"v": "a"}
    assert client.get_json("https://example.test/b") == {"v": "b"}
    assert client.get_json("https://example.test/a") == {"v": "a"}
    assert client.calls_made == 2


def test_cache_dir_comes_from_acolhe_cache_env(tmp_path, monkeypatch):
    target = tmp_path / "from-env"
    monkeypatch.setenv("ACOLHE_CACHE", str(target))
    client = make_client({"https://example.test/a": {"v": 1}})
    client.get_json("https://example.test/a")
    assert (target / "siconfi").is_dir()
    assert list((target / "siconfi").glob("*.json"))


def test_corrupt_cache_entry_is_refetched_not_fatal(tmp_path):
    url = "https://example.test/a"
    client = make_client({url: {"v": 1}})
    client._cache_dir = str(tmp_path)
    client.get_json(url)
    stale = list((tmp_path / "siconfi").glob("*.json"))[0]
    stale.write_text("{ this is not json")
    fresh = make_client({url: {"v": 1}})
    fresh._cache_dir = str(tmp_path)
    assert fresh.get_json(url) == {"v": 1}


def test_retries_on_500_then_succeeds():
    url = "https://example.test/flaky"
    def flaky(_url, n):
        if n < 3:
            return (500, b"boom")
        return (200, json.dumps({"ok": True}).encode())
    client = make_client({url: flaky})
    client._cache_dir = None
    assert client.get_json(url) == {"ok": True}
    assert client.calls_made == 3


def test_retries_on_429():
    url = "https://example.test/throttled"
    def throttled(_url, n):
        return (200, b'{"ok":1}') if n >= 2 else (429, b"slow down")
    client = make_client({url: throttled})
    assert client.get_json(url) == {"ok": 1}


def test_retries_on_timeout_which_is_what_http_000_really_is():
    url = "https://example.test/slow"
    def sometimes(_url, n):
        if n < 2:
            raise SiconfiUnavailable("TimeoutError: timed out")
        return (200, b'{"ok":1}')
    client = make_client({url: sometimes})
    assert client.get_json(url) == {"ok": 1}


def test_gives_up_after_attempts_and_raises_rather_than_returning_empty():
    url = "https://example.test/dead"
    client = make_client({url: 503})
    with pytest.raises(SiconfiUnavailable):
        client.get_json(url)
    assert client.calls_made == 4


def test_404_is_not_retried():
    url = "https://example.test/gone"
    client = make_client({url: 404})
    with pytest.raises(SiconfiUnavailable):
        client.get_json(url)
    assert client.calls_made == 1


def test_html_error_page_with_status_200_is_not_accepted_as_data():
    url = "https://example.test/html"
    client = make_client({url: lambda _u, _n: (200, b"<html>gateway error</html>")})
    with pytest.raises(SiconfiUnavailable):
        client.get_json(url)


def test_backoff_delays_grow_and_are_jittered():
    delays = []
    url = "https://example.test/dead"
    client = SiconfiClient(
        transport=lambda _u, _t: (500, b""),
        retry=RetryPolicy(attempts=5, base_delay=1.0, max_delay=30.0),
        sleep=delays.append,
    )
    with pytest.raises(SiconfiUnavailable):
        client.get_json(url)
    assert len(delays) == 4
    # Full jitter: each delay sits inside its own exponentially growing ceiling.
    for i, delay in enumerate(delays, start=1):
        assert 0 <= delay <= min(30.0, 1.0 * (2 ** i))
    assert delays[-1] >= 0


def test_browser_user_agent_is_sent():
    from screen.buyer import USER_AGENT
    assert "Mozilla/5.0" in USER_AGENT


def test_tls_verification_is_never_disabled():
    """Guard against someone 'fixing' a timeout with verify=False."""
    source = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "screen", "buyer.py")).read()
    assert "verify=False" not in source
    assert "_create_unverified_context" not in source
    assert "CERT_NONE" not in source


# --------------------------------------------------------------------------
# CNPJ -> IBGE resolution
# --------------------------------------------------------------------------


ENTES = {"items": [
    {"cod_ibge": 1303007, "ente": "Nhamundá", "uf": "AM", "esfera": "M",
     "cnpj": "04283578000153", "populacao": 21251, "exercicio": 2026},
    {"cod_ibge": 3147006, "ente": "Paracatu", "uf": "MG", "esfera": "M",
     "cnpj": "18278051000145", "populacao": 99005, "exercicio": 2026},
], "count": 2, "hasMore": False}


def entes_client(extra=None):
    from screen.buyer import entes_url
    responses = {entes_url(): ENTES}
    responses.update(extra or {})
    return make_client(responses)


def test_cnpj_resolves_to_ibge():
    directory = EnteDirectory(entes_client())
    assert directory.ibge_for_cnpj("04283578000153") == 1303007


def test_cnpj_resolves_when_punctuated():
    directory = EnteDirectory(entes_client())
    assert directory.ibge_for_cnpj("04.283.578/0001-53") == 1303007


def test_entes_table_is_fetched_once_and_cached(tmp_path):
    client = entes_client()
    client._cache_dir = str(tmp_path)
    directory = EnteDirectory(client)
    directory.ibge_for_cnpj("04283578000153")
    directory.ibge_for_cnpj("18278051000145")
    directory.by_ibge(1303007)
    assert client.calls_made == 1


def test_unknown_cnpj_resolves_to_none():
    directory = EnteDirectory(entes_client())
    assert directory.ibge_for_cnpj("99999999999999") is None


def test_name_lookup_is_accent_insensitive():
    directory = EnteDirectory(entes_client())
    assert directory.by_name("nhamunda", "AM")["cod_ibge"] == 1303007
    assert directory.by_name("Nhamundá", "am")["cod_ibge"] == 1303007


# --------------------------------------------------------------------------
# End to end, still with no network
# --------------------------------------------------------------------------


def screen_with(anexo_payload, cnpj="04283578000153", exercicio=2026, periodo=3, **kw):
    from screen.buyer import entes_url
    record = [i for i in ENTES["items"] if i["cnpj"] == cnpj]
    ibge = record[0]["cod_ibge"] if record else 1303007
    url = rreo_anexo07_url(ibge, exercicio, periodo)
    client = entes_client({url: anexo_payload})
    request = ScreenRequest(cnpj=cnpj, exercicio=exercicio, periodo=periodo, **kw)
    return screen_buyer(request, client, EnteDirectory(client))


def test_end_to_end_reject_for_the_nhamunda_shape():
    payload = anexo07(inscritos_ant=11_591.36, inscritos_prev=2_901_930.95,
                      pagos=None, cancelados=17_964.48, saldo=2_895_557.83)
    passed, reason, evidence = screen_with(payload)
    assert passed is False
    assert evidence["outcome"] == REJECT
    assert RISK_DELAY in evidence["risks"]
    assert evidence["cod_ibge"] == 1303007
    assert evidence["paid_ratio"] == pytest.approx(0.0)
    assert "Nhamundá/AM" in reason


def test_end_to_end_pass():
    payload = anexo07(inscritos_ant=1_537.24, inscritos_prev=9_359_359.52,
                      pagos=9_225_149.81, cancelados=0.0, saldo=135_746.95)
    passed, _reason, evidence = screen_with(payload, cnpj="18278051000145")
    assert passed is True
    assert evidence["outcome"] == PASS


def test_unknown_cnpj_is_unscreenable_not_a_pass():
    passed, reason, evidence = screen_with(anexo07(), cnpj="11111111111111")
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE
    assert "not in the SICONFI entes table" in reason


def test_no_data_for_the_period_is_unscreenable_not_a_pass():
    """Every period comes back empty -- the ente filed nothing."""
    passed, reason, evidence = screen_with({"items": [], "count": 0})
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE
    assert "has not published RREO Anexo 07" in reason
    assert len(evidence["urls_tried"]) == 3


def test_falls_back_to_an_earlier_period_and_records_which_one():
    from screen.buyer import entes_url
    good = anexo07(inscritos_prev=1_000_000, pagos=900_000, cancelados=0, saldo=100_000)
    client = entes_client({
        rreo_anexo07_url(1303007, 2026, 3): {"items": [], "count": 0},
        rreo_anexo07_url(1303007, 2026, 2): {"items": [], "count": 0},
        rreo_anexo07_url(1303007, 2026, 1): good,
    })
    passed, _reason, evidence = screen_buyer(
        ScreenRequest(cnpj="04283578000153"), client, EnteDirectory(client))
    assert passed is True
    assert evidence["periodo"] == 1
    assert len(evidence["urls_tried"]) == 3


def test_api_down_is_unscreenable_not_a_pass():
    from screen.buyer import entes_url
    url = rreo_anexo07_url(1303007, 2026, 3)
    client = make_client({entes_url(): ENTES, url: 503})
    passed, reason, evidence = screen_buyer(
        ScreenRequest(cnpj="04283578000153"), client, EnteDirectory(client))
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE
    assert "SICONFI did not answer" in reason


def test_entes_table_down_is_unscreenable_not_a_pass():
    from screen.buyer import entes_url
    client = make_client({entes_url(): 500})
    passed, reason, evidence = screen_buyer(
        ScreenRequest(cnpj="04283578000153"), client, EnteDirectory(client))
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE
    assert "entes table" in reason


def test_empty_entes_table_is_unscreenable_not_a_pass():
    from screen.buyer import entes_url
    client = make_client({entes_url(): {"items": [], "count": 0}})
    passed, _reason, evidence = screen_buyer(
        ScreenRequest(cnpj="04283578000153"), client, EnteDirectory(client))
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE


def test_screening_by_ibge_code_needs_no_cnpj():
    payload = anexo07(inscritos_prev=1_000_000, pagos=900_000, cancelados=0, saldo=100_000)
    client = entes_client({rreo_anexo07_url(1303007, 2026, 3): payload})
    passed, _r, evidence = screen_buyer(
        ScreenRequest(cod_ibge="1303007"), client, EnteDirectory(client))
    assert passed is True
    assert evidence["ente"] == "Nhamundá/AM"


def test_neither_cnpj_nor_ibge_is_unscreenable():
    client = entes_client()
    passed, _r, evidence = screen_buyer(ScreenRequest(), client, EnteDirectory(client))
    assert passed is False
    assert evidence["outcome"] == UNSCREENABLE


def test_every_unscreenable_path_reports_passed_false():
    """One assertion covering the whole class of failures."""
    from screen.buyer import entes_url
    url = rreo_anexo07_url(1303007, 2026, 3)
    scenarios = [
        make_client({entes_url(): 500}),                                  # API down
        make_client({entes_url(): ENTES, url: 503}),                      # report fetch down
        make_client({entes_url(): ENTES, url: {"items": [], "count": 0}}),# nothing filed
        make_client({entes_url(): ENTES, url: anexo07()}),                # all zeros
    ]
    for client in scenarios:
        passed, reason, evidence = screen_buyer(
            ScreenRequest(cnpj="04283578000153"), client, EnteDirectory(client))
        assert passed is False
        assert evidence["outcome"] == UNSCREENABLE
        assert "CANNOT BE SCREENED" in reason
