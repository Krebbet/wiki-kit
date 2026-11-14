# OPD Mismatch Tolerance: How Much Training-Inference Mismatch Can On-Policy Distillation Take? (Yu et al.)

Measurement study of how much rollout-engine/trainer mismatch (quantized rollouts, stale weights, injected weight noise) on-policy distillation absorbs before training quality drops. On a 7B student (DeepSeek-R1-Distill-Qwen-7B, teacher Skywork-OR1-Math-7B), OPD keeps held-out KL within $\Delta<20\%$ of the standard run up to 0.184 nats/token of mismatch (>200x the standard vLLM BF16 engine's 0.0008) and fails by 0.39, while REINFORCE and GRPO break at roughly 12x and 60x. The budget is model-specific, a cheap offline admission check predicts pass/fail, and per-token RL corrections (importance sampling, score centering) do not help OPD. arXiv:2611.11450; code: github.com/benyucong/train-inference-mismatch-opd.

Note: read in full from the capture, main text plus appendix limitations; appendix tables (B-H) were skimmed only via the main-text references.

## Method

- **Mismatch measure:** $d_n=\frac1{N_n}\sum_t[\log q(y_t|y_{<t})-\log p_\theta(y_t|y_{<t})]$ (Eq. 2), an estimate of $\mathrm{KL}(q\Vert p_\theta)$ on engine-visited prefixes, in nats/token; level $D(c)$ = average over steps 1-200. Same scale covers quantization, staleness (q = older weights) and noise.
- **Quality:** held-out KL to the teacher on 530 problems (AIME24 + MATH-500), scored with the standard engine; $\Delta(c)=K(c)/K(0)-1$ (Eq. 3). Fail if $\Delta\ge\tau=0.20$ and the paired bootstrap CI excludes 0 (rule pre-registered). Empirical bracket $B_\text{emp}(\tau)=[\max_{\text{pass}}D,\ \min_{\text{fail}}D]$ (Eq. 4). Accuracy (AIME24/25, AMC23) is a secondary check.
- **Admission check:** candidate engine samples 2 responses on 16 problems; BF16 engine re-scores the same tokens, giving $\hat D(c)$ (Eq. 5). Admit if $\alpha\hat D(c)<L$ with $\alpha=1.5$, $L=0.41$ (so threshold about 0.27). No trainer or teacher needed; 6 configs in 24 min on 1 GPU vs 5.5-6 h on 8 GPUs per full run.
- **Setup:** 200 steps, 8 prompts x 8 responses (DAPO-Math-17k), T=1, 16k tokens, lr $10^{-6}$, verl + vLLM, 2x4 GH200. 17 rollout configs on 7B: 6 quantized (ModelOpt FP8, NVFP4 emulated, vLLM FP8 KV cache; each all-layer or first-layer-KV-in-BF16), 5 staleness (k in {1,2,4,8} versions, colocated), 4 weight-noise ($\sigma\in\{0.0665,0.15,0.234,0.325\}$ x weight std), 2 FP8 + async. Also 1.5B (JustRL teacher) and Llama-3.2-3B students.

## Results

| Result | Number |
|---|---|
| Standard engine mismatch D(0) | 0.0008 nats/token; standard 7B run cuts held-out KL 0.0965 -> 0.0481 |
| Passing configs (12) | D <= 0.184 (>200x D(0)), $\Delta$ in [-5.0%, +6.4%] |
| Failing configs | noise at D~0.39: $\Delta$~+23%; all-layer FP8/KV (D 0.56-0.68): $\Delta$ +54-60%, -3 to -5 acc pts, rollouts almost never correct from step 1 |
| Budget bracket | $B_\text{emp}(0.20)=[0.184,0.39]$; at $\tau=0.25$ it is [0.39,0.56]; no run inside the bracket |
| Staleness | k=8 gives only D=0.0028; throughput saturates at 1.62x (k=4) / 1.59x (k=8), all within 3% of standard KL |
| FP8 first-layer KV in BF16 | vLLM FP8-cache $\hat D$ drops 0.52 -> 0.0037; first layer's KV cache carries 93-99% of FP8-cache mismatch (keys: ~82% of that layer's effect) |
| 1.5B student, all-layer FP8 | D 0.36-0.39 but $\Delta$ +420-479%, about -11 acc pts; BF16 first-layer KV fixes it ($\Delta$=-4.3%) |
| Llama-3.2-3B, all-layer ModelOpt FP8 | D~0.01, passes ($\Delta$=+5.6%) |
| Speed (7B) | ModelOpt FP8 + k=8 reaches sync run's final KL 1.62x sooner (acc 60.5 vs 61.5); FP8 + k=4 reaches 90%-of-gain target 1.69x sooner; FP8 KV cache holds >=1.93x tokens; ModelOpt FP8 1.27x updates/h at train batch |
| Admission check | all 8 preselected decisions match outcomes (estimates <=0.030 or >=0.408); in-training mismatch reached 1.56-1.68x estimate, above the 1.5 margin; noise at 0.39 fails despite sitting under L=0.41 (retro L=0.184 is consistent with all 8) |
| RL under OPD-passing engines | REINFORCE breaks on 3/3 (acc -21, -59, -63 pts); GRPO on 2/3 (noise, NVFP4 entropy collapse, -15 pts); all-layer FP8 breaks everything |
| Offline OPD ([[research/teacher-student-rl/semi-opd-offline-student-rollouts]]-style fixed rollouts) | D=0.082 at steps 100/200, inside the budget |

