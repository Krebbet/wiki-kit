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

**Update 2026-05-03 (weekly brief):** the "single-CSP capture" reading is itself wrong — both top-2 frontier labs are now multi-CSP-distributed at material scale.

1. **Microsoft ↔ OpenAI partnership amended (2026-04-27).** Microsoft's IP license is now **non-exclusive** through 2032; Microsoft's outbound revenue share to OpenAI eliminated; Azure remains primary first-launch venue but **OpenAI can serve all products to customers across any cloud provider**. See [[openai-microsoft-restructure-2026-04]].
2. **GPT-5.5 + OpenAI frontier family on AWS Bedrock (2026-04-28)** — limited preview, GA "within weeks". OpenAI now lives on Azure (primary, first-launch) + AWS Bedrock + direct API.
3. **Google → Anthropic up-to-$40B + 5 GW Google Cloud (2026-04-24).** Adds GCP-substrate compute commit on top of Anthropic's existing AWS Trainium $100B / 5 GW deal. Anthropic now runs on **Trainium AND TPU AND general-purpose hyperscaler iron** at material scale. See [[google-anthropic-40b-2026-04]].

The 2026 procurement read settles: **multi-CSP lab distribution is the durable model**; lab-CSP coupling is real at the financing layer (equity-plus-compute structured deals) but **not exclusive at the distribution layer**. Enterprises can buy any frontier lab through any of the top-3 hyperscalers within 6 months. The "which hyperscaler's iron?" question framed in the 2026-04-23 update remains the right framing — but with the caveat that **the same lab now runs on multiple iron substrates across CSPs**, so the answer can be a procurement choice rather than a forced consequence.

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

## Anthropic enterprise wallet-share via OEM + hyperscaler-native distribution (2026-05)

Two signals from May 2026 show Anthropic gaining enterprise spend-share through platform-level embedding and hyperscaler billing integration — distribution channels that are structurally distinct from direct API consumption. No revenue figures were disclosed in either announcement.

**SAP Business AI Platform — Claude OEM-embedded in Joule (announced 2026-05-17, forward-looking)**

SAP and Anthropic announced at SAP Sapphire (2026-05-17) that Claude will serve as the primary reasoning and agentic engine inside SAP's Joule assistant across S/4HANA, SuccessFactors, and Ariba. The integration uses MCP as the connectivity bus to heterogeneous SAP and external systems, and embeds within SAP's existing governance/approval workflows rather than running in parallel to them.

Wallet-share read: for enterprises already on SAP's stack — 400,000+ customers, per SAP — Claude arrives bundled inside a platform they already pay for. The consumption pattern is OEM (Anthropic is a component vendor to SAP) rather than an enterprise buying Anthropic API directly. This inflates Anthropic's effective enterprise reach without necessarily showing up in direct-API spend-share metrics.

Caveats: source is a press release / announcement post (2026-05-17). All capability claims are forward-looking ("plans to expand," "will collaborate"). No GA date, no pricing, no named customer deployments, no benchmark data disclosed. SAP simultaneously states an "open ecosystem" (any model supported) — the "primary" designation creates switching friction but is not an exclusive lock.

Note: MCP is also the connectivity layer in this deployment; the OX Security RCE disclosure (2026-05-08, 11+ CVEs across 7,000+ MCP servers) applies directly to enterprise risk assessment of this integration path — see [[mcp-rce-supply-chain-2026-05]].

**Claude Platform on AWS — AWS-billed distribution path (GA 2026-05-11)**

Anthropic's full-feature Claude Platform API went GA on AWS on 2026-05-11. It delivers complete Anthropic feature parity (Managed Agents, Skills, MCP connector, Files API, code execution, prompt caching, citations, batch) under AWS IAM authentication, CloudTrail audit logging, and AWS consolidated billing. Critically, spend retires against the enterprise's existing AWS commitments — same mechanism that GPT-5.5-on-Bedrock uses (limited preview as of 2026-04-28, per [[openai-microsoft-restructure-2026-04]]). Both are competing for the same AWS-committed enterprise budget, within weeks of each other.

The path is distinct from Amazon Bedrock: Anthropic operates the service; data is processed outside the AWS boundary (Anthropic's infrastructure, not AWS's). This matters for regulated workloads (HIPAA, FedRAMP, EU data sovereignty) — those require Bedrock, not this path. The AWS billing integration is a procurement-friction reducer, not a data-residency guarantee.

Same-day feature parity with the native Claude API is an explicit commitment (vs. Bedrock's historically slower rollout) — a meaningful differentiator for teams chasing bleeding-edge agent capabilities.

Wallet-share read: the AWS commitment-retirement mechanism lowers procurement friction and creates billing-surface retention (switching vendors triggers procurement overhead once commitments are being retired). Combined with the existing Bedrock presence and Google Cloud Model Garden availability (2026-04-22), Anthropic is now distributed across all three major hyperscaler billing surfaces simultaneously — a structural multi-CSP distribution position that mirrors what OpenAI achieved via the amended Microsoft deal (2026-04-27). See also [[google-anthropic-40b-2026-04]] for the Google Cloud compute substrate context.

**Combined read (2026-05):** Anthropic is gaining enterprise wallet-share through two distinct channels that do not show up cleanly in direct-API spend metrics: (a) OEM embeds inside dominant enterprise platforms (SAP, and previously Finance Agents verticals), where consumption is platform-mediated; and (b) hyperscaler-billed paths (AWS consolidated billing, Bedrock, GCP Model Garden) that let enterprises buy Anthropic within existing cloud commitments. The "direct API vs. CSP" dichotomy is increasingly unhelpful — Anthropic is on all of them.

## Source

- `raw/research/enterprise-ai-landscape-2026/01-a16z-arms-race-2026.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md`
- `raw/research/enterprise-ai-landscape-2026/05-a16z-cio-2025.md`
- `raw/research/weekly-2026-04-23/01-google-cloud-next-2026-day2.md`
- `raw/research/weekly-2026-04-23/05-anthropic-aws-5b-100b-2026-04.md`
- `raw/research/weekly-2026-05-03/01-openai-microsoft-restructure.md`
- `raw/research/weekly-2026-05-03/02-google-anthropic-40b.md`
- `raw/research/weekly-2026-05-17/.ingest/02-sap-anthropic-business-ai-2026-05.summary.md`
- `raw/research/weekly-2026-05-17/.ingest/03-claude-platform-on-aws-2026-05.summary.md`

## Related

- [[enterprise-ai-market-2025-2026]]
- [[ai-app-categories-2025]]
- [[../platforms/databricks|databricks]]
- [[../platforms/snowflake|snowflake]]
- [[google-cloud-next-2026-day2]]
- [[google-cloud-agentic-partner-fund-2026-04]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[agentic-compute-pricing-2026-04]]
- [[openai-microsoft-restructure-2026-04]]
- [[google-anthropic-40b-2026-04]]
- [[../llms/deepseek|deepseek]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]]
- [[anthropic-enterprise-distribution-2026-05]]
- [[mcp-rce-supply-chain-2026-05]]
