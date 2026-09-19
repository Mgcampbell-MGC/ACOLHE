# Co-packing / kit assembly in São Paulo — published-source survey

Compiled 2026-09-19. Catalogue and website reading only. Nobody was contacted, no
form was filled, no quote requested, no registration made, nothing spent. Every UF
below was resolved by fetching `https://publica.cnpj.ws/cnpj/{cnpj14}`; a trading
name was never trusted as an address. Where a company does not print its CNPJ,
the number was located via a directory search and then verified at the API, and
this is said explicitly. Companion table: `data/cost_copacking.csv`.

Operating model being priced:

    wholesalers (Brás/Pari, SP) → co-packer (SP) → one consolidated shipment → município

Lot sizes ~100 (median) to 5.000 kits of 17–20 items (clothes, towels, plastic
bathtub, toiletries, bag). The founder can pack ~150–250 kits herself.

---

## Headline

1. **Nobody publishes a per-kit assembly price.** Not one of 20 providers examined
   prints a per-unit, per-hour, per-pallet or setup figure for kit assembly. Every
   per-kit number at 100 / 500 / 5.000 is UNVERIFIED and needs a quote.
2. **Five SP providers publish "no minimum"** (VIP Manuseios, DirectaLog, G+Ship,
   Contacto "poucas unidades", DRENG "sem contratos de longo prazo"). None publishes
   a setup fee; none says there is none.
