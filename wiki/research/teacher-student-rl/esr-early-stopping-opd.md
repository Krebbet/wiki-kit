# ESR: Early Stopping Rollout for On-Policy Distillation

On-Policy Distillation (OPD) assumes the teacher can score the student's trajectory at any position, but this assumption breaks down as the student-generated prefix grows: the teacher is increasingly forced to condition on tokens drawn from an off-policy distribution, causing it to revert from problem-solving to autocompletion — a failure mode the authors call **Off-policy Teacher Decay**. ESR fixes this with a single-line intervention: truncate the student rollout to its first $N$ response tokens and compute the reverse-KL distillation loss only over that prefix. Despite touching no other hyperparameter, this change outperforms full-rollout OPD across tasks (math, code, function calling), training regimes (LoRA, FFT), model scales (students 1.5B–32B, teachers 1.7B–72B), and model families (Qwen2.5, Qwen3, Gemma 2, Gemma 3), while reducing wall-clock cost by up to 24× and peak GPU memory by up to 4×.

## Source

- arXiv: https://arxiv.org/abs/2605.27028
- Capture: `raw/research/weekly-2026-05-30/01-esr-early-stopping-opd.md`
- Authors: Zhou Ziheng, Jiaqi Li, Huacong Tang, Ying Nian Wu, Demetri Terzopoulos (UCLA / BIGAI)

## Method

**Off-policy Teacher Decay (diagnosis).** At position $t$ the teacher scores $\pi_T(\cdot \mid x, y_{<t}^S)$. For small $t$ the conditioning context is close to teacher's own distribution; as $t$ grows the student prefix $y_{<t}^S$ drifts increasingly off-policy to the teacher. Empirical evidence: on MATH-500, teacher avg@4 drops from 65.30% (unconditional) to 62.70% at $N=100$ student tokens and to 51.75% at $N=300$, approaching the student baseline at 50.95%. The teacher is effectively narrating someone else's reasoning rather than correcting it.

**ESR loss.** Standard OPD loss:

$$\mathcal{L}_\text{full} = \mathbb{E}_{y \sim \pi_s}\left[\sum_{t=1}^{T} \text{KL}\!\left(\pi_s(\cdot \mid x, y_{<t}) \;\|\; \pi_t(\cdot \mid x, y_{<t})\right)\right]$$

ESR replaces this with:

$$\mathcal{L}_\text{ESR}(N) = \mathbb{E}_{y \sim \pi_s,\, |y| \leq N}\left[\sum_{t=1}^{|y|} \text{KL}\!\left(\pi_s(\cdot \mid x, y_{<t}) \;\|\; \pi_t(\cdot \mid x, y_{<t})\right)\right]$$

Default $N = 100$ tokens; generation terminates at EOS if reached earlier. For cross-family pairs (different tokenizers), the student rollout is decoded to text and re-encoded under the teacher tokenizer; loss is computed on token-aligned spans via greedy text-span match.

## Key results

**MATH-500 (LoRA, avg@4 / pass@4)** — selected pairs:

| Pair (Student → Teacher) | Student | Teacher | OPD | ESR |
|---|---|---|---|---|
| Qwen2.5-Math-1.5B → Qwen3-1.7B | 50.95 | 65.30 | 62.35 | **65.85 ⋆** |
| Qwen2.5-14B → Qwen3.5-35B-A3B | 73.80 | 83.85 | 5.40 (collapse) | **75.15** |
| Gemma-2 2B → Gemma-3 4B | 13.45 | 66.60 | 22.95 | **27.20** |
| Gemma-2 2B → Qwen3-4B (cross-family) | 13.45 | 77.95 | 16.40 (↓−11.5) | **19.90** |

⋆ = ESR surpasses the teacher reference. Full-rollout OPD collapses (peak < 20% or degrades sharply) in most cross-generation and cross-family pairs; ESR degrades nowhere across the tested grid.

**Efficiency (single A6000, bs=16, Qwen3-1.7B teacher):**

| Metric | OPD | ESR | Gain |
|---|---|---|---|
| Wall time / step | 194 s | 8 s | 24× |
| Peak GPU memory | 63.3 GB | 24.1 GB | 2.6× (4.1× training phase alone) |

