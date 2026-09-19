"""One regression test per trap. Each of these produced a confidently wrong
number in this project's history. None of them is hypothetical.

Trap 3 is the only one still outstanding: it needs the price-history puller.
It is listed as an explicit TODO at the foot of this file, never silently omitted.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse.spec import classify  # noqa: E402
from price.bom import build  # noqa: E402
from price.cost import CostRow  # noqa: E402
from price.margin import cost_floor, suggest_bid  # noqa: E402
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
# TRAP 4 - cross-spec comparison inside one catalogue heading.
# A 17,2 L bathtub priced against a market whose live band is 20-25 L is a
# 36-percentage-point margin error. Of 259 banheira lines, 131 state a
# capacity and the 20-25 L band alone is 115 lines / R$1.038.317.
# --------------------------------------------------------------------------

def test_trap4_bathtub_capacity_bands_do_not_share_a_median():
    sku_small, ok_small, why_small = classify("BANHEIRA SENSITIVE FEMININO 17,2 L")
    sku_big, ok_big, _ = classify("BANHEIRA INFANTIL 24 L MONTE LIBANO")

    assert sku_small == "BANHEIRA" and sku_big == "BANHEIRA"
    # Same family, but only one of them conforms - so they never share a median.
    assert ok_big is True
    assert ok_small is False
    assert "17.2 L" in why_small or "17,2" in why_small or "outside" in why_small


def test_trap4_unstated_capacity_is_not_conforming():
    """An unstated spec must never be silently treated as conforming."""
    sku, ok, why = classify("BANHEIRA BABY ROSA PLASTIBRASIL")
    assert sku == "BANHEIRA"
    assert ok is False
    assert "capacity" in why.lower()


def test_trap4_shampoo_volume_band():
    """A 400ml retail bottle is not the 200ml a kit spec asks for."""
    _, ok_retail, _ = classify("SHAMPOO 400ML #16555 BUBA")
    _, ok_kit, _ = classify("SHAMPOO INFANTIL 200ML")
    assert ok_retail is False
    assert ok_kit is True


def test_trap4_hooded_towel_is_a_different_product():
    _, ok, why = classify("TOALHA DE BANHO COM CAPUZ 70X100")
    assert ok is False
    assert "capuz" in why.lower() or "hooded" in why.lower()


def test_trap4_sacola_is_not_a_mochila():
    """The R$27,34 sacola must not be priced as the R$52,27 mochila."""
    _, ok_sacola, why = classify("BOLSA COURINO VINICRON MAVE BABY")
    _, ok_mochila, _ = classify("MOCHILA BABY PRINTS #802 ESPERA FELIZ")
    assert ok_sacola is False
    assert ok_mochila is True
    assert "mochila" in why.lower()


def test_trap4_meias_pair_ambiguity():
    """'12 UNIDADES' of socks may be 12 socks or 12 pairs. Only trust PARES."""
    _, ok_vague, _ = classify("KIT MEIA BEBE - 12 UNIDADES")
    _, ok_clear, _ = classify("MEIA BEBE PIPOQUINHA - 4 PARES")
    assert ok_vague is False
    assert ok_clear is True


# --------------------------------------------------------------------------
# TRAP 6 - an adjacent market swept in by keyword.
# 4.052 rows carrying R$155,7M of a Mato Grosso SCHOOL-UNIFORM programme
# landed in a kit harvest. A '\bMEIA' regex pulled school socks in as baby
# socks at R$9,3M. Uncaught, the market was sized 3,7x too large.
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "descricao",
    [
        "TENIS ESCOLAR MASCULINO TAMANHO 34",
        "CAMISETA ESCOLAR MANGA CURTA MALHA PV",
        "BERMUDA ESCOLAR TACTEL AZUL MARINHO",
        "MEIA ESCOLAR BRANCA KIT UNIFORME",
        "MOCHILA ESCOLAR COSTAS REFORCADA",
        "AGASALHO ESCOLAR CONJUNTO MOLETOM",
    ],
)
def test_trap6_school_uniform_programme_excluded(descricao):
    sku, ok, why = classify(descricao)
    assert sku is None
    assert ok is False
    assert "programme" in why.lower() or "bundle" in why.lower()


def test_trap6_a_real_baby_sock_still_classifies():
    """The exclusion must not also kill the genuine article."""
    sku, ok, _ = classify("MEIA BEBE ZERINHO - 4 PARES - TAMANHO RN")
    assert sku == "MEIAS"
    assert ok is True


# --------------------------------------------------------------------------
# TRAP 9 - CATMAT is null at municipal level, and the kit market is 97%
# municipal. A classifier that needs catalogoCodigoItem classifies nothing
# where the money is.
# --------------------------------------------------------------------------

def test_trap9_classifier_never_requires_catmat():
    """No executable reference to a catalogue code anywhere in the classifier.

    Checked against the parsed AST rather than the raw text, so the module may
    still explain in prose why it refuses to use CATMAT.
    """
    import ast
    import inspect

    from parse import spec as spec_module

    tree = ast.parse(inspect.getsource(spec_module))
    names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    } | {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    } | {
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
        and len(node.value) < 200          # skip docstrings
    }
    for forbidden in ("catalogoCodigoItem", "codigoCatmat", "catmat_code", "catmat"):
        assert forbidden not in names, (
            f"{forbidden} is referenced in code in spec.py - CATMAT is null "
            f"on municipal tenders and the kit market is 97% municipal"
        )

    # And it classifies happily from the description alone.
    sku, ok, _ = classify("BODY MANGA LONGA 100% ALGODAO TAMANHO RN")
    assert sku == "BODY" and ok is True


def test_trap9_inmetro_certified_skus_are_refused():
    """Mamadeiras and chupetas carry Portaria Inmetro 490/2014 certification."""
    for descricao in ("MAMADEIRA ANTICOLICA 260ML", "CHUPETA SILICONE ORTODONTICA"):
        sku, ok, why = classify(descricao)
        assert sku is None
        assert ok is False
        assert "490/2014" in why or "excluded" in why.lower()


# --------------------------------------------------------------------------
# TRAP 10 - a retail price mistaken for a wholesale one. Every cost row must
# carry a supplier CNPJ and a verified_at, enforced rather than trusted.
# --------------------------------------------------------------------------

def _row(**kw):
    base = dict(
        bom_line="body", sku="BODY", cost=7.56, basis="per_piece",
        supplier="CONFECCOES EMILIO LTDA", supplier_cnpj="50191584000106",
        supplier_uf="SP", product_ref="KIT BODY ML 3UN #302084",
        url="https://www.emilio.com.br", verified_at="2026-09-19",
    )
    base.update(kw)
    return CostRow(**base)


def test_trap10_cost_row_requires_supplier_cnpj():
    with pytest.raises(ValueError, match="CNPJ"):
        _row(supplier_cnpj="")
    with pytest.raises(ValueError, match="CNPJ"):
        _row(supplier_cnpj="123")          # not 14 digits


def test_trap10_cost_row_requires_verified_at_and_url():
    with pytest.raises(ValueError, match="verified_at"):
        _row(verified_at="")
    with pytest.raises(ValueError, match="URL"):
        _row(url="")


def test_trap10_cost_row_requires_a_real_uf():
    """A trading name is not an address."""
    with pytest.raises(ValueError, match="UF"):
        _row(supplier_uf="")
    with pytest.raises(ValueError, match="UF"):
        _row(supplier_uf="Sao Paulo")      # must be the 2-letter UF


def test_trap10_a_good_row_is_accepted():
    assert _row().landed_cost() == 7.56


# --------------------------------------------------------------------------
# TRAP 11 - interstate cost not loaded. LC 123 art. 13 §1 XIII (h) charges a
# Simples optante the internal-minus-interstate ICMS difference: SP internal
# 18% vs interstate-into-SP 12% = ~6 points.
# Verified traps: atacadosaopaulo.com.br is in ES, rymo.com.br (listed by the
# Sao Paulo sindicato itself) is in AM.
# --------------------------------------------------------------------------

def test_trap11_non_sp_supplier_is_loaded_six_points():
    sp = _row(supplier_uf="SP", cost=10.00)
    es = _row(supplier_uf="ES", cost=10.00)     # atacadosaopaulo.com.br
    am = _row(supplier_uf="AM", cost=10.00)     # rymo.com.br

    assert sp.landed_cost() == 10.00
    assert es.landed_cost() == 10.60
    assert am.landed_cost() == 10.60
    assert es.is_interstate and am.is_interstate and not sp.is_interstate


def test_trap11_cheaper_headline_can_lose_after_loading():
    """An out-of-state supplier must beat SP by MORE than 6% to be cheaper."""
    sp = _row(supplier_uf="SP", cost=10.00)
    cheaper_looking = _row(supplier_uf="ES", cost=9.60)   # 4% cheaper headline

    assert cheaper_looking.cost < sp.cost
    assert cheaper_looking.landed_cost() > sp.landed_cost()


def test_trap11_an_unpriced_line_never_becomes_zero():
    """A gap must block, never silently cost R$0,00."""
    import os

    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "cost_table.csv",
    )
    bom = build(path)
    assert bom.gaps, "fixture expects unpriced lines"
    assert bom.confidence() == "FLOOR_ONLY"
    assert cost_floor(bom) is None
    price, why = suggest_bid(476.05, bom)
    assert price is None
    assert "unpriced" in why.lower()


# --------------------------------------------------------------------------
# TODO - still needs a module that does not exist yet.
#   TRAP 3  recency filter -> needs the price-history puller (dataResultado
#           filter). The endpoint returns ~5 years silently; without the
#           filter every pool is ~3x too large.
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# TRAP 4, second form - a stated capacity that the parser fails to READ looks
# exactly like an unstated one, so the failure is invisible. Found live: 'L'
# with a word boundary drops both '24 LITROS' and '22 Lts'.
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "text,expected",
    [
        ("BANHEIRA INFANTIL - 24 LITROS # BM2123", 24.0),
        ("BANHEIRA ADOLETA - 20 LITROS # 0362 CAJOVIL", 20.0),
        ("BANHEIRA PLASTIBABY 22 Lts", 22.0),
        ("BANHEIRA 22 LT", 22.0),
        ("BANHEIRA 20L AZUL", 20.0),
        ("BANHEIRA SENSITIVE 17,2 L", 17.2),
        # must NOT be read as a capacity
        ("BANHEIRA BABY 0-6 MESES", None),
        ("BANHEIRA SUPORTA 30 KG", None),
        ("BANHEIRA BABY ROSA PLASTIBRASIL", None),
    ],
)
def test_trap4_capacity_is_read_in_every_form_sellers_write_it(text, expected):
    from parse.spec import classifier

    assert classifier().capacity_litres(text) == expected


def test_trap4_cheapest_conforming_is_taken_from_a_sorted_set():
    """The R$29,71 error: a cheaper conforming tub existed in the same set and
    was missed by reading an unsorted list. Assert ordering explicitly."""
    from parse.spec import classifier

    cat = [("BANHEIRA INFANTIL 24 LITROS", 29.71),
           ("BANHEIRA ADOLETA 20 LITROS", 18.90),
           ("BANHEIRA TRANSLUCIDA 20 LITROS", 24.08),
           ("BANHEIRA SENSITIVE 17,2 L", 22.90)]
    clf = classifier()
    conforming = [
        (price, name) for name, price in cat
        if clf.classify(name)[1]
    ]
    assert min(conforming)[0] == 18.90
    assert 22.90 not in [p for p, _ in conforming]   # 17,2 L never conforms
