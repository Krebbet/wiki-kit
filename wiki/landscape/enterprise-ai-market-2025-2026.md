# Enterprise AI Market 2025–2026

Macro landscape of enterprise AI adoption across 2025 and 2026, consolidating survey data from Menlo Ventures (Dec 2025), a16z (May 2025 CIO baseline and Apr 2026 arms-race update), and Deloitte (2026 report). Covers market size, buy-vs-build patterns, deployment depth, multi-model behaviour, and spend trajectories. Claim dates are preserved since the domain shifts month-to-month; re-verify before quoting.

## Market size

- Enterprise generative AI spend reached **$37B in 2025**, up from $11.5B in 2024 (3.2x YoY) and $1.7B in 2023; now **~6% of the global SaaS market** and the fastest-growing software category in history (Menlo 2025-12-09).
- **Application layer $19B; infrastructure layer $18B** (Menlo 2025-12-09).
- **≥10 AI products now at $1B+ ARR; 50 at $100M+ ARR** (Menlo 2025-12-09).
- Scope caveat: Menlo's $37B excludes hyperscaler inference revenue (AWS / GCP / Azure), chip revenue (Nvidia), and embedded-AI features inside existing software (e.g. Intuit Assist). IDC / Gartner-style totals that include those will be larger — scope mismatch, not a contradiction *(synthesis)*. See [[open-questions-2026-04]] C6.

## Average enterprise LLM spend

- **~$4.5M two years ago → ~$7M now → ~$11.6M expected in 2026** (~65% YoY projected) (a16z 2026-04).
- Application spend pattern: **budgeted ~$3.9M, actually spent ~$6M** — consistent upside-surprise (a16z 2026-04).
- Innovation-budget share of LLM spend **collapsed from ~25% in 2024 to 7% in 2025** — gen AI has graduated to permanent lines in central IT and BU budgets (a16z 2025-05).

## Buy-vs-build — clear swing to buy

- **76% purchased vs 24% built** in 2025, reversed from 53/47 in 2024 (Menlo 2025-12-09).
- AI deal conversion: **47% of explored AI solutions reach production vs 25% for traditional SaaS** — roughly 2x (Menlo 2025-12-09).
- Over the 12 months preceding May 2025, enterprises swung clearly from build to buy; custom internal builds increasingly seen as hard to maintain and not a source of advantage (a16z 2025-05). Regulated verticals (healthcare) are the main exception.
- **"Death of the app layer" narrative not supported**: enterprises are migrating *toward* third-party applications, including in historically DIY-heavy categories like knowledge management and workflow automation (a16z 2026-04). See [[open-questions-2026-04]] C1.
- **Over 90% of customer-support respondents testing third-party apps**; one public fintech reversed an internal build-out after a market review (a16z 2025-05).

## Deployment depth

- **34%** of organizations use AI to "deeply transform" (new products / services or reinvented core processes); **30%** redesign key processes around AI; **37%** apply AI at surface level with little or no process change (Deloitte 2025-09 survey, published 2026).
- **66%** report productivity / efficiency gains; **only 20%** report revenue growth from AI, with **74%** saying revenue growth is a future goal — efficiency banked, top-line still aspirational (Deloitte 2025-09 survey).
- Only **16% of enterprise and 27% of startup deployments** qualify as "true agents" (LLM plans + executes + observes + adapts); the rest are fixed-sequence or routing workflows around a single model call (Menlo 2025-12-09).

## Internal vs customer-facing

- **59% internal / 41% customer-facing** use cases; both convert at similar rates (Menlo 2025-12-09).
- In May 2025, most spend was internal with tech-forward firms starting to pivot customer-facing (a16z 2025-05). Customer-facing is the next spend wave.

## Multi-model is default

- **81% of enterprises use three or more model families** in testing or production as of 2026-04 (up from 68% less than a year prior) (a16z 2026-04).
- **37% ran 5+ models in production** in May 2025, up from 29% a year earlier — driven by per-use-case routing, not just lock-in avoidance (a16z 2025-05).

## Gating factors (Deloitte's scale gates, 2026)

- **Governance** — enterprises where senior leadership actively shapes AI governance report significantly greater business value than those delegating to technical teams alone. Recommended: oversight embedded in performance rubrics; governance integrated into existing risk / oversight structures rather than run as parallel "shadow" functions (Deloitte 2025-09 survey).
- **Workforce redesign** — insufficient worker skills is the single biggest reported barrier to integrating AI into workflows. Most orgs focus on education; far fewer re-architect roles. New role categories named: AI operations managers, human-AI interaction specialists, quality stewards (Deloitte 2025-09 survey).
- **Data / infrastructure** — Deloitte argues legacy architectures cannot power real-time, autonomous AI; advocates a "living AI backbone" as prerequisite for agentic and physical AI.

## Deloitte's three-category AI framing (2026)

- **Generative AI** — broadest industry-impact category; specific sub-use-case rankings referenced in Deloitte's report but not inlined in the captured excerpt.
- **Agentic AI** — highest expected impact in customer support; other high-potential use cases: supply chain, R&D, knowledge management, cybersecurity.
- **Physical AI** — robotics, autonomous vehicles, drones; adoption "especially advanced" in manufacturing, logistics, defense.

## 2025 → 2026 time-series signals *(synthesis)*

Tracking claims that appear in both the May-2025 baseline and the 2026 update:

- **Multi-model adoption**: 37% ran 5+ (May 2025, a16z) → 81% run 3+ (Apr 2026, a16z). Lens shifted from "how many" to "three is table stakes."
- **Build-to-buy swing**: observed in 2025 (a16z) and confirmed year-end (Menlo 76/24) — 2026 arms-race data confirms continued migration.
- **Fine-tuning retreat**: "less necessary" in May 2025 (a16z); still declining in 2026 ("fading in enterprise"). Reversal would require RL-fine-tuning maturation. See [[open-questions-2026-04]] C2.
- **Direct-to-lab hosting**: ~40% in March 2024 → ~80% by 2026-04 (a16z) — meaningful reversal of the CSP-default procurement assumption. See [[open-questions-2026-04]] C3.

## Reader notes

- Deloitte numbers are from the captured HTML excerpt; the full PDF (not captured) has additional enumerations referenced in prose but not inlined.
- Menlo is an Anthropic investor (portfolio conflicts flagged in source: Anthropic, Wispr Flow, OpenRouter, Numeric, Open Hands, Meticulous, Graphite, Harness, Eve, Neon, Pinecone, Goodfire). a16z is an OpenAI investor; cross-checks against Yipit panel data.
- "95% of AI initiatives fail" (an MIT figure circulated in summer 2025) is rebutted by Menlo's demand-side data — see [[open-questions-2026-04]] C4.

## Source

- `raw/research/enterprise-ai-landscape-2026/01-a16z-arms-race-2026.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md`
- `raw/research/enterprise-ai-landscape-2026/03-deloitte-state-2026.md`
- `raw/research/enterprise-ai-landscape-2026/05-a16z-cio-2025.md`

## Related

- [[llm-api-enterprise-share]]
- [[ai-app-categories-2025]]
- [[ai-apps-layer-2026]]
- [[open-questions-2026-04]]
