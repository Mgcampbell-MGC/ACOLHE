"""The certidão expiry tracker. The pack's shortest validity is 30 days
(CRF/FGTS) and CAIXA only reissues from the 5th day before expiry: the
tracker must say RENOVAR inside that window and VENCIDA after it, and must
never turn a fallback period into a verified PASS."""

import os
import sys
from datetime import date

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen import documentos as d  # noqa: E402

TODAY = date(2026, 9, 19)


def test_config_cycle_is_the_shortest_verified_validity():
    cfg = d.load()
    verified = [v["validity_days"] for v in cfg["documents"].values()
                if v.get("validity_verified") and (v.get("validity_days") or 0) > 0]
    assert min(verified) == cfg["cycle"]["shortest_validity_days"] == 30
    assert cfg["cycle"]["renewal_cadence_days"] == 30 - cfg["documents"]["crf_fgts"]["renewable_from_days"]


def test_every_document_has_the_tracker_fields():
    cfg = d.load()
    for doc_id, spec in cfg["documents"].items():
        for key in ("name", "validity_days", "validity_verified", "required_for", "cost_brl"):
            assert key in spec, (doc_id, key)
        if spec["validity_days"] is None:
            # either it never expires, or a fallback is stated -- never silent
            assert "fallback_days" in spec or spec["validity_verified"], doc_id


def test_crf_is_green_then_renew_then_expired():
    fresh = d.status("crf_fgts", TODAY, TODAY)
    assert fresh.state == d.OK and fresh.verified
    assert fresh.expires_on == date(2026, 10, 19)
    assert fresh.renew_from == date(2026, 10, 14)      # 5th day before expiry
    window = d.status("crf_fgts", date(2026, 8, 24), TODAY)   # 26 days old
    assert window.state == d.RENEW
    dead = d.status("crf_fgts", date(2026, 8, 1), TODAY)
    assert dead.state == d.EXPIRED and "HOJE" in dead.reason


def test_printed_valid_until_beats_the_configured_period():
    s = d.status("certidao_rfb_pgfn", date(2026, 9, 1), TODAY, valid_until=date(2026, 9, 25))
    assert s.expires_on == date(2026, 9, 25) and s.verified
    assert s.state == d.RENEW                           # inside the 30-day slack


def test_a_fallback_period_is_never_a_verified_pass():
    s = d.status("cnpj_comprovante", TODAY, TODAY)
    assert s.state == d.OK and not s.verified and "UNVERIFIED" in s.reason
    old = d.status("cnpj_comprovante", date(2026, 5, 1), TODAY)
    assert old.state == d.EXPIRED


def test_per_bid_and_no_expiry_documents_are_not_tracked():
    assert d.status("declaracoes_edital", None, TODAY).state == d.PER_BID
    assert d.status("atestado_capacidade_tecnica", date(2025, 1, 1), TODAY).state == d.NO_EXPIRY
    assert d.status("inscricoes_ie_ccm", date(2025, 1, 1), TODAY).state == d.NO_EXPIRY


def test_a_document_she_never_recorded_is_missing_and_blocks():
    s = d.status("cndt", None, TODAY)
    assert s.state == d.MISSING and s.blocks_bid


def _full_pack(day=TODAY):
    cfg = d.load()
    return {k: day for k, v in cfg["documents"].items() if v["validity_days"] != 0}


def test_can_bid_with_a_fresh_pack_but_flags_the_fallbacks():
    ok, blocking, flags = d.can_bid(_full_pack(), TODAY)
    assert ok and not blocking
    assert {f.doc_id for f in flags} >= {"cnpj_comprovante", "ato_constitutivo",
                                         "certidao_falencia_tjsp", "certidao_rfb_pgfn"}


def test_an_expired_crf_blocks_the_bid():
    pack = _full_pack()
    pack["crf_fgts"] = date(2026, 8, 1)
    ok, blocking, _ = d.can_bid(pack, TODAY)
    assert not ok and [b.doc_id for b in blocking] == ["crf_fgts"]


def test_next_run_on_a_fresh_pack_is_set_by_the_shortest_window():
    """PGE-SP's period is an UNVERIFIED 30-day fallback (site answered 405),
    so it -- not the CRF -- sets the first reissue date: day 20. The CRF
    window opens on day 25. Verifying the e-CRDA period moves this."""
    assert d.next_run(_full_pack(), TODAY) == date(2026, 10, 9)
    rows = d.report(_full_pack(), TODAY)
    assert [r.doc_id for r in rows[:2]] == ["certidao_pge_sp", "crf_fgts"]
    assert rows[1].renew_from == date(2026, 10, 14)


def test_report_sorts_missing_and_expired_ahead_of_green():
    pack = _full_pack()
    del pack["cndt"]
    pack["crf_fgts"] = date(2026, 8, 1)
    rows = d.report(pack, TODAY)
    assert [r.state for r in rows[:2]] == [d.MISSING, d.EXPIRED]
