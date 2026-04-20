# DeepSeekMath / GRPO: Group Relative Policy Optimization

Shao et al. (DeepSeek-AI, 2024) introduce **GRPO**, a critic-free PPO variant that has become the canonical RL-from-verifier-reward (RLVR) algorithm for LLM reasoning. Applied to DeepSeekMath-Instruct 7B, GRPO lifts MATH from 46.8% → 51.7% and GSM8K from 82.9% → 88.2%, the first open 7B to break 50% on competition MATH without tools or voting. The paper also presents a unified gradient view of SFT, RFT, DPO, PPO, and GRPO.

## Method

- **Drop the critic.** PPO trains a value network V_φ of comparable size to π_θ; GRPO removes it. For each prompt q, sample a *group* of G outputs `{o_1, ..., o_G}` from π_{θ_old} and use the group's reward statistics as the baseline.
- **Group-relative advantage.** Score outputs with reward model r_φ to get `r = {r_1, ..., r_G}`. Outcome-supervision: normalise `Ã_i = (r_i − mean(r)) / std(r)` and assign that advantage to *every token* of o_i. Process-supervision: PRM scores each step; per-token advantage is the sum of normalised step rewards from the current step onward.
- **Objective** (Eq. 3):
  `J_GRPO(θ) = E_{q, {o_i}} [ (1/G) Σ_i (1/|o_i|) Σ_t min(ρ_{i,t} Â_{i,t}, clip(ρ_{i,t}, 1−ε, 1+ε) Â_{i,t}) − β D_KL(π_θ || π_ref) ]`
  with `ρ_{i,t} = π_θ(o_{i,t}|q,o_{i,<t}) / π_{θ_old}(o_{i,t}|q,o_{i,<t})`.
- **KL placement.** Unlike PPO (KL inside per-token reward), GRPO adds D_KL directly to the loss using Schulman's positive unbiased estimator.
- **Iterative variant** (Algorithm 1): periodically retrain the reward model on fresh policy rollouts (10% replay), reset π_ref ← π_θ, continue.
- **Unified paradigm.** Sec 5 frames SFT/RFT/Online-RFT/DPO/PPO/GRPO as variants of the same gradient form, differing in (data source, reward function, gradient coefficient).

## Claims

- DeepSeekMath-RL 7B (after GRPO on ~144k GSM8K+MATH CoT prompts): GSM8K 88.2 (+5.3 over Instruct), MATH 51.7 (+4.9), CMATH 88.8 (+4.2) — RL gains transfer out-of-domain (Sec 4.2, Table 5).
- DeepSeekMath-Base 7B reaches Minerva 540B parity on English math while training on a 120B-token Common-Crawl-derived corpus (Table 2).
- Code-pretraining-then-math beats general-pretraining-then-math on both with-tools and without-tools math reasoning (Table 6).
- GRPO uses ~half the memory of PPO at 7B by removing V_φ; with 64 samples/prompt, batch 1024, lr 1e-6, KL coef 0.04, single update per exploration step.
- Process supervision marginally outperforms outcome supervision when a competent PRM exists; iterative RL with replay continues to improve past the single-pass plateau (Fig 6).

## Sample efficiency

GRPO trades sample efficiency for variance reduction: G samples per prompt (G=64 in the paper) for an in-group baseline. Strong gains are obtained from ~144k prompts — small by pretraining standards but well above single-sample. The unified-paradigm view in Sec 5 is the more useful lens for low-data work: the gradient coefficient determines what "counts" as a good sample, and GRPO's group-relative form means a single prompt with high-variance rollouts is informative even with no oracle label.

## Relevance to the project

GRPO is the de-facto host loop David's method will most likely sit inside or alongside. Two specific hooks: (1) the group-relative baseline naturally accommodates a single training prompt rolled out G times — exactly the single-sample regime — without a separate critic to overfit; (2) the per-token advantage broadcast (outcome) or step-sum (process) is the natural insertion point for an information-gain or concept-distance signal in place of (or added to) r_φ. The paper's unified gradient table is also the cleanest map for positioning a new objective among RFT/DPO/PPO/GRPO.

## Source

- arXiv: 2402.03300
- Raw markdown: `../../../raw/research/single-sample-llm-learning/25-F-1-deepseekmath-grpo.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/F-1-deepseekmath-grpo.pdf`

## Related

- [[learning-to-think]] — uses GRPO as the outer loop for an information-theoretic dense process reward
- [[rl-sparse-subnetwork]] — observes 75% sparsity in the GRPO update on this very model
- [[math-shepherd]] — PRM construction style used for the process-supervision variant
- [[deepseek-r1]] — the rule-reward, no-PRM successor that pushed this further
