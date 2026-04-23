---
name: ppo
description: PPO replaces TRPO's constrained optimisation with a clipped probability-ratio surrogate, enabling multiple minibatch epochs on the same rollout data via first-order optimisation.
type: research
---

# Proximal Policy Optimization Algorithms

Schulman, Wolski, Dhariwal, Radford, Klimov — OpenAI, arXiv:1707.06347 (2017). PPO achieves trust-region-like stability without conjugate-gradient or line-search by replacing TRPO's KL constraint with a clipped surrogate objective. Clipping the probability ratio $r_t(\theta) = \pi_\theta(a_t|s_t)/\pi_{\theta_\text{old}}(a_t|s_t)$ into $[1-\epsilon, 1+\epsilon]$ forms a pessimistic lower bound on the unconstrained objective, blocking excessively large updates without a hard constraint. Multiple minibatch SGD/Adam epochs are then safe to run on a single batch of rollouts, improving data efficiency over vanilla PG. An actor-critic formulation with GAE advantage estimation is the canonical instantiation.

## Method

**Probability ratio and CPI baseline.** Let $r_t(\theta) = \pi_\theta(a_t|s_t)/\pi_{\theta_\text{old}}(a_t|s_t)$, so $r(\theta_\text{old})=1$. TRPO maximises the conservative-policy-iteration (CPI) surrogate (Eq. 6):

$$L^\text{CPI}(\theta) = \hat{\mathbb{E}}_t\!\left[r_t(\theta)\,\hat{A}_t\right]$$

Without a constraint, unchecked maximisation of $L^\text{CPI}$ causes destructively large updates.

**Clipped surrogate objective (Eq. 7).** The core PPO objective:

$$L^\text{CLIP}(\theta) = \hat{\mathbb{E}}_t\!\left[\min\!\left(r_t(\theta)\hat{A}_t,\;\operatorname{clip}(r_t(\theta),\,1-\epsilon,\,1+\epsilon)\,\hat{A}_t\right)\right]$$

with $\epsilon=0.2$ as default. Taking the min of clipped and unclipped terms makes $L^\text{CLIP}$ a lower bound on $L^\text{CPI}$: improvement from moving $r_t$ outside $[1-\epsilon,1+\epsilon]$ is ignored; degradation is not. $L^\text{CLIP}=L^\text{CPI}$ to first order at $\theta_\text{old}$.

**Adaptive KL variant (Eq. 8).** An alternative (or complement) to clipping:

$$L^\text{KLPEN}(\theta) = \hat{\mathbb{E}}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_\text{old}}(a_t|s_t)}\hat{A}_t - \beta\,\text{KL}[\pi_{\theta_\text{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t)]\right]$$

$\beta$ is adapted each update: halved when $d < d_\text{targ}/1.5$, doubled when $d > 1.5\,d_\text{targ}$, where $d=\hat{\mathbb{E}}_t[\text{KL}[\pi_{\theta_\text{old}},\pi_\theta]]$. Empirically worse than clipping across MuJoCo benchmarks.

**Actor-critic + GAE (Eqs. 9–12).** With shared policy/value parameters, the combined objective is:

$$L^\text{CLIP+VF+S}(\theta) = \hat{\mathbb{E}}_t\!\left[L^\text{CLIP}_t(\theta) - c_1 L^\text{VF}_t(\theta) + c_2 S[\pi_\theta](s_t)\right]$$

where $L^\text{VF}_t = (V_\theta(s_t)-V_t^\text{targ})^2$ and $S$ is an entropy bonus. Advantages are estimated via truncated GAE (Eq. 11):

$$\hat{A}_t = \sum_{k=0}^{T-t-1}(\gamma\lambda)^k\delta_{t+k}, \qquad \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$$

reducing to the $n$-step return estimator at $\lambda=1$.

**Algorithm.** $N$ actors each collect $T$ timesteps; $NT$ samples are used for $K$ epochs of minibatch SGD with batch size $M \leq NT$. Default MuJoCo hyperparameters: $T=2048$, $K=10$, $M=64$, $\gamma=0.99$, $\lambda=0.95$, Adam lr $3\times10^{-4}$.

## Claims

**MuJoCo surrogate ablation (Table 1, 7 tasks, 1M timesteps, avg. normalised score):**

| Variant | Score |
|---|---|
| No clipping or penalty | -0.39 |
| Clipping $\epsilon=0.1$ | 0.76 |
| **Clipping $\epsilon=0.2$** | **0.82** |
| Clipping $\epsilon=0.3$ | 0.70 |
| Adaptive KL $d_\text{targ}=0.01$ | 0.74 |
| Fixed KL $\beta=1$ | 0.71 |

Clipping with $\epsilon=0.2$ dominates all KL-penalty variants and ablations.

**Continuous control vs. prior art (Fig. 3, 7 MuJoCo tasks, 1M timesteps):** PPO (clip) outperforms TRPO, A2C, A2C+Trust Region, CEM, and vanilla PG with adaptive stepsize on almost all environments.

**Atari (Table 2, 49 games, 40M frames, compared against A2C and ACER):**

- By *avg. reward over all training*: PPO wins 30/49, ACER wins 18/49, A2C wins 1/49.
- By *avg. reward over last 100 episodes*: ACER wins 28/49, PPO wins 19/49, A2C wins 1/49.

PPO wins on fast learning; ACER's experience replay gives it an edge on final-performance metrics. PPO's gains are obtained without replay or off-policy correction, only first-order optimisation.

**Humanoid locomotion (Fig. 4):** PPO scales to 3D humanoid tasks (RoboschoolHumanoid, Flagrun, FlagrunHarder) with up to 128 parallel actors; the adaptive-KL variant was independently applied to similar high-DOF locomotion tasks by Heess et al. (2017).

## Relevance to the project

PPO is the substrate that GRPO, DAPO, GSPO, and essentially every RLVR recipe for LLMs either inherit or explicitly modify. [[../rlvr-mechanics/deepseekmath-grpo]] strips PPO's value network $V_\phi$ — the most memory-intensive component at LLM scale — replacing it with a group-relative in-batch baseline, while preserving the clipped-ratio surrogate and the per-token advantage weighting verbatim. Any method operating in the single-sample or low-sample regime needs to understand this lineage: the clipped surrogate determines how far a gradient step can move the policy per update, the KL regularisation term (moved outside the per-token reward in GRPO) controls reference-policy drift, and the absence of $V_\phi$ changes what "baseline variance" even means when $N$ is small. PPO as described here is also the direct algorithm used in InstructGPT-style RLHF (see [[instructgpt]]), making it the historical bridge between the tabula-rasa RL results above and LLM alignment work.

## Source

- arXiv: https://arxiv.org/abs/1707.06347
- `../../../raw/research/rl-optimizers/02-01-ppo-schulman.md`

## Related

- [[_overview]] — rl-optimizers theme overview
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO drops $V_\phi$, keeps clipped-ratio surrogate; canonical LLM PPO descendant
- [[instructgpt]] — canonical application of PPO to LLM alignment (RLHF)
- [[rloo]] — claims REINFORCE with leave-one-out baseline matches or beats PPO for LLM finetuning
