---
name: spiral
description: Liu et al. 2025 — multi-turn multi-agent self-play on zero-sum language games (Kuhn Poker, TicTacToe, Simple Negotiation) with role-conditioned advantage estimation (RAE); trains LLMs on game play alone and achieves up to +10.5% transfer to reasoning benchmarks, beating SFT on 25k expert trajectories.
type: research
---

# SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn RL

Bo Liu, Leon Guertler, Simon Yu, Zichen Liu, Penghui Qi, Daniel Balcells, Mickel Liu, Cheston Tan, Weiyan Shi, Min Lin, Wee Sun Lee, Natasha Jaques. Preprint 2025. arXiv:2506.24119. A fully online multi-agent self-play system that trains LLMs on three zero-sum language games with verifiable outcomes. The key technical contribution is Role-conditioned Advantage Estimation (RAE), which maintains separate EMA baselines per game and role to correct for positional asymmetries; without RAE, reasoning-trace length collapses to near-zero within 200 steps and math performance drops from 35% to 12%. Multi-game SPIRAL training achieves +10.5% average across 8 reasoning benchmarks on 4 model families, outperforming SFT on 25,000 expert game trajectories from a 32B teacher model.

## Method

A single shared policy $\pi_\theta$ plays both roles in each game via system-prompt role conditioning (no separate parameters per role). Actors run in parallel (vLLM + TextArena); a centralised learner performs synchronous policy-gradient updates on Oat's distributed actor-learner architecture.

**Reward.** Terminal only: $R_0(\tau) = \rho_i(s_T) \in \{-1, 0, 1\}$, $R_1(\tau) = -R_0(\tau)$. All intermediate rewards are 0. No KL penalty, no entropy bonus, no length normalisation.

**Role-conditioned Advantage Estimation (RAE).** Standard REINFORCE on zero-sum games is high-variance because opposing objectives and positional asymmetries (first-move advantage in TicTacToe, information asymmetry in Kuhn Poker) create different positional baselines. RAE maintains a separate EMA baseline $b_{G,p}$ for each game $G$ and player role $p$:

$$b_{G,p} \leftarrow \alpha\, b_{G,p} + (1 - \alpha)\, R_p(\tau), \quad A_{G,p}(\tau) = R_p(\tau) - b_{G,p}$$

Variance-reduced policy gradient:

$$\nabla_\theta J_\text{SPIRAL}(\theta) = \mathbb{E}_{G \sim \mathcal{G}}\; \mathbb{E}_{\tau \sim \pi_\theta \times \pi_\theta \mid G} \left[ \sum_{p \in \{0,1\}} A_{G,p}(\tau) \cdot \sum_{t \in T_p} \nabla_\theta \log \pi_\theta\!\left(y_t^{(p)} \mid s_t, p, G\right) \right]$$

PPO-style clipping ($\epsilon = 0.2$) applied during inner update epochs.

**Three games** chosen for complementary cognitive targets:
- **TicTacToe** — spatial/pattern reasoning, perfect information
- **Kuhn Poker** — probabilistic inference, EV calculation, information asymmetry
- **Simple Negotiation** — strategic optimisation, multi-turn bargaining

**Online self-play.** Both players are copies of the current policy $\pi_\theta$; the opponent improves continuously alongside the learner, creating an automatic curriculum. Fixed-opponent training plateaus and leads to exploitation strategies; self-play maintains ~50% win rate throughout (Table 3).

## Claims

| Setting | Metric | Before | After | Delta |
|---|---|---|---|---|
| Qwen3-4B-Base, multi-game | Avg 8 benchmarks | 34.0% | 44.5% | +10.5% |
| Qwen3-8B-Base, multi-game | Avg 8 benchmarks | 39.5% | 49.6% | +10.1% |
| Qwen3-4B-Base, Kuhn Poker | AIME24 | 9.6% | 18.2% | +8.6% |
| Qwen3-4B-Base, Kuhn Poker | MMLU-Pro | ~49% | ~57% | +8.4% |
| SPIRAL (single game, 400 steps) vs SFT (25k Qwen3-32B trajectories) | Avg 8 benchmarks | 39.7% | 39.7% (SFT) | SPIRAL wins all 8 |

