"""Assemble a bill of materials and return cost WITH its confidence.

The central rule: a BOM with an unpriced line does not have a cost. It has a
floor and a gap. Returning a number that quietly omits four of seventeen lines
is how a basket comes in comfortably under its bar and takes the whole
business with it.

Freight is carried separately and always flagged an estimate. The measured
freight study in this project's record was run on PAPER -- 3,6 kg and dense.
A 24 L banheira is about 0,5 kg actual and ships on DIMENSIONAL weight, and an
assembled kit is a bag of air by design. Correios hard-caps a parcel at ~29 kg
and every B2B road carrier refuses to quote without a contract. So the number
here is a placeholder with a flag on it, not a measurement.
"""

from dataclasses import dataclass, field

from price.cost import ACCOUNT_TIER_DISCOUNT_PCT, load_cost_table


@dataclass
class BOM:
    lines: list = field(default_factory=list)
    gaps: list = field(default_factory=list)
    freight_per_kit: float = 0.0
    freight_is_estimate: bool = True
    freight_basis: str = "UNQUOTED"

    # -- costs -------------------------------------------------------------

    def published_tier_cost(self):
        """Sum of landed costs at the published price. The honest number."""
        return round(sum(line.landed_cost() for line in self.lines), 2)

    def account_tier_cost(self):
        """Speculative -- the ~45% account discount has never been quoted."""
        return round(sum(line.account_tier_cost() for line in self.lines), 2)

    def total_with_freight(self, tier="published"):
        base = (
            self.published_tier_cost()
            if tier == "published"
            else self.account_tier_cost()
        )
        return round(base + self.freight_per_kit, 2)

    # -- confidence --------------------------------------------------------

    @property
    def is_complete(self):
        return not self.gaps

    def confidence(self):
        """What this BOM may legitimately be used for.

        COMPLETE   every line priced, no spec risk -> bid on it
        RISKY      every line priced, but a line's spec may not hold
        FLOOR_ONLY unpriced lines remain -> the total is a FLOOR, never a cost
        """
        if self.gaps:
            return "FLOOR_ONLY"
        if any(line.spec_risk not in ("NONE", "") for line in self.lines):
            return "RISKY"
        return "COMPLETE"

    def blocking_reasons(self):
        out = [f"{g['bom_line']}: {g['reason']}" for g in self.gaps]
        out += [
            f"{line.bom_line}: spec risk {line.spec_risk} -- {line.notes}"
            for line in self.lines
            if line.spec_risk not in ("NONE", "")
        ]
        return out

    # -- reporting ---------------------------------------------------------

    def top_lines(self, n=5):
        """Filter 6.1: always print the rows behind the figure."""
        return sorted(self.lines, key=lambda line: -line.landed_cost())[:n]

    def summary(self):
        lines = []
        conf = self.confidence()
        total = self.published_tier_cost()
        label = "FLOOR (incomplete)" if conf == "FLOOR_ONLY" else "cost"
        lines.append(
            f"BOM {label}: R$ {total:,.2f} across {len(self.lines)} priced lines "
            f"[{conf}]"
        )
        if self.gaps:
            lines.append(
                f"  {len(self.gaps)} line(s) UNPRICED -- the real cost is HIGHER "
                f"than the figure above:"
            )
            for gap in self.gaps:
                lines.append(f"    - {gap['bom_line']}")
        lines.append(f"  top {min(5, len(self.lines))} lines by cost:")
        for line in self.top_lines():
            flag = "" if line.spec_risk in ("NONE", "") else f"  !{line.spec_risk}"
            lines.append(
                f"    R$ {line.landed_cost():7.2f}  {line.bom_line:24s}"
                f"{line.supplier_uf}{flag}"
            )
        lines.append(
            f"  account tier (INFERRED -{ACCOUNT_TIER_DISCOUNT_PCT:.0f}%, never quoted): "
            f"R$ {self.account_tier_cost():,.2f}"
        )
        lines.append(
            f"  freight: R$ {self.freight_per_kit:,.2f} per kit "
            f"[{'ESTIMATE -- ' + self.freight_basis if self.freight_is_estimate else 'quoted'}]"
        )
        return "\n".join(lines)


def build(cost_table_path, freight_per_kit=0.0, freight_is_estimate=True,
          freight_basis="UNQUOTED"):
    rows, gaps = load_cost_table(cost_table_path)
    return BOM(
        lines=rows,
        gaps=gaps,
        freight_per_kit=freight_per_kit,
        freight_is_estimate=freight_is_estimate,
        freight_basis=freight_basis,
    )
