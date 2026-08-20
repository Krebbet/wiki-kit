# Endogenous State Capacity

Besley & Persson model state capacity not as an institutional inheritance that causes growth but as an **investment a ruling group chooses**, made under uncertainty about who will hold power next. A two-group, two-period polity: whoever is incumbent at the end of period 1 sets **fiscal capacity** (the ability to tax — auditors, VAT systems) and **legal capacity** (the ability to support markets — courts, property and credit registries) for period 2, trading investment cost today against the expected value of holding, or losing, that capacity tomorrow. The two are modelled as complements, so whatever raises investment in one raises it in the other. The drivers are the probability of a common-interest state (external-conflict risk), political stability, and the inclusiveness of political institutions. The paper's most useful feature for this wiki is its epistemic discipline: **the authors explicitly deny that their own cross-country correlations between tax capacity, financial development and income can be read causally**, and state that causation on one of their central results runs from income to market support and taxation rather than the reverse.

**Evidence tier note.** (b) throughout, and unusually clean about it. The core is a formal model with propositions and appendix proofs — internal consistency rigorously derived, which establishes the model is coherent, not that it describes the world. The empirical material is *summarised from companion papers, not reproduced*: long-run historical proxies (share of years at external war 1816–1975 from Correlates of War; share of years as a democracy 1800–1975 from Polity IV; legal origin from La Porta et al.) correlated with present-day capacity indicators, cross-sectionally, with **no exclusion-restriction argument offered for any of them** and no controls or robustness checks shown in this document. One historical illustration (England, Glorious Revolution to the Napoleonic Wars). One quasi-experimental channel exists — commodity-price shocks instrumenting resource-rent shocks in the civil-war analysis — but it is summarised rather than reproduced, so its identification cannot be audited here.

---

## The model

**[model]** Two groups, incumbent *I* and opposition *O*, two periods. The incumbent at the end of period 1 chooses τ₂ (fiscal capacity) and π₂ (legal capacity). Investment is worth making in proportion to **E(λ₂)**, the expected value of the capacity next period, which rises with:

1. **The probability of a "common-interest" state** — a high public-goods demand shock, external conflict risk being the canonical case.
2. **Political stability** — a low probability γ of turnover. An incumbent expecting to lose power has weaker reason to build machinery the successor will inherit.
3. **Inclusiveness of political institutions (θ)**, specifically when instability is high.

Fiscal and legal capacity are **supermodular** in payoff, hence complements: raising the return to one raises investment in the other.

**[model]** Two institutional parameters carry the political side, and the paper keeps them conceptually distinct from capacity itself:

- **θ ∈ [0, ½]** — "the representativeness of political institutions through checks and balances or electoral systems", operationally the weight the incumbent places on the opposition group's welfare. θ = 0 is an unconstrained autocrat; θ = ½ is a utilitarian planner.
- **γ** — the exogenous probability of peaceful turnover; "a crude measure of political instability."

**[wiki synthesis]** The distinction the model maintains is worth carrying, because most of this literature loses it: **θ and γ are institutions — the constraints on how power is used and how it changes hands. τ and π are capacity — accumulated public capital.** Institutions shape the *incentive* to invest in capacity; capacity is not itself an institution in this framework. Much of the confusion in the state-capacity literature comes from using one word for both, and this source is a usable model of how to keep them apart. Note the naming collision inside this wiki too: [[state-capacity-and-level-of-government]] uses "state capacity" for US state and local administrative capacity, a different level of analysis entirely.

## The investment trap

**[model]** The paper's sharpest result, and a failure mode this wiki does not otherwise have. **Proposition 4:** political instability causes an incumbent to withhold fiscal-capacity investment for fear the machinery will be inherited and turned against its own group. Low capacity perpetuates weak legal protection for the opposition and production inefficiency, which sustains the conditions producing the instability — a self-reinforcing low-capacity equilibrium held in place by **rational anticipation of future expropriation**.

**[wiki synthesis]** This is mechanistically distinct from the two accumulation stories already on the wiki, and the distinction should be preserved rather than absorbed. [[institutional-sclerosis]] runs on Olson-style coalition accretion — something builds up. [[path-dependence-and-increasing-returns]] runs on increasing returns — early choices raise the cost of later ones. Besley & Persson's trap is **forward-looking**: nothing accumulates, and nothing is locked in by sunk cost. The state stays weak because a rational actor correctly forecasts the future distribution of power. It is closer in structure to a holdup problem than to either, and it is one of the very few mechanisms in this wiki that predicts persistent institutional weakness with no historical residue doing the work.

## The genius of taxation, and rent-preservation by direct self-dealing

**[model]** Section 2's result: when fiscal capacity is below a threshold τ̂(θ, α), an incumbent group with a large capital-owning share σ can find it more profitable to **deny legal protection to the opposition group** — suppressing aggregate wages to preserve capital rents for its own group — than to redistribute efficiently through taxation. Aggregate production falls; the incumbent group's rents rise.

**[wiki synthesis]** Record this as a rent-extraction mechanism structurally different from regulatory capture. There is no agency being captured by an external interest: the ruling group is directly denying a public good to a rival group because doing so raises its own factor returns. The lever is *withholding* institutional provision rather than bending it. See [[regulatory-capture]] for the contrast.

## Levers, and what they are worth

**[model]** All comparative statics, none tested by the authors:

