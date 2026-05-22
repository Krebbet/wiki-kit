# Mention Markets

**Mention markets** are binary prediction-market contracts that resolve on whether a specified keyword or phrase appears in a future publicly-observable corpus — a speech, a podcast episode, a tweet, a newspaper headline, an esports broadcast. They are the **emerging category most-directly suited to text-based modeling** because the resolution observable is itself textual: the same modality as the model.

This page covers (1) Polymarket's Mentions category as it exists today, with a captured snapshot of active markets and subcategory counts, and (2) the Kalshi-validated **Market-Conditioned Prompting (MCP)** technique that beats the market baseline by Brier on earnings-call mention markets (Kim et al. 2026, arXiv 2602.21229). The MCP methodology is platform-portable but **has not been validated on Polymarket-specific mention markets**; bridging that gap is the immediate operator-side research direction.

**Capture-gap resolved 2026-05-14.** `tools/capture_polymarket_market.py` was implemented and smoke-tested; per-market resolution-criteria text is now reachable via the Gamma API. See [Gamma API capture workflow](#gamma-api-capture-workflow-per-market-resolution-rules) below for usage. The wiki's lint check that every market page must link its resolution criteria is now technically unblocked; the practical bottleneck is now scoping which markets warrant per-market wiki pages.

## Pop Culture vertical — overview pointer

Mention markets sit inside Polymarket's broader Pop Culture parent category (435 markets / 14 subcategories at 2026-05-12 capture). For the **full-vertical overview** — which subcategories are mention-markets vs outcome-bets, per-market $-volumes, structural-shape mix — see [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]. The TL;DR: only 3 of the 6 captured 2026-05-14 subcategories (Tweet Markets, MrBeast, Iceman) actually host mention-style markets; Taylor Swift, Reality TV, GTA VI, Aliens are outcome/announcement-driven. The 4 largest subcategories by count (Celebrities 78, Movies 73, Awards 72, Music 70) remain unenumerated and are the natural next capture target.

## What a mention market is

(Source for Polymarket category: `raw/research/polymarket-market-trends-and-llm-edge/06-polymarket-mentions-category.md`. Source for the Kalshi formal definition: `raw/research/polymarket-market-trends-and-llm-edge/02-mention-markets-llm.md`.)

- **Contract:** binary Yes/No. Yes resolves if the specified keyword appears in the named source during the observation window.
- **Resolution corpus:** named per-market (transcript of a specific speech; podcast episode; Truth Social posts during a calendar window; etc.).
- **Resolution observable:** keyword presence — typically verbatim-match, sometimes with a count threshold (`"10+ times"`).
- **Observation window:** fixed at market creation. Common cadences observed on Polymarket: weekly recurring (Trump weekly speech), monthly (Trump-in-May), one-shot (Powell's specific FOMC press conference), event-bound (IEM Atlanta Grand Finals).
- **Resolution mechanism on Polymarket:** UMA Optimistic Oracle — see [[uma-optimistic-oracle]]. On Kalshi (Kim et al.'s setting): automated exact-string match against the official post-call transcript released by Kalshi.

### Resolution-rule grammar — canonical 3-component structure

(Source: `raw/research/polymarket-politics-and-niche-markets/07-polymarket-help-clarifications.md`, Polymarket Help Center — "How Are Markets Clarified?")

Polymarket's own statement: **"The market title describes the market, but the rules define how it should be resolved."** Every market's `Rules` block specifies exactly three components:

| # | Component | Specifies | Mention-market consequence |
|---|---|---|---|
| 1 | **Resolution source** | Authoritative data source (transcript provider, official video, named publication) | Names the canonical corpus that counts |
| 2 | **End date** | Closing / expiry datetime | Defines the observation window upper bound |
| 3 | **Edge cases** | Explicit handling of ambiguous / boundary situations | **Carries count thresholds, pluralization rules, possessive rules, compound-word exclusions, tied outcomes — none of which appear in the title** |

**Operational consequence for any modeling pipeline.** Reading market *titles* only is not sufficient. Count thresholds ("10+ times" vs "20+ times"), observation windows ("first JRE of the week"), pluralization semantics ("Yes" if `Sleepy Joe` OR `Sleepy Joes` is uttered? compound `Sleepy-Joe-style` excluded?), and exact-string vs lemma matching all live in component 3. The recurring per-market resolution-criteria gap flagged below is precisely this: the rules block is what's missing from current captures, not the title.

This is what motivates the kit-level proposal in `master_notes.md` 2026-05-12 to build `tools/capture_polymarket_market.py` against the Gamma API — the API exposes the rules block (which the SPA event-page captures cannot reliably retrieve).

## Polymarket Mentions category — snapshot 2026-05-12

(Source: `raw/research/polymarket-market-trends-and-llm-edge/06-polymarket-mentions-category.md`, captured `polymarket.com/culture/mention-markets`.)

The Mentions page sits under Polymarket's Pop Culture parent category. Snapshot subcategory counts (visible at capture):

| Subcategory | Markets |
|---|---|
| All (Culture parent) | 435 |
| Celebrities | 78 |
| Movies | 73 |
| Awards | 72 |
| Music | 70 |
| Tweet Markets | 34 |
| Courts | 30 |
| YouTube | 14 |
| Eurovision | 13 |
| Reality TV | 12 |
| Iceman | 10 |
| Taylor Swift | 10 |
| MrBeast | 9 |
| GTA VI | 6 |
| Aliens | 4 |

Named subcategories sum to ~355; the remaining ~80 markets likely live in the unlabeled "Mentions" parent slice or in multi-tag overlap.

**Subcategory-name vs actual-content reality check.** A 2026-05-14 sweep ([[snapshots/polymarket-mention-cottage-industry-2026-05-14]]) found that only **3 of the 6 named "mention-adjacent" subcategories** actually host mention content — Tweet Markets (28 markets, **the headline cottage industry**), Iceman (partial, with chart/sales markets alongside), and MrBeast (1 mention + 8 brackets/milestones). Taylor Swift (15 markets), Reality TV (12), and GTA VI (7) contain **zero mention markets** — they are outcome bets (pregnancy/album binaries, season winners, launch-date races, conditional bundles). The 435-market Pop Culture total over-states the mention-market footprint; treat per-subcategory verdicts separately.

### Active series matrix — the "cottage industry"

The mention-market vertical is best read as a matrix of **(speaker × corpus × cadence × count-threshold)** cells. Each cell is its own recurring market series; new instances list per period. Documented series from captures across 2026-05-12 and 2026-05-13:

| Speaker / Subject | Corpus | Cadence | Threshold type | Sources |
|---|---|---|---|---|
| Elon Musk | Twitter | Weekly (rolling windows) + monthly + 2-day | Count bracket-bins (20-wide) | [[snapshots/polymarket-top-markets-2026-05-13]] (3 overlapping windows live, $12M combined); [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (~$19M aggregate, modal 100–139/wk) |
| **Donald Trump (Truth Social)** | Truth Social posts | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal 180–199/wk; $297K vol) |
| **White House account** | Twitter | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal 180–199/wk; $147K vol) |
| **Ted Cruz** | Twitter | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal 120–139/wk; $44K vol; tight prior 97% near-resolution) |
| **CZ (Changpeng Zhao)** | Twitter | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal <20/wk historically; regime shift to 20–39 in May 15–22 — flag) |
| **Zelenskyy** | Twitter | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal 80–99/wk; $33K vol; tight prior 85%) |
| **Khamenei** | Twitter | Weekly | Count bracket-bins (narrow: <5, 5–9) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal <5/wk; $12K vol; very low-volume poster) |
| **NYC Mayor** | Twitter | Weekly | Count bracket-bins (20-wide) | [[snapshots/polymarket-mention-cottage-industry-2026-05-14]] (modal 20–39/wk; $10K vol; tight prior 95%) |
| Trump | Truth Social posts | Weekly | Binary keyword (per term) | This page below ("Trump Truth Social May 11–17") |
| Trump | Live speeches | Weekly + monthly + per-event | Binary keyword + grouped sub-themes (animals, Trump-named things) | This page below + [[snapshots/polymarket-politics-category-2026-05-13]] |
| Powell | FOMC press conferences | Per-event | Binary keyword | Help-center criteria: verbatim mention, plural/possessive count, compound exclude |
| Keir Starmer | UK PMQs | Per-event | **Count threshold** ("10+ times" / "20+ times") | This page below |
| Joe Rogan Experience | First episode of week | Weekly | Binary keyword | This page below |
| Lemonade Stand Podcast | Specific episode | Per-episode | Binary keyword | This page below |
| All-In Podcast | Specific episode | Weekly | Binary keyword | This page below |
| MrBeast | Next YouTube video | Monthly | Binary keyword + count threshold ("Hundred / Thousand / Million 10+ times") | This page below |
| ICEMAN show | Episode keywords | Per-event | Binary keyword | This page below |
| NYT | Front-page headlines | Weekly | Binary keyword | This page below |
| IEM Atlanta esports | Tournament broadcast | One-shot per tournament | Count threshold ("Molly / Molotov 10+ times") | This page below |

