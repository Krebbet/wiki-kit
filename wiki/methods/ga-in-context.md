# Genetic Algorithms in Context

The existing formulation method uses a genetic algorithm (GA) as its candidate generator. This page examines GA's footprint in the recent food-formulation literature, what the literature's alternatives are, and how to judge when to extend the GA, complement it, or migrate away. Treat most of what follows as *(editorial)* — it is a reasoned reading of a six-source survey, not a direct extraction from any one source.

## What the corpus actually says about GA

GA is **nearly absent by name** in the 2025 review corpus for food formulation. The one explicit reference in the consortium paper (arXiv 2509.21556) is to a *"Non-dominated Sorting Genetic Algorithm II"* used with Radial Basis Function neural networks to formulate a reduced-serum culture medium for cultivated-meat growth — a cell-culture problem, not a consumer-product formulation. GAs are also mentioned in passing for fermentation process optimisation. The Oz et al. review on AI-enabled ingredient substitution does **not** list GA among its method taxonomy (it lists Bayesian optimisation, Pareto methods, reinforcement learning, graph neural networks, and LLMs). Kuhl's Nature Perspective does not list GA.

Two readings are consistent with this absence:

- **GA has moved out of the food-specific literature** because BO-based approaches are more sample-efficient on the small evaluation budgets typical in food R&D, and generative models are more expressive for structured outputs. The reviews are reporting what researchers are publishing, not what practitioners are running.
- **GA is still widely used in industry**, but industrial users do not publish their pipelines, and the academic reviews therefore undersample it.

Both readings are probably partly true. Neither means GA is wrong.

## What GA is still well suited to

- **Large combinatorial search spaces** — ingredient selection from catalogues of thousands, multi-component recipes where the number of valid compositions is vast. GA's population-based exploration is natively built for this.
- **Mixed discrete-continuous encodings** — an ingredient list (discrete) combined with fractions (continuous) and process settings (continuous or discrete) maps cleanly to mixed chromosomes. BO often needs tricks to handle this.
- **Easy parallelism** — evaluating a population in parallel is straightforward; GA amortises well when the scorer is fast.
- **Robustness to noisy, non-differentiable objectives** — particularly when the scorer is a mix of ML surrogates and rule-based filters.
- **Multi-objective variants exist and are mature** — NSGA-II (explicitly referenced once in the corpus) and NSGA-III provide Pareto-aware selection with minimal additional machinery.
- **Explainability of the search trace** — generations and parent–child lineage are inspectable in a way a deep generative model's latent sampling is not.

## Where GA is dominated by alternatives

- **Small evaluation budgets with expensive evaluations.** If each candidate costs a pilot run or a sensory panel, BO-with-surrogate is more sample-efficient by a large margin.
- **Structured output spaces where priors matter.** If the corpus of known formulations carries important structural information (which ingredients tend to co-occur, which combinations are flavour-coherent), a generative model trained on that corpus proposes more plausible candidates than random crossover. This is the argument for VAEs, GANs, diffusion, and LLM-based generators.
- **Inverse design from target properties.** GA can do this by selecting fitness = distance-to-target, but conditioning a generative model directly on the target property is usually cleaner. See [[inverse-design]].
- **Soft-constraint reasoning.** Cultural, dietary, and regulatory constraints are easier to express in an LLM or ontology layer than as GA fitness penalties.

## An evaluation axis for "should we extend or replace?"

Practical questions to ask, framed as axes rather than answers:

1. **Sample budget per generation.** If evaluating a GA generation is cheap (fast surrogate), GA stays competitive. If each call is expensive, BO dominates.
2. **Dimensionality of the encoded formulation.** GA scales well to hundreds of dimensions with good encodings; BO gets hard above ~20 without structure.
3. **Need for candidate priors.** If "plausible formulations" are a meaningful concept in the domain, generative models will beat unconstrained GA search on plausibility.
4. **Constraint type.** Hard numeric constraints (cost ceilings, nutrient bands) are fine for GA. Soft semantic constraints ("kid-friendly snack", "Latin American flavour profile") favour LLM-assisted generation.
5. **Multi-objective structure.** If trade-offs between cost, sensory, nutrition, and function are first-class, Pareto-aware methods (NSGA-II or Pareto BO) dominate weighted-sum GA.
6. **Cost of the surrogate.** If the predictive model is mature, accurate, and fast, the GA's expensive-evaluation argument weakens — BO's advantage shrinks and generative-model expressiveness becomes more attractive.
7. **Explainability.** If stakeholders need to understand *why* a candidate was produced, GA's lineage trace is a real asset. Latent-space decoding is harder to narrate.

## Editorial read on the method direction

The most likely useful path for the existing method is not *replace GA* but *flank it*:

- Keep the GA as the core combinatorial engine for multi-ingredient search.
- Add **LLM-assisted proposal** as a parallel generator for the ingredient-substitution problem class — the user's "cheaper peanut-oil replacement" pattern — because substitution is a soft-constraint reasoning problem where LLM + ontology plays to strengths.
- Add **generative models (VAE or diffusion)** as a second parallel generator when the customer brief is under-specified and the goal is novel formulations rather than replacements.
- Route candidates from all three generators into a **shared Pareto-aware selector** (see [[multi-objective-optimization]]) backed by a richer predictive model stack ([[predictive-models]]).
- Keep **scenario/decision-tree** reasoning from the CIM (see [[npd-process]]) as a sanity layer for chain-wide feasibility that neither GA nor LLM captures well.

This is a hybrid architecture, not a migration. The fitness function doesn't change; the candidate supply diversifies.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — method taxonomy conspicuously omitting GA
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — NSGA-II reference (cultivated-meat medium); GA cited for fermentation
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — VAE, GAN, foundation-model framing as alternatives

All claims outside the direct attributions above are *(editorial)*.

## Related

- [[candidate-generation]]
- [[multi-objective-optimization]]
- [[ingredient-substitution]]
- [[inverse-design]]
- [[predictive-models]]
- [[genai-leverage-points]]
