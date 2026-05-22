# Polymarket Strategy Matrix

Consolidated operator view of edge strategies on Polymarket, organized around **two distinct edge modes** the wiki supports:

- **Predictive-edge** — model the underlying event resolution better than the market crowd. Buy now, hold to resolution.
- **Secondary-market timing** — exploit price-movement patterns within a market's lifecycle, regardless of outcome. Buy low (wide spread / early lifecycle / pre-news), sell high (tight spread / mid-maturity / post-news).

The secondary-market lever is real and standard CLOB — per [[polymarket-architecture]] "Trading & order lifecycle", positions are freely tradable pre-resolution via market or limit orders with partial fills. This page maps both modes to bet themes and the specific signal that says "edge is available."

## Per-theme strategy matrix

### Mention markets — Tweet count / "will X say Y" / podcast keywords

- **Cottage industry:** 8 small-volume speakers in [[mention-markets#active-series-matrix-the-cottage-industry]] (Trump-Truth-Social, White House, Ted Cruz, CZ, Zelenskyy, Khamenei, NYC Mayor, plus podcast/show series); volume tiers $10K–$300K vs Elon's ~$19M aggregate.
- **Predictive-edge signal:** per-speaker historical posting cadence → Poisson / NegBin bracket CDF; mid-week Bayesian update from observed count. Kim et al. **MixMCP** validated on Kalshi — `p_mix = 0.7·p_mkt + 0.3·p_mcp` beats market Brier 0.1402 → 0.1392; edge concentrates in mid-confidence 50–70% regime per [[mention-markets#headline-results--kalshi-earnings-call-mention-markets]].
- **Secondary-market timing:** rolling-overlap arb between same-speaker windows (e.g. Elon Musk May 8–15 / 12–19 / 15–22 markets share interior days, constraining priors). High base-rate keyword bins compress to near-100% mid-week; sell before final confirmation.
- **Edge-availability signal:** speaker has stable historical cadence + market is one of the 8 small-volume speakers (not the Elon flagship at ~$19M aggregate).

### Movies — opening-weekend box-office + RT score ladders

- **Predictive-edge signal:** advance ticket sales (Fandango / AMC), Thursday-preview gross (hard signal 36 hr pre-resolution); critic-screening wave timing (1–3 days pre-release); prior-film RT correlations; Beta-distribution prior over critic score.
- **Secondary-market timing:** **RT ladder monotonicity arb** — any `P(≥X) < P(≥X+5)` is a direct Long MRA per [[arbitrage-taxonomy]] §3. Live example captured 2026-05-16: "In the Grey" `P(≥55) = 7% < P(≥60) = 9.5%` (2.5 pp violation) — see [[snapshots/polymarket-broad-coverage-sweep-2026-05-16#movies--live-rt-monotonicity-arb]].
- **Edge-availability signal:** new film with bracket-bin opening market + thin sub-market liquidity ($1K–$84K vol) + advance ticket data accessible. Run a monotonicity Σ-check across the bracket ladder daily.

### Streaming chart positions — Billboard Hot 100 / Netflix Top 10

- **Predictive-edge signal:** public Spotify / Apple Music streaming-data API; Netflix Top 10 viewership feed (public). Prior-week rank + streaming-trajectory anchors the distribution. 9 YES Billboard/Spotify events at 2026-05-16 per [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] Music section.
- **Secondary-market timing:** weekly cadence creates pre-Sunday-chart-release vs post-release spread cycle. Newly-listed pre-week markets carry wider spread; tightens as week progresses.
- **Edge-availability signal:** public streaming-data API + recurring weekly Billboard markets visible on Music landing.

### YouTube creator metrics — densest YES cluster (58%)

- **Pool:** 12 active events; 9 MrBeast + 4 non-MrBeast — **xQc / Forsen / Jack Doherty / Clavicular** per [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]].
- **Predictive-edge signal:** public YouTube API → channel-level historical growth (Poisson / power-law fit), updated with intra-period view trajectory.
- **Secondary-market timing:** subscriber-milestone date-ladder monotonicity Σ-check (same logic as RT). Non-MrBeast creators carry thin volume ($2K–$4K/day) → wide-spread regime suitable for patient liquidity provision.
- **Edge-availability signal:** public YouTube API access + creator with stable channel-growth history; xQc / Forsen / Doherty / Clavicular are unsaturated relative to MrBeast.

### AI / tech milestones

- **Predictive-edge signal:** Chatbot Arena live leaderboard (single authoritative feed) for current-month best-AI markets; trademark filings / SEC filings / corporate press cycles for release-date ladders. Per [[llm-forecasting-by-domain]] — Tech is mixed-tier overall but leaderboard-observable markets have a structured signal.
- **Secondary-market timing:** pre-leaderboard-update vs post-update price swings; release-date ladder monotonicity arb.
- **Edge-availability signal:** Tech 27% YES rate per [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]. **Gamma API anonymizes non-leading candidates as "Company A/B/C"** — opportunities exist where the full PMF can be reconstructed from off-platform sources.

### Crypto short-horizon Up/Down + Hit-Price

- **Predictive-edge signal:** technical / microstructure quant on spot feed (vol forecasting, RV models, calibration-pipeline-style structured estimators). Per [[llm-forecasting-by-domain]] — Crypto is **LLM-weak**, open field for structured quant.
- **Secondary-market timing:** Pre-Market subcategory dominates with 115 of 261 crypto markets per [[snapshots/polymarket-crypto-category-2026-05-13]] — token-launch FDV markets carry pre-event spread compression patterns. BTC 5m Up-or-Down has $22M lifetime aggregate (recurring); per-instance sizing is small.
- **Edge-availability signal:** LLM-weak domain + technical-data fluency. The 5m / 15m / 1h horizon markets favor speed + data over reasoning.

### Corporate event binaries — Finance narrow window

- **Predictive-edge signal:** SEC EDGAR filings (S-1, 10-K), VC announcement tracking, on-chain MicroStrategy treasury monitoring. Small information set; non-quant domain knowledge edge.
- **Secondary-market timing:** pre-filing rumour spread compression; post-announcement re-pricing.
- **Edge-availability signal:** Finance is only 10% YES per [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] but the 3 YES events sit in the AI-frontier wheelhouse: SpaceX IPO date-ladder + month picker; Anthropic-valued-higher-than-OpenAI binary.

### Geopolitical date-ladder events

- **Predictive-edge signal:** OSINT feeds (news velocity, satellite imagery), survival-analysis hazard models. Per [[llm-forecasting-by-domain]] — Geopolitics is **LLM-strong** domain.
- **Secondary-market timing:** **monotonicity arb across the ladder** per [[snapshots/polymarket-geopolitics-category-2026-05-13]] — `P(by T_1) ≤ P(by T_2)` for `T_1 < T_2`. Implied conditional window pricing: `P(in (T_1, T_2] | not by T_1) = (P_2 − P_1) / (1 − P_1)`. Iran airspace 39%/47% is currently the tightest live spread (8 pp slack).
- **Edge-availability signal:** tightest cross-leg spread + thin liquidity. Live monotonicity Σ-check daily across Iran cluster (US-Iran peace, Strait of Hormuz, regime fall, Reza Pahlavi, Israel withdraws from Lebanon, etc.).

### Conditional / scenario-grid markets

- **Predictive-edge signal:** joint-distribution model from individual-race priors.
- **Secondary-market timing:** **combinatorial arb** between scenario composite and component marginals per [[arbitrage-taxonomy]] §3.2.2 + [[snapshots/polymarket-midterms-category-2026-05-13]]. At 2026-05-13 capture, midterms balance-of-power vs chamber marginals implied `P(R-Sweep) ≈ −12%` — a textbook combinatorial-arb candidate.
- **Edge-availability signal:** scenario-grid market + its component binaries both live with depth.

### LP yield farming — the meta-strategy

- **Three stackable yield sources** per [[polymarket-lp-incentives]]:
  - **Liquidity Rewards** (platform-funded, proximity-weighted to mid, per-market max-spread gate, both-sides rule below `$0.10` mid)
  - **Maker Rebates** (taker-fee-funded; `fee_eq = C × feeRate × p × (1−p)` per fill; Crypto 20% / others 25% rebate; min $1 payout)
  - **Sponsor Market Rewards** (third-party USDC, daily distribution, sponsor return = zero)
- **Per-market LP-yield:** `LP_yield = liquidity_rewards_share + maker_rebate_share + Σ active_sponsor_rewards_share` (all per-market, no cross-market netting).
- **Secondary-market timing implication:** **sponsor-pull dynamic** — when a sponsor's daily reward pool ends, depth compresses and spreads re-widen. Exploitable both as LP (capture wider spread post-end) and as a buyer (cheaper entries).
- **Edge-availability signal:** live at `polymarket.com/rewards`. 2026-05-16 capture: **Esports dominates the sponsor queue** — Valorant BO3 series ~$3,412 USDC reward per match. See [[polymarket-lp-incentives#live-data-from-polymarketcomrewards-2026-05-16]].

## Pure secondary-market timing patterns — orthogonal to fundamental edge

These work *regardless* of whether you have a fundamental view on the underlying event. They exploit structural microstructure patterns the wiki has documented.

| Pattern | Signal it's exploitable | Source |
|---|---|---|
| **Longshot fade** | Tail-probability markets (`p < 0.10`) carry **650–900 bps half-spread** — order of magnitude above IEM/racetracks. Patient liquidity provision on the wide side. | [[polymarket-microstructure]] SF1 |
| **Listing-spread compression** | Newly-listed markets (NEW-tag) carry wider spread that tightens as market matures; mid-maturity is the operator sweet spot. | [[platform-comparison-kalshi-polymarket]] |
| **Half-life maturation arc** | Trump YES 2024: Kyle's λ `0.53 → 0.01`; arb half-life `2 hr → 0.74 min`. Operator window is mid-maturity (weeks-to-months pre-resolution). | [[polymarket-liquidity-evolution]] |
| **Bracket Σ-check** | Within a multi-bracket market, `Σ P(bracket_i) ≈ 1.00`; deviations are MRA. Applies to Tweet-count, RT score, seat-count, box-office bracket markets. | [[arbitrage-taxonomy]] §3 + [[polymarket-market-structures]] Structure 4 |
| **Date-ladder monotonicity** | Across same-event multi-expiry legs, `P(by T_1) ≤ P(by T_2)` must hold. Iran airspace 8 pp slack today. RT "In the Grey" 2.5 pp violation today (live). | [[snapshots/polymarket-geopolitics-category-2026-05-13]] + [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] |
| **Scenario-vs-marginals combinatorial** | Composite scenario probabilities must be consistent with component marginals. Midterms `P(R-Sweep) ≈ −12%` example. | [[snapshots/polymarket-midterms-category-2026-05-13]] + [[arbitrage-taxonomy]] §3.2.2 |
| **Mirrored Yes ↔ No reflection** | A single mispricing manifests as both Long signal (`Ask_A + Ask_B < 1.00`) AND crossed synthetic Short (`Bid_A + Bid_B > 1.00`). Deduplicate to avoid double-counting. | [[single-market-arbitrage-empirics]] |
| **Post-game oracle-window spread blow-out** | Sports/event markets see spreads spike to ~7,500 bps after game end while UMA resolves. **Don't trade** — apparent arbs are stale orders, not real liquidity. | [[snapshots/polymarket-niche-categories-2026-05-13]] + [[single-market-arbitrage-empirics]] |
| **Sponsor-end depth pull** | When a sponsor's reward pool expires, depth compresses and spreads re-widen. Track `polymarket.com/rewards` for sponsorship end-dates. | [[polymarket-lp-incentives#operator-side-strategy-notes]] |
| **LLM-overconfident tail bias** | If other operators are using uncalibrated LLM outputs as signal, the wrong-direction tail trades they push create contrarian opportunities. Speculative; no direct empirical confirmation in the wiki. | [[llm-epistemic-calibration]] (Editorial — synthesis) |

## Signal-availability decision tree

Given a candidate market, ask in order:

1. **Is the market in a YES-classified theme?** (mentions / box office / streaming charts / YouTube / AI leaderboard / corporate event / geopolitics date-ladder) — see [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] for the 45 YES events identified across the 162-event 2026-05-16 sweep.
2. **Do you have the predictive-edge data source?** (per-speaker timeline / advance ticket sales / streaming API / YouTube API / Chatbot Arena / SEC EDGAR / OSINT). If yes → predictive-edge mode.
3. **Is the market in a structural-arb shape?** (date-ladder / bracket bins / scenario-grid / mirrored Yes ↔ No / sponsor-active). If yes → run Σ-checks or monotonicity-checks for direct MRA per [[arbitrage-taxonomy]].
4. **Is the market in a microstructure-pattern regime?** (longshot tail / newly-listed wide spread / mid-maturity / sponsor-end pull). If yes → buy-low timing mode.
5. **Is none of the above true?** Likely a saturated quant-mainstream market (Fed rate, commodities, headline politics, mainstream sports). Skip per the saved feedback memory.

## Where this page does NOT yet have answers

- **Empirical performance for any of these strategies on Polymarket.** Kim et al. MCP is Kalshi-validated; box-office bracket-bin modeling is unvalidated on Polymarket; YouTube view-count Poisson is operationally plausible but unbacktested. The wiki has the theoretical frameworks ([[market-maker-handbook-prediction-markets]], [[logit-jump-diffusion-kernel]]) but no Polymarket-side empirical proof for predictive-edge strategies in the YES themes.
- **Optimal-quoting under the 3-program LP stack.** Per [[polymarket-lp-incentives#what-this-page-does-not-cover]] — the combined `LP_yield` formula is correct in shape but the optimal-spread-and-size choice depends on per-market max-spread, current sponsor pool, fill probability. Non-trivial.
- **Per-event resolution-rule corpus.** Only one market has captured binding rules (Trump-Xi bilateral). The 45 YES-classified markets in [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] would each benefit from a `tools/capture_polymarket_market.py --slug <slug>` run.

## Source

This is a synthesis page; all substantive claims trace to existing wiki pages (no new raw sources). Generated 2026-05-16 in response to a /query for consolidated strategy view following the discovery that selling positions pre-resolution is a standard CLOB capability (resolved in [[polymarket-architecture]] Trading & order lifecycle 2026-05-16).

## Related

- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[mention-markets]]
- [[polymarket-microstructure]]
- [[polymarket-liquidity-evolution]]
- [[polymarket-lp-incentives]]
- [[polymarket-architecture]]
- [[llm-forecasting-by-domain]]
- [[llm-epistemic-calibration]]
- [[market-maker-handbook-prediction-markets]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]
- [[snapshots/polymarket-geopolitics-category-2026-05-13]]
- [[snapshots/polymarket-midterms-category-2026-05-13]]
