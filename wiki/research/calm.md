# Confident Adaptive Language Modeling (CALM)

CALM (Schuster et al., NeurIPS 2022; Google Research / MIT CSAIL) is a framework for **per-token early exit** in autoregressive Transformer decoding. Rather than running every generated token through all $L$ decoder layers, CALM exits at the earliest layer $i$ for which a local confidence score $c_t^i$ exceeds a calibrated threshold $\lambda_t^i$, provably bounding degradation versus the full model via the Learn then Test (LTT) framework. On T5 8-layer across summarization, translation, and QA benchmarks, softmax-based confidence achieves up to ×3 speedup with guaranteed quality preservation; oracle experiments show the theoretical ceiling at ×5.2 FLOPs reduction on CNN/DM.

## Method core

**Early-exit decision rule.** At each decoding step $t$, the next token is predicted from the shallowest layer meeting threshold:

$$
y_{t+1} := \begin{cases}
\arg\max\, p(y_{t+1} \mid d_t^1) & \text{if } c_t^1 \geq \lambda_t^1, \\
\arg\max\, p(y_{t+1} \mid d_t^2) & \text{if } c_t^2 \geq \lambda_t^2, \\
\vdots \\
\arg\max\, p(y_{t+1} \mid d_t^L) & \text{otherwise.}
\end{cases}
$$

**Confidence measures.** Three options are evaluated:

- **Softmax response** — top-two gap of $\text{softmax}(W^i d_t^i)$. Highest predictive power; FLOPs-heavy due to full vocabulary projection.
- **Hidden-state saturation** — cosine similarity $\text{sim}(d_t^i, d_t^{i-1})$. Parameter-free; identifies representation saturation; competitive but typically weaker than softmax.
- **Early-exit classifier** — a frozen linear head $M(d_t^i)$ trained post-hoc via per-layer cross-entropy against a local consistency oracle $\mathbf{1}[\arg\max p(y|d_t^i) = \arg\max p(y|d_t^L)]$. Adds only $|\mathbf{d}|+1$ parameters; preferred when total (including parallelisable) FLOPs dominate.

**Decaying threshold.** Early-token mistakes compound across the sequence. CALM mitigates this with a position-decaying threshold motivated by the approximately logarithmic decay of per-perturbation influence with sequence position:

$$
\lambda'(\lambda, t) := \operatorname{clip}_{[0,1]}\!\left(\tfrac{9}{10}\lambda + \tfrac{1}{10}e^{-\tau \cdot t/N}\right)
$$

where $N$ is max output length and $\tau$ is a user temperature. A fixed threshold produces a cliff in the efficiency–quality trade-off; the decaying schedule reveals smooth Pareto frontiers.

**State-copying for missing hidden states.** Self-attention at layer $i$ for token $t$ requires $d_s^{i-1}$ for all prior tokens $s < t$. When token $s$ exited at layer $j < i-1$, those states are unavailable. CALM copies: $d_s^k := d_s^j$ for all $k > j$, but applies layer $i$'s own projections $W_K^i, W_V^i$ to compute key-values. Oracle experiments confirm near-lossless quality: oracle ROUGE-L = 38.24 vs full-model 38.32 at 1.53 average layers/token on CNN/DM. Copying projected $K^j, V^j$ vectors directly instead causes severe degradation to ROUGE-L 23.02 — projecting with the current layer's weights is critical.

**Multi-layer auxiliary loss.** Fine-tuning uses linearly-increasing per-layer weights so that deeper layers receive proportionally stronger gradient signal:

$$
\mathcal{L} = \sum_{i=1}^{L} \omega_i \mathcal{L}_i, \quad \omega_i = \frac{i}{\sum_{j=1}^{L} j}
$$

The early-exit classifier is trained in a second frozen pass after the backbone is fine-tuned.

**Calibrated threshold selection.** Quality guarantees (textual consistency $\mathbb{E}[\mathcal{D}(Y_\text{early}, Y_\text{full})] \leq \delta$ or risk consistency against references) are certified at $\geq 1-\epsilon$ ($\epsilon = 0.05$) via LTT. A grid $\Lambda = (\lambda_1 > \lambda_2 > \cdots > \lambda_k)$ is tested in descending order using Hoeffding-Bentkus p-values on a calibration set; fixed-sequence testing controls FWER. Calibration for textual consistency requires only unlabeled prompts — no gold references.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G3** (token-conditional routing) | **Direct** | Canonical confidence-based per-token depth routing; the primary concrete realization of G3 in the depth dimension. |
| **G1** (block isolation / swappability) | Indirect precondition | CALM's exit quality degrades if intermediate layers don't produce useful vocabulary distributions. Without [[block-isolation-training]]-style pressure, early exits are noisier. |
| **G2** (dynamic parameter allocation) | Not applicable | CALM routes in the depth dimension at inference time; it is not a parameter-allocation method. |

## Credibility

Primary source: peer-reviewed NeurIPS 2022. Google Research / MIT CSAIL. Code released at `github.com/google-research/t5x/tree/main/t5x/contrib/calm`. Theoretical guarantees are rigorous (LTT, FWER-controlled). Empirical results on standard benchmarks with a single backbone (T5 1.1, 8 layers); generalization to larger or decoder-only models is not demonstrated in the paper.

## Empirical claims

- Softmax confidence: up to **×3 speedup** on T5 8-layer with provable quality bounds at specified $\delta$.
- Oracle confidence (agreeing with final-layer argmax): 1.2–1.5 average layers/token — theoretical ceiling.
- Dynamic oracle: **×5.2 FLOPs reduction** on CNN/DM summarization with near-zero ROUGE-L drop.
- Longer-output tasks (summarization, translation) benefit most; short QA outputs are encoder-latency-dominated.

## Open questions / failure modes

- Results on a single small backbone (8-layer T5). Whether confidence signals remain reliable at scale (e.g. 70B decoder-only) is untested.
- Copying hidden states from earlier exits ($d_s^k := d_s^j$) introduces a distributional mismatch; the near-lossless oracle result holds at low exit rates but may degrade at aggressive thresholds.
- CALM requires a calibration set; distribution shift between calibration and deployment invalidates the coverage guarantee.
- The paper does not use early-exit-aware pretraining ([[layerskip]]-style layer dropout + shared exit head). On backbones without that training pressure, exit quality at shallow layers is weaker and confidence signals are less discriminative.
- Decoding throughput gains depend on hardware: early exit reduces FLOPs but may not reduce wall-clock time on batched GPU inference where the bottleneck is memory bandwidth, not compute.

## Source

- `raw/research/selective-replacement-and-training/21-calm.md` (PDF capture, arXiv 2207.07061, NeurIPS 2022)
- `raw/research/selective-replacement-and-training/14-calm-abs.md` (arXiv abstract)

## Related

- [[layerskip]] — training-time pairing: LayerSkip prepares the model (layer dropout + shared early-exit head), CALM does the per-token decision at inference.
- [[mod]] — concurrent / complementary alternative: top-$k$ routing trained jointly routes tokens around blocks rather than exiting early; different trade-off (routing overhead vs. no calibration set needed).
- [[token-conditional-routing]] — concept anchor; CALM is the canonical confidence-based per-token early-exit method.
- [[block-isolation-training]] — preconditions: CALM benefits from any training pressure that makes intermediate representations viable exit points.
- [[modular-deep-learning]] — survey context.
