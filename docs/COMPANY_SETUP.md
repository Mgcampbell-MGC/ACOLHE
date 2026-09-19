# COMPANY_SETUP — ACOLHE COMÉRCIO DE ENXOVAIS LTDA

**Verification date:** 2026-09-19. Every figure below was read at the URL shown on that date. Nothing was registered, nobody was contacted, no money was spent.
**Currency:** PTAX venda 18/09/2026 = R$ 5,1575/US$ (BCB, <https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='09-18-2026'&$format=json>). Founder's budget US$ 500–2.500 = **R$ 2.579–12.894**, non-reloading.

**Source labels**
- `[STATUTE]` — text of a law/decree/resolution read on planalto.gov.br or an official RFB/DREI copy.
- `[OFFICIAL]` — a government page or gazette (gov.br, SEFAZ-SP, JUCESP/DOE-SP, Prefeitura de SP, IBGE).
- `[VENDOR]` — the seller's own price/terms page (certificadora, bank, contador, bidding portal). Prices move; re-read before paying.
- `[INFERENCE]` — my reading; not written anywhere in those words.
- **UNVERIFIED** — no primary source would give it; the note says what blocked it.

Builds on `docs/LEGAL_FINDINGS.md` (IN RFB 1.234/2012, art. 48 I, DIFAL, ST); that analysis is not repeated here.

---

## 0. Bottom line

| | Minimum path | Conservative path |
|---|---|---|
| **One-time, nothing → bid-ready** | **R$ 218,99** (US$ 42) | **R$ 1.012,89** (US$ 196) |
| **Fixed monthly** | **R$ 196** (US$ 38) | **R$ 473** (US$ 92) |
| **Elapsed time, decide → can submit a bid** | 5 business days | **10–15 business days (2–3 weeks)**; 30+ if JUCESP/SEFAZ raise an exigência |

Both one-time paths sit far below the US$ 500 floor of the budget. The recurring cost is dominated by the contador (R$ 136–225/month), not by tech (VPS R$ 30). Section 9 has the line-by-line table; section 11 lists every inherited figure that was wrong or out of date.

---

## 1. Legal entity and tax regime

**1.1 Vehicle: sociedade limitada with one sócia (SLU).** `[STATUTE]` Código Civil art. 1.052 §1º: "A sociedade limitada pode ser constituída por 1 (uma) ou mais pessoas" (Lei 13.874/2019). <https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm>. No statutory minimum capital for a limitada (arts. 997, 1.052–1.055 set none).

**1.2 ME ceiling.** `[STATUTE]` LC 123 art. 3º I: microempresa = receita bruta anual ≤ **R$ 360.000,00**; EPP from R$ 360.000,01 to R$ 4.800.000,00. <https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm>. The ME/EPP enquadramento is declared at the Junta (it is what triggers the reduced JUCESP fee in 3.1 and the LC 123 art. 48 benefits); the Simples opt-in is a separate act (1.5).

**1.3 Anexo I effective rates — CONFIRMED, all four inherited numbers are right.** `[STATUTE]` LC 123, Anexo I (redação da LC 155/2016, vigência 01/01/2018), same URL:

| Faixa | RBT12 | Alíquota nominal | Parcela a deduzir |
|---|---|---|---|
| 1ª | até 180.000,00 | 4,00% | – |
| 2ª | 180.000,01 a 360.000,00 | 7,30% | 5.940,00 |
| 3ª | 360.000,01 a 720.000,00 | 9,50% | 13.860,00 |
| 4ª | 720.000,01 a 1.800.000,00 | 10,70% | 22.500,00 |

Effective rate = (RBT12 × nominal − dedução) / RBT12 (LC 123 art. 18 §1º-A):
- RBT12 R$ 180.000 → **4,00%** ✔
- RBT12 R$ 360.000 → (26.280 − 5.940)/360.000 = **5,65%** ✔
- RBT12 R$ 500.000 → (47.500 − 13.860)/500.000 = **6,73%** ✔
- RBT12 R$ 720.000 → (68.400 − 13.860)/720.000 = **7,58%** ✔

Repartição 1ª/2ª faixa: IRPJ 5,50 / CSLL 3,50 / Cofins 12,74 / PIS 2,76 / CPP 41,50 / **ICMS 34,00%** (the ICMS share is what a monofásica/ST product removes — see LEGAL_FINDINGS §4).

