# OPSA vs OPD-Dual-Nature — does OPD transfer teacher-specific patterns, or just suppress the student's own low-confidence tokens?

## Positions

**Position A — OPSA ([[../research/teacher-student-rl/opsa-teacher-free-self-adaptation]]).** OPD's empirical gains come from suppressing low-log-probability tokens sampled by the student itself — an operation requiring no teacher at all. Training on noisy-only or fully teacher-free (single fixed negative advantage) supervision matches standard OPD performance; high-logp tokens, where student and teacher content would actually differ, contribute no learning signal even with random advantages assigned to them. The paper's own "Takeaway": "OPD gains may arise not from distilling teacher knowledge, but from suppressing low-probability tokens sampled by the student itself, an operation that requires no teacher at all."

**Position B — OPD-Dual-Nature ([[../research/teacher-student-rl/opd-dual-nature-generalization]]).** OPD transfers the teacher's reasoning *patterns*, not answers to particular problems (Sec 3.1). The evidence is a same-origin vs cross-origin dissociation: same-origin teacher-student pairs (shared base checkpoint) generalize broadly across language, reasoning horizon, and domain; cross-origin pairs stay narrowly fit to the training distribution, and higher cross-origin teacher competence does not improve transfer. Top-K next-token overlap between teacher and student rises over training for same-origin pairs but stays flat for cross-origin pairs (Fig. 6) — offered as mechanistic evidence that same-origin OPD pulls the student toward whole-policy agreement with the *specific* teacher, not just toward any distributional sharpening. This dissociation only makes sense if the teacher's specific behavioral content (hence its identity/origin) is actually what's being transferred.

## Resolution rule

*(Open — no ruling yet.)*

This is a direct, not merely soft, tension: Position A's mechanism (advantage mass concentrates on student-low-logp tokens; teacher identity/noise barely matters) predicts that *which* teacher supplies the advantage sign should matter little beyond producing roughly the right sign on roughly the right tokens — it does not obviously predict a same-origin/cross-origin generalization split, since a teacher-free fixed advantage on the same token selection reproduces OPD's gains in Position A's own experiments. Conversely, Position B's mechanism requires the *specific* teacher's whole-policy identity to be what's being absorbed, which is difficult to reconcile with Position A's finding that teacher supervision noise (up to 97.8% mis-signed tokens for a 235B teacher) barely changes final performance.

Two threads worth separating before either position is dismissed:
- **Different measurement targets.** Position A's noise-insensitivity result is measured on in-distribution math accuracy (AIME24 etc.) after training on a single teacher's noisy vs. clean supervision. Position B's central evidence is *out-of-distribution transfer* (cross-language, cross-horizon, cross-domain) between teacher-swapped pairs, not accuracy on the training distribution. It is possible that near-teacher-invariant, low-logp-suppression-driven gains dominate the training-distribution numbers (explaining Position A's noise-insensitivity) while a smaller, teacher-identity-dependent whole-policy-alignment effect exists underneath and only shows up in Position B's OOD transfer probes — i.e., the two papers may be measuring different slices of the same phenomenon rather than contradicting each other outright.
- **Confound in Position B's origin manipulation.** Same-origin vs cross-origin pairs necessarily differ in more than "teacher identity" — they differ in base-checkpoint compatibility, tokenizer/architecture match, and (per Position A's finding) potentially in how noisy/well-calibrated the teacher's advantage signal is against that particular student's own token distribution. Position B does not run Position A's noisy/teacher-free ablations within its same-origin vs cross-origin design, so it cannot currently rule out that the same-origin advantage is itself a token-selection/calibration artifact rather than genuine whole-policy content transfer.

**What would resolve it:** run Position A's diagnostics (noisy-only vs clean-only vs teacher-free fixed-advantage training; high-logp-token ablation) separately for same-origin and cross-origin teacher-student pairs from Position B's setup. If teacher-free fixed-advantage training reproduces cross-origin OOD transfer as well as same-origin OOD transfer, Position B's origin-dependent generalization claim would not survive — the effect would reduce to token-selection dynamics that happen to correlate with origin. If teacher-free training reproduces same-origin transfer but *not* cross-origin transfer (i.e., the origin gap persists even with no real teacher influence beyond sign/selection), that would indicate a genuine teacher-identity-dependent component Position A's diagnosis does not capture.

## Source

Surfaced via the 2026-09-04 weekly sweep. OPSA (arXiv:2608.31046), Sections 2.2–2.3, 3.1–3.2, in `raw/research/weekly-2026-09-04/.ingest/01-opsa-does-opd-really-distill.summary.md`.

## Related

- [[../research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — Position A paper
- [[../research/teacher-student-rl/opd-dual-nature-generalization]] — Position B paper
- [[../research/teacher-student-rl/opdvr-verifiable-reward]] — related OPD-noise diagnosis, sides with calibrating-not-removing the teacher
- [[../research/teacher-student-rl/gc-opd-group-calibrated]] — related OPD-noise diagnosis, sides with calibrating-not-removing the teacher
- [[../../weekly-briefs/2026-09-04]] — brought in by the 2026-09-04 weekly sweep
