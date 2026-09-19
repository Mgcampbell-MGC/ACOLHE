"""A cost table nobody re-measures quietly rots, and nothing downstream would
notice: the margin engine would keep producing confident bids on a price
that stopped being true months ago. This is the one place that stops it.
"""

import csv
import datetime
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price.bom import build  # noqa: E402
from price.cost import FRESHNESS_DAYS, CostRow, is_stale, staleness_days  # noqa: E402
from price.margin import suggest_bid  # noqa: E402

TODAY = datetime.date(2026, 9, 19)


def _row(verified_at):
    return CostRow(
        bom_line="body", sku="BODY", cost=7.56, basis="per_piece",
        supplier="CONFECCOES EMILIO LTDA", supplier_cnpj="50191584000106",
        supplier_uf="SP", product_ref="x", url="https://www.emilio.com.br",
        verified_at=verified_at,
    )


def test_a_fresh_row_is_not_stale():
    assert not is_stale(_row("2026-09-19"), today=TODAY)
    assert not is_stale(_row("2026-08-25"), today=TODAY)          # 25 days


def test_a_row_past_the_limit_is_stale():
    assert is_stale(_row("2026-08-01"), today=TODAY)              # 49 days
    assert staleness_days(_row("2026-08-01"), today=TODAY) == 49


def test_an_unparseable_date_is_stale_not_fresh():
    """Never let a garbage date pass as a current price."""
    assert staleness_days(_row("sem data"), today=TODAY) is None
    assert is_stale(_row("sem data"), today=TODAY)


def test_a_missing_date_cannot_even_be_constructed():
    """Stronger than stale: CostRow refuses a row with no verified_at at all,
    so an undated price never reaches the freshness check in the first place."""
    with pytest.raises(ValueError, match="verified_at"):
        _row("")


def test_the_limit_is_configurable_per_call():
    assert is_stale(_row("2026-09-10"), today=TODAY, limit_days=5)
    assert not is_stale(_row("2026-09-10"), today=TODAY, limit_days=FRESHNESS_DAYS)


# -- through the BOM ---------------------------------------------------------

_HEADER = ("bom_line,sku,cost_per_bom_unit,basis,pack_size,listed_price,supplier,"
           "supplier_cnpj,supplier_uf,product_ref,url,verified_at,is_inference,"
           "spec_risk,notes\n")


def _table(tmp_path, rows):
    path = tmp_path / "cost.csv"
    with open(path, "w", newline="") as fh:
        fh.write(_HEADER)
        w = csv.writer(fh)
        for line, cost, seen in rows:
            w.writerow([line, line.upper(), cost, "unit", 1, cost,
                        "CONFECCOES EMILIO LTDA", "50191584000106", "SP", "ref",
                        "https://www.emilio.com.br", seen, "FALSE", "NONE", ""])
    return str(path)


def test_a_stale_row_becomes_a_gap_and_blocks_the_bid(tmp_path):
    path = _table(tmp_path, [("body", 7.56, "2026-09-19"),
                             ("mochila", 52.27, "2026-05-01")])   # 141 days old
    bom = build(path, today=TODAY)
    assert len(bom.lines) == 1
    assert len(bom.gaps) == 1
    gap = bom.gaps[0]
    assert gap["bom_line"] == "mochila"
    assert gap["spec_risk"] == "STALE"
    assert "141 days old" in gap["reason"]
    assert bom.confidence() == "FLOOR_ONLY"
    price, why = suggest_bid(476.05, bom)
    assert price is None


def test_a_fully_fresh_table_is_complete(tmp_path):
    path = _table(tmp_path, [("body", 7.56, "2026-09-19"),
                             ("mochila", 52.27, "2026-09-10")])
    bom = build(path, today=TODAY)
    assert bom.gaps == []
    assert bom.confidence() == "COMPLETE"


def test_the_real_cost_table_is_fresh_today():
    """Measured 2026-09-19. If this fails later, the weekly re-harvest is
    the fix -- not loosening the limit."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bom = build(os.path.join(root, "data", "cost_table.csv"), today=TODAY)
    assert not any(g["spec_risk"] == "STALE" for g in bom.gaps)
