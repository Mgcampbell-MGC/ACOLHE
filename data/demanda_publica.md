# The demand side of the kit-natalidade market

**Researched 2026-09-21 by an HTTP-only agent. Nobody was contacted.** Published
sources only: statute text from Planalto, TSE jurisprudence, CNAS resolutions,
IBGE/SIDRA APIs, the FNAS's own guidance, and the PNCP public API. Every number
below carries the URL it came from. Numbers I *derived* are marked and the
arithmetic is shown. Where a thing could not be established, it says so; §6 is
the register of those, and §7 the register of sources that would not load.

**Read §0 first.** The single most important methodological fact in this file is
that PNCP's search API caps every query at 600 rows and sorts by *last-update*
date, so most counts you can build from it are samples, not censuses — and the
project's existing `data/market/tenders.json` is one of those samples.

---

## 0. What the measurement rails actually are, and what they can bear

| Rail | What it gives | What it cannot give |
|---|---|---|
| `pncp.gov.br/api/search` | full-text match over published editais/contratos; a `total` count per query | more than **600 rows** per query (12 pages × 50 — measured, every query hit it); no date filter (tested: `data_publicacao_pncp_inicial`, `dataInicial` are silently ignored); `ordenacao=-data` sorts by **data_atualizacao**, not publication |
| PNCP Family B (`/orgaos/{cnpj}/compras/{ano}/{seq}/itens`, `.../resultados`) | item lists, quantities, estimated and **homologated** unit prices, winner CNPJ and porte | only for one purchase at a time; the bare `/compras/{ano}/{seq}` endpoint 301s |
| PNCP contract search + `/contratos/{ano}/{seq}` | **supplier name and CNPJ** on signed contracts — the supplier name *is* indexed by the search, verified below | contracts only; an SRP ata with no contrato published is invisible |
| IBGE SIDRA / servicodados APIs | births, population by income class, municipality list | nothing about who buys kits |

**Consequence for this file.** Three different PNCP datasets appear below and
they are *not* interchangeable:

- **Sample R** — `data/market/tenders.json`, the project's existing harvest.
  Seven relevance-ranked queries, **every one capped at 600**. Useful for
  *presence* (this municipality bought a kit at least once) and for the geographic
  spread. **Useless for any time trend**, because a relevance ranking is not a
  random or complete sample of years.
- **Window W** — my own date-ordered pull of the query `kit enxoval`, which
  returned 543 distinct rows whose oldest `data_atualizacao` is **2025-09-29**.
  Since `data_atualizacao ≥ data_publicacao` always, every edital matching that
  query **published on or after 2025-10-01 is in the set**. Window W is therefore
  a *complete* 12-month census for that one query phrasing, and is the only rail
  here on which a month-by-month or year-on-year statement is defensible.
- **Contracts C** — my own pull of PNCP *contratos* matching four kit phrasings,
  each resolved to its supplier CNPJ. Used only for §5.

---

## 1. How big is this, really?

### 1.1 How many municipalities buy kits

