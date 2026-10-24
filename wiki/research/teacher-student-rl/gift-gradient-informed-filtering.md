# GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL (SJTU/Tencent)

GIFT selects which tokens receive on-policy self-distillation (OPSD) loss during GRPO by splitting each token's distillation gradient into components parallel and orthogonal to the RL gradient, keeping tokens that either conflict (first) or add a novel direction, then annealing the kept fraction linearly to zero so the final policy is pure outcome-RL. Highest average among 8 baselines on all three Qwen3 sizes over AMC23/AIME24/AIME25 (+2.99 to +5.03% relative over base). Gains are small and concentrated on AIME25. Code: github.com/lilifree/GIFT. Note: summary-derived; the OLMo-3-7B-Think results and appendices were not read (capture truncated).

## Method

- **Loss:** $L = L_{GRPO} + \frac{\lambda}{N_{valid}} \sum_i m_i(t)\, w_i\, sKL_i$, with $\lambda=1$. Teacher = same model conditioned on a reference solution (OPSD, privileged info).
- **Per-token geometry (logit space):** $r_i$ = GRPO gradient, $d_i = w_i(p_i - \tilde q_i)$ = distillation gradient. $a_i = \langle d_i, \hat r_i\rangle$ (negative = conflict), $b_i = \|d_i - a_i \hat r_i\|$ (orthogonal, novel direction); $a^2+b^2=\|d\|^2$.
- **Score:** $s_i = a_i$ if $a_i<0$; $b_i$ if $a_i\ge 0$; $0$ if no RL gradient (zero-variance group). Rank by $s_i$, keep top $k_t$ across the whole sub-batch. Closed form, $O(|V|)$ per token, no extra backward pass.
- **Coverage annealing:** retention $\kappa_t$ = 1 through a full-coverage phase $H$, then linear to 0 at $T_{exit}$. Conflicting tokens drop first ("teacher loses reach, not voice"). After $T_{exit}$, pure GRPO.
- **Theory (local, first-order, token-level):**
  - Thm 1: $\partial L_{primary}/\partial\eta = -\|r\|^2 - \lambda\|r\|a_i$; sign of $a_i$ is a first-order safety gate.
  - Thm 2: $b_i$ is the maximal distillation decrease among unit-norm perturbations neutral to the GRPO surrogate. A token with $b_i>0$ is not a token-local scalar rescaling of the GRPO gradient, so advantage-modulation methods (RLSD/RLCSD/OPDVR) cannot add new directions. Paper itself: no finite-step or shared-parameter conclusion follows.
  - Thm 3: score ranking exactly solves the lexicographic exact-quota program (min conflicts, then opposition, then max $\sum b^2$).
- **Data:** DeepMath-103K difficulty splits; Knights-and-Knaves (K&K). Qwen3 1.7B/4B/8B.

## Results

| Setting (avg AMC23/AIME24/AIME25, mean@12) | Base | Best baseline | GIFT |
|---|---|---|---|
| Qwen3-1.7B | 51.65 | 53.20 (UFT) | 54.25 |
| Qwen3-4B | 74.67 | 76.85 (LUFFY) | 77.20 |
| Qwen3-8B | 76.67 | 78.04 (OPDVR) | 78.96 |
| K&K avg | 60.60 | 61.95 (OPSD) | 62.85 |

K&K OOD (9-11 roles): +4.70% relative. Baselines: GRPO, OPSD, SDPO, RLSD, RLCSD, OPDVR, LUFFY, UFT.

Ablations (8B math avg):

| Variant | Avg |
|---|---|
| all tokens | 77.49 |
| random tokens | 77.20 |
| entropy-KL selection | 76.92 |
| gradient-cosine selection | 77.63 |
| conflict-only | 77.08 |
| residual-only | 76.97 |
| teacher-norm | 76.90 |
| conflict-free | 77.73 |
| full GIFT | 78.96 |

