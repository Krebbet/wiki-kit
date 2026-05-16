---
name: dora
description: DoRA decomposes each pretrained weight into a magnitude scalar and a directional matrix, then applies LoRA only to the direction — factoring updates into two orthogonal modes that together recover full-fine-tuning's learning pattern (ICML 2024 Oral).
type: research
---

# DoRA: Weight-Decomposed Low-Rank Adaptation

Liu, Wang, Yin, Molchanov, Wang, Cheng & Chen (ICML 2024 Oral; NVIDIA + HKUST) identify a structural reason LoRA lags behind full fine-tuning (FT): the two methods exhibit fundamentally different patterns of magnitude and direction update relative to the pretrained weights. LoRA shows a strong positive correlation between the two (correlation +0.83), meaning it cannot easily make a large directional change with a small magnitude change or vice versa. FT shows a negative correlation (−0.62), allowing fine-grained independent adjustment of each mode. **DoRA** resolves this by decomposing every weight matrix into a magnitude vector $m$ and a directional matrix $V/\|V\|_c$, then applying a LoRA-style low-rank adapter exclusively to the direction while leaving magnitude as a free scalar. This recovers the FT learning pattern (DoRA correlation −0.31) without any inference overhead — the adapted weight merges back exactly as standard LoRA does.

## Source

- arXiv: 2402.09353
- ICML 2024 Proceedings, Vol. 235
- Raw markdown: `raw/research/selective-finetuning/12-13-dora.md`
- Code: https://github.com/NVlabs/DoRA

## Method

**Weight decomposition.** Any weight matrix $W \in \mathbb{R}^{d \times k}$ is written as:

$$W = m \cdot \frac{V}{\|V\|_c}$$

where $m \in \mathbb{R}^{1 \times k}$ is a row of per-column magnitude scalars, $V \in \mathbb{R}^{d \times k}$ is the directional matrix, and $\|\cdot\|_c$ denotes the column-wise vector norm. Each column of $V/\|V\|_c$ is a unit vector; the corresponding entry in $m$ sets its scale.

**Initialization.** Starting from pretrained weight $W_0$, set $m = \|W_0\|_c$ and $V = W_0$. This ensures $W' = W_0$ before any gradient step.

**DoRA update.** LoRA's low-rank delta $\Delta V = BA$ ($B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$, $r \ll \min(d,k)$) is applied only to the direction:

$$W' = m \cdot \frac{W_0 + BA}{\|W_0 + BA\|_c}$$

Trainable parameters: $m$ (scalar per column, $\sim 1 \times k$) and the LoRA matrices $B, A$. The pretrained $W_0$ is frozen. At inference, $W'$ merges to a full-rank matrix — no added latency over LoRA.

**Gradient geometry.** The gradient w.r.t. the directional update is:

$$\nabla_{V'} \mathcal{L} = \frac{m}{\|V'\|_c} \left(I - \frac{V' V'^T}{\|V'\|_c^2}\right) \nabla_{W'} \mathcal{L}$$

The scaling $m/\|V'\|_c$ and the projection away from $V'$ together improve gradient covariance conditioning — the same effect that motivates Weight Normalization (Salimans & Kingma 2016). Because $V' = V + \Delta V$, this improvement is fully inherited by the LoRA delta $\Delta V$.

**Gradient analysis of the negative-slope pattern.** For a weight vector with a smaller directional update ($S_1$) vs. a larger one ($S_2$) at equal update norm, the cosine of the gradient with the current direction is larger in $S_1$. The magnitude gradient $\nabla_{m^*}\mathcal{L} = \|\nabla_{w'}\mathcal{L}\| \cdot \cos(\nabla_{w'}\mathcal{L}, v)$ is therefore larger in $S_1$ than in $S_2$ — so smaller direction change implies larger magnitude change, producing the negative correlation that characterises FT.

**Memory reduction.** Treating $\|V + \Delta V\|_c$ as a stop-gradient constant during backprop removes the extra gradient graph introduced by the decomposition. This cuts training memory by ~24% on LLaMA-7B and ~12% on VL-BART with negligible accuracy impact ($\le 0.2$ points).

## Claims

All numbers from paper tables; baselines are standard LoRA unless noted.

