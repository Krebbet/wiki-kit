# Single-Market Arbitrage — Empirics

Two empirical lenses on intra-market arbitrage (Market Rebalancing Arbitrage, MRA — see [[arbitrage-taxonomy]] for definitions and execution paths) point in the same direction: opportunities exist but extractable size is depth-constrained at retail scale, and the binding friction is Shleifer-Vishny limits-to-arbitrage, not opportunity scarcity.

**Two scopes, reconciled:**

- **Cross-platform / full-lifecycle (Saguillo et al. 2026):** 17,218 conditions Apr 2024–Apr 2025; **41% of conditions** had ≥1 MRA opportunity at some point; **~$11M extracted** via single-condition buy/sell strategies. Median profit-per-dollar ~$0.60.
- **NBA / in-game only (Cheng, Yang, Zou 2026):** 75M LOB snapshots across 173 NBA games Feb–Mar 2026; **7 valid in-game episodes** in 3,042 markets; **$210 capped profit** (heavily right-skewed). Median duration **3.6 seconds**.

These are not contradictory. The cross-platform study captures the *full lifecycle* of each market, including the long mid-maturity window where deviations persist for minutes to hours ([[polymarket-liquidity-evolution]]); the NBA study captures only the in-game window of contracts with ~hours of lifespan, in which dislocations close in seconds. The lesson: which study describes *your* execution regime depends on the holding window you're operating in.

## Saguillo et al. — single-condition MRA at platform scale

