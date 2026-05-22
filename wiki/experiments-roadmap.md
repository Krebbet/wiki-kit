# Experiments Roadmap — Phase-1 Validation per Model Archetype

Per-archetype experimental design for the 4 actionable model archetypes from [[feasibility-review]] §"Recurring model archetypes" (A1, A3, A4, A5). Each experiment defines: the bet, hypothetical edge, conditions for success, sample market, minimal validation run, and quantitative success criteria. Failure modes redirect rather than block.

Sequencing: A5(b) first (zero-modeling, lowest cost, highest base rate, broadest coverage), then A1, then A3 + A4 in parallel, then A5(a). End-of-week-4 yields first verdict per archetype.

---

## A1 — Count-distribution PMF (Poisson / NegBin / lognormal)

### Thesis

Buy underpriced + sell overpriced bins in newly-opened weekly tweet-count brackets where fitted Poisson/NegBin PMF diverges from market PMF by >5pp after 5% taker fee. Pure statistical fit on a stable speaker cadence with regime-shift detection per [[feasibility/mention-markets]] §3.

### Hypothetical edge

- Per-bin mispricing: 5-10pp on 2-3 of 8-bracket events on newly-opened windows before mid-week observations narrow distribution.
- Brier delta target: absolute Brier improvement ~0.005-0.010 vs market PMF (Kim et al. MixMCP magnitude reference per [[mention-markets]]).
- Window-level EV after fees: ~+2-5% on $500-$2K positions.

### Conditions for success

1. Speaker cadence stationary in trailing 8-12 wks OR regime shifts detectable from recent 4-wk window.
2. X API v2 free tier (500K reads/mo) delivers reliable counts for 8 non-Elon speakers + Truth Social RSS for Trump.
3. Newly-opened windows carry stale PMF first 12-48h before mid-week observation narrowing per [[feasibility/mention-markets]] §5.
4. $500-$2K limit orders fill at mid prices, not bid/ask cross.
5. Mid-week posterior `P(bracket | k obs in t/7) ∝ Poisson(k; λ·t/7)·prior` collapses sharply enough to overcome fee+spread.

### Experiment

**Sample market:** `cz-binance-of-tweets-may-19-may-26-2026` ([[feasibility/mention-markets]] §7 — newly opened, $1.2K vol, active regime shift <20→20-39/wk).

**Run:**
1. Days 1-2: build X API v2 ingestion for 8 speakers (CZ, Trump-TS, White House, Cruz, Zelenskyy, NYC Mayor, Khamenei, Elon control). Fit Poisson + NegBin via MLE; AIC selection.
2. Day 3: compute bracket PMF for open windows; compare to Gamma API market PMF; flag bins with `|model_p − market_p| > 5pp`.
3. Days 3-28: paper-trade $500 limit-order entries inside spread for flagged bins. ~256 paper bets target across 4 wks × 8 speakers × ~8 brackets.
4. Day 28: aggregate Brier(model) vs Brier(market) on resolved windows.

**Time / cost:** ~3 days engineering + 4 wks passive. Free.

### Success criteria (all three must pass)

| Metric | Bar |
|---|---|
| Brier delta | Brier(model) − Brier(market) ≤ **−0.005** across paper-trade set |
| Mid-confidence accuracy | Win rate on `0.3 ≤ market_p ≤ 0.7` bins > **55%** |
| Net paper-trade EV | Aggregate after 5% taker + 50bps slippage > **+2%** of notional |

**Outcomes:**
- **Pass all:** scale to $2K/leg real capital × 4 speakers × next 4 weekly windows.
- **Fail Brier only:** restrict to stationary speakers (Zelenskyy, NYC Mayor, Khamenei).
- **Fail net EV only:** restrict to >8pp edge bins or maker-side entries only.

---

## A3 — LLM keyword-binary (MixMCP)

### Thesis

Apply Kim et al. MixMCP (`p_mix = 0.7·p_mkt + 0.3·p_mcp`) to non-political keyword-binary mention markets where resolution corpus is YouTube auto-caption text. Buy/sell mid-confidence bins where `|p_mix − p_mkt| > 5pp`. Edge concentrates in `p_mkt ∈ [0.5, 0.7]` per [[feasibility/mention-markets]] §3.

### Hypothetical edge

- Brier delta: Kim et al. 0.1402 → 0.1392 on Kalshi N=856 earnings-call → ~0.001/bin, compounding across 32 sub-markets per ICEMAN episode and recurring cadence.
- Mid-confidence directional accuracy: MCP wins 56.7%/62.5% at 50-60%/60-70% bands per Kim.
- Per-episode EV: ~+1-3% on mid-confidence portfolio assuming Kim magnitudes transfer.

