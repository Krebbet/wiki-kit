# Watchlist

Persistent radar for this wiki. Items flagged by `/weekly-brief` sweeps (or added manually) that are worth tracking but don't yet merit full ingest. Entries live here until promoted to a wiki page (via `/ingest`) or retired.

**Format:** under each section header, one bullet per item: `- <title> — <≤12-word why / status>`. No URLs, no multi-sentence descriptions. The brief reads this as a scannable ledger.

**Lifecycle:** added by the weekly brief (up to 10 per run) or by hand; promoted to full ingest when a theme reaches ≥2 watchlist entries or when the user tags an item as load-bearing; retired silently after 90 days without promotion.

---

## Single-sample RL fine-tuning

- Effective-question ratio measurements beyond GSM8K/MATH — unclear whether 1-shot-RLVR's post-saturation generalisation holds on non-math domains

## Teacher-student RL / dense-teacher-signal

- SDFT (Shenfeld et al., arXiv:2601.19897) — self-distillation for continual learning; surveyed but not ingested
- SDPO (Hübotter et al., arXiv:2601.20802) — self-distillation from textual feedback; surveyed not ingested
- G-OPD / ExOPD (Yang et al., arXiv:2602.12125) — theoretical unification of OPD as dense KL-constrained RL; surveyed not ingested
- HDPO (arXiv:2603.23871) — hybrid distillation policy optimization via privileged self-distillation; mentioned not captured
- Black-Box OPD (Ye, Dong et al., arXiv:2511.10643) — OPD without teacher-logit access

## RL optimisers / GRPO lineage

- λ-GRPO (arXiv:2510.06870) — unifies GRPO/DAPO/Dr. GRPO with learnable token preferences
- Goldilocks RL (arXiv:2602.14868) — teacher-driven data sampling targeting $p \approx 0.5$ difficulty
- Posterior-GRPO (arXiv:2508.05170) — rewarding reasoning processes in code
- DRA-GRPO (arXiv:2505.09655) — diverse reasoning paths for math
- Efficient Reasoning via Reward Model (arXiv:2511.09158)

## Concept learning

- Reversal curse follow-ups (cited by [[research/teacher-student-rl/rlt-followups-2026]] ExGRPO) — generalisation-vs-memorisation line
- Compositional generalisation benchmarks — no captured measurement of whether curriculum-RL methods pass
- RCE follow-ups (Chaudhry 2025) — monitor for extensions

## Catastrophic forgetting / continual learning

- EWC variants applied to RL fine-tuning (not just CPT) — gap from [[research/catastrophic-forgetting/ewc-gemma2-cpt]]
- Per-concept Fisher anchor composition — untested at curriculum scale per [[research/synthesis/concept-curriculum-method]]

## Commercial adoption signals

- Qwen3 post-training recipe — uses GSPO; watch for Qwen3.5 / Qwen4 updates
- MiMo (Xiao et al., 2026) — mentioned as OPD adopter in [[research/teacher-student-rl/rlt-followups-2026]]; unreviewed
- GLM-5 (Zeng et al., 2026) — same

## Architecture adjacent

- Structured Fisher optimiser (RACS, Alice) follow-ups — cited once in [[research/rlvr-mechanics/_overview]]
- Sparse subnetwork discovery methods without a full RL run — open question in [[research/rlvr-mechanics/_overview]]

## Empirical contradictions to resolve

- DPO-vs-RLOO disagreement — [[research/rl-optimizers/dpo]] reports DPO beats PPO-from-checkpoint on HH; [[research/rl-optimizers/rloo]] reports RLOO beats DPO. Close-read pending.

---

## Related

- [[reference-sources]] — what the weekly brief scans
- [[index]] — wiki-wide page catalog
- [[research/synthesis/concept-curriculum-method]] — most recent north star
