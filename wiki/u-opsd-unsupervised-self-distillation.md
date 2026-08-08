# U-OPSD: On-Policy Self-Distillation without Any Supervision

UC San Diego / Georgia Tech / UMD / ByteDance (arXiv:2608.06296, Aug 2026). Extends OPSD (Zhao et al. 2026) — which trains teacher and student as the same model under asymmetric contexts, teacher conditioned on a ground-truth solution y*, student seeing only the problem — by removing the ground truth entirely. U-OPSD samples G=8 rollouts per unlabeled prompt from a stop-gradient copy of the policy, takes a plurality vote over boxed final answers to get a pseudo-answer with a self-consistency score, and (when consensus clears a threshold) uses the shortest agreeing rollout as the teacher's privileged context — distilled via forward-KL/generalized-JS divergence into the student along disagreeing rollouts. No gold solutions, external teacher, or RL scalar reward are used; consensus substitutes for ground truth as *dense conditioning context*, not as a reward signal.

## Method

LoRA rank 64, teacher frozen at the initial policy, per-token pointwise clipping, full-vocabulary (or top-k truncated) divergence. Training is skipped when consensus is below threshold (default τ=0.5) or when all rollouts already agree — an implicit curriculum that focuses updates on the model's "competence frontier." Derives from OPD (Gu et al. 2024; Agarwal et al. 2024), OPSD (Zhao et al. 2026), and self-consistency/majority-voting (Wang et al. 2023).

## Results

Evaluated on Qwen3-4B/8B (thinking + non-thinking) and Qwen3-4B-Instruct-2507 / Qwen3-30B-A3B-Instruct-2507 across AIME24, AIME25, HMMT25, MATH500, AMC23. Non-thinking mode: +8.5 pts (Qwen3-4B, 40.96→49.49 avg) and +10.7 pts (Qwen3-8B, 43.57→54.31 avg) over base — beating supervised OPSD by 3.2 and 2.3 pts, and beating GT-supervised SFT/GRPO too. Thinking mode gains are smaller (+1.9–2.2 pts, roughly matching OPSD). Transfers to a 30B MoE without retuning (Qwen3-30B-A3B-Instruct-2507 75.77→77.46 pass@1, beating OPSD by 1.1 pts). Beats label-free baselines (TTRL, RENT, Intuitor) by a wide margin — those improve ≤1.5 pts over base, versus U-OPSD's 7–11 pt gains. Key ablation: full-vocabulary divergence beats sampled-token by 13.7–15.6 pts; disabling consensus filtering entirely (τ=0) actually *beats* the default τ=0.5 threshold — filtering costs more signal than the noise it removes.

## Applicability

Any project with a capable base model (Qwen3-class, 4B–30B tested), unlabeled or weakly-labeled problem sets with only problem statements (no gold solutions), and modest RL/rollout infrastructure (vLLM sampling, G=8 rollouts/prompt, LoRA rank-64, ~150 training steps). Still restricted to domains with parseable/extractable answers (boxed final-answer math here). The core argument — that self-consistency is a far stronger signal as dense teacher-conditioning context than as a scalar reward — generalizes to any RLVR-adjacent post-training setup wanting to drop the reliance on curated GT labels.

## Reproducibility

No code, weights, or repo link found in the captured source; appears to be an arXiv preprint only.

## Related

- [[dopd-dual-on-policy-distillation]] — same problem family (privileged-context OPD); DOPD fixes "privilege illusion" via per-token advantage-gap routing, U-OPSD fixes external-supervision dependence via self-consistency-derived context.
- [[flux-opd]] — parallel OPD refinement (reverse-KL decomposition + conflict term) for non-verifiable-reward tasks; U-OPSD targets verifiable-answer math but removes GT entirely.
- [[anti-self-distillation]] — AntiSD's PMI-identity critique targets a failure mode of default on-policy self-distillation (entropy suppression); U-OPSD's majority-vote teacher construction is a different design point in the same OPSD space.
- [[rlsd-self-distilled-rlvr]] — also decouples direction/magnitude in self-distilled RLVR to fix privileged-info leakage; U-OPSD is a more radical version of the same underlying concern (what info is "allowed" into the teacher context).

## Source

- `raw/research/weekly-2026-08-08/01-on-policy-self-distillation-no-supervision.md` (arXiv:2608.06296)
