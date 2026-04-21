# Field Overview

Where computational food formulation sits in 2025, based on six survey-grade sources (two Nature-family perspectives, two arXiv consortium surveys, a peer-reviewed review on ingredient substitution, and one older Wageningen monograph for historical baseline). This is the orientation page — entry point for someone opening the wiki cold.

## The field is in a transition

The older baseline (Benner's Wageningen thesis, 2004) describes food product development as an empirical, chain-wide, expert-driven process: stage-gate phases, Quality Dependence Diagrams, Information Matrices, scenario enumeration, human judgement on feasibility. See [[npd-process]]. Candidate generation is manual; predictive modelling is qualitative.

The four 2025 sources (Oz et al. on AI-enabled ingredient substitution; Zhou et al. on AI for food manufacturing; Kuhl on AI for food; the AI-for-Sustainable-Food-Futures consortium) describe a different field: data-driven design, predictive ML surrogates, generative candidate proposers, LLM-assisted substitution, inverse design, multi-agent discovery loops. All four sources argue that traditional development is "slow, empirical, and fragmented" and position AI as the inflection. The fifth 2025 source (IUFoST) works a different axis — classification and definitional hygiene for formulation-vs-processing (see [[food-classification-schemes]]) — but shares the push toward quantified, measurable frameworks.

The transition is real but uneven. The algorithms exist; the data does not.

## The common thesis across 2025 sources

1. **Ingredient substitution is the most tractable AI-leveraged problem.** The reference product gives a target; the change budget gives a constraint; the five-axis match (flavour, function, nutrition, culture/regulation, cost) maps cleanly to multi-objective optimisation. See [[ingredient-substitution]] and [[multi-objective-optimization]].
2. **Data, not algorithms, is the bottleneck.** The missing asset is standardised multimodal datasets linking formulation → processing → rheology → sensory → nutrition. Sensory panels cannot produce ML-scale labels. See [[datasets-and-databases]] and [[open-gaps]].
3. **Inverse design is the stated frontier.** Target property → formulation, via conditional generative models or optimisation over predictive surrogates. No general-purpose inverse-design tool for food formulation is public yet. See [[inverse-design]].
4. **LLMs are the near-term leverage.** Literature mining, substitution reasoning, feedback translation, formulation copilots. Limits are real (cultural unevenness, no molecular grounding, hallucination) but the low-hanging fruit is high. See [[genai-leverage-points]].
5. **Human-in-the-loop is still unavoidable at key steps.** Sensory validation, regulatory and cultural review, process-scale calibration. See [[human-in-the-loop]].

## Method landscape

Candidate generation is pluralising. The method classes in active use or proposal: genetic algorithms (historically dominant, now thin in recent literature), Bayesian optimisation (the current default for sample-efficient search), generative models (VAE, GAN, diffusion) for inverse design, graph neural networks for property-aware proposal, LLMs for soft-constraint reasoning, ontology-based rule engines for hard-constraint filtering, reinforcement learning for feedback-loop settings. Real pipelines combine classes. See [[candidate-generation]] and [[ga-in-context]].

Predictive models cluster around property domains — texture and rheology (best-developed), flavour and aroma (Principal Odor Map and successors), fermentation / bioprocess, nutrition (weakest), sensory (hard, human-panel-anchored). Hybrid physics + ML is the recurring architectural pattern. See [[predictive-models]].

Ingredient representation is converging on heterogeneous graphs with multi-relation edges (chemical, sensory, co-occurrence, nutritional, cultural) and functional-role taxonomies. See [[ingredient-data-structures]].

## Where the user's method sits

The existing formulation pipeline (GA + predictive models, HITL-heavy, with historical-product and pricing data) sits squarely inside the empirical-to-AI transition the corpus describes. The corpus suggests that replacement is not the right frame — extension is. Specifically:

- The **GA backbone** is under-represented in recent literature but remains well-suited to combinatorial ingredient search. See [[ga-in-context]] for when to extend it vs. flank it with alternatives.
- The **predictive-model stack** can be deepened with GNN surrogates (flavour), hybrid physics+ML (rheology), and explicit process-parameter integration. See [[predictive-models]].
- The **evaluation/selection step** can migrate from weighted-sum to Pareto-aware, exposing trade-offs rather than hiding them. See [[multi-objective-optimization]].
- **LLM-assisted substitution** is a high-leverage addition for under-specified customer briefs and cultural/regulatory reasoning.
- **Inverse-design framing** reframes the customer brief itself as a target-property vector and aligns the fitness function accordingly.

## Reading order

If the reader is new:

1. **[[npd-process]]** — organisational baseline.
2. **[[ingredient-substitution]]** — the core problem class.
3. **[[candidate-generation]]** and **[[ga-in-context]]** — generator side.
4. **[[predictive-models]]** and **[[multi-objective-optimization]]** — scorer and selector.
5. **[[inverse-design]]** and **[[genai-leverage-points]]** — extension directions.
6. **[[ingredient-data-structures]]** and **[[datasets-and-databases]]** — data substrate.
7. **[[open-gaps]]** — where the field agrees it is weak.

Food-science reference pages ([[rheology-and-texture]], [[ingredient-functionality]], [[bioavailability-and-matrix-effects]], [[food-classification-schemes]]) are for definition lookups, not linear reading.

## Source

All six captured sources contribute to this overview; per-claim attribution lives on the downstream pages. Raw files:

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md`
- `raw/research/formulation-landscape/03-iufost-formulation-classification.md`
- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md`
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md`
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md`
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md`

## Related

- [[npd-process]]
- [[ingredient-substitution]]
- [[candidate-generation]]
- [[ga-in-context]]
- [[predictive-models]]
- [[multi-objective-optimization]]
- [[inverse-design]]
- [[genai-leverage-points]]
- [[human-in-the-loop]]
- [[ingredient-data-structures]]
- [[datasets-and-databases]]
- [[industry-examples]]
- [[open-gaps]]
- [[food-classification-schemes]]
