# Logit Jump-Diffusion Kernel (RN-JD)

Dalen / Daedalus Research (2025) proposes a **logit jump-diffusion with risk-neutral drift** as the "Black-Scholes kernel" for prediction-market event contracts. State variable `x_t = logit(p_t)` lives on `ℝ`; price `p_t = S(x_t) ∈ (0, 1)` is a Q-martingale under a drift specifically pinned to compensate the diffusion + jump contributions to the sigmoid map. The framework yields: a calibration pipeline (filtering + EM + RN-drift enforcement), a derivative layer (variance / correlation / corridor / first-passage), and a quoting framework (see [[market-maker-handbook-prediction-markets]]).

**Critical validation caveat — read first.** All quantitative results in the paper (Table 1, MSE / MAE / QLIKE comparisons against random-walk-logit, WF/Jacobi, ARMA-GARCH) are on **synthetic data generated from the model's own RN-JD distribution**. 20 high-volume Polymarket markets are used only as a scale reference for noise calibration, not as the data-generating process under test. There is **no out-of-sample test on actual historical Polymarket prices** in the captured material. Any wiki page citing performance numbers must repeat this caveat. The framework is best read as *theoretical scaffolding* for which a real empirical validation remains future work.

## State and SDE

`x_t = logit(p_t)`, with `p_t ∈ (0, 1)` mapped to `ℝ`. Inverse: `p_t = S(x_t) = 1 / (1 + e^{−x_t})`.

SDE (Eq. 1):

```
dx_t = μ(t, x_t) dt + σ_b(t, x_t) dW_t + ∫_ℝ z Ñ(dt, dz)
```

Symbols:
- `σ_b(t, x_t)` — **belief volatility** (the tradable risk factor).
- `W_t` — standard Brownian motion.
- `Ñ(dt, dz) = N(dt, dz) − ν_t(dz) dt` — compensated jump measure.
- `ν_t` — Lévy measure satisfying `∫_ℝ min{1, z²} ν_t(dz) < ∞`.

## Risk-neutral drift (Eq. 3) — the load-bearing equation

The drift `μ(t, x)` is pinned so that `p_t = S(x_t)` is a Q-martingale:

```
μ(t, x) = − [ ½ S″(x) σ_b²(t, x) + ∫_ℝ (S(x + z) − S(x) − S′(x) χ(z)) ν_t(dz) ] / S′(x)
```

Auxiliary identities used throughout:
- `S′(x) = p (1 − p)`
- `S″(x) = p (1 − p)(1 − 2p)`
- `χ(z) = z · 1_{|z| < 1}` — truncation function for the jump compensator

After drift is pinned, the **only tradable risk factors** are: `σ_b` (belief vol), jump intensity and moments (via `ν_t`), and cross-event dependence `ρ_{ij}`.

## Multi-event covariance (Eq. 4, short-maturity frozen-state)

```
Cov(dp_i, dp_j) |_t  ≈  S_i′ S_j′ σ_{b,i} σ_{b,j} ρ_{ij}(t) dt  +  ∫_{ℝ²} Δp_i Δp_j ν_{ij,t}(dz_i, dz_j) dt
```

First term — diffusive covariation. Second term — co-jump aggregation. `ρ_{ij}(t) = corr(dW_i, dW_j)`.

## PIDE for exotic pricing (Eq. 7)

Backward equation for terminal payoff `g(x_T)`:

```
∂_t V + μ(t, x) ∂_x V + ½ σ_b²(t, x) ∂_{xx} V + ∫_ℝ [V(t, x + z) − V(t, x) − ∂_x V · χ(z)] ν_t(dz) = 0
V(T, x) = g(x)
```

Solvers cited: finite-difference with fast convolution for the jump integral; Fourier methods for constant/affine coefficients; Monte Carlo with variance reduction.

## Greeks in the logit domain

```
Δ_x  = ∂V/∂x      = S′(x)  = p(1 − p)
Γ_x  = ∂²V/∂x²    = S″(x)  = p(1 − p)(1 − 2p)
ν_b  = ∂V/∂σ_b              (belief-vega)
ν_ρ  = ∂V/∂ρ_{ij}           (correlation-vega)
```

