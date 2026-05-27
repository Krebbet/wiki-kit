# OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models

Block-wise differentiable PTQ that freezes full-precision weights and learns only two small parameter sets per block — clipping thresholds (LWC) and equivalent activation-to-weight transforms (LET) — achieving QAT-quality results at PTQ cost, down to W2A16 and W4A4 across LLaMA and OPT families. All learned parameters are absorbed post-calibration, leaving zero inference overhead.

## Method core

Each transformer block $\mathcal{F}(\mathbf{W}, \mathbf{X})$ is replaced by a quantized proxy $\mathcal{F}(Q_w(\mathbf{W};\Theta_1,\Theta_2),\, Q_a(\mathbf{X};\Theta_2))$; block-wise output MSE is minimised via SGD over two disjoint parameter sets, with no gradient flowing across block boundaries.

**Learnable Weight Clipping (LWC)** — $\Theta_1 = \{\gamma, \beta\}$: per-channel sigmoid-gated clipping strengths in $[0,1]$ that scale the MinMax dynamic range before quantization. Post-calibration, absorbed into quantized weights; zero runtime cost.

**Learnable Equivalent Transformation (LET)** — $\Theta_2 = \{\delta, s, s_a\}$: channel-wise shift $\delta$ and scale $s$ on activations, transferred equivalently to weights via

$$\tilde{\mathbf{X}} = (\mathbf{X} - \delta) \oslash s, \qquad \tilde{\mathbf{W}} = s \odot \mathbf{W}$$

Extended to Q/K attention affinity via scale $s_a$. All factors absorbed into preceding LayerNorms or linear projections post-calibration — zero inference overhead.

Both sets trained jointly per block, sequentially across blocks (no cross-block gradient). Calibration: 128 samples, 20–40 epochs, AdamW, single A100-40G; 1 h (LLaMA-2-7B) to 16 h (LLaMA-2-70B).

## Goal relevance

**G1 (swappable isolated blocks):** Direct relevance. Block-wise error minimisation treats each transformer block as an independently optimisable unit with fixed inter-block interfaces, the same isolation assumption required for swappable block training. OmniQuant is one of the cleanest demonstrations in the literature that per-block independent optimisation is both tractable and sufficient — see [[block-isolation-training]].

**G2 (dynamic per-block params):** Partial relevance. $\Theta_1$ and $\Theta_2$ are per-block learned parameters that adapt each block individually, analogous to learning per-block hyperparameters during post-processing rather than pretraining. The block-local optimisation loop is directly transferable as a pattern.

**G3 (token-conditional routing):** Background only. Quantization is static; no routing or token-conditional behaviour.

## Credibility

- **Venue / year:** ICLR 2024 (arXiv 2308.13137, Aug 2023)
- **Code:** public — https://github.com/OpenGVLab/OmniQuant
- **Ablation rigor:** Strong — component ablations (LWC-only, LET-only, combined), hyperparameter sweeps (calibration size, epochs, lr), ET-method comparison table (Table A1), clipping-baseline comparison (Table A14)
- **Replication:** GPTQ, [[smoothquant]], and OS+ baselines reproduced with per-channel/per-token for fair comparison

## Empirical claims

- W2A16 LLaMA-13B: OmniQuant PPL 13.21 vs [[gptq]] PPL 5.5×10³ on WikiText2 — roughly 420× reduction in perplexity degradation.
- W4A4 LLaMA-7B zero-shot avg accuracy: 52.65 vs OS+ 48.43 (+4.22 pp); surpasses QAT baseline LLM-QAT+SQ 46.43 (+6.22 pp).
- W4A4 LLaMA-65B zero-shot avg accuracy: 59.22 vs OS+ 52.52 (+6.70 pp).
- W4A16g128 on A100-80G: ~2× inference throughput over FP16 for 7B (134 vs 69 tokens/s); running memory 14.4 GB → 5.7 GB.
- Training cost: LLaMA-2-7B in ~1 h, 70B in ~16 h, single GPU, 128 calibration samples.

## Open questions / failure modes

- LET applied to the second FFN linear layer causes instability (attributed to high post-nonlinearity activation sparsity); excluded from the method as released.
- W4A4 and W6A6 lack production hardware kernel support; deployment benchmarks cover weight-only quantization only — activation-quantized speedups are theoretical.
- For weight-only quantization on LLaMA, LET yields negligible benefit; LWC alone suffices — suggesting LET is activation-outlier-specific and may not transfer uniformly across architectures.
- Calibration domain is WikiText2; cross-domain degradation not evaluated.
- No evaluation of block-swapping after quantization — composability of independently-quantized blocks drawn from different model variants is unknown.

## Source

- `raw/research/block-training-quantization/18-omniquant.md` (PDF capture)
- `raw/research/block-training-quantization/04-omniquant-abs.md` (arXiv abstract)

## Related

- [[brecq]] — block-reconstruction predecessor; OmniQuant extends with learnable transforms
- [[gptq]] — explicitly outperformed; OmniQuant uses learnable clipping vs GPTQ's Hessian rounding
- [[awq]] — activation-aware scaling without backprop; OmniQuant's LET is the differentiable evolution
- [[spinquant]] — alternative outlier handling via rotations
- [[smoothquant]] — direct precursor of OmniQuant's LET equivalent transformation
- [[block-isolation-training]] — concept anchor; OmniQuant's block-wise differentiable PTQ is one of the cleanest examples of per-block independent optimization for transformers
- [[qlora]] — quantization for fine-tuning context
