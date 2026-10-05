# Agentic Compute Breaks Flat-Subscription Pricing (2026-04-21)

On **2026-04-21**, two independent events in a single 24-hour window exposed the same structural failure: **flat-subscription pricing for AI developer tools cannot absorb the compute variance introduced by agent-mode workflows.**

1. **GitHub paused new Pro, Pro+, and Student Copilot signups**; tightened Pro usage limits; removed Opus models from Pro (Opus 4.7 on Pro+ only). Stated rationale: "service reliability and a sustainable Copilot experience." Refund window through 2026-05-20.
2. **Anthropic quietly tested removing Claude Code from the $20 Pro tier** (initially ~2% of new signups). Documentation updated site-wide; practitioner backlash on HN (675 points, 635 comments) and Bluesky within hours; Anthropic reverted the change same day.

The events are independent and the primary source for this page (GitHub changelog) does not reference the Claude Code event. But they land 24 hours apart against the same structural pressure: production coding-agent workloads consuming compute at rates that break $20/month economics.

## What GitHub actually changed (2026-04-21)

- **Signup pause.** New Pro, Pro+, and Student signups halted. Copilot Free remains open. Existing users can still upgrade between plans.
- **Usage limits tightened.** Pro+ is now "more than 5X the limits of Pro" — exact Pro cap not disclosed. VS Code and Copilot CLI will warn users approaching limits; usage-progress tracking forthcoming.
- **Opus removed from Pro.** All Opus models gone from the Pro tier. Opus 4.7 retained only on Pro+. Opus 4.5 and 4.6 slated for removal from Pro+ (previously announced 2026-04-16).
- **Refund path.** Subscribers may cancel and receive pro-rata refund through **2026-05-20** via Settings → Billing and licensing → Licensing → Manage subscription.

## What the Claude Code event added

