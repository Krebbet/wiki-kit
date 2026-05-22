---
title: "Feasibility Assessment — AI / Tech Milestone Markets"
captured_on: "2026-05-16"
tags: [ai, tech, chatbot-arena, release-dates, robotics, feasibility]
schema_version: 1
---

# Feasibility Assessment — AI / Tech Milestone Markets

Structured 10-section assessment covering Chatbot Arena leaderboard markets, AI model release-date ladders (Gemini 3.x; no active GPT-6 standalone event found), and Figure robotics livestream markets. Sources: Gamma API pulls on `tech`, `ai`, `openai`, and `gpt-5` tags (2026-05-16) plus existing wiki research base.

---

## 1. Market Inventory

**AI Leaderboard Race markets (Chatbot Arena, lmarena.ai)**

| Event | Slug | Vol (all-time) | Vol 24h | Liq | NegRisk | End |
|---|---|---|---|---|---|---|
| Best AI model end of May | `which-company-has-the-best-ai-model-end-of-may` | $7.42M | $332K | $2.31M | Yes | 2026-05-31 |
| Best AI model end of May (Style Control On) | `which-company-has-the-1-ai-model-end-of-may-style-control-on` | $550K | $57K | $225K | Yes | 2026-05-31 |
| Second-best AI model end of May | `which-company-has-the-second-best-ai-model-end-of-may` | $107K | $19K | $93K | Yes | 2026-05-31 |
| Best Coding AI model end of May | `which-company-has-the-best-coding-ai-model-end-of-may` | $36K | $8K | $56K | Yes | 2026-05-31 |
| Second-best Coding AI model end of May | `which-company-has-the-second-best-coding-ai-model-end-of-may` | $34K | $24K | $43K | Yes | 2026-05-31 |
| Best Chinese AI Company end of May | `best-chinese-ai-company-end-of-may` | $117K | $17K | $44K | Yes | 2026-05-31 |
| Best AI model end of June | `which-company-has-best-ai-model-end-of-june` | $5.89M | $37K | $848K | Yes | 2026-06-30 |
| Which companies have #1 AI model by June 30 | `which-companies-will-have-a-1-ai-model-by-june-30` | $1.56M | $6K | $33K | No | 2026-06-30 |

**Release-date ladder markets (Gemini)**

| Event | Slug | Vol (all-time) | Vol 24h | Liq | NegRisk | End |
|---|---|---|---|---|---|---|
| Gemini 3.5 released by...? | `gemini-3pt5-released-by-june-30` | $1.35M | $54K | $39K | No | 2026-06-30 |
| Gemini 3.2 released by...? | `gemini-3pt2-released-by` | $519K | $26K | $53K | No | 2026-06-30 |
| Gemini 3.2 released on...? | `gemini-3pt2-released-on` | $308K | $24K | $111K | Yes | 2026-05-31 |
| New Gemini reasoning flagship released by...? | `new-gemini-reasoning-flagship-released-by` | $97K | $8K | $27K | No | 2026-06-30 |

**GPT / OpenAI standalone release-date markets:** None active under `openai` or `gpt-5` tags as of 2026-05-16. The `openai` tag surfaces only the June leaderboard market and the Musk v. Altman litigation. No GPT-6 event exists.

**Robotics livestream markets (Figure F.03)**

| Event | Slug | Vol (all-time) | Vol 24h | Liq | NegRisk | End |
|---|---|---|---|---|---|---|
| Figure F.03 runtime without failure | `how-long-will-figures-f03-robots-run-without-failure` | $66K | $49K | $6K | Yes | 2026-05-21 |
| Figure F.03 packages pushed by May 21 | `of-packages-pushed-by-figures-f03-robots-by-may-21-10-pm-et` | $85K | $27K | $15K | No | 2026-05-21 |

---

## 2. Resolution Mechanisms

**Chatbot Arena leaderboard markets:** All eight leaderboard markets resolve by reading the "Rank" column in the "Text Arena | Overall" (or "Coding") tab at `https://lmarena.ai/leaderboard/text` at exactly 12:00 PM ET on the stated date. Style Control is toggled per the specific market. Tiebreaker order: Arena score then alphabetical company name. The feed is publicly accessible, machine-readable (JSON API available), and continuously updated. This is the single cleanest observable resolution source in the AI/tech market cluster.

