# Governance Indicators and Their Construction (WGI)

The Worldwide Governance Indicators are six country-year scores — Voice & Accountability, Political Stability, Government Effectiveness, Regulatory Quality, Rule of Law, Control of Corruption — built by Kaufmann & Kraay from **35 perceptions-based data sources** combined in an **Unobserved Components Model** that weights each source by the inverse of its estimated measurement-error variance and propagates a **formally reported margin of error**. Three facts about it are load-bearing for this wiki, and the third is routinely ignored by the literature that cites it. **(1) The unit is the country-year, without exception**: 214 economies, 1996–2023, six scalars each, and no sub-national or agency-level product exists or is proposed anywhere in the methodology paper. **(2) It is perception-exclusive by written inclusion criterion**, not merely perception-heavy — inclusion criterion #1 states the sources "must provide subjective views or perceptions... as the WGI are based exclusively on this type of data", and objective/de jure data is acknowledged as useful and then categorically excluded, partly *because* de jure measures can be gamed. **(3) Its own confidence intervals say most of the comparisons people make with it are not comparisons.** Only **61% of pairwise country comparisons** have non-overlapping 90% intervals; only **0.2% of one-year changes**, **3% of five-year changes**, **7% of ten-year changes** and **13% of the full 1996–2023 change** are significant at 90%. That is the instrument's own arithmetic, reported by its own authors, and it belongs in the summary rather than a footnote because nearly every downstream use — rankings, year-on-year "improvement", eligibility cutoffs — presumes the opposite.

**Evidence tier note.** **(b) model** for the aggregation machinery: the UCM is a formal empirical-Bayes latent-variable estimator, fully derived, applied to secondary data — "The WGI do not involve new primary data collection on our part." **(a) empirical** for the three robustness analyses the 2024 update runs on its own 25-year, 35-source dataset: the equal-weighting check, the global-trend check, and the correlated-measurement-error check. The authors grade their own weakest evidence explicitly — on correlated errors, "the evidence presented in this section is suggestive, not conclusive", because both governance and measurement error are unobserved and so cannot be disentangled. **(c) wiki synthesis** is marked inline. Note the authorship position: this is the instrument's own creators summarising and defending their own work, and they say so in a self-citation note; the self-critique is nonetheless unusually candid.

## The construction, precisely

**[model]** For each of the six dimensions, country *c*, source *k*:

`y(c,k) = α(k) + β(k)·(g(c) + ε(c,k))`

where `g(c)` is unobserved governance (standardised to mean 0, SD 1 across countries), `ε(c,k)` is source-specific measurement error with variance `σ²(k)`, and `α(k)`/`β(k)` rescale each source's arbitrary units (a 6-point scale, a 10-point scale) into common ones. Under joint normality and **independence of errors across sources**, the conditional-mean estimator is

`E[g(c)|y(c)] = Σ w(k)·((y(c,k) − α(k))/β(k))`, with `w(k) = σ⁻²(k) / (1 + Σ σ⁻²(k'))`

— **inverse-variance ("precision") weighting**: a source believed to be less noisy counts for more. The margin of error follows mechanically:

`SD[g(c)|y(c)] = (1 + Σ σ⁻²(k))⁻¹ᐟ²`

which shrinks as more and better sources cover a country. WGI reports a 90% interval as ±1.64 × this SD, in natural units (≈ −2.5 to 2.5) and with the interval's own bounds converted to percentile rank. The authors treat this as the instrument's defining virtue: "A key attribute of the WGI is that these margins of error are explicitly reported... In contrast, in many other measures of governance and institutional quality, they are left implicit."

The independence assumption in that derivation is the whole game, and it is contested from outside — see [[critiques-of-governance-indicators]], where Arndt & Oman show that relaxing it to a 0.5 error correlation **doubles** the average standard error for Rule of Law (0.33 → 0.66).

**Source composition.** Roughly 230,000 country-year-source data points; 30 of the 35 sources active in 2023, against 12 in 1996. About one-third from four commercial business-information providers, a quarter from NGO sources, ~20% each from household/firm surveys and public-sector providers. **11 of 35 are household or firm surveys** (first-person perception and self-reported experience — "how often do firms make extra payments in connection with taxes, customs, and judiciary"); **24 of 35 are expert assessments** (third-party scoring by analysts). Sources built from other existing indices are excluded by design — Transparency International's CPI is excluded from WGI for exactly this reason, and EBRD's Transition Indicators were dropped post-2014 when a methodology change turned them into a compilation.

