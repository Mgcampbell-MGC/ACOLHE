# Supplier Credit & Cadastro Policy — Toiletries / Descartáveis Lines

Compiled 2026-09-19. Catalogue and policy-page reading only; no supplier was contacted and no
registration was performed. Every UF below was resolved by fetching
`https://publica.cnpj.ws/cnpj/{cnpj14}` — trading name was never trusted as an address.

**Selection rule applied:** credit policy first, price second. Terms in month 2 versus month 13
is the difference between year one and year two of this business.

---

## Summary table

| Supplier | CNPJ | UF (verified) | Prices public? | Pedido mínimo | New-client payment | Path to terms |
|---|---|---|---|---|---|---|
| Brascol (ONESHOP DISTRIBUIDORA LTDA) | 18.483.322/0001-02 | **SP** — São Paulo, Brás | **No — login-gated** | R$500 atacado / R$1.500 alto atacado | PIX, cartão 6x | **Boleto parcelado** (CNAE-restricted) |
| JN Fraldas (MENSA DISTRIBUIDORA LTDA) | 10.290.457/0001-31 | **SP** — São Paulo, Canindé | **Yes** (retail tier) | none published | PIX / Visa / Master / Elo | None published |
| Tenda Atacado (TENDA ATACADO SA) | 01.157.555/0011-86 | **SP** — Guarulhos | **Yes** | none published | Boleto **à vista**, cartão | None |

All three are SP. No ICMS-differential penalty applies to any of them, so the ~6-point
LC 123 art. 13 §1 XIII "h" hurdle never had to be invoked on this basket.

---

## 1. Brascol — ONESHOP DISTRIBUIDORA LTDA
- **CNPJ** 18.483.322/0001-02 · **UF SP**, São Paulo (Brás) — verified at
  https://publica.cnpj.ws/cnpj/18483322000102
  (razão social ONESHOP DISTRIBUIDORA LTDA, fantasia BRASCOL, situação Ativa, aberta 2013-07-05)
- **Address published on site:** Rua Maria Marcolina, 748 — Brás, São Paulo/SP, CEP 03011-000
- **Source read:** https://brascol.com.br/pagina/perguntas-frequentes and
  https://brascol.com.br/puericultura/higiene-e-saude/perfumaria/c

**Who may register**
> "basta possuir um CNPJ de qualquer natureza de atividade, inclusive são aceitos CNPJ de
> Microempreendedor Individual (MEI). Desde que o CNPJ esteja ativo."

- **Minimum months in business: none stated.** Only an *active* CNPJ (and active inscrição
  estadual where applicable) is required. MEI explicitly accepted, any CNAE.
- Self-service cadastro: *"Clique em 'Minha Conta', cadastre-se e saia comprando!"*

**Minimum order**
- Atacado: **"Mínimo de R$ 500 — Peças variadas"**
- Alto Atacado: **"Mínimo de R$ 1.500 e 03 peças por referência"** — and per the FAQ,
  *"valor mínimo de compra é de R$ 1.500,00, e é exigido que sejam adquiridas no mínimo 3 peças por produto"*

**Payment / terms**
- PIX (à vista)
- Cartão de crédito em até 6x sem juros, parcela mínima R$350
- **"Boleto parcelado (apenas para cadastros com CNPJ e CNAE's específicos)"**

**Assessment — this is the credit-policy winner.** Brascol is the *only* one of the three with a
published route to deferred payment, and it imposes **no seasoning requirement** (no minimum
months trading) and accepts MEI. Terms are gated on CNAE, not on time in business, which means
they are potentially available from month 1 rather than month 13 — but the specific eligible
CNAEs are not published and must be confirmed before this is banked.

**Blocking caveat:** every price is `"Cadastre-se para ver o preço"`. Brascol's perfumaria
category (63 produtos) carries the exact BOM SKUs — *Sabonete Líquido Infantil Pimpolho Cuida
250ml*, *Hidratante Infantil Pimpolho Cuida 250ml*, *Condicionador Bebê Buba Care 250ml* — but
none could be priced without registering, which was out of scope. **Its prices are UNVERIFIED.**

---

## 2. JN Fraldas — MENSA DISTRIBUIDORA LTDA
- **CNPJ** 10.290.457/0001-31 · **UF SP**, São Paulo (Canindé, Rua Conselheiro Dantas 466) —
  verified at https://publica.cnpj.ws/cnpj/10290457000131
  (fantasia DISTRIBUIDORA J.N., situação Ativa, aberta 2008-05-09)
- **CNAE principal: "Comércio atacadista de produtos de higiene pessoal"** — the exact supplier
  class this BOM needs, and the one CONFECCOES EMILIO (a textile atacadista) is not.
