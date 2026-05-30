---
sources:
  - "raw/research/thesis-foundations/07-mamba2-ssd.md"
  - "raw/research/thesis-foundations/08-mamba-empirical-8b.md"
tags: [ssm, mamba, hybrid, attention, architecture, state-space]
---

# Mamba-2 and SSM–Attention Hybrids

Two papers span the same architectural design space from opposite ends. Dao & Gu (2024, arXiv 2405.21060) establish the theoretical basis — proving that selective SSMs and linear attention variants are dual forms of the same structured-matrix computation — and use it to build Mamba-2, which Pareto-dominates both Mamba and Transformer++ at 125M–2.7B scale on the Pile. NVIDIA (2024, arXiv 2406.07887) then validates the hybrid design at production scale: an 8B, 3.5T-token controlled study shows a Mamba-2/attention/MLP hybrid beats a matched Transformer on all 12 standard tasks (+2.65 pts avg) while delivering up to 8× faster inference. Together they establish that the correct inductive bias is a *mix* of block types at specific ratios — not a monoculture of any one type.

## Structured State Space Duality

The central theoretical contribution of Dao & Gu is the **Structured State Space Duality (SSD)** framework. SSMs of the form h_t = A_t h_{t-1} + B_t x_t, y_t = C_t h_t can be rewritten as a matrix multiplication M·x where M is a **1-semiseparable matrix** — a matrix whose lower-triangular part has rank 1 at every submatrix. Linear attention (with scalar gating) generates the same class. This duality is not cosmetic: it means both families are instances of *structured-matrix sequence mixing*, and algorithms that are efficient for one transfer to the other.

The practical payoff is a **block-decomposition hardware algorithm** that splits the semiseparable matrix into on-diagonal (intra-chunk, computed in parallel like attention) and off-diagonal (cross-chunk, computed as a matrix multiply) blocks. This enables a single kernel that is simultaneously hardware-efficient and exact — unlike ring-buffer or recurrence-only implementations.

The framework also clarifies what linear attention *cannot* do: transformations on the attention kernel matrix that lack a finite feature map are outside the structured-matrix family. This is the formal reason SSM layers cannot fully replace softmax attention for tasks requiring unbounded O(T) state (see Failure Modes below).

## Mamba-2 Architecture

Mamba-2 replaces Mamba's selective scan with an SSD layer. Key block design changes (ablated at ~129M parameters):

- **Multi-value/multi-input (MVA/MIS) head pattern**: B and C are shared across heads; A and X are per-head. This substantially outperforms multi-query (MQA) and multi-key (MKA) patterns at identical total state size — 11.66 vs. 12.62/12.59 perplexity at 125M, 8.73 vs. 9.33/9.36 at 360M.
- **State expansion**: N=64 is the standard operating point; Mamba-2 with N=256 substantially outperforms Mamba-1 on the multi-query associative recall (MQAR) hard task.
- **Speed**: SSD is 2–8× faster than Mamba's fused scan at N=64; faster than FlashAttention-2 at sequence lengths ≥ 2K; 6× faster at 16K. Below 2K tokens, SSD is slower than FlashAttention-2.

Full-scale result (07): Mamba-2-2.7B trained on 300B tokens (Pile) achieves perplexity 6.09 and zero-shot avg 60.2, outperforming Pythia-6.9B on the same data.

**Adding MLP layers does not help quality.** Mamba-2-MLP (32 SSD + 32 MLP at 2.7B) reaches perplexity 6.13, worse than pure Mamba-2 (6.09). MLPs are useful only for training throughput or MoE upcycling.

## Hybrid Empirical Results at Scale

NVIDIA's study trains four matched 8B models on identical data and evaluates on 12 standard and 23 long-context tasks:

| Model | Tokens | 12-task avg | 5-shot MMLU |
|---|---|---|---|
| Transformer (baseline) | 3.5T | — | 50.07 |
| Pure Mamba | 3.5T | −2.65 | ~47 |
| Pure Mamba-2 | 3.5T | below Transformer | below Transformer |
| **Mamba-2-Hybrid** | **3.5T** | **+2.65 over Transformer** | **53.60** |

The winning hybrid (56 layers, 8.66B params): **43% Mamba-2 SSM layers, 7% self-attention layers, 50% MLP layers**. Layers are interleaved throughout the full depth — not stacked in homogeneous sections. Attention layers are spaced by a greedy algorithm (Algorithm 1 in the paper) that maximizes inter-attention gaps with Mamba-2 runs between them; MLP layers are distributed away from the start. All layer-type assignments are fixed at architecture construction; no learned routing.

Training efficiency is nearly identical: hybrid MFU 29.9% vs. Transformer MFU 30.7% on H100s. The hybrid *lags* the Transformer early in training but eventually surpasses it — crossover point is data-scale-dependent.

Long-context: continued pretraining to 16K/32K (50B additional tokens) yields a 16K hybrid that beats the 16K Transformer by +13 pts avg on 13 RULER tasks. A 128K hybrid achieves 100% Phonebook accuracy beyond its training context length.

Inference: up to **8× faster token generation** than the matched Transformer at long context lengths, owing to Mamba-2's constant-state recurrence replacing the growing KV cache.

