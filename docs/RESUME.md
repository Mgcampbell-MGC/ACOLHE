# RESUME — where the build stands (written 2026-09-19, end of day)

Read this first in a fresh session. Everything below is committed on
`claude/hopeful-lamport-0uqn9c`; the working tree was clean at the time.

## Standing orders from the founder (do not re-ask)
- No money spent, nothing registered, no supplier or buyer contacted, no PR
  opened — **ask first** for any of those. Nothing of the kind has happened.
- Capital is a DIAL (`config/capital.yaml: capital.available_brl: null`),
  not R$15.600. Rule 12 says UNVERIFIABLE until she sets it.
- Co-packer is part of the plan: wholesalers (SP) → co-packer (SP) → one
  consolidated shipment → município. C3 forbids employees/contractors; a
  co-packer is a vendor.
- Email heartbeat + Google Sheets writer are **HELD until Monday's Family B
  verdict** ("hold everything until Monday tells us whether the reading rail
  is coming back"). Needs from her when unheld: Google service-account JSON,
  mail API key, `capital.available_brl`.

## Monday 2026-09-21 11:00Z — trigger `trig_01EjwvkCJ5bApz7EZXQcVgUu`
1. Re-try PNCP Family B (`api/pncp/v1 .../itens`, 503 all day 19/09, HAProxy
   empty pool; log in `data/editais/familyB_retry_log.txt`).
2. If up: run a real descent, fix the UNVERIFIED item field names in
   `harvest/descend.py`, price `kit_enxoval`, then call the Step 0 gate
   (task #4: BOM ≤R$200 build all; 200–230 supplier account first; >230 stop).
   Current: R$198,78 for 16/17 lines; gross ~18% at 75% anchor with LTL,
   negative with parcel freight (`docs/BUSINESS_OPERATING_SYSTEM.md` §9).
3. If still down: say so; the scanner (Family A) still works — 4 live
   candidates found on a real day.

## What was built today (all tested; 370 tests, `set -o pipefail` always)
- Rule 13 (`screen/rules.py`): SRP call-off she cannot serve → refuse.
- `screen/documentos.py` + `config/documentos.yaml` + `docs/HABILITACAO.md`:
  certidão tracker; company runs on a 25-day cadence (CRF/FGTS 30 days).
- `parse/entrega.py`: local de entrega → ONE_ADDRESS / CALLOFF / HOUSEHOLD /
  UNKNOWN; `.freight_mode` for `price/freight.estimate`. 9/9 real texts match.
- `docs/BUSINESS_OPERATING_SYSTEM.md`: only PENDING left is Family B.

## Next in line (task #8, in progress — nothing of it written yet)
`harvest/run_daily.py` runs harvest → scan → descend → buyer screen → workbook
but does NOT yet run `screen.rules.run_all` or price (`price.bom.build` +
`price.freight.estimate(uf, qty, mode)` + `price.margin.suggest_bid`).
Plan: a `screen/admit.py` that builds the tender dict from a candidate
(objeto, items, item_count, classified_count, uf, uf_feasibility via
`feasibility_from_config(quantity)`, siconfi from buyer evidence, line_values,
quantity, srp, capital from `config/capital.yaml`, cogs_per_kit from the BOM,
edital_text None until `/arquivos` is read → rules 2/3/9/10 stay VERIFICAR),
converts `Result` → `rule_results[id] = {passed, is_flag, reason}` for
`report/digest._decision`, and sets `suggested_bid` / `bid_rationale` /
`price_blocked`. Fixtures: `tests/test_run_daily.py` StubClient.

## Known open gaps (all listed in BOS §8)
Interior-CEP freight; LTL tables beyond SP→CE; co-packer quote (never sent);
account-tier discount (15 supplier emails, never sent); PGE-SP / RFB validity
read at source; Licitanet fees.
