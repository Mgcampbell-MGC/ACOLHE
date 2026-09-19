# RISK REGISTER — ACOLHE

**Written:** 2026-09-19, against the working tree at commit `12106aa` plus the
uncommitted edits present on disk at the time of reading (`screen/rules.py`
rule 12 and `feasibility_from_config`, `price/bom.py` `assembly_cost`,
`price/cost.py` `is_stale`, `config/capital.yaml`, `config/ufs.yaml`).
While this was being written `harvest/run_daily.py`, `harvest/descend.py`
and `docs/BUSINESS_OPERATING_SYSTEM.md` appeared on disk (untracked). A grep
of `run_daily.py` finds no bidlog write, no email/Sheet transport, no use of
`codigoIbge`, no `srp` handling, no timezone — so entries H1, H2, A4, D1 and
A2 below stand against the entry point as it exists now.
**Stance:** adversarial. Nothing here was fixed, nobody was contacted, nothing
was spent. Where I measured something myself it says MEASURED; where I estimate
it says ESTIMATE and should be treated the way this repo treats any unverified
number.

Two things I measured while reading, because they are the kind of error this
project has caught a dozen times and had not caught yet:

- **MEASURED:** running `rule_2_atestado` over the seven real edital texts in
  `data/editais/*.txt` returns `QUANTITATIVE → REJECT` for **7 of 7** that have
  a qualificação técnica heading. The matches are `'10%'`, `'5%'`, `'100%'` —
  multa and garantia clauses, not atestado clauses. The rule scans the whole
  edital for `\d{1,3}\s*%`. The rule built specifically not to over-reject
  over-rejects 100% of the real sample. The 272 passing tests use two-line
  fixtures and cannot see it.
- **MEASURED:** the R$176,32 BOM subtotal recorded in commits `1587095` and
  `a0bcbb0` sums `fralda_descartavel_rn` at `cost_per_bom_unit = 1.3211`, i.e.
  **one diaper**, while `toalhas_umedecidas` is carried at a whole pack
  (R$6,02) "as the conservative reading". Same file, opposite conventions. A
  kit line is a pack ("pct com 30 unidades" in the São João do Paraíso spec).
  Restating diapers at the listed pack price alone moves the floor from
  R$176,32 to R$198,78; a 30-count pack moves it further. There is no
  per-kit quantity column anywhere, so the 3 bodies / 3 mijões / 3 macacões /
  2 cueiros of the same spec are each summed once.

---

## 1. Ranked table

Rank is by (likelihood × severity), then by how cheap the fix is. Severity
scale: **KILLS** = kills the business · **TENDER** = loses a tender ·
**MARGIN** = costs margin · **TIME** = costs her hours. Status: **UNADDRESSED**
· **DETECTED** (the system sees it and says so) · **MITIGATED** (there is a
control) · **IN PROGRESS** (uncommitted code on disk moves toward a control).

