# Salesforce Agentforce "SalesBleed" vulnerabilities — 2026-09

Zenity Labs disclosed "SalesBleed" (reported via The Register, 2026-09-24): three now-fixed Agentforce flaws — two 0-click CRM exfiltration chains via Web-to-Lead prompt injection, and one anonymous Slack phishing flaw. Salesforce fixed all three (verified 2026-09-21) and collaborated on remediation. The generalizable lesson is an "agent triple": any agent that ingests externally submitted records, renders links/images, and holds sensitive tool access is exposed. Security-vendor research (Zenity sells agent security); one secondary-press source, video PoC claimed.

## Mechanics (per Zenity, as reported)
- **Exfil chain:** attacker-submitted Web-to-Lead content lands in CRM; an Agentforce subagent with the Query Records tool reads it as context ("check my latest leads"); injected instructions make the agent emit an image/link whose fetch carries data to an external host. The frontend fetches external img URLs without sanitization or user interaction.
- **Guardrail bypass:** Trusted URLs redaction did not register hostnames ending in an unrecognized TLD, and certain characters broke URL parsing. Slack URL unfurling auto-fetches previews, a second exfil channel.
- **Slack phishing:** the "Reply to a Slack Thread" action needed no user confirmation and carried no visible attribution to the invoking user.

## Timeline
Reported 2026-06-01; Salesforce confirmed fix work next day; Trusted URLs bypass fix verified 2026-08-19; all three fixes verified 2026-09-21; report published 2026-09-24.

## Reading
- Michael Bargury (Zenity): "secure-by-design remains essential but for agents it may no longer be enough." Vendor-managed guardrails proved bypassable by trivial parsing edge cases — buyers should not treat them as a boundary.
- Mitigations implied: allowlist (not TLD denylist) URL handling, confirmation on outbound-message actions, visible per-user attribution, neutralize auto-fetched images/unfurls, runtime monitoring.
- Surface widening: Slack and Claude-surfaced CRM data ([[salesforce-anthropic-claudeforce-2026-08]]) extend the blast radius beyond Salesforce's UI; the source does not mention Claudeforce, so that link is this wiki's inference.
- Extends C18 (governance claims vs friction): see [[../conflicts/open-questions-2026-04]].

## Source
- `raw/research/weekly-2026-09-30/02-salesforce-salesbleed.md` (The Register, 2026-09-24, reporting Zenity Labs)

## Related
- [[../platforms/salesforce]]
- [[salesforce-anthropic-claudeforce-2026-08]]
- [[agent-safety-incidents-2026-08]]
- [[openai-agent-escape-incidents-2026-09]]
- [[agent-identity-governance-2026-09]] — missing attribution/confirmation supports this category
- [[blackhat-ai-coding-agent-cves-2026-08]]
- [[mcp-rce-supply-chain-2026-05]]
- [[nvidia-open-agent-safety-platform-2026-09]]
