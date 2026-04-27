# SSM-Centric Viewpoint vs Associative-Memory / TTT Taxonomy

**Status:** open. Opened 2026-04-27 from the [[mamba-3]] ingest. Framing-level disagreement between two camps that classify the same models differently.

## Position A — Linear sequence models are best understood as associative-memory optimizers

**Source:** [[nested-learning]] (Behrouz et al. NeurIPS 2025).

**Claim:** The MIRAS taxonomy unifies linear sequence models — Mamba-2, Gated DeltaNet, DeltaNet, RWKV, RetNet, GLA, etc. — as *associative-memory optimizers* with structurally equivalent inner-loop dynamics. [[titans-miras]] presents this as a complete frame: every fast-weight or recurrent update can be re-expressed as an instance of MIRAS' parametric ICL / online-regression formulation.

**Basis:** MIRAS taxonomy as presented in [[titans-miras]] and the Hope / M3 derivations in [[nested-learning]].

## Position B — SSMs are an irreducible viewpoint, not a special case of associative memory

**Source:** [[mamba-3]] (CMU / Princeton / Together AI / Cartesia AI, arXiv:2603.15569).

**Claim (§5.4, paraphrased):** *"Complex values are meaningless as the coefficient of a regression objective; hence, Mamba-3 is not obviously interpretable within [associative memory / TTT] frameworks."* The SSM-centric viewpoint — exponential-trapezoidal discretization, complex state for data-dependent rotary dynamics, MIMO matmul updates — derives design choices the associative-memory frame cannot motivate.

**Basis:** Mamba-3 §5.4. The complex-state innovation (which lets Mamba-3 solve TC⁰-hard state-tracking tasks Mamba-2 cannot) is the load-bearing example: a regression coefficient cannot be complex-valued in a coherent associative-memory interpretation, but a complex SSM transition can be.

## Why this is a conflict, not a vocabulary preference

Position A claims **completeness**: any new linear sequence model should be derivable from / equivalent to a MIRAS instance. Position B exhibits a **counter-example**: a model whose design choice (complex state) has no MIRAS analogue. If Position A is right, the complex-state innovation should be re-expressible; if Position B is right, MIRAS is one frame among several, not a unifier.

Note that this is **distinct from** [[conflicts/fixed-state-ssm-long-context]]. That conflict is about *empirical capacity at long context*; this one is about *which framework is load-bearing for designing new models*.

## Resolution rule

Either:

1. A successor to [[nested-learning]] re-expresses Mamba-3's complex-state dynamics inside MIRAS (resolving in Position A's favour), or
2. Further SSM-side innovations land that are similarly outside the associative-memory frame, hardening Position B.

Both camps should also clarify the scope of their claims — *every* linear sequence model vs *every* sequence model vs *real-valued* sequence models. The literal Mamba-3 §5.4 wording targets associative memory at the *regression-coefficient* level, which is narrower than the full MIRAS frame.

## Related

- [[mamba-3]], [[nested-learning]], [[titans-miras]], [[test-time-training]].
- [[conflicts/icl-emergent-vs-nested-levels]] — adjacent NL-framing dispute (different axis: ICL nature, not SSM compatibility).
- [[conflicts/ttt-distinct-vs-parametric-icl]] — same family of "is X really subsumable under MIRAS?" tensions.
- [[conflicts/fixed-state-ssm-long-context]] — separate empirical conflict on the same SSM line.
- [[watchlist]] — Mamba-2, Gated DeltaNet, S5, LRU, RetNet, MAML, Schmidhuber SRWM.
