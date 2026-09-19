"""The local-de-entrega reader against the SEVEN REAL EDITAIS (plus two TRs).

Why it matters (price/freight.py, measured 2026-09-19): one parcel per kit
to a Northeast capital is 37-52% of the kit price; one LTL shipment to ONE
consignee is ~15%. The expectations below are the human reading of each
text, recorded here so the reader can never drift from them silently.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse.entrega import (CALLOFF, HOUSEHOLD, ONE_ADDRESS, UNKNOWN,  # noqa: E402
                           classify_delivery)
from price.freight import estimate  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITAIS = os.path.join(ROOT, "data", "editais")

# stem -> (mode, parcelado, street fragment or None), from reading the clause
EXPECTED = {
    # 5.3 "A entrega devera ocorrer no Fundo Municipal de Saude, Rua Nereu Ramos 107";
    # 5.1 "de forma parcelada, conforme demanda"
    "agrolandia_sc_pe01_2026": (ONE_ADDRESS, True, "NEREU RAMOS"),
    # TR: validity counted "a contar da data de entrega a SEMTDES"; kits go to
    # the gestantes THROUGH the CRAS -- purpose, not the supplier's obligation
    "belterra_pa_26-017": (ONE_ADDRESS, False, None),
    # 8.7 "entregues na Secretaria Municipal de Assistencia Social" (no street);
    # obrigacoes b) "ate o local indicado pela Administracao" is boilerplate
    "bocaiuvadosul_pr_pe40_2025": (ONE_ADDRESS, True, None),
    # Cap. XXIII: "nos locais determinados pelo departamento solicitante ...
    # na ordem de servico", "parceladamente"
    "bomsucessodosul_pr_pe34_2026_EDITAL": (CALLOFF, True, None),
    # the TR is silent on the place; the edital answers
    "bomsucessodosul_pr_pe34_2026_TR": (UNKNOWN, True, None),
    # "no local indicado pela Administracao, preferencialmente nas
    # dependencias do CRAS ou em outro endereco designado pelo Municipio"
    "coronelxavierchaves_mg_pl72_2026_EDITAL_RETIFICADO": (CALLOFF, True, None),
    # 8.2 names the Secretaria at Rua Mato Grosso 47 "ou em local ainda a ser
    # determinado pelo SETOR DEMANDANTE, constante na nota de empenho"
    "irece_ba_dom2777": (CALLOFF, True, "MATO GROSSO"),
    # 14.4 "nos locais indicados na respectiva Ordem de Fornecimento"
    "saojoaodoparaiso_ma_23388": (CALLOFF, True, None),
    # TR 4.1 "na Prefeitura de Sao Pedro do Iguacu, Rua Niteroi 121";
    # 4.2 "conforme a necessidade da contratante"
    "saopedrodoiguacu_pr_TR_kit": (ONE_ADDRESS, True, "NITEROI"),
}


def _text(stem):
    path = os.path.join(EDITAIS, stem + ".txt")
    if not os.path.exists(path):
        pytest.skip(f"{stem}.txt not present")
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


@pytest.mark.parametrize("stem,expected", sorted(EXPECTED.items()))
def test_reader_matches_the_human_reading_of_each_real_edital(stem, expected):
    mode, parcelado, street = expected
    d = classify_delivery(_text(stem))
    assert d.mode == mode, f"{stem}: {d.mode} ({d.reason})"
    assert d.parcelado is parcelado, f"{stem}: parcelado={d.parcelado}"
    if street:
        assert street in (d.evidence.get("street") or ""), d.evidence


def test_none_of_the_real_editais_delivers_to_households():
    modes = [classify_delivery(_text(s)).mode for s in EXPECTED]
    assert HOUSEHOLD not in modes


def test_only_a_single_shot_lot_to_one_seat_is_priced_as_ltl():
    """Eight of nine say parcelado or leave the address to the ordem de
    fornecimento: the shipments are small and the bid must survive parcel
    freight. Belterra is the one single-shot delivery to one seat."""
    ltl = [s for s in EXPECTED if classify_delivery(_text(s)).freight_mode == "ltl"]
    assert ltl == ["belterra_pa_26-017"]


# -- synthetic clauses the seven do not contain ------------------------------

def test_household_delivery_is_named_and_unbiddable():
    d = classify_delivery("8.1 Os kits deverao ser entregues no domicilio das beneficiarias, "
                          "conforme lista fornecida pela Secretaria.")
    assert d.mode == HOUSEHOLD and d.freight_mode == "parcel"
    assert "NAO LICITAR" in d.reason


def test_purpose_of_the_purchase_is_not_a_delivery_obligation():
    d = classify_delivery("Aquisicao de kit natalidade para serem entregues as gestantes "
                          "atendidas pelo CRAS. 4.1 Os kits serao entregues na Secretaria "
                          "Municipal de Assistencia Social.")
    assert d.mode == ONE_ADDRESS


def test_the_foro_clause_is_not_a_home_delivery():
    d = classify_delivery("Fica eleito o foro da comarca, com renuncia a qualquer outro, por "
                          "mais privilegiado que seja o domicilio, para dirimir duvidas sobre a "
                          "entrega e o recebimento.")
    assert d.mode != HOUSEHOLD


def test_a_cross_reference_to_the_tr_is_not_a_calloff():
    d = classify_delivery("Os itens serao entregues no local indicado no Termo de Referencia. "
                          "TR 3.1: A entrega devera ocorrer na Secretaria Municipal de Saude, "
                          "Rua das Flores, n 10.")
    assert d.mode == ONE_ADDRESS and "FLORES" in d.evidence["street"]


def test_empty_text_is_unknown_and_priced_as_parcel():
    d = classify_delivery("")
    assert d.mode == UNKNOWN and d.freight_mode == "parcel" and "VERIFICAR" in d.reason


def test_freight_mode_feeds_the_measured_lanes():
    single = classify_delivery("4.1 Entrega unica na sede da Secretaria Municipal de Assistencia "
                               "Social de Fortaleza, Av. Central, n 100.")
    assert single.freight_mode == "ltl"
    per_kit, basis, _ = estimate("CE", 100, mode=single.freight_mode)
    assert per_kit == pytest.approx(53.99) and "LTL" in basis
    small = classify_delivery("4.1 Entregas parceladas conforme demanda na sede da Secretaria "
                              "Municipal de Assistencia Social de Fortaleza.")
    assert small.freight_mode == "parcel"
    assert estimate("CE", 100, mode=small.freight_mode)[0] == pytest.approx(152.60)
