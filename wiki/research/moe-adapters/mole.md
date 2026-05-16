---
tags: [moe-adapters, lora-composition, parameter-efficient, gating, v-and-l, nlp]
arXiv: "2404.13628"
venue: ICLR 2024
authors: "Wu, Huang, Wei (Microsoft Research Asia / Tsinghua)"
date_added: 2026-05-16
---

# Mixture of LoRA Experts (MoLE)

Wu et al. (ICLR 2024) propose **MoLE**, a LoRA-composition method that treats each layer of independently-trained LoRAs as a distinct expert and learns a per-layer gating function to mix them. Unlike linear arithmetic merging (which dilutes individual LoRA identity) or reference tuning (which requires full-model retraining), MoLE freezes all LoRA and base-model weights and trains only the gating parameters — minimal overhead, retrain-free composition.

## Source

- arXiv: 2404.13628; ICLR 2024
- Raw: `../../../raw/research/moe-adapters/05-06-mole.md`
- Code: https://github.com/yushuiwx/MoLE

## Method

### Motivating observations

1. **Arithmetic merging degrades identity.** Direct composition ($\hat{W} = W + \sum_i \Delta W_i$) corrupts the base model when $N \geq 3$; normalised merging ($\sum_i w_i \Delta W_i,\; \sum w_i=1$) protects the base but washes out individual LoRA characteristics as each $w_i \to 1/N$.
2. **Layers encode distinct features.** In V&L, LoRA layers at different depths encode separable visual attributes (coat colour vs. facial structure). In NLP (FLAN-T5), layers 0–20% of depth best handle QNLI, 40–60% handle ANLI-R2, 80–100% handle ANLI-R1. ⟹ global composition weights are suboptimal; *per-layer* weights are warranted.

### Hierarchical weight control

Given a pre-trained block $\theta$ and $N$ trained LoRA deltas $\{\Delta\theta_i\}$, MoLE computes the output of each LoRA independently:

$$E_{\Delta\theta_i}(x) = x'_{\Delta\theta_i} + f_\text{FFN}(\text{LN}(x'_{\Delta\theta_i});\,\Delta\theta_i)$$

These outputs are concatenated, normalised, and projected to gate logits:

$$\mathbf{E}_\Omega(x) = \text{Norm}\!\left(E_{\Delta\theta_0}(x) \oplus \cdots \oplus E_{\Delta\theta_{N-1}}(x)\right), \quad \mathbf{E}_\Omega \in \mathbb{R}^\xi,\; \xi = N \times L \times d$$

$$\varepsilon = \text{Flatten}(\mathbf{E}_\Omega(x))^\top \cdot \mathbf{e}, \quad \varepsilon \in \mathbb{R}^N$$

where $\mathbf{e} \in \mathbb{R}^{\xi \times N}$ is a learnable parameter. Gate weights are a temperature-scaled softmax:

$$G(\varepsilon_i) = \frac{\exp(\varepsilon_i / \tau)}{\sum_{j=1}^{N} \exp(\varepsilon_j / \tau)}$$

with learnable temperature $\tau$. The composed output is:

$$\tilde{E}_\Omega(x) = \sum_{i=0}^{N} G(\varepsilon_i) \cdot E_{\Delta\theta_i}(x)$$

and the final block output adds the base model:

$$O(x) = F_\theta(x) + \tilde{E}_\Omega(x)$$

Only $\mathbf{e}$ and $\tau$ (per layer) are trained; all LoRAs and $\theta$ are frozen.

### Gating balancing loss

Without regularisation the gating collapses — one early-performing LoRA captures ~68% of the gate weight. A balancing loss counters this:

$$\mathcal{L}_\text{balance} = -\log \prod_{i=0}^{N} \bar{q}^{(i)}, \qquad \bar{q}^{(i)} = \frac{1}{M}\sum_{k=1}^{M} G\!\left(\varepsilon^{(k)}_i / \tau\right)$$

where $M$ is the number of gated blocks. Combined loss: $\mathcal{L} = \mathcal{L}_D + \alpha\,\mathcal{L}_\text{balance}$ ($\alpha=0.5$ in experiments).

### Two inference modes

1. **Standard mode:** all $N$ LoRAs active with learned gate weights.
2. **Masking mode:** manually zero out unwanted LoRAs and renormalise remaining weights proportionally — no retraining required. Allows subset selection or single-LoRA extraction from the trained gate.

### Gating granularity

Four granularity levels were tested: matrix-wise (m-MoLE), layer-wise (l-MoLE), block-wise (b-MoLE), network-wise (n-MoLE). Intermediate granularities (b/l) are best; finest (m) over-controls and breaks intra-LoRA parameter relationships; coarsest (n) has too few optimisable parameters.

## Claims

