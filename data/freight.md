# Freight SP → Northeast/North — first measured numbers

Measured 2026-09-19 (UTC 18:25–18:45). Public sources and public calculators only. No carrier was
contacted, no quote requested, no account created, nothing paid. Companion data:
`data/cost_freight.csv` (453 rows; every row carries its URL, timestamp and `is_estimate`).

Vocabulary used throughout:
- **MEASUREMENT** = a number read from a public calculator run by me, or from a table the carrier
  itself publishes.
- **ARITHMETIC** = my multiplication of measurements (flagged `is_estimate=TRUE` in the CSV).
- **UNVERIFIED** = could not be read from a public source; what would settle it is stated.
- Blog posts and help-center articles of third parties are quoted only for context and are
  labelled "not a measurement".

---

## 1. Method

| Source | What it is | How it was read | Status |
|---|---|---|---|
| Correios "Calculador de preços e prazos nacionais" — https://www2.correios.com.br/sistemas/precosPrazos/ | Official public calculator, **à vista (balcão)** prices, no contract | The page is a plain HTML form (`prazos.cfm`). Chromium/Playwright could not be used (see blocks), so the form was submitted as HTTP POST with **all 92 fields the page itself sends**, origin CEP 03005-000 (Rua do Lucas, Brás — echoed back by the calculator), posting date 19/09/2026, "Outra embalagem", format caixa. 80 calls, 80 valid results; the calculator echoed origin and destination addresses on every result, which is how the destination CEPs were validated. | MEASUREMENT |
| Melhor Envio public calculator — https://www.melhorenvio.com.br/api/v2/calculator (the endpoint behind the "Calcular frete com desconto" box on https://melhorenvio.com.br/) | Public, **pre-registration**, no login, no CNPJ, no contract, no minimum. Returns Correios (PAC/SEDEX/Mini Envios), Jadlog (.Package, .Package Centralizado, .Com), Total Express Standard, Loggi (Express/Coleta/Ponto), JeT Standard, LATAM Cargo éFácil, Buslog, Azul Cargo | 32 GET calls, 198 priced options | MEASUREMENT (site disclaimer: "*Os valores são estimativas e podem variar devido a taxas, cubagem, quantidade de envios e outros fatores") |
| STC Transportes "Tabela de Fretes" — https://stctransportes.com.br/tabela-de-fretes/ | A road carrier's own published price table, SP (Guarulhos) → Fortaleza and CE interior, both per-parcel ("De Mão em Mão", 1–30 kg) and LTL (31–32.000 kg, R$/ton) | Read from the page | MEASUREMENT (published table) |
| Correios rule pages and contract terms (URLs in §2) | Official | Read | Rules |
| Carrier public pages (Braspress, Jadlog, Melhor Envio, SuperFrete, Total Express, FedEx/TNT, Kangu) | Public wording on minimums / how to quote | Read | §6 |

