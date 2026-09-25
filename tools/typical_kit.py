"""Deal-by-deal economics of the real per-item kit dispensas in data/typical_kit/.

Goods cost = sum over lines of qty_homologada x multiplier x checked unit cost
(the verifier's corrected cost wins over the first price). Only lines mapped
to a layette article are costed; revenue is taken on the SAME lines, so a
tender's margin never compares one set of items' cost with another's price.
"""
import json, os, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "typical_kit")
CEILING = 65492.11


def prices(r):
    out = {}
    for b in r["priced"]:
        chk = {c["sku_id"]: c for c in b["checks"]}
        for p in b["prices"]:
            c = chk.get(p["sku_id"]) or {}
            v = p["unit_cost"]
            if c.get("verdict") in ("WRONG_PRICE", "NONCONFORMING", "TOO_DEAR", "UNREACHABLE") and c.get("correct_unit_cost"):
                v = c["correct_unit_cost"]
            out[p["sku_id"]] = (v, c.get("verdict", "UNCHECKED"))
    return out


def deals(min_cover=0.9):
    r = json.load(open(os.path.join(D, "workflow_result.json")))
    T = {t["tender"]: t for t in json.load(open(os.path.join(D, "tenders.json")))}
    lines = [json.loads(l) for l in open(os.path.join(D, "lines.jsonl"))]
    mp = {m["line_id"]: m for m in r["mappings"]}
    pr = prices(r)
    rows = []
    for tid, t in T.items():
        if tid in ("T07", "T23") or t["contract_hom_total"] > CEILING:
            continue
        rev = rev_c = cost = 0.0
        detail = []
        for o in (l for l in lines if l["tender"] == tid):
            q = o["qty_homologada"] or o["qty"] or 0
            lr = q * o["hom_unit"]; rev += lr
            m = mp.get(o["line_id"])
            if not m or m["sku_id"] == "NOT_KIT":
                continue
            v = pr.get(m["sku_id"].replace("NEW:", ""), (None,))[0]
            if v is None:
                continue
            lc = q * m["multiplier"] * v
            rev_c += lr; cost += lc
            detail.append((o["line_id"], o["desc"][:60], q, o["hom_unit"], m["sku_id"], m["multiplier"], v, lr - lc))
        if rev and rev_c / rev >= min_cover:
            rows.append(dict(tender=tid, municipio=t["municipio"], uf=t["uf"], kits=t["max_line_qty"],
                             revenue=rev_c, goods=cost, detail=detail))
    return rows


if __name__ == "__main__":
    rows = deals()
    print(len(rows), "deals with >=90% of revenue costed")
    print("aggregate goods share", round(sum(r["goods"] for r in rows) / sum(r["revenue"] for r in rows), 3))
