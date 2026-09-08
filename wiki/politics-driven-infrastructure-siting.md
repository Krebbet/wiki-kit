# Politics-Driven Infrastructure Siting and the Cost of Political Redesign

A state can build infrastructure that is net-positive for the economy and still route it wrong, on purpose — because the route serves the ruler's own strategic geography, not the market's. China's Grand Canal, forcibly rerouted after the Mongol Yuan moved the capital to Beijing in 1271, is a rare case where the size of that "political redesign tax" is directly measured against a market-optimal counterfactual: the canal was worth 2.5–6.1% of aggregate population, but the specific politically-chosen route sacrificed roughly a third to a half of that gain (1.1–2.2% of population) relative to a trade-cost-minimizing route.

## Mechanism

The Grand Canal's actual course is best explained not by trade-cost minimization but by the least-cost route connecting the military frontier, the economic core, and wherever the capital happens to sit. **[empirical]** A 1 km increase in the "optimal route to the capital" (a constructed least-cost path) predicts ~0.87 km of actual waterway — the canal was built to move troops, tribute grain, and officials to and from the seat of power, not to maximize trade volume.

The causal chain runs: capital location → canal route → market access → population/economic activity. Market access (a Donaldson–Hornbeck-style discounted sum of other grids' population, weighted by travel cost) raises local population density. **[empirical]** A 1% increase in market access predicts ~0.14–0.24% more population density, with OLS and IV estimates converging. The market-access-to-population mechanism itself is standard spatial economics; the paper's contribution is showing that in this setting the market access is *politically*, not economically, determined — an infrastructure network's shape is downstream of a sovereign's location choice, not of trade-cost geometry.

## Identification strategy

The 1271 Mongol capital relocation is treated as a natural experiment: an exogenous shock to where the political center of gravity sat, unlikely to recur, that reshaped an entire transportation network. **[empirical]** Two placebo/event-study tests pin the channel down as genuinely political rather than merely geological or trend-driven:

- The route to the *prior* (Song) capital predicts the canal's path before 1271 and loses predictive power after.
- The route to the *new* (Yuan) capital gains predictive power only after 1271, with no pre-trend.
- An event-study of the market-access shock over 1102–1290 shows no pre-trend and a sharp, permanent break exactly at 1290, shortly after the relocation.

The market-access → population estimates are further identified via an IV strategy using the same "optimal route to capital" instrument, weighted by variables fixed well before the outcome period (Tang-era population, or a pre-1500 Caloric Suitability Index). **[empirical]** First-stage F-statistics exceed 100 across specifications — an unusually clean instrument by this literature's standards.

## Key finding: decomposing value creation from misallocation

The paper's structural contribution is separating two questions that are normally conflated: was the infrastructure worth building at all, and was it built in the right place. **[model]** Using a spatial-equilibrium structural counterfactual (Eaton–Kortum / Donaldson–Hornbeck-style, calibrated with land/labor income shares α=0.4, γ=0.55 taken from external historical-China estimates), the authors find:

- Removing the canal entirely would have cost 2.5–6.1% of aggregate population — the canal's net aggregate value, despite its political route.
- Replacing the actual politically-chosen route with a market-optimal one would have added back 1.1–2.2% of aggregate population — the pure cost of political redesign, roughly a third to a half of the canal's own potential gain.

This is the paper's central move: a politically-motivated institution/investment can be simultaneously net-positive *and* substantially misallocated. Political motive does not have to make an intervention net-harmful to still impose a real, measurable efficiency tax on top of its benefit.

**[model]** The authors caveat their own structural numbers: income shares are calibrated rather than estimated, and unobserved grid productivity is backed out under an assumed labor-mobility regime the paper itself flags as imperfect. They also show that naive reduced-form (partial-equilibrium) projections systematically overstate the cost of losing the canal relative to the full general-equilibrium treatment (e.g., 9.26% vs. 5.47% for a counterfactual removal in 741) — a general methodological lesson that partial-equilibrium estimates of politically-motivated infrastructure's cost will tend to overstate it relative to a full network-reallocation treatment.

## Lock-in and decay

**[model]** Once the Yuan set the Beijing–Hangzhou route, the Ming and Qing — different ruling houses, ~350 years later, with capitals that happened to also sit near Beijing — kept it essentially unchanged. Swapping the Yuan's own optimal route into Ming/Qing-era networks moves population by only 0.06–0.23%, i.e., near zero: the route had become locked in independent of any fresh political rationale, a quantified instance of infrastructure path-dependence outliving both the original actor and the original motive.

**[model]** The counterfactual value of the canal also decays over time for a reason distinct from institutional age itself: the loss from hypothetically dropping the canal runs ~5–6% of population Tang through Ming (741–1580) but falls to ~2.5% by the Qing (1776–1820), attributed to the rise of competing sea shipping — an exogenous technological substitute eroding a politically-locked asset's value, rather than decay driven by the infrastructure's own age.

## Bearing on institutions, power, and economic production

Decision rights over the canal's route sat entirely with the ruling house — the Yuan founders relocating the capital to their own steppe power base, later the Yongle Emperor relocating the Ming capital to his own northern power base — with no accountability mechanism beyond dynastic succession. **[wiki synthesis]** This is pure top-down discretionary power exercised by whoever controls the state, with infrastructure functioning as both an instrument of that power and a direct byproduct of its geographic base. The paper explicitly situates this as one case of a general pattern also documented in modern contexts (roads favoring a president's own ethnic region in Kenya; colonial railroads built for military rather than commercial logic) — politically-motivated siting is a recurring phenomenon, not unique to imperial China.

