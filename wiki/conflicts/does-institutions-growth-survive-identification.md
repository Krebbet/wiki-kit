# Conflict: Does Institutions → Growth Survive Its Own Identification Strategy?

**Status: OPEN — not adjudicated.** This is the central conflict of the `institutions-and-growth` batch and it sits directly on the wiki user's working thesis that institutions determine economic production. It is filed with care about what each side actually claims, because the popular version of this dispute ("do institutions matter?") is not the dispute. **Both camps agree that measured institutional-quality indices correlate strongly with national income.** Nobody here denies the correlation. The disagreement is whether the field's flagship identification strategy — instrumenting institutions with European settler mortality in ex-colonies — recovers a causal effect *of institutions*, and whether the indices being instrumented measure institutions at all.

The user has a stake in the affirmative answer. That is a reason to file this precisely rather than resolve it early.

## Position A — the effect is identified, and it is large

**The claim.** Colonial-era settler mortality is a source of exogenous variation in current institutions. Instrumenting on it, institutions explain roughly three-quarters of cross-country income variance (AJR) or about half (Rodrik et al.), and the estimate is robust across alternative institution measures, alternative mortality-construction methods, extensive control sets, sample restrictions and outlier exclusion.

**Sources and what each contributes:**

- **Acemoglu, Johnson & Robinson (2001)** — *(a) empirical, cross-country 2SLS, N≈64.* Baseline α = 0.95 (s.e. 0.16). Settler mortality alone explains ~26% of variance in current institutions; each link of the longer chain (mortality → settlement → early institutions → current institutions) individually holds. Over-identification tests using early institutions and settlement share as additional instruments fail to reject. [[colonial-origins-and-the-settler-mortality-instrument]]
- **Acemoglu, Johnson & Robinson (2002)** — *(a) empirical.* The reversal of fortune: colonies rich in 1500 are poor today, a pattern robust across four independent source series for 1500 urbanisation and density and across a wide control set. The timing argument against "temperate drift" — the reversal is 19th-century and industrialisation-linked — is independent of the instrument and survives it.
- **Rodrik, Subramanian & Trebbi (2002)** — *(a) empirical.* Institutions beat geography and trade openness in a simultaneous horse race; the institutions coefficient is stable across dozens of permutations. Also the batch's only quantitative attempt at a *channel*: institutions' coefficient on physical capital per worker is ~6× that on human capital and ~3.2× that on TFP. [[institutions-vs-geography-vs-trade-horse-race]]

**The strongest form of Position A**, steelmanned: a single instrument produces a coefficient that survives an unusually broad robustness programme and reproduces across two different institutional-quality indices from two different vendors and two different research teams with different priors. The reversal-of-fortune pattern itself is not in dispute, and the geography camp has no comparably strong answer to it.

## Position B — the instrument does not identify institutions, and the indices do not measure them

**The claim.** Two separable objections that reinforce each other. The instrument is built from data too poor and too systematically mis-assigned to bear the weight; and the endogenous variable it instruments is a measure of recent policy outcome, not of durable institutional constraint.

**Sources, and note that two of the three re-run Position A's own regressions on Position A's own data:**

- **Albouy (2008)** — *(a) empirical: an archival data audit plus re-estimation.* **The single hardest fact in this conflict.** 36 of AJR's 64 mortality rates are borrowed from a neighbouring country or conjectured; 22 of those trace to two thin extrapolations — a chain of French campaign rates from western Mali spread across six countries partly through place-name confusion, and 16 Latin American countries assigned rates derived from **19 bishop deaths** across three temperature bands, scaled up by a factor benchmarked to a miscalculated Mexico campaign rate. Campaign and barracks rates are conflated, and the conflation runs *with* the hypothesis: campaign rates appear significantly more often in high-expropriation-risk, low-GDP countries (rejected at 2%). With both corrections applied, the first stage is **insignificant even with no controls and switches sign in three of eight specifications**; using weak-instrument-robust Anderson–Rubin inference, the confidence region for the institutions effect is **the entire real line** in most specifications. AJR's "results hold without Africa" defence leaves 13 non-conjectured countries whose surviving relationship is driven entirely by the Neo-Europes.
- **Glaeser, La Porta, Lopez-de-Silanes & Shleifer (2004)** — *(a) empirical.* The indices used across this literature (ICRG expropriation risk, KKM government effectiveness, Polity constraints on the executive) are outcome and perception measures: they rise sharply with income, have within-country volatility roughly **twice** that of years of schooling, mean-revert sharply, are close to uncorrelated with objective constitutional measures (electoral rule, judicial independence, constitutional review), and score a dictator who *chooses* not to expropriate identically to one who *cannot* — the USSR and Singapore among the ten lowest-expropriation-risk countries in 1984. On AJR's instruments specifically: log settler mortality correlates **.67** with modern malaria risk and **−.73** with years of schooling in 2000; re-running AJR's own joint mortality-and-malaria robustness regression on the full sample, both are significant; and in a 2SLS horse race off the same instruments, **predicted schooling predicts income and predicted executive constraints does not**.
- **Deaton (2009)** — *(b) methodological essay.* The framework, not the technical case. **External** (not caused by the outcome) does not imply **exogenous** (orthogonal to the error term); exogeneity "is an identifying assumption that must be made prior to analysis of the data, [so] no empirical tests are possible", which means an over-identification test cannot validate identification — passing is consistent with all instruments being invalid. And with heterogeneous effects, IV recovers a LATE for the complier subpopulation, which for AJR would be the ex-colonies whose institutional trajectory was actually shifted by settler mortality, not all ex-colonies. **Deaton names AJR once, in a list, and never demonstrates a competing channel** — see the note below.

