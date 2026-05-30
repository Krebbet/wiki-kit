# Universal Transformer

Dehghani et al. (2018) propose the Universal Transformer (UT), a recurrent-depth variant of the Transformer that ties weights across all layers and applies a dynamic per-position halting mechanism (Adaptive Computation Time, ACT), achieving Turing-completeness. The model applies the same encoder block — multi-head self-attention followed by a transition function — repeatedly over all positions in parallel, with shared parameters across steps. On algorithmic and language understanding benchmarks it outperforms both standard Transformers and LSTMs at comparable parameter counts, making it the canonical anchoring reference for weight-tied, iterative transformer depth.

## Architecture (weight-tied recurrence)

The core innovation is replacing distinct per-layer weights with a single shared block applied T times. Each recurrent step runs: multi-head self-attention (global dependencies) followed by a transition function (local structure or position-wise FFN), with sinusoidal positional encodings augmented by a step-index encoding to distinguish recurrence depth from sequence position.

The transition function is task-dependent: a depth-wise separable convolution (Chollet 2016) for tasks that benefit from local inductive bias, or a standard position-wise fully-connected layer otherwise. These run in series after attention within each shared step — not as parallel or replacement blocks.

Fixed-T UT is exactly equivalent to a weight-tied multi-layer Transformer. The parameter saving versus depth scaling is the mechanism; generalization is the claimed benefit.

## Adaptive Computation Time (ACT)

ACT makes halting per-position rather than global. At each recurrent step a scalar halt probability is predicted via a sigmoid dense layer applied to each position's current state. Accumulation continues until the cumulative probability exceeds a threshold hyperparameter or a maximum step count is reached. The final step's contribution uses a fractional remainder (soft halting), and the halt predictor is trained end-to-end.

Observed behavior on bAbI: positions corresponding to semantically complex tokens (those tied to more supporting facts) receive more ponder steps — depth is adaptively allocated by input difficulty. Attention distributions start uniform and progressively sharpen onto supporting facts across steps, analogous to iterative reasoning.

ACT does not route tokens to different sub-networks; it allocates depth per token within a single shared block.

## Theoretical results (Turing-completeness)

With sufficient recurrence depth and a suitable transition function, the UT is Turing-complete — unlike the standard fixed-depth Transformer. The weight-tying + ACT combination is the mechanism enabling this: dynamic halting means computation time is not bounded a priori, permitting simulation of arbitrary programs given sufficient memory.

## Scale / benchmarks

All experiments are at base-model scale (comparable to Vaswani et al. 2017 Transformer-base); no validation beyond ~base size is reported.

| Task | UT | Baseline |
|---|---|---|
| WMT14 En-De (BLEU) | 28.9 (base, fixed-T) | Transformer-base 28.0 |
| LAMBADA perplexity | 142 (w/ ACT) | Transformer 7321 |
| LAMBADA RC accuracy | 0.5625 | Transformer 0.0 |
| bAbI avg error (10K, single) | 0.23 | Transformer 15.2 |
| Subject-verb agreement | 99.2% (w/ ACT) | LSTM w/ attn SOTA |
| Algorithmic (Copy seq-acc, len 400) | 0.35 | Neural GPU 1.0 |
| Algorithmic (Addition seq-acc, len 400) | 0.02 | Neural GPU 1.0 |

Algorithmic tasks trained on length 40, tested on length 400 (out-of-distribution generalization). Neural GPU used curriculum training that UT experiments did not.

Dynamic halting outperforms fixed-step UT on LAMBADA even when the fixed model is given more steps (8- or 9-step fixed UT < UT w/ ACT), suggesting ACT acts as a regularizer beyond simply increasing average depth.

ACT marginally degrades MT results; the UT with dynamic halting is not reported for WMT14 in the paper's main MT table.

## Open questions

1. Whether the recurrent inductive bias scales to very large models — all benchmarks are base-scale.
2. Whether better transition functions (beyond separable conv and FFN) yield further gains.
3. Whether ACT's regularization effect persists at larger scale or becomes a bottleneck.
4. The gap between UT and Neural GPU on algorithmic tasks trained without curriculum — recurrence alone is insufficient for perfect algorithmic generalization.

## Source
- `raw/research/thesis-foundations/04-universal-transformers.md` — "Universal Transformers", Dehghani et al., arXiv 2018

## Related
- [[looped-transformers-and-reasoning]] — Latent-Thoughts extends UT with formal expressiveness proofs, 1B-scale reasoning empirics, explicit chain-of-thought equivalence.
- [[looped-language-models]] — Ouro is a direct engineering descendant: same weight-sharing core, replaces ACT with entropy-regularized exit, scales to 7.7T tokens.
- [[looped-vs-depth-scaling]] (open conflict) — whether architectural looping helps at language-modeling perplexity vs. only at reasoning remains contested.
