# Influence-Directed Distillation: Solving the Diversity Bottleneck in Sampled-Token On-Policy Distillation

Yang, Dai, Sun, Zhang, Zhou, Zhu, Li, and Gao (BiliBili, UNC Chapel Hill, USTC, Shanghai University of Finance and Economics; arXiv:2608.29846) study *sampled-token on-policy distillation* (OPD) — the cheap variant of on-policy distillation that queries the teacher's log-probability only for the student's own sampled tokens, rather than a full-vocabulary or top-$K$ teacher distribution. They diagnose a specific failure mode, *diversity distillation failure* (pass@1 rises while pass@$k$ stalls), by decomposing each gradient update's effect on entropy into a signed first-order quantity, then use that diagnostic to build a teacher-free fix — **Influence-Directed Adaptive OPD (IDA-OPD)** — that recovers the diversity teacher-informed methods normally buy with much more expensive full-vocabulary or top-$K$ teacher queries.

## Method

Sampled-token OPD trains the student via a reverse-KL-flavored imitation loss using the K1 estimator: sample $y \sim p_\theta(\cdot\mid h)$ from the student itself, form the advantage

$$A_y = \log p_T(y\mid h) - \log p_\theta(y\mid h)$$

(teacher log-prob minus student log-prob at the sampled token), and take

$$\ell^{OPD}_y = -\text{sg}(A_y)\log p_\theta(y\mid h)$$

with $\text{sg}(\cdot)$ a stop-gradient. This needs only one teacher log-prob per position — no full-vocabulary or top-$K$ teacher distribution — which is what makes sampled-token OPD cheap relative to EOPD/AOPD-style variants.

The paper's diagnostic contribution is **Theorem 1 (First-Order Local Entropy Influence)**: for a small update step $\eta$, the resulting change in the student's per-token entropy is

$$\Delta H = \eta \cdot I_H(y) + O(\eta^2), \qquad I_H(y) = A_y \, D_y$$

where $D_y$ depends only on the student's own current distribution at that position (its "local probability structure," Eq. 1). This decouples an update's entropy effect into (a) the teacher–student log-prob gap $A_y$ and (b) student-side local geometry $D_y$ — and $I_H(y)$'s *sign* tells you whether a given update expands or contracts entropy, which $A_y$ alone does not (Figure 1: $A_y$ correlates only weakly and two-sidedly with measured entropy change, while $I_H(y)$ tracks it tightly). Empirically (Figure 2), cumulative entropy loss is not driven by high-divergence updates — it peaks at near-zero teacher–student divergence ($\delta_y \approx 0$), simply because that region has the largest token-count volume. Vanilla OPD's uniform treatment of the advantage lets this high-volume, low-divergence region silently drain entropy.

**IDA-OPD** intervenes only where the sign of $I_H(y)$ says entropy is contracting, leaving entropy-expanding updates untouched:

$$\tilde A_y = \begin{cases} w_y \, A_y & \text{if } I_H(y) < 0 \\ A_y & \text{otherwise} \end{cases}, \qquad \ell^{IDA\text{-}OPD}_y = -\text{sg}(\tilde A_y)\log p_\theta(y\mid h)$$

with divergence-adaptive shrinkage weight

$$w_y = \frac{|q_y - p_y|}{q_y + p_y} \in [0,1)$$

(where $p_y, q_y$ are student/teacher probabilities at the sampled token). Proposition 1 shows this weighting gives quadratic attenuation near teacher–student agreement (exactly where the volume-driven entropy drain was concentrated) and near-lossless pass-through at high disagreement (where the signal is informative and should not be suppressed). Critically, $w_y$ is computed from quantities OPD already has — the sampled-token teacher log-prob — so the fix adds a sign-gate and a reweighting, not new teacher information.

## Claims

- **Diversity recovery on math (Qwen3-4B/8B, teacher = GRPO-trained Qwen3-Non-Thinking-RL-Math, DeepMath103K difficulty-6 subset):** IDA-OPD raises pass@16 over vanilla OPD by **+4.2 to +7.2 pp on the 8B student** and **+4.3 to +8.3 pp on the 4B student**, across AIME24, AIME25, HMMT Feb, and HMMT Nov, while broadly preserving pass@1 (pass@1 changes are small and occasionally slightly negative, e.g. −0.2 on HMMT Feb/4B).
- **Matches or beats teacher-informed methods at lower cost:** IDA-OPD matches or exceeds EOPD and AOPD — both of which require top-$K$ or full-vocabulary teacher distributions — while querying only the sampled-token teacher log-prob, i.e. $O(L)$ information cost versus their $O(L_{sel}\cdot K)$.
- **Student exceeds teacher on pass@16:** on several benchmarks the distilled student's pass@16 *surpasses the teacher's own pass@16* — **83.3% vs. teacher's 80.0% on 4B/AIME24**, and **76.7% vs. teacher's 73.3% on 8B/AIME25** (raw source, lines ~464–518, corroborates these exact figures). This is an externally-taught student beating its teacher via ordinary cross-model OPD, not a self-distillation setup.
- **Code distillation (Qwen3-4B, MBPP+/LiveCodeBench):** IDA-OPD improves both pass@1 and pass@16, where vanilla OPD leaves pass@16 essentially flat — the diversity-bottleneck pattern and its fix generalize beyond math.
- **Ablations validate both pieces are necessary (Table 3):** removing the $I_H(y)$ sign-gate over-attenuates entropy-expanding updates and hurts pass@1; hard-masking (dropping all entropy-contracting updates outright, rather than shrinking them) protects diversity but does the most damage to pass@1. The gate and the graded shrinkage are both required — neither alone suffices.
- **Shrinkage functional form matters (Table 4):** the linear weight $w_y$ outperforms constant, sqrt, and square alternatives; this is not a parameter-free universal law, though it still needs no extra teacher signal beyond the sampled-token log-prob already used by OPD.
- **Mechanistic evidence:** the token-level entropy histogram (Figure 4b) shows IDA-OPD keeps the student's per-token uncertainty distribution close to the teacher's at both extremes, versus vanilla OPD's pile-up in the near-deterministic 0.0–0.1 entropy bin (~74% of tokens vs. teacher's ~57%).

