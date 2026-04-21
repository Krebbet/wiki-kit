# Inverse Design

Kuhl's framing (2025 Nature Perspective) makes this explicit: instead of predicting the property *given* the formulation, treat the target property as the input and generate the formulation and process parameters as the output. The forward-prediction loop becomes a design loop.

## The framing

Traditional forward prediction: *formulation → model → predicted property.*

Inverse design: *target property → model → candidate formulation (+ process).*

The practical value is that customer briefs arrive as targets, not as inputs. "A peanut-oil replacement at 30% lower cost that keeps the sensory profile within a tolerance" is a target specification, not a starting point. An inverse-design method produces the formulation rather than asking a forward model to score a human-proposed one.

## How the corpus proposes to implement it

- **Conditional generative models** — VAEs and diffusion models conditioned on target-property vectors. The VAE decoder or diffusion reverse process produces candidate formulations consistent with the conditioning. Named in Kuhl (VAE); cited by the consortium paper for *de novo* protein design in alternative-meat contexts (diffusion).
- **Text-to-formulation LLMs.** Natural-language prompts encode target intent ("cherry, candy, vanilla" for a flavour), the LLM generates molecular or ingredient-level proposals. NotCo's **Generative Aroma Transformer** is the named exemplar — the input is a textual flavour profile, the output a novel flavour molecule or ingredient recipe.
- **Optimisation over a learned surrogate.** Train a forward predictive model (see [[predictive-models]]); then search the formulation space — by GA, BO, or gradient-based methods if the surrogate is differentiable — to minimise distance to the target property vector. This is the pragmatic route when the predictive model already exists and the generative-model route is premature.
- **Foundation-model framing** (Kuhl). A multimodal transformer pre-trained on recipes, images, nutrition tables, sensory labels, and processing data would let fine-tuning produce inverse-design heads for specific target properties. No such foundation model exists for food yet — Kuhl calls its creation a priority.

## Why it is hard in food

- **Many-to-one property maps.** Multiple formulations can hit the same target profile; which one the model returns is not controlled by the objective alone. Priors (cost ceiling, "prefer plant proteins", "avoid soy") have to enter the conditioning.
- **Matrix dependence.** Same ingredient at the same fraction produces different properties in different matrices (see [[bioavailability-and-matrix-effects]]). Inverse design that ignores the target matrix will propose feasible-looking but actually non-performing candidates.
- **Infeasible proposals.** Generative models happily emit ingredient combinations that are regulatorily banned, culturally inappropriate, or physically unstable. A constraint/ontology filter layer (see [[multi-objective-optimization]]) is essential downstream.
- **Data scarcity.** Training a useful conditional generator requires many (formulation, property) pairs labelled across multiple property axes. This is exactly the dataset the corpus says does not yet exist at scale.

## Current deployment

NotCo's pipeline is the most-cited real deployment of inverse design in a consumer food product — Giuseppe proposes candidates conditioned on a target reference (e.g. cow's milk) and iterates with expert sensory feedback. Brightseed's discovery of bioactive compounds via analysis of ~700,000 phytochemicals is an inverse-design-adjacent pattern (target bioactivity → compounds → source ingredients). No general-purpose inverse-design tool for food formulation is publicly available.

## Implication for the expanded method

Inverse design is a natural *extension*, not a replacement, of a GA + predictive-model pipeline. Two ways to approach it from the existing method:

1. **Use the existing predictive models as the surrogate for optimisation-driven inverse design.** Frame the customer brief as a target-property vector; run GA / BO to minimise distance, subject to cost and regulatory constraints. Requires no new models — just a reframing of the fitness function and the interface.
2. **Add a conditional generator** as a second proposal stream in the hybrid architecture sketched in [[ga-in-context]]. When the brief is under-specified or novel (no close reference product), the generator gives candidates that random GA crossover would take many generations to reach.

The foundation-model approach (Kuhl) is useful to track but not actionable in the short term without a pre-training corpus that does not yet exist.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — latent-space substitution; inverse search over ingredient embeddings
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — diffusion for de novo protein design; conditional generation in NotCo pipelines; multi-agent agentic loops for inverse exploration
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — primary source for the inverse-design framing; VAE / GAN / foundation-model architectures; NotCo Generative Aroma Transformer; Brightseed Forager

## Related

- [[candidate-generation]]
- [[genai-leverage-points]]
- [[predictive-models]]
- [[multi-objective-optimization]]
- [[ingredient-substitution]]
- [[industry-examples]]
