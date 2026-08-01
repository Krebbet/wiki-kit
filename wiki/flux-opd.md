# Flux-OPD: On-Policy Distillation with Evolving Contexts

PKU/Kling/Tsinghua/SJTU (arXiv:2607.28022, submitted 30 Jul 2026) propose Flux-OPD, an on-policy distillation (OPD) paradigm for open-ended, non-verifiable-reward tasks that folds context-pool refresh directly into a single training run rather than alternating deploy/train phases. The stabilizing trick is a reverse-KL decomposition of the on-policy context-distillation (OPCD) objective into a geometric-mean distillation target plus a "conflict term" that measures teacher disagreement across contexts; that conflict term is then used, non-heuristically, to scale down correction strength exactly when context-conditioned teachers disagree. On video-generation prompt optimization and medical QA it beats OPD/OPCD/OEL baselines and — unlike OPCD/OEL — never degrades the initial SFT student.

## Method

Extends On-Policy Context Distillation (OPCD [Askell 2021; Ye et al. 2026]) and Online Experiential Learning (OEL [Ye et al. 2026]) by unifying context-evolution and distillation into one loop instead of alternating deploy/train stages.

**Reverse-KL decomposition (Proposition 1).** The OPCD objective E_c[D_KL(p_θ ‖ q_c)] decomposes as:

D_KL(p_θ ‖ q_geo) + (−log Z)

where q_geo is the *normalized geometric mean* of context-conditioned teacher distributions {q_c}, and −log Z ≥ 0 is the conflict term quantifying disagreement among those teacher distributions. Corollary 1: the conflict term is gradient-independent w.r.t. student parameters under a fixed context/history — it's a diagnostic signal, not something the student can optimize away. This mirrors, in reverse-KL form, a prior forward-KL/arithmetic-mean decomposition (Yang et al. 2026).

**Contextual correction.** Distilling directly toward q_geo,k is unstable — it shifts every context-update iteration (this is exactly OEL's failure mode, see below). Instead, Flux-OPD anchors the target to the stable, context-free teacher q0 and injects only the log-space delta:

Δ_k = log q_geo,k − log q0,  q_k^flux = softmax(log q0 + λ_k · Δ_k)

**Contextual weighting.** λ_k = α · clip(1 − δ_k/τ, λ_min, λ_max), where δ_k = −log Z_k is the measured conflict at iteration k. Correction strength drops automatically when context-conditioned teachers disagree — the conflict term derived in Proposition 1 doubles as the modulation signal, rather than an ad hoc schedule.

**Training loop:** K iterations of {extract experience-item contexts from current-student trajectories via the teacher} → {context distillation against the corrected target q_k^flux}. Context pool refreshed every 300 steps. Implementation keeps top-64 (main runs) / top-B target logits, renormalized, standard reverse-KL loss — no reward model, no PPO/GRPO optimizer.

## Results

Three student-teacher pairs: Qwen3-VL-Instruct 4B/8B, Qwen2.5-VL-Instruct 7B/32B, Qwen3 1.7B/8B.

- **Video-generation prompt optimization** (VBench/Video-Bench downstream, Wan2.1-VACE-1.3B & CogVideoX-2B generators): Flux-OPD best "Total" in every configuration. E.g. Video-Bench avg with 8B teacher: Flux-OPD 80.18 vs OPD 79.28, OPCD 79.02, OEL 76.86.
- **Medical QA** (HealthBench, Qwen3 8B→1.7B, Table 2): Flux-OPD 20.61 vs Student 19.06, OPD 19.63, OPCD 19.53, OEL 19.66.
- **Ablation (Table 4)**, isolating each mechanism on medical QA: evolving contexts alone, no correction/weighting (V1) 19.63 ≈ OEL 19.66; contextual correction with fixed best λ=0.7 (V2) 20.03; full Flux-OPD (correction + conflict-derived weighting) 20.61 — the derived weighting adds ~0.6 pp over the best static-λ variant.
- **Stability**: Fig. 5a — OEL shows loss surges / gradient-norm spikes at every context-pool update; Flux-OPD decreases as steadily as vanilla OPD.
- **OOD generalization**: after medical-QA training, Flux-OPD beats OPD on IF-Eval prompt-level strict accuracy (Fig. 5b).
- Critically: naive OPCD and OEL baselines *degrade* the initial SFT student on the prompt-optimization task; only Flux-OPD (and, on medical QA, plain OPD) improve over it.

## Novelty vs prior OPD/self-distillation work

Refinement/recombination, not a new architecture. Builds directly on OPD (Agarwal et al. 2024, ICLR), Context Distillation (Askell 2021), and the companion OPCD/OEL papers (Ye et al. 2026, same lead-author lineage). The two genuinely new contributions: (a) the reverse-KL decomposition itself — geometric-mean target + conflict term (Proposition 1), the reverse-KL analog of a pre-existing forward-KL/arithmetic-mean decomposition; (b) using the derived conflict term (−log Z) as a principled, theory-motivated signal to modulate correction strength, rather than a hand-tuned schedule. Closest prior baseline is OEL, which the authors show fails when naively compressed into one continuous run (Fig. 1b); Flux-OPD's anchor-plus-correction is the fix. Distinct from [[dopd-dual-on-policy-distillation]]'s "privilege illusion" fix (per-token routing by privileged advantage gap) — different failure mode (unstable evolving-context targets vs information-asymmetry token routing), both are OPD refinements, parallel not contradictory. Also methodologically parallel to [[rlsd-self-distilled-rlvr]] (Bayesian evidence-ratio credit weighting) and [[anti-self-distillation]] (PMI-identity-derived JSD correction): all three decompose a KL/PMI-style teacher-student objective and use the derived scalar term to reweight the update, rather than inventing a new loss from scratch. Also adjacent in application space (open-ended task optimization without verifiable rewards) to [[gepa-reflective-prompt-evolution]], which solves the non-verifiable-reward problem via prompt evolution with no weight updates at all — an alternative, orthogonal strategy to Flux-OPD's weight-space distillation.

## Reproducibility

No code/weight release stated in the source. Full training pseudocode (Algorithm 1) and hyperparameters tabulated (Table 7: τ, calibration mode, α, λ bounds per task/model setting) — reproducible from spec, not from released artifacts. Public datasets (VPO 10K SFT prompts, RaR-Medicine ~18K rubric-paired questions) and public benchmarks (VBench, Video-Bench, HealthBench, IF-Eval). Compute: modest — 8× A800 GPUs, batch size 64, lr 2e-6, 10 epochs; standard OPD-style infra (frozen teacher capable of both context-free and context-conditioned inference, student rollout collection, periodic context-pool refresh), no RL infra required. Freshly posted, no external citation/adoption signal yet; co-authored with Kling Team (Kuaishou's video-gen product team), suggesting applied interest in prompt-optimization-for-video-gen as a production use case.

## Source

- `raw/research/weekly-2026-08-01/05-flux-opd.md`

## Related

- [[dopd-dual-on-policy-distillation]]
- [[rlsd-self-distilled-rlvr]]
- [[anti-self-distillation]]
- [[gepa-reflective-prompt-evolution]]
