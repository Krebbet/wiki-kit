# Coconut: Chain of Continuous Thought

Coconut (Hao et al., arXiv:2412.06769, Dec 2024) is a reasoning paradigm in which an LLM alternates between standard token generation ("language mode") and a **latent mode** where the last hidden state $h_{t-1} \in \mathbb{R}^d$ is fed directly as the next input embedding, bypassing decode-to-token and re-embed entirely. The result is a fully differentiable reasoning chain that lives in continuous space. Probing shows latent thoughts encode multiple candidate next-reasoning-step children simultaneously — implicitly performing BFS — without any explicit training for it. On logical reasoning benchmarks (ProntoQA, ProsQA) Coconut matches or exceeds CoT while generating far fewer tokens; it does not yet surpass CoT on GSM8k.

## Core mechanism

Let $x = (x_1, \ldots, x_T)$ be the input sequence. Standard language mode:

$$H_t = \text{Transformer}(E_t), \qquad M(x_{t+1} \mid x_{\leq t}) = \text{softmax}(W h_t)$$

where $E_t = [e(x_1), \ldots, e(x_t)]$ and $h_t = H_t[t, :]$.

**Latent mode** is delimited by special tokens `<bot>` (begin-of-thought) at position $i$ and `<eot>` (end-of-thought) at position $j$. For $i < t < j$ the input embedding sequence becomes:

$$E_t = [e(x_1),\, \ldots,\, e(x_i),\, h_i,\, h_{i+1},\, \ldots,\, h_{t-1}]$$

Each $h_{t-1}$ is the last hidden state of the previous forward pass — already processed by the final layer-norm so magnitudes are bounded. After $t \geq j$ the sequence reverts to token embeddings:

$$E_t = [e(x_1),\, \ldots,\, e(x_i),\, h_i,\, \ldots,\, h_{j-1},\, e(x_j),\, \ldots,\, e(x_t)]$$

The LM head $W$ is **not applied** during latent mode; $M(x_{t+1} \mid x_{\leq t})$ is undefined for $i < t < j$. Softmax projections can still be computed for probing purposes without being used for generation.

## Curriculum training

Training requires $N+1$ stages:

- **Stage 0:** Standard CoT fine-tuning — full language reasoning chain.
- **Stage $k$ ($k \geq 1$):** Replace the first $k$ language reasoning steps with $k \times c$ continuous thoughts ($c$ is a hyperparameter; $c = 1$ for logical reasoning, $c = 2$ for GSM8k). The cross-entropy loss is computed on the **remaining language tokens only**; questions and latent thoughts are masked. The objective does not ask the continuous thoughts to compress the removed language steps — it asks them to facilitate prediction of future reasoning.
- Optimizer state is reset between stages (following iCoT, Deng et al. 2024).

Without the curriculum (training directly in the final stage with all reasoning replaced by continuous thoughts) performance is no better than no-CoT. Curriculum is load-bearing.

For logical reasoning (max 6 steps): $N = 6$, each stage 5 epochs, final stage held until 50 total epochs. For GSM8k: $N = 3$ plus one additional stage that removes all remaining language reasoning, 6 epochs stage 0 / 3 epochs thereafter.

## Halt mechanism

**Begin:** `<bot>` is inserted immediately after the question tokens at inference time.

**End:** Two strategies for placing `<eot>`:

1. **Learned classifier:** A binary classifier trained on latent thought vectors decides when to terminate.
2. **Fixed count:** The number of continuous thoughts is fixed to match the final training stage.

Both perform comparably. Experiments use fixed-count (option 2) for simplicity.

## BFS emergence

By probing latent thoughts (forcing the model to decode language following an intermediate continuous thought), the paper shows:

- **Step 1:** High probability mass distributed across multiple candidate next-step children simultaneously — the model does not commit to one branch.
- **Step 2:** Probability mass narrows; the top candidate at step 2 may differ from the top candidate at step 1 (non-greedy selection).

Interpretation: continuous thoughts act as an implicit value function over nodes in the reasoning DAG, estimating each node's potential for reaching the target. Nodes closer to leaf nodes (lower height) receive sharper, more accurate probability estimates; nodes farther from leaves (higher height) exhibit more diffuse, uncertain estimates. This explains why deferring commitment until later steps improves performance on planning-heavy tasks.

