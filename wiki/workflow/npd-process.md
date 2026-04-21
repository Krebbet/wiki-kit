# NPD Process and the Chain Information Model

The organisational baseline for how food product development works in industry, drawn primarily from Marco Benner's 2004 Wageningen thesis. Useful as the reference "empirical mode" that AI-driven approaches ([[field-overview]]) aim to improve on, and as an articulation of the decision structure that an expanded method must still support.

## Stage-gate skeleton

Most food companies use a **stage-gate** model for new product development (NPD): a pipeline of stages (ideation, concept and formulation, prototyping, scale-up, commercialisation) separated by *gates* where cross-functional reviewers go/kill the project. The gates are risk-reduction checkpoints — later-stage gates typically assess production feasibility, safety, shelf life, and regulatory compliance. Teams are cross-functional (R&D, sensory, QA, packaging, compliance, finance, marketing, sales, logistics, legal).

## The Chain Information Model (CIM)

Benner's thesis proposes the CIM as a tool to make *chain-wide* information flow explicit during NPD. It has three phases:

1. **Information gathering** — identify all product, process, and supply-chain information needed to judge whether a candidate formulation will work end-to-end, from breeder → grower → processor → producer → retailer → consumer.
2. **Information processing** — link the gathered information to understand process effects on quality. The main artefacts here are **Quality Dependence Diagrams** (QDDs) mapping which actors and processes influence each quality characteristic, and an **Information Matrix** (quality characteristics × chain actors) marking strong vs. weak relationships. Decision trees then enumerate feasible options per actor; combinations become scenarios.
3. **Information dissemination** — select the best scenario and distribute actor-specific instructions down the chain.

Selection uses economic and technological feasibility criteria. The thesis explicitly does not specify a formal ranking procedure — scenario selection is human judgement.

## Where the method is tacit today

Benner is candid that construction of the Information Matrix is "mostly an expert job" because the quality-characteristic → process relationships are usually implicit knowledge. The book's chapter 6 flags automation of QDD/matrix construction and text-mining of scientific publications as future work. Two decades on, the modern AI literature picks up exactly those threads — see [[genai-leverage-points]] and [[human-in-the-loop]].

## Implication for the expanded method

The CIM is a **qualitative, scenario-based candidate-generation workflow**. Its modern successors — Bayesian optimisation over formulation vectors, LLM-based substitution, generative inverse design — change *how* scenarios are produced but still need to plug into the gate structure (feasibility checks, cross-functional sign-off) and the chain-wide information layer (ingredient specs, processing conditions, consumer and regulatory inputs). Any expansion of the user's GA + predictive-model pipeline should say explicitly which CIM phase it touches: most candidate-generation work sits in phase 2, not phase 1.

## Source

- `raw/research/formulation-landscape/02-wageningen-systematic-npd.md` — primary source, entire page
- `raw/research/formulation-landscape/07-future-of-food-arxiv.md` — brief alignment on stage-gate framing and the "trial-and-error" baseline

## Related

- [[field-overview]]
- [[human-in-the-loop]]
- [[candidate-generation]]
- [[genai-leverage-points]]
- [[ingredient-data-structures]]
