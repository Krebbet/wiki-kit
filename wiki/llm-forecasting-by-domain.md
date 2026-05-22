# LLM Forecasting Edge — by Domain

Two papers establish where LLM-based forecasting on prediction markets has signal and where it does not. **PolyBench** (arXiv 2604.14199) benchmarks 7 SOTA LLMs as trading agents on 38,666 Polymarket binary markets over a 6-day window (Feb 6–12 2026) using a financial metric (CWR — confidence-weighted return). **"Future Is Unevenly Distributed"** (arXiv 2511.18394) tests 4 LLMs across 6 categories on 150 questions (25 per category) pooled from Polymarket, Metaculus, and Manifold, using forecasting-accuracy metrics (Brier, ECE). Both findings converge: **Geopolitics and Politics are LLM-strong; Finance, Sports, and Crypto are LLM-weak**. This is the first-order deployment decision — domain choice dominates prompt-engineering or model selection.

**Both results are in-sample.** PolyBench evaluates the same 6-day window used for snapshot construction; the LLM-by-domain paper uses a held-out split within Jan–Jul 2025 but no walk-forward test. Treat the tier ranking as directional, not point-estimable.

## Domain tiers

(Sources: `raw/research/polymarket-market-trends-and-llm-edge/01-polybench-llm.md` Sec. 4–5 + `raw/research/polymarket-market-trends-and-llm-edge/04-llm-forecast-by-domain.md`.)

| Tier | Domains | Evidence |
|---|---|---|
| **Strong** | Geopolitics, Politics | GPT-5 Brier 0.14 on Geopolitics, ECE 0.09; GPT-4.1 88% accuracy on Geopolitics. PolyBench radar (Fig. 4): Politics positive-CWR for all 3 charted models. |
| **Mixed** | Entertainment, Technology | Best Brier 0.23 (Entertainment), 0.24 (Technology). **News augmentation hurts these** — Claude-3.7 Entertainment accuracy drops 68% → 56% with news; DeepSeek-R1 drops 68% → 40%. |
| **Weak** | Finance, Sports, Crypto | Finance accuracy 40–56% (near coin-flip). Sports 48–60%. PolyBench Crypto: models maintain confidence 0.8–0.9 despite "deeply negative" CWR — the worst domain by alpha. |

**Operational implication:** for the wiki's edge-finding goal, prefer Geopolitics/Politics markets for LLM-driven signal generation. Sports markets are *opportunity-rich* per [[arbitrage-taxonomy]] but the binding constraint is depth (see [[single-market-arbitrage-empirics]]) — LLM edge is not the bottleneck there. Finance and Crypto offer no LLM edge regardless of model.

## News-augmentation: helps where structure is text-encoded, hurts where it isn't

(`raw/research/polymarket-market-trends-and-llm-edge/04-llm-forecast-by-domain.md` Sec. 4.)

- **Finance and Sports** — adding 10 Exa-API news snippets per question (upper-bounded by question creation date) improves Brier and ECE. These domains require timely fact-grounding the base model lacks.
- **Entertainment and Technology** — adding the same context *hurts* materially. Mechanisms named in the source: **recency bias** (model overweights latest snippet), **rumour overweighting** (unverified snippet treated as fact), **definition drift** (snippet introduces a definition variant that contradicts the resolution criterion).
- **Geopolitics** — news adds marginal noise: Claude-3.7 84%→80%; GPT-5 holds at 84%; GPT-4.1 88%→76%.

Recipe per category:

| Category | Use news context? |
|---|---|
| Geopolitics | Optional; marginal noise |
| Politics | Optional; check per-model |
| Finance | Yes (with strict cutoff enforcement) |
| Sports | Yes (with strict cutoff enforcement) |
| Entertainment | **No** (or filter aggressively) |
| Technology | **No** (or filter aggressively) |

**Temporal-leakage warning** (Sec. 4 of the same paper): even with question-creation-date cutoffs on Exa retrieval, the authors observed snippets that resolved the question slipping through. Time-bounded retrieval is necessary but not sufficient — verify snippet content against cutoff date case-by-case.

## PolyBench — financial-metric findings

(`raw/research/polymarket-market-trends-and-llm-edge/01-polybench-llm.md`, Sec. 4–5.)

**Metric choice.** Authors explicitly decline Brier / log-loss / ECE, citing "lack of reliable, unbiased continuous probability references in volatile decentralized prediction markets." Their primary metric is **Confidence-Weighted Return**:

```
B_k = c_k · L                   — budget per trade (confidence × max lot)
π_k = S_k − I_k  (correct)      — profit per trade
π_k = −I_k       (incorrect)
CWR = Σ π_k / Σ I_k             — Eq. 3, Sec. 4.2
```

with `S_k` shares acquired by absorbing the CLOB ask side until `B_k` is exhausted. `APY = r · (365 / D)` annualizes per-trade returns by days-to-resolution `D`.

The methodological substitution is contestable: Brier *can* be computed against realized outcomes post-resolution, so the authors' objection is really to **using market prices as the calibration target**, not to proper scoring rules. **Cross-link** to [[llm-epistemic-calibration]] which does exactly that on Kalshi, but only for questions resolving *after* the model's training cutoff to eliminate contamination.

**Headline financial results** (in-sample, Feb 6–12 2026, $100 lot size):

| Model | Accuracy | Overall CWR | Notes |
|---|---|---|---|
| MiMo-V2-Flash | 62.1% | **+17.6%** | Best by CWR; alpha resilient up to ~$500 lot |
| Gemini-3-Flash | 75.0% | +6.2% | Highest accuracy; lower CWR due to confidence-weighting mismatch |
| Other 5 models | 53–59% | 0 to −12% | Below the accuracy floor for positive CWR |

The implicit accuracy floor for CWR profitability, holding confidence calibration ~constant, is **between 59% and 62%**.

### Strategy-tag analysis — Table 6

The PolyBench prompt asks the model to tag each trade with a strategy. Per-tag CWR (MiMo-V2-Flash):

| Strategy tag | CWR |
|---|---|
| **`news_catalyst`** | **50.0%** |
| `value_bet` | 19.2% |
| `arbitrage` | negative (across most models) |
| `stable_yield` | near-zero |

`news_catalyst` is the strongest individual tag — breaking-news shifts in expected value that the market hasn't yet absorbed. Consistent with the [[mention-markets]] mechanism in the adjacent paper: textual events with clear cut-off rules and clear resolution sources are where LLM-derived signal lives.

**`arbitrage` tag is semantic, not mathematical.** The LLM is identifying things *it calls* arbitrage; the consistently negative CWR strongly suggests these are not the [[arbitrage-taxonomy]] price-deviation arbitrages — they are false positives at the prompt level. Do not interpret PolyBench's negative arbitrage-tag CWR as evidence against the empirically-documented $40M MRA/Combinatorial extraction in `[[arbitrage-taxonomy]]`.

## Lot-size alpha ceiling

(`raw/research/polymarket-market-trends-and-llm-edge/01-polybench-llm.md` Sec. 5.)

Alpha decays logarithmically with lot size as CLOB depth is exhausted. Approximate ceiling at which alpha disappears:

- MiMo-V2-Flash: ~$500
- Gemini-3-Flash: degrades earlier (closer to $100)

This is the empirical instantiation of the depth-decay regression (SF8) in [[polymarket-microstructure]] applied to LLM-driven trades. Practical: **LLM edge exists but is not scalable beyond small position sizes** on the markets in this sample. The constraint is depth, not insight — same conclusion as the limits-to-arbitrage finding in [[single-market-arbitrage-empirics]].

## Confidence is informative — even when not "calibrated"

PolyBench reports `CWR > Non-CWR` (un-weighted return) for **all 7 models**: confidence-weighting strictly improves returns. Even without proper-scoring-rule calibration, LLM-expressed confidence carries useful signal. Implication for any pipeline: prefer confidence-weighted position sizing (PolyBench's `B_k = c_k · L`) over flat sizing, even if you have not yet recalibrated the confidence scores.

(Caveat: the systematic *over*confidence documented in [[llm-epistemic-calibration]] means raw confidence is not a probability. Confidence-weighted sizing is improved by sizing, not by the literal numeric value of the confidence. Combine with post-hoc calibration before using confidence as `p` in EV calculations.)

## Failure-mode taxonomy

(`raw/research/polymarket-market-trends-and-llm-edge/04-llm-forecast-by-domain.md` Sec. 4. **Caveat**: the prose example for *Rumour Overweighting* does not match the JSON trace in Appendix B.2 of the paper — the trace shows both predictions = NO, contradicting the narrative. Treat the taxonomy as credible, but do not cite that specific trace as confirmatory.)

1. **Recency bias** — most-recent snippet treated as most-load-bearing regardless of provenance.
2. **Rumour overweighting** — unverified/rumour snippets shift the posterior as if confirmed.
3. **Definition drift** — snippet introduces a definition variant that diverges from the resolution criterion (e.g., a colloquial sense vs the contract's specified sense).

These are the failure modes that drive the Entertainment/Technology degradation with news. They explain the recipe table above.

## Mapping to the wiki

- **Use this page to choose where to deploy.** If a market is in a Strong-tier category, an LLM forecast is a candidate signal. If in Weak-tier, default to other primitives ([[arbitrage-taxonomy]], [[polymarket-microstructure]] depth-decay timing, etc.).
- **Combine with [[mention-markets]]** for the operational pipeline on a specific Polymarket-emerging category where text-based signal applies.
- **Combine with [[llm-epistemic-calibration]]** before using LLM confidence as a probability for EV/Kelly sizing.

## Source

- `raw/research/polymarket-market-trends-and-llm-edge/01-polybench-llm.md` — PolyBench (arXiv 2604.14199); 7 LLMs × 38,666 Polymarket markets × 36,165 predictions; in-sample 6-day window Feb 6–12, 2026; CWR primary metric; strategy-tag analysis Table 6; lot-size alpha ceiling Sec. 5.
- `raw/research/polymarket-market-trends-and-llm-edge/04-llm-forecast-by-domain.md` — "Future Is Unevenly Distributed" (arXiv 2511.18394); 4 LLMs × 150 questions (25/category, 6 categories); pooled Polymarket/Metaculus/Manifold Jan–Jul 2025; Brier/ECE per category with and without news; failure-mode taxonomy.

## Related

- [[mention-markets]]
- [[llm-epistemic-calibration]]
- [[polyswarm-llm-trading-framework]]
- [[polymarket-microstructure]]
- [[arbitrage-taxonomy]]
- [[market-maker-handbook-prediction-markets]]