- Without RAE: reasoning-trace length collapses to near-zero within 200 steps; MATH500 accuracy drops from ~35% to ~12%.
- Multi-game training (59.5% win-rate vs Gemini 2.5 Flash) beats all single-game specialists (best: 52.9%), confirming game complementarity.
- Already-RLVR-trained DeepSeek-R1-Distill-Qwen-7B gains +1.4%.
- Llama-3.1-8B-Instruct gains +2.0%, showing transfer even from instruction-tuned models.
- Statistically robust over 3 random seeds (14, 42, 100).

**Transfer patterns (GPT-4.1 CoT classification over 290 game traces + 46,792 math solutions):**

| Pattern | Game traces (late training) | Math solutions (late training) |
|---|---|---|
| Case-by-case analysis | 72% | 71% |
| Expected value calculation | 78% | 28% |
| Pattern recognition | 35% | 45% |

Note: correlational analysis, not causal.

## Why this is load-bearing for single-sample concept learning

The counter-intuitive transfer result — abstract zero-sum games improve AIME and GPQA with zero math exposure during training — is the paper's centrepiece, and it is genuinely surprising even given the base-model-capacity framing of [[understanding-self-play]]. The relevance to single-sample concept learning is *indirect*: SPIRAL is about *transfer* from game-structured self-play, not about learning a specific concept from one example.

The RAE contribution is the most transferable technical idea. Multi-turn concept-learning RL faces exactly the variance problem RAE solves: if a model alternates between a "proposer role" and a "solver role" within a single trajectory (as in [[../self-improvement/multi-turn-policy-verifier]]), role-specific baselines prevent the advantage estimates for different roles from interfering. RAE is a lightweight solution that does not require separate critic networks per role.

The result that RAE failure causes reasoning-trace collapse (35% → 12% on MATH500 without it) is a strong empirical argument that role-specific credit assignment is load-bearing, not a minor stabilisation detail. This is worth preserving in the design of any multi-turn, multi-role training loop.

**Tension with [[understanding-self-play]].** The Invisible Leash bound says self-play cannot generate reasoning trajectories outside the base model's support. SPIRAL's +10.5% gains are consistent with this: they represent *within-support* redistribution of probability mass rather than genuinely novel reasoning. But the magnitude of the gains and the specificity of the transfer (EV calculation from Kuhn Poker) push the limits of a "mere redistribution" interpretation. This tension is a candidate for `wiki/conflicts/` once the conflicts directory is populated.

## Limitations

- Game environments are hand-picked and engineered; the design of games may implicitly encode biases constraining which reasoning patterns emerge.
- Transfer mechanism is correlational, not causal (LLM-as-judge classification).
- Computational cost: 8 H100 GPUs, ~25 hours per run — at the boundary of "small LLM" research budgets.
- Reasoning-trace lengths plateau after ~400 steps; simply extending training duration does not help.
- No analysis of negative transfer or catastrophic forgetting.
- Reward hacking acknowledged but not observed in these simple games; risk increases in complex environments.
- Evaluation on academic benchmarks only; no real-world task transfer tested.

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/09-spiral.md`
- `../../../raw/research/self-play-concept-learning/09-09-spiral.md`
- arXiv: https://arxiv.org/abs/2506.24119

## Related

- [[../rl-optimizers/_overview]] — RAE is a multi-agent variant of REINFORCE with role-specific EMA baselines; connects to GAE and advantage normalisation lineage
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — sparse terminal reward structure and entropy / KL considerations parallel SPIRAL's design
- [[../self-improvement/_overview]] — self-play as curriculum; automatic opponent evolution
- [[understanding-self-play]] — Invisible Leash tension: SPIRAL's gains are within base-model support, but their magnitude challenges a weak interpretation of the bound
- [[two-stage-dynamic]] — supplies the resolution: SPIRAL's gains are consistent with Stage-2 dynamics (game-self-play preserves entropy by construction, satisfying the Stage-2 entry condition); the Invisible Leash bound is Stage-1-scoped
- [[invisible-leash]] — the formal bound; SPIRAL's results demonstrate that entropy-preserving self-play sits in a regime where the bound's on-policy assumption is approached but not violated
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — the open conflict; refined 2026-05-01 with Two-Stage account
- [[spag]] — game-as-reasoning-training parallel; different game choice and training objective
- [[asymmetric-self-play]] — pre-LLM two-agent template; SPIRAL generalises to multi-turn language games
- [[_overview]] — theme synthesis
