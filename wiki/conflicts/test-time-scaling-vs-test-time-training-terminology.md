# "Test-Time Scaling" vs "Test-Time Training": Terminology Scope Clash

**Status:** open (terminology/scope, not a factual dispute). Flagged by [[test-time-scaling-taxonomy]] (weekly-brief 2026-08-22).

## Position A — "test-time scaling" means budgeted inference over a fixed model

**Source:** [[test-time-scaling-taxonomy]] (Hariri et al., Case Western Reserve, arXiv:2608.04001).

**Claim:** "Test-time scaling is most naturally viewed as a family of budgeted inference algorithms built atop a fixed autoregressive model" (Section 2.1) — weight/persistent-state updates are explicitly out of scope. Single-trajectory, leaf-level, and prefix-level regimes are all defined with `p_θ` held fixed throughout.

**Basis:** Section 2.1's formal definition, cited alongside Welleck et al. 2024, Snell et al. 2025, Muennighoff et al. 2025, Wu et al. 2024 as sharing this fixed-model framing.

## Position B — existing wiki usage of "test-time" language spans training/adaptation too

**Sources:** [[tempo-test-time-rl]] (TEMPO, arXiv:2604.19295) and the [[test-time-training]] cluster (Titans, Hope, In-Place TTT).

**Claim:** TEMPO titles itself "Scaling Test-Time Training for Large Reasoning Models" and performs EM-style critic recalibration with gradient updates at test time — a weight-update mechanism. The [[test-time-training]] cluster page groups architectures whose test-time behavior is defined by updating fast weights or persistent memory. Both use "test-time" language for mechanisms that Position A's taxonomy would classify as *training*, not *scaling*.

## Tension

Not a factual contradiction — no source disputes another's numbers or claims. The tension is purely terminological: "test-time scaling" and "test-time training" name adjacent but distinct axes (fixed-model budgeted inference vs weight/state updates at inference), and this wiki's existing pages don't consistently draw that line before this ingest. A reader skimming both clusters could easily conflate "TEMPO scales test-time training" with the fixed-model TTS regime this taxonomy defines — they are not the same thing.

## Resolution rule

No empirical test resolves a naming convention. Adopt the taxonomy's distinction wiki-wide going forward:
- **Test-time scaling (TTS)** — fixed base model, budget spent on samples/search/reduction ([[test-time-scaling-taxonomy]], and any future BoN/search/stopping-rule ingests).
- **Test-time training (TTT)** — weight or persistent-state updates during/after inference ([[test-time-training]] cluster, [[tempo-test-time-rl]]).
Future ingests should classify against this split explicitly rather than trusting a source's own self-applied label (TEMPO's title is the cautionary example).

## Related

- [[test-time-scaling-taxonomy]] — source of Position A; also carries a `## Scope note: scaling vs training` section spelling out this same distinction.
- [[test-time-training]], [[tempo-test-time-rl]] — Position B pages.
- [[conflicts/ttt-distinct-vs-parametric-icl]] — adjacent but separate tension (whether TTT is mechanistically distinct from ICL, not a naming dispute).
