"""The daily workbook. The ONLY thing she is expected to open.

DESIGN PRINCIPLE, and everything else follows from it:

    The file she works in must be the same file that becomes the bid log.

A system that emits a read-only report and separately asks her to maintain a
record gets no record. And the bid log is the only asset here that compounds,
because PNCP publishes who won and never who lost -- so her own history is the
one dataset nobody can buy.

FILE OWNERSHIP is therefore strict, and it is what stops the machine eating
her work:

    HOJE / PIPELINE / SAUDE   system writes, she reads.   Rebuilt every day.
    MINHAS APOSTAS            SHE writes.                 The machine reads
                              her columns back and re-applies them on every
                              rebuild, keyed by the PNCP number. It never
                              invents, edits or deletes a value she typed.

Two more rules that are not negotiable:

  * The workbook is in PORTUGUESE. She is a native speaker and not a
    developer. The code and the repo stay in English so they can be diffed
    and reasoned about; her interface is in her language.
  * Nothing is ever silently absent. A tender the machine could not price, a
    buyer it could not screen and a harvest that came up short each get a
    visible row saying so. A blank cell must never be readable as "fine".
"""

import datetime
import os
import shutil

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

# ACOLHE brand, so the thing she opens every morning looks like her company.
TEAL = "1F4E4A"
TERRACOTTA = "C96F4A"
CREAM = "F7F3EC"
SAGE = "8FA89B"
CHARCOAL = "2B2B2B"

