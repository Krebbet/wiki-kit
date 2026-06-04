---
setup_approved: true
last_reviewed: 2026-05-30
---

# Watchlist — Identified But Not Captured

Papers and projects referenced in radar-2026-04 summaries that *would* deserve their own page once captured. Each entry: 1–2 sentences on why it matters and what page in this wiki cites it. Promote to a full ingest with `/research` when an entry becomes load-bearing for a follow-on question.

## Architectures & sequence models

- **LoopMDM: Looped Diffusion Language Models (arXiv:2605.26106)** — Selectively loops early-middle DiT layers in masked diffusion models; 3.3× fewer training FLOPs to match standard MDM performance, +8.5 pp GSM8K; loop count varied at inference for flexible compute scaling. Extends [[hyperloop-transformers]] cluster to the diffusion-LM domain. *(weekly-brief 2026-06-03.)*
- **Depth-Attention: Cross-Layer Value Mixing (arXiv:2606.05014)** — Lets each attention layer query across keys from all previous layers at the same token position; zero added parameters, <0.01% extra FLOPs; up to +2.3 accuracy across 360M–3B models. *(weekly-brief 2026-06-03.)*
- **"Do Language Models Need Sleep?" (Lee, McLeish, Goldstein, May 2026)** — Offline recurrence / memory consolidation pass for fast-weight Transformers; 'sleep' phase integrates across-context memory outside inference; novel framing of in-context vs. consolidated memory. *(weekly-brief 2026-06-03.)*
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
- **Universal Transformers (Dehghani 2018) / ALBERT (Lan 2019)** — parameter-shared looped-Transformer ancestors that Hyperloop derives from. *(hyperloop-transformers.)*
- **Middle-cycle looped Transformers (Bae 2025; Saunshi 2025) / Geiping 2025 / Prairie 2026** — current loop-as-test-time-compute line; Hyperloop is the latest entrant. *(hyperloop-transformers.)*
- **ELT: Elastic Looped Transformers (arXiv:2604.09168, Apr 2026)** — single looped-transformer training yields elastic family of visual generative models; FID 2.0 on ImageNet at 4× fewer params. Visual-gen branch of the looped-transformer cluster. *(weekly-brief 2026-04-27.)*
- **Loop, Think, & Generalize (arXiv:2604.07822, OSU-NLP, Apr 2026)** — recurrent-depth Transformers enable systematic compositional generalization and depth extrapolation in implicit reasoning. *(weekly-brief 2026-04-27.)*
- **Universal Transformers Need Memory (arXiv:2604.21999, Apr 2026)** — theoretical depth-vs-state trade-offs in adaptive recursive Transformer reasoning. *(weekly-brief 2026-04-27.)*
- **Attention to Mamba: Cross-Architecture Distillation (arXiv:2604.14191, Apr 2026)** — two-stage linearisation+distillation transfers a Transformer to Mamba with near-teacher perplexity (14.11 vs 13.86). *(weekly-brief 2026-04-27.)*
- **S5 / LRU** — prior MIMO SSMs that traded state capacity for training efficiency; Mamba-3's MIMO formulation preserves capacity instead. *(mamba-3.)*
- **H3 / Megalodon** — earlier complex-valued SSMs that were LTI and underperformed Transformers; Mamba-3 is the first to combine selective dynamics with complex state. *(mamba-3.)*
- **MoDr: Mixture-of-Depth-Recurrent Transformers (ICLR 2026 poster)** — LoRA-based multi-branch dynamic routing over Huginn's looped-Transformer depth layers; auxiliary-loss-free load balancing. +7.2% over Huginn on math, +21.2% on commonsense. First MoE-style method applied *within* the loop-depth dimension; extends the [[hyperloop-transformers]] cluster. *(weekly-brief 2026-05-04.)*
- **SDVG: Speculative Decoding for Autoregressive Video Generation (arXiv:2604.17397, Apr 2026)** — training-free quality-based routing replaces token-level verification for block-AR video diffusion; 1.59× speedup at 98.1% quality, 2.09× at 95.7%. First speculative decoding application to AR video. *(weekly-brief 2026-05-04.)*
- **FLUID: Continuous-Time Hyperconnected Sparse Transformer (arXiv:2605.04421, May 2026)** — Rewrites attention logits as solutions to a linear ODE with input-dependent nonlinear recurrent gates ("Liquid Attention"); Liquid Hyper-Connection replaces residuals to resolve seesaw effect. Up to 47% gain across irregular time-series / long-range forecasting / autonomous-vehicle control. Theoretical unification of attention and CT-RNNs. *(weekly-brief 2026-05-11.)*
- **Joint Latent Diffusion LM (arXiv:2605.07933, May 2026)** — Twin paper to [[coladlm]]: jointly trains encoder + DiT + decoder for diffusion LMs (vs frozen-latent baselines) with MSE decoder loss, diffusion-to-encoder warmup, adaptive timestep sampling, decoder-input noise. 2–13× faster generation. Constitutes a cluster with ColaDLM and Break the Block. *(weekly-brief 2026-05-11.)*
- **Break the Block (arXiv:2605.02263, May 2026)** — RL post-training for diffusion LLMs: applies monotonic-entropy-descent reward to dynamic block sizing; observation that correct reasoning has monotonically descending block entropy. Plug-and-play; consistent gains over fixed-size block baselines. Companion to [[coladlm]] / Joint Latent DLM on the diffusion-LM RL line. *(weekly-brief 2026-05-11.)*
- **Transformers are Inherently Succinct (ICLR 2026 Outstanding Paper, Bergsträßer et al., Apr 2026)** — Award-winning theoretical result: Transformers encode concepts more succinctly than RNNs under a formal representational-efficiency framework ("succinctness"). Provides theoretical grounding for the architectural advantage. *(weekly-brief 2026-05-11.)*
- **Mean Mode Screaming: MV-Split Residuals for 1000-Layer Diffusion Transformers (arXiv:2605.06169, May 2026)** — Names a previously undescribed ultra-deep-DiT collapse mode ("mean mode screaming") and fixes it with mean–variance split residuals (separately-gained centered residual + leaky trunk-mean replacement), demonstrating a trainable 1000-layer DiT. Project page with interactive visualizations. *(weekly-brief 2026-05-18.)*
- **Equilibrium Reasoners: Learning Attractors Enables Scalable Reasoning (arXiv:2605.21488, CMU, May 2026)** — Frames reasoning as learning task-conditioned fixed-point attractors; unrolling to ~40k-equivalent layers via latent fixed-point iteration reaches >99% on Sudoku-Extreme. Latent depth-scaling sibling to [[gram-recursive-reasoning]] / [[hrm-text]] and the looped-transformer line [[hyperloop-transformers]]. *(weekly-brief 2026-05-25.)*
- **Full Attention Strikes Back (arXiv:2605.16928, May 2026)** — Full-attention LLMs are intrinsically sparse (~15% retrieval heads); RTPurbo converts full→sparse attention in <100 training steps for 9.36× prefill speedup at 1M context. Efficiency counterpart to [[triattention]] / [[neural-garbage-collection]]. *(weekly-brief 2026-05-25.)*
- **ConvexTok: Tokenisation via Convex Relaxations (arXiv:2605.22821, May 2026)** — Casts BPE/Unigram tokenizer construction as an integer program solved via LP relaxation; within 1% of the theoretical bits-per-byte optimum and improves downstream LM perplexity. Rare principled-tokenization entry. *(weekly-brief 2026-05-25.)*

