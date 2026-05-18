# Conflicts

Open and resolved conflicts between sources. Create one file per conflict; link it here.

## Open

- [[mcpo-vs-dr-grpo-std-fix]] — is removing std normalisation sufficient to eliminate GRPO's difficulty bias, or does a $p(1-p)$ residual survive?
- [[mcpo-vs-dapo-mastered-prompts]] — discard all-correct prompts (DAPO Dynamic Sampling) or retain + regularise with hinge-KL (MCPO)?
- [[knowrl-vs-rlt-hint-design]] — minimal-sufficient atomic hints with no KL (KnowRL) vs maximal-context + plausibility regularisation (RLT)?
- [[invisible-leash-vs-spiral-transfer]] — does Understanding-Self-play's "Invisible Leash" bound (solver only re-weights base-model probability mass) admit SPIRAL's +10.5% game-self-play→reasoning transfer, or is one of the two framings wrong? **Refined 2026-05-01:** Two-Stage Dynamic View provides the bridge — Position A is Stage-1-scoped; Stage 2 admits genuine expansion under entropy preservation. **Sharpened 2026-05-10:** Position A now token-level operationalised by [[../research/rlvr-mechanics/rethinking-rl-sparse-selection]] (0% shifted outside base top-5) and structurally grounded by [[../research/rlvr-mechanics/binary-rewards-rl-challenges]] (forward/reverse-KL asymmetry to $p^*$). Residual gap: SPIRAL's opponent-adaptation vs standard Stage-2 RLVR.
- [[fest-tuned-rl-vs-demonstration-necessity]] — FEST finds tuned-LR pure RL is a formidable baseline (≈ ReLIFT on full 46K), contradicting the implicit demonstration-necessity premise of the single-sample theme; likely a baseline-tuning-rigour artefact — demonstration guidance shifts from "unlocks performance" to "makes the closing delta sample-efficient + stable". **Opened 2026-05-17.**
- [[unified-vs-two-model-self-play]] — R-Zero's Appendix D claims unified-model self-play collapses; AZR / LSP / SQLM / SPICE all successfully train unified-model. Resolution candidate: each working paper has a distinct stabiliser (mode diversity / quality reward / Goldilocks floor / structural asymmetry); R-Zero's reward shape has none. **2026-05-10 update:** [[../research/teacher-student-rl/mad-opd]] adjacent data point — naive multi-teacher (MT-OPD, no debate stabiliser) underperforms single-teacher OPD on code in 4/6 configs; consistent with the editorial reading that stabiliser presence, not architectural multiplicity, is the load-bearing axis.

## Resolved

_(none)_
