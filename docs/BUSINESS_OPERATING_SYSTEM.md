# ACOLHE: how the business works

**Rewritten 2026-09-22.** This version replaces the one dated 2026-09-21. Several things arrived after that version was written: the Step 0 costing, the payment-terms measurement, the niche study and a re-run of the market figures. Several of its headline numbers did not survive them. A review of this rewrite was also applied: it corrects figures that disagreed with the reconciled fact sheet, and it adds the missing go/no-go threshold, capital, storage, tax-timing and delivery-risk material. §11 lists what changed.

**How to read the numbers.** Every figure carries a tag:

| Tag | Meaning |
|---|---|
| **[M]** MEASURED | Read directly from a primary source or from a data file in this repo |
| **[C]** CALCULATED | Worked out from measured numbers. The arithmetic is shown where it is short. |
| **[A]** ASSUMED | A modelling input that nobody has measured |
| **[U]** UNVERIFIED | Claimed, but not confirmed at the source |

**The standing rule:** a number is only as good as where it came from. Every retraction this project has had to make came from one mistake: taking a number from one case and applying it to a case that was not comparable. Three examples: a per-item clearing ratio applied to a lote, a pregão price applied to a dispensa, and one kit's cost compared with a different kit's price. This document does not do that. Where a comparison would be needed and does not exist, the document says so.

---

## 0. The business in one paragraph

One person in São Paulo plans to sell newborn layette kits (*kit natalidade / enxoval de bebê*) to Brazilian municipalities, through public procurement published on PNCP. She has about 87 hours a month; that is her own stated limit. She will never hire employees or contractors, although suppliers and service vendors are fine. She never phones a buyer to sell and never holds a buyer's credentials.

A system in this repo reads the kit tenders published on PNCP and throws out the ones that cannot be won or served. It is meant to tell her which to bid. Today it can find and screen tenders, but it cannot yet recommend one (§7).

**The main finding so far is about the purchase mechanism, not the product.** Dispensas clear at a median of 99% of the buyer's estimate, against 65% for pregões [C]. The 99% pools two kinds of dispensa: direct-award atos, which she cannot bid, and open avisos, which she can. The 19 open avisos clear at a median of 86,8% [C] (§2). The strategy is built on this finding.

**Nobody yet knows whether a typical dispensa kit can be supplied at a profit.** No dispensa kit has ever been costed. One kit has been costed: Itaquaquecetuba's branded 17-line kit. It loses money when sold through a pregão.

At the time of writing ACOLHE has none of these:
- a CNPJ;
- a bid;
- a customer;
- a supplier account;
- a quote from anyone.

§12 describes one measurement that would settle whether the business can work, and the pass mark it has to clear. The measurement uses data already in the repo.

### 0.1 The business model canvas

The canvas below describes the business as it is designed. The tags show which parts are measured and which are still hopes.

| Block | Content | Status |
|---|---|---|
| **Customer segments** | Municipal social-assistance secretarias and their Fundos (FMAS/FMS), which buy newborn kits as a *benefício eventual*. 16–18% of kit editais are published by an órgão whose name contains "FUNDO" [C]. This is a name match only; it does not establish that the Fundo is the legal buyer. About 98% of kit tenders **by count** are municipal [C]. Share by **value** has not been measured, and it is well below 98% once state central purchases are counted. 654 distinct municipalities had a kit tender in the last 12 months, all spheres (646 in the municipal sphere) [C, floor]. At least 1.124 municipalities (20,2%) have a kit edital on PNCP for 2022–2026 [C, Sample R floor]. **Target: the ~139 open dispensa avisos a year** [C]. They sit under the R$65.492,11 legal ceiling [M] and are usually 200 kits or fewer. The other 133 of the 272 dispensas are atos of direct award, with no proposal window. | Demand side: measured (floor) |
| **Value proposition** | A kit that conforms to the edital, delivered to the buyer's address within the call-off window and invoiced correctly (NF-e carrying the empenho number), with every certidão current, so the buyer's processing never stalls. It is sold through the fastest legal mechanism, at or below the buyer's own estimate. | Designed; not yet delivered to anyone |
| **Channels** | *Discovery:* PNCP, read daily by the system. *Selling:* only through the bidding platforms (Compras.gov.br/SICAF, BLL, BNC, Portal de Compras Públicas, Licitanet). *Delivery:* an LTL carrier or parcel services (Correios PAC, or cheaper routes through Melhor Envio) from SP to the buyer's address. | Discovery built. Selling not started. Delivery priced to 8 capitals only. |
| **Customer relationships** | Impersonal and transactional, with no sales calls. Her reputation builds through atestados and a clean delivery record. 33 contact rows (30 municipalities) are staged for **research** calls. None has been made. Whether research calls fit her "never phone to sell" rule is her decision [M]. | Deliberately minimal |
| **Revenue streams** | One-off supply contracts, invoiced per empenho. Median dispensa: **R$342,05 per kit** (pooled; R$327,00 once two data artefacts are removed, §2), **100 kits**, **R$40.100** revenue [C, n=52]. On the 19 open avisos alone: R$236,72 per kit and 120 kits [C, n=19]. No contract can exceed R$65.492,11 [M]. Written payment terms have a median of 30 days [C]. How fast buyers actually pay is **unmeasured**. | Price measured. Receipts not measured. |
| **Key activities** | Daily scan and selection. Reading editais and bidding: a budget of ≤0,6 h per bid [A], from the operating plan (BOS §6), unsourced and not measured. Buying from SP wholesalers, then assembling, storing and shipping: a budget of ≤8 h per won order [A], the C9 budget, not measured. Invoicing and chasing the atesto. Reissuing certidões (CRF/FGTS every 25 days). | Loop designed; not wired (§6, §7) |
| **Key resources** | The scanner and its data (built). Her 87 h a month (stated). Working capital: **null** in config. The written plan says R$15.600 [U]. The only budget she has recorded is **US$500–2.500 = R$2.579–12.894, non-reloading** [M, COMPANY_SETUP]. Space at home: a 100-kit lot in the assumed 60×40×40 box is **about 9,6 m³** [C]. The e-CNPJ and certidões (not obtained), an atestado (none yet), and the bid log (**0 rows**). | Mostly missing |
| **Key partners** | SP wholesale catalogues: Emilio supplies 11 of the 16 priced lines [M], and nobody has been contacted. For LTL, one carrier's **published** referencial table (STC Transportes, Guarulhos/SP to CE); it is not a quote [M rates]. Correios PAC and Melhor Envio, used at public calculator rates [M]. Bag/silk factories and a co-packer, **none quoted**: none of the 20 co-packing providers actually read publishes a per-kit price, and 4 more sites could not be read [M]. A contador. A bank (Cora). The bidding platforms. | Identified; nobody contacted |
| **Cost structure** | *Variable:* kit materials (**unmeasured for any dispensa kit**). Parcel freight per 60×40×40 box to 8 capitals [M], R$88,09–188,40 depending on route (§4c). LTL R$53,99/kit for 100 kits to the Fortaleza capital tier [C, published table]. Assembly: self-pack time never measured, and no co-packer price. Simples DAS: 4,00% effective at R$180k, rising [C]. Platform fees [M]: Compras.gov.br R$0; BLL 1,5% of the adjudicated lote, only on a win, capped at R$600; BNC R$118,80 per proposal, win or lose; PCP R$129 per process or R$165 per month. *Fixed:* R$196–473 per month [C]. *One-time:* R$218,99–1.012,89 [C]. | Variable cost is the missing half of the business |