Near `p → 0, 1`: `Δ_x → 0`; curvature peaks in the swing zone `p ≈ 0.5`. P&L attribution per period (Sec. 4.6):

```
dΠ ≈ Δ_x dp + ½ Γ_x (dp)² + ν_b dσ_b + Σ_j ν_ρ(j) dρ_{ij} + (jump ΔP terms)
```

Risk buckets: directional (`Δ_x`), curvature/news (`Γ_x`), information intensity (`ν_b` + jump second moments), cross-event (`ν_ρ` + co-jump covariance).

## Belief variance / corridor / first-passage products

### Belief variance swap on x (Eq. 5)

Fair strike:

```
K_{t,T}^{x-var}  ≈  ∫_t^T σ_b²(u) du  +  ∫_t^T λ(u) E[z²(u)] du
```

Parallel to classical variance-swap theory. The two terms separate diffusive QV and jump contribution.

### Belief variance swap on p (Eq. 6, short-maturity frozen-state)

```
K_{t, t+Δ}^{p-var}  ≈  [p_t (1 − p_t)]² · [ ∫_t^{t+Δ} σ_b²(u) du  +  ∫_t^{t+Δ} ∫_ℝ (S(x_t + z) − S(x_t))² ν_u(dz) du ]
```

Prefactor `[p(1 − p)]²` is `(S′(x))²` from Itô on the sigmoid. Second term captures jump contribution to QV of `p` (rather than `x`).

### Realised QV of x

```
QV_{t,T}^x  =  ∫_t^T σ_b²(u, x_u) du  +  Σ_{t < u ≤ T} (Δx_u)²
```

## Calibration pipeline (Sec. 5)

1. **Data conditioning.** Trade-weighted mid; clamp `p ∈ [ε, 1 − ε]` (e.g. `ε = 1e-5`); logit transform; resample to uniform grid (100 ms – 1 s); outlier hygiene.
2. **Heteroskedastic observation model** (Eq. 10): `y_t = logit(p̃_t) = x_t + η_t`, with
   ```
   Var(η_t) = σ_η²(t) = a_0 + a_1 s_t² + a_2 d_t^{-1} + a_3 r_t + a_4 ι_t²
   ```
   where `s_t` = spread, `d_t` = depth, `r_t` = trade rate, `ι_t` = order imbalance. Fitted by robust regression on short-horizon squared microstructure innovations (Hasbrouck-style).
3. **State filtering.** Gaussian state-space Kalman filter/smoother on `x`; unscented KF or particle smoother when `p` is pinned near `0/1` or jumps are very frequent.
4. **EM for diffusion / jump separation** (Eqs. 11–12). Increment mixture:
   ```
   Δx_t ~ N(μ_t Δ, σ_b²(t) Δ)   with prob 1 − λ_t Δ
   Δx_t ~ f_J(·; θ_t)            with prob λ_t Δ
   ```
   - E-step: `γ_t = λ_t Δ ψ_t / (λ_t Δ ψ_t + (1 − λ_t Δ) φ_t)`.
   - M-step:
     ```
     σ̂_b²(t) ← [ Σ (1 − γ_t)(Δx̂_t − μ_t Δ)² / Σ (1 − γ_t) ] / Δ
     λ̂(t)   ← (1/Δ)(1/|B|) Σ γ_t
     ŝ_J²(t) ← Σ γ_t (Δx̂_t)² / Σ γ_t
     ```
5. **RN drift enforcement** (Eq. 14). After each EM iteration, recompute `μ(t, x)` from Eq. 3, with jump compensation `E[·]` approximated by MC (600 draws/step, symmetric Gaussian jumps); EWMA-smooth `μ`; cap at `|0.25| s⁻¹`. Re-run smoother. **1–2 outer loops sufficient.**
6. **Surface construction.** Penalized least-squares spline over `(τ, m)` grid (maturity × moneyness analog) with shape constraints: nonnegativity, edge stability, term smoothness. Uncertainty bands from sandwich / bootstrap.
7. **Cross-event dependence.** De-jumped diffusive correlations estimated on intervals where `max(γ_i, γ_j) < τ_J`; same spline smoothing. Co-jumps tested via high-frequency statistics.

**Inputs required:** mid / bid-ask / trade streams.
**Computational cost:** `O(N × EM_steps)` per event for filtering; PIDE/MC for exotic pricing.

