---
name: rstg-selective-negative-group-distillation
description: RSTG gates OPD+SFT distillation exclusively onto GRPO's all-fail zero-variance groups, confidence-weighted and token-masked, fixing naive GRPO+OPD's math regression
type: research
---

# Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance

Han, Xiao, Lu et al. (TJU / Meituan LongCat), arXiv:2608.00782. RSTG (Recover Signal via Teacher Guidance) gates on-policy distillation (OPD) so it fires *only* on GRPO groups where all $G$ rollouts fail (negative zero-variance, $\hat A_i=0$ everywhere) — teacher-confidence-weighted, token-masked to high-entropy/high-divergence positions, plus an auxiliary SFT term on teacher-generated correct traces. This selective gating fixes a documented failure: naively blending GRPO with OPD across *all* prompts underperforms plain GRPO on math (−0.2 to −1.57 pts across model pairs) despite helping on code. RSTG beats both plain GRPO and naive GRPO+OPD uniformly — +4.02% math / +3.05% code aggregate over naive GRPO+OPD — while restricting the OPD training signal to just 3.63% of the 57K-sample math set (the negative-zero-variance subset), and explicitly measures/preserves exploratory capacity via a token-overlap metric so the student doesn't collapse onto the teacher's distribution.

## Why naive GRPO+OPD fails (three reasons, §1)

The paper's starting puzzle: blending OPD into every GRPO step degrades math performance. Three causes identified:

| Reason | Mechanism |
|---|---|
| **Sample-level uniformity** | OPD applied indiscriminately across all prompts — including ones GRPO already handles fine — dilutes the RL signal with distillation noise where it isn't needed. |
| **Teacher-boundedness** | Full-strength OPD pulls the student toward the teacher's ceiling everywhere, capping exploratory capacity even on prompts where the student is already competitive or could out-explore the teacher. Echoes the "teacher ceiling" argument in [[../self-play/invisible-leash]]. |
| **Advantage asymmetry** | OPD's reverse-KL-as-advantage is systematically *more negative* on negative-zero-variance prompts than positive-zero-variance prompts (Fig. 4) — the term that most needs positive signal gets the most punishing one, compounding rather than correcting the zero-gradient problem. |

RSTG's answer is not "tune how much OPD to blend in" — it's "apply it only where GRPO structurally has zero gradient, and even then, sparingly." Ablating away the careful weighting/masking machinery (leaving raw OPD-on-negative-groups) actually drops below the simpler ReLIFT baseline (51.74 vs 52.52 avg) — the fix is the specific combination, not "add OPD to negatives."

## Method

Three components, activated only when a GRPO group is negative zero-variance ($r_j = 0\ \forall j \in G$):

**1. Confidence-weighted OPD on negative groups (§4.1, Eq. 9).**

$$A^{Hybrid}_{i,t} = \begin{cases} \beta \cdot \omega_i \cdot A^{OPD}_{i,t} & \text{if } r_j=0\ \forall j \in G \\ A^{GRPO}_{i,t} & \text{otherwise} \end{cases}$$

$\omega_i \in [0,1]$ is the teacher's mean@8 mastery score on the prompt (how reliably the teacher solves it). $\beta$ is linearly annealed: $\beta_{init}=5\times10^{-3}$, decay $\delta=5\times10^{-5}$, floor $\beta_{min}=1\times10^{-3}$ — shared between the OPD and SFT terms.

Data-selection finding (Fig. 3): restricting OPD training data to `Dswtr` (student-fails-all-8, teacher-succeeds-all-8) — only **3.63%** of the 57K-prompt set — *outperforms* OPD trained on the full dataset `D`. `Dsw` (student-fails-all, any teacher outcome) is an intermediate improvement over full-`D` OPD; `Dswtr` is best. This is a data-selection/curriculum efficiency claim restricted to the distillation signal — the underlying RL training still consumes all 57K prompts.

