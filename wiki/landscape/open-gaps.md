# Open Gaps

Where the 2025 corpus agrees the field is weak. These gaps shape what the expanded formulation method cannot reliably do today, and where extensions have to invest in infrastructure before they can deliver.

## The data gap is the root cause

Every AI-focused source in the corpus (Oz et al., Kuhl, Zhou et al., consortium) names the **lack of standardised multimodal datasets linking formulation → processing → rheology → sensory → nutrition** as the single biggest constraint. Kuhl: "data that correlate formulation to rheology, texture, and flavor are rare." Sensory panels cannot scale to deep-learning data volumes; in-line process logs sit in proprietary plant databases with inconsistent metadata; cross-company data sharing is blocked by commercial competition and privacy concerns.

Implication: any method expansion that depends on a learned surrogate is bottlenecked by labelled-data availability before it is bottlenecked by algorithm choice. Synthetic data, transfer learning, and active-learning sampling are the pragmatic workarounds.

## Model generalisation

Corpus-wide agreement that current predictive models "fail to generalise across new food matrices" (Oz et al.). A model trained on beverages will not transfer to baked goods; a rheology model trained on plant-protein–polysaccharide blends does not extrapolate to high-moisture extrusion products. Hybrid physics + ML is the usual proposed remedy; evaluating cross-matrix transferability should be part of any model-validation protocol. See [[predictive-models]].

## Bioavailability and digestion modelling

Oz et al. flags micronutrient bioavailability tools as "underdeveloped." Most substitution work optimises on the nutrient label and ignores matrix effects that determine what the body actually absorbs (see [[bioavailability-and-matrix-effects]]). Extending predictive scoring to bioavailability is technically hard (digestion is a multi-stage physiological process, microbiome-modulated) and data-starved.

## Explainability for regulated contexts

Black-box outputs are not acceptable in regulatory submissions, clinical claims, or traceable corporate decisions. Oz et al. and Zhou et al. both call out the explainability gap. Practical consequences: (a) predictive-model outputs need calibrated uncertainty and feature-attribution, (b) LLM outputs need human-written justification chains before they enter a submission, (c) agentic-AI discovery loops need audit trails.

## Cultural diversity in training data

Most sensory and recipe training corpora are Western-dominated. Oz et al. and the consortium paper both identify this as a generalisation hazard, not just a fairness concern — models trained on Western panels predict poorly for non-Western product categories and consumer bases. Building culturally diverse sensory data is hard because it requires distributed panel infrastructure.

## Real-time in-line process data

Oz et al. notes that predictive models "do not integrate real-time process parameters (shear rate, pH, thermal gradients)." Zhou et al. make this a central theme: new sensing and in-line monitoring tools are proposed as the route in, but deployment is early-stage. Digital twins coupling simulation with sensor feedback are the target architecture, mostly at pilot scale.

## Benchmarks and standards

The consortium paper and Zhou et al. both call for shared community benchmarks, open repositories, and domain-specific FAIR implementations. No food-specific benchmark comparable to what drug discovery or protein structure prediction have in their fields. Without standardised evaluation, method comparison is ad-hoc.

## Foundation models for food

Kuhl argues that multimodal foundation models pretrained on recipes, images, nutrition, sensory, and processing data would unlock a wave of inverse-design applications. Such models **do not yet exist** for food. The pre-training corpus would have to be assembled first, which circles back to the data gap.

## Ingredient variability

Zhou et al. highlight that "two batches of the same ingredient can behave very differently even when certificates of analysis report similar values" — particularly acute for plant proteins. Predictive models trained on a single batch will not match production reality. Adaptive recalibration against in-line measurements is the proposed response, but the measurement infrastructure and the calibration protocols are both immature.

## LLM-specific risks

The consortium paper is explicit:

- Off-the-shelf LLMs "perform unevenly across cultural contexts" and "often fail to capture diverse user preferences."
- They "lack molecular-level understanding of food and have limited knowledge of food safety."
- They can generate outputs that are "numerically inconsistent, unsafe, or infeasible."
- Hallucinated health claims risk undermining consumer trust and regulatory standing.

Practical treatment: LLMs belong in the *proposal* and *reasoning* roles, not in the final quantitative decision or the regulatory text.

## Preference elicitation on a Pareto front

The corpus is good on MOO methods but thin on how the customer actually *chooses* a point on the Pareto front. Recommender systems with sliders are the usual interface; no formalised preference-elicitation protocol is proposed. This is a genuinely open design problem for any hybrid method that intends to surface trade-offs rather than hide them. See [[multi-objective-optimization]].

## Scale-up and deployment

Zhou et al. and the consortium paper both emphasise that most AI-driven formulation systems have been demonstrated at pilot or lab scale; industrial deployment is limited by capital investment, workforce training, and validation on production lines. Digital twins in particular "have not been tested at scale" for most food categories.

## Implications for the expanded method

1. **Invest in data infrastructure before chasing model sophistication.** A rich ingredient graph with five-axis similarity, combined with a well-curated labelled (formulation, property) corpus, will do more than swapping a predictive model architecture.
2. **Plan for cross-matrix generalisation failures.** Track which product categories a model has been validated on; do not silently reuse across categories.
3. **Always emit calibrated uncertainty** from predictive scorers — needed for BO, for Pareto-aware selection, and for regulatory defensibility.
4. **Design the preference-elicitation interface early** — a Pareto-aware method with no way for the customer to pick a point is not operationally useful.
5. **Keep LLM outputs in proposal roles with audit trails**; do not let them produce final quantitative commitments.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — data, generalisation, bioavailability, explainability, cultural-diversity, real-time-process gaps
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — LLM risks, foundation-model proposal, benchmark gap, scale-up barriers
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — ingredient variability, in-line sensing, standards, privacy-preserving collaboration
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — multimodal dataset gap, foundation-model absence, sensory-data scarcity

## Related

- [[field-overview]]
- [[datasets-and-databases]]
- [[predictive-models]]
- [[ingredient-substitution]]
- [[multi-objective-optimization]]
- [[genai-leverage-points]]
- [[bioavailability-and-matrix-effects]]