## Relation to Huginn

Both Coconut and [[huginn]] implement a "hidden state as next input" feedback loop, but at different levels:

| | Coconut | Huginn |
|---|---|---|
| **Loop unit** | Full model stack | Single repeated block |
| **Loop dimension** | Sequence position (each thought = one new position $t$) | Depth (same position $t$, block applied $r$ times) |
| **Halt signal** | `<eot>` token (fixed count or binary classifier) | Per-position router decides number of block repetitions |
| **Recurrence type** | Sequence-level: $h_t \to e_{t+1}$ | Depth-level: $h_t^{(r)} \to h_t^{(r+1)}$ |

Both face the same halt problem: when to stop iterating. Coconut's `<eot>` mechanism is analogous to Huginn's depth router — both are learned halting decisions in continuous space, closely related to [[pondernet]] and [[universal-transformers]]. [[loopformer]] occupies similar territory (sequence-level looped transformers for length generalisation).

## Key results

Main experiments use GPT-2 as base model.

| Method | GSM8k Acc (%) | ProntoQA Acc (%) | ProsQA Acc (%) |
|---|---|---|---|
| CoT | 42.9 | 98.8 | 77.5 |
| No-CoT | 16.5 | 93.8 | 76.7 |
| iCoT | 30.0 | 99.8 | 98.2 |
| Pause Token | 16.4 | 77.7 | 75.9 |
| **Coconut** | **34.1** | **99.8** | **97.0** |
| Coconut w/o curriculum | 14.4 | 52.4 | 76.1 |

Coconut outperforms no-CoT on all benchmarks. Matches CoT on ProntoQA and ProsQA (and surpasses CoT on ProsQA). Does not yet surpass CoT on GSM8k, though it achieves a better efficiency–accuracy trade-off (fewer tokens for comparable accuracy). **ProsQA is introduced by the same authors** — the ProsQA superiority over CoT should be read with a self-evaluation caveat.

**Larger model ablations (GSM8k, $c = 1$):**

| Model | No-CoT | Coconut |
|---|---|---|
| Llama 3.2-3B | 26.0 | 31.7 |
| Llama 3-8B | 42.2 | 43.6 |

Gains are consistent but smaller than GPT-2. The authors attribute this to extensive language-focused pretraining making the latent-space transition harder — the method likely requires **latent-space pretraining** to fully generalise to large models.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G3** (token-conditional routing) | **High** | Canonical latent thought routing; `<eot>` is exactly learned halting in continuous space — the clearest demonstration of G3 extended to the depth/recurrence dimension. |
| **G1** (block isolation / swappability) | Not applicable | Coconut does not address block isolation. |
| **G2** (dynamic parameter allocation) | Not applicable | Coconut does not address parameter allocation. |

## Credibility

arXiv preprint (v1 Dec 2024, v3 Nov 2025). No peer-reviewed venue. Code not mentioned in source materials. Rigorous ablations: curriculum vs. no-curriculum, continuous thoughts vs. pause tokens, per-stage probing analysis, fixed vs. learned `<eot>`. Self-evaluation caveat on ProsQA (dataset introduced by same authors). Llama ablations confirm directional consistency but smaller gains — extrapolation to large models is uncertain and authors acknowledge latent-space pretraining as an open requirement.

## Source

- `raw/research/recurrent-reasoning/05-coconut-abs.md` (arXiv:2412.06769)
- `raw/research/recurrent-reasoning/08-coconut-pdf.md`

## Related

- [[huginn]] — depth-level recurrence via hidden-state feedback; halt via router vs. Coconut's `<eot>`; complementary perspectives on continuous-space iteration.
- [[loopformer]] — sequence-level looped transformers; structural sibling to Coconut's recurrence pattern.
- [[universal-transformers]] — early adaptive-depth recurrence; halt via ACT, conceptual ancestor of both Huginn and Coconut's halting problem.
- [[pondernet]] — learned halting in recurrent networks; closest formal antecedent to the `<eot>` binary classifier strategy.
- [[calm]] — inference-time adaptive depth in a single forward pass via confidence-based early exit; complementary approach to compute allocation (layer-depth vs. sequence-level latent steps).
- [[mod]] — token-conditional routing around blocks; orthogonal axis (spatial routing) to Coconut's temporal/depth recurrence.
