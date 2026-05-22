# Conflict — Polymarket Wash Trading Share

Two captured sources report incompatible-looking wash-trading shares on Polymarket. **The conflict is not yet resolved.** Both findings stand on the wiki with their methodology and scope qualifiers preserved; do not collapse to a single number until further data closes the gap.

| Source | Wash share reported | Methodology | Time window | Scope |
|---|---|---|---|---|
| Dubach (2026) — cited in [[polymarket-microstructure]] SF7 | **Median 1%, p99 10.6%, max 22.2%** | "Lower-bound" metric (self-described); per-market computation across cross-section | Feb 21 – Apr 15, 2026 | 600 markets (top-100 by volume + random 500) |
| Columbia University study (Nov 2025) — cited in Sacra `raw/research/polymarket-market-content-and-sizing/02-sacra-polymarket.md` | **Average 25% (trailing 3-year), peak ~60% (Dec 2024)** | Not detailed in Sacra summary; "wash trading averaged 25% of activity" | 3-year trailing as of Nov 2025; peak measured Dec 2024 | Polymarket platform-wide |

## Why both can be true simultaneously

1. **Methodology gap.** Dubach calls his metric "lower-bound" — designed to count only confidently-identified wash trades and accept false negatives. Columbia's methodology is not in the captured corpus; if it uses a broader definition (e.g., a network-graph-based detection that catches more indirect cycles), the larger headline is consistent.
2. **Time-window gap.** Dubach measures Feb–Apr 2026 — a year and a half *after* the Columbia study's Dec 2024 peak. The 2024 election cycle plausibly involved more wash trading (incentive programs, attention) than the post-election regime.
3. **Denominator difference.** Dubach reports a **per-market median** (1%) — typical market is barely affected. Columbia reports an **aggregate share of platform activity** — heavily skewed by a small number of large markets where wash is concentrated. These are not the same statistic. p99 across Dubach's 600 markets is 10.6%; max is 22.2%. If those high-wash markets carried disproportionate volume during the election, an *aggregate* share of 25% is arithmetically compatible with a *median* of 1%.
4. **Scope difference.** Dubach is the top-100-by-volume stratum + random-500 sample. Columbia is platform-wide — which includes the long tail of small markets that may have systematically different wash incentives.

## Why neither is fully credible until reconciled

- Dubach's "lower-bound" caveat means his numbers may understate.
- Columbia's number is cited via Sacra; the wiki has not ingested the Columbia paper directly. Methodology and exact scope are not in-corpus.
- Polymarket itself has not published a wash-trading measurement that would adjudicate.

## What to do about it operationally

- **Use Dubach's per-market p99 (10.6%) as the conservative ceiling for any single-market backtest.** SF7's median-1% reading is the right anchor for a per-market sanity check.
- **Use Columbia's 25% as the conservative discount for any platform-aggregate volume claim** during peak periods (Dec 2024 election; potentially Sep 2025+ surge per [[polymarket-bet-content-trends]]). When citing aggregate volume, flag that the underlying may overstate organic activity by up to 25%.
- **Do not silently reconcile.** Until a third source resolves methodology, both numbers stay on the wiki with their qualifiers.

## Open follow-ups to close the conflict

1. **Ingest the Columbia University study directly.** Sacra cites it; the paper itself is not in the corpus. A direct read would establish methodology and resolve scope.
2. **Compute Polymarket wash share with the volume-decomposition framework from [[polymarket-liquidity-evolution]].** The V^E / V^G accounting (Tsang & Yang) is methodologically clean and reproducible — running it on a post-Sep-2025 sample would give the wiki a third independent measurement.
3. **Cross-check against Allium / Dune dashboards.** Falcon X used Allium for volume figures (see [[platform-comparison-kalshi-polymarket]]). On-chain wash-detection on Allium would be an alternative measurement vector.

## Pages that should know about this conflict

- [[polymarket-microstructure]] — SF7 (Dubach) currently cited without the Columbia counter-finding. Should add a "see also" pointer here.
- [[polymarket-bet-content-trends]] — flagged in its Manipulation/integrity section.
- [[platform-comparison-kalshi-polymarket]] — volume claims should carry a wash-share discount caveat for peak periods.
- [[polymarket-liquidity-evolution]] — the V^E / V^G volume-decomposition methodology is the natural third measurement vector.

## Source

- `raw/research/polymarket-types-and-opportunities/02-polymarket-microstructure.md` — Dubach 2026 SF7 (already in wiki via [[polymarket-microstructure]]).
- `raw/research/polymarket-market-content-and-sizing/02-sacra-polymarket.md` — Sacra profile citing Columbia University study (Nov 2025).

## Status

**Open.** Awaiting Columbia study direct ingest or a third measurement. Conflict last reviewed 2026-05-13.
