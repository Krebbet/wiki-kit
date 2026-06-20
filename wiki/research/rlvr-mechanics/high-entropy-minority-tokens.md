# Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective RLVR

Wang et al. (arXiv:2506.01939, Jun 2025; NeurIPS 2025). Accepted NeurIPS 2025. Token-entropy analysis of RLVR reveals that only ~20% of tokens — those exhibiting high entropy in CoT rollouts — drive the effective gradient signal. These "fork tokens" are the decision points where the model steers toward different reasoning pathways. Restricting policy gradient updates exclusively to these high-entropy positions **matches full-gradient training on Qwen3-8B and significantly surpasses it on Qwen3-14B and Qwen3-32B** (up to +11.04 on AIME'25), exhibiting a strong scaling trend. The low-entropy 80% is not neutral noise — training on it exclusively degrades performance markedly.

## Key Finding: the 80/20 Rule, Operationalized

- In Chain-of-Thought reasoning traces, only a small fraction of token positions show high entropy; the majority are low-entropy (near-deterministic continuations once the direction is set).
- RLVR training **does not redistribute entropy broadly** — it largely preserves the base model's entropy pattern, concentrating adjustments at already-high-entropy positions.
- The effective causal contribution of the full gradient signal is almost entirely attributable to the high-entropy minority.
- Training exclusively on the low-entropy 80% produces a **marked performance decline** — ruling out the interpretation that the majority tokens are inert. They are actively harmful to restrict to.

The 80/20 framing: 20% of tokens (high-entropy "forks") account for ~100%+ of the learning benefit, and training on the remaining 80% hurts.

## Method: Entropy-Gated Gradient Restriction

**Fork token identification.** For each position $t$ in a CoT rollout, compute token entropy $H_t$ under the current policy (or base model). Positions with $H_t > \tau$ are "fork tokens" — the model is genuinely uncertain about which reasoning direction to take.

**Gradient mask.** During RLVR policy gradient updates, zero the gradient at all positions with $H_t \leq \tau$. Only fork-token positions receive gradient updates. The threshold $\tau$ selects approximately the top 20% highest-entropy positions.

**Training regime unchanged otherwise.** The method is a drop-in modification to standard RLVR (e.g., GRPO/PPO): same reward signal, same rollout sampling, same advantage estimation — only the per-token gradient application is gated.

This is a **training intervention**, not a post-hoc analysis: the entropy gate is applied *during* gradient computation, not retrospectively.

## Results

Evaluated on Qwen3-8B, Qwen3-14B, and Qwen3-32B base models; benchmarks AIME'24 and AIME'25.

| Model | vs. full-gradient RLVR (AIME'25) | vs. full-gradient RLVR (AIME'24) |
|---|---|---|
| Qwen3-8B | ≈ parity | ≈ parity |
| Qwen3-14B | **+4.79** | **+5.21** |
| Qwen3-32B | **+11.04** | **+7.71** |

Strong scaling trend: the larger the model, the more the entropy-gated approach outperforms full-gradient RLVR. Low-entropy–only training control confirms the 80% majority tokens actively hurt performance when trained on exclusively.

## Relation to [[rethinking-rl-sparse-selection]]

These papers are **complementary lenses** on the same underlying phenomenon, approached from opposite directions:

| | rethinking-rl-sparse-selection (Akgul et al., 2605.06241) | This paper (Wang et al., 2506.01939) |
|---|---|---|
| **Framing** | Post-hoc analysis: what does RLVR *actually change*? | Prospective intervention: where *should* the gradient go? |
| **Unit of analysis** | Token positions reranked by RL (1.0–4.1% of positions) | Token positions with $H_t > \tau$ (top ~20% by entropy) |
| **Key finding** | RL reranks only 1–4% of positions; always within base top-5; those positions have 5–12× higher entropy | Gradient restricted to top-20% entropy tokens matches or beats full-gradient; low-entropy tokens are actively harmful |
| **Entropy connection** | Reranked positions have 5–12× elevated entropy vs. trajectory mean — entropy *predicts* where RL acts | Entropy *gates* where gradient updates are applied during training |
| **Method output** | Mechanistic explanation + REASONMAXXER (offline RL-free alternative) | Entropy-gated RLVR (online, drop-in mask) |
| **Actionable output** | Offline contrastive CE on ~50 problems ($4–25) | Per-token entropy mask on standard RLVR rollouts |

The convergence is notable: Akgul et al. find empirically that RL concentrates at high-entropy positions (5–12× elevation); Wang et al. find prescriptively that restricting to those positions improves outcomes. Together they establish a two-sided case: **RL both naturally does and should restrict its effective updates to high-entropy fork positions**.

Where they diverge: rethinking-rl-sparse-selection finds the active set is 1–4% (positions actually reranked); this paper uses a wider 20% entropy gate. The difference likely reflects that the gate is a coarser proxy for "where the update matters" — many high-entropy positions may be gated in without contributing a reranking event, but also without hurting.

## Design Implications for Single-Sample Training

The fork-token finding is a direct design primitive for single-sample / low-data RLVR:

1. **Gradient budget concentration.** In the extreme single-sample setting, every gradient step is expensive relative to data. Fork-token gating reduces effective gradient computation cost while improving signal-to-noise — a double win at low sample counts.

2. **Entropy-based importance sampling for sparse data.** With one or few training examples, the signal from low-entropy (near-deterministic) token positions is close to zero. Identifying and concentrating on fork positions makes the update more informative per example.

3. **Gate source matters.** The paper uses the base or current policy's entropy to identify fork tokens. In single-sample settings where on-policy rollouts are limited, the base model's entropy (computed once, reused) is an efficient proxy — aligning with REASONMAXXER's frozen-$\pi_\text{base}$ gate.

4. **Scaling trend is encouraging.** The larger the model, the more entropy-gating helps over full-gradient. This suggests that as capacity increases, the wasted gradient signal from low-entropy positions scales up faster than the useful signal — making the gate more valuable at the model scales relevant to this wiki's target range (1–40B).

5. **Composition slot.** No captured paper combines entropy-gated gradient masking with single-sample reward. This is an open design slot: entropy-gated RLVR on 1–few reward signals, leveraging base-model entropy to identify fork positions without requiring large rollout batches.

## Source

- `raw/research/weekly-2026-06-19/05-high-entropy-minority-tokens.md`
- arXiv: https://arxiv.org/abs/2506.01939

## Related

- [[rethinking-rl-sparse-selection]] — complementary post-hoc analysis; reranked positions have 5–12× elevated entropy, convergent empirically with this paper's prospective entropy gate
- [[_overview]] — RL-as-selection-not-learning cluster; this paper adds the gradient-gating angle
- [[../weekly-briefs/2026-06-19]] — brought in by the 2026-06-19 weekly sweep
