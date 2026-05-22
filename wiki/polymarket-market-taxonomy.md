# Polymarket Market Taxonomy

Polymarket's canonical data model: a **market** is a single binary Yes/No tradable unit; an **event** is a container holding one or more markets. Single-market events are 1:1 with their market; grouped (multi-market) events host mutually exclusive multi-outcome prediction sets. Identifiers are `conditionId`, `questionId`, and a pair of ERC1155 token IDs. CLOB tradability gated by `enableOrderBook`. Sports markets auto-cancel resting limit orders at scheduled game start.

## Markets

- **Atomic unit:** a single binary Yes/No question. No native multi-outcome at the market level — multi-outcome is constructed by grouping binary markets inside an event.
- **Identifiers** per market:
  - `conditionId` — primary key inside the CTF (Conditional Token Framework) contracts.
  - `questionId` — hash of the market question, used for resolution.
  - Two ERC1155 token IDs (one Yes, one No) — used for CLOB trading and as the on-chain position representation.
- **CLOB gate:** `enableOrderBook: true` is required for order-book trading. Markets can exist on-chain with `enableOrderBook: false` and be ineligible for CLOB execution.

## Events

Two shapes:

- **Simple (single-market) event** — event ≈ market (1:1). E.g., `fed-decision-in-october` → one Yes/No.
- **Grouped (multi-market) event** — event contains ≥2 markets, each a Yes/No on a distinct outcome. Used for mutually exclusive multi-outcome questions. Example: the 2024 Presidential Election event grouped `Trump?`, `Harris?`, `Biden?`, `Other?` as four binary markets sharing the event container — see [[polymarket-architecture]] for how NegRisk enforces `Σ P(Yesᵢ) = 1` across grouped markets.

## Identification and lookup

Both markets and events carry a unique `slug`, embedded in the URL: `https://polymarket.com/event/<slug>`. Slugs are the standard lookup key against the Gamma API:

```
GET https://gamma-api.polymarket.com/events?slug=<slug>
```

Slug is also the wiki-side convention for dated price snapshots: `raw/markets/<slug>/<YYYY-MM-DD>.*`.

## Sports markets — auto-cancel rule

Outstanding limit orders are **automatically cancelled** at the **scheduled** game start time. Operational risk flagged in the docs: if a game starts earlier than scheduled, orders may not clear in time — Polymarket explicitly warns "Always monitor your orders closely around game start times". Treat this as an oracle-of-time exposure when running automated quoting against sports markets.

## Market creation pipeline

(Source: Polymarket Help Center "How Are Markets Created?", `raw/research/polymarket-creation-and-secondary-market/01-help-how-markets-created.md`, captured 2026-05-16. The `docs.polymarket.com` version of the same article is byte-for-byte identical.)

**Canonical statement** from Polymarket's own help center:

> *"While users cannot directly create their own markets, they are encouraged to suggest ideas for new markets."*

So the pipeline is **proposal-only for users**; Polymarket's internal team is the sole listing authority. There is **no community vote, no on-chain governance, no permissionless listing path** documented anywhere in the captured corpus.

### Proposal channels

- **Twitter / X — tag `@polymarket`.** Documented as the primary channel in the Help Center article.
- Other channels (Discord `#market-review` for *clarifications* on existing markets — see [[uma-optimistic-oracle]]) are not documented as proposal channels.

### Required proposal fields

Three things the Help Center asks proposers to include:

1. **Market title** — the question phrasing.
2. **Resolution source** — the authoritative data source that will determine the outcome at resolution. Polymarket explicitly links to the resolution article (the `13364518` Help Center page covered in [[uma-optimistic-oracle]]).
3. **Evidence of demand for trading that market** — qualitative signal that other traders will participate.

### What's NOT documented

- **Approval timeline** — how long from proposal to listing is not stated.
- **Rejection criteria** — what causes a proposal to be declined.
- **Quantitative demand bar** — "evidence of demand" is qualitative; no specific volume / follower / engagement threshold.
- **Whether recurring-series templates** (weekly Trump-speech, MrBeast-video, JRE-episode mention-market series per [[mention-markets#active-series-matrix-the-cottage-industry]]) are auto-instantiated by Polymarket internal tooling or manually re-listed each period. The pattern of NEW-tagged markets appearing weekly suggests automation, but Polymarket doesn't disclose.
- **Identity of `submitted_by` wallets** on Gamma API (e.g. `0x91430CaD2d3975766499717fA0D66A78D814E5c5` on FIFA Spain). Almost certainly Polymarket-internal multisig given the centralized listing model — but not confirmed.

### What users *can* do unilaterally — sponsor an existing market

The closest retail-accessible analog to "create a market" is **sponsoring an existing market** to drive liquidity into it. Anyone can deposit USDC into a smart contract that pays daily rewards to that market's LPs. See [[polymarket-lp-incentives#3-sponsor-market-rewards-third-party-funded]] for the full mechanics. The sponsor earns **zero direct return** — the incentive is purely strategic (driving depth so you can trade size into it without paying the longshot spread premium documented in [[polymarket-microstructure]] SF1).

## What this taxonomy does NOT cover

- Resolution flow (proposal → challenge → DVM) — see [[uma-optimistic-oracle]].
- Token redemption and CTF adapter mechanics — see [[polymarket-architecture]].
- Order-book depth, spread, and execution behavior — see [[polymarket-microstructure]].
- Full market-creation pipeline — partial coverage above; open follow-up.

## Source

- `raw/research/polymarket-types-and-opportunities/08-polymarket-markets-events.md` — Polymarket Documentation: Markets & Events (concept page).
- `raw/research/polymarket-types-and-opportunities/09-polymarket-docs-overview.md` — Polymarket Documentation: Overview (top-level docs; contributes the `negRisk` flag and `tickSize` order-model facts).
- `raw/research/polymarket-creation-and-secondary-market/01-help-how-markets-created.md` — Polymarket Help Center "How Are Markets Created?" (canonical proposal pipeline; users cannot create directly, must propose via @polymarket Twitter tag with title + resolution source + demand evidence).

## Related

- [[polymarket-architecture]]
- [[uma-optimistic-oracle]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
