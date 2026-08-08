---
name: grpo-std-identity
description: Exact finite-group identity showing GRPO/Dr.GRPO/DAPO are three operations on one scalar (group std); reframes (not resolves) the mcpo-vs-dr-grpo-std-fix conflict
type: research
---

# GRPO, Dr. GRPO, and DAPO Are Three Operations on One Number: The Group-Standard-Deviation Identity

A theory paper (not a new algorithm) that derives an exact, finite-group policy-gradient identity for binary-reward RLVR and uses it to show GRPO, Dr. GRPO, and DAPO differ only in what they do to a single scalar — the group reward standard deviation $\sigma = \sqrt{k(G-k)}/G$ for $k$ correct out of $G$ rollouts: GRPO divides by it, Dr. GRPO drops the division, DAPO discards the group when it is zero. The identity yields two closed forms with no free parameters — a group-size law $G^* = 1/(8\varepsilon p(1-p))$ for a target gradient fidelity $1-\varepsilon$, and a silent-group rate $p^G+(1-p)^G$ — both validated against Big-Math (N=215,608 problems) and a controlled 6,000-prompt Bernoulli-logit training run. The paper's central interpretive claim is that GRPO's $\sigma$-division and Dr. GRPO's removal are not a bug/fix pair but two different, individually coherent implicit objectives (arcsine-stabilized $E[2\arcsin\sqrt p]$ vs. raw success rate $E[p]$) — this reframes, without adjudicating, the open [[../../conflicts/mcpo-vs-dr-grpo-std-fix|mcpo-vs-dr-grpo-std-fix]] conflict.

## The identity

For a prompt with $G$ i.i.d. rollouts under the current policy and a binary verifier reward ($k$ correct, $G-k$ incorrect), a single on-policy GRPO gradient step (ratio $=1$, first step only) is exactly:

$$g = \sigma\,(\bar s_+ - \bar s_-), \qquad \sigma = \frac{\sqrt{k(G-k)}}{G} \tag{Eq. 4, Thm. 1}$$

where $\bar s_+, \bar s_-$ are the mean score-function gradients $\nabla_\theta \log \pi_\theta$ over the correct and incorrect rollouts respectively. This holds **independent of any baseline choice** and in **any policy parameter dimension** — it is an exact algebraic identity for the binary-reward case, not an approximation. $\sigma = \sqrt{k(G-k)}/G$ is precisely the empirical standard deviation of a $G$-sample Bernoulli group, which is why every downstream difference between GRPO, Dr. GRPO, and DAPO collapses to what each does with this one number.

**Proposition 1** (mean-centering = RLOO): GRPO's advantage construction is two operations — mean-center, then divide by $\sigma$. The mean-centering step alone equals the RLOO / baselined-REINFORCE advantage ([[rloo]]) up to a constant $G/(G-1)$ rescaling absorbed into the learning rate. So among GRPO's two operations, **only the $\sigma$-division is objective-changing**; mean-centering is a free (bias-preserving) baseline choice, consistent with [[dr-grpo]]'s own appendix derivation of the same equivalence.

## Three operations on $\sigma$

