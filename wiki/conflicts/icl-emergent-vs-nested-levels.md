# In-Context Learning: Emergent Capability vs Direct Consequence of Nested Levels

**Status:** open. Pre-flagged from radar-2026-04 ingest. Standard "ICL-as-emergent" framing not yet captured.

## Position A — ICL is a direct consequence of nested-level structure, not emergent

**Source:** [[nested-learning]] (Behrouz et al., NeurIPS 2025).

**Claim:** *"In-context learning is the characteristic of having multiple nested levels … per se it is not an emergent characteristic but a direct consequence of having multiple levels in the NL representation of the neural learning module."*

**Basis:** Section 6, "In-Context Learning" subsection (around line 847-849 of the captured PDF).

This is part of NL's broader reframing where:
- Architectures and optimizers are unified as nested associative-memory systems.
- "Knowledge transfer between levels" subsumes ICL, MAML, hypernetworks, learned optimizers, and TTT as instances of one mechanism.

## Position B — ICL is an emergent capability of scale (Brown 2020 / Wei 2022)

**No source captured.** The standard framing post-GPT-3: ICL appears as a phase transition with parameter and pretraining-data scale; not predictable from smaller-scale behaviour. Wei et al. 2022 inventorise emergent capabilities; Schaeffer 2023 contests the metric-driven appearance of "emergence."

## Resolution rule when Position B arrives

NL's claim is testable on architectures that *can be configured* at multiple nested-level counts: does ICL strength correlate monotonically with level count at fixed parameter budget? If yes, that's evidence for NL. If ICL is governed by parameter scale at fixed level count, the emergent-capability framing survives.

Note that Schaeffer 2023's "mirage" argument cuts both ways — it questions the *evidence* for emergence as a phase transition, not the underlying mechanism.

## Related

- [[nested-learning]], [[test-time-training]]
- [[conflicts/ttt-distinct-vs-parametric-icl]] — adjacent NL claim that TTT is parametric ICL.
- [[watchlist]] — Brown 2020, Wei 2022, Schaeffer 2023 not captured.