### Conditions for success

1. GPT-4-class LLM produces calibrated `p_mcp` given T (10-15 prior transcripts) + N (news within 7d).
2. ICEMAN auto-captions (free) accurate enough for stable phrase-frequency baseline. WER 5-10% per [[feasibility/youtube]] §"Risks" — material for brand names/proper nouns.
3. Polymarket keyword markets resolve by string-match against transcript (resolution corpus = auto-caption corpus). Verify on `what-will-be-said-on-iceman` resolution rule.
4. Mid-confidence bin set `0.5 ≤ p_mkt ≤ 0.7` has ≥4 sub-markets/episode on avg.
5. Episode cadence allows ≥3-5 episodes within 4-wk window.
6. **Platform transfer holds** — Kim validated only on Kalshi fixed-format earnings calls. Polymarket podcast = the test.

### Experiment

**Sample market:** `what-will-be-said-on-iceman` ([[feasibility/mention-markets]] §7 — 32 sub-markets/episode, $22K 24h, $104K all-time).

**Run:**
1. Days 1-3: build pipeline — scrape prior 10-15 ICEMAN transcripts via `youtube-transcript-api`; tokenize; compute keyword base-rates; design LLM prompt per Kim MCP spec.
2. Next 3-5 ICEMAN episodes:
   - T-24h: pull 28-32 sub-markets via Gamma API; record p_mkt.
   - Generate p_mcp per bin via LLM.
   - Compute `p_mix = 0.7·p_mkt + 0.3·p_mcp`.
   - Log paper-trade entries on bins with `|p_mix − p_mkt| > 5pp`.
3. Post-episode: pull resolution via Gamma API. Spot-check 3-5 keyword resolutions against auto-caption corpus.
4. Day 21: aggregate Brier(p_mix) vs Brier(p_mkt); directional win rate; net EV.

**Time / cost:** ~3 days engineering + 3-4 wks. LLM API ~$5-20 (5 episodes × 32 bins × 1 call) + free transcripts.

### Success criteria (all three must pass)

| Metric | Bar |
|---|---|
| Aggregate Brier gain | Brier(p_mix) − Brier(p_mkt) ≤ **−0.005** across ≥96 predictions |
| Mid-confidence win rate | On `0.5 ≤ p_mkt ≤ 0.7` bins, directional choice wins **>55%** |
| Resolution-corpus identity | Spot-check ≥**90%** match between auto-caption tokenization and actual resolution |

**Mandatory cross-validation:** 2 episodes on a second non-political speaker (All-In, Lemonade Stand) — if Brier gain disappears on transfer, ICEMAN result is corpus-specific.

**Outcomes:**
- **Pass + cross-val:** scale to $200-$500/leg on next 5 ICEMAN episodes; extend to JRE/All-In.
- **Directional pass, Brier fail:** size at half-Kelly; archetype works for selection not magnitude.
- **Platform-transfer fail:** defer to political markets with exact-corpus identity (Starmer Hansard).

---

## A4 — Bayesian intra-period update on real-time observable

### Thesis

Box-office bracket markets and RT ladders receive hard mid-period observables (Thursday preview gross T-36h; RT reviews post-embargo). Bayesian posterior arrives sharper than market mid in some window before market closes gap. Buy/sell brackets where `|posterior − market_mid| > 3pp` per [[feasibility/movies]] §"Modeling spine".

### Hypothetical edge

- Box-office: Thursday preview r≈0.85-0.90 with final 3-day gross via genre multiplier. Market mid partially reprices but bracket-bin distribution lags.
- Per-bin EV after fees: ~+2-5% on >3pp divergence bins with T-2h-to-Sunday execution window.
- RT: Beta-update on individual review accumulation gives sharper P(score ≥ X) than market mid first 24-48h post-embargo.

### Conditions for success

1. Thursday preview gross posted reliably by The Numbers / BOM by 11pm Thursday ET.
2. Polymarket bracket mid does NOT fully reprice to optimal posterior in first 2-12h post-observable.
3. Window between observable and bracket close ≥ 2-12h.
4. Genre multipliers (horror 3-4×, superhero 4-6×, family 3-5×, drama 2-4× per [[feasibility/movies]]) generalize within 1σ on test films.
5. Comp-set sample (last 2-3 yrs × genre, ~30-50 films) large enough for stable lognormal CDF.

