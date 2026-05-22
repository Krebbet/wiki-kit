# LLM Epistemic Calibration on Prediction Markets

KalshiBench (arXiv 2512.16030) tests 5 frontier LLMs on 300 Kalshi binary questions resolving **after** all model training cutoffs (Oct 1 – Nov 30, 2025; methodology directly portable to Polymarket). The headline finding: **all frontier LLMs are systematically overconfident**; only one of five (Claude Opus 4.5, Brier 0.227, ECE 0.120) beats the base-rate baseline by Brier Skill Score; **extended-reasoning modes calibrate worse than base models**; and cost-per-prediction does not predict calibration (DeepSeek-V3.2 at $0.36/run achieves better ECE than GPT-5.2-XHigh at $30.32/run). Operational consequence: **LLM-expressed confidence scores cannot be used as probabilities for EV / Kelly sizing without post-hoc calibration** (temperature scaling or Platt scaling required).

**Caveat — model-naming anachronism.** The paper credits NeurIPS 2024 as its venue but evaluates models with claimed training cutoffs through October 2025 (`Claude Opus 4.5`, `GPT-5.2-XHigh`, etc.) — model identifiers not consistent with publicly-available NeurIPS-2024-era releases. The internal calibration methodology is self-consistent and credible; the specific *per-model* numbers should be treated with caution if cross-referenced against external benchmarks. Use the **methodology** (temporal filtering, calibration metric definitions) as load-bearing; treat the per-model rankings as illustrative.

## Why this matters for Polymarket

The wiki's modeling backbone — [[logit-jump-diffusion-kernel]] and [[market-maker-handbook-prediction-markets]] — is validated only on synthetic data drawn from the kernel's own distribution. **KalshiBench is the most rigorous real-data calibration study in the captured corpus** and its temporal-filter methodology is directly applicable to Polymarket. If you build any LLM-driven signal pipeline for Polymarket, the calibration discipline below is the price of entry.

Connects directly to:
- [[mention-markets]] — Kim et al.'s MCP technique outputs LLM probabilities that, per this paper, are systematically overconfident before recalibration. MCP's `α=0.7` market-prior weighting partially neutralizes this, but doesn't replace explicit calibration.
- [[polyswarm-llm-trading-framework]] — quarter-Kelly sizing using raw LLM confidence as `p` is risky absent calibration; over-stated `p` → over-sized positions.
- [[llm-forecasting-by-domain]] — PolyBench declined Brier/ECE metrics on Polymarket entirely; KalshiBench is the methodology that PolyBench *should have* used (or that we should apply on top of PolyBench data).

## The temporal-filtering methodology (the load-bearing contribution)

Eliminates training-data contamination — the dominant failure mode for any LLM forecasting benchmark.

```
D_filtered = { (q, y) ∈ D :  t_close(q)  >  max_{m ∈ M}  t_cutoff(m) }
```

Read: keep only questions whose **resolution time** `t_close(q)` is strictly later than the **latest training cutoff** across the set of models `M` being evaluated. For the 5-model panel in this paper, the cutoff was October 1, 2025.

**Why it matters.** A model whose training data includes the *resolved* outcome will trivially predict it; this inflates accuracy without measuring forecasting ability. Without temporal filtering, any benchmark on past prediction markets measures memorization, not foresight. KalshiBench's filter is conservative (max across all models), so the dataset shrinks substantially, but the resulting evaluation is contamination-clean.

Operational implication for Polymarket evaluation pipelines: apply the same rule to your own backtests. Use `gamma-api.polymarket.com/events?slug=...` to query `closingDate` (or equivalent) and filter against your model's published cutoff. **Without this filter, all forecasting-edge claims on historical markets are suspect.**

Other dataset-shape rules cited:
- **Deduplication:** limit 2 questions per series ticker to preserve diversity while reducing temporal redundancy.
- **Exclusion of ambiguous resolutions:** contracts with missing or unclear criteria filtered out at quality-screening stage.

