"""Build a call list of municipalities that actually buy kits, with contacts
taken from their OWN published editais.

Same technique that produced the first nine contacts by hand, now that PNCP's
file endpoint is back: for each buyer, list /arquivos, download the edital,
extract the text, and pull the e-mails and phones the document itself prints.

NOBODY IS CONTACTED. This reads published procurement documents only.
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
from pncp_fetch import STATS, arquivos, get  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "buyer_contacts.csv")
UA = "ACOLHE-research/1.0 (public procurement analysis)"

EMAIL = re.compile(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.(?:gov\.br|com\.br|org\.br|com|br)", re.I)
PHONE = re.compile(r"\(?\b(\d{2})\)?\s?[\s.\-]?(9?\d{4})[\s.\-]?(\d{4})\b")
# addresses of the platforms, not the municipality
NOISE = re.compile(r"@(?:bnc|bll|licitanet|portaldecompras|comprasnet|gov\.br$|publicacoes|"
                   r"licitardigital|bbmnet|comprasbr|portaldecompraspublicas)", re.I)


def pdf_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
    except Exception as e:
        return None, f"download failed: {type(e).__name__}"
    if raw[:4] != b"%PDF":
        try:
            return raw.decode("utf-8", "replace"), "plain text"
        except Exception:
            return None, "not a PDF and not text"
    try:
        import pypdf
        rd = pypdf.PdfReader(io.BytesIO(raw))
        return "\n".join((p.extract_text() or "") for p in rd.pages[:25]), f"{len(rd.pages)}p"
    except Exception as e:
        return None, f"pdf parse failed: {type(e).__name__}"


def contacts_from(text, uf):
    flat = re.sub(r"[ \t]+", " ", text or "")
    mails, phones = [], []
    for m in EMAIL.findall(flat):
        pass
    for m in set(re.findall(EMAIL, flat)):
        if not NOISE.search(m) and len(m) < 60:
            mails.append(m.lower())
    for a, b, c in set(PHONE.findall(flat)):
        if a.startswith("0") or a == "00":
            continue
        phones.append(f"({a}) {b}-{c}")
    # prefer a .gov.br address of the municipality itself
    mails.sort(key=lambda x: (0 if ".gov.br" in x else 1, len(x)))
    return mails[:3], phones[:3]


def pick(n_per_uf=3, target=36):
    d = json.load(open(os.path.join(ROOT, "data", "market", "tenders.json"), encoding="utf-8"))
    k = [x for x in d if is_kit((x.get("title") or "") + " " + (x.get("description") or ""))[0]]
    rec = [x for x in k if (x.get("data_publicacao_pncp") or "") >= "2025-09-21"]
    rec.sort(key=lambda x: x.get("data_publicacao_pncp") or "", reverse=True)
    seen_mun, per_uf, out = set(), Counter(), []
    for pref_disp in (True, False):            # dispensas first, then pregões to fill
        for t in rec:
            if len(out) >= target:
                break
            is_disp = t.get("modalidade_licitacao_nome") == "Dispensa"
            if pref_disp != is_disp:
                continue
            mun = (t.get("municipio_nome"), t.get("uf"))
            if mun in seen_mun or per_uf[t.get("uf")] >= n_per_uf:
                continue
            seen_mun.add(mun)
            per_uf[t.get("uf")] += 1
            out.append(t)
    return out


def main():
    cands = pick()
    print(f"{len(cands)} municipalities selected\n")
    rows = []
    for i, t in enumerate(cands, 1):
        cnpj, ano, seq = t["orgao_cnpj"], t["ano"], t["numero_sequencial"]
        arqs, note = arquivos(cnpj, ano, seq)
        mails, phones, src, pages = [], [], "", ""
        if arqs:
            for a in arqs[:3]:
                url = a.get("url") or a.get("uri")
                if not url:
                    continue
                txt, pnote = pdf_text(url)
                if txt:
                    m, p = contacts_from(txt, t.get("uf"))
                    mails += [x for x in m if x not in mails]
                    phones += [x for x in p if x not in phones]
                    src, pages = a.get("titulo") or a.get("tipoDocumentoNome") or "", pnote
                if mails and phones:
                    break
        rows.append({
            "municipio": t.get("municipio_nome"), "uf": t.get("uf"),
            "orgao": t.get("orgao_nome"), "cnpj": cnpj,
            "modalidade": t.get("modalidade_licitacao_nome"),
            "publicado": (t.get("data_publicacao_pncp") or "")[:10],
            "objeto": (t.get("description") or t.get("title") or "")[:180],
            "emails": " · ".join(mails[:3]), "telefones": " · ".join(phones[:3]),
            "fonte": src, "paginas": pages,
            "pncp": f"https://pncp.gov.br/api/consulta/v1/orgaos/{cnpj}/compras/{ano}/{seq}",
            "arquivos_note": note,
        })
        flag = "OK " if mails or phones else "-- "
        print(f"  {flag}{i:>2}/{len(cands)} {str(t.get('municipio_nome'))[:24]:26}{t.get('uf')}  "
              f"{len(mails)}e {len(phones)}t  {note[:22]}")
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    got = sum(1 for r in rows if r["emails"] or r["telefones"])
    print(f"\n{got}/{len(rows)} with at least one contact -> {OUT}")
    print("HTTP:", STATS)


if __name__ == "__main__":
    main()