## Optimizers

- **Polar Express: Optimal Matrix Sign Methods and Muon Algorithm (ICLR 2026 Honorable Mention, Amsel et al., Apr 2026)** — Approximation theory yields optimal polynomials for the polar decomposition at the core of Muon; GPU-first low-precision design. Practical optimizer-theory contribution. *(weekly-brief 2026-05-11.)*

- **Muon (Jordan 2024)** — Newton-Schulz orthogonalization optimizer that NL re-derives as polynomial mapping to an orthogonal coordinate system; M3 builds on it. *(nested-learning.)*
- **AdaMuon** — Muon variant referenced as M3's training-time peer. *(nested-learning.)*
- **Shampoo / Soap** — Second-order optimizers re-decomposed as 2-level associative memories under NL. *(nested-learning.)*
- **MatryoshkaLoRA (arXiv:2605.07850, May 2026)** — Nested-rank LoRA: a fixed diagonal matrix P inserted between adapters embeds gradient information at all sub-ranks simultaneously, so one trained adapter is accurate at every truncation rank; subsumes LoRA and DyLoRA as special cases; introduces the AURAC metric. Practical PEFT rank-selection method. *(weekly-brief 2026-05-18.)*
- **Rethinking Muon Beyond Pretraining (arXiv:2605.19282, May 2026)** — Identifies regimes where the Muon optimizer fails post-pretraining (VLA fine-tuning, RLVR) and proposes a high-pass spectral correction. Extends the Muon-theory line (Polar Express). *(arXiv ID unverified at scan time — confirm before promotion.)* *(weekly-brief 2026-05-25.)*

