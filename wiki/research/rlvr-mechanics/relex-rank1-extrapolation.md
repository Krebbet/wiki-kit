# RELEX: Rank-1 Trajectory Extrapolation for RLVR

RELEX (arXiv:2605.21468) establishes two geometric regularities of RLVR weight-update trajectories — near-rank-1 structure and near-linear scalar dynamics — and exploits them to reconstruct full-training checkpoints from as little as 15% of training via a closed-form SVD plus linear regression procedure, matching or exceeding full RLVR on in-domain MATH and OOD reasoning benchmarks across Qwen2.5-Math-1.5B, Qwen3-4B-Base, and Qwen3-8B-Base.

## Core Findings

**Finding 1 — Rank-1 structure.** For each weight tensor $W^{(\ell)}$, define the parameter delta $\Delta\theta_t^{(\ell)} = W_t^{(\ell)} - W_0^{(\ell)}$ and stack flattened deltas into a trajectory matrix:

$$M^{(\ell)} = [\,\Delta\theta_1^{(\ell)}\;|\;\cdots\;|\;\Delta\theta_T^{(\ell)}\,]^\top \in \mathbb{R}^{T \times d}, \quad M^{(\ell)} = U\Sigma V^\top$$

A rank-1 reconstruction $\hat{M}_1^{(\ell)} = \sigma_1 u_1 v_1^\top$ preserves nearly all of the downstream accuracy gain over the base model. The leading right singular vector $v_1^{(\ell)}$ defines a stable subspace throughout training, and the rank-1 component accounts for 81.4% of rank-5 subspace variance. Components 2–5 are lower-variance, less monotonic, and noisy — projecting onto $v_1^{(\ell)}$ acts as a denoising step, discarding stochastic optimization variance.

**Finding 2 — Linear dynamics.** The scalar projection coefficient

$$c_t^{(\ell)} = \langle \Delta\theta_t^{(\ell)},\, v_1^{(\ell)} \rangle$$

evolves near-linearly with training step $t$, with $R^2 > 0.98$ across most tensors.

## RELEX Algorithm

Three steps, no learned components:

1. **Subspace estimation.** Observe $T_\text{cut}$ RLVR checkpoints (15–20% of full training budget). For each tensor $\ell$, apply truncated SVD to the delta matrix and extract $v_1^{(\ell)}$.

2. **Coefficient extrapolation.** Project observed deltas onto $v_1^{(\ell)}$ to get $\{c_t^{(\ell)}\}_{t=1}^{T_\text{cut}}$. Fit by least squares:

$$a^{(\ell)} = \frac{\text{Cov}(t,\, c_t^{(\ell)})}{\text{Var}(t)}, \quad b^{(\ell)} = \bar{c}^{(\ell)} - a^{(\ell)}\bar{t}$$

Predict at target step $T$: $\hat{c}_T^{(\ell)} = a^{(\ell)} T + b^{(\ell)}$.

3. **Weight reconstruction.** Reconstruct the extrapolated checkpoint:

$$\hat{W}_T^{(\ell)} = W_0^{(\ell)} + \hat{c}_T^{(\ell)} \cdot v_1^{(\ell)}$$

Overhead is one truncated SVD per tensor plus a two-scalar linear fit — negligible relative to training.

## Experimental Results

Main results (MATH accuracy and OOD average; OOD = AIME25, AIME26, HMMT25, AMC23):

| Model | Method | Cost | MATH | OOD Avg |
|---|---|---|---|---|
| Qwen2.5-Math-1.5B | Full RLVR | 100% | 71.5 | 28.4 |
| Qwen2.5-Math-1.5B | RELEX | 15% | 71.6 | 30.0 |
| Qwen2.5-Math-1.5B | Weight Extrap. | 15% | 70.4 | — |
| Qwen2.5-Math-1.5B | ExPO | 15% | 67.7 | — |
| Qwen2.5-Math-1.5B | AlphaRL | 15% | 67.3 | — |
| Qwen3-4B-Base | Full RLVR | 100% | 85.5 | 42.3 |
| Qwen3-4B-Base | RELEX | 15% | 85.6 | 43.0 |
| Qwen3-8B-Base | Full RLVR | 100% | 88.5 | 47.1 |
| Qwen3-8B-Base | RELEX | 20% | 87.4 | 46.2 |

