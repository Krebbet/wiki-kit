# AKV — Cache Engineering for Agents

Tsinghua/CUHK (arXiv:2610.28577). Agents `drop` and `repos` (re-rotate) entries of their own active KV cache instead of trimming or summarizing text and re-prefilling, served by AKV, an SGLang-based engine with a drop/reposition-aware radix tree. Claims −27.7% API-equivalent cost and +1.7 avg points vs threshold-triggered summarization over 3 open models × 4 agent benchmarks; code released (thu-nics/AKV). Cache-level alternative to the text-level approach of [[context-language-models]].

## Method
- Ops on the live KV cache, logical trajectory unchanged: `append`; `drop(P)` (exclude KV entries from future attention, retained states/positions untouched); `repos` (RoPE re-rotation of retained keys to contiguous positions, resets the position index so long runs don't hit the limit).
- Cache state is history-dependent: identical tokens can carry different KV under different op sequences, so plain prefix matching is incorrect. Formalised as a cache-operation sequence.
- Serving ("stateless interface, stateful serving"): `messages` plus optional `cache` field describing drops/repositions per request; extended radix tree (drop + reposition nodes, position labels), drop-aware eviction, segment-batch attention to restore history-dependent state in one prefill pass (attention segmented, FFN batched).
- Primary policy: tool-response rolling drop — keep all reasoning KV plus latest K=12 tool responses (motivated by attention analysis: older/tool tokens get less attention). Also explored: cache-management-as-tool (agent decides) and recursive self-improvement of cache policies.
- Lineage: StreamingLLM / H2O / SnapKV eviction ([[triattention]] is a training-free sibling), position-independent caching, RadixAttention.

## Results
- Table 1 (BCP, GAIA-Text, SWE-Verified, xbench-DS; avg score / avg cost ¢, Standard → AKV): MiniMax-M2.7 52.4/5.0 → 53.7/4.4; GPT-OSS-120B 51.0/11.2 → 53.1/7.3; MiroThinker-1.7-Mini 44.1/20.4 → 45.8/14.8. Not uniform per benchmark; no variance reported.
- Serving (GPT-OSS-120B, 80 longest SWE-Verified trajectories, replayed): AKV at concurrency 14 vs Standard peak at 12 — 1.51× P95 latency, 1.18× output throughput; Standard collapses at C≥14 from re-prefill and KV pressure. KV cache reads are 82.4% of API cost.
- Ablation: dropping reasoning KV hurts (SWE 36.5/34.5 vs 41.0); `repos` adds +7 pts BCP by allowing runs past the position limit.
- Cache-as-tool, 100-task BCP: GPT-OSS-120B 61.0 vs 52.1 Standard; MiniMax-M2.7 64.0 vs 56.0 (more turns). RSI-refined policy: −15.6% / −17.8% cost at Standard accuracy (iterations 3/6).

## Caveats
- Self-hosted only (needs attention/KV control); RoPE full-attention models only — linear-attention/SSM support is future work. Retained KV was computed attending to dropped text (train/inference shift handled empirically, no training).
- Cost is API-equivalent estimate from list prices, not measured; serving benchmark is trajectory replay; first-100-task subsets, few seeds.
- Soft tension with [[context-language-models]]: AKV argues text-level edits force re-prefill and criticises CLM's session-local suffix-cache buffers. Overlaps [[neural-garbage-collection]] (learned eviction vs hand/RSI policy).

## Source
- raw/research/weekly-2026-10-24/01-akv-cache-engineering.md (arXiv:2610.28577; code github.com/thu-nics/AKV)

## Related
- [[context-language-models]] — text-level context self-editing; direct competitor
- [[neural-garbage-collection]] — RL-trained KV eviction
- [[triattention]] — training-free KV compression
- [[latentpress]] — long-context compression for agents
- [[polar-rl-harness]] — prefix-merging / cache-correctness in agentic RL
- [[macaron-v1]] — own-view reconstruction for prefix-cache reuse
- [[memagent]] — long-horizon context management
- [[self-evolving-agent-harness]] — RSI of policies parallels cache-policy RSI
- [[deepseek-v4]] — architectural KV cost reduction