- **LLaMA-7B commonsense reasoning (8 tasks avg):** DoRA 78.4 vs. LoRA 74.7 (+3.7); DoRA† (rank halved) 77.5 vs. LoRA 74.7 (+2.8) with half the trainable parameters. Surpasses ChatGPT zero-shot CoT (77.0).
- **LLaMA-13B commonsense avg:** DoRA 81.5 vs. LoRA 80.5 (+1.0); DoRA† 80.8 vs. LoRA 80.5 with $\sim 0.35\%$ params (vs. Parallel adapter's 2.89%).
- **LLaMA2-7B commonsense avg:** DoRA 79.7 vs. LoRA 77.6 (+2.1); DoRA† 80.5 (+2.9).
- **LLaMA3-8B commonsense avg:** DoRA 85.2 vs. LoRA 80.8 (+4.4); DoRA† 85.0 (+4.2).
- **VL-BART image-text understanding (4 tasks avg):** DoRA 77.4 vs. LoRA 76.5 (+0.9), matching FT (77.3) at 5.96% params.
- **VL-BART video-text understanding (4 tasks avg):** DoRA 85.4 vs. LoRA 83.5 (+1.9); both below FT (87.5) but DoRA closes half the gap.
- **LLaVA-1.5-7B visual instruction tuning (7-task avg):** DoRA 67.6 vs. LoRA 66.9 (+0.6) and FT 66.5 — DoRA exceeds FT at 4.63% params.
- **DoRA direction/magnitude correlation:** −0.31, vs. FT −0.62 and LoRA +0.83. Directional and magnitude deviations from $W_0$ are both smaller under DoRA than LoRA (Figure 3), consistent with the hypothesis that a strong pretrained prior requires only small, targeted adjustments.
- **Composability:** DoRA is compatible with VeRA (shared frozen random matrices) and achieves further gains, confirming the decomposition is orthogonal to the low-rank structure chosen for $\Delta V$.

## Strengths

- **Structural, not heuristic.** The decomposition follows directly from Weight Normalization reparameterization; the motivation is mathematical (gradient conditioning) and empirically confirmed (correlation sign matches FT).
- **Zero inference cost.** Merged weight $W' \in \mathbb{R}^{d \times k}$ — same shape as $W_0$. No adapter branches or hook layers at deploy time.
- **Broadly compatible.** Works on LLM (LLaMA family), LVLM (LLaVA), multimodal encoder-decoder (VL-BART); NLP and vision-language domains.
- **Parameter-efficient direction.** DoRA† beats LoRA with half the rank, suggesting the decomposition recovers capacity that LoRA wastes on entangled magnitude-direction updates.
- **Interpretable update modes.** Magnitude and direction are semantically distinct: magnitude scaling adjusts a feature's overall strength; direction rotation reorients which feature is expressed. This makes the parameter roles explicit, not implicit in a joint low-rank delta.

## Weaknesses

- **Extra scalar parameters.** $m$ adds $k$ scalars per adapted weight matrix (one per column). Marginal (~0.01% extra params) but non-zero.
- **Memory overhead during training.** The stop-gradient approximation reduces but does not fully eliminate the extra backprop memory from the projection term. Still higher than vanilla LoRA.
- **No layer-selectivity analysis.** The paper does not systematically investigate which layers benefit most from decoupled magnitude vs. direction updates — a tuning granularity ablation is noted but not exhaustive.
- **Correlation analysis is post-hoc.** The negative-slope observation motivates the design but is confirmed empirically rather than derived from first principles about what FT should look like.

## Relevance to this wiki's project

DoRA is the cleanest structural demonstration that **different kinds of weight update live in separable network components**. Magnitude scaling and direction rotation are orthogonal modes — the decomposition $W = m \cdot V/\|V\|_c$ makes this explicit at the matrix level. This directly answers the anchoring question "isolate different parts of the network for different operations": DoRA shows the operation can be factored *within* a single weight matrix, not just across layers or modules.

For the proposed method ($R_w$ — weight-region adapters; [[../synthesis/proposed-method]]), DoRA provides a theoretical scaffold: if a concept's representation decomposes into magnitude (how strongly a feature fires) and direction (which feature fires), single-sample learning might need to update only one mode while freezing the other. An example with a strong prior might need only a magnitude nudge; a genuinely new concept might need a directional shift. DoRA's empirical finding that FT uses both modes independently — and that giving LoRA this freedom recovers FT capacity — is evidence that mode-isolation is mechanistically real, not a design fiction.

## Connections to the wiki

**Within selective-finetuning theme:**
- [[o-lora]] — O-LoRA enforces orthogonality between task LoRA subspaces; DoRA factors within a single weight's update. Complementary structural constraints, different granularity.
- [[skill-localization]] — Sparse-subset localisation by module/neuron vs. DoRA's structured decomposition within each weight. Both answer "where does learning live?" at different resolution.
- [[rome]], [[memit]], [[alphaedit]], [[mend]] — Rank-1 / low-rank edits to $W_{\text{proj}}$; DoRA decomposes the *pretrained weight itself* rather than injecting a delta into an associative memory. Conceptually adjacent but mechanistically distinct.
- [[knowledge-neurons]], [[ff-kv-memories]] — Value-vector view of MLP weights; DoRA's direction corresponds loosely to which key-value associations are expressed, magnitude to how strongly.
- [[lima]], [[surgical-finetuning]] — Both argue that small, targeted updates to a well-pretrained model suffice; DoRA provides the formal mechanism explaining why: magnitude and direction adjustments are largely decoupled in FT, so the model can make minimal changes of each independently.
- [[pit]], [[packnet]], [[hat]] — Continual learning with parameter isolation; DoRA's two-mode decomposition could in principle lock one mode per task.
- [[knowledge-editing-survey]] — Survey context for weight-level editing; DoRA sits in the PEFT-as-editing family.

**Existing wiki cross-theme:**
- [[../synthesis/proposed-method]] — $R_w$ weight-region adapters: DoRA's magnitude/direction split is a concrete instance of orthogonal update modes within one region; informs how to parameterize per-region adapters.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — RL selectively updates 5–30% of weights; DoRA shows that even within the updated weights, update type (magnitude vs. direction) matters — both sparsity and update-mode decomposition are operative.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER uses rank-32 LoRA; DoRA is a drop-in improvement for any LoRA within that pipeline.
- [[../decoding-time-steering/repe]] — RepE uses LoRA fine-tuning toward contrast-vector targets; DoRA's directional adapter is directly applicable — steering toward a contrast direction is a direction update, and DoRA makes that cleaner by isolating it from magnitude drift.

## Related

- [[o-lora]]
- [[skill-localization]]
- [[rome]]
- [[memit]]
- [[alphaedit]]
- [[mend]]
- [[knowledge-neurons]]
- [[ff-kv-memories]]
- [[lima]]
- [[surgical-finetuning]]
- [[pit]]
- [[packnet]]
- [[hat]]
- [[knowledge-editing-survey]]
- [[../synthesis/proposed-method]]
- [[../rlvr-mechanics/rl-sparse-subnetwork]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../decoding-time-steering/repe]]
