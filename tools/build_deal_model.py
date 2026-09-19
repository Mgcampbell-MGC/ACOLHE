"""Build docs/ACOLHE_deal_model.xlsx -- a hand-driven per-deal model.

Every number she can change is blue on yellow. Everything else is a formula.
Defaults come from the repo's measured tables (data/cost_table.csv,
data/cost_freight.csv, price/margin.py, config/capital.yaml).
"""
import csv
import os
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "ACOLHE_deal_model.xlsx")

F = "Arial"
BLUE = Font(name=F, color="0000FF", size=10)
BLACK = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
GREEN = Font(name=F, color="008000", size=10)
H1 = Font(name=F, size=14, bold=True)
H2 = Font(name=F, size=11, bold=True, color="FFFFFF")
YELLOW = PatternFill("solid", fgColor="FFFF00")
DARK = PatternFill("solid", fgColor="1F3864")
GREY = PatternFill("solid", fgColor="F2F2F2")
BRL = '"R$" #,##0.00;("R$" #,##0.00);-'
PCT = '0.0%'
INT = '#,##0'
thin = Side(style="thin", color="BFBFBF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)

wb = Workbook()

# ---------------------------------------------------------------- BOM sheet
bom = wb.active
bom.title = "BOM"
bom["A1"] = "Goods cost per kit -- from data/cost_table.csv (observed SP wholesale, 2026-09-19)"
bom["A1"].font = H1
bom["A2"] = "Blue cells are editable: change a unit cost or a quantity per kit and the DEAL sheet follows."
bom["A2"].font = BLACK
hdr = ["BOM line", "SKU", "Qty per kit", "Unit cost (R$)", "Line cost (R$)", "Basis", "Supplier UF", "Notes"]
for c, h in enumerate(hdr, 1):
    cell = bom.cell(row=4, column=c, value=h)
    cell.font = H2; cell.fill = DARK; cell.border = BOX
    cell.alignment = Alignment(horizontal="center", wrap_text=True)
with open(os.path.join(ROOT, "data", "cost_table.csv"), encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
r = 5
for row in rows:
    bom.cell(row=r, column=1, value=row["bom_line"]).font = BLACK
    bom.cell(row=r, column=2, value=row["sku"]).font = BLACK
    q = bom.cell(row=r, column=3, value=1); q.font = BLUE; q.fill = YELLOW; q.number_format = INT
    cost = row["cost_per_bom_unit"].strip()
    u = bom.cell(row=r, column=4, value=float(cost) if cost else None)
    u.font = BLUE; u.fill = YELLOW; u.number_format = BRL
    lc = bom.cell(row=r, column=5, value=f"=IF(D{r}=\"\",\"\",C{r}*D{r})")
    lc.font = BLACK; lc.number_format = BRL
    bom.cell(row=r, column=6, value=row["basis"]).font = BLACK
    bom.cell(row=r, column=7, value=row["supplier_uf"]).font = BLACK
    note = ("UNPRICED -- the kit bag; needs the real edital spec (PNCP Family B). "
            "Type an estimate here or in DEAL!C15." if not cost else
            "diaper: pack of 18 at pack price" if row["bom_line"] == "fralda_descartavel_rn" else "")
    bom.cell(row=r, column=8, value=note).font = BLACK
    for c in range(1, 9):
        bom.cell(row=r, column=c).border = BOX
    r += 1
last = r - 1
bom.cell(row=r, column=4, value="TOTAL priced lines").font = BOLD
t = bom.cell(row=r, column=5, value=f"=SUM(E5:E{last})"); t.font = BOLD; t.number_format = BRL; t.border = BOX
bom.cell(row=r + 1, column=4, value="Unpriced lines").font = BOLD
u = bom.cell(row=r + 1, column=5, value=f"=SUMPRODUCT(--(D5:D{last}=\"\"))"); u.font = BOLD; u.number_format = INT
BOM_TOTAL = f"BOM!$E${r}"
BOM_GAPS = f"BOM!$E${r + 1}"
for col, w in zip("ABCDEFGH", (26, 26, 11, 14, 14, 11, 11, 60)):
    bom.column_dimensions[col].width = w
bom.freeze_panes = "A5"

# ------------------------------------------------------------ FREIGHT sheet
fr = wb.create_sheet("FREIGHT")
fr["A1"] = "Freight per kit -- MEASURED 2026-09-19 (data/freight.md, data/cost_freight.csv)"
fr["A1"].font = H1
fr["A2"] = ("Parcel = Correios PAC balcao, one 60x40x40 cm box per kit, SP 03005-000 to the CAPITAL CEP. "
            "LTL = consolidated road freight to ONE consignee; only SP->CE has a published table (STC). "
            "Blank = never measured: the DEAL sheet will say so rather than use zero. Blue cells editable.")
fr["A2"].font = BLACK; fr["A2"].alignment = Alignment(wrap_text=True)
fr.merge_cells("A2:E2"); fr.row_dimensions[2].height = 48
for c, h in enumerate(["UF", "Parcel per kit (R$)", "LTL per kit (R$)", "Transit days (PAC, business)", "Source"], 1):
    cell = fr.cell(row=4, column=c, value=h)
    cell.font = H2; cell.fill = DARK; cell.border = BOX; cell.alignment = Alignment(horizontal="center", wrap_text=True)
parcel = {"BA": (132.90, 6), "PE": (152.60, 6), "CE": (152.60, 7), "PA": (152.60, 8),
          "MA": (188.40, 8), "SE": (188.40, 8), "RN": (188.40, 7), "MG": (116.60, 5)}
ltl = {"CE": 53.99}
ufs = ["MG", "MA", "BA", "CE", "PE", "SE", "PA", "RN", "PB", "AL", "PI", "GO", "TO", "RJ", "PR", "SC", "RS", "AM", "SP"]
r = 5
for uf in ufs:
    fr.cell(row=r, column=1, value=uf).font = BOLD
    p = fr.cell(row=r, column=2, value=parcel.get(uf, (None, None))[0]); p.font = BLUE; p.fill = YELLOW; p.number_format = BRL
    l = fr.cell(row=r, column=3, value=ltl.get(uf)); l.font = BLUE; l.fill = YELLOW; l.number_format = BRL
    d = fr.cell(row=r, column=4, value=parcel.get(uf, (None, None))[1]); d.font = BLUE; d.fill = YELLOW; d.number_format = INT
    src = ("Correios public calculator, measured" if uf in parcel else "NOT MEASURED")
    if uf in ltl:
        src += "; LTL: STC Transportes published table SP->Fortaleza, 100 kits (R$52,57 at 5.000)"
    fr.cell(row=r, column=5, value=src).font = BLACK
    for c in range(1, 6):
        fr.cell(row=r, column=c).border = BOX
    r += 1
FR_LAST = r - 1
for col, w in zip("ABCDE", (8, 20, 18, 22, 70)):
    fr.column_dimensions[col].width = w

# --------------------------------------------------------------- DEAL sheet
d = wb.create_sheet("DEAL", 0)
d.column_dimensions["A"].width = 3
d.column_dimensions["B"].width = 46
d.column_dimensions["C"].width = 18
d.column_dimensions["D"].width = 70
d["B1"] = "ACOLHE -- does this deal pencil?"; d["B1"].font = H1
d["B2"] = "Type in the BLUE cells only. Everything else recalculates. One tender per copy of this file."
d["B2"].font = BLACK

def section(row, title):
    for c in (2, 3, 4):
        cell = d.cell(row=row, column=c); cell.fill = DARK; cell.font = H2
    d.cell(row=row, column=2, value=title)

def inp(row, label, value, fmt=BRL, note=""):
    d.cell(row=row, column=2, value=label).font = BLACK
    c = d.cell(row=row, column=3, value=value); c.font = BLUE; c.fill = YELLOW; c.number_format = fmt; c.border = BOX
    d.cell(row=row, column=4, value=note).font = Font(name=F, size=9, italic=True, color="595959")

def out(row, label, formula, fmt=BRL, note="", bold=False, font=BLACK):
    d.cell(row=row, column=2, value=label).font = BOLD if bold else BLACK
    c = d.cell(row=row, column=3, value=formula); c.font = Font(name=F, size=10, bold=bold, color=font.color); c.number_format = fmt; c.border = BOX
    d.cell(row=row, column=4, value=note).font = Font(name=F, size=9, italic=True, color="595959")

section(4, "1. THE TENDER")
inp(5, "Kits in the lot (quantidade)", 100, INT, "For an SRP use the quantity you expect to be called off, not the ceiling.")
inp(6, "Buyer's estimated price per kit (valor estimado / kit)", 359.05, BRL, "From the edital. R$359,05 was the Itaquaquecetuba 2025 estimate for a 17-item kit.")
inp(7, "My bid as % of the estimate", 0.75, PCT, "75% is the opening anchor in price/margin.py. Per-item lines clear at 97-100%; lote unico at 36-63%.")
inp(8, "Buyer UF", "CE", "@", "Two letters. Drives freight and transit from the FREIGHT sheet.")
inp(9, "Delivery mode: LTL or PARCEL", "LTL", "@", "LTL only when the edital delivers the WHOLE lot to ONE address in one go. 'Parcelado' or addresses per ordem de fornecimento = PARCEL.")
dv = DataValidation(type="list", formula1='"LTL,PARCEL"', allow_blank=False); d.add_data_validation(dv); dv.add("C9")
inp(10, "Days from empenho to cash in bank", 45, INT, "Measured on 7 editais: 34 best, 40-55 typical, 69 worst (docs/ORDER_TO_CASH.md).")

section(12, "2. MY COST PER KIT")
out(13, "Goods per kit at list price (BOM sheet)", f"={BOM_TOTAL}", BRL, "Sum of the 16 priced lines. Edit unit costs/quantities on the BOM sheet.", font=GREEN)
inp(14, "Supplier discount off list (account tier)", 0.0, PCT, "0% until an account is opened. ~45% is the UNVERIFIED account-tier figure; do not use it until quoted.")
inp(15, "Allowance for unpriced lines (kit_enxoval bag etc.)", 0.0, BRL, "BOM has 1 unpriced line. Leave 0 only if you accept that risk; the verdict flags it.")
inp(16, "Self-pack ceiling (kits you can pack yourself per order)", 240, INT, "config/capital.yaml: 8 h per won order at 2 min/kit. Above this a co-packer is REQUIRED.")
inp(17, "Co-packer cost per kit (if lot > ceiling)", None, BRL, "NO QUOTE EXISTS. 24 SP providers surveyed, none publishes a price. Blank = unknown -> verdict blocks.")
out(18, "Assembly per kit", '=IF(C5<=C16,0,IF(C17="","",C17))', BRL, "0 when you pack it yourself; the co-packer figure otherwise; blank = unknown.")
out(19, "Freight per kit from the FREIGHT sheet",
    (f'=IFERROR(IF(C9="LTL",'
     f'IF(INDEX(FREIGHT!$C$5:$C${FR_LAST},MATCH(C8,FREIGHT!$A$5:$A${FR_LAST},0))="","",INDEX(FREIGHT!$C$5:$C${FR_LAST},MATCH(C8,FREIGHT!$A$5:$A${FR_LAST},0))),'
     f'IF(INDEX(FREIGHT!$B$5:$B${FR_LAST},MATCH(C8,FREIGHT!$A$5:$A${FR_LAST},0))="","",INDEX(FREIGHT!$B$5:$B${FR_LAST},MATCH(C8,FREIGHT!$A$5:$A${FR_LAST},0)))),"")'),
    BRL, "Blank = not measured for that UF/mode. Override below if you have a real quote.", font=GREEN)
inp(20, "Freight per kit OVERRIDE (leave blank to use the table)", None, BRL, "Type a quoted figure here to replace the table value.")
out(21, "Freight per kit USED", '=IF(C20<>"",C20,IF(C19="","",C19))', BRL, "")
inp(22, "Packaging / box / label per kit", 0.0, BRL, "Not yet costed. A 60x40x40 box is not free.")
out(23, "TOTAL COST PER KIT", '=IF(OR(C18="",C21=""),"",C13*(1-C14)+C15+C18+C21+C22)', BRL, "Blank means a cost leg is unknown -- that is a NO BID, not a zero.", bold=True)

section(25, "3. TAXES, FEES, CAPITAL")
inp(26, "Revenue last 12 months (RBT12) for the Simples bracket", 180000, BRL, "First year: use the lot revenue x expected lots. Anexo I brackets: <=180k 4,00% | 360k 5,65% | 500k 6,73% | 720k 7,58%.")
out(27, "Simples Nacional rate on revenue", '=IF(C26<=180000,0.04,IF(C26<=360000,0.0565,IF(C26<=500000,0.0673,0.0758)))', PCT, "LC 123 Anexo I, effective rate (price/margin.py).")
inp(28, "IRRF withheld by the buyer", 0.0, PCT, "0% if the IN RFB 1.234 Anexo IV declaration is filed with every contract. 1,2% if it is not -- and there is no refund path.")
inp(29, "Platform fee as % of lot value", 0.015, PCT, "BLL: 1,5% of the lote adjudicado, only on a win. Compras.gov.br: 0%.")
inp(30, "Platform fee cap (R$)", 600, BRL, "BLL caps at R$600 when the lote > R$40.000. Put a huge number for no cap.")
inp(31, "Platform fixed fee per process (R$)", 0, BRL, "BNC R$118,80 / PCP R$129 per process even if you lose. BLL and Compras.gov.br: 0.")
inp(32, "Capital available (R$)", None, BRL, "THE DIAL. Blank = unknown; the verdict says so instead of assuming.")
inp(33, "Target NET margin", 0.15, PCT, "What 'pencils' means to you. Change it and the required price moves.")

section(35, "4. THE DEAL")
out(36, "Bid price per kit", "=C6*C7", BRL, "")
out(37, "Revenue (lot)", "=C36*C5", BRL, "")
out(38, "Cost of goods + freight + assembly (lot)", '=IF(C23="","",C23*C5)', BRL, "")
out(39, "Gross profit (lot)", '=IF(C38="","",C37-C38)', BRL, "")
out(40, "Gross margin %", '=IF(C39="","",IF(C37=0,0,C39/C37))', PCT, "")
out(41, "Simples tax", "=C37*C27", BRL, "")
out(42, "IRRF withheld", "=C37*C28", BRL, "")
out(43, "Platform fee", "=MIN(C37*C29,C30)+C31", BRL, "")
out(44, "NET PROFIT (lot)", '=IF(C39="","",C39-C41-C42-C43)', BRL, "", bold=True)
out(45, "NET MARGIN %", '=IF(C44="","",IF(C37=0,0,C44/C37))', PCT, "", bold=True)
out(46, "Net profit per kit", '=IF(C44="","",C44/C5)', BRL, "")
out(47, "Cash you must put up before the buyer pays", '=IF(C38="","",C38+C31)', BRL, "Goods, freight, assembly and any fixed fee are paid before the empenho pays out.")
out(48, "Annualised return on that cash", '=IF(OR(C44="",C47=""),"",IF(C47=0,0,C44/C47*365/C10))', PCT, "Net profit / cash tied up, scaled by the days to cash.")
out(49, "Hours of your time this order allows (C9)", "=8", INT, "Constraint C9: <= 8 h per won order. A lot above the self-pack ceiling needs a co-packer.")

section(51, "5. WHAT THIS DEAL NEEDS TO LOOK LIKE")
out(52, "Break-even price per kit (net profit = 0)", '=IF(C23="","",(C23+C31/C5)/(1-C27-C28-C29))', BRL, "Below this you lose money. Ignores the platform cap (conservative).")
out(53, "Price per kit for the target net margin", '=IF(C23="","",(C23+C31/C5)/(1-C27-C28-C29-C33))', BRL, "")
out(54, "  ...as % of the buyer's estimate", '=IF(C53="","",C53/C6)', PCT, "If this is above ~97% the lot cannot be won at target: per-item lines clear at 97-100%, lote unico far lower.")
out(55, "Max cost per kit at my bid for the target margin", "=C36*(1-C27-C28-C29-C33)-C31/C5", BRL, "What goods+freight+assembly must come in under.")
out(56, "Freight per kit that would still hit target (rest of cost fixed)", '=IF(C18="","",C55-C13*(1-C14)-C15-C18-C22)', BRL, "Negative = no freight price saves it at this bid.")
out(57, "Capital check", '=IF(C32="","UNKNOWN -- set capital in C32",IF(C47="","UNKNOWN -- cost incomplete",IF(C47<=C32,"OK","SHORT by R$ "&TEXT(C47-C32,"#,##0"))))', "@", "")
out(58, "VERDICT",
    '=IF(C23="","NO BID -- a cost leg is unknown (assembly or freight blank)",'
    'IF(C45<0,"NO -- loses money",'
    'IF(C45<C33,"THIN -- net "&TEXT(C45,"0.0%")&" below target "&TEXT(C33,"0%"),'
    'IF(AND(C32<>"",C47>C32),"PENCILS BUT CANNOT FUND -- "&C57,'
    'IF(C5>C16,"PENCILS -- needs a co-packer (lot > self-pack ceiling)",'
    'IF({gaps}>0,"PENCILS -- but "&{gaps}&" BOM line(s) unpriced; allowance in C15 is your guess","PENCILS"))))))'.format(gaps=BOM_GAPS),
    "@", "", bold=True)
d["C58"].fill = PatternFill("solid", fgColor="E2EFDA")

section(60, "6. SENSITIVITY -- net margin % by bid level and freight per kit")
d["B61"] = "Bid as % of estimate  \\  freight per kit (R$)"; d["B61"].font = BOLD
fr_cols = [("LTL SP->CE", 53.99), ("PAC to BA", 132.90), ("PAC to CE/PE/PA", 152.60), ("PAC to MA/SE/RN", 188.40)]
for j, (lab, val) in enumerate(fr_cols):
    col = 3 + j
    c = d.cell(row=61, column=col, value=lab); c.font = BOLD; c.alignment = Alignment(horizontal="center", wrap_text=True)
    v = d.cell(row=62, column=col, value=val); v.font = BLUE; v.fill = YELLOW; v.number_format = BRL; v.border = BOX
    d.column_dimensions[get_column_letter(col)].width = max(d.column_dimensions[get_column_letter(col)].width or 0, 18)
d["B62"] = "freight per kit ->"; d["B62"].font = BLACK
for i, pct in enumerate([0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]):
    row = 63 + i
    p = d.cell(row=row, column=2, value=pct); p.font = BLUE; p.fill = YELLOW; p.number_format = PCT; p.border = BOX
    p.alignment = Alignment(horizontal="right")
    for j in range(len(fr_cols)):
        col = get_column_letter(3 + j)
        # net% = 1 - cost/price - simples - irrf - platform% (cap ignored, fixed fee per kit included)
        f = (f'=IF(C$18="","",1-(($C$13*(1-$C$14)+$C$15+$C$18+{col}$62+$C$22)+$C$31/$C$5)/($C$6*$B{row})'
             f'-$C$27-$C$28-$C$29)')
        c = d.cell(row=row, column=3 + j, value=f); c.font = BLACK; c.number_format = PCT; c.border = BOX
d["B73"] = "Read it: find your bid level, read across to the freight you will really pay. Anything under the target in C33 is not a deal."
d["B73"].font = Font(name=F, size=9, italic=True, color="595959")

section(75, "LEGEND AND SOURCES")
notes = [
    "Blue on yellow = you type. Green = pulled from another sheet. Black = formula. Do not type over black cells.",
    "Goods: data/cost_table.csv, observed SP wholesale catalogue prices on 2026-09-19, supplier CNPJ/UF on every row. 16 of 17 lines priced.",
    "Freight: Correios PAC balcao public calculator and the STC published table, measured 2026-09-19 to CAPITAL CEPs only. Interior CEPs may differ.",
    "Assembly: no co-packer publishes a per-kit price (data/copacking.md). Self-pack ceiling from config/capital.yaml.",
    "Taxes: Simples Anexo I effective rates (LC 123); IRRF 1,2% per IN RFB 1.234 unless the Anexo IV declaration is filed (docs/LEGAL_FINDINGS.md).",
    "Platform fees: Regulamento BLL 2026 art. 17 (1,5%, cap R$600 above R$40k lots); BNC 2026 art. 24 (R$118,80/process); PCP adhesion page (R$129/process).",
    "Days to cash: docs/ORDER_TO_CASH.md, seven real editais. This model ignores late fines, sample costs and the SRP obligation to serve every call-off.",
]
for i, n in enumerate(notes):
    c = d.cell(row=76 + i, column=2, value=n); c.font = Font(name=F, size=9); c.alignment = Alignment(wrap_text=True, vertical="top")
    d.merge_cells(start_row=76 + i, start_column=2, end_row=76 + i, end_column=4)
    d.row_dimensions[76 + i].height = 26
d.freeze_panes = "A4"
for row in d.iter_rows(min_row=4, max_row=58, min_col=4, max_col=4):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
for r in range(5, 59):
    d.row_dimensions[r].height = 27 if d.cell(row=r, column=4).value else 16

wb.save(OUT)
print(OUT)
