# SpinQuant: LLM Quantization with Learned Rotations

PTQ method that learns orthonormal rotation matrices on the Stiefel manifold via Cayley SGD to eliminate activation and weight outliers, closing the W4A4KV4 accuracy gap to full precision to ~2.9 pts on LLaMA-2 7B. Unlike [[quarot]], which uses fixed random Hadamard rotations, SpinQuant optimizes two of the four rotations ($R_1$, $R_2$) directly against a calibration loss while leaving model weights frozen.

## Method core

Four rotation matrices are inserted at structurally invariant positions in a pre-norm transformer. "Invariant" means the rotation can be absorbed into adjacent linear weights without changing forward-pass semantics, except where absorption is impossible (KV cache and MLP intermediate activations).

- $R_1$ ($D_\text{token} \times D_\text{token}$, global): rotates the full residual stream; absorbed into downstream weight matrices. Removes channel-wise outliers feeding Q/K/V/up/gate projections.
- $R_2$ ($D_\text{head} \times D_\text{head}$, per-layer): multiplies $W_V$; inverse $R_2^\top$ applied head-wise to $W_O$ inputs. Absorbed at inference time. Targets value-cache and out-projection input outliers.
- $R_3$ (online, KV cache path): fixed random Hadamard; applied at runtime before KV quantization; not absorbed.
- $R_4$ (online, MLP down-projection input): fixed random Hadamard; applied at runtime; not absorbed.

**SpinQuant$_\text{no had}$** = $R_1 + R_2$ only (fully absorbable; zero forward-pass overhead at inference). **SpinQuant$_\text{had}$** = all four ($R_3$, $R_4$ via fast Hadamard transform, ~8% latency overhead).

**Learning objective** — optimize $\{R_1, R_2\}$ on the Stiefel manifold $\mathcal{M}$ with weights frozen:

$$\arg\min_{R \in \mathcal{M}} \mathcal{L}_Q(R_1, R_2 \mid W, X)$$

where $\mathcal{L}_Q$ is cross-entropy evaluated on a calibration set (800 samples from WikiText-2, 100 iterations). Weights are quantized activation-side only during this phase; [[gptq]] is applied afterward for weight quantization error — decoupling the two error sources.

**Cayley SGD** — constraint-preserving update rule that keeps $R$ on the Stiefel manifold at each step:

$$R' = \Delta R(Y)\, R, \quad \Delta R(Y) = \left(I - \tfrac{\alpha}{2}Y\right)^{-1}\!\left(I + \tfrac{\alpha}{2}Y\right)$$

where $Y = \hat{G} - \hat{G}^\top$ is the skew-symmetric matrix derived from the loss gradient $\hat{G}$. ~2× cost of naive SGD per iteration; orthonormality is guaranteed exactly, not approximately. $\{R_1, R_2\}$ comprise only ~0.26% of model parameter count.

## Goal relevance

- **G1 (swappable isolated blocks)**: background only — SpinQuant is PTQ for monolithic LLMs. The per-layer $R_2$ (independent per block) suggests rotation-based block fingerprinting that could compose cleanly with modular block pools; see [[block-isolation-training]].
- **G2 (dynamic per-block params)**: indirect — $R_2$ is learned separately per layer, amounting to per-block parameter differentiation. A precedent for per-block learned parameters without retraining the full model.
- **G3 (token-conditional routing)**: not relevant — SpinQuant is unconditional and applies uniformly across all tokens.

## Credibility

- Venue / year: arXiv 2405.16406 (Meta), 2024; no peer-review venue noted in source
- Code: public — github.com/facebookresearch/SpinQuant
- Ablation rigor: strong — rotation type (FP vs Hadamard), optimization vs random, compatibility with [[gptq]], initialization sensitivity, per-component ablation ($R_1/R_2$ vs $R_1$–$R_4$), 7 models × 4 bit-width settings
- Replication: code public; [[quarot]] comparison uses independently run baselines

## Empirical claims

- W4A4KV4 LLaMA-2 7B: SpinQuant$_\text{had}$ reaches 64.0 avg. zero-shot accuracy (gap to FP: 2.9 pts) vs. LLM-QAT 44.9 (gap 22.0) and [[smoothquant]] 39.0 (gap 27.9 pts).
- W4A8 LLaMA-3 8B: SpinQuant$_\text{no had}$ leaves only 1.0 pt gap to FP, +4.1 pts over [[gptq]] alone.
- W4A8KV8 Mistral-7B: SpinQuant$_\text{no had}$ narrows gap from 12.1 (baseline) to 1.6 pts.
- LLaMA-3 70B W4A4: SpinQuant$_\text{had}$+GPTQ outperforms [[quarot]]+GPTQ by up to 28.6 pts.
- Rotation variance: best vs worst random rotation differs by 13 pts on LLaMA-2 7B W4A4; Cayley-optimized rotation reduces variance to near-zero across seeds.
- Decoding speed (LLaMA-3 8B, M1 Pro): FP 177 ms/token → SpinQuant$_\text{no had}$ 58.9 ms/token (~3× speedup); SpinQuant$_\text{had}$ 63.9 ms/token (8% overhead vs no-had).
- Optimization wall-clock: 13–30 min for 1B–8B models; 3.5 h for 70B.

## Open questions / failure modes

- $R_3$/$R_4$ Hadamard matrices are fixed random (not learned) — whether learning all four rotations improves results is open.
- Closed-form optimal rotation for known outlier distributions left as future work.
- Post-norm architectures break the rotational invariance argument; no evaluation on those.
- No evaluation on instruction-tuned variants; rotation may need re-learning after RLHF/SFT.
- Calibration set distribution mismatch (WikiText-2) for domain-specific LLMs unexplored.
- KV-cache quantization under grouped-query attention (GQA) not explicitly ablated.

## Source

- `raw/research/block-training-quantization/22-spinquant.md` (PDF capture; note: marker introduced letter-spacing artifacts in the title — canonical title is "SpinQuant: LLM Quantization with Learned Rotations")
- `raw/research/block-training-quantization/05-spinquant-abs.md` (arXiv abstract)

## Related

- [[brecq]] — block-reconstruction PTQ; orthogonal axis to rotation
- [[gptq]] — applied for weights after SpinQuant's $R_1$/$R_2$ rotation; explicit composition in the paper
- [[awq]] — alternative outlier handling via per-channel scaling
- [[omniquant]] — alternative learnable PTQ; LET vs rotation
- [[smoothquant]] — alternative outlier-migration baseline; SpinQuant outperforms by 20–25 pts at W4A4
- [[quarot]] — concurrent work using random Hadamard rotations; SpinQuant uses learned ones
- [[block-isolation-training]] — concept anchor; per-block $R_2$ learning is per-block parameter differentiation
