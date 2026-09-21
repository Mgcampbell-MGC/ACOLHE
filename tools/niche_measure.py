"""Measure a candidate niche exactly as the kit natalidade market was measured.

Same two passes, same filters, same separation of tender structures. The point
is comparability: a niche only beats the kit if it beats it on the numbers that
decided the kit -- clearing ratio by mechanism, and supplier concentration.
"""
import json
import os
import statistics as st
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pncp_fetch import STATS, itens, resultados, search  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NICHES = {
    "medalhas": (["medalhas trofeus", "troféus premiacao", "medalha personalizada"],
                 r"MEDALH|TROFEU|TROFÉU|PREMIACAO|PREMIAÇÃO"),
    "camisetas": (["camisetas personalizadas evento", "confeccao camisetas uniforme evento",
                   "camiseta silk screen"], r"CAMISET|CAMISA\b"),
    "expediente": (["material de expediente papelaria", "material de expediente escritorio"],
                   r"EXPEDIENTE|PAPELARIA|ESCRIT[OÓ]RIO"),
}


def run(name, queries, keep, max_pages=20, descend=90):
    out = os.path.join(ROOT, "data", "market", f"niche_{name}")
    os.makedirs(out, exist_ok=True)
    found = {}
    for q in queries:
        for p in range(1, max_pages + 1):
            d, note = search(q, pagina=p, tam=50)
            if d is None:
                continue
            items = d.get("items") or []
            if not items:
                break
            for it in items:
                if it.get("numero_controle_pncp"):
                    found.setdefault(it["numero_controle_pncp"], it)
            if len(items) < 50:
                break
        print(f"  [{name}/{q}] -> {len(found)} cumulative")
    import re
    pat = re.compile(keep, re.I)
    kept = [t for t in found.values()
            if pat.search((t.get("title") or "") + " " + (t.get("description") or ""))]
    json.dump(kept, open(os.path.join(out, "tenders.json"), "w"), ensure_ascii=False)
    print(f"  {name}: {len(found)} hits, {len(kept)} survive the keyword filter")

    todo = [t for t in kept if t.get("tem_resultado")]
    todo.sort(key=lambda t: t.get("data_publicacao_pncp") or "", reverse=True)
    todo = todo[:descend]
    recs = []
    for i, t in enumerate(todo, 1):
        its, note = itens(t["orgao_cnpj"], t["ano"], t["numero_sequencial"])
        rec = {"key": t["numero_controle_pncp"], "uf": t.get("uf"),
               "modalidade": t.get("modalidade_licitacao_nome"),
               "municipio": t.get("municipio_nome"), "itens": []}
        for it in (its or []):
            row = {k: it.get(k) for k in ("numeroItem", "quantidade", "valorUnitarioEstimado",
                                          "temResultado")}
            row["descricao"] = (it.get("descricao") or "")[:200]
            if it.get("temResultado"):
                res, _ = resultados(t["orgao_cnpj"], t["ano"], t["numero_sequencial"],
                                    it.get("numeroItem"))
                row["res"] = [{k: r.get(k) for k in ("niFornecedor", "nomeRazaoSocialFornecedor",
                                                     "porteFornecedorNome", "valorUnitarioHomologado",
                                                     "quantidadeHomologada")} for r in (res or [])]
            rec["itens"].append(row)
        recs.append(rec)
        if i % 15 == 0:
            print(f"    {name} {i}/{len(todo)}")
            json.dump(recs, open(os.path.join(out, "results.json"), "w"), ensure_ascii=False)
    json.dump(recs, open(os.path.join(out, "results.json"), "w"), ensure_ascii=False)
    return kept, recs


def analyse(name, kept, recs):
    print(f"\n===== {name.upper()}")
    print(f"  tenders kept: {len(kept)} · descended: {len(recs)}")
    print("  modalidade:", dict(Counter(t.get("modalidade_licitacao_nome") for t in kept).most_common(4)))
    # clearing ratio PER LINE (these niches are mostly per-item, not kits)
    by_mod = {}
    wins = Counter()
    for r in recs:
        for it in r["itens"]:
            e = it.get("valorUnitarioEstimado")
            hs = [x["valorUnitarioHomologado"] for x in (it.get("res") or [])
                  if x.get("valorUnitarioHomologado")]
            for x in (it.get("res") or []):
                if x.get("niFornecedor"):
                    wins.update([(x["niFornecedor"], x.get("nomeRazaoSocialFornecedor"))])
            if e and hs and e > 0:
                by_mod.setdefault(r.get("modalidade"), []).append(min(hs) / e)
    for mod, rs in sorted(by_mod.items(), key=lambda x: -len(x[1])):
        if len(rs) < 5:
            continue
        rs.sort()
        print(f"  {str(mod):22} n={len(rs):>4}  clearing: p25 {rs[len(rs)//4]:.0%} "
              f"MEDIAN {st.median(rs):.0%}  p75 {rs[3*len(rs)//4]:.0%}  "
              f"· exatamente 100%: {sum(1 for x in rs if abs(x-1)<1e-9)/len(rs):.0%}")
    tot = sum(wins.values())
    if tot:
        shares = [(c / tot) ** 2 for c in wins.values()]
        print(f"  fornecedores distintos: {len(wins)} · linhas ganhas: {tot} · "
              f"HHI {sum(shares)*10000:,.0f} · com 1 só contrato: "
              f"{sum(1 for c in wins.values() if c==1)/len(wins):.0%}")
        for (cnpj, nome), c in wins.most_common(3):
            print(f"      {(nome or '?')[:42]:44} x{c}")


if __name__ == "__main__":
    for name in (sys.argv[1:] or list(NICHES)):
        qs, keep = NICHES[name]
        kept, recs = run(name, qs, keep)
        analyse(name, kept, recs)
    print("\nHTTP:", STATS)
