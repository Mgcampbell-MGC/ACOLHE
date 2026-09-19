"""Build docs/ACOLHE_fornecedores.xlsx -- who to contact, in what order, and what to ask.

Everything here was read from a public catalogue or company site and, where a
CNPJ is stated, resolved at publica.cnpj.ws. NOBODY HAS BEEN CONTACTED.
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "ACOLHE_fornecedores.xlsx")

FN = "Arial"
BLACK = Font(name=FN, size=10)
BOLD = Font(name=FN, size=10, bold=True)
BLUE = Font(name=FN, size=10, color="0000FF")
SMALL = Font(name=FN, size=9, color="595959")
H1 = Font(name=FN, size=14, bold=True)
HDR = Font(name=FN, size=10, bold=True, color="FFFFFF")
DARK = PatternFill("solid", fgColor="1F3864")
YELLOW = PatternFill("solid", fgColor="FFFF00")
RED = PatternFill("solid", fgColor="FCE4E4")
GREENF = PatternFill("solid", fgColor="E2EFDA")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
TOP = Alignment(vertical="top", wrap_text=True)

wb = Workbook()


def header(ws, row, labels, widths):
    for i, (lab, w) in enumerate(zip(labels, widths), 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = HDR; c.fill = DARK; c.border = BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30


def put(ws, row, values, fills=None, fonts=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = (fonts or {}).get(i, BLACK); c.border = BOX; c.alignment = TOP
        if fills and i in fills:
            c.fill = fills[i]


# ============================================================ START HERE
s = wb.active
s.title = "COMECE AQUI"
s["A1"] = "Fornecedores — quem contactar, em que ordem, e porquê"; s["A1"].font = H1
s["A2"] = ("Ninguém foi contactado. Nada foi comprado, nada foi cadastrado. "
           "Esta lista é para você decidir — e quando decidir, os e-mails prontos estão nas duas últimas abas.")
s["A2"].font = BLACK
s["A3"] = ("Ordem sugerida: os dois primeiros valem mais que todos os outros juntos. "
           "Um resolve o preço do kit; o outro resolve tudo acima de 240 kits.")
s["A3"].font = SMALL
header(s, 5, ["#", "Contactar", "Porquê este", "O que isto destrava", "Quanto custa perguntar", "Contactado em", "Resposta"],
       [4, 30, 52, 52, 18, 14, 34])
steps = [
    ("1", "Emilio (Confecções Emilio)",
     "Hoje ele sozinho fornece 11 das 16 linhas com preço. Os preços que temos são do catálogo aberto — a tabela de revenda nunca foi vista.",
     "O preço real do kit. Todo o modelo de margem depende desta resposta. Também: pedido mínimo, prazo de pagamento e se ele fatura para PJ nova.",
     "R$ 0 — um e-mail"),
    ("2", "Um co-packer (comece pela DirectaLog)",
     "Ninguém publica preço por kit montado. Sem um número, o sistema recusa qualquer lote acima de 240 kits.",
     "A metade grande do mercado. E o prazo de montagem, que decide se editais de 5 dias são possíveis.",
     "R$ 0 — um e-mail"),
    ("3", "Brascol (OneShop Distribuidora)",
     "Preços atrás de login, mas é o único que publica um caminho para BOLETO PARCELADO. Cobre banheira e provavelmente muita coisa do Emilio.",
     "Segunda fonte + a única possibilidade conhecida de comprar a prazo, que é o que muda o ciclo de caixa de 34 dias para ~6.",
     "R$ 0 — cadastro no site"),
    ("4", "JN Fraldas (Mensa Distribuidora)",
     "Fornece as 4 linhas de higiene. Preços públicos, mas de varejo — a tabela de revenda não foi vista.",
     "Desconto nas fraldas e lenços, que são as linhas de consumo mais caras do kit.",
     "R$ 0 — um e-mail"),
    ("5", "Yanai Atacado",
     "Tem a banheira mais barata conforme encontrada (R$17,89) e vende roupas de bebê — pode cobrir linhas do Emilio.",
     "Benchmark de preço nas roupas. Se bater o Emilio, a concentração cai sozinha.",
     "R$ 0 — um e-mail"),
    ("6", "Um segundo co-packer com frota própria (COTLOG ou Doma)",
     "Os dois montam kits E são transportadoras. A Doma tem filial em Belém-PA.",
     "Possivelmente o problema do frete inteiro: frete no contrato deles em vez de encomenda a R$150/kit.",
     "R$ 0 — um e-mail"),
    ("7", "Um fornecedor da bolsa/mochila do kit",
     "A linha kit_enxoval (a própria bolsa) não tem preço nem fornecedor. Municípios costumam querer o brasão impresso.",
     "A 17ª linha do BOM e o gate do Step 0.",
     "R$ 0 — pesquisa em curso"),
    ("8", "Tenda Atacado",
     "Só uma linha (sabonete líquido), boleto só à vista, é cash-and-carry.",
     "Pouco. Deixe por último.",
     "R$ 0"),
]
r = 6
for st in steps:
    put(s, r, list(st) + [None, None], fills={6: YELLOW, 7: YELLOW}, fonts={6: BLUE, 7: BLUE})
    s.row_dimensions[r].height = 56
    r += 1
s.cell(row=r + 1, column=2, value="Regra que você me deu: eu não contacto ninguém sem a sua palavra. Diga 'pode mandar' e eu envio os textos das duas últimas abas para você aprovar antes de sair.").font = SMALL
s.merge_cells(start_row=r + 1, start_column=2, end_row=r + 1, end_column=5)
s.freeze_panes = "A6"

# ================================================================= GOODS
g = wb.create_sheet("MERCADORIAS")
g["A1"] = "Fornecedores de mercadoria — o que já foi lido do catálogo público"; g["A1"].font = H1
g["A2"] = ("CNPJ resolvido em publica.cnpj.ws; a UF vem da API, nunca do que o site diz. "
           "Preços observados em 2026-09-19. Colunas azuis são suas.")
g["A2"].font = SMALL
header(g, 4, ["Prioridade", "Nome", "Razão social", "CNPJ", "UF / cidade", "Linhas do kit que cobre",
              "Preços públicos?", "Pedido mínimo", "Pagamento (novo cliente)", "Site", "O que ainda não sabemos",
              "Contactado em", "Desconto obtido", "Pedido mínimo real", "Prazo pagamento"],
       [10, 20, 30, 20, 20, 40, 16, 20, 26, 30, 44, 14, 16, 16, 16])
goods = [
    ("1", "Emilio", "CONFECCOES EMILIO LTDA", "50.191.584/0001-06", "SP / São Paulo",
     "11 de 16: mochila, banheira, cobertor, cueiro, pagão, body, pano de boca, meias, toalha banho, kit higiene, saboneteira",
     "Sim (catálogo VTEX aberto)", "não publicado", "não publicado",
     "https://www.emilio.com.br",
     "Tabela de revenda, pedido mínimo, prazo, se fatura para CNPJ novo, estoque real. RISCO #15 do registro: 11 linhas num só CNPJ."),
    ("2", "Brascol", "ONESHOP DISTRIBUIDORA LTDA", "18.483.322/0001-02", "SP / São Paulo (Brás)",
     "banheira confirmada; catálogo atrás de login — provável sobreposição ampla com o Emilio",
     "Não — exige login", "R$500 atacado / R$1.500 alto atacado", "PIX, cartão 6x; BOLETO PARCELADO por CNAE",
     "https://brascol.com.br",
     "Tudo além da banheira. Quais CNAEs liberam o boleto parcelado — é o único caminho de crédito conhecido."),
    ("3", "JN Fraldas", "MENSA DISTRIBUIDORA LTDA", "10.290.457/0001-31", "SP / São Paulo (Canindé)",
     "4: fralda descartável RN, toalhas umedecidas, shampoo infantil, óleo infantil",
     "Sim (tier varejo)", "não publicado", "PIX / Visa / Master / Elo",
     "https://www.jnfraldas.com.br",
     "Se existe tier de revenda. Nenhum caminho para prazo publicado."),
    ("4", "Yanai Atacado", "COMERCIO DE ROUPAS YANAI LTDA", "44.040.459/0001-94", "SP / São Paulo",
     "banheira (a mais barata conforme: R$17,89); é atacado de ROUPAS — pode cobrir as linhas têxteis",
     "Sim", "não publicado", "não publicado",
     "https://yanaiatacado.com.br",
     "Todo o catálogo têxtil. Esta é a pista mais promissora para quebrar a concentração no Emilio."),
    ("5", "Lar & Cia Utilidades", "não resolvido", "UNVERIFIED", "SP? (não confirmado)",
     "banheira e utilidades plásticas", "Sim", "—", "—",
     "https://www.lareciautilidades.com.br",
     "O CNPJ não foi encontrado no site. Sem CNPJ não há UF confirmada — e a UF muda o ICMS em ~6 pontos."),
    ("6", "Tenda Atacado", "TENDA ATACADO SA", "01.157.555/0011-86", "SP / Guarulhos",
     "1: sabonete líquido", "Sim", "não publicado", "Boleto À VISTA, cartão",
     "https://tendaatacado.com.br",
     "Pouco a ganhar. Cash-and-carry, sem prazo."),
    ("7", "Martins", "MARTINS COMERCIO E SERVICOS DE DISTRIBUICAO S/A", "43.214.055/0001-07", "MG / Uberlândia",
     "banheira", "Sim", "não publicado", "não publicado",
     "https://www.martinsatacado.com.br",
     "FORA DE SP: pela LC 123 art. 13 §1 XIII (h) você paga a diferença de ICMS, ~6 pontos. Só vale se for >6% mais barato."),
]
r = 5
for row in goods:
    put(g, r, list(row) + [None, None, None, None],
        fills={12: YELLOW, 13: YELLOW, 14: YELLOW, 15: YELLOW},
        fonts={12: BLUE, 13: BLUE, 14: BLUE, 15: BLUE})
    g.row_dimensions[r].height = 62
    r += 1
g.cell(row=r + 1, column=2, value="Uma busca por segundas fontes (têxteis, puericultura, higiene e a bolsa do kit) está em andamento; esta aba cresce quando ela terminar.").font = SMALL
g.freeze_panes = "B5"

# ============================================================== COVERAGE
c = wb.create_sheet("CONCENTRACAO")
c["A1"] = "Quantos fornecedores cada linha do kit tem hoje"; c["A1"].font = H1
c["A2"] = ("Esta é a aba que explica por que o Emilio é o e-mail número 1. "
           "Quinze das dezassete linhas têm UM fornecedor. Se ele disser não, o kit não existe.")
c["A2"].font = BLACK
header(c, 4, ["Linha do kit", "Fornecedores conhecidos", "Quantos", "Risco"], [30, 60, 10, 40])
cov = [
    ("banheira_lisa", "Yanai (R$17,89) · Brascol (R$18,05) · Emilio (R$18,90) · Lar & Cia · Martins/MG", 5, "OK — cinco fontes, spread de 5,6%"),
    ("mochila", "Emilio", 1, "ÚNICA FONTE"),
    ("cobertor_infantil", "Emilio", 1, "ÚNICA FONTE"),
    ("cueiro", "Emilio", 1, "ÚNICA FONTE"),
    ("pagao", "Emilio", 1, "ÚNICA FONTE"),
    ("body_manga_longa", "Emilio", 1, "ÚNICA FONTE"),
    ("pano_de_boca", "Emilio", 1, "ÚNICA FONTE"),
    ("par_de_meias", "Emilio", 1, "ÚNICA FONTE"),
    ("toalha_banho_infantil", "Emilio", 1, "ÚNICA FONTE"),
    ("kit_higiene_bebe", "Emilio", 1, "ÚNICA FONTE"),
    ("saboneteira", "Emilio", 1, "ÚNICA FONTE"),
    ("fralda_descartavel_rn", "JN Fraldas", 1, "ÚNICA FONTE"),
    ("toalhas_umedecidas", "JN Fraldas", 1, "ÚNICA FONTE"),
    ("shampoo_infantil", "JN Fraldas", 1, "ÚNICA FONTE"),
    ("oleo_infantil", "JN Fraldas", 1, "ÚNICA FONTE"),
    ("sabonete_liquido", "Tenda Atacado", 1, "ÚNICA FONTE"),
    ("kit_enxoval (a bolsa)", "nenhum", 0, "SEM PREÇO E SEM FORNECEDOR — trava o gate do Step 0"),
]
r = 5
for line, who, n, risk in cov:
    fill = GREENF if n >= 2 else RED
    put(c, r, [line, who, n, risk], fills={4: fill})
    c.row_dimensions[r].height = 22
    r += 1
c.cell(row=r + 1, column=1, value="Emilio sozinho:").font = BOLD
c.cell(row=r + 1, column=2, value="11 das 16 linhas com preço").font = BOLD
c.cell(row=r + 2, column=1, value="Fonte: data/cost_table.csv, data/cost_banheira.csv, data/cost_toiletries.csv, docs/RISK_REGISTER.md risco #15.").font = SMALL
c.freeze_panes = "A5"

# ============================================================ CO-PACKERS
k = wb.create_sheet("MONTAGEM (CO-PACKERS)")
k["A1"] = "Quem pode montar os kits — 24 empresas de SP examinadas, nenhuma publica preço"; k["A1"].font = H1
k["A2"] = ("Você pode montar até ~240 kits sozinha (8 h por pedido, 2 min por kit). Acima disso é obrigatório. "
           "Peça cotação a três: um barato sem mínimo, um com capacidade provada, um que também é transportadora.")
k["A2"].font = BLACK
header(k, 4, ["Prioridade", "Empresa", "Razão social", "CNPJ", "Cidade", "Por que este",
              "Mínimo publicado", "Embarca no frete dele?", "Site", "Contactado em", "Preço por kit", "Prazo (dias)"],
       [10, 22, 34, 20, 18, 46, 16, 20, 40, 14, 16, 12])
cop = [
    ("1", "DirectaLog", "DIRECTALOG LOGISTICA LTDA", "22.932.742/0001-98", "Osasco/SP",
     "Sem mínimo, cobrança por serviço, preparo em D+3, confere XML contra o físico, nomeia Correios/Jadlog/Total Express. O perfil mais próximo do que você precisa.",
     "sem mínimo", "Sim — retribui tabela das transportadoras", "https://www.directalog.com.br"),
    ("2", "VIP Manuseios", "não impresso no site — UNVERIFIED", "UNVERIFIED", "São Paulo/SP",
     "'Sem volume mínimo'. Confere por NF com relatório por NF e saldo em tempo real — exatamente o controlo que você precisa recebendo de 4 atacadistas.",
     "sem mínimo", "Sim — cota junto aos Correios", "https://www.vipmanuseios.com.br"),
    ("3", "COTLOG", "COTLOG SOLUCOES LOGISTICAS LTDA", "10.273.317/0001-55", "Cotia/SP",
     "Monta kits E é transportadora própria (rodoviário fracionado + aéreo, porta a porta). ISO 9001. Pode resolver o frete junto com a montagem.",
     "não publicado", "Sim — frota/contrato próprios", "https://www.cotlog.com.br/montagem-kits"),
    ("4", "Doma Logística", "DOMA LOGISTICA LTDA", "27.541.681/0001-51", "Guarulhos/SP",
     "Frota própria e FILIAL EM BELÉM-PA — a única com presença publicada no Norte/Nordeste, que é onde estão os editais que valem a pena.",
     "não publicado", "Sim — frota própria", "https://www.domalogistica.com.br"),
    ("5", "UP! Manuseios", "UP ORGANIZACAO E EVENTOS LTDA", "43.213.105/0001-31", "São Paulo/SP",
     "Único com capacidade PROVADA publicada: 7.500 kits em 10 dias úteis, paletizados. É a referência para um lote grande.",
     "não publicado", "Sim — Correios/transportadora/carro dedicado", "https://www.upmanuseios.com.br"),
    ("6", "DRENG", "DRENG SOLUCOES E TECNOLOGIA EM LOGISTICA LTDA", "48.878.504/0001-35", "São Paulo/SP",
     "Publica que tem tabela de preços pré-fixada com desconto progressivo e sem contrato longo. Deve responder rápido com número.",
     "não publicado", "não declarado", "https://www.dreng.com.br"),
    ("7", "G+Ship (Guarde Mais)", "ROGER FULFILLMENT LTDA", "46.373.347/0001-80", "São Paulo/SP",
     "Sem mínimo e tem simulador de preço no site. Mas o transporte é por sua conta.",
     "sem mínimo", "Não — transporte é do cliente", "https://goship.com.br"),
    ("8", "Tempos", "TEMPOS DE BRASIL TERCEIRIZACAO... LTDA", "01.211.578/0001-50", "Santana de Parnaíba/SP",
     "Co-packer industrial desde 1996, 2.000 m², ISO 9001:2015. Para o cenário de 5.000 kits.",
     "não publicado", "não declarado", "https://www.tempos.com.br/co-packer"),
    ("9", "Mão na Massa", "MAO NA MASSA PRODUCOES LTDA", "26.195.320/0001-38", "São Paulo/SP",
     "Montagem + armazenagem, despacho por Correios ou motoboy. Segunda onda.",
     "não publicado", "Sim — Correios", "https://www.maonamassamanuseios.com.br"),
    ("10", "Envio Certo", "ENVIO CERTO PRODUCOES E SERVICOS LTDA", "43.628.686/0001-72", "São Paulo/SP",
     "CNAE 8292-0/00 (envasamento e empacotamento sob contrato) — é literalmente a atividade. Foco em kits de influencer.",
     "não publicado", "Sim — com rastreio nacional", "https://www.enviocertomanuseios.com.br"),
    ("11", "Teconlog", "TECONLOG SOLUCOES LOGISTICAS LTDA", "22.027.337/0001-25", "Vargem Grande Paulista/SP",
     "7.000 m², 6.000 posições-palete, expedição D+0. Grande — pode não querer um cliente pequeno.",
     "não publicado", "Parceiros homologados", "https://teconlog.com.br"),
    ("12", "Paulista Express", "PAULISTA EXPRESS TRANSPORTES LTDA", "74.289.034/0001-84", "São Bernardo do Campo/SP",
     "Transportadora com frota própria que também monta kits — mas a cobertura publicada é só SP capital e interior.",
     "não publicado", "Sim — frota própria (só SP)", "https://www.paulistaexpress.com.br"),
    ("13", "Contacto Logística", "não impresso no site — UNVERIFIED", "UNVERIFIED", "São Paulo/SP",
     "Publica 'poucas unidades ou grandes quantidades'. CNPJ não confirmado.",
     "sem mínimo", "não declarado", "https://contactologistica.com.br"),
    ("14", "Grupo SRM", "SRM - TERCEIRIZACAO DE SERVICOS E RECURSOS HUMANOS LTDA", "02.798.885/0001-41", "Barueri/SP",
     "ATENÇÃO: vende MÃO DE OBRA por peça montada, não é armazém. Isso pode esbarrar na regra C3 (sem funcionários). Só como último recurso e com o contador a confirmar.",
     "não publicado", "Não", "https://www.gruposrm.com.br"),
]
r = 5
for row in cop:
    put(k, r, list(row) + [None, None, None],
        fills={10: YELLOW, 11: YELLOW, 12: YELLOW}, fonts={10: BLUE, 11: BLUE, 12: BLUE})
    k.row_dimensions[r].height = 58
    r += 1
notes = [
    "NÃO contactar: Nascra Brindes — CNPJ com situação SUSPENSA na Receita.",
    "Fora de perfil: FM Logistic (só grandes contas), Saberpack (envase de alimentos/químicos), Cartlog (endereço em Londrina/PR), LJ Indústria (CNPJ não impresso).",
    "Não são co-packers: Mercado Livre Full, Amazon FBA, Magalu, Shopee — só montam pedidos das próprias plataformas.",
    "Sites bloqueados na pesquisa (podem valer uma olhada manual): Lotus Logística, MPP Log/Promopack, DHL Fulfillment, Frenet.",
]
for i, n in enumerate(notes):
    cell = k.cell(row=r + 1 + i, column=2, value=n); cell.font = SMALL; cell.alignment = TOP
    k.merge_cells(start_row=r + 1 + i, start_column=2, end_row=r + 1 + i, end_column=6)
k.freeze_panes = "B5"

# ========================================================= EMAIL: GOODS
e = wb.create_sheet("E-MAIL p MERCADORIAS")
e.column_dimensions["A"].width = 3
e.column_dimensions["B"].width = 108
e["B1"] = "Mensagem pronta — fornecedores de mercadoria"; e["B1"].font = H1
e["B2"] = ("Copie, troque [NOME] e a lista de itens, envie. Não promete volume que você não tem "
           "e não esconde que a empresa é nova — os dois mentem e os dois são descobertos no cadastro.")
e["B2"].font = SMALL
body = """Assunto: Cadastro de revenda — kits de enxoval para prefeituras (CNPJ em SP)

