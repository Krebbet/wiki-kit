# Reference Sources

The watched-source set for `/weekly-brief` on this wiki, plus the scope/selection/conventions that **override** the kit defaults. The kit skill is written for an AI/ML paper-radar; this wiki is a quant-operational reference for prediction-market arbitrage and trading-strategy design, so the `## Scope`, `## Signal hierarchy`, `## Selection priority`, and `## Local conventions` sections below take precedence over anything in `.claude/commands/weekly-brief.md`.

## Scope

**In scope** (a brief blends all four — see [[experiments-roadmap]] and the open [[conflicts/wash-trading-share]] for the threads it feeds):

- **Platform & structure changes** — Polymarket / Kalshi fee schedules, new market types, LP/reward programs, resolution-rule and oracle schema changes, UMA dispute mechanics. The operating environment the strategies run in.
- **Live mispricing / arb signals** — structural arb, monotonicity violations, term-structure gaps on tracked markets. No dedicated live-data capture tool exists yet, so these route to `wiki/watchlist.md` + [[experiments-roadmap]] as follow-ups rather than the capture pipeline.
- **Research radar** — new papers (arXiv `q-fin.TR/PR/MF`, `cs.CL/LG`, `stat.ML`; SSRN FEN) on market microstructure, arbitrage, calibration, and LLM forecasting. Captured as wiki pages, matching the existing research backbone.
- **Experiment status** — phase-1 checkpoints from [[experiments-roadmap]] (A1/A3/A4/A5): initiation dates, first verdicts, Brier/EV results, new conflicts opened.

**Out of scope:**

- Generic crypto price commentary, token launches, or DeFi yield that doesn't bear on a prediction-market edge.
- Politics/sports punditry for its own sake (we track *market structure and mispricing*, not who's winning).
- Pure AI/ML model-release news unless it changes KalshiBench/PolyBench replicability or LLM-forecasting tractability.

## Signal hierarchy (overrides skill defaults)

Ignore the skill's AI/ML aggregator list (alphaXiv, r/MachineLearning, AK's X timeline). Scan, cheapest to most expensive:

1. **Platform feeds** (Tier 2) — Polymarket/Kalshi blog + docs/release notes for structural changes. Highest operator relevance.
2. **Native market data** (Tier 1) — Gamma / Kalshi APIs for volume deltas, new high-liquidity markets, and structural-arb shapes on tracked markets.
3. **Research feeds** (Tier 3) — arXiv q-fin + cs.CL/LG recent listings and SSRN FEN for new microstructure/forecasting papers.
4. **Commentary** (Tier 4) — a small set of prediction-market operator accounts for what practitioners are flagging.

A candidate that surfaces across ≥2 of these is a strong capture/watchlist signal.

## Selection priority