| Method | Operation on $\sigma$ | Implicit objective ascended | Consequence |
|---|---|---|---|
| **GRPO** | divide by $\sigma$ | $E[2\arcsin\sqrt p]$ — arcsine-variance-stabilized | Bathtub-shaped difficulty weight $w(p) = 1/\sqrt{p(1-p)}$ reallocates gradient mass toward extreme-difficulty prompts |
| **Dr. GRPO** | drop division ($\sigma \to 1$) | $E[p]$ — raw success rate | Uniform per-prompt weight; recovers the unbiased PPO-style objective (matches [[dr-grpo]]'s own std-bias diagnosis) |
| **DAPO** | discard if $\sigma = 0$ (keep-rule $0<k<G$) | $E[p]$ restricted to non-silent groups | Removes the $p^G+(1-p)^G$ silent-group mass entirely rather than down- or up-weighting it; refills via oversampling (matches [[dapo]]'s Dynamic Sampling) |

Note DAPO's other three tricks (Clip-Higher, Token-Level Loss, Soft Overlong Punishment) are untouched by this identity — only Dynamic Sampling maps onto the $\sigma=0$ discard operation.

## Closed forms

**Large-$G$ attenuation** (Corollary 1, Eq. 7): the realized gradient magnitude at finite $G$ relative to its large-$G$ limit $\sqrt{p(1-p)}$:

$$\sigma(G,p) \approx \sqrt{p(1-p)}\left(1 - \frac{1}{8Gp(1-p)}\right)$$

**Group-size law** (Corollary 2, Eq. 9): the group size $G^*$ needed for gradient fidelity $1-\varepsilon$ at difficulty $p$:

$$G^* = \frac{1}{8\varepsilon\, p(1-p)} = \frac{w(p)^2}{8\varepsilon}, \qquad w(p) = \frac{1}{\sqrt{p(1-p)}} \tag{Eq. 11}$$

$w(p)$ is the same bathtub-shaped difficulty weight GRPO's $\sigma$-division induces — the harder (or easier) the prompt, the more rollouts it takes to realize a faithful gradient.

| Difficulty $p$ | $G$ for 95% fidelity | $G=8$ realized fidelity |
|---|---|---|
| 0.5 (coin-flip) | $\approx 11$ | 93% |
| 0.05 (hard) | $\approx 69$ (exact: 273 at 99% vs. closed-form 263) | $\approx 54\%$ |

At the conventional $G=8$, coin-flip prompts are near gradient-faithful; a $p=0.05$ prompt needs roughly $6\times$ more rollouts and is badly underfit at $G=8$.

**Silent-group rate** (Eq. 10): $p^G + (1-p)^G$ — the probability a group of $G$ rollouts is all-correct or all-wrong (zero gradient under GRPO/Dr. GRPO, discarded under DAPO). At $G=8$: **44%** closed-form vs. **43%** measured by direct rollout subsampling on Big-Math. An irreducible **11.2%** of prompts are silent at *any* $G$ (those with true solve rate exactly 0 or 1).

## Empirical validation

- **Big-Math** (N=215,608 problems, empirical solve rates from Llama-3.1-8B, static gradient-budget accounting, not live training): standardization (GRPO's $\sigma$-division) shifts gradient-mass share on extreme-difficulty prompts from **13.9% → 24.7%** (1.78× reallocation vs. Dr. GRPO), and correspondingly reduces medium-difficulty share 22.8% → 17.5%.
- **Controlled run** (M=6,000 Bernoulli-logit toy prompts, 150 training steps, $G=8$, GRPO vs. Dr. GRPO vs. DAPO — a live but non-LM toy training loop): realized (finite-$G$) version of the same reallocation, 14.3% → 17.0%; silent-group-rate prediction vs. measured tracks at $R^2=0.999$ across training; GRPO lifts the initially-hardest quartile to 0.99 mean solve rate vs. Dr. GRPO's 0.88; DAPO is fastest to converge but at 3.5× oversampling cost concentrated on the same difficulty extremes GRPO upweights.
- DAPO's own reported all-correct-fraction curve is reproduced from the closed form at $R^2=0.92$ — flagged by the authors as a consistency check, not a unique fit (a generic 2-parameter saturating curve fits equally well, $R^2=0.98$).

## Limitations (author-stated)

- Binary reward only — no treatment of continuous/non-binary reward.
- On-policy, first-gradient-step only ($\text{ratio}=1$); clipping, KL penalty, and off-policy staleness are explicitly out of scope.
- Controlled-run validation uses scalar Bernoulli-logit toy policies, not a real LM training loop — "a full language-model training loop... is the natural next test."
- Closed-form group-size law degrades near $p \in \{0,1\}$ (exact $G=273$ vs. closed-form $G^*=263$ at $p=0.05$, 99% fidelity).
- No held-out task-accuracy evaluation anywhere in the paper — every result is about gradient-mass allocation and training dynamics, not downstream benchmark performance.
- Explicitly flagged as open: whether the extra weight standardization places on the hardest prompts improves generalization beyond the trained difficulty range.

## Bearing on the mcpo-vs-dr-grpo-std-fix conflict

This paper does **not** resolve [[../../conflicts/mcpo-vs-dr-grpo-std-fix|the open conflict]] over whether Dr. GRPO's std-removal is a complete fix for GRPO's difficulty bias, or whether MCPO's advantage-denominator rescaling is required on top of it (per [[mcpo]] Sec 4.2). Instead it **reframes the terms of the debate**: §6 ("What the Division Optimizes") and §10 (Discussion) argue there is no single privileged ground-truth objective to be "fixed" toward — $\sigma$-division and $\sigma$-removal ascend two different, individually valid objectives ($E[2\arcsin\sqrt p]$ vs. $E[p]$), and "the right choice depends on whether the training goal prioritizes raw success-rate alignment, hard-prompt pressure, or compute efficiency." This sharpens rather than settles the conflict: it supplies the exact closed forms (group-size law, difficulty weight $w(p)$) needed to quantify what MCPO's rescaling actually trades off, but is silent on whether MCPO's "incomplete fix" characterization of Dr. GRPO is itself correct — MCPO's specific claim (that a $p(1-p)$-proportional weight *survives* std-removal and requires further correction) is neither confirmed nor contested here. Relatedly, §5 notes discarding is not the only response to a silent group — a fixed-reference sign advantage (Nie et al., arXiv:2605.07689) assigns nonzero updates to unanimous groups instead — bearing on, but not resolving, [[mcpo]]'s Dynamic-Sampling critique of DAPO.

## Source

- `raw/research/weekly-2026-08-07/01-grpo-drgrpo-dapo-identity.md`

## Related

- [[dr-grpo]] — this source supplies the exact finite-group identity and large-$G$ limit ($E[p]$) underlying Dr. GRPO's std-removal fix, and formalizes its difficulty-bias observation as exactly $\partial_p\, 2\arcsin\sqrt p$
- [[dapo]] — formalizes DAPO's Dynamic Sampling as precisely discarding the $\sigma=0$ silent-group mass $p^G+(1-p)^G$; reproduces DAPO's own all-correct-fraction curve from the closed form
- [[mcpo]] — directly implicated in the reframed conflict (see below); this source's closed forms quantify the difficulty-weighting tradeoff MCPO's advantage rescaling operates on, without adjudicating MCPO's "incomplete fix" claim against Dr. GRPO
- [[../rlvr-mechanics/deepseekmath-grpo]] — original GRPO; this source's Eq. 4 identity underlies its standardized-advantage construction exactly
- [[rloo]] — Proposition 1 formally confirms GRPO's mean-centering step is RLOO / baselined-REINFORCE up to a $G/(G-1)$ rescaling
- [[first-principles-two-axis-framework]] — parallel unification effort for the same GRPO-family lineage via a different lens (algebraic single-group identity here vs. two-axis structural derivation there); complementary, not conflicting
- [[../../conflicts/mcpo-vs-dr-grpo-std-fix]] — reframes rather than resolves — see conflict file for full analysis
- [[../../weekly-briefs/2026-08-07]] — brought in by the 2026-08-07 weekly sweep
