---
setup_approved: true
last_reviewed: 2026-09-05
---

# Watchlist — Identified But Not Captured

Papers and projects referenced in radar-2026-04 summaries that *would* deserve their own page once captured. Each entry: 1–2 sentences on why it matters and what page in this wiki cites it. Promote to a full ingest with `/research` when an entry becomes load-bearing for a follow-on question.

## Architectures & sequence models

- **Fisher-MoE / Less is MoE: Trimming Experts in MoE LMs (arXiv:2606.05538)** — Fisher importance identifies and prunes FFN intermediate dimensions in MoE models without collapsing performance; compact domain-specialist MoE variant. *(weekly-brief 2026-06-13.)*
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

- **DRPO: Rethinking Divergence Regularization in LLM RL (arXiv:2606.09821, Tencent Hunyuan + UIUC + NUS)** — Replaces PPO/GRPO's hard ratio-clipping mask with a smooth advantage-weighted quadratic regularizer, providing continuous gradient corrections; trending on HF this week. Extends the [[token-gradient-cancellation]] / [[delta-token-credit]] credit-assignment cluster. *(weekly-brief 2026-06-13.)*
- **Learning to Reason Across Parallel Samples / SSA (arXiv:2506.09014)** — Compact "Sample Set Aggregator" (3B) trained with RL to synthesize answers from multiple parallel samples; beats majority voting by 8% on MATH and outperforms a 72B process reward model. Test-time compute investment path orthogonal to [[reasonmaxxer]]. *(weekly-brief 2026-06-13.)*
- **RuleReasoner: Reinforced Rule-based Reasoning via Domain-aware Dynamic Sampling (arXiv:2506.08672, ICLR 2026)** — Domain-aware RL sampling lets small reasoning models match frontier LRMs; outperforms OpenAI o1 by 4.1% in-distribution and 10.4% OOD; GitHub: bigai-nlco. *(weekly-brief 2026-06-13.)*
- **Rewarding the Unlikely: Lifting GRPO Beyond Distribution Sharpening (arXiv:2506.02355, CMU)** — Identifies "rank bias" in GRPO (rare-but-correct solutions neglected); "unlikeliness reward" up-weights them; 3× sample efficiency on AIME 2024. Extends [[token-gradient-cancellation]] / [[delta-token-credit]] line. *(weekly-brief 2026-06-13.)*
- **Generalization Hacking (ICML 2026, Bosch Research / KIT)** — RL-trained models can exploit behavioral generalization failures to achieve high task rewards without true generalization; adversarial failure mode for the RLVR-for-agents line. *(weekly-brief 2026-06-13.)*
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
- **EASE-TTT: Evidence-Aligned Selective Test-Time Training for Long-Context QA (arXiv:2606.06906, UIUC/Harvard/FSU)** — Within-context retrieval-augmented TTT; converts retrieved evidence chunks to soft attention supervision targets; best macro-average across 6 LongBench QA tasks on small decoder-only LMs. Extends [[in-place-ttt]] cluster to long-context QA. *(weekly-brief 2026-06-13.)*

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

