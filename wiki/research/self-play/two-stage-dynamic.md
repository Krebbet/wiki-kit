---
name: two-stage-dynamic
description: Two-stage probability-mass dynamic in RLVR training — Stage 1 (exploitation) collapses entropy and starves unexplored tokens; Stage 2 (exploration) inverts this once high-probability tokens saturate. Reconciles the Invisible-Leash shrinkage result with SPIRAL-style expansion: both are real, phase-conditional.
type: research
---

# Two-Stage Dynamic View: Shrinkage, Expansion, or Both?

Xinhao Yao, Lu Yu, Xiaolin Hu, Fengwei Teng, Qing Cui, Jun Zhou, Yong Liu. Renmin University of China / Ant Group / Xiamen University. *The Debate on RLVR Reasoning Capability Boundary: Shrinkage, Expansion, or Both? A Two-Stage Dynamic View.* arXiv:2510.04028, October 2025. **TL;DR:** RLVR training exhibits two distinct phases. Stage 1 (exploitation) narrows capability by boosting already-sampled tokens while starving unexplored optimal ones; Stage 2 (exploration) inverts this once high-probability tokens saturate. Both the "shrinkage" camp (Invisible Leash / Yue et al.) and the "expansion" camp (ProRL / SPIRAL-adjacent work) are correct — each describes a different phase of the same dynamic.

## Method

### Theoretical anchor

From Theorem 1, the expected logit update for token $v$ at layer $l$ is:

$$\mathbb{E}\bigl[\Delta z_v^l\bigr] \propto \pi^l(v) \left[(1-\pi^l(v))\hat{A}(v) - \sum_{u \neq v} \pi^l(u)\hat{A}(u)\right]$$

The update scales with $\pi^l(v)$. When a token $a_2$ is optimal ($r(a_2) > r(a_1)$) but undersampled ($\pi^l(a_2) \approx 0$), the gradient update to its logit is near zero regardless of its advantage. This is the mechanism that locks Stage 1 in place.

### Stage 1 — exploitation (shrinkage)

The model predominantly samples explored high-reward token $a_1$ and low-reward token $a_3$; the optimal but undersampled $a_2$ is almost never drawn. Positive advantage pushes $\pi(a_1)$ up and $\pi(a_3)$ down; $\pi(a_2)$ "remains largely unchanged (or may even decrease)." Empirical signature: standard GRPO causes rapid, monotone entropy collapse on the held-out MATH test set. Large-$k$ Pass@$k$ falls below the base model because diversity of solution paths is suppressed.

### Stage 2 — exploration (expansion)

As $\pi(a_1) \to 1$, the gradient term $(1 - \pi(a_1)) \to 0$ — further increases slow. When $a_2$ is occasionally sampled and $\hat{A}(a_2) > 0$ while $\hat{A}(a_1) < 0$, $\pi(a_2)$ rises and $\pi(a_1)$ decreases. Entropy recovers and eventually exceeds the base model. Large-$k$ Pass@$k$ recovers and surpasses baseline. The transition is triggered by saturation of the dominant high-reward token, gated primarily by **training duration** and **entropy preservation**.

### Variants

GRPO-N uses only negative-advantage gradient components (suppressing reinforcement of entire trajectories including erroneous steps); GSPO applies sequence-level clipping. Both defer or avoid entropy collapse and allow Stage 2 to emerge. ProRL (Liu et al.) escapes Stage 1 via periodic reference-policy and optimizer resets; the paper identifies this as an independent engineering route to the same transition.

## Claims

- **Stage 1 evidence:** Standard GRPO on Llama-3.2-3B-Instruct, AIME 2025: Pass@256 = 16.7 vs. base 36.7 — a 55% drop at large $k$.
- **Stage 2 evidence (GRPO-N, Qwen2.5-Math-7B):** AMC 2023 Pass@256 = 100.0 vs. base 97.5; AIME 2025 Pass@256 = 66.7 vs. base 46.7. Held-out entropy "significantly exceeds that of the base model."
- **OOD generalisation at Stage 2:** GRPO on ARC-c Pass@128 = 96.3 vs. GRPO-N 100.0; on MMLU-Pro Pass@256 GRPO collapses to 90.6 while GRPO-N holds 100.0.
- **Transition driver:** $\pi(a_1) \to$ saturation. Timing varies with reward gap, initial probabilities, and learning rate — no universal crossover step is quantified.
- **Liu et al.'s ProRL result** is cited as Stage 2 evidence; the paper says "their conclusions align closely with our findings."

## Why this is load-bearing for single-sample concept learning

This paper provides the **theoretical bridge that resolves the open conflict** between Invisible Leash and SPIRAL-style transfer results ([[../../conflicts/invisible-leash-vs-spiral-transfer]]). The resolution changes two load-bearing design constraints:

1. **Training duration is a categorical hyperparameter, not a tuning detail.** Premature termination (standard practice at a few hundred steps) locks the method into Stage 1 and prevents access to reasoning trajectories outside the base model's sampling distribution. Any proposed method must specify a regime that reaches Stage 2 or explicitly scope itself to exploitation-only extraction.

2. **Entropy preservation is a proxy for Stage 2 accessibility.** For single-sample concept fine-tuning, where the optimal reasoning path may be genuinely novel, methods that collapse entropy self-defeat on exactly the cases where learning matters most. Entropy-preserving objectives (GRPO-N, GSPO) or reference-policy resets (ProRL) should be considered.

3. **Refines the ruling on Position A (Invisible Leash).** Stage 1 is the dominant story for short runs and correctly characterises the exploitation phase. Position A remains the right frame for standard short training, but is now stage-scoped rather than a universal bound on all RLVR training.

## Limitations

- Tested only on GRPO/GSPO variants, mathematical reasoning benchmarks, 3B–7B models. Generalisation to other domains, larger models, or game-based self-play (multi-turn, evolving opponent) is theoretical.
- SPIRAL is not cited; the Stage 2 reading of its gains is the reviewer's inference, not the paper's claim.
- No explicit transition step is quantified; prescribing a training budget requires model- and task-specific profiling.
- The theoretical extension from a 3-action toy model to full-vocabulary long-generation sequences relies on a Proposition 1 / NTK argument, not direct empirical validation at that scale.
- Three open questions acknowledged: how to design efficient fine-grained probability-mass allocation; which base-model properties favour Stage 2; where the Stage 2 ceiling lies.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/06-two-stage-dynamic.md`
- `../../../raw/research/self-play-quality-extraction/07-06-two-stage-dynamic.md`
- arXiv: https://arxiv.org/abs/2510.04028

## Related

- [[invisible-leash]] — the Invisible Leash bound that this paper re-scopes to Stage 1
- [[yue-rlvr-boundary]] — empirical companion establishing the shrinkage claim
- [[understanding-self-play]] — proposer-is-everything; Stage 2 provides the expansion that understanding-self-play anticipates
- [[spiral]] — Stage-2-consistent transfer result; game-self-play likely avoids entropy collapse by construction
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — the open conflict this paper partially resolves
- [[../synthesis/proposed-method]] — training-duration and entropy-preservation are now load-bearing hyperparameters
- [[_overview]]