3. **Inbound receiving with conferência is published by nine providers** (UP!, VIP,
   Envio Certo, DirectaLog, Teconlog, DRENG, G+Ship, COTLOG, Doma). VIP and DirectaLog
   explicitly say the check is against the nota fiscal (VIP: "conferência por NF,
   relatório por NF"; DirectaLog: "conferência XML vs Físico").
4. **Outbound freight — the valuable answer — splits three ways:**
   - **Carrier-3PLs that ship on their own CNPJ/fleet:** COTLOG (Cotia; own
     "transporte rodoviário fracionado" + aéreo, "coletamos no embarcador e
     entregamos no cliente"), Doma Logística (Guarulhos; own fleet, filiais in
     Vitória-ES, Itajaí-SC, **Belém-PA**, "qualquer região do Brasil"), Paulista
     Express (SBC; own fleet, but published coverage is SP capital + interior only).
     All three also list "montagem de kits". DirectaLog's CNAE is road freight
     (4930202) and it publishes "frete conforme tabela das transportadoras" with
     Correios, Jadlog and Total Express named — i.e. it re-bills carrier tables
     under its own account.
   - **Handling houses that dispatch via Correios / a transportadora / dedicated
     car** but do not say whose contract: UP! Manuseios, VIP Manuseios, Envio Certo,
     Mão na Massa (Correios/motoboy only), Teconlog ("parceiros homologados",
     in-house Correios posto avançado).
   - **Explicitly NOT shipping on their own account:** G+Ship — its published terms
     say transport is "responsabilidade exclusiva do CLIENTE … valores … pagos
     diretamente às empresas de transporte contratadas pelo CLIENTE".
   Only **Doma** publishes a North/Northeast footprint (Belém-PA branch). No
   provider publishes a Northeast rate.
5. **Turnaround published:** UP! case — 7.500 kits in 10 working days (~750/day);
   DirectaLog — marketplace prep in "até 3 dias úteis", orders until 11h ship same
   day; VIP — "prazo sempre é calculado após o recebimento de todo o material";
   Teconlog/G+Ship — same-day dispatch (D+0; G+Ship if NF by 16h).
   **Payment terms published:** only G+Ship (cartão, boleto, TED, PIX; monthly
   boleto with NF-e). All others: UNVERIFIED.
6. **Marketplace fulfilment (ML Full, Amazon FBA, Magalu, Shopee) is not usable**
   for a tender delivery: each ships only orders placed on its own marketplace;
   Amazon MCF (off-Amazon orders) lists ten countries and Brazil is not one of them.
   Melhor Envio and Loggi do give a contract-free path but per package, not per
   consolidated lot; Correios accepts "pessoas físicas e jurídicas, com ou sem
   contrato" with a 100 cm / 200 cm-sum box limit.

---

## Q1 — Price per kit assembled at ~100 / 500 / 5.000

**Published assembly prices: none.** What IS published:

| Source | What it publishes | Applies to our kit? |
|---|---|---|
| DirectaLog FAQ | Charging *model*: "armazenagem por posição/palete, picking por item, packing por pedido e frete conforme tabela das transportadoras" — no numbers | Model yes, numbers UNVERIFIED |
| G+Ship (Guarde Mais) | "não há limite de produtos, nem mínimos"; pick & pack simulator (JS slider, no static table); "Nossos preços são escalonados"; items >3 kg or fragile "podem ter custos adicionais" | Bathtub is bulky → surcharge likely; UNVERIFIED |
| DRENG | "tabelas de preços pré-fixadas, com descontos progressivos conforme o volume" — simulator page 404 | UNVERIFIED |
| Grupo SRM | Bills kit assembly labour "por peça montada ou produzida" — no rate | Labour-only model, UNVERIFIED |
| Nascra (blog) | R$ 50–200 per kit for 100–500 units — but this is a *promotional gift kit including the goods*, and the company's CNPJ is **Suspensa** at the Receita | NOT an assembly price; do not use |
| Wistor (blog) | e-commerce fulfilment R$ 4,50–19,50 per order, avg R$ 13,00 (300 orders/mo, 2 items) — excludes packaging, transport, setup | 2-item B2C pick, not a 17-item kit |
| Stokki (blog) | R$ 4–18 per order, avg R$ 11 (2023, 400 orders/mo, 2 items) | same caveat |
| Já Enviou (blog) | storage R$ 80–200/posição/mês; pick&pack R$ 4–10/pedido for 1–3 SKUs; "taxas adicionais para serviços como kits" | same caveat; confirms kits are surcharged |
| Magalu Fulfillment | manuseio "por produto vendido" R$ 0,05–3,90 (≤30 kg) by volume band; storage R$ 0,003–1,90/day by volume band | Marketplace-only; not kit assembly |
| Amazon FBA | logistics fee per unit by weight/price band; storage R$ 75/m³ (<10.000 cm³) or R$ 37,50/m³; pickup R$ 0,93–43,23/box | Marketplace-only |

**Verdict:** no per-kit band can honestly be written. The e-commerce per-order figures
(R$ 4–20) are for 1–3 light items; a 17–20-item kit with a bathtub is a different job.
Treating them as a floor is an inference and is labelled so in the CSV
(`is_inference=TRUE` on the benchmark rows).

**What settles it (ask in the quote):** price per kit assembled for lots of 100, 500,
5.000 with the real BOM (17–20 items, one 20 L bathtub, one bag); whether the bathtub
attracts a bulk/fragile surcharge; whether the client's own box/bag counts as
"packaging supplied"; and the hourly rate if they price by labour.

## Q2 — Minimum order quantity and setup / onboarding fee

| Provider | MOQ published | Setup fee published |
|---|---|---|
| VIP Manuseios | "Sem volume mínimo." | none stated |
| DirectaLog | "Não temos volume mínimo de pedidos … micro e pequenas empresas"; "Sem fidelidade" | none stated ("Integração em 24h") |
| G+Ship | "não há limite de produtos, nem mínimos exigidos" | none stated; contract + "Acordo Comercial" required per terms |
| DRENG | "Sem exigência de contratos de longo prazo ou cláusulas de fidelidade" | none stated |
| Contacto | "Poucas unidades ou grandes quantidades." | none stated |
| Teconlog | "de qualquer porte" (B2B/B2C) | none stated |
| UP!, Mão na Massa, Envio Certo, COTLOG, Doma, Paulista, Tempos, SRM, Javai, LJ | nothing on MOQ | nothing |

No provider publishes a setup/onboarding fee. G+Ship's terms require 48 h notice
before goods arrive and one barcode/SKU per unit of measure — an onboarding
*requirement*, not a fee.

## Q3 — Receive from multiple wholesalers and reconcile against a packing list?

Published, in their words:

- **UP! Manuseios** — "Recebimento de material · Separação, contagem e organização ·
  Triagem e conferência · Relatório de entrada e saída de material." Case: 667.500
  pieces sorted "por modelo, tamanho e quantidade" into 7.500 kits.
- **VIP Manuseios** — "Recebimento, conferência, armazenagem e controle com
  rastreabilidade. Relatório por NF e saldo em tempo real." Also: the client normally
  supplies the box/bag; VIP supplies tape, bubble wrap, labels, and can buy packaging
  "mediante aprovação prévia".
- **Envio Certo** — "Cuidamos do recebimento, armazenagem, montagem personalizada,
  conferência, embalagem e disparo com rastreio nacional."
- **DirectaLog** — "Coletores de dados, conferência XML vs Físico"; kits and packs
  listed under Manuseio; "Armazenagem e Distribuição B2B" is a named service line.
- **Teconlog** — "Recebimento: conferência minuciosa e entrada sistêmica imediata."
- **DRENG** — "Recebemos os produtos do seu fornecedor, realizamos uma conferência
  detalhada de cada item."
- **G+Ship** — terms 5.1.3: receipt confirmed by signature on the NF after conferência;
  6.1.1: client must announce inbound ≥48 h ahead.
- **COTLOG** — "Fulfillment: desde o recebimento, armazenagem, faturamento, expedição";
  inventory "cíclico, rotativo ou geral".
- **Doma** — "gerenciamento de estoque … rigoroso controle de estoque com inventário".

Multi-supplier inbound is not stated as such by anyone, but every one of the above
reconciles by NF, and a Brás wholesaler ships with an NF-e, so the packing list *is*
the set of NF-es. **Ask:** whether they accept N inbound deliveries from N suppliers
under one project, how they report shortages against the NF, and how long goods may
sit before assembly at no charge.

## Q4 — Do they ship, and on whose freight contract?

This is the question that decides the model. Verbatim, per provider:

| Provider | Published statement on outbound | Own contract/fleet? | North/Northeast? |
|---|---|---|---|
| **COTLOG** (Cotia) | "Porta a Porta: Coletamos no embarcador e entregamos no cliente"; own "Transporte rodoviário fracionado" and "transporte aéreo" pages; CNAE 5250804 (organização logística do transporte) | Yes — sells freight as its own service | Not stated |
| **Doma Logística** (Guarulhos) | "atende desde pequenos até grandes volumes de forma fracionada em qualquer região do Brasil"; "matriz em Guarulhos e filiais … Vitória–ES, Itajaí–SC e Belém–PA"; "ampla frota de veículos"; aéreo "24h a 72h"; CNAE 4930202 | Yes — own fleet | **Belém-PA branch published**; NE not named |
| **Paulista Express** (SBC) | "veículos próprios … caminhões baús, plataforma, carroceria, sider e carretas … cadastro de mais de 100 veículos"; rastreadores; seguro Porto Seguro; CNAE 4930202 | Yes — own fleet | Published coverage = SP capital zones + interior SP only |
| **DirectaLog** (Osasco) | "Integramos com Correios, Jadlog, Total Express e outras transportadoras"; "frete conforme tabela das transportadoras"; regions list ends "Todo Brasil"; CNAE 4930202 | Re-bills carrier tables under its own account (implied by "tabela das transportadoras" as a line in *its* invoice) — **confirm** | "Todo Brasil" listed; no NE rate |
| **Teconlog** (V. G. Paulista) | "Despachos para todo país, com roteirização e parceiros homologados"; "Posto Avançado dos Correios … dentro da nossa operação"; "Soluções door-to-door … B2B e B2C" | Carriers "homologados" — whose contract not stated | "todo país" |
| **UP! Manuseios** (SP) | "Envios correios … Envios transportadora · Envios porta a porta · Envio carro dedicado"; case: "kits foram paletizados para envio terrestre" | Not stated | Not stated |
| **VIP Manuseios** (SP) | "envio via Correios, transportadora ou carro dedicado, e relatório de acompanhamento de cada envio"; "Para grandes volumes, cotamos junto aos Correios" | Not stated — wording suggests they quote carriers on the client's behalf | Not stated |
| **Envio Certo** (SP) | "disparo com rastreio nacional" | Not stated | Not stated |
| **Mão na Massa** (SP) | "Via Correios – Sedex, Pac ou mala direta · Via motoboy" | Correios only | Correios reach |
| **G+Ship / Guarde Mais** (SP) | Terms 4.10: "É responsabilidade exclusiva do CLIENTE a contratação de transporte … valores … pagos diretamente às empresas de transporte contratadas pelo CLIENTE"; 5.1.19: may "apresentar ao CLIENTE as transportadoras que diariamente coletam" | **No** | n/a |
| DRENG, Contacto, Javai, Tempos, LJ, SRM | no carrier statement | — | — |

**So:** three SP providers (COTLOG, Doma, Paulista Express) are themselves freight
operators that also assemble kits, and one (DirectaLog) publishes that freight is
billed by it at carrier tables. Doma is the only one with a published North branch.
None publishes a Northeast price, so the NE leg remains UNVERIFIED for every provider.

**Ask:** "Do you issue the CT-e in your own name for the outbound leg, or do you
book it under my CNPJ?"; "Quote SP→(Recife, Fortaleza, Salvador, Belém, Manaus) for
100 / 500 / 5.000 kits palletised"; "What is your ad valorem / GRIS on a R$ 176 kit?"

### Marketplace and aggregator players (evidence they do not fit)

- **Mercado Livre Full** — the ML landing page (`/full`) returned 404; the seller-side
  explainer read states it handles "pedidos realizados dentro da plataforma por
  vendedores que habilitam a opção de entrega Full". ML Negócios returned 405.
- **Amazon FBA** — eligibility: active CNPJ on SEFAZ, Simples or Regime Normal, IE in
  SP/MG/PR/RJ/SC/RS/CE/DF/PE/BA/GO/ES; fee is "por unidade enviada ao cliente"; box
  limit 105 cm per side / 200 cm sum. Amazon's MCF FAQ: "MCF is available in
  Australia, Canada, France, Germany, Italy, Japan, Mexico, Spain, India, and the
  United Kingdom" — Brazil absent, so off-Amazon orders cannot be fulfilled.
- **Magalu Fulfillment** — fees are "por produto vendido" and pickup "do seu armazém
  até os CDs do Magalu"; nothing for B2B delivery.
- **Shopee Full** — eligibility (blog reading of Shopee rules): CNPJ, ≥4,5 stars,
  ≥5 orders/day, price ≥R$ 20; ships Shopee orders only.
- **Loggi** — T&C: pre-paid users (PF or PJ) pay by card/PIX/wallet without a
  contract; post-paid requires a "Proposta Comercial"; ICMS-contributor PJ must ship
  with NF-e (DC-e forbidden for them); ressarcimento cap R$ 1.000 pre-paid. Per
  package, by CEP coverage — not a consolidated lot.
- **Melhor Envio** — "livre de contratos"; "Não precisa [CNPJ]! O cadastro … é feito
  usando seu CPF"; "fretes até 80% mais baratos que os preços do balcão". Per
  package; weight/dimension limits page blocked (403).
- **Correios** — "Pessoas físicas e jurídicas, com ou sem contrato"; coleta only with
  contract; package max 100 cm longest side, 200 cm sum. A bathtub kit box will be
  near or over this.
- **Jadlog** — publishes service families (.com ≤30 kg, Package, Rodo ≤50 kg, Cargo
  aéreo B2B, Rodo Econômico fracionado B2B); the only path is a form that requires
  CNPJ and "nossa equipe comercial entrará em contato" — i.e. contract.
- **Frenet** — 403 (blocked). **DHL Fulfillment Network pricing** — HTTP/2
  INTERNAL_ERROR ×3 and 503 (blocked).

## Q5 — Turnaround and payment terms

| Provider | Turnaround published | Payment terms published |
|---|---|---|
| UP! Manuseios | Case: 7.500 kits / 667.500 pieces in 10 working days, palletised | none |
| VIP Manuseios | "O prazo sempre é calculado após o recebimento de todo o material, e estará incluso no orçamento" | none |
| DirectaLog | Marketplace prep "em até 3 dias úteis"; orders until 11h dispatched same day; "Integração em 24h" | "cobrança por serviço … sem taxas fixas elevadas"; no instrument named |
| Teconlog | "D+ZERO: Pedidos recebidos até o cut-off são despachados no mesmo dia" | none |
| G+Ship | Same-day pick/pack if payment confirmed and NF issued by 16h | Cartão de Crédito, Boleto Bancário, TED, PIX; monthly boleto + NF-e for services |
| Doma | Aéreo "entre 24h a 72h" (transport, not assembly) | none |
| DRENG, COTLOG, Contacto, Envio Certo, Mão na Massa, Tempos, SRM, Paulista, Javai, LJ | none | none |

None of the handling houses publishes prazo de pagamento (à vista / boleto N dias /
faturado). **Ask:** deposit on approval? boleto at 14/28 days? do they invoice
separately for assembly (NFS-e) and freight (CT-e)?

## Blocked / unreachable (recorded, not skipped)

| Site | What happened |
|---|---|
| lotuslogistica.com (Lotus Logística, SBC per search snippet) | "Recv failure: Connection reset by peer" ×6 across two attempts with backoff; WebFetch 503 |
| mpplog.com.br (MPP Log / Promopack) | proxy "CONNECT tunnel failed, response 502" ×6; DNS ENOTFOUND on WebFetch |
| dhl.com …/fulfillment-network/pricing.html | "HTTP/2 stream … INTERNAL_ERROR" ×3; WebFetch 503 |
| frenet.com.br | HTTP 403 (110-byte body) |
| ajuda.melhorenvio.com.br (limits article) | HTTP 403 (Cloudflare-style redirect stub) |
| basedeconhecimento.tray.com.br (ML Full article) | HTTP 403 |
| mercadolivre.com.br/full | 404; /negocios 405 |
| VIP Manuseios /contato, /politica-de-privacidade | 404 (CNPJ therefore not on site) |
| DRENG /simular-mensalidade | 404 (price simulator not reachable) |

---

## Every company examined

CNPJ/UF from `https://publica.cnpj.ws/cnpj/{cnpj14}` unless marked UNVERIFIED.
"Src" = where the CNPJ number was first seen: F = site footer, D = directory
search then API-verified.

| Company (trading) | Razão social | CNPJ | Src | UF / city (API) | CNAE (API) | Porte | What they publish | URL read |
|---|---|---|---|---|---|---|---|---|
| UP! Manuseios | UP ORGANIZACAO E EVENTOS LTDA | 43.213.105/0001-31 | F | SP / São Paulo (Paraíso) | 8230-0/01 organização de feiras e eventos | ME (2021) | Kit assembly; receiving/counting/conferência; storage; Correios/transportadora/carro dedicado; 7.500-kit case in 10 days | https://www.upmanuseios.com.br/ ; …/manuseio-e-montagem-de-kits |
| VIP Manuseios | not printed | **UNVERIFIED** | — | SP / São Paulo (site: "galpão em São Paulo") | — | — | "Sem volume mínimo"; conferência por NF; Correios/transportadora/carro dedicado; prazo after all goods received | https://www.vipmanuseios.com.br/ |
| Mão na Massa Manuseios | MAO NA MASSA PRODUCOES LTDA | 26.195.320/0001-38 | F | SP / São Paulo (Jd. Aeroporto; office Al. Santos) | 8230-0/01 | ME (2016) | Kit assembly; storage; Correios (Sedex/PAC) or motoboy | https://www.maonamassamanuseios.com.br/ ; …/logistica-promocional |
| Envio Certo Manuseios | ENVIO CERTO PRODUCOES E SERVICOS LTDA | 43.628.686/0001-72 | F | SP / São Paulo (Vila Moraes) | 8292-0/00 envasamento e empacotamento sob contrato | ME (2021) | Receiving, storage, assembly, conferência, dispatch "com rastreio nacional"; influencer-kit focus | https://www.enviocertomanuseios.com.br/manuseio-de-kits |
| DirectaLog | DIRECTALOG LOGISTICA LTDA | 22.932.742/0001-98 | D | SP / Osasco | 4930-2/02 transporte rodoviário de carga | ME (2015) | No minimum; per-service billing; kits/packs; Correios+Jadlog+Total Express; D+3 prep; "Todo Brasil"; ANVISA | https://www.directalog.com.br/fulfillment-sao-paulo ; /manuseio ; /faq |
| Teconlog | TECONLOG SOLUCOES LOGISTICAS LTDA | 22.027.337/0001-25 | D | SP / Vargem Grande Paulista | 5211-7/01 armazéns gerais | EPP (2015) | 7.000 m², 6.000 pallet positions; conferência; B2B/B2C; "parceiros homologados"; Correios PA in-house; D+0 | https://teconlog.com.br/ ; /quem-somos |
| DRENG | DRENG SOLUCOES E TECNOLOGIA EM LOGISTICA LTDA | 48.878.504/0001-35 | F | SP / São Paulo (Casa Verde Alta) | 5211-7/99 depósitos para terceiros | EPP (2022) | Pre-fixed price tables, progressive discounts, no long contract; conferência; B2B/B2C/D2C | https://www.dreng.com.br/ ; /sobre-a-dreng |
| G+Ship (Guarde Mais) | ROGER FULFILLMENT LTDA | 46.373.347/0001-80 | F (terms) | SP / São Paulo (Vila Guilherme) | 4930-2/02 | Demais (2022) | No minimum; simulator; transport is client's; pays by cartão/boleto/TED/PIX | https://goship.com.br/sao-paulo/sao-paulo/fulfillment-em-sao-paulo/ ; /preco/ ; /termos-e-condicoes/ |
| COTLOG | COTLOG SOLUCOES LOGISTICAS LTDA | 10.273.317/0001-55 | D | SP / Cotia | 5250-8/04 organização logística do transporte | EPP (2008) | Kit assembly; 1.840 pallet positions; own fracionado + aéreo; porta a porta; ISO 9001 | https://www.cotlog.com.br/montagem-kits ; / ; /transporte-rodoviario-fracionado |
| Paulista Express | PAULISTA EXPRESS TRANSPORTES LTDA | 74.289.034/0001-84 | D | SP / São Bernardo do Campo | 4930-2/02 | Demais (1994) | Carrier with own fleet + 100 registered vehicles; kit assembly page; coverage SP capital/interior | https://www.paulistaexpress.com.br/montagem-kits-promocionais ; /frota ; /empresa |
| Doma Logística | DOMA LOGISTICA LTDA | 27.541.681/0001-51 | D | SP / Guarulhos | 4930-2/02 | ME (2017) | Kit assembly; 10.000 m²; own fleet; branches Vitória-ES, Itajaí-SC, Belém-PA; "qualquer região do Brasil" | https://www.domalogistica.com.br/empresa-montagem-kits ; / ; /frete-fracionado |
| Contacto Logística | not printed | **UNVERIFIED** | — | SP / São Paulo (Vila Mariana, site) | — | — | "Poucas unidades ou grandes quantidades"; fulfillment, armazenagem, pick & pack | https://contactologistica.com.br/conteudo/montagem_de_kits ; / |
| Tempos | TEMPOS DE BRASIL TERCEIRIZACAO DE MONTAGEM DE PRODUTOS E SERVICOS LTDA | 01.211.578/0001-50 | D | SP / Santana de Parnaíba | 8292-0/00 | EPP (1996) | Industrial co-packer, 2.000 m², ISO 9001:2015; no shipping statement | https://www.tempos.com.br/co-packer ; /contato |
| Grupo SRM | SRM - TERCEIRIZACAO DE SERVICOS E RECURSOS HUMANOS LTDA | 02.798.885/0001-41 | F | SP / Barueri | 7820-5/00 locação de mão de obra temporária | Demais (1998) | Labour for kit assembly billed "por peça montada"; not a warehouse | https://www.gruposrm.com.br/montagem-e-manuserio-de-kits-promocionais |
| Nascra Brindes | NASCRA SOLUCOES EM PERSONALIZACAO LTDA | 27.332.194/0001-89 | D | SP / São Paulo — **situação SUSPENSA** | 7319-0/03 marketing direto | ME (2017) | R$ 50–200/unit for *gift kits incl. goods*, 100–500 pcs | https://www.nascra.com.br/site/kits-promocionais-preco |
| Javai Logística | JAVAI FULFILLMENT LTDA | 16.758.935/0001-71 | D | SP / Guarulhos | 5320-2/02 entrega rápida | ME (2012) | E-commerce fulfilment; no kit or carrier statement | https://dimi-javailogistica.com.br/fulfillment-para-pequenas-empresas-sao-paulo |
| LJ Indústria | not printed | **UNVERIFIED** | — | SP / Barueri (site: Castelo Branco km 30,5) | — | — | Industrial co-packer since 1996; montagem de kits | https://www.lj.com.br/ |
| FM Logistic Brasil | not printed | **UNVERIFIED** | — | (multinational) | — | — | Enterprise co-packing/co-manufacturing; no SME offer | https://www.fmlogistic.com.br/solucoes/co-packing/ |
| Saberpack | not printed | **UNVERIFIED** | — | SP / São Paulo (Butantã) + Piracicaba | — | — | Food/chemical envase co-packer — wrong category | https://www.saberpack.com.br/envase-co-packer |
| Cartlog | not printed | **UNVERIFIED** | — | **PR / Londrina** (site address) — non-SP | — | — | Kit assembly + fulfilment; SP listed without address | https://www.cartlog.com.br/fulfillment-preco |
| Guarde Mais (self-storage arm) | GUARDE MAIS PAULISTANA SELF STORAGE LTDA | 39.910.722/0001-19 | D | SP / São Paulo (same address as Roger Fulfillment) | 5211-7/02 guarda-móveis | Demais (2020) | Self-storage; fulfilment is via G+Ship above | https://guardemais.com.br/ |
| Loggi | LOGGI TECNOLOGIA LTDA / L4B LOGISTICA LTDA | 18.277.493/0001-77 / 24.217.653/0001-95 | F (T&C) | SP / São Paulo | — | — | Pre-paid without contract; post-paid by proposal; per package | https://www.loggi.com/enviar-pacotes/para-voce/termos-e-condicoes/ |
| Mercado Livre | MERCADO LIVRE BRASIL LTDA | 03.007.331/0001-41 | F | SP / Osasco | — | — | Full = platform orders only | https://www.mercadolivre.com.br/ajuda/Full_5227 (footer) |

Benchmark blog sources (not providers): Wistor https://wistor.com.br/blog/qual-e-o-custo-do-fulfillment/ ;
Stokki https://www.stokki.com.br/blog/quanto-custa-terceirizar-o-fulfillment-para-seu-e-commerce
(CNPJ 35.149.864/0001-54 in footer, not resolved) ; Já Enviou https://jaenviou.com.br/blog/fulfillment-para-ecommerce ;
Loghouse https://loghouse.com.br/quanto-custa-fulfillment/ (CNPJ 36.032.658/0001-22 in footer, no R$ in body).

---

## Ready-to-send quote questions (one message, same to each shortlisted provider)

1. Preço por kit montado para lotes de 100, 500 e 5.000 kits, BOM de 17–20 itens
   (roupas, toalhas, banheira plástica 20 L, higiene, bolsa), embalagem final = bolsa
   do próprio kit dentro de caixa de papelão. Há adicional por item volumoso (banheira)?
2. Cobram por kit, por hora ou por peça? Há taxa de setup/projeto, mínimo de
   faturamento ou mensalidade?
3. Recebem entregas de 3–6 fornecedores distintos (Brás/Pari) para o mesmo projeto?
   Conferem contra as NF-e? Como reportam faltas/avarias e em quanto tempo?
4. Quantos dias de armazenagem sem custo entre o primeiro recebimento e a expedição?
   Preço por posição-palete/dia além disso?
5. Prazo de montagem em dias úteis, contado do recebimento do último item, para 100 /
   500 / 5.000 kits.
6. Expedição: emitem CT-e em nome de vocês (frete no contrato de vocês) ou reservam
   no meu CNPJ? Quais transportadoras? Cotação de um lote paletizado SP → Recife,
   Fortaleza, Salvador, Belém e um município do interior do NE, para 100 e 500 kits.
   Ad valorem / GRIS sobre kit de ~R$ 176?
7. Entrega em órgão público: aceitam entrega agendada com conferência do recebedor,
   canhoto assinado e comprovante para o processo de pagamento?
8. Condições de pagamento: sinal na aprovação? boleto 14/28 dias? faturamento
   separado montagem (NFS-e) e frete (CT-e)?
9. Seguro da mercadoria em armazém e em trânsito — quem cobre, até que valor?
10. Cadastro: exigem tempo mínimo de CNPJ, faturamento mínimo ou referências?
