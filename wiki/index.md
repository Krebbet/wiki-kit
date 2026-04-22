# Wiki Index

AI research and engineering trends: LLM/SLM training, fine-tuning, RL and reward design, novel architectures, computer vision, and evolutionary approaches to LLMs.

Catalog of all pages in this wiki. Updated on every ingest.

---

## Overview & meta

| Page | Summary |
|---|---|
| [[reference-sources]] | Trend radar — curated X handles, awesome-lists, podcasts, subreddits, and Discord communities the wiki watches. Consulted by `/lint`. |
| [[watchlist]] | Papers and projects identified during ingests but not yet captured. 1–2 sentences each, with the wiki page that referenced them. Promote to `/research` when they become load-bearing. |

---

## Architectures & sequence models

| Page | Summary |
|---|---|
| [[titans-miras]] | Google Research Titans (deep-MLP long-term memory module with gradient-driven "surprise" updates) + MIRAS (taxonomy of sequence models as associative-memory optimizers). Beats GPT-4 on BABILong claim. |
| [[nested-learning]] | Behrouz et al. NeurIPS 2025: unifying paradigm casting architectures and optimizers as nested associative-memory systems. Hope = self-modifying Titans + Continuum Memory System; M3 = multi-scale Muon. Holds 10M context on BABILong. |
| [[in-place-ttt]] | ByteDance/PKU Apr-2026: drop-in TTT for pretrained LLMs by repurposing gated-MLP `W_down` as fast weights with NTP-aligned target. Qwen3-4B RULER-64k 74.3 → 78.7 with no architecture change. |
| [[test-time-training]] | Cluster page comparing the three TTT-flavoured sources (Titans, Hope, In-Place TTT) on host, objective, drop-in vs from-scratch, and forgetting mechanism. |
| [[tidar]] | NVIDIA single-model hybrid: drafts tokens via masked diffusion, AR-verifies in same forward pass. 4.71×–5.91× throughput vs Qwen base AR; beats EAGLE-3 on measured T/s. |
| [[manifold-constrained-hyper-connections]] | DeepSeek mHC: stabilizes Hyper-Connections by projecting residual-mixing matrix onto Birkhoff polytope via Sinkhorn-Knopp. Composite-mapping Amax 3000 → 1.6 at 27B; +2.1 BBH, +2.3 DROP vs HC. |

## Training & optimization

| Page | Summary |
|---|---|
| [[eggroll]] | Oxford/MILA/NVIDIA Evolution Strategies at hyperscale: low-rank LoRA-style perturbations + counter-based PRNG → ~100× ES throughput. Beats GRPO on 14B RWKV-7 reasoning where GRPO is infeasible (Adam state). Pure-int8 RNN pretraining at population 2^20. |

## Self-supervised learning

| Page | Summary |
|---|---|
| [[lejepa]] | Balestriero & LeCun: JEPA training objective enforcing isotropic-Gaussian embeddings via sliced characteristic-function regularizer (SIGReg). Removes stop-gradient, EMA teacher, predictor, register tokens. ViT-H/14 79% IN-1K linear probe. ~50 LOC. |

## Self-improving agents

| Page | Summary |
|---|---|
| [[huxley-godel-machine]] | KAUST/Schmidhuber HGM: tree-search self-improving coding agent that scores parents by *clade* (descendant-aggregated) success rate (CMP) instead of own benchmark score. Approximates Gödel Machine under stated assumptions. SWE-bench Verified 61.4%, top-10. |

## Computer vision / 3D

| Page | Summary |
|---|---|
| [[sharp-view-synthesis]] | Apple SHARP: feedforward regression of 1.2M-Gaussian 3DGS scene from one RGB image in <1s on A100. Beats diffusion baselines (Gen3C, ViewCrafter) by 21–43% perceptual metrics, 1000× faster. Apple ml-sharp repo. |
| [[moonlake-world-models]] | Moonlake position post: pure 2D video diffusion cannot yield interactive world simulators; proposes hybrid pipeline binding *neutral information-free latent codes* to coarse 3D mesh patches as scaffolds for video diffusion. Position only — no benchmarks. |

---

## Conflicts (open positions)

| Page | Summary |
|---|---|
| [[conflicts/long-context-attention-vs-recurrent-memory]] | Titans/Hope claim recurrent memory beats GPT-4-class attention at extreme context. Awaiting attention-side counter-source. |
| [[conflicts/fixed-state-ssm-long-context]] | Titans/Hope claim fixed-state SSMs (Mamba-2) cannot capture rich long-sequence info. Awaiting SSM-side defence. |
| [[conflicts/grpo-vs-evolution-strategies]] | EGGROLL claims ES matches/beats GRPO at scale; only feasible at 14B+. Awaiting GRPO-orthodoxy primary source. |
| [[conflicts/icl-emergent-vs-nested-levels]] | NL claims ICL is a direct consequence of nested levels, not emergent. Contradicts Brown 2020 / Wei 2022 framing. |
| [[conflicts/ttt-distinct-vs-parametric-icl]] | NL subsumes TTT under parametric ICL; In-Place TTT treats TTT as a distinct mechanism complementing attention. Internal cluster tension. |
| [[conflicts/regression-vs-diffusion-view-synthesis]] | SHARP claims feedforward regression Pareto-dominates diffusion for nearby-view single-image synthesis. Awaiting diffusion-side defence (Gen3C, etc.). |
| [[conflicts/pure-video-vs-3d-world-models]] | Moonlake claims pure video diffusion cannot yield interactive world simulators. Awaiting Sora-class pure-scaling defence. |

---
