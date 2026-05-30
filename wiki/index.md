# Wiki Index

Catalog of all pages in this wiki. Updated on every ingest.

Scope: methods for integrating heterogeneous architecture blocks (CNNs, GNNs, SSMs, etc.), repetitive/looped computation, and routing mechanisms inside transformer networks — building toward an experimental plan around block-level specialization.

---

## Overview

| Page | Summary |
|---|---|
| [[block-operations-and-modular-routing]] | Splits activation tensors into uniform blocks; Modular Representation-Preserving Mappings (SMFR) as FFN replacement. Perfect compositional generalization on synthetic algorithmic tasks where FFNs + Transformers fail; soft routing beats hard (Gumbel). Synthetic, small-scale evidence only. |
| [[brain-inspired-modularity]] | Cognitive and neuroscience framings of modularity from papers 03 and 10: the Symbol Binding Problem / superposition-catastrophe motivation (inspiration-only) vs. MICRO's four brain-network-aligned experts validated with neuroscience localizers (direct-transfer). Covers cross-cutting agreement on per-block routing, the seeded-vs-emergent specialisation axis, and open questions about what genuine direct-transfer would require. |
| [[expert-choice-routing]] | Inverts MoE routing so experts pick tokens (not vice versa), guaranteeing load balance and per-token variable compute. >2× training speedup over Switch/GShard at same quality. Specialization claim is performance-inferred, not mechanistically probed. |
| [[looped-language-models]] | Ouro: weight-shared recurrent transformer blocks with entropy-regularized adaptive exit; 1.4B params / 7.7T tokens; 2–3× parameter efficiency over dense baselines. Looping enhances knowledge *manipulation* not *storage*. Practical failure modes: RL alignment broken, KV cache reuse catastrophic, gradient oscillations >4 recurrent steps. |
| [[looped-transformers-and-reasoning]] | k-layer transformer looped L times nearly matches kL-layer non-looped on reasoning at 1B scale, with far fewer parameters. Looped = implicit chain-of-thought. Tradeoff: worse perplexity at iso-FLOP but better reasoning. |
| [[mamba-2-and-ssm-hybrids]] | Structured State Space Duality (SSD) proves SSMs and linear-attention variants are dual forms of the same structured-matrix computation; Mamba-2 is 2–8× faster than Mamba. NVIDIA's 8B / 3.5T-token controlled study finds a Mamba-2/attention/MLP hybrid (~8–10% attention) beats a matched Transformer on all 12 standard tasks and most long-context tasks. Known SSM failure modes: copying, in-context learning gaps, prompt sensitivity. |
| [[mixture-of-cognitive-reasoners-micro]] | MICRO: post-training clone of each transformer block into 4 brain-network-aligned experts (Language / Logic / Social / World) via a 3-stage curriculum. Matches or beats MoE + dense baselines on reasoning; r=0.7 neuroscience-localizer correlation. Strongest positive evidence in this batch for learned-routing specialization. |
| [[mixture-of-depths]] | Tokens learn to route around full attention+MLP blocks per layer via top-k expert-choice routing; equal or better loss than isoFLOP vanilla at 50% per-forward-pass FLOPs and 66% faster stepping. Routing analysis shows harder-to-predict tokens engage more blocks. |
| [[modular-deep-learning-survey]] | Four-axis taxonomy of modular deep learning (computation / routing / aggregation / training); argues explicit modularity addresses negative interference, catastrophic forgetting, and systematic-generalisation failure. Primary contrarian voice on whether learned routing specializes (citing Mittal, Muqeeth, Lewis). |
| [[routing-mechanisms-in-modular-networks]] | Aux / synthesis taxonomy page applying the wiki's three-axis routing characterization (soft-vs-hard, dispatch signal, specialization origin) across papers 01, 02, 03, 09, 10. Cross-cutting observations on expert-choice convergence, hard-vs-soft-by-granularity, and specialization-emergence-vs-enforcement. |
| [[thesis-architecture-sketch]] | Design synthesis: composes Ouro-style looped weight-shared recurrence (with middle-looping) + MICRO-style MOB routing with curriculum-seeded specialization + Ouro entropy-regularized two-stage exit gate into the thesis's looped-routed-specialized architecture. Lists considerations, painpoints, and the prioritized open research questions that block the design. |
| [[universal-transformer]] | 2018 foundational weight-tied recurrent-depth Transformer with per-position Adaptive Computation Time (ACT) halting; Turing-complete; beats vanilla on algorithmic + LAMBADA tasks. Superseded empirically by looped-transformers-and-reasoning and looped-language-models but remains the conceptual anchor for the looped lineage. |

---

## Open conflicts

| Conflict | Question | Status |
|---|---|---|
| [[learned-routing-specialization]] | Does learned routing produce genuine functional specialization, or reliably underspecialize? | open |
| [[looped-vs-depth-scaling]] | Does architectural looping trade perplexity for reasoning, or overcome the perplexity penalty at scale? | open |

---
