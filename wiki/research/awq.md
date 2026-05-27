# AWQ: Activation-Aware Weight Quantization for On-Device LLM Compression and Acceleration

AWQ is a post-training quantization (PTQ) method that identifies salient weight channels via calibration-set activation magnitudes and applies per-channel scaling to reduce quantization error — with no backpropagation, no reconstruction loop, and only ~16 calibration sequences. Scaling is absorbed into adjacent operators at inference time, yielding zero runtime overhead. The accompanying TinyChat engine delivers 3.2–3.9× throughput over FP16 on edge-class hardware. At W4A16 granularity AWQ matches or beats [[gptq]] at all scales from 7B to 70B parameters and generalises to multimodal models (OpenFlamingo, VILA) and MoE architectures ([[mixtral]]-8x7B).

## Method core

Standard linear layers $y = Wx$ are replaced at inference time by:

$$y = Q\!\left(W \cdot \operatorname{diag}(\mathbf{s})\right)\!\left(\operatorname{diag}(\mathbf{s})^{-1} x\right)$$

where $\mathbf{s} = \mathbf{s}_X^\alpha$ is a per-(input-)channel scale derived from offline activation statistics and $\alpha \in [0,1]$ is grid-searched to minimise:

$$\left\|Q\!\left(W \cdot \operatorname{diag}(\mathbf{s})\right)\!\operatorname{diag}(\mathbf{s})^{-1} X - WX\right\|$$

$\operatorname{diag}(\mathbf{s})^{-1}$ is fused into the preceding operator (LayerNorm, embedding, or previous linear), so no runtime scale application occurs. The quantization is weight-only (W4A16 or W3A16); activations remain FP16. No gradients are computed at any stage. Calibration requires only ~16 sequences — 10× fewer than [[gptq]] with better out-of-distribution robustness (+0.5–0.6 PPL shift vs +2.3–4.9 for GPTQ).

## Goal relevance

- **G1 (swappable isolated blocks):** background — AWQ operates uniformly across all weight channels and does not address block isolation or swappability, but a per-block AWQ variant is a natural extension; calibration statistics could be gathered per block independently.
- **G2 (dynamic per-block params):** weak background — static PTQ, not dynamic allocation; however, the activation-saliency insight directly parallels the hypothesis that some blocks carry more signal and could warrant differential bit allocation during inference.
- **G3 (token-conditional routing):** not relevant — no routing mechanism.
- **Deployment background:** directly relevant to running quantized block pools on edge hardware (Jetson Orin, mobile SoCs); TinyChat's INT4 dequantization kernels are a usable starting point.

## Credibility

- **Venue / year:** MLSys 2024, Best Paper Award
- **Code:** released — https://github.com/mit-han-lab/llm-awq
- **Weights:** released via HuggingFace AWQ model zoo
- **Ablation rigor:** strong — $\alpha$ grid search (Tables 2/3/5), calibration-set size and distribution robustness (Figure 8), mixed-precision baseline (Table 1), INT2 extreme setting (Table 9)
- **Replication:** widely adopted — HuggingFace Transformers, TensorRT-LLM, vLLM, Google Vertex AI, Amazon SageMaker, AMD ROCm, Intel Neural Compressor, FastChat, LMDeploy

## Empirical claims

- **LLaMA/Llama-2 INT3-g128 WikiText-2 PPL:** AWQ 6.24 vs GPTQ-R 6.42 (7B); AWQ 3.74 vs GPTQ-R 3.86 (70B).
- **INT4-g128:** AWQ matches or beats GPTQ-R at all scales 7B–70B; near-lossless on Llama-2-70B (3.41 vs FP16 3.32).
- **OpenFlamingo-9B INT4-g128 COCO 32-shot CIDEr:** AWQ −1.17 vs RTN −4.57 and GPTQ −6.72.
- **VILA-7B/13B INT4-g128:** lossless across 11 VLM benchmarks.
- **TinyChat throughput:** 3.2–3.9× over HuggingFace FP16 on RTX 4090 and Jetson Orin.
- **Calibration efficiency:** AWQ achieves better PPL with 16 sequences vs GPTQ's 192; OOD penalty +0.5–0.6 PPL vs +2.3–4.9 for GPTQ.
- **Mixtral-8x7B INT4-g128:** 6.05 PPL vs 5.94 FP16 — activation-aware scaling transfers to MoE block-pool architectures.

## Open questions / failure modes

- Per-block or per-layer non-uniform bit allocation is not explored; all layers receive identical treatment. Whether activation saliency could drive block-granularity bit assignment (directly relevant to G2) is an open question.
- Calibration-set domain shift is small but non-zero; behaviour on heavily out-of-domain fine-tuned adapters is unknown.
- INT2 requires GPTQ on top of AWQ; AWQ alone is insufficient at extreme compression ratios.
- W4A16 dequantization on non-CUDA platforms (CPU, custom accelerators) requires platform-specific kernels; TinyChat addresses CUDA/ARM/AVX but portability is non-trivial.
- No interaction with block-structured sparsity or structured pruning.

## Source

- `raw/research/block-training-quantization/16-awq.md` (PDF capture)
- `raw/research/block-training-quantization/03-awq-abs.md` (arXiv abstract)

## Related

- [[brecq]] — alternative PTQ via block reconstruction
- [[gptq]] — most-cited weight-only PTQ baseline; AWQ orthogonal and combinable
- [[omniquant]] — block-wise learnable clipping; AWQ's $\alpha$ grid search is related but no backprop
- [[spinquant]] — rotation-based PTQ; can compose with AWQ
- [[smoothquant]] — W8A8 alternative; AWQ targets W4A16 memory-bound regime
- [[llm-int8]] — predecessor W8A8 approach; motivates weight-only quantization direction
- [[mixtral]] — Mixtral-8x7B MoE result demonstrates AWQ on block-pool architectures (relevant for G2/G3 deployment)
