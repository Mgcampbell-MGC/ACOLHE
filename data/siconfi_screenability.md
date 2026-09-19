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

## Two corrections to the agent report that produced screen/buyer.py

1. **Its named examples are wrong.** It reported Rodeiro/MG and Ribeirão
   Corrente/SP as verified at raw-HTTP level to have "0 rows across every
   exercício 2024-2026 × every período 1-6". Both return full, usable data on
   the first call:

   - Rodeiro/MG (3143906): 71 rows; inscritos R$22.624.463,06;
     saldo 1,49%; cancelados 0,61% → PASS
   - Ribeirão Corrente/SP (3543501): 43 rows; inscritos R$1.033.597,97;
     saldo 7,02% → PASS

   Its headline *direction* survives — most small municípios genuinely cannot
   be screened — but the specific verification behind it did not hold, and
   its 34,5% sits at the bottom of the interval measured here.

2. **Its zero-row finding is CONFIRMED and is the important one.** SICONFI
   omits zero-valued rows entirely, so a column is absent rather than zero:
   - Nhamundá/AM has **no `Pagos (c)` row** — because it paid nothing.
   - Ribeirão Corrente/SP has **no `Cancelados (d)` row**.

   A reader that treats an absent column as "no data" drops exactly the worst
   payers in Brazil out of the screen. `pagos` must be derived from the
   published identity `c = (a+b) − d − e`, with the source recorded.
