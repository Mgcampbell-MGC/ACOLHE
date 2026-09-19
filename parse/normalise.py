"""THE FIVE FILTERS. Nothing that produces an aggregate may bypass this module.

Each function here exists because a specific measurement error was made on this
data. Do not relax one without a failing test that justifies it.

Filter 1  RECENCY        price history endpoints return ~5y silently
Filter 2  PIECES         pack counts live in free text, not in a field
Filter 3  LOT-TOTAL      buyers type the lot total into precoUnitario
Filter 4  SPEC CONTROL   a PDM holds objects at 2-10x different prices
Filter 5  DEDUPE/BUNDLE  shadow rows, adjacent programmes, bundle rows
"""

import re
import unicodedata

# --------------------------------------------------------------------------
# Filter 2 - PIECES
# --------------------------------------------------------------------------

# Written-out counts appear in supplier catalogues ("PAR", "DUPLA") and in
# PNCP unit siglas ("CENTO", "MILHEIRO").
WORD_COUNTS = {
    "UNICA": 1, "UNICO": 1, "UNIDADE": 1, "UM": 1,
    "PAR": 2, "DUPLA": 2, "DOIS": 2, "DUAS": 2,
    "TRES": 3, "QUATRO": 4, "CINCO": 5, "SEIS": 6,
    "OITO": 8, "DEZ": 10, "DUZIA": 12,
    "CENTO": 100, "MILHEIRO": 1000,
}

# Unit siglas as they arrive on PNCP / compras.gov.br item rows.
SIGLA_CAPACITY = {
    "UN": 1, "UND": 1, "UNID": 1, "UNIDADE": 1, "PC": 1, "PEC": 1, "PÇ": 1,
    "KIT": 1, "CJ": 1, "JG": 1, "JOGO": 1, "CONJUNTO": 1, "PAR": 2,
    "C": 100, "CENTO": 100, "CEM": 100,
    "MIL": 1000, "MILHEIRO": 1000, "MLH": 1000,
    # CX / PCT / PACOTE carry no intrinsic count - the count is in the text.
    "CX": None, "CAIXA": None, "PCT": None, "PACOTE": None, "FD": None,
    "FARDO": None, "SC": None, "SACO": None, "DZ": 12, "DUZIA": 12,
}

_NUM_PACK = re.compile(
    r"(?<![\d,.])(\d{1,4})\s*"
    r"(?:X\s*)?"
    r"(?:UNIDADES?|UNID\b|UND\b|UN\b|PE[CÇ]AS?\b|PCS?\b|PARES\b)",
    re.I,
)
_PACK_NUM = re.compile(
    r"(?:C/|COM|KIT|PACK|LEVE|EMBALAGEM\s+COM|CAIXA\s+COM|PACOTE\s+COM)\s*"
    r"(\d{1,4})(?![\d,.%])",
    re.I,
)


def strip_accents(text):
    if text is None:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", str(text))
        if unicodedata.category(c) != "Mn"
    )


def pack_count_from_text(text):
    """Pieces per sold unit, read out of free text. 1 when nothing says otherwise.

    'FRALDA COM BAINHA - 3 UNIDADES'   -> 3
    'BODY COM DECOTE CANOA (2 UNIDADES)' -> 2
    'MEIA ... PAR'                      -> 2
    """
    if not text:
        return 1
    flat = strip_accents(text).upper()

    match = _NUM_PACK.search(flat)
    if match:
        count = int(match.group(1))
        if 1 <= count <= 1000:
            return count

    match = _PACK_NUM.search(flat)
    if match:
        count = int(match.group(1))
        # 'KIT 3' is a pack of three; 'KIT 2024' is a model year.
        if 1 <= count <= 144:
            return count

    for word, count in WORD_COUNTS.items():
        if re.search(rf"\b{word}\b", flat) and count > 1:
            return count

    return 1


def capacity_of(unidade, capacidade_fornecimento=None, descricao=None):
    """Pieces represented by one row's 'quantidade'.

    Order matters: an explicit positive capacity field wins, then the sigla,
    then the free text. capacidadeUnidadeFornecimento is frequently 0.0, which
    must fall through rather than zeroing the row.
    """
    try:
        cap = float(capacidade_fornecimento)
        if cap > 0:
            return cap
    except (TypeError, ValueError):
        pass

    sigla = strip_accents(unidade).upper().strip().rstrip(".")
    if sigla in SIGLA_CAPACITY:
        known = SIGLA_CAPACITY[sigla]
        if known is not None:
            return float(known)
        # CX / PCT / PACOTE - the count is only ever in the description.
        return float(pack_count_from_text(descricao))

    return float(pack_count_from_text(descricao) if descricao else 1)


def pieces(quantidade, unidade=None, capacidade_fornecimento=None, descricao=None):
    """Filter 2. Always use this instead of 'quantidade' directly."""
    try:
        qty = float(quantidade)
    except (TypeError, ValueError):
        return 0.0
    return qty * capacity_of(unidade, capacidade_fornecimento, descricao)


