# What this business actually is — measured, 2026-09-21

From 1.982 tenders pulled off PNCP, 1.600 surviving the scanner's own kit filter, and
220 descended to their published results. Method and its limits are in §6; read them
before quoting anything here.

---

## 1. The finding that changes the strategy

**The purchase mechanism decides the price. Not the lot size, not the state, not the year.**

| | n | Median clearing (homologado ÷ estimado) |
|---|---|---|
| **Dispensa eletrônica** | 52 | **99 %** |
| **Pregão eletrônico** | 40 | **65 %** |

Not one pregão in the sample cleared at its estimate. **Every single one discounted.**
Dispensas split: 38 % award at exactly the estimate, and the 56 % that *do* discount
still land at a median of **89 %** — well above any pregão.

It first looked like lot size, because the quartiles line up neatly (1–80 kits → 99 %,
530–18.000 kits → 65 %). That is a confound: 41 of 52 dispensas are ≤200 kits and 29 of
40 pregões are >200. Splitting by mechanism *within* each size band kills the size
effect and leaves the mechanism effect standing.

**What that is worth.** On a R$380 kit, 99 % versus 65 % of estimate is roughly
**R$130 per kit** — larger than the entire gross margin the deal model was built around.

The three big published contracts (Itaquaquecetuba 75,4 %, Mãe Gaúcha 77,4 %, Filhos de
Minas 74,1 %) are all *pregões*, and all sit in the expected band. They were never the
market this business can serve — they are the top of a market whose body is elsewhere.

---

## 2. So what is the business?

**A long tail of small direct contracts, found fast.**

| | |
|---|---|
| Median lot, ≤200 kits | **100 kits** |
| Median price per kit | **R$ 382,44** (p25 R$ 236 · p75 R$ 569) |
| Median contract revenue | **R$ 35.786** |
| Dispensas as a share of all kit tenders | **622 / 1.600 = 39 %** |

At R$382 a kit against a sourced cost near R$250 all-in, that is a **~35 % gross margin
on the lots she can actually serve** — not the 0,6 % the model showed on Friday, and not
the 16 % it showed on Saturday. Both of those were priced against pregão economics.

**The catch is the clock.** Dispensa windows run about three days. The one that got away
on 19/09 — Rio Branco do Sul, R$16.520, ~46 kits, a perfect fit for the capital — was a
dispensa published on a Monday afternoon and closed on the Thursday. A scanner that runs
four days late does not lose 4 % of the market; it loses **the whole of the part that
pays best.**

---

## 3. Who buys, where, and when

**Geography.** SP 196 · BA 170 · PR 153 · MG 134 · GO 113 · MA 100 · CE 79 · RN 72 ·
PA 71 · PE 69. Spread across every region, with no state above 13 %.

**Seasonality is real and it is budgetary, not political.** Publications by month across
the sample: Jan 43 · Feb 112 · **Mar 178 · Apr 165 · May 184 · Jun 182 · Jul 188 ·
Aug 180** · Sep 144 · Oct 91 · Nov 73 · Dec 60. March to August is roughly **three times**
December–January. A business that is not ready to bid by February has missed most of a year.

**17 % buy through a Fundo** (FMAS/FMS) rather than the prefeitura — so the buyer's CNPJ
is frequently not the prefeitura's, which the buyer screen already accounts for.

---

## 4. Who wins

**ME and EPP dominate the long tail.** Across the per-item results: ME 677 · EPP 331 ·
Demais 245. In the lote tenders: ME 15 · Demais 4 · EPP 1.

The wider contract pull (536 contracts, all suppliers resolved) puts **HHI at 181** — an
order of magnitude below the threshold for an unconcentrated market. **72,8 % of
suppliers hold exactly one contract**; only 10 of 239 operate in three or more states;
four of the ten largest contracts went to firms holding one or two contracts in total.

**There is no gatekeeper.** That is the single most favourable structural fact found.

One correction to what was said this morning: **CONDAFE, which won Itaquaquecetuba, is
not a beginner.** 47 contracts, R$5,7M, 16 states. It is an EPP by *porte*, which is a
revenue classification, not a size-of-operation one.

---

## 5. What this says to do

1. **Target dispensas.** They are 39 % of the tenders and pay 30+ points better. They are
   also where the atestado requirement is usually absent, which solves the first-sale
   problem at the same time.
2. **The scanner must run every morning.** Three-day windows make a late scan worthless
   for exactly the tenders worth most.
3. **Re-price the deal model against R$382, not R$359, and against dispensa clearing.**
   The model's conclusions were drawn from a pregão and do not transfer.
4. **Be ready by February.** The market triples in March.
5. **The R$65.492 dispensa ceiling caps revenue per contract**, not margin. Median
   contract revenue of R$35.786 already exceeds R$15.600 of capital, so supplier terms
   matter more than the model assumed — a 28-day boleto is worth more than a discount.

---

## 6. Method, and what these numbers are not

- **Discovery** was `/api/search`, full text, seven phrasings, deduplicated by
  `numero_controle_pncp`. **There is no server row cap** — an earlier reading said there
  was; 600 was this repo's own `MAX_PAGES`. But **the ordering is by relevance, not
  date**, so a partial pull is a relevance-ranked sample and **its year distribution is an
  artefact that must not be read as a trend.**
- **Full-text search over-collects.** 1.982 hits, 382 discarded by the scanner's own
  filter (308 with no kit pattern; 40 service contracts; 14 cleaning; 7 hospital). The
  1.600 that survive are the population used here.
- **Only 220 tenders were descended to results**, chosen most-recent-first among those
  PNCP flagged `tem_resultado`. **This is not a random sample**, and recency may correlate
  with things that matter.
- **Price comparisons are made within tender structure.** LOTE (the kit is one line, so
  the unit price *is* the kit price) and PER_ITEM (the kit is the sum of ~17 lines, and one
  missing line makes the kit unknown) are never pooled for a price claim. 64 SINGLE-line
  tenders are excluded from all price statistics because no kit price can be derived.
- **n is small where it is small.** 14 LOTE and 79 PER_ITEM tenders carry usable price
  pairs; the mechanism split rests on 52 dispensas and 40 pregões. The dispensa-vs-pregão
  gap is wide enough (99 % vs 65 %, with zero pregão overlap at the top) to be worth
  acting on, but it is one pull on one day.
- **The PER_ITEM maximum of R$39.000 per kit is a data artefact**, almost certainly a lot
  total recorded as a unit price. Medians are used throughout for that reason.
- **PNCP was unstable.** 2.337 calls, 2 outright failures after five attempts each; several
  pages needed four or five tries. Two search phrasings were truncated by a bug, since
  fixed, that let one dropped connection end a whole query.
