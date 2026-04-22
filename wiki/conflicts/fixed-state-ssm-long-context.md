# Fixed-State SSMs at Extreme Context

**Status:** open. Pre-flagged from radar-2026-04 ingest. SSM-side source not yet captured.

## Position A — Fixed-size recurrent state cannot capture rich long-sequence information

**Source:** [[titans-miras]] (Google Research blog).

**Claim:** Fixed-size recurrent states (Mamba-2, SSMs) *"cannot adequately capture the rich information in very long sequences."* Hence Titans replaces fixed-size compressed state with a learnable network (deep MLP memory module) trained online via a surprise gradient.

**Basis:** Second paragraph of intro and "Conclusion" section.

[[nested-learning]] extends this — Hope (self-modifying Titans + CMS) holds long-context performance to **10M tokens** on BABILong where fixed-state ARMT and even Titans (without CMS) degrade after 1M.

## Position B — Fixed-state SSMs are sufficient at extreme context (with the right design)

**No source captured.** Awaiting an ingest of a Mamba-2 / state-space-model paper that defends the fixed-state design for long context. Mamba-2 is referenced as a baseline by both Titans and Hope but not captured; primary capture is the next step to make this conflict resolvable.

## Resolution rule when Position B arrives

Compare on shared long-context benchmarks (BABILong, RULER, NIAH variants) at matched parameter budgets and matched pretraining-token budgets. Note Titans' BABILong claims are **unreplicated** (source is a blog, not third-party run).

Worth distinguishing two sub-claims:
- *Information-theoretic*: a fixed-size state has bounded mutual information with arbitrarily long histories. Titans/Hope contest this with a *learnable* (not fixed) state.
- *Empirical*: at the scales we actually train, fixed-state SSMs degrade past some context length. The empirical claim is testable; the information-theoretic claim is a definitional matter.

## Related

- [[titans-miras]], [[nested-learning]], [[test-time-training]]
- [[conflicts/long-context-attention-vs-recurrent-memory]] — adjacent (different opponent).
- [[watchlist]] — Mamba-2, Gated DeltaNet, RWKV-7, RetNet not captured.
