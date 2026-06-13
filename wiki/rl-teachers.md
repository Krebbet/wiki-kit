# Reinforcement Learning Teachers (RLT) — RL-Optimized Distillation Teachers

RLTs train small (7B) teacher models via RL with dense rewards tied directly to student comprehension of generated explanations, outperforming distillation from models orders of magnitude larger. A 7B RLT beats Bespoke-7B (DeepSeek-R1 traces + postprocessing) across AIME'24, MATH-500, and GPQA Diamond at <0.05% of R1's estimated training compute.

## Method

**Key reframe:** A teacher is given both the question *and* the ground-truth solution and tasked with producing a step-by-step explanation that helps a student model understand *why* the solution is correct. This sidesteps the exploration bottleneck of standard reasoning RL (where the model must first discover solutions).

**Training loop:**
1. Teacher LM receives (question, solution) and generates a candidate explanation.
2. Explanation fed to a frozen student LM.
3. Two dense reward signals computed from the student's response:
   - **Solution-Seeking Reward (r^SS):** Student's log-probability of reproducing the correct solution given the explanation. `avg{log π_s(s_i)} + α · min{log π_s(s_i)}` where α = 0.01.
   - **KL Divergence Reward (r^KL):** Penalizes explanations the student couldn't have generated independently. KL divergence between teacher-conditioned distribution (with solution) and student prior (question only), using average + max reduction.
4. Final reward: `r^RLT = r^SS − λ · r^KL` with λ = 3.
5. GRPO optimization: group size 64, 125 training steps, batch size 1024, LR 1×10⁻⁶, 8×H100.

**Inference pipeline:** RLT generates explanations for training problems → standard SFT run on those explanations for the student.

**Secondary finding:** Pre-RL teacher (no RL training) as a ranker — when 7B outputs are ranked by the RLT reward, keeping only top traces reaches 90% of the Bespoke-R1 baseline. The reward function is a strong signal even without policy optimization.

## Results

**Main distillation results (student = Qwen2.5-7B or 32B, 17K problems):**

| Method | AIME'24 | MATH-500 | GPQA Diamond | Overall |
|---|---|---|---|---|
| RLT-7B → 7B student | 23.3% | 82.8% | 42.4% | 49.50% |
| Bespoke-7B (DeepSeek-R1 traces) | 20.0% | 82.0% | 37.8% | 46.60% |
| RLT-7B → 32B student | 66.7% | 93.4% | 59.6% | 73.23% |
| Bespoke-32B | 63.3% | 93.0% | 58.1% | 71.47% |

**Cold-start RL (student distilled from RLT, then RL fine-tuned):**

| Method | AIME'24 | MATH-500 | GPQA Diamond | Overall |
|---|---|---|---|---|
| RLT-7B → RL | 26.7% | 84.0% | 40.9% | 50.53% |
| Bespoke-7B → RL | 16.7% | 82.8% | 45.4% | 48.30% |

**Out-of-distribution (Countdown, zero-shot):** RLT 52.3% vs direct RL on countdown 50.8% vs Bespoke 49.2%.

**Reward correlation:** Pearson r = 0.89 between RLT reward rank and final student performance.

**Compute:** 7B RLT training: 280.4 H100-hours. 17K explanation generation: 6.7 H100-hours. Estimated DeepSeek-R1 training: >688,000 H800-hours.

## Applicability

Best fit when: you have (question, ground-truth solution) pairs and want strong student reasoning without access to a frontier teacher. Produces a reusable teacher — one 7B RLT can cold-start RL for multiple student sizes and transfers zero-shot to novel domains (Countdown demonstrated). Student is fixed during teacher training, so the teacher is specialized to the designated student's architecture; generalization to other student families not directly tested. Reward requires two student forward passes per training step.

## Novelty

**vs. standard KD:** Conventional distillation collects fixed outputs from a larger teacher; no feedback loop between student comprehension and teacher behavior. RLT closes this loop.

**vs. RLHF-style teacher training:** RLHF uses a proxy reward model. RLT's reward is the student's literal log-probability of the correct answer — direct, dense, ground-truth-tied, no proxy.

**vs. standard RLVR:** RLVR trains on sparse binary correctness rewards, requiring exploration to discover solutions. RLTs receive the solution upfront and optimize only the pedagogical quality of explanations — converting a hard exploration problem into a dense supervision problem.

**Core insight:** Teaching ability and problem-solving ability are separable. A small model trained as a *teacher* (given solutions) via RL can outperform a much larger model used as a *teacher* via trace collection.

## Reproducibility

- Code: https://github.com/SakanaAI/RLT
- arXiv: 2506.08388 (v1: 2025-06-10, v3: 2025-10-29)
- Venue: NeurIPS 2025 (accepted)
- Authors: Edoardo Cetin, Tianyu Zhao, Yujin Tang (Sakana AI)
- Base teacher model: Qwen2.5-7B
- Training: GRPO, 125 steps, batch 1024, group 64, LR 1e-6, 8×H100

## Source

- raw/research/weekly-2026-06-13/05-rl-teachers.md
- arXiv: https://arxiv.org/abs/2506.08388

## Related

- [[rlsd-self-distilled-rlvr]] — RLSD fixes self-distillation's MI gap via on-policy self-distillation; RLT uses a separate dense-reward teacher instead; complementary strategies for improving student reasoning quality
- [[anti-self-distillation]] — AntiSD fixes KL direction for on-policy self-distillation; RLT avoids the problem with a separate teacher
- [[spurious-rewards-rlvr]] — RLT's dense student-comprehension reward is a concrete alternative to sparse binary correctness; relevant to the reward quality debate
- [[high-entropy-tokens-rlvr]] — adjacent paper from same weekly batch; both concern what makes RL-based reasoning training signal effective
