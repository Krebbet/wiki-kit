# Waypoint-OPD: Gated On-Policy Distillation of RL-Induced Policy Shifts

Waypoint-OPD (arXiv:2610.21601, Alibaba Cloud) extends Direct-OPD, which uses the endpoint log-ratio log pi_1/pi_0 of an RL-trained teacher as a dense implicit reward for a student. It gates that endpoint shift per prefix by the cosine agreement between the early (Initial to Waypoint) and late (Waypoint to Final) shifts of the same RL run. When the two segments point opposite ways (reversal), the endpoint signal is zeroed. The authors claim the best domain average over OPD, OPD2 and Direct-OPD in all six math/code x student settings. Single-run tables, AIME24 doubles as validation and test, no independent reproduction.

## Method

- Three frozen checkpoints from one teacher RL run (Qwen3-4B, non-thinking RL): Initial pi_0, Waypoint pi_m (RL step 600), Final pi_1 (step 1200). Shared tokenizer with students.
- On each student-generated prefix, take the student's top-k (k=16) candidates with student-renormalized weights q_t and score them with all three teachers.
- Shifts d1 = log pi_m - log pi_0 and d2 = log pi_1 - log pi_m telescope to the endpoint shift d. Each is centered with a q_t-weighted mean (removes the action-independent component).
- Agreement c_t = q_t-weighted cosine of the centered early/late shifts; gate g_t = max(0, c_t), fallback g_t = 1 if either norm <= 1e-8. Batch-scale normalization kappa_B = clip(tau / mean gate, kmin, kmax) keeps the average gate scale stable.
- Dense candidate objective A_t(a) = sg[kappa_B q_t(a) g_t d_t(a)], maximized as sum A_t(a) log pi_theta(a|s_t) minus beta*KL to the student init; dual-clipped PPO in verl.
- The waypoint supplies only consistency evidence, not an imitation target. Cost over Direct-OPD: one extra frozen-teacher scoring pass; no new parameters, rollouts or verifier calls.
- Lineage: OPD (reverse-KL on student prefixes), Direct-OPD (Feng et al. 2026; DPO-style implicit reward), OPD2 (Heo et al. 2026; sign-agreement gate between teacher-minus-base and teacher-minus-student advantages).

## Results

- Math (mean@32 over AIME24/25/26, HMMT Feb25/Nov25/Feb26, AMC23), Avg Waypoint-OPD vs Direct-OPD: Qwen3-8B 56.14 vs 53.96 (+2.18); 14B 59.20 vs 57.61 (+1.59); 30B-A3B 57.85 vs 55.96 (+1.89). OPD 51.04/56.17/51.22; OPD2 51.46/52.83/52.68; bases 26.04/27.32/28.03.
- Teacher Qwen3-4B math: Initial 24.84, Waypoint 51.82, Final 56.13. The 14B and 30B-A3B students exceed the Final teacher by +3.07 and +1.72; 8B matches it. 19 of 21 benchmark comparisons beat Direct-OPD.
- Code (mean@8 over MBPP, MBPP+, LCB v4/v5/v6), 8B/14B/30B-A3B: 53.25/57.82/57.54 vs Direct-OPD 50.59/56.30/56.35. Teacher Final 55.37. Gains in all 15 code comparisons vs Direct-OPD; OPD2 wins individual cells (14B LCB v5, 30B-A3B MBPP/MBPP+).
- Ablations (Qwen3-8B math Avg): full 56.14; no normalization 55.22; no gate 53.50; shuffled gate 51.20 (worse than no gate and below Direct-OPD 53.96, so the gate carries real information). Gaps are non-additive and "no gate" does not isolate centering.
- Training curves: from step 60 it leads Direct-OPD on AIME25/26 and HMMT Nov25 at every evaluation (13/15 checkpoint comparisons); exceeds the Final teacher on HMMT Nov25 only.

## Caveats

- Single run per cell, no seeds or variance; some gaps <0.5pp.
- Checkpoint selection uses AIME24 as validation, which is also in the test average (selection leakage).
- Appendix F (waypoint step 500/600/700 sensitivity) and H (training cost) unread in the ingested extraction.
- Teacher RL checkpoints not stated as released. Code: github.com/hhhbxloveai/WaypointOPD (verl).
- Needs a waypoint checkpoint saved during teacher RL; same-tokenizer students only.

## Applicability

For teams holding an RL teacher with Initial/intermediate/Final checkpoints from one run who want to transfer RL gains to same-tokenizer students without a verifier. Cost is 3x teacher forward on top-16 student tokens.

## Relation to the OPD cluster

- Output-space gating helps here, whereas [[ride-opd-residual-extrapolation]] reports output-space extrapolation (ExOPD) degrades; RIDE works in hidden-state space. Different mechanisms (gating vs extrapolation), so not a direct contradiction.
- Mildly qualifies the premise that the endpoint shift alone is a sufficient signal: a reversal between early and late shifts marks it unreliable.
- "Suppress when signals disagree" parallels [[flux-opd]] (down-weight conflict terms when teachers disagree) and [[dopd-dual-on-policy-distillation]] (per-token routing). The shared log-ratio-as-dense-reward idea appears in [[vimpo]] and [[poem-predicting-rl-outcomes]].
- Gating a selective subset of the shift is consistent with RL changing few tokens ([[reasonmaxxer]]); see [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]. Direct-OPD and OPD2 are not captured as pages.

## Source

- raw/research/weekly-2026-10-17/01-waypoint-opd.md
- https://arxiv.org/pdf/2610.21601

## Related

[[ride-opd-residual-extrapolation]], [[dopd-dual-on-policy-distillation]], [[flux-opd]], [[one-shot-opd-data-efficiency]], [[anti-self-distillation]], [[u-opsd-unsupervised-self-distillation]], [[rlsd-self-distilled-rlvr]], [[vimpo]], [[poem-predicting-rl-outcomes]], [[reasonmaxxer]], [[agents-a1-horizon-scaling]], [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]
