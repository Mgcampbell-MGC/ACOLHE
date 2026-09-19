"""The 06:00 job. One entrypoint that runs the whole daily loop in order.

    harvest PNCP  ->  find kit tenders  ->  window guard
    ->  descend into each item list     ->  the workbook

Deliberately thin: every step lives in its own module with its own tests.
This file only sequences them and refuses to hide a failure between them.

Two things it does NOT do, on purpose:
  * It never swallows a harvest failure. If PNCP is down for the listing,
    that raises, the cron shows red, and no workbook is written that could
    be mistaken for a quiet day.
  * It does not send anything. The push (email, Google Sheet) is Step 8 and
    is held until the reading rail's status is known. The workbook on disk
    is the output for now.

A descent that comes back UNAVAILABLE is NOT a failure of this job: it is a
fact about PNCP Family B that the workbook reports per tender as VERIFICAR
with the reason. The scan is still worth having without it.
"""

import datetime
import json
import os
import sys

from harvest.daily import scan, summarise as summarise_scan
from harvest.descend import descend, summarise as summarise_descent
from harvest.pncp_client import PNCPClient, jsonl_sink
from report.digest import build

DEFAULT_STATE = os.environ.get("ACOLHE_STATE", os.path.expanduser("~/.acolhe/state"))
DEFAULT_CACHE = os.environ.get("ACOLHE_CACHE", os.path.expanduser("~/.acolhe/cache"))


def _default_buyer_screen(cnpj, cod_ibge):
    """SICONFI payment-risk screen for one buyer. Returns (passed, reason, evidence).

    Called with the codigoIbge PNCP itself puts on every tender row -- never
    with a code typed or remembered. On 2026-09-19 a typed code screened the
    wrong municipio and was reported as verification; this path cannot make
    that mistake because it never handles a code a human wrote down.
    """
    from screen.buyer import ScreenRequest, SiconfiUnavailable, screen_buyer

    try:
        return screen_buyer(ScreenRequest(cnpj=str(cnpj or ""),
                                          cod_ibge=str(cod_ibge or "")))
    except SiconfiUnavailable as exc:
        return False, f"SICONFI indisponivel: {exc}", {"outcome": "UNSCREENABLE"}


_VERDICT_PT = {"PASS": "PAGA", "REJECT": "NAO PAGA", "UNSCREENABLE": "NÃO VERIFICÁVEL"}


def run(day, out_xlsx, client=None, state_dir=None, cache_dir=None,
        modalidades=(6, 7, 8), today=None, now=None, do_descend=True,
        min_interval=1.1, buyer_screen=None):
    """Run one day. Returns everything the caller might want to inspect.

    day        'YYYYMMDD' -- the publication day to harvest (yesterday, in cron)
    out_xlsx   where the workbook goes; her typed columns are read back first
    client     injectable for tests; a real PNCPClient otherwise
    """
    state_dir = state_dir or DEFAULT_STATE
    cache_dir = cache_dir or DEFAULT_CACHE
    os.makedirs(state_dir, exist_ok=True)
    today = today or datetime.date.today()
    now = now or datetime.datetime.now()

    if client is None:
        client = PNCPClient(cache_dir=cache_dir, state_dir=state_dir,
                            min_interval=min_interval, concurrency=1)

    # 1. harvest -- a failure here RAISES. No silent quiet day.
    sink_path = os.path.join(state_dir, f"harvest-{day}.jsonl")
    sink = jsonl_sink(sink_path)
    try:
        report = client.harvest_day(day, modalidades=list(modalidades), sink=sink)
    finally:
        sink.close()
    with open(sink_path, encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh if line.strip()]

    # 2. find kit tenders; 3. window guard (inside scan)
    candidates, near_misses, stale = scan(rows, day=day, now=now)

    # 4. descend -- UNAVAILABLE is reported per tender, never raised here
    descent = []
    if do_descend and candidates:
        descent = descend(client, candidates)
        for cand, rec in zip(candidates, descent):
            cand["items_status"] = rec["items_status"]
            cand["items"] = rec["items"]
            cand["items_error"] = rec.get("error")

    # 4b. screen the buyer -- with PNCP's own codigoIbge, never a typed code.
    # A REJECT is a rule-6 failure the workbook renders as NAO LICITAR with
    # the reason; UNSCREENABLE stays visible as exactly that.
    screen = buyer_screen if buyer_screen is not None else _default_buyer_screen
    for cand in candidates:
        passed, reason, evidence = screen(cand.get("cnpj"), cand.get("ibge"))
        outcome = (evidence or {}).get("outcome") or ("PASS" if passed else "UNSCREENABLE")
        cand["buyer_outcome"] = outcome
        cand["buyer_verdict"] = _VERDICT_PT.get(outcome, outcome)
        cand["buyer_reason"] = reason
        cand["buyer_evidence"] = evidence
        if outcome == "REJECT":
            cand.setdefault("rule_results", {})["6"] = {
                "passed": False, "is_flag": False, "reason": reason}

    # 5. the workbook -- her columns are read back before anything is written
    build(out_xlsx, candidates, health=report, today=today,
          stale=stale, near_misses=near_misses)

    return {
        "day": day,
        "rows": len(rows),
        "candidates": candidates,
        "near_misses": near_misses,
        "stale": stale,
        "descent": descent,
        "report": report,
        "out_xlsx": out_xlsx,
    }


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        print("usage: python -m harvest.run_daily YYYYMMDD OUT.xlsx [--no-descend]",
              file=sys.stderr)
        return 2
    day, out = argv[0], argv[1]
    result = run(day, out, do_descend="--no-descend" not in argv)
    print(summarise_scan(result["candidates"], result["near_misses"],
                         result["stale"], report=result["report"]))
    if result["descent"]:
        print()
        print(summarise_descent(result["descent"]))
    print(f"\nworkbook: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
