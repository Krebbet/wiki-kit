# Willison: Anthropic and OpenAI Have Found Product-Market Fit

Simon Willison's May 27 2026 blog post argues that the convergence of two developments — enterprise pricing shifted from flat seats to API-rate-card billing, and coding agents burning vastly more tokens than chat — marks a genuine product-market fit inflection for Anthropic and OpenAI. He identifies November 2025 as the model-quality inflection point and April 2026 as the revenue inflection point, and reads high-profile "AI cost alarm" stories (Uber, Microsoft) not as failure signals but as confirmation that customers are crossing a price threshold and saying yes anyway.

## Source

Simon Willison, "I think Anthropic and OpenAI have found product-market fit," simonwillison.net, May 27 2026.
URL: https://simonwillison.net/2026/May/27/product-market-fit/

This is the third post in a natural Willison trilogy: [[case-studies/willison-cognitive-cost]] (practitioner cost experience) → [[case-studies/willison-vibe-agentic-convergence]] (quality and trust signals, November 2025 inflection) → this post (revenue and pricing implications, April 2026 inflection).

## The Enterprise Pricing Shift

Prior to late 2025, Anthropic's Enterprise plan was sold as flat seats with "enough usage for a typical workday." At some point Anthropic changed this to **$20/seat/month plus API-rate-card pricing for usage**. Anthropic told The Information the change occurred in November 2025; the story broke publicly on April 14 2026. Existing customers are encountering the new terms as contracts renew. (collect-but-confirm: Anthropic spokesperson via The Information, April 14 2026.)

OpenAI made a structurally equivalent move for Codex:

- **April 2 2026** — pricing shifted to API token alignment for new and existing Plus, Pro, ChatGPT Business, and new ChatGPT Enterprise plans.
- **April 23 2026** — extended to all existing ChatGPT Enterprise plans including Edu, Health, Gov, and ChatGPT for Teachers.

Source: OpenAI Codex rate card help article, confirmed via Internet Archive snapshot.

The net result: as of April 2026 the enterprise cost for both OpenAI Codex and Anthropic Claude Code/Cowork equals the listed public API price. The per-seat consumer subscription discount is no longer extended to enterprise buyers.

