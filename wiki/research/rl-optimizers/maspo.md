---
name: maspo
description: Unified three-axis GRPO-family objective (Gradient Utilization, Probability Mass, Signal Reliability) via soft Gaussian gating with mass-adaptive variance and asymmetric reward-SNR control; subsumes Clip Higher / DAPO, DAC, and advantage reweighting as single-axis special cases.
type: research
---

# MASPO: Unifying Gradient Utilization, Probability Mass, and Signal Reliability

arXiv:2602.17550. MASPO is a **new objective** — not merely a taxonomic framework — that jointly addresses three orthogonal failure modes of GRPO's hard-clip trust region. The central argument: GRPO's binary clip $F(\rho) = \mathbf{1}[|\rho - 1| \le \varepsilon]$ conflates three distinct problems (wasteful gradient utilisation, probability-mass blindness, reward-SNR asymmetry) and each prior variant (DAPO, DAC, BAPO) corrects exactly one. MASPO derives a single gating function from a MaxEnt relaxation of an L2 mass-displacement constraint and encodes all three corrections in a dual-variable adaptive variance. The result is a strictly more general objective under which the single-axis predecessors are recoverable as special cases. Validated on DeepSeek-R1-Distill-Qwen 1.5B / 7B / 14B with +2.8–3.7% Avg@32 over GRPO across AIME/MATH500.

## Method

### Three Axes

| Axis | Problem with GRPO clip | Prior partial fix | MASPO mechanism |
|---|---|---|---|
| **Gradient Utilization** | Binary gate discards all gradient when $\|\rho-1\| > \varepsilon$, wasting off-policy data | Clip Higher / DAPO: raise $\varepsilon_\text{high}$ for $\hat{A} > 0$ | Soft Gaussian gate — non-zero gradient everywhere, decaying smoothly |
| **Probability Mass** | Same $\varepsilon$ for all tokens regardless of $\pi_{\theta_\text{old}}$; rare tokens need wider trust region | DAC / DCPO: scale clip bound by $\pi_{\theta_\text{old}}$ | Mass-adaptive variance $\sigma \propto \pi_{\theta_\text{old}}^{-\alpha}$ |
| **Signal Reliability** | Symmetric constraint treats positive (verified) and negative (noisy credit-assignment) advantages identically | BAPO / Advantage Reweighting: down-weight uncertain negative advantages | Asymmetric variance: $\sigma_+$ expanded for high-confidence exploitation, $\sigma_-$ compressed to guard near-miss reasoning chains |

### Soft Gaussian Gating

Replace the binary clip with a unilateral Gaussian weight on the IS ratio $\rho_{i,t} = \pi_\theta / \pi_{\theta_\text{old}}$:

$$F(\rho_{i,t}) = \exp\!\left(-\frac{(\rho_{i,t} - 1)^2}{2\sigma^2}\right)$$

Applied only when $\hat{A}_i > 0, \rho > 1$ or $\hat{A}_i < 0, \rho < 1$ — the exploiting quadrants. When the ratio moves against the advantage sign, the standard $\min$ clipping still applies (unilateral design). The bilateral counterpart (SAPO) gates both directions and empirically collapses — MASPO's ablations confirm the unilateral choice is load-bearing.

The Gaussian kernel is derived in Appendix A via MaxEnt relaxation: minimise the KL-from-uniform subject to an L2 mass-displacement constraint $\mathbb{E}[(\rho - 1)^2] \le \delta$. This yields the Gaussian form and proves that the constraint tightness $\sigma$ must scale inversely with $\pi_{\theta_\text{old}}$ to hold the same mass-displacement bound across tokens:

$$\sigma \propto \pi_{\theta_\text{old}}^{-\alpha}, \quad \alpha \in [0.3, 0.5]$$

### Dual-Variable Adaptive Variance (JMASPO)

The combined objective uses separate variances for positive and negative advantages:

$$\sigma_+ = \sigma_\text{base} \cdot (1 + \beta_\text{high} \cdot \hat{A})$$
$$\sigma_- = \frac{\sigma_\text{base}}{1 - \beta_\text{low} \cdot \hat{A}}$$

$\sigma_+$ widens when $\hat{A}$ is large (high-confidence signal — exploit aggressively). $\sigma_-$ compresses when $|\hat{A}|$ is large and negative. Appendix B proves that GRPO group-relative advantages monotonically track query difficulty: large $|\hat{A}|$ identifies easy queries where near-misses have mostly correct intermediate steps. Compressing $\sigma_-$ for those tokens prevents destroying reusable reasoning chains (the "catastrophic unlearning" argument).

Paper simplifies to three hyperparameters: $\sigma_\text{base} = 1$, $\beta_\text{low} = \beta_\text{high} = \beta$; recommends $\alpha = 0.3\text{–}0.5$, $\beta = 0.03$.

### Subsumption vs. Orthogonality

