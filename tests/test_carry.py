"""Rule 12 and the assembly line: can she CARRY a win, not just win it.

A win she cannot fund or cannot pack is worse than not bidding -- a default,
a penalty, possibly a bidding suspension. Every unknown here must surface as
UNVERIFIABLE, never as a quiet pass.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price.bom import BOM  # noqa: E402
from screen.rules import (  # noqa: E402
    feasibility_from_config,
    rule_5_prazo_entrega,
    rule_12_can_she_carry_it,
)


def _cap(available=40_000.0, max_kits=240):
    return {"capital": {"available_brl": available},
            "lot_limits": {"max_kits_per_order": max_kits},
            "fulfilment": {"self_pack_max_kits": max_kits}}


# -- rule 12 ---------------------------------------------------------------

def test_a_median_lot_passes():
    r = rule_12_can_she_carry_it(108, 176.32, capital=_cap())
    assert r.passed, r.reason


def test_itaquaquecetuba_scale_is_refused_on_fulfilment():
    """5.000 kits x 17 items = 85.000 items. One person cannot pack that."""
    r = rule_12_can_she_carry_it(5_000, 176.32, capital=_cap())
    assert not r.passed
    assert r.evidence["outcome"] == "FULFILMENT"
    assert "default" in r.reason.lower()


def test_a_lot_she_cannot_fund_is_refused_on_capital():
    r = rule_12_can_she_carry_it(200, 176.32, capital=_cap(available=10_000.0))
    assert not r.passed
    assert r.evidence["outcome"] == "CAPITAL"
    assert "wholesaler" in r.reason


def test_unknown_capital_is_not_a_pass():
    """config/capital.yaml ships with available_brl: null on purpose."""
    r = rule_12_can_she_carry_it(108, 176.32, capital=_cap(available=None))
    assert not r.passed
    assert r.evidence["outcome"] == "UNVERIFIABLE"
    assert "NOT SET" in r.reason


def test_unknown_quantity_or_cost_is_not_a_pass():
    assert not rule_12_can_she_carry_it(None, 176.32, capital=_cap()).passed
    assert not rule_12_can_she_carry_it(108, None, capital=_cap()).passed


def test_rule_12_reads_the_real_config_without_crashing():
    """The shipped config has capital null; the rule must say so, not raise."""
    r = rule_12_can_she_carry_it(108, 176.32)
    assert r.evidence["outcome"] in ("UNVERIFIABLE", "FULFILMENT", "CAPITAL") or r.passed


# -- rule 5 with unmeasured transit ----------------------------------------

def test_unmeasured_transit_is_verificar_not_pass():
    """config/ufs.yaml ships every transit_days as null until freight lands."""
    table = feasibility_from_config()
    assert table.get("MA") is None, "fixture expects MA transit still unmeasured"
    r = rule_5_prazo_entrega(15, uf="MA", uf_feasibility=table)
    assert not r.passed
    assert r.evidence["outcome"] == "UNVERIFIABLE"
    assert "UNMEASURED" in r.reason


def test_measured_transit_still_works():
    r = rule_5_prazo_entrega(15, uf="MG", uf_feasibility={"MG": 9})
    assert r.passed


def test_copacker_leg_is_added_above_the_self_pack_ceiling():
    """A big lot needs the co-packer leg; with its lead time unknown the whole
    UF goes back to None rather than being silently rounded to zero."""
    small = feasibility_from_config(quantity=100)
    big = feasibility_from_config(quantity=1_000)
    assert small.get("SP") == 3 + 1            # buy_and_assemble + transit
    assert big.get("SP") is None               # copacker_lead_days is null


# -- assembly line in the BOM ------------------------------------------------

def _bom():
    b = BOM(lines=[], gaps=[])
    b.self_pack_max_kits = 240
    return b


def test_small_lot_assembly_is_self_pack_at_zero_cash():
    cost, basis = _bom().assembly_cost(108)
    assert cost == 0.0
    assert "self-pack" in basis


def test_large_lot_with_no_quote_is_unquoted_not_zero():
    cost, basis = _bom().assembly_cost(1_000)
    assert cost is None
    assert "NO co-packer quote" in basis


def test_large_lot_with_a_quote_prices_it():
    b = _bom()
    b.copacker_cost_per_kit = 5.0
    cost, basis = b.assembly_cost(1_000)
    assert cost == 5.0
    assert "quoted" in basis


def test_total_with_freight_includes_a_quoted_copacker():
    b = _bom()
    b.copacker_cost_per_kit = 5.0
    assert b.total_with_freight(quantity=1_000) == pytest.approx(5.0)
    assert b.total_with_freight(quantity=100) == pytest.approx(0.0)
