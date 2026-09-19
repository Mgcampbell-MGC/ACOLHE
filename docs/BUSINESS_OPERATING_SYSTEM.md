# ACOLHE — The Business Operating System

**What the business looks like when it is done and humming.** Written
2026-09-19. Every number carries its provenance; every gap is marked
UNVERIFIED or PENDING rather than smoothed over. Sections marked
`PENDING <agent>` are being filled from source by a parallel workstream and
must not be read as settled.

---

## 0. The business in one paragraph

ACOLHE sells newborn layette kits (17–20 specified items in one bag) to
Brazilian municipalities through public tenders. It never prospects: `Lei
14.133/2021 art. 54` obliges every contracting body in Brazil to publish what it
is about to buy, with the item list, on one free national API before it may
buy. A machine reads that feed every morning, finds the kit tenders, checks
whether the buyer actually pays its suppliers, prices the kit against a
verified wholesaler cost table, runs twelve admission rules, and writes one
row per tender into a Google Sheet: **LICITAR** with a suggested price,
**NÃO LICITAR** with the reason, or **VERIFICAR** with what is missing. The
founder reads one email, bids on the platform where the machine says to, buys
the goods only after she wins, has a co-packer assemble anything above what she
can pack herself, ships once, invoices with the empenho number on the face of
the nota fiscal, and is paid. Nothing is bought until it is sold. Nothing is
stored. Nobody is employed.

---

## 1. The loop

```
                    Lei 14.133 art. 54 obliges the buyer to publish
                                     │
   06:00  ┌──────────────────────────▼──────────────────────────┐
   daily  │  harvest PNCP ──► find kit tenders ──► window guard  │  machine
          │  ──► 12 rules ──► SICONFI buyer screen ──► price     │
          │  ──► Google Sheet row + one email                    │
          └──────────────────────────┬──────────────────────────┘
                                     │
   08:00  ┌──────────────────────────▼──────────────────────────┐
   daily  │  reads the subject line. Opens the sheet only if     │  her
          │  something says LICITAR or fecha em ≤ 5 dias.        │  ≤ 0,6 h / bid
          │  Checks the number. Bids on the platform.            │
          │  Types the result into HER columns.                  │
          └──────────────────────────┬──────────────────────────┘
                                     │ win
          ┌──────────────────────────▼──────────────────────────┐
   on win │  empenho ──► buy from SP wholesalers ──► co-packer   │  ≤ 8 h / order
          │  ──► one shipment ──► recebimento ──► NF with the    │
          │  empenho number ──► liquidação ──► paid              │
          └──────────────────────────┬──────────────────────────┘
                                     │
                          bid log grows: the only asset
                          nobody can buy, because PNCP
                          publishes who WON, never who lost
```

---

## 2. Who does what — the ledger of judgement

Ten of the twelve gates are facts, not opinions. The machine decides facts.
She decides the four things that are legally or irreducibly hers.

| The machine decides | She decides |
|---|---|
| Is it a kit tender (object text) | Accept a tender the rules flagged marginal |
| Is it live and from today (window guard) | Sign anything |
| Per-item or lote único (rule 1) | Submit the bid on the platform |
| Atestado qualitative or quantitative (rule 2) | The habilitação document pack |
| Custom model demanded (rule 3) | |
| Kit size sourceable (rule 4) | |
| Deliverable in time to that UF (rule 5) | |
| Buyer pays its suppliers (rule 6, SICONFI) | |
| ME/EPP exclusive lines present (rule 7, a flag) | |
| Every line spec-classified (rule 8) | |
| Payment deadline from the buyer's own decree (rule 9) | |
| Advance payment offered (rule 10, a flag) | |
| Bid logged (rule 11) | |
| She could carry the win: fund it and pack it (rule 12) | |
| Suggested opening price = 75% of estimate, never below cost floor | |

**A rule that cannot verify returns VERIFICAR, never PASS.** An unscreenable
buyer, an unmeasured transit day, unknown capital, an unquoted co-packer: each
surfaces as a named gap she can see, because a gap rendered as "fine" is how
this business would lose money silently.

---

## 3. Rhythms

### Daily, 06:00, the machine (≈2 minutes of network, ~93 calls)
1. Harvest yesterday's national publication, modalidades 6/7/8. Cache every
   response; a re-run costs zero calls. Report `distinct` and `served`
   separately, and `complete=False` if PNCP served fewer than it declared.
2. Find kit tenders by object text; exclude adjacent programmes (school
   uniforms, hospital linen); drop out-of-window rows and SAY so.