**[wiki synthesis]** For this wiki's institutions/power/economic-production framework, the paper supplies a rare *quantified* instance of a general claim this wiki otherwise holds mostly as theory: that political control over a resource-allocation decision imposes a measurable efficiency cost even when the underlying investment remains net-beneficial. It also complicates any empirical design (including horse-race studies) that treats "market access" or similar geography-based measures as an exogenous primitive — here it is shown to be endogenous to a political choice (capital siting) that varies historically and could in principle be politically motivated elsewhere too.

**Evidence tier note.** The reduced-form/placebo/event-study results (route-prediction regressions, market-access-to-population elasticities, the sign-flipping placebo tests, first-stage F-statistics) rest on data the authors actually analyzed and are marked **[empirical]**. The headline welfare decomposition (aggregate value, misallocation cost, lock-in counterfactuals, time-decay figures) comes from a calibrated structural spatial-equilibrium model with an admittedly imperfect labor-mobility assumption, and is marked **[model]** throughout.

## Source

- `raw/research/weekly-2026-09-08/01-politics-driven-market-access-grand-canal.md` — Bai, Bian & Jia, "Politics-driven Market Access and Its Cost: Evidence from China's Grand Canal," NBER Working Paper w35721, 2026. https://www.nber.org/papers/w35721

## Related

- [[institutions-vs-geography-vs-trade-horse-race]] — this paper shows that "market access," a workhorse geography-side control in institutions-vs-geography horse races, can itself be endogenous to a political decision (capital siting) rather than a purely exogenous geographic primitive, complicating any regression that treats it as such.
- [[rent-seeking-and-the-welfare-cost-of-transfers]] — Tullock's claim that political allocation imposes cost beyond the standard deadweight-loss triangle, and that he could suggest no way of measuring it; this paper is a rare real-world, quantified analogue — a directly measured political-redesign cost layered on top of a still-net-positive investment.
- [[developmental-state-and-embedded-autonomy]] — both concern concentrated political authority directing infrastructure/investment allocation; this paper's decomposition (the same political decision both created value and destroyed it) sharpens the "does state direction of the economy help or harm output" question that page carries.
- [[koreas-economic-planning-board]] — another case of concentrated state authority over investment/infrastructure decisions, disciplined (or not) by a different accountability structure than the dynastic succession that bounded the Yuan/Ming/Qing rulers.
- [[colonial-origins-and-the-settler-mortality-instrument]] — a methodological family resemblance: both exploit a historically fixed, plausibly exogenous variable to instrument a present-day outcome, though this paper's placebo tests (sign flips exactly at the 1271 political shock) identify a materially cleaner channel.
- [[de-jure-vs-de-facto-power-and-captured-democracy]] — a different register of power reshaping economic allocation (elite capture under democratization vs. dynastic infrastructure siting), only a loose thematic parallel but both concern how holders of power redirect resource allocation toward their own base.
- [[dimensions-of-institutional-variation]] — supplies a candidate general axis: whether an institution's resource-allocation decision rule is optimized for political control versus economic output, here demonstrated with a method for quantifying the gap between the two counterfactuals.
