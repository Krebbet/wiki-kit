# TiDAR — Think in Diffusion, Talk in AutoRegression

NVIDIA hybrid (arXiv:2511.08923) that drafts tokens in parallel via masked diffusion and verifies/samples them autoregressively in the same forward pass — a single-model self-speculative architecture claiming AR-quality output at **4.71×–5.91× throughput**.

## Method

Sequence-level hybrid built on top of an AR base (continual pretraining from Qwen2.5-1.5B / Qwen3-8B). Key design:

- **Structured attention mask over a doubled-length input.** Prefix tokens get causal attention (AR mode); the appended block of mask tokens gets bidirectional attention conditioned on the prefix (one-step diffusion mode). This modifies Block Diffusion (Arriola 2025) which keeps only the last block bidirectional rather than all blocks; this restores label-shifted NTP loss on the prefix that Block Diffusion cannot compute.
- **Training objective**: weighted sum of standard NTP CE loss (AR section) + diffusion CE loss where the diffusion section is fully masked at every step (rather than randomly corrupted as in Block Diffusion / SBD / LLaDA / Dream). Full-mask training simplifies loss balancing (equal token counts), densifies the diffusion signal, and aligns train with one-step inference. Loss balancing factor `α=1` by default.
- **Inference**: each forward pass simultaneously (a) AR-verifies the previous step's drafts via rejection sampling against the joint distribution and (b) pre-drafts next-step tokens via one-step diffusion, conditioned on every possible acceptance prefix (so one of the pre-drafts is always usable regardless of how many tokens were accepted). Apple MTP (Samragh 2025) is cited as the inspiration for the parallel pre-drafting structure.
- **Exact KV cache supported** (unlike Fast-dLLM, d-KV Cache, or pure dLMs); rejected-prefix KV is evicted with no recompute.
- Inference uses a pre-initialised Flex Attention block mask sliced per step; sequence reordering puts draft+prefix in the slot expected by the cached mask.

Training: 50B tokens for 1.5B (block sizes 4/8/16); 150B tokens for 8B (block 16). Cosine LR 1e-5 → 3e-6, 1% warmup, seq len 4096, BF16, distributed Adam, modified Megatron-LM + Torchtitan. Batch size 2M tokens (DDP) on H100s.

## Results

On Qwen2.5-1.5B and Qwen3-8B continual-pretrains (Tables 2-4, Figure 4):

- **TiDAR-1.5B**: 7.45 avg tokens/NFE; HumanEval 43.29, HumanEval+ 39.02, MBPP 41.40, MBPP+ 61.11, GSM8k 53.90, Minerva 25.48 (avg **44.03**). Beats Block Diffusion-1.5B (38.41) trained on the same recipe; closes most of the gap to Qwen2.5-1.5B base AR (41.64).
- **TiDAR-8B (Trust-Diff)**: 8.25 tokens/NFE; HumanEval 57.93, HumanEval+ 55.49, MBPP 65.40, MBPP+ 80.95, GSM8k 80.44, Minerva 51.64 (avg **65.31**). Compare Qwen3-8B AR base 68.09; LLaDA-8B 41.78; Dream-7B 58.74. Beats all open dLMs and approaches AR.
- **Likelihood (Table 3)** on MMLU/ARC/Hellaswag/PIQA/Winogrande: TiDAR-8B avg **75.40**, exceeding Qwen3-8B AR (74.25), Dream-7B (71.86), LLaDA-8B (68.06). TiDAR computes likelihood causally in a single NFE rather than via MC sampling (128 steps for the dLM baselines).
- **Throughput (Figure 4, single H100, batch=1, native PyTorch + Flex Attention):** **4.71×** speedup over Qwen2.5-1.5B AR, **5.91×** over Qwen3-8B AR; beats EAGLE-3 weights from AngelSlim/Tengyunw both in T/NFE and T/s conversion rate.
- **Ablations**: full-mask training beats random-mask (Table 5: ~3-7 pt quality gain on coding at the same draft length). Trust-AR vs Trust-Diff logit aggregation is robust across α.

## Applicability

- Any team running an open AR base (Qwen2.5/Qwen3 demonstrated; method is base-model agnostic) with continual-pretraining compute on the order of 50B–150B tokens.
- Strong candidate for **batch=1 latency-critical serving** (chatbots, agentic stepwise loops, on-device speculative decoding) where you want EAGLE-3-class speedups without the EAGLE training-time test or two-model deployment burden — TiDAR is a single model.
- No inference hyperparameters to tune (in contrast to confidence/entropy thresholds in Dream/LLaDA/Fast-dLLM).

Prerequisites: BF16 H100-class hardware (or anywhere Flex Attention runs), Megatron-LM-style distributed training, willingness to double sequence length during training (memory cost). Long-context extension and large-batch behaviour are explicitly listed as open work.

## Novelty

Recombination with a genuinely new design choice. Closest prior: Block Diffusion (Arriola 2025) and Set Block Decoding (Gat 2025), which already mix causal/bidirectional attention. TiDAR's specific contributions:
1. Restricting the bidirectional region to only the last (decoding) block, uniquely enabling prefix NTP loss alongside diffusion loss in the same forward pass (Block Diffusion cannot do this due to label leakage).
2. Full-mask diffusion training (vs random-mask) producing one-step drafting sufficient for high acceptance.
3. Single-forward-pass parallel draft+verify+pre-draft, conditioned on all possible acceptance prefixes (Apple-MTP-style trick repurposed for diffusion drafts).
4. First demonstration that a diffusion-style approach beats SOTA speculative decoding (EAGLE-3) on **measured T/s**, not just T/NFE.

No new losses, optimizers, or model surgery beyond attention masking + a doubled training sequence.

## Reproducibility

Paper is the only artifact referenced. **No GitHub URL, no Hugging Face weights, no paperswithcode entry.** Training framework described as "modified Megatron-LM with Torchtitan support" — internal NVIDIA stack; no release commitment stated. EAGLE-3 baselines are public; Block Diffusion was retrained internally. Independent reproduction would require redoing 50B-token continual pretraining on a Qwen2.5/Qwen3 base.

## Adoption

Fresh NVIDIA paper (Nov 2025). Author roster (Molchanov, Kautz) suggests probable integration into NVIDIA's inference stack and likely community attention. Method explicitly positioned against the diffusion-LLM line (LLaDA, Dream, Block Diffusion, Fast-dLLM, SBD, EAGLE-3, DeepSeek-V3 MTP) and frames itself as the new Pareto frontier — likely to draw responses.

## Source

- `raw/research/radar-2026-04/03-tidar.md` — TiDAR paper PDF (arXiv:2511.08923). Captured 2026-04-22.

## Related

- [[watchlist]] — Block Diffusion, EAGLE-3, LLaDA, Dream, Apple MTP, DeepSeek-V3 MTP referenced but not captured.
