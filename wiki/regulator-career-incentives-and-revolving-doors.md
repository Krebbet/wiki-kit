# Regulator Career Incentives and Revolving Doors

Charles-Cadogan (arXiv 2610.08804, working paper dated 2026-10-08) models a regulator's prospective job at the regulated firm as a call option on firm value. Because the payoff is convex in firm value, the regulator gains from signals that raise value, leverage and volatility, and those same signals push the firm toward a high-vega "warning" or crash region. This gives the exit side of capture a contingent-claim formalisation, in which the regulator, not the industry, initiates the softness. The wiki-relevant empirical anchor is not the paper's own contribution but a cited quasi-experimental study (Kalmenovitz et al. 2025): about half of regulators in exposed agencies appear to respond to revolving-door incentives. **Treat the formal model as an assumption-driven illustration and the empirics as secondhand.**

**Evidence tier note.** The paper's own contribution is (b): a formal model with propositions, a stylised calibration that is explicitly "proof-of-concept, not estimated, not fit", and three bank-failure vignettes. Status: **un-refereed arXiv working paper**, single author (business-school finance theorist), funded by the Institute for Innovation and Technology Management. The only (a) content is **secondhand**: the Kalmenovitz, Dal Bo, Colonnello and related studies are reported through this paper and the primary studies were not read in the ingest. The SVB and Signature vignettes do not match the model's mechanism (see Caveats). Most claims below are therefore **[model]**.

## The option mechanism

**[model]** Regulator payoff is (alpha*V - K)+, with V firm value, alpha the equity-linked share of the future package (0 < alpha < 1) and K the current compensation (the strike). The unit is the individual regulator paired with one Merton-style levered firm; the public (taxpayer) is the implicit writer of the put. The borrowed logic is the Hall-Murphy executive-stock-option argument applied to a public agent.

**[model]** Chain of results:
- A regulatory signal theta raises firm value, debt and volatility. Assumption 2.2: debt rises proportionally faster than value when debt is weakly penalised (D_theta/D > V_theta/V). Assumption 2.5: signals raise volatility.
- Higher volatility raises option vega, lowers distance to default, and raises tail risk (Prop. 2.7).
- Prop. 2.3: the regulator trades consumer surplus for firm profit by steering the firm into the high-price regime to enhance the career option.
- Prop. 2.8 defines three regions by comparing the vega drift with the leverage drift: go-leverage, early warning, crash. A tight debt/distress penalty rho dampens or reverses the effect.

**[wiki synthesis]** The distinctive structural point is that the regulator needs no bribe, threat or demonstrated industry action. A standing labour-market prospect is enough, so the softness is endogenous to the regulator's own objective. Note that the model's central results are built in through Assumptions 2.2 and 2.5, which supply the conclusion (see Caveats).

## What the calibration shows, and does not

**[model — calibration, not evidence]** Parameters V0 = 1, alpha = 0.05, K = 0.030, D0 = 0.55, sigma0 = 0.20; V rises 8% per unit signal, D 15%, sigma 30%. Leverage L rises from 0.550 to 0.616 and option payoff from 0.020 to 0.028 as theta goes 0 to 2. A bank-like anchor (D0/V0 = 0.65, sigma0 = 0.25) gives a critical theta of 0.48 for a default probability above 5%. A Monte Carlo (10,000 draws) gives Pr{DD < 1.5} = 0.008. **Do not cite these numbers as findings.** The regions are produced by the assumed inequality, and the stopping-horizon panel is "not a full dynamic programming solution".

## The external empirical layer (secondhand)

