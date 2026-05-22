# Combinatorial Arbitrage — Empirics

Inter-market arbitrage on Polymarket (Definition 4 in [[arbitrage-taxonomy]]) requires identifying *dependent* market pairs first — pairs whose joint resolution space is constrained, so prices across them must satisfy a no-arbitrage identity. Two empirical lenses:

- **Cross-platform / U.S. 2024 election:** Saguillo et al. (2026) check **46,360 candidate pairs**, surviving topic + end-date filter narrows to **1,576**, formal-dependence detection (LLM-based) confirms **13 dependent pairs**, all from 2024 U.S. election. Per-opportunity profit ~$100 on average. Pair 4 (popular-vote winner vs popular-vote-winner-takes-presidency) had **6,630 opportunities**.
- **NBA Moneyline ↔ Spread:** Cheng, Yang, Zou (2026) document **290 active episodes** in 173 NBA games via the structural subset relation `{Δ > h} ⊂ {Δ ≥ 1}`. Median yield **101 bps in-game**; **76.9 % depth-constrained to ~14.8 shares**; **zero "Middle" jackpot realizations** in the sample.

The two studies illustrate two different routes to identifying dependence: **semantic** (LLM + embeddings, scalable to the full platform) and **structural** (the spread-vs-moneyline subset relation is a derivation, not a discovery).

## Saguillo et al. — semantic dependence detection at platform scale

