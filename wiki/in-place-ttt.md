# In-Place Test-Time Training

ByteDance Seed + PKU (arXiv:2604.06169, Apr 2026) propose **In-Place TTT**: repurpose the gated-MLP `W_down` projection as fast weights updated at inference via a chunk-wise, NTP-aligned objective, giving pretrained LLMs a "drop-in" continual-adaptation capability **without architecture changes or pretraining-from-scratch**.

## Method

Treats the final projection `W_down` of each gated MLP block as fast weights:

```
O = (φ(H W_gate^T) ⊙ H W_up^T) W_down^T
```

`W_up`, `W_gate` and attention stay frozen. At inference, sequence is split into non-overlapping chunks of size `C` (best 512–1024). For each chunk `i`:

1. **Apply step**: `O_[i] = Z_[i] (W_down^(i))^T`.
2. **Update step**: one gradient descent step on `W_down` using activations `Z_[i]` as keys and an **NTP-aligned target** `V_hat = Conv1D(X_0) W_target` as values, with similarity loss `L = -<·,·>_F`, giving the closed-form update:

```
W_down^(i) = W_down^(i-1) + η · V_hat_[i]^T Z_[i]
```

The Conv1D shifts/mixes future-token embeddings into the target (causally padded at chunk boundaries); fast weights reset at document boundaries. The associative update admits a **parallel scan**, making it Context-Parallel-native.

Builds directly on the prior fast-weights / TTT line: Schlag-Irie-Schmidhuber linear-transformers-as-fast-weight-programmers, Sun et al. TTT-RNN (arXiv:2407.04620), Titans (Behrouz 2501.00663), LaCT "Test-time training done right" (Zhang 2505.23884), DeltaNet, GLA.

**Key novelty vs LaCT/Titans:** in-place on existing MLPs (not a new layer), and NTP-aligned target rather than reconstruction.

## Results

**Drop-in continual training on Qwen3-4B-Base** (~20B tokens @ 32k + ~15B tokens @ 128k, YaRN for RoPE).

**RULER (Table 1)** — baseline vs In-Place TTT:

| Length | Baseline | In-Place TTT |
|---|---|---|
| 64k | 74.3 | **78.7** |
| 128k | 74.8 | **77.0** |
| 256k (extrapolation) | 41.7 | **43.9** |

Short-context essentially flat.

**Generalises (Table 2):**
- LLaMA-3.1-8B: **+2.1 @ 64k**.
- Qwen3-14B-Base: **+2.7 @ 64k**, +1.2 @ 64k+YaRN.

**From-scratch 4B (Table 3, 120B tokens @ 8k context):**
- RULER-16k: **6.58 → 19.99** with Full Attn.
- RULER-8k: **9.91 → 26.80** with SWA.
- Commonsense (HellaSwag/ARC/MMLU/PIQA) roughly neutral or marginally positive.

**500M / 1.5B from-scratch on Pile + Proof-Pile-2** beats SWA, GLA, DeltaNet, and LaCT on sliding-window perplexity up to 32k (Figure 2).

**Ablations (Figure 3, 1.7B):**
- Performance scales with state size (more TTT layers).
- Chunk size 512–1024 optimal.
- Both Conv1D and W_target needed (Conv1D matters more for long context, W_target for short).

**Efficiency (Figure 4):** "negligible overhead" on prefill throughput and peak memory at all context lengths for SWA and Full-Attn 4B configs.

## Applicability

High applicability to anyone doing **long-context post-training on existing open LLMs** (Qwen, LLaMA families demonstrated) — no architecture rewrite, no pretrain-from-scratch, code released.

Prerequisites: continual-training compute (paper used ~35B tokens for the Qwen3-4B run); a long-context corpus; YaRN or similar RoPE extension for >native context; **Context Parallelism support** in the training stack to exploit the parallel-scan implementation.

Also applicable as a from-scratch architectural choice for new LLMs at 500M–4B+ scales. **Orthogonal to attention variants** (works on top of Full Attn., SWA), so could stack with GLA/SSM backbones (left as future work).

## Novelty

Refinement / recombination rather than wholly new paradigm. The TTT framing, fast-weights, and chunk-wise updates all exist (Sun, Titans, LaCT, DeltaNet, RetNet). Two genuinely new pieces:

(a) **Repurposing the existing MLP `W_down` as fast weights** — sidesteps the standard TTT trade-off of needing a new layer that demands pretraining-from-scratch.

(b) **NTP-aligned target** (Conv1D over future-token embeddings × trainable projection) replacing the generic reconstruction `v_t = E_{x_t}` used by prior TTT, with **Theorem 1** (induction-head setting) showing the LM-aligned target raises the correct-next-token logit by `≥ λ_lr · c_norm² · c_align` while reconstruction's effect is bounded by ε.

Closest prior: LaCT (Zhang 2505.23884, "Test-time training done right") which also uses large chunks; In-Place TTT differs by being drop-in on pretrained MLPs and by the NTP target.

## Reproducibility

Code released: <https://github.com/ByteDance-Seed/In-Place-TTT>. Algorithm 1 in Appendix B specifies the CP-parallel-scan algorithm. Training-data composition and hyperparameters detailed in Appendix C.1–C.3. **No released weights.** No paperswithcode entry. Evaluations done with public OpenCompass + RULER + Pile/Proof-Pile-2.

## Adoption

Brand-new (April 2026). ByteDance Seed has institutional weight; the released GitHub repo lowers the barrier. Cites and competes with active 2025 lines (Titans, LaCT, DeltaNet, Lattice, TNT) — sits in a crowded but fast-moving subfield. Watch for: paperswithcode RULER long-context entries, follow-on work combining In-Place TTT with GLA/SSM backbones, third-party reproduction on Qwen/LLaMA.

## Source

- `raw/research/radar-2026-04/09-in-place-ttt.md` — In-Place TTT paper PDF (arXiv:2604.06169). Captured 2026-04-22.

## Related

- [[test-time-training]] — cluster page; In-Place TTT is the current SOTA "drop-in for pretrained LLMs" instance alongside Titans (Memory As Context) and Hope (self-modifying Titans + CMS).
- [[titans-miras]] — earlier Titans framing.
- [[nested-learning]] — Hope architecture (self-modifying Titans + CMS).
- [[watchlist]] — Sun TTT-RNN, LaCT, DeltaNet, GLA, RetNet, YaRN, RULER referenced but not captured.
