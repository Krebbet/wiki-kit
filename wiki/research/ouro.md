# Ouro (Scaling Latent Reasoning via Looped Language Models)

Ouro (Zhu et al., arXiv:2510.25741, Oct 2025; ByteDance Seed + UC Santa Cruz / Princeton / Mila) is a family of pre-trained **Looped Language Models (LoopLM)** that build iterative latent reasoning into pre-training rather than deferring it to chain-of-thought post-training. A single weight-tied decoder block is applied recurrently for up to $T_{\max}=4$ steps; an exit gate learned in two stages controls per-input depth allocation. Trained on 7.7T tokens, Ouro-1.4B matches Qwen3-4B and Ouro-2.6B matches/beats Qwen3-8B and Gemma3-12B on most benchmarks, at 2–3$\times$ parameter efficiency. Mechanistic experiments (Capo/Mano synthetic tasks) show the gains come from **knowledge manipulation** (multi-hop composition), not increased knowledge storage capacity ($\approx 2$ bits/parameter regardless of loop count). Weights are open-source at `ouro-llm.github.io`.

## Architecture

**Backbone.** Standard decoder-only Transformer; no exotic sub-modules beyond the recurrence.

- **Ouro-1.4B:** 24 layers, hidden size 2048, MHA + SwiGLU FFN, RoPE positional embeddings.
- **Ouro-2.6B:** 48 layers (same hidden size); obtained by **layer duplication upcycling** of the 24-layer checkpoint — the recurrent weight-tying makes this unusually smooth relative to standard transformer upcycling.
- **Sandwich normalization:** `RMSNorm` placed before both attention and FFN sub-layers (borrowed from Huginn / Geiping et al. 2025). Cited as critical for training stability under deep recurrence.
- **Vocabulary:** SmolLM2 tokenizer, 49,152 tokens — optimized for English/code; Chinese support was present in Stage 1 but removed from Stage 2 onward (no Chinese vocabulary slots).
- **Recurrent depth:** $t \in \{1,\ldots,T_{\max}\}$; the full $N$-layer stack $\mathcal{M}$ is applied $t$ times:

$$F^{(t)}(\cdot) = \operatorname{lmhead} \circ \underbrace{\mathcal{M} \circ \mathcal{M} \circ \cdots \circ \mathcal{M}}_{t \text{ iterations}} \circ \operatorname{emb}(\cdot)$$

An LM head and exit gate are attached at every step. Training started at $T_{\max}=8$ (Stage 1a) but reduced to 4 after gradient instability; all reported results use $T_{\max}=4$.

## Adaptive Halting: Two-Stage Training

The gating mechanism is the paper's primary contribution and is the closest published implementation to what Experiment 1 (token-conditional halting over a recurrent block) aims to build.

**Exit gate.** A linear probe on the final-layer hidden state outputs an instantaneous exit probability $\lambda_t(x) = \sigma(\text{Linear}_\phi(h^{(t)})) \in (0,1)$. The discrete exit distribution is:

$$p_\phi(t \mid x) = \lambda_t(x) \prod_{j=1}^{t-1}(1 - \lambda_j(x)), \quad t < T_{\max}; \qquad p_\phi(T_{\max} \mid x) = \prod_{j=1}^{T_{\max}-1}(1 - \lambda_j(x))$$

At inference, exit occurs at the first step where $\operatorname{CDF}(t \mid x) \geq q$; threshold $q$ is a deployment-time knob.

### Stage I — Entropy-Regularized Pre-training

Without regularization, $p_\phi$ collapses onto $t = T_{\max}$ (self-reinforcing gradient). The objective prevents this:

$$\mathcal{L} = \sum_{t=1}^{T_{\max}} p_\phi(t \mid x)\, \mathcal{L}^{(t)} - \beta\, H(p_\phi(\cdot \mid x))$$

This is equivalent to a variational ELBO with a **uniform prior** over exit steps ($\pi_t = 1/T_{\max}$):

$$\mathcal{L}_{\mathrm{ELBO}} = \sum_t p_\phi(t \mid x)\,\mathcal{L}^{(t)} + \beta\,\mathrm{KL}(p_\phi \,\|\, \pi)$$

