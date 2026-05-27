# Experiment 1: Router-as-Static-Path (Replication Baseline)

**Status:** Proposal / Pre-experiment  
**Goal family:** G3 (token-conditional routing)  
**Date:** 2026-05-26

---

## Motivation

The long-term objective is an LLM that routes freely through a pool of shared blocks and halts whenever it decides computation is complete — replacing the fixed layer-by-layer execution stack with a learned, dynamic traversal. Before training routing over heterogeneous blocks (which requires solving block isolation, routing, and block diversity simultaneously), we need a clean baseline: *can a trained router replicate a known, static execution path?*

This experiment answers that question while leaving the weights frozen. If a router cannot replicate the static path of a Loop LLM with its own weights frozen, none of the harder problems are tractable.

---

## Why a Loop LLM as Base

A Loop LLM repeatedly applies the **same block** N times in sequence. This is the ideal testbed for Experiment 1:

- The routing problem is maximally simplified: the router only needs to learn "execute this block, then this block, ..., N times, then stop."
- The block weights are already shared, so there is no block identity to learn — only execution count and halt timing.
- The static baseline is unambiguous: N iterations of the same block, all tokens synchronized, fixed halt after step N.

**Base model: Huginn** (Geiping et al., 2025, arXiv:2502.05171). A pretrained depth-recurrent decoder LM that reuses a single transformer block for a fixed N iterations at each forward pass. Pretrained on 800B tokens, 3.5B parameters, weights released at `tomg-group-umd/huginn-0125`; code at `seal-rg/recurrent-pretraining`. Multiple 2025 papers analyze its internals, giving strong prior work to reference. Classical Universal Transformers (Dehghani et al., 2019) are conceptually equivalent but have no modern pretrained decoder checkpoint — they would require training from scratch.

**Lighter alternative: Parcae** (Prairie et al., 2026, arXiv:2604.12946). Checkpoints from 140M upward released at `SandyResearch/parcae-*`. Use if 3.5B is too large for the available GPU budget. Note: Parcae introduces a spectral-norm constraint for training stability — this is relevant when we later unfreeze weights, less so for frozen-weight router training.

---

## Experiment Design

### Setup

| Component | Choice | Rationale |
|---|---|---|
| Base model | **Huginn** (Geiping et al., 2025) — `tomg-group-umd/huginn-0125` | Pretrained depth-recurrent decoder LM (3.5B params, 800B tokens); released weights; reuses a single block N times; active community follow-up. Recommended over classical Universal Transformer (no pretrained checkpoint; encoder-only; toy-scale). Parcae (`SandyResearch/parcae-140m`) is a lighter alternative if 3.5B is too large. |
| Layer weights | **Frozen** | Isolates the router as sole trainable component |
| Training signal | KL divergence to frozen UT output distribution | Imitation objective; avoids confounding with task loss |
| Dataset | Same distribution as UT pretraining, or a held-out text corpus | Router sees same regime the weights were optimized for |

### Router Architecture

A lightweight head on top of the current hidden state, producing a halt probability at each step:

```
h_t^(k)  →  LayerNorm  →  Linear(d_model → d_model/4)  →  ReLU  →  Linear(d_model/4 → 1)  →  σ  →  p_halt^(k)
```

Halt at step K if `Σ_{k=1}^{K} p_halt^(k) ≥ threshold` (PonderNet-style geometric prior) or if `p_halt^(k) > 0.5` (greedy).

### Routing Granularity — First Decision Point

Three options with different tradeoffs:

**Option A — Per-sequence routing (recommended for v1)**  
One halt decision per step; the same decision applies to all tokens in the sequence. All tokens are always synchronized. No attention mask complications. Simplest to implement and debug.

**Option B — Per-token routing**  
Each token independently accumulates halt probability. Most expressive — matches the long-term target where different tokens need different compute. However, creates a hard problem: if token `j` has halted at step 3 and token `i` is still running at step 5, what does token `i` attend to? (See §"Attention Complications" below.)

**Option C — Per-position routing (batch-synchronized)**  
Halt decisions are per-token but applied in lockstep — a token halts at the first step where its individual halt probability crosses threshold *and* no later token in the batch forces it to continue. Useful for decoder-only generation where the current token is always the last.

**Start with Option A.** If the router successfully replicates the static path under Option A, run a follow-on with Option B to measure the attention complication cost.

### Training Objective

```
L = L_imitation + λ * L_budget

L_imitation = KL( p_router(y|x) || p_static(y|x) )
L_budget    = max(0, E[steps_taken] - N_target)   # optional; set λ=0 first
```

λ=0 for Phase 1a. Once the router successfully replicates the static path (convergence), add λ > 0 in Phase 1b to see if the router finds shorter paths that preserve output quality.

### Success Criteria

| Metric | Pass threshold |
|---|---|
| KL(router \|\| static) on val set | < 0.01 nats/token |
| Perplexity delta (router − static) | < 0.5 |
| Router halt distribution (with λ=0) | Concentrated at step N (≥ 90% of sequences) |
| Router halt distribution (with λ>0) | Mean steps < N with perplexity delta < 1.0 |

