# Watchlist — Identified But Not Captured

Papers and projects referenced in radar-2026-04 summaries that *would* deserve their own page once captured. Each entry: 1–2 sentences on why it matters and what page in this wiki cites it. Promote to a full ingest with `/research` when an entry becomes load-bearing for a follow-on question.

## Architectures & sequence models

- **Mamba-2 (Dao & Gu 2024)** — State-space-model line; fixed-size recurrent state. Cited as a baseline by Titans/Hope, framed as the "fixed-state-suffices" position [[titans-miras]] contests. *(Cited in: titans-miras, nested-learning, eggroll, in-place-ttt.)*
- **Gated DeltaNet** — Linear-recurrent baseline beaten by Titans. *(titans-miras, nested-learning, in-place-ttt.)*
- **DeltaNet / RWKV-7 / GLA / RetNet / Comba** — Modern-RNN / linear-attention family that Hope and In-Place TTT compete against on long-context benchmarks. RWKV-7 is also EGGROLL's workhorse model (constant state + huge inference batch). *(eggroll, nested-learning, in-place-ttt.)*
- **LongMem** — External-memory predecessor to Titans' deep-MLP memory module. *(titans-miras.)*
- **Block Diffusion (Arriola 2025)** — TiDAR's closest prior; mixes causal/bidirectional attention. *(tidar.)*
- **Set Block Decoding (Gat 2025)** — Adjacent block-mixing architecture. *(tidar.)*
- **LLaDA-8B / Dream-7B / Fast-dLLM / SBD** — Diffusion-LLM baselines TiDAR beats. *(tidar.)*
- **EAGLE-1/2/3 / Medusa / DeepSeek-V3 MTP / Apple MTP** — Speculative decoding lineage TiDAR self-speculates against. *(tidar.)*
- **Hyper-Connections (Zhu 2024)** — Original HC paper that mHC stabilizes. *(manifold-constrained-hyper-connections.)*
- **MUDDFormer / DenseFormer / RMT / LAuReL / DeepCrossAttention** — Wider-residual-stream family alongside HC/mHC. *(manifold-constrained-hyper-connections.)*
- **DeepSeek-V3** — MoE backbone mHC inherits (MLA attention, DualPipe schedule). *(manifold-constrained-hyper-connections.)*

## Optimizers

- **Muon (Jordan 2024)** — Newton-Schulz orthogonalization optimizer that NL re-derives as polynomial mapping to an orthogonal coordinate system; M3 builds on it. *(nested-learning.)*
- **AdaMuon** — Muon variant referenced as M3's training-time peer. *(nested-learning.)*
- **Shampoo / Soap** — Second-order optimizers re-decomposed as 2-level associative memories under NL. *(nested-learning.)*

## Self-supervised learning

- **I-JEPA (Assran 2023, CVPR)** — Direct predecessor to LeJEPA; LeJEPA outperforms with smaller model / fewer epochs and removes I-JEPA's predictor + EMA stack. *(lejepa.)*
- **DINO / DINOv2 / DINOv3** — Teacher-student EMA SSL line LeJEPA explicitly removes the heuristics from. Beaten by LeJEPA on Galaxy10 in-domain pretraining. *(lejepa.)*
- **VICReg (Bardes 2021)** — Variance-invariance-covariance SSL; LeJEPA proves it strictly subsumes VICReg as a 4-moment SIGReg degenerate case. *(lejepa.)*
- **BYOL (Grill 2020) / MoCo (He 2020)** — Earlier teacher-student/momentum-contrast SSL that LeJEPA reframes as crutches for collapse. *(lejepa.)*
- **V-JEPA** — Video JEPA variant; natural sibling to LeJEPA in the JEPA family. *(lejepa.)*

## Test-time training / fast weights

- **Sun et al. TTT-RNN (arXiv:2407.04620)** — Foundational modern TTT paper; Titans, Hope, In-Place TTT all cite. Chunk-wise dual-form training procedure used by all three. *(titans-miras, nested-learning, in-place-ttt.)*
- **LaCT (Zhang 2505.23884, "Test-time training done right")** — In-Place TTT's closest peer; large-chunk TTT. *(in-place-ttt.)*
- **Schlag-Irie-Schmidhuber linear-transformers-as-fast-weight-programmers** — Theoretical ancestor to all of TTT. *(in-place-ttt, nested-learning.)*
- **Schmidhuber self-referential weight matrix (1993)** — Earliest self-modifying-architecture lineage; cited by NL. *(nested-learning.)*
- **MAML (Finn 2017)** — Meta-learning baseline NL absorbs as a special case. *(nested-learning.)*

