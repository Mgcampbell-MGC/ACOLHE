"""Take the founder's restructured deal model, fix the Simples table, set it to a
deal that actually passes, and add the SCENARIOS sheet.

Styling conventions are HERS and are copied, not replaced: Arial, dark green
1F3B36 section bars, yellow FFF2A8 + blue 0000FF for typed inputs, grey 9pt notes.
"""
import os
import shutil

from openpyxl import load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "ACOLHE_deal_model.xlsx")
# The founder's own restructured workbook was the starting point. That upload is
# ephemeral, so the committed file is the source of truth from here on; every
# edit below sets an absolute value or replaces a sheet outright, so re-running
# this against the committed file is idempotent.
_UPLOAD = ("/root/.claude/uploads/0136d521-4d06-562e-b5db-7a27acb508dd/"
           "01b2f4cc-ACOLHE_deal_model_1.xlsx")
SRC = _UPLOAD if os.path.exists(_UPLOAD) else OUT

FN = "Arial"
DARKG = "1F3B36"
BAR = PatternFill("solid", fgColor=DARKG)
YEL = PatternFill("solid", fgColor="FFF2A8")
GREY = PatternFill("solid", fgColor="F2F2F2")
HDRF = Font(name=FN, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=FN, size=14, bold=True, color=DARKG)
LBL = Font(name=FN, size=10)
LBLB = Font(name=FN, size=10, bold=True)
IN = Font(name=FN, size=10, color="0000FF")
NOTE = Font(name=FN, size=9, color="808080")
BRL = '"R$ "#,##0;("R$ "#,##0);-'
BRL2 = '"R$ "#,##0.00;("R$ "#,##0.00);-'
PCT = '0.0%;(0.0%);-'
PCT2 = '0.00%;(0.00%);-'
NUM = '#,##0;(#,##0);-'
NUM1 = '#,##0.0;(#,##0.0);-'

if os.path.abspath(SRC) != os.path.abspath(OUT):
    shutil.copy(SRC, OUT)
wb = load_workbook(OUT)

# ---------------------------------------------------------------- 1. Simples
# Their table used the effective rate at each BAND CEILING and stopped at
# R$720k. LC 123 Anexo I is (RBT12 x nominal - deducao) / RBT12, and it runs
# to R$4,8M. At a band ceiling the two agree exactly (360k -> 5,65%,
# 500k -> 6,73%, 720k -> 7,58%), so nothing already correct changes; the
# interior of each band stops being overstated and the >720k bands exist.
# Closes RISK_REGISTER #26.
ANEXO_I = ('IF({r}<=0,0.04,'
           'IF({r}<=180000,0.04,'
           'IF({r}<=360000,({r}*0.073-5940)/{r},'
           'IF({r}<=720000,({r}*0.095-13860)/{r},'
           'IF({r}<=1800000,({r}*0.107-22500)/{r},'
           'IF({r}<=3600000,({r}*0.143-87300)/{r},'
           '({r}*0.19-378000)/{r}))))))')
d = wb["DEAL"]
d["C20"] = "=" + ANEXO_I.format(r="INPUTS!$C$23")
d["C65"] = "=" + ANEXO_I.format(r="C64")
d["D20"] = ("LC 123 Anexo I, alíquota EFETIVA = (RBT12 x nominal - dedução)/RBT12. "
            "Cobre as seis faixas até R$4,8M.")
wb["INPUTS"]["D23"] = ("Anexo I efetivo: ≤180k 4,00% · 360k 5,65% · 720k 7,58% · "
                       "1,8M ~9,1% · 3,6M ~11,9%. Tem de bater com a receita do ano "
                       "que você planeia — é o que a verificação 9 compara.")

