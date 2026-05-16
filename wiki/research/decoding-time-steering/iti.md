---
title: "Inference-Time Intervention (ITI)"
arxiv: "2306.03341"
year: 2023
venue: "NeurIPS 2023"
authors: "Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, Martin Wattenberg"
tags: [decoding-time-steering, activation-editing, truthfulness, probing, attention-heads, R_w]
theme: decoding-time-steering
---

# Inference-Time Intervention (ITI)

Li et al. (NeurIPS 2023) demonstrate that LLaMA models harbour a linear representation of truthfulness inside a sparse subset of attention heads — and that steering activations along that representation at inference time roughly doubles TruthfulQA true-and-informative scores with fewer than 100 labelled examples. The central diagnostic is a **~40% probe–generation gap**: LLaMA-7B's best single head achieves 83.3% linear probe accuracy on truthfulness while the model generates correctly on only ~43% of the same questions. The gap is direct evidence that correct-answer representations exist in the base model but are suppressed at output — the model is not missing knowledge, it is failing to route it. ITI closes that gap by adding a learned shift vector into selected head outputs at every autoregressive step, with zero weight updates and negligible runtime overhead.

## Source

- arXiv: 2306.03341  
- Raw: `../../../raw/research/decoding-time-steering/08-09-iti.md`

## Method

**Step 1 — Probe.** For each attention head $(l, h)$, collect last-token activations $x_l^h \in \mathbb{R}^D$ over $N = 5{,}918$ TruthfulQA QA-pairs with binary truthfulness labels. Fit a linear probe

$$p_\theta(x_l^h) = \text{sigmoid}(\langle \theta, x_l^h \rangle)$$

per head; select top-$K$ heads by validation accuracy. The probe weight $\theta_l^h$ (or equivalently the mass-mean-shift direction) defines the truthful direction for that head.

**Step 2 — Intervene.** At inference, replace standard MHA with:

$$x_{l+1} = x_l + \sum_{h=1}^{H} Q_l^h\!\left(\operatorname{Att}_l^h(P_l^h x_l) + \alpha\,\sigma_l^h\,\theta_l^h\right)$$

where $\alpha \in \mathbb{R}^+$ is intervention strength, $\sigma_l^h$ is the empirical std of head activations along $\theta_l^h$ estimated from the probing dataset, and $\theta_l^h = \mathbf{0}$ for non-selected heads. The intervention is applied autoregressively at every token position.

**Offline baking.** Because each layer adds a constant vector, the intervention collapses to a bias edit with zero runtime overhead:

$$\operatorname{Bias}_l = \alpha \sum_{h=1}^{H} Q_l^h(\sigma_l^h\,\theta_l^h)$$

This can be written directly into the output-projection bias of a pretrained model (see `honest_llama2_chat_7B` on HuggingFace).

**Direction comparison (Table 3, LLaMA-7B, true*info %).** Mass mean shift (42.3%) > probe weight direction (34.8%) > CCS unsupervised (33.4%) > random direction (31.2%) vs. baseline (30.5%). Random-direction null is flat — the gain is direction-specific, not a generic norm perturbation.

**Head selectivity (Table 5).** Head-wise selection (42.3%) > point-wise selection (39.2%) > no selection / all heads (35.4%). Sparsifying to $K$ heads preserves informativeness that blanket intervention degrades.

## Claims

- **Probe–generation gap.** LLaMA-7B layer 14, head 18: probe accuracy 83.3% vs. generation accuracy on TruthfulQA ~43% — a ~40 pp gap. Concatenating all heads raises probe to 84.4%; the gap persists. (Sec 1, Fig 2B.)
- **TruthfulQA generation, Alpaca:** true*informative 32.5% → 65.1%; true 32.7% → 66.6%; MC 27.8% → 31.9%. (Table 2.)
- **TruthfulQA generation, Vicuna:** true*informative 51.5% → 74.0%; true 55.6% → 88.6%; MC 33.3% → 38.9%. (Table 2.)
- **Data efficiency:** direction similarity saturates early (Fig 6A); 81 questions (10% of TruthfulQA, 2-fold CV) is sufficient for optimal hyperparameter selection; as few as ~40 examples locate the direction.
- **OOD generalisation:** NaturalQuestions 46.6% → 51.3% (+4.7 pp); TriviaQA 89.6% → 91.1% (+1.5 pp); MMLU 35.71% → 40.16% (+4.45 pp). Zero new direction-finding on OOD sets — directions from TruthfulQA transfer. (Table 4.)
- **Truthfulness–helpfulness tradeoff:** true*informative follows an inverted-U in $\alpha$ (Fig 4); at high $\alpha$ the model increasingly responds "I have no comment." Trade-off is continuous and user-tunable. (Fig 6B.)
- **Computational overhead:** the constant-per-layer shift is numerically equivalent to editing the output-projection bias — zero FLOPs added beyond the bias term already present in standard MHA. (Sec 5.2.)

## Strengths