| # | Risk | Likelihood | Severity | Status | Cheapest credible mitigation (type) |
|---|------|-----------|----------|--------|--------------------------------------|
| 1 | Rule 2 rejects every real edital (whole-text `%` scan) | HIGH — MEASURED 7/7 | TENDER (every one) | UNADDRESSED | Scope marker search to the clause window; add a regression test that runs the rule over `data/editais/*.txt` (code, ~15 lines) |
| 2 | BOM has no per-kit quantity; diapers carried at 1/18 pack; multiples summed once | HIGH — MEASURED | MARGIN (−R$22 to −R$60/kit, flattering direction) | UNADDRESSED | Add `qty_per_kit` column and multiply; carry consumables at pack basis; trap test (code + data) |
| 3 | Workbook drops her typed rows after one day; nothing writes `log/bidlog.py` | HIGH — structural | KILLS the only compounding asset | UNADDRESSED | Carry forward every key in `hers`; append to SQLite on every row she marks "Eu licitei? = SIM" (code) |
| 4 | SRP call-offs she cannot refuse (5 dias úteis, parcelado, 12 months) | HIGH — 5 of 7 editais + Itaqua are RP | KILLS (default → art. 156 sanction) | UNADDRESSED (`srp` captured, never read) | Rule: SRP + prazo ≤ 5 dias úteis = NÃO LICITAR unless stock is held; show "RP" in HOJE (code) + never hold two atas in year one (decision) |
| 5 | Empate ficto local/regional gives a local ME last look on her price | HIGH — she is always the out-of-state bidder | TENDER (silently, after she leads) | UNADDRESSED | Flag `PRIORIDADE.*(LOCAL|REGIONAL)` / `SEDIADAS? LOCAL` as a warning; bid 10% under target or skip where it appears (code + decision) |
| 6 | Freight R$0,00 on goods that ship cubed (tub alone ≈ 7,8 kg cubed) | HIGH | MARGIN → KILLS a northern win | DETECTED (flag only) | `suggest_bid` returns NO BID when freight is None (code); one carrier quote for a 200-kit pallet to MG and to AM (money: R$0) |
| 7 | Family B is the only rail to items, edital PDF and quantities, and was 503 all day | HIGH — 15/15, three agents | TIME → kills the value proposition | DETECTED (recall floor stated) | Second rail: `linkSistemaOrigem` / platform document URL, and a "paste 5 clauses" fallback in the sheet (code + process) |
| 8 | Buyer CNPJ is the FMAS/FMS, not the prefeitura → UNSCREENABLE even where RREO exists; `codigoIbge` is in every Family A row and unused | HIGH — Irecê and Agrolândia buy via the Fundo | TIME / TENDER | UNADDRESSED | Screen by `unidadeOrgao.codigoIbge` first, CNPJ second (code, ~5 lines) |
| 9 | "Paid ~day 45" is a handoff assumption; editais say "30 dias após atesto" and atesto is undefined; SUAS not under IN 77 (UNVERIFIED) | HIGH | KILLS (cash) | DETECTED in LEGAL_FINDINGS, not in `capital.yaml` | Model 75 days until the bid log shows otherwise; write `docs/ORDER_TO_CASH.md` from the seven editais (decision) |
| 10 | Capital (US$500–2.500 ≈ R$2,7–13,7k) funds 12–60 kits per 45-day cycle; every priced supplier is prepay | HIGH | KILLS (slowly) | IN PROGRESS (rule 12 blocks big lots; nothing gets her to scale) | Set `available_brl`; bid only lots whose COGS ≤ 60% of capital; get Brascol CNAE answer (decision + process) |
| 11 | Atestado catch-22: 6 of 7 editais need one prior sale; she has none | HIGH on day one | TENDER | UNADDRESSED | One private sale of a few kits to any PJ (creche, ONG) and a signed declaração (process, ~R$500) |
| 12 | Cron dies silently; no heartbeat; no email/Sheet transport exists in the repo | HIGH over 12 months | TIME / TENDER (3-day windows) | UNADDRESSED | Free dead-man ping (healthchecks.io) + date in the workbook filename (code) |
| 13 | Bid log, cache and workbook live only on the R$30 VPS; git remote holds code only | MED | KILLS the asset | UNADDRESSED | Nightly copy of `db/`, `arquivo/`, workbook to her Google Drive or an encrypted git branch (code) |
| 14 | VERIFICAR is the normal outcome → she reads 40–263-page PDFs on 87 h/month | HIGH | TIME | DETECTED | Extract the five clauses (prazo, pagamento, atestado, amostra, julgamento) from PDF text into the sheet (code) |
| 15 | Emilio (11 of 16 lines) never verified as a supplier: tier, min order, terms, stock, login wall | HIGH | MARGIN / default | UNADDRESSED (credit policy covers only toiletries suppliers) | One registration and one R$500 test order (process, money) |
| 16 | Self-pack ceiling of 240 kits assumes 2 min/kit and 8 h total; receiving, checking and labelling 17 SKUs × 240 is not 8 h | MED-HIGH | MARGIN / default | IN PROGRESS (`assembly_cost` stub, copacker null) | Set `self_pack_max_kits` ≈ 80 until timed; one co-packer quote (decision + money) |
| 17 | Coari/AM = 34,8% of the clearing pool and Coari REJECTS on SICONFI (35,9% unpaid) | HIGH | KILLS the thesis if the residual pool is small | UNADDRESSED | Rebuild clearing stats from Family A homologated values excluding rule-6 rejects (code + decision) |
| 18 | SICONFI cache stores empty `{"items":[]}` forever; `exercicio=2026, periodo=3` hardcoded | MED | TIME (false NÃO VERIFICÁVEL forever) | UNADDRESSED | TTL on empty payloads; derive exercício/período from the date (code) |
| 19 | Rule 11 circularity + rule 6 interface mismatch: a good tender reads "NAO LICITAR: bid not written to the bid log"; `buyer.py` evidence has no `status` key | HIGH when wired | TENDER | UNADDRESSED | Make rule 11 a flag before bid time; adapter `evidence → {"status":"ok",...}` with a test (code) |
| 20 | Rule 10 turns "não … permitida a antecipação de pagamentos" into "Prioritise it" (MEASURED on Bom Sucesso do Sul) | MED | MARGIN / TIME | UNADDRESSED | Negative context (`NAO|VEDAD`) within 40 chars (code) |
| 21 | Rule 1 misses "MENOR PREÇO GLOBAL" (Irecê) because objeto has no "LOTE" | MED | MARGIN / TENDER | UNADDRESSED | Add pattern; read `criterioJulgamento` where present (code) |
| 22 | Samples: session suspended until first-placed bidder ships a kit (Bom Sucesso cap. XXIII) | MED | TIME / TENDER | UNADDRESSED | Flag `APRESENTA[CÇ][AÃ]O DE AMOSTRAS` (code) |
| 23 | Marca/modelo per item declared at proposal, locked for 12 months | MED | TIME / TENDER | UNADDRESSED | Declare manufacturer refs with alternates; buy at award (process) |
| 24 | Wrong NF-e (Fundo vs Prefeitura CNPJ, empenho number, NCM) restarts the payment clock | MED | TIME → cash | UNADDRESSED | Per-buyer NF checklist; ask for the empenho before shipping (process) |
| 25 | Certidões expire (FGTS 30 d) — checked at session and at each payment | MED | TIME | UNADDRESSED | Calendar reminder / SICAF (process) |
| 26 | Simples table stops at R$720k (7,58%); R$1,8M band is ≈9,45%; IRRF 1,2% and platform winner fees not modelled | MED | MARGIN 2–5 pts | UNADDRESSED | Extend table; add contingency lines (code, ~10 lines) |
| 27 | Kitting may be industrialização por encomenda → Anexo II + IPI; LEGAL_FINDINGS never asked | MED — UNVERIFIED | MARGIN / compliance | UNADDRESSED | Ask the contador before the first NF-e (decision) |
| 28 | `skus.yaml` costs drifted from `cost_table.csv` (banheira 29,71 vs 18,90; 3 "UNPRICED" lines are priced) | MED | MARGIN / TIME | UNADDRESSED | Delete `cost_observed` from skus.yaml or test equality (code) |
| 29 | Cost table rots: VTEX login wall → `Price: null` → rows silently vanish; CSV keeps 2026-09-19 forever | MED-HIGH | MARGIN | IN PROGRESS (`is_stale`, 30 d) | Weekly harvest asserts row count vs last run; stale row → NO BID (code) |
| 30 | She is sick for a week while a call-off or delivery is open | MED | KILLS if mid-delivery | UNADDRESSED | Never more than one open order; co-packer ships direct (decision) |
| 31 | Transit days null for every UF → rule 5 returns UNVERIFIABLE for every tender | HIGH | TIME (all VERIFICAR) | IN PROGRESS (honest null) | Correios published prazo table per UF (code, R$0) |
| 32 | "dias úteis" vs "dias corridos" not distinguished (5 úteis = 7 corridos) | MED | TENDER / default | UNADDRESSED | Parse the qualifier (code) |
| 33 | `in_window` / `days_left` compare naive Brasília timestamps to server clock (UTC VPS drops a tender 3 h early) | LOW | TENDER | UNADDRESSED | `zoneinfo("America/Sao_Paulo")` (code) |
| 34 | Two SICONFI docs disagree on the IBGE codes of the same municípios (Rodeiro 3156304 vs 3143906) — one screened the wrong ente | LOW-MED | TIME / wrong verdict | UNADDRESSED | Never resolve by name or by hand; use PNCP `codigoIbge` (code) |
| 35 | "Vedada subcontratação" + co-packer assembling the object | LOW-MED | TENDER / penalty | UNADDRESSED | Document co-packer as a packaging vendor, not a supplier of the object (decision) |
| 36 | Faceless vs public procurement: the ata, contract and DOM publish the razão social and often the signatory | LOW | constraint conflict | UNADDRESSED | Accept, or use a procurador (decision) |
| 37 | Incumbents: CONDAFE on 5.000-kit SRPs, BRINK MOBIL on component bands; 78,5% of winners win once = local one-offs | structural | MARGIN / TENDER | DETECTED in notes | Niche to 50–300-kit assembled lots where no local ME exists; verify after 10 logged bids (decision) |
| 38 | Family A 500s on single dates; a short day is flagged INCOMPLETA but nothing re-runs D-1 | MED | TENDER | DETECTED | Cron runs D, D-1, D-2 (cache makes it free) (code) |
| 39 | PNCP v1 deprecation / API key / tighter 429 | MED over 2 years | TIME | partly DETECTED | Pin version, alert on schema change (code) |
| 40 | xlsx round-trip between VPS and her PC; a rebuild between download and upload | MED | TIME | UNADDRESSED | Google Sheet via service account held by the machine (decision) |
| 41 | Textile labelling (composition label) missing on Brás wholesale garments → rejected at receipt | LOW | TIME | UNADDRESSED | Check on the test order (process) |
| 42 | Account-tier 45% inferred from paper | LOW | MARGIN | MITIGATED (published tier default + warning) | Delete the constant (code) |
| 43 | ICMS-ST exit 01/04/2026 not reflected in supplier prices; banheira NCM unverified | LOW | MARGIN | DETECTED in LEGAL_FINDINGS | Ask the supplier for NCM (process) |
| 44 | 429 budget on a shared egress IP | LOW | TIME | MITIGATED | Dedicated IPv4 (money, small) |
| 45 | The cost table is priced against a tender that is already awarded (Itaqua, `existeResultado: true`, SRP to CONDAFE) | certain | TIME | DETECTED | Re-anchor the BOM on a live spec (São João do Paraíso is in hand) (decision) |

