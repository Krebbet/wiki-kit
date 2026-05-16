---
title: "MoRAM: Mixture of Rank-1 Associative Memory"
aliases: ["MoRAM", "Little By Little"]
tags: [moe-adapters, continual-learning, lora, peft, forgetting, rank-1, key-value-memory]
date: 2026-05-16
status: literature
---

# MoRAM: Mixture of Rank-1 Associative Memory

Continual learning with LoRA-based MoE degrades as expert pools grow: coarse rank-$r$ experts have low specialization, new experts duplicate old ones, and external routers increasingly fail to index the expanding pool — "routing collapse." MoRAM (Lu et al., 2025) dissolves this by abandoning coarse-grained experts and explicit routers entirely. Instead, rank-1 adapters are treated as atomic key-value memory pairs that self-activate via intrinsic key-input alignment. New tasks add $r$ new rank-1 atoms; old atoms are frozen. Routing collapses from a learned network to a content-addressable inner product. The framing is "little by little": fine-grained memory expansion that scales without router fragility.

## Source

- arXiv: 2506.21035 — Lu, Zhao, Xue, Yao, Moore, Gong (UNSW / CSIRO Data61), 2025
- Raw capture: `raw/research/moe-adapters/07-07-moram.md`

## Method

### Weights as Linear Associative Memory

The foundation is a reinterpretation of weight matrices. A rank-$m$ matrix $\mathbf{W} \in \mathbb{R}^{d_\text{out} \times d_\text{in}}$ is decomposed into $m$ atomic key-value pairs $\{(\mathbf{k}_i, \mathbf{v}_i)\}_{i=1}^{m}$ such that:

$$\mathbf{y} = \mathbf{W}\mathbf{x} \approx \sum_{i=1}^{m} \mathbf{v}_i (\mathbf{k}_i^\top \mathbf{x})$$

The inner product $\mathbf{k}_i^\top \mathbf{x}$ is the relevance (activation strength) of the $i$-th memory slot; $\mathbf{v}_i$ is the retrieved value. Keys and values are static parameters — not dynamic projections like attention — representing knowledge patterns from pre-training.

### Rank-1 Adapters as Atomic Memory Experts

Rather than a single rank-$r$ block $\Delta\mathbf{W} = \mathbf{B}\mathbf{A}$, MoRAM decomposes the update into $r$ atomic rank-1 terms:

$$\Delta\mathbf{W}\mathbf{x} = \sum_{i=1}^{r} \underbrace{\mathbf{B}_{:,i}}_{\text{Value } \mathbf{v}_i} \left( \underbrace{\mathbf{A}_{i,:}}_{\text{Key } \mathbf{k}_i^\top} \mathbf{x} \right)$$

Row vector $\mathbf{A}_{i,:}$ is the key; column vector $\mathbf{B}_{:,i}$ is the value. After $t$ tasks the accumulated memory $\mathcal{M}_t = \{(\mathbf{B}_{:,i}, \mathbf{A}_{i,:})\}_{i=1}^{r_t}$ grows incrementally, and the effective update is a sparse input-dependent mixture:

$$\Delta\mathbf{W}^{(t)} = \sum_{i=1}^{r_t} w_i \mathbf{B}_{:,i} \mathbf{A}_{i,:}$$

where $w_i \in \mathbb{R}$ is the retrieval confidence of atom $i$ on the current input.

### Self-Activation: Replacing the Router

The mixing weights are derived directly from the key-input alignment — no external router network. For input $\mathbf{x} \in \mathbb{R}^{d_\text{in}}$, the raw relevance score for atom $i$ is:

$$s_i = \frac{\mathbf{A}_{i,:}\,\mathbf{x}}{\sqrt{\sum_{j=1}^{r_t}(\mathbf{A}_{j,:}\,\mathbf{x})^2}}$$

The denominator is $\ell_2$-normalization across the full memory ensemble for numerical stability. This is content-addressable retrieval: the memory key itself determines the atom's utility.

### Sparse Routing Pipeline

Three stages sharpen the sparse mixture:

1. **Top-$k$ masking** — retain only the $k$ highest-scoring atoms:

$$[\text{TopK}(\mathbf{s}, k)]_i = \begin{cases} s_i & \text{if } s_i \in \text{top-}k(\mathbf{s}) \\ -\infty & \text{otherwise} \end{cases}$$

2. **Temperature-scaled softmax** — concentrates probability mass and routes gradients to specialist atoms:

