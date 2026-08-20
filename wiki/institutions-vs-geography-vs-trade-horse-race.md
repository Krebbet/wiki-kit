# Institutions vs. Geography vs. Trade: the Cross-Country Horse Race

Rodrik, Subramanian & Trebbi race three candidate determinants of 1995 national income against each other — institutional quality, geography, and trade openness — instrumenting institutions with AJR's settler mortality and openness with a Frankel–Romer gravity-predicted trade share, simultaneously. Their result is that institutional quality "trumps" both: once instrumented, geography's direct effect and integration's direct effect go to zero or flip sign while institutions stay large and stable across dozens of permutations. **The page exists because this paper is the most commonly cited independent corroboration of AJR — and it is not independent.** Its identifying variation for institutions is AJR's instrument, imported wholesale and not re-defended, so every objection at [[colonial-origins-and-the-settler-mortality-instrument]] transfers here unchanged. Two further things the paper reports about itself are load-bearing and rarely carried forward: **in the larger 140-country sample where the instrument set is over-identified, the over-identification tests fail** (p = 0.0071 and 0.0365), and the authors respond by preferring the smaller just-identified sample rather than fixing or explaining the failure; and their own Section IV is titled, in part, **"An instrument does not a theory make"**, disowning the reading that their result licenses any institutional prescription.

**Evidence tier note.** (a) empirical in form — cross-country 2SLS, single cross-section, 1995 income — resting entirely on exclusion restrictions the paper does not test and, for the institutions instrument, does not argue. The mechanism claim (property rights → physical capital) is (b): it rests on one supplementary decomposition regression that is not itself instrumented for the mechanism. The stock-flow decay formalisation in Section IV.B is (b) with no estimated parameter.

---

## The design

**[empirical]** Core equation: `log y = μ + α·INS + β·INT + γ·GEO + ε`, with institutions (INS) and integration (INT) both treated as endogenous and geography (GEO, distance from the equator) treated as exogenous and entering both stages directly.

- **Institutions instrument:** AJR's log settler mortality.
- **Integration instrument:** Frankel & Romer's (1999) gravity-predicted bilateral trade share, imported wholesale. The paper does not construct it and defends it only by noting it has "passed... the AER-test" — i.e. survived peer review in the trade literature — not by independently establishing exclusion.
- **Institutions, operationally:** the Kaufmann–Kraay–Zoido-Lobatón (2002) **rule of law** index, a standardised composite of perceptions-based survey and expert assessments, range −2.5 to +2.5, mean −0.25 in the 80-country sample. This is **not AJR's variable.** The authors substitute it for wider country coverage and justify the substitution by noting the two correlate at ρ = 0.78 in the overlap sample and reproduce "very similar" IV coefficients.
- **Headline result:** institutional quality explains roughly half the cross-national variance in income in the preferred specification, and the coefficient is remarkably stable across alternative geography and openness measures, sample restrictions, and outlier exclusion (their Tables 4–6). The IV coefficient (≈2.0) is about **3× the OLS coefficient (≈0.7)**, which they attribute to attenuation from measurement error.

**[wiki synthesis]** That attenuation story is an auxiliary assumption, not a finding. The same 3× gap is equally consistent with an invalid instrument inflating the IV estimate — the paper does not distinguish the two, and the same interpretive move appears in AJR's original.

## The mechanism claim, and how thin it is

**[empirical]** Their proposed channel is investment incentive: secure property rights and credible rule of law reduce expropriation risk and so raise physical investment. The evidence is a Hall & Jones-style decomposition of income into physical capital, human capital and TFP (their Table 3): institutions' coefficient on **physical capital per worker is ~6× its coefficient on human capital per worker and ~3.2× its coefficient on TFP** in the 80-country sample.

