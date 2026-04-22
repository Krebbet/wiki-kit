---
source: "raw/research/radar-2026-04/03-tidar.md"
slug: "03-tidar"
summarized_on: "2026-04-22"
schema_version: 1
---

# TiDAR: Think in Diffusion, Talk in AutoRegression (NVIDIA, arXiv:2511.08923)

## One-line
NVIDIA proposes TiDAR, a single-model hybrid that drafts tokens in parallel via masked diffusion and verifies/samples them autoregressively in the same forward pass, claiming AR-quality output at 4.71x-5.91x the throughput.

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
Sequence-level hybrid architecture built on top of an AR base (continual pretraining from Qwen2.5-1.5B / Qwen3-8B). Key design:
- A structured attention mask over a doubled-length input: prefix tokens get causal attention (AR mode), the appended block of mask tokens gets bidirectional attention conditioned on the prefix (one-step diffusion mode). This is a modification of Block Diffusion (Arriola et al., 2025) which keeps only the last block bidirectional rather than all blocks; this restores label-shifted NTP loss on the prefix that Block Diffusion cannot compute.
- Training objective is a weighted sum of standard NTP CE loss (AR section) and a diffusion CE loss where the diffusion section is fully masked at every step (rather than randomly corrupted as in Block Diffusion / SBD / LLaDA / Dream). Full-mask training simplifies loss balancing (equal token counts), densifies the diffusion signal, and aligns train with one-step inference. Loss balancing factor alpha=1 by default.
- Inference: each forward pass simultaneously (a) AR-verifies the previous step's drafts via rejection sampling against the joint distribution and (b) pre-drafts next-step tokens via one-step diffusion, conditioned on every possible acceptance prefix (so one of the pre-drafts is always usable regardless of how many tokens were accepted). Apple MTP (Samragh et al., 2025) is cited as the inspiration for the parallel pre-drafting structure.
- Exact KV cache supported (unlike Fast-dLLM, d-KV Cache, or pure dLMs); rejected-prefix KV is evicted with no recompute.
- Inference uses a pre-initialized Flex Attention block mask sliced per step; sequence reordering puts draft+prefix in the slot expected by the cached mask.
Training: 50B tokens for 1.5B (block sizes 4/8/16), 150B tokens for 8B (block 16). Cosine LR 1e-5 -> 3e-6, 1% warmup, seq len 4096, BF16, distributed Adam, modified Megatron-LM + Torchtitan. Batch size 2M tokens (DDP) on H100s.

## Results
On Qwen2.5-1.5B and Qwen3-8B continual-pretrains (Tables 2, 3, 4, Figure 4):
- TiDAR-1.5B: 7.45 avg tokens/NFE; HumanEval 43.29, HumanEval+ 39.02, MBPP 41.40, MBPP+ 61.11, GSM8k 53.90, Minerva 25.48 (avg 44.03); beats Block Diffusion-1.5B (38.41 avg) trained on the same recipe; closes most of the gap to Qwen2.5-1.5B base AR (41.64 avg).
- TiDAR-8B (Trust-Diff): 8.25 tokens/NFE; HumanEval 57.93, HumanEval+ 55.49, MBPP 65.40, MBPP+ 80.95, GSM8k 80.44, Minerva 51.64 (avg 65.31). Compare Qwen3-8B AR base 68.09; LLaDA-8B 41.78; Dream-7B 58.74. So TiDAR-8B beats all open dLMs and approaches AR.
- Likelihood (Table 3) on MMLU/ARC/Hellaswag/PIQA/Winogrande: TiDAR-8B avg 75.40, exceeding Qwen3-8B AR (74.25), Dream-7B (71.86), LLaDA-8B (68.06). TiDAR computes likelihood causally in a single NFE rather than via MC sampling (128 steps for the dLM baselines).
- Throughput (Figure 4, single H100, batch=1, native PyTorch + Flex Attention): 4.71x speedup over Qwen2.5-1.5B AR, 5.91x over Qwen3-8B AR; beats EAGLE-3 weights from AngelSlim/Tengyunw both in T/NFE and T/s conversion rate.
- Ablations: full-mask training beats random-mask (Table 5: ~3-7 pt quality gain on coding at the same draft length). Trust-AR vs Trust-Diff logit aggregation (Figure 6) is robust across the loss-balancing factor — alpha=1 yields nearly identical quality either way.

