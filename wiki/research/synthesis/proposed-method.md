---
name: proposed-method
description: Implementation-oriented summary of the proposed reference-grounded single-sample concept fine-tuning method — components, end-to-end flow, and prioritised reading list of source papers to review before coding.
type: research
---

# Proposed Method — Reference-Grounded Single-Sample Concept Fine-Tuning

*Editorial synthesis. Consolidates [[single-sample-concept-skeleton]] with the teacher-student-RL findings into an implementation-focused roadmap. Every component traces to a corpus paper; the composition is the project frame, not a claim from any single paper.*

## One-paragraph summary

Train a small LLM on a small curriculum of worked examples (think: a calculus textbook with ~10–100 exercises, each with its reference chapter) by repeatedly applying a Reinforcement-Learned-Teacher-style gradient step per exercise, with four safety rails: a failure-trigger that only fires on examples the current policy cannot resolve, a sparse subnetwork mask that confines every edit to ~5–30% of the weights, a Fisher-weighted EWC anchor that protects unrelated capability, and a Minimum-Description-Length test on sibling inputs that grades concept-understanding rather than pattern-memorisation. The reference material sits in the prompt during every gradient step, providing persistent grounding the way a textbook does for a student.

## Goal

Update model weights on a small set of (reference_text, question, solution) examples such that:

1. **Each edit is grounded.** The model sees the reference text while learning from each exercise — not just the question–answer pair.
2. **Each edit is triggered.** Only examples the current policy cannot resolve fire an update; trivially-known examples are skipped.
3. **Each edit is localised.** Updates live in an RL-induced subnetwork; unrelated capability is protected by construction and by an EWC anchor.
4. **Each edit is graded for understanding.** An explanation is rewarded by how much it raises a student's conditional log-probability of the correct solution — not by whether the policy can produce the answer itself. An MDL check on sibling inputs discards edits that compress the seed but not the concept family.

## Components

| Id | Component | Source | Role |
|---|---|---|---|
| **R** | **RLT reward** — $r^{RLT} = r^{SS} - \lambda r^{KL}$. $r^{SS}$ is the student's avg+min log-prob of the correct solution $s$ given the teacher's think-tokens $t$ and question $q$; $r^{KL}$ is the KL between teacher-with-solution and student-without-solution over the think-tokens, penalising answer-leakage. | [[../teacher-student-rl/sakana-rlt]] | Dense, annotation-free per-token reward. Replaces correctness-only reward. |
| **P1** | **Failure trigger** — $F(x) = H(\pi_\theta(y\|x)) / (M(\pi_\theta(y\|x)) + \varepsilon)$, $M = p_{(1)} - p_{(2)}$. Fire an update only if $F(x) > \tau$. | [[../concept-learning/recursive-concept-evolution]] | Cheap label-free gate. Most exercises are skipped — only the ones the policy cannot currently resolve generate gradients. |
| **P2** | **Sparse subnetwork mask** — pre-compute $M_\theta$ from a handful of reference rollouts via top-$k$ $\|$Fisher · magnitude$\|$ with LayerNorms excluded. Restrict every gradient to $M_\theta$. | [[../rlvr-mechanics/rl-sparse-subnetwork]] | Edit locality by construction. RL only touches 5–30% of weights anyway; making it explicit bounds the blast radius. |
| **P4** | **Principle decomposition** (optional) — decompose each concept into 5–10 natural-language sub-criteria; evaluate each rollout along every principle; reward is a vector. | [[../critique-self-correction/constitutional-ai]] | Higher per-sample signal density. Addressable per-axis gradient instead of a scalar. |
| **C** | **Reference-in-context** — the textbook chapter (or selected passages) sits in the teacher's prompt before the question and the solution. No weight updates touch the reference; it is conditioning only. | *Novel to this method; closest corpus support is* [[../in-context-learning-theory/icl-bayesian-inference]] *(per-token information theorem) and* [[../test-time-training/algorithm-distillation]] *(frozen-weights, all-in-context).* | Persistent grounding across iterations. The per-token-information theorem argues explicitly that longer structured context carries more posterior signal than many short examples. |
| **V** | **MDL concept-test on siblings** — maintain a small held-out set of *related* inputs (paraphrases, transformed instances, concept-family siblings). An edit commits iff it reduces description length on the sibling set: $\Delta DL(\text{sibling set}) < 0$. Revert otherwise. | [[../concept-learning/recursive-concept-evolution]] | Grades understanding vs memorisation. A pattern-matching edit compresses the seed but not the family. |
| **F** | **EWC Fisher anchor** — compute Fisher diagonal on a pretraining-representative task set once; add $\frac{\lambda_{EWC}}{2}\sum_i F_i (\theta_i - \theta^*_i)^2$ to the loss. | [[../catastrophic-forgetting/ewc-gemma2-cpt]] | Forgetting protection. Complements **P2**'s subnetwork mask with an explicit anchor on the frozen-capability side. |
| **S** | **Stopping signal** — monitor L2T-style Fisher/SVD info-gain per episode; stop the per-exercise loop when the info-gain delta plateaus *and* the MDL delta on siblings has stabilised. | [[../rlvr-mechanics/learning-to-think]], [[../concept-learning/recursive-concept-evolution]] | Avoids the 1-shot-RLVR post-saturation overfit band (>~1.4k steps). |
| **G** | **Diversity injection** — group size $G > 1$ in GRPO; entropy bonus; optionally sample think-tokens at higher temperature. | [[../single-sample-rl-finetuning/1-shot-rlvr]], [[../teacher-student-rl/ho-reasoning-teachers]] | Prevents collapse to a single memorised explanation. Entropy loss shown load-bearing for post-saturation generalisation; diverse reasoning is load-bearing for distillation quality. |