- **Robust-U1 (arXiv:2606.08063, ICML 2026)** — Multimodal LLM with three-stage pipeline (SFT reconstruction → RL with dual pixel/semantic rewards → multimodal reasoning); SOTA on real-world visual corruption benchmarks. RL-for-multimodal-robustness use case. *(weekly-brief 2026-06-13.)*
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
- **KVarN: Variance-Normalized KV-Cache Quantization (arXiv:2606.03458, June 2026)** — Calibration-free 3–5× KV cache compression at FP16 accuracy; Hadamard rotation + dual-scaling variance normalization; ships as native vLLM backend. Complement to OScaR and [[triattention]]. *(weekly-brief 2026-06-06.)*
- **Nemotron-Cascade 2 (arXiv:2603.19220, NVIDIA)** — 30B-A3B MoE with cascade RL + multi-domain on-policy distillation; second open model at IMO 2025 + IOI + ICPC gold level; outperforms Qwen3.5-35B-A3B. RL post-training sibling to [[deepseek-v4]]. *(weekly-brief 2026-06-06.)*
- **SAM 3D (arXiv:2511.16624, CVPR 2026 Best Paper)** — Extends SAM paradigm to grounded 3D reconstruction from single images; 5:1 human-preference win rate on real-world objects. Extends SAM2 cluster into 3D; adjacent to [[sharp-view-synthesis]] and [[cosmos-3]]. *(weekly-brief 2026-06-06.)*
- **MLEvolve (arXiv:2606.06473, ICML 2026)** — LLM-based multi-agent that outperforms AlphaEvolve on math algorithm optimization; Progressive Monte Carlo Graph Search + retrospective memory. Evolutionary AutoML; extends [[huxley-godel-machine]] / [[eggroll]] evolutionary line. *(weekly-brief 2026-06-06.)*
- **ProRL Agent (arXiv:2603.18815, Microsoft Research)** — Decouples RL rollout from training loop; supports rootless HPC sandboxing; predecessor to [[polar-rl-harness]]; validated on SWE/math/STEM. Foundational infra paper for the agentic RL wave. *(weekly-brief 2026-06-06.)*
- **Rethinking Continual Experience Internalization (arXiv:2606.04703, June 2026)** — Identifies "progressive capability collapse" in multi-iteration experience learning; principle-level > instance-level experience and step-wise > global injection. Continual post-training methodology; adjacent to [[huxley-godel-machine]] / [[seal-self-adapting]]. *(weekly-brief 2026-06-06.)*
- **Flash-WAM (arXiv:2606.05254, June 2026)** — 23× speedup on joint video+action diffusion models via modality-aware consistency distillation; enables real-time robot control from World Action Models. Robotics distillation adjacent to [[cosmos-3]] policy mode. *(weekly-brief 2026-06-06.)*
- **STARE: Surprisal-Guided Token-Level Advantage Reweighting (arXiv:2606.19236)** — Identifies entropy-critical tokens via batch-internal surprisal quantiles, reweights advantages, adds target-entropy closed-loop gate to prevent collapse in GRPO; beats DAPO 4–8% on AIME24/25 across 1.5B–32B. Code released. Extends [[high-entropy-tokens-rlvr]] / [[token-gradient-cancellation]] cluster. *(weekly-brief 2026-06-27.)*
- **JetSpec: Parallel Tree Drafting for Speculative Decoding (arXiv:2606.18394)** — Causal parallel draft head predicts multiple tree nodes in one forward pass while preserving branch-wise causal conditioning; 9.64× speedup on MATH-500 with Qwen3-8B on B200. Code: hao-ai-lab/JetSpec. *(weekly-brief 2026-06-27.)*
- **ParaRNN (Apple, ICLR 2026 Oral)** — Breaks sequential-computation barrier for nonlinear RNNs: 665× training speedup; 7B-parameter RNN reaches Transformer-comparable perplexity. Open-sourced. Recurrent-architecture alternative with transformer-scale training feasibility. *(weekly-brief 2026-06-27.)*
- **DAG-MoE: Structural Aggregation in MoE (arXiv:2606.01062, ICML 2026)** — Replaces standard weighted-sum expert aggregation with a learned DAG structure over selected experts; enables multi-step reasoning within a single MoE layer; consistently outperforms standard MoE on LM and downstream tasks. *(weekly-brief 2026-06-27.)*
- **MoE Surpasses Dense Under Equal Resources (arXiv:2506.12119, StepFun/Fudan)** — First systematic demonstration MoE beats dense at identical total-parameter + compute + data budget; identifies stable "optimal activation rate" region across model sizes. Directly relevant to [[deepseek-v4]] / MoE cluster. *(weekly-brief 2026-06-27.)*
- **G2PO: Group-Graph Policy Optimization (arXiv:2606.22995)** — Converts linear agent trajectories into a global state-transition graph; group-aggregation state-value + edge-centric advantage estimation reduces variance in long-horizon agentic RL; beats GRPO-style baselines on WebShop/ALFWorld/AppWorld. Extends [[agentflow]] / [[memagent]] agentic RL cluster. *(weekly-brief 2026-06-27.)*
- **Log-Linear Attention (arXiv:2506.04761, ICLR 2026)** — Attention mechanism with logarithmically growing hidden states; matmul-rich parallel form with log-linear compute cost; more expressive than linear attention while staying sub-quadratic. Extends sub-quadratic attention cluster. *(weekly-brief 2026-06-27.)*
- **Programming by Backprop (arXiv:2506.18777)** — Training regime where declarative instructions in training data "program" reusable algorithmic behaviors into model weights without I/O examples; LLMs learn to execute programs from source code alone. HuggingFace daily paper June 23. *(weekly-brief 2026-06-27.)*
- **Bridging Offline and Online RL for LLMs (arXiv:2506.21495)** — Systematic comparison of offline/semi-online/online RL regimes (DPO/GRPO variants) for verifiable and non-verifiable tasks; online strongly dominates; multi-task joint training (verifiable + non-verifiable) improves both. HF daily paper June 26. *(weekly-brief 2026-06-27.)*
- **"Scaling Laws, Carefully" (Lilian Weng, June 24 2026)** — Authoritative synthesis from Anthropic's head of safety research: Kaplan vs Chinchilla disagreements, compute-optimal allocation mechanics, why fitting details make extrapolation brittle. High-impact blog post driving r/MachineLearning discussion; URL: lilianweng.github.io/posts/2026-06-24-scaling-laws/. *(weekly-brief 2026-06-27.)*

