# ACOLHE — the business operating system

**Rewritten 2026-09-21**, after PNCP's item feed came back and the market was measured
rather than assumed. Every number carries its provenance. Where something is unknown it
says so; where an earlier version of this document was wrong, §11 says what and why.

---

## 0. The business in one paragraph

One person in São Paulo sells newborn layette kits (*kit natalidade / enxoval*) to Brazilian
municipalities through public procurement. She never phones a buyer, never holds a buyer's
credentials, and has no employees or contractors — only suppliers. A system reads every kit
tender published in Brazil each morning, discards the ones that cannot be won or cannot be
served, prices the rest against a sourced bill of materials, and tells her which to bid. She
buys only after she wins, assembles or has assembled, and ships. **The edge is not sourcing,
packing or shipping — anyone can do those. The edge is knowing which tender to touch.**

---

## 1. The market, measured

From 4.333 PNCP records pulled on 2026-09-21, 2.044 surviving the scanner's own kit filter.
**These are floors, not a census** — see §10.

| | |
|---|---|
| Kit tenders in the last 12 months | **786** |
| …of which **dispensa eletrônica** | **272** |
| …of which pregão eletrônico | 502 |
| Distinct municipalities buying, 12 months | **648** |
| Distinct municipalities, all years | **1.272** |
| Municipalities in Brazil | 5.571 → **~23% have bought** |

**Geography:** SP 91 · MG 90 · BA 74 · PR 67 · GO 45 · MA 42 · PA 37 · PE 36. No state above
12%. This is a national market served electronically, not a local one.

**Seasonality is budgetary, not political.** By month: Jan 30 · Feb 45 · **Mar 87 · Jun 88** ·
Jul 76 · Sep 76 · Oct 71 · Dec 50. March through September runs ~2× January–February.
A 2026 check found election-year publication volume flat, so the driver is the budget cycle.

**Concentration: there is no gatekeeper.** Across 536 contracts with every supplier resolved:
**HHI 181** — an order of magnitude below the threshold for an unconcentrated market.
**72,8% of suppliers hold exactly one contract.** Only 10 of 239 operate in three or more
states. Four of the ten largest contracts went to firms holding one or two contracts in total.

---

## 2. The strategy, and the single finding it rests on

**The purchase mechanism decides the price. Not the product, the state, the size or the year.**

| | n | Median clearing (homologado ÷ estimado) | Median price/kit |
|---|---|---|---|
| **Dispensa eletrônica** | 52 | **99 %** | R$ 342,05 |
| Pregão eletrônico | 40 | **65 %** | R$ 382,44 |

**Not one pregão in the sample cleared at its estimate.** Every single one discounted.
Dispensas split: 38% award at exactly the estimate; the 56% that do discount still land at a
median of **89%** — above every pregão.

Checked for the obvious artefact: if dispensas merely recorded the accepted price as the
estimate, all would sit at exactly 1,0. They do not. And it is not a lot-size effect in
disguise — splitting by mechanism *within* size bands kills the size effect and leaves the
mechanism effect standing.

**On a R$380 kit, 99% versus 65% is about R$130 per kit — larger than the entire gross margin
the business was originally modelled on.**

> **The strategy is therefore: bid dispensas.** They are 35% of the tenders and pay ~34 points
> better. They are also where the *atestado* requirement is usually absent, which solves the
> first-sale problem at the same time. Pregões are a fallback, not the plan.

**The cost of that strategy is speed.** Dispensa windows run about three days. On 2026-09-19
the system found Rio Branco do Sul/PR — R$16.520, ~46 kits, an exact fit for the capital —
four days after publication, one day after it closed. **A scanner that runs late does not lose
a slice of the market; it loses the part that pays best.**

---

## 3. Unit economics

Sourced cost R$198,78 for 16 of 17 BOM lines (`data/cost_table.csv`, observed SP wholesale
catalogue prices, supplier CNPJ and URL on every row), plus measured freight.

| At the median dispensa | |
|---|---|
| Price per kit | R$ 382,44 |
| Goods + LTL freight | R$ 252,77 |
| **Gross / Net margin** | **33,9 % / 29,7 %** |

**Freight remains the assassin.** The same kit with parcel freight to the Northeast
(R$152,60/kit, measured) nets **4,1%** — nothing. One parcel per kit to Maranhão is R$188,40.
The delivery clause decides whether a tender is biddable at all, which is why
`parse/entrega.py` exists.

**Selection is most of the business.** Price per kit runs p25 **R$236** · median **R$382** ·
p75 **R$569**. A p25 kit loses money at our costs. A p75 kit nets over R$11.000/month on its
own. Bidding the right ones matters more than sourcing better.

