---
name: soar-edge-of-learnability
description: Sundaram et al. (MIT/Meta FAIR, 2026) — SOAR. Bilevel meta-RL; teacher LLM generates synthetic Q–A pairs, student trains on them with RLVR, teacher rewarded by student's improvement on a fixed hard dataset. Escapes plateaus where direct RL has 0/128 success.
type: research
---

# Teaching Models to Teach Themselves: Reasoning at the Edge of Learnability (SOAR)

Sundaram, Quan, Kwiatkowski, Ahuja, Ollivier, Kempe — MIT & Meta FAIR, arXiv:2601.18778 (Feb 2026). Addresses RLVR's fundamental plateau problem: when the initial success rate on a target dataset is near zero, RL has no gradient signal. SOAR (Self-Optimization via Asymmetric RL) is a bilevel meta-RL framework in which a *teacher* copy of the model generates synthetic question-answer pairs, a *student* copy trains on them with standard RLVR, and the teacher is rewarded by the student's measured improvement on the fixed hard dataset. The teacher never sees the hard problems — it discovers useful stepping stones purely through the student-progress reward signal.

## Method

Let $\pi_\theta$ be a base LM. Assume a dataset $\mathcal{D} = \{(q_i, a_i)\}$ of hard problems where $\pi_\theta$ achieves 0/128 successful generations; split into $\mathcal{D}_{\text{train}}, \mathcal{D}_{\text{test}}$.

Bilevel objective:

$$\max_\phi \mathbb{E}_{\mathcal{X} \sim \pi_\phi^T} \left[ R\left(\pi_{\theta'(\mathcal{X})}^S, \mathcal{D}_{\text{train}}\right) \right] \quad \text{s.t.} \quad \theta'(\mathcal{X}) = \text{RL-UPDATE}(\theta, \mathcal{X})$$

- **Outer (teacher) loop.** RLOO trains the teacher $\pi_\phi^T$. Group size $g$, samples $g\cdot n$ rollouts subdivided into $g$ candidate synthetic datasets $\mathcal{X}_1, \dots, \mathcal{X}_g$ of size $n$ each. Teacher generates both question and answer (no automatic verifier for synthetic correctness).
- **Inner (student) loop.** Student $\pi_\theta^S$ trains with RLVR (also RLOO) on $\mathcal{X}_k$ for 10 steps, producing $\theta'(\mathcal{X}_k)$. Student baseline performance on a sampled subset of $\mathcal{D}_{\text{train}}$ gives the teacher reward for candidate $\mathcal{X}_k$.
- **Avoiding BPTT.** RLOO in the outer loop replaces unrolling the inner loop with a REINFORCE-style estimator; this is the first "double meta-RL loop" for LLM self-play the authors know of.
- **Grounded vs intrinsic rewards.** Teacher is *not* rewarded by majority-vote consistency, intrinsic learnability proxies, or reward-model preferences — those are what the authors deliberately avoid, having observed prior self-play systems drift to degenerate tasks, suffer diversity collapse, and hit sudden performance collapse.
- **Initialisation:** $\theta = \phi = \theta_{\text{base}}$. Llama-3.2-3B-Instruct in the main experiments.

## Claims

On hard subsets of MATH and HARP (problems where the base model achieves 0/128):

- **MATH hard subset:** ~4× pass@1 and ~2× pass@32 over direct-RL baseline.
- **HARP hard subset:** ~2× pass@1 and ~1.5× pass@32.
- **Transfer:** teacher-generated problems trained on one hard dataset transfer to unlock learning on hard datasets they were not optimised for.
- **Decoupled teaching and solving.** A base LM that cannot solve the hard problems can nevertheless generate useful stepping stones — meta-RL sharpens this latent pedagogical capacity into a reliable signal.
- **Grounded > intrinsic.** Grounding the teacher reward in student progress on real problems outperforms intrinsic/proxy rewards used in prior self-play, and avoids the diversity-collapse and reward-hacking failure modes.
- **Structure beats correctness.** Analysis of generated questions reveals that *structural quality and well-posedness* matter more for learning progress than whether the teacher's proposed answer is actually correct. Even with mostly incorrect answers, structurally reasonable questions provide gradient signal.

Study is backed by >600 multi-seed runs with ablations.

## Positioning

SOAR differs from [[sakana-rlt]] in two structural ways. (i) In SOAR the teacher produces *new problems*; in RLT the teacher produces *explanations for given problems*. (ii) SOAR's reward is *student's held-out accuracy change*; RLT's is student log-probability on the provided solution — orders-of-magnitude denser but requires the solution to be available to the teacher. The two are complementary: SOAR's teacher expands the problem distribution, RLT's teacher densifies the per-problem reasoning signal. A composition — SOAR generates a stepping-stone curriculum, RLT explains each step — is not in the paper.

The "teacher can propose useful exercises without being able to solve them" result is directly relevant to curriculum-with-reference designs: it suggests that even a base model unable to solve the target problems can still surface a workable exercise set from latent pretraining knowledge, provided the reward loop measures *student progress* rather than trusting the teacher's own correctness.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/04-soar-edge-of-learnability.md`
- arXiv: https://arxiv.org/abs/2601.18778
- Project page: https://ssundaram21.github.io/soar/

## Related

- [[_overview]] — theme synthesis
- [[fan-learning-to-teach]] — canonical bilevel teacher-RL with validation-accuracy reward
- [[sakana-rlt]] — RL-teacher with dense per-step log-prob reward; complementary action space (explanations, not curricula)
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — DOTS targets $p=0.5$ difficulty; SOAR's "generate the right stepping stones" is a generative analogue
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — the plateau-avoidance axis: 1-shot RLVR picks a high-variance seed; SOAR generates many
- [[../self-improvement/_overview]] — self-play adjacent; SOAR's contribution is grounding rewards in real-dataset progress rather than intrinsic proxies
