# Supplier Shortlist — second sources against the Emilio concentration

**Compiled 2026-09-19.** Public catalogue and website reading only. **Nobody was contacted**
— no email, no form, no WhatsApp, no phone, no registration, no account, no purchase.
TLS verification was never disabled; every site that refused a request is named in
§4 below rather than worked around. **Every CNPJ in `suppliers_shortlist.csv` was
resolved at `https://publica.cnpj.ws/cnpj/{cnpj14}`** — no UF in this document rests on a
trading name or on a site's own "São Paulo" claim. Where something was not read directly
the cell says `UNVERIFIED`, not a number.

---

## 1. Headline

**17 new CNPJ-verified candidates: 7 layette, 2 puericultura/plásticos, 3 higiene, 5 kit bag.
13 of the 17 are SP; 4 are not (2 SC, 1 PR, 1 ES).** Three of the SP ones sit outside the
capital — Valinhos, Ribeirão Preto and Santo André — so no ICMS hurdle, but not a Brás walk-in
either.

The concentration in risk #15 is now covered in *structure* — every category has at least one
verified alternative CNPJ — but only thinly in *price*. Four BOM lines gained a second source
whose price can actually be read today. The rest gained a name and an address.

**The finding that matters most is not on the shortlist — it is what the shortlist says about
Emilio.** Paulimar Atacadista (Pari/Brás, public prices, no login) stocks the *same Minasrey
manufacturer references* the cost table already cites, and is **dearer than Emilio on every
comparable line**: toalha fralda 3 un R$18,38 against Emilio's R$10,26; pano de boca 2 un
R$13,75 against Emilio's 3 un for R$5,55. Era Uma Vez, also SP and also publicly priced, wants
R$14,90 for a body manga longa RN against Emilio's R$7,56, and R$129,90 for a cobertor against
Emilio's R$12,15. **Emilio is not a mid-market price that a second source will undercut; it is
at or near the floor.** Diversifying away from it should be budgeted as a cost of resilience,
not modelled as a saving. The repo's framing of a second source as "a price benchmark" is
answered: the benchmark says the incumbent is cheap.

The second real finding is a credit one. **MaxQualy publishes "Boleto 7 dias com 2% de desconto"
with a R$300 minimum, openly, on its lojista storefront** — the second published route to
deferred payment anywhere in this repo, after Brascol, and unlike Brascol's *boleto parcelado*
it is not advertised as CNAE-gated. That speaks to risk #10 ("every priced supplier is prepay")
more directly than anything in the layette category does.

---

## 2. Per-category tables

Full columns, notes and caveats live in `data/suppliers_shortlist.csv`. `Prices` = whether a
price can be read without registering.

### 2.1 Layette textiles — 7 candidates (6 SP, 1 SC)

| Trading name | Razão social | CNPJ | UF / city | Prices | Min. order | Lines it could cover |
|---|---|---|---|---|---|---|
| **Paulimar Atacadista** | PAULIMAR CONFECCOES LTDA | 60.656.782/0001-43 | **SP** / São Paulo (Pari) | **Public** | none published | body, pagão, cueiro, pano de boca, meias, toalha, cobertor, **sacola** |
| Yora Atacado | BW MODAS LTDA. | 00.213.833/0007-26 | **SP** / São Paulo (Pari) | Login-gated | **R$450** online / R$800 loja | body, pagão, cueiro, pano de boca, toalha, cobertor, meias |
| Mafessoni Baby & Kids | CONFECCOES MAFESSONI LTDA. | 96.222.781/0001-38 | **SP** / Mairiporã | Login-gated | none published | body, pagão — **this is the factory behind Emilio's body** |
| Era Uma Vez | ROUPAS DE BEBE E ENXOVAIS LTDA | 38.479.807/0001-21 | **SP** / São Paulo | **Public** | none published | body, pagão, cobertor, cueiro, meias — **retail price band** |
| Markha Baby | MARKHA ENXOVAIS E PRESENTES PARA BEBE LTDA. | 03.383.226/0001-07 | **SP** / São Paulo | UNVERIFIED | UNVERIFIED | body, cobertor (categories present, no price rendered) |
| Paravati Atacado | PARAVATI CONFECCAO E DISTRIBUIDORA DE ROUPAS LTDA | 40.826.972/0001-54 | **SP** / São Paulo (Brás) | Login-gated | none published | UNVERIFIED — no layette category confirmed |
| Dugu Atacadista | VOIGTEX TOALHAS E VARIEDADES LTDA | 44.073.063/0001-43 | **SC** / Joinville ⚠ | **Public** | none published | cueiro, pano de boca, toalha, **kit enxoval pronto** |

