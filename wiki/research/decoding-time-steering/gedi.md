---
title: "GeDi: Generative Discriminator Guided Sequence Generation"
authors: "Krause, Gotmare, McCann, Keskar, Joty, Socher, Rajani"
year: 2020
arxiv: "2009.06367"
venue: "EMNLP 2021 Findings"
theme: decoding-time-steering
tags: [controlled-generation, class-conditional-lm, bayesian-decoding, contrastive-decoding, detoxification]
status: background
---

# GeDi: Generative Discriminator Guided Sequence Generation

GeDi (Krause et al. 2020) uses a small class-conditional LM (CC-LM) as a *generative discriminator* to reweight the next-token distribution of a frozen large LM via Bayes rule. Two parallel CC-LM forward passes — one under control code $c$, one under anti-code $\bar{c}$ — yield per-token class posteriors for the entire vocabulary at negligible marginal cost, sidestepping the per-candidate forward passes required by standard discriminators. The result is controllable, domain-transferable generation that is >30× faster than PPLM while matching or exceeding its steering quality.

## Source

Krause, B., Gotmare, A. D., McCann, B., Keskar, N. S., Joty, S., Socher, R., & Rajani, N. F. (2020). *GeDi: Generative Discriminator Guided Sequence Generation*. EMNLP 2021 Findings. arXiv:2009.06367.

## Method

At each decoding step the CC-LM (parameters $\theta$) computes the class posterior for every candidate next token via Bayes rule over partial sequences:

