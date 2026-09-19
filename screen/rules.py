"""The 11 admission rules, as pure functions.

Each returns a Result(passed, reason, evidence). The reason is written for the
founder to read, not for a log file: she has to be able to look at a NO-BID and
understand it in one line without opening the edital.

Thresholds live in config/rules.yaml. Never inline one here.

There is no pricing skill that rescues a tender she should not have entered.
The filters ARE the business.
"""

import os
import re
from dataclasses import dataclass, field

import yaml

from parse.normalise import strip_accents

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "rules.yaml"
)


@dataclass
class Result:
    rule_id: str
    passed: bool
    reason: str
    evidence: dict = field(default_factory=dict)
    is_flag: bool = False       # an opportunity/warning, not an admission test

    def __bool__(self):
        return self.passed


def _cfg(config=None):
    if config is not None:
        return config
    with open(_CONFIG_PATH) as fh:
        return yaml.safe_load(fh)


def _any(patterns, text):
    flat = strip_accents(text or "").upper()
    for pat in patterns or []:
        match = re.search(pat, flat, re.I | re.M)
        if match:
            return match.group(0)
    return None


# ---------------------------------------------------------------------------

def rule_1_lote_unico(objeto, items=None, config=None):
    """Per-item lines clear at 97-100% of estimate; lote unico at 36-63%."""
    cfg = _cfg(config)["rule_1_lote_unico"]
    if not cfg.get("enabled", True):
        return Result("1", True, "rule disabled")

    hit = _any(cfg["patterns"], objeto)
    if hit:
        return Result("1", False, f"LOTE UNICO tender (matched {hit!r}). Lote "
                      f"unico clears at 36-63% of estimate against 97-100% for "
                      f"per-item lines.", {"match": hit})

    if items is not None and cfg.get("reject_if_single_item_covers_whole_object"):
        if len(items) == 1:
            return Result("1", False, "a single item covers the whole object, "
                          "which is a lote unico by another name",
                          {"item_count": 1})
    return Result("1", True, "judged per item", {"item_count": len(items or [])})


def rule_2_atestado(edital_text, config=None):
    """Reject a QUANTITATIVE atestado only. A qualitative one is satisfied by
    one prior sale of any size, public or private -- rejecting all of them
    would discard most of the market."""
    cfg = _cfg(config)["rule_2_atestado"]
    if not cfg.get("enabled", True):
        return Result("2", True, "rule disabled")

    flat = strip_accents(edital_text or "").upper()
    windows = _clause_windows(flat, cfg["clause_headings"],
                              span=int(cfg.get("clause_span_chars", 3000)))

    # MEASURED 2026-09-19: searching the WHOLE document for a percentage
    # returned QUANTITATIVE for 7 of 7 real editais, on '10%', '5%', '100%'
    # from multa and garantia clauses nowhere near the atestado. The marker
    # must be found INSIDE the qualificacao tecnica clause, and that window
    # must actually be about an atestado, or it is not our clause.
    #
    # ABSENT means no window is about an atestado -- not merely that no
    # heading matched. Agrolandia/SC has a boilerplate 'capacidade tecnica'
    # phrase and the word 'atestado' zero times in 41 pages: ABSENT.
    relevant = [w for w in windows
                if re.search(r"ATESTAD|COMPROVA[CÇ][AÃ]O\s+DE\s+(?:APTID|CAPACID)", w)]
    if not relevant:
        return Result("2", True, "no qualificacao tecnica clause found",
                      {"clause": "ABSENT"})

    for window in relevant:
        hit = _quantitative_near_atestado(window, cfg["quantitative_markers"])
        if hit:
            return Result("2", False, f"QUANTITATIVE atestado: the clause demands "
                          f"{hit!r}. A first-time bidder cannot satisfy a quantity "
                          f"or percentage threshold.",
                          {"clause": "QUANTITATIVE", "match": hit})
    return Result("2", True, "QUALITATIVE atestado -- satisfied by one prior "
                  "sale of any size, public or private",
                  {"clause": "QUALITATIVE"})


def _clause_windows(flat, headings, span=3000):
    """The text that follows each clause heading, one window per occurrence.

    A heading can appear more than once (an index, a cross-reference, the
    clause itself). Every occurrence gets a window so the real one is never
    missed; the caller decides which windows are genuinely about the topic.
    """
    out = []
    for pat in headings or []:
        for match in re.finditer(pat, flat, re.I | re.M):
            # A heading is a LOCUS, not a boundary. Belterra/PA writes the
            # whole requirement as '... COM ATESTADO DE CAPACIDADE TECNICA.'
            # -- the phrase that matches the heading is the TAIL of the
            # atestado mention, so a window starting after it never sees the
            # word 'atestado'. Look a little before, too.
            out.append(flat[max(0, match.start() - 300):match.end() + span])
    return out


_MARKER_REACH = 400   # chars either side of the word ATESTADO


def _quantitative_near_atestado(window, markers):
    """A quantity or percentage counts only if it sits NEXT TO the atestado.

    'atestado ... comprovando no minimo 50% do quantitativo' is quantitative.
    A '10%' multa two paragraphs later in the same clause is not. Searching
    the whole window is how 7 of 7 real editais read QUANTITATIVE today.
    """
    for m in re.finditer(r"ATESTAD", window):
        local = window[max(0, m.start() - _MARKER_REACH):m.end() + _MARKER_REACH]
        hit = _any(markers, local)
        if hit:
            return hit
    return None


_NEGATION_BEFORE = re.compile(
    r"(?:\bN[AÃ]O\b|\bVEDAD[AO]\b|\bPROIBID[AO]\b|\bNEM\b|\bSEM\b)[^.;]{0,120}$",
    re.I,
)


def _negated(flat, start):
    """True when the 120 chars before `start` negate what follows.

    'nao sendo, em nenhuma hipotese, permitida a antecipacao de pagamentos'
    is a PROHIBITION, and a naive grep read it as an offer.
    """
    return bool(_NEGATION_BEFORE.search(flat[max(0, start - 120):start]))


def rule_3_modelo_do_orgao(edital_text, config=None):
    cfg = _cfg(config)["rule_3_modelo_do_orgao"]
    if not cfg.get("enabled", True):
        return Result("3", True, "rule disabled")
    hit = _any(cfg["patterns"], edital_text)
    if hit:
        return Result("3", False, f"custom spec ({hit!r}) -- unsourceable from "
                      f"any catalogue", {"match": hit})
    return Result("3", True, "no custom-model clause")


def rule_4_kit_size(item_count, config=None):
    cfg = _cfg(config)["rule_4_kit_size"]
    if not cfg.get("enabled", True):
        return Result("4", True, "rule disabled")
    if item_count is None:
        return Result("4", False, "item count unknown -- cannot confirm the kit "
                      "is sourceable", {"item_count": None})
    if item_count > cfg["max_items"]:
        return Result("4", False, f"{item_count}-item kit exceeds the "
                      f"{cfg['max_items']}-item ceiling: too many sourcing "
                      f"points. The one priced 18-item kit came in at -3,1%.",
                      {"item_count": item_count})
    if item_count > cfg["warn_above"]:
        return Result("4", True, f"{item_count} items -- near the sourcing "
                      f"ceiling, check every line has a supplier",
                      {"item_count": item_count}, is_flag=True)
    return Result("4", True, f"{item_count} items, sourceable",
                  {"item_count": item_count})


_UFS_PATH = os.path.join(os.path.dirname(_CONFIG_PATH), "ufs.yaml")
_CAPITAL_PATH = os.path.join(os.path.dirname(_CONFIG_PATH), "capital.yaml")


def _capital_cfg():
    with open(_CAPITAL_PATH) as fh:
        return yaml.safe_load(fh)


def feasibility_from_config(quantity=None):
    """Days needed to deliver to each UF, or None where transit is UNMEASURED.

    needed = buy_and_assemble + transit (+ co-packer lead when the lot is
    above the self-pack ceiling). A None anywhere in that sum stays None:
    an unmeasured leg must never be silently rounded to zero.
    """
    with open(_UFS_PATH) as fh:
        ufs = yaml.safe_load(fh)
    cap = _capital_cfg()
    base = ufs.get("buy_and_assemble_days") or 0
    fulfil = cap.get("fulfilment", {})

    copack_leg = 0
    if quantity is not None and quantity > (fulfil.get("self_pack_max_kits") or 0):
        copack_leg = fulfil.get("copacker_lead_days")    # may be None

    out = {}
    for group in ("target", "secondary", "deprioritised"):
        for uf, spec in (ufs.get(group) or {}).items():
            transit = (spec or {}).get("transit_days")
            if transit is None or copack_leg is None:
                out[uf] = None
            else:
                out[uf] = base + transit + copack_leg
    return out


def rule_5_prazo_entrega(prazo_days, uf=None, uf_feasibility=None, config=None):
    """31,2% of these are <=5 days and one live edital demanded 3."""
    cfg = _cfg(config)["rule_5_prazo_entrega"]
    if not cfg.get("enabled", True):
        return Result("5", True, "rule disabled")
    if prazo_days is None:
        return Result("5", False, "prazo de entrega not found in the edital -- "
                      "cannot confirm it is achievable", {"prazo_days": None})

    table = uf_feasibility if uf_feasibility is not None else feasibility_from_config()
    needed = table.get(uf, cfg["min_days_absolute"]) if uf else cfg["min_days_absolute"]
    if needed is None:
        # Transit days for this UF have never been measured. That is not a
        # pass: nobody has shown the kit can get there in time.
        return Result("5", False, f"transit days to {uf} are UNMEASURED, so "
                      f"{prazo_days} days cannot be confirmed achievable -- "
                      f"VERIFICAR, not a rejection",
                      {"prazo_days": prazo_days, "needed": None, "uf": uf,
                       "outcome": "UNVERIFIABLE"})
    if prazo_days < needed:
        return Result("5", False, f"{prazo_days} days to deliver to {uf}, but "
                      f"{needed} are needed to buy, assemble and ship there",
                      {"prazo_days": prazo_days, "needed": needed, "uf": uf})
    return Result("5", True, f"{prazo_days} days to {uf} is achievable "
                  f"(needs {needed})",
                  {"prazo_days": prazo_days, "needed": needed, "uf": uf})


def rule_6_buyer_payment(siconfi, config=None):
    """SICONFI screen. An UNSCREENABLE buyer is not a passing buyer."""
    cfg = _cfg(config)["rule_6_buyer_payment"]
    if not cfg.get("enabled", True):
        return Result("6", True, "rule disabled")

    if not siconfi or siconfi.get("status") != "ok":
        why = (siconfi or {}).get("status", "no data")
        passed = bool(cfg.get("unscreenable_is_a_pass", False))
        return Result("6", passed, f"buyer could not be screened ({why}). "
                      f"An unscreenable buyer is treated as a REJECT, because "
                      f"defaulting it to pass is how this business loses money.",
                      {"status": why})

    inscritos = float(siconfi.get("inscritos") or 0)
    saldo = float(siconfi.get("saldo") or 0)
    cancelados = float(siconfi.get("cancelados") or 0)

    if inscritos <= 0:
        return Result("6", False, "buyer reports zero restos a pagar inscritos "
                      "-- nothing to measure, so payment behaviour is unknown",
                      {"inscritos": inscritos})

    unpaid = saldo / inscritos
    written_off = cancelados / inscritos
    ev = {"inscritos": inscritos, "saldo": saldo, "cancelados": cancelados,
          "unpaid_ratio": round(unpaid, 4), "cancelado_ratio": round(written_off, 4)}

    if written_off > cfg["max_cancelados_ratio"]:
        return Result("6", False, f"buyer WROTE OFF {written_off:.1%} of what "
                      f"suppliers had already earned (limit "
                      f"{cfg['max_cancelados_ratio']:.0%}). That is default, "
                      f"not delay.", ev)
    if unpaid > cfg["max_saldo_over_inscritos"]:
        return Result("6", False, f"buyer still owes {unpaid:.1%} of the prior "
                      f"year's liquidated invoices (limit "
                      f"{cfg['max_saldo_over_inscritos']:.0%}). Delay on this "
                      f"scale exhausts the working capital.", ev)
    return Result("6", True, f"buyer has paid {1 - unpaid:.1%} of prior-year "
                  f"liquidated invoices and wrote off {written_off:.1%}", ev)


