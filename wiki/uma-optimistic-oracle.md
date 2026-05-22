# UMA Optimistic Oracle (Polymarket Resolution)

Polymarket's primary resolution oracle is **UMA's Optimistic Oracle (OO)**: anyone may propose an outcome by bonding ~$750 pUSD; if undisputed within 2 hours, the proposal is accepted and the market resolves; if disputed, a counter-bond initiates a new proposal round, and a second dispute escalates to a Data Verification Mechanism (DVM) vote by UMA token holders. Total elapsed time: ~2 hours (no dispute) or 4–6 days (one or two disputes). Winning bond positions earn back their own bond plus half of the opponent's bond. Bond economics imply a structural monitoring edge for disputers watching the 2-hour challenge window.

**Polymarket's resolution layer is not UMA-only.** Subsequent captures revealed that:
- **Pyth Network** is used as a secondary oracle for "some markets" (Grayscale Sep 2024, `raw/research/polymarket-market-content-and-sizing/07-grayscale-polymarket.md`). Specific market types using Pyth are not named in the captured corpus.
- **Chainlink** is used for *deterministic / financial* events (Falcon X Jan 2026, `raw/research/polymarket-market-trends-and-llm-edge/06-falconx-emerging-trends.md`). UMA handles ambiguous events; Chainlink handles deterministic feeds where dispute mechanics are unnecessary.
- **Crypto price markets** ([[snapshots/polymarket-crypto-category-2026-05-13]]) do not disclose their price feed on the category landing page — likely Chainlink or Pyth per the above, but unconfirmed.

The full resolution-mechanism page below documents UMA mechanics in detail; the multi-oracle picture is structurally important for understanding *which* markets are dispute-prone (UMA-resolved) vs immediate-deterministic (Chainlink / Pyth feed). This wiki currently lacks dedicated coverage of the Chainlink and Pyth integrations — open follow-up.

## The three-phase flow

**Phase 1 — Proposal.** Anyone selects a winning outcome, posts a bond (typically $750 pUSD), submits to UMA Oracle.

**Phase 2 — Challenge period (2 hours).** If no dispute: proposal accepted, market resolves. If disputed: a new proposal round begins. If second proposal is also disputed: escalates to DVM.

**Phase 3 — Debate (24–48 hours, if disputed).** Disputer posts matching $750 counter-bond. Evidence submitted in UMA Discord channels `#evidence-rationale` and `#voting-discussion`.

**Phase 4 — DVM vote (~48 hours, if escalated).** UMA token holders vote. Outcome enforced on-chain via the appropriate `UmaCtfAdapter` contract.

Three possible resolution paths:

| Flow | Sequence | Elapsed |
|---|---|---|
| No dispute | Propose → Resolve | ~2 hr |
| One dispute | Propose → Challenge → Propose → Resolve | longer |
| Two disputes | Propose → Challenge → Propose → Challenge → DVM Resolve | 4–6 days |

## Bond economics

Both parties post $750 pUSD (typical). Outcomes:

| Outcome | Bond distribution |
|---|---|
| Proposer wins | Proposer recovers own bond + ½ of disputer's bond (~$375 net gain) |
| Disputer wins | Disputer recovers own bond + ½ of proposer's bond (~$375 net gain) |
| "Too Early" — event hasn't concluded | Disputer wins: recovers own bond + ½ of proposer's bond |
| "Unknown / 50-50" (rare) | Market resolves at $0.50 per token; disputer recovers own bond + ½ of proposer's bond |

**Structural edges implied by the bond table** (`raw/research/polymarket-types-and-opportunities/10-polymarket-uma-resolution.md`):

- **Monitoring premature proposals.** A disputer who catches a proposal submitted before the event concludes wins on "Too Early" *even if* the proposed outcome eventually proves correct. Edge condition: ambiguous end-time markets + active 2-hour window monitor + ≥$750 pUSD working capital.
- **50-50 fair-value asymmetry.** A binary position held at price `p < 0.5` on one outcome still returns `$0.50` on a 50-50 resolution — i.e., above its purchased fair value. Realisation rate is low; treat as a tail upside, not a positive-EV strategy on its own.

### Live Gamma API observation — $500 bond, not $750 (2026-05-14)

Probing the Gamma API (`gamma-api.polymarket.com/events?slug=<slug>`) on two distinct markets — a mention market (`what-will-trump-say-during-bilateral-events-with-xi-jinping`) and a high-volume non-mention market (`2026-fifa-world-cup-winner-595`, $976M cumulative volume) — both return **`umaBond` = "500"** and **`umaReward` = "5"** on every sub-market. Same value across mention and non-mention, same value across thin and ultra-deep markets.

This conflicts with the "$750 pUSD" figure documented below (sourced from the Polymarket Help Center 2026-05-13 capture). Three possible reconciliations:

1. **Help docs are stale.** Plausible — the $750 figure may reflect an earlier bond schedule that was lowered. Live API is currently $500.
2. **$750 is the disputer bond; $500 is the proposer bond.** The API field is `umaBond` per-market without specifying side. Resolved-disputed markets would need a separate capture to verify.
3. **Higher-stakes markets carry higher bonds**, and $500 is the default. Not supported by the FIFA capture ($976M volume, still $500 bond).

