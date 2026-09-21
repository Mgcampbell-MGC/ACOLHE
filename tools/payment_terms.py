"""How many days does a DISPENSA actually take to pay?

WHY THIS EXISTS. The business model carries a 45-day cash cycle, and every
capacity number depends on it: lots/year = (capital / cash per lot) x (365 /
float days). But that 45 was read off seven PREGAO editais -- big SRP
contracts with provisional-then-definitive acceptance and a 30-day clock that
only starts once a servidor signs the atesto.

A dispensa is a different instrument: one delivery, no ata, often no formal
recebimento. Nobody has checked whether it pays faster. If it pays in 20 days
instead of 45 the same business earns R$10.235/month instead of R$4.271 --
with no change to capital, cost or win rate. That makes this the cheapest
open question in the project.

METHOD. Take dispensas from the harvested market data, pull each one's
published documents, extract the payment clause, and record BOTH numbers that
matter: the day count, and the EVENT it counts from. docs/ORDER_TO_CASH.md
established that "30 days" means something different in every edital --
from the atesto, from the NF, from delivery, or "up to the 10th of the
following month" -- so a day count without its trigger is not an answer.
"""
import csv
import io
import json
import os
import re
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from market_analyse import is_kit  # noqa: E402
from pncp_fetch import STATS, arquivos  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "payment_terms.csv")
UA = "ACOLHE-research/1.0 (public procurement analysis)"

NUM = {"um": 1, "dois": 2, "tres": 3, "cinco": 5, "sete": 7, "dez": 10, "quinze": 15,
       "vinte": 20, "trinta": 30, "quarenta": 40, "sessenta": 60, "noventa": 90}
# a payment clause: a day count within reach of a payment word
PAY = re.compile(
    r"(?:pagamento|pag\.|paga(?:r|mento)?|quita\w*)[^.]{0,260}?"
    r"(?:at[eé]\s+o?\s*)?(\d{1,3})\s*\(?\s*[a-zçãéê]*\s*\)?\s*"
    r"\(?(dias?|d\.?\s?u\.?|dias?\s+[uú]teis)\)?", re.I)
TRIGGER = [
    (r"atest\w+|atesto", "ATESTO"),
    (r"nota\s+fiscal|NF-?e?\b|fatura", "NOTA FISCAL"),
    (r"recebimento\s+definitivo", "RECEB. DEFINITIVO"),
    (r"recebimento\s+provis", "RECEB. PROVISORIO"),
    (r"entrega|fornecimento", "ENTREGA"),
    (r"m[eê]s\s+subsequente|m[eê]s\s+seguinte", "MES SEGUINTE"),
    (r"liquida[cç][aã]o", "LIQUIDACAO"),
]


def doc_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
    except Exception as e:
        return None, f"download: {type(e).__name__}"
    if raw[:4] == b"%PDF":
        try:
            import pypdf
            rd = pypdf.PdfReader(io.BytesIO(raw))
            return "\n".join((p.extract_text() or "") for p in rd.pages[:40]), f"{len(rd.pages)}p"
        except Exception as e:
            return None, f"pdf: {type(e).__name__}"
    return raw.decode("utf-8", "replace"), "text"


def clause(text):
    """(days, uteis, trigger, verbatim) from the best payment clause found."""
    flat = re.sub(r"\s+", " ", text or "")
    best = None
    for m in PAY.finditer(flat):
        days = int(m.group(1))
        if not 1 <= days <= 120:
            continue
        unit = m.group(2).lower()
        uteis = "til" in unit or re.match(r"d\.?\s?u", unit) is not None
        seg = flat[max(0, m.start() - 200):m.end() + 200]
        trig = next((label for pat, label in TRIGGER if re.search(pat, seg, re.I)), "NAO DITO")
        score = (trig != "NAO DITO", days >= 5)
        if best is None or score > best[0]:
            best = (score, days, uteis, trig, re.sub(r"\s+", " ", seg)[:300])
    return best[1:] if best else (None, None, None, None)


def main(limit=40):
    t = json.load(open(os.path.join(ROOT, "data", "market", "tenders.json"), encoding="utf-8"))
    k = [x for x in t if is_kit((x.get("title") or "") + " " + (x.get("description") or ""))[0]]
    disp = [x for x in k if x.get("modalidade_licitacao_nome") == "Dispensa"]
    preg = [x for x in k if x.get("modalidade_licitacao_nome") == "Pregão - Eletrônico"]
    for g in (disp, preg):
        g.sort(key=lambda x: x.get("data_publicacao_pncp") or "", reverse=True)
    pool = [("Dispensa", x) for x in disp[:limit]] + [("Pregão", x) for x in preg[:limit // 2]]
    rows = []
    for i, (mod, x) in enumerate(pool, 1):
        arqs, note = arquivos(x["orgao_cnpj"], x["ano"], x["numero_sequencial"])
        days = uteis = trig = verb = None
        src = ""
        for a in (arqs or [])[:3]:
            url = a.get("url") or a.get("uri")
            if not url:
                continue
            txt, pnote = doc_text(url)
            if txt:
                days, uteis, trig, verb = clause(txt)
                src = f"{a.get('tipoDocumentoNome') or ''} {pnote}"
            if days:
                break
        rows.append({"modalidade": mod, "municipio": x.get("municipio_nome"), "uf": x.get("uf"),
                     "publicado": (x.get("data_publicacao_pncp") or "")[:10],
                     "dias": days, "dias_uteis": uteis, "contado_de": trig,
                     "verbatim": verb, "fonte": src, "arquivos": note,
                     "pncp": x["numero_controle_pncp"]})
        print(f"  {i:>3}/{len(pool)} {mod[:9]:10}{str(x.get('municipio_nome'))[:20]:22}{x.get('uf')}  "
              f"{str(days or '—'):>4} {'úteis' if uteis else 'corridos' if days else ''} {trig or ''}", flush=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    import statistics as st
    print("\n" + "=" * 78)
    for mod in ("Dispensa", "Pregão"):
        got = [r for r in rows if r["modalidade"] == mod and r["dias"]]
        n = sum(1 for r in rows if r["modalidade"] == mod)
        if not got:
            print(f"{mod}: 0/{n} com cláusula legível"); continue
        d = sorted(r["dias"] for r in got)
        print(f"\n{mod}: {len(got)}/{n} com cláusula legível")
        print(f"   dias: min {d[0]} · p25 {d[len(d)//4]} · MEDIANA {st.median(d)} · "
              f"p75 {d[3*len(d)//4]} · max {d[-1]}")
        print(f"   contado de: {dict(Counter(r['contado_de'] for r in got).most_common())}")
        print(f"   em dias úteis: {sum(1 for r in got if r['dias_uteis'])}/{len(got)}")
    print(f"\n-> {OUT}")
    print("HTTP:", STATS)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