**[wiki synthesis]** This is one decomposition regression, not separately identified for the mechanism. It is the only quantitative attempt in this batch to say *through which channel* institutions act, which is why it is recorded here — but it does not settle [[open-questions]] Q13, and its human-capital coefficient being the smallest of the three sits directly against Glaeser et al.'s finding that predicted schooling beats predicted executive constraints in a 2SLS horse race off the same instruments.

## What the paper reports against itself

Three things, all in the paper, all routinely dropped when it is cited.

**[empirical]** **1. The over-identification tests fail.** With two endogenous regressors and, in the 80-country specification, exactly two excluded instruments, the system is just-identified and no individual exclusion restriction can be tested there. In the 140-country sample the authors add language-fraction instruments (ENGFRAC, EURFRAC, from Hall & Jones) alongside the gravity instrument, making the system over-identified — and **the over-identification tests reject at p = 0.0071 and 0.0365 (their Table 2)**. Their stated response is to prefer the smaller, just-identified settler-mortality sample. Deaton's warning at [[colonial-origins-and-the-settler-mortality-instrument]] bites in both directions here: passing an over-identification test is consistent with all instruments being invalid, and failing one is consistent with only a subset being so — but a *failed* test is nonetheless a statistical rejection of the instrument set, and preferring a sample in which the test cannot be run does not answer it.

**[empirical]** **2. Settler mortality is not cleanly excluded from the other endogenous regressor.** Their own first stage shows settler mortality significantly affecting *integration* as well as institutions (coefficients −0.39 to −0.27, Panel C). This is consistent with the model as written — SM appears in both first-stage equations by construction — but it means the instrument nominally "for institutions" is doing double duty, and the clean one-instrument-one-regressor story oversimplifies what is identified.

**[empirical]** **3. The instrument's own first stage decays over time, and the authors read the decay against themselves.** Run by decade, settler mortality's first-stage coefficient on institutions falls: **0.94 (1970s) → 0.87 (1980s) → 0.71 (1990s)**, while Polity IV executive-constraint scores over the same 71 countries *rise*: **3.21 → 3.52 → 4.37**. The authors read this as evidence that institutions are mutable rather than fixed by colonial history — a substantively interesting claim. It also **weakens the time-invariant persistence assumption the instrument's exogeneity depends on**, and the paper does not resolve the tension.

**[wiki synthesis]** Point 3 is a real contribution to a different question and should be carried to [[decay-as-real-vs-decay-as-overstated]]: it is country-level calendar-time evidence that measured institutional quality moves over a few decades. It is not institution-level age evidence and does not close Q7 or Q39. It also converges with Glaeser et al.'s volatility finding from the opposite camp — both report that these indices move a lot over short horizons — while disagreeing about what that means. Rodrik reads mutability; Glaeser reads that the indices are not measuring institutions.

## The authors' own disclaimers

**[empirical]** Section IV.A, **"An instrument does not a theory make"**, explicitly distinguishes their identification strategy from a causal theory of development. Section IV.C, "The hard work is still ahead", is blunter: the operational guidance the result yields is "extremely meager"; the strategy is "doubly unhelpful from a policy perspective" because it isolates only the *exogenous* component of institutional variation, not the policy-manipulable component; and "our findings do not map into a determinate set of policy desiderata."

**[empirical]** Their illustration is the **China/Russia contrast**: Chinese entrepreneurs invested heavily with no formal private property under a nominally socialist legal system, while Russian investors stayed wary despite a formal Western-style property-rights regime. What the paper takes from this is that *credible* commitment matters more than nominal legal form. It does not analyse the power arrangements producing credibility in either case.

**[wiki synthesis]** The China/Russia pair is the point at which three sources in this batch converge from three directions and none of them notices. Rodrik: formal property law without credibility does nothing. Glaeser et al.: a ruler who chooses not to expropriate scores the same as one who cannot, and their cases are Singapore, China and South Korea. Wade: East Asian investment boomed under executives with almost no formal constraint ([[developmental-state-and-embedded-autonomy]]). The common observation is that **the measured constraint variable and the thing investors actually respond to come apart in exactly the cases with the fastest growth.** Filed at [[constraint-vs-capacity-as-the-investment-mechanism]].