| Measure | Value | Basis |
|---|---|---|
| Municipalities in Brazil | **5.571** entries | [IBGE localidades API](https://servicodados.ibge.gov.br/api/v1/localidades/municipios), read 2026-09-21 — CALCULATED as `len()` of the response. (The conventional figure is 5.570 municipalities; the API's extra row is Brasília/DF.) |
| Distinct municipalities with ≥1 kit edital on PNCP, **2022–2026** | **≥ 1.124** — **20,2 % of all municipalities** | CALCULATED from Sample R (1.982-row snapshot taken 2026-09-21 ~16:3x, all 7 queries; filtered to 1.750 genuine kit objects by the regex in §8), `data/market/tenders.json` |
| Distinct municipalities with a kit edital in **one 12-month window**, from **one query phrasing** | **372** | CALCULATED from Window W — see 1.3 |
| Kit editais published in that same 12-month window | **442** | CALCULATED from Window W |

CALCULATED: 1.124 ÷ 5.571 = 20,17 %.

Geographic spread of those 1.124 (CALCULATED from Sample R): MG 117, SP 110,
PR 108, BA 105, MA 74, GO 63, CE 60, RN 56, PA 53, PE 51, PI 47, PB 37, SE 32,
ES 29, RJ 29, AL 27, RS 27, MT 26, MS 25, SC 22, TO 12, AP 5, AM 5, RO 3, RR 1.
**Every state is represented.** 1.724 of the 1.750 editais are municipal;
**311 of 1.750 (17,8 %) are published by an órgão whose name contains "FUNDO"**,
which corroborates — but does not establish — the project's working assumption
that the buying entity is often the Fundo Municipal de Assistência Social and
therefore carries a different CNPJ from the prefeitura.

**These are floors, and the gap between them and the truth is large and
unmeasured.** Window W uses a single phrasing. The full-text `total` counts PNCP
reports for the other phrasings, read 2026-09-21 from
`https://pncp.gov.br/api/search/?tipos_documento=edital&q=...`, are:

| Query | `total` editais reported |
|---|---|
| `kit natalidade` | 2.776 |
| `kit maternidade` | 1.605 |
| `kit gestante` | 1.468 |
| `kit enxoval` | 1.321 |
| `enxoval bebe` / `enxoval para bebe` | 1.229 / 1.229 |
| `enxoval recem nascido` | 775 |

Those totals include false positives (PNCP's full text matches loosely — the
`kit natalidade` result set contains "materiais de expediente" rows), so they are
**not** a count of kit tenders. They are evidence that the true population is in
the low thousands of editais, not the hundreds, and that **no single pull can see
all of it**.

**What is safe to say:** **at least 1.124 Brazilian municipalities — one in five —
have published a newborn-kit tender on PNCP since 2022**, and **at least 372
publish one in any given twelve months**. Both are floors from capped samples;
the true numbers are higher by an unknown margin, and there is no published
census that would settle them (see §6).

### 1.2 Births, and births in the target income bracket

| Item | Value | Source |
|---|---|---|
| Nascidos vivos ocorridos no ano, Brasil **2024** | **2.370.945** | [IBGE SIDRA tabela 2612, variável 218](https://apisidra.ibge.gov.br/values/t/2612/n1/all/v/218/p/2024/c2/0) |
| 2023 | 2.518.039 | same |
| 2022 | 2.537.078 | same |
| 2021 | 2.630.703 | same |
| 2020 | 2.673.913 | same |
| 2019 | 2.806.483 | same |

**Births are falling: −15,5 % from 2019 to 2024** (CALCULATED:
2.370.945 ÷ 2.806.483 − 1 = −15,52 %). A supplier's unit of demand is shrinking
about 3 % a year.

Income bracket — Censo 2022, population living in private households, by
**per-capita household income class**
([IBGE SIDRA tabela 10296](https://apisidra.ibge.gov.br/values/t/10296/n1/all/v/13604,1013604/p/2022/c2/6794/c86/95251/c386/all)):

| Class | People | Share |
|---|---|---|
| Até ¼ salário mínimo | 21.081.892 | 10,43 % |
| Mais de ¼ a ½ SM | 37.359.033 | 18,49 % |
| Sem rendimento | 5.771.024 | 2,86 % |
| **Total** | **202.044.547** | 100 % |

CALCULATED: share at **≤ ½ SM per capita = 10,43 + 18,49 = 28,92 %**;
at **≤ ¼ SM = 10,43 %**.

**IBGE does not publish births cross-tabulated by household income**, so the
number of births in the target bracket cannot be read. It can only be estimated,
and the estimate rests on an assumption that is probably wrong in a known
direction.

### 1.3 The spend arithmetic — two routes, and why the gap matters

**Route A — top-down ceiling.** Assumptions, each of which may fail:

1. Births distribute across income classes like the general population.
   *This is the weak link: fertility is higher in lower-income households, so
   this understates the eligible cohort.*
2. Every eligible birth receives a benefit.
   *False — coverage is far from universal.*
3. Every benefit is in kind, not cash. *False, and getting more false — see §2.4.*
4. Unit price = R$ 359,05, the price Itaquaquecetuba actually paid in 2026.

```
births 2024                        2.370.945
× share ≤ ½ SM per capita (28,92%) =   685.677 births      [CALCULATED]
× R$ 359,05 per kit                = R$ 246,2 milhões/ano  [CALCULATED]

narrower cut, ≤ ¼ SM (10,43%)      =   247.289 births      [CALCULATED]
× R$ 359,05                        = R$  88,8 milhões/ano  [CALCULATED]
```

So the **absolute ceiling on the in-kind newborn-kit market is roughly
R$ 90–250 million a year**, and the real figure is materially below it because
assumptions 2 and 3 are both false. Anyone quoting the top of that range is
quoting a number that assumes 100 % coverage and zero cash benefits.

**Route B — bottom-up measured floor.** Contracts actually signed and published
on PNCP in the twelve months to 2026-09-21, matching four kit phrasings and
filtered to genuine kit objects: **202 contracts, R$ 13.778.293,38, across 126
buying órgãos and 120 suppliers** (CALCULATED from Contracts C — §5.4). That is a
hard floor and a deep undercount: it sees only contracts matching four phrasings,
and an SRP ata with no `contrato` record published is invisible to it — the
Itaquaquecetuba award of R$ 1.795.250 is itself missing from it.

**The honest statement of market size:** the *ceiling* is around
**R$ 250 million a year**, the *observable contract-published floor* is about
**R$ 14 million a year**, and the truth is somewhere between. **This research
could not narrow it further**, because neither the number of municipalities
running a programme nor their average coverage rate is published anywhere I could
reach. A useful middle marker: the four largest *state* programmes found (§4.3 —
two of them verified as central purchases on PNCP, two from official figures)
are worth on the order of **R$ 50–60 million a year**, which already
exceeds the entire contract-published municipal floor — so the true total is
plainly in the high tens of millions at minimum, and the 20 % of municipalities
seen tendering (§1.1) suggests it is materially higher than that.

### 1.4 Three real clearing prices — the most useful numbers in this file

All three read from PNCP `/itens/{n}/resultados`, all three **lote único**
(the whole kit priced as one line, menor preço):

| Buyer | Year | Qty | Estimated R$/kit | **Homologated R$/kit** | Clearing | Winner (porte) |
|---|---|---|---|---|---|---|
| [Itaquaquecetuba/SP](https://pncp.gov.br/app/editais/46316600000164/2025/447) | 2025/26 | 5.000 | 476,05 | **359,05** | **75,42 %** | CONDAFE (EPP) |
| [RS — Mãe Gaúcha](https://pncp.gov.br/app/editais/87958658000199/2025/976) | 2025 | **80.000** | 778,42 | **602,28** | **77,37 %** | RS Comércio e Prest. de Serviços de Apoio SA (Demais) |
| [MG — SES, Filhos de Minas](https://pncp.gov.br/app/editais/18715516000188/2024/133) | 2024 | **38.760** | 435,00 | **322,49** | **74,14 %** | Brink Mobil Equipamentos Educacionais (Demais) |

CALCULATED clearing ratios: 359,05/476,05 = 75,42 %; 602,28/778,42 = 77,37 %;
322,49/435,00 = 74,14 %.

**Three independent lote-único observations, three states, two years, clustering
at 74–77 %.** The project's "bid 75 % of estimate" rule now rests on three data
points rather than one. It is still three, not a distribution — but the spread is
tight and the sample spans an EPP win and two large-firm wins.

---

## 2. What governs the money

### 2.1 The statute

**LOAS (Lei 8.742/1993), art. 22, in its current wording (Lei 12.435/2011)** —
[planalto.gov.br/ccivil_03/leis/l8742.htm](https://www.planalto.gov.br/ccivil_03/leis/l8742.htm):

> Art. 22. Entendem-se por benefícios eventuais as provisões suplementares e
> provisórias que integram organicamente as garantias do Suas e são prestadas aos
> cidadãos e às famílias em virtude de nascimento, morte, situações de
> vulnerabilidade temporária e de calamidade pública.
>
> § 1º A concessão e o valor dos benefícios de que trata este artigo serão
> definidos pelos Estados, Distrito Federal e Municípios e **previstos nas
> respectivas leis orçamentárias anuais**, com base em critérios e prazos
> definidos pelos respectivos Conselhos de Assistência Social.

**Correction to a premise this project has been carrying:** the "renda mensal per
capita inferior a 1/4 do salário mínimo" income test **is in the *original* 1993
text of art. 22 and was removed by Lei 12.435/2011**. The current federal statute
sets *no* income threshold for benefícios eventuais. Any ¼- or ½-SM cut-off you
meet in a tender comes from that municipality's own law or CMAS resolution, not
from LOAS. (Vitória/ES, for instance, still applies ¼ SM — §2.4.)

**Decreto 6.307/2007** —
[planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6307.htm](https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6307.htm):

- art. 1º §2º — concession and **value** of the natalidade and morte benefits are
  regulated by the state/DF/municipal Conselhos, on criteria set by the CNAS.
- art. 3º — the auxílio natalidade attends "preferencialmente" to (I) needs of the
  *nascituro*, (II) support to the mother on stillbirth or newborn death, (III)
  support to the family on the mother's death.
- art. 5º — **DF and Municípios** fund the auxílios natalidade and funeral.
- art. 6º — **Estados** transfer money to municipalities as *participação no custeio*.
- art. 9º — provisions tied to health, education or other sectoral policies are
  **not** benefícios eventuais. (Relevant: several of the state programmes in §4
  are run by the health secretariat, which puts them outside this regime.)

The decree is silent on kit-versus-cash. That question is answered by the CNAS.

### 2.2 Kit or cash: the CNAS changed the answer in October 2025

**Old rule — Resolução CNAS 212/2006** (DOU 27/10/2006), art. 6º:

> Art. 6º O benefício natalidade pode ocorrer na forma de pecúnia **ou** em bens
> de consumo.
> § 1º Os bens de consumo consistem no **enxoval do recém nascido**, incluindo
> itens de vestuário, utensílios para alimentação e de higiene…
> § 2º Quando o benefício natalidade for assegurado em pecúnia deve ter como
> referência valor das despesas previstas no parágrafo anterior.

Source: [LegisWeb transcription](https://www.legisweb.com.br/legislacao/?id=103281),
read 2026-09-21. That page also records that Resolução 212/2006 was **revogada
pela Resolução CNAS nº 81 de 11/10/2022**. This is the text that put the word
*enxoval* into Brazilian social-assistance law, and it put kit and cash on an
equal footing.

**New rule — Resolução CNAS nº 213, de 28 de outubro de 2025**, art. 2º § 1º:

> Os benefícios eventuais constituem provisões socioassistenciais a serem
> **preferencialmente garantidas em forma de pecúnia**, podendo ocorrer também em
> forma de bens e, excepcionalmente, como prestação de serviço.

Full text read from the copy published by
[jari.rs.gov.br/arqs/33030.pdf](https://www.jari.rs.gov.br/arqs/33030.pdf)
(a Rio Grande do Sul state circular carrying the resolution as an attachment;
the DOU original could not be opened — §7). Corroborated by
[CNM](https://cnm.org.br/comunicacao/noticias/resolucao-do-cnas-define-parametros-para-concessao-de-beneficios-eventuais-e-exige-adequacoes-municipais-ate-2026),
[MPPR](https://site.mppr.mp.br/assistenciasocial/Noticia/Resolucao-CNAS-no-2132025-novos-parametros-para-Beneficios-Eventuais)
and
[blogcnas.com](https://www.blogcnas.com/post/cnas-publica-resolu%C3%A7%C3%A3o-n%C2%BA-213-sobre-par%C3%A2metros-para-provis%C3%A3o-de-benef%C3%ADcios-eventuais).

Other provisions of Res. 213/2025 that bear on the business:

- **art. 35 — every municipal council and gestor must bring local rules into line
  within one year of publication**, i.e. by **28 October 2026 — five weeks from
  today.** Every municipality in the country is, right now, obliged to re-open and
  re-write the instrument that authorises its kit programme.
- art. 6º — **CadÚnico registration may not be required** as a condition of the
  benefit. Programmes that screened on CadÚnico must change.
- art. 14 — the natalidade provision must take account of twins, triplets,
  disability, and guarda/adoção/acolhimento situations (i.e. variable kit counts).
- arts. 21–23 — the **Conselho Estadual (CEAS)**, after pactuação in the CIB,
  approves the criteria for **state co-financing** of benefícios eventuais, and
  art. 23 requires that co-financing be **annual, systematic and regular**.
- art. 34 — gestores must report to the council **every six months** on the
  budget forecast and execution of benefícios eventuais.

**This is the most consequential fact in the file after the election rule.** A
national normative act, eleven months old, tells every municipal council in
Brazil that cash is the preferred form and kits the secondary one, and gives them
a deadline five weeks away to rewrite their rules accordingly. It does not ban
kits — art. 2º §1º explicitly keeps "bens" available, and art. 5º of
Decreto 6.307 still makes the municipality the funder. But the direction of
national policy is away from the product this business sells.

### 2.3 How it is funded — and which parts are stable

**Reading of the statute** (this is a reading, not a quotation of a rule that
says so in these words):

- **LOAS art. 15 I** — Municípios "destinar recursos financeiros para custeio do
  pagamento dos benefícios eventuais de que trata o art. 22".
- **LOAS art. 13 I** — Estados "destinar recursos financeiros aos Municípios, a
  título de **participação no custeio** do pagamento dos benefícios eventuais".
- **LOAS art. 12 II** — the União co-finances "o aprimoramento da gestão, os
  serviços, os programas e os projetos". **Benefícios eventuais are not in that
  list.**

The FNAS says it outright. **FNAS/MDS, *Fundos de Assistência Social* (2025),
section 5, "Aplicação dos recursos"** —
[fnas.mds.gov.br/wp-content/uploads/2025/08/Fundos-de-Assistencia-Social.pdf](https://fnas.mds.gov.br/wp-content/uploads/2025/08/Fundos-de-Assistencia-Social.pdf):

> Benefícios eventuais (como auxílio-funeral, cesta básica) – **Fonte de recursos
> do Tesouro Municipal e Cofinanciamento Estadual, sendo vedado o uso dos
> recursos federais.**

| Money source | Can it pay for a kit? | Stability year to year |
|---|---|---|
| Municipal own revenue (Tesouro Municipal) | **Yes** — the normal source | Depends entirely on the LOA and the mayor. This is the whole risk. |
| State co-financing (via FEAS, criteria set by CEAS) | **Yes** | Res. 213/2025 art. 23 *requires* it be annual and regular — but only where the state has chosen to co-finance at all |
| Federal FNAS cofinanciamento fundo a fundo (Piso Básico Fixo etc.) | **No — expressly vedado** | n/a |
| IGD-SUAS | **No** — it is management support (LOAS art. 12-A: "apoio financeiro à gestão"), not benefit funding | n/a |
| Emendas parlamentares | **Not established** — see §6 | Notoriously year-by-year |

**What this means for a supplier.** There is no federal money underwriting this
market. Every kit is bought with municipal own revenue, possibly topped up by the
state. That is the direct answer to "a programme that exists one year and not the
next": the funding is the least stable kind there is — a discretionary line in a
municipal budget, approved annually, with no federal floor beneath it. A
municipality that buys 500 kits this year has no obligation and no earmarked
transfer obliging it to buy any next year.

The counterweight is that PNCP shows **repeat behaviour**: in Sample R's 1.750
genuine editais, 692 municipalities appear once, **305 twice, 84 three times,
29 four times and 14 five or more times** — i.e. **432 of 1.124 (38,4 %) bought
more than once** (CALCULATED). But a capped sample cannot tell you whether those
repeats are consecutive years or two purchases in one year, and 38 % is a floor
on repeat-buying, not an estimate of it.

### 2.4 Cash instead of a kit: a worked municipal example

**Vitória/ES** pays the natalidade benefit **in cash**, under Resolução 016/2017
of the Conselho Municipal de Assistência Social (COMASV), requested at the CRAS
within 90 days of birth, paid within 60 days of request, to families with
**renda per capita ≤ ¼ do salário mínimo** —
[Carta de Serviços de Vitória](https://cartadeservicos.vitoria.es.gov.br/areas/1-Assistencia-Social/servicos/894-Auxilio-Natalidade/)
and [m.vitoria.es.gov.br/semas/beneficio-por-natalidade](https://m.vitoria.es.gov.br/semas/beneficio-por-natalidade),
read 2026-09-21. The published pages do **not** state the value in reais (§6).

Vitória is not an outlier to be dismissed; it is the form Resolução 213/2025 now
calls "preferential". A municipality that switches from kit to cash removes itself
from this market permanently and at zero cost.

### 2.5 Is there a minimum percentage of the FMAS for benefícios eventuais?

**No such national rule was found.** Res. 213/2025 sets none; LOAS sets none;
Decreto 6.307 sets none. The only minimum-percentage rule found in this area is a
different one, and it is about **social control**, not benefits: the mandatory
minimum of IGD-PBF/IGD-SUAS resources that must be spent supporting the municipal
council, which
[CNM reports](https://www.amupe.org/2025/cnm-traz-alerta-sobre-conselho-municipal/)
rises from **3 % to 10 % with effect from January 2026**. That is a cost to the
municipality, not a floor under kit spending. **Marked UNVERIFIED** as to whether
any *state* imposes a minimum share for benefícios eventuais — states set their
own co-financing criteria via CEAS (Res. 213/2025 art. 21) and 27 state
resolutions were not checked.

---

## 3. Seasonality, and the election-year rule

### 3.1 The statute, verbatim

**Lei 9.504/1997, art. 73 § 10** (included by Lei 11.300/2006) —
[planalto.gov.br/ccivil_03/leis/l9504.htm](https://www.planalto.gov.br/ccivil_03/leis/l9504.htm):

> § 10. **No ano em que se realizar eleição, fica proibida a distribuição gratuita
> de bens, valores ou benefícios por parte da Administração Pública**, exceto nos
> casos de calamidade pública, de estado de emergência ou de **programas sociais
> autorizados em lei e já em execução orçamentária no exercício anterior**, casos
> em que o Ministério Público poderá promover o acompanhamento de sua execução
> financeira e administrativa.
>
> § 11. Nos anos eleitorais, os programas sociais de que trata o § 10 não poderão
> ser executados por entidade nominalmente vinculada a candidato ou por esse
> mantida.

Penalty: § 4º multa of 5.000–100.000 UFIR; § 5º (redação da Lei 12.034/2009)
**cassação do registro ou do diploma** of the benefited candidate for breach of
the *caput* **or of § 10**; § 7º the conduct is also improbidade administrativa
under Lei 8.429 art. 11 I.

### 3.2 Does it bite on kit natalidade? Yes — and harder than expected

All quotations below are from the TSE's own *Temas Selecionados*, page
"Distribuição gratuita de bens, valores ou benefícios", **updated 15/6/2026**,
read 2026-09-21 —
[temasselecionados.tse.jus.br/.../distribuicao-gratuita-de-bens-valores-ou-beneficios](https://temasselecionados.tse.jus.br/temas-selecionados/condutas-vedadas-a-agentes-publicos/distribuicao-gratuita-de-bens-valores-ou-beneficios).

**(a) It applies in *any* election year, to *every* level of government.** This
is a **reading of the statute, not a quotation of a holding**: § 10 says "no ano
em que se realizar eleição" and binds "a Administração Pública" at large, whereas
§ 3º *expressly* confines the inciso VI restrictions to "agentes públicos das
esferas administrativas cujos cargos estejam em disputa". The absence of that
limitation in § 10 is the argument. The TSE's language points the same way —

> Doutrina e jurisprudência são uníssonas no sentido de que o § 10 do art. 73 da
> Lei 9.504/97 **aplica-se de forma indistinta a todos os agentes públicos**,
> alcançando parlamentares que recaiam nas vedações previstas.
> — Ac. de 26/9/2024 no AgR-REspEl n. 115, rel. Min. Isabel Gallotti

— though that case was about reaching *vereadores*, not about a municipality in a
federal election year. **I found no decision squarely on the point.** The reading
is that **2026, a federal/state election year, restricts municipalities too**, and
it is a reading a supplier should treat as probably right but not settled.

**(b) The exception needs a *specific* law — and a generic LOAS-style municipal
law is not enough.** This is the finding that matters most:

> …ratificou a compreensão de que a hipótese autorizadora do § 10 do art. 73 da
> Lei nº 9.504/1997 **somente se perfaz com autorização legislativa específica,
> não satisfazendo esse requisito a existência de dispositivo legal genérico
> previsto na Lei de Organização da Assistência Social**. […] o referido caso
> tratou de situação idêntica: lei municipal que constitui […] **"mera cópia da
> Lei Orgânica da Assistência Social – LOAS"**.
> — Ac. de 18.5.2023 no AREspE nº 060106560, rel. Min. Raul Araújo, applying
> REspEl nº 372-75/ES, rel. Min. Alexandre de Moraes

**(c) Budget provision is not enough; the programme must have actually been
executed the year before.**

> O art. 73, § 10, da Lei n. 9.504/1997 exige, **cumulativamente**, autorização em
> lei específica e execução orçamentária no exercício anterior […]. A execução
> orçamentária pressupõe não apenas previsão, mas **efetiva implementação** do
> programa no exercício anterior ao pleito, sendo inadmissível sua comprovação por
> presunções ou probabilidades.
> — Ac. de 14/5/2026 no AgR-REspEl n. 060064110

**(d) The offence is objective — no electoral intent need be shown.**

> A norma em questão configura **ilícito de natureza objetiva, não exigindo
> demonstração de finalidade eleitoral**.
> — RO-El n. 060165574 (2025); same in the cestas básicas line of cases

**(e) Scaling up an existing programme is itself a risk.** Increasing 500 to 761
cestas was **allowed** (Ac. 1º.3.2011, AgR-REspe n. 999874789 — the programme was
already running), but a **400 % increase** in assistance spending against the
prior year, on generic vulnerability reports, was held to be conduta vedada *and*
abuso de poder (Ac. de 16/4/2026 no AgR-PetCiv n. 060103478).

### 3.3 What that means in practice for a supplier

**The restriction is on the *distribution*, not on the *procurement*.** The
statute prohibits "a distribuição gratuita de bens" — it does not prohibit
running a licitação. A municipality may lawfully tender and buy in an election
year; what it may not do is hand the goods out unless its programme clears the
two-part test. In practice the two are joined: a buyer that cannot distribute has
no reason to buy.

**The operational reading, which a bidder can apply from published documents:**

| The buyer's legal basis is… | Position in an election year |
|---|---|
| A **specific municipal law** creating a named programme (e.g. *Programa Mãe Itaquá*), executed with real spending in the prior year | Within the exception. Safe. |
| A **CMAS resolução** alone, with no municipal law | **Outside the exception** — a resolução is not "lei" |
| A **generic municipal law on benefícios eventuais** that reproduces LOAS | **Outside the exception**, per AREspE 060106560 |
| A programme **launched in the election year itself** | Outside the exception, squarely |

**This inverts a premise the project has been carrying.** The working assumption
has been that the typical legal basis is "a benefício eventual created by a
resolução do CMAS rather than a branded programme". If that is right for most
buyers, then *most* of this market is legally exposed in an election year, and
the *branded* programmes — Mãe Itaquá, Mãe Gaúcha, Nascer Bem — are the safe ones.
**How many buyers have a specific law versus a generic one was not measured and
would have to be read edital by edital** (§6).

### 3.4 Did 2026 actually chill the market? Measured: no

Window W — every PNCP edital matching `kit enxoval`, published **2025-10-01 to
2026-09-21**, filtered to genuine newborn-kit objects. **442 editais, 372 distinct
municipalities, 436 of 442 municipal.**

| Month | Editais | | Month | Editais |
|---|---|---|---|---|
| 2025-10 | 43 | | 2026-04 | 49 |
| 2025-11 | 35 | | 2026-05 | 32 |
| 2025-12 | 38 | | 2026-06 | 44 |
| 2026-01 | **20** | | 2026-07 | 33 |
| 2026-02 | 34 | | 2026-08 | 34 |
| 2026-03 | **57** | | 2026-09 (21 days) | 23 |

CALCULATED: monthly mean Oct–Dec 2025 (non-election quarter) = (43+35+38)/3 =
**38,7**. Monthly mean Jan–Aug 2026 (complete months of the election year) =
(20+34+57+49+32+44+33+34)/8 = 303/8 = **37,9**. **A difference of 2 %.**

**The election year did not stop municipal kit procurement.** That is a measured
result on a complete window, not an inference from a sample. It is consistent
with the statute: buying is not prohibited, and the programmes that survive are
the ones with a specific law and prior-year execution — which is most of the ones
that were already running.

**Seasonality within the window:** January is the trough (20, roughly half the
mean) and **March is the peak (57)**. That is the shape you would expect from the
budget cycle: the LOA is approved in December, empenhos cannot run until the new
exercise opens, and the first wave of tenders lands in Feb–April. A supplier's
quiet month is January and the busiest quarter is Q1–Q2.

**Do not over-read this.** It is one query phrasing over one year. A year-on-year
comparison across 2024 (municipal election) / 2025 / 2026 **could not be built**,
because the search rail cannot produce complete windows that far back (§0, §6).
The apparent −29 % in 2026 that Sample R suggests is **an artefact of relevance
ranking and should not be used**.

### 3.5 One observed, dated side-effect worth knowing

Fetching the Paraná state news portal on 2026-09-21 returned, in place of the
article:

> Em cumprimento à **Lei Federal nº 9.504/1997**, este portal manterá
> temporariamente indisponíveis os conteúdos de comunicação institucional durante
> o **período de vedação eleitoral**.
> — [parana.pr.gov.br/aen](https://www.parana.pr.gov.br/aen/Noticia/Com-carrinhos-e-acessorios-Estado-inicia-distribuicao-inedita-de-10-mil-kits-para-maes)

That is art. 73 VI "b" (publicidade institucional in the three months before the
poll), not § 10. It matters operationally: **state programme pages are being taken
offline right now**, which is why several sources in §4 and §7 would not load. A
supplier researching state programmes between July and October of an election year
will find the evidence missing.

---

## 4. State-level programmes

**The key distinction is who signs the contract.** A state that buys centrally is
one customer with a tender of 40.000–80.000 kits; a state that funds
municipalities leaves the tenders where they were. The evidence below is PNCP
purchase records wherever possible, because press releases do not say who
contracts.

### 4.1 States that buy centrally — verified from PNCP

| State | Programme | Purchase | Qty | Est R$/kit | Homol R$/kit | Winner |
|---|---|---|---|---|---|---|
| **RS** | **Mãe Gaúcha** | [Subsec. da Administração Central de Licitações, PE 976/2025](https://pncp.gov.br/app/editais/87958658000199/2025/976) — object literally "KIT ENXOVAL - MATERNIDADE - PROGRAMA MÃE GAÚCHA" | **80.000** | 778,42 | **602,28** | RS Comércio e Prestação de Serviços de Apoio SA, CNPJ 17.112.698/0001-30, porte *Demais* |
| **MG** | **Filhos de Minas** | [Secretaria de Estado da Saúde, PE 133/2024](https://pncp.gov.br/app/editais/18715516000188/2024/133) — "COMPRA ESTADUAL - KIT ENXOVAL BEBÊ" | **38.760** | 435,00 | **322,49** | Brink Mobil Equipamentos Educacionais Ltda, CNPJ 79.788.766/0025-00, porte *Demais* |
| **BA** | (unnamed) | [Estado da Bahia, PE 934/2024](https://pncp.gov.br/app/editais/13937032000160/2024/934) and [PE 1047/2024](https://pncp.gov.br/app/editais/13937032000160/2024/1047), "kits enxoval auxílio natalidade" | small per-item lots (120 kits on 1047) | — | per item | C I Alves Barreto & Cia (ME) won all 17 items of 1047 |
| **ES** | (unnamed) | [Estado do Espírito Santo, PE 465/2024](https://pncp.gov.br/app/editais/27080530000143/2024/465), "kit enxoval recém nascido" | 500–1.000 per item | — | per item | split across 4 MEs |
| **RR** | **Colo de Mãe** | [SELC, Dispensa 233/2025](https://pncp.gov.br/app/editais/53212344000120/2025/233) — banheiras "para compor o kit enxoval… Programa Colo de Mãe", Secretaria de Estado do Trabalho e Bem-Estar Social | 2.365 banheiras | 25,73 | 25,73 | Icamiabas Serviços (ME) |
| **RJ** | (unnamed) | [Estado do Rio de Janeiro, PE 1584/2023](https://pncp.gov.br/app/editais/42498600000171/2023/1584) — "kits de enxoval para recém-nascido (Kits Maternidade)" | — | — | — | not resolved |

**The MG figure independently verifies the press number.** Agência Minas reported
Filhos de Minas as 38.760 kits for R$ 12,5 mi (that page returned 503 — the figure
is from a search-engine snippet of `agenciaminas.mg.gov.br`, §7); PNCP shows a
2024 SES purchase of exactly **38.760 kits homologated at R$ 12.499.712,40**. The
two match to the unit, which is the strongest cross-validation in this file: the
press number *is* the homologated contract, not an estimate.

### 4.2 States running a programme where the buying model is not confirmed

| State | Programme | Scale | Secretaria | Source |
|---|---|---|---|---|
| **PR** | **Nascer Bem Paraná**, launched Sep/2025 | **16.000 kits**, ≈ **R$ 10 milhões**, **222 municípios**; 2.810 kits delivered in 156 municípios by early 2026; kit includes a **carrinho de bebê** | Sedef (desenvolvimento social) | [parana.pr.gov.br/aen](https://www.parana.pr.gov.br/aen/Noticia/Nascer-Bem-Parana-ja-entregou-28-mil-kits-com-carrinhos-de-bebe-em-156-municipios) — **page currently withheld under the electoral rule; figures read from search-engine snippets of the official domain, not from the page itself** |
| **MA** | **Maranhão Acolhe**, launched 20/12/2025 | **9.000 kits planned for 2026**, **45 items**, distributed through **maternidades**, starting at MACMA | **Secretaria de Estado da Saúde** | [saude.ma.gov.br](https://www.saude.ma.gov.br/noticias/governo-lanca-programa-maranhao-acolhe-e-entrega-enxovais-para-maes-atendidas-na-macma/) |
| **GO** | **OVG — Enxovais de Bebê** (Organização das Voluntárias de Goiás) | 15-piece cotton kit, delivered in a nylon bag; linked to *Meninas de Luz* | OVG | [ovg.org.br](https://www.ovg.org.br/site/?programas=enxovais-de-bebe) — **the page states the kits are produced by costureiras and volunteers, i.e. made in-house rather than procured. Not a market.** |
| **PE** | **Mãe Coruja Pernambucana** | integrated maternal-infant network; kit component not confirmed | multi-secretaria | search result only; **not verified from an official page** |

CALCULATED for PR: R$ 10.000.000 ÷ 16.000 kits = **R$ 625 per kit** — the highest
unit value found, consistent with a kit containing a pushchair.

### 4.3 What the state layer is worth, and what it does to a one-person supplier

Adding the four largest state programmes found: RS 80.000 + MG 38.760 +
PR 16.000 + MA 9.000 = **143.760 kits** (CALCULATED). **This mixes bases and is
indicative only:** RS and MG are single-tender quantities verified on PNCP, PR and
MA are programme-year targets from official communications, and the PR and MA
buying models are unconfirmed. At the RS/MG homologated prices that is on the
order of **R$ 50–60 million** — a large share of the whole measured market,
concentrated into a handful of tenders.

**And those tenders are the ones a one-person business cannot win.** Both
central purchases verified on PNCP went to firms of porte *Demais* (large). 80.000 kits at
602,28 is R$ 48 million of working capital and a logistics operation. The
centralising state is a *competitor for the demand*, not a customer: every
municipality that receives state kits is a municipality that stops tendering.

**The countervailing observation:** the smaller state purchases (BA, ES, RR) were
split into per-item lots and won by **MEs**. Where a state buys per item rather
than as a lote, the small supplier is back in the game.

### 4.4 A caution about PNCP's `esfera` field

Do not read "Estadual" as "the state is buying". Several rows labelled Estadual
are **municipal purchases transacted through a state's central platform CNPJ** —
e.g. [Estado de Minas Gerais, Dispensa 620/2023](https://pncp.gov.br/app/editais/18715615000160/2023/620)
whose object is "KIT AUXILIO NATALIDADE PARA A SECRETARIA DE ASSISTÊNCIA SOCIAL
DO **MUNICÍPIO DE ALTO CAPARAÓ/MG**". Read the object text, not the label.

---

## 5. Who else is in this market

### 5.1 CONDAFE resolved

**CONDAFE COMÉRCIO DE ROUPAS LTDA (EPP), CNPJ 10.430.444/0001-10.** PNCP's
contract search indexes the supplier name: a search for `CONDAFE` over
`tipos_documento=contrato` returns **47 contracts, and all 47 resolve to CNPJ
10.430.444/0001-10** when each is fetched from
`/api/pncp/v1/orgaos/{cnpj}/contratos/{ano}/{seq}` — so the match is on the
supplier, not on the object text. Verified 2026-09-21.

| CONDAFE, PNCP-published contracts | Value |
|---|---|
| Contracts found | **47** |
| Total contracted value | **R$ 5.742.116,59** (CALCULATED: sum of `valorGlobal`) |
| Median contract | **R$ 40.500,00** (CALCULATED) |
| Years covered | 2025 (31), 2026 (16) |
| States | **16 UFs** — SP 10, RJ 7, PR 6, MG 5, AL 4, RS 2, PE 2, ES 2, MS 2, and one each in GO, TO, PB, BA, PI, RN, MA |

Largest: [Recife/PE 2026, R$ 1.483.726,91](https://pncp.gov.br/app/contratos/10565000000192/2026/57)
("ENXOVAL INFANTIL"); [Mossoró/RN 2025, R$ 785.040,00](https://pncp.gov.br/app/contratos/14928192000105/2025/16);
[Rio de Janeiro/RJ 2026, R$ 370.161,00](https://pncp.gov.br/app/contratos/42498733000148/2026/491);
[Volta Redonda/RJ 2025, R$ 349.713,00](https://pncp.gov.br/app/contratos/29063294000182/2025/14).

**Note the Itaquaquecetuba 5.000-kit award (R$ 1.795.250) is *not* in that
R$ 5,74 M** — it was an SRP with no `contrato` record retrieved by this search.
CONDAFE's real volume is higher than the figure above.

**What CONDAFE is:** a clothing wholesaler (`comércio de roupas`) that supplies
kits among other textile lines — its contract list also includes lençóis,
colchonetes and cama-e-banho. It is an **EPP that operates in sixteen states**.
That is the shape of the incumbent: not a giant, not local.

### 5.2 The large-lot specialists

The two verified state central purchases went to firms of porte *Demais*:

- **RS Comércio e Prestação de Serviços de Apoio SA**, CNPJ 17.112.698/0001-30 —
  80.000 kits, R$ 48.182.400.
- **Brink Mobil Equipamentos Educacionais Ltda**, CNPJ 79.788.766/0025-00 —
  38.760 kits, R$ 12.499.712,40. A school-equipment supplier, not a baby-goods
  firm: evidence that **large public-sector generalists cross into this category
  when the lot is big enough**. It is also, by CNPJ root, the **single most
  frequent kit-contract winner in Contracts C — 41 contracts** across several
  filiais (§5.4), so it is both the biggest and the busiest player found.

### 5.3 The long tail

Per-item state lots went to micro-firms: C I Alves Barreto & Cia (ME) took all 17
items of BA 1047/2024; Espírito Santo's 20-item tender split across **João e
Maria Ateliê (ME), Comercial Têxtil DFM (ME), Maximus Comércio (ME), Barra
Comércio de Equipamentos (ME)**; Icamiabas Serviços (ME) took Roraima's banheiras.

### 5.4 Concentration, measured

**Contracts C** — every PNCP *contrato* matching four kit phrasings, each resolved
to its supplier CNPJ. **536 contracts pulled, 536 suppliers resolved (100 %),
463 of them genuine kit objects** after the §8 regex. Signature years: 2024 (111),
2025 (212), 2026 (132), plus 8 earlier.

| Measure | Value |
|---|---|
| Kit contracts with a resolved supplier | **463** |
| Distinct buying órgãos | **233** |
| Distinct supplier companies (CNPJ) | **242** |
| Distinct supplier **groups** (CNPJ root, merging filiais) | **239** |
| Total contracted value | **R$ 28.417.598,82** |
| **Median** contract | **R$ 17.091,97** |
| Mean contract | R$ 61.377,10 |
| Largest single contract | R$ 2.016.000,00 |
| Signed in the 12 months to 2026-09-21 | **202 contracts, R$ 13.778.293,38, 126 buyers, 120 suppliers** |

All CALCULATED from Contracts C.

**Concentration, by CNPJ root:**

| | Share of contracts | Share of value |
|---|---|---|
| Top 1 group | 8,9 % | 8,3 % |
| Top 3 | 18,1 % | 21,5 % |
| Top 5 | 22,9 % | 29,9 % |
| Top 10 | 29,8 % | 43,1 % |
| **HHI** | **181** | **278** |

CALCULATED. For reference, competition authorities generally treat a market below
HHI 1.500 as *unconcentrated*; this one is an order of magnitude below that.

**The long tail is the market.** CALCULATED from Contracts C:

- **174 of 239 supplier groups (72,8 %) hold exactly one contract.**
- Only **32 groups** hold three or more.
- Only **10 of 239 groups (4,2 %) operate in three or more states.**
- Of 400 distinct buyer–supplier pairs, only **56 recur** — i.e. **86 % of
  buyer–supplier relationships are one-off.** Incumbency buys you very little.

**The most frequent winners:**

| Contracts | Value | CNPJ root | Name |
|---|---|---|---|
| 41 | R$ 2.140.688,62 | 79.788.766 | **Brink Mobil Equipamentos Educacionais** |
| 31 | R$ 934.661,55 | 51.689.269 | AMA Comércio e Serviços |
| 12 | R$ 180.632,75 | 23.379.637 | Comercial Higi Tex |
| 11 | R$ 242.812,30 | 08.974.702 | Comercial Debeche Têxtil (EPP) |
| 11 | R$ 1.613.817,00 | 10.430.444 | **CONDAFE Comércio de Roupas** |
| 7 | R$ 27.838,00 | 32.294.249 | G. C. Amorim Confecções |
| 7 | R$ 169.757,90 | 19.980.359 | Comercial Têxtil DFM |

(CONDAFE shows 11 here rather than the 47 of §5.1 because Contracts C is filtered
by *object text*, while the §5.1 pull searched the *supplier name*. The two agree:
11 of CONDAFE's 47 contracts describe themselves as kit purchases.)

**The biggest single contracts went to firms with almost no repeat presence:**
DUCS Comércio, Serviços e Importações took R$ 2.352.000,00 across just 2
contracts; Master Comércio e Serviço R$ 1.463.960,00 on **one**; S G Pontes Aguiar
R$ 820.950,00 on one; Megamix Comércio de Papelaria R$ 596.057,00 on one.
**A single large tender can be won by a firm with no track record in the
category** — which is the most directly encouraging fact in this section for a
new entrant, and the clearest evidence that the category has no gatekeepers.

### 5.5 The structural answer

**Measured: this is not a concentrated market. HHI 181 by contract count, 278 by
value; 72,8 % of suppliers hold a single contract; 86 % of buyer–supplier
relationships are one-off. It is an open field with a two-tier shape.**

- **Tier 1 — a handful of very large, infrequent lots** (state central
  purchases, and large municipalities like Itaquaquecetuba). Won by firms with
  capital: two of the three biggest observed went to *Demais*-porte companies, and
  the one that went to an EPP (CONDAFE at Itaquaquecetuba) went to an EPP that
  already operates in sixteen states.
- **Tier 2 — a very long tail of small municipal purchases**, median in the tens
  of thousands of reais, won overwhelmingly by ME/EPP firms, often local.

**A newcomer is entering an open field in Tier 2 and a hard one in Tier 1 —
though not a closed one:** four of the ten largest contracts in Contracts C went
to firms holding one or two contracts in the whole dataset.

The encouraging fact recorded in `ITAQUAQUECETUBA_REAL.md` — "a small company won
it" — is true but needs its qualifier: the EPP that won 5.000 kits in São Paulo is
a national operator with 47 contracts in 16 states, not a beginner. The genuinely
encouraging fact is the structural one: **with 239 supplier groups, no group
holding more than 9 % of contracts, and most relationships one-off, there is no
incumbent whose position a newcomer has to dislodge.** What decides entry here is
price and habilitação, not relationships.

---

## 6. What could not be established

1. **No census of municipalities running a kit/auxílio-natalidade programme
   exists that I could reach.** The obvious source — Censo SUAS, Gestão Municipal
   questionnaire, which does collect a benefits block — publishes its results
   through MDS portals that returned *Conteúdo Restrito*, HTTP 503 or empty
   replies throughout (§7), and the dados.gov.br API requires a key (HTTP 401).
   The only coverage statistic found is second-hand and eleven years old:
   **Censo SUAS 2009–2013, 25 % of municipalities still had no regulating
   instrument for benefícios eventuais** — CFESS, *Nota Técnica sobre benefícios
   eventuais* (2020), citing Gomes (2015, p. 05),
   [cfess.org.br](https://www.cfess.org.br/arquivos/NotaTecnicaBeneficiosEventuais2020.pdf).
   That is about regulation of *all* benefícios eventuais, not about kits, and it
   is a decade stale. **It should not be used as a market size.**
2. **Births by household income bracket.** IBGE publishes births by mother's age
   and education, not by income. The §1.3 figure is an estimate resting on an
   assumption known to be wrong in a knowable direction.
3. **Total annual spend.** Only bounded (§1.3), not measured.
4. **Year-on-year trend, and therefore the 2024-vs-2025-vs-2026 election
   comparison.** PNCP's search caps at 600 rows and sorts by update date; a
   complete window older than about twelve months cannot be built from it. The
   within-2026 result in §3.4 stands; the cross-year one does not exist.
5. **What share of buyers have a *specific* municipal law versus a generic one.**
   This is the variable that decides election-year exposure (§3.3) and it is only
   readable edital by edital, from each buyer's cited legal basis.
   **This is the single most valuable unfinished piece of work in this file**, and
   it is cheap: every edital states its legal basis, and the PNCP `/arquivos`
   endpoint already works.
12. **Whether art. 73 § 10 has ever been applied to a municipality in a *federal*
    election year.** No decision on that exact fact pattern was found (§3.2 (a));
    the conclusion there is a reading of the statute, not a holding.
6. **Whether emendas parlamentares fund kit purchases, and how much.** PNCP
   carries a `possui_emenda_parlamentar` field but it is **null on 778 of 779 rows**
   in Sample R, so the rail exists and is unpopulated. Not measurable from PNCP
   today.
7. **The value of Vitória/ES's cash benefit in reais**, and how many municipalities
   pay cash rather than kits. No national tally of the kit-versus-cash split exists.
8. **Whether any state imposes a minimum share of the municipal fund for
   benefícios eventuais.** 27 CEAS resolutions not checked.
9. **PR Nascer Bem and RS Mãe Gaúcha programme pages** could not be read directly;
   the PR figures here come from search-engine snippets of the official domain
   while the page itself is withheld under the electoral publicity rule (§3.5).
   The RS programme is nonetheless verified independently through its PNCP
   purchase.
10. **The DOU original of Resolução CNAS 213/2025.** The text used is a faithful
    copy published by a state government; the in.gov.br page would not open (§7).
11. **PE Mãe Coruja's kit component** — search result only, no official page read.

---

## 7. Blocked-sources register

Recorded as blocked, not worked around. TLS verification was never disabled.

| Source | Symptom | Bearing |
|---|---|---|
| `planalto.gov.br` via WebFetch | HTTP 503 | worked around with `curl` — statutes obtained |
| `www.mds.gov.br/webarquivos/...` (Orientações Técnicas; Perguntas Frequentes; Resolução 212 PDF) | `curl: (52) Empty reply from server` on every retry | Res. 212 text obtained from LegisWeb instead; MDS FAQ not read |
| `gov.br/mds/.../censo-suas` and `.../beneficios-eventuais` | page renders **"Conteúdo Restrito"** | **Censo SUAS coverage numbers not obtained — this is gap #1** |
| `dados.gov.br` CKAN and public API | HTTP 401 (API key required) | Censo SUAS microdata not obtained |
| `redesuas.mds.gov.br/monitorasuas` | empty reply / HTTP 503 | MonitoraSUAS figures not obtained |
| `aplicacoes.mds.gov.br/sagirmps/...`, `/snas/regulacao/...` | empty reply / HTTP 503 | CNAS resolution originals not obtained from MDS |
| `in.gov.br` DOU article pages | returns a 1 KB stub | Res. 213/2025 DOU original not obtained |
| `www.desenvolvimentosocial.pr.gov.br` | HTTP 403 | PR programme page — see next row |
| `www.parana.pr.gov.br/aen/...` | HTTP 404 + banner: content withheld **"em cumprimento à Lei Federal nº 9.504/1997 … período de vedação eleitoral"** | PR figures fall back to search snippets. **This is itself a finding — §3.5** |
| `www.estado.rs.gov.br/...` (Mãe Gaúcha) | HTTP 404 | RS programme verified via PNCP instead |
| `www.saude.ma.gov.br/destaques/...` | HTTP 404 on one slug; the `/noticias/` slug worked | MA obtained |
| `agenciaminas.mg.gov.br` | 302 → `/comunicado`, then HTTP 503 | MG verified via PNCP instead |
| `cnm.org.br` via WebFetch | HTTP 403 | CNM content obtained via search results only |
| `www.jari.rs.gov.br` | first attempt `ws_closed_mid_exchange`, succeeded on retry | Res. 213/2025 obtained |
| `pncp.gov.br` | intermittent `curl (52)`, `RemoteDisconnected`, HTTP 301 on the bare `/compras/{ano}/{seq}` endpoint | worked around with the project's retrying client; **every failed call is recorded, no value was inferred from one** |

---

## 8. Provenance of the derived datasets

| Dataset | How built | Where |
|---|---|---|
| Sample R | pre-existing `tools/market_harvest.py` PASS 1, 7 relevance-ranked queries, all capped at 600 | `data/market/tenders.json` — **snapshot analysed: 1.982 rows taken 2026-09-21**, copied to scratchpad `sampleR_final.json`. The live file was being written by another process during this research, so every Sample R figure here refers to that frozen copy, not to whatever the file now contains |
| Window W | my own pull, `ordenacao=-data`, 12 pages × 50, query `kit enxoval`; 543 distinct rows, oldest `data_atualizacao` 2025-09-29; filtered to 478 genuine kit objects by regex, 442 of them published ≥ 2025-10-01 | scratchpad `recent.json`, `ke_window.json` |
| Contracts C | my own pull, `tipos_documento=contrato`, queries `kit natalidade`, `kit enxoval bebe`, `enxoval recem nascido`, `kit maternidade gestante`; 536 candidates, **all 536 resolved** to a supplier CNPJ, 463 genuine kit objects after the regex | scratchpad `contratos.json`, `contratos_hit.json` |
| CONDAFE set | `tipos_documento=contrato`, `q=CONDAFE`, 47 rows, each resolved | scratchpad `condafe.json` |
| State purchases | PNCP `/itens` + `/itens/{n}/resultados` for 8 named state compras | scratchpad `estaduais.json` |

The regex used to separate genuine kit objects from PNCP's loose full-text
matches, so it can be audited:

```
POS = (KIT|KITS)\s*(DE\s*)?(NATALIDADE|MATERNIDADE|ENXOVAL|GESTANTE|BEB[EÊ]|RECEM)
      | ENXOVA(L|IS) | AUX[IÍ]LIO[- ]NATALIDADE
NEG = UNIFORME ESCOLAR | ENXOVAL HOSPITALAR | PROCESSAMENTO DE ENXOVAL
      | LOCA[CÇ][AÃ]O DE ENXOVAL | CERCA ELETRICA | ENXOVAL DE CAMA
      | CAMA, MESA E BANHO | ROUPARIA
```


---

## 9. The three facts that should most change a decision to enter

1. **CNAS Resolução 213/2025, art. 2º § 1º** makes *pecúnia* the preferred form of
   every benefício eventual and gives every municipal council until
   **28 October 2026** — five weeks from this writing — to rewrite its rules.
   Kits remain lawful, but national policy now points away from them. Nothing else
   found in this research threatens the product category itself. **§2.2**
2. **In an election year the exception in Lei 9.504/97 art. 73 § 10 requires a
   *specific* municipal law, and the TSE has expressly held that a municipal law
   that is "mera cópia da LOAS" does not qualify.** If most buyers rest on a CMAS
   resolução or a generic benefícios-eventuais law, most of this market is legally
   exposed every second year — and the *branded* programmes are the safe ones.
   Yet measurement says the chill did not arrive in 2026: procurement ran flat.
   Both halves of that need to be true at once, and reconciling them is the single
   most valuable further piece of work. **§3.2–§3.4**
3. **The supply side has no gatekeeper.** 239 supplier groups, HHI 181, 72,8 % of
   them holding one contract, 86 % of buyer–supplier relationships one-off, and
   four of the ten largest contracts won by firms with one or two contracts in
   total. Entry is decided by price and habilitação, not by incumbency. The
   offsetting fact is that the *large* lots — the state central purchases that
   account for a large share of the money — went to large firms, and every
   municipality a state supplies centrally is a municipality that stops tendering.
   **§4.3, §5.4, §5.5**

A fourth, quieter one: **births are falling 3 % a year** (§1.2). The unit of
demand shrinks even if every other variable holds.
