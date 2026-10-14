# Restate

Berlin durable-execution runtime for AI agents and backend workflows, founded 2022 by Apache Flink creators. $20M Series A led by Singular (with Redpoint Ventures, Capital One Ventures), announced 2026-09-30; $27M total raised. Direct competitor to Temporal, the category leader. Replit Agent runs its durable orchestration on it (vendor-quoted).

**Tier:** startup. **Stub: single-source page (TNW, citing a company statement and TechCrunch); extend when independent practitioner reports, pricing, or benchmarks arrive.**

## What it does

Durable execution: records what a program has already done so it resumes correctly after a crash, restart, or dropped connection. Company argues agents make this harder because they run longer and call models, tools, APIs, and other agents (2026-09-30). CEO Stephan Ewen: the product "never was built for agents in the beginning, but it just happened to be a perfect match" (TechCrunch quote).

## Techniques under the hood

- Own distributed log as the base for execution, state, and communication; explicitly not built on a general-purpose database.
- No further architecture detail in source (SDKs, consistency model, latency): not specified in source.

## Deployment model

Managed service plus recently launched Bring Your Own Cloud (managed version run inside the customer's own cloud account). Self-hosting / open-source status: not specified in source.

## Customization hooks

Not specified in source.

## Running costs

Pricing not specified in source. Ewen says several six- and seven-figure customer contracts closed in recent months (vendor-quoted, 2026-09-30).

## Hard limits

Not specified in source: no throughput, latency, or failure-mode claims.

## Market reception (2026-09-30)

- **$20M Series A**: Singular lead; Redpoint Ventures and Capital One Ventures participating. Total funding $27M.
- **Founders:** Stephan Ewen (CEO; co-created Apache Flink, ex-CTO Data Artisans, which Alibaba bought in 2019 and renamed Ververica), Igal Shilman, Till Rohrmann, plus Ahmed Farghal (ex-Stripe, Meta) joining as fourth co-founder with the round.
- **Vendor-quoted adoption (unverified):** "hundreds of companies", including DOSS, Bilt Rewards, and Fortune 500 firms.
- **Replit:** moved Replit Agent onto Restate; new agent design uses over 10x the durable actions of the old one (Ewen blog post). Replit president Michele Catasta: it "now handles all durable orchestration at Replit".
- **Competitor context:** TechCrunch says Temporal leads the field. Per the same source Temporal raised a $550M Series E at $12.55B valuation in September 2026 (secondhand, not verified here). Restate is ~1/27th of Temporal's latest round *(editorial)*.
- **Use of funds:** go-to-market hires, more engineers, commercial hub in San Francisco.

## Hype-vs-reality delta

Adoption count, Replit scale, and contract sizes are all company-sourced. "Perfect match" for agents is retrofit positioning: the runtime predates the agent wave *(editorial)*. The credible part is the Flink pedigree and the Replit reference; the named-customer list is thin on production detail.

## Build-vs-buy signals

- Alternative to hand-rolled retry/checkpoint logic and to Temporal. Durable execution is becoming a distinct agent-infra layer below orchestration frameworks *(editorial)*.
- BYOC addresses data-residency objections that block managed-only runtimes.
- No pricing or limits data: not enough to recommend over Temporal. Re-check when a second source lands.

## Source

- `raw/research/weekly-2026-10-07/06-restate.md`

## Related

- [[ai-infrastructure-frontiers-2026]]
- [[ai-app-categories-2025]]
- [[aws-bedrock-agentcore-june-2026]]
- [[google-cloud-agentic-partner-fund-2026-04]]
