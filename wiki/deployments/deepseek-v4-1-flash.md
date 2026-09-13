# DeepSeek-V4.1-Flash

DeepSeek AI released DeepSeek-V4.1-Flash on 2026-09-10: an open-weight (MIT license), multimodal Mixture-of-Experts model with a 552B backbone (plus 196B additional "Engram" conditional-memory parameters) and a 1M-token context window, activating 8B parameters per token during prefill and 16B during decode. The release targets long-horizon agent serving specifically — repeated prefills and million-token contexts turn agent serving into an input-heavy, KV-cache-bound workload — and its headline number is a global KV cache footprint of 890 bytes/token, about 1/4 of DeepSeek-V4-Flash and roughly 437x smaller than DeepSeek-V1. Ships with vLLM/SGLang/Transformers support and a public API with low/high/max reasoning tiers. **Collect-but-confirm:** this is a third-party writeup (MarkTechPost), not DeepSeek's own primary channel, and all comparison-benchmark numbers are DeepSeek-self-reported; the open-weight MIT release itself is a strong independent reproducibility signal regardless.

## Architecture: attacking KV-cache size from three angles

**Causal Encoder-Decoder (halves prefill).** The 40-layer backbone splits into a 20-layer causal encoder and 20-layer decoder. Following YOCO, the decoder derives its KV from the final encoder hidden state via per-layer projection weights rather than computing its own global KV — prompt tokens stop at the encoder, nearly halving prefill compute. Sliding-window attention (128-token window) still runs every layer, so decoder SWA state is rebuilt by replaying only the last 128 prompt tokens ("Decoder SWA Bounded Replay").

**Compressed Sparse Attention 2 (CSA2, attacks the layer axis).** Each layer is statically assigned one of three modes: *Full* (computes its own KV, projects indexer K, selects fresh Top-512 indices), *Reindex* (reuses the last Full layer's KV/indexer K but rescores with its own indexer Q), or *Reuse* (reuses both KV and Top-K indices, skipping the indexer entirely). The 18 CSA2 encoder layers use a 2-in-3 compression pattern; the 20 decoder layers use 1-in-5, with a Hierarchical Sparse Indexer letting the Full layer build a candidate pool of up to 16,384 positions for later Reindex layers to score against.

**FP4 KV quantization + tiered storage.** Main KV is quantized to E2M1 (one E4M3 scale per 16 channels, NVFP4-style) via quantization-aware training, nearly halving storage versus V4's FP8 cache. SWA KV is no longer persisted to SSD — it lives in a distributed DRAM pool (10% of host DRAM, minutes-scale TTL) while global KV keeps a guaranteed 72-hour lifetime; on a miss, only 128 tokens are recomputed rather than replaying the full window across every layer. Net effect: single-token decode FLOPs rise only ~25% as context grows from 4K to 1M tokens.

## Training and results

Pre-training: 45T multimodal tokens (7:1 text-to-multimodal), sparse attention trained from scratch at 64K sequence length (no dense warmup), context extended to 1M at 34T tokens. The base model matches DeepSeek-V4-Pro-Base on world knowledge and coding using 1/3 the total and 1/4 the activated parameters. Post-training uses no new algorithms — gains come from large-scale verifiable-agent-task synthesis, RL across heterogeneous scaffolds (Claude Code, Codex, OpenCode, Pi, mini-SWE, DeepSeek Harness), and on-policy distillation from 40+ teachers. Selected max-effort results (DeepSeek-self-reported): Terminal-Bench 2.1 90.6 (vs. Opus-5's 89.1, GPT-5.6 Sol's 88.8); DeepSWE v1.1 74.2 (vs. Opus-5's 74.0); Terminal-Bench 4.0 31.2 (trailing Opus-5's 51.8 and GPT-5.6 Sol's 39.9); GPQA Diamond 90.9 (trailing Opus-5's 93.4).

## Related

- [[patterns/anthropic-context-engineering]] — same "long context strains resources" problem framed from opposite ends of the stack: Anthropic treats it as an attention-budget/curation problem (JIT retrieval, compaction), this source treats it as a hardware/serving problem (HBM/SSD bandwidth, KV bytes/token)
- [[patterns/claude-platform-cost-optimization]] — extends that page's prompt-caching coverage with serving-layer KV-cache compression mechanics (prefill/KV cache, byte-exact prefix requirement) at a level of technical depth that page doesn't cover
- [[patterns/context-folding]] — complementary rather than competing long-horizon mitigations: AgentFold folds context at the agent-policy level (variable-granularity summarization), V4.1-Flash reduces the need for folding by shrinking the underlying KV footprint
- [[patterns/topology-taxonomy]] — candidate mitigation class (model/serving-architecture KV compression) for the cross-cutting long-horizon-context-loss synthesis page, distinct from the harness/agent-layer classes already listed
- [[patterns/openai-gpt-5-6-agentic-primitives]] — parallel frontier-lab bet that some context-cost problems belong at the model-training/architecture layer rather than the harness layer; contrast: open-weight (MIT) vs. closed API-only
- [[evaluation/osworld-v2]] — parallel observation that long-horizon computer-use agents show sharply nonlinear token/cost curves; V4.1-Flash's near-flat decode-FLOPs scaling is a direct architectural response to that curve, though unverified against OSWorld-style benchmarks specifically

## Source

- `raw/research/weekly-2026-09-13/04-04-deepseek-v4-1-flash.md` — captured 2026-09-13 from MarkTechPost, "DeepSeek AI Released DeepSeek-V4.1-Flash..." (2026-09-10). **Third-party writeup**; the open-weight MIT release on Hugging Face is independently verifiable, but comparison-benchmark numbers are DeepSeek-self-reported (collect-but-confirm).
