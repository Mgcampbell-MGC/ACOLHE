# Editais — kit natalidade / kit enxoval / kit maternidade

Retrieval run: **2026-09-19, 16:19–16:35 UTC**. Everything here was fetched from the live source in
that window. Nothing in this directory is reconstructed from memory, from a news article, or from a
summary. Where a document could not be retrieved, the field says `NAO_OBTIDO` and the failure is
recorded below with its HTTP status code.

---

## 1. PRIMARY TARGET — Itaquaquecetuba/SP 2025/447 — **SPEC NOT OBTAINED**

**The verbatim 17-item list was NOT retrieved. Do not price against anything in this directory for
this tender.** No item list has been invented, inferred, or paraphrased.
`itaquaquecetuba_2025_447.json` carries `"itens": null` deliberately.

### What WAS verified at source

`GET https://pncp.gov.br/api/consulta/v1/orgaos/46316600000164/compras/2025/447` → **HTTP 200**
(saved as `itaqua_familyA_compra.json`). Verbatim fields:

| field | value |
|---|---|
| `objetoCompra` | `AQUISICAO DE KIT MATERNIDADE ` (trailing space is in the source) |
| `orgaoEntidade.razaoSocial` | `MUNICIPIO DE ITAQUAQUECETUBA` |
| `numeroControlePNCP` | `46316600000164-1-000447/2025` |
| `numeroCompra` / `processo` | `90088` / `E90088` |
| `valorTotalEstimado` | `2380250.00` |
| `valorTotalHomologado` | `1795250.00` |
| `modalidadeNome` | `Pregão - Eletrônico` |
| `srp` | `true` |
| `tipoInstrumentoConvocatorioNome` | `Edital` |
| `amparoLegal.nome` | `Lei 14.133/2021, Art. 28, I` |
| `dataPublicacaoPncp` | `2025-11-19T16:25:16` |
| `dataAberturaProposta` | `2026-03-17T09:00:00` |
| `dataEncerramentoProposta` | `2026-03-17T09:15:00` |
| `situacaoCompraNome` | `Divulgada no PNCP` |
| `existeResultado` | `true` |
| `usuarioNome` | `CONAM Consultoria em Administração Municipal` |
| `justificativaPresencial` | `CONFORME JUSTIFICATIVA INTERNA!` |

2.380.250,00 ÷ 5.000 = **476,05** and 1.795.250,00 ÷ 5.000 = **359,05** — both per-kit figures the
caller gave reproduce exactly **if** the quantity is 5.000. Family A does not expose quantities, so
5.000 is consistent-but-unverified, not confirmed.

Family A exposes **no item, file, or result sub-resource**. Confirmed against the live OpenAPI
document (`GET /api/consulta/v3/api-docs` → 200). The complete path list is:

```
/v1/atas                      /v1/contratos
/v1/atas/atualizacao          /v1/contratos/atualizacao
/v1/contratacoes/atualizacao  /v1/instrumentoscobranca/inclusao
/v1/contratacoes/proposta     /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}
/v1/contratacoes/publicacao   /v1/pca/  /v1/pca/atualizacao  /v1/pca/usuario
```

There is no `…/{sequencial}/itens`. Item detail exists **only** in Family B.

### Every attempt, with status code

