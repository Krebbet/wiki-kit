# State Stream Transformer V2: Nonlinear Latent Recurrence

Fifth Dimension (arXiv:2605.00206). SST V2 adds per-layer FFN-driven horizontal latent-state recurrence to a frozen **Gemma 3 27B** backbone via QLoRA, training exclusively on 6,579 GSM8K examples on a single RTX PRO 6000. A Latent State Cache (LSC) vector streams across positions — blended into the post-attention hidden state before each FFN, then updated by that FFN's nonlinear output — giving a fixed 651 KB horizontal memory footprint independent of context length. A two-pass training scheme (rollout pass → associative scan → parallel pass) parallelises what would otherwise be a sequential dependency at O(α²) ≈ 6–12 × 10⁻⁴ approximation error. Headline wins: **+15.15 pp on GPQA-Diamond** (61.11% vs 45.96% fine-tuned baseline, 28.04% error reduction) and **46.38% error reduction on GSM8K** (97.19% vs 94.77%), beating DeepSeek V3 671B and Gemma 2.0 Flash with 25× fewer parameters.

## Method

- **Latent State Cache (LSC):** a d-dimensional vector per layer, blended into the post-attention hidden state before the FFN with a learned per-dimension per-layer scalar α_l ∈ [0.015, 0.10]. Post-FFN output updates the LSC. Total blend parameters: 333,312.
- **Nonlinear recurrence:** unlike linear-dynamics SSMs, the LSC evolves through each layer's pretrained GELU FFN — the Transformer's own nonlinearity is reused rather than replaced. Attention is preserved alongside the stream.
- **Two axes of computation:** vertical = standard per-position FFN depth; horizontal = LSC carries transformed representations across positions so context is not reset at each token.
- **Two-pass parallel training:** pass 1 runs without the blend to produce approximate states; a per-layer associative scan propagates them; pass 2 re-runs with blend enabled and co-trains LoRA + blend parameters. Training cost ≈ 2× a standard forward pass; enables fully parallel training of a nominally sequential recurrence.
- **Iterative inference:** 1–4 iterations per token tested (imax=4 for headline numbers); LSC carries state between iterations. **Overthinking caveat:** flat imax=4 drops GPQA-Diamond to 42.9%; the 61.11% figure requires staged compute (post-hoc best iteration per question). A learned halting probe trained from position-0 latent state predicts convergence before generation — demonstrated but not yet integrated into inference.
- **V1→V2 delta:** V2 introduces per-layer learnable blend scalars, the two-pass associative-scan training scheme, and iterative inference. V1 used a simpler fixed-blend architecture without the parallel-training trick.

## Results

- **GPQA-Diamond (N=198):** 61.11% vs fine-tuned baseline 45.96% → **+15.15 pp, 28.04% error reduction**. Baseline-matched fine-tune isolates the mechanism cleanly.
- **GSM8K (N=1,319):** 97.19% vs baseline 94.77% → +2.43 pp, **46.38% error reduction**.
- **External comparisons (0-shot greedy):** 27B SST at imax=4 exceeds DeepSeek V3 671B (59.1%), Gemini 2.0 Flash (60.1%), Llama 3.3 70B (50.5%), and Llama 3.1 405B (96.8% on GSM8K) — all 25× or more larger.
- **Training-data efficiency:** all gains from QLoRA on 6,579 GSM8K examples only; no additional instruction-tuning or RLHF.

## Why this matters

SST V2 is a **third path** in the long-context-architecture debate captured in [[conflicts/fixed-state-ssm-long-context]]. The existing conflict has two camps: (A) fixed-state SSMs are insufficient for long-sequence reasoning ([[ssm-tool-use-length-generalization]], [[titans-miras]]) vs (B) hybrid SSM+attention architectures recover much of the gap ([[mamba-3]]). SST V2 does neither — it keeps a full Transformer backbone and adds nonlinear horizontal state recurrence per layer, orthogonal to both the SSM replacement line and the TTT/fast-weights line ([[in-place-ttt]], [[titans-miras]], [[nested-learning]]). The LSC is fixed-size (constant 651 KB), but the update is FFN-nonlinear, which the paper argues provides materially more per-step representational power than the linear or near-linear dynamics Theorem 2.1 of [[ssm-tool-use-length-generalization]] was proven for. Whether SST V2's fixed LSC genuinely escapes that theorem's information-theoretic ceiling — or whether the GPQA-Diamond gains reflect benchmark-specific compression rather than principled long-context capacity — is unresolved. See [[conflicts/fixed-state-ssm-long-context]] for the updated three-position framing.

Comparing to the nearest horizontal-recurrence neighbor: [[hyperloop-transformers]] adds loop-level depth recurrence with shared weights across the full sequence; SST V2 adds per-layer LSC blend at each forward pass, finer granularity and no weight sharing. Both preserve attention and add horizontal state, but the granularity and memory mechanism differ. [[latent-grpo]] is convergent in goal (more reasoning per token without growing context) but orthogonal in mechanism — it compresses discrete CoT chains into vocabulary-superposition tokens at inference, while SST V2 streams hidden-layer states during generation. The two could in principle be stacked.

## Reproducibility

- Backbone: Gemma 3 27B (Google).
- Training hardware: single RTX PRO 6000.
- Training data: GSM8K only (6,579 examples, CodeACT format).
- Training cost: ≈ 2× forward-pass compute per step (two-pass scheme).
- Halting probe: demonstrated feasibility only; not yet production-integrated.
- Code: not referenced in the source; no public repo or weights link cited.

## Source

- `raw/research/weekly-2026-05-11/02-sst-v2.md` — arXiv:2605.00206.

## Related

- [[conflicts/fixed-state-ssm-long-context]] — SST V2 is Position C (Transformer + nonlinear horizontal state); updates the two-position conflict.
- [[ssm-tool-use-length-generalization]] — Theorem 2.1 limits fixed-state GSSMs with linear dynamics; SST V2's nonlinear LSC may not fall under this class.
- [[mamba-3]] — SSM replacement line; SST V2 augments rather than replaces attention.
- [[titans-miras]] — uses trainable memory network to escape fixed-state ceiling; SST V2 keeps fixed-size LSC but makes update nonlinear.
- [[hyperloop-transformers]] — loop-level depth recurrence with shared weights vs SST V2's per-layer LSC blend; similar horizontal-state motivation, different granularity.
- [[latent-grpo]] — continuous latent reasoning at inference (vocab-superposition tokens); convergent goal, orthogonal mechanism.
- [[in-place-ttt]], [[nested-learning]] — TTT/fast-weights line for long-context; distinct from SST V2's fixed nonlinear LSC approach.
