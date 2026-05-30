# Lyrie

Lyrie.ai (OTT Cybersecurity LLC, Dubai) exited stealth on 2026-05-11 with a $2M pre-seed and the release of the Agent Trust Protocol (ATP), an open cryptographic standard for AI agent identity, scope, attestation, delegation, and revocation. The company's pitch is that autonomous AI agents currently operate without any protocol-level identity or authorization layer — the ATP is positioned as the "SSL/TLS for agents," though that analogy is unverified vendor marketing from a stealth-exit announcement.

## What It Does

Lyrie wraps the ATP open standard inside a broader autonomous cybersecurity platform targeting the threat surface created by agentic AI deployments. Platform capabilities as claimed (2026-05-11, unverified):

- **Autonomous penetration testing** — described as a 7-phase pentest from a single command with proof-of-concept exploits and code-level remediation. No third-party benchmarks.
- **Adversarial AI red-teaming** — GCG and AutoDAN workflows on H200 GPU infrastructure.
- **OWASP ASI 2026 coverage** — threat catalog mapped to the Agentic Security Initiative.
- **Zero-day research** — described as autonomous discovery in compiled software via "Omega-Suite" binary analysis. Unverified.
- **Deployment range** — claimed production-ready from consumer hardware through enterprise GPU infrastructure. No SaaS/on-prem breakdown in source.

No named customers. No third-party benchmarks. All capability claims come from the stealth-exit press release.

## Agent Trust Protocol (ATP)

ATP is the technically novel piece. The mechanism addresses agent trust at the protocol layer rather than at the network perimeter — a gap made acute by multi-agent orchestration frameworks like MCP where agents can be compromised or impersonated without any identity signal reaching the orchestrator (see [[landscape/mcp-rce-supply-chain-2026-05]]).

Five pillars (per Lyrie's own specification):

| Pillar | What it covers |
|---|---|
| **Identity** | Cryptographic identity assignment per agent |
| **Scope** | Authorized action surface, enforced at protocol level |
| **Attestation** | Proof that an agent is operating as declared |
| **Delegation** | Chain-of-trust for agent-spawns-agent patterns |
| **Revocation** | Invalidation of compromised or expired agent credentials |

The framing directly targets the "every AI agent is effectively anonymous" problem (CEO Guy Sheetrit, 2026-05-11). This is a real gap — current agentic stacks authenticate at the API-key level, not the agent level, which means scope enforcement and tamper detection have no foundation.

**Standardisation status:** IETF submission is in-process as of 2026-05-11. It is NOT ratified and has no IETF working-group adoption to date. The "SSL/TLS for agents" analogy is vendor marketing framing with no independent validation. Treat as a pre-standard proposal.

**Reference implementation:** MIT-licensed, publicly available at `github.com/OTT-Cybersecurity-LLC/lyrie-ai`.

## Funding and Traction

- **$2M pre-seed** closed 2026-05-11. Investor names not disclosed in source.
- **Anthropic Cyber Verification Program (CVP)** — OTT Cybersecurity LLC accepted as a verified dual-use cybersecurity operator (2026-05-11). Scope covers vulnerability research, offensive security tooling, and red-team workflows on Claude infrastructure, subject to Anthropic safety policies. See [[llms/anthropic-claude-family]].
- Series A preparation underway targeting enterprise and government markets; not closed as of source date.
- No disclosed revenue, customers, or production deployments.

## Positioning

The ATP scope/attestation model is the concrete technique worth watching regardless of Lyrie's platform trajectory. Protocol-level agent identity addresses a structural gap that perimeter-based approaches (firewalls, API gateways) cannot close once agents are operating inside trusted boundaries. The MCP RCE disclosure ([[landscape/mcp-rce-supply-chain-2026-05]]) is a concrete example of the threat vector ATP's model targets: a compromised MCP server has no agent-level identity signal for an orchestrator to verify or revoke.

ATP is open (MIT). Teams building multi-agent orchestration can adopt the protocol without Lyrie's platform. Lock-in risk is low at the protocol level; Lyrie's platform lock-in is unknown and pre-commercial.

## Source

`raw/research/weekly-2026-05-17/04-lyrie-agent-trust-protocol-2026-05.md`

Original: GlobeNewswire — "Lyrie Completes $2 Million Preseed Round to Build the Security Layer for the AI Agent Era," 2026-05-11. https://www.globenewswire.com/news-release/2026/05/11/3291848/0/en/lyrie-completes-2-million-preseed-round-to-build-the-security-layer-for-the-ai-agent-era.html

## Related

- [[landscape/mcp-rce-supply-chain-2026-05]] — OX Security MCP STDIO RCE disclosure; 7,000+ vulnerable servers; the concrete threat vector ATP's scope/attestation model is designed to address
- [[llms/anthropic-claude-family]] — Anthropic CVP acceptance context
- [[landscape/yc-w26-ai-batch]] — adjacent security-for-agents startup cluster signal
