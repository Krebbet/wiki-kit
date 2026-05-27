# Comparing Fixed and Adaptive Computation Time for Recurrent Neural Networks

Fojo et al. (2018) propose Repeat-RNN as an ablation of [[act]]: a fixed-$\rho$ recurrent loop that repeats each input token a constant number of times rather than adaptively halting. Across both tasks tested (parity and cumulative addition), Repeat-RNN matches or outperforms ACT in solution rate and training steps, sometimes converging more than 2× faster. The result challenges the necessity of the adaptive halting mechanism for these tasks and suggests the depth benefit of ACT may derive primarily from repeated computation, not from the halting signal.

## Core comparison

**Architectures compared:** vanilla RNN / LSTM (baseline), ACT-RNN / ACT-LSTM (Graves 2016), and Repeat-RNN / Repeat-LSTM (the proposed ablation). Repeat-RNN differs from ACT in exactly one dimension: $\rho$ is a fixed hyperparameter, not learned. The input augmentation (binary flag distinguishing first vs. repeated sub-steps) is shared with ACT; the final state is taken as the last sub-step's hidden state rather than a probability-weighted mean.

**Tasks:** Two synthetic tasks from the original ACT paper — (1) parity/XOR of a 64-element vector (single-token, no recurrence across time), (2) cumulative digit addition over a length-5 sequence (requires coherent hidden state). Small model scale: 128 tanh units for parity, LSTM for addition.

**Hyperparameter tradeoff:** ACT requires tuning $\tau$ (ponder cost); Repeat-RNN requires tuning $\rho$ (repetition count). Both are task-dependent with no principled way to set a priori.

## Key findings

**Repeat-RNN matches or beats ACT on both tasks.**

- Parity: Repeat-RNN $\rho=2$ solves the task in 22k training steps vs. 53k for the best ACT configuration ($\tau=10^{-2}$). Average repetitions used by the winning ACT config (1.81) are nearly identical to $\rho=2$ (2.00) — ACT is not learning sparse computation; it is learning near-uniform repetition.
- Addition: ACT solves with ~5 repetitions on average; Repeat-RNN $\rho=3$ also solves (997k steps), and $\rho=5$ outperforms most ACT configs (514k steps).
- Baseline RNN (no repetition) fails to solve either task regardless of training budget, confirming that depth of computation per token matters.

**Instability at large $\rho$.** Both tasks show degradation when $\rho$ is increased beyond a task-appropriate value. Authors attribute this to exploding gradients over longer unrolled sequences. ACT does not exhibit this because its ponder cost penalizes excessive computation.

**Adaptive halting contributes negligible benefit over fixed-$N$ repetition** on these tasks: the key signal is repeated computation, not the routing itself.

## Implications for ACT vs. PonderNet choice

This result tightens the interpretation of [[act]] and [[pondernet]] for Experiment 1. If adaptive halting provides no measurable advantage over fixed-$\rho$ loops on well-characterized tasks, then the halting mechanism (whether ACT or PonderNet) must be justified on grounds other than raw task performance:

1. **Computation efficiency.** ACT can vary $N(t)$ per token, potentially using fewer FLOPs on easy tokens. Repeat-RNN cannot. In a practical loop-LLM setting with heterogeneous token difficulty, this remains the strongest argument for adaptive halting.
2. **Challenge 5 (trivial-solution trap).** If the router can match adaptive-compute performance by simply fixing $N$ and ignoring the halting signal, there is strong pressure toward the trivial solution: route everything uniformly. This paper is direct evidence that the trivial fixed-$N$ solution is competitive in task-accuracy terms — the router must be regularized or incentivized to actually discriminate, or the evaluation must be structured so that uniform routing is suboptimal (e.g., mix of very easy and very hard examples with different optimal depths).
3. **PonderNet specificity.** PonderNet's geometric prior and KL regularization were motivated by gradient instability in ACT's remainder trick, not by task accuracy. This paper suggests that accuracy parity with fixed-$N$ is expected even under ACT — the PonderNet / ACT choice should be made on gradient stability and training dynamics grounds, not on whether halting is "necessary" for the task.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Low | Fixed vs. adaptive repetition concerns compute allocation within a single shared block, not block isolation or swappability. |
| **G2** (dynamic parameter allocation) | Medium | Direct comparison to adaptive vs. fixed allocation of compute per token; shows fixed-$N$ is competitive, raising the bar for any learned-allocation mechanism to justify itself. |
| **G3** (token-conditional routing with learned halting) | High | Core evidence for the trivial-solution trap in Experiment 1. If fixed-$\rho$ matches adaptive routing in accuracy, the router's learning signal is weak or absent without additional structure. |

## Credibility

arXiv preprint (March 2018); 4-page workshop-style paper (ICLR 2018 workshop likely, not published at a full venue). Single-GPU experiments. Tasks are exactly the two from the original ACT paper, ensuring direct comparability. Code publicly available (TensorFlow + PyTorch). Scope is narrow: synthetic toy tasks only, small scale, no language modeling or generation benchmarks. Results should be treated as an existence proof and ablation signal, not a definitive empirical claim at scale.

## Empirical claims

- Repeat-RNN $\rho=2$ solves parity in 22k steps vs. ACT's 53k (best config). _(Table 1)_
- Repeat-RNN $\rho=3$ solves addition in 997k steps; $\rho=5$ in 514k steps; ACT $\tau=10^{-2}$ in 899k steps. _(Table 2)_
- Winning ACT configs use average repetitions of 1.81–2.04 (parity) and 5.08–6.74 (addition), closely tracking the optimal fixed $\rho$ values. _(Tables 1–2)_
- Too-large $\rho$ causes instability (accuracy collapse late in training), attributed to exploding gradients. _(Fig. 2, 6, 8)_

## Open questions

- Does the fixed-$N$ parity result hold at scale? In generative LLMs with heterogeneous token distributions, easy/hard token mix may make adaptive halting matter more.
- How much of the Repeat-RNN advantage in training speed is due to avoiding ACT's biased gradients at the halting boundary vs. simpler optimization landscape?
- What task structure would make adaptive halting strictly necessary (not merely helpful)? The authors flag this as future work.

## Source

- `raw/research/loop-challenges/01-comparing-act-fixed-abs.md`
- `raw/research/loop-challenges/07-comparing-act-fixed-pdf.md`

## Related

[[act]], [[pondernet]], [[universal-transformers]], [[huginn]]
