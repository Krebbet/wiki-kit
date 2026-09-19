# SP³O vs. the critic-free trend — is critic removal or critic repair the right response to PPO's critic problems?

## Positions

**Position A — critic-free trend ([[../research/rl-optimizers/_overview]], [[../research/rlvr-mechanics/deepseekmath-grpo]]).** The RL-for-LLM optimiser lineage (PPO → InstructGPT → DPO → GRPO → post-GRPO) is framed as convergent evidence that the critic is dispensable: GRPO drops PPO's value network $V_\phi$ entirely, substituting group-relative reward statistics as the baseline, motivated explicitly by the critic's cost (a value network of comparable size to the policy) and reliability problems. RLOO, DPO, and KTO all remove or sidestep the critic by different routes. The `_overview` page's "The critic is optional" section treats this as a settled cross-cutting theme: for small-$G$/single-sample settings, "the critic-free path is non-negotiable."

**Position B — SP³O ([[../research/rlvr-mechanics/ppo-critic-value-flattening]]).** PPO's critic doesn't fail because critics are structurally the wrong tool — it fails because of a specific, fixable pathology. Under terminal-only reward ($\gamma=\lambda=1$), every within-response Monte Carlo target is identical, so the standard dense per-token critic loss decomposes into a mean-fit term plus a term minimized by flat, uninformative predictions regardless of the true within-response value trajectory ("Value Flattening"), compounded by redundant gradient updates from temporally correlated adjacent states. Supervising the critic at only ~3 sparse, well-separated anchor positions per response (SP³O) fixes this without touching the actor objective, rollout procedure, or return targets — and in controlled comparisons on Qwen3-4B/8B-Base, the repaired critic-based method beats both PPO *and* GRPO (+6.31pp math avg, +2.84pp OOD avg at 4B; gap holds at 8B).

## Basis of the tension

If the critic were dispensable *because critics are the wrong mechanism* for LLM RLVR — as the family-tree framing in Position A implies by treating every post-PPO critic-removal as progress — a repaired critic-based method should not be able to beat the critic-free state of the art (GRPO) in a controlled, same-backbone, same-reward comparison. SP³O's numbers say otherwise: the actor/rollout/reward setup is identical to the GRPO and PPO baselines it's compared against, so the only variable is the value-loss supervision pattern. This suggests PPO's critic was *badly trained*, not badly motivated — a materially different diagnosis than "critics don't work for this problem class," and one the critic-free narrative doesn't currently account for.

## Resolution rule

*(Open — no ruling yet.)* SP³O's own paper does not claim to refute critic-free RL in general, and its scope is narrower than a full rebuttal of Position A: results are shown only under terminal-only reward with $\gamma=\lambda=1$ (the exact condition that makes Value Flattening formally provable), on Qwen3-4B/8B-Base, math-heavy benchmarks. What would sharpen this: (a) whether SP³O's gain over GRPO holds under dense/shaped rewards, where the implicit-variance-penalty argument's premise (identical MC targets at every position) doesn't apply as cleanly; (b) a head-to-head SP³O-vs-GRPO comparison at the group sizes and model scales where GRPO's memory/compute advantage over any critic-based method (fixed or otherwise) is most load-bearing — SP³O still trains a full value network, so even a cheap-to-supervise critic carries $V_\phi$'s memory footprint, which GRPO avoids entirely; (c) whether VinePPO or other critic-repair baselines the SP³O paper cites but doesn't compare against close some or all of the gap, which would suggest the result is about critic-training *technique* generally rather than specifically validating a return to critic-based methods.

If SP³O's advantage survives (a)–(c), Position A's framing needs a caveat: critic-free is a compute/memory-driven engineering choice at scale, not a strict performance win. If it doesn't survive, Position A stands largely as-is and SP³O becomes a narrow result specific to terminal-only-reward, moderate-scale settings.

## Source

Surfaced via the 2026-09-18 weekly sweep. SP³O / Value Flattening (arXiv:2609.18708), Section 5.2 (main comparison), Eq. 5 (variance-penalty decomposition), in `raw/research/weekly-2026-09-18/.ingest/05-ppo-critic-value-flattening.summary.md`.

## Related

- [[../research/rlvr-mechanics/ppo-critic-value-flattening]] — Position B paper
- [[../research/rl-optimizers/_overview]] — Position A, "The critic is optional" cross-cutting theme
- [[../research/rlvr-mechanics/deepseekmath-grpo]] — GRPO's original critic-removal motivation (cost/instability)
- [[../research/rlvr-mechanics/_overview]] — theme-level note on this tension, 2026-09-18 update
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