**The strongest form of Position B**, steelmanned: over half the instrument's observations are not measurements, a third of it reduces to two extrapolations, the measurement error is correlated with the outcome in the direction that supports the hypothesis, and when the affirmative camp's own specifications are re-run on corrected data with inference appropriate to a weak instrument, the estimate is consistent with any value. Independently, the thing being instrumented moves too fast and correlates too poorly with actual constitutional rules to be the durable constraint the theory is about.

## What is established, and what is not

Four statements, kept apart because collapsing them is how this literature gets miscited.

| Proposition | Status |
|---|---|
| Measured institutional-quality indices correlate with national income | **Well-evidenced.** Both camps agree; not in dispute. |
| The constraint → investment → growth *mechanism* | **Theorised, unmeasured.** AJR call it a black box themselves and inherit it by citation. Rodrik's Table 3 decomposition is the only quantitative attempt and is not separately identified. |
| Settler mortality identifies institutions specifically | **Contested, unresolved.** Not shown; also not shown that a better-built instrument would fail. |
| Direction of causality between institutions, growth and human capital | **Contested, unresolved.** Only one sequencing test exists in this batch and it runs against Position A. |
| Corrected settler-mortality data still supports AJR's coefficient | **Evidenced against** (Albouy). |
| Standard indices measure durable constraint rather than recent policy outcome | **Evidenced against** (Glaeser et al.). |

## Position A is internally split

**[wiki synthesis]** This is not two camps. Three of the four affirmative sources undercut the strong reading themselves, and this matters for how the conflict is scored:

- **Rodrik, Subramanian & Trebbi** report that their **over-identification tests fail** in the 140-country sample (p = 0.0071 and 0.0365) and respond by preferring the smaller sample in which the test cannot be run. They title a section "An instrument does not a theory make" and state that "our findings do not map into a determinate set of policy desiderata." They also report the instrument's first stage decaying by decade (0.94 → 0.87 → 0.71), which weakens the persistence assumption the exogeneity rests on, and do not resolve the tension.
- **Besley & Persson** state directly that "there is no good reason to believe that these correlations can be interpreted causally", make state capacity endogenous by construction, and say of one of their own central results that "causation runs from income to market support and taxation, not the other way around". [[endogenous-state-capacity]]
- **AJR themselves** concede the culture confound as unresolved, concede that their malaria control is endogenous, concede that within Africa the first stage collapses, and concede in the Handbook chapter that their framework is "largely verbal rather than mathematical, and thus, by its very nature, not fully specified" and that "we do not as yet have a satisfactory understanding of the mechanisms through which institutions persist".
- **Wade's** fastest-growing cases score **low** on AJR's own constraint axis. [[developmental-state-and-embedded-autonomy]]

## A correction to this wiki's own framing

**[wiki synthesis]** The commissioning brief for this job stated that Deaton's Keynes Lecture uses AJR as its worked example. **It does not.** Deaton names AJR in a single sentence, in a list of six external-but-not-necessarily-exogenous instruments, establishing only that settler mortality is not reverse-caused by current income. He never names a competing channel — malaria, yellow fever, disease burden and ecology do not appear in the source — and never engages the expropriation-risk measure. His worked demonstrations are the aid-growth instruments and Angrist–Lavy's Maimonides rule. **Albouy and Glaeser carry the technical critique; Deaton supplies the general framework in which their results are read, and should not be cited as having audited AJR.** Recorded here so the overstatement does not propagate.

## What would settle it

**[wiki synthesis]** Two things, and only together. Neither exists in this batch.