## Mechanism (Sec. 6)

- **Error vanishes at the teacher:** mismatch adds logit-gradient bias $g^z=\delta\odot A-p_\theta(\delta^\top A)$, $\|g\|_1\le2\|\delta\|_1\|A\|_\infty$ with $A=\log p_T-\log p_\theta$; goes to 0 as student approaches teacher. With a constant reward R (REINFORCE) the error $R\delta$ does not shrink. Expected OPD gradient with fixed engine is exactly that of $\frac12\mathbb E_q[(\log p_\theta-\log p_T)^2]$, so teacher-matching stays stationary (requires advantage computed from trainer log-probs).
- **But the update shrinks faster:** error is 0.11-0.13x its initial size at step 200, error-to-update ratio rises 0.93 -> 1.88, so mismatch matters more late in training.
- **Drift sign is not the story:** shifting advantages by +0.15/+0.5 flips the drift toward the engine yet held-out KL ends 6.5-6.9% lower than standard (unexplained).
- **Per-token corrections do not help:** score centering leaves KL 2.3-3.7% above uncentered OPD; truncated IS raises KL 2.9%/7.0% (steps 100/200). Score centering does fix RL (+61 pts REINFORCE at step 100, +16.5 GRPO at step 200).
- **Prefix shift:** error splits into per-token T and prefix-shift S (engine reaches different prefixes). From passing to failing noise, S grows 5.3x vs T 2.1x; fixing S by response reweighting needs ~$10^{27}$ responses per effective sample, so staying in budget is the only remedy.

## Caveats

- One run per configuration (repeat spread 1.0-1.5% KL); CIs resample problems, not seeds. Some runs used a newer GPU driver.
- Single main student-teacher pair; teacher is an RL-tune of the student (a more distant pair may have a smaller budget). No run lies inside the 0.184-0.39 bracket; 1.5B budget not located; no Qwen3 training result (4B failed the plain-OPD precheck). Math only, reverse-KL single-sample OPD, <=200 steps, NVFP4 emulated.
- Pilot-derived admission settings were insufficient; no prediction tested near the budget edge; staleness limit not located (RL runs also failed the learning test in 200 steps, so RL comparison is under a scaled-down recipe).
- Open: why 0.39 noise fails only by step 200, why positive advantage offsets lower KL.

## Thesis relevance

- Practical constraint for any OPD-style or OPSD-style stage in the pipeline: cheap rollouts (FP8, async) are essentially free if the first-layer KV cache stays BF16 and mismatch is verified per student. Relevant to low-compute single-sample loops, where rollout cost dominates.
- Explains why offline or reused-rollout OPD ([[research/teacher-student-rl/semi-opd-offline-student-rollouts]], [[research/teacher-student-rl/one-shot-opd]]) works: fixed-rollout mismatch (0.082) sits inside the budget. The teacher-anchored objective makes OPD robust where sparse-reward RL ([[research/rlvr-mechanics/deepseekmath-grpo]]) is not, an additional argument for dense teacher signal over outcome reward in small-data regimes.
- Does not bear on what is transferred (pattern vs low-confidence suppression); purely a systems/stability result.

## Source

- `raw/research/weekly-2026-11-13/01-opd-mismatch-tolerance.md` (arXiv:2611.11450, https://arxiv.org/abs/2611.11450; code: https://github.com/benyucong/train-inference-mismatch-opd)

## Related

- [[research/teacher-student-rl/semi-opd-offline-student-rollouts]] — fixed rollouts from initial student; shown here to sit inside the budget
- [[research/teacher-student-rl/one-shot-opd]]
- [[research/teacher-student-rl/ier-gradient-reliability-opd]] — gradient reliability in OPD
- [[research/teacher-student-rl/sequential-opd-then-rl]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]] — reverse-KL OPD vs off-policy
- [[research/teacher-student-rl/reverse-kl-distillation-guarantees]] — stationarity at the teacher
- [[research/teacher-student-rl/mopd-gradient-diagnosis]]
- [[research/teacher-student-rl/opsd-compresses-rlvr]]
- [[research/rlvr-mechanics/deepseekmath-grpo]] — GRPO baseline that breaks at about 60x D(0)
- [[research/teacher-student-rl/_overview]]
- [[../weekly-briefs/2026-11-13]] — brought in by the 2026-11-13 weekly sweep
