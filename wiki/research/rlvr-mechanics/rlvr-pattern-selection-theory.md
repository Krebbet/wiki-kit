# Reshaping Reasoning in LLMs: A Theoretical Analysis of RL Training Dynamics through Pattern Selection

Chen, Li, Zou (arXiv:2506.04695, Jun 2025; v2 Sep 2025). Theoretical and empirical account of RL training dynamics in LLMs at the reasoning-pattern level, complementing token-level mechanistic analyses (cf. [[rethinking-rl-sparse-selection]]). Core finding: different reasoning patterns have relatively stable success rates throughout RL training — RL's effect is to reshape *which patterns are used*, not to modify the patterns themselves or install new ones. RL optimises a sparse subset of critical tokens to shift pattern distributions, not pattern competence. The paper formalises two reward regimes — RLVR (verifiable reward) and RLIF (model's internal feedback) — with distinct convergence behaviour. For RLVR, the base model's existing reasoning quality is the decisive factor determining whether training converges well or becomes a hard-optimisation case. For RLIF, internal rewards initially improve the model but degrade performance with continued training. Together, the theoretical framework and supporting experiments advance the "RL-as-selection-not-learning" interpretation from token-level empirics to a principled pattern-distribution account.

## Key claims

- **Pattern success rates are stable under RL training.** Reasoning patterns exhibit relatively constant success rates throughout training; RL does not make any pattern intrinsically better, it changes which patterns are produced.
- **RL acts on a sparse subset of critical tokens.** At the token level, only a sparse subset of positions is actually optimised; the mechanism by which pattern distributions shift is concentrated at these positions. (Parallel finding to [[rethinking-rl-sparse-selection]]'s 1–4% RERANKED positions.)
- **RL reshapes pattern distributions, not pattern capabilities.** The primary effect is reweighting over the existing set of reasoning patterns available in the base model — consistent with the Invisible Leash / Position A framing.
- **RLVR convergence is gated by base model reasoning quality.** Two convergence cases: easy case (base model already has sufficient reasoning competence, training converges to optimal strategy) and hard-optimisation case (base model reasoning quality is insufficient, convergence becomes intractable).
- **RLIF improves then degrades.** Training with model-internal feedback shows an improvement phase followed by degradation, suggesting an internal reward signal that becomes unreliable as it influences the model it is measuring.
- **Formal theoretical framework.** Unlike purely empirical predecessors, this paper provides a rigorous theoretical model of both RLVR and RLIF dynamics, grounding the empirical RL-as-selection observation in a derivable account.

## Relation to wiki thesis

This paper operates at the reasoning-pattern level and provides the **theoretical substrate** for the RL-as-selection cluster in [[_overview]]. Where [[rethinking-rl-sparse-selection]] (Akgul et al.) demonstrates at the token level that 0% of RL-promoted tokens exit the base top-5, Chen et al. provide the pattern-level picture: reasoning patterns themselves are unchanged in quality; RL shifts their frequency of use. The two papers are complementary levels of the same claim.

The RLVR convergence result is directly relevant to the wiki thesis's concern with low-data and single-sample regimes: if the base model's reasoning quality gates convergence, then the quality of the seed example (and whether it elicits the right pattern) is decisive — not just training compute. This tightens the link between pattern pre-existence in the base model and the viability of single-sample or low-shot RLVR.

The RLIF degradation result is a caution for self-play architectures that rely on internal reward: continued training past an initial improvement phase can reverse gains, consistent with the Invisible Leash framing's concern that RL-on-self-signal may not reliably extend beyond base-model capacity.

## Source

- `raw/research/weekly-2026-06-19/01-rlvr-pattern-selection-theory.md`
- arXiv: https://arxiv.org/abs/2506.04695 (v2, Sep 2025)

## Related

- [[rethinking-rl-sparse-selection]] — token-level empirical companion; 0%-shifted outside base top-5; REASONMAXXER; the pattern-level view here is the aggregate framing over that token-level mechanism
- [[binary-rewards-rl-challenges]] — information-geometric account of RLVR; third lens on the same cluster
- [[_overview]] — RL-as-selection-not-learning cluster; this paper adds the theoretical dimension
- [[../self-play/invisible-leash]] — Invisible Leash Theorem C.1 (support inclusion); this paper is a pattern-level theoretical confirmation of Position A
- [[../self-play/yue-rlvr-boundary]] — Yue's pass@k inversion; base-model reasoning quality as the binding constraint is consistent with the boundary analysis there
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — new theoretical evidence for Position A (pattern selection, not skill installation)
- [[../../weekly-briefs/2026-06-19]] — brought in by the 2026-06-19 weekly sweep