---

## 2. Full entries

### A. Data rail

**A1. Family B is the only path to items, edital PDFs, quantities and results, and it was down all day.**
Mechanism: `harvest/daily.py` reads object text from Family A. Everything the
rules need beyond that — item count (rule 4, 8), edital text (rules 2, 3, 9,
10), quantity (rule 12), the PDF itself — lives only on `api/pncp/v1/…/itens`
and `…/arquivos/1`. Confirmed against the live OpenAPI document that Family A
has no such sub-resource. While Family B is down every kit candidate lands on
`VERIFICAR: sem dados de itens`. The machine is then a keyword scanner and she
is the parser. Likelihood HIGH: 15/15 attempts across three agents, HAProxy
"no server available", `/api/search` also down. Severity: TIME, and it removes
the reason the system exists. Status: DETECTED (the digest says "recall
ceiling ~1 in 4" and "INCOMPLETA"), UNMITIGATED. Cheapest mitigation: (code)
try `linkSistemaOrigem` and the platform's public document URL (BNC/BLL
publish the edital PDF at their own hosts; the municipal Cloudflare wall is
not the only copy); (process) give her a "paste the five clauses" column so a
manual read still feeds the rules.

**A2. Route fallback widens the date window.** MITIGATED by `in_window()`
after the Nova Roma/GO case. Residual: `in_window` and `report/digest.py
days_left` compare naive PNCP Brasília timestamps to `datetime.now()` on the
VPS. On a UTC box a tender closing 09:00 BRT reads as closed at 06:00 BRT and
is dropped as stale on its last morning — the morning she would bid.
Likelihood LOW, severity TENDER. Fix: `zoneinfo`.

