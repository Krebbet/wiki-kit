---
name: kto
description: "binary-signal alignment via Kahneman-Tversky prospect theory; HALO family; no preference pairs needed"
type: research
---

# KTO: Model Alignment as Prospect Theoretic Optimization

Ethayarajh, Xu, Muennighoff, Jurafsky, Kiela — Stanford / Contextual AI, arXiv:2402.01306 (ICML 2024). Frames LLM alignment through prospect theory and introduces the HALO (human-aware loss) family — a class of objectives whose implied value functions share structural properties with the Kahneman-Tversky model of human utility. KTO is the HALO derived directly from that model: it maximizes the KT-utility of generations rather than the log-likelihood of preferences. It requires only a binary desirable/undesirable signal per example, not preference pairs, making it cheaper and more practical to collect at scale. Despite using a weaker signal, KTO matches or exceeds DPO performance at 1B–30B parameter scales.

## Method

**HALO definition.** Let $r_\theta(x, y) = l(y)\log\frac{\pi_\theta(y|x)}{\pi_\text{ref}(y|x)}$ be the implied reward and $Q(Y'|x)$ a reference point distribution. A loss $f$ is a HALO for value function $v$ (non-decreasing, concave in gains) if:

$$f(\pi_\theta, \pi_\text{ref}) = \mathbb{E}_{x,y\sim\mathcal{D}}\bigl[a_{x,y}\,v\!\bigl(r_\theta(x,y) - \mathbb{E}_Q[r_\theta(x,y')]\bigr)\bigr] + C_\mathcal{D}$$

where $a_{x,y}\in\{-1,+1\}$. DPO and PPO-Clip are both HALOs (Theorem 3.5); SLiC and conditional SFT are not, which tracks their empirically weaker performance.

**Kahneman-Tversky value function.** The canonical KT form is:

$$v(z;\lambda,\alpha,z_0) = \begin{cases}(z-z_0)^\alpha & z \geq z_0 \\ -\lambda(z_0-z)^\alpha & z < z_0\end{cases}$$

with median $\alpha=0.88$, $\lambda=2.25$. KTO replaces the numerically unstable power function with the logistic $\sigma$, controls curvature via $\beta$, and splits loss aversion into separate hyperparameters $\lambda_D, \lambda_U$ for desirable and undesirable outputs.

**KTO loss.** The reference point $z_0$ is estimated as $\widehat{z}_0 = \max\bigl(0, \frac{1}{m}\sum_{i}\log\frac{\pi_\theta(y_j|x_i)}{\pi_\text{ref}(y_j|x_i)}\bigr)$ using mismatched pairs from the microbatch (shifted outputs). The loss is:

$$\mathcal{L}_\text{KTO}(\pi_\theta,\pi_\text{ref}) = \mathbb{E}_{x,y\sim\mathcal{D}}\bigl[\lambda_y - v(x,y)\bigr]$$

where $r_\theta(x,y) = \log\frac{\pi_\theta(y|x)}{\pi_\text{ref}(y|x)}$ and

$$v(x,y) = \begin{cases}\lambda_D\,\sigma\!\bigl(\beta(r_\theta(x,y)-z_0)\bigr) & y \sim y_\text{desirable}|x \\ \lambda_U\,\sigma\!\bigl(\beta(z_0 - r_\theta(x,y))\bigr) & y \sim y_\text{undesirable}|x\end{cases}$$

**Contrast with DPO.** DPO's reference point is the dispreferred output $y_l$ in the same pair, grounded in a Bradley-Terry preference model. KTO's reference point is the marginal KL divergence across all outputs for $x$, estimated without any paired structure. This decouples examples entirely — each $(x,y)$ is trained on independently.

## Claims

- **KTO $\geq$ DPO at 1B–30B.** SFT+KTO is competitive with SFT+DPO across Pythia-{1.4B,2.8B,6.9B,12B} and Llama-{7B,13B,30B} on GPT-4-judged winrate vs. SFT targets. KTO alone beats DPO alone on Llama-{7B,13B,30B} (p < 0.01 at 7B and 30B after correction).
- **Benchmark scores (Zephyr-β-SFT on UltraFeedback).** KTO ($\beta$=0.1): MMLU 58.6, GSM8K 53.5, HumanEval pass@1 30.9, BBH 52.6 — vs. DPO: 58.2 / 40.0 / 30.1 / 44.1.
- **Extreme data imbalance.** Up to 90% of desirable examples can be discarded (with $\lambda_D$ rescaled per Eq. 9) while KTO still outperforms DPO on Llama-7B.
- **No preference structure needed.** `one-y-per-x` (a single output per input, no pairing) still outperforms DPO despite halving data volume.
- **SFT optional.** When the pretrained model is strong, KTO without a preceding SFT stage matches SFT+DPO quality; DPO without SFT tends to hallucinate and ramble.
- **HALOs beat non-HALOs.** DPO and offline PPO outperform SLiC and CSFT at 13B+ (p < 0.05); only HALO-aligned Llama-{13B,30B} models consistently match or beat SFT targets.

## Relevance to the project

KTO's binary-signal framing maps directly onto a single-sample training setting: if the learner receives one example and a scalar "this generation was good / bad" signal, KTO is the natural alignment objective — it requires no second contrastive example and no preference annotation. The HALO framework also provides a theoretical vocabulary for comparing the inductive biases of DPO, IPO, SLiC, and KTO side by side, which matters when choosing or designing an objective for a regime where data is by construction minimal. The result that offline PPO with dummy ±1 rewards can match DPO at most scales (until 30B) is separately relevant: it suggests that the structure of the loss — the inductive bias toward human-aware value functions — dominates the quality of the reward signal, which is useful when constructing rewards from sparse, low-information feedback.

## Source

- arXiv: https://arxiv.org/abs/2402.01306
- Raw: `../../../raw/research/rl-optimizers/03-05-kto-ethayarajh.md`

## Related

- [[_overview]]
- [[dpo]]
- [[instructgpt]]
- [[ppo]]