## Calibration metrics — definitions

```
Brier Score:        BS  = (1/N) Σᵢ (pᵢ − yᵢ)²
                    benchmarks: 0 (perfect) | 0.20 (good calibration / human range) | 0.25 (random p=0.5)

Brier Skill Score:  BSS = 1 − BS / BS_climatology,  BS_climatology = ȳ(1 − ȳ)
                    positive BSS → beats naive base-rate predictor; ȳ = 0.40 in this sample

Expected Calibration Error (B=10 bins):
                    ECE = Σ_b (|B_b| / N) · | acc(B_b) − conf(B_b) |

Maximum Calibration Error:
                    MCE = max_b | acc(B_b) − conf(B_b) |

Overconfidence Rate at threshold τ:
                    OCR@τ = | { i : pᵢ > τ ∧ ŷᵢ ≠ yᵢ } | / | { i : pᵢ > τ } |
```

Human anchors (Tetlock & Gardner 2015):
- **Superforecaster Brier:** 0.15–0.20.
- **Superforecaster ECE:** ~0.03–0.05.
- **Aggregate prediction-market wisdom-of-crowds:** Brier 0.12–0.18.

## Per-model headline results

(Source: `raw/research/polymarket-market-trends-and-llm-edge/05-kalshibench-llm-calibration.md`. Sample: N = 300; window: Oct 1 – Nov 30, 2025; platform: Kalshi binary contracts; base rate ȳ = 0.40.)

| Model | Accuracy | Brier ↓ | BSS ↑ | ECE ↓ | MCE ↓ |
|---|---|---|---|---|---|
| Claude Opus 4.5 | 69.3% | **0.227** | **+0.057** | **0.120** | **0.246** |
| Kimi-K2 | 67.1% | 0.347 | −0.446 | 0.298 | 0.570 |
| Qwen3-235B | 65.7% | 0.346 | −0.437 | 0.297 | 0.479 |
| DeepSeek-V3.2 | 64.3% | 0.339 | −0.407 | 0.284 | 0.630 |
| GPT-5.2-XHigh | 65.3% | 0.433 | −0.799 | 0.395 | 0.622 |

**Five readings:**

1. **Only Claude beats the base rate** (BSS > 0). Four of five models are *worse than always predicting 0.40* on Brier — a 50%-yes baseline strategy strictly dominates them.
2. **Best LLM Brier (0.227) is materially worse than human superforecaster Brier (0.15–0.20).** LLMs as currently configured do not match expert human forecasters on this task.
3. **Best LLM ECE (0.120) is 2.4–4× worse than human superforecaster ECE (~0.03–0.05).** The calibration gap is the more important gap; raw probabilities are usable only after recalibration.
4. **GPT-5.2-XHigh — extended-reasoning model — is the worst calibrated.** Extended-reasoning concentrates predictions in the high-confidence tail (104/300 = 35% of predictions in the 90–100% bin) where actual accuracy is 33.7%. The reasoning chain reinforces, rather than dampens, initial confidence.
5. **Cost ≠ calibration.** DeepSeek-V3.2 ($0.36/run, ECE 0.284) is cheaper *and* better-calibrated than GPT-5.2-XHigh ($30.32/run, ECE 0.395). For a signal-extraction pipeline, ~84× cost efficiency with better calibration is a clean win.

## Overconfidence at the tail — the structural finding

For each model, **expressed confidence exceeds realized accuracy**:
- Average confidence range across models: 74–82 %
- Average accuracy range: 64–69 %

The gap is largest at the high-confidence end. **OCR @ 90 %** (fraction of predictions made at >90% confidence that are wrong):

| Model | OCR @ 90% |
|---|---|
| DeepSeek-V3.2 | 14.7% |
| Claude Opus 4.5 | 20.8% |
| GPT-5.2-XHigh | 27.7% |
| Kimi-K2 | 31.1% |
| Qwen3-235B | 32.4% |

