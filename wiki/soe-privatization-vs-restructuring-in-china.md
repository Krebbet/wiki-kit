# SOE Privatization vs Restructuring in China (Wang 2026)

Wang (arXiv 2610.08729, Oct 2026) estimates capital-, labor- and material-augmenting productivity for Chinese industrial firms 1998-2008 and finds that SOE privatization raised only labor-augmenting productivity, and only briefly (about +0.023 log points in the first three years, fading to a non-significant -0.011). Most of the state sector's productivity catch-up came instead from restructuring of the SOEs the state kept, plus exit of the weakest plants. **Treat as a strong-data, weak-identification datapoint on ownership change as a lever, not a verdict on privatization as a whole:** the source is an un-refereed preprint, productivity is revenue-based, and the counterfactual (kept SOEs) is assumed credible rather than randomised.

**Evidence tier note.** The empirical layer is (a): the NBS Annual Census of Industrial Production (cleaned by Jaumandreu and Yin), 372,813 firms and 1,659,612 firm-years, ten manufacturing sectors, structural CES estimation by dynamic-panel GMM with an ownership-augmented productivity process, plus a Callaway-Sant'Anna event study. Identification is by design assumption (predetermined ownership, destination-matched pre-privatization terms), not a quasi-experiment. The mechanism readings (soft budgets, administrative input allocation) are (b)-style interpretation: stated, not tested. Status: **un-refereed arXiv preprint by a PhD candidate**. Everything on this page not attributed to the paper is **[wiki synthesis]**.

## The population and the contrast

**[empirical]** SOEs fell from 17,271 (1998) to 3,351 (2008), over 80%; private firms rose from 29,146 to 189,337. Of 35,663 ever-SOE firms: 1,608 stayed state-owned throughout ("kept"), 15,235 exited the panel, 8,695 were clean privatizers (7,325 to private, 1,078 to collective, 240 foreign, 52 mixed), and 6,916 were excluded (re-nationalizers and ownership "flicker"). Ownership is set by the majority shareholder (50% of paid-in capital). The design compares privatizers to kept SOEs, not to the pooled SOE population, which is dominated by exiters.

## What the data show

**[empirical]** Technological change is strongly factor-biased, not Hicks-neutral: mean annual growth is 16.9% capital-augmenting, 14.2% labor-augmenting, 0.4% materials-augmenting; the elasticity of substitution is 0.384 (gross complements).

**[empirical]** Privatization (to private or foreign) versus kept SOEs:

| Factor | Early (first 3 yrs) | Late |
|---|---|---|
| Labor-augmenting | +0.023 | -0.011 (n.s.) |
| Capital-augmenting | +0.021 (p<0.10) | -0.049 (significant) |
| Materials-augmenting | -0.017 | -0.016 |

Privatization to collectives carries a labor penalty (about -0.07). Privatized firms do not converge to always-private levels; they track the kept-SOE trajectory. Privatizers also show higher markups (+2.9% post vs pre).

**[empirical]** The 1998 incumbent cohort (73,728 firms, the heaviest legacy overstaffing) is the exception: labor gains of +0.081 early and +0.112 late, persistent, with no capital gain.

**[empirical]** Catch-up decomposition (Melitz-Polanec) of the state sector's 1999-2008 mean productivity change (+2.04 log points K, +1.96 L): the within-survivor shift is 1.573 for K (about 77%) and 1.192 for L (61%); entry about 28% / 26%; exit/selection is -0.111 for K and +0.213 for L (about 11% of the labor change, almost all low-productivity firms leaving the panel); privatized-out firms contribute slightly negatively (-0.047 K, -0.031 L). Kept SOEs raised output 10.4%/yr with capital -0.6%/yr and labor -2.2%/yr, output growth coming via materials (+9.9%/yr).

**[empirical]** Levels differ by ownership: SOEs sit below private firms on capital and labor augmentation (private steady-state capital gap 0.82 log points) but above on materials-augmentation (private -0.081, collective -0.079, foreign -0.029, all p<0.01). Exiting SOEs were far below kept SOEs on K (-0.188) and L (-0.179).

