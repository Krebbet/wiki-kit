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
| [[coladlm]] | ByteDance Seed (arXiv:2605.06548). Three-stage continuous-latent diffusion LM: causal Text VAE (d=16) → ~1.8B block-causal DiT prior via Flow Matching (block size 16) → conditional decoder. ~2B total; best scaling curve at high compute (~2000 EFLOPs) vs matched AR and LLaDA on 8 benchmarks under few-shot generative eval. ~1.6–2× reduction in sequential decoding depth. PPL not comparable to AR (structural gap flagged by authors). Section 5.5: qualitative multimodal extension via MMDiT. |
| [[manifold-constrained-hyper-connections]] | DeepSeek mHC: stabilizes Hyper-Connections by projecting residual-mixing matrix onto Birkhoff polytope via Sinkhorn-Knopp. Composite-mapping Amax 3000 → 1.6 at 27B; +2.1 BBH, +2.3 DROP vs HC. |
| [[hyperloop-transformers]] | MIT: middle-cycle looped Transformer + loop-level mHC (diagonal-sigmoid H_res, not Sinkhorn). Beats depth-matched Transformer on FineWeb-Edu PPL and downstream task accuracy at three scales (136M–991M looped) using ~50% fewer params. Survives INT4 GPTQ. |
| [[triattention]] | MIT/NVIDIA/ZJU: training-free KV cache compression via pre-RoPE Q/K concentration — a closed-form trigonometric distance-preference score replaces post-RoPE attention sampling. 2.5× throughput at matched AIME25 accuracy; 10.7× KV memory; 6.3× on MATH 500 at budget 1024. Code released. |
| [[mamba-3]] | CMU/Princeton/Together/Cartesia, ICLR 2026 poster (arXiv:2603.15569). Three SSM-principled deltas vs Mamba-2: exponential-trapezoidal discretization, complex-valued state transitions (data-dependent RoPE-like dynamics on B/C), MIMO matmul updates. +1.8 avg over Mamba-2 at 1.5B; first selective SSM with complex state, solving TC⁰-hard tasks (parity, modular arithmetic). |
| [[ssm-tool-use-length-generalization]] | Apple, ICLR 2026 Oral (arXiv:2510.14826). Formal proof + experiments: fixed-memory recurrent architectures (Mamba/LSTM/RetNet/H3/etc.) cannot solve long-form generation in CoT-only or single-turn-tool-use settings (Theorem 2.1) but achieve length generalization on any tractable task with a Turing-tape-style interactive memory tool (Theorem 2.2). Mamba-1.4B trained on ≤5-digit addition extrapolates to 1000-digit addition at 100%. |
| [[sst-v2]] | Fifth Dimension (arXiv:2605.00206). QLoRA-tuned Gemma 3 27B + per-layer FFN-driven horizontal Latent State Cache (LSC); two-pass training parallelises the sequential recurrence (O(α²) ≈ 6–12×10⁻⁴ approximation error). +15.15 pp GPQA-Diamond, 46% GSM8K error reduction, beats DeepSeek V3 671B with 25× fewer params. Third path in [[conflicts/fixed-state-ssm-long-context]] (Transformer + nonlinear horizontal state). |
| [[memagent]] | ByteDance Seed / Tsinghua (arXiv:2507.02259, ICLR 2026 Oral). RL-trained agent overwrites a 1024-token plain-text memory buffer each step via Multi-Conv DAPO; trained at 8K context, RL-MemAgent-14B extrapolates to 3.5M-token QA with <5% accuracy loss; >95% RULER 512K. Third path in long-context architecture: neither scaled attention nor recurrent SSM. |
| [[delta-mem]] | δ-mem (arXiv:2605.12357). Frozen full-attention backbone + compact gated delta-rule online state (8×8/layer, r=8) steering attention via dynamic low-rank Δq/Δo corrections; ~4.87M new params (0.12%), SFT only. Qwen3-4B avg +4.87 pp, MemoryAgentBench ×1.31, LoCoMo TTL ~×1.93. Memory-skeptical third path in [[conflicts/long-context-attention-vs-recurrent-memory]] / [[conflicts/fixed-state-ssm-long-context]]. |
| [[elf-embedded-language-flows]] | MIT (Kaiming He et al., arXiv:2605.10938). Continuous diffusion LM: Flow Matching entirely in continuous embedding space, discretize only at t=1 via a shared-weight denoiser-decoder (no separate decoder, no compression VAE). WMT14 De-En BLEU 26.4, XSum R1 36.0 (best vs AR/MDLM/Duo); 10× fewer training tokens, no distillation. Parallel to [[coladlm]] in the continuous diffusion-LM cluster. |
| [[orthrus]] | Orthrus (arXiv:2605.12825). Lightweight trainable masked-diffusion head injected into a frozen AR transformer sharing one KV cache; KL-distilled vs live AR teacher → mathematically lossless output. Up to 7.83× speedup, O(1) (~4.5 MiB) KV overhead, exact AR parity. Frozen-backbone sibling of [[tidar]]. |
| [[gated-deltanet-2]] | NVIDIA (arXiv:2605.22791). Decouples delta-rule linear attention's single scalar gate β_t into two channel-wise gates — key-axis erase b_t + value-axis write w_t (recovers Gated DeltaNet/KDA as tied-gate special cases). Pure-recurrent beats Mamba-2/GDN/KDA/Mamba-3 SISO+MIMO at 1.3B/100B (recurrent avg 53.11 vs Mamba-3 MIMO 52.39); MK-NIAH-1 @4K 37.8 vs ≤28.0. Ablation: erase gate alone recovers most retrieval gain → update-rule specificity, not state size. Code released. Displaces [[mamba-3]] as recurrent SOTA. |
| [[hrm-text]] | SapientInc (arXiv:2605.20613). 1B dual-timescale hierarchical recurrent model (H2L3, 8 H/L steps, 4× recursion) pretrained from scratch on instruction-response pairs only — no raw-text phase, ~$1,472 / 40B tokens. MATH 56.2 / GSM8K 84.5 / ARC-C 81.9; beats Huginn 3.5B (MATH 12.6) at 127× more compute, rivals 2–7B dense models at 96–432× the compute. Positions task-completion-only pretraining against Chinchilla raw-text orthodoxy. Code released. |
| [[gram-recursive-reasoning]] | GRAM (KAIST/Mila/NYU, arXiv:2605.19376). Makes deterministic Recursive Reasoning Models (HRM/TRM/Looped Transformers) stochastic via ELBO/amortized VI — stochastic residual on the high-level state → multi-trajectory latent reasoning (N parallel, majority/LPRM select) + unconditional generation, no architecture change. Sudoku-Extreme 97.0% (vs TRM 87.4 / HRM 61.3); ARC-AGI-1 66.7% (vs TRM 55.7 / HRM 52.0). alphaXiv top-trending this week. |