**What the canvas shows.** The right side of the canvas (customers, channels, revenue) is measured, and it looks good. The left side (partners, activities, resources, costs) is largely unknown, and that is the side that decides the margin.

---

## 1. The market, measured

The source is 4.333 PNCP records pulled on 2026-09-21. 2.044 of them pass the scanner's own kit filter [C, re-run 2026-09-22 from `data/market/tenders.json`]. **These figures are floors, not a census.** The harvest is full-text and ranked by relevance (§10).

| | Value | Tag |
|---|---|---|
| Kit tenders published in the last 12 months (from 2025-09-22) | **786** | C |
| …of which dispensa | **272** (35%): 139 are avisos open for proposals, and 133 are "Ato que autoriza a Contratação Direta" (direct awards with no proposal window) | C |
| …of which pregão eletrônico / pregão presencial | 491 / 11 | C |
| …of which inexigibilidade / other | 9 / 3 | C |
| Dispensa share, all years 2021–26 | 711 / 2.044 = 34,8% | C |
| Complete 12-month census for one search phrase ("kit enxoval", Window W) | 442 editais, 372 municipalities, 148 dispensas (33,5%) | C |
| Municipalities with a kit tender, last 12 months | **654** across all spheres (646 in the municipal sphere) | C |
| Municipalities with at least one kit edital | At least 1.124 (20,2%, Sample R, 2022–2026). The current harvest, pooled over 2021–26, gives 1.255 in the municipal sphere (22,5% of 5.571). Both are cumulative multi-year floors, not annual rates. | C |
| Municipalities with more than one kit edital | 38,4% (432/1.124, Sample R) [floor]. This is not a clean repeat-purchase rate: about a quarter of the repeats fall inside a single calendar year, which suggests re-published, deserted or split tenders. | C |
| Contract value measured, 12 months | R$13,78 mi across 202 contracts. **A hard floor and a large undercount.** | C |

**"Bought" or "published"? A change from the fact sheet, flagged.** Earlier versions and the fact sheet describe the ≥1.124 as municipalities that "have bought". Strictly, it counts municipalities that **published** a kit edital. Only 717 of them (12,9%) have an edital with a result flagged, which is the closest proxy for a purchase [C, Sample R]. The floor is still valid as a count of interested buyers. It is not a count of completed purchases.

**About Window W.** Its source rows are held in the session scratchpad, not in the repo, so it is CALCULATED, not MEASURED. The pull may miss some rows: the fact sheet bounds the shortfall at ~40–57. A re-pull on 2026-09-22 reported 51 more editais, all published Apr–Sep 2026. That re-pull is also uncommitted, so it is [U] and is not used below. If it is confirmed, the 2026 seasonal and election-year figures below would rise. Of the 148 dispensas, 77 were avisos and 71 were atos. The regex also keeps some items that are not newborn kits, such as mattresses, hospital linen and furniture.

**The "ceiling" on the market is neither an estimate nor a ceiling.** `demanda_publica.md` computes R$88,8–246,2 mi a year of in-kind spending [A]. Including IBGE's "Sem rendimento" income class, which the file omits, moves this to R$113,1–270,5 mi [C, on assumed coverage]. The source file itself calls two of its assumptions false. Do not quote either range as the size of the market.

**Geography, last 12 months:** SP 91 · MG 90 · BA 74 · PR 67 · GO 45 · MA 42 · PA 37 · PE 36. No state is above about 12% [C]. This is a national market served electronically, not a local one. Freight transit has been measured for only 9 UFs, which limits which tenders she can bid (§6.3).

**Seasonality is mild** [C; Window W, one year, one search phrase]:
- January is the trough (20 editais) and March the peak (57). The other months run 32–49.
- March–August runs at about **1,4 times** December–January.
- The relevance-ranked harvest shows about 2 times. Its sampling inflates that figure, so do not use it.

**The 2026 election year shows a −2% change**: 38,7 → 37,9 editais a month [C, Window W]. That is one search phrase and one year, with no non-election baseline, so it is not a measured election effect. Read it as "no large drop visible".

**No supplier dominates the market** [C, on 463 genuine kit contracts out of 536 pulled, 239 CNPJ roots; source data in the scratchpad only]:
- **HHI 181** by count and 278 by value, far below the threshold for a concentrated market.
- **72,8% of suppliers hold exactly one contract.**
- 86% of buyer–supplier pairs occurred only once.

Measured the same way on the descent results (per line won), HHI is 130 and 31% of suppliers won a single line [C]. By winner size on per-item result lines, the counts are ME 677 · EPP 331 · Demais 245 [M]. These count lines, not firms, and a few very active firms dominate them. Small firms do win.

**Frequent winners exist, and they are not beginners.** Brink Mobil has 41 contracts and AMA has 31. CONDAFE is an EPP by *porte*, but it holds 47 PNCP contracts across 16 states [C].

---

## 2. The strategy, and the dispensa finding

**The purchase mechanism affects the price more than anything else measured.**

The base is 93 priced tenders out of 220 that were descended to results. They were taken most-recent-first, from tenders published 2026-03-06 to 2026-09-17. **This is not a random sample** [C, re-run].

| | n | Median clearing (homologado ÷ estimado) | Median price per kit | Median lot |
|---|---|---|---|---|
| **Dispensa, all** | 52 | **99%** | **R$342,05** (PER_ITEM R$311,87, n=42; LOTE R$492,88, n=10) | 100 kits |
| …atos (direct award, not biddable) | 33 | 100% | R$386,10 (n=31, artefacts excluded) | 100 |
| …**avisos (open for proposals)** | 19 | **86,8%** | **R$236,72** | 120 |
| Pregão eletrônico | 40 | **65%** | R$382,44 (PER_ITEM R$418,90, n=36; LOTE R$295,68, n=4) | — |

*The aviso/ato split and its prices come from a re-run on the same file [C]. n=19 is small.*

How the results split [C]:
- **Dispensas:** 38% cleared at exactly the estimate and 62% below it. The dispensas that discounted have a median of about 89%. Most of the exact-100% cases are atos.
- **Pregões:** none cleared at exactly 100%, but 5 of 40 cleared at 95% or more. Araraquara reached 99,996%.

**Checks on the finding:**
- *Could dispensas be recording the accepted price as the estimate?* If so, all of them would sit at exactly 1,0. Only 38% do.
- *Are these dispensas she could bid?* Only the 19 avisos. They clear at 86,8% against 64,7% for pregão eletrônico, so her usable advantage is about **22 points, not 34**.
- *Is it really a lot-size effect?* Size and mechanism overlap: dispensas are mostly ≤200 kits and pregões mostly >200. The gap still holds within the two middle size bands, where both mechanisms occur. Those cells have n=8–18, and together they hold 47 tenders. The finding is strong enough to act on, but it comes from one pull.