Destination CEPs used (all echoed back by the Correios calculator as the capital's centre):
Recife 50010-000 (Av. Guararapes, Santo Antônio) · Fortaleza 60010-000 · São Luís 65010-000 ·
Belém 66010-000 · Salvador 40010-000 · Belo Horizonte 30130-000 · Aracaju 49010-000 · Natal 59010-000.

Parcel configurations measured:
- **A. 60×40×40 cm, 3 kg** — the assembled kit as one box (0,096 m³). Cubic weight 96.000/6.000 = **16 kg**.
- **B. 60×40×40 cm, 16 kg** — same box at its cubic weight, to show whether actual weight matters at all.
- **C. 40×30×30 cm, 3 kg** — a denser hypothetical (0,036 m³, cubic 6 kg). Not achievable with the bathtub (seller-stated tub box ≈ 0,047 m³), included to make the dimensional effect visible.
- **D. 30×25×20 cm, 3 kg** — cubic 2,5 kg → billed at actual weight (control).
- **E. Split kit = 60×40×20 cm @ 1 kg (tub box, 0,048 m³, cubic 8 kg) + 40×30×25 cm @ 2 kg (soft goods, cubic exactly 5 kg → billed at actual)** — the realistic alternative packing.

### Sites that blocked or failed (record)
| Site | What happened |
|---|---|
| https://www.correios.com.br/enviar/precos-e-prazos/ | HTTP 404 — the calculator now lives at www2.correios.com.br/sistemas/precosPrazos/ |
| Playwright/Chromium (pre-installed at /opt/pw-browsers) | `net::ERR_CERT_AUTHORITY_INVALID` on every HTTPS page: the session's egress proxy re-terminates TLS and Chromium's NSS store did not contain its CA; `certutil` is not installed and `apt-get install libnss3-tools` returned 404. TLS verification was **not** disabled; the Correios form was submitted over plain HTTP POST instead (identical to what the browser sends). |
| https://www.totalexpress.com.br/ (all paths) | HTTP 400 JSON `"The 'User-Agent' header is required"` even with Chrome and Firefox User-Agents — WAF block. Total Express prices were obtained via Melhor Envio instead. |
| https://www.fedex.com/pt-br/open-account.html, …/shipping/rates/quote-request.html, …/shipping-tools/freight-quote.html, FedEx domestic T&C PDF | "FedEx \| System Down … It appears you don't have permission to view this webpage" (Akamai). tnt.com quote pages: 404. |
| https://centraldeajuda.melhorenvio.com.br/… | HTTP 403 (Zendesk). melhorenvio.com.br home and API worked. |
| https://www.kangu.com.br/ | Redirects to https://www.mercadolivre.com.br/ajuda/38279 which is a JS shell to curl and 403 to the fetch tool. |
| https://www.jadlog.com.br/jadlog/simulacao | Public simulator exists (JSF/PrimeFaces + reCAPTCHA on page); programmatic submits returned `javax.faces.application.ViewExpiredException`. Needs an interactive browser. Jadlog prices were obtained via Melhor Envio instead. |
| https://www.braspress.com.br/w/cotacao/view | Login wall ("ENTRAR / Solicite seu acesso"). |
| https://www.correios.com.br/para-voce/correios-de-a-a-z/limites-de-dimensoes-e-peso and wap.correios.com.br/…/limites-de-dimensoes-e-peso | 404 / redirect to home. The 30 kg limit was taken from the SEDEX service page instead (§2). |

---

## 2. Correios public rules (official pages)

**Dimensional weight — formula and threshold.** Source: "Termo de Condições de Prestação de Serviços
de Encomendas Nacionais (SEDEX e PAC)", correios.com.br,
https://www.correios.com.br/enviar/precisa-de-ajuda/contrate-os-correios/arquivos/contratos-formalizados-ate-fevereiro-de-2020/18-termo-de-condicoes-de-prestacao-de-servicos-de-encomendas-nacio-ns-sedex-e-pac.pdf
(read 2026-09-19; this is the pre-March-2020 contract annex, still the only Correios document on
correios.com.br that states the rule; the post-2020 "Termo de Condições Comerciais" does not repeat it):

> "6.1. O maior valor entre o peso físico (real) e o peso volumétrico (cúbico) define o preço do
> serviço de encomenda. 6.1.1. Encomenda com peso volumétrico até cinco quilogramas sempre será
> precificada pelo peso físico. … 6.3.1. O fator volumétrico para os serviços de encomenda é 6.000
> (seis mil) … (Comprimento x Largura x Altura ÷ 6.000)."

The calculator behaves exactly like this today: 60×40×40 at 3 kg and at 16 kg price identically
(all 8 capitals, PAC and SEDEX); 40×30×25 at 2 kg (cubic exactly 5 kg) prices as 2 kg.

**Size limits.** Source: https://www2.correios.com.br/sistemas/precosprazos/Formato.cfm (the
calculator's own "Limites de dimensões de embalagens", read 2026-09-19): pacote/caixa for SEDEX 10,
SEDEX 12, SEDEX and PAC — comprimento 11–100 cm, largura 6–100 cm, altura 0,4–100 cm, **soma
C+L+A 17,4–200 cm**. Same limits on https://www.correios.com.br/enviar/encomendas/saiba-mais-nacional
("maior dimensão (C ou L ou A): 100 cm; soma máxima das dimensões (C + L + A): 200 cm").

**Weight limit.** https://www.correios.com.br/enviar/encomendas/saiba-mais-nacional (SEDEX page,
read 2026-09-19): "e) Peso: • 30 kg". The calculator's own JS refuses > 30 kg for SEDEX 10/12 and
> 10 kg for SEDEX Hoje. So the cap is **30 kg, not 29 kg**. A higher cap for contract clients
(third parties say 50 kg) is UNVERIFIED — no correios.com.br page reachable today states it.

