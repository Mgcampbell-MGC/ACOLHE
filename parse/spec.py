"""SKU classification with spec control -- Filter 4.

A catalogue heading (PDM) holds materially different objects at 2-10x
different prices. Classifying by keyword alone and taking a median across the
result manufactures a margin out of nothing. Three worked failures:

  BANHEIRA  priced at a 17,2 L tub against a market whose live band is
            20-25 L. 36 margin points of fiction.
  CADERNO   a 96-page brochura priced against a PDM topped by an
            R$11.126 leather binder. +23-28% became +4,2%.
  APONTADOR a 'simples' priced against a PDM that is 78% 'com deposito'.
            R$3,0M of apparent market was really R$77.492.

So classification returns three things, never just a label: the SKU, whether
the row actually CONFORMS to our product on the spec dimensions that move
price, and -- when it does not -- why it was dropped. A row that cannot be
spec-checked is not silently treated as conforming.
"""

import os
import re

import yaml

from parse.normalise import is_bundle, strip_accents

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "skus.yaml"
)

# Sellers write capacity as '24 LITROS', '22 Lts', '20L', '17,2 L'. An earlier
# version matched only 'L' with a word boundary, which silently dropped both
# 'LITROS' and 'Lts' -- and dropping a stated capacity looks exactly like an
# unstated one, so the error is invisible.
_CAPACITY_L = re.compile(r"(\d{1,3})(?:[,.](\d))?\s*(?:LITROS?|LTS?|L)\b", re.I)

# Guards against eating '0-6 MESES', '30 KG' or a product code.
_CAPACITY_SANE = (5.0, 60.0)
_VOLUME_ML = re.compile(r"(\d{2,4})\s*ML\b", re.I)
_SIZE_CM = re.compile(r"(\d{2,3})\s*[X]\s*(\d{2,3})\s*(?:CM)?", re.I)


class Classifier:
    """Classify an item description to a SKU, with spec control.

    Deliberately never looks at catalogoCodigoItem / CATMAT. That field is
    null on municipal tenders, and the kit market is 97% municipal, so a
    classifier that needs it classifies nothing where the money is.
    """

    def __init__(self, config_path=None):
        with open(config_path or _CONFIG_PATH) as fh:
            cfg = yaml.safe_load(fh)
        self.skus = cfg["skus"]
        self.excluded = cfg.get("excluded", {})
        defaults = cfg.get("defaults", {})
        self.global_anti = [re.compile(p, re.I) for p in defaults.get("global_anti", [])]
        self.programme_anti = [
            re.compile(p, re.I) for p in defaults.get("programme_anti", [])
        ]
        self._compiled = {
            name: {
                "match": [re.compile(p, re.I) for p in body.get("match", [])],
                "anti": [re.compile(p, re.I) for p in body.get("anti", [])],
            }
            for name, body in self.skus.items()
        }
        self._excl = {
            name: [re.compile(p, re.I) for p in body.get("match", [])]
            for name, body in self.excluded.items()
        }

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def capacity_litres(text):
        """Litres stated by the seller. None when unstated -- never inferred."""
        flat = strip_accents(text or "").upper()
        for match in _CAPACITY_L.finditer(flat):
            whole, frac = match.group(1), match.group(2)
            litres = float(f"{whole}.{frac}") if frac else float(whole)
            lo, hi = _CAPACITY_SANE
            if lo <= litres <= hi:
                return litres
        return None

    @staticmethod
    def volume_ml(text):
        match = _VOLUME_ML.search(strip_accents(text or "").upper())
        return float(match.group(1)) if match else None

    def is_excluded_sku(self, text):
        """Mamadeiras and chupetas are Inmetro-certified. Never bid them."""
        flat = strip_accents(text or "").upper()
        for name, pats in self._excl.items():
            if any(p.search(flat) for p in pats):
                return name
        return None

    def is_adjacent_programme(self, text):
        """Trap 6. A school-uniform programme once added R$155,7M to a kit harvest."""
        flat = strip_accents(text or "").upper()
        for pat in self.programme_anti:
            if pat.search(flat):
                return pat.pattern
        return None

    # -- the classifier ----------------------------------------------------

    def classify(self, descricao, require_spec=True):
        """Return (sku, spec_ok, reason).

        sku      the family, or None when nothing matched or the row is out
        spec_ok  True only when the row demonstrably conforms on the spec
                 dimensions that move price. Unknown spec is NOT conforming.
        reason   why it was dropped, or why the spec failed. Human-readable:
                 the founder reads these.
        """
        if not descricao or not str(descricao).strip():
            return None, False, "empty description"

        flat = strip_accents(descricao).upper()

        excluded = self.is_excluded_sku(flat)
        if excluded:
            return None, False, (
                f"excluded SKU {excluded}: "
                f"{self.excluded[excluded]['reason'].strip()}"
            )

        programme = self.is_adjacent_programme(flat)
        if programme:
            return None, False, f"adjacent programme (matched /{programme}/)"

        if is_bundle(flat):
            return None, False, (
                "bundle row: prices more than one distinct article, so its "
                "cost basis is not a single component"
            )

        for pat in self.global_anti:
            if pat.search(flat):
                return None, False, f"global anti-pattern /{pat.pattern}/"

        for name, pats in self._compiled.items():
            if not any(p.search(flat) for p in pats["match"]):
                continue
            hit = next((p.pattern for p in pats["anti"] if p.search(flat)), None)
            if hit:
                return None, False, f"{name} anti-pattern /{hit}/"
            spec_ok, why = self.check_spec(name, flat, require_spec=require_spec)
            return name, spec_ok, why

        return None, False, "no SKU matched"

    def check_spec(self, sku, flat, require_spec=True):
        """Filter 4 proper. Returns (conforms, reason)."""
        spec = (self.skus.get(sku) or {}).get("spec") or {}
        if not spec:
            return True, "no spec dimensions defined for this SKU"

        band = spec.get("capacity_litres")
        if band:
            litres = self.capacity_litres(flat)
            if litres is None:
                if spec.get("capacity_required") and require_spec:
                    return False, (
                        "capacity not stated by the seller, and this SKU is "
                        "priced by capacity band - cannot be assumed"
                    )
                return False, "capacity not stated"
            lo, hi = band
            if not (lo <= litres <= hi):
                return False, (
                    f"capacity {litres:g} L is outside the {lo}-{hi} L band "
                    f"where the tender lines actually are"
                )

        vol = spec.get("volume_ml")
        if vol:
            millilitres = self.volume_ml(flat)
            if millilitres is None:
                return False, "volume not stated"
            lo, hi = vol
            if not (lo <= millilitres <= hi):
                return False, f"volume {millilitres:g} ml outside {lo}-{hi} ml"

        if spec.get("hooded") is False and re.search(r"CAPUZ", flat):
            return False, "hooded towel is a different, dearer product"

        if spec.get("unit_is_pair") and not re.search(r"\bPARES?\b", flat):
            return False, (
                "listing does not say PARES, so pair-vs-sock is ambiguous"
            )

        if spec.get("form") == ["mochila"] and not re.search(r"\bMOCHILA\b", flat):
            return False, "a sacola/bolsa is not a mochila"

        return True, "conforms"


_DEFAULT = None


def classifier():
    """Shared instance. The config is read once."""
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = Classifier()
    return _DEFAULT


def classify(descricao, require_spec=True):
    return classifier().classify(descricao, require_spec=require_spec)
