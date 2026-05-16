---
name: invisible-leash
description: Wu et al. 2026 — formal proof that on-policy RLVR cannot assign positive probability to solutions the base model assigned zero, with empirical support showing shrinkage:expansion ratios of 2:1–3.6:1 across 1.5B–14B models; the foundational theoretical text for Position A (RLVR = precision-sharpening, not concept-installation).
type: research
---

# The Invisible Leash: Why RLVR May or May Not Escape Its Origin

Fang Wu, Weihao Xuan, Ximing Lu, Mingjie Liu, Yi Dong, Zaid Harchaoui, Yejin Choi (Stanford University; University of Tokyo / RIKEN AIP; University of Washington; NVIDIA). *The Invisible Leash? Why RLVR May or May Not Escape Its Origin.* Preprint arXiv:2507.14843, July 2025; revised February 2026. Correspondence: Yejin Choi.

RLVR is a support-constrained optimizer: it cannot assign positive probability to any solution the base model assigns zero probability. Across 1.5B–14B models on math, logic, factual QA, coding, and Reasoning Gym benchmarks, support shrinkage (correct solutions lost) consistently outweighs support expansion (new solutions gained) by ratios of 2:1 to 3.6:1. RLVR reliably improves pass@1 but depresses pass@k at large sampling budgets — and AIME2024 pass@8192 shows the base model at 93.3% versus ProRL-1.5B at 83.3% despite RLVR winning at pass@1.

## Method

The paper develops a formal framework measuring *support dynamics* over the solution set. Define $P$ = problems solvable by both base and RLVR, $E$ = problems newly solvable by RLVR (expansion), $S$ = problems solvable by base but lost by RLVR (shrinkage). Three statistics:

- $\text{SRR} = P / (P + S)$ — Support Retention Rate
- $\text{NDR} = E / (P + E)$ — Net Discovery Rate
- $\text{NSCR} = (E - S) / (P + E + S)$ — Net Support Change Rate

Sampling budgets $k \in \{1024, \ldots, 16384\}$ for Reasoning Gym; $k \in \{4096, 8192\}$ for math. Detectability threshold $\epsilon \approx 3.66 \times 10^{-4}$ at $k = 8192$, $\zeta = 0.05$.

Models: ProRL-1.5B-v1/v2, Nemotron-1-7B, Skywork-OR1-7B, Nemotron-1-14B, Phi4-Reason-Plus-14B, Kangheng-OVR-7B. SFT vs. RLVR comparison: Qwen2.5-Math-7B trained with DAPO vs. SFT on the same DeepMath-103K dataset.

## Claims

**1. Theorem C.1 — Support Preservation under on-policy RLVR.**

Let $\pi_\theta(y \mid x)$ be the RLVR-trained distribution obtained via standard on-policy gradient updates. Then for all $x \in \mathcal{X}$:

$$\mathrm{supp}(\pi_\theta(\cdot \mid x)) \subseteq \mathrm{supp}(q(\cdot \mid x))$$

If $q(y^* \mid x) = 0$ for some correct solution $y^*$, RLVR cannot discover $y^*$. Proof by induction: any $y^*$ with $\pi_\theta(y^* \mid x) = 0$ is never sampled, contributes no gradient, and remains at zero. Holds for REINFORCE, PPO, GRPO, DAPO, and REINFORCE++.

**2. Corollary C.2 — Asymptotic sampling upper bound.**

$$\limsup_{k \to \infty} \mathrm{pass@}k_{\pi_\theta}(x) \leq \limsup_{k \to \infty} \mathrm{pass@}k_q(x)$$

No finite sampling budget lets RLVR exceed the base model's asymptotic pass@k — the formal "invisible leash."

**3. Theorem C.6 — Entropy reduction.** Any RLVR update satisfies $H[\pi_\theta] \leq H[q]$ (equality only if reward is constant on the support). Establishes the precision–coverage trade-off: RLVR sharpens pass@1 by concentrating mass on known high-reward modes while narrowing the answer-level entropy.

**4. Proposition C.4 — Variational characterisation.** The RLVR objective is a KL projection:

$$\pi^*(y \mid x) \propto q(y \mid x) \cdot \exp(\beta R(x, y))$$

In the $\beta \to \infty$ limit, the optimal policy is the renormalised restriction of $q$ to the correct set $\mathcal{C}$. Even infinite reward pressure cannot escape $q$'s support.

**5. Aggregate support-dynamics (Table 1).** NSCR is uniformly negative (−0.01 to −0.06) across all tested models. ProRL-1.5B-v2: $P = 2388$, $E = 48$, $S = 175$; shrinkage:expansion ≈ 3.6:1. NDR never exceeds 0.04 anywhere.

**6. pass@k inversion.** AIME2024: base pass@8192 = 93.3% vs. ProRL-1.5B 83.3% despite RLVR winning at pass@1. Same pattern on leg-counting, family relationships, power function in Reasoning Gym.

