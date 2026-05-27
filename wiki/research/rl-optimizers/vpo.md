# VPO — Vector Policy Optimization

VPO (Bahlous-Boldi, Puri, Shenfeld et al., MIT Improbable AI / Sakana AI, arXiv:2605.22817) is a drop-in replacement for the GRPO advantage estimator that trains a policy to produce **reward-diverse sets of candidates** by substituting a fixed scalar scalarization with stochastic Dirichlet-sampled scalarizations over a vector-valued reward. The core argument: scalar RL post-training collapses the policy's output distribution, destroying the diversity that test-time search (best@k, evolutionary search) depends on. VPO reframes post-training as a coverage problem over the Pareto frontier of reward components, leaving exploitation to the downstream search procedure.

## Source
- [`raw/research/vector-policy-optimization/01-vpo-paper.md`](../../../raw/research/vector-policy-optimization/01-vpo-paper.md) — arXiv:2605.22817, captured 2026-05-27

## Problem: diversity collapse under scalar RLVR

Under standard GRPO, all rollouts in a group receive gradient toward whichever candidates currently maximise the fixed scalar $w^{*\top}r(x,y)$. As training progresses, the policy's candidate distribution collapses: additional samples become near-duplicates. The paper quantifies this on Maze (Qwen3-4B): GRPO's reward diversity metric drops to 0.003 by end of training, and best@k plateaus at 0.432 regardless of k. This is the same diversity-collapse problem documented analytically in [[../rlvr-mechanics/binary-rewards-rl-challenges]] (I-projection mode collapse) and empirically in [[../single-sample-rl-finetuning/1-shot-rlvr]] (post-saturation gibberish traces).

When test-time search is available, training should focus on *coverage* — producing a candidate pool that spans diverse high-quality trade-offs — rather than converging to a single best response.

## Setting: vector-valued rewards

In many practical tasks the reward decomposes naturally into $d$ components:
$$r(x,y) = [r_1(x,y), \ldots, r_d(x,y)] \in \mathbb{R}^d$$

Examples: per-test-case correctness in code generation, per-criterion preference scores in RLHF, per-hop correctness in multi-hop reasoning, per-tool-call structural/content scores in agentic tasks. Any weight vector $w \in \Delta^{d-1}$ over the simplex induces a scalar objective $w^\top r(x,y)$; standard training fixes a single $w^*$.

## Algorithm

VPO has two components: multi-answer chains (capacity) and stochastic scalarization (incentive).

### Component 1 — Multi-answer chains

Following Puri et al. [2026] (Multi-RLVR), the model emits $m$ candidate completions $S = \{y_1, \ldots, y_m\}$ within a single autoregressive rollout, separated by a delimiter. Each $y_i$ attends to all prior $y_1, \ldots, y_{i-1}$, giving the model in-context capacity to recognise which regions of the solution space are already covered and steer subsequent candidates toward different ones. This provides the *capacity* for diversity but not the incentive — without an appropriate reward, the model still collapses to near-identical answers (verified in the Multi-RLVR ablation: reward-space diversity collapses in 3 of 4 domains under a fixed scalarization).

### Component 2 — Stochastic scalarization / set-level objective

For each rollout, $K$ weight vectors are sampled iid from $\text{Dir}(\alpha=1)$ (uniform over the simplex). The set-level reward is:
$$\hat{R}(S^{(g)}) = \frac{1}{K}\sum_{k=1}^{K}\max_{s \in S^{(g)}} w^{(k)\top} r(x, s)$$

This is a Monte Carlo estimate of $R(S) = \mathbb{E}_{w \sim \text{Dir}(\alpha)}[\max_{y \in S} w^\top r(x,y)]$, which directly rewards *covering* the Pareto frontier rather than concentrating on a single trade-off. The $K$ weights are shared across all $G$ rollout-sets in the group, ensuring that advantage estimates are comparable.

### GRPO integration

Advantage = within-group z-score over per-rollout $\hat{R}(S^{(g)})$ scores, broadcast uniformly across every token in rollout $g$. No value/critic network. Standard PPO-clip ($\varepsilon=0.2$) objective. **The only departure from vanilla GRPO is the advantage estimator.**

## When VPO helps vs. hurts

### Non-collinearity condition (on-policy ρ̄ diagnostic)

VPO's advantage requires the on-policy reward components to be *non-collinear*. The paper measures $\bar{\rho}$ = mean off-diagonal Pearson correlation of the $d \times d$ reward correlation matrix computed from the trained policy's rollout pool. The gain is roughly linear in $(1 - \bar\rho)$:

| Domain | $\bar\rho$ | VPO best@k advantage |
|---|---|---|
| Maze | 0.39 | +0.161 |
| EUREQA | 0.05 | +0.022 |
| MuSiQue | — | +0.104 (best@30) |
| UltraFeedback (5 ArmoRM dims) | 0.95 | −0.004 (VPO *hurts*) |