Bom dia,

Sou [SEU NOME], da [EMPRESA], em São Paulo. Montamos kits de enxoval para
recém-nascidos e fornecemos para prefeituras através de licitação pública
(pregão eletrônico). Compramos o kit completo — roupas, enxoval, higiene,
banheira e bolsa — e entregamos montado ao município.

Gostaria de abrir cadastro de revenda e receber a tabela de atacado.
Algumas perguntas objetivas:

1. Qual a tabela de preços para revenda/atacado nos itens abaixo, e como ela
   se compara ao preço do site?
      - [colar aqui a lista de itens e as quantidades típicas]

2. Existe pedido mínimo, por valor ou por peça? E pedido mínimo por SKU?

3. Condições de pagamento para cliente novo: só PIX/cartão, ou existe caminho
   para boleto a prazo? Em quantos pedidos ou em quanto tempo?

4. Como funciona o faturamento para CNPJ? Emitem NF-e com os dados do meu
   pedido de compra?

5. Vocês conseguem reservar/segurar estoque entre a assinatura de um contrato
   público e a compra? Nosso ciclo é: ganhamos a licitação, recebemos a nota
   de empenho e só então compramos — normalmente com 5 a 20 dias para entregar.

6. Entregam num endereço de terceiros em São Paulo (empresa que monta os kits)
   ou só no endereço de cadastro?

