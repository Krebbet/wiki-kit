# OpenAI GPT-5.6 (Sol / Terra / Luna) + Government Preview Window (2026-06-26)

OpenAI announced June 26, 2026 a three-model family (Sol, Terra, Luna) under the GPT-5.6 umbrella, with a notable constraint: the US government coordinated a ~30-day preview window before public launch, restricting initial access to ~20 government-approved partners. This is the first instance of a US government-imposed pre-release window on a commercial frontier AI family — a new norm that both Anthropic (Mythos 5, same week) and OpenAI are now operating under. Public launch expected July 2026.

## The three models

| Model | Positioning | Input/Output pricing (per 1M tokens) | Notes |
|---|---|---|---|
| **Sol** | Flagship; strongest reasoning; cybersecurity-hardened | $5 / $30 | max-reasoning + ultra/subagent modes; Cerebras at 750 tok/sec in July |
| **Terra** | Balanced performance/cost | $2.50 / $15 | Competes directly with Claude Sonnet 5 at the mid-tier |
| **Luna** | High-volume; fastest | $1 / $6 | Targets high-throughput agentic workloads |

**Context:** GPT-4.5 retired from ChatGPT on June 26 (simultaneous). GPT-5.2 retired June 12. The 5.6 family is a significant generational step from GPT-5.5.

## Government-gated rollout

The 30-day government-coordinated preview window is the operationalization of Trump's June 2, 2026 "Promoting Advanced AI Innovation and Security" EO. Both OpenAI (GPT-5.6) and Anthropic (Mythos 5) appear to be subject to the same window — suggesting it is a blanket policy for frontier model releases, not a targeted restriction. The legal mechanism (EAR, ITAR, or executive order) was not publicly specified as of June 26.

**Enterprise planning implication:** Frontier model releases now have a ~30-day lag between internal/partner availability and public/enterprise API access. Enterprises that depended on same-day API access to plan product releases will need to adjust their roadmapping cadence. Enterprises that participate in government-adjacent research or have cleared federal contracts may qualify for the preview tier.

## Sol: key capabilities

- **Cybersecurity hardening**: sol is the first GPT model described as purpose-built for security use cases — firmware analysis, vulnerability research, red-team support. Positioned ahead of Anthropic's Mythos 5 in cybersecurity benchmarks (per OpenAI partner disclosures; not independently verified at capture).
- **Ultra/subagent modes**: new invocation modes allowing Sol to spawn and coordinate sub-agents natively, without external orchestration scaffolding.
- **Max-reasoning mode**: token-compute budget allocation at the invocation level.
- **Cerebras inference**: Sol available on Cerebras hardware at up to 750 tokens/second in July — inference speed ~3-5x typical frontier model throughput. Targets real-time agentic workloads where latency is the bottleneck.

## Competitive context

Terra at $2.50/$15 per 1M tokens is a direct shot at Claude Sonnet 5 ($2/$10 introductory through Aug 31, 2026). The tiers match closely:
- Terra: $2.50/$15 — balanced, frontier-class
- Claude Sonnet 5: $2/$10 — near-Opus 4.8 performance (Anthropic-claimed)

Luna at $1/$6 competes with high-throughput tiers from Gemini 3.5 Flash and open-weight inference APIs (Together AI, DeepInfra).

## Pricing update (2026-07-31) — Luna -80%, Terra -20%, Sol gains Fast mode

Roughly five weeks after launch, OpenAI cut GPT-5.6 pricing sharply, framed by trade press as a response to enterprise AI-budget scrutiny rather than a capability upgrade:

| Model | Launch pricing (2026-06-26) | Updated pricing (2026-07-31) | Change |
|---|---|---|---|
| **Luna** | $1 / $6 | **$0.20 / $1.20** | -80% |
| **Terra** | $2.50 / $15 | **$2 / $12** | -20% |
| **Sol** | $5 / $30 | **$5 / $30 (unchanged)** | gains "Fast mode" — 2.5x faster, no stated price premium in this source, "no change to intelligence quality" |

Positioning also sharpened: Luna for "high-volume busywork... that doesn't require knowledge-intensive task fulfilment or strategy"; Terra for "everyday knowledge work" (consulting/project-management-style tasks).

**Market context cited (Forbes, 2026-07-31):**
- Uber "burned through its 2026 enterprise AI budget in a little over the first quarter" after Claude Code usage was maxed out by its 5,000 engineers.
- Microsoft reportedly stopped Claude Code usage when the bill exceeded its annual budget within months (corroborates the Claude Code cancellation signal already tracked in [[anthropic-subscription-split-2026-06]]).
- Harness "State of AI in FinOps 2026" survey (~700 finops/engineering leaders): ~29% of orgs attribute >25% of total cloud spend to AI; ~42% review AI costs only quarterly despite spend shifting materially within a week; 40%+ still track AI cost via spreadsheets.
- Open question raised in coverage: whether this cut cascades into broader ChatGPT plan pricing and forces Anthropic/Microsoft to match.

**AWS Bedrock mirrored the cut** the same week (Luna -80%, Terra -20%, effective ~2026-07-30, reported in AWS's Aug 3 weekly roundup) — independent confirmation this is a genuine list-price change, not a single-channel promotion.

**Hype-vs-reality:** framed explicitly as margin/cost-pressure response — competitive pressure from cheaper Chinese open-weight models (e.g. GLM-5.2) is cited as a driver — not a confidence-driven or capability-driven pricing move.

**Source:** `raw/research/weekly-2026-08-05/05-gpt56-pricing-cuts.md` (Forbes, Rachel Wells, 2026-07-31)

## What's not known at capture

- Benchmark numbers for Sol vs Claude Fable 5 / Gemini 3.1 Ultra: not independently verified; OpenAI partner disclosures are the only source for cybersecurity claims.
- Whether the Cerebras partnership extends beyond Sol: not confirmed.
- Whether enterprise API customers get preview access at a lower tier than government: not specified.
- Context window sizes for each model: not disclosed.

## Source

- URL: https://openai.com/index/previewing-gpt-5-6-sol/
- URL: https://venturebeat.com/technology/openai-unveils-gpt-5-6-sol-terra-and-luna-models-but-only-accessible-to-limited-preview-partners-for-now-per-us-gov
- URL: https://www.cnbc.com/2026/06/26/openai-limits-new-ai-models-to-trusted-partners-request-us-government.html
- Captured: 2026-07-01 (weekly-brief scan)

## Related

- [[llms/openai]] — full OpenAI model family + platform context
- [[landscape/anthropic-export-controls-2026-06]] — Anthropic/Mythos 5 simultaneous government preview window
- [[landscape/ai-regulatory-deadlines-2026]] — regulatory context for government AI review requirements
- [[landscape/chatgpt-market-share-2026-06]] — competitive position context
- [[landscape/openai-jalapeno-chip-2026-06]] — OpenAI custom silicon context (Jalapeño; Broadcom partnership)
- [[landscape/agentic-compute-pricing-2026-04]] — this pricing cut is the latest entry in the agentic-compute pricing-war thread
- [[landscape/anthropic-subscription-split-2026-06]] — Uber/Microsoft Claude Code budget-exhaustion data points corroborate the enterprise-AI-spend-strain narrative cited here
- [[landscape/agent-safety-incidents-2026-08]] — Sol's "cybersecurity-hardened" claim vs. AISI red-team finding, same week
