# Test-Time Training: Distinct Paradigm vs Parametric In-Context Learning

**Status:** open. Internal tension within radar-2026-04 cluster (NL vs In-Place TTT framings).

## Position A — TTT is just parametric ICL

**Source:** [[nested-learning]] (Behrouz et al., NeurIPS 2025).

**Claim:** *"Test-time training and test-time memorization are in fact instances of parametric in-context learning."* The train/test boundary is an artifact of how we organize training, not a meaningful mechanistic distinction.

**Basis:** Section 6, "Test Time Training/Memorization are Instances of In-Context Learning" callout box.

This collapses the TTT-vs-ICL distinction into a single mechanism viewed at different "knowledge transfer" levels in the Nested Learning hierarchy.

## Position B — TTT is mechanistically distinct from ICL

**Source:** [[in-place-ttt]] (ByteDance / PKU, arXiv:2604.06169).

**Claim (implicit):** TTT is a distinct mechanism that *complements* attention rather than replacing it. The paper repurposes the existing MLP `W_down` as fast weights with an NTP-aligned target, keeping attention untouched.

**Basis:** The architectural design (TTT as a parallel mechanism on top of attention, not a substitute) and ablation results showing both Conv1D and W_target are needed in addition to attention.

Earlier TTT work (Sun et al. 2407.04620; Titans-MAC) also treats TTT as a distinct module rather than a level of an emergent ICL hierarchy.

## Tension

NL frames TTT as a consequence of having multiple update-frequency levels. In-Place TTT shows TTT contributing on top of attention with a different objective (NTP-aligned vs reconstruction) and produces measurable RULER gains that don't obviously correspond to "another ICL level" in NL terms. The two camps are not strictly contradictory — NL is a *reframing* — but they make different operational predictions:
- NL: rich enough nested-level structure ⇒ ICL covers what TTT does.
- In-Place TTT: even with attention's ICL capacity, an *additional* fast-weight mechanism with an LM-aligned target adds measurable long-context performance.

## Resolution rule

Compare matched architectures: a Hope-style nested-level model with no explicit fast-weights vs the same model with In-Place TTT's `W_down` mechanism added. If In-Place TTT adds nothing on top of Hope's nested levels, NL wins. If it adds long-context performance, the "TTT is distinct" position survives.

## Related

- [[test-time-training]] — cluster page comparing the three TTT-flavoured sources.
- [[nested-learning]], [[in-place-ttt]], [[titans-miras]]
- [[conflicts/icl-emergent-vs-nested-levels]] — adjacent NL claim.
