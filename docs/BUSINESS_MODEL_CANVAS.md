# ACOLHE: Business Model Canvas

*As of 2026-09-22. Every figure comes from the reconciled fact sheet or the repo's data files. The four figures marked "re-run 2026-09-22" were recomputed from `data/market/*.json` with the helpers in `tools/market_analyse.py`: the aviso/ato split, the proposal windows, the rule 5 exposure and the size bands.*

**Tags.** [MEASURED] means read directly from a primary source or a repo data file. [CALCULATED] means derived from measured numbers. [ASSUMED] means a modelling input nobody has measured. [UNVERIFIED] means claimed but not confirmed at source.

**Constraints that shape every block.** ACOLHE has one founder with about 87 hours a month. That is her own stated budget and a fixed limit, not a modelling input. She will never hire employees or contractors, though suppliers and service vendors are fine. She never phones a buyer to sell and never holds a buyer's credentials. The company has no CNPJ, no bid, no customer, no supplier account and no quote yet.

---

## 1. Customer Segments

- **Main segment: small municipalities buying kits by dispensa.** The buyer is the Secretaria de Assistência Social, and the kit is a benefício eventual handed out through the CRAS. There were 272 kit dispensas in the last 12 months [CALCULATED, floor], out of 786 kit tenders in total [CALCULATED, floor].
  - **Only about half of these dispensas can be bid (re-run 2026-09-22).** 133 of the 272 are published as an *Ato que autoriza a Contratação Direta*. That document authorises an award already decided, so there is no proposal window to bid into [MEASURED `tipo_nome` field; the "no window" meaning is a reading of the document type]. The other 139 are *Avisos de Contratação Direta*, which are open for proposals. **The biddable segment is 139 avisos a year, not 272.**
  - **Lot size:** the median lot is 100 kits [CALCULATED, n=52 priced dispensas]. For per-item tenders the lot is the largest line quantity, so this is a proxy and not a counted kit total.
  - **Contract value:** the median is R$40.100 [CALCULATED as kit price × lot proxy, n=52]. It is capped by the legal dispensa ceiling of R$65.492,11 [MEASURED, Decreto 12.807/2025].
- **The contracting body is often a Fundo, not the prefeitura.** 16–18% of kit tenders are published by an FMAS or FMS [CALCULATED by name match]. Whether the NF-e and the payment go to the fund's CNPJ has not been checked buyer by buyer [UNVERIFIED]. Proposals, invoices and certidões must name the right entity.
- **Municipal share:** about 98% of kit tenders by count [CALCULATED]. The share by value is lower, because two state central purchases are large.
- **Buyers are spread across the country.**
  - **Last 12 months:** 654 distinct municipalities published a kit tender (all spheres) [CALCULATED, floor]. Publishing a tender is not the same as buying.
  - **By state, 12 months:** SP 91 · MG 90 · BA 74 · PR 67 · GO 45 · MA 42 · PA 37 · PE 36. No state has more than about 12% [CALCULATED].
  - **Ever bought:** at least 1.124 municipalities (20,2%, Sample R) [CALCULATED, floor]. In the current harvest, 1.255 municipal-sphere buyers appear (22,5%) [CALCULATED].
  - **Repeat buyers:** 38,4% bought more than once [CALCULATED, floor, Sample R].