3. Descend into each candidate's item list — **PENDING Family B recovery.**
   Until then the scan is a floor: ~1 in 4 kit tenders describes itself
   generically and is only reachable through `/itens`.
4. Run the twelve rules. Screen the buyer. Price the basket.
5. Read HER columns back from the Sheet, then write the machine's columns.
   Never clear-and-rewrite. Keep a dated backup.
6. Send the email. **Every day, including empty days** — a missing email must
   mean the system is broken, never that the market was quiet.

### Daily, 08:00, her (≤ 0,6 h per bid, C9)
Subject line: `ACOLHE 22/09 — 3 novas · 1 fecha em 3 dias`. Open the sheet only
when a row says LICITAR or a deadline is near. Bid. Record.

### Weekly, the machine
- Re-harvest the wholesaler catalogues (VTEX / Shopify / WooCommerce public
  APIs). Every cost row carries `verified_at`; **the system must refuse to bid
  on a cost older than the freshness limit rather than quietly using it.**
- Re-check certidão validity against `config/documentos.yaml` — **PENDING
  habilitação agent** for the validity periods. The shortest one sets the
  renewal cadence of the whole company.
- Export the bid log to CSV and copy `acolhe.sqlite` off-box.

### On every win (≤ 8 h per order, C9)
**PENDING order-to-cash agent** for the day-by-day timeline from the seven
real editais. Known already: nothing ships before the nota de empenho exists;
the empenho number goes on the face of the NF or the payment clock restarts;
the IN RFB 1.234 Anexo IV declaration is filed per contract or 1,2% is
withheld with no RFB refund path.

---

## 4. The four constraints, and which one binds

Capital is a dial, not a fixed number (`config/capital.yaml`,
`available_brl: null` until the founder sets it).

```
lots_per_year = (capital ÷ COGS_per_lot) × (365 ÷ float_days)
```

**Float days is the lever.** No supplier terms → pay ~day 11, paid ~day 45,
float ≈ 34. With 28-day terms → float ≈ 6. That is a ~5× collapse in cycle
length, after which capital stops binding and something else does:

| Constraint | Binds when | Current state |
|---|---|---|
| Capital | float is long (no supplier terms) | dial unset |
| Win count | she can fund more lots than she wins | **almost certainly binding early** |
| Her time | 87 h/month; ≤0,6 h/bid; ≤8 h/order | budget, not yet measured |
| Physical fulfilment | lot > ~240 kits without a co-packer | **rule 12 enforces** |

**Supplier credit terms are worth more than doubling her capital and cost
nothing.** Brascol is the only wholesaler found with a published route to
deferred payment, gated on CNAE rather than time in business — terms in month
two, not month thirteen. Its prices are behind a login. One free registration.

### The lot-size ceiling
Lot sizes in this market span two orders of magnitude. Median edital ≈108 kits
≈ R$19k COGS. Itaquaquecetuba = 5.000 kits ≈ R$880k COGS and 83+ hours of
packing. **Rule 12 refuses lots above the fulfilment ceiling or beyond
available capital**, because winning one she cannot carry is a default, a
penalty and possibly a bidding suspension — worse than not bidding.

---

## 5. The numbers, with provenance

| Figure | Value | Source | Status |
|---|---|---|---|
| BOM, 16 of 17 lines | **R$ 176,32** | `data/cost_table.csv`, observed catalogue prices, supplier CNPJ + UF on every row | FLOOR — `kit_enxoval` unpriced; assembly and freight not included |
| Observed clearing price, 17-item kit | R$ 359,05 | PNCP Family A: homologado 1.795.250 ÷ 5.000 | quantity 5.000 UNVERIFIED (Family A carries none) |
| Gross at that price | ~51% | computed | a CEILING, because the BOM is a floor |
| Net of Simples Anexo I at RBT12 ≤ 180k | ~47% | 4,00% | PENDING company-setup agent to reconfirm the 2026 table |
| Kit tenders per working day | 5 (2026-09-15, one measured day) | `harvest/daily.py` live run | title-only, so a floor; handoff's ~4,0 reproduces |
| National tenders per day, mod. 6/7/8 | 4.595 | PNCP Family A | measured |
| Daily harvest cost | ~93 calls, ~2 min | measured | handoff's "~5.560 calls" was wrong by ~60× |
| PNCP rate limit | 429 after ~30 burst, ~30 s, no Retry-After, shared across families by source IP | measured, 62 hits on a national sweep | the real daily constraint |
| Small municípios screenable via SICONFI | **45%** (n=60, ±12,6 pp) of the 74,5% of municípios under 25k pop. | measured | rule 6 returns UNSCREENABLE for roughly half of real targets |
| Editais with a quantitative atestado | 1 of 12 | 7 retrieved + handoff's 5 | the feared barrier is largely illusory |
| Textile lines vs handoff | −44,8% on 5 comparable lines | re-measured | handoff had pack prices as unit prices |
| Mochila | R$ 52,27 vs R$ 25,00 target | measured | the one line that went the wrong way; 30% of BOM |
| Freight per kit | — | — | **UNQUOTED. PENDING freight agent.** Ships on dimensional weight |
| Assembly per kit | — | — | **UNQUOTED. PENDING co-packer agent.** Never costed by anyone |

