# ACOLHE: how the business runs

*Operations runbook, as of 2026-09-22. Written for the founder. English, with Portuguese terms of art.*

**How to read the numbers.** Every figure has a tag:
- **[M] MEASURED**: read directly from a primary source or a data file in the repo.
- **[C] CALCULATED**: derived from measured numbers. The arithmetic is shown.
- **[A] ASSUMED**: a modelling input that nobody has measured.
- **[U] UNVERIFIED**: claimed but not confirmed at source.
- **[ILLUSTRATIVE]**: invented for the worked example only. It is not evidence of anything.

**Read this first: the runbook and today are different.** This document describes how the business is meant to run once it is trading. Today it is not trading.
- There is no CNPJ, no bid, no customer, no supplier account, and no quote from anyone.
- `capital.available_brl` is null. The plan's R$15.600 is UNVERIFIED.
- The only kit that has been costed (Itaquaquecetuba) loses money on the pregão where it was actually bought (§4.1). **No dispensa kit has been costed, so there is no measured margin for the business the strategy targets.**
- The daily job is not scheduled anywhere (no cron, no systemd, no CI) and has no heartbeat.
- The daily job runs the SICONFI buyer screen (`screen/buyer.py`). Only a REJECT is written as a rule-6 failure (NÃO LICITAR). An unscreenable buyer shows as NÃO VERIFICÁVEL and falls through to VERIFICAR. The job runs none of the other rules and prices nothing. So the workbook can say only **VERIFICAR** or **NÃO LICITAR**, never **LICITAR** [M].
- There is one daily scan workbook, `docs/licitacoes/2026-09-19_licitacoes.xlsx` [M]. It covered PNCP publication day 2026-09-15 and ran 4 calendar days after it [C: 19 − 15]. It missed the Rio Branco do Sul dispensa (PDE 31/2026, R$16.520,64): the window guard dropped it because it had closed about 18 h earlier [M]. No scan has been saved since.
- The bid log has zero rows [M].

Every place below where the target differs from today is marked **TODAY:**. §8 lists what must change before the runbook can run as written.

---

## 1. The operating rhythm

### 1.1 Every recurring cycle

Who does it: **M** = machine, **F** = founder, **S** = supplier, **CP** = co-packer, **CA** = carrier, **MU** = municipality, **CT** = contador.