## RL / post-training

- **GURU: Revisiting RL for LLM Reasoning from a Cross-Domain Perspective (arXiv:2506.14965, ACL 2026)** — 92K verifiable RL examples across 6 domains (Math, Code, Science, Logic, Simulation, Tabular); open dataset release; challenges assumption that RLVR only elicits pre-trained knowledge. Trending on HF Papers this week. *(weekly-brief 2026-06-03.)*
- **Faster Synchronous On-Policy RL via Straggler-Aware Group Sizing (arXiv:2606.02218)** — Addresses DAPO/GRPO training wall-clock bottleneck caused by slow rollout stragglers; adaptive group sizing keeps synchronous on-policy competitive with async approaches. *(weekly-brief 2026-06-03.)*
- **MemTrain: Self-Supervised Memory Agent Training (arXiv:2606.03197)** — GRPO-trained memory agents on unlabeled Wikipedia via masked entity reconstruction + memory recall proxy tasks; +17.67 pp over task-specific post-training on long-text QA without labeled data. *(weekly-brief 2026-06-03.)*
- **MHGPO: Multi-Agent Heterogeneous Group Policy Optimization (arXiv:2506.02718, ACL 2026)** — Estimates relative advantages across heterogeneous agent-group rollouts; shifts optimization from per-agent to global system success; outperforms critic-network baselines at lower compute. *(weekly-brief 2026-06-03.)*
- **DAPO (Yu 2025) / DCPO (Yang 2025) / SSPO (Yang 2025)** — Token-level reweighting fixes for GRPO; DFPO unifies the underlying failure mode (gradient non-cancellation) and proposes simpler stop-gradient transforms. *(token-gradient-cancellation.)*
- **TEPO: Token-Level Policy Optimization (arXiv:2604.12736)** — Sequence-level likelihood bridge between group reward and per-token KL mask; stabilizes GRPO. Adjacent to RLSD and DFPO. *(weekly-brief 2026-04-27.)*
- **GSPO (Zheng 2025)** — Sequence-coupled multiplicative-weight GRPO variant that DFPO identifies as structurally non-cancelling. *(token-gradient-cancellation.)*
- **MIPROv2 (Opsahl-Ong 2024)** — Joint instruction + few-shot prompt optimizer; GEPA's direct predecessor and headline baseline. *(gepa-reflective-prompt-evolution.)*
- **TextGrad / APO / Trace / OptoPrime** — prior prompt-optimization line that GEPA's reflective + Pareto-illumination + system-aware-merge combination beats. *(gepa-reflective-prompt-evolution.)*
- **MAP-Elites / QD search (Mouret & Clune 2015)** — Quality-Diversity search lineage GEPA's Pareto-illumination adapts. *(gepa-reflective-prompt-evolution.)*
- **DeepSeek Sparse Attention** — Closest prior to NGC: separate KL-trained KV-eviction indexer with detached gradients; NGC unifies eviction and token gradients under one reward. *(neural-garbage-collection.)*
- **SnapKV / KeyDiff / KNorm / StreamingLLM / Breadcrumbs / Memento** — Inference-time KV-eviction baselines that NGC's RL-trained eviction beats by 2–3×. *(neural-garbage-collection.)*
- **ml-intern (HF, Apr 2026)** — open-source agent automating LLM post-training: browses arXiv, runs GRPO fine-tuning; pushed Qwen3-1.7B GPQA 8.5% → 32% unattended. Tooling rather than method. *(weekly-brief 2026-04-27.)*
- **LEPO: Latent Reasoning Policy Optimization (arXiv:2604.17892, ACL 2026)** — RL on continuous latent reasoning via Gumbel-Softmax stochasticity injection; two-stage rollout/optimization with unified gradient for latent + discrete tokens. Sibling to [[latent-grpo]] — both are RL-for-latent-reasoning from the same week. *(weekly-brief 2026-05-04.)*
- **Thinking Without Words (arXiv:2604.22709, Apr 2026)** — discrete abstract latent tokens (reserved vocabulary) as scratchpad; policy-iteration warm-up alternates CoT bottlenecking + self-distillation. Shorter than continuous CoT, stronger than continuous-latent approaches. Discrete-token sibling to [[latent-grpo]] / LEPO. *(weekly-brief 2026-05-04.)*
- **ThinkPRM (arXiv:2504.16828)** — generative verbalized step-wise PRM that verifies each CoT step by generating an extended verification chain; data-efficient (no step-level supervision needed beyond outcome labels). Trending alongside [[neural-garbage-collection]] and 2604.22981. *(weekly-brief 2026-05-04.)*
- **Reward Models Are Secretly Value Functions (arXiv:2604.22981, Apr 2026)** — reframes ORM training as discarding intermediate-position information; proposes temporally coherent reward signal across token positions. Complements [[rlsd-self-distilled-rlvr]] and [[neural-garbage-collection]] (both exploit intermediate-token signals). *(weekly-brief 2026-05-04.)*
- **Accelerating RL Post-Training Rollouts via System-Integrated Speculative Decoding (arXiv:2604.26779, Apr 2026)** — practical NeMo-RL + vLLM implementation integrating MTP heads / external drafters / Eagle3 into RL rollout generation, sync + async pipelines. Closes the systems gap for everyone scaling GRPO. *(weekly-brief 2026-05-04.)*
- **IOP-GSPO: Internalizing Outcome Supervision into Process Supervision (arXiv:2605.05226, May 2026)** — Three-step pipeline that converts outcome supervision into token-level signals by selecting repairable failures, model-self-generating repair, and feeding back via truncation gating. +4.9–6.9% over GSPO; beats exogenous process supervision. Sits in the credit-assignment family alongside [[token-gradient-cancellation]] / [[agentflow]] Flow-GRPO. *(weekly-brief 2026-05-11.)*
- **UCPO: Uniform-Correct Policy Optimization (arXiv:2605.00365, May 2026)** — Adds conditional uniformity penalty over correct-solution distribution to GRPO; identifies mode collapse as a *structural* property of GRPO objectives, not a training artifact. +10% AIME24 Pass@64; 45% higher equation-level diversity in correct set across 1.5B–7B. *(weekly-brief 2026-05-11.)*
- **ResRL: Negative-Sample Projection Residual RL (arXiv:2605.00380, May 2026)** — SVD-based projection of negative-token hidden representations onto low-rank positive subspace; conservative modulation of negative gradients via projection residuals. +9.4% Avg@16, +7.0% Pass@128 over NSR; SoTA across 12 benchmarks. *(weekly-brief 2026-05-11.)*
- **RAO: Recursive Agent Optimization (arXiv:2605.06639, May 2026)** — RL trains agents to spawn recursive sub-agent copies of themselves and delegate sub-tasks; 95% success on context-constrained tasks that exceed model context window; faster wall-clock than single-agent baselines. Divide-and-conquer inference scaling that complements [[agentflow]] and [[memagent]]. *(weekly-brief 2026-05-11.)*
- **Tool Calling is Linearly Readable and Steerable (arXiv:2605.07990, May 2026)** — Mechanistic interp: tool selection is linearly encoded in activations *before* generation across 12 models (270M–27B); adding mean-difference vectors switches tool choice at 77–100% accuracy. Even untrained base models encode correct tool internally at 69–82%. *(weekly-brief 2026-05-11.)*
- **SU-01: Gold-Medal Olympiad Reasoning via Simple Unified Scaling (arXiv:2605.13301, May 2026)** — 30B-A3B model reaching IMO-2025 / IPhO-2025 gold-medal level via a three-stage pipeline: reverse-perplexity SFT curriculum → two-stage RL (verifiable then proof-level) → test-time scaling; sustains 100K-token reasoning trajectories. High-visibility reasoning milestone; code released. *(weekly-brief 2026-05-18.)*
- **SDAR: Self-Distilled Agentic RL (arXiv:2605.15155, May 2026)** — On-policy self-distillation for multi-turn agents: a teacher branch with privileged context provides dense token-level guidance, gated via a sigmoid auxiliary objective; +9.4% success on ALFWorld. Same OPD family as [[rlsd-self-distilled-rlvr]]; code promised, not yet released. *(weekly-brief 2026-05-18.)*
- **Geometry Conflict: Explaining & Controlling Forgetting in Continual Post-Training (arXiv:2605.09608, May 2026)** — Represents each post-training task by its parameter-update vector and studies the covariance geometry; derives conditions for capability transfer vs interference and a geometric-compatibility rule for controllable update integration. Timely given the volume of continual-post-training work. *(weekly-brief 2026-05-18.)*
- **Vector Policy Optimization (arXiv:2605.22817, May 2026)** — Drop-in GRPO replacement that trains on vector-valued rewards to produce *diverse* solutions, improving best-of-N and evolutionary/test-time-search budgets. alphaXiv #1 this week; complements the diversity-preserving-RL line (UCPO) and [[token-gradient-cancellation]]. *(weekly-brief 2026-05-25.)*
- **Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented Agents (arXiv:2605.21768, May 2026)** — LoGo-GRPO rerolls from shared memory checkpoints to fix fairness in multi-session RL; joint memory-formation + memory-evolution training with a progressive curriculum. Credit-assignment cousin of [[delta-token-credit]] / [[agentflow]] for [[memagent]]-style agents. *(weekly-brief 2026-05-25.)*
- **HINT-SD: Targeted Hindsight Self-Distillation for Long-Horizon Agents (arXiv:2605.17873, May 2026)** — Sparse failure-targeted self-distillation: full-trajectory hindsight isolates causal failure actions and avoids supervising successful/neutral turns. OPD-family sibling of [[anti-self-distillation]] / [[rlsd-self-distilled-rlvr]] / SDAR. *(weekly-brief 2026-05-25.)*
- **GoLongRL: Capability-Oriented Long-Context RL with Multitask Alignment (arXiv:2605.19577, May 2026)** — RL framework extending LLM context via multitask alignment without length-generalization degradation. Adjacent to the long-context cluster [[memagent]] / [[delta-mem]]. *(weekly-brief 2026-05-25.)*

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

