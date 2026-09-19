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
