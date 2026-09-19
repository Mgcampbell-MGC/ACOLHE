# SICONFI probe — verification notes for the buyer payment-risk screen

Probed 2026-09-19, 16:30–16:40 UTC, from the ACOLHE dev container via the
agent HTTPS proxy. Every figure below was measured, not assumed. Where a
claim in the handoff brief did not survive contact with the API it is marked
**CONTRADICTED**.

Host: `https://apidatalake.tesouro.gov.br/ords/siconfi/tt`
No API key, no auth, no rate limit observed. Oracle ORDS behind the scenes
(responses leak the internal host `host-5hrds-scan.prosubnet.vcndados.oraclevcn.com`
in their `links`).

---

## 1. Endpoint status and latency

| Endpoint | Status | Latency | Bytes | Verdict |
|---|---|---|---|---|
| `GET /tt/entes` | 200 | 0.34 / 0.39 / 0.54 s (n=3) | 866,510 | works |
| `GET /tt/rreo` (RREO-Anexo 07) | 200 | 0.20–0.36 s, median 0.23 s (n=5) | ~7–23 KB | works |
| `GET /tt/rgf` (RGF-Anexo 05) | 200 | 0.23 s | 661 | **200 but always empty — see §5** |
| `GET /tt/anexos-relatorios` | 504 / 200 | 62 s … 120 s timeout | 10,861 | flaky, avoid |
| `GET /tt/extrato_relatorios` | 200 | 1.0 s | 524 | 0 rows for the ente tried |
| `GET /open-api-catalog/tt/` | 200 | 1.8 s | 15,655 | useful, authoritative param list |

`entes` is 866,510 bytes — the brief's "~866 KB" is **confirmed exactly**.

**Browser User-Agent.** We always send one (`Mozilla/5.0 … Chrome/125`). Note
for honesty: a control request with *no* UA also returned 200 in 0.46 s, so I
could not reproduce a UA-based block today. Sending it stays cheap insurance
against ORDS bot rules; do not conclude from this that it is unnecessary.

**HTTP 000 is real.** The first `anexos-relatorios` call died at 90 s with
curl code 28 (`http=000`, 0 bytes). A retry succeeded in 62.8 s; a later call
returned a genuine `504` after 120 s. That is exactly the timeout/proxy case
the brief warns about — the answer is backoff, never `verify=False`. TLS
verification was never disabled at any point in this probe.

---

## 2. `/tt/entes` — the CNPJ ↔ IBGE join

```
GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes
```

`{"items":[…], "hasMore":false, "limit":6000, "offset":0, "count":5598}`

```json
{
  "cod_ibge": 4107157,
  "ente": "Diamante D'Oeste",
  "capital": "0  ",
  "regiao": "SU",
  "uf": "PR",
  "esfera": "M",
  "exercicio": 2026,
  "populacao": 4513,
  "cnpj": "77817476000144"
}
```

5,598 rows in one page (`hasMore: false`), split `M`=5570, `E`=26, `U`=1,
`D`=1. Carries both `cnpj` (unpunctuated, 14 digits) and `cod_ibge`, so the
join the screen needs is a single cached fetch. Cached to disk permanently.

The six municípios used for end-to-end validation resolved cleanly:

| Município | IBGE | CNPJ | Pop. |
|---|---|---|---|
| Nhamundá/AM | 1303007 | 04283578000153 | 21,251 |
| Coari/AM | 1301209 | 04262432000121 | 73,576 |
| Itaquaquecetuba/SP | 3523107 | 46316600000164 | 382,983 |
| Maués/AM | 1302900 | 04282869000127 | 66,336 |
| Icatu/MA | 2105104 | 05296298000142 | 25,332 |
| Paracatu/MG | 3147006 | 18278051000145 | 99,005 |

---

## 3. `/tt/rreo` — RREO Anexo 07, the payment record

```
GET /tt/rreo?an_exercicio=2026&nr_periodo=3&co_tipo_demonstrativo=RREO
           &no_anexo=RREO-Anexo%2007&co_esfera=M&id_ente={cod_ibge}
```