Until resolved, treat both figures as candidates. The bond-economics math in this page (net gain ~$375 = ½ of opponent's bond at $750 each) becomes **net gain ~$250** at the $500 live API value. If you are sizing capital for proposer/disputer activity, use $500.

`umaReward` = $5 is the proposer reward on a successful, undisputed proposal — confirms the "reward separate from bond return" detail captured below, with a concrete magnitude. **$5 reward on $500 bond ≈ 1% rate**; a proposer who is wrong about timing forfeits 100% of bond to recover $5 — heavily asymmetric, do not propose without high confidence.

Logged in `master_notes.md` 2026-05-14 as open project-scope note pending verification.

### Polymarket Help Center additions

(Source: `raw/research/polymarket-politics-and-niche-markets/04-polymarket-help-resolution.md`, Polymarket Help Center "How Are Prediction Markets Resolved?", captured 2026-05-13.)

Three details that explicitly extend the bond mechanics above:

- **Proposer reward separate from bond return.** On a successful, unchallenged proposal, the proposer receives the bond back **plus a reward** — the reward is a distinct payout, not part of the bond. Magnitude not specified in this source; needs per-market or UMA-protocol confirmation.
- **"Propose too early" = full bond forfeiture.** Hard rule, explicit in the Help Center: an early proposal loses the entire $750. The "Too Early" bond-distribution row above (disputer recovers own bond + ½ of proposer's bond) is the disputer-side accounting of the same event; the proposer side is total bond loss.
- **Bond denomination — USDC.e (vs pUSD).** The Help Center says "$750 USDC.e bond"; this page above (drawn from the developer docs) says "$750 pUSD". pUSD is Polymarket's wrapped USDC.e — see [[polymarket-architecture]] — so the two terms refer to the same instrument. Treat as display aliases.
- **Settlement mechanics — explicit.** Per the Help Center: winning shares pay **$1.00 each**, losing shares go to **$0.00**, trading **halts** at resolution. These match the page above but the Help Center states them as primary settlement mechanics.

## Resolution rules per market

Every market's `Resolution Rules` field specifies (`raw/research/polymarket-types-and-opportunities/10-polymarket-uma-resolution.md`):

- Resolution source (official announcement, specific website, etc.)
- End date eligible for resolution
- Edge-case handling for ambiguous situations

**Docs warning to operators:** *the market title describes the question; the rules define how it resolves.* Always read the rules before trading. This drives the wiki's lint check that every market page must link to its captured resolution-criteria text.

## Clarifications

Polymarket may issue an `Additional context` update after a market opens. Clarifications:

- Cannot alter the fundamental intent of the question.
- Published on-chain via a bulletin-board contract.
- Should be considered by UMA voters when resolving disputes.

Requests are filed in Polymarket Discord `#market-review`.

## Post-resolution redemption flow

1. Trading stops at resolution.
2. Winning ERC1155 outcome tokens are burned by the `UmaCtfAdapter`.
3. Adapter releases USDC.e collateral from the CTF contract.
4. USDC.e is wrapped into pUSD and returned to the wallet.

Example: 100 winning tokens → $100 pUSD.

## Contract addresses (Polygon Mainnet)

- `UmaCtfAdapter v3.0`: `0x157Ce2d672854c848c9b79C49a8Cc6cc89176a49`
- `UmaCtfAdapter v2.0`: `0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74`
- `UmaCtfAdapter v1.0`: `0xCB1822859cEF82Cd2Eb4E6276C7916e692995130`

## Documented edge cases

- **FIDE World Blitz Chess Championship 2024** — both Carlsen and Nepomniachtchi were declared winners of different sections; UMA's mutual-exclusivity constraint forced selection of a single "True" outcome. Source: `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §2.1.3. The captured docs do not reproduce the resolution criteria text for this market; flag for follow-up capture if needed for the per-market lint rule.

## Governance attack surface

UMA token voting power is concentrated among large holders (Dune dashboard `dune.com/primo_data` referenced in `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §2.1.3). AFT 2024 paper on DAO attacks is cited for the broader governance-risk context. Operational implication: a small but non-zero probability that a contested resolution can be moved by coordinated voting concentration, especially on markets where the realized payoff to attackers exceeds the cost of acquiring vote weight. No empirical incident is documented in our captured sources.

## External resources cited

- UMA Oracle Portal: `https://oracle.uma.xyz/`
- UMA Documentation: `https://docs.uma.xyz/`
- `UmaCtfAdapter` source code: `https://github.com/Polymarket/uma-ctf-adapter`

## Source

- `raw/research/polymarket-types-and-opportunities/10-polymarket-uma-resolution.md` — Polymarket Documentation on UMA-based resolution; full OO flow, timing tables, bond mechanics, vote outcomes, clarifications mechanism, redemption flow, contract addresses.
- `raw/research/polymarket-types-and-opportunities/07-arb-probabilistic-forest.md` §2.1.3 — UMA OO described as primary resolution mechanism on Polymarket; voting-concentration risk citation; FIDE chess edge case.
- `raw/research/polymarket-market-content-and-sizing/07-grayscale-polymarket.md` — Pyth as secondary oracle for "some markets" (institutional research, Sep 2024).
- `raw/research/polymarket-market-trends-and-llm-edge/06-falconx-emerging-trends.md` — Chainlink for deterministic/financial events; UMA for ambiguous (Jan 2026 practitioner piece).
- `raw/research/polymarket-politics-and-niche-markets/04-polymarket-help-resolution.md` — Polymarket Help Center "How Are Prediction Markets Resolved?"; proposer reward separate from bond, USDC.e denomination, settlement-mechanics primary statement (captured 2026-05-13).

## Related

- [[polymarket-market-taxonomy]]
- [[polymarket-architecture]]
- [[single-market-arbitrage-empirics]]
- [[snapshots/polymarket-crypto-category-2026-05-13]]