## What the margins of error actually imply

**[empirical]** The numbers, from the instrument's own reporting:

| Comparison | Share statistically significant at 90% |
|---|---|
| All pairwise country comparisons, all indicators, all years since 1996 | **61%** (range 52% Political Stability – 70% Voice & Accountability) |
| One-year change within a country | **0.2%** |
| Five-year change | **3%** |
| Ten-year change | **7%** |
| Full 27-year change, 1996–2023 | **13%** (rising to ~one-third at a looser 68% interval) |

The significant share of pairwise comparisons rose from 52% (1996) to 62% (2005) as the source count grew 12 → 31, then plateaued at 61–65%.

**[wiki synthesis]** Read plainly: **a majority of country pairs are distinguishable and a very large minority are not, and essentially no year-to-year movement is signal.** Rank tables and "country X improved this year" claims built on WGI are, by the instrument's own arithmetic, mostly reporting noise. This is the empirical backbone for percentile-rank instability as a named defect of this whole class of composite index — and it is stated by the index's authors, not by its critics, which makes it very hard to dismiss.

## Robustness checks the 2024 update runs on itself

**[empirical]** Three, and one of them cuts against the elaborateness of the method:

- **Weighting scheme.** A naive four-step equal-weighted z-score alternative correlates **0.97–0.99** with the precision-weighted baseline in the 2023 cross-section and 0.98–0.99 averaged over 25 years. Share of countries where the equal-weighted estimate falls outside the baseline's 90% interval: under 5% for four of six indicators, but **24%** for Political Stability and **17%** for Rule of Law in 2023. Reassuring about robustness; also a statement that the precision-weighting machinery buys little over an average for most dimensions.
- **Correlated measurement error.** Tested indirectly: pairwise correlations among four commercial risk providers (EIU, Crisis24, PRS, S&P Global) against correlations between those providers and two firm surveys (WEF, IMD). For five of six indicators the two correlation types are nearly identical and neither rises over time — evidence against the specific worry that commercial raters converge on each other. The authors' own caveat is the citable part: because both true governance and measurement error are unobserved, the test cannot separate "these sources agree because both are accurate" from "these sources agree because they share a bias".
- **Global trend.** The baseline fixes the global mean and SD at 0 and 1 every year by construction, which would mask a world genuinely improving or declining. A time-varying global mean and SD are re-derived algebraically from the existing parameters, with "little evidence of trends" 1996–2023 — which is what licenses reading WGI's relative movements as absolute ones.

## Perception-exclusivity, and why it is the strongest form of D90's claim

**[empirical]** WGI's stated inclusion criterion #1 is that sources "must provide subjective views or perceptions of relevant dimensions of governance, as the WGI are based exclusively on this type of data." The authors acknowledge objective and de jure data exists and is useful — "Objective data on the specific laws and regulations 'on the books'... also are useful" — and exclude it anyway. One of their four justifications is itself an anti-gaming argument: de jure indicators are "susceptible to 'gaming' where policy makers target reforms to narrowly change specific measures simply because they happen to be included in an aggregate indicator", and perceptions cannot be reformed-on-paper the same way.

**No component of WGI at any level scores an institution's own documents, budget, personnel records or observable behaviour.** Underlying questions sometimes name an institution *class* — "confidence in the police force", "trust in the supreme court", "degree of judicial independence", "quality of the civil service" — but always as one national score for that whole class, never a specific court, precinct or regulator, and WGI then aggregates even that into one of six composites.

**[wiki synthesis]** This is the strongest version of [[dimensions-of-institutional-variation]] **D90**'s claim anywhere in this wiki. Glaeser et al. argued from the outside that the standard indices measure recent outcome and perception rather than durable constraint; here the instrument's own methodology paper states perception-exclusivity as a **design choice**, in writing, with reasons. There is nothing to infer. Note the complication recorded on D90 alongside it, from [[measurement-validity-framework]]: Munck & Verkuilen argue the objective/subjective dichotomy is itself overstated, so "perception-exclusive" locates the problem without settling it.

