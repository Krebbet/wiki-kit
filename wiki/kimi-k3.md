# Kimi K3: KDA/MLA Hybrid MoE with Firecracker-Sandboxed Agentic RL

Moonshot's Kimi K3 is a 2.78T-parameter (104B active), 1M-context open-weight model combining a Kimi Delta Attention (KDA) / Gated-MLA hybrid attention stack with an 896-expert MoE using a new Quantile Balancing router, trained via agentic RL across 51M Firecracker-microVM sandboxes (AgentENV) and distilled from 9 specialist RL models via MOPD — reaching near-frontier benchmarks (Artificial Analysis Intelligence Index v4.1: 57.1, #4 of 580) at a claimed 2.5× training-FLOPs efficiency gain over Kimi K2.

## Architecture

**Attention — KDA (69/93 layers).** KDA is a Diagonal-Plus-Low-Rank linear-attention operator: `S_t = (D_t − a_t b_tᵀ) S_{t-1} + k_t v_tᵀ`, with `a_t = b_t = k_t`. Lineage: linear attention → DeltaNet (online-gradient-descent associative memory) → Gated DeltaNet (adds a scalar per-token forget gate) → KDA, first shown at 48B-A3B scale in Kimi Linear (Oct 2025), which turns the scalar gate into 128 per-channel decay rates (one per key-axis row of the 128×128 state). K3's delta vs. Kimi Linear is the gate itself: a **lower-bounded sigmoid gate** (`g = lower_bound · sigmoid(...)`, bounded in [-5, 0)) replacing Kimi Linear's unbounded negative-softplus gate. Purely a kernel-efficiency change — bounding all decay factors ≥ exp(-5) removes the need for special-cased diagonal position-pair tiles in the chunkwise kernel, and is the change that permits FlashKDA's small chunk size (below). KDA is a tied-gate (`a_t = b_t = k_t`) special case of the more general erase/write-gate decomposition in [[gated-deltanet-2]]; K3 is now the flagship production deployment of that special case.

**Attention — MLA (24/93 layers + final).** Every 4th layer is Gated Multi-head Latent Attention, DeepSeek-V2's technique unmodified: tokens project to one shared latent (kv_lora_rank 512, qk_rope_head_dim 64, 576 numbers/token) instead of per-head KV. MLA compresses per-token cache ~42.7× vs. ordinary MHA (1,152 vs 49,152 bytes/token/layer). The hybrid's cache-reduction ceiling vs. an all-MLA 93-layer design is ~3.9× (93/24) — and there's a real crossover, not just an asymptotic win: the fixed 221.55 MiB KDA cache (allocated per request from token 0) costs *more* than an all-MLA design below ~2,923 tokens. Attention-ablation evidence for the fixed-size-state approach at 1M-token scale: BrowseComp with compaction disabled (full raw 1M-token context) scores 90.4 vs. 91.2 with compaction — only a 0.8pp drop. Compare [[deepseek-v4]]'s CSA+HCA hybrid, same MLA lineage (DeepSeek-V2), same goal of shrinking KV cache via a different hybrid split. Compare also [[mamba-3]], a parallel line in the DPLR/gated-recurrence family.

**MoE + Quantile Balancing.** DeepSeekMoE-style shared+routed split pushed to 896 routed experts (top-16) + 2 shared experts per layer, routed-expert hidden width halved (7168→3584) to keep 896-wide communication affordable, plus RMSNorm and a softcapped SiLU-GLU activation to control top-16-of-896 activation blowup. Load balancing replaces DeepSeek-V3's fixed-step (γ) auxiliary-loss-free bias update with **Quantile Balancing (QB)**: per-step, per-GPU histograms of router margins are all-reduced and used to compute a bias that drives each expert toward exactly its target token quota in a single pass — framed as an assignment problem solved via per-expert "prices," vs. DeepSeek-V3's fixed-step sign search.

**Kernels.** FlashKDA (CUTLASS) makes KDA chunkwise at 16-token chunks (vs. FLA's default 64), enabled specifically by the bounded gate; split into a token-parallel "prepare" kernel and a head-parallel serial "recurrence" kernel (≥15% faster than a fused version per the repo's own ablation). Forward-only prefill is open; backward pass, decode kernel, and context-parallel planner stay closed. MoonEP is a new expert-parallel comms layer guaranteeing every GPU receives exactly S×K tokens/step via *dynamic redundant experts* — duplicate an overloaded expert onto a spare rank for that step, plan computed by a register-resident greedy loop — instead of DeepEP/ECHO/UltraEP's static/worst-case redundancy provisioning; also dedups token-vector payload (not score) when multiple top-k routes land on the same destination rank.

## RL infrastructure: AgentENV + MOPD

