# DeepSeekMath / GRPO: Group Relative Policy Optimization

Shao et al. (DeepSeek-AI, 2024) introduce **GRPO**, a critic-free PPO variant that has become the canonical RL-from-verifier-reward (RLVR) algorithm for LLM reasoning. Applied to DeepSeekMath-Instruct 7B, GRPO lifts MATH from 46.8% → 51.7% and GSM8K from 82.9% → 88.2%, the first open 7B to break 50% on competition MATH without tools or voting. The paper also presents a unified gradient view of SFT, RFT, DPO, PPO, and GRPO.

## Method

- **Drop the critic.** PPO trains a value network $V_\phi$ of comparable size to $\pi_\theta$; GRPO removes it. For each prompt $q$, sample a *group* of $G$ outputs $\{o_1, ..., o_G\}$ from $\pi_{\theta_\text{old}}$ and use the group's reward statistics as the baseline.
- **Group-relative advantage.** Score outputs with reward model $r_\phi$ to get $r = \{r_1, ..., r_G\}$. Outcome-supervision: normalise $\tilde{A}_i = (r_i - \text{mean}(r)) / \text{std}(r)$ and assign that advantage to *every token* of $o_i$. Process-supervision: PRM scores each step; per-token advantage is the sum of normalised step rewards from the current step onward.
- **Objective** (Eq. 3):
  $$J_\text{GRPO}(\theta) = \mathbb{E}_{q, \{o_i\}} \left[ \frac{1}{G} \sum_i \frac{1}{|o_i|} \sum_t \min(\rho_{i,t} \hat{A}_{i,t}, \text{clip}(\rho_{i,t}, 1-\varepsilon, 1+\varepsilon) \hat{A}_{i,t}) - \beta D_\text{KL}(\pi_\theta \| \pi_\text{ref}) \right]$$
  with $\rho_{i,t} = \pi_\theta(o_{i,t}|q,o_{i,<t}) / \pi_{\theta_\text{old}}(o_{i,t}|q,o_{i,<t})$.
- **KL placement.** Unlike PPO (KL inside per-token reward), GRPO adds $D_\text{KL}$ directly to the loss using Schulman's positive unbiased estimator.
- **Iterative variant** (Algorithm 1): periodically retrain the reward model on fresh policy rollouts (10% replay), reset $\pi_\text{ref} \leftarrow \pi_\theta$, continue.
- **Unified paradigm.** Sec 5 frames SFT/RFT/Online-RFT/DPO/PPO/GRPO as variants of the same gradient form, differing in (data source, reward function, gradient coefficient).

## Claims

- DeepSeekMath-RL 7B (after GRPO on ~144k GSM8K+MATH CoT prompts): GSM8K 88.2 (+5.3 over Instruct), MATH 51.7 (+4.9), CMATH 88.8 (+4.2) — RL gains transfer out-of-domain (Sec 4.2, Table 5).
- DeepSeekMath-Base 7B reaches Minerva 540B parity on English math while training on a 120B-token Common-Crawl-derived corpus (Table 2).
- Code-pretraining-then-math beats general-pretraining-then-math on both with-tools and without-tools math reasoning (Table 6).
- GRPO uses ~half the memory of PPO at 7B by removing $V_\phi$; with 64 samples/prompt, batch 1024, lr 1e-6, KL coef 0.04, single update per exploration step.
- Process supervision marginally outperforms outcome supervision when a competent PRM exists; iterative RL with replay continues to improve past the single-pass plateau (Fig 6).

## Sample efficiency

GRPO trades sample efficiency for variance reduction: $G$ samples per prompt ($G=64$ in the paper) for an in-group baseline. Strong gains are obtained from ~144k prompts — small by pretraining standards but well above single-sample. The unified-paradigm view in Sec 5 is the more useful lens for low-data work: the gradient coefficient determines what "counts" as a good sample, and GRPO's group-relative form means a single prompt with high-variance rollouts is informative even with no oracle label.

## Relevance to the project

GRPO is the de-facto host loop David's method will most likely sit inside or alongside. Two specific hooks: (1) the group-relative baseline naturally accommodates a single training prompt rolled out $G$ times — exactly the single-sample regime — without a separate critic to overfit; (2) the per-token advantage broadcast (outcome) or step-sum (process) is the natural insertion point for an information-gain or concept-distance signal in place of (or added to) $r_\phi$. The paper's unified gradient table is also the cleanest map for positioning a new objective among RFT/DPO/PPO/GRPO.

## Source

- arXiv: 2402.03300
- Raw markdown: `../../../raw/research/single-sample-llm-learning/25-F-1-deepseekmath-grpo.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/F-1-deepseekmath-grpo.pdf`

## Related

- [[learning-to-think]] — uses GRPO as the outer loop for an information-theoretic dense process reward
- [[rl-sparse-subnetwork]] — observes 75% sparsity in the GRPO update on this very model
- [[math-shepherd]] — PRM construction style used for the process-supervision variant
- [[deepseek-r1]] — the rule-reward, no-PRM successor that pushed this further
