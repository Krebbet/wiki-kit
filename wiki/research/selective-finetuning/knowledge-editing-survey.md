---
title: "Knowledge Editing for Large Language Models: A Survey"
aliases: ["knowledge-editing-survey", "KME survey", "Wang et al. 2024 KME"]
tags: [selective-finetuning, knowledge-editing, survey, background, locate-then-edit, taxonomy]
source: "Wang, Zhu, Liu, Zheng, Chen, Li — ACM Computing Surveys 2024; arxiv 2310.16218"
theme: selective-finetuning
depth: background
---

# Knowledge Editing for Large Language Models: A Survey

This survey (Wang et al., ACM Computing Surveys 2024) provides the canonical taxonomy and evaluation vocabulary for Knowledge-based Model Editing (KME). KME aims to *precisely* modify a pre-trained LLM to incorporate a specific edit $e = (s, r, o \to o^*)$ without degrading knowledge irrelevant to that edit — a harder constraint than naive fine-tuning, which optimises no locality requirement. The framework unifies disparate methods (ROME, MEMIT, MEND, AlphaEdit, …) under a single constrained optimisation problem and supplies the metric suite this wiki uses for cross-method comparison.

## Source

Wang, Song et al. "Knowledge Editing for Large Language Models: A Survey." *ACM Computing Surveys*, 2024. arXiv:2310.16218. Captured from PDF 2026-05-13.

## Taxonomy

The survey classifies KME methods by *where* and *how* new knowledge enters the model:

| Category | Mechanism | Representative methods | Key trade-off |
|---|---|---|---|
| **External Memorization** | Frozen base weights; new knowledge in auxiliary parameters or memory | SERAC, IKE, GRACE, T-Patcher, MeLLo | Best locality; storage overhead scales with edit count |
| ↳ Memory-based | Cache of edits queried at inference (scope classifier + counterfactual model) | SERAC, IKE, MemPrompt, MeLLo | Gradient-free; struggles with multi-hop |
| ↳ Extension-based | Trainable neurons / adapters appended to FFN layers | CALINET, T-Patcher, GRACE, SWEA | Architecturally clean; limited capacity |
| **Global Optimization** | All parameters updated; constraints prevent collateral damage | MEND, RecAdam, F-Learning, MELO | Best generality; poor locality, slow |
| ↳ Constrained fine-tuning | Regularise $\lVert\phi^* - \phi\rVert \le \delta$ or loss difference | RecAdam, Zhu et al. (Modifying-Memory), RECT, PPA | Straightforward; overfits on small edit sets |
| ↳ Intermediate fine-tuning | Hyper-network $H$ predicts $\Delta\phi$ from gradient $\nabla_\phi \mathcal{L}$ | KE, SLAG, MEND, KGEditor | Efficient inference; hyper-net capacity limits LLM scale |
| **Local Modification** | Locate weight subset $\phi_k$; edit only those | ROME, MEMIT, EMMET, PMET, DINM | Best efficiency; scalability degrades with edit count |
| ↳ Groundtruth-based | Supervision from $y^*$ drives location + closed-form update of $W_2$ (FFN layer 2 as key-value memory $\mathbf{K}\mathbf{W}_2 = \mathbf{V}$) | ROME, MEMIT, EMMET, PMET, DEPN | Canonical locate-then-edit; MEMIT extends to mass edits |
| ↳ Prompt-based | Corruption-restore causal mediation locates $\phi_k$ bottom-up from prompt | MEMITCSK, BIRD | Handles commonsense / bidirectional edits |

**Knowledge neuron view (underpins local modification):** FFN layers act as key-value memories. Given $\mathbf{h}^{(l-1)}$, the two-layer FFN computes $\text{FFN}(\mathbf{h}) = \text{GELU}(\mathbf{h}\mathbf{W}_1)\mathbf{W}_2$. The rows of $\mathbf{W}_1$ function as keys; $\mathbf{W}_2$ functions as the value store. Editing = finding the subject-specific key $\mathbf{k}^*$ and computing a rank-one (ROME) or rank-$u$ (MEMIT) update to $\mathbf{W}_2$.

## Evaluation Criteria

The survey formalises six metrics; this wiki should apply all six when comparing methods:

| Metric | Formal definition | What it tests |
|---|---|---|
| **Accuracy** | $\text{Acc}(f^*;\mathcal{E}) = \mathbb{E}_{e\in\mathcal{E}}\mathbf{1}\{f^*(x_e) = y_e^*\}$ | Edit success on the target prompt |
| **Locality** | $\text{Loc}(f^*, f; \mathcal{O}_\mathcal{E}) = \mathbb{E}_{x\in\mathcal{O}_\mathcal{E}}\mathbf{1}\{f^*(x) = f(x)\}$ | Preservation of unrelated knowledge |
| **Generality** | $\text{Gen}(f^*; e) = \mathbb{E}_{x\in\mathcal{X}_e}\mathbf{1}\{f^*(x) \in \mathcal{Y}_e^*\}$ | Generalisation to paraphrased in-scope inputs |
| **Portability** | $\text{Por}(f^*; \tilde{e})$, where $\tilde{e}$ is logically related (reversed relation, neighbouring relation) | Multi-hop / reasoning-chain propagation |
| **Retainability** | Average per-edit accuracy change across a sequence of edits | Sequential editing stability |
| **Scalability** | $\text{Sca}(M;\mathcal{E}) = \mathbb{E}_{e}\text{Acc}(M(f;\{e\})) - \text{Acc}(M(f;\mathcal{E}))$ | Accuracy drop when editing in batch |