⚠ Non-SP. LC 123 art. 13 §1 XIII (h) — must beat an SP supplier by **more than ~6 points** to be
genuinely cheaper.

### 2.2 Puericultura / plásticos — 2 candidates (both SP)

| Trading name | Razão social | CNPJ | UF / city | Prices | Min. order | Lines |
|---|---|---|---|---|---|---|
| **Plasútil** | PLASUTIL-INDUSTRIA E COMERCIO DE PLASTICOS LTDA | 56.450.877/0001-39 | **SP** / São Paulo (matriz) | Quote only | **R$2.000** (published) | banheira 21 L, saboneteira |
| ISSAM | ISSAM IMPORTACAO E EXPORTACAO LTDA | 00.327.385/0003-68 | **SP** / São Paulo (Pari) | Login-gated | none published | saboneteira (porta-sabonete) only |

**This is the weakest category and it should be read as a gap, not a result.** Plasútil's R$2.000
minimum is roughly 15% of the top of the capital band in `config/capital.yaml` for a single line
item, and its CNPJ is the one number in this whole exercise that the company does **not** publish
on its own site (see §5). ISSAM covers a R$3,01 line and nothing else. Neither is a working
substitute for Emilio on `banheira_lisa` or `kit_higiene_bebe` today.

### 2.3 Higiene e perfumaria infantil — 3 candidates (all SP)

| Trading name | Razão social | CNPJ | UF / city | Prices | Min. order | Terms | Lines |
|---|---|---|---|---|---|---|---|
| **MaxQualy** | MAXQUALY - COMERCIO E LOGISTICA DE COSMETICOS LTDA | 53.748.042/0001-71 | **SP** / Valinhos | **Public** (lojista storefront) | **R$300** | **Boleto 7 dias, 2% desconto** | shampoo, sabonete, óleo, kits |
| ABC Fraldas | **GALPAO DAS FRALDAS LTDA** | 41.666.720/0001-78 | **SP** / Santo André | Partial (Mercado Shops → ML) | none published | none published | fralda RN, toalhas umedecidas |
| 7Y Distribuidora | 7Y DISTRIBUIDORA DE FRALDAS LTDA | 07.018.219/0001-67 | **SP** / São Paulo (Brás) | **No** | none published | none published | fralda RN, toalhas umedecidas |

### 2.4 The kit bag — 5 candidates (2 SP, 1 SC, 1 PR, 1 ES)

| Trading name | Razão social | CNPJ | UF / city | Prices | Min. order | Personalisation |
|---|---|---|---|---|---|---|
| **Brindes SP** | BRINDES SP CONFECCOES E COMERCIO DE BOLSAS E BRINDES LTDA | 46.033.832/0001-05 | **SP** / São Paulo | Quote only | **50 un** (20 un térmica) | **sublimação, silk-screen, bordado, transfer** |
| Luna Baby Bolsas | SM BOLSAS E ACESSORIOS LTDA | 48.290.986/0001-08 | **SP** / Ribeirão Preto | **Public** | none | bordado do nome — **R$745–837, priced out** |
| Coutre Bolsas | V M INDUSTRIA E COMERCIO LTDA | 28.165.813/0001-50 | **SC** / Guarujá do Sul ⚠ | UNVERIFIED | UNVERIFIED | offered; corporate/brasão work not established |
| Fazendo Arte Baby | TICK TACK TOE ARTIGOS DO VESTUARIO LTDA | 05.769.392/0001-71 | **PR** / Curitiba ⚠ | **Public** | none | own manufacture — **from R$196,90, priced out** |
| Luminati Brindes | ORIGINAIS DISTRIBUIDORA DE BRINDES LTDA | 29.065.741/0001-32 | **ES** / Serra ⚠ | Quote only | ~500 peças | silk, bordado, digital, patches — no maternity line |