**7. SFT vs. RLVR on identical data (Table 3).** SFT on DeepMath-103K produces positive NSCR (Olympiad NSCR = +0.042, $E = 49$, $S = 25$). DAPO on the same data produces negative NSCR (Olympiad NSCR = −0.065, $E = 25$, $S = 61$). This directly isolates the support-contraction effect to the RLVR objective itself, not the data or scale.

**8. Perplexity narrowing (Table 2).** RLVR increases model perplexity on external reasoning traces (DeepSeek-R1, Claude Sonnet 4). ProRL perplexity on Claude Sonnet 4 AIME2024 traces rises from 8.76 (base) to 14.91 (ProRL), confirming structural narrowing toward self-generated trajectories.

**9. Token vs. answer entropy decoupling.** ProRL and DAPO show *increased* token-level entropy (DeepSeek-1.5B: 0.44 → ProRL: 0.52) alongside *decreased* answer-level entropy. Higher local stochasticity does not imply global coverage expansion; token entropy is a misleading signal.

## Why this is load-bearing for single-sample concept learning

This is the foundational theoretical paper for **Position A** in [[../../conflicts/invisible-leash-vs-spiral-transfer]]: RLVR is quality-optimisation over latent capacity, not capacity installation. The implications are architectural:

Gradient updates will not install novel concepts; they will re-weight existing latent capacity. This forces the concept-installation question onto three channels:

1. **The proposer / curriculum** (component B in [[../synthesis/proposed-method]]): must supply problems at the edge of or outside current base-model support.
2. **The reference text** (component C): a worked example the model can imitate but not yet self-generate seeds new support via in-context learning *before* any gradient step.
3. **Distillation** (which the paper explicitly distinguishes from RLVR): providing ground-truth traces from a stronger oracle directly expands support — this is the SFT phase, not the RL phase.

The SFT-vs-RLVR comparison (Table 3) is directly actionable: if the method includes an SFT phase on reference-text traces, that phase is the true concept-installation step; RLVR afterward is precision-sharpening. Conflating the two misattributes concept learning to the RL phase.

The perplexity diagnostic (Table 2) is also reusable: if a trained model assigns high perplexity to reference-text reasoning traces, that is a signature of RLVR-induced narrowing, not improved understanding.

## Limitations

- **pass@k as the primary proxy** is imperfect — it captures solution retrieval, not novel reasoning capacity. Wen et al. (2025) propose CoT-pass@k as an improvement; results may be conservative.
- **Theorem C.1 requires on-policy sampling.** Off-policy methods, importance-sampling replay, or explicit diversity-seeking objectives are outside the theoretical scope; these are proposed (but not tested) as escape routes.
- **Empirical scope: mostly distilled bases.** All large models (except OLMo-2-0425-1B and Phi4) are distilled from DeepSeek-R1 checkpoints; results on genuinely non-distilled base models may differ.
- **OLMo-2-0425-1B outlier (NDR = 0.10).** This model shows substantially higher NDR and SDS than all others (Table 1, Table 12). The paper does not explain it; likely reflects a weaker base with more recoverable long-tail mass. Signals the pattern is not universal.
- **Evaluation targets final-answer correctness only.** Intermediate reasoning quality is not separately tracked.
- **Finite-$\epsilon$ threshold.** Completions just below the $\epsilon \approx 3.66 \times 10^{-4}$ detectability threshold might be recoverable with very large compute.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/01-invisible-leash.md`
- `../../../raw/research/self-play-quality-extraction/06-01-invisible-leash.md`
- arXiv: https://arxiv.org/abs/2507.14843

## Related

- [[understanding-self-play]] — operational follow-up: what self-play *can* achieve within the leash (precision sharpening, format alignment, subskill recomposition)
- [[yue-rlvr-boundary]] — independent empirical companion; pass@k inversion on 6 algorithms across 4 models; converges on the same conclusion
- [[two-stage-dynamic]] — refinement that scopes the leash to Stage 1; clarifies when Stage 2 distillation or curriculum escape applies
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — Wen et al. (2506.14245): **counterpoint**, not support — uses CoT-Pass@K to argue RLVR genuinely *extends* the reasoning boundary on AIME/coding, pushing back on the pure-reweighting (Position A) reading of this theorem
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — the recorded wiki tension; this paper is the primary text for Position A
- [[../synthesis/proposed-method]] — must account for which component handles concept-installation vs. precision-sharpening given this paper's constraint
- [[_overview]]
- [[../decoding-time-steering/_overview]] **(added 2026-05-13)** — every method in the decoding-time / activation-steering theme satisfies Theorem C.1 **by construction**: no gradient updates, no support shifts. The clearest existence proofs: [[../decoding-time-steering/actadd]] (no-support-shift at $n=1$ contrast pair), [[../decoding-time-steering/iti]] (random-direction control is null — only directions internal to base support are causally effective), [[../decoding-time-steering/repe]] (LAT-derived reading vectors transfer base→RLHF chat, confirming concept directions exist pre-training), [[../decoding-time-steering/contrastive-decoding]] (CD's $V_\text{head}$ plausibility gate hard-masks tokens below expert's top mass — Theorem C.1 enforced at decode time). The 4-year decoding-time arc is the empirical complement of this paper's formal result.