**Consequence for the kit:** one 60×40×40 kit = 16 kg cubic. Two kits in one box (60×80×40 or
120×40×40) = 32 kg cubic, over the 30 kg cap (and 120 cm over the 100 cm side limit). **One
parcel per kit is forced** unless the kit is repacked smaller.

**Contract — who can sign, minimums, tiers.** Sources, all read 2026-09-19:
- https://www.correios.com.br/enviar/precisa-de-ajuda/contrate-os-correios — "Nossos pacotes de
  serviços reúnem produtos e condições comerciais … **\*Sem exigência de valor mínimo mensal**";
  "Isenção da cota mínima nos dois primeiros ciclos de faturamento".
- https://www.correios.com.br/enviar/precisa-de-ajuda/perguntas-frequentes-como-contratar-os-correios —
  "O Correios Fácil é um sistema … que permite celebração de contrato comercial de forma 100%
  online." "Quais os documentos necessários…? Contratação via Correios Fácil: **Certificado digital
  e-CNPJ**". "A contrapartida é o valor mínimo que sua empresa deve consumir com os Correios para
  poder usufruir das tarifas mais reduzidas. Esse valor varia de acordo com o serviço." Credit for
  a-faturar contracts: "O crédito inicial, pré-aprovado é de 425 vezes o primeiro porte da carta
  comercial."
- https://www.correios.com.br/correios-empresas — "**Novo pacote Clube Correios** — Preços e
  benefícios exclusivos nos serviços de encomendas SEDEX e PAC, com pagamento realizado no momento
  da utilização dos serviços … por meio de cartão de crédito e/ou outra modalidade de pagamento
  utilizada nas postagens à vista."
- **Termo de Condições Comerciais**, version dated 09/09/2026 with appendices dated 13/08/2026
  (72 pp.): https://www.correios.com.br/enviar/precisa-de-ajuda/contrate-os-correios/arquivos/contratos-formalizados-a-partir-de-marco-de-2020/termo-de-condicoes-comerciais/@@download/file/140%20Termo_de_Condi%C3%A7%C3%B5es_Comerciais_01082025.pdf
  - Apêndice A (categories by "expectativa de receita anual", R$): BRONZE "-", PRATA 12.000,
    OURO 30.000, PLATINUM 480.000, DIAMANTE 3.360.000, INFINITE 19.200.000.
  - Apêndice D (packages, "Valor Mínimo Mensal (R$)"): **Clube Correios: pagamento no ato = Sim,
    valor mínimo = "-", redução de preço = "-"**; **Platinum: valor mínimo "-", redução de preço
    "-"**; **Diamante Start 1: R$ 100.000 mensal**, redução de preço Sim; Diamante Start 2:
    200.000 mensal; Diamante 1–4: 280.000 / 440.000 / 800.000 / 1.200.000 (cobrança semestral);
    Infinite 1–8: 1.600.000 … 500.000.000.
  - Apêndice C ("benefício de diferenciação de preços"): for **PAC, SEDEX, SEDEX 10/12, Mini
    Envios** the columns Clube Correios and Platinum show "-" = "Sem aplicação de redutores de
    preços"; Diamante Start 1 onward show "✓".
  - §6.1(b): "Isenção de cobrança de complementação financeira do valor mínimo mensal, por 2 (dois)
    ciclos de faturamento … a cada período de 12 (doze) meses".
  - §3.2.2.1(b) (penalty clause): "Para os clientes dos pacotes PLATINUM e CLUBE CORREIOS … apenas
    os serviços de SEDEX e PAC, com aplicação dos preços equivalentes à modalidade à vista (de
    balcão)."
  - Footnote 3, Apêndice D: "Para clientes novos é exigido desempenho mínimo de 20,65% superior ao
    valor mínimo mensal do pacote contratado" (applies to the Packet 200 benefit only).
- Older list on https://www.correios.com.br/enviar/precisa-de-ajuda/saiba-mais-como-contratar-os-correios
  still says "Empresário Individual … Relação de Faturamento dos últimos 12 meses assinada pelo
  empresário e pelo contador" — inconsistent with the FAQ's "e-CNPJ only" for Correios Fácil.