**[wiki synthesis]** The headline decomposes into three separable margins that the policy label "SOE reform" bundles: ownership level (who holds the shares), ownership change (the transition event), and restructuring of the firm under unchanged ownership. The paper finds level matters for K and L, change adds little, and restructuring dominates the catch-up.

## Mechanism as the source states it

**[model]** The labor gain is read as shedding of administratively inflated employment sustained by soft-budget guarantees, so privatization removes a one-time stock of excess labor and has no second act. The materials reversal is read as preferential administrative access to inputs. Neither is directly tested. Part of the capital result may be repricing of formerly subsidised state capital: a 30% subsidy assumption strengthens the capital null (early capital wedge falls to -0.092).

**[wiki synthesis]** If the mechanism is right, the gain is a stock adjustment (excess labor) rather than a flow improvement in efficiency, which fits the front-loaded fade and the larger persistent effect in 1998 incumbents, where the stock was biggest. This is one reading; the paper has no direct overstaffing measure.

## Tension with the wiki's ownership theories

State as a tension, not a ruling.

- **[[property-rights-theory-of-the-firm]].** Grossman-Hart ownership shifts the owner's incentive to make non-contractible, relationship-specific investment. Hart's prison application predicts a private operator has a greater incentive to cut cost and to innovate, with the contingency that the case is weak where quality-cutting or violence matters. Wang's early labor shedding is consistent with the cost-cutting half. The absence of a persistent capital or materials gain, and the failure of privatizers to move off the kept-SOE trajectory, sits uneasily with the innovation half. But the theory is about specific investments and contract incompleteness, and the paper measures revenue productivity by factor, so the two do not test the same object. Not a refutation either way.
- **[[agency-costs-and-ownership-structure]].** Jensen-Meckling predicts agency cost rises as the owner-manager's equity share falls, with the loss priced ex ante into the claim. It is a model of dispersed equity, not of a state principal with no tradable claim. Wang's finding that ownership change does little within-firm is hard to square with a simple reading that concentrating private residual claims cuts agency cost. It is compatible with the view that the state-owned firms in the sample were already being restructured and monitored via other channels, and that "private" destination firms need not be owner-managed. The paper does not observe the post-privatization ownership structure beyond the majority-holder category.
- **[wiki synthesis]** The common thread: both theories condition the efficiency gain on features the paper does not measure (contract incompleteness, monitoring intensity, competition). The wiki therefore holds an open tension between theory-predicted ownership effects and one large dataset where the effect is small and transient. The 1998-incumbent result (large and persistent) shows the effect is not uniformly absent, so the tension is about average effect and timing.

## Caveats that bound what this shows

1. **Revenue-based productivity.** Outputs are revenue, so factor-augmenting productivity is conflated with price and markup; cross-factor contrasts are largely insulated, but levels are not. Higher post-privatization markups may be read as productivity.
2. **Selection by design assumption.** No randomised or quasi-experimental shock. Credibility rests on privatization taking 8-14 months from decision to implementation and on near-zero pre-terms (K +0.012 n.s., L +0.020). "Grasp the large, let go of the small" is non-random selection by the state.
3. **Capital pre-trend.** The capital event-study path has a pre-trend (p=0.01), so the capital result is suggestive only. The labor leads are flat (joint p=0.59).
4. **Exit is confounded.** Ownership terms for exiting SOEs blend type gap and negative-shock selection; exit from the panel is not the same as closure.
5. **Mechanism untested.** Soft budgets, overstaffing and input allocation are interpretations; no direct measure.
6. **Scope.** Chinese manufacturing 1998-2008 only (post-2008 NBS data unreliable; no value-added or intermediates), firms above 5m RMB sales plus all SOEs, 50% majority-ownership threshold, CES with three factors and AR(1) productivity. Generalisation to later periods is asserted, not tested. Industry subsamples are thin and some wedge estimates reach only p<0.10.
7. **The paper's own limit.** It says privatization is one margin of reform and the null does not concern the reform as a whole. Reading it as "privatization does not work" overstates it.
8. **No power or party variable.** Nothing on cadre appointment or party control, so it cannot be read against [[party-organisation-control-of-chinese-soes]] on those mechanisms.

