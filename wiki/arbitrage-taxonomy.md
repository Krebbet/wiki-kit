# Arbitrage Taxonomy (Polymarket)

Saguillo, Ghafouri, Kiffer et al. (2026) — "Unravelling the Probabilistic Forest" — provide the canonical taxonomy of arbitrage on Polymarket: **Market Rebalancing Arbitrage (MRA)** within a market, and **Combinatorial Arbitrage** across two dependent markets. Both classes derive from the same $1.00-Rule structure underwritten by Polymarket's CTF primitives — `splitPosition`, `mergePositions`, `convertPositions` — see [[polymarket-architecture]]. Empirical anchor: ~$39.6M extracted across both types between April 1, 2024 and April 1, 2025, with **41% of 17,218 conditions** offering at least one MRA opportunity at some point in the measurement window.

All strategies below are **non-atomic on the CLOB** — multi-leg execution exposes the operator to leg-fill risk. Profitability formulas state guaranteed payoff *conditional* on all legs filling at the quoted prices.

## Definitions

### Definition 1 — Single market outcome (§3.1.1)

A market `M = {C₁, C₂, …, Cₙ}` of `n` conditions is **exhaustive** iff `|V| = n` and `∀v ∈ V : Σ_{cᵢ ∈ v} cᵢ = 1`, where `V` is the set of resolution vectors `v = ⟨c₁, …, cₙ⟩` with `cⱼ ∈ {0, 1}`. Equivalently: exactly one condition resolves true.

### Definition 2 — Two-market outcome dependence (§3.1.2)

Two markets `M1` (size `n`) and `M2` (size `m`) are **independent** iff `|V₁ × V₂| = n · m`, **dependent** otherwise. When dependent, there exist **dependent subsets** `S ⊂ M1` and `S′ ⊂ M2` such that `∀v ∈ V₁ × V₂ : Σ_{cᵢ ∈ S} cᵢ = Σ_{c′ⱼ ∈ S′} c′ⱼ` — i.e., across all jointly-feasible resolutions, the count of TRUE conditions in `S` equals the count in `S′`.

### Definition 3 — Market Rebalancing Arbitrage (§3.2.1)

Within a single market `M`:

- **Long opportunity at time `t`:** `Σᵢ val(Yᵢ, t) < 1`. Profit at resolution: `1 − Σᵢ val(Yᵢ, t)`.
- **Short opportunity at time `t`:** `Σᵢ val(Yᵢ, t) > 1`. Profit at resolution: `Σᵢ val(Yᵢ, t) − 1`.

Symbols: `val(Yᵢ, t)` = price of YES token for condition `Cᵢ` at time `t`; `Nᵢ` = NO token; `n` = number of conditions.

### Definition 4 — Combinatorial Arbitrage (§3.2.2)

Given dependent markets `M1`, `M2` with dependent subsets `S ⊂ M1`, `S′ ⊂ M2`:

- If `Σ_{c ∈ S} val(T_c, t) < Σ_{c′ ∈ S′} val(T_{c′}, t)`: hold YES for `S` and YES for the complement of `S′`.
- If `Σ_{c ∈ S} val(T_c, t) > Σ_{c′ ∈ S′} val(T_{c′}, t)`: hold YES for the complement of `S` and YES for `S′`.

Profit: `|Σ_{c ∈ S} val(T_c, t) − Σ_{c′ ∈ S′} val(T_{c′}, t)|`.

**Asymmetry footnote (§3.2.2, fn 7):** Only YES positions across complementary subsets are considered; NO positions cannot be substituted because, in a NegRisk multi-condition market, multiple NOs can be simultaneously true by design — the symmetry that holds for binary single-condition pairs breaks.

## Strategies and execution paths

### Long MRA

1. Observe `Σᵢ val(Yᵢ, t) < 1`.
2. Buy one unit of each YES position.
3. At resolution, exactly one YES pays $1; sum of acquisition costs `< 1`, so profit = `1 − Σᵢ val(Yᵢ, t)`.

### Short MRA — Path A (buy all NOs)

1. Observe `Σᵢ val(Yᵢ, t) > 1`.
2. Buy one unit of each NO position. Sum of NO resolutions = `n − 1`.
3. Profit = `n − Σᵢ val(Nᵢ, t) = Σᵢ val(Yᵢ, t) − 1`.

### Short MRA — Path B (faster: SPLIT + sell YES)

1. Observe `Σᵢ val(Yᵢ, t) > 1`.
2. For each condition, call `splitPosition` (deposit 1 USDC, mint one YES + one NO complement) → see [[polymarket-architecture]] for the primitive.
3. Sell all newly-minted YES tokens at market.
4. Profit `= Σᵢ val(Yᵢ, t) − 1` realised immediately (vs. waiting for resolution in Path A).

Empirically (§7.3) Path A's *buying NO* variant dominated realised extraction in the measurement window — Polymarket itself flagged unusual NO-buying activity in public communications.

### Single-condition arbitrage (degenerate Long/Short MRA)

For a single binary condition (n=1):

- `YES + NO < 1` → buy both.
- `YES + NO > 1` → SPLIT + sell both.

