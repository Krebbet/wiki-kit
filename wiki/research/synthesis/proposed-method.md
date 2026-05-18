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
| **G** | **Diversity injection** — group size $G > 1$ in GRPO; entropy bonus; optionally sample think-tokens at higher temperature. **Pre-flight check (2026-05-01):** before training, audit candidate diversity using [[../self-play/info-gain-self-play]]'s prequential MDL test (Algorithm 1) — if epiplexity $S_{C,T}$ doesn't rise monotonically across iterations, fix proposer strength / synthetic direction *before* tuning reward shape. Diversity that isn't *learnable* (e.g. random rephrasings outside the Goldilocks zone) is wasted compute. | [[../single-sample-rl-finetuning/1-shot-rlvr]], [[../teacher-student-rl/ho-reasoning-teachers]], [[../self-play/info-gain-self-play]], [[../self-play/rstar]] (5-action MCTS as drop-in template at the per-problem level) | Prevents collapse to a single memorised explanation. Entropy loss shown load-bearing for post-saturation generalisation; diverse reasoning is load-bearing for distillation quality. |
| **L** | **Format/fluency guard (composite)** — five composable corpus tools, all targeting the same failure mode: KL leash to $\pi_\text{base}$ ([[../single-sample-rl-finetuning/reft]], [[../rl-optimizers/instructgpt]]); EWC Fisher anchor (component **F** above); Balashov sparse mask (component **P2** above); Dr-GRPO length/std bias fix ([[../rl-optimizers/dr-grpo]]); DAPO Overlong Reshape on truncated rollouts ([[../rl-optimizers/dapo]]); MCPO hinge-KL on *mastered* prompts ([[../rl-optimizers/mcpo]]); InstructGPT ptx (mixed pretraining gradients during RL). | [[../single-sample-rl-finetuning/1-shot-rlvr]] (gibberish-trace at ~1.4k steps), [[../rl-optimizers/mcpo]] §4.1 Fig 2 (unanchored drift on mastered prompts ≈5% one-step regression — the mechanism behind 1-shot RLVR's degeneracy), [[../single-sample-rl-finetuning/cbrl]] (anneal-to-zero scaffold requirement) | Foregrounds what was previously scattered across **F**, **P2**, **S**, and the inline KL leash line. At $N=1$ every post-saturation step is unanchored drift on the same prompt's distribution — DAPO Dynamic Sampling is a no-op; MCPO hinge-KL is the corpus's specific response. **L** is what stops the format collapse [[../single-sample-rl-finetuning/1-shot-rlvr]] documents. |

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
| Without **L** (format/fluency guard) | The 1-shot-RLVR gibberish-trace failure at ~1.4k steps. At $N=1$ post-saturation, every step is unanchored drift; DAPO Dynamic Sampling is a no-op (only one prompt); MCPO §4.1 shows ~5% one-step regression on mastered prompts. Test outputs degrade after training outputs do. |

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

## Inner-loop reading order — alternative cut by reward vs dataset

The Tier-1/2/3 lists above are keyed by *which component each paper supports*. When the question is instead "I've read Tier 1 — what next, focused on the inner-loop training itself: how to shape the reward signal and how to set up the data?", the same corpus rearranges as below. Both views point at the same papers; pick whichever cut matches your current question.

### Reward signal — beyond correctness or RLT alone

| Read | Contribution |
|---|---|
| [[../rlvr-mechanics/learning-to-think]] | Episodic GRPO with **label-free Fisher/SVD info-gain reward** (per-token, dense, no PRM); $r/d \approx 1\text{–}10\%$ at 1.5B. Complement to **R**; also the stopping diagnostic **S**. |
| [[../teacher-student-rl/knowrl]] | **Atomic knowledge-points + Constrained Subset Search**; minimal-sufficient hint design; *no KL* loss; 1.5B SOTA. Closest precedent for "smallest concept-unit per step". |
| [[../process-reward-models/pav-rewarding-progress]] | **PAV** — process advantage as step-level *progress* under a complementary prover. >8% search gain, 5–6× RL efficiency over outcome RM. The per-step cousin of **R** when CoTs are long. |
| [[../process-reward-models/math-shepherd]] | Automated step labels from rollout success rate, no human annotation. The "process reward without humans" baseline to compare **R** against. |
| [[../process-reward-models/uprm]] | **uPRM — flagged 2026-05-18 for experiment-proposal refinement.** Fully *unsupervised* PRM from frozen-LLM next-token marker probabilities — no step labels, no final answers, ≈ supervised PRMs on Best-of-8. **Key property for this method:** markedly more reward-hacking-robust as an *RL reward* (supervised PRM collapses <50 iters on Qwen2.5-Math-7B; uPRM does not). Directly relevant to the inner-loop reward choice in [[concept-curriculum-method]] §First-experiment (ii) and [[recursive-concept-learning]] Phase-0: a label-free, hacking-robust dense signal is exactly what the bounded inner loop needs when the textbook setting has no step labels. Also the *observational* foil to the interventional credit-assignment idea in [[parked-ideas]] P2 ("backtrack"). Open: does uPRM's marker-probability signal survive the reference-in-context (**C**) prompt, and does it compose with RLT **R** or replace it? |
| [[../teacher-student-rl/pm4grpo]] | **TACReward** — process-mining alignment between student and teacher traces as dense scalar; drops into RLOO/GRPO/GSPO. Substitutable inner-loop reward when a teacher trace exists (which it does in the textbook setting). |
| [[../teacher-student-rl/trice-cot-latent-variable]] | Rationales as latent variables; **marginal LL via MCMC-EM with control variate**; learns from incorrect rationales. Decides what to do with wrong teacher rollouts that still carry gradient. |
| [[../critique-self-correction/critic-cot]] | SFT on weak-supervision critique-refine pairs; System-2 step-wise critique. 93.3% GSM8K, 57.8% MATH500. Recipe for *building* the critique RM when none is off-the-shelf. |
| [[../self-improvement/multi-turn-policy-verifier]] | **PAG** — single LLM alternates policy/verifier roles in multi-turn RL. Bears on whether $\pi_s$ in **R** must be a separate student or can be the policy's own snapshot (open question §5 below). |
| [[../rl-optimizers/dr-grpo]] | Identifies and removes length and std biases in GRPO. Recommended outer optimiser regardless of which reward you pick. |
| [[../rl-optimizers/mcpo]] | **Hinge-KL on mastered prompts** + advantage-denominator rescaling. Bears directly on **P1** semantics — what to do once an exercise is mastered. |

### Dataset setup — exercises, siblings, contrast, ordering

| Read | Contribution |
|---|---|
| [[../single-sample-rl-finetuning/critique-ft-one-problem]] | **1-problem → 600-row** template via teacher critique amplification. Direct precedent for "one textbook exercise → many gradient signals". |
| [[../teacher-student-rl/ho-reasoning-teachers]] | Fine-tune-CoT — **diverse rationales are the load-bearing extension**. Calibrates **G**: how many diverse $t$ rollouts per $(q,s)$ matter. |
| [[../single-sample-rl-finetuning/reft]] | SFT warm-up + PPO on **multiple sampled CoT paths per problem**; +10–12% over SFT on math without external RM. Simplest "sample $K$ CoTs, reward correct" baseline against which **R** must justify itself. |
| [[../single-sample-rl-finetuning/data-efficiency-rft]] | **DOTS** difficulty-targeted online data selection ($p \approx 0.5$); rollout replay. Calibration recipe for both training-item and eval-item difficulty. |
| [[../single-sample-rl-finetuning/cbrl]] | **Curriculum of annealed few-shot demonstration prepending** during RLVR; +1.3–22.3% over GRPO-only. Recipe for how the reference text / worked solutions decay across iterations — speaks to **C**. |
| [[../teacher-student-rl/soar-edge-of-learnability]] | **Bilevel meta-RL**: teacher generates synthetic Q–A, student trains with RLVR, teacher rewarded by student improvement on hard set. The recipe for *generating* exercises beyond the hand-curated textbook. |
| [[../concept-evaluation/contrast-sets]] | Local-decision-boundary perturbations (manual, label-flipping); up-to-25% drop vs raw test set. Operationalises **V**'s sibling set. |
| [[../concept-evaluation/gsm-symbolic]] | Symbolic templates over GSM8K; up-to-65% drop on irrelevant-clause "NoOp". Math-domain sibling generator; templated rather than authored. |
| [[../concept-evaluation/math-perturb]] | 279 hard-perturbed level-5 MATH problems where the original solution path no longer applies. Stress-test for "concept installed vs path installed". |
| [[../concept-evaluation/counterfactual-tasks]] | Same abstract task, counterfactual content (base-9, modified chess). Cleanest single axis for procedure-vs-abstraction. |
| [[../concept-evaluation/skill-mix]] | Random $k$-subsets from $N$ skills; combinatorial explosion makes memorisation infeasible. Compositional retest *and* dataset-construction recipe. |

### Theoretical anchors specific to the inner loop

- [[../in-context-learning-theory/icl-bayesian-inference]] — per-token-information theorem; **a long reference-in-context carries more posterior signal than many short examples**. The theoretical underpinning for **C**.
- [[../in-context-learning-theory/icl-as-gradient-descent]] — implicit ICL update is rank-1 outer product $(Wx-y)x^\top$; argues explicit single-sample fine-tunes should mirror this — LoRA-shaped, not full-weight.
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — **CoT-Pass@K** separates format gain from genuine reasoning gain. Instrument alongside **V** to distinguish format-vs-substance movement.

### Suggested order if the reward shape is your blocking question

1. Reward shape: [[../rlvr-mechanics/learning-to-think]] → [[../critique-self-correction/constitutional-ai]] → [[../teacher-student-rl/trice-cot-latent-variable]].
2. Reward granularity: [[../process-reward-models/pav-rewarding-progress]] → [[../process-reward-models/math-shepherd]] → [[../teacher-student-rl/knowrl]].
3. Dataset shape: [[../single-sample-rl-finetuning/critique-ft-one-problem]] → [[../teacher-student-rl/ho-reasoning-teachers]] → [[../single-sample-rl-finetuning/reft]] → [[../single-sample-rl-finetuning/data-efficiency-rft]] → [[../single-sample-rl-finetuning/cbrl]].
4. Sibling/contrast for the **V** gate: [[../concept-evaluation/contrast-sets]] → [[../concept-evaluation/gsm-symbolic]] → [[../concept-evaluation/counterfactual-tasks]].
5. Optimiser corrections you'll inherit: [[../rl-optimizers/dr-grpo]] → [[../rl-optimizers/mcpo]].

## Known gaps the implementation will hit

1. **Cheap mask-discovery.** Balashov recovers $M_\theta$ from a *converged* RL run. The proposed method needs $M_\theta$ from a handful of reference rollouts. Candidate — top-$k$ $\|$Fisher · magnitude$\|$ — is principled but unvalidated at small rollout budgets.
2. **RLT at small group size.** GRPO's group-relative baseline collapses at $G=1$ and is noisy at small $G$. Sakana used $G=64$; a textbook-scale budget may not afford this. Candidate workarounds: shared baseline from a frozen reference per prompt, leave-one-out baseline across principle axes or input perturbations.
3. **Sibling set construction.** $V$ requires a pool of concept-family siblings for each exercise. Options: paraphrase augmentations, LLM-generated isomorphs, nearest-neighbour retrieval from the textbook. **Update 2026-04-28:** [[../concept-evaluation/contrast-sets]] (Gardner et al., EMNLP 2020) operationalises this directly — small, manual, label-flipping local-boundary perturbations are *exactly* what siblings should be. [[../concept-evaluation/gsm-symbolic]] gives the math-domain analogue via symbolic templates. Open question is whether a teacher LLM can generate contrast-set-quality siblings without manual authorship.
4. **Reference-in-context during RL — partial answer found, decision locked.** Original concern: no corpus paper runs gradient updates while a large reference document sits in the *teacher's* prompt with $r^{KL}$-style soft leakage protection (memory cost, attention dilution, teacher learns to ignore reference). [[../self-play/spice]] (Liu, Jin et al., Meta, Oct 2025) supplied a *structural* alternative — Challenger reads document $d$, Reasoner answers without seeing $d$. **Decision locked 2026-05-01:** user has chosen **structural** over soft (memory: `feedback_self_play_design_choices.md`). Default Phase-0+ design: Reasoner does not see reference text during gradient step; teacher/Challenger does. RLT $r^{KL}$ regulariser dropped from the default loss. *Additional constraint surfaced:* training duration and entropy preservation are now load-bearing hyperparameters per [[../self-play/two-stage-dynamic]] — RLVR enters Stage-2 expansion regime only under entropy preservation; standard short-training GRPO stays in Stage-1 / Invisible-Leash bound ([[../self-play/invisible-leash]] Theorem C.1, [[../self-play/yue-rlvr-boundary]] empirical). Component **G** updated with [[../self-play/info-gain-self-play]]'s epiplexity pre-flight check.
5. **Student choice.** Sakana uses a frozen Qwen2.5-7B as the student. Using the current policy's own frozen snapshot $\pi_s := \pi_\theta^{(t-1)}$ couples student and teacher curricula — potentially unstable. Decide up front.
6. **Concept-probe metric on LLM math.** The MDL test requires a compression estimator that works on LLM-generated reasoning. RCE's operationalisation is vision-first; its LLM numbers are projected, not measured (see [[../concept-learning/_overview]] caveat). **Update 2026-04-28:** the [[../concept-evaluation/_overview|concept-evaluation theme]] supplies five candidate behavioural axes ([[../concept-evaluation/gsm-symbolic]] symbolic perturbation, [[../concept-evaluation/math-perturb]] hard solution-path perturbation, [[../concept-evaluation/counterfactual-tasks]] counterfactual variants, [[../concept-evaluation/contrast-sets]] local boundary, [[../concept-evaluation/skill-mix]] compositional combination) and one representational alternative ([[../concept-evaluation/causal-abstraction]] IIA) to MDL-on-text — all measured rather than projected. [[../concept-evaluation/embers-autoregression]] supplies the diagnostic prior.
7. **Ordering and interference across exercises.** Bayesian-ICL predicts ordering-sensitivity; the method inherits it. No protocol for exercise ordering is specified above.

## Extension: parametric SFT to lift $p_\gamma$ in the target region (2026-05-11)

*Open extension surfaced by a /query against the 2026-05-10 RL-as-selection-not-learning cluster.* The original method embeds reference material **in-context** via component **C**. Under the 2026-05-10 cluster, RLVR has a hard coverage wall — [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7 ($N \gtrsim 1/p_\gamma(x)$) and Theorem 6 ($\beta\log(1/\pi^*(S_N|x))$ saturation) — and [[../self-play/yue-rlvr-boundary]] identifies distillation as the unique mechanism that genuinely expands the support beyond what RLVR can reach. An extension worth tracking: pair the RL inner loop with a **parametric SFT round on the reference material itself**, designed to lift $\pi^*(S|x)$ in the target region *before* RL is asked to concentrate within that support.

**Working name.** Component **C** (in-context reference) keeps its existing role; the new axis is component **C_w** (weight-update reference).

**Corpus support — already in the wiki.**
- [[../single-sample-rl-finetuning/deepseek-r1]] — multi-stage SFT/RL pipeline with cold-start long-CoT SFT before stage-1 RL; rejection-sampled SFT between RL stages.
- [[../rl-optimizers/instructgpt]] — SFT → RM → PPO+ptx; PPO+ptx specifically mixes pretraining gradients into RL to prevent capability drift.
- [[../single-sample-rl-finetuning/reft]] — 1–2 epoch SFT warm-up + PPO on multiple sampled CoTs; +10–12 pp over SFT alone.
- [[../single-sample-rl-finetuning/cbrl]] — demonstrations prepended during RL with linearly annealed injection probability; gains *persist* after withdrawal.
- [[../teacher-student-rl/knowrl]] — atomic knowledge-points injected on hard samples, CSS-selected to minimal-sufficient subset, withdrawn at inference; pruning interaction paradox documents that more context is not monotonically better.
- [[../teacher-student-rl/co-evolving-policy-distillation]] — alternating GRPO and bidirectional mutual on-policy distillation; demonstrates that SFT-during-RL can sustain top-$k$ overlap >0.90 while RL drives capability.
- [[../self-improvement/star]] — rationalise-then-SFT loop on self-generated correct reasoning; the "SFT-installs, RL-selects" pattern at minimum cost.

**Corpus boundary — what *fails* in this direction.**
- [[../teacher-student-rl/opsd-compresses-rlvr]] — RL-then-SFT (Incorrect-only OPSD) loses 7–10 pp. Distillation after RL only compacts; it cannot install reasoning states the student doesn't already support. **Implication: SFT must precede or alternate with RL, not follow it as a corrective.**

**Design constraints inherited from the corpus.**
1. *Pre-RL or interleaved, not post-RL corrective* (OPSD-compresses).
2. *Minimal-sufficient over maximal context* (KnowRL's pruning paradox; full-KP injection can regress).
3. *Anneal the scaffold* (CBRL: gains persist iff injection probability decays to zero).
4. *Forgetting protection composes here* — components **F** (EWC anchor) and **P2** (Balashov mask) apply to the SFT round as well as the RL round; without them the SFT round risks erasing the very capability the RL round acts on.
5. *Target the support-lifting requirement quantitatively* — the SFT pass should raise $\pi^*(S|x)$ for the target $x$ above the threshold where Theorem 7 becomes feasible. Open: how to measure $p_\gamma$ pre-SFT without a full RL probe.

**What the corpus does *not* yet say.** No captured paper does parametric SFT on a textbook *body* (as opposed to long-CoT demonstrations or per-problem hints) before a per-concept RLT loop. The "SFT-installs, RL-selects" recipe at *textbook-as-target* granularity is consistent with the wiki but **not directly demonstrated**. This is the open experimental question this extension generates.

**Relation to existing components.**
- Composes with **C**: keep reference-in-context for the structural-asymmetry property (the SPICE-locked decision); add **C_w** as a preceding/alternating SFT pass on the same reference.
- Composes with **G**: epiplexity pre-flight ([[../self-play/info-gain-self-play]]) applies before *and* after the SFT pass — if the SFT round doesn't raise learnable-information for the target region, abort before spending RL budget.
- Composes with **V** (MDL sibling test): apply the sibling test after the SFT pass and again after the RL pass. The SFT pass should improve compression on siblings *without* RL; if it doesn't, the SFT data shape is wrong.

**Relation to other method proposals.**
- [[concept-curriculum-method]] step (b) packets already carry a Textbook body alongside $(Q, E, A)$ examples; whether to run weight-update SFT on the Textbook before the inner RL loop is left open in that page. This extension closes that as an explicit design choice.
- [[recursive-concept-learning]] (RCL) inherits the same choice at every recursed-into node.

### Sub-extension: offline logit-reweighting from a subject-matter prior (parametric-free variant) (2026-05-12)

*Open hypothesis surfaced by the user 2026-05-12.* Claim: the relevant information is already in the base model; instead of (or before) any weight update, **reweight logits at inference time with a learned subject-matter prior** to push the model into the right solution space. Naming: **component R_w** (offline reweight prior) — orthogonal to **C** (in-context reference), **C_w** (SFT reference), **C_b** (per-rollout commentary SFT).

**Where the corpus directly supports the hypothesis.**

| Result | Source | What it says |
|---|---|---|
| **Token-level: RL = sparse logit rerank within base top-5** | [[../rlvr-mechanics/rethinking-rl-sparse-selection]] | Across GRPO/PPO/RLOO and three families: **0% of RL-promoted tokens lie outside base top-5**; 1.0–4.1% of positions reranked; mean rank 2.14–2.39; oracle intervention at those positions exactly recovers RL pass@1. **The information IS in there; RL only reranks at high-entropy positions.** |
| **REASONMAXXER: rank-32 $W_O$ LoRA at 0.27–0.49% params matches RL** | [[../rlvr-mechanics/rethinking-rl-sparse-selection]] | Operationalises the offline reweight: ~50 problems + entropy-gated contrastive + rank-8 $W_O$ LoRA = 0.04% params; \$4–25 vs \$200–\$103k. **Strongest existence proof in the corpus that an offline prior suffices.** |
| **BOLT closed-form static target** | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] | $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$ — the KL-RLVR target is a Boltzmann tilt of the base. Static reweighting reaches the same target as online RL at 75–85% less wall-clock. |
| **Filtered model $p^*$ as I-projection** | [[../rlvr-mechanics/binary-rewards-rl-challenges]] | The verifier-filtered model IS a reweighting; information-geometric structure (Dymetman). |
| **ICL = posterior over latent pretraining concepts** | [[../in-context-learning-theory/icl-bayesian-inference]] | Theoretical underpinning: conditioning shifts the prior. Per-token-information theorem makes "long reference in context > many short examples" formal. **The hypothesis as a theorem.** |
| **Algorithm Distillation: frozen weights, all in-context** | [[../test-time-training/algorithm-distillation]] | Limit case: transformer pre-trained on RL learning histories *executes the RL algorithm in-context with no weight updates*. |
| **CBM test-time intervention** | [[../concept-learning/concept-bottleneck-models]] | Literally edit concept coordinates at inference. |
| **TEMPO E-step verifier-ensemble recalibration** | [[../test-time-training/tempo]] | M-step refines policy; E-step is verifier-ensemble logit reweighting; +18.1pp AIME24 on OLMO3-7B. |
| **rStar test-time multiplier** | [[../self-play/rstar]] | No fine-tuning; 32 MCTS × 5 actions + peer discriminator; LLaMA2-7B GSM8K **12.51% → 63.91%**. Pure decoding-time reweighting at the trajectory level. |

**Corpus gap closed 2026-05-13.** The classical *decoding-time-only* family is now a full theme: [[../decoding-time-steering/_overview]]. Thirteen captures spanning four years (PPLM 2019 → Park-Veitch 2024), all supporting the R_w claim with no contradictions. Primary anchors for the R_w extension:

| Anchor | Why load-bearing |
|---|---|
| [[../decoding-time-steering/iti]] (Li 2023) | **40% probe–generation gap** on LLaMA-7B TruthfulQA — direct quantitative evidence model "knows but doesn't say". TruthfulQA Alpaca 32.5% → 65.1% via head-level activation shift; ~40–81 contrast pairs suffice. |
| [[../decoding-time-steering/repe]] (Zou 2023) | Umbrella framework — LAT scan + reading vector + linear/piecewise/projection-erasure control + LoRRA. **Concept-reading beats few-shot prompting on 5 QA benchmarks.** 4-experiment evaluation protocol (correlation / manipulation / termination / recovery). |
| [[../decoding-time-steering/dola]] (Chuang 2023) | **Single-model layer-contrast** — no auxiliary model, no training, no retrieval. +12–17pp TruthfulQA on LLaMA family via late-vs-early-layer logit subtraction. Cleanest "info is intrinsic" demonstration. |
| [[../decoding-time-steering/cd-improves-reasoning]] (O'Brien 2023) | Math/reasoning regime: LLaMA-65B + CD = 57.7 on GSM8K, beats PaLM-540B. Mid-training-checkpoint amateurs better than fully-trained small models — operationalises "skill increment recoverable post-hoc by subtraction." |
| [[../decoding-time-steering/cfg-lm]] (Sanchez 2023) | Structural parallel to BOLT: $\log P(w\|c) + \gamma(\log P(w\|c) - \log P(w))$ — same multiplicative-reweighting form as $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$, with prompt-direction acting as the reward signal. **LAMBADA SoTA at 7B beating PaLM-540B.** |
| [[../decoding-time-steering/linear-rep-hypothesis]] (Park 2024) | **Formal theory anchor.** Theorem 2.5: adding $\bar\lambda_W$ to context increases $P(W=1)$ while leaving causally-separable concepts unchanged. Theorem 3.2: causal inner product unifies probing (reading) and steering (control) via Riesz isomorphism. Concept = cone direction defined by counterfactual pairs. |
| [[../decoding-time-steering/actadd]] (Turner 2023) | **$n=1$ contrast-pair limit** — the absolute data-efficiency floor of the family. Two prompts, no labels, no optimisation. Single-sample existence proof at activation level. |
| [[../decoding-time-steering/dexperts]] (Liu 2021) | Product-of-experts decoding $\mathbf{z}_t + \alpha(\mathbf{z}^+ - \mathbf{z}^-)$ with anti-expert direction; small specialist LMs steer frozen base via logit-additive prior. Most direct prior-art instantiation of R_w. |

See [[decoding-time-shapes]] for the cross-source synthesis: 13 methods tabulated by intervention point × data floor × access × mechanism × R_w-implication, plus the Bayesian-vs-Boltzmann correspondence connecting decoding-time and training-time reweighting onto the same target distributions.

**Unanimous finding across all 13 captures:** the information is in the base model; an offline reweighting prior (logit-space or activation-space) suffices to put it into the right solution space. No paper contradicts; this is the four-year empirical / methodological / theoretical consensus that R_w stands on.

**Weight-level backbone added 2026-05-13.** Where the decoding-time-steering theme is the inference-time / reweighting backbone, [[../selective-finetuning/_overview]] is the **training-time / weight-modification backbone** for R_w. Fifteen captures across four sub-families: knowledge editing (locate-then-edit), skill localization, continual-learning gradient masking, and PEFT with explicit weight decomposition. Primary anchors for selective gradient application:

| Anchor | Why load-bearing |
|---|---|
| [[../selective-finetuning/rome]] (Meng NeurIPS 2022) | **Rank-one MLP edit** at causal-traced mid-layer FF: factual associations are localised; surgical overwrite leaves other behaviour unchanged. |
| [[../selective-finetuning/memit]] (Meng ICLR 2023) | Scales ROME to **thousands of edits** distributed across critical mid-layers; least-squares solve on GPT-J 6B / GPT-NeoX 20B. |
| [[../selective-finetuning/alphaedit]] (Fang ICLR 2025 Outstanding) | **Null-space projection**: perturbation projected onto null space of preserved knowledge — by construction cannot affect preserved-fact outputs. Plug-and-play on ROME/MEMIT (+36.7%). Closest captured mechanism to "selective gradient mathematically cannot affect other behaviours." |
| [[../selective-finetuning/skill-localization]] (Panigrahi ICML 2023) | **0.01% of params carry >95% of fine-tuned skill** via grafting. Direct empirical evidence that skills isolate to sparse subsets. |
| [[../selective-finetuning/lima]] (Zhou NeurIPS 2023) | **1000 curated examples** preserve format and beat RLHF. **Superficial Alignment Hypothesis**: knowledge from pretraining, format from a tiny surface patch. The wiki's central distinction stated as a paper's headline. |
| [[../selective-finetuning/surgical-finetuning]] (Lee ICLR 2023) | **Selectively fine-tune subset of *layers***; different shifts → different layer choices. Theoretical justification for 2-layer nets. Direct prescription for "apply gradient to specific layers only." |
| [[../selective-finetuning/o-lora]] (Wang EMNLP 2023 Findings) | Each new task in a **LoRA subspace orthogonal to all prior task subspaces** — direct realisation of "isolated subspaces for isolated behaviours" at the parameter level. |
| [[../selective-finetuning/dora]] (Liu ICML 2024 Oral) | Weight = **magnitude × direction** decomposition; LoRA on direction only; mimics full-FT update geometry. Demonstrates that *kinds* of updates can be structurally isolated. |
| [[../selective-finetuning/pit]] (Jiang 2024) | **Pre-instruction-tune on QA before CPT on documents**: model learns "how to encode knowledge for QA-style access" before seeing the new documents. **Direct knowledge-injection recipe that preserves QA format.** Closest captured paper to component **C_w⁺** (chunked SFT + RLVR-on-summary). |
| [[../selective-finetuning/mend]] (Mitchell ICLR 2022) | **Hypernetwork** learns to transform the fine-tuning gradient via rank-1 decomposition; gradient-as-target alternative to ROME's weights-as-target. Edits on 10B+ models. |
| [[../selective-finetuning/knowledge-neurons]], [[../selective-finetuning/ff-kv-memories]] | Foundational mechanistic story: FF layers as key-value memories (Geva); individual neurons store specific facts (Dai). Why ROME/MEMIT work. |
| [[../selective-finetuning/packnet]], [[../selective-finetuning/hat]] | Pre-LLM continual-learning ancestors: per-task pruned subnetworks (PackNet) and per-task hard-attention gradient masks (HAT). Historical anchors for the gradient-masking lineage. |
| [[../selective-finetuning/knowledge-editing-survey]] | Landscape view: three-category taxonomy + six evaluation metrics (success, generalisation, **locality**, portability, scalability, fluency). The *locality* metric is the explicit "doesn't affect non-target outputs" criterion. |

**Cross-source claim (training-time + inference-time + RL-observed):** behaviour is *isolable* in identifiable parameters / subspaces / layers / neurons. The localisation scale ranges from single neurons (Knowledge Neurons) through 0.01% of params (Skill Localization) through 0.04% rank-8 $W_O$ LoRA (REASONMAXXER) through 5–30% (Balashov spontaneous). The corpus has converged on this from multiple independent directions — making selective SFT a mechanistic claim, not just an engineering aspiration.

**Composing the recipes — locked 2026-05-13 (design ruling).** User confirmation: *"These should all be complementary."* The five primitives target structurally different surfaces and compose without conflict; the working architecture is the full stack, not a choice among alternatives.

| Stage | Primitive | Surface acted on | Source |
|---|---|---|---|
| 1 | **Ordering** | Sequence of training stages | [[../selective-finetuning/pit]] — instruction-tune on QA *before* CPT on documents |
| 2 | **Sparse mask** | Which parameters receive gradient | [[../selective-finetuning/skill-localization]] — restrict to ~0.01% subset carrying the skill |
| 3 | **Orthogonal subspace** | Direction of gradient flow | [[../selective-finetuning/o-lora]] — LoRA in subspaces orthogonal to prior tasks |
| 4 | **Surgical edit** | Atomic factual rewrites | [[../selective-finetuning/rome]] / [[../selective-finetuning/memit]] — rank-one MLP updates for facts that don't need full SFT |
| 5 | **Null-space projection** | Perturbation orthogonal to preserved-knowledge outputs | [[../selective-finetuning/alphaedit]] — wrap the whole stack so perturbations cannot affect preserved-fact outputs |

No captured paper tests the composition end-to-end. The pieces target disjoint surfaces (when to update / which params / which direction / which atomic edits / which output-invariance constraint), so they are formally non-conflicting. The wiki's working frame is: **treat them as a composable stack of design primitives, not as alternatives to choose between.**

**Three structural answers to skill-stacking interference (added 2026-05-16).** A /research run on "does RLVR skill-stacking just reallocate optimization?" surfaced that the corpus offers three complementary answers, now three themes:

| Answer | Mechanism | Theme |
|---|---|---|
| **Implicit** | On-policy RL is biased toward KL-minimal, off-principal, sparse solutions → monolithic stacking is gentle (RL forgets far less than SFT) | [[../catastrophic-forgetting/_overview]] (RL's Razor, Path-Not-Taken, RFT-mitigates-forgetting) |
| **Explicit** | Mask / anchor / orthogonalise the gradient so it cannot move prior-skill params | [[../selective-finetuning/_overview]] (EWC, O-LoRA, AlphaEdit null-space, Skill-Localization) |
| **Architectural** | Don't co-train skills — route separately-trained delta/LoRA experts at inference (the user's **MoERA** technique) | [[../moe-adapters/_overview]] (LoRAMoE, BTX, Self-MoE, MoRAM) |

These compose with the C_w / C_b / R_w stack: the implicit answer ([[../catastrophic-forgetting/rls-razor]]) is *why* an RLVR-based installation loop degrades response style less than an SFT-based one (mechanistic support for component **L**); the architectural answer ([[../moe-adapters/loramoe]]) is a routing-based alternative realisation of R_w (install a behaviour in one expert, leave the others untouched — vs. locate-then-edit or orthogonal-subspace). [[../moe-adapters/loramoe]] is the bridge — a forgetting-mitigation method built from routed LoRA experts, filed under moe-adapters but load-bearing for both themes. Open: no captured paper trains the routed experts by RLVR (which per [[../catastrophic-forgetting/rls-razor]] would make them KL-minimal/off-principal); RLVR-expert × router composition is the untested MoERA design question.

**Composition with other components.**
- *Replaces or precedes RL*: REASONMAXXER's existence proof says ~50 problems + rank-8 $W_O$ LoRA can substitute for Stage 2(a) entirely. The question for this project is whether the same recipe works *per concept* (not just per benchmark).
- *Composes with **C_w***: an offline reweight LoRA trained on chunk-derived QA is a parametric-free instantiation of **C_w**. The chunk's information enters via the reweight prior, not full-weight SFT.
- *Composes with **L***: a static reweight prior cannot cause format collapse (no gradient flow through $\pi_\text{base}$), so **L** is unnecessary in the pure-reweight variant. This is the strongest case for offline-only operation.
- *Bounded by the same coverage wall*: [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7's $N \gtrsim 1/p_\gamma$ applies — if the concept isn't in $\pi_\text{base}$'s support, no reweight installs it. Capacity expansion still requires SFT-distillation per [[../self-play/yue-rlvr-boundary]].

### Sub-extension: chunked SFT + RLVR-on-summary (Stage 1 variant) (2026-05-12)

*Refines **C_w**.* User's 2026-05-12 sketch: chunk the textbook, SFT each chunk into weights, then have the model emit a *summary of what it learned* and treat that summary-generation as RLVR with a bounded reward. Naming: **component C_w⁺** (synthesis-bounded textbook SFT).

The bounded-reward question has at least six corpus-attested shapes. **The wiki's strongest single answer is RLT $r^{SS}$ with chunk-derived held-out QA as the eval set** — the summary plays the role of teacher think-tokens $t$ in [[../teacher-student-rl/sakana-rlt]]; bounded by normalised log-prob; reward correlates $r=0.89$ with student gain.

| Reward shape | Source | What bounds it |
|---|---|---|
| RLT $r^{SS} = \log\pi_s(s\mid t, q)$ over chunk-QA | [[../teacher-student-rl/sakana-rlt]] | Log-prob normalisation + RLT $r^{KL}$ against answer-leakage |
| L2T Fisher/SVD info-gain | [[../rlvr-mechanics/learning-to-think]] | Fisher norm; label-free; $r/d\approx 1\text{–}10\%$ |
| Epiplexity prequential MDL | [[../self-play/info-gain-self-play]] | MDL; use as gate not gradient |
| Self-judge rubric | [[../self-improvement/self-rewarding-lm]] | Rubric range. **Caveat:** gains transfer to open-ended generation but not to math/reasoning under OA seed |
| Process verifier per step | [[../process-reward-models/math-shepherd]] | Binary verifier on step-success rate |
| TRICE marginal-LL with control variate | [[../teacher-student-rl/trice-cot-latent-variable]] | Variance-reduction; learns from incorrect summaries |

**Design constraints.** Epiplexity pre-flight ([[../self-play/info-gain-self-play]]) applies between chunks — if a chunk's summary doesn't raise learnable-information for the held-out QA, abort that chunk before spending RL budget. Self-Rewarding LM's length-blowup ($1092 \to 2552$ tokens across 3 iterations) is a format/fluency warning — see component **L** below. STaR temperature ablation requires trace-level filtering, not answer-level.

**Open questions.**
- Granularity: paragraph, section, or chapter as the chunk unit? Wiki has no precedent at textbook scale.
- Whether to interleave chunked SFT with the per-exercise inner loop (CoPD-style) or run all chunks first (DeepSeek-R1 cold-start style).
- Whether the RLVR-on-summary step counts toward Stage 2 (and competes for compute with Stage 2(a)+(b)) or Stage 1.

### Sub-extension: per-rollout commentary-SFT (Stage 2(b) variant) (2026-05-12)

*Refines the inner loop alongside **C_w**.* The user's 2026-05-12 sketch proposes a two-step inner loop per exercise: **(a)** RL/BOLT on the exercise — rollouts, verifier scores, optimise — followed by **(b)** *for each rollout*, generate a teacher commentary, append to the sample, and SFT on the (rollout + commentary) pair. Naming: **component C_b** (per-rollout commentary-SFT).

**Corpus precedents — three independent attestations, never composed.**
- [[../self-improvement/star]] rationalization branch is the closest precedent: on failures, prepend gold answer as a hint, resample a rationale, keep ones that now produce the gold, SFT on the union with hint stripped. STaR's outer loop is the proposed inner loop's structure.
- [[../single-sample-rl-finetuning/critique-ft-one-problem]] is the amplification existence proof: 1 problem × 10 generators × 7 teacher critiques → 600 (problem, candidate, critique) SFT rows; beats 1-shot RLVR at 1/15–1/20 compute on Qwen2.5-Math-7B. Calibrates Stage 2(b)'s per-exercise yield.
- [[../teacher-student-rl/trice-cot-latent-variable]] handles wrong rollouts: rationales as latent variables, marginal-LL via MCMC-EM with control variate, **learns from incorrect rationales**, beats STaR. Directly answers "what to do with teacher commentaries on failed rollouts that still carry gradient information".
- [[../teacher-student-rl/co-evolving-policy-distillation]] alternating GRPO + bidirectional mutual on-policy distillation is the existence proof that the (a)/(b) interleave sustains top-$k$ overlap >0.90 while RL drives capability. *Alternating*, not *simultaneous-per-rollout*.
- [[../critique-self-correction/critic-cot]] gives the recipe for *building* the commentary generator via weak-supervision critique-refine pairs; 93.3% GSM8K when used as the trained critic.
- [[../teacher-student-rl/sakana-rlt]]'s $r^{SS}=\log\pi_s(s\mid t,q)$ formalises "teacher commentary as the think-tokens $t$"; the dense per-token signal Stage 2(b) wants to capture parametrically.

**Design constraints inherited from the corpus.**
1. *Order matters.* [[../teacher-student-rl/opsd-compresses-rlvr]] — SFT after RL only *compacts* (Incorrect-only OPSD loses 7–10pp). Stage 2(b) must run *interleaved* with Stage 2(a), per-rollout — not as a post-exercise corrective. The same boundary that constrained **C_w**'s position relative to RL applies recursively inside the per-exercise loop.
2. *Filter at trace level, not answer level.* STaR temperature ablation (Section 5): correct-answer-via-wrong-reasoning poisons the SFT signal. Stage 2(b)'s SFT step needs commentary-quality gating, not just answer-correctness.
3. *Wrong rollouts still carry gradient.* TRICE's marginal-LL framing argues against discarding failed rollouts — they should drive an MCMC-EM-style update on the commentary distribution rather than be dropped. Stage 2(b)'s filter shape (keep-only, weight-by-correctness, or full marginalisation) is a design knob.
4. *RL gradient + SFT gradient on the same rollout is uncharacterised.* Captured methods *alternate* (CoPD) or *filter-then-SFT* (STaR) — not *simultaneous-per-rollout*. The double-counting risk is open.

**What the corpus does *not* yet say.** No captured paper applies, *per rollout, in the same inner loop step*, both an RL update (advantage-weighted on the rollout) and an SFT update on (rollout + generated commentary). The natural composition of STaR-rationalize + critique-FT + TRICE-wrong-rollout-salvage at per-rollout granularity is novel as a composition.

**Relation to existing components.**
- Composes with **R**: keep RLT reward as Stage 2(a)'s gradient-of-record; commentary in **C_b** can be either the same teacher's think-tokens $t$ (parametric instantiation of Sakana's $t$) or an independent critique stream (critic-CoT trained separately).
- Composes with **V** (MDL sibling test): apply gate after the combined (a)+(b) step. If only (b) improves MDL on siblings, the RL contribution is decorative; if only (a) does, the commentary-SFT is decorative; both is the load-bearing signal.
- Composes with **C_w**: same support-lifting argument applies — commentary-SFT extends $\pi^*(S\mid x)$ in directions the rollout-only weighted-SFT (BOLT) cannot reach when the rollout support is reward-truncated.
- Composes with **G** (diversity): commentary-SFT compounds STaR's "rationalise many ways" with critique-FT's "many wrong rollouts × many critiques" — Stage 2(b) is *where* the diversity Ho-reasoning-teachers calls load-bearing actually enters weight-space.

**Open experimental questions.**
- Per-rollout SFT vs per-exercise SFT (batch all rollouts' commentaries, then one SFT pass at end of exercise).
- Commentary generated by the same teacher producing think-tokens for **R**, or by a separately-trained critic ([[../critique-self-correction/critic-cot]])?
- Whether iterative BOLT ([[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 11) as Stage 2(a)'s optimiser interacts coherently with per-rollout SFT in (b) — sampler refresh between BOLT rounds may double-count what (b) already installs.
- Stage 2(b) at $G=1$: with one rollout per exercise, the (b) step degenerates to "STaR-rationalize-one-trace + SFT" — a cheaper baseline that Stage 2(a) must justify itself against.

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
