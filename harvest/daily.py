"""The scanner: find every buyer publishing a newborn-kit tender, nationally.

This is the origination layer. It answers one question each morning -- WHO is
about to buy, and where -- by reading what Lei 14.133 art. 54 obliges every
contracting body in Brazil to publish before it may buy anything.

Three things it must never do, each learned the hard way:

  1. Never report a short harvest as a quiet market. If PNCP served fewer
     tenders than it said it held, that is a suspected outage and the scan
     says so rather than printing a smaller number.
  2. Never count a repeat as coverage. distinct != served.
  3. Never let a keyword drag in an adjacent programme. A Mato Grosso
     school-uniform tender is not a newborn kit, and one regex once added
     R$155,7M of them to a kit harvest.

RECALL CEILING, stated up front: this matches on the tender's OBJECT TEXT.
Roughly a quarter of kit tenders describe themselves generically ("aquisicao
de enxovais", "material de consumo") and are only reachable by descending into
each tender's item list -- which lives exclusively on PNCP's Family B API.
While Family B is down, this scan runs at partial recall BY CONSTRUCTION, and
the report says so instead of implying it found everything.
"""

import collections
import re

from parse.normalise import strip_accents

# What a newborn-kit tender calls itself. Deliberately broad: precision comes
# from the exclusions below, because a false positive costs one read and a
# false negative costs the tender.
KIT_PATTERNS = [
    # ENXOVAIS is the plural and appears in real objects as often as the
    # singular. Matching only ENXOVAL silently halves recall on this word.
    r"KIT\s+(?:NATALIDADE|MATERNIDADE|BEBE|ENXOVA(?:L|IS)|GESTANTE|NASCER|RECEM)",
    r"ENXOVA(?:L|IS)(?:\s+(?:DE\s+)?(?:BEBE|MATERNIDADE|RECEM|NEONATAL))?",
    r"KIT\s+(?:PARA\s+)?(?:GESTANTES?|PUERPERAS?)",
    r"(?:BOLSA|MOCHILA)\s+MATERNIDADE",
    r"\bLAYETTE\b",
    r"KIT\s+PRIMEIRO\s+ENXOVAL",
    r"AQUISI[CÇ][AÃ]O.{0,40}\bBEBES?\b",
    r"\bMA[EÊ]\s+(?:ITAQUA|GAUCHA|PARANAENSE|NOSSA)",
    r"NASCER\s+BEM",
]

# Adjacent programmes that share vocabulary and are NOT our market.
NOT_KIT = [
    r"ESCOLAR", r"UNIFORME", r"MERENDA", r"CESTA\s+B[AÁ]SICA",
    r"MATERIAL\s+DID[AÁ]TICO", r"T[EÊ]NIS\s+ESCOLAR",
    r"MEDICAMENTO", r"HOSPITALAR", r"ODONTOL[OÓ]GIC",
    r"LIMPEZA", r"EXPEDIENTE", r"INFORM[AÁ]TICA",
    r"COMBUST[IÍ]VEL", r"VE[IÍ]CULO", r"OBRA", r"PAVIMENTA",
    r"LOCA[CÇ][AÃ]O", r"SERVI[CÇ]OS?\s+DE", r"M[AÃ]O\s+DE\s+OBRA",
    r"BER[CÇ][AÁ]RIO\s+MOBILI", r"CRECHE\s+MOBILI",
]

_KIT_RE = [re.compile(p, re.I) for p in KIT_PATTERNS]
_NOT_RE = [re.compile(p, re.I) for p in NOT_KIT]


def kit_signal(objeto):
    """(is_candidate, matched_pattern, exclusion) for one tender's object text.

    The exclusion is reported WHENEVER one fired, not only when a kit pattern
    also matched. A row rejected with no stated reason is indistinguishable
    from a row that was never seen, and that is how a scan quietly narrows.
    """
    if not objeto:
        return False, None, None
    flat = strip_accents(objeto).upper()

    excl = next((p.pattern for p in _NOT_RE if p.search(flat)), None)
    hit = next((p.pattern for p in _KIT_RE if p.search(flat)), None)
    return bool(hit and not excl), hit, excl


def buyer_of(row):
    org = row.get("orgaoEntidade") or {}
    unit = row.get("unidadeOrgao") or {}
    return {
        "cnpj": org.get("cnpj"),
        "nome": org.get("razaoSocial"),
        "esfera": org.get("esferaId"),
        "municipio": unit.get("municipioNome"),
        "uf": unit.get("ufSigla"),
        "ibge": unit.get("codigoIbge"),
    }


