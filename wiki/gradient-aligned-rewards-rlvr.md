# Gradient-Aligned Rewards (GAR)

Tsinghua/Renmin/CAS/USTC/ANU/PKU/Macau (arXiv:2609.03342) propose Gradient-Aligned Reward (GAR): a dense, rollout-level RLVR reward that scores each *correct* rollout by cosine similarity between its truncated output-layer gradient and an expert-anchor gradient derived from the dataset's own chain-of-thought solution — fixing binary-outcome RLVR's inability to rank correct trajectories once a GRPO group becomes all-correct.

## Method

Reward-shaping add-on to GRPO/REINFORCE++, not a new optimizer. The verifier gate is retained (incorrect rollouts get zero bonus). Instead of the full parameter gradient, GAR freezes the transformer body, does a no-grad forward pass to get output-layer hidden states, and backprops a teacher-forcing CE loss only through the output projection — cost O(V×d) instead of O(|θ|). The gradient-activation signal S_t = G_t ⊙ h̄_t is averaged over the response span and L2-normalized into a per-rollout vector; the dataset's shipped CoT solution is mapped through the same procedure to a cached expert-anchor vector. Reward = cosine(rollout vector, anchor vector), group-centered, clipped at zero, added atop base reward. Theorem 1 shows this truncated-gradient cosine is bi-Lipschitz-equivalent to output-layer NTK similarity; Theorem 3 proves the shaping is "safe" (never degrades a correct response below base reward).

## Results

Trained Qwen3-4B/8B-Base from scratch (no SFT warmup), full-parameter RL. GAR-GRPO beats GRPO by +10–33% relative pass@1 across IMO-AnswerBench/HMMT'25/HMMT'26/AIME'26 at both scales (largest: HMMT'25 4B, +52.4% relative with REINFORCE++). Zero-shot transfer despite math-only training: +2.4–2.6 pp on GPQA Diamond and MMLU-Pro. Beats gradient-based competitors Grad2Reward and G2RL on every benchmark at <9% wall-clock overhead (vs. their 37–44%). Ablation confirms the verifier gate is load-bearing: removing it collapses GAR below baseline.

Code released: github.com/LQgdwind/GAR.

## Applicability

Any RLVR pipeline training on a corpus with shipped expert CoT solutions (NuminaMath-CoT-style) can add GAR as a near-free reward hook — works with LoRA/PEFT policies too since only the output-layer needs gradients. Not applicable to open-ended/non-verifiable tasks (no verifier gate to anchor on).

## Related

- [[vimpo]] — closest sibling: also a critic-free, analytically-grounded credit-assignment signal, but token-level via KL-regularized value recurrence vs. GAR's rollout-level gradient-cosine.
- [[token-gradient-cancellation]] / [[delta-token-credit]] — token-level gradient-space diagnoses of GRPO; GAR uses gradients as a reward *feature* rather than to detect/suppress cancellation.
- [[rrc-reward-ranking]] — same "denser reward without a separate trained reward model" thread.
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — complementary, orthogonal axis (rollout-level correctness-ranking vs. token-level relevance-weighting).
