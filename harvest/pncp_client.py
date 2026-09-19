"""One client for both PNCP API families, with a disk cache, a resumable
cursor, and an explicit completeness report.

WHY THIS FILE EXISTS
--------------------
PNCP exposes the tender universe behind two API families that fail
INDEPENDENTLY and unpredictably:

    Family A   api/consulta/v1   the documented public API
    Family B   api/pncp/v1       the portal's own API

A previous harvest was built against one family alone and lost a full run when
that family went down. Availability inverts without warning. So every request
in this module goes through ONE path that knows about both families, retries
with backoff, falls back where a second route can answer the same question,
and RECORDS every failure instead of quietly shortening the harvest.

MEASURED 2026-09-19, by probing the live endpoints (not from documentation):

  * A /contratacoes/publicacao   HTTP 200, ~1s.  The spine of the harvest.
  * A /contratacoes/atualizacao  HTTP 200, ~1s, but returned a 500
                                 ("Erro na comunicacao com o banco de dados")
                                 on one of four attempts. Family A is NOT
                                 uniformly healthy -- it is merely mostly up.
  * A /contratacoes/proposta     answers, but in 21-25s. A 25s timeout loses
                                 it. This is why DEFAULT_TIMEOUT is 45.
  * B every endpoint tried       HTTP 503 from the load balancer
                                 ("No server is available to handle this
                                 request"), 8 attempts out of 8, against real
                                 orgao/ano/sequencial triples taken from live
                                 Family A rows. Family B is down today, not
                                 merely rejecting our parameters.
  * tamanhoPagina is bounded: < 10 gives 400 "must be greater than or equal
    to 10", > 50 gives 400 "Tamanho de pagina invalido". The usable window is
    10..50, so a full day costs ceil(rows/50) calls, not fewer.
  * BOTH families sit behind ONE shared rate limiter. Roughly 30 requests in a
    burst earns HTTP 429 "Limite de Requisicoes Excedido" for about 30
    seconds, and the 429 carries NO Retry-After header. This is why the
    default concurrency is 2 and there is a floor delay between requests. A
    fast client here is a blocked client.

A harvest that returns fewer tenders than the API itself said exist is a
SUSPECTED OUTAGE, not a quiet market. HarvestReport carries expected-vs-got
and the failure list so a caller can tell those two apart.
"""

import collections
import hashlib
import json
import os
import random
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

try:
    import requests
except ImportError:  # pragma: no cover - requests is available in this project
    requests = None


# Several PNCP endpoints behave differently for a non-browser agent, and the
# portal has historically served different content to unknown agents. Always
# send this, on both families.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

FAMILY_A = "consulta"   # api/consulta/v1  -- documented public API
FAMILY_B = "portal"     # api/pncp/v1      -- the portal's own API

BASE_A = "https://pncp.gov.br/api/consulta/v1"
BASE_B = "https://pncp.gov.br/api/pncp/v1"

# 6 = Pregao Eletronico, 7 = Pregao Presencial, 8 = Dispensa.
MODALIDADES = (6, 7, 8)

# Measured: the server rejects anything outside this window with a 400.
MIN_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50

# Transient by nature: retrying these is correct. Anything else (400, 404) is
# our own bug or a genuinely absent record, and retrying it just burns the
# rate-limit budget that the rest of the harvest needs.
RETRY_STATUS = frozenset({429, 500, 502, 503, 504})

DEFAULT_TIMEOUT = 45          # /contratacoes/proposta measured at 21-25s.
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_BACKOFF_BASE = 1.0
DEFAULT_BACKOFF_CAP = 60.0
DEFAULT_CONCURRENCY = 2       # Measured 429 ceiling. Do not raise casually.
DEFAULT_MIN_INTERVAL = 0.35   # Floor between requests, shared across threads.

DEFAULT_CACHE = os.path.expanduser("~/.cache/acolhe/pncp")


class PNCPError(Exception):
    """Base class, so callers can catch everything this module raises."""


class Unavailable(PNCPError):
    """Every route for one logical question failed after its retry budget.

    Carries the failures so the caller can log WHICH family died with WHICH
    status, rather than seeing a bare exception and guessing.
    """

    def __init__(self, question, failures):
        self.question = question
        self.failures = list(failures)
        detail = ", ".join(f.short() for f in self.failures) or "no attempts"
        super().__init__(f"{question}: all routes failed [{detail}]")