## End-to-end flow

```
INPUT
  — T:     reference text (textbook chapter)
  — E = {(q_i, s_i)}:  small exercise set (N ≈ 10–100)
  — π_θ:   base policy (7B–14B)
  — π_s:   student policy (same or smaller; typically a frozen snapshot of π_θ)
  — Siblings(q):  sibling-set generator (paraphrase / transform / LLM-generated)

ONE-TIME SETUP
  1. Compute EWC Fisher F* on pretraining-representative tasks.        # F
  2. Roll out π_θ on a few reference examples; compute mask M_θ =
     top-k(|F · |θ||) with LayerNorms excluded.                        # P2
  3. Freeze π_s := π_θ at this checkpoint.
  4. Snapshot π_base := π_θ for KL leash and EWC anchor.

PER-EXERCISE LOOP  for each (q, s) ∈ E:
  5. f ← F(q; π_θ).                                                     # P1
     if f ≤ τ:   skip this exercise (policy already confident).

  6. Sample G teacher think-token rollouts t_1..t_G from π_θ(· | T, q, s).
                                                                        # C, G
  7. For each t_g, score:
       r_SS_g =  avg_k log π_s(s_k | t_g, q)
                 + α · min_k log π_s(s_k | t_g, q)
       r_KL_g =  avg   D_KL(π_θ(·|T,q,s,<k) || π_s(·|q,<k))
                 + α · max D_KL(...)
       r_g    =  r_SS_g − λ · r_KL_g                                    # R
       (optional) r_g += Σ_j β_j · principle_score_j(t_g)              # P4 optional

  8. GRPO advantage:  Â_g = (r_g − mean) / (std + ε).

  9. Gradient:  g = ∇_θ  E[Â · log π_θ(t | T, q, s)]
               g ← M_θ ⊙ g                                              # P2
               loss += λ_KL · D_KL(π_θ || π_base)                       # KL leash
               loss += (λ_EWC / 2) Σ_i F*_i (θ_i − θ*_i)^2              # F

 10. Proposed step θ' ← θ − η·g.

 11. Sibling validation:
       R_sib = Siblings(q)
       ΔDL = DL(π_θ' ; R_sib) − DL(π_θ ; R_sib)                         # V
       if ΔDL < 0:   commit θ ← θ'
       else:         revert (or shrink η, re-propose).

 12. Stopping check:  if info-gain Δ plateaus AND ΔDL stable:           # S
       break per-exercise loop; move to next exercise.

OUTPUT
  — Updated π_θ with concept-family performance gains on siblings,
    bounded forgetting on unrelated pretraining tasks.
```

## What each primitive buys you, and what fails without it

