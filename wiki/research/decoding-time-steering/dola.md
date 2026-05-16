---
title: "DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models"
authors: "Yung-Sung Chuang, Yujia Xie, Hongyin Luo, Yoon Kim, James Glass, Pengcheng He"
year: 2023
arxiv: "2309.03883"
venue: "ICLR 2024"
tags: [decoding-time-steering, factuality, layer-contrastive, hallucination, inference-time]
relevance: central
---

# DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models

Factual knowledge in transformer LMs is layer-localised: entities and dates show high JSD between early and final layers, while function words converge at mid-depth. DoLa exploits this asymmetry at inference time by dynamically selecting a *premature* layer $M$ and subtracting its logits from the *mature* (final) layer $N$, amplifying factual signal with no weight update, no retrieval, and no auxiliary model.

## Source

Chuang et al. (2023). *DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models.* arXiv:2309.03883. ICLR 2024.

## Method

At each decoding step, select the premature layer by maximum Jensen-Shannon divergence from the final layer over a candidate set $J$:

$$M = \arg\max_{j \in J} \, \mathrm{JSD}\!\left(q_N(\cdot \mid x_{<t}) \,\Big\|\, q_j(\cdot \mid x_{<t})\right)$$

Compute the contrastive next-token distribution restricted to a plausibility mask $V_\text{head} = \{x_t : q_N(x_t) \geq \alpha \max_w q_N(w)\}$:

$$\hat{p}(x_t \mid x_{<t}) = \mathrm{softmax}\!\left(\log \frac{q_N(x_t)}{q_M(x_t)}\right)\bigg|_{x_t \in V_\text{head}}$$

where $q_j(x_t \mid x_{<t}) = \mathrm{softmax}(\phi(h_t^{(j)}))_{x_t}$ is the vocabulary-head projection of the $j$-th layer hidden state. The plausibility mask prevents low-probability tokens from dominating after log-ratio amplification (same guard as contrastive decoding). Layer buckets (2–4 groups) narrow the JSD search space; the best bucket is chosen on a small validation split.

## Claims

- +12–17 pp absolute on TruthfulQA %Truth×Info across LLaMA-7B/13B/33B/65B; matches ITI without requiring supervised labels.
- MC2/MC3 gains ~20 pp (LLaMA-7B MC2: 40.6 → 63.8; LLaMA-13B: 43.3 → 64.9).
- +1–4% StrategyQA, +2% GSM8K chain-of-thought — DoLa improves reasoning where model-contrastive CD degrades it.
- Decoding overhead 1.00–1.08×; throughput hit 1–7% across 7B–65B model sizes.
- No training, no retrieval, no external model — pure inference-time, single model.

## Strengths

- Single-model: no auxiliary classifier (contrast with ITI) and no amateur model (contrast with contrastive decoding).
- Dynamic JSD-based layer selection is empirically grounded — JSD heatmaps directly show that factual tokens maintain high divergence into the final layers while structural tokens converge early, making the selection criterion mechanistically motivated rather than arbitrary.
- Reasoning tasks improve rather than degrade, distinguishing DoLa from model-level CD.
- Plausibility mask preserves fluency by keeping only tokens the mature layer already rates plausibly.

## Weaknesses

- Evaluated on LLaMA family only; generality to other architectures (especially those with different residual-stream depth profiles) is unverified.
- Bucket choice requires a small in-distribution validation set; DoLa-static (brute-force layer search) is more sensitive to distributional shift.
- TruthfulQA MC1 shows marginal underperformance at 33B scale — winner-takes-all setting is less stable under the log-ratio operation.
- Long generation requires a repetition penalty ($\theta = 1.2$); greedy decoding only — no beam-search or speculative-decoding latency data.

## Relevance to this wiki's project

DoLa is the most direct existence proof for $R_w$ in the proposed method. It demonstrates that factual knowledge already encoded in upper layers can be surfaced purely by logit reweighting (layer contrast) — no weight update, no external retrieval, no second model. This is exactly the "offline reweighting" $R_w$ envisions: a static or learned layer-difference logit prior applied at inference time.

The fluency-vs-factuality split between lower and upper layers mirrors the BOLT coverage-wall intuition: the surface prior (lower-layer fluency signal) can be dampened at inference time via layer subtraction, exposing the richer factual distribution that would otherwise be masked. Crucially, DoLa does not move outside the model's support — it surfaces what is already there, mapping directly onto Invisible Leash C.1. From a single-sample perspective, DoLa's approach is fully offline and per-token dynamic, requiring no labelled examples at the layer-selection step, which aligns with the wiki's zero-additional-data constraint.

## Connections to the wiki

- [[../synthesis/proposed-method]] — DoLa is a direct existence proof for $R_w$: single-model logit reweighting, no training required.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — mechanistic dissection of RL sparsity in transformer layers; DoLa's JSD layer-localisation is a complementary inference-time view of the same layerwise specialisation.
- [[../in-context-learning-theory/induction-heads]] — layer-localised circuits in transformers; DoLa's JSD analysis corroborates that factual retrieval is concentrated in upper layers.
- [[../self-improvement/self-rewarding-lm]] — [[../conflicts/invisible-leash-vs-spiral-transfer]] (Invisible Leash framing): DoLa demonstrates no support shift — the reweighting stays within the model's existing probability mass.
- [[../concept-learning/_overview]] — concept-as-direction hypothesis: upper-layer factual signal aligns with concept directions in the late residual stream.

Within decoding-time-steering theme: [[contrastive-decoding]] (model-contrastive parent — DoLa is the *layer-contrastive* sibling), [[cd-improves-reasoning]], [[cfg-lm]], [[dexperts]], [[gedi]], [[fudge]], [[pplm]], [[repe]], [[iti]], [[actadd]], [[caa]], [[linear-rep-hypothesis]].

## Related

- Li et al. (2022) — Contrastive Decoding (model-contrastive; DoLa adapts its plausibility mask and log-ratio operator to the within-model setting).
- Burns et al. (2022) — ITI (inference-time intervention via supervised probes; DoLa matches it without labels).
- Dai et al. (2022) — knowledge neurons in BERT feedforward layers (mechanistic basis for DoLa's layer-localisation assumption).
- Meng et al. (2022) — ROME (factual knowledge editable via specific FFN layers; same localisation prior exploited differently).
- Tenney et al. (2019) — layer-wise probing of linguistic vs. semantic content in BERT (early empirical support for the lower/upper layer split).