RELEX matches or outperforms full RLVR on the 1.5B and 4B models; the 8B falls marginally short on in-domain MATH (87.4 vs 88.5) but is within noise on OOD. Optimal $T_\text{cut}$ is model-dependent: 1.5B prefers larger windows; Qwen3-4B-Base benefits from $T_\text{cut}=75$; Qwen3-8B-Base from $T_\text{cut} \in \{100,125\}$.

**Long-horizon extrapolation** (from $T_\text{cut}=125$, predicting up to $10\text{–}20\times$ beyond the observation window) is stable for the 1.5B model (MATH 71.6–71.7 at steps 500–1000) but shows mild degradation for Qwen3-8B-Base at step 1000 (88.0 → 85.6), consistent with accumulated linear extrapolation error.

## Ablations

Ablations on Qwen2.5-Math-1.5B at $T_\text{cut}=75$:

| Variant | Step 200 | Step 500 |
|---|---|---|
| SVD rank-1 (ours) | 70.0 | 71.6 |
| Raw delta (no SVD) | 68.5 | 70.7 |
| Rank-5 subspace | 68.4 | 70.6 |
| Rank-10 subspace | 68.8 | 70.5 |
| Linear fit (ours) | 70.0 | 71.6 |
| Polynomial fit | 17.8 | 0.1 |
| Neural network fit | 69.5 | 72.1 |

Increasing rank degrades performance — the extra components add noise rather than signal. Polynomial fitting catastrophically fails (near-zero accuracy), demonstrating that simplicity is load-bearing. Neural network fit slightly edges linear at step 500 but with no principled stopping criterion and at greater risk of overfitting the short observation window.

## Weight-Space Geometry

Appendix B of the paper measures direction similarity (cosine) and magnitude ratio between RELEX-reconstructed and true RLVR checkpoints:

- **Reconstruction mode** ($T_\text{cut}=500$, predicting within window): direction similarity 0.50→0.91, magnitude ratio ≈1.0 — near-perfect alignment.
- **Extrapolation mode** ($T_\text{cut}=75$, predicting step 500): direction similarity drops (0.72→0.35), magnitude ratio inflates (1.26→2.70) — geometrically divergent from true training-path checkpoints, yet competitive on task performance. This suggests the extrapolated direction captures transferable reasoning structure rather than distribution memorization.

The inflated magnitude ratio (up to 2.70×) is a potential risk factor for downstream fine-tuning or further RL.

## Relevance to the Single-Sample Thesis

RELEX is direct evidence that RLVR operates in an extremely low-dimensional subspace of parameter space. A rank-1 geometry implies that meaningful capability gains consume far fewer effective degrees of freedom than parameter count, which is an enabling prior for per-concept single-sample adaptation: if each concept lives in a near-rank-1 subspace, cross-concept interference is structurally suppressed. The finding that the relevant subspace is identifiable from very short training exposure mirrors the single-sample regime's requirement to extract signal from minimal data.

## Limitations

1. Evaluated only on mathematical reasoning with GRPO + Qwen family; generalization to PPO, code generation, Llama, or Mistral is unverified.
2. $T_\text{cut}$ selection is purely empirical; no principled criterion exists without holdout validation.
3. Linear dynamics break down for larger models beyond $\sim 8\times$ the observation window.
4. The denoising / "transferable reasoning" interpretation is descriptive, not formally proven.
5. Rank-1 structure may be specific to homogeneous math training distributions; untested on diverse multi-task corpora.

## Source

- arXiv:2605.21468 — *You Only Need Minimal RLVR Training: Extrapolating LLMs via Rank-1 Trajectories*

## Related

- [[_overview]] — RLVR mechanics overview; rank-1 trajectory structure is a core geometric finding
- [[rl-sparse-subnetwork]] — complementary empirical evidence that RLVR updates are sparse/low-dimensional
- [[rethinking-rl-sparse-selection]] — related characterization of what RLVR modifies in weight space
- [[../../selective-finetuning/skill-localization]] — both identify that capability gains are localized in low-dimensional subspaces; rank-1 extrapolation and skill localization are complementary perspectives on the same phenomenon
- [[../../synthesis/fine-tuning-best-practices]] — practical implication: 15% training cost to match full RLVR is a strong efficiency result
- [[../../weekly-briefs/2026-07-03]] — brought in by the 2026-07-03 weekly sweep
