# Memory Attention

Jiale Kang (arXiv:2609.28399, Sept 2026). Replaces self-attention's value projection `W_V` entirely with `V = K + Norm(M)`, where `M` is a layer-specific, token-ID-indexed embedding table looked up (not computed) per token — collapsing two learned components (value projection, token embedding) into one additive construction. At matched training-token budgets across MHA/GQA/MQA/gated attention at 373M–2.8B params (10–20B tokens, FineWeb-10BT), MA beats standard attention on perplexity and 7-task zero-shot downstream average, and needs 14–30% fewer tokens to hit matched loss (confounded with MA's larger param count — the authors flag this themselves).

## Method

Standard attention projects hidden states into Q, K, V via three separate linear maps. MA drops `W_V`: values become `V = K_pre-RoPE + Norm(M)`, where `M = Norm(E[s])` is a per-layer learnable table `E ∈ R^(N×d_v)` (N = vocab size) indexed by token ID `s`. Keys supply the contextual component (already computed for attention scoring); the memory table supplies a token-specific, context-independent component. At inference, RMSNorm folds into the table ahead of time, reducing value construction to lookup + add — no matmul.

Two extensions: **MA-Offload** exploits that lookup addresses depend only on token ID/layer index (not hidden states) — the folded tables can live in CPU memory and be prefetched ahead of the layer that needs them, cutting GPU parameter residency. **MA-Recall** (analyzed, not benchmarked) reconstructs historical values on the fly from retained keys + token IDs instead of caching V, trading a persistent value cache for repeated retrieval/reconstruction compute.

Section 3.2 draws a formal connection to MLA: since MLA's K and V are both derived from a shared compressed latent, the value map can be pulled outside the softmax by associativity; MA is framed as reusing K directly (no learned linear value map) plus a token-memory additive term — same functional role, explicitly *not* claimed as an algebraic reformulation of MLA.

Positioned against the "supplement dense compute with lookup capacity" family — Value Embeddings, DeepEmbed, Per-Layer Embeddings (Gemma 3n), STEM, Engram — all of which *add* a lookup term to a still-present dense projection. MA's novelty is removing the dense projection instead.

## Results

- WikiText PPL 31.55→28.64 (MHA-1024); LAMBADA PPL 50.46→43.68 (GQA); downstream zero-shot accuracy +0.71 to +1.16 points across scales, not uniform per task (ARC-Easy/PIQA slightly regress at the larger 2048-hidden scale).
- Single-needle NIAH: MA 97.4%/96.8% at 1K/2K tokens (trained at 2K context) vs. standard 82.6%/82.1%; at 2× extrapolation (4K) MA 41.9% vs. standard 25.9% — both degrade substantially past 2×.
- Training-token efficiency at matched loss: 1.42× (24L/d1024) and 1.16× (24L/d2048) — not isolated from MA's larger parameter count.
- Inference (single H800, BF16, batch 8): MA prefill −3.04% latency, decode +0.86% vs. standard, despite ~2.08× total params. MA-Offload cuts GPU parameter storage 55% below plain MA (and 7% below standard attention's footprint) while matching standard's latency.

## Applicability

Architecture-level change requiring pretraining from scratch — not shown as a retrofit onto existing checkpoints. Validated only at small/mid scale (373M–2.8B params, 10–20B tokens). Good fit for capacity-constrained GPU deployments wanting extra effective parameters without proportional GPU memory, or teams already evaluating embedding/lookup-capacity approaches (DeepEmbed/PLE/Engram-style) wanting a comparison point that *removes* rather than supplements the value projection.

## Reproducibility

Code released: `github.com/Joluck/memory-attention`, built on the open flash-linear-attention framework. No released weights, no PapersWithCode entry, no independent reproduction yet (solo-authored, September 2026 preprint).

## Source

- raw/research/weekly-2026-09-26/01-memory-attention.md
- arXiv: https://arxiv.org/abs/2609.28399

## Related

- [[gated-deltanet-2]] — parallel example of modifying attention's value/update pathway (there: splitting the delta-rule gate; here: replacing `W_V` with lookup+add) rather than the QK/softmax mechanism.
- [[moe-architecture-survey]] — MA's "add capacity via O(1)-per-token lookup instead of proportional dense compute" pitch is the same bottleneck-migration logic the survey traces for MoE, from a non-MoE, non-routed angle.
- [[triattention]] — both target attention/KV-pathway efficiency and report inference-latency/memory tradeoffs alongside accuracy gains.

Note: MA's static, context-independent, token-only memory is a different mechanism from the wiki's recurrent/compressive long-context memory cluster ([[conflicts/long-context-attention-vs-recurrent-memory]], [[conflicts/fixed-state-ssm-long-context]]) — its NIAH gains don't bear on that debate.
