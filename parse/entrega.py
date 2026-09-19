"""Read the edital's LOCAL DE ENTREGA -- the clause that decides the margin.

MEASURED 2026-09-19 (price/freight.py): one parcel per kit to a Northeast
capital costs 37-52% of the kit price; one consolidated LTL shipment to ONE
consignee costs ~15%. So whether the buyer takes the lot at a single
municipal address, at addresses named call-off by call-off, or at the
beneficiaries' homes is worth more than every other clause combined.

Three answers, plus the one that is not an answer:

  ONE_ADDRESS   a named seat (Secretaria, Prefeitura, Fundo, CRAS, sede),
                usually with a street address -> LTL is possible
  CALLOFF       "nos locais determinados pelo departamento solicitante",
                "local indicado pela Administracao", "ou em outro endereco
                designado" -> addresses arrive with each ordem de
                fornecimento; she cannot price a lane she does not know
  HOUSEHOLD     domicilio / residencia das beneficiarias / porta a porta
                -> one parcel per kit, unbiddable on cubed goods
  UNKNOWN       no delivery clause found -> VERIFICAR, priced as parcel

Read on the seven real editais (data/editais) -- see tests. Whatever the
clause says, 'parcelado' (delivery per call-off, conforme demanda) means the
shipments are small: LTL is only priced when the lot goes in one go.
"""

import re
from dataclasses import dataclass, field

from parse.normalise import strip_accents

ONE_ADDRESS, CALLOFF, HOUSEHOLD, UNKNOWN = "ONE_ADDRESS", "CALLOFF", "HOUSEHOLD", "UNKNOWN"

_WINDOW = 350
_ENTREG = re.compile(r"\bENTREG(?:A|AS|UE|UES|AR|ANDO)\b")
# windows about these are not about delivering the goods
_NOISE = re.compile(r"\b(AMOSTRAS?|FATURAS?|DOCUMENTA|ENVELOPE|PROPOSTA|CERTID|RECURSO|LANCE|CREDENCIAMENTO)\b")

_SEAT = (r"(?:SEDE D[AO]|SECRETARIA|PREFEITURA|FUNDO MUNICIPAL|ALMOXARIFADO|CRAS|"
         r"CENTRO DE REFERENCIA|SEMTDES|SEMTEPS|SEMAS|DEPARTAMENTO|UNIDADE)")
_ONE = re.compile(
    r"\b(?:ENTREG\w*(?:\s+(?:UNICA|TOTAL|INTEGRAL|DEVERA|SERA|SER|FEITA|REALIZADA|EFETUADA)){0,3}"
    r"\s+(?:N[AO]|A|AO|NAS?\s+DEPENDENCIAS\s+D[AO])|"
    r"ENTREGA\s+D[AO]S\s+(?:BENS|PRODUTOS|MATERIAIS|ITENS|KITS)\b[^.;]{0,60}?,?\s+N[AO]|"
    r"(?:DEVERA\s+)?OCORRER(?:A)?\s+N[AO]|REALIZAD[AO]\s+N[AO]|"
    r"LOCAL\s+DE\s+ENTREGA\s*:?\s*(?:SERA\s+)?N?[AO]?)\s+" + _SEAT)
# "no local indicado NO TERMO DE REFERENCIA" is a cross-reference, not a call-off
_XREF = re.compile(r"^\s*(?:TERMO|EDITAL|ANEXO|ITEM|SUBITEM|PRESENTE)\b")
# "para serem entregues AS GESTANTES ATENDIDAS PELO CRAS" is the purpose of
# the purchase, not the supplier's delivery obligation
_PURPOSE = re.compile(r"^[^.;]{0,60}?\b(?:ATENDID|ACOMPANHAD|PEL[AO]\s+(?:CRAS|CENTRO\s+DE\s+REFERENCIA|EQUIPE))")
_STREET = re.compile(
    r"\b(?:RUA|AV\.?|AVENIDA|TRAVESSA|PRACA|RODOVIA|ESTRADA)\b[\s\S]{3,90}?\bN[O.º°]?\s*\.?\s*\d{1,5}\b")
# the delivery chapter itself outranks every incidental mention elsewhere
_HEADING = re.compile(r"LOCA(?:L|IS)\s+DE\s+(?:EXECUCAO\s+OU\s+)?ENTREGA|PRAZOS?\s+E\s+(?:DO\s+)?LOCA(?:L|IS)|LOCAL\s+E\s+PRAZO")