**Conclusion for this line: the consumer "bolsa maternidade" market is the wrong market.**
Its floor is R$196,90 and its median is far above; Emilio's plain mochila is R$52,27 and the whole
kit BOM is R$176–199. Only two routes are in budget: a **wholesale sacola** (Paulimar's Kit Sacola
e Frasqueira, R$49,90, publicly priced) for an unbranded bag, or the **promotional/confecção
route** (Brindes SP, 50-unit minimum, four marking methods) when the edital wants the brasão.
Brindes SP publishes no price of any kind, so `mochila` remains **unpriced at a personalised
spec** — but it now has a named, CNPJ-verified, SP supplier with a minimum small enough for the
50–300-kit lots risk #37 recommends.

---

## 3. BOM lines that STILL have only one source

Strict test: a *second* source counts only if it is a different CNPJ, verified, **and** its price
for that line can be read today. A supplier that stocks the category behind a login is structure,
not a benchmark.

### 3.1 Lines that now have a genuine, readable second price ✅

| Line | Was | Now also | New price read |
|---|---|---|---|
| `pano_de_boca` | Emilio R$1,85/pc | Paulimar | R$13,75 / 2 un — **dearer** |
| `toalha_banho_infantil` | Emilio R$3,42/pc | Paulimar | R$18,38–19,34 / 3 un — **dearer** |
| `mochila` | Emilio R$52,27 | Paulimar (sacola + frasqueira) | R$49,90 — **cheaper, first real alternative** |
| `body_manga_longa` | Emilio R$7,56/pc | Era Uma Vez | R$14,90 — **dearer, retail band** |
| `pagao` | Emilio R$15,34 | Era Uma Vez (macacão) | R$9,99–29,90 — spec not matched to a 3-peça pagão |
| `cobertor_infantil` | Emilio R$12,15 | Era Uma Vez | R$129,90 — a ceiling, not a competitor |

### 3.2 Lines that gained a supplier but **no second price** ⚠

`cueiro`, `par_de_meias` (Paulimar and Yora both stock them; no price captured for either line) ·
`fralda_descartavel_rn` and `toalhas_umedecidas` (7Y and ABC Fraldas both carry them; neither
publishes a price on its own storefront) · `shampoo_infantil`, `oleo_infantil`, `sabonete_liquido`,
`kit_higiene_bebe` (MaxQualy carries the categories; individual baby-line prices were not opened) ·
`saboneteira` (ISSAM, login-gated; Plasútil, quote only).

### 3.3 Lines still effectively **single-sourced on price** ❌

- **`banheira_lisa`** — Emilio R$18,90 remains the only price this repo can read. The cost table's
  Yanai R$17,89 / Brascol R$18,05 cross-check stands, but Brascol is login-gated so that figure was
  never verified at source. The only new candidate, Plasútil, is quote-only behind a R$2.000 minimum.
  *Independent corroboration gained:* Cajovil's own catalogue lists refs **0361, 0362 and 0858 as
  20 L**, which confirms the `#0362 / 20 litros` spec in `cost_table.csv` from the manufacturer side.
- **`kit_higiene_bebe`** (R$5,20) and **`saboneteira`** (R$3,01) — still Emilio-only on price. The
  puericultura category is where this sweep failed.
- **`kit_enxoval`** — still **UNPRICED**, as `cost_table.csv` says. One thing changed: Dugu
  Atacadista (SC) is the only supplier found anywhere that sells a ready-assembled *"kit enxoval
  10 peças"*. Its product page could not be read (see §4), so no price is claimed — but for a line
  that had no supplier at all, that is a lead worth following.

**Emilio still carries 11 of 16 priced lines. After this work it is the sole *readable price* on
roughly 8 of them.** The change is that every one of those 8 now has at least one named,
CNPJ-verified, mostly-SP company behind it that could be asked.

---

## 4. Blocked / unreachable sources register

Recorded, not worked around. No TLS check was disabled and no wall was circumvented.

**Refused the request outright**