When reward components are effectively collinear under the current policy (e.g., UltraFeedback's ArmoRM dimensions), the Dirichlet simplex collapses to a near-line and VPO provides no diversity benefit. **Run the $\bar\rho$ diagnostic before deciding to use VPO.**

### Pass@1 regression trade-off

VPO is designed for test-time search (best@k or evolutionary search) and explicitly accepts a pass@1 regression. On LiveCodeBench (Qwen2.5-Coder-7B-Instruct), VPO is *worse* than GRPO at pass@1 but outperforms at every best@k (k > 1), with the gap widening with k. Inside the OpenEvolve evolutionary search loop on the 32 hardest problems (those where both methods score 0 at best@30), VPO continues discovering solutions over 200 iterations while GRPO plateaus.

### Comparison to multi-answer and goal-conditioned baselines

| Baseline | Why it fails |
|---|---|
| Multi-RLVR (multi-answer, fixed scalarization) | Reward-space diversity collapses in training (verified 3/4 domains) |
| Goal-conditioned GRPO (text-encoded weight vector) | Mode-collapses — model ignores conditioning; best@k stalls (best@3 == best@6 on Maze) |
| GDPO (per-dimension advantage normalisation) | Underperforms VPO at matched compute |
| GRPO with 3× rollout budget | VPO(n=8) > GRPO(n=24) on MuSiQue best@3 |

## Empirical results (Tables 1–4)

| Domain | Model | Metric | VPO | Best scalar baseline |
|---|---|---|---|---|
| Maze | Qwen3-4B | best@30 | **0.593** | GRPO 0.432 |
| Maze | Qwen3-4B | diversity | **1.006** | GRPO 0.003 |
| MuSiQue | Qwen3-1.7B | best@30 | **0.832** | GRPO 0.728 |
| MuSiQue | Qwen3-1.7B | F1@30 | **0.678** | GRPO 0.447 |
| LiveCodeBench | Qwen2.5-Coder-7B | best@k (k>1) | **better** | GRPO better at pass@1 |
| OpenEvolve (32 hardest LCB) | Qwen2.5-Coder-7B | discovery rate | **continues rising** | GRPO plateaus at 0 |

## Relevance to this wiki

**Component P4 (Principle decomposition / vector reward) in [[../synthesis/proposed-method]]:** P4 lists the vector reward as "optional" with a fixed weighted sum. VPO is the empirical existence proof that training with a vector reward under RL is beneficial — but requires non-collinear sub-criteria. It supplies both the concrete objective ($R(S) = \mathbb{E}_w[\max_{y \in S} w^\top r]$) and the critical guard condition ($\bar\rho < {\sim}0.8$). See [[../synthesis/parked-ideas]] P3 for the experiment-proposal flag.

**Tension with pass@1 regime:** Our proposed-method targets concept installation measured by single-shot correctness. VPO explicitly degrades pass@1. If the evaluation regime is pass@1 (not search-augmented), VPO's stochastic scalarization should not replace the fixed P4 objective. P3 defers this decision to an empirical check.

**Relation to diversity collapse findings:** VPO's motivation is the same collapse documented in [[../rlvr-mechanics/binary-rewards-rl-challenges]] (I-projection mode collapse) and [[component G|../synthesis/proposed-method]] (entropy bonus for diversity preservation). It is the training-objective complement to the inference-time diversity techniques.

**Goal-conditioned failure warning:** VPO shows that conditioning the model on a text-encoded weight vector fails — the model ignores it. This is a caution for any design that relies on explicit principle-axis conditioning (a pattern that could appear in P4 or in [[../self-play/spag]]-style instruction conditioning).

## Limitations and scope

1. Validated on large training corpora (thousands of prompts, $G=8$, $m=3$ answers/rollout). Requires $G > 1$ to compute a meaningful advantage — not applicable at $G=1$.
2. Pass@1 degrades by design. Not a default choice for evaluation regimes where single-shot correctness dominates.
3. Non-collinearity is a necessary condition, not guaranteed. Must be checked on-policy with the $\bar\rho$ diagnostic.
4. Multi-hop QA (MuSiQue), logic (EUREQA), tool-use (ToolRL), and coding (LCB) settings only. No SFT or instillation-of-new-knowledge setting.

## Related
- [[_overview]] — post-GRPO RL-optimizer family
- [[../rlvr-mechanics/deepseekmath-grpo]] — base GRPO that VPO replaces the advantage estimator of
- [[dapo]] — companion post-GRPO variant (dynamic sampling, token-level PG loss)
- [[dr-grpo]] — removes length/std biases; orthogonal to VPO's scalarization change
- [[gspo]] — sequence-level ratio; orthogonal axis
- [[ep-grpo]] — post-GRPO credit-assignment fix; observational, single-answer; complement to VPO's set-level diversity
- [[../rlvr-mechanics/binary-rewards-rl-challenges]] — formal account of mode collapse VPO addresses
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — empirical diversity collapse post-saturation (same failure mode, different setting)
- [[../self-play/_overview]] — multi-answer chain is structurally related to diversity-injection in SPICE/SPIRAL
- [[../synthesis/proposed-method]] — component P4 (vector reward); VPO is the concrete objective recipe
- [[../synthesis/parked-ideas]] — P3: experiment-proposal flag for applying VPO to P4