**One partial crack, and it does not help.** Several underlying sources are firm- or household-level microdata before country aggregation — World Bank Enterprise Surveys, Gallup World Poll — and WBES record-level data is publicly available. So a firm's own experience is in principle recoverable from the raw survey. But WGI discards it, and the questions those firms answer are about the general national business, regulatory and judicial environment, not about a specific institution the firm dealt with. There is no route from WGI to an institution-level score.

## What the authors themselves disclaim

**[empirical]** "The WGI are not designed to be a tool to evaluate specific governance reforms in individual economies... the WGI must be supplemented with more granular country-specific data." The paper proposes no prescriptive use and names no lever. It also cites its own standing — >25,000 citations, adoption by the Millennium Challenge Corporation, IMF, Moody's, Fitch, MSCI ESG and Disney's sourcing policy — which is promotional about impact, and is also the reason the misuse catalogue at [[critiques-of-governance-indicators]] matters: an instrument this widely wired into money allocation carries its measurement flaws into real decisions.

## What transfers to scoring a single institution

**[wiki synthesis]** **The data does not transfer at all. One technique does.**

**Inverse-variance precision weighting with a formally propagated, reported margin of error** is a general procedure for combining several noisy partial signals about one unobserved target, and nothing in it depends on the target being a country. If any row in [[dimensions-of-institutional-variation]] is ever built from multiple partial proxies for a single institution — say, three imperfect indicators of mandate clarity read off different documents — this is the aggregation rule to use, and the reported margin of error is the part to copy, not the weighting. WGI's own equal-weighting check shows the weights barely matter; the interval is what changes how the number gets used.

Two conditions on borrowing it, both visible in WGI's own results. The estimator needs an estimate of each source's error variance, which WGI gets from cross-source disagreement across 214 countries — an analyst scoring one institution has no such sample and would have to obtain error variances another way. And the independence-of-errors assumption has to be defended, not assumed; on a single institution, several proxies drawn from the same document set or the same informants are almost certainly correlated, which is the exact failure Arndt & Oman quantify at country level.

## Source

- `raw/research/measuring-institutions/02-wgi-methodology.md` — Daniel Kaufmann & Aart Kraay, "The Worldwide Governance Indicators: Methodology and 2024 Update", World Bank, September 2024. https://www.worldbank.org/content/dam/sites/govindicators/doc/wgimethodologypaper.pdf
- `raw/research/measuring-institutions/03-qog-standard-codebook.md` — *The QoG Standard Dataset 2021 Codebook*, Quality of Government Institute, University of Gothenburg (used here only as provenance: its WGI entries carry per-dimension estimate, source-count and standard-error variables and WGI's own caveat that annual re-standardisation makes the scores "not directly suitable for over-time comparisons within countries". **Sampled at roughly 3–5% of its ~2,000 variable entries.**) https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan21.pdf

## Related

- [[measurement-validity-framework]] — the batch anchor; run WGI through its three stages and the conceptualisation-stage question ("is 'governance' one construct or six?") is the one WGI never answers, since the authors state their six categories are a typology and not a causal model.
- [[critiques-of-governance-indicators]] — Arndt & Oman audit this exact instrument from outside: the independence-of-errors assumption, the aggregation weights that give household surveys ~0.01 against Freedom House's 0.39, and the bright-line eligibility misuse the margins of error make indefensible.
- [[v-dem-measurement-model]] — the other major construction methodology in this batch, solving a harder version of the same problem (individual rater bias) with a heavier apparatus, and equally country-year.
- [[worldwide-bureaucracy-indicators]] — the instrument in this batch that gets closest to an institution; its wage-premium measures show **no correlation** with WGI Government Effectiveness, which is a fact about both.
- [[dimensions-of-institutional-variation]] — **D90**, whose claim this page states in its strongest available form, and **D122**, where the WGI country score is registered `rejected` as an institution-level axis.
- [[colonial-origins-and-the-settler-mortality-instrument]] — carries Glaeser et al.'s durable-rule-vs-outcome attack on the same class of index; this page is the confirmation from inside.
- [[world-management-survey]] — the contrast that decides the matter for this wiki: an instrument that scores 11,383 individual organisations and finds 77% of the variation *within* country-and-industry, which is exactly the variation WGI's design cannot see.
- [[open-questions]] — **Q90**, the level-of-analysis fork, and **Q120**–**Q122**.
