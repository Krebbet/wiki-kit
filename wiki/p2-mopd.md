# P^2-MOPD: Parameter-Prior Multi-Teacher On-Policy Distillation

P^2-MOPD (arXiv:2611.03953, StepFun/Adelaide, code SinuoWang/P2-MOPD) improves multi-teacher on-policy distillation (MOPD, the specialist-consolidation stage in [[kimi-k3]] and [[deepseek-v4]]) by parameterizing the student as its own trainable weights plus a learnable linear combination of frozen expert task vectors. Mixing coefficients and weights are trained jointly under the unchanged MOPD loss. On Qwen3-1.7B/4B with four domain experts, it reaches 94.7%/94.9% average recovery vs 80.9%/83.1% for MOPD from the same task-arithmetic start, passing MOPD's final score in half the steps, at 1.09-1.24x wall-clock.

## Method

- Student module (q/k/v/o, gate/up/down): W_m = B_m + sum_k alpha_{k,m} tau_{k,m}, with tau = expert - base (frozen). B and alpha both trainable; no gradient to experts or teachers. Other tensors (embeddings, norms, head) train as in MOPD.
- Init at the task-arithmetic (TA) merge: B = base, alpha = lambda_k, so step 0 equals the merge. Same model class as a plain student; the experts bias the optimization path, not the hypothesis space.
- Granularity: per-module (main, 1008 / 784 coefficients at 4B / 1.7B), per-layer, or per-model (K scalars).
- Distinct from IM-MOPD (merges task vectors at fixed points by validation rule) and from MOPD (TA init), where task vectors only set the start.
- Mechanism claim: weight-only MOPD barely moves along the lagging expert's task vector (MedQA); one scalar per module makes it reachable. The medical gradient sits 98% on alpha_med and is anti-aligned (cosine -0.78/-0.63 at 4B) with finance/IF gradients.

## Results

Four domains (MedQA, CaseHOLD, FinQA, IFBench), 100 steps, avg@3, 3 seeds (Table 1):

| | 4B avg rec. | 4B worst | 1.7B avg rec. | 1.7B worst |
|---|---|---|---|---|
| TA merge | 43.0 | 23.7 | 32.4 | 17.2 |
| MOPD (TA init) | 83.1 | 47.2 | 80.9 | 32.0 |
| IM-MOPD | 88.0 | 84.1 | 67.8 | 48.7 |
| P^2-MOPD | 94.9 | 89.4 | 94.7 | 88.0 |

- At step 50: 92.3 (4B) / 90.5 (1.7B), above MOPD (TA init) final. Ahead in all 24 seed-paired comparisons.
- Raw average score +2.66 (4B), +2.17 (1.7B). Cross-domain std of recovery 21.8 -> 4.6 at 4B.
- Plain MOPD (no TA init) collapses at 1.7B: MedQA 5.2, avg recovery -15.7. MOPD (TA init) at 1.7B ends below the TA start on MedQA (erosion of an existing capability).
- Ablations: coefficients only (in-span, weights frozen) falls far short; weights only equals MOPD (TA init); learning only alpha_med gives 95.0 vs 95.8 avg; random directions instead of task vectors gives 70.2. Both channels needed.
- Cost (Table 7, 8 GPUs): 6.51 h vs 5.26 h at 4B (1.24x); 4.90 vs 4.48 h at 1.7B (1.09x). Update step 5-7x slower; rollouts dominate.
- Granularity (Table 6): model-level 96.5/97.2 avg rec. with 4 coefficients but higher cross-domain std at 1.7B (9.3); layer-level at 4B drops to 73.4.

## Caveats

- Scale: 1.7B/4B Qwen3, four domains, 100 steps; no evidence at frontier scale or with 9+ experts as in [[kimi-k3]].
- Memory: K frozen task vectors at full-weight size resident during training.
- Recovery is normalized by base-to-teacher gap, which varies up to 3x across domains; raw gains are smaller (+2-3 points).
- Baselines were run by the authors on the IM-MOPD harness; IM-MOPD 1.7B varies 18 points across seeds. No independent reproduction (unverified).
- Preprint dated 2026-11-06.

## Source

- raw/research/weekly-2026-11-14/02-p2-mopd.md (arXiv 2611.03953)

## Related

- [[kimi-k3]]: MOPD from 9 specialist RL models; the consolidation step this targets
- [[deepseek-v4]]: another MOPD user
- [[ride-opd-residual-extrapolation]]: also exploits expert-minus-base parameter residuals in OPD
- [[waypoint-opd]]: OPD refinement using RL-shift geometry
- [[dopd-dual-on-policy-distillation]]: OPD variant fixing privileged-information failure
- [[one-shot-opd-data-efficiency]]: OPD diagnostics
