# PolySwarm — Multi-Agent LLM Trading Framework

Barot & Borkhatariya (2026) — "PolySwarm: A Multi-Agent LLM Framework for Prediction Market Trading and Latency Arbitrage" (arXiv 2604.03888) — present a system design for a 50-LLM-persona swarm with confidence-weighted Bayesian aggregation, KL/JS-divergence-based inefficiency detection, and a CEX-to-DEX latency arbitrage module targeting Polymarket. The framework is **architectural, not empirical**: the paper reports no live or paper-traded P&L, no win-rates, no realized Brier scores against ground-truth outcomes. The captured material describes equations, system blocks, and reference benchmarks; it does *not* validate the framework against actual Polymarket resolutions.

**The latency thesis directly conflicts with [[polymarket-liquidity-evolution]]** — Tsang & Yang (2026) document Trump YES arb half-life of 0.74 minutes by October 2024 on mature high-liquidity markets, whereas PolySwarm's latency module assumes "several minutes" of exploitable human reaction lag. The framework is best read as **applicable to thin / newly-listed / low-liquidity markets only** — i.e., the immature-market regime that is the wiki's stated edge-finding focus. For mature high-liquidity markets the latency window has effectively closed.

## Architecture (Sec. 3)

(Source: `raw/research/polymarket-market-trends-and-llm-edge/03-polyswarm-multiagent.md`.)

- **Persona pool:** 50 LLM personas defined with diverse priors, knowledge frames, and reasoning styles. **25 sampled per scan** to balance diversity and inference cost; agents do **not** communicate during inference (preserves independent draws for Bayesian aggregation).
- **Market scan loop:** 5-second REST polling of Polymarket Gamma API. Stated as "the practical resolution limit of Polymarket's REST API." Structural lower bound on execution latency is ~2 s — Polygon PoS block time.
- **Inputs per agent:** market title + resolution criteria + chain-of-thought structured prompt. Crucially, **market-implied probability is withheld** from individual agents — it is incorporated only at the Bayesian-aggregation stage. This avoids the "agents anchor on the market" failure mode that would collapse swarm diversity.
- **Model deployment:** frontier models (GPT-4, Claude 3 Opus) cited as default; Ollama (local LLaMA/Mistral) offered as cost-latency tradeoff. **Cost (frontier configuration):** "thousands of dollars per day" for 50 agents × hundreds of markets. SQLite response cache with configurable TTL is the primary cost-mitigation lever for stable markets.
- **Persistence and rate limits:** Gamma API polling cadence and per-market state caching are the rate-limit gating; not detailed numerically in the captured material.

## Equations

### Bayesian aggregation (Eqs. 1–2)

Confidence-weighted swarm probability:

```
p_swarm = Σᵢ (wᵢ · pᵢ) / Σᵢ wᵢ              — Eq. 1
```

where `wᵢ` is per-agent reliability/confidence weight and `pᵢ` is the agent's probability estimate over the 25 sampled agents.

Bayesian mixture with market prior:

```
p_combined = 0.70 · p_swarm + 0.30 · p_market        — Eq. 2
```