## Attention Ratio Finding

This is the thesis-load-bearing result. Both papers independently derive an optimal attention-layer ratio in an otherwise SSM-dominant stack:

- **07 (Dao & Gu, 350M, 7B tokens)**: pure Mamba-2 perplexity 8.60; adding 1 attention layer drops to 8.38; optimum near **~10% attention** (5–6 of 48 layers). At 2.7B / 300B tokens: 6 attention layers (of 64 total) achieves 5.95 vs. 6.09 pure Mamba-2 and 6.13 pure Transformer.
- **08 (NVIDIA, 130M–840M ablation)**: validation-loss minimum at **~8% attention** layers; 50% MLP layers feasible without quality loss, and speeds training ~20% vs. 5% MLPs.

The two figures converge on the same regime (~8–10% attention) despite different scales, datasets, and training durations. The practical implication: a Transformer-scale stack *does not need* attention as the primary mixing operation — SSM layers do most of the work, attention serves as a sparse retrieval substrate, and MLP layers fill the parameter budget efficiently.

Paper 07 hypothesizes the functional split: **SSM layers act as general sequence-to-sequence maps; attention layers act as a fast in-context retrieval mechanism.** Paper 08 validates this at 8B scale — the hybrid's gains over pure SSMs are sharpest on tasks that stress in-context copying and retrieval.

Attention layer *position* matters less than spacing: 07 finds that evenly-spaced attention positions (not clustered at extremes) are optimal; specific indices do not significantly affect quality as long as spacing is maintained.

## Failure Modes

From 08 unless noted:

**Copying / phonebook recall** — Pure Mamba and Mamba-2 fail the Phonebook task for sequences beyond ~500 tokens. This failure does *not* improve with more training data (gap persists at 3.5T tokens). Root cause (per 07): SSD's bounded recurrent state cannot represent the O(T) KV cache required for exact symbol copying over long distances.

**In-context learning gaps** — Pure SSMs trained on 1.1T tokens score ~15–17 points below the matched Transformer on 5-shot MMLU. The gap narrows to ~1.4 pts at 3.5T tokens but does not close. The hybrid eliminates this gap and exceeds the Transformer.

**Multi-document QA** — The 16K/32K hybrid trails the Transformer by ~1 point avg on LongBench multi-document QA (HotpotQA, 2WikiMQA, Musique). Hypothesized cause: SSM recurrent states are confused by concatenated irrelevant documents, accumulating interference across document boundaries in a way that self-attention's per-query retrieval avoids.

**Prompt sensitivity** — Hybrid models are more sensitive to prompt formatting than Transformers. On Musique, minor prompt reformulation swung hybrid accuracy from 10.63 to 16.16; the matched Transformer ranged 15.25–17.68 under the same variation. This asymmetry is not yet well characterized.

**RoPE incompatibility** — Adding RoPE to hybrid attention layers does not improve base accuracy and hurts long-context extension performance (08). Hybrid attention layers appear to learn positional structure differently from pure Transformer attention.

**MQAR / architectural unknowns** — 07 flags that Mamba-2 substantially outperforms Mamba-1 on the hard MQAR task, but the authors explicitly state they do not know which specific architectural change drives the improvement: "We are not sure which aspect of the architecture is the predominant factor, which remains a question to explore in future work."

## Open Questions

From 07 (Dao & Gu):
- Which architectural change in Mamba-2 vs. Mamba-1 drives MQAR improvement?
- Can attention-sink interpretability techniques transfer to SSM/Mamba-2 layers?
- Can structured matrix algorithms handle general diagonal SSMs (not just scalar-identity A) with equal hardware efficiency?
- Principled non-causal Mamba variants via structured matrix viewpoint.
- What other structured mask matrices (beyond semiseparable) define useful efficient-attention variants?
- Formal characterization of the expressiveness gap between softmax attention and sub-quadratic models.

From 08 (NVIDIA):
- Data efficiency and crossover dynamics: when exactly does hybrid surpass Transformer as a function of training tokens?
- Prompt robustness of hybrid vs. Transformer — why is the hybrid more sensitive, and does instruction tuning fix it?
- Long-context continued pretraining data selection: packing unrelated sequences may harm hybrid SSM-Transformer models more than Transformers.
- Performance of aligned/instruction-tuned hybrid models vs. Transformer counterparts.
- No NAS or automated hybrid architecture search was studied; optimal ratios were found by hand ablation.

---

## Sources
- `raw/research/thesis-foundations/07-mamba2-ssd.md` — Dao & Gu (2024, arXiv 2405.21060) *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality*
- `raw/research/thesis-foundations/08-mamba-empirical-8b.md` — NVIDIA (2024, arXiv 2406.07887) *An Empirical Study of Mamba-based Language Models*

## Related
- [[modular-deep-learning-survey]] — hybrid SSM+attention at fixed ratios is a concrete instance of the survey's "fixed routing" category: structural, not learned.
- [[expert-choice-routing]] — both papers study block specialization via non-uniform compute: EC within-layer; hybrid cross-layer.
- [[mixture-of-depths]] — both show heterogeneous stacks beat homogeneous but via different mechanisms.
