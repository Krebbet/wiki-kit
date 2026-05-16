# MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate

arXiv:2605.01347, May 2026 (Alibaba/HUST). Replaces the single OPD teacher with a $K=2$, $R=2$ inter-teacher **debate ensemble**: each teacher force-decodes the student's on-policy state conditioned on the full debate transcript $H_m^R$ (privileged context), with token-level supervision aggregated by softmax-normalised post-debate confidence weights $w_k$. Adds a step-level extension **OPAD** for agentic trajectories (debate at each environment step before force-decoding the student's action) and a theoretically-derived **task-adaptive divergence** (JSD for agentic tasks, reverse KL for code generation). 4B student trained under 14B+8B debate **exceeds the 14B teacher alone** on LCB-v6 by +4.26% pass@1 / +10.29% BoN@16 — the single-teacher ceiling is broken across all six evaluated configs.

## Source

- `raw/research/weekly-2026-05-10/05-mad-opd-multi-agent-debate.md`

## Method

**OPD as dense token-level RL (Eq. 1).** Per-token reward $r_D(s_t) \triangleq -D(p^* \| p_S)$ where $D$ is a divergence and $p^*$ a teacher distribution.

**MAD-OPD loss (Eq. 8).** With $K$ teachers running $R$ rounds of debate over student state $s_m$:

$$\mathcal{L}_\text{MAD-OPD}(\theta) = \mathbb{E}\left[\sum_t \sum_k w_k \cdot D(p_{T_k}(\cdot | s_m, H_m^R, \hat{y}_{<t}) \| p_S(\cdot | s_m, \hat{y}_{<t}))\right]$$

$w_k$ comes from softmax over each teacher's post-debate confidence (Eq. 7). The full debate transcript $H_m^R$ is *privileged* — visible to teachers, not student.

**OPAD (Eqs. 9–10).** At each agentic step $m$ in a trajectory, teachers debate over $s_m = (x, \tau_{<m})$ before force-decoding the student's action $a_m$. Per-step losses summed over the on-policy rollout. Stabilises long-horizon agentic training where error compounding kills naive off-policy debate distillation.

**Task-adaptive divergence (Remark 1, Lemmas 1–2, Propositions 1–2).**
- **Agentic tasks → JSD.** Lemma 1: $\| \nabla_z \text{JSD}_{0.5} \|_\infty \leq 2$ — bounded gradient under privileged $p$–$q$ gap; Proposition 1 confirms per-token gradient stability.
- **Code generation → reverse KL.** Lemma 2 + Proposition 2: reverse KL produces mode concentration on a single coherent code path. Forward-KL or JSD over diverse-but-incompatible code paths produces incoherent supervision (the **MT-OPD failure mode**, Table 1 — naive multi-teacher averaging falls *below* single-teacher OPD on code in 4 of 6 configs).

## Empirical results

| Config | Headline |
|---|---|
| 14B+8B → 4B | +2.4% Ag-Avg / +3.7% Co-Avg over best single-teacher OPD |
| 14B+8B → 4B (LCB-v6) | 4B student exceeds 14B teacher: +4.26% pass@1, +10.29% BoN@16 |
| MAD-OPD ranks first | Overall Avg across all six configurations (1.7B–14B students × 8B–32B teachers) |
| MT-OPD (no debate) | Underperforms single-teacher OPD on code in 4/6 configs |
| R=3 rounds | Degrades vs R=2 due to context bloat |

Training data: ToolACE (~16K agentic step-split) + OpenThoughts3 (30K code). Compute overhead $K \times R = 4$ teacher passes per training step. Vocabulary-aligned teachers required (logit-access white-box only).

## Why it matters

- **Single-teacher ceiling broken.** This is the cleanest empirical result yet that the OPD bottleneck is *teacher-pool diversity*, not teacher capacity. A 4B student under debate-2-of-2 exceeds the 14B teacher alone.
- **Task-adaptive divergence.** First principled derivation of JSD-vs-reverse-KL choice from privileged-context gradient analysis, not empirical sweep. Suggests the divergence-choice question in [[co-evolving-policy-distillation|CoPD]]'s alternating GRPO+mutual-KL setup may have a similar task-conditioned answer.
- **OPAD** as a clean step-level distillation primitive for long-horizon agentic training — orthogonal to GRPO-style RL.

## Connections to the wiki

- **[[_overview]]** — adds debate-as-supervision to the teacher-student RL toolkit.
- **[[rlt-followups-2026]]** — slots into the post-RLT OPD landscape; OPAD and task-adaptive divergence are the differentiators.
- **[[co-evolving-policy-distillation]]** — CoPD raises teacher quality via co-evolution; MAD-OPD raises *effective* teacher quality via debate ensemble. Complementary mechanisms; both alternatives to the static fixed-teacher MOPD orthodoxy.
- **[[sakana-rlt]]** — RLT's privileged-information teaching (teacher sees answer); MAD-OPD's privileged-information is the debate transcript. Same primitive applied differently.
- **[[../self-play/debate]]** — Irving et al. debate for safety; Du et al. (arXiv:2305.14325) MAD are the direct ancestors. MAD-OPD repurposes debate from inference-time eval to training-time supervision.
- **[[../self-improvement/multi-turn-policy-verifier]]** (PAG) — multi-role; OPAD's step-level debate is structurally adjacent.
- **[[../synthesis/proposed-method]]** — debate ensemble is a possible realisation of the "external critic / second model" component for single-sample concept learning.
- **[[../../conflicts/unified-vs-two-model-self-play]]** — debate is explicitly multi-model. The framing **"bottleneck is teacher-pool diversity, not single-teacher capability"** bears directly on the unified vs two-model conflict and supports the two-model side at the OPD-supervision level.

## Conflicts

- **Novelty claim** ("first to bring debate live into OPD training as token-level supervision"). Authors distinguish from SMAGDi (arXiv:2511.05528) and MAGDi (ACL 2024) on grounds those use *pre-computed* debate traces. Worth checking.
- **MT-OPD < single-teacher OPD on code.** Counter-intuitive; per-token averaging across incompatible code paths produces incoherent supervision. Useful failure mode for the wiki: ensemble distillation **with** divergence design > ensemble distillation **without**.

## Limitations

- White-box teachers only (logit access).
- Shared teacher–student vocabulary required.
- Capability gap ceiling: 1.7B student vs 14B+8B teachers (~13× ratio) hits a floor — student cannot generate on-policy trajectories inside teachers' competence regime.
- Math benchmarks excluded — generalisation to reasoning-heavy domains unvalidated.

## Related

- [[_overview]]
- [[rlt-followups-2026]]
- [[co-evolving-policy-distillation]]
- [[opsd-compresses-rlvr]] — companion week-of OPD paper (compaction angle)
- [[sakana-rlt]]
- [[../self-play/debate]]
- [[../self-play/_overview]]
- [[../self-improvement/multi-turn-policy-verifier]]
- [[../critique-self-correction/_overview]]
- [[../synthesis/proposed-method]]
- [[../../conflicts/unified-vs-two-model-self-play]] — debate ensemble framing supports two-model side
- [[../../weekly-briefs/2026-05-10]] — brought in by the 2026-05-10 weekly sweep