7. Qual o prazo de entrega para São Paulo capital, num pedido de [X] peças?

Sou uma operação pequena e nova — não vou prometer volume que ainda não tenho.
O que posso dizer é que cada contrato ganho é uma compra fechada, do kit
inteiro, e que preciso de um fornecedor com preço estável para conseguir
precificar uma proposta com 12 meses de validade.

Obrigado pela atenção,
[SEU NOME] — [EMPRESA] — CNPJ [xx] — [telefone] — [e-mail]"""
r = 4
for line in body.split("\n"):
    cell = e.cell(row=r, column=2, value=line or None)
    cell.font = Font(name="Courier New", size=10); cell.alignment = Alignment(vertical="top")
    r += 1
e.cell(row=r + 1, column=2, value="Por que a pergunta 5 importa: você compra DEPOIS de ganhar. Um fornecedor que não segura estoque transforma uma vitória numa multa.").font = SMALL
e.cell(row=r + 2, column=2, value="Por que a pergunta 6 importa: se o fornecedor entrega direto no co-packer, você nunca toca na mercadoria — é esse o modelo.").font = SMALL

# ====================================================== EMAIL: CO-PACKER
p = wb.create_sheet("E-MAIL p MONTAGEM")
p.column_dimensions["A"].width = 3
p.column_dimensions["B"].width = 108
p["B1"] = "Mensagem pronta — empresas de montagem de kits"; p["B1"].font = H1
p["B2"] = "Mesma mensagem para as três primeiras da aba MONTAGEM. As respostas são comparáveis lado a lado."
p["B2"].font = SMALL
body2 = """Assunto: Cotação — montagem de kits de enxoval (lotes de 100 a 5.000)