- Raise political inclusiveness θ, which can shift the inefficiency threshold τ̂ below existing fiscal capacity.
- Reduce political instability (lower γ), inducing earlier capacity investment.
- Exogenous circumstance — higher expected external-conflict severity — can crowd out rent-extractive policy by raising the value of a future common-interest state.
- A speculative "big push" investment in legal capacity to raise wages and break out of a conflict trap (Section 3.4), **flagged by the authors themselves as untested**: "to the extent that this is important, we might expect..."

**[wiki synthesis]** These are model outputs, not evidence, and the third one is uncomfortable as advice. Nothing here belongs above tier (iii) on [[reform-levers]].

## The historical illustration

**[empirical, second-hand]** England: fiscal capacity accumulating over roughly 150 years — Glorious Revolution 1688, then 40-plus years of Whig parliamentary dominance, tax reaching 20% of GDP, and the Napoleonic-era income tax reaching **36% of GDP** by the early 1800s (citing Stasavage 2007, O'Brien 2005, Mathias & O'Brien 1976).

**[wiki synthesis]** This is the same case [[credible-commitment]] runs on, used for a **different and complementary mechanism**, and the pairing is worth making explicit because the two are often collapsed. North & Weingast's Glorious Revolution protects *private* investment by constraining the ruler from expropriating it. Besley & Persson's Glorious Revolution changes the ruler's own incentive to invest in *state* capacity, by changing who expects to hold that capacity and under what constraint. Same event, two different investments, two different investors. Neither is tested against the other, and this source does not engage North & Weingast's version.

**[wiki synthesis]** Note also what this is *not*. It is national fiscal-capacity accumulation over historical time, not organisational age or decay in the sense [[open-questions]] Q7 asks about. Do not fold it into the age thread.

## What the authors deny about their own evidence

**[empirical]** Quoted, because the disclaimer is the point: "There is no good reason to believe that these correlations can be interpreted causally. Indeed, our core model's explanation of them will emphasize their joint determination with institutions, historical shocks and initial conditions being common omitted factors that drive all three of these variables." And, on Proposition 2: "the result also makes clear that causation runs from income to market support and taxation, not the other way around."

**[wiki synthesis]** This matters for how the batch is scored. Besley & Persson are conventionally filed in the affirmative camp on institutions and growth, and in one sense they are — capacity does real work in their model. But their own architecture makes state capacity **endogenous**, chosen by a forward-looking incumbent, and by the same logic treats political institutions (θ, γ) as plausibly jointly determined with income rather than as an exogenous first cause. They do not deliver a clean identified causal effect of institutions on growth and do not claim to; their conclusions are "consistent with the model", not "estimated". **The affirmative camp is internally split on exactly the question the critics attack**, and this source is one of the two places that shows.

**[wiki synthesis]** Two further honest limits the paper does not close: the mapping from θ and γ onto real-world checks, balances and electoral systems is a reduced-form parameterisation asserted rather than validated; and the model is silent on private capital accumulation as a growth channel until an ad hoc extension near the end, so its own growth result is a partial-equilibrium consequence of legal capacity raising wages rather than a growth model.

## Level of analysis

**[wiki synthesis]** The national state throughout. The model's quantities aggregate to national tax rate, national legal capacity and national income; every cited empirical measure is a country-year panel or a country-level historical share. **No sub-national, firm-level or individual-institution unit appears anywhere.** Capacity is measured by four indicators each for fiscal and legal capacity (contract enforcement, property-rights protection, tax-structure measures, scaled 0–1), all national scalars. Nothing here scores an agency.

## Source

- `raw/research/institutions-and-growth/05-besley-persson-state-capacity.md` — Timothy J. Besley & Torsten Persson, "State Capacity, Conflict and Development", NBER Working Paper 15088, June 2009 (the basis for Persson's 2008 Econometric Society Presidential Address). https://www.nber.org/system/files/working_papers/w15088/w15088.pdf

## Related

- [[credible-commitment]] — the same England case for a complementary mechanism: that page's ruler cannot expropriate the investor; here the ruler will not invest because a successor might expropriate the state.
- [[colonial-origins-and-the-settler-mortality-instrument]] — the contrast in identification strategy is the point: exogenous-shock IV there, endogenous rational choice here, with this source explicitly refusing the causal reading the other asserts.
- [[constraint-vs-capacity-as-the-investment-mechanism]] — this page supplies the formal-model version of the capacity limb of that conflict.
- [[state-capacity-and-level-of-government]] — **terminology collision, not a substantive parallel**: that page's "state capacity" is US state and local administrative capacity; this one's is national fiscal and legal capacity in a cross-country model.
- [[transaction-costs]] — legal capacity π functions as an enforcement-cost variable analogous to that page's channel, but derived from an endogenous-investment model rather than a governance-cost framework.
- [[regulatory-capture]] — the "genius of taxation" result is capture-adjacent but structurally different: direct self-dealing by the ruling group, not an external interest capturing a regulator.
- [[institutional-sclerosis]] — the investment trap is a rival mechanism for persistent institutional weakness that needs no accumulation and no lock-in, only correct forecasting.
- [[what-is-an-institution]] — a formal example of treating institutional *capacity* as accumulated public capital distinct from institutions as constraints, which is a distinction that page does not currently draw.
- [[dimensions-of-institutional-variation]] — θ was checked against the register and found already present at D7; γ enters as D93, `candidate`, with its level-of-analysis problem stated.
- [[open-questions]] — Q90 (level of analysis), Q91 (the affirmative camp's internal split).
