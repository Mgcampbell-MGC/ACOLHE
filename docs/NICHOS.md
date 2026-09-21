# The three adjacent niches, measured against the kit

**2026-09-21.** Same rail, same method: search PNCP, keep what a keyword filter admits,
descend 90 tenders each into their published results, compute clearing ratio by mechanism
and supplier concentration. 3.162 API calls, 3 failures.

---

## 1. What the screen said, and why it was wrong

A first-pass screen scored 20 verticals on mechanism, value density, assembly burden and
licence barriers. **It ranked the kit 10th of 18** and put medalhas, informática and
expediente at the top.

**It never looked at contract size.** That turns out to be the variable that decides.

---

## 2. Measured

| | Kit natalidade | Medalhas | Camisetas | Expediente |
|---|---|---|---|---|
| Tenders found | 2.044 | 2.039 | 1.028 | 1.566 |
| **Dispensas** | 711 (35%) | **1.519 (74%)** | 655 (64%) | 1.012 (65%) |
| Dispensa clearing, median | 99% | **100%** | 100% | 97% |
| …share landing at exactly 100% | 38% | **59%** | 50% | 32% |
| Pregão clearing, median | 65% | 58% | **49%** | 75% |
| **HHI** | **181** | 219 | 379 | 232 |
| Suppliers with one contract | **73%** | 41% | 45% | 31% |
| **Median dispensa contract** | **R$ 30.848** | R$ 5.588 | R$ 8.450 | R$ 3.570 |

**Medalhas beats the kit on every mechanism measure.** Twice the dispensa share, a median
clearing of exactly 100%, and 59% of contracts awarded at the estimate without a discount.
Its pool of dispensas — 1.519 — is more than double the kit's.

**And the kit's contracts are five and a half times bigger.**

---

## 3. What it takes to earn the same money

At the kit's measured ~30% net margin, to clear **R$144.000 a year**:

| Niche | Profit/contract | Wins needed | Hours/year | % of its dispensa pool | **Profit per hour** |
|---|---|---|---|---|---|
| **Kit natalidade** | R$ 9.254 | **16** | 124 | 2,2% | **R$ 1.157** |
| Medalhas | R$ 1.676 | 86 | 172 | 5,7% | R$ 838 |
| Camisetas | R$ 2.535 | 57 | 227 | 8,7% | R$ 634 |
| Expediente | R$ 1.071 | 134 | 269 | 13,3% | R$ 536 |

**The kit wins on profit per hour, and it is not close.** Sixteen wins a year against
eighty-six is the difference between a side business and a full-time one.

It also wins on *reachability*: 16 wins is **2,2% of its dispensa pool**; medalhas needs
**5,7%** and expediente **13,3%**. The niches with more tenders need a much higher hit rate,
not a lower one, because each win is worth so much less.

---

## 4. What this comparison assumes, and what it does not know

Stated plainly because the conclusion depends on it:

- **The 30% net margin is measured only for the kit.** Applying it to the others is an
  assumption. Medalhas could be far richer — a medal costing R$3 and clearing at R$18 is
  entirely plausible, and nobody has priced one.
- **Hours per order are assumed**, not measured: 8h for the kit (17 items into a bag), 4h for
  camisetas, 2h for the single-SKU niches. **If a medalhas order really takes 2 hours and its
  margin is better than 30%, the profit-per-hour gap closes or reverses.** That is the single
  measurement that would change this table.
- Clearing ratios here are **per line**, not per kit. Comparable within the dispensa/pregão
  split, not directly against the kit's per-kit figures in `O_MERCADO.md`.
- 90 descents per niche, most-recent-first — **not a random sample**.
- The keyword filters are cruder than the kit's five-filter pipeline, so some over-collection
  survives.

---

## 5. The verdict

**Stay with the kit.** Not because it is the easiest market — it is the most concentrated
work per order and the only one needing assembly — but because **each win is worth five times
more and needs a third of the hit rate.**

**Keep medalhas as the named fallback.** It is genuinely the better *market*: 74% dispensa,
100% clearing, 1.519 opportunities a year, no assembly, trivial freight, no licence, HHI 219.
If the kit market contracts — and §9 of the operating system lists real reasons it might, from
a shift to cash benefits to state programmes buying centrally — medalhas is where the same
machine points next. **The scanner, the rules, the buyer screen and the bid log are
product-agnostic.** Only `config/skus.yaml` and the cost table would change.

**One caution about camisetas:** HHI 379 and a single supplier holding 85 of 550 winning
lines. That is the most concentrated of the four and the only one showing a dominant
incumbent.