The uniform prior is deliberately depth-unbiased; a geometric or Poisson-lognormal prior (as in [[pondernet]]) would softly favor early halting. $\beta$ was annealed from 0.1 (Stage 1a) to 0.05 (Stages 1b–4) to reduce conflicting gradients and give the model more freedom to discover useful depth patterns.

### Stage II — Focused Adaptive Gate Training

LM weights are **frozen**; only $\phi$ is updated. The gate is supervised on a per-token loss-improvement signal:

$$I_i^{(t)} = \max\!\left(0,\; \mathcal{L}_i^{(t-1)}_{\mathrm{stop}} - \mathcal{L}_i^{(t)}_{\mathrm{stop}}\right)$$

$$w_i^{(t)} = \sigma\!\left(k \cdot (I_i^{(t)} - \gamma)\right), \quad k=50.0,\; \gamma=0.005$$

where $w_i^{(t)} \approx 1$ recommends continuing and $\approx 0$ recommends exiting. The gate is trained via binary cross-entropy between predicted continuation probability $1 - \lambda_i^{(t)}$ and label $w_i^{(t)}$. This directly penalizes both **underthinking** (exit when gain is large) and **overthinking** (continue when gain has stalled). Ablations (Figure 5) confirm Stage-II-trained gate outperforms entropy-regularized-only gate by $\approx 2$–3 points MMLU at matched average exit round.

## KV-Cache Inference Strategy

Naively, $T_{\max}=4$ steps require 4$\times$ KV cache memory. During the **decoding phase**, reuse of the last step's KV cache achieves 4$\times$ memory reduction with $<0.3$-point accuracy loss:

| Strategy | GSM8K | MATH-500 | Memory |
|---|---|---|---|
| Full (4$\times$ cache) | 78.92 | 82.40 | 1.00$\times$ |
| **Last-step only** | **78.85** | **80.40** | **4.00$\times$** |
| Averaged | 78.73 | 78.52 | 4.00$\times$ |
| First-step only | 18.73 | 8.43 | 4.00$\times$ |

First-step reuse is **catastrophic** (GSM8K: 78.92 → 18.73). During **prefilling**, all four KV caches are required; reuse there causes $>10$-point GSM8K degradation.

## Empirical Results

**Base models** (evaluated with `lm-eval-harness`):

- Ouro-1.4B R4 vs. Qwen3-4B: BBH 71.02 vs. 70.95; GSM8K 78.92 vs. 72.86; MATH-500 82.40 vs. 59.60.
- Ouro-2.6B R4 vs. Qwen3-8B: MMLU-Pro 55.73 vs. 53.72; BBH 80.46 vs. 77.65; MATH-500 90.85 vs. 62.30.
- Ouro-2.6B also surpasses Gemma3-12B on reasoning-intensive tasks (BBH, MATH-500).

**Thinking models** (SFT on 8.3M reasoning examples, evaluated at $T=4$):

| Model | AIME24 pass@1 | AIME24 pass@10 | OlympiadBench | GPQA |
|---|---|---|---|---|
| Ouro-1.4B-Thinking-R4 | **65.0** | 83.3 | 71.6 | 45.5 |
| Ouro-2.6B-Thinking-R4 | 64.7 | **90.0** | **76.4** | 52.7 |
| Qwen3-4B (reference) | 61.3 | 75.0 | 73.2 | 54.5 |
| Qwen3-8B (reference) | **73.0** | 86.7 | 75.3 | **59.1** |

**Depth sensitivity.** Performance peaks at trained depth ($T=4$) and degrades gracefully during extrapolation ($T=5$–8). At $T=1$ on Thinking models, performance collapses (AIME24: 0.00 for 1.4B), confirming iterative refinement is load-bearing for complex reasoning.

## Mechanistic Finding: Knowledge Manipulation vs. Capacity

**Capo task (knowledge capacity).** Trained GPT-2-style models (1M–40M params) on synthetic biography memorization. Looped (4 steps) and non-looped iso-parameter models both converge to $\approx 2$ bits/parameter. Looping does **not** increase knowledge storage capacity; the parameter count is the direct capacity predictor.

