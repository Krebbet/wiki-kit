# TriAttention — Trigonometric KV Cache Compression

Training-free, inference-time KV cache compression method that exploits pre-RoPE Q/K vector concentration to score key importance via a closed-form trigonometric series. Matches Full Attention reasoning accuracy at **2.5× throughput** or **10.7× KV-memory reduction**; at a matched KV budget of 1024 on MATH 500, **6.3× speedup** over Full Attention on Qwen3-8B. Mao, Lin, Huang, Xie, Fu, Zhuang, Han, Chen — MIT + NVIDIA + Zhejiang University, arXiv:2604.04921 (Apr 2026).

## Method

Drop-in KV pruning at inference time; no training, fine-tuning, or architecture change. The core observation is that **Q and K vectors in pre-RoPE space are tightly concentrated around fixed non-zero centers** (Mean Resultant Length R > 0.95 for ~90% of heads in Qwen3-8B), stable across token positions, input contexts, and domains. Because pre-RoPE vectors are unaffected by positional rotation, substituting the learned centers into the RoPE attention logit reduces it to a **trigonometric series that depends only on the Q–K distance Δ**. This "distance preference" curve is computed offline per-head via a one-shot calibration (any domain, ~50k–960k tokens).

At inference, each cached key is scored by:
1. **`Strig`** — the trigonometric series evaluated at multiple future offsets `{1, 2, 4, …, 2^16}`, using `E[qf]` as a proxy for future queries.
2. **`Snorm`** — a frequency-band-weighted norm term that activates for heads with low concentration (weighted by `(1 − Rf)`).

`S = Strig + Snorm` is computed per key; for GQA, scores are z-score-normalised per query head and aggregated via **max**. Pruning triggers every β=128 decoded tokens; the top-B keys are retained and the rest evicted.

**Prior art:** builds on SnapKV (observation-window attention scoring), R-KV (recent-query attention + redundancy detection for reasoning), VATP (value-norm importance), and StreamingLLM (sink tokens). The distinguishing move is analysing **pre-RoPE** space (stable directional structure) rather than post-RoPE (polluted by positional rotation), then deriving a **closed-form** scoring function rather than empirically sampling attention.

## Results

Tested on Qwen3-8B, DeepSeek-R1-Distill-Llama-8B, DeepSeek-R1-Distill-Qwen-7B, and GPT-OSS-20B with max generation 32k tokens.

- **AIME25** (Table 1, KV budget 2048, Qwen3-8B): TriAttention **32.9%** vs R-KV 17.5% vs SnapKV 20.0% vs Full Attention 40.8%. At matched Full-Attention accuracy (40.8%), TriAttention achieves **2.5× throughput** (563.5 vs 222.8 tok/s) or **10.7× KV memory reduction**.
- **AIME24** (Table 1, Qwen3-8B): TriAttention **42.1%** vs R-KV 25.4% vs SnapKV 34.6% vs Full Attention 57.1%.
- **MATH 500** (Table 2, KV budget 512, Qwen3-8B): TriAttention **56.0%** vs R-KV 46.4% vs SnapKV 49.2% vs Full Attention 69.6%. At budget 1024, TriAttention 68.4% ≈ Full Attention 69.6%; throughput **1,405 vs 223 tok/s = 6.3× speedup** (Table 4).
- **vs R-KV at comparable accuracy** (Table 5): TriAttention requires **half the KV budget** (1,024 vs 2,048) and **85% higher throughput** (1,405 vs 760 tok/s).
- **Recursive memory retention** (Figure 5D, DFS benchmark, depth 6–20): TriAttention matches Full Attention up to depth 16; R-KV collapses at depth 16 (61% → 31%).
- **Trigonometric series reconstruction** (Figure 3): Pearson `r̄ > 0.5` mean across all heads in Qwen3, Qwen2.5, Llama3; `r̄ = 0.72` for head 0 layer 0.
- **Ablation** (Table 3A): removing `Strig` collapses AIME24 from 42.1% → 18.8%; removing `Snorm` drops AIME24 ~5.4%. **Calibration data domain is irrelevant** (coding vs reasoning: 44.2% vs 42.1% on AIME24).

Hardware: A100 80GB (bfloat16, FlashAttention-2); GPT-OSS on H100 with FlashAttention-3.

## Applicability

Drop-in inference-time KV compression for any **RoPE-based LLM** doing long-context or extended-reasoning generation (chain-of-thought, AIME-class math). Prerequisites:

- RoPE positional encoding — the pre-RoPE concentration phenomenon is tied to RoPE and validated on Qwen3/Qwen2.5/Llama3/MLA (DeepSeek).
- A small calibration dataset (~50k tokens, any domain).
- No retraining, no architecture change, no RL infrastructure.

Enables single-consumer-GPU deployment of models that would OOM under Full Attention at 32k context (the paper demonstrates OpenClaw on one consumer GPU). Offline calibration is cheap; inference overhead is one pruning pass every 128 tokens.

## Novelty

Genuinely new technique in the KV compression landscape. The key discovery — **pre-RoPE Q/K concentration** and its **trigonometric distance-preference interpretation** — is novel. Closest prior work is R-KV (post-RoPE recent-query scoring for reasoning) and SnapKV (observation-window attention scoring). TriAttention's distinguishing change is moving the analysis from post-RoPE (where positional rotation pollutes directional information) to pre-RoPE (stable vectors), then deriving a closed-form scoring function rather than empirically sampling attention. The offline calibration design and GQA normalisation-then-max aggregation are practical novelties.

## Reproducibility

- Code: <https://github.com/WeianMao/triattention>.
- Paper: arXiv:2604.04921 (captured 2026-04-22).
- No paperswithcode entry observed. No released weights (weights-free method — works on any RoPE LLM).
- No independent reproduction at capture time.

## Adoption

Preprint (April 2026); no evidence of independent reproduction, citations, or leaderboard entry visible. Authors validated across four models (Qwen3-8B, DS-Llama-8B, DS-Qwen-7B, GPT-OSS-20B). Code is public. Community uptake unknown at capture time.

## Source

- `raw/research/weekly-2026-04-22/01-triattention.md` — TriAttention paper PDF (arXiv:2604.04921). Captured 2026-04-22.

## Related

- [[in-place-ttt]] — also addresses long-context memory pressure for pretrained LLMs at inference time; In-Place TTT adds fast-weight recurrence to the gated-MLP path, whereas TriAttention prunes the KV cache. Parallel / complementary approaches.
- [[titans-miras]] — Titans uses recurrent memory to sidestep KV cache growth; TriAttention compresses it instead. Contrasting strategies for the same bottleneck.
- [[test-time-training]] — cluster page on TTT-flavoured approaches; TriAttention is a non-TTT inference-time efficiency method, worth linking as a counterpoint.
- [[watchlist]] — SnapKV, R-KV, VATP, StreamingLLM cited as prior art but not captured.
