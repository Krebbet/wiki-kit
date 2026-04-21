# Ingredient Substitution

The "cheaper peanut-oil replacement" problem class, treated rigorously. Drawn primarily from Oz et al.'s 2025 review (*Foods*), which is the deepest treatment in the corpus.

## The problem, as the literature frames it

Substitution is the replacement of one or more components in a formulation while preserving sensory quality, technological functionality, nutritional value, and cultural/dietary compatibility. The core difficulty Oz et al. identifies: substitution **rarely has a one-to-one analogue** and almost always requires compensatory adjustments — swap peanut oil for sunflower, and you may need to adjust an emulsifier, retune the process temperature, and check that the flavour carriers still behave.

Problem classes in the literature:

- **Cost-driven** — replacing a price-volatile or expensive ingredient (the user's peanut-oil case).
- **Supply-driven** — replacing a disrupted ingredient (seasonality, geopolitical supply shocks).
- **Allergen-driven** — removing a top allergen (gluten, dairy, egg, peanut, tree nut, soy) while preserving function.
- **Nutrition-driven** — reducing sugar / sodium / saturated fat; increasing protein / fibre.
- **Sustainability-driven** — animal-to-plant protein swaps; high-impact to low-impact oils.
- **Cultural / regulatory** — achieving Halal/Kosher/organic/clean-label eligibility; regional additive approvals.

Outcomes are non-linear and matrix-dependent. Oz et al.: "even subtle compositional changes can have disproportionate sensory effects." Practitioners typically run empirical, iterative trial-and-error loops that "struggle to optimize multiple competing objectives."

## What makes substitution multidimensional

Oz et al. argue — and this is the paper's central reframing — that substitution is not a single-axis similarity problem; a valid substitute must match the reference simultaneously along five axes:

1. **Flavour compatibility** — taste and aroma profiles, including the non-linear interactions between trace volatiles and matrix components. Substitution at the dominant compound usually fails unless the supporting volatile profile is reconstructed.
2. **Technological functionality** — the ingredient's role in structure, emulsification, gelation, water binding, viscosity, gas retention. A plant-protein substitute for casein may score well on nutrition but catastrophically fail on gel formation in a cheese analogue.
3. **Nutritional equivalence and bioavailability** — not just "same nutrient quantity" but "same absorbed nutrient," accounting for matrix effects (see [[bioavailability-and-matrix-effects]]) and antinutritional factors.
4. **Cultural, religious, and regulatory constraints** — ingredient eligibility for Halal/Kosher, allergen-labelling rules, certification requirements, regional additive bans.
5. **Cost and sustainability** — per-unit price at target scale, plus LCA indicators (carbon, water, biodiversity) that may be soft or hard constraints depending on customer framing.

Each of these can be quantified or at least rule-filtered; the hard part is that a candidate can only be judged after all five are evaluated and trade-offs are explicit. This is precisely the case for Pareto-aware MOO — see [[multi-objective-optimization]].

## Data required

Oz et al. and the supporting consortium paper converge on this shopping list:

- **Ingredient composition** — proximate analysis, molecular descriptors, volatile-compound profile.
- **Sensory panels** — labelled taste/aroma/texture scores per ingredient and reference product.
- **Functional measurements** — viscosity, elasticity, yield stress, emulsification capacity, gel strength, water-holding capacity, phase behaviour. Ideally under the processing conditions the target product will see.
- **Process conditions** — temperature, pH, ionic strength, shear rate, thermal history.
- **Nutritional data** — amino-acid profile, macronutrient composition, micronutrient forms, digestibility, bioavailability (underdeveloped in current tools).
- **Cultural / regulatory metadata** — taxonomies, certification schemes, allergen registries, regional approvals.
- **Cost and LCA** — price per unit at relevant sourcing, environmental-impact indicators (region-specific LCA databases named as a recognised limitation).

See [[datasets-and-databases]] for what is publicly available; see [[open-gaps]] for what is not.

## Methods for producing substitute candidates

The methods taxonomy from Oz et al., with brief notes on fit:

- **Graph-based similarity search.** Ingredients as nodes in a heterogeneous graph, edges weighted by chemical, sensory, co-occurrence, nutritional, and cultural similarity. Substitution = graph query for similar nodes on the required axes. Clean baseline; natural home for GNN embeddings. See [[ingredient-data-structures]].
- **Graph neural network property prediction.** Principal Odor Map (GNN trained on odorant–descriptor pairs) for flavour-side scoring. Claimed human-level accuracy on unseen compounds; contested whether this holds in real food matrices.
- **LLM-based reasoning.** BERT/GPT extract ingredient–function–sensory relationships from recipes, reviews, labels; cultural and dietary reasoning runs as soft-constraint filtering. NotCo's Giuseppe and Generative Aroma Transformer are named deployments.
- **Bayesian optimisation.** Sample-efficient search over the substitute candidate space when each evaluation (panel, pilot) is expensive.
- **Reinforcement learning.** Iterative refinement in feedback-loop settings.
- **Ontology-based rule engines.** Enforce certification / allergen / regional regulatory compliance as hard filters. Plant Jammer is the named platform; the pattern is widely applicable.
- **Multi-objective optimisation as the integrator.** Pareto / fuzzy / Bayesian combination of per-axis scores. See [[multi-objective-optimization]].

## Concrete industry examples

- **NotCo** — plant-based dairy (NotMilk from pineapple juice, cabbage juice, pea protein; NotChicken from a tomato-strawberry pairing). Pipeline uses latent-space candidate generation with expert sensory feedback per iteration.
- **Climax Foods, Perfect Day, Meati** — plant/precision-fermentation cheese and ice-cream analogues; AI-aided ingredient mining.
- **Plant Jammer** — formulation environment letting manufacturers prioritise Halal-certified texturisers, exclude allergens, cap carbon footprint — constraints as first-class inputs.
- **Brightseed (Forager)** — discovery of bioactive compounds (N-trans-caffeoyltyramine, N-trans-feruloyltyramine) from analysis of ~700,000 phytochemicals.
- **Live Green Co (Charaka)** — knowledge-integrated substitution drawing on traditional/ancestral plant knowledge at scale.

## Where the field agrees it is weak

- **Real-world processing variation** — most substitution models assume steady-state conditions; production floors vary in shear, temperature, and residence time. Models rarely incorporate in-line process parameters.
- **Micronutrient bioavailability** — tools are "underdeveloped"; substitutes can match nutrient labels while failing to deliver the absorbed effect.
- **Cross-matrix generalisation** — a model trained on beverages fails on baked goods and vice versa.
- **Culturally diverse sensory data** — most labelled sensory corpora are Western.
- **Explainability for regulatory review** — black-box models limit adoption in regulated submissions.

## Implication for the expanded method

The user's existing method already does ingredient-level optimisation. The substitution-specific leverage points from the corpus:

1. **Add a substitution-query mode** distinct from new-formulation search. Substitution has a *reference product* and a *change budget*; framing the search as "minimal deviation satisfying target constraints" is different from unconstrained optimisation.
2. **Encode the five-axis structure** (flavour, function, nutrition, culture/regulation, cost/sustainability) as the Pareto axes. Avoid collapsing to a weighted sum.
3. **Use an ingredient graph** with multiple typed edges as the substitution backbone (see [[ingredient-data-structures]]).
4. **Add a constraint/ontology layer** for certification, allergen, and regional regulatory filtering — before predictive scoring, to avoid wasted evaluation budget.
5. **Use LLM-assisted proposal** for soft-constraint substitution queries where the customer brief is under-specified (*"a cheaper peanut-oil replacement that keeps a kid-friendly profile"*) — the LLM handles the cultural/functional intent, the GA or BO handles the fine-grained search.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — primary source; entire page structure tracks this review
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — NotCo deployment detail, graph and GNN methods, in-line processing gaps
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — ingredient variability challenge, plant-protein batch-to-batch variation
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — NotCo case studies, Brightseed, FoodProX-style degree-of-processing classifiers, LLM-based substitution

## Related

- [[candidate-generation]]
- [[multi-objective-optimization]]
- [[ingredient-data-structures]]
- [[ingredient-functionality]]
- [[bioavailability-and-matrix-effects]]
- [[predictive-models]]
- [[genai-leverage-points]]
- [[industry-examples]]
- [[open-gaps]]
