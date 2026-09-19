# HABILITAÇÃO — o pacote de documentos e os cadastros de plataforma

**Data da pesquisa:** 19 de setembro de 2026
**Perfil:** ME optante pelo Simples Nacional, sede em São Paulo/SP (capital), vende bens (kits de enxoval) a municípios em pregão eletrônico sob a Lei 14.133/2021. Fundadora opera sozinha.

> **Aviso.** Levantamento de fontes primárias para revisão por advogado/contador. Não é parecer. Onde não li a fonte que fixa um número, escrevi **UNVERIFIED** e disse o que resolveria.

**Convenções**
- `[LEI]` — texto normativo lido integralmente na fonte indicada.
- `[PLATAFORMA]` — página ou regulamento do próprio emissor/plataforma, lido nesta sessão.
- `[INFERÊNCIA]` — minha leitura; não está escrito com todas as letras na fonte.
- `[NÃO LIDO]` — a fonte existe, mas o servidor bloqueou a leitura automatizada; o valor vem de trecho de busca ou de fonte secundária e **não deve ser tratado como verificado**.

---

## 0. Tabela-resumo (alimenta `config/documentos.yaml`)

| # | Documento | Emissor | URL | Custo | validity_days | Alívio ME/EPP | Fonte |
|---|---|---|---|---|---|---|---|
| 1 | Comprovante de Inscrição e Situação Cadastral (cartão CNPJ) | RFB | https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp | R$ 0 | **UNVERIFIED** (RFB não fixa; editais costumam pedir ≤ 90 dias) | — | Lei 14.133 art. 68 I `[LEI]`; página RFB `[PLATAFORMA]` |
| 2 | Ato constitutivo (contrato social consolidado) + Certidão Simplificada JUCESP | JUCESP | https://www.jucesponline.sp.gov.br/ (Certidão Simplificada, IDProduto=4) | R$ 0 (online) | **UNVERIFIED** (JUCESP não fixa; editais costumam pedir ≤ 90 dias) | — | art. 66 `[LEI]`; JUCESP Online `[PLATAFORMA]` |
| 3 | Certidão Negativa de Débitos relativos a Créditos Tributários Federais e à Dívida Ativa da União (conjunta RFB/PGFN) | RFB + PGFN | https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir | R$ 0 | **180** `[NÃO LIDO]` — a própria certidão imprime "válida até"; o rastreador deve ler essa data | Prazo de cura LC 123 art. 43 §1º: 5 dias úteis + 5 | art. 68 III/IV `[LEI]`; gov.br serviço `[PLATAFORMA]`; Portaria Conjunta RFB/PGFN 1.751/2014 `[NÃO LIDO]` |
| 4 | Certidão Negativa de Débitos Tributários Não Inscritos (SEFAZ-SP) | SEFAZ-SP | https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx | não declarado na página (emissão automática; `[INFERÊNCIA]` R$ 0) | **180** (Portaria CAT-135/2014 art. 6º: "6 (seis) meses" salvo prazo fixado pelo órgão solicitante) | idem | art. 68 III `[LEI]`; Portaria CAT-135/2014 `[LEI]` |
| 5 | Certidão Negativa de Débitos Inscritos em Dívida Ativa (e-CRDA, PGE-SP) | PGE-SP | https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf | R$ 0 ("de forma automática e gratuita") | **UNVERIFIED** (site da PGE devolve HTTP 405 a leitura automatizada; a certidão emitida traz a própria validade) | idem | art. 68 III `[LEI]`; portal PGE `[PLATAFORMA]` |
| 6 | Certidão Conjunta de Débitos de Tributos Mobiliários (PMSP) | SF-PMSP | https://prefeitura.sp.gov.br/web/fazenda/w/servicos/certidoes/2394 | não declarado (`[INFERÊNCIA]` R$ 0) | **180** (Portaria SF 182/2021, via página "Validade das Certidões") | idem | art. 68 II/III `[LEI]`; páginas SF-PMSP `[PLATAFORMA]` |
| 7 | Certificado de Regularidade do FGTS (CRF) | CAIXA | https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf | R$ 0 (`[INFERÊNCIA]`: consulta pública) | **30** (Manual de Regularidade do Empregador v19, item 2.7.1) — renovável a partir do 5º dia anterior ao vencimento (2.7.2) | idem (art. 43 abrange "regularidade fiscal e trabalhista") | art. 68 IV `[LEI]`; Lei 8.036 art. 27 "a" `[LEI]`; Manual CAIXA `[PLATAFORMA]` |
| 8 | Certidão Negativa de Débitos Trabalhistas (CNDT) | TST | https://cndt-certidao.tst.jus.br/inicio.faces | R$ 0 (CLT art. 642-A: "expedida gratuita e eletronicamente") | **180** (CLT art. 642-A §4º) | idem | art. 68 V `[LEI]`; CLT 642-A `[LEI]` |
| 9 | Certidão de distribuição de Falências, Concordatas e Recuperações (TJSP) **+ complemento eproc** "Comarcas e Turmas Recursais (Primeiro Grau) – Cível" | TJSP | e-SAJ https://esaj.tjsp.jus.br/sco/abrirCadastro.do e https://certidoes.tjsp.jus.br/ (conta gov.br) | R$ 0 (Provimento CSM 2.356/2016; Comunicado SPI 47/2016) | **UNVERIFIED** (TJSP não fixa; SICAF adota 1 ano quando a certidão não traz validade; editais costumam pedir 90 dias) | — | art. 69 II `[LEI]`; TJSP `[PLATAFORMA]` |
| 10 | Balanço patrimonial + DRE (ou balanço de abertura) | contador da empresa (registro via ECD/SPED ou JUCESP) | — | honorários contábeis: **UNVERIFIED** | anual — SICAF: prazo da ECD | **Dispensado** para bens de pronta entrega: Decreto 8.538 art. 3º (âmbito federal); empresa nova: balanço de abertura (art. 65 §1º) | art. 69 I, art. 65 §1º `[LEI]`; Decreto 8.538 `[LEI]`; FAQ SICAF Q16/Q18 `[PLATAFORMA]` |
| 11 | Atestado de capacidade técnica (qualitativo) | cliente anterior (público ou privado) | — | R$ 0 | sem validade legal (o fato atestado não expira) | — | art. 67 II, §§1º-3º `[LEI]` |
| 12 | Declarações do edital (atende requisitos; art. 7º XXXIII CF; reserva de cargos PcD; custos trabalhistas na proposta; não impedimento/fato impeditivo; enquadramento ME/EPP; conhecimento das condições) | a própria licitante | preenchidas na plataforma / anexadas | R$ 0 | por certame (emitir a cada proposta) | Declaração ME/EPP é o gatilho dos arts. 42-49 LC 123 | art. 63 I, IV, §1º; art. 68 VI; art. 14; art. 67 VI `[LEI]`; Decreto 8.538 art. 13 §2º `[LEI]` |
| 13 | Declaração IN RFB 1.234/2012 Anexo IV (optante do Simples) | a própria licitante | ver `docs/LEGAL_FINDINGS.md` §1 | R$ 0 | por contrato (e por prorrogação), 2 vias, na assinatura | é o próprio alívio (dispensa de IRRF) | IN 1.234 art. 6º e §5º `[LEI]` (lido em LEGAL_FINDINGS) |
| 14 | Certificado digital e-CNPJ A1 (ICP-Brasil) | AC (Certisign, Soluti, Valid…) | ver §1.14 | **R$ 219,90 – 274,90** (Certisign); R$ 235,00 (Soluti); R$ 203,00–257,20 (Valid, combo) | **365** (12 meses) | — | páginas das ACs `[PLATAFORMA]` |
| 15 | Inscrição estadual (Cadesp) e inscrição municipal (CCM) | SEFAZ-SP / SF-PMSP | — | R$ 0 | sem validade | — | art. 68 II `[LEI]` |
| 16 | SICAF — Certificado de Registro Cadastral (nível I obrigatório para pregão eletrônico) | MGI / Compras.gov.br | https://www3.comprasnet.gov.br/sicaf-web/index.jsf | R$ 0 ("O SICAF é e continuará sendo gratuito") | **365**, renovação automática se CNPJ válido na RFB (IN SEGES 3/2018 art. 18) — mas as certidões mantêm as próprias validades (art. 18 §2º) | — | IN 3/2018 `[LEI]`; FAQ SICAF `[PLATAFORMA]` |