**2. Token selection (§4.2, inspired by Xu et al. 2026 / TIP).** Mask OPD gradients to the top-k% tokens by combined score

$$s_t = \hat h_t + \hat d_t - \hat h_t \hat d_t$$

(Soft-OR of normalized student entropy $\hat h_t$ and teacher-student divergence $\hat d_t = |A^{OPD}_{i,t}|$, Eq. 10–13). Slows convergence to the teacher and cuts gradient noise — this is the mechanism that protects exploration, directly targeting the "teacher-boundedness" failure mode above.

**3. Auxiliary SFT on negative groups (§4.3, Eq. 14).** On the same negative-zero-variance prompts, add an SFT loss over teacher-generated correct trajectories (shortest of 8 pre-generated teacher samples per prompt), reframed as off-policy RL with constant advantage $A^{SFT}_t=1$ — injects purely positive gradient exactly where RL has none, counteracting OPD's advantage asymmetry.

### Pseudocode sketch

```
for each GRPO step:
    for each prompt i in batch:
        sample G rollouts, compute rewards r_1..r_G
        if all r_j == 0:                      # negative zero-variance group
            A_OPD  = teacher-reverse-KL-as-advantage(rollouts, teacher)
            A_OPD  = mask_to_topk_tokens(A_OPD, score=soft_or(entropy, divergence))
            A_hyb  = beta * omega_i * A_OPD     # Eq. 9, beta annealed
            loss  += pg_loss(A_hyb)
            loss  += sft_loss(teacher_best_of_8_trajectory, advantage=1)  # Eq. 14
        else:
            A_grpo = group_relative_advantage(r_1..r_G)
            loss  += pg_loss(A_grpo)            # standard GRPO branch
    beta = max(beta - delta, beta_min)
```

## Results

Table 1 headline, Qwen3-1.7B→4B teacher-student pair (math-avg / code-avg):

| Method | Math avg | Code avg |
|---|---|---|
| GRPO | 51.57 | 60.03 |
| GRPO + naive OPD | 51.37 (↓ vs GRPO) | 64.55 |
| **RSTG** | **55.39** | **67.11** |

Aggregate across 3 teacher-student pairs and 6 benchmarks: RSTG beats naive GRPO+OPD by **+4.02% math / +3.05% code**, and beats standard GRPO too. RSTG also beats ReLIFT (SFT-only-on-negatives) and RL-ZVP (entropy-based asymmetric advantage on zero-variance prompts) on 2/3 model pairs.

Incremental ablation (Table 3 / App. A.7), same pair, avg score: GRPO+OPD (naive) 51.37 → +OPD gated to negative-zero-var 52.69 → +Advantage Weighting 53.24 → +Token Selection → +SFT 55.39. Monotonic — every component contributes.

Exploration-preservation check (§5.4, top-16 token-overlap $M_{overlap}$ between teacher/student candidate distributions at step 200): RSTG 65.81% vs OPD-alone 69.7% vs naive GRPO+OPD 67.6% — RSTG keeps the student measurably further from teacher-collapse than either baseline, consistent with the token-selection mechanism doing its job.

Cost (App. A.5): ~12 extra wall-clock hours over 550 steps on 8×A100 vs plain GRPO (plus ~2 hrs on 2×A100 to pre-generate SFT teacher trajectories for the full 57K set) — "fully manageable" per the authors.

## Limitations

- Math and code domains only; agentic tasks left to future work.
- OPD requires "a meaningful capability gap between teacher and student" — the same-size pair (Qwen3-4B-Instruct → Qwen3-4B-Instruct-2507) shows visibly smaller gains, an implicit ceiling-effect the paper flags without resolving.
- Largest teacher tested is 14B; larger-scale effectiveness is asserted, not verified.
- Constant $\beta$ always underperforms the best annealed schedule (Table 2) — some brittleness to the $\beta$ schedule.
- Not framed in concept-acquisition terms; evidence is closer to credit-assignment recovery (zero-variance groups are *unassigned* signal, not *absent* signal) than to compositionality or OOD generalization.

