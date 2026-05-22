# Feasibility — AI / Tech Milestones

Chatbot Arena leaderboard rank races, Gemini release-date ladders, and Figure F.03 robotics livestream markets. **YES-tier**, two distinct edge modes: (1) structural-feed monitoring on Chatbot Arena ranks (edge in detecting new model entries, not betting on current favorite); (2) survival/hazard modeling on Gemini release ladders (edge on conditional window pricing, especially Gemini 3.5 May/June threshold gap). No active GPT-6 standalone market exists. Live Gamma API 2026-05-16.

## Rubric (snapshot)

| Dimension | Notes |
|---|---|
| Data | Lmarena.ai live leaderboard (JSON scrape), USPTO trademark search, HuggingFace + GitHub release feeds, YouTube livestream counter for Figure — all free/structural |
| Modeling | Binary leaderboard-stability + USPTO-conditioned hazard model + Poisson rate extrapolation for Figure |
| Saturation | High on near-term Gemini ladders (3.2 May 22 at 96%); moderate on Chatbot Arena; low on Figure livestream + Gemini 3.5 |
| Liquidity | $39K–$2.31M; alpha ceiling ~$500/trade per [[llm-forecasting-by-domain]] PolyBench |

## Top markets

**Chatbot Arena (NegRisk candidate-race, lmarena.ai resolution):**

| Event | Slug | Vol_all | Vol_24h | Liq | End |
|---|---|---|---|---|---|
| Best AI model end of May | `which-company-has-the-best-ai-model-end-of-may` | $7.42M | $332K | $2.31M | 2026-05-31 |
| Best AI model end of June | `which-company-has-best-ai-model-end-of-june` | $5.89M | $37K | $848K | 2026-06-30 |
| Best AI model May (Style Control On) | `which-company-has-the-1-ai-model-end-of-may-style-control-on` | $550K | $57K | $225K | 2026-05-31 |
| Second-best AI model May | `which-company-has-the-second-best-ai-model-end-of-may` | $107K | $19K | $93K | 2026-05-31 |
| Best Chinese AI Company May | `best-chinese-ai-company-end-of-may` | $117K | $17K | $44K | 2026-05-31 |

**Gemini release-date ladders (NegRisk where flagged; structurally hazard):**

| Event | Slug | Vol_all | Vol_24h | Liq | End |
|---|---|---|---|---|---|
| Gemini 3.5 released by...? | `gemini-3pt5-released-by-june-30` | $1.35M | $54K | $39K | 2026-06-30 |
| Gemini 3.2 released on...? (27 buckets) | `gemini-3pt2-released-on` | $308K | $24K | $111K | 2026-05-31 |
| Gemini 3.2 released by...? | `gemini-3pt2-released-by` | $519K | $26K | $53K | 2026-06-30 |

**Figure F.03 robotics:**

| Event | Slug | Vol_all | Vol_24h | Liq | End |
|---|---|---|---|---|---|
| F.03 runtime without failure | `how-long-will-figures-f03-robots-run-without-failure` | $66K | $49K | $6K | 2026-05-21 |
| # packages pushed by May 21 | `of-packages-pushed-by-figures-f03-robots-by-may-21-10-pm-et` | $85K | $27K | $15K | 2026-05-21 |

**No active GPT-6 / GPT-5.5 release-date market exists** under `openai` or `gpt-5` tags as of 2026-05-16 — only the June leaderboard and Musk v. Altman litigation.

## Current implied probabilities

**Best AI model end of May:** Anthropic 81.5% / Google 18.5% / OpenAI 1.1% — Σ ≈ 1.013 (NegRisk near-Σ=1).
**End of June:** Anthropic 68.9% / Google 22.5% / OpenAI 6.5% — more uncertain over 6-week window.

**Gemini 3.5 ladder:**
```
S(May 31) = 0.197, S(June 30) = 0.104, S(July 31) = 0.055
P(release in June | not by May 31) = (0.896 − 0.803)/(1 − 0.803) = 47%
```

**Gemini 3.2 ladder (hazard concentrated at Google I/O May 20–21):**
```
S(May 15) ≈ 0.976  →  S(May 19) ≈ 0.130  →  S(May 22) ≈ 0.043
~83% mass in May 15–22 window
```

