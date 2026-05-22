# Feasibility — Conditional / Scenario-Grid Markets

2026 Midterms balance-of-power composite vs chamber-control binaries; 2028 Democratic primary scenario grids. **CONDITIONAL YES.** Live mispricing in D-Senate + R-House composite leg (1.45¢ vs ~3.0¢ implied) and R-Sweep (22.5¢ vs ~18.5¢). Underlying structural inconsistency: composite-implied P(D House) 44.95% vs standalone binary 78.5% — 33.5pp gap. Binding constraint: thin D-Senate + R-House leg ($112K liq, ~$15–30K effective position). Expected gross ~$200–$400/round-trip. Live Gamma API 2026-05-16.

## Live state

**Balance-of-Power composite (`balance-of-power-2026-midterms`, $6.79M total vol, $560K liq, end 2026-11-03):**

| Outcome | Price | Vol | Liq |
|---|---|---|---|
| D Senate, D House | 43.5¢ | $1.72M | $161.6K |
| R Senate, D House | 33.5¢ | $1.37M | $101.6K |
| R Senate, R House | 22.5¢ | $1.33M | $123.3K |
| D Senate, R House | **1.45¢** | $1.04M | **$112.0K** |
| Other | 0.85¢ | $1.33M | $62.8K |
| **Σ** | **101.8%** | | |

**Chamber-control binaries:**

| Market | Outcome | Price | Vol | Liq |
|---|---|---|---|---|
| House | Democratic | **78.5¢** | $3.39M | $306.9K |
| House | Republican | 21.5¢ | $2.88M | $240.6K |
| Senate | Republican | 55.5¢ | $1.11M | $156.1K |
| Senate | Democratic | 46.5¢ | $1.28M | $161.2K |

**Per-seat district markets:** $12K–$83K per race — ~100×–500× thinner than chamber-control.

## The May 13 -12% candidate — NOT LIVE

Prior snapshot in [[snapshots/polymarket-midterms-category-2026-05-13]] showed only D-Sweep (43%) + R-Senate+D-House (33%); inferred P(R-Sweep) = -12% residual. **Artifact of partial UI capture.** With all four legs visible in live data, R-Sweep trades 22.5¢ (positive). The original arb candidate is **NOT LIVE**.

## The live live mispricing

```
Composite-implied P(D House) = P(D Sweep) + P(D Senate & R House)
                              = 43.5% + 1.45% = 44.95%

Chamber-control standalone P(D House) = 78.5%
Gap: +33.55pp

Composite-implied P(R Senate) = P(R Senate & D House) + P(R Sweep)
                                = 33.5% + 22.5% = 56.0%
Standalone P(R Senate) = 55.5%
Gap: 0.5pp (negligible)
```

Senate marginals are consistent. House marginal is severely inconsistent. The **D-Senate + R-House leg at 1.45¢ is the culprit**.

**If chamber binaries are correct:**
- P(D Senate & R House) should ≈ P(D Senate) − P(D Sweep) = 46.5% − 43.5% = **3.0%** — market prices 1.45% (~2× underpriced).
- P(R Sweep) should ≈ 1 − 43.5% − 3.0% − 35.0% = **18.5%** — market prices 22.5% (~4pp overpriced).

**Arb topology:**
- Buy D-Senate + R-House YES (1.45¢, $112K liq) — the underpriced leg.
- Hedge: Sell R-Sweep YES (22.5¢, $123K liq) — the overpriced leg.
- Or cross-market: Long D-Senate + R-House composite + Short Democratic House binary (78.5%) + Long Republican Senate binary (55.5%).

**Binding constraint:** D-Senate + R-House liq $112K caps effective position ~$15–30K. At 1.45¢ entry on $30K with ~3.0¢ fair → gross ~$465 unhedged; hedges reduce to **~$200–$400 net per round-trip**.

## Joint-distribution check

```
P(D Senate | D House wins) = P(D Sweep) / P(D House)
                            = 43.5 / 78.5 = 55.4%
```
Above standalone P(D Senate) = 46.5%. Unusual: D-Senate is harder 2026 terrain; a wave big enough to flip the House does not obviously raise the conditional. Composite may express that crowd disagrees with binary on House — i.e., composite participants think P(D House) is closer to 45% than 78.5%.

