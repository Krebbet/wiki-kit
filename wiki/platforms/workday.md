# Workday

At Workday Rising (reported 2026-10-14 to 10-21) Workday made its Sana agentic layer ("Sana Home") the front door for users, announced an Agent Harness (runtime for agents over HR/finance data) it describes as generally available, plus ambient agents and Decision/Work Intelligence apps. **Single secondary source:** Constellation Research relaying vendor statements; no Workday primary captured.

**Tier:** enterprise platform. **Working read (2026-10-21):** incumbent SaaS keeping the interface in-house (contrast Salesforce ceding UI to Claude) and exposing its system of record to outside agents via governed MCP.

## Agent Harness

- Runtime where agents run in isolated environments with cross-process context and built-in memory; serves Workday agents and third-party agents, which run outside the Harness and reach data over MCP with governance.
- Build with Workday's Developer Agent or frameworks such as Google ADK and TypeScript.
- **GA: vendor-stated, unverified.** Article says "Workday said Agent Harness is generally available" (2026-10-21), with no date, region or tier caveats; confirm against a Workday primary.
- Pricing: consumption via Flex Credits; no rates published. No hard limits, customer evidence or adoption numbers.

## Sana

- Sana Home unifies tasks, agent activity and meetings; "generally available for multiple Workday customers" (vague partial GA); priced under Flex Credits. Sana Principal Agent orchestrates across agents/apps for Sana Enterprise customers. Sana Agent Builder named, no detail. Sana was acquired a little over a year earlier (linked article cites ~$11B spend; not verified here).
- Analyst Holger Mueller (Constellation) calls Workday "the only vendor offering an all-purpose agentic interface" (opinion, unverified).

## Other announcements

- Ambient agents / Talent Acquisition Agent (Recruiting, Paradox, HiredScore, skills data): GA Q1 2027, not available.
- Workday Candidate Profile: candidate-controlled, prefills about 80% of standard application fields; no screening or ranking; GA December 2026; on by default, included in Recruiting subscriptions.
- Decision Intelligence (predictive scenarios across Planning, HCM, finance) and Work Intelligence (catalog of work by task; cost of work across humans and AI): availability and pricing not stated.
- Named without detail: Admin Agent, AI Localized Payroll, Agentic CLM, Compliance Intelligence, Data Cloud.
- CEO Aneel Bhusri: Workday will "refound" around AI ("Chapter Four").

## Takeaways

- Worth stealing: governed MCP access for external agents; platform-supplied memory and isolated runtime.
- Build-vs-buy: Harness is the route for custom agents on HR/finance data; ADK/TypeScript support lowers framework lock-in; cost unpredictable until Flex Credit rates exist.
- Follow-ups: Flex Credit rates, primary-source GA confirmation, Sana Home GA breadth, Decision/Work Intelligence availability.

## Source

- `raw/research/weekly-2026-10-21/03-workday-sana-agent-harness.md` — Constellation Research, "Workday makes Sana its interface, launches Agent Harness, decision and work intelligence", captured 2026-10-21.

## Related

[[thesis/agents-eating-saas]] [[platforms/salesforce]] [[landscape/salesforce-anthropic-claudeforce-2026-08]] [[platforms/microsoft]] [[landscape/agent-identity-governance-2026-09]] [[landscape/aws-bedrock-agentcore-june-2026]] [[landscape/google-cloud-next-2026-day2]] [[landscape/agentic-compute-pricing-2026-04]] [[platforms/databricks]] [[platforms/snowflake]] [[landscape/enterprise-ai-market-2025-2026]]
