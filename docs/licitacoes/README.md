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

**A fazer na segunda:** ver o resultado homologado de Rio Branco do Sul no PNCP. Um
preço real de fechamento de um kit natalidade de ~46 unidades é exatamente o
parâmetro que falta para calibrar o modelo — melhor do que qualquer estimativa.

### E o teto de recall

Tudo acima saiu do TEXTO DO OBJETO. Cerca de 1 em cada 4 licitações de kit não se
descreve como tal no título e só é visível pela lista de itens (PNCP Família B, fora
do ar naquele dia). Então o dia 15/09 provavelmente teve 6 ou 7 licitações de kit, não
5 — e as que faltam não estão nesta tabela porque ninguém consegue vê-las ainda.
