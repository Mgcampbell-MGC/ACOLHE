"""The descent, tested against a stub because Family B has never answered.

The invariant that matters: UNAVAILABLE is not EMPTY. An outage that reads
as 'no items' would make a real kit tender look like nothing to price -- the
quietest possible way to lose it.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harvest.descend import (  # noqa: E402
    classify_item,
    descend,
    descend_one,
    parse_key,
    summarise,
)
from harvest.pncp_client import Unavailable  # noqa: E402

KEY = "46316600000164-1-000447/2025"


class Stub:
    """A client whose itens() does exactly what the test says."""

    def __init__(self, pages=None, raise_on_page=None):
        self.pages = pages or {}
        self.raise_on_page = raise_on_page
        self.calls = []

    def itens(self, cnpj, ano, sequencial, pagina=1, page_size=50):
        self.calls.append((cnpj, ano, sequencial, pagina))
        if self.raise_on_page is not None and pagina >= self.raise_on_page:
            raise Unavailable("https://pncp.gov.br/api/pncp/v1/x", [])
        return self.pages.get(pagina, {"data": [], "totalPaginas": 1})


def _item(n, desc, qty=5000, unit="UN", price=None):
    return {"numeroItem": n, "descricao": desc, "quantidade": qty,
            "unidadeMedida": unit, "valorUnitarioEstimado": price}


# -- the key --------------------------------------------------------------

def test_parse_key_reads_the_real_itaquaquecetuba_key():
    assert parse_key(KEY) == ("46316600000164", 2025, 447)


def test_parse_key_rejects_junk():
    assert parse_key("") is None
    assert parse_key(None) is None
    assert parse_key("not-a-key") is None


# -- the invariant --------------------------------------------------------

def test_unavailable_is_recorded_not_emptied():
    rec = descend_one(Stub(raise_on_page=1), KEY)
    assert rec["items_status"] == "UNAVAILABLE"
    assert rec["items"] == []
    assert "pncp" in rec["error"].lower()


def test_empty_is_distinct_from_unavailable():
    rec = descend_one(Stub(pages={1: {"data": [], "totalPaginas": 1}}), KEY)
    assert rec["items_status"] == "EMPTY"
    assert rec["error"] is None


def test_outage_mid_pagination_keeps_what_was_read_and_says_unavailable():
    pages = {1: {"data": [_item(i, "BODY MANGA LONGA") for i in range(50)],
                 "totalPaginas": 2}}
    rec = descend_one(Stub(pages=pages, raise_on_page=2), KEY)
    assert rec["items_status"] == "UNAVAILABLE"     # never OK on a partial read
    assert len(rec["items"]) == 50
    assert rec["pages_read"] == 1


def test_bad_key_is_its_own_status():
    rec = descend_one(Stub(), "garbage")
    assert rec["items_status"] == "BAD_KEY"


# -- reading and classifying ----------------------------------------------

def test_a_real_kit_is_classified_line_by_line():
    pages = {1: {"data": [
        _item(1, "Banheira para bebe de 22 LITROS, rigida"),
        _item(2, "Body manga longa 100% algodao tamanho RN"),
        _item(3, "Mamadeira de 50 ml com bico de silicone"),
        _item(4, "Lenco umedecido, contendo 48 lencos no pc"),
    ], "totalPaginas": 1}}
    rec = descend_one(Stub(pages=pages), KEY)
    assert rec["items_status"] == "OK"
    by = {i["numero"]: i for i in rec["items"]}
    assert by[1]["sku"] == "BANHEIRA" and by[1]["spec_ok"]
    assert by[2]["sku"] == "BODY" and by[2]["spec_ok"]
    assert by[3]["sku"] is None and "490/2014" in by[3]["reason"]   # Inmetro
    assert by[4]["sku"] == "UMEDECIDAS" and by[4]["spec_ok"]         # not a bundle


def test_pieces_are_computed_from_the_description_not_assumed():
    """Filter 2. PNCP items carry no capacity field."""
    rec = classify_item(_item(1, "FRALDA COM BAINHA - 3 UNIDADES", qty=1000, unit="PCT"))
    assert rec["pieces"] == 3000.0


def test_field_names_are_read_defensively_and_raw_row_is_kept():
    """Nobody has seen a Family B 200. Alternate spellings must not zero a row."""
    row = {"numero": 7, "descricaoItem": "Cueiro flanelado 80x80",
           "qtde": 240, "unidade": "UN", "valorUnitario": 4.1}
    rec = classify_item(row)
    assert rec["numero"] == 7
    assert rec["sku"] == "CUEIRO"
    assert rec["quantidade"] == 240
    assert rec["valor_unitario_estimado"] == 4.1
    assert rec["raw"] is row


def test_a_bare_list_payload_is_accepted():
    rec = descend_one(Stub(pages={1: [_item(1, "Toalha de banho simples 85x85")]}), KEY)
    assert rec["items_status"] == "OK" and rec["items"][0]["sku"] == "TOALHA_BANHO"


def test_pagination_follows_totalPaginas():
    pages = {1: {"data": [_item(i, "BODY") for i in range(50)], "totalPaginas": 2},
             2: {"data": [_item(i, "BODY") for i in range(50, 60)], "totalPaginas": 2}}
    stub = Stub(pages=pages)
    rec = descend_one(stub, KEY)
    assert len(rec["items"]) == 60
    assert [c[3] for c in stub.calls] == [1, 2]


# -- over many candidates ---------------------------------------------------

def test_descend_keeps_order_and_buyer_identity():
    cands = [{"pncp_key": KEY, "municipio": "Itaquaquecetuba", "uf": "SP"},
             {"pncp_key": "bad", "municipio": "X", "uf": "MA"}]
    out = descend(Stub(raise_on_page=1), cands)
    assert [r["municipio"] for r in out] == ["Itaquaquecetuba", "X"]
    assert out[0]["items_status"] == "UNAVAILABLE"
    assert out[1]["items_status"] == "BAD_KEY"


def test_summary_shouts_about_unavailable_and_never_calls_it_empty():
    out = descend(Stub(raise_on_page=1), [{"pncp_key": KEY, "municipio": "I", "uf": "SP"}])
    text = summarise(out)
    assert "UNAVAILABLE=1" in text
    assert "NOT empty kits" in text
    assert "VERIFICAR" in text