## Sample efficiency

This is not a single-sample or few-shot paper. It operates in a standard large-scale RL-distillation regime (DeepMath103K difficulty-6 subset for math; $n=128$ rollouts per problem for pass@$k$ estimation at eval time). There is no claim about learning from one or few examples. Its relevance to this wiki is as an **RL/distillation mechanism** paper — specifically a fix to a known pathology of the token-efficient (sampled-token, single-teacher-query-per-position) OPD estimator, which is itself one of the cheapest-per-example on-policy training signals in the teacher-student RL literature. The "no full-vocabulary teacher information needed" property is the closest analog to sample/information efficiency here: it is about efficiency of *supervision signal per token*, not about efficiency of *training examples*.

## Relevance to the project

The wiki's teacher-student-rl/OPD cluster tracks the sampled-token OPD estimator (K1: advantage from a single sampled-token teacher log-prob) as a recurring locus of subtle failure modes and repairs — this paper is a clean addition to that lineage. It sits alongside [[opdvr-verifiable-reward]] and [[gc-opd-group-calibrated]] as a third way of repairing the *advantage signal* used by sampled/dense OPD token credit, without introducing new external teacher information: OPDVR fixes a mis-signed reward via a ReLU gate, GC-OPD substitutes a verifier-calibrated residual, and IDA-OPD gates/shrinks the advantage by the sign and magnitude of a first-order entropy-influence term. All three leave the estimator's basic information budget untouched while changing what gets done with it.

It also offers a second, structurally parallel example (alongside [[../rlvr-mechanics/high-entropy-minority-tokens]]) of "entropy-selective token gating" as a general pattern for RL/distillation gradient interventions — that page gates on high-entropy "fork" tokens to concentrate RL gradient signal; this paper gates on the *sign* of a first-order entropy-influence quantity to decide which token updates to shrink in a distillation KL objective. Different objective, same underlying move of using per-token entropy structure as the intervention trigger.

The pass@16 student-exceeds-teacher numbers (83.3 vs. 80.0 on 4B/AIME24; 76.7 vs. 73.3 on 8B/AIME25) are a soft, tangential data point for the wiki's [[../../conflicts/adrs-vs-opsd-compaction]] thread: they show a student surpassing its teacher via ordinary cross-model OPD with an externally RL-trained teacher, not via the privileged self-distillation setups (OPSD/ADRS) that thread is centrally about — worth noting as a parallel phenomenon under a different mechanism, not a new formal data point in that specific conflict.

## Limitations

- The authors' own ablations (Table 3) show the sign-gate and the graded shrinkage are both necessary; dropping either degrades results in different directions (pass@1 loss without the gate, larger pass@1 loss with hard-masking instead of shrinkage).
- The shrinkage functional form is not parameter-free: Table 4 shows linear $w_y$ beats constant/sqrt/square weighting, implying some sensitivity to functional-form choice even though no extra teacher signal is required.
- Theorem 1 is explicitly a first-order, idealized-logit-space, single-gradient-step approximation; the authors validate its relevance to real AdamW training only via macro-level entropy-trajectory correlation (Figure 4a), not a formal guarantee under multi-step, momentum-based optimization.
- Unstated: all experiments distill from an RL-trained teacher within the *same* model family and tokenizer as the student (Qwen3 self-family). No cross-tokenizer or cross-architecture transfer is tested, unlike some cited OPD variants (e.g., SimCT).
- The headline win is squarely pass@$k$/diversity recovery; pass@1 gains are inconsistent and sometimes slightly negative (e.g., −0.2 on HMMT Feb/4B) — this is a diversity-preservation fix, not a general accuracy improvement.

## Source

- `raw/research/weekly-2026-09-04/02-influence-directed-distillation-opd.md`
- arXiv: https://arxiv.org/abs/2608.29846

## Related

- [[opsa-teacher-free-self-adaptation]] — this week's sibling OPD paper: both propose fixes to the sampled-token/K1 OPD estimator's implicit advantage signal via different diagnoses (entropy-influence-gated shrinkage here vs. removing the teacher entirely there); worth cross-linking as sibling sampled-token-OPD-repair methods
- [[opd-dual-nature-generalization]] — parallel diagnostic lens on what sampled-token OPD actually transfers (patterns/diversity here; pattern-transfer/generalization scope there)
- [[opdvr-verifiable-reward]] — both modify the advantage used in sampled/dense OPD token credit
- [[gc-opd-group-calibrated]] — both modify OPD's advantage signal without adding external teacher information beyond what's already queried
- [[rlt-followups-2026]] — landscape-tracking page for the OPD lineage, new 2026 entry
- [[../../conflicts/adrs-vs-opsd-compaction]] — soft/tangential addition: student pass@16 matches-or-surpasses teacher on several benchmarks via ordinary cross-model OPD, not privileged self-distillation like OPSD/ADRS — a softer data point in this conflict thread, not a new formal one
- [[../../weekly-briefs/2026-09-04]] — brought in by the 2026-09-04 weekly sweep
