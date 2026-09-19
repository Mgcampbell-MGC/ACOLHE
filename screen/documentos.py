"""The certidão expiry tracker, on top of config/documentos.yaml.

A certidão lapsing is the one way to lose a tender she already WON: Lei
14.133 art. 63 II-III demands the pack from the winner after julgamento and
art. 92 XVI again at every payment. The shortest validity in the pack is 30
days (CRF/FGTS, Manual CAIXA v19 item 2.7.1), renewable only from the 5th
day before expiry -- so the whole company runs on a ~25-day cadence.

Pure functions. The caller supplies what she recorded: for each document,
the issue date and, when the document prints its own "válida até", that
date -- it is preferred over the configured period. Nothing here PASSes on
a guess: a period the issuer does not fix is a fallback and is flagged
UNVERIFIED even while it is green.
"""

import os
from dataclasses import dataclass
from datetime import date, timedelta

import yaml

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "documentos.yaml"
)

# How long before expiry the machine asks her to reissue, when the issuer
# does not restrict early issuance. 180-day certidões are reissued with the
# semester slack from the config (180 - 150 = 30 days).
OK, RENEW, EXPIRED, MISSING, PER_BID, NO_EXPIRY = (
    "OK", "RENOVAR", "VENCIDA", "FALTA", "POR_CERTAME", "SEM_VALIDADE")


@dataclass
class Status:
    doc_id: str
    name: str
    state: str
    expires_on: date | None
    renew_from: date | None
    days_left: int | None
    verified: bool          # False = the period is a fallback the issuer never fixed
    reason: str
    required_for: tuple

    @property
    def blocks_bid(self):
        return "bid" in self.required_for and self.state in (EXPIRED, MISSING)


def load(path=_CONFIG_PATH):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _as_date(value):
    if value is None or isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def status(doc_id, issued_on, today, valid_until=None, config=None):
    """State of ONE document. issued_on None = she never recorded it."""
    config = config or load()
    spec = config["documents"][doc_id]
    name = spec["name"]
    req = tuple(spec.get("required_for") or ())
    cycle = config.get("cycle") or {}
    slack = int(cycle.get("semester_cycle_days", 150))
    slack = max(1, 180 - slack)
    issued_on, valid_until = _as_date(issued_on), _as_date(valid_until)
    period = spec.get("validity_days")
    verified = bool(spec.get("validity_verified"))

    if period == 0:
        return Status(doc_id, name, PER_BID, None, None, None, True,
                      "emitida a cada certame / contrato -- nao expira, nao se rastreia", req)

    if issued_on is None and valid_until is None:
        return Status(doc_id, name, MISSING, None, None, None, verified,
                      "nunca registrada -- emitir e anotar a data", req)

    if valid_until is not None:
        expires, verified, basis = valid_until, True, "validade impressa no documento"
    elif period is None:
        fallback = spec.get("fallback_days")
        if not fallback:
            return Status(doc_id, name, NO_EXPIRY, None, None, None, True,
                          "o emissor nao fixa validade e o fato atestado nao expira", req)
        expires, verified = issued_on + timedelta(days=int(fallback)), False
        basis = f"prazo de {fallback} dias e' um FALLBACK (edital costuma exigir) -- UNVERIFIED"
    else:
        expires = issued_on + timedelta(days=int(period))
        basis = f"{period} dias ({'fonte lida' if verified else 'NAO LIDO'})"

    # Reissue window: the issuer's own limit when it has one (CRF: from the
    # 5th day before), otherwise the semester slack capped at a third of the
    # period so a 30-day fallback is not RENOVAR from the day it is issued.
    early = spec.get("renewable_from_days")
    lead = int(early) if early else min(slack, max(1, (expires - issued_on).days // 3)
                                        if issued_on else slack)
    renew_from = expires - timedelta(days=lead)
    days_left = (expires - today).days
    if days_left < 0:
        state, why = EXPIRED, f"venceu ha {-days_left} dias -- reemitir HOJE"
    elif today >= renew_from:
        state, why = RENEW, f"vence em {days_left} dias -- reemitir agora"
    else:
        state, why = OK, f"vence em {days_left} dias; reemitir a partir de {renew_from.isoformat()}"
    return Status(doc_id, name, state, expires, renew_from, days_left, verified,
                  f"{why}; {basis}", req)


def report(issued, today, config=None):
    """All documents, most urgent first.

    issued: {doc_id: date | (issued_on, valid_until)} as she recorded them.
    A document absent from the dict is MISSING.
    """
    config = config or load()
    out = []
    for doc_id in config["documents"]:
        rec = issued.get(doc_id)
        issued_on, valid_until = (rec if isinstance(rec, tuple) else (rec, None))
        out.append(status(doc_id, issued_on, today, valid_until, config))
    rank = {MISSING: 0, EXPIRED: 1, RENEW: 2, OK: 3, PER_BID: 4, NO_EXPIRY: 5}
    out.sort(key=lambda s: (rank[s.state], s.days_left if s.days_left is not None else 10**6))
    return out


def can_bid(issued, today, config=None):
    """(ok, blocking, flags). Blocking = a bid-required document expired or
    never recorded. Flags = green on a fallback period -- she may bid, the
    edital may still disagree, and the row says so."""
    rows = report(issued, today, config)
    blocking = [r for r in rows if r.blocks_bid]
    flags = [r for r in rows if r.state in (OK, RENEW) and not r.verified]
    return not blocking, blocking, flags


def next_run(issued, today, config=None):
    """The date the machine must next tell her to reissue something --
    the renewal cadence made concrete. None when nothing is tracked."""
    dates = [r.renew_from for r in report(issued, today, config)
             if r.renew_from is not None and r.state == OK]
    return min(dates) if dates else None