- **Delivery reach limits the segment in practice.** Rule 5 checks delivery time against measured transit days, and transit is measured for only 9 UFs: SP plus the eight target states. **18 UFs, including PR (67 tenders) and GO (45), have no measured transit time** [MEASURED, `config/ufs.yaml`]. For those UFs rule 5 returns UNVERIFIABLE, so once the rule is wired in, a tender there can never be LICITAR [MEASURED in code]. Those 18 UFs account for 328 of the 786 tenders in the last 12 months, 110 of the 272 dispensas and 53 of the 139 avisos (re-run 2026-09-22) [CALCULATED].
- **Fallback: pregões eletrônicos.** There were 491 in 12 months [CALCULATED]. They clear at a median 65% of the estimate [CALCULATED, n=40], and the 11 of 81–200 kits cleared at a median 62% [CALCULATED]. That makes pregões a harder, lower-price segment.
- **Out of reach today:** large single-lot SRP pregões such as Itaquaquecetuba (5.000 kits) [MEASURED], and state central programmes such as RS (80.000 kits) and MG (38.760) [MEASURED].
- **Demand risks for this segment:**
  - Federal money cannot pay for benefícios eventuais (FNAS) [MEASURED].
  - **CNAS Resolução 213/2025** makes cash the preferred form of the benefit ("preferencialmente garantidas em forma de pecúnia"). It was read only from a secondary copy, never from the DOU original. Councils must adapt their local rules by **28/10/2026, 36 days away** [UNVERIFIED].
  - Births fell 15,5% from 2019 to 2024 [CALCULATED].
  - **Election year 2026:** monthly editais fell 2%, from 38,7 to 37,9 a month [CALCULATED; one query phrasing, one year].
  - **Seasonality:** January is the trough (20 editais) and March the peak (57). Other months run 32–49, and March–August is about 1,4× December–January [CALCULATED, complete Window W, 442 editais].
- **One non-public customer is probably needed:** one private sale to obtain an atestado. 7 of the 8 real editais tested ask for one [MEASURED, n=8]. How often dispensas ask has never been counted [UNVERIFIED].

## 2. Value Propositions

- **For the buyer:** a complete kit that meets the specification, fully documented and delivered to the address in the edital, at or under the buyer's own estimate. The buyer does no extra work. Nothing is offered beyond what the edital asks for.
- **A valid proposal where offers may be few, at a smaller price edge than the headline suggests.** Dispensas clear at a median 99% of the estimate [CALCULATED, n=52], but the aviso/ato split changes what that means:
  - **Atos:** the 33 priced atos cleared at a median 100%, and 17 of them at exactly the estimate. She cannot bid into these.
  - **Avisos:** the 19 priced avisos cleared at a median **86,8%**, and 4 of them at the estimate (re-run 2026-09-22) [CALCULATED].
  - Against pregões at 65%, the edge she can actually use is therefore about 22 points, not 34. n=19 is small, and whether any aviso had competition is unknown [UNVERIFIED].
- **Size and mechanism are confounded.** Dispensas are mostly ≤200 kits and pregões mostly larger. The dispensa-over-pregão gap is established only within two size bands, n=47 in total [CALCULATED; the kit counts are lot proxies]:
  - 81–200 kits: dispensas 98,9% (n=18), pregões 62,3% (n=11).
  - 201–530 kits: dispensas 100% (n=10), pregões 67,5% (n=8).
  - The sample is non-random: most-recent-first, six months, one pull.
- **ME status, with the advantages it carries in law.**
  - ME/EPP quotas exist; the Itaquaquecetuba quota was 1.250 kits [MEASURED].
  - Fiscal or labour irregularities can be cured in 5 working days, plus 5 more if the administration grants them [MEASURED]. Plan on 5.
  - Small firms already win. On result lines with a declared porte, MEs won 677, EPPs 331 and other firms 245 [MEASURED]. These are article lines, not contracts.
- **National reach from the São Paulo wholesale cluster.** 15 of the 16 priced lines come from SP suppliers [MEASURED]. The reach is limited by rule 5 (see Customer Segments).
- **Clean compliance.** Documents follow the edital exactly. The CRF lasts 30 days and can be renewed from day −5, so it is reissued every 25 days [CALCULATED]. The pitch is reliability, not relationships.
- **Caveat: price competitiveness is unproven.** No dispensa kit has ever been costed, so ACOLHE cannot yet say it can meet an aviso estimate at a profit [UNVERIFIED].

## 3. Channels

- **Discovery: PNCP, read daily by the scanner.** One family of PNCP calls finds the tenders and a second pulls their items [MEASURED]. There is no daily fallback source: `/api/search` is used only by research tools [MEASURED].
  - The job is not scheduled anywhere and has no heartbeat [MEASURED].
  - Only one workbook exists, dated 2026-09-19. The run was four days late and missed the Rio Branco do Sul dispensa [MEASURED].
