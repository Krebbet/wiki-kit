# Claude chat and Cowork unified for Enterprise (2026-11)

On 2026-11-11 (capture date) Anthropic announced that Claude chat and Cowork are one experience, generally available for Claude Enterprise plans on web, desktop and mobile; it first shipped for Pro and Max in September 2026. Agentic work runs in Anthropic-managed cloud sessions (isolated VM per session, network egress off by default for Enterprise). Pricing stays usage-based; admins get four cost controls (Efficient mode, model entitlements, tiered spend limits, pooled group budgets). Vendor-authored single source; efficiency numbers are Anthropic's own claims. Signal: the agent surface is moving into a vendor-hosted runtime, which narrows the case for a self-built agent shell on Claude. Watch the default-on date (unverified, see below).

## What shipped

- **GA date:** announced 2026-11-11 (raw capture date; the post says "generally available today"). Prior step: chat and Cowork unified for Pro and Max in September 2026 (month only; no day given).
- **Surface:** one Claude on web, desktop and mobile. Conversations start as chat; when a task needs code execution or files, Claude continues in the cloud and returns the finished document, analysis or deck. Work continues after the laptop is closed.
- **Carry-over:** chats, projects, connectors, skills and plugins carry over to the unified experience.
- **Plan naming:** the post's editor's note says pre-2026-10-30 mentions of Max include what are now the Max and Ultra plans.

## Security model (per post, 2026-11-11)

- Builds on already-approved chat controls: SSO and the Compliance API. Data encrypted in transit and at rest; not used for training by default.
- Cloud sessions run in isolated VMs, network egress off by default for Enterprise, connector credentials kept outside the sandbox. Central visibility for security teams is asserted, not detailed.
- Full architecture is deferred to a Trust Center best-practices guide (not captured).

## Cost controls

- **Pricing:** Enterprise stays usage-based. Agentic work can use more tokens than quick chat.
- **Efficient mode:** new setting that keeps the unified experience on Sonnet and Haiku models.
- **Model entitlements:** which models each role can use.
- **Spend limits:** org, group and member level.
- **Pooled group budgets:** one shared monthly amount per group.
- **Model efficiency claims (Anthropic, unverified independently):** Claude Opus 5.5 "costs 40% less to run" than Opus 5 on typical workloads; Sonnet 5.5 up to 30% less than Sonnet 5 for most work. Cited via a claude.dev blog post, not captured.

## Admin rollout

- Managed in Organization settings. Existing Enterprise customers get an email about the rollout for their organization.
- **Excluded, stay on current configuration:** orgs using zero data retention for Claude Code, a HIPAA-ready configuration, or customer-managed encryption keys.
- Access is controlled by role.

## Default-on date: unverified

A secondary German source claims the unified experience turns on by default 2026-11-16 for existing orgs. The raw file does not confirm this: it states only that admins "can manage the rollout" in Organization settings and that customers will be emailed. No default-on date appears. Treat 2026-11-16 as **unverified**. Check the admin setup guide and the rollout email before telling a client a date.

## Gaps

- No audit-log or Compliance API coverage statement for cloud (Cowork-style) sessions. The post only says the Compliance API is an existing control the change "builds on". Whether agentic cloud sessions are fully covered is not stated. Ask before assuming.
- No concrete pricing figures, token rates or Efficient-mode quality tradeoffs.
- ZDR, HIPAA-ready and customer-managed-key orgs are excluded, so the most regulated tenants do not get the feature yet; no timeline given.
- Customer quotes (Carvana, LifeMoves, Quantium, one unnamed) are vendor-selected testimonials, not independent reception. Net market reception: no friction-surface evidence captured.

## Build-vs-buy readthrough

- **Buy leaning for knowledge-work agents on Claude Enterprise:** the managed VM sandbox, connector credential isolation, role-based model access and pooled budgets cover pieces teams otherwise build (sandboxing, secrets handling, cost governance). Inference, not a source claim.
- **Build still holds** where data residency, ZDR, HIPAA-ready or customer-managed keys are required, since those orgs are excluded for now, or where egress-off-by-default blocks needed integrations.
- **Cost risk:** usage-based pricing plus higher agentic token use makes Efficient mode and spend limits the controls to configure on day one; Efficient mode pins to Sonnet/Haiku, so heavy reasoning tasks lose Opus.
- Contrast with the earlier consumer-plan restructuring in [[landscape/anthropic-subscription-split-2026-06]] and the channel push in [[landscape/anthropic-enterprise-distribution-2026-05]].

## Source

- `raw/research/weekly-2026-11-11/02-claude-unified-enterprise.md` (Anthropic blog, "Claude Cowork and chat come together for Enterprise", https://claude.com/blog/unified-claude-enterprise, captured 2026-11-11)
- German secondary-source default-on claim (2026-11-16): relayed in the task brief, not captured in raw; unverified.

## Related

- [[llms/anthropic-claude-family]]
- [[landscape/anthropic-enterprise-distribution-2026-05]]
- [[landscape/anthropic-subscription-split-2026-06]]
- [[landscape/agent-identity-governance-2026-09]]
- [[landscape/anthropic-opaque-acquihire-2026-10]]
- [[landscape/github-copilot-local-sandboxing-2026-10]]
