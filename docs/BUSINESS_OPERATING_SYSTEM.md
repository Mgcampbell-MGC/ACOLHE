# ACOLHE — The Business Operating System

**What the business looks like when it is done and humming.** Written
2026-09-19. Every number carries its provenance; every gap is marked
UNVERIFIED or PENDING rather than smoothed over. The one remaining PENDING
is PNCP Family B (the item-reading rail), re-checked Monday 2026-09-21.

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
4. Run the thirteen rules. Screen the buyer. Price the basket.
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
- Run the certidão tracker (`screen/documentos.py` over
  `config/documentos.yaml`, 16 documents, 5 platforms — `docs/HABILITACAO.md`).
  The shortest validity in the pack is **30 days: the CRF/FGTS** (Manual
  CAIXA v19 item 2.7.1), and CAIXA only reissues from the 5th day before
  expiry, so **the company runs on a 25-day cadence**; the 180-day certidões
  (CNDT, SEFAZ-SP, PMSP, RFB/PGFN) ride a semester cycle with 30 days of
  slack. An expired or never-recorded bid document blocks admission;
  a period the issuer never fixed (cartão CNPJ, JUCESP, TJSP falência,
  PGE-SP e-CRDA) is green on a fallback **and flagged UNVERIFIED** — the
  printed *válida até* on the issued document always wins. Lei 14.133
  art. 63 III demands the pack only from the winner after julgamento and
  art. 64 II lets her refresh one that lapsed after the proposal date: the
  real kill is a certidão already dead **on proposal day**, or a
  state/municipal/falência upload that expired inside SICAF (IN 3/2018
  art. 18 §2 — those are not auto-refreshed; RFB/PGFN, FGTS and CNDT are).
- Export the bid log to CSV and copy `acolhe.sqlite` off-box.

### On every win (≤ 8 h per order, C9)
From `docs/ORDER_TO_CASH.md`, built from Lei 14.133 arts. 82–95 and 137–145,
Lei 4.320, Decreto 11.462/2023, MCASP and the seven editais' own clauses
(machine-readable in `config/order_to_cash.yaml`, 12 stages S1–S12):

