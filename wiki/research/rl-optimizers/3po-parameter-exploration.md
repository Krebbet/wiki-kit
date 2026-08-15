---
name: 3po-parameter-exploration
description: Parameter-space exploration for RLVR — sample policy weights from an IVON variational posterior instead of/alongside temperature scaling; rescues more zero-advantage GRPO groups than action-space exploration baselines at near-identical FLOPs. Third position (prevention) in the mcpo-vs-dapo-mastered-prompts conflict.
type: research
---

# 3PO: Parameter-Space Exploration for RLVR via Variational Learning

Venkatkrishna, Daheim, Gurevych (INSAIT / UKP Darmstadt), arXiv:2608.09805. Introduces Perturbed Parameter Policy Optimization (3PO): instead of controlling RLVR exploration in action space (temperature scaling), sample the *policy weights themselves* from an IVON variational posterior each step. Temperature scaling only reweights the output distribution — it cannot reorder tokens (Fig. 1) — so it can widen or narrow variance but never surface trajectories the base ranking suppresses. Weight-space noise can. Three variants (B3PO/M3PO/C3PO) trade off cheaply between per-group rollout diversity and gradient-sample variance; the best variant (C3PO) beats GRPO and three action-space exploration baselines on math and code RLVR at near-identical FLOPs, and produces measurably fewer dead (zero-advantage) groups during training.

## Method

Weight perturbation via the IVON reparameterization (Shen et al., ICML 2024):

$$\hat\theta = m + \sigma \odot z,\quad z\sim\mathcal N(0,I),\qquad \sigma = \frac{1}{\sqrt{\lambda(h+\delta)}} \tag{Eq. 3–4}$$

with $h$ a diagonal-Hessian estimate and $\lambda$ an inverse-temperature / effective-sample-size hyperparameter controlling noise magnitude. This is one Monte-Carlo sample of the generalized variational objective (Eq. 2, an ELBO: expected loss under $q$ plus a $\lambda^{-1}$-scaled KL to a prior $p_0$).

Three variants (Fig. 2; Algorithms 1–2, Appendix K):

- **B3PO** — one perturbation $\hat\theta_b$ per gradient step, synced across all $G$ rollouts. Weight-space analogue of step-level temperature control.
- **M3PO** — $M$ independent perturbations per step, GRPO loss computed separately per perturbation (group size $G/M$ under equal compute), gradients averaged before one posterior update. Lower gradient-sample variance, less per-group diversity.
- **C3PO** — $N$ perturbations per step, $G/N$ rollouts each, but advantages computed over the *full pooled* group of $G$ responses rather than per-perturbation — directly targets GRPO group diversity. Requires **Seq-MIS** (sequence-level importance sampling + masking, ratio clipped to $[0.5, 2.0]$) to correct the training–inference mismatch from mixing rollouts of $N$ distinct policies; without it, training reward stays flat (Appendix I, Fig. 12 middle).

Reward is standard binary correctness; advantage is vanilla group-relative GRPO (Eq. 1, no KL term, following DAPO). On-policy, single gradient update per batch — no batch-online replay. Explicitly framed as compatible/orthogonal to Clip-Higher, entropy regularization, and advantage-shaping: stacking, not replacing.

## Claims