**Figure F.03 runtime:** P(≥200h) = 64.5%; resolves May 21.

## Data sources

| Source | Access | Signal |
|---|---|---|
| lmarena.ai/leaderboard/text | Public, JSON API stable | Live #1 per tab/style-control; resolution feed |
| HuggingFace `/models?sort=createdAt` | Free | Pre-leaderboard signal for new frontier model cards |
| GitHub `/releases` on key org repos | Free | Open-source release tag precedes HF card by hours |
| USPTO TSDR / TM full-text | Free | Model name filings 4–8 weeks before release; same-day in edge cases |
| Press release RSS (OpenAI/Anthropic/Google blogs) | Free | Public availability announcements |
| Google I/O 2026 (May 20–21) | Calendar | Dominant near-term catalyst |
| Figure F.03 YouTube livestream | Free (no API needed) | In-stream package counter + visible failure events |
| Brett Adcock @adcock_brett | Free | Backup signal for F.03 failure/pause |

## Modeling spine

**Chatbot Arena binary stability:**
```
P(rank_1 unchanged by T) = (1 − λ_displacement)^days_to_T
λ from historical leaderboard transition rate
update on HuggingFace/GitHub model-card detection in candidate org set
```

**Release-date hazard (Gemini):**
```
S_mkt(t) = 1 − P_market(release_by_t)
S_prior(t) = Weibull(α,β; t − last_release_date)
S_posterior = (1−w)·S_mkt + w·S_prior
signal updates: USPTO filing → S(t<filing+8wk) drops sharply
                I/O announcement public access → resolves YES
                I/O closed beta → modest positive shift on later legs
                I/O silence → negative on May 31, mass into June 30
```

**Figure F.03 (Poisson rate extrapolation):**
```
rate = packages_so_far / elapsed_hours
expected_final = packages_so_far + rate · hours_remaining
P(≥threshold) = 1 − Poisson_CDF(threshold−1; λ=expected_final)
runtime: P(survive to T | survived to t_now) = S(T)/S(t_now), exponential base hazard
```

## Structural-arb shape

- **Monotonicity Σ-check (Gemini 3.2 released-on, 27 buckets):** P(by T1) ≤ P(by T2) for T1<T2 must hold. Any inversion is MRA per [[arbitrage-taxonomy]].
- **NegRisk Σ-check (Chatbot Arena race events):** Σ P(Yes_i) ≈ 1.00 across named sub-markets.
- **NegRisk anonymization gap:** Gamma API anonymizes non-leading sub-markets ("Company A", "Company B"). Pattern: only companies with nonzero liquidity history appear with real names. Impact:
  - Main AI leaderboard (May/June): **No blocking** — Anthropic, Google, OpenAI, xAI, Alibaba, DeepSeek, etc. visible.
  - Best Chinese AI Company May: **Fully blocked** — all 25 sub-markets "Company A"–"Company Y" at $0. Requires off-platform reconstruction.
  - Style Control variant (May): **Partial** — top 3 visible.

## Microstructure regime

- **Deep markets:** May AI leaderboard $2.31M liq — spread tightness limits edge size; alpha ceiling ~$500/trade per [[llm-forecasting-by-domain]] PolyBench.
- **Two-horse race (May):** Anthropic 81.5% / Google 18.5% leaves limited repricing space unless new #1 model enters.
- **June 6-week window:** More uncertain (3 plausible runners); higher edge potential.
- **Thin Gemini 3.5 ($39K liq):** Position sizing constrained but meaningful.
- **Figure F.03 ($6K liq runtime):** Position cap ~$2K-$5K; tiny but high-information-rate.

## Saturation

- **Trademark filing tracking:** Documented practitioner edge among AI forecasting community. Compressed on near-term Gemini ladders. Residual edge on longer-horizon markets (Gemini 4.0, GPT-6 when listed).
- **Chatbot Arena niche:** Smaller tracking community. Lag between new model entry and market repricing = hours to days. **Structural-feed edge lives here.**
- **Figure F.03:** Unique observability via YouTube. Not standard AI-Twitter topic. Lowest saturation; tiniest liquidity.

