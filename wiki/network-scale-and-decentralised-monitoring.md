# Network Scale and Decentralised Monitoring

Tchuente (arXiv 2511.23320, Nov 2025) models monitoring as a network public good and derives a size threshold above which centralised monitoring beats decentralised: when units' efforts are strategic complements, local monitors internalise too little of the spillover, and the complementarity needed to justify centralisation falls as the network grows. Applied to US nursing homes, the paper reports kinks in severe-failure incidence at about 7 homes per county and about 34 homes per chain. **Treat as a suggestive single-sector datapoint, not an established scale law:** the source is a single-author, un-refereed preprint; the empirical outcome is a count; nothing is causally identified; and the paper is internally inconsistent on the county threshold.

**Evidence tier note.** The theory is (b): a formal model with derived results (Theorem 1, a stochastic extension), internally valid but assumption-driven, with the key premise that centralisation internalises more complementarity at higher cost built in. The empirical layer is (a) but weak: one cross-section of CMS administrative data (Oct 2025), facility-level regressions with threshold tests at county and chain level. The strongest empirical element is the sup-F break test with placebo checks. Status: **un-refereed arXiv preprint**, Purdue Dept of Agricultural Economics.

## The model

**[model]** Each unit's marginal return to its own effort rises with its neighbours' mean effort (strategic complementarity, parameter lambda). Monitoring is a public good on the network. Centralised monitoring internalises more of the complementarity (lambda_C > lambda_D) but costs more (K_C > K_D). Equilibrium effort is amplified by 1/(1-lambda). Theorem 1: a unique threshold lambda*(n) exists and is strictly decreasing in network size n; inverted, decentralised oversight is optimal only below n*(lambda). In a linear-Gaussian stochastic extension, variance and shock sensitivity rise sharply as lambda times the network's largest eigenvalue approaches the threshold.

**[wiki synthesis]** The scale logic is externality-driven, which separates it from [[knowledge-hierarchies-and-the-cost-of-scale]], where depth is cost-minimising under a knowledge constraint. Lambda is the strength of cross-unit interaction, so the model is a formal complement to the qualitative licence in [[hierarchy-and-near-decomposability]]: delegating on aggregates is safe when interactions are weak, and the model says it fails when they are strong relative to size. It is a network version of the nonseparability that grounds monitoring in [[team-production-and-monitoring]].

**Caveat on the unit.** What is "too big" is the monitored network (counties, chains), not the monitor. The regulator's own size is never modelled, and the paper treats it as a benevolent welfare maximiser.

## The nursing-home evidence

Unit: certified skilled nursing facilities (SNFs) nested in counties and in corporate chains (about two-thirds of SNFs), regulated by one federal agency, CMS.

**[empirical — cross-section, sup-F break test]**
- Break in severe-failure (Special Focus Facility, SFF) incidence against log network size: county sup F = 508.5, break at about 7 homes; chain sup F = 36.3, break at about 34 homes. Placebo breaks on ownership shares fall at 2-3 facilities and are small and unstable.
- Peer-correlation coefficients rise above threshold: county overall-rating 0.150 below vs 0.758 above; chain overall-rating 0.680 below vs 0.837 above.
- Variance: county deficiency variance about 178 above vs 92 below (Levene rejects equality); overall-rating variance unchanged.
- Deterioration (change in deficiencies between inspection cycles): significantly worse in large counties; positive but imprecise in large chains (confidence interval includes zero).

**[empirical — a prediction that fails]** In large chains variance is lower, not higher: large chains are more homogeneous (consistent with internal standardisation) while still showing more tail failures. The paper concedes its variance-amplification prediction "does not apply uniformly across institutional architectures". **[wiki synthesis]** Homogeneity in the bulk coexisting with higher tail failure is a useful counterexample to reading standardisation as safety; compare [[institutional-isomorphism]].

## Caveats that bound what this shows

