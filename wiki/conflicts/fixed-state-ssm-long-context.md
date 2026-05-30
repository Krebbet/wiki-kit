# Fixed-State SSMs at Extreme Context

**Status:** open. Pre-flagged from radar-2026-04 ingest. SSM-side source not yet captured.

## Position A — Fixed-size recurrent state cannot capture rich long-sequence information

**Source:** [[titans-miras]] (Google Research blog).

**Claim:** Fixed-size recurrent states (Mamba-2, SSMs) *"cannot adequately capture the rich information in very long sequences."* Hence Titans replaces fixed-size compressed state with a learnable network (deep MLP memory module) trained online via a surprise gradient.

**Basis:** Second paragraph of intro and "Conclusion" section.

[[nested-learning]] extends this — Hope (self-modifying Titans + CMS) holds long-context performance to **10M tokens** on BABILong where fixed-state ARMT and even Titans (without CMS) degrade after 1M.

### Position A — formal proof added

[[ssm-tool-use-length-generalization]] (Apple, ICLR 2026 Oral, arXiv:2510.14826) **proves Theorem 2.1**: for any GSSM (Mamba-1/2, LSTM, GRU, Linear Transformer, RetNet, H3, local-attention Transformer), in CoT-only or single-turn-tool-use settings, error ≥ 1 − α for sufficiently large problem size n. This converts what had been the Titans/Hope assertion into a formal impossibility result for fixed-memory recurrent architectures on long-form generation. The result is empirical-grounded (Pythia 10→20 digit addition, Mamba/LSTM length-bounded on Hanoi past training depth) — it isn't a worst-case bound only.

## Position B — Fixed-state SSMs are sufficient at extreme context (with the right design)

### B (partial, hybrid-only) — [[mamba-3]] (CMU/Princeton/Together/Cartesia, arXiv:2603.15569, 2026-04-27)

**Claim (partial defence):** Mamba-3 *concedes* the retrieval weakness of pure fixed-state SSMs — explicit acknowledgement of *"natural retrieval-based weaknesses of fixed state-size"* (§4.1.2) — and **shifts the battleground to hybrids**. Mamba-3 layers interleaved with attention match or exceed pure-Transformer baselines on retrieval (Table 4: SWDE / SQuAD / FDA / TriviaQA / NQ / DROP / NIAH).

This is *not* a defence of pure fixed-state SSMs against Position A. It is a partial Position-B variant: "fixed-state SSMs are sufficient *if* paired with attention layers". Pure-Mamba-3 still degrades at retrieval-heavy long context.

### B (decoupled-gate fixed-state recurrent) — [[gated-deltanet-2]] (NVIDIA, arXiv:2605.22791, 2026-05-25)

**Claim (strongest pure-fixed-state defence yet):** the long-context retrieval weakness of fixed-state recurrence is an artifact of the *update rule*, not of fixed-state capacity. Gated DeltaNet / KDA use a single scalar gate β_t that ties "how much to erase" to "how much to write"; GDN-2 decouples them into two channel-wise gates — a key-axis erase gate b_t and a value-axis write gate w_t — recovering GDN/KDA as tied-gate special cases at the *same* state size.

**Empirical:** at 1.3B / 100B FineWeb-Edu, in **pure recurrent mode (no attention layers)**, GDN-2 beats Mamba-2, Gated DeltaNet, KDA, and both Mamba-3 SISO and MIMO on aggregate LM + commonsense (recurrent avg 53.11 vs Mamba-3 MIMO 52.39). The gap is largest exactly where Position A predicts fixed states fail — multi-key retrieval: recurrent MK-NIAH-1 @4K **37.8 vs ≤28.0** for every baseline (KDA next-best). Ablation: making *only* the erase gate channel-wise (scalar write) recovers most of the retrieval gain → update-rule specificity, not raw state size, is the lever.

