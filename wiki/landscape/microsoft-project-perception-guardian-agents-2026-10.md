# Microsoft Project Perception and Guardian Agents (2026-10)

Microsoft expanded Project Perception (Microsoft Security) from SOC agents into agent governance: Guardian Agents that monitor and contain other agents, a per-agent identity layer, and a "Dynamic Agent Risk" score. Announced the week of 2026-10-19 (blog dated 2026-10-19); preview only, used inside Microsoft and "a small set of select customers". **Watch, not buy:** the containment claims are vendor-stated, the customer base is tiny, and Nadella himself said the products "need to be battle tested" (Dark Reading, captured 2026-11-04). Single trade-press source; analyst quotes are the only independent signal.

## What Microsoft says it ships (preview, 2026-10)

- **Project Perception:** first public preview via Defender in 2026-08 for SOC scenarios, with red/blue/green agents (scan attacker paths / rank risks / mitigate). Initial use is vulnerability management via MDASH (AI code scanner, preview), which uses several models including MAI-Cyber-1-Flash, Microsoft's first cyber-specialised model.
- **Agent identity:** each agent gets an identity separate from the user who launched it, starting with zero permissions and up-scoping to what the task needs. Entra Agent ID is extended to agents not built for Entra.
- **Discovery:** detects 35 more local agent types, 60 in total, including Claude Code, OpenAI Codex and GitHub Copilot. Expanded agent registry across M365 admin center, Defender, Entra, Intune and Purview, plus a Perception Agent Insights view.
- **Dynamic Agent Risk:** one continuously updated score from Entra, Defender, Intune, Purview, Sentinel and Global Secure Access signals, replacing siloed scores. Includes intent-vs-action monitoring: the source's example is an expense-approval agent hit by hidden prompt injection that starts touching a wire-transfer system and is flagged as off-intent.
- **Dynamic Conditional Access for agents:** block writes while keeping reads, restrict network paths, revoke access, or stop the runtime. Claimed to interrupt a live session without disrupting the user's own work (vendor-stated, preview).
- **MXC (Microsoft Execution Container):** sandbox that keeps credentials and security controls outside the agent's reach. Rationale: an attacker "will manipulate the security controls first". See [[landscape/github-copilot-local-sandboxing-2026-10]] for the developer-side GA.

## Cost, rollout, limits

- Builds on Microsoft 365 E7 ($99/user/month; includes E5, Agent 365, Entra Suite). Microsoft has not said whether the new capabilities are in E7; Perception is priced on consumption. Forrester (Cser) estimates E7 at about $1,200/user/year list, about $600 after typical 40-50% volume discounts (2026-10).
- Guardian Agent capabilities expand to more external customers in broader preview rings over the next months; more at Ignite (2026-12).
- Partners can publish agent risk events into Agent 365 via public APIs, but Microsoft could not name public partner integrations.

## Reception and criticism

- Nadella (2026-10, CISO event): Perception and Agent 365 (GA since 2026-05) "need to be battle tested"; Defender behavioural monitoring "has to go way up".
- Forrester (Cser): least privilege yes, "least agency" no; third-party integration "not first rate so far"; expects an E7 upsell push. Calls the Okta-led Blueprint Alliance "a marketing ploy"; Microsoft is not a named member.
- Suzu Labs CTO Calderone: the worst outcomes happen inside the authorised envelope, and guardian agents are themselves overprivileged, manipulable actors.
- Okta (Peri): guardian agents are only as good as the ecosystem; "control authority, not how models think".

## Competitive context (vendor-announced, recent weeks)

Okta Agent Gateway (separate agent vs user permissions; planned token-rejecting kill switch), Teleport (Cisco-backed; task-tied privileges), CrowdStrike Agentic Identity Provider + Falcon Guardian (endpoint agent discovery and controls). Choice per Forrester: Microsoft-centric stack (Entra/Defender/Intune) versus multivendor ("many vendors, many price lists"); the unified-stack pitch fits poorly for agents running across AWS, GCP, Salesforce and ServiceNow.

## Techniques worth stealing

Separate agent identity from user identity; zero-start permissions with task-scoped up-scoping; keep credentials and monitoring outside the agent sandbox; graduated response (block writes, keep reads) instead of a binary kill; intent-vs-action drift as a risk signal. Baseline that costs nothing: inventory every agent including dev machines, per-agent identity with expiring credentials, human approval for consequential actions (Calderone).

## Source

- `raw/research/weekly-2026-11-04/02-microsoft-guardian-agents.md` (Dark Reading news analysis, captured 2026-11-04). The same source cites a July 2026 OpenAI incident per METR (2026-08-26); not verified here, see [[landscape/openai-agent-escape-incidents-2026-09]].

## Related

- [[platforms/microsoft]] — Agent 365 / E7 profile
- [[landscape/agent-identity-governance-2026-09]] — per-agent identity category and peers
- [[landscape/microsoft-foundry-agent-harness-2026-09]] — Microsoft agent identity lifecycle
- [[landscape/microsoft-build-2026-06]] — Scout policy conformance lineage
- [[landscape/nvidia-open-agent-safety-platform-2026-09]] — separate-from-agent enforcement parallel
- [[landscape/gemini-at-work-agent-2026-10]] — Google per-agent identity and Agent Sandbox
- [[landscape/openai-agent-escape-incidents-2026-09]] — incident motivation
- [[landscape/blackhat-ai-coding-agent-cves-2026-08]] — coding agents as discovered agent types