## Training & optimization

| Page | Summary |
|---|---|
| [[eggroll]] | Oxford/MILA/NVIDIA Evolution Strategies at hyperscale: low-rank LoRA-style perturbations + counter-based PRNG → ~100× ES throughput. Beats GRPO on 14B RWKV-7 reasoning where GRPO is infeasible (Adam state). Pure-int8 RNN pretraining at population 2^20. |
| [[rlsd-self-distilled-rlvr]] | IIE/CAS + JD.COM: fixes on-policy self-distillation's privileged-info leakage by decoupling direction (verifier reward, same as GRPO) from magnitude (teacher/student evidence ratio as scalar weight). +2.32% avg over GRPO on Qwen3-VL-8B across 5 multimodal-reasoning benchmarks; RLSD@200 steps beats GRPO@400. |
| [[token-gradient-cancellation]] | Alibaba/Tsinghua: formal "gradient exchangeability" condition for stable GRPO-style RL — shared/template tokens must cancel across trajectories. DFPO (Min-Replace or Adv-Orthogonal stop-gradient transforms) restores cancellation. +5.6 / +6.9 / +5.6 pp avg@32 (AIME25 / LiveCodeBench v6 / HMMT25) over GSPO at Qwen3-32B; gain grows with group size. |
| [[neural-garbage-collection]] | Stanford/Goodman lab: end-to-end RL training of KV-cache eviction *jointly* with chain-of-thought, using outcome reward only. 2–3× cache compression with minimal accuracy loss on AMC/AIME; first method to unify eviction and token gradients under one signal. Replay attention mask corrects off-policyness from dynamic cache mutation. |
| [[gepa-reflective-prompt-evolution]] | UC Berkeley/Stanford/Databricks/MIT, ICLR 2026 oral (arXiv:2507.19457). Genetic-Pareto reflective prompt optimizer for compound AI systems; no weight updates. Beats GRPO by up to 20% with up to 35× fewer rollouts on Qwen3-8B/6 tasks. Cross-model transfer: prompts optimized on Qwen3-8B beat baselines optimized natively on GPT-4.1-Mini. |
| [[tempo-test-time-rl]] | Tianjin/Tongyi Lab/CUHK/Shanghai AI Lab (arXiv:2604.19295). Test-time training for LRMs framed as EM. TTRL/EMPO are M-step-only EM variants and structurally drift; TEMPO restores the E-step via periodic critic recalibration on labeled data. OLMO3-7B AIME 2024 33.0 → 51.1 avg@16; Qwen3-14B 42.3 → 65.8. Maintains pass@k where TTRL/EMPO degrade it. |
| [[latent-grpo]] | Tsinghua/Alibaba (arXiv:2604.27998). RL post-training for latent (continuous-token) reasoning via three GRPO stabilization fixes: invalid-sample masking, one-sided Gumbel STE, optimal first-token selection. Qwen2.5-Math-7B +14.77 pp Pass@1 over Latent-SFT, +4.27 pp over explicit GRPO with **3.31× fewer reasoning tokens**. AIME24 pass@64 50.0 vs explicit GRPO 23.3. |
| [[agentflow]] | Stanford/TAMU/UCSD/Lambda, ICLR 2026 Oral (arXiv:2510.05592). Four-module agentic system (Planner / Executor / Verifier / Generator) trained on-policy via Flow-GRPO — broadcasts trajectory-level outcome reward to every turn's policy update. Qwen2.5-7B + Flow-GRPO beats GPT-4o on search/agentic/math/science benchmarks. |
| [[reasonmaxxer]] | USC / DEVCOM ARL (arXiv:2605.06241). Token-level analysis across 4 base/RL pairs: RL modifies only 1–4% of token positions, all within the base model's top-5, all at high-entropy decisions; the correction fits in a rank-32 LoRA. ReasonMaxxer (entropy-gated contrastive FT on 50 problems, minutes single-GPU, $4–$25) matches or exceeds full RL across 3 model families × 6 scales × 6 math benchmarks ($200–$103K). Reframes RL as sparse policy selection, not capability learning. |
| [[scalelogic]] | ScaleLogic (arXiv:2605.06638). Controlled synthetic benchmark for RL reasoning scaling: power-law T ∝ D^γ holds with R² > 0.99 across 5 logical-expressiveness levels and 3 RL algorithms (DAPO/GRPO/GSPO); γ ranges 1.04 (implication-only) → 2.60 (+quantification). Training on the most-expressive curriculum transfers +10.66 pp across 8 math/reasoning benchmarks; simpler curricula plateau at +2–3 pp. "What you train on dominates how much." |
| [[anti-self-distillation]] | AntiSD (Xiaohongshu/CAS, arXiv:2605.11609). PMI identity (Lemma 2): default on-policy self-distillation equals conditional PMI, so it structurally suppresses high-entropy deliberation tokens. Fix: *ascend* JSD (bounded advantage) + entropy-gated activation; potential-based shaping (optimum-invariant). Reaches GRPO accuracy in 2–10× fewer steps, up to +11.5 pp (Qwen3-4B 51.3→62.8); default SD collapses below base on every model. Code + WandB. Distinct SD instantiation from [[rlsd-self-distilled-rlvr]]. |
| [[delta-token-credit]] | DelTA (Renmin U / Ant Intl, arXiv:2605.21467). Reframes GRPO/DAPO updates as a linear discriminator over token-gradient vectors; shared formatting/entity tokens dominate both centroids and dilute reward-separating directions. Fix: per-token discriminative-contrast coefficients λ∈[0.8,1.2] reweight the DAPO surrogate. +3.26 pp (Qwen3-8B-Base) / +2.62 pp (14B) on 7 hard-math benchmarks; top-50% λ tokens beat full-token DAPO, bottom-50% collapse training. Code released. Third frame in [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]. |
| [[high-entropy-tokens-rlvr]] | Alibaba/Qwen (Wang et al., NeurIPS 2025, arXiv:2506.01939). Restricting RLVR gradient updates to the ~20% highest-entropy "forking" tokens matches or beats full-gradient training; gains scale with model size: +11.04 AIME'25 and +7.71 AIME'24 at Qwen3-32B. Active training-time intervention complementary to [[reasonmaxxer]]'s post-hoc observation. |
| [[spurious-rewards-rlvr]] | (arXiv:2506.10947, June 2025). GRPO with random or negatively-correlated rewards yields +21.4 pp MATH-500 on Qwen2.5-Math-7B (vs +29.1 real rewards); gain attributed to GRPO clipping bias amplifying high-prior pretrained behaviors, not reward learning. Fourth frame in [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]; model-family-dependent (fails for Llama3/OLMo2). |
| [[llamarl]] | Meta (arXiv:2505.24034, May 2025). Production async RL framework for Llama 3 post-training: single-controller PyTorch design decouples rollout from update via colocated offloading + async off-policy training + RDMA weight sync. 10.7× speedup over DeepSpeed-Chat-like synchronous systems on 405B policy; formal proof of async speedup. First RL infrastructure page in this wiki. |