## Relation to two open wiki conflicts

**[[../../conflicts/knowrl-vs-rlt-hint-design]]** is framed as *when/how much* teacher hint or guidance to inject during RL — [[knowrl]] answers with per-problem minimal-sufficient knowledge points (content axis), [[sakana-rlt]] with a KL-regularised dense hint density (density axis). RSTG doesn't take a position on hint content or density — it answers a third, orthogonal question: *which groups* get any teacher signal at all, gated purely by GRPO's own reward variance ($r_j=0\ \forall j$). It sharpens the conflict by adding a data-selection axis neither existing position addresses, rather than resolving either side.

**[[../../conflicts/mcpo-vs-dr-grpo-std-fix]]** is about the same symptom RSTG targets — GRPO groups with identical reward producing zero gradient — but [[../rl-optimizers/mcpo]] (hinge-KL anchor + advantage-denominator rescaling) and [[../rl-optimizers/dr-grpo]] (std-normalization removal) both fix it via *internal* reward/advantage reshaping, no external model required. RSTG is a structurally different, teacher-dependent resolution path: it doesn't touch the advantage formula for non-degenerate groups at all, and requires a stronger external teacher to supply the recovered signal. Orthogonal remedy for the same symptom, not a competing internal fix — worth noting as a third resolution path in that conflict file, applicable only when a teacher model is available.

## Source

- `raw/research/weekly-2026-08-07/02-rstg-teacher-guidance-negative-groups.md`

## Related

- [[knowrl]] — KnowRL answers "what content" to inject via minimal-sufficient knowledge points; RSTG answers "which groups" via reward-variance gating — orthogonal axes of the same hint-design conflict
- [[sakana-rlt]] — RLT is the origin of the teacher-hint-density debate; RSTG's activation is structurally different (binary gate on group variance, not a tunable density dial)
- [[../rl-optimizers/mcpo]] — MCPO fixes the same all-same-reward zero-gradient GRPO group via internal hinge-KL + advantage-denominator rescaling; RSTG is an external-teacher-dependent alternative for the identical symptom
- [[../rl-optimizers/dr-grpo]] — Dr. GRPO's std-normalization fix addresses a disjoint failure mode (length/std bias); RSTG doesn't touch std normalization and operates only on negative-zero-variance groups
- [[../rlvr-mechanics/curriculum-boundary-aware-rl]] — near-identical "zero-advantage collapse" diagnosis with a similar teacher-guided-trace-injection fix, framed as boundary expansion rather than credit-assignment recovery
- [[opsd-compresses-rlvr]] — OPSD's "compaction not correction" claim (OPD can't create new reasoning states) sits in tension with RSTG's claim that OPD recovers otherwise-absent signal specifically on negative-zero-variance prompts, where the student has no signal at all rather than a signal to compact
- [[rlt-followups-2026]] — natural addition to the post-RLT OPD-family landscape as a 2026-08 selective/gated-activation entry
- [[../self-play/invisible-leash]] — RSTG's "teacher-boundedness" failure reason and its explicit slowing of teacher-convergence (token selection, small annealed $\beta$) is a distillation-specific echo of the support-collapse / teacher-ceiling argument
- [[../rl-optimizers/first-principles-two-axis-framework]] — instance of that page's "GRPO-OPD hybrid" structural-extension category (reward-side $T_C$ in-expectation-distillation operator, conditionally gated)
- [[../../conflicts/knowrl-vs-rlt-hint-design]] — RSTG sharpens this conflict along a third axis (when/which groups) rather than resolving the content (KnowRL) or density (RLT) dispute
- [[../../conflicts/mcpo-vs-dr-grpo-std-fix]] — RSTG is an orthogonal, teacher-dependent resolution path for the same zero-gradient-group symptom via external distillation rather than internal reward/advantage reshaping
- [[../../weekly-briefs/2026-08-07]] — brought in by the 2026-08-07 weekly sweep
