"""The descent: read each candidate tender's ITEM LIST and classify it.

This is the reading rail. The daily scanner finds tenders by their object
text and runs at ~75% recall by construction, because roughly one kit tender
in four describes itself generically. Only the item list says what a
municipio is actually buying -- CATMAT is null at municipal level, so
`descricao` on each item is the whole signal.

Item detail exists ONLY on PNCP Family B (api/pncp/v1). Family A has no item
endpoint at all, confirmed against its live OpenAPI document. Family B has
returned 503 on every attempt on 2026-09-19, so this module was written and
tested against a stubbed client and has never seen a real Family B 200.

FIELD NAMES ARE THEREFORE UNVERIFIED. The handoff names `numeroItem`,
`descricao`, `quantidade`, `valorUnitarioEstimado` and a unit field; each is
read defensively with fallbacks, and the raw row is kept on every record so
the mapping can be audited the day Family B answers. When it does, run one
real descent, fix the mapping if needed, and delete this paragraph.

THE ONE RULE: an unreachable API and an empty item list mean opposite things.
`items_status` says which. Nothing downstream may treat UNAVAILABLE as [].
"""

import re

from harvest.pncp_client import Unavailable
from parse.normalise import pieces, strip_accents
from parse.spec import classify

_KEY = re.compile(r"^(\d{14})-(\d)-(\d{1,6})/(\d{4})$")

# Read defensively: nobody has seen a real Family B item row today.
_DESC = ("descricao", "descricaoItem", "objetoItem", "descricaoDetalhada")
_UNIT = ("unidadeMedida", "unidade", "siglaUnidade", "unidadeFornecimento")
_QTY = ("quantidade", "quantidadeItem", "qtde")
_PRICE = ("valorUnitarioEstimado", "valorUnitario", "valorEstimado")
_NUM = ("numeroItem", "numero", "item")


def parse_key(pncp_key):
    """'46316600000164-1-000447/2025' -> (cnpj, ano, sequencial). None if malformed."""
    match = _KEY.match(str(pncp_key or "").strip())
    if not match:
        return None
    cnpj, _, sequencial, ano = match.groups()
    return cnpj, int(ano), int(sequencial)


def _first(row, keys, default=None):
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def _rows_of(payload):
    """Family B may answer with a bare list or a paged dict. Accept both."""
    if payload is None:
        return [], None
    if isinstance(payload, list):
        return payload, None
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return data, payload.get("totalPaginas")
        # a dict that is itself a single item row
        if any(k in payload for k in _DESC):
            return [payload], None
    return [], None


def classify_item(row):
    """One item row -> one auditable record. The raw row travels with it."""
    descricao = _first(row, _DESC, "")
    unidade = _first(row, _UNIT)
    quantidade = _first(row, _QTY)
    sku, spec_ok, reason = classify(descricao)
    return {
        "numero": _first(row, _NUM),
        "descricao": " ".join(str(descricao).split())[:240],
        "unidade": unidade,
        "quantidade": quantidade,
        # Filter 2: pack counts live in free text; PNCP items carry no
        # capacity field, so the description is the only place to look.
        "pieces": pieces(quantidade, unidade, None, descricao) if quantidade is not None else None,
        "valor_unitario_estimado": _first(row, _PRICE),
        "sku": sku,
        "spec_ok": bool(spec_ok),
        "reason": reason,
        "raw": row,
    }


def descend_one(client, pncp_key, page_size=50, max_pages=20):
    """Items for one tender, with a status that never lies about why it is empty."""
    parsed = parse_key(pncp_key)
    if parsed is None:
        return {"pncp_key": pncp_key, "items_status": "BAD_KEY", "items": [],
                "error": f"cannot parse PNCP key {pncp_key!r}"}
    cnpj, ano, sequencial = parsed

    items, pagina = [], 1
    while pagina <= max_pages:
        try:
            payload = client.itens(cnpj, ano, sequencial, pagina=pagina,
                                   page_size=page_size)
        except Unavailable as exc:
            # The whole point of this module: an outage is NOT an empty list.
            return {"pncp_key": pncp_key, "items_status": "UNAVAILABLE",
                    "items": items, "pages_read": pagina - 1,
                    "error": str(exc)[:300]}
        rows, total_pages = _rows_of(payload)
        items.extend(classify_item(r) for r in rows if isinstance(r, dict))
        if not rows or len(rows) < page_size:
            break
        if total_pages is not None and pagina >= int(total_pages):
            break
        pagina += 1

    return {"pncp_key": pncp_key,
            "items_status": "OK" if items else "EMPTY",
            "items": items, "pages_read": pagina, "error": None}


def descend(client, candidates, **kw):
    """Descend into every candidate. Returns one record per candidate, in order."""
    out = []
    for cand in candidates:
        rec = descend_one(client, cand.get("pncp_key"), **kw)
        rec["municipio"] = cand.get("municipio")
        rec["uf"] = cand.get("uf")
        out.append(rec)
    return out


def summarise(results):
    """What she and the digest need: how many could be read, and what is in them."""
    by_status = {}
    for r in results:
        by_status[r["items_status"]] = by_status.get(r["items_status"], 0) + 1
    lines = [f"DESCENT: {len(results)} tender(s) -- "
             + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items()))]
    if by_status.get("UNAVAILABLE"):
        lines.append(f"  !! {by_status['UNAVAILABLE']} tender(s) could NOT be read: "
                     f"PNCP Family B unavailable. These are NOT empty kits. Do not "
                     f"price them; report VERIFICAR.")
    for r in results:
        if r["items_status"] != "OK":
            continue
        ok = sum(1 for i in r["items"] if i["spec_ok"])
        refused = [i for i in r["items"] if i["sku"] is None]
        lines.append(f"  {r.get('municipio') or '?'}/{r.get('uf') or '?'}  "
                     f"{len(r['items'])} items, {ok} conforming"
                     + (f", {len(refused)} refused" if refused else ""))
        for i in refused[:2]:
            lines.append(f"      x {i['descricao'][:60]}  <- {i['reason'][:40]}")
    return "\n".join(lines)