**[wiki synthesis]** Note also the gap between the paper's framing and its own text: the title and abstract ("Institutions Rule", institutions "trump" everything else) carry none of Section IV's concessions forward, which is why the paper is downstream-cited as a strong universal claim rather than as the narrower, sample- and instrument-conditional statistical result it is.

## The stock-flow decay model

**[model]** Section IV.B formalises institutional quality as a stock accumulated from policy flows with an explicit decay term: **dI/dt = Σ αᵢ·pᵢ − δ·I**, where pᵢ is policy on dimension i, αᵢ its impact, and δ the rate at which institutional quality decays absent countervailing action. **No estimate of δ is offered and the decay claim is not tested.** Record it as a formalisation, not evidence; it is one more instance of the pattern this wiki keeps finding, in which decay is written into a model's structure and never measured.

## Level of analysis

**[wiki synthesis]** Strictly country-level and cross-sectional. Every variable — INS, INT, GEO, income — is a single scalar per country; the paper contributes nothing to the register at [[dimensions-of-institutional-variation]] beyond the fact that "rule of law" is being used, at national aggregate level, as a proxy for institutional quality as such. It never asks who holds decision rights inside a country's institutions, how officials are selected, or who can remove them.

## Why this is a separate page and not folded into the anchor

**[wiki synthesis]** Recorded because the merge was considered. The case for merging is real: this paper shares AJR's instrument and therefore all of its problems, and keeping it separate risks a reader treating it as independent corroboration. The case against, which won: the paper contributes four things the anchor page does not carry and would bury — the three-way horse race against geography and trade specifically, the failed over-identification test, the decade-by-decade decay of the first stage, and the authors' unusually explicit self-disclaimer on policy reach. The dependency is handled instead by stating it in the first paragraph and again here: **this page supplies no independent identification.** Cite the two together or not at all.

## Source

- `raw/research/institutions-and-growth/04-rodrik-institutions-rule.md` — Dani Rodrik, Arvind Subramanian & Francesco Trebbi, "Institutions Rule: The Primacy of Institutions over Geography and Integration in Economic Development", NBER Working Paper 9305, October 2002. https://www.nber.org/system/files/working_papers/w9305/w9305.pdf

## Related

- [[colonial-origins-and-the-settler-mortality-instrument]] — the source of this paper's institutions instrument and of every objection to it; the two papers are one identification strategy, not two.
- [[does-institutions-growth-survive-identification]] — the open conflict; this paper's failed over-identification test is one of its exhibits.
- [[institutions-as-fundamental-cause]] — the theory this paper's result is usually taken to support, and which its own authors decline to supply.
- [[constraint-vs-capacity-as-the-investment-mechanism]] — the China/Russia contrast is this paper's contribution to that conflict.
- [[credible-commitment]] — the macro statistical version of that page's property-rights-drives-investment claim, with no institutional-design detail where that page has a single case and a market-priced measure.
- [[decay-as-real-vs-decay-as-overstated]] — the decade-by-decade first-stage decline and rising Polity scores are country-level calendar-time evidence of institutional mutability; they extend that conflict without settling it.
- [[developmental-state-and-embedded-autonomy]] — Wade's cases are the ones where a high-growth economy scores low on exactly the axis this paper finds decisive.
- [[schooling-and-institutional-quality]] — the direct counter-result off the same instrument: this paper's Table 3 puts institutions' coefficient on human capital at roughly one-sixth of its coefficient on physical capital, where Glaeser et al. instrument for both and find only schooling survives the second stage.
- [[what-is-an-institution]] — "institutions" here is one perceptions-based composite per country, which collapses every definitional distinction that page maintains.
- [[open-questions]] — Q13 (which channel dominates — this paper's Table 3 is the only quantitative attempt in the batch), Q90 (level of analysis).