Lead every selection with the **edge-tractability filter** (per the operator's standing research-focus guidance), then the usual cross-confirmation rules:

1. **Edge-tractability** — favor *tractable-observable + non-saturated-crowd + repeatable-structure* edges: mention markets, crypto Up/Down, calendrical/regulatory events. **Downweight** saturated, illiquid, or one-off markets: Senate-race horse-races, pandemic/one-shot geopolitical bets.
2. **Multi-source cross-confirmation** — surfaced by ≥2 signals (platform + research, or data + commentary) beats single-source mention.
3. **Load-bearing for an open thread** — resolves or advances an open [[conflicts/wash-trading-share]] (or any new conflict file) or an [[experiments-roadmap]] archetype.
4. **Mechanism novelty over volume** — one new arb/forecasting mechanism > five reframings of an existing one.
5. **Reproducibility** — released data/code > promised > closed.

**Hard skip:** vendor marketing with no mechanism, restated odds without structure, anything failing the edge-tractability filter at #1.

## Required briefing coverage

Independent of the ≤5-capture cap, every brief must carry:

1. **Platform/structure delta** — any Polymarket/Kalshi fee, market-type, reward, or resolution change this week (or "none observed").
2. **Live arb watch** — status of the tracked structural arbs in `wiki/watchlist.md` (re-checked, still open / closed / new violation).
3. **Experiment status** — one line per in-flight [[experiments-roadmap]] archetype that moved.
4. **Research captures** — the ≤5 ingested + watchlist overflow.

## Local conventions

- **Voice:** math-first, terse, facts-first, no hedging — match `wiki/CLAUDE.md`. Audience is a single quant operator; don't define Kelly, Brier, EV, or standard microstructure terms.
- **Date every claim** — prices, liquidity, and fee facts go stale fast; stamp them.
- **Cite or it didn't happen** — every claim points to a `[[wiki-link]]` or a `raw/` path; flag low-sample evidence.
- **Cadence:** weekly, Monday 08:45 America/Toronto (see `## Weekly sweep schedule`).
- **Autonomous:** no human gate mid-run; the brief + the uncommitted diff are the audit trail.
- **Don't commit** — leave `wiki/` and `raw/research/weekly-<DATE>/` uncommitted; the user commits after review.
- **Kit-level learnings** → append to `master_notes.md` with `Status: open`; don't harvest in the same run.

## Status vocabulary

- **active** — sweep every `/weekly-brief` run.
- **probation** — recently added or unverified; sweep, but drop after 2 empty runs. New entries below start here until a run confirms they're reachable + high-signal.
- **retired** — kept for provenance; do not sweep.

## How `/weekly-brief` and `/lint` evolve this list

- A source that yields a capture or load-bearing watchlist entry → promote `probation` → `active`.
- A source bot-walls the capture script or returns nothing for 2 runs → demote toward `retired`; record bot-walls under `## Known bot-walled hosts`.
- New high-signal sources surfaced mid-run get appended as `probation` with the run date in `Added`.

---

## Tier 1 — Native market data

No dedicated capture tool yet — monitor for volume/liquidity deltas and structural-arb shapes; route findings to `wiki/watchlist.md`.

| Source | URL | Role | Added | Status |
|---|---|---|---|---|
| **Polymarket Gamma API** | https://gamma-api.polymarket.com | markets by `tag_slug`, live liquidity/volume, monotonicity-arb detection | 2026-05-25 | active |
| **Polymarket CLOB API** | https://docs.polymarket.com | order-book depth for execution-limit checks | 2026-05-25 | active |
| **Kalshi API** | https://trading-api.readme.io | parallel structure/fee data; mention-market cross-validation | 2026-05-25 | probation |

## Tier 2 — Platform & structure feeds

| Source | URL | Role | Added | Status |
|---|---|---|---|---|
| **Polymarket blog** | https://polymarket.com/blog | fee changes, new market types, LP/reward programs | 2026-05-25 | active |
| **Polymarket docs** | https://docs.polymarket.com | resolution-rule + oracle schema changes | 2026-05-25 | active |
| **Kalshi blog** | https://kalshi.com/blog | structural patterns, accuracy findings, fee changes | 2026-05-25 | probation |
| **Kalshi docs** | https://docs.kalshi.com | market-type + settlement schema changes | 2026-05-25 | probation |
| **UMA / oracle** | https://docs.uma.xyz | optimistic-oracle dispute mechanics (see [[uma-optimistic-oracle]]) | 2026-05-25 | probation |

## Tier 3 — Research feeds

| Source | URL | Role | Added | Status |
|---|---|---|---|---|
| **arXiv q-fin.TR** | https://arxiv.org/list/q-fin.TR/recent | trading & market microstructure | 2026-05-25 | active |
| **arXiv q-fin.PR** | https://arxiv.org/list/q-fin.PR/recent | pricing of securities | 2026-05-25 | active |
| **arXiv q-fin.MF** | https://arxiv.org/list/q-fin.MF/recent | mathematical finance / arbitrage | 2026-05-25 | active |
| **arXiv cs.CL** | https://arxiv.org/list/cs.CL/recent | LLM forecasting, calibration, structured-event prediction | 2026-05-25 | active |
| **arXiv cs.LG / stat.ML** | https://arxiv.org/list/cs.LG/recent | forecasting models, agentic time-series | 2026-05-25 | probation |
| **SSRN Financial Economics Network** | https://www.ssrn.com/index.cfm/en/fen/ | empirical arbitrage, prediction-market studies | 2026-05-25 | probation |

## Tier 4 — Commentary & operator intelligence

Low SNR; populate/validate on first sweep. Official accounts are `active`; individual operators start `probation` until a run confirms signal.

| Source | URL | Role | Added | Status |
|---|---|---|---|---|
| **Polymarket (X)** | https://x.com/Polymarket | platform announcements | 2026-05-25 | active |
| **Kalshi (X)** | https://x.com/Kalshi | platform announcements | 2026-05-25 | active |
| **Domer (X)** | https://x.com/Domahhhh | known Polymarket trader; live mispricing chatter | 2026-05-25 | probation |

## Known bot-walled hosts

_(none recorded yet — append host + workaround as capture scripts hit walls)_

## Weekly sweep schedule

```
45 8 * * 1 cd /home/david/code/wiki-polymarket && git checkout polymarket-wiki && /home/david/.local/bin/claude -p --dangerously-skip-permissions "/weekly-brief" >> /tmp/weekly-brief-polymarket-cron.log 2>&1
```

Monday 08:45 America/Toronto (08:00 slot is taken by another wiki). If the machine is off at fire time, the run is skipped — no catch-up.

## Related

- [[CLAUDE]] — wiki operating manual
- [[index]] — content catalog
- [[experiments-roadmap]] — phase-1 archetypes the brief tracks
- [[watchlist]] — the radar the brief is centered on
