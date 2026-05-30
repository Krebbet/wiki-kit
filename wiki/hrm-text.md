# HRM-Text

SapientInc (arXiv:2605.20613) introduces HRM-Text, a 1B-parameter hierarchical recurrent model with a dual-timescale H/L module design (2 outer H-module cycles × 3 inner L-module steps = 8 H/L steps per token, 4× recursion depth) pretrained from scratch on instruction-response pairs only — no raw-text pretraining phase. Training runs 46 hours on 16× H100s (~$1,472) over 40B unique tokens (60B with repetition). The headline result: MATH 56.2 / GSM8K 84.5 / ARC-C 81.9 at ~1×10²¹ FLOPs, beating Huginn 3.5B (MATH 12.6 / GSM8K 34.6 / ARC-C 38.2) at 127× more compute, and matching or beating 2–7B dense open models (Llama3.2 3B at 162×, Gemma3 4B at 96×, Qwen3.5 2B at 432× the compute) on most benchmarks. The paper positions this co-design of architecture + training objective as a challenge to Chinchilla-style raw-text scaling orthodoxy — stated as the authors' claim, not a wiki ruling.

## Method

**Architecture.** Hierarchical recurrent structure (HRM: Hierarchical Recurrent Model): dual-timescale slow (H) and fast (L) modules, parameterized as H2L3. Each token pass executes 8 total H/L steps with 4× recursion depth via parameter sharing. Distinguishable from generic looped Transformers (single-module fixed loops) and RINS.

**Stabilization.**
- *MagicNorm*: per-module exit normalization layered over internal PreNorm blocks. Forward pass sees PostNorm-like activation bounds across N steps; TBPTT backward horizon K ≪ N means gradients behave PreNorm-like. Bridges the PreNorm/PostNorm tradeoff under deep recurrence with truncated backprop.
- *Warmup deep credit assignment*: truncated BPTT starting K=2 (last two recurrent steps), linearly warming to K=5 across training. Curriculum over credit-assignment path length avoids early optimization pathologies.

**Training objective.** Task-completion pretraining only: loss = −log P(x_a | x_q), response-only NLL, trained from scratch on instruction-response pairs (FLAN, OpenMathInstruct2, AceReason, etc.). No unsupervised raw-text phase. PrefixLM attention mask — bidirectional over instruction tokens, causal over response — gives encoder–decoder separation in a decoder-only implementation. Explicit `<think>...</think>` CoT traces are stripped before training, forcing reliance on internal recurrent computation rather than token-level reasoning chains.

Derives from: original HRM (Wang et al., arXiv:2506.21734) for symbolic tasks; Universal Transformers for recurrent depth; T5/FLAN lineage for PrefixLM + instruction-response objectives.

## Results

Single checkpoint, 40B unique tokens (60B with repetition), 16× H100, 46h, ~$1,472.

**Table 1 — FLOPs-matched architecture comparison (1B scale):**

| Model | MMLU | ARC-C | DROP | GSM8K | MATH |
|---|---|---|---|---|---|
| HRM 1B | 60.73 | 81.91 | 82.21 | 84.53 | 56.16 |
| Looped Transformer 1B | 56.51 | 74.06 | 76.20 | 75.13 | 48.30 |
| RINS 1B | 56.09 | 76.71 | 79.92 | 77.71 | 48.90 |
| Transformer 1B | 53.15 | 74.32 | — | — | — |

**Table 3 — Ablation, FLOPs-matched (objective × attention mask × arch):**

| Config | MMLU | MATH |
|---|---|---|
| Transformer 1B + P(x) + Causal | 40.55 | 35.44 |
| Transformer 1B + P(x_a\|x_q) + Causal | 47.72 | 47.04 |
| Transformer 1B + P(x_a\|x_q) + PrefixLM | 53.15 | 48.36 |
| HRM 1B + P(x_a\|x_q) + PrefixLM | 60.73 | 56.16 |

**Table 4 — vs. contemporary open models:**