The Anthropic Claude Code / Pro-plan test was not captured in this batch (HN thread + Simon Willison's writeup are the public record). What's retrievable without a capture:

- Tested on ~2% of new Pro signups.
- Docs updated site-wide (the mistake that triggered mass backlash).
- Reverted within 24 hours.
- Signals that Anthropic is actively probing where to draw the line between consumer and agentic-use-case tiers — same pressure surface as GitHub, different product.

## Why this is structural

- The **>5x usage differential** between GitHub Copilot Pro and Pro+ implies agent sessions are driving a long-tail of extreme consumers. Flat pricing cannot absorb that variance — vendors are forced toward **tiered consumption or compute-cap models**.
- Opus exclusion from Pro is an **Anthropic-specific cost signal**: Opus 4.7 is expensive enough that GitHub cannot include it at a $10/month price point, confirming **frontier-model costs resist commodification** even at negotiated hyperscaler-API rates.
- **Pro+ is the durable revenue unit.** Pro commoditizes; Pro+ captures the users whose agent workflows generate real compute. The response is tiering, not price increase — consistent with "commodification pressure at Pro tier, premium layer preserved."
- Two independent companies hitting the same pressure surface in 24 hours is the hallmark of a structural shift, not a one-off vendor decision.

## Implications

### For developers

- Subscription-based access to frontier coding models is under durable downward pressure at the $10–20 tier. Opus and equivalent-class models are migrating to $100+ tiers.
- Copilot Free remains open; the free tier is increasingly a funnel, not a product.
- Agent-mode workflows (long parallelized sessions) are now the *default* user pattern, not a power-user edge case — evidenced by the fact that they're breaking plan economics at scale.

### For enterprises

- Seat-based licensing is structurally mispriced for agent-heavy teams. Expect vendors to move to hybrid (seat + consumption) or consumption-only enterprise pricing on 2026 timelines.
- Procurement should model per-developer compute consumption, not just license count. The variance across a development team will widen as agent adoption matures.
- **Build-vs-buy implication:** If internal teams are already paying $100+/developer/month for Pro+-equivalent access, self-hosted local-model options (e.g., Qwen3.6-27B-class models quantized for consumer GPUs) become economically competitive for specific workflows. Watch the open-weight coding-model tier (see [[../watchlist|watchlist]]).

### For frontier-model providers

- Anthropic's Opus and OpenAI's high-tier models have pricing power at the premium tier and nowhere else. This shifts revenue mix away from flat-fee reseller channels toward **direct API consumption** — which reinforces [[llm-api-enterprise-share]] enterprise direct-relationships patterns, not against them.

## Update 2026-05-03 — pressure compounds from above and below

Two follow-on signals tighten the structural read:

**Above the premium tier:** Cursor 3.2 (2026-04-24) ships **`/multitask` async parallel subagents** plus expanded worktrees and multi-root workspaces (see [[../startups/cursor|cursor]]). Default workflow is now N parallel subagents per developer-hour rather than one serialized agent. Compute consumption per developer rises commensurately. The Pro+/Enterprise pricing tier carries this load — expected upward pricing pressure on harness-class subscriptions through 2026.

**Below the subscription tier:** DeepSeek V4 Pro/Flash (2026-04-24) ships **MIT-licensed, 1M context, MoE** at **$0.14 / $0.28 per M tokens (Flash)** and **$1.74 / $3.48 (Pro)** — see [[../llms/deepseek|deepseek]]. Frontier-adjacent capability at **~1/30th the input cost** of GPT-5.5 / Opus 4.7. Combined with Qwen3.6-27B (Apache 2.0, single-GPU 16.8 GB Q4 quantization, 77.2% SWE-bench Verified — see [[../watchlist|watchlist]] 2026-04-23 entry), the open-weight tier has materialised into a **viable substitute for specific enterprise workloads** at <1/10th the per-token economics.

**Refined three-tier read:**

| Tier | Workload | Price point | Pressure direction |
|---|---|---|---|
| Open-weight self-hosted | Cost-sensitive coding, ETL agents, internal tooling | ~$0.14/M tokens or self-host fixed cost | **Compresses subscription floor** |
| Premium subscription / direct API | Mainstream agentic coding, integration-heavy workflows | $20–$200/dev/month + variable | **Stable but tiering up to Pro+ levels** |
| Hyperscaler-routed enterprise | Compliance / data-residency / multi-CSP procurement | Rebated long-term contracts | **Multi-CSP distribution is durable** (see [[openai-microsoft-restructure-2026-04]], [[google-anthropic-40b-2026-04]]) |

The pricing-economics question "**at what price point does coding-agent compute commoditize?**" is starting to get a layered answer: open-weight tier sets the floor, premium tier captures variance, and hyperscaler distribution captures enterprise procurement.

## Update 2026-05-10 — third pricing pattern: credit-based agent pricing

**OpenAI Workspace Agents** (launched 2026-04-22 in ChatGPT Enterprise; free trial through 2026-05-06; **credit-based pricing thereafter**) introduces a third pricing pattern alongside the existing two:

| Pattern | Vendor examples | Mechanism |
|---|---|---|
| **Flat tiered subscription** | GitHub Copilot Pro/Pro+, Anthropic Claude Pro/Max, Cursor Pro/Pro+ | Seat-based with usage caps; tiering captures variance |
| **Burst-API metering** | Direct API consumption (Anthropic, OpenAI, Google) | Per-token billing |
| **Credit-based agent pricing** *(NEW)* | OpenAI Workspace Agents (ChatGPT Enterprise) | Agent credits sit *on top of* seat cost; finance teams must model agent-credit consumption distinct from seat consumption |

**Microsoft Agent 365 GA (2026-05-01)** takes a different path — bundling **governance** (not agent execution) into M365 E7 SKU at no separate per-agent cost; standalone at USD 15/user/month per "individual who manages or sponsors agents." See [[../platforms/microsoft|microsoft]]. Distinct from the three execution-pricing patterns above; positions governance as a fourth seat-based monetisation layer.

**Refined four-tier read** (replaces the 2026-05-03 three-tier):

| Tier | Workload | Price point | Pressure direction |
|---|---|---|---|
| Open-weight self-hosted | Cost-sensitive coding, ETL agents, internal tooling | ~$0.14/M tokens or self-host fixed cost | **Compresses subscription floor** |
| Premium subscription / direct API | Mainstream agentic coding, integration-heavy workflows | $20–$200/dev/month + variable | **Stable, tiering up to Pro+** |
| **Credit-based agent execution** *(NEW)* | Enterprise non-coding agents (admin builder, vertical agents) | Seat cost + agent credit metering | **Decouples agent cost from seat cost** — finance-team-friendly |
| Hyperscaler-routed enterprise | Compliance / data-residency / multi-CSP procurement | Rebated long-term contracts | **Multi-CSP distribution durable** (see [[openai-microsoft-restructure-2026-04]], [[google-anthropic-40b-2026-04]]) |
| Governance bundle | Agent control-plane / observability | Bundled into existing seat SKU (M365 E7) or USD 15/seat | **Governance monetised separately from execution** |

The credit-pattern is particularly notable because it **separates agent unit-economics from seat unit-economics** — this is the budget primitive enterprise CFOs have been asking for. Watch whether Microsoft Copilot, Salesforce Agentforce, or Anthropic Managed Agents adopt similar credit metering through 2026-Q3.

## Update 2026-05 — infrastructure response: per-call micropayment rails (x402 / AgentCore Payments)

**Amazon Bedrock AgentCore Payments** (preview, 2026-05-17) is the infrastructure-side response to the flat-subscription-economics-breaking thesis this page documents. The mechanism: when an agent hits an HTTP 402 from a paid endpoint, AgentCore authenticates, executes a stablecoin micropayment via the x402 protocol (USDC on Base via Coinbase CDP wallet or Stripe Privy wallet), attaches payment proof, and returns the content — without interrupting the agent's reasoning loop. Session-scoped spending limits enforced at the platform layer (not the agent layer). Paid-endpoint discovery via the Coinbase x402 Bazaar MCP server.

**Where this fits the four-tier read.** x402-style micropayment settlement is not a fifth pricing tier — it is an enabling primitive for two existing tiers:

- *Credit-based agent execution* (tier 3): per-call stablecoin settlement is the same unit-economics logic as credit metering, pushed down to the transport layer and made machine-native. Agents can now pay for external services the same way they already pay for model tokens.
- *Hyperscaler-routed enterprise* (tier 4): AgentCore Payments sits inside AWS's managed agent platform; enterprise procurement of the rail happens through the same channel as the rest of AgentCore. Adds a spend-governance dimension (per-session limits) that enterprise CFOs will want.

The HTTP 402 / x402 primitive is notable independent of the AWS wrapper: a standardised machine-readable payment signal requires no bespoke billing integration per endpoint — any service that wants to monetise agent traffic can emit a 402. Google's AP2 protocol (Cloud Next '26, 2026-04-22) is a parallel/competing standard for the same class of agent-to-service commerce; x402 positions as the open-protocol alternative (x402 Foundation), with AgentCore as a managed implementation.