**A3. Family A is up but not uniformly reliable.** A 500 on a single-date
`publicacao` query was observed. The client marks the day INCOMPLETA and the
health sheet says so — good — but the cron only ever asks for "today". A page
missed on Monday is never refetched. Fix: run D, D-1, D-2 every morning; the
never-expiring cache makes the repeat calls free.

**A4. SICONFI cannot screen ~55% of small municípios, and the CNPJ join makes
it worse than that.** The screen resolves buyer → IBGE via CNPJ in the entes
table. Kit tenders are bought by the Fundo Municipal de Assistência Social /
Fundo Municipal de Saúde with its own CNPJ (Irecê `18918319000166`, Agrolândia
`83102582000144` in `clauses.csv`); that CNPJ is not in the entes table, so
the buyer is UNSCREENABLE even when the prefeitura has a clean RREO. Family A
already carries `unidadeOrgao.codigoIbge` on every row (verified in
`itaqua_familyA_compra.json`: `"codigoIbge":"3523107"`) and `buyer_of()`
already extracts it as `ibge` — nothing passes it to `ScreenRequest.cod_ibge`.
Likelihood HIGH, severity TIME/TENDER (a real share of screenable buyers reads
NÃO VERIFICÁVEL). Fix: five lines.

**A5. SICONFI cache freezes empties forever; the period is hardcoded.**
`SiconfiClient.get_json` writes any HTTP 200 body to disk permanently,
including `{"items": []}` — which SICONFI returns for "not filed yet". A
município that files período 3 in October stays UNSCREENABLE on this VPS
until someone deletes `.cache/siconfi`. `ScreenRequest` defaults to
`exercicio=2026, periodo=3`; in 2027 nothing rolls it. Fix: TTL on empty
payloads, derive the period from the date.

**A6. The 429 budget.** Measured ~30 burst → 429, ~30 s, keyed on source IP,
shared across families. The daily listing (93 calls) is inside it; a Family B
descent (~5.400 calls) is ~3 hours at that rate, so "when Family B is back"
the daily loop is a 3-hour job, not a morning job. Also: SICONFI has no
observed limit today; it is Oracle ORDS and could add one. Status MITIGATED
(shared gate). Residual LOW.

### B. Measurement — the next error and where it hides

**B1. The diaper line is one diaper.** See the head of this document. The
subtotal that two commit messages quote as "BOM 16 of 17 at R$176,32" is
internally inconsistent: wipes at pack, diapers at unit. It hides in the
`basis` column — a column nothing reads. `bom.py` sums `cost` regardless of
basis. Likelihood: certain; severity MARGIN, in the flattering direction, on
the largest consumable in the kit. Fix: a `qty_per_kit` column, consumables
at pack basis, and a trap test that fails if any `per_*` basis appears
without a multiplier.

**B2. No per-kit quantity anywhere.** The São João do Paraíso spec
(`saojoaodoparaiso_kit_spec.json`) asks 3 body manga curta, 3 body manga
longa, 3 mijão, 3 macacão, 2 cueiro. The BOM sums one of each. Any real kit
will be 20–40% dearer than the table says. Same fix as B1.

**B3. `skus.yaml` disagrees with `cost_table.csv`.** BANHEIRA `cost_observed:
29.71` (corrected to 18,90 in `26ea255`), SABONETE 17,01 (now 8,99), SHAMPOO
21,39 (now 10,45), FRALDA_DESC / UMEDECIDAS / OLEO "UNPRICED" (all priced).
The README's own rule — "when a correction lands, propagate it" — was broken
on the day it was written. Nothing in the pipeline reads `cost_observed`
today, so the exposure is whoever reads it tomorrow (a "quick check" by her,
or a future shortcut). Fix: remove the field or test it against the CSV.

**B4. Two SICONFI documents disagree on the IBGE code of the same
município.** `siconfi_probe.md` §7 verified "Rodeiro/MG 3156304, Ribeirão
Corrente/SP 3543105" as zero-row; `siconfi_screenability.md` re-ran
"Rodeiro/MG (3143906)" and "Ribeirão Corrente/SP (3543501)" and found full
data. One of these screened a different município and called it evidence.
The by-name join in `EnteDirectory.by_name` and any hand-typed code can do
the same thing silently. This is exactly the class of error the project keeps
finding: the label is right and the identifier is wrong. Fix: use PNCP's
`codigoIbge`; never resolve by name; a test that the six validation entes'
names match the entes table.

**B5. Where the next one hides.** (i) Unit qualifiers nothing parses: "pct
c/03 unid", "kit com 3 pares", "pacote com 5", "dias úteis" — 7 of 20 SJP
lines and 4 of 7 delivery clauses carry one. (ii) `days_left` and rule 5
treat "5 dias úteis" as 5 calendar days. (iii) Emilio's 3-pack "TAMANHO RN AO
G" (flagged SIZE_GRADED — good) and Tenda's CEP-dependent price (flagged —
good). (iv) `rule_2`'s whole-text scan (below). The pattern across the git
log is: a regex or a sort that is right on the fixture and wrong on the real
document. Every rule in `screen/rules.py` has been tested only on fixtures.

