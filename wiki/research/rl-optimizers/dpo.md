---
name: dpo
description: "closed-form policy from preference pairs; implicit reward; no RL loop"
type: research
---

# Direct Preference Optimization (DPO)

Rafailov, Sharma, Mitchell, Ermon, Manning, Finn — Stanford / CZ Biohub, NeurIPS 2023. DPO eliminates the explicit reward model and RL training loop of standard RLHF by reparameterising the reward directly in terms of the policy. The key insight is that the KL-constrained reward-maximisation objective (Eq. 3 in the paper) has an analytic optimal policy, which can be inverted to express any reward function as a log-ratio of policy to reference. Plugging this into the Bradley-Terry preference model cancels the intractable partition function and yields a simple binary cross-entropy loss over preference pairs. Training requires only a static offline preference dataset — no on-policy sampling, no value function, no PPO.

## Method

**Change of variables.** The standard RLHF RL objective is:

$$\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D},\, y \sim \pi_\theta(y|x)}\!\left[r_\phi(x,y)\right] - \beta\, D_{\mathrm{KL}}\!\left[\pi_\theta(y|x) \,\|\, \pi_{\mathrm{ref}}(y|x)\right]$$

The closed-form optimal policy for any reward $r$ is $\pi_r(y|x) = \frac{1}{Z(x)}\pi_{\mathrm{ref}}(y|x)\exp\!\left(\frac{1}{\beta}r(x,y)\right)$, where $Z(x)$ is the (intractable) partition function. Inverting this gives:

$$r(x, y) = \beta \log \frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)} + \beta \log Z(x)$$

**Partition function cancels.** The Bradley-Terry preference model depends only on the *difference* of rewards between two completions $y_w \succ y_l$, so $Z(x)$ cancels exactly. Substituting the reparameterisation into the BT model and forming a maximum-likelihood objective over the preference dataset $\mathcal{D} = \{(x^{(i)}, y_w^{(i)}, y_l^{(i)})\}$ gives the DPO loss:

$$\mathcal{L}_{\mathrm{DPO}}(\pi_\theta;\pi_{\mathrm{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\!\left[\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right]$$

**Gradient interpretation.** The gradient increases $\log\pi(y_w|x)$ and decreases $\log\pi(y_l|x)$, but with an importance weight $\sigma(\hat{r}_\theta(x, y_l) - \hat{r}_\theta(x, y_w))$ — upweighting examples where the implicit reward currently mis-ranks the pair. Without this weight the objective degenerates (the paper's "naïve" ablation, Appendix Table 3).

**$\beta$ as KL coefficient.** $\beta$ is identical to the KL penalty coefficient in the original RLHF objective. Larger $\beta$ → tighter constraint on deviation from $\pi_{\mathrm{ref}}$; smaller $\beta$ → more aggressive preference optimisation.

**Theorem 1** (Rafailov et al.): under mild assumptions, every reward equivalence class consistent with the Plackett-Luce / Bradley-Terry model is representable by the reparameterisation $r(x,y) = \beta\log\frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)}$, so no expressiveness is lost relative to an explicit reward model.

## Claims

- **Sentiment control (IMDb, GPT-2-large).** DPO's reward/KL Pareto frontier strictly dominates PPO and PPO-GT (oracle with ground-truth rewards). DPO achieves the highest reward at every KL budget tested.
- **Summarisation (Reddit TL;DR, GPT-J).** DPO win rate vs. human-written summaries: ~61% at temperature 0, exceeding PPO's best-case 57%. DPO also achieves a higher maximum win rate than Best-of-N. DPO is substantially more robust to sampling temperature than PPO.
- **Out-of-distribution generalisation.** Evaluated zero-shot on CNN/DailyMail (different distribution), DPO GPT-4 win rates (0.36/0.31 at temps 0/0.25) exceed PPO (0.26/0.23), despite DPO not using the additional unlabelled Reddit prompts PPO uses.
- **Single-turn dialogue (Anthropic HH, Pythia-2.8B).** DPO is the only computationally efficient method that improves over chosen completions in the test set. PPO from a published checkpoint fails to beat the base Pythia-2.8B model. DPO matches or beats Best-of-128 Preferred-FT.
- **Human evaluation.** In TL;DR human study, DPO samples preferred 58% of the time over greedy PPO. GPT-4 judgments correlated with humans at ~70–86% agreement, similar to inter-human agreement.
- **Training stability.** DPO has no value function, no on-policy rollouts, and no reward normalisation. The paper identifies PPO instability as arising from the un-normalised soft value function baseline; DPO sidesteps this entirely.
- **Compute.** DPO is a single-model classification objective; PPO requires training or loading a separate reward/value head and sampling from the policy in the training loop.

## Relevance to the project

DPO is the canonical offline, no-RL-loop alternative to PPO-based RLHF. It establishes that preference optimisation can be reduced to a supervised objective over fixed data — a direction that is central to many subsequent methods. For this project's interest in minimal-sample fine-tuning, DPO is the natural comparison point for any method that learns from preference signal rather than scalar reward: KTO (Ethayarajh et al.) drops the paired-response requirement; ORPO folds the reference-free contrast into SFT; IPO (Azar et al.) corrects the over-optimisation tendency of the BT model; SLiC uses a hinge loss variant. The Back-to-Basics / RLOO paper argues REINFORCE with leave-one-out baselines outperforms DPO on reasoning tasks, and GRPO (DeepSeekMath) subsumes DPO in a unified gradient view of preference and process reward signals.

## Source

- arXiv: https://arxiv.org/abs/2305.18290
- Raw: `../../../raw/research/rl-optimizers/01-03-dpo-rafailov.md`

## Related

- [[_overview]]
- [[ppo]]
- [[instructgpt]]
- [[kto]]
- [[rloo]] — Back-to-Basics paper argues REINFORCE/RLOO outperforms DPO on reasoning benchmarks
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO paper includes DPO in its unified gradient view of preference and process reward objectives