All 3PO variants beat GRPO and three action-space baselines (EntReg entropy bonus, Polaris temperature-on-entropy-collapse, KL-Cov) on average Pass@1 across six math benchmarks (AIME'24–26, MATH-500, AMC, Minerva) on Olmo-3-1025-7B and Qwen2.5-Math-7B, at near-identical FLOPs (Table 1, Table 3):

| Model | C3PO avg. Pass@1 | GRPO avg. Pass@1 | Δ |
|---|---|---|---|
| Olmo-3-1025-7B | 44.04 | 42.99 | +1.05 pp |
| Qwen2.5-Math-7B | 46.88 | 45.36 | +1.52 pp |

Gains concentrate on the hardest benchmarks (up to +4.17 pp Olmo3 AIME'26, +5.83 pp Qwen2.5-Math AIME) and are larger on code generation (LiveCodeBench-v6, Olmo3/CodeR1-12K) than math — the authors read this as parameter exploration mattering most where the pre-RL model is weakest (code SFT baseline 9.5% vs. math 35.02%). C3PO also reaches GRPO's final reward within 50% of the training steps. Multi-seed robustness (Appendix G): C3PO beats GRPO on all 3 seeds (+0.89 pp avg., paired-$t$ $p=0.027$; AIME'24 +1.8 pp, $p=0.023$).

**The zero-advantage-groups result (Fig. 3, Section 4.3):** using multiple parameter samples produces net-positive rescue of zero-advantage GRPO groups over training, while action-space methods (Polaris in particular) net-*lose* groups instead. "3PO's trajectories come from LLM policies that are likely under the posterior and which are less likely to generate invalid trajectories than the undirected exploration of action-space methods." Fig. 3 (middle/right) shows Polaris's high-temperature token reordering mostly buys *degenerate* rollouts, and EntReg's entropy bonus mostly buys *incorrect* rollouts, not useful diversity.

## Limitations (acknowledged)

- M3PO/C3PO run ≈1.5× wall-clock vs. GRPO despite near-identical FLOPs — a systems artifact (unfused IVON kernels, inefficient multi-model sampling in vLLM), not fundamental.
- $\lambda$ (noise magnitude) is sensitive and model-dependent: too low ($10^8$) collapses C3PO training entirely; optimum is $10^9$ for Olmo3, up to $10^{10}$ for the less-robust Qwen2.5-Math.
- B3PO's advantage over GRPO doesn't hold on average — high noise-sample variance and limited group diversity make it degenerate into malformed rollouts later in training (diminishing zero-advantage rescue over time, Fig. 3 left).
- A learned noise prior (loading the IVON Hessian from the SFT phase) gives negligible benefit — the SFT-phase Hessian stays nearly isotropic (<8% of values outside $[0.9h_0, 1.1h_0]$), so a from-scratch constant-$h_0$ init works as well. Positioned as a practical positive (drop-in on any off-the-shelf checkpoint) but shows the "learned posterior" framing is doing less work than the variational-learning framing suggests.
- The extreme limit ($N=G$, greedy decode per fresh model) is unstable (Appendix J) — some action-space sampling is still needed; pure parameter-space exploration doesn't fully replace it.
- Compute-limited: authors expect benefits to grow with model scale (citing pretraining-neighborhood-density arguments) but don't test it; no ablation of $\lambda$ against scale despite the hypothesis; the "rescue vs. lose" framing is a proxy metric, not validated per-prompt against downstream accuracy.

## Bearing on the mastered-prompts / zero-advantage conflict

[[../../conflicts/mcpo-vs-dapo-mastered-prompts]] debates what to do with zero-advantage GRPO groups once they occur: DAPO discards them (Dynamic Sampling), MCPO retains and anchors them with a hinge-KL penalty. 3PO doesn't take either side — it attacks the *upstream* cause instead. By diversifying the *policies* that generate a group's rollouts (via weight perturbation) rather than post-hoc filtering or reweighting groups that already collapsed to uniform reward, 3PO reduces how often zero-advantage groups arise in the first place. This is a third, orthogonal axis on the same failure mode — prevention-via-policy-diversity, compatible in principle with either discard or regularize as a fallback for groups that still go silent. It does not resolve whether DAPO's discard or MCPO's anchor is the right response to a silent group *once one occurs*; it only changes how often the question arises. Same posture as [[cue-grpo-rarity-credit]] and [[grpo-std-identity]] — reframes/sidesteps rather than adjudicates the DAPO-vs-MCPO dispute.

Also worth flagging against [[../self-play/invisible-leash]]'s Theorem C.1 ($\mathrm{supp}(\pi_\theta)\subseteq\mathrm{supp}(q)$ for on-policy updates, bounding $\mathrm{pass@}k$ from above by the base policy's support): weight-space noise, unlike token-level temperature noise, is not obviously bound by $\mathrm{supp}(\pi_\theta)$ — sampling from a different weight draw can put probability mass on trajectories the *original* policy's action-space support excludes. 3PO doesn't test this directly (no pass@k-ceiling analysis), but it's a candidate counter-mechanism to the Invisible-Leash support-inclusion argument, worth a follow-up check if the wiki ever formalizes weight-space exploration against that bound.

## Cited leads for follow-up

- **Bai, Wang, Ye, Chen (arXiv:2602.02555)** — concurrent "Learning to Explore with Parameter-Space Noise," applies classical Gaussian weight noise (Plappert/Fortunato-style) directly to RLVR; 3PO's authors frame it as a B3PO variant with an adaptive noise scheduler instead of a learned Hessian. Direct comparison paper worth ingesting.
- **Cong, Daheim, Shen, Yokota, Khan, Möllenhoff (arXiv:2506.14280)** — "Improving LoRA with variational learning," same author cluster; relevant to the wiki's selective-finetuning/LoRA theme.
- **Minut, Daheim et al. (arXiv:2606.23357)**, "SOAP-Bubbles" — structured (non-diagonal) weight uncertainty, flagged as the natural extension beyond IVON's diagonal approximation.

## Source

- `raw/research/weekly-2026-08-14/01-3po-parameter-exploration-rlvr.md`

## Related

- [[_overview]]
- [[dapo]] — 3PO cites DAPO's dataset/loss formulation as its training substrate; offers an orthogonal parameter-space lever to DAPO's action-space Clip-Higher / Dynamic Sampling
- [[mcpo]] — same zero-advantage-group symptom, different axis: MCPO regularizes after the fact, 3PO prevents beforehand
- [[cue-grpo-rarity-credit]] — another method that sidesteps rather than resolves the mastered-prompt conflict, via a different mechanism (post-normalization credit redistribution vs. pre-emptive policy diversity)
- [[grpo-std-identity]] — reframes the same conflict cluster from the std-normalization axis
- [[../rlvr-mechanics/curriculum-boundary-aware-rl]] — near-identical empirical target (zero-advantage / beyond-boundary collapse), attacked via teacher-guided trace injection rather than exploration
- [[../self-play/invisible-leash]] — Theorem C.1 support-inclusion bound; parameter-space noise is a candidate counter-mechanism, not tested directly here
- [[../rlvr-mechanics/_overview]] — general reward-is-the-bottleneck theme; 3PO's finding that action-space exploration mostly buys malformed/incorrect rollouts reinforces the theme's skepticism of undirected exploration fixes
- [[../../conflicts/mcpo-vs-dapo-mastered-prompts]] — 3PO adds a third position (prevention) to this open conflict
- [[../../weekly-briefs/2026-08-14]] — brought in by the 2026-08-14 weekly sweep