- **Proposal windows are short, so a late scan costs bids.** Across the 139 avisos of the last 12 months (re-run 2026-09-22) [CALCULATED from `data_inicio_vigencia` → `data_fim_vigencia`, read as the proposal window]:
  - The median window is about 5 days (p25 3, p75 6, maximum about 14,7).
  - 41 windows (29%) are 3 days or less, and 60 (43%) are 4 days or less.
  - A run that lags four days, as the only one on record did, can miss up to 43% of the biddable segment.
  - The earlier "about 3 days", based on one dispensa, is superseded.
- **Bidding platforms and fees [MEASURED]:** Compras.gov.br / SICAF R$0 · BLL 1,5% of the adjudicated lot, capped at R$600 · BNC R$118,80 per process · PCP R$129 per process or R$165 a month · Licitanet not confirmed [UNVERIFIED].
- **Delivery:**
  - **Correios PAC balcão from SP:** 5 dias úteis to Belo Horizonte and 6–8 to the North and Northeast capitals [MEASURED calculator quote, 2026-09-19]. These are quoted times, not observed transit, and interior CEPs are unmeasured.
  - **Deadline after a call-off:** from immediate to 20 calendar days [MEASURED clauses].
  - **Days needed under rule 5:** 3 days to buy and assemble [ASSUMED, never timed] plus PAC transit. That gives SP 4 · MG 8 · BA/PE 9 · CE/RN 10 · MA/SE/PA 11 [CALCULATED].
    - Buying after the win works only where the clause allows about 11 days or more. The clock starts at the empenho, not at the win.
    - Rule 13 treats an SRP call-off of 5 days or less as impossible without stock [MEASURED, config].
    - For a shorter clause she must hold stock at her own risk or skip the tender.
- **Getting paid:** NF-e, then the buyer's atesto (sign-off), then the ordem bancária (payment order). Written payment clauses have a median of 30 days for both dispensas and pregões [CALCULATED, corrected CSV]. These are written maxima, not observed payments.
- **No outbound sales channel.** There are no calls, visits or advertising. 33 contact rows covering 30 municipalities are staged for research calls, and none has been made [MEASURED]. Whether research calls fit her "never phones a buyer to sell" rule is her decision, not yet recorded.

## 4. Customer Relationships

- **The procedure is the relationship.** Buyers award by law, not by loyalty. 86% of buyer–supplier pairs are one-off, and 72,8% of suppliers hold a single contract [CALCULATED].
- **Repeat business has to be won again each time.** 38,4% of buyers bought more than once [CALCULATED, floor], but each purchase is a new tender. An SRP price register (ARP) creates no obligation to buy (art. 83) [MEASURED].
- **Contact is written and runs through the platform:** platform chat, e-mail and official letters. She never holds a buyer's logins.
- **Reputation builds through documents, not rapport.** Each on-time delivery can yield an atestado de capacidade técnica for the next tender. It is the only relationship asset that grows over time.
- **Penalties frame the relationship [MEASURED]:**
  - Refusing an empenho under an ARP counts as total default (Lei 14.133 art. 90 §5). The fine is 20%.
  - Late delivery costs 0,3%–5% per day. Each edital sets its own base and cap.
  - Reliability matters more than price here.

## 5. Revenue Streams

- **One revenue type:** per-kit sales on public contracts. There is no subscription and no recurring contract.
- **Medalhas: a later side income, not a switch** (founder decision, commit e91740f). Their monthly correlation with kit tenders is +0,96 [CALCULATED], so they do not fill empty months.
- **Dispensa price level [CALCULATED, n=52]:**
  - **Median R$342,05 per kit** (p25 about R$208, p75 about R$515).
  - By structure: per-item R$311,87 (n=42) and lote R$492,88 (n=10).
  - This median pools many different kit contents. Do not compare it with the R$250,98 Itaquaquecetuba bill of materials.
  - **Open avisos only** (the biddable ones, re-run 2026-09-22): median R$236,72 per kit, n=19. These are again different kits, and n is small.
- **Clearing:** a median 99% of the estimate across all dispensas, but **86,8% on the avisos she can bid** (see Value Propositions).
- **Revenue per win:** R$40.100 median on a 100-kit median lot [CALCULATED, n=52], capped at R$65.492,11 [MEASURED].
  - The R$40.100 is price × lot proxy. In 21 of the 42 per-item dispensas, line quantities differ, so the proxy can overstate revenue.
  - Two other medians measure different things and are not interchangeable: R$30.848 (80 kit dispensas in the descents) and R$17.092 (463 PNCP contracts, all mechanisms) [CALCULATED].