**Answer on "can a new CNPJ get a contract with no volume?"** Yes on paper: Correios Fácil is
online, needs an e-CNPJ, and the Clube Correios and Platinum packages carry no valor mínimo. **But
the same terms mark those two packages as "sem aplicação de redutores de preços" for PAC and SEDEX;
the first package with reducers (Diamante Start 1) requires R$ 100.000 of postage per month.** What
Clube Correios actually charges for PAC relative to balcão is therefore UNVERIFIED (Correios
markets "preços exclusivos"; the tables sit behind the Correios Empresas login). What settles it:
sign in to Correios Empresas with an e-CNPJ and download the Clube Correios PAC table, or ask the
4003 8212 line for it — both are outside this task's rules.

---

## 3. Results by destination (MEASUREMENTS, 2026-09-19)

Prices in R$ per parcel. Correios days = dias úteis after posting (calculator). Melhor Envio (ME)
days = its `delivery_time` (range in the CSV).

### 3.1 The kit as one box — 60×40×40 cm, 3 kg (billed 16 kg cubic)

| Destination | Correios PAC balcão | Correios SEDEX balcão | PAC via ME | SEDEX via ME | Jadlog .Package via ME | Jadlog .Package Centralizado via ME | Total Express Std via ME | Cheapest option via ME |
|---|---|---|---|---|---|---|---|---|
| Recife PE | **152,60** (6 du) | 427,20 (1 du) | 133,73 (8 d) | 348,08 (3 d) | 224,20 (9 d) | 188,87 (7 d) | 278,89 (13 d) | LATAM Cargo éFácil 100,44 (2 d) |
| Fortaleza CE | **152,60** (7) | 427,20 (1) | 133,73 (9) | 348,08 (3) | 218,24 (8) | 240,31 (7) | 279,98 (12) | éFácil 114,23 (2 d) |
| São Luís MA | **188,40** (8) | 516,40 (4) | 164,71 (10) | 420,57 (6) | 242,75 (11) | 178,14 (9) | 279,43 (9) | éFácil 116,48 (6 d) |
| Belém PA | **152,60** (8) | 427,20 (4) | 133,73 (10) | 348,08 (6) | 218,24 (10) | 195,74 (10) | 294,15 (7) | PAC via ME 133,73 (éFácil 155,64) |
| Salvador BA | **132,90** (6) | 304,10 (1) | 117,50 (8) | 248,24 (3) | 180,63 (5) | 152,22 (5) | 136,15 (6) | éFácil 102,62 (2 d) |
| Belo Horizonte MG | **116,60** (5) | 226,80 (1) | 102,61 (7) | 184,76 (3) | 121,76 (5) | 113,71 (4) | 101,26 (4) | Buslog Rodoviário 65,10 (2 d) |
| Aracaju SE | **188,40** (8) | 516,40 (2) | 164,71 (10) | 420,57 (4) | 198,62 (8) | 171,99 (6) | 278,07 (6) | éFácil 106,50 (4 d) |
| Natal RN | **188,40** (7) | 516,40 (2) | 164,71 (9) | 420,57 (4) | 242,75 (9) | 221,30 (8) | 279,74 (9) | éFácil 88,09 (2 d) |

Also measured (in CSV): Loggi Express/Coleta/Ponto (Recife 143,15 / 191,50 / 124,62; not offered
to CE, RN), JeT Standard (Recife 258,86; BH 110,43), Azul Cargo (no route to any of the eight).

Reading: Correios balcão PAC is the reference; Melhor Envio's PAC is 12,4 % below balcão with no
contract (133,73 vs 152,60); Jadlog and Total Express are **dearer** than PAC for this box; the
cheapest thing on the market for a capital CEP is LATAM Cargo éFácil (air, 1–3 d, R$ 88–116), which
is offered only where the CEP is inside LATAM's delivery footprint — for interior municípios this is
UNVERIFIED.

### 3.2 Same box, 16 kg actual (dimensional-weight control)
Identical to 3.1 in every one of the 16 Correios cells (PAC and SEDEX, 8 capitals). **Actual
weight is irrelevant at these dimensions; the box is billed at 16 kg whether it holds 3 kg or 16 kg.**