**[empirical — reported via the paper, primary not read]**
- **Kalmenovitz et al. (2025):** payroll records on about 22 million US federal employees; bunching of salaries just below the 18 USC 207 post-employment-restriction threshold, a quasi-experimental design. In agencies with broad regulatory powers, limited political supervision and frequent contact with high-paying industries, **49% of regulators respond to revolving-door incentives, forgoing 7.4% of wage potential**. Revolvers initiate fewer enforcement actions and write rules with lower compliance costs.
- **Dal Bo (2006):** former FCC commissioners who take industry jobs raise support for industry by nearly 11% in their last year.
- Also cited without detail: Colonnello et al. (2023, European bank supervisory boards), Katic and Kim (2024), Emery and Faccio (2025, procurement renegotiation costs).
- **Counter-evidence cited by the paper itself:** Colonnello finds positive valuation and faster growth for firms with ex-industry supervisors, so the channel carries a private gain beside the tail-risk cost. Kempf (2020) finds mobility incentives can improve rating accuracy. Heims and Moxon argue capture claims need evidence on the mechanism, not just outcomes.

**[wiki synthesis]** The bunching design shows that regulators respond to the restriction threshold, i.e. that the incentive exists and is priced. It does not show that the response damages the public interest. Enforcement and rule-writing effects are reported in the same breath, but their identification is not described in the paper.

## Relation to the existing capture pages

**Extension.** [[regulatory-capture]] catalogues channels (rent-seeking, capture by threat, cultural capture, hardwiring, boundary manipulation) and records that Stigler's agency is a "passive instrument". This page adds an exit-side channel in which the regulator is an active rational agent. [[amakudari-and-institutionalized-capture]] is the institutionalised, ministry-run version of the same incentive; Kalmenovitz's US evidence is the informal-market analogue. The Japanese *wataridori* pattern (serial posts to dodge a cooling-off rule) is a warning that a US-style pay-threshold restriction can be routed around.

**Real tension, with Carpenter & Moss.** Their evidentiary test for diagnosing capture requires demonstrated industry intent and action, plus exclusion of innocent alternatives. This model needs neither: capture arises without industry action, from the regulator's own option. That makes it the mechanism-agnostic definition's hard case, since a diagnosis under the test would fail on the intent limb even where the incentive is real. The paper's own cited counter-readings (Heims and Moxon; Kempf) line up on the Carpenter & Moss side. **[wiki synthesis]** The two are reconcilable: the bunching evidence is a mechanism-level test of the kind Carpenter & Moss ask for, but the paper's firm-level tail-risk and bank-failure claims are not.

**Tension, with Stigler.** Stigler's model locates capture in industry organising costs against diffuse publics; here the industry's role is only to be a credible future employer. De Chiara and Schwarz (2021, cited) put it as "the revolving door publicly signals willingness to reward lenient regulators". This is a different supply-side mechanism, not a contradiction. Compare [[career-concerns-and-managerial-risk-taking]], where career concerns produce timidity; here the same career logic produces risk-seeking through convex outside pay, the opposite sign. **[wiki synthesis]** Whether career incentives yield caution or risk-taking depends on the shape of the payoff (concave reputation vs convex equity-linked option).

## Caveats that bound what this shows

1. **Un-refereed, single author.** Some propositions are loosely stated; Prop. 2.1 is an "isomorphism" with proof deferred to an abstract mechanism-design appendix.
2. **Conclusion assumed.** Assumption 2.5 (signals raise volatility) assumes the tail-risk result, and the Pr{V<0} step is loosely derived. The calibration regions follow from D_theta/D > V_theta/V.
3. **Calibration is not estimated.** See above.
4. **Vignettes do not match the mechanism.** Lehman is a supervisory vacuum (the voluntary SEC CSE programme). At SVB the CEO sat on the San Francisco Fed's board in 2019, and the Fed post-mortem found tailoring after the 2018 EGRRCPA reduced supervisory assertiveness. At Signature, Barney Frank sat on the board and denied influence; the FDIC blamed management, rapid growth, uninsured deposits and supervision that could have been more forceful. Banker-on-regulator-board and regulator-on-bank-board links are not regulator exits to the regulated firm. The author concedes the cases are "not proof", and they were not chosen blind.
5. **Secondhand empirics.** The 49%, 7.4% and 11% figures come through the paper, not the primary studies.
6. **Scope.** US financial regulation and federal payroll. The model assumes monopolistic competition, no transfers or taxes, a deterministic signal, and K < alpha*D. The Kalmenovitz effect holds in agencies with broad powers, weak political supervision and high-paying industry contact.
7. **Not a deregulation argument.** The paper's Remark 2.2 says the result is conditional on capture and does not imply that deregulation is better. [[regulatory-capture]] records that corrosive capture operates through deregulation, so the two should not be read as aligned.
8. **No age or scale-of-institution claim.** Scale enters only as firm leverage or size.

