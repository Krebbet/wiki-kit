# Strategic Classification

Mechanism page for the **strategic classification** literature: the formal game in which a firm posts a classifier *f*, individuals best-respond by manipulating their input *x* to ∆(x) at cost *c(x, ∆(x))*, and the firm anticipates this response when designing *f*. This is the theoretical underpinning of the entire profile-manipulation lever cluster on [[possible-strategic-levers]] (#6 session-rotation, #7 demographic spoofing, #11 fingerprint parity), the [[obfuscation]] mechanism page, and the per-attribute spoofing arms race documented on [[browser-fingerprinting]]. Anchored on Hardt, Megiddo, Papadimitriou & Wootters 2016 (foundational); Liu et al. 2024 *Contextual Dynamic Pricing with Strategic Buyers* (the pricing-domain instantiation); and Milli, Miller, Dragan & Hardt 2019 (the social-cost counter-argument). Where ACA ([[algorithmic-collective-action]]) studies *coordinated* user-side manipulation, strategic classification studies *individual-level* manipulation in equilibrium.

## Foundational framework — Hardt, Megiddo, Papadimitriou & Wootters 2016

ITCS 2016; arXiv 1506.06980. The paper formalises gaming as a sequential Stackelberg game and identifies a sharp computational frontier between tractable and intractable cost functions.

**The full-information game (Definition 1.1):**
- **Jury** (firm), knowing distribution *D*, target classifier *h*, and cost function *c*, publishes classifier *f*.
- **Contestant** (individual), knowing all the above, plays best-response ∆(x) = argmax_y *f(y) − c(x, y)*. Maximises utility = *f(∆(x)) − c(x, ∆(x))*.
- Jury's payoff is *P[h(x) = f(∆(x))]*.

**The statistical game (Definition 1.4):** Jury observes only labelled samples from *D* and *h*, publishes *f*. Strategy-robust learning (Definition 1.5) requires *f* to achieve payoff ≥ OPT_h(D, c) − ε with high probability over samples, for *any* h and D — a stronger guarantee than PAC learning.

**Key dichotomy:**

| Cost function class | Tractability |
|---|---|
| **Separable** (c(x, y) = max{0, c₂(y) − c₁(x)}) | **Polynomial-time, sample-efficient strategy-robust learning** (Theorem 2.3 + Algorithm 1). Sample complexity depends only on Rademacher complexity of *H*. |
| **Minima of k separable functions** | poly(m, exp(k), 1/ε, log(1/δ)) — bounded blow-up. Every cost function on finite X can be written as a minimum of |X|² separable functions (Proposition 3.1); for metrics, an ε-net covers via covering-number-many functions. |
| **General metric costs** | **NP-hard** (Theorem 4.1, reduction from 3SAT) — even with full information about *h* and uniform *D*, computing the strategic maximum within ε = 1/|X|^η is NP-hard. |

**Algorithm 1 (separable case)** is mechanically simple: candidate thresholds are *s_i ∈ c₂(X)*; empirical error err(s_i) = P[h(x) ≠ c₁[s − 2](x)] is computed on samples; the empirically-best threshold is returned. Claim 2.6 shows that separable costs let the optimal acceptance region be expressed as a threshold on c₂(·), so the search space collapses.

**Empirical anchor (§5):** Apontador (Brazilian search engine) spam-detection dataset. Algorithm 1 outperforms standard SVMs under realistic gaming and remains robust to substantial cost-function misspecification.

**Why this matters for the wiki:** the separable / non-separable distinction tells you *which manipulation lever is durable*. Attributes whose manipulation cost is independent of the original value (separable) admit polynomial-time firm response; attributes whose manipulation cost depends on the original (non-separable, metric) make robust-classification NP-hard. This is the formal argument for why **per-attribute spoofing tools (Family 6 fingerprint rotation per [[browser-fingerprinting]]) are recoverable by adaptive firms** — the cost structure is separable enough.

## Pricing-domain instantiation — *Contextual Dynamic Pricing with Strategic Buyers*

arXiv 2307.04055. Direct extension of the Hardt et al. 2016 framework to the contextual-bandit / dynamic-pricing setting. The seller posts a contextual price function; the buyer manipulates context features at cost to obtain a lower price; the seller does not observe the true features.

**Two headline results:**

1. **Theorem 1 — naive pricing is broken.** Standard contextual pricing using observed (manipulated) features incurs **linear regret Ω(T)** under strategic buyers. The naive-seller setting is the formal proof that obfuscation works against an unsophisticated firm.

2. **Theorems 2 + 3 — adaptive pricing recovers Õ(√T) regret.** A two-phase **explore-then-exploit** structure:
   - **Exploration phase** uses uniform pricing (price independent of features → zero manipulation incentive → buyer reveals true features honestly).
   - **Exploitation phase** estimates the buyer's equilibrium manipulation rule **x_t = x_t⁰ − A⁻¹β₀ g'(·)** and prices accordingly (back out true features).

**The cost-structure parameter.** The smallest eigenvalue λ_min(A) of the manipulation-cost matrix determines the regret penalty, *not* whether learning succeeds. Higher manipulation cost → smaller penalty for the seller; learning still recovers sublinear regret.

**Critical implication for the wiki — see [[the-firms-view|§3]] and [[obfuscation-strategic-readout]]:**

> Obfuscation **is** effective against naive contextual pricing. Against **adaptive sellers** with multi-phase learning + repeat-buyer data, obfuscation effectiveness *degrades over time*. The seller can infer the manipulation structure and recover sublinear regret. Wiki framings of "high effectiveness against [[pricing-algorithm-taxonomy|Family 1 / Family 3]]" need an adaptive-seller caveat.

## Social-cost counter-argument — Milli, Miller, Dragan & Hardt 2019

FAccT 2019; arXiv 1808.08460. Inverts the strategic-classification programme: when the firm tightens its threshold in response to manipulation, what happens to the cost borne by *individuals*?

**Core trade-off (Theorem 3.1):** Institutional utility U_∆(τ) is quasiconcave in threshold τ; social burden B₊(τ) is monotonically non-decreasing. **Any increase in firm accuracy beyond the non-strategic optimum strictly increases the expected cost B₊(τ) that *positive (deserving)* individuals must incur to be correctly classified.** This is unavoidable for outcome-monotonic cost functions.

**Disparate-impact amplification — two routes to inequity:**

1. **Theorem 4.1 — different feature distributions.** Under first-order stochastic dominance (disadvantaged group has lower outcome likelihoods conditional on being truly positive), the social *gap* G(τ) = B₊,b(τ) − B₊,a(τ) is positive and monotonically increasing in τ.
2. **Theorem 4.2 — different adaptation costs.** With identical feature distributions but higher adaptation costs for a disadvantaged group (κ ≥ 1), the social gap is non-negative and monotonically non-decreasing in τ.

**FICO empirical anchor (n = 301,536):** with linear cost c(x, x') = α(x' − x), the Black-white gap grows from ~0 at τ = 0 to substantial disparity at τ = 100. With cost ratio κ = 2, threshold increase 60 → 70 multiplies the Black-white gap by ~2.5; κ = 3 gives ~4×.

**Lemma 3.2 — Nash vs Stackelberg.** Nash equilibria, unlike Stackelberg, provide latitude to trade off institutional utility against social burden. Stackelberg solutions (firm-leader, accuracy-maximising) impose maximal social burden.

**Implication carried into the strategy layer (see [[obfuscation-strategic-readout]] §Disparate-Impact Externality).** Per-individual obfuscation, deployed without collective constraint on firm response, creates a **regressive equity externality**:
- Wealthy users absorb the rising manipulation cost.
- Disadvantaged users face an increment they cannot afford.
- The aggregate consumer-side action makes the firm tighten — the cost falls on those who can't manipulate.

This is the strongest argument *against* obfuscation as a sole-lever strategy and the strongest argument *for* pairing obfuscation with collective constraint (regulation, antitrust, [[platform-cooperatives|exit pathway]]) on firm response.

## How this maps onto the wiki

| Wiki anchor | Strategic-classification connection |
|---|---|
| [[obfuscation]] | The mechanism page for per-individual feature manipulation. Strategic classification provides the formal equilibrium model. The Bó et al. 2024 pricing strategic-response experiment cited there is a direct empirical instance of this game. |
| [[obfuscation-strategic-readout]] | Strategy readout. Now updated with (a) the adaptive-seller caveat from B2 and (b) the disparate-impact externality from B3 (Milli et al.). |
| [[browser-fingerprinting]] | Per-attribute spoofing arms race is the engineering instantiation. Venugopalan et al. 2024 FP-Inconsistent (~97% TNR) is a direct instance of the firm winning the strategic game when separability + cross-attribute consistency are exploitable. |
| [[pricing-algorithm-taxonomy]] | Family 1 (GLM/contextual bandit) and Family 3 (retail offer bandit) are the pricing-algorithm classes most directly subject to the *Contextual Dynamic Pricing with Strategic Buyers* result. |
| [[possible-strategic-levers\|Lever #6 (session rotation), #7 (demographic spoofing), #11 (fingerprint parity)]] | All sit inside this framework. The separability dichotomy says which spoofing dimensions firms can recover from cheaply. |
| [[collective-bargaining-for-data]] | Porat 2024's individual strategic abstention is the framework's instance for an individual deciding whether participation cost exceeds the benefit. Hardt 2016's game theory underwrites Porat's analysis. |
| [[algorithmic-collective-action]] | The *coordinated* counterpart. ACA studies what α-fraction collectives can achieve when manipulation is jointly chosen; strategic classification studies what individuals achieve in equilibrium. Same mechanism layer, different agency assumption. |
| [[the-firms-view]] §3, §4 | Firm-side framing of the same dynamics: robust pricing under strategic buyers + threshold-tightening with disparate impact. |

## Conflict / qualification carried into strategy

**Hardt et al. 2016's framing assumes both parties act rationally with clear payoffs.** Richards & Hartzog 2015 (cited on [[obfuscation]]) argues asymmetric power means individuals *cannot* respond rationally — they lack information, resources, or legal standing. **Resolution per [[obfuscation-strategic-readout]]:** these are orthogonal, not contradictory. Strategic Classification provides the *equilibrium model* that explains why obfuscation-by-response works or fails. Richards & Hartzog provides the *political counter-argument* that even if equilibrium gaming is theoretically sound, it is not a substitute for legal / structural reform.

**Milli et al. 2019's social-cost result is the strongest theoretical argument for not deploying obfuscation as a sole lever.** It does not invalidate the lever — it bounds the conditions under which the lever is durable for equity-conscious deployment.

## Source

- Hardt, Megiddo, Papadimitriou & Wootters. 2016. *Strategic Classification*. ITCS 2016; arXiv 1506.06980. Captured: `raw/research/clawnet-adjacent-methods/15-strategic-classification-hardt-2016.md` + `04-strategic-classification-hardt-2016-abs.md`. Trust tag: peer-reviewed ITCS, foundational paper.
- *Contextual Dynamic Pricing with Strategic Buyers*. arXiv 2307.04055. Captured: `raw/research/clawnet-adjacent-methods/18-contextual-pricing-strategic-buyers.md` + `05-contextual-pricing-strategic-buyers-abs.md`. Trust tag: arXiv preprint, theoretical extension to pricing setting.
- Milli, Miller, Dragan & Hardt. 2019. *The Social Cost of Strategic Classification*. FAccT '19; arXiv 1808.08460. Captured: `raw/research/clawnet-adjacent-methods/17-social-cost-strategic-classification.md` + `06-social-cost-strategic-classification-abs.md`. Trust tag: peer-reviewed FAccT, foundational equity counter-argument.

## Related

- [[obfuscation]] — mechanism page for the consumer-side action
- [[obfuscation-strategic-readout]] — strategy readout incorporating B2 (adaptive-seller caveat) + B3 (disparate-impact externality)
- [[algorithmic-collective-action]] — coordinated counterpart
- [[the-firms-view]] — §3 (robust pricing) + §4 (disparate-impact externality)
- [[pricing-algorithm-taxonomy]] — Family 1 + Family 3 are the directly affected pricing-algorithm classes
- [[browser-fingerprinting]] — per-attribute engineering instantiation
- [[possible-strategic-levers]] — strategy-layer lever inventory (cluster #6, #7, #10, #11 anchored here)
- [[data-disruption-strategy-map]] — strategy matrix (§L1 obfuscation row updated with adaptive-seller + equity externality caveats)