For a well-calibrated forecaster, OCR @ 90% should be < 10%. **All five models materially exceed this**; the worst (Qwen3) is off by 3.2×. Implication: trades sized on raw LLM confidence > 90% lose money in expectation absent recalibration.

This concentration creates a **secondary opportunity**: if other market participants are using uncalibrated LLM outputs as signal, the wrong-direction tail trades they push the market toward become contrarian opportunities. (Speculative; no direct evidence captured.)

## Practical pipeline — what to actually do

1. **Apply temporal filter.** No historical Polymarket evaluation is credible without it. Use the model's published training cutoff date as the lower bound on question close dates.
2. **Recalibrate confidence post-hoc.** Two cheap options:
   - **Temperature scaling:** fit a single scalar `T > 1` such that `softmax(logit / T)` minimizes NLL on a held-out calibration set. Reduces sharpness uniformly.
   - **Platt scaling:** fit a sigmoid `p_cal = σ(a · p_raw + b)` on a calibration set. More flexible.
   Both require a calibration set of (LLM-output, realized-outcome) pairs disjoint from your evaluation set.
3. **Avoid extended-reasoning modes for probability elicitation.** Per the GPT-5.2-XHigh result, longer chain-of-thought hurts calibration. Use base models for the probability output; if reasoning is needed, run it separately and feed it back as context.
4. **Apply domain conditioning.** Better calibration in Entertainment / Sports / Elections (high training-data coverage); worse in Crypto / Mentions / Economics. Cross-link to [[llm-forecasting-by-domain]] for the domain-tier ranking; both papers converge on Finance/Sports/Crypto as LLM-weak domains, but for *different reasons* — calibration here, accuracy there.
5. **Beat the base rate first.** Before sizing on LLM output, verify it has BSS > 0 on your filtered evaluation set. If it doesn't, you have no edge — the model is worse than `p = ȳ` everywhere.
6. **For sizing:** never use raw `p_llm` directly in `f* = (p·b − (1−p)) / b`. Substitute `p_cal` (post-recalibration), and apply a fractional-Kelly multiplier ≤ 0.25 to absorb residual calibration error.

## Open questions for Polymarket-specific work

- **Does the same model ranking hold on Polymarket?** KalshiBench is Kalshi-only. Resolution mechanics differ (CFTC-regulated objective settlement vs UMA Optimistic Oracle with dispute window — see [[uma-optimistic-oracle]]). The category mix differs slightly (Polymarket has more crypto and politics; Kalshi has more sports). The temporal-filter methodology ports cleanly; per-model rankings may not.
- **What's the calibration of the *market itself* on Polymarket?** Tetlock cites aggregate prediction-market Brier 0.12–0.18. A Polymarket-specific number, computed post-resolution with proper temporal filtering, would establish the bar any LLM signal must clear.
- **Is there an LLM ensemble that materially out-calibrates any single LLM?** PolySwarm ([[polyswarm-llm-trading-framework]]) claims swarm calibration > single-model but reports no numbers; this is an open empirical question.

## Source

- `raw/research/polymarket-market-trends-and-llm-edge/05-kalshibench-llm-calibration.md` — KalshiBench (arXiv 2512.16030); 300 Kalshi binary questions × 5 frontier LLMs; window Oct 1 – Nov 30, 2025; 13 categories (40% yes-rate); reliability diagrams; full metric definitions and equations; cost-per-prediction comparison. Note model-naming anachronism caveat above.

## Related

- [[llm-forecasting-by-domain]]
- [[mention-markets]]
- [[polyswarm-llm-trading-framework]]
- [[logit-jump-diffusion-kernel]]
- [[market-maker-handbook-prediction-markets]]
- [[polymarket-microstructure]]
- [[uma-optimistic-oracle]]
