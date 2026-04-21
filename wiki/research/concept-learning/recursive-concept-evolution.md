# Recursive Concept Evolution for Compositional Reasoning in Large Language Models

Chaudhry (Purdue, 2025; arXiv:2602.15725). RCE addresses the claim that fixed pretrained representation geometry imposes a hard ceiling on compositional reasoning: when the basis directions needed for a task were not learned during pretraining, no amount of CoT, ToT, or self-consistency can synthesise them — they all "search more thoroughly with the wrong map". RCE attaches a learnable, growing library of low-rank concept *subspaces* `{B_i ∈ R^{d×r}}` (default `r=16`, `d=4096`) to a frozen base model (Mistral-7B). At a designated mid-layer `ℓ*=18`, an MLP gate selects top-`k=2` concepts and the residual stream is updated `h' = h + Σ_{i∈A(x)} g_i(x) B_i B_i^⊤ h`. Concepts spawn when an entropy/margin failure score fires, compete via an MDL criterion, merge via SVD when synergistic, and crystallise via checkpointing. Reported gains over DisCO: +8.3 on ARC-AGI-2, +6.1 on MATH, +5.7 on BBH, +7.2 on GPQA, +4.9 on HLE, at 1.04× base FLOPs.

## Method

- **Concept = (basis, gate, projection).** `C_i = (B_i, g_i, P_i = B_i B_i^⊤)`. `B_i` has orthonormal columns; `g_i: R^d → [0,1]` is a sparse top-`k` MLP gate; `P_i` projects into the concept subspace and back. Each concept ≈ 65k parameters; full library of 128 ≈ 33MB (<0.25% of base).
- **Spawn.** Failure score `F(x) = H(logits) / (M(logits) + ε)` with `M = p_(1) − p_(2)`. When `F > τ` (default 5.0), a generator MLP `G(h_pool) → R^{d×r}` produces `k_s` candidates (perturbed by isotropic noise σ=0.03, QR-orthogonalised).
- **Compete (MDL).** Accept iff `ΔL − λ Ω(C_new) > 0` where `Ω(C_i) = α ‖B_i‖_* + β KL(g_i ‖ π_i)`. Nuclear-norm penalty bounds effective rank; KL penalty enforces gate sparsity.
- **Merge.** For pairs `(i,j)` with negative synergy `Syn(i,j) = L(C\{i,j} ∪ {C_ij}) − L(C)`, fuse via `[B_i | B_j] ∈ R^{d×2r} → top-r SVD → QR`. Yields hierarchical compositions (primitive symmetry + colour-map → "reflect-and-recolor").
- **Regularisation.** `L_total = L_LM + λ_orth Σ_{i≠j} ‖B_i^⊤ B_j‖_F^2 + λ_ov (1/N) Σ_i ‖B_i^⊤ B_i − I_r‖_F^2 + λ_gate H(g)` plus a KL-to-frozen-base penalty to prevent fluency drift. Base model frozen throughout.
- **Crystallisation.** Checkpoint the library; optionally distill into permanent LoRA adapters with an EWC-style Fisher-information trust region to avoid clobbering prior concepts.

## Claims

- **Main table (Mistral-7B).** Base 12.4 / 28.6 / 51.3 / 24.1 / 8.2 → RCE 28.0 / 47.4 / 70.5 / 41.4 / 18.7 on ARC-AGI-2 / MATH / BBH / GPQA / HLE. Best baseline DisCO: 19.7 / 41.3 / 64.8 / 34.2 / 13.8.
- **Compute.** RCE 1.04× base FLOPs vs CoT 3.2×, SC(n=16) 16×, ToT 24.5×.
- **OOD robustness on ARC-AGI-2.** Performance retention under colour permutation / rotation / distractor: RCE 94.3 / 91.7 / 95.8 vs DisCO 78.5 / 73.9 / 80.2.
- **Library dynamics.** Stabilises at 47 active concepts (12 primitives, 23 merged intermediates, 12 high-level abstractions). Average task-reuse: primitives 4.3, merged 8.7. Sublinear growth.
- **Ablations on ARC-AGI-2 / MATH (Mistral-7B).** Removing MDL: 14.6 / 31.2 (largest drop, −13.4 / −16.2). Removing invariance augmentation: 18.3 / 39.8. Removing KL constraint: 21.5 / 35.6. Removing merge: 23.1 / 42.7.
- **Theory.** Proposition 1: rank of augmented covariance `rank_ε(Σ′) ≥ rank_ε(Σ)`, strict when `B_i` has support outside col(Σ). PAC-Bayesian generalisation bound proportional to `√(Ω(C)/n)`.
- **Caveats (per the paper).** Llama-3-8B and Qwen-14B numbers in Table 1 are *projected*, not measured. Failure modes: long formal proofs (single-layer injection limit), explicit external memory tasks, adversarial concept-aligned traps.

## Sample efficiency

RCE is not single-sample but is explicitly *sample-targeted*: a concept is spawned only when the failure score crosses τ, so each new abstraction is paid for by a single difficult example that the existing geometry cannot encode. The MDL gate then forces that abstraction to generalise (compress) or be rejected — preventing the per-example overfitting that single-sample updates normally invite. The merge mechanism amortises further: a concept once accepted contributes to many downstream tasks (reuse rate 4–9), so the per-concept marginal sample cost decays. This is the single most relevant feature for David's project: spawn-on-failure + MDL-on-acceptance is a recipe for "one example, one concept" weight updates that *do not* corrupt unrelated capability, because the base model is frozen and concepts must pay an explicit complexity cost.

## Relevance to the project

This paper offers an operational definition of "concept" that is closer to David's setting than CBMs: a concept is a *low-rank, gate-routed, frozen-base-additive subspace* that is born in response to representational inadequacy and survives only if it compresses. Three project-relevant primitives:

1. **Failure-triggered learning.** `F(x) = H/(M+ε)` is a label-free signal for "the current weights cannot resolve this input" — a candidate trigger for when single-sample fine-tuning should fire instead of running indiscriminately.
2. **MDL as the concept-vs-pattern test.** Pattern matching = library growth without compression; concept acquisition = library growth with negative MDL cost. This makes the project's central thesis (concept vs pattern) operationally measurable: a successful single-sample update should reduce description length on held-out related inputs.
3. **Frozen base + low-rank addend + KL leash.** This is the architectural envelope inside which a single-sample update can be safely localised — orthogonal to existing concepts, sparse on activation, KL-bounded on output drift. The natural project deliverable is a single-sample variant that produces a single new `B_i` rather than RCE's continuous stream.

Caveat: parts of the experimental table are projected and the paper is recent; treat absolute numbers cautiously. The architectural ideas — spawn / MDL / merge / crystallise — are the inspiration regardless.

## Source

- arXiv: 2602.15725
- Raw markdown: `../../../raw/research/single-sample-llm-learning/07-07-recursive-concept-evolution.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/07-recursive-concept-evolution.pdf`

## Related

- [[concept-bottleneck-models]] — fixed concept vocabulary, supervised at training time; RCE is the dynamic, self-supervised counterpart
- [[../in-context-learning-theory/icl-bayesian-inference]] — Bayesian "latent concepts in pretraining" view; RCE adds new concepts post hoc instead of selecting from a fixed prior
- [[../in-context-learning-theory/icl-as-gradient-descent]] — implicit rank-1 update interpretation; RCE adds *explicit* low-rank updates
- [[../meta-learning-few-shot/_overview]] — prior-engineering vs learned-prior distinction maps onto fixed-vocabulary CBM vs evolving RCE
