# ACOLHE

A one-person government-supply desk selling newborn layette kits
(kits natalidade / enxoval) to Brazilian municipalities.

`Lei 14.133/2021 art. 54` compels every contracting body to publish its
complete tender document, item list included, on PNCP before it may buy.
The machine reads those tenders, prices them, screens them, and proposes a bid.

## Status

**Step 0 — closing the cost table.** In progress. See `data/cost_table.csv`
and `docs/STEP0_FINDINGS.md`.

## Layout

    config/   skus.yaml, rules.yaml, ufs.yaml
    harvest/  PNCP clients and the daily fetch
    parse/    normalise.py -- THE FIVE FILTERS. Nothing bypasses it.
    price/    cost, BOM, margin
    screen/   the 11 admission rules and the SICONFI buyer screen
    log/      the bid log -- append-only, the only asset that compounds
    report/   the daily digest
    tools/    catalogue harvesters
    tests/    test_traps.py -- one regression test per known measurement error

## Rules that govern this repo

- Every number needs a primary-source URL. Write UNVERIFIED where one cannot
  be had. A flagged gap is worth more than a plausible figure.
- Every aggregate computed from a government API is wrong until filtered.
  Apply the five filters in `parse/normalise.py` before believing anything.
- Observed listings beat published claims.
- When a correction lands, propagate it to every claim that depends on it.
