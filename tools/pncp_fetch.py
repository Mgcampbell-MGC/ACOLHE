"""A patient PNCP client for research pulls.
import urllib.parse

MEASURED 2026-09-21: pncp.gov.br is unstable. In one minute the same URL
returned 200, then a bare connection close (curl 52), then a 30-second hang.
Family A (api/consulta/v1) was down entirely while Family B and
/api/search were healthy -- the exact inverse of 2026-09-19.

So: every call retries with backoff, every outcome is recorded, and a value
is NEVER inferred from a failed call. A pull that could not complete says so.
"""
import json
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "ACOLHE-research/1.0 (public procurement analysis)"
MIN_INTERVAL = 1.2          # shared-IP rate limit: 429 seen at ~30 burst
_last = [0.0]
STATS = {"calls": 0, "ok": 0, "fail": 0, "codes": {}}


def _throttle():
    wait = MIN_INTERVAL - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()


def get(url, tries=5, timeout=45):
    """(data, note). data is None when every attempt failed; note says why."""
    last = "no attempt"
    for n in range(tries):
        _throttle()
        STATS["calls"] += 1
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                STATS["ok"] += 1
                STATS["codes"][r.status] = STATS["codes"].get(r.status, 0) + 1
                if not body.strip():
                    return [], "empty body"
                return json.loads(body), f"200 on attempt {n + 1}"
        except urllib.error.HTTPError as e:
            STATS["codes"][e.code] = STATS["codes"].get(e.code, 0) + 1
            last = f"HTTP {e.code}"
            if e.code == 404:
                return None, "404"                      # do not retry a real absence
            if e.code == 429:
                time.sleep(20 + 10 * n)
                continue
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(min(2 ** n + random.random(), 20))
    STATS["fail"] += 1
    return None, f"FAILED after {tries}: {last}"


SEARCH = "https://pncp.gov.br/api/search/"
B = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}"


def search(q, pagina=1, tam=50, tipos="edital", extra=""):
    url = (f"{SEARCH}?tipos_documento={tipos}&q={urllib.parse.quote(q)}"
           f"&pagina={pagina}&tam_pagina={tam}{extra}")
    return get(url)


def itens(cnpj, ano, seq, tam=100):
    return get(B.format(cnpj=cnpj, ano=ano, seq=seq) + f"/itens?pagina=1&tamanhoPagina={tam}")


def resultados(cnpj, ano, seq, numero_item):
    return get(B.format(cnpj=cnpj, ano=ano, seq=seq) + f"/itens/{numero_item}/resultados")


def arquivos(cnpj, ano, seq):
    return get(B.format(cnpj=cnpj, ano=ano, seq=seq) + "/arquivos")


if __name__ == "__main__":
    d, note = search(sys.argv[1] if len(sys.argv) > 1 else "kit natalidade")
    print(note)
    if d:
        print("keys:", list(d.keys()))
        print("total:", d.get("total"), "items:", len(d.get("items", [])))
        if d.get("items"):
            for k, v in d["items"][0].items():
                print(f"  {k:28} {str(v)[:95]}")