- **Pregão price level:** median R$382,44 per kit (n=40) [CALCULATED]. This is not a dispensa price. Three very large lote-único pregões cleared at 74–77% [MEASURED].
- **Timing of cash:**
  - Written payment term: median 30 days [CALCULATED].
  - **Homologação to cash, single order:** about 40 days at best, 45–75 typical [CALCULATED from 7 pregão editais plus an ASSUMED atesto lag]. No dispensa is in this set of editais.
  - **Under SRP there is no bound,** because the buyer need not order at all [MEASURED rule].
  - Actual payment speed is unknown, because there is no bid log [UNVERIFIED].
- **Volume is unknown.** One win a week means 52 wins a year:
  - Against all 272 dispensas that is a win rate of about 19%.
  - Against the 139 avisos she can actually bid it is **37,4%** [CALCULATED].
  - The real win rate has never been measured.

## 6. Key Resources

- **The founder's time:** 87 hours a month (her stated limit).
  - **One win a week while bidding all 272 dispensas:** about 48 h a month (35 h for wins plus 272 × 0,6 h ÷ 12 for bids) [CALCULATED on ASSUMED budgets of 8 h per win and 0,6 h per bid].
  - **Bidding only the 139 avisos:** about 42 h a month, on the same assumptions [CALCULATED].
  - Neither figure counts daily screening, reading VERIFICAR editais, certidão reissues or live sessions.
- **Money:**
  - `capital.available_brl` is null in config.
  - The written plan says R$15.600 [UNVERIFIED].
  - COMPANY_SETUP records her budget as **US$500–2.500 = R$2.579–12.894**, non-reloading (PTAX 18/09/2026) [MEASURED as recorded].
  - Whether that budget covers only company setup or also working capital is not recorded. Whether even one 100-kit lot is fundable depends on that answer and on a kit cost nobody has measured. **Open question for her.**
- **The scanner.**
  - It has 371 passing tests and 13 rules [MEASURED].
  - `run_daily.py` runs no admission rules (except rule 6 on REJECT) and no pricing, so every row reads VERIFICAR or NÃO LICITAR, never LICITAR [MEASURED].
  - **SICONFI buyer screen:** it can screen 45% of small municípios (27/60, 95% CI about 32–58%) [MEASURED, sample]. An earlier 34,5% run falls inside that interval.
- **Market data:**
  - `data/market/tenders.json`: 2.044 kit tenders, 2021–26.
  - `data/market/results.json`: 93 priced tenders.
  - `data/typical_kit/`: 42 per-item dispensas, 587 line items, exported for costing [MEASURED].
- **Legal identity (not yet created):**
  - A one-member limitada (SLU), taxed as an ME under the Simples.
  - An e-CNPJ certificate and a SICAF registration.
  - **Certidões:** five regularity certidões, checked at signature, empenho and payment. SRP requires a balanço even from an ME [MEASURED].
- **The bid log.** The code exists, but no rows have been written and db/ is empty [MEASURED]. It is the only asset that compounds with use.

## 7. Key Activities

- **Daily: scan, filter, screen buyers and descend into each tender's items.** Today this runs by hand, is not scheduled and produces no LICITAR [MEASURED]. Given the 5-day median window, it has to run every day.
- **Screen and price each tender.** This means wiring the 13 rules and the price model into the daily run. Four fixes come first:
  - **Rule 1** rejects every lote-único tender on an unsourced 36–63% clearing figure. The measured values contradict it: 74–77% on three large pregões [MEASURED], and 87–100% on the 10 lote dispensas [CALCULATED].
  - **Rule 5** needs transit days for the 18 unmeasured UFs, starting with PR and GO.
  - **The price model** opens every bid at 0,75, whatever the mechanism. The source of that figure is outside the repo [UNVERIFIED]. The measured aviso median is 86,8%.
  - **Simples table:** it stops at R$720k in the code.
