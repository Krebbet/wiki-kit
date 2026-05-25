# Agent Interoperability Protocols

Mechanism page for the **substrate communication-protocol layer** that ClawNet, DID/VC architectures, and any other cross-vendor agent collaboration framework all build on top of. Anchored on Louck, Stulman & Dvir 2025 *Improving Google A2A Protocol: Protecting Sensitive Data and Mitigating Unintended Harms in Multi-Agent Systems* (arXiv 2505.12490). A2A (Agent2Agent) is Google's open protocol for cross-vendor agent interoperability, released April 2025 and contributed to the Linux Foundation in June 2025. The paper analyses A2A's security gaps and proposes mitigations relevant to consumer-counter-power deployment of any agent-collaboration framework — A2A's structural weaknesses are *inherited* by ClawNet and need addressing at the protocol layer rather than the governance layer alone.

## What A2A is

A2A standardises message exchange between AI agents across enterprise systems regardless of underlying frameworks or vendors. Core capabilities:

- **Capability discovery** via "Agent Cards" in JSON format.
- **Task management** with defined lifecycle states.
- **Agent-to-agent collaboration** via context + instruction sharing.
- **User experience negotiation** that adapts to different UI capabilities.

Built on **OAuth 2.0, HTTPS, JWT tokens** — inherited web security primitives originally designed for human-initiated sessions, not for autonomous, scale-operated agents. **This is the structural problem the paper identifies.**

## Six core security gaps documented

| # | Gap | Severity |
|---|---|---|
| 1 | **Token lifetimes are implementation-dependent**, not protocol-enforced. Leaked credentials can remain valid for hours or days (CVE-2025-1198 cited). | High |
| 2 | **No strong customer authentication (SCA) requirement** for high-risk actions like payments or identity switching. CWE-306 ("missing authentication for critical function"). | High |
| 3 | **Coarse-grained OAuth scopes** that grant overly broad access (e.g., full calendar access when only availability is needed). 18.5% of OAuth deployments empirically request unnecessary scopes (Dimova et al.) violating GDPR Article 5 (data minimisation). | High |
| 4 | **Absence of explicit user consent flows** before sensitive data sharing or delegation. GDPR Article 7 + PSD2 compliance gaps. | High |
| 5 | **Excessive exposure of data to intermediary agents** when direct user-to-service channels could minimise propagation risk. | Medium-high |
| 6 | **Threat of prompt injection attacks** that manipulate agents into disclosing sensitive data despite security instructions. | High |

## Empirical leakage finding

The paper benchmarks two implementations (both Gemini 2.0 Flash) under 9 adversarial prompt-injection variants × 5 repetitions = 45 attempts to elicit simulated credit-card and ID numbers.

| Implementation | Leakage rate |
|---|---|
| **Baseline A2A** (sensitive data retained in agent context) | **60–100%** |
| **Enhanced A2A** (DirectDataFlowController with context separation) | **0%** across all 45 attempts |

**Performance overhead** is acceptable: latency variance 0.2–0.8s in some tests, "within acceptable bounds for interactive agent workflows."

This is the load-bearing empirical result — context separation via direct user-to-service flows + ephemeral tokens essentially **eliminates prompt-injection leakage** while keeping operational overhead negligible.

## Eight protocol-level mitigations proposed

1. **Ephemeral tokens** (30 sec – 5 min, single-use) for sensitive transactions.
2. **Multi-factor SCA** using zero-knowledge proofs, biometrics, or MFA before payment / identity operations.
3. **Granular per-task scopes** binding tokens to specific actions, amounts, and time windows.
4. **Explicit `USER_CONSENT_REQUIRED` task state** that pauses execution until user approval; auditability for regulatory alignment.
5. **`DirectDataFlowController` pattern** enabling secure direct user-to-service data tunnels, bypassing intermediary agents.
6. **Bundled transaction approval** to reduce consent fatigue while maintaining security through single SCA-verified session.
7. **Audit logging** with timestamped consent records + identity confirmation (PSD2 + GDPR alignment).
8. **Threat-model documentation** at protocol layer — semi-trusted agents, TLS 1.3 transport, verified endpoint registries, user-verifiable approvals.

## Why this matters for the wiki's mandate