---

## 6. The files — where everything lives, who owns what

```
config/
  skus.yaml          24 SKUs: match, anti-patterns, plausible price window,
                     spec dimensions that must agree before two rows share a median
  rules.yaml         thresholds for the 12 rules — never in code
  capital.yaml       capital DIAL, float days, self-pack ceiling, co-packer lead
  ufs.yaml           target UFs by priority; transit_days null until measured
  documentos.yaml    PENDING — validity days per certidão, for the expiry tracker
  order_to_cash.yaml PENDING — the stages after a win, machine-readable
  cnaes.yaml         PENDING — CNAEs to register, Simples admissibility
harvest/
  pncp_client.py     both API families, backoff, disk cache, resumable cursor,
                     ROUTE_MIXED detection, distinct ≠ served
  daily.py           the national scanner + the window guard
parse/
  normalise.py       THE FIVE FILTERS. Nothing bypasses it.
  spec.py            SKU classification with spec control (Filter 4)
price/
  cost.py            a cost row REQUIRES supplier CNPJ, UF, URL, date;
                     non-SP loaded +6 pts (LC 123 art. 13 §1 XIII h)
  bom.py             COST vs FLOOR; assembly line; a gap is never R$0
  margin.py          net of Simples; 75% anchor; NO BID when the floor is unknown
screen/
  rules.py           the 12 rules, pure functions, (passed, reason, evidence)
  buyer.py           SICONFI: PASS / REJECT / UNSCREENABLE; zero rows omitted
                     by SICONFI are derived from the published identity
log/
  bidlog.py          append-only; corrections supersede; no UPDATE, no DELETE
report/
  digest.py          the workbook. HOJE / PIPELINE / MINHAS APOSTAS / SAÚDE.
                     Portuguese. Her columns read back and never overwritten.
data/
  cost_table.csv     17 lines, provenance on every one
  editais/           7 real editais, verbatim clause classification
  siconfi_screenability.md, copacking.md (PENDING), freight.md (PENDING)
docs/
  LEGAL_FINDINGS.md  six statutory questions, primary sources, confidence labels
  HABILITACAO.md, ORDER_TO_CASH.md, COMPANY_SETUP.md, RISK_REGISTER.md  PENDING
tests/               272 tests. One per known measurement error, and growing.
```

**Ownership rule for the Sheet:** the machine writes HOJE, PIPELINE and SAÚDE;
she writes the yellow columns of MINHAS APOSTAS; the machine reads those back
before every write and never invents, edits or deletes a value she typed.
SQLite is the truth; the Sheet is a view; a weekly `.xlsx` goes off-box.

---

## 7. The legal position that shapes pricing (settled, from primary sources)

- **Do not embed DIFAL.** STF Plenário ADI 5469 struck cláusula nona of
  Convênio 93/2015 for Simples senders; LC 190/2022 did not revive it;
  SEFAZ-SP RC 26939/2022 and RC 32028/2025 confirm. A competitor who embeds it
  is several points dearer for nothing.
- **ICMS-ST on perfumaria/higiene in SP ended 1 April 2026** (Portaria SRE
  94/2025). A wholesaler still pricing an ST load is using a regime that no
  longer exists — renegotiation leverage. Counterweight: ICMS returns inside
  the DAS on resale; effective Anexo I rate on that revenue rises. Recalculate,
  do not presume.
- **IRRF is 1,2%, not 1,5%.** Anexo IV filed per contract, 2 vias, at
  signature. The withheld amount belongs to the município (CF art. 158 I) and
  the RFB has no refund mechanism — the declaration is cheap insurance.