**The full long tail is not yet enumerated.** Pop Culture has 435 markets across 14 named subcategories. The matrix above documents only the top ~12 series visible at the 2026-05-12 capture. Below the visible-fold are the rest of the 78-Celebrities, 73-Movies, 72-Awards, 70-Music, 30-Courts, 13-Eurovision, 12-Reality TV, 10-Iceman, 10-Taylor Swift, 9-MrBeast, 6-GTA VI, 4-Aliens subcategories. Many of those subcategories carry their own per-subject mention series. Enumerating the long tail is a follow-up: requires either deeper scroll captures of each subcategory landing page (mostly succeeds — see [[snapshots/polymarket-niche-categories-2026-05-13]]) or the Gamma-API capture tool (kit gap, `master_notes.md` 2026-05-12).

### Gamma API capture workflow — per-market resolution rules

Implemented 2026-05-14 (`tools/capture_polymarket_market.py`). Single HTTP call to `gamma-api.polymarket.com/events?slug=<slug>` returns the full event tree including all sub-markets, with the **binding resolution-rule text** in the `description` field — exactly the component-3 edge-case content the title-vs-rules distinction above warns gets missed by title-only scraping.

```bash
# Capture a single event with all sub-markets
poetry run python -m tools.capture_polymarket_market --slug what-will-trump-say-during-bilateral-events-with-xi-jinping

# Output goes to raw/markets/<slug>/<YYYY-MM-DD>.md by convention
# Or override with --out
poetry run python -m tools.capture_polymarket_market --slug <slug> --out raw/research/<topic>
```

