"""The rules against the SEVEN REAL EDITAIS, not two-line fixtures.

MEASURED 2026-09-19: with the quantitative-marker search spanning the whole
document, rule 2 returned QUANTITATIVE -> REJECT for 7 of 7 editais that have
a qualificacao tecnica heading, on '10%', '5%' and '100%' lifted from multa
and garantia clauses. The edital workstream, reading the same seven by hand,
found ONE without the clause and SIX qualitative. The first day Family B
returned edital text, every row of HOJE would have read NAO LICITAR.

These expectations are the human classification in data/editais/clauses.csv.
"""

import glob
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen.rules import rule_2_atestado, rule_10_pagamento_antecipado  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITAIS = os.path.join(ROOT, "data", "editais")

# file stem prefix -> clause class, from the edital workstream's reading
EXPECTED = {
    "agrolandia_sc_pe01_2026": "ABSENT",
    "belterra_pa_26-017": "QUALITATIVE",
    "bocaiuvadosul_pr_pe40_2025": "QUALITATIVE",
    "bomsucessodosul_pr_pe34_2026_EDITAL": "QUALITATIVE",
    "coronelxavierchaves_mg_pl72_2026_EDITAL_RETIFICADO": "QUALITATIVE",
    "irece_ba_dom2777": "QUALITATIVE",
    "saojoaodoparaiso_ma_23388": "QUALITATIVE",
    # Read from the real PNCP file on 2026-09-21, once Family B came back:
    # "ATESTADO(S) DE DESEMPENHO DE ATIVIDADE PERTINENTE E COMPATIVEL ...
    #  FORNECIDOS POR PESSOA JURIDICA DE DIREITO PUBLICO OU PRIVADO, INDICANDO
    #  QUANTIDADES, PRAZOS E OUTROS DADOS CARACTERISTICOS" (cl. 10.1.4.1).
    # It names no minimum quantity and no percentage, and it accepts a PRIVATE
    # issuer explicitly -- the first-sale route in docs/HABILITACAO.md, in the
    # words of the biggest buyer in the corpus.
    "itaqua_arq_7": "QUALITATIVE",
}


def _text(stem):
    path = os.path.join(EDITAIS, stem + ".txt")
    if not os.path.exists(path):
        pytest.skip(f"{stem}.txt not present")
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


@pytest.mark.parametrize("stem,expected", sorted(EXPECTED.items()))
def test_rule_2_matches_the_human_reading_of_each_real_edital(stem, expected):
    result = rule_2_atestado(_text(stem))
    got = result.evidence.get("clause")
    assert got == expected, (
        f"{stem}: rule 2 says {got} (match={result.evidence.get('match')!r}), "
        f"the edital reads {expected}"
    )
    # and a qualitative or absent clause must ADMIT the tender
    if expected != "QUANTITATIVE":
        assert result.passed


def test_rule_2_never_rejects_all_of_them():
    """The failure mode that was live: a whole-document percentage search."""
    verdicts = [rule_2_atestado(_text(s)).evidence.get("clause") for s in EXPECTED]
    assert verdicts.count("QUANTITATIVE") == 0, verdicts


def test_rule_10_reads_bom_sucesso_do_suls_prohibition_as_a_prohibition():
    """'nao sendo, em nenhuma hipotese, permitida a antecipacao de pagamentos'
    was being offered as a working-capital gift."""
    result = rule_10_pagamento_antecipado(_text("bomsucessodosul_pr_pe34_2026_EDITAL"))
    assert result.passed
    assert not result.is_flag
    assert result.evidence.get("negated") is True
    assert "FORBIDDEN" in result.reason


def test_rule_10_still_flags_a_genuine_offer():
    result = rule_10_pagamento_antecipado(
        "10.1 Sera admitido PAGAMENTO ANTECIPADO de 30% do valor, nos termos do art. 145."
    )
    assert result.is_flag
    assert result.evidence.get("negated") is None


def test_every_real_edital_file_is_covered():
    """A new PDF landing in data/editais without an expectation here must fail,
    so the real-file suite grows with the corpus instead of silently shrinking."""
    present = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(EDITAIS, "*.txt"))}
    ignored = {"familyB_retry_log", "bomsucessodosul_pr_pe34_2026_TR",
               "saopedrodoiguacu_pr_TR_kit", "crato_ce_dom5941",
               # Itaquaquecetuba's TR is a scanned PDF whose OCR is unusable
               # ("Secretaria" comes out as "ecretêriâ"). The retificado-2
               # EDITAL carries the same 17-item table in clean text, so the
               # rules are exercised against that instead.
               "itaqua_arq_8"}
    uncovered = present - set(EXPECTED) - ignored
    assert not uncovered, f"add expectations for: {sorted(uncovered)}"