$$w_i = \operatorname{softmax}\!\left(\frac{\text{TopK}(\mathbf{s}, k)}{\tau_{\text{MoRAM}}}\right)_i$$

Lower $\tau_{\text{MoRAM}}$ sharpens specialization; $\tau = 0.01$ is the reported optimum.

3. **Threshold-based pruning at inference** — prunes atoms below relevance threshold $\delta$:

$$w_i \leftarrow \mathbf{1}\{s_i \geq \delta\} \odot w_i$$

### Continual Learning Protocol

For each new task: introduce $r$ new rank-1 pairs, freeze all prior atoms, jointly route across old and new. No replay, no regularization loss, no load-balancing auxiliary. Old frozen atoms can be reused (reactivated by self-activation if relevant) or extended by new ones.

## Claims

- **CLIP / X-TAIL benchmark:** MoRAM outperforms MoE-Adapter, RAIL-Primal, CoDyRA, ZSCL, and others on Transfer, Average, and Last accuracy. It does so without external domain IDs or feature banks required by prior SOTA.
- **LLM / TRACE benchmark:** On LLaMA-2-7B-Chat, MoRAM achieves OP = 44.54 ± 0.9 and BWT = 1.37 ± 0.3; next-best method (TreeLoRA) reaches OP = 43.52, BWT = 3.46. On Gemma-2B-it: OP = 36.27, BWT = 2.74 vs TreeLoRA 33.41 / 8.50. On LLaMA-3-1B-Instruct: OP = 37.77, BWT = 3.12.
- **Forgetting / interference:** Ablation (Table 4) shows external router applied to rank-1 atoms performs *worse* than the coarse MoE-LoRA baseline (routing collapse), while self-activated retrieval matches or exceeds it. Full MoRAM (self-activation + sparsity + temperature + threshold) tops all ablation variants.
- **Parameter efficiency:** MoRAM with 41.9M total / 26.2M active parameters matches LoRA rank-32 (83.9M) on HumanEval and outperforms it on out-of-domain MMLU — 1/3 of active parameters for equivalent or better generalization.
- **Rank specialization:** Visualization shows distinct ranks respond to distinct semantic patches; activation patterns for Task-1 inputs are nearly unchanged after Task-2 training, demonstrating interference suppression.
- **No auxiliary losses needed:** Self-activation naturally yields balanced, stable routing without load-balancing regularization; adding regularization to key vectors was empirically harmful.

## Strengths / Novelty

- **Router-free MoE.** Eliminating the external router removes its failure mode: the router's parameter count grows with the expert pool and must learn increasingly ambiguous mappings. Self-activation scales without degradation because the routing condition is intrinsic to the expert's content.
- **Atomic rank-1 granularity.** Each expert encodes exactly one key-value pair — the minimum possible cross-task surface area. Coarse rank-$r$ adapters force all $r$ subspaces to activate together; rank-1 atoms activate independently. This is the core mechanism behind reduced interference.
- **Content-addressable retrieval.** The "little by little" framing is not just incremental in size but in routing style: inference becomes memory lookup rather than learned dispatch, which is structurally more stable as memory grows.
- **Reuse without entanglement.** Old frozen atoms can be reactivated for new tasks if their key is relevant — cross-task positive transfer without any parameter update to old weights.
- **No task identity at inference.** Unlike methods requiring domain IDs or task boundaries, MoRAM routes purely from input content, enabling operation on mixed-domain test distributions (the X-TAIL setting).

## Weaknesses / Limits

- **Fixed rank-1 granularity.** Forcing every expert to rank-1 may underfit tasks requiring high-dimensional structure that cannot be efficiently factored into many rank-1 atoms. Rank-1 is maximally fine-grained; useful when tasks are sparse in weight space but may require more atoms total.
- **Growing memory pool.** $r_t$ grows linearly with tasks (modulo optional pruning). The top-$k$ routing cap bounds forward-pass cost, but the key-scoring step scales with $r_t$ — could become a bottleneck at very long task sequences.
- **Pruning not deeply evaluated.** The paper mentions low-utility atom pruning for sub-linear expansion but treats it as a secondary result (Appendix A.10). The tradeoff between pruning aggressiveness and retention on earlier tasks is not characterized in the main body.
- **Hyperparameter sensitivity.** Three interlocking sparsity controls ($k$, $\tau$, $\delta$) must be tuned jointly. The ablation shows each contributes and that wrong values hurt, but there is no guidance for setting them in a new continual-learning regime.
- **Benchmark scope.** TRACE and X-TAIL are the primary CL benchmarks. Standard split-CIFAR or split-ImageNet class-incremental settings — where forgetting baselines are most densely studied — are not evaluated in the main paper.

