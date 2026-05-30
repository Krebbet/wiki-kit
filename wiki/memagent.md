# MemAgent: RL-Trained Memory Overwrite for Long Context

ByteDance Seed / Tsinghua AIR (arXiv:2507.02259, ICLR 2026 Oral, July 2025). MemAgent is an agent workflow that reads documents in fixed-size segments and overwrites a 1024-token memory buffer at each step, achieving end-to-end long-context capability without any architectural change to the base LLM. Training via Multi-Conv DAPO — an extension of DAPO to multi-conversation RL rollouts — teaches the model what to keep versus discard across discrete overwrites. Headline result: trained on 8K context (32K documents), RL-MemAgent-14B extrapolates to 3.5M-token QA with <5% accuracy loss; >95% average accuracy on 512K RULER OOD tasks.

## Method

- **Segment-and-overwrite:** document streamed as ~5000-token chunks; each step the model reads `(chunk, previous_memory)` and writes a new 1024-token memory; final answer generated from `(query, memory)` only. Per-step window fixed at 8K (1024 query + ~5000 chunk + 1024 memory + 1024 output).
- **Memory is plain tokens:** memory lives in the standard context window as ordinary readable token sequences — no exotic attention kernels, no architectural modification, no disruption to generation or parallelization.
- **Linear complexity:** `|memory| = M` is constant; each chunk costs `O(C + M)`; end-to-end scales as `O(N)` in document length.
- **Multi-Conv DAPO:** vanilla GRPO cannot handle multiple context-independent conversations per training sample. Authors extend DAPO to `(group, conversation, token)` dimensionality — outcome reward comes from the final conversation; group-normalized advantages are propagated uniformly across all preceding memory-update conversations.
- **RL is load-bearing:** overwrite is non-differentiable, so supervised imitation alone cannot teach compression policy; ablation shows memory-without-RL still degrades with length; the 7B RL model beats a 32B no-RL model.
- **Training regime:** Qwen2.5-7B/14B-Instruct backbone; ~32K synthetic HotpotQA documents at 32K tokens; 8K training context window; no positional re-scaling at inference.

## Results

- **RULER-HotpotQA extrapolation (Table 2):** RL-MemAgent-14B holds ~75–84% accuracy from 7K to 3.5M tokens. All baselines collapse: Qwen2.5-Instruct-14B-1M → 0% at 896K; DS-Distill-Qwen-32B → ~7% at 896K; QwenLong-L1-32B degrades past 60K.
- **OOD RULER tasks at 512K:** MemAgent-14B achieves >95% average accuracy across NIAH variants, variable tracking, frequent-word extraction, and SQuAD QA at 8K–512K — <5% performance loss outside training distribution.
- **RL ablation:** RL training yields near-flat accuracy curves across length; no-RL memory degrades; 7B RL-model outperforms 32B no-RL model.
- **Comparative baselines:** outperforms Qwen2.5-Instruct-1M series, DS-Distill-Qwen series, QwenLong-L1-32B, and truncation baseline — all at similar or larger parameter counts.
- **ICLR 2026 Oral** — peer-reviewed, high-visibility venue.

## Why this matters

MemAgent is a third path in long-context architecture: neither (a) scaled or sparse attention nor (b) recurrent-memory architectural changes (SSMs, linear attention, hybrid layers). Instead, a stock Transformer backbone with a fixed context window handles unbounded context via an RL-trained agent workflow. This directly challenges [[conflicts/fixed-state-ssm-long-context]] Position A's blanket claim that fixed-size state cannot capture rich long-sequence information — MemAgent's 1024-token buffer is a fixed-size state, yet achieves >75% at 3.5M tokens. The crucial differentiator is *learned compression via RL* rather than static gating; this may be the loophole in the Titans argument, worth logging as a Position C in that conflict thread. It also extends [[conflicts/long-context-attention-vs-recurrent-memory]] with a third option: attention-based transformer + fixed window + agent workflow, demonstrating that attention does not need to scale to the full sequence.

Compared to [[ssm-tool-use-length-generalization]], both papers are constructive "third paths" that solve the fixed-state bottleneck without changing the base architecture. They sit on opposite sides: SSM-tool-use leaves the Mamba backbone alone and adds a Turing-tape tool via supervised NTP; MemAgent leaves the Transformer backbone alone and adds a token-space memory overwrite via RL. Together they form a complementary pair — one for recurrent architectures, one for attention architectures — both achieving near-lossless extrapolation from short-context training.

Multi-Conv DAPO is the load-bearing training primitive here, and it joins a growing cluster of GRPO-line credit-assignment fixes: [[token-gradient-cancellation]] fixes within-group token gradient cancellation; [[agentflow]]'s Flow-GRPO broadcasts outcome reward across multi-turn module boundaries; MemAgent's Multi-Conv DAPO broadcasts outcome reward across context-independent multi-conversation rollouts. The same structural trick — broadcast a sparse outcome reward to all latent decisions that contributed — is what unlocks RL training in three different sequential problems this year.

## Reproducibility

- Project page: https://memagent-sialab.github.io/ (BytedTsinghua-SIA lab).
- No separate code repository or model weights confirmed in the source; project page is the primary release artifact.
- Backbone Qwen2.5-7B/14B-Instruct; training on synthetic HotpotQA at ~32K samples; 8K context; reproducible at moderate GPU budget.

## Source

- `raw/research/weekly-2026-05-11/04-memagent.md` — arXiv:2507.02259 (ICLR 2026 Oral).

## Related

- [[conflicts/fixed-state-ssm-long-context]] — MemAgent challenges Position A (fixed-size state can't capture rich long-sequence info); recommend adding a Position C entry.
- [[conflicts/long-context-attention-vs-recurrent-memory]] — MemAgent is the third path between scaled attention and recurrent architectures.
- [[ssm-tool-use-length-generalization]] — complementary constructive theorem on the SSM/recurrent side; both are tool/agent-augmented third paths.
- [[agentflow]] — parallel multi-conv RL framing; Flow-GRPO vs Multi-Conv DAPO as sibling credit-assignment fixes.
- [[token-gradient-cancellation]] — sibling GRPO-credit-assignment fix at the within-trajectory token level.
- [[titans-miras]] — Titans uses gradient-based test-time memorization; MemAgent uses RL-trained token-space overwrite; different mechanisms for the long-context trilemma.
- [[nested-learning]] — Hope reaches 10M context via self-modifying Titans; MemAgent reaches 3.5M via RL memory; different architectural lineages, same scaling goal.
- [[in-place-ttt]] — In-Place TTT extends SSM expressivity via fast-weight TTT; MemAgent's RL memory is a complementary escape route for Transformer backbones.
- [[test-time-training]] — adjacent; both fast-weight TTT and RL-trained memory aim to overcome fixed-context limits.