## Self-supervised learning

| Page | Summary |
|---|---|
| [[lejepa]] | Balestriero & LeCun: JEPA training objective enforcing isotropic-Gaussian embeddings via sliced characteristic-function regularizer (SIGReg). Removes stop-gradient, EMA teacher, predictor, register tokens. ViT-H/14 79% IN-1K linear probe. ~50 LOC. |
| [[vision-banana]] | Google DeepMind (arXiv:2604.20329). Lightweight instruction-tuning of Nano Banana Pro on a small vision-task mix recasts segmentation / metric depth / surface normals as decodable RGB outputs. Zero-shot SOTA: beats SAM 3 (Cityscapes mIoU 0.699 vs 0.652), Depth Anything V3 (avg δ1 0.929 vs 0.918, no intrinsics), Lotus-2 normals — without sacrificing generation quality. |

## Self-improving agents

| Page | Summary |
|---|---|
| [[huxley-godel-machine]] | KAUST/Schmidhuber HGM: tree-search self-improving coding agent that scores parents by *clade* (descendant-aggregated) success rate (CMP) instead of own benchmark score. Approximates Gödel Machine under stated assumptions. SWE-bench Verified 61.4%, top-10. |
| [[skillopt]] | Microsoft Research (arXiv:2605.23904, May 2026). First systematic text-space optimizer for agent skills: a separate optimizer model proposes bounded add/delete/replace edits to a skill document, accepted only on strict validation improvement. Best-or-tied on all 52 (model × benchmark × harness) cells; +24.8 pp GPT-5.5 in Codex; skills transfer across models and harnesses. Zero deployment overhead. |
| [[seal-self-adapting]] | MIT/Harvard (SEAL, arXiv:2506.10943, June 2025). LLMs generate their own fine-tuning data and training directives ("self-edits") then apply gradient-based weight updates; outer RL loop trains the model to produce effective self-edits via downstream task performance reward. Only approach where adaptation strategy itself is a learned RL behavior. |

