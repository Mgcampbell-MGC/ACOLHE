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
# VERIFIED 2026-09-21: there is NO server-side row cap. An earlier reading of
# this file's own log concluded PNCP capped every query at 600 rows -- it does
# not; 600 was THIS CONSTANT (12 x 50). Page 40 of "kit natalidade" returns a
# full 50 rows against a reported total of 2.777. What IS true: the ordering is
# by relevance, not by date (pages 1 and 40 both span 2024-2026), so a truncated
# pull is a relevance-ranked SAMPLE and its year distribution is an artefact
# that must never be read as a trend.
MAX_PAGES = 60          # 50 per page; the largest query reports ~2.777 rows
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
            if d is None:
                # A transient failure used to end the whole query here, silently
                # truncating it. Skip the page, record it, and keep going.
                continue
            if not d.get("items"):
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