- **Probe–generation gap is the key contribution.** 40 pp quantifies the routing bottleneck with direct activation-level evidence. Not a theoretical claim — measured on a real model and benchmark.
- **Data efficiency is extreme.** ~40–81 contrast pairs vs. RLHF's thousands of preference annotations. Direction-similarity plateau in Fig 6A shows the truthful subspace is geometrically coherent and easy to find.
- **Head-level localization.** Strictly finer than residual-stream methods (ActAdd, CAA): unrelated heads are untouched, preserving general language model behaviour (low KL on OpenWebText).
- **Zero weight-update, offline-bakeable.** No fine-tuning pass required; the intervention can be distributed as a bias-vector patch with no architecture change.
- **Null control is clean.** Random direction yields 31.2% (flat vs. 30.5% baseline) — confirms specificity of the truthful direction. (Table 3.)
- **Geometry is multi-dimensional.** Orthogonal probe $\theta'$ achieves better-than-chance accuracy, indicating "truth" occupies a low-dimensional subspace rather than a single direction — aligns with [[linear-rep-hypothesis]].

## Weaknesses

- **TruthfulQA-centric.** 817 adversarially curated questions spanning 38 misconception categories. OOD gains are real but modest (+4.7 pp on NQ, +1.5 pp on TriviaQA). MMLU gain (+4.45 pp) likely reflects distribution overlap with TruthfulQA-style misconceptions.
- **Requires held-out labelled contrast pairs.** Fully unsupervised CCS gives only 33.4% true*info vs. 42.3% for supervised probe — unsupervised discovery of the truthful direction does not yet close the gap.
- **$K$ and $\alpha$ selected empirically.** No principled rule for optimal intervention strength or number of heads; requires a validation sweep on held-out TruthfulQA. Generalization of these hyperparameters to new domains is untested.
- **Models tested: LLaMA-7B, Alpaca, Vicuna only.** All 7B-class; scaling behaviour and head-localization patterns at 13B/70B are unknown.
- **Truthful direction is dataset-relative.** TruthfulQA operationalizes "avoid common human misconceptions" — not the full scope of factual correctness. Authors acknowledge this explicitly (Sec 3.1).

## Relevance to this wiki's project

ITI is the **primary empirical anchor for $R_w$** — the hypothesis that single-sample learning is bottlenecked not by missing capacity but by routing/selection failure.

The 40 pp probe–generation gap is the cleanest published quantification of this: the base model contains the correct representation; standard decoding fails to route it. This maps directly onto the BOLT coverage wall: the bottleneck is not what the model has encoded but what the generation procedure selects.

Critically, ITI does not move the model outside its generative support: the random-direction null (Table 3) confirms the shift is not injecting new information — it is amplifying an existing internal representation. This is Invisible Leash Theorem C.1 operating at the activation layer rather than the logit layer: intervention stays within the support of the base distribution.

The low-rank structure of the intervention (a single direction per head, $\sim K \times D$ parameters total) parallels REASONMAXXER's rank-8 $W_O$ LoRA (0.04% of parameters): both are low-rank corrections that redirect internal representations rather than add capacity. The analogy is tight — head output-projection bias vs. $W_O$ LoRA are both interventions on the same matrix.

For the proposed method: if the concept skeleton $R_w$ is learned from a single sample, ITI shows that (a) the target representation likely already exists in the pretrained model, and (b) a sparse, low-rank steering signal is sufficient to surface it at generation time. This argues for an architecture where the learned concept direction functions as a dynamic ITI-style bias — computed per-forward-pass from the input, rather than fixed from a static probing dataset.

## Connections to the wiki

- [[repe]] — RepE is the umbrella activation-control framework; ITI is an instance of RepE's Reading + Control pipeline applied at head granularity.
- [[actadd]] — Residual-stream sibling: adds a steering vector to the residual stream after MLP rather than per-head before $Q_l^h$. ITI's head-level localization is the key differentiator.
- [[caa]] — Contrastive Activation Addition: same mass-mean-shift direction computation as ITI's best-performing variant, applied to residual stream. ITI adds head selection on top.
- [[linear-rep-hypothesis]] — Theoretical backbone: truthful directions being linear and geometry being a subspace (Fig 2B, orthogonal probe) is direct empirical support.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER rank-8 $W_O$ LoRA at 0.04% params: analogous low-rank routing correction at token level; same conceptual move (sparse intervention redirects existing representation rather than adding knowledge).
- [[../concept-learning/concept-bottleneck-models]] — Test-time intervention on concept slots: ITI is the activation-space analogue of CBM concept-slot intervention.
- [[../concept-learning/recursive-concept-evolution]] — Low-rank concept subspaces; truthful directions are a special case of concept-aligned low-rank structure.
- [[../synthesis/proposed-method]] — $R_w$ primary empirical anchor; ITI's gap quantification directly motivates the routing-correction framing.
- [[../self-play/invisible-leash]] — Theorem C.1: support inclusion constraint. ITI's random-direction null (Table 3) provides empirical confirmation that effective steering stays within the base model's support.

## Related

- [[repe]] — umbrella framework; ITI is a RepE instance
- [[actadd]] — residual-stream sibling
- [[caa]] — averaged-contrast sibling
- [[linear-rep-hypothesis]] — theoretical backbone for linear truthful directions
- [[contrastive-decoding]] — inference-time quality improvement via likelihood contrast
- [[cd-improves-reasoning]] — contrastive decoding applied to reasoning
- [[dexperts]] — expert/anti-expert product-of-experts decoding
- [[gedi]] — generative discriminator for controlled generation
- [[fudge]] — future discriminator for generation control
- [[pplm]] — plug-and-play LM: gradient-based activation steering (predecessor)
- [[dola]] — decoding by contrasting layers; related probing-during-decoding idea
- [[cfg-lm]] — classifier-free guidance applied to language models
