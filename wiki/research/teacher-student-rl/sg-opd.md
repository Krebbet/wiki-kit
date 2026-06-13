---
priority: P3
arxiv: "2606.09304"
submitted: "2026-06-08"
---

# SG-OPD: Sign-Gated On-Policy Distillation

Standard OPD breaks in practice via two failure modes: (1) *trajectory-level misalignment* — student on-policy rollouts drift to a distribution where teacher per-token preferences are unreliable; and (2) *non-uniform token reliability* — some teacher signals point against the verifier-correct direction. SG-OPD fixes both with complementary mechanisms: *phased teacher sampling* injects verifier-endorsed teacher rollouts into the student batch at cold-start to anchor early distribution; and a *sign-consistency gate* extrapolates teacher supervision on tokens where teacher and verifier agree, and interpolates (dampens) it where they disagree. On competition math, SG-OPD gains +1.98 per-sample and +7.50 per-question over standard OPD.

## Method

**Phased teacher sampling.** During cold-start, verifier-endorsed teacher rollouts are mixed into the student's on-policy batch at a decaying schedule. This anchors the student's distribution near the teacher's before on-policy rollouts dominate, addressing trajectory-level misalignment without abandoning the on-policy regime.

**Sign-consistency gate.** For each token $t$ in a student rollout, the sign of the teacher's KL-divergence update direction is compared against the verifier-correct direction. Define the gate:

$$g(t) = \begin{cases} \lambda_\text{extrap} & \text{if } \operatorname{sign}(\nabla_t^\text{teacher}) = \operatorname{sign}(\nabla_t^\text{verifier}) \\ \lambda_\text{interp} & \text{otherwise} \end{cases}$$

where $\lambda_\text{extrap} > 1 \geq \lambda_\text{interp} > 0$. The modified per-token loss is:

$$\mathcal{L}_\text{SG-OPD}(t) = g(t) \cdot \mathcal{L}_\text{OPD}(t)$$

The gate is binary and non-zeroing: disagreeing tokens receive a dampened update, not a dropped one. The verifier supplies a binary outcome signal (correct/incorrect trajectory); its sign is propagated to the token level to weight which teacher updates are trusted. This is a refinement within the OPD/policy-gradient family — the per-token distillation loss acts as a dense per-token reward $r_D(s_t) = -D(p^* \| p_S)$, and the sign-consistency coefficient functions as a learned advantage weight derived from verifier agreement.

## Results

On competition-level mathematical reasoning benchmarks, SG-OPD consistently outperforms standard OPD:

- **+1.98** per-sample average gain
- **+7.50** per-question average gain

Full benchmark-by-benchmark breakdown and model-size ablations are not available from the captured abstract alone (PDF did not render).

## Hint design relevance

SG-OPD weakly corroborates KnowRL's "selective trust" position without endorsing the minimal-sufficient extreme. The sign-consistency gate structurally resembles KnowRL's principle of pruning unreliable signal: teacher tokens that contradict the verifier-correct direction are discounted. But SG-OPD retains interpolated (dampened, not zeroed) updates on disagreeing tokens rather than dropping them — it does not endorse the minimal-sufficient extreme that KnowRL advocates. Tentative reading: corroborates selective trust over uniform teacher deference, without resolving the KnowRL vs. RLT atomic-vs-maximal tension. See [[conflicts/knowrl-vs-rlt-hint-design]].

## Limitations

- Evaluated only on competition mathematics; generalization to other reasoning domains unknown.
- The binary gate is a simplification — a graduated trust score might recover more signal from disagreeing tokens.
- The phased cold-start mix-in schedule introduces a hyperparameter whose sensitivity is not reported.
- Full method details (exact loss formulation, training hyperparameters, per-benchmark table) unavailable from capture — PDF rendered as non-content icons.

## Source

- `raw/research/weekly-2026-06-12/07-sg-opd.md` — captured PDF (arXiv:2606.09304)

## Related

- [[teacher-student-rl/_overview]] — parent theme
- [[teacher-student-rl/opsd-compresses-rlvr]] — base framework SG-OPD extends
- [[teacher-student-rl/sgsd-skill-gated-distillation]] — parallel OPD variant (skill-based gating)
- [[teacher-student-rl/mad-opd]] — parallel OPD variant (debate stabiliser)
- [[teacher-student-rl/esr-early-stopping-opd]] — parallel stability fix
- [[teacher-student-rl/knowrl]] — adjacent: SG-OPD's sign-gate mediates the minimal/maximal hint debate
- [[conflicts/knowrl-vs-rlt-hint-design]] — open conflict this paper partially addresses
- [[weekly-briefs/2026-06-12]] — brought in by the 2026-06-12 weekly sweep