## Levers proposed, and their evidence

| Lever | Evidence base |
|---|---|
| Post-employment restrictions / cooling-off rules | **[empirical, secondhand]** Kalmenovitz shows regulators respond to the threshold; no evidence that restrictions improve regulatory outcomes. Cooling-off rules are listed as future research. Evasion risk per *wataridori*. |
| Raise the debt/distress penalty rho | **[model]** only; assumed to dampen the effect. |
| Reduce option-like (equity-linked) compensation in outside offers | **[model]** only; outside offers are not directly controllable. |
| Consolidated supervision to close vacuums | Lehman vignette only; narrative. |
| Truthful debt-reporting legislation | Gestured at, untested. |
| Regulatory independence | Ambiguous; the paper cites Schram and Ule that independence cuts holdup but can entrench capture. |

**[wiki synthesis]** Everything here is a pointer; nothing is tested. Political supervision appears as a scope condition (the effect is concentrated where it is limited), so insulation of the kind discussed in [[civil-service-tenure-and-political-insulation]] may raise exposure to this channel, which is a trade-off worth checking against the original paper. Counterpoint on the debt penalty: it is a weight in the regulator's objective, which is the multitask-weighting problem of [[multitask-incentive-theory]].

## Public/private and power

**[wiki synthesis]** The channel is public-to-private. The mechanism (a convex outside option on a counterparty) is not specific to the state, so analogues exist for auditors and rating agencies; Kempf (2020) is the cited and mixed evidence there. No cross-sector test exists. Power is conceived as the firm's ability to offer future rewards, with ex ante screening of appointments (Kane 2011) as a related channel; the paper has no account of the distribution of political power.

## Source

- `raw/research/weekly-2026-10-13/02-regulator-career-revolving-door.md` — G. Charles-Cadogan, "A Regulator's Career Option: Revolving Doors, Regulatory Signals, and Firm Tail Risk", arXiv 2610.08804, working paper dated 2026-10-08. Un-refereed.

## Related

- [[regulatory-capture]] — the canonical capture page; this adds an exit-side channel and a tension with the Carpenter & Moss evidentiary test.
- [[amakudari-and-institutionalized-capture]] — the organised, ministry-run version of the same incentive, including cooling-off evasion.
- [[career-concerns-and-managerial-risk-taking]] — career concerns with the opposite payoff shape.
- [[cooptation]] — entry-side and cultural capture versus exit-side incentive capture.
- [[incentives-under-multiple-principals]] — a latent private principal (the future employer).
- [[multitask-incentive-theory]] — the debt penalty as a low-weight, hard-to-measure task.
- [[credible-commitment]] — cooling-off rules as commitment devices.
- [[rational-actor-accounts-of-bureaucratic-behaviour]] — a quantified share of responders.
- [[personnel-economics-of-the-state]] — public pay against the outside option.
- [[civil-service-tenure-and-political-insulation]] — political supervision as a scope condition.
- [[dimensions-of-institutional-variation]] — candidate axes: post-employment restriction strength, compensation convexity, distress-penalty weight.
- [[reform-levers]] — post-employment restrictions as a lever.
- [[fda-case-profile]] — another regulator with industry-mobility and capture questions.