## Synthetic experiment (Sec. 6) — what was actually measured

- Platform: Polymarket (20 high-volume markets used only as **scale reference** for noise calibration).
- Data: **synthetic RN-consistent paths**, `N = 6000` steps at 1 Hz (~100 min equivalent), corrupted with heteroskedastic observation noise mimicking spread / depth variation.
- **Not real Polymarket data.** No multi-month real backtest.
- Task: causal forward-sum forecast of next-window realised logit variance, `H = 60 s`.
- Metric: MSE, MAE, log-MSE, **QLIKE** (Eq. 13). QLIKE definition: `QLIKE = Σ [RV_t / V̂_t − log(RV_t / V̂_t) − 1]`.
- Split: train / validation / test (thirds); `c_J` tuned on validation by QLIKE; evaluation on test only.

Table 1 results (test set, `H = 60 s`):

| Model | MSE_all | MAE_all | QLIKE_all |
|---|---|---|---|
| **RN-JD (causal)** | **70.28** | **1.588** | 1.46 |
| RW-logit (const σ) | 77.41 | **1.163** | 4.73 |
| Logit (const σ) | 76.75 | 2.078 | 2.66 |
| WF / Jacobi (mapped) | 1.71 × 10¹⁷ | 3.67 × 10⁷ | 1.95 |
| ARMA-GARCH (mapped) | 1.07 × 10¹⁹ | 5.33 × 10⁸ | **0.796** |

Reading: RN-JD wins MSE and MAE; ARMA-GARCH wins QLIKE but produces **catastrophically large** MSE and MAE due to instability when mapped from `p`-space to logit space. Same instability for WF / Jacobi. **Interpret with discipline:** the synthetic data is generated from the RN-JD model's own distribution, so RN-JD is being tested in a regime where its assumptions exactly hold by construction. This is an in-sample test of the calibration pipeline, not a model-comparison against an unknown DGP.

## What this framework does NOT do

- No empirical inefficiency / mispricing pattern documented. The paper is normative / prescriptive (proposing a kernel + pipeline + product layer), not empirical.
- No real-data backtest. The 20-market scale reference is for noise calibration only.
- No coverage of UMA oracle or resolution mechanics — see [[uma-optimistic-oracle]].
- No coverage of execution-venue mechanics — see [[polymarket-architecture]] for CLOB / NegRisk details.

## Math summary — the kernel in one block

```
State:           x_t = logit(p_t)                                              p_t = S(x_t) = 1/(1+e^{-x_t})
SDE (Eq. 1):     dx_t = μ(t,x) dt + σ_b(t,x) dW_t + ∫_ℝ z Ñ(dt, dz)
RN drift (Eq. 3): μ(t,x) = −[½ S″(x) σ_b² + ∫(S(x+z)−S(x)−S′(x)χ(z)) ν_t(dz)] / S′(x)
Greeks (Sec.4.1): Δ_x = S′(x) = p(1−p);    Γ_x = S″(x) = p(1−p)(1−2p)
Cov  (Eq. 4):    Cov(dp_i, dp_j) ≈ S_i′ S_j′ σ_bi σ_bj ρ_ij dt + ∫_{ℝ²} Δp_i Δp_j ν_{ij,t}(dz) dt
PIDE (Eq. 7):    ∂_t V + μ ∂_x V + ½ σ_b² ∂_xx V + ∫[V(x+z)−V(x)−∂_x V·χ(z)] ν dz = 0
Variance swap (p, Eq. 6):
                 K^{p-var}_{t,t+Δ} ≈ [p(1−p)]² [ ∫ σ_b² du + ∫∫ (S(x+z)−S(x))² ν du ]
```

## Source

- `raw/research/polymarket-types-and-opportunities/06-prediction-bs-kernel.md` — Shaw Dalen / Daedalus Research, "Toward Black–Scholes for Prediction Markets: A Unified Kernel and Market-Maker's Handbook". Sections 3 (kernel definition), 4 (Greeks, P&L attribution, quoting framework), 5 (calibration pipeline), 6 (synthetic experiment, Table 1).

## Related

- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[polymarket-architecture]]
- [[polymarket-liquidity-evolution]]