### 3.3 Denser boxes, 3 kg
| Box (cubic kg) | PAC balcão PE/CE/PA | PAC balcão MA/SE/RN | PAC balcão BA | PAC balcão MG | PAC via ME PE/CE/PA | PAC via ME MA/SE/RN |
|---|---|---|---|---|---|---|
| 60×40×40 (16) | 152,60 | 188,40 | 132,90 | 116,60 | 133,73 | 164,71 |
| 40×30×30 (6) | 65,90 | 81,70 | 57,80 | 50,50 | 60,63 | 74,27 |
| 30×25×20 (2,5 → billed 3) | 49,70 | 59,60 | 44,50 | 40,10 | — | — |

Halving each side from 60×40×40 to 40×30×30 cuts the PAC price by 57 %. The bathtub prevents this
in practice.

### 3.4 Split kit (tub box 60×40×20 @ 1 kg + soft-goods box 40×30×25 @ 2 kg) — PAC
| Destination | Tub box (billed 8 kg) | Soft box (billed 2 kg) | **Kit total, 2 parcels** | vs. one 60×40×40 box | Same split via ME |
|---|---|---|---|---|---|
| Recife / Fortaleza / Belém | 79,20 | 41,80 | **121,00** | −20,7 % | 70,47 + 37,65 = 108,12 |
| São Luís / Aracaju / Natal | 98,00 | 49,80 | **147,80** | −21,6 % | 86,90 + 44,86 = 131,76 |
| Salvador | 69,40 | 37,60 | **107,00** | −19,5 % | 61,95 + 33,88 = 95,83 |
| Belo Horizonte | 60,60 | 33,60 | **94,20** | −19,2 % | 54,06 + 30,43 = 84,49 |

Two tighter boxes beat one box of air by about a fifth, because the second box drops under the
5 kg cubic threshold and is billed at its 2 kg. This assumes the tub really ships in 60×40×20
(the seller-stated 0,047 m³); the tub's actual C×L×A is UNVERIFIED — measuring one tub box settles it.

### 3.5 A road carrier's published per-parcel price (STC, SP→Fortaleza only)
https://stctransportes.com.br/tabela-de-fretes/ — "De Mão em Mão", 1 volume, 1–30 kg, cubagem
300 kg/m³ and ≤ 0,125 m³, "sem coleta na origem, incluso entrega no destino; somente para as
capitais": Convencional **R$ 29 / 49 / 79** for the 10 / 20 / 30 kg tiers; Expresso R$ 58 / 98 / 158.
The 60×40×40 kit = 0,096 m³ × 300 = 28,8 kg → 30 kg tier → **R$ 79,00 to Fortaleza**, i.e. half of
PAC balcão (152,60), but the sender must hand it in at the Guarulhos terminal and the receiver is
in the capital.

---

## 4. Per-kit arithmetic for 100 and 5.000 kits (ARITHMETIC on the measurements above)

Kit price ≈ R$ 359. Parcels per kit: **1** (one 60×40×40 box; two kits per box breaks the 30 kg /
100 cm rules) or **2** (split packing). No calculator or public table publishes a volume tier for
parcels, so at balcão or via Melhor Envio 5.000 kits cost exactly 50× the 100-kit lot.

### 4.1 Correios PAC balcão, one 60×40×40 box per kit
| Destination band | Per kit | % of R$ 359 | 100 kits | 5.000 kits |
|---|---|---|---|---|
| Salvador | 132,90 | 37,0 % | 13.290,00 | 664.500,00 |
| Recife / Fortaleza / Belém | 152,60 | 42,5 % | 15.260,00 | 763.000,00 |
| São Luís / Aracaju / Natal | 188,40 | 52,5 % | 18.840,00 | 942.000,00 |
| Belo Horizonte (for comparison) | 116,60 | 32,5 % | 11.660,00 | 583.000,00 |

**NE/N band, 100 kits: R$ 132,90–188,40 per kit = 37–52 % of the kit price.** SEDEX balcão is
R$ 304,10–516,40 per kit = 85–144 % — for MA, SE and RN SEDEX costs more than the kit.

### 4.2 Correios PAC via Melhor Envio (no contract, no minimum, pay per label)
| Band | Per kit | % | 100 kits | 5.000 kits |
|---|---|---|---|---|
| Salvador | 117,50 | 32,7 % | 11.750 | 587.500 |
| Recife / Fortaleza / Belém | 133,73 | 37,3 % | 13.373 | 668.650 |
| São Luís / Aracaju / Natal | 164,71 | 45,9 % | 16.471 | 823.550 |

