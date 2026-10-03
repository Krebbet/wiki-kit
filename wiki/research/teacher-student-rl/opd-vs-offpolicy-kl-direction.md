# On-Policy or Off-Policy? A Systematic Study of Distillation Dynamics

arXiv:2609.35259 (Piskorz, Berthon, van der Schaar; submitted 2026-09-28). Controlled strong-to-weak distillation study that independently varies rollout policy (student to teacher spectrum), token-level KL direction, and learning rate on Llama3 and Qwen2.5 (science, medical, arithmetic). Finding: rollout policy is *not* the central factor. KL direction shapes performance and output coverage; learning rate governs forgetting and update sparsity. Forward KL is robust to rollout policy; reverse KL is sensitive and prefers student rollouts. This challenges the "on-policy is inherently better" premise behind much of the OPD and forgetting literature in this wiki.

## Source

- `raw/research/weekly-2026-10-02/02-opd-vs-offpolicy-kl-direction.md` (arXiv abs-page capture; abstract only)

## Claims

| Axis | Effect (per abstract) |
|---|---|
| Rollout policy (on vs off) | Not central to final task performance |
| KL direction | Shapes performance and coverage; forward KL stable across rollout policies, reverse KL needs student-generated rollouts |
| Learning rate | Governs forgetting and update sparsity |
| On-policy data | Still improves generalisation to harder Countdown variants under both KLs, but the advantage does not reliably survive subsequent RLVR |
| Robustness | Holds without gradient clipping, with sampled KL estimators, with longer reasoning chains |

Implications:
- Sparse updates and low forgetting attributed to on-policy learning ([[../catastrophic-forgetting/rls-razor]], [[../catastrophic-forgetting/rft-mitigates-forgetting]]) are, here, confounded with learning rate. See [[../../conflicts/on-policy-forgetting-vs-lr-confound]].
- Reverse-KL's rollout sensitivity matches why sampled-token OPD (a reverse-KL estimator) needs on-policy states ([[one-shot-opd]], [[opsa-teacher-free-self-adaptation]]); forward-KL distillation is the off-policy-tolerant regime. [[mad-opd]] chooses reverse KL for code for coherence reasons: a different axis.
- On-policy advantage not persisting through RLVR echoes [[sequential-opd-then-rl]] and [[opsd-compresses-rlvr]] (OPD/distillation gains largely compacted by later RL).

Caveat: abstract only; the scales (7B?) and LR grids were not captured, and the setting is strong-to-weak distillation rather than RL with a verifier, so transfer to RLVR forgetting results is an inference.

## Related

- [[_overview]] — teacher-student-rl cluster
- [[one-shot-opd]] — on-policy state coverage mechanism
- [[opsa-teacher-free-self-adaptation]] — sampled-token OPD mechanism
- [[sequential-opd-then-rl]] — distillation gains vs later RL
- [[mad-opd]] — task-adaptive divergence choice
- [[../catastrophic-forgetting/_overview]] — forgetting theme (on-policy constraint account)
- [[../catastrophic-forgetting/rls-razor]] — on-policy KL-minimality claim under challenge
- [[../catastrophic-forgetting/rft-mitigates-forgetting]] — RFT retention claim
- [[../catastrophic-forgetting/rft-data-perspective]] — on-policy data account
- [[../../conflicts/on-policy-forgetting-vs-lr-confound]] — opened by this page
- [[../../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
