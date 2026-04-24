# LLM API Enterprise Share

Anthropic, OpenAI, Google Gemini, and open-source / Chinese models by enterprise share — spend, production adoption, use-case leadership, hosting model. Sources disagree on some numbers; we preserve each source's framing and date-stamp accordingly. Re-verify before quoting — the space shifts monthly.

## Spend share — Menlo's lens (what enterprises pay whom)

Menlo's enterprise LLM API **spend-share** snapshot (2025-12-09):

| Provider | 2023 | 2024 | 2025 |
|---|---|---|---|
| Anthropic | 12% | 24% | **40%** |
| OpenAI | 50% | — | **27%** |
| Google | 7% | — | **21%** |
| Top three combined | — | — | **88%** |
| Remaining (Meta Llama, Cohere, Mistral, long tail) | — | — | 12% |

**Coding-LLM share (2025-12-09):** Anthropic **54%**, OpenAI **21%** (OpenAI down from 42% six months earlier; Anthropic credit to Claude Code).

**Open-source share:** **11%** (down from 19% in 2024), attributed to Llama stagnation since Llama 4 (April 2025) (Menlo 2025-12-09).

**Chinese open-source models:** **1% of total enterprise LLM API usage** (~10% of the open-source slice), despite rising startup / indie adoption of Qwen, DeepSeek V3 / R1, Moonshot Kimi, MiniMax, Z.AI GLM on vLLM and OpenRouter. Cited: Airbnb uses Qwen heavily for user-facing AI; Cursor uses Qwen as the open-source base for its internal model (Menlo 2025-12-09, citing KrASIA + Al Jazeera, Nov 2025).

## Production adoption — a16z's lens (who's deployed)

a16z CIO survey 2026-04 production-deployment rates:

| Provider | CIOs with it in production | Incl. testing |
|---|---|---|
| OpenAI | **78%** | — |
| Anthropic | **44%** | >63% |
| Google Gemini | (gaining steadily) | — |

Cross-check: a16z's Yipit-panel data shows **~85% OpenAI** and **~55% Anthropic**, both trending with the survey (a16z 2026-04).

**Model-depth within each vendor:**
- **75% of Anthropic customers** run Sonnet 4.5 or Opus 4.5 in production — adoption concentrated at the frontier (a16z 2026-04).
- **46% of OpenAI customers** have GPT-5.2 or 5.2 Pro in production; a long tail remains on earlier model families because they "work well enough" (a16z 2026-04).

**Update 2026-04-22 (weekly brief):** Anthropic released **Opus 4.7** on 2026-04-16, replacing Opus 4.6 as the default Opus across Claude products. Pricing held flat at $5/$25 per M tokens. See [[../llms/anthropic-claude-family|anthropic-claude-family]] for the release detail. The "75% on Sonnet 4.5 / Opus 4.5" data point is now two model generations stale on the Opus side — watch for update on next enterprise-survey ingest.

**Update 2026-04-23 (weekly brief):** Two structural signals in the past 72 hours that revise the read on lab-hosting:

1. **Anthropic↔AWS $5B / $100B / 10-year / up-to-5-GW deal (2026-04-20).** Anthropic's inference and training substrate is now AWS Trainium-committed for a decade. Enterprises buying "direct from Anthropic API" run on AWS compute regardless of procurement channel — the lab-vs-CSP dichotomy in C3's 80% figure is weaker than the survey language implies. See [[../llms/anthropic-claude-family|anthropic-claude-family]] and [[../conflicts/open-questions-2026-04|C3]].
2. **Google Cloud Model Garden (GEAP, 2026-04-22)** — Anthropic Claude Opus/Sonnet/Haiku available through GCP *alongside* AWS Bedrock and Anthropic-direct. L'Oréal explicitly names "multi-LLM flexibility" as a buying criterion for GCP. Labs are distributing through all channels simultaneously — neither direct-to-lab nor CSP-mediated is exclusive. See [[google-cloud-next-2026-day2]].

Combined read: the "direct-to-labs" signal that C3 tracks is real at the *procurement surface* (who you sign the contract with) but obscures the underlying compute substrate, which is hyperscaler-locked by the lab-CSP structured deals. The useful question is no longer "direct or CSP?" but "which hyperscaler's iron are you renting, and via which billing surface?"

