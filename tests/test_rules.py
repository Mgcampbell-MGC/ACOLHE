"""The 11 admission rules. Each test encodes a measured fact, not a guess.

The two that matter most are rule 2 and rule 6, in opposite directions:
rule 2 must NOT over-reject (rejecting every atestado clause discards most of
the market), and rule 6 must NOT under-reject (an unscreenable buyer defaulting
to pass is how the business loses money).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen.rules import (  # noqa: E402
    rule_1_lote_unico,
    rule_2_atestado,
    rule_3_modelo_do_orgao,
    rule_4_kit_size,
    rule_5_prazo_entrega,
    rule_6_buyer_payment,
    rule_7_me_epp_reserve,
    rule_8_spec_control,
    rule_9_payment_deadline,
    rule_10_pagamento_antecipado,
    rule_11_log_the_bid,
    run_all,
)


# -- rule 1 ----------------------------------------------------------------

def test_rule1_rejects_lote_unico():
    assert not rule_1_lote_unico("LOTE UNICO - KIT NATALIDADE 5000 UNIDADES")
    assert not rule_1_lote_unico("LOTE 01 - AQUISICAO DE ENXOVAIS")


def test_rule1_admits_per_item():
    got = rule_1_lote_unico("AQUISICAO DE KIT NATALIDADE", items=[1, 2, 3])
    assert got.passed


def test_rule1_single_item_is_lote_unico_by_another_name():
    assert not rule_1_lote_unico("AQUISICAO DE KITS", items=[1])


# -- rule 2: must not over-reject ------------------------------------------

def test_rule2_rejects_quantitative_atestado():
    got = rule_2_atestado(
        "QUALIFICACAO TECNICA: atestado comprovando fornecimento de no minimo "
        "50% da quantidade licitada."
    )
    assert not got.passed
    assert got.evidence["clause"] == "QUANTITATIVE"


def test_rule2_admits_qualitative_atestado():
    """Satisfied by ONE prior sale of any size, public or private."""
    got = rule_2_atestado(
        "QUALIFICACAO TECNICA: atestado de capacidade tecnica fornecido por "
        "pessoa juridica de direito publico ou privado, comprovando o "
        "fornecimento de objeto compativel."
    )
    assert got.passed
    assert got.evidence["clause"] == "QUALITATIVE"


def test_rule2_admits_when_absent():
    got = rule_2_atestado("1. DO OBJETO. 2. DA PARTICIPACAO. 3. DOS PRECOS.")
    assert got.passed
    assert got.evidence["clause"] == "ABSENT"


# -- rules 3, 4 -------------------------------------------------------------

def test_rule3_rejects_custom_model():
    assert not rule_3_modelo_do_orgao("Os itens serao CONFORME MODELO DO ORGAO.")
    assert rule_3_modelo_do_orgao("Os itens seguirao as especificacoes do TR.")


def test_rule4_kit_size():
    assert rule_4_kit_size(17).passed
    assert not rule_4_kit_size(19).passed
    assert rule_4_kit_size(17).is_flag          # 17 > warn_above 15
    assert not rule_4_kit_size(None).passed     # unknown is not a pass


# -- rule 5 -----------------------------------------------------------------

def test_rule5_rejects_impossible_deadline():
    """One live edital demanded 3 days."""
    got = rule_5_prazo_entrega(3, uf="MA", uf_feasibility={"MA": 12})
    assert not got.passed
    assert "3 days" in got.reason


def test_rule5_admits_workable_deadline():
    assert rule_5_prazo_entrega(15, uf="MG", uf_feasibility={"MG": 9}).passed


def test_rule5_unknown_prazo_is_not_a_pass():
    assert not rule_5_prazo_entrega(None, uf="BA").passed


# -- rule 6: must not under-reject -----------------------------------------

def test_rule6_rejects_nhamunda_shaped_buyer():
    """Nhamunda/AM paid 0,0% and published a R$2,12M kit tender."""
    got = rule_6_buyer_payment(
        {"status": "ok", "inscritos": 1_000_000, "saldo": 1_000_000, "cancelados": 0}
    )
    assert not got.passed
    assert got.evidence["unpaid_ratio"] == 1.0


def test_rule6_rejects_write_offs_as_default_not_delay():
    got = rule_6_buyer_payment(
        {"status": "ok", "inscritos": 1_000_000, "saldo": 0, "cancelados": 50_000}
    )
    assert not got.passed
    assert "WROTE OFF" in got.reason
    assert "default" in got.reason.lower()


def test_rule6_admits_a_payer():
    got = rule_6_buyer_payment(
        {"status": "ok", "inscritos": 1_000_000, "saldo": 150_000, "cancelados": 5_000}
    )
    assert got.passed


def test_rule6_unscreenable_buyer_is_rejected_not_passed():
    """The single most dangerous default in the whole system."""
    for payload in (None, {}, {"status": "api down"}, {"status": "ente not found"}):
        got = rule_6_buyer_payment(payload)
        assert not got.passed, f"{payload!r} must not pass"
        assert "REJECT" in got.reason


def test_rule6_zero_inscritos_does_not_divide_by_zero():
    got = rule_6_buyer_payment({"status": "ok", "inscritos": 0, "saldo": 0,
                                "cancelados": 0})
    assert not got.passed


# -- rule 7: an opportunity flag, never a rejection -------------------------

def test_rule7_flags_reserved_lines_without_blocking():
    got = rule_7_me_epp_reserve([50_000, 90_000, 20_000])
    assert got.passed and got.is_flag
    assert got.evidence["reserved_lines"] == 2
    assert "48 I" in got.reason


def test_rule7_no_reserved_lines():
    got = rule_7_me_epp_reserve([100_000, 250_000])
    assert got.passed and not got.is_flag


# -- rules 8, 9, 10, 11 -----------------------------------------------------

def test_rule8_rejects_mostly_unclassified():
    assert not rule_8_spec_control(classified=10, total=17).passed
    assert rule_8_spec_control(classified=16, total=17).passed


def test_rule9_extracts_decreto_and_rejects_unknown():
    got = rule_9_payment_deadline(
        "O pagamento observara o Decreto Municipal 7.088/2024.", parsed_days=28
    )
    assert got.passed
    assert "7.088/2024" in (got.evidence["decreto"] or "")

    unknown = rule_9_payment_deadline("O pagamento sera efetuado.", parsed_days=None)
    assert not unknown.passed
    assert "no national default" in unknown.reason


def test_rule9_rejects_a_deadline_capital_cannot_carry():
    assert not rule_9_payment_deadline("Decreto Municipal 1/2020",
                                       parsed_days=90).passed


def test_rule10_flags_advance_payment_as_an_opportunity():
    got = rule_10_pagamento_antecipado("Havera PAGAMENTO ANTECIPADO de 30%.")
    assert got.passed and got.is_flag
    assert "Prioritise" in got.reason


def test_rule11_unlogged_bid_fails():
    assert not rule_11_log_the_bid(False).passed
    assert rule_11_log_the_bid(True).passed


# -- the whole engine -------------------------------------------------------

def _good_tender():
    return {
        "objeto": "AQUISICAO DE KIT NATALIDADE PARA GESTANTES",
        "items": list(range(17)),
        "item_count": 17,
        "classified_count": 17,
        "edital_text": (
            "QUALIFICACAO TECNICA: atestado de capacidade tecnica comprovando "
            "fornecimento compativel. O pagamento observara o Decreto "
            "Municipal 7.088/2024."
        ),
        "prazo_days": 15,
        "uf": "MG",
        "uf_feasibility": {"MG": 9},
        "siconfi": {"status": "ok", "inscritos": 1_000_000, "saldo": 100_000,
                    "cancelados": 1_000},
        "line_values": [50_000, 120_000],
        "payment_days": 28,
        "logged": True,
    }


def test_run_all_admits_a_good_tender():
    admit, results = run_all(_good_tender())
    assert admit, [r.reason for r in results if not r.passed]
    assert len(results) == 11


def test_run_all_rejects_on_any_hard_rule():
    tender = _good_tender()
    tender["objeto"] = "LOTE UNICO - KIT NATALIDADE"
    admit, results = run_all(tender)
    assert not admit
    assert not results[0].passed


def test_run_all_flags_never_block():
    """Rule 7 and rule 10 fire as flags and must not change admission."""
    tender = _good_tender()
    tender["line_values"] = [50_000]                       # triggers rule 7 flag
    tender["edital_text"] += " Havera PAGAMENTO ANTECIPADO."  # rule 10 flag
    admit, results = run_all(tender)
    assert admit
    assert any(r.is_flag for r in results)


def test_every_failure_carries_a_readable_reason():
    """She reads these. A rejection with no reason is not a rejection."""
    tender = _good_tender()
    tender["siconfi"] = None
    tender["prazo_days"] = 2
    _, results = run_all(tender)
    failures = [r for r in results if not r.passed]
    assert failures, "fixture is meant to fail several rules"
    for r in failures:
        # A rejection she cannot act on is not a rejection.
        assert r.reason and len(r.reason) > 30, f"rule {r.rule_id}: {r.reason!r}"
        assert r.evidence is not None
    for r in results:
        assert r.reason, f"rule {r.rule_id} returned no reason at all"
