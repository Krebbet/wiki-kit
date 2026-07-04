# DOPD: Dual On-Policy Distillation

DOPD (arXiv:2606.30626, NUS/CUHK/PKU/JD) addresses a fundamental failure mode in on-policy distillation (OPD) with privileged information: "privilege illusion," where the apparent teacher-student gap conflates a genuine capability gap with an information asymmetry gap. Instead of uniformly distilling from one privileged teacher, DOPD computes a per-token **privilege advantage gap** A — the log-probability difference between privileged teacher and privileged student under identical inputs — and routes each token to one of four regimes with distinct supervision objectives, strengths, and granularities. On LLM benchmarks (Qwen3-8B→Qwen3-1.7B), DOPD averages 51.4 across 8 benchmarks vs Vanilla OPD 43.9 (+7.5 pp, 89.8% gap recovery), including surpassing the teacher on four hard tasks. On VLM benchmarks it gains +6.0 pp over Vanilla OPD with 69.2% gap recovery; gains are consistent across five teacher-student size pairs and scale favorably where Vanilla OPD collapses (8B→0.6B: +14.1 pp vs +3.5 pp).

## Method

The setup: student generates on-policy rollouts; teacher provides token-level supervision. When privileged inputs (verified hints for LLMs, bounding boxes for VLMs) are added, vanilla OPD suffers privilege illusion — the teacher's advantage partly stems from information it holds but the student can never replicate, causing the student to fit shortcuts rather than acquire transferable ability, and producing entropy collapse.

**Privilege advantage gap.** For each token y_n, compute A = |log Π_T(y_n|x,p,y_<n) − log Π_S(y_n|x,p,y_<n)| where both teacher and student receive the same privileged context p. Large A under controlled privileged conditions implies a real capability gap; small A implies the teacher's edge is informational.

**Four token regimes** (based on A vs batch-average Ā, and q_T, q_S vs their averages):

| Regime | Condition | Interpretation | Objective |
|--------|-----------|---------------|-----------|
| LH | Low A, both high prob | Privileged info bottleneck, not capability | Light teacher: Top-K reverse KL, weight β_l=0.6 |
| LL | Low A, both low prob | Uncertain region, noisy signal | Weak self-anchor: Top-K reverse KL on stop-grad priv. student, weight β_w=0.3 |
| HT | High A, high q_T | Critical capability gap — teacher credibly ahead | Strong teacher: full-vocabulary JS divergence, weight 1.0 |
| HS | High A, high q_S | Student confident, teacher unreliable — preserve exploration | Light self-anchor: Top-K reverse KL on stop-grad priv. student, weight β_l=0.6 |

The privileged student shares parameters with the deployed student but receives p during training; the privileged teacher is frozen. Cost: one extra student forward pass per step.

**Training data:** 32K LLM samples (general/math/code) + 25K VLM samples (ViRL39K); privileged inputs generated and quality-filtered via GPT-5.4.

## Results

**LLM (Qwen3-8B → Qwen3-1.7B):**
- DOPD 51.4 avg (8 benchmarks) vs Vanilla OPD 43.9 (+7.5 pp)
- Outperforms strongest baselines: ExOPD +4.4, Uni-OPD +4.8, EOPD +5.3
- Surpasses teacher policy on AIME25 (23.3 vs 20.2), ZebraLogic (26.9 vs 25.0), C-Eval (71.3 vs 77.1 — not here), BFCLv3 (60.2 vs 60.0), LCBv5 (27.1 vs 23.6)

**VLM (Qwen3-VL-8B → Qwen3-VL-2B):** 58.4 avg vs Vanilla OPD 52.4 (+6.0 pp); beats VA-OPD by 2.1 pp.

**Scalability (5 pairs):** +11.1–14.1 pp across all pairs (2–3× Vanilla OPD improvement); gains scale with teacher-student ratio while Vanilla OPD degrades at large ratios.

**Additional:** Reaches step-200 baseline performance at step-80 (1.5× training efficiency); outperforms second-best OOD generalization by 3.1/4.3 pp; stable entropy trajectory (no collapse observed in self-distillation baselines).

## Source
- arXiv: 2606.30626
- Captured: `raw/research/weekly-2026-07-04/04-dopd-dual-on-policy-distillation.md`

## Related
- [[rlsd-self-distilled-rlvr]] — self-distillation for RLVR with privileged-info leakage fix (complementary, different mechanism)
- [[anti-self-distillation]] — entropy suppression in naive on-policy self-distillation; different root cause (PMI identity) but compatible critique
- [[delta-token-credit]] — per-token discriminative reweighting in GRPO; token-level differentiation in RL (parallel to DOPD's token routing in distillation)
- [[token-gradient-cancellation]] — gradient cancellation as bottleneck; per-token stop-gradient transforms
- [[high-entropy-tokens-rlvr]] — ~20% high-entropy forking tokens carry disproportionate learning signal; parallel finding to DOPD's high-advantage-gap token importance
- [[thought-anchors]] — causally load-bearing tokens in CoT; behavioral corroboration of token non-uniformity
- [[rl-teachers]] — teacher models optimized for student comprehension rather than own performance