## Wallet-share shift (OpenAI → Anthropic / Gemini)

- Anthropic posted the largest share increase of any frontier lab since May 2025, **growing +25% in enterprise penetration** (a16z 2026-04).
- OpenAI wallet share: **~56%** and declining; Anthropic and Gemini gaining at OpenAI's expense (a16z 2026-04).
- All three still post strong **absolute** spend growth despite share reallocation — a growing pie (a16z 2026-04).

## Use-case leadership (2026-04)

- **OpenAI** — dominates horizontal use cases: general chatbots, enterprise knowledge management, customer support. Incumbency advantage from first adoption (a16z 2026-04).
- **Anthropic** — leads in software development and data analysis; token-heavy coding drives a large portion of the wallet-share gain (a16z 2026-04). Menlo claims "18 months atop LLM leaderboards for coding" since Claude Sonnet 3.5 (June 2024), but public leaderboard gaps are closer — treat the "18 months" figure as Menlo framing, not a leaderboard fact (Menlo 2025-12-09; see [[open-questions-2026-04]] C5).
- **Google Gemini** — broad across use cases but meaningfully lower in coding (a16z 2026-04).

## May 2025 baseline (for time-series comparison)

- OpenAI overall share leader; **67% of OpenAI users run non-frontier models in production** (vs 41% Google, 27% Anthropic) — structural depth in non-frontier SKUs (a16z 2025-05).
- **23% of enterprises had OpenAI o3 in production; only 3% had DeepSeek** despite heavy press — DeepSeek was a startup phenomenon, not enterprise (a16z 2025-05).
- Google rode GCP relationships and Gemini's price-to-performance (cited: Gemini 2.5 Flash ~$0.26/M tokens vs GPT-4.1 mini ~$0.70/M tokens) (a16z 2025-05).
- Anthropic concentrated in tech-forward firms — coding use-case lead translating into enterprise credibility (a16z 2025-05).
- Open-source (Llama, Mistral) skewed to larger enterprises with on-prem / data-security / fine-tuning needs (a16z 2025-05).

## Hosting-model shift (direct-to-lab up, CSP-default down)

- **~80% of enterprises comfortable hosting directly with the labs** (vs via CSPs like AWS Bedrock / Azure AI / Vertex) by 2026-04, up from ~40% in March 2024 (a16z 2026-04). Contradicts the "CSPs are the default procurement path" assumption — see [[open-questions-2026-04]] C3.
- In May 2025, direct-to-provider hosting was already shifting, with **Databricks** cited as a common third-party host where the enterprise's primary cloud didn't serve the target model (a16z 2025-05). See [[databricks]].

## Reasoning-model adoption

- **54% say reasoning models accelerated LLM adoption** in their org — cited reasons: faster time-to-value, less prompt engineering, better integration, higher trust (a16z 2026-04).
- In May 2025, enterprises were testing reasoning models heavily but few had them in production; OpenAI's o-series led early production adoption (a16z 2025-05).

## Pricing models

- Preferred enterprise AI pricing remains **usage-based** (a16z 2025-05).
- **Outcome-based pricing is hyped but CIOs reject it in practice** — concerns over unclear outcome definitions, unpredictable costs, and attribution (a16z 2025-05).
- Inference cost trend: **~10x / 12 months down** per a16z's "LLMflation" framing (a16z 2025-05). xAI Grok 3 mini and Gemini 2.5 Flash cited as price-to-performance leaders at the small / mid tier.

## Source

- `raw/research/enterprise-ai-landscape-2026/01-a16z-arms-race-2026.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md`
- `raw/research/enterprise-ai-landscape-2026/05-a16z-cio-2025.md`
- `raw/research/weekly-2026-04-23/01-google-cloud-next-2026-day2.md`
- `raw/research/weekly-2026-04-23/05-anthropic-aws-5b-100b-2026-04.md`

## Related

- [[enterprise-ai-market-2025-2026]]
- [[ai-app-categories-2025]]
- [[../platforms/databricks|databricks]]
- [[../platforms/snowflake|snowflake]]
- [[google-cloud-next-2026-day2]]
- [[google-cloud-agentic-partner-fund-2026-04]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[agentic-compute-pricing-2026-04]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]]
