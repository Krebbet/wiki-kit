# MRPD: Replay, Don't Resample — Off-Policy Consolidation of Long-Horizon RL Experts (Yue et al., UIUC)

MRPD (Multi-expert Replay Policy Distillation) consolidates per-domain GRPO experts into one student by replaying the experts' own RL training logs in chronological order. Each step does a policy-gradient update with the importance ratio taken against the logged policy, plus a dense reverse-KL to the final experts at the logged prefixes. It makes no generation, tool or environment calls. On Qwen3-4B with three domains (reasoning, search, SQL), it scores 58.6 average over 16 held-out sets against 58.1 for multi-teacher on-policy distillation (MOPD), at 9.2 h vs 29.4 h wall-clock on 8 H100s. Ablations say log order matters more than data amount or rewards. It is not a single-sample paper: it uses about 460k logged trajectories. arXiv:2611.24059.

## Method

Setup: $D=3$ domains (Python-sandbox reasoning / ReTool, search / Search-R1, SQL / Spider+BIRD), binary reward in $\{-1,+1\}$, shared SFT-cold-start init $\pi_{ref}$ (Qwen3-4B). One GRPO expert per domain, $K=300$ steps, 64 prompts x 8 samples per step, lr $10^{-6}$, clip $(0.2, 0.28)$, no KL penalty. Each run logs tokens, loss mask (tool outputs excluded), reward and the sampling log-probs $\pi_{old}$ per sample.

Replay: at step $k$, take one optimizer step on $D_k=\bigcup_d D_k^d$ (1536 samples). The student walks the experts' trajectory in order, from policies near $\pi_{ref}$ to the final experts.

$$J=\mathbb E\Big[\tfrac1g\sum_i\tfrac1{|M_i|}\sum_{t\in M_i}\big(\min(r_tA_i,\,\mathrm{clip}(r_t)A_i)-\beta\,\mathrm{KL}(\pi_\theta\|\pi_T^d)\big)\Big],\quad r_t=\frac{\pi_\theta}{\pi_{old}^{k,d}}$$

- The ratio is taken against the logging policy, with group-normalized advantage $A_i$.
- Default KL is dense: closed form over the top-256 tokens plus a tail atom, $\beta=1$, applied outside the clip.
- The sampled-token variant (MOPD-style) enters through the advantage and goes through the clip.
- Cost per step: one forward pass of each expert; the trainer is the only process.

## Key claims

