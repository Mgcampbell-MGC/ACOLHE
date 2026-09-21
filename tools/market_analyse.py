"""What the kit-natalidade market actually looks like, from PNCP results.

METHOD, stated up front because the conclusions depend on it:

1. /api/search is FULL TEXT. "kit natalidade" matches 2.776 documents, and
   that number is NOT a count of kit tenders -- it includes school kits,
   hospital linen and anything whose text happens to contain the words. Every
   row is therefore re-filtered here through parse/normalise.kit_signal, the
   same filter the daily scanner uses, and the discard count is reported.

2. A tender's STRUCTURE decides what a price means. Two shapes exist:
      LOTE      the whole kit is one line. valorUnitario = price per KIT.
      PER-ITEM  each of the ~17 articles is its own line. valorUnitario =
                price of one article, and the kit price is the sum.
   Mixing them produces nonsense. On 2026-09-20 a clearing-ratio claim was
   made from a per-item figure and applied to a lote; this module keeps them
   apart and reports each separately, with n.

3. A ratio is only computed where BOTH the estimate and the homologated value
   are present and positive. Missing is missing.
"""
import json
import os
import re
import statistics as st
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harvest.daily import kit_signal  # noqa: E402
from parse.normalise import strip_accents  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, "data", "market")

# A single line whose text enumerates the whole kit -> LOTE.
_LOTE = re.compile(r"KIT\s+\w*\s*CONTENDO|CONTENDO\s*:?\s*\d|COM\s+\d{1,2}\s+ITENS|"
                   r"COMPOSTO\s+(?:POR|DE)\s+\d{1,2}\s+ITENS")


