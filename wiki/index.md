# Wiki Index

Quant-analytical knowledge base for finding edges in immature prediction markets — Polymarket primary, Kalshi as comparison; covers market mechanics, betting/modeling strategy, and microstructure to support strategy design and back-testing.

Catalog of all pages in this wiki. Updated on every ingest.

---

## Overview

| Page | Summary |
|---|---|
| [[polymarket-market-taxonomy]] | Canonical market/event data model: binary Yes/No markets, simple vs grouped events, identifiers (conditionId, questionId, ERC1155 token IDs), `enableOrderBook` CLOB gate, slug-based identification, sports auto-cancel rule. |
| [[polymarket-architecture]] | Hybrid CLOB on Polygon: off-chain matching + on-chain settlement; CTFExchange vs NegRiskCTFExchange; ERC1155 conditional tokens; USDC.e + pUSD; split / merge / convert primitives that enforce `Σ P = 1`. |
| [[uma-optimistic-oracle]] | UMA-based resolution flow: $750 pUSD proposal/dispute bonds, 2-hour challenge window, DVM escalation path, 4–6 day total disputed timeline, "Too Early" + 50-50 edge cases, post-resolution redemption. |
| [[polymarket-microstructure]] | Eight stylized facts (Dubach 2026): longshot spread premium, uniform-grid depth profile, ~32 effective makers median, depth decay near resolution, ~59% feed-only direction-inference accuracy → on-chain `OrderFilled` mandatory. |
| [[polymarket-liquidity-evolution]] | 2024 Election market maturation: arb half-life 2 hours → 0.74 min; Kyle's λ 0.53 → 0.01 on Trump YES; volume mismeasurement (~2.45× naive overstatement). |
| [[arbitrage-taxonomy]] | Saguillo et al. (2026) canonical taxonomy: Market Rebalancing vs Combinatorial Arbitrage with formal definitions and profit formulas; ~$39.6M extracted Apr 2024–Apr 2025; 41% of conditions had ≥1 MRA opportunity. |
| [[single-market-arbitrage-empirics]] | Two scopes reconciled: $11M+ realised single-condition extraction at platform scale (Saguillo) vs $210 capped on NBA in-game (Cheng); Sports flagged as underexploited; depth-bound limits-to-arbitrage. |
| [[combinatorial-arbitrage-empirics]] | Cross-market arb requires dependence detection: LLM-based semantic pipeline (Saguillo, 13 confirmed pairs in 2024 election) vs structural derivation (Cheng, NBA ML/Spread); 76.9% depth-constrained; zero Middle jackpots. |
| [[logit-jump-diffusion-kernel]] | RN-JD model (Dalen 2025): `dx_t = μ dt + σ_b dW_t + jumps`, RN drift pins `p_t = S(x_t)` to martingale; PIDE, Greeks in logit units, calibration pipeline. **All validation on synthetic data — no real-data backtest captured.** |
| [[market-maker-handbook-prediction-markets]] | A–S quoting in logit units (Eqs. 8–9), inventory caps near tails, cross-event β-hedge with co-jump correction, calendar variance hedge, toxicity guards, P&L attribution. Same synthetic-only caveat. |
| [[mention-markets]] | Polymarket's word/phrase prediction category (435 Pop Culture markets, 14 subcategories) + Kim et al.'s Market-Conditioned Prompting technique (Kalshi-validated, Brier 0.1402 → 0.1392 with MixMCP `α=0.7`). The most-directly LLM-edge-ready emerging category. Per-market resolution criteria currently a wiki gap. |
| [[llm-forecasting-by-domain]] | Where to deploy LLM forecasting: Geopolitics/Politics strong; Finance/Sports/Crypto weak. PolyBench CWR + LLM-by-domain Brier/ECE converge. News-augmentation helps Finance/Sports, hurts Entertainment/Tech. Lot-size alpha ceiling ~$100–$500. |
| [[llm-epistemic-calibration]] | KalshiBench: all frontier LLMs systematically overconfident; only Claude beats base-rate BSS; extended-reasoning calibrates worst. Temporal-filter methodology is the gold standard for contamination-free Polymarket eval pipelines. Model-naming anachronism caveat. |
| [[polyswarm-llm-trading-framework]] | 50-persona LLM swarm + Bayesian aggregation + CEX-DEX latency arb framework. No empirical P&L. Latency thesis ("several minutes" of human lag) conflicts with mature-market 0.74-min half-life — applicable only to thin/immature markets. |
| [[platform-comparison-kalshi-polymarket]] | Industry sizing (~$64B 2025, $325B+ run-rate Jan 2026); Polymarket and Kalshi at ~$400M OI each but Kalshi 3× monthly volume; tick size, fee structure (V2 March 2026), per-vertical Polymarket vs Kalshi splits, ICE capital structure, TRM 5-tier user cohort segmentation. |
| [[polymarket-bet-content-trends]] | Synthesis of *what is actually traded* — multi-source volume trajectory (2023 $73M → Feb 2026 $425M single-day), per-vertical sizing, largest named markets historical + current, user-tier P&L case studies (top wallet $6.2M / 80-day), manipulation patterns. |
| [[snapshots/polymarket-top-markets-2026-05-13]] | Dated cross-market snapshot: 20 top markets with $-vol/odds/liq (Dem 2028 Nominee $1B all-time, FIFA WC $963M / $215M liq, Eurovision $156M, Trump-China visit, three overlapping Elon Musk tweet markets). |
| [[snapshots/polymarket-crypto-category-2026-05-13]] | Dated crypto-vertical snapshot: 261 crypto markets total, Pre-Market subcategory largest (115/261); implied prices BTC ~$81k / ETH ~$2.3k / SOL ~$95 / XRP ~$1.45; 21 top markets enumerated. |
| [[conflicts/wash-trading-share]] | Open conflict: Dubach 2026 SF7 (median 1%, max 22.2%, per-market) vs Columbia Nov 2025 (25% avg, 60% Dec 2024 peak, platform-aggregate). Both stand pending methodology reconciliation. |
| [[polymarket-market-structures]] | Catalogue of 7 structural shapes Polymarket markets take: simple binary, date-ladder, candidate race, bracket bins, scenario grid, conditional bundle, mention. Per-structure arb topology + canonical 3-component resolution-rule grammar. |
| [[snapshots/polymarket-politics-category-2026-05-13]] | Politics-vertical snapshot: 22 subcategories (Midterms 544 largest, 1,600 total), 21 markets enumerated; 5 structural types present in single view; 2028 nominee complex $2.2B+ all-time vol. |
| [[snapshots/polymarket-geopolitics-category-2026-05-13]] | Combined Geopolitics (567 markets / 16 subcats) + Iran (184 markets / 12 subcats) snapshot; date-ladder term structure with conditional probabilities; Iran airspace 39%/47% is tightest live ladder. |
| [[snapshots/polymarket-midterms-category-2026-05-13]] | 2026 Midterms: 544 markets; 6 structural types; balance-of-power composite vs chamber-control binaries is a direct combinatorial-arb candidate (visible inconsistency: P(R-Sweep) implied at −12% from marginals). |
| [[snapshots/polymarket-niche-categories-2026-05-13]] | Combined Aliens (4 active, $38M flagship) + Science (20 markets, $58.7M aggregate); Kevin Warsh conditional-bundle exemplar; earthquake magnitude-ladder potential monotonicity violation flagged. |
| [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] | 6-subcategory sweep classifying mention markets vs outcome markets: Tweet Markets (28 markets, 9 speakers) is the headline cottage industry; MrBeast + Iceman partial; Taylor Swift / Reality TV / GTA VI are NOT mention markets. Includes the Gamma API smoke-test capture of the 33-sub-market Trump-Xi bilateral event. |
| [[polymarket-lp-incentives]] | The 3 distinct LP-reward programs: Liquidity Rewards (platform-funded, proximity-weighted, max-spread gate), Maker Rebates (taker-fee-funded, formula `fee_eq = C·feeRate·p·(1−p)`, Crypto 20% / others 25% rebate), Sponsor Market Rewards (third-party USDC, daily distribution, sponsor return = zero). Live Esports queue 2026-05-16: ~$3,412/Valorant series. |
| [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] | 6-category sweep filtered by retail-tractable criterion. 162 events surveyed, 45 YES / 40 PARTIAL / 77 NO. YouTube densest at 58% YES rate; Finance worst at 10%. Includes live RT-monotonicity-arb finding on "In the Grey" (P(≥55) < P(≥60)). |
| [[polymarket-strategy-matrix]] | Consolidated operator view — two edge modes (predictive vs secondary-market timing); per-theme strategy matrix (mentions / box office / streaming / YouTube / AI / crypto / corporate-event / geopolitics / scenario-grid / LP yield); 10 pure secondary-market timing patterns; signal-availability decision tree. |
| [[feasibility-review]] | **Cross-theme meta-review.** Ranks the 10 feasibility assessments by rubric + capital tier + time-to-edge; identifies top 5 live time-sensitive trades (CZ regime, D-Senate+R-House composite, MSTR May 31 on-chain, Iran airspace 8pp, MrBeast Jun 30); cross-cutting daily Σ-check watchlist; reusable infra build sequence; 5 recurring model archetypes (count-distribution / hazard / LLM keyword / Bayesian intra-period / structural-feed + Σ-check) with cross-archetype patterns. |
| [[experiments-roadmap]] | **Phase-1 validation experiments** for the 4 actionable model archetypes (A1 count-distribution, A3 LLM keyword/MixMCP, A4 Bayesian intra-period, A5 structural-feed + Σ-check). Per archetype: thesis + hypothetical edge + conditions for success + sample market + minimal run + quantitative success criteria (Brier delta, win rate, net EV, multi-leg execution viability). 4-week sequencing produces first verdict per archetype before real-capital scale-up. |
| [[feasibility/mention-markets]] | GO (16/20). 8 non-Elon tweet-count speakers + Starmer PMQs keyword-binary; CZ regime-shift live; Hansard API = resolution corpus; ICEMAN MixMCP transfer candidate. |
| [[feasibility/movies]] | Conditional YES (15/20). Box-office bracket via Thursday preview gross + comp-set lognormal; RT ladder via Beta-update with monotonicity arb; trade-press consensus is saturation tier. |
| [[feasibility/streaming-charts]] | Conditional YES (14/20). Billboard via Markov rank-transition + Chartmetric; Netflix via persistence+shock (no intra-week data); Netflix lowest pro-saturation of any chart type. |
| [[feasibility/youtube]] | YES (15/20). MrBeast subscriber + view + Day-1 bracket fully YouTube Data API v3-tractable; 58% YES rate is densest cluster on Polymarket; non-MrBeast Twitch-primary or legal. |
| [[feasibility/ai-tech-milestones]] | YES (two edge modes). Chatbot Arena structural-feed monitoring + Gemini hazard ladder + USPTO trademark tracking; Figure F.03 livestream rate-extrapolation; no GPT-6 market exists yet. |
| [[feasibility/crypto-short-horizon]] | AVOID except FDV niches. Max-saturation quant territory; resolution feed = Binance BTC/USDT 1m candles (NOT Chainlink/Pyth); Pre-Market FDV is the retail niche. |
| [[feasibility/corporate-event-binaries]] | NARROW-YES. SpaceX IPO via EDGAR S-1 + MSTR on-chain via Arkham + Anthropic vs OpenAI via Crunchbase; 26/30 Finance events out-of-scope (commodity-quant-saturated); total deployable $60K–$175K. |
| [[feasibility/geopolitical-date-ladder]] | YES with conditions. Iran cluster dominates 10:1; Saguillo term-structure monotonicity (airspace 8pp / uranium 5pp); IMF Portwatch = Hormuz resolution oracle; UMA dispute risk HIGH on consensus markets. |
| [[feasibility/scenario-grid]] | Conditional YES — LIVE MISPRICING. D-Senate+R-House composite at 1.45¢ vs ~3.0¢ (~2× underpriced); P(D House) gap 33.5pp composite vs binary; binding $112K liq → $15–30K position. May-13 −12% candidate was capture artifact. |
| [[feasibility/lp-yield-farming]] | Meta-strategy; structurally sound at right scale. Starmer cluster $200–400/day with $98–129K deployed; A-S quoting with inventory skew; fourth yield layer `holdingRewardsEnabled` discovered. |