**B6. The rules engine has never been run on a real edital — and when it is,
it rejects all of them.** MEASURED: `rule_2_atestado` over the seven texts
returns QUANTITATIVE for every edital with a qualificação técnica heading,
matching `'10%'` (Agrolândia — which has no atestado at all), `'5%'`
(Bocaiúva, Coronel Xavier Chaves, Irecê), `'100%'` (Belterra, SJP), `'10%'`
(Bom Sucesso). The marker search is not scoped to the clause. `rule_10` on
Bom Sucesso do Sul matches `ANTECIPACAO DE PAGAMENTO` inside "não sendo, em
nenhuma hipótese, permitida a antecipação de pagamentos" and reports
"expressly provided — prioritise it". `rule_1` on Irecê's objeto finds no
LOTE and passes the one MENOR PREÇO GLOBAL tender in the sample. Severity:
TENDER — as wired, the first day Family B returns edital text, HOJE reads
NÃO LICITAR on every line. Fix: scope rule 2 to the window between the
heading and the next numbered heading; negative context for rule 10; add
`MENOR PRE[CÇ]O GLOBAL` to rule 1; and a test file that runs every rule over
`data/editais/*.txt` with the expected verdicts from `clauses.csv`.

**B7. Rule 11 and rule 6 cannot be wired as written.** `run_all` fails any
tender with `logged=False`, and `report/digest.py _decision` turns any failed
non-flag rule into NÃO LICITAR — so the only tenders that will show "NAO
LICITAR: bid not written to the bid log" are the ones that passed everything
else. `rule_6` expects `{"status": "ok", "inscritos", "saldo", "cancelados"}`;
`screen_buyer` returns `(passed, reason, evidence)` with `outcome`,
`inscritos_brl`, `saldo_brl`. No adapter exists; the tests for each side use
their own shape. Whoever wires it will either write the adapter or get
UNSCREENABLE for every buyer. Fix: rule 11 becomes a flag until bid time;
one adapter with one test.

### C. Economics

**C1. Freight is R$0,00 on goods that ship by volume.** The tub is 513 g and
~0,047 m³: at the Correios divisor (6.000 cm³/kg) that is ≈7,8 kg cubed on
its own; the mochila adds ≈3 kg; a kit is ≈11 kg cubed and ships as air.
ESTIMATE: single-parcel Correios SP→AM/PA/MA at that weight is on the order
of R$100–180 per kit — i.e. more than the whole gross margin at the Itaqua
clearing price of R$359. Consolidated pallet freight to MG/BA by road is an
order of magnitude less per kit but needs a carrier contract; Coari has no
road. The BOM flags freight as ESTIMATE and `margin.py` warns, but
`suggest_bid` still returns a price with freight at zero. Fix: (code) freight
None → NO BID, like assembly; (money, R$0) one quote from Jadlog/Braspress/
Correios for a 200-kit pallet to Belo Horizonte and to Manaus; a per-UF
freight band in `ufs.yaml`.

**C2. Assembly is uncosted and the self-pack ceiling is optimistic.**
`capital.yaml` derives 240 kits from 8 h ÷ 2 min. That 8 h is the whole C9
budget for the order: receiving 17 SKUs from three suppliers, counting them,
checking sizes and labels, boxing, labelling each kit with its contents
(Belterra 11.6 / "etiqueta clara"), palletising, meeting the carrier. At a
realistic 5–8 min/kit the ceiling is 60–100 kits, and 240 kits is ≈17 m³ of
goods in an apartment. `copacker_cost_per_kit: null` and `copacker_lead_days:
null` — the co-packer that the business plan depends on above 100 kits has no
quote, no lead time, and no name. Fix: set the ceiling to 80 until timed; one
co-packer quote; the uncommitted `assembly_cost` correctly blocks above the
ceiling — keep that.

**C3. Capital vs lot size.** US$500–2.500 is ≈R$2.750–13.750. Every priced
supplier is prepay (JN: PIX/card; Tenda: boleto à vista; Emilio: unknown;
Brascol: boleto parcelado only for unspecified CNAEs). At ≈R$200–260 landed
per kit that is 12–60 kits per cycle, i.e. R$4–20k of revenue per 45–75-day
cycle, before contador (~R$250/month), certificado digital, VPS and platform
registration. At that scale the fixed overhead is a material share of gross
margin and the business cannot reach the lot sizes where the margin engine's
anchors were measured. Rule 12 (uncommitted) will correctly refuse the 5.000-
kit win; nothing in the repo describes how she gets from 40 kits to 400.
Decision only: set `available_brl`, cap lot COGS at ~60% of it, and treat the
Brascol CNAE answer as the first milestone.

**C4. Tax and fee lines not in `margin.py`.** `SIMPLES_ANEXO_I` stops at
R$720k (7,58%); the R$720k–1,8M band is ≈9,45% effective, so a good year is
under-taxed by ~2 points. IRRF 1,2% if a município withholds despite Anexo IV
is non-refundable through the RFB (LEGAL_FINDINGS §1) and is not a
contingency line. Platform winner fees: Agrolândia and Irecê run on BNC and
several platforms charge the winning supplier a usage fee — UNVERIFIED for
BNC, not grepped, not modelled. Fix: ten lines.