- Coverage annealing beats sequential (OPSD then GRPO) by 1.59 pp and coefficient-weight annealing by 2.87 pp.
- Scope: sub-batch 78.96 vs per-rollout 77.37 vs per-prompt 77.45.
- Heuristic selectors do not beat random; the gain over "all tokens" is about +1.5 pt and needs the full conflict-then-novelty rule plus annealing.

## Relation to thesis

- **Not a sample-efficiency paper.** No few-shot or single-sample experiment. Only indirect link: the teacher uses a per-prompt reference solution (privileged information), the same supervision form a single-example method would supply.
- **Concept-learning evidence is weak.** Benchmark accuracy plus K&K OOD only; no perturbation, probe or mechanistic test. "Generalizable reasoning skills" is inferred from an OOD gain on n=100 problems per split.
- **Useful design idea for hybrid teacher+RL training:** gate auxiliary dense signal by alignment with the outcome-RL gradient, then withdraw it so the final policy carries no teacher bias. Zero-variance groups (RL gradient vanishes) get neutral score 0, the same case RSTG/SKALD target; relevant when single-sample RL often yields degenerate groups.
- **Token-subset sufficiency:** consistent with [[research/teacher-student-rl/ier-gradient-reliability-opd]] (small subset suffices), with a different criterion (RL-gradient alignment vs Fisher reliability).

## Limitations

- **Stated:** on easier benchmarks (AMC23, AIME24) simpler variants (Conflict-Free, Conflict-only) match or beat full GIFT; full rule pays mainly on AIME25. Theorems are local and first-order.
- **Unstated:**
  - Gains small (AMC23 +0.1 to +0.56%) and concentrated in AIME25 (n=30, noisy). No seeds or variance in the captured text.
  - GIFT not best on AMC23 at any size, nor on AIME24 at 4B/8B.
  - Ablations on one model size per task.
  - Per-token logit-space geometry ignores shared-parameter coupling.
  - Requires reference solutions; inapplicable to label-free settings.
  - Teacher-logit compute cost not quantified.
  - Code and weights promised "upon acceptance" though an abstract repo link exists.
  - Late-stage instability / info-leak acknowledged only via [[research/teacher-student-rl/privileged-info-opsd]].

## Conflict notes

- **Soft, flagged: vs [[research/teacher-student-rl/sequential-opd-then-rl]].** That page says a hard OPD-then-RL switch beats 9 joint methods because joint mixing causes sign-conflicting gradients. GIFT reports filtered-joint training beating sequential by 1.59 pp, and its filter targets exactly that failure mode. Not a strict contradiction: different models, tasks, teachers (self vs external). Note, no ruling.
- **Soft, flagged: vs [[research/rlvr-mechanics/high-entropy-minority-tokens]].** That page: top-20% high-entropy tokens match or beat full gradient. GIFT Table 3: entropy-KL selection (76.92) underperforms random (77.20). Different objective (auxiliary distillation selection vs policy-gradient masking), likely no direct conflict.

## Source

- `raw/research/weekly-2026-10-23/02-gift-gradient-informed-filtering.md`
- arXiv:2610.30796 (SJTU/Tencent)

## Related

- [[research/teacher-student-rl/sequential-opd-then-rl]] — sequential baseline GIFT claims to beat
- [[research/teacher-student-rl/opdvr-verifiable-reward]] — ReLU gate is a scalar modulator; baseline beaten at all sizes
- [[research/teacher-student-rl/rstg-selective-negative-group-distillation]] — group/token gating; zero-variance case
- [[research/teacher-student-rl/rlcsd]] — advantage-modulating baseline
- [[research/teacher-student-rl/ier-gradient-reliability-opd]] — gradient-geometry token selector for OPD
- [[research/teacher-student-rl/sg-opd]] — per-token sign gate
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — token-level update selection
- [[research/teacher-student-rl/privileged-info-opsd]] — reference-conditioned OPSD teachers
- [[../weekly-briefs/2026-10-23]] — brought in by the 2026-10-23 weekly sweep
