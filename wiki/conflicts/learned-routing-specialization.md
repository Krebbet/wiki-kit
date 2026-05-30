# Conflict — Does Learned Routing Produce Specialization?

**Status:** open
**Opened:** 2026-04-24
**Ruling:** frame as open / contested. Both positions worth tracking as the wiki grows.

## The question

Does learned routing in modular transformers produce genuine functional specialization of experts/blocks, or does it reliably underspecialize (collapse to ensembling, route by surface-form, fail to improve as task count grows)?

## Position A — learned routing specializes

Evidence from:

### Expert Choice Routing (01)

EC routing outperforms hash-layer routing by 2.7 points avg on GLUE/SuperGLUE at 100M/64E (84.0 vs 81.3) and by 3.4 points at 8B/64E (92.6 vs 89.2 for dense). The paper argues the gap demonstrates that learned affinity drives genuine specialization beyond load balancing alone — hash routing achieves the same structural load balance without learned weights and scores lower. **Caveat: specialization is inferred entirely from downstream performance gaps. The paper does not mechanistically probe what semantic content routes to which expert; there is no routing analysis or expert inspection. The specialization claim is performance-inferred, not demonstrated.**

### Mixture of Depths (02)

MoD routing analysis (Figure 5) shows a non-trivial structured pattern: some tokens consistently participate in every block while others route around blocks whenever possible, and tokens routed more often correlate with higher-entropy (harder-to-predict) predictions. Stochastic routing (Gaussian-sampled weights) fails badly — significantly worse than the vanilla baseline — confirming that the learned signal is essential and that the observed pattern is not an artifact of capacity allocation. This is evidence of input-conditional structured routing, not ensemble averaging.

### MICRO (10)

MICRO (AlKhamissi et al.) is the strongest positive evidence in this batch. A per-token top-1 MLP router assigns tokens to one of four brain-network-aligned expert blocks (Language, Logic, Social, World) per layer. Observed specialization:

- Domain-consistent routing on test inputs: arithmetic tokens route to the Logic expert; social-cognition tokens route to the Social expert.
- Layer-wise hierarchy: early layers favor the Language expert for linguistic grounding; deeper layers route to domain-specific experts. This hierarchy was not explicitly enforced.
- Router probabilities on 1,000 sentences correlate r = 0.7 with independently collected human behavioral ratings of mental-state content (Tuckute et al., 2024b dataset).
- Neuroscience localizer experiments confirm that Language and MD localizers recover the corresponding expert modules.

**Critical caveat: MICRO's specialization is seeded by a three-stage curriculum — Stage 2 calibrates the router using GPT-4O-annotated token-level pseudo-labels before large-scale SFT. Specialization is not the product of raw end-to-end learned routing; it requires explicit inductive bias injection. The r = 0.7 result and domain-consistent routing patterns are genuine, but they arise from a training regime specifically designed to produce them.**

## Position B — learned routing underspecializes

Evidence from:

### Modular Deep Learning survey (09)

The survey (Pfeiffer, Ruder, Vulić, Ponti) catalogues a consistent body of contrarian evidence across multiple independent studies:

- **Mittal et al. (2022)** (cited via survey): learned routing under-utilizes modules and achieves *less* specialization as task count grows. Fixed routing generally outperforms learned routing in their evaluation.
- **Muqeeth et al. (2022)** (cited via survey): learned routing underperforms fixed routing in real (non-synthetic) multi-task settings.
- **Lewis et al. (2021)** (cited via survey): in MoE transformers, routing is driven by token surface form (syntactic/semantic token identity) rather than by sentence-level or task-level semantics, limiting functional expressiveness.
- **Module collapse**: documented as a systematic failure of hard learned routing without auxiliary losses — the router over-exploits a small subset of modules, leaving others untrained.
- **Training instability**: at initialization, modules are random so the router cannot make principled decisions; modules do not specialize until routed consistently — creating a chicken-and-egg instability.
- **Token-level routing leads to out-of-domain drops** (Artetxe et al., 2022, cited via survey): pre-training gains from learned routing do not reliably transfer to fine-tuning.

The survey's summary position: fixed routing (dispatch by task identity, language, or domain metadata known a priori) generally outperforms learned routing and guarantees specialization by construction.

## Possible resolutions (editorial)

Three framings — not ruling between them:

1. **Resolved in favor of Position A** — learned routing does specialize; earlier negative results (Mittal, Muqeeth, Lewis) reflect weak training regimes, insufficient scale, or poorly designed routing architectures. EC and MoD demonstrate that with proper structural design (expert-choice inversion, load-balance guarantees), specialization emerges.

2. **Resolved in favor of Position B** — learned routing reliably underspecializes; Position A's claims are either performance-inferred without mechanistic demonstration (EC), emergent but semantically shallow (MoD's token-difficulty correlation is not task-level functional specialization), or dependent on curriculum scaffolding rather than raw learned routing (MICRO). The survey's evidence base is broader and more heterogeneous than any single positive result.

3. **Contingent** — learned routing specializes only under specific conditions: sufficient calibration signal (MICRO's curriculum), structural load-balance enforcement (EC's expert-choice inversion), or explicit training to make routing non-trivial (MoD's stochastic control confirms randomness fails). Raw end-to-end learned routing without these scaffolds is insufficient.

MICRO's three-stage curriculum is consistent with all three resolutions but most naturally supports (3): specialization is achievable under learned routing given the right inductive biases, not as a default outcome of gradient descent on task loss.

## What would resolve this?

*(Editorial — not derived from the sources above.)*

- **Mechanistic probes of expert internals**: go beyond performance gaps and routing distributions to inspect what representations experts encode (e.g., probing classifiers on expert-specific hidden states, causal ablations that swap expert assignments). EC in particular provides no such evidence.
- **Controlled fixed-vs-learned routing comparisons**: hold architecture, scale, task count, and training compute constant; vary only whether routing is fixed (metadata-driven) or learned. The survey's claims rest on multiple heterogeneous comparisons; a clean paired study at modern scale is missing.
- **Scaling studies of specialization emergence**: does functional specialization reliably emerge at larger compute/task-count, or does underspecialization persist? Mittal et al.'s finding that specialization *decreases* with task count is particularly worth stress-testing at scale.
- **Disentangling curriculum from routing**: train a MICRO-like architecture without Stage 2 calibration and measure how much specialization survives. This would directly test whether the router's learned signal suffices or whether the inductive bias is doing the work.
- **Standardized specialization metrics**: the survey flags (§9.1) that no benchmark currently measures routing quality or specialization degree independently of downstream performance. Without such metrics, "specialization" is not directly observed in any of the above papers.

## Related
- [[expert-choice-routing]]
- [[mixture-of-depths]]
- [[modular-deep-learning-survey]]
- [[mixture-of-cognitive-reasoners-micro]]
- [[routing-mechanisms-in-modular-networks]]

## Source
- `raw/research/thesis-foundations/01-expert-choice-routing.md`
- `raw/research/thesis-foundations/02-mixture-of-depths.md`
- `raw/research/thesis-foundations/09-modular-deep-learning-survey.md`
- `raw/research/thesis-foundations/10-neuro-cognitive-reasoners.md`
