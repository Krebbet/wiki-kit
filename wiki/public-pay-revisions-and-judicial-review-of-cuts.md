# Public Pay Revisions and Judicial Review of Cuts

Quaiyyum (arXiv 2611.12565, Nov 2026) treats public pay as a nominal price fixed by law, so governments revise it in discrete, fiscally conditioned steps: a fixed cost of acting makes revisions large and rare, a convex cost of financing a raise at once makes them small and frequent. A dynamic discrete-choice model fitted to legal pay acts in eleven countries is then used to evaluate two institutional designs. Review of cuts by a court after they take effect (Portugal) invites cuts the court will strike, and partial indexation (Bangladesh) beats full indexation once automatic increases must be financed.

**Evidence tier note.** Status: **un-refereed arXiv preprint**, so all findings are provisional. Tier (a) for the hand-built documentary record of pay acts, the fixed-effects regressions and the Portuguese ruling record; tier (b) for the structural model (a formal model with derived propositions, estimated rather than identified by exogenous variation); the two design experiments are model-conditional counterfactuals, closer to (b) than (a). The author states the model accounts for pay histories but does not forecast them.

## The reset logic

**[model]** Pay is nominal, so inflation erodes it between legal acts. Two costs pull in opposite directions: a fixed cost of acting (a legislative round, a commission) pushes toward larger, rarer revisions; a convex financing cost (the whole payroll increase must be funded at once) pushes toward smaller, more frequent ones. Faster erosion makes revisions both larger and more frequent, and the elasticity of revision size to erosion identifies which cost dominates (Corollary 1). The fixed-cost half is borrowed from firm price-setting (menu costs); the author states the financing-cost half has no firm counterpart.

**[model]** Cuts occur only under market stress or an adjustment program, because the Treasury requires payroll savings that rise with the sovereign spread; a cut lowers the deficit that feeds next year's stress risk. Post-crisis debt overhang raises the political cost of the payroll and holds pay down (in Portugal, while debt exceeds 85% of GDP).

## Empirical patterns

**[empirical]** Design: a hand-built record of the general civil-service pay decision from the legal act or official notice, dated by first payment, for eleven countries (Portugal 2008-2024, Spain and Lithuania 2007-2023, Hungary 2007-2012, Ireland, Italy, Cyprus, Romania, US 1995-2024, Bangladesh 1989-2024, India 1987-2024; 233 country-years) plus a 50-country ledger of 151 legislated changes (1977-2024). An undocumented year is coded "unknown", never "no change". A year-by-year audit found 292 general revisions the ledger had omitted (31 of 100 random years).

- **Pay erodes between acts and is restored in steps.** Cross-country, raise size and interval length are rank-correlated (0.44, p = 0.01), unconditional on inflation.
- **Raises and cuts arise in different circumstances.** Country and year fixed-effects linear-probability models: lagged growth raises the probability of a raise by 2.04pp and lowers that of a cut by 1.34pp; fiscal balance is a point weaker (+1.35pp on cut).
- **Legal reversals create payment paths.** Legislated, paid and lasting cuts differ, so a cut on the statute book is not a cut that stays.

## Judicial review of cuts (Portugal)

**[empirical]** Case record: the Constitutional Court's rulings 353/2012, 187/2013 and 413/2014; three of four crisis cuts were struck, two after taking effect.

**[model]** Proposition 2: a court that strikes cuts after they take effect leaves the temporary saving with the Treasury, so the government proposes cuts it expects to lose, since each has some chance of standing. The incentive disappears only if review is both certain and prior to effect (stated as complements).

**[model]** Counterfactual courts over Portugal's 2010-2024 budgets, from the 2010 documented state with the documented macro history; the government re-solves under each court. Calibrated court: strike probability 0.9, after effect.