Source: `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §6.1, §7.

- Sample: **17,218 conditions** (8,559 from 1,578 NegRisk markets + 8,659 from single-condition markets).
- Period: April 1, 2024 – April 1, 2025. Platform: Polymarket. Price input: VWAP over one Polygon block; carry-forward up to 5,000 blocks; opportunities ignored when any token > $0.95.

### Findings

- **7,051 of 17,218 conditions (41%)** had ≥ 1 arb opportunity. All detected single-condition opportunities were **long** (i.e., `YES + NO < 1`); no short opportunities detected at the single-condition level (`raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §6.1).
- **Median profit-per-dollar across topics: ~$0.60** — well above the $0.02 minimum-profit filter the authors apply. The authors term this "remarkable market inefficiency".
- **Crypto** had the largest outliers in opportunity count per condition.
- **Single-condition realised extraction:** $5,899,287 (buying below $1) + $4,682,075 (selling above $1; this is via SPLIT-and-sell paths inside NegRisk markets where short opportunities exist — see [[arbitrage-taxonomy]] §Short MRA Path B).
- **Extreme single case** (`raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §6.1): user `@Tutaaa91` bought both YES and NO for `< $0.02` each on a single condition, profiting **$58,983** from one trade.

### Multi-condition (NegRisk) intra-market MRA

(Source: same paper, §6.2.) 1,578 NegRisk markets; **662 (42%)** had ≥1 intra-market opportunity. Average **~100 opportunities per market**. Both long and short opportunities exist at this level (unlike the single-condition case). Average max profit ~$0.40 per dollar for both directions. Realised by strategy:

- Buying NO: **$17,307,114** (overwhelmingly dominant)
- Buying YES: $11,092,286
- Selling YES: $612,189
- Selling NO: $4,264

The dominance of *buying NO* aligns with Polymarket's own public communications flagging unusual NO-buying activity in the period.

## Cheng, Yang, Zou — NBA single-market in-game

Source: `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md`.

### Sample and method

- 75,088,497 LOB snapshots across **3,042 markets** in **173 NBA games**, Feb 4 – Mar 4, 2026.
- Two execution paths considered:
  - **Buy Path (Long):** `Ask_A + Ask_B < 1.00` → buy both outcomes at ask.
  - **Mint-and-Sell (Short):** mint a complete set for $1.00 via `splitPosition`, sell both tokens at bid when `Bid_A + Bid_B > 1.00`.
- Mirrored-orderbook deduplication is essential: Polymarket's CLOB synthetically reflects a buy for YES at `$P` into a sell for NO at `$1 − P`, so each raw mispricing appears as *both* a Long and a Short signal; the pipeline evaluates both paths independently and retains only one per simultaneous pair (`raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` §3 Mirrored orderbook deduplication).
- **Phantom-arb prevention:** sequential order-book updates within **500 ms** are clustered to a single timestamp (eliminates phantom sub-second arbs from the 2–50 ms CLOB API serialization delay). Duration capping: `Valid_Duration_n = min(t_{n+1} − t_n, C_phase)` with `C_phase = 1800 s` (Pre/Post-Game), `300 s` (In-Game).
- **Post-game filter:** 30 of 37 raw single-market detections (~81.1 %) were **post-game artefacts** — stale limit orders persisting after game-end while makers withdrew quotes during the oracle-resolution waiting window. These are excluded as non-executable. The bid-ask spread during this window inflates to **7,532.65 bps** (vs 1,030.90 bps in-game and 392.20 bps pre-game).

### Findings

- **7 valid in-game episodes** survive filtering; **0 pre-game episodes**.
- Time in arb: **0.0001 % of in-game time**.
- Median duration: **3.614 seconds** — well below typical human reaction time.
- Capped profit ($100/episode cap): **$210.19 aggregate**, heavily skewed by one outlier (median yield 11.0 % ≈ $11/episode excluding outlier).
- Uncapped theoretical profit: $4,418.44 — illustrates the gap between theoretically detectable and practically extractable.
- **Spread markets (3 episodes): $194.08** capped profit, vs Moneyline (3 episodes): **$5.10**. Spread markets show deeper liquidity vacuums during dislocations.

### What this empiric does NOT say

It does NOT say that single-market arb on Polymarket is rare in general — it says that on NBA contracts during the in-game phase only, it is rare. NBA contracts are short-lived (hours) and never reach the mid-maturity depth window where the Saguillo finding's 41% opportunity rate accumulates.

## Reconciliation

| Dimension | Saguillo (cross-platform) | Cheng (NBA in-game) |
|---|---|---|
| Time window | Full market lifecycle | In-game only (excludes pre-game and post-game) |
| Markets | All categories incl. politics, crypto, sports | NBA game markets only |
| Contract lifespan | Days to many months | Hours |
| Number of opportunities | High (41 % of conditions) | Very low (7 episodes / 75M snapshots) |
| Median duration | Not separately stated for full sample; long enough to net $0.60/$ | 3.6 s |
| Effective constraint | Execution latency / non-atomic leg risk | Same execution latency, against vastly shorter window |
| Realised $ | $11M+ (single-condition only) | $210 |

Together they establish: **opportunity density scales with market lifespan**. Long-lived political and crypto markets see persistent mid-maturity windows where MRA is profitable at retail scale; short-lived sports contracts compress that window into seconds where only programmatic actors operate.

## Limits to arbitrage — Shleifer-Vishny applied

`raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` and `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` both apply Shleifer & Vishny (1997) limits-to-arbitrage to Polymarket: the binding friction is **order-book depth, not bankroll**. Cheng et al. report depth-capped executable size at ~14.8 shares average across 76.9 % of episodes; Tsang & Yang report that mid-2024 election arbitrage closed in <1 minute (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §5). For an operator with $X working capital, the rate-limiting factor is *finding more shallow-depth opportunities at the right moment*, not how much capital can be deployed against any single one.

## Operator takeaways

- For passive-profile execution: target single-condition long MRA on Politics/Crypto/Culture markets with 1–3 months to resolution, where Saguillo's 41 % opportunity density and ~$0.60/$ profit median both live. Mid-maturity is the regime ([[polymarket-liquidity-evolution]]).
- For high-frequency execution: be aware NBA in-game windows are 3-second median; you are competing with bots at the leg-fill latency frontier (`raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §7.4 Figure 12 — log-linear profit-vs-transaction profile of top accounts).
- **Sports is consistently identified as high-frequency opportunity but low realised extraction** (`raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §6.2 — "Sports largely absent from realized arbitrage charts"; possibly underexploited). This is the cleanest "edge" signal in the captured corpus.
- Always exclude post-resolution windows when scanning: the spread explodes to ~7,500 bps and the apparent arbs are stale-order artefacts ([[uma-optimistic-oracle]] for the oracle-window timing).

## Source

- `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` — Saguillo, Ghafouri, Kiffer et al. (2026), §6.1, §6.2, §7.3, §7.4. The platform-scale single-condition and NegRisk-multi-condition MRA empirics; topic breakdown; NO-buying dominance; top-arbitrageur profile.
- `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` — Cheng, Yang & Zou (2026), §3–4 and Appendix A.4 / B.3. NBA in-game and post-game empirics; mirrored-orderbook deduplication; phantom-arb filter; bid-ask spread by phase.
- `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §5 — half-life evidence cited for the mid-maturity window claim.

## Related

- [[arbitrage-taxonomy]]
- [[combinatorial-arbitrage-empirics]]
- [[polymarket-liquidity-evolution]]
- [[polymarket-microstructure]]
- [[uma-optimistic-oracle]]
