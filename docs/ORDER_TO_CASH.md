# ORDER_TO_CASH — from winning a municipal kit tender to the money arriving

**Research date:** 2026-09-19. **Scope:** a one-person ME (Simples Nacional, Anexo I, sede SP) selling newborn layette kits to municipalities under Lei 14.133/2021, mostly through Sistema de Registro de Preços (SRP).

> Not legal or accounting advice. This is a map of primary sources — statute text read at planalto.gov.br, gov.br manuals, live PNCP fields, and the seven real editais in `data/editais/` — built to be checked by a lawyer/accountant before she relies on it. Anything I could not source is marked **UNVERIFIED**.

**Labels used**
- `[STATUTE]` — text read in full at the URL given.
- `[GOV.BR GUIDANCE]` — federal manual (STN MCASP, NF-e MOC) or a live government API field. Guidance, not law; federal rules bind municipalities only where the statute says so.
- `[EDITAL]` — verbatim quote, file name given. Seven editais: Agrolândia/SC, Bocaiúva do Sul/PR, Bom Sucesso do Sul/PR, Coronel Xavier Chaves/MG, Irecê/BA, São João do Paraíso/MA, Belterra/PA (TR only). Line numbers refer to the `.txt` extractions.
- `[INFERENCE]` — my reading of the sources; no source says it in those words.
- **UNVERIFIED** — could not be sourced today.

Builds on `docs/LEGAL_FINDINGS.md` (IRRF Anexo IV = §1, SUAS/IN 77 = §2, DIFAL = §3) and `data/siconfi_probe.md` (RREO Anexo 07). Those are not redone here.

---

## 0. The seven editais at a glance (the numbers the timeline uses)

| Edital (file) | ARP signing window | Call-off instrument | Delivery deadline | Recebimento definitivo deadline | Payment term as written | Restart clause on bad NF | Late-payment interest |
|---|---|---|---|---|---|---|---|
| Agrolândia/SC PE 01/2026/FMS (`agrolandia_sc_pe01_2026.txt`) | 5 dias úteis da convocação (21.1) | Autorização de Fornecimento / Ordem de Compra (5.1) | 10 dias (5.2) | none stated | até 30 dias do recebimento definitivo **e** atesto da NF (27.1) | none explicit | **none** |
| Bocaiúva do Sul/PR PE 40/2025 (`bocaiuvadosul_pr_pe40_2025.txt`) | 5 dias da convocação (14.1) | Empenho / Autorização de Compra (8.1, 8.5) | 15 dias úteis (8.5) | provisório 5 d.u. após entrega; definitivo até 8 d.u. após provisório (8.3) | até 30 dias da apresentação da NF (13.1) + 5 d.u. conferência (13.6); ARP 8.1: 30 dias do recebimento **ou** atesto | 13.3 — clock restarts after regularização | 1% a.m. + atualização (13.8) |
| Bom Sucesso do Sul/PR PE 34/2026 (`bomsucessodosul_pr_pe34_2026_EDITAL.txt`) | 5 dias úteis (15.1) | Nota de empenho retirada em 5 d.u. da convocação + ordem de fornecimento (21.1, 22.1) | 5 dias úteis (23.1) | definitivo pelo gestor em até 5 d.u. do provisório, mediante termo (23.4 II) | 10 / **20 (ME/EPP)** / 30 dias corridos (22.1.1–22.1.3), counted from receipt of NF **+ empenho + OF + termo de recebimento definitivo** | 22.4 suspends; ARP 11.3: NF devolvida, vencimento 15 dias após reapresentação | 6% a.a. (22.5); ARP 9.6: 0,5% a.m. |
| Coronel Xavier Chaves/MG PE 37/2026 (`coronelxavierchaves_mg_pl72_2026_EDITAL_RETIFICADO.txt`) | 5 dias da convocação (9.1) | Ordem de Compra por e-mail + Nota de Empenho (ARP 3.2) | 20 dias corridos do envio da OC (TR 6; ARP 8.1) | none stated; substituição em 24h (TR 8) | até 30 dias após a entrega do objeto e da NF (TR 7) | TR 7 — "contado a partir de sua reapresentação" | **none** |
| Irecê/BA PE SRP 003/2026 (`irece_ba_dom2777.txt`) | 5 dias úteis (10.1) | Ordem de fornecimento + nota de empenho "com força de contrato" (ARP 15.1) | 5 dias (8.1/9.1) | none stated; ARP 10.3: análise de amostras "tempo médio 30 dias" | edital 9.2: até 30 dias do recebimento da NF (= atesto, 9.3); **ARP 11.1: "no mês subsequente, até o 10º dia"** — the two texts disagree | 9.4.1 / ARP 11.3 — sobrestado, reinicia | atualização monetária pelo índice da Ata (ARP 11.9) |
| São João do Paraíso/MA (`saojoaodoparaiso_ma_23388.txt`) | 5 dias úteis (12.1, 12.5) | Ordem de Fornecimento + Nota de Empenho (14.1, 14.7) | 10 dias úteis da OF (14.1) | none stated; payment "após a assinatura do Termo de Recebimento Definitivo" (16.2) | NF protocolada até o 5º dia útil do mês subsequente (16.1); **no payment day-count anywhere** | 16.7 — "prorrogará automaticamente" | 6% a.a. (16.8–16.9) |
| Belterra/PA 26-017 TR (`belterra_pa_26-017.txt`) | n/a (TR only) | Ordem de Fornecimento (4.1) | imediato (4.1); substituição 48h (11.11) | provisório "no ato da entrega" (11.11); atestação por servidor (12.4) | até 30 dias do recebimento da NF (13.1) = atesto (13.3) | 13.4 — sobrestado, reinicia | **none** |

Every "30 days" above is counted from a different event. That is the single most important fact in this document.

---

## 1. Homologação and adjudicação

**Statutory basis.** `[STATUTE]` Lei 14.133/2021, art. 71: "Encerradas as fases de julgamento e habilitação, e exauridos os recursos administrativos, o processo licitatório será encaminhado à autoridade superior, que poderá: (...) IV - adjudicar o objeto e homologar a licitação." <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm>

**Document produced / by whom.** Termo de adjudicação and termo de homologação, signed by the autoridade superior (Bom Sucesso 14.1–14.2: "adjudicado pelo Prefeito Municipal (...) A homologação deste Pregão compete ao Prefeito Municipal"). In pregão without appeal the pregoeiro adjudicates and forwards for homologação (Coronel Xavier Chaves 12.11: "Não havendo recurso, a Pregoeira adjudicará o objeto ao licitante vencedor e encaminhará o procedimento à autoridade superior para homologação.").

**Where it appears.** `[GOV.BR GUIDANCE — live API]` On PNCP the award is visible on the compra record through `existeResultado: true` and a non-zero `valorTotalHomologado`, while `situacaoCompraNome` can stay `Divulgada no PNCP` (observed on Itaquaquecetuba 2025/447 — `data/editais/README.md` §1). Per-item results (supplier name, quantity) live only on the Family B endpoints (`/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}/itens/{n}/resultados`) which were 503 all day on 2026-09-19. Practically the homologação is also posted on the bidding platform (BNC, Compras.gov.br, BLL) where the session ran. `[INFERENCE]`

**What she receives.** Nothing is sent to her by force of statute at homologação; what follows is the **convocação** (stage 2). Agrolândia 21.1: "a empresa vencedora será convocada **via e-mail** a assinar A ATA DE REGISTRO DE PREÇOS". Coronel Xavier Chaves TR: "A Ordem de Compra será enviada para o e-mail cadastrado". So the e-mail address on the proposal is the operational channel.

**What it obliges.** Not a right to a contract: Coronel Xavier Chaves 15.4 / Irecê 14.4: "A homologação do resultado desta licitação não implicará direito à contratação." Once convoked, refusal is total default: `[STATUTE]` art. 90, § 5º: "A recusa injustificada do adjudicatário em assinar o contrato ou em aceitar ou retirar o instrumento equivalente no prazo estabelecido pela Administração caracterizará o descumprimento total da obrigação assumida".

**Typical timing.** Day 0 by definition. Convocação is not time-bounded by any of the seven editais. **UNVERIFIED** how many days pass between homologação and convocação in practice.