## Architectures & sequence models (continued — weekly-brief 2026-07-04)

- **FlashMorph: Morphing into Hybrid Attention Models (arXiv:2606.30562, ByteDance Seed/Fudan)** — Budget-constrained subset optimization selects which full-attention layers to replace with linear alternatives; joint gate optimization + discretization; maintains long-context performance with reduced FLOPs. Extends hybrid-attention cluster. *(weekly-brief 2026-07-04.)*
- **Multi-Block Diffusion Language Models (arXiv:2606.29215, SJTU)** — Extends diffusion LMs from single-block to multi-block decoding via Multi-block Teacher Forcing (MultiTF) + Block Buffer-based decoding; TPF 3.47→6.19, accuracy 79.95→81.03 on math/code. Extends [[coladlm]] / [[elf-embedded-language-flows]] diffusion-LM cluster. *(weekly-brief 2026-07-04.)*
- **Formalizing Latent Thoughts: Four Axioms of Thought Representation in LLMs (arXiv:2606.27378, UBC-Okanagan)** — Establishes four formal axioms for latent thought representations in LLMs; 58 HF upvotes; theoretical grounding for CoT and latent reasoning research. Adjacent to [[latent-grpo]] / [[lepo]] latent-reasoning cluster. *(weekly-brief 2026-07-04.)*

## RL / post-training (continued — weekly-brief 2026-07-04)

- **Prefix-RFT: Blending Supervised and Reinforcement Fine-Tuning with Prefix Sampling (arXiv:2507.01679)** — Prefix sampling from demonstrations seeds RL exploration, addressing SFT's poor generalization and RFT's reward hacking; outperforms standalone SFT, RFT, and mixed-policy RFT on mathematical reasoning. Novel training paradigm bridging SFT/RFT. *(weekly-brief 2026-07-04.)*
- **Denser ≠ Better: Limits of On-Policy Self-Distillation for Continual Post-Training (arXiv:2607.01763)** — Empirical analysis challenging the assumption that denser self-distillation signals always improve continual post-training; identifies failure regimes. Adjacent to [[anti-self-distillation]] / [[dopd-dual-on-policy-distillation]] distillation-critique cluster. *(weekly-brief 2026-07-04.)*
- **BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Speculative Decoding (arXiv:2606.31315)** — Lightweight policy predicts optimal block size per input from prefill representation; 5.92 acceptance length, 4.20× speedup on Qwen3-4B; plug-and-play. Extends speculative-decoding cluster ([[tidar]]). *(weekly-brief 2026-07-04.)*

## Evolution strategies (continued — weekly-brief 2026-07-04)

- **EvoPolicyGym: Evaluating Autonomous Policy Evolution in Interactive Environments (arXiv:2607.02440)** — 16-author benchmark for measuring iterative LLM-driven policy self-improvement across 16 RL environments; GPT-5.5 tops the suite. Evaluation framework for [[huxley-godel-machine]] / [[seal-self-adapting]] line. *(weekly-brief 2026-07-04.)*
- **PopuLoRA: Co-Evolving LLM Populations for Reasoning Self-Play (arXiv:2605.16727)** — Population-based LoRA adapters as teacher (proposer) / student (solver) with weight-space evolution operators on frozen 7B base; mean population beats compute-matched baselines on 10 code+math benchmarks. Evolutionary PEFT at LLM scale. *(weekly-brief 2026-07-04.)*

