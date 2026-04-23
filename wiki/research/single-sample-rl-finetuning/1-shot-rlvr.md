# Reinforcement Learning for Reasoning in Large Language Models with One Training Example

Wang et al. (NeurIPS 2025) show that RLVR with a *single* math problem repeated as the entire training set is enough to elicit large reasoning gains in capable base LLMs. On Qwen2.5-Math-1.5B the chosen example $\pi_1$ lifts MATH500 from 36.0% to 73.6% and the 6-benchmark average from 17.6% to 35.7%, matching full-set RLVR on a 1.2k DeepScaleR subset. The paper isolates several mechanistic phenomena — post-saturation generalization, cross-category transfer, and rising self-reflection — that suggest the gains are unlocking latent capability rather than teaching new skills.

## Method
- GRPO over a dataset of size 1 (the single example is duplicated to fill the 128-sample batch). Reward is binary outcome correctness; loss has policy-gradient, KL-to-reference and entropy components. The "128" is the GRPO group size $G$, not data replay — GRPO's group-relative advantage $(r_i - \text{mean}(r))/\text{std}(r)$ is identically zero at $G = 1$, so $G > 1$ is structurally required. Rollout diversity comes from stochastic decoding at temperature $> 0$, not from the dataset; the $(1 - 1/G)$ term in [[data-efficiency-rft]] Theorem 1 is why pushing $G$ to 128 (vs the GRPO paper's default 64) extracts more gradient per step in the $N = 1$ regime.
- *Historical variance* data selection: train on full pool for 500 steps, score each example by $v_i = \mathrm{var}(s_{i,1},\dots,s_{i,E})$ over per-epoch training accuracies, rank, and pick the top item ($\pi_1$). Many other examples (incl. low-variance ones) also work. This is a heuristic proxy for the principled within-group-reward-variance quantity formalised by [[data-efficiency-rft]] Theorem 1: $\mathbb{E}[\|g\|^2] \propto p(1-p)(1-1/G)$, peaking at $p = 0.5$. A prompt whose per-epoch accuracy fluctuates is empirically one whose current-policy pass-rate spent time near 0.5 during the calibration run — exactly where the GRPO gradient is strongest. The 500-step full-pool calibration run that historical-variance selection requires is also the mechanism that makes 1-shot RLVR *not quite* a cold-start method.
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

## Side effects and failure modes

The paper documents the training-trace "gibberish multilingual" phenomenon after ~1.4k steps and notes cross-domain transfer is positive (ARC), but does **not** measure forgetting on non-reasoning tasks or tie the training-trace degeneracy to a mechanism. Synthesis from adjacent corpus pages:

**What the paper measures:**
- Training-trace rollouts degrade to gibberish after ~1.4k steps; test outputs stay coherent (Fig 2). Training-trace drift and test-time distribution are dissociable.
- Cross-domain transfer is positive — ARC-Easy 48.0 → 55.8, ARC-Challenge 30.2 → 33.4, better than full-set RLVR (Tab 1).
- Label-robustness asymmetry: wildly-wrong-but-guessable labels are worse than wildly-wrong-unguessable ones (Tab 5).

**What adjacent pages predict but the paper doesn't measure:**
- Blast radius is bounded: [[../rlvr-mechanics/rl-sparse-subnetwork]] shows RL touches only 5–30% of weights, LayerNorms essentially never. Upper bound on how much 1-shot RLVR *can* damage unrelated capabilities.
- "Forgetting" is likely *reweighting*, not deletion: [[rlvr-incentivizes-reasoning]] argues RLVR selects for existing CoT priors. Failure mode is "capability X harder to elicit" rather than "capability X erased".
- Mastered-prompt drift is the mechanism behind the training-trace gibberish: [[../rl-optimizers/mcpo]] shows unregularised drift on mastered prompts causes ~5% one-step regression on those prompts (Sec 4.1, Fig 2). In 1-shot RLVR the trained prompt becomes mastered by ~step 100 and remains mastered for the rest of training — every subsequent step is unanchored drift on *that* prompt's distribution.
- Zero-variance escape is unavailable: at $N=1$, [[../rl-optimizers/dapo]]'s Dynamic Sampling filter is a no-op — you can't skip a zero-variance prompt when it's your only prompt. The paper works around this by hand-picking $\pi_1$ via historical variance, a prompt whose empirical pass rate sat near 0.5 during a calibration run (see [[data-efficiency-rft]] Theorem 1). See also [[../conflicts/mcpo-vs-dapo-mastered-prompts]].
- EWC-Fisher-anchor is the corpus's canonical forgetting counter: [[../catastrophic-forgetting/ewc-gemma2-cpt]] preserved English on 7/7 benchmarks + improved Lithuanian on 5/7, but for *continual pretraining*, not RLVR. [[../synthesis/proposed-method]] proposes composing EWC with RLVR; composition is untested.

**Gaps — side effects not addressed anywhere in the wiki:**
- Cross-task forgetting on non-reasoning benchmarks (instruction-following, style, safety, tool use, long-context). The paper only tested math + ARC.
- Behaviour past 1.4k steps — the 10k, 100k step regime is unobserved.
- Interaction of the $r^{KL}$ term with single-prompt training. Regular RLVR computes KL under a varied prompt distribution; 1-shot computes it under exposure to only $\pi_1$'s distribution, possibly biasing the regulariser.
- Stability of the Balashov sparse subnetwork when the gradient comes from a single prompt — does the mask stay localised or bloat?
- Retention after priors are consumed. Shao's amplification story assumes the base model has priors worth sharpening; what happens once those priors are concentrated?

**How 1-shot side effects differ from regular RLVR:**

| Axis | Regular RLVR | 1-shot RLVR |
|---|---|---|
| Mastered-prompt escape | Distribution churns; each prompt crosses $p \to 1$ once and moves on | Single prompt hits $p \to 1$ and stays; all later steps are drift on that prompt's distribution |
| Zero-variance escape | DAPO Dynamic Sampling filters degenerate groups | Filter is a no-op |
| Training-trace gibberish | Rarely reported; averaged across prompts | Observed at ~1.4k steps on the trained prompt |
| Cross-domain generalisation | Correlated with training distribution breadth | Surprisingly positive on ARC despite math-only training — *better* than full-set RLVR |

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