- **Bid:** read the edital and file the proposal on the right platform. Allow about 0,6 h per bid [ASSUMED].
- **Keep habilitação current:** five certidões, with the CRF reissued every 25 days [CALCULATED]. File the Anexo IV declaration with every contract (see Cost Structure).
- **Fulfil each order:** buy in SP, receive and check the goods, assemble, ship, invoice, obtain the atesto and collect payment.
  - **Self-pack ceiling:** the config allows 240 kits [ASSUMED 2 min per kit, never timed]. The risk register estimates 60–100 and recommends 80 until the work is timed.
- **Log every bid and its outcome**, starting with the first. This is how the win rate and payment speed get measured.

## 8. Key Partners

- **Confecções Emilio (SP):** 11 of the 16 priced lines, 65,7% of the materials value [CALCULATED]. It has never been contacted, and its wholesale table, minimum order and terms are unseen [MEASURED]. This is a concentration risk.
- **Second sources:** 17 candidates with verified CNPJs, 13 in SP [MEASURED]. Only 2 lines have the same article confirmed at a second CNPJ [CALCULATED]. The hygiene lines are priced from public catalogues, one of them a CE drugstore for the óleo. None of these firms has been contacted.
- **Credit-term suppliers [MEASURED]:** none has been tested, and no priced supplier gives terms.
  - MaxQualy publishes a 7-day boleto, for hygiene goods only.
  - Brascol offers a boleto parcelado (instalment payment slip), restricted by CNAE (activity code).
- **Co-packers:** none of the 24 surveyed publishes a per-kit price [MEASURED]. An earlier "quoted R$5,00" was never a quote.
- **Carriers.** All the per-kit figures below assume one kit per box [ASSUMED], and the tub box's real size is unverified.

  | Option | Price | Tag |
  |---|---|---|
  | Correios PAC balcão, one 60×40×40 box per kit | Belo Horizonte R$116,60 (5 d.u.); NE capitals R$132,90–188,40 | MEASURED 2026-09-19 |
  | PAC via Melhor Envio (no contract, no minimum) | 12,4% below balcão | MEASURED |
  | Two-box split (tub + soft goods), balcão | about 20% cheaper: R$94,20 (BH) to R$147,80 (São Luís, Aracaju, Natal) | CALCULATED on the seller-stated tub size |
  | Two-box split via Melhor Envio | R$84,49–131,76 | CALCULATED |
  | LATAM Cargo éFácil via Melhor Envio | R$88,09–116,48, capitals only; interior coverage unverified | MEASURED |
  | STC road LTL, SP→Fortaleza, 100 kits | R$53,99 per kit | CALCULATED from published rates on an ASSUMED box and NF value |

- **Contador (accountant).**
  - **Simples opt-in:** within 30 days of the last inscription deferral and never later than 60 days after the CNPJ opening date. Miss it and the company is on Lucro Presumido until January [MEASURED, CGSN 140 art. 6 §5 I].
  - Another project document says Res. CGSN 183/2025 replaced this with an opt-in at CNPJ registration. Nothing in the repo sources that claim [UNVERIFIED]. The contador should confirm it before the CNPJ is opened.
  - The contador also prepares the SRP balanço.
- **Certificate authority, JUCESP and the bank [MEASURED]:**
  - e-CNPJ: R$203–275 a year, or R$0 in the first year through Cora (for CNH holders).
  - JUCESP registration fee: R$218,99.

## 9. Cost Structure

- **Materials: the only kit costed is the wrong kit to plan on.**
  - **Itaquaquecetuba spec, 16 of 17 lines: R$250,98** [CALCULATED from list prices, 2026-09-21].
    - Excluded: the mochila, the tub vinyl's application, freight, assembly and tax.
    - 8 of the 11 lines with a colour requirement are priced in colours the edital does not allow [MEASURED].
  - **With the mochila at the buyer's own line estimate of R$98,51: R$349,49** [CALCULATED; the mochila figure is ASSUMED].
  - **The cost of a typical dispensa kit has never been measured.**
