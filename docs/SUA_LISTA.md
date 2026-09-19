# Your list — what only you can decide, and what each one unlocks

One page. **Four of these are free and take minutes.** Two cost money. Three are
questions for someone else. Nothing here is urgent except the Simples window in §3,
and that clock only starts the day you open the company.

Everything not on this page is mine, and it is already moving.

---

## 1 · Two numbers — free, five minutes

| | What | Why it matters |
|---|---|---|
| ☐ | **How much cash can this business use?** | Right now the system says *"capital unknown"* and refuses to confirm you could fund a lot you win. One number turns that into a real answer: how many kits per order, how many orders per year. It is a **dial, not a commitment** — change it any time. Goes in `config/capital.yaml`. |
| ☐ | **What net margin makes a deal worth your time?** | The model defaults to 15%. It is your number, not mine. It decides what "pencils" means, and what price a tender has to reach before the system tells you to bid. Cell **C33** of the deal model. |

---

## 2 · Two permissions — free, one word each

You told me: ask before contacting any supplier. So I am asking. **Both cost R$0**
and I write the emails; you read them before anything is sent.

| | What | Why it matters |
|---|---|---|
| ☐ | **Email ~15 SP wholesalers for account (revenda) pricing** | This is the **single biggest swing in the whole business.** The R$198,78 kit is built on *published retail-facing catalogue prices.* The wholesale tier is rumoured to be ~45% below that — **completely unverified.** If it is real, a deal that today nets 0,6% nets 25%+. If it is not real, we need to know now, not after a win. |
| ☐ | **Ask one SP co-packer for a per-kit quote** | I surveyed 24 providers. **Not one publishes a price.** Without a number, every lot above ~240 kits comes back **NO BID** — the system refuses to guess. One quote unlocks the entire large-lot half of the market, and also tells us their lead time, which decides whether short-deadline tenders are possible at all. |

---

## 3 · The company — R$219–1.013 once, 10–15 business days

Only start this when you want to actually bid. Then it runs in one sequence:

| | Step | Notes |
|---|---|---|
| ☐ | **Ltda ME at JUCESP** | **R$218,99** (Portaria JUCESP 146/2025, ME/EPP rate, DARE 370-0). 11 CNAEs already chosen and checked against the Simples exclusion lists — they are in `config/cnaes.yaml`. **MEI is not an option**: the ceiling is R$81k and wholesale trade is not on the permitted list. |
| ☐ | ⚠️ **Opt into Simples Nacional** | **30 days from the last inscrição deferral, and never more than 60 days from the CNPJ date.** Miss it and you are in Lucro Presumido until January — that is the one genuinely unforgiving deadline in this whole business. Put the date in your phone the day the CNPJ comes out. |
| ☐ | **e-CNPJ A1 certificate** | **R$203–275/year.** The only spend that is strictly mandatory to submit a bid. *Cora offers it free* when you open and move a business account there — requires a CNH. |
| ☐ | **Business bank account** | Cora and Nubank are both R$0/month with free Pix and boletos. |
| ☐ | **Find a contador** | ~R$136–200/month published. Needed for the balanço, which some editais demand. |

**Then everything else is free.** All eight certidões cost R$0. SICAF is free.
Compras.gov.br is free to register *and* to bid. BLL charges only if you win.
After that the only recurring costs are the contador and ~R$30/month of small taxes.

---

## 4 · One sale — free, whenever, removes a real wall

| | What | Why it matters |
|---|---|---|
| ☐ | **Sell a few kits to any organisation and get a signed declaration** | Six of seven real editais ask for an *atestado de capacidade técnica* — proof you have supplied something similar before. Day one, you have none. **The law does not require the buyer to be a government body** (Lei 14.133 art. 67, and §2 forbids limits on when or where). A creche, an ONG, a maternidade, a friend's company — one real sale, one signed page, and that wall is gone permanently. |

---

## 5 · Later — only when the system goes live

Held until Monday tells us whether PNCP's item feed is coming back. I will ask again then.

| | What | Why |
|---|---|---|
| ☐ | Google service-account JSON | So the daily sheet updates itself instead of living in a file nobody opens |
| ☐ | An email API key | So a missing email means the system broke, not that the market was quiet |

---

## 6 · Three questions for your contador — ask once, at the first meeting

| | Question | What rides on it |
|---|---|---|
| ☐ | Does assembling a kit count as *industrialização por encomenda*? | If yes: Anexo II + IPI instead of Anexo I. **Worth 2–5 margin points.** Nobody has asked this yet. |
| ☐ | Does the TFE (R$362,95/yr) apply to a PJ at a home address? | The city's page answers this only for individuals. Budgeted as if yes. |
| ☐ | Is a balanço de abertura enough for a first-year company? | Some editais want a balance sheet; a new company files an opening one. |

---

## What is NOT on your list

Because it is mine, and it is done or moving: the scanner, the filters, the thirteen
admission rules, the buyer payment screen, the pricing engine, the freight
measurements, the certidão expiry tracker, the habilitação document pack, the daily
workbook, the bid log, the legal research, and the deal model.

**The honest state of the business:** it can find tenders and decide whether to bid
on them. It cannot yet read item lists — PNCP's feed for that has been down since
Friday, and I check again Monday morning. And the kit's true cost depends on §2
above, which is why those two emails are the most valuable thing on this page.

---

*Sources for every number here: `docs/COMPANY_SETUP.md`, `docs/HABILITACAO.md`,
`docs/BUSINESS_OPERATING_SYSTEM.md`, `docs/RISK_REGISTER.md`.
Nothing on this list has been done, spent, or sent.*
