# On-policy forgetting advantage vs learning-rate confound

Does on-policy rollout data itself reduce forgetting and update magnitude (RL's Razor, RFT papers), or is that effect an artifact of the learning rates that RL-style and SFT-style runs are typically trained at?

## Positions

**Position A — on-policy is protective.** [[../research/catastrophic-forgetting/rls-razor]]: at matched new-task accuracy, on-policy RL forgets less than SFT because it is biased to KL-minimal solutions. [[../research/catastrophic-forgetting/rft-mitigates-forgetting]] and [[../research/catastrophic-forgetting/rft-data-perspective]]: self-generated rollouts are low-perplexity-gap, low-eNTK-magnitude data that preserve prior knowledge.

**Position B — rollout policy is not the driver ([[../research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]).** In a controlled strong-to-weak distillation study varying rollout policy, KL direction and learning rate independently, rollout policy "does not necessarily play a central role"; learning rate governs forgetting and update sparsity, and KL direction governs performance and coverage. On-policy data helps generalise to harder Countdown variants but not reliably after later RLVR.

## Tension

Position A attributes low forgetting/sparse updates to on-policy data; Position B finds those track learning rate with rollout policy held to a spectrum. If B generalises, existing RL-vs-SFT forgetting gaps may partly reflect different LRs rather than data provenance.

Non-identical settings, so not a clean contradiction: B is distillation with a dense teacher KL objective (forward/reverse), not outcome-reward RL; A's comparisons are RL vs SFT on verifiable tasks. Reverse-KL, the OPD-style objective, is where B also finds on-policy rollouts matter, so partial agreement is plausible.

## Resolution rule

*(Open — no ruling yet.)* Resolve by an LR-matched RL-vs-SFT forgetting comparison (sweep LR for both, compare at matched new-task accuracy), or by checking whether B's LR-dependence of forgetting holds with an outcome-reward objective.

## Source

Surfaced via the 2026-10-02 weekly sweep: arXiv:2609.35259 abstract, `raw/research/weekly-2026-10-02/02-opd-vs-offpolicy-kl-direction.md` (abstract only), checked against the wiki's catastrophic-forgetting theme.

## Related

- [[../research/teacher-student-rl/opd-vs-offpolicy-kl-direction]] — Position B paper
- [[../research/catastrophic-forgetting/rls-razor]] — Position A
- [[../research/catastrophic-forgetting/rft-mitigates-forgetting]] — Position A
- [[../research/catastrophic-forgetting/rft-data-perspective]] — Position A
- [[../research/catastrophic-forgetting/_overview]]
- [[../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
