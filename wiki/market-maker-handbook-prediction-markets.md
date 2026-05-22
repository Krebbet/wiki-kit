# Market-Maker Handbook — Prediction Markets

Practitioner layer of the [[logit-jump-diffusion-kernel]]: inventory-aware quoting in logit units (Avellaneda–Stoikov adapted), cross-event β-hedge, calendar variance hedge, anti-pick-off / toxicity guards, P&L attribution by risk bucket, and a day-one quote menu. All formulas below are from Sec. 4 of Dalen / Daedalus Research (2025).

**Same caveat as the kernel page applies:** the quoting and hedging prescriptions are derived from a kernel whose only quantitative validation is on synthetic data drawn from the kernel's own distribution. Treat as a *structured starting point* for real-data experimentation, not a battle-tested handbook. Empirical realism is one of the wiki's open research directions.

## Inventory-aware quoting (Eqs. 8–9)

Quote in log-odds space. Let `x_t = logit(p_t)` (mid in logit units), `q_t` inventory (contracts long − short), `γ` risk aversion, `T − t` risk horizon, `σ_b²` short-horizon belief variance, `k` exponential arrival-rate decay, `A` baseline arrival intensity.

**Reservation quote** (skew due to inventory):

```
r_x(t) = x_t − q_t · γ · σ_b² · (T − t)                     (8)
```

**Optimal half-spread (in x):**

```
2 δ_x(t) ≈ γ σ_b² (T − t) + (2 / k) log(1 + γ / k)          (9)
```

**Post quotes:**

```
x_bid = r_x − δ_x
x_ask = r_x + δ_x
```

**Map back to price space:**

```
p_bid = S(x_bid),  p_ask = S(x_ask)
δ_p ≈ S′(x) · δ_x = p(1 − p) · δ_x
```

The Jacobian `p(1 − p)` automatically compresses quoted spreads as `p → 0` or `p → 1` — useful for thin/tail outcomes where SF1's longshot premium ([[polymarket-microstructure]]) suggests spreads are otherwise structurally wide due to inventory risk.

**Assumptions:** order-arrival intensity decays exponentially in distance from mid, `λ(δ) = A exp(−k δ)`; standard A–S asymptotics. Applies to single-event vanilla contracts (binary YES/NO).

## Inventory cap near boundaries

```
|q_t| ≤ q_max(t) ∝ 1 / max{ S′(x_t), ε }
```

Prevents over-exposure as `S′(x) → 0` near `p ≈ 0, 1`. Operationally: when quoting a market that drifts toward a tail, *automatically reduce the allowed inventory limit*, not just widen quotes.

## Cross-event β-hedge (Sec. 4.4)

Instantaneous diffusive hedge ratio of event `i` against event `j`:

```
β_{i ← j}  ≈  Cov(dp_i, dp_j) / Var(dp_j)
            ≈  (S_i′ / S_j′) · ρ_{ij}
```

Apply shrinkage: `β̃ = α β`, `α ∈ [0.5, 1)`, clamp when `S_k′ → 0` (i.e. near tails). When co-jump covariance is material (election night, major scheduled news), add the co-jump correction:

```
Δβ_{ij}^{jump}  ≈  ∫ Δp_i Δp_j ν_{ij,t}(dz_i, dz_j) / [ (S_j′)² σ_{b,j}² ]
```

Strategy condition: the diffusive hedge alone over-hedges around known jump windows. The recipe is "over-hedge diffusive correlation around known jump windows; carry first-passage notes to absorb threshold gaps" — i.e., split into two instruments: a diffusive hedge sized for normal regimes, and a discrete payoff (first-passage / barrier) that pays off if the threshold breaks.

## Calendar hedge via variance strips (Sec. 4.3)

Belief-variance exposure `ν̂_b(t, Δ)` is the book's directional sensitivity to `σ_b` over the next interval `Δ`. Notional for an `x`-variance strip:

```
N^{x-var}  ≈  − ν̂_b(t, Δ) / (∂ K_{t, t+Δ}^{x-var} / ∂σ_b)  ∝  − ν̂_b(t, Δ) / σ_b
```

Use short windows around scheduled data releases (where `σ_b` is spiky); longer windows for slow resolution decay. If listed variance products are unavailable, synthesise with adjacent maturities or related events.

## Anti pick-off / toxicity guards

Three discrete triggers (Sec. 4.5, summarised):

1. **VPIN-style short-horizon order-imbalance spike** → widen `δ_x` or pull quotes.
2. **Scheduled announcement approach** → ramp `γ` and / or `T − t` in (9); pause on unscheduled-jump detectors.
3. **Adverse mid drift / queue position loss** → cancel-replace.