- **Count from the nota de empenho, not from homologação.** Empenho → cash is
  **≈34 days best** (Bom Sucesso do Sul: ME/EPP term 20 dias corridos),
  **≈40–55 typical** (five editais say "30 days", each from a *different*
  event: atesto, NF presentation, entrega+NF, or "até o 10º dia do mês
  subsequente"), **≈69 worst bounded** (Bocaiúva). Homologação → empenho adds
  5–35 days for ARP signature/publication **plus an unbounded wait for the
  first call-off under SRP.** The handoff's "~45 days" is a best-case
  single-order floor, not a projection.
- **She cannot freely decline an SRP call-off.** Art. 83 makes the registered
  price a *compromisso de fornecimento*; refusing the empenho is
  descumprimento total (art. 90 §5); Decreto 11.462 art. 28 II cancels her
  registration, mirrored verbatim in four editais; fines of 20% of total value
  (Bom Sucesso 27.1, Bocaiúva 15.1). Lawful exits are narrow and in writing
  *before* the empenho.
- **"Buy after the empenho" is infeasible where delivery is 5 days or
  "imediato"** (Belterra, Bom Sucesso, Irecê): she must hold stock or eat
  late fines (5% on day 1; 2%/day). This is a direct tension with the
  made-to-order model and must be a rule, not a surprise.
- **The empenho number goes in the NF-e XML** — MOC 7.0 Anexo I group ZB,
  field `ZB02 xNEmp` — *and* in `infCpl` for the servidor doing the atesto.
  A defective NF restarts the clock from resubmission in **6 of 7** editais.
- **Recebimento definitivo has no deadline in 5 of 7** (art. 140 §3 delegates
  it); most payment terms only start there. Two of the three most common
  stalls are outside her control; the third — the five certidões at ARP
  signature, every empenho and every payment — is entirely hers.
- IN RFB 1.234 Anexo IV filed per contract, or 1,2% is withheld with no RFB
  refund path.

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
| Gross at that price, goods only | ~45% | computed on R$198,78 | a CEILING, because the BOM is a floor — and **before freight and assembly** |
| **Freight per kit, SP → Northeast capital, one parcel per kit** | **R$ 132,90 – 188,40 = 37–52% of the kit price** | Correios PAC balcão, public calculator, 60×40×40 cm, 2026-09-19 (`data/freight.md`, 453 measured rows) | **MEASURED. This is the whole gross margin.** MA/SE/RN +23% vs PE/CE/PA; BA −13% |
| Freight per kit, consolidated LTL to one municipal address | **~R$ 54 (15%)** at 100 kits; R$ 52,57 at 5.000 | STC Transportes published table, SP→CE only, 300 kg/m³ cubed | other states UNVERIFIED; **the delivery-address clause of each edital decides which mode applies** |
| Gross after LTL freight, before assembly | **~36%** | computed | the honest working figure; per-parcel delivery is **loss-making** |
| Dimensional weight | 60×40×40 = 16 kg cubic, price identical at 3 kg and 16 kg | Correios rule: max(physical, C×L×A/6.000) | only cubic centimetres move the price; split packing saves ~20% |
| Correios contract, new CNPJ, no volume | exists (Clube Correios / Platinum, e-CNPJ only, no minimum) | Termo de Condições Comerciais 09/09/2026 | but PAC/SEDEX carry **no price reducers** on those packages; first discounted tier needs R$100k/month |
| Net of Simples Anexo I at RBT12 ≤ 180k | ~47% | 4,00%, recomputed against the LC 155/2016 table | confirmed; LC 227/2026 takes effect only 01/01/2027 (art. 182 I b), so 2026 is unchanged |
| One-time cost, nothing → bid-ready | **R$ 219 – R$ 1.013** (≈US$42–196) | `docs/COMPANY_SETUP.md`: JUCESP 218,99 · e-CNPJ A1 203–275 · contador month 1 · one portal credit | far inside the US$500 floor of C5 |
| Fixed monthly cost | **R$ 196 – R$ 473** | contador 136–225 · TFE ~30 · VPS 30 · portal 0–165 | DAS variable at 4,00% |
| Days to bid-ready | **10–15 business days** realistic | SP time-to-CNPJ 1 day 10 h (Mapa de Empresas) | 30+ if JUCESP/SEFAZ raise an exigência |
| Kit tenders per working day | 5 (2026-09-15, one measured day) | `harvest/daily.py` live run | title-only, so a floor; handoff's ~4,0 reproduces |
| National tenders per day, mod. 6/7/8 | 4.595 | PNCP Family A | measured |
| Daily harvest cost | ~93 calls, ~2 min | measured | handoff's "~5.560 calls" was wrong by ~60× |
| PNCP rate limit | 429 after ~30 burst, ~30 s, no Retry-After, shared across families by source IP | measured, 62 hits on a national sweep | the real daily constraint |
| Small municípios screenable via SICONFI | **45%** (n=60, ±12,6 pp) of the 74,5% of municípios under 25k pop. | measured | rule 6 returns UNSCREENABLE for roughly half of real targets |
| Editais with a quantitative atestado | 1 of 12 | 7 retrieved + handoff's 5 | the feared barrier is largely illusory |
| Textile lines vs handoff | −44,8% on 5 comparable lines | re-measured | handoff had pack prices as unit prices |
| Mochila | R$ 52,27 vs R$ 25,00 target | measured | the one line that went the wrong way; 30% of BOM |
| Freight per kit | see the four freight rows above | `data/freight.md`, `data/cost_freight.csv` | measured for parcels and one LTL lane; the rest of the LTL map is the gap |
| Assembly per kit | — | `data/copacking.md`, 24 SP providers, 20 CNPJs resolved | **UNQUOTED — no provider publishes a per-kit price.** Only B2C per-order picks (R$4–19,50) exist, marked inference. One quote needed |
| Co-packer with own-account freight | COTLOG (10.273.317/0001-55), Doma (27.541.681/0001-51, branch in Belém-PA), Paulista Express | published | **Northeast under their own contract: UNVERIFIED for every provider** |
| Hand-assembly capacity evidenced | 7.500 kits / 10 working days | UP! Manuseios, published case | an events-handling ME, not a warehouse 3PL — matters for the 5.000-kit tail |
| Contract-free per-parcel routes | Correios "com ou sem contrato"; Melhor Envio on CPF; Loggi pre-paid | published | cover the ~100-kit median only if the box fits **100 cm/side, 200 cm sum** — a bathtub kit box is at that limit |

---

## 6. The files — where everything lives, who owns what

```
config/
  skus.yaml          24 SKUs: match, anti-patterns, plausible price window,
                     spec dimensions that must agree before two rows share a median
  rules.yaml         thresholds for the 13 rules — never in code
  capital.yaml       capital DIAL, float days, self-pack ceiling, co-packer lead
  ufs.yaml           target UFs by priority; transit_days null until measured
  documentos.yaml    16 documents + 5 platforms: validity days, whether the
                     period was READ at the issuer, cost, ME/EPP relief
  order_to_cash.yaml the 12 stages after a win, machine-readable
  cnaes.yaml         CNAEs to register, Simples admissibility
harvest/
  pncp_client.py     both API families, backoff, disk cache, resumable cursor,
                     ROUTE_MIXED detection, distinct ≠ served
  daily.py           the national scanner + the window guard
parse/
  normalise.py       THE FIVE FILTERS. Nothing bypasses it.
  spec.py            SKU classification with spec control (Filter 4)
  entrega.py         local de entrega: ONE_ADDRESS / CALLOFF / HOUSEHOLD /
                     UNKNOWN -> the freight mode; read on 9/9 real texts
price/
  cost.py            a cost row REQUIRES supplier CNPJ, UF, URL, date;
                     non-SP loaded +6 pts (LC 123 art. 13 §1 XIII h)
  bom.py             COST vs FLOOR; assembly line; a gap is never R$0
  margin.py          net of Simples; 75% anchor; NO BID when the floor is unknown
screen/
  rules.py           the 13 rules, pure functions, (passed, reason, evidence)
  documentos.py      certidão tracker: OK / RENOVAR / VENCIDA / FALTA per
                     document; can_bid(); next_run() = the 25-day cadence
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
  siconfi_screenability.md, copacking.md (24 SP providers), freight.md (453 rows)
docs/
  LEGAL_FINDINGS.md  six statutory questions, primary sources, confidence labels
  HABILITACAO.md, ORDER_TO_CASH.md, COMPANY_SETUP.md, RISK_REGISTER.md
tests/               370 tests. One per known measurement error, and growing.
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
| Freight to the actual município CEP, and LTL lanes beyond SP→CE | parcels measured only to capital CEPs; interior bands may differ; only one road carrier publishes a table | re-run the Correios form POST against the editais' own delivery CEPs. The *local de entrega* clause is now READ (`parse/entrega.py`, 9 of 9 real texts match the human reading): 4 name one seat, 4 leave the address to each ordem de fornecimento, 8 of 9 are *parcelado* — so only Belterra prices as LTL; every other bid must survive parcel freight |
| Assembly per kit | 24 SP providers surveyed, 20 CNPJs resolved: **none publishes a per-kit price** | one quote — never sent (needs her go-ahead) |
| Co-packer lead time | feeds rule 5 and rule 13; nothing published | same quote |
| Whether a co-packer ships on its own carrier contracts | COTLOG (Cotia) and Doma (Guarulhos, Belém-PA branch) publish own-fleet fractional freight + kit assembly; **no price published** | same quote |
| Transit days per UF | measured for 8 capitals (PAC 6–8 dias úteis); interior and the other 19 UFs not | being written into `config/ufs.yaml` from `cost_freight.csv`; rule 5 stays UNVERIFIABLE where nothing was measured |
| Capital available | rule 12 cannot verify funding until set | **the founder sets the dial** |
| Account-tier discount (~45%) | decides whether the whole basket is live | 15 supplier emails, never sent |
| Body 3-packs "RN AO G" | size-graded or three RN? | the real edital wording |
| Banheira band | R$18,90 / 23,65 / 29,71 on one word | the real edital wording |
| PGE-SP e-CRDA and RFB/PGFN validity | both feed the tracker; PGE site answered 405, RFB norm is JS-only — 30 d / 180 d are fallbacks | read the *válida até* on the first issued certidão and record it |
| Licitanet fees; BNC/BLL/PCP certificate requirement | which portals cost money to bid on | Licitanet is a JS shell (403) — UNVERIFIED; Compras.gov.br and BLL (plano por êxito) are free to bid on, BNC R$118,80 and PCP R$129 per process are READ |
| Homologação → convocação, and first call-off under SRP | empenho → cash is measured (34/40–55/69 days) but the wait before the empenho is unbounded in all 7 editais | only the bid log will measure it |
| Simples opt-in window | **≤60 days from CNPJ** (CGSN 140 art. 6º §5º I); miss it and she is in Lucro Presumido until January | a calendar item, not a research item — it goes on the setup checklist with a date |
| SP TFE (R$362,95/yr) for a PJ at a home address | whether it applies | one question to the contador |
| Family B availability | the reading rail; 503 on every attempt all day | **Monday 08:00 BRT scheduled re-check** |

---

## 9. What "humming" looks like

It is a Tuesday in March. The cron ran at 06:00 and the email arrived at
06:03: `ACOLHE 10/03 — 4 novas · 1 fecha em 4 dias · sistema OK`. She reads
it on her phone. One row says NÃO LICITAR: Icatu/MA — it paid 0,0% of last
year's liquidated invoices. The LICITAR row is a município near Fortaleza/CE,
180 kits, delivery to one CRAS address: goods R$ 198,78 + LTL freight
R$ 53,99 on the published SP→CE table + a quoted co-packer at R$ 5,00 =
**cost floor R$ 257,77**. Estimate R$ 420,00, anchor at 75% = R$ 315,00,
**gross 18%, net of Simples 14%.** Thin — and that is the honest number, not
the 51% the inherited plan carried, because the plan had no freight and no
assembly in it at all. Buyer paid 91% of prior-year invoices; atestado
qualitative; 12 days to deliver against 3 + 7 needed. She opens the platform,
enters R$ 315,00, and types LICITEI · 315,00 into her column. Twelve minutes.

The row below it is Aracaju/SE, 300 kits, **delivery to each beneficiary's
home** — parcel freight R$ 188,40 per kit on top of R$ 198,78 of goods
against a R$ 359 ceiling. NÃO LICITAR, and the reason says why: *frete por
encomenda excede a margem*. Six months ago that tender would have been bid
and lost money.

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

`docs/RISK_REGISTER.md` holds 45 ranked risks. Its top five, each verified
at source before being written here, and what was done:

1. **Rule 2 rejected 7 of 7 real editais.** The quantitative-atestado search
   spanned the whole document and matched `10%` / `5%` / `100%` from multa
   and garantia clauses. The human reading is 1 ABSENT + 6 QUALITATIVE. The
   day Family B returned text, every HOJE row would have read NÃO LICITAR.
   *Fixed: markers now searched only inside the qualificação-técnica window;
   the test runs over the real .txt files. Rule 10 likewise read a
   prohibition as an offer — negation now handled.*
2. **The diaper line was carried at 1/18 of a pack while wipes were carried
   per pack** — opposite conventions, R$22,46 in the flattering direction on
   the floor NO-BID relies on. *Fixed: pack basis, BOM → R$198,78.*
3. **The bid log did not accumulate.** MINHAS APOSTAS was rebuilt from
   today's candidates only, so Monday's bid and the lance she typed vanished
   from Tuesday's sheet. *Fixed: prior rows carried forward verbatim.* Still
   open: nothing bridges the workbook to `log/bidlog.py`, and the SQLite and
   workbook live only on the VPS.
4. **SRP call-offs she cannot refuse** — the single most dangerous
   unaddressed risk: everything else loses a tender or margin; this turns a
   *win* into a sanction. *SRP is now on every HOJE row; a rule that treats
   ≤5-day call-offs on an ARP as stock-holding is still to build.*
5. **Empate ficto works against the out-of-state ME, and a day-one company
   has no atestado at all.** The cheapest fix in the register: one private
   sale of a few kits to any PJ with a signed declaração.

Also from the register and confirmed: `skus.yaml` had drifted from the cost
table the same day the propagation rule was written (*fixed, with a drift
test*); `suggest_bid` returned a price with freight at R$0,00 on cubed goods
(*fixed: unquoted freight now blocks like an unpriced line*); rule 11 was a
gate rather than a flag and rejected every unlogged tender (*fixed*); and the
buyer screen is never called with the `codigoIbge` PNCP already supplies —
which is also how I screened the wrong municípios today (*retracted in
`data/siconfi_screenability.md`; wiring is next*).

Known already, unchanged: Family B never returning means the machine finds
but cannot read (*decision*); a certidão lapsing loses a won tender
(*expiry tracker, pending `documentos.yaml`*); the cron dying silently
(*heartbeat email, designed, held*).