MASPO **subsumes** the exploration-axis fix (Clip Higher / DAPO $\varepsilon_\text{high}$ relaxation) and the signal-reliability fix (BAPO / advantage reweighting) as special cases recoverable with degenerate variance settings. It **subsumes** the mass-axis fix (DAC) structurally, though DAC's ratio-bound formulation expresses the same $\pi_{\theta_\text{old}}$ scaling differently — MASPO does not provide an explicit parameter-matching reduction to DAC, and DAC is competitive on 1.5B (see Conflicts below). MASPO is **orthogonal** to GSPO: GSPO replaces token-level IS ratios with sequence-level ratios and operates on a different granularity entirely; MASPO retains token-level IS ratios and improves the constraint shape. MASPO is also orthogonal to Dr. GRPO's std-normalisation fix, which it does not address.

## Claims

- **AIME / MATH500 (Table 2):** +3.0% Avg@32 and +2.8% Pass@32 over GRPO on 1.5B; +2.9% / +2.6% on 7B; +2.8% / +3.7% on 14B. All trained on DAPO-Math-17K, 16 off-policy updates per IS step (batch 512, mini-batch 32).
- **Training dynamics:** Higher entropy throughout training relative to all baselines — no premature exploitation collapse. Faster convergence (fewer gradient steps to the same accuracy).
- **Scaling:** Consistent gains at 1.5B, 7B, 14B. Behaviour at 70B+ and MoE architectures untested.
- **Constraint:** Requires verifiable binary rewards. The asymmetric risk controller assumes positive advantages correspond to verified correct outputs and negative to ambiguous near-misses. The assumption breaks for subjective or partial reward domains.

## Conflicts raised

**vs. Dr. GRPO.** Dr. GRPO identifies std-normalisation collapse (all-correct or all-wrong groups yield $\sigma_r = 0$, dividing by zero) as a critical failure mode. MASPO inherits GRPO's unnormalised group-relative advantage $\hat{A} = (r - \mu_r)/\sigma_r$ unchanged and neither acknowledges nor fixes this. In single-sample or small-group settings (this project's core scope), MASPO carries the same degenerate-group instability as raw GRPO.

**vs. SAPO.** MASPO claims SAPO's bilateral Gaussian gating causes training collapse and shows this empirically. SAPO's paper frames bilateral gating as a principled improvement. The unilateral choice is MASPO's ablation-supported departure from SAPO, but the literature does not yet reconcile these positions.

**vs. GSPO.** GSPO argues token-level IS ratios are fundamentally misaligned (a single draw cannot correct a distributional mismatch) and sequence-level KL is the correct metric. MASPO retains token-level IS ratios and improves only the constraint shape. These are competing diagnoses of why GRPO is unstable — not yet resolved.

**vs. DAC subsumption.** DAC addresses probability-mass sensitivity using a ratio-bound function of $\pi_{\theta_\text{old}}$ that is arguably equivalent to MASPO's mass-adaptive limiter expressed differently. MASPO claims strict superiority but DAC is competitive on 1.5B and the paper provides no ablation establishing parameter-matching equivalence.

## Relevance to the project

MASPO's three-axis taxonomy is the most systematic available frame for asking which GRPO variant best suits single-sample training. The three axes directly map to problems that worsen at low data: gradient waste is proportionally more costly when rollouts are expensive; probability-mass blindness is worse when token distributions are narrow (single-concept inputs); and reward-SNR asymmetry is harder to control without group averaging.

The asymmetric risk controller's $\sigma_-$ compression — designed to protect intermediate reasoning chains from erasure by large negative advantage updates — is a direct mechanism for concept preservation under RL updates, central to the single-sample learning hypothesis.

Critical caveat: MASPO does not fix the degenerate-group normalisation problem that Dr. GRPO targets. Any single-sample deployment of MASPO must either patch in Dr. GRPO's std fix or accept that all-correct groups will produce NaN / zero-gradient updates. This parallels the unified gradient view in [[../rlvr-mechanics/deepseekmath-grpo]] Sec 5, which traces all GRPO-family failure modes back to the group-normalisation design.

## Source

- arXiv: https://arxiv.org/abs/2602.17550
- Raw: `../../../raw/research/weekly-2026-04-23/04-maspo-unifying-sample-efficient.md`

## Related

- [[_overview]]
- [[dapo]] — MASPO subsumes Clip Higher (DAPO's $\varepsilon_\text{high}$ decoupling) as the exploration-only partial fix; DAPO-Math-17K is the shared training dataset
- [[dr-grpo]] — fixes std-normalisation collapse that MASPO inherits; necessary companion fix for single-sample or small-group use
- [[gspo]] — competing diagnosis (token-level IS ratios are the root problem vs. MASPO's constraint-shape diagnosis); orthogonal level of granularity
- [[ppo]] — ancestor; MASPO departs from PPO/TRPO KL framing by switching to L2 mass-displacement constraint
- [[../rlvr-mechanics/deepseekmath-grpo]] — GRPO direct baseline; MASPO Sec 3 derives binary gating as special case $F(\rho) = \mathbf{1}[|\rho-1| \le \varepsilon]$; unified gradient view in Sec 5
- [[../rlvr-mechanics/_overview]]
- [[../rlvr-mechanics/learning-to-think]]
- [[../single-sample-rl-finetuning/1-shot-rlvr]]
- [[../single-sample-rl-finetuning/data-efficiency-rft]]
- [[../synthesis/single-sample-concept-skeleton]] — $\sigma_-$ compression as concept-preservation mechanism under RL updates
- [[../synthesis/proposed-method]]
- [[../../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep
