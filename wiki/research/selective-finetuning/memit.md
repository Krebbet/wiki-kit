---
title: "MEMIT — Mass-Editing Memory in a Transformer"
aliases: ["MEMIT", "mass-editing memory"]
tags: [selective-finetuning, knowledge-editing, weight-surgery, mlp-memories, scaling]
source: "Meng et al., ICLR 2023 — https://arxiv.org/abs/2210.07229"
---

# MEMIT — Mass-Editing Memory in a Transformer

MEMIT (Meng et al., 2023) scales [[rome|ROME]]'s single-fact weight surgery to thousands of simultaneous edits by distributing parameter updates across a *range* of causally implicated MLP layers rather than a single layer. The central insight is that factual recall is mediated by a contiguous band of mid-layer MLPs acting jointly on the last subject token; spreading residual corrections evenly across that band minimises per-layer weight perturbation and preserves unedited behaviour. MEMIT is the cleanest existence proof that surgical, interpretability-grounded weight edits can scale—a direct template for the question of whether SFT signal can be injected selectively without touching format, fluency, or reasoning tokens.

## Source

Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau. **"Mass-Editing Memory in a Transformer."** ICLR 2023. [arXiv:2210.07229](https://arxiv.org/abs/2210.07229). Code/data: memit.baulab.info.

## Method

**Causal localisation.** Causal mediation analysis on GPT-J (6B) identifies a range of critical MLP layers $\mathcal{R}$ (layers 3–8 for GPT-J) that jointly mediate factual recall at the last subject token $S$. Unlike ROME, which targets a single layer, MEMIT selects the entire range.

**Residual-stream decomposition.** The final hidden state decomposes as:

$$h_i^L = h_i^0 + \sum_{l=1}^{L} a_i^l + \sum_{l=1}^{L} m_i^l$$

Each MLP $m_i^l$ adds independently to the residual stream, so corrections can be distributed across all $l \in \mathcal{R}$ without double-counting.

**Per-layer batch update (the core equation).** Treating $W_{\text{out}}^l$ as a linear associative memory with pre-existing key covariance $C_0 = \lambda \cdot \mathbb{E}_k[kk^\top]$, the optimal weight delta for a batch of $u$ new associations with keys $K_1$ and residuals $R = M_1 - W_0 K_1$ is:

$$\Delta^l = R^l {K^l}^\top \!\left(C_0^l + K^l {K^l}^\top\right)^{-1}$$

$C_0^l$ is precomputed once from an empirical input sample; $\lambda \approx 1.5 \times 10^4$ balances old vs. new associations.

**Two-phase algorithm.**

1. *Compute target vectors $z_i$.* For each edit $(s_i, r_i, o_i)$, optimise a residual $\delta_i$ by gradient descent so that substituting $z_i = h_i^L + \delta_i$ into layer $L$ causes the model to predict $o_i$ across $P$ random-prefix paraphrase prompts (aids generalisation).

2. *Spread $z_i - h_i^L$ over $\mathcal{R}$ iteratively.* Layer by layer in ascending order, assign each layer a $\frac{1}{L - l + 1}$ fraction of the remaining residual, apply Eq. $\Delta^l$ above, then re-collect activations before proceeding to the next layer. This corrects for the fact that earlier layer edits shift downstream activations.

No meta-learned hypernetwork is required; every quantity is computed analytically or by short local optimisation.

## Claims

- MEMIT successfully edits **10,000 zsRE facts on GPT-J (6B)**: Efficacy 96.7 %, Paraphrase 89.7 %, Specificity 26.6 %, composite Score 50.7—outperforming ROME (2.6), MEND (20.0), and fine-tuning with weight decay FT-W (42.1).
- On COUNTERFACT at 10,000 edits (GPT-J): MEMIT Score 85.8 vs. ROME 50.3, MEND 23.1, FT-W 67.6; fluency (GE) preserved near baseline (619.9 vs. 622.4); consistency (RS) 40.1 vs. baseline 29.4.
- MEMIT scales to **GPT-NeoX (20B)** with comparable performance: Score 82.0, Efficacy 97.2 %, Specificity 70.8 %.
- ROME degrades at $n \geq 32$ edits; MEND loses all efficacy before $n = 1{,}000$; MEMIT maintains high score across the entire log-scale curve up to $n = 10{,}000$.
- FT-W achieves high probability-based efficacy but causes **complete generation failure** (GE collapses to 293.9 vs. baseline 622.4), confirming that naive fine-tuning damages fluency even when facts are recalled.
- Performance on mixed-relation batches is near the linear average of individual-relation runs, indicating **no interference penalty** from diversity of edits.
- Some relations remain hard (e.g., athlete's sport), but MEMIT outperforms all baselines even on hard cases.
- The $z_i$ optimisations are embarrassingly parallel; the reported 7.4 hr wall-clock for 10,000 edits is a naive serial implementation.

## Strengths

- **Closed-form weight update** — no auxiliary network, no meta-training; edits are computed analytically from a stored covariance statistic.
- **Layer-load balancing** — distributing the residual across $|\mathcal{R}|$ layers keeps per-layer $\|\Delta^l\|$ small, which empirically preserves specificity and fluency better than concentrating change in one layer.
- **Interpretability-grounded** — targets are chosen by causal tracing, not heuristic; the method is auditable.
- **Scale demonstrated** — 100× improvement over prior state-of-the-art in number of simultaneous edits, on production-scale models (6B, 20B).
- **Fluency preserved** — unlike FT-W, generation entropy stays near baseline even at 10,000 edits.

## Weaknesses

- **MLP-only; no attention editing** — factual storage in attention layers or in very early/late MLPs is ignored; some facts may not localise cleanly to $\mathcal{R}$.
- **Flat (s, r, o) representation** — spatial, temporal, mathematical, procedural, and symmetric relations are out of scope; "Tim Cook is CEO of Apple" and "The CEO of Apple is Tim Cook" must be edited separately.
- **Prompt sensitivity** — like ROME, success depends on the templated prompt $p(s, r)$; arbitrary phrasing is only partially handled through paraphrase prefixes.
- **Covariance proxy** — $C_0 = \lambda \mathbb{E}[kk^\top]$ is an approximation; the true pre-training key distribution is unknown, and $\lambda$ requires tuning.
- **No multi-hop consistency** — editing one fact does not automatically cascade to logically dependent facts.
- **Runtime** — even with parallelisation, editing thousands of facts requires hours on A6000-class hardware.
- AlphaEdit ([[alphaedit]]) later shows that projecting $\Delta$ onto the null space of preserved knowledge further reduces collateral damage, which MEMIT does not do.

## Relevance to this wiki's project

The anchoring question for this wiki is: *how to inject new SFT signal that boosts capacity without degrading response format, language, or thinking tokens?*

MEMIT is the sharpest existence proof that **selective weight surgery scales**. Key implications:

1. **Isolate by layer, not by loss.** MEMIT shows that causal tracing can identify *which* MLP layers carry a specific type of information. By analogy, one could trace which layers carry format/language behaviour and which carry factual/reasoning content, then apply gradient updates only to the latter—the MEMIT update equation is the template.

2. **The $\Delta^l$ formula is directly reusable.** If we want to inject a new reward signal (e.g., from a single-sample SFT example) into a specific layer range without moving other layers, $\Delta^l = R{K}^\top (C_0 + K K^\top)^{-1}$ is the closed-form update. $C_0$ can be precomputed offline from a representative input corpus.

3. **Distributing across layers reduces per-layer damage.** For $R_w$ extension in [[../synthesis/proposed-method]], this suggests spreading the write update across the causal band rather than concentrating it at the single most-activated layer.

4. **FT-W's fluency collapse is a warning.** Naive fine-tuning—even with weight decay—destroyed generation quality at scale (GE halved). Any SFT regime that does not localise updates risks exactly this failure mode on thinking tokens or format tokens.

5. **Scale-invariance of the method.** The per-edit cost is $O(d^2)$ for a closed-form solve, not a full backward pass; this is cheap enough to consider per-batch or per-step selective updates during a training run.

## Connections to the wiki

Within the selective-finetuning theme:
- [[rome]] — direct ancestor; MEMIT replaces ROME's single-layer rank-one constraint with a multi-layer batch update.
- [[knowledge-neurons]] — earlier empirical localisation work that MEMIT supersedes with causal tracing.
- [[ff-kv-memories]] — theoretical grounding for treating MLP layers as key-value memories, the conceptual basis of the $\Delta^l$ derivation.
- [[mend]] — hypernetwork baseline that MEMIT consistently outperforms at $n \geq 6$.
- [[alphaedit]] — successor that adds null-space projection to further protect unedited knowledge.
- [[skill-localization]] — complementary approach localising *skills* rather than facts; the two can be combined.
- [[lima]] — shows that a small set of high-quality examples suffices for alignment; MEMIT-style surgery could be the write mechanism for those examples.
- [[surgical-finetuning]] — gradient-based counterpart to MEMIT's analytic approach.
- [[o-lora]], [[dora]], [[pit]] — low-rank/structured alternatives; MEMIT's closed-form is rank-$u$ but targets specific layers.
- [[packnet]], [[hat]] — continual-learning masking methods; MEMIT achieves analogous preservation by explicit covariance regularisation.
- [[knowledge-editing-survey]] — comprehensive taxonomy placing MEMIT in context.

Existing wiki cross-references:
- [[../synthesis/proposed-method]] — $R_w$ extension: MEMIT demonstrates that surgical writes scale, validating the hypothesis that capacity injection need not be global.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — RLVR reward signals activate sparse subnetworks; MEMIT suggests those subnetworks could be written to directly rather than discovered through RL.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — the question of *which* parameters to update during RL aligns with MEMIT's causal-localisation answer for knowledge.
- [[../self-play/invisible-leash]] — if the leash constrains output format, MEMIT-style layer targeting could enforce it at the weight level rather than through reward shaping.
- [[../decoding-time-steering/_overview]] — activation-level steering is the inference-time analogue; MEMIT is the weight-level, persistent version.
- [[../concept-learning/_overview]] — concept representations may localise to the same MLP band MEMIT targets; surgical injection of concept-specific capacity is a natural extension.

## Related

- Meng et al. 2022 (ROME) — single-edit rank-one precursor.
- Mitchell et al. 2022 (MEND, SERAC) — hypernetwork-based baselines.
- Dai et al. 2022 — sparse neuron editing; contrasted with MEMIT's dense associative-memory view.
- Geva et al. 2021/2022 — MLP layers as key-value memories; theoretical foundation.
- AlphaEdit (Fang et al.) — null-space projection successor to MEMIT.
