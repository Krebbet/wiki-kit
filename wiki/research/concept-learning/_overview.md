# Concept Learning

Theme covering *operational definitions of "concept"* in neural models and the two architectural primitives that come with them: the supervised, fixed-vocabulary **concept bottleneck** (CBM) and the self-supervised, dynamic, low-rank **concept subspace library** (RCE). Both papers commit to making "concept" a mechanical object — a coordinate, a subspace, a gate — rather than an emergent representational property, which is what makes them load-bearing for a concept-based fine-tuning method.

## Pages

- [[concept-bottleneck-models]] — Koh et al., ICML 2020. `x →_g c →_f y` with a human-labelled concept vector `c ∈ R^k` at an intermediate layer; matches end-to-end accuracy on OAI / CUB, enables test-time concept intervention, robust to background shift on TravelingBirds.
- [[recursive-concept-evolution]] — Chaudhry 2025 (arXiv:2602.15725; numbers include projected rows). Frozen base + growing library of low-rank subspaces `{B_i ∈ R^{d×r}}` with top-k gated residual injection at layer 18; spawn on entropy/margin failure, compete via MDL, merge via SVD; +4.9–8.3 over DisCO on ARC-AGI-2 / MATH / BBH / GPQA / HLE at 1.04× base FLOPs.

## Cross-cutting themes

**"Concept" is an architectural commitment, not a representation claim.** CBM pins concepts to specific coordinates of a chosen bottleneck layer; RCE pins them to orthonormal low-rank subspaces added to the residual stream. In both papers, the concept object is addressable (you can intervene on it or turn it off) *by construction*, rather than being inferred post hoc via probes. Koh et al. show explicitly that linear probes on a standard model fail to recover the concepts a CBM bottleneck captures by design.

**Fixed vs evolving vocabulary is the main axis.** CBM needs the concept set enumerated and labelled at training time (`k` components known in advance). RCE drops that requirement: concepts are spawned by a label-free failure score `F(x) = H(logits) / (M(logits) + ε)` and survive only if they reduce description length. This is the single biggest gap between classical concept learning and concept-based LLM fine-tuning, because the latter has no curated concept inventory.

**Supervision moves from outputs to concepts (CBM) or disappears (RCE).** CBM reframes annotation as labelling intermediate concepts rather than final targets; RCE reframes annotation cost as zero but substitutes an MDL prior. Both answer the same question — *how do you tell a concept from a pattern?* — differently: CBM by external ground truth, RCE by compression.

**Intervention and gating are duals of the same primitive.** CBM exposes concepts for test-time *correction* (oracle replaces `ĉ_j`); RCE exposes them for train-time *routing* (`g_i(x)` selects). Both require the concept channel to be architecturally isolated from the main pathway, else the model learns to route around it (CBM joint regime with small `λ`; RCE without KL-to-base).

**Concept routing beats end-to-end on distribution shift.** TravelingBirds (CBM: 0.48–0.50 vs 0.63 standard, under train/test background swap) and ARC-AGI-2 perturbations (RCE: 91–96% retention under colour permutation / rotation / distractor vs DisCO's 74–80%) both point at the same mechanism: a concept channel that is not used to solve the training task via spurious correlations cannot be corrupted by them at test time.

**Concept-based fine-tuning's operational core is here.** From CBM: the independent-bottleneck result (`f` trained on true `c` has best post-intervention error) implies that single-sample concept imprinting needs a *clean* concept channel untainted by joint optimisation. From RCE: failure-triggered spawn + MDL + frozen base + KL leash is exactly the envelope a one-example weight update can live inside without corrupting unrelated capability. The natural project synthesis is to spawn a single `B_i` per example when `F(x) > τ`, constrain it to be orthogonal to the existing library, and keep it only if it pays its MDL cost on held-out related inputs.

## Method comparison

| Aspect | CBM (Koh 2020) | RCE (Chaudhry 2025) |
|---|---|---|
| Concept object | Coordinate of bottleneck layer, dim 1 | Low-rank subspace `B_i ∈ R^{d×r}`, r=16 |
| Vocabulary | Fixed, human-enumerated, `k` known a priori | Open, grows from 0; stabilises ~47 concepts |
| Annotation | Dense per-concept labels `(x, c, y)` | None — MDL replaces labels |
| When concept is added | At training time, all at once | Online, when failure score fires |
| Acceptance criterion | Joint / sequential / independent loss | `ΔL − λ Ω(C) > 0` (MDL with nuclear-norm + KL) |
| Base model | Jointly trained (or frozen `f` in sequential) | Frozen; concepts are additive residual injections |
| Intervention handle | Test-time coordinate substitution | Top-k gate activation at layer 18 |
| Domain evaluated | Vision (OAI x-rays, CUB birds) | LLM reasoning (ARC-AGI-2, MATH, BBH, GPQA, HLE) |
| Robustness probe | TravelingBirds background swap | ARC-AGI-2 colour/rotation/distractor perturbations |
| Sample-efficiency unit | Concept correction at test time | Failure-triggered spawn at train time |
| Parameter cost | Width `k` on one layer | ~65k params/concept, ~0.25% of base for 128 |
| Compute at inference | Same as base | 1.04× base FLOPs |

## Open questions

- **Can CBM's oracle-concept signal and RCE's MDL signal be combined?** A hybrid where human-labelled concepts seed the library and MDL governs the rest is not explored in either paper, yet it is the natural answer to "you have a few labelled concepts but no closed set".
- **Is concept-as-axis (CBM) ever equivalent to concept-as-subspace (RCE) under a change of basis?** If so, what conditions (isotropy, rank budget) make the two architectures interchangeable; if not, what task properties select each.
- **Can RCE's spawn trigger `F(x) = H/(M+ε)` be used as a single-sample-update gate outside RCE itself?** The signal is label-free and cheap, which makes it a candidate for "when should I fire a single-example fine-tune step?" in a broader training loop.
- **Do concepts in RCE's library correspond to anything in Balashov's RL-induced sparse subnetwork?** Both are low-dimensional, task-specific, and added on top of a frozen base — cf. [[../rlvr-mechanics/rl-sparse-subnetwork]]. No paper co-measures.
- **Closed-vocabulary concepts fail on open-world LLM targets.** CBM's biggest transfer blocker for this project is that general LLM "concepts" cannot be pre-enumerated. How much of CBM's intervention story survives if concepts are discovered instead of declared?
- **RCE's Llama-3-8B and Qwen-14B numbers are *projected* not measured** (per the paper's own caveat). Treat absolute gains cautiously; the architectural primitives (spawn / MDL / merge / crystallise) are the durable contribution regardless.

## Source PDFs

- `../../../raw/research/single-sample-llm-learning/pdfs/H-1-concept-bottleneck-models.pdf`
- `../../../raw/research/single-sample-llm-learning/pdfs/07-recursive-concept-evolution.pdf`

## Related themes

- [[../in-context-learning-theory/_overview]] — Bayesian "latent concepts in pretraining" view; CBM makes those concepts observed; RCE adds new ones post hoc
- [[../meta-learning-few-shot/_overview]] — concepts as cluster centres (ProtoNets) and as adaptation directions (MAML); representation-side counterparts to the architectural commitments here
- [[../rlvr-mechanics/_overview]] — RL edits a sparse, low-rank-adjacent subnetwork; structurally adjacent to RCE's concept subspaces, with no paper co-measuring
- [[../single-sample-rl-finetuning/_overview]] — the downstream setting these primitives feed into
