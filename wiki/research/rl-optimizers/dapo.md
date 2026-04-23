---
name: dapo
description: Open-source GRPO-derivative from ByteDance; four-trick recipe; 50 AIME'24 on Qwen2.5-32B
type: research
---

# DAPO: An Open-Source LLM Reinforcement Learning System at Scale

Yu et al. — ByteDance Seed + Tsinghua AIR, arXiv:2503.14476 (2025). DAPO (Decoupled Clip and Dynamic sAmpling Policy Optimization) is an open-source GRPO-derivative targeting long-CoT RLVR. Starting from a naive GRPO run that yielded only 30 points on AIME 2024 from Qwen2.5-32B, the authors diagnose three failure modes — entropy collapse, reward noise from truncated samples, and zero-gradient batches — and address each with a targeted fix. The resulting four-trick system reaches 50 points on AIME 2024, surpassing DeepSeek-R1-Zero-Qwen-32B (47 points) in 50% fewer training steps. Full training code, algorithm, and dataset (DAPO-Math-17K) are released.

## Method

DAPO modifies GRPO in four ways and drops the KL-to-reference penalty entirely. The KL term is removed on the grounds that long-CoT reasoning requires the policy to diverge substantially from the reference; the regularisation is therefore counterproductive (§2.3).

The full objective is:

$$J_\text{DAPO}(\theta) = \mathbb{E} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \min\!\left( r_{i,t}(\theta)\,\hat{A}_{i,t},\; \text{clip}\!\left(r_{i,t}(\theta), 1-\varepsilon_\text{low}, 1+\varepsilon_\text{high}\right)\hat{A}_{i,t} \right) \right]$$

$$\text{s.t.}\quad 0 < \bigl|\{o_i \mid \text{is\_equivalent}(a, o_i)\}\bigr| < G$$

where $r_{i,t}(\theta) = \pi_\theta(o_{i,t} \mid q, o_{i,<t}) / \pi_{\theta_\text{old}}(o_{i,t} \mid q, o_{i,<t})$ and $\hat{A}_{i,t} = (R_i - \text{mean}(\{R_i\}_{i=1}^G)) / \text{std}(\{R_i\}_{i=1}^G)$.

### 1. Clip-Higher

Standard PPO/GRPO uses a symmetric clip range $[1-\varepsilon, 1+\varepsilon]$. With $\varepsilon=0.2$, a low-probability exploration token ($\pi_{\theta_\text{old}} = 0.01$) can increase to at most $0.012$, while a high-probability exploitation token ($\pi_{\theta_\text{old}} = 0.9$) can reach $1.08$ — an asymmetry that suppresses exploration and drives entropy collapse. DAPO decouples the bounds: $\varepsilon_\text{low} = 0.2$, $\varepsilon_\text{high} = 0.28$ (default). Increasing $\varepsilon_\text{low}$ would suppress tokens to zero and collapse the sampling space, so only the upper bound is relaxed.

### 2. Dynamic Sampling

When all $G$ rollouts for a prompt are correct (or all wrong), the group-normalised advantage is zero and contributes no gradient. As training progresses, the fraction of all-correct prompts grows monotonically (Figure 3b), shrinking the effective batch and amplifying gradient variance. DAPO enforces the constraint $0 < |\{o_i \mid \text{correct}\}| < G$ by over-sampling and filtering prompts at the batch boundary before any gradient step. Sampling cost per batch is therefore dynamic; the authors report wall-clock time is not significantly affected because long-tail generation already dominates synchronised rollout time.

### 3. Token-Level Policy Gradient Loss

GRPO normalises by averaging token losses within each sequence, then averaging across sequences — giving equal weight to every sample regardless of length. Tokens in long responses therefore contribute disproportionately less per token to the batch gradient, which (a) weakens learning from high-quality long traces and (b) fails to penalise low-quality patterns (gibberish, repetition) that manifest in long outputs, causing pathological entropy growth and length inflation. DAPO replaces the per-sequence mean with a single sum over all tokens in the batch divided by total token count $\sum_i |o_i|$, so every token contributes uniformly to the gradient update.

### 4. Overlong Reward Shaping

Truncated samples are penalised by default with a hard $-1$ reward. This introduces noise because a valid reasoning chain may simply be long, not wrong. DAPO applies **Soft Overlong Punishment**:

$$R_\text{length}(y) = \begin{cases} 0 & |y| \leq L_\text{max} - L_\text{cache} \\ \dfrac{(L_\text{max} - L_\text{cache}) - |y|}{L_\text{cache}} & L_\text{max} - L_\text{cache} < |y| \leq L_\text{max} \\ -1 & L_\text{max} < |y| \end{cases}$$

The penalty ramps linearly from $0$ to $-1$ over a cache window $L_\text{cache}$ below $L_\text{max}$, then hard-clips at $-1$ for truly truncated responses. Default: $L_\text{max} = 16{,}384$, $L_\text{cache} = 4{,}096$, generation cap $= 20{,}480$ tokens. This is added to the rule-based correctness reward (§2.4).

## Claims

Progressive ablation on AIME 2024 avg@32, Qwen2.5-32B base (Table 1):

| Configuration | AIME 2024 avg@32 |
|---|---|
| DeepSeek-R1-Zero-Qwen-32B | 47 |
| Naive GRPO | 30 |
| + Overlong Filtering | 36 |
| + Clip-Higher | 38 |
| + Soft Overlong Punishment | 41 |
| + Token-level Loss | 42 |
| + Dynamic Sampling (full DAPO) | **50** |

- DAPO reaches **50 points** on AIME 2024 with Qwen2.5-32B base, surpassing DeepSeek-R1-Zero-Qwen-32B's **47 points**.
- DAPO achieves this in **50% of the training steps** required by DeepSeek-R1-Zero-Qwen-32B (Figure 1).
- Dynamic Sampling specifically reduces convergence time despite increasing per-step sampling cost (Figure 6).

## Relevance to the project

DAPO is the reference implementation of "GRPO done right for long-CoT RLVR" — the four tricks are independent, composable, and each addresses a concrete failure mode rather than a hyper-parameter choice, making them directly applicable to any small-N RL setting. Dynamic Sampling is the most immediately relevant: when training on a single sample (or a very small curriculum), most rollout groups will be all-correct or all-wrong at different points in training, producing vanishing gradients exactly when the model is near the learning boundary. Filtering to only mixed-outcome groups is a near-zero-cost fix that concentrates gradient signal on the prompts where the model is uncertain — the same regime a single-sample concept learner must inhabit. The token-level loss is also consequential for long-CoT traces, where a single correct extended reasoning chain must not be drowned out by shorter, noisier responses in the batch.

## Source

- arXiv: https://arxiv.org/abs/2503.14476
- Raw: `../../../raw/research/rl-optimizers/05-06-dapo-bytedance.md`

## Related

- [[_overview]]
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO ancestor
- [[dr-grpo]] — sibling critique of GRPO
- [[gspo]] — alternative path (group sequential policy optimisation)