**Where this sits:** the closest entry yet to the long-vacant *orthodox* Position-B slot — a fixed-state recurrent model defending fixed-state design on retrieval — but it wins by changing the *update rule*, not by enlarging or learning the state (contrast Titans' learnable deep-MLP memory). It directly rebuts [[mamba-3]]'s concession that pure fixed-state SSMs carry "natural retrieval-based weaknesses": at matched scale, pure-recurrent GDN-2 closes much of that gap without adding attention. It does **not** touch Apple's Theorem 2.1 — GDN-2's RULER numbers are in-distribution retrieval, not the formal 1000-digit-style length-extrapolation the theorem bounds.

### B (tool-augmented) — [[ssm-tool-use-length-generalization]] (Apple, ICLR 2026 Oral, arXiv:2510.14826, 2026-04-30)

**Claim:** Don't change the SSM. Don't add attention. Add an interactive (multi-turn) memory tool.

**Theorem 2.2 (constructive):** there exists a memory-tool oracle (pointer-based read/write + left/right moves — a Turing-machine tape interface) and a training-data construction such that a simple GSSM learning algorithm achieves length generalization on *any* computationally tractable long-form generation task.

**Empirical:** Mamba-1.4B trained on ≤5-digit addition extrapolates to **1,000-digit addition at 100%** (Figure 2 right). Logical Graph: 10 → 1,000 nodes at 98%. Coding: Mamba-1.4B finetuned on SWE-agent trajectories *maintains* accuracy on larger codebases beyond training distribution where Pythia degrades. Single-turn tool-use experiments confirm Theorem 2.1 empirically (both architectures fail).

**Where this leaves the conflict:** the orthodox-Position-B slot (a pure fixed-state SSM defending its long-context performance against Titans/Hope) remains uncaptured. The tool-augmented variant is a third path neither side originally considered, and it makes the Position-A "fixed states don't suffice" claim moot for downstream tasks: yes, fixed states don't suffice, *and* the architecture doesn't need to change — just bolt on the right tool interface.

### B (RL-trained memory overwrite) — [[memagent]] (ByteDance Seed / Tsinghua AIR, arXiv:2507.02259, ICLR 2026 Oral)

**Claim:** Keep the Transformer backbone, keep its attention, keep its KV cache as-is. Instead, train an *agent workflow* that reads documents in fixed-size chunks and overwrites a **1024-token plain-text memory buffer** at each step via Multi-Conv DAPO (a multi-conversation extension of DAPO/GRPO). The memory lives in ordinary context tokens; no architectural change to the base LLM.

**Empirical:** trained at 8K context window (32K documents), RL-MemAgent-14B extrapolates to **3.5M-token QA with <5% accuracy loss**. **>95% on 512K RULER** OOD. Beats Qwen2.5-Instruct-14B-1M and QwenLong-L1-32B by ~15–25 pp on extreme-length retrieval/reasoning at matched backbone class.

**Where this sits:** MemAgent has a *fixed-size state* (1024 tokens) and yet length-generalizes to 437× its training context. This is empirical evidence that the Position-A claim "fixed-size state cannot capture rich long-sequence info" is too strong as stated. The loophole is **RL-trained compression** — the model learns *what to keep* per overwrite, not by architectural induction but by outcome-reward optimization. Distinct from the Apple tool-augmented path (no read/write tape; the agent itself decides the keep/discard policy) and from the Mamba-3 hybrid path (no attention added beyond what the Transformer backbone already has).

### Position C — Transformer + nonlinear horizontal state (no SSM, no tool)

**Source:** [[sst-v2]] (Fifth Dimension, arXiv:2605.00206, May 2026).

**Claim:** A third path orthogonal to both the SSM line and the tool/memory-agent line: keep the Transformer backbone, keep attention, but **add a per-layer FFN-driven nonlinear Latent State Cache (LSC)** that streams a fixed-size d-dimensional vector across positions horizontally. The LSC is *fixed-size* (651 KB total, independent of context length) but its update is the Transformer's own pretrained GELU FFN — nonlinear, not linear-recurrent like a GSSM.

**Empirical:** **+15.15 pp GPQA-Diamond** (61.11% vs 45.96% fine-tuned baseline; 28% error reduction), **46% error reduction on GSM8K** (97.19% vs 94.77%), beats DeepSeek V3 671B and Gemma 2.0 Flash with 25× fewer params. Two-pass parallel training keeps the recurrence trainable; per-position approximation error O(α²) ≈ 6–12×10⁻⁴.

**Tension with Theorem 2.1:** the impossibility result in [[ssm-tool-use-length-generalization]] covers the *GSSM class* (Mamba-1/2, LSTM, GRU, linear-transformer, RetNet, H3, local-attention) with linear or near-linear dynamics. SST V2 is **not a GSSM** — it augments a Transformer rather than replacing attention, and its horizontal recurrence runs through a *nonlinear* per-layer FFN. Whether this distinction exempts SST V2 from Theorem 2.1's scope is open: the empirical out-of-distribution reasoning gains on GPQA-Diamond suggest the FFN nonlinearity provides more per-step representational power than the linear dynamics the theorem assumes, but no formal proof has been offered either way.

### Position C′ — Frozen Transformer + delta-rule online state (fixed 8×8, no SSM, no tool)

**Source:** [[delta-mem]] (δ-mem, arXiv:2605.12357, May 2026).

**Claim:** A fixed-size state even *smaller* than a typical SSM state — an **8×8 matrix per layer** (r=8) — is sufficient for substantial memory-heavy gains, *because the state feeds dynamic attention corrections rather than directly generating tokens*. Keep a frozen full-attention backbone; train only ~4.87 M new projection params (0.12%) via SFT; the gated delta-rule write S_t = Diag(λ_t)S_{t-1} + Diag(β_t)(v−S_{t-1}k)kᵀ does error-correction with controlled forgetting, and the readout adds low-rank Δq/Δo corrections to the frozen backbone's attention.

**Empirical:** Qwen3-4B-Instruct avg 46.79 → 51.66 (+4.87 pp); MemoryAgentBench ×1.31; LoCoMo ×1.20; LoCoMo TTL ~×1.93. Generalizes to Qwen3-8B and SmolLM3-3B (+10.88 pp).

**Tension with Theorem 2.1:** [[ssm-tool-use-length-generalization]]'s impossibility result binds the *GSSM class* with linear/near-linear dynamics on formal long-form-generation length-generalization tasks. δ-mem is not a GSSM (it augments a frozen Transformer, not replaces attention) and its delta-rule write is nonlinear in the gates; its reported gains are on softer memory-heavy QA (MemoryAgentBench/LoCoMo F1), not the formal task classes Apple bounds. Like [[sst-v2]] (nonlinear horizontal FFN state) and [[memagent]] (RL-trained plain-text overwrite), it sits outside the theorem's scope rather than refuting it. The three third-path entries differ in *how* the fixed state is updated: SST V2 = pretrained FFN; MemAgent = RL outcome-reward overwrite; δ-mem = supervised gated delta-rule into the attention pathway.

### B (orthodox) — nearest source is [[gated-deltanet-2]]

No source defends the *exact* Mamba-2 design for long context against Position A. [[gated-deltanet-2]] is the closest: it defends *fixed-state recurrence* generally (not Mamba-2 specifically), attributing prior failures to the scalar update gate rather than state capacity, and demonstrates strong pure-recurrent retrieval at matched scale. A defence of the canonical Mamba-2 design itself against [[titans-miras]] / [[nested-learning]]'s Position A remains uncaptured.

## Resolution rule when Position B arrives

Compare on shared long-context benchmarks (BABILong, RULER, NIAH variants) at matched parameter budgets and matched pretraining-token budgets. Note Titans' BABILong claims are **unreplicated** (source is a blog, not third-party run).

Worth distinguishing two sub-claims:
- *Information-theoretic*: a fixed-size state has bounded mutual information with arbitrarily long histories. Titans/Hope contest this with a *learnable* (not fixed) state.
- *Empirical*: at the scales we actually train, fixed-state SSMs degrade past some context length. The empirical claim is testable; the information-theoretic claim is a definitional matter.

## Related

- [[titans-miras]], [[nested-learning]], [[mamba-3]], [[gated-deltanet-2]], [[test-time-training]], [[ssm-tool-use-length-generalization]], [[sst-v2]], [[memagent]], [[delta-mem]]
- [[conflicts/long-context-attention-vs-recurrent-memory]] — adjacent (different opponent).
- [[conflicts/ssm-vs-associative-memory-taxonomy]] — separate Mamba-3-driven framing tension with [[nested-learning]].
- [[watchlist]] — Mamba-2, Gated DeltaNet, RWKV-7, RetNet not captured.