**Caveats.** Source is the AWS first-party launch blog (2026-05-17); no independent corroboration at preview. Pricing for the payment rail itself not disclosed. "First managed end-to-end payment capabilities for agents" claim (AWS) is contested by Google's AP2 timeline — the distinction between protocol and managed platform is load-bearing and not fully resolved. Fiat payments, broader commerce flows, and additional protocols (ACP, MPP) are roadmap items, not preview scope. See [[landscape/agentcore-payments-x402-2026-05]] for full detail.

## Update 2026-07-31 — OpenAI cuts GPT-5.6 pricing under budget pressure

First outright **price cut** (not a new tier or protocol) on this thread: OpenAI cut GPT-5.6 Luna 80% ($1→$0.20 / $6→$1.20 per 1M tokens) and Terra 20% ($2.50→$2 / $15→$12), leaving flagship Sol unchanged but adding a speed-only "Fast mode." AWS Bedrock mirrored the cut the same week. Trade press ties this directly to enterprise budget-blowout stories — Uber exhausted its 2026 AI budget by Q1 partly on Claude Code usage; Microsoft reportedly stopped Claude Code usage after its bill exceeded budget within months (see [[anthropic-subscription-split-2026-06]]). Reads as the pricing-war thread's first genuine margin-compression signal, distinct from the credit-metering and micropayment-rail patterns above — full detail at [[openai-gpt56-sol-2026-06]].

## Update 2026-08-09 — enterprise cost pullback: KPMG Global AI Pulse Q2 2026