class Failure(object):
    """One failed HTTP attempt, kept verbatim.

    Requirement 5/6: an outage must be visible. A Failure is never discarded;
    it lands in the cursor on disk and in the HarvestReport.
    """

    def __init__(self, url, family, status=None, error=None, attempt=0):
        self.url = url
        self.family = family
        self.status = status        # int, or None for a connection-level error
        self.error = error          # exception class name, for HTTP 000 cases
        self.attempt = attempt
        self.when = time.time()

    def short(self):
        return f"{self.family} {self.status or self.error}"

    def as_dict(self):
        return {
            "url": self.url,
            "family": self.family,
            "status": self.status,
            "error": self.error,
            "attempt": self.attempt,
            "when": self.when,
        }

    @staticmethod
    def from_dict(d):
        f = Failure(d["url"], d["family"], d.get("status"), d.get("error"),
                    d.get("attempt", 0))
        f.when = d.get("when", 0.0)
        return f

    def __repr__(self):
        return f"<Failure {self.family} {self.status or self.error} {self.url}>"


class Response(object):
    """What a Transport returns. Deliberately tiny so tests can fake it."""

    def __init__(self, status, body, url=""):
        self.status = status
        self.body = body            # already-decoded text
        self.url = url

    def json(self):
        return json.loads(self.body)


class RequestsTransport(object):
    """The real network. Isolated behind this class so tests can replace it.

    TLS verification is NEVER disabled. HTTPS here goes through a proxy with
    its own CA bundle, which requests picks up from REQUESTS_CA_BUNDLE /
    SSL_CERT_FILE in the environment. A connection error means timeout or
    proxy -- the fix is backoff, never verify=False. There is intentionally no
    parameter on this class that could turn verification off.
    """

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        if requests is None:  # pragma: no cover
            raise RuntimeError("requests is not installed")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        })

    def get(self, url, timeout=None):
        r = self.session.get(url, timeout=timeout or self.timeout)
        return Response(r.status_code, r.text, url)


class DiskCache(object):
    """Persistent response cache keyed by URL.

    Requirement 3: a re-run must cost ZERO network calls for data already
    held. Only successful responses are stored -- caching a 503 would freeze
    an outage into the dataset, which is exactly the failure mode this whole
    client exists to prevent.

    Entries never expire by default. A tender day that has already been
    published does not change, so re-fetching it would only spend the shared
    rate-limit budget. Pass ttl_seconds if a caller wants otherwise.
    """

    def __init__(self, directory=None, ttl_seconds=None):
        self.directory = directory or os.environ.get("ACOLHE_CACHE", DEFAULT_CACHE)
        self.ttl_seconds = ttl_seconds
        self.lock = threading.Lock()
        os.makedirs(self.directory, exist_ok=True)

    def path_for(self, url):
        key = hashlib.sha1(url.encode("utf-8")).hexdigest()
        # Shard on the first two hex chars: a full daily descent is thousands
        # of files and one flat directory gets slow to stat.
        shard = os.path.join(self.directory, key[:2])
        return os.path.join(shard, key + ".json")

    def get(self, url):
        path = self.path_for(url)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                entry = json.load(fh)
        except (OSError, ValueError):
            return None
        if self.ttl_seconds is not None:
            if time.time() - entry.get("fetched_at", 0) > self.ttl_seconds:
                return None
        return entry

    def put(self, url, family, status, payload):
        entry = {
            "url": url,
            "family": family,
            "status": status,
            "fetched_at": time.time(),
            "body": payload,
        }
        path = self.path_for(url)
        with self.lock:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(entry, fh, ensure_ascii=False)
            os.replace(tmp, path)   # atomic: a kill mid-write leaves no half file
        return entry