---

## Coverage status (as of 2026-05-16)

The wiki has strong **structural / mechanics** coverage and partial **market enumeration**. Enumerated markets sit at ~150 specific markets visible across snapshots vs ~3,000+ in the universe Polymarket exposes — **roughly 3–5% explicit enumeration, ~100% structural shape coverage**.

**Per-category enumeration status (10 in-scope categories, sports excluded per user direction):**

| Category | Universe count | Wiki enumeration | Per-market depth |
|---|---|---|---|
| Politics | 1,600 | Landing + Midterms subcat (~21 + ~25 specific) | 1 (Trump-Xi via Gamma) |
| Geopolitics | 567 | Landing + Iran subcat (~20 + ~20) | 0 |
| Pop Culture / Mentions | 435 | Landing + 7 subcats + broad-sweep 6 subcats top-30 each (Movies/Music/YouTube/Celebrities classified YES/PARTIAL/NO) | 0 |
| Crypto | 261 | Landing (~21 of 261) | 0 |
| Science | 20 | Landing (20 of 20) | 0 |
| **Tech** | 526 | **Top-30 by 24h vol** via Gamma API tag_slug (2026-05-16); 8 YES / 10 PARTIAL / 12 NO | 0 |
| **Finance** | ~30+ visible | **Top-30 by 24h vol** via Gamma API; 3 YES / 2 PARTIAL / 25 NO; mostly commodity-quant-saturated | 0 |
| Weather | unknown | 0 — only Hantavirus via Science cross-tag | 0 |
| Economics | unknown | 0 | 0 |
| Other / General | unknown | 0 | 0 |

