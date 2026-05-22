# Polymarket Market Structures

Catalogue of the structural shapes Polymarket markets take. Every market is fundamentally a binary Yes/No on a single condition (the atomic unit per [[polymarket-market-taxonomy]]), but markets are *composed* into events and series in patterns that determine where edge lives. This page enumerates the observed structures, each anchored to a specific captured example, with notes on arb topology and modeling implication per structure.

Sources: cross-category 2026-05-13 snapshots — [[snapshots/polymarket-politics-category-2026-05-13]], [[snapshots/polymarket-geopolitics-category-2026-05-13]], [[snapshots/polymarket-midterms-category-2026-05-13]], [[snapshots/polymarket-niche-categories-2026-05-13]] — plus [[snapshots/polymarket-top-markets-2026-05-13]], [[snapshots/polymarket-crypto-category-2026-05-13]], and Polymarket Help Center docs (`raw/research/polymarket-politics-and-niche-markets/04-polymarket-help-resolution.md`, `07-polymarket-help-clarifications.md`).

## 1. Simple binary

Single condition, Yes/No, single event card. The atomic unit.

- **Examples:** "Will Trump and Xi kiss at their summit?" ($896K vol, ~99% No — `raw/.../01-polymarket-politics-master.md`). "Aliens.gov confirmed immigration website?" ($182K vol, 49% Yes — `raw/.../05-polymarket-aliens-category.md`).
- **Edge surface:** pure model-vs-market on the one condition. No structural arb.
- **Typical liquidity:** thin (often < $1M vol) unless the event is itself headline-driven.

## 2. Date-ladder (multi-expiry on the same event)

Same underlying question replicated against multiple expiry dates (typically `May 31 / Jun 30 / Dec 31` in the captured corpus). Each expiry is its own binary Yes/No card, but they share the underlying event.

- **Dominant in the Iran vertical** (`raw/.../03-polymarket-iran-category.md`): every high-volume Iran topic has 2–3 dated legs. Examples at 2026-05-13:
  - US-Iran peace deal: Jun 30 = 34%, Dec 31 = 63%
  - Strait of Hormuz normal: May 15 < 1%, end-May = 8%, end-June = 32%
  - Iranian regime fall: May 31 = 1%, Jun 30 = 5%
  - Trump blockade lifted: May 31 = 23%, Jun 30 = 51%
  - Iran closes airspace: May 31 = 39%, Jun 30 = 47%
- **Also seen in:** Politics ("Starmer out by ?" Jun 30 47% / Dec 31 79%; "Epstein suicide note released by ?" May 8 < 1% / May 31 11% — `raw/.../01-polymarket-politics-master.md`); Aliens ("Will the US confirm aliens exist by ?" Sep 30 11% / Dec 31 15% — `raw/.../05-polymarket-aliens-category.md`).
- **Math.** Monotonicity is the no-arb constraint:
  ```
  P(event by T_1) ≤ P(event by T_2)  for  T_1 < T_2
  ```
  Violations are immediate Market Rebalancing Arbitrage candidates per [[arbitrage-taxonomy]] Def. 3. Implied conditional probability of the event landing in the inter-expiry window:
  ```
  P(event in (T_1, T_2] | not by T_1)  =  ( P(by T_2) − P(by T_1) ) / ( 1 − P(by T_1) )
  ```
  Worked example: peace deal Jun 30 = 34%, Dec 31 = 63% → conditional P(H2 deal | no H1 deal) = (0.63 − 0.34) / (1 − 0.34) ≈ **44%**. This is the term-structure slice the market is pricing.
- **Edge surface:** monotonicity checks across the ladder; term-structure pricing of events. **Iran airspace (May 31 39% / Jun 30 47%)** is the tightest spread at capture — small absolute slack, watch for inversion.

## 3. Candidate race (multi-outcome grouped event)