| # | URL | Code |
|---|---|---|
| 1 | `api/pncp/v1/orgaos/46316600000164/compras/2025/447/itens?pagina=1&tamanhoPagina=50` | **503** |
| 2 | `api/pncp/v1/orgaos/46316600000164/compras/2025/447/arquivos` | **503** |
| 3 | `api/pncp/v1/orgaos/46316600000164/compras/2025/447` | **503** |
| 4 | `pncp-api/v1/orgaos/46316600000164/compras/2025/447/itens` (alt gateway prefix) | **503** |
| 5 | `pncp-api/v1/orgaos/46316600000164/compras/2025/447/arquivos/1` (canonical edital PDF) | **503** |
| 6 | `api/pncp/v1/usuarios` (unrelated Family B route) | **503** |
| 7 | `api/pncp/v3/api-docs` (Family B's own swagger) | **503** |
| 8 | `api/search/?q=kit maternidade&tipos_documento=edital` | **503** |
| 9 | `api/search/?q=itaquaquecetuba kit maternidade` | **503** |
| 10 | `treina.pncp.gov.br/api/pncp/v1/…/447/itens` | 404 (training env is UP but holds different data) |
| 11–25 | background backoff loop, 12 cycles × 2 endpoints, 15s→300s, 16:19–16:35 UTC | **9× 503, 3× 000** (see `familyB_retry_log.txt`) |
| 26 | `pncp.gov.br/app/editais/46316600000164/2025/447` (portal HTML) | 200 — Angular shell only; its data comes from Family B, so it renders empty |
| 27 | `alertalicitacao.com.br/!licitacao/PNCP-46316600000164-1-000447-2025` | 200 — summary only, **no item list**; points back to the 503 PDF |
| 28 | `www.itaquaquecetuba.sp.gov.br/compras/licitacoes-vigentes/` | **403** Cloudflare `Just a moment…` |
| 29 | `www.itaquaquecetuba.sp.gov.br/compras/` | **403** Cloudflare |
| 30 | `www.itaquaquecetuba.sp.gov.br/compras/licitacoes-concluidas/` | **403** Cloudflare |
| 31 | `www.itaquaquecetuba.sp.gov.br/sistema/?pg=compras-e-licitacoes-concluidas` | **403** Cloudflare |
| 32 | `www.itaquaquecetuba.sp.gov.br/sistema/arquivos/compras/edital/1094/…pdf` (known-good PDF path, control test) | **403** Cloudflare |
| 33 | `itaqua.sp.gov.br/compras/licitacoes-vigentes/` (alt host) | **403** Cloudflare |
| 34 | `itaqua.sp.gov.br/sistema/arquivos/compras/edital/1094/…pdf` | **403** Cloudflare |
| 35 | `itaquaquecetuba.sp.gov.br/compras/licitacoes-concluidas/` (no-www) | **403** Cloudflare |
| 36 | `www.diariooficial.itaquaquecetuba.sp.gov.br/index.php/prefeitura/compras` | **000** — `CONNECT tunnel failed, 502` at the egress gateway |
| 37 | `r.jina.ai/https://www.itaquaquecetuba.sp.gov.br/compras/licitacoes-vigentes/` (reader proxy) | **403** — proxy relayed the same Cloudflare challenge |
| 38 | `archive.org/wayback/available?url=pncp.gov.br/app/editais/46316600000164/2025/447` | 200, `archived_snapshots: {}` — **never archived** |
| 39 | Wayback CDX `itaquaquecetuba.sp.gov.br/sistema/arquivos/compras/edital/*` | 200, **0 rows** |
| 40 | Wayback CDX `pncp.gov.br/pncp-api/v1/orgaos/46316600000164/compras/2025/447*` | 200, **0 rows** (1 prior attempt died `curl (35) Recv failure`, retried) |
| 41 | Wayback CDX `pncp.gov.br/app/editais/46316600000164/2025/447*` | 200, **0 rows** |
| 42 | `bllcompras.com/Process/ProcessSearchPublic` (Itaquaquecetuba runs on BLL) | 200 but a 1.7 KB JS shell; public search needs a real browser session |

Four independent web searches for the edital text (`pregão 90088/2025`, `kit maternidade
Itaquaquecetuba`, `CONDAFE`, `BLL 90088`) returned no copy of the document. The only hits were the
municipality's own Cloudflare-blocked pages, unrelated 90088/2025 tenders in other municipalities
(Piranga/MG, São Luís/MA, UFG), and news coverage of the "Mãe Itaquá" programme. **That news
coverage lists kit contents in prose; it is NOT the spec and was deliberately not used.**

### Why the 503 is not fixable from here

The body is HAProxy's `No server is available to handle this request.` — the backend pool for that
service is empty. It is returned identically for Family B's own swagger and for unrelated Family B
routes, so it is a service-wide outage, not a route, header, auth, or rate-limit problem. No
User-Agent, HTTP version, or header permutation changes it. TLS verification was never disabled and
`HTTPS_PROXY` was never unset.

### To get the spec when PNCP recovers

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
curl -sS -A "$UA" "https://pncp.gov.br/api/pncp/v1/orgaos/46316600000164/compras/2025/447/itens?pagina=1&tamanhoPagina=50"
curl -sS -A "$UA" -o itaqua_edital.pdf "https://pncp.gov.br/pncp-api/v1/orgaos/46316600000164/compras/2025/447/arquivos/1"
```

---

## 2. PNCP API status as observed (2026-09-19 16:31 UTC)

| family | base | status |
|---|---|---|
| **A — Consulta** | `pncp.gov.br/api/consulta/v1` | **UP (200)** — but see the caveat below |
| **B — PNCP** | `pncp.gov.br/api/pncp/v1` and `pncp.gov.br/pncp-api/v1` | **DOWN — 503 on 15/15 attempts** |
| **Search** | `pncp.gov.br/api/search` | **DOWN — 503** (the caller did not know about this one) |

Caveat on Family A: healthy for the single-tender lookup and for most date queries, but
`/v1/contratacoes/publicacao?dataInicial=20260918&dataFinal=20260918&codigoModalidadeContratacao=6`
returned **HTTP 500** while `…20260901…` returned 200. Family A is up but not uniformly reliable.

---

## 3. SECONDARY TARGETS — seven editais retrieved (HTTP 200, PDFs in this directory)

Clause-by-clause classification is in `clauses.csv` (one row per edital, verbatim quotes in the
`*_verbatim` columns). Full extracted text of every PDF sits next to it as `<name>.txt`.

| # | edital | source | atestado |
|---|---|---|---|
| 1 | Agrolândia/SC — PE 01/2026/FMS | `agrolandia.sc.gov.br` | **ABSENT** |
| 2 | Bocaiúva do Sul/PR — PE 40/2025 | `bocaiuvadosul.pr.gov.br` | QUALITATIVE |
| 3 | Bom Sucesso do Sul/PR — PE 34/2026 | `bomsucessodosul.pr.gov.br` | QUALITATIVE |
| 4 | Coronel Xavier Chaves/MG — PE 37/2026 (PL 72/2026, retificado) | `coronelxavierchaves.mg.gov.br` | QUALITATIVE |
| 5 | Irecê/BA — PE SRP 003/2026 (FMAS) | `procede.api.br` (DOM ed. 2777) | QUALITATIVE |
| 6 | São João do Paraíso/MA — Kit Enxoval de Bebê | `saojoaodoparaiso.ma.gov.br` | QUALITATIVE |
| 7 | Belterra/PA — 26-017 (Termo de Referência) | `belterra.pa.gov.br` | QUALITATIVE |

**Not one of the seven imposes a quantitative atestado.** No percentage, no minimum quantity, no
minimum contract value anywhere. Agrolândia has no qualificação técnica section at all — the word
"atestado" does not occur once in its 41 pages.

Two near-misses worth reading carefully rather than trusting the label: Irecê says "no mínimo, 1
(um) atestado", and the word "quantidades" appears only in its rule *permitting* the summing of
several atestados — that widens eligibility, it does not impose a floor. São João do Paraíso uses
the stock phrase "pertinentes e compatíveis, em características, quantidades e prazos", which names
quantities without fixing any, and its PDF is a poor scan.

### Delivery deadlines

Bom Sucesso do Sul **5 dias úteis** · Irecê **5 dias** · Agrolândia **10 dias** · São João do
Paraíso **10 dias** · Bocaiúva do Sul **15 dias úteis** · Coronel Xavier Chaves **20 dias corridos**
· Belterra **imediato** (plus replacement of non-conforming goods within 24 h).

### Judging method

Six of seven are **MENOR PREÇO POR ITEM**. **Irecê is MENOR PREÇO GLOBAL** — effectively lote único,
so the whole basket must be quoted. The exact string "LOTE ÚNICO" appears in none of them.

### "CONFORME MODELO DO ÓRGÃO"

**Does not appear in any of the seven.** The only near-match is Coronel Xavier Chaves 5.1, "proposta
formal conforme modelo contido no ANEXO II do Edital" — a reference to the edital's own proposal
form, not to a physical model supplied by the órgão.

### "PAGAMENTO ANTECIPADO"

Six of seven are silent. **Bom Sucesso do Sul forbids it in terms**: 22.1, "não sendo, em nenhuma
hipótese, permitida a antecipação de pagamentos e o pagamento de fornecimentos não executados ou
executados de forma incompleta".

### Payment deadlines and the two-number pattern

The expected "N + M dias úteis under a Decreto Municipal" shape is largely **absent**. Five of seven
give one flat number — 30 days. Only two split it, and neither matches the expected form:

- **Bom Sucesso do Sul** gives **three** numbers, keyed to supplier size, not a liquidação/pagamento
  split: 10 dias corridos (MEI) / 20 (ME or EPP) / 30 (everyone else), under **Decreto Municipal nº
  3.283 de 28/09/2025** (preamble). A bidder that is neither MEI nor ME/EPP is paid in 30.
- **Bocaiúva do Sul** gives 30 days from presentation of the nota fiscal (13.1) plus a separate
  **5 dias úteis** for checking and approving it (8.5) — so effectively 5 + 30, with no Decreto cited.
- **São João do Paraíso** fixes only the first number: the NF must be filed by the **5th business
  day** of the following month (16.1); no payment day-count is stated anywhere.

Decreto Municipal citations exist but mostly govern SRP or regional preference, not payment: Irecê
nº 207/2024 (SRP), Bom Sucesso do Sul nº 3.009/2021-2022 (margem de preferência), Agrolândia nº
045/2023, 101/2024, 048/2025 and nº 097/2023 (the last only for income-tax withholding).

---

## 4. Contradictions with the brief

1. **The outage is wider than "Family B".** `pncp.gov.br/api/search` is also 503. Any recovery check
   should cover both.
2. **Family A is not uniformly healthy** — a 500 on one `contratacoes/publicacao` date query.
3. **The session date moved.** `alertalicitacao` records the opening as **11/12/2025 09:15**, while
   Family A now returns `dataAberturaProposta 2026-03-17T09:00` with `dataAtualizacao
   2026-02-26T14:04:50`. The tender was postponed by roughly three months.
4. **"Homologated" is not what PNCP says.** `situacaoCompraNome` is still `Divulgada no PNCP`; the
   award shows only as `existeResultado: true` plus a non-zero `valorTotalHomologado`. Neither the
   CONDAFE award nor the 5.000-unit quantity could be confirmed at source — Family A carries no
   supplier name and no quantities, and the result endpoints are in the 503 family.
5. **The R$476,05 / R$359,05 per-kit figures check out**, but only on the assumption of 5.000 units.
6. **The atestado worry may be misplaced for this product class.** Seven of seven are qualitative or
   absent — one prior sale of any size, public or private, satisfies every one of them.
7. **The bigger bid-blocker here is not the atestado, it is samples and global pricing.** Bom Sucesso
   do Sul required physical samples (a `Parecer_amostras` document is published alongside its
   edital), and Irecê judges on price global.

---

## 5. Files

| file | what it is |
|---|---|
| `README.md` | this document |
| `itaquaquecetuba_2025_447.json` | verified Family A metadata; `"itens": null` — spec NOT obtained |
| `itaqua_familyA_compra.json` | raw Family A response, unmodified |
| `familyB_retry_log.txt` | timestamped log of the backoff loop, every status code |
| `clauses.csv` | one row per edital, 20 columns, verbatim clause quotes |
| `agrolandia_sc_pe01_2026.pdf` / `.txt` | 41 pp |
| `bocaiuvadosul_pr_pe40_2025.pdf` / `.txt` | 48 pp |
| `bomsucessodosul_pr_pe34_2026_EDITAL.pdf` / `.txt` | 45 pp |
| `bomsucessodosul_pr_pe34_2026_TR.pdf` / `.txt` | 8 pp, termo de referência |
| `coronelxavierchaves_mg_pl72_2026_EDITAL_RETIFICADO.pdf` / `.txt` | 70 pp |
| `irece_ba_dom2777.pdf` / `.txt` | 113 pp, DOM ed. 2777 containing PE SRP 003/2026 |
| `saojoaodoparaiso_ma_23388.pdf` / `.txt` | 263 pp, degraded scan |
| `belterra_pa_26-017.pdf` / `.txt` | 7 pp, TR with the full item list |
| `saopedrodoiguacu_pr_TR_kit.pdf` / `.txt` | 6 pp — **Pregão Presencial under Lei 10.520/2002 + Decreto Municipal 105/2015**, i.e. pre-14.133. Kept for the item wording only; NOT classified in `clauses.csv` and not counted among the seven |
| `crato_ce_dom5941.pdf` / `.txt` | 22 pp — **aviso/extrato only**, no clauses. Records a kit natalidade award to ATENA COMÉRCIO, valor global R$ 46.800,00. Not classified |
| `pncp_familyA_scan_kit.json` | Family A sweep, see below |

### About `pncp_familyA_scan_kit.json`

A nationwide sweep of Family A `contratacoes/publicacao` (modalidades 6 and 8, 2026-03-01 →
2026-09-19) filtering `objetoCompra` for NATALIDAD/ENXOVAL/MATERNIDADE/BEBÊ, run to build a
source-verified census of comparable tenders. **It did not finish inside this session and the file
may be absent or partial.** It was never used to source any figure above; every edital in
`clauses.csv` was found and fetched independently. Re-run it with
`scan.py` if the census is wanted — note Family A intermittently 500s on single-date queries, so it
needs the retry logic it already has.

---

## 6. What this failure blocks downstream

`data/cost_table.csv` in this repo is being priced against a 17-line Itaquaquecetuba BOM whose
source is a handoff, not the edital. Three of its rows state their own dependency on the very text
that could not be retrieved today:

- **`kit_enxoval`** — `spec_risk: BLOCKING`, cost empty: *"UNPRICED AND UNSPECIFIED. A kit inside a
  kit. … Cannot price until the real Itaquaquecetuba item text is read."*
- **`banheira_lisa`** — `spec_risk: CAPACITY_BAND`: *"COST IS BAND-SENSITIVE: 'min 20L' = R$18,90;
  '>=22L' = R$23,65; 'exactly 24L' = R$29,71. Re-price once the real edital wording is known."*
  A single word in the item text moves this line by **57%**.
- **`body_manga_longa`** — `spec_risk: SIZE_GRADED`: *"many 3-packs are labelled TAMANHO RN AO G
  which may be size-graduated … If the edital demands a single size this price does not hold.
  MUST VERIFY before banking."*

So the unavailable spec is not a documentation gap — it is load-bearing for at least one unpriced
line and two priced lines that can move materially. **Until
`api/pncp/v1/…/2025/447/itens` or `pncp-api/v1/…/2025/447/arquivos/1` returns 200, the per-kit BOM
total should be treated as provisional**, and no bid should be submitted against it.

---

## 7. Daily-loop cost: the handoff's ~5.560 calls/day is wrong by ~60x

Measured 2026-09-19 against Family A for 2026-09-15:

| modalidade | tenders |
|---|---|
| 6 Pregão Eletrônico | 1.719 |
| 7 Pregão Presencial | 50 |
| 8 Dispensa | 2.826 |
| **total** | **4.595** |

At `tamanhoPagina=50` that is **~93 listing calls for a full national day**, not
5.560. The remaining ~5.400 in the original estimate were Family B per-tender
`/itens` calls — and those cannot be made at all while Family B is 503.

`tamanhoPagina` on PNCP is bounded **10..50** (below 10 and above 50 both 400).

### The real constraint is a rate limit nobody had measured

**~30 requests in a burst returns HTTP 429 "Limite de Requisições Excedido",
clearing in ~30s, with NO `Retry-After` header.** It is keyed on source IP and
shared across both API families, so anything else egressing the same host
spends the same budget. A full national-day attempt collected 62 of them.

So the daily loop is governed by the 429 budget, not by bandwidth, and 93
calls is comfortably inside it. The per-tender descent is what would not be.

### A fallback that silently loses rows, found live and fixed

In one run `publicacao` page 4 took five 429s, the client fell back to
`atualizacao`, and that page returned **16 tenders already seen**. The two
routes are differently ordered, so "page 4" is a different set: 16 real
tenders were never fetched while the row count still read 200/200.

The client now records the route per page, flags `ROUTE_MIXED`, refuses to
call such a harvest complete, and reports `distinct` separately from `served`.
Counting repeats as coverage is precisely how a short harvest passes for a
full one.