- **Step 0 gate** [MEASURED, git 6cc7938]:
  - The written rule: at ≤R$200, build everything; at R$200–230, open a supplier account first; above R$230, stop.
  - **R$250,98 means STOP by the letter.** On the merits the call is not yet possible: it turns on four unquoted inputs (mochila, vinyl application, freight and assembly).
  - The gate was set for the Itaquaquecetuba spec and says nothing about a dispensa kit.
- **Freight:** no figure exists for any real buyer's address. See Key Partners for the measured options. Against a kit of about R$342, parcel freight of R$85–188 would be 25–55% of the price [CALCULATED ratio; the kits differ].
- **Assembly and printing:**
  - No per-kit assembly price exists [MEASURED].
  - Tub vinyl printing costs R$1,86–2,78 per kit; applying it is unpriced [CALCULATED].
  - Silk-screen setup for the mochila costs R$720–1.500, one time [ASSUMED].
- **Storage:** the risk register puts 240 Itaquaquecetuba-type kits at about 17 m³ [ASSUMED]. Pro rata, a 100-kit lot is about 7 m³ [CALCULATED on ASSUMED]. Where lots would be stored, and at what cost, is not recorded. **Open question.**
- **Atestado private sale:** one sale of a few kits to a company or organisation (a creche or ONG), with a signed declaration. The register estimates about R$500 for the process [ASSUMED], plus the kits themselves. Whether a buyer accepts it in practice is [UNVERIFIED].
- **Tax:**
  - **Simples Anexo I effective rates:** 4,00% at R$180k, 5,65% at R$360k, 6,73% at R$500k and 7,58% at R$720k [CALCULATED]. The code's table stops at R$720k.
  - **DIFAL** on sales: 0 for a Simples company [MEASURED].
  - **ICMS differential on inputs bought from other states:** about 6 points [ASSUMED].
  - **IRRF 1,2% withholding:** a Simples optant is probably exempt if it files the IN RFB 1.234/2012 **Anexo IV** declaration with each contract, in two copies, at signature (art. 6 §5) [MEASURED statute]. Treat each empenho as a new contract [ASSUMED reading].
    - No COSIT ruling confirms the exemption [UNVERIFIED].
    - One edital (Coronel Xavier Chaves) asserts retention with no Simples carve-out [MEASURED].
    - Amounts withheld are not recoverable from the RFB. On a R$342,05 kit, the exposure is about R$4,10 per kit [CALCULATED].
  - **Kitting as industrialização** (Anexo II plus IPI) has never been asked. It could be worth 2–5 margin points [UNVERIFIED].
- **Fixed and one-time costs [CALCULATED]:**
  - Monthly fixed: R$196–473 (R$2.352–5.676 a year).
  - One-time setup: R$218,99–1.012,89. The minimum needs JUCESP to accept a gov.br signature [UNVERIFIED] and a free e-CNPJ through Cora, which requires a CNH.
  - Platform fees: see Channels.
- **Cost of capital: the payment float.**
  - **In config:** `capital.yaml` pays the supplier on day 11 and is paid on day 45, a 34-day float [ASSUMED inputs].
  - **In the operating document (BOS):** a 45-day float [ASSUMED].
  - **In the risk register:** it recommends modelling 75 days [ASSUMED].
  - **Homologação to cash:** about 40 days at best and 45–75 typical, with SRP unbounded [CALCULATED].
  - No supplier terms are in place [MEASURED].
- **Margin: none can be stated for a dispensa kit.**
  - **Itaquaquecetuba, on a pregão:**
    - R$359,05 − R$250,98 = **R$108,07 per kit (30,1%)** before the mochila [CALCULATED].
    - With the mochila at R$98,51, **R$9,56 (2,7%)** remains [CALCULATED; mochila ASSUMED].
    - Simples alone would be about **R$23–34 per kit**: 6,41% if only the quota is won and 9,45% for the full award [CALCULATED on an ASSUMED RBT12]. That already exceeds R$9,56.
    - **Verdict: a loss to breakeven before freight and assembly.** The kit is also unservable at that scale: no co-packer, and 1.250+ kits against a self-pack ceiling of 240.
  - **The same spec on a dispensa:** hypothetical. No dispensa with this spec or this estimate exists in the data.
  - **A typical dispensa kit:** the price is measured, the cost is **UNMEASURED**.
  - The old "R$382,44 / R$252,77 / 33,9% gross" compared a pregão price median with a bill of materials priced against the wrong spec. It is void.