**What can go wrong.** Art. 71 I–III: return for saneamento, revogação or anulação can still happen after judgement; art. 90 § 3º: "Decorrido o prazo de validade da proposta indicado no edital sem convocação para a contratação, ficarão os licitantes liberados" (proposal validity: e.g. Coronel Xavier Chaves 5.8, 60 days).

---

## 2. Ata de Registro de Preços vs contract — and whether she can decline a call-off

**Statutory basis.** `[STATUTE]` Lei 14.133, arts. 82–86.
- Art. 83: "A existência de preços registrados implicará **compromisso de fornecimento** nas condições estabelecidas, mas **não obrigará a Administração a contratar**, facultada a realização de licitação específica para a aquisição pretendida, desde que devidamente motivada."
- Art. 84: "O prazo de vigência da ata de registro de preços será de 1 (um) ano e poderá ser prorrogado, por igual período, desde que comprovado o preço vantajoso. Parágrafo único. O contrato decorrente da ata de registro de preços terá sua vigência estabelecida em conformidade com as disposições nela contidas."
- Art. 82, IV: the edital must state "a possibilidade de o licitante oferecer ou não proposta em quantitativo inferior ao máximo previsto no edital, **obrigando-se nos limites dela**".
- Art. 82, VII: cadastro de reserva — other bidders who accept the winner's price are registered behind her.
- Art. 95: the contract instrument may be replaced by "carta-contrato, nota de empenho de despesa, autorização de compra ou ordem de execução de serviço" in "II - compras com entrega imediata e integral dos bens adquiridos e dos quais não resultem obrigações futuras".

Federal SRP regulation (`[STATUTE]` Decreto 11.462/2023, art. 1º: federal scope only — "no âmbito da Administração Pública federal direta, autárquica e fundacional") <https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/d11462.htm>. Municipalities have their own decrees (Irecê: Decreto Municipal 207/2024; Coronel Xavier Chaves ARP 7.4.3 cites "Decreto nº 4733, de 2024"; Bom Sucesso 19.1 adopts "artigos 25 a 27, do Decreto Federal nº 11.462/2023" by reference). Where the municipal decree is unknown, the federal text is the best available model, labelled as such.

**The difference for her.**

| | Contract (single order) | ARP (SRP) |
|---|---|---|
| What she signs | Termo de contrato, or nota de empenho as substitute (art. 95) | Ata de Registro de Preços; then each call-off comes as nota de empenho + ordem de fornecimento (Irecê ARP 15.1: "emissão de nota de empenho específica com a empresa, que terá força de contrato") |
| Quantity | Fixed | A ceiling; buyer may call off any amount up to it, or nothing (art. 83; Agrolândia 4.2: "A Administração não está obrigada a contratar os quantitativos estimados") |
| Duration | Per contract | 12 months + 12 (art. 84); Coronel Xavier Chaves ARP 3.1 counts from "divulgação no sítio eletrônico oficial"; Bocaiúva ARP 3.1 "eficácia legal após a data da publicação do seu extrato no Diário Oficial" |
| Price | Fixed/reajuste per contract | "fixos e irreajustáveis" during the ARP (Bom Sucesso 19.1) except arts. 25–27 events |
| Budget | Empenho at signature | No empenho at ARP signature; empenho only per call-off (Coronel Xavier Chaves ARP 3.1.1: "As aquisições decorrentes da Ata (...) ficam condicionadas à existência de disponibilidade orçamentária e financeira") |
| Her exposure | One delivery, one clock | Repeated small deliveries on short notice (Bom Sucesso 23.1: "5 (cinco) dias úteis, parceladamente, de acordo com as solicitações das Secretarias"); each with its own NF, atesto and payment clock |

**How a call-off is triggered.** Ordem de fornecimento / ordem de compra / autorização de fornecimento + nota de empenho, sent by e-mail (Coronel Xavier Chaves ARP 8.2.1–8.2.4: sent to the registered e-mail; "A Ordem de Compra será considerada devidamente recebida pela empresa adjudicatária 02 (dois) dias úteis após o envio do e-mail por parte da contratante nos casos em que a empresa deixar de acusar o recebimento"). São João do Paraíso 14.7: "A cada solicitação será emitida a correspondente Ordem de Fornecimento, na qual constarão as quantidades e os locais de entrega, acompanhada da respectiva Nota de Empenho". Bom Sucesso 18.2/21.1: she is convoked to **retirar** the nota de empenho "dentro do prazo de 5 (cinco) dias úteis de sua convocação, sob pena de decair o direito à contratação".

**Can she DECLINE a call-off? — No, not freely.** `[STATUTE + EDITAL]`
- The registered price is a "compromisso de fornecimento" (art. 83). Refusing the empenho is treated like refusing the contract (art. 90, § 5º).
- Federal model, Decreto 11.462 art. 28: "O registro do fornecedor será cancelado (...) quando o fornecedor: (...) II - não retirar a nota de empenho, ou instrumento equivalente, no prazo estabelecido pela Administração **sem justificativa razoável**". Mirrored verbatim in Agrolândia 12.1.2, Coronel Xavier Chaves 11.1.2/ARP 7.1.2, Irecê 9.1.4, Bom Sucesso 20.1.2.1.4.
- Fines: Bom Sucesso 27.1: refusal "em assinar a Ata de Registro de Preços ou retirar a respectiva nota de empenho (...) caracterizará o descumprimento total do compromisso assumido e a sujeitará à multa de 20% (vinte inteiros por cento) sobre o seu valor total". Bocaiúva 15.1: 20% "sobre o valor total da ata de registro de preços" for not signing the ARP.
- The lawful exits are narrow: (a) **ex ante**, bid for a quantity below the ceiling and be bound only up to it (art. 82, IV; Agrolândia 9.4.1; Coronel Xavier Chaves ARP 3.4.1); (b) price became unviable through a proven supervening fact — request price update with cost sheet (Decreto 11.462 art. 27, § 1º); if denied, "o fornecedor deverá cumprir as obrigações estabelecidas na ata, sob pena de cancelamento do seu registro" (art. 27, § 2º); (c) buyer asks her to *lower* the price and she refuses — then "o fornecedor será liberado do compromisso assumido quanto ao item registrado, sem aplicação de penalidades administrativas" (art. 26, § 1º; only when market price fell); (d) caso fortuito / força maior, proven (art. 29, II; Bom Sucesso 20.1.1; Bocaiúva ARP cancelamento "a pedido"). `[INFERENCE]` None of these is a "no thanks" button; (b) and (d) require a written, documented request before the empenho is due.
- Asymmetry to price in: she is bound for 12 months at a fixed price; the buyer is bound to nothing (art. 83).

**Where the ARP appears.** `[GOV.BR GUIDANCE — live API]` `GET https://pncp.gov.br/api/consulta/v1/atas?dataInicial=AAAAMMDD&dataFinal=AAAAMMDD` returned 200 on 2026-09-19 with fields `numeroAtaRegistroPreco`, `dataAssinatura`, `vigenciaInicio`, `vigenciaFim`, `dataPublicacaoPncp`, `cnpjOrgao`, `numeroControlePNCPCompra`. Editais confirm: Bocaiúva 14.3 "O preço registrado, com a indicação dos fornecedores, será divulgado no PNCP"; Agrolândia 9.13: ARP "posteriormente disponibilizada no sistema eletrônico utilizado pelo Município e no Portal Nacional de Contratações Públicas – PNCP".

**Typical timing.** Convocação → signature: 5 dias / 5 dias úteis in all six editais with a clause, extendable once "por igual período" (art. 90, § 1º). Publication: art. 94 gives the Administration up to "20 (vinte) dias úteis, no caso de licitação" to publish a contract on PNCP as "condição indispensável para a eficácia"; Decreto 11.462 art. 22 counts ARP vigência "do primeiro dia útil subsequente à data de divulgação no PNCP". `[INFERENCE]` So ARP effectiveness is somewhere between day 5 and day ~33 after homologação; the call-off after that is unbounded within the 12-month window.