# ------------------------------------------------- 2. set it to a deal that passes
# Scenario B below: the best deal available TODAY, with no supplier account,
# no co-packer and the capital actually on hand.
i = wb["INPUTS"]
i["C5"] = 61        # biggest lot R$15.600 funds at a cost of R$252,77/kit
i["C7"] = 0.90      # per-item lots clear at 97-100% of estimate: 90% wins and pays
i["C32"] = 8        # what the capital allows at a 45-day float, not a hope
d["D50"] = "Set to what the capital actually allows (see check 5), not to a hope."

# ------------------------------------------------------------ 3. SCENARIOS
if "SCENARIOS" in wb.sheetnames:
    del wb["SCENARIOS"]
s = wb.create_sheet("SCENARIOS", wb.sheetnames.index("GATES") + 1)
s.sheet_view.showGridLines = False
s.column_dimensions["A"].width = 2
s.column_dimensions["B"].width = 46
for col in "CDEFGH":
    s.column_dimensions[col].width = 16
s.column_dimensions["I"].width = 56

s["B2"] = "SCENARIOS  —  the same business under six sets of facts"
s["B2"].font = TITLE
s["B3"] = ("Each column stands alone: the blue cells are its own assumptions, everything below is "
           "computed from them. Lots per year is never assumed — it is what R$15.600 of capital "
           "can actually turn over at that column's float.")
s["B3"].font = NOTE
s["B3"].alignment = Alignment(wrap_text=True)
s.merge_cells("B3:I3")
s.row_dimensions[3].height = 26

heads = [
    ("C", "A · As typed", "100 kits at 75% of estimate — the anchor inherited from the written plan."),
    ("D", "B · TODAY, done right", "The same market, bid the way a per-item lot is actually won, in a lot the capital can fund."),
    ("E", "C · + 20% supplier discount", "Emilio opens a revenda account. Nothing else changes."),
    ("F", "D · + 28-day supplier terms", "Terms instead of prepay: cash is out 6 days, not 45."),
    ("G", "E · Terms, NO discount", "Terms alone, list prices. Put this next to column C."),
    ("H", "F · Lote único at 50%", "Why rule 1 refuses these: a single-lot tender clears at 36–63% of estimate."),
]
r = 5
for c in "BCDEFGHI":
    s[f"{c}{r}"].fill = BAR
    s[f"{c}{r}"].font = HDRF
s[f"B{r}"] = "SCENARIO"
for col, title, _ in heads:
    s[f"{col}{r}"] = title
    s[f"{col}{r}"].alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
s[f"I{r}"] = "WHAT IT MEANS"
s.row_dimensions[r].height = 32

# assumptions ---------------------------------------------------------------
ASSUMP = [
    ("Kits in the lot", NUM, [100, 61, 73, 73, 61, 61]),
    ("Bid as % of the buyer's estimate", PCT, [0.75, 0.90, 0.90, 0.90, 0.90, 0.50]),
    ("Supplier discount off list", PCT, [0, 0, 0.20, 0.20, 0, 0]),
    ("Freight per kit (LTL SP→CE, measured)", BRL2, [53.99] * 6),
    ("Days the cash is out (float)", NUM, [45, 45, 45, 6, 6, 45]),
]
r = 6
first_assump = r
for label, fmt, vals in ASSUMP:
    s[f"B{r}"] = label
    s[f"B{r}"].font = LBL
    for (col, _, _), v in zip(heads, vals):
        cell = s[f"{col}{r}"]
        cell.value = v
        cell.font = IN
        cell.fill = YEL
        cell.number_format = fmt
        cell.alignment = Alignment(horizontal="center")
    r += 1
KITS, BIDPCT, DISC, FREIGHT, DAYS = (first_assump + n for n in range(5))