## Self-improving agents

- **Darwin Gödel Machine (DGM, Zhang 2025a, arXiv:2505.22954)** — HGM's primary baseline; greedy-benchmark-score parent selection that HGM replaces with CMP. *(huxley-godel-machine.)*
- **Self-Improving Coding Agent (SICA, Robeyns 2025, arXiv:2504.15228)** — HGM's secondary baseline. *(huxley-godel-machine.)*
- **Gödel Machine (Schmidhuber 2003)** — Theoretical anchor HGM claims to approximate under Assumption 1. *(huxley-godel-machine.)*
- **SWE-bench (Verified + Lite)** — Primary benchmark for HGM and the broader self-improving-agent line. *(huxley-godel-machine.)*
- **SKILL0 (arXiv 2604.*, Apr 2026)** — In-Context RL framework for LLM agents: internalises skills into model parameters via ICRL, enabling autonomous behaviour without external skill descriptions at inference. Parametric counterposition to external-KB agent frameworks (SkillX below). *(weekly-brief 2026-04-22.)*
- **SkillX (Zhejiang U + Ant Digital, Apr 2026)** — Automated framework that builds a plug-and-play skill knowledge base for LLM agents using a hierarchical (planning / functional / atomic) representation. ~10% task-success lift for weaker models. External-KB counterposition to SKILL0's parametric approach. *(weekly-brief 2026-04-22.)*

## Evolution strategies

- **Salimans et al. 2017 OpenES** — Direct ancestor of EGGROLL; full-rank Gaussian ES at modest scale (~1440 population). *(eggroll.)*
- **MeZO (Malladi 2023)** — Closest 2-point ES baseline; EGGROLL argues 2-point methods can't pretrain. *(eggroll.)*
- **Qiu et al. 2025 ("ES at scale: LLM fine-tuning beyond RL")** — Concurrent ES-for-LLMs line. *(eggroll.)*
- **Korotyshova et al. 2025 (ESSA / CMA-ES on LoRA SVD bases)** — Concurrent ES-for-LLMs line. *(eggroll.)*
- **Garbus & Pollack (GECCO 2025)** — Low-rank neuroevolution; nearest neighbour to EGGROLL's perturbation trick. *(eggroll.)*

## Computer vision / 3D

- **3D Gaussian Splatting (Kerbl 2023, SIGGRAPH)** — De-facto representation underpinning SHARP. *(sharp-view-synthesis.)*
- **Depth Pro (Bochkovskii 2025, ICLR)** — Apple's depth backbone used by SHARP (low-res image encoder unfrozen). *(sharp-view-synthesis.)*
- **Splatter Image (Szymanowicz 2024) / Flash3D (2025a)** — Per-pixel Gaussian feedforward predecessors to SHARP. *(sharp-view-synthesis.)*
- **Gen3C / ViewCrafter / ZeroNVS / CAT3D / Wonderland** — Diffusion-side view-synthesis line SHARP positions against. *(sharp-view-synthesis.)*
- **AdaMPI (Han 2022)** — Source of the warp-back trick SHARP inverts for SSFT. *(sharp-view-synthesis.)*
- **Sora-class video foundation models / Genie** — Pure-video-scaling world-model line that Moonlake's hybrid 3D position challenges. *(moonlake-world-models.)*
- **OpenWorldLib (arXiv:2604.04707, Peking/Kuaishou/HKUST/Tsinghua/NUS/SJTU, Apr 2026)** — Unified inference framework + taxonomy for advanced world models (video gen, physics sim, 3D reconstruction, action-conditioned prediction, language-grounded). Explicitly argues text-to-video generators don't qualify as world models — aligns with the 3D-world-model side of [[conflicts/pure-video-vs-3d-world-models]]. *(weekly-brief 2026-04-22.)*

## Benchmarks & evaluation

- **BABILong** — Long-context reasoning benchmark; headline for Titans (>2M) and Hope (10M). *(titans-miras, nested-learning.)*
- **RULER** — Long-context retrieval/reasoning suite; key for Hope and In-Place TTT. *(nested-learning, in-place-ttt.)*

## Infrastructure

- **TileLang (Wang 2025)** — Kernel-fusion framework used for mHC's Sinkhorn-Knopp iteration. *(manifold-constrained-hyper-connections.)*
- **DualPipe** — DeepSeek-V3 pipeline schedule extended for mHC's n-stream cross-stage communication. *(manifold-constrained-hyper-connections.)*
- **YaRN** — RoPE-extension method used for Qwen3 long-context in In-Place TTT runs. *(in-place-ttt.)*