**What can go wrong.** Regularidade fiscal is re-checked before formalizing (art. 91, § 4º) and again at every empenho (Bom Sucesso 21.2: "Por ocasião da emissão da nota de empenho, verificar-se-á por meio do SICAF e de outros meios se o fornecedor beneficiário mantém as condições de habilitação"). Missing the 5-day window → cadastro de reserva is called (art. 90, § 2º; Agrolândia 21.3). ARP silent for months → no revenue, no remedy (art. 83).

---

## 3. The Nota de Empenho

**Statutory basis.** `[STATUTE]` Lei 4.320/1964 <https://www.planalto.gov.br/ccivil_03/leis/l4320.htm>:
- Art. 58: "O empenho de despesa é o ato emanado de autoridade competente que cria para o Estado obrigação de pagamento pendente ou não de implemento de condição."
- Art. 60: "**É vedada a realização de despesa sem prévio empenho.** § 1º Em casos especiais previstos na legislação específica será dispensada a emissão da nota de empenho. (...) § 3º É permitido o empenho global de despesas contratuais e outras, sujeitas a parcelamento."
- Art. 61: "Para cada empenho será extraído um documento denominado 'nota de empenho' que indicará o nome do credor, a especificação e a importância da despesa bem como a dedução desta do saldo da dotação própria."
- Art. 59, § 1º (municipal): "é vedado aos Municípios empenhar, no último mês do mandato do Prefeito, mais do que o duodécimo da despesa prevista no orçamento vigente."

Lei 14.133, art. 95: the nota de empenho can *be* the contract (see stage 2). Bom Sucesso 21.6: "A nota de empenho da despesa terá força de contrato, conforme prevê o art. 95, II, da Lei nº 14.133/2021." Coronel Xavier Chaves ARP 3.2: "As aquisições decorrentes da Ata de Registro de Preços serão formalizadas exclusivamente mediante emissão de Nota de Empenho e Ordem de Compra"; 3.1.2: "A Nota de Empenho e a Ordem de Compra deverão indicar a respectiva dotação orçamentária".

`[GOV.BR GUIDANCE]` STN, MCASP 10ª ed., item 4.4.2.1 <https://www.tesourotransparente.gov.br/publicacoes/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp/2024/26> (PDF "MCASP - 10ª Edição.pdf"): "Consiste na reserva de dotação orçamentária para um fim específico. (...) **É recomendável constar no instrumento contratual o número da nota de empenho, visto que representa a garantia ao credor de que existe crédito orçamentário disponível e suficiente para atender a despesa objeto do contrato.** Nos casos em que o instrumento de contrato é facultativo, a Lei nº 14.133/2021 admite a possibilidade de substituí-lo pela nota de empenho de despesa, hipótese em que o empenho representa o próprio contrato." Types: ordinário (one payment), estimativo, global (parcelled).

**Who produces it.** The ordenador de despesa of the buying unit (secretaria/fundo), from the dotação named in the edital (Bom Sucesso: "08.03 Fundo municipal de Assistência Social; (...) 33.90.30 Material de Consumo; Despesa 548").

**Why nothing ships before it exists.** `[INFERENCE from art. 60 + art. 63 + art. 83]` Without an empenho there is no budget reserved, no legal obligation to pay (art. 58), no basis for liquidação (art. 63, § 2º, II lists "a nota de empenho" as a required basis) and, under SRP, no obligation on the buyer at all (art. 83). Goods delivered against a verbal or e-mail request are a gift until an empenho exists. Belterra TR 4.2: "As despesas correrão a conta dos recursos consignados no Orçamento Público, cujo programa de trabalho e elemento de Despesa constará na Respectiva nota de empenho".

**What must be on it.** Art. 61: credor (her CNPJ/razão social), especificação (items, quantities, unit prices as in the ARP), importância, dotação/deduction. Check it against the ARP before shipping: `[INFERENCE]` a value or description mismatch between empenho and NF is a liquidação defect (stage 6) and a restart trigger (stage 5).

**Why its number must be on the nota fiscal.** Liquidação is done by matching three documents (art. 63, § 2º: contract/ata, nota de empenho, comprovantes da entrega). Editais make the match a condition of the invoice: Bocaiúva 13.1(e): "Inserir no corpo da Nota Fiscal, em campo apropriado, o número do Empenho e Dados Bancários"; 13.1(d): "Cópia do Empenho ou Ordem de Serviço correspondente"; Bom Sucesso ARP 9.3.3.2: "O número da Ata, número do Pedido de Fornecimento (ou ofício) e número do empenho". The NF-e layout has a dedicated field for it — see stage 5.

**Typical timing.** Under SRP: unbounded (stage 2). Once convoked: Bom Sucesso gives 5 dias úteis to retirar. Delivery clocks start at receipt of the empenho/OF (Bocaiúva 8.5 "após o recebimento dos pedidos (...) através da Autorização de Compra ou Empenho"; São João do Paraíso 14.1; Coronel Xavier Chaves: first business day after the e-mail).

**What can go wrong.** Empenho issued with less than the ordered quantity/value (needs reforço — MCASP 4.4.2.1); empenho dated in exercise N but delivery in N+1 (→ restos a pagar, stage 8); last-month-of-mandate cap (art. 59, § 1º — December 2028 for current mayors); LRF art. 42 (last two quadrimesters of mandate, no obligation without cash cover) — `[INFERENCE]` expect thinner and later empenhos from May to December of an election year.

---

## 4. Delivery and recebimento (provisório vs definitivo)

**Statutory basis.** `[STATUTE]` Lei 14.133, art. 140: "O objeto do contrato será recebido: (...) II - em se tratando de compras: a) **provisoriamente, de forma sumária**, pelo responsável por seu acompanhamento e fiscalização, com verificação posterior da conformidade do material com as exigências contratuais; b) **definitivamente**, por servidor ou comissão designada pela autoridade competente, **mediante termo detalhado** que comprove o atendimento das exigências contratuais. § 1º O objeto do contrato poderá ser rejeitado, no todo ou em parte, quando estiver em desacordo com o contrato. (...) § 3º **Os prazos e os métodos para a realização dos recebimentos provisório e definitivo serão definidos em regulamento ou no contrato.**" Art. 117: fiscal do contrato "anotará em registro próprio todas as ocorrências". Art. 92, § 7º (Lei 14.770/2023): "consideram-se como adimplemento da obrigação contratual (...) a entrega do bem, ou parcela destes".

**Who signs.** Provisório: the fiscal (Bom Sucesso 23.4 I: "Provisoriamente, de forma sumária, pelo fiscal responsável"; Belterra 11.11: "No ato da entrega, os kits serão recebidos provisoriamente para posterior conferência quantitativa e qualitativa"). Definitivo: the gestor do contrato or designated servidor/comissão (Bom Sucesso 23.4 II: "Definitivamente, pelo gestor do contrato, no prazo máximo de 5 (cinco) dias úteis, contados da data do recebimento provisório, mediante termo hábil, após verificação do relatório detalhado e da documentação apresentada pelos fiscais do contrato"). Agrolândia 8.2(a): "servidor especialmente designado, registrando as ocorrências, bem como atestar o recebimento dos produtos".

**Within how many days.** Only two of seven fix a deadline for the definitivo:
- Bocaiúva 8.3: "a) Provisoriamente, no prazo de 05 (cinco) dias úteis após efetuada a entrega (...) b) Definitivamente, em até 08 (oito) dias úteis após o recebimento provisório." → up to 13 dias úteis (≈ 17–19 calendar days) after delivery.
- Bom Sucesso 23.4 II: 5 dias úteis after provisório.
- Agrolândia, Coronel Xavier Chaves, Irecê, São João do Paraíso, Belterra: **no deadline**. Since art. 140, § 3º delegates deadlines to "regulamento ou contrato", where the contract is silent the fiscal's own pace governs. **UNVERIFIED** whether any of these five has a municipal regulamento fixing it. Irecê ARP 10.3 adds: "o órgão contratante poderá selecionar (...) amostras dos itens entregues, a fim de serem submetidas a exames (...) O tempo médio de análise é de 30 (trinta) dias."

**What the termo looks like.** Art. 140 II(b): "termo detalhado". Editais call it "termo hábil" (Bom Sucesso), "Termo de Recebimento Definitivo" (São João do Paraíso 16.2), or simply the atesto on the NF (Bocaiúva 13.2: "a mesma deverá estar devidamente atestada pelo secretário responsável"; Belterra 12.4: "A atestação da nota (...) será por um servidor designado"). `[INFERENCE]` In small municipalities the "termo" is often a stamp-and-signature on the DANFE. She should ask for a copy (or a photo) of the attested DANFE/termo on the day it is signed — it is the document that starts most payment clocks (stage 6).