The URL in the brief is **correct as given**. Sample row:

```json
{
  "exercicio": 2026, "demonstrativo": "RREO", "periodo": 3,
  "periodicidade": "B",
  "instituicao": "Prefeitura Municipal de Nhamundá - AM",
  "cod_ibge": 1303007, "uf": "AM", "populacao": 21251,
  "anexo": "RREO-Anexo 07", "esfera": "M", "rotulo": "Padrão",
  "coluna": "Em 31 de dezembro de 2025 (b)",
  "cod_conta": "RestosAPagarProcessadosENaoProcessadosLiquidadosInscritosEmExercicioAnterior",
  "conta": "TOTAL (III) = (I + II)",
  "valor": 2901930.95
}
```

### Account codes we read (`conta` = `TOTAL (III) = (I + II)`)

| Col | `cod_conta` (prefix `RestosAPagarProcessadosENaoProcessadosLiquidados`) | Meaning |
|---|---|---|
| (a) | `…InscritosEmExerciciosAnteriores` | owed, from years before last |
| (b) | `…InscritosEmExercicioAnterior` | owed, from 31 Dec last year |
| (c) | `…Pagos` | actually paid |
| (d) | `…Cancelados` | written off |
| (e) | `…APagar` | still outstanding |

Identity published by SICONFI: `e = (a + b) − (c + d)`.
We use `inscritos = a + b`, matching the denominator implied by that identity.

### **CONTRADICTED** — the block is *not* "processados" only

The brief calls this "restos a pagar **PROCESSADOS**". The actual account
prefix is `RestosAPagarProcessadosENaoProcessados**Liquidados**` — processados
*plus* não-processados that have since been **liquidated**. Economically the
brief's description still holds (liquidated = delivered, attested, legally
due, unpaid), so the screen is measuring the right thing. But anyone matching
on the literal string "Processados" will pick the wrong account. There is a
genuinely separate `RestosAPagarNaoProcessados*` block in the same payload —
goods not yet delivered — which we deliberately ignore.

### **TRAP** — SICONFI omits zero-valued rows

`Pagos (c)` is **absent from the payload entirely** for an ente that paid
nothing. Observed: present for Coari, Itaquaquecetuba, Maués, Paracatu;
**absent for Nhamundá and Icatu** — precisely the two worst payers.

Read naively, a missing `Pagos` looks like missing data, and the very worst
buyers in the country would quietly drop out of the screen. So we never trust
its absence. We derive it from the published identity:

```
c = (a + b) − d − e
```

Verified to the cent against all four entes that *did* publish (c):

| Ente | published (c) | derived (a+b)−d−e | match |
|---|---|---|---|
| Coari/AM | 4,462,227.05 | 4,462,227.05 | ✅ |
| Itaquaquecetuba/SP | 109,771,258.50 | 109,771,258.50 | ✅ |
| Maués/AM | 2,593,733.16 | 2,593,733.16 | ✅ |
| Paracatu/MG | 9,225,149.81 | 9,225,149.81 | ✅ |

`evidence["pagos_source"]` records `published`, `derived`, or
`published_inconsistent` so any decision stays auditable.

### Other gotchas

- **Key on `cod_conta`, never on `coluna`.** SICONFI ships two spellings of
  the same label in one response: `"Saldo e = (a+ b) - (c + d)"` and
  `"Saldo e = (a + b) - (c + d)"`.
- **Filter `conta` to `TOTAL (III)`.** The same `cod_conta` also appears for
  `PODER EXECUTIVO`, `PODER LEGISLATIVO`, `Câmara Municipal` and the
  `(I)`/`(II)` subtotals. Summing blindly double-counts by ~2×.
- **`nr_periodo` is effectively required.** Omitting it returns
  `count: 0` with HTTP 200 — a silent empty, not an error. Paracatu with
  `?an_exercicio=2025&id_ente=3147006` → 0 rows; add `nr_periodo=6` → 56 rows.
