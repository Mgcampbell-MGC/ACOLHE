"""Screen adjacent niches in the same business model, on the criteria the kit
natalidade work actually established.

WHAT THE KIT TAUGHT US, and therefore what to score on:

 1. MECHANISM beats product. Dispensa clears at ~99% of estimate, pregao at
    ~65% (measured, n=52/40). A niche bought mostly by dispensa is worth ~30
    margin points more than the same goods bought by pregao.
 2. FREIGHT KILLS BULK. A parcel to the Northeast costs R$132-188. On a R$380
    kit that is half the price. Value per kilo is not a detail, it is the
    business. The kit natalidade is a bag of air with a 22-litre bathtub in it.
 3. ASSEMBLY IS THE LABOUR CEILING. 17 items into a bag caps her at 240 kits
    per order and forces an unquoted co-packer. A single-SKU product removes
    that constraint completely.
 4. LICENCES EXCLUDE. Medicamentos need AFE, food needs vigilancia sanitaria.
    A one-person ME cannot carry those.

Counts come from /api/search and are FULL TEXT: they over-collect and are a
signal of activity, never a census. Modalidade mix is computed from the rows
actually returned, so it is a sample statistic with its n reported.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pncp_fetch import search  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "market", "niches.json")

# (query, densidade R$/kg, montagem?, licenca?, nota)
NICHES = [
    ("cartucho toner impressora",   "ALTA",  "nenhuma", "nao", "consumo recorrente, todo orgao usa"),
    ("medalhas trofeus",            "ALTA",  "nenhuma", "nao", "eventos escolares e esportivos"),
    ("material de expediente papelaria", "MEDIA", "nenhuma", "nao", "o item mais comprado do Brasil"),
    ("kit escolar material",        "MEDIA", "ALTA",    "nao", "mesmo modelo do enxoval, muito maior"),
    ("uniforme escolar",            "MEDIA", "nenhuma", "nao", "confeccao, spec pesada"),
    ("camisetas personalizadas evento", "MEDIA", "impressao", "nao", "silk, mesma cadeia do brinde"),
    ("equipamento de informatica notebook", "ALTA", "nenhuma", "nao", "spec pesada, concorrido"),
    ("material esportivo bolas",    "BAIXA", "nenhuma", "nao", "volumoso"),
    ("EPI equipamento protecao individual", "MEDIA", "nenhuma", "CA", "exige Certificado de Aprovacao"),
    ("kit higiene pessoal",         "MEDIA", "ALTA",    "nao", "vizinho direto do enxoval"),
    ("cesta basica alimentos",      "BAIXA", "ALTA",    "sim", "pesado, perecivel, vigilancia"),
    ("material de limpeza",         "BAIXA", "nenhuma", "nao", "pesado, margem fina"),
    ("livros didaticos paradidaticos", "ALTA", "nenhuma", "nao", "denso, sem spec ambigua"),
    ("brinquedos pedagogicos",      "BAIXA", "nenhuma", "INMETRO", "certificacao compulsoria"),
    ("colchoes camas abrigo",       "BAIXA", "nenhuma", "nao", "volume puro, frete proibitivo"),
    ("kit dormitorio enxoval cama mesa banho", "MEDIA", "ALTA", "nao", "abrigos e casas de acolhimento"),
    ("material odontologico escova dental", "MEDIA", "ALTA", "ANVISA", "saude bucal escolar"),
    ("fardamento guarda municipal", "MEDIA", "nenhuma", "nao", "nicho pequeno e fiel"),
    ("bandeiras faixas placas",     "MEDIA", "impressao", "nao", "pequeno, recorrente"),
    ("kit maternidade gestante",    "MEDIA", "ALTA",    "nao", "o negocio atual, para comparar"),
]


def main():
    rows = []
    for q, dens, mont, lic, nota in NICHES:
        d, note = search(q, pagina=1, tam=50)
        items = (d or {}).get("items") or []
        mods = Counter(i.get("modalidade_licitacao_nome") for i in items)
        n = sum(mods.values())
        disp = mods.get("Dispensa", 0)
        rows.append({
            "nicho": q, "total_fulltext": (d or {}).get("total"), "amostra_n": n,
            "dispensa_pct": (disp / n if n else None), "modalidades": dict(mods),
            "densidade": dens, "montagem": mont, "licenca": lic, "nota": nota, "http": note,
        })
        print(f"  {q[:38]:40} total={str((d or {}).get('total')):>6} "
              f"disp={disp:>2}/{n:<2} ({(disp/n if n else 0):>4.0%})  {note}")
    json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=1)

    print("\n" + "=" * 104)
    print(f"{'nicho':40}{'atividade':>10}{'% dispensa':>12}{'densidade':>11}{'montagem':>11}{'licença':>10}")
    print("=" * 104)
    scored = []
    for r in rows:
        if not r["amostra_n"]:
            continue
        # crude, stated openly: mechanism + density + no assembly + no licence
        s = (r["dispensa_pct"] * 40
             + {"ALTA": 30, "MEDIA": 15, "BAIXA": 0}[r["densidade"]]
             + (20 if r["montagem"] == "nenhuma" else 5 if r["montagem"] == "impressao" else 0)
             + (10 if r["licenca"] == "nao" else 0))
        scored.append((s, r))
    for s, r in sorted(scored, reverse=True, key=lambda x: x[0]):
        print(f"{r['nicho'][:38]:40}{r['total_fulltext'] or 0:>10,}{r['dispensa_pct']:>11.0%}"
              f"{r['densidade']:>11}{r['montagem']:>11}{r['licenca']:>10}   score {s:.0f}")


if __name__ == "__main__":
    main()