**C5. Kitting may reclassify her out of Anexo I.** Placing goods into a new
package is "acondicionamento" (RIPI, Decreto 7.212/2010, art. 4, IV), and an
encomendante of industrialização por encomenda can be equiparada a industrial
(art. 9, IV). If that reading holds, the ME falls into Anexo II with IPI in
the DAS and an IE as industrial. LEGAL_FINDINGS assumed Anexo I and did not
raise it. UNVERIFIED. Decision: one question to the contador before the first
NF-e — it also settles what NCM the kit line carries on the NF-e (RGI 3(b),
essential-character item), which is exactly the field that gets an NF-e
rejected (D3).

**C6. The account-tier discount.** 45% inferred from Chamex paper. Textiles in
Brás do not discount a published wholesale price by 45%. MITIGATED: the
default tier is published and the account tier is labelled INFERRED
everywhere. Residual LOW. Delete the constant before someone bids on it.

**C7. The mochila.** 30% of the current BOM at R$52,27 vs a R$25 target.
DETECTED. The real question is not the mochila: it is that the whole 17-line
BOM was priced against Itaquaquecetuba 2025/447, which has
`existeResultado: true`, `valorTotalHomologado 1.795.250`, is an SRP, and by
the README's own account went to CONDAFE — a tender she can never bid, whose
item list she never read. The one real, in-hand spec (SJP, 20 lines) has a
mamadeira (excluded) and 20 > 18 lines (rule 4). The cost table is anchored to
a phantom. Decision: re-anchor on the Belterra TR (7 pp, full item list,
in hand).

### D. Operations

**D1. SRP call-offs.** Itaqua `srp: true`; Agrolândia, Bocaiúva, Bom Sucesso,
Coronel Xavier Chaves, Irecê and SJP are all "registro de preços" with
"entrega parcelada … de acordo com as solicitações". An ata binds her for 12
months at a fixed price to deliver each Ordem de Fornecimento in 5 dias úteis
(Bom Sucesso, Irecê) or "imediato" (Belterra). Each call-off is a separate
purchase, freight, NF-e and 30-day clock; wholesale prices move within the
year; her capital sits in the previous call-off's receivable. Refusing a
call-off is inexecução: multa, impedimento de licitar with that ente for up to
3 years (Lei 14.133 art. 156, IV), declaração de inidoneidade nationally (V).
`daily.py` captures `srp` and nothing reads it; HOJE does not show it.
Likelihood HIGH, severity KILLS. Fix: (code) surface RP in HOJE and add a rule
that RP + prazo ≤ 5 dias úteis = NÃO LICITAR unless a stock line is on file;
(decision) one open ata at a time in year one.

**D2. Delivery deadlines vs transit.** 31,2% ≤ 5 days; Belterra "imediato"
with 24 h replacement of non-conforming goods — from São Paulo to Pará.
`ufs.yaml` transit_days are null for every UF, and the uncommitted rule 5
correctly returns UNVERIFIABLE — which means every tender is VERIFICAR until
someone types the numbers. Correios publishes prazo tables per origin/
destination for free. Also nothing distinguishes "dias úteis" from "dias
corridos". Fix: code, R$0.

**D3. A wrong NF-e restarts the clock.** The NF-e must name the right CNPJ
(the Fundo, not the Prefeitura — or vice versa), carry the empenho and
contract number in informações complementares, match item descriptions and
quantities to the empenho exactly, carry a defensible NCM per kit (C5), and
the right bank data. One rejection is +30–45 days on a business with 34 days
of float. No checklist exists. Fix: process — per-buyer checklist, ask for
the empenho before shipping.

**D4. Certidões.** CRF-FGTS is valid 30 days; CND federal and CNDT 180;
estadual and municipal vary by município. Habilitação must hold at the
session and throughout execution (art. 92, XVI); many municípios re-check at
payment. A sick week in the wrong month stops a payment. Fix: process — a
recurring reminder; SICAF where the platform reads it.

**D5. Samples.** Bom Sucesso do Sul cap. XXIII: the first-placed bidder may
be called to ship a sample within a deadline, session suspended pending
analysis; a `Parecer_amostras` was actually issued. A sample is one full kit
bought at retail speed and shipped at her cost, plus days. Rule 3 only
matches órgão-supplied samples. Fix: flag `APRESENTA[CÇ][AÃ]O DE AMOSTRAS`.