Locality and generality are the axes that define the core tension: optimising one typically hurts the other.

## Method Landscape

Brief status of methods that have or will have dedicated pages in this wiki:

- **[[knowledge-neurons]]** — neuron-attribution precursor; establishes that mid-to-upper FFN neurons store factual associations activatable by subject prompts.
- **[[ff-kv-memories]]** — theoretical grounding; Geva et al. (2021) formalise FFN-as-key-value-memory, underpinning all local-modification methods.
- **[[rome]]** — canonical groundtruth-based locate-then-edit; rank-one update of $\mathbf{W}_2$ in a single critical FFN layer; introduces CounterFact benchmark.
- **[[memit]]** — scales ROME to mass editing ($u$ simultaneous edits across a range of FFN layers); residual-attribution strategy spreads updates to avoid interference.
- **[[mend]]** — intermediate fine-tuning; hyper-network performs low-rank decomposition of fine-tuning gradient to produce $\Delta\phi$ without modifying all parameters.
- **[[alphaedit]]** — local modification variant; projects weight updates into the null space of preserved-knowledge directions to harden locality.

## Strengths

- Unified constrained-optimisation formulation makes the three categories formally comparable, not just qualitatively.
- Six-metric evaluation suite (accuracy, locality, generality, portability, retainability, scalability) is the de-facto community standard — benchmarks CounterFact, zsRE, MQuAKE are all indexed to it.
- Clear delineation of *where* knowledge lives (FFN $\mathbf{W}_2$, not attention) and *how* to reach it (causal mediation for location, closed-form least-squares for update) gives actionable guidance.
- Identifies the fundamental locality–generality trade-off that motivates AlphaEdit's null-space projection and MEMIT's layer-spreading strategy.

## Weaknesses

- Local modification methods degrade with edit count: retainability and scalability both suffer as edits compound in the same parameter subspace.
- Global optimisation methods (MEND, constrained fine-tuning) are model-agnostic but slow and locality-weak.
- Portability (multi-hop propagation) remains an open problem across all three categories; MeLLo's decomposition trick is a workaround, not a principled solution.
- Survey mostly treats factual triples $(s, r, o)$; skill-level or behavioural edits (the concern of [[skill-localization]] and this wiki's project) are not well covered — KME metrics do not straightforwardly transfer to formatting or reasoning behaviour.
- External memorisation methods are gradient-free and locality-safe, but do not update the model's internal weights — the edit is not durable across context windows or fine-tuning passes.

## Relevance to This Wiki's Project

Background depth. The survey defines the vocabulary — locate-then-edit, locality, generality, portability — that underlies the selective-finetuning theme. The proposed method ($R_w$ extension) is asking whether *skill subnetworks* (not individual factual neurons) can be isolated for targeted updates; the KME taxonomy maps the prior work that makes this question precise:

- **External memorisation** corresponds to LoRA / adapter approaches that append parameters without changing base weights — cf. [[o-lora]], [[dora]].
- **Global optimisation** corresponds to standard fine-tuning with regularisation — cf. [[surgical-finetuning]].
- **Local modification** is the direct ancestor of [[rome]], [[memit]], [[alphaedit]], and is the style closest to the wiki's core interest in weight-level isolation.

The locality metric is essentially $R_w$'s constraint: edits to skill $k$ must not shift skill $j \neq k$. The portability metric maps to the generalisation arm of concept-curriculum evaluation.

## Connections to the Wiki

- [[rome]] — canonical locate-then-edit; groundtruth-based local modification.
- [[memit]] — mass-edit extension of ROME; scalability benchmark.
- [[mend]] — intermediate fine-tuning; hyper-network gradient transformation.
- [[alphaedit]] — null-space projection to harden locality.
- [[knowledge-neurons]] — neuron-attribution precursor to local modification.
- [[ff-kv-memories]] — FFN-as-key-value-memory theoretical foundation.
- [[skill-localization]] — skill-level analogue; moves from individual fact neurons to behavioural subnetworks.
- [[lima]] — format-vs-knowledge separation; touches the external-memorisation intuition (instruction format lives in a thin layer, not deep in weights).
- [[surgical-finetuning]] — constrained fine-tuning in the global-optimisation category.
- [[o-lora]], [[dora]] — extension-based external memorisation at skill granularity.
- [[pit]] — instruction-then-CPT as alternative to direct weight editing.
- [[packnet]], [[hat]] — mask-based isolation; structural analogue to the local-modification locality constraint.
- [[../synthesis/proposed-method]] — $R_w$ extension; survey defines the locate-then-edit landscape that motivates the project.
- [[../decoding-time-steering/_overview]] — decoding-time analogues of external memorisation (no weight change).
- [[../concept-learning/_overview]] — concept-as-direction lineage; FFN value vectors as concept directions.

## Related

- Meng et al. 2022 — ROME (CounterFact; rank-one update)
- Meng et al. 2023 — MEMIT (mass editing)
- Mitchell et al. 2022 — MEND (gradient decomposition hyper-network)
- Geva et al. 2021 — Transformer FFN as key-value memories ([[ff-kv-memories]])
- Dai et al. 2022 — Knowledge neurons in pretrained transformers ([[knowledge-neurons]])
- EWC / PackNet / HAT — catastrophic-forgetting literature that the locality constraint recapitulates