- **Order, then amount, then reward.** Shuffling the step order costs 0.6 points (dense KL) or 1.0 (sampled-token) with KL. Without KL it costs 3.8 (SFT), 2.6 (RAFT) and 3.1 (PG-only). Cutting to 576 samples/step costs only 0.2-0.5. Zeroing rewards costs 0.4-0.5. Ordered 576/step (58.5) still matches MOPD and beats the full shuffled logs (58.0).
- **Quasi-on-policy.** Mean $|\log\pi_\theta-\log\pi_{old}|$ starts at 0.012. PG-only never exceeds 0.026 (clip fraction $\le0.003$, near MOPD's 0.017). Dense KL opens a gap that peaks at 0.126 around step 20 (4% of tokens clipped), then falls to 0.019 as the logs catch up. Shuffled replay stays high.
- **Dense beats sampled-token KL** by 0.4-0.5. The sampled-token estimate is unbiased only for student-sampled tokens, covers one coordinate, and gets clipped.
- **KL direction is second-order.** Reverse beats forward (58.6 vs 57.8) only when combined with PG. $\beta=1$ is best; 3x either way costs about 0.5.
- **The teacher term adds about 1 point on identical logs.** KL alone 58.2; KL+PG 58.6; no-KL PG-only 57.7, RAFT 57.6, SFT 57.5.
- **Inherited drift.** MOPD inherits the final search expert's drift (the expert hits the turn limit in about 60% of rollouts; the MOPD student in 80% from step 50). MRPD's ordered replay avoids this.

## Results

| Method | Avg (16 sets) | Cost (8 H100) |
|---|---|---|
| $\pi_{ref}$ | 28.2 | - |
| Uniform soup / TIES | 46.1 / 56.8 | - |
| RAFT / online GRPO / PPO | 51.5 / 52.5 / 52.6 | 22-24 h (GRPO / PPO) |
| MOPD / MOPD+GRPO | 58.1 / 58.2 | 29.4 h (MOPD+GRPO) |
| **MRPD** | **58.6** | **9.2 h** (110 s/step); 3.7 h data-matched (576/step) |
| GRPO experts (teachers) | 59.3 | 30 / 32 / 4.5 h total |

Per domain, MRPD scores reasoning 63.7, search 42.0 and SQL 70.1, and is the only student in the top two on every domain. MOPD is best on reasoning (63.8) and worst on search (40.6). Consolidation costs about 14% of expert training compute. The worst MRPD step is 173 s, against 626-1887 s for online runs.

## Limitations

- The online baselines get 576 samples/step (to keep sampling affordable), which confounds the "beats online RL" claim. The MOPD teacher is the same final expert, which favors logs taken from the teacher's trajectory.
- Reasoning is the hardest domain: AIME24 50.4 vs 53.8, AIME25 40.7 vs 42.5, AMC23 87.5 vs 90.3. Reward reaches 0.2 only after about 75 steps, against about 30 for MOPD. The student trails its GRPO experts by 0.7.
- Needs a shared init $\pi_{ref}$ and retained logs with log-probs that match the trainer's numerics. Only 3 domains, one 4B model, binary rewards, $K=300$. Scaling to more experts or larger models is untested.
- The "curriculum" reading is inferred from the shuffle ablation; no reverse-order or controlled curriculum run. No forgetting or OOD measurement.

## What it means for our thesis

- **Consolidation recipe.** If concept-specific single-sample experts (1-40B) are trained separately, MRPD is a cheap way to merge them without merging-induced collapse (merging collapses on search/SQL here). It needs no new rollouts, only retained logs.
- **Trajectory as curriculum.** The expert's own training path is a free easy-to-hard schedule. This supports ordered, staged data in [[../synthesis/concept-curriculum-method]]. Evidence is indirect (one shuffle granularity).
- **Dense teacher signal over outcome reward.** The distillation term adds about 1 point over reward-only replay, matching the pattern that dense token signal carries more than sparse outcome reward.
- **Gaps.** There is no concept-transfer or perturbation test, so the paper cannot separate concept acquisition from pattern imitation. Forgetting is unmeasured, so the quasi-on-policy mismatch numbers are only a proxy for the on-policy-forgetting story in [[../catastrophic-forgetting/rls-razor]].

## Conflicts

- Tension: [[opd-vs-offpolicy-kl-direction]] reports that reverse KL is sensitive to rollout policy and prefers student rollouts. MRPD applies reverse KL on logged, non-student prefixes and it works (58.6), but only because ordered replay keeps the student quasi-on-policy (shuffled replay degrades; direction matters only with PG). Soft tension, partly reconciled; it extends the "rollout policy is not central" thread. No conflict page filed.
- Extension: [[../../conflicts/opsa-vs-opd-pattern-transfer]]. A teacher distribution adds a small, consistent gain (about 0.5-1.0) on identical logs, while most of the gain comes from the replayed trajectories themselves. This is weak support for neither Position A (teacher not needed) nor a strong Position B.

## Source

- `raw/research/weekly-2026-11-20/04-mrpd-replay-consolidation.md` (arXiv:2611.24059)

## Related

- [[mopd-gradient-diagnosis]] — dense top-k vs sampled-token KL parallels that page's top-64 KL result
- [[dn-mopd-domain-normalized]] — multi-teacher consolidation seesaw; different failure axis (inherited drift)
- [[opd-vs-offpolicy-kl-direction]] — controlled on/off-policy KL study; see Conflicts
- [[semi-opd-offline-student-rollouts]] — another rollout-reuse OPD variant
- [[co-evolving-policy-distillation]] — challenges fixed-teacher MOPD; MRPD keeps fixed teachers but changes the data path
- [[opd-dual-nature-generalization]] — routed multi-teacher OPD
- [[opsa-teacher-free-self-adaptation]] — teacher-free variants vs the roughly 1-point KL gain
- [[esr-early-stopping-opd]] — both attack OPD rollout cost
- [[../catastrophic-forgetting/rls-razor]] — on-policy forgetting counterpart
- [[../curriculum-and-decomposition/_overview]] — logs as curriculum
- [[../curriculum-and-decomposition/e2h-curriculum-rl]] — curriculum ordering for RL
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — rollout reuse in RFT
- [[../rlvr-mechanics/deepseekmath-grpo]] — base GRPO objective
- [[../synthesis/concept-curriculum-method]] — curriculum framing for our method
- [[../../conflicts/opsa-vs-opd-pattern-transfer]]
- [[../weekly-briefs/2026-11-20]] — brought in by the 2026-11-20 weekly sweep