1. **An independently reconstructed settler-mortality series with transparent provenance.** Every rate sourced to data collected inside the country it is assigned to; campaign and barracks rates separated and reported separately; laborer and soldier populations not compared on different statistics (maxima against averages); the imputation status disclosed per observation. Albouy's own verdict is that surviving colonial records may not support such a series — in which case the honest conclusion is that this instrument is *unavailable*, not that it works or fails.
2. **A timing and sequencing design.** This is what actually discriminates institutions→growth from growth→institutions, and it depends on no instrument. **Only Glaeser et al.'s Table 12 attempts one anywhere in this batch** — a fixed-effects panel at 5-year intervals, in which initial schooling predicts subsequent institutional improvement on 3 of 4 measures while initial institutions predict no subsequent improvement in schooling. A symmetric design run by the affirmative camp on the affirmative camp's variables does not exist here, and its absence is itself informative.

**[wiki synthesis]** A third thing would settle a different and, for this wiki, more important question: **any design at all that measures an individual institution's effect on production.** Nothing in this batch does. See [[open-questions]] Q90.

## Source

- `raw/research/institutions-and-growth/01-ajr-colonial-origins.md` — Acemoglu, Johnson & Robinson, "The Colonial Origins of Comparative Development: An Empirical Investigation", NBER WP 7771 (*AER* 91(5), 2001). https://www.nber.org/system/files/working_papers/w7771/w7771.pdf
- `raw/research/institutions-and-growth/02-ajr-reversal-of-fortune.md` — Acemoglu, Johnson & Robinson, "Reversal of Fortune", NBER WP 8460. https://www.nber.org/system/files/working_papers/w8460/w8460.pdf
- `raw/research/institutions-and-growth/03-ajr-institutions-fundamental-cause.md` — Acemoglu, Johnson & Robinson, "Institutions as the Fundamental Cause of Long-Run Growth", NBER WP 10481, 2004. https://www.nber.org/system/files/working_papers/w10481/w10481.pdf
- `raw/research/institutions-and-growth/04-rodrik-institutions-rule.md` — Rodrik, Subramanian & Trebbi, "Institutions Rule", NBER WP 9305, 2002. https://www.nber.org/system/files/working_papers/w9305/w9305.pdf
- `raw/research/institutions-and-growth/05-besley-persson-state-capacity.md` — Besley & Persson, "State Capacity, Conflict and Development", NBER WP 15088, 2009. https://www.nber.org/system/files/working_papers/w15088/w15088.pdf
- `raw/research/institutions-and-growth/06-wade-developmental-state-dead-or-alive.md` — Robert H. Wade, "The Developmental State: Dead or Alive?", *Development and Change* 49(2), 2018, 518–546. https://researchonline.lse.ac.uk/id/eprint/87356/1/Wade_%20Developmental%20State.pdf
- `raw/research/institutions-and-growth/07-crit-glaeser-do-institutions-cause-growth.md` — Glaeser, La Porta, Lopez-de-Silanes & Shleifer, "Do Institutions Cause Growth?", NBER WP 10568, 2004. https://www.nber.org/system/files/working_papers/w10568/w10568.pdf
- `raw/research/institutions-and-growth/08-crit-albouy-settler-mortality.md` — David Y. Albouy, "The Colonial Origins of Comparative Development: An Investigation of the Settler Mortality Data", NBER WP 14130, 2008. https://www.nber.org/system/files/working_papers/w14130/w14130.pdf
- `raw/research/institutions-and-growth/09-crit-deaton-instruments-of-development.md` — Angus Deaton, "Instruments of Development", Keynes Lecture, British Academy, 2008/2009. https://www.princeton.edu/~deaton/downloads/Instruments_of_Development.pdf

## Related

- [[colonial-origins-and-the-settler-mortality-instrument]] — the anchor page, carrying the instrument, the Albouy audit and the Glaeser measurement attack in full detail.
- [[institutions-vs-geography-vs-trade-horse-race]] — Position A's second exhibit, and the source of the failed over-identification test that splits Position A internally.
- [[institutions-as-fundamental-cause]] — the theory Position A is defending, with its authors' own "largely verbal... not fully specified" verdict on it.
- [[endogenous-state-capacity]] — an affirmative-camp source that denies the causal reading of its own correlations.
- [[developmental-state-and-embedded-autonomy]] — the case set in which growth and measured executive constraint move in opposite directions.
- [[constraint-vs-capacity-as-the-investment-mechanism]] — the mechanism-level conflict this one leaves open; even if identification were settled, that one would not be.
- [[credible-commitment]] — the same substantive claim on single-case historical evidence, with the opposite weakness: a mechanism with one canonical illustration rather than a large sample with a contested instrument.
- [[decay-as-real-vs-decay-as-overstated]] — the structural parallel is worth noting: in both conflicts the affirmative camp's canonical evidence turns out on inspection to be thinner than its citation record implies, and in both the critics run no positive test of their own.
- [[open-questions]] — Q15 (the arrow's strength, now with far more evidence attached), Q90 (level of analysis), Q91, Q92.
