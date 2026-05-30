# DelTA

**Discriminative Token credit Assignment for Reinforcement Learning from Verifiable Rewards** — Zhang et al., Renmin University / Ant International; arXiv:2605.21467. DelTA reframes GRPO/DAPO-style RLVR policy-gradient updates as an implicit linear discriminator over token-gradient vectors: standard sequence-level objectives form positive/negative side-wise centroids by advantage-weighted averaging of token gradients, but shared high-frequency tokens (formatting, problem entities) dominate both centroids and dilute the directions that actually separate higher- from lower-reward responses. Fix: one iteration of entropy-regularized centroid refinement yields discriminative-contrast coefficients λ ∈ [0.8, 1.2] per token; these replace the uniform token average in the DAPO surrogate with a self-normalized λ-weighted loss. On 7 hard-math benchmarks (AIME24/25/26, HMMT25-Feb/Nov, HMMT26-Feb, Brumo25), DelTA beats the strongest baseline by +3.26 pp (Qwen3-8B-Base, avg 28.40 vs. SAPO 25.14) and +2.62 pp (Qwen3-14B-Base, avg 39.91 vs. FIPO 37.29).

## Method

**Discriminator view of RLVR.** A grouped-rollout RLVR objective can be read as forming two token-gradient centroids — one averaged over positive-advantage tokens, one over negative — and pushing the policy to separate them. Shared/formatting tokens have high-magnitude gradients that collapse both centroids toward a common background subspace, shrinking the discriminative margin.

**λ discriminative-contrast coefficients.** For each token, compute a score from the distance margin of its token-gradient vector to the opposite-side centroid vs. its own-side centroid (closed-form sigmoid, Eq. 6). Run K=1 step of entropy-regularized centroid refinement on those scores. Map final scores to λ ∈ [0.8, 1.2]. Coefficients are stop-gradient and computed from an LM-head-restricted gradient proxy (not full-parameter gradients) for tractability.

**Surrogate reweighting.** Replace the uniform per-token average in the DAPO surrogate with a self-normalized λ-weighted sum (Eq. 8). The discriminator framing generalises to any advantage-weighted sequence-level RLVR objective (Appendix E).

## Results

Training: DeepMath-103K, VeRL; Qwen3-8B-Base and Qwen3-14B-Base; max 30k tokens, 16 samples/problem.

- **8B:** avg 28.40 vs. SAPO 25.14 (+3.26 pp); beats DAPO (+5.45 pp), DAPO+FT (+3.60 pp), FIPO (+4.51 pp).
- **14B:** avg 39.91 vs. FIPO 37.29 (+2.62 pp).
- **Ablation (Table 2):** opposite-side comparison is load-bearing; within-side-only variant (21.67 avg on 4-bench subset) underperforms plain DAPO (23.33) — centroid *contrast* is what matters, not centroid magnitude alone.
- **Token-selection experiment (Figs 3–4, Sec 5.2):** top-50% λ tokens outperform full-token DAPO; bottom-50% λ tokens actively collapse training. Low-λ tokens are not merely uninformative — they are harmful to the update direction.
- **Training dynamics (Fig 2):** DAPO plateaus and degrades (shorter responses, rising entropy); DelTA sustains longer responses, lower entropy, rising reward.

Validated on OLMo3-7B as well; backbone-agnostic.

## Applicability

Any RLVR loop with DAPO/GRPO-class objectives and grouped rollouts. Requirements: token-gradient access (or LM-head proxy), positive/negative rollout groups, moderate per-batch overhead (Appendix L.1). No external reward models or value functions. Applicable to math and code at 8B–14B scale on standard VeRL/similar infrastructure.

## Novelty

The discriminator framing of the RLVR gradient update is new as an analysis lens. The reweighting algorithm is a refinement of DAPO, not a new training paradigm. Closest prior: FIPO (Ma et al., 2026) uses future-KL-influenced token selection; Forking Tokens (Wang et al., 2025) uses entropy-based selection. DelTA derives weights from positive-negative gradient-space contrast (centroid geometry), not entropy or future influence. No direct prior for the LDA-centroid-contrast view.

## Reproducibility

Code: https://github.com/RUCBM/DelTA. Hyperparameters in Appendix I. No independent reproduction as of 2026-05-25 (preprint captured same day). HF Daily Papers featured this week.

## Source

- `raw/research/weekly-2026-05-25/05-delta-token-credit.md` (arXiv:2605.21467)

## Related

- [[token-gradient-cancellation]] — DelTA's "shared tokens dominate both centroids" analysis is a discriminator-space restatement of the gradient-cancellation pathology; fixes are complementary (DFPO orthogonalises in parameter space; DelTA reweights the surrogate).
- [[reasonmaxxer]] — Both find RL meaningfully touches only a sparse token subset; DelTA's λ coefficients give a mechanistic account of *which* tokens those are (high discriminative contrast, not merely high entropy).
- [[anti-self-distillation]] — sibling per-token RL-credit paper surfaced the same week; parallel problem framing.
- [[neural-garbage-collection]] — both connect token-level selection to RLVR update quality; orthogonal mechanisms (KV eviction vs. credit reweighting).
- [[agentflow]] — uses DAPO/Flow-GRPO surrogate; DelTA's λ reweighting could layer on top of any DAPO-class objective.
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — DelTA is a third mechanistic frame (LDA centroid contrast) in this open conflict: consistent with sparse-token sparsity while offering an independent account of the gradient-cancellation pathology.
