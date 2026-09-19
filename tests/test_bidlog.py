"""The bid log's invariants. If these break, the only compounding asset in
the business is gone, and it cannot be rebuilt from any public source.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log import bidlog  # noqa: E402


@pytest.fixture
def conn(tmp_path):
    return bidlog.connect(str(tmp_path / "db" / "acolhe.sqlite"))


def _bid(**kw):
    base = dict(
        tender_key="46316600000164-1-000447/2025",
        municipio="Itaquaquecetuba", uf="SP", sku="KIT_NATALIDADE",
        quantity=5000, her_cost=174.86, her_bid=357.04, estimate=476.05,
        result="pending",
    )
    base.update(kw)
    return base


def test_append_returns_ids_and_persists(conn):
    first = bidlog.append(conn, **_bid())
    second = bidlog.append(conn, **_bid(tender_key="x-1/2026"))
    assert first and second and second > first
    assert len(bidlog.current_rows(conn)) == 2


def test_module_exposes_no_update_or_delete_path():
    """Append-only is a property of the module, not a habit of its callers."""
    import inspect

    source = inspect.getsource(bidlog)
    assert "UPDATE bid" not in source.upper().replace("'", "").replace('"', "")
    assert "DELETE FROM" not in source.upper()
    assert not hasattr(bidlog, "update")
    assert not hasattr(bidlog, "delete")


def test_a_correction_is_a_new_row_not_an_edit(conn):
    original = bidlog.append(conn, **_bid())
    corrected = bidlog.correct(conn, original, result="lost", winning_price=349.00)

    # The original row still exists, untouched.
    raw = list(conn.execute("SELECT * FROM bid ORDER BY id"))
    assert len(raw) == 2
    assert raw[0]["result"] == "pending"
    assert raw[1]["result"] == "lost"
    assert raw[1]["supersedes"] == original

    # But the live view shows only the correction.
    current = bidlog.current_rows(conn)
    assert len(current) == 1
    assert current[0]["id"] == corrected
    assert current[0]["winning_price"] == 349.00
    # Fields not restated are carried forward, not lost.
    assert current[0]["municipio"] == "Itaquaquecetuba"


def test_quantity_band_is_derived(conn):
    rid = bidlog.append(conn, **_bid(quantity=5000))
    row = [r for r in bidlog.current_rows(conn) if r["id"] == rid][0]
    assert row["quantity_band"] == "1k-5k"


def test_rule_results_are_stored_as_json(conn):
    rid = bidlog.append(conn, **_bid(rule_results={"1": True, "6": False}))
    row = [r for r in bidlog.current_rows(conn) if r["id"] == rid][0]
    assert '"6": false' in row["rule_results"]


def test_tender_key_is_required(conn):
    with pytest.raises(ValueError, match="tender_key"):
        bidlog.append(conn, **_bid(tender_key=""))


def test_result_must_be_a_known_value(conn):
    with pytest.raises(ValueError, match="result must be"):
        bidlog.append(conn, **_bid(result="maybe"))


def test_export_csv_round_trips(conn, tmp_path):
    bidlog.append(conn, **_bid())
    bidlog.append(conn, **_bid(tender_key="y-2/2026", result="won"))
    out = tmp_path / "bids.csv"
    assert bidlog.export_csv(conn, str(out)) == 2
    text = out.read_text()
    assert "Itaquaquecetuba" in text and "tender_key" in text


def test_export_csv_of_an_empty_log_still_writes_a_header(conn, tmp_path):
    out = tmp_path / "empty.csv"
    assert bidlog.export_csv(conn, str(out)) == 0
    assert "tender_key" in out.read_text()


def test_reopening_the_db_keeps_every_row(tmp_path):
    """No migration may drop a row."""
    path = str(tmp_path / "db" / "acolhe.sqlite")
    conn = bidlog.connect(path)
    for i in range(5):
        bidlog.append(conn, **_bid(tender_key=f"k-{i}/2026"))
    conn.close()

    reopened = bidlog.connect(path)          # runs the schema again
    assert len(bidlog.current_rows(reopened)) == 5


def test_win_rate_refuses_to_report_off_a_handful(conn):
    for i in range(6):
        bidlog.append(conn, **_bid(tender_key=f"k-{i}/2026",
                                   result="won" if i < 5 else "lost"))
    rate, n, why = bidlog.win_rate(conn)
    assert rate is None          # 83% off 6 bids would be a lie
    assert n == 6
    assert "noise" in why


def test_win_rate_reports_once_there_is_something_to_report(conn):
    for i in range(12):
        bidlog.append(conn, **_bid(tender_key=f"k-{i}/2026",
                                   result="won" if i < 3 else "lost"))
    rate, n, _ = bidlog.win_rate(conn)
    assert n == 12
    assert rate == pytest.approx(0.25)


def test_losing_margin_is_the_thing_nobody_else_can_compute(conn):
    bidlog.append(conn, **_bid(tender_key="a/2026", result="lost",
                               her_bid=400.00, winning_price=360.00))
    bidlog.append(conn, **_bid(tender_key="b/2026", result="lost",
                               her_bid=400.00, winning_price=200.00))
    bidlog.append(conn, **_bid(tender_key="c/2026", result="won"))

    gaps = bidlog.losing_margin(conn)
    assert len(gaps) == 2                      # the win contributes nothing
    assert gaps[0]["gap_pct"] == 10.0          # sorted: nearest miss first
    assert gaps[1]["gap_pct"] == 50.0


def test_pending_bids_are_excluded_from_win_rate(conn):
    for i in range(20):
        bidlog.append(conn, **_bid(tender_key=f"p-{i}/2026", result="pending"))
    rate, n, _ = bidlog.win_rate(conn)
    assert n == 0 and rate is None