### Experiment

**Sample markets:** Box-office bracket events on next 5 wide-release films via Gamma API `tag_slug=box-office`. Backtest corpus from Gamma API `closed=true` last 6 months.

**Phase 1 — Backtest (~1 wk, no capital):**
1. Pull all closed box-office bracket markets from Gamma API.
2. Reconstruct Thursday preview gross (The Numbers historical) + genre tag per event.
3. Compute Bayesian posterior `P(bracket | preview, genre_multiplier)` from comp-set lognormal CDF.
4. Pull historical market mid at T-24h, T-12h, T-6h, T-2h, T+0.
5. Measure repricing-lag distribution.

**Phase 2 — Forward paper-trade (~5-10 wks across 5 films):**
1. T-2h after Thursday 11pm ET preview gross: pull bracket via Gamma API.
2. Compute Bayesian posterior.
3. Flag bins with `|posterior_p − market_p| > 3pp`.
4. Log limit-order entries at market mid.
5. Hold to Sunday resolution; record fill + P&L.

**Time / cost:** ~1 wk engineering + ~5-10 wks observation. Free.

### Success criteria

**Phase 1 gate:**

| Metric | Bar |
|---|---|
| Repricing lag exists | Median observed lag (Thursday preview → market mid within 3pp of posterior) > **2 hours** |

**Phase 2 (both must pass):**

| Metric | Bar |
|---|---|
| Aggregate paper-trade EV | > **+3%** of notional after 5% taker + 25bps slippage across 5 films |
| Directional accuracy | Posterior beats market mid as predictor of resolved bracket on **>60%** of bins (~25 bins) |

**Outcomes:**
- **Pass both phases:** scale to $1-3K/bin × next 3 films; extend to RT Beta-update on prestige films post-embargo.
- **Fail Phase 1:** market is more efficient than thesis; archetype not actionable for box-office.
- **Fail aggregate EV / pass directional:** restrict to >5pp divergence bins + maker-side entries only.

---

## A5 — Structural-feed detection + zero-modeling Σ-check overlay

Two sub-experiments because the archetype has two distinct mechanisms.

### A5(a) — Chatbot Arena leaderboard repricing lag

#### Thesis

New top-3 leaderboard entries on lmarena.ai precede Polymarket repricing by hours-to-days per [[feasibility/ai-tech-milestones]] §"Saturation". Long new leader + short displaced leader on rank-change detection.

#### Hypothetical edge

5-20pp gap captured at rank-change moment, closes over hours-to-days.

#### Conditions for success

1. lmarena.ai JSON API stable + machine-readable.
2. New top-3 entry within 4-wk window probable (base rate needs verification).
3. Hourly polling cadence sufficient (lag > 1h between leaderboard change and market repricing).
4. Sub-market depth absorbs $2-5K position without > 2pp impact.

#### Experiment

**Sample market:** `which-company-has-best-ai-model-end-of-june` ([[feasibility/ai-tech-milestones]] §1 — $5.89M all-time, $848K liq, 6-wk window).

**Run:**
1. Days 1-3: dual hourly poller (lmarena.ai/leaderboard/text + Polymarket Gamma API for Anthropic/Google/OpenAI/xAI sub-markets).
2. Days 4-30: for each detected top-3 rank change, log Polymarket prices at change_time + 1h + 2h + 4h + 8h + 24h. Simulate entry at t_change long-new-leader + short-displaced.
3. Parallel: HuggingFace `models?sort=createdAt` monitor on orgs (google, openai, anthropic, meta-llama, deepseek-ai, mistralai, 01-ai). Log card-create → leaderboard-appear → market-reprice.

**Time / cost:** ~3 days engineering + 30 days passive. Free.

#### Success criteria

| Metric | Bar |
|---|---|
| Median lag exceeds polling cadence | t_change → t_market_reprice_within_2pp > **2 hours** |
| Simulated trade EV | Avg return at T_change → T+24h > **+5%** after 5% taker fee |
| Sample size | ≥**2 events** partial signal / ≥**5 events** confident |

**Outcomes:**
- **Pass:** scale to $2-5K/trade on next rank change; extend monitoring to pre-leaderboard HF signals.
- **Sub-hour lag:** archetype requires WebSocket/co-located feed; defer pending infra.
- **<2 events in 30d:** rank changes too rare; defer to next 8-wk observation cycle.

### A5(b) — Daily Σ-check yield

#### Thesis

