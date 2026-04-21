# Candidate Generation

Methods for producing candidate formulations — the *proposal* step in any formulation-design pipeline, before evaluation and selection. This page surveys the method classes present in the corpus, their search spaces, and what each is best at.

A "candidate" here is a formulation: a weighted list of ingredients (with optional process parameters) aimed at meeting target properties. The choice of candidate-generation method determines three things: the shape of the search space, the sample efficiency of the search, and the kinds of constraints the proposer can respect natively.

## Method classes in the corpus

### Manual / scenario-based

The Wageningen CIM (see [[npd-process]]) is the canonical example: for each chain actor, expert teams enumerate feasible options in a decision tree; combinations of per-actor choices become scenarios; the NPD team picks the best by economic and technological feasibility. *Strength:* respects tacit knowledge and chain-wide interdependencies. *Weakness:* combinatorially limited — scales only as far as the expert team can enumerate. Benner himself flags this as the step most amenable to automation.

### Genetic algorithms

A working method class in industry but near-absent in the recent review corpus. The only explicit mention is the consortium paper (arXiv 2509.21556) citing GAs for *fermentation* parameter optimisation. See [[ga-in-context]] for detail on why GA's representation in the literature has thinned and where it still fits.

### Bayesian optimisation

Treated as the go-to method for multi-objective substitution in the Oz et al. review. Fits well when evaluating candidates is expensive (sensory panels, pilot runs) because BO is sample-efficient; Pareto-aware BO handles the substitution trade-off space natively. *Strength:* efficient on small evaluation budgets, handles noisy observations. *Weakness:* scales poorly above moderate dimensionality, and the surrogate is sensitive to representation.

### Reinforcement learning

Cited for iterative substitution in Oz et al. and for fermentation process control in the consortium paper. Fits when candidate generation and evaluation happen in a feedback loop (digital twin, in-line sensing) and exploration can be rewarded by structured signals. *Strength:* handles sequential decision-making, constraints, and multi-step processes. *Weakness:* sample-hungry without simulator; reward shaping is subtle.

### Generative models (VAE, GAN, diffusion)

Kuhl's Nature Perspective is the clearest on this. VAEs encode formulations into a latent space; natural-language prompts or target property vectors condition decoding to propose novel formulations. GANs train a generator to produce candidate formulations against a discriminator that distinguishes real from synthetic. Diffusion models are cited for *de novo protein design* in alternative-meat contexts (consortium paper). *Strength:* expressive over structured output; conditioning on targets gives inverse-design capability (see [[inverse-design]]). *Weakness:* needs large training corpus; often proposes infeasible candidates that a constraint layer must filter.

### Graph neural networks

Dominant representation for ingredient spaces (see [[ingredient-data-structures]]). Used for both *property prediction* (the Principal Odor Map predicts odor profiles from molecular structure at human-level accuracy) and *candidate generation* (graph embeddings let a search operator "walk" from a known ingredient to functionally similar but differently priced alternatives).

### LLMs

Used for (a) generating candidate recipes from natural-language prompts, (b) literature mining to extract ingredient–function–sensory relationships that structure the search space, (c) reasoning over cultural and regulatory constraints during substitution. NotCo's Generative Aroma Transformer is the prominent named example. See [[genai-leverage-points]]. *Strength:* respects soft constraints (cultural, dietary, regulatory), accepts high-level human intent. *Weakness:* lacks molecular-level understanding; will hallucinate infeasible combinations.

### Ontology-based rule engines

Domain-knowledge-encoded filters that enforce regulatory, dietary, and cultural constraints after candidate generation. Plant Jammer is the named platform. Often used in composition with ML-based generators to prune hard constraint violations.

### Constraint programming / sparse regression

Mentioned by the consortium paper as a post-processing step to refine generative-model candidates against explicit constraints (cost ceilings, target-property bands).

## Choosing among them

The corpus does not prescribe a single winner. The implicit taxonomy:

- **Tight constraints, expensive evaluation, moderate-dim space** → Bayesian optimisation with Pareto-aware acquisition.
- **Large-scale property prediction with sensory and molecular structure** → GNN surrogates.
- **Inverse-design framing** (target properties → formulation) → VAE/GAN/diffusion with conditioning.
- **Soft constraints involving intent, culture, or dietary context** → LLM-assisted proposal with ontology filtering downstream.
- **Sequential or process-coupled decisions** → RL (with a trusted simulator).
- **Legacy scenario-enumeration problems** → GA or scenario trees, with the modern literature nudging toward surrogates or generative proposals for sample efficiency.

Real pipelines combine classes. NotCo's published description couples latent-space generation with expert sensory feedback loops; the consortium paper describes BO and active learning around a GNN surrogate.

## Implication for the expanded method

The existing method (GA + predictive models) has a *generator* (GA) and a *scorer* (predictive models). The main levers to pull are:

1. **Richer generators** — adding LLM-assisted proposal for the ingredient-substitution class of problem, or generative-model proposals for novel formulations unconstrained by recipe priors.
2. **Better scorers** — GNN-based property surrogates informed by literature-mined ingredient relationships.
3. **MOO-native selection** — replacing weighted-sum or lexicographic ranking with Pareto-aware selection (see [[multi-objective-optimization]]).
4. **A constraint/ontology layer** — so that regulatory and cultural filters are first-class, not post-hoc.

## Source

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — scenario/decision-tree candidate generation; automation as explicit future direction
- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — BO, RL, GNN, LLM, ontology-based rules, multi-method framing
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — latent-space autoencoders, conditional generation, diffusion for proteins, LLM fine-tuning on Recipe1M+, multi-agent LLMs, GA for fermentation
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — hybrid data+physics models, PIPA / Digital Extruder
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — VAE, GAN, foundation-model framing, NotCo generative aroma transformer

## Related

- [[ga-in-context]]
- [[multi-objective-optimization]]
- [[ingredient-substitution]]
- [[predictive-models]]
- [[inverse-design]]
- [[genai-leverage-points]]
- [[ingredient-data-structures]]
- [[industry-examples]]