def in_window(row, day=None, now=None):
    """(ok, reason) -- is this tender actually live and actually from this day?

    MEASURED, 2026-09-19. The publicacao and atualizacao routes are NOT two
    views of the same thing. For 2026-09-15 publicacao held 4.595 records and
    atualizacao held 8.323 -- but the extra ones are not tenders publicacao
    missed. They are OLDER tenders touched in that window.

    Worked example: Nova Roma/GO 14901848000104-1-000008/2026, a genuine kit
    enxoval tender, appeared via atualizacao in a harvest for the 15th. It was
    published on the 4th and its proposal window CLOSED ON THE 10TH. A
    fallback had injected an eleven-day-old dead tender into a live scan.

    So a route fallback does not merely reorder pages -- it silently widens
    the date window. This guard is the backstop: date-stamp every candidate
    against the day we asked for, and against the clock.
    """
    import datetime

    def parse(value):
        if not value:
            return None
        try:
            return datetime.datetime.fromisoformat(str(value)[:19])
        except ValueError:
            return None

    published = parse(row.get("dataPublicacaoPncp")) or parse(row.get("dataInclusao"))
    closes = parse(row.get("dataEncerramentoProposta"))
    now = now or datetime.datetime.now()

    if day and published:
        asked = datetime.datetime.strptime(str(day), "%Y%m%d").date()
        if published.date() != asked:
            return False, (f"published {published.date()}, not {asked} -- a route "
                           f"fallback widened the window")
    if closes and closes < now:
        return False, f"proposal window closed {closes.date()}"
    return True, "live"


def scan(rows, day=None, now=None):
    """Split a day's national harvest into candidates, excluded and the rest.

    Pass `day` (YYYYMMDD) to enforce the window guard above. Without it the
    scan still works, but a fallback-injected stale tender would pass through.
    """
    candidates, excluded, stale = [], [], []
    for row in rows:
        objeto = row.get("objetoCompra") or ""
        is_kit, hit, excl = kit_signal(objeto)
        buyer = buyer_of(row)
        record = {
            "pncp_key": row.get("numeroControlePNCP"),
            "objeto": " ".join(objeto.split())[:180],
            "valor_estimado": row.get("valorTotalEstimado"),
            "valor_homologado": row.get("valorTotalHomologado"),
            "srp": row.get("srp"),
            "modalidade": row.get("modalidadeNome"),
            "encerramento": row.get("dataEncerramentoProposta"),
            "matched": hit,
            "excluded_by": excl,
            **buyer,
        }
        if is_kit:
            ok, why = in_window(row, day=day, now=now)
            if ok:
                candidates.append(record)
            else:
                record["stale_reason"] = why
                stale.append(record)
        else:
            excluded.append(record)
    return candidates, [r for r in excluded if r["matched"]], stale


def summarise(candidates, near_misses, stale=(), report=None):
    """The lines a human reads. Every aggregate prints its underlying rows."""
    out = []
    by_uf = collections.Counter(c["uf"] for c in candidates if c["uf"])
    by_esfera = collections.Counter(c["esfera"] for c in candidates)

    out.append(f"KIT CANDIDATES: {len(candidates)}")
    if by_esfera:
        shown = ", ".join(f"{k or '?'}={v}" for k, v in by_esfera.most_common())
        out.append(f"  by sphere (M=municipal, E=estadual, F=federal): {shown}")
    if by_uf:
        shown = ", ".join(f"{uf}={n}" for uf, n in by_uf.most_common(12))
        out.append(f"  by UF: {shown}")

    out.append(f"  {min(8, len(candidates))} of {len(candidates)} rows behind that count:")
    for c in sorted(candidates, key=lambda r: -(r["valor_estimado"] or 0))[:8]:
        val = c["valor_estimado"]
        money = f"R$ {val:>14,.2f}" if val else "R$        (none)"
        out.append(f"    {money}  {c['municipio'] or '?'}/{c['uf'] or '?':2s}  "
                   f"{c['objeto'][:74]}")

    if stale:
        out.append(f"  !! {len(stale)} kit tender(s) DROPPED as out-of-window -- "
                   f"a route fallback injected them:")
        for c in stale[:4]:
            out.append(f"    [{c['stale_reason']}] {c['municipio']}/{c['uf']} "
                       f"{c['objeto'][:56]}")

    if near_misses:
        out.append(f"  {len(near_misses)} matched a kit word but were EXCLUDED "
                   f"as an adjacent programme:")
        for c in near_misses[:4]:
            out.append(f"    [{c['excluded_by']}] {c['objeto'][:84]}")

    if report is not None:
        # Read the report's real attributes. NEVER getattr-with-a-default here:
        # a renamed field would then report the integrity check as None, which
        # reads like "fine" and is actually "not checked". That happened.
        out.append("")
        out.append(f"HARVEST INTEGRITY: distinct={report.rows_total} "
                   f"served={report.rows_served} expected={report.total_expected} "
                   f"pages={report.pages_fetched} complete={report.complete}")
        if report.rows_duplicate:
            out.append(f"  {report.rows_duplicate} duplicate row(s) suppressed "
                       f"-- served minus distinct, not lost tenders")
        if report.missing:
            out.append(f"  !! {report.missing} tender(s) PNCP said it held were "
                       f"never fetched -- this scan is SHORT, not a quiet market")
        if report.route_mixed:
            out.append("  !! ROUTE_MIXED: a fallback served part of this day, and "
                       "the routes are ordered differently, so coverage is unknown")
        if report.failures:
            out.append(f"  !! {len(report.failures)} route(s) failed outright")
        if report.suspected_outage:
            out.append("  >> SUSPECTED OUTAGE. Do not treat this count as the market.")
    out.append("")
    out.append("RECALL: object-text match only. Tenders whose object text is "
               "generic are reachable only via PNCP Family B /itens, which is "
               "currently unavailable. Treat this as a FLOOR on the market.")
    return "\n".join(out)