### 4.3 Split kit (2 parcels), PAC
| Band | Balcão per kit | % | 100 kits | 5.000 kits | via ME per kit | % |
|---|---|---|---|---|---|---|
| Salvador | 107,00 | 29,8 % | 10.700 | 535.000 | 95,83 | 26,7 % |
| Recife / Fortaleza / Belém | 121,00 | 33,7 % | 12.100 | 605.000 | 108,12 | 30,1 % |
| São Luís / Aracaju / Natal | 147,80 | 41,2 % | 14.780 | 739.000 | 131,76 | 36,7 % |

### 4.4 Cheapest per-parcel option seen on a public calculator (LATAM éFácil via ME, capitals only)
R$ 88,09 (Natal) – 116,48 (São Luís) per kit = 24,5–32,4 %; 100 kits R$ 8.809–11.648; 5.000 kits
R$ 440.450–582.400. Availability at interior CEPs UNVERIFIED.

### 4.5 Correios with contract
UNVERIFIED (see §2). Note the scale: a 5.000-kit lot is R$ 0,6–0,9 M of PAC postage at balcão,
i.e. R$ 100.000/month for 6–9 months — exactly the Diamante Start 1 minimum, the first package whose
terms include PAC/SEDEX price reducers. The reducer percentages are not public.