**D6. Brand lock-in.** Agrolândia, Bom Sucesso (3.5) and SJP (5.1.2, "de cada
item que compõe o kit") require marca and modelo per item in the proposal.
She is then bound to those SKUs for the ata's life; a stock-out at Emilio
means a written substitution request. Fix: process — declare manufacturer
references (Cajovil #0362, Camesa #1.12600 …) with one alternate each; buy
only after the OF.

**D7. Vedada subcontratação.** Belterra 9.4, Bom Sucesso 1.6/6.8, Agrolândia
8.1. A co-packer assembling the kits is, on a hostile reading, partial
subcontracting of the object. Likelihood LOW-MED; decision: document the
co-packer as a packaging vendor; keep the contract of supply in her name.

**D8. Textile labelling and INMETRO.** Coronel Xavier Chaves requires INMETRO
where compulsory (none of the kit lines except mamadeira/chupeta, correctly
excluded). Composition labels on garments are mandatory (Conmetro) and Brás
wholesale packs sometimes lack them; a receiving servant can refuse. LOW.
Check on the test order.

### E. Legal / fiscal

**E1. Empate ficto local/regional works against her every time.** Decreto
8.538 art. 9, II / LC 123 art. 48 §3: where the edital adopts it, a local or
regional ME within 10% of the best price gets to cover it. She is an SP ME
selling to MG/BA/CE/PE/PA/MA: she is never local. The clause is optional and
must be in the edital — and nothing in `rules.yaml` looks for it. This is the
most plausible explanation for "78,5% of winners win exactly once a year":
the local shop wins its own município's kit once, with last look. Severity
TENDER, silently — she bids, leads, and is covered. Fix: (code) a warning
flag on `PRIORIDADE DE CONTRATA[CÇ][AÃ]O.*(LOCAL|REGIONAL)` /
`SEDIADAS? (LOCAL|REGIONAL)MENTE`; (decision) either bid ≥10% under her own
target where it appears or skip.

**E2. Atestado on day one.** Rule 2 is right that a qualitative atestado is
satisfied by one prior sale — she has none. Six of seven editais need one;
only Agrolândia-type editais (ABSENT) are open to her today. Fix: one private
sale of a few kits to any PJ with a signed declaração — the cheapest legal
mitigation in this register.

**E3. IRRF.** Probable exemption, Anexo IV per contract, 1,2% if withheld,
no RFB refund. DETECTED in LEGAL_FINDINGS §1; not in the margin. Process:
Anexo IV attached to every proposal and contract; contingency line.

**E4. What LEGAL_FINDINGS left UNVERIFIED, and what each one costs.** (i) No
SC COSIT on art. 2º-A × art. 4º XI → 1,2% of gross per contract with a
literalist município. (ii) SUAS fundo-a-fundo not "transferência voluntária"
→ no federal 20-working-day clock; the clock is "30 dias após atesto" with
atesto undefined → cash cycle is whatever the município makes it; the 45-day
assumption in `capital.yaml` is a handoff figure and SICONFI says the median
small município still owes 21–24% of last year's liquidated invoices. (iii)
Banheira NCM vs ST annexes → a few points on one line. (iv) ADI 5464 formal
extinction → nil. The one that moves money is (ii).

**E5. ICMS-ST exit 01/04/2026.** Higiene left ST in SP; toiletry suppliers may
still price as if not; the DAS ICMS share on those lines rises. Net effect
probably favourable, not modelled. LOW.

**E6. Reforma tributária horizon.** LC 214/2025 and LC 227/2026 (noted in
LEGAL_FINDINGS §6.6) change how Simples optantes interact with IBS/CBS from
2027; compras governamentais have their own regime. Not a 2026 risk; a 2027
re-read.

### F. Competition

**F1. CONDAFE-scale incumbents.** The one tender the BOM was built around
cleared at R$359 for 5.000 kits under an SRP held by a firm with scale,
terms and logistics. Her landed floor with diapers restated, freight and
assembly is ESTIMATE R$230–290 — CONDAFE's price leaves her 20–35% gross on a
lot she cannot fund (rule 12) or pack (C2). The big SRPs are not her market.

**F2. BRINK MOBIL in the component bands.** Noted in `skus.yaml`: a
manufacturer with R$32M capital takes half the body+macacão band; 18,5% goes
to ME/EPP. Per-item component tenders are a manufacturer's market. Her
market is assembled kits in small municípios — which is exactly where SICONFI
cannot screen (A4) and where empate ficto lives (E1).

**F3. Atomised one-off winners.** If 78,5% of winners win once a year, there
is no repeat-buyer learning; the bid log needs 10 decided bids before
`win_rate()` will speak, and at 2–4 bids a month that is 3–5 months of blind
bidding. Decision: accept it and make the first ten bids small.

### G. Founder

**G1. The C9 budget is consumed by reading.** With Family B down every
candidate is VERIFICAR and the only way to a verdict is the PDF: 41–263 pages
(SJP is a 19 MB degraded scan). Four live candidates a day at an hour each is
the whole 87 h/month before a single bid. Fix: (code) extract the five
clauses from the PDF text into HOJE so she reads five lines, not 70 pages.

**G2. Live sessions.** Pregão eletrônico modo aberto is a live lance phase at
a fixed hour (09:00 Brasília for Irecê and Itaqua); overlapping sessions
cannot both be attended; "never phone-based selling" is fine but the session
itself is synchronous screen time. Decision: bid only where sessions do not
overlap; the digest should show session time, not only closing date.

**G3. Sick for a week.** No bids: fine. An open call-off or an in-transit
delivery with a 24 h replacement clause: a default, with no employee or
contractor allowed to step in. Decision: never more than one open order; a
co-packer who ships direct so fulfilment does not pass through her.

**G4. Single points of failure that are her.** Certidões (D4), NF-e (D3),
the session (G2), the workbook edit (H3), the supplier PIX payment, the
carrier booking, the co-packer instruction. Every one is a manual step with
no second operator by design. The mitigations are all "fewer open orders".

### H. System

**H1. Cron dies silently; no transport exists.** No heartbeat, no monitor,
no email, no Google Sheets code in the repo — the brief's "emails her a
Google Sheet row" is not built; `report/digest.py` writes an .xlsx to a path
on the VPS. If the cron stops, the file is simply yesterday's, and the SAUDE
sheet — which exists to say "something failed" — is only written when the run
happens. Fix: a free dead-man ping and the run date in the filename.

**H2. Her rows do not survive the day.** `build()` reads her columns back
keyed by Nº PNCP (good, tested), then writes MINHAS APOSTAS only for today's
`candidates`. Tenders are harvested by publication day, so Monday's tender is
absent on Tuesday and her typed lance for it is not re-emitted — it survives
only in `arquivo/<date>_ACOLHE.xlsx`. And nothing bridges the workbook to
`log/bidlog.py`: the SQLite bid log with its append-only invariants is
written by tests only. The repo says the bid log is the only asset that
compounds; as wired, it does not accumulate. Fix: carry forward every key in
`hers` even when not in today's candidates; append a bidlog row whenever "Eu
licitei?" is SIM.

**H3. Backup.** `.gitignore` excludes `db/*.sqlite` and `.cache/`; `arquivo/`
and the workbook live next to the digest on the VPS. The git remote
(`github.com/Mgcampbell-MGC/ACOLHE`) backs up code only. Losing the R$30 VPS
loses the bid log, every SICONFI/PNCP cache entry and her history. Fix: a
nightly copy to her Google Drive (she already has one) or an encrypted
branch.

**H4. The xlsx round trip.** She must get the file off the VPS, edit it in
Excel/LibreOffice, and put it back before the next rebuild, or the rebuild
reads stale columns. Two processes writing one file with `os.replace` is
atomic but not merged. Decision: a Google Sheet written by a service account
whose credentials live on the machine — consistent with "she never holds
credentials".

**H5. The cost table rots.** `tools/vtex_harvest.py` caches 7 days but is not
scheduled; `cost_table.csv` is hand-written with `verified_at 2026-09-19` on
every row; the uncommitted `is_stale` (30 days) is not called by anything
yet. A VTEX login wall returns `Price: null`, `rows_from` skips those rows,
and the harvest shrinks silently. Fix: schedule the harvest; assert row count
vs previous run; `is_stale` → NO BID.

**H6. PNCP API drift.** v1 could be deprecated, keyed, or throttled harder.
Partly DETECTED (unparseable body is a distinct failure). Fix: pin, alert.

### I. Concentration

**I1. Coari/AM.** 34,8% of the clearing pool and a rule-6 REJECT (35,9%
unpaid). Nhamundá (0% paid) and Icatu (0% paid) are also in the validation
set and both REJECT. The award/estimate anchors (0,75; per-item 97–100%; lote
único 36–63%) in `rules.yaml` and `margin.py` come from a handoff pool not in
this repo, dominated by buyers her own screen refuses. If the residual pool
after screening is a fraction of the headline, the market she is pricing for
is smaller and worse-paying than every number in `config/` implies. Fix:
rebuild the clearing statistics from Family A `valorTotalHomologado` over
the kit candidates, excluding rule-6 rejects and UNSCREENABLEs, and re-derive
`OPENING_ANCHOR` from that.

**I2. Supplier concentration.** Emilio supplies 11 of 16 priced lines and
has not been verified as a supplier at all (tier, cadastro, minimum, terms,
stock). Brascol, the only one with a published path to terms, is
login-gated and CNAE-gated. One login wall or one policy change at Emilio
re-prices most of the BOM overnight.

---

## 3. The five things I would fix before letting her bid

1. **Make the rules engine survive contact with a real edital.** Scope rule
   2's marker search to the clause window; negative context for rule 10;
   `MENOR PREÇO GLOBAL` in rule 1; rule 11 as a pre-bid flag; the rule 6
   adapter; a test that runs every rule over `data/editais/*.txt` and asserts
   the verdicts in `clauses.csv`. Today the engine rejects 7/7 real editais
   and flips one prohibition into a priority. Code, one afternoon.

2. **Give the BOM quantities, and carry consumables by the pack.** Add
   `qty_per_kit`, restate diapers, multiply the 3-body/3-mijão lines, and add
   the trap test. Then re-anchor the table on the Belterra TR instead of the
   awarded Itaqua tender. Until this is done the floor is understated by
   R$22–60 per kit in the flattering direction — the one direction this
   business cannot afford.

3. **Turn freight and SRP into hard gates, not flags.** `suggest_bid` returns
   NO BID when freight is None or when the tender is RP with a call-off
   deadline ≤ 5 dias úteis and no stock line. Get one carrier quote for a
   200-kit pallet to MG and to AM (R$0) and put a per-UF band in `ufs.yaml`
   alongside Correios' published transit days. Add the empate-ficto and
   amostra flags while in the file.

4. **Make the bid log actually accumulate, and back it up.** Carry forward
   every key she has typed; write a bidlog row on "Eu licitei? = SIM"; copy
   `db/`, `arquivo/` and the workbook off the VPS nightly; add a dead-man
   ping so a dead cron is loud. The only compounding asset must not depend on
   one R$30 box and one daily overwrite.

5. **Fix the two numbers only she can set, and the one sale only she can
   make.** Put a real `available_brl` in `capital.yaml` and let rule 12 cap
   lot COGS at ~60% of it; replace the 45-day cash assumption with 75 until
   the bid log says otherwise; and make one private sale of a few kits to a
   PJ to hold a signed atestado before the first pregão. Without the atestado
   six of seven editais are closed to her regardless of price.
