# Research brief — Brazilian municipalities that buy newborn layette kits

**Hand this whole file to a research assistant that can open and render real web pages
(JavaScript, PDFs, portals behind interstitials).** It is self-contained: you need no other
context. Everything below was established by an HTTP-only agent that could not render
JavaScript, and the gaps it left are exactly what a browser can close.

---

## 1. What this is for

A one-person business in São Paulo is preparing to sell **kits natalidade / kits enxoval de
bebê** (newborn layette kits) to Brazilian municipalities through public procurement. Before
registering anything, the founder wants to *talk to the people who actually run these
programmes* — to understand how they work, what goes wrong, and what buyers wish suppliers
did differently.

**You are finding published contact details and published facts. You are not contacting
anyone and you are not helping anyone sell.** The founder will decide who to speak to.

---

## 2. Hard rules — do not break these

1. **CONTACT NOBODY.** No email, no contact form, no WhatsApp, no phone call, no
   registration, no account creation, no "request a quote". Read published pages only.
2. **Never state a fact you did not read.** If a page would not load, write
   `NÃO VERIFICADO` and say which URL failed and how. An invented-but-plausible email is
   far worse than a blank.
3. **Never guess a contact from a pattern.** Do not assume `licitacao@<cidade>.<uf>.gov.br`
   exists because it exists elsewhere. Only record what a page actually prints.
4. **Watch for template placeholder data.** At least one of these municipalities publishes
   an unconfigured website template containing `contato@prefeitura.gov.br`,
   `(00) 0000-0000` and `Rua Principal, 123`. That is not a contact — it is a CMS default.
   If a value looks like a placeholder, say so and discard it.
5. **Prefer institutional contacts** (setor de licitações, secretaria, ouvidoria) over
   individuals. You may record a public official's name and *official* phone/email when the
   municipality itself publishes them in that capacity — for example a pregoeiro named in an
   edital. Never record a personal mobile or private address.
6. **Cite a URL for every single data point**, plus the date you read it.
7. If you cannot verify something, that is a *result*, not a failure. Report it plainly.

---

## 3. Useful background this research already established

- The buying body is usually the **Secretaria Municipal de Assistência Social**, and the kits
  are handed over through a **CRAS** (Centro de Referência de Assistência Social).
- The money is often held by a **Fundo Municipal de Assistência Social (FMAS)** rather than
  the prefeitura, which means **the buyer's CNPJ is not the prefeitura's CNPJ**.
- The legal basis is usually a **benefício eventual** of the SUAS system, created by a
  **resolução do CMAS** (the municipal social-assistance council) — *not* a named municipal
  programme with a brand. Searching for "programa" often finds nothing; searching for
  `"benefício eventual" natalidade <município>` or `resolução CMAS <município>` works better.
- Two **state** programmes sit above these municipal purchases and are worth understanding:
  **Maranhão Acolhe** (launched Dec 2025; a 45-item kit including a personalised bag) and
  **Nascer Bem** in Paraná. Municipal buys appear to complement state delivery.
- Purchases split between **pregão eletrônico** (larger) and **dispensa eletrônica**
  (smaller, ≤ R$65.492,11 in 2026 under Lei 14.133 art. 75 II, often a 3-day window).

**Every tender record is public** at
`https://pncp.gov.br/api/consulta/v1/orgaos/{CNPJ}/compras/{ano}/{sequencial}` — this returns
JSON and works reliably. The *files* endpoint (`https://pncp.gov.br/api/pncp/v1/orgaos/{CNPJ}/compras/{ano}/{seq}/arquivos`)
was returning **HTTP 503 on every attempt** and is the single reason most editais could not
be read. **Try it again** — if it is back up, the edital PDFs it serves answer many questions
below at once.

---

## 4. GROUP A — five municipalities, deep gaps

These published a kit tender on 15 September 2026. What is already verified is listed so you
do not repeat it.

### A1. Maracás — BA — pop. 27.620 — CNPJ 13.910.203/0001-67 — compra 2026/131
Dispensa, R$60.910. Object names gestantes em vulnerabilidade (sede **and** zona rural), the
CRAS, the Secretaria de Desenvolvimento Social, and *Benefício Eventual–Natalidade*.
- ✅ Already have: `licitacoesmaracas@gmail.com`, `(73) 3533-2121`, Equipe de Pregão
  `(73) 99823-6264`, Praça Ruy Barbosa 705, pregoeiro named in the edital.
- ❓ **Need:** direct email and phone for the **Secretaria Municipal de Desenvolvimento
  Social** (the unidade solicitante). `transparencia.maracas.ba.gov.br/contato` and
  `/estrutura-organizacional` are JavaScript-only — a browser should render them.
