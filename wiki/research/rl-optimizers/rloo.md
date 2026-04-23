---
name: rloo
description: REINFORCE Leave-One-Out for RLHF; simpler than PPO, beats PPO and DPO on LLM alignment
type: research
---

# Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human Feedback in LLMs (RLOO)

Ahmadian et al. — Cohere / Cohere For AI, arXiv:2402.14740 (2024). The central claim is that most of PPO's machinery is unnecessary in the RLHF setting: because the policy is initialised from a strong pre-trained + SFT model, the action distribution is already concentrated, gradient variance is low, and the bias introduced by actor-critic value bootstrapping outweighs its variance-reduction benefit. The paper revisits the problem formulation, arguing that rewards are only assigned at the end of a full generation, making the token-level MDP an unnecessary complication — the problem reduces to a contextual bandit. Under this framing, vanilla REINFORCE consistently outperforms PPO by 3.2–20.3% in win-rate across all dataset/model pairings, and REINFORCE Leave-One-Out (RLOO) outperforms PPO, DPO, and RAFT across all evaluated settings.

## Method

### Sequence-level vs token-level MDP

PPO models each token as an action, making partial sequences states and requiring a learned value network to estimate per-token advantages via GAE. In practice the reward model only assigns a non-zero intrinsic reward to the `<EOS>` token; all intermediate tokens receive only the KL component. Because environment dynamics are fully deterministic (the next state is the concatenation of the current state and the generated token), the MDP collapses to a bandit: one action (the full generation) from one initial state (the prompt). Modeling partial completions forces a critic, adds a model copy to GPU memory, and introduces bias without providing useful signal [§3.3].

### REINFORCE objective

The bandit framing admits the sequence-level REINFORCE estimator directly:

$$\nabla_\theta J(\theta) = \mathbb{E}_{x \sim \mathcal{D},\, y \sim \pi_\theta(\cdot|x)}\bigl[R(x,y)\,\nabla_\theta \log \pi_\theta(y|x)\bigr]$$

where $R(x,y) = r_\phi(x,y) - \beta \log \frac{\pi_\theta(y|x)}{\pi_\text{ref}(y|x)}$ is the KL-penalised reward. Variance is reduced without introducing bias by subtracting a baseline $b$ with high covariance with the return. A moving-average baseline $b_\text{MA} = \frac{1}{S}\sum_s R(x_s, y_s)$ suffices for the single-sample case [§2.2].

### RLOO: multi-sample baseline

With $k$ i.i.d. online samples $y^{(1)},\ldots,y^{(k)} \sim \pi_\theta(\cdot|x)$ per prompt, each sample can use the other $k-1$ as an unbiased, parameter-free estimate of the expected return:

$$b_i = \frac{1}{k-1}\sum_{j \neq i} R(x, y^{(j)})$$

The RLOO gradient is then [§2.3, from Kool et al. 2019]:

$$\nabla_\theta J(\theta) = \frac{1}{k}\sum_{i=1}^{k}\left[R(x,y^{(i)}) - b_i\right]\nabla_\theta \log \pi_\theta(y^{(i)}|x)$$

This baseline is constructed on-the-fly at each training step and requires no learned value network, no extra model copy, and no critic training. All $k$ samples contribute to the policy update, unlike RAFT which discards all but the top-ranked sample.

## Claims

**Win-rates (GPT-4 simulated, vs SFT reference completions)** — Table 1 of the paper:

| Method | TL;DR | HH (Pythia-6.9B) | HH (Llama-7B) |
|---|---|---|---|
| RLOO (k=4) | **77.9** | **43.7** | **64.1** |
| RLOO (k=2) | **74.2** | **47.6** | **62.2** |
| RAFT (k=4) | 73.2 | 42.1 | 63.3 |
| RAFT (k=2) | 72.1 | 37.7 | 58.4 |
| REINFORCE w/ baseline | 70.7 | 37.9 | 55.3 |
| Vanilla PG | 70.4 | 36.4 | 52.3 |
| PPO | 67.6 | 29.2 | 32.0 |
| DPO | 66.6 | 39.0 | 61.9 |

- **REINFORCE beats PPO** by 3.2% (TL;DR) to 20.3% (HH Llama) in win-rate across all settings [§1, Table 1].
- **RLOO (k=4) beats PPO** by 10.3, 14.5, and 32.1 points on TL;DR, HH (Pythia), and HH (Llama) respectively [§5.2].
- **Sample efficiency.** RLOO (k=2) either matches or outperforms RAFT (k=4) on both datasets — half the sampling budget for equal or better performance [§5.1, Fig. 3].
- **Fluency and diversity.** RLOO achieves substantially lower perplexity than PPO (27.6 vs 40.4 on HH-Llama) while maintaining comparable diversity [Table 2].
- **Robustness.** Under increased KL penalty ($\beta = 0.5, 1.0$) and added reward noise ($\sigma = 3.0, 5.0$), RLOO degrades far less than RAFT, which depends on accurate ranking of the top sample [§5.2.2].
- **Compute.** Eliminating the value network removes one model copy from memory. PPO requires loading up to 4 models simultaneously (generator, reference, critic, reward model); RLOO requires only 3 (generator, reference, reward model). The paper describes RLOO as "3× faster, 70% less RAM" relative to PPO in implementation [§1 introduction context; the exact numbers are cited in downstream literature referencing this work].

## Relevance to the project

RLOO is the natural lightweight default for single-sample or small-group RL fine-tuning. Its group-relative baseline — using peer samples from the same prompt to normalise reward — is exactly the mechanism GRPO ([[../rlvr-mechanics/deepseekmath-grpo]]) extends to the RLVR setting: GRPO replaces the reward model with a verifier and sets group size $G$ as the RLOO $k$. The DeepSeekMath paper cites RLOO explicitly as the ancestral estimator. For the project's single-sample RLVR regime, RLOO with small $k$ (2–4) is the lowest-overhead online RL option that still gets unbiased variance reduction — no critic, no value network, no separate baseline model. The key caveat is that the paper evaluated RLOO only on dense reward (reward model at sequence end) in the RLHF setting; the project's verifier-based sparse reward and very small curricula ($N \approx 10$–$100$) extend beyond the evaluated regime, so GRPO's process-reward extensions may still be needed.

## Source

- arXiv: https://arxiv.org/abs/2402.14740
- Raw: `../../../raw/research/rl-optimizers/06-04-rloo-ahmadian.md`

## Related

- [[_overview]] — RL optimizers overview
- [[ppo]] — PPO, the baseline RLOO is compared against throughout
- [[dpo]] — DPO, the RL-free baseline RLOO outperforms
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO extends RLOO's group-relative baseline to verifier-based RLVR
