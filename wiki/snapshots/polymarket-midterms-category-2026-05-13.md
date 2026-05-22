# Polymarket 2026 Midterms — Snapshot 2026-05-13

Capture of `polymarket.com/politics/midterms`, 2026-05-13. **544 total Midterms markets** (per page FAQ); landing-page view shows a partial render of ~25 cards across **6 structural types**. The Balance-of-Power composite vs the individual chamber-control binaries is a textbook **combinatorial arbitrage candidate** — see `## Combinatorial-arb surface` below. Source: `raw/research/polymarket-politics-and-niche-markets/04-polymarket-midterms-category.md`.

The 2026 midterms ballot includes all 435 House seats, 35 of 100 Senate seats, and 36 governor races. The landing view at capture surfaced 12 House per-seat markets but **no Senate-individual-seat or Governor markets** — the page's "Show more markets" UI control indicates these exist but are below the fold; full enumeration would require deeper scroll.

## Six structural types in the captured view

### Type 1 — Chamber-control binaries (single grouped event, party-leg sub-markets)

| Market | Party leg | Odds | Vol |
|---|---|---|---|
| Which party will win the House in 2026? | Democratic Party Yes | 79% | $6M total (monthly cadence) |
| | Republican Party Yes | 23% | (same event) |
| Which party will win the Senate in 2026? | Republican Party Yes | 53% | $2M total |
| | Democratic Party Yes | 47% | (same event) |

Sums (79% + 23% = 102%; 53% + 47% = 100%) reflect Polymarket's grouped-event convention: each party leg has an independent order book, so sums approximate but do not strictly equal 1.00. Per [[polymarket-market-taxonomy]].

### Type 2 — Balance-of-power scenario grid (multi-outcome composite)

| Outcome | Odds |
|---|---|
| Democrats Sweep (D Senate ∧ D House) | 43% |
| R Senate ∧ D House | 33% |
| (R Sweep) | — (not in capture view) |
| (D Senate ∧ R House) | — (not in capture view) |

Total event vol: $7M. Visible outcomes sum to 76%; the residual ~24% is split between R-Sweep and D-Senate ∧ R-House.

### Type 3 — Seat-count bracket markets (multi-outcome numeric bins)

| Market | Bracket | Odds | Vol |
|---|---|---|---|
| Republican Senate seats after 2026 midterms | ≤47 | 26% | $2M total |
| | Exactly 50 | 19% | (same event) |
| Republican House seats after 2026 midterms | Below 190 | 26% | $231K total |
| | 190–194 | 13% | (same event) |

These imply a tradable PMF over seat totals. The captured view shows only 2 brackets per market; complete bracket sets are below the fold.

### Type 4 — Per-seat district binaries

12 House race markets visible (no Senate-individual or Governor seats in capture view):

| Race | Leading | Odds | Runner-up | Vol | Notes |
|---|---|---|---|---|---|
| KS-03 House | D | 87% | R 14% | $12K | |
| GA-04 House | D | 94% | R 5% | $24K | safe-seat |
| MS-02 House | D | 84% | R 17% | $22K | |
| FL-19 House | R | 90% | D 11% | — | NEW |
| IL-16 House | R | 88% | D 9% | $12K | |
| MI-05 House | R | 91% | D 10% | — | NEW |
| CA-34 House | D | 94% | R 4% | $24K | safe-seat |
| MA-03 House | D | 93% | R 6% | $14K | |
| OK-03 House | R | 94% | D 4% | $83K | safe-seat |
| PA-04 House | D | 93% | R 7% | — | NEW |
| LA-02 House | D | 81% | R 16% | $40K | |
| LA-06 House | R | 82% | D 16% | $57K | |

Liquidity is uniformly thin — $12K–$83K per race vs $2M–$7M for chamber-control markets. The implied liquidity asymmetry is **~100×–500×** for the same political signal.

### Type 5 — Primary winner (multi-candidate)

| Race | Candidate | Odds | Vol |
|---|---|---|---|
| NJ Republican Senate Primary Winner | Alex Zdan | 64% | $418K |
| | Richard Tabor | 33% | (same event) |

### Type 6 — Congressional map binaries

| State | Outcome | Odds | Vol |
|---|---|---|---|
| North Carolina (new map?) | Yes | 97% | $243K total |
| California (new map?) | Yes | 95% | (same event) |
| Virginia (new map?) | Yes | 9% | $38K |