Smoke test on the Trump-Xi bilateral event ([[raw/markets/what-will-trump-say-during-bilateral-events-with-xi-jinping/2026-05-14]]) returned **33 sub-markets** with the canonical mention-market criteria text:

- **Plural & possessive count** (verbatim spec)
- **Compound-word rule** — explicit example: "joyful is **not** a compound word for 'joy', however 'killjoy' **is** a compounding of 'kill' and 'joy'"
- **Full-name accounting** — "If this market requires a specified number of mentions of a person's first or last name, a full-name mention will count as one mention (e.g., if a market is about 'Joe / Biden 5+ times,' a mention of 'Joe Biden' will count once)"
- **AI-generated audio/video does NOT count toward resolution** — non-obvious edge case
- **Only live-broadcast remarks count** — pre-recorded interviews excluded
- **Cancellation clause** — if the named event is cancelled / not aired by stated deadline, the market resolves No

The JSON response also includes per-market `umaBond` (live value: **$500 USDC.e**, conflicting with $750 in [[uma-optimistic-oracle]]), `umaReward` (live: **$5**), `orderPriceMinTickSize` (variable 0.001–0.01 depending on probability regime — conflicts with [[platform-comparison-kalshi-polymarket]] $0.0001 claim), `orderMinSize` (5 USDC), `conditionId`, `questionID`, and `clobTokenIds`. See `tools/capture_polymarket_market.py` for the full field set.

**Use this workflow** to capture per-market resolution rules for any market series you intend to model. The per-market `description` field is the binding spec for component-3 edge cases (count thresholds, exclusion rules, observation-window precision).

### Operator-discovery workflow for finding new series