## Applicability
- Fits any team that already runs an open AR base (Qwen2.5/Qwen3 demonstrated; the method is base-model agnostic) and has continual-pretraining compute on the order of 50B-150B tokens. The 1.5B run was 50B tokens at 2M batch on H100; the 8B used 150B tokens with gradient checkpointing.
- Strong candidate for batch=1 latency-critical serving (chatbots, agentic stepwise loops, on-device speculative decoding) where you want EAGLE-3-class speedups without the EAGLE training-time test or two-model deployment burden — TiDAR is a single model.
- Prerequisites: BF16 H100-class hardware (or anywhere Flex Attention runs), Megatron-LM-style distributed training, the willingness to double sequence length during training (memory cost). Long-context extension and large-batch behavior are explicitly listed as open work.
- No inference hyperparameters to tune (in contrast to confidence/entropy thresholds in Dream/LLaDA/Fast-dLLM).

## Novelty
Recombination with a genuinely new design choice. The closest prior work is Block Diffusion (Arriola, 2025) and Set Block Decoding (Gat, 2025), which already mix causal/bidirectional attention. TiDAR's specific contributions:
1. Restricting the bidirectional region to only the last (decoding) block, which uniquely enables prefix NTP loss alongside diffusion loss in the same forward — Block Diffusion cannot do this due to label leakage.
2. Full-mask diffusion training (vs. random-mask) producing one-step drafting that is sufficient for high acceptance.
3. Single-forward-pass parallel draft+verify+pre-draft, conditioned on all possible acceptance prefixes (an Apple-MTP-style trick repurposed for diffusion drafts).
4. First demonstration that a diffusion-style approach beats SOTA speculative decoding (EAGLE-3) on measured T/s, not just T/NFE.
Does not introduce new losses, optimizers, or model surgery beyond attention masking + a doubled training sequence.

## Reproducibility
- Paper (arXiv:2511.08923) is the only artifact referenced in the captured source. No GitHub URL, no Hugging Face weights, no paperswithcode entry mentioned in the body or references section read.
- Training framework described as "modified Megatron-LM with Torchtitan support" — internal NVIDIA stack; no release commitment stated.
- Baselines they compare against (EAGLE-3 weights via AngelSlim and Tengyunw on HF) are public; Block Diffusion they retrained themselves under the same recipe.
- Independent reproduction would require redoing 50B-token continual pretraining on a Qwen2.5/Qwen3 base — feasible for a well-resourced lab but not trivial.

## Adoption
- This is a fresh NVIDIA paper (arXiv 2511.xxxxx => Nov 2025); too new to have downstream citations. The radar capture date is 2026-04-22, ~5 months out.
- Author roster (Molchanov, Kautz) and NVIDIA affiliation suggest probable integration into NVIDIA's inference stack and likely community attention. Cannot confirm leaderboard climb from this source alone.
- Method explicitly positioned against the diffusion-LLM line (LLaDA, Dream, Block Diffusion, Fast-dLLM, SBD, EAGLE-3, DeepSeek-V3 MTP) and frames itself as the new Pareto frontier — likely to draw responses.

## Conflicts
The wiki currently has no content pages besides `reference-sources`, so no contradictions are possible at this moment. Forward-looking flags: TiDAR's central claim — that diffusion-style parallel drafting can beat speculative decoding (EAGLE-3) on wall-clock T/s — is the kind of claim that may be contested by future EAGLE/Medusa/MTP-camp results; worth re-checking once a parallel speculative-decoding page exists.
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
(Wiki contains only `[[reference-sources]]` at present; no existing topical pages to link. Anticipated cross-refs once sibling ingests land in the same radar:)
- [[diffusion-language-models]] — would be the natural parent page; TiDAR extends Block Diffusion / LLaDA / Dream lineage.
- [[speculative-decoding]] — TiDAR is positioned as a self-speculative single-model alternative to EAGLE-3 / Medusa / DeepSeek-V3 MTP / Apple MTP.
- [[parallel-decoding]] / [[multi-token-prediction]] — overlaps with the broader MTP discussion.
- [[inference-efficiency]] — wall-clock throughput, KV-cache management, free-token-slot exploitation.
- [[hybrid-architectures]] — sequence-level mixing of causal and bidirectional attention.

## Conflict flags
(none) — no existing wiki content to contradict.

## Proposed page shape
- New page: `tidar` under a `wiki/architectures/` or `wiki/inference/` topical subdir — one focused page covering the architecture, training recipe, results, and a comparison table against EAGLE-3 / Block Diffusion / LLaDA / Dream.
- AND seed two thin parent pages so cross-refs work: `diffusion-language-models` (with sections on LLaDA, Dream, Block Diffusion, Fast-dLLM, SBD, TiDAR) and `speculative-decoding` (Medusa, EAGLE-1/2/3, DeepSeek-V3 MTP, Apple MTP, TiDAR-as-self-speculative).
- Defer a `parallel-decoding` / `multi-token-prediction` umbrella page until a sibling ingest justifies it; otherwise TiDAR's content can live entirely in the two parents above plus its own page.