## Data sources

| Source | Signal | Coverage |
|---|---|---|
| FiveThirtyEight / Silver Bulletin | Seat ratings + generic ballot + district forecasts | All 35 Senate + ~40 competitive House |
| RealClearPolitics | Polling averages by race + generic ballot | Competitive subset |
| FEC EDGAR | Cash-on-hand by candidate | All 435 House + 35 Senate |
| OpenSecrets | Competitive-race fundraising tracker | Top-100 |
| Decision Desk HQ | Per-seat win probabilities | All races |
| Inside Elections / Sabato | Qualitative tier ratings | All races |

## Modeling spine

```
S_i = P(D wins Senate seat i),  i = 1..35
H_j = P(D wins House seat j),   j = 1..435

P(D Senate majority) = P(Σ S_i + D_held ≥ 50)
P(D House majority)  = P(Σ H_j ≥ 218)
```
Joint correlation via single national-environment factor (generic ballot); historical ρ ≈ 0.6–0.8 between Senate and House chamber outcomes.

### Consistency summary

| Check | Composite-implied | Chamber binary | Model-implied | Verdict |
|---|---|---|---|---|
| P(D House) | 44.95% | 78.5% | ~75–80% | Composite severely low |
| P(R Senate) | 56.0% | 55.5% | ~50–58% | Consistent |
| P(D Sweep) | 43.5% | — | ~35–45% | Plausible |
| P(R Sweep) | 22.5% | — | ~10–20% | Mildly high |
| P(D Senate & R House) | **1.45%** | — | **~2–4%** | **Underpriced** |

## Structural-arb shape

- **Composite-vs-marginals (intra-composite):** Σ = 101.8% — minor MRA long opportunity per [[arbitrage-taxonomy]] §3.
- **Composite-vs-binary cross-market:** 33.5pp gap on P(D House) is the dominant inconsistency.
- **Per-leg targeted:** D-Senate + R-House at 1.45¢ vs ~3.0¢ fair → ~2× underpricing.

## Microstructure regime

| Market | Liq | Vol_all | Arb size cap |
|---|---|---|---|
| D Sweep | $161.6K | $1.72M | ~$30–60K |
| R Senate & D House | $101.6K | $1.37M | ~$20–40K |
| R Sweep | $123.3K | $1.33M | ~$25–50K |
| **D Senate & R House (thin)** | **$112K** | $1.04M | **~$15–30K** |
| House Dem binary | $306.9K | $3.39M | ~$50–100K |
| Senate Rep binary | $156.1K | $1.11M | ~$30–60K |
| Per-seat district | $12K–$83K | — | $2K–$10K |

Per-seat $12K–$83K vs chamber-control $2M–$7M depth asymmetry confirmed (matches May-13 snapshot).

## Saturation

1. **Election forecasters (538-style):** Sophisticated models, don't directly trade Polymarket. Public output near-free for any operator → ingesting these is saturated.
2. **PredictIt cross-traders:** Known to cross-trade; PredictIt $850 cap drives familiarity. Likely monitor composite-vs-marginals.
3. **Polymarket-native bots:** [[combinatorial-arbitrage-empirics]] top wallet $2M extracted via 4,049 transactions. Midterms composite-vs-binary semantic dependency is more complex than simple within-market MRA — fewer bots have this dependency loaded.
4. **Retail:** Dominate per-seat district markets; directional, not arb.

**Saturation verdict:** Chamber-control binaries well-saturated relative to fundamentals (78.5% D-House aligns with mainstream forecasting). Composite's D-Senate + R-House underpricing is **less saturated** because: (a) multi-leg dependency map required, (b) thin leg makes size-sensitive bots averse, (c) mispricing is in a low-attention leg.

## 2028 Democratic primary scenario grids

**Current state:** `2028 Democratic Presidential Nominee` event ($1.14B lifetime vol, $60.8M liq). NegRisk multi-candidate (Ossoff 6.25%, Buttigieg 4.25%, Beshear 2.75%, Clooney 0.65%, Oprah 0.75%, Raimondo 0.75%). **No scenario-grid composite (nominee × VP, nominee × Senate) visible as of 2026-05-16.**

