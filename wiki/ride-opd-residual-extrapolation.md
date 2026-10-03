# RIDE: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation

RIDE (arXiv:2609.36484, USTC/Rutgers/ZJU et al.) is an on-policy distillation (OPD) refinement for the same-initialization setting (teacher = RL(base), student initialized at base). It extrapolates the teacher-minus-base hidden-state residual past the teacher, with target h* = lambda*h_T + (1-lambda)*h_B, instead of regressing to the teacher (OPRD, lambda=1) or extrapolating in output space (ExOPD). The authors claim RIDE matches or exceeds the RL teacher on all four base/teacher pairs (math, lambda=1.25), while ExOPD degrades below the teacher. Theory attributes ExOPD's instability to a (lambda-1)^2 variance term that RIDE's deterministic hidden-state gradient avoids. Brand-new paper with no external discussion yet.

## Method

- Setting: base, teacher and student share architecture, tokenizer and LM head. On each student-generated prefix, run frozen teacher and frozen base. Layerwise residual Delta^(l)_t = h_T^(l) - h_B^(l).
- Target (Eq. 6): h* = h_T + (lambda-1)Delta. Loss (Eq. 7): masked, dimension-normalized MSE of student hidden states to sg(h*), over all L layers and the last k=2000 response positions. Loss rescaled by lambda^-2 (Remark G.1).
- lambda=1 recovers OPRD (on-policy layerwise hidden-state regression, Yang et al. 2026a) exactly. Only the target differs.
- Theory:
  - Prop 4.1: ExOPD (output-space extrapolation, Yang et al. 2026b) has sampled-token advantage A_lambda = l(v) - (lambda-1)rho(v). Its conditional variance contains a (lambda-1)^2 Var[rho] term that does not vanish as p->q. RIDE's gradient is deterministic given the rollout (conditional variance 0).
  - Under a shared linear head, the output-space target is the head projection of the RIDE target (Eq. 8). The head attenuates the residual anisotropically and constrains no layer below the final one.
  - Prop 4.2: the regression equals maximizing a linear directional reward (lambda-1)<h-h_T, Delta> under a quadratic penalty centered at the teacher.
- Background lineage: OPD (Agarwal 2024, Gu 2024, Thinking Machines 2025), ExOPD / generalized-OPD reward extrapolation, OPRD, implicit-reward view (DPO, PRIME), task arithmetic / weight extrapolation, linear-representation steering (Turner, Zou, Arditi).

## Results

Setup: four pairs (R1-Distill-1.5B -> JustRL-1.5B, Qwen3-4B -> Just-Qwen3-4B, Llama-3.2-3B -> Just-Llama-3.2-3B, Phi-4-mini -> Just-Phi-4-mini). DAPO-Math-17K prompts, 500 steps, 3 seeds, lambda=1.25. Metric: Avg@16 over AIME24, AIME25, AIMO (AMC22-23).

Table 1 Avg. (teacher / student / OPD top-1 / OPRD / ExOPD / RIDE):

| Pair | Teacher | Student | OPD top-1 | OPRD | ExOPD | RIDE |
|---|---|---|---|---|---|---|
| R1-1.5B | 55.30 | 39.00 | 52.90 | 54.50 | 49.87 | 56.38 |
| Qwen3-4B | 65.59 | 62.82 | 59.24 | 62.01 | 48.75 | 66.07 |
| Llama-3.2-3B | 13.01 | 6.99 | 1.08 | 10.94 | 6.95 | 13.33 |
| Phi-4-mini | 17.96 | 15.13 | 12.90 | 17.33 | 12.22 | 18.30 |

- RIDE margin over OPRD: 0.97 to 4.06 points. Over ExOPD: 9.1 points on average. RIDE is the only method whose mean exceeds the teacher on all four pairs (Fig. 3).
- Authors' caveat: on three pairs the margin over the teacher is within one across-seed std (Table 4). Llama AIME numbers sit near the eval floor, so the evidence there rests on AIMO.
- ExOPD falls below the untouched student on the three small-RL-gap pairs (by 14.1 points on Qwen3-4B). It also falls below OPD top-1 on R1-1.5B (49.87 vs 52.90), though RL moved that teacher 16.3 points.
- Lambda sweep (Fig. 4, R1-1.5B, single runs):
  - RIDE: 48.2 at 0.5, 54.3 at 1, 55.4 at 1.25 (peak), 55.2 at 1.15, 55.3 at 1.35, 52.3 / 52.4 at 1.5 / 2. Degradation is graceful.
  - ExOPD: best at lambda<=1 (52.9), 49.9 at 1.25, 46.2 at 2. Format score drops from 92% to 64%.
  - lambda>=1 shortens RIDE responses to 5.3-5.7k tokens. lambda<1 lengthens them to 6.8-7.4k.
