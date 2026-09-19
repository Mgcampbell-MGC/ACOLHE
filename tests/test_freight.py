"""Freight from measurements, and what it does to a bid.

The headline of 2026-09-19: one parcel per kit to a Northeast capital costs
37-52% of the kit price -- the whole gross margin. This suite pins that the
pricing engine now SEES that number instead of pricing at R$0,00.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price.bom import build  # noqa: E402
from price.freight import estimate, ltl_per_kit, parcel_per_kit  # noqa: E402
from price.margin import compute, suggest_bid  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COST_TABLE = os.path.join(ROOT, "data", "cost_table.csv")


# -- the measurements are what the module returns ---------------------------

@pytest.mark.parametrize("uf,price", [("BA", 132.90), ("PE", 152.60), ("CE", 152.60),
                                      ("PA", 152.60), ("MA", 188.40), ("SE", 188.40),
                                      ("RN", 188.40), ("MG", 116.60)])
def test_parcel_per_kit_returns_the_measured_pac_balcao_price(uf, price):
    got, days, basis = parcel_per_kit(uf)
    assert got == pytest.approx(price)
    assert days is not None and 5 <= days <= 10
    assert "capital CEP" in basis and "measured" in basis


def test_unmeasured_uf_is_unquoted_not_zero():
    got, days, basis = parcel_per_kit("AC")
    assert got is None and "no measured" in basis
    per_kit, basis, _ = estimate("AC")
    assert per_kit is None and basis.startswith("UNQUOTED")


def test_ltl_only_where_a_table_was_published():
    per_kit, src = ltl_per_kit("CE", 100)
    assert per_kit == pytest.approx(53.99) and "STC" in src
    assert ltl_per_kit("CE", 5000)[0] == pytest.approx(52.57)
    per_kit, why = ltl_per_kit("MA", 100)
    assert per_kit is None and "UNVERIFIED" in why


def test_ltl_mode_falls_back_to_parcel_rather_than_zero():
    per_kit, basis, _ = estimate("MA", 100, mode="ltl")
    assert per_kit == pytest.approx(188.40)
    assert "PAC balcao" in basis


# -- what freight does to the bid --------------------------------------------

def test_parcel_freight_to_the_northeast_eats_the_margin():
    """Goods R$198,78 + parcel R$188,40 to MA = R$387,18 > the R$359,05 award."""
    freight, basis, is_est = estimate("MA", 100)
    bom = build(COST_TABLE, freight_per_kit=freight, freight_is_estimate=is_est,
                freight_basis=basis)
    m = compute(359.05, bom, quantity=100)
    assert m.unit_cost > 359.05
    assert m.gross_pct < 0


def test_ltl_freight_leaves_a_real_but_thinner_margin():
    freight, basis, is_est = estimate("CE", 100, mode="ltl")
    bom = build(COST_TABLE, freight_per_kit=freight, freight_is_estimate=is_est,
                freight_basis=basis)
    m = compute(359.05, bom, quantity=100)
    assert 25 < m.gross_pct < 40           # ~30% with goods at 198,78 + 53,99


def test_a_measured_freight_basis_is_not_treated_as_unquoted():
    """suggest_bid blocks on UNQUOTED freight; a measured estimate must pass
    that gate (it may still be NO BID for other reasons, e.g. an open line)."""
    freight, basis, is_est = estimate("BA", 100)
    bom = build(COST_TABLE, freight_per_kit=freight, freight_is_estimate=is_est,
                freight_basis=basis)
    price, why = suggest_bid(476.05, bom)
    assert "freight is UNQUOTED" not in why