One event with multiple named candidate outcomes, each its own Yes/No sub-market. Sub-prices encode the candidate's probability of winning; cross-candidate constraint is `Σ P(candidate_i) ≈ 1` (subject to spread).

- **Largest examples in the corpus** (`raw/.../01-polymarket-politics-master.md`):
  - **Democratic Presidential Nominee 2028 — $1B** all-time vol; Gavin Newsom 24%, Kamala Harris 9%
  - **Republican Presidential Nominee 2028 — $616M**; JD Vance 37%, Marco Rubio 25%
  - Presidential Election Winner 2028 — $579M; JD Vance 19%, Newsom 17%
  - Brazil Presidential Election — $71M; Lula 42%, Flávio Bolsonaro 35%
  - Next French Presidential Election — $69M; Bardella 24%, Philippe 20%
  - 2026 Seoul Mayoral Election Winner — $38M; Chong Won-oh 85%
  - Iran leader end of 2026 — $8M; Mojtaba Khamenei 64%, Reza Pahlavi 8% (sum 72%, residual 28% in other candidates) — `raw/.../03-polymarket-iran-category.md`
- **Edge surface:** Σ-check against 1.00 is the structural arb (Saguillo et al. MRA per [[arbitrage-taxonomy]]); per-candidate model edge is the standard prediction-market play. Each candidate's order book is independent — `Σ` may exceed or fall short of 1.00 by a small margin without being an arb (rounding + spread), but large deviations are MRA candidates.

## 4. Bracket / range bins (multi-outcome numeric)

A numeric outcome (count, price, seat total, temperature) is partitioned into bins, each bin a Yes/No sub-market. The market collectively prices a probability mass function over the binned variable.

- **Examples:**
  - **Elon Musk tweet-count weekly markets** (`raw/.../01-polymarket-politics-master.md`): three overlapping windows live at capture — May 8–15 ($7M, 100–119 = 48%), May 12–19 ($4M, 120–139 = 20%, 140–159 = 20% tied), May 15–22 ($503K NEW, 120–139 = 18%). See [[mention-markets]] for the recurring-cadence pattern.
  - **Republican Senate seat-count** (`raw/.../04-polymarket-midterms-category.md`): ≤47 = 26%, exactly 50 = 19%, complementary bins inferrable.
  - **Republican House seat-count**: Below 190 = 26%, 190–194 = 13%.
  - **Crypto Price-Range markets** (BTC 80k–82k 86%, 78k–80k 10% on May 13 — [[snapshots/polymarket-crypto-category-2026-05-13]]).
  - **Earthquake count markets** (`raw/.../06-polymarket-science-predictions.md`): "How many 5.5+ earthquakes May 11–17?" — count brackets; "How many 7.0+ by Jun 30?" 8+ = 81%.
  - **May 2026 Temperature Increase** — 1.15–1.19°C = 45% (range bins on a continuous variable).
- **Edge surface:** the bracket prices imply a PMF; a structured forecast model (Poisson for counts, predictive distribution for temperatures, district-by-district Bayesian model for seat totals) produces an alternative PMF; mispriced bins are the trades. Cross-bracket Σ-check is the MRA constraint.

## 5. Scenario grid (multi-axis composite)

One event with N outcomes, each outcome a *combination* of multiple underlying conditions. Resolution requires the entire scenario to be true.

- **Canonical example** (`raw/.../04-polymarket-midterms-category.md`): **"Balance of Power: 2026 Midterms"** — $7M vol. Four outcomes:
  - D-Sweep (D Senate ∧ D House) = 43%
  - R-Senate ∧ D-House = 33%
  - (R-Sweep and D-Senate ∧ R-House outcomes implied, sum to ~24%)
