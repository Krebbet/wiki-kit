# Single-Sample Concept Fine-Tuning — Candidate Method Skeleton *(synthesis)*

*Editorial synthesis. Composes four primitives drawn from this wiki's corpus into one candidate skeleton for a concept-based, single-sample LLM fine-tuning method. This is not source content — the individual primitives are traced; the composition is the project frame, not anything any single paper claims.*

## Goal

Update model weights on a single training example `(x, y*)` such that:

1. The edit lands in an **addressable, reversible subnetwork** (not the whole model).
2. The edit **fires only when needed** (not on every example).
3. The edit is scored with a **dense, label-free signal** (not a scalar outcome).
4. The edit is **validated against held-out related inputs** (not just the seed).

## The four primitives

### P1 — Failure trigger (RCE)
`F(x) = H(π_θ(y|x)) / (M(π_θ(y|x)) + ε)` with `M = p_(1) − p_(2)`. When `F(x) > τ`, the current policy cannot resolve `x` with confidence — fire single-sample update. Cheap, label-free. See [[../concept-learning/recursive-concept-evolution]].

### P2 — Sparse subnetwork mask (Balashov)
RL effectively touches only 5–30% of weights (DeepSeek-Math 7B + GRPO specifically). Pre-compute a mask `M_θ` from a handful of reference rollouts via Fisher magnitude + LayerNorm exclusion. Restrict every gradient to `M_θ`. Edit locality by construction; unrelated capability protected; mask reusable across examples. See [[../rlvr-mechanics/rl-sparse-subnetwork]].

### P3 — Fisher-proxy information-gain reward (L2T)
Per-episode reward `r_t ≈ I(θ; episode_t)` estimated via low-rank Fisher / SVD proxy (`r/d ≈ 1–10%` at 1.5B). Dense, label-free, per-rollout. No external PRM required. See [[../rlvr-mechanics/learning-to-think]].

### P4 — Principle decomposition (CAI)
Decompose the target concept into 5–10 natural-language principles. Each becomes a reward dimension evaluated by an LLM judge (self or sibling). CAI showed principle-decomposition replaces tens of thousands of preference labels. Reward becomes a *vector* over addressable axes rather than a scalar. See [[../critique-self-correction/constitutional-ai]].

## Candidate skeleton

```
on each training example (x, y*):

  1. Trigger.
     f = F(x) on π_θ.
     if f ≤ τ: skip.    # policy already confident; no edit

  2. Decompose.
     p_1..p_k = principles(concept(x, y*))     # CAI
     # human-authored for seed concepts; LLM-extracted for open-vocab

  3. Roll out.
     y_1..y_G ~ π_θ(·|x)                        # G small for single-sample

  4. Score each rollout.
     r_g =  α · L2T_info_gain(y_g)              # P3
          + β · Σ_k principle_score(y_g; p_k)   # P4
          + γ · verifier(y_g, y*)               # if available

  5. GRPO advantage.
     Â_g = (r_g - mean_g) / (std_g + ε)

  6. Gradient step.
     g  = ∇_θ  E[Â · log π_θ(y|x)]
     g ← M_θ ⊙ g                                # P2: restrict to mask
     apply with KL leash to π_θ_base

  7. Validate (MDL-ish).
     ΔDL = desc_length(π_θ ; related_set) - desc_length(π_θ_prev ; related_set)
     if ΔDL < 0: commit.
     else: revert (or shrink step and retry).
```

## Why each primitive is load-bearing

| Primitive | Without it | With it |
|---|---|---|
| P1 trigger | Every example updates — catastrophic-forgetting risk | Updates fire only on failures; most examples untouched |
| P2 mask | Full-param update — large, unaudited blast radius | Edit lives in RL-induced subnetwork; unrelated capability protected |
| P3 reward | Need external PRM or human step labels | Dense signal from model internals; zero annotation |
| P4 principles | Reward is a scalar — low per-sample signal | Reward decomposes into addressable axes; each axis a separate gradient |

Remove any single primitive and the composition degrades into an existing method: drop P1 and it becomes straight 1-shot RLVR; drop P2 and it's L2T on a single example; drop P3+P4 and it's masked GRPO with sparse outcome reward; drop P4 and it's single-example RL with Fisher reward.

## Relation to existing single-sample work

