# Recursive Concept Evolution for Compositional Reasoning in Large Language Models

Chaudhry (Purdue, 2025; arXiv:2602.15725). RCE addresses the claim that fixed pretrained representation geometry imposes a hard ceiling on compositional reasoning: when the basis directions needed for a task were not learned during pretraining, no amount of CoT, ToT, or self-consistency can synthesise them — they all "search more thoroughly with the wrong map". RCE attaches a learnable, growing library of low-rank concept *subspaces* $\{B_i \in \mathbb{R}^{d \times r}\}$ (default $r=16$, $d=4096$) to a frozen base model (Mistral-7B). At a designated mid-layer $\ell^*=18$, an MLP gate selects top-$k=2$ concepts and the residual stream is updated $h' = h + \Sigma_{i \in A(x)} g_i(x) B_i B_i^\top h$. Concepts spawn when an entropy/margin failure score fires, compete via an MDL criterion, merge via SVD when synergistic, and crystallise via checkpointing. Reported gains over DisCO: +8.3 on ARC-AGI-2, +6.1 on MATH, +5.7 on BBH, +7.2 on GPQA, +4.9 on HLE, at 1.04× base FLOPs.

## Method

- **Diagnosis vs alternative diagnosis.** Easy misread: "the model is uncertain about *which* of its existing parts hold the answer, RCE re-routes / amplifies the right one." That would be a *routing* problem (knowledge present, access broken) and would call for retrieval/attention fixes. RCE's diagnosis is stronger: a **representational** problem — "the basis directions needed for a task were not learned during pretraining." $F$ detects the symptom of *that*, and the additive $B_i$ are constructed *new directions* (favoured by the spawn mechanism precisely when they have support outside $\text{col}(\Sigma)$, see Proposition 1 below), not selections from existing directions. Without this distinction the method collapses to "boost what the model already knows", which is exactly what CoT/ToT/SC do and what the paper argues hits the representational ceiling.
- **Concept = (basis, gate, projection).** $C_i = (B_i, g_i, P_i = B_i B_i^\top)$. $B_i$ has orthonormal columns; $g_i: \mathbb{R}^d \rightarrow [0,1]$ is a sparse top-$k$ MLP gate; $P_i$ projects into the concept subspace and back. Each concept $\approx$ 65k parameters; full library of 128 $\approx$ 33MB (<0.25% of base).
- **Geometric reading.** Decompose $h = h_\parallel + h_\perp$ w.r.t. subspace $B_i$. Then $h' |_{\text{im}(B_i)} = (1 + g_i(x)) h_\parallel$ and $h' |_{\text{im}(B_i)^\perp} = h_\perp$ — the update is a **selective, input-conditional scalar amplification** of whatever component of the residual stream already lies in the learned subspace, with the orthogonal complement untouched. Per concept, two things are jointly learned: *which* subspace to amplify ($B_i$, $d \times r$, orthonormal) and *how much* to amplify ($g_i(x)$, scalar, top-$k$ sparse). The base model is frozen throughout — unlike LoRA-style FT, no pretrained weight is modified; RCE is a learned, gated, additive read-modify-write on the residual stream of a frozen network. Note Proposition 1 (below): the spawn mechanism prefers $B_i$ with support *outside* $\text{col}(\Sigma)$, so the "amplification" frame should not be read as "boost directions already prominent in $h$" — the load-bearing case is amplifying directions the pretrained geometry barely encoded.
- **Spawn.** Failure score $F(x) = H(\text{logits}) / (M(\text{logits}) + \varepsilon)$ with $H$ the entropy of the next-token marginal distribution and $M = p_{(1)} - p_{(2)}$ the top-1−top-2 probability gap. When $F > \tau$ (default 5.0), a generator MLP $G(h_{\text{pool}}) \rightarrow \mathbb{R}^{d \times r}$ produces $k_s$ candidates (perturbed by isotropic noise $\sigma=0.03$, QR-orthogonalised). Gradients from the downstream LM loss propagate back through the projection $B_i B_i^\top h$ into $G$'s parameters, so the generator learns to produce subspaces that reduce prediction error on inputs where $F$ is high — i.e. trigger and candidate factory co-adapt.
  - **Why H/M and not H or M alone.** The two quantities detect different failure modes. *H alone* would fire on legitimate paraphrastic ambiguity (interchangeable function words, near-synonyms) where the basis is fine; *M alone* would fire on a sharp near-tie between two well-formed alternatives even when the rest of the distribution is sharp. The ratio fires only when the distribution is **both diffuse and uncommitted** — many alternatives carry mass *and* the top two are not separated — which is the diagnostic for "no basis direction can pin down the answer". This is what the paper calls "representational inadequacy"; importantly, $F$ is gradient-free and label-free — purely a function of the model's own logits — making it usable as a single-sample fine-tuning trigger without external supervision.