**Gemini release-date ladders:** Resolve YES if Google makes a named model (Gemini 3.2 / 3.5 / reasoning flagship) "available to the general public" — open beta or rolling waitlist qualifies; closed beta does not. "Gemini 4" does not count toward Gemini 3.5. Resolution source is a consensus of credible reporting, with Google's own announcement as primary. Resolution ambiguity risk: Google I/O announcements with phased rollouts could trigger dispute (closed vs. open access timing). This is the dominant resolution-risk for the ladder markets.

**Figure F.03 robotics markets:** Resolve against Figure's official YouTube livestream (`https://www.youtube.com/watch?v=luU57hMhkak`). Runtime market: counts whole hours until a 2-minute window with zero packages pushed. Package count market: reads the in-stream counter. Backup sources: Brett Adcock's X account, credible reporting. The data source is a YouTube live counter — publicly accessible, low-latency, unambiguous. No API needed; visual monitoring of the stream suffices.

---

## 3. Data Sources and Observability

**Chatbot Arena (lmarena.ai)**
- Public leaderboard at `https://lmarena.ai/leaderboard/text`. Real-time updates as votes are cast.
- JSON API endpoint available (undocumented but stable; structured scrape is practical).
- Resolution-relevant state: current #1 rank per tab/style-control combination.
- **Structural-feed observable** — this is a quant edge, not a rumour-chasing edge. The leaderboard changes discretely when a new model enters and displaces the leader. Monitor rate: check daily with spike-detection on model additions.
- Model card releases on Hugging Face signal imminent leaderboard insertion for open-source models. Track `https://huggingface.co/models?sort=createdAt` for new frontier-model cards from key orgs (google, openai, anthropic, meta-llama, deepseek-ai, mistralai, 01-ai).
- GitHub release commits: for open-source models (Meta Llama, Mistral, DeepSeek), a public repo release tag precedes HuggingFace card by hours. Watch `github.com/{org}/{model}/releases`.

**USPTO trademark filings**
- Public USPTO full-text search at `https://tmsearch.uspto.gov`. Model names (e.g., "Gemini 3.5", "GPT-6") are typically filed 4-8 weeks before release; in some cases same-day.
- Known practitioner edge: trademark tracking is documented as a signal for release-date markets. Search for OpenAI, Google, Anthropic in trademark classes 9, 42 (software, SaaS).
- Caveat: negative signal only (no filing != no release). Positive signal (new filing) has strong but not 1:1 predictive value.

**Press release feeds**
- OpenAI: `https://openai.com/blog` (RSS-parseable). Anthropic: `https://www.anthropic.com/news`. Google: `https://blog.google/technology/ai/` and Google DeepMind blog.
- I/O timing: Google I/O 2026 is scheduled for May 20-21. This is the dominant near-term catalyst for Gemini 3.2 / 3.5 / reasoning flagship markets.
- Hugging Face model cards: `https://huggingface.co/blog` and individual model cards under `/google/`, `/openai/`, `/anthropic/` namespaces.

**Figure robotics**
- Resolution source is the YouTube livestream itself (link in market description). No separate API needed. The in-stream package counter is the primary observable.
- Brett Adcock's X account (@adcock_brett) is a designated backup source. Monitor for posts signaling failure/pause.

---

## 4. Current Market Prices and Implied Probabilities

**Best AI model end of May (lmarena.ai, style control off, 2026-05-16):**

| Company | P(Yes) | Notes |
|---|---|---|
| Anthropic | 0.815 | Current #1 on leaderboard |
| Google | 0.185 | Gemini series competitive; Google I/O catalyst imminent |
| OpenAI | 0.011 | Sharp decline from prior months |
| xAI | 0.0015 | Grok not near top |
| All others | <0.002 | Near-zero |

Implied: P(Anthropic OR Google) ≈ 1.000. Two-horse race. NegRisk constraint check: Sigma P_i at current prices ≈ 1.013 — small overage consistent with bid/ask spread; check sub-market level for arb.

**Best AI model end of June (lmarena.ai, style control off, 2026-05-16):**

| Company | P(Yes) |
|---|---|
| Anthropic | 0.689 |
| Google | 0.225 |
| OpenAI | 0.065 |
| xAI | 0.0145 |
| All others | <0.008 |

June market is more uncertain than May (Anthropic drops from 81.5% to 68.9%), reflecting probability of new model releases over a longer window.

**Gemini 3.5 released by...:**

| Deadline | P(Yes) |
|---|---|
| March 31 (closed) | 0.000 |
| April 30 (closed) | 0.000 |
| May 31 | 0.803 |
| June 30 | 0.896 |
| July 31 | 0.945 |