**Menor validade do pacote: 30 dias (CRF/FGTS).** É a cadência em que o sistema inteiro tem de rodar. Detalhe operacional que reduz o risco: a CAIXA permite renovar a partir do 5º dia antes do vencimento, então a janela útil é de ~25 dias.

---

## 1. PARTE 1 — O pacote de habilitação (Lei 14.133 arts. 62-70)

### 1.0 O que a lei diz sobre *quando* os documentos são exigidos `[LEI]`
Texto lido em <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm>.

- **Art. 62** divide a habilitação em jurídica, técnica, fiscal-social-trabalhista e econômico-financeira.
- **Art. 63, II e III:** "será exigida a apresentação dos documentos de habilitação **apenas pelo licitante vencedor**"; os de regularidade fiscal "somente em momento posterior ao julgamento das propostas, e apenas do licitante mais bem classificado". → No dia da sessão ela só precisa das **declarações** e da proposta; o pacote é cobrado **depois de ganhar**. É exatamente aí que a validade mata: a certidão precisa estar válida na data em que o pregoeiro a convoca, dias após a sessão.
- **Art. 64, II:** admite diligência para "atualização de documentos cuja validade tenha expirado **após** a data de recebimento das propostas". → Se a certidão estava válida na entrega da proposta e venceu depois, a lei manda aceitar a atualização. Se já estava vencida na entrega, não há socorro.
- **Art. 65 §1º:** empresas criadas no exercício financeiro da licitação "ficarão autorizadas a substituir os demonstrativos contábeis pelo **balanço de abertura**".
- **Art. 70, II e III:** a documentação pode ser substituída por registro cadastral (SICAF) previsto no edital, e **dispensada, total ou parcialmente, nas contratações para entrega imediata e nas de valor inferior a 1/4 do limite de dispensa para compras em geral**. O limite atualizado do art. 75 II é **R$ 65.492,11** (Decreto 12.807/2025, Anexo, lido em <https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/D12807.htm>) → 1/4 = **R$ 16.373,03**.
- **Art. 92, XVI:** o contrato obriga a "manter, durante toda a execução do contrato, (...) todas as condições exigidas para a habilitação". → As certidões continuam sendo cobradas a cada **pagamento**. O rastreador não pode parar quando o contrato é assinado.

### 1.1 Alívio ME/EPP — o que vale e onde `[LEI]`
- **Lei 14.133 art. 4º:** "Aplicam-se às licitações e contratos disciplinados por esta Lei as disposições constantes dos arts. 42 a 49 da Lei Complementar nº 123".
- **LC 123 art. 42** (redação LC 155/2016): "a comprovação de regularidade **fiscal e trabalhista** das microempresas (...) somente será exigida para efeito de assinatura do contrato". <https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm>
- **LC 123 art. 43 caput:** a ME apresenta toda a documentação "mesmo que esta apresente alguma restrição". **§1º:** "prazo de **cinco dias úteis**, cujo termo inicial corresponderá ao momento em que o proponente for declarado vencedor do certame, **prorrogável por igual período**, a critério da administração pública, para regularização da documentação". **§2º:** não regularizar = decadência do direito à contratação.
  - Atenção: o texto original (2 dias úteis) ainda aparece na página do Planalto como redação histórica; a vigente é 5 + 5.
  - Escopo: só **fiscal e trabalhista** (itens 3-8 da tabela). Não cobre falência, balanço, atestado, ato constitutivo.
- **Decreto 8.538/2015** <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/decreto/d8538.htm>: **art. 1º §1º** limita o decreto à administração pública **federal**. Ou seja, num pregão municipal ele não vincula o pregoeiro; o que vincula é a LC 123 diretamente (art. 47 parágrafo único: "enquanto não sobrevier legislação estadual, municipal ou regulamento específico de cada órgão mais favorável (...), aplica-se a legislação federal"). Na prática os editais municipais copiam o decreto. `[INFERÊNCIA]`
  - **Art. 3º:** "Na habilitação em licitações para o fornecimento de bens para **pronta entrega** ou para a locação de materiais, não será exigida da microempresa ou da empresa de pequeno porte a apresentação de balanço patrimonial do último exercício social."
  - **Art. 4º §1º-§2º:** repete os 5 + 5 dias úteis; no pregão o prazo conta "da divulgação do resultado da fase de habilitação".
  - **Art. 13 §2º:** "Deverá ser exigida do licitante a ser beneficiado a **declaração**, sob as penas da lei, de que cumpre os requisitos legais para a qualificação como microempresa" — é a declaração de enquadramento do item 12.
  - A FAQ normativa do SICAF (Q18) aplica o art. 3º e acrescenta o limite: "a ata decorrente de Sistema de Registro de Preços **não é considerada pronta entrega**, caso em que deve ser exigido o balanço patrimonial da ME/EPP". <https://www.gov.br/compras/pt-br/acesso-a-informacao/perguntas-frequentes/sicaf-normativo> `[PLATAFORMA]` → **Pregões SRP de kits (a maioria) exigirão balanço mesmo de ME.** Não conte com a dispensa.