---

## 4. Scale — the target is one a week

Capital is not the constraint people assume. The formula is:

```
lots/year = (capital ÷ cash per lot) × (365 ÷ float days)
```

With R$15.600 and a 45-day cash cycle that is 8,2 lots a year. **The binding term is the
float, not the capital.**

| Wins/month | Capital @45d | Revenue/yr | Simples | Net/month | Hours/month |
|---|---|---|---|---|---|
| 1 | R$22.812 | R$280k | 5,2% | R$6.202 | 8 |
| **2** | R$45.623 | R$560k | 7,0% | **R$12.042** | 16 |
| 4 | R$91.247 | R$1,12M | 8,7% | R$23.030 | 32 |
| **4,3 — one a week** | **R$98.850** | **R$1,21M** | 8,8% | **R$24.834** | **35** |
| one a week @171 kits | R$277.105 | R$3,40M | 11,7% | R$62.336 | 35 |

**Borrowed capital is cheap against this margin.** At 4%/month — expensive Brazilian working
capital — one a week still nets **R$19.883**/month at 61 kits and **R$48.457** at 171.
Supplier terms are the free version of the same lever: a 28-day boleto cuts the float from 45
days to 6 and drops the capital requirement for one-a-week to **R$13.180**.

**The constraint moves to win rate.** 52 wins against ~272 dispensas a year is ~19%. Nobody
knows the real rate, and **the only way to learn it is to bid** — which is why the bid log is
the most valuable asset in the system.

**Ramp planned for year one:** Q1 1 win · Q2 3 · Q3 5 · Q4 6 = **15 wins, ~R$93k net**.
Then 2–4/month. Build for one a week; let the rate find its level.

---

## 5. The kit itself

Read from Itaquaquecetuba's own edital (PE 90088/2025, 5.000 kits, cleared R$359,05 to an EPP).
**The buyer published a per-line price table that sums to exactly R$476,05** — verified to the
centavo against the PNCP estimate. It is the best cost benchmark in the project.

**Fifteen of our sixteen sourced lines sit under what the winner realised on them.** Two do not:

- **`oleo_infantil` is the only line we lose on** — R$23,89 sourced against R$17,93 realised.
  A sourcing failure on one line; the cheapest thing in the business to fix.
- **`shampoo_infantil` has R$0,80 of slack** — effectively none.

**The branded-kit problem.** That tender requires the backpack to carry **four silk-screen
elements** (three different institutional artworks plus a satin label bearing the supplier's
own CNPJ) and the bathtub to ship with **CMYK vinyl already applied on three faces**, warranted
12 months against peeling. Measured vinyl printing is only R$2,20–2,78/kit — **printing is not
what is expensive.** What is: no printer found will print a bag you supply (every one is a
factory that prints only bags it makes), so the R$52,27 plain-bag row is not a base to add to.
The edital values that line at **R$98,51**. Carry that until a factory quotes. A branded kit
drops net margin from ~30% to ~18%.

Lead time is a live risk: one bag supplier publishes **20 working days**, against a 20
*calendar* day delivery deadline. **The printed bag is the long pole**, not the goods.

---

## 6. The loop

**Every morning** — harvest yesterday's publications, find kit tenders by object text, drop
anything outside its window, descend into item lists, run the thirteen admission rules, screen
the buyer's payment record at SICONFI, price against the BOM and measured freight, write the
workbook. **This must run daily**: three-day windows make a late scan worthless.

**Per bid, ≤0,6 h.** Open the workbook only when a row says LICITAR. Bid. Record.

**Per win, ≤8 h.** Buy from SP wholesalers, assemble (≤240 kits) or co-pack, ship, invoice with
the empenho number in the NF-e, chase the atesto.

**Every 25 days** — reissue the certidões. The CRF/FGTS is valid 30 days and reissuable only
from the 5th day before expiry; it sets the cadence of the whole company.

---

## 7. What exists

370+ tests. `harvest/` (both PNCP families, plus `/api/search` as a second discovery rail
after Family A went down) · `parse/` (five filters, SKU classification, delivery-clause
reader) · `screen/` (thirteen rules, SICONFI buyer screen, certidão tracker) · `price/` (cost
table with freshness, BOM floor, measured freight, margin) · `report/` (the Portuguese
workbook) · `log/` (append-only bid log) · `tools/` (market harvest, analysis, niche screen).