These are the kill-switch layer. The handbook positions them as essential: without them, the A–S quoting framework gets gored by toxic flow that doesn't satisfy the exponential-decay assumption.

## P&L attribution (Sec. 4.6)

```
dΠ ≈ Δ_x dp + ½ Γ_x (dp)² + ν_b dσ_b + Σ_j ν_ρ(j) dρ_{ij} + (jump ΔP terms)
```

Five risk buckets:

1. Directional (`Δ_x`)
2. Curvature / news (`Γ_x`)
3. Information intensity (`ν_b` + jump second moments)
4. Cross-event (`ν_ρ` + co-jump covariance)
5. Jump tail (residual)

Operational use: at end-of-day, attribute the day's P&L to each bucket; risk-adjusted compensation should be measured per-bucket, not in aggregate, to incentivise the right hedge discipline.

## Belief-vega for p-variance (Sec. 4.1)

```
ν_b  ∝  [ p(1 − p) ]²  ·  σ_b
```

Reflects the Jacobian `S′(x)² = (p(1 − p))²` from the `K^{p-var}` formula in [[logit-jump-diffusion-kernel]]. Practical: `ν_b` near the boundaries `p ≈ 0, 1` is *quartically* suppressed by `[p(1 − p)]²`. Boundary markets are weakly variance-exposed; this is structural, not a measurement artefact.

## Day-one quote menu (Sec. 4.8)

A starter book for an operator deploying this framework:

1. Vanilla event contracts (tightest where `S′(x)` largest — i.e., near `p = 0.5`).
2. `x`-variance strips around scheduled news.
3. A few liquid correlation strikes between coupled events.
4. Corridor variance centred on `p ∈ [0.35, 0.65]` for high-flow markets.

The menu is consistent with the structural quoting analysis: concentrate where Greeks are largest, hedge where co-movement is material, and offer event-derivatives (variance / correlation / corridor) as natural extensions once vanilla coverage is in place.

## How this connects to the empirics

The handbook is theoretical. The empirical pages tell us:

- [[polymarket-microstructure]] — longshot spread premium (SF1) suggests the inventory-cap section above is *load-bearing* in practice. SF8 depth-decay suggests `(T − t)` in Eq. 9 has to be calibrated against the within-market depth trajectory, not just notional time-to-resolution.
- [[polymarket-liquidity-evolution]] — Kyle's λ 0.53 → 0.01 over a market lifespan suggests `σ_b` is dramatically non-stationary; a static calibration window will misprice quotes in early-market regimes.
- [[arbitrage-taxonomy]] — the existence of profitable arb (~$40M extracted) means *some* operators are systematically picking off mid-quoted books. The toxicity guards above are not optional.

These cross-references mark the open territory: the handbook prescribes a discipline, the empirics tell us where that discipline must be tightened beyond the synthetic-data validation.

## Math summary — quoting in one block

```
Reservation:   r_x = x − q · γ · σ_b² · (T − t)              (8)
Half-spread:   2δ_x ≈ γ σ_b² (T − t) + (2/k) log(1 + γ/k)   (9)
Post:          x_bid = r_x − δ_x,  x_ask = r_x + δ_x
Price-space:   δ_p ≈ p(1 − p) · δ_x
Inv. cap:      |q| ≤ q_max ∝ 1 / max{S′(x), ε}
β-hedge:       β_{i←j} ≈ (S_i′ / S_j′) · ρ_{ij}
Cal-hedge:     N^{x-var} ≈ −ν̂_b(t,Δ) / (∂K^{x-var}/∂σ_b)
P&L:           dΠ ≈ Δ_x dp + ½ Γ_x (dp)² + ν_b dσ_b + Σ ν_ρ dρ + jump
```

## Source

- `raw/research/polymarket-types-and-opportunities/06-prediction-bs-kernel.md` — Shaw Dalen / Daedalus Research, "Toward Black–Scholes for Prediction Markets: A Unified Kernel and Market-Maker's Handbook". Sec. 4 (4.1 Greeks, 4.2 A–S quoting, 4.3 calendar hedge, 4.4 cross-event β-hedge, 4.5 toxicity guards, 4.6 P&L attribution, 4.8 day-one quote menu).

## Related

- [[logit-jump-diffusion-kernel]]
- [[polymarket-microstructure]]
- [[polymarket-liquidity-evolution]]
- [[arbitrage-taxonomy]]