**Data artefacts in the dispensa sample.** Two of the 42 PER_ITEM dispensas, Pedro Laurentino/PI and Ribeira do Piauí/PI, record the lot total as a unit price (one line, quantity 1). They show R$39.000 and R$31.439 "per kit". Removing them gives:
- a dispensa median of **R$327,00** (n=50) instead of R$342,05 [C, re-run];
- a PER_ITEM median of R$297,30 (n=40).

`data/typical_kit/tenders.json` holds all 42, so **40 are usable**. Teresina/PI is recorded as a dispensa for 520 kits at R$273.052. That is above both the R$65.492,11 ceiling and the 200-kit band. Either it rests on a different legal basis or it is a data error; which is unknown [U]. Exclude it from any "typical dispensa" work.

**Three large lote-único pregões cluster in the mid-70s:** Itaquaquecetuba 75,42%, RS Mãe Gaúcha 77,37% and MG Filhos de Minas 74,14% [M, n=3]. These are lots of 5.000 to 80.000 kits, and two of them are state central purchases. They say nothing about small lots.

> **The strategy: bid dispensa avisos.** There are about 139 a year. They clear about 22 points closer to the buyer's estimate than pregões [C]. Pregões are a fallback, not the plan.
>
> **What this does not show:** that dispensa kits are profitable. The finding is about price relative to the estimate. The cost of those kits has never been measured (§4c).

**How big a dispensa is** [C]:
- Median lot 100 kits. Median revenue **R$40.100** (price per kit × lot size, n=52). Summing the recorded homologated totals gives a lower median, R$26.658,50, because in half the PER_ITEM dispensas the lines have different quantities. The two bases are not interchangeable.
- Other "median contract" figures in the repo measure other things: R$30.848 (kit dispensas in descents, n=80) and R$17.092 (PNCP contracts, all modalities, n=463). Do not swap them for each other.
- Pooled across both mechanisms, the ≤200-kit median is also R$382,44. That it equals the pregão median is a coincidence. It is not a dispensa price.
- **Hard cap:** the 2026 dispensa ceiling is **R$65.492,11** per contract (Decreto 12.807/2025) [M].

**The price of this strategy is speed.** Rio Branco do Sul/PR had a 3,0-day window [M]. The kit windows seen on 15/09 ran 3–14 days [M]. Across the 139 avisos of the last 12 months, the window from `data_inicio_vigencia` to `data_fim_vigencia` (read as the proposal window) has a **median of about 5 days** (p25 3, p75 6, maximum 14,7); **41 (29%) close within 3 days and 60 (43%) within 4** [C, `data/market/tenders.json`, re-run 2026-09-23]. Reading those two fields as the proposal window is an interpretation of PNCP's field names. The one workbook the system has ever produced (2026-09-19) came out four days late and missed that Rio Branco do Sul dispensa [M]. A late scan does not lose a random slice of the market. It loses the short-window dispensas, which pay best.

**The atestado is not waived in dispensas.** An earlier version said dispensas "usually do not ask". That was never counted [U], and 7 of 8 real editais tested ask for a qualitative atestado. The legal waiver (art. 70 III) applies only below R$16.373,03 or for *entrega imediata*, and the buyer may still choose not to use it [M]. Art. 67 does not restrict who may issue an atestado, so a declaration from a private buyer reads as valid [M]. Whether buyers accept one in practice is [U].

