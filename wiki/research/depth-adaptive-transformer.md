# Depth-Adaptive Transformer

Elbayad et al. (ICLR 2020; Facebook AI Research / Univ. Grenoble Alpes) equip a Transformer seq2seq decoder with $N$ per-layer output classifiers and a learned halting mechanism that selects, per output token, the layer at which to emit a prediction — trading accuracy for computation along a smooth Pareto frontier. On IWSLT14 De-En the best token-specific configuration (Tok-C geometric-like) matches the $N=6$ baseline at 76% fewer decoder-layer computations (average exit $\approx1.42$); on WMT14 En-Fr, Tok-LL geometric-like matches BLEU 43.4 at $\approx40\%$ of decoder blocks.

## Method core

**Multi-classifier decoder.** Each of the $N$ decoder blocks $\text{block}_n$ has an associated output classifier $C_n$ parameterized by $W_n$:

$$
p(y_{t+1} \mid h_t^n) = \text{softmax}(W_n h_t^n)
$$

At training time all $N$ classifiers are optimized simultaneously. At inference the model selects a single classifier determined by the halting decision for token $t$.

**Halting mechanisms.** Two token-specific designs are evaluated:

- **Multinomial** — a single linear classifier on $h_t^1$ (first-block state) predicts the exit $n$ as a $N$-way softmax; one forward look at the first block determines depth before running deeper.
- **Geometric-like** — a binary halt signal $\chi_t^n = \sigma(w_h^\top h_t^n + b_h)$ is computed after each block; decoding exits when $\chi_t^n > \tau_n$, defaulting to block $N$ if no threshold is crossed. This is a learned sequential decision process.

A sequence-level variant also exists: one multinomial classifier on the mean encoder output chooses a fixed depth for the entire output sequence.

**Training regimes.** Two modes address the inconsistency between exit sequences seen at train vs. test time:

- **Aligned training** (preferred) — all $N$ loss terms evaluated in a single forward pass assuming all prior hidden states are at the current layer. A weighted cross-entropy sum $\mathcal{L}_\text{dec} = -\frac{1}{\sum_n \omega_n}\sum_n \omega_n \text{LL}^n$ with uniform weights $\omega_n=1$ performs best. Missing states at inference are copied up (see below).
- **Mixed training** — $M$ paths of random exit sequences are sampled per sentence; the model is explicitly exposed to cross-layer hidden-state combinations. Slower (requires $M$ passes) and empirically weaker than aligned training, likely because residual connections propagate lower-layer features effectively even without explicit mixed-state training.

**Joint loss.** An exit loss $\mathcal{L}_\text{exit}$ trained via cross-entropy to an oracle distribution $q_t^*$ is combined with the decoding loss:

$$
\mathcal{L}(x, y) = \mathcal{L}_\text{dec}(x, y) + \alpha \mathcal{L}_\text{exit}(x, y)
$$

Two oracle families: **likelihood-based** ($q_t^* = \delta(\arg\max_n \text{LL}_t^n - \lambda n)$, with optional RBF smoothing over neighbouring positions) and **correctness-based** ($q_t^* = \delta(\arg\max_n \tilde{C}_t^n - \lambda n)$, where $\tilde{C}_t^n$ counts correct argmax predictions, smoothed by RBF kernel). The regularization weight $\lambda$ controls the depth–accuracy trade-off; higher $\lambda$ biases toward earlier exits.

## Attention mask solution

**The problem.** Decoder self-attention at time $t$, layer $n$ requires key-value pairs $\{K_s^{n-1}, V_s^{n-1}\}$ for all prior tokens $s < t$. When token $s$ exited at layer $d_s < n$, states $h_s^{n-1}$ were never computed.

**DAT's solution — state copying with per-layer projection.** When token $s$ exits at layer $d_s$, its last computed state $h_s^{d_s}$ is copied to all upper layers:

$$
h_s^k := h_s^{d_s} \quad \forall k > d_s
$$

Then, when block $n$ attends at time $t$, it applies block $n$'s own key and value projection matrices $W_K^n, W_V^n$ to the copied state $h_s^{d_s}$ to produce $K_s^n, V_s^n$. The projection is layer-specific; what is shared across layers is the hidden state vector, not the KV tensors.

At the FLOPs level (see Algorithm 2 in the paper): skipped block $n_s$ for token $s$ still computes $K$ and $V$ from the copied state ($\text{FS} = 4d_d^2$ FLOPs per skipped block) so that future tokens' self-attention can function. This is the minimum overhead required to maintain a coherent KV cache.

**Comparison with the CALM solution.** [[calm]] independently arrives at the same fix: copy $h_s^j$ upward and apply layer $i$'s own $W_K^i, W_V^i$. CALM explicitly ablates copying the already-projected $(K^j, V^j)$ and reports catastrophic degradation (ROUGE-L 23.02 vs 38.24), confirming that re-projection with the current layer's weights is critical — a finding consistent with DAT's design choice.