Four pragmatic levers a retail operator can use:

1. **Re-capture `polymarket.com/culture/mention-markets`** weekly — new series tagged `NEW` on the card render (3 NEW series visible in the 2026-05-12 capture: Trump Truth Social, JRE first-of-week, Lemonade Stand, All-In, MrBeast Eliminate, Trump-named things, IEM Atlanta).
2. **Per-subject subcategory landings** (`/pop-culture/celebrities`, `/pop-culture/mrbeast`, `/pop-culture/taylor-swift`, etc.) — each surfaces the per-subject series independently of the top-level Mentions page. **Caveat per [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]**: only ~half of these subcategory landings actually contain mention markets; many are outcome-only (Taylor Swift, Reality TV, GTA VI).
3. **`polymarket.com/culture/tweets-markets`** — the largest single mention-market reservoir (28 markets, 9 speakers; see [[snapshots/polymarket-mention-cottage-industry-2026-05-14]]). Re-capture for new speakers as they're added.
4. **Gamma API per-event capture** via `tools/capture_polymarket_market.py` (above) — for once you have a candidate event slug, returns the full sub-market set + binding resolution rules. Combine with #1–3 to first *discover* candidate events, then *capture* the rule text.

### Active markets visible at capture (selected; binary Yes/No, odds = implied probability at 2026-05-12)

| Event / window | Outcome | Yes | Vol |
|---|---|---|---|
| NYT front-page headlines (May 4–10) | "Street" | <1% | $81K |
| Trump weekly speech (May 17) | "Sleepy Joe" | 100% | $60K |
| Trump weekly speech (May 17) | "Cuba" | 91% | — |
| Trump–Xi bilateral | "Iran" | 74% | $87K |
| Trump–Xi bilateral | "Tariff" | 71% | — |
| Keir Starmer next PMQs | "Mr. Speaker 10+ times" | 89% | $30K |
| Keir Starmer next PMQs | "Mr. Speaker 20+ times" | 64% | — |
| Trump Truth Social (May 11–17) | "ICE" | 50% | — |
| Trump Truth Social (May 11–17) | "Football" | 37% | — |
| JRE first episode of week (May 11) | "Left" | 96% | — |
| JRE first episode of week (May 11) | "Table" | 77% | — |
| Trump May (full month) | "Pulitzer" | 100% | $30K |
| Trump May (full month) | "Nuke" | 70% | — |
| Lemonade Stand podcast (May 13) | "Crazy" | 95% | — |
| Lemonade Stand podcast (May 13) | "China" | 82% | — |
| All-In Podcast (May 15) | "Anthropic" | 93% | — |
| All-In Podcast (May 15) | "Software" | 90% | — |
| MrBeast next YouTube video | "Eliminate / Eliminated" | 78% | — |
| MrBeast next YouTube video | "Hundred / Thousand / Million 10+ times" | 74% | — |
| ICEMAN | "Daddy" | 87% | $60K |
| ICEMAN | "Covid" | 75% | — |
| Trump-named things in May | "Trump Family" | 52% | — |
| Trump-named things in May | "Trump Tower" | 52% | — |
| Animals Trump says in May | "Turkey / Turkiye" | 70% | $14K |
| Animals Trump says in May | "Cat" | 41% | — |
| IEM Atlanta 2026 Grand Finals | "Molly / Molotov 10+ times" | 70% | — |
| IEM Atlanta 2026 Grand Finals | "Five Seven" | 70% | — |

**Reading the snapshot.** The high-Yes markets (≥90%) are either near-certain words for the speaker/format or markets that have effectively resolved; treat as liquidity-provision opportunities, not directional edges. The interesting edge cells are the **mid-confidence (40–80% Yes)** markets where MCP's empirical edge zone lives.

## Market-Conditioned Prompting (MCP)

(Source: `raw/research/polymarket-market-trends-and-llm-edge/02-mention-markets-llm.md`, Sec. 3–4. **Important**: this paper is on **Kalshi earnings-call** mention markets — not Polymarket. Methodology is portable; empirical validation on Polymarket is still pending.)

### Definition

```
p_mcp = LLM_θ(T, N | p_mkt)
```