**Plan on one private sale to get the first atestado.** Here is what the repo says about it:
- **Who buys:** any legal entity, such as a creche, an ONG, a maternidade, or a company that gives kits to employees.
- **How many kits:** "a few".
- **Budget:** about R$500 [A, RISK_REGISTER #11].
- **What she needs back:** a signed declaration on the buyer's letterhead, with the buyer's CNPJ.
- **When:** the sale has to be invoiced by ACOLHE, so it comes after the CNPJ and before the first bid that asks for an atestado.

Still open: who the buyer is, whether the sale makes or loses money, and how long it takes.

---

## 3. The kit, and what it costs

### 3.1 Kits vary a lot

"The kit" is not one product. Two examples:
- **Caseiros/RS** bought a dispensa kit at R$323,50. It is a bag plus soap, cloths, a gel pack, pads, cream, a towel, alcohol gel and cotton buds [M, `results.json`].
- **Itaquaquecetuba's kit** is 17 specified lines, including a branded backpack and a printed bathtub [M].

The two kits share almost nothing. Across dispensas the price per kit runs from about R$208 (p25) to about R$515 (p75) [C]. That range mostly reflects **different contents**, not different prices for the same product.

### 3.2 The one kit that has been costed: Itaquaquecetuba PE 90088/2025 (SRP)

| | Value | Tag |
|---|---|---|
| Quantity | 5.000 kits (3.750 open competition + 1.250 ME/EPP quota) | M |
| Buyer's estimate | R$476,05 per kit. The 17 per-line estimates sum to it exactly. | M |
| Award | R$359,05 per kit (75,42%), R$1.795.250, to CONDAFE (EPP). One price for the whole lote; the winner's per-line prices are not published. | M |
| Mochila (backpack) | Buyer's estimate R$98,51 [M]. The R$74,30 figure is a pro-rata allocation (98,51 × 0,7542) [A], not a realised price. | M / A |
| **Materials, 16 of 17 lines (mochila excluded)** | **R$250,98**, at catalogue list prices on 2026-09-21 (`data/cost_table_v2.csv`) | C |
| **Not in R$250,98** | The mochila. Printing the tub's vinyl, R$1,86–2,78 per kit [C], plus applying it, which is unpriced. Freight to Itaquaquecetuba, never quoted. Assembly/co-packing, with no price anywhere. Taxes. | M / C |
| Lines under the buyer's own per-line estimate | 16 of 16. The towel is the tightest, R$0,21 under. Being under the estimate is not a test of competitiveness, because this lote cleared at 75,42%. | C |
| Lines above a uniform 75,42% allocation | 5 lines, all negative: toalha com capuz −9,58, banheira 22 L −6,83, sabonete −3,12, fralda −1,88, shampoo −1,41. Total −R$22,82, 72% of it from the towel and the tub. These are not the winner's prices. | A (allocation) |

**Spec conformity** [M]:
- 8 of the 11 lines with a colour requirement are priced in a colour the edital does not allow.
- No 22 L tub in amarelo/verde was found in stock anywhere.
- No "pelo alto" 90×110 blanket was found.

**Supplier concentration** [M / C]:
- Emilio supplies 11 of the 16 lines, 65,7% of the materials value.
- 15 of the 16 lines come from SP suppliers.
- Nobody was contacted. All prices are list prices, with no volume quotes.

**Branding** [M, edital]:
- The backpack carries four silk-screen artworks.
- The tub ships with CMYK vinyl on three faces.
- The R$52,27 catalogue bag does not qualify: it is already printed, and it is not the made-to-order article in the spec. The spec bag is unpriced, so **carry R$98,51 as a placeholder** [A].
- One bag supplier publishes a **20-working-day lead time**, against a 20-day delivery term [M]. **The printed bag is the item that takes longest to get.**

**The old cost figures are void for this kit.** R$198,78 was priced against the wrong spec: six to nine articles failed the written spec, depending on how the pagão is counted. The R$176,32 before it counted one diaper where the spec means a pack. Neither is the cost of this kit or of any identified kit.

### 3.3 Step 0: the verdict

The gate was written in advance (git 6cc7938) [M]:
- **R$200 or less** of materials: build everything.
- **R$200–230:** open a supplier account first.
- **Above R$230:** stop.

**R$250,98 is above R$230, so by its own rule the gate says STOP for the Itaquaquecetuba spec.** The gate cannot be decided finally on the merits, because four inputs are still unquoted: the mochila, the vinyl application, freight and assembly. All four can only make the cost worse.

**Do not build the business on the Itaquaquecetuba kit.** It loses money on the pregão where it was actually bought, and ACOLHE could not serve that scale (§4a). Step 0 says nothing about a typical dispensa kit, because none has been costed.

---

## 4. Unit economics: three cases that must be kept apart

**First, the old headline is withdrawn.** The previous version showed "R$382,44 price / R$252,77 goods + LTL / 33,9% gross" (and 29,7% net). That comparison does not hold, for three reasons:
- **R$252,77** is R$198,78 (the old wrong-spec materials) plus R$53,99 (LTL SP→Fortaleza, 100 kits) [C: 198,78 + 53,99 = 252,77]. It is not the cost of any real kit.
- **R$382,44** is the pregão median (n=40), not a dispensa price.
- The price side is a median across *other municipalities' kits*, whose contents were never costed.

So 33,9% gross, 29,7% net and 26,1% at R$342,05 are arithmetic on numbers that describe different things. **Retire all of them.** A valid comparison needs the same kit and the same spec on both sides. There are three cases below, and only the first is fully grounded.

### (a) Itaquaquecetuba spec, sold by pregão at its real price (R$359,05)

| | Per kit | Tag |
|---|---|---|
| Award (17 lines, mochila included) | R$359,05 | M |
| − materials, 16 lines (mochila excluded) | R$250,98 | C |
| = difference | R$108,07 (30,1%). **Not a margin:** a 16-line cost taken from a 17-line price. | C |
| − mochila at the buyer's estimate (R$98,51) | **R$9,56 left (2,7%)** | C (mochila A) |
| − mochila at the allocated R$74,30 instead | R$33,77 left | A |
| Simples tax alone | About R$23 (6,41% effective, on an assumed RBT12 of R$449k, the quota only) to R$34 per kit (9,45%, the full award). Even at the 4,00% floor rate it is R$14,36 [C: 359,05 × 0,04]. | C, on an assumed RBT12 |

Both "left" figures are before vinyl and its application, freight, assembly and tax.

**Verdict: a loss, or at best breakeven, before freight and assembly.** Tax alone, at any rate, is more than the R$9,56 left. The commit's −7,1% gross figure points the same way. That commit did not record its inputs. Working backwards gives an implied cost of about R$384,5 per kit, of unknown composition [U].

**ACOLHE also cannot physically deliver it today** [C / M]:
- The 1.250-kit quota is 5,2 times the 240-kit self-pack ceiling [A], and about 15,6 times the 80 kits the risk register recommends.
- No co-packer has quoted.
- The bag's lead time (20 working days) is longer than the 20-day delivery term.
- Materials alone cost R$313.725 for the quota [C], or R$436.862 with the mochila at estimate [A]. Her recorded budget is R$2.579–12.894.
- Storing 1.250 kits in a 60×40×40 box would take about 120 m³ [C]. That rules out working from home.

### (b) The same spec on a dispensa: never observed

| | Per kit | Tag |
|---|---|---|
| 99% of R$476,05 | R$471,29 | C, on an ASSUMED transfer of the dispensa ratio to a pregão's estimate |
| − materials + mochila at estimate (250,98 + 98,51) | R$349,49 | C (mochila A) |
| **= left before vinyl, application, freight, assembly and tax** | **R$121,80 (25,8%)**. Not a margin. | C |

At the 86,8% aviso median, the same arithmetic leaves R$63,72 [C: 413,21 − 349,49].

- The dispensa ceiling caps such a sale at about 137 kits. At that size, silk-screen setup (R$720–1.500 [A]) adds about R$5–11 per kit.
- **No dispensa with this spec, or with this estimate, exists in the data.** This whole case is [A].
- The commit's "+18,4% gross / ~14,4% net" is this case with CE freight added. It is a hypothesis, not a result.

### (c) A typical dispensa kit: the case the strategy depends on

| | Value | Tag |
|---|---|---|
| Price per kit, median | R$342,05 pooled (R$327,00 without the two artefacts). Open avisos: **R$236,72** (n=19). | C |
| Clearing | 99% pooled. Open avisos: 86,8%. | C |
| Lot / revenue, median | 100 kits / R$40.100 (avisos: 120 kits) | C |
| **Cost per kit** | **UNMEASURED.** No materials list has been built for any dispensa kit. | — |
| **Margin** | **Cannot be stated.** Any figure would be [A]. | — |

**Freight shows how much this unknown matters.** All figures are per kit, for one 60×40×40 box (billed at 16 kg cubic weight), to capital CEPs only [M, `data/freight.md`, public calculators, 2026-09-19]:

| Route | R$ per kit | Notes |
|---|---|---|
| Correios PAC, over the counter | 116,60 (BH) to 188,40 | Northeast capitals R$132,90–188,40 |
| PAC via Melhor Envio | 102,61–164,71 | No contract, no minimum |
| Two-box split (tub box + soft goods), PAC | 94,20–147,80 | Assumes the tub box really is 60×40×20 [U] |
| LATAM Cargo éFácil (air) | 88,09–116,48 | NE capitals except Belém. Interior CEPs [U]. |
| LTL, STC published table, 100 kits, Fortaleza tier | 53,99 | Not a quote. CE interior tiers R$59,57–93,31. |

Even the cheapest parcel route is 26–34% of a R$342 kit, and 37–49% of the R$236,72 aviso median [C, illustrative]. The 60×40×40 box is sized for Itaquaquecetuba's 22 L tub. A dispensa kit without a tub could ship much smaller: a 40×30×30 box cuts PAC by 57% [M]. **Box size is therefore part of the cost to be measured.** Freight to real delivery addresses (interior CEPs) has not been measured.

**Storage.** A 100-kit lot in the 60×40×40 box takes about **9,6 m³** [C: 100 × 0,096 m³, on an assumed box]. It would sit in her home between receipt from suppliers and pickup by the carrier. A smaller kit needs less space. Whether she has the room is not recorded.

---

## 5. Scale and capital

### 5.1 The target: one win a week

One win a week (52 a year) is an ASSUMED target. It implies these win rates:
- **19% of all 272 dispensas** [C: 52/272].
- **37,4% of the 139 avisos she could actually bid** [C: 52/139]. This is before any screening.

Screening cuts the pool further:
- **53 of the 139 avisos (38%) are in UFs with no measured transit** [C]. For those, rule 5 can return only VERIFICAR (§6.3).
- Across all 272 dispensas, the figure is 110 [C].

No win rate has been measured, and **only bidding can measure it**. That is why the bid log is the most valuable thing the business will own. It has zero rows.

**Hours per month at one win a week: about 48 of her 87, as a lower bound** [C, on ASSUMED budgets]:
- 52 wins × ≤8 h ÷ 12 ≈ 35 h.
- Plus bidding: 272 bids × ≤0,6 h ÷ 12 ≈ 13,6 h.

The 48 hours leave out several things: screening and reading VERIFICAR editais, live pregão sessions, certidões, invoicing, storage handling, and rejections. The risk register notes two further pressures:
- **G1:** reading VERIFICAR editais could fill the 87 hours on its own.
- **C2:** 8 hours per order is optimistic at 5–8 minutes per kit.

### 5.2 The formula

```
lots per year   = (capital ÷ cash per lot) × (365 ÷ float days)
lots in flight  = wins per year × float days ÷ 365
capital needed  = lots in flight × cash per lot
```

These are identities [C]. Their inputs:

| Input | Value | Tag |
|---|---|---|
| Capital | `capital.available_brl` = **null**. The written plan says R$15.600 [U]. Her recorded budget is **R$2.579–12.894**, non-reloading [M, COMPANY_SETUP, US$500–2.500 at PTAX 18/09/2026]. | U / M |
| Float (days from paying suppliers to being paid) | `capital.yaml` says **34 days** (pay the supplier on day 11, paid on day 45) [A, config value]. The operating plan models 45. The risk register recommends planning cash for payment on **day 75**. | A |
| Cash per lot | Cost of goods + freight + assembly for the lot | **unmeasured** (§4c) |

**How the float changes things, independent of cost** [C]:

| Float | Capital turns per year (365 ÷ float) | Lots in flight at one a week |
|---|---|---|
| 75 days (the register's planning case) | 4,9 | 10,7 |
| 45 days (the operating plan) | 8,1 | 6,4 |
| 34 days (config) | 10,7 | 4,8 |

**What her money buys.** The setup costs of R$218,99–1.012,89 come out of it first.

| Capital | Left after setup | Cash available per kit, one 100-kit lot |
|---|---|---|
| R$12.894 (top of her budget) | R$11.881–12.675 | **≤R$119–127** |
| R$2.579 (bottom of her budget) | R$1.566–2.360 | **≤R$16–24**, which no kit meets |
| R$15.600 (the plan) [U] | — | ≤R$156 |

[C] Monthly fixed costs (R$196–473) come out of the same money. Whether any aviso kit (median price R$236,72) can be bought and shipped for about R$120 is exactly what §12 move 1 measures. **At any of these capital figures, one win a week is not fundable**: at a 45-day float it needs 6,4 lots in flight.

### 5.3 Why the float, not capital, is the lever

Capital and float enter the formula in the same way: halving the float does exactly what doubling the capital does. The difference is price. Capital costs money, while the float can be shortened for free, through supplier terms, current certidões and a clean NF-e.

**None of those terms has been obtained** [M]:
- None of the priced suppliers offers terms.
- MaxQualy publishes a 7-day boleto, for hygiene lines only.
- Brascol offers a boleto parcelado, but only to buyers with certain CNAEs.
- Neither has been tested.

No supplier offers 28-day terms. The earlier "45 → 6 days" claim follows only from the 34-day base.

**The previous capital/net table is withdrawn as a forecast** (R$22.812 … R$98.850; R$6.202 … R$24.834/month). It rests on the void R$382,44 / R$252,77 pair, 61 kits, a 45-day float, zero platform fee and R$6.000 a year of fixed cost. Treat it as illustrative. The "15 wins, ~R$93k" year-one ramp is an aspiration, not a projection.

### 5.4 When the tax leaves, relative to the cash

This is a worked example, with the dates as [A]:
- The NF-e travels with the goods, so it is issued at dispatch.
- The Simples DAS on that revenue falls due on the **20th of the following month** (LC 123 art. 21 III; not read at source in this repo [U]).

| | Empenho early in the month (1 Mar) | Empenho late in the month (25 Mar) |
|---|---|---|
| NF-e issued at dispatch | ~4 Mar | ~28 Mar |
| DAS due | 20 Apr (day 50) | 20 Apr (day 26) |
| Ordem bancária, typical 40–55 d | 10–25 Apr | 4–19 May |
| Result | Tax and cash arrive at about the same time | **The DAS leaves 2–4 weeks before the cash** |

On a R$40.100 lot at 4,00%, the DAS is R$1.604 [C], and it has to be held in cash in addition to the lot. Simples allows cash-basis recognition of revenue, which would remove this gap. Whether ACOLHE should elect it is **an open question for the contador**; the repo has not examined it.

---

## 6. How the business runs: the loop

This section describes the **intended** operation, with what actually works today marked. Days are calendar days unless marked d.u. (*dias úteis*, working days).

### 6.1 Every morning (automated; her review time is not measured)

| Step | What happens | Wired today? |
|---|---|---|
| 1. Harvest | Pull yesterday's PNCP publications. Family A finds tenders; Family B reads their items. | Yes, but only when run by hand |
| 2. Filter | Keep kit tenders and drop closed windows. | Yes |
| 3. Descend | Read the item lists and classify each tender as PER_ITEM or LOTE. | Yes |
| 4. Admit | Run the 13 admission rules (10 can reject, 3 only flag). | **No** |
| 5. Screen the buyer | SICONFI payment record, standing in for rule 6. Only a REJECT blocks a tender. About 45% of small municípios can be screened (27/60, 95% CI ~32–58%) [M]; a second sample of 200 gave 34,5%, inside that interval. | Partly |
| 6. Price | Materials + measured freight + tax, against the estimate | **No** |
| 7. Report | Portuguese workbook: LICITAR / VERIFICAR / NÃO LICITAR | Yes, but it can only say VERIFICAR or NÃO LICITAR |
| 8. Heartbeat | Warn her if the job did not run. | **No** |

**Her part:** open the workbook and look only at LICITAR rows. Until steps 4 and 6 are wired, every candidate is VERIFICAR. At about an hour per candidate, four candidates a day would use all 87 h a month [estimate, RISK_REGISTER G1].

### 6.2 For each bid (≤0,6 h [A]: an unsourced budget from the operating plan, not measured)

1. Read the edital. Check:
   - the **delivery clause**: address, whether delivery is per household, and the call-off window;
   - the **atestado** requirement;
   - the habilitação list;
   - the platform.
2. Price the kit **line by line against this edital's own spec**, never against a median.
3. Check the colours, sizes and volumes the spec demands (§3.2).
4. Submit on the platform.
   - Habilitação documents are demanded only from the winner.
   - An ME has **5 d.u.** to fix fiscal or labour problems. The buyer may extend this by another 5 at its discretion, so plan on 5.
   - An SRP is not "pronta entrega", so the ME balanço waiver does not protect her there (SICAF FAQ Q18) [M]. How often SRP editais actually demand a balanço has not been counted in the repo; a working note puts it at 3 of 7 [U].
5. Handle any **impugnação or recurso**. The time this takes is not budgeted anywhere.
6. For a pregão (the fallback), attend the **live lance session** at a fixed hour (09:00 Brasília in Irecê and Itaquaquecetuba). Overlapping sessions cannot both be attended [M, RISK_REGISTER G2]. Session time is not in any hour budget.
7. **Record the bid in the bid log:** tender, price, estimate, outcome, winning price.

### 6.3 For each won order: order to cash (≤8 h [A], the C9 budget, not measured)

The model below comes from **7 documents: pregão/SRP editais plus one termo de referência (Belterra/PA)** [M]. **No dispensa's order-to-cash has been traced end to end.** For a dispensa, a single order is assumed, with the empenho acting as the contract [A].

The payment clauses were measured separately in `data/payment_terms.csv`:
- 19 usable dispensa rows (18 buyers) and 8 pregão rows, after 4 mis-parsed rows were corrected.
- Median **30 days** for both mechanisms.
- These are written maxima, not observed payments.
- Only 30 of the 60 editais were readable.

| Stage | What she does | Days |
|---|---|---|
| Homologação → sign | Confirm the award. Sign within 5 dias or 5 d.u. | Homologação → ARP: days to weeks, not measured [A]. Under SRP, first empenho: **unbounded** (art. 83). |
| **Nota de empenho** | Buy nothing without it. Check the CNPJ, items, quantities and value. | |
| Buy + assemble | Order from SP wholesalers and self-pack. The self-pack ceiling is **unknown (60–240 kits)**; plan on 80 until it is timed [A]. No co-packer price exists. | ≈3 days [A] |
| Store | Hold the lot at home until pickup: about 9,6 m³ per 100 kits [C]. | |
| Ship | LTL or parcel to the buyer's address. PAC to capitals takes 5–8 d.u. [M]; interior CEPs are not measured. | Call-off windows run from *imediato* to 20 days [M] |
| Invoice | NF-e to the exact CNPJ on the empenho, carrying the empenho, order and ARP numbers. | A defect restarts the payment clock. |
| Recebimento → atesto | Get dated proof of delivery and chase the atesto in writing. 5 of 7 documents set no deadline for it. | 5–8 d.u. where set; otherwise unbounded |
| **Empenho → ordem bancária** | | Best 34 d [C]. **Typical 40–55 d** [A: atesto lag assumed]. Worst bounded 69 d. SJP and Irecê are unbounded. |
| **Homologação → cash** | | Single order: **~40 d best, 45–75 d typical** [C]. Under SRP: **unbounded**. |

**If goods are rejected** [M, ORDER_TO_CASH]:
- Replacement windows are **24 h** (Coronel Xavier Chaves; Bocaiúva ARP), **48 h** (Bocaiúva, Belterra) and **5 days** (Agrolândia).
- A rejection restarts the payment clock.
- From SP, PAC cannot meet a 24–48 h window outside SP.
- SEDEX costs R$226,80–516,40 per box to the measured capitals, 1–4 d.u. [M].
- The practical options are to ship spare kits with the order, or to accept the late-delivery fine. What either costs has not been estimated.

**Delivery rules that decide whether a tender can be bid:**
- The days she needs are buy/assemble (3 d [A]) plus PAC transit [M]. By UF: **SP 4**, MG 8, BA/PE 9, CE/RN 10, MA/SE/PA 11.
- A call-off of 5 days or less can therefore be met only in SP [C]. The 5-day cut-off itself is a policy threshold.
- **18 UFs have no measured transit** (`config/ufs.yaml`), including PR (67 kit tenders in 12 months) and GO (45). Rule 5 returns VERIFICAR, never PASS, for them. Measuring transit to those UFs is cheap and unlocks 38% of the avisos.
- "Buy only after winning" works only where the clause allows about 8–11 d.u. or more, depending on the UF. Otherwise she must hold stock at her own risk or skip the tender.

**Penalties** [M]:
- **Refusing an empenho under an ARP** is total default (art. 90 §5). Bom Sucesso and Bocaiúva set a 20% fine for it. The law allows 0,5–30% (art. 156 §3).
- **Late delivery:** daily fines of 0,3% (Irecê, São João do Paraíso) to 2% (Coronel Xavier Chaves) of the value. Bom Sucesso adds a **one-off 5% on the first day** of delay; that 5% is not a daily rate.
- **Under an SRP** she is bound to the registered price for up to 24 months (art. 84), and the buyer is not obliged to buy.

### 6.4 Certidões

Reissue the CRF/FGTS every 25 days. It is valid for 30 days and can be renewed from the 5th day before it expires [M]. The 25-day cycle is an operating choice, not a legal deadline. The cartão CNPJ and the JUCESP simplificada are renewed with it by choice. The 180-day certidões are reissued about every 150 days. PGE-SP and the TJSP falência certidão follow the validity printed on the document [U].

The usual count is **five regularity certidões**: federal RFB/PGFN, state, municipal, CRF/FGTS and CNDT [M]. In São Paulo the state leg is two documents (SEFAZ-SP and PGE-SP), and editais may add the TJSP falência certidão. They are checked at signature and at payment. They are also checked at the empenho where the edital says so: explicitly in 1 of the 7 O2C documents (Bom Sucesso 21.2). **Plan as if every empenho checks them. A lapsed certidão holds up every payment.**

### 6.5 Monthly and yearly

- **Monthly:** pay the DAS by the 20th (§5.4) and pay the contador.
- **Every December:** make sure every delivery has its **atesto before 31/12**. Un-attested goods become *restos a pagar não processados* and can be cancelled.
- **2028:** the municipal election year brings a budget cliff [A].

---

## 7. What exists, and what is not yet wired

**Built and tested (371 tests pass) [M]:**
- `harvest/` (Family A + B, daily driver)
- `parse/` (filters, SKU classification, delivery-clause reader)
- `screen/` (**13 rules**, the SICONFI screen, the certidão tracker)
- `price/`
- `report/`
- `log/` (bid-log code)
- `tools/` (market and niche analysis; `/api/search` is **research only, not a daily fallback**)

**Not wired, or wrong [M]:**
- **`harvest/run_daily.py` runs no admission rules and prices nothing.** It runs only the SICONFI check, and blocks only on REJECT. It can never say LICITAR.
- **Not scheduled anywhere and no heartbeat.** One workbook has ever been produced, on 2026-09-19, four days late.
- **Bid log:** nothing writes to it, nothing bridges the workbook to it, and `db/` is empty.
- **`price/margin.py`** uses OPENING_ANCHOR = 0,75 for every tender. The value comes from a handoff pool that is not in the repo, and it ignores the dispensa/pregão split.
- **The Simples table** stops at R$720k.
- **Rule 1 rejects every lote-único tender**, on an unsourced 36–63% band [U]. The measured 74–77% applies only to three large pregões.
- **Rule 5** returns VERIFICAR for the 18 UFs with no measured transit (§6.3).
- **`data/payment_terms.csv`:** at least 6–9 clauses are in dias úteis, but the flag reads False on every row (a parser bug).
- **`price/cost.py`:** the 45% account-tier discount is an inference, not a measurement.
- **The README is out of date:** it still says R$176,32, 12 rules and 280 tests.

**Documents:**
- `O_MERCADO.md` and `data/demanda_publica.md`: the market.
- `ITAQUAQUECETUBA_REAL.md` and `data/cost_table_v2.md`: the costed kit.
- `data/typical_kit/` (42 dispensas, 40 usable; 587 lines): the input for §12.
- `ORDER_TO_CASH.md`, `HABILITACAO.md`, `COMPANY_SETUP.md`, `LEGAL_FINDINGS.md`, `RISK_REGISTER.md`, `NICHOS.md`.
- `SUA_LISTA.md`. Where its numbers differ from this document, this document wins.

**Workbooks:**
- `ACOLHE_municipios.xlsx`: 33 rows, 30 municipalities, **nobody contacted**.
- `ACOLHE_deal_model.xlsx` and `ACOLHE_fornecedores.xlsx`.

---

## 8. Setup, and what it costs

| | Value | Tag |
|---|---|---|
| Legal form | SLU (a one-member limitada). No minimum capital. ME up to R$360k, EPP up to R$4,8M. MEI is not allowed. | M |
| One-time cost | R$218,99 (minimum path) to R$1.012,89 (conservative). The minimum path needs the gov.br signature to be accepted [U] and a Cora e-CNPJ voucher, which requires a CNH. | C |
| JUCESP fee | R$218,99, unavoidable | M |
| e-CNPJ | R$203–275 a year paid; the low end is a combo price, and standalone A1s run about R$220–275. **R$0 via Cora** for CNH holders, in the first year. | M |
| Monthly fixed cost | R$196–473 (R$2.352–5.676 a year). Whether the TFE applies at a home address is [U]. | C |
| Time to CNPJ | About 1 day 10 hours (SP, 2025 average) | M |
| Time until she can submit a bid | 5 / 10–15 / 30+ business days. Only the CNPJ leg is measured. | A |
| **Simples opt-in** | **Within 30 days of the last registration approval, and no more than 60 days after the CNPJ opens** (CGSN 140 art. 6 §5 I) [M]. Miss it and the company is outside the Simples until the January window, on Lucro Presumido per COMPANY_SETUP. Strictly, Presumido applies only if she elects it; otherwise the company is on Lucro Real [U]. **Open question:** a working note says Res. CGSN 183/2025 moved the option to the CNPJ inscription itself. This is not confirmed in the repo [U], so confirm it with the contador before opening. | M / U |
| Simples Anexo I effective rate | 4,00% at R$180k · 5,65% at R$360k · 6,73% at R$500k · 7,58% at R$720k | C |
| Platforms | Compras.gov/SICAF R$0 · BLL 1,5% of the lote (capped at R$600) · BNC R$118,80 per process · PCP R$129 per process or R$165 per month · Licitanet [U] | M |
| DIFAL on sales | R$0 for a Simples company (ADI 5469) | M |
| ICMS difference on inputs bought outside SP | About 6 points on goods bought from **non-SP** suppliers only, as coded | A |
| IRRF 1,2% withholding | Expected R$0 with the Anexo IV declaration. There is a risk a município withholds anyway, and no COSIT ruling covers the point. | U |
| Kitting treated as manufacturing (Anexo II + IPI) | Not yet asked. Worth **2–5 margin points** if it applies. | U |

**Sequencing:** do not open the company until §12 move 1 gives a go. Opening starts the Simples opt-in clock (on the 30/60 reading) and the monthly fixed costs.

---

## 9. What could kill it

1. **A typical dispensa kit may cost too much.** This is the whole margin question, and it is unmeasured (§4c). At her recorded budget, a 100-kit lot must cost no more than about R$120 per kit in cash (§5.2).
2. **A late scan.** Aviso windows have a median of about 5 days and 29% close within 3 [C]. Missing one is silent. The job is not scheduled and has no heartbeat.
3. **Delivery clauses and geography.** Call-offs of 5 days or less can be met only in SP. 18 UFs are unverifiable, and freight is 26–55% of a R$342 kit depending on route (§4c).
4. **Rejection.** A 24–48 h replacement window cannot be met from SP by parcel, and fines start on the first day of delay (§6.3).
5. **An SRP call-off she cannot serve.** Refusing is total default, with a 20% fine in two editais. Rule 13 is meant to refuse such tenders, but it is not wired.
6. **Capital and float.** Her recorded budget is R$2.579–12.894, config capital is null, and the plan's R$15.600 is unconfirmed. The DAS can leave before the cash (§5.4). No supplier gives terms.
7. **Spec conformity.** Catalogue items often fail the spec: 8 of 11 colour lines in §3.2.
8. **The first atestado.** 7 of 8 editais tested ask for one. It needs one private sale (~R$500 [A]).
9. **Supplier concentration.** Emilio accounts for 65,7% of the priced materials value and has never been contacted.
10. **No federal money.** The FNAS bars federal funds for *benefícios eventuais* [M].
11. **A shift to cash benefits.** CNAS Resolução 213/2025 reportedly says *"preferencialmente em pecúnia"* and gives councils one year to comply. The deadline is reported as **28/10/2026**, 36 days away [U]; other working notes put it at 29/10. The date rests on a publication date nobody has confirmed. The text was read only from a secondary copy (jari.rs.gov.br); the DOU original was never obtained.
12. **State programmes buying centrally.** RS (80.000 kits) and MG (38.760) are confirmed on PNCP [M]. PR (16.000) and MA (9.000) are [U]. Do not sum these.
13. **Falling births:** −15,5% from 2019 to 2024 [C].
14. **Election rules:** Lei 9.504 art. 73 §10 [M statute; its application to municipalities in 2026 is a reading]. The 2028 budget cliff [A].

---

## 10. What these numbers are not

- **Not a census.** Discovery is full-text and relevance-ranked. Even Window W may miss ~40–57 rows. The "600-row cap" was this repo's own page limit, not PNCP's.
- **Not random.** The 220 descended tenders were taken most-recent-first, and only 93 had prices.
- **Not large.** 52 dispensas (19 of them avisos) and 40 pregões carry the central finding. Within-band cells are n=8–18. It is one pull.
- **Not explained.** Nobody knows whether the 38% of dispensas that cleared at exactly 100% were contested. Most of them are atos.
- **Not one product.** Price medians are medians across **different kits**. Never set one against the cost of a single kit.
- **Not pooled.** Use R$342,05 (R$327,00 without artefacts) for dispensas and R$236,72 for avisos. R$382,44 is a pregão figure.
- **Not observed payments.** The 30-day median is the written maximum. Half the editais could not be read, some clauses are in dias úteis, and **no real payment has been observed.**
- **Not a margin.** Neither R$250,98 nor R$349,49 is the cost of anything ACOLHE plans to sell.
- **Not quotes.** Every price is a published list or calculator rate. No co-packer price exists (0 of 24 providers). An earlier "quoted R$5,00" was never a quote.
- **Not timed.** 2 minutes per kit, ≤0,6 h per bid and ≤8 h per order are all [A].
- **Windows read from field names.** The 5-day median reads PNCP's vigência start/end fields as the proposal window; no edital-by-edital check has been made.
- **Not committed.** HHI 181, Window W and its re-pull rest on scratchpad data, not the repo.
- **Not a market size.** R$13,78 mi is a floor. The "ceiling" is a scenario.

---

## 11. Where earlier versions were wrong

The corrections share one pattern: **each one generalised a number across cases that were not comparable.**

**Carried over from the previous version**

1. **"A second supplier will be cheaper."** Paulimar is dearer than Emilio on every comparable line. A second supplier buys resilience, not savings.
2. **"Bid 90% of estimate; the 75% anchor is the problem."** Large lotes cluster at 74–77% (n=3). Small lotes behave differently.
3. **"A company your size won it."** CONDAFE is an EPP, but it holds 47 contracts across 16 states.
4. **"240–450 dispensas a year."** The measured figure is 272, and only 139 of those are open avisos.
5. **"PNCP caps search at 600 rows."** That was this repo's own page limit.

**New in the 2026-09-22 rewrite**

6. **The 33,9% / 29,7% unit economics** compared one kit's cost with other kits' prices. Retired.
7. **"Sourced cost R$198,78."** It was priced against the wrong spec. The real-spec figure is R$250,98 for 16 lines. Five lines lose against the allocation, not one.
8. **Step 0 says STOP** for the Itaquaquecetuba spec. "+18,4% at dispensa clearing" is a hypothesis.
9. **"Dispensas pay faster."** Written terms have a median of 30 days for both mechanisms.
10. **The niche ranking** rests on an assumed 30% margin and is unsettled. Her decision stands: medalhas is a later side income, not a switch (c49b6fe, e91740f). Medalhas tenders move with kit tenders; the correlation is about 0,88 on complete years.
11. **"The system tells her which to bid."** It does not.
12. **"Not one pregão cleared at its estimate."** True only at exact equality: 5 of 40 cleared at ≥95%.
13. **"HHI 181 across 536 contracts."** The figure covers 463 genuine kit contracts.

**Corrected in this revision**

14. **Window W was given as 493 / 417 / 163 [M].** The census is 442 / 372 / 148 (33,5%) [C]. The re-pull behind the higher figures is uncommitted [U].
15. **Seasonality was given as 1,69×, with March and June tied.** The fact-sheet figure is 1,4×, with March as the peak. The "~2×" comes from the relevance-ranked harvest.
16. **The election year was given as +12,5%.** The figure is −2% (38,7 → 37,9).
17. **Median dispensa revenue was given as R$26.658,50, with R$40.100 called "modelled".** R$40.100 is the median priced dispensa revenue. R$26.658,50 is a different base, the summed homologated totals.
18. **Proposal windows.** "About 3 days" rested on one dispensa. Measured on 139 avisos (2026-09-23): median ~5 days, 29% within 3 days, 43% within 4.
19. **The O2C corpus was described as "1 dispensa TR".** No dispensa has been traced end to end. Timings are now 40–55 d (empenho → OB) and 45–75 d (homologação → cash).
20. **The float: "45 days is the working figure".** Config says 34 [A]. The plan models 45. Plan cash for 75.
21. **Late fines were given as "0,10%–5% per day".** The 5% is a one-off first-day charge. Daily rates run 0,3–2%.
22. **The ME cure period was given as a flat "5+5 d.u.".** It is 5 d.u., with 5 more at the buyer's discretion.
23. **"SRP requires a balanço from an ME" was stated as universal.** The waiver does not cover SRP. Actual frequency has not been counted.
24. **Kitting as manufacturing was put at +0,50 DAS points.** The fact sheet gives 2–5 margin points [U].
25. **"≤5-day call-offs cannot be met in any measured UF."** SP (4 days) can meet them.
26. **Required win rate.** It is now stated against the 139 biddable avisos as well as the 272 dispensas.

---

## 12. The next moves, in order

**0. Before measuring: write down the pass mark and the money** (her decisions; about an hour).
- **Set her capital** in `config/capital.yaml`. Her recorded budget is R$2.579–12.894; rule 12 cannot pass while the field is null.
- **Set her hourly hurdle H**, the value she puts on an hour of her time, in R$. It is not recorded anywhere. Fix it *before* the measurement, the way the Step 0 gate was fixed in advance (6cc7938), so the result cannot move the goalposts.
- **Get the DOU original of CNAS 213/2025.** Confirm its date (reported as 28/10/2026 [U]) and what it requires. If buyers are moving to cash, it is better to know before any money is spent.

**1. Measure the cost of real dispensa kits from data already in the repo, without contacting anyone.**
- **Input:** `data/typical_kit/` holds 42 PER_ITEM kit dispensas with their line items and homologated line prices. **40 are usable**; exclude the two lot-total artefacts, Pedro Laurentino/PI and Ribeira do Piauí/PI.
- **Sample:** 10–20 of them [A: a sampling choice], within the R$65.492,11 ceiling and at 200 kits or fewer. Weight the sample toward open **avisos**, because those are the tenders she can bid.
- **Check quantities:** in about half the tenders the lines have different quantities, so check tender by tender that "one of each line = one kit".
- **Cost each kit:** price it line by line against the SP catalogues used for `cost_table_v2`. Pick the smallest box it fits, and add freight to the buyer's delivery address.

**The pass mark** [formula C; H and the example A]:

```
contribution per kit  c = P × (1 − s − f) − M − F − A
pass (per lot)          c × kits ≥ H × 8 h + fixed cost per win
fundable                (M + F + A) × kits + DAS held back ≤ her capital
```

The terms:
- **P** is the homologated kit price of that tender.
- **s** is the Simples effective rate, 4,00% at RBT12 R$180k.
- **f** is the platform fee: 0 on Compras.gov; up to 1,5% on BLL, capped at R$600; R$118,80 ÷ kits on BNC.
- **M** is materials, **F** freight to that buyer, and **A** co-packing if any.
- **Fixed cost per win** is R$196–473 a month divided by her wins per month.

*Example only:* at H = R$100/h and one win a month with R$473 fixed, a 100-kit lot must leave at least R$1.273, about R$12,73 per kit after everything.

- **Go:** the median sampled aviso kit passes, and the lot is fundable from her capital. The business then works on paper. The remaining unknowns are the win rate and payment speed, and only bidding reveals those.
- **No-go:** the kit strategy fails on its own terms. Medalhas should then be measured the same way before any money is spent.

Report the **share of sampled kits that pass** as well as the median; that share says how many of the ~139 avisos a year are worth bidding.

**2. If go: get ready to bid** (in this order).
1. **Wire and schedule the daily loop:**
   - run the rules and pricing in `run_daily.py`;
   - schedule it and add a heartbeat;
   - bridge the workbook to the bid log;
   - replace the 0,75 anchor with a per-mechanism anchor (86,8% avisos, 65% pregões, from the measured medians; still one pull);
   - replace Rule 1's unsourced lote band;
   - extend the Simples table;
   - fix the dias-úteis flag;
   - update the README.
2. **Measure PAC transit to the 18 unmeasured UFs** (PR and GO first).
3. **Time self-packing on 10 real kits**, then set `self_pack_max_kits` from the result (80 until then).
4. **Register with Emilio** and get its wholesale table, minimum order and payment terms (RISK_REGISTER #15 suggests a R$500 test order).
5. **Decide whether research calls fit her rule.** The 30 municipalities are staged.

**3. Then open the company, and make the private sale.**
- Opening starts the Simples clock (confirm with the contador which rule applies, §8) and the fixed costs.
- Make the private sale for the atestado (~R$500 [A]).
- Then bid the first aviso that passes rules 1–13 and the §12 pass mark, and record every bid in the log.