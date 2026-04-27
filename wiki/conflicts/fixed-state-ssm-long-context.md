# Fixed-State SSMs at Extreme Context

**Status:** open. Pre-flagged from radar-2026-04 ingest. SSM-side source not yet captured.

## Position A — Fixed-size recurrent state cannot capture rich long-sequence information

**Source:** [[titans-miras]] (Google Research blog).

**Claim:** Fixed-size recurrent states (Mamba-2, SSMs) *"cannot adequately capture the rich information in very long sequences."* Hence Titans replaces fixed-size compressed state with a learnable network (deep MLP memory module) trained online via a surprise gradient.

**Basis:** Second paragraph of intro and "Conclusion" section.

[[nested-learning]] extends this — Hope (self-modifying Titans + CMS) holds long-context performance to **10M tokens** on BABILong where fixed-state ARMT and even Titans (without CMS) degrade after 1M.

## Position B — Fixed-state SSMs are sufficient at extreme context (with the right design)

### B (partial, hybrid-only) — [[mamba-3]] (CMU/Princeton/Together/Cartesia, arXiv:2603.15569, 2026-04-27)

**Claim (partial defence):** Mamba-3 *concedes* the retrieval weakness of pure fixed-state SSMs — explicit acknowledgement of *"natural retrieval-based weaknesses of fixed state-size"* (§4.1.2) — and **shifts the battleground to hybrids**. Mamba-3 layers interleaved with attention match or exceed pure-Transformer baselines on retrieval (Table 4: SWDE / SQuAD / FDA / TriviaQA / NQ / DROP / NIAH).

This is *not* a defence of pure fixed-state SSMs against Position A. It is a partial Position-B variant: "fixed-state SSMs are sufficient *if* paired with attention layers". Pure-Mamba-3 still degrades at retrieval-heavy long context.

### B (orthodox) — still no source

Awaiting an ingest of a Mamba-2 / state-space-model paper that defends the *pure* fixed-state design for long context against [[titans-miras]] / [[nested-learning]]'s Position A.

## Resolution rule when Position B arrives

Compare on shared long-context benchmarks (BABILong, RULER, NIAH variants) at matched parameter budgets and matched pretraining-token budgets. Note Titans' BABILong claims are **unreplicated** (source is a blog, not third-party run).

Worth distinguishing two sub-claims:
- *Information-theoretic*: a fixed-size state has bounded mutual information with arbitrarily long histories. Titans/Hope contest this with a *learnable* (not fixed) state.
- *Empirical*: at the scales we actually train, fixed-state SSMs degrade past some context length. The empirical claim is testable; the information-theoretic claim is a definitional matter.

## Related

- [[titans-miras]], [[nested-learning]], [[mamba-3]], [[test-time-training]]
- [[conflicts/long-context-attention-vs-recurrent-memory]] — adjacent (different opponent).
- [[conflicts/ssm-vs-associative-memory-taxonomy]] — separate Mamba-3-driven framing tension with [[nested-learning]].
- [[watchlist]] — Mamba-2, Gated DeltaNet, RWKV-7, RetNet not captured.
