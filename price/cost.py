"""The cost table, and the two loadings that must be applied before any
cost is compared to any award price.

TRAP 10 - a retail price mistaken for a wholesale one. Every cost row must
carry the supplier's CNPJ and the date it was verified, or it is not a cost,
it is a rumour. Enforced in CostRow.__post_init__, not by convention.

TRAP 11 - interstate cost not loaded. LC 123 art. 13 §1 XIII (h) charges a
Simples optante the difference between the internal and the interstate ICMS
rate. SP internal 18% vs interstate-into-SP 12% is ~6 points. An out-of-state
supplier must beat an SP one by MORE than 6% to be cheaper. A trading name is
not an address: atacadosaopaulo.com.br is in Espirito Santo, rymo.com.br is in
Amazonas and is listed by the Sao Paulo sindicato itself. Resolve the UF from
the CNPJ, never from the name.
"""

import csv
import os
from dataclasses import dataclass, field
from datetime import date

# LC 123 art. 13 §1 XIII (h). SP internal 18% - interstate into SP 12%.
INTERSTATE_LOAD_PCT = 6.0
HOME_UF = "SP"

# The account tier is an INFERENCE, not a quote. Derived backwards from one
# observed case: Chamex published R$30,60, the state pays R$19,83 in SP, so
# winners are invoiced somewhere near R$16-18. NOBODY HAS BEEN ASKED.
ACCOUNT_TIER_DISCOUNT_PCT = 45.0
ACCOUNT_TIER_IS_INFERENCE = True


@dataclass
class CostRow:
    """One observed supplier price for one BOM line.

    cost is per BOM UNIT already -- a 3-pack divided where the BOM consumes
    one piece, NOT divided where the BOM consumes the whole kit. basis records
    which, so the decision stays auditable.
    """

    bom_line: str
    sku: str
    cost: float
    basis: str
    supplier: str
    supplier_cnpj: str
    supplier_uf: str
    product_ref: str
    url: str
    verified_at: str
    pack_size: int = 1
    listed_price: float = None
    is_inference: bool = False
    spec_risk: str = "NONE"
    notes: str = ""

    def __post_init__(self):
        # Trap 10. A cost without a traceable supplier and a date is not a cost.
        if not self.supplier_cnpj or len(str(self.supplier_cnpj).strip()) != 14:
            raise ValueError(
                f"{self.bom_line}: cost row needs a 14-digit supplier CNPJ "
                f"(got {self.supplier_cnpj!r}). A price without a supplier is "
                f"a rumour, and retail prices enter the table exactly this way."
            )
        if not self.verified_at:
            raise ValueError(
                f"{self.bom_line}: cost row needs verified_at. An undated price "
                f"cannot be known to be current."
            )
        if not self.url:
            raise ValueError(
                f"{self.bom_line}: cost row needs a primary-source URL."
            )
        if not self.supplier_uf or len(str(self.supplier_uf).strip()) != 2:
            raise ValueError(
                f"{self.bom_line}: cost row needs the supplier's real UF, "
                f"resolved from its CNPJ. A trading name is not an address."
            )

    @property
    def is_interstate(self):
        return self.supplier_uf.strip().upper() != HOME_UF

    def landed_cost(self):
        """Trap 11. The number that may be compared to an award price.

        An out-of-state supplier's price is loaded by the ICMS differential
        before any comparison, because that differential is a real cost we pay.
        """
        if self.is_interstate:
            return round(self.cost * (1 + INTERSTATE_LOAD_PCT / 100.0), 4)
        return round(self.cost, 4)

    def account_tier_cost(self):
        """Speculative. Always reported SEPARATELY from the published tier."""
        return round(self.landed_cost() * (1 - ACCOUNT_TIER_DISCOUNT_PCT / 100.0), 4)


def load_cost_table(path):
    """Read data/cost_table.csv. Unpriced lines come back as gaps, not zeros.

    Returns (rows, gaps). A gap is a BOM line we cannot cost. Callers must
    treat a gap as blocking, never as R$0,00 -- a missing line that silently
    costs nothing is how a BOM comes in flatteringly under its bar.
    """
    rows, gaps = [], []
    with open(path) as fh:
        for raw in csv.DictReader(fh):
            if not (raw.get("cost_per_bom_unit") or "").strip():
                gaps.append(
                    {
                        "bom_line": raw["bom_line"],
                        "sku": raw.get("sku") or "",
                        "reason": raw.get("notes") or "unpriced",
                        "spec_risk": raw.get("spec_risk") or "BLOCKING",
                    }
                )
                continue
            rows.append(
                CostRow(
                    bom_line=raw["bom_line"],
                    sku=raw.get("sku") or "",
                    cost=float(raw["cost_per_bom_unit"]),
                    basis=raw.get("basis") or "unit",
                    supplier=raw.get("supplier") or "",
                    supplier_cnpj=(raw.get("supplier_cnpj") or "").strip(),
                    supplier_uf=(raw.get("supplier_uf") or "").strip(),
                    product_ref=raw.get("product_ref") or "",
                    url=raw.get("url") or "",
                    verified_at=raw.get("verified_at") or "",
                    pack_size=int(raw.get("pack_size") or 1),
                    listed_price=float(raw["listed_price"]) if (raw.get("listed_price") or "").strip() else None,
                    is_inference=(raw.get("is_inference") or "").upper() == "TRUE",
                    spec_risk=raw.get("spec_risk") or "NONE",
                    notes=raw.get("notes") or "",
                )
            )
    return rows, gaps


def staleness_days(row, today=None):
    """How old a price is. A cost table nobody re-measures quietly rots."""
    try:
        seen = date.fromisoformat(row.verified_at)
    except (ValueError, TypeError):
        return None
    return ((today or date.today()) - seen).days