s[f"I{first_assump}"] = "Column A is 100 kits because that is the median tender; B–E are the biggest lot R$15.600 can actually fund."
s[f"I{BIDPCT}"] = "Per-item lots clear at 97–100% of estimate. Bidding 75% was never required — it was inherited."
s[f"I{DISC}"] = "UNVERIFIED. ~45% is the rumoured account tier; 20% is deliberately conservative."
s[f"I{FREIGHT}"] = "Swap this for R$188,40 (PAC to MA) and every column below turns negative."
s[f"I{DAYS}"] = "45 = prepay. 6 = a supplier granting 28 days. This one line is the whole business."
for rr in range(first_assump, first_assump + 5):
    s[f"I{rr}"].font = NOTE
    s[f"I{rr}"].alignment = Alignment(wrap_text=True, vertical="center")

# shared constants ----------------------------------------------------------
r += 1
s[f"B{r}"] = "Shared by every column: estimate R$359,05 · capital R$15.600 · fixed costs R$6.000/yr · 8 h per order · R$5,20/US$"
s[f"B{r}"].font = NOTE
s.merge_cells(f"B{r}:I{r}")
SHARED = r
EST, CAPITAL, FIXED, HOURS, FX = ("INPUTS!$C$6", "INPUTS!$C$28", "INPUTS!$C$33",
                                  "INPUTS!$C$34", "INPUTS!$C$35")
r += 2


def block(title, rows):
    global r
    for c in "BCDEFGHI":
        s[f"{c}{r}"].fill = BAR
        s[f"{c}{r}"].font = HDRF
    s[f"B{r}"] = title
    r += 1
    out = {}
    for label, fmt, tmpl, note, bold in rows:
        s[f"B{r}"] = label
        s[f"B{r}"].font = LBLB if bold else LBL
        for col, _, _ in heads:
            cell = s[f"{col}{r}"]
            cell.value = "=" + tmpl.format(c=col)
            cell.font = Font(name=FN, size=10, bold=bold)
            cell.number_format = fmt
        if note:
            s[f"I{r}"] = note
            s[f"I{r}"].font = NOTE
            s[f"I{r}"].alignment = Alignment(wrap_text=True, vertical="center")
        out[label] = r
        r += 1
    r += 1
    return out


COST = f"(BOM!$E$22*(1-{{c}}{DISC})+{{c}}{FREIGHT})"
BID = f"({EST}*{{c}}{BIDPCT})"
REV = f"({BID}*{{c}}{KITS})"
CASH = f"({COST}*{{c}}{KITS})"
LOTS = f"(({CAPITAL}/{CASH})*365/{{c}}{DAYS})"
REVY = f"({REV}*{LOTS})"
RATE = ANEXO_I.format(r=REVY)
FEE = "MIN({rev}*INPUTS!$C$25,INPUTS!$C$26)".format(rev=REV)
NET = f"({REV}-{CASH}-{REV}*({RATE})-{FEE})"

block("ONE LOT", [
    ("Cost per kit", BRL2, COST, "Goods after discount, plus freight. Assembly is R$0 — every lot here is inside the 240-kit self-pack ceiling.", False),
    ("Bid price per kit", BRL2, BID, None, False),
    ("Cash you must front", BRL, CASH, "Must not exceed R$15.600. That ceiling is what sets the lot size.", False),
    ("Net margin on the lot", PCT, f"IF({REV}=0,0,{NET}/{REV})", None, True),
    ("Net profit on the lot", BRL, NET, None, False),
])
block("A YEAR OF LOTS LIKE THIS", [
    ("Lots the capital can actually carry", NUM1, LOTS, "Not an assumption: capital ÷ cash per lot × 365 ÷ float days.", False),
    ("Revenue for the year", BRL, REVY, None, False),
    ("Simples effective rate at that revenue", PCT2, RATE, "Rises with revenue — the columns that scale pay a higher rate, and that is already deducted below.", False),
    ("TAKE-HOME for the year, after fixed costs", BRL, f"({NET}*{LOTS}-{FIXED})", None, True),
    ("   …per month", BRL, f"(({NET}*{LOTS}-{FIXED})/12)", None, True),
    ("   …per month in US$", BRL, f"IF({FX}=0,0,({NET}*{LOTS}-{FIXED})/12/{FX})", None, False),
    ("Hours a month that takes", NUM1, f"({HOURS}*{LOTS}/12)", "Against the 87 h/month the plan allows. Column D is the only one that starts to fill them.", False),
])

