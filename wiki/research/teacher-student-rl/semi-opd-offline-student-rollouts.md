# Semi-OPD: Distilling on Frozen Initial-Student Rollouts

Semi-OPD (Zhao, Fu, ..., Grover, Molchanov; NVIDIA/UCLA) freezes the student rollouts: sample once from the initial instruction-tuned student, score once with the teacher, and reuse the set for the whole run while recomputing only the student log-probs. It beats standard on-policy distillation (OPD) on 14 of 17 teacher-student pairs (up to +13.6% accuracy, up to 11.4x speedup), and the gain is predicted by the initial top-64 teacher-student token overlap (Pearson $r=-0.73$, $n=17$). Diagnosis: on low-overlap pairs, OPD's evolving rollouts drift off the teacher's distribution, so the teacher signal degrades; frozen short initial-student rollouts trade some student on-policyness for teacher on-policyness.

## Method

Sample $D_0=\{(x_i,y_i)\}$, $y_i\sim\pi_0(\cdot\mid x_i)$ once. Cache $\log\pi_T(y_t\mid s_t)$. Train with the OPD sampled-token objective on the fixed set:

$$\mathcal{L}=\mathbb{E}_{(x,y)\sim D_0}\sum_t -A_t\log\pi_\theta(y_t\mid s_t),\quad A_t=\mathrm{sg}\big[\log\pi_T(y_t\mid s_t)-\log\pi_\theta(y_t\mid s_t)\big]$$

$A_t$ is a per-token reverse-KL "reward", recomputed with the current $\theta$ each step. Rollout generation, teacher scoring, and training run as separate full-cluster phases (no online generation, one teacher pass). Rollouts per prompt are tunable.

## Claims

- 14/17 pairs better than OPD (1.5B-235B; Qwen3, DeepSeek-R1-Distill, Nemotron-Cascade-2; thinking and non-thinking); within 0.1-2.6% on the other 3.
- Table 1 (avg@32, AIME24/25/26 + HMMT Feb26): Qwen3-1.7B <- Qwen3-4B-Inst (overlap 62.5%): Semi-OPD 39.8 vs OPD 26.2, FastOPD 30.7, Lightning OPD 30.0, Relay-OPD 32.7. Qwen3-4B <- 30B-A3B-Inst: 57.4 vs OPD 44.9, FastOPD 52.5, Lightning 52.2, Relay 48.6.
- High-overlap pair (Nemotron-Cascade-2 <- Math-Expert, 89.3%): Semi-OPD 74.1 = OPD 74.1, FastOPD 74.8 best; Semi-OPD still 4.5x faster than OPD.
- Speedups: up to 11.4x vs OPD, 2.7x vs FastOPD, up to 35x vs Relay-OPD.
- Qwen3 thinking-mode pairs: OPD collapses mid-training; Semi-OPD keeps improving. Math-only distillation transfers to HumanEval/HumanEval+.
- Gap to teacher not closed (1.7B student 39.8 vs teacher 47.5).

## Overlap-ratio decision rule

$$\text{Overlap@}K=\mathbb{E}_{t\sim\pi_0\text{ rollouts}}\frac{|\mathrm{Top}K(\pi_0)\cap\mathrm{Top}K(\pi_T)|}{K},\quad K=64$$

(metric from Li et al., *Rethinking OPD*). Low overlap (~60%): use Semi-OPD; gain is large. Overlap above ~70%: gain is near zero; at ~89% OPD (or FastOPD) is competitive or marginally better. No crisp cutoff is given; the fit is moderate ($r=-0.73$), and the diagnostic is computed on initial-student rollouts, so it is prompt/domain dependent. Cheap to run before committing to an OPD variant.

## Mechanism

Effective distillation needs on-policyness w.r.t. both student (anti exposure bias) and teacher (signal quality). OPD maximizes the first and can lose the second on misaligned pairs. Correlational evidence:

- OPD rollouts lengthen and degrade on low-overlap pairs; a rollout cap hurts the low-overlap pair but helps the high-overlap one.
- Fraction of tokens with $p_T>p_S$ (positive reward) is larger under Semi-OPD throughout training.
- Advantage persists under top-$k$ ($k=32$) reverse KL, not only sampled-token.
- Semi-OPD beats distilling on teacher rollouts: student-generated rollouts matter, not just a fixed cache (consistent with reverse KL needing student support).
- Truncating cached traces to the first 1/4, 1/2, 3/4 at fixed token budget slows convergence and lowers accuracy: full-trajectory coverage matters.
- OPD warm-started from Semi-OPD converges to the same level as OPD from scratch under the same rollout cap ("rollout-determined equilibrium"); on the high-overlap pair Semi-OPD -> OPD improves further.

## Limitations

- Needs adequately strong initial rollouts: from a base (non-instruct) student Semi-OPD underperforms OPD.
- SFT on teacher rollouts first (Lightning-OPD recipe) slightly raises overlap but lowers final Semi-OPD performance.
- Math-centric (DAPO-Math train, AIME/HMMT eval, one code transfer check); the equilibrium characterization is left open.
- The explanation is supported by correlational ablations, not causal intervention.
- Some baselines are reported from Relay-OPD's paper (different tuning/infra); speedups are implementation dependent.
- The paper flags that many OPD-variant gains were measured on poorly aligned pairs and may be overstated.

## Thesis relevance

- Not a single-sample paper; the efficiency gain is compute/wall-clock, not data count. It does cite single-example and 1%-token OPD results (see [[one-shot-opd]]).
- Single-sample implication: with a tiny prompt set, a frozen cached rollout set is the natural regime (one generation phase, one teacher pass, many epochs). Overlap@64 gives a cheap pre-check on whether the teacher in the loop is usable at all for a given student. If overlap is low, expect fresh-rollout OPD to degrade even with a single prompt; if high, fresh rollouts add little cost-adjusted value either way.
- The "teacher-student compatibility governs OPD outcomes" framing adds a data point to [[../../conflicts/opsa-vs-opd-pattern-transfer]].
- Weak indirect concept evidence only (math -> code transfer); no compositionality tests.

## Source

- `raw/research/weekly-2026-10-16/02-semi-opd-offline-rollouts.md`
- arXiv:2610.11291

## Related

- [[esr-early-stopping-opd]] — same teacher-decay diagnosis, opposite remedy (truncate vs freeze short initial rollouts); scope tension
- [[one-shot-opd]] — both question OPD's need for fresh data; teacher-alignment determines value
- [[opd-vs-offpolicy-kl-direction]] — rollout freshness not central; reverse KL wants student rollouts
- [[opsa-teacher-free-self-adaptation]] — teacher-preferred-token fraction and the teacher-needed-or-not dispute
- [[gc-opd-group-calibrated]] — teacher-verifier disagreement grows with context length
- [[co-evolving-policy-distillation]] — same top-k overlap metric (kept >0.90 there); Semi-OPD is the low-overlap counterpart
- [[sg-opd]] — alternative fix for OPD signal quality
- [[tgopd-verify-before-distill]] — teacher-reliability gating vs overlap-based method choice
- [[mopd-gradient-diagnosis]] — OPD mechanics diagnostics
- [[ida-opd-entropy-influence]] — OPD-variant gains possibly measured on low-overlap pairs
- [[rlt-followups-2026]] — OPD lineage
- [[../process-reward-models/cliff-first-mistake-credit]] — OPD baseline weakness consistent with low-overlap finding
- [[../../conflicts/opsa-vs-opd-pattern-transfer]]
- [[_overview]] — teacher-student RL theme overview
- [[../weekly-briefs/2026-10-16]] — brought in by the 2026-10-16 weekly sweep