The LLM is given the market probability `p_mkt` (on the 0–100 scale) **as an explicit Bayesian prior** and instructed via system prompt to update it using the textual evidence — rather than form an independent forecast. The model returns a single integer/float ∈ [0, 100] which is rescaled to [0, 1].

**Inputs at inference time:**
- `T` — prior-quarter earnings-call transcript (the most-load-bearing input per the ablation; see below).
- `N` — up to 100 recent news items (title, snippet, source, date) retrieved via SERP API at the cutoff (7 days pre-call).
- `p_mkt` — market probability at the cutoff (numeric, on 0–100 scale).

**Model used:** GPT-5.1, structured output, no fine-tuning, fixed decoding across all conditions. **No ablations across other LLMs** — generalization to weaker/cheaper models is not established.

### MixMCP (convex mixture)

```
p_mix = α · p_mkt + (1 − α) · p_mcp,   α = 0.7
```

`α = 0.7` chosen on a held-out split within the same 856-instance dataset; plateau observed at `α ∈ [0.6, 0.8]`. **In-sample.** Operational reading: dampen the LLM's posterior toward the market prior, so the LLM's role is *refinement* rather than *replacement*. The 70/30 weight matches the same ratio chosen heuristically by `[[polyswarm-llm-trading-framework]]` (Eq. 2) — convergent practitioner intuition that the market prior should dominate.

### Headline results — Kalshi earnings-call mention markets

Dataset: N = 856 contracts; 50 companies × 70 earnings events; Apr–Dec 2025; cutoff 7 days pre-call.

| Method | Brier ↓ | ECE ↓ | Acc ↑ | F1 ↑ |
|---|---|---|---|---|
| Market probability (baseline) | 0.1402 | 0.0651 | 79.8 | 0.840 |
| W/O PROMPTING{T,N,M} (market as plain text, no prior framing) | 0.1674 | 0.0705 | 74.4 | 0.782 |
| MCP (Bayesian prior framing) | 0.1470 | **0.0514** | 78.2 | 0.822 |
| **MixMCP** (0.7·market + 0.3·MCP) | **0.1392** | 0.0666 | **80.3** | **0.842** |

**Headline reading.**
- MixMCP beats the market baseline by Brier (0.1402 → 0.1392, absolute Δ = 0.0010). Tight margin, but reproduced across the full 856 contracts.
- MCP alone wins ECE (0.0514) — best **calibration** — but loses Brier to the market.
- W/O PROMPTING underperforms — **the framing matters**, not mere market-number exposure. The system prompt instruction to treat `p_mkt` as a Bayesian prior is the load-bearing design choice.

**Internal Brier inconsistency:** Section 4.2 prose reports market Brier of 0.1441; Tables 1 and 5 report 0.1402. Treat 0.1402 as canonical (table value); the prose appears to be a typo.

### Where the edge concentrates — regime analysis

In the **disagreement subset** (70 instances, 8.2% of contracts, where MCP's binary prediction differs from market's binary prediction):

- Market probability **50–60%**: MCP wins 17/30 (56.7%)
- Market probability **60–70%**: MCP wins 5/8 (62.5%)
- Market probability **<50%**: MCP wins 5/18 (27.8%) — market dominates
- Market probability **>70%**: MCP wins 1/14 (7.1%) — market dominates

**The edge lives in the mid-confidence band** (50–70% market probability). Operational reading: trigger MCP-based position entries only when `p_mkt ∈ [0.5, 0.7]` *and* the MCP posterior disagrees. Outside this band, defer to the market.

This maps directly to a subset of the Polymarket mentions snapshot above: Trump–Xi "Iran" 74%, Starmer "20+ times" 64%, JRE "Table" 77%, MrBeast "Eliminate" 78%, Trump May "Nuke" 70%, ICEMAN "Covid" 75% — all candidates for MCP application *if* the modeling is rebuilt for the Polymarket regime.

### Context ablation — what to feed the model

(`raw/research/polymarket-market-trends-and-llm-edge/02-mention-markets-llm.md` Table 5, no-market conditions.)