**If goods are rejected.** Art. 140, § 1º. Replacement windows: Bocaiúva 8.4: 48 h ("substituir ou complementar"); Bocaiúva ARP: 24 h; Coronel Xavier Chaves TR 8: "no prazo máximo de 24 (vinte e quatro) horas, sob pena de aplicação de multa"; Belterra 11.11: 48 h; Agrolândia 5.5: "05 (cinco) dias"; São João do Paraíso 15.3: 30 days (CDC art. 18). Irecê ARP 10.4: "A rejeição dos itens não justificará atrasos em relação ao prazo de entrega fixado." Late-delivery fines are steep: Bom Sucesso 27.4.1: "5% (cinco inteiros por cento) pelo 1º (primeiro) dia de atraso"; Coronel Xavier Chaves 13.x(b): "multa de 2% (dois por cento) sobre o valor total da proposta por dia de atraso"; Irecê ARP 11.6 / São João do Paraíso 21.3.2: 0,3% per day. Partial delivery: Coronel Xavier Chaves ARP 8.7 accepts it only with a matching NF and "aceite expresso"; Agrolândia 27.2: "O recebimento definitivo implica a entrega total dos itens pela empresa".

**Delivery deadlines (from receipt of the call-off).** Belterra: imediato · Bom Sucesso: 5 dias úteis · Irecê: 5 dias · Agrolândia: 10 dias · São João do Paraíso: 10 dias úteis · Bocaiúva: 15 dias úteis · Coronel Xavier Chaves: 20 dias corridos. `[INFERENCE]` With "imediato" and 5-day windows, buying inputs only after the empenho arrives is not feasible unless the supplier ships same-day; she either holds stock at her own risk or accepts the fine schedule above. This is the point where the handoff's "buy goods ~day 11" model and the editais collide.

---

## 5. The Nota Fiscal (NF-e)

**What the município requires on it.** `[EDITAL]`
- Empenho number, and often the ARP/pedido number: Bocaiúva 13.1(e) (empenho + dados bancários "no corpo da Nota Fiscal, em campo apropriado"); Bom Sucesso ARP 9.3.3: "9.3.3.1. A modalidade e o número da Licitação; 9.3.3.2. O número da Ata, número do Pedido de Fornecimento (ou ofício) e número do empenho; 9.3.3.3. número do item e descrição do produto: 9.3.3.4. A descrição do produto na Nota Fiscal, deverá obrigatoriamente, ser precedida da descrição constante da Ata de Registro de Preços; 9.3.3.5. valor unitário (conforme a Ata de Registro de Preços), forma de apresentação e valor total. 9.3.3.6. O Banco, número da agência e da conta corrente da CONTRATADA."
- Banking details: Coronel Xavier Chaves TR 7: "DEVERÁ INFORMAR, NA NOTA FISCAL, OS DADOS BANCÁRIOS PARA PAGAMENTO (PREFERENCIALMENTE DE CONTA MANTIDA NO BANCO DO BRASIL S.A. OU NA CAIXA ECONÔMICA FEDERAL) (...) CASO POSSUA, DEVERÁ TAMBÉM INFORMAR A CHAVE PIX." Bocaiúva 13.4–13.5: bank transfer only, "não sendo aceito eventuais BOLETOS BANCÁRIOS", account "obrigatoriamente (...) vinculada ao CNPJ do participante".
- Marks/lots: Bom Sucesso 23.3: "nota fiscal contendo os nomes, as marcas, os lotes de fabricação e seus respectivos quantitativos".
- Issued to the right CNPJ (Bom Sucesso ARP 11.1: "emitida: a Prefeitura Municipal de Bom Sucesso do Sul - PR CNPJ sob nº 80.874.100/0001-86") — for fundos (FMS, FMAS) check whether the fund has its own CNPJ. **UNVERIFIED** per buyer.
- Two copies where asked (Bom Sucesso 22.1 "em 2 (duas) vias").
- Accompanied by certidões at every payment: all seven (e.g. Bocaiúva 13.1(a)–(c); São João do Paraíso 16.6.1–16.6.5; Coronel Xavier Chaves TR 7: "a não apresentação implicará a não realização do pagamento até ocorrer a regularização").
- Elements checked at liquidação: Irecê ARP 11.2: "a) o prazo de validade; b) a data da emissão; c) os dados da Ata e do órgão contratante; d) o período respectivo de execução do contrato; e) o valor a pagar; e eventual destaque do valor de retenções tributárias cabíveis."

**Where those go in the NF-e layout.** `[GOV.BR GUIDANCE]` NF-e Manual de Orientação do Contribuinte 7.0, Anexo I (Leiaute e Regras de Validação), portal nacional <https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=ndIjl+iEFdE=>:
- Group **ZB "compra" — "Informação adicional de compra"**: `ZB02 xNEmp` "Nota de Empenho — Identificação da Nota de Empenho, quando se tratar de compras públicas (NT 2011/004)" (1–22 chars); `ZB03 xPed` "Pedido" (1–60); `ZB04 xCont` "Contrato" (1–60). This is the field the empenho number belongs in.
- Item level: `I60 xPed` "Número do Pedido de Compra" (1–15) and `I61 nItemPed`.
- Free text: `Z03 infCpl` "Informações Complementares de interesse do Contribuinte" (up to 5000 chars) — where the human-readable line "Empenho nº …, ARP nº …, Pregão nº …, Banco/Ag/CC, Optante Simples Nacional" goes, since municipal staff read the DANFE, not the XML. `[INFERENCE]` Fill both ZB02 and infCpl: the XML field satisfies systems, the printed line satisfies the servidor doing the atesto.
- Destinatário: `E16a indIEDest` = "9=Não Contribuinte, que pode ou não possuir Inscrição Estadual"; `B25a indFinal` = "1=Consumidor final"; `B11a idDest` = "2=Operação interestadual"; emitente `C21 CRT` = "1=Simples Nacional", with the CSOSN groups (N10c etc.).

**Tax treatment (do not redo — see LEGAL_FINDINGS).** ICMS is inside the DAS; no DIFAL to the destination state (LEGAL_FINDINGS §3, ADI 5469); no ISS (goods, not services); no IRRF for a Simples optant if the Anexo IV declaration is on file (§1), otherwise 1,2% may be withheld and is not recoverable from RFB. Editais confirm the pattern: Agrolândia 27.3 (IR retained only from "não optante do Simples Nacional"); Irecê 9.9 / ARP 11.14 and Belterra 13.8, identical text: "A Contratada regularmente optante pelo Simples Nacional (...) não sofrerá a retenção tributária quanto aos impostos e contribuições abrangidos por aquele regime. **No entanto, o pagamento ficará condicionado à apresentação de comprovação, por meio de documento oficial, de que faz jus ao tratamento tributário favorecido**". Coronel Xavier Chaves TR 7 asserts retention "aplicando-se, o percentual constante na coluna 02, do Anexo I, da IN RFB n.º 1.234/2012" — with no Simples carve-out written in; `[INFERENCE]` present the Anexo IV declaration proactively there or expect 1,2% withheld.

**What the IN RFB 1.234 Anexo IV declaration must accompany.** Per LEGAL_FINDINGS §1 (IN 1.234 art. 6º): presented "no ato da assinatura do contrato", 2 vias, per contract/prorrogação (§ 5º), and SC COSIT 61/2020 says the portal-consultation shortcut applies only "à etapa dos pagamentos". `[INFERENCE]` Under SRP, treat **each nota de empenho** as a new contract for this purpose (art. 95 makes it the contract): attach a signed Anexo IV to the ARP signature and again to every NF, plus the Simples optant certificate printout, because Irecê/Belterra condition payment on "documento oficial".

