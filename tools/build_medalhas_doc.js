const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,
       ShadingType,AlignmentType,BorderStyle,LevelFormat,PageBreak} = require('docx');
const fs=require('fs');

const F="Calibri", DK="1F3B36", GREY="595959";
const P=(t,o={})=>new Paragraph({spacing:{after:o.after??120},alignment:o.align,
  border:o.rule?{bottom:{style:BorderStyle.SINGLE,size:6,color:"BFBFBF",space:6}}:undefined,
  children:[new TextRun({text:t,font:F,size:o.size??21,bold:o.b,italics:o.i,color:o.color??"000000"})]});
const H=(t,l)=>new Paragraph({heading:l,spacing:{before:260,after:120},
  children:[new TextRun({text:t,font:F,bold:true,size:l===HeadingLevel.HEADING_1?30:24,color:DK})]});
const B=(t)=>new Paragraph({numbering:{reference:"b",level:0},spacing:{after:80},
  children:[new TextRun({text:t,font:F,size:21})]});

const W=[2900,1750,1750,1750,1750];
const cell=(t,o={})=>new TableCell({width:{size:o.w,type:WidthType.DXA},
  shading:o.fill?{type:ShadingType.CLEAR,color:"auto",fill:o.fill}:undefined,
  margins:{top:60,bottom:60,left:90,right:90},
  children:[new Paragraph({alignment:o.align,children:[new TextRun({text:t,font:F,size:19,
    bold:o.b,color:o.color??"000000"})]})]});
const table=(head,rows,widths=W)=>new Table({columnWidths:widths,
  rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>cell(h,{w:widths[i],fill:DK,b:true,color:"FFFFFF",align:i?AlignmentType.CENTER:undefined}))}),
    ...rows.map(r=>new TableRow({children:r.map((c,i)=>cell(String(c),{w:widths[i],align:i?AlignmentType.CENTER:undefined,b:r.bold}))}))]});

