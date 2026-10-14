# Armadin

AI-native offensive-security startup (Palo Alto, CA) founded by Mandiant founder Kevin Mandia. Deploys swarms of specialized AI agents that behave like skilled adversaries, probe an organization's attack surface, and chain minor weaknesses into validated attack paths. Raised a $255.5M Series B at a valuation "topping $2.5B" (reported 2026-10-07), a16z and Accel co-leading; $445M total raised about seven months after its March 2026 launch. **Single-source page (SecurityWeek); performance claims are vendor-supplied and unverified.**

**Tier:** startup.

## What it does

- Continuous adversarial testing in place of periodic penetration tests and vulnerability scanners. Company thesis (2026-10-07): frontier models cut the time and expertise needed to find and exploit vulnerabilities, so point-in-time testing cannot give an accurate picture of exploitable risk.
- Agents probe the attack surface, attempt exploitation, and combine "seemingly minor" issues into validated attack paths: internet-facing vulnerability, then lateral movement, then compromise of cloud resources or sensitive systems.
- Output is the attack path plus its blast radius, rather than thousands of disconnected findings.

## Techniques

- Swarm of specialized agents, not a single agent. Role split not specified in source.
- Every action passes through a control layer overseen by a safety model trained on feedback from human security experts (company claim).
- Funding is earmarked for research, model training, and go-to-market, so in-house model training is implied *(editorial)*. Model details not specified in source.

## Deployment

- Company says it is running agentic attack campaigns in production for Fortune 500 and government customers (unverified; no named customers).
- Delivery model (SaaS / on-prem / customer-environment footprint): not specified in source.

## Costs

Not specified in source.

## Limits and safety

- Exercise agents ran without privileged credentials, source code access, or whitelisting of security controls (company claim, 2026-08).
- False-positive rate, scope limits, and failure modes: not specified in source.
- Running live offensive agents against production systems is a blast-radius risk; the safety-model control layer is the only mitigation described *(editorial)*.

## Evidence: August 2026 live exercise

With agentic security operations provider TENEX.ai, a three-day live AI cyberattack, billed by the vendors as "the largest controlled live AI cyberattack on record" (vendor framing, press-release headline):

- 1,300 attacks, 26,000 agents, about 17M offensive actions, against more than 25,000 services.
- 238 findings, 98 described as significant, chained into 38 validated attack paths.
- No independent verification; no comparison against a human red team baseline.

## Reception and funding

- 2026-10-07: $255.5M Series B, valuation above $2.5B. Co-led by Andreessen Horowitz and existing investor Accel. New: Bain Capital Ventures, Redpoint. Existing participants: 8VC, Ballistic Ventures, GV, In-Q-Tel, Kleiner Perkins, Menlo Ventures.
- 2026-03: formal launch with $189.9M. Late 2025: $24M seed. Total $445M.
- Team: Kevin Mandia (CEO; founded Mandiant 2004, sold to FireEye for $1B in 2014, later acquired by Google for $5.4B), CTO Travis Lanham, chief offensive security officer Evan Peña, chief architect David Slater.
- Same-day SecurityWeek related coverage: Island ($400M at $6.4B) and Cyera ($400M at $12B+), so large security rounds are clustering *(editorial)*.

## Source

- raw/research/weekly-2026-10-07/03-armadin.md (SecurityWeek, captured 2026-10-07)

## Related

- [[lyrie]]
- [[agent-safety-incidents-2026-08]]
- [[agent-identity-governance-2026-09]]
- [[blackhat-ai-coding-agent-cves-2026-08]]