**Timing.** The NF-e travels with the goods (Agrolândia 5.4: "acompanhados da respectiva nota fiscal contendo a descrição detalhada dos itens"), so its emission date ≈ shipment date. But *presentation* for payment may be later: Bom Sucesso 22.1 wants the NF together with "termo de recebimento definitivo do objeto, emitido previamente pelo gestor"; São João do Paraíso 16.1: protocolada "até o 5° (quinto) dia útil subsequente ao mês do fornecimento e aceite definitivo dos produtos, acompanhada de ofício de encaminhamento". Note the art. 137 § 2º IV two-month clock runs from *emissão* (stage 7), so an early emission date shortens her wait for that remedy, while the payment clock in most editais starts only at atesto.

**What can go wrong — the restart.** Six of seven restart the clock on any defect:
- Bocaiúva 13.3: "Havendo erro na apresentação da Nota Fiscal/Fatura ou dos documentos pertinentes à contratação, ou, ainda, circunstância que impeça a liquidação da despesa, o pagamento ficará pendente até que a Contratada providencie as medidas saneadoras. Nesta hipótese, **o prazo para pagamento iniciar-se-á após a comprovação da regularização da situação**, não acarretando qualquer ônus para a Contratante."
- Bom Sucesso 22.4: "o prazo constante do item 22.1 poderá ser suspenso até que haja reparação do vício"; ARP 11.3: "As notas fiscais que apresentarem incorreções serão devolvidas e seu vencimento ocorrerá 15 (quinze) dias após a data da sua reapresentação."
- Coronel Xavier Chaves TR 7: "Em caso de irregularidade na emissão dos documentos fiscais, o prazo de pagamento será contado a partir de sua reapresentação".
- Irecê 9.4.1 / ARP 11.3; Belterra 13.4 (same text as Bocaiúva); São João do Paraíso 16.7: "prorrogará automaticamente o prazo para pagamento, sem direito a qualquer acréscimo ou compensação financeira, sendo o atraso de exclusiva responsabilidade da CONTRATADA".
- Agrolândia has no explicit restart clause but 8.2(c) lets the buyer "Recusar (...) documentos fiscais em desacordo com os bens adquiridos".
The handoff's Paracatu/MG item 11.1.2 is not in this repo and could not be quoted; the mechanism above is the same one.

---

## 6. Liquidação and pagamento

**Statutory basis.** `[STATUTE]` Lei 4.320:
- Art. 62: "O pagamento da despesa só será efetuado quando ordenado após sua regular liquidação."
- Art. 63: "A liquidação da despesa consiste na verificação do direito adquirido pelo credor tendo por base os títulos e documentos comprobatórios do respectivo crédito. § 1º Essa verificação tem por fim apurar: I - a origem e o objeto do que se deve pagar; II - a importância exata a pagar; III - a quem se deve pagar a importância, para extinguir a obrigação. § 2º A liquidação da despesa por fornecimentos feitos ou serviços prestados terá por base: I - o contrato, ajuste ou acôrdo respectivo; II - a nota de empenho; III - os comprovantes da entrega do material ou da prestação efetiva do serviço."
- Art. 64: "A ordem de pagamento é o despacho exarado por autoridade competente, determinando que a despesa seja paga. Parágrafo único. A ordem de pagamento só poderá ser exarada em documentos processados pelos serviços de contabilidade."
- Art. 65: payment "por tesouraria ou pagadoria regularmente instituídas por estabelecimentos bancários credenciados".

`[GOV.BR GUIDANCE]` MCASP 10ª ed. 4.4.2.2–4.4.2.4 adds the accounting stage "em liquidação" (goods delivered, verification pending) between empenho and liquidação, and: "O pagamento consiste na entrega de numerário ao credor por meio de cheque nominativo, ordens de pagamentos ou crédito em conta, e só pode ser efetuado após a regular liquidação da despesa."

`[STATUTE]` Lei 14.133, art. 141: "No dever de pagamento pela Administração, será observada a **ordem cronológica para cada fonte diferenciada de recursos**, subdividida nas seguintes categorias de contratos: I - fornecimento de bens; (...) § 1º A ordem cronológica (...) poderá ser alterada, mediante prévia justificativa da autoridade competente e posterior comunicação ao órgão de controle interno da Administração e ao tribunal de contas competente, exclusivamente nas seguintes situações: (...) **II - pagamento a microempresa, empresa de pequeno porte**, agricultor familiar, produtor rural pessoa física, microempreendedor individual e sociedade cooperativa, **desde que demonstrado o risco de descontinuidade do cumprimento do objeto do contrato**; (...) § 2º A inobservância imotivada da ordem cronológica referida no caput deste artigo ensejará a apuração de responsabilidade do agente responsável, cabendo aos órgãos de controle a sua fiscalização. § 3º **O órgão ou entidade deverá disponibilizar, mensalmente, em seção específica de acesso à informação em seu sítio na internet, a ordem cronológica de seus pagamentos**, bem como as justificativas que fundamentarem a eventual alteração dessa ordem."
Art. 92 V–VI: every contract must state "o preço e as condições de pagamento (...) e os critérios de atualização monetária entre a data do adimplemento das obrigações e a do efetivo pagamento" and "o prazo para liquidação e para pagamento". Art. 143: "No caso de controvérsia sobre a execução do objeto, quanto a dimensão, qualidade e quantidade, a parcela incontroversa deverá ser liberada no prazo previsto para pagamento." Art. 145: no advance payment unless expressly in the edital (Bom Sucesso 22.1 forbids it outright).

**Art. 141 in practice.** `[INFERENCE]` The queue is per *fonte de recursos* — a kit paid from FNAS/SUAS funds is in a different queue from one paid from recursos próprios (Bom Sucesso: "Recursos próprios do município"). Art. 141 sets no day-count; the days come from the edital (LEGAL_FINDINGS §2 and rule_9). The ME jump-the-queue right (§ 1º II) needs a written request showing "risco de descontinuidade" — that is her working-capital situation stated plainly — and creates a paper trail the tribunal de contas sees; it is a lever for a stuck invoice, not a routine. The monthly publication duty (§ 3º) is the tool: the buyer's own site must show where her NF sits in the queue.

**Payment terms as they actually appear (every stated term).**
1. Agrolândia 27.1: "no prazo de até 30 (trinta) dias, contado do recebimento definitivo do objeto e do atesto da nota fiscal, observada a ordem cronológica e a regularidade fiscal da contratada"; TR 9.1: "em ordem cronológica, em até 30 (trinta) dias após o atesto do documento de cobrança".
2. Bocaiúva 13.1: "em até 30 (trinta) dias, contados a partir da apresentação da nota fiscal"; 13.6: "prazo de até 05 (cinco) dias úteis para conferência e aprovação"; ARP 8.1: "em até 30 dias a partir do efetivo recebimento do produto ou do atesto da Nota Fiscal pelo secretário responsável".
3. Bom Sucesso 22.1: "a contar do recebimento da nota fiscal/fatura discriminada, em 2 (duas) vias, acompanhada da nota de empenho, da ordem de fornecimento, bem como do termo de recebimento definitivo do objeto, emitido previamente pelo gestor (...) 22.1.1 no prazo de 10 (dez) dias corridos, quando a Contratada estiver enquadrada como MEI; 22.1.2 no prazo de 20 (vinte) dias corridos, quando a Contratada estiver enquadrada como ME ou EPP; 22.1.3 no prazo de 30 (trinta) dias corridos, nos demais casos." (Decreto Municipal 3.283/2025 in the preamble.)
4. Coronel Xavier Chaves TR 7: "em até 30 (trinta) dias após a entrega do objeto e da respectiva Nota Fiscal."
5. Irecê 9.2: "no prazo de até 30 (trinta) dias, contados a partir do recebimento da Nota Fiscal ou Fatura"; 9.3: "Considera-se ocorrido o recebimento da nota fiscal ou fatura no momento em que o órgão contratante atestar a execução do objeto do contrato." ARP 11.1: "o pagamento das mercadorias será devido após a liquidação do objeto, conforme fornecimento, a ser pago no mês subsequente, até o 10º (décimo) dia." **These two disagree**; the ARP is the instrument she signs.
6. São João do Paraíso 16.1–16.2: NF "protocolada (...) até o 5° (quinto) dia útil subsequente ao mês do fornecimento e aceite definitivo"; payment "após a assinatura do Termo de Recebimento Definitivo". No day count.
7. Belterra 13.1: "no prazo máximo de até 30 (trinta) dias, contados a partir do recebimento da Nota Fiscal ou Fatura"; 13.3: "Considera-se ocorrido o recebimento do documento fiscal no momento em que o órgão contratante atestar a execução"; 3.1: "30 dias após a entrega do produto e emissão da nota fiscal juntamente com as certidões".