Counted separately in §6.1 of the source from multi-condition MRA.

### Combinatorial Arbitrage execution

The dependent-subset structure must be identified first (semantic, not numeric — see §5 of the source for the LLM-based detection pipeline using DeepSeek-R1-Distill-Qwen-32B and Linq-Embed-Mistral embeddings; not all candidate-pairs that share a topic and end-date are truly dependent). Once identified, the price-imbalance condition in Definition 4 above triggers the cross-market buy.

## Empirical anchors

(Source: `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §6–7. Period: April 1, 2024 – April 1, 2025. Platform: Polymarket. In-sample; no out-of-sample test.)

| Class | Conditions / pairs | Opportunity rate | Median profit-per-$ | Total realised |
|---|---|---|---|---|
| Single-condition MRA | 17,218 conditions | 41% had ≥1 opportunity | ~$0.60 | $5.9M (buy < $1) + $4.7M (sell > $1) |
| Multi-condition (NegRisk) MRA | 1,578 NegRisk markets | 42% had ≥1 opportunity | ~$0.40 (long and short) | $17.3M (buy NO) + $11.1M (buy YES) + small short components |
| Combinatorial | 46,360 pairs checked; 1,576 surviving topic/date filter; 13 confirmed dependent (all 2024 election) | varies | average per-opp ~$100 | $60K, $18K, $16K, $0.6K (top 4 pairs) |
| **Total realised** | — | — | — | **~$39.6M** |

**By topic (§6.2):** Politics dominates extracted value (concentrated around Nov 5 2024 and Aug 2024 Dem VP/presidential pick). Sports has the **highest opportunity frequency** but is **largely absent** from realised extraction — flagged in the source as "possibly underexplored venue". This is the most operationally interesting line item in the table for the wiki's edge-finding goal.

**Profit filter** used in the source: opportunities with `< $0.05 profit per dollar` excluded to focus on higher-reward cases given execution risk (§6, fn 11).

**Top arbitrageur** (§7.4): wallet `0xd218e4…` extracted $2.0M in 4,049 transactions. Top-10 listed in source Table 1.

**Bot-like profile** (§7.4, Figure 12): top accounts show a log-linear profit-vs-transaction curve consistent with automated execution. Manual operators are not on this leaderboard.

**Edge size relative to industry volume.** The ~$39.6M total realised extraction in the Apr 2024 – Apr 2025 window is **roughly 0.06% of 2025 industry volume** ($64B, see [[platform-comparison-kalshi-polymarket]]) — and ~$20.2M of that $40M was inside the Politics topic on a window dominated by the 2024 U.S. election. Useful framing: the documented automated-arb economy is a small fraction of total flow, consistent with the bot-like top-10 leaderboard above (a small number of operators extracting a small but persistent share). It does not bound the size of *un*documented or non-arb edges (e.g., the model-based forecasting edges in [[llm-forecasting-by-domain]] and [[mention-markets]]).

## Price input — VWAP convention

Source §6 uses VWAP over one Polygon block (~2 s); last price carried forward up to 5,000 blocks (~2.5 hr) if no trades; set to 0 if still untradeable. Arbitrage assessed only when no token price exceeds **$0.95** (i.e., the market still has genuine residual uncertainty). Operational lesson: if you adopt a different price input (last-trade, mid, top-of-book ask), recompute the profit threshold; the $0.60 median is bound to *this* VWAP convention.

## Where the depth-constraint bites

The opportunity *frequency* numbers above do not translate directly into extractable size. See [[single-market-arbitrage-empirics]] and [[combinatorial-arbitrage-empirics]] for the depth-constraint empirics from the NBA study (Cheng, Yang & Zou 2026) — in the worked case, **76.9 % of combinatorial episodes had executable size constrained to ~14.8 shares average**, so the $100 cap on a per-episode budget could not be deployed. The Shleifer-Vishny (1997) limits-to-arbitrage framework applies cleanly: depth, not insight, is the binding constraint at retail scale.

## Math summary

Inline form for the canonical conditions:

```
Long MRA:           Σᵢ val(Yᵢ, t) < 1            →  profit = 1 − Σᵢ val(Yᵢ, t)
Short MRA (path A): Σᵢ val(Yᵢ, t) > 1            →  profit = Σᵢ val(Yᵢ, t) − 1 (buy all Nᵢ)
Short MRA (path B):  same condition              →  SPLIT then sell all Yᵢ, profit realised now
Comb. Arb (Def 4):   |Σ_S val(T_c) − Σ_{S′} val(T_{c′})|  =  profit
```

## Source

- `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` — Saguillo et al. (2026), "Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets". Sections 3 (definitions), 5 (LLM dependency detection), 6 (empirical inefficiencies by subtype), 7 (extracted dollar totals, top arbitrageur profile, NO-buying dominance).

## Related

- [[polymarket-architecture]]
- [[single-market-arbitrage-empirics]]
- [[combinatorial-arbitrage-empirics]]
- [[polymarket-liquidity-evolution]]
- [[uma-optimistic-oracle]]