- **Combinatorial arb candidate vs component markets.** The same midterms page lists separate chamber-control binaries: P(D-House) = 79%, P(R-Senate) = 53%. Under correlation assumptions, scenario probabilities must be consistent with the marginals: e.g., `P(D-House) = P(D-Sweep) + P(D-Senate-and-R-House)`. With visible numbers, P(D-Sweep) = 43% and P(D-House) = 79% imply P(D-Senate ∧ R-House) ≈ 36% — which is inconsistent with the visible P(D-Senate) = 47% under joint independence; the inconsistency is the arb surface. Cross-link to [[combinatorial-arbitrage-empirics]] for the dependency-detection methodology (Saguillo et al. used an LLM-semantic pipeline; here the dependency is structurally given).
- **Edge surface:** cross-market consistency Σ-check is the highest-confidence arb in the corpus when the scenario marginals and the chamber binaries are both live with depth.

## 6. Conditional cross-market bundle

One event-card bundles N otherwise-independent legs into a single grouped event with shared metadata (icon, vol display). Each leg is a separate Yes/No on its own substantive condition; the bundling carries no logical dependency between the legs.

- **Canonical example** (`raw/.../05-polymarket-aliens-category.md`): **"What will happen before Kevin Warsh is confirmed?"** — $734K vol — bundles:
  - Fed rate cut leg ( < 1% Yes)
  - US confirms aliens exist leg ( < 1% Yes)
  - Both legs priced near-zero; bundling is for *display narrative* (a "before X" wrapper around two thematically-distinct longshots), not for joint resolution. Resolution is per-leg.
- **Edge surface:** legs are independent — edge in either leg is self-contained. Bundling may *under-publicize* a leg (a trader scanning for "aliens" markets might miss the leg if they scan only by primary category tag). No structural arb between the legs themselves.
- **Why it matters:** the shape is novel in the wiki and shows up in places a flat-category scraper would miss. A pipeline searching for "aliens" markets that filters on the top-level event title would skip this bundle entirely.

## 7. Mention markets (count + observation-window special case)

A specialization of binary or bracket-bins where the resolution observable is the *occurrence* (or count) of a specified keyword in a named corpus during an observation window. The structure deserves its own naming because the resolution-criteria text carries unusual edge-case complexity.

