---
name: fan-learning-to-teach
description: Fan et al., ICLR 2018 — pre-LLM canonical "Learning to Teach" (L2T). Teacher agent trained via REINFORCE with held-out validation accuracy as reward; outputs training-data, loss, or hypothesis-space actions. Halves training-data requirement, transfers across architectures.
type: research
---

# Learning to Teach (L2T)

Fan, Tian, Qin, Li, Liu — ICLR 2018, arXiv:1805.03643. The canonical pre-LLM paper that frames the teacher as a parametric agent optimised by reinforcement learning against student feedback. Two intelligent agents interact: the *student* $\mu(D, L, \Omega)$ is an ordinary supervised learner minimising empirical risk; the *teacher* $\phi_\theta$ outputs one of three action types — training data $D$, loss function $L$, or hypothesis space $\Omega$ — to facilitate student training. The teacher's reward is the student's held-out validation accuracy after the student updates, and the teacher is optimised with REINFORCE. Paper focuses on *data teaching* ($A = D$) empirically.

## Method

Formulated as a sequential decision process:

- State $s_t \in \mathcal{S}$ constructed from the current student $f_{t-1}$ plus past teaching history.
- Action $a_t \in \mathcal{A}$: a subset of training data (data-teaching), a loss function (loss-teaching), or a hypothesis space (model-teaching).
- Teacher policy $\phi_\theta: \mathcal{S} \to \mathcal{A}$ optimised to maximise $\mathcal{M}(\mu(D, L, \Omega), D_{\text{test}})$ — the student's performance under its own SGD / ERM procedure on the teacher-selected inputs.
- Reward = student's accuracy on a held-out development set after the student update.
- Optimisation: REINFORCE.

Once converged, the teacher can be transferred to new students and new tasks without retraining, provided the state representation is shared. In data-teaching the teacher re-selects training minibatches adaptively rather than following a fixed curriculum (CL) or self-paced schedule (SPL).

## Claims

- **Data-efficiency.** With L2T-selected data the student reaches roughly the same accuracy as a standard learner using "roughly half" of the training data on image classification and text understanding tasks.
- **Architecture-agnostic.** Works across MLP, CNN, RNN — the teacher is not tied to a specific student architecture.
- **Transfer.** Teacher trained on MNIST with an MLP student transfers to CIFAR-10 with a ResNet student, still yielding the data-efficiency gain without teacher retraining.
- **Convergence-speed gain.** Fewer iterations to reach target accuracy, in addition to using less data.
- **Framework generality.** Covers data-teaching, loss-teaching, and hypothesis-space-teaching as three instances of the same bilevel agent-agent RL formulation.

## Positioning

The paper predates the current teacher-rationale lineage (CoT, reasoning traces, LM-as-teacher). Its contribution is the *formulation*: teaching as an optimisation problem, with a parameterised teacher agent and a gradient (via RL) flowing from student feedback back into teacher parameters. Modern LLM-era variants — RLT ([[sakana-rlt]]), SOAR ([[soar-edge-of-learnability]]) — all inherit this structure; what changes is (a) the action space (now natural-language explanations or synthetic Q–A pairs) and (b) the inner-loop student signal (now log-likelihoods of correct solutions, not validation accuracy). The older machine-teaching literature (Zhu et al.) required an oracle target model; L2T dropped the oracle assumption and replaced it with a bilevel RL objective.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/01-fan-learning-to-teach.md`
- arXiv: https://arxiv.org/abs/1805.03643

## Related

- [[_overview]] — theme synthesis
- [[sakana-rlt]] — LLM-era descendant: same bilevel RL but explanations instead of data selection
- [[soar-edge-of-learnability]] — bilevel teacher-student meta-RL at LLM scale, rewards grounded in student progress
- [[saha-teacher-explanations]] — inference-time analogue: teacher explanations guide student predictions
- [[../meta-learning-few-shot/_overview]] — Schmidhuber/Finn meta-learning lineage that L2T parallels on the teaching side