ClawNet ([[clawnet-readout]]) is presented as a *governance overlay* on A2A — adding identity binding, scoped authorization, action-level accountability. **A2A's vulnerabilities are inherited:** ClawNet's policy layer cannot fully remediate token-replay risk, coarse OAuth scopes, or prompt-injection leakage if A2A itself does not enforce ephemeral tokens, granular scopes, or context separation.

**Concrete implication.** ClawNet's appeal is its three governance primitives (identity / authz / accountability). But under the current A2A specification, those primitives operate over a transport layer that:
- Lets long-lived tokens leak indefinitely.
- Allows OAuth scope over-permissioning.
- Does not enforce SCA for high-stakes actions.
- Does not specify a consent state machine.
- Exposes sensitive data to intermediary agents by default.

A consumer-counter-power deployment of ClawNet that handles payment credentials, identity documents, or DSAR-extracted personal data (per [[data-disruption-strategy-map|Tier 1 #1]] DSAR coordination) inherits these gaps.

**Recommended pattern**: ClawNet (or DID/VC, per [[decentralized-agent-identity]]) governance + A2A protocol enhancements per this paper. Co-dependent, not standalone.

## How this maps onto the wiki

| Wiki anchor | Connection |
|---|---|
| [[clawnet-readout]] | A2A is the transport substrate underneath ClawNet. The risk catalogue on [[clawnet-readout]] should reference this page; the "centralised operator trust" + "contact-graph metadata" risks have A2A-layer counterparts (token-management, scope-granularity). |
| [[decentralized-agent-identity]] | DID/VC architecture also runs on top of A2A in the prototype. Same protocol-layer caveats. |
| [[agent-mediated-negotiation-empirics]] | Negotiation-layer benchmarks (AgenticPay, Abdelnabi) assume the messages are unforged + the agents are who they say they are. A2A protocol security underwrites those assumptions. |
| [[data-disruption-strategy-map\|Risk class 3 — authenticated-endpoint automation]] | A2A operates exclusively in authenticated-endpoint territory. Token lifetime + scope granularity + SCA are the governance primitives that distinguish acceptable from CFAA-exposed automation. |
| [[possible-strategic-levers]] | Any lever depending on agent-mediated coordination (cross-cutting infrastructure section) inherits A2A's substrate properties. |

## Caveats

1. **A2A protocol evolves rapidly.** The paper analyses an early version; v0.3 (Linux Foundation contribution, June 2025) introduced some hardening (gRPC support, signed security cards). Subsequent versions may close some of the documented gaps.
2. **The paper's mitigations are protocol-level proposals**, not yet adopted into the A2A spec. Adoption depends on the A2A Working Group governance.
3. **Single research-group analysis.** Independent threat-model review at the W3C / Linux Foundation level not yet captured on this wiki.
4. **Adjacent protocols** (Anthropic's Model Context Protocol; KQML; FIPA-ACL) are not analysed in this paper. A complete agent-interop substrate landscape would catalogue them; they are not yet on this wiki.

## Source

- Louck, Stulman & Dvir. 2025. *Improving Google A2A Protocol: Protecting Sensitive Data and Mitigating Unintended Harms in Multi-Agent Systems*. arXiv 2505.12490. Ariel Cyber Innovation Center (Ariel University) + Jerusalem College of Technology. Captured: `raw/research/clawnet-adjacent-methods/20-a2a-protocol-security-2025.md` + `10-a2a-protocol-security-2025-abs.md`. Trust tag: arXiv preprint, single research group, empirical prompt-injection benchmark (45 attempts) + protocol-level threat-model analysis.

**Substrate references** — to cite directly when wiki claims are load-bearing:
- Google A2A Protocol Specification (April 2025; Linux Foundation contribution June 2025).
- W3C OAuth 2.0 / OpenID Connect specifications.
- CVE-2025-1198 (token replay), CVE-2024-7042 (agent exploitation), CWE-306 (missing authentication), CWE-200 (unauthorized exposure), CWE-1220 (coarse-grained access control).

## Related

- [[clawnet-readout]] — governance overlay running on top of A2A; inherits A2A's protocol-layer vulnerabilities
- [[decentralized-agent-identity]] — alternative governance model; same A2A substrate
- [[agent-mediated-negotiation-empirics]] — negotiation-layer behaviour above the protocol
- [[data-disruption-strategy-map]] — risk class 3 (authenticated-endpoint automation) is the operational frame
- [[the-firms-view]] — none directly; A2A security is symmetric (firm-side and consumer-side both benefit from hardening)
