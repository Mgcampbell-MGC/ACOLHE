"""Margin, and the bid price that follows from it.

Two rules that override any pricing instinct:

SIZE AGAINST THE HOMOLOGATED AWARD, NEVER THE ESTIMATE. The estimate is a
pre-bid ceiling built to be beaten. Award/estimate runs at a median 0,75-0,80
and the haircut worsens with lot size.

NEVER BID BELOW THE COST FLOOR. And when the BOM is incomplete, the floor is
not known -- it is only a lower bound -- so there is no safe bid at all.
"""

from dataclasses import dataclass

# Award / estimate, measured across bands: assembled 0,75 - components 0,80 -
# body+macacao 0,79. p25 0,52, p75 0,99. ~60% clear >=70% of estimate.
OPENING_ANCHOR = 0.75

# Simples Nacional Anexo I effective rate by RBT12. LC 123.
SIMPLES_ANEXO_I = [
    (180_000, 4.00),
    (360_000, 5.65),
    (500_000, 6.73),
    (720_000, 7.58),
]


def simples_rate(rbt12):
    for ceiling, rate in SIMPLES_ANEXO_I:
        if rbt12 <= ceiling:
            return rate
    return SIMPLES_ANEXO_I[-1][1]


@dataclass
class Margin:
    unit_price: float
    unit_cost: float
    quantity: int
    tax_pct: float
    gross_pct: float
    gross_total: float
    net_pct: float
    is_floor_only: bool
    warnings: list


def compute(unit_price, bom, quantity=1, rbt12=180_000, tier="published"):
    """Margin on one line at a given sell price.

    Returns net of the Simples rate, because a gross margin that ignores tax
    is not a margin the founder can spend.
    """
    unit_cost = bom.total_with_freight(tier=tier)
    tax_pct = simples_rate(rbt12)

    gross_pct = ((unit_price - unit_cost) / unit_price * 100) if unit_price else 0.0
    net_pct = gross_pct - tax_pct
    gross_total = (unit_price - unit_cost) * quantity

    warnings = []
    if not bom.is_complete:
        warnings.append(
            f"BOM is INCOMPLETE ({len(bom.gaps)} unpriced line(s)). This cost is "
            f"a FLOOR, so the margin shown is a CEILING and the real margin is "
            f"lower. Do not bid on it."
        )
    if bom.freight_is_estimate:
        warnings.append(
            f"Freight R$ {bom.freight_per_kit:,.2f} is an ESTIMATE "
            f"({bom.freight_basis}), not a quote. Low-density goods ship on "
            f"dimensional weight; get one real quote before bidding north."
        )
    if tier == "account":
        warnings.append(
            "Priced at the ACCOUNT tier, which is an INFERENCE. No supplier has "
            "been asked. Do not bid on this number."
        )
    for reason in bom.blocking_reasons():
        warnings.append(reason)

    return Margin(
        unit_price=round(unit_price, 2),
        unit_cost=round(unit_cost, 2),
        quantity=quantity,
        tax_pct=tax_pct,
        gross_pct=round(gross_pct, 1),
        gross_total=round(gross_total, 2),
        net_pct=round(net_pct, 1),
        is_floor_only=not bom.is_complete,
        warnings=warnings,
    )


def cost_floor(bom, tier="published"):
    """The price below which a bid loses money. None when it cannot be known."""
    if not bom.is_complete:
        return None
    return bom.total_with_freight(tier=tier)


def suggest_bid(estimate, bom, rbt12=180_000, anchor=OPENING_ANCHOR):
    """Propose an opening price. She decides; the system only proposes.

    Returns (price, rationale). price is None when no safe bid exists.
    """
    floor = cost_floor(bom)
    if floor is None:
        return None, (
            f"NO BID: the BOM has {len(bom.gaps)} unpriced line(s), so the cost "
            f"floor is unknown. Any price here is a guess."
        )
    if bom.freight_is_estimate and str(bom.freight_basis).upper().startswith("UNQUOTED"):
        # A kit is a bag of air that ships on dimensional weight. With freight
        # at R$0,00 the 'floor' is not a floor: on a Northeast lot it can be
        # the whole gross margin. Unquoted freight blocks exactly like an
        # unpriced line.
        return None, (
            f"NO BID: freight is UNQUOTED. The cost floor R$ {floor:,.2f} omits "
            f"it entirely, and on cubed goods to the Northeast it can exceed the "
            f"margin. Get one measured freight figure before pricing."
        )

    anchored = estimate * anchor
    if anchored <= floor:
        return None, (
            f"NO BID: {anchor:.0%} of the estimate is R$ {anchored:,.2f}, at or "
            f"below the cost floor R$ {floor:,.2f}. This tender cannot be won "
            f"profitably. There is no pricing skill that rescues a tender she "
            f"should not have entered."
        )

    gross = (anchored - floor) / anchored * 100
    net = gross - simples_rate(rbt12)
    return round(anchored, 2), (
        f"{anchor:.0%} of estimate R$ {estimate:,.2f} = R$ {anchored:,.2f}; "
        f"cost floor R$ {floor:,.2f}; gross {gross:.1f}%, net of Simples "
        f"{net:.1f}%."
    )
