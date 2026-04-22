# Long Context: Attention-at-Scale vs Recurrent-Memory

**Status:** open. Pre-flagged from radar-2026-04 ingest. No counter-source captured yet.

## Position A — Recurrent memory wins at extreme context

**Source:** [[titans-miras]] (Google Research blog).

**Claim:** *"Titans outperforms all baselines, including extremely large models like GPT-4"* on BABILong despite *"many fewer parameters"*, and *"scale[s] effectively to context window sizes larger than 2 million tokens."* Titans (MAC variant) achieves this with a deep-MLP long-term memory module performing test-time memorization driven by a gradient-based "surprise" signal.

**Basis:** "Extreme long-context recall" section of the blog; figure caption "Performance of Titans on extreme long-context reasoning."

[[nested-learning]] extends this with Hope reaching **10M context** on BABILong where Titans/ARMT degrade after 1M.

## Position B — Scale + attention dominates

**No source captured.** Awaiting an ingest of a long-context-attention paper (e.g., Gemini 1.5/2.x long-context, GPT-4-128k+, scaled sparse-attention work) that argues vanilla attention with engineering tricks (RoPE extension, ring attention, etc.) handles extreme context without architectural special-casing.

## Resolution rule when Position B arrives

Capture the strongest version of the attention-side argument. Compare benchmark-by-benchmark on shared evals (BABILong, RULER, NIAH variants) at matched parameter and pretraining-token budgets. Note: Titans' headline "beats GPT-4" claim is **unreplicated** — the source is a blog post, not an independent benchmark.

## Related

- [[titans-miras]], [[nested-learning]], [[test-time-training]]
- [[conflicts/fixed-state-ssm-long-context]] — adjacent: Titans also rejects the fixed-state SSM stance.
