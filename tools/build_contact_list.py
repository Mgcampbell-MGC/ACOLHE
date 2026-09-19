"""docs/ACOLHE_municipios.xlsx -- who to phone, what to ask, what to write down.

Every contact here was read out of a PUBLISHED edital in data/editais/, in the
clause that names it as the channel for esclarecimentos or as the órgão's own
address. Nothing was scraped from a private source and NOBODY has been
contacted.
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "ACOLHE_municipios.xlsx")

FN = "Arial"
DARKG = "1F3B36"
BAR = PatternFill("solid", fgColor=DARKG)
YEL = PatternFill("solid", fgColor="FFF2A8")
GREENF = PatternFill("solid", fgColor="E2EFDA")
HDR = Font(name=FN, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=FN, size=14, bold=True, color=DARKG)
B = Font(name=FN, size=10)
BB = Font(name=FN, size=10, bold=True)
BLUE = Font(name=FN, size=10, color="0000FF")
NOTE = Font(name=FN, size=9, color="808080")
MONO = Font(name="Courier New", size=10)
thin = Side(style="thin", color="BFBFBF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
TOP = Alignment(vertical="top", wrap_text=True)

wb = Workbook()


def header(ws, row, labels, widths):
    for i, (lab, w) in enumerate(zip(labels, widths), 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = HDR; c.fill = BAR; c.border = BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30


def put(ws, row, values, blue_from=None, height=52):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.border = BOX; c.alignment = TOP
        if blue_from and i >= blue_from:
            c.font = BLUE; c.fill = YEL
        else:
            c.font = B
    ws.row_dimensions[row].height = height


# ============================================================ COMECE AQUI
s = wb.active
s.title = "COMECE AQUI"
s.sheet_view.showGridLines = False
s["A1"] = "Falar com municípios — não para vender, para entender"
s["A1"].font = TITLE
for i, (txt, f) in enumerate([
    ("Isto NÃO é uma ligação de venda. Você não tem CNPJ, não pode licitar, e não está oferecendo nada. "
     "Você está perguntando como o programa funciona. Essa é uma conversa que um servidor público "
     "costuma aceitar de bom grado — e é a única forma de descobrir o que nenhum edital diz.", B),
    ("Duas conversas diferentes, com pessoas diferentes. Não misture as duas.", BB),
], start=2):
    s.cell(row=i + 1, column=1, value=txt).font = f
    s.merge_cells(start_row=i + 1, start_column=1, end_row=i + 1, end_column=6)
    s.cell(row=i + 1, column=1).alignment = TOP
    s.row_dimensions[i + 1].height = 40 if i == 2 else 16

header(s, 6, ["", "Com quem", "Por que essa pessoa", "O que só ela sabe", "Quanto dura", "Como abrir"],
       [4, 30, 46, 52, 12, 46])
convos = [
    ("A", "Secretaria de Assistência Social / coordenação do CRAS",
     "É quem entrega o kit na mão da mãe. Não compra — mas define o que vai dentro, ouve a reclamação e sabe se o kit serviu.",
     "Quantos kits por ano de verdade. O que as mães dizem que falta. O que veio errado da última vez. "
     "Se o programa tem lei municipal própria. Se é contínuo ou depende de emenda.",
     "15–20 min",
     "«Estou estudando o mercado de kit natalidade e vi que o município de vocês comprou. Você teria 15 minutos "
     "para me explicar como o programa funciona aí? Não estou vendendo nada — ainda nem tenho empresa aberta.»"),
    ("B", "Setor de Licitações / Compras — o pregoeiro ou agente de contratação",
     "É quem conduz o certame. Fala com fornecedor o dia inteiro e sabe exatamente onde eles falham.",
     "Quantos licitantes apareceram. Se já deu deserto ou fracassado, e por quê. O que trava a habilitação de "
     "empresa pequena. Se o preço estimado veio de cotação ou do último contrato.",
     "10–15 min",
     "«Estou me preparando para participar de licitações de kit natalidade e queria entender melhor o processo "
     "antes de me cadastrar. Posso fazer duas ou três perguntas?»"),
]
r = 7
for row in convos:
    put(s, r, row, height=96)
    r += 1

r += 1
s.cell(row=r, column=1, value="A ordem que eu faria").font = BB
r += 1
order = [
    ("1º", "Coronel Xavier Chaves / MG", "É o contato mais completo que existe na pasta: e-mail, telefone COM RAMAL e WhatsApp, todos impressos no próprio edital. Município pequeno, o programa é do CRAS, e o edital é recente e bem escrito. Maior chance de alguém atender e conversar."),
    ("2º", "São Pedro do Iguaçu / PR", "O único edital que publica o e-mail do DEPARTAMENTO DE ASSISTÊNCIA SOCIAL direto, não o da licitação. É a conversa A sem intermediário."),
    ("3º", "Belterra / PA", "O termo de referência inteiro é da SEMTDES e traz o e-mail dela em cada página. Município do Pará, kit entregue via CRAS — perfil exato do seu cliente-alvo, e longe de São Paulo."),
    ("4º", "Bocaiúva do Sul / PR", "Setor de compras com telefone direto. Bom para a conversa B."),
    ("5º", "Irecê / BA", "Pregão de até 400 kits, agente de contratação nomeado no edital. Maior volume da pasta — bom para entender um comprador maior."),
]
for a, b_, c_ in order:
    s.cell(row=r, column=1, value=a).font = BB
    s.cell(row=r, column=2, value=b_).font = BB
    cell = s.cell(row=r, column=3, value=c_); cell.font = B; cell.alignment = TOP
    s.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
    s.row_dimensions[r].height = 40
    r += 1

r += 2
for c in range(1, 7):
    s.cell(row=r, column=c).fill = BAR
s.cell(row=r, column=1, value="TRÊS REGRAS").font = HDR
r += 1
rules = [
    "Não ofereça nada, não mande catálogo, não peça para ser cadastrada como fornecedora. No momento em que virar venda, a conversa acaba e a porta fecha.",
    "Ligue em horário de expediente do interior: 8h–11h ou 13h–16h. Muita prefeitura pequena fecha ao meio-dia.",
    "Se pedirem para você formalizar por e-mail, formalize — e guarde a resposta. Um servidor explicando o programa por escrito vale mais que dez editais.",
]
for t in rules:
    cell = s.cell(row=r, column=1, value=t); cell.font = B; cell.alignment = TOP
    s.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    s.row_dimensions[r].height = 28
    r += 1

# ================================================================ CONTATOS
c = wb.create_sheet("CONTATOS")
c.sheet_view.showGridLines = False
c["A1"] = "Contatos — todos lidos no edital publicado do próprio município"
c["A1"].font = TITLE
c["A2"] = ("Cada e-mail e telefone abaixo está impresso no edital ou no termo de referência que o município "
           "publicou. A coluna «onde no edital» diz exatamente onde. Colunas amarelas são suas.")
c["A2"].font = NOTE
header(c, 4, ["Município", "UF", "O que compraram", "Setor", "E-mail", "Telefone / WhatsApp",
              "Onde no edital", "Falei em", "Com quem", "O que disseram"],
       [22, 5, 40, 26, 34, 22, 38, 12, 20, 46])
contacts = [
    ("Coronel Xavier Chaves", "MG", "RP kits de natalidade para puérperas em vulnerabilidade atendidas pelo CRAS (PE 37/2026)",
     "Setor de Licitações", "licitacao@coronelxavierchaves.mg.gov.br", "(32) 3216-1053 ramais 109 e 110 · WhatsApp (32) 99199-6496",
     "Quadro «Mais informações» do edital retificado, com horário de expediente do setor"),
    ("São Pedro do Iguaçu", "PR", "Materiais para montagem de kits de enxoval de bebê (Termo de Referência)",
     "Departamento de Assistência Social", "acaosocial-spi@yahoo.com.br", "(45) 3255-8000",
     "Cabeçalho do TR: «e-mail: Depto de assistência Social»"),
    ("Belterra", "PA", "Enxoval para bebê (kit natalidade) para gestantes atendidas pelo CRAS — SEMTDES",
     "SEMTDES — Sec. Mun. de Trabalho e Desenvolvimento Social", "semtdes@belterra.pa.gov.br", "não publicado no TR",
     "Rodapé de todas as páginas do TR, com o endereço Vila Americana, Centro"),
    ("Bocaiúva do Sul", "PR", "RP itens de higiene para compor kits natalidade (PE 40/2025)",
     "Setor de Compras e Licitações", "licitacaobocaiuvadosul@gmail.com", "(41) 92003-9870 · (41) 92003-9850",
     "Rodapé de cada página: «SETOR DE COMPRAS E LICITAÇÕES», Rua Carlos Alberto Ribeiro, 21, Centro"),
    ("Irecê", "BA", "RP produtos para compor kit de enxoval natalidade, até 400 kits (PE SRP 003/2026) — FMAS",
     "Agente de Contratação / Pregoeiro", "irecepregao@gmail.com", "(74) 3641-1733 · (74) 3641-3116",
     "Aviso de licitação assinado pelo Agente de Contratação, 26/01/2026"),
    ("Bom Sucesso do Sul", "PR", "RP kits enxoval para bebê e kits higiene para bebê (PE 34/2026)",
     "Compras / Licitações / Contratos", "compras@bssul.pr.gov.br · licitacoes@bssul.pr.gov.br · contratos@bssul.pr.gov.br", "(46) 3199-2333",
     "Cap. XXIX: «A comunicação entre o MUNICÍPIO e o fornecedor se dará pelos e-mails…»; telefone no TR"),
    ("Agrolândia", "SC", "RP higiene pessoal e itens infantis para compor kits para gestantes (PE 01/2026/FMS)",
     "Pregoeiro", "pregoeiro@agrolandia.sc.gov.br", "(47) 3534-4212",
     "Item 5.2: canal para pedidos de esclarecimento e impugnações"),
    ("São João do Paraíso", "MA", "RP kit enxoval de bebê para gestantes e puérperas — Sec. Mun. de Assistência Social",
     "CPL — Comissão Permanente de Licitação", "cplsjparaiso@gmail.com", "(99) 99105-3540",
     "Quadro «Pedidos de esclarecimentos e impugnações»"),
    ("Itaquaquecetuba", "SP", "Kit maternidade, 17 itens, SRP (PE 90088/2025) — o kit que o BOM inteiro copia",
     "não publicado no que foi lido", "—", "—",
     "Registro do PNCP; o edital em PDF não pôde ser baixado (Família B fora do ar)"),
]
r = 5
for row in contacts:
    put(c, r, list(row) + [None, None, None], blue_from=8, height=56)
    r += 1
c.cell(row=r + 1, column=1, value=(
    "Faltam aqui os cinco municípios da varredura de 15/09 — Alvorada de Minas/MG, Maracás/BA, Vitória/ES, "
    "Junco do Maranhão/MA e Rio Branco do Sul/PR. Os contatos deles estão sendo levantados e entram nesta aba "
    "quando estiverem confirmados na fonte.")).font = NOTE
c.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=7)
c.freeze_panes = "A5"

# ================================================================ PERGUNTAS
q = wb.create_sheet("O QUE PERGUNTAR")
q.sheet_view.showGridLines = False
q.column_dimensions["A"].width = 3
q.column_dimensions["B"].width = 100
q["B1"] = "As perguntas — leve impressas, marque as respostas"
q["B1"].font = TITLE
q["B2"] = ("Não faça todas. Escolha quatro ou cinco. Uma conversa boa é curta e termina com a pessoa "
           "querendo falar de novo.")
q["B2"].font = NOTE
blocks = [
    ("CONVERSA A — Assistência Social / CRAS   (a mais valiosa)", [
        "Como funciona o programa de kit natalidade aqui? Quem tem direito?",
        "Quantos kits vocês entregam por ano, mais ou menos? É estável ou varia muito?",
        "O programa tem lei ou decreto municipal próprio, ou é decidido a cada ano?",
        "O recurso vem de onde — orçamento próprio, emenda parlamentar, cofinanciamento estadual?",
        "Quem decide o que vai dentro do kit? Já mudou a lista alguma vez? Por quê?",
        "O que as mães mais comentam quando recebem? Tem alguma coisa que sempre falta?",
        "Já chegou kit com problema — item faltando, tamanho errado, qualidade ruim? O que vocês fizeram?",
        "Vocês entregam no CRAS, na maternidade, ou na casa da família?",
        "Se eu fosse fornecer para vocês, o que você diria que a maioria dos fornecedores erra?",
    ]),
    ("CONVERSA B — Licitações / Pregoeiro", [
        "Quantas empresas costumam aparecer num pregão de kit natalidade de vocês?",
        "Já deu deserto ou fracassado? O que aconteceu?",
        "O preço estimado vocês tiram de cotação com fornecedores ou do contrato anterior?",
        "Vocês costumam pedir amostra antes de adjudicar?",
        "O atestado de capacidade técnica é exigido? Aceitam atestado de cliente privado?",
        "Para uma empresa nova, de outro estado, o que costuma dar problema na habilitação?",
        "Vocês compram mais por pregão ou por dispensa? Como uma empresa fica sabendo de uma dispensa?",
        "Na prática, quantos dias levam do empenho até o pagamento?",
        "A entrega é num endereço só, ou parcelada conforme a demanda?",
    ]),
    ("O QUE ANOTAR DEPOIS — vale mais que a ligação", [
        "Nº de kits por ano · valor por kit que eles acham normal · nº de licitantes típico",
        "Se já deu deserto — e por quê. Uma licitação sem licitante é um comprador querendo comprar e sem conseguir.",
        "Se aceitam atestado privado. É a resposta que destrava a sua primeira venda.",
        "Dias reais até o pagamento. O modelo assume 45; ninguém confirmou isso com um comprador.",
        "O nome e o ramal de quem falou com você, e se pode ligar de novo.",
    ]),
]
r = 4
for title, items in blocks:
    for col in range(2, 3):
        q.cell(row=r, column=col).fill = BAR
    cell = q.cell(row=r, column=2, value=title); cell.font = HDR
    r += 2
    for it in items:
        cell = q.cell(row=r, column=2, value="☐  " + it)
        cell.font = B; cell.alignment = TOP
        q.row_dimensions[r].height = 26
        r += 1
    r += 2

# ============================================================== O MERCADO
m = wb.create_sheet("O QUE JÁ SABEMOS")
m.sheet_view.showGridLines = False
m.column_dimensions["A"].width = 3
m.column_dimensions["B"].width = 44
m.column_dimensions["C"].width = 72
m["B1"] = "Antes de ligar — o que os editais já responderam"
m["B1"].font = TITLE
m["B2"] = "Não gaste a ligação perguntando o que já está escrito. Use para mostrar que você estudou."
m["B2"].font = NOTE
facts = [
    ("Quem compra", "Quase sempre a Secretaria de Assistência Social via CRAS, e muitas vezes o FUNDO (FMAS/FMS) e não a prefeitura — o CNPJ do comprador é outro."),
    ("Como compram", "Das 5 licitações de kit do dia 15/09, TRÊS foram DISPENSA ELETRÔNICA e duas pregão. As pequenas vão por dispensa — janela de 3 dias, teto de R$65.492 (art. 75 II), e normalmente sem atestado."),
    ("Prazo de entrega", "Entre «imediato» (Belterra) e 20 dias corridos (Coronel Xavier Chaves). Cinco dias é o mais comum."),
    ("Pagamento", "Todos dizem «até 30 dias», mas cada um conta a partir de um evento diferente: do atesto, da NF, da entrega, ou «até o dia 10 do mês seguinte»."),
    ("Atestado", "6 dos 7 editais lidos exigem atestado de capacidade técnica; 1 (Agrolândia) não exige nada. Nenhum exige que seja de órgão público."),
    ("Entrega", "8 de 9 são parceladas ou com endereço definido a cada ordem de fornecimento. Só um entrega o lote inteiro num endereço só."),
    ("Tamanho", "De R$11.621 (Junco do Maranhão) a R$944.586 (Vitória). O que cabe no capital de R$15.600 é a faixa de baixo."),
]
r = 4
for a, b_ in facts:
    m.cell(row=r, column=2, value=a).font = BB
    cell = m.cell(row=r, column=3, value=b_); cell.font = B; cell.alignment = TOP
    m.row_dimensions[r].height = 42
    r += 1
r += 1
cell = m.cell(row=r, column=2, value=(
    "O que NENHUM edital responde, e por isso vale a ligação: quantos concorrentes aparecem, se já deu deserto, "
    "quantos dias o pagamento leva DE VERDADE, se aceitam atestado privado, e o que as mães acham do kit."))
cell.font = Font(name=FN, size=10, bold=True, color="9C0006"); cell.alignment = TOP
m.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
m.row_dimensions[r].height = 46

wb.save(OUT)
print(OUT)
