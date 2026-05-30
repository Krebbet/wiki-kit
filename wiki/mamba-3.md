# Mamba-3: Improved Sequence Modeling using State Space Principles

CMU / Princeton / Together AI / Cartesia AI (arXiv:2603.15569, ICLR 2026 poster). Mamba-2 successor with three SSM-principled deltas — exponential-trapezoidal discretization, complex-valued state transitions, and MIMO formulation. +1.8 avg accuracy over Mamba-2 at 1.5B; first selective SSM with complex-valued state, solving state-tracking tasks (parity, modular arithmetic) that real-valued SSMs cannot.

## Method

Three changes vs Mamba-2 (Dao & Gu 2024):

1. **Exponential-trapezoidal discretization** — replaces Mamba-1/2's heuristic Euler/ZOH discretization with a second-order trapezoidal rule. The recurrence expands to reveal an implicit two-band convolution on the SSM input, *empirically replacing* the explicit short causal convolution used in prior recurrent models.
2. **Complex-valued state transitions** — the imaginary component implements data-dependent rotary-style embeddings on B and C projections. First selective SSM with complex state; prior complex SSMs (H3, RetNet, Megalodon) were LTI and underperformed Transformers.
3. **MIMO (multi-input, multi-output) SSM** — switches outer-product to matmul state update; α_t, Δ_t, B_t shared across R copies of the hidden state (rank R). 4× decoding FLOPs at fixed state size with no wall-clock decode penalty (better hardware utilization).

Architectural extras: BCNorm (RMS norm on B/C projections replacing post-gate RMSNorm), BC bias terms. Trained on 100B FineWeb-Edu tokens at 2K context, Llama-3.1 tokenizer.

## Results

Zero-shot lm-eval avg, 100B FineWeb-Edu, 1.5B scale (Table 3):

| Model | Avg | FW-Edu ppl |
|---|---|---|
| Transformer-1.5B | 55.4 | — |
| Mamba-2-1.5B | 55.7 | 10.47 |
| GDN-1.5B (Gated DeltaNet) | 55.8 | — |
| **Mamba-3-SISO-1.5B** | **56.4** | **10.35** |
| **Mamba-3-MIMO-1.5B (R=4)** | **57.6** | **10.24** |

- MIMO at state size 64 matches Mamba-2 at state size 128 perplexity (half latency).
- **State-tracking** (Table 5b): Mamba-3 solves Parity and Modular Arithmetic; Mamba-2 and real-valued Mamba-3 ablation score at chance — complex state is load-bearing for TC⁰-hard tasks.
- **Inference** (Table 6, H100 BF16, batch 128): SISO on par with Mamba-2 Triton kernels; MIMO (R=4) ~2× slower than SISO but still faster than Transformer via vLLM.
- **Hybrid** (Table 4): Mamba-3 layers interleaved with attention outperform pure Transformer on retrieval (SWDE, SQuAD, FDA, TriviaQA, NQ, DROP, NIAH).

## Conflict positions

- **[[conflicts/fixed-state-ssm-long-context]]** — partial defence of the SSM camp. Mamba-3 explicitly acknowledges fixed state size causes retrieval weakness ("natural retrieval-based weaknesses of fixed state-size", §4.1.2) and recommends hybrid Mamba-3 + attention. Doesn't refute the [[titans-miras]] / [[nested-learning]] claim that pure fixed-state SSMs degrade at long context — *shifts the battleground to hybrids*.
- **MIRAS / associative-memory framing** (new, see [[conflicts/ssm-vs-associative-memory-taxonomy]]). §5.4 argues *"complex values are meaningless as the coefficient of a regression objective; hence, Mamba-3 is not obviously interpretable within [associative memory / TTT] frameworks"*. Direct framing-level contradiction with [[nested-learning]]'s MIRAS taxonomy that classifies all linear sequence models (incl. Mamba-2) as associative-memory optimizers.

## Reproducibility

Training and inference kernels released at https://github.com/state-spaces/mamba (footnote 1). No pretrained weights or HuggingFace card referenced. From-scratch reproduction needs significant compute (100B-token runs at 1.5B).

## Source

- `raw/research/weekly-2026-04-27/01-mamba-3.md` — arXiv:2603.15569.

## Comparison: Gated DeltaNet-2

[[gated-deltanet-2]] (NVIDIA, arXiv:2605.22791, 2026-05-25) **displaces Mamba-3 as recurrent SOTA at 1.3B.** At matched 1.3B / 100B FineWeb-Edu, GDN-2 beats both Mamba-3 SISO and MIMO on aggregate LM + commonsense (recurrent avg 53.11 vs Mamba-3 MIMO 52.39) and decisively on multi-key retrieval (recurrent MK-NIAH-1 @4K 37.8 vs ≤28.0 for every baseline). Where Mamba-3 *concedes* "natural retrieval-based weaknesses of fixed state-size" (§4.1.2) and shifts the battle to hybrids, GDN-2 argues the weakness is the **update rule**: decoupling Gated DeltaNet/KDA's single scalar gate into channel-wise erase (key-axis) and write (value-axis) gates recovers most of the retrieval gain via the erase gate alone — at fixed state size. See [[conflicts/fixed-state-ssm-long-context]].

## Related

- [[titans-miras]], [[nested-learning]] — MIRAS framing tension; Mamba-3 explicitly positions outside the associative-memory lineage.
- [[gated-deltanet-2]] — beats Mamba-3 SISO/MIMO as recurrent SOTA at 1.3B; attributes the gap to the delta-rule update, not state capacity.
- [[in-place-ttt]] — both improve recurrent/SSM behaviour at deployment; In-Place TTT adapts pretrained Transformers, Mamba-3 is from-scratch SSM.
- [[test-time-training]] — §5.4 contrasts SSM viewpoint vs TTT/linear-attention "associative memory" framing.
- [[conflicts/fixed-state-ssm-long-context]], [[conflicts/ssm-vs-associative-memory-taxonomy]].
- [[watchlist]] — Mamba-2, Gated DeltaNet, S5, LRU, RetNet, Megalodon.
