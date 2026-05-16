# BOLT: Reference-Sampled Boltzmann Projection for KL-Regularized RLVR

Shu et al. (arXiv:2605.02469, May 2026). For KL-regularised RLVR with fixed reference policy $\pi_\text{ref}$, the **unique** reference-sampled weighted-SFT objective whose induced policy equals the Boltzmann target $\pi^*(y|x) \propto \pi_\text{ref}(y|x) \exp(r(x,y)/\beta)$ is the prompt-normalised density-ratio weight $w^\star = \exp(r/\beta)/Z(x)$ (Theorems 3, 4). Any other weighting (raw reward, filtered positive, advantage) pays an irreducible RLVR value gap (Corollary 5). The paper derives **finite one-shot saturation** ($\beta \log(1/\pi^*(S_N|x))$, Theorem 6) and a coverage–ESS frontier (Theorem 7), and shows iterative BOLT is exactly **KL policy mirror descent** — after $K$ rounds with sampler refresh, $\pi_{\theta_K} \propto \pi_{\theta_0} \exp(K r/\beta)$ (Theorem 11). Empirically: matches/exceeds GRPO at 75–85% less wall-clock, 18–31% less peak memory.

Together with [[tsallis-loss-continuum|Tsallis $\mathcal{J}_Q$]] (which did the un-regularised case), BOLT closes the analytical picture of KL-regularised RLVR as a member of the weighted-SFT family.

## Intuition

KL-regularised RLVR has a closed-form solution: $\pi^*(y|x) \propto \pi_\text{ref}(y|x) \exp(r(x,y)/\beta)$ — the reference policy **tilted** toward high-reward sequences, with $\beta$ controlling tilt aggressiveness. This Gibbs/Boltzmann form is also the starting point in [[../rlvr-mechanics/binary-rewards-rl-challenges]] Eq. 1.

The central move: $\pi^*$ is a *reweighted version of $\pi_\text{ref}$*, so you can hit it with a one-shot weighted cross-entropy fit on samples drawn from $\pi_\text{ref}$ — no RL gradient needed. "Weighted SFT" in BOLT's sense means standard cross-entropy where each $(x, y_n)$ example carries a credit-weight $\hat{w}(x, y_n) = \exp(r(x, y_n)/\beta)/\hat{Z}_N(x)$ — the prompt-normalised Boltzmann density-ratio (Eq. 10). Theorem 3 shows this objective's gradient equals the forward-KL projection gradient $\nabla\text{KL}(\pi^*\|\pi_\theta)$, and Theorem 4 makes the Boltzmann ratio the *unique* weight (up to prompt scale) that lands on $\pi^*$ when sampling from $\pi_\text{ref}$. Any other weighting — raw $\exp(r/\beta)$, filtered-positive (as in [[../self-improvement/star]] / ReST), advantage — misses $\pi^*$ by an irreducible $\beta \cdot \mathbb{E}_x[\text{KL}(\tilde\pi_w\|\pi^*)]$ (Corollary 5; 1.44–3.60 pp empirically, Table 2).

What RL still buys over one-shot BOLT, both bounded:
- **Wider support.** Theorem 6 caps one-shot BOLT at $\beta\log(1/\pi^*(S_N|x))$ — more epochs can't close this; only more or better rollouts can. Theorem 7 makes the binding constraint reference pass-rate $p_\gamma$, not budget.
- **Sampler refresh.** Theorem 11: iterative BOLT (refresh the sampler from the current policy each round, equivalently update the reference to the newly fitted policy) is *exactly* KL policy mirror descent — after $K$ rounds, $\pi_{\theta_K} \propto \pi_{\theta_0}\exp(K r/\beta)$. Corollary 12: when reference pass-rate $p_0(x) > 0$, iterative BOLT closes the static-vs-online gap *exponentially* in $K$. RL's marginal value over BOLT lives in sampler refresh, not in the gradient method.

The slogan: **online RLVR is one way to sample $\pi^*$; static weighted SFT with the Boltzmann ratio is another, and they share the same target.**