- **Periodo 3 is the current frontier.** Paracatu 2026: p1=52, p2=36, p3=36,
  p4/p5/p6=0 rows. The brief's `nr_periodo=3` is the right default for
  September 2026. The screen falls back 3→2→1 and records which period
  answered.

---

## 4. Measured results — the six validation municípios

All from `an_exercicio=2026&nr_periodo=3`, URL pattern in §3, `id_ente` as shown.

| Município | IBGE | inscritos (a+b) | pagos (c) | cancelados (d) | saldo (e) | paid | **saldo/insc** | **canc/insc** | Outcome |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Nhamundá/AM** | 1303007 | 2,913,522.31 | **0.00** *(derived)* | 17,964.48 | 2,895,557.83 | **0.0%** | **99.4%** | 0.62% | **REJECT** |
| Icatu/MA | 2105104 | 1,091,838.69 | **0.00** *(derived)* | 0.00 | 1,091,838.69 | **0.0%** | **100.0%** | 0.00% | **REJECT** |
| Coari/AM | 1301209 | 6,963,391.36 | 4,462,227.05 | 0.00 | 2,501,164.31 | 64.1% | **35.9%** | 0.00% | **REJECT** |
| Maués/AM | 1302900 | 2,960,671.29 | 2,593,733.16 | 0.00 | 366,938.13 | 87.6% | 12.4% | 0.00% | PASS |
| Itaquaquecetuba/SP | 3523107 | 115,642,629.08 | 109,771,258.50 | 118.77 | 5,871,251.81 | 94.9% | 5.1% | 0.00% | PASS |
| Paracatu/MG | 3147006 | 9,360,896.76 | 9,225,149.81 | 0.00 | 135,746.95 | 98.5% | 1.5% | 0.00% | PASS |

**Nhamundá is genuinely rejected.** It paid R$ 0.00 of the R$ 2,913,522.31 it
had already booked as owed to suppliers — the brief's "0,0%" claim is
**confirmed**. All three rejections are pure *delay*: not one of the six
breached the 2% write-off limit (worst is Nhamundá at 0.62%).

---

## 5. **CONTRADICTED** — the RGF cash-position rail does not exist

The brief proposes a second opinion:

```
GET .../rreo?…&no_anexo=RGF-Anexo%2005&co_poder=E
```

Two separate problems.

1. **`/tt/rreo` does not accept `co_poder` at all.** Per the authoritative
   OpenAPI catalog (`/open-api-catalog/tt/`):
   - `/rreo` → `an_exercicio, co_esfera, co_tipo_demonstrativo, id_ente, no_anexo, nr_periodo`
   - `/rgf` → the same plus `co_poder` and `in_periodicidade`
   The `co_poder=E` in the brief's URL is silently ignored, and asking `/rreo`
   for an `RGF-*` anexo returns `count: 0`.

2. **`/tt/rgf` returns zero rows for everything tried.** Exhaustively:
   exercícios 2024/2025/2026 × períodos 1–3 × `in_periodicidade` Q/S/A ×
   with and without `co_poder`, `no_anexo`, `co_esfera`; and the widest
   possible query, `?an_exercicio=2025&in_periodicidade=Q&limit=5`, with no
   ente filter at all. **Every one: HTTP 200, `count: 0`.** The endpoint is
   published and responds, but appears to hold no data.

Consequence: **Disponibilidade de Caixa Líquida is not available** as a second
opinion. The screen therefore rests on RREO Anexo 07 alone. I did not fake a
cash-position signal, and the module has no dead code pretending to fetch one.
If a cash cross-check is wanted later, the candidates are `/tt/dca` (annual
balance sheet) or `/tt/msc_patrimonial` — neither probed here.

Also noted: `/tt/anexos-relatorios`, the natural way to discover valid
`no_anexo` strings, documents only `DCA` and `QDCC` (168 rows, spheres
M/E/U/C). It lists **no RREO or RGF anexos at all**, despite `RREO-Anexo 07`
working. Do not use it to validate anexo names.