Daily Σ-check across NegRisk + ladder + threshold + RT + scenario-grid surfaces detects mechanical MRAs at zero modeling cost. Saguillo: ~$39.6M extracted Apr 2024-Apr 2025; 41% of conditions had ≥1 MRA opportunity per [[arbitrage-taxonomy]].

#### Hypothetical edge

3-10pp slack on detected violations; per-violation hedged EV +1-3% on $5-10K positions.

#### Conditions for success

1. MRAs ≥3/wk with slack >2pp to amortize automation.
2. Limit-order both legs simultaneously avoids partial-fill loss > 50bps.
3. UMA dispute risk per event identifiable + excludable per [[feasibility/geopolitical-date-ladder]] §8.
4. Polymarket-native bots dominate within-market MRA but semantic-dependency MRAs less saturated per [[combinatorial-arbitrage-empirics]].

#### Experiment

**Run:** 14-30 day daily Σ-check across 5 streams per [[feasibility-review]] §"Cross-cutting structural arb watchlist":
1. Days 1-5: build daily 9am ET automation across all 5 streams.
2. Days 6-30: log every violation > 2pp slack with leg liquidity, dispute risk classification, time-to-resolution.
3. Viable violations (slack > 2pp + LOW dispute + leg liq > $10K): paper-trade hedged entry; hold to resolution OR slack-close.
4. Day 30: aggregate per-violation hedged EV; multi-leg execution success rate.

**Time / cost:** ~5 days engineering + 30 days passive. Free.

#### Success criteria

| Metric | Bar |
|---|---|
| MRA frequency | ≥**3 violations/wk** with slack >2pp + LOW dispute + liq > $10K |
| Multi-leg execution viability | ≥**2 successful end-to-end hedged executions** with partial-fill loss < 50bps each |
| Net hedged EV | Aggregate after-fee P&L > **+1%** of total notional |

**Outcomes:**
- **Pass all:** scale to $5-10K/hedged arb real capital; combine with A5(a).
- **Fail frequency:** within-market MRA too saturated; restrict to semantic-dependency only (Midterms composite-vs-binary).
- **Fail execution:** restrict to single-market Σ-check (no cross-market arb).

---

## Sequencing and exit logic

**Week 1:** A5(b) automation built first — lowest engineering cost, broadest coverage, runs in background. A1 X API ingestion built in parallel; CZ paper-trade begins.

**Week 2:** A3 ICEMAN pipeline built; A4 backtest run (Phase 1 gate).

**Week 3:** A4 Phase 2 paper-trade begins (films release roughly weekly). A5(a) Chatbot Arena dual poller built; observation begins.

**Week 4:** First verdict per archetype:
- A1: Brier + win rate + EV from ~4 weeks of paper-trades.
- A3: Brier + directional accuracy from 3 ICEMAN episodes + cross-val.
- A4: Backtest verdict + 2-3 films from Phase 2.
- A5(a): Lag distribution + event count.
- A5(b): MRA frequency + execution viability + hedged EV.

**Archetypes that pass:** scale to real capital per per-archetype scale-up rules.
**Archetypes that fail any criterion:** redirect per per-archetype outcome rules.
**Archetypes that fail all criteria:** shelve; document failure mode in [[feasibility-review]] open follow-ups.

End-of-week-4 review consolidates verdicts and updates [[polymarket-strategy-matrix]] with empirically-validated archetype subset.

## Source

- [[feasibility-review]] — Recurring model archetypes section is the framework this roadmap operationalizes
- [[feasibility/mention-markets]] §3 + §7 — A1 + A3 modeling specs
- [[feasibility/movies]] §"Modeling spine" — A4 box-office multiplier spec
- [[feasibility/ai-tech-milestones]] §"Modeling spine" + §"Saturation" — A5(a) Chatbot Arena
- [[mention-markets]] — Kim et al. MixMCP `p_mix = 0.7·p_mkt + 0.3·p_mcp` reference
- [[arbitrage-taxonomy]] — Saguillo MRA definitions for A5(b)
- [[combinatorial-arbitrage-empirics]] — saturation evidence for semantic-dependency MRAs

## Related

- [[feasibility-review]]
- [[polymarket-strategy-matrix]]
- [[feasibility/mention-markets]]
- [[feasibility/movies]]
- [[feasibility/youtube]]
- [[feasibility/ai-tech-milestones]]
- [[feasibility/scenario-grid]]
- [[mention-markets]]
- [[arbitrage-taxonomy]]
- [[llm-forecasting-by-domain]]