Implied conditional P(release in June | not by May 31) = (0.896 - 0.803) / (1 - 0.803) = 0.093/0.197 ≈ 47%.

**Gemini 3.2 released by...:**

| Deadline | P(Yes) |
|---|---|
| May 8 (past) | 0.000 |
| May 15 | 0.024 |
| May 18 | 0.029 |
| May 19 | 0.870 |
| May 22 | 0.957 |
| May 31 | 0.980 |
| June 30 | 0.994 |

Market-implied survivor function drops sharply at May 19-22 window. Google I/O (May 20-21) is the obvious catalyst. The 27-bucket "released on" market gives a full day-by-day PMF.

**Figure F.03 runtime:**

| Bracket | P(Yes) |
|---|---|
| <8 hours | 0.000 |
| 8-50 hours | 0.000 |
| 50-100 hours | 0.160 |
| 100-200 hours | 0.215 |
| 200+ hours | 0.645 |

Market consensus at capture: 64.5% probability of >=200 hours continuous operation. Resolves May 21.

---

## 5. NegRisk Anonymization Issue

**Finding: Partially blocks modeling for some sub-markets; does not block the primary edge.**

The Gamma API anonymizes non-leading sub-market candidates in NegRisk events as "Company A", "Company B", "Company C", etc. This is systematic across 16 of 30 tech-tag events. Pattern: only companies that have ever held nonzero liquidity appear with their real names; those that have never attracted trading are anonymized.

**Impact by market type:**

- **Main AI leaderboard race (Best AI model May/June):** No blocking. All major companies (Anthropic, Google, OpenAI, xAI, Alibaba, ByteDance, DeepSeek, Meta, Mistral, Meituan, Baidu, Microsoft, Amazon, Moonshot, Z.ai) appear with real names and current prices. The only anonymized slots are the true tail (never traded). Modeling the top 2-3 outcomes is fully feasible.

- **Best Chinese AI Company end of May (`best-chinese-ai-company-end-of-may`):** Fully blocked. All 25 sub-markets appear as "Company A" through "Company Y" with zero volume and zero prices. No price discovery has occurred. Modeling this market requires reconstructing the full company list off-platform (e.g., from the Chatbot Arena Chinese-model sub-leaderboard at lmarena.ai), then mapping to anonymized slots — labor-intensive with no guarantee of correct assignment.

- **Style-Control variant (May, Style Control On):** Partial. Anthropic (0.820), Google (0.170), OpenAI (0.013), Mistral, Meituan visible; "Company C", "Company I" anonymized. Modeling the top 3 is feasible.

**Operational conclusion:** For the primary Chatbot Arena leaderboard markets, anonymization does not block modeling — the full PMF across tradeable outcomes is visible. For the Chinese-market-specific sub-variant, anonymization creates a gap requiring off-platform reconstruction. Flag as a known data-quality limitation rather than a hard block on the category.

---

## 6. Edge Assessment by Market Type

### 6a. Chatbot Arena Leaderboard Race (Monthly Rank Markets)

**Verdict: YES — structural-feed observable edge; thin on the May market, more interesting on June.**

Edge mechanism: The leaderboard is a live, public, machine-readable feed. Position changes are discrete events (new model enters and displaces current leader). The edge is:
1. **Pre-leaderboard-update positioning** — detect a new top model (via HuggingFace card / GitHub release tag / press release) before it appears on Chatbot Arena and before the market has repriced.
2. **Intra-month leaderboard monitoring** — track daily rank changes; update position sizing as the leader's lead widens or narrows.

**Saturation check:** The May market ($7.42M volume, $2.31M liquidity) is deep by Polymarket standards. Spread tightness limits edge size; alpha ceiling per [[llm-forecasting-by-domain]] PolyBench data is ~$500/trade. The two-horse race (Anthropic 81.5% / Google 18.5%) leaves limited repricing opportunity unless a new #1 model enters.

The June market ($5.89M, $848K liquidity) is more interesting: Anthropic 68.9% / Google 22.5% / OpenAI 6.5% leaves meaningful uncertainty across 3 runners over a 6-week window.

**PolyBench classification note:** Technology is nominally "mixed-tier" per [[llm-forecasting-by-domain]]. However, the Chatbot Arena sub-category is a structural-feed market — the resolution source is an observable number, not a qualitative judgment. Treat as **stronger than the Technology tier average**. The mixed-tier rating applies to diffuse tech questions; leaderboard markets with a single authoritative feed are analytically closer to Sports (observable outcome) than general Technology (judgment-required).