Demand-side confirmation of the thesis this page has tracked since April: **49% of surveyed executives report scaling back AI agent deployments over cost**, per KPMG's Q2 2026 Global AI Pulse survey (2,145 senior leaders, 20 countries, $50M+ revenue orgs). Root cause cited is the same usage-based/token-metering unpredictability documented on this page's vendor-action thread (Copilot Pro pause, Claude Code Pro test, credit-metering, GPT-5.6 cuts) — except this is the first *survey-quantified* buyer-side reaction rather than a single vendor incident.

- **Spend holds even as deployments shrink.** Average AI spend across surveyed orgs held around $188M even as the number of active agent deployments fell — money isn't leaving the category, it's concentrating in fewer, better-understood use cases.
- **ROI is still rare.** Only ~7% of respondents report established, measurable ROI from agent deployments (per Forbes' coverage of the same report).
- **Cost-visibility gap.** Related coverage cites limited real-time cost visibility at scale, echoing the same "install a meter before you scale" dynamic Anthropic hit internally with its own (paused) Agent SDK credit-pool plan — see [[anthropic-subscription-split-2026-06]].
- **GitHub Copilot billing-shock anecdote** recurs in this reporting cycle as a concrete case study of the token-metering-unpredictability failure mode this page's April entries first documented.

**Hype-vs-reality:** this is the clearest data point yet that the "agents are being adopted everywhere" narrative and the "agents are unaffordable to run at scale" narrative are both true simultaneously — adoption breadth and deployment retention are decoupling. Any build-vs-buy advisory should now default to asking for the client's *realized* cost-per-task, not the vendor's list price, before recommending scale-up.

**Source:** `raw/research/weekly-2026-08-12/02-kpmg-ai-pulse-cost-pullback.md` (Forbes citing KPMG Global AI Pulse Q2 2026, 2026-08-09)

## Update 2026-09-09 — September 1 reset: Copilot credit cuts + a disputed Sonnet 5 rate rise

A practitioner cost-comparison analysis (arturmarkus.com) documents a repricing event across two of the three vendors this page tracks, with **seat prices unchanged** in all three cases — the mechanism is allowance/rate change, not a sticker-price move, continuing the pattern this page has documented since April.

- **GitHub Copilot** — the transitional AI-credit allowance (in effect June 1–September 1) reverted to permanent, lower levels: Business dropped **3,000 → 1,900 credits/user/month (-36.7%)**; Enterprise dropped **7,000 → 3,900 (-44.3%)**. A team that had normalized to 3,000 credits/month now pays ~$11/seat/month in overage at $0.01/credit — raising Business's effective per-seat cost from $19 to **~$30/month** (a 58% effective increase) with no listed price change. Tech Times (cited in-source) reports agentic bills jumping **10x–50x** for power users under this mechanism. 10-developer annual floor: **$2,280/year** at zero overage.
- **Cursor** — the only one of the three unaffected: Business seat price held at **$40/month** ($4,800/year floor for 10 developers), with request-based (not token/credit-metered) billing continuing to "absorb volatility" per the source's framing.
- **Claude Code / Anthropic API** — the source claims Sonnet 5's introductory API rate expired 2026-08-31, moving list price from $2/$10 to **$3/$15 per M tokens** (a 50% increase both legs), citing a secondary report (EnterpriseDNA). **This directly conflicts with [[../llms/anthropic-claude-family|anthropic-claude-family]]'s existing record that Anthropic made $2/$10 the *permanent* rate on 2026-08-11, explicitly cancelling a planned Sept 1 step-up to $3/$15.** Flagged as open conflict **C22** on [[../conflicts/open-questions-2026-04|open-questions-2026-04]] — not resolved here; treat Sonnet 5's current API rate as unconfirmed pending a primary Anthropic source.

**Read:** if the Sonnet 5 rate-rise claim holds up, all three vendors in this comparison would have used an allowance/expiry mechanism rather than an announced price change to raise effective cost on the same date (2026-09-01) — a repricing pattern this page should watch for as a recurring seasonal event, not a one-off. If the claim doesn't hold up (Anthropic's permanent-pricing commitment stands), then Copilot is the sole mover this cycle. Either way, the source's own recommendation — instrument per-developer usage and set model-routing defaults/alerts before assuming sticker price holds — is consistent with this page's long-running thesis that procurement should model realized cost-per-task, not list price.

**Source:** `raw/research/weekly-2026-09-09/05-september-pricing-reset.md` (arturmarkus.com, practitioner cost-comparison blog, 2026-09-01/09).