**Other dimensions:**

- **Per-market resolution rules (binding spec):** 1 of thousands captured (Trump-Xi bilateral via [[mention-markets#gamma-api-capture-workflow-per-market-resolution-rules]]). Tool exists — gap is operational.
- **Time-series for active markets:** 0 multi-date snapshots. Convention `raw/markets/<slug>/<YYYY-MM-DD>.md` documented; only 1 file written.
- **Aggregate sizing / volume trajectory:** strong — [[polymarket-bet-content-trends]] and [[platform-comparison-kalshi-polymarket]] consolidate 2023→2026 arc with cross-source reconciliation.
- **Participant cohorts:** partial — TRM 5-tier segmentation in [[platform-comparison-kalshi-polymarket]]; wallet-distribution numbers (top-0.1% / 59% / etc.) flagged but uncaptured Verge source.
- **Resolution mechanics:** strong — full UMA flow + Gamma criteria + 3-component rule grammar.
- **Modeling techniques:** strong — Kim et al. MCP, PolyBench LLM-edge, KalshiBench calibration, RN-JD kernel.

**Highest-value gaps for capture, ranked (after 2026-05-16 broad-coverage sweep):**

1. Politics subcategories beyond Midterms (Trump 305 — many mention-style — Primaries 189, Global Elections 147, US Election 146 — 787 markets). Gamma API `tag_slug` bypass works.
2. Geopolitics subcategories beyond Iran (Ukraine 106, Middle East 74, Israel 73, China 49 — 302 markets). Gamma API bypass works.
3. Per-event resolution-rule text for the YES-classified markets in [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]] (~45 events) — use `tools/capture_polymarket_market.py --slug <slug>` to grab each.
4. Per-market resolution rules for the 8 small-volume tweet speakers (cottage-industry retail target).
5. Weather / Economics / Other categories — 3 of 10 in-scope categories still with zero coverage. Gamma API bypass works (`tag_slug=weather`, `tag_slug=economics`, etc.).
6. Awards subcategory — explicitly de-prioritized per user feedback (Oscars/Emmys/Grammys saturated by Hollywood analytics).
5. Finance / Tech / Economics / Weather / Other category landing pages (5 of 10 categories with zero coverage).
6. Time-series for any 1–2 markets (the dated-snapshot pattern needs ≥2 dates to start serving its purpose).

---
