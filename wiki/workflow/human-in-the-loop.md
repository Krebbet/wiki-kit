# Human-in-the-Loop Patterns

Where human expertise remains essential in computational food formulation, where it can be automated, and what the literature says about the interface between the two.

## Sources agree on what still needs a human

Sensory validation. Every AI-focused source in the corpus (Oz et al., Kuhl, Zhou et al., Kuhl et al.) is explicit that model-predicted sensory properties are not a substitute for human panels on the final candidate. AI can narrow the search, but the last mile is still a tasting. Cultural / regulatory review is the second unanimous point: certification (Halal, Kosher), allergen labelling, GMO disclosure, fair-trade and LCA signals sit in ontology-based filters that gate what humans approve.

## Tacit knowledge vs. data-driven inference

Benner's 2004 Wageningen thesis frames tacit expert knowledge as *the* bottleneck — the Information Matrix and Quality Dependence Diagrams (see [[npd-process]]) exist to surface implicit knowledge into shareable formats. Expert elicitation is the work.

The modern sources flip the balance. Oz et al. and the arXiv consortium paper (2509.21556) push LLMs and knowledge-graph extraction as literature-scale substitutes for expert elicitation: BERT/GPT extract ingredient–function–sensory relationships from published recipes and papers; LLMs reason over dietary and cultural constraints; knowledge graphs encode substitutability heuristics. The claim is not that experts become unnecessary — it is that the elicitation burden moves off the critical path.

A striking, contestable claim in the consortium paper is that fine-tuned LLMs can "match expert food scientists in predicting sensory panel rankings." The context is narrow (specific product categories; specific evaluation metrics), but if it holds, the role of expert sensory intuition in *early-stage* ranking narrows.

## Interface patterns the corpus names

- **Feedback loops.** Consumer feedback ("too chewy") → LLM translation → quantifiable engineering parameters → next formulation iteration (Zhou et al.).
- **Recommender systems with constraint filters.** Plant Jammer lets formulators prioritise Halal-certified texturizers, exclude allergens, and target a carbon-footprint ceiling as first-class inputs.
- **Expert-in-the-loop generation.** NotCo's pipeline couples latent-space candidate generation with expert sensory feedback each cycle — the AI proposes, the human narrows, the AI re-proposes.
- **Digital twins with sensor integration.** Real-time process data (shear, temperature, moisture) continuously retrain the predictive model against in-line measurements (Zhou et al.).
- **Agentic discovery loops.** ProtAgents, Sparks, Virtual Lab, BioDiscoveryAgent autonomously generate hypotheses, run simulations, and report back; humans intervene at review points, not every iteration.

## Implication for the expanded method

The user's existing method is "heavily HITL dependent." Two dimensions to think about:

1. **Where should a human stay?** The corpus answers: sensory validation, regulatory sign-off, cultural judgement, novel-category scaling. A GA + predictive-model pipeline cannot honestly automate these with current data and models.
2. **Where can a human leave?** Literature mining, ingredient-property lookup, constraint-filter construction, first-pass candidate ranking, feedback-to-parameter translation — all plausible targets for LLM or agentic automation.

Framing extensions of the method as *which HITL step they remove* is a clean evaluation axis.

## Source

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — tacit-knowledge primacy, Information Matrix as elicitation tool
- `raw/research/formulation-landscape/04-ai-ingredient-substitution.md` — sensory validation still required, recommender-system interfaces
- `raw/research/formulation-landscape/06-ai-sustainable-food-futures.md` — LLM parity claim on sensory ranking, agentic systems, digital twins
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — automation-with-operator-judgement framing, knowledge-base capture
- `raw/research/formulation-landscape/08-ai-for-food-nature-2025.md` — AI as partner, democratisation caveats

## Related

- [[npd-process]]
- [[genai-leverage-points]]
- [[ingredient-substitution]]
- [[open-gaps]]
- [[field-overview]]