## Update 2026-09-16 — Sonnet 5 rate-rise claim resolved (against it); Copilot/Cursor read stands

C22 (the disputed Sonnet 5 $2/$10 → $3/$15 claim, immediately above) is now **resolved**: Anthropic's live pricing page, pulled today, still lists Sonnet 5 at $2/$10 and explicitly states the previously-scheduled 2026-09-01 step-up to $3/$15 "will not occur." Full evidence and sourcing trail in [[../conflicts/open-questions-2026-04|open-questions-2026-04]] C22 — in short, the EnterpriseDNA article behind the arturmarkus.com claim was published 2026-08-02, nine days before Anthropic's cancellation announcement, and was a forward warning about a scheduled increase, not a report that it happened; it was recirculated after the fact without being checked against the superseding announcement. A GitHub Community Discussion (#198015) surfaced as a possible independent corroboration of the rate-rise turned out, on direct inspection, to be unrelated — it's about GitHub Copilot's own credit-consumption model, not Anthropic API pricing.

**Revised read:** the "allowance/expiry mechanism raises effective cost across the board on 2026-09-01" pattern this page flagged does **not** extend to Anthropic — Copilot is confirmed as the sole mover this cycle (credit-allowance cut), with Cursor and Anthropic API pricing both holding. This narrows, but does not remove, this page's thesis: procurement should still model realized cost-per-task rather than list price, because at least one of three tracked vendors (Copilot) did use a non-sticker-price mechanism to raise effective cost this cycle — but it's no longer accurate to describe this as an industrywide pattern across all three vendors.

**Source:** `raw/research/weekly-2026-09-16/08-anthropic-pricing-current.md` (platform.claude.com, live pricing page, checked 2026-09-16); `raw/research/weekly-2026-09-16/10-github-copilot-credits-discussion.md` (GitHub Community Discussion #198015, checked 2026-09-16, found not relevant to Sonnet 5 pricing).

## Update 2026-09-22 — same-day price war: Claude Opus 5.5 ($4/$20) vs. GPT-6 Sol/Luna ($2/$10, $0.10/$0.50) — Sol lands exactly on Sonnet 5's price

Two frontier labs cut prices on the same calendar day, hours apart — the sharpest single data point yet for this page's mid-tier commoditization thesis.

**Anthropic — Claude Opus 5.5 (2026-09-22, launch post).** First release in the new "Claude 5.5" family, replacing Opus 5 as Anthropic's flagship. Pricing (per 1M tokens): input **$4** (down from Opus 5's $5, -20%), output **$20** (down from $25), cache reads **$0.20** (down from $0.50, -60%; Anthropic notes cache reads "make up the majority of agentic and coding work costs"), cache writes **$5** (down from $6.25). A "Fast mode" premium tier runs $8/$40 (up to 2.5x speed; Claude Code + Claude Platform only). Anthropic's combined claim — per-token cuts plus fewer tokens burned per task — is "40% less to run than Opus 5 on typical workloads." No promotional end-date is stated; treated here as the new standing rate, consistent with Anthropic's $2/$10 Sonnet 5 permanence stance (C22, resolved 2026-09-16, above).

**OpenAI — GPT-6 Sol and Luna (2026-09-22, hours after Anthropic, per VentureBeat).** Sol (mid "workhorse" tier, below flagship GPT-6 Astra) drops to **$2/$10** per 1M tokens — exactly **50% below GPT-5.6 Sol's $4/$20**, and exactly matching **Claude Sonnet 5's $2/$10** list price. Luna (low-cost/high-volume tier) drops to **$0.10/$0.50** — 50%/58.3% below GPT-5.6 Luna's $0.20/$1.20. OpenAI frames both cuts as **permanent, non-promotional pricing** (contrast: the same source notes Gemini 3.8 Flash's current rate is a time-limited introductory offer) and attributes them to "improvements to inference and caching," not a margin-eating discount. 90% discount on cached Sol input reads.