def rule_7_me_epp_reserve(line_values, config=None):
    """LC 123 art. 48 I reserves lines <= R$80.000 EXCLUSIVELY to ME/EPP,
    PER ITEM not per tender. Where a body marks them 'Sem beneficio' that is
    an impugnacao ground: free, written, statutory."""
    cfg = _cfg(config)["rule_7_me_epp_reserve"]
    if not cfg.get("enabled", True):
        return Result("7", True, "rule disabled")

    threshold = cfg["threshold_brl"]
    reserved = [v for v in (line_values or []) if v is not None and v <= threshold]
    ev = {"threshold": threshold, "reserved_lines": len(reserved),
          "total_lines": len(line_values or [])}
    if reserved:
        return Result("7", True, f"{len(reserved)} of {len(line_values)} lines "
                      f"are at or under R$ {threshold:,.0f} and are reserved "
                      f"EXCLUSIVELY to ME/EPP by LC 123 art. 48 I. If the "
                      f"tender marks them 'Sem beneficio', that is an "
                      f"impugnacao ground.", ev, is_flag=True)
    return Result("7", True, "no lines under the ME/EPP exclusive threshold", ev)


def rule_8_spec_control(classified, total, config=None):
    """Filter 4 at tender level: if we cannot classify the lines, we cannot
    price them, and an unpriced line is not a cheap line."""
    cfg = _cfg(config)["rule_8_spec_control"]
    if not cfg.get("enabled", True):
        return Result("8", True, "rule disabled")
    if not total:
        return Result("8", False, "no items to classify", {"total": 0})
    unclassified = total - classified
    ratio = unclassified / total
    ev = {"classified": classified, "total": total,
          "unclassified_ratio": round(ratio, 3)}
    if ratio > cfg["max_unclassified_ratio"]:
        return Result("8", False, f"{unclassified} of {total} lines could not "
                      f"be spec-classified ({ratio:.0%}). An unclassified line "
                      f"cannot be priced, and pricing it anyway is the 36-point "
                      f"bathtub error.", ev)
    return Result("8", True, f"{classified} of {total} lines spec-classified", ev)


def rule_9_payment_deadline(edital_text, parsed_days=None, config=None):
    """There is NO national figure. The deadline is in the buyer's own decree."""
    cfg = _cfg(config)["rule_9_payment_deadline"]
    if not cfg.get("enabled", True):
        return Result("9", True, "rule disabled")

    decreto = _any([cfg["patterns"][0]], edital_text)
    ev = {"decreto": decreto, "days": parsed_days}
    if parsed_days is None:
        return Result("9", False, f"payment deadline not extracted"
                      + (f" (found the citation {decreto!r} but not the days)"
                         if decreto else " and no Decreto Municipal cited")
                      + ". There is no national default to fall back on.", ev)
    if parsed_days > cfg["max_days_acceptable"]:
        return Result("9", False, f"payment in {parsed_days} days exceeds the "
                      f"{cfg['max_days_acceptable']}-day limit the working "
                      f"capital can carry", ev)
    return Result("9", True, f"payment in {parsed_days} days"
                  + (f" per {decreto}" if decreto else ""), ev)


