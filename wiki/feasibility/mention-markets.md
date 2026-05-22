# Feasibility — Mention Markets

Tweet-count brackets + keyword-binary speech markets. Strongest YES of the 10 themes (16/20). Academically-validated method (MixMCP Brier 0.1402→0.1392 on Kalshi per [[mention-markets]]), structurally rich arb surface, and a well-enumerated cottage industry of 9+ speakers with tractable Poisson/NegBin count models. The 8 non-Elon speakers ($10K–$300K vol/market) are the retail-accessible entry point. Live Gamma API pull 2026-05-16.

## Rubric (out of 20)

| Dimension | Score | Notes |
|---|---|---|
| Data availability | 5 | X API + Truth Social RSS + Hansard API + YouTube auto-captions + FOMC transcripts — free/<$50/mo |
| Modeling tractability | 4 | Count: Poisson/NegBin CDF trivial. Keyword: MixMCP needs LLM inference + corpus pipeline |
| Market depth/sizing | 3 | Non-Elon $5K–$300K/week caps positions at $2K–$5K/bin; Elon series saturated |
| Non-saturation | 4 | Elon saturated; non-Elon thin volume → low sophistication; CZ regime-shift uncontested |
| **Total** | **16/20** | |

## Top 5 markets to attack

| Rank | Slug | Vol_24h | Vol_all | Why |
|---|---|---|---|---|
| 1 | `cz-binance-of-tweets-may-15-may-22-2026` | $53K | $57K | Active <20→20–39/wk regime shift; stale priors before mid-week update |
| 2 | `what-will-keir-starmer-say-at-the-next-prime-ministers-questions-event-154` | $0.4K | $34K | Hansard API = resolution corpus; 30 sub-markets; very low saturation |
| 3 | `nyc-mayor-of-tweets-may-12-may-19-2026` | $2K | $6K | Thinnest tier; clean Poisson; low-risk model validation |
| 4 | `what-will-be-said-on-iceman` | $23K | $104K | Non-political; stable show format; 32 sub-markets; YouTube transcript T |
| 5 | `zelenskyy-of-tweets-may-15-may-22-2026` | $1K | $6K | Disciplined ~80–140/wk cadence; geopolitical regime filter trades |

Speaker volume tiers: Elon ~$2–7M/window (saturated); Trump TS ~$58K; CZ $9–57K (regime-shift); Ted Cruz ~$12K; Zelenskyy/NYC Mayor/Khamenei <$10K each.

## Data sources

- **X API v2** (`GET /2/users/:id/tweets`) — free tier 500K reads/mo, sufficient for 8 non-Elon speakers; minutes lag.
- **Truth Social RSS** (`truthsocial.com/@realDonaldTrump.rss`) — free; minutes lag.
- **YouTube Data API v3** + `youtube-transcript-api` — free; auto-captions for MrBeast, ICEMAN, JRE, All-In, Lemonade Stand.
- **UK Parliament Hansard API** (`api.parliament.uk`) — free; T+2–4h post-PMQs; resolution-corpus identity.
- **FOMC transcripts** (`federalreserve.gov`) — free; intra-event monitoring for live press conferences.

## Modeling spine

**Count brackets (Poisson/NegBin):**
```
N_week ~ Poisson(λ)     if Var(N) ≈ E[N]
N_week ~ NegBin(r, p)   if Var(N) >> E[N]   (Musk overdispersed)
P(N ∈ [a,b]) = CDF(b) − CDF(a−1)
```
Mid-week Bayesian update: `P(bracket | k obs in t/7 elapsed) ∝ Poisson(k; λ·t/7) · prior`. With 4 of 7 days elapsed, posterior collapses sharply — this is where intra-week edge lives. Closed-form; sub-second per event.

**Keyword-binary (MixMCP, Kim et al. per [[mention-markets]]):**
```
p_mcp = LLM_θ(T, N | p_mkt)                # T = prior transcripts, N = recent news
p_mix = 0.7·p_mkt + 0.3·p_mcp
```
Edge concentrates in `p_mkt ∈ [0.5, 0.7]` per disagreement-subset analysis (MCP wins 56.7% at 50–60%, 62.5% at 60–70%; loses at tails). Brier gain 0.0010 absolute — meaningful only across portfolio of mid-confidence bins.