The 70/30 weight is asserted as a "tunable hyperparameter" with no optimization data presented. **Convergence to the same 70/30 ratio** appears in `[[mention-markets]]` (Kim et al. MixMCP `α = 0.7` for the *market* weight, not the swarm weight — i.e., the ratios are reversed). The two papers' opposite weighting on the market prior is a notable disagreement that the captured material does not reconcile. Operational reading: **the right market-prior weight is regime-dependent** — for thin/illiquid markets where the market price is itself noisy, weight the swarm more (this paper's 30% market); for mature markets where the market price is highly informative, weight the market more (Kim et al.'s 70% market).

### Entry gate (Eq. 3)

EV computed against current market odds:

```
EV = p_combined · b − (1 − p_combined)        — Eq. 3
```

where `b` is the net decimal odds of YES implied by the current market price.

**Gate:** `EV > 5%` (configurable) AND swarm standard deviation `< 30%`. The swarm-stdev gate is a disagreement filter: when the 25 agents disagree wildly, the aggregate posterior is unreliable; PolySwarm abstains.

### Inefficiency scores (Eqs. 4–5)

```
D_KL(P ∥ Q) = Σ P(x) log( P(x) / Q(x) )       — Eq. 4
D_JS(P ∥ Q) = ½ D_KL(P ∥ M) + ½ D_KL(Q ∥ M),  M = ½(P + Q)   — Eq. 5
```

Used as **inefficiency-detection signals**: `P` is the swarm distribution, `Q` is the market-implied distribution. `D_JS` is bounded in `[0, log 2]`, symmetric, and used as the primary score. Large `D_JS` → swarm strongly disagrees with market → candidate inefficiency.

### Position sizing — quarter-Kelly (Eq. 6)

```
f* = (p · b − (1 − p)) / b                    — Eq. 6 (standard Kelly)
f_actual = 0.25 · f*                          — quarter-Kelly
```

Hard cap: `MAX_POSITION_USDC` (default $10 per trade). The combination of quarter-Kelly + low absolute cap reflects awareness of the limits-to-arbitrage depth constraints documented in `[[single-market-arbitrage-empirics]]` — even with a correct edge, deep deployment is bounded.

### Calibration benchmarks (Eqs. 7–8)

```
BS = (1/N) Σ (f_t − o_t)²                     — Brier, Eq. 7
LL = − (1/N) Σ [o_t log f_t + (1 − o_t) log(1 − f_t)]   — Log-loss, Eq. 8
```

Reference values cited:
- **Uniform forecaster:** Brier = 0.25 (assigning p = 0.5 everywhere).
- **Human superforecaster** (Tetlock & Gardner): Brier = 0.10–0.18.

The paper claims "swarm aggregation consistently outperforms single-model baselines in probability calibration on Polymarket prediction tasks" but **no specific Brier numbers, sample sizes, or time windows are reported** in the captured material. Treat the claim as an architectural intuition, not validated evidence.

## Three strategy modules

### 1. Negation-pair arbitrage

Two semantically matched markets covering event `E` and `¬E` with `P(E) + P(¬E) ≠ 1` beyond a configurable threshold. Detection: semantic similarity matching on title strings → compute implied probability sum → flag deviations.

This is a subtype of **Market Rebalancing Arbitrage** as formally defined in `[[arbitrage-taxonomy]]` (Saguillo et al. Def. 3): `Σᵢ val(Yᵢ, t) ≠ 1` on a NegRisk market. PolySwarm's contribution is the *semantic-match detection*, not the arbitrage definition itself.

### 2. CEX-to-DEX latency arbitrage

```
p_cex = Φ(ln(S / K) / (σ · √T))
```

Black-Scholes-derived implied probability for a Polymarket crypto-price contract, where `S` = spot, `K` = strike, `σ` = hourly vol, `T` = time-to-expiry (hours). PolySwarm compares stale `p_poly` against fresh `p_cex` and trades the divergence.

**Scope constraint:** **crypto-price contracts only**. The formula requires a liquid CEX reference price; political/macro/sports markets have no analogous `p_cex`. The paper's title says "latency arbitrage" broadly, but the implementation is narrow.

**Latency thesis caveat (the load-bearing conflict).** PolySwarm assumes "several minutes" of human reaction lag between CEX price events and full Polymarket price incorporation. Per `[[polymarket-liquidity-evolution]]`, by October 2024 the Trump YES arb half-life had compressed to 0.74 minutes — automated participants close arbitrage windows in under a minute on mature markets. The PolySwarm latency assumption holds at most in:
- Newly-listed markets in the first few weeks (per the maturation trajectory).
- Markets that have lower 24h volume (consistent with the wiki's emerging-markets focus).
- Edge cases where CEX moves trigger a Polymarket re-quote that the swarm can front-run within the 5-second scan loop.

For high-volume political markets in the days before resolution, the latency thesis is **not currently empirically defensible** from the captured corpus.

### 3. Cross-market Bayesian consistency

For exhaustive mutually-exclusive outcome sets (e.g., quarterly GDP categories), enforce `Σ = 1` — violations → position in underpriced partitions. For conditional-probability inconsistencies (e.g., `P(B | A)` against unconditional `P(A)`, `P(B)`), flag as structural inefficiency.

This is structurally adjacent to **Combinatorial Arbitrage** in `[[arbitrage-taxonomy]]` (Saguillo et al. Def. 4), which requires *semantic dependence detection* across markets. PolySwarm's Bayesian-consistency angle adds the conditional-probability check, which Saguillo's pipeline does not explicitly do.

## Calibration and validation status

(`raw/research/polymarket-market-trends-and-llm-edge/03-polyswarm-multiagent.md`.)

- **No empirical P&L.** No trade counts, no win rates, no realized returns reported in the captured text.
- **Calibration benchmarks** cited (Tetlock superforecaster Brier 0.10–0.18) but no measured Brier reported for PolySwarm itself.
- **In-sample / out-of-sample status: ambiguous.** Paper explicitly warns about LLM training-cutoff contamination but does not state whether its own evaluation enforces a temporal-filter discipline (see `[[llm-epistemic-calibration]]` for the proper methodology — KalshiBench's `D_filtered = {(q, y) : t_close(q) > max_m t_cutoff(m)}` rule).
- **70/30 weight unjustified.** Asserted as "tunable hyperparameter"; no sensitivity analysis, no held-out optimization. Operator should re-tune on their own data.

## How to use this framework

Given the validation status:

1. **Treat as a reference architecture, not a deployable system.** The Eqs. 1–8 above are reasonable building blocks; the system as specified has not been proven to make money on Polymarket.
2. **Apply selectively to immature markets.** The latency thesis only stands up in thin/newly-listed regimes per the conflict with `[[polymarket-liquidity-evolution]]`. Use this framework on markets in the wiki's stated edge-finding zone (early lifecycle, mid-maturity); do not deploy against mature high-volume markets where competitive automation has compressed the window below the 5-second scan cadence.
3. **Replace the 70/30 with measured weight.** Either Kim et al.'s reversed 30/70 (see `[[mention-markets]]`) or a per-category optimized weight. The "right" market-prior weight depends on whether the market price is informative (mature markets) or noisy (thin markets).
4. **Cross-validate with `[[llm-epistemic-calibration]]`'s post-hoc-calibration discipline.** Raw LLM confidence scores are systematically overconfident; a swarm doesn't fix this unless individual agents have been calibrated.
5. **For the latency arb module specifically:** crypto-price contracts only; expect competing automated participants; the 5-second scan ceiling is a hard floor on response time.

## Source

- `raw/research/polymarket-market-trends-and-llm-edge/03-polyswarm-multiagent.md` — Barot & Borkhatariya (2026), "PolySwarm: A Multi-Agent LLM Framework for Prediction Market Trading and Latency Arbitrage" (arXiv 2604.03888). All equations Sec. 3; architecture spec; reference calibration benchmarks; no empirical P&L.

## Related

- [[polymarket-liquidity-evolution]]
- [[arbitrage-taxonomy]]
- [[single-market-arbitrage-empirics]]
- [[combinatorial-arbitrage-empirics]]
- [[mention-markets]]
- [[llm-forecasting-by-domain]]
- [[llm-epistemic-calibration]]
- [[market-maker-handbook-prediction-markets]]
- [[logit-jump-diffusion-kernel]]