class Cursor(object):
    """Resumable harvest state on disk.

    Requirement 4: killing the process mid-harvest and restarting must resume
    without duplicating or losing rows.

    Two mechanisms, because either alone is not enough:
      * done_pages  -- pages already delivered to the sink, so we skip them.
      * seen_keys   -- every numeroControlePNCP already emitted. Page numbers
                       are not stable identity: if a fallback route returns
                       the same tenders in a different order, page 3 is not
                       the same set twice. Deduping on the tender's own key is
                       what actually guarantees no duplicates.

    Writes are atomic (tmp + os.replace), so a kill during a flush leaves the
    previous good state rather than a truncated file.
    """

    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.done_pages = set()     # "modalidade:pagina"
        self.seen_keys = set()
        self.expected_rows = {}     # modalidade -> totalRegistros
        self.expected_pages = {}    # modalidade -> totalPaginas
        self.failures = []
        self.served_by = collections.Counter()
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                state = json.load(fh)
        except (OSError, ValueError):
            return
        self.done_pages = set(state.get("done_pages", []))
        self.seen_keys = set(state.get("seen_keys", []))
        self.expected_rows = {int(k): v for k, v in state.get("expected_rows", {}).items()}
        self.expected_pages = {int(k): v for k, v in state.get("expected_pages", {}).items()}
        self.failures = [Failure.from_dict(d) for d in state.get("failures", [])]
        self.served_by = collections.Counter(state.get("served_by", {}))

    def flush(self):
        state = {
            "done_pages": sorted(self.done_pages),
            "seen_keys": sorted(self.seen_keys),
            "expected_rows": self.expected_rows,
            "expected_pages": self.expected_pages,
            "rows_committed": self.rows_committed,   # derived; for humans reading the file
            "failures": [f.as_dict() for f in self.failures],
            "served_by": dict(self.served_by),
        }
        with self.lock:
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.path)

    @property
    def rows_committed(self):
        """Derived, never stored.

        A separate counter can drift out of step with seen_keys after an
        abrupt kill -- the counter is lost with the unflushed page while the
        keys are recovered from the sink file. Deriving it means the number
        the report prints is always the number of distinct rows we actually
        hold.
        """
        return len(self.seen_keys)

    def is_done(self, modalidade, pagina):
        return f"{modalidade}:{pagina}" in self.done_pages

    def mark_done(self, modalidade, pagina):
        self.done_pages.add(f"{modalidade}:{pagina}")


class HarvestReport(object):
    """Expected vs got, plus every failure. Requirement 6.

    The point of this object: a harvest that returns fewer tenders than PNCP
    itself reported in totalRegistros is a SUSPECTED OUTAGE. Without this, a
    half-dead API produces a short harvest that looks exactly like a quiet
    market, and the business acts on a number that is silently wrong.
    """

    def __init__(self, day, modalidades):
        self.day = day
        self.modalidades = list(modalidades)
        self.expected_rows = {}
        self.expected_pages = {}
        self.pages_fetched = 0
        self.pages_skipped_cached = 0
        self.rows_total = 0         # cumulative across runs, from the cursor
        self.rows_new = 0           # emitted by THIS run
        self.rows_duplicate = 0     # suppressed by the cursor's seen_keys
        self.failures = []
        self.served_by = collections.Counter()
        self.network_calls = 0
        self.cache_hits = 0

    @property
    def total_expected(self):
        return sum(self.expected_rows.values())

    @property
    def missing(self):
        """Rows PNCP said exist that we do not hold. Never negative."""
        return max(0, self.total_expected - self.rows_total)

    @property
    def complete(self):
        return not self.failures and self.missing == 0 and self.total_expected > 0

    @property
    def suspected_outage(self):
        """True when the harvest is short or anything failed.

        Deliberately pessimistic. A false alarm costs a human five minutes; a
        missed outage costs a day of tenders nobody knows are absent.
        """
        return bool(self.failures) or self.missing > 0

    def failures_by_status(self):
        c = collections.Counter()
        for f in self.failures:
            c[f.status or f.error] += 1
        return dict(c)

    def summary(self):
        verdict = "COMPLETE" if self.complete else "SUSPECTED OUTAGE"
        return (
            f"{verdict} day={self.day} modalidades={self.modalidades} "
            f"rows={self.rows_total}/{self.total_expected} "
            f"(new={self.rows_new} dup_suppressed={self.rows_duplicate}) "
            f"pages_fetched={self.pages_fetched} "
            f"network_calls={self.network_calls} cache_hits={self.cache_hits} "
            f"served_by={dict(self.served_by)} "
            f"failures={len(self.failures)}:{self.failures_by_status()}"
        )

    def as_dict(self):
        return {
            "day": self.day,
            "modalidades": self.modalidades,
            "expected_rows": self.expected_rows,
            "expected_pages": self.expected_pages,
            "rows_total": self.rows_total,
            "rows_new": self.rows_new,
            "rows_duplicate": self.rows_duplicate,
            "missing": self.missing,
            "pages_fetched": self.pages_fetched,
            "network_calls": self.network_calls,
            "cache_hits": self.cache_hits,
            "complete": self.complete,
            "suspected_outage": self.suspected_outage,
            "served_by": dict(self.served_by),
            "failures": [f.as_dict() for f in self.failures],
        }


