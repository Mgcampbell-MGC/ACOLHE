# The real kit, the real price, the real winner — Itaquaquecetuba 2025/447

**Read 2026-09-21, the morning PNCP Family B came back.** Everything below is from the
municipality's own published files: the item list, the results endpoint, and
`p.e._90088_25_edital_retificado2.pdf` (70 pages, clean text). Saved in
`data/editais/itaqua_spec_17_itens.json`, `itaqua_result_{1,2}.json`, `itaqua_arq_7.txt`.

## 1. The number the whole model was missing

| | |
|---|---|
| Órgão | Município de Itaquaquecetuba/SP, CNPJ 46.316.600/0001-64 |
| Compra | Pregão Eletrônico 90088/2025, SRP, **Programa Mãe Itaquá** |
| Quantidade | 5.000 kits — **3.750 ampla concorrência + 1.250 cota ME/EPP (25%)** |
| Estimado | **R$ 476,05 / kit** |
| **Homologado** | **R$ 359,05 / kit** — R$ 1.795.250 total |
| **Clearing ratio** | **75,42 % do estimado** |
| Vencedor | **CONDAFE COMÉRCIO DE ROUPAS LTDA EPP**, CNPJ 10.430.444/0001-10, porte **EPP** |
| Data do resultado | 2026-03-24 |
| Entrega | **20 dias** da assinatura, **endereço único**: Almoxarifado Central, Rua Caiabu 240 |

**A small company won it.** Not a wholesaler, not a giant: an EPP, the same category this
business would register as. That is the single most encouraging fact in the project.

**And the 75% anchor was right.** The inherited plan's "bid 75% of estimate" was not
arbitrary — this tender cleared at 75,42%. On 2026-09-20 the SCENARIOS sheet argued for
bidding 90% on the grounds that per-item lots clear at 97–100%. **That reasoning does not
apply here**: this is a *lote* (all 17 items priced as one kit, menor preço), and a lote in
São Paulo cleared at 75,4%. One data point is not a distribution, but it is one more than
the 97–100% figure ever had.

## 2. The three ambiguous rows, settled

| BOM line | What we assumed | What the edital says |
|---|---|---|
| `banheira_lisa` | 20 L (R$18,90) or 24 L (R$29,71) — a R$11 swing on one word | **22 litros**, polipropileno, transparente com detalhes amarelo/verde, 26×43×67 cm |
| `toalhas_umedecidas` | pack or single wipe | **Embalagem com 100 unidades**, TNT, loção à base de água sem álcool — our pack basis of 100 is correct |
| `body_manga_longa` | "RN ao G" 3-pack: three RN or one of each? | Neither. **One unit, tamanho P**, 100% algodão, amarelo ou verde |

## 3. `kit_enxoval` — the last unpriced line — is now specified

> **01.8 Kit Enxoval contendo 01 Touca, 01 Par de Luvas e 01 Par de Sapatinhos de malha
> (ou pantufa). Composição: 100% algodão. Cor Amarelo ou Verde.**

`config/skus.yaml` already carries TOUCA and LUVA. The line is priceable as soon as those
three are quoted together.

## 4. Two costs nobody has priced — and they are not small

**The kit is BRANDED.** Two of the seventeen lines are custom-printed:

- **01.1 Mochila** — PVC com efeito búfalo, 42×34×18 cm, cor RGB 193,188,182, with **four**
  silk-screen elements, not three, and they are **different artworks**: the project logo on
  the front pocket (20 × 7,5 cm), one institutional logo on the left pocket and the
  **Prefeitura Municipal de Itaquaquecetuba** on the right (each **5 × 7 cm** — 20 × 20 cm
  is the *pocket*, not the logo), plus a white satin care label in silk (4 × 5 cm) carrying
  the programme logo **and the supplier's own CNPJ**. Different artworks mean separate
  screens, and silk is priced per colour and per screen burned.
