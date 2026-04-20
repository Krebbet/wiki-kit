# RLVR Mechanics & Sparse Subnetwork

Theme covering the *mechanics* of RL with verifier rewards (RLVR) for LLM reasoning: the canonical optimiser (GRPO), what RL actually changes inside the model (sparse subnetwork), and how to densify the reward signal without external annotators (information-theoretic process reward in L2T).

## Pages

- [[deepseekmath-grpo]] — GRPO, the critic-free, group-relative PPO variant; unified gradient view of SFT/RFT/DPO/PPO/GRPO.
- [[rl-sparse-subnetwork]] — RL fine-tuning modifies only 5–30% of weights across seven algorithms; updates are sparse but full-rank; subnetwork-only retraining recovers full performance.
- [[learning-to-think]] — L2T: episodic GRPO with a universal information-gain process reward computed via PAC-Bayes + Fisher / low-rank SVD, no external PRM.

## Cross-cutting themes

**RL is a micro-edit, not a re-parameterisation.** Balashov shows RL touches a small (5–30%), reproducible, but high-rank subset of weights — including specifically on DeepSeek-Math 7B + GRPO (75% sparsity). LayerNorms are essentially never touched. This reframes "fine-tune with RL" from "shift the whole network into a new policy" to "find and turn a small set of behavioural knobs". L2T's low-rank Fisher proxy (r/d ≈ 1–10% at 1.5B) is dimensionally consistent with where this subnetwork lives, even though L2T is motivated by tractability rather than empirical sparsity.

**The reward, not the optimiser, is the bottleneck for sample efficiency.** GRPO's contribution is *engineering* (drop the critic, baseline from group); the unified gradient table in Sec 5 makes clear that SFT, RFT, DPO, PPO, and GRPO differ mostly in their gradient coefficient. L2T's contribution is to replace a sparse outcome reward with a dense, *annotation-free* per-episode information-gain signal. The implication for low-data work: design the coefficient to extract maximum gradient signal per sample (information-gain, group-relative advantage, process reward), and the optimiser is largely interchangeable.

**Outcome-only RL is wasteful and self-defeating.** L2T's Sec 3.2 measurements on Omni-MATH show GRPO-trained DeepScaleR uses >2x the minimum tokens needed and accuracy *peaks at ~16–20 episodes then declines* due to attention dilution and context truncation. Adding a length penalty alone makes things worse (Table 1). Process-dense rewards are needed to extract the full benefit of test-time compute scaling.

**Concept-based fine-tuning is mechanically supported.** If RL effectively edits a small, consistent subnetwork (Balashov), and if information gain per episode can be measured cheaply via Fisher/SVD (L2T), then a single training example can be used to (a) identify *which* knobs the example wants to turn and (b) quantify *how far* they actually moved — both of which are the missing primitives for a single-sample, concept-based fine-tuner.

## Method comparison

| Method | Reward source | Critic | Density | Annotation cost | Reported gain |
|---|---|---|---|---|---|
| PPO | learned RM, per-token KL in reward | yes (V_φ ≈ |π_θ|) | sparse outcome | RM training | baseline |
| GRPO | learned RM, group-relative baseline | no | sparse outcome (or PRM step) | RM training | +5 MATH over Instruct |
| GRPO + PRM | step-level PRM | no | dense process | PRM + step labels | marginal over outcome |
| L2T | internal info-gain (Fisher/SVD) on top of GRPO | no | dense per-episode | none | +3.7 vs GRPO, ~2x token efficient |
| Subnetwork-only RL (Balashov) | any RL | depends on host | inherits host | identify mask once | matches/exceeds θ_full |

## Open questions

- Does the L2T information-gain reward, computed on the low-rank proxy θ̃, in fact correlate with updates landing in Balashov's RL-induced subnetwork? Both papers point at the same low-dimensional structure but never co-measure.
- Is the cross-algorithm subnetwork overlap evidence of a *task* subnetwork or an *alignment-shaped* subnetwork? Balashov's overlap analysis spans alignment and math RL; the distinction matters for transfer.
- L2T uses 919 AIME problems and 4k NuminaMath samples. How far down the data axis does the information-gain reward continue to help — does it work in the single-sample regime that motivates this wiki?
- GRPO requires G rollouts per prompt for the baseline. In single-sample RLVR, what is the right G, and does group-relative variance reduction collapse when the prompt distribution is degenerate?
- Can the Balashov mask be discovered without a full RL run — e.g., from a few rollouts and Fisher information — and used as a hard constraint in single-sample training?

## Source PDFs

- `../../../raw/research/single-sample-llm-learning/pdfs/04-learning-to-think.pdf`
- `../../../raw/research/single-sample-llm-learning/pdfs/05-rl-sparse-subnetwork.pdf`
- `../../../raw/research/single-sample-llm-learning/pdfs/F-1-deepseekmath-grpo.pdf`

## Related themes

- [[single-sample-rl-finetuning]]
- [[process-reward-models]]