**Why grids don't yet exist:** 2028 primary is 2+ years out; scenario composites require both legs well-defined and simultaneously active. VP pick market for 2028 does not exist yet.

**Per-candidate MRA check:** Each binary (YES + NO) sums to 100% — properly priced. Cross-candidate NegRisk Σ > 1.00 is by design, not exploitable per [[arbitrage-taxonomy]] §3.2.2 fn 7.

**Feasibility for 2028 scenario grids:** Monitor from ~mid-2027 when VP / running-mate markets activate. **Not actionable today.**

## Implementation

**Step 1 — Dependency map (one-time, no LLM):** P(D House) = P(D Sweep) + P(D Senate + R House). Document 6-leg dependency graph.

**Step 2 — Price monitor (5–15min poll):**
```
gap_house          = P(D House binary) − [P(D Sweep) + P(D Senate & R House)]
gap_senate         = P(R Senate binary) − [P(R Senate & D House) + P(R Sweep)]
gap_composite_sum  = Σ P(composite_legs) − 1.00
```
Alert when |gap_house| > 5pp OR |gap_senate| > 3pp OR |gap_composite_sum| > 2%.

**Step 3 — Joint-distribution prior (weekly):** Pull Decision Desk / Silver Bulletin per-seat probabilities; fit two-factor correlated Bernoulli; output P(D Senate), P(D House), joint PMF.

**Step 4 — Sizing/execution:** Size to thin-leg liq (~$15–30K). Limit orders on CLOB. Monitor partial-fill risk on 4-leg arb.

**Step 5 — Fundamental overlay:** Where composite-vs-binary > model fair by >5pp, add directional view from per-seat priors.

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Partial-fill on multi-leg arb | High | Execute largest/most-liquid legs first |
| Composite reprices before hedge fills | High | Limit-order both legs simultaneously |
| D-Senate + R-House leg-fill risk (thin) | Med-high | Size conservatively $15–20K; limit orders only |
| Resolution-rule divergence (composite vs binaries) | Medium | Composite cites AP/Fox/NBC consensus; verify chamber binary uses same threshold |
| "Other" outcome resolves (independent winner) | Low | 0.85¢ Other is real tail; composite positions exposed |
| PredictIt cross-traders close gap | Medium | Gap is large (33.5pp on House); closes over weeks not days |
| UMA dispute | Low | Election calls are low-dispute; precedent established |

## Decision-tree mapping

1. **Q1 YES-theme?** YES — combinatorial-arb is a documented edge type per [[polymarket-strategy-matrix]].
2. **Q2 Data source?** YES — Gamma API for prices; Decision Desk + Silver Bulletin for joint-distribution prior (free/public).
3. **Q3 Structural-arb?** YES — composite-vs-binary inconsistency 33.5pp; D-Senate + R-House underpriced 2×.
4. **Q4 Microstructure?** Thin D-Senate + R-House leg ($112K liq) is binding; CLOB limit orders required.

## Open follow-ups

1. Gamma API monitor for gap_house / gap_senate / gap_composite_sum.
2. Pilot $5–10K position in D-Senate + R-House YES against Republican House binary hedge.
3. Per-seat joint-distribution model build from Decision Desk + Silver Bulletin.
4. Defer 2028 primary scenario-grid work to ~mid-2027 (VP-pick market emergence dependent).
5. Resolution-rule comparison composite vs chamber binary (AP/Fox/NBC consensus — same source?).

## Source

- `raw/feasibility/scenario-grid/summary.md` (2026-05-16)
- Gamma API `/events?tag_slug=midterms` + `/events?slug=balance-of-power-2026-midterms` (2026-05-16)
- Gamma API `/events?tag_slug=primaries` (2026-05-16)
- [[snapshots/polymarket-midterms-category-2026-05-13]]

## Related

- [[snapshots/polymarket-midterms-category-2026-05-13]]
- [[arbitrage-taxonomy]]
- [[combinatorial-arbitrage-empirics]]
- [[polymarket-strategy-matrix]]
- [[uma-optimistic-oracle]]
- [[polymarket-architecture]]
- [[feasibility-review]]