def rule_10_pagamento_antecipado(edital_text, config=None):
    """art. 145 permits it only where expressly in the edital. Rare, and where
    it appears the working-capital problem is zero."""
    cfg = _cfg(config)["rule_10_pagamento_antecipado"]
    if not cfg.get("enabled", True):
        return Result("10", True, "rule disabled")
    flat = strip_accents(edital_text or "").upper()
    for pat in cfg["patterns"]:
        for match in re.finditer(pat, flat, re.I | re.M):
            if _negated(flat, match.start()):
                # MEASURED: Bom Sucesso do Sul/PR forbids it in so many words
                # and a plain grep offered it as a working-capital gift.
                return Result("10", True, "advance payment is expressly FORBIDDEN "
                              "in this edital", {"match": match.group(0),
                                                 "negated": True})
            return Result("10", True, "PAGAMENTO ANTECIPADO is expressly provided "
                          "(art. 145) -- the working-capital cost of this tender is "
                          "zero. Prioritise it.", {"match": match.group(0)},
                          is_flag=True)
    return Result("10", True, "no advance payment", {"match": None})


def rule_11_log_the_bid(logged, config=None):
    cfg = _cfg(config)["rule_11_log_the_bid"]
    if not cfg.get("enabled", True):
        return Result("11", True, "rule disabled")
    if not logged:
        # A FLAG, not a gate. Logging happens AT BID TIME; before she bids
        # nothing is logged yet, and treating that as a rejection made every
        # admissible tender read NAO LICITAR. The obligation stands: an
        # unlogged bid is information nobody can ever recover.
        return Result("11", True, "not yet logged -- write the bid log the moment "
                      "she bids. PNCP never publishes who lost or what they bid.",
                      {"logged": False}, is_flag=True)
    return Result("11", True, "bid logged", {"logged": True})


def rule_12_can_she_carry_it(quantity, cogs_per_kit, config=None, capital=None):
    """A win she cannot fund or cannot pack is WORSE than not bidding.

    It is a default, a penalty, and possibly a bidding suspension. Two
    ceilings, both from config/capital.yaml:
      - kits per order: the self-pack ceiling until a co-packer with a stated
        capacity is on file
      - lot COGS vs available capital, over the float window
    Unknown capital is NOT a pass. The rule says it cannot verify.
    """
    cfg = _cfg(config)["rule_12_can_she_carry_it"]
    if not cfg.get("enabled", True):
        return Result("12", True, "rule disabled")
    cap = capital if capital is not None else _capital_cfg()

    if quantity is None or cogs_per_kit is None:
        return Result("12", False, "quantity or unit cost unknown -- cannot "
                      "tell whether she could carry this lot if she won it",
                      {"quantity": quantity, "cogs_per_kit": cogs_per_kit,
                       "outcome": "UNVERIFIABLE"})

    max_kits = (cap.get("lot_limits") or {}).get("max_kits_per_order")
    if max_kits is not None and quantity > max_kits:
        return Result("12", False, f"{quantity:,} kits exceeds the {max_kits:,}-kit "
                      f"ceiling she can physically fulfil. Winning this would "
                      f"be a default, not a sale.",
                      {"quantity": quantity, "max_kits": max_kits,
                       "outcome": "FULFILMENT"})

    lot_cogs = quantity * cogs_per_kit
    available = (cap.get("capital") or {}).get("available_brl")
    if available is None:
        passed = bool(cfg.get("unknown_capital_is_a_pass", False))
        return Result("12", passed, f"lot needs R$ {lot_cogs:,.2f} of goods and "
                      f"available capital is NOT SET in config/capital.yaml -- "
                      f"cannot confirm she could fund it",
                      {"lot_cogs": round(lot_cogs, 2), "available": None,
                       "outcome": "UNVERIFIABLE"})

    ceiling = available * float(cfg.get("max_capital_share_per_lot", 1.0))
    if lot_cogs > ceiling:
        return Result("12", False, f"lot needs R$ {lot_cogs:,.2f} of goods "
                      f"against R$ {ceiling:,.2f} she can commit. She could "
                      f"not pay the wholesaler.",
                      {"lot_cogs": round(lot_cogs, 2), "ceiling": round(ceiling, 2),
                       "outcome": "CAPITAL"})
    return Result("12", True, f"lot needs R$ {lot_cogs:,.2f}; within the "
                  f"R$ {ceiling:,.2f} she can commit and the {max_kits}-kit "
                  f"fulfilment ceiling",
                  {"lot_cogs": round(lot_cogs, 2), "ceiling": round(ceiling, 2),
                   "max_kits": max_kits})