---

## What the canvas says

The right-hand side of the canvas is measured and strong. There are about 786 kit tenders a year, spread across roughly 650 municipalities with no state above about 12%. Contracts are unconcentrated (HHI about 181), and small firms win. **The biddable dispensa segment, however, is 139 avisos, not 272.** Those avisos clear at a median 86,8% (n=19), not 99%. That is still about 22 points above pregões, but on a small sample and only within the 81–530-kit bands. One win a week needs a 37,4% win rate on avisos. More than a third of the avisos (53 of 139) are in states that rule 5 cannot yet clear, and 43% close within 4 days, so a scanner that does not run daily loses them.

The left-hand side and the cost base are mostly assumed or empty. No partner has been contacted, no quote exists, and capital is null. Her budget is recorded as R$2.579–12.894 against a plan figure of R$15.600. The scanner cannot yet recommend a bid. The price she can charge is known; what it costs to deliver that kit to that address is not. The only kit costed end to end fails its own Step 0 gate and would lose money at pregão clearing.

## The block most likely to be wrong

**Cost Structure.** Every other block has at least a measured floor, but the cost of the product the strategy depends on, a typical ≤200-kit aviso kit, has never been measured. Dispensa kit prices run from about R$208 (p25) to R$515 (p75), so no single bill of materials can stand in for them. The cost could be viable or fatal, and nothing in hand says which. It can be settled without contacting anyone:

1. Start from `data/typical_kit/` (42 per-item dispensas, 587 lines).
2. Exclude the 2 tenders where a lot total was recorded as a unit price (Pedro Laurentino/PI and Ribeira do Piauí/PI), which leaves 40.
3. Weight the result towards the 15 avisos among the 42, because those are the kits she can actually bid. The sample was collected most-recent-first, not at random.
4. Price each kit line by line, using its real line quantities, against the same SP catalogues used for `cost_table_v2`.
5. Add freight to each buyer's address, tax and IRRF exposure.

That gives a measured cost against a measured price for the same kit.

## Next steps and sequencing

This is a recommended order. It is not measured, and the choices in step 2 are hers.

1. **Run the measurement above.** It needs no contact and no spending.
2. **Decisions only she can make, in parallel:**
   - Set `capital.available_brl`, and say whether R$2.579–12.894 is all the money there is.
   - Decide whether research calls fit her no-selling-calls rule.
   - Watch CNAS 213/2025 up to 28/10/2026 and try again to read the DOU original.
3. **Wire and schedule the system:**
   - Put the rules and pricing into `run_daily.py`.
   - Fix rule 1, add transit days for PR and GO, and replace the 0,75 opening ratio with a mechanism-specific one.
   - Schedule the job daily, with a heartbeat.
   - Build the bridge from the workbook to the bid log.
4. **Only if step 1 clears:**
   - Get quotes: Emilio's wholesale table, one co-packer, freight to real addresses.
   - Time the self-pack.
   - Arrange the atestado private sale.
5. **Hold off opening the company until steps 1 and 2 are done.** Opening starts the ≤60-day Simples clock and the monthly fixed costs. The contador should first confirm whether the opt-in rule has changed.

---

## Layout for the classic canvas grid

| Key Partners (§8) | Key Activities (§7) | Value Propositions (§2) | Customer Relationships (§4) | Customer Segments (§1) |
|---|---|---|---|---|
| (left, full height) | Key Resources (§6) (stacked under Key Activities) | (centre, full height) | Channels (§3) (stacked under Customer Relationships) | (right, full height) |
| **Cost Structure (§9)**, bottom left, under Partners, Activities and Resources | | | **Revenue Streams (§5)**, bottom right, under Relationships, Channels and Segments | |

- **Top band:** five columns. The left column is Key Partners. The second has Key Activities over Key Resources. The centre is Value Propositions. The fourth has Customer Relationships over Channels. The right column is Customer Segments.
- **Bottom band:** Cost Structure on the left and Revenue Streams on the right.
- **Reading the canvas:** measured on the right (Segments, Channels, Revenue), mostly assumed on the left (Partners, Resources, Costs).