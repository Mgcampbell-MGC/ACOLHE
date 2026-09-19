"""
Buyer payment-risk screen, backed by SICONFI (Tesouro Nacional).

The question this answers
------------------------
We sell to municipalities on ~30-45 day terms with thin working capital.
Before bidding we want to know one thing: when this municipality has already
received goods, signed off on them and booked the invoice as owed -- does it
actually hand over the money?

Brazil publishes exactly that, free and keyless, in RREO Anexo 07
("Restos a Pagar"). Every ente declares, for invoices carried over from prior
years, how much was:

    inscritos   booked as owed        (a + b)
    pagos       actually paid          (c)
    cancelados  written off            (d)
    saldo       still outstanding      (e) = (a + b) - (c + d)

Two ratios fall out, and they mean very different things to us:

    saldo / inscritos       DELAY      -- they still intend to pay, but late.
                                          Costs us working capital; a long
                                          enough delay kills a cycle.
    cancelados / inscritos  WRITE-OFF  -- they tore up the invoice.
                                          Costs us the sale outright.

The screen keeps those separate on purpose. A buyer that is merely slow is a
financing problem; a buyer that cancels is a bad debt. Do not blend them.

Three outcomes, never two
-------------------------
PASS, REJECT, and UNSCREENABLE. A buyer we could not measure is NOT a buyer
that measured clean. Every failure path in this module -- ente unknown, no
report filed for that period, zero inscritos, API down -- lands on
UNSCREENABLE with passed=False. Defaulting an unscreenable buyer to "pass" is
precisely how this business loses money.

Source: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo
See data/siconfi_probe.md for the endpoint verification behind this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

SICONFI_BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"

# SICONFI sits behind an Oracle ORDS gateway that sometimes drops connections
# from clients with a scripted User-Agent. Always send a browser one.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

DEFAULT_CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache")


@dataclass(frozen=True)
class Thresholds:
    """The rule. Configurable -- the logic below never hardcodes a number."""

    # Reject if more than this share of what was owed is still unpaid.
    max_saldo_ratio: float = 0.30
    # Reject if more than this share of what was owed was written off.
    max_cancelados_ratio: float = 0.02
    # Below this, inscritos is too small a base to read anything into.
    # (A municipality with R$ 900 of restos a pagar tells us nothing.)
    min_inscritos_brl: float = 1000.0


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 5
    base_delay: float = 1.0
    max_delay: float = 30.0
    timeout: float = 90.0


# Outcomes. Three, not two.
PASS = "PASS"
REJECT = "REJECT"
UNSCREENABLE = "UNSCREENABLE"

# Risk kinds, kept separate because their consequences differ.
RISK_DELAY = "delay"
RISK_WRITE_OFF = "write_off"


# --------------------------------------------------------------------------
# The RREO Anexo 07 account codes
# --------------------------------------------------------------------------
#
# We read the "Restos a Pagar Processados e Nao Processados Liquidados" block.
# "Liquidados" is the load-bearing word: the goods were delivered, a public
# servant attested receipt, and the debt is legally due. That is our invoice.
#
# We key on cod_conta, never on the human column label -- SICONFI ships at
# least two spellings of the same saldo label ("Saldo e = (a+ b) - (c + d)"
# and "Saldo e = (a + b) - (c + d)"). cod_conta is stable; labels are not.

_PREFIX = "RestosAPagarProcessadosENaoProcessadosLiquidados"

CONTA_INSCRITOS_ANTERIORES = _PREFIX + "InscritosEmExerciciosAnteriores"  # (a)
CONTA_INSCRITOS_ANTERIOR = _PREFIX + "InscritosEmExercicioAnterior"       # (b)
CONTA_PAGOS = _PREFIX + "Pagos"                                           # (c)
CONTA_CANCELADOS = _PREFIX + "Cancelados"                                 # (d)
CONTA_SALDO = _PREFIX + "APagar"                                          # (e)

# The consolidated bottom line: TOTAL (III) = (I + II), i.e. ordinary plus
# intra-orcamentario restos a pagar.
CONTA_TOTAL_PREFIX = "TOTAL (III)"


class SiconfiUnavailable(Exception):
    """The API could not be reached, or answered with something unusable."""


# --------------------------------------------------------------------------
# 1. The pure screen -- no network, no clock, no disk. This is the rule.
# --------------------------------------------------------------------------


@dataclass
class RestosAPagar:
    """The four figures RREO Anexo 07 gives us, in reais."""

    inscritos: float          # (a + b) booked as owed
    pagos: float              # (c) actually handed over
    cancelados: float         # (d) written off
    saldo: float              # (e) still outstanding
    pagos_source: str = "published"   # "published" or "derived"
    source_url: str = ""
    ente: str = ""
    exercicio: int = 0
    periodo: int = 0


def screen_figures(figures: RestosAPagar, thresholds: Thresholds = Thresholds()):
    """
    Decide on a buyer from its restos a pagar figures.

    Returns (passed, reason, evidence).

    `passed` is True only for a buyer we measured and that cleared both
    thresholds. Anything we could not measure returns False with an
    UNSCREENABLE outcome -- check evidence["outcome"] if you need to tell a
    clean buyer from an unknown one, because they are not the same buyer.

    `reason` is written for the founder to read, not for a log parser.
    `evidence` carries every raw number so the call can be audited later.
    """
    evidence = {
        "outcome": None,
        "risks": [],
        "ente": figures.ente,
        "exercicio": figures.exercicio,
        "periodo": figures.periodo,
        "inscritos_brl": figures.inscritos,
        "pagos_brl": figures.pagos,
        "cancelados_brl": figures.cancelados,
        "saldo_brl": figures.saldo,
        "pagos_source": figures.pagos_source,
        "saldo_ratio": None,
        "cancelados_ratio": None,
        "paid_ratio": None,
        "thresholds": asdict(thresholds),
        "source_url": figures.source_url,
    }

    # -- Cases where the arithmetic cannot be done honestly. ----------------
    # None of these may become a PASS.

    if figures.inscritos is None or figures.saldo is None:
        evidence["outcome"] = UNSCREENABLE
        return (False, _unscreenable_reason(figures, "the report is missing the restos a pagar figures"), evidence)

    if figures.inscritos < 0 or figures.saldo < 0 or figures.cancelados < 0:
        evidence["outcome"] = UNSCREENABLE
        return (False, _unscreenable_reason(figures, "the published figures are negative, which should not happen"), evidence)

    if figures.inscritos == 0:
        # Division by zero. Also genuinely ambiguous: it could mean a
        # municipality that pays everything inside the budget year (excellent)
        # or one that simply did not report (unknown). We cannot tell which,
        # so we do not guess in our own favour.
        evidence["outcome"] = UNSCREENABLE
        return (
            False,
            _unscreenable_reason(
                figures,
                "it reported zero restos a pagar inscritos, so there is no payment history to measure. "
                "That may mean it settles everything within the budget year, or that it did not report. "
                "We cannot tell which from this data",
            ),
            evidence,
        )

    if figures.inscritos < thresholds.min_inscritos_brl:
        evidence["outcome"] = UNSCREENABLE
        return (
            False,
            _unscreenable_reason(
                figures,
                "it only booked R$ {:,.2f} of restos a pagar, too small a base to read a payment habit from "
                "(floor is R$ {:,.2f})".format(figures.inscritos, thresholds.min_inscritos_brl),
            ),
            evidence,
        )

    # -- The measurement. --------------------------------------------------

    saldo_ratio = figures.saldo / figures.inscritos
    cancelados_ratio = figures.cancelados / figures.inscritos
    paid_ratio = figures.pagos / figures.inscritos

    evidence["saldo_ratio"] = saldo_ratio
    evidence["cancelados_ratio"] = cancelados_ratio
    evidence["paid_ratio"] = paid_ratio

    delayed = saldo_ratio > thresholds.max_saldo_ratio
    wrote_off = cancelados_ratio > thresholds.max_cancelados_ratio

    if delayed:
        evidence["risks"].append(RISK_DELAY)
    if wrote_off:
        evidence["risks"].append(RISK_WRITE_OFF)

    head = "{} ({}, RREO Anexo 07, exercicio {} periodo {}) paid {:.1%} of the R$ {:,.2f} it already owed suppliers.".format(
        figures.ente or "This municipality",
        _fmt_pagos_source(figures.pagos_source),
        figures.exercicio,
        figures.periodo,
        paid_ratio,
        figures.inscritos,
    )

    if not delayed and not wrote_off:
        evidence["outcome"] = PASS
        reason = (
            head
            + " Still outstanding: {:.1%} (R$ {:,.2f}), under the {:.0%} limit. "
            "Written off: {:.2%} (R$ {:,.2f}), under the {:.0%} limit. "
            "This buyer pays.".format(
                saldo_ratio, figures.saldo, thresholds.max_saldo_ratio,
                cancelados_ratio, figures.cancelados, thresholds.max_cancelados_ratio,
            )
        )
        return (True, reason, evidence)

    evidence["outcome"] = REJECT
    parts = [head]

    if delayed:
        parts.append(
            "DELAY RISK: {:.1%} (R$ {:,.2f}) of what it owed is still unpaid, above our {:.0%} limit. "
            "Money we are owed would sit there. That is a working-capital hit -- it ties up the cash "
            "we need for the next cycle.".format(
                saldo_ratio, figures.saldo, thresholds.max_saldo_ratio
            )
        )
    if wrote_off:
        parts.append(
            "WRITE-OFF RISK: it cancelled {:.2%} (R$ {:,.2f}) of what it owed, above our {:.0%} limit. "
            "Cancelled means the invoice was torn up, not paid late. That is a lost sale, not a slow one.".format(
                cancelados_ratio, figures.cancelados, thresholds.max_cancelados_ratio
            )
        )

    if delayed and not wrote_off:
        parts.append(
            "Note it is not writing invoices off -- the problem here is speed, not honesty. "
            "If you want this buyer anyway, price the delay in or demand better terms."
        )
    elif wrote_off and not delayed:
        parts.append(
            "Note it settles the rest promptly -- the problem here is that some invoices simply vanish."
        )

    parts.append("Do not bid.")
    return (False, " ".join(parts), evidence)


def _fmt_pagos_source(source):
    if source == "derived":
        return "pagos derived from the published saldo identity"
    return "pagos as published"


def _unscreenable_reason(figures, detail):
    who = figures.ente or "This municipality"
    return (
        "{} CANNOT BE SCREENED: {}. "
        "Treat this as unknown risk, not as a clean buyer -- we have no evidence either way. "
        "Check by hand before committing stock.".format(who, detail)
    )


# --------------------------------------------------------------------------
# 2. Transport: cache on disk, exponential backoff with jitter, browser UA
# --------------------------------------------------------------------------


def _http_get(url, timeout):
    """
    The only place this module touches the network.

    Returns (status_code, body_bytes). Raises SiconfiUnavailable on timeout or
    connection failure -- the caller decides whether to retry.

    TLS verification is never disabled. A dead connection here is a timeout or
    a proxy hiccup; the answer to that is backoff, not trusting a stranger.
    """
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return (response.status, response.read())
    except urllib.error.HTTPError as exc:
        return (exc.code, exc.read())
    except Exception as exc:
        # Socket timeout, DNS failure, proxy reset -- all retryable.
        raise SiconfiUnavailable("{}: {}".format(type(exc).__name__, exc)) from exc


def _cache_dir():
    return os.environ.get("ACOLHE_CACHE") or DEFAULT_CACHE_DIR


def _cache_path(url):
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
    return os.path.join(_cache_dir(), "siconfi", digest + ".json")


class SiconfiClient:
    """
    Fetches SICONFI JSON, keyed by URL, cached to disk forever.

    A re-run of the same screen costs zero calls. That matters: the founder
    re-runs the daily digest, and SICONFI is slow and occasionally down.
    """

    def __init__(self, transport=_http_get, retry=RetryPolicy(), cache_dir=None, sleep=time.sleep):
        self.transport = transport
        self.retry = retry
        self._cache_dir = cache_dir
        self.sleep = sleep
        self.calls_made = 0
        self.cache_hits = 0

    def _dir(self):
        return self._cache_dir or _cache_dir()

    def _path(self, url):
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
        return os.path.join(self._dir(), "siconfi", digest + ".json")

    def get_json(self, url):
        """Return parsed JSON for `url`, from disk if we have ever fetched it."""
        path = self._path(url)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    self.cache_hits += 1
                    return json.load(handle)["body"]
            except (ValueError, KeyError, OSError):
                # Corrupt cache entry -- drop it and refetch rather than die.
                try:
                    os.remove(path)
                except OSError:
                    pass

        body = self._fetch_with_backoff(url)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"url": url, "fetched_at": time.time(), "body": body}, handle)
        os.replace(tmp, path)
        return body

    def _fetch_with_backoff(self, url):
        last_error = "unknown"
        for attempt in range(self.retry.attempts):
            if attempt:
                # Exponential backoff with full jitter. Jitter matters because
                # a batch screen would otherwise retry in lockstep and hammer
                # a struggling API at exactly the same instants.
                ceiling = min(self.retry.max_delay, self.retry.base_delay * (2 ** attempt))
                self.sleep(random.uniform(0, ceiling))

            try:
                self.calls_made += 1
                status, raw = self.transport(url, self.retry.timeout)
            except SiconfiUnavailable as exc:
                last_error = str(exc)
                continue

            if status == 200:
                try:
                    return json.loads(raw.decode("utf-8"))
                except (ValueError, UnicodeDecodeError) as exc:
                    # A 200 carrying an HTML error page or a truncated body.
                    last_error = "200 with unparseable body: {}".format(exc)
                    continue

            if status == 429 or status >= 500:
                last_error = "HTTP {}".format(status)
                continue

            # 4xx other than 429: retrying will not help.
            raise SiconfiUnavailable("HTTP {} for {}".format(status, url))

        raise SiconfiUnavailable(
            "gave up on {} after {} attempts (last: {})".format(url, self.retry.attempts, last_error)
        )


# --------------------------------------------------------------------------
# 3. CNPJ -> IBGE resolution, via the entes table
# --------------------------------------------------------------------------


def entes_url():
    return SICONFI_BASE + "/entes"


def _digits(value):
    return "".join(ch for ch in str(value) if ch.isdigit())


def _strip_accents(text):
    return "".join(
        ch for ch in unicodedata.normalize("NFD", str(text).lower())
        if unicodedata.category(ch) != "Mn"
    ).strip()


class EnteDirectory:
    """
    The CNPJ <-> IBGE join.

    PNCP identifies a buyer by CNPJ; SICONFI wants an IBGE code. The entes
    table (~866 KB, 5598 rows, changes maybe once a year) carries both, so we
    fetch it once and cache it hard.
    """

    def __init__(self, client):
        self.client = client
        self._by_cnpj = None
        self._by_ibge = None
        self._by_name = None

    def _load(self):
        if self._by_cnpj is not None:
            return
        payload = self.client.get_json(entes_url())
        items = payload.get("items", [])
        if not items:
            raise SiconfiUnavailable("the entes table came back empty")

        self._by_cnpj = {}
        self._by_ibge = {}
        self._by_name = {}
        for item in items:
            cnpj = _digits(item.get("cnpj") or "")
            if cnpj:
                self._by_cnpj[cnpj] = item
            ibge = item.get("cod_ibge")
            if ibge is not None:
                self._by_ibge[str(ibge)] = item
            key = (_strip_accents(item.get("ente") or ""), str(item.get("uf") or "").upper())
            self._by_name.setdefault(key, item)

    def by_cnpj(self, cnpj):
        """Return the ente record for a CNPJ, or None if it is not a known ente."""
        self._load()
        return self._by_cnpj.get(_digits(cnpj))

    def by_ibge(self, cod_ibge):
        self._load()
        return self._by_ibge.get(str(cod_ibge))

    def by_name(self, name, uf):
        self._load()
        return self._by_name.get((_strip_accents(name), str(uf).upper()))

    def ibge_for_cnpj(self, cnpj):
        record = self.by_cnpj(cnpj)
        return None if record is None else record.get("cod_ibge")


# --------------------------------------------------------------------------
# 4. Reading RREO Anexo 07
# --------------------------------------------------------------------------


def rreo_anexo07_url(cod_ibge, exercicio, periodo):
    query = urllib.parse.urlencode({
        "an_exercicio": exercicio,
        "nr_periodo": periodo,
        "co_tipo_demonstrativo": "RREO",
        "no_anexo": "RREO-Anexo 07",
        "co_esfera": "M",
        "id_ente": cod_ibge,
    })
    return "{}/rreo?{}".format(SICONFI_BASE, query)


def _sum_conta(items, cod_conta):
    """
    Total the TOTAL (III) rows for one account code.

    Returns None when the account is absent entirely -- which is NOT the same
    as zero, and the caller must decide what to do about it.
    """
    values = [
        item.get("valor") or 0.0
        for item in items
        if item.get("cod_conta") == cod_conta
        and str(item.get("conta", "")).startswith(CONTA_TOTAL_PREFIX)
    ]
    if not values:
        return None
    return float(sum(values))


def parse_anexo07(payload, source_url="", ente="", exercicio=0, periodo=0):
    """
    Pull the four figures out of an RREO Anexo 07 response.

    Returns a RestosAPagar, or None when the ente filed nothing for this
    period.

    The subtle part: SICONFI omits zero-valued rows. A municipality that paid
    nothing at all has NO "Pagos (c)" row -- the column simply is not there.
    Read naively that looks like missing data, and the worst payers in the
    country would silently drop out of the screen. So we never trust the
    absence of Pagos; we derive it from the identity SICONFI itself publishes:

        saldo (e) = (a + b) - (c + d)   =>   c = (a + b) - d - e

    Verified to the cent against every ente in the probe that did publish (c).
    """
    items = payload.get("items", [])
    if not items:
        return None

    inscritos_anteriores = _sum_conta(items, CONTA_INSCRITOS_ANTERIORES) or 0.0
    inscritos_anterior = _sum_conta(items, CONTA_INSCRITOS_ANTERIOR) or 0.0
    cancelados = _sum_conta(items, CONTA_CANCELADOS) or 0.0
    saldo = _sum_conta(items, CONTA_SALDO)
    pagos_published = _sum_conta(items, CONTA_PAGOS)

    inscritos = inscritos_anteriores + inscritos_anterior

    if saldo is None:
        # Without the saldo we have neither the numerator nor a way to derive
        # pagos. The ente filed something, but not this block.
        if inscritos == 0:
            return None
        saldo = inscritos - cancelados - (pagos_published or 0.0)

    derived_pagos = inscritos - cancelados - saldo
    if pagos_published is None:
        pagos = max(0.0, derived_pagos)
        pagos_source = "derived"
    else:
        pagos = pagos_published
        pagos_source = "published"
        if abs(derived_pagos - pagos_published) > 1.0:
            # The published figures do not close. Flag it rather than pick one.
            pagos_source = "published_inconsistent"

    if not any([inscritos, pagos, cancelados, saldo]):
        return None

    return RestosAPagar(
        inscritos=inscritos,
        pagos=pagos,
        cancelados=cancelados,
        saldo=saldo,
        pagos_source=pagos_source,
        source_url=source_url,
        ente=ente,
        exercicio=exercicio,
        periodo=periodo,
    )


# --------------------------------------------------------------------------
# 5. The whole screen, end to end
# --------------------------------------------------------------------------


@dataclass
class ScreenRequest:
    cnpj: str = ""
    cod_ibge: str = ""
    exercicio: int = 2026
    periodo: int = 3
    # RREO is bimonthly and entes file late. If the asked-for period is not
    # there, walk back through earlier periods of the same exercise rather
    # than calling the buyer unscreenable over a filing lag. Whichever period
    # actually answered is recorded in the evidence.
    fallback_periods: tuple = (3, 2, 1)


def screen_buyer(request, client=None, directory=None, thresholds=Thresholds()):
    """
    Screen one municipality, from a CNPJ or an IBGE code, end to end.

    Returns (passed, reason, evidence), same contract as screen_figures.
    Every failure mode below returns passed=False with outcome UNSCREENABLE.
    """
    client = client or SiconfiClient()
    directory = directory or EnteDirectory(client)

    base_evidence = {
        "outcome": UNSCREENABLE,
        "risks": [],
        "cnpj": request.cnpj,
        "cod_ibge": request.cod_ibge,
        "thresholds": asdict(thresholds),
    }

    # -- resolve the ente -------------------------------------------------
    cod_ibge = request.cod_ibge
    ente_name = ""
    try:
        if not cod_ibge:
            if not request.cnpj:
                base_evidence["error"] = "no CNPJ and no IBGE code supplied"
                return (False, _unscreenable_reason(RestosAPagar(0, 0, 0, 0), "we were given neither a CNPJ nor an IBGE code"), base_evidence)
            record = directory.by_cnpj(request.cnpj)
            if record is None:
                base_evidence["error"] = "CNPJ not present in the SICONFI entes table"
                return (
                    False,
                    "CANNOT BE SCREENED: CNPJ {} is not in the SICONFI entes table, so we could not find its "
                    "IBGE code. It may be a state body, an autarquia, a consorcio or a hospital foundation "
                    "rather than a prefeitura -- those buy too, but they do not file RREO under a municipal "
                    "code. Treat as unknown risk, not as a clean buyer.".format(request.cnpj),
                    base_evidence,
                )
            cod_ibge = record.get("cod_ibge")
            ente_name = "{}/{}".format(record.get("ente"), record.get("uf"))
        else:
            record = directory.by_ibge(cod_ibge)
            if record is not None:
                ente_name = "{}/{}".format(record.get("ente"), record.get("uf"))
    except SiconfiUnavailable as exc:
        base_evidence["error"] = str(exc)
        return (
            False,
            "CANNOT BE SCREENED: could not load the SICONFI entes table ({}). The API is unreachable right "
            "now. Treat as unknown risk, not as a clean buyer, and retry before the bid deadline.".format(exc),
            base_evidence,
        )

    base_evidence["cod_ibge"] = cod_ibge
    base_evidence["ente"] = ente_name

    # -- pull the report ---------------------------------------------------
    periods = [request.periodo] + [p for p in request.fallback_periods if p != request.periodo]
    tried = []
    figures = None
    for periodo in periods:
        url = rreo_anexo07_url(cod_ibge, request.exercicio, periodo)
        tried.append(url)
        try:
            payload = client.get_json(url)
        except SiconfiUnavailable as exc:
            base_evidence["error"] = str(exc)
            base_evidence["urls_tried"] = tried
            return (
                False,
                "{} CANNOT BE SCREENED: SICONFI did not answer ({}). Treat as unknown risk, not as a clean "
                "buyer, and retry before the bid deadline.".format(ente_name or cod_ibge, exc),
                base_evidence,
            )

        figures = parse_anexo07(
            payload, source_url=url, ente=ente_name,
            exercicio=request.exercicio, periodo=periodo,
        )
        if figures is not None:
            break

    base_evidence["urls_tried"] = tried

    if figures is None:
        base_evidence["error"] = "no RREO Anexo 07 data for exercicio {} in periods {}".format(
            request.exercicio, periods)
        return (
            False,
            "{} CANNOT BE SCREENED: it has not published RREO Anexo 07 for exercicio {} in any of periods {}. "
            "A municipality that does not file its accounts is not a municipality that pays on time -- but we "
            "have no measurement, so this is unknown risk, not a clean bill of health.".format(
                ente_name or cod_ibge, request.exercicio, ", ".join(str(p) for p in periods)),
            base_evidence,
        )

    passed, reason, evidence = screen_figures(figures, thresholds)
    evidence["cnpj"] = request.cnpj
    evidence["cod_ibge"] = cod_ibge
    evidence["urls_tried"] = tried
    return (passed, reason, evidence)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Screen a municipality's payment risk via SICONFI.")
    parser.add_argument("targets", nargs="+", help="CNPJ or 7-digit IBGE code")
    parser.add_argument("--exercicio", type=int, default=2026)
    parser.add_argument("--periodo", type=int, default=3)
    parser.add_argument("--max-saldo", type=float, default=Thresholds.max_saldo_ratio)
    parser.add_argument("--max-cancelados", type=float, default=Thresholds.max_cancelados_ratio)
    parser.add_argument("--json", action="store_true", help="print evidence as JSON")
    args = parser.parse_args(argv)

    thresholds = Thresholds(max_saldo_ratio=args.max_saldo, max_cancelados_ratio=args.max_cancelados)
    client = SiconfiClient()
    directory = EnteDirectory(client)

    exit_code = 0
    for target in args.targets:
        digits = _digits(target)
        request = ScreenRequest(
            cnpj="" if len(digits) == 7 else target,
            cod_ibge=target if len(digits) == 7 else "",
            exercicio=args.exercicio,
            periodo=args.periodo,
        )
        passed, reason, evidence = screen_buyer(request, client, directory, thresholds)
        print("[{}] {}".format(evidence["outcome"], reason))
        if args.json:
            print(json.dumps(evidence, ensure_ascii=False, indent=2, default=str))
        print()
        if not passed:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