---

## 6. The reference statistics — mostly **CONFIRMED**, in the right universe

The brief's figures (148 of the 200 largest kit-buying municípios) were marked
UNVERIFIED. I could not rebuild that exact universe — the kit-buyer list lives
in PNCP, not here — so I measured two proxies with the screen itself.

**Proxy A — 200 largest municípios by population** (160k–11.9M): 193 measured.

| Statistic | Handoff claim | Measured (largest 200) |
|---|---:|---:|
| median paid | 76.7% | 84.0% |
| p25 paid | 44.9% | 58.0% |
| p10 paid | 23.5% | 31.8% |
| owed >30% | 43.2% | 32.6% |
| owed >50% | 29.1% | 17.6% |
| wrote off >5% | 6.1% | 9.3% |

This looked like a miss — until the size bias was controlled for. Big cities
pay far better than small ones.

**Proxy B — random samples by population band** (200 each, seed 11):

| Statistic | Handoff | <25k pop (n=69) | 25k–100k pop (n=147) |
|---|---:|---:|---:|
| median paid | 76.7% | 78.6% | **76.6%** |
| p25 paid | 44.9% | 46.4% | 48.2% |
| p10 paid | 23.5% | 27.5% | 21.2% |
| owed >30% | 43.2% | 44.9% | 44.2% |
| owed >50% | 29.1% | 26.1% | 27.9% |
| wrote off >5% | 6.1% | 7.2% | 4.1% |

**The handoff statistics reproduce.** The 25k–100k band matches almost
line for line (median 76.6% vs 76.7% claimed). Treat them as verified *for
small and mid-sized municípios* — which is where kit tenders concentrate — and
as too pessimistic for large cities.

**The core thesis holds: the risk is DELAY, not DEFAULT.** Median cancelados
ratio across the largest 200 is **0.042%** — effectively zero. Municípios pay
late; they very rarely tear the invoice up.

One caveat the brief understates: **14.0%** of the largest 200 breached our
2% write-off limit, and 9.3% wrote off more than 5% (vs 6.1% claimed). The
write-off tail is real, just thin. The screen keeps the two risks on separate
lines for exactly this reason.

---

## 7. **NEW, and the biggest operational finding** — most small municípios cannot be screened at all

Not in the brief, and it dominates everything else.

| Population band | Screenable (PASS+REJECT) | Unscreenable |
|---|---:|---:|
| 200 largest | 96.5% | 3.5% |
| 25k–100k (n=200) | 73.5% | 26.5% |
| **<25k (n=200)** | **34.5%** | **65.5%** |

**Roughly two thirds of small municípios have no RREO Anexo 07 in SICONFI.**

This is *not* a filing lag, and falling back a year does not help — measured
on the identical sample: exercício 2026 → 34.5% screenable; exercício 2025 →
34.5% screenable. Verified at the raw-HTTP level on three of them
(Rodeiro/MG 3156304, Ribeirão Corrente/SP 3543105, Rio Preto/MG 3155900):
**0 rows across every exercício 2024–2026 × every período 1–6**, and 0 rows
for *any* RREO anexo whatsoever. They are simply absent from the dataset.

Why it matters: kit tenders concentrate in exactly this band. The screen will
return UNSCREENABLE for most of them — which is the honest answer, and why
UNSCREENABLE is a first-class outcome rather than a quiet PASS. Plan for
manual diligence on that majority, and do not read UNSCREENABLE as "fine".

---

## 8. Reproducing this

```bash
export ACOLHE_CACHE=/path/to/cache          # disk cache, keyed by URL
python3 screen/buyer.py 1303007 1301209 3523107 1302900 2105104 3147006
python3 screen/buyer.py 04283578000153 --json     # by CNPJ, with evidence
python3 -m pytest tests/test_buyer.py -q           # 52 tests, no network
```

First run over the six: 6.2 s, 7 network calls. Re-run: **0.034 s, 0 network
calls, 7 cache hits.**
