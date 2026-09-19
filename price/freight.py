"""Freight per kit, from what was actually MEASURED -- never from an assumption.

MEASURED 2026-09-19 (data/freight.md, 453 rows in data/cost_freight.csv):

  One parcel per kit, 60x40x40 cm, Correios PAC balcao, SP -> capital CEP:
      BA 132,90 | PE/CE/PA 152,60 | MA/SE/RN 188,40 | MG 116,60
      = 37-52% of a R$359 kit. THE WHOLE GROSS MARGIN.
  Consolidated LTL to ONE consignee, SP -> CE (STC published table):
      ~R$54 per kit at 100 kits, R$52,57 at 5.000  = ~15%.

Dimensional weight governs absolutely: 60x40x40 cubes to 16 kg and the
calculator returned the same price at 3 kg and at 16 kg. Road LTL cubes even
harder (300 kg/m3 -> 28,8 kg per kit).

So which mode an edital allows is the most important thing the edital parser
reads: parse/entrega.py classifies the local de entrega (ONE_ADDRESS /
CALLOFF / HOUSEHOLD / UNKNOWN) and its .freight_mode is the `mode` to pass
here. Only a single-shot lot to one named seat is 'ltl'; everything else --
parcelado, addresses per ordem de fornecimento, homes, silence -- is priced
as PARCEL, the number that, if wrong, is wrong in the direction that costs a
tender rather than the direction that loses money on one.

Everything here is flagged is_estimate=True even though the parcel prices are
measurements, because they were measured to the CAPITAL CEP and the buyer is
an interior municipio. The basis string says exactly what was measured.
"""

import csv
import os

_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "cost_freight.csv",
)

# The one LTL lane with a PUBLISHED table. Everything else is UNVERIFIED.
LTL_MEASURED = {
    "CE": {"per_kit_100": 53.99, "per_kit_5000": 52.57,
           "source": "STC Transportes published table SP->Fortaleza, 300 kg/m3, "
                     "data/freight.md s.4.6, 2026-09-19"},
}

PARCEL_BOX = "60x40x40"


def _load():
    with open(_CSV, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def parcel_per_kit(uf, rows=None):
    """Worst measured PAC balcao price to this UF's capital, per parcel = per kit.

    Returns (price, days, basis) or (None, None, reason) when nothing was
    measured for that UF. 'Worst' because a single bid price must be set
    against the dearest destination it may have to serve.
    """
    rows = rows if rows is not None else _load()
    cands = [
        r for r in rows
        if r.get("carrier") == "Correios"
        and (r.get("service") or "").strip().upper() == "PAC"
        and (r.get("box_cm") or "").replace(" ", "").lower() == PARCEL_BOX
        and (r.get("dest_uf") or "").upper() == str(uf or "").upper()
        and (r.get("is_estimate") or "").upper() == "FALSE"
        and (r.get("price_brl") or "").strip()
    ]
    if not cands:
        return None, None, f"no measured PAC parcel price to {uf}"
    worst = max(cands, key=lambda r: float(r["price_brl"]))
    days = max((int(r["days"]) for r in cands if (r.get("days") or "").strip().isdigit()),
               default=None)
    basis = (f"Correios PAC balcao, 1 parcel/kit {PARCEL_BOX} cm, SP 03005-000 -> "
             f"{worst.get('dest_city')}/{uf} capital CEP, measured {worst.get('measured_at', '')[:10]}")
    return float(worst["price_brl"]), days, basis


def ltl_per_kit(uf, quantity):
    """Consolidated road freight to ONE consignee. Only SP->CE is measured."""
    lane = LTL_MEASURED.get(str(uf or "").upper())
    if not lane:
        return None, f"no published LTL table for {uf} -- UNVERIFIED"
    per_kit = lane["per_kit_5000"] if (quantity or 0) >= 5000 else lane["per_kit_100"]
    return per_kit, lane["source"]


def estimate(uf, quantity=None, mode="parcel", rows=None):
    """(per_kit, basis, is_estimate). The number bom.build() should be given.

    mode='parcel'  the conservative default until the edital's local de
                   entrega is read. Loss-making on cubed goods, and that is
                   the point: it must be SEEN, not assumed away.
    mode='ltl'     only when the edital delivers to a single municipal
                   address AND a table exists for that lane.
    """
    if mode == "ltl":
        per_kit, basis = ltl_per_kit(uf, quantity)
        if per_kit is not None:
            return per_kit, f"LTL to one consignee: {basis}", True
        # fall through to parcel rather than return zero
    price, _days, basis = parcel_per_kit(uf, rows=rows)
    if price is None:
        return None, f"UNQUOTED: {basis}", True
    return price, basis, True