- **BES: Self-Improving LMs with Bidirectional Evolutionary Search (arXiv:2605.28814, Harvard/MIT)** — Couples forward evolutionary search (recombining partial trajectories) with backward goal decomposition into checkable subgoals; provides dense intermediate feedback; +3.8% on multi-hop reasoning for Llama-3.1-8B-Instruct. *(weekly-brief 2026-06-03.)*
- **GrepSeek: Training Search Agents for Direct Corpus Interaction (arXiv:2605.29307, UMass Amherst)** — Trains compact LLMs to search corpora via shell commands (grep/find) rather than index-based retrieval; 7.6× acceleration via parallel execution; competitive with RAG on 7 QA benchmarks. *(weekly-brief 2026-06-03.)*
- **PEFT Scaling: Towards Million Personal Models of Trillion Parameters (arXiv:2606.02437)** — Reframes LoRA-style adapters not as a budget substitute but as persistent personal model state; argues PEFT can scale to millions of distinct personalized instances on shared trillion-parameter foundations. *(weekly-brief 2026-06-03.)*
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
- **Darwin Family: Evolutionary Model Merging (arXiv:2605.14386, May 2026)** — Evolutionary search over model-merge recipes ("Darwin Family"); lower-confidence capture (arXiv ID seen in HF list, details unconfirmed at scan time — flagged for follow-up lookup before promotion). *(weekly-brief 2026-05-18.)*