**Training–inference consistency.** Under *aligned* training the model never sees cross-layer hidden states during training; yet it works at inference because copied states are re-projected through layer-specific weights. Mixed training explicitly exposes the model to these states during training but turns out to be unnecessary given the residual connection structure.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (swappable isolated blocks) | Indirect | Each decoder block must produce a useful output distribution (via $C_n$) independently of upper blocks — a mild form of output-interface pressure. Not a full isolation-training regime; blocks are trained jointly with shared gradients. |
| **G2** (dynamic per-block parameter allocation) | Not applicable | DAT routes in depth at inference; it does not dynamically allocate parameters or expand/contract per-block capacity. |
| **G3** (token-conditional routing) | **Direct — primary reference for depth routing with attention consistency** | Per-token exit is exactly token-conditional routing along the depth axis. DAT is the canonical pre-CALM instantiation of this pattern in autoregressive structured prediction. The attention mask / state-copying solution (§ above) is the reference answer to Experiment 1 Challenge 3. |

## Credibility

ICLR 2020 (peer-reviewed). Four authors: Elbayad (Univ. Grenoble Alpes intern at FAIR), Gu, Grave, Auli (Facebook AI Research). Implemented in fairseq. Code availability: fairseq-integrated; no separate standalone release noted in the paper. Ablations are thorough: two training regimes × five oracle/classifier combinations × two benchmarks (IWSLT14 De-En 160K pairs; WMT14 En-Fr 35.5M pairs). Hyper-parameter ablations for $\lambda$ and $\sigma$ reported. Gradient scaling appendix. WMT14 results show reduced (but nonzero) gains at scale, a realistic caveat.

## Empirical claims

- **IWSLT14 De-En (6 blocks):** Tok-C geometric-like matches $N=6$ baseline (BLEU $\approx34.7$) at average exit AE $=1.42$, corresponding to **76% fewer decoder-layer computations**.
- **IWSLT14 De-En:** Aligned model (no adaptive exit) matches 6-block baseline at fixed exit $n=3$, i.e., half the layers; outperforms per-block baselines at $n=2,\ldots,6$.
- **WMT14 En-Fr (6 blocks, Transformer-big):** Tok-LL geometric-like matches best baseline (BLEU 43.4) at AE $=2.40$ (**40% of decoder blocks**); matches best aligned result (BLEU 43.6) at AE $=3.25$.
- Confidence thresholding (no exit training required, just threshold tuning on valid set) is competitive but incurs large output-classifier FLOPs overhead at large vocab ($V=44$k) — geometric-like classifiers dominate on FLOPs-normalized plots.
- Qualitative: model assigns deeper exits to sequence beginnings, shallower exits near end-of-sequence; low-confidence tokens (top-1 score $<0.5$) consistently exit at higher layers.

## Open questions / failure modes

- **Encoder is not depth-adapted.** The full encoder runs on every input; savings are decoder-only. For encoder-heavy or encoder-decoder-balanced tasks the ceiling is lower.
- **Aligned training mismatch.** Training never sees cross-layer KV combinations; the copy heuristic is not explicitly trained. Mixed training was designed to fix this but underperforms — the explanation (residual connections) is plausible but not mechanistically verified.
- **WMT14 scale attenuation.** Adaptive depth gains shrink on the larger benchmark; sequence-specific methods improve only marginally. The paper does not explain why.
- **Depth routing only.** Token-conditional routing here operates only along depth; no mechanism to route tokens to different parameter pools (FFN experts, distinct block initializations). See [[mod]] and [[sparse-upcycling]] for orthogonal capacity-routing.
- **Autoregressive latency.** Per-token sequential exits are amenable to early stopping in autoregressive decode (one token at a time) but complicate batched GPU inference: variable exit depths across batch items create ragged computation graphs unless padding / speculative execution is used.
- **No block isolation.** Blocks are jointly trained; swapping block $n$ from one model into another is not supported without full retraining.

## Source

- `raw/research/loop-computation/04-depth-adaptive-abs.md`
- `raw/research/loop-computation/12-depth-adaptive-pdf.md`

## Related

- [[calm]] — independent reinvention of the same state-copying fix (2022); adds calibrated confidence thresholds and LTT quality guarantees; operates on encoder-decoder T5 rather than seq2seq NMT.
- [[mod]] — Mixture-of-Depths (2024); routes tokens around entire blocks via top-$k$ selection rather than exiting early; complementary axis of per-token depth routing without the attention-consistency problem.
- [[layerskip]] — training-time counterpart: layer dropout + shared exit head prepare every layer prefix to produce a useful distribution, reducing the training–inference gap that DAT's aligned/mixed training debate targets.
- [[concepts/token-conditional-routing]] — concept anchor; DAT is the earliest autoregressive structured-prediction instantiation.
