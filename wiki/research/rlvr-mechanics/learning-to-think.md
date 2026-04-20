# Learning to Think: Information-Theoretic Reinforcement Fine-Tuning for LLMs

L2T (Wang et al., NeurIPS 2025) reframes RL fine-tuning as an episodic MDP with a *dense, universal process reward* derived from internal model signals — specifically, episode-wise information gain in parameters. The reward needs no external annotator or task-specific evaluator and is plugged into a GRPO outer loop. Reported gains: ~3.7% absolute pass@1 over GRPO and ~2x token efficiency on AIME/MATH/Minerva at 1.5B scale.

## Method

- **Episodic reformulation.** A query–response trace is split by `<think>...</think>` markers into K episodes; the MDP state at episode k is `s_k = (x, z_{1:k-1})`, the action `z_k` is a token block (Sec 4.1).
- **Dense process reward** (Eq. 3):
  `r_k^prg = [J_r(π_θ(·|s_k, z_k)) − J_r(π_θ(·|s_k))]  −  β · [I(θ_k; s_k) − I(θ_{k-1}; s_{k-1})]`
  The first bracket is *fitting information gain* (rise in correctness probability after consuming z_k); the second is a *parameter compression penalty* on context-induced parameter MI, discouraging redundant absorption.
- **Tractable estimator.** The MI penalty is intractable in θ ∈ R^d. They take a low-rank SVD proxy `θ̃ ∈ R^r` (r/d ≈ 1–10% at 1.5B; 0.1–1% at 7B), assume Gaussian posterior, and use a Fisher-information second-order Taylor expansion (Theorem 4.2) — one extra forward call per episode.
- **Policy update.** Riding GRPO: episode-level reward `R_{i,k} = r_i^out / K_i + α r_{i,k}^prg`, redistributed to tokens by log-prob surprise weights, normalised within group, plugged into clipped PG with KL.

## Claims

- DeepScaleR-1.5B + L2T: avg 57.8 vs GRPO 55.0 across AIME24/25, AMC23, MATH500, MinervaMATH (Table 1, +3.3 abs).
- DeepSeek-R1-Distill-Qwen-1.5B + L2T: avg 49.2 vs GRPO 46.0 (Table 1, +4.3 abs).
- Token cost: ~18% of base model, ~50% of GRPO, ~80% of MRT/ReST-MCTS at matched accuracy (Fig 2, Fig 3).
- Outcome-only RL frequently doubles the minimal token count needed; accuracy peaks around 16–20 episodes and *declines* after (Fig 1, Sec 3.2).

## Sample efficiency

Fine-tunes DeepScaleR on **919 AIME problems (1989–2023)** and the Distill-Qwen variant on a 4k-sample slice of NuminaMath. Not single-sample, but small-corpus and process-dense — every episode yields a learning signal regardless of label availability. The information-theoretic reward is annotation-free, so it could in principle drive very low-data regimes where an external PRM is unaffordable.

## Relevance to the project

L2T's parameter-information-gain reward is essentially the formalism David's "concept-based learning" needs: a per-step measure of *how much the model's state moved* given a single example. The Fisher/SVD low-rank proxy is a cheap way to monitor concept absorption per sample, and the compression penalty matches the "don't overfit to surface form" intuition behind concept distillation. Worth borrowing the estimator wholesale; the GRPO host is replaceable.

## Source

- arXiv: 2505.10425
- Raw markdown: `../../../raw/research/single-sample-llm-learning/04-04-learning-to-think.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/04-learning-to-think.pdf`

## Related

- [[deepseekmath-grpo]] — host RL algorithm
- [[rl-sparse-subnetwork]] — explains why information-gain estimates may be low-rank in practice
- [[math-shepherd]], [[lets-verify-step-by-step]] — external PRM alternatives L2T explicitly avoids
