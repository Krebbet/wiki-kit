# Multi-Objective Optimization

Why food formulation — and ingredient substitution in particular — is *inherently* a multi-objective optimisation (MOO) problem, and what the corpus says about handling the trade-off space.

## Why MOO is the right abstraction

The objectives that a formulation has to satisfy simultaneously are not commensurable. A typical customer brief involves some combination of:

- **Sensory quality** (taste, aroma, texture match to a target or reference product).
- **Functional performance** (emulsion stability, viscosity profile, gelation behaviour under expected process conditions — see [[ingredient-functionality]]).
- **Nutritional profile** (macronutrient targets, micronutrient content, bioavailability — see [[bioavailability-and-matrix-effects]]).
- **Cost** (per unit product, at target scale).
- **Regulatory compliance** (allergen labelling, additive approvals in target markets, certification eligibility).
- **Cultural and dietary compatibility** (Halal, Kosher, organic, non-GMO, clean-label, specific diet).
- **Sustainability / environmental impact** (LCA metrics — carbon footprint, water, biodiversity; often region-dependent).

Scalarising these into a single weighted sum is usually the wrong move. The weights are typically unknown to the customer at the start of the engagement; the trade-offs are what they want to *see*, not what they already know how to balance. Oz et al. make this explicit: substitution rarely has a one-to-one analogue and requires compensatory adjustments, "often to balance multiple competing objectives."

## Methods cited for handling the trade-off space

- **Pareto optimisation.** The dominant framing in the ingredient-substitution review (Oz et al.) and the arXiv consortium paper. Instead of picking one candidate, compute and present the Pareto front of non-dominated candidates; let the human (or a preference-elicitation step) choose the operating point. NSGA-II is the named implementation in the consortium paper's cultivated-meat-medium example.
- **Bayesian optimisation with Pareto acquisition.** Multi-objective BO variants (ParEGO, PESMO, NEHVI) pick the next candidate by expected improvement over the current front. Sample-efficient when evaluations are expensive (pilot runs, sensory panels). Oz et al. list BO as a core method.
- **Reinforcement learning with multi-reward shaping.** Oz et al. cite RL for iterative substitution; rewards can reflect multiple axes, though reward shaping is subtle.
- **Fuzzy logic and Bayesian inference** over probabilistic module outputs. Oz et al.'s proposed framework has each module produce probabilistic scores (flavour, function, nutrition, culture, regulation) and uses fuzzy / Bayesian combination to negotiate conflicts.
- **Ontology- and rule-based filtering** as a *constraint* layer rather than an objective. Certification requirements, allergen exclusions, and regional regulatory approvals are usually hard constraints; ontology-aware filters prune the Pareto front to feasible candidates.
- **Scalarisation with LCA weights.** Asadollahi et al.'s MOO-LCA framework (cited by Oz et al.) balances environmental impacts, cost, and functional properties with explicit scalarisation. Miranda-Ackerman and Azzaro-Pantel apply carbon-labeling and organic-content thresholds within a MOO formulation.

## Preference elicitation

The corpus does **not** engage deeply with how a human picks a point on the Pareto front. Oz et al. flag "recommender systems with dietary, sensory, economic, and cultural constraints" as the interface — effectively letting the user set constraint bounds and drop non-satisfying candidates. Digital-twin and feedback-loop interfaces (consortium paper; see [[human-in-the-loop]]) support iterative refinement but don't formalise preference elicitation. This is a real gap; practitioners often fall back on weighted sums or interactive sliders that undersell the trade-off structure. See [[open-gaps]].

## Constraint modelling

Distinguish hard from soft constraints at the design stage:

- **Hard:** cost ceiling, allergen absence, certification eligibility, regional regulatory approval. Treat as feasibility filters — infeasible candidates should not enter the Pareto set.
- **Soft:** sensory target match, sustainability preference, cultural compatibility scores. Treat as objectives on the Pareto front.

A common mistake in the literature (implicit) is pushing soft constraints into hard filters (e.g. "sensory score > 0.8") or vice versa (scoring cost as an objective when the customer has a firm ceiling). The framing choice changes which candidates the method surfaces.

## Implication for the expanded method

If the existing method uses a weighted-sum fitness, migrating to a Pareto-aware selector (e.g. NSGA-II if the GA backbone stays, or Pareto BO if the BO path opens) is likely higher-leverage than replacing the candidate generator. Two practical moves:

1. **Split objectives from constraints explicitly** in the fitness spec. Allergen and regulatory filters are not weights.
2. **Report the Pareto front, not the winner.** The customer wants to see the trade-offs; the weighted-sum winner hides the information they care about most.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — Pareto, BO, RL, fuzzy logic, ontology filters, MOO-LCA, carbon-thresholded MOO; multi-objective framing of substitution
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — NSGA-II (cultivated-meat medium example), Pareto-aware BO in active learning loops
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — multivariable optimisation framing

## Related

- [[candidate-generation]]
- [[ga-in-context]]
- [[ingredient-substitution]]
- [[predictive-models]]
- [[human-in-the-loop]]
- [[open-gaps]]