def load(name):
    p = os.path.join(M, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def is_kit(text):
    ok, matched, excl = kit_signal(text or "")
    return ok, excl


def structure(rec):
    """LOTE / PER_ITEM / SINGLE / UNKNOWN for one tender."""
    items = rec.get("itens") or []
    if not items:
        return "UNKNOWN"
    if len(items) == 1:
        d = strip_accents(items[0].get("descricao") or "").upper()
        return "LOTE" if _LOTE.search(d) else "SINGLE"
    # several lines: a lote split into ampla + cota ME/EPP is still a lote
    lote_like = sum(1 for i in items if _LOTE.search(strip_accents(i.get("descricao") or "").upper()))
    if lote_like >= max(1, len(items) // 2):
        return "LOTE"
    return "PER_ITEM" if len(items) >= 5 else "SINGLE"


def kit_price(rec, kind):
    """(estimated_per_kit, homologated_per_kit, qty) or (None, None, None).

    LOTE      -> the per-unit values ARE per kit; quantities add up.
    PER_ITEM  -> the kit is the SUM of one of each line; a line whose price is
                 missing makes the whole kit unknown, exactly like a BOM gap.
    """
    items = rec.get("itens") or []
    if kind == "LOTE":
        est = [i["valorUnitarioEstimado"] for i in items if i.get("valorUnitarioEstimado")]
        hom, qty = [], 0
        for i in items:
            for r in (i.get("resultados") or []):
                if r.get("valorUnitarioHomologado"):
                    hom.append(r["valorUnitarioHomologado"])
                    qty += r.get("quantidadeHomologada") or 0
        if not est:
            return None, None, None
        # ampla + cota are the same kit at the same price: take the median
        return st.median(est), (st.median(hom) if hom else None), (qty or None)
    if kind == "PER_ITEM":
        est = 0.0
        for i in items:
            v = i.get("valorUnitarioEstimado")
            if not v:
                return None, None, None
            est += v
        hom, complete = 0.0, True
        for i in items:
            rs = [r for r in (i.get("resultados") or []) if r.get("valorUnitarioHomologado")]
            if not rs:
                complete = False
                break
            hom += min(r["valorUnitarioHomologado"] for r in rs)
        qty = max((i.get("quantidade") or 0) for i in items) or None
        return est, (hom if complete else None), qty
    return None, None, None


def main():
    tenders = load("tenders.json")
    results = {r["key"]: r for r in load("results.json")}
    print(f"PASS 1: {len(tenders)} distinct tenders matched by full-text search")
    print(f"PASS 2: {len(results)} descended (those PNCP flagged tem_resultado)\n")

    kept, dropped = [], Counter()
    for t in tenders:
        ok, excl = is_kit((t.get("title") or "") + " " + (t.get("description") or ""))
        (kept.append(t) if ok else dropped.update([excl or "no kit pattern"]))
    print(f"FILTER: {len(kept)} survive the scanner's own kit filter, {len(tenders) - len(kept)} discarded")
    for k, v in dropped.most_common(8):
        print(f"   discarded {v:4}  {k}")

    keys = {t["numero_controle_pncp"] for t in kept}
    print(f"\n--- WHO BUYS  (n={len(kept)} filtered tenders)")
    print("  UF:", dict(Counter(t.get("uf") for t in kept).most_common(12)))
    print("  modalidade:", dict(Counter(t.get("modalidade_licitacao_nome") for t in kept).most_common()))
    fundo = sum(1 for t in kept if "FUNDO" in (t.get("orgao_nome") or "").upper())
    print(f"  bought through a FUNDO (not the prefeitura): {fundo} / {len(kept)} = {fundo/max(1,len(kept)):.0%}")
    anos = Counter(t.get("ano") for t in kept)
    print("  ano:", dict(sorted(anos.items())))
    meses = Counter((t.get("data_publicacao_pncp") or "")[5:7] for t in kept if t.get("data_publicacao_pncp"))
    print("  mês de publicação:", dict(sorted(meses.items())))

    print(f"\n--- PRICES, BY TENDER STRUCTURE (this is the distinction that matters)")
    by = {}
    for key, rec in results.items():
        if key not in keys:
            continue
        kind = structure(rec)
        est, hom, qty = kit_price(rec, kind)
        by.setdefault(kind, []).append((rec, est, hom, qty))
    for kind, rows in sorted(by.items()):
        priced = [(r, e, h, q) for r, e, h, q in rows if e and h and e > 0]
        print(f"\n  {kind}: {len(rows)} tenders, {len(priced)} with BOTH an estimate and a homologated price")
        if not priced:
            continue
        ratios = sorted(h / e for _, e, h, _ in priced)
        kits = sorted(h for _, _, h, _ in priced)
        qtys = sorted(q for _, _, _, q in priced if q)
        def band(v, f="{:.1f}"):
            return (f"min {f.format(v[0])} · p25 {f.format(v[len(v)//4])} · MEDIAN {f.format(st.median(v))}"
                    f" · p75 {f.format(v[3*len(v)//4])} · max {f.format(v[-1])}")
        print(f"    clearing ratio (homologado / estimado): {band(ratios, '{:.0%}')}")
        print(f"    price per kit homologado (R$):          {band(kits, '{:,.2f}')}")
        if qtys:
            print(f"    kits per contract:                      {band(qtys, '{:,.0f}')}")
        portes = Counter(r.get("porteFornecedorNome") for _, _, _, _ in [] )
        portes = Counter()
        wins = Counter()
        for rec, _, _, _ in priced:
            for i in rec["itens"]:
                for r in (i.get("resultados") or []):
                    if r.get("porteFornecedorNome"):
                        portes.update([r["porteFornecedorNome"]])
                    if r.get("niFornecedor"):
                        wins.update([(r["niFornecedor"], r.get("nomeRazaoSocialFornecedor"))])
        print(f"    porte do vencedor: {dict(portes.most_common())}")
        top = wins.most_common(6)
        print(f"    distinct winners: {len(wins)}; most frequent:")
        for (cnpj, nome), n in top:
            print(f"        {n[:46]:48} {cnpj}  x{n if False else ''}{wins[(cnpj,nome)]}")

    print("\n--- WHAT COULD NOT BE PRICED")
    for kind, rows in sorted(by.items()):
        miss = [r for r, e, h, q in rows if not (e and h)]
        print(f"  {kind}: {len(miss)} of {len(rows)} lack a usable estimate/homologated pair")


if __name__ == "__main__":
    main()
