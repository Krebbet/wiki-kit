---
tags: [selective-finetuning, continual-learning, gradient-masking, background]
source_paper: "Serra et al., ICML 2018 — Overcoming Catastrophic Forgetting with Hard Attention to the Task"
arxiv: "1801.01423"
---

# HAT — Hard Attention to the Task

Serra et al. (ICML 2018) propose learning per-task binary attention masks over network units via SGD, alongside the main task loss. Each task $t$ gets a separate mask; cumulative masks from prior tasks gate weight updates so earlier tasks' parameters are left intact. HAT cuts catastrophic forgetting rates by 45–80% across an 8-dataset sequential image-classification benchmark. It establishes the core primitive — **per-task binary mask learned during training, applied at both forward pass and gradient step** — that later LLM-era continual learning methods extend.

## Source

- arXiv: 1801.01423
- Raw: `../../../raw/research/selective-finetuning/08-11-hat.md`

## Method

**Task embedding → soft gate.** For task $t$, layer $l$ holds a trainable embedding $\mathbf{e}_l^t$. During training the attention vector is:

$$\mathbf{a}_l^t = \sigma(s \, \mathbf{e}_l^t)$$

where $\sigma$ is sigmoid and $s > 0$ is a scaling parameter. At inference $s = s_{\max} \gg 1$, so $\sigma$ approximates a unit step and $\mathbf{a}_l^t \in \{0,1\}^{N_l}$.

**Annealing schedule.** Within each epoch, $s$ is linearly annealed over batches $b = 1, \ldots, B$:

$$s = \frac{1}{s_{\max}} + \left(s_{\max} - \frac{1}{s_{\max}}\right) \frac{b-1}{B-1}$$

Starting near $s \approx 0$ makes all units equally active at epoch start; ending at $s_{\max}$ polarises the mask toward $\{0,1\}$ by epoch end.

**Forward pass.** Attended activations: $\mathbf{h}_l' = \mathbf{a}_l^t \odot \mathbf{h}_l$. The last layer uses a hard-coded binary head per task (standard multi-head).

**Gradient masking (backward pass).** After training task $t$, the cumulative mask is:

$$\mathbf{a}_l^{\leq t} = \max\!\left(\mathbf{a}_l^t,\, \mathbf{a}_l^{\leq t-1}\right) \quad \text{(element-wise)}$$

When training task $t{+}1$, the gradient $g_{l,ij}$ for weight connecting unit $j$ (layer $l{-}1$) to unit $i$ (layer $l$) is masked:

$$g_{l,ij}' = \left(1 - \min\!\left(a_{l,i}^{\leq t},\, a_{l-1,j}^{\leq t}\right)\right) g_{l,ij}$$

Units with high cumulative attention (important for prior tasks) receive near-zero gradient updates — a hard freeze via mask multiplication, not via a loss penalty.

**Capacity regularisation.** To reserve capacity for future tasks, an attention-weighted $L_1$ term is added to the loss:

$$R\!\left(\mathbf{A}^t, \mathbf{A}^{<t}\right) = \frac{\sum_{l,i} a_{l,i}^t \left(1 - a_{l,i}^{<t}\right)}{\sum_{l,i} \left(1 - a_{l,i}^{<t}\right)}$$

Units already used by prior tasks are excluded from the penalty; $c \geq 0$ scales the term.

## Claims

- Cuts catastrophic forgetting by 45–80% vs. baselines (EWC, SI, PackNet, PathNet, PNNs) on 8-task random-order image classification (Sec. 1, Abstract).
- Mask learning requires no separate stage — embeddings $\mathbf{e}_l^t$ are trained jointly with network weights via backprop (Sec. 2.2).
- Hard masking is unit-based, not weight-based: the mask structure is lightweight; weight-level masking is derived automatically (Sec. 2.3).
- $s_{\max}$ controls the stability–plasticity tradeoff: small $s_{\max}$ → soft sigmoid → allows forgetting; large $s_{\max}$ → near-binary → hard freeze (Sec. 2.4).
- Robust to hyperparameter choices; only two meaningful hyperparameters: $s_{\max}$ (stability) and $c$ (compressibility) (Sec. 4).

## Strengths

- Clean primitive: no heuristic pruning ratios (vs. PackNet), no evolutionary search (vs. PathNet), no post-training importance estimation (vs. EWC).
- Gradient masking is exact and differentiable during training — masks participate in backprop.
- Compressibility constant $c$ gives explicit control over capacity per task.

## Weaknesses

- **Task identity required at inference.** The correct mask $\mathbf{a}_l^t$ must be selected at test time; no mechanism for inferring task ID from input.
- **Vision-era architecture.** Evaluated on AlexNet-style CNNs on small image datasets; not demonstrated on transformers or language tasks.
- **Bounded capacity.** Once all units are saturated by prior masks, no room remains for new tasks — capacity management is manual.
- **Sequential-only.** Assumes strict task boundaries; not designed for continual streams without clear task delineation.

## Relevance to This Wiki's Project

HAT is background depth: it established the **per-task binary mask via SGD** primitive. The proposed method's $R_w$ weight-restriction component ([[../synthesis/proposed-method]]) inherits this lineage — selectively blocking gradient updates to preserve prior knowledge. The LLM-era extensions ([[o-lora]], [[skill-localization]]) replace the unit-level binary mask with parameter-subspace constraints better suited to transformer weight matrices, but the core idea (gradient masking conditioned on prior task masks) is HAT's contribution.

## Connections to the Wiki

- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC uses Fisher-weighted soft regularisation on the loss; HAT uses hard gradient masking; both mitigate forgetting but HAT's freeze is more absolute.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov finds RL naturally activates a sparse subnetwork per task, structurally analogous to HAT's learned mask but discovered post-hoc rather than trained concurrently.
- [[../synthesis/proposed-method]] — $R_w$ is the direct descendant: selective gradient blocking for weight preservation in single-sample concept updates.

## Related

- [[packnet]] — CVPR sibling; both do per-task gradient masking, but PackNet uses heuristic weight pruning with pre-assigned ratios where HAT uses learned unit-level masks.
- [[o-lora]] — LLM-era descendant; orthogonal LoRA subspaces enforce task separation in weight-update space, replacing binary unit masks.
- [[skill-localization]] — sparse mask extracted post-hoc via activation analysis; HAT learns it during training.
- [[surgical-finetuning]] — selective layer updating; complements HAT's unit-level selectivity with layer-level analysis.
- [[pit]] — parameter-isolated tuning; same isolation goal in the LoRA-era.
- [[dora]] — weight decomposition for efficient adaptation; contrasts HAT's masking approach.
- [[knowledge-editing-survey]], [[rome]], [[memit]], [[alphaedit]], [[mend]], [[knowledge-neurons]], [[ff-kv-memories]] — knowledge editing methods that locate and update specific parameters; HAT instead prevents overwriting via masking.
- [[lima]], [[surgical-finetuning]] — data-efficient finetuning context.