| Drop this primitive | Failure mode |
|---|---|
| Without **R** (RLT reward) | Reduced to correctness-only reward; inherits RLVR's exploration problem and 1-shot-RLVR's reliance on already-capable bases. |
| Without **P1** (trigger) | Every exercise updates, including ones the policy already solves — forgetting risk compounds across the curriculum. |
| Without **P2** (mask) | Full-parameter update; blast radius unaudited; forgetting bound depends solely on EWC + KL leash. |
| Without **C** (reference) | Reduces to standard RLT on (q, s) pairs. Loses the "textbook-as-grounding" benefit and the Bayesian-ICL per-token-information advantage. |
| Without **V** (MDL sibling test) | No discriminator for concept-vs-pattern. Edit commits on any local loss reduction — the pattern-memorisation failure mode. |
| Without **F** (EWC) + **KL leash** | Unrelated capability drifts; the method becomes a specialisation rather than a concept installer. |
| Without **S** (stopping) | Post-saturation overfit — 1-shot RLVR shows accuracy peaks then declines after ~1.4k steps without a stopping rule. |
| Without **G** (diversity) | Collapse to one memorised explanation — every corpus single-sample method that works has explicit diversity; every one that lacks it fails. |

## Relation to existing single-sample work

- **[[../teacher-student-rl/sakana-rlt]] (RLT).** Provides **R**. Missing: **P1**, **P2**, **C**, **V**, **F**. RLT as-is is a teacher-training method; the proposed method uses RLT's reward function as the gradient-of-record for a concept-installation loop on the deployment model.
- **[[../single-sample-rl-finetuning/1-shot-rlvr]] (1-shot RLVR).** Provides the repetition existence-proof + entropy-loss observation. Missing: **R** (uses correctness), **C** (no reference), **V** (no concept test).
- **[[../concept-learning/recursive-concept-evolution]] (RCE).** Provides **P1**, a richer form of **P2** (concept subspaces), and **V**. RCE spawns new parameters; the proposed method edits existing ones via RLT instead.
- **[[single-sample-concept-skeleton]].** This document's ancestor. The skeleton proposed L2T info-gain as **P3**; this document replaces it with RLT's **R** because the textbook provides solutions, removing L2T's core motivation (no-solution regime). L2T info-gain is retained as the stopping diagnostic **S**.

## Pre-implementation reading list

### Tier 1 — must-read before writing any code (7 papers)

These are the load-bearing primitives. Each corresponds to a specific component the implementation cannot work without.

| # | Read | Component | Why |
|---|---|---|---|
| 1 | [[../teacher-student-rl/sakana-rlt]] | **R** | The reward function is the heart of the method — $r^{SS}$ formula, the min/max reduction, $r^{KL}$ against answer-leakage, the GRPO integration, hyperparameters (batch 1024, group 64, lr 1e-6, 125 steps). Also: the 7B-teacher / 32B-student existence proof. |
| 2 | [[../rlvr-mechanics/deepseekmath-grpo]] | base optimiser | GRPO's formulation. Group-relative advantage, KL-to-ref term, gradient-coefficient unification with PPO/DPO/SFT/RFT. |
| 3 | [[../single-sample-rl-finetuning/1-shot-rlvr]] | repetition dynamics + **G** | The overfit boundary (~1.4k steps), the entropy-loss load-bearing result, the 8.6-point non-format delta. Cautionary tale for the stopping rule. |
| 4 | [[../concept-learning/recursive-concept-evolution]] | **P1, V** | Failure trigger $F(x) = H/(M+\varepsilon)$; MDL acceptance on held-out related inputs; spawn-on-failure philosophy. |
| 5 | [[../rlvr-mechanics/rl-sparse-subnetwork]] | **P2** | The 5–30% sparsity result; LayerNorm exclusion; Fisher · magnitude mask-discovery heuristic. |
| 6 | [[../catastrophic-forgetting/ewc-gemma2-cpt]] | **F** | Fisher anchor construction on real pretraining tasks; $\lambda_{EWC}$ calibration; the "preserves 7/7 English benchmarks while gaining 5/7 Lithuanian" existence proof. |
| 7 | [[single-sample-concept-skeleton]] | overall framing | The four-primitive precursor to this document; its gaps list; its "remove any primitive and it degrades into an existing method" analysis. |

### Tier 2 — read before extending beyond the baseline (5 papers)

Needed once the minimal loop works and you want to add curriculum synthesis, principle-decomposition, or probabilistic grounding.