Kept here as a subsection rather than a separate page (this week's capture batch avoids over-fragmenting; revisit if RL-infra pages accumulate around it).

**Post-training pipeline.** SFT → 9 separate RL models spanning 3 domains (general/agentic/coding) × 3 reasoning-effort budgets (reward = −1 for exceeding a per-problem token budget; lower-effort models made by annealing the budget down) → **MOPD (Multi-Teacher On-Policy Distillation)**: the student generates its own rollouts, each token rewarded by the clipped log-ratio between student and the domain/effort-matched teacher, distilling all 9 specialists into one final deployable model on the same RL infra (including partial rollouts).

**AgentENV.** A Rust sandbox runtime on Firecracker microVMs exposing pause/fork/snapshot as first-class RL primitives: pause suspends a trajectory the partial-rollout scheduler deprioritized, fork gives reward judging a disposable copy with no side effects on the live trajectory, snapshot supports failure recovery via dirty-page-tracking direct memory snapshot and copy-on-write shared devices — addressing kernel panics/deadlocks that plain container sandboxes suffer under aggressive agents. Scale: 51,219,741 sandboxes built across 1,505,678 images; checkpoint/resume at 133ms/49ms; up to 6.5× memory overcommit. Open-sourced (`kvcache-ai/AgentENV`) as an E2B-compatible sandbox runtime — ships the sandbox, not an RL loop; bring your own trainer. The report names Kimi Code, Claude Code, Codex, [[openclaw]], and Hermes as harnesses the agent-RL loop can instantiate as training scaffolds.

Compare to other agentic-RL infra: [[polar-rl-harness]] (NVIDIA) takes a harness-agnostic proxy-interception approach rather than sandbox-centric; [[llamarl]] (Meta) is a production async RL framework focused on colocation and off-policy handling rather than sandbox isolation. AgentENV's contribution is orthogonal — sandbox-level pause/fork/snapshot primitives, not the RL algorithm or scheduler itself.

## Results

- 88.3% Terminal-Bench 2.1 (vs. GPT-5.6 Sol 88.8%)
- 42.0% SWE-Marathon (vs. Claude Fable 5's 35.0%)
- 91.2% BrowseComp (top score, independent numbers agree)
- Artificial Analysis Intelligence Index v4.1: 57.1, #4 of 580 models — behind Claude Fable 5 (59.9) and GPT-5.6 Sol (58.9), ahead of Claude Opus 4.8 (55.7); next-best open-weight model GLM-5.2 trails at 51.1
- Headline efficiency claim: 2.5× training-FLOPs efficiency over Kimi K2 at matched validation loss (fitted scaling-law curves), credited jointly to architecture/data/recipe
- Named weakness: trails frontier labs "by wide margins" on HLE-Full and CritPt research-reasoning benchmarks

## Novelty vs. prior work

Recombination and refinement, not a clean-sheet architecture. KDA itself was already public via Kimi Linear at 48B-A3B scale; K3's contribution is the bounded gate (kernel-motivated) and running the operator at 2.78T scale as the majority (69/93) attention layer. MLA is unmodified DeepSeek-V2. The shared/routed MoE split is DeepSeekMoE; QB is a new refinement of DeepSeek-V3's aux-loss-free bias update (single-pass histogram quantile vs. fixed-step sign search). MoonEP's guaranteed-S×K dispatch via dynamic redundant experts is new relative to DeepEP (sizes for worst-case S×K×R) and ECHO/UltraEP (preset redundancy, can stall without a feasible plan). AgentENV's dirty-page-tracking memory snapshot and copy-on-write shared devices are new open infrastructure filling a real gap. MOPD is on-policy distillation extended to multiple domain/effort-specific teachers.

## Reproducibility

Weights: [moonshotai/Kimi-K3 on Hugging Face](https://huggingface.co/moonshotai/Kimi-K3), full 2.78T params released. Code released for all three named infra pieces: [FlashKDA](https://github.com/MoonshotAI/FlashKDA) (CUTLASS kernels — forward-only prefill, bf16, fixed head-dim 128; backward/decode/context-parallel planner closed), [MoonEP](https://github.com/MoonshotAI/MoonEP) (CUTLASS CuTe DSL), [AgentENV](https://github.com/kvcache-ai/AgentENV) (Rust/Firecracker sandbox — ships the sandbox, not the RL loop). 47-page technical report with named figures/tables cited throughout. Independent third-party benchmark (Artificial Analysis) corroborates lab-reported numbers. Adoption signal is early: Kimi Linear (the KDA precursor) already had community uptake (`flash-linear-attention` ships a maintained `fla.ops.kda` backend); AgentENV was developed "in collaboration with our partners," implying at least one external group already invested; no independent replication of K3 as a whole reported yet.

## Source

- `raw/research/weekly-2026-08-01/01-kimi-k3-architecture.md`

## Related

- [[gated-deltanet-2]] — KDA is a tied-gate special case of its erase/write-gate decomposition; K3 is the frontier-scale production instance.
- [[deepseek-v4]] — parallel hybrid-attention MoE design (CSA+HCA vs. KDA+MLA) built on the same MLA lineage, same KV-cache-reduction goal.
- [[mamba-3]] — parallel line in the DPLR/gated-recurrence family that KDA also descends from.
- [[openclaw]] — named as one of the agent harnesses K3's agentic-RL loop can instantiate as a training scaffold.
- [[polar-rl-harness]] — comparison: harness-agnostic proxy-based agentic-RL infra vs. AgentENV's sandbox-centric approach.
- [[llamarl]] — comparison: production async RL infra design choices (colocation, off-policy handling) vs. AgentENV's sandbox isolation.
