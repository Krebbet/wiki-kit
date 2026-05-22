# Polymarket Mention Cottage Industry — Snapshot 2026-05-14

Combined capture of 6 Pop Culture subcategories, intended to answer: **which subcategories actually host retail-tractable mention markets with simple predictive strategies, and which are outcome bets in mention clothing?**

**The verdict** (against the user's `feedback_market_research_focus` criterion — tractable observable + non-saturated crowd + repeatable structure):

| Subcategory | Markets | Verdict | Why |
|---|---|---|---|
| **Tweet Markets** | 28 (20 visible + 8 below fold) | **YES — primary cottage industry** | 9 speakers × weekly cadence × 20-wide count brackets. Per-speaker base-rate (Poisson / NegBin) model is straightforward; lower-volume speakers (Khamenei, NYC Mayor, CZ) likely carry mispricing. |
| **Iceman** | 18 outcomes / 10 events | **PARTIAL** | Keyword markets ("Daddy", "Covid") exist alongside chart-race / sales / release-date markets. The keyword sub-type is the retail target. |
| **MrBeast** | 9 | **PARTIAL** — 1 mention + 8 brackets/milestones | One Structure-7 mention market ("What will MrBeast say in next YouTube video?") + bracket-bin view-counts (Day-1, Week-1) + near-100% milestone ladders. |
| Taylor Swift | 15 / 7 events | **NO** | Celebrity-lifestyle outcomes. Highest-vol $2M "pregnant before 2027" — one-shot announcement-driven, no model edge. Only Billboard chart markets are tractable; no mentions. |
| Reality TV | 12 | **NO** | All 12 are outcome bets (season winners, eliminations, casting). Same structural class as sports. |
| GTA VI | 7 | **NO** | Dominant type is cross-domain race binary ("What will happen before GTA VI?" Structure 6 conditional bundle — alien disclosure et al. — see [[polymarket-market-structures]]). |

Sources: `raw/research/polymarket-mention-cottage-industry/01-polymarket-tweet-markets.md` through `06-polymarket-gta-vi.md`, captured 2026-05-14.

## Tweet Markets — the headline cottage industry

**9 distinct speakers** across X (Twitter) and Truth Social, all running weekly 20-wide count-bracket markets:

| Speaker | Platform | Approx weekly modal count | Recent leading bracket | Recent leading odds | Vol per market |
|---|---|---|---|---|---|
| **Elon Musk** | X | 100–139 | 100–119 (May 8–15) | 53% | **$10M / $5M / $2M** across 3 rolling windows |
| Donald Trump | Truth Social | 180–199 | 180–199 (May 8–15) | 59% | $297K |
| White House | X | 180–199 | 180–199 (May 8–15) | 57% | $147K |
| Ted Cruz | X | 120–139 | 120–139 (May 5–12, near-resolution) | 97% | $44K |
| CZ (Changpeng Zhao) | X | < 20 (regime-shifting?) | <20 → 20–39 across weeks | 100% → 65% | $33K |
| Zelenskyy | X | 80–99 | 80–99 (May 8–15) | 85% | $33K |
| Khamenei | X | < 5 | <5 | 92% | $12K |
| NYC Mayor | X | 20–39 | 20–39 | 95% | $10K |

(Source: `raw/research/polymarket-mention-cottage-industry/01-polymarket-tweet-markets.md`. 28 markets total; table shows 8 of 9 speakers — Elon Musk has multiple windows live; the 9th visible-but-not-detailed speaker entry exists in the source.)

### Rolling-window overlap (Elon Musk specifically)

Three Elon Musk weekly markets simultaneously live:

| Window | Leading bracket | Odds | Vol |
|---|---|---|---|
| May 8–15 (mid-resolution) | 100–119 | 53% | $10M |
| May 12–19 (mid-week) | 120–139 | 23% | $5M |
| May 15–22 (just opened) | 100–119 | 14% | $2M |

Plus a **monthly May 2026** market ($2M vol, 520–539 leading at 7%) and a **2-day May 14–16** market ($270K vol, <40 leading at 52%).

**Structural arb candidate.** Three overlapping windows share interior days. If May 8–15 resolves at bin X, the shared days constrain May 12–19's prior. Operator pre-condition: real-time tweet-count tracking against the speaker's account.

### Implied volume tiers

- **Elon Musk: ~$19M+ aggregate** — overwhelmingly dominant; saturated by sophisticated participants.
- **Trump Truth Social: ~$333K** — second-largest.
- **White House: ~$160K**, Ted Cruz ~$66K, CZ ~$56K, Zelenskyy ~$33K, NYC Mayor / Khamenei ~$10K each.

**Operational reading.** Elon Musk markets are well-priced and crowded — model edge is hard. The eight smaller-volume speakers ($10K–$300K per market) are the retail-tractable target. CZ exhibits an active regime shift (May 5–12 `<20` at 100% → May 15–22 `20–39` at 65%) — apparent behavioral change; base-rate models need a regime-detection layer.

### Modeling spine

```
Bracket probability from Poisson:        P(N ∈ [a,b]) = P(N ≤ b) − P(N ≤ a−1),   N ~ Poisson(λ)
                                          with λ = speaker's weekly post rate

Overdispersed alternative:               N ~ NegBin(r, p)   when historical Var(N) >> E[N]

Mid-week Bayesian update:                P(bracket | k posts in t days)  ∝
                                          P(bracket) · P(k | bracket, t/7 elapsed)
                                          using truncated Poisson likelihood
```

Inputs: historical weekly post counts per speaker (scrape from X / Truth Social public timeline). Compute fit, derive bracket CDF probabilities, compare to market odds. Where market prob < model prob, take Yes side; vice versa.

### Conflicts to flag in the data

- **Khamenei brackets sum > 100%** (`<5` at 92% + `5–9` at 10% = 102%). Either rounding or non-mutually-exclusive brackets. Capture per-market resolution rules via [[mention-markets#gamma-api-capture-workflow]] to verify.
- **CZ regime shift** — model adjustment required, not a wiki conflict.

## MrBeast — partial mention category

(`raw/research/polymarket-mention-cottage-industry/02-polymarket-mrbeast.md`, 9 markets.)

**One Structure-7 mention market** (the retail-tractable target):
- "What will MrBeast say during his next YouTube video?" — Prize 68%, Hundred/Thousand/Million 10+ times 65%

**Plus 8 non-mention markets:**
- 2 bracket-bin view-count markets (Day-1: 35–40M = 40%, 30–35M = 35%; Week-1: 80–90M = 44%, 70–80M = 42%) — Structure 4, modelable but different from mention modeling
- 4 milestone/ladder markets (subscriber and total-view targets, most resolved or ≥98%) — near-zero edge
- 1 "50m views first day by May 31" simple binary (5%)
- 1 biography binary — "married by Dec 31" 72%, $37K vol — announcement-driven

**Operator focus.** The single mention market + the two view-count bracket markets together form a tight 3-market modeling target per MrBeast video release.

## Iceman — partial mention category

(`raw/research/polymarket-mention-cottage-industry/04-polymarket-iceman.md`, 18 outcomes across 10 events.)

Iceman is a podcast/show; the subcategory mixes 6 structural types:
- **Mention/keyword markets** (the cottage-industry hit: "Daddy" 87%, "Covid" 75% per [[mention-markets]] active-series matrix; 2026-05-12 capture)
- Date-ladder (release timing)
- Candidate-race (features)
- Simple binary (Billboard #1)
- Bracket-bins (sales, runtime, chart spots)
- Cross-category chart-race

Per-episode keyword markets are the cottage-industry retail target; the other 5 types are announcement-driven or sales-modeling.

## Taylor Swift — NOT the cottage industry

(`raw/research/polymarket-mention-cottage-industry/03-polymarket-taylor-swift.md`, 15 sub-markets across 7 events.)

**No mention markets at all.** All markets are celebrity-lifestyle outcomes:
- Highest-vol $2M "Taylor Swift pregnant before 2027" — one-shot announcement; no model edge.
- 2 Billboard chart markets (monthly cadence, 4 sub-markets) — tractable but not mention-style.
- Tour / album release date markets — announcement-driven.

Flag: a duplicate-event was raised on "US in May" vs "in May" chart-market pair (different scopes, similar titles).

## Reality TV — NOT the cottage industry

(`raw/research/polymarket-mention-cottage-industry/05-polymarket-reality-tv.md`, 12 markets.)

**Zero mention markets.** 12 outcome bets:
- 6 season-winner markets (multi-outcome candidate race — Structure 3)
- 1 elimination/weekly outcome
- 1 casting binary
- 1 show-event engagement (proposal during finale, etc.)
- 3 off-show celebrity status bets

Structurally similar to sports — outcome-driven, not text-resolution. User's exclusion of sports applies here by analogy.

## GTA VI — NOT the cottage industry

(`raw/research/polymarket-mention-cottage-industry/06-polymarket-gta-vi.md`, 7 markets visible.)

Dominant type: **cross-domain race binary** ("What will happen before GTA VI launches?" event grouping that pairs the GTA VI launch date with unrelated longshot legs — alien disclosure, etc. — Structure 6 conditional bundle, see [[polymarket-market-structures]]).

No first-week-sales brackets, no in-game-content mention markets at capture. Subcategory is announcement-driven.

## Cross-references

- [[mention-markets]] — the canonical reference; updated this run with the Gamma API workflow and the 9-speaker matrix.
- [[polymarket-market-structures]] — Tweet Markets is the canonical Structure 4 (bracket bins) implementation on a recurring observable.
- [[arbitrage-taxonomy]] — rolling-window Elon Musk markets have shared-interior-day constraints (MRA candidate).
- [[snapshots/polymarket-top-markets-2026-05-13]] — the prior-day cross-vertical snapshot.
- [[snapshots/polymarket-politics-category-2026-05-13]] — Trump speech mention markets and the politics-side of the cottage industry.

## Source

- `raw/research/polymarket-mention-cottage-industry/01-polymarket-tweet-markets.md` — `polymarket.com/culture/tweets-markets` captured 2026-05-14
- `raw/research/polymarket-mention-cottage-industry/02-polymarket-mrbeast.md` — `polymarket.com/pop-culture/mrbeast` captured 2026-05-14
- `raw/research/polymarket-mention-cottage-industry/03-polymarket-taylor-swift.md` — `polymarket.com/pop-culture/taylor-swift` captured 2026-05-14
- `raw/research/polymarket-mention-cottage-industry/04-polymarket-iceman.md` — `polymarket.com/pop-culture/iceman` captured 2026-05-14
- `raw/research/polymarket-mention-cottage-industry/05-polymarket-reality-tv.md` — `polymarket.com/pop-culture/reality-tv` captured 2026-05-14
- `raw/research/polymarket-mention-cottage-industry/06-polymarket-gta-vi.md` — `polymarket.com/pop-culture/gta-vi` captured 2026-05-14