- ❓ Which **resolução do CMAS** creates the benefício eventual natalidade here, and what it
  says about quantity and eligibility.

### A2. Vitória — ES — pop. 322.869 — CNPJ 27.142.058/0001-26 — compra 2026/590
Pregão, **R$944.586** — by far the largest. Bought by the prefeitura, not a fundo.
- ✅ Already have: SEMAS `(27) 3382-6172`; pregão `(27) 3382-6074` / `3382-6037`; CPL
  `(27) 3382-6253`; Secretária Carla Mognato Scardua Shalders; Subsecretária de Proteção
  Social Básica Graziella Almeida Lorentz.
- ❓ **Need: a working SEMAS email.** The emails on the SEMAS page are **obfuscated against
  scraping** (they render as scrambled text to a plain fetch). A browser should read them.
- ❓ **The big one:** Vitória's *Benefício por Natalidade* is paid **in cash**, single
  instalment, under **Resolução 016/2017 do COMASV**. So the R$944k **Kit Bebê** is a
  *different* programme and **no authorising instrument for it could be found.** Find what
  created it — a lei municipal, a decreto, a COMASV resolution, a programme page, anything.
- ❓ The pregoeiro for this tender (the edital could not be downloaded).
- 💡 Lead worth following: `portaldecompras.vitoria.es.gov.br` has a working public JSON
  search (`POST /search.json`, needs a session cookie and `_token` from the homepage) whose
  records carry a `comissao` object with sigla, address and email. Its data appears to stop
  at 2023 but the commission directory is still useful.
  `transparencia.vitoria.es.gov.br/Licitacao.Lista.aspx?exercicio=2026` responds but loads
  its list by JavaScript postback.

### A3. Alvorada de Minas — MG — pop. 4.159 — CNPJ 18.303.164/0001-53 — compra 2026/75
Pregão, R$41.665, "aquisição de **ENXOVAIS** destinados às unidades de saúde e casa de apoio".
- ✅ Already have: `licitacao@alvoradademinas.mg.gov.br`, `alvoradademinas@gmail.com`,
  `(31) 3520-0000` / `3520-0001`, `saude@alvoradademinas.mg.gov.br`,
  `gabinete@alvoradademinas.mg.gov.br`, Assistência Social `(31) 3862-1209`.
- ❓ **The decisive question: is this a baby layette at all?** It is bought by the
  **Secretaria de Saúde** and destined for health units and a "casa de apoio" — so "enxoval"
  here may mean **hospital bed linen** (sheets, towels, pillowcases), not newborn clothing.
  It is the only one of the five not routed through assistência social. **Read the edital or
  the item list and settle it.** `alvoradademinas.mg.gov.br/licitacoes` returns a Laravel
  error page in production; the sub-route `/licitacoes/pregao-eletronico` works and serves
  the PDFs. `app2.licitardigital.com.br/pesquisa/112815` (its linkSistemaOrigem) returned 403.

### A4. Junco do Maranhão — MA — pop. 5.146 — CNPJ 01.612.334/0001-89 — compra 2026/28
Dispensa, R$11.621 — the smallest. Bought through the **FMAS**.
- ✅ Already have (only this): `gabinete@juncodomaranhao.ma.gov.br`, `(98) 3271-1017`,
  Rua Walmir Araujo — from the transparency portal.
- ⚠️ **TRAP:** the municipality's institutional site publishes **template placeholder data**
  — `contato@prefeitura.gov.br`, `(00) 0000-0000`, `Rua Principal, 123`. Do not record any
  of it.
- ❓ **Need:** any real contact for the **setor de licitações** and for the **Secretaria
  Municipal de Assistência Social**. Try the Diário Oficial dos Municípios do Maranhão
  (`diariooficial.famem.org.br`, which returned 503) and the FMAS's own publications.
