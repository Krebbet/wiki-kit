# Test-Time Training (cluster)

Three sources in the radar-2026-04 ingest converge on **online parameter updates during inference** — what the literature calls fast-weights, test-time training (TTT), or test-time memorization. This page links the three and notes the design dimensions where they differ.

## Members

- [[titans-miras]] — Titans (MAC variant) treats a deep-MLP memory module as test-time-memorized state, written via a gradient "surprise" signal. MIRAS recasts virtually all sequence models as associative-memory optimizers parameterized by (memory architecture, attentional bias, retention gate, memory algorithm). Reports beating GPT-4 on BABILong at much smaller scale and >2M context.
- [[nested-learning]] — Hope = self-modifying Titans + Continuum Memory System. Subsumes TTT under "parametric in-context learning" within a Nested Learning framework. Adds multi-frequency MLP chains as the FFN. Holds long-context performance to **10M tokens**.
- [[in-place-ttt]] — Repurposes the gated-MLP `W_down` projection as fast weights with an NTP-aligned target (Conv1D over future-token embeddings × trainable projection). The drop-in story: applies to **pretrained Qwen3 / LLaMA-3.1 without architecture changes**.

## Design dimensions

| Dimension | Titans | Hope (Nested Learning) | In-Place TTT |
|---|---|---|---|
| Fast-weight host | New deep-MLP memory module | Self-modifying Titans block + CMS chain | Existing gated-MLP `W_down` |
| Update objective | Surprise = gradient of memorization loss | Delta Gradient Descent (L2 regression + Sherman-Morrison) | NTP-aligned (Conv1D target) |
| Drop-in vs from-scratch | From scratch | From scratch | **Drop-in on pretrained LLMs** |
| Forgetting mechanism | Adaptive weight-decay gate | Multi-frequency CMS levels | Reset at document boundaries |
| Chunking | Chunk-wise parallel | Chunk-wise dual-form (Sun 2024 / Behrouz 2025c) | Chunk size 512–1024 optimal, parallel scan, CP-native |
| Reported long-context reach | >2M (BABILong) | 10M (BABILong) | 256k extrapolation (RULER) |
| Theory hook | Gradient-as-surprise | Adam = optimal element-wise L2 AM (Theorem in §1.2) | NTP-aligned target raises correct-token logit ≥ λ_lr·c_norm²·c_align (Theorem 1) |

## Tensions across the cluster

- **NL claims TTT is parametric ICL** (i.e., not a distinct paradigm) — see [[conflicts/ttt-distinct-vs-parametric-icl]]. In-Place TTT keeps TTT as a distinct mechanism that *complements* attention rather than replacing it.
- **Hope and Titans require pretraining-from-scratch**; In-Place TTT explicitly targets the drop-in case. The two camps are not adversarial — they answer different operational questions.
- **EGGROLL** sits adjacent (also "non-gradient-via-backprop" updates) but operates at training time, not inference time, and uses ES rather than fast-weight gradient updates. Worth noting because the same constant-state-RNN substrate (RWKV) recurs in EGGROLL's compute argument and in TTT's fast-weight viability.

## Source

This is a cluster/synthesis page; it draws on [[titans-miras]], [[nested-learning]], and [[in-place-ttt]] — see those pages for source captures.

## Related

- [[titans-miras]], [[nested-learning]], [[in-place-ttt]]
- [[eggroll]] — adjacent non-backprop-update line (training-time, not inference-time).
- [[conflicts/ttt-distinct-vs-parametric-icl]]
- [[watchlist]] — Sun et al. TTT-RNN, LaCT, DeltaNet, GLA, RWKV-7, fast-weight programmers (Schlag, Schmidhuber) referenced but not captured.