| Context | Brier | ECE | Acc |
|---|---|---|---|
| ∅ (question only) | 0.2635 | 0.1993 | 63.1 |
| N (news only) | 0.2372 | 0.1387 | 66.2 |
| T (prior-quarter transcript only) | 0.2038 | 0.1105 | 70.0 |
| T + N | 0.1991 | 0.0928 | 70.1 |

**Transcript > news.** Feeding the prior-quarter earnings-call transcript gives larger gains than feeding news alone. Combining (T + N) gives marginal improvement over T alone. **Operational reading**: prioritize speaker-history corpora (prior episodes of the same podcast, prior speeches by the same politician, prior front pages of the same publication) over generic news retrieval.

Polymarket-applicable corollary: for each mentioned-subject + named-corpus pair (e.g., Trump + Truth Social, MrBeast + YouTube), assemble the speaker's recent history in that medium as `T`; supplement with news only as `N`.

## Cross-link to the LLM-by-domain landscape

[[llm-forecasting-by-domain]] tiers Geopolitics and Politics as the strongest LLM-baseline domains and Finance/Sports as weakest. Mention markets cut **across** that taxonomy — the Polymarket snapshot includes politics (Trump speech), media/entertainment (MrBeast, JRE), and even esports (IEM Atlanta) corpora. The *modality* (text resolution observable) matters more than the topical taxonomy: any speaker + medium with a stable speaker-history corpus is a candidate for MCP-style modeling, regardless of which LLM-by-domain tier the speaker's subject sits in.

## Open research questions

1. **Per-market resolution criteria text on Polymarket.** Currently absent from the wiki. Required for the lint check; required for honest backtesting. Fix: `tools/capture_polymarket_market.py` against the Gamma API.
2. **MCP transfer to Polymarket.** Kim et al. validate MCP on Kalshi only. The Kalshi corpus has a single fixed-format resolution source (Kalshi-published transcript). Polymarket mention markets vary widely in resolution source (Truth Social posts, podcast videos, esports broadcasts, NYT front pages). MCP transfer needs per-corpus retrieval pipelines and per-corpus resolution-checking — non-trivial engineering.
3. **MCP transfer to non-GPT-5.1 models.** The paper has no model ablations; generalization to cheaper/local models is unknown.
4. **Threshold / count markets** ("Mr. Speaker 10+ times", "Hundred/Thousand/Million 10+ times"). These have a continuous latent (the count) projected to a binary observation. A regression-then-threshold approach (predict the count, then map to the indicator) likely beats direct binary prompting — not tested in Kim et al.
5. **Recurring-cadence base-rate edge.** Many Polymarket mention markets are weekly recurring with stable speakers. A backtest of historical resolution rates for "Sleepy Joe in a Trump weekly speech" gives a base rate that the market may consistently mis-price; this is a no-LLM-needed edge worth measuring.

## Source

- `raw/research/polymarket-market-trends-and-llm-edge/02-mention-markets-llm.md` — Kim, Kwon et al. (2026), "Forecasting Future Language: Context Design for Mention Markets" (arXiv 2602.21229). Kalshi earnings-call mention markets; MCP and MixMCP defined; full Table 5 / Table 1; α=0.7 plateau in-sample; GPT-5.1 only.
- `raw/research/polymarket-market-trends-and-llm-edge/06-polymarket-mentions-category.md` — Polymarket Mentions category landing page (`polymarket.com/culture/mention-markets`), captured 2026-05-12. Subcategory taxonomy + active-market snapshot. Per-market resolution-criteria text NOT captured — see capture gap above.
- `raw/research/polymarket-politics-and-niche-markets/07-polymarket-help-clarifications.md` — Polymarket Help Center "How Are Markets Clarified?", captured 2026-05-13. Canonical 3-component rule grammar; title-vs-rules distinction.

## Related

- [[polymarket-market-taxonomy]]
- [[polymarket-market-structures]]
- [[uma-optimistic-oracle]]
- [[llm-forecasting-by-domain]]
- [[llm-epistemic-calibration]]
- [[polyswarm-llm-trading-framework]]
- [[market-maker-handbook-prediction-markets]]
- [[snapshots/polymarket-niche-categories-2026-05-13]]
