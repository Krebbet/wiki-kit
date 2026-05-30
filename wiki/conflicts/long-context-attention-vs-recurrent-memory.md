# Long Context: Attention-at-Scale vs Recurrent-Memory

**Status:** open. Pre-flagged from radar-2026-04 ingest. No counter-source captured yet.

## Position A — Recurrent memory wins at extreme context

**Source:** [[titans-miras]] (Google Research blog).

**Claim:** *"Titans outperforms all baselines, including extremely large models like GPT-4"* on BABILong despite *"many fewer parameters"*, and *"scale[s] effectively to context window sizes larger than 2 million tokens."* Titans (MAC variant) achieves this with a deep-MLP long-term memory module performing test-time memorization driven by a gradient-based "surprise" signal.

**Basis:** "Extreme long-context recall" section of the blog; figure caption "Performance of Titans on extreme long-context reasoning."

[[nested-learning]] extends this with Hope reaching **10M context** on BABILong where Titans/ARMT degrade after 1M.

## Position B — Scale + attention dominates

**No source captured.** Awaiting an ingest of a long-context-attention paper (e.g., Gemini 1.5/2.x long-context, GPT-4-128k+, scaled sparse-attention work) that argues vanilla attention with engineering tricks (RoPE extension, ring attention, etc.) handles extreme context without architectural special-casing.

## Position C — RL-trained explicit memory overwrites (third path, escapes the binary)

**Source:** [[memagent]] (ByteDance Seed / Tsinghua AIR, arXiv:2507.02259, ICLR 2026 Oral).

**Claim:** Neither scaled attention nor recurrent-memory architectural change. Keep a stock Transformer backbone and its standard attention. Instead, train an *agent workflow* via Multi-Conv DAPO that reads documents in fixed-size chunks and overwrites a 1024-token plain-text memory buffer at each step. The memory is ordinary context tokens — no kernel changes, no architectural modification — but the RL outcome reward teaches the model *what to keep*.

**Empirical:** trained at 8K context window, RL-MemAgent-14B extrapolates to **3.5M-token QA with <5% accuracy loss**; **>95% on 512K RULER**. Beats long-context-attention baselines (Qwen2.5-Instruct-14B-1M) at extreme-length retrieval/reasoning at matched backbone.

**Where this sits in the binary:** MemAgent is not Position A (recurrent memory wins) — its memory is plain context tokens, no architectural memory module. It's not Position B (attention wins) — vanilla long-context attention would need 3.5M tokens of KV cache for the same task. The path is *orthogonal*: a learned overwrite policy under outcome reward.

## Position C′ — Hybrid: frozen attention backbone + delta-rule online state

**Source:** [[delta-mem]] (δ-mem, arXiv:2605.12357, May 2026).

**Claim:** Neither pure recurrence (Position A) nor scaled attention (Position B). Keep a **frozen full-attention backbone** and bolt on a compact fixed-size matrix state (8×8 per layer, r=8) updated by a gated delta-rule; its readout steers the frozen backbone's attention via *dynamic low-rank query/output corrections*. Explicitly memory-skeptical of Position B: cites "context rot" (Hong et al. 2025) to argue *"even million-token context windows do not fundamentally solve the memory problem"* — added context length ≠ effective use of it.

**Empirical (Qwen3-4B-Instruct):** avg 46.79 → 51.66 (+4.87 pp, TSW); MemoryAgentBench 29.54 → 38.85 (×1.31, MSW); LoCoMo TTL 26.14 → 50.50 (~×1.93, SSW). 4.87 M new params (0.12%); holds across Qwen3-8B and SmolLM3-3B.

**Where this sits in the binary:** like [[memagent]] it keeps stock attention and adds a fixed-size state, but the state is a *parametric* delta-rule matrix coupled into the attention pathway (not plain context tokens, not an RL-trained overwrite policy). It supplies the memory-skeptical critique the empty Position-B slot was meant to answer — and answers it the other way: scaling attention is *not* the fix.

## Resolution rule when Position B arrives

Capture the strongest version of the attention-side argument. Compare benchmark-by-benchmark on shared evals (BABILong, RULER, NIAH variants) at matched parameter and pretraining-token budgets. Note: Titans' headline "beats GPT-4" claim is **unreplicated** — the source is a blog post, not an independent benchmark.

## Related

- [[titans-miras]], [[nested-learning]], [[test-time-training]], [[delta-mem]], [[memagent]]
- [[conflicts/fixed-state-ssm-long-context]] — adjacent: Titans also rejects the fixed-state SSM stance; δ-mem is a third-path entry there too.
