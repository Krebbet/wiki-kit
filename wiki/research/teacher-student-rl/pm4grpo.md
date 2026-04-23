---
name: pm4grpo
description: Lee, Park, Sim, Bae (2026) — TACReward / PM4GRPO. Represents reasoning as an event log via process mining; dense reward = structural alignment between student's and teacher's reasoning traces; integrates into sparse-reward policy gradient (RLOO, GRPO, GSPO) without architectural change. GSPO + TACReward: 89.2% avg relative accuracy gain.
type: research
---

# Reasoning-Aware Proxy Reward Model using Process Mining (TACReward / PM4GRPO)

Lee, Park, Sim, Bae — Pusan & Changwon National Universities, arXiv:2510.25065 (preprint Jan 2026). Addresses the sparse-reward problem in reasoning RL: within a GRPO group, if most rollouts have the same correctness, the advantage signal collapses to zero. Proposes **TACReward** (Trace, Alignment, Check Reward), a scalar reward in $[0, 1]$ that measures how well the student's reasoning trace aligns *structurally* with a teacher's, using process mining. Slots into RLOO, GRPO, and GSPO as an auxiliary dense reward without architectural modifications or human annotation.

## Method

Treat each reasoning rollout as an **event log**: a sequence of events $e = (c, a, t, d_1, \dots, d_m)$ where $c$ is the case id (problem id), $a$ is the *activity* (reasoning step type — "Formulate Strategy", "Recall Definition", "Apply Formula", "Verify Answer", etc.), $t$ is the timestamp. A trace $\sigma = \langle e_1, \dots, e_n \rangle$ is the ordered sequence of events in one rollout; the log is a multiset of traces.

**Process mining pipeline (no human annotation required):**

1. **Trace** — extract event sequences from teacher and policy rollouts; no step labels, the activity taxonomy comes from the LM itself.
2. **Alignment** — apply process-mining alignment / conformance-checking (e.g. Alpha Miner, Inductive Miner) between the teacher and policy event logs to compute stepwise structural deviations.
3. **Check** — aggregate deviations into a scalar reward $R \in [0, 1]$.

Drop TACReward into the standard sparse-reward objective alongside the correctness signal. The teacher model $\pi_\phi$ is assumed "more mature" than the policy $\pi_\theta$; no separate PRM training, no step labels.

## Claims

Evaluated on MATH, Omni-MATH, AIME, OlympiadBench, KICE, and CoT-Math:

- **Consistent gains across base optimisers.** TACReward added to RLOO, GRPO, or GSPO beats the plain versions on all benchmarks.
- **GSPO + TACReward: 89.2% average relative accuracy improvement** (headline number).
- **No architectural changes.** The reward is a scalar in $[0, 1]$, so it drops in beside any existing scalar reward.
- **No extra human annotation.** Unlike classical PRMs (PRM800K, Math-Shepherd), TACReward derives step labels from the process-mining alignment rather than curated human annotations.
- **Addresses group-reward collapse in GRPO.** When all rollouts in a group share the same correctness, the traditional advantage estimate vanishes; TACReward provides structural differentiation.

## Positioning

PM4GRPO sits on the student side: the teacher is frozen and serves as a reference process model; the policy (student) is what gets trained. This is the *opposite* direction from [[sakana-rlt]], where the teacher is trained and the student is used to score teacher outputs. The two are conceptually stackable: an RLT teacher provides high-quality reference traces; PM4GRPO then uses those traces as the structural anchor against which the student's RL rollouts are aligned.

Relative to [[../process-reward-models/_overview]]:
- Classical PRMs (Lightman, Math-Shepherd) learn a step-level value function from step labels.
- PM4GRPO replaces the learned PRM with a process-mining alignment against a reference teacher trace — zero training for the reward, provided the teacher's reasoning is trusted.

The unresolved question is *what makes a trustworthy teacher reference* — the paper assumes "more mature than the policy" without a quantitative bound.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/06-pm4grpo.md`
- arXiv: https://arxiv.org/abs/2510.25065
- Code: https://github.com/Thrillcrazyer/TACReward
- Model: https://huggingface.co/Thrillcrazyer/TACReward7B

## Related

- [[_overview]] — theme synthesis
- [[sakana-rlt]] — complementary: teacher-side; RLT trains the teacher, PM4GRPO uses the teacher to score the student
- [[../process-reward-models/_overview]] — step-level reward family; PM4GRPO is the teacher-aligned, annotation-free variant
- [[../process-reward-models/math-shepherd]] — label-free PRM via rollout success rate; comparison point for TACReward's structural approach
- [[../rlvr-mechanics/deepseekmath-grpo]] — base optimiser
- [[../rlvr-mechanics/learning-to-think]] — L2T's Fisher/SVD info-gain reward is the internal-signal analogue of TACReward's external teacher-alignment signal
