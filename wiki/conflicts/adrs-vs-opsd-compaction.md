# ADRS vs OPSD-Compresses-RLVR — can privileged self-distillation create new capability, or only compact existing capability?

## Positions

**Position A — OPSD Compresses What RLVR Teaches ([[../research/teacher-student-rl/opsd-compresses-rlvr]]).** On-policy self-distillation (same-model teacher via privileged context) acts as a **safe compaction** of already-correct trajectories, not a correction mechanism. Correct-only OPSD: −29% length, near-zero accuracy change. Incorrect-only OPSD: −7 to −10 pp accuracy. OPSD "cannot create new reasoning states the student's distribution doesn't already support" — it shortens what RLVR already reached, it doesn't extend it.

**Position B — ADRS ([[../research/teacher-student-rl/adrs-self-distilled-reward-shaping]]).** Self-distilled, training-only privileged signal (no external teacher) delivers accuracy/SOTA gains purely from reward shaping: +10.1 pp ALFWorld over the strongest OPD-lineage baseline, and — the sharper claim — **+11.9 pp on ALFWorld's held-out unseen split**, a genuine transfer result rather than a compaction of trajectories the student already produces.

## Resolution rule

*(Open — no ruling yet.)*

This is a **soft** tension, not a direct contradiction, for two reasons the source summary itself flags:

- **Different role in the pipeline.** OPSD is evaluated as a *post-RLVR compaction stage* on top of already-RL-trained math models (SFT → RLVR → OPSD). ADRS is an *in-loop reward-shaping signal* injected directly into RL credit assignment during training (no separate post-hoc compaction stage) on multi-turn agentic tasks. "Does privileged self-distillation add capability" may not be the same question when it's a discrete post-processing step vs. a continuous in-loop advantage term.
- **Different domain and unseen-split semantics.** OPSD's claim is about math reasoning-state support (does the student's own distribution already contain the correct state). ADRS's unseen-split transfer is about ALFWorld task-category generalization (novel task instances within the same environment family, not necessarily reasoning states genuinely outside the base policy's support). The two "does X create new Y" claims may be measuring structurally different notions of novelty.

**What would resolve it:** an ablation that runs ADRS's privileged-rescoring + TVA-gate mechanism as a *post-hoc compaction stage* on an already-RLVR-trained model (OPSD's setting) rather than in-loop, to see whether the transfer gain survives outside the agentic in-loop-credit setting — or, conversely, an OPSD-style correct-only/incorrect-only outcome-filtered ablation of ADRS's own unseen-split gain, to check whether ADRS's +11.9 pp comes from genuinely novel reasoning states or from compaction/selection effects within states the un-shaped GRPO policy could already reach with enough rollouts.

## Source

Surfaced via the 2026-08-21 weekly sweep. ADRS (arXiv:2608.03223) §5.6, Conflict flags in `raw/research/weekly-2026-08-21/.ingest/05-agentic-rl-self-distilled-reward-shaping.summary.md`.

## Related

- [[../research/teacher-student-rl/opsd-compresses-rlvr]] — Position A paper
- [[../research/teacher-student-rl/adrs-self-distilled-reward-shaping]] — Position B paper
- [[../research/teacher-student-rl/rstg-selective-negative-group-distillation]] — also revises what "OPD adds signal" means (recovers signal on negative-zero-variance prompts specifically, a third framing distinct from both compaction and general capability transfer)
- [[../../weekly-briefs/2026-08-21]] — brought in by the 2026-08-21 weekly sweep