# verdict row ---------------------------------------------------------------
for c in "BCDEFGHI":
    s[f"{c}{r}"].fill = GREY
s[f"B{r}"] = "WHAT THE COLUMN SAYS"
s[f"B{r}"].font = LBLB
takerow = r - 5          # "TAKE-HOME for the year" row
for col, _, _ in heads:
    s[f"{col}{r}"] = (f'=IF({col}{takerow}<0,"LOSES MONEY",'
                      f'IF({col}{takerow}<12000,"TOO SMALL TO LIVE ON","WORKS"))')
    s[f"{col}{r}"].font = Font(name=FN, size=10, bold=True)
    s[f"{col}{r}"].alignment = Alignment(horizontal="center")
    s.conditional_formatting.add(
        f"{col}{r}",
        CellIsRule(operator="equal", formula=['"WORKS"'],
                   fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(color="006100", bold=True)))
    s.conditional_formatting.add(
        f"{col}{r}",
        CellIsRule(operator="equal", formula=['"LOSES MONEY"'],
                   fill=PatternFill("solid", fgColor="FFC7CE"), font=Font(color="9C0006", bold=True)))
s[f"I{r}"] = 'R$12.000/yr is a placeholder for "worth doing at all" — change it if your bar is different.'
s[f"I{r}"].font = NOTE
r += 3

# the three sentences -------------------------------------------------------
for c in "BCDEFGHI":
    s[f"{c}{r}"].fill = BAR
    s[f"{c}{r}"].font = HDRF
s[f"B{r}"] = "THE THREE THINGS THIS TABLE SAYS"
r += 1
lines = [
    ("1.  The 75% anchor was the whole problem, and it costs nothing to fix.",
     "Goods plus freight are 70,4% of the buyer's estimate before a centavo of tax. Bidding 75% leaves 4,6 points "
     "to cover Simples, the platform fee and profit — it cannot be done. Per-item lots clear at 97–100% of estimate, "
     "so 90% both wins and pays. Column A to column B is one number typed differently: −R$429/month becomes +R$1.694."),
    ("2.  Supplier TERMS are worth about six times a supplier DISCOUNT.",
     "A 20% discount (column C) takes the month to ~R$4.000. Terms alone, at list price (column E), take it past "
     "R$11.000 — because the same R$15.600 turns over eight times as often. When you write to a wholesaler, "
     "'do you have boleto a prazo' is a bigger question than 'what is your revenda price'."),
    ("3.  Two kinds of tender can never work, at any price.",
     "Lote único (column F) clears at 36–63% of estimate against a 70,4% cost floor — arithmetically unwinnable, "
     "which is what rule 1 already refuses. And any tender delivering kit-by-kit to households: parcel freight to "
     "MA is R$188,40 a kit and turns every column above negative. That is what the local-de-entrega reader is for."),
]
for head, body in lines:
    s[f"B{r}"] = head
    s[f"B{r}"].font = Font(name=FN, size=10, bold=True, color=DARKG)
    s.merge_cells(f"B{r}:I{r}")
    r += 1
    s[f"B{r}"] = body
    s[f"B{r}"].font = Font(name=FN, size=9)
    s[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    s.merge_cells(f"B{r}:I{r}")
    s.row_dimensions[r].height = 40
    r += 2

s[f"B{r}"] = ("Still true in every column: the 17th BOM line (the kit bag) is carried at R$0 because nobody has priced it, "
              "and no co-packer has quoted, so nothing here may exceed 240 kits. Both are on your list.")
s[f"B{r}"].font = Font(name=FN, size=9, color="9C0006")
s.merge_cells(f"B{r}:I{r}")
s.freeze_panes = "C6"

wb.save(OUT)
print(OUT)