## Computer vision / 3D

| Page | Summary |
|---|---|
| [[sharp-view-synthesis]] | Apple SHARP: feedforward regression of 1.2M-Gaussian 3DGS scene from one RGB image in <1s on A100. Beats diffusion baselines (Gen3C, ViewCrafter) by 21–43% perceptual metrics, 1000× faster. Apple ml-sharp repo. |
| [[moonlake-world-models]] | Moonlake position post: pure 2D video diffusion cannot yield interactive world simulators; proposes hybrid pipeline binding *neutral information-free latent codes* to coarse 3D mesh patches as scaffolds for video diffusion. Position only — no benchmarks. |
| [[asymflow]] | Stanford (arXiv:2605.12964). Rank-asymmetric flow-matching velocity: full-rank data term, low-rank PCA-subspace noise term — lets a vanilla DiT model pixel space unmodified. ImageNet-256 FID **1.57** (best plain-transformer pixel diffusion); Procrustes latent→pixel lift makes AsymFLUX.2 beat the FLUX.2-klein latent base. Pixel-side evidence in [[conflicts/pixel-space-vs-latent-space-generation]]. |
| [[sensenova-u1]] | SenseNova-U1 / NEO-unify (arXiv:2605.12500). End-to-end unified multimodal (8B dense, 30B-A3B MoE) with **no VE and no VAE**: single MoT backbone, AR cross-entropy (language) + pixel-space flow matching (vision). Top open-source GenEval 0.91 / OpenING 9.16 / RealUnify 52.4; 32× pixel compression matches FLUX.1-dev VAE PSNR at 8×. Pixel-side anchor of [[conflicts/pixel-space-vs-latent-space-generation]]; parallels [[vision-banana]]. |

