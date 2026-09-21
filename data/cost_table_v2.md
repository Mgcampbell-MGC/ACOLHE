# Cost table v2 — the BOM re-priced against the REAL Itaquaquecetuba specification

**Priced 2026-09-21** against `docs/ITAQUAQUECETUBA_REAL.md` and the 17 item descriptions in
`data/editais/itaqua_spec_17_itens.json` (PE 90088/2025, 5.000 kits, estimado R$476,05/kit,
homologado R$359,05/kit = 75,42%). Machine-readable rows in `data/cost_table_v2.csv`,
same columns as `data/cost_table.csv`.

**Nobody was contacted.** No email, form, WhatsApp, phone, registration or account. Published
catalogue prices only. TLS verification was never disabled; every source that refused is in §6
rather than worked around. **Every CNPJ below was resolved at `https://publica.cnpj.ws/cnpj/{cnpj14}`**
on 2026-09-21 — see §5. Where something could not be read the cell says UNVERIFIED, not a number.

---

## 1. Headline

| | |
|---|---|
| **New BOM, 16 lines (mochila excluded)** | **R$ 250,98** |
| Same 16 lines, what the winner realised | R$ 284,73 *(R$359,05 − 74,30 mochila)* |
| **Headroom before freight, assembly, taxes and the banheira vinyl** | **R$ 33,75 — 11,9 % of realised** |
| Same 16 lines, buyer's own estimate | R$ 377,54 *(R$476,05 − 98,51 mochila)* |
| Old table, the 15 comparable lines | R$ 146,51 *(R$198,78 − 52,27 mochila)* |
| **Those same 15 lines, re-priced** | **R$ 243,69 — up R$ 97,18, +66 %** |
| `kit_enxoval` | **priced for the first time: R$ 7,29** |
| `oleo_infantil` | **fixed: R$23,89 → R$16,46, now R$1,47 under realised** |

**R$198,78 was never the cost of this kit.** Six lines were priced against the wrong article and
the correction is worth R$97 a kit. The BOM still clears the winner's realised price on 11 of 16
lines, but the cushion is now R$33,75, not the R$85-odd the old table implied — and freight,
assembly and the banheira's printed vinyl all still have to come out of it. **None of those three
is quoted anywhere in this repo, so the Step 0 gate still cannot be called.**

---

## 2. Line by line

Δ = what the winner realised on that line, minus our cost. Negative = we lose money on it.

| # | Line | Old cost | Buyer est. | Realised | **New cost** | Δ | Moved? |
|---|---|---|---|---|---|---|---|
| 01.1 | mochila | 52,27 *(lisa)* | 98,51 | 74,30 | **— UNPRICED** | — | out of scope by instruction |
| 01.2 | banheira_lisa **22 L** | 18,90 *(20 L)* | 36,91 | 27,84 | **34,67** | **−6,83** | ✅ re-priced at 22 L |
| 01.3 | cobertor_infantil | 12,15 *(80×110)* | 42,66 | 32,17 | **26,66** | +5,51 | ✅ old size failed 90×110 |
| 01.4 | cueiro **kit 3 pç** | 3,94 *(1 pç)* | 36,62 | 27,62 | **11,81** | +15,81 | ✅ basis fixed |
| 01.5 | pagao | 15,34 | 26,20 | 19,76 | **17,89** | +1,87 | ✅ components verified |
| 01.6 | fralda_rn **pack ≥32** | 23,78 *(18)* | 44,83 | 33,81 | **35,69** | **−1,88** | ✅ re-priced at 32 |
| 01.7 | body_manga_longa **tam P** | 7,56 *(prematuro)* | 18,99 | 14,32 | **7,84** | +6,48 | ✅ size risk resolved |
| 01.8 | **kit_enxoval** | **—** | 15,91 | 12,00 | **7,29** | +4,71 | ✅ **first price** |
| 01.9 | pano_de_boca **pacote 3** | 1,85 *(1 pç)* | 16,35 | 12,33 | **5,55** | +6,78 | ✅ basis fixed |
| 01.10 | par_de_meias | 2,01 *(100 % poliamida)* | 8,29 | 6,25 | **5,44** | +0,81 | ✅ composition fixed |
| 01.11 | toalha_banho **COM CAPUZ** | 3,42 *(sem capuz)* | 39,81 | 30,02 | **39,60** | **−9,58** | ✅ different product |
| 01.12 | toalhas_umedecidas 100 un | 6,02 | 15,39 | 11,61 | **6,02** | +5,59 | ➖ confirmed, basis right |
| 01.13 | sabonete_liquido **≥240 ml** | 8,99 *(210 ml)* | 16,00 | 12,07 | **15,19** | **−3,12** | ✅ volume fixed |
| 01.14 | shampoo_infantil **≥240 ml** | 10,45 *(200 ml)* | 14,92 | 11,25 | **12,66** | **−1,41** | ✅ volume fixed |
| 01.15 | **oleo_infantil** ≥100 ml | **23,89** | 23,77 | **17,93** | **16,46** | **+1,47** | ✅ **loss closed** |
| 01.16 | kit_higiene **2 peças** | 5,20 | 15,37 | 11,59 | **5,20** | +6,39 | ➖ confirmed conforming |
| 01.17 | saboneteira | 3,01 | 5,52 | 4,16 | **3,01** | +1,15 | ➖ unchanged |
| | **TOTAL (16)** | **146,51** *(15)* | **377,54** | **284,73** | **250,98** | **+33,75** | |