const doc=new Document({
 numbering:{config:[{reference:"b",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,
   style:{paragraph:{indent:{left:360,hanging:220}}}}]}]},
 sections:[{properties:{page:{margin:{top:1000,bottom:1000,left:1100,right:1100}}},children:[

 H("Medalhas e troféus — o negócio de reserva",HeadingLevel.HEADING_1),
 P("Notas para decisão futura. Medido em 21/09/2026 a partir de 2.039 licitações reais do PNCP, "+
   "das quais 90 descidas até o resultado homologado. Nada aqui foi contratado, comprado ou contactado.",
   {i:true,color:GREY,size:19,rule:true,after:200}),

 H("O que é",HeadingLevel.HEADING_2),
 P("Prefeituras compram medalhas, troféus e placas de homenagem para premiar gente em eventos: "+
   "campeonatos municipais, jogos escolares, gincanas, projetos pedagógicos, corridas, festivais. "+
   "Toda cidade faz isso, todo ano, e quase sempre compra por dispensa eletrônica porque os valores são pequenos."),
 P("Exemplos reais dos últimos meses:",{after:60}),
 B("Mambaí/GO — troféus, medalhas e placas para o Campeonato Municipal 2026"),
 B("São Miguel Arcanjo/SP — 750 medalhas personalizadas para eventos da Secretaria de Esporte"),
 B("Carmo do Rio Claro/MG — medalhas para alunos do projeto pedagógico “Construindo Números”"),
 B("Cruzaltense/RS — premiação do Campeonato Municipal de Bochas"),

 H("Por que é o plano B certo",HeadingLevel.HEADING_2),
 P("É o negócio do kit com as partes difíceis removidas. Não tem montagem: compra medalha, manda medalha. "+
   "O frete é irrelevante — uma caixa de 750 medalhas não se compara a uma banheira de 22 litros, e foi o "+
   "frete que quase matou o kit. Não tem armadilha de especificação: ninguém é desclassificado por confundir "+
   "20 com 22 litros. Não exige licença. E a personalização usa a mesma cadeia de impressão que o kit já precisa "+
   "para a mochila e a banheira."),
 P("O mais importante: o sistema já construído não sabe nem se importa com o que está sendo vendido. "+
   "O varredor, as treze regras, a triagem do comprador e o registro de propostas são agnósticos de produto. "+
   "Trocar de nicho significa trocar o arquivo de SKUs e a tabela de custos. Nada mais.",{b:true}),

 H("Os números, medidos",HeadingLevel.HEADING_2),
 table(["","Kit natalidade","Medalhas","Camisetas","Expediente"],[
   ["Licitações encontradas","2.044","2.039","1.028","1.566"],
   ["Dispensas","711 (35%)","1.519 (74%)","655 (64%)","1.012 (65%)"],
   ["Fechamento em dispensa","99%","100%","100%","97%"],
   ["Fecham no preço estimado","38%","59%","50%","32%"],
   ["HHI (concentração)","181","219","379","232"],
   ["Contrato mediano","R$ 30.848","R$ 5.588","R$ 8.450","R$ 3.570"]]),
 P("Medalhas ganha do kit em tudo que é mecanismo: o dobro da fatia em dispensa, fechamento mediano "+
   "de exatamente 100% do estimado, 59% adjudicadas sem desconto nenhum, e 1.519 oportunidades por ano "+
   "contra 711 do kit.",{after:100}),
 P("E o contrato do kit é cinco vezes e meia maior. É isso que decide.",{b:true}),

 H("O que custa fazer o mesmo dinheiro",HeadingLevel.HEADING_2),
 table(["Para R$ 144.000/ano","Lucro/contrato","Vitórias","Horas/ano","Lucro/hora"],[
   ["Kit natalidade","R$ 9.254","16","124","R$ 1.157"],
   ["Medalhas","R$ 1.676","86","172","R$ 838"],
   ["Camisetas","R$ 2.535","57","227","R$ 634"],
   ["Material de expediente","R$ 1.071","134","269","R$ 536"]],[2900,1750,1500,1500,1750]),
 P("Dezesseis vitórias por ano contra oitenta e seis. E repare no que é contra-intuitivo: os nichos com "+
   "MAIS licitações exigem uma taxa de acerto MAIOR, não menor, porque cada vitória vale muito menos."),

 new Paragraph({children:[new PageBreak()]}),

 H("Não é um preenchedor de temporada — é de capacidade",HeadingLevel.HEADING_2),
 P("Testei se medalhas movimenta nos meses em que o kit fica parado. Não movimenta. "+
   "A correlação mensal entre os dois é +0,96: eles sobem e descem juntos, nos mesmos meses, "+
   "porque os dois seguem o mesmo ciclo orçamentário municipal.",{b:true}),
 table(["Mês","Kit","Medalhas","Mês","Kit","Medalhas"],[
   ["jan","2,8%","3,4%","jul","11,3%","11,5%"],
   ["fev","7,3%","6,3%","ago","10,9%","11,5%"],
   ["mar","10,5%","9,7%","set","9,0%","10,1%"],
   ["abr","10,7%","11,3%","out","5,4%","5,9%"],
   ["mai","11,4%","10,3%","nov","4,6%","5,8%"],
   ["jun","12,0%","10,1%","dez","4,1%","4,1%"]],[1300,1450,1600,1300,1450,1600]),
 P("Os dois morrem de outubro a janeiro e explodem de março a setembro. Então medalhas não preenche "+
   "meses vazios — preenche HORAS vazias dentro dos meses cheios. A 2 vitórias por mês no kit, "+
   "só 16 das 87 horas mensais estão sendo usadas. É essa folga que medalhas ocupa, e é por isso "+
   "que só faz sentido depois que o kit estiver rodando sozinho."),

 H("O que não se sabe, e que mudaria a conta",HeadingLevel.HEADING_2),
 P("Duas suposições sustentam a tabela acima e nenhuma das duas foi medida para medalhas:",{after:80}),
 B("A margem de 30% foi medida só no kit. Uma medalha que custa R$3 e fecha a R$18 pode ter margem muito melhor. Os preços unitários homologados observados vão de R$4,28 a R$24 por medalha, e troféus de R$18 a R$1.600."),
 B("As horas por pedido são estimadas: 8h para o kit (17 itens numa bolsa), 2h para medalhas (SKU único). Se um pedido de medalhas realmente levar 2 horas E a margem for melhor que 30%, a diferença de lucro por hora fecha ou inverte."),
 P("Medir as duas coisas custa uma tarde e nenhuma ligação. Vale fazer antes de ligar a chave — mas "+
   "não antes do kit estar de pé.",{i:true}),

 H("O que ligaria a chave",HeadingLevel.HEADING_2),
 B("Trocar config/skus.yaml pelos SKUs de medalha e troféu"),
 B("Montar uma tabela de custos com 2 ou 3 fornecedores de brindes/premiação em SP"),
 B("Ajustar as palavras de busca do varredor — nada mais do sistema muda"),
 B("Confirmar que a mesma empresa (CNAE) pode vender os dois. Provavelmente sim: 4649-4/99 já cobre brindes"),

 H("Quando fazer",HeadingLevel.HEADING_2),
 P("Depois que o kit estiver ganhando de forma previsível — digamos, três meses seguidos com pelo menos "+
   "uma vitória — e não antes. O motivo não é medo: é que a taxa de vitória do kit ainda é desconhecida, "+
   "e dividir a atenção antes de conhecê-la significa não aprender nem uma nem outra."),
 P("O risco que justifica manter este plano vivo: o mercado do kit pode encolher. Uma resolução nacional "+
   "empurrando o benefício para dinheiro em vez de bens, programas estaduais comprando de forma "+
   "centralizada, e a queda de ~3% ao ano nos nascimentos são todos reais. Se isso acontecer, medalhas "+
   "é para onde a mesma máquina aponta — e apontar custa um arquivo de configuração."),
 P("Evitar camisetas: HHI 379, com um único fornecedor detendo 85 das 550 linhas vencidas. "+
   "É o único dos quatro com um incumbente dominante.",{i:true,color:"9C0006"}),
 ]}]});

Packer.toBuffer(doc).then(b=>{fs.writeFileSync('/home/user/ACOLHE/docs/ACOLHE_medalhas_plano_B.docx',b);console.log('written');});
