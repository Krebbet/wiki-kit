# Improving Data Efficiency for LLM Reinforcement Fine-tuning Through Difficulty-targeted Online Data Selection and Rollout Replay

Sun et al. (2025) introduce two orthogonal techniques to slash GRPO compute: (1) **DOTS**, an online data-selection rule that prefers questions whose *current-policy* failure rate is near 0.5 (where the GRPO advantage variance is maximal), with adaptive difficulty estimated cheaply via attention over a small reference set; and (2) **RR**, a FIFO rollout-replay buffer with importance-sampling-corrected GRPO loss. Together they cut total RL fine-tuning time 23–62% across six LLM-dataset pairs without losing accuracy.

## Method
- **Adaptive difficulty:** at step $t$, $d_q^{(t)} = \frac{1}{G}\sum_i (1 - r_i^{(t)})$ with $G$ rollouts.
- **Attention-based prediction:** roll out only on a reference subset $D_{\text{ref}}$ of $K$ ≈ 128–256 questions; for unseen $q$, embed and compute $\hat{d}_q^{(t)} = \sum_i a_i d_i^{(t)}$ with $a_i = \mathrm{softmax}(z_q^\top z_i / \sqrt{h})$. Calibrate via Platt scaling on $(\mu^{(t)}, \sigma^{(t)})$.
- **DOTS sampling:** $P(q) \propto \exp(-|\hat{d}_q - 0.5|/\tau)$. Theorem 1: $\mathbb{E}[\|g\|^2] \propto p(1-p)(1-1/G)$, maximized at $p=0.5$.
- **Rollout replay:** generate fresh rollouts for $\delta B$ of the batch, fill $(1-\delta)B$ from FIFO buffer. Off-policy correction via importance ratio $\tilde r_{i,t}(\theta) = \pi_\theta / \pi_{\theta_{\text{behavior}}}$ inside the clipped GRPO objective.

## Claims
- Total training time: -23% to -62% across 6 (model, dataset) combos (Tab. 1). Average 40.7%; best result Qwen2.5-3B + DeepMath at 61.65%.
- Per-step cost: RR alone -11% to -13% (rollout generation is 46–54% of per-step time).
- Difficulty prediction: Pearson $\rho > 0.7$ with ground-truth adaptive difficulty across all settings (Tab. 2).
- DOTS lifts the *effective question* ratio (those with non-degenerate group reward) substantially above vanilla GRPO every step (Fig. 4).
- Trained adapter + calibration is necessary: off-the-shelf Qwen embeddings give much weaker correlation (Tab. 8).
- Generalizes outside math (Fig. 6 right) and complements an external curriculum baseline.

## Sample efficiency
This is the *opposite* end of the single-sample spectrum — a full pool with smarter sampling — but it operationalizes the same insight that drives 1-shot RLVR: gradient signal is concentrated where the policy's success rate is interior (not 0 or 1). DOTS automates the discovery of "interesting" examples that 1-shot RLVR finds via historical-variance hand-selection. RR is unrelated to single-sample but reduces wall-clock for any rollout-bounded RLVR.

## Relevance to the project
Useful as a diagnostic and scaling lens for David's design. Two takeaways: (1) the $p \to 0.5$ rule is a concrete, theoretically motivated recipe for picking the "right" single example or small concept seed — i.e. one where the model is uncertain enough to benefit; and (2) the attention-over-reference-set trick gives a cheap way to score every candidate concept by adaptive difficulty without full rollouts, which could become a concept-quality scorer in a single-sample workflow. The rollout-replay piece is more relevant if/when David scales beyond a single sample and wants on/off-policy mixing.

## Source
- arXiv: 2506.05316
- Raw markdown: `../../../raw/research/single-sample-llm-learning/06-06-data-efficiency-rft.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/06-data-efficiency-rft.pdf`

## Related
- [[1-shot-rlvr]]
- [[rlvr-incentivizes-reasoning]]
- [[../rlvr-mechanics/_overview]]
- [[../data-efficient-survey/limited-data-ft-survey]]
