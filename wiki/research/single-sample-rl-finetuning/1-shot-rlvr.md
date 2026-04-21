# Reinforcement Learning for Reasoning in Large Language Models with One Training Example

Wang et al. (NeurIPS 2025) show that RLVR with a *single* math problem repeated as the entire training set is enough to elicit large reasoning gains in capable base LLMs. On Qwen2.5-Math-1.5B the chosen example $\pi_1$ lifts MATH500 from 36.0% to 73.6% and the 6-benchmark average from 17.6% to 35.7%, matching full-set RLVR on a 1.2k DeepScaleR subset. The paper isolates several mechanistic phenomena — post-saturation generalization, cross-category transfer, and rising self-reflection — that suggest the gains are unlocking latent capability rather than teaching new skills.

## Method
- GRPO over a dataset of size 1 (the single example is duplicated to fill the 128-sample batch). Reward is binary outcome correctness; loss has policy-gradient, KL-to-reference and entropy components.
- *Historical variance* data selection: train on full pool for 500 steps, score each example by $v_i = \mathrm{var}(s_{i,1},\dots,s_{i,E})$ over per-epoch training accuracies, rank, and pick the top item ($\pi_1$). Many other examples (incl. low-variance ones) also work.
- Ablations swap weight decay, KL, entropy coefficients to isolate which component drives generalization.

## Claims
- Qwen2.5-Math-1.5B + $\pi_1$: MATH500 36.0% to 73.6%, 6-bench avg 17.6% to 35.7%; non-format gains 8.6% / 7.0% over format-reward baseline (Fig. 1, Tab. 8).
- 2-shot $\{\pi_1,\pi_{13}\}$ matches 7.5k MATH train set (avg 36.6% vs 36.7%) (Fig. 1).
- Cross-domain transfer: 1-shot math RLVR raises ARC-Easy 48.0 to 55.8 and ARC-Challenge 30.2 to 33.4, *better* than full-set RLVR (Tab. 1).
- Works across Qwen2.5-Math-1.5B/7B, Llama-3.2-3B-Instruct, DeepSeek-R1-Distill-Qwen-1.5B and across GRPO/PPO (Tab. 4, Tab. 11).
- Post-saturation generalization: training accuracy on $\pi_1$ saturates by step ~100; test performance keeps climbing for >1k steps; overfitting (gibberish multilingual training-trace output) only emerges after ~1.4k steps and even then test outputs remain coherent (Fig. 2).
- Ablations (Tab. 5): policy-gradient loss alone reproduces most of the gain; entropy loss adds ~4% on MATH500 / 2.5% on AIME24; weight decay does almost nothing — distinguishing this regime from grokking.
- Entropy-loss-only training on $\pi_1$ yields part of the gain (Qwen2.5-Math-1.5B 36.0 to 63.4 on MATH500) but underperforms a pure format-reward baseline (65.0) (Tab. 6).
- Label robustness: a slightly wrong but plausible numeric label (e.g. 12.7 vs true 12.8) preserves performance; a wildly wrong but guessable label is worse than a wildly wrong unguessable one (Tab. 5 rows 11–13).

## Sample efficiency
This is the canonical existence proof for true single-example RL fine-tuning. The training set is literally one prompt-answer pair; gains hold across 5 backbones and 2 RL algorithms. The mechanism is amplification, not teaching: $\pi_1$ is *easy* for the base model (high pre-training pass-rate). RLVR reweights probability mass toward already-present correct reasoning chains and the format/structure that exposes them. Self-reflection token frequency and response length on *test* problems both grow during training despite seeing only one prompt.

## Relevance to the project
The closest available analogue to David's "concept-based, single-sample" hypothesis. Three transferable insights: (1) a single example can act as a generic *exploration prompt* if the reward shapes which existing trajectories survive — concept-learning may be similar amplification rather than gradient memorization; (2) post-saturation generalization implies the loss landscape rewards continued sampling even after the seed is "solved", supporting designs that keep an example active beyond convergence; (3) entropy / exploration regularization is a load-bearing component, not cosmetic — any single-shot scheme should budget for diversity preservation. Caveat: gains depend heavily on a *strong base model with the relevant priors*; this paradigm rides on, rather than instals, capability.

## Source
- arXiv: 2504.20571
- Raw markdown: `../../../raw/research/single-sample-llm-learning/01-01-rl-one-training-example.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/01-rl-one-training-example.pdf`

## Related
- [[critique-ft-one-problem]]
- [[rlvr-incentivizes-reasoning]]
- [[deepseek-r1]]
- [[data-efficiency-rft]]
- [[../rlvr-mechanics/_overview]]
- [[../process-reward-models/_overview]]