- **LC 123 art. 48 I is per item and mandatory.** Lines ≤ R$80.000 marked
  "Sem benefício" are an impugnação ground: art. 164, 3 working days before
  opening, no cost. Attack the *absence of justification*, not the flag.
- **Empate ficto works against us.** Selling from SP into MG/BA/PE, we are the
  outsider; a local ME within 10% gets the last look at our price.
- **SUAS fundo-a-fundo transfers are probably NOT transferências voluntárias**
  (INFERÊNCIA, unsettled): do not model the fast federal clock for SUAS buyers.

---

## 8. What is still UNVERIFIED — the honest list

| Gap | Why it matters | What settles it |
|---|---|---|
| `kit_enxoval` line | last unpriced BOM line | the real edital text — PNCP Family B |
| Freight per kit | largest unmeasured cost; dimensional weight | PENDING freight agent (Correios public calculator) |
| Assembly per kit | never costed by anyone | PENDING co-packer agent; then one quote |
| Co-packer lead time | feeds rule 5; can make short-notice tenders undeliverable | same |
| Whether a co-packer ships on its own carrier contracts | would solve the freight problem entirely | same |
| Transit days per UF | rule 5 returns UNVERIFIABLE until set | PENDING freight agent |
| Capital available | rule 12 cannot verify funding until set | **the founder sets the dial** |
| Account-tier discount (~45%) | decides whether the whole basket is live | 15 supplier emails, never sent |
| Body 3-packs "RN AO G" | size-graded or three RN? | the real edital wording |
| Banheira band | R$18,90 / 23,65 / 29,71 on one word | the real edital wording |
| Certidão validity periods | the renewal cadence of the company | PENDING habilitação agent |
| Order-to-cash day count | the handoff's ~45 days is an assumption | PENDING order-to-cash agent |
| Company setup costs | inherited figures unverified | PENDING company-setup agent |
| Family B availability | the reading rail; 503 on every attempt all day | **Monday 08:00 BRT scheduled re-check** |

---

## 9. What "humming" looks like

It is a Tuesday in March. The cron ran at 06:00 and the email arrived at
06:03: `ACOLHE 10/03 — 4 novas · 1 fecha em 4 dias · sistema OK`. She reads
it on her phone. One row says LICITAR: Icatu/MA — no, Icatu is REJECTED, it
paid 0,0% of last year's invoices. The LICITAR row is Maracás/BA, 180 kits,
suggested R$ 298,00, cost floor R$ 189,40 including a quoted co-packer and
Correios contract freight, buyer paid 91% of prior-year invoices, atestado
qualitative, 12 days to deliver against 9 needed. She opens the platform,
enters R$ 298,00, and types LICITEI · 298,00 into her column. Twelve minutes.

Two rows say VERIFICAR: one buyer is under 25.000 people and SICONFI has
nothing on it; one tender's transit to Roraima has never been measured. She
skips both. Nothing was hidden from her and nothing was decided for her.

Three weeks later the empenho arrives. The system opens a won-order card:
supplier, SKU, quantity, cost, the co-packer's address, the empenho number
already formatted for the NF. She sends the POs. The co-packer ships. The
termo de recebimento is signed on day 6. The NF goes out with the empenho
number on its face on day 7. Payment lands on day 34 — the ata said 30 dias
após a liquidação and this município liquidates fast; the system learns that
and will weight Maracás higher next time.

The bid log has 41 rows. Win rate is 7 of 31 decided — 22,6%, and the system
only started reporting it at row 10. She lost four to a local bidder's last
look and the system now flags empate-ficto exposure in the Northeast. The
cost table was refreshed on Sunday; two prices moved. Every certidão is green
for at least 40 days. Capital is set at R$ 30.000 and nothing has bound on it
since Brascol granted 28 days in November.

She has spent 61 hours this month. She has never phoned anyone.

---

## 10. What could stop it

**PENDING risk-register agent** for the ranked list. Known already, in order
of how cheaply each is prevented:

1. Family B never returns → the machine finds but cannot read. *Decision.*
2. Freight comes in at 15% of revenue rather than 2% → the margin halves.
   *One measurement.*
3. A stale cost is used because nothing checks `verified_at` against today.
   *Code, one afternoon.*
4. A certidão lapses and a won tender is lost at habilitação. *Expiry
   tracker, once `documentos.yaml` exists.*
5. The cron dies silently. *The daily heartbeat email, already designed.*
6. She wins something above the fulfilment ceiling. *Rule 12, shipped today.*
