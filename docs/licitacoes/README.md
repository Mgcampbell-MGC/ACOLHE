# Licitações encontradas — arquivo diário

Cada arquivo é a saída de um dia do scanner (`python -m harvest.run_daily YYYYMMDD saida.xlsx`),
nomeado pelo dia de PUBLICAÇÃO no PNCP, não pelo dia em que foi rodado.

**Por que esta pasta existe:** a primeira varredura real (19/09/2026) foi escrita num diretório
temporário e quase se perdeu. As licitações são o único ativo perecível do negócio — duas das
quatro encontradas fechavam em 3 dias. A partir daqui o scanner grava aqui, no repositório, e
cada dia fica versionado.

As abas são as de `report/digest.py`: **HOJE**, **PIPELINE**, **MINHAS APOSTAS**,
**SAÚDE DO SISTEMA**. As colunas que a fundadora digita (em MINHAS APOSTAS) são lidas de volta
a cada execução e nunca sobrescritas.

| Arquivo | Dia | Candidatas | Observação |
|---|---|---|---|
| `2026-09-19_licitacoes.xlsx` | 2026-09-19 | 4 | Primeira varredura real. 4.595 licitações lidas, coleta completa. Todas as 4 ficaram em VERIFICAR: o PNCP Família B estava fora do ar e a lista de itens não pôde ser lida, então não houve preço nem lance sugerido. |

---

## O que mais havia no dia 15/09/2026 — a varredura completa

4.595 licitações publicadas, coleta completa (o PNCP declarou 4.595 e entregou 4.595).
Procurando **toda** a linguagem de enxoval — `ENXOVA`, `KIT NATALIDADE`, `KIT BEBÊ`,
`KIT MATERNIDADE`, `KIT GESTANTE`, `RECÉM-NASCIDO`, `PUERPERA`, `BERÇÁRIO`,
`FRALDA`, `PUERICULTURA` — apareceram **14 licitações**. Quatro viraram candidatas.
As outras dez:

| Resultado | Quantas | Quais |
|---|---|---|
| **PERDIDA — prazo já fechado** | **1** | **Rio Branco do Sul/PR**, kit natalidade, R$16.520,64 |
| Excluída: enxoval HOSPITALAR | 1 | Cidade Gaúcha/PR — locação de enxoval de hospital, não é o nosso mercado |
| Excluída: fralda avulsa, não kit | 6 | São Pedro do Turvo/SP e Alto Jequitibá/MG (geriátrica), Cosmópolis/SP e Aracaju/SE (junto com dieta/seringa), Passo Fundo/RS, Patos de Minas/MG (médico-hospitalar) |
| Excluída: berçário, mas outra coisa | 2 | Espírito Santo do Pinhal/SP (conserto de máquina de lavar), Campina Grande/PB (higiene para creches) |

As nove exclusões estão certas. **A perdida não.**

### Rio Branco do Sul/PR — a que escapou, e por quê

    objeto:        "fornecimento de kit natalidade, com entrega parcelada,
                    conforme a necessidade da Secretaria, durante 12 meses"
    valor:         R$ 16.520,64   (~46 kits a R$359 — o tamanho que CABE no capital)
    publicada:     2026-09-15 15:50
    propostas até: 2026-09-18 23:59
    janela:        3 dias

Era a licitação que melhor servia ao negócio no dia inteiro — pequena o bastante
para o capital disponível — e fechou antes de alguém olhar, porque a varredura rodou
no dia 19 sobre as publicações do dia 15.

**O que isto ensina, e é a lição operacional mais cara do dia:** as janelas de proposta
vão de **3 a 14 dias**. Das cinco licitações de kit do dia, a de janela mais curta era
a única viável. Um scanner que roda com quatro dias de atraso não perde 4 dias de
oportunidade — perde exatamente as licitações pequenas e rápidas, que são o mercado
desta empresa. **A varredura tem de rodar todo dia, de manhã, sobre a publicação da
véspera.** Isto é o risco #12 do registro ("o cron morre em silêncio") aparecendo com
outra roupa.

**Era uma DISPENSA, não um pregão.** `modalidadeNome: Dispensa`, `numeroCompra: PDE 31`
(processo de dispensa eletrônica), processo 143/2026, `srp: false`. Isso explica a janela
de 3 dias — e faz dela mais do que uma licitação perdida. Pelo art. 75 II da Lei 14.133 o
teto de dispensa em 2026 é **R$ 65.492,11** (Decreto 12.807/2025), e R$16.520 está bem
dentro. As dispensas costumam não exigir atestado de capacidade técnica: é exatamente o
caminho de PRIMEIRA VENDA identificado em `docs/HABILITACAO.md` §4. Ou seja, escapou não
só um contrato, mas uma porta de entrada.

### Os links

    Órgão      MUNICIPIO DE RIO BRANCO DO SUL — CNPJ 76.105.576/0001-85
    Unidade    FUNDO DE ASSISTÊNCIA SOCIAL — Rio Branco do Sul/PR (IBGE 4122206)
    Compra     2026 / sequencial 163 — numeroControlePNCP 76105576000185-1-000163/2026

| O quê | URL | Estado |
|---|---|---|
| Registro da compra (Família A) | `https://pncp.gov.br/api/consulta/v1/orgaos/76105576000185/compras/2026/163` | **VERIFICADO** — HTTP 200, devolve o registro |
| Página pública | `https://pncp.gov.br/app/editais/76105576000185/2026/163` | formato NÃO VERIFICADO — o app do PNCP é JavaScript e devolve a mesma casca de 59.879 bytes para qualquer rota, então não dá para confirmar por fetch. Abrir no navegador para confirmar |
| Itens (Família B) | `https://pncp.gov.br/api/pncp/v1/orgaos/76105576000185/compras/2026/163/itens` | fora do ar em 19/09 |
| Resultados por item | `https://pncp.gov.br/api/pncp/v1/orgaos/76105576000185/compras/2026/163/itens/{n}/resultados` | idem — é aqui que sai quem venceu e por quanto |
| Arquivos (o edital em PDF) | `https://pncp.gov.br/api/pncp/v1/orgaos/76105576000185/compras/2026/163/arquivos` | idem |

**A fazer na segunda:** `valorTotalHomologado` ainda estava **null** na consulta de
19/09 — fechou dia 18 e o resultado não tinha sido publicado. Reler o registro da
Família A e, se ela voltar, os resultados por item. Um preço real de fechamento de um
kit natalidade de ~46 unidades é exatamente o parâmetro que falta para calibrar o
modelo — melhor do que qualquer estimativa.

**Aviso sobre os links da planilha:** `report/digest.py` monta o link trocando os
separadores do numeroControlePNCP, o que dá `/app/editais/76105576000185/1/000163/2026`.
Pode estar errado — a rota documentada é `{cnpj}/{ano}/{sequencial}`. Não foi possível
distinguir por fetch (as duas devolvem a mesma casca). Confirmar no navegador na segunda
e corrigir o gerador se for o caso.

### E o teto de recall

Tudo acima saiu do TEXTO DO OBJETO. Cerca de 1 em cada 4 licitações de kit não se
descreve como tal no título e só é visível pela lista de itens (PNCP Família B, fora
do ar naquele dia). Então o dia 15/09 provavelmente teve 6 ou 7 licitações de kit, não
5 — e as que faltam não estão nesta tabela porque ninguém consegue vê-las ainda.
