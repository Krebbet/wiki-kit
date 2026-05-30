# δ-mem: Online Associative Memory via Delta-Rule State for Frozen LLM Backbones

δ-mem augments a frozen full-attention LLM with a compact fixed-size (r=8) matrix state updated by a gated delta-rule; readout steers backbone attention via dynamic low-rank corrections at inference time. Trained via SFT on QASPER (2,219 samples, 1 epoch) with only 4.87M–19.47M new params (0.12–0.48% of Qwen3-4B), it yields +4.87pp avg across memory-heavy QA benchmarks (TSW config, ×1.10 over frozen baseline), +6.76pp over the strongest non-δ-mem baseline Context2LoRA, and ×1.31 on MemoryAgentBench (MSW). Backbone is never updated; inference GPU memory matches vanilla.

## Method

**Parametric add-on.** Six small projection matrices (W_q^m, W_k^m, W_v^m, W_β, W_q^Δ, W_o^Δ) trained over a frozen Transformer. Backbone seq len kept at 512; memory write budget 8,192 tokens.

**Per-token mechanics.**
1. Project hidden state into r=8 associative-memory space (L2-normed keys, tanh queries).
2. READ: matrix-vector product against S_{t-1} — O(r·d), history-length independent.
3. Corrections: read projected into Δq (query-side) and Δo (output-side), added to frozen backbone's attention query and output ("qo" config).
4. WRITE (gated delta-rule): `S_t = Diag(λ_t)S_{t-1} + Diag(β_t)(v_t^m − S_{t-1}k_t^m)(k_t^m)^T`; β_t and λ_t=1−β_t are data-dependent per-dim gates (error-correction residual write + controlled forgetting).

**Write granularities.**
- TSW: per token.
- SSW: per message/segment (average pooled before write).
- MSW: N=4 parallel sub-states, concatenated at read — reduces interference, costs 4× params (19.47M).

**Objective.** AR cross-entropy over responses only; context compressed into state S_C before backbone sees it.

**Training infra.** 8×A800, DeepSpeed ZeRO-2, 1 epoch on QASPER.

## Results

Primary backbone: Qwen3-4B-Instruct (avg score across eval suite).

| Config | Score | Δ vs frozen |
|--------|-------|-------------|
| Frozen baseline | 46.79 | — |
| TSW | 51.66 | +4.87pp (×1.10) |
| SSW | 51.44 | +4.65pp |
| MSW | 50.74 | +3.95pp |
| Context2LoRA (best prior) | 44.90 | −1.89pp vs frozen |

**Memory-heavy subtasks (MSW/SSW):**
- MemoryAgentBench: 29.54→38.85 (MSW, ×1.31)
- LoCoMo avg: ~40.79→49.12 (MSW, ×1.20)
- LoCoMo TTL subtask: 26.14→50.50 (SSW, ×1.93)
- HotpotQA EM/F1: 42.35/56.00→49.41/63.66 (TSW)

**Other backbones:** Qwen3-8B +3.66pp (SSW); SmolLM3-3B +10.88pp (MSW, ×1.42).

**Context-recovery ablation (state only, no explicit context in input):**
- HotpotQA EM: 0.08→6.48; F1: 8.27→15.20
- LoCoMo avg: 3.49→8.05
Demonstrates the state carries recoverable semantic content.

**Parameter overhead vs alternatives:**
- TSW/SSW: 4.87M (0.12%); MSW: 19.47M (0.48%)
- MemGen: 46.20M; MLP Memory: 3,078M (76.40%)

**Ablations.**
- Head routing: qo default (47.21); qkvo marginally better (48.05) not worth params; output-only (47.05) > query-only (44.51) > key-only (42.19).
- Depth: all-layers best (47.97); middle-12 layers > front-12 or back-12.

## Novelty

Refinement/recombination with a novel coupling mechanism. Not claimed as a wholly new paradigm.

1. **Dynamic low-rank correction:** W_q^Δ and W_o^Δ are fixed projections, but their input is the live-evolving S_{t-1} — same weights produce history-dependent attention steering each step.
2. **Attention-pathway coupling:** LongMem/Memorizing Transformers route memory through a separate retrieval channel; δ-mem routes through attention query and output computation itself.
3. **Error-correction writes in r=8 space** with Qwen-Next/RetNet-derived forget gates, while backbone runs at full model dimension d.

Closest priors: Titans (deep-MLP fast weights, trained from scratch); In-Place TTT (repurposes MLP_down with NTP objective, also drop-in over frozen backbone).

## Reproducibility

No code, weights, or paperswithcode entry cited. Training data (QASPER split, 2,219 samples) is public. Math fully specified in paper. Main reproduction risk: MemoryAgentBench and LoCoMo eval harnesses — MemoryAgentBench is recent (Hu et al. 2025) with limited prior population. No independent reproduction as of capture date.

Preprint only; no citations or leaderboard placement yet.

## Positioning

δ-mem is a third-path long-context entry alongside [[memagent]] and [[sst-v2]] — fixed 8×8 online state + frozen full-attention backbone, neither scaled attention nor recurrent SSM. Closest structural peer is [[in-place-ttt]]: both are drop-in test-time state modifications over a frozen backbone via SFT, but δ-mem routes through attention corrections (new low-rank projections W_q^Δ, W_o^Δ) while in-place-ttt repurposes MLP_down with an NTP objective. Derives associative-memory framing from [[titans-miras]]; classifiable under [[nested-learning]] MIRAS.

Bears on [[conflicts/long-context-attention-vs-recurrent-memory]] (memory-skeptical/hybrid side — fixed-size state shows measurable gains without full attention scaling) and [[conflicts/fixed-state-ssm-long-context]] (extends the "third path" argument: fixed-state additions to full-attention backbones as distinct from pure SSM scaling). Soft scope-tension with [[ssm-tool-use-length-generalization]] Apple Theorem 2.1 — that theorem covers fixed-memory recurrents failing formal length-generalization task classes; δ-mem's gains are on softer memory-heavy QA (LoCoMo, HotpotQA), not tasks requiring strict length-generalization guarantees, so the tension is one of framing rather than direct contradiction.

## Source

`raw/research/weekly-2026-05-18/02-delta-mem.md` (arXiv:2605.12357)

## Related

[[in-place-ttt]] · [[titans-miras]] · [[test-time-training]] · [[nested-learning]] · [[memagent]] · [[sst-v2]] · [[ssm-tool-use-length-generalization]] · [[conflicts/long-context-attention-vs-recurrent-memory]] · [[conflicts/fixed-state-ssm-long-context]]
