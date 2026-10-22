# Notion AI

Notion (SaaS workspace) announced on 2026-10-21 a "sixth-generation" agent harness: agents that can work on a single task for 24+ hours (up from 5 minutes), an upgraded `Auto` model router, partial bring-your-own-key (BYOK) and ChatGPT-plan connections, an admin "AI Command Center" (still "soon"), and a new two-pool credit system. Almost all numbers are Notion's own claims from one vendor blog post; no independent validation.

**Tier:** enterprise/prosumer SaaS platform. **Working read (2026-10-21):** a clear example of an incumbent SaaS app turning into a model-agnostic agent/context layer, and of credit pools plus routing replacing flat AI seat pricing.

## What it does

- Notion Agent (personal), Custom Agents (shared/team), Notion MCP (external agents such as ChatGPT and Claude use Notion as shared "brain"; Skills via MCP "coming soon"; Notion calls MCP its "fastest-growing product in Notion history").
- Hundreds of tools via MCPs/connectors (a few dozen earlier in summer 2026); seven models added in the past month.
- Vendor claims: infra uptime above 99.9%; agents up to 50% faster on web/mobile.

## Techniques

- Durable execution: queue-backed worker loop per session, survives restarts.
- Agents write short scripts instead of doing work in tokens.
- Context management: provider-native compaction where available; large tool results offloaded.
- `Auto` router: cheap/fast models for simple requests, stronger ones for long/hard work; re-routes if the current model stalls; new models adoptable immediately among approved providers.
- "Review for me": a separate model judges action safety before execution.

## Costs (credits)

- Business and Enterprise seats: 1,500 Standard credits per month (Notion picks the model via Auto) plus 500 Select credits per month (user picks model, or runs own Custom Agents) per seat.
- Admins can buy workspace credits for shared Custom Agents, high-consumption models (post names Fable and Astra) and overage. Team Custom Agents default to Select credits. ChatGPT-plan connection in the personal agent bypasses both pools.
- Rollout: live for new customers 2026-10-21; existing customers switch 2026-11-02, including those not yet renewed; credits reset at renewal.
- **Vendor-claimed:** Auto gives "similar results" to Opus 5.5 and Astra at about 90% lower average cost across 20+ use cases; Custom Agent runs about 30% cheaper "in testing"; "vast majority" unlikely to run out. No methodology (chart only).

## Customization and limits

- BYOK: Enterprise private alpha via account team. ChatGPT Plus/Pro/Go connection works for the personal agent only, not Custom Agents (FAQ names Pro and Plus).
- Admin controls: restrict models, control who creates/pauses/archives Custom Agents, per-member and per-agent spend limits.
- Not shipped: AI Command Center, Skills via MCP. 24-hour task length is the current ceiling.

## Reading

The credit restructure also moves expensive models onto paid add-on credits, so it is a margin-control move as well as a cost-saving one. A sixth harness rebuild signals heavy churn (favors buy over build). Routing is becoming a commodity SaaS feature.

## Open tension

Notion lists Astra as a live, high-consumption model. The wiki records Astra as gated and reportedly scrapped (WSJ, secondhand; see [[llms/openai]], [[landscape/openai-astra-critical-2026-09]], [[landscape/openai-devday-dots-gpt61-sol-2026-09]]). Unresolved: Notion's "Astra" may be a different or later release. Not filed as a conflict; verify.

## Source

- `raw/research/weekly-2026-10-21/02-notion-agent-harness.md` — Notion blog, "Agents, rebuilt to do more for less", captured 2026-10-21. Vendor-only.

## Related

[[landscape/agentic-compute-pricing-2026-04]] [[landscape/anthropic-subscription-split-2026-06]] [[landscape/stripe-openrouter-acquisition-2026-08]] [[startups/restate]] [[startups/parallel-web-systems]] [[llms/openai]] [[llms/anthropic-claude-family]] [[llms/xai-grok-family]] [[landscape/agent-identity-governance-2026-09]] [[platforms/microsoft]] [[thesis/agents-eating-saas]]