- **01.2 Banheira** — **adesivos de vinil já aplicados** nas laterais esquerda, direita e
  cabeceira; impressão digital CMYK em alta resolução, recorte eletrônico, resistente à água,
  **durabilidade mínima de 12 meses**, with a specified "Adesivo do Programa Mãe Itaquá".

`data/cost_table.csv` prices a plain bag (R$52,27) and a plain tub. **Neither carries a
printing cost, and the BOM total of R$198,78 is therefore not a floor for this tender.**
Worse for that line: no printer found publishes *personalização de material do cliente* —
every bag source is a fabricante that prints only bags it makes. So the plain-bag-plus-
printing model is structurally wrong, and the R$52,27 row is not a base to add to. (The
R$52,27 item is not even blank: it is a catalogue bag that already carries a print.)
This is exactly what the supplier sweep found on 2026-09-19: *Brindes SP*
(46.033.832/0001-05, SP, 50-unit minimum, silk/sublimação/bordado) is the named route, and
it publishes no price.

## 5. Other spec corrections to the cost table

| Line | Problem |
|---|---|
| `fralda_descartavel_rn` | Edital demands a **pacote com no mínimo 32 unidades**. The cost table carries a **18-unit** pack. Re-price. |
| `toalha_banho_infantil` | Edital demands a toalha **COM CAPUZ**, 68×100 cm, one unit. The cost table prices a plain towel at 1/3 of a 3-pack. Wrong SKU and wrong basis. |
| `cueiro` | **Kit de 03 peças** 50×80 cm sold as one line — not three separately-priced pieces. |
| `pagao` | **03 peças: 01 colete + 01 blusa manga longa + 01 calça com pé**, tamanho P. |
| `kit_higiene_bebe` | Only **02 peças: 01 pente + 01 escova**. Many market kits have 3–4 pieces; this one does not. |
| `sabonete_liquido`, `shampoo_infantil` | **mínimo 240 ml** each. Confirm the quoted volumes. |
| `oleo_infantil` | **mínimo 100 ml**. R$23,89 for 100 ml looks high — re-check. |
| Colour | Almost every textile line is **"Amarelo ou Verde"**. A colour constraint narrows the supplier catalogue. |

## 6. What the machinery got right, and what it got wrong

`parse/entrega.classify_delivery` on the real text: **ONE_ADDRESS**, freight mode **LTL**,
not parcelado — evidence `'ENTREGUES NO ALMOXARIFADO'`, `'RUA CAIABU, Nº 240'`. Correct.

`parse/spec.classify` on the 17 real descriptions: **13 of 17 classified**, and the four
misses are informative rather than random:

- **01.1 Mochila — a false negative.** Rejected by the global anti-pattern `COMPOSTO (DE|POR)`,
  which exists to catch bundle rows. Here "filme **composto de** Policloreto de Vinila"
  describes a *material*. The anti-pattern needs to look for a composition of ARTICLES, not
  of substances.
- **01.4 cueiro, 01.5 pagão, 01.16 kit higiene** — all rejected as bundles. They are
  multi-piece, but they are multi-piece **sets sold as one BOM line**, which is different
  from a bundle row that hides several articles. `is_bundle` needs that distinction.
- **01.10 meias** — "Par de Meias ... Par 1" was not accepted because the classifier wants
  the plural "PARES".

`screen.rules.rule_2_atestado` reads clause 10.1.4.1 as **QUALITATIVE**, correctly: it asks
for an atestado, sets **no minimum quantity and no percentage**, and accepts an issuer that
is a "pessoa jurídica de direito público **ou privado**". The biggest buyer in the corpus
states the first-sale route of `docs/HABILITACAO.md` in its own words.

## 7. Two things to fold into other documents

- **Falência certidão: "com data inferior a 60 dias"** (clause under art. 69 II). Tighter
  than the 90-day fallback in `config/documentos.yaml`. The tracker should carry 60 as the
  conservative assumption for TJSP.
