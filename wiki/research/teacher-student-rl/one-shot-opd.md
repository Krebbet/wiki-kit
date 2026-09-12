# One-Shot On-Policy Distillation ("Rethinking OPD II")

"Rethinking On-Policy Distillation of Large Language Models II: One Training Example" (arXiv:2609.04172, Tsinghua/UCAS/Northeastern/UIUC/JHU) shows that on-policy distillation (OPD) trained on a **single query for hundreds of steps** recovers **62–89% of full-data OPD's gain** across four task domains and three model families. The explanation is a data/algorithm split: OPD's unit of supervision is the *state* (token-position prefix), not the query — one query's 64 rollouts yield tens of thousands of supervised states, so "OPD is data-overfed but algorithm-starved."

## Method

Standard OPD (student rollouts + per-token teacher KL supervision) applied at the data-minimal limit: one query, 64 rollouts/step, hundreds to 1000 steps. Two advantage estimators: sampled-token $A_i^{OPD} = \log\pi_T(y_i|s) - \log\pi_\theta(y_i|s)$, and top-$k$ ($k$=16) probability-weighted KL truncation.

The paper's causal construct is **state coverage**: represent each visited state $s=(x, y_{<i})$ by the teacher's final-layer hidden vector, cluster full-data OPD's visited states into $K$=200 clusters (PCA+K-means), and measure what fraction of those clusters a given query set's rollouts reach. Two supporting **alignment dynamics** metrics track *how fast* the teacher-student gap closes: distance left $d_t$ (mean $|$log-prob gap$|$ over visited positions) and absorption rate $v_t = (d_t - d_{t+1})/d_t$ (fraction of remaining gap closed per update).

## Key results

| Domain | One-shot gap recovery | Notes |
|---|---|---|
| Math reasoning | 72% (step 1000) | Headline result; 87% at step 300 |
| Code generation | 73% | |
| Instruction following | 66% | |
| Agentic tool use | 64% | |

- A single query reaches **71.5% state coverage** (vs. full-data's 100%), most of it (65.9%) within the first 100 steps.
- **16 semantically diverse queries reach 98.9% coverage** and match full-data training — holds for both single-domain OPD and multi-teacher OPD (MOPD: 16 queries/domain recovers 101% of full-data MOPD's gain).
- Robust to query difficulty: **works even on a query the student never solves** (0/8 pass rate before training).
- Content need not even state a task — content-light templates (empty `<think>` scaffold) and off-domain WildChat conversational queries drive OPD to within ~1 point of the real-query baseline. The input's role reduces to "starting the student reasoning," not stating a solvable problem.
- Absorption rate falls at nearly the same rate (4–6× between step 50–200) regardless of query count (1/4/16/full) — a property of the optimizer, not the data.

## One-shot OPD vs. one-shot RLVR (direct comparison, Section 7.2)

The paper runs a controlled head-to-head on the **same query**: RLVR (GRPO, 8 rollouts/query, outcome reward) saturates once the query is solved on nearly every rollout — zero-advantage groups kill the learning signal. OPD's per-token teacher-student gap persists and keeps training productive: **OPD's validation gain over 1000 steps is more than 2× RLVR's** on the same query. Structural claim: RLVR's usable-input class is constrained to verifiable, outcome-variable tasks; OPD's is not, since supervision comes from local state-level divergence rather than trajectory-level reward — it tolerates non-tasks as training inputs.

## Relation to the wiki's single-sample thesis

This is the first corpus paper to bring the one-shot-RLVR experimental lens ([[../single-sample-rl-finetuning/1-shot-rlvr]]) to a *distillation* objective. It reframes what "single-sample learning" means for dense-supervision methods: one example is a large multi-state training set in disguise, and the causal driver of generalization is state coverage, not query count.

## Limitations (authors' own)

- State coverage is a semantic-level proxy measured against a reference space built from full-data rollouts, not an absolute measure.
- What sets the absorption rate itself is left unexplained — documented as an optimizer property, not mechanistically derived.
- MOPD experiments cover only 3 domains/1 teacher each.
- One-shot's visited states have a heavier tail of off-reference states (17.2% exceedance vs. 3.8–4.4% for 4/16-shot) yet are statistically inseparable from full-data states (AUROC 0.552) — a fairly weak robustness check for the causal coverage story.

## Conflict flags

This paper's mechanism assumes genuine progressive teacher-student distributional alignment (rising top-16 overlap, closing entropy gap) drives the gain from coverage. [[opsa-teacher-free-self-adaptation]] argues sampled-token OPD's gains require no real teacher signal at all. Not a head-to-head test — see [[../../conflicts/opsa-vs-opd-pattern-transfer]], extended 2026-09-11 with this paper as one of three pieces of new evidence.

## Source

- arXiv: [2609.04172](https://arxiv.org/abs/2609.04172) — "Rethinking On-Policy Distillation of Large Language Models II: One Training Example"
- Sequel to arXiv:2604.13016 ("Rethinking OPD I")
- Captured via 2026-09-11 weekly sweep: `raw/research/weekly-2026-09-11/01-rethinking-opd-ii-single-example.md`

## Related

- [[../single-sample-rl-finetuning/1-shot-rlvr]] — direct precedent this paper's methodology is modeled on; Section 7.2 gives a controlled comparison
- [[_overview]] — teacher-student-rl theme overview, OPD saga
- [[opsa-teacher-free-self-adaptation]] — conflicting mechanism account, see conflict below
- [[opd-dual-nature-generalization]] — parallel corroboration: teacher-unsolved problems are equally useful (pattern/state-transfer over answer-transfer)
- [[esr-early-stopping-opd]] — parallel state-level lens on which prefixes/states carry useful teacher signal
- [[sequential-opd-then-rl]] — 2026-09-11 sibling capture, same conflict extension
- [[tgopd-verify-before-distill]] — 2026-09-11 sibling capture, same conflict extension
- [[../../conflicts/opsa-vs-opd-pattern-transfer]] — extended with this paper's evidence
- [[../../weekly-briefs/2026-09-11]] — brought in by the 2026-09-11 weekly sweep