- No court: cuts in force sum to 121 log points; social loss 25.83 a year; mean crisis-year pay 85.9% of reference.
- Calibrated post-effect court: cuts in force sum to 62; loss 37.04. Struck cuts save 12.9% of a year's payroll while in force, but the restorations that undo them add 20.0%, financed at once. Crisis-year pay is lower (83.8%), so the court does not protect pay during the crisis.
- Review before effect: temporary savings vanish, restorations fall to 6.2% of payroll, cuts in force 41, crisis pay 86.8%, loss 29.06.
- Review before effect and certain: the government proposes no excess cuts; cuts in force 30, crisis pay 87.7%; cost is debt of 95.4% of GDP in 2024 against 93.1%.
- Every one of 20 courts (four strike probabilities by five review delays) costs at least 2.29 a year more than no court. After-effect courts pay through restoration financing; before-effect courts through the Treasury's penalty.

**[wiki synthesis]** Read carefully: the paper's claim is that timing and certainty of review rank designs, not that review is welfare-improving. Its objective values a court only through pay, budget and output, so any protective value of the court (rule of law, employee rights) is outside the loss. The result is crisis-specific: in the model's own world, where crises are about 6% of years, the courts hardly differ, and faster or more certain review does not reduce struck cuts.

## Financed indexation (Bangladesh)

**[model]** Pay is set by a commission (about one scale per six years) with interim allowances. Free full indexation would cut the stationary loss from 17.22 to 5.14 a year. When automatic increases must be financed, the government lets pay fall further behind, because lower pay makes each automatic increase cheaper: mean pay 85.7% of reference under full financed indexation against 88.1% when financing is free. Because the financing charge is quadratic, halving the indexed share keeps half the protection at a quarter of the charge. Half indexation lowers loss (without fixed costs) up to a financing coefficient of 0.99 of the estimated allowance coefficient (0.77 across the confidence region); full indexation only below 0.34 (0.13). Wherever half indexation lowers social loss, the government is also better off by its own objective.

## What the paper cannot carry

- **[empirical]** In-sample fit is good: the documented value lies inside the 90% model interval for 31 of 34 statistics in annual countries passing a pre-fixed adequacy test. But re-estimated without a block of years, the model predicts the block worse than constant probabilities, and outside Portugal and Spain a myopic government fits as well as a forward-looking one (Bangladesh included).
- The output-transmission block is calibrated and conditional, not identified; Portuguese alternative pay paths differ little in output but widely in financing cost. Overhang is placed only within a wide set.
- Court and indexation results each rest on one country (four rulings; one commission case). Eleven hand-picked countries, mostly euro-area crisis years; eight European, US, Bangladesh, India. Court incentives and appointment are not modelled; ruling probabilities are calibrated to Portugal.
- The levers are model predictions under a calibrated welfare objective, not tested interventions.

**Ideological priors.** Mainstream macro-fiscal (structural dynamic discrete choice); no partisan lean. Taxpayer-versus-employee weight is an estimated parameter. The conclusion that prior review would have cut Portugal's crisis cost is stronger than a model without out-of-sample forecasting power can carry.

## Source

- `raw/research/weekly-2026-11-10/02-government-pay-revisions.md` (arXiv 2611.12565, Quaiyyum, "That Time of the Year Again: Government Pay Revisions in the Aggregate Economy").

## Related

- [[credible-commitment]] — indexation is a commitment device; financing cost decides whether giving up discretion pays.
- [[veto-points-and-bureaucratic-autonomy]] — a court as veto point on cuts; post-effect review leaves the saving in place.
- [[political-decay-and-vetocracy]] — judicialisation with a measured fiscal cost, on a different object (pay, not procedure).
- [[personnel-economics-of-the-state]] — the budget-level pay decision upstream of recruitment-wage effects.
- [[civil-service-tenure-and-political-insulation]] — pay as a lever the political principal holds, distinct from tenure.
- [[whitehall-monitor-2026-case-profile]] — SCS pay 24% below 2010 as an instance of erosion and reset.
- [[blame-avoidance-and-negativity-bias]] — cuts only under external compulsion; consistent with blame avoidance, not tested here.
- [[measurement-validity-framework]] — "unknown" versus "no change" coding and the 292 omitted revisions.
- [[dimensions-of-institutional-variation]] — candidate rows: indexation share, fixed versus financing revision cost, timing and certainty of review.
- [[reform-levers]] — two model-predicted levers, below randomised evidence.
- [[neo-weberian-state-and-administrative-traditions]] — continental court intervention on pay versus US statutory formula.
