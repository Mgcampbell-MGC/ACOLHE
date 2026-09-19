"""Rule 13: an SRP call-off she cannot serve turns a WIN into a sanction.

Named by the risk register as the single most dangerous unaddressed risk --
everything else loses a tender or margin; this one produces a 20% fine and a
cancelled registration out of a tender she WON. The facts come from
docs/ORDER_TO_CASH.md: Belterra 'imediato', Bom Sucesso 5 d.u., Irece 5 dias.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen.rules import rule_13_srp_calloff, run_all  # noqa: E402


def test_a_one_shot_purchase_is_untouched():
    r = rule_13_srp_calloff(False, 2)
    assert r.passed and not r.is_flag


def test_short_calloff_with_no_stock_is_refused():
    """Irece/BA: registro de precos, entrega em 5 dias. Buy-after-empenho
    cannot make that from Sao Paulo."""
    r = rule_13_srp_calloff(True, 5)
    assert not r.passed
    assert r.evidence["outcome"] == "CALLOFF"
    assert "sanction" in r.reason


def test_belterra_style_immediate_calloff_is_refused():
    r = rule_13_srp_calloff(True, 0)
    assert not r.passed


def test_unknown_calloff_on_an_srp_is_not_a_pass():
    """An ARP binds her for 12 months. Admitting it without knowing the
    call-off term is admitting it on a guess."""
    r = rule_13_srp_calloff(True, None)
    assert not r.passed
    assert r.evidence["outcome"] == "UNVERIFIABLE"
    assert "VERIFICAR" in r.reason


def test_a_stock_buffer_turns_a_refusal_into_a_flag():
    r = rule_13_srp_calloff(True, 5, stock_buffer_days=10)
    assert r.passed and r.is_flag
    assert "buffer" in r.reason


def test_a_long_calloff_is_workable():
    """Coronel Xavier Chaves/MG: 20 dias corridos -- buy after the empenho."""
    r = rule_13_srp_calloff(True, 20)
    assert r.passed and not r.is_flag


def test_run_all_carries_rule_13_and_a_short_srp_blocks_admission():
    tender = {
        "objeto": "AQUISICAO DE KIT NATALIDADE", "items": list(range(17)),
        "item_count": 17, "classified_count": 17,
        "edital_text": ("QUALIFICACAO TECNICA: atestado de capacidade tecnica "
                        "comprovando fornecimento compativel. Decreto Municipal 1/2024."),
        "prazo_days": 15, "uf": "MG", "uf_feasibility": {"MG": 9},
        "siconfi": {"status": "ok", "inscritos": 1_000_000, "saldo": 100_000,
                    "cancelados": 1_000},
        "line_values": [50_000, 120_000], "payment_days": 28, "logged": True,
        "quantity": 120, "cogs_per_kit": 198.78,
        "capital": {"capital": {"available_brl": 40_000.0},
                    "lot_limits": {"max_kits_per_order": 240},
                    "fulfilment": {"self_pack_max_kits": 240}},
        "srp": True, "calloff_days": 5,
    }
    admit, results = run_all(tender)
    assert len(results) == 13
    assert not admit
    r13 = [r for r in results if r.rule_id == "13"][0]
    assert not r13.passed

    tender["calloff_days"] = 20
    admit, _ = run_all(tender)
    assert admit