**News augmentation warning:** Per [[llm-forecasting-by-domain]], Technology markets show accuracy degradation with news augmentation (recency bias, rumour overweighting). Do not feed unfiltered AI-Twitter commentary into a pricing model. Stick to the leaderboard feed itself as the signal source.

### 6b. Release-Date Ladder Markets (Gemini 3.x)

**Verdict: YES — survival/hazard model applies; residual edge on within-window timing.**

**Structural fit:** Gemini release-date "by T" ladders are textbook survival data. Let S(t) = P(release > t) = 1 - P(release by t). The market-implied survivor function for Gemini 3.2:

```
S(May 15) ≈ 0.976
S(May 19) ≈ 0.130  [~84% probability mass in May 15-19 window]
S(May 22) ≈ 0.043
S(May 31) ≈ 0.020
S(Jun 30) ≈ 0.006
```

The implied hazard at Google I/O (May 20-21) is enormous: ~83% probability of release in the May 15-22 window. The "released on" market (slug `gemini-3pt2-released-on`) with 27 buckets extends this to a full PMF over calendar days — the monotonicity constraint P(by T1) <= P(by T2) for T1 < T2 must hold across all ladder legs; any violation is an MRA per [[arbitrage-taxonomy]].

**Hazard model inputs:**
- Prior release cadence: Gemini 1.0 -> 1.5 -> 2.0 -> 2.5 -> 3.0 -> 3.1 -> 3.2 series. Model inter-release gaps; condition on current elapsed time.
- Known catalysts: Google I/O 2026 (May 20-21) is the strongest positive catalyst. Historically, Gemini major versions have accompanied I/O.
- USPTO trademark search for "Gemini 3.5": check for any new filings; a fresh filing would sharply shift the 3.5 ladder.

**Saturation:** Gemini 3.2 markets are near-fully priced for May-22 release (96%). The residual edge is in the exact-day market (`gemini-3pt2-released-on`, 27 buckets, $111K liquidity) with nuanced per-day pricing. The Gemini 3.5 market ($39K liquidity) is thin enough for a meaningful position.

**GPT-6 note:** No standalone GPT-6 or GPT-5.5 release-date ladder exists as of this capture. The `openai` tag surfaces only the June leaderboard and the Musk v. Altman litigation. Trademark tracking (see Section 3) is the recommended early-signal source to detect when a GPT-6 market may open.

### 6c. Figure F.03 Robotics Livestream Markets

**Verdict: YES — unique market type; data source is the YouTube livestream itself; closes May 21.**

**Market uniqueness:** These are the only Polymarket markets in the current sweep that resolve against a live YouTube stream counter. Resolution state is visible in real-time to anyone watching, with no intermediary. The edge is:
1. **Rate extrapolation:** The package counter increments continuously. At any point: current packages / elapsed hours = throughput rate. Project forward to May 21 10 PM ET. Poisson model; adjust for observed downtime.
2. **Failure-time modeling:** The runtime market resolves on first failure (2-min gap in conveyor activity). Monitor the stream for near-failure events; update P(>200h) as elapsed time increases without failure.

**Data source details:** Figure's YouTube livestream `https://www.youtube.com/watch?v=luU57hMhkak`. The in-stream counter is the authoritative resolution source. Backup: Brett Adcock's X account (@adcock_brett) for announced pauses/failures.

**Current state (2026-05-16):** Market prices P(>=200h) = 64.5%. The market is 5 days from its May 21 close. If the stream has been running continuously since opening, elapsed time at capture determines the posterior — a live check of the stream is the first operational step.

**Liquidity warning:** Runtime market has only $6K liquidity and $66K volume. Position-sizing ceiling is very low; MRA may have a large percentage impact on the bracket.

---

## 7. Competing Forecasters / Saturation Assessment

**AI Twitter / forecasting community saturation:**

- AI model release dates (especially GPT-X, Gemini-X) are among the most actively tracked topics on AI Twitter. Large accounts and dedicated trackers monitor trademark filings and press release timing. The Gemini 3.2 market at ~96% for May 22 and the near-consensus on Google I/O as the vehicle suggests the market is already well-informed.
- Trademark-filing tracking is a **known, documented edge** among AI forecasting practitioners. The residual edge from this source has likely compressed on near-term Gemini ladders. The edge remains on longer-horizon markets (Gemini 4.0, GPT-6 if/when such markets open).
- Chatbot Arena leaderboard changes are tracked by a much smaller community — this is more niche. The lag between a new model appearing on the leaderboard and market repricing may be hours to days, depending on how closely retail follows the leaderboard. This is where the structural-feed edge lives.