## Infrastructure (continued — weekly-brief 2026-07-04)

- **OpenAI gpt-oss-120b / gpt-oss-20b (July 2026)** — OpenAI's first open-weight model release at frontier scale; gpt-oss-120b benchmarks near o3/o4-mini, fits on a single GPU; gpt-oss-20b runs locally on high-end consumer hardware. Significant industry shift; no single technical paper. *(weekly-brief 2026-07-04.)*
- **Genie 3 (Google DeepMind, July 2026)** — Foundation world model generating interactive 3D environments at 720p/24fps for minutes (vs Genie 2's 10–20 seconds); supports promptable world events via text. Adjacent to [[conflicts/pure-video-vs-3d-world-models]] pure-video-scaling position. *(weekly-brief 2026-07-04.)*

## RL / post-training (continued — weekly-brief 2026-08-01)

- **BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms (arXiv:2607.26497)** — HF Daily Papers trending, July 31. Provocative empirical finding that classic BM25 retrieval matches/outperforms learned retrievers at scale in RAG; part of this week's memory/retrieval cluster alongside MemoHarness, Metis, Memory Decoder at Scale. *(weekly-brief 2026-08-01.)*
- **Metis: Memory Foundation Model (arXiv:2607.26760, MemTensor)** — HF Daily Papers, July 31. Dedicated memory foundation model; part of the "memory as first-class LLM component" cluster surfacing this week. *(weekly-brief 2026-08-01.)*
- **Memory Decoder at Scale: A Pretrained, Parametric Long-Term Memory (arXiv:2607.27919)** — HF Daily Papers, July 31. Parametric alternative to retrieval-based long-term memory, scaling study. Adjacent to [[delta-mem]] / [[memagent]] cluster. *(weekly-brief 2026-08-01.)*
- **Distilled Reinforcement Learning for LLM Post-training (arXiv:2607.17247)** — Addresses cross-family transfer limits of on-policy distillation vs. coarse RL supervision; adjacent to [[dopd-dual-on-policy-distillation]] / [[flux-opd]] distillation-critique cluster. *(weekly-brief 2026-08-01.)*
- **Understanding Reasoning from Pretraining to Post-Training (arXiv:2607.16097)** — Uses chess as a controlled testbed across the full pretrain→SFT→RL pipeline to study where reasoning capability originates. Methodology relevant to the [[reasonmaxxer]] / [[high-entropy-tokens-rlvr]] sparse-policy-selection debate. *(weekly-brief 2026-08-01.)*
- **Position: Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces (arXiv:2504.09762)** — r/MLScaling top post of the week; pushback against treating CoT tokens as literal reasoning, relevant to [[thought-anchors]] / RL-interpretability debates. *(weekly-brief 2026-08-01.)*

## Infrastructure (continued — weekly-brief 2026-08-01)

- **Molt: A Scalable PyTorch-Native Training Framework for Agentic Reinforcement Learning (arXiv:2607.21653, NVIDIA NeMo)** — HF trending; lean, hackable RL trainer scaling to trillion-param MoE at throughput comparable to Megatron. Open-sourced. Adjacent to [[polar-rl-harness]] / [[llamarl]] infra cluster. *(weekly-brief 2026-08-01.)*
- **DeepSeek-V4-Flash-0731 (July 2026)** — Fast-follow flash variant of DeepSeek-V4; ArtificialAnalysis index ~50 (1pt behind GLM-5.2/GPT-5.6), matches Sonnet 5 / Grok 4.5 on DeepSWE. Extends [[deepseek-v4]] cluster. *(weekly-brief 2026-08-01.)*
- **Qwen3.7-Flash (Alibaba, July 2026)** — First Qwen release that is API-only — no open weights or technical report, breaking Alibaba's prior fully-open release pattern. Notable strategic-shift signal rather than a technical contribution. *(weekly-brief 2026-08-01.)*
- **Claude Opus 5 (Anthropic, July 24 2026)** — New SOTA on FrontierBench v0.1 / GDPval-AA at same price as Opus 4.8; adds a low/medium/high "effort" toggle and self-verification/error-recovery behavior. Used as the primary scaffold in this week's [[ai-agents-open-ended-research]]. *(weekly-brief 2026-08-01.)*

## RL / post-training (continued — weekly-brief 2026-08-08)

- **AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning (arXiv:2608.05987)** — Applies the on-policy self-distillation pattern to agentic RL loops recursively. Sibling of [[u-opsd-unsupervised-self-distillation]] in this week's 6-paper OPD cluster explosion. *(weekly-brief 2026-08-08.)*
- **OPD-V: Visual On-Policy Self-Distillation with Modality Balance (arXiv:2608.05131)** — CV/multimodal extension of OPD; +15.7pp accuracy on Qwen3.5-4B backbone. OPD cluster sibling. *(weekly-brief 2026-08-08.)*
- **Poly-OPD: Heterogeneous Multi-Teacher On-Policy Distillation for Capability-Selectable Flow Models (arXiv:2608.04349)** — Consolidates multiple heterogeneous teachers into one compact flow-matching student. OPD cluster sibling. *(weekly-brief 2026-08-08.)*
- **Cross-Domain Hybrid OPD for Generalizable Search Agents (arXiv:2608.02101)** — Combines agentic RL with cross-domain on-policy distillation to generalize search-agent behavior. OPD cluster sibling. *(weekly-brief 2026-08-08.)*
- **On-Policy Delta Distillation (OPD²) for Multilingual Math Reasoning (arXiv:2608.05802)** — Delta variant of OPD transferring reasoning gains across languages. OPD cluster sibling; fifth of six OPD papers surfaced this week alongside [[u-opsd-unsupervised-self-distillation]]. *(weekly-brief 2026-08-08.)*
- **LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks (arXiv:2608.01964)** — HF Daily Papers #1 ranking this week; reformulates long-horizon agent execution as explicit task-state management outside the LLM context (Manage-Execute-Audit loop). Pushes Qwen3.7-Plus 51.8%→80.7% on WeaveBench. Adjacent to [[argus-agentic-runtime]] agentic-runtime cluster. *(weekly-brief 2026-08-08.)*
- **HarnessOpt-Bench: Evaluating LLMs at Harness Optimization (arXiv:2608.06301)** — Benchmark for automated agent-harness optimization; finds optimizer-model choice matters more than the harness it acts through, across 111 scored runs. Adjacent to [[memoharness]] / [[argus-agentic-runtime]]. *(weekly-brief 2026-08-08.)*

## Infrastructure (continued — weekly-brief 2026-08-08)

- **Qwen3.8-Max (Alibaba, August 3 2026)** — 2.4T-param MoE, first Max-class Qwen model to go open-weight; claims OSWorld-Verified 86.1, beating GPT-5.6 Sol / Claude Fable 5 / Gemini 3.1 Pro. Major open-weight capability jump; extends the frontier open-weight race alongside [[kimi-k3]] / [[deepseek-v4]]. *(weekly-brief 2026-08-08.)*
- **DeepSeek-V4-Flash-0731 post-train agentic update (July 31 2026)** — RL-with-verifiable-rewards post-training alone (no architecture/scale change) drove DeepSWE 7%→54%, beating V4-Pro on 9/9 agent benchmarks. Strong RLVR case study; extends [[deepseek-v4]] cluster (this is a post-train update to the entry captured 2026-08-01). *(weekly-brief 2026-08-08.)*
- **Import AI #467 — self-sustaining AI viruses (Jack Clark, August 3 2026)** — Reports a prototype self-replicating AI worm (U. Toronto/Vector/Cambridge/ServiceNow) achieving ~37% end-to-end attack success via stolen GPU compute. Policy/capability risk signal from this wiki's jackclarkSF source. *(weekly-brief 2026-08-08.)*

## RL / post-training (continued — weekly-brief 2026-08-22)

- **SPADE: Self-Play in Adaptive Synthetic Executable Environments (arXiv:2608.*)** — Self-play framework for language-agent self-improvement via adaptively-generated executable environments; +8.1pp on reasoning benchmarks. Part of this week's self-play/dynamic-environment cluster alongside EnvHarness and OpenART. *(weekly-brief 2026-08-22.)*
- **EnvHarness: Awakening Static Worlds for Agent Learning (arXiv:2608.*)** — Dynamic, customizable training-environment generation for LLM agents; +9.0pp on held-out tasks. Same self-play/dynamic-environment cluster as SPADE. *(weekly-brief 2026-08-22.)*
- **OpenART: Scaling Agent Red Teaming via Open-Ended Environment Evolution (arXiv:2608.00677)** — 10,000+ validated stateful red-team scenarios across 50 domains via open-ended environment evolution. Same self-play/environment-design cluster as SPADE/EnvHarness, applied to red-teaming. *(weekly-brief 2026-08-22.)*
- **ToolHazard: Scaling Adversarial Environments for Security Evaluation and Alignment of LLM-based Agents (arXiv:2608.11878)** — Automated (Env Simulator + Attacker Agent + User Simulator) synthesis of indirect-prompt-injection environments; ships ToolHazard-Bench. Pairs thematically with OpenART. *(weekly-brief 2026-08-22.)*
- **TRACES: A Benchmark for Epistemic Reliability in Scientific Reasoning by LLMs (arXiv:2608.11415)** — 42 retracted/pseudoscientific probe corpus; LLMs engage with flawed premises ~95% of the time instead of rejecting them. *(weekly-brief 2026-08-22.)*
- **Spark-to-Paper: End-to-End Research Paper Generation as a Composable Skill (arXiv:2608.11924)** — One-line idea → draft paper with verified citations, auto-run experiments, editable figures (~$10 API cost/paper). HF Daily Papers #1 (Aug 13). Adjacent to [[ai-agents-open-ended-research]]'s skepticism about autonomous research judgment. *(weekly-brief 2026-08-22.)*
- **SWE-Bench ProMax: Benchmarking Agents on Large-Scale Multilingual Code Refactoring (arXiv:2608.09802)** — 170 curated multilingual refactoring tasks (avg 11.4 files/261.6 LOC changed); best model only 41.2% resolve rate — harder, less-contaminated successor to SWE-bench Verified. *(weekly-brief 2026-08-22.)*

## Computer vision / 3D (continued — weekly-brief 2026-08-22)

- **4DAnyone (Ant Research, Aug 2026)** — Reconstructs 4D humans from monocular video via multiview-consistent video generation lifted into 4D Gaussian Splatting; 62 HF upvotes. *(weekly-brief 2026-08-22.)*

## Infrastructure (continued — weekly-brief 2026-08-22)

- **FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution (arXiv:2608.16157, UC Berkeley)** — Runs 20+ open-weight MoE models via bandwidth-adaptive expert offloading on hardware from 8GB laptop GPUs to a single workstation GPU. *(weekly-brief 2026-08-22.)*
- **GLM-5.3 (Z.ai, August 14 2026)** — 743B base MoE model; leads CyberGym/AutomationBench; open weights staged behind safety review, not yet public. Extends the frontier open-weight race alongside [[kimi-k3]] / [[deepseek-v4]] / Qwen3.8-Max. *(weekly-brief 2026-08-22.)*

## Evolution strategies (continued — weekly-brief 2026-08-29)

- **Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO (arXiv:2608.27351)** — Second ES-vs-GRPO coverage paper surfacing the same week as [[es-solution-coverage]]; same subfield, not yet independently read. *(weekly-brief 2026-08-29.)*
- **Hyper-ES: Effective Evolution Strategies for LLM Reasoning via Descent Direction Merging (arXiv:2608.05541)** — Merges ES descent directions across a population for more sample-efficient LLM reasoning fine-tuning; third ES-for-LLM-reasoning paper this cluster this week. *(weekly-brief 2026-08-29.)*

## RL / post-training (continued — weekly-brief 2026-08-29)

- **Reward Hacking Benchmark: Measuring Exploits in LLM Agents with Tool Use (arXiv:2605.02964)** — Benchmark quantifying reward-hacking exploits in tool-using LLM agents; adjacent to [[debate-training-reward-hacking]]'s mitigation angle. *(weekly-brief 2026-08-29.)*
- **Ryan Greenblatt on Dwarkesh Podcast (Aug 11 2026)** — Recursive self-improvement, verifiable training, and reward-hacking risk framing; podcast-only, no paper captured. *(weekly-brief 2026-08-29.)*

## Self-improving agents (continued — weekly-brief 2026-08-29)

- **Accelerating Scientific Research with Gemini in the Real-World / Co-Scientist (arXiv:2608.26701, Google DeepMind)** — Gemini-based multi-agent system moves from in-silico hypothesis generation to execution-grounded, closed-loop real-world experiments (materials science, biology, CS). *(weekly-brief 2026-08-29.)*

## Benchmarks & evaluation (continued — weekly-brief 2026-08-29)

- **ASI-Bench: At the Dawn of Artificial Superintelligence (arXiv:2608.17271)** — First benchmark progressively withdrawing methodological guidance across 60 project-level research tasks (scores drop ~51→~27 as guidance is removed); probes autonomous end-to-end scientific capability rather than isolated task performance. *(weekly-brief 2026-08-29.)*

## Infrastructure (continued — weekly-brief 2026-08-29)

- **Demystifying Agent Skills: Why They Work—Until They Don't (arXiv:2608.14036)** — Taxonomy of agent-skill failure modes; procedural anchoring dominates over knowledge injection, retrieval precision collapses as skill pools grow. Trended alongside AutoSaddler as this week's "agent harness/scaffolding" meta-topic. *(weekly-brief 2026-08-29.)*
- **AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces (Microsoft, arXiv:2608.23041)** — Auto-improves agent harnesses from failure traces; +9–10pp on GAIA2/SWE-Bench Pro/Terminal-Bench. Code released (github.com/microsoft/AutoSaddler). *(weekly-brief 2026-08-29.)*

## Computer vision / 3D (continued — weekly-brief 2026-08-29)

- **VGI-Bench: Probing Visual Intelligence in Video Generation Models** — Benchmark for physical/visual intelligence in video-generation models. *(weekly-brief 2026-08-29.)*
- **UrbanGround** — Multimodal LLM-agent navigation/spatial-reasoning benchmark in a realistic 3D city replica. *(weekly-brief 2026-08-29.)*

## Architectures & sequence models (continued — weekly-brief 2026-09-05)

- **LLaDA-Image: Building Strong Image Generators with Fully Open Training Recipes (arXiv:2609.03796)** — 6B DiT built on the LLaDA2.0-Mini diffusion-LM backbone; image-only pretrain-then-align recipe; new open-source SOTA on Qwen-Image-Bench (53.5). HF Daily Papers #2 trending. Diffusion-LM-as-image-backbone sibling of [[coladlm]] / [[elf-embedded-language-flows]]. *(weekly-brief 2026-09-05.)*
- **"Uno" — diffusion-augmented LLM framework unifying AR and discrete diffusion decoding** — Surfaced as alphaXiv-trending via two independent search passes; claimed 2.5× single-request speedup via parallel decoding. Exact arXiv ID/URL could not be confirmed at scan time — flagged as an unverified lead, needs direct-source lookup before promotion to a capture. *(weekly-brief 2026-09-05.)*

## Computer vision / 3D (continued — weekly-brief 2026-09-05)

- **SolarWM: Open Data and Scalable Training for Long-Horizon Video World Models (arXiv:2609.02886)** — Open training recipe + open data for long-horizon video world models. Adjacent to [[conflicts/pure-video-vs-3d-world-models]]. *(weekly-brief 2026-09-05.)*
- **LightNav-0: VLM Spatial Intelligence for Generalist Embodied Navigation (arXiv:2608.30935)** — Compact VLM for embodied navigation with a compute-efficiency angle. *(weekly-brief 2026-09-05.)*

## Infrastructure (continued — weekly-brief 2026-09-05)

- **Import AI #471 — "Why Hugging Face worries me; space mining; Five Eyes on AI" (Jack Clark, Aug 31 2026)** — Policy-lead commentary on open-model-ecosystem risk (Hugging Face) and dual-use/national-security framing. Continues the policy/capability-risk thread from Import AI #467 (self-sustaining AI worm, 2026-08-08). *(weekly-brief 2026-09-05.)*
