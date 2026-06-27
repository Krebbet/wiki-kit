# First-Principles Derivation of LLM Policy Optimization: Two-Axis Framework

A 60-page theory survey (arXiv:2606.16733) that derives every major LLM policy-gradient algorithm — REINFORCE → PPO → GRPO → post-GRPO variants → Agentic RL → GRPO-OPD hybrid — from the shared objective $J(\theta) = \mathbb{E}_{\tau \sim p_\theta(\tau)}[R(\tau)]$ using trajectory probability ($p_\theta(\tau)$) and reward ($R(\tau)$) as the two diagnostic axes. No new algorithm proposed; the contribution is an organizational framework that locates every post-GRPO paper as a **failure-motivated response** along one or both axes.

## Derivation spine (Part I)

Starting from $J(\theta) = \sum_\tau p_\theta(\tau) R(\tau)$ (Eq. 3):

1. Log-derivative trick: $\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim p_\theta}[R(\tau) \nabla_\theta \log p_\theta(\tau)]$ — reduces to $\sum_t \nabla_\theta \log \pi_\theta(a_t|s_t)$ (Eq. 7)
2. Reward-to-go $G_t$ removes causally irrelevant pre-$t$ rewards (Eq. 8–9)
3. Advantage $A^\pi(s_t, a_t) = Q^\pi(s_t, a_t) - V^\pi(s_t)$ (Eq. 12)
4. GAE + TD bootstrapping → per-step Actor-Critic
5. PPO: clipped importance ratio $r_{i,t} = \pi_\theta / \pi_{\theta_\text{old}}$ + KL penalty (Eq. 23, 31)
6. **GRPO:** substitutes trained critic with $\hat{A}_i = (R_i - \mu_G)/\sigma_G$ broadcast uniformly to all tokens in response $y_i$ (Eq. 30–31)

## Two-axis taxonomy

**Trajectory side** — interventions on how samples enter the update:
- Rollout collection: GRESO, Prompt Replay, PODS
- Diversity: DIVER
- Repair: SCoRe/PAG (fix failed rollouts)
- Clipping: asymmetric clipping (DAPO Clip-Higher)
- Ratio granularity: GSPO (sequence-level ratio)

**Reward side** — interventions on what signal weights the update:
- Critic-free baselines: GRPO group-relative, RLOO leave-one-out, ReMax greedy
- Statistical bias correction: Dr.GRPO (removes std-normalisation bias)
- Credit assignment: PRM, GRAIL (token-level saliency), GTPO (entropy-weighted advantage)
- Reward density/shaping, multi-objective aggregation

**Both-side (compound failures):**
- **Clip–variance coupling:** symmetric clipping + $\sigma_G$ shrink → entropy collapse (DAPO fixes both simultaneously)
- **Granularity coupling:** token-level ratio with sequence-level advantage, or vice versa

## Structural extensions (Part III)

**Agentic RL:** trajectory-side expansion from single-turn generation to multi-turn environment interaction. Adds credit-assignment and delayed-feedback problems on the reward side; does not exit the $J(\theta)$ frame.

**GRPO-OPD hybrid:** reward-side expansion via four operators:
- $T_A$: importance ratio
- $T_B$: advantage
- $T_C$: in-expectation distillation (teacher log-prob on reward side)
- $T_D$: external regularizer

Retains $J(\theta)$; distinct from divergence-minimization OPD (MiniLLM, GKD) which exits the policy-gradient frame.

## Boundary cases (out-of-frame)

- **DPO:** replaces $J(\theta)$ with a preference objective; no rollouts; not a trajectory- or reward-side fix. The paper treats DPO as "outside the policy-gradient frame" and asserts this makes benchmark comparisons across the boundary misleading (§9.1).
- **Divergence-minimization OPD (MiniLLM, GKD):** replaces reward factor with KL divergence; loses all GRPO reward-side improvements.

## Central open problem (§9.3)

No theory for when trajectory-side and reward-side fixes must **co-vary**. The "missing joint theory" for compound failures (when a fix on one axis requires a complementary fix on the other axis to avoid a new failure mode) is identified as the main gap.

## How to use this page

This page is a **derivation anchor** for the rl-optimizers theme. When a new post-GRPO paper arrives, locate it in the two-axis framework first:
- If it only modifies rollout collection / clipping / ratio → trajectory-side
- If it only modifies baseline / credit assignment / reward shaping → reward-side
- If it addresses an interaction between clipping and advantage normalization → compound/both-side
- If it exits $J(\theta)$ (new objective, preference-based, divergence-minimization) → boundary case

## Key figures

- **Figure 1 (p.3):** Full landscape map — blue spine from $J(\theta)$ to GRPO, with trajectory-side, reward-side, and both-side branches; Agentic RL and GRPO-OPD subtrees. The key visual summary.
- **Figure 2 (p.14):** Structure of the GRPO line — GRPO as pure reward-side substitution, then all post-GRPO failure classes.
- **Eq. 3:** $J(\theta) = \mathbb{E}_{\tau \sim p_\theta(\tau)}[R(\tau)]$ — organizing objective
- **Eq. 30–31:** GRPO group-relative advantage and objective
- **Table 1 (p.2):** Survey comparison — this paper is the only one with "From $J(\theta)$", "Diagnostic", "Agentic", and "OPD" all checked

## Source

- `raw/research/weekly-2026-06-26/05-first-principles-policy-optimization.md` (arXiv:2606.16733)

## Related

- [[research/rl-optimizers/_overview]] — comprehensive theoretical reference for the entire RL-optimizer lineage; derivation backbone currently implicit in the overview
- [[research/rl-optimizers/deepseekmath-grpo]] — paper derives GRPO from first principles (Eq. 30–31)
- [[research/rl-optimizers/dapo]] — DAPO's Clip-Higher + Dynamic Sampling is a both-side (clip–variance coupling) fix in §6.4
- [[research/rl-optimizers/dr-grpo]] — std-bias removal is classified as a reward-side statistical-bias-correction intervention in §6.3
- [[research/rl-optimizers/gspo]] — sequence-level ratio is a trajectory-side ratio-granularity fix in §6.2
- [[research/rl-optimizers/grail]] — token-level saliency is a reward-side credit-assignment fix in §6.3
- [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] — BOLT's weighted-SFT objective exits the $J(\theta)$ frame in the same way DPO does
- [[research/teacher-student-rl/_overview]] — GRPO-OPD hybrid (§8) provides the theoretical $T_A$–$T_D$ operator framework for the OPD family
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]] — Dymetman's diversity-collapse maps directly to the clip–variance coupling failure mode (§6.4)
- [[research/synthesis/fine-tuning-best-practices]] — two-axis diagnostic framework is a natural scaffold for the best-practices cookbook; both-side compound failure taxonomy is currently missing from that page
- [[research/weekly-briefs/2026-06-26]] — brought in by the 2026-06-26 weekly sweep
