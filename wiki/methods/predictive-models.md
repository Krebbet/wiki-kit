# Predictive Models

The *scorer* side of a formulation pipeline: models that predict food properties from composition and process parameters. Essential input to both candidate evaluation and surrogate-based search. Organised by the property domain being predicted.

## Texture and rheology

Mechanical and flow properties (see [[rheology-and-texture]]) are the best-studied prediction target because instrumented measurement is comparatively cheap.

- **Random forests** (Dahl et al., cited in Oz et al.) on plant protein–polysaccharide blends predict both linear and nonlinear rheological properties (G', G", yield stress) reasonably accurately within a constrained chemical space.
- **Physics-informed neural networks** (PINNs) blend constitutive equations with data-driven fitting; more interpretable than plain networks when the mechanical theory is partially known.
- **Constitutive neural networks** (consortium paper) discover physics-based models from texture and rheology data in an automated way — useful for plant-based meat where the mechanical theory is still being built.
- **Autoencoders** predict sensory texture attributes from rheological measurements, giving a partial bridge from physical to sensory texture.
- **Support vector machines and neural networks** on mechanical-plus-acoustic signatures identify snack freshness with up to 92% accuracy (consortium paper).
- **Transfer learning** with pretrained vision backbones (VGGNet, ResNet, DenseNet) extends to cooking-time and texture prediction from images.

Limits named across the corpus: poor generalisation across food matrices; nonlinear mechanics (fracture, high-strain yield) missed; process parameters (shear, temperature, pH) rarely integrated.

## Flavour and aroma

- **Principal Odor Map** — a GNN trained on odorant–descriptor pairs, organising thousands of molecules in a perceptual embedding. Reported **human-level accuracy** on 400 unseen compounds, with predictions aligned to sensory panel averages more closely than the median panelist. Foundational for flavour-side candidate scoring.
- **Attention-based GNN variants** extend this to odorant *mixtures*, where volatiles interact non-linearly and trace-level compounds can dominate perception.

The unsolved problem: models trained on isolated compounds or simplified matrices generalise poorly to real food, where matrix components (lipids, proteins, carbohydrates) modulate aroma release.

## Nutrition and bioavailability

Covered thinly across the corpus. ML models exist for protein digestibility from amino-acid profiles, and AI image-recognition tools estimate nutrient intake from dish-level data. Oz et al.'s diagnosis: micronutrient bioavailability models "remain underdeveloped"; most approaches overlook matrix interactions, antinutritional factors, and postprandial metabolic outcomes. Training sets depend on well-characterised ingredients, limiting applicability to novel or composite substitutes. See [[bioavailability-and-matrix-effects]].

## Fermentation and bioprocess

- **Kinetic bioprocess models** — classical, physics-based, constrained by steady-state assumptions.
- **Flux-balance analysis** and metabolic flux models — face computational bottlenecks at industrial scale.
- **Machine learning** models nonlinear fermentation dynamics; reinforcement learning optimises co-culture conditions in bioreactors.
- **SVM, fuzzy inference, evolutionary algorithms** for prediction and adaptive control.

## Sensory (panel-level)

The corpus is cautious. LLMs trained on food-panel data claim (consortium paper, citation 98) to "match expert food scientists in predicting sensory panel rankings" — a strong claim context-dependent on category and metric, worth replicating before depending on. Feature-based ML on compositional inputs can predict overall acceptance within narrow product categories; cross-category generalisation is poor. See [[human-in-the-loop]] for why sensory validation is still a last-mile human task.

## Process outcome (e.g. extrusion)

PIPA / "Digital Extruder" (Zhou et al.) — proprietary — simulates thousands of formulations under extrusion to forecast structural and sensory outcomes before physical trials. Validation data not published; plausible given extrusion physics but unverified.

## Architecture patterns worth noting

- **Hybrid data-driven + physics-based models** are the recurring structural pattern (Zhou et al., consortium paper). Pure ML struggles with the matrix-dependence of food properties; pure physics misses the empirically important nonlinearities. Hybrid models trade some modelling effort for better sample efficiency and better extrapolation.
- **Multimodal inputs.** Force–deformation curves, images, spectroscopy, sensor logs, panel scores — all rich signals for food properties — arrive in different modalities. Foundation-model pre-training across modalities is proposed but no deployed food-specific model exists yet.
- **Ensemble over single models.** Food data is noisy and heterogeneous; ensemble methods (RF, gradient boosting, stacking) typically outperform single learners on tabular food-science tasks.

## Accuracy claims worth flagging

- **Principal Odor Map's "human-level accuracy"** — strong claim, repeated across sources, but the benchmarking is on isolated odorants, not matrix-embedded perception. Treat as a ceiling, not an operating point.
- **92% snack-freshness accuracy** (consortium paper, SVM + mechanical + acoustic) — narrow product class; cross-product generalisation untested.
- **LLMs matching expert food-scientist panel rankings** (consortium paper citation 98) — context unclear; worth direct replication before relying on in the pipeline.

## Limits the corpus agrees on

- Narrow training sets → poor cross-matrix generalisation.
- Real-time in-line process parameters rarely integrated.
- Sensory data cannot scale to deep-learning volumes without synthetic data or transfer learning.
- Explainability is lacking; regulated contexts push back on black-box outputs.
- Ingredient variability (plant-protein batch-to-batch differences) degrades prediction without adaptive recalibration.

## Implication for the expanded method

If the existing method uses property-specific predictive models, the priority upgrades suggested by the corpus are:

1. **Add GNN surrogates** for flavour/aroma scoring; the Principal Odor Map is public and a reasonable starting point.
2. **Adopt hybrid physics + ML** for rheology/texture where the constitutive theory is partial — constitutive neural networks or PINNs rather than pure deep nets.
3. **Integrate process parameters** explicitly in the input — not just ingredient vectors, but ingredient × process conditions.
4. **Track model uncertainty**, not just point estimates; Pareto-aware search with uncertain objectives needs calibrated uncertainty (a BO requirement).
5. **Plan for recalibration** against in-line sensor feedback once a candidate moves to pilot — the digital-twin pattern from the consortium paper.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — rheology RF, GNN flavour models, nutrition/bioavailability modelling gaps, explainability limits
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — constitutive neural networks, PINNs, SVM+acoustic, transfer learning, LLM-sensory parity claim, fermentation RL
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — PIPA/Digital Extruder, ingredient variability
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — network→property mapping, TPA-to-rheology relationship, inverse-design framing of prediction

## Related

- [[candidate-generation]]
- [[multi-objective-optimization]]
- [[inverse-design]]
- [[rheology-and-texture]]
- [[ingredient-functionality]]
- [[bioavailability-and-matrix-effects]]
- [[datasets-and-databases]]
- [[open-gaps]]