## Computer vision / 3D

- **3D Gaussian Splatting (Kerbl 2023, SIGGRAPH)** — De-facto representation underpinning SHARP. *(sharp-view-synthesis.)*
- **Depth Pro (Bochkovskii 2025, ICLR)** — Apple's depth backbone used by SHARP (low-res image encoder unfrozen). *(sharp-view-synthesis.)*
- **In Depth We Trust (arXiv:2604.05715, Apr 2026)** — Reliable monocular-depth supervision for 3DGS; addresses scale ambiguity + multi-view inconsistency. *(weekly-brief 2026-04-27.)*
- **World-R1 (arXiv:2604.24764, Apr 2026)** — Microsoft Research + Zhejiang U. Flow-GRPO + 3D-aware rewards from pretrained 3D foundation models, applied to Wan 2.1 video diffusion to enforce geometric consistency. RL-in-the-loop for video generation; training-free at inference. Adjacent to [[conflicts/pure-video-vs-3d-world-models]] (3D-side counter-camp). *(weekly-brief 2026-05-04.)*
- **PERSIST (arXiv:2603.03482, Microsoft Research)** — Decomposes world model into world-frame 3D evolution model + camera model + world-to-pixel renderer. Persistent 3D state improves spatial memory, temporal coherence, out-of-view environment tracking. More explicit 3D decomposition than [[moonlake-world-models]]; extends [[conflicts/pure-video-vs-3d-world-models]]. *(weekly-brief 2026-05-04.)*
- **Tuna-2 (Meta FAIR, arXiv:2604.24763, Apr 2026)** — encoder-free multimodal: a single Transformer decoder processes raw pixel embeddings for both perception and generation. Companion to [[vision-banana]] on the generation-as-perception theme — opposite direction (remove encoders entirely vs instruction-tune a generator). *(weekly-brief 2026-05-04.)*
- **Splatter Image (Szymanowicz 2024) / Flash3D (2025a)** — Per-pixel Gaussian feedforward predecessors to SHARP. *(sharp-view-synthesis.)*
- **Gen3C / ViewCrafter / ZeroNVS / CAT3D / Wonderland** — Diffusion-side view-synthesis line SHARP positions against. *(sharp-view-synthesis.)*
- **AdaMPI (Han 2022)** — Source of the warp-back trick SHARP inverts for SSFT. *(sharp-view-synthesis.)*
- **Sora-class video foundation models / Genie** — Pure-video-scaling world-model line that Moonlake's hybrid 3D position challenges. *(moonlake-world-models.)*
- **OpenWorldLib (arXiv:2604.04707, Peking/Kuaishou/HKUST/Tsinghua/NUS/SJTU, Apr 2026)** — Unified inference framework + taxonomy for advanced world models (video gen, physics sim, 3D reconstruction, action-conditioned prediction, language-grounded). Explicitly argues text-to-video generators don't qualify as world models — aligns with the 3D-world-model side of [[conflicts/pure-video-vs-3d-world-models]]. *(weekly-brief 2026-04-22.)*
- **AnyFlow: Any-Step Video Diffusion via On-Policy Flow Map Distillation (arXiv:2605.13724, NVlabs, May 2026)** — Replaces endpoint-consistency distillation with flow-map transition learning over arbitrary time intervals (Flow Map Backward Simulation); first any-step distillation for video that *scales* rather than degrades with more steps. Code released. *(weekly-brief 2026-05-18.)*
- **SANA-WM: Minute-Scale World Modeling with Hybrid Linear DiT (arXiv:2605.15178, NVIDIA, May 2026)** — 2.6B world model generating 60s 720p video on a single GPU: hybrid linear attention (GDN frame-wise + softmax), dual-branch 6-DoF camera control, two-stage pipeline with long-video refiner; trains in 15 days on 64×H100. Relevant to [[conflicts/pure-video-vs-3d-world-models]]. *(weekly-brief 2026-05-18.)*
- **Causal Forcing++ (arXiv:2605.15141, THU-ML, May 2026)** — Real-time interactive video generation at 1–2 steps: causal consistency distillation uses a single online teacher step (not precomputed ODE trajectories) for init; −50% first-frame latency, 4× cheaper Stage-2 training; extends to action-conditioned world models. Follow-up to ICML-2026 Causal Forcing. *(weekly-brief 2026-05-18.)*
- **WorldKV: Efficient World Memory with World Retrieval and Compression (arXiv:2605.22718, May 2026)** — Training-free KV-cache framework for video world models: camera/action-aware retrieval + key-similarity token pruning for 2× throughput at full-KV fidelity. Relevant to [[conflicts/pure-video-vs-3d-world-models]] and the KV-compression line. *(weekly-brief 2026-05-25.)*

