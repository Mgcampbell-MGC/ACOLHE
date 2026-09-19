"""The scanner's job is recall first, precision second -- but never at the cost
of dragging in an adjacent programme.

A false positive costs one read. A false negative costs the tender. So the
patterns are broad and the exclusions do the discriminating. These tests pin
both directions, because widening one silently breaks the other.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harvest.daily import kit_signal, scan, summarise  # noqa: E402


# -- things that ARE our market -------------------------------------------

@pytest.mark.parametrize(
    "objeto",
    [
        "AQUISICAO DE KIT MATERNIDADE",
        "Registro de Precos para fornecimento de Kit Enxoval de Bebe",
        "AQUISICAO DE KIT NATALIDADE PARA GESTANTES DO MUNICIPIO",
        "CONTRATACAO DE EMPRESA PARA FORNECIMENTO DE ENXOVAIS",
        "AQUISICAO DE KIT PARA GESTANTES",
        "Aquisicao de bolsa maternidade e itens de enxoval",
        "AQUISICAO DE ENXOVAL NEONATAL",
        "KIT RECEM NASCIDO - PROGRAMA MUNICIPAL",
        "Aquisicao de kit bebe para o Fundo Municipal de Assistencia Social",
    ],
)
def test_real_kit_tenders_are_found(objeto):
    is_kit, hit, excl = kit_signal(objeto)
    assert is_kit, f"missed: {objeto!r} (excluded by {excl})"


# -- things that share the vocabulary and are NOT our market ---------------

@pytest.mark.parametrize(
    "objeto",
    [
        # The Mato Grosso programme that added R$155,7M to one kit harvest.
        "AQUISICAO DE KIT ESCOLAR E UNIFORME ESCOLAR PARA A REDE MUNICIPAL",
        "AQUISICAO DE ENXOVAL HOSPITALAR PARA O HOSPITAL MUNICIPAL",
        "AQUISICAO DE KIT MATERNIDADE - MEDICAMENTOS E MATERIAL HOSPITALAR",
        "AQUISICAO DE CESTA BASICA E KIT ENXOVAL PARA FAMILIAS - MERENDA",
        "LOCACAO DE VEICULO PARA TRANSPORTE DE GESTANTES",
        "AQUISICAO DE MATERIAL DE LIMPEZA E ENXOVAL PARA CRECHES",
        "CONTRATACAO DE SERVICOS DE LAVANDERIA DE ENXOVAL",
    ],
)
def test_adjacent_programmes_are_excluded(objeto):
    is_kit, hit, excl = kit_signal(objeto)
    assert not is_kit, f"wrongly admitted: {objeto!r}"
    # Whatever the reason, the scan must be able to SAY why it dropped the row.
    assert excl is not None, "an exclusion must name the pattern that caught it"


@pytest.mark.parametrize(
    "objeto",
    [
        "AQUISICAO DE COMBUSTIVEL",
        "PAVIMENTACAO ASFALTICA DE VIAS URBANAS",
        "AQUISICAO DE MATERIAL DE EXPEDIENTE",
        "",
        None,
    ],
)
def test_unrelated_tenders_do_not_match_at_all(objeto):
    is_kit, hit, excl = kit_signal(objeto)
    assert not is_kit
    assert hit is None


def test_an_exclusion_names_the_pattern_that_caught_it():
    """A silent drop is indistinguishable from a tender that never existed."""
    _, hit, excl = kit_signal("AQUISICAO DE KIT ENXOVAL ESCOLAR")
    assert hit is not None, "it did look like a kit"
    assert "ESCOLAR" in excl, "and we must be able to say why we dropped it"


# -- the scan over rows ----------------------------------------------------

def _row(objeto, uf="MG", mun="Exemplo", esfera="M", valor=100000.0):
    return {
        "numeroControlePNCP": f"x-{abs(hash(objeto)) % 9999}/2026",
        "objetoCompra": objeto,
        "valorTotalEstimado": valor,
        "srp": True,
        "modalidadeNome": "Pregão - Eletrônico",
        "orgaoEntidade": {"cnpj": "1" * 14, "razaoSocial": f"MUNICIPIO DE {mun}",
                          "esferaId": esfera},
        "unidadeOrgao": {"municipioNome": mun, "ufSigla": uf, "codigoIbge": "3100000"},
    }


def test_scan_splits_candidates_from_near_misses():
    rows = [
        _row("AQUISICAO DE KIT MATERNIDADE"),
        _row("AQUISICAO DE KIT ENXOVAL ESCOLAR PARA A REDE MUNICIPAL"),
        _row("PAVIMENTACAO ASFALTICA"),
        _row("Registro de Precos - Kit Enxoval de Bebe", uf="MA"),
    ]
    cand, near = scan(rows)
    assert len(cand) == 2
    assert {c["uf"] for c in cand} == {"MG", "MA"}
    # the school-uniform row is reported as a NEAR MISS, not silently dropped
    assert len(near) == 1
    assert "ESCOLAR" in near[0]["excluded_by"]
    # the road-paving row is not a near miss at all
    assert all("PAVIMENTA" not in n["objeto"] for n in near)


def test_scan_carries_the_buyer_identity_needed_downstream():
    """Every candidate must be joinable to SICONFI by IBGE and to the CNPJ rails."""
    cand, _ = scan([_row("KIT NATALIDADE")])
    row = cand[0]
    for field in ("cnpj", "municipio", "uf", "ibge", "pncp_key", "encerramento"):
        assert field in row


def test_summary_prints_the_rows_behind_the_count():
    """Never report an aggregate without the rows under it."""
    rows = [_row(f"AQUISICAO DE KIT MATERNIDADE {i}", valor=1000.0 * i)
            for i in range(12)]
    cand, near = scan(rows)
    text = summarise(cand, near)
    assert "KIT CANDIDATES: 12" in text
    assert "rows behind that count" in text
    # and it must state the recall ceiling rather than implying completeness
    assert "RECALL" in text and "FLOOR" in text


def test_summary_flags_a_short_harvest_rather_than_shrinking_quietly():
    class Report:
        rows_total, rows_served, pages_fetched = 40, 40, 2
        failures = [{"route": "publicacao", "status": 503}]

        def is_complete(self):
            return False

    text = summarise(*scan([_row("KIT MATERNIDADE")]), report=Report())
    assert "complete=False" in text
    assert "SHORT, not a quiet market" in text
