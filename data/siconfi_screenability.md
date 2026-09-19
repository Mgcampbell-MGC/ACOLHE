# How many of our actual buyers can the SICONFI screen actually screen?

Measured 2026-09-19 by the main session, independently of the agent that built
`screen/buyer.py`. Every figure here came from a live call.

## The question

Rule 6 rejects a buyer on its payment record. That is only useful if the
record exists. It mostly does not.

## Measurement

Universe, from `apidatalake.tesouro.gov.br/ords/siconfi/tt/entes`:

| | |
|---|---|
| municípios total | **5.570** |
| under 25.000 population | **4.151 (74,5%)** |

Random sample of 60 municípios under 25.000 population, seed 7, querying
`RREO-Anexo 07`, exercício 2026, período 3, and requiring a `TOTAL` row
carrying `RestosAPagarProcessadosENaoProcessadosLiquidadosInscritos`:

| outcome | n | share |
|---|---|---|
| **SCREENABLE** | 27/60 | **45,0%** |
| no usable RREO Anexo 07 | 33/60 | 55,0% |
| fetch errors | 0 | — |

At n=60 the 95% interval is roughly ±12,6 points, so 45,0% spans about
32% to 58%.

## What this means for the business

**Three quarters of Brazilian municípios are under 25.000 people, and that is
exactly where kit tenders concentrate. Roughly half of them cannot be screened
at all.**

So rule 6 will return UNSCREENABLE — not PASS, not REJECT — for a large share
of real targets. That is why UNSCREENABLE is a first-class outcome in
`screen/rules.py` and why `unscreenable_is_a_pass` defaults to false in
`config/rules.yaml`. A buyer we cannot screen is not a buyer that screened
clean.

The operational consequence is that manual diligence on small buyers is not an
edge case, it is the normal path, and the digest must make that visible rather
than letting a silent UNSCREENABLE look like a quiet pass.

## A retraction, and what actually held

**My earlier "correction" of the buyer-screen agent was wrong, and the agent
was right.** I claimed Rodeiro/MG and Ribeirão Corrente/SP returned full,
usable RREO data and therefore its named evidence "did not hold". I had typed
IBGE codes from memory — 3143906 and 3543501 — instead of looking them up.
Those codes belong to other municípios. The real codes, from the SICONFI
`entes` table, are:

| município | correct cod_ibge | rows, 2026 período 3 |
|---|---|---|
| Rodeiro/MG | **3156304** | **0 — UNSCREENABLE** |
| Ribeirão Corrente/SP | **3543105** | **0 — UNSCREENABLE** |
| (code I used) 3143906 | a different ente | 71 |
| (code I used) 3543501 | a different ente | 43 |

So the agent's two named examples stand. This is the exact "label right,
identifier wrong" error class this project keeps catching, and this time it
was mine. The adversarial risk-register workstream caught the mismatch by
noticing the two SICONFI documents disagreed on the same município's code.

What still holds from my measurement: the **45,0% screenable (n=60, ±12,6
pp)** figure was drawn from `entes.json` with real `cod_ibge` values, not
typed ones, so it is unaffected. The agent's 34,5% sits inside that interval.
The business conclusion is unchanged and, if anything, firmer: **roughly half
to two-thirds of small municípios cannot be screened, and rule 6 must return
UNSCREENABLE for them — never a quiet pass.**

## The finding that is confirmed and matters most

SICONFI omits zero-valued rows entirely, so a column is *absent* rather than
zero: Nhamundá/AM has **no `Pagos (c)` row** precisely because it paid
nothing. A reader treating an absent column as "no data" drops the worst
payers in Brazil out of the screen. `pagos` must be derived from the
published identity `c = (a+b) − d − e`, with the source recorded.

## Lesson written into the repo

Never type an identifier. Resolve every município to its `cod_ibge` from the
`entes` table, and every company to its UF from its CNPJ. `harvest/daily.py`
already carries `unidadeOrgao.codigoIbge` from PNCP on every candidate; the
buyer screen must be called with THAT, not with a looked-up or remembered
code.
