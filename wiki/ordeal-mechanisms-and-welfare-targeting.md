# Ordeal Mechanisms and Welfare Targeting

A work requirement can cut a welfare program's caseload sharply while doing nothing for the behavior it claims to target — and the reason is a specific failure of the "ordeal" theory that is supposed to justify it. Cai, Kim & Leung's 2026 quasi-experimental study of SNAP's ABAWD work requirement finds that reinstating it (≥80 hrs/month paid work, volunteer work, workfare, or training; benefit loss after 3 of 36 months unmet) cut participation 7–13% with **no** detectable increase in employment or earnings, disproportionately screened out the *lowest*-income recipients rather than the non-employed it nominally targets, and — once a reworked welfare model counts the cost to those pushed off the rolls — imposes a social cost of roughly $2.19 per dollar of budget savings.

## The theoretical move: infeasibility, not cost

**[model]** Standard ordeal-mechanism theory (Nichols & Zeckhauser 1982; Besley & Coate 1992) treats compliance as *costly but achievable* — an ordeal that screens by imposing a burden the truly needy are more willing to bear. Under that framing, and by the envelope theorem, marginal exiters are roughly indifferent between complying and leaving, so their exit contributes negligibly to welfare loss. This paper instead models compliance as **infeasible** for a subset of participants — they cannot document sufficient hours, secure a workfare slot, or obtain an exemption determination, regardless of willingness — which makes their lost benefits a first-order welfare cost, independent of any behavioral-bias assumption. This is the paper's genuine theoretical contribution: a mechanism, not merely a relabeling, for why the classical ordeal result (screening is roughly welfare-neutral at the margin) fails here.

## Evidence

**[empirical] Strongest evidence.** Triple-differences and difference-in-differences designs on linked administrative SNAP and Census LEHD employment/earnings microdata (5–9 states), exploiting staggered county-level ABAWD-waiver reinstatement crossed with an age-50 exemption cutoff, robust to the Sun & Abraham (2021) staggered-adoption correction and to a tighter 48–52 age band:

- Participation falls 4.4–8.7 percentage points (7–13%).
- Employment effect: −0.4pp, tightly bounded around zero.
- Earnings effect: −$15, not statistically significant.
- Average participant gross income *rises* $24 (4%) post-reinstatement — because lower-income recipients exit disproportionately, not because incomes rose.

**[a — weakest evidence].** The headline welfare-cost figure (Marginal Value of Public Funds, $2.19 per dollar of budget savings in the baseline calibration, 1.17–3.58 across alternative social weights) is a calibrated formal model, not a directly measured cost: the two-hours/month compliance-cost assumption and a $75 application-cost parameter (borrowed from Finkelstein & Notowidigdo 2019) are asserted rather than measured for this population — the authors state they could not find a direct estimate of compliance time costs for this setting.

## What the rule actually does: worsened targeting, not screening

**[wiki synthesis]** This is a clean instance of proxy/measurement failure at the policy level: caseload reduction is treated by policymakers as evidence the rule "worked," while the stated behavioral objective (employment) shows a tightly-bounded null. The ordeal intended to screen by need instead screens by *compliance capacity* — catching the non-employed no more than others, but catching lower-income people disproportionately, precisely the population the program exists to reach.

## Power and administration

**[empirical]** Rule-setting authority sits with Congress (the 2025 One Big Beautiful Bill Act raised the ABAWD age ceiling to 64 and restricted geographic waivers, narrowing state/county discretion that previously existed); states retain nominal discretion (up to 15% caseload exemption, with latitude over prioritization criteria) but are accountable to federally-set eligibility criteria and unemployment-rate formulas they do not control. The paper's findings are explicitly extrapolated — not tested — to that 2025 expansion, which applies the same mechanism to a much older (up to 64), lower-employment population in areas with fewer job opportunities.

## Scope

**[a]** United States; SNAP's ABAWD population (childless adults, focal comparison ages 45–49 vs. 50–55 exempt); 5–9 states with linked administrative data; the post-Great-Recession reinstatement wave (2009–2010 suspension through 2016 reinstatement). Extrapolation to the 2025 policy expansion and to other work-requirement programs (e.g., proposed extensions to housing assistance) is argued by analogy, not tested.

## Bearing on reform levers

**[wiki synthesis]** This is a negative-lever finding for this wiki's [[reform-levers]] inventory, which currently has no negative-signed tier-(i) entry: an actively-expanding real-world policy lever (work requirements) is shown, under a clean quasi-experimental design, not to deliver its claimed benefit (no employment/earnings gain) while imposing a first-order, quantified cost on the population it excludes.

## Source

- `raw/research/weekly-2026-09-22/02-arxiv-snap-work-requirements.md` — Cai, Kim & Leung, "Screening Out the Needy: The Effects of SNAP Work Requirements," arXiv preprint 2609.19660, 2026.

## Related

- [[red-tape]] — Bozeman's definition of red tape (a rule that imposes burden and achieves nothing) is here sharpened from assertion to measurement: real compliance/exclusion cost, null effect on the stated behavioral goal.
- [[reform-levers]] — supplies this wiki's first negative-signed tier-(i) (quasi-experimental) lever entry: work requirements, shown to fail their stated goal while imposing first-order cost on excluded participants.
- [[measurement-validity-framework]] — the paper's core critique (caseload reduction is a poor proxy for the policy's actual behavioral target) parallels Munck & Verkuilen's conflation/proxy failure modes, applied here to a policy outcome metric rather than a country-level index.
- [[rent-seeking-and-the-welfare-cost-of-transfers]] — Tullock's transfer-cost accounting and this paper's MVPF welfare-cost calculation are structurally parallel (both quantify a transfer program's true social cost beyond naive fiscal accounting), though the mechanisms differ (rent dissipation vs. ordeal exclusion).
- [[incentives-under-multiple-principals]] — Dixit's public/private-differences-of-degree-not-kind claim and multi-principal framing bear loosely on SNAP's federal/state administrative split, though this source does not test principal-agent incentive strength directly.
- [[capital-requirements-and-entrepreneurial-entry]] — both are entry/exit screening mechanisms (welfare eligibility vs. business incorporation) captured in the same weekly sweep; both burden without functioning as the quality filter their designers assumed, via different mechanisms (infeasibility vs. size mismatch).