## Levers and their evidence

| Lever | Yield in this paper | Evidence base |
|---|---|---|
| Ownership transfer | Small, transitory, labor-only | **[empirical]** large panel, selection by design assumption |
| Restructuring of retained state firms | Dominant (about 61-77% of the within-state catch-up) | **[empirical]** decomposition; the specific restructuring actions are not identified |
| Exit of weakest plants | About 11% of labor gain | **[empirical]** decomposition |
| Hardening budget constraints, repricing subsidised capital | Implied only | **[model]** not tested |

**[wiki synthesis]** The restructuring lever is the largest yet least specified: the paper shows retained SOEs shed labor and raised output on flat capital, but not what management, incentive or control changes did it. That is the gap to fill before it is a usable lever; see [[reform-levers]] for how the wiki tiers lever evidence. No evidence here on any of this in a non-Chinese or non-manufacturing setting.

## Public/private and power

**[wiki synthesis]** Levels deny invariance (private beats SOE on K and L, SOE beats private on materials), yet the transformation process looks largely invariant to the ownership label: the gains come from restructuring and selection rather than from the label change. On power the paper is silent beyond the state's discretion over which firms to privatize or close and its administrative allocation of inputs. Not named in the source: capture and decay vocabulary, and any firm-age effect (only an incumbent vs entrant cohort contrast).

## Source

- `raw/research/weekly-2026-10-13/01-china-soe-privatization-technology.md` — Ziyao Wang, "Ownership and Non-Neutral Technological Change: Evidence from China's State-Owned Enterprise Privatization", arXiv:2610.08729 (v. Oct 7 2026). Un-refereed preprint. Summary read: `raw/research/weekly-2026-10-13/.ingest/01-china-soe-privatization-technology.summary.md`.

## Related

- [[party-organisation-control-of-chinese-soes]] — same SOE universe; this paper has no party-control variable, so ownership and party control are unlinked here.
- [[property-rights-theory-of-the-firm]] — residual-control transfer predicts efficiency effects; tension stated above.
- [[agency-costs-and-ownership-structure]] — ownership concentration and agency cost; tension stated above.
- [[separation-of-ownership-and-control]] — ownership versus control or restructuring as separate levers.
- [[decision-rights-and-authority-theory-of-the-firm]] — restructuring authority within retained state firms.
- [[reform-levers]] — ownership transfer, internal restructuring and exit as levers with different yields.
- [[political-economy-of-public-sector-reform]] — selection vs treatment in reform evaluation.
- [[regionally-decentralized-authoritarianism]] — context for Chinese SOE reform dynamics.
- [[developmental-state-and-embedded-autonomy]] — selective state retention ("grasp the large, let go of the small").
- [[rent-seeking-and-the-welfare-cost-of-transfers]] — capital subsidy and administrative input allocation as transfers.
- [[internal-conflict-and-structural-inefficiency]] — soft-budget-sustained overstaffing as structural inefficiency.
- [[governance-structures]] — state versus private governance on factor-specific efficiency.
- [[institutional-sclerosis]] — legacy overstaffing in 1998 incumbents.
- [[gradual-institutional-change]] — decade-long staged SOE reform.
- [[fast-and-slow-moving-institutions]] — front-loaded transition gain that fades.
- [[dimensions-of-institutional-variation]] — ownership type, destination and timing as candidate dimensions.
- [[firm-age-and-performance]] — weak link: incumbent vs entrant cohort contrast, not age.
- [[open-questions]] — does ownership-level or restructuring-level control drive public-sector gains?
