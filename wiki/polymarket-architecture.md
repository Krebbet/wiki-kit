# Polymarket Architecture

Hybrid CLOB on Polygon: off-chain order matching against on-chain settlement of ERC1155 conditional tokens (Gnosis CTF). USDC is the underlying collateral; pUSD is the deposit-wallet wrapper. Two exchange contracts: `CTFExchange` for single-condition (binary) markets and `NegRiskCTFExchange` for grouped multi-outcome markets. The `$1.00 Rule` — `Σ P(outcome) = 1` across the outcome set of a market — is enforced by three on-chain primitives: `splitPosition`, `mergePositions`, `convertPositions`, which underpin the [[arbitrage-taxonomy]].

## Execution venue

- **CLOB (Central Limit Order Book), hybrid-decentralized:** order matching off-chain on Polymarket's servers; only matched bids hit the chain (`raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md`, `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md`).
- **Order model:** limit orders with `price`, `size`, `side`, `tickSize`, and a `negRisk` flag identifying grouped-market orders (`raw/research/polymarket-types-and-opportunities/09-polymarket-docs-overview.md`).
- **Gasless trading and deposit wallets** are the recommended path for new API users; Polymarket pays user gas (also noted in `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §3 — gas-paid-by-platform during the 2024 election window).
- **Maker rebates and liquidity rewards** are offered to market makers via dedicated programs (`raw/research/polymarket-types-and-opportunities/09-polymarket-docs-overview.md`).

## On-chain settlement (Polygon, chain 137)

- **Token standard:** ERC1155 conditional tokens (Gnosis Conditional Token Framework). Each market has a pair `(Yes, No)` of ERC1155 IDs identified via `conditionId` / `questionId` — see [[polymarket-market-taxonomy]].
- **Settlement token:** USDC.e on Polygon; pUSD (Polymarket USD) is the deposit-wallet wrapper. Winning tokens redeem 1:1 for USDC.e → wrapped back into pUSD on redemption (`raw/research/polymarket-types-and-opportunities/10-polymarket-uma-resolution.md`).
- **Block timing:** Polygon ~2 s block time; finality buffer 256 blocks. Block timestamps accurate to ±4 s, median 2 s, via linear interpolation from anchor block (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §2).

## Exchange contracts

- **`CTFExchange`** — for single-condition (binary) markets. V1 at `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` through April 2026; V2 at `0xE111180000d2663C0091e4f400237545B87B996B` launched early April 2026 with hard cutover (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §2). Both versions emit identical `OrderFilled` signature, topic `0xd0a08e8c493f9c94f29311604c9de1b4e8c8d4c06bd0c789af57f2d65bfec0f6`.
- **`NegRiskCTFExchange`** — for grouped multi-outcome markets; pairs with the `NegRiskAdapter` (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §2). Identified by `neg_risk=True` and a shared `neg_risk_market_id` in API metadata (`raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §2.1).
- **CTF conditional tokens contract:** `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045`. Three key events: `OrderFilled`, `PositionSplit`, `PositionsMerge`.

## The $1.00 Rule and the three primitives

For a market of `n` mutually exclusive outcomes, the no-arbitrage identity is `Σᵢ P(outcomeᵢ) = 1` at all times. Three on-chain primitives enforce this:

- **`splitPosition`** — deposit 1 USDC → receive 1 Yes + 1 No (binary) or `n` complementary tokens (grouped). Mints a complete set.
- **`mergePositions`** — deposit 1 of each outcome → receive 1 USDC. Burns a complete set.
- **`convertPositions`** (NegRisk only) — converts `Q` units of `M` NO tokens spanning `M` outcomes into `Q` YES tokens for the remaining `N − M` outcomes plus `(M − 1) × Q` USDC (`raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §2).

These primitives are the mechanical floor under [[arbitrage-taxonomy]]: when book prices breach the identity, `split` or `merge` realizes the deviation as a guaranteed profit, subject to non-atomic execution risk on the CLOB legs.

## Aggressor-sign encoding

`OrderFilled` events do not expose aggressor sign as a named field; it is encoded in the asset IDs (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §2):

- `takerAssetId == 0` → taker posted USDC → buyer → sign `+1`.
- `makerAssetId == 0` → maker posted USDC → sign `−1`.

Critical for any direction-dependent measure — see [[polymarket-microstructure]] for why feed-only direction inference is unreliable on Polymarket and why the on-chain `OrderFilled` is mandatory.

## Trading & order lifecycle

(Sources: Polymarket Help Center "Can I Sell Early?" and "Limit Orders", `raw/research/polymarket-creation-and-secondary-market/04-help-can-sell-early.md` and `03-help-limit-orders.md`, both captured 2026-05-16.)

### Secondary market — yes, positions are freely tradable

Polymarket's canonical statement on selling before resolution: *"You may sell shares at any point before the market is resolved by either placing a market order to sell shares at the prevailing bid price in the orderbook, or by placing a limit order for how many shares you wish to sell and at what price."* The limit order fills only if/when a counterparty matches at your price.

This is the implicit "secondary market" the platform offers — every share you hold can be transferred to another wallet via the CLOB at any time pre-resolution. There is no lock-up, no settlement delay between purchase and resale, and partial sells are supported.

### Order types

- **Market orders** — execute immediately at the prevailing best available price. Fast and simple; worse execution in illiquid markets. Minimum trade size $1.
- **Limit orders** — fill only when a counterparty matches at your price. Minimum order size 5 shares. **Partial fills supported**: a resting limit order can be sliced by multiple counterparties in sequence over time.
- **Time-in-force semantics:** implicit GTC (good-til-cancelled); orders persist until manually cancelled or until an auto-cancel event fires. The Help Center article does not document GTC/GTD/IOC as a taxonomy.

For closing positions: market orders are fine for small trades in liquid markets; for anything sized above ~$20 or in less-traded markets, **use limit orders** for better prices and access to maker rebates (see [[polymarket-lp-incentives#2-maker-rebates-taker-fee-funded]]).

### Sports auto-cancel (whole-book wipe)

Sports markets have a hard mechanic: **at scheduled game start time, the entire order book is wiped** — not just your own orders, the whole book. This is distinct from the per-user cancellation on other markets and is documented in [[polymarket-market-taxonomy]] under the sports auto-cancel rule. Operational consequence: if a game starts earlier than scheduled, orders may not clear in time before the first event happens; flag for any automated sports-market quoting strategy.

### Sports 3-second taker delay

Sports markets apply a **3-second delay to all marketable taker orders** (1-second delay under an NBA/MLB A/B test). Reduces maker adverse-selection exposure to fast-data holders; raises taker fill-time uncertainty. This is the structural reason single-market sports arbitrage windows are so compressed in [[single-market-arbitrage-empirics]] (NBA in-game median arb window 3.6 s — the 3-second delay puts retail traders functionally outside the executable window).

### Per-market tick size

`orderPriceMinTickSize` is per-market (`0.01` central, `0.001` tail) per the live Gamma API observations in [[mention-markets#gamma-api-capture-workflow-per-market-resolution-rules]]; revised in [[platform-comparison-kalshi-polymarket]] tick-size section.

## MEV and private-mempool caveat

MEV bots (sandwiching, back-running) on Polygon contaminate on-chain trade direction as a ground truth for organic flow. Private mempool services (Marlin Relay, Bloxroute, Flashbots-on-Polygon variants) capture a non-trivial share of order flow and are invisible to public-mempool analysis (`raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §2). Any strategy back-test that filters for "organic" trades must contend with this.

## Source

- `raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` §2 — Section 2 of Dubach (2026) details the CTFExchange V1/V2 contract addresses, `OrderFilled` event signature and aggressor-sign encoding, Polygon block timing, and MEV caveats.
- `raw/research/polymarket-types-and-opportunities/04-polymarket-2024-election.md` §2–3 — Tsang & Yang (2026) on CTFExchange vs NegRiskCTFExchange, split/merge/convert primitives, gas paid by platform.
- `raw/research/polymarket-types-and-opportunities/05-polymarket-nba-arb.md` §2 — UCLA group on hybrid CLOB design and mirrored-liquidity reflection of Yes ↔ No quotes.
- `raw/research/polymarket-creation-and-secondary-market/03-help-limit-orders.md` — Polymarket Help Center "Limit Orders" (partial fills, GTC semantics, sports 3-second taker delay + auto-cancel whole-book wipe at game start).
- `raw/research/polymarket-creation-and-secondary-market/04-help-can-sell-early.md` — Polymarket Help Center "Can I Sell Early?" (canonical secondary-market statement).
- `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §2.1 — CTF conditional tokens contract address and the three on-chain events `OrderFilled` / `PositionSplit` / `PositionsMerge`; NegRisk metadata flags.
- `raw/research/polymarket-types-and-opportunities/09-polymarket-docs-overview.md` — Platform-level facts: gasless, deposit wallets, maker rebates, builder program, `tickSize`, `negRisk` flag, pUSD.

## Related

- [[polymarket-market-taxonomy]]
- [[uma-optimistic-oracle]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[polymarket-liquidity-evolution]]
