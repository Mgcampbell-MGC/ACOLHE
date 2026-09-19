"""THE BID LOG. Append-only. The only asset here that compounds.

PNCP publishes who WON. It never publishes who lost, or what they bid:
/itens/{n}/resultados returns exactly one row -- the homologated winner --
even on a genuine multi-bidder pregao, and /propostas, /lances,
/classificacao, /fornecedores and /participantes all 404.

So nobody -- not her, not a competitor, not the R$3.997/yr software vendors --
can know the real win rate or the real losing prices. EXCEPT her, about her
own bids. After six months this file tells her exactly where to bid, and it is
a file nobody can buy.

Three invariants, enforced rather than trusted:
  1. APPEND ONLY. There is no update path and no delete path in this module.
  2. A correction is a NEW ROW that supersedes an old one, never an edit.
  3. No migration may drop a row. schema_version travels with every row and
     unknown columns are preserved.
"""

import csv
import json
import os
import sqlite3
from datetime import datetime, timezone

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS bid (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    schema_version    INTEGER NOT NULL,
    logged_at         TEXT    NOT NULL,
    bid_date          TEXT    NOT NULL,
    tender_key        TEXT    NOT NULL,
    municipio         TEXT,
    uf                TEXT,
    sku               TEXT,
    spec              TEXT,
    quantity          INTEGER,
    quantity_band     TEXT,
    her_cost          REAL,
    her_bid           REAL,
    estimate          REAL,
    result            TEXT,      -- won | lost | cancelled | pending
    winning_price     REAL,      -- when she loses, this is the prize
    n_bidders         INTEGER,
    rule_results      TEXT,      -- JSON, the rules AS THEY STOOD AT BID TIME
    supersedes        INTEGER,   -- a correction points at the row it replaces
    note              TEXT,
    extra             TEXT       -- JSON. Unknown columns survive migrations here.
);
CREATE INDEX IF NOT EXISTS idx_bid_tender ON bid(tender_key);
CREATE INDEX IF NOT EXISTS idx_bid_result ON bid(result);
CREATE INDEX IF NOT EXISTS idx_bid_uf ON bid(uf);
"""

_FIELDS = [
    "bid_date", "tender_key", "municipio", "uf", "sku", "spec", "quantity",
    "quantity_band", "her_cost", "her_bid", "estimate", "result",
    "winning_price", "n_bidders", "rule_results", "supersedes", "note", "extra",
]

VALID_RESULTS = {"won", "lost", "cancelled", "pending"}


def _band(quantity):
    """Quantity bands, because win rate varies by lot size far more than by UF."""
    if quantity is None:
        return None
    for ceiling, label in ((100, "1-100"), (500, "101-500"), (1000, "501-1k"),
                           (5000, "1k-5k"), (20000, "5k-20k")):
        if quantity <= ceiling:
            return label
    return "20k+"


def connect(db_path):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def append(conn, **kw):
    """Write one bid row. The ONLY write path in this module.

    Returns the new row id. Never modifies an existing row.
    """
    result = (kw.get("result") or "pending").lower()
    if result not in VALID_RESULTS:
        raise ValueError(
            f"result must be one of {sorted(VALID_RESULTS)}, got {result!r}"
        )
    if not kw.get("tender_key"):
        raise ValueError("tender_key is required -- an unattributable bid row "
                         "teaches nothing later")

    row = {f: kw.get(f) for f in _FIELDS}
    row["result"] = result
    row["bid_date"] = kw.get("bid_date") or datetime.now(timezone.utc).date().isoformat()
    row["quantity_band"] = kw.get("quantity_band") or _band(kw.get("quantity"))
    for json_field in ("rule_results", "extra", "spec"):
        value = row.get(json_field)
        if value is not None and not isinstance(value, str):
            row[json_field] = json.dumps(value, ensure_ascii=False)

    cols = ["schema_version", "logged_at"] + _FIELDS
    values = [SCHEMA_VERSION, datetime.now(timezone.utc).isoformat()] + [
        row[f] for f in _FIELDS
    ]
    cur = conn.execute(
        f"INSERT INTO bid ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
        values,
    )
    conn.commit()
    return cur.lastrowid


def correct(conn, original_id, **kw):
    """Supersede an earlier row with a new one. Never an in-place edit.

    Used when a result lands: the bid was logged 'pending' at bid time, and the
    outcome arrives weeks later.
    """
    prior = conn.execute("SELECT * FROM bid WHERE id = ?", (original_id,)).fetchone()
    if prior is None:
        raise ValueError(f"no bid row {original_id} to supersede")
    merged = {f: prior[f] for f in _FIELDS}
    merged.update(kw)
    merged["supersedes"] = original_id
    return append(conn, **merged)


def current_rows(conn):
    """Live view: a row that something else supersedes is history, not current."""
    superseded = {
        r["supersedes"]
        for r in conn.execute("SELECT supersedes FROM bid WHERE supersedes IS NOT NULL")
    }
    return [
        r for r in conn.execute("SELECT * FROM bid ORDER BY id")
        if r["id"] not in superseded
    ]


def export_csv(conn, path):
    """Trivially exportable, by design. She must never be locked in."""
    rows = [dict(r) for r in conn.execute("SELECT * FROM bid ORDER BY id")]
    if not rows:
        rows = []
        header = ["id", "schema_version", "logged_at"] + _FIELDS
    else:
        header = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def win_rate(conn, **filters):
    """What only she can know. Returns None until there is something to know.

    Deliberately refuses to report a rate off a handful of bids: an early
    win rate is noise, and acting on it is worse than having none.
    """
    rows = [r for r in current_rows(conn) if r["result"] in ("won", "lost")]
    for key, value in filters.items():
        rows = [r for r in rows if r[key] == value]
    if len(rows) < 10:
        return None, len(rows), (
            f"only {len(rows)} decided bids -- too few to mean anything. "
            f"A win rate off a handful of bids is noise."
        )
    won = sum(1 for r in rows if r["result"] == "won")
    return won / len(rows), len(rows), f"{won} of {len(rows)} decided bids"


def losing_margin(conn):
    """How far under her the winners came in. Nobody else in Brazil has this."""
    out = []
    for r in current_rows(conn):
        if r["result"] == "lost" and r["winning_price"] and r["her_bid"]:
            gap = (r["her_bid"] - r["winning_price"]) / r["her_bid"] * 100
            out.append({"tender_key": r["tender_key"], "uf": r["uf"],
                        "sku": r["sku"], "quantity_band": r["quantity_band"],
                        "her_bid": r["her_bid"],
                        "winning_price": r["winning_price"],
                        "gap_pct": round(gap, 1)})
    return sorted(out, key=lambda d: d["gap_pct"])