Source: `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §5, §6.3.

### Dependence detection pipeline

1. **Topic filter (§4.1.1):** Linq-Embed-Mistral cosine similarity between condition-text embedding and topic-label embeddings. Topics: Politics, Economy, Technology, Crypto, Twitter, Culture, Sports. Validated at **92 % accuracy** on 100 manually labelled instances.
2. **End-date filter:** only pairs sharing the same topic AND end date are checked further. Rationale: centralised market creation means co-event markets share end dates.
3. **Market reduction (§5.1):** markets with > 4 conditions pruned to top-4 by total traded volume (YES + NO) plus a fifth "all others" catch-all (logical OR). Appendix C shows > 90 % of market liquidity is in top-4 conditions.
4. **LLM joint-resolution check (§5):** DeepSeek-R1-Distill-Qwen-32B given the union of conditions from two markets, asked to enumerate valid joint truth-value vectors. Consistency checks:
   - Valid JSON returned;
   - Exactly one TRUE per market in each vector;
   - Set size ≤ `n + m` for reduced markets of sizes `n, m`.
5. **Single-market sanity validation:** 81.45 % valid JSON rate on a single-market enumeration task — useful as a quality floor on the broader pipeline.

Without these filters: brute-force pair check is `O(2^{n+m})` over potentially huge `n + m` and over `46,360 × ...` pairs — infeasible. With the topic + end-date heuristic, the search collapses to **1,576 pairs** to LLM-check, of which **13 are confirmed dependent** in the U.S. election dataset.

### Findings

| Pair | Description | # opportunities | Realised extraction |
|---|---|---|---|
| Pair 1 | (election politics pair, source §6.3) | 176 | $15,819 |
| Pair 2 | (election politics pair) | 72 | $60,237 |
| Pair 3 | (election politics pair) | — | $629 |
| Pair 4 | popular-vote winner vs popular-vote-winner-takes-presidency | **6,630** | $18,472 |
| Pair 8 | (election politics pair) | 0 | $0 |

- Total cross-market extraction in dataset: realised values above sum to ~$95K across the four monetised pairs.
- Average per-opportunity max profit: **~$100** (suggesting total token volume per window ≈ $2K — depth-bound).
- Concentration: opportunities cluster in low-liquidity windows.
- **No arbitrage detected in the 2 NegRisk-Single pairs** — i.e., dependence between a multi-condition (NegRisk) market and a single-condition market did exist semantically but did not manifest as exploitable price deviations.

Operational note: the dependence-detection step is the *novel cost* of combinatorial arb. Once you have the dependency map, the price check (Definition 4) is constant-time per snapshot.

## Cheng, Yang, Zou — NBA Moneyline + Spread structural arbitrage

Source: `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md`.

### Structural derivation of dependence

Final point differential `Δ = S_A − S_B`, `Δ ∈ ℤ \ {0}`.

- Moneyline A (`MLA`) pays iff `Δ ≥ 1`.
- Spread A (`SpA`) pays iff `Δ > h`, where `h ≥ 1` is the spread (integer or half-integer).

`{Δ > h} ⊂ {Δ ≥ 1}` — therefore efficient pricing requires `Price(SpA) ≤ Price(MLA)`. Violation: `Bid(SpA) > Ask(MLA)` is a necessary (but not sufficient for execution) arb condition. The complementary cross-market check:

```
Ask(MLA) + Ask(SpB) < 1.00
```

where `SpB` is the spread underdog YES (a synthetic short on the overpriced spread). When holds: buy both legs for cumulative cost < $1.00, guaranteed $1.00 payout from exactly one — net profit `1.00 − Ask(MLA) − Ask(SpB)`.

This is a *derived* dependence — no LLM needed. The structural relationship comes directly from sport-market resolution rules.

### "Middle" jackpot mechanic

For `h = 1.5` (Team A ML + Team B +1.5):

| Δ | Team A ML | Team B +1.5 | Total |
|---|---|---|---|
| Δ ≥ 2 | $1.00 | $0.00 | $1.00 |
| **Δ = 1** | **$1.00** | **$1.00** | **$2.00** |
| Δ ≤ 0 | $0.00 | $1.00 | $1.00 |

When the final margin lands exactly in the spread gap, both legs pay → $2.00 on $1.00 deployed. **Empirical realization in 290 episodes: zero.** The simultaneous occurrence of pricing dislocation AND a margin in the gap proved too rare to assign meaningful probability weight in this sample. Treat the Middle jackpot as a tail upside, not a positive-EV anchor.

### Unified State Machine (synchronisation methodology)

Two asynchronous order books (Moneyline and Spread) are merged via full outer join on UTC timestamps. State imputation uses **strict forward-fill**:

```
P_M(t_n) = P_M(t_i),  where t_i = max{t ∈ T_M | t ≤ t_n}
```

This prevents look-ahead bias — only limit orders verifiably resting at moment `t_n` are used. Combined with the 500 ms phantom-arb clustering and per-phase duration capping (`C_phase = 300 s` in-game, `1800 s` pre/post-game), spurious sub-second arbs from API serialisation delay are eliminated.

### Findings

| | Value |
|---|---|
| Sample | 8.59 million discrete combinatorial states across 173 NBA games |
| Period | Feb 4 – Mar 4, 2026 |
| Active executable episodes (after post-game artefact removal) | **290** (of 523 raw candidates) |
| Median episodes per game | 2.00 |
| Time in arb (in-game) | 0.1762 % |
| Time in arb (pre-game) | 0.0034 % |
| Median in-game episode duration | 16 seconds |
| Share of episodes ≤4s | 17.2 % |
| Concentration | Final minutes of live play; end-game rapid probability shifts |
| Median yield (in-game) | **101.01 bps** |
| Median yield (pre-game, 11 episodes only) | 309.28 bps |
| Capped profit ($100/episode cap) | $559.59 aggregate |
| Uncapped theoretical profit | $2,032.75 |
| Middle jackpot realizations | **0** |

### Depth is the binding constraint

**76.9 % of episodes had executable size constrained to an average of ~14.8 shares** (i.e., ~$14.80 deployable at $1.00 par). The $100/episode budget cap was rarely binding because the order-book depth ran out first. No Kelly or fractional-Kelly discussion needed — the choice variable is not risk tolerance but how to source more opportunities at the right moment. Shleifer-Vishny limits-to-arbitrage applies cleanly.

## Why combinatorial empirics matter

- **They expose a different cost structure.** Single-market MRA needs an opportunity scanner. Combinatorial needs a *dependence map* (semantic discovery) AND a scanner. The former cost is one-time per platform-state; the latter is a per-snapshot price check.
- **Saguillo's $100-per-opportunity average + 6,630 opportunities on Pair 4** implies a deployable annual edge in the tens of thousands of dollars on a single dependent pair if you can run the dependence-detection at platform scale (the LLM pipeline costs are modest at the 1,576-pair filtered scale).
- **Cheng's zero Middle jackpot** is the bear case for tail-payoff strategies on NBA: do not back-test combinatorial NBA arb under an "expected $2.00 payoff" assumption.
- **Pair-discovery generalises beyond elections.** Saguillo only confirmed 13 dependent pairs from the U.S. election; presumably more exist across other event clusters (CFB / NBA cross-market, crypto-price ladders, economy-event chains). This is a wiki research direction.

## Math summary

```
Combinatorial condition (Def. 4):
    Long :   Σ_{c∈S} val(T_c, t) < Σ_{c′∈S′} val(T_{c′}, t)
              →  hold YES(S) ∪ YES(complement of S′)
    Short:   inverse
    Profit:  |Σ_{c∈S} val(T_c, t) − Σ_{c′∈S′} val(T_{c′}, t)|

NBA ML/Spread (structural):
    Ask(MLA) + Ask(SpB) < 1.00       →  buy both
    Middle:  Δ ∈ (0, h]               →  $2.00 payoff (rare)

State imputation (look-ahead-free):
    P_M(t_n) = P_M(t_i),  t_i = max{t ∈ T_M | t ≤ t_n}
```

## Source

- `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` — Saguillo, Ghafouri, Kiffer et al. (2026), §5 (LLM dependency detection pipeline), §6.3 (combinatorial empirical results), §4.1.1 (Linq-Embed-Mistral topic classification + 92% accuracy).
- `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` — Cheng, Yang & Zou (2026), §4.1 (subset relation derivation), Table 5 (Middle jackpot payoff), §4 (combinatorial empirical findings), Appendix B.3 (state-imputation forward-fill methodology).

## Related

- [[arbitrage-taxonomy]]
- [[single-market-arbitrage-empirics]]
- [[polymarket-liquidity-evolution]]
- [[polymarket-architecture]]
