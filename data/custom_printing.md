# Custom printing on the branded kit — published-source survey

Compiled 2026-09-21, the day `docs/ITAQUAQUECETUBA_REAL.md` established that the kit is
branded. Catalogue and website reading only. **Nobody was contacted**, no form was filled,
no quote requested, no registration made, nothing spent. Every UF below that carries a CNPJ
was resolved at `https://publica.cnpj.ws/cnpj/{cnpj14}`; a trading name or a site's own
"São Paulo" was never trusted — and twice it was wrong (see §6). Where a company does not
print its CNPJ, the UF is marked as declared-only and is **not** a verified UF.

Companion table: `data/custom_printing.csv` (35 rows).

---

## 1. Headline — what does branding this kit add per unit?

**At 100 / 500 / 5.000 kits, the honest answer is: only one of the four cost components can
be priced from published sources. The other three are UNVERIFIED.**

| Component | 100 kits | 500 kits | 5.000 kits | Status |
|---|---|---|---|---|
| **A. Banheira — vinyl printing** (3 die-cut stickers) | **R$ 2,20** | **R$ 1,86** | **R$ 1,86** | **OBSERVED** (RJ) |
| A′. same, cheapest *SP* supplier | R$ 2,78 | R$ 2,78 | R$ 2,78 | **OBSERVED** (SP) |
| **B. Banheira — sticker application** onto the tub | ? | ? | ? | **UNVERIFIED** |
| **C. Mochila — silk screen**, 3 logos + satin label | ? | ? | ? | **UNVERIFIED** |
| **D. Setup / matriz / clichê**, one-time | ? | ? | ? | **UNVERIFIED** |
| **TOTAL added per kit** | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | — |

**No supplier publishes enough to price this kit's branding without a quote.** One line — the
vinyl printing — can be priced exactly. The rest cannot, and the largest of them (C) probably
cannot be priced *at all* in the form the cost model assumes. That is §2.

### The one number that is real

Component A is not an estimate. The edital gives the sticker dimensions literally, and one
printer publishes both a per-m² rate and the arithmetic it uses:

```
Adesivo "Programa Mãe Itaquá"   14 × 8 cm  (head end, inside)   = 0,0112 m²
Adesivo "Prefeitura"            15 × 4 cm  × 2 (left + right)    = 0,0120 m²
                                                        TOTAL   = 0,0232 m² per banheira
```

Segunda Via Gráfica publishes: **R$95,00/m² under 500 units, R$80,00/m² at 500+**, electronic
die-cut included, transparent stock available, and the worked formula verbatim —
`0,07 × 0,10 × 100 × R$95,00 = R$66,50`. It charges the **bounding box** of each sticker, so
the calculation above is theirs, not ours.

- 100 kits = 300 stickers → under the 500-unit step → 0,0232 × 95 = **R$2,20/kit**
- 500 kits = 1.500 stickers → 0,0232 × 80 = **R$1,86/kit**
- 5.000 kits = 15.000 stickers → **still R$1,86/kit**, because *no step below R$80 is published*.
  Treat R$1,86 at 5.000 as a **ceiling on list price**, not a real large-order price.

Cheapest compliant **SP** equivalent is Uniartes' *adesivo etiqueta corte especial*, "a partir
de R$120,00/m²" → **R$2,78/kit** at every quantity. The SP premium is R$0,92/kit (33%), which
clears the ~6-point ICMS threshold comfortably — but see §7 before acting on it.

---

## 2. The finding that matters more than any price

**The plain-bag-plus-printing model is structurally wrong, and the R$52,27 bag in
`data/cost_table.csv` is not the base of this line.**

Three reasons, all from published sources:

1. **Every bag supplier found is a *fabricante* that prints what it sells.** Idaplast (CNAE
   1521100, *fabricação de artigos para viagem, bolsas e semelhantes*), Brindes SP ("somos
   fabricantes"), JC Promocionais, Bolsavel, Silk Gra. **Not one publishes a
   "personalização de material do cliente" service** — printing a bag you send them. The
   brief flagged this as the distinction that "changes everything": it resolves against the
   plain-bag model. The real cost of line 01.1 is a **finished made-to-order bag price**, and
   the R$52,27 plain bag is irrelevant to it.

2. **The spec bag is not a catalogue article.** PVC film with buffalo effect in RGB 193,188,182,
   42×34×18 cm *minimum*, piping in RGB 97,164,156, four pockets including a transparent
   waterproof inner pocket, nickel-plated metal adjusters, four grey plastic studs, and a
   **satin care label carrying the supplier's own CNPJ**. Idaplast's nearest catalogue
   maternity bag is 38×33×16 cm — smaller than the edital's *minimum* on all three axes.
   This bag is tooled to order. There is no catalogue price for it anywhere.

3. **The R$52,27 bag is not even blank.** `cost_table.csv` prices "MOCHILA BABY PRINTS #802
   ESPERA FELIZ" — a bag that already carries its own printed design. It could not receive
   three institutional logos even if a printer would take customer material.

### What the edital itself says the branded articles are worth

The tender publishes an estimated unit price for each of the 17 lines. The 17 rows sum to
exactly **R$476,05**, matching the published estimate — so the table is read correctly.

| Line | Edital's estimate | Our plain-article cost | Gap |
|---|---|---|---|
| 01.1 Mochila (branded, full spec) | **R$ 98,51** | R$ 52,27 | **+R$ 46,24** |
| 01.2 Banheira (stickers applied) | **R$ 36,91** | R$ 18,90 – 29,71 | **+R$ 7,20 to +R$ 18,01** |

**Read these as the buyer's estimate, not as cost.** The tender cleared at **75,42%** of
estimate. Applied to these two lines the winner's implied realisation is **R$74,29** for the
bag and **R$27,83** for the tub — and R$27,83 is *below* the R$29,71 top of our plain-tub
range. CONDAFE therefore buys the tub well under retail, which means the R$7,20–18,01 gap is
**not** the cost of stickers: it contains the supplier's buying advantage and margin too.

The gap is an **upper bound on what the buyer believed branding plus spec-upgrade costs.**
It is the best-supported bound available, and it is worth far more than any brindes catalogue
found in this sweep. Against it, component A at R$1,86–2,78 is small: on the banheira line,
**printing is not the expensive part — application and the spec upgrade are.**

---

## 3. Per-category table

### `vinil_adesivo` — printed transparent adhesive vinyl (12 rows)

| Supplier | UF | Basis | Price | Die-cut incl.? | Lead | Note |
|---|---|---|---|---|---|---|
| **Segunda Via Gráfica** | RJ | m² | **R$95 <500un / R$80 ≥500un** | **YES** | 3–4 d | best published; min R$25/order |
| **Uniartes** (UNIARTES LTDA) | **SP** | m² | **R$120 "a partir de"** (corte especial) | **YES** | 7 d | min R$40; compliant SP option |
| Uniartes — transparent, straight cut | SP | m² | R$100 | no | 7 d | 4x0 photo quality, but corte reto |
| Revenda Infinity | SP | m² | R$30,90 | **no** — "refilado no tamanho" | 1–2 d | cheapest + fastest, **non-compliant as published** |
| Gráfica JN | SP | — | **login wall** | — | — | resale-tier pricing; good quote target |
| Gráfica Paulista Cartões | **MG** | — | **JS-only** | offers meio corte | — | name says Paulista, CNPJ says Uberaba/MG |
| Graphic Store | RS | — | **template vars** | yes | — | publishes "não fazemos orçamentos especiais" |

### `silk_bolsa` — silk screen on bags (10 rows)

| Supplier | UF | Price published? | What it does publish |
|---|---|---|---|
| **WG Embalagens** | RJ | **YES — R$45,00 / up to 100 pcs / 1 colour** | the only silk-screen price in the whole sweep |
| Brindes SP | SP | no (reconfirmed) | **20 dias úteis**, 30–50 unit minimum |
| Iniciativa Brindes | SP | no | "Até 4 cores" — the practical ceiling |
| Silk Gra | SP | no | catalogue photos only |
| Redd Brindes | SP (declared) | no | six techniques described, zero prices |
| Laser Company SP | SP (declared) | no | publishes **policromia separation** — only one that does |
| Top Laser | SP (declared) | no | "Impressão em Até 5 Dias" |
| Stampinny | ? | **no** | URL ends `-preco`, page has no price |
| Toca do Silk | ? | **403 blocked** | was the best matriz-fee lead |

### `bolsa_personalizada_pronta` — finished personalised bag (8 rows)

| Supplier | UF | Price | Includes silk? | Min | Lead |
|---|---|---|---|---|---|
| **Idaplast** | **SP** | — | 1/2/3/4 colours offered | "por modelo e layout" | — |
| Caicó Brindes | **RN** | **R$4,58–4,76/un** | **yes, 1 colour** | 25–50 un | **30 d** |
| Brindes Design | RJ | **R$34–45/pc @ 500** | **yes, "com gravação em SILK"** | 500 | — |
| Zen Brindes / DAXX MÍDIA | SP | R$10–500 (a 50× range) | up to 5 colours | 100 | 15 d |
| Luminati | **ES** | — | "500 peças, logo em 1 cor" | — | — |
| JC Promocionais | SP (declared) | — | — | atacado p/ CNPJ only | — |
| Bolsavel | SP (declared) | — | "preços de fábrica" | — | — |

### `aplicacao` — applying the stickers (3 rows)

| Supplier | UF | Publishes application? | Price |
|---|---|---|---|
| **Alô Sara Manuseios** | SP (declared) | **YES — "aplicação de vinil"**, named service, 35+ yrs | **none** |
| Raotech | SP (declared) | rotulagem adesiva + montagem de kits | none |
| Silk Mac | **?** | terceirização de rotulagem | none |

### `copacker_personalizacao` (2 rows)

**Negative result, recorded as a result.** All 24 SP providers in `data/copacking.md` were
re-examined. **None publishes silk screen, serigrafia, printing or adhesive application as a
service.** The only near-hit in the whole file is Envio Certo's "montagem personalizada",
which means assembly to the client's spec — not graphic personalisation. Nascra is the one
whose *razão social* literally reads "SOLUÇÕES EM PERSONALIZAÇÃO"; its page carries only
illustrative whole-kit ranges (R$50–200/unit **including the goods**), its own disclaimer says
the figures may not be current, and its CNPJ is **SUSPENSA**. The sticker-application line is
**not covered** by the co-packers already surveyed.

---

## 4. What the industry charges for, and how

Established from published pages, not inferred:

1. **Price scales by NUMBER OF COLOURS, not by number of positions.** Idaplast publishes
   "silk screen 1, 2, 3 ou 4 cores"; Iniciativa Brindes "Até 4 cores"; Zen Brindes "até 5
   cores" and states the driver verbatim: *"O valor do produto varia de acordo com a
   quantidade, cores de gravação e tipo de gravação."* Quantity, colours, technique — position
   count is never named as a price axis.
2. **Catalogue prices already include ONE colour in ONE position.** Three independent
   confirmations: Caicó ("1 Cor em Silk Screen" inside the unit price), Brindes Design ("com
   gravação em SILK"), Luminati ("Valor referente a 500 peças, com aplicação de logo em 1 cor").
   **The extra colours and extra positions are exactly the part nobody publishes** — and this
   kit needs three different institutional logos plus a satin label.
3. **500 pieces / 1 colour is the sector's default quoting basis.** Luminati and Brindes Design
   both price on it. Useful: the founder's 500-kit scenario is the industry's native tier.
4. **Setup is charged per COLOUR (per screen burned), once per order.** No supplier published a
   figure. A trade article (`camisetasem12h`, **a blog, not a supplier**) publishes R$80–150
   per colour for the matriz. That is the only number available and it is not a quote.
5. **Vinyl is charged per m² of BOUNDING BOX, with electronic die-cut normally included.**
   Segunda Via and Graphic Store both fold the recorte into the m² rate. Only the *straight-cut*
   lines are cheaper (Infinity R$30,90 vs Uniartes corte especial R$120).
6. **Application is a labour line nobody prices.** One company in the entire sweep names it.

### Why setup dominates at 100 and vanishes at 5.000

Four silk elements (front 20×7,5; left pocket 5×7; right pocket 5×7; satin label 4×5), three
of them *different* institutional logos. If each averages 3 colours → ~9–10 screens.
At the blog's R$80–150/screen that is **R$720–1.500 one-time**:

| Quantity | Setup per kit (**INFERRED**, blog rate) |
|---|---|
| 100 | **R$7,20 – 15,00** |
| 500 | R$1,44 – 3,00 |
| 5.000 | **R$0,14 – 0,30** |

This is the shape of the answer even though the rate is not a quote: **at 100 kits the
branding is a setup problem; at 5.000 it is a per-piece problem.** It also explains why the
whole industry quotes — the answer genuinely depends on the artwork's colour count, which no
price list can anticipate.

---

## 5. Lead times for printed goods (added to the delivery deadline)

| Supplier | Published lead | Fits Itaquaquecetuba's 20 days? |
|---|---|---|
| Revenda Infinity (vinyl, SP) | **1–2 dias úteis** | yes |
| Segunda Via (vinyl, RJ) | 3–4 days after artwork | yes |
| Top Laser (silk, SP) | "até 5 dias" | yes |
| Uniartes (vinyl, SP) | 7 dias úteis | yes |
| WG Embalagens (silk, RJ) | 7–10 dias úteis | tight |
| **Brindes SP (bag + silk, SP)** | **20 dias úteis** ≈ 28 corridos | **NO — exceeds the 20-day deadline on its own** |
| Zen Brindes (bag, SP) | 15 days | tight, leaves ~5 days |
| **Caicó Brindes (bag, RN)** | **30 days** | **NO** |

**This is a real constraint, not a footnote.** The printed *bag* is the long pole: the two
suppliers that publish a bag lead time both **exceed or consume** a 20-day municipal deadline
before assembly, inspection or freight. Vinyl stickers are fast and are not the risk.
Artwork approval time is published by nobody and is additional.

---

## 6. Blocked-sources register

Recorded as blocked. Nothing was worked around, no TLS verification was disabled, no login
was created.

| Source | What blocked it | What was lost |
|---|---|---|
| `tocadosilk.com.br/gravacao-de-tela-serigrafia` | **HTTP 403**, also to a normal browser UA | the matriz/tela **setup fee** — the single most wanted missing number |
| `revendajn.com.br/produto/adesivo-transparente` | **login wall** — "Você precisa estar logado… para visualizar os preços" | SP resale-tier vinyl prices |
| `paulistacartoes.com.br/adesivo-vinil-transparente` | **JS-only** pricing ("Buscando dados") | quantity-tier die-cut sticker table |
| `graphicstore.com.br/…recorte-eletronico` | unrendered template variables | die-cut price table |
| `lotuslogistica.com/…montagem-de-kits-promocionais` | **connection reset** | copacker personalisation check |
| `embalagens.cotanet.com.br/sacola/sacola-silk-screen` | **expired TLS certificate** — not bypassed | silk-on-bags price |
| `mpplog.com.br/promopack` | DNS does not resolve | copacker personalisation check |
| `multimarksdigital.com.br/estamparia` | DNS does not resolve | a page titled "TABELA DE PREÇOS" |
| `360imprimir.com.br/saco-tipo-mochila` | "Produto temporariamente indisponível" | published bag price curve |

### Two UF traps caught

- **Gráfica Paulista Cartões** — trades as "Paulista", advertises "Adesivo de Vinil – São
  Paulo", uses an (11) number. CNPJ 12.019.274/0001-01 resolves to **CONFORMÁTICA
  ACABAMENTOS GRÁFICOS LTDA, Uberaba/MG**.
- **Luminati Brindes** — lists Rio de Janeiro, **São Paulo**, Curitiba and Porto Alegre as its
  cities. CNPJ 29.065.741/0001-32 resolves to **ORIGINAIS DISTRIBUIDORA DE BRINDES LTDA,
  Serra/ES**.

Both would have been recorded as SP on the site's own word. Neither is.

---

## 7. What only a quote can settle

1. **The finished branded bag price at 100 / 500 / 5.000.** The whole of line 01.1. Nobody
   publishes it and, given §2, nobody can — the article is made to order. Targets:
   **Idaplast** (SP, real bag factory, publishes the colour scale), **Bolsavel** (SP,
   Americana), **Brindes SP** (SP, known lead, but its own 20-dia-útil lead time is a problem),
   **JC Promocionais** (SP, sells this exact category).
2. **The setup / matriz / clichê fee, per colour.** Never observed. Decides the 100-kit case
   almost by itself. Must be asked as *"quantas telas, a quanto cada, cobrado uma vez?"*
3. **The colour count of the three logos.** Programa Mãe Itaquá, Governo do Estado de SP,
   Prefeitura de Itaquaquecetuba. Price scales on this and on nothing else the market publishes.
   **Get the artwork before asking for any bag quote** — a quote without it is meaningless.
4. **Sticker application onto polypropylene.** Not published by anyone, including all 24
   surveyed co-packers. Ask **Alô Sara Manuseios** (the only firm that names "aplicação de
   vinil") and **Raotech**. Ask per piece for 3 stickers on a curved 22 L tub. The founder can
   apply ~150–250 kits herself, so this only truly binds at 500+.
5. **Whether the vinyl meets the spec, in writing.** No printer publishes the edital's three
   hard requirements: **12 months' durability without colour loss or peeling**, **adhesion to
   polypropylene without bubbling**, water resistance through cleaning. Segunda Via's published
   claim ("podem molhar, lavar, ir ao micro-ondas, congelar") is suggestive and is **not** the
   warranty the edital demands. A supplier declaration is a habilitação risk, not just a price.
6. **A real 5.000-unit vinyl price.** R$80/m² is a 500-unit list rate. 116 m² is a different
   conversation and no step is published.
7. **Whether ANY printer takes customer material.** Not one page in this sweep says yes. If
   one does, the plain-bag model returns; if none does, §2 stands permanently.
8. **Whether the SP/RJ vinyl gap survives ICMS.** R$0,92/kit ≈ R$4.600 over 5.000 kits. Under
   LC 123 art. 13 §1 XIII h the differential can erase it. Stickers are light, so freight will
   not — this is a tax question, not a logistics one.

---

## 8. Effect on the Step 0 gate

`docs/ITAQUAQUECETUBA_REAL.md` §8 held that the gate cannot be called until the BOM is
re-priced and the two branded lines are quoted. **That still holds**, and this survey narrows
it rather than closing it:

- The **banheira** branding is now bounded: **R$1,86–2,78/kit of printing**, plus an
  unpriced application step, against an edital estimate that leaves R$7,20–18,01 of headroom
  on that line. This line is unlikely to break the model.
- The **mochila** is the open risk, and it is larger than "R$52,27 plus some printing". The
  edital estimates the branded article at **R$98,51** — 88% above the plain bag in the cost
  table — and at the observed 75,42% clearing ratio the winner realised about **R$74,29** on it.
  **Until a bag factory quotes the real article, line 01.1 should be carried at the edital's
  estimate, not at R$52,27.** Carrying it at R$52,27 understates the BOM by roughly R$46/kit,
  which is about R$230.000 across 5.000 kits.
