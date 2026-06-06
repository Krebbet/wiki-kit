# SDPG: Self-Distilled Policy Gradient

**arXiv:2606.04036** | Liu, Zhang, Zhang, Gu (UCLA / Quanquan Gu lab) | Submitted 2 Jun 2026

SDPG combines on-policy self-distillation with group-relative RLVR into a single loss. The core observation: a model conditioned on privileged context (i.e., the solution) can supervise its own unconditional generations via a student-to-teacher reverse-KL divergence computed over the full vocabulary — making this an auxiliary dense-supervision signal for RLVR's typically sparse 0/1 reward. The framework composes three components: (1) group-relative verifier advantages with normalised standard deviation (the GRPO backbone), (2) exact full-vocabulary on-policy self-distillation, and (3) reference-policy KL regularisation. Empirically, SDPG improves both stability and performance over standalone RLVR and self-distillation baselines.

## Method

SDPG augments a standard GRPO objective with an auxiliary reverse-KL self-distillation term. At a high level, the training signal is:

$$\mathcal{L}_{\text{SDPG}} = \mathcal{L}_{\text{GRPO}} + \alpha \cdot \mathcal{L}_{\text{SD}}$$

where $\mathcal{L}_{\text{GRPO}}$ is the standard group-relative policy gradient loss with normalised std advantages, and $\mathcal{L}_{\text{SD}}$ is the full-vocabulary student-to-teacher reverse KL:

$$\mathcal{L}_{\text{SD}} = D_{\text{KL}}\!\left(\pi_\theta(\cdot \mid q) \;\Big\|\; \pi_\theta(\cdot \mid q, s^*)\right)$$

where $\pi_\theta(\cdot \mid q)$ is the student (unconditional) policy and $\pi_\theta(\cdot \mid q, s^*)$ is the same model conditioned on the privileged solution $s^*$ — the teacher role. This is *self*-distillation: no separate teacher model, just the same weights under two context conditions.

Key design choices relative to related work:

- **Full-vocabulary** reverse-KL (not top-$k$ or token-filtered), making it exact on-policy.
- **Normalised std** in the group-relative advantage — contrast with [[dr-grpo]], which argues for *removing* std normalisation. SDPG retains it with explicit normalisation; this is a potential conflict (see below).
- **Reference-policy KL** in the loss as a regulariser, keeping the policy from drifting too far — unlike [[dapo]], which drops the reference KL entirely.
- The privileged context used by the teacher is the verified solution $s^*$, which parallels [[../teacher-student-rl/rlt-followups-2026|OPSD]] (Zhao et al., arXiv:2601.18734) and the broader self-distillation-with-privileged-info wave.

Structurally, SDPG is the most explicit formulation of the "same-model, two-context" self-distillation idea as a drop-in RLVR auxiliary loss. Where OPSD trains by minimising reverse-KL *instead of* GRPO, SDPG runs both in parallel. The full-vocabulary reverse-KL is described as a specific instantiation of the abstract "on-policy self-distillation" principle.

## Results

*Note: the raw capture is abstract-only (PDF rendered as images); quantitative table entries are not available from the captured source. The claims below are drawn from the abstract.*

- SDPG **improves stability** over RLVR baselines (GRPO-family) and self-distillation baselines.
- SDPG **improves performance** over both baseline classes.
- No specific benchmark numbers (AIME, MATH, GSM8K pass@1 etc.) are recoverable from the abstract alone.

Code released at: https://github.com/lauyikfung/SDPG

## Source

- `raw/research/weekly-2026-06-05/01-sdpg-self-distilled-policy-gradient.md`

## Related

- [[_overview]] — RL optimizer lineage; SDPG is a post-GRPO RLVR variant with self-distillation auxiliary
- [[dapo]] — drops reference KL entirely; SDPG retains it
- [[dr-grpo]] — removes std normalisation from GRPO; SDPG retains normalised std — potential methodological conflict
- [[gspo]] — sequence-level IS variant; SDPG uses standard token-level GRPO with auxiliary loss
- [[../rlvr-mechanics/deepseekmath-grpo]] — base optimiser SDPG extends
- [[../rlvr-mechanics/_overview]] — RLVR mechanics context
- [[../teacher-student-rl/rlt-followups-2026]] — OPSD (arXiv:2601.18734) is the closest sibling: same "same-model, two-context" self-distillation idea, but as a replacement for rather than auxiliary to GRPO; also covers the broader self-distillation-with-privileged-info wave (SDFT, SDPO, G-OPD)
- [[../teacher-student-rl/sakana-rlt]] — Sakana RLT uses a *separate* teacher model conditioned on (Q, A); SDPG collapses this to a single model
- [[../teacher-student-rl/_overview]] — OPD/self-distillation theme overview
- [[../weekly-briefs/2026-06-05]] — brought in by the 2026-06-05 weekly sweep