Gains on eleven lines total **+R$56,57**; losses on five total **−R$22,82**.

---

## 3. What moved, and why

### 3.1 `kit_enxoval` — the blocking line, priced. R$ 7,29

`KIT COM 3 PEÇAS - TOUCA LUVA E SAPATO EM MALHA #101 - CASTELO`, CONFECCOES EMILIO
(50191584000106, **SP**), [product page](https://www.emilio.com.br/kit-com-3-pecas---touca-luva-e-sapato-em-malha---101---castelo/p).

It matches edital 01.8 component for component — *01 touca, 01 par de luvas, 01 par de
sapatinhos **de malha*** — the page states **"Material 100% algodão"**, and the variant list
carries **AMARELO** and **VERDE**. It is the only kit found anywhere that satisfies the colour
constraint. Confirmed at a **second CNPJ at the same price**: COMERCIO DE ROUPAS YANAI
(44040459000194, SP) sells *Kit Luva, Touca, Sapatinho Castelo 100% Algodão* at
[R$7,29](https://yanaiatacado.com.br/products/kit-luva-touca-sapatinho-castelo-100-algodao).

*The one caveat, stated because it is on the same page:* "Pompom 100% acrílico. Acabamento 96%
algodão e 4% elastano." The body is 100% algodão; the **trim is not**. A strict pregoeiro could
reject on that. `config/skus.yaml` should carry KIT_ENXOVAL at 7,29 with that flag, and the
TOUCA / LUVA entries can be closed — the line is bought as one kit, not three items.

Rejected: `#080 FOFINHO` R$10,90 (100% **acrílico** — fails outright), `#104 CASTELO` lã R$11,76,
FIO DE AMOR tricô kits R$30,32–31,70.

### 3.2 `oleo_infantil` — the only line the business was losing on. R$ 23,89 → **R$ 16,46**

**Yes, it can be fixed, and it is fixed.** `OLEO BABY MUNDO BITA 100ML`, EMPREENDIMENTOS PAGUE
MENOS S/A (06626253000151, **CE — not SP**),
[product page](https://www.paguemenos.com.br/oleo-baby-mundo-bita-100ml/p), sold by the
storefront operator itself (not a marketplace seller), in stock. **R$1,47 under the R$17,93 the
winner realised.** Non-SP, so LC 123 art. 13 §1 XIII (h) adds ~6 points → effective **≈R$17,45**,
still under, but only by R$0,48.

Three cheaper numbers were found and **none of them is banked**, for reasons worth recording:

| Price | What | Why not banked |
|---|---|---|
| **R$8,15** | Óleo Hidratante Corporal **Turma da Xuxinha 120 ml** (Baruel, ref 7896020154525), DROGARIA SAO PAULO S.A. (61412110056533, **SP**), page states "Óleo de Amêndoas e Vitamina E", "hipoalergênico", Fases da Vida: Infantil. [link](https://www.drogariasaopaulo.com.br/oleo-hidratante-corporal-turma-da-xuxinha-120ml/p) | `AvailableQuantity` read **0** on 2026-09-21. Published price, real provenance, **not purchasable today**. This is the number to chase: it says the SP floor is less than half what we are carrying. |
| R$12,77 | Óleo Infantil **Muriel Baby Menino 100 ml** on paguemenos.com.br | Sold by marketplace seller **"FarmaViver"**, which publishes no CNPJ. **No CNPJ, no UF, no row** — the standing rule. |
| R$3,79 | Óleo Mineral Natural Farmax 100 ml, Drogaria São Paulo | It is a **laxative medicine** (via oral, "para constipação"), not an óleo infantil. Also `AvailableQuantity` 0. |

**No wholesaler in the shortlist stocks this line at all.** MENSA/JN Fraldas' cheapest is the
same R$23,89 Anjinho 200 ml we already had; TENDA ATACADO carries **no** infant oil (searched
"oleo", "oleo bebe", "oleo mineral", "oleo de amendoas bebe", "hidratante infantil" — 0 hits);
MaxQualy's lojista storefront carries **no** infant oil (only hair oils). **This line is currently
priced on a drugstore channel and still needs a wholesale source before 5.000 units.**

### 3.3 `banheira_lisa` at 22 litres — priced on its own, and it loses money. R$ 34,67

Not interpolated. Emilio's entire 22 L set was read on 2026-09-21:

| Ref | Price | Colours in stock |
|---|---|---|
| **MAJESTIC #0973** | **34,67** | AZUL, ROSA (DOURADO 0) |
| TRANSLÚCIDA #0852 | 36,34 | AZUL, ROSA |
| INFANTIL #0822 | 44,20 | AZUL, ROSA |
| INFANTIL #0810 | 44,20 | ROSA — **lists VERDE, 0 in stock** |
| TRANSPARENTE #0714 | 44,20 | BRANCO |
| ACONCHEGO MAGESTADE #0946 | 49,14 | AZUL, ROSA |

Cross-checked at Yanai (44040459000194, SP): *Banheira 22 Litros Transparente Adoleta* **R$36,34**
— a 4,8 % spread on the same manufacturer, so R$34,67 is a market price, not an outlier.

**Two things fail and both are on the record:** the edital wants *transparente com detalhes
**amarelo ou verde*** and **no 22 L tub in stock anywhere read offers it** (cheapest listing a
verde variant is R$44,20, out of stock in verde); and the approximate **26×43×67 cm** is not
published on any 22 L page — UNVERIFIED. The R$8,94 of slack the earlier note computed against a
20 L tub does not exist: **at 22 L this line is R$6,83 under water before a single vinyl is
printed.** Measured vinyl printing was R$2,20–2,78/kit, so the true exposure is ≈R$9–10 a kit.

### 3.4 `toalha_banho_infantil` with a hood — the biggest single loss. R$ 39,60

Edital 01.11: toalha **com capuz**, atoalhado 100% algodão, **mínimo 68 × 100 cm**, verde ou
amarela. **The 100 cm side kills the mainstream of the category** — every 70×70 and 70×90 hooded
towel fails, which is the whole of Emilio's cheap tier (R$13,10–20,53) and all four of Yanai's
(R$15,36–27,82). Only 13 hooded towels at Emilio reach ≥68×100 at all.

- **Banked: R$39,60** — `TOALHÃO COM CAPUZ 100X85CM - LOUPIOT NATURE #530944 MINASREY`,
  **VERDE** in stock, 100% algodão. Cheapest that meets size **and** composition **and** colour.
- Cheapest ignoring colour: **R$32,49**, `TOALHÃO DE BANHO SOFT COM CAPUZ #1426 PAPI`, 100×75 cm,
  "2 camadas de fralda soft 100% algodão" — prints, not verde/amarelo.
- Cheapest whose page actually uses the word **atoalhado**: **R$41,05**,
  `TOALHÃO AVENTAL COM CAPUZ 100X85 #530943`, VERDE, "tecido atoalhado com fralda".

So the loss is **R$9,58** as banked, and **R$11,03** if a pregoeiro enforces "atoalhado" literally.
The R$26,60 of apparent slack in the old document was slack on a 65 cm plain towel.

### 3.5 `fralda_descartavel_rn` at 32+ units. R$ 35,69

`FRALDA DESCARTÁVEL RECÉM-NASCIDO TRIPLA PROTEÇÃO P HUGGIES 32 UNIDADES`, TENDA ATACADO SA
(01157555001186, **SP**/Guarulhos), sku 000000000000938752-UN, EAN 17896007552440.
**The only ≥32-unit RN pack under R$50 found at any CNPJ-verified supplier.** The two alternatives,
both MENSA/JN Fraldas (SP), are Pampers Primeiros Dias RN C/36 **R$51,49** and Huggies Natural
Care RN C/34 **R$54,06**. Loses R$1,88 against realised.

Two flags: the title carries **both** "Recém-Nascido" and "P" — the edital wants RN, and the size
letter is ambiguous on the page. And "corte anatômico" / "barreira antivazamento" are not stated
in those words (the page does state *dermatologicamente testada*).

### 3.6 The three basis errors that were flattering the table by R$26

`cueiro` R$3,94 → **R$11,81**, `pano_de_boca` R$1,85 → **R$5,55**, `toalha` 1/3-of-pack → whole
unit. The edital buys a **kit de 03 peças** and a **pacote com 03 unidades**; the old table
consumed one piece of each. Same products, same suppliers, same pages — only the basis changed,
and it is worth **R$11,57** on those two lines alone.

`body_manga_longa` was the opposite kind of error: the old R$7,56 came from a **TAMANHO
PREMATURO** 3-pack, and the edital wants **tamanho P**. The SIZE_GRADED warning in `skus.yaml`
can now be retired for this SKU: on `KIT BODY MANGA LONGA CANELADO #2000 BABY DUFY` the size is a
**selectable variant at one price** (RN/P/M/G, R$23,53), so the P pack yields three size-P bodies
and the BOM consumes one → **R$7,84**. Page states 100% algodão. P in stock.

### 3.7 The two toiletries whose volume was simply wrong

Both were under-costed because the product was too small, not because it was cheap.

- `shampoo_infantil` — the old 200 ml Pompom **fails "mínimo 240 ml"**. The R$0,80 of slack the
  earlier document worried about was slack on a non-conforming product. Now
  **`SHAMPOO CAMOMILA ANJINHO 400ML` R$12,66** at MENSA/JN Fraldas (SP), whose page matches the
  edital almost word for word: *testados dermatologicamente e oftalmologicamente*, *"Chega de
  lágrimas"*, *sem corante*, camomila. "Sem sal" is not stated — UNVERIFIED. Loses R$1,41.
- `sabonete_liquido` — the old 210 ml Baruel **fails "mínimo 240 ml"**. Now
  **`SABONETE LÍQUIDO TURMA DA XUXINHA COM GLICERINA 400ML` R$15,19** at Drogaria São Paulo
  (SP), page specs: Fases da Vida **Infantil**, Tipo **Glicerinado / Hipoalergênico**, 400 ml,
  in stock. SP wholesale alternative: Anjinho Camomila 400 ml **R$16,78** at JN Fraldas. Cheaper
  but weaker spec match: Palmolive Kids Suave 315 ml **R$14,15** at Tenda. Loses R$3,12.

### 3.8 `cobertor_infantil` — the old row failed on size, and "pelo alto" is unverifiable

Edital 01.3: 100% poliéster, **pelo alto**, estampado, **mínimo 90 cm × 1,10 m**, amarelo ou verde.
The old R$12,15 CAMESA is **80×110** — it fails. Banked: `COBERTOR BABY PETIT CANE 90CM × 1,10M
#PTCANIN202201 ETRURIA` **R$26,66**, page states "Composição: 100% poliéster", 90 × 110 cm.

**"Pelo alto" is not evidenced on any 90×110 product read.** This page says *toque de seda*. The
only items anywhere that use the words are at Yanai — *Cobertor Pelo Alto Jolitex* R$43,99 and
*Pelo Alto Hazime* R$48,29 — and **neither publishes dimensions or composition**, so neither can
be matched to this spec. Cheaper 90×110 100% poliéster options fail harder (CAMESA microfibra
R$19,90 — and `skus.yaml` carries an anti-pattern on MICROFIBRA for this family); dearer flannel
ones are R$34,67 (Camesa) and R$37,80 (Hazime).

### 3.9 `par_de_meias` — composition, not price, was the problem

The old R$2,01 Luqui is **"100% Poliamida"** and not atoalhada; the edital wants **atoalhada, em
algodão, poliamida e elastano**. Banked: `KIT MEIA ATOALHADA 3 PARES #T08004-0004 TRI FIL`,
**"modelo atoalhado"**, **"66% Algodão, 31% Poliamida e 3% Elastano"** — the exact three fibres —
**tamanho P** a stocked variant, R$16,31 / 3 pares = **R$5,44 a par**. Colour branco.
Runners-up: Rikam atoalhada baby R$4,99 (composition not published), Delos/You RN R$3,35/par
(composition fits, not atoalhada).

### 3.10 Three lines confirmed unchanged

`toalhas_umedecidas` R$6,02 — the edital says *"Embalagem com 100 (cem) unidades"*, so the pack
basis this table already carried is **right** and the BOM_UNIT_AMBIGUOUS flag is retired. Re-read
at source 2026-09-21, still R$6,02, in stock. Still unverified on the page: TNT, loção sem álcool
etílico, sem parabenos, 18 × 14 cm mínimo, validade 12 meses.

`kit_higiene_bebe` R$5,20 — and it is now **confirmed conforming**: exactly 02 peças, "escova de
cerdas macias", "pente contém pontas arredondadas", **VERDE in stock**. The 3–4-piece fallbacks
the old note offered (R$8,06 / R$15,48) would be **over-spec** for this edital.

`saboneteira` R$3,01 — carried unchanged but **nothing about it is verified**: the page has no
description at all, sibling refs say only "100% Plástico" (not PP), the variant is BRANCO not
amarelo/verde, and no dimension is published for an 80–100 g bar. Yanai has a cheaper one at
R$2,97. This is the weakest-provenance row in the table for its size.

---

## 4. Still unpriced, and what it would take

| Line | State | What is missing |
|---|---|---|
| **01.1 mochila** | **UNPRICED** — excluded from this pass by instruction | A quote from a confecção that prints **four different silk artworks** on a made-to-order PVC bag. The named SP route, BRINDES SP (46033832000105, min 50 un), publishes no price. The old R$52,27 is a **plain catalogue bag** and is structurally not a base to add printing to. Realised: R$74,30. |
| **01.2 banheira — vinyl** | **UNPRICED** (tub priced at R$34,67) | Adesivos de vinil CMYK on three faces, water-resistant, 12-month durability, **already applied**. Printing was measured at R$2,20–2,78/kit elsewhere in the repo; the **application labour** has never been quoted. |
| Freight | **UNQUOTED** | ONE_ADDRESS / LTL to Rua Caiabu 240, 20 days. The banheira alone will be **cubed** (513 g against ~0.047 m³). |
| Assembly / co-packing | **UNQUOTED** | 5.000 kits, 16 articles each. |

Every other line carries a price with a supplier name, a CNPJ, a UF, a product reference, a URL
and a date.

---

## 5. CNPJs resolved at the registry, 2026-09-21

All six resolved at `https://publica.cnpj.ws/cnpj/{cnpj14}`. No UF below rests on a trading name
or on a site's own claim.

| CNPJ | Razão social returned | UF | Cidade | Situação | Tipo |
|---|---|---|---|---|---|
| 50.191.584/0001-06 | CONFECCOES EMILIO LTDA | **SP** | São Paulo | Ativa | Matriz |
| 44.040.459/0001-94 | COMERCIO DE ROUPAS YANAI LTDA | **SP** | São Paulo | Ativa | Matriz |
| 10.290.457/0001-31 | MENSA DISTRIBUIDORA LTDA. | **SP** | São Paulo | Ativa | Matriz |
| 01.157.555/0011-86 | TENDA ATACADO SA | **SP** | Guarulhos | Ativa | Filial |
| 61.412.110/0565-33 | DROGARIA SAO PAULO S.A. | **SP** | São Paulo | Ativa | Filial |
| 06.626.253/0001-51 | EMPREENDIMENTOS PAGUE MENOS S/A | **CE** ⚠ | Fortaleza | Ativa | Matriz |

⚠ **The only non-SP supplier in the table is Pague Menos, on `oleo_infantil` alone.** LC 123
art. 13 §1 XIII (h) charges the internal-minus-interstate ICMS difference, ~6 points: R$16,46
becomes ≈R$17,45 landed, which is still under the R$17,93 realised — **by R$0,48**. Replacing it
with the SP option (Drogaria São Paulo, R$8,15) the moment that SKU is back in stock removes both
the ICMS drag and most of the cost.

**Fourteen of the sixteen priced lines are SP**, and eleven of them are Emilio. The concentration
`suppliers_shortlist.md` flagged is unchanged by this pass — and the two-CNPJ cross-checks it
enabled (Yanai on `kit_enxoval` at the identical R$7,29, and on the 22 L banheira within 4,8 %)
are the only independent confirmations in the table.

---

## 6. Blocked-sources register, this pass

Recorded, not worked around. No TLS check was disabled, no wall was circumvented, nobody was
contacted.

**Refused outright**

| Source | What happened | What it cost us |
|---|---|---|
| `www.drogasil.com.br` | **HTTP 403** on both the catalogue and the store endpoints | The third large SP pharmacy chain; would have been a clean third read on `oleo_infantil`. |
| `www.bimdistribuidora.com.br` | **HTTP 403** | Named in search results as a higiene-infantil atacadista. |

**Reachable but unusable as a price source**

| Source | Why |
|---|---|
| `brascol.com.br` / ONESHOP (18483322000102, SP) | Login wall, already on record. Not retried. |
| `www.ultrafarma.com.br`, `www.panvel.com`, `www.montrealdistribuidora.com.br` | No public catalogue endpoint found (404). |
| `www.laroya.com.br`, `www.lukinhasbaby.com.br` | Prices are public, but **neither publishes a CNPJ** on any page read. Without a CNPJ the UF cannot be proved, so they stay **leads, not sources**. |
| `lojista.maxqualy.com.br` (53748042000171, SP) | **Readable, and read.** It simply does not carry the lines: no infant oil, no infant shampoo, no fraldas. Its only baby wash is Biotropic 230 ml at R$15,83 — **under the 240 ml minimum**, so it fails 01.13. The "second published route to deferred payment" finding stands; it is not a price source for this kit. |
| `www.paulimar.com.br` (60656782000143, SP) | Public prices, bespoke platform, **no higiene line**; the 2026-09-19 sweep already found it dearer than Emilio on every comparable textile. |
| `www.mercantilatacado.com.br` | Open VTEX catalogue, read — it is a **food** wholesaler; the only "óleo" rows are soya and canned sardines. |
| Marketplace seller **"FarmaViver"** on paguemenos.com.br | Lists the cheapest genuine infant oil (R$12,77) but **publishes no CNPJ**. Price discarded under the provenance rule rather than banked. |

---

## 7. What this does to the Step 0 gate

It **narrows** it without settling it.

- The kit is **R$250,98 in materials for 16 of 17 lines**, against **R$284,73** the winner realised
  on those same lines. **R$33,75 a kit, 11,9 %**, is what is left for freight, assembly, the
  banheira's printed vinyl and its application, and every tax — **none of which is quoted**.
- `kit_enxoval` no longer blocks anything. It is the cheapest surprise in the kit: R$7,29 against
  R$12,00 realised, at two independent SP CNPJs.
- `oleo_infantil` **no longer loses money** and the SP evidence says it could land near R$8.
- The losses have **moved to the physical lines**: `banheira_lisa` −6,83 and
  `toalha_banho_infantil` −9,58 are now 73 % of all the red in the table, and neither is a
  sourcing slip — both are the edital's own dimensions (22 L; 68 × 100 cm) pricing us out of the
  cheap tier of the category.
- Two lines fail their written spec at the price banked and would need a dearer SKU or a
  challenge: the 22 L banheira has **no amarelo/verde in stock anywhere read**, and no 90 × 110
  cobertor read anywhere says **"pelo alto"**.

**The honest position: the gate turns on the mochila, the vinyl, freight and assembly — four
numbers, none of them in this file.** The materials side is now measured against the real
specification and it clears, but only just.