def rule_13_srp_calloff(srp, calloff_days, stock_buffer_days=None, config=None):
    """An SRP call-off she cannot serve turns a WIN into a sanction.

    Registro de precos binds her for 12 months at a fixed price and the buyer
    to nothing. Refusing the empenho is descumprimento total, cancels her
    registration and draws a 20% fine. Where the call-off term is a few days,
    'buy after the empenho' is impossible and only stock -- which the
    business model forbids -- or a co-packer buffer covers it.
    """
    cfg = _cfg(config)["rule_13_srp_calloff"]
    if not cfg.get("enabled", True):
        return Result("13", True, "rule disabled")
    if not srp:
        return Result("13", True, "not a registro de precos -- one-shot purchase",
                      {"srp": False})

    limit = int(cfg["max_calloff_days_without_stock"])
    if calloff_days is None:
        passed = bool(cfg.get("unknown_calloff_is_a_pass", False))
        return Result("13", passed, "REGISTRO DE PRECOS and the call-off delivery "
                      "term is UNKNOWN -- an ARP binds her for 12 months; do not "
                      "admit it on a guess. VERIFICAR the prazo de entrega por "
                      "ordem de fornecimento.",
                      {"srp": True, "calloff_days": None, "outcome": "UNVERIFIABLE"})

    if calloff_days <= limit and not stock_buffer_days:
        return Result("13", False, f"REGISTRO DE PRECOS with a {calloff_days}-day "
                      f"call-off and no stock buffer on file. Buying after the "
                      f"empenho cannot make that; refusing it is descumprimento "
                      f"total (art. 90 par. 5), registration cancelled, 20% fine. "
                      f"A win here is a sanction.",
                      {"srp": True, "calloff_days": calloff_days, "limit": limit,
                       "outcome": "CALLOFF"})
    if calloff_days <= limit:
        return Result("13", True, f"REGISTRO DE PRECOS with a {calloff_days}-day "
                      f"call-off, covered by a {stock_buffer_days}-day stock "
                      f"buffer on file -- watch it",
                      {"srp": True, "calloff_days": calloff_days,
                       "stock_buffer_days": stock_buffer_days}, is_flag=True)
    return Result("13", True, f"REGISTRO DE PRECOS, {calloff_days}-day call-off "
                  f"is workable by buying after the empenho",
                  {"srp": True, "calloff_days": calloff_days, "limit": limit})


def run_all(tender, config=None):
    """Run every rule over one tender dict. Returns (admit, results).

    admit is True only when no non-flag rule failed. Flags never block.
    """
    cfg = _cfg(config)
    results = [
        rule_1_lote_unico(tender.get("objeto"), tender.get("items"), cfg),
        rule_2_atestado(tender.get("edital_text"), cfg),
        rule_3_modelo_do_orgao(tender.get("edital_text"), cfg),
        rule_4_kit_size(tender.get("item_count"), cfg),
        rule_5_prazo_entrega(tender.get("prazo_days"), tender.get("uf"),
                             tender.get("uf_feasibility"), cfg),
        rule_6_buyer_payment(tender.get("siconfi"), cfg),
        rule_7_me_epp_reserve(tender.get("line_values"), cfg),
        rule_8_spec_control(tender.get("classified_count", 0),
                            tender.get("item_count") or 0, cfg),
        rule_9_payment_deadline(tender.get("edital_text"),
                                tender.get("payment_days"), cfg),
        rule_10_pagamento_antecipado(tender.get("edital_text"), cfg),
        rule_11_log_the_bid(tender.get("logged", False), cfg),
        rule_12_can_she_carry_it(tender.get("quantity"), tender.get("cogs_per_kit"),
                                 cfg, tender.get("capital")),
        rule_13_srp_calloff(tender.get("srp"), tender.get("calloff_days"),
                            tender.get("stock_buffer_days"), cfg),
    ]
    admit = all(r.passed for r in results if not r.is_flag)
    return admit, results