---

## Attention Complications (Per-Token Routing)

This is the central technical risk for anything beyond Option A. It deserves explicit treatment now even if we defer it.

**The problem:** In a standard transformer, the KV cache at each layer is indexed by sequence position. In a looped architecture with per-token routing, different tokens may be at different "steps" when they compute attention. Three candidate solutions:

1. **Synchronized stepping (strict):** All tokens advance together — effectively Option A. Simple, but forfeits per-token compute control.

2. **Step-indexed KV cache:** Treat each (position, step) pair as a unique key-value entry. Token at step k can attend to any token at step ≤ k at any prior position. This generalizes causal masking to a 2D (position, step) mask. Expensive in memory; attention complexity grows with steps × sequence length.

3. **Recurrent hidden-state accumulation (Block-Recurrent style):** Each token maintains a running state that is updated at each step, and attention is only over the previous step's states (not all steps). This recovers the sequential structure and makes the KV cache step-independent, but loses full self-attention across steps.

The choice here will have large downstream consequences for how routing generalizes to a heterogeneous block pool. **Flag for dedicated investigation after Experiment 1 Option A succeeds.**

---

## Differentiable Halting — Mechanism Choice

Three approaches in the literature:

| Approach | How it works | Pros | Cons |
|---|---|---|---|
| ACT (Graves 2016) | Halt probability accumulated per step; remainder trick for fractional halt | Deterministic, differentiable | Unstable gradients, sensitive to prior |
| PonderNet (Banino 2021) | Geometric prior on step count; KL term against prior | More stable training, principled prior | Adds a KL term that competes with imitation objective |
| Gumbel-softmax / STE | Discrete halt as one-hot, relaxed during training | Fully discrete at inference | High variance gradients, mode collapse risk |

**Recommend PonderNet-style** for v1: the geometric prior on halt step gives the router a natural starting point (halt around N/2 by default) and the KL term is easy to zero out when λ=0 to get pure imitation. If the prior interferes, fall back to ACT.

---

## Technical Challenges

### 1. Gradient flow through a discrete halt decision *(blocking — must solve before training)*

The halt signal is inherently discrete. All three mechanisms in the table above have failure modes: ACT's remainder trick has documented gradient instability; PonderNet's geometric prior KL term competes with the imitation objective (the prior wants the router to halt around N/2, the imitation wants it to halt at N); Gumbel-softmax has mode collapse risk (router collapses to always-halt or never-halt). The proposal recommends PonderNet-style with λ_prior=0, but this removes the stabilising prior and leaves a raw continuous approximation to a discrete decision — stability of this configuration at 3.5B is untested.

**Mitigation:** profile gradient magnitudes through the halt head in the first 100 steps; if they blow up, fall back to ACT with a small ponder cost penalty.

### 2. Hidden-state observability: does $h_t^{(k)}$ signal "I should stop"? *(confirmed severe — mitigation known)*

[[research/mechanistic-looped-lms]] proves this is not a soft concern: input-injection LMs (Huginn) converge to **cyclic fixed points within $k \approx 1$–$2$ recurrences post-prelude** (Prop. 4.1, with full induction proof in App. A). For $k \geq 2$, $h^{(k)} \approx h^{(k+1)}$ to near-exact precision — a 2-layer MLP has no signal to distinguish "step 3 of 8" from "step 7 of 8". Attention patterns freeze as a corollary (Prop. 4.2, Lipschitz bound $L_\text{sm} = 1/2$).

**Mitigation (known, tested):** [[research/loopformer]]'s sinusoidal $(t, \Delta t)$ Fourier step conditioning breaks the cyclic fixed-point symmetry by injecting a discriminating step signal via AdaLN zero-init. This is the required fix before a halt head is viable on a Huginn base. Practically: add $(t, \Delta t)$ step conditioning to the halt head's input before any training attempt — do not attempt to train the halt head on raw $h^{(k)}$ for Huginn-based routers.

### 3. Huginn's internal loop architecture vs. router insertion point *(architecture compatibility)*

Huginn's recurrent depth design includes specific gating choices for stable training. The router must intercept at the correct point in Huginn's loop — after the block's residual output but before the next iteration's entry point. The exact insertion point is not in the wiki yet (paper pending ingest). Getting this wrong means the router operates on stale hidden states or interferes with Huginn's internal mechanisms.

**Mitigation:** read `seal-rg/recurrent-pretraining` forward-pass code before implementing; identify the exact loop unrolling point.

### 4. Training cost: double forward pass *(computational, manageable)*

Computing $\text{KL}(p_\text{router} \| p_\text{static})$ requires running the frozen model to get $p_\text{static}(y|x)$ for every batch, then the router-controlled model for $p_\text{router}(y|x)$. At 3.5B params this is ~2× the forward-pass cost per training step.