Documents: `O_MERCADO.md` (the measurement) · `ITAQUAQUECETUBA_REAL.md` (the real kit) ·
`HABILITACAO.md` · `ORDER_TO_CASH.md` · `COMPANY_SETUP.md` · `LEGAL_FINDINGS.md` ·
`RISK_REGISTER.md` · `SUA_LISTA.md` (what the founder decides).

---

## 8. Setup, and what it costs

One-time **R$219–1.013**; monthly R$196–473; 10–15 business days to a CNPJ. The only
*mandatory* spend to be able to bid is the **e-CNPJ A1 at R$203–275**. Every certidão is free,
SICAF is free, Compras.gov.br is free to bid on, BLL charges only on a win.

**One unforgiving deadline: Simples opt-in within 60 days of the CNPJ**, or Lucro Presumido
until January.

**The first atestado.** Six of seven editais demand one — and Itaquaquecetuba, the largest
buyer in the corpus, accepts one from a *"pessoa jurídica de direito público **ou privado**"*.
One private sale plus a signed declaration clears it. Dispensas usually do not ask at all.

---

## 9. What could kill it

1. **A late scan.** Three-day windows. The failure mode is silence, not error.
2. **Parcel delivery.** Household or per-address delivery makes a tender unbiddable. Read the
   clause before pricing.
3. **Bidding p25 kits.** Loses money at our costs. Selection is the business.
4. **An SRP call-off she cannot serve** — art. 83, 20% fine. Rule 13 refuses those.
5. **No federal money underwrites this market.** The FNAS states plainly that benefícios
   eventuais are funded by municipal treasury and state co-financing, *"sendo vedado o uso dos
   recursos federais."* Every kit is own-revenue, re-voted annually.
6. **A possible shift toward cash benefits.** Research reports CNAS Resolução 213/2025 making
   benefits *"preferencialmente em pecúnia"*, with municipal councils required to rewrite their
   rules by 28 October 2026. **NOT independently verified** — the DOU original was never
   obtained. Probable, not settled, and worth settling before money is spent.
7. **State programmes.** Maranhão Acolhe, Mãe Gaúcha, Nascer Bem and others buy centrally.
   Every municipality a state supplies is one that stops tendering.
8. **Births are falling** ~3%/yr (−15,5% 2019→2024).

---

## 10. What these numbers are not

- **Discovery is full-text and relevance-ordered**, not date-ordered. A partial pull is a
  sample and **its year distribution is an artefact that must not be read as a trend**. There
  is no server row cap — an earlier reading said there was; that 600 was this repo's own
  `MAX_PAGES`.
- **Only 220 tenders were descended to results**, most-recent-first. **Not a random sample.**
- **n is small where it is small**: 52 dispensas and 40 pregões carry the central finding. The
  gap (99% vs 65%, zero pregão overlap at the top) is wide enough to act on. It is one pull.
- **Price claims are never pooled across tender structures.** LOTE (the kit is one line) and
  PER-ITEM (the kit is the sum of ~17 lines) are kept apart; 64 single-line tenders are
  excluded from all price statistics.
- **Still unmeasured, and it matters:** whether dispensas *pay* faster than pregões. The
  45-day float is carried over from seven pregão editais. If dispensas pay in 20 days the base
  case more than doubles. This is the cheapest open question in the business.
- **Also unmeasured:** the real win rate; whether the 38% of dispensas clearing at exactly
  100% are uncontested or pre-arranged; the co-packer price; the account-tier discount.

---

## 11. Where earlier versions of this document were wrong

Recorded because the corrections were expensive and the pattern is instructive — **every one
came from generalising a number across cases that were not comparable.**

1. **"A second supplier will be cheaper."** The benchmark came back: Paulimar, an atacadista
   carrying the same manufacturer references, is **dearer than Emilio on every comparable
   line**. Emilio is at or near the market floor. Diversifying is a cost of resilience, not a
   saving.
2. **"Bid 90% of estimate; the 75% anchor is the problem."** Wrong for a *lote*.
   Itaquaquecetuba cleared at 75,4%, Mãe Gaúcha 77,4%, Filhos de Minas 74,1% — all pregões,
   all clustered. The 97–100% figure came from the original plan and describes per-item
   tenders, which behave differently.
3. **"A company your size won it."** CONDAFE is an EPP by *porte* — a revenue classification —
   but holds 47 contracts across 16 states. Not a beginner.
4. **"240–450 dispensas a year."** That came from a shallow pull and counted only dispensas
   while being presented as the market. The measured 12-month figure is **786 kit tenders,
   272 of them dispensas**, and still a floor.
5. **"PNCP caps search at 600 rows."** It does not. That was this repo's own page limit.
