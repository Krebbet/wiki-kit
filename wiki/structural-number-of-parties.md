# The Structural Number of Parties

Un-refereed arXiv preprint (2611.24714, Nouboukpo, Aladji and Muktar 2026). Proposes the Structural Number of Parties (SNP), an election-independent benchmark for party-system scale computed only from population P and area A: N = max(2, ln[(P/10^6)(A/10^4)]). Applied to 54 African states, it is set against registered-party counts and the Golosov effective number of parties (ENP) to flag "over-" and "under-fragmented" systems. The authors' own tests show the SNP is uncorrelated with realized fragmentation, so it works as a descriptive scale, not as a predictor of how many parties a state sustains.

**Evidence tier note.** (b) for the SNP itself: a defined index with stated mathematical properties (monotonicity, floor, logarithmic returns), not an estimated relationship; the "structural capacity" reading is the authors' **[model]** interpretation. (a) only for the descriptive tables: World Bank population and area for 54 states, a 17-state registration-versus-ENP sample (counts and elections from different years, cross-sectional), and 50-state correlations with existing indices. No causal design and no outcome validation. Scope is Africa.

## Findings

- **[model]** Definition: floor of 2 (the authors cite Sartori's hegemonic/competitive line), log of the population-area product, constants P0 = 10^6 and A0 = 10^4 chosen by convention. The gaps are log ratios: registered parties over SNP, ENP over SNP, and registered over ENP (the last needs no SNP).
- **[empirical]** SNP spans 2.00-10.12 (median 6.06); ten small states sit at the floor. Annual change 2013-2023 is small (median 0.23), because it equals log population growth.
- **[empirical]** All 17 registers exceed the SNP (median 14x) while Golosov ENP is below it in 14. Registered-to-effective ratios run from 3.2 (Benin) to 219 (Cameroon), median 25. DR Congo is the one case with both register and ENP far above the benchmark.
- **[empirical]** The SNP does not track realized fragmentation: Spearman rho 0.06-0.08 with ENP, and about zero once DR Congo is dropped. It tracks the Seat Product estimate (rho 0.89), but that is mostly shared population content; area adds no measurable information (coefficient not significant).
- **[empirical]** Nine of the 14 "below benchmark" cases have ENP under 2, so their negative sign follows from the floor, not from scale. Signs are robust to the calibration constant for 16 of 17 states; magnitudes are not and are read only comparatively.
- **Internal tension.** The conclusion speaks of a "profound impact" of geography and demography on fragmentation. The paper's own correlations show none among 49 states, and the baseline is normative by construction, so no result could have shown it wrong.

## Reading for the wiki

**[wiki synthesis]** A worked case for [[measurement-validity-framework]]: the index has construct definition and robustness checks but no criterion validation. It cannot fail, since it never meets an outcome. Its useful part is the register-versus-effective-competition ratio, which needs no SNP. That ratio measures formal pluralism against effective pluralism, an instance of form-versus-function divergence like that in [[goal-displacement-and-bureaucratic-ritualism]], and a candidate row (de jure entry vs de facto competition) for [[dimensions-of-institutional-variation]]. The paper's point that ENP is unavailable where elections are suspended parallels the coverage problems of [[v-dem-measurement-model]]. Party count is the input to veto-player counts in [[veto-players-and-policy-stability]], so a structural-count baseline would matter there only if shown to predict effective counts; this paper shows it does not. No existing page is contradicted.

## Source

- `raw/research/weekly-2026-11-24/03-structural-number-of-parties.md` (arXiv 2611.24714; un-refereed).

## Related

- [[measurement-validity-framework]] — construct vs criterion validity.
- [[v-dem-measurement-model]] — expert-coded regime indices where election data are weak.
- [[veto-players-and-policy-stability]] — party count as veto-player input.
- [[selectorate-theory-and-the-winning-coalition]] — dominant-party and winning-coalition logic.
- [[goal-displacement-and-bureaucratic-ritualism]] — formal registration without effective function.
- [[dimensions-of-institutional-variation]] — de jure vs de facto competition.