**The commoditization point.** GPT-6 Sol landing at exactly Sonnet 5's price is not incidental — OpenAI is pricing its mid-tier model directly at Anthropic's existing mid-tier rate, positioning Sol as a "direct swap-in competitor" at that price point (source's own framing). Combined with same-day timing on the Opus 5.5 / Sol-Luna announcements, this is the clearest evidence yet on this page that **mid-tier frontier pricing is converging to a single commodity number** ($2/$10), while the flagship tier still holds a premium (Opus 5.5 $4/$20, GPT-6 Astra Standard $10/$50).

**Cross-vendor snapshot** (condensed from the source's own 2026-09-22 comparison table, which additionally spans Meta Muse Spark, DeepSeek-V4.1-Flash/V4-Pro, MiniMax-M3, LongCat-2.0, Gemini 3.7/3.8 Flash, Grok 4.7, Kimi K3, Sakana Fugu Ultra, and the full Claude/OpenAI lineups — full table not reproduced here):

| Model | Input $/M | Output $/M | Tier |
|---|---|---|---|
| GPT-6 Luna | $0.10 | $0.50 | Low-cost / high-volume |
| Xiaomi MiMo-V2.6-Flash (MIT, open-weight) | $0.14 | $0.28 | Open-weight low-cost |
| Claude Sonnet 5 | $2.00 | $10.00 | Mid / "workhorse" |
| GPT-6 Sol | $2.00 | $10.00 | Mid / "workhorse" |
| Claude Opus 5.5 | $4.00 | $20.00 | Premium / flagship |
| GPT-6 Astra (Standard) | $10.00 | $50.00 | Flagship |
| Claude Fable 5 / Fable 5.1 | $10.00 | $50.00 | Most-capable |

Luna beats Sonnet 5 on raw rate by ~95% both directions, but against open-weight MiMo-V2.6-Flash, Luna is cheaper only on input (-29%) and actually **79% more expensive on output** — self-hosted open-weight remains a distinct cost structure, not dominated by the hyperscaler cuts this page has tracked since April (see the three/four-tier reads above).

**C22 reinforcement.** OpenAI's own source independently reconfirms Claude Sonnet 5 at $2/$10 as of 2026-09-22, using it as Sol's explicit price-parity reference point — a second independent confirmation (after Anthropic's own 2026-09-16 pricing page, above) that C22 resolved correctly in favor of permanent $2/$10. See [[../conflicts/open-questions-2026-04|open-questions-2026-04]] C22.

**Caveats.** Anthropic's benchmark claims (Walleye Capital, Gray Swan, Zapier, WANDR, GDPval-AA v2.1) are vendor-selected in a launch post, with Anthropic itself flagging that "benchmark margins have become a less reliable guide to real-world differences" at this capability level — no independent corroboration in this batch. OpenAI's Sol/Luna cost-per-task comparisons (AutomationBench, DeepSWE, OSWorld, Agents' Last Exam) are benchmarked against Opus 5, not the same-day Opus 5.5 — the source flags these numbers as already stale hours after publication. Treat both vendors' "X% cheaper per task" claims as unverified pending independent, same-harness benchmarking of Opus 5.5 vs. Sol/Luna.

**Source:** `raw/research/weekly-2026-09-23/01-01-anthropic-opus-5-5.md` (Anthropic launch post, 2026-09-22); `raw/research/weekly-2026-09-23/02-02-openai-gpt6-sol-luna.md` (VentureBeat, 2026-09-22).

## Conflict-flag cross-refs

- **C8** — "Coding agents = AGI for near-term enterprise tasks." GitHub's signup pause is *evidence agents are being used productively at scale by individual developers*, not just enterprise. This strengthens the C8 position A (coding agents are working). The counter (still fails on long-horizon / integration-heavy enterprise work) remains — the failure mode has shifted from "do agents work?" to "can we afford to run them?"
- **C13** — Practitioner revenue skepticism vs Menlo spend. Copilot spend at the subscription tier is real enough to stress infrastructure; commodification pressure exists at Pro tier; Pro+ is the durable revenue unit. Revenue-reality question shifts from "does the spend exist?" to "at what price point does it commoditize?"
- **C4** (2026-08-26) — McKinsey's 2026 State of AI survey (6% of enterprises are "AI high performers," ~90% of use cases stuck in pilot) is the Menlo-independent adoption check C4 was waiting on, and converges with Gartner's 88%-pilots-fail and KPMG's 49%-scaled-back figures already tracked on this page. Spend and adoption-breadth keep growing (this page's throughline) while realized ROI stays concentrated in a small minority of deployments — the two trends are not in tension, they're describing different layers of the same market. See [[../conflicts/open-questions-2026-04|open-questions-2026-04]] C4.
- **C22** (2026-09-09, opened; 2026-09-16, resolved; 2026-09-22, independently reinforced) — a practitioner source claimed Sonnet 5's API rate rose from $2/$10 to $3/$15 on 2026-09-01, contradicting Anthropic's own 2026-08-11 permanent-pricing announcement on [[../llms/anthropic-claude-family|anthropic-claude-family]]. **Resolved 2026-09-16 in favor of the permanent-$2/$10 position** — Anthropic's live pricing page confirms $2/$10 still stands and the step-up "will not occur"; the contrary claim traced to a stale pre-cancellation source. **Independently reconfirmed 2026-09-22** — OpenAI's GPT-6 Sol launch coverage cites Sonnet 5 at $2/$10 as Sol's price-parity reference point, a second, unrelated-vendor confirmation of the resolved position. See [[../conflicts/open-questions-2026-04|open-questions-2026-04]] C22.

## Source

- `raw/research/weekly-2026-04-23/04-github-copilot-pro-plan-2026-04.md` (GitHub Changelog, 2026-04-21)
- `raw/research/weekly-2026-05-03/04-cursor-3-2-multitask.md` (Futurum Research, 2026-04-29)
- `raw/research/weekly-2026-05-03/05-deepseek-v4.md` (Simon Willison, 2026-04-24)
- `raw/research/weekly-2026-05-10/05-openai-workspace-agents.md` (VentureBeat, 2026-04-22 — credit-pricing third pattern)
- `raw/research/weekly-2026-05-10/03-microsoft-agent-365-ga.md` (Microsoft Security Blog, 2026-05-01 — governance bundle pattern)
- `raw/research/weekly-2026-08-05/05-gpt56-pricing-cuts.md` (Forbes, 2026-07-31 — GPT-5.6 price cut)
- `raw/research/weekly-2026-08-26/04-04-mckinsey-state-of-ai-2026-08.md` (The Register, 2026-08-25 — McKinsey State of AI 2026 survey, cross-ref to C4)
- `raw/research/weekly-2026-09-09/05-september-pricing-reset.md` (arturmarkus.com, 2026-09-01/09 — Copilot credit cuts + disputed Sonnet 5 rate rise, cross-ref to C22)
- `raw/research/weekly-2026-09-16/08-anthropic-pricing-current.md` (platform.claude.com, live pricing page, checked 2026-09-16 — C22 resolution)
- `raw/research/weekly-2026-09-16/10-github-copilot-credits-discussion.md` (GitHub Community Discussion #198015, checked 2026-09-16 — checked as candidate C22 corroboration, found not relevant)
- `raw/research/weekly-2026-09-23/01-01-anthropic-opus-5-5.md` (Anthropic launch post, 2026-09-22 — Claude Opus 5.5 pricing)
- `raw/research/weekly-2026-09-23/02-02-openai-gpt6-sol-luna.md` (VentureBeat, 2026-09-22 — GPT-6 Sol/Luna pricing, cross-vendor table)

Adjacent (not captured in this batch):
- Simon Willison, "Claude Code confusion," 2026-04-22 — https://simonwillison.net/2026/Apr/22/claude-code-confusion/
- HN thread: Claude Code removed from Pro (2026-04-21, 675 pts)
- HN thread: Changes to GitHub Copilot plans for individuals (2026-04-21, 526 pts)

## Related

- [[ai-app-categories-2025]]
- [[llm-api-enterprise-share]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]] (Claude Opus 5.5, 2026-09-22)
- [[../llms/openai|openai]] (Workspace Agents credit pricing; GPT-6 Sol/Luna, 2026-09-22)
- [[../platforms/microsoft|microsoft]] (Agent 365 governance bundle)
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C8, C13, C22)
- [[../watchlist|watchlist]] (Qwen3.6-27B open-weight tier)
- [[../startups/cursor|cursor]] (3.2 multitask)
- [[../llms/deepseek|deepseek]]
- [[landscape/agentcore-payments-x402-2026-05]]
- [[landscape/openai-gpt56-sol-2026-06]] (2026-07-31 pricing cut)