HRM-Text 1B (1×10²¹ FLOPs / 0.06T tokens) vs. competitors:
- Huginn 3.5B: 127× more compute; MATH 12.6, GSM8K 34.6, ARC-C 38.2
- Llama3.2 3B: 162× more compute
- Gemma3 4B: 96× more compute
- Qwen3.5 2B: 432× more compute
- Ouro 1.4B: 259× more compute; higher MMLU (67.4 vs 60.7) but lower ARC-C (60.9 vs 81.9), GSM8K (78.9 vs 84.5), MATH (22.4 vs 56.2)

HRM-Text beats or matches above on most benchmarks; exceptions are Hellaswag and Winogrande.

**Effective depth (Figures 4, 5):** HRM shows larger KL in deep layers (logit lens), higher block-wise hidden-state delta norms (mean 34.12 vs Transformer 29.65 vs RINS 25.42), lower cosine similarity between adjacent blocks — indicating more active deep computation than looped baselines.

**Contamination:** statistically clean on all benchmarks except DROP at n=13 (n=20 clean); clean-subset DROP 81.1, indicating genuine generalization.

## Applicability

- Architecture research on recurrent-depth LMs at low budget; 16 H100 × 2 days is attainable by small academic labs.
- Pretraining from scratch with only instruction-response data (no raw-text corpus required). Dataset composition detailed in paper Tables 5–6.
- Reasoning-heavy applications where factual breadth is handled by retrieval or external memory. §5.1 explicitly proposes pairing the compact recurrent reasoning core with a knowledge store (Engram conditional memory) as the next step.
- No RL post-training or extended inference-time compute required; strong MATH/GSM8K results obtained purely from architecture + objective.
- Context length 4,096. Inference requires custom PrefixLM attention masking in serving — engineering constraint, not fundamental.

## Novelty

Genuine novelty in co-designing three components together at LM scale:
1. Hierarchical dual-timescale H+L recurrence — more structured than generic looped Transformers or RINS.
2. MagicNorm — new technique bridging PreNorm/PostNorm tradeoffs under TBPTT asymmetry.
3. Task-completion-only pretraining from scratch as the primary (and sole) pretraining stage, not an instruction-tuning phase atop a pretrained base.

Closest prior work: Huginn (recurrent-depth LM), Looped Transformers, RINS, Ouro. Key differentiator: HRM-Text trains from scratch at small budget rather than extending an existing pretrained model with additional depth.

## Reproducibility

Code: `github.com/sapientinc/HRM-Text`. Weights: EMA checkpoint from the single training run, stated as publicly released alongside code. Training cost ($1,472), hardware (16× H100, 46h), and dataset composition (Tables 5–6) fully specified. No independent reproductions observed at capture date.

## Adoption

New paper (captured 2026-05-25). Benchmarked directly against Huginn and Ouro (recurrent-depth peers) and Llama/Qwen/Gemma (dense open models). No independent reproductions or citations yet. The democratic pretraining cost may drive rapid community uptake. The paper's central claim — architecture + objective co-design can substitute for large-scale raw-text pretraining — is a direct positioned challenge to Chinchilla/Kaplan scaling-law orthodoxy; independent validation pending.

## Source

- `raw/research/weekly-2026-05-25/02-hrm-text.md` (arXiv:2605.20613)

## Related

- [[hyperloop-transformers]] — closest structural peer; both use looped/recurrent depth at sub-1B–1B scale; HRM-Text's dual-timescale H+L hierarchy is more structured than mHC loops; Looped Transformer is benchmarked directly against HRM in Table 1 FLOPs-matched comparison.
- [[gram-recursive-reasoning]] — sibling recurrent-reasoning model surfaced the same week; parallel direction in learned recurrent depth for reasoning.
- [[latent-grpo]] — both suppress explicit token-level CoT (HRM-Text strips `<think>` traces; latent-GRPO uses continuous latent reasoning); different mechanisms, same intuition.
- [[nested-learning]] — multi-scale fast/slow computation; HRM's dual-timescale H/L design shares the hierarchical temporal abstraction idea.
- [[ssm-tool-use-length-generalization]] — unresolved interaction: that work argues fixed-memory recurrent architectures cannot handle long-form CoT; HRM-Text relies on internal recurrent compute and strips CoT, leaving open how recurrent depth interacts with CoT-length limits.
- [[memagent]] — external-memory complement to a compact reasoning core; directly relevant to HRM-Text §5.1's Engram forward vision.
