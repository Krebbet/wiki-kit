---
title: "Transformer Feed-Forward Layers Are Key-Value Memories"
authors: "Geva, Schuster, Berant, Levy"
year: 2021
venue: "EMNLP"
theme: selective-finetuning
type: mechanistic-analysis
status: read
tags: [feed-forward, key-value-memory, mechanistic-interpretability, knowledge-localization, layer-analysis]
---

# Transformer Feed-Forward Layers Are Key-Value Memories

Feed-forward (FF) layers account for two-thirds of a transformer's parameters yet were largely unanalysed at the time. Geva et al. show they function as **unnormalized key-value memories**: the first weight matrix $K$ encodes keys that detect input patterns; the second matrix $V$ encodes values that induce distributions over the output vocabulary. Lower layers detect shallow n-gram patterns; upper layers store semantic, concept-level patterns. The layer output is a composition of hundreds of simultaneously active memories, refined across depth via residual connections. This mechanistic story is the theoretical bedrock for all subsequent fact-localization and targeted-editing work.

## Source

Geva, M., Schuster, R., Berant, J., & Levy, O. (2021). Transformer Feed-Forward Layers Are Key-Value Memories. *EMNLP 2021*. [arXiv:2012.14913](https://arxiv.org/abs/2012.14913)

Raw: `/raw/research/selective-finetuning/04-02-ff-kv-memories.md`

## Method

### Feed-forward layer as unnormalized memory

A standard transformer FF layer (bias omitted) is:

$$\text{FF}(\mathbf{x}) = f\!\left(\mathbf{x} \cdot K^\top\right) \cdot V$$

where $K, V \in \mathbb{R}^{d_m \times d}$, $f$ is ReLU, and $d_m$ is the hidden dimension (number of memory cells). This is structurally identical to a key-value neural memory (Sukhbaatar et al., 2015):

$$\text{MN}(\mathbf{x}) = \operatorname{softmax}\!\left(\mathbf{x} \cdot K^\top\right) \cdot V = \sum_{i=1}^{d_m} p(k_i \mid \mathbf{x})\, v_i$$

The only difference is the normalizing softmax vs. unnormalized ReLU. Expanding $\text{FF}(\mathbf{x})$ in the same sum form:

$$\text{FF}(\mathbf{x}) = \sum_{i} \underbrace{\text{ReLU}\!\left(\mathbf{x} \cdot k_i^\top\right)}_{\text{memory coefficient } m_i} \cdot v_i$$

Each scalar $m_i$ is the coefficient gating $v_i$; cells with $m_i = 0$ are inactive (ReLU sparsity). The output is thus a **weighted sum of value vectors $v_i$ over key-matched memories**.

### Intra-layer composition and inter-layer refinement

Within a layer, hundreds of cells are simultaneously active (10–50% of $d_m = 4096$). The layer output typically differs from every individual memory's top prediction — composition, not retrieval from a single cell. Across layers, residual connections act as a refinement mechanism:

$$\mathbf{o}^\ell = \text{FF}(\mathbf{x}^\ell) + \mathbf{r}^\ell, \qquad \mathbf{x}^\ell = \text{LayerNorm}(\mathbf{r}^\ell)$$

The residual carries the running distribution; each FF layer nudges it rather than replacing it. ~⅓ of predictions stabilize by the bottom few layers; most decisions finalize around layer 10+ on the 16-layer model studied.

## Claims

1. **Keys detect human-interpretable input patterns.** For a 16-layer, 247M-parameter LM (WikiText-103), human experts could identify at least one clear pattern for every sampled key, covering 65–80% of that key's top-25 trigger prefixes.
2. **Lower layers (1–9) encode shallow patterns; upper layers (10–16) encode semantic patterns.** Experts classified lower-layer keys as n-gram/surface triggers; upper-layer keys as topic/relational patterns (e.g. "part of" relations, TV-show context). Removing the final token of a prefix disrupts lower-layer coefficients far more than upper-layer ones.
3. **Values in upper layers induce next-token distributions aligned with their key's patterns.** Agreement rate between $\operatorname{argmax}(v_i \cdot E)$ and the next token of $k_i$'s top trigger example rises from ~0% (layers 1–10) to 3.5% (layers 11–16) — orders of magnitude above a random baseline (0.0004%).
4. **Layer output is compositional, not dominated by a single memory.** In ≥68% of examples at every layer, the layer's predicted token differs from the top prediction of every individual active memory cell.
5. **Residual connections implement iterative refinement, not wholesale replacement.** When FF output changes the residual's top prediction, it usually produces a "compromise" token matching neither the residual nor the FF cell — suggesting a probability-mass redistribution, not an override.
6. **The number of active memories dips around layer 10**, the same transition point where semantic patterns become dominant over shallow ones — suggesting a qualitative behavioral shift at mid-depth.

## Strengths

- **Theoretical clarity.** The algebraic equivalence between FF layers and key-value memories (Eq. 1 vs. Eq. 2) is exact; the only gap is normalization. This is not an analogy but a structural identity.
- **Empirical grounding.** Human expert annotation of 160 sampled keys, verified by systematic coefficient-mutation experiments and vocabulary-projection analysis.
- **Layer-resolved picture.** Provides concrete shallow-vs-semantic stratification by depth, enabling principled decisions about which layers to target for which operations.
- **Generality.** The FF-as-KV framing holds for any transformer (encoder, decoder, seq2seq) — not limited to the WikiText-103 LM studied.

## Weaknesses

- **Single model, single domain.** All experiments use a 16-layer adaptive-input LM trained on WikiText-103. Generalization to GPT-2/3 scale, instruction-tuned models, or multilingual settings is asserted but not shown.
- **Correlation, not causation.** Expert annotation identifies patterns correlated with high activation; it does not prove the layer is *causally responsible* for storing that fact (the causal complement is Meng et al.'s causal tracing in ROME).
- **Unnormalized coefficients.** ReLU activations are unbounded; treating $m_i$ as a "probability" is an approximation. The vocabulary-projection of values is explicitly noted to be uncalibrated.
- **Human annotation bottleneck.** Pattern identification relies on NLP PhD students; coverage is limited to 160 keys out of 65,536 ($d_m \cdot 16$). Automated pattern discovery is left as future work.
- **Static analysis.** Examines the trained model; does not study how these memories form during training or how fine-tuning modifies them.

## Relevance to this wiki's project

This paper answers the anchoring question — **how to isolate parts of the network for different operations** — at the mechanistic level.

The key-value memory view converts an opaque weight matrix into a structured address space: each memory cell $(k_i, v_i)$ is a (pattern detector, distribution emitter) pair. This directly enables:

- **Layer selection for edits.** If upper-layer values hold semantic/factual distributions and lower-layer keys hold surface triggers, then editing a fact requires targeting upper FF layers, not lower ones, and not attention. This is the implicit assumption behind ROME's causal tracing (which empirically confirms it) and MEMIT's multi-layer extension.
- **$R_w$ abstraction.** The proposed method's $R_w$ weight-region representation maps cleanly to "the value matrix $V$ of layers $\ell \in \mathcal{L}_\text{semantic}$." Geva et al. provide the theoretical warrant for why that region has the right structure.
- **Single-sample learning.** If a new concept must be injected from one example, the FF key-value view tells you what to rewrite (a small set of upper-layer value vectors) and what not to touch (lower-layer pattern keys, which should remain general). Editing the wrong layer wastes capacity or breaks existing patterns.
- **Surgical fine-tuning rationale.** Papers like [[surgical-finetuning]] and [[skill-localization]] observe empirically that only certain layers need updating for a given task; Geva et al. explain *why* — layers are not interchangeable, they store qualitatively different information.

Without this paper, "edit facts at a specific MLP layer" is an engineering heuristic. With it, there is a principled account: upper-layer value vectors are the write-addresses for factual associations, and the residual stream is the read-out pathway.

## Connections to the wiki

Within selective-finetuning theme:
- [[knowledge-neurons]] — Dai et al. operationalize at the individual neuron (single $i$) level; Geva operates at the layer level. Together they bracket the granularity of fact storage.
- [[rome]] — uses the FF-as-KV result directly: causal tracing targets mid-to-upper FF layers; the rank-1 edit is precisely a value-vector update.
- [[memit]] — extends ROME's single-layer edit to batch updates across multiple upper-layer FF matrices.
- [[alphaedit]] — orthogonal-update editing, same FF target layer rationale.
- [[mend]] — gradient decomposition edits; the key-value structure explains why low-rank updates to $V$ are sufficient.
- [[skill-localization]] — task vectors localized in FF subsets; Geva's layer stratification predicts which subset matters.
- [[lima]] — surface fine-tuning with few examples; works because upper-layer semantics are already encoded, only value emphasis needs shifting.
- [[surgical-finetuning]] — choosing which layers to freeze: Geva's depth-stratification is the mechanistic basis.
- [[o-lora]], [[dora]], [[pit]] — low-rank adaptation methods; applying them to upper FF layers over lower layers is justified here.
- [[packnet]], [[hat]] — parameter-isolation methods; selecting the FF-value subspace as the isolation target follows from Geva.
- [[knowledge-editing-survey]] — Geva (2021) is typically cited as the theoretical foundation chapter.

Cross-theme:
- [[../synthesis/proposed-method]] — $R_w$ weight-region abstraction; this paper defines the mechanistic semantics of that region.
- [[../in-context-learning-theory/induction-heads]] — mechanistic-interp at the attention level; together with Geva, gives a full FF + attention decomposition of transformer computation.
- [[../decoding-time-steering/dola]] — DoLa's layer-contrastive decoding exploits exactly the lower-vs-upper factual content stratification Geva characterizes.
- [[../decoding-time-steering/repe]] — representation engineering targets residual-stream directions; Geva explains what FF layers contribute to those directions.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse subnetwork selection; the FF-key sparsity (10–50% active per forward pass) motivates subnetwork views.

## Related

- Meng et al. (2022) — ROME: causal tracing verifies the upper-FF factual-storage claim with intervention experiments.
- Dai et al. (2022) — Knowledge Neurons: neuron-level granularity within the same FF key framing.
- Sukhbaatar et al. (2015) — End-to-End Memory Networks: the KV-memory architecture Geva maps onto.
- Sukhbaatar et al. (2019) — Augmenting Self-Attention with Persistent Memory: earlier reparameterization observation, less analytic follow-through.
- Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits: complementary mechanistic decomposition at the attention circuit level.