- ❓ Whether the kit here is tied to **Maranhão Acolhe** (the state's 45-item kit).

### A5. Rio Branco do Sul — PR — pop. 37.558 — CNPJ 76.105.576/0001-85 — compra 2026/163
**Dispensa eletrônica "PDE 31"**, R$16.520, processo 143/2026, *"entrega parcelada durante o
período de 12 meses"* — recurring supply in the form of a dispensa. Bought through the FMAS.
Its proposal window closed 18/09/2026.
- ✅ Already have (only this): `ouvidoria@riobrancodosul.pr.gov.br`, `(41) 98743-2024`,
  Rua Horacy Santos 222 — from the diário oficial footer.
- ❓ **Need:** licitações and CRAS/Assistência Social contacts. The whole portal
  (`riobrancodosul.atende.net`, IPM Sistemas — `riobrancodosul.pr.gov.br` redirects there) is
  **JavaScript-only**: `/telefones/`, `/licitacao/`, `/cidadao/pagina/licitacoes`,
  `/cidadao/pagina/servicos-do-cras`, `/subportal/cras` all return HTTP 200 with nothing but
  a `<title>`. **A browser will render these. This is the single highest-value target in this
  brief** — it is a portal full of contacts that is simply invisible without JavaScript.
- ❓ **Did this dispensa get a winner, and at what price?** As of 19/09 the PNCP record showed
  `valorTotalHomologado: null`. A real clearing price for a ~46-kit lot is extremely valuable.
  Check the PNCP record, the municipal portal and the diário oficial.
- ❓ Whether it relates to Paraná's **Nascer Bem** programme.

---

## 5. GROUP B — eight municipalities already contactable, one gap each

For these, contacts were extracted from their own published editais. What is mostly missing
is the **social-services side** — the people who run the programme rather than the tender.

| Município | UF | Have | Need |
|---|---|---|---|
| Coronel Xavier Chaves | MG | `licitacao@coronelxavierchaves.mg.gov.br`, (32) 3216-1053 r.109/110, WhatsApp (32) 99199-6496 | Secretaria de Assistência Social / CRAS direct contact |
| São Pedro do Iguaçu | PR | `acaosocial-spi@yahoo.com.br`, (45) 3255-8000 | Confirm that address is current; find the CRAS coordinator |
| Belterra | PA | `semtdes@belterra.pa.gov.br` | A **phone number** — none is published in the TR |
| Bocaiúva do Sul | PR | `licitacaobocaiuvadosul@gmail.com`, (41) 92003-9870 / 9850 | Assistência Social contact |
| Irecê | BA | `irecepregao@gmail.com`, (74) 3641-1733 / 3641-3116 | Assistência Social contact; the tender was up to 400 kits — find the programme behind it |
| Bom Sucesso do Sul | PR | `compras@bssul.pr.gov.br`, `licitacoes@`, `contratos@`, (46) 3199-2333 | Assistência Social contact |
| Agrolândia | SC | `pregoeiro@agrolandia.sc.gov.br`, (47) 3534-4212 | Assistência Social / Fundo Municipal de Saúde contact |
| São João do Paraíso | MA | `cplsjparaiso@gmail.com`, (99) 99105-3540 | Assistência Social contact; possible Maranhão Acolhe link |
| Itaquaquecetuba | SP | nothing — CNPJ 46.316.600/0001-64, compra 2025/447 | **Everything.** This is a 17-item "kit maternidade" tender whose item list the whole cost model is built on. Its edital PDF could never be downloaded. Get the item list and the contacts. |

---

## 6. Questions worth answering for any of them

Whatever you can establish from published sources, for any municipality:

1. How many kits per year, and is the programme continuous or annual?
2. What is in the kit — the item list, with quantities and specs?
3. Which instrument authorises it (lei, decreto, resolução do CMAS)?
4. Where does the money come from — municipal budget, emenda parlamentar, state or federal
   co-financing?
5. Has a kit tender there ever gone **deserta** (no bidders) or **fracassada** (no valid
   bid)? *This is the most commercially valuable fact in the whole brief* — it identifies a
   buyer who wants to buy and cannot find a supplier.
6. What did past kit tenders actually **clear at**, per kit?
7. Do they buy by pregão or dispensa, and how does a supplier learn about a dispensa in time?

---

## 7. Output format

Return **one table of contacts** with exactly these columns:

```
municipio, uf, cnpj_orgao, orgao_nome, setor, contato_tipo, contato_valor,
fonte_url, data_leitura, confianca, notas
```

- `contato_tipo`: one of `email`, `telefone`, `whatsapp`, `endereco`, `site`, `pessoa`
- `confianca`: `VERIFICADO` (you read it on an official page) or `NÃO VERIFICADO` (with the
  reason in `notas`)
- One row per contact detail.

Then a **short written section per municipality**: who they are, what they bought, who to
speak to and why, what you could establish about the programme, and an explicit list of what
you could not verify.

Finally, a **register of every URL that blocked you** and how (403, 503, captcha,
login wall, JavaScript-only, placeholder data).

---

## 8. What a good answer looks like

Not "here are 40 email addresses". A good answer is:

> *"Rio Branco do Sul's portal renders fine in a browser. The licitações department is
> X at telephone Y, read at URL Z on this date. The CRAS page lists three units with these
> addresses. The PDE 31 dispensa was won by [company] at R$[value] per kit — here is the
> publication. And Alvorada de Minas is hospital bed linen, not a baby layette: here is the
> item list."*

Precision and provenance beat volume. **Three verified contacts and one settled question are
worth more than forty unverified rows.**