| Market | Saturation | Position |
|---|---|---|
| May AI leaderboard (Anthropic 81.5%) | Near-saturated | <$1K or skip |
| June AI leaderboard | Moderate | ~$2–5K |
| Gemini 3.2 by May 22 (95.7%) | Highly saturated | Skip |
| Gemini 3.5 by May 31 (80.3%) | Moderate | ~$5K (thin liq) |
| Gemini 3.2 released-on (27 buckets) | Lower (per-day nuance) | ~$10K |
| Figure F.03 | Low | ~$2–5K |

## Decision-tree mapping

1. **Q1 YES-theme?** YES — leaderboard rank and release-date are observable structural feeds.
2. **Q2 Data source?** YES — lmarena.ai (free + = resolution), USPTO (free), HF/GitHub feeds (free), YouTube livestream for Figure.
3. **Q3 Structural-arb?** YES — Gemini released-on monotonicity (27 buckets); NegRisk Σ on Chatbot Arena.
4. **Q4 Microstructure?** Moderate liquidity allows real positions; alpha ceiling $500/trade binding on deep markets.

## Risks

1. **I/O resolution-ambiguity (Gemini 3.2):** "Limited beta" framing vs "open beta or rolling waitlist" criterion. Monitor exact language carefully.
2. **Leaderboard stability:** New #1 model entry within May/June would reprice Anthropic-YES sharply. Primary tail risk.
3. **NegRisk anonymization:** Best Chinese AI Company unworkable without off-platform candidate list reconstruction from lmarena.ai Chinese sub-leaderboard.
4. **Figure stream discontinuity:** YouTube outage or paused run → backup sources introduce resolution-certainty lag.
5. **Thin-liquidity alpha ceiling:** PolyBench-documented ~$500/trade — binding across all but May AI leaderboard.
6. **PolyBench classification refinement:** Tech is "mixed-tier" per [[llm-forecasting-by-domain]] but Chatbot Arena (single observable feed) is closer to Sports tier; treat as **stronger than Technology average**. Do NOT feed unfiltered AI-Twitter into pricing model (news-augmentation degrades accuracy on Technology).

## Operational checklist

1. Daily lmarena.ai/leaderboard/text scrape (both style-control states); alert on rank-1 change + new top-10 entry.
2. HuggingFace model-create monitor for orgs: google, openai, anthropic, meta-llama, deepseek-ai, mistralai, 01-ai.
3. Weekly USPTO TM search: "Gemini 3.5", "GPT-6", "Claude 4.5"; classes 9 + 42.
4. Google blog RSS for I/O announcements (May 20–21).
5. Figure F.03 livestream status check pre-position; daily compute rate + bracket model until May 21.
6. Gemini 3.2 released-on monotonicity Σ-check across 27 buckets.

## Open follow-ups

1. Trademark filing detection automation (daily USPTO crawl) — confirm no Gemini 3.5 filing exists before sizing on that ladder.
2. Build leaderboard transition rate λ from public battle history on lmarena.ai.
3. Reconstruct Chinese AI Company list from lmarena.ai Chinese sub-leaderboard — defer until candidate list available, then assess.
4. PolyBench Brier benchmark calibration: compute Chatbot Arena Brier vs PolyBench Technology baseline.

## Source

- `raw/feasibility/ai-tech-milestones/summary.md` (2026-05-16)
- `raw/research/polymarket-broad-coverage-sweep/01-polymarket-tech-gamma.md`
- Gamma API live pulls: `tag_slug=tech`, `tag_slug=ai`, `tag_slug=openai`, `tag_slug=gpt-5`
- Slugs `which-company-has-the-best-ai-model-end-of-may`, `gemini-3pt5-released-by-june-30`, `how-long-will-figures-f03-robots-run-without-failure`

## Related

- [[llm-forecasting-by-domain]]
- [[polymarket-strategy-matrix]]
- [[arbitrage-taxonomy]]
- [[polymarket-market-structures]]
- [[snapshots/polymarket-broad-coverage-sweep-2026-05-16]]
- [[feasibility-review]]