**Robotics markets:** Figure F.03 livestream markets are unique and not a standard AI-Twitter tracking topic. The package counter is observable to anyone, but the market depth ($6K-$15K liquidity) suggests low participation. This is the thinnest and potentially most exploitable sub-category if you can maintain real-time stream monitoring.

**Assessment by market:**
- May AI leaderboard (81.5% Anthropic): near-saturated; edge only if Anthropic loses #1 before May 31.
- June AI leaderboard: moderate saturation; 6-week window with multiple potential model releases keeps uncertainty alive.
- Gemini 3.2 release by May 22 (95.7%): highly saturated; near-fully priced.
- Gemini 3.5 release by May 31 (80.3%): moderate saturation; $39K liquidity is thin enough for a position.
- Figure F.03 markets: low saturation; unique observability but tiny liquidity.

---

## 8. Modeling Approaches

### Chatbot Arena Leaderboard Race

**Model:** Binary event model (will current #1 remain #1 by resolution date?), updated daily.

Inputs:
- Current leaderboard rank and Arena score (from lmarena.ai API or scrape).
- Model release news: HuggingFace new model cards (filter for orgs: google, openai, anthropic, meta-llama, deepseek-ai, mistralai, 01-ai).
- GitHub release tags for open-source models.
- Prior probability based on historical leaderboard stability — how often does the #1 rank change within a calendar month? (Compute from Chatbot Arena's public battle history.)

Update rule: Bayesian; prior = current market price; likelihood update triggered by new model entries that could plausibly displace current #1.

### Release-Date Ladder (Survival/Hazard)

**Model:** Non-parametric survival model calibrated to market-implied S(t), updated on each new signal.

```python
# Pseudocode
S_mkt = {date: 1 - P_market(release_by_date) for date in ladder_dates}
# Structural prior from historical release cadence
S_prior = weibull_cdf(alpha, beta, t - last_release_date)
# Bayesian blend
S_posterior = (1 - w) * S_mkt + w * S_prior
# Signal update when trademark filed or I/O announcement confirmed:
S_posterior[t >= announcement_date] *= p_conditional_on_announcement
```

Catalyst signals and directional impact:
- USPTO trademark filing (new): strong positive (release imminent; reduce S(t) sharply for near-term legs).
- Google I/O announcement of public availability: resolves May 31 YES.
- I/O demo without public access: modest positive shift (beta access raises P(public by June 30)).
- Silence at I/O: negative update on May 31; June 30 absorbs the probability mass.

### Figure F.03 Livestream (Rate Extrapolation)

**Model:** Poisson rate with known endpoint.

```python
# At time t_now:
packages_so_far = read_stream_counter()
elapsed_hours = (t_now - t_start).total_seconds() / 3600
rate = packages_so_far / elapsed_hours  # packages/hour
hours_remaining = (t_deadline - t_now).total_seconds() / 3600
expected_final = packages_so_far + rate * hours_remaining
# P(>= threshold) = 1 - Poisson_CDF(threshold - 1, lambda=expected_final)
```

Runtime model: At time t_now with no failure yet, P(survive to T | survived to t_now) = S(T) / S(t_now) under a parametric hazard model. Use exponential (constant hazard) as base; update parameters from any near-failure events observed in the stream.

---

## 9. Operational Checklist

1. **Chatbot Arena monitor:** Set up daily scrape of `lmarena.ai/leaderboard/text` (both style-control states). Alert on any rank-1 change. Alert on new model entries in top 10.
2. **HuggingFace / GitHub model-release monitor:** Watch `huggingface.co/models?sort=createdAt` daily for frontier-model cards from key orgs. GitHub API on `/releases` for deepseek-ai, google-deepmind, meta-llama, mistralai.
3. **USPTO trademark search:** Weekly search for "Gemini 3.5", "GPT-6", "Claude 4.5" in classes 9 and 42. Baseline: confirm no current filing for Gemini 3.5 before taking a position on the 3.5 market.
4. **Google press release feed:** Monitor `blog.google/technology/ai/` RSS for I/O-adjacent announcements. I/O is May 20-21; any public release announcement resolves Gemini 3.2 YES.
5. **Figure F.03 livestream:** Check stream status immediately before entering positions. Compute current rate; update package-count and runtime-bracket model. Monitor daily until May 21 close.
6. **Gemini 3.2 released-on market (27 buckets):** Run monotonicity Sigma-check across all 27 day-buckets. Any P(by T1) > P(by T2) for T1 < T2 is an MRA per [[arbitrage-taxonomy]].
7. **NegRisk Sigma-check:** For all NegRisk leaderboard markets, verify Sigma P(Yes_i) ≈ 1.00 across named sub-markets. Overage > 1.0 or significant underage creates combinatorial pressure.

---

## 10. Verdict and Recommendations

**One-line verdict:** AI/tech milestone markets are a YES-tier opportunity with two distinct edge modes — leaderboard-feed structural monitoring for rank races (edge concentrates in detecting new model entries, not betting on the current favorite) and survival/hazard modeling for Gemini release ladders (edge on conditional window pricing, particularly the May/June threshold gap on the 3.5 market).

**Priority ranking by feasibility:**

| Market | Edge Mode | Feasibility | Position Limit |
|---|---|---|---|
| Gemini 3.5 released by May 31 / June 30 | Hazard + USPTO | High | ~$5K (thin liq $39K) |
| Gemini 3.2 released on exact-day (27 buckets) | Monotonicity arb + hazard | High | ~$10K ($111K liq) |
| Figure F.03 package count / runtime | Rate extrapolation, stream monitor | High (if stream live) | ~$2K-$5K (thin) |
| Best AI model end of June (Anthropic/Google/OpenAI) | Leaderboard structural feed | Medium | ~$2K-$5K (deep liq, alpha ceiling ~$500/trade) |
| Style Control On variant (May) | Leaderboard structural feed | Medium | ~$2K (thinner) |
| Second-best AI model May | Leaderboard structural feed | Medium | ~$3K ($93K liq) |
| Best AI model end of May | Leaderboard structural feed | Low (saturated, Anthropic 81.5%) | <$1K or skip |
| GPT-6 release markets | Hazard + USPTO | Deferred (no market exists) | — |

**Key risks:**

1. **Google I/O resolution-ambiguity risk** — if Google announces Gemini 3.2 at I/O in a "limited beta" framing, whether this triggers YES resolution is not cut-and-dried per the resolution criteria ("open beta or rolling waitlist acceptable"). Monitor the exact language of any Google announcement against the resolution rule closely.
2. **Leaderboard stability risk** — a new #1 model entering Chatbot Arena (e.g., a GPT-4.1 update, new Gemini version) within the May/June window would sharply reprice the market. This is the primary tail risk for Anthropic-YES holders.
3. **NegRisk anonymization gap** — the Best Chinese AI Company market is fully anonymized (all 25 slots show "Company X" with $0 volume). Do not enter this market without reconstructing the full company list from lmarena.ai's Chinese model sub-leaderboard first.
4. **Figure F.03 livestream discontinuity** — if the stream goes offline (outage, or Figure pauses the run) the market's observable data source disappears. Backup sources (Adcock X, credible reporting) introduce a resolution-certainty lag.
5. **Thin liquidity ceiling** — the highest-feasibility markets (Gemini 3.5, Figure) have liquidity of $6K-$53K. The alpha ceiling from PolyBench (~$500/trade) is the binding constraint across all these markets; position sizing must be calibrated against depth curves, not theoretical EV.

---

## Sources

- `raw/research/polymarket-broad-coverage-sweep/01-polymarket-tech-gamma.md` — Tech tag Gamma API capture 2026-05-16 (30 events)
- `raw/research/polymarket-broad-coverage-sweep/.ingest/01-polymarket-tech-gamma.summary.md` — Ingest summary with verdicts
- `wiki/llm-forecasting-by-domain.md` — PolyBench domain tiers; Technology mixed-tier; news augmentation failure modes
- `wiki/polymarket-strategy-matrix.md` — AI/tech milestone strategy stub; NegRisk anonymization note
- Gamma API live pulls: `tag_slug=tech`, `tag_slug=ai`, `tag_slug=openai`, `tag_slug=gpt-5`, event slugs `which-company-has-the-best-ai-model-end-of-may`, `gemini-3pt5-released-by-june-30`, `how-long-will-figures-f03-robots-run-without-failure` (all 2026-05-16)

## Related

- [[llm-forecasting-by-domain]]
- [[polymarket-strategy-matrix]]
- [[arbitrage-taxonomy]]
- [[polymarket-market-structures]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
