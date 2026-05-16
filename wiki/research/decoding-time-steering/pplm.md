---
title: "PPLM: Plug and Play Language Models"
aliases: ["PPLM", "Plug and Play Language Models"]
tags: [decoding-time-steering, controlled-generation, background, historical]
status: background
year: 2019
venue: ICLR 2020
arxiv: "1912.02164"
authors: ["Dathathri", "Madotto", "Lan", "Hung", "Frank", "Molino", "Yosinski", "Liu"]
theme: decoding-time-steering
depth: background
---

# PPLM: Plug and Play Language Models

The foundational paper for gradient-based decoding-time steering. Dathathri et al. (2019) showed that a frozen pretrained LM can be steered at inference time by back-propagating attribute gradients into its key-value cache — no LM retraining required. Every major successor in the decoding-time-steering lineage (GeDi, FUDGE, ActAdd, ITI, CAA) either directly cites PPLM or inherits its core intuition while fixing its central cost: one backward pass per token.

## Source

Dathathri, S., Madotto, A., Lan, J., Hung, J., Frank, E., Molino, P., Yosinski, J., & Liu, R. (2019). *Plug and Play Language Models: A Simple Approach to Controlled Text Generation.* ICLR 2020. arXiv:1912.02164.

## Method

The LM (GPT-2 345M) is frozen. At each generation step, the cached key-value history $H_t$ is perturbed by gradient ascent on an attribute model $p(a \mid x)$:

$$\Delta H_t \leftarrow \Delta H_t + \alpha \frac{\nabla_{\Delta H_t} \log p(a \mid H_t + \Delta H_t)}{\|\nabla_{\Delta H_t} \log p(a \mid H_t + \Delta H_t)\|^\gamma}$$

After $m = 3$–$10$ update steps, a fresh forward pass with $\tilde{H}_t = H_t + \Delta H_t$ yields the steered next-token distribution. A KL penalty toward the unmodified LM and a post-normalisation geometric-mean fusion stabilise fluency. Setting $\alpha = 0$ exactly recovers the base LM.

Two attribute model variants: **BoW** (bag-of-words, zero learned parameters) and **PPLM-Discrim** (single linear layer, ~1,000 parameters, trained on LM hidden states).

## Claims

- PPLM-Discrim uses ~1,000 parameters vs. GPT-2's 345M — a ~100,000× ratio — yet matches CTRL (1.6B parameters, fully retrained) on topic and sentiment control.
- Topic accuracy: 11.1% (uncontrolled) → 46.9% (BC) → 51.7% (BCR reranking).
- Sentiment control: 73.7% human-rated accuracy vs. GPT2-FT-RL 13.3% and weighted decoding 18.9%.
- Toxicity reduced from 63.6% to 4.6% by following the negative attribute gradient.
- $\alpha$ is continuously tunable; $\alpha = 0$ recovers the unmodified LM exactly.

## Strengths

- Established the "tiny classifier guides large LM at decode time" pattern subsequently adopted by GeDi, FUDGE, ActAdd, ITI, and CAA.
- No LM retraining; attribute models are trivially swappable.
- Mathematically clean: samples from $p(x \mid a) \propto p(a \mid x)\,p(x)$ via latent-space Langevin dynamics.
- Multi-attribute control by composing gradients from independent classifiers.

## Weaknesses

- $m = 3$–$10$ backward passes per token: 3–10× slower than ordinary sampling. This is the central liability that motivated every successor.
- Gradients are applied only to $H_t$ (KV cache), not the full residual stream; later work (ActAdd, ITI, CAA) shows residual-stream offsets are more effective and cheaper.
- Fluency degrades at high $\alpha$ without KL penalty and BCR reranking; BC variant fluency drops to 2.79 vs. 3.54 uncontrolled baseline.
- Discriminator training requires attribute-labelled text (though small amounts suffice).

## Relevance to this wiki's project

**Background / historical anchor.** PPLM is superseded for practical use but is the existence proof for the entire decoding-time steering family. Its direct relevance to $R_w$ (the concept-steering write head) is as a lineage root:

- It grounds the empirical claim that "concept direction in activation space" is meaningful and steerable.
- The modern implementation point shifts from $H_t$ (KV cache, iterative gradient ascent) to the residual stream (ActAdd/ITI/CAA, single-shot additive offset) — the trajectory from PPLM to those methods is the story of eliminating the backward-pass cost.
- For single-sample efficiency the iterative gradient loop is a non-starter; PPLM motivates why the field moved to forward-only steering.

## Connections to the wiki

- [[../synthesis/proposed-method]] — $R_w$ is a single-shot descendant of this lineage; PPLM is the historical existence proof.
- [[gedi]] — direct successor; replaces gradient ascent with Bayes-rule classifier scoring (forward-only).
- [[fudge]] — parallel successor; future-discriminator variant, also forward-only.
- [[actadd]] — residual-stream successor; eliminates backward passes entirely via additive steering vectors.
- [[iti]] — head-level successor; intervention on attention heads rather than KV cache.
- [[caa]] — scaled ActAdd; contrastive activation addition across layers.
- [[repe]] — representation engineering; broader framework that PPLM's KV-cache perturbation fits inside.
- [[linear-rep-hypothesis]] — theoretical grounding for why gradient-on-$H_t$ works at all.
- [[contrastive-decoding]], [[cd-improves-reasoning]], [[dexperts]], [[dola]], [[cfg-lm]] — parallel decoding-time control methods that avoid gradient computation.

## Related

- Nguyen et al. (2017) — Plug & Play Generative Networks (PPGN) for images; direct visual inspiration.
- Keskar et al. (2019) — CTRL; the fully-retrained baseline PPLM benchmarks against.
- Ziegler et al. (2019) — GPT-2-FT-RL; RL fine-tuning baseline.
- Roberts & Rosenthal (1998) — MALA sampler; theoretical basis for the latent-space update rule.
