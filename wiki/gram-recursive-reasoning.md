# GRAM (Generative Recursive Reasoning Models)

Authors from KAIST, Mila/Yoshua Bengio's group, and NYU (arXiv:2605.19376) extend deterministic Recursive Reasoning Models (HRM, TRM, Looped Transformers) by replacing each deterministic latent-state update with a stochastic residual perturbation trained via ELBO/amortized variational inference — enabling multi-trajectory probabilistic reasoning (N parallel trajectories selected by majority vote or a Latent Process Reward Model) and unconditional generation from the same architecture. Headline result: 97.0% on Sudoku-Extreme vs. TRM 87.4% / HRM 61.3%; 66.7% on ARC-AGI-1 vs. TRM 55.7% / HRM 52.0%.

## Method

GRAM wraps any deterministic RRM with a stochastic latent-state transition. At each outer step, the model computes a deterministic proposal `u_t` from the prior state, samples `ε_t ~ N(μ_θ(u_t), σ²_θ(u_t)·I)`, and sets `z_t = u_t + ε_t`. Stochasticity is applied only to the **high-level** (`h`) component of a hierarchical two-scale `(h, l)` state; the low-level (`l`) component is refined deterministically K times per transition (fast/slow decomposition).

Training: ELBO with a posterior `q_ϕ(τ|x,y)` (target-conditioned) and prior `p_θ(τ|x)`; deep supervision at each of N_sup outer steps; truncated BPTT within each step. Unconditional generation `p_θ(x)` replaces the input with an empty conditioning embedding — same recurrent process, no architectural change.

Inference-time scaling: N parallel trajectories sampled from the prior, selected via majority voting or a **Latent Process Reward Model (LPRM)** — a value head trained on final-accuracy regression targets. Authors frame this width-based scaling as complementary to (and lower-latency than) depth-based sequential scaling.

## Results

| Benchmark | GRAM | TRM | HRM |
|---|---|---|---|
| Sudoku-Extreme | **97.0%** | 87.4% | 61.3% |
| ARC-AGI-1 | **66.7%** | 55.7% | 52.0% |
| ARC-AGI-2 | **16.0%** | 11.1% | 9.7% |

- **N-Queens 8×8** (20 samples, 10M params): GRAM 99.7% acc / 90.3% coverage vs. AR 96.3% / 84.8%, TRM 66.8% / 36.1%, HRM 78.7% / 26.7%.
- **Graph Coloring 8-vertex**: GRAM 2.7 conflict edges / 85.8% coverage vs. AR 19.0 / 83.0%, MDLM 2.7 / 84.5%.
- **Unconditional Sudoku**: 99.05% valid boards (10.9M params, 16 steps) vs. D3PM 55.1% valid (55.1M params, 1000 steps).
- **Binarized MNIST**: GRAM IS 2.04 / FID 73.34 (256 steps) vs. D3PM IS 1.86 / FID 74.03 (1000 steps); TRM collapses at FID 303.29.
- **Compute efficiency**: GRAM N=20 / 16 iterations (97.0%) outperforms TRM at 320 iterations (90.5%) on Sudoku-Extreme at comparable compute.
- **Ablation** (Sudoku): stochastic guidance alone on Looped TF → 65.64 (from 61.25); + deep supervision → 73.90; full GRAM → 93.96. Both stochasticity and learned guidance are necessary — removing either causes significant degradation.

## Novelty

Prior stochastic recurrent models (VRNN, STORN, DKF, DreamerV2/V3) apply stochastic dynamics to sequential observation modeling; GRAM reinterprets the same stochastic state-space formulation as **computation** rather than temporal data. The specific contribution: learned Gaussian residual noise injected into the high-level component of HRM/TRM-style hierarchical recursive Transformers, trained with ELBO, unifying conditional reasoning and unconditional generation in one compact model. LPRM for trajectory selection is a secondary novelty.

## Applicability and Caveats

Drop-in extension for any deterministic RRM (Looped TF, HRM, TRM) on constraint-satisfaction or structured reasoning tasks. Compact scale (~7–27M params in all experiments) — not evaluated at LLM pretraining scale. Sequential deep supervision is a noted training-efficiency bottleneck. Width-based inference scaling requires proportional inference compute.

## Reproducibility

Project website: https://ahn-ml.github.io/gram-website/. Preprint only; no code repository or released weights confirmed. All baselines (HRM, TRM, Looped TF) reproduced from scratch by authors under identical settings. Not yet on paperswithcode leaderboards.

## Source

`raw/research/weekly-2026-05-25/03-gram-recursive-reasoning.md` (arXiv:2605.19376)

## Related

- [[hyperloop-transformers]] — Looped Transformers are one of GRAM's deterministic baselines; stochastic guidance is a drop-in extension to the looped architecture.
- [[hrm-text]] — Sibling deterministic RRM (HRM) surfaced the same week; GRAM's stochastic layer sits on top of HRM-style hierarchical recursion.
- [[latent-grpo]] — Parallel latent-reasoning-without-explicit-tokens line; LATENT-GRPO uses RL post-training on LLM continuous tokens, GRAM uses variational inference on purpose-built small RRMs.
- [[nested-learning]] — Multi-scale fast/slow state decomposition parallel; GRAM's `(h, l)` hierarchy decouples timescales in the same spirit.
