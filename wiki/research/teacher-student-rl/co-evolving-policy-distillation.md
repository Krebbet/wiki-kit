# Co-Evolving Policy Distillation (CoPD)

Gu et al. (arXiv:2604.27083). Replaces the static "train experts, then distill" pipeline (Qwen3, GLM-5 MOPD orthodoxy) with **alternating phases** of branch-specific GRPO and **bidirectional mutual on-policy distillation** across $K$ parallel branches initialised from a shared base. Top-$k$ token overlap is held above 0.90 throughout training (vs. monotonic collapse under static MOPD), and the unified merged model surpasses every single-expert ceiling on Qwen3-VL-4B reasoning. Direct empirical challenge to fixed-teacher OPD: absorption efficiency depends on overlap, and overlap must be *maintained*, not assumed.

## Source
- [`raw/research/weekly-2026-05-03/03-co-evolving-policy-distillation.md`](../../../raw/research/weekly-2026-05-03/03-co-evolving-policy-distillation.md) — captured 2026-05-03 (arXiv:2604.27083)

## Method

$K$ branches, shared base $\pi_0$. Two interleaved phases:

- **Phase I — branch GRPO** ($S_{RL}$ steps): each branch $k$ optimises its own data $D_k$ via GRPO. Opens behavioural gap between branches → distillation becomes informative.
- **Phase II — mutual OPD** ($S_{OPD}$ steps): each branch generates rollouts on the *other* branch's data and absorbs token-level supervision from the other branch via on-policy KL. Closes the gap → distillation becomes absorbable.

Token-level cross-branch teacher signal:
$$\delta_{i,t}^{(k\leftarrow j)} = \log\pi_{\theta_j}(y_{i,t}^{(k)}\mid x', y_{i,<t}^{(k)}) - \log\pi_{\theta_k}(y_{i,t}^{(k)}\mid x', y_{i,<t}^{(k)})$$
Cross-branch advantage $\hat{A}^{(k)} = \beta_k\,\delta^{(k\leftarrow j)}$. Final unified model = simple parameter merge across co-evolved branches. Three-branch case uses **hub-and-spoke** topology (text branch = hub).

## Empirical headline (Qwen3-VL-4B-Instruct)

| Recipe | Overall avg | Notes |
|---|---|---|
| Mixed-data RLVR | 55.60 | suffers capability divergence cost $\Phi(D_1, D_2)$ |
| Static OPD (best) | 56.29 | absorption gated by low overlap $O_\text{low}$ |
| Single Text-Expert | 56.13 | single-expert ceiling |
| **CoPD (2-branch)** | **57.71** | surpasses all single-expert ceilings |
| MOPD (3-branch) | 56.99 | static multi-expert distillation |
| **CoPD (3-branch)** | **58.12** | surpasses MOPD and per-domain experts on aggregate |

**Pilot study:** post-OPD gain vs. top-$k$ overlap gives $r = 0.89$ (linear, $R^2 = 0.79$) — overlap is the explanatory variable.

## Where it sits in the wiki

- Sits inside [[../teacher-student-rl/_overview]] as a teacher-student variant where *teacher and student roles swap each phase*. Closest cousin: [[rlt-followups-2026]] (OPD lineage); CoPD's contribution is the **mutual + alternating** twist.
- Distinct from [[soar-edge-of-learnability]] (asymmetric bilevel meta-RL: teacher generates tasks, student RLVRs).
- Distinct from [[sakana-rlt]] (RLT's reward = student log-prob given teacher think-tokens).
- Cross-link to [[../self-play/_overview]]: CoPD's "parallel selves mutually teaching" framing is structurally adjacent to self-play; sits as a non-self-play sibling.
- Phase-alternation pattern is an *engineered* version of the [[../self-play/two-stage-dynamic]] exploration ↔ exploitation transition.
- **Direct empirical challenge** to fixed-teacher MOPD orthodoxy in [[rlt-followups-2026]]: the absorption-efficiency claim ($\eta(O_\text{mod}) \gg \eta(O_\text{low})$) means static OPD operates below ceiling.

## Mechanism — what stops drift

- Overlap $O_k(\pi_\theta, \pi_T) > 0.90$ is *maintained throughout* (Figure 4).
- Optimal $S_{RL} : S_{OPD} = 1.5:1$. Too long an RLVR phase re-introduces low-overlap regime → distillation bandwidth collapses.

## Limitations / scope

1. **Multi-capability consolidation, not single-sample concept learning** — relevance to the wiki's core thesis is indirect (mechanism, not data regime). Sample cost = sum of two independent expert budgets.
2. Three-branch video avg with CoPD (59.21) doesn't beat Video-Expert alone (58.75) on every sub-benchmark — wins MathVideoQA, loses MVBench/MMVU. MOPD underperforms video expert outright.
3. Hub-and-spoke topology for $K > 2$ is heuristic, not derived; pairwise-distillation cost at scale not analysed.
4. Single base model (Qwen3-VL-4B) — generalisability across families not shown.

## Related

- [[_overview]] — teacher-student RL theme
- [[rlt-followups-2026]] — OPD/MOPD lineage; CoPD challenges static-teacher orthodoxy
- [[soar-edge-of-learnability]] — asymmetric bilevel comparator
- [[sakana-rlt]] — different transfer reward (student log-prob)
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO backbone
- [[../self-play/_overview]] — parallel-selves framing adjacency
- [[../self-play/two-stage-dynamic]] — engineered exploration↔exploitation alternation
- [[../../weekly-briefs/2026-05-03]] — brought in by the 2026-05-03 weekly sweep