- **Cota ME/EPP of 25%** (1.250 of 5.000), LC 123 art. 48 III — and CONDAFE won **both** the
  open item and the reserved quota.

## 7b. The buyer published its own line-by-line estimate — and it verifies

The rectified edital carries a priced table, one row per article. **Extracted and summed
independently: 17 lines, exactly R$ 476,05**, to the centavo, matching the
`valorUnitarioEstimado` PNCP returns. That makes it the best cost benchmark in the project:
not a catalogue guess but the buyer's own valuation of this exact specification.

Set against our sourced costs, and against what the winner actually realised (estimate ×
75,42%):

| Linha | Nosso custo | Estimativa | A 75,4% | Folga |
|---|---|---|---|---|
| mochila | 52,27 *(liso)* | **98,51** | 74,30 | 22,03 *(4 elementos de silk)* |
| banheira_lisa | 18,90 *(lisa, 20 L)* | **36,91** | 27,84 | 8,94 *(22 L + vinil + aplicação)* |
| cobertor_infantil | 12,15 | 42,66 | 32,17 | 20,02 |
| cueiro | 3,94 | 36,62 | 27,62 | 23,68 |
| pagao | 15,34 | 26,20 | 19,76 | 4,42 |
| fralda_descartavel_rn | 23,78 *(pack 18)* | 44,83 | 33,81 | 10,03 |
| body_manga_longa | 7,56 | 18,99 | 14,32 | 6,76 |
| **kit_enxoval** | **—** | 15,91 | 12,00 | **sem custo** |
| pano_de_boca | 1,85 | 16,35 | 12,33 | 10,48 |
| par_de_meias | 2,01 | 8,29 | 6,25 | 4,24 |
| toalha_banho_infantil | 3,42 *(sem capuz)* | 39,81 | 30,02 | 26,60 |
| toalhas_umedecidas | 6,02 | 15,39 | 11,61 | 5,59 |
| sabonete_liquido | 8,99 | 16,00 | 12,07 | 3,08 |
| shampoo_infantil | 10,45 | 14,92 | 11,25 | 0,80 |
| **oleo_infantil** | **23,89** | 23,77 | 17,93 | **−5,96 PERDE** |
| kit_higiene_bebe | 5,20 | 15,37 | 11,59 | 6,39 |
| saboneteira | 3,01 | 5,52 | 4,16 | 1,15 |
| **TOTAL** | **198,78** *(16)* | **476,05** | **359,05** | |

**Fifteen of sixteen sourced lines sit under what the winner realised on them**, and the
implied gross is ~44,6% before freight, assembly and printing. Two lines break the pattern:

- **`oleo_infantil` is the only line we are losing on** — R$23,89 sourced against R$17,93
  realised. That is a sourcing failure on one line, not a market problem, and it is the
  single cheapest thing on this page to fix.
- **`shampoo_infantil` has R$0,80 of slack** — effectively none.

The two branded lines have the least real slack once their actual requirement is counted:
R$22,03 to cover four silk elements on a made-to-order bag, and R$8,94 to cover the jump
from a 20 L plain tub to a 22 L tub plus printed vinyl on three faces plus application.
Measured vinyl printing runs R$2,20–2,78 per kit, so the printing itself is not what is
tight — **the tub upgrade and the application labour are.**

## 8. What this does to the Step 0 gate

**It does not settle it — it moves it.** R$198,78 for 16 of 17 lines was never the cost of
*this* kit: at least four lines are priced against the wrong spec, one is a 18-pack where 32
is demanded, and two lines require printing that has never been quoted. The honest position
is that the gate cannot be called until the BOM is re-priced against the specification above
and the two branded lines have a real quote.

What *is* settled: **a company of exactly this size won 5.000 kits at R$359,05**, delivery to
a single address, 20 days, on a qualitative atestado a private sale would satisfy.