- Mechanism (Fig. 1, 5):
  - The 512 weakest LM-head directions hold 79.8% of residual hidden-state energy (33.3% under isotropy) but only 30.0% of centered-logit energy.
  - Those directions receive 73.0% of the representation-loss gradient but 48.6% of the output-KL gradient.
  - The residual keeps 0.59 of an isotropic direction's head gain. Head singular values span 71.7 to 1.8.
  - ExOPD conditional variance rises 12.6x from lambda=1 to 2. The variance minimum sits near lambda~1.14.
  - Teacher head drift from base: 1.65%.
  - Student update cosine with the residual: 0.954. Realized projection 1.69 vs target 1.25 (student overshoots).
- Ablation (Table 3, R1-1.5B): random-direction (55.04), reversed (53.90), mismatched-origin residual from Qwen2.5-Math-1.5B-Instruct (54.75) and trajectory-mismatched (55.12) all land within about 1 point of OPRD (54.50). RIDE reaches 56.38, so the gain is attributed to the true RL-induced residual on identical prefixes.

## Applicability

- Candidate uses: distilling an RL run back into its base, or merging RL experts that share a base (the multi-teacher OPD stage in specialist-merge recipes, cf. [[kimi-k3]], [[sensenova-u1-5]], [[agents-a1-horizon-scaling]]).
- Prerequisites: pre-RL base checkpoint, shared architecture/tokenizer/head, hidden-state access to all layers, three forward passes per rollout (student, teacher, base). Per-rollout cost is in Table 6, not read.
- Limits stated by the authors: single global lambda, math reasoning only, one RL recipe (JustRL). Calibration and safety of students trained on non-realizable hidden-state targets are untested. Overshooting the teacher could amplify RL biases.

## Novelty/caveats

- Refinement and recombination: OPRD (hidden-state OPD) plus ExOPD-style lambda scaling of the implicit teacher-base reward, moved from output space to hidden-state space. Closest priors: OPRD (the lambda=1 case) and ExOPD (same lambda and reference, different space).
- New elements: the head-attenuation analysis, the (lambda-1)^2 conditional-variance proposition explaining ExOPD instability, the reward-plus-penalty interpretation, and the direction-control ablations.
- Related prior work cited: RISE (2609.05295), "Extrapolation cliff in OPD" (2605.08737), PHF (2606.29340), Li et al. 2604.13016 (OPD failure modes).
- Gains over the teacher are small and within seed noise on three of four pairs. Lambda sweep is single-run on one pair.
- Soft tension with [[reasonmaxxer]], which describes RL changes as sparse (1-4% of token positions, rank-32 LoRA correction). RIDE treats the RL change as a dense, consistent direction in every layer. Compatible (sparse in token space vs a representation-space direction), but the framing differs. See also [[sparse-policy-selection-vs-gradient-cancellation]].
- ExOPD degradation under output-space extrapolation is not otherwise covered in the wiki.

## Reproducibility

- Code, RL-teacher checkpoints and eval scripts are "released upon publication". The abstract gives a project page link (github.com/xixixixixxxx/RIDE). Release status not verified.
- Base checkpoints and JustRL-1.5B are public. Other teachers are built from the public JustRL recipe. Hyperparameters in Table 5. Proofs in Appendix A.
- Only part of the appendices (lines 1-884 of 1286) was read in ingest. Remaining appendix content is unverified.

## Source
- arXiv: 2609.36484
- Captured: `raw/research/weekly-2026-10-03/01-ride-opd-residual-extrapolation.md`

## Related
- [[one-shot-opd-data-efficiency]] — OPD diagnostic study; RIDE adds an objective-level refinement
- [[dopd-dual-on-policy-distillation]] — another OPD refinement (token routing); RIDE changes the target space
- [[flux-opd]] — OPD target reformulation (geometric-mean target) for non-verifiable tasks
- [[anti-self-distillation]] — OPD/OPSD target fixes
- [[rlsd-self-distilled-rlvr]] — direction vs magnitude decoupling in self-distillation
- [[negative-self-distillation]] — OPD/OPSD cluster
- [[u-opsd-unsupervised-self-distillation]] — OPD/OPSD cluster
- [[reasonmaxxer]] — RL change as sparse token policy selection vs dense representation direction
- [[poem-predicting-rl-outcomes]] — RL policy delta from base (log-ratio vs hidden residual) as a composable linear object
- [[rl-teachers]] — RL teacher to student transfer
- [[agents-a1-horizon-scaling]] — multi-teacher OPD stage
- [[kimi-k3]] — MOPD from 9 specialist RL models
- [[sensenova-u1-5]] — multi-teacher OPD consolidating RL experts
- [[sparse-policy-selection-vs-gradient-cancellation]] — RL as small, structured, consistent updates
