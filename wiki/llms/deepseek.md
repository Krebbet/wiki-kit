# DeepSeek Model Family

Running page for DeepSeek (Chinese AI lab, MIT-licensed open weights) — release timeline, capability / pricing, and enterprise-distribution status. Profiled here from **DeepSeek V4 preview (2026-04-24)** onwards. For broader open-weight enterprise share see [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]] (Menlo's read: ~1% of total enterprise LLM API usage at end-2025; Cursor + Airbnb among named users of DeepSeek/Qwen-class).

## Release timeline

| Date | Model | Notes |
|---|---|---|
| 2025-03-24 | DeepSeek V3-0324 | Per Simon Willison thread — earliest of recent V3 series. |
| 2025-08-22 | DeepSeek V3.1 | Continued V3 lineage. |
| 2025-12-01 | DeepSeek V3.2 + V3.2 Speciale | Last release before V4. V3.2 is 685B total params. |
| **2026-04-24** | **DeepSeek V4-Pro + V4-Flash (preview)** | First V4-series release. MIT license, 1M-token context, MoE. See below. |

## DeepSeek V4 Preview (2026-04-24)

### Architecture

| | DeepSeek-V4-Pro | DeepSeek-V4-Flash |
|---|---|---|
| Total params | 1.6 T | 284 B |
| Active params | 49 B | 13 B |
| Architecture | Mixture of Experts | Mixture of Experts |
| Context | 1 M tokens | 1 M tokens |
| License | MIT | MIT |
| HF size | 865 GB | 160 GB |
| Hosted via | OpenRouter (and DeepSeek's own API) | OpenRouter |

V4-Pro is now **the largest open-weights model**: larger than Kimi K2.6 (1.1 T), GLM-5.1 (754 B), more than 2× DeepSeek V3.2 (685 B).

### Pricing — the headline

DeepSeek's posted pricing (api-docs.deepseek.com/quick_start/pricing):

| Model | Input ($/M tokens) | Output ($/M tokens) |
|---|---|---|
| **V4-Flash** | $0.14 | $0.28 |
| **V4-Pro** | $1.74 | $3.48 |

Compare frontier (Anthropic, OpenAI, Gemini):

- Claude **Opus 4.7** — $5 / $25 per M tokens (see [[anthropic-claude-family]])
- Claude **Sonnet 4.6** — ~$3 / $15
- Approximate frontier-model parity range — DeepSeek V4-Pro is **~1/3 of Sonnet's input price and ~1/7 of Opus** at the output side.

Simon Willison's framing: *"almost on the frontier, a fraction of the price."*

### Capability (early-cycle, vendor / enthusiast benchmarks)

- Pelican-on-bicycle SVG (Willison's running informal eval) — both V4-Pro and V4-Flash credible; Pro materially better than V3.2 (Dec 2025). No formal SWE-bench / GDPval-AA / BigCodeBench numbers yet.
- 1M context — competitive with Gemini 3.x family at the very long-context tier; not comparable on the same evals as Gemini 3.1 Ultra (multimodal native).
- Open weights mean **fine-tunability and self-hosting** are first-class — the differentiator vs hosted-only frontier APIs.

## Why this matters

### Open-weight cost-collapse continues

Stacking the past two weeks:

- 2026-04-22: **Qwen3.6-27B** (Apache 2.0) — beats Alibaba's own 397B MoE on SWE-bench Verified (77.2%); runs Q4 in 16.8 GB on a single consumer GPU. See [[../watchlist|watchlist]] (2026-04-23 entry).
- 2026-04-24: **DeepSeek V4-Flash** — 284B MoE / 13B active; 160 GB on HF; ~1/30th the input cost of GPT-5.5 / Opus 4.7.
- 2026-04-24: **DeepSeek V4-Pro** — 1.6T MoE / 49B active; **largest open-weights model ever** at MIT license.

The 2026-Q2 picture: **frontier-adjacent capability is being released at progressively-cheaper open-weight tiers every week.** This compounds with [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] — the $20 / $100+ subscription tiers come under pressure both from above (agentic workloads break flat-fee economics) *and* from below (open-weight self-hosting becomes economically competitive for specific workloads).

### Enterprise distribution remains thin

Per [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]:

- Open-source share of enterprise LLM API spend: **11%** in 2025 (down from 19% in 2024) — Menlo 2025-12-09.
- Chinese open-source models: **~1% of total enterprise LLM API usage** (~10% of the open-source slice) — Menlo 2025-12-09.
- Cited heavy users: **Airbnb** (Qwen for user-facing AI), **Cursor** (Qwen as base for internal model).

DeepSeek V4 hasn't shifted this yet — it's <2 weeks old. **Watch:** Menlo's next enterprise survey for whether V4-class releases meaningfully move the open-weight enterprise share, or whether the 11% / 1% split holds.

### Geopolitical / supply-chain caveat

Chinese-origin model weights deployed in U.S. enterprises remain a **CIO-level risk question**: data residency, IP-flow scrutiny, evolving U.S. export-controls reciprocity. Per a16z 2025-05, even with strong leaderboard performance, **enterprise DeepSeek production adoption was 3% vs OpenAI o3 at 23%** at that snapshot. Pricing alone hasn't been enough to flip that gap; legal / compliance friction is the binding constraint.

## Build-vs-buy implications

- **For cost-sensitive coding workloads where leaderboard difference is small** (form-fill agents, basic refactors, ETL transforms, internal tooling): V4-Flash at $0.14 / $0.28 is a serious challenger to the $3+/$15+ tier. Run benchmarks on the actual workload, not on aggregate leaderboards.
- **For self-hosted / on-prem / sovereignty deployments** where Chinese-origin weights are acceptable: V4-Pro extends the upper bound of "what an enterprise can run on its own iron" by a large margin. Pair with on-device / regional-inference vendors (see [[../startups/runanywhere|runanywhere]] cluster, BVP edge-inference picks in [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]] §4).
- **For client advisory:** continue to flag China-origin compliance friction as the binding go/no-go gate for U.S. and EU enterprise deployments. The **technical** case keeps strengthening; the **legal / procurement** case has barely moved.

## Hype-vs-reality delta

- "Almost on the frontier" — Simon Willison's framing; not yet supported by independent SWE-bench / GDPval-AA / BFCL leaderboard runs. Wait 2–6 weeks for those.
- Pricing is **list-API price**; serving costs at scale (especially for V4-Pro at 49B active) require GPU clusters that approach hyperscaler retail pricing. The cost-advantage compresses materially at full self-host scale.
- "Largest open-weights model" is a clean claim, but **largest doesn't mean best** — utility depends on the workload, not the parameter count.

## Source

- `raw/research/weekly-2026-05-03/05-deepseek-v4.md` (Simon Willison, 2026-04-24)

Adjacent (not captured in this batch):
- DeepSeek API pricing — https://api-docs.deepseek.com/quick_start/pricing
- HuggingFace model cards — DeepSeek-V4-Pro, DeepSeek-V4-Flash

## Related

- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]
- [[anthropic-claude-family]]
- [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]]
- [[../startups/runanywhere|runanywhere]]
- [[../watchlist|watchlist]]