**Mitigation:** pre-compute and cache $p_\text{static}$ logits over the training corpus before router training begins. Valid for the entire frozen-weight phase.

### 5. The trivial solution trap *(optimisation risk — structural)*

With λ=0, the global optimum is "always run exactly N steps" — also the trivially learnable solution. A router that learns this passes Exp 1's success criteria while learning nothing about routing. When Phase 1b introduces λ>0, a router that only learned "run N steps" will have no gradient signal for routing decisions and may fail to generalise to Exp 2.

**Mitigation:** after Phase 1a convergence, probe whether the router's penultimate activations encode step-count vs. sequence-complexity information. A probe classifier for step index should be near-perfect; one for sequence difficulty should be near-random if the router is a pure counter. Use this to decide whether Phase 1b is meaningful.

### 6. Attention semantics across loop iterations *(architecture, load-bearing for Exp 2)*

Already covered in §"Attention Complications" above. The key addition: the choice of KV cache semantics (Option A synchronized vs. Option B step-indexed vs. Option C recurrent) constrains all future experiments. [[concepts/token-conditional-routing]] notes that token-level routing already creates load-balancing pressure that impedes task-level specialisation (§4.2.3 caution from [[research/modular-deep-learning]]); variable-depth attention compounds this.

**Mitigation:** commit to Option A for Exp 1; design the KV cache interface to be swappable before Exp 2.

### 7. Position encoding accumulation across iterations *(subtle, deferred to Exp 2)*

Standard position encodings (sinusoidal, RoPE) are added at each iteration. If the router halts a token at step $k < N$, the token's final representation saw the position encoding $k$ times instead of $N$ times, changing the effective scale of positional information in the residual stream. Benign under Option A (all tokens run N steps), but breaks when steps vary.

---

## Key Unknowns This Experiment Will Resolve

1. **Can a lightweight router learn the static path from KL supervision alone?** (The core question.)
2. **Does the router discover the static path exactly, or does it find functionally equivalent shorter paths?** (If shorter paths with ≤ 0.5 PPL delta appear *before* adding the budget penalty, this is a strong positive signal.)
3. **What is the router overhead as a fraction of block forward-pass cost?** (Should be < 5% to be worth it.)
4. **Does gradient flow through the halting mechanism cause instability?** (PonderNet vs. ACT stability comparison.)
5. **At what granularity does the router need to operate to replicate the static path?** (Option A likely sufficient; Option B may be needed for shortcuts.)

---

## What This Does NOT Test

- Routing through heterogeneous (non-tied) blocks — that is Experiment 2.
- Router behavior after joint fine-tuning with blocks — Experiment 3.
- Generalizing to sequences outside the training distribution.
- Memory-efficient implementation for production (KV cache management with variable steps).

---

## Research Calls

Papers already in the wiki that are directly relevant:

- `wiki/research/calm.md` — per-token early exit with confidence threshold; halt mechanism reference
- `wiki/research/layerskip.md` — layer-skipping with early exit loss; training tricks for sparse execution
- `wiki/research/mod.md` — token routing through variable depth; capacity framing
- `wiki/research/lora.md` — if router needs to be more expressive than a linear head

Papers **not yet in the wiki** that need to be ingested before starting implementation:

| Paper | Why needed | Priority |
|---|---|---|
| **Universal Transformers** (Dehghani et al., 2018) | The base architecture; defines ACT, weight-tying, the static loop we replicate | **Critical** |
| **Adaptive Computation Time** (Graves, 2016) | The original halt mechanism; defines remainder trick and ponder cost | **Critical** |
| **PonderNet** (Banino et al., 2021, NeurIPS) | Modern differentiable halting; more stable than ACT; geometric prior | **Critical** |
| **Looped Transformers as Programmable Computers** (Giannou et al., 2023) | Alternative loop LLM framing; may be a better base than classic UT | High |
| **Depth-Adaptive Transformer** (Elbayad et al., 2020) | Per-token early exit in seq2seq; directly addresses the attention mask problem with variable-depth tokens | High |
| **Block-Recurrent Transformers** (Hutchins et al., 2022) | Recurrent hidden state across loop iterations; relevant if we go with solution 3 for attention complications | Medium |
| **Deep Equilibrium Models (DEQ)** (Bai et al., 2019) | Fixed-point framing of looped networks; router could learn to halt at convergence rather than at a fixed step | Medium |

---

## Open Questions Before Starting

1. **Base model confirmed:** Huginn (`tomg-group-umd/huginn-0125`). If GPU budget is constrained, fall back to Parcae-140M or Parcae-770M. Do not train from scratch — the frozen weights need to encode a real distribution for imitation to be meaningful.
2. Per-sequence (Option A) first, then per-token (Option B) — agree on this ordering before implementation.
3. KL supervision vs. direct next-token CE loss against router outputs — are these equivalent? (They are if we assume the static UT's output distribution is the target, not the true data distribution.)
4. PonderNet or ACT — need to read both before deciding.