**1.4 Does LC 227/2026 change Anexo I for 2026? NO.** `[STATUTE]`
- LC 227/2026 amends LC 123 through its **art. 169** (<https://www.planalto.gov.br/ccivil_03/leis/lcp/Lcp227.htm>). The compiled LC 123 on Planalto carries LC 227 markers on **arts. 18 (inciso VI, "Vide"), 22 (caput and new incisos IV–VI: repasse do IBS), 31 §4º ("Vide"), 33 (caput), 39 (caput, §5º) and 41 (two incisos revoked)**. None touches Anexo I, art. 18 §1º-A (the effective-rate formula) or art. 18-A §1º.
- Timing: **LC 227 art. 182, I, b: art. 169 produces effects only from 1º de janeiro de 2027.** So every LC 227 change to LC 123 is dormant in 2026.
- Separately, LC 214/2025 (IBS/CBS) also amends LC 123 (its art. 517: Anexos I–V gain IBS/CBS columns, art. 18 §4º rewritten). LC 214 art. 544, III (as amended by LC 227): art. 517 effects from **1º de janeiro de 2027** as well. <https://www.planalto.gov.br/ccivil_03/leis/lcp/Lcp214.htm>.
- **Correction to LEGAL_FINDINGS §6.6:** it lists "35, §4º" among the LC 227 hits; the compiled text carries no LC 227 marker on art. 35. The list should read arts. 18, 22, 31, 33, 39, 41. Cosmetic — no effect on rates.
- `[INFERENCE]` For 2027 planning: the Simples ICMS share (34%) becomes ICMS+IBS+CBS shares; the total Anexo I nominal rates as published today do not change, but the crédito the municipality can take and the "opção pelo regime regular de IBS/CBS" (LC 123 art. 18 §4º as amended) become a pricing question. Not a 2026 issue.

**1.5 Simples opt-in window for a new company.** `[STATUTE]` LC 123 art. 16 §3º: the option "produzirá efeitos a partir da data do início de atividade, desde que exercida nos termos, prazo e condições a serem estabelecidos no ato do Comitê Gestor". Resolução CGSN 140/2018 art. 6º §5º I (redação Res. CGSN 150/2019): after the CNPJ, the ME must formalise the option **"no prazo de até 30 (trinta) dias, contado do último deferimento de inscrição, seja ela a municipal ou, caso exigível, a estadual, desde que não ultrapasse 60 (sessenta) dias da data de abertura constante do CNPJ"**. Read on the Receita Estadual/RS consolidated Simples legislation PDF, p. 83 (<https://atendimento.receita.rs.gov.br/upload/arquivos/202508/22150110-legislacao-setorial-consolidada-ges-sn-v01.pdf>) — an official state-tax copy, because the RFB's own viewer (normas.receita.fazenda.gov.br → normasinternet2) is a JavaScript app that returned no text (see §12). **Miss this window and the company is in Lucro Presumido until January.**

**1.6 MEI is out — CONFIRMED on both counts.**
- `[STATUTE]` LC 123 art. 18-A §1º: "considera-se MEI quem tenha auferido receita bruta, no ano-calendário anterior, de até **R$ 81.000,00** (oitenta e um mil reais)" (redação LC 188/2021; no LC 227 marker). Planalto URL above.
- `[STATUTE]` Resolução CGSN 140/2018 **Anexo XI** (ocupações permitidas ao MEI): the string "ATACAD" occurs **0 times** in the RFB copy (<https://www8.receita.fazenda.gov.br/simplesnacional/arquivos/manual/anexo_xi.pdf>, 43 pp.) and 0 times in the RFB SIJUT copy (<https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=64455>, 34 pp.). The gov.br MEI activity list also has 0 hits (<https://www.gov.br/empresas-e-negocios/pt-br/empreendedor/quero-ser-mei/atividades-permitidas>).

---

## 2. CNAEs — register these (details and index entries in `config/cnaes.yaml`)

Source: IBGE CONCLA CNAE 2.3 via the IBGE data API `[OFFICIAL]` (<https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/{code}>; the interactive CONCLA page returned 403 behind a JS challenge). Simples check: none of these codes appears in CGSN 140 **Anexo VI** (impeditivos) or **Anexo VII** (ambíguos) — read at <https://www.gov.br/empresas-e-negocios/pt-br/drei/arquivos/AnexoVI.pdf> and <https://www.gov.br/empresas-e-negocios/pt-br/drei/arquivos/AnexoVII.pdf> `[STATUTE]`. All are revenda de mercadorias → LC 123 art. 18 §4º I → Anexo I.

| Family | Wholesale (atacado) | Retail (varejo) | IBGE index entry that proves coverage |
|---|---|---|---|
| Vestuário / enxoval | **4642-7/01** (principal) | 4781-4/00 | "ENXOVAL; COMÉRCIO ATACADISTA DE" / "ENXOVAL; COMÉRCIO VAREJISTA" |
| Cama, mesa e banho | 4641-9/02 | 4755-5/03 | "LENÇOL, FRONHA, COBERTOR, COLCHA E SIMILARES" |
| Higiene pessoal (fralda, sabonete, talco) | 4646-0/02 | 4772-5/00 | "FRALDAS DESCARTÁVEIS", "SABONETES", "TALCO" |
| Cosméticos (cremes, loções, óleo infantil) | 4646-0/01 | 4772-5/00 | "CREMES E LOÇÕES" |
| Brinquedos | **4649-4/99** (no dedicated atacado code exists) | 4763-6/01 | "BRINQUEDOS DE QUALQUER MATERIAL" |
| Puericultura (chupeta, mamadeira, mordedor, carrinho, banheira plástica) | **4649-4/99** | 4789-0/99 (carrinhos) | "CHUPETA, MAMADEIRA, MORDEDOR", "CARRINHOS DE BEBE", "ARTIGOS DE BORRACHA E PLÁSTICO PARA USO DOMÉSTICO" |
| Kit misto (catch-all) | 4693-1/00 | – | "MERCADORIAS EM GERAL, SEM PREDOMINÂNCIA DE ALIMENTOS" |

Two findings the inherited checklist did not have: (i) **there is no CNAE "atacado de brinquedos" or "atacado de puericultura"** — IBGE indexes both under 4649-4/99, so that single code is the wholesale cover for toys, puericultura and the bathtub; (ii) pomada para assaduras registered at ANVISA as medicamento would fall under 4644-3/01 (atacado de medicamentos, AFE required) — check the product's registration before bidding it; the yaml excludes that code on purpose.

---

## 3. Opening the company (Redesim / VRE|Redesim SP / JUCESP)

**3.1 JUCESP fee — 2026 table.** `[OFFICIAL]` Portaria JUCESP nº 146, de 19/12/2025 (DOE-SP 22/12/2025), Anexo I, item **2.1 "Contrato Social … (Empresa enquadrada em ME ou EPP)": 5,70 UFESP = R$ 218,99**, paid by **DARE código 370-0**; item 2 (não-ME) R$ 273,55; **DARF column blank** for item 2 (no federal registration fee on the 2026 table). UFESP 2026 = R$ 38,42 (Comunicado Dicar-88/25, cited in the Portaria). <https://www.institucional.jucesp.sp.gov.br/downloads/Portaria%20n%C2%BA%20146%20-%20Tabela%20de%20Pre%C3%A7os%202026.pdf>. Item 2.4 confirms JUCESP runs **registro automático** for Ltda (ato sanatório within 30 days, isento). The old `jucesp.sp.gov.br/tabela.asp` (Deliberação 01/2005, R$ 54,00 + DARF R$ 5,06) is still online and is **out of date** — do not use it.

**3.2 Flow.** `[OFFICIAL]` gov.br Redesim: Passo 1 Viabilidade → Passo 2 Inscrição (DBE/coleta nacional, CNPJ) → Passo 3 Licenciamento. <https://www.gov.br/empresas-e-negocios/pt-br/redesim/abrir-cnpj>. In São Paulo the state integrator is VRE|Redesim (<https://vreredesim.sp.gov.br/home>, linked from the JUCESP home; its TLS handshake failed through this session's proxy, so its own pages are **UNVERIFIED** here). The Prefeitura de São Paulo confirms the integration: "o contribuinte consegue realizar todo o processo de registro, licenciamento, viabilidade, obtenção de CNPJ, e liberação de CCM por meio de uma mesma plataforma" (<https://prefeitura.sp.gov.br/web/fazenda/w/servicos/ccm/21137>, 29/03/2024).

**3.3 Time to CNPJ.** `[OFFICIAL]`
- Brazil, July/2026: **"23 horas é o tempo médio para abertura de empresas"; 73,7% opened in less than one day** (<https://www.gov.br/empresas-e-negocios/pt-br/mapa-de-empresas>). The same page warns that since Dec/2025 the new RFB "Módulo de Administração Tributária (MAT)" flow raised measured times.
- **São Paulo state: 1 dia e 10 horas** (2º quadrimestre 2025), the slowest state; national 21 h; viabilidade 9 h + registro 12 h (<https://www.gov.br/empresas-e-negocios/pt-br/mapa-de-empresas/boletins/mapa-de-empresas-boletim-2o-quadrimestre-2025.pdf>, pp. 6–7). A 2026 SP-specific figure sits only in the JS dashboard <https://estatistica.redesim.gov.br/tempos-abertura> (unreadable here) — **UNVERIFIED for 2026**.
- The Redesim clock excludes licences/alvará (<https://estatistica.redesim.gov.br/assets/docs/TextoInformativoTempoAberturaPJ.pdf>).

**3.4 Inscrição Estadual (SEFAZ-SP / Cadesp).** `[OFFICIAL]` Mandatory for any establishment with an ICMS activity (RICMS/2000 art. 19 ff.). Requested **inside the Redesim flow**, **"Taxa: Não há taxa."** Exigências, if any, are answered via SIPET; unanswered exigências → automatic indeferimento. The page publishes no processing time. <https://portal.fazenda.sp.gov.br/servicos/cadesp/Paginas/Abertura-de-Empresas.aspx>.

**3.5 CCM (Cadastro de Contribuintes Mobiliários, São Paulo capital).** `[OFFICIAL]` For PJ, done "exclusivamente pela internet, na página do Empreenda Fácil" (VRE); inscription due within 30 days of start (Lei 8.435/76). No fee is listed on the page → **R$ 0 (inferred from absence, not stated)**. <https://prefeitura.sp.gov.br/web/fazenda/w/servicos/ccm/21137>, <https://prefeitura.sp.gov.br/web/fazenda/w/servicos/ccm/2368>.

**3.6 TFE — a recurring municipal tax the inherited checklist missed.** `[OFFICIAL]` Taxa de Fiscalização de Estabelecimentos (Lei 13.477/2002), annual, due 10 July; owed by every PJ "que explore estabelecimento no município, cujo endereço seja comercial ou residencial aberto ao público". 2026 table, Seção 1: code **31402 "Outras atividades do comércio … ou não especificadas": R$ 362,95/ano**; 30902 (varejo de perfumaria e cosméticos) R$ 1.088,85. <https://prefeitura.sp.gov.br/web/taxas2026/tfe-taxa-de-fiscaliza%C3%A7%C3%A3o-de-estabelecimentos>, table <https://capital.sp.gov.br/documents/d/fazenda/tfe_ativ2026-pdf>. Whether a home-office PJ at a "residencial não aberto ao público" address escapes it is stated on the page only for Pessoas Físicas → **UNVERIFIED for PJ; budget R$ 362,95/yr** (≈ R$ 30/month) until the contador confirms.

**3.7 Digital signature to file the contrato social.** JUCESP's VRE requires a digital signature on the ato. Whether the free gov.br signature (conta prata/ouro) is accepted or an e-CPF (ICP-Brasil) is required could not be read (VRE blocked, §12) → **UNVERIFIED**; the conservative path budgets an e-CPF A1: Soluti R$ 160,00, Certisign R$ 186,90, Safeweb from R$ 195 `[VENDOR]` (URLs in §5).

---

## 4. Capital social

- Inherited plan: R$ 20–30.000 integralizado, her own money. No legal minimum (§1.1). It is not a cost — it sits in the company's bank account and buys stock.
- **Lei 14.133 art. 69 §4º — CONFIRMED verbatim** `[STATUTE]`: "A Administração, **nas compras para entrega futura e na execução de obras e serviços**, poderá estabelecer no edital a exigência de capital mínimo ou de patrimônio líquido mínimo equivalente a **até 10% (dez por cento) do valor estimado da contratação**." <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm>.
- `[INFERENCE]` Two consequences: (i) for **pronta entrega** the edital may not demand capital mínimo at all — the §4º list is exhaustive; (ii) where it applies, R$ 20.000 covers any lot with valor estimado ≤ R$ 200.000, i.e. every art. 48 I reserved lot (≤ R$ 80.000) with room to spare. §2º of the same article bans minimum prior faturamento (see LEGAL_FINDINGS §6.2).

---

## 5. Certificado digital e-CNPJ A1 — current prices (all `[VENDOR]`, read 2026-09-19)

| Certificadora | Product | Price | URL |
|---|---|---|---|
| **Cora (bank) voucher** | e-CNPJ A1 **or** A3 em nuvem, 1 year, issued by a partner AC | **R$ 0** — "Ganhe 1 ano de Certificado Digital ao abrir sua conta Cora"; requires opening **and moving** the account; **"Oferta válida apenas para titulares de CNH"**; voucher valid 30 days | <https://www.cora.com.br/certificado-digital/> |
| Valid | "e-CNPJ A1 + e-CPF Nuvem 4 meses (combo)" | R$ 203,00 promo (R$ 257,20 list); no standalone A1 price shown | <https://www.validcertificadora.com.br/> (read through the WebFetch tool; curl got 429) |
| Certisign | e-CNPJ PME A1, 12 months | R$ 219,90 à vista (12× R$ 18,33) | <https://www.certisign.com.br/> |
| Certisign | e-CNPJ A1, 12 months | R$ 274,90 à vista (12× R$ 22,91) | same |
| Soluti | "CERTIFICADO PJ A1" | R$ 235,00 | <https://www.soluti.com.br/> (loja.soluti.com.br reset the connection 3×) |
| Safeweb | e-CNPJ A1, 12 months | "A partir de R$ 275" | <https://www.safeweb.com.br/> |
| **Serasa Experian** | — | **No longer sells certificates**: "Não emitiremos novos certificados. Consulte a lista de certificadoras para emitir um novo certificado." | <https://serasa.certificadodigital.com.br/> |

Verdict: the inherited "R$ 200–300/year" band is right for a paid A1 (R$ 203–275); the floor is R$ 0 via Cora if she holds a CNH. Serasa must come off the list.

---

## 6. Conta PJ (all `[VENDOR]`, read 2026-09-19)

| Bank | Monthly fee | Pix | Boleto de cobrança | Accepts LTDA/SLU? | Source |
|---|---|---|---|---|---|
| **Cora** | R$ 0 ("Sem mensalidades ou taxa de manutenção"); R$ 12,99 only after 360 days with no transaction | Free, unlimited | Free; "Boleto para contas não MEI (apenas a partir do 101º boleto pago) R$ 1,90 por boleto pago" | Yes (PJ; MEI has its own tier) | <https://www.cora.com.br/>, fee table PDF <https://cms.cora.com.br/wp-content/uploads/2026/08/Tabela-de-valores-Cora.docx.pdf> |
| **Nubank (Nu Empresas)** | "Zero taxa de manutenção" | "Zero tarifa para envio ou recebimento via Pix" | "Zero tarifa para boletos de cobrança"; no quantity limit; value R$ 6,00–15.000,00 per boleto | "MEI, EI, EIRELI, LTDA, Sociedade Empresária Limitada e Empresário Individual Imobiliário" | <https://nubank.com.br/empresas/>, FAQ <https://nubank.com.br/empresas/perguntas> |
| **Inter Empresas** | "Conta PJ Digital Inter: completa e 100% gratuita" | "Pix gratuito e ilimitado" | "TEDs e boletos gratuitos por mês" — **quantity not published on the page → UNVERIFIED** | Yes: lists "LTDA — Sociedade Limitada (LTDA) e a Sociedade Limitada Unipessoal (SLU)" | <https://www.inter.co/empresas/conta-digital/pessoa-juridica/> |
| **C6 Bank** | — | — | — | — | **UNVERIFIED — every c6bank.com.br URL returned HTTP 403 (bot challenge) to curl and to WebFetch** |

`[INFERENCE]` Municipalities pay by ordem bancária/transfer, not boleto, so boleto limits are irrelevant to the core business; Pix/TED being free is what matters. Any of the three verified accounts works; Cora is the only one that also removes the certificate cost.

---

## 7. Contador

- CFC/CRC publish no fee table (cfc.org.br home checked; no "honorários" guidance) → the inherited "R$ 200–400/month" had no source.
- Published online-contador prices `[VENDOR]`, plan for comércio / Simples Nacional, lowest tier:
  - **Contabilix** — "Comércio", Simples: **Online R$ 136/mês** (promo; list R$ 199), Expert R$ 168 (R$ 279), Premium R$ 272 (R$ 399); "Faturamento ideal: até R$ 25.000/mês". <https://www.contabilix.com.br/planos>
  - **Contabilizei** — "planos a partir de **R$ 195/mês**" (Padrão), R$ 225, R$ 395; "Abertura de CNPJ grátis" with a plan. <https://www.contabilizei.com.br/>
  - **Agilize** — no price on the page ("Consulte nossos planos"); "abertura de empresa sem custo, mediante pagamento da primeira mensalidade". <https://agilize.com.br/>
- A traditional local escritório contábil: **UNVERIFIED** (no price page exists by construction).
- Corrected band: **R$ 136–225/month** at the entry tier; opening handled free by the same contador on a plan. The inherited R$ 200–400 was too high at the bottom and had no source at the top.

---

## 8. Bidding infrastructure (the checklist called it "first registrations")

- **SICAF / Compras.gov.br** `[OFFICIAL]`: "o Sicaf é 100% digital e GRATUITO!" <https://www.gov.br/compras/pt-br/sistemas/sicaf-digital>. Needed for federal buyers and for any municipality running its pregão on Compras.gov.br.
- **BLL** `[VENDOR]`: "Cadastro gratuito — R$ 0,00 para se cadastrar — Você paga somente se vencer — **1,5% limitado ao teto máximo de R$ 600,00 por lote**"; or Plano Trimestral **R$ 630,00/trimestre** (from 13/07/2026). <https://bll.org.br/para-fornecedor/>
- **BNC** `[VENDOR]`: "Plano de única participação R$ 118,80"; "Cadastro gratuito". <https://bnc.org.br/>
- **Portal de Compras Públicas** `[VENDOR]`: Mensal **R$ 165,00**; Anual R$ 1.650,00 (R$ 137,50/mês); **Crédito R$ 129,00 por processo** (30 days). <https://www.portaldecompraspublicas.com.br/fornecedores>
- `[INFERENCE]` Which portal a municipality uses is in each edital (rule 11 logs it). Start on the R$ 0 paths (Compras.gov.br + BLL êxito); buy a PCP credit only for a specific edital that passes the 11 rules. Lei 14.133 art. 87 §2º bans complementary cadastro *for access to the edital*, not platform use fees (LEGAL_FINDINGS §6.5).
- **IN RFB 1.234/2012 Anexo IV** — confirmed in the RFB multivigente copy archived by CGU `[STATUTE]`: "ANEXO IV — DECLARAÇÃO A SER APRESENTADA PELA PESSOA JURÍDICA CONSTANTE DO INCISO XI DO ART. 4º (REDAÇÃO DADA PELA INSTRUÇÃO NORMATIVA RFB Nº 1244, DE 30 DE JANEIRO DE 2012)"; art. 6º caput "no ato da assinatura do contrato … em 2 (duas) vias"; **art. 6º §5º "aplica-se no caso de prorrogação do contrato ou a cada novo contrato"** → filed **per contract**. <https://repositorio.cgu.gov.br/bitstream/1/41431/20/instrucao_normativa_1234_rfb_2012.pdf> (pp. 12, 29). Full analysis in LEGAL_FINDINGS §1; nothing there changes.

---

## 9. Cost table

### 9.1 One-time (nothing → bid-ready)

| # | Item | Minimum path | Conservative path | Label / source |
|---|---|---|---|---|
| 1 | JUCESP — registro do contrato social, ME/EPP (DARE 370-0) | **R$ 218,99** | R$ 218,99 | `[OFFICIAL]` Portaria JUCESP 146/2025 item 2.1 |
| 2 | Federal registration DARF | R$ 0 (column blank on the 2026 table) | R$ 0 | `[OFFICIAL]` same |
| 3 | Inscrição Estadual SEFAZ-SP | R$ 0 ("Não há taxa") | R$ 0 | `[OFFICIAL]` §3.4 |
| 4 | CCM São Paulo | R$ 0 (no fee listed) | R$ 0 | `[OFFICIAL]`/inferred §3.5 |
| 5 | Digital signature for the ato (gov.br vs e-CPF) | R$ 0 (gov.br, if accepted — UNVERIFIED) | R$ 195,00 (e-CPF A1 Safeweb; Soluti R$ 160) | `[VENDOR]` §3.7 |
| 6 | e-CNPJ A1 | R$ 0 (Cora voucher, CNH required) | R$ 274,90 (Certisign e-CNPJ A1) | `[VENDOR]` §5 |
| 7 | Contador — abertura | R$ 0 (free with plan) | R$ 195,00 (first month, Contabilizei, counted here as the setup cost) | `[VENDOR]` §7 |
| 8 | SICAF / Compras.gov.br | R$ 0 | R$ 0 | `[OFFICIAL]` §8 |
| 9 | BLL / BNC / PCP cadastro | R$ 0 (BLL êxito) | R$ 129,00 (one PCP credit) | `[VENDOR]` §8 |
| 10 | Capital social R$ 20–30.000 | not a cost (stays in the company) | – | §4 |
| | **Total** | **R$ 218,99 ≈ US$ 42** | **R$ 1.012,89 ≈ US$ 196** | PTAX 5,1575 |

Both are under the US$ 500 (R$ 2.579) floor. Contingency the budget can absorb without reloading: JUCESP exigência (isento within 30 days), a second certificate, a PCP monthly plan for a busy month.

### 9.2 Recurring monthly (fixed; DAS excluded because it is a % of revenue)

| # | Item | Low | High | Label / source |
|---|---|---|---|---|
| 1 | Contador | R$ 136 (Contabilix promo) | R$ 225 (Contabilizei 2nd tier) | `[VENDOR]` §7 |
| 2 | Conta PJ | R$ 0 | R$ 0 | `[VENDOR]` §6 |
| 3 | e-CNPJ amortised | R$ 0 (Cora) | R$ 23 (R$ 274,90/12) | `[VENDOR]` §5 |
| 4 | TFE São Paulo (R$ 362,95/yr, code 31402) | R$ 30 | R$ 30 | `[OFFICIAL]` §3.6 (PJ home-office applicability UNVERIFIED) |
| 5 | VPS | R$ 30 | R$ 30 | given |
| 6 | Bidding portal plan | R$ 0 (Compras.gov.br + BLL êxito) | R$ 165 (PCP mensal) | `[VENDOR]` §8 |
| | **Fixed total** | **R$ 196 ≈ US$ 38** | **R$ 473 ≈ US$ 92** | |
| 7 | DAS (Simples Anexo I) | 4,00% of receita bruta while RBT12 ≤ R$ 180k | 5,65% at R$ 360k | `[STATUTE]` §1.3 |
| 8 | BLL success fee | 1,5% of the lot, cap R$ 600 | per lot won | `[VENDOR]` §8 |

Annualised fixed cost: R$ 2.352–5.676. Sanity check against the business: a single R$ 30.000 lot at the BOM margin in `price/` covers a year of the low case.

---

## 10. Timeline — decide → can submit a bid

| Step | Depends on | Elapsed (business days) | Source for the duration |
|---|---|---|---|
| gov.br account (prata/ouro), decide name/CNAEs/capital, contrato social drafted (contador or DREI template) | – | day 0–1 | – |
| VRE|Redesim SP: viabilidade → DBE → contrato social signed → JUCESP registro automático → **CNPJ** | step 1 | **+1 to +2** (SP avg 1 d 10 h across viabilidade+registro; Brazil 23 h Jul/2026) | `[OFFICIAL]` §3.3 |
| IE (SEFAZ-SP, same flow) and CCM (VRE) deferred | CNPJ | +1 to +5 (no published SLA; SIPET exigência possible) | `[OFFICIAL]` §3.4–3.5, duration UNVERIFIED |
| Simples opt-in on the Portal do Simples Nacional | last inscription deferral | ≤ 30 days after the last deferral, ≤ 60 days after CNPJ | `[STATUTE]` §1.5 |
| Conta PJ opened and moved | CNPJ | +1 to +3 (Cora: "em menos de 7 minutos" to apply; verification not timed) | `[VENDOR]` §6 |
| e-CNPJ A1 issued (Cora voucher + partner videoconference, or bought) | CNPJ, bank | +1 to +5 | `[VENDOR]` §5 |
| SICAF, BLL/BNC/PCP cadastro; Anexo IV template; certidões (RFB/PGFN, FGTS via Conectividade Social with e-CNPJ, CNDT, estadual, municipal) | e-CNPJ | +1 to +3 | `[OFFICIAL]` §8 |
| **Can submit a bid** | all | **5 (optimistic) / 10–15 (realistic) / 30+ (an exigência at JUCESP or SEFAZ)** | |

Calendar: **2–3 weeks realistic.** The step most likely to slip is the IE, because SEFAZ-SP exigências are answered asynchronously through SIPET and there is no published processing time.

---

## 11. Corrections to the inherited checklist

| Inherited claim | Status | Corrected to | Where |
|---|---|---|---|
| Anexo I effective rates 4,00 / 5,65 / 6,73 / 7,58% | **Confirmed** | unchanged | §1.3 |
| LC 227/2026 "changed arts. 18, 22, 31, 33, 35, 39" | **Partly wrong** | markers on arts. 18, 22, 31, 33, 39, **41**; **no marker on art. 35**; and **none takes effect before 01/01/2027** (LC 227 art. 182 I b) | §1.4 |
| Any LC 227 effect on 2026 Anexo I rates | **None** | 2026 rates unchanged; LC 214 art. 517 changes also start 2027 | §1.4 |
| MEI ceiling R$ 81.000; Anexo XI "ATACADISTA" 0× | **Confirmed** | unchanged | §1.6 |
| Contador R$ 200–400/month | **Out of date / unsourced** | **R$ 136–225/month** at the entry tier (Contabilix, Contabilizei); opening free with a plan; local escritório UNVERIFIED | §7 |
| "Register SEVERAL CNAEs" (no codes given) | **Filled in** | 11 codes in `config/cnaes.yaml`; **no dedicated wholesale CNAE exists for brinquedos or puericultura — both are 4649-4/99**; all admitted to Simples (not in Anexo VI/VII) | §2 |
| Capital cap "10% of estimated value" (art. 69 §4º) | **Confirmed, with a scope note** | applies only to compras para **entrega futura** and obras/serviços; for pronta entrega it cannot be demanded at all | §4 |
| e-CNPJ A1 "R$ 200–300/year" | **Confirmed band; floor wrong; one vendor gone** | R$ 203–275 paid; **R$ 0 via Cora** (CNH required); **Serasa Experian no longer issues certificates** | §5 |
| Conta PJ "Cora / Nubank / Inter / C6" | **3 of 4 verified** | Cora, Nubank, Inter: R$ 0 monthly, free Pix, free boletos (Cora: first 100 paid; Inter quota unpublished). **C6: UNVERIFIED (403)** | §6 |
| JUCESP fees "(DARE/taxas)" (no number) | **Filled in** | **R$ 218,99** (ME/EPP, 5,70 UFESP, DARE 370-0), DARF nil; the 2005 table still online (R$ 54,00) is obsolete | §3.1 |
| Inscrição Estadual and CCM (no cost given) | **Filled in** | IE: "Não há taxa" (SEFAZ-SP); CCM: no fee listed, via VRE | §3.4–3.5 |
| "Realistic days to CNPJ" | **Filled in** | SP 1 d 10 h (2º quad. 2025); Brazil 23 h (Jul/2026); 2026 SP figure UNVERIFIED | §3.3 |
| IN RFB 1.234 Anexo IV per contract | **Confirmed** | art. 6º §5º; Anexo IV redação IN 1.244/2012 | §8 |
| Decreto 8.538 art. 3º; Lei 14.133 art. 65 §1º | **Confirmed verbatim** (re-read 2026-09-19): "Art. 3º Na habilitação em licitações para o fornecimento de bens para pronta entrega ou para a locação de materiais, não será exigida da microempresa ou da empresa de pequeno porte a apresentação de balanço patrimonial do último exercício social." <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/decreto/d8538.htm>; "§ 1º As empresas criadas no exercício financeiro da licitação deverão atender a todas as exigências da habilitação e ficarão autorizadas a substituir os demonstrativos contábeis pelo balanço de abertura." <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm> | unchanged; scope caveat in LEGAL_FINDINGS §6.3 still applies | – |
| (missing) TFE São Paulo | **Added** | R$ 362,95/yr, code 31402; PJ home-office applicability UNVERIFIED | §3.6 |
| (missing) bidding-portal fees | **Added** | SICAF free; BLL 1,5% cap R$ 600/lot or R$ 630/quarter; BNC R$ 118,80; PCP R$ 165/month or R$ 129/process | §8 |
| (missing) Simples opt-in window | **Added** | 30 days from last inscription deferral, ≤ 60 days from CNPJ (CGSN 140 art. 6º §5º I) | §1.5 |

---

## 12. What blocked me (method transparency)

- **normas.receita.fazenda.gov.br** (Res. CGSN 140 main text): `link.action` returns a redirect page to `normasinternet2.receita.fazenda.gov.br/#/…`, a JS app; its `/api/…` returned 403; `imprimir.action` returned 0 bytes. Anexos VI, VII and XI were read from the RFB `anexoOutros.action` PDFs and the DREI copies on gov.br; the art. 6º text from the Receita Estadual/RS consolidated PDF.
- **concla.ibge.gov.br**: 403 behind a JS challenge; used the IBGE data API instead (same dataset).
- **vreredesim.sp.gov.br**: TLS "unable to get local issuer certificate" through the session proxy (not disabled, as instructed); the state integrator's own pages are therefore unread.
- **estatistica.redesim.gov.br/tempos-abertura**: JS-only dashboard; used the gov.br Mapa de Empresas page and the 2º quadrimestre 2025 boletim.
- **c6bank.com.br**: 403 on every URL (curl and WebFetch). **validcertificadora.com.br**: 429 to curl, read via WebFetch. **loja.soluti.com.br**: connection reset ×3 (home page used). **serasa.certificadodigital.com.br**: reachable, and says it has exited the market.
- **in.gov.br** (DOU page for CGSN 140): 403. **jucesp.sp.gov.br** "Tabela de preços e prazos" link is `href="#"` on the home page; the 2026 table was found on `institucional.jucesp.sp.gov.br` via a gov.br-restricted search.
- **contabilizei.com.br/planos-e-precos** and **agilize.com.br/precos**: 404; prices taken from each home page.
- **portal.fazenda.sp.gov.br/servicos/ufesp** and **legislacao.fazenda.sp.gov.br** UFESP pages: 404; the 2026 UFESP (R$ 38,42) is quoted from the JUCESP Portaria, which cites Comunicado Dicar-88/25.
- No blog, no accounting-software content page and no aggregator was used for any number in this file.
