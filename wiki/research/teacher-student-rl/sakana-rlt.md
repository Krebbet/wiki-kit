---
name: sakana-rlt
description: Sakana AI's Reinforcement-Learned Teachers — 7B teacher given (Q, A), RL-rewarded by student's likelihood of recovering the answer from the teacher's explanation; beats distillation pipelines using 670B+ teachers.
type: research
---

# Reinforcement Learning Teachers of Test Time Scaling (RLT)

Cetin, Zhao, Tang — Sakana AI, arXiv:2506.08388 (2025). Trains a class of "Reinforcement-Learned Teachers" (RLTs) specifically to produce distillation traces rather than solve from scratch. RLTs are prompted with both the question $q$ and the ground-truth solution $s$, and tasked to "connect the dots" with step-by-step explanations. Training reward is dense: feed the teacher's explanation to a student and score the student's conditional log-probability of the correct solution. A 7B RLT distilling a 32B student beats existing pipelines that use DeepSeek-R1 / QwQ (orders-of-magnitude larger) as teachers — and training the 32B student takes less than a day on a single H100 node vs months for direct RL.

## Method

Teacher $\pi_\theta$ receives `<question, solution>` in its prompt and produces think-token explanations $t_{o_i}$. Training is GRPO over a two-term reward:

$$r^{SS}_i = \text{avg}\{\log \pi_s^{s_i}\} + \alpha \min\{\log \pi_s^{s_i}\}, \quad \pi_s^{s_i} = \pi_s(s_i \mid t_{o_i}, q_i)$$

$$r^{KL}_i = \text{avg}\{\mathbb{D}_{KL}(\pi_\theta^{t_{o_i}} \| \pi_s^{t_{o_i}})\} + \alpha \max\{\mathbb{D}_{KL}(\pi_\theta^{t_{o_i}} \| \pi_s^{t_{o_i}})\}$$

$$r^{RLT}_i = r^{SS}_i - \lambda r^{KL}_i$$

$r^{SS}$ rewards the student's likelihood of recovering $s_i$ given $(q_i, t_{o_i})$. $r^{KL}$ regularises think tokens toward the student's distribution under $q_i$ alone — without this, the teacher can trivially pump likelihood by restating the solution in the explanation. Avg+min/max reductions prevent length bias and keep every token in the signal. Training: Qwen2.5-7B-Instruct base, 125 GRPO steps, batch 1024, group size 64, lr $1\times10^{-6}$, SFT warmup. At test time the think tokens are extracted and re-packaged into standard student distillation prompts.

## Claims

| Model | Data | AIME 2024 | MATH 500 | GPQA-Diamond | Overall |
|---|---|---|---|---|---|
| Bespoke-7B (R1 distillation) | 17K | 20.0 | 82.0 | 37.8 | 46.60 |
| **RLT-7B** | 17K | **23.3** | **82.8** | **42.4** | **49.50** |
| Bespoke-32B | 17K | 63.3 | 93.0 | 58.1 | 71.47 |
| **RLT-32B** | 17K | **66.7** | **93.4** | **59.6** | **73.23** |
| Bespoke-32B-1K | 1K | 46.7 | 92.6 | 57.5 | 65.60 |
| **RLT-32B-1K** | 1K | **60.0** | **94.0** | **60.1** | **71.37** |

- **Small teacher, large student works.** A 7B RLT distills a 32B student to higher performance than pipelines where the teacher is DeepSeek-R1 (671B) or QwQ-32B.
- **Raw outputs beat post-processed pipelines.** No filtering, re-formatting, or closed-source LM rewrites — RLT's raw traces directly beat Sky-T1 (QwQ post-processed), s1 (Gemini post-processed), Bespoke (R1 post-processed).
- **Cold-start RL wins too.** RLT-7B + RL reaches 50.5 overall vs 48.3 for Bespoke-7B + RL and 40.8 for direct RL on 7B.
- **Zero-shot OOD transfer beats direct RL.** Applied zero-shot to Countdown (no RLT retraining), the 7B RLT produces distillation data that yields *higher* performance than direct RL on Countdown itself. Overlap between direct-RL-solved problems and Bespoke-7B-solved is 98.5% — suggesting RL on the base mostly steers distribution toward long-context generation without adding new capability.
- **Reward correlates with student gain.** Pearson 0.89 between RLT-reward-ranked trace quality and student downstream performance; the top-ranked traces from the teacher *before any RL* already yield 90% of the R1-distillation baseline's gain.
- **Design ablations matter.** Removing $r^{KL}$ produces traces that restate the solution to pump likelihood; removing min/max reductions biases the teacher toward long explanations that dilute hard-token contributions to $r^{KL}$.
- **Compute delta.** Distilling a 32B student on fixed traces: <1 day on single H100 node. Direct RL on the same model/data: months.

## Why this is load-bearing for single-sample concept learning

RLT is the corpus's cleanest instance of the user's described algorithm: an explanation-generating model optimised so that another model can recover the correct answer using it. The `(question, reference-solution, explanation) → student conditional likelihood` loop is exactly the shape required to grade "did the model get the concept from this textbook-style example?" at training time. The $r^{KL}$ regulariser — forcing the explanation to remain plausible from the student's no-solution perspective — is the mechanism that keeps the teacher from trivially leaking the answer, which is precisely the risk in a textbook-exercise loop where the reference material is present during training.

Limitations as-is: RLT requires a separate student model at every gradient step (expensive); the teacher specialises and is not the deployment model; the paper does not test small curricula at the N ≈ 10–100 scale the project targets.

## Follow-ups and adoption (as of 2026-04)

See [[rlt-followups-2026]] for the full landscape. Headline: **no captured 2025-Q4–2026-Q2 follow-up paper directly cites RLT**. The dense teacher-side signal paradigm is healthy and has gained commercial adoption — but via *On-Policy Distillation* (Agarwal 2023 → Qwen3 / MiMo / GLM-5 / Thinking Machines' Tinker) rather than via RLT's reference-in-teacher-prompt framing. The closest paradigmatic sibling is OPSD (Zhao et al., arXiv:2601.18734), which collapses RLT's separate-student cost by making the teacher the same model conditioned on privileged information (verified reasoning traces). Kwiatkowski et al. (arXiv:2602.03979, Meta FAIR + UvA) independently arrive at the $\log \pi(\text{answer}\mid \text{prompt}, \text{CoT})$ reward formula that is structurally identical to RLT's $r^{SS}$, with no citation.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/05-sakana-rlt.md`
- arXiv: https://arxiv.org/abs/2506.08388
- Code: https://github.com/SakanaAI/RLT

## Related

- [[_overview]] — theme synthesis
- [[rlt-followups-2026]] — follow-up landscape and adoption evidence (2025-Q4 → 2026-Q2)
- [[fan-learning-to-teach]] — pre-LLM ancestor of teacher-RL with student-accuracy reward
- [[saha-teacher-explanations]] — inference-time predecessor: teacher explanations improve student predictions
- [[soar-edge-of-learnability]] — bilevel meta-RL with student-improvement reward
- [[ho-reasoning-teachers]] — classical reasoning-distillation: teacher CoT → student SFT
- [[trice-cot-latent-variable]] — marginal-likelihood objective over rationales, same conceptual shape without an external teacher
- [[../single-sample-rl-finetuning/_overview]] — the downstream regime RLT traces feed
- [[../rlvr-mechanics/deepseekmath-grpo]] — base optimiser
- [[../synthesis/single-sample-concept-skeleton]] — RLT is the natural "reference-material-in-context" plug-in for the skeleton's P3 (reward) slot