| Source | What happened | Why it mattered |
|---|---|---|
| `loja.tambasa.com` | **HTTP 403** to both direct fetch and the page reader | Lists the *exact* Cajovil 20 L banheira — would have been a clean cross-check on `banheira_lisa`. (Tambasa is MG in any case.) |
| `www.novacatalogo.com.br` (Nova Atacado, Brás) | **HTTP 403**; the business also states orders are taken only by WhatsApp | Enxoval infantil atacadista — out of reach without contact, which is prohibited |
| `www.lojadasfraldas.com` | **HTTP 403** | Diaper distributor |
| `www.mercadaodasfraldas.com.br` | **HTTP 403** | Diaper distributor |
| `billkids.com.br` | Served a rate-limiter interstitial (`limiter.performflow.com`) | Brás enxoval lead |
| `www.vicemar.com.br` | **HTTP 503** on every attempt | Brás enxoval lead |
| `www.dianakids.com.br` | Connection failed (no HTTP response) | Brás lead |
| `bolsaspersonalizadas.com.br` | Connection failed (no HTTP response) | Bag lead |
| `www.cajovil.com.br` (root) | Connection failed on direct fetch; a sub-page rendered via the page reader | Manufacturer of Emilio's banheira; publishes **no CNPJ and no prices** |

**Reachable but JS-gated / login-gated, so unusable as a price source**

- `www.atacadaodasfraldas.com.br` — renders `Carregando preço…` for every item and states
  *"Esta loja está em Implantação"*.
- `www.blattfraldas.com.br` — 30-year Brás diaper distributor, prices behind login, **no CNPJ
  published**.
- `www.acelerapdv.com.br` — *"cadastre-se para ver nossos preços"*, Interlagos/SP address, **no
  CNPJ published anywhere read**.
- `brascol.com.br` — the known wall, already on record in `data/supplier_credit_policy.md`.

**Reachable, relevant, but no CNPJ published on any page read → leads, NOT candidates**

`www.laroya.com.br` (Nuvemshop; public prices and it stocks *every* layette line — the single most
promising lead left open) · `www.lukinhasbaby.com.br` (Tray; public prices, enxoval + puericultura) ·
`www.l4.com.br` (public prices, **R$300 minimum published**, Brás) · `www.bbvindo.com.br` ·
`textilabril.com.br` · `www.ascona.com.br` · `www.lambariatacado.com.br` (checked and **excluded** —
no enxoval line at all) · `www.jcpromocionais.com.br`, `jagb.com.br`, `bolsavel.com.br`,
`doceanjobolsas.com.br`, `www.maternalbags.com.br` (bag makers).

None of these is in the CSV. Without a CNPJ their UF cannot be proved, and an unproved UF is
worth nothing here — see §5.

---

## 5. Three things that contradict, or sharpen, what the repo already believes

1. **`data/supplier_credit_policy.md` concludes Brascol is "the *only* one … with a published route
   to deferred payment."** True of the three toiletries suppliers it examined; **not true of the
   market.** MaxQualy (SP/Valinhos, CNPJ 53.748.042/0001-71) publishes *"Boleto 7 dias com 2% de
   desconto"* against a R$300 minimum, on an open storefront, with no CNAE condition stated.
   The credit-policy conclusion should be narrowed to its sample.

2. **A site's stated address is not its UF — demonstrated twice in this sweep.** Luminati Brindes
   presents Rio de Janeiro and São Paulo offices; `publica.cnpj.ws` puts ORIGINAIS DISTRIBUIDORA DE
   BRINDES LTDA in **Serra/ES**. And ABC Fraldas' own footer says *"Abc Fraldas Ltda CNPJ
   41.666.720/0001-78"* while the registry returns **GALPAO DAS FRALDAS LTDA** for that number — a
   trading name that is not the razão social, which is exactly the kind of label/identifier mismatch
   `RISK_REGISTER.md` §B4 warns about, and which will matter the first time a habilitação document
   is filled in. **The one CNPJ here not published by its own owner** is Plasútil's: it was taken
   from a third-party listing and confirmed only by razão-social match at the registry. It is flagged
   as such in the CSV and should be re-confirmed from a nota fiscal before it is relied on.

3. **The login wall is the norm in this trade, not a Brascol quirk.** Of the layette atacadistas
   found, Yora, Paravati, Mafessoni and Brascol all gate prices; Paulimar is the exception that
   proves it. This raises the odds on risk #29 (`Price: null` → rows silently vanish) and means any
   price-diversification plan runs through a cadastro sooner or later — which is precisely the
   registration that risk #15 already says is the cheapest fix and which was out of scope here.