## Combinatorial-arb surface

The **balance-of-power composite** (Type 2) and the **chamber-control binaries** (Type 1) are the same underlying events at different granularities. The marginals must be consistent:

```
P(D-House)  =  P(D-Sweep)  +  P(D-Senate ∧ R-House)         [marginal over Senate]
            +  P(D-Senate ∧ R-House — partial)              ... etc.

P(D-Sweep)  +  P(R-Senate ∧ D-House)  +  P(D-Senate ∧ R-House)  +  P(R-Sweep)  =  1
```

Visible numbers:
- P(D-Sweep) = 43%
- P(R-Senate ∧ D-House) = 33%
- P(D-House marginal) = 79%
- P(R-Senate marginal) = 53%, ⇒ P(D-Senate marginal) = 47%

Implied from marginals:
- P(D-Senate ∧ R-House) ≈ P(D-House) − P(D-Sweep) = 79% − 43% = **36%**
- ⇒ P(R-Sweep) ≈ 1 − 43% − 33% − 36% = **−12%** (!)

The negative residual is the smoking-gun inconsistency. Either (a) the visible 79% is a rounded composite of two independent sub-markets that don't quite agree, (b) P(R-Senate ∧ D-House) at 33% over-allocates relative to the implied P(D-Senate ∧ R-House), or (c) one of the four scenario outcomes carries a price that does not align with the marginal binaries.

**This is the [[combinatorial-arbitrage-empirics]] dependency-detection problem in its simplest form** — no LLM needed; the dependency is structurally given. The arb topology:

- If the composite is mispriced relative to the marginals, build a position in the composite that hedges via the chamber-control binaries (or vice versa).
- Depth-bounded: the per-seat / per-race markets ($12K–$83K) cannot support a hedge at scale, but the chamber-control markets ($2M–$7M) and the composite ($7M) are large enough to absorb mid-size positions.
- The exact arb size depends on a full-bracket Σ-check (Type 3 implied PMF should also be consistent with the marginals); fragments captured here do not yield the closed-form trade.

## Strategy notes per type

| Type | Where edge plausibly lives |
|---|---|
| 1. Chamber-control binaries | Model vs market (national tides); deep enough to size |
| 2. Balance-of-power composite | Joint-distribution model + combinatorial arb against marginals (above) |
| 3. Seat-count bracket | Structured Bayesian seat-by-seat model → implied PMF vs market PMF |
| 4. Per-seat district | Local model edge; very thin so size-constrained; safe seats are near-zero-edge |
| 5. Primary multi-candidate | Per-candidate poll/momentum model |
| 6. Congressional map | Legal/process binary — narrow legalistic information edge |

## Cadence and resolution

- **Cadence tags observed:** monthly (most chamber-control); daily (some); per-event for primaries.
- **Resolution date:** Election Day 2026 (early November) for chamber/seat markets; per-state schedule for primaries and map markets.
- **Resolution mechanism** per page FAQ: "official government, regulatory, or primary-source reporting." UMA backbone — see [[uma-optimistic-oracle]].

## What this snapshot does not yet enumerate

- 522 of 544 Midterms markets are below the fold — Senate per-seat (35 expected), Governor (36 expected), and many additional House races. A scroll-extended capture or per-subcategory captures would close this gap.
- Full bracket coverage for the seat-count PMFs (only 2 brackets per market visible).
- Per-market resolution-rule text (subject to the SPA capture gap — see `master_notes.md` 2026-05-12).

## Cross-references

- [[polymarket-market-structures]] — anchor for Types 1–6; this snapshot is the canonical exemplar of Type 5 (scenario grid) and Type 3 (seat-count brackets).
- [[combinatorial-arbitrage-empirics]] — the composite-vs-marginals arb topology applies the dependency-detection framework explicitly.
- [[arbitrage-taxonomy]] — both MRA (within bracket Σ-check) and combinatorial (scenario vs marginals) opportunities present.
- [[snapshots/polymarket-politics-category-2026-05-13]] — the parent politics-vertical view.
- [[polymarket-bet-content-trends]] — politics is the wiki's most-documented vertical for content trends.

## Source

- `raw/research/polymarket-politics-and-niche-markets/04-polymarket-midterms-category.md` — `polymarket.com/politics/midterms` captured 2026-05-13.
