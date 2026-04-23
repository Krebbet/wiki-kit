# MCPO vs Dr. GRPO — is std-removal a complete fix for the difficulty-bias problem?

## Positions

**Position A — Dr. GRPO ([[../research/rl-optimizers/dr-grpo]]).** Removing std normalisation from GRPO advantages (along with the per-response length normalisation $1/|o_i|$) yields an *unbiased*, difficulty-invariant objective. "Dr. GRPO" = GRPO *without* the std and length terms. The resulting training is claimed to be bias-free and achieves SOTA on AIME 2024 via Qwen2.5-Math-7B in 27h on 8×A100.

**Position B — MCPO ([[../research/rl-optimizers/mcpo]]).** Removing std is *necessary but not sufficient*. After std removal, the effective per-query weight is still proportional to $p(x)(1 - p(x))$ where $p(x)$ is the current policy's success rate on prompt $x$ — so the weight still peaks at $p=0.5$ and falls off toward the boundaries. The difficulty bias therefore *persists*: majority-correct prompts (high $p$) receive weaker weight than interior-difficulty prompts, and all-correct prompts ($p = 1$) produce zero gradient. MCPO's fix (Sec 4.2, Eq 6, citing DisCO [15]) is to additionally rescale the advantage denominator for $p > 0.5$, flattening the query-weight curve.

## Resolution rule

*(Open — no ruling yet.)*

The two positions *agree* on the diagnosis (the std term introduces difficulty bias that favours interior-difficulty prompts). They *disagree* on whether removing std is enough, with MCPO providing a concrete algebraic argument that a $p(1-p)$ weight survives the removal. MCPO's analysis is extended by the additional advantage-denominator rescaling, which Dr. GRPO does not perform.

**What would resolve it:** an ablation that runs (a) GRPO with std, (b) Dr. GRPO (no std, no length normalisation), (c) MCPO (no std, rescaled advantage denominator), on the same base model and benchmark, and compares both pass@1 and the mastered-prompt-fraction trajectory across training steps. MCPO reports this comparison for a subset of conditions (Fig 5); a fuller ablation would settle the question.

**If Position B (MCPO) holds:** Dr. GRPO's claim to bias-elimination is overstated; the project's single-sample method should prefer MCPO's objective as the less-biased option, particularly at $G$-small / post-saturation regimes where $p \to 1$ collapses the gradient.

**If Position A (Dr. GRPO) holds:** the $p(1-p)$ residual is empirically small enough to ignore; the simpler Dr. GRPO objective is preferred for compute/debug reasons.

## Source

Surfaced via the 2026-04-23 weekly sweep. MCPO (arXiv:2604.16972) explicitly critiques Dr. GRPO (arXiv:2503.20783) in its Sec 4.2 — see the basis quote in [[../research/rl-optimizers/mcpo]]'s `## Conflicts raised` section.

## Related

- [[../research/rl-optimizers/mcpo]] — Position B paper
- [[../research/rl-optimizers/dr-grpo]] — Position A paper
- [[../research/rl-optimizers/dapo]] — adjacent (DAPO's Token-Level PG Loss also addresses the length-bias piece)
- [[../research/single-sample-rl-finetuning/data-efficiency-rft]] — DOTS' $p(1-p)$ theorem is the underlying gradient-magnitude result both positions rely on
- [[../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep
