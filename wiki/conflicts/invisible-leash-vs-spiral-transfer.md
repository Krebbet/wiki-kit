---
name: invisible-leash-vs-spiral-transfer
description: Conflict — Understanding Self-play's Invisible-Leash bound (solver only re-weights base-model probability mass) vs SPIRAL's headline that game self-play yields +10.5% on 8 reasoning benchmarks beating SFT on 25k expert trajectories. Compatible if "within base-model capacity" includes "non-trivially extractable", but the framings are in tension.
type: conflict
status: open
---

# Conflict — Invisible Leash vs SPIRAL's Game-to-Reasoning Transfer

## Position A — [[../research/self-play/understanding-self-play]] (Chae, Alam, Rastogi, NeurIPS 2025 Workshop)

Self-play's "Invisible Leash" theorem: **the solver only re-weights existing base-model probability mass; new reasoning trajectories cannot be created**. Performance gains from self-play come entirely from the proposer generating a progressively harder, more diverse curriculum. Frozen-proposer ablation confirms locking proposer weights preserves entropy but sacrifices both curriculum evolution and downstream performance. The $p \approx 0.5$ reward-shaping trick that works for one method (R-Zero) fails for another (AZR), reinforcing that *the trained proposer*, not a reward heuristic, drives quality.

**Scope of the claim:** AZR-style and R-Zero-style self-play settings on the configurations tested.

## Position B — [[../research/self-play/spiral]] (Liu et al. 2025)

Multi-turn zero-sum game self-play (Kuhn Poker, TicTacToe, Simple Negotiation) on Qwen3-4B-Base yields **+10.5% across 8 reasoning benchmarks**. Single-game (Kuhn Poker alone) on Qwen3-4B-Base produces +8.6% on math and +8.4% on general reasoning, **outperforming SFT on 25,000 expert game trajectories**. Three transferring cognitive patterns identified: case-by-case analysis, expected-value calculation, pattern recognition. Role-conditioned advantage estimation (RAE) is required — without it, reasoning-trace length collapses to near-zero within 200 steps and math performance drops 35% → 12%.

**Scope of the claim:** Multi-turn zero-sum games, online self-play, Qwen3 / Llama families, 4B–8B.

## Tension

Position A claims gains are bounded by base-model capacity and that the *solver* contribution is essentially nil — improvement comes from *curriculum* (proposer). Position B claims a +10.5% reasoning improvement from game-self-play, beating SFT on 25k expert trajectories — which would seem to require *some* skill installation rather than mere re-weighting.

The two positions are not formally contradictory:
- "Within base-model capacity" can include *latent* reasoning that requires non-trivial extraction. Self-play could be a powerful extraction mechanism without violating the bound.
- Position B's gains are *transfer* from games to reasoning, not within-domain skill install. The proposer in SPIRAL is *the game environment + opponent self-copy*, not a question-generator. Position A's "proposer is everything" framing covers question-generation in AZR-style; SPIRAL's proposer-equivalent is the game itself.

But the **practical implication** for the user's "play with a concept" question diverges:

- If A is the right reading: **focus all design effort on the proposer** (concept-decomposition, question-generation, frontier-targeting). The solver's RL loop is incidental.
- If B is the right reading: **a well-designed game (zero-sum, multi-turn, asymmetric) installs reasoning skills** even when the game has nothing to do with the target domain. The "proposer" is the game design, not a generator policy.

## Editorial reading

The two positions are probably both right at different scales of granularity:
- A's bound is a *capacity* bound — gains live within the support of the base model.
- B's result shows that *extracting* this capacity is non-trivial and that game-self-play is one effective extraction mechanism.

For the wiki's frame (single-sample concept fine-tuning), this matters because:
1. The proposer-quality bottleneck (A) is real, but so is the game-extraction effect (B). Both are levers.
2. SPIRAL's "single-game-suffices" result is surprising and undertheorised — the three transferring cognitive patterns identified are correlational, not causal. The mechanism is not understood.
3. The Invisible-Leash bound is sharp for the AZR-style "ask questions, answer them" loop, but does not directly cover game-self-play with environment dynamics.

## Resolution status

**Refined, still open** *(updated 2026-05-10)*. Two papers from the 2026-05-10 weekly sweep tighten Position A substantially:

- [[../research/rlvr-mechanics/rethinking-rl-sparse-selection]] (arXiv:2605.06241) provides the **token-level mechanistic operationalisation**: across GRPO/PPO/RLOO and three model families, RL reranks 1.0–4.1% of token positions, with **0% shifted outside the base top-5**. Mean promoted rank 2.14–2.39. Oracle intervention exclusively at reranked positions exactly recovers RL pass@1; random substitution does not. The corrective signal fits a rank-32 LoRA at 0.27–0.49% of params (or rank-8 $W_O$ at 0.04%). REASONMAXXER — entropy-gated contrastive on ~50 problems — matches/exceeds full RL at $4–25 vs $200–$103k. **Position A's support-inclusion claim is now empirically sharp at the token level, not just at the trajectory level.**
- [[../research/rlvr-mechanics/binary-rewards-rl-challenges]] (Dymetman, arXiv:2605.02375) supplies the **formal collapse mechanism**. The filtered model $p^* = a(\cdot|\mathcal{Y}_1)$ is the I-projection of base $a$ onto the valid set; KL-controlled RL converges to $p^*$ in *forward* KL as $\beta \to 0$, but $\text{KL}(p^\beta \| p^*) = +\infty$ for every finite $\beta$ (Theorem 3.1d). Under model misspecification + small $\beta$, the optimiser is driven to parametrically-easy near-Dirac policies; $p^*$ is provably unreachable in reverse KL. **Position A now has a structural account of why pass@k drops while pass@1 rises.**

Earlier refinement (2026-05-01) via [[../research/self-play/two-stage-dynamic]] (Yao et al., arXiv:2510.04028) provided the theoretical bridge between Positions A and B:

- **Stage 1 (exploitation):** $\mathbb{E}[\Delta z_v^l] \propto \pi^l(v)$ — gradient updates only flow to already-sampled tokens. Optimal-but-undersampled tokens get $\approx 0$ update because $\pi^l(v) \approx 0$. **Standard GRPO stays here.** This is exactly the regime described by Position A: support narrows, pass@k inverts at large $k$, the Invisible Leash bound is sharp.
- **Stage 2 (exploration):** Once high-reward tokens saturate ($1 - \pi \to 0$), their gradient contribution weakens; suboptimal tokens occasionally get sampled and rise. **GRPO-N variant on Qwen2.5-Math-7B reaches Pass@256 = 100% on AMC2023 vs GRPO 97.5% and base 97.5%, with held-out entropy *exceeding* the base model.**
- The transition is gated by *training duration + entropy preservation*. SPIRAL's game-self-play is entropy-preserving by construction (zero-sum game with continually-improving opponent), making Stage 2 reachable.

**Refined position:**

- Position A (Invisible Leash, Yue) is **Stage-1-scoped**, not a universal bound. It is sharp for short-training RLVR and for setups that don't preserve entropy. [[../research/self-play/invisible-leash]] (Theorem C.1) proves the support bound *for on-policy gradient updates*, which is consistent with Stage-1-only behaviour.
- Position B (SPIRAL transfer) is consistent with Stage-2 dynamics but not directly proved equivalent. The opponent-adaptation mechanism may add something beyond what Stage 2 of standard RLVR provides — this is the genuine residual gap.
- **The original "two compatible claims" reading was right; the two-stage view supplies the formal grounding it lacked.**

**Practical implications for the wiki:**

- Training duration and entropy preservation become *load-bearing hyperparameters* in [[../research/synthesis/proposed-method]], not afterthoughts.
- Position A remains the user's chosen working frame (per memory `feedback_self_play_design_choices.md`), now refined: gains live within base-model latent capacity in Stage 1; Stage 2 *may* extend the support, but extracting Stage-2 dynamics requires explicit entropy preservation (e.g. game-self-play, [[../research/self-play/info-gain-self-play]]'s epiplexity criterion).
- Conflict remains **open** on the residual question: does SPIRAL's opponent-adaptation add something beyond standard Stage-2 RLVR, or is it fully accounted for?
- **2026-05-10 update:** Position A is now token-level-sharp ([[../research/rlvr-mechanics/rethinking-rl-sparse-selection|Rethinking-RL]] sparse selection) and structurally-grounded ([[../research/rlvr-mechanics/binary-rewards-rl-challenges|Binary-Rewards]] forward-vs-reverse-KL asymmetry). The residual question — whether game-self-play's transfer is genuinely outside Position A's bound or just a Stage-2 instantiation of it — now turns squarely on whether **SPIRAL extends the support** (Position-B-specific) or merely **rebalances within it** (Position A consistent). Neither has yet directly tested this with token-level support diagnostics on SPIRAL training.

## Related

- [[../research/self-play/_overview]] — covers both positions in the theme synthesis
- [[../research/self-play/understanding-self-play]] — Position A operationalised
- [[../research/self-play/invisible-leash]] — Position A formalised (Theorem C.1)
- [[../research/self-play/yue-rlvr-boundary]] — Position A empirical foundation (pass@k inversion)
- [[../research/self-play/two-stage-dynamic]] — the refinement that makes Position A Stage-1-scoped
- [[../research/self-play/spiral]] — Position B (Stage-2-consistent)
- [[../research/self-play/spag]] — adversarial language game; partial bridge between the two
- [[../research/self-play/info-gain-self-play]] — epiplexity as the criterion for whether Stage 2 is reachable
- [[../research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — Wen et al. (2506.14245): **counter-evidence to A** (corrected 2026-05-16 — previously mislabelled "Shao et al., sympathetic to A"). Uses CoT-Pass@K to argue RLVR genuinely extends the reasoning boundary, contra the pure-reweighting reading. Strengthens the case that the A/B conflict is unresolved, not settled for A.
- [[../research/rlvr-mechanics/rethinking-rl-sparse-selection]] — token-level sharp evidence for Position A (2026-05-10)
- [[../research/rlvr-mechanics/binary-rewards-rl-challenges]] — formal collapse mechanism for Position A (2026-05-10)

## Source

Conflict between captured wiki pages (no single raw doc — this is a cross-source tension):
- Position A: [[../research/self-play/invisible-leash]] (Theorem C.1), [[../research/self-play/yue-rlvr-boundary]] (pass@k inversion), [[../research/rlvr-mechanics/rethinking-rl-sparse-selection]], [[../research/rlvr-mechanics/binary-rewards-rl-challenges]]
- Position B: [[../research/self-play/spiral]] (game-self-play transfer)
- Refinement: [[../research/self-play/two-stage-dynamic]] (Stage-1-scoping)
- Counter-evidence to A: [[../research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] (Wen et al., CoT-Pass@K boundary extension)