"Date of payment" = date the ordem bancária is issued, not when funds land (Irecê 9.5 / ARP 11.11; Belterra 13.5: "Será considerada data do pagamento o dia em que constar como emitida a ordem bancária"). `[INFERENCE]` add 1–2 business days for the credit to arrive.

**Range.** 20 days (Bom Sucesso, ME) to 30 days (five editais), counted from an event that is itself 0 to ~19 days after delivery, or undefined (São João do Paraíso). Irecê ARP's "até o 10º dia do mês subsequente" can be shorter or longer than 30 days depending on the delivery date in the month.

**What can go wrong.** Certidão expired at payment → payment held (Coronel Xavier Chaves TR 7; Irecê 11.5: notified, "no prazo de 5 (cinco) dias úteis, regularize sua situação ou (...) apresente sua defesa", then 11.7 rescisão). Pending fine → withheld (Bocaiúva ARP 8.8: "Nenhum pagamento será efetuado à FORNECEDORA antes de paga ou relevada eventual multa"). Fonte de recursos not yet transferred → LEGAL_FINDINGS §2; Bocaiúva 13.9 explicitly excludes from its interest clause delays "por necessidades de pagamento via repasses (ex.: de convênios)".

---

## 7. Late payment

**Statutory basis.** `[STATUTE]` Lei 14.133:
- Art. 137, § 2º: "O contratado terá direito à extinção do contrato nas seguintes hipóteses: (...) **IV - atraso superior a 2 (dois) meses, contado da emissão da nota fiscal, dos pagamentos ou de parcelas de pagamentos devidos pela Administração** por despesas de obras, serviços ou fornecimentos". § 3º, II: these hypotheses "assegurarão ao contratado o direito de optar pela suspensão do cumprimento das obrigações assumidas até a normalização da situação, admitido o restabelecimento do equilíbrio econômico-financeiro". § 3º, I: not available "quando decorrerem de ato ou fato que o contratado tenha praticado, do qual tenha participado ou para o qual tenha contribuído" — i.e. a rejected NF is her delay, not theirs.
- Art. 138, § 2º: when termination is the Administration's fault, the contractor gets "II - pagamentos devidos pela execução do contrato até a data de extinção; III - pagamento do custo da desmobilização".
- Art. 92, V: atualização monetária clause is mandatory in every contract.
- Art. 115, § 1º: "É proibido à Administração retardar imotivadamente a execução" — including "na hipótese de posse do respectivo chefe do Poder Executivo".