---

## Agent frameworks & memory

| Page | Summary |
|---|---|
| [[openclaw]] | OpenClaw: MIT-licensed, local-first AI agent runtime (formerly Moltbot/ClawdBot). Four-layer memory architecture (bootstrap files / session transcript / context window / retrieval index); plain-Markdown workspace; 70/30 vector/BM25 hybrid search; dreaming consolidation; providence labels (Apr 2026). |
| [[openclaw-claude-code-memory]] | Giving Claude Code persistent memory via OpenClaw-derived patterns: Hindsight shared banks (bidirectional cross-tool recall), Channels/Telegram (always-on agent), Mem0 plugin (drop-in replacement). Known constraint: Anthropic stated Claude Code is not designed for always-on third-party agents at scale — production use should build a dedicated API harness. |

---

## Conflicts (open positions)

| Page | Summary |
|---|---|
| [[conflicts/long-context-attention-vs-recurrent-memory]] | Titans/Hope claim recurrent memory beats GPT-4-class attention at extreme context. Awaiting attention-side counter-source. |
| [[conflicts/fixed-state-ssm-long-context]] | Titans/Hope claim fixed-state SSMs (Mamba-2) cannot capture rich long-sequence info. Third-path defences: SST V2 / MemAgent / δ-mem; [[gated-deltanet-2]] is the nearest pure-fixed-state defence (the gap is the update rule, not capacity). Canonical Mamba-2 defence still uncaptured. |
| [[conflicts/grpo-vs-evolution-strategies]] | EGGROLL claims ES matches/beats GRPO at scale; only feasible at 14B+. Awaiting GRPO-orthodoxy primary source. |
| [[conflicts/icl-emergent-vs-nested-levels]] | NL claims ICL is a direct consequence of nested levels, not emergent. Contradicts Brown 2020 / Wei 2022 framing. |
| [[conflicts/ttt-distinct-vs-parametric-icl]] | NL subsumes TTT under parametric ICL; In-Place TTT treats TTT as a distinct mechanism complementing attention. Internal cluster tension. |
| [[conflicts/regression-vs-diffusion-view-synthesis]] | SHARP claims feedforward regression Pareto-dominates diffusion for nearby-view single-image synthesis. Awaiting diffusion-side defence (Gen3C, etc.). |
| [[conflicts/pure-video-vs-3d-world-models]] | Moonlake claims pure video diffusion cannot yield interactive world simulators. Awaiting Sora-class pure-scaling defence. |
| [[conflicts/ssm-vs-associative-memory-taxonomy]] | Mamba-3 (§5.4) argues complex-state SSM dynamics aren't expressible inside MIRAS; [[nested-learning]] presents MIRAS as a unifier. Framing-level dispute about which lens designs new models. |
| [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] | Four-way mechanistic debate on why RLVR works. A: [[reasonmaxxer]] (sparse 1–4% high-entropy tokens drive gains). B: [[token-gradient-cancellation]] (gradient cancellation across shared tokens is the bottleneck). C: [[delta-token-credit]] (most tokens net-negative, discriminator reweighting fixes). D: [[spurious-rewards-rlvr]] (GRPO clipping bias amplifies pretrained behaviors regardless of reward correctness; model-family-dependent). |
| [[conflicts/pixel-space-vs-latent-space-generation]] | [[sensenova-u1]] + [[asymflow]] argue the VAE/encoder latent bottleneck is unnecessary (pixel-space matches latent at higher compression; AsymFLUX.2 pixel-finetune beats FLUX.2-klein latent base). Contradicts [[coladlm]]'s latent-VAE-is-the-scaling-direction bet. Resolved per-domain; CoLa-DLM's high-compute claim unrefuted at its own scale. |

---