| Cycle | What happens | Who | Founder time |
|---|---|---|---|
| **Daily, 06:00: machine scan** | The job harvests yesterday's PNCP publications (Family A; modalidades 6, 7, 8) and runs the kit filter, the window guard, the descent into item lists (Family B), the SICONFI screen, the 13 rules, local de entrega/freight and pricing. It then writes `docs/licitacoes/AAAA-MM-DD_licitacoes.xlsx`. If PNCP is down the job **raises**, so a failure never looks like a quiet day. **TODAY:** the job is not scheduled, has no heartbeat, runs no rules beyond rule 6 and prices nothing. The workbook stays on the server's disk (RISK_REGISTER #12/#13). There is no daily fallback rail (`/api/search` is used only by research tools). | M | 0 h (target) [A] |
| **Daily, after the scan: founder review** | Open today's workbook and check that it covers yesterday's publication day; a missing or stale file means the scan failed. Read the LICITAR rows (target) or the VERIFICAR rows worth reading (today). Type a decision in her column; the machine keeps typed columns on the next run. | F | ~0,2 h/day [A]. RISK_REGISTER G1: VERIFICAR at ~1 h per edital could use the whole 87 h. |
| **Per bid** | Open the edital and confirm the delivery, local de entrega, payment and atestado clauses. Check the ME/EPP reserve and anything worth an impugnação (§2, step 11). Enter the proposal on the buyer's platform: Compras.gov.br R$0; BLL 1,5% of the adjudicated lote, cap R$600; BNC R$118,80/process; PCP R$129/process or R$165/month [M]. **Pregão only:** attend the live lance session at its fixed hour (§2, step 11). Write the bid-log row **at bid time** (rule 11). | F (platform) | **≤0,6 h** [A: BOS budget; the pregão session time is unmeasured] |
| **Per habilitação** (when she ranks first) | Upload the documents the edital demands. Only the winner provides documents. An ME gets 5+5 dias úteis to cure fiscal or labour certidões she presented [M: LC 123 art. 43 §1º]. The second 5 is at the Administration's discretion, so **plan on 5**. The cure does not cover a missing document, falência, balanço or atestado. | F, MU | inside the 0,6 h or the 8 h [A] |
| **Per won order** (single order or SRP call-off) | Acknowledge the empenho. Buy from SP wholesalers. Receive, store and assemble the kits. Emit the NF-e with the empenho number, ship, collect proof of delivery, chase the atesto, present the invoice package and follow up on payment. **Buy-after-win works only where the delivery clause allows ≥ ~11 days**; otherwise hold stock at her own risk or skip the tender. Above the self-pack ceiling a co-packer is required, and **0 of 24 providers surveyed publishes a price** [M]. **Storage:** where inbound goods and packed kits sit is unplanned. 100 packed kits take ≈9,6 m³ [C: 100 × 0,096 m³, on the ASSUMED box], before inbound cartons. Whether her home can hold that is an **open question**. | F, S, CP, CA, MU | **≤8 h** [A] |
| **Every ~25 days (CRF) and ~150 days** | **Every ~25 days:** reissue the CRF/FGTS. It is valid 30 days and renewable from day −5 [M]. Reissue the cartão CNPJ and JUCESP simplificada at the same time, for convenience. **Every ~150 days:** RFB/PGFN, SEFAZ-SP, PMSP and CNDT (180 days; read the "válida até" printed on each) [M]. That makes **5 core fiscal and labour certidões** [M]. Some editais also ask for the PGE-SP e-CRDA (validity UNVERIFIED; 30-day fallback [A]), the TJSP falência and the JUCESP simplificada, so count them per edital. **When they are checked: at signature, at each empenho and at payment** [M]. They also travel with the NF at delivery. | F | ~1 h per cycle [A] |
| **Weekly, Friday** (proposed) | Failure-mode check (§7). | F | ~0,5 h [A] |
| **Monthly** | Send the NF-e XMLs and the PJ bank statement to the contador, who issues the DAS (Simples Anexo I effective rates: 4,00% @R$180k · 5,65% @R$360k · 6,73% @R$500k · 7,58% @R$720k [C]). The DAS is due on the 20th of the following month (Res. CGSN 140 art. 40) [U in repo]. **Open question for the contador before the first NF-e:** does kitting count as industrialização (Anexo II + IPI)? Worth 2–5 margin points [U]. | F, CT | ~1 h [A]; contador R$136–225/month [M] |
| **Annual** | **TFE São Paulo:** R$362,95, due 10 July [M]. Whether it applies at a home address is unverified [U]. **e-CNPJ A1:** valid 365 days, R$203–275/yr, or R$0 through the Cora voucher (CNH holders) [M]. **SICAF:** 365 days, renews automatically [M]. **Balanço:** the contador prepares it. **An SRP requires a balanço even from an ME**, because an ARP is not pronta entrega (SICAF FAQ Q18) [M]. In its first year a company may use a balanço de abertura (art. 65 §1º). **December:** aim to have the atesto and liquidação done before 31/12 (§3.3) [A]. | F, CT | ~2 h/yr [A] |
| **The seasonal year** | The complete Window W (one phrasing, 12 months, 442 editais): January is the trough (20), March the peak (57), and the other months run 32–49. Mar–Aug is **≈1,4×** Dec–Jan [C]. The relevance-ranked harvest shows ~2×, which is inflated by the sampling. Plan certidões, stock checks and time off for December–January. | — | — |

### 1.2 The monthly time budget

**87 h/month** is her stated budget [A: stated by her, not measured]. At the aspiration of one win a week (all hour inputs assumed):

| Activity | Arithmetic | h/month | Tag |
|---|---|---|---|
| Bids | 272 dispensa records/yr × 0,6 h ÷ 12 | 13,6 | C on A |
| Won orders | 52/yr × 8 h ÷ 12 | 34,7 | C on A |
| **Headline: bids + wins** | 13,6 + 34,7 | **≈48 of 87** (48,3) | C on A |
| Other routine (not in the headline) | review 4,4 + certidões 1,2 + weekly 2,2 + contador 1,2 | ≈9,0 | C on A, no source for any input |

- **The bids line is crude.** 133 of the 272 records are "Ato que autoriza a Contratação Direta", which have no proposal window. Only 139 are Avisos she can bid on [C, re-run]. At 0,6 h each, the 139 Avisos give ≈7,0 h/month. RISK_REGISTER G1 puts reading at ~1 h per candidate, and at four candidates a day that fills all 87 h [A]. **Reading editais could consume far more than the budget assumes.** That is the first thing the bid log should measure.
- **The 19% is not a win rate.** 52 wins ÷ 272 dispensa records = 19% of *all* dispensas [C]. Against the 139 biddable Avisos alone it is **52 ÷ 139 = 37,4%** [C]. She will bid on fewer still after the rules discard some, so the rate needed per bid is higher. **The real win rate is unknown.**

---

## 2. The tender decision flow

A tender goes from publication to one of three verdicts: **LICITAR** (bid), **NÃO LICITAR** (do not bid, with a one-line reason in Portuguese), or **VERIFICAR** (the machine does not know, and says why). An unknown is never shown as NÃO LICITAR.

1. **Publication (day D).** The buyer publishes on PNCP. Across the 139 avisos of the last 12 months, the window from `data_inicio_vigencia` to `data_fim_vigencia` (read as the proposal window) has a **median of about 5 days** (p25 3, p75 6, maximum 14,7); **41 (29%) close within 3 days and 60 (43%) within 4** [C, `data/market/tenders.json`, re-run 2026-09-23]. Reading those two fields as the proposal window is an interpretation of PNCP's field names. **Scan every day.**
2. **06:00 on D+1: harvest** (Family A). A failed pull fails the job loudly and writes no workbook.
3. **Kit filter on the objeto.** **KILLS** non-kit rows. It keeps 2.044 of 4.333 raw rows [C].
4. **Window guard.** **KILLS** closed windows.
5. **Descent (Family B).** Reads lines, quantities and estimates. If Family B is unavailable or empty, the verdict is **VERIFICAR**. An outage is not an empty kit.
6. **Buyer screen: SICONFI, rule 6.** Restos a pagar saldo must be ≤30% of inscritos and cancelados ≤2%. **REJECT kills.** An unscreenable buyer is **not a pass**. About **45%** of small municípios can be screened (27/60, 95% CI ~32–58%) [M]; a second sample, 69/200 = 34,5%, falls inside that interval. **TODAY:** unscreenable falls through to VERIFICAR.
7. **The 13 rules** (`config/rules.yaml`): 10 gates (1–6, 8, 9, 12, 13) and 3 flags (7, 10, 11). A missing input on a gate fails that gate.

   | # | Rule | Effect |
   |---|---|---|
   | 1 | Lote único / item único | **KILLS**. **Open defect:** it rests on an unsourced 36–63% clearing figure, which is contradicted by 74,14% / 75,42% / 77,37% on three large lote pregões [M, n=3]. It also kills dispensa LOTE tenders (median R$492,88/kit, n=10 [C]). |
   | 2 | *Quantitative* atestado | **KILLS**. A qualitative atestado passes. |
   | 3 | "Conforme modelo do órgão" / "amostra fornecida" | **KILLS**. |
   | 4 | More than 18 items (warning above 15) | **KILLS**. An unknown count fails. |
   | 5 | Prazo de entrega < 3 days buy-and-assemble [A] + PAC transit to the capital [M] | **KILLS**. Prazo needed: SP 4, MG 8, BA/PE 9, CE/RN 10, MA/SE/PA 11. **Outside SP, no measured UF meets a ≤5-day call-off** [C]. The 19 UFs with no measured transit (including PR, SC, GO, RJ) are rejected at any prazo. The comparison ignores corridos vs úteis. |
   | 6 | SICONFI | **KILLS** on REJECT. |
   | 7 | ME/EPP reserve (LC 123 art. 48 I: lines ≤R$80k) | Flag. An unmarked reserve is a free impugnação ground (step 11). |
   | 8 | Every line classifiable into a SKU | **KILLS** above 20% unclassified. |
   | 9 | Payment deadline | **KILLS** above 45 days; a term that is not extracted also fails. |
   | 10 | Pagamento antecipado (art. 145) | Flag (good news). |
   | 11 | Log the bid | Flag. |
   | 12 | Kits ≤ pack ceiling, lot COGS ≤ capital | **KILLS**. **TODAY every tender fails here** (capital is null). |
   | 13 | SRP call-off ≤5 days with no stock | **KILLS**. Refusing an empenho under an ARP is total default (art. 90 §5), with a **20% fine** on the total value (Bom Sucesso 27.1, Bocaiúva 15.1) [M]. Other editais set their own rate. |

   **TODAY:** `screen/rules.py` passes its tests (the suite has 371 passing tests [M]) but is not wired into `run_daily.py`. RISK_REGISTER B6/B7: rules 6 and 11 cannot be wired as written, and all the rules have been tested only on fixtures.
8. **Local de entrega and freight.**
   - **ONE_ADDRESS** is priced as consolidated LTL. The only corridor with a carrier table is SP→Fortaleza capital, R$53,99/kit at 100 kits [C, on an ASSUMED 0,096 m³ box and invoice value]. The code calls this dict `LTL_MEASURED`, but the figures are calculated.
   - **CALLOFF / HOUSEHOLD / UNKNOWN** are priced as one parcel per kit: PAC balcão to capital CEPs, MG R$116,60 and NE/N R$132,90–188,40 [M]. Against a ~R$342 kit that is 39–55% [C]. Interior CEPs are unmeasured. **HOUSEHOLD** is killed by price.
9. **Pricing** (`price/`). The cost floor is BOM + freight + Simples, from which the machine suggests a bid. **TODAY:** no dispensa kit has a BOM, so any kit other than Itaquaquecetuba comes out `price_blocked` → **VERIFICAR**. `OPENING_ANCHOR = 0,75` is backed only by lote pregões (n=3). Kit dispensas clear at a median ~0,99 (all) and pregões at ~0,65 [C]. **Dispensa Avisos she can bid into clear at 0,868 (§4.2).** A per-mechanism anchor is needed before pricing is wired. The Simples table in the code stops at R$720k.
10. **Verdict.** Any failed gate gives NÃO LICITAR. All gates plus a price gives LICITAR. Anything unknown gives VERIFICAR. **The machine never bids.**
11. **Around the session (founder, per bid).**
    - **Impugnação:** file it up to **3 dias úteis before abertura**, free of charge (Lei 14.133 art. 164) [M: LEGAL_FINDINGS §5]. Grounds include an unmarked ME/EPP reserve (rule 7) and a missing interest clause. The deadline is short and cannot be recovered, so triage must happen on the day the edital appears.
    - **Recurso (art. 165):** used against later acts (habilitação, julgamento) [M]. The filing deadlines are not recorded in the repo [U]; read them in each edital.
    - **Live lance session (pregão fallback):** modo aberto runs live at a fixed hour, for example 09:00 Brasília at Irecê and Itaquá [M: RISK_REGISTER G2]. Two sessions at the same time cannot both be attended, so bid only where sessions do not overlap. The workbook should show session time. Time per session is unmeasured [A]. Whether dispensa Avisos also run a live lance phase is an **open question**; read each aviso.

**Kills outright:** kit filter, window guard, rules 1–6 (6 on REJECT), 8, 9, 12, 13; HOUSEHOLD by price; any kit whose cost floor exceeds the estimate. **Flags only:** 7, 10, 11.

---

## 3. Order to cash

### 3.1 The stages

Day 0 is homologação. Sources: `config/order_to_cash.yaml` and `docs/ORDER_TO_CASH.md`. The corpus is **7 editais, all pregão/SRP or a TR; 0 dispensas** [M]. Dispensa timing is extrapolated.

| # | Stage | Trigger | Realistic days | Who | Money |
|---|---|---|---|---|---|
| 1 | **Homologação / adjudicação** | Authority signs | day 0 | MU | — |
| 2 | **Convocação** to sign the contract/ARP | Homologação | The convocação itself is unbounded [U]. The signature window is 5 dias or 5 d.u., extendable once [M]. Certidões are checked. | MU → F | — |
| 3 | **ARP published** (SRP) | Signature | The lag is unmeasured [U]. The ARP binds her for 12 months, extendable to 24 (art. 84). It binds the buyer to nothing (art. 83) [M]. | MU | — |
| 4 | **Nota de Empenho + OF** | Single order: usually with the convocação [A]. SRP: any time in the vigência, or never. | **Acknowledge the same day.** The delivery deadline usually runs from the OF, and from the empenho in Bocaiúva and SJP [M]. Certidões are checked at empenho. **Nothing ships before the empenho exists** (her rule; an inference from Lei 4.320 arts. 58, 60, 63 and Lei 14.133 art. 83). | MU → F | — |
| 5 | **Purchase of goods** | Empenho | same day to +1 [A] | F → S | **OUT #1.** No priced supplier gives terms. MaxQualy publishes a 7-day boleto (hygiene only; R$300 minimum; carries no BOM line at spec) [M]. Brascol's boleto parcelado is CNAE-gated [U]. Both untested. |
| 6 | **Receipt, storage, assembly** | Goods arrive | ≈3 days buy+assemble [A]. Packing speed: an untimed 2 min/kit [A] vs 5–8 min/kit (RISK_REGISTER C2) [A]. The config's ceiling is 240 kits [C on A]; the register's realistic range is 60–100, and it recommends 80 until timed. Storage space is unplanned (§1.1). | S, F (or CP) | co-packer fee (unpriced) |
| 7 | **Shipping + NF-e** | Kits packed | Emit the NF-e to the CNPJ **on the empenho**. That is a Fundo (FMAS/FMS) for 16–18% of buyers [C]. Fields: xNEmp = empenho, xPed = OF, xCont = ata. PAC transit to capitals is 5–8 d.u. [M]. | F, CA | **OUT #2 (freight)** |
| 8 | **Delivery / recebimento provisório** | Arrival | Delivery deadlines run from immediate to 20 calendar days after call-off [M]. Keep a photo of the stamped DANFE. | CA, MU | **Late fines: 0,3%–5%** [M], set clause by clause: 0,3%/day (Irecê, SJP), 2% of the proposal per day (CXC), 5% for day 1 (Bom Sucesso). |
| 9 | **Recebimento definitivo / atesto** | Provisório | **5 of 7 editais fix no deadline** [M]. In most editais the payment clock starts here. A rejection means substitution within 24 h to 5 days [M], and the clock restarts. Follow up in writing every 5 d.u. | MU | — |
| 10 | **Invoice package** | Atesto | Target: 1 day after the atesto [A]. The package: NF-e, empenho, OF, valid certidões, signed Anexo IV (IN RFB 1.234), proof of Simples. **Any defect restarts the clock** [M]. | F | — |
| 11 | **Liquidação** | Complete documents | Only Bocaiúva fixes ≤5 d.u. [M]. | MU | — |
| 12 | **Ordem bancária → credit** | Liquidação | **Stated term: median 30 days for both dispensas (19 usable rows, 18 buyers) and pregões (8)**, after correcting 4 mis-parsed rows [C]. These are **written maxima, not observed payments**. At least 6–9 clauses are in dias úteis, but the parser flags none (a bug). Only 30 of 60 editais were readable. Certidões must be valid **on payment day**. | MU | **MONEY IN** |

### 3.2 The totals, and the float

- **Empenho → ordem bancária:** 34 d best · 40–55 d typical (on an assumed atesto lag) · 69 d worst bounded. SJP and Irecê are unbounded [C/A].
- **Homologação → cash, single order:** **~40 days best, 45–75 typical** [C: clause sums plus an assumed atesto lag]. **Under SRP it is unbounded** (art. 83).
- **Float** (all assumed): `capital.yaml` 34 days (pay on day 11, paid on day 45); the BOS models 45; the risk register recommends 75. **Plan on 45 and hold cash for 75.** Real payment speed is **unmeasured**; only the bid log will measure it.
- **Capital:** lots/yr = (K ÷ cash per lot) × (365 ÷ float) [C, identity]. K is null. R$15.600 comes from the written plan [U]. `COMPANY_SETUP.md` separately records a non-reloading founder budget of US$500–2.500 (R$2.579–12.894) for setup. Whether any of it is working capital is not recorded. **Whether even one median 100-kit lot is fundable cannot be known until both K and the kit's cost are measured.**

### 3.3 If payment is late

The `order_to_cash.yaml` S11 ladder, in order:
1. Written request citing the clause and the ordem cronológica (art. 141 §3).
2. Release of the parcela incontroversa (art. 143).
3. ME request to jump the queue (art. 141 §1 II).
4. Moratory interest, invoiced separately.
5. Art. 137 §2 IV notice once the delay exceeds 2 months from NF-e emission. That is day 60–63, usually 62 [C].
6. Representation to the Tribunal de Contas.

**December:** 31/12 is the cut-off (Lei 4.320 art. 36) [M]. A debt becomes RPP by being *liquidated* by 31/12, not merely attested. Aim for both before 31/12 [A]. How each município treats RPNP is UNVERIFIED.

---

## 4. The economics, and a worked example

### 4.1 The one costed kit (Step 0): a loss on a pregão

- **The kit:** Itaquaquecetuba PE 90088/2025 SRP, 17 lines, 5.000 kits. Estimate R$476,05/kit; award **R$359,05/kit (75,42%)** to CONDAFE [M].
- **BOM, 16 of 17 lines** (catalogue list prices, 2026-09-21, mochila excluded): **R$250,98** [C]. It excludes the mochila, the tub vinyl application, freight, assembly and tax. 8 of 11 colour-constrained lines are priced in colours the edital does not allow [M].
- **Award − BOM:** 359,05 − 250,98 = **R$108,07/kit (30,1%)** [C].
- **With the mochila at the buyer's R$98,51:** **R$9,56/kit (2,7%)** left [C; the mochila figure is ASSUMED]. Simples alone would take ~R$23–34/kit [C on an assumed RBT12].
- **Verdict: loss to breakeven, before freight and assembly.**
- **It is also unservable today:**
  - The quota alone is 1.250 kits, 5,2× the self-pack ceiling [C].
  - No co-packer is quoted.
  - The bag's 20-working-day lead time exceeds the 20-day delivery term.
  - Materials for the quota alone are R$313.725 [C].
- **Step 0 gate:** **STOP by the letter** (R$250,98 > R$230) [M]. It cannot be called on the merits until the mochila, vinyl application, freight and assembly are quoted.
- **The same spec on a dispensa** is hypothetical. No dispensa with this spec or estimate exists in the data [A].
- **This kit says nothing about a typical dispensa kit.** Do not carry its cost into §4.2.

### 4.2 Worked example: one small dispensa Aviso, publication to cash

> **Labels.** Legal steps and terms are **[M]** where the repo measures them. The municipality, dates, estimate, prices and hours are **[ILLUSTRATIVE]**. **The goods cost is UNMEASURED**, so the example shows a **breakeven**, not a profit. It assumes the target state: company open and on Simples, certidões valid, a qualitative atestado in hand, capital set, the scan wired and scheduled, and a BOM for this kit. **None of that exists today.**

**The tender [ILLUSTRATIVE]:**
- An Aviso de Contratação Direta from the Secretaria de Assistência Social of a ~15.000-inhabitant município in interior MG (MG is #2 by volume: 90 tenders in 12 months [C]).
- **100 kits**, the median dispensa lot [C]. PER_ITEM, 12 lines.
- Estimate **R$300,00/kit = R$30.000,00**. This is a round number, not a median of anything. For reference, the median homologated price across the 19 priced Avisos is R$236,72/kit [C, re-run], so kit contents vary widely.
- Delivery 15 calendar days from the empenho, to one address. Payment "até 30 dias após o atesto". Qualitative atestado.
- The lot is under the R$65.492,11 ceiling [M]. 100 kits is inside the config's 240 but **above the register's recommended 80** [A], so on that recommendation she would need a co-packer or would skip the tender.

**The price she wins at: 86,8% of the estimate = R$260,40/kit → R$26.040,00** [C].
- **86,8% is the median for dispensa Avisos** (n=19), the ones she can bid on [C, re-run from `results.json`].
- The all-dispensa median of 99% (n=52) is driven by the 33 Atos, which have no proposal window and clear at a median of 100% [C].
- **Sensitivity:** at 99% the price is R$297,00/kit → R$29.700,00. That is R$36,60/kit, or R$3.660 on the lot, more than the base case [C]. Do not plan on it.
- The sample is non-random and six months long.

| Date (2027) | Day | What happens | Who | Founder h | Cash out | Cash in |
|---|---|---|---|---|---|---|
| Tue 08/06 | — | Published on PNCP | MU | — | — | — |
| Wed 09/06, 06:00 | — | Scan: filter, window, descent, SICONFI PASS, rules pass, ONE_ADDRESS, priced → **LICITAR** | M | 0 | — | — |
| Wed 09/06 | — | Review. Read the edital, check stock and colour line by line (§7), check impugnação grounds, enter the proposal, write the bid-log row | F | 0,7 | platform R$0 (Compras.gov.br), or 1,5% on BLL if won | — |
| Mon 14/06 | — | Window closes (6 days [ILLUSTRATIVE]; the aviso median is about 5) | — | — | — | — |
| Tue 15/06 | — | Ranked first; uploads habilitação | F | 0,2 | — | — |
| **Thu 17/06** | **0** | **Homologação** | MU | — | — | — |
| Mon 21/06 | 4 | **Empenho + OF.** Acknowledged. **Deadline Tue 06/07.** Orders placed and paid. | F → S | 1,0 | **Goods: G (UNMEASURED)** | — |
| Thu 24/06 | 7 | Goods arrive at home and are checked against the OF. Space for ~9,6 m³ of packed kits is needed [C on A]. | S → F | 1,0 | — | — |
| Fri 25/06 | 8 | Packs 100 kits: ≈3,3 h at the untimed 2 min/kit, or 8,3–13,3 h at 5–8 min/kit [C on A]. NF-e with xNEmp. Carrier collects. | F, CA | 4,3 | **Freight: F (unmeasured)** | — |
| Fri 02/07 – Wed 07/07 | 15–20 | Transit is 5–8 d.u. [M]. At 8 d.u. the kits arrive one day late. | CA | — | **Day-1 fine** [C]: R$78,12 (0,3%) to R$1.302,00 (5%); CXC's 2% = R$520,80. A 20% cap would be R$5.208,00. | — |
| Fri 02/07 | 15 | Base case: delivered; stamped DANFE photographed | MU | 0,3 | — | — |
| Fri 09/07 | 22 | Atesto (5 d.u. [A]); invoice package sent; **30-day clock starts** | MU, F | 0,5 | — | — |
| ~05/07–10/07 | — | CRF renewal falls due (renewable from day −5) [M] | F | 0,3 | — | — |
| ~Tue 20/07 | — | **DAS on June's NF-e** [C]. At 4,00%: R$1.041,60. If June is her only revenue, RBT12 annualises to R$312.480 (2ª faixa) and the rate is 5,40%: **R$1.405,92** (Res. CGSN 140 art. 22). Cash or competência basis is UNVERIFIED. **The tax may leave before the customer pays.** | CT → F | 0,2 | **R$1.041,60–1.405,92** | — |
| Mon 26/07 | 39 | Written follow-up | F | 0,2 | — | — |
| **Mon 09/08** | **53** | **Cash lands** (OB by atesto + 30) | — | — | — | **R$26.040,00** |
| | | **Total founder time** | | **≈8,7 h** [ILLUSTRATIVE]. At 5–8 min/kit it is 13,7–18,7 h, above the 8 h C9 budget. | | |

**What the example shows [C on ILLUSTRATIVE inputs]:**
- **Float:** money leaves on days 4 and 8 and returns on day 53, so 45–49 days. That sits inside the 45–75-day typical band.
- **Breakeven all-in cost per kit** (goods + packaging + freight must come in below this):

  | Clearing | DAS 4,00% | DAS annualised | With BLL 1,5% |
  |---|---|---|---|
  | **86,8% (base)** | (26.040 − 1.041,60) ÷ 100 = **R$249,98** | (26.040 − 1.405,92) ÷ 100 = **R$246,34** | R$246,08 / R$242,43 |
  | 99% (upside) | (29.700 − 1.188,00) ÷ 100 = R$285,12 | (29.700 − 1.673,10) ÷ 100 = R$280,27 | R$280,67 / R$275,81 |

- **Whether a real dispensa kit costs less than this is the single unmeasured question in the business.** Nothing may be put in the table from the Itaquá BOM (a different kit), from BH parcel freight (R$116,60/kit [M]), or from the Fortaleza LTL corridor [C on A].

---

## 5. Year one: from opening the company to steady state

Dates assume she decides in October 2026. **Phase 0 comes before any money is spent.**

| Phase | When | What | Key facts |
|---|---|---|---|
| **0. Measure, then decide** | Oct 2026 | 1. **Price 10–20 real dispensa kits line by line.** Source: the 42 PER_ITEM kit dispensas with full item lists and homologated line prices (`data/typical_kit/tenders.json`, 42 rows) [M]. Favour Avisos, the kits she can bid on. In 21 of the 42 the line quantities differ, so a line sum is not always one kit; check each. Price against the `cost_table_v2` catalogues, plus freight to each address. **This settles viability without contacting anyone.**<br>2. Set `capital.available_brl`.<br>3. **Research calls: decide.** 33 rows / 30 municipalities are staged and none has been contacted [M]. **The calls do not have to come before any bid:** the measurement in item 1 needs no contact, and no rule requires a call. Whether research calls fit "never phones a buyer to sell" is her decision, not yet recorded (**open question**).<br>4. **CNAS 213/2025** ("preferencialmente em pecúnia"). The deadline is **28/10/2026, 36 days away** [U]. It was read only from a state copy; read the DOU original. **If buyers shift to cash:** no trigger for acting has been set (**open question**). What the repo supports: the monthly year-on-year count (§7) is the indicator. The scanner, rules, buyer screen and bid log are product-agnostic, so only `skus.yaml` and the cost table change (NICHOS §5). **Medalhas** is the named fallback, and the founder decided it is a later side income, not a switch (e91740f). Its profit-per-hour ranking (R$838/h vs kit R$1.157/h) rests on an assumed 30% margin and is **unsettled** after Step 0. Its +0,96 correlation with kit tenders means it does not fill seasonal gaps. **Measure medalhas the same way before spending on it.**<br>5. Schedule the scan and wire the rules (§8). | If the median dispensa kit does not clear materials + freight + tax by enough to pay for her 8 h, stop. The kit strategy then fails on its own terms. |
| **1. Open the company** | After item 1 says yes | SLU (no minimum capital; ME ≤R$360k, EPP ≤R$4,8M; MEI excluded) via VRE/Redesim SP. JUCESP R$218,99 (unavoidable). **CNPJ in ~1–2 days** (SP 2025 average 1 d 10 h). Then IE and CCM. Opening starts the Simples clock, so open only when she is ready to bid. | **One-time cost:** R$218,99 (minimum path; needs gov.br signature accepted [U] and the Cora e-CNPJ voucher, which needs a CNH) to R$1.012,89 (conservative) [C]. **Fixed:** R$196–473/month [C]. The TFE at a home address is unverified. |
| **2. Simples opt-in: hard deadline** | ≤30 days from last deferral, ≤60 from CNPJ | Request the Simples option. Tick it in the CNPJ application flow, and have the contador confirm on day 1. | **≤30 days from the last deferral (IE/CCM) and ≤60 days from CNPJ opening** [M: CGSN 140]. **Miss it and she is on Lucro Presumido until January.** Open question: an RFB FAQ citing Res. CGSN 183/2025 may have changed the procedure [U]; the contador should confirm. |
| **3. Bid-ready** | Weeks 1–3 | Conta PJ, e-CNPJ, certidões, SICAF, BLL/BNC/PCP cadastros, Anexo IV template, balanço de abertura. | 5 / **10–15** / 30+ business days to first bid [A]. |
| **4. First atestado** | Weeks 2–8, in parallel | **(i)** One private sale plus a signed declaration. Art. 67 does not restrict the issuer; acceptance in practice is unverified [M/U]. **(ii)** Editais without qualificação técnica, or with the art. 70 III waiver (<R$16.373,03 or entrega imediata; optional for the buyer). | **Plan on one private sale.** 7 of 8 real editais tested ask for a qualitative atestado [M]. How often dispensas ask was never counted [U]. |
| **5. First bids** | Mid-November onward | ≈22,7 kit dispensa records a month (272 ÷ 12), of which ≈11,6 are biddable Avisos (139 ÷ 12) [C]. Bid only on LICITAR rows. Avoid December deliveries that cannot be liquidated by 31/12. | Every bid writes a bid-log row. |
| **6. First win** | Unknown | 19% of all dispensas, or 37,4% of Avisos, are required shares, not win rates [C]. **The real win rate is unknown.** | The first win produces the first measured float. |
| **7. Ramp** | Feb–Sep 2027 | The March peak is ≈1,4× Dec–Jan (Window W) [C]. Capital, the pack ceiling, storage and hours decide how many orders run at once. RISK_REGISTER G3 advises never more than one open order. | BOS capital tables are **illustrative, not forecasts**. |
| **8. Capacity target (aspiration)** | Late 2027 | One win a week [A]. **≈48 of 87 h/month** on bids and wins [C on A]. | **Month-12 review from the bid log:** win rate, days to cash, cost vs price per kit. **Watch 2028** (end of mandates, LRF art. 42) [A]. The 2026 election year showed −2% [C: one phrasing, one year]. |

---

## 6. What never happens

**The founder never:**
- **phones a buyer to sell.** Research calls are a separate decision (§5, Phase 0). None has been made [M].
- **holds a buyer's credentials.**
- **hires employees or contractors.** Suppliers, co-packers, carriers and the contador are paid per service.
- **ships before an empenho exists.**
- **refuses an empenho under an ARP.** That is total default (art. 90 §5), with a 20% fine [M]. The protection is rule 13.
- **bids on a non-LICITAR row** without writing down why.

**The machine never:** contacts anyone; bids; fills a gap with a guess; hides a failure.

---

## 7. Failure modes to check every week (proposed Friday routine, ~0,5 h [A])

| Failure mode | Why it matters | Weekly check |
|---|---|---|
| **Late or missing scan** | Window lengths are unmeasured and one was ~3 days. The only scan ran 4 days late and missed Rio Branco do Sul [M]. | Five workbooks, each for the previous day? Heartbeat green? **TODAY:** no cron, no heartbeat. |
| **Certidão lapse** | Checked **at signature, empenho and payment** [M]. A lapse holds the payment [M]. | CRF expiring in ≤5 days → renew. Any 180-day certidão in its last 30 days → renew. |
| **SRP call-off** | An ARP binds her for 12–24 months. Call-offs run from immediate to 20 days [M]. Refusing costs a 20% fine [M]. | Open ARPs: price, remaining quantity, call-off term. Could she serve one this week? |
| **Parcel delivery** | R$116,60–188,40 per kit to capitals [M], 39–55% of a ~R$342 kit [C]. | Any bid not read as ONE_ADDRESS? |
| **Cheap kits** | Dispensa prices run from p25 ≈R$208 to p75 ≈R$515 [C]: contents vary widely. Profit per tier is **unmeasured**. A cheap kit still carries the same freight and the same 8 h. | For each bid: price per kit and freight share. The deal model's red flag is freight above ~20% of the bid [A]. |
| **Supplier stock-out or wrong colour** | Emilio supplies 11 of 16 lines (65,7% of value) and 15 of 16 lines are from SP; list prices only; nobody contacted [M/C]. 8 of 11 colour lines were non-conforming. No 22 L tub in amarelo/verde is in stock anywhere [M]. | Before each bid and each empenho: stock, colour and size line by line. A second source for each line. |
| **Storage full** | Unplanned; ~9,6 m³ per 100 packed kits [C on A]. | Space for the next order's inbound goods and packed kits? |
| **Atesto not arriving** | 5 of 7 editais set no deadline [M]. | After 5 d.u.: written follow-up. |
| **Payment overdue** | 30 days is a written maximum [C]. | Past term: start the S11 ladder (§3.3). |
| **Demand shock** | CNAS 213/2025 could move buyers to cash [U]. Births fell 15,5% 2019→2024 [C]. There is no federal money for kits (FNAS) [M]. | Monthly: kit tenders vs the same month last year. The trigger for turning to the medalhas measurement is not set (**open question**). |

---

## 8. Before this runbook can run as written

Ordered by what blocks the first safe bid:

1. **Measure the cost of real dispensa kits** (§5, Phase 0, item 1). There is no margin without it.
2. **Schedule the 06:00 job and add a heartbeat.**
3. **Wire rules 1–13 and pricing into `run_daily.py`.** Fix rule 1's unsourced threshold. Replace the 0,75 anchor with one per mechanism (Avisos 0,868; pregão 0,65).
4. **Record the decisions:** `capital.available_brl` (rule 12 fails every tender until it is set), research calls yes/no, and the CNAS response and trigger.
5. **Time the self-pack** on 10 real kits, replacing the 2 min/kit and the 240 ceiling. **Decide where stock is kept.**
6. **Build the workbook → bid-log bridge.** The bid log is the only asset that compounds, and it has zero rows.
7. **Get supplier quotes and terms:** Emilio's wholesale table, minimum and terms, plus a second source for single-source lines.
8. **Open the company** (§5), only after item 1 says yes and capital is set. Opening starts the Simples clock.