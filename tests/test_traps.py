"""One regression test per trap. Each of these produced a confidently wrong
number in this project's history. None of them is hypothetical.

Traps 3, 4, 6, 9, 10, 11 depend on modules not yet built (spec.py, cost.py) and
are marked xfail-by-absence rather than silently omitted -- see TODO markers.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse.normalise import (  # noqa: E402
    capacity_of,
    is_bundle,
    is_shadow_row,
    in_plausible_window,
    pack_count_from_text,
    pieces,
    unit_price_per_piece,
)


# --------------------------------------------------------------------------
# TRAP 1 - unit sigla ignored -> per-piece price 30-50% wrong.
# Fired NINE times in this archive, three of them within hours of the law
# warning about it being written.
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "unidade,capacidade,descricao,expected",
    [
        ("C", 0.0, "FRALDA DE PANO", 100.0),
        ("CENTO", None, "FRALDA DE PANO", 100.0),
        ("MIL", 0.0, "SACO PLASTICO", 1000.0),
        ("MILHEIRO", None, "SACO PLASTICO", 1000.0),
        ("UN", 0.0, "BODY MANGA LONGA", 1.0),
        ("PAR", 0.0, "MEIA INFANTIL", 2.0),
        ("DZ", 0.0, "PANO DE BOCA", 12.0),
        # capacidade field wins when positive
        ("CX", 24.0, "BANHEIRA", 24.0),
        # capacidade 0.0 must fall through to the text, not zero the row
        ("CX", 0.0, "FRALDA COM BAINHA - 3 UNIDADES", 3.0),
        ("PCT", 0.0, "BODY COM DECOTE CANOA (2 UNIDADES)", 2.0),
        ("PACOTE", None, "CUEIRO ESTAMPADO 50X80 - 3 UNIDADES", 3.0),
    ],
)
def test_trap1_unit_sigla(unidade, capacidade, descricao, expected):
    assert capacity_of(unidade, capacidade, descricao) == expected


def test_trap1_capacidade_zero_never_zeroes_a_row():
    """capacidadeUnidadeFornecimento is frequently 0.0. It must fall through."""
    assert pieces(500, "CX", 0.0, "FRALDA - 3 UNIDADES") == 1500.0
    assert pieces(500, "CX", 0.0, "FRALDA") == 500.0


def test_trap1_pack_count_lives_in_free_text():
    """PNCP items carry NO capacity field at all. The count is only in words."""
    assert pack_count_from_text("FRALDA COM BAINHA - 3 UNIDADES") == 3
    assert pack_count_from_text("BODY COM DECOTE CANOA (2 UNIDADES)") == 2
    assert pack_count_from_text("KIT BODY MANGA CURTA C/ 5") == 5
    assert pack_count_from_text("BODY MANGA LONGA CANELADO") == 1
    # a model year is not a pack count
    assert pack_count_from_text("KIT VERAO 2027") == 1


def test_trap1_per_piece_price():
    """The R$11,81 three-pack is R$3,94 a piece, not R$11,81."""
    got = unit_price_per_piece(11.81, 1, "PCT", 0.0,
                               "CUEIRO ESTAMPADO CARICIA 50X80 - 3 UNIDADES")
    assert round(got, 2) == 3.94


# --------------------------------------------------------------------------
# TRAP 2 - a lot total typed into precoUnitario with quantidade=1 lands in the
# smallest quantity band by construction. 126 of 1.934 rows, R$2,33M phantom.
# --------------------------------------------------------------------------

def test_trap2_lot_total_row_is_dropped():
    window = (1.0, 50.0)  # plausible R$/piece for a pen
    assert not in_plausible_window(673553.00, window)
    assert not in_plausible_window(59500.00, window)
    assert in_plausible_window(1.68, window)


def test_trap2_window_rejects_none_and_junk():
    assert not in_plausible_window(None, (1.0, 50.0))
    assert not in_plausible_window("abc", (1.0, 50.0))


# --------------------------------------------------------------------------
# TRAP 5 - regex family != product family.
# '\bBODY' swept in two-piece sets whose cost basis is two garments, turning
# R$77k of genuine clearing value into an apparent R$1,08M.
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "descricao",
    [
        "CONJUNTO BODY + BERMUDA",
        "CONJUNTO BODY + CALCA",
        "CONJUNTO  BODY- 3 PECAS  # 01.0412 - RADANI",
        "KIT  BODY MANGA LONGA + CULOTE SEM PE - TAMANHO RN AO G",
    ],
)
def test_trap5_multi_garment_set_is_not_a_body(descricao):
    assert is_bundle(descricao) is True


@pytest.mark.parametrize(
    "descricao",
    [
        "BODY MANGA LONGA 100% ALGODAO TAMANHO RN",
        "BODY SURPRESA - TAMANHO UNICO #002273 -MAFESSONI",
        "BODY COM DECOTE CANOA (2 UNIDADES)",
    ],
)
def test_trap5_a_plain_body_is_still_a_body(descricao):
    assert is_bundle(descricao) is False


# --------------------------------------------------------------------------
# TRAP 7 - duplicate shadow rows (same total, qt=0, vu=0). 432 of 7.549.
# --------------------------------------------------------------------------

def test_trap7_shadow_rows():
    assert is_shadow_row(0, 0) is True
    assert is_shadow_row(0.0, 0.0) is True
    assert is_shadow_row(1, 359.05) is False
    assert is_shadow_row(5000, 0) is False


# --------------------------------------------------------------------------
# TRAP 8 - a whole-kit LOTE row sitting inside a component family.
# A R$215.000 '600 KITS CONTENDO: Banheira... Mamadeira...' line was counted
# as FRALDA.
# --------------------------------------------------------------------------

def test_trap8_bundle_row_excluded_from_component_family():
    row = ("600 KITS CONTENDO: Banheira, Mamadeira, Fralda de pano, "
           "Body manga longa, Toalha de banho")
    assert is_bundle(row) is True


def test_trap8_kit_composto_por():
    assert is_bundle("KIT MATERNIDADE COMPOSTO POR 17 ITENS") is True


# --------------------------------------------------------------------------
# TODO - these need modules that do not exist yet. Listed so the gap is
# visible rather than silently missing from the suite.
#   TRAP 3  recency filter          -> needs the price-history puller
#   TRAP 4  spec control by capacity-> needs parse/spec.py + config/skus.yaml
#   TRAP 6  adjacent programme      -> needs parse/spec.py anti-patterns
#   TRAP 9  CATMAT null municipally -> needs parse/spec.py
#   TRAP 10 retail vs wholesale     -> needs price/cost.py schema
#   TRAP 11 interstate +6 points    -> needs price/cost.py
# --------------------------------------------------------------------------