1. **Count outcome.** The outcome is a count of SFF facilities against log network size, so some mechanical increase with size is expected; a kink in a count is not a kink in a rate. No per-facility rate threshold is reported in the text.
2. **Outcome conflation.** SFF is a regulator-selected designation, mixing facility failure with CMS targeting. A conflation failure under [[measurement-validity-framework]]; see also [[multitask-incentive-theory]] on regulator-selected metrics.
3. **No causal identification.** The paper explicitly declines to solve the reflection problem (Manski 1993); the peer regressions are "linear projections" and "maintained assumptions". The claim is correlational.
4. **Single cross-section.** "Deterioration" is a change between two inspection cycles, not a panel.
5. **Thresholds are not estimates of n*(lambda).** Lambda is never estimated, so reading the breakpoints as n*(lambda) is an interpretation, not a test. Title and abstract frame them as sharp realisations of the model; the evidence is weaker than that framing.
6. **The central benefit is assumed, not tested.** lambda_C > lambda_D is built in; no data test whether centralised monitoring improves outcomes above the threshold. K_C is a free parameter and no cost of centralisation is measured.
7. **Internal inconsistency on the county threshold.** The text gives both "about 7" (the break at log n = 2.20) and "more than approximately nine nursing homes" (Section 6.2.1), and the placebo text says "6-7". Which number to cite is unresolved; this page says "about 7" and flags the discrepancy. Do not quote the threshold to false precision.
8. **Scope.** US nursing homes, Oct 2025 vintage, CMS regime; single-break specification only; grid restricted to the 10th-90th percentile of log n; controls limited to ownership, beds, ratings and state fixed effects. The thresholds 7 and 34 are sector-specific, not constants. Counties are administrative units, not necessarily the true monitoring network.

## Levers proposed, and their evidence

The source proposes size-triggered federal involvement (prioritise screening and enhanced reviews above about 7 homes per county and 34 per chain) and corporate compliance staffing that scales with chain size. **[wiki synthesis]** The evidence base is the correlational threshold and spillover results above; nobody evaluates whether such targeting improves outcomes. A targeting rule also presumes a non-captured regulator, an assumption left open by the paper and exposed to [[regulatory-capture]] by large chains.

## Public/private and power

**[wiki synthesis]** The paper claims generality (school districts, hospital networks, water utilities, foster care) across public regulators and private chains, with the caveat that the dispersion-standardisation balance depends on institutional architecture. Within the data the geographic network (regulatory-facing) amplifies variance while the organisational network (corporate) dampens it, so the two do not behave invariantly. Generality beyond nursing homes is asserted, not tested. On power the paper is silent: no regulator selection, capture or lobbying by large chains. Decentralised versus centralised monitoring is a [[formal-and-real-authority]] choice in which monitoring intensity, not information, is the lever. Not named in the source: capture, goal displacement, ossification, and any age claim.

## Source

- `raw/research/weekly-2026-10-06/01-too-big-to-monitor.md` — Tchuente, "Too Big to Monitor? Network Scale and the Breakdown of Decentralized Monitoring", arXiv:2511.23320, Nov 2025. Un-refereed preprint.

## Related

- [[knowledge-hierarchies-and-the-cost-of-scale]] — the other threshold-like scale account; knowledge constraint there, externality internalisation here.
- [[hierarchy-and-near-decomposability]] — Simon's qualitative licence to delegate; lambda formalises the interaction strength it depends on.
- [[team-production-and-monitoring]] — monitoring as a response to nonseparability.
- [[polycentric-governance]] — Ostrom's nested monitoring; this adds a size-conditioned account of when local monitoring stops sufficing.
- [[incentives-under-multiple-principals]] — regulator, chain headquarters and county form a multi-layer structure whose principal conflicts the paper does not model.
- [[formal-and-real-authority]] — the delegation choice, with monitoring intensity as the lever.
- [[organizational-economics-of-the-state]] — O-ring-like interdependence across units and systems-level monitoring design.
- [[state-capacity-and-level-of-government]] — the tier at which to monitor, with a size trigger.
- [[bureaucratic-growth-and-parkinsons-law]] — scale pathology located in the monitored population rather than the bureau's headcount.
- [[dimensions-of-institutional-variation]] — candidate axes: monitoring locus, complementarity strength, network-size threshold for oversight regime.
- [[institutional-isomorphism]] — large chains' homogeneity alongside tail failure.
- [[regulatory-capture]] — exposure of a size-triggered targeting rule.
- [[multitask-incentive-theory]] — regulator-selected metrics.
- [[measurement-validity-framework]] — SFF count as a conflated measure.