**Iterative refresh closes the static-vs-online gap, not the support bound.** The cumulative target $\pi_{\theta_0}\exp(Kr/\beta)$ is supported on $\text{supp}(\pi_{\theta_0})$ for every $K$ — exactly [[../self-play/invisible-leash]] Theorem C.1 applied to the iterated procedure. Sharpening by factor $K$ is equivalent to running at $\beta_\text{eff} = \beta/K$, which under misspecification *worsens* the [[../rlvr-mechanics/binary-rewards-rl-challenges]] near-Dirac collapse (Eq. 10), and aligns with [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s 0%-shifted-outside-base-top-5 finding. Capacity expansion needs distillation from a *teacher* with support outside $\pi_{\theta_0}$ ([[../self-play/yue-rlvr-boundary]]) or an entropy-preserving Stage-2 mechanism ([[../self-play/two-stage-dynamic]]) — not more BOLT rounds on the same base.

## Weighting scheme — mechanical view

The Boltzmann weight $\hat{w}(x, y_n) = \exp(r(x, y_n)/\beta)/\hat{Z}_N(x)$ is **a per-prompt softmax over the $N$ verifier-scored rollouts at temperature $\beta$**, scaled so the per-prompt weight-sum is $N$ (i.e. the average rollout-credit is 1).

Within a prompt, only reward *differences* matter — $\hat{w}(x, y_a)/\hat{w}(x, y_b) = \exp((r_a - r_b)/\beta)$. Across prompts, the per-prompt denominator $\hat{Z}_N(x)$ cancels prompt-difficulty bias: a prompt where every rollout scores high doesn't dominate one where every rollout scores low. **Both kinds of normalisation are load-bearing**: dropping the prompt-wise normalisation (raw $\exp(r/\beta)$) lands on a different target, with empirical 1.44–3.60 pp loss in Table 2.

Limits of the softmax temperature:
- $\beta \to 0$: weights concentrate on the top-reward rollout per prompt — equivalent to greedy rejection-sampling / RFT.
- $\beta \to \infty$: weights flatten to uniform — reduces to plain SFT on $\pi_\text{ref}$-samples.
- Iterative refresh: $K$ rounds at $\beta$ is equivalent to one round at $\beta_\text{eff} = \beta/K$ (Theorem 11), so iteration *sharpens* the softmax over time.

Comparison to alternative weighting choices, all of which miss $\pi^*$ by $\beta \cdot \mathbb{E}_x[\text{KL}(\tilde\pi_w \| \pi^*)] > 0$ (Corollary 5; Table 1):

| Weight $w(x, y)$ | What goes wrong | Cross-ref |
|---|---|---|
| **$\exp(r/\beta) / \hat{Z}_N(x)$** | **(BOLT — uniquely lands on $\pi^*$ given $q=\pi_\text{ref}$, Theorem 4)** | — |
| $\exp(r/\beta)$ raw | Cross-prompt bias: easier prompts over-dominate the loss | Table 2 |
| $\exp(r/\beta) / Z_\text{global}$ | Same cross-prompt bias at a different scale | Table 1 |
| $\mathbb{1}[r > \tau]$ (filtered positive) | Discards the $\beta$-controlled margin; all "correct" rollouts treated equally | [[../self-improvement/star]] |
| $A(x, y)$ (advantage) | Lands on a non-$\pi^*$ target | Table 1 |

## Source

- `raw/research/weekly-2026-05-10/04-bolt-kl-rlvr-boltzmann.md`

## Method

**Two-phase procedure (Algorithm 1).**

*Phase 1.* Sample $N$ rollouts per prompt from $\pi_\text{ref}$. Compute verifier scores $r(x, y_n)$. Estimate prompt-wise normaliser $\hat{Z}_N(x) = \frac{1}{N} \sum_n \exp(r(x, y_n)/\beta)$. Store empirical Boltzmann weights $\hat{w}(x, y) = \exp(r/\beta)/\hat{Z}_N$ (Eq. 10).

*Phase 2.* Standard multi-epoch weighted SFT on the precomputed dataset.

**Theorem 3.** The reference-sampled weighted-likelihood gradient equals the forward-KL projection gradient $\nabla \text{KL}(\pi^* \| \pi_\theta)$ — i.e. the weighted-SFT induced policy lands on $\pi^*$.

**Theorem 4 (target-matching law).** Any sampler-weight pair $(q, w)$ with $\tilde{\pi}_w = \pi^*$ must satisfy $w(x, y) = \bar{w}(x) \cdot \pi^*(y|x) / q(y|x)$. Under $q = \pi_\text{ref}$ this collapses uniquely to the Boltzmann ratio (up to prompt scale).

**Corollary 5.** Any target mismatch is irreducible RLVR value loss:

$$J_\text{RL}(\pi^*) - J_\text{RL}(\tilde{\pi}_w) = \beta \cdot \mathbb{E}_x[\text{KL}(\tilde{\pi}_w \| \pi^*)]$$

**Theorem 6 (one-shot saturation).** With stored support $S_N$ from $N$ rollouts, the achievable RLVR value is bounded by

$$J_\text{RL}(\pi^*) - J_\text{RL}(\hat{\pi}) \geq \beta \log(1/\pi^*(S_N | x))$$

— extra SFT epochs cannot remove this gap. The bound depends only on the *support*, not the rollouts' weights.

**Theorem 7 / Corollary 8 (coverage–ESS frontier).** Hitting near-optimal set $A_\gamma(x)$ with probability $\geq 1-\delta$ requires

$$N \gtrsim \max\left(\frac{\log(1/\delta)}{p_\gamma(x)},\, \frac{L^2 C_2(x) \log(1/\delta)}{\varepsilon^2}\right)$$

For binary verifier with reference pass-rate $p$: $C_2(x) \geq (1-\eta)^2/p$. **The binding constraint is reference pass-rate $p_\gamma$, not budget.**

**Theorem 11 — iterative BOLT = KL-PMD.** With sampler refresh between rounds, after $K$ rounds: $\pi_{\theta_K}(y|x) \propto \pi_{\theta_0}(y|x) \exp(K r(x,y)/\beta)$ — effective temperature sharpens by factor $K$. Recovers relative-entropy policy search.

## Empirical results (Qwen3-8B)

| Method | GSM8K | MATH | Time | Mem |
|---|---|---|---|---|
| GRPO | (baseline) | (baseline) | 1.0× | 1.0× |
| BOLT | +2.95 pp | +6.16 pp | 0.15× | 0.69–0.82× |
| Iterative BOLT | +1.68 to +3.38 pp over best non-BOLT | | | |

Single-run, no multi-seed; treat as directional.

## Why this matters for the wiki's central question

1. **One-shot saturation has a closed form (Theorem 6).** Wang et al.'s [[../single-sample-rl-finetuning/1-shot-rlvr|1-shot RLVR]] sits at the frontier of $N=1$. BOLT explains *exactly* what 1-shot can and cannot achieve: bounded by $\beta \log(1/\pi^*(S_1|x))$. If $S_1$ already covers near-optimal sequences for the prompt, the gap is small; otherwise no SFT epoch budget closes it.
2. **Coverage wall (Theorem 7).** Sample efficiency is governed by reference pass-rate $p_\gamma$, *not* model capacity. This sharpens the design constraint for any single-sample method: the chosen training example must lie in the high-$p_\gamma$ regime of the base model.
3. **Iterative refresh recovers RL** (Theorem 11). Each refresh round multiplies the effective $\beta$-sharpness by 1 — closes the static gap exponentially when $p_0(x) > 0$ (Corollary 12). RL's marginal value over BOLT comes from refresh, not the gradient method itself.

## Connections to the wiki

- **[[../single-sample-rl-finetuning/1-shot-rlvr]]** — Theorem 6 + Theorem 7 directly explain when 1-shot RLVR works and where it fails. Should propagate the gap formula back to that page.
- **[[../single-sample-rl-finetuning/_overview]]** — canonical analytical account of the single-sample regime.
- **[[tsallis-loss-continuum]]** — Tsallis $\mathcal{J}_Q$ unifies RLVR/SFT for the **un-regularised** objective. BOLT does the analogous unification for the **KL-regularised** objective. Together they cover both ends.
- **[[dpo]]** — DPO uses the same Boltzmann closed form but doesn't address finite-coverage gaps. BOLT extends the static analysis.
- **[[maspo]]** — induced-target taxonomy (Table 1 of BOLT) lines up with MASPO's unifying axes; only BOLT achieves $\tilde{\pi}_w = \pi^*$ exactly.
- **[[dapo]]** — DAPO is the large-scale online RLVR system; BOLT provides its **static** weighted-SFT replacement theory and an empirical demonstration that the static replacement is competitive at much lower wall-clock.
- **[[../rlvr-mechanics/_overview]]** — Theorem 11 recovers PMD; an analytical link from RLVR-as-iterative-BOLT to RL theory.
- **[[../self-improvement/star]]** — STaR appears in BOLT Table 1 with induced target $q^+ \neq \pi^*$; BOLT explains its population-level bias.
- **[[../self-play/invisible-leash]]** — the support wall (Theorem 6) is the static-data counterpart of the invisible-leash dynamic. Position A gets sharper with BOLT.
- **[[../synthesis/proposed-method]]** — Theorems 6/7 are load-bearing for the proposed method's sample-efficiency analysis.

## Conflicts

- **vs. online RLVR (DAPO, Kimi k1.5).** BOLT matches/exceeds GRPO at far less compute. Single-run; not multi-seed or budget-matched. Directional, not settled.
- **vs. Refit / raw-reward weighting.** Corollary 5 + Table 2 (1.44–3.60 pp gap) confirm population bias of unnormalised reward weights; common practice (STaR, ReST filtering) is suboptimal in target.

## Related

- [[../single-sample-rl-finetuning/1-shot-rlvr]]
- [[../single-sample-rl-finetuning/_overview]]
- [[tsallis-loss-continuum]]
- [[dpo]]
- [[maspo]]
- [[dapo]]
- [[dr-grpo]]
- [[../rlvr-mechanics/_overview]]
- [[../rlvr-mechanics/binary-rewards-rl-challenges]] — companion theory paper this week
- [[../self-improvement/star]]
- [[../self-play/invisible-leash]]
- [[../synthesis/proposed-method]]
- [[../../weekly-briefs/2026-05-10]] — brought in by the 2026-05-10 weekly sweep
- [[../decoding-time-steering/_overview]] **(added 2026-05-13)** — full decoding-time / activation-steering theme. The Boltzmann form $\pi^* \propto \pi_\text{ref}\exp(r/\beta)$ has structural analogues at decode time: [[../decoding-time-steering/cfg-lm]] $\log P(w\|c) + \gamma(\log P(w\|c) - \log P(w))$ where the conditioning direction acts as the reward; [[../decoding-time-steering/contrastive-decoding]] expert-minus-amateur logit difference; [[../decoding-time-steering/dexperts]] $\mathbf{z} + \alpha(\mathbf{z}^+ - \mathbf{z}^-)$. Each lands on the same target distribution as a Boltzmann tilt of the base for concepts already in support; see [[../synthesis/decoding-time-shapes]] for the explicit Bayesian-vs-Boltzmann correspondence table.