- **1-shot RLVR** (Wang) — has P3-lite (GRPO verifier) and neither P1 nor P2. Single example selected by offline search, not by failure trigger.
- **Critique FT on one problem** — has a supervised analogue of P4 (teacher critiques as dense signal) and neither P1 nor P2. SFT, not RL.
- **RCE** (Chaudhry) — has P1 and a richer form of P2 (explicit low-rank *subspaces*, not masks on base params) and an MDL validator. No P4. Adds concept parameters rather than fine-tuning in place; the "in-place fine-tune" variant of RCE is exactly this skeleton.

The four-primitive composition is not any of the above; it's the specific hybrid the corpus *implies* but does not instantiate.

## Gaps / unknowns

- **Cheap mask discovery.** Balashov recovers `M_θ` from a converged RL run. Need a heuristic that estimates it from `≤ G` rollouts + a Fisher snapshot on a single example. Candidate: top-k |Fisher · magnitude| with LayerNorms excluded. Unvalidated.
- **Principle extraction for open-world concepts.** CAI hand-authored principles. For unseen concepts an LLM must self-decompose the concept, and decomposition quality is unmeasured. Candidate probe: multi-sample principle generation + consistency.
- **Low-G variance reduction.** GRPO's group-relative baseline collapses at `G=1` and is noisy at small `G`. Candidate: shared baseline from a frozen reference policy per prompt, or a leave-one-out baseline across perturbations of `x`.
- **Related-input pool for validation.** MDL over a held-out related set requires the set. Options: x-augmentations (paraphrase, invariance transforms), nearest-neighbour retrieval from pretraining corpus, or LLM-generated sibling prompts. None validated here.
- **Catastrophic forgetting bound.** The P2 mask + KL leash mitigate but do not bound forgetting. This is the unclaimed territory — no paper in the current corpus addresses it. Next research cluster to run.
- **Reference-material-in-context during weight updates.** The skeleton is silent on whether a comprehensive reference text (e.g. a textbook chapter, a worked-solution library) should sit in the prompt while the loop iterates. TTT keeps synthetic tasks in-context for *one* test instance ([[../test-time-training/ttt-few-shot]]); Algorithm Distillation is gradient-free ([[../test-time-training/algorithm-distillation]]); Reflexion's memory is Ω=1–3 ([[../critique-self-correction/reflexion]]). None of these do *weight-updating RL with a persistent long-context reference*. Bayesian-ICL's per-token-information theorem argues this would help ([[../in-context-learning-theory/icl-bayesian-inference]]); no corpus method instantiates it.
- **Small-curriculum band (N ≈ 10–100).** Existing single-sample work sits at N=1 (1-shot RLVR, CFT) or training-scale (rStar-Math); the middle band of a curated curriculum (e.g. textbook exercises sharing a reference text) is unmeasured. Load-bearing for "synthesise a textbook, run the exercises" designs.
- **Concept probing for LLM math understanding.** RCE and CBM concept-probes are vision-first; RCE's LLM numbers are *projected* per the paper's own caveat. A direct test of whether a specific math concept (chain rule, integration by parts) is installed vs pattern-matched is not in the corpus.

## Next capture priorities

Downstream research leads this skeleton exposes (for a future `/research` run):

- Catastrophic forgetting under single-sample updates (EWC, MAS, task-vector merging, SLERP, TIES, DARE).
- Cheap mask-discovery heuristics (Fisher × magnitude, SNIP-style pruning transferred to RL, sparse RL adapters).
- Principle self-extraction by LLMs (constitution-generation, chain-of-critique taxonomies).
- Info-gain rewards at small G (leave-one-out baselines for RLHF/RLVR).
- Dense-reward composability (α/β/γ weighting under competing signals).
- Retrieval-augmented / long-context fine-tuning (RETRO / Atlas / RA-DIT variants; long-context RL with documents resident in prompt).
- Curriculum and textbook synthesis for LLMs (graded problem sets, AI-generated curricula, self-grading loops over exercises).
- Worked-example / reference-grounded RL (triples of (problem, worked-solution-in-context, final-answer); CoT with reference grounding).
- LLM concept-probing for math specifically (mechanistic evaluation of whether named concepts are installed vs memorised after RLVR).

## Source

Pure editorial synthesis. Primitives traced to:

- P1: [[../concept-learning/recursive-concept-evolution]]
- P2: [[../rlvr-mechanics/rl-sparse-subnetwork]]
- P3: [[../rlvr-mechanics/learning-to-think]]
- P4: [[../critique-self-correction/constitutional-ai]]

No new external sources.

## Related

- [[../single-sample-rl-finetuning/_overview]]
- [[../rlvr-mechanics/_overview]]
- [[../concept-learning/_overview]]
- [[../critique-self-correction/_overview]]
- [[../process-reward-models/_overview]]