### 4.6 LTL / carga fracionada, single consignee (STC published table, SP→CE only)
Per kit: 0,096 m³ × 300 kg/m³ = **28,8 kg cubado** (vs 3 kg real — cubed again, at a harsher factor
than Correios' 6.000, which is 166,7 kg/m³).

100 kits, Fortaleza capital tier (SPO/FTZ R$ 1.675,80/t; NF = 100 × 359 = R$ 35.900):
- frete-peso 2,880 t × 1.675,80 = 4.826,30 (above the R$ 131,10 minimum)
- ad valorem 0,70 % × 35.900 = 251,30; GRIS 0,30 % = 107,70
- CAT 20 + ITR 20 + despacho 20 = 60,00; pedágio R$ 2,38/100 kg × 2.880 kg = 68,54; coleta São Paulo 85,00
- **total R$ 5.398,84 → R$ 53,99 per kit (15,0 %)**, 6 days to Fortaleza

5.000 kits, same tier: 144.000 kg → 241.315,20 + AV 12.565,00 + GRIS 5.385,00 + 60 + pedágio
3.427,20 + coleta 85 = **R$ 262.837,40 → R$ 52,57 per kit (14,6 %)** (the per-kit cost is flat
because the table is linear in kg; only the fixed R$ 145 vanishes).

Interior tiers of the same table: FTZi (R$ 1.869,60/t, mín. 330, 8 days) → **R$ 59,57/kit** (100)
/ 58,15 (5.000); FTZii (R$ 3.041,06/t, mín. 440, 12 days) → **R$ 93,31/kit** (100) / 91,89 (5.000).
So the LTL band for a single consignee in CE is **R$ 53–93 per kit = 15–26 %**, before any
last-mile inside the município and before checking whether the edital's delivery point accepts a
pallet/lot rather than individual parcels. Other NE/N states: no carrier table found — UNVERIFIED;
the STC figures are one carrier's referencial table for one corridor, not a market rate.

---

## 5. What governs the price: dimensional weight (answered)
At 60×40×40 the parcel is billed at 16 kg by Correios (factor 6.000, threshold 5 kg) and at 28,8 kg
by a road LTL carrier (factor 300 kg/m³). Actual weight (3 kg) never enters the price. Every real
saving comes from cubic centimetres, not grams: the split packing (§3.4) saves ~20 %, a hypothetical
40×30×30 kit would save 57 %.

---

## 6. What the road carriers publish about minimums and quoting (exact wording, read 2026-09-19)

- **Braspress** — https://www.braspress.com/duvidas-frequentes/ : "Como faço uma cotação? Os
  clientes com negociação ativa devem acessar a página da Cotação Online. **Quem não possui
  negociação deve entrar em contato com o departamento comercial da filial BRASPRESS mais
  próxima.**" "Como é calculado o frete? O frete é calculado de acordo com a característica da
  operação do cliente, levando em consideração a distância da origem do despacho até o seu destino,
  o valor da mercadoria e as suas generalidades/taxas." "O que é cubagem? Cubagem é a cobrança pelo
  espaço ocupado de uma mercadoria." Taxes named: "Tas (Taxa de administração SEFAZ), Taxa de
  Pedágios, Gris, Taxa de coleta/entrega". **No minimum volume figure is published.** Online quote:
  https://www.braspress.com.br/w/cotacao/view = login only.
- **Jadlog** — https://www.jadlog.com.br/jadlog/servicos : "Jadlog.com — Ideal para envio rápido
  de produtos com até 30 kg vendidos pela internet." "Jadlog Package — Indicado para pequenos
  volumes B2C ou B2B com prazo rodoviário." "Jadlog Rodo — Suas encomendas até 50 kg na modalidade
  rodoviária." The commercial contact form asks "\* Quantidade de pedidos/mês" and the Pickup form
  "Média diária de envios". **No minimum is published.** A public simulator exists at
  https://www.jadlog.com.br/jadlog/simulacao (blocked to scripts, see §1). Third-party help pages
  (Melhor Envio, SuperFrete blogs — not measurements) say Jadlog has no minimum shipment count.
- **Melhor Envio** — https://melhorenvio.com.br/ : "acesso a diversas transportadoras e Correios
  de forma prática, integrada e **livre de contratos**." "Precisa ter CNPJ para se cadastrar no
  Melhor Envio? Não precisa! O cadastro … é feito usando seu CPF." "Coleta grátis via Pegaki —
  Para verificar a disponibilidade é preciso ter a **demanda mínima de 10 pedidos por coleta**."
  Disclaimer under the calculator: "\*Os valores são estimativas e podem variar devido a taxas,
  cubagem, quantidade de envios e outros fatores." Claims "até 80% mais baratos que os preços do
  balcão" (marketing; measured gap on PAC here was 12 %).
- **SuperFrete** — https://superfrete.com/ : "Usar a SuperFrete é grátis, sem mensalidades,
  **gasto mínimo** ou tarifas escondidas. Você paga só pelo frete que utilizar." "Preciso ter CNPJ
  para usar a SuperFrete? Não." No public calculator without registration was found.
- **Total Express** — direct site blocked (§1). Its "Standard" service is quoted through Melhor
  Envio at R$ 278–294 per kit to NE/N (dearer than PAC).
- **TNT Mercúrio / FedEx** — blocked (§1). A search-engine snippet of fedex.com says freight quotes
  apply "para volumes acima de 68 kg" — not read from the page, UNVERIFIED.
- **Kangu** — no longer exists: kangu.com.br redirects to a Mercado Livre help page; Melhor Envio,
  SuperFrete and Loggi blog posts (not measurements) date the shutdown to 23 Feb 2025.
- **STC Transportes** (the one carrier with a public table) — "Prazo de pagamento: conforme
  cadastro. Cubagem: 300 kg/m³." Per-parcel service "Somente para as capitais". No minimum stated;
  the LTL table starts at 31 kg.

---

## 7. Contradictions with the brief, and open items
1. Correios' parcel cap is **30 kg**, not ~29 kg (official SEDEX page and the calculator's own JS).
2. "Every B2B road carrier refuses to quote without a contract" is too strong: Melhor Envio's public
   calculator quotes Jadlog, Total Express, Loggi, JeT, LATAM Cargo and Buslog with no login;
   Jadlog runs a public simulator; STC publishes its whole table. What is true: Braspress, Total
   Express and FedEx/TNT **direct** are closed to a new CNPJ without a commercial contact.
3. Kangu is gone (Feb 2025).
4. "Correios contract with no minimum" exists (Clube Correios, Platinum), but the published terms
   give those packages **no PAC/SEDEX price reducers**; reducers start at R$ 100.000/month.
5. The Northeast is not one price: MA/SE/RN are 23 % dearer than PE/CE/PA by PAC, and BA is 13 %
   cheaper. A single bid price across municípios must be set against the R$ 188,40 corner, not
   the R$ 152,60 middle.
6. SEDEX is not an option: at MA/SE/RN it exceeds the kit price.
7. Open: prices above are for **capital** CEPs. Correios prices by CEP range and interior municípios
   may fall in a different band; the same form POST can be re-run against the editais' CEPs
   (UNVERIFIED until done). Whether the edital's delivery point is one municipal address (which
   makes LTL at ~R$ 55–95/kit the natural mode) or door-to-door to families (parcels) is
   UNVERIFIED — read the "local de entrega" clause of each edital.