| # | Read | Role | Why |
|---|---|---|---|
| 8 | [[../teacher-student-rl/soar-edge-of-learnability]] | curriculum synthesis | Bilevel meta-RL with grounded rewards. Useful if you want the method to *generate* exercises beyond the hand-curated textbook set. Also: "structural quality > answer correctness" — matters for synthesising worked solutions. |
| 9 | [[../rlvr-mechanics/learning-to-think]] | **S** (stopping) | L2T's Fisher/SVD info-gain reward as the stopping diagnostic. Low-rank proxy cost $r/d \approx 1\text{–}10\%$ at 1.5B. |
| 10 | [[../single-sample-rl-finetuning/critique-ft-one-problem]] | data amplification | The 1-problem-to-600-rows template. Useful if a single textbook exercise needs more gradient signal than one prompt provides. |
| 11 | [[../critique-self-correction/constitutional-ai]] | **P4** (optional) | Principle-decomposition as vector reward. Apply when per-concept axes (e.g. *chain rule*, *product rule*, *integration by parts*) are separately addressable. |
| 12 | [[../teacher-student-rl/trice-cot-latent-variable]] | probabilistic grounding | The marginal-likelihood objective; MCMC-EM with control-variate; learning from incorrect rationales. Read before deciding how to handle wrong teacher rollouts that still carry gradient information. |

### Tier 3 — theoretical grounding (3 papers)

Read when you hit design questions the empirical papers above don't resolve.

| # | Read | Role | Why |
|---|---|---|---|
| 13 | [[../in-context-learning-theory/icl-bayesian-inference]] | justifies **C** | Per-token-information theorem — explicit argument that a long reference-in-context carries more posterior signal than many short examples. The theoretical underpinning for "keep the textbook in the prompt". |
| 14 | [[../in-context-learning-theory/icl-as-gradient-descent]] | update shape | The implicit ICL update is rank-1 outer-product $(Wx - y)x^\top$. Explicit single-sample fine-tunes should mirror this — LoRA-shaped, not full-weight. |
| 15 | [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] | format-vs-substance | CoT-Pass@K metric separates format gain from genuine reasoning gain. Instrument this alongside **V** to confirm concept uptake isn't a format artefact. |

## Known gaps the implementation will hit

1. **Cheap mask-discovery.** Balashov recovers $M_\theta$ from a *converged* RL run. The proposed method needs $M_\theta$ from a handful of reference rollouts. Candidate — top-$k$ $\|$Fisher · magnitude$\|$ — is principled but unvalidated at small rollout budgets.
2. **RLT at small group size.** GRPO's group-relative baseline collapses at $G=1$ and is noisy at small $G$. Sakana used $G=64$; a textbook-scale budget may not afford this. Candidate workarounds: shared baseline from a frozen reference per prompt, leave-one-out baseline across principle axes or input perturbations.
3. **Sibling set construction.** $V$ requires a pool of concept-family siblings for each exercise. Options: paraphrase augmentations, LLM-generated isomorphs, nearest-neighbour retrieval from the textbook. None validated in corpus.
4. **Reference-in-context during RL — unmeasured.** No corpus paper runs gradient updates while a large reference document sits in the prompt. Risks: memory / context-length cost; attention-dilution over long context; the teacher may learn to ignore the reference.
5. **Student choice.** Sakana uses a frozen Qwen2.5-7B as the student. Using the current policy's own frozen snapshot $\pi_s := \pi_\theta^{(t-1)}$ couples student and teacher curricula — potentially unstable. Decide up front.
6. **Concept-probe metric on LLM math.** The MDL test requires a compression estimator that works on LLM-generated reasoning. RCE's operationalisation is vision-first; its LLM numbers are projected, not measured (see [[../concept-learning/_overview]] caveat).
7. **Ordering and interference across exercises.** Bayesian-ICL predicts ordering-sensitivity; the method inherits it. No protocol for exercise ordering is specified above.

## Source

Pure editorial synthesis. Primitives traced to corpus pages; composition is the project frame.

## Related

- [[single-sample-concept-skeleton]] — the ancestor synthesis page; more primitive-focused, less implementation-focused
- [[../teacher-student-rl/_overview]] — the theme where **R** lives
- [[../single-sample-rl-finetuning/_overview]] — the downstream regime this method operates in
- [[../rlvr-mechanics/_overview]] — base optimiser, sparse subnetwork, and info-gain reward
- [[../concept-learning/_overview]] — **P1** and **V** source theme
- [[../critique-self-correction/_overview]] — **P4** source theme
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — **F** source
- [[../in-context-learning-theory/_overview]] — theoretical grounding for **C**