## Benchmarks & evaluation

- **BABILong** — Long-context reasoning benchmark; headline for Titans (>2M) and Hope (10M). *(titans-miras, nested-learning.)*
- **RULER** — Long-context retrieval/reasoning suite; key for Hope and In-Place TTT. *(nested-learning, in-place-ttt.)*

## Infrastructure

- **TileLang (Wang 2025)** — Kernel-fusion framework used for mHC's Sinkhorn-Knopp iteration. *(manifold-constrained-hyper-connections.)*
- **DualPipe** — DeepSeek-V3 pipeline schedule extended for mHC's n-stream cross-stage communication. *(manifold-constrained-hyper-connections.)*
- **YaRN** — RoPE-extension method used for Qwen3 long-context in In-Place TTT runs. *(in-place-ttt.)*
- **MinT: Managed Infrastructure for Training & Serving Millions of LLMs (arXiv:2605.13779, May 2026)** — LoRA-as-a-service at trillion-parameter scale: base model kept resident while LoRA adapter revisions cycle through rollout/update/export/evaluation/serving/rollback; validated beyond 1T total params incl. MLA + DSA attention paths; rank-1 adapters <1% of base size. Production-infra gap academic RL work doesn't cover; code closed. *(weekly-brief 2026-05-18.)*
- **OScaR: Occam's Razor for Extreme KV Cache Quantization (arXiv:2605.19660, May 2026)** — Canalized Rotation + Omni-Token Scaling for near-lossless INT2 KV quantization; 5.3× memory reduction, 4.1× throughput. KV-efficiency complement to [[triattention]] and WorldKV. *(weekly-brief 2026-05-25.)*