- **Compete (MDL).** Accept iff $\Delta L - \lambda \Omega(C_{\text{new}}) > 0$ where $\Omega(C_i) = \alpha \|B_i\|_* + \beta \text{KL}(g_i \| \pi_i)$. Nuclear-norm penalty bounds effective rank; KL penalty enforces gate sparsity.
- **Merge.** For pairs $(i,j)$ with negative synergy $\text{Syn}(i,j) = L(C \setminus \{i,j\} \cup \{C_{ij}\}) - L(C)$, fuse via $[B_i | B_j] \in \mathbb{R}^{d \times 2r} \rightarrow \text{top-}r \text{ SVD} \rightarrow QR$. Yields hierarchical compositions (primitive symmetry + colour-map → "reflect-and-recolor").
- **Regularisation.** $L_{\text{total}} = L_{\text{LM}} + \lambda_{\text{orth}} \Sigma_{i \neq j} \|B_i^\top B_j\|_F^2 + \lambda_{\text{ov}} (1/N) \Sigma_i \|B_i^\top B_i - I_r\|_F^2 + \lambda_{\text{gate}} H(g)$ plus a KL-to-frozen-base penalty to prevent fluency drift. Base model frozen throughout.
- **Crystallisation.** Checkpoint the library; optionally distill into permanent LoRA adapters with an EWC-style Fisher-information trust region to avoid clobbering prior concepts.

## Claims

- **Main table (Mistral-7B).** Base 12.4 / 28.6 / 51.3 / 24.1 / 8.2 → RCE 28.0 / 47.4 / 70.5 / 41.4 / 18.7 on ARC-AGI-2 / MATH / BBH / GPQA / HLE. Best baseline DisCO: 19.7 / 41.3 / 64.8 / 34.2 / 13.8.
- **Compute.** RCE 1.04× base FLOPs vs CoT 3.2×, SC(n=16) 16×, ToT 24.5×.
- **OOD robustness on ARC-AGI-2.** Performance retention under colour permutation / rotation / distractor: RCE 94.3 / 91.7 / 95.8 vs DisCO 78.5 / 73.9 / 80.2.
- **Library dynamics.** Stabilises at 47 active concepts (12 primitives, 23 merged intermediates, 12 high-level abstractions). Average task-reuse: primitives 4.3, merged 8.7. Sublinear growth.
- **Ablations on ARC-AGI-2 / MATH (Mistral-7B).** Removing MDL: 14.6 / 31.2 (largest drop, −13.4 / −16.2). Removing invariance augmentation: 18.3 / 39.8. Removing KL constraint: 21.5 / 35.6. Removing merge: 23.1 / 42.7.
- **Theory.** Proposition 1: rank of augmented covariance $\text{rank}_\varepsilon(\Sigma') \geq \text{rank}_\varepsilon(\Sigma)$, strict when $B_i$ has support outside $\text{col}(\Sigma)$. PAC-Bayesian generalisation bound proportional to $\sqrt{\Omega(C)/n}$.
- **Caveats (per the paper).** Llama-3-8B and Qwen-14B numbers in Table 1 are *projected*, not measured. Failure modes: long formal proofs (single-layer injection limit), explicit external memory tasks, adversarial concept-aligned traps.

## Sample efficiency

RCE is not single-sample but is explicitly *sample-targeted*: a concept is spawned only when the failure score crosses $\tau$, so each new abstraction is paid for by a single difficult example that the existing geometry cannot encode. The MDL gate then forces that abstraction to generalise (compress) or be rejected — preventing the per-example overfitting that single-sample updates normally invite. The merge mechanism amortises further: a concept once accepted contributes to many downstream tasks (reuse rate 4–9), so the per-concept marginal sample cost decays. This is the single most relevant feature for David's project: spawn-on-failure + MDL-on-acceptance is a recipe for "one example, one concept" weight updates that *do not* corrupt unrelated capability, because the base model is frozen and concepts must pay an explicit complexity cost.

## Relevance to the project

This paper offers an operational definition of "concept" that is closer to David's setting than CBMs: a concept is a *low-rank, gate-routed, frozen-base-additive subspace* that is born in response to representational inadequacy and survives only if it compresses. Three project-relevant primitives:

1. **Failure-triggered learning.** $F(x) = H/(M+\varepsilon)$ is a label-free signal for "the current weights cannot resolve this input" — a candidate trigger for when single-sample fine-tuning should fire instead of running indiscriminately.
2. **MDL as the concept-vs-pattern test.** Pattern matching = library growth without compression; concept acquisition = library growth with negative MDL cost. This makes the project's central thesis (concept vs pattern) operationally measurable: a successful single-sample update should reduce description length on held-out related inputs.
3. **Frozen base + low-rank addend + KL leash.** This is the architectural envelope inside which a single-sample update can be safely localised — orthogonal to existing concepts, sparse on activation, KL-bounded on output drift. The natural project deliverable is a single-sample variant that produces a single new $B_i$ rather than RCE's continuous stream.

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