### 1.2 Documento a documento

#### 1. Cartão CNPJ — art. 68 I
- Emissão: <https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp> (página "Emissão de Comprovante de Inscrição e de Situação Cadastral", lida). Gratuito.
- Validade: **UNVERIFIED** — a RFB não fixa. O SICAF puxa os dados do CNPJ automaticamente (IN 3/2018 art. 11 §1º; manual normativo). Editais costumam exigir emissão ≤ 90 dias `[INFERÊNCIA]`. Para o rastreador: reemitir a cada 30 dias junto com o CRF custa zero e elimina a dúvida.

#### 2. Ato constitutivo — art. 66
- "A documentação a ser apresentada (...) limita-se à comprovação de existência jurídica da pessoa e, quando cabível, de autorização para o exercício da atividade" (art. 66). Para uma LTDA/SLU: contrato social consolidado + alterações, registrados na JUCESP.
- **Certidão Simplificada JUCESP:** o JUCESP Online (<https://www.jucesponline.sp.gov.br/faq.aspx>, lido) diz que emite "**gratuitamente**, certidão com extrato de informações atualizadas constantes de atos" (Certidão Simplificada). Não há validade fixada pela JUCESP: **UNVERIFIED**; editais costumam pedir ≤ 90 dias `[INFERÊNCIA]`. Emitir junto com o ciclo de 30 dias.

#### 3. Certidão conjunta RFB/PGFN — art. 68 III e IV
- Página de serviço gov.br (lida): <https://www.gov.br/pt-br/servicos/emitir-certidao-de-regularidade-fiscal-perante-a-fazenda-nacional> — "Este serviço é gratuito para o cidadão"; emissão PJ em <https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/Emitir>; tipos CND / CPEND / CPD; base legal: CTN arts. 205-206, **Portaria Conjunta RFB/PGFN nº 1.751/2014**. O modelo oficial da certidão (Anexo, PDF lido em normas.receita.fazenda.gov.br) traz "Certidão emitida gratuitamente com base na Portaria Conjunta RFB/PGFN nº 1.751, de 2/10/2014" e "válida para o estabelecimento matriz e suas filiais".
- Validade: **180 dias `[NÃO LIDO]`**. A página "Prazos" da PGFN (<https://www.gov.br/pgfn/pt-br/servicos/orientacoes-contribuintes/certidoes-de-regularidade-fiscal/prazos>) devolveu "Conteúdo Restrito"/404 à leitura automatizada e o texto da Portaria 1.751 no sistema Normas da RFB é servido apenas por JavaScript. O trecho de busca dessa página diz "180 (cento e oitenta) dias (...) Portaria MF nº 358/2014". **O que resolve:** abrir a certidão emitida — ela imprime "Válida até". O rastreador deve ler a data do documento, não assumir 180.
- Abrange previdência (contribuições sociais) — atende ao art. 68 IV "Seguridade Social".

#### 4. SEFAZ-SP — Certidão Negativa de Débitos Tributários Não Inscritos — art. 68 III
- Emissão: <https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx> (lida; "Base Legal: Portaria CAT-135, de 18/12/2014"; "Sistema disponível em dias úteis das 06:00 às 21:00").
- **Portaria CAT-135/2014** (lida em <https://legislacao.fazenda.sp.gov.br/Paginas/pcat1352014.aspx>): art. 1º — emitida pelo endereço eletrônico; **art. 6º — "Não existindo prazo fixado pelo órgão solicitante, a validade da certidão será de 6 (seis) meses, contados da data de sua expedição."** → 180 dias para o rastreador (6 meses de calendário podem ser 181-184 dias; usar 180 é conservador). Se o edital fixar outro prazo, o edital prevalece.
- Custo: a página não declara; emissão é automática. `[INFERÊNCIA]` gratuita.

#### 5. PGE-SP — e-CRDA (débitos inscritos em dívida ativa) — art. 68 III
- Editais paulistas exigem as **duas** certidões estaduais (não inscritos SEFAZ + inscritos PGE). `[INFERÊNCIA]` a partir do desenho institucional; a PGE explica a divisão em <https://www.portalcms.pge.sp.gov.br/pge/servicos-ao-cidadao/servicos-fiscais/certidoes-regularidade> (lida): "o documento pode ser gerado de forma **automática e gratuita** através do link de Solicitação de Certidão Negativa".
- Emissão: <https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf>.
- Validade: **UNVERIFIED.** O site da PGE (JSF) devolveu HTTP 405 a todas as tentativas (curl com UA de navegador e WebFetch), inclusive o "Manual de Certidão de Débitos" em PDF. **O que resolve:** emitir uma e-CRDA e ler o campo de validade impresso; ou abrir o FAQ <https://www.dividaativa.pge.sp.gov.br/sc/pages/duvidas/faq.jsf?param=4867> num navegador.

#### 6. PMSP — Certidão Conjunta de Débitos de Tributos Mobiliários — art. 68 II e III
- Serviço (lido): <https://prefeitura.sp.gov.br/web/fazenda/w/servicos/certidoes/2394> — "certidão unificada por CPF/CNPJ raiz"; "Para pessoas jurídicas a certidão somente é emitida através do CNPJ raiz, tendo validade para todos os seus estabelecimentos no Município"; "Certidão Negativa: emissão em até 10 dias, contados do pedido ou da solução das pendências". Pressupõe inscrição no CCM (art. 68 II).
- Validade: página "Validade das Certidões de Tributos Imobiliários e Mobiliários" (lida, <https://prefeitura.sp.gov.br/web/fazenda/w/servicos/certidoes/28638>): "As novas certidões negativas emitidas a partir de 05 de agosto de 2021 voltam a ter prazo de validade de **180 dias**" (Portaria SF nº 182/2021). Idem na notícia <https://capital.sp.gov.br/web/fazenda/w/noticias/29937>.
- **Risco operacional:** "emissão em até 10 dias" quando há pendência — não dá para deixar para o dia da convocação.

#### 7. CRF/FGTS — art. 68 IV; Lei 8.036 art. 27 "a"
- **Lei 8.036/1990 art. 27** (lida, <https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm>): "A apresentação do Certificado de Regularidade do FGTS (...) é obrigatória nas seguintes situações: a) habilitação e licitação promovida por órgão da Administração Federal, Estadual e Municipal".
- Consulta/emissão: <https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf> (lida).
- **Validade: 30 dias.** Manual de Orientações — Regularidade do Empregador v19, CAIXA, vigência 08/01/2026, item **2.7.1**: "O CRF é válido em todo o território nacional pelo prazo de 30 dias contados da data de sua emissão." Item **2.7.2**: "renovável a partir do quinto dia anterior ao seu vencimento". <https://www.caixa.gov.br/Downloads/fgts-manuais-e-cartilhas-operacionais/Manual_de_Regularidade_do_Empregador_v19.pdf> `[PLATAFORMA]`
- Empresa sem empregados: ainda precisa do CRF; a situação "regular" sem recolhimentos existe, mas exige o cadastro do empregador (Conectividade Social / FGTS Digital). `[INFERÊNCIA]` — o manual não trata de PJ sem empregado explicitamente; **o que resolve:** emitir o CRF uma vez e ver se sai.

#### 8. CNDT — art. 68 V
- **CLT art. 642-A** (Lei 12.440/2011, lida em <https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12440.htm> e no texto consolidado da CLT): "expedida **gratuita e eletronicamente**"; §3º "certificará a empresa em relação a todos os seus estabelecimentos"; **§4º "O prazo de validade da CNDT é de 180 (cento e oitenta) dias, contado da data de sua emissão."**
- Emissão: <https://cndt-certidao.tst.jus.br/inicio.faces> (lida: "documento indispensável à participação em licitações públicas").

#### 9. Certidão de falência/recuperação — art. 69 II
- Texto: "certidão negativa de feitos sobre falência expedida pelo distribuidor da sede do licitante".
- TJSP (lido, <https://www.tjsp.jus.br/Certidoes>): "Certidão de Falências, Concordatas e Recuperações – O pedido é feito pela internet. (...) **A partir de 05/11/2025, esta certidão deverá ser complementada com a certidão COMARCAS E TURMAS RECURSAIS (Primeiro Grau) – CÍVEL, emitida pelo sistema eproc**" — esta segunda em <https://certidoes.tjsp.jus.br/> com **conta gov.br**. "Prazo: até 5 dias." → **São dois documentos, não um.** Um edital que peça "certidão de falência do distribuidor da sede" será satisfeito só com o par. `[INFERÊNCIA]` quanto ao rigor do pregoeiro; o TJSP é explícito quanto ao complemento.
- Custo: **R$ 0** — Comunicado SPI 47/2016 (lido, <https://www.tjsp.jus.br/PrimeiraInstancia/Comunicados/Comunicado?codigoComunicado=7719>): "O Provimento CSM nº 2356/2016 estabeleceu a gratuidade para expedição das certidões cíveis em geral (...) Todas as certidões expedidas pelo Tribunal de Justiça serão fornecidas gratuitamente".
- Validade: **UNVERIFIED** — o TJSP não fixa. O SICAF (FAQ normativo Q21): "Quando não constar a data de validade da Certidão de Falência e Concordata, deve-se adotar o período de 1 (um) ano." Editais costumam pedir 90 dias `[INFERÊNCIA]`. Para o rastreador: 90 dias é o pior caso razoável; marcar como `edital_may_override`.

#### 10. Balanço patrimonial — art. 69 I e §6º; art. 65 §1º
- Regra: "balanço patrimonial, demonstração de resultado de exercício e demais demonstrações contábeis dos 2 (dois) últimos exercícios sociais" (art. 69 I); "limitar-se-ão ao último exercício no caso de a pessoa jurídica ter sido constituída há menos de 2 (dois) anos" (§6º); empresa criada no exercício: **balanço de abertura** (art. 65 §1º). Vedado exigir faturamento mínimo (§2º); permitido capital/PL mínimo de até 10% do valor estimado nas compras para entrega futura (§4º) — SRP é entrega futura `[INFERÊNCIA]`.
- SICAF (FAQ normativo, lido): Q15 — o prazo de atualização "segue o prazo limite definido pela RFB para transmissão da ECD ao SPED"; Q16 — "podem ser registrados (...) o balanço de abertura, intermediário e anual"; Q17 — autenticação pelo recibo da ECD ou, para quem não é obrigado à ECD, "cópia digitalizada do Balanço Patrimonial autenticado pela junta comercial".
- Alívio ME/EPP: Decreto 8.538 art. 3º (pronta entrega) — ver §1.1 e a ressalva do SRP.
- Custo: honorários do contador — **UNVERIFIED**.

#### 11. Atestado de capacidade técnica — art. 67
- **Art. 67 II:** "certidões ou atestados (...) que demonstrem capacidade operacional na execução de serviços similares de complexidade tecnológica e operacional equivalente ou superior". **§1º:** exigência restrita às parcelas de maior relevância (≥ 4% do valor estimado). **§2º:** "será admitida a exigência de atestados com **quantidades mínimas de até 50%** das parcelas (...), **vedadas limitações de tempo e de locais específicos**". **§3º:** fora de obras/engenharia, a Administração pode substituir por "outra prova de que (...) a empresa possui conhecimento técnico e experiência prática", nas formas previstas em regulamento.
- **O que é um atestado QUALITATIVO:** um documento, emitido por pessoa jurídica de direito público ou privado, que declara que a licitante forneceu bens compatíveis com o objeto (ex.: "kits de enxoval para recém-nascido") **sem exigir quantidade mínima**. O art. 67 não restringe o emissor a órgão público, não impõe forma e proíbe limite de tempo (§2º). Uma única venda anterior, de qualquer tamanho, atende — é o que `config/rules.yaml` rule_2 já assume.
- **Como uma empresa sem histórico obtém o primeiro:**
  1. **Venda privada** (maternidade, creche, ONG, empresa que dá kit a funcionárias) → pedir ao comprador uma declaração em papel timbrado, com CNPJ, descrição do objeto, período e "cumpriu satisfatoriamente". A lei aceita (art. 67 II não distingue emissor; §4º admite até entidade estrangeira). `[LEI + INFERÊNCIA]`
  2. **Primeira venda pública sem atestado:** (a) editais que não exigem qualificação técnica (2 dos 5 medidos em rules.yaml); (b) **contratação direta** por dispensa (art. 75 II, até R$ 65.492,11) ou pregão de valor **< R$ 16.373,03** (1/4 do limite), onde o art. 70 III permite dispensar a habilitação total ou parcialmente; (c) contratações para **entrega imediata** (art. 70 III). Depois da primeira entrega, pedir o atestado ao município (o art. 88 §3º prevê que o contratante "emitirá documento comprobatório da avaliação realizada").
  3. **O cadastro de atesto do PNCP (art. 88 §4º) não existe ainda** — o FAQ do PNCP lista "cadastro de atesto de cumprimento de obrigações" entre funcionalidades que o portal "deverá" disponibilizar. `[PLATAFORMA]`
- Fonte do TCU: a página <https://licitacoesecontratos.tcu.gov.br/> respondeu com captcha ("This question is for testing whether you are a human visitor") — **não lida**. Nada nesta seção depende dela.

#### 12. Declarações — tudo com base no texto da lei
| Declaração | Base | Observação |
|---|---|---|
| Atende aos requisitos de habilitação | art. 63 I | "o declarante responderá pela veracidade" |
| Cumpre reserva de cargos PcD/reabilitado | art. 63 IV | exigida "do licitante" — mesmo sem empregados (a cota só incide a partir de 100 empregados; a declaração é de cumprimento das exigências "previstas em lei") `[INFERÊNCIA]` |
| Proposta compreende integralidade dos custos trabalhistas | art. 63 §1º | "sob pena de desclassificação" — é de desclassificação, não de inabilitação |
| Não emprega menor (CF art. 7º XXXIII) | art. 68 VI | |
| Não impedimento / inexistência de fato impeditivo | art. 14 (rol de impedidos), art. 156 (sanções) | editais chamam de "declaração de inexistência de fato impeditivo" `[INFERÊNCIA]` — ver CEIS/CNEP no PNCP |
| Enquadramento ME/EPP | LC 123 art. 3º; Decreto 8.538 art. 13 §2º | é o gatilho do empate ficto (art. 44-45 LC 123) e da cura de 5 dias |
| Conhecimento das condições locais | art. 67 VI | irrelevante para bens; muitos editais mantêm |
| Declaração de responsabilidade / veracidade dos documentos | prática de edital | `[INFERÊNCIA]` |

Todas são **por certame** (validity = 0 no YAML: emitir a cada proposta). No Compras.gov.br são marcadas em tela no envio da proposta `[INFERÊNCIA — não verificado nesta sessão]`.

#### 13. IN RFB 1.234/2012 Anexo IV
Já documentado com fontes lidas em `docs/LEGAL_FINDINGS.md` §1: art. 6º — "no ato da assinatura do contrato (...) Anexos II, III ou IV (...) em 2 (duas) vias"; §5º — "a cada novo contrato" e a cada prorrogação; SC COSIT 61/2020 — a consulta ao portal do Simples só substitui a declaração na etapa de pagamento. `required_for: contract, payment`.

#### 14. Certificado digital e-CNPJ A1
- Para que serve aqui: acesso ao SICAF por certificado (FAQ SICAF-sistema Q1/Q4: "O SICAF aceita certificados do tipo A1 (Pessoa Jurídica - e-CNPJ) e A3 (Pessoa Física - e-CPF)"), assinatura de propostas/contratos, NF-e. **Mas** a página de serviço gov.br do SICAF (lida) diz que basta "selo de confiabilidade verificado" gov.br (prata ou ouro) **ou** certificado digital — ver Parte 3.
- Preços lidos nas páginas das ACs (19/09/2026):
  - **Certisign** <https://www.certisign.com.br/>: "e-CNPJ A1 — Válido por 12 meses — R$ 274,90 à vista"; "e-CNPJ PME A1 — Para pequenas/médias empresas — R$ 219,90 à vista".
  - **Soluti** <https://www.soluti.com.br/certificado-digital/e-cnpj>: "CERTIFICADO PJ A1 — R$ 235,00".
  - **Valid** <https://www.validcertificadora.com.br/>: "e-CNPJ A1 + e-CPF Nuvem 4 Meses (Combo) — R$ 203,00 (preço normal R$ 257,20)".
  - **Serasa:** todas as páginas devolveram 403; o índice do site tem título "Encerramento"; a busca reporta comunicado ao ITI (fev/2024) de saída do mercado ICP-Brasil, sem novas emissões desde 06/05/2024. `[NÃO LIDO]` — **não contar com a Serasa**.
- Validade: 12 meses (A1). Custo recorrente anual.

#### 15. Inscrições estadual e municipal — art. 68 II
"inscrição no cadastro de contribuintes estadual e/ou municipal, se houver, relativo ao domicílio ou sede do licitante, pertinente ao seu ramo de atividade e compatível com o objeto contratual". Comércio de bens → IE (Cadesp) e CCM. Sem validade; comprovadas por consulta pública.

---

## 2. PARTE 2 — As plataformas

### 2.0 O que a Lei 15.266/2025 mudou — e o que NÃO mudou `[LEI]`
Texto lido em <https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15266.htm> (DOU 24/11/2025, vigência imediata).

- **Art. 87 caput** (nova redação): "os órgãos e entidades (...) deverão utilizar o sistema de registro cadastral unificado disponível no PNCP, para efeito de cadastro unificado de **licitantes e de contratados**, na forma estabelecida em **regulamento do Poder Executivo federal**." Antes: "de licitantes, na forma disposta em regulamento". Duas mudanças: alcança contratados; a competência regulamentar passa a ser explicitamente federal (acaba a tese de regulamento por ente).
- **Art. 87 §2º não foi alterado.** Continua: "É proibida a exigência, pelo órgão ou entidade licitante, de registro cadastral complementar para acesso a edital e anexos." (A pergunta original atribuía a reescrita ao §2º; foi o caput.)
- **Art. 175 §1º** (nova redação): "Desde que mantida a integração com o PNCP, as contratações poderão ser realizadas por meio de sistema eletrônico fornecido por pessoa jurídica de **direito público ou privado**, na forma de **regulamento do Poder Executivo federal**." → As plataformas privadas (BLL, BNC, Licitanet, PCP) passam a depender de regulamento federal para operar.
- **Art. 79 IV + §1º VII:** cria o **Sicx** (comércio eletrônico); admissão de fornecedores "observado o disposto no art. 87".
- **Decreto 13.106/2026** (lido, <https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d13106.htm>, vigência 08/09/2026) regulamenta o **Sicx** (art. 79 IV), não o art. 87. Mas: **art. 5º** "O acesso pelos fornecedores ao Sicx (...) será realizado por meio de integração com o registro cadastral unificado"; **art. 10 §1º** habilitação "comprovada por meio do registro cadastral unificado, de que trata o art. 87"; **art. 33 §1º** condições para integrar plataformas privadas (integração com o registro unificado e o PNCP, aplicação dos arts. 42-49 da LC 123…); **art. 35 (transitório):** "Os fornecedores deverão manter seus dados cadastrais atualizados no **SICAF**, na hipótese de não haver integração com o registro cadastral unificado."
- **Estado hoje (19/09/2026):** o FAQ do PNCP (lido, <https://www.gov.br/pncp/pt-br/pncp/perguntas-e-respostas>) ainda lista "sistema de registro cadastral unificado" entre o que o PNCP "**deverá** (...) disponibilizar", e lista o SICAF entre os "Sistemas Federais de Logística Pública Integrados ao PNCP". Não localizei decreto regulamentando o art. 87 (busca no Planalto e gov.br). **Conclusão:** não existe cadastro de fornecedor no PNCP para ela fazer; o SICAF é o cadastro unificado de fato; cada plataforma privada mantém o próprio cadastro. **O que resolve:** publicação do decreto do art. 87 — monitorar planalto.gov.br/_ato2023-2026/2026/decreto e o FAQ do PNCP.
- **O que muda para os cadastros dela:** nada hoje. Quando o registro unificado sair, o art. 87 §2º + art. 10 §2º do Decreto 13.106 apontam para "um cadastro, todas as plataformas" — mas as plataformas privadas continuarão cobrando pelo *uso* (o §2º proíbe exigir cadastro complementar para **acessar edital**, não proíbe taxa de participação). `[INFERÊNCIA]`

### 2.1 Compras.gov.br (federal; muitos municípios usam)
- Cadastro de fornecedor = **SICAF nível I (credenciamento)** — IN SEGES 3/2018 art. 9º: "o credenciamento é o nível básico do registro cadastral no Sicaf que permite a participação dos interessados na modalidade licitatória Pregão, em sua forma eletrônica, bem como na Dispensa Eletrônica". Ver Parte 3.
- URL: <https://www.gov.br/compras/pt-br/sistemas/sicaf-digital> → sistema <https://www3.comprasnet.gov.br/sicaf-web/index.jsf>; login do fornecedor via gov.br.
- Custo: **R$ 0** para cadastrar e para participar (FAQ SICAF-sistema: "O SICAF é, e continuará sendo, gratuito!"; página: "100% digital e GRATUITO").
- Certificado: FAQ SICAF-sistema Q1 "Sim. O fornecedor deverá possuir certificado digital (...) ICP-Brasil"; **porém** a página de serviço gov.br (lida, <https://www.gov.br/pt-br/servicos/cadastrar-se-como-fornecedor-da-administracao-publica>) diz "Qualquer pessoa com acesso ao Gov.br e que possua selo de confiabilidade verificado, além do certificado digital ou certificado em nuvem" e, nas etapas, "selo de confiabilidade (prata ou superior) **ou** certificação digital". As duas fontes são do MGI; a de serviço é a mais recente (FAQ cita "Portal de Compras... com emprego do certificado digital", redação da migração 2018). **Tratar o e-CNPJ como necessário na prática** (assinatura de contrato, NF-e) mas o SICAF em si pode abrir com conta gov.br prata/ouro. `[INFERÊNCIA sobre precedência]`
- Treinamento: FAQ "5. Existe algum ambiente de treinamento?" (lida, <https://www.gov.br/compras/pt-br/acesso-a-informacao/perguntas-frequentes/contratos/utilizacao-do-sistema/5-existe-algum-ambiente-de>): "Sim. O link para o ambiente de treinamento é https://treina.contratos.comprasnet.gov.br/login" (esse é o Contratos.gov.br). O menu do portal lista "Compras.gov.br Treinamento" → <https://treinamento.comprasnet.gov.br/seguro/loginPortal.asp> (lida: tela de login "Faça o Login no Compras.gov.br", com "Quero me Cadastrar").

### 2.2 Portal de Compras Públicas (PCP)
- Cadastro: <https://www.portaldecompraspublicas.com.br/cadastre-se> (lida; aceita "Pessoa Física, MEI, ME, EPP, LTDA…"). Cadastro gratuito; "aviso de licitações gratuito".
- Preços (página de adesão lida, <https://www.portaldecompraspublicas.com.br/adesao/fornecedor>): **Mensal R$ 165,00/mês**; **Anual R$ 1.650,00** (= R$ 137,50/mês); **Crédito R$ 129,00 por processo** ("1 crédito para usar em qualquer tipo de processo com validade de 30 dias, pagamento somente por cartão"). Todos os planos incluem "Participação de cotações e dispensas de licitação" e "Treinamento ao vivo com ambiente exclusivo de testes".
- **Não é gratuito para dar lance.** A página justifica: "o Portal cobra uma taxa de ressarcimento pelo uso da plataforma, prevista em lei (Art. 62 da Lei 14.133/21)". O art. 62 trata de habilitação, não de taxas — a citação está errada; a cobrança se sustenta em jurisprudência do TCU sobre plataformas privadas, não nesse artigo. `[LEI + INFERÊNCIA]`
- Certificado digital: não mencionado nas páginas lidas — **UNVERIFIED**. Central de ajuda (Zendesk) devolveu 403.

### 2.3 BLL Compras
- Cadastro: <https://bllcompras.com/Home/Login>; informações em <https://bll.org.br/para-fornecedor/> (lida): "Cadastro gratuito — R$ 0,00 para se cadastrar"; "Plano Trimestral — R$ 630,00 / trimestre — A partir de 13/07/2026"; plano por êxito "1,5% limitado ao teto máximo de R$ 600,00 por lote".
- **Regulamento BLL 2026** (PDF lido, <https://bll.org.br/wp-content/uploads/2026/07/Regulamento-BLL-2026.pdf>), art. 17 II "Plano Taxa Variável: Apenas o licitante vencedor será responsável pelo pagamento da taxa de sucesso. A cobrança será de 1,5% (...) sobre o valor do lote adjudicado, limitada ao teto máximo de R$ 600,00 (...) por lote, quando o valor do lote for superior a R$ 40.000,00 (...), após a adjudicação." §1º "a cobrança será devida a partir do cadastro da proposta". §2º-§4º: vencimento em 45 dias (contrato de aquisição) ou parcelado pelo prazo de entrega/vigência da ata (SRP: 1ª parcela em 60 dias). §5º: em pregão por maior desconto, valores fixos R$ 600 / 1.200 / 1.300 por 1 / 2 / 3+ lotes. Art. 18: "Em nenhuma hipótese a cobrança será realizada com base no valor empenhado".
  - **Confirmado:** 1,5% com teto R$ 600, só no êxito. **Nuance:** o teto R$ 600 opera quando o lote > R$ 40.000; abaixo disso paga 1,5% do lote (matematicamente < R$ 600, coerente). Em SRP a taxa incide sobre o **lote adjudicado da ata**, não sobre o que for efetivamente empenhado (art. 18 diz o inverso do que se poderia esperar: cobra sobre o adjudicado, nunca sobre o empenhado). Para o modelo de margem: em ata de R$ 100 mil que executa 30%, a taxa é R$ 600 sobre os R$ 30 mil realizados = 2%. `[INFERÊNCIA aritmética]`
- Certificado digital: não mencionado — **UNVERIFIED**.
- Treinamento: "Capacitação gratuita", BLL Academy <https://bll.org.br/bll-academy/>.

### 2.4 BNC — Bolsa Nacional de Compras
- Cadastro: <https://bnc.org.br/cadastro/> → sistema <https://bnccompras.com/Home/Login>. Home (lida): "Cadastro gratuito"; "Planos para fornecedores — R$ 118,80 — Plano de única participação"; "Participação avulsa por processo, com pagamento posterior"; "Planos de participação pós-pago".
- **Regulamento BNC 2026** (PDF lido, <https://bnc.org.br/wp-content/uploads/2026/07/Regulamento-BNC-2026.pdf>), art. 24: Plano A "Por participação — o licitante terá o valor do plano cobrado para cada proposta cadastrada (...) A não participação efetiva no edital não anula a cobrança"; Plano B mensal; Plano C trimestral. Preços de B e C não constam no regulamento nem na home — **UNVERIFIED**. Treinamentos "disponibilizados gratuitamente". Multa de 2% + 1% a.m. por atraso.
- **Não é gratuito para dar lance**: R$ 118,80 por processo, cobrado mesmo sem lance efetivo (basta cadastrar proposta).
- Certificado digital: não mencionado — **UNVERIFIED**.

### 2.5 Licitanet
- <https://licitanet.com.br/> é uma aplicação JavaScript (Vite); WebFetch devolveu 403; curl trouxe apenas a casca (2-4 KB) para /, /fornecedor, /planos, /regulamento, /termos-de-uso; o portal legado <https://portal.licitanet.com.br/regulamento.php> devolve uma tela de login. **Nada de preço foi lido em fonte própria.** Trechos de busca da própria Licitanet falam em "planos de assinatura de participação única, mensal, trimestral, semestral e anual" e em não cobrar dos órgãos. **UNVERIFIED** para preço, certificado e treinamento. **O que resolve:** abrir <https://licitanet.com.br/fornecedor> num navegador.

### 2.6 Outras plataformas
Não medi quais outras plataformas são proeminentes em pregões municipais. **O que resolve:** o próprio `harvest/` do repositório — o PNCP expõe o sistema de origem de cada compra; contar a distribuição nos editais já colhidos vale mais que qualquer lista publicada.

### 2.7 Quadro de custos de plataforma
| Plataforma | Cadastrar | Dar lance | Ganhar | Fonte |
|---|---|---|---|---|
| Compras.gov.br / SICAF | R$ 0 | R$ 0 | R$ 0 | FAQ SICAF `[PLATAFORMA]` |
| BLL | R$ 0 | R$ 0 (plano êxito) | 1,5% do lote, teto R$ 600 | Regulamento 2026 `[PLATAFORMA]` |
| BNC | R$ 0 | R$ 118,80 por processo (pós-pago) | — | home + Regulamento `[PLATAFORMA]` |
| PCP | R$ 0 | R$ 129 por processo, ou R$ 165/mês, ou R$ 1.650/ano | — | página de adesão `[PLATAFORMA]` |
| Licitanet | UNVERIFIED | UNVERIFIED (planos pagos) | UNVERIFIED | não lido |

---

## 3. PARTE 3 — SICAF

### 3.1 Norma
**IN SEGES/MP nº 3/2018** (lida, <https://www.gov.br/compras/pt-br/acesso-a-informacao/legislacao/instrucoes-normativas/instrucao-normativa-no-3-de-26-de-abril-de-2018>), alterada pelas IN 10/2020 e 107/2020; listada como vigente na página "Legislação por tema — SICAF" (15/08/2024). Base: Decreto 3.722/2001. Observação: a IN ainda referencia os arts. 27-31 da Lei 8.666; não foi reescrita para a 14.133 — os níveis mapeiam 1:1 para os arts. 66-69. `[INFERÊNCIA]`

### 3.2 Passo a passo (gov.br serviço + Manual Normativo, ambos lidos)
1. Conta **gov.br** com selo **prata ou ouro** (ou certificado digital ICP-Brasil e-CNPJ/e-CPF).
2. Acessar <https://www.gov.br/compras/pt-br> → "Fornecedor" → "Cadastre-se aqui" (serviço gov.br: tempo estimado ~10 min).
3. **Nível I – Credenciamento:** informar CNPJ; o sistema puxa da RFB razão social, CNAE, natureza jurídica, porte, QSA (FAQ Q2). Clicar "Credenciar". Só isso já permite participar de pregão eletrônico e dispensa eletrônica (IN art. 9º). Emite-se o **CRC** (Certificado de Registro Cadastral).
4. **Nível II – Habilitação jurídica:** upload do ato constitutivo (limite 15 MB por documento — FAQ sistema).
5. **Nível III – Regularidade fiscal federal e trabalhista:** **automático** — IN art. 11 §1º: "obtida por meio do compartilhamento de informações entre os órgãos responsáveis"; Manual Normativo: "certidões correspondentes à regularidade fiscal federal e trabalhista, obtidas por compartilhamento de dados entre órgãos"; FAQ Q2: o sistema integra "certidões de cunho fiscal e trabalhista, da seguridade social e do FGTS". → RFB/PGFN, FGTS e CNDT são validados pelo próprio SICAF.
6. **Nível IV – Regularidade estadual e municipal:** **upload manual** das certidões SEFAZ-SP, PGE-SP e PMSP (IN art. 12; não há compartilhamento).
7. **Nível V – Qualificação técnica:** upload de atestados (opcional; o edital pode pedir direto).
8. **Nível VI – Econômico-financeira:** balanço (IN art. 16; prazo da ECD — FAQ Q15) e certidão de falência (FAQ Q21: adotar 1 ano se sem validade). Calculadora de índices: <https://tutoriais.comprasgovernamentais.gov.br/calculadora/>.
9. Quem acessa: qualquer sócio do QSA, ou o "responsável pelo cadastro", ou o responsável pela PJ na RFB (FAQ sistema Q2-Q3).

### 3.3 O que o SICAF valida sozinho vs. o que ela mantém
| Automático (compartilhamento) | Manual (upload, com validade própria) |
|---|---|
| Dados do CNPJ (RFB) | Ato constitutivo (nível II) |
| Certidão conjunta RFB/PGFN | Certidões estadual (SEFAZ + PGE) e municipal (nível IV) |
| CRF/FGTS | Atestados (nível V) |
| CNDT | Balanço e certidão de falência (nível VI) |

### 3.4 Renovação
- **IN art. 18:** "O registro cadastral no Sicaf, bem como a sua renovação, será válido em âmbito nacional pelo prazo de **um ano**." **§1º:** "A manutenção cadastral será realizada **automaticamente** pelo Sistema, desde que o cadastrado encontre-se com o CPF e o CNPJ válidos na RFB." **§2º:** "O prazo de validade estipulado no caput **não alcança** as certidões ou documentos de cunho fiscal e trabalhista, da Seguridade Social, do FGTS, Balanço Patrimonial e demais demonstrações contábeis com prazos de vigência próprios, cabendo ao fornecedor manter atualizados seus documentos para efeito de habilitação."
- **IN art. 7º:** o cadastrado responde pela exatidão dos dados; desatualização pode causar inabilitação.
- Tradução para o rastreador: o **cadastro** nunca vence na prática; o que vence são os documentos — e no SICAF os federais se renovam sozinhos (a consulta é ao vivo), enquanto **estadual, municipal, falência e balanço vencem no upload** e precisam ser reenviados.
- Custo: "O cadastramento no SICAF é realizado sem ônus" (Manual Normativo) — cuidado com sites falsos que cobram (FAQ sistema).

---

## 4. Respostas diretas

1. **Menor validade do pacote: 30 dias — CRF/FGTS** (Manual CAIXA 2.7.1). Renovável a partir do 5º dia antes do vencimento. Cadência do sistema: **rodar a cada 25 dias**, reemitindo CRF + cartão CNPJ + certidão simplificada JUCESP (grátis, sem validade fixada) no mesmo lote. As de 180 dias (RFB/PGFN, CNDT, SEFAZ-SP, PMSP) entram num ciclo semestral com folga de 30 dias; PMSP pede até 10 dias para emitir quando há pendência.
2. **Custo único para ficar apta a licitar:** o único desembolso obrigatório é o **e-CNPJ A1: R$ 219,90–274,90/ano** (Certisign), R$ 235 (Soluti), R$ 203–257,20 (Valid combo). Todo o resto do pacote é R$ 0 (RFB, SEFAZ-SP*, PGE-SP, PMSP*, CAIXA*, TST, TJSP, JUCESP online, SICAF). *custo não declarado na página, emissão automática. Balanço: honorários contábeis UNVERIFIED. Custos de plataforma não são "únicos": BLL só no êxito; BNC R$ 118,80/processo; PCP R$ 129/processo ou R$ 165/mês; Licitanet UNVERIFIED.
3. **Grátis para dar lance:** Compras.gov.br (sempre) e BLL (plano por êxito: paga só quem ganha). BNC e PCP cobram por processo. Licitanet UNVERIFIED.
4. **Primeiro atestado qualitativo com zero histórico:** (i) uma venda privada + declaração do comprador — o art. 67 não exige emissor público nem quantidade e proíbe limite de tempo/local (§2º); (ii) entrar em editais sem qualificação técnica, em contratações diretas (art. 75 II ≤ R$ 65.492,11) ou de valor < R$ 16.373,03 / entrega imediata (art. 70 III), e pedir o atestado ao município após a entrega (art. 88 §3º); (iii) o cadastro de atesto do PNCP (art. 88 §4º) ainda não existe.
5. **Contradições com o que foi dito na tarefa:**
   - A Lei 15.266/2025 reescreveu o **caput** do art. 87 (e o art. 175 §1º), **não o §2º**.
   - BLL: o teto de R$ 600 vale "quando o valor do lote for superior a R$ 40.000"; abaixo disso a taxa é 1,5% do lote. Há também plano trimestral de R$ 630. Em SRP a base é o lote **adjudicado**, não o empenhado (art. 18) — a taxa efetiva sobre o realizado pode passar de 1,5%.
   - e-CNPJ: a página de serviço gov.br do SICAF aceita **conta gov.br prata/ouro como alternativa** ao certificado; o FAQ (mais antigo) diz "obrigatório". Na prática ele será necessário para assinar contratos e emitir NF-e, então o custo fica.
   - **Serasa saiu do mercado de certificação** (não lido diretamente: site em "Encerramento", 403). Certificadoras vivas: Certisign, Soluti, Valid.
   - Decreto 8.538/2015 vale para a administração **federal** (art. 1º §1º); nos municípios o que vincula é a LC 123 diretamente. E a dispensa de balanço para "pronta entrega" **não alcança SRP** segundo o SICAF — a maior parte dos pregões de kit é SRP.
   - A certidão de falência do TJSP virou **duas certidões** desde 05/11/2025 (SAJ + eproc); a eproc exige conta gov.br.
   - O prazo de cura da LC 123 art. 43 §1º é **5 dias úteis + 5**, não os 2 dias da redação original ainda visível no Planalto.
   - Não existe, hoje, cadastro de fornecedor no PNCP; o Decreto 13.106/2026 regulamenta o Sicx e manda usar o SICAF "enquanto não houver integração".
   - Art. 63 III/art. 64 II: as certidões são cobradas **só do vencedor, depois do julgamento**, e a lei manda aceitar atualização das que venceram após a proposta — o risco real é a certidão **já vencida no dia da proposta**, ou a estadual/municipal vencida no upload do SICAF.

## 5. O que ficou bloqueado nesta sessão (registro)
| Alvo | Resultado | Efeito |
|---|---|---|
| planalto.gov.br via WebFetch | 503; **curl com UA de navegador: 200** | nenhum — todas as leis lidas |
| normas.receita.fazenda.gov.br (Portaria 1.751/2014) | página só com redirecionamento JS | validade RFB/PGFN marcada NÃO LIDO |
| gov.br/pgfn "Prazos" | WebFetch: "Conteúdo Restrito"; curl: 404 | idem |
| dividaativa.pge.sp.gov.br (todas as páginas e PDFs) | HTTP 405 | validade PGE-SP UNVERIFIED |
| sp156.prefeitura.sp.gov.br | 403 | substituída pela página SF 28638 (lida) |
| licitacoesecontratos.tcu.gov.br | captcha | sem efeito (usei o texto da lei) |
| licitanet.com.br | 403 (WebFetch) / casca JS (curl) | preços UNVERIFIED |
| serasa.certificadodigital.com.br; gov.br/iti comunicado | 403 / "Conteúdo Restrito" | saída da Serasa NÃO LIDA |
| caixa.gov.br páginas .aspx | loops de redirect | Manual v19 (PDF) lido — suficiente |
| ajuda.portaldecompraspublicas.com.br | 403 | certificado no PCP UNVERIFIED |
| tutoriais.comprasgovernamentais.gov.br/sicaf | 502 (2 tentativas) | Manual Normativo (PDF) lido — suficiente |
| Manual operacional do SICAF (PDF) e Guia para fornecedores (PDF) | servidor devolveu HTML de 54 KB, não PDF | idem |
