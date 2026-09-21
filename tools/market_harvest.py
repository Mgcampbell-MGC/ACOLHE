"""Build the real picture of the kit-natalidade market from PNCP.

Two passes, both resumable, both refusing to invent anything:

  PASS 1  /api/search over several phrasings -> every tender that mentions a
          layette kit, with its identifiers, UF, modalidade and tem_resultado.
  PASS 2  for the ones that HAVE a result, /itens and /itens/{n}/resultados ->
          estimated price, homologated price, quantity, and who won.

Written 2026-09-21, the day Family B came back. Family A was down, so
/api/search is the discovery rail; it is full text, so PASS 1 over-collects
on purpose and the filtering happens in analysis, where it can be audited.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pncp_fetch import STATS, arquivos, itens, resultados, search  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "market")
os.makedirs(OUT, exist_ok=True)

QUERIES = ["kit natalidade", "kit enxoval", "enxoval bebe", "kit maternidade",
           "enxoval recem nascido", "kit gestante", "enxoval para bebe"]
MAX_PAGES = 12          # 50 per page
TAM = 50


def pass1():
    path = os.path.join(OUT, "tenders.json")
    found = {}
    if os.path.exists(path):
        found = {r["numero_controle_pncp"]: r for r in json.load(open(path))}
        print(f"resuming with {len(found)} already collected")
    log = []
    for q in QUERIES:
        for page in range(1, MAX_PAGES + 1):
            d, note = search(q, pagina=page, tam=TAM)
            log.append({"q": q, "pagina": page, "note": note,
                        "total": (d or {}).get("total"), "n": len(((d or {}).get("items") or []))})
            print(f"  [{q}] p{page}: {note} total={(d or {}).get('total')} n={len(((d or {}).get('items') or []))}")
            if not d or not d.get("items"):
                break
            for it in d["items"]:
                key = it.get("numero_controle_pncp")
                if key:
                    it["_query"] = q
                    found.setdefault(key, it)
            if len(d["items"]) < TAM:
                break
        json.dump(list(found.values()), open(path, "w"), ensure_ascii=False)
    json.dump(log, open(os.path.join(OUT, "pass1_log.json"), "w"), ensure_ascii=False, indent=1)
    print(f"PASS 1 done: {len(found)} distinct tenders -> {path}")
    return list(found.values())


def pass2(tenders, limit=None):
    path = os.path.join(OUT, "results.json")
    done = {}
    if os.path.exists(path):
        done = {r["key"]: r for r in json.load(open(path))}
        print(f"resuming with {len(done)} already descended")
    todo = [t for t in tenders if t.get("tem_resultado") and t["numero_controle_pncp"] not in done]
    todo.sort(key=lambda t: t.get("data_publicacao_pncp") or "", reverse=True)
    if limit:
        todo = todo[:limit]
    print(f"PASS 2: {len(todo)} tenders with a published result to descend")
    for i, t in enumerate(todo, 1):
        cnpj, ano, seq = t["orgao_cnpj"], t["ano"], t["numero_sequencial"]
        its, note = itens(cnpj, ano, seq)
        rec = {"key": t["numero_controle_pncp"], "cnpj": cnpj, "ano": ano, "seq": seq,
               "municipio": t.get("municipio_nome"), "uf": t.get("uf"),
               "orgao": t.get("orgao_nome"), "modalidade": t.get("modalidade_licitacao_nome"),
               "situacao": t.get("situacao_nome"), "titulo": t.get("title"),
               "objeto": (t.get("description") or "")[:400],
               "publicado": t.get("data_publicacao_pncp"), "itens_note": note, "itens": []}
        for it in (its or []):
            n = it.get("numeroItem")
            row = {k: it.get(k) for k in ("numeroItem", "descricao", "quantidade", "unidadeMedida",
                                          "valorUnitarioEstimado", "valorTotal", "temResultado",
                                          "situacaoCompraItemNome", "criterioJulgamentoNome",
                                          "tipoBeneficioNome")}
            row["descricao"] = (row.get("descricao") or "")[:600]
            if it.get("temResultado"):
                res, rnote = resultados(cnpj, ano, seq, n)
                row["resultados"] = [{k: r.get(k) for k in
                                      ("niFornecedor", "nomeRazaoSocialFornecedor", "porteFornecedorNome",
                                       "quantidadeHomologada", "valorUnitarioHomologado",
                                       "valorTotalHomologado", "dataResultado", "ordemClassificacaoSrp")}
                                     for r in (res or [])]
                row["resultados_note"] = rnote
            rec["itens"].append(row)
        done[rec["key"]] = rec
        if i % 5 == 0 or i == len(todo):
            json.dump(list(done.values()), open(path, "w"), ensure_ascii=False)
            print(f"  {i}/{len(todo)} {rec['municipio']}/{rec['uf']} itens={len(rec['itens'])} {note}")
    json.dump(list(done.values()), open(path, "w"), ensure_ascii=False)
    print(f"PASS 2 done: {len(done)} records -> {path}")
    print("HTTP stats:", STATS)


if __name__ == "__main__":
    t = pass1()
    pass2(t, limit=int(sys.argv[1]) if len(sys.argv) > 1 else None)