HEADER = Font(bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill("solid", fgColor=TEAL)
WARN_FILL = PatternFill("solid", fgColor="FFE2D6")
HERS_FILL = PatternFill("solid", fgColor="FFF6CC")
GOOD_FILL = PatternFill("solid", fgColor="E3EFE6")

# The columns SHE owns. The machine reads these back and never writes them.
HER_COLUMNS = [
    "Eu licitei?",
    "Meu lance (R$)",
    "Resultado",
    "Preço vencedor (R$)",
    "Nº de concorrentes",
    "Minhas anotações",
]

SHEET_TODAY = "HOJE"
SHEET_PIPELINE = "PIPELINE"
SHEET_BIDS = "MINHAS APOSTAS"
SHEET_HEALTH = "SAUDE DO SISTEMA"


def _style_header(ws, ncols):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = HEADER
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 30


def _autosize(ws, widths):
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = width


def days_left(encerramento, today=None):
    """Working days are what matter, but calendar days are what she reads."""
    if not encerramento:
        return None
    try:
        end = datetime.datetime.fromisoformat(str(encerramento)[:19]).date()
    except ValueError:
        return None
    return (end - (today or datetime.date.today())).days


def read_back_her_columns(path):
    """Everything she typed, keyed by PNCP number. Survives every rebuild."""
    if not os.path.exists(path):
        return {}
    try:
        wb = load_workbook(path, data_only=True)
    except Exception:            # a corrupt or open file must not lose data
        return {}
    if SHEET_BIDS not in wb.sheetnames:
        return {}

    ws = wb[SHEET_BIDS]
    headers = [c.value for c in ws[1]]
    if "Nº PNCP" not in headers:
        return {}
    key_at = headers.index("Nº PNCP")

    kept = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or key_at >= len(row) or not row[key_at]:
            continue
        mine = {}
        for column in HER_COLUMNS:
            if column in headers:
                at = headers.index(column)
                if at < len(row) and row[at] not in (None, ""):
                    mine[column] = row[at]
        if mine:
            kept[str(row[key_at])] = mine
    return kept


def _decision(candidate):
    """What she should do, and why, in one readable line.

    An unknown is reported as an unknown. 'VERIFICAR' is a real outcome and
    must never be quietly rendered as 'NAO LICITAR' -- a tender dropped for a
    reason nobody stated is a tender silently lost.
    """
    rules = candidate.get("rule_results") or {}
    failed = [r for r in rules.values() if not r.get("passed") and not r.get("is_flag")]
    if failed:
        return "NAO LICITAR", failed[0].get("reason", "regra reprovada")

    if candidate.get("suggested_bid"):
        return "LICITAR", candidate.get("bid_rationale", "")

    if candidate.get("price_blocked"):
        return "VERIFICAR", candidate["price_blocked"]

    return "VERIFICAR", "sem dados de itens - o PNCP nao entregou a lista"


def build(path, candidates, health=None, today=None, stale=(), near_misses=()):
    """Write the workbook, preserving everything she has typed."""
    today = today or datetime.date.today()
    hers = read_back_her_columns(path)

    if os.path.exists(path):                     # never destroy a prior day
        backup_dir = os.path.join(os.path.dirname(path) or ".", "arquivo")
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy2(path, os.path.join(
            backup_dir, f"{today.isoformat()}_{os.path.basename(path)}"))

    wb = Workbook()

    # ---------------------------------------------------------------- HOJE
    ws = wb.active
    ws.title = SHEET_TODAY
    cols = ["Município", "UF", "O que estão comprando", "Valor estimado (R$)",
            "Fecha em", "Dias restantes", "DECISÃO", "Por quê",
            "Lance sugerido (R$)", "Margem", "O comprador paga?", "Link PNCP"]
    ws.append(cols)
    _style_header(ws, len(cols))

    ordered = sorted(candidates,
                     key=lambda c: (days_left(c.get("encerramento"), today)
                                    if days_left(c.get("encerramento"), today) is not None
                                    else 999))
    for c in ordered:
        left = days_left(c.get("encerramento"), today)
        decision, why = _decision(c)
        ws.append([
            c.get("municipio"), c.get("uf"), c.get("objeto"),
            c.get("valor_estimado"),
            (str(c.get("encerramento")) or "")[:10] or "não informado",
            left if left is not None else "não informado",
            decision, why,
            c.get("suggested_bid") or "—",
            f"{c['gross_pct']:.0f}%" if c.get("gross_pct") is not None else "—",
            c.get("buyer_verdict") or "NÃO VERIFICÁVEL",
            f"https://pncp.gov.br/app/editais/{(c.get('pncp_key') or '').replace('-', '/')}",
        ])
        row = ws.max_row
        if decision == "LICITAR":
            ws.cell(row=row, column=7).fill = GOOD_FILL
        elif decision == "VERIFICAR":
            ws.cell(row=row, column=7).fill = WARN_FILL
        if left is not None and left <= 5:
            ws.cell(row=row, column=6).fill = WARN_FILL
            ws.cell(row=row, column=6).font = Font(bold=True, color="C0392B")
    _autosize(ws, [22, 5, 58, 18, 12, 14, 14, 52, 18, 10, 20, 46])

    # ------------------------------------------------------------ PIPELINE
    ws = wb.create_sheet(SHEET_PIPELINE)
    cols = ["Fecha em", "Dias restantes", "Município", "UF",
            "O que estão comprando", "Valor estimado (R$)", "DECISÃO", "Nº PNCP"]
    ws.append(cols)
    _style_header(ws, len(cols))
    live = [c for c in ordered
            if days_left(c.get("encerramento"), today) is None
            or days_left(c.get("encerramento"), today) >= 0]
    for c in live:
        left = days_left(c.get("encerramento"), today)
        ws.append([(str(c.get("encerramento")) or "")[:10], left,
                   c.get("municipio"), c.get("uf"), c.get("objeto"),
                   c.get("valor_estimado"), _decision(c)[0], c.get("pncp_key")])
    _autosize(ws, [12, 14, 22, 5, 58, 18, 14, 30])

    # ------------------------------------------------------- MINHAS APOSTAS
    ws = wb.create_sheet(SHEET_BIDS)
    cols = (["Data", "Nº PNCP", "Município", "UF", "O que era",
             "Quantidade", "Meu custo (R$)", "Lance sugerido (R$)"] + HER_COLUMNS)
    ws.append(cols)
    _style_header(ws, len(cols))
    ws.cell(row=1, column=9).comment = None
    for c in ordered:
        key = str(c.get("pncp_key") or "")
        mine = hers.get(key, {})
        ws.append([
            today.isoformat(), key, c.get("municipio"), c.get("uf"),
            c.get("objeto"), c.get("quantidade"), c.get("unit_cost"),
            c.get("suggested_bid"),
        ] + [mine.get(col, "") for col in HER_COLUMNS])
        for offset in range(len(HER_COLUMNS)):
            ws.cell(row=ws.max_row, column=9 + offset).fill = HERS_FILL
    for offset in range(len(HER_COLUMNS)):
        ws.cell(row=1, column=9 + offset).fill = PatternFill("solid", fgColor=TERRACOTTA)
    _autosize(ws, [11, 30, 22, 5, 50, 11, 15, 18, 12, 16, 12, 20, 18, 40])

    # ---------------------------------------------------------------- SAUDE
    ws = wb.create_sheet(SHEET_HEALTH)
    ws.append(["Verificação", "Resultado", "O que isso significa"])
    _style_header(ws, 3)
    for line in _health_rows(health, candidates, stale, near_misses):
        ws.append(line)
        if line[1] in ("FALHOU", "ATENÇÃO"):
            ws.cell(row=ws.max_row, column=2).fill = WARN_FILL
    _autosize(ws, [40, 16, 92])

    tmp = path + ".tmp"
    wb.save(tmp)
    os.replace(tmp, path)        # atomic: she never sees a half-written file
    return path


def _health_rows(health, candidates, stale, near_misses):
    """Never let a silent failure look like a quiet day."""
    rows = []
    if health is None:
        rows.append(["Coleta do PNCP", "ATENÇÃO",
                     "Nenhum relatório de coleta foi gerado. Não é possível "
                     "afirmar que a busca de hoje foi completa."])
        return rows

    complete = getattr(health, "complete", None)
    rows.append([
        "A coleta do dia foi completa?",
        "SIM" if complete else "FALHOU",
        f"{health.rows_total} licitações distintas de {health.total_expected} "
        f"que o PNCP declarou ter." + (
            "" if complete else
            "  ATENÇÃO: a lista de hoje está INCOMPLETA. Não trate este número "
            "como o mercado do dia.")])
    if getattr(health, "route_mixed", False):
        rows.append(["Rota alternativa usada", "ATENÇÃO",
                     "Parte do dia veio de outra rota do PNCP, que ordena e "
                     "data os registros de forma diferente. A cobertura é "
                     "desconhecida."])
    rows.append(["Licitações de kit encontradas", str(len(candidates)),
                 "Somente por texto do objeto. Cerca de 1 em cada 4 licitações "
                 "de kit não se descreve como tal e só aparece descendo à "
                 "lista de itens (API Família B do PNCP)."])
    if stale:
        rows.append(["Descartadas por estarem fora do prazo", str(len(stale)),
                     "Licitações antigas ou já encerradas que entraram por uma "
                     "rota alternativa. Foram removidas de propósito."])
    if near_misses:
        rows.append(["Descartadas por serem de outro programa", str(len(near_misses)),
                     "Ex.: kit escolar, enxoval hospitalar. Não é o nosso mercado."])
    return rows