class RateLimiter(object):
    """A floor delay between requests, shared across worker threads.

    Measured: a burst of about 30 requests earns a 429 for ~30 seconds from a
    limiter that both families share. Politeness here is not etiquette, it is
    throughput -- a blocked client harvests nothing.
    """

    def __init__(self, min_interval=DEFAULT_MIN_INTERVAL):
        self.min_interval = min_interval
        self.lock = threading.Lock()
        self.next_at = 0.0

    def acquire(self):
        if self.min_interval <= 0:
            return
        with self.lock:
            now = time.time()
            wait = self.next_at - now
            if wait < 0:
                wait = 0.0
            self.next_at = max(now, self.next_at) + self.min_interval
        if wait > 0:
            time.sleep(wait)


class PNCPClient(object):
    """One client that knows both API families.

    Fallback is honest about where it is possible. Probed 2026-09-19:

      "which tenders were published on day D for modalidade M"
          Family A /contratacoes/publicacao  -> primary
          Family A /contratacoes/atualizacao -> same shape, same paging
             fields, a different server-side index. Verified to answer the
             same question, so it is a genuine fallback when the primary
             route 500s.
          Family B has no date-listing equivalent, so there is no B route
             here. Saying otherwise would be a lie that shows up as a silent
             short harvest.

      "the items / winner / files of one compra"
          Family B ONLY. Family A has no item endpoint -- /orgaos/{cnpj}/
          compras/{ano}/{seq}/itens under api/consulta/v1 returns 404, so
          there is nothing to fall back TO. When B is down, these calls fail
          loudly and land in the report, which is the correct behaviour: the
          alternative is pretending a tender has no items.
    """

    def __init__(self, cache_dir=None, state_dir=None, transport=None,
                 max_attempts=DEFAULT_MAX_ATTEMPTS,
                 backoff_base=DEFAULT_BACKOFF_BASE,
                 backoff_cap=DEFAULT_BACKOFF_CAP,
                 concurrency=DEFAULT_CONCURRENCY,
                 min_interval=DEFAULT_MIN_INTERVAL,
                 timeout=DEFAULT_TIMEOUT,
                 cache_ttl=None,
                 sleeper=None):
        self.cache = DiskCache(cache_dir, ttl_seconds=cache_ttl)
        self.state_dir = state_dir or os.path.join(self.cache.directory, "state")
        os.makedirs(self.state_dir, exist_ok=True)
        self.transport = transport if transport is not None else RequestsTransport(timeout)
        self.max_attempts = max_attempts
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self.concurrency = max(1, concurrency)
        self.timeout = timeout
        self.limiter = RateLimiter(min_interval)
        # Injectable so tests can assert on backoff without actually waiting.
        self.sleeper = sleeper if sleeper is not None else time.sleep

        self.events_path = os.path.join(self.state_dir, "events.jsonl")
        self.events = []            # in-memory mirror, handy in tests
        self.failures = []          # every failure this client has seen
        self.network_calls = 0
        self.cache_hits = 0
        self._counter_lock = threading.Lock()

    # -- structured logging -------------------------------------------------

    def log(self, event, **fields):
        """One JSON object per line.

        Requirement 5: which family served each row, and EVERY failure with
        its status code. Machine-readable because the interesting question
        ("did family B serve anything at all today?") is a grep, not a read.
        """
        record = {"ts": round(time.time(), 3), "event": event}
        record.update(fields)
        self.events.append(record)
        try:
            with open(self.events_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            pass    # logging must never be the reason a harvest dies
        return record

    # -- HTTP ---------------------------------------------------------------

    def backoff_delay(self, attempt):
        """Exponential backoff with jitter.

        Half the delay is fixed and half is random. The fixed half keeps us
        off a struggling server; the random half stops concurrent workers from
        retrying in lockstep and recreating the burst that caused the 429.
        """
        base = min(self.backoff_cap, self.backoff_base * (2 ** attempt))
        return base / 2.0 + random.random() * (base / 2.0)

    def fetch_json(self, url, family):
        """Cache-first GET returning parsed JSON. Raises Unavailable.

        The cache is consulted BEFORE the rate limiter and before any socket
        is opened, which is what makes a second run cost zero network calls.
        """
        entry = self.cache.get(url)
        if entry is not None:
            with self._counter_lock:
                self.cache_hits += 1
            self.log("cache_hit", url=url, family=family)
            return entry["body"]

        failures = []
        for attempt in range(self.max_attempts):
            self.limiter.acquire()
            status = None
            error = None
            try:
                with self._counter_lock:
                    self.network_calls += 1
                resp = self.transport.get(url, timeout=self.timeout)
                status = resp.status
                if status == 200:
                    try:
                        payload = resp.json()
                    except ValueError:
                        # 200 with an unparseable body: treat as a failure, do
                        # not cache. Caching garbage is worse than refetching.
                        error = "InvalidJSON"
                    else:
                        self.cache.put(url, family, status, payload)
                        self.log("fetch_ok", url=url, family=family,
                                 status=status, attempt=attempt)
                        return payload
            except Exception as exc:   # noqa: BLE001
                # Connection reset / timeout / proxy hiccup. This is the
                # "HTTP 000" case. The fix is backoff, never verify=False.
                error = type(exc).__name__

            failure = Failure(url, family, status, error, attempt)
            failures.append(failure)
            with self._counter_lock:
                self.failures.append(failure)
            self.log("fetch_fail", url=url, family=family, status=status,
                     error=error, attempt=attempt)

            retryable = (status in RETRY_STATUS) or (status is None)
            if not retryable:
                # 400/404: retrying cannot help and spends the shared budget.
                break
            if attempt + 1 < self.max_attempts:
                self.sleeper(self.backoff_delay(attempt))

        raise Unavailable(url, failures)

    def fetch_first(self, question, routes):
        """Try each (family, url) in turn. First success wins.

        This is the fallback in requirement 1. Routes are ordered by measured
        reliability, not by preference.
        """
        failures = []
        for family, url in routes:
            try:
                payload = self.fetch_json(url, family)
            except Unavailable as exc:
                failures.extend(exc.failures)
                self.log("route_failed", question=question, family=family, url=url)
                continue
            self.log("route_served", question=question, family=family, url=url)
            return payload, family, failures
        raise Unavailable(question, failures)

    # -- Family A: the listing ---------------------------------------------

    @staticmethod
    def _listing_url(path, day, modalidade, pagina, page_size):
        query = urllib.parse.urlencode({
            "dataInicial": day,
            "dataFinal": day,
            "codigoModalidadeContratacao": modalidade,
            "pagina": pagina,
            "tamanhoPagina": page_size,
        })
        return f"{BASE_A}/{path}?{query}"

    def listing_routes(self, day, modalidade, pagina, page_size):
        """Routes that answer 'what was published on this day'.

        Both are Family A. Family B has no equivalent -- see the class
        docstring. When B returns, a third route belongs here.
        """
        return [
            (FAMILY_A, self._listing_url("contratacoes/publicacao", day,
                                         modalidade, pagina, page_size)),
            (FAMILY_A, self._listing_url("contratacoes/atualizacao", day,
                                         modalidade, pagina, page_size)),
        ]

    def fetch_page(self, day, modalidade, pagina, page_size):
        """One page of the listing. Returns (payload, family)."""
        question = f"listing day={day} mod={modalidade} page={pagina}"
        payload, family, _ = self.fetch_first(
            question, self.listing_routes(day, modalidade, pagina, page_size))
        return payload, family

    # -- Family B: the descent into one compra ------------------------------

    def itens(self, cnpj, ano, sequencial, pagina=1, page_size=MAX_PAGE_SIZE):
        """Item rows for one compra. Family B only -- A has no item endpoint.

        Measured 503 today. The call raises rather than returning [], because
        an empty item list and an unreachable API mean opposite things and
        the five filters downstream must never confuse them.
        """
        url = (f"{BASE_B}/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens"
               f"?pagina={pagina}&tamanhoPagina={page_size}")
        payload, _, _ = self.fetch_first(f"itens {cnpj}/{ano}/{sequencial}",
                                         [(FAMILY_B, url)])
        return payload

    def resultado_item(self, cnpj, ano, sequencial, numero_item):
        """The homologated winner for one item. Family B only.

        Returns the winner ONLY -- never the losing bids. Anything downstream
        that wants a price distribution cannot get it here.
        """
        url = (f"{BASE_B}/orgaos/{cnpj}/compras/{ano}/{sequencial}"
               f"/itens/{numero_item}/resultados")
        payload, _, _ = self.fetch_first(
            f"resultados {cnpj}/{ano}/{sequencial}/{numero_item}",
            [(FAMILY_B, url)])
        return payload

    def arquivos(self, cnpj, ano, sequencial, pagina=1, page_size=MAX_PAGE_SIZE):
        """Edital PDF and annexes metadata. Family B only."""
        url = (f"{BASE_B}/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos"
               f"?pagina={pagina}&tamanhoPagina={page_size}")
        payload, _, _ = self.fetch_first(f"arquivos {cnpj}/{ano}/{sequencial}",
                                         [(FAMILY_B, url)])
        return payload

    # -- the daily harvest --------------------------------------------------

    def cursor_for(self, day, modalidades, page_size):
        name = f"day-{day}-mod{'-'.join(str(m) for m in modalidades)}-p{page_size}.json"
        return Cursor(os.path.join(self.state_dir, name))

    def harvest_day(self, day, modalidades=MODALIDADES, page_size=MAX_PAGE_SIZE,
                    max_pages=None, sink=None, cursor=None, reconcile_with=None):
        """Harvest one day nationally. Resumable, cached, and self-auditing.

        day is YYYYMMDD. sink is called with each new row and must persist it
        before returning -- a page is only marked done AFTER its rows have
        been through the sink, so a kill between the two costs a refetch (free
        from cache) rather than a lost row.

        max_pages caps pages per modalidade. It exists for smoke tests against
        the live API; a real descent leaves it None.

        reconcile_with is the path of the JSONL the sink writes to. Pass it
        whenever the harvest can be killed, which is always.

        WHY: the cursor is flushed once per PAGE, but the sink writes once per
        ROW. Kill the process halfway through a page and those rows are on
        disk while the cursor has no memory of them -- resume would write them
        a second time. The file the rows actually landed in is the only
        trustworthy record of what we hold, so we read the keys back out of it
        and seed the cursor. The cursor stays an optimisation for skipping
        whole pages; it is not the source of truth.
        """
        if not (MIN_PAGE_SIZE <= page_size <= MAX_PAGE_SIZE):
            # Measured server behaviour: outside this window is a hard 400.
            raise ValueError(
                f"tamanhoPagina must be {MIN_PAGE_SIZE}..{MAX_PAGE_SIZE}, got {page_size}")

        cursor = cursor or self.cursor_for(day, modalidades, page_size)
        if reconcile_with:
            recovered = keys_in_jsonl(reconcile_with)
            extra = recovered - cursor.seen_keys
            if extra:
                self.log("cursor_reconciled", path=reconcile_with,
                         recovered_rows=len(extra))
            cursor.seen_keys |= recovered
        report = HarvestReport(day, modalidades)
        start_calls, start_hits = self.network_calls, self.cache_hits

        for modalidade in modalidades:
            self._harvest_modalidade(day, modalidade, page_size, max_pages,
                                     sink, cursor, report)

        cursor.flush()

        report.expected_rows = dict(cursor.expected_rows)
        report.expected_pages = dict(cursor.expected_pages)
        report.rows_total = cursor.rows_committed
        report.served_by = collections.Counter(cursor.served_by)
        report.failures = list(cursor.failures)
        report.network_calls = self.network_calls - start_calls
        report.cache_hits = self.cache_hits - start_hits

        # Requirement 6: surfaced, not swallowed. The caller still gets the
        # report -- we refuse to raise, because partial data is worth keeping.
        # But the outage is on the record before anyone looks at the rows.
        self.log("harvest_done", **report.as_dict())
        if report.suspected_outage:
            self.log("SUSPECTED_OUTAGE", day=day,
                     missing=report.missing,
                     expected=report.total_expected,
                     got=report.rows_total,
                     failures=report.failures_by_status())
        return report

    def _harvest_modalidade(self, day, modalidade, page_size, max_pages,
                            sink, cursor, report):
        # Page 1 tells us how many pages exist. On a resumed run it is a cache
        # hit, so asking again is free.
        try:
            payload, family = self.fetch_page(day, modalidade, 1, page_size)
        except Unavailable as exc:
            # We do not even know what we are missing. That is the worst case
            # and it must be loud.
            cursor.failures.extend(exc.failures)
            cursor.flush()
            self.log("modalidade_unreachable", day=day, modalidade=modalidade,
                     statuses=[f.status for f in exc.failures])
            return

        total_rows = payload.get("totalRegistros", 0)
        total_pages = payload.get("totalPaginas", 0)
        cursor.expected_rows[modalidade] = total_rows
        cursor.expected_pages[modalidade] = total_pages

        last_page = total_pages if max_pages is None else min(total_pages, max_pages)
        if max_pages is not None:
            # Honest accounting: if the caller capped the descent, the
            # expectation must be capped too, or every smoke test would
            # report a fake outage.
            cursor.expected_rows[modalidade] = min(total_rows, last_page * page_size)

        self._commit_page(modalidade, 1, payload, family, sink, cursor, report)

        pages = [p for p in range(2, last_page + 1)
                 if not cursor.is_done(modalidade, p)]
        # Fetch in small ordered batches: concurrency for speed, ordered
        # commits so the cursor stays meaningful if we are killed mid-batch.
        for i in range(0, len(pages), self.concurrency):
            batch = pages[i:i + self.concurrency]
            with ThreadPoolExecutor(max_workers=self.concurrency) as pool:
                futures = [pool.submit(self._try_page, day, modalidade, p, page_size)
                           for p in batch]
                results = [f.result() for f in futures]
            for pagina, payload, family, failures in results:
                if failures:
                    cursor.failures.extend(failures)
                if payload is None:
                    continue
                self._commit_page(modalidade, pagina, payload, family,
                                  sink, cursor, report)

    def _try_page(self, day, modalidade, pagina, page_size):
        """Fetch one page without letting a failure kill the whole batch."""
        try:
            payload, family = self.fetch_page(day, modalidade, pagina, page_size)
            return pagina, payload, family, []
        except Unavailable as exc:
            self.log("page_unreachable", day=day, modalidade=modalidade,
                     pagina=pagina, statuses=[f.status for f in exc.failures])
            return pagina, None, None, exc.failures

    def _commit_page(self, modalidade, pagina, payload, family, sink, cursor, report):
        """Deliver a page's rows, then mark it done. Order matters.

        Rows go to the sink first and the cursor is flushed after, so a crash
        between the two re-delivers a page we already have (deduped by
        seen_keys) instead of losing it.
        """
        if cursor.is_done(modalidade, pagina):
            return
        rows = payload.get("data") or []
        new_rows = 0
        for row in rows:
            key = row.get("numeroControlePNCP")
            if not key:
                # No stable identity: fall back to a content hash so the row
                # is still deduplicated across runs rather than dropped.
                key = hashlib.sha1(
                    json.dumps(row, sort_keys=True, ensure_ascii=False).encode()
                ).hexdigest()
            if key in cursor.seen_keys:
                report.rows_duplicate += 1
                continue
            cursor.seen_keys.add(key)
            cursor.served_by[family] += 1
            # Requirement 5: which family served THIS row.
            self.log("row", key=key, family=family, modalidade=modalidade,
                     pagina=pagina)
            if sink is not None:
                sink(row)
            new_rows += 1
        report.rows_new += new_rows
        report.pages_fetched += 1
        cursor.mark_done(modalidade, pagina)
        cursor.flush()


def keys_in_jsonl(path, key_field="numeroControlePNCP"):
    """Row keys already present in a JSONL sink file.

    Used to rebuild dedupe state after a kill. Tolerates a truncated last
    line: a process killed mid-write leaves one, and refusing to read the
    whole file because of it would be worse than skipping that row (which
    then simply gets refetched from cache and rewritten).
    """
    keys = set()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                key = row.get(key_field)
                if not key:
                    key = hashlib.sha1(
                        json.dumps(row, sort_keys=True, ensure_ascii=False).encode()
                    ).hexdigest()
                keys.add(key)
    except OSError:
        pass
    return keys


def jsonl_sink(path):
    """A sink that appends rows to JSONL and fsyncs each one.

    fsync per row is slow and deliberate: the resume guarantee is only as good
    as the weakest of (rows on disk, cursor on disk). Buffered rows plus a
    flushed cursor would resume past data that never landed.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    handle = open(path, "a", encoding="utf-8")

    def write(row):
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())

    write.close = handle.close
    return write
