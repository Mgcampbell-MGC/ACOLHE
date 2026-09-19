"""Harvest a VTEX storefront's public catalogue into JSONL.

Used for Step 0 (closing the cost table). VTEX exposes prices on
/api/catalog_system/pub/products/search with no login, so every row here is an
observed catalogue price, not a derived or inferred one.

Every response is cached to disk keyed by URL: a re-run costs zero network
calls. Same discipline the PNCP client needs in Step 1.
"""

import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
CACHE = os.environ.get("ACOLHE_CACHE", "/tmp/acolhe-cache")
PAGE = 50


def fetch(url, ttl_days=7):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path) and (time.time() - os.path.getmtime(path)) < ttl_days * 86400:
        with open(path) as fh:
            return json.load(fh)

    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as resp:
                body = resp.read().decode("utf-8", "replace")
            data = json.loads(body)
            with open(path, "w") as fh:
                json.dump(data, fh)
            return data
        except Exception as exc:  # noqa: BLE001 - every failure is worth retrying
            last = exc
            time.sleep(2 ** attempt)
    print(f"  FAIL {url} :: {last}", file=sys.stderr)
    return None


def rows_from(product, host):
    """Flatten a VTEX product into one row per SKU, with the price as offered."""
    out = []
    for item in product.get("items", []):
        for seller in item.get("sellers", []):
            offer = seller.get("commertialOffer", {}) or {}
            price = offer.get("Price")
            if price in (None, 0):
                continue
            out.append(
                {
                    "supplier_host": host,
                    "product_name": product.get("productName"),
                    "sku_name": item.get("name"),
                    "brand": product.get("brand"),
                    "ref": product.get("productReference") or item.get("referenceId"),
                    "categories": product.get("categories", []),
                    "price": price,
                    "list_price": offer.get("ListPrice"),
                    "available": offer.get("AvailableQuantity"),
                    "url": product.get("link"),
                    "description": (product.get("description") or "")[:600],
                }
            )
    return out


def sweep(host, fq, label, cap=600):
    """Page through one VTEX query, newest offset first, until it runs dry."""
    seen, rows = set(), []
    for start in range(0, cap, PAGE):
        url = (
            f"https://{host}/api/catalog_system/pub/products/search"
            f"?{fq}&_from={start}&_to={start + PAGE - 1}"
        )
        batch = fetch(url)
        if not batch:
            break
        for product in batch:
            pid = product.get("productId")
            if pid in seen:
                continue
            seen.add(pid)
            for row in rows_from(product, host):
                row["query"] = label
                rows.append(row)
        if len(batch) < PAGE:
            break
    return rows


def main():
    host = sys.argv[1]
    spec_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(spec_path) as fh:
        queries = json.load(fh)

    everything = []
    for label, fq in queries.items():
        got = sweep(host, fq, label)
        print(f"{label:28s} {len(got):5d} rows")
        everything.extend(got)

    with open(out_path, "w") as fh:
        for row in everything:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"\n{len(everything)} rows -> {out_path}")


if __name__ == "__main__":
    main()