**Threshold count (Starmer "Mr. Speaker 10+/20+"):** Predict continuous latent count via regression, then threshold. Likely outperforms direct binary prompting; not empirically validated on Polymarket (gap flagged in [[mention-markets]] Open Research Q4).

## Structural-arb shape

- **Rolling-window overlap arb (Elon Musk multi-window):** May 12–19 / May 14–16 / May 15–22 share interior days. If May 14–16 resolves 65–89 (98% prob), it constrains May 12–19's plausible bracket via accumulation lower bound — no-model bracket-elimination trade. Needs real-time X API tracking.
- **Bracket Σ-check:** ΣP(bracket_i) ≈ 1.00 enforced; deviations >2–3 pp are MRA per [[arbitrage-taxonomy]] §3. Khamenei <5 + 5–9 sums to ~102% (boundary case). Daily Σ-check across all 20 tweet-market events = one API call.
- **Count-threshold monotonicity (Starmer 10+/20+):** P(20+) ≤ P(10+) must hold. Currently P(20+)=0.66, P(10+) inferred ≥0.89 (consistent). Any P(20+) > P(10+) is direct MRA, zero modeling.

## Microstructure regime

- **Thin-market regime (non-Elon $5K–$50K/week):** Wide spreads, patient limit-order LP viable; first-mover advantage in first 12–24h of newly-opened windows.
- **Regime-shift moments (CZ, newly-opened windows):** Stale priors in market PMF before mid-week observations update — directional edge without LLM infra.
- **Longshot tail bins (binary keyword):** Rare words priced 5–15% Yes; 650–900 bps half-spread per [[polymarket-microstructure]] SF1. Patient limit-order LP on clearly-Yes bins.

## Saturation

- **Elon Musk tweet-count (~$14M+ aggregate):** Near-certainly modeled by 2–3+ sophisticated retail; assume near-zero edge without real-time X API + outperformance.
- **Trump TS / White House / Ted Cruz:** Moderate; public RSS = easy count check, but proper NegBin fitting non-trivial. ~1–3 sophisticated models.
- **CZ active regime shift:** Highest-probability candidate; stale models on historical <20/wk cadence; regime not yet priced.
- **Zelenskyy / NYC Mayor / Khamenei:** Very low; thin volume implies few sophisticated participants.
- **MixMCP keyword-binary:** Academic methodology not yet widely deployed at retail; mid-confidence band uncontested.

## Decision-tree mapping

1. **Q1 YES-theme?** YES — count + keyword-binary structures both have documented modeling per [[polymarket-strategy-matrix]].
2. **Q2 Data source available?** YES — X API, Truth Social RSS, YouTube captions, Hansard API; all free/low-cost.
3. **Q3 Structural-arb shape?** YES — overlap arb, Σ-check, monotonicity.
4. **Q4 Microstructure regime?** YES — thin-market LP + regime-shift mispricing.

## Open follow-ups

1. Build X API + Truth Social RSS backfill for 8 non-Elon speakers; fit per-speaker Poisson/NegBin; compare to current open windows.
2. CZ May 19–26 window ($1.2K vol, just opened) — same-week regime-shift trade; time-sensitive.
3. Pull last 10 PMQs from Hansard; compute per-keyword base-rates across 30 Starmer sub-markets; flag 50–70% mid-confidence discrepancies.
4. Daily bracket Σ-check tool wired to `gamma-api.polymarket.com/events?tag_slug=tweets-markets&active=true`; log violations >3 pp.
5. Prototype MixMCP on ICEMAN prior-episode corpus — cleanest non-political test bed; 32 bins per episode; 3–5 episode dry-run before capital.

## Source

- `raw/feasibility/mention-markets/summary.md` (2026-05-16)
- Gamma API live pulls: `tag_slug=mention-markets`, `tag_slug=tweets-markets`
- [[mention-markets]]
- [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]

## Related

- [[mention-markets]]
- [[polymarket-strategy-matrix]]
- [[polymarket-market-structures]]
- [[arbitrage-taxonomy]]
- [[polymarket-microstructure]]
- [[llm-forecasting-by-domain]]
- [[feasibility-review]]