The dominant OPD cost is autoregressive generation of ~1000-token sequences (180 s/step); ESR generates only 100 tokens (5 s/step).

**$N$ sensitivity.** On cross-generation Qwen2.5-Math-1.5B → Qwen3-1.7B, ESR is robust for $N \in [50, 200]$; all beat OPD. Cross-family pairs are more sensitive (stable at $N=50$, unstable at $N=100$), consistent with the diagnosis: larger student–teacher gap → faster teacher decay → shorter safe window.

## Analysis: why ESR works

**Cascading Alignment.** Even though training touches only positions $[0, N]$, per-position KL on the *untrained* late positions drops by 30–40% after ESR training. Proposed mechanism: early tokens encode problem framing and strategic planning (case study: first 100 tokens name the unknown and identify the key geometric relationship; last 100 tokens execute algebra). Once the student adopts the teacher's planning style, the execution follows.

**Sub-mode Commitment.** Reverse KL $\text{KL}(\pi_s \| \pi_t)$ is mode-seeking: it penalises student mass outside teacher support but not concentration within it. Full-rollout OPD averages supervision over late "execution" tokens and regresses the student toward the teacher's dominant (verbose) mode. ESR — supervising only the high-KL planning window — lets the student commit to a secondary but higher-quality sub-mode. Empirical signature: ESR-trained student median response length is ~380 tokens vs ~1,530 for full-rollout and ~1,150 for the teacher; the ESR student favours teacher top-2–5 choices over top-1 (47.4% vs 44.6% for OPD), while being more confident in its own choice (top-1 probability 0.79 vs 0.77).

**Position is an independent signal axis.** Selecting the same 100 tokens by top-KL, top-student-entropy, top-teacher-entropy, or their products all underperform ESR and most underperform plain OPD. The top-100 highest-KL tokens account for ~93% of the full-trajectory loss — high-signal tokens are *not* high-quality supervision. Token saliency and token positional utility are orthogonal.

## Relation to concurrent work

Zhang et al. (arXiv:2602.15260) independently report that prefix-supervised OPD is an effective efficiency lever, but in a setting where the student is a *base* model without prior reasoning ability. In that regime, prefix-only OPD does not surpass full-trajectory. ESR is explicitly for students that already reason (instruction-tuned/math-SFT); ESR provides the systematic cross-family/cross-generation matrix, mechanism analysis, and the teacher-ceiling-breaking result not present in Zhang et al.

Li et al. (arXiv:2604.13016, *Rethinking OPD*) note in passing that student prefix degrades teacher signal and that full rollout may not be needed. ESR provides the dedicated mechanism study, naming the "Off-policy Teacher Decay" failure mode and isolating position as an independent axis from KL/entropy. The two papers are consistent: *Rethinking OPD*'s finding that "instability originates at later tokens and propagates backward" is the same phenomenon ESR quantifies and remedies.

## Limitations

- Requires a student that already has basic reasoning ability (instruction-tuned or math-SFT). For base-model students, full-trajectory supervision may be necessary (Zhang et al. finding).
- Evaluated only on small open-source models (<100B); whether the story holds at industrial scale (trillion-parameter models, millions of trajectories) is untested.
- Not evaluated on multi-modal or long-horizon tasks where positional signal-quality patterns may differ.

## Related

- [[_overview]] — teacher-student RL theme overview
- [[rlt-followups-2026]] — OPD landscape; ESR adds a position-based failure-mode diagnosis
- [[mad-opd]] — debate-as-privileged-info approach to breaking the OPD teacher ceiling; ESR breaks the ceiling via sub-mode commitment instead
- [[opsd-compresses-rlvr]] — OPSD as post-RL compaction; ESR addresses the online OPD efficiency problem orthogonally
- [[sakana-rlt]] — dense teacher-side signal; ESR is the efficiency complement
- [[co-evolving-policy-distillation]] — co-evolution approaches vs ESR's truncation approach
- [[../synthesis/proposed-method]] — ESR's 24× efficiency gain makes teacher-in-loop distillation feasible under the project's single-sample budget constraint
- [[../weekly-briefs/2026-05-30]] — brought in by the 2026-05-30 weekly sweep