$$P_\theta(c \mid x_{\leq t}) = \frac{P(c)\,P_\theta(x_{1:t} \mid c)^{\alpha/t}}{\sum_{c' \in \{c,\bar{c}\}} P(c')\,P_\theta(x_{1:t} \mid c')^{\alpha/t}}$$

where $\alpha$ is a learnable scale and $t$ normalises for sequence length. The guided posterior used for sampling is:

$$P_w(x_t \mid x_{<t}, c) \propto P_\text{LM}(x_t \mid x_{<t}) \cdot P_\theta(c \mid x_t, x_{<t})^\omega$$

with $\omega > 1$ amplifying the steering signal. An optional filtering heuristic removes low-$P_\theta(c)$ tokens while preserving at least cumulative probability mass $\rho$ in $P_w$.

Training adds a discriminative cross-entropy loss $L_d$ to the standard generative NLL $L_g$:

$$L_{gd} = \lambda\, L_g + (1-\lambda)\, L_d$$

making the CC-LM a better classifier without abandoning its generative capability.

## Claims

- >30× faster than PPLM at 256-token generation with GPT2-XL (0.095 vs. 3.116 sec/token); two CC-LM passes vs. 10+ gradient steps through the base LM.
- Stronger out-of-domain sentiment control than PPLM on book text: positivity 3.85 vs. 3.53; negativity 1.85 vs. 2.62 (1–5 human scale). CC-LM trained on movie reviews generalises to book text because the Bayesian contrast cancels domain-specific vocabulary bias.
- Zero-shot topic generalisation: a GeDi trained on four news topics generates coherent text on "space", "climate", "education", etc. from a single BPE-token control code; CTRL and PPLM cannot do this.
- Significantly reduces GPT-2 (1.5B) toxicity (avg. 1.13–1.17 vs. 1.45 on 1–3 scale) without sacrificing perplexity.
- Per-token classification cost ~10,000× less than a unidirectional discriminator for typical vocabulary sizes ($|V| \approx 50{,}000$), achieved by reusing CC-LM hidden states across decoding steps.

## Strengths

- **Key trick is the generative classifier identity.** Scoring all $|V|$ next tokens requires only two CC-LM forward passes; the autoregressive hidden states are cached, so the incremental cost is a single new position per pass.
- **Contrastive Bayes cancels domain bias.** Shared attributes of $c$ and $\bar{c}$ divide out, letting a movie-review GeDi steer book text without pulling vocabulary toward film terminology.
- **Zero-shot transfer via control codes.** Single-token codes embed semantics from pretraining; topics unseen during CC-LM fine-tuning are handled by the base LM's own knowledge, not explicit supervision.
- **Base LM weights are frozen.** No forgetting, no retraining cost; applicable to any LM that shares tokenisation and exposes next-token logits.

## Weaknesses

- GeDi and the base LM must share the exact tokenisation; incompatible with black-box APIs that do not return per-token log-probabilities.
- Zero-shot topic control degrades on long domain-specific prompts where the base LM's context overwhelms the CC-LM's steering signal.
- Scaling tested only to GPT-2 1.5B; behaviour at 7B–70B+ (modern instruction-tuned models) is untested.
- 2020-era evaluation: 50–100 human-rated prompts per condition; effect sizes may not replicate under rigorous modern benchmarks.
- Requires training or obtaining a CC-LM for each attribute family; not zero-shot for entirely new attribute *types* (only new topics within a trained attribute family).

## Relevance to this wiki's project

GeDi is the cleanest prior-art instantiation of the $R_w$ (reweight) module in the proposed method. Its Bayesian posterior $P_w \propto P_\text{LM} \cdot P_\theta(c)^\omega$ is the parametric form of exactly what the proposed method intends: a small auxiliary signal shifts the base LM's distribution toward a target concept without touching base weights. Two direct consequences for the research agenda:

1. **Frozen-base feasibility is established.** If the concept is already latent in the base LM (consistent with the Rethinking-RL 0%-shifted finding), GeDi-style decoding surfaces it without any gradient update, making single-sample concept acquisition purely an inference-time problem.
2. **Speed-controllability tradeoff is solved at the decoding layer.** PPLM's latency ruled out interactive or online use; GeDi's latency does not. This leaves the open question for this project as *learning* the CC-LM (or a lighter proxy) from a single labelled example, rather than efficiency.

Treat as Background depth: the mechanism is well-understood and the paper is from 2020; the wiki's contribution is upstream (acquiring the concept representation, not the decoding algorithm itself).

## Connections to the wiki

- [[../synthesis/proposed-method]] — GeDi is direct prior art for the $R_w$ reweighting design; the proposed method's novelty is in acquiring $\theta$ from one sample, not in the decoding formula itself.
- [[../in-context-learning-theory/icl-bayesian-inference]] — GeDi makes the Bayesian-inference view of ICL parametric: the CC-LM posterior plays the role of the implicit Bayesian prior that ICL theory treats abstractly.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — the 0%-shifted result implies the concept exists in the base LM; GeDi shows frozen-base decoding is sufficient to surface it.
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — GeDi sidesteps catastrophic forgetting entirely by leaving base weights untouched; relevant when comparing decoding-time vs. fine-tuning approaches.
- [[pplm]] — direct ancestor; GeDi's contribution is solving PPLM's per-step gradient cost.
- [[dexperts]] — product-of-experts sibling operating in the same Bayesian-decoding family.
- [[fudge]] — future-discriminator sibling; FUDGE conditions on future completions rather than current token posteriors.
- [[contrastive-decoding]], [[cd-improves-reasoning]], [[dola]] — later contrastive-decoding methods that share GeDi's contrast-of-distributions intuition.
- [[cfg-lm]] — classifier-free guidance applied to LMs; equivalent to GeDi with $\bar{c}$ = unconditional.
- [[repe]], [[iti]], [[actadd]], [[caa]], [[linear-rep-hypothesis]] — representation-space steering methods; orthogonal axis (activation space vs. logit space) for the same goal.

## Related

- Dathathri et al. (2020) — PPLM (gradient-based predecessor).
- Keskar et al. (2019) — CTRL (class-conditional LM training).
- Holtzman et al. (2018) — Weighted decoding (original discriminator-guided decoding).
- Liu et al. (2021) — DExperts (product-of-experts variant).
- Yang & Klein (2021) — FUDGE (future discriminator variant).