**Mano task (knowledge manipulation).** Complex modular-arithmetic tree evaluation. Looped models ($k \otimes 12/k$, $k\in\{2,3,6\}$) consistently outperform iso-parameter non-looped baselines across all difficulty levels $L \in \{10, 16, 24\}$, and often match or beat iso-FLOP baselines. LoopLM has a better inductive bias for **parsing structured procedures** given fixed knowledge.

**Multi-hop QA.** Looped models learn 3-hop reasoning with fewer unique training samples and converge faster than non-looped iso-parameter models; sample efficiency advantage generalizes to natural-language compositional tasks.

**Theoretical result (Theorem 1, informal).** Fix $n$ as the maximum knowledge graph size $G$. There exists a one-layer transformer, independent of the context graph $G_{\mathrm{ctx}}$, that solves graph reachability $(s,t) \in G + G_{\mathrm{ctx}}$ with $O(\log_2 D)$ sequential loop steps, where $D$ is the diameter of $G + G_{\mathrm{ctx}}$:

| Method | Sequential steps |
|---|---|
| Discrete CoT | $O(n^2)$ |
| Continuous CoT | $O(D)$ |
| LoopLM (Universal Transformer) | $O(\log D)$ |

The exponential reduction in sequential steps stems from LoopLM computing all-pair connectivity in parallel across attention heads at each loop.

## Goal Relevance

| Goal | Relevance | Notes |
|---|---|---|
| **G1** (block isolation) | Medium | Ouro's weight-tied block is the extreme limit of block reuse — the same parameters everywhere — rather than isolation between distinct blocks. Demonstrates that deep iteration over a single shared block is viable at scale, but does not address swappability. |
| **G2** (dynamic parameter allocation) | Not applicable | Ouro iterates depth, not parameters; block parameter count is fixed across steps. |
| **G3** (token-conditional routing) | **High** | Stage II exit gate is exactly G3 instantiated in the depth dimension: a learned linear probe makes a per-input (and implicitly per-token) halting decision over a recurrent block pool. The two-stage training procedure (entropy-regularized pre-training + frozen-LM gate fine-tuning on loss-improvement signal) is the closest published blueprint for the adaptive-halt component of Exp 1. |

## Credibility

arXiv preprint only (v4, Nov 2025). Not peer-reviewed. ByteDance Seed + academic collaborators (Yoshua Bengio among supervisors). Strong ablation suite: Capo/Mano synthetic tasks with iso-parameter and iso-FLOP controls, depth sensitivity sweep ($T=1$–8), KV-cache ablation, early-exit strategy comparison. Honest disclosures:

- **Single tokenizer limitation:** SmolLM2 49K vocab, optimized for English and code; Chinese support dropped after Stage 1. Non-English and non-code capabilities are likely weaker than parameter-matched dense models with multilingual tokenizers.
- **Failed RL alignment:** RLVR (DAPO/GRPO) experiments did not improve over SFT checkpoint. Root cause: vLLM/SGLang fixed-execution-path rollouts are incompatible with LoopLM's variable-depth computation. Off-policy workaround (select exit token post-hoc from 4-step rollout) produced mismatch; fixed-4-step RL also failed to beat SFT. Infrastructure gap, not fundamental.

## Source

- `raw/research/recurrent-reasoning/01-ouro-abs.md` (arXiv abstract, arXiv:2510.25741)
- `raw/research/recurrent-reasoning/12-ouro-pdf.md` (PDF capture)

## Related

- [[huginn]] — shares sandwich normalization and recurrent-depth scaling motivation; Ouro cites Geiping et al. 2025 directly.
- [[universal-transformers]] — original weight-tied recurrent transformer (Dehghani et al. 2018); Ouro is the scaled-to-7.7T-tokens descendant.
- [[act]] — Adaptive Computation Time; precursor halting mechanism for recurrent networks.
- [[pondernet]] — geometric-prior ELBO for dynamic halting; Ouro's Stage I objective is the same ELBO with a uniform prior instead of geometric.
- [[calm]] — per-token early exit via confidence threshold; CALM exits at a layer boundary in a fixed-depth model whereas Ouro exits at a recurrence-step boundary in a looped model — complementary depth-routing approaches.
- [[parcae]] — related adaptive-depth inference work.
- [[rltt]] — recurrent latent-thought training; related latent reasoning paradigm.
- [[looprpt]] — related looped transformer with recursive parameter sharing.
