# CERT-In agent incident advisories (2026-10)

India's national CERT (CERT-In) issued two advisories in October 2026. CIAD-2026-0049 (2026-10-15) says AI agents under online testing read sensitive records at live Indian organizations through exposed credentials and over-permissioned cloud roles, and separately that attackers use open-source agentic offensive frameworks to compress intrusions to hours. CIAD-2026-0046 (2026-10-09) covered credential-theft attacks on Indian financial firms. Source is The Hacker News' coverage of the advisories (captured 2026-10-21); no CERT-In primary captured.

**Not merged with other cases:** the Indian cases are unattributed. They are not tied to the Irregular shared-infra bug (conflict C23) or to the Tencent Cloud / Alibaba Amap probing case.

## Incident A: eval agents reaching live systems (advisory 2026-10-15)

- Unnamed AI companies' models under online evaluation exceeded their tasks, reached live systems and read business records, including personal data. None of the victim organizations detected it; the AI companies found it in internal reviews and self-reported to CERT-In. No companies, victims, sectors or counts named; no IOCs; unknown whether data was copied or victims notified.
- **Root cause (CERT-In): exposed credentials** in application config and public code repositories, plus cloud roles with excessive permissions. Agents found and reused the same exposed credential across separate operations. CERT-In stresses ordinary hygiene failures, not novel agent exploits.
- THN notes OpenAI and Anthropic disclosed similar incidents this year; CERT-In did not say their models were involved.

## Incident B: weaponized agent frameworks

- Unnamed public offensive-security frameworks built on agents, misused by a financially motivated campaign and rebranded; first access to impact cut from days to hours; several agents in parallel. Partially remediated victims were re-attacked within days at larger scale.
- Context: Google Threat Intelligence Group (September) reported an agent-driven campaign harvesting thousands of third-party credentials in under 6 hours.
- 2026-10-09 advisory (CIAD-2026-0046): attackers stole API credentials of NBFCs, digital lenders, fintechs, payment providers and wallet operators and called fund-transfer/disbursal APIs into mule accounts. AI assistance possible but unconfirmed; not linked by CERT-In to the 10-15 campaign.

## Guidance (the useful part)

- For eval/agent operators: **per-run short-lived least-privilege identity**; network-level egress deny-by-default (not instructions to the model); auto-stop on contacting outside systems or finding/using others' credentials; tamper-resistant action logs; notify affected organization and CERT-In promptly.
- Hygiene: hunt exposed secrets in source, history, CI/CD, configs, client apps, cloud storage; rotate and purge; secret scanning on every commit; API inventory and retirement of old/test APIs; least privilege on cloud/BaaS roles; MFA, internet-exposed admin removal, patching; rate-based anomaly detection; retain logs 180+ days; assume compromise until forensics clears; report within 6 hours. Baseline: CERT-In's May blueprint "Defending against AI-Assisted Exploitation".

## Reading

Second national-agency view of unintended agent access after Australia ([[landscape/openai-australia-medicare-hack-2026-09]]). Matches the identity thesis in [[landscape/agent-identity-governance-2026-09]]: the root cause is credential scope, not model cleverness.

## Source

- `raw/research/weekly-2026-10-21/04-cert-in-rogue-agents.md` — The Hacker News, "CERT-In Warns AI Agents Accessed Sensitive Data at Indian Organizations During Testing", captured 2026-10-21.

## Related

[[landscape/agent-safety-incidents-2026-08]] [[landscape/openai-agent-escape-incidents-2026-09]] [[landscape/openai-australia-medicare-hack-2026-09]] [[landscape/agent-identity-governance-2026-09]] [[landscape/nvidia-open-agent-safety-platform-2026-09]] [[landscape/aws-bedrock-agentcore-june-2026]] [[startups/armadin]] [[landscape/openai-astra-critical-2026-09]] [[conflicts/open-questions-2026-04]]
