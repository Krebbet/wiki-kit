# HRM: Hierarchical Reasoning Model

Wang et al. (arXiv:2506.21734) introduce HRM, a 27M-parameter recurrent architecture built around two interdependent modules operating at different timescales — a high-level (H) module for slow, abstract planning and a low-level (L) module for rapid, detailed computation. The H/L hierarchy is jointly trained end-to-end from 1000 task examples, without pretraining, without Chain-of-Thought supervision, and without explicit intermediate reasoning tokens. Target domain: symbolic and structured reasoning (Sudoku, maze path-finding, ARC). This is the foundational paper; [[hrm-text]] scales it to 1B parameters on language tasks; [[gram-recursive-reasoning]] extends it with ELBO-trained stochastic latent state.

## Method

HRM achieves computational depth through recurrence rather than layer stacking. Two modules are tightly coupled across recurrent steps: H provides planning context to L; L's outputs feed back into H. At each forward pass over a token or task step, the model executes multiple H/L cycles — depth is a function of recurrent iterations, not parameter count.

This is not generic weight-shared looping (as in Universal Transformers or [[hyperloop-transformers]]). The two-module hierarchy enforces a structured temporal abstraction: H operates on a slower abstraction timescale, L operates within each H cycle. The architecture is trained end-to-end with a single task-completion loss; no intermediate reasoning states are supervised or produced.

Total parameters: 27M. Operates in a single forward pass. No CoT data required. Training requires only 1000 samples per task.

## Results

Figures cross-referenced from [[gram-recursive-reasoning]], where HRM is the primary deterministic baseline:

| Benchmark | HRM | TRM | GRAM |
|---|---|---|---|
| Sudoku-Extreme | 61.3% | 87.4% | **97.0%** |
| ARC-AGI-1 | 52.0% | 55.7% | **66.7%** |
| ARC-AGI-2 | 9.7% | 11.1% | **16.0%** |
| N-Queens 8×8 acc / coverage | 78.7% / 26.7% | 66.8% / 36.1% | **99.7% / 90.3%** |

The abstract further claims near-perfect performance on complex Sudoku and optimal maze path-finding, and outperformance of much larger models on ARC — all at 27M parameters and 1000 training samples.

## Novelty

The core claim: a dual-timescale H/L recurrent hierarchy with 27M parameters and 1000 training examples achieves near-perfect performance on symbolic reasoning benchmarks where large CoT-prompted LLMs fail. The mechanism is H/L coupling at different temporal abstractions, not deeper stacking, not more data.

Distinguishing features:
- **No CoT tokens:** reasoning is fully internalized into recurrent depth; no intermediate outputs supervised or generated.
- **No pretraining:** trained from scratch on the target task distribution only.
- **Structured hierarchy:** H/L is a two-module design with explicit timescale separation, distinct from single-module looped architectures.
- **Extreme data efficiency:** 1000 training samples is the regime, not a floor.

Note: MagicNorm, TBPTT warmup curriculum, and PrefixLM training objectives are HRM-Text contributions — not part of the original HRM.

## Relationship to Extensions

**[[hrm-text]]** (arXiv:2605.20613, SapientInc) scales the same H/L dual-timescale design to 1B parameters on language tasks. Adds MagicNorm stabilization, TBPTT warmup from K=2 to K=5, and PrefixLM pretraining on instruction-response pairs only. The architecture is parameterized as H2L3 (2 outer H cycles × 3 inner L steps). Training cost: ~$1,472 on 16× H100s. Achieves MATH 56.2 / GSM8K 84.5 / ARC-C 81.9, beating dense models 2–7× its size at 96–432× the compute.

**[[gram-recursive-reasoning]]** (arXiv:2605.19376, KAIST/Mila/NYU) uses HRM as its primary deterministic baseline and extends it by replacing the deterministic H-module update with a stochastic residual: `z_t = u_t + ε_t` where `ε_t ~ N(μ_θ(u_t), σ²_θ(u_t)·I)`, trained via ELBO. GRAM supports N parallel reasoning trajectories selected by majority vote or a Latent Process Reward Model. GRAM outperforms HRM on all benchmarks (Sudoku-Extreme 97.0% vs 61.3%, ARC-AGI-1 66.7% vs 52.0%).

## Reproducibility

- **arXiv:** 2506.21734
- **Code:** not confirmed in abstract capture; may be in PDF
- **Venue:** preprint, submitted 2025-06-26, last revised 2025-08-04 (v3)
- **HF upvotes:** 54 (captured 2026-06-27)

## Source

`raw/research/weekly-2026-06-27/05-hrm.md` (arXiv:2506.21734)

## Related

- [[hrm-text]] — 1B-parameter language version of HRM; same dual-timescale H/L architecture extended to text pretraining with MagicNorm and TBPTT warmup; trains from scratch on instruction-response data only
- [[gram-recursive-reasoning]] — stochastic extension of HRM: replaces deterministic H-module update with ELBO-trained Gaussian residuals and supports N parallel trajectories; GRAM outperforms HRM on all benchmarks (Sudoku-Extreme 97.0% vs 61.3%, ARC-AGI-1 66.7% vs 52.0%)
- [[hyperloop-transformers]] — sibling looped-Transformer cluster; uses loop-level hyper-connections on a single middle block vs HRM's two-module H/L hierarchy; different recurrent mechanisms, same compute-via-depth class
- [[latent-grpo]] — parallel direction: both suppress explicit CoT tokens; HRM uses recurrent depth, latent-GRPO uses continuous latent RL post-training on existing LLMs
- [[nested-learning]] — multi-scale fast/slow computation parallel; shares hierarchical temporal abstraction intuition with HRM's H/L design