**Interest/correction clauses in the seven editais (show the range).**
- Bocaiúva 13.8 / ARP 8.11: "Em caso de atraso de pagamento motivado exclusivamente pelo CONTRATANTE, o valor devido deverá ser acrescido de atualização financeira (...) juros de mora serão calculados à taxa de 1% (um por cento) ao mês." (≈12% a.a. + correction)
- Bom Sucesso 22.5: "EM = I x N x VP (...) I = Índice de compensação financeira = 0,00016438 (...) i = taxa percentual anual no valor de 6%"; ARP 9.6: "0,5% (meio por cento) ao mês, ou 6% (seis por cento), calculados de forma simples, ao ano". (6% a.a., no separate correction)
- São João do Paraíso 16.8–16.9: same 6% a.a. formula ("0,00016438").
- Irecê ARP 11.9: "os valores devidos ao contratado serão atualizados monetariamente (...) mediante aplicação do índice da Ata que represente o menor valor acumulado no período" (correction only, no interest; the Ata's index is IPCA per 7.x).
- **Agrolândia, Coronel Xavier Chaves, Belterra: no interest or correction clause at all** (searched "atualiza", "juros", "encargos morat", "compensação financeira"). `[INFERENCE]` That omission breaches art. 92, V; she can raise it at esclarecimento/impugnação (art. 164, per LEGAL_FINDINGS §5) or, after the fact, argue art. 92 V + Código Civil default interest — **UNVERIFIED** which rate a court would apply.
- Note what every clause excludes: delays she "contributed to" (art. 137 § 3º I; Bocaiúva 13.9; Bom Sucesso 22.5 "desde que o fornecedor beneficiário não tenha concorrido"); and Bom Sucesso 19.6 in the price chapter: "Não se admitirá nenhum encargo financeiro, como juros, despesas bancárias e ônus semelhantes."

**Practical remedies for a small supplier, in order of cost.** `[INFERENCE from the statute]`
1. Day +1 after the edital term: written request to the fiscal/gestor citing the clause and the art. 141 § 3º published queue (ask where the NF sits). Check the buyer's transparency page for the monthly ordem cronológica.
2. Ask for the incontroversa part (art. 143) if the hold is about one item.
3. Art. 141 § 1º II request (ME, "risco de descontinuidade"), copied to the controle interno.
4. Invoice the moratory interest "em fatura própria" (Bom Sucesso 22.5 says exactly that) — it is contractual, not a favour.
5. At 2 months from NF emission: formal notice invoking art. 137 § 2º IV and § 3º II — suspend further call-offs under that ARP without penalty. This is the one moment SRP asymmetry flips in her favour.
6. Representação to the tribunal de contas (art. 141 § 2º; the TCE is the body the ordem cronológica is reported to) — free, written.
7. Judicial: ação de cobrança; restos a pagar processados "em geral, não podem ser cancelados" (MCASP 4.7.3) so the liquidated debt survives the year-end.

---

## 8. Restos a pagar — how an unpaid invoice is carried across 31 December

**Statutory basis.** `[STATUTE]` Lei 4.320, art. 35: "Pertencem ao exercício financeiro: (...) II - as despesas nêle legalmente empenhadas." Art. 36: "Consideram-se Restos a Pagar as despesas empenhadas mas não pagas até o dia 31 de dezembro distinguindo-se as processadas das não processadas." Art. 37: despesas de exercícios anteriores. Decreto 93.872/1986 (federal), art. 67: "§ 1º Entendem-se por processadas e não processadas, respectivamente, as despesas liquidadas e as não liquidadas"; art. 68 § 2º (federal): RPNP not liquidated are blocked "em 30 de junho do segundo ano subsequente ao de sua inscrição". <https://www.planalto.gov.br/ccivil_03/decreto/d93872.htm>. LC 101/2000 (LRF), art. 42: no obligation in the last two quadrimesters of a mandate "que tenha parcelas a serem pagas no exercício seguinte sem que haja suficiente disponibilidade de caixa" <https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm>.

`[GOV.BR GUIDANCE]` MCASP 10ª ed.:
- 4.7.2: "Serão inscritas em restos a pagar não processados as despesas não liquidadas, nas seguintes condições: ▪ O serviço ou material contratado tenha sido prestado ou entregue e que se encontre, em 31 de dezembro de cada exercício financeiro em fase de verificação do direito adquirido pelo credor (despesa em liquidação); ou ▪ O prazo para cumprimento da obrigação assumida pelo credor estiver vigente (despesa a liquidar). A inscrição de despesa em restos a pagar não processados é realizada após a anulação dos empenhos que não serão inscritos em virtude de restrição em norma do ente da Federação".
- 4.7.3: "Serão inscritas em restos a pagar processados as despesas liquidadas e não pagas no exercício financeiro, ou seja, aquelas em que o serviço, a obra ou o material contratado tenha sido prestado ou entregue e aceito pelo contratante (...) Neste caso, em geral, **não podem ser cancelados**, tendo em vista que o fornecedor de bens ou serviços satisfez a obrigação de fazer e a Administração conferiu essa obrigação."

**What it means for one of her invoices at year-end.** `[INFERENCE]`
- Delivered, attested (liquidada), unpaid on 31/12 → **RPP**: her credit survives, is paid from the next year's cash, and is what the SICONFI RREO Anexo 07 block `RestosAPagarProcessadosENaoProcessadosLiquidados…` counts (`data/siconfi_probe.md` §3 — the buyer screen `rule_6_buyer_payment` reads inscritos/pagos/cancelados/saldo from there). A high saldo/inscritos ratio means the ente carries liquidated supplier debt into the next year and pays it slowly; a high cancelados ratio means it writes such debt off.
- Delivered but **not** attested on 31/12 → **RPNP "em liquidação"**: can be anulado "em virtude de restrição em norma do ente" before inscription (MCASP 4.7.2). The municipality's own year-end decree decides — **UNVERIFIED** per município. This is why the atesto date matters more than the delivery date in December.
- Empenho issued, goods not yet delivered on 31/12 → **RPNP "a liquidar"**: same exposure; federal rule gives it validity to 30 June of year +2 (Decreto 93.872 art. 68 § 2º), municipal rules vary.
- Election-year effect: LRF art. 42 and Lei 4.320 art. 59 § 1º (last month of the mandate: no more than one twelfth of budgeted spending may be empenhado) — expect fewer, later and smaller empenhos in H2 2028 and a December cliff.

---

## Timeline — Day 0 = homologação

Days are calendar days unless marked d.u. (dias úteis; 1 d.u. ≈ 1,4 calendar days). Source for each number is the clause quoted in the stage above.

| Step | Best edital | Typical (five 30-day editais) | Worst edital | Unbounded? |
|---|---|---|---|---|
| A. Homologação → convocação to sign ARP | 1 | 3–7 `[INFERENCE]` | ? | **yes** (no clause) |
| B. Convocação → ARP signed | 1 | ≤5 / ≤5 d.u. (+ same again if extended) | 14 | no |
| C. ARP signed → published (eficácia/vigência) | 1 | 2–10 `[INFERENCE]` | 20 d.u. ≈ 28 (art. 94) | no |
| D. ARP effective → first nota de empenho + ordem de fornecimento | 0 | **unknown** | 365 | **yes** (art. 83) |
| E. Empenho received → she must retirar/acknowledge | 0 | 2 d.u. deemed (CXC 8.2.4) | 5 d.u. (Bom Sucesso 21.1) | no |
| F. Empenho → delivery deadline (her buy/assemble/ship must fit here) | 0 (Belterra) | 5 d.u.–10 d.u. (Bom Sucesso, Irecê, Agrolândia, SJP) | 15 d.u. ≈ 21 (Bocaiúva) / 20 (CXC) | no |
| G. Delivery → recebimento provisório | 0 (Belterra, Bom Sucesso) | 0–5 d.u. (Bocaiúva) | — | no |
| H. Provisório → definitivo / atesto | 5 d.u. (Bom Sucesso) | **no deadline** in 5 of 7 | 8 d.u. (Bocaiúva); "30 dias" sample analysis (Irecê ARP 10.3) | **yes** in 5 of 7 |
| I. Atesto/NF presentation → payment term | 20 (Bom Sucesso, ME) | 30 | undefined (SJP); "10º dia do mês subsequente" (Irecê ARP) | partly |
| J. Ordem bancária → money in account | 0 | 1–2 `[INFERENCE]` | — | no |

**Adding it up from the empenho (the only clock she can plan around):**

| Edital | Delivery | Definitivo/atesto | Payment | **Empenho → ordem bancária** |
|---|---|---|---|---|
| Bom Sucesso do Sul (ME term) | ≤7 | ≤7 | 20 | **≈ 34** (best in set) |
| Belterra | 0 | ? (assume 3–10) | 30 | **≈ 33–40** |
| Irecê (edital text) | 5 | ? (3–30) | 30 | **≈ 38–65**; ARP text: up to 10th of following month |
| Agrolândia | 10 | ? (3–10) | 30 | **≈ 43–50** |
| Coronel Xavier Chaves | 20 | (clock runs from entrega + NF) | 30 | **≈ 50** |
| Bocaiúva do Sul | 21 | ≤18 (5+8 d.u.) | 30 (from NF presentation; NF travels with goods) | **≈ 51–69** |
| São João do Paraíso | 14 | ? | NF by 5th d.u. of next month; term undefined | **≈ 45–?** UNVERIFIED |

**From homologação:** add A+B+C (≈ 5–35 days) **plus D, which no edital bounds**. Under SRP the honest answer is "34–70 days after the empenho, and the empenho arrives whenever the secretaria decides, if ever". Under a single-order contract (art. 95 empenho-as-contract, e.g. Belterra's TR), the empenho typically comes with the convocação, so ≈ 40–75 days from homologação. The handoff's "paid ~day 45" is the best-case single-order path (immediate empenho + 30-day term counted from delivery + fast atesto) and is a floor, not a projection, for SRP.

**The three places the clock most often restarts or stalls** (`[INFERENCE]` from clause structure — I cannot measure frequency from seven documents):
1. **NF/document defect → clock restarts from reapresentação** (6 of 7 editais; stage 5). Triggers she controls: missing empenho/ARP number, wrong CNPJ, description not prefixed by the ARP wording, value ≠ empenho, expired certidão, missing Simples proof. Cost: the whole term again (Bom Sucesso ARP: 15 days from reapresentação; the others: full 20–30 days).
2. **Recebimento definitivo / atesto with no deadline** (5 of 7; stage 4). The payment term in Agrolândia, Irecê, Belterra and São João do Paraíso does not start until a servidor signs; Bocaiúva allows up to 13 d.u.; Irecê ARP allows a 30-day sample test. Rejection of any item restarts G–H after substitution (24 h–5 days) and, for Agrolândia, definitivo requires "entrega total".
3. **The call-off gap under SRP** (step D; stage 2). Not a restart but the largest stall: the ARP obliges her for 12 months and the buyer for nothing (art. 83). At year-end it compounds with restos a pagar (stage 8) and, in 2028, with LRF art. 42.
A fourth, entirely in her hands: certidões (federal/estadual/municipal/FGTS/CNDT) required at ARP signature, at every empenho and at every payment — one lapsed certidão holds payment in all seven.

---

## Checklist — o que ela faz em cada vitória (PT-BR)

Imprima e siga por pedido. Cada linha cita a base; "editais" = os sete em `data/editais/`.

**No dia da homologação (Dia 0)**
1. Confirmar no portal da licitação (BNC / Compras.gov.br / BLL) e no PNCP que o item foi **adjudicado e homologado** em seu nome (Lei 14.133, art. 71, IV). Anotar nº do pregão, nº do processo, nº do item, quantidade máxima e preço registrado.
2. Conferir que o e-mail cadastrado na proposta está sendo lido todo dia — a convocação e as ordens de compra chegam por ele (Agrolândia 21.1; Coronel Xavier Chaves TR: "considerar-se-á a Ordem de Compra como devidamente recebida dois dias úteis após o envio do e-mail").
3. Puxar as 5 certidões e anotar as datas de vencimento: Receita/PGFN (conjunta), Estadual (SP), Municipal (sede), FGTS (CRF), CNDT. Marcar renovação 10 dias antes de cada vencimento. Sem elas não se assina ata, não se recebe empenho e não se recebe pagamento (Lei 14.133, art. 91, § 4º; Bom Sucesso 21.2; todos os sete na cláusula de pagamento).
4. Ler no edital/ARP: (a) quem emite a ordem de fornecimento e o empenho; (b) prazo de entrega e a partir de que evento conta; (c) prazo do recebimento definitivo (se houver); (d) de que evento conta o prazo de pagamento; (e) o que a NF tem de conter; (f) se há cláusula de juros/correção. Preencher `config/order_to_cash.yaml` para este pedido.

**Na convocação para assinar a Ata (Dias 1–10)**
5. Assinar dentro do prazo (5 dias / 5 dias úteis em todos os editais). Se precisar, pedir prorrogação **por escrito, dentro do prazo**, uma única vez (art. 90, § 1º). Perder o prazo = decai o direito e o cadastro de reserva é chamado (art. 90, § 2º).
6. Entregar a **Declaração Anexo IV da IN RFB 1.234/2012** em 2 vias assinadas, e guardar a 2ª via com recibo (ver LEGAL_FINDINGS §1). Juntar a consulta de optante do Simples impressa — Irecê e Belterra condicionam o pagamento a "documento oficial".
7. Guardar cópia da Ata assinada e conferir sua publicação no PNCP (`/api/consulta/v1/atas`) ou no Diário Oficial do Município. A vigência de 12 meses conta da publicação, não da assinatura (Decreto 11.462, art. 22; Bocaiúva ARP 3.1).
8. Lembrar: a Ata obriga **você** por 12 meses ao preço registrado; **não obriga** o município a comprar (art. 83). Não comprar insumo por conta da Ata.

**Quando chegar a Ordem de Fornecimento / Nota de Empenho**
9. **Nada sai do estoque sem a nota de empenho em mãos** (Lei 4.320, art. 60: "É vedada a realização de despesa sem prévio empenho"). Pedido só por telefone/WhatsApp não é pedido.
10. Acusar o recebimento por e-mail no mesmo dia (Coronel Xavier Chaves ARP 8.2.3; Bom Sucesso 21.5.1). A partir daí conta o prazo de entrega.
11. Conferir a nota de empenho contra a Ata: seu CNPJ/razão social, itens, quantidades, preço unitário, valor total, dotação. Divergência → pedir correção **antes** de entregar; o empenho errado trava a liquidação (Lei 4.320, art. 63, § 2º, II).
12. Anotar: nº do empenho, nº da ordem de fornecimento/ofício, secretaria/fundo requisitante e **CNPJ do destinatário** (prefeitura ou fundo — conferir qual).
13. Calcular a data-limite de entrega (dias corridos ou úteis, conforme o edital) e o plano de compra/montagem/expedição que cabe nela. Se não cabe, comunicar por escrito **antes** do vencimento (Coronel Xavier Chaves 8.2; São João do Paraíso 14.3: prorrogação só com pedido escrito e fundamentado).

**Na expedição**
14. Emitir a NF-e para o CNPJ exato do empenho, com: `indIEDest = 9` (não contribuinte), `indFinal = 1`, `idDest = 2` (interestadual), `CRT = 1` (Simples), CSOSN correto (MOC 7.0, Anexo I).
15. Preencher o grupo **"compra"** do XML: `xNEmp` = nº da nota de empenho, `xPed` = nº da ordem de fornecimento, `xCont` = nº da Ata/contrato (MOC 7.0, Anexo I, ZB02–ZB04).
16. Escrever também em **Informações Complementares** (`infCpl`), para quem lê o DANFE: "Pregão Eletrônico nº __/__ – Processo nº __ – Ata de Registro de Preços nº __ – Ordem de Fornecimento nº __ – **Nota de Empenho nº __** – Item __ – Banco __ Ag. __ C/C __ (CNPJ __) – PIX __ – Optante pelo Simples Nacional (LC 123/2006): não sujeita à retenção do art. 4º, XI, da IN RFB 1.234/2012" (Bocaiúva 13.1(e); Bom Sucesso ARP 9.3.3; Coronel Xavier Chaves TR 7).
17. Descrição de cada item **começando pela descrição da Ata**, com marca, lote e quantidade; valor unitário igual ao registrado (Bom Sucesso ARP 9.3.3.4–9.3.3.5, 23.3).
18. A NF-e (DANFE) viaja com a mercadoria (Agrolândia 5.4). Levar/enviar também: cópia do empenho, cópia da ordem de fornecimento, as 5 certidões vigentes, Anexo IV assinado, e 2 vias impressas da NF onde exigido (Bom Sucesso 22.1).

**Na entrega e no recebimento**
19. Conseguir prova da entrega com data: DANFE carimbado/assinado pelo fiscal (recebimento provisório — art. 140, II, "a"). Fotografar.
20. Conferir se o edital exige que a NF só seja **protocolada** depois do recebimento definitivo (Bom Sucesso 22.1; São João do Paraíso 16.1: até o 5º dia útil do mês seguinte, com ofício). Se sim, protocolar no primeiro dia possível e guardar o protocolo.
21. Se algum item for recusado: substituir no prazo do edital (24 h em Coronel Xavier Chaves e Bocaiúva-ARP; 48 h em Bocaiúva e Belterra; 5 dias em Agrolândia) e pedir novo recebimento por escrito. Multa por atraso começa no 1º dia (Bom Sucesso 27.4.1: 5%).
22. Pedir a data do **recebimento definitivo / atesto** e cópia do termo (art. 140, II, "b"). Onde o edital não fixa prazo (Agrolândia, CXC, Irecê, SJP, Belterra), cobrar por e-mail a cada 5 dias úteis, educadamente e por escrito.

**Depois do atesto — a contagem do pagamento**
23. Calcular o vencimento a partir do evento certo do edital (atesto / apresentação / entrega + NF / 10º dia do mês seguinte) e registrar no sistema.
24. No vencimento + 1 dia útil sem crédito: e-mail ao gestor citando a cláusula e pedindo a posição na **ordem cronológica** publicada no site (art. 141, § 3º).
25. Se o atraso continuar: (a) pedir liberação da parte incontroversa (art. 143); (b) requerer, por escrito e como ME, a antecipação do art. 141, § 1º, II, demonstrando o risco de descontinuidade; (c) emitir fatura dos encargos moratórios onde o edital prevê (Bocaiúva 1% a.m.; Bom Sucesso e SJP 6% a.a.; Irecê correção pelo índice da Ata).
26. Aos **2 meses da emissão da NF** sem pagamento: notificação formal invocando o art. 137, § 2º, IV e § 3º, II — direito de suspender novos fornecimentos daquela Ata até regularizar. Antes disso, entregar novo pedido daquele mesmo comprador é decisão de crédito, não obrigação cega.
27. Se for dezembro: garantir o **atesto antes de 31/12**. Empenhada e liquidada vira "restos a pagar processados" (não cancela, em regra — MCASP 4.7.3); entregue sem atesto vira "não processado" e pode ser anulada pela norma do próprio município (MCASP 4.7.2).

**Sempre**
28. Nunca desligar as certidões: renovar antes de cada empenho e de cada pagamento.
29. Nunca aceitar pedido acima do saldo da Ata (Decreto 11.462, art. 23: "vedado efetuar acréscimos nos quantitativos").
30. Preço ficou inviável? Pedido escrito de revisão com planilha (Decreto 11.462, art. 27 e cláusula equivalente do edital) **antes** do próximo empenho; recusar empenho sem isso é inadimplemento total (art. 90, § 5º; multa de 20% em Bom Sucesso 27.1 e Bocaiúva 15.1).

---

## Open points (UNVERIFIED)

1. Days between homologação and convocação in practice — no clause bounds it.
2. Whether Agrolândia, Coronel Xavier Chaves, Irecê, São João do Paraíso or Belterra have a municipal regulamento fixing recebimento definitivo deadlines (art. 140, § 3º).
3. The municipal year-end rule for cancelling RPNP in each of the seven municípios.
4. The default interest rate a court would apply where the edital has no clause (Agrolândia, CXC, Belterra).
5. Whether each fundo (FMS/FMAS) invoices under its own CNPJ or the prefeitura's.
6. The Paracatu/MG item 11.1.2 text cited in the handoff — not in the repo; the equivalent clauses are quoted in stage 5.
7. PNCP Family B per-item result endpoints — 503 throughout 2026-09-19; the "resultado" view could not be read.

## Sources read in full today
- Lei 14.133/2021 — <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm> (arts. 71, 82–86, 89–95, 115, 117, 137–145)
- Lei 4.320/1964 — <https://www.planalto.gov.br/ccivil_03/leis/l4320.htm> (arts. 35–37, 58–65)
- Decreto 11.462/2023 — <https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/d11462.htm> (arts. 1, 18–29)
- Decreto 93.872/1986 — <https://www.planalto.gov.br/ccivil_03/decreto/d93872.htm> (arts. 67–69)
- LC 101/2000, art. 42 — <https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm>
- STN, MCASP 10ª edição (2023), Parte I, itens 4.4.2 e 4.7 — <https://www.tesourotransparente.gov.br/publicacoes/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp/2024/26>
- NF-e MOC 7.0, Anexo I — <https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=ndIjl+iEFdE=> (groups B, C, E, I05, N10c, Z, ZB)
- PNCP API consulta v1 — `/v1/atas`, `/v1/contratos` (200 on 2026-09-19), `/v1/orgaos/{cnpj}/compras/{ano}/{seq}` (per `data/editais/README.md`)
- The seven editais in `data/editais/*.txt`, clauses quoted above by number.