- Physical stores: Pari, Brás, Anchieta. Forty years trading.
- **Sources read:** https://www.jnfraldas.com.br/atacado/ , https://www.jnfraldas.com.br/termos/ ,
  https://www.jnfraldas.com.br/politica-de-entrega/

**Who may register**
> "Qualquer negócio com CNPJ: casa de repouso, home care, clínica, hospital, farmácia, mercado e revenda."

**Cadastro speed — the strongest feature**
> "O cadastro é feito nesta página e o preço de atacado é liberado na hora, sem esperar aprovação."

> "Com o CNPJ cadastrado, é só entrar na sua conta: os preços de atacado aparecem direto na loja,
> produto por produto, com o preço de varejo riscado do lado e sem tabela em PDF."

- **Minimum months in business: none stated.** No approval queue at all.

**Minimum order**
- No minimum order value published. Free freight threshold: *"Frete grátis acima de R$500 em SP"*.

**Payment / terms**
- Footer: *"Pagamento: PIX VISA MASTER ELO"*; *"até 5% no PIX"*.
- **No boleto, no faturamento, no prazo appears anywhere** in the atacado page, Termos, or
  Política de entrega. New clients are effectively **PIX/cartão antecipado only**.
- An institutional channel exists — *"Consultor dedicado, cotação personalizada e entrega
  programada… Falar com o comercial"* — so terms may be negotiable for volume, but nothing is
  published. Treat terms as unavailable until proven otherwise.

**Pricing-tier warning:** because atacado prices only appear after CNPJ login, the prices
harvested here (unauthenticated) are the **VAREJO tier**. Cross-checking an identical SKU
confirms it — Huggies Natural Care RN 34un is R$54.06 at JN versus R$53.29 at Tenda, and
Johnson's Baby shampoo 200ml is R$21.00 at JN versus R$19.89 at Tenda. JN's published numbers
therefore sit **above** its own wholesale tier and are safe **ceilings**, not floors.

JN also publishes a **"preço por tira"** (per-diaper price) on every diaper product and defines
a fardo in its own FAQ as *"a caixa fechada com 3 ou 4 pacotes iguais"* — useful, and a direct
confirmation that the pack-count trap is real at this supplier.

---

## 3. Tenda Atacado — TENDA ATACADO SA
- **CNPJ** 01.157.555/0011-86 · **UF SP**, Guarulhos — verified at
  https://publica.cnpj.ws/cnpj/01157555001186
  (razão social TENDA ATACADO SA, filial, situação Ativa, CNAE "Comércio atacadista de
  mercadorias em geral, sem predominância de alimentos")
- CNPJ and address also self-published in the storefront API `seller` object:
  Rua Professor João Cavalheiro Salem 365, Guarulhos/SP.
- **Source read:** https://www.tendaatacado.com.br/institucional/como-pagar

**Who may buy**
- **No CNPJ requirement and no cadastro barrier** — cash-and-carry / atacarejo. Anyone can buy
  at the published price. This is the lowest-friction supplier of the three.

**Minimum order**
- None published.

**Payment / terms**
- Cartão de crédito (Visa, Mastercard, Discover, Elo, Hipercard, JCB) — à vista ou parcelado
  em produtos selecionados; Tenda Card; **Boleto bancário à vista**, *"o prazo de pagamento do
  seu pedido é de 1 dia útil"*, confirmation up to 2 business days.
- **No faturamento, no credit line, no CNPJ terms of any kind.** Boleto here is a prepayment
  instrument, not credit.

**Pricing-tier warning:** Tenda product pages state *"Informe seu CEP para visualizar o preço"* —
**prices are CEP-dependent.** The figures recorded were taken from the default (non-CEP) public
API response and must be re-confirmed for the actual delivery CEP before being banked.

---

## Recommendation

**Register with Brascol, buy interim volume from JN Fraldas.**

Brascol is the only supplier of the three offering a published path to deferred payment
(boleto parcelado), it accepts MEI with **no minimum time in business**, it sits in Brás, and its
perfumaria catalogue carries the precise BOM SKUs. Its R$500 atacado minimum is trivially met by
a layette-kit run. The single unknown — which CNAEs qualify for boleto parcelado — is the one
question worth resolving first, because it decides whether terms arrive in month 2 or never.

JN Fraldas is the right *priceable* supplier today: correct CNAE (atacadista de higiene pessoal),
SP, instant atacado unlock with no approval wait, and it alone stocked four of the five BOM lines.
Its lack of published terms is the only mark against it.

Tenda is the fallback: cheapest verified sabonete líquido and zero onboarding friction, but it
will never extend terms, so it cannot be the backbone supplier.
