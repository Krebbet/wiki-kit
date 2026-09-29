# The Allocative Cost of War (Ukraine)

Amann, Gorodnichenko & Talavera (IZA DP 18895, Aug 2026) use near-census Ukrainian firm data to argue that the 2022 invasion cut allocative productivity by roughly 20-40% because labour and capital were misallocated across surviving firms, and that this accounts for about half of the wartime output loss. The wiki's interest is narrow: it is a quantified case in which an economy's allocation system, not its factor stock, is the binding constraint under stress, with a firm-size gradient whose sign flips with the type of shock. It is an un-refereed working paper, and every institutional or policy explanation in it is conjecture.

**Evidence tier note.** (a) for the descriptive core only: an un-refereed IZA working paper, self-described as "preliminary... not definitive". The Hsieh-Klenow misallocation measure, the raion-level dose-response and the peer-country comparison are measured; the growth accounting is back-of-envelope; the mechanisms and all policy claims are (b) or (c), and the authors themselves say the policy section is "not directly studied in the paper". Not an institution-level study: the state appears only as a background actor.

## What was measured

**[empirical]** Balanced firm panel 2018-2024 from ORBIS (about 55.8% of 2021 business-entity workers retained; utilities, public administration, defence and firms in occupied raions excluded), aggregated to sector by raion (district) and to the national economy, benchmarked against neighbouring Eastern European countries cleaned the same way. Allocative TFP is measured as dispersion of marginal revenue products of capital and labour (Hsieh-Klenow).

- Allocative TFP fell roughly 20-40% (depending on weighting); a 1 SD rise in raion war intensity (geocoded event data, VIINA, built from news text) is associated with an 11pp larger TFP decline, and war intensity explains over 60% of cross-raion variation.
- Growth accounting attributes roughly half the wartime output loss to misallocation; about $59bn of private-sector value added lost 2022-24 (about 44% of 2021 net output of the sample sectors). The authors say this decomposition had not been documented before.
- Adaptation: the economy was +8.1pp more efficient than a fixed-weight counterfactual by 2024 (+0.9pp in 2022, +6.5pp in 2023); 55-58% of the gain came from reallocation within raion, 22-25% between raions, about 20% between industries.
- Liberated raions show no permanent scar once ongoing attacks are controlled.

## Shock type changes the firm-size gradient

**[empirical]** The paper compares three episodes in the same country. In 2022 (kinetic shock) the smallest firms lost most and larger firms fared better. In 2014 (Crimea/Donbas) and 2008-09 (financial crisis) the largest firms were hit most, through banking integration and a macro-financial channel; 2014 showed a shallow geographic gradient, the financial crisis a "slow burn" to a 2011 trough (about -20% allocative TFP) and no geographic gradient. So the size effect is not a stable property of scale; it depends on which shock arrives. This is the page's most reusable finding for the wiki's scale questions, but it rests on one country and three episodes.

## What is conjecture

- **[model]** Why large firms did better in 2022 (internal capital markets, credit access, "political connections that provide priority access to scarce resources such as electricity") is explicitly a conjecture.
- **[model]** Mobilisation and displacement as drivers are inferred from sectoral patterns (for example construction), not separately identified. The authors' own caveats: TFP-as-MRP-dispersion conflates any wedge (markups, adjustment costs, regulation) with "misallocation"; ORBIS geocodes relocated firms at their final address; micro firms are under-represented; attack intensity is not randomly assigned; employment series come from ILO estimates because Ukrstat published none.
- **[model]** The policy list (housing support and remote-work facilitation for displaced workers, credit guarantees and war insurance, permit expediting, air defence, decentralised decision-making and distributed energy, pre-conflict labour-market flexibility and financial depth) is inferred from the decomposition, not tested. The "centralised, single-point-of-failure systems amplify damage" claim is asserted, not studied.

## Bearing on the wiki

**[wiki synthesis]** Three modest readings. (1) It is a measured, if contested, instance of frictions in reallocation (intermediation collapse, permits, search) raising the cost of moving resources, which is the [[transaction-costs]] mechanism seen under stress rather than in steady state. (2) The no-scar result for liberated raions is a short-window regional datapoint against lock-in after an exogenous shock; it does not contradict [[path-dependence-and-increasing-returns]], whose mechanism concerns institutional form, not firm allocation, and the window here is two to three years. (3) The decentralisation and single-point-of-failure argument sits next to [[polycentric-governance]] and [[hierarchy-and-near-decomposability]] but adds no evidence for either. It also notes, in passing, that Ukrainian statistical and registry institutions "continued to function", which is what made the study possible.

Candidate register axes (not added to the register this run; would be `candidate, not scoreable`, sourced only to this paper's assertions): reallocation flexibility under stress, and centralisation of critical infrastructure or authority as a single point of failure.

**Camp note.** Mainstream neoclassical framing (equal marginal products as the benchmark, market frictions as the problem, deregulation and financial deepening as remedies); openly value-laden and pro-Ukraine in tone; academic affiliations (IfW Kiel, UC Berkeley, Birmingham).

## Scope

Ukraine, one war, plus two comparison episodes in the same country; a large diversified economy with functioning statistical institutions. Public sector, utilities, defence and occupied areas are excluded, so nothing here concerns state-owned versus private allocative efficiency. External validity to other wars or to peacetime institutional stress is asserted ("countries that face security threats"), not shown. The recovery result holds only after ongoing attacks are controlled.

## Source

- `raw/research/weekly-2026-09-29/01-allocative-cost-of-war.md` — Amann, Gorodnichenko & Talavera, "The Allocative Cost of War: A View to a Kill...ing of Productivity," IZA Discussion Paper 18895, August 2026. https://docs.iza.org/dp18895.pdf (open-access mirror of the CEPR version that was capture-blocked on the 2026-09-15 sweep).
- Derived summary: `raw/research/weekly-2026-09-29/.ingest/01-allocative-cost-of-war.summary.md`.

## Related

- [[transaction-costs]] — reallocation frictions as transaction-cost-type barriers, here quantified under stress.
- [[path-dependence-and-increasing-returns]] — the no-permanent-scar result is a short-window, regional counterpoint to lock-in claims; scope-limited.
- [[polycentric-governance]] — the untested decentralisation argument is adjacent to Ostrom's nesting and polycentricity.
- [[hierarchy-and-near-decomposability]] — single-point-of-failure versus decentralised architecture echoes near-decomposability, asserted only.
- [[state-capacity-and-level-of-government]] — sub-national variation and state function under attack; the registry capacity that enabled the data.
- [[fast-and-slow-moving-institutions]] — the +0.9 / +6.5 / +8.1pp adaptation path is a small datapoint on adjustment speed.
- [[dimensions-of-institutional-variation]] — source of the two candidate axes noted above.