Both labs simultaneously released new frontier models at higher per-token prices: GPT-5.5 (April 23) at 2× the API price of GPT-5.4 (collect-but-confirm: stated without citation), and Opus 4.7 (April 16) at approximately 1.4× the effective cost of Opus 4.6 when accounting for the new tokenizer (Willison's own April 20 token-count analysis).

## Why Coding Agents Drive This

The pricing shift is only consequential because of what coding agents actually consume. Willison's own 30-day API-equivalent spend, estimated using the `ccusage` tool:

- Claude Code: **$1,199.79** (personal estimate, self-reported, tool-assisted)
- OpenAI Codex: **$980.37** (personal estimate, self-reported, tool-assisted)
- Total: **$2,180.16** in API-equivalent tokens against **$200** in actual consumer subscription spend

Willison describes himself as a moderately heavy user, not running agents around the clock. Enterprise customers running agents continuously across engineering teams face this delta at scale — and under the new pricing structure, they pay it.

Willison's argument: coding agents burn vastly more tokens than chat interactions, and they are daily drivers for extremely well-compensated professionals. A $100–200/month/user subscription model cannot fund the labs' infrastructure needs; $200–1,000+/month/user in API consumption can.

## Product-Market Fit Evidence

### Revenue signals

Anthropic is rumored to approach **$10.9 billion in Q2 2026 revenue**, potentially its first profitable quarter. (collect-but-confirm: WSJ, unnamed sources.)

As of August 2025, Cursor and GitHub Copilot together accounted for an estimated **$1.2 billion** of Anthropic's then-~$4 billion revenue. (collect-but-confirm: VentureBeat, "sources familiar with the matter.") The pivot toward direct Claude Code Enterprise is framed by Willison as cutting out those API resellers — Claude Code directly competes with Cursor and Copilot, which is why Cursor is investing in its own models.

### Hiring posture

Willison scraped the public job boards using Claude Code + Datasette Cloud / Datasette Agent:

- OpenAI: 703 open jobs; 229 (32.6%) categorized as enterprise sales/support (account executives, GTM, Forward Deployed Engineers). (Willison's own scrape, approximate as of post date.)
- Anthropic: 390 open jobs; 105 (26.9%) enterprise-facing. (Same methodology.)

He notes the irony that companies selling AI automation are building large human-intensive enterprise sales forces.

### Inference spend

The SpaceX S-1 SEC filing (May 2026) disclosed that Anthropic agreed to pay **$1.25 billion/month** through May 2029 for compute capacity across Colossus and Colossus II. Anthropic framed the deal publicly as enabling higher usage limits for Claude Code and the Claude API — heavily implying the capacity is for inference, not training. (Primary source: SpaceX S-1, SEC EDGAR.)

Anthropic already holds compute from other vendors; willingness to commit $1.25B/month to a single additional vendor indicates inference demand has scaled to an order of magnitude that makes this necessary.

## The "Failure" Stories Reinterpreted

Willison explicitly rejects the AI-cost-alarm reading of two widely circulated stories.

**Uber**: Uber CTO Praveen Neppalli Naga reported Uber had "maxed out its full year AI budget just a few months into 2026," primarily due to Claude Code. Willison's reading: Claude Code only became reliably useful in November 2025; a budget set in 2025 could not have predicted 2026 enterprise adoption levels. Uber COO Andrew Macdonald separately noted 25% of code commits via Claude Code last quarter while acknowledging difficulty tracing the productivity gain to shipped consumer features — headlines rendered this as failure; Willison reads it as growing pains of genuine adoption.

**Microsoft**: Microsoft cancelled Claude Code licenses, ostensibly to enforce internal Copilot use and for financial reasons tied to the June 30 fiscal year-end.

Willison's framing: the best pricing signal is "customer sucks air through their teeth and then says yes." Budget overruns and mid-year cuts followed by continued enterprise deals look exactly like that effect, not like product rejection.

## The April 2026 Inflection

Willison names two inflection points:

- **November 2025** — model quality inflection: GPT-5.1 and Opus 4.5, combined with their coding agent harnesses, became genuinely useful for sustained work. Six months of adoption followed.
- **April 2026** — revenue inflection: enterprise pricing locked to API rates, new higher-priced frontier models released, and the financial consequences of November's adoption are landing on company balance sheets.

He notes that hard confirmation will come from the S-1 documents for upcoming Anthropic and OpenAI IPOs, which will provide audited figures.

## Limitations and Reliability Notes

- Willison's personal usage estimates ($1,199.79 / $980.37) are self-reported and tool-assisted (ccusage); they are specific and plausible but not independently verifiable.
- Anthropic's November 2025 pricing change date comes from an Anthropic spokesperson via The Information, not from a public primary document. (collect-but-confirm.)
- Revenue figures ($10.9B Q2, $1.2B Cursor+Copilot share) are from unnamed sources via WSJ and VentureBeat respectively. (collect-but-confirm.)
- OpenAI and Anthropic job counts are from Willison's own scrape at post date and are approximate.
- GPT-5.5 pricing at 2× GPT-5.4 is stated without citation.
- The post does not attempt to disaggregate how much of the revenue growth is coding agents vs. other product lines.

## Related

[[case-studies/willison-cognitive-cost]] — first in Willison trilogy; documents the practitioner cost experience (parallel agents, budget exhaustion) that creates the token-burn profile this post argues drives PMF revenue

[[case-studies/willison-vibe-agentic-convergence]] — second in Willison trilogy; covers quality and trust signals and names November 2025 as the model-quality inflection; this post extends that with the April 2026 revenue inflection

[[anthropic-internal-study]] — Anthropic's 132-engineer internal study corroborating heavy agent usage that drives the token volumes Willison points at

[[deployments/anthropic-finance-agents]] — Anthropic's direct-enterprise Managed Agents vertical; represents the product strategy of cutting out API resellers that Willison describes

[[deployments/cognition-cloud-agents]] — enterprise agent deployment at scale (Itaú); illustrates the spending dynamic described here

[[deployments/openai-symphony]] — OpenAI's zero-human-code project; a direct data point on enterprise agent token burn

[[case-studies/cursor-agent-harness]] — Cursor named as major Anthropic API customer now undercut by Claude Code direct; explains why Cursor is investing in proprietary models

[[security/adr-uber-mcp-detection]] — Uber's security tooling for Claude Code; Uber is the central anecdote in the "failure story reinterpreted" section
