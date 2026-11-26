# MONAI Label zero-day found and exploited by attacker agents (2026-11)

Amazon Threat Intelligence reported (2026-11-20) that a suspected China-nexus actor's autonomous agents, running the open-source Cairn framework, found a path-traversal zero-day in the MONAI Label medical-imaging server and later gained root on one university server. **Action: upgrade to 0.8.6 or later, remove from untrusted networks, and treat previously exposed hosts as possibly compromised.** The flaw is independently supported; the agent story rests on Amazon alone.

## Vulnerability (checked 2026-11-25)

- CVE-2026-133968, CVSS 3.1 9.8 (scored by MITRE as CNA; NVD API, published 2026-11-20); affected before 0.8.6. Advisory GHSA-qc22-rmgc-vg94.
- CISA KEV: added 2026-11-23.
- 0.8.6 reached PyPI 2026-11-22 (package contents not inspected). Both captured write-ups say no fixed release; that is out of date. The CSA note also says no CVE was assigned.
- Authentication is off by default; per CSA, the low-privilege ANNOTATOR role suffices when it is on.

## Incident, per Amazon (not independently confirmed)

- Campaign of about 48 hours from 2026-09-08. About 11 minutes from API mapping to arbitrary file write; root came in a separate later session.
- Operator set goal and targets; agents chose methods, with some human intervention.
- Attribution: moderate confidence. No named group, no government link established. Underlying LLM not named.
- A second university network compromise is inferred, not confirmed. Other attempts failed. No patient data reported affected.

## Defender actions

Upgrade; firewall; enable authentication (`MONAI_LABEL_AUTH_ENABLE`); run unprivileged with writes limited to the datastore; check upload-endpoint logs, unexpected files, startup files, SSH keys and cron; rebuild where compromise is plausible. Inventory research-run AI services outside central IT. Indicators are in the source captures.

## Why it matters *(synthesis)*

Agents used offensively against a real target, discovering a flaw rather than replaying a known one, if Amazon's account holds. Patch-to-exploit assumptions built on human attacker speed are suspect.

## Source

- `raw/research/weekly-2026-11-25/06-monai-thehackernews.md` (The Hacker News, captured 2026-11-25)
- `raw/research/weekly-2026-11-25/07-monai-csa.md` (Cloud Security Alliance, 2026-11-21)
- NVD API, CISA KEV catalog and PyPI, queried 2026-11-25

## Related

- [[landscape/agent-safety-incidents-2026-08]]
- [[landscape/cert-in-agent-incidents-2026-10]]
- [[landscape/openai-astra-critical-2026-09]]
- [[landscape/openai-australia-medicare-hack-2026-09]]
- [[landscape/blackhat-ai-coding-agent-cves-2026-08]]