Bom dia,

Sou [SEU NOME], da [EMPRESA], em São Paulo. Fornecemos kits de enxoval para
recém-nascidos a prefeituras, por licitação. Preciso de um parceiro para
receber a mercadoria de 3 a 6 atacadistas do Brás/Pari, montar os kits e
expedir para o município.

Cada kit tem 17 a 20 itens: roupas de bebê, toalhas, banheira plástica de
20 litros, itens de higiene e uma bolsa. A embalagem final é a própria bolsa
do kit, dentro de caixa de papelão.

1. Preço por kit montado para lotes de 100, 500 e 5.000 kits. Há adicional
   por item volumoso (a banheira)?
2. Cobram por kit, por hora ou por peça? Há taxa de setup, mínimo de
   faturamento ou mensalidade?
3. Recebem entregas de 3 a 6 fornecedores distintos para o mesmo projeto?
   Conferem contra as NF-e? Como e em quanto tempo reportam faltas e avarias?
4. Quantos dias de armazenagem sem custo entre o primeiro recebimento e a
   expedição? Preço por posição-palete/dia além disso?
5. Prazo de montagem em dias úteis, contado do recebimento do último item,
   para 100 / 500 / 5.000 kits.
6. Expedição: emitem CT-e em nome de vocês (frete no contrato de vocês) ou
   reservam no meu CNPJ? Quais transportadoras? Peço cotação de um lote
   paletizado de São Paulo para Recife, Fortaleza, Salvador, Belém e um
   município do interior do Nordeste, para 100 e 500 kits. Há ad valorem ou
   GRIS sobre um kit de ~R$ 200?
