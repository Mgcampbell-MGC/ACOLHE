# ACOLHE

A one-person government-supply desk selling newborn layette kits
(kits natalidade / enxoval) to Brazilian municipalities.

`Lei 14.133/2021 art. 54` compels every contracting body to publish its
complete tender document, item list included, on PNCP before it may buy.
The machine reads those tenders, prices them, screens them, and proposes a bid.
She decides. Nothing is bought until it is sold; nothing is stored; nobody is
employed.

**Start here:** `docs/BUSINESS_OPERATING_SYSTEM.md` — the whole business as
one system, with every number's provenance and every gap marked.

## Status, 2026-09-19

| Step | State |
|---|---|
| 0 Cost table | 16 of 17 lines priced at observed catalogue prices, **R$ 176,32**. `kit_enxoval` blocked on the unreadable edital. Assembly and freight UNQUOTED. Gate uncalled. |
| 1 PNCP client | **Acceptance met** — second run zero network calls; kill/resume loses nothing. Family B (item detail) 503 all day; Monday re-check scheduled. |
| 2 Normaliser + traps | 11 of 11 traps regression-tested |
| 3 Spec control | 24 SKUs; 18/20 on a real edital |
| 4 Edital parser | not started (blocked on Family B `/arquivos`) |
| 5 Rules + buyer screen | **12 rules** incl. rule 12 (can she carry the win); SICONFI screen with UNSCREENABLE as a first-class outcome |
| 6 Margin engine | NO BID on an incomplete or stale BOM |
| 7 Bid log + workbook | append-only log; Portuguese workbook, her columns never overwritten |
| 8 Deploy + push | held until Monday's Family B verdict |

**280 tests.** Six research workstreams in flight: co-packing, freight,
habilitação, order-to-cash, company setup, risk register.

## Layout

    config/   skus, rules, capital (a dial), ufs, documentos*, order_to_cash*, cnaes*
    harvest/  PNCP client, the daily national scanner + window guard
    parse/    normalise.py -- THE FIVE FILTERS. Nothing bypasses it. spec.py
    price/    cost (provenance enforced, +6 pt interstate, freshness), BOM vs FLOOR, margin
    screen/   the 12 admission rules; the SICONFI buyer screen
    log/      the bid log -- append-only, the only asset that compounds
    report/   the daily workbook she reads
    data/     cost tables, 7 real editais, SICONFI measurements
    docs/     LEGAL_FINDINGS, BUSINESS_OPERATING_SYSTEM, and the pending research
    tests/    one regression test per known measurement error, and growing
    (* = pending)

## Rules that govern this repo

- Every number needs a primary-source URL. Write UNVERIFIED where one cannot
  be had. A flagged gap is worth more than a plausible figure.
- Every aggregate computed from a government API is wrong until filtered.
- A rule that cannot verify returns VERIFICAR, never PASS.
- Observed listings beat published claims. A trading name is not an address.
- When a correction lands, propagate it to every claim that depends on it.
- Run tests with `set -o pipefail`; a red suite never commits.