## Relevance to This Wiki's Project

**Router-free MoERA variant.** The current MoERA design uses delta-LoRA experts with an explicit router. MoRAM demonstrates that the router can be eliminated entirely by decomposing adapters to rank-1 and grounding routing in key-input alignment. This is a concrete design point for MoERA: a router-free variant where $R_w$ is replaced by self-activation over atomic behaviour experts. The cost is more experts (rank-1 rather than rank-$r$) but the gain is elimination of router-induced forgetting and routing ambiguity.

**Rank-1 key-value framing connects to FF-as-KV-memories.** MoRAM's grounding in [[../selective-finetuning/ff-kv-memories]] is explicit: the paper cites the linear associative memory literature and treats weight rows as keys. This is the same framing used to understand why FF layers are the locus of factual knowledge. MoRAM operationalizes it for adaptation: if the pre-trained weight matrix is already a KV store, fine-tuning should add new KV entries rather than perturbing existing ones.

**Minimal-interference skill-stacking.** The wiki's zero-sum-reallocation concern — that installing a new behaviour overwrites capacity used by existing behaviours — is directly addressed by the rank-1 atomic structure. Each new skill occupies its own rank-1 slot. Old slots are frozen. New slots activate only when their key is relevant. This is as close to zero-interference skill-stacking as any LoRA variant has demonstrated. The BWT scores (1.37 on LLaMA-2-7B vs 7–18 for alternatives) are the strongest evidence in the moe-adapters theme that this interference bound is achievable.

**Single-sample regime.** MoRAM is evaluated in multi-task CL; its atomic expansion mechanism is compatible in principle with a one-shot or few-shot per-task regime, though this is not tested. The rank-1 atom added per concept could in principle be learned from a single example if the key captures the right subspace — this is speculative but structurally supported.

## Connections to the Wiki

- [[_overview]] — MoRAM is the key router-free entry in the moe-adapters theme; contrasts with every router-dependent method surveyed
- [[loramoe]] — LoraMoE is the canonical router-based MoE-LoRA; MoRAM's ablation (Table 4) shows external router applied to rank-1 atoms induces retrieval collapse that is *worse* than coarse-grained MoE-LoRA — the router itself is the liability
- [[mole]], [[mov-molora]] — both use external mixture weights; MoRAM eliminates the mixing network in favor of content-addressable scoring
- [[self-moe]] — Self-MoE upcycles dense into MoE via self-distillation; MoRAM also eliminates router but does so for CL rather than upcycling
- [[btx]], [[sparse-upcycling]] — router-dependent upcycling baselines; MoRAM shows the router is dispensable at fine-grained granularity
- [[../catastrophic-forgetting/_overview]] — MoRAM is a primary method for the forgetting theme; BWT ≈ 1–3 across models is the best forgetting result in the wiki
- [[../catastrophic-forgetting/path-not-taken]] — rank-1 atomic experts are structurally adjacent to off-principal sparse updates: both avoid perturbing the principal directions of the pre-trained weight matrix
- [[../selective-finetuning/ff-kv-memories]] — MoRAM's theoretical grounding is the linear associative memory view of weight matrices; rank-1 adapters are new KV entries appended to the existing memory
- [[../selective-finetuning/skill-localization]] — if skills are localized to specific weight subspaces, rank-1 experts that activate only on relevant inputs are a natural implementation
- [[../selective-finetuning/_overview]] — the rank-1 KV framing is a bridge between selective finetuning and adapter-based methods
- [[../synthesis/proposed-method]] — MoRAM's router-free atomic experts are a concrete existence proof for the $R_w$ router-free variant; the BWT numbers ground the interference-suppression claim

## Related

- O-LoRA (TRACE baseline) — orthogonal subspace LoRA; structural forgetting prevention vs MoRAM's content-addressable approach
- HiDeLoRA — hierarchical decomposition LoRA; complex structural expansion vs MoRAM's simple atomic accumulation
- TreeLoRA — tree-structured LoRA expansion; next-best on TRACE but BWT = 3.46–8.50 vs MoRAM's 1.37–3.12
- EWC — parameter regularization; MoRAM outperforms without any regularization loss
- Linear Associative Memory (Kohonen 1972; Hopfield 1982) — theoretical basis for the key-value weight matrix framing
- MoE-Adapter (Yu et al.) — CLIP CL baseline with explicit router; MoRAM outperforms on all X-TAIL metrics
