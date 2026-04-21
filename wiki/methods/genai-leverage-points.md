# GenAI Leverage Points

Concrete ways LLMs and other generative models can enter the formulation workflow, drawn from the proposals across the AI-focused sources. Framed as *entry points* — discrete places where GenAI adds leverage — rather than as a replacement for the existing pipeline.

## Entry points identified in the corpus

### 1. Literature → structured knowledge

Use LLMs to extract ingredient–function–sensory–process relationships from published papers, recipes, and reviews; populate a knowledge graph that structures downstream search and reasoning. Oz et al. and the consortium paper both emphasise this as the highest-leverage near-term use: the literature contains decades of relationship knowledge that is currently locked in prose. This directly addresses the tacit-knowledge bottleneck Benner's thesis identified 20 years ago (see [[npd-process]]).

### 2. Candidate generation from natural-language intent

Text-to-formulation: customer briefs expressed in natural language become inputs to a conditional generator. NotCo's **Generative Aroma Transformer** is the named exemplar — a textual flavour profile (*"cherry, candy, vanilla"*) yields a novel flavour-molecule recipe. More broadly, LLMs handle soft semantic constraints ("kid-friendly snack", "Mediterranean profile") that hard optimisation objectives struggle with. Best paired with downstream constraint filters since LLMs hallucinate infeasible combinations.

### 3. Ingredient substitution with cultural and dietary reasoning

LLMs combined with knowledge graphs generate substitutability heuristics respecting dietary restrictions, allergen sensitivities, and cultural norms. Plant Jammer's formulation environment — prioritising Halal-certified texturisers, excluding allergens, minimising carbon footprint — illustrates the pattern. The leverage is that soft constraints are encoded in the LLM's training data; hard constraints come from the ontology layer.

### 4. Consumer feedback → quantifiable parameters

LLMs translate qualitative feedback ("too chewy", "too sweet on the finish") into engineering parameters the formulation pipeline can act on (Zhou et al.). Closes a loop that is usually manual and high-latency. Particularly useful when consumer input arrives in multiple languages or informal channels (reviews, social media).

### 5. Formulation copilot for R&D teams

LLMs as interactive assistants to food scientists: surface relevant literature for a brief, suggest candidate substitutions, explain the reasoning trace. The "formulation copilot" framing from the consortium paper. Value is cognitive leverage on the scientist's own workflow, not autonomous decision-making.

### 6. Multi-agent agentic AI for discovery loops

Systems like **ProtAgents**, **Sparks**, **Virtual Lab**, **BioDiscoveryAgent** (all consortium-paper citations) autonomously generate hypotheses, run simulations, and report. Applied to food, the obvious targets are ingredient discovery (search chemical space for new bioactive or functional compounds) and fermentation optimisation. Deployment in food manufacturing is still at the pilot stage.

### 7. Diffusion models for de novo protein design

Cited in the consortium paper as the protein-side inverse-design pattern for plant-based meat: generate novel edible-protein sequences with tunable mechanical and nutritional properties. Closer to biotech than to classic formulation, but relevant to the alternative-protein expansion of the design space.

### 8. Synthetic training data generation

LLMs generate synthetic texture-descriptor-to-mechanical-property pairings to augment sparse sensory training sets (consortium paper). Useful as an augmentation technique when ground-truth labels are expensive; should be flagged as synthetic and not conflated with panel data.

### 9. Workforce training and tutoring

Intelligent tutoring systems adapted to food-science curricula; AR/VR simulations of manufacturing environments (Zhou et al.). Tangential to formulation itself but relevant to the institutional setting the method sits in.

### 10. Recipe generation under constraints

Fine-tuned LLMs producing constrained recipes (nutritional targets, sustainability caps, allergen exclusions, cultural preferences). Closer to consumer-product personalisation than to industrial formulation, but the constraint-aware pattern transfers.

## Risks the sources flag

- **Lack of molecular-level understanding.** LLMs trained on text "lack molecular-level understanding of food" (consortium paper) and will make chemically nonsensical proposals. Couple with physics- or chemistry-aware surrogates.
- **Cultural unevenness.** Off-the-shelf LLMs "perform unevenly across cultural contexts" and can misread preferences. Fine-tuning or cultural-embedding layers are needed for non-Western deployments.
- **Hallucinated health claims.** Oz et al. caution that many LLM-proposed health benefits are based on preclinical data and "require further validation for physiological relevance." Never let an LLM draft a nutrition claim without human and (if applicable) regulatory review.
- **Numerical inconsistency.** LLMs "can generate outputs that are numerically inconsistent, unsafe, or infeasible." Always validate quantitative outputs (fractions, temperatures, concentrations) against constraints before acting on them.
- **Black-box outputs for regulated work.** Regulatory submissions require traceable reasoning. LLM outputs as-is are usually inadequate; keep the LLM in a proposal role with human-written justifications downstream.

## Implication for the expanded method

Pragmatic order of integration, highest leverage first:

1. **Literature-mining layer** — run LLMs over the corpus of scientific papers and internal reference documents to populate the ingredient-relationship graph (see [[ingredient-data-structures]]).
2. **Substitution proposal** — LLM-assisted substitution for under-specified briefs, paired with ontology filtering and existing predictive scoring.
3. **Feedback translation** — consumer / panel feedback → engineering parameters.
4. **Formulation copilot** — LLM-as-assistant surfacing relevant prior work and flagging constraints during human design sessions.
5. **Conditional generators** (VAE, diffusion) for inverse design once a labelled (formulation, property) corpus is available (see [[inverse-design]]).

The agentic-AI and foundation-model directions are worth tracking but premature for a near-term extension without significant data infrastructure.

## Source

- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — LLMs for substitution reasoning, knowledge-graph integration, health-claim caveats
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — formulation copilot framing, ProtAgents / Sparks / Virtual Lab / BioDiscoveryAgent, synthetic-data generation, LLM risks (molecular understanding, cultural bias)
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — consumer-feedback translation, knowledge-base capture, workforce-training applications
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — NotCo Generative Aroma Transformer, foundation-model framing, ChefFusion
- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — (context) tacit-knowledge bottleneck LLM literature mining addresses

## Related

- [[candidate-generation]]
- [[inverse-design]]
- [[ingredient-substitution]]
- [[human-in-the-loop]]
- [[ingredient-data-structures]]
- [[industry-examples]]
- [[open-gaps]]