def unit_price_per_piece(total_or_unit_price, quantidade, unidade=None,
                         capacidade_fornecimento=None, descricao=None):
    """Price for ONE piece, given a price quoted per sold unit."""
    cap = capacity_of(unidade, capacidade_fornecimento, descricao)
    if not cap:
        return None
    try:
        return float(total_or_unit_price) / cap
    except (TypeError, ValueError, ZeroDivisionError):
        return None


# --------------------------------------------------------------------------
# Filter 5 - BUNDLES AND ADJACENT PROGRAMMES
# --------------------------------------------------------------------------

# A row naming two or more garments has a two-garment cost basis and must never
# sit inside a single-component family. This is the BODY +R$1,08M error.
_BUNDLE_JOIN = re.compile(
    r"\b(?:CONJUNTO|CONJ\.?|KIT)\b.{0,80}?"
    r"\b(?:\+|E|COM|CONTENDO|/)\b",
    re.I,
)
_MULTI_GARMENT = re.compile(
    r"\b(BODY|MACACAO|PAGAO|BERMUDA|BLUSA|CAMISETA|JARDINEIRA|VESTIDO|"
    r"SHORTS?|(?P<calca>CALCA|CULOTE|MIJAO|SARUEL))\b",
    re.I,
)
_KIT_CONTENTS = re.compile(r"\bCONTENDO\b|\bCOMPOSTO\s+(?:DE|POR)\b", re.I)

# 'CONTENDO' alone does NOT make a bundle. Measured on a real edital:
#   '600 KITS CONTENDO: Banheira, Mamadeira, Fralda...'  -> a bundle
#   'Lenco umedecido, contendo 48 lencos no pc'          -> a PACK COUNT
#   'Luva para bebe, contendo 01 par de luva'            -> a PACK COUNT
# Treating the latter two as bundles silently drops real lines from a harvest.
# A count plus a GENERIC noun names a kit without listing it:
# 'COMPOSTO POR 17 ITENS', 'KIT DE BANHO 3 PECAS'.
_GENERIC_CONTENTS = re.compile(
    r"\d{1,3}\s*(?:ITENS?|ITEM|PE[CÇ]AS?|PRODUTOS?|VOLUMES?|ARTIGOS?)\b", re.I
)
# Articles that can appear in a kit. Two or more distinct ones after a
# CONTENDO/COMPOSTO marker is what actually makes a bundle.
_ARTICLES = re.compile(
    r"\b(BANHEIRA|MAMADEIRA|FRALDA|BODY|MACACAO|PAGAO|TOALHA|CUEIRO|MANTA|"
    r"COBERTOR|MEIA|LUVA|TOUCA|SABONETE|SHAMPOO|TALCO|OLEO|PENTE|ESCOVA|"
    r"SABONETEIRA|MOCHILA|BOLSA|LENCO|CALCA|MIJAO|CHUPETA|PANO)\b",
    re.I,
)


def is_bundle(descricao):
    """True when a row prices more than one distinct garment/article.

    'CONJUNTO BODY + BERMUDA'          -> True  (two garments)
    '600 KITS CONTENDO: Banheira...'   -> True  (a whole kit inside a component family)
    'BODY MANGA LONGA CANELADO'        -> False
    """
    if not descricao:
        return False
    flat = strip_accents(descricao).upper()

    marker = _KIT_CONTENTS.search(flat)
    if marker:
        tail = flat[marker.end():]
        distinct_after = {m.group(1).upper() for m in _ARTICLES.finditer(tail)}
        # Two or more distinct articles after the marker: a real kit.
        if len(distinct_after) >= 2:
            return True
        # A count followed by a GENERIC container noun -- '17 ITENS',
        # '3 PECAS' -- is a kit whose contents simply are not enumerated here.
        if _GENERIC_CONTENTS.search(tail):
            return True
        # A count followed by a SPECIFIC article -- 'contendo 48 lencos',
        # 'contendo 01 par de luva' -- is a PACK COUNT, not a kit. Falling
        # through here is the whole point: it must stay classifiable.

    distinct = {
        ("CALCA" if m.group("calca") else m.group(1)).upper()
        for m in _MULTI_GARMENT.finditer(flat)
    }
    if len(distinct) >= 2:
        return True

    # 'CONJUNTO ... 3 PEÇAS' is a bundle even when only one garment is named.
    if re.search(r"\bCONJUNTO\b", flat) and _MULTI_GARMENT.search(flat):
        return True

    return False


def is_shadow_row(quantidade, valor_unitario):
    """Filter 5. Duplicate shadow rows carry qt=0 and vu=0 against a real total."""
    try:
        return float(quantidade) == 0 and float(valor_unitario) == 0
    except (TypeError, ValueError):
        return False


# --------------------------------------------------------------------------
# Filter 3 - LOT-TOTAL ROWS
# --------------------------------------------------------------------------

def in_plausible_window(unit_price, window):
    """Filter 3. window is (lo, hi) from config/skus.yaml, in R$ per piece."""
    if unit_price is None or not window:
        return False
    lo, hi = window
    try:
        return float(lo) <= float(unit_price) <= float(hi)
    except (TypeError, ValueError):
        return False