- See [[mention-markets]] for the full treatment (Polymarket Pop Culture 435 markets across 14 subcategories; Kalshi-validated Market-Conditioned Prompting modeling technique).
- Three resolution-rule levers that vary per market (and live in component 3 — *edge cases* — of the canonical rule grammar; see §"Resolution rule grammar" below):
  1. **Count threshold** — `Yes if "Sleepy Joe" said ≥1 time` vs `≥10 times` (`raw/.../06-polymarket-mentions-category.md` from prior run shows both shapes — Starmer PMQs "10+ times" 89% / "20+ times" 64%).
  2. **Observation window** — a specific speech (`>10 min on camera`), a calendar window (`May 8–15`), a single event (`first JRE of the week`).
  3. **Exact-string semantics** — pluralization rules, possessive rules, compound-word exclusion (per Polymarket's `What will Trump say in next live speech?` resolution criteria observed in prior search).

## Resolution rule grammar (the canonical 3 components)

Source: `raw/research/polymarket-politics-and-niche-markets/07-polymarket-help-clarifications.md` — Polymarket Help Center "How Are Markets Clarified?".

**Polymarket's own statement:** *"The market title describes the market, but the rules define how it should be resolved."*

Every Polymarket market's `Rules` block specifies exactly three components:

| # | Component | What it specifies | Mention-market consequence |
|---|---|---|---|
| 1 | **Resolution source** | The authoritative data source used to determine the outcome (official announcement, named website, transcript provider). | Names the canonical transcript / video / publication that counts. |
| 2 | **End date** | The market's closing/expiry datetime. | Defines the observation window upper bound. |
| 3 | **Edge cases** | Explicit handling of ambiguous or boundary situations. | **Carries count thresholds, pluralization rules, compound-word exclusions, tie-breaking — none of which appear in the title.** |

**Operational consequence.** Any scraping pipeline that consumes only market *titles* misses the binding spec entirely. Count thresholds, observation windows, and exclusion criteria all live in component 3. The wiki's recurring per-market resolution-criteria gap (flagged in [[mention-markets]] and [[snapshots/polymarket-crypto-category-2026-05-13]]) is precisely this: the rules block is what's missing, not the title.

This is what motivates the kit-level proposal in `master_notes.md` 2026-05-12 to build `tools/capture_polymarket_market.py` against the Gamma API — the API exposes the rules block (which the SPA event-page captures cannot reliably retrieve).

## Strategy implications by structure

Per-structure summary of where edge most plausibly lives:

| Structure | Primary edge source | Primary arb topology |
|---|---|---|
| 1. Simple binary | Model vs market on the single condition | None structural |
| 2. Date-ladder | Term-structure conditional pricing | Monotonicity check across legs (MRA) |
| 3. Candidate race | Per-candidate model edge | `Σ P(candidate) ≈ 1` MRA check |
| 4. Bracket bins | Structured-PMF model (Poisson, Bayesian) vs bin prices | Cross-bracket `Σ ≈ 1` MRA |
| 5. Scenario grid | Joint-probability model vs scenario prices | Combinatorial arb vs component marginals |
| 6. Conditional bundle | Per-leg model edge (legs are independent) | None structural; legs evaluated separately |
| 7. Mention | Speaker-history corpus + count model + edge-case rule parsing | Same as 1 or 4 depending on count vs binary |

Crypto Up/Down 5m, Hit Price, Above/Below markets are mostly Structure 1 (binary) or Structure 4 (bracket — Price Range). Sports markets (out of scope for this wiki per user direction) are Structures 1, 3, and 4. Mention markets (Structure 7) overlap with Structures 1 and 4.

## What this page does not yet cover

- **Conditional markets with logical dependence** (vs Structure 6's bundling without dependence). E.g., "If Trump nominates X, will X be confirmed?" — captured corpus does not yet contain a clean example. Worth surfacing when an example appears.
- **Scalar / range markets resolving on continuous values**, distinct from bracket-bin discretization. Polymarket primarily binarizes via brackets; true scalar contracts (paying out proportional to outcome) appear absent from the captured corpus.
- **Per-market resolution-rule text for the corpus** — blocked by the kit gap above; will be unblocked once the Gamma-API capture tool exists.

## Source

- `raw/research/polymarket-politics-and-niche-markets/01-polymarket-politics-master.md` — Politics category landing; market-type variants enumeration.
- `raw/research/polymarket-politics-and-niche-markets/03-polymarket-iran-category.md` — Iran vertical; date-ladder structure exemplar.
- `raw/research/polymarket-politics-and-niche-markets/04-polymarket-midterms-category.md` — Midterms; balance-of-power composite + chamber binaries combinatorial example.
- `raw/research/polymarket-politics-and-niche-markets/05-polymarket-aliens-category.md` — Aliens; conditional bundle exemplar (Kevin Warsh).
- `raw/research/polymarket-politics-and-niche-markets/06-polymarket-science-predictions.md` — Science; bracket-bins on natural-disaster counts.
- `raw/research/polymarket-politics-and-niche-markets/07-polymarket-help-clarifications.md` — Polymarket canonical 3-component rule grammar.

## Related

- [[polymarket-market-taxonomy]]
- [[mention-markets]]
- [[arbitrage-taxonomy]]
- [[combinatorial-arbitrage-empirics]]
- [[uma-optimistic-oracle]]
- [[polymarket-bet-content-trends]]
- [[snapshots/polymarket-politics-category-2026-05-13]]
- [[snapshots/polymarket-geopolitics-category-2026-05-13]]
- [[snapshots/polymarket-midterms-category-2026-05-13]]
- [[snapshots/polymarket-niche-categories-2026-05-13]]
- [[snapshots/polymarket-top-markets-2026-05-13]]
- [[snapshots/polymarket-crypto-category-2026-05-13]]