_CALLOFF = [
    r"LOCA(?:L|IS)\s+(?:DE\s+ENTREGA\s+)?(?:INDICAD|DETERMINAD|DESIGNAD|DEFINID|ESTABELECID)\w*\s+(?:PEL|N)[AO]S?\b",
    r"LOCAL\s+(?:AINDA\s+)?A\s+SER\s+(?:DETERMINAD|DEFINID|INDICAD)",
    r"OUTRO\s+ENDERECO\s+(?:DESIGNAD|INDICAD|DETERMINAD)",
    r"LOCAIS\s+DE\s+ENTREGA\s*[,;:]?\s*(?:ACOMPANHAD|CORRENDO|SEM)",
    r"CONSTAR\w*\s+(?:AS\s+QUANTIDADES\s+E\s+)?OS?\s+LOCA(?:L|IS)\s+DE\s+ENTREGA",
    r"LOCAIS\s+INDICADOS\s+NA\s+(?:RESPECTIVA\s+)?ORDEM",
    r"CONFORME\s+(?:INDICAD|SOLICITAD)\w*\s+(?:PEL[AO]|N[AO])\s+(?:SECRETARIA|ADMINISTRACAO|SETOR|DEPARTAMENTO)",
]
_HOUSEHOLD = [
    r"\bDOMICILIAR\b|ENTREG\w*\s+(?:EM|A|NO)\s+DOMICILIO|\bDOMICILIOS?\s+D[AO]S?\s+(?:BENEFICI|GESTANT|FAMILI|USUARI|PUERPER)",
    r"\bRESIDENCIAS?\s+D[AO]S?\s+(?:BENEFICI|GESTANT|FAMILI|USUARI|PUERPER|MAES?\b)",
    r"\bENDERECOS?\s+D[AO]S?\s+(?:BENEFICI|GESTANT|FAMILI|USUARI|PUERPER|MAES?\b)",
    r"\bPORTA\s+A\s+PORTA\b",
    r"\bENTREG\w*\s+(?:DIRETAMENTE\s+)?(?:AS|AOS|PARA\s+AS|PARA\s+OS|NAS\s+CASAS\s+D[AO]S)\s+(?:FAMILIAS|GESTANTES|BENEFICIARI|PUERPERAS|USUARI)",
]
_PARCELADO = [r"FORMA\s+PARCELADA", r"\bPARCELADAMENTE\b", r"\bPARCELAD[AO]S?\b",
              r"CONFORME\s+(?:A\s+)?(?:DEMANDA|NECESSIDADE)", r"DE\s+ACORDO\s+COM\s+(?:A\s+)?(?:DEMANDA|NECESSIDADE|AS\s+SOLICITACOES)"]


@dataclass
class Delivery:
    mode: str
    reason: str
    parcelado: bool
    evidence: dict = field(default_factory=dict)

    @property
    def freight_mode(self):
        """What price/freight.estimate() should be asked for."""
        if self.mode == ONE_ADDRESS and not self.parcelado:
            return "ltl"
        return "parcel"


def _windows(flat):
    out, last_end = [], -1
    for m in _ENTREG.finditer(flat):
        a, b = max(0, m.start() - _WINDOW), min(len(flat), m.end() + _WINDOW)
        if a < last_end:              # merge overlapping windows
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
        last_end = b
    return [flat[a:b] for a, b in out if not _NOISE.search(flat[a:b][:_WINDOW])]


def _first(patterns, text, reject=None):
    """First pattern hit whose tail is not rejected (a cross-reference, a
    statement of purpose). Returns the matched text or None."""
    for p in patterns:
        for m in re.finditer(p, text):
            if reject is None or not reject.search(text[m.end():m.end() + 100]):
                return m.group(0)
    return None


def classify_delivery(edital_text):
    """Delivery(mode, reason, parcelado, evidence) from the edital / TR text."""
    flat = re.sub(r"[ \t]+", " ", strip_accents(edital_text or "").upper())
    if not flat.strip():
        return Delivery(UNKNOWN, "VERIFICAR: sem texto do edital -- frete cotado como encomenda", False)

    parcelado = _first(_PARCELADO, flat)
    windows = _windows(flat)
    house = one = calloff = street = None
    seat_and_calloff = False        # the SAME clause names a seat and leaves the door open
    boilerplate = None              # "local indicado pela Administracao" far from the seat
    # a window under the delivery heading is read first and alone
    headed = [w for w in windows if _HEADING.search(w)]
    for w in headed + [w for w in windows if w not in headed]:
        # domicilio / residencia / porta a porta are unambiguous; "entregues
        # as gestantes" only counts when it is not the purpose of the purchase
        house = house or _first(_HOUSEHOLD[:-1], w) or _first(_HOUSEHOLD[-1:], w, reject=_PURPOSE)
        c = _first(_CALLOFF, w, reject=_XREF)
        m = _ONE.search(w)
        if m and c:
            seat_and_calloff = True
        if m and not one:
            one = m.group(0)
        if m and not street:
            s = _STREET.search(w[m.start():m.start() + 260])
            street = s.group(0).strip() if s else None
        if headed and w in headed and (m or c):
            if c:
                calloff = c
            break                       # the chapter answered; stop reading
        if c:
            if m or not one:
                calloff = calloff or c
            else:
                boilerplate = boilerplate or c
    ev = {"windows": len(windows), "seat": one, "street": street, "calloff": calloff,
          "household": house, "parcelado": parcelado, "boilerplate": boilerplate}
    par = bool(parcelado)

    if house:
        return Delivery(HOUSEHOLD, f"entrega nas residencias ({house.strip()!r}): uma encomenda por kit -- "
                        "37-52% do preco em frete; NAO LICITAR sem frete medido ao CEP", par, ev)
    if calloff and (seat_and_calloff or not one):
        why = ("enderecos chegam com cada ordem de fornecimento"
               f" ({calloff.strip()!r})")
        if one:
            why += f"; sede nomeada ({one.strip()!r}) mas nao e' a unica"
        return Delivery(CALLOFF, f"VERIFICAR: {why} -- frete cotado como encomenda ate' saber o lote por pedido", par, ev)
    if one:
        why = f"um consignatario: {one.strip()!r}" + (f", {street!r}" if street else ", sem logradouro no texto")
        if boilerplate or calloff:
            why += f" (clausula generica noutro ponto: {(boilerplate or calloff).strip()!r})"
        if par:
            why += " -- mas fornecimento PARCELADO: lotes por pedido pequenos, frete como encomenda"
        else:
            why += " -- lote unico: LTL consolidado e' possivel"
        return Delivery(ONE_ADDRESS, why, par, ev)
    return Delivery(UNKNOWN, "VERIFICAR: nenhuma clausula de local de entrega encontrada -- "
                    "frete cotado como encomenda", par, ev)
