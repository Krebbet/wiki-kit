# Token Gradient Cancellation / DFPO: Design Conditions for Intra-Group Sequence-Level Rewards

Alibaba / Tsinghua (arXiv:2604.13088). Formal structural condition for stable GRPO-style RL: intra-group objectives must maintain **token-level gradient exchangeability** so reward-irrelevant template tokens cancel across trajectories. Proposes **DFPO** (Drift Fixing Policy Optimization) — two minimal stop-gradient weight transformations that restore cancellation. +5.6 / +6.9 / +5.6 pp avg@32 on AIME25 / LiveCodeBench v6 / HMMT25 over GSPO at Qwen3-32B; gain grows with group size.

## Method

Token-level credit assignment analysis of intra-group comparative RL objectives (GRPO, GSPO, variants).

**Core claim — Gradient exchangeability** (Eq. 2): stable training requires shared / weak-credit tokens to have **exchangeable per-trajectory effective weights** so their group-aggregate gradient cancels to zero. Two mechanisms break this:

1. **Sequence-coupled multiplicative weights** (GSPO-style product over all tokens) make non-cancellation the structural norm. Corollary 3.3 argues by measure-zero that exact cancellation is generic-impossible under sequence coupling.
2. **Asymmetric piecewise clipping** (GRPO's min/clip) breaks exchangeability even in token-factorized objectives.

**Fix — DFPO**: apply one of two **stop-gradient** intra-group weight transformations *before* computing gradients:

- **Min-Replace** (Eq. 17): replace all `w_i` with `min_group(w_i)`.
- **Adv-Orthogonal Reweighting** (Eq. 18): project `w` onto the subspace orthogonal to the advantage vector.

Stop-gradient is essential — without it the transformation re-couples the gradients. Drop-in: no architecture change, no rollout-protocol change. Derives from GRPO (Shao et al. 2024) and GSPO (Zheng et al. 2025).

## Results

Compute-matched (same total tokens, same optimizer steps), avg@32, 5 seeds; paired bootstrap p<0.01 (Table 1):

| Benchmark | Model | GRPO | GSPO | GRPO-fix | DFPO (Min-Replace) |
|---|---|---|---|---|---|
| AIME25 | Qwen3-32B | 76.9 | 76.9 | 80.6 | **82.5** |
| LiveCodeBench v6 | Qwen3-32B | 64.5 | 64.7 | 69.1 | **71.6** |
| HMMT25 | Qwen3-32B | 55.5 | 55.8 | 59.6 | **61.4** |
| AIME25 | Qwen3-Next-80B-A3B | — | 89.8 | — | **93.2** |

- Compute efficiency (Table 2): DFPO reaches the training-reward threshold at **0.91× the compute of GSPO**.
- **Group size ablation** (Table 4): relative gain over GSPO grows with G — +3.1 (G=2) → +5.7 (G=16) on AIME25 Qwen3-32B. Theory predicts this; observed.

## Novelty

Refinement / theoretical grounding of GRPO/GSPO practice, not a new paradigm. What's new: (1) unifies previously ad-hoc instability observations under a **single structural condition** (gradient exchangeability / cancellation); (2) formal proof (Prop. 3.1, KL drift bound) that non-cancellation is structurally inevitable under sequence coupling; (3) the corrective transforms are simpler than DAPO's token-level tricks or GSPO's full sequence-level redesign.

Position: complementary to [[eggroll]] (which replaces GRPO with ES) and [[rlsd-self-distilled-rlvr]] (which adds a teacher-weighting signal). DFPO **fixes** GRPO/GSPO rather than replacing.

## Reproducibility

Code release stated as anonymous via GitHub; no active link in captured PDF. Public Qwen3-32B / Qwen3-Next-80B-A3B-Thinking and public benchmarks (AIME25, LiveCodeBench, HMMT25). Hyperparameters in Appendices B, I, J.

## Source

- `raw/research/weekly-2026-04-27/04-token-gradient-cancellation.md` — arXiv:2604.13088.

## Related

- [[eggroll]] — both target GRPO instability at scale; EGGROLL **replaces** GRPO with ES, DFPO **fixes** GRPO structurally; contrasting strategies for the same failure mode.
- [[rlsd-self-distilled-rlvr]] — RLSD targets privileged-info leakage in self-distillation; DFPO targets gradient non-cancellation in group objectives. Complementary diagnoses on the same lineage.
- [[neural-garbage-collection]] — concurrent GRPO-line extension (action-space, KV cache); composable with DFPO at the trainer.
- [[watchlist]] — DAPO (Yu 2025), DCPO (Yang 2025), SSPO (Yang 2025), TEPO (2604.12736).