7. Entrega em órgão público: aceitam entrega agendada com conferência do
   recebedor, canhoto assinado e comprovante para o processo de pagamento?
8. Condições de pagamento: sinal na aprovação? boleto 14/28 dias? faturam
   separado a montagem (NFS-e) e o frete (CT-e)?
9. Seguro da mercadoria em armazém e em trânsito — quem cobre e até que valor?
10. Cadastro: exigem tempo mínimo de CNPJ, faturamento mínimo ou referências?

Obrigado,
[SEU NOME] — [EMPRESA] — CNPJ [xx] — [telefone] — [e-mail]"""
r = 4
for line in body2.split("\n"):
    cell = p.cell(row=r, column=2, value=line or None)
    cell.font = Font(name="Courier New", size=10); cell.alignment = Alignment(vertical="top")
    r += 1
p.cell(row=r + 1, column=2, value="A pergunta 6 é a mais valiosa de todas: se o co-packer embarcar no contrato de frete DELE, o frete pode cair de ~R$150 por kit (encomenda) para ~R$55 (carga consolidada). Isso é a margem inteira.").font = SMALL
p.cell(row=r + 2, column=2, value="A pergunta 5 alimenta a regra 5 do sistema: um prazo de montagem longo torna editais de 5 dias impossíveis, e é melhor saber antes de licitar.").font = SMALL

wb.save(OUT)
print(OUT)
