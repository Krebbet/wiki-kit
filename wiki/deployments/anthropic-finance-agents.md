# Anthropic Agents for Financial Services (2026-05-05)

Anthropic released ten named finance-domain agent templates packaged as a three-component reference architecture (skills + connectors + subagents), shipping as plugins for Claude Cowork / Claude Code and as cookbooks for Claude Managed Agents. The announcement also introduces a taxonomic distinction between connectors (governed data access) and MCP apps (provider tools embedded in Claude), expands the financial-services connector ecosystem to eight new partners, and adds Claude add-ins for Microsoft 365 applications.

## Source

- Anthropic News, "Agents for financial services," 2026-05-05 — `raw/research/weekly-2026-05-08/04-anthropic-finance-agents.md`. Vendor announcement post; all capability claims, benchmark figures, and ecosystem characterisations are vendor-stated unless otherwise noted.

## The 10 agent templates

Templates are grouped by workflow domain. Each ships as a plugin (Claude Cowork / Claude Code) and as a Managed Agent cookbook.

**Research and client coverage**

| Template | Function |
|---|---|
| Pitch builder | Creates target lists, runs comparables, drafts pitchbooks for client meetings |
| Meeting preparer | Assembles client and counterparty briefs ahead of calls |
| Earnings reviewer | Reads transcripts and filings, updates models, flags thesis-relevant changes |
| Model builder | Creates and maintains financial models from filings, data feeds, and analyst inputs |
| Market researcher | Tracks sector and issuer developments; synthesises news, filings, and broker research |

**Finance and operations**

| Template | Function |
|---|---|
| Valuation reviewer | Checks valuations against comparables, methodology, and firm review standards |
| General ledger reconciler | Reconciles GL accounts and runs NAV calculations against books of record |
| Month-end closer | Runs the close checklist, prepares journal entries, produces close reports |
| Statement auditor | Reviews financial statements for consistency, completeness, and audit-readiness |
| KYC screener | Assembles entity files, reviews source documents, packages escalations for compliance |

Source for template descriptions: vendor-stated.

## Architecture: skills + connectors + subagents

Each template is a reference architecture that packages three components (vendor-stated):

- **Skills** — instructions and domain knowledge for the task.
- **Connectors** — governed, real-time access to the data the task runs on (see Connectors vs MCP apps below).
- **Subagents** — additional Claude models called by the main agent for specific sub-tasks. Examples given by the source: comparables selection, methodology checks.

The main-agent + specialist-subagent pattern is a concrete vertical-deployment instance of the manager-agent topology; see [[patterns/topology-taxonomy]].

The three-component decomposition (skills / connectors / subagents) maps directly onto the externalization vocabulary in [[patterns/externalization-survey]] (skills externalization, context/protocol externalization, multi-agent harness), grounding that survey's taxonomy in a named vendor product.

## Connectors vs MCP apps

The announcement draws an explicit two-tier distinction:

> "Connectors give Claude governed, real-time access to a provider's data, and MCP apps go a step further by embedding the provider's own tools directly inside Claude."

- **Connectors** — data-access integrations providing governed, real-time reads. Examples: FactSet, S&P Capital IQ, MSCI, PitchBook, Morningstar, Chronograph, LSEG, Daloopa (existing); Dun & Bradstreet, Fiscal AI, Financial Modeling Prep, Guidepoint, IBISWorld, SS&C Intralinks, Third Bridge, Verisk (new).
- **MCP apps** — integration tier that embeds the provider's own tools as interactive capabilities within Claude. **Moody's** is the sole MCP-app example: surfaces proprietary credit ratings and data on 600M+ public and private companies for compliance, credit analysis, and business development.

This is a new taxonomic tier not present in [[deployments/mcp-infrastructure]], which treats MCP primarily as a protocol/infrastructure layer without distinguishing governed-data-read connectors from provider-tool-embedding MCP apps. The Moody's example is the anchor for this distinction.

## Managed Agents capabilities cited

When deployed as a Claude Managed Agent (public beta on the Claude Platform), templates include the following harness features (all vendor-stated):

- **Long-running sessions** — capable of spanning multi-hour deal close processes.
- **Per-tool permissions** — fine-grained access controls per tool call.
- **Managed credential vaults** — secrets managed by the platform rather than the client.
- **Audit log in Claude Console** — every tool call and decision is inspectable by compliance and engineering teams.

These building blocks parallel the harness-engineering pattern; see [[patterns/effective-harnesses]]. This is Anthropic's productized harness for vertical domains, standing in as the counterpart to the hand-engineered harnesses described in that page.

## Microsoft 365 add-ins

Claude add-ins for Excel, PowerPoint, and Word are generally available; Outlook is announced as coming soon (vendor-stated as of 2026-05-05). Context carries automatically across all four applications without re-explanation — an analyst who builds a model in Excel does not need to re-explain it when work moves to PowerPoint.

**Dispatch** (Claude Cowork feature): users can assign Claude tasks by text or voice from anywhere; Claude works on local files while the analyst is away, with results ready for review on return (vendor-stated).

This M365 add-in layer is the agent-facing complement to the cross-cloud governance plane described in [[deployments/microsoft-agent-365]].

## Vendor-stated benchmark numbers

- Claude Opus 4.7 leads the Vals AI Finance Agent benchmark at **64.37%** — vendor-stated; benchmark is a third-party (Vals AI) measure, so treat as collect-but-confirm rather than authoritative.

## Enterprise adopters cited (testimonial, not performance claims)

Citadel, FIS, BNY (via Eliza integration), Carlyle, Mizuho, Travelers, Walleye Capital (vendor-stated: 100% of 400 employees on Claude Code), Hg, Dun & Bradstreet, Morningstar, FactSet. Quoted verbatim in the source; these are marketing testimonials, not independent benchmarks.

## Related

- [[patterns/mcp-multi-agent-framework]] — multi-agent infrastructure underpinning the template deployment model
- [[deployments/mcp-infrastructure]] — connector vs MCP app distinction extends and conflicts with this page's existing MCP framing; Moody's example is the anchor
- [[patterns/effective-harnesses]] — Managed Agent harness features (long sessions, per-tool permissions, credential vaults, audit log) as Anthropic's productized vertical harness
- [[patterns/externalization-survey]] — three-component template = skills + protocols + harness instantiation; concrete vendor grounding for the survey's taxonomy
- [[patterns/topology-taxonomy]] — main-agent + specialist subagent (comparables, methodology checks) is a manager-agent topology instance
- [[patterns/agent-skills]] — the underlying skill-authoring spec behind the "skills + connectors + subagents" packaging
- [[patterns/agent-personas]] — empirical caveat: naive expert personas net ≈ zero on mixed knowledge/alignment workloads
- [[deployments/microsoft-agent-365]] — multi-cloud governance counterpart; M365 add-in layer complements that page's governance plane
