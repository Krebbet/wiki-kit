# DeepSeek-V4: 1.6T MoE with Hybrid Attention and mHC

DeepSeek-V4-Pro is a 1.6T-parameter (49B activated) MoE LLM with 1M-token context, achieving 27% of V3's single-token inference FLOPs and 10% of V3's KV cache via a hybrid CSA+HCA attention mechanism, stabilized by [[manifold-constrained-hyper-connections]] (mHC). First production-scale deployment of mHC. SOTA open-source on LiveCodeBench (93.5), Codeforces Rating (3206), and SWE-Verified (80.6, matching Claude Opus 4.6).

## Architecture

Two model sizes: **V4-Pro** (1.6T total / 49B active, 1M context) and **V4-Flash** (284B total / 13B active, 1M context). Both are MoE transformers pretrained on >32T tokens. FP4 precision for MoE expert weights; FP8 mixed precision elsewhere.

**Hybrid attention: CSA + HCA.** Compressed Sparse Attention (CSA) reduces KV representations via structured sparsity; Heavily Compressed Attention (HCA) applies stronger compression on selected layers. Combined result: ~10% of V3's KV cache at 1M context, 27% of V3's single-token inference FLOPs. V3 used MLA (Multi-head Latent Attention); V4's CSA+HCA supersedes it.

**Manifold-Constrained Hyper-Connections (mHC).** mHC replaces conventional residual connections by constraining residual-mixing matrices to the Birkhoff polytope via Sinkhorn-Knopp. Provides gradient stability in deep MoE stacks at scale. V4 is the first large-scale production deployment of this technique (see [[manifold-constrained-hyper-connections]] for the original paper).

**Optimizer: Muon** (replaces AdamW). First large-scale MoE training with Muon; provides faster convergence and improved stability.

## Training

Two-stage post-training: (1) independent domain-expert cultivation via SFT + GRPO per domain; (2) unified model consolidation via on-policy distillation, merging specialist knowledge into a single model. Think Max inference mode requires ≥384K context.

## Results

**Base model deltas vs V3.2-Base (V4-Pro-Base):**
- MMLU-Pro: +8.0 (65.5 → 73.5)
- SimpleQA-Verified: +26.9 (28.3 → 55.2)
- FACTS Parametric: +35.5 (27.1 → 62.6)
- LongBench-V2: +11.3 (40.2 → 51.5)
- HumanEval Pass@1: +14.0 (62.8 → 76.8)

**Instruct model (V4-Pro-Max vs frontier closed-source):**
- LiveCodeBench: 93.5 (best reported, vs Gemini-3.1-Pro-High 91.7)
- Codeforces Rating: 3206 (vs GPT-5.4 3168)
- SWE-Verified: 80.6 (matches Claude Opus 4.6 80.8, Gemini 80.6)
- Apex Shortlist: 90.2 (best reported, vs Gemini 89.1)
- GPQA Diamond: 90.1 (Think Max; behind Gemini 94.3)
- MRCR 1M: 83.5 (behind Claude Opus 4.6 92.9)

**Flash-Max vs Pro-Max:** Flash achieves comparable reasoning (LiveCodeBench 91.6 vs 93.5; HMMT 94.8 vs 95.2) at 13B vs 49B active params; trails on pure knowledge tasks (SimpleQA-Verified 34.1 vs 57.9).

## Applicability

Drop-in replacement for DeepSeek-V3/V3.2. V4-Flash (13B active) is the cost-effective path for most inference deployments; V4-Pro (49B active) justified for coding competitions, agentic workflows, and hard reasoning. 1M context practically usable given CSA+HCA KV reduction. Requires FP4-capable hardware or software dequantization. Inference via vLLM and SGLang (day-one support).

## Source

- HuggingFace: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro (MIT license)
- ModelScope: deepseek-ai/DeepSeek-V4-Pro, deepseek-ai/DeepSeek-V4-Flash
- Technical report: not linked at time of capture (model card + HF release only)

## Related

- [[manifold-constrained-hyper-connections]] — mHC is a direct dependency; V4 validates mHC at 1.6T scale
- [[triattention]] — related KV compression via attention restructuring; compare compression ratios
- [[memagent]] — 1M-context handling; CSA+HCA (dense Transformer) vs memory-augmented approach
- [[gated-deltanet-2]] — recurrent SOTA at long context; V4 is the MoE dense-attention comparison point
- [[llamarl]] — V4's two-stage GRPO → on-policy distillation post-training is relevant to production RL infra design
