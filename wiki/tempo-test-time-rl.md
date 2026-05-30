# TEMPO: Scaling Test-Time Training for Large Reasoning Models

Tianjin / Tongyi Lab / CUHK / Shanghai AI Lab (arXiv:2604.19295, 2026-04-26). Reframes test-time training for LRMs as Expectation-Maximization and shows that prior self-rewarding TTT methods (TTRL, EMPO) are incomplete EM variants — they run only the M-step and let the reward signal drift. TEMPO restores the missing E-step by periodically recalibrating a token-level value critic on labeled data; the actor then keeps refining on unlabeled test questions without diversity collapse. OLMO3-7B AIME 2024 33.0 → 51.1 avg@16; Qwen3-14B 42.3 → 65.8. Beats both TTRL and EMPO on every (model, benchmark) pair tested, and crucially **maintains pass@k** where TTRL/EMPO degrade it.

## Method

Actor-critic TTT formalized as EM on the joint distribution `p(y, correctness | x)`:

- **E-step (Critic Recalibration).** Every K iterations, freeze the actor and fine-tune the token-level value critic `V_ϕ(x, y_{1:t})` on a small labeled set `D_L` by minimizing MSE against binary correctness outcomes. This anchors the reward signal in verifiable external supervision so it can't co-evolve with the policy.
- **M-step (Policy Refinement).** Generate trajectories on *unlabeled* test questions `D_u`. Compute per-token advantages `A_t = R − V_ϕ(x, y_{1:t})` from the critic's intermediate value estimates. Update the actor with a clipped policy-gradient objective.

Both actor and critic are bootstrapped via standard RLVR (PPO on `D_L` using DAPO-Math-17K or Dolci-RL-Zero-General) before TTT begins. Base models tested: OLMO3-7B, Qwen3-8B, Qwen3-14B. Max response length 16K, batch 256 (≤8B) / 128 (14B).

The EM diagnosis is the load-bearing contribution. §5 formalizes TTRL's auxiliary distribution as `q(y|x) ∝ 𝟙(y ∈ Y_majority) · π_θ0(y|x)` — i.e. the critic is the *current* policy's majority vote — and shows this creates a positive-feedback loop that collapses to the policy's most-confident mode.

## Results

**Math (avg@16 / pass@8, Table 1):**

| Model | Benchmark | Zero-RL baseline | TEMPO | Δ avg@16 / pass@8 |
|---|---|---|---|---|
| OLMO3-7B | AIME 2024 | 33.0 / 56.1 | 51.1 / 61.6 | +18.1 / +5.5 |
| OLMO3-7B | AIME 2025 | 26.3 / 41.1 | 37.0 / 52.5 | +10.7 / +11.4 |
| Qwen3-8B | AIME 2024 | 26.3 / 53.0 | 42.7 / 61.1 | +16.4 / +8.1 |
| Qwen3-14B | AIME 2024 | 42.3 / 69.1 | 65.8 / 73.3 | +23.5 / +4.2 |

TEMPO climbs steadily over **350 training steps** without plateau (Figure 4); TTRL/EMPO plateau ~100 steps and *lose* pass@k from there.

**General reasoning (Table 2, OLMO3-7B):** BBH 46.8 → 68.2; AGI Eval 37.9 → 62.4; ZebraLogic 22.2 → 35.1; GPQA-Diamond avg@8 21.9 → 32.4.

**Ablation (Figures 5/6):** Frozen-critic variant plateaus ~100 steps. Continuing supervised PPO from a converged checkpoint yields negligible gain — the unlabeled-test-distribution shift is doing real work, not just extra compute.

## Why this matters

TEMPO sharpens the framing in [[test-time-training]]: TTT methods that close the loop with self-generated rewards (TTRL, EMPO, Theta-Evolve) are doing M-step-only EM and **necessarily** drift unless the reward signal is re-anchored. The fix is structural — token-level critic recalibration on a small labeled set — and is independent of architecture (in contrast to [[in-place-ttt]] which modifies the gated-MLP host). Together TEMPO + In-Place TTT bracket the design space: TEMPO modifies the *training procedure*, In-Place TTT modifies the *architecture*; both target the same drift problem.

Where this leaves [[ssm-tool-use-length-generalization]]'s argument that interactive tool-use is a more tractable escape than richer state: TEMPO is in a third category — not richer state, not external memory, but a calibrated reward signal so the policy can keep learning on the test distribution.

## Reproducibility

- Code: https://github.com/QingyangZhang/TEMPO
- Weights: https://huggingface.co/collections/qingyangzhang/tempo
- Project page: https://qingyangzhang.github.io/tempo-homepage
- Preprint, no independent reproduction at capture date.

## Source

- `raw/research/weekly-2026-05-04/01-tempo-test-time-rl.md` — arXiv:2604.19295.

## Related

- [[test-time-training]] — TEMPO is the actor-critic-EM entry in the cluster; the existing TTRL/EMPO entries should be read with the EM-incompleteness framing.
- [[in-place-ttt]] — parallel TTT on unlabeled inference data; In-Place TTT modifies architecture, TEMPO modifies the training procedure.
- [[eggroll]] — adjacent on the "post-RLVR-saturation" theme; EGGROLL uses ES because GRPO is infeasible at 14B+, TEMPO uses calibrated EM because self-rewarding TTT drifts.
- [[token-gradient-cancellation]], [[rlsd-self-distilled-rlvr]] — RL post-training stabilization line.
- [[conflicts/ttt-distinct-vs-parametric-icl]] — TEMPO trains on the unlabeled *test distribution* without any in-context examples, hardening the TTT-as-distinct-from-ICL position.