- **V&L (Stable Diffusion v2.1, DreamBooth base):** Composing 3 visual-concept LoRAs across 15 subject triplets, MoLE averages text-alignment 0.759 vs. SVDiff 0.728 vs. NLA 0.678; image-alignment (concept 1) 0.783 vs. 0.746 vs. 0.715. Excels on both metrics simultaneously — unusual given the known text–image alignment trade-off.
- **V&L vs. full-parameter SOTA:** At 3–6 concepts, MoLE text-alignment 0.752 avg outperforms Textual Inversion (0.717) and NLA (0.672); falls slightly short of Custom Diffusion on image-alignment (0.743 vs. 0.760) while being far more lightweight.
- **NLP (FLAN-T5, BBH):** MoLE avg 42.2 EM vs. LoRAHub 38.4 (+3.8) and PEMs 33.2 (+9.0).
- **NLP (Translation):** avg BLEU 26.9 vs. LoRAHub 25.4 (+1.5) and PEMs 24.2 (+2.7).
- **NLP (Struct-to-Text):** avg Rouge 40.3 vs. LoRAHub 38.1 (+2.2) and PEMs 37.7 (+2.6).
- **NLP (NLI):** avg EM 80.5 vs. LoRAHub 79.2 (+1.3) and PEMs 78.8 (+1.7).
- **Scaling:** With 48 and 128 LoRAs, MoLE leads LoRAHub by +2.5 and +3.0 respectively; LoRAHub zeros out many weights at scale. All methods degrade at 128 LoRAs, indicating composition at very large $N$ remains unsolved.
- **Generalisation:** LoRAs trained on NLI tasks, evaluated on BBH: MoLE +2.4 over LoRAHub, +3.7 over PEMs.

## Strengths / Novelty

- **Identity preservation without retraining.** The gate is the only new parameter; each LoRA's weights are untouched and individually recoverable. This directly addresses the dilution failure mode of arithmetic merging.
- **Retrain-free masking mode.** Post-training subset selection via weight redistribution gives practitioners flexibility without the computational cost of reference tuning (Gu et al., Mix-of-Show).
- **Layer-level specificity.** The per-layer gating respects the empirically observed depth-wise feature specialisation inside LoRAs — a qualitatively different inductive bias than global scalar weights (LoRAhub) or uniform normalization.
- **Works across modalities.** Same mechanism validated on text-to-image (V&L) and language (NLP) with only the domain-specific loss $\mathcal{L}_D$ differing.

## Weaknesses / Limits

- **Requires a small training set per target composition.** The gate must be fitted (400–800 iterations) for each desired LoRA combination — not zero-shot. Cost scales with the number of desired compositions.
- **Quadratic gate input size.** The concatenated $\mathbf{E}_\Omega \in \mathbb{R}^{N \times L \times d}$ projection grows with $N$, $L$, and $d$; becomes expensive at large $N$ (already degrading at $N=128$).
- **Not jointly trained.** Individual LoRAs are pre-trained independently, so there is no mechanism for the experts to specialise relative to each other (contrast [[loramoe]] which jointly trains router and LoRAs).
- **Composition-at-inference only.** MoLE is a post-hoc combiner; it cannot adapt base-model features to a new concept mixture.

## Relevance to this wiki's project

MoLE is the *composition primitive* for the delta-LoRA expert family: given $N$ independently-trained task-specific LoRAs (analogous to MoERA's delta-LoRA experts), how do you combine them at inference without destroying what each one learned? The per-layer soft gating is directly applicable as the $R_w$ composition operator in [[../synthesis/proposed-method]]: one could train a gate over a set of concept-specific LoRAs and apply either mode (standard soft gate or masked subset) without retraining the experts.

The key contrast with LoRAMoE ([[loramoe]]): MoLE composes *already-trained* LoRAs post-hoc; LoRAMoE trains experts and a router jointly from scratch. For MoERA, where experts may be added incrementally (single-sample, one concept at a time), MoLE's post-hoc composability is more practical — no re-training of prior experts when a new one is added.

The masking mode is also relevant to catastrophic forgetting ([[../catastrophic-forgetting/_overview]]): old-concept LoRAs can be preserved and selectively gated in or out rather than merged into a single weight update.

## Connections to the wiki

- [[loramoe]] — jointly-trained router alternative; different regime (train-time vs. post-hoc), different scaling properties
- [[mov-molora]] — another architecture in the composed-adapter family
- [[self-moe]] — self-specialisation approach vs. MoLE's external expert composition
- [[btx]] — branch-then-expert paradigm; compare expert construction strategies
- [[sparse-upcycling]] — densely-pretrained model → sparse MoE; composition at a coarser level
- [[moram]] — MoRA variant in this theme; contrast adapter rank vs. composition
- [[_overview]] — moe-adapters theme overview
- [[../selective-finetuning/o-lora]] — orthogonal LoRA per task; MoLE composes rather than orthogonalises
- [[../selective-finetuning/dora]] — DoRA decomposes LoRA updates; complementary decomposition perspective
- [[../selective-finetuning/_overview]] — selective fine-tuning context
- [[../synthesis/proposed-method]] — $R_w$ composition operator; MoLE is a direct candidate instantiation
- [[../catastrophic-forgetting/_overview]] — masking mode provides selective forgetting mitigation

## Related

- Wu et al. 2024 — arXiv 2404.13628 (this paper)
- Huang et al. 2023 — LoRAhub (gradient-free weight estimation baseline)
- Zhang et al. 2023 — PEMs (arithmetic operator baseline for NLP)
- Han et al. 2023 — SVDiff (arithmetic baseline for V&L)
- Gu et al. 2023 — Mix-of-Show / reference tuning-based composition (the high-cost alternative)
