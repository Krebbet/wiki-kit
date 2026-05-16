---
title: "Contrastive Activation Addition (CAA)"
aliases: ["CAA", "Rimsky 2023", "Panickssery 2023"]
tags: [decoding-time-steering, activation-engineering, background-depth]
arxiv: "2312.06681"
venue: "ACL 2024"
authors: ["Nina Panickssery", "Nick Gabrieli", "Julian Schulz", "Meg Tong", "Evan Hubinger", "Alexander Matt Turner"]
year: 2023
theme: decoding-time-steering
depth: background
---

# Contrastive Activation Addition (CAA)

Scaled-up successor to [[actadd]]: instead of one hand-picked prompt pair, CAA averages residual-stream activation differences over hundreds of A/B multiple-choice pairs to extract a behaviour-specific steering vector, then adds it at every post-prompt token position during inference. Evaluated on seven alignment-relevant behaviours across Llama-2 Chat 7B and 13B. The key non-obvious result is **base-to-chat transfer**: vectors extracted from the base model steer the RLHF chat model — RLHF leaves middle-layer concept geometry intact.

## Source

Panickssery et al., *Steering Llama 2 via Contrastive Activation Addition*, ACL 2024. [arXiv:2312.06681](https://arxiv.org/abs/2312.06681).

## Method

Given a dataset $D$ of (prompt $p$, positive completion $c_p$, negative completion $c_n$) triples, the Mean Difference steering vector at layer $L$ is:

$$v_\text{MD} = \frac{1}{|D|} \sum_{p,\, c_p,\, c_n \,\in\, D} \left( a_L(p, c_p) - a_L(p, c_n) \right)$$

where $a_L(\cdot)$ returns the residual-stream activation at layer $L$ at the answer-token position. Prompt pairs share identical question text; only the trailing answer letter ("A" or "B") differs, so the difference cancels most confounds and isolates the target-behaviour direction.

At inference time, $\alpha \cdot v_\text{MD}$ is added to the residual stream at every generated-token position (post-prompt). Optimal layers: 13–15 for Llama-2 7B/13B ($\approx 1/3$–$1/2$ depth).

## Claims

- Shifts behaviour on all 7 tested dimensions (sycophancy, refusal, hallucination, corrigibility, survival instinct, myopic reward, AI coordination) in both MC and GPT-4-rated open-ended settings at 7B and 13B.
- **Stacks additively** on system-prompt design and finetuning for 3 of 7 behaviours — implies CAA targets a distinct degree of freedom from prompt or weight conditioning.
- Generalises to open-ended generation in every case where A/B finetuning fails to transfer (most notably sycophancy).
- Minimal capability cost: MMLU shift $\leq 0.04$ at multiplier $|\alpha| = 1$; subtracting the sycophancy vector slightly improves TruthfulQA.
- **Base-to-chat transfer** (§8.3): vectors from the Llama-2 base model steer the Chat (RLHF) model at layers 10–15, confirming RLHF does not destroy middle-layer concept geometry.
- Cosine-similarity probing shows tokens such as "I cannot help" activate the refusal steering vector — the direction is concept-encoding, not a proxy artefact.

## Strengths

Averaging over hundreds of pairs (vs a single pair in [[actadd]]) substantially reduces noise, yielding more reliable vectors. Validation is broad: 7 behaviours, 2 model scales, two evaluation formats (MC + free-text rated by GPT-4). The "stacks on finetuning" finding is the strongest published evidence that activation-space steering occupies a complementary mechanism to weight-space fine-tuning — an additive-correction framing. The base-to-chat transfer result is empirically clean and theoretically consequential.

## Weaknesses

- Scope limited to Llama-2 Chat 7B and 13B; no base-model open-ended evaluation, no 70B results.
- GPT-4 evaluator is prompt-sensitive; free-text rating protocol is not reproducible independently.
- The finetuning baseline is unoptimised — the CAA-over-finetuning delta may shrink with better fine-tuning.
- Adding $\alpha \cdot v_\text{MD}$ at every post-prompt token caps usable multiplier before generation quality degrades.
- Residual-stream norm grows with depth; $v_\text{MD}$ is not normalised, so $\alpha$ is not comparable across layers.

## Relevance to this wiki's project

**Background depth but load-bearing for R_w.** The base-to-chat transfer result (§8.3) is the strongest direct empirical anchor for the R_w hypothesis within the activation-steering family: a concept direction that exists pre-RLHF survives fine-tuning and can be activated without any gradient update. This directly supports the single-sample learning premise — the target representation is already present in the base model, gradient signal merely needs to locate and upweight it.

The "stacks on finetuning" finding implies R_w and gradient-based fine-tuning occupy orthogonal degrees of freedom. The analogy to the Invisible Leash is tight: a model steered with $\alpha \cdot v_\text{MD}$ cannot move outside base-model activation support ([[../self-play/invisible-leash]]), just as base-support constrains what RLVR can express. The connection to [[../rlvr-mechanics/rl-sparse-subnetwork]] is geometric: if RLVR selects a pre-existing sparse subnetwork, $v_\text{MD}$ geometrically identifies that subnetwork's principal axis.

## Connections to the wiki

- [[../concept-learning/_overview]] — concept-as-direction thesis; $v_\text{MD}$ is a linear readout of CBM/RCE geometry
- [[../synthesis/proposed-method]] — R_w logit-reweighting is the gradient-space dual of adding $v_\text{MD}$ to activations
- [[../self-play/invisible-leash]] — base-support constraint; CAA cannot steer outside base-model activation manifold
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse subnetwork as geometric precondition for steering-vector recovery

## Related

Within theme: [[actadd]] (single-pair ancestor), [[repe]] (umbrella framework; shared MD extraction), [[iti]] (head-level cousin; same MD extraction targeting sparse attention heads), [[linear-rep-hypothesis]] (theoretical backbone).

Adjacent: [[contrastive-decoding]], [[cd-improves-reasoning]], [[dexperts]], [[gedi]], [[fudge]], [[pplm]], [[dola]], [[cfg-lm]].
