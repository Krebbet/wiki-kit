# Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive RLVR

Alibaba/Qwen team (Wang et al., NeurIPS 2025) show that restricting RLVR gradient updates to the ~20% of highest-entropy "forking" tokens matches or significantly beats full-gradient training, with gains increasing with model scale (+11.04 AIME'25 at Qwen3-32B).

## Source

- `raw/research/weekly-2026-06-03/02-high-entropy-tokens-rlvr.md` (arXiv:2506.01939, June 2025, NeurIPS 2025)

## Method

The paper analyzes token entropy patterns in CoT reasoning traces and identifies three key observations:
1. Only ~20% of tokens exhibit high entropy at any decoding step — these are "forking" tokens at genuine decision points.
2. RLVR training largely preserves the base model's entropy distribution; policy changes concentrate at the high-entropy positions.
3. Low-entropy tokens (the 80% majority) contribute noise, not signal, to the policy gradient.

Based on this, the authors propose masking policy gradient updates to exclude low-entropy tokens, updating only the high-entropy "forking" subset. The method is model-agnostic and implemented on top of a standard GRPO-style RLVR setup with verifiable math rewards.

## Results

Evaluated on Qwen3-8B, Qwen3-14B, Qwen3-32B:
- **Qwen3-8B**: forking-token training matches full-gradient RLVR.
- **Qwen3-14B**: +4.79 AIME'25, +5.21 AIME'24 vs. full-gradient baseline.
- **Qwen3-32B**: +11.04 AIME'25, +7.71 AIME'24 vs. full-gradient baseline.
- Training on the 80% low-entropy tokens alone causes marked performance decline, confirming asymmetric importance.
- Strong positive scaling trend: larger models benefit more from entropy-selective training.

## Novelty

[[reasonmaxxer]] established post-hoc that RL modifies only 1–4% of tokens at high-entropy positions. This paper closes the loop: it characterizes the entropy dynamics *during* RLVR (not post-hoc), confirms RLVR adheres to the base model's entropy structure, and proposes a training-time intervention — forking-token gradient masking — that yields measurable gains especially at larger scales. The scaling trend is a new empirical finding not previously reported.

**Measurement-frame note**: ReasonMaxxer reports 1–4% modified tokens (fraction where teacher reranks top-5); this paper uses a 20% entropy-percentile cut as the forking threshold. Different frames, not a contradiction.

## Related

- [[reasonmaxxer]] — tight cluster: ReasonMaxxer observes RL edits only high-entropy positions; this paper actively masks gradients on low-entropy tokens; together they form the "entropy-selective RL" cluster
- [[token-gradient-cancellation]] — DFPO argues shared low-signal tokens dilute gradient quality; entropy masking is an orthogonal but related mechanism to cancel low-value gradient contributions
- [[delta-token-credit]] — DelTA uses discriminative contrast to down-weight shared tokens; entropy masking achieves similar filtering via a different signal
- [[anti-self-distillation]] — PMI identity shows self-distillation suppresses high-entropy deliberation tokens; RL and SD act on the same token population in opposite directions
- [[spurious-rewards-rlvr]] — adds a fourth competing account of why RLVR gains occur; the entropy-masking result here assumes reward signal is genuine (challenges the spurious-rewards claim at scale)
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — this paper is evidence for Position A (sparse high-entropy tokens drive gains), now with a training-time intervention rather than just observation
