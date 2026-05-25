# Decentralized Agent Identity

Mechanism page for the **W3C Decentralized Identifier (DID) + Verifiable Credential (VC) architecture for AI agents** as the **decentralised alternative to ClawNet's centralised cloud orchestration** for cross-user agent collaboration. ClawNet ([[clawnet-readout]]) addresses cross-user agent governance via a single cloud orchestration server holding gateway containers and L1 ACLs; that page flagged "centralised operator trust" as risk #1. This page documents the natural counterpart: each agent self-controls a ledger-anchored DID; trust is established via third-party-issued VCs; no central orchestrator. Anchored on Garzon et al. 2025 *AI Agents with Decentralized Identifiers and Verifiable Credentials* (arXiv 2511.02841, Technische Universität Berlin / T-Labs).

## Core architecture

**Each agent holds a unique W3C Decentralized Identifier (DID) anchored in a shared distributed ledger.** The DID document (DID doc) contains public keys and service endpoints; only the agent's private-key holder can update it. The prototype uses Hyperledger Indy (permissioned DLT) as the test ledger, queried via DIF Universal Resolver REST endpoint.

**Two credential types:**

1. **Basic VCs (bVCs)** — issued by the agent's own security domain's orchestrator. Minimal claims: "is an agent, with this DID, in this domain."
2. **Rich VCs (rVCs)** — issued by in-domain authority agents. Claims about roles, capabilities, authorisations, organisational affiliation.

**Cross-user dialogue protocol.** At dialogue initiation, both agents perform zero-trust mutual authentication: each presents its DID and selected VCs as a Verifiable Presentation (VP); the other verifies cryptographic signatures on the VP and on each VC, plus issuer trustworthiness. Uses **DIF Presentation Exchange** (Decentralized Identity Foundation standard) for VP exchange and **DIF Credential Manifest** for VC issuance.

**Trust model.**
- **Intra-domain trust** relies on the orchestrator's DID doc (shared outside the ledger).
- **Cross-domain trust** requires **organisational trust**: both agents must independently recognise and trust the issuer of the presented VCs, even without prior agreement.
- **Unstructured claims** in VCs (natural language, images, audio) — an LLM can interpret these to bootstrap dynamic trust without rigid schema standardisation between domains.

## Empirical findings from the prototype

The paper deployed agents using LangChain (Process I), AutoGen (Process II), and A2A (Process III) and ran 100 trials per process across GPT-4.1, GPT-4.1-mini, and GPT-4o.

| Metric | Result |
|---|---|
| **Completion rates** | Process I (intra-domain attestation, LangChain): 63–91%. Process II (intra-domain, AutoGen): 90–91%. Process III (cross-domain A2A): 80–91%. |
| **Failure modes** | LLM forgot data; altered VC fields; skipped authentication steps. |
| **Security incident** | Both agents agreed to accept one-way authentication, violating policy. |
| **Performance** | Single cross-domain auth: ~10–30 seconds. Driven by sequential LLM calls (10–40 per process), not ledger resolution (<1% of latency). |
| **Token costs** | Process I/II: 50–200K tokens (input + output). Process III: ~50K. High due to repeated LLM routing of JSON-LD VCs. |

**Critical finding.** The prototype delegated security orchestration to the LLM via system prompts. Authors conclude this is **technically feasible but "at least questionable" for production**. They recommend moving VC/VP routing to **deterministic code** while keeping the LLM in charge of **policy decisions** (e.g., "should I disclose this VC?").

## ClawNet vs DID/VC — the architectural tradeoff

| Dimension | ClawNet (centralised) | DID/VC (decentralised) |
|---|---|---|
| **Identity binding** | Cloud orchestrator | Ledger-anchored DID |
| **Trust root** | Operator (single) | Ledger + issuer consensus (distributed) |
| **Policy updates** | Fast, operator-controlled | Slower, requires cross-domain negotiation / re-issuance |
| **Operator burden** | High (auth, key rotation, gateway containers) | Low (agents self-manage keys) |
| **Operator risk** | Single point of failure / trust | Eliminated |
| **Issuer governance** | Implicit (operator controls who issues) | **Explicit (must be pre-agreed; unsolved in the paper — eIDAS suggested as template)** |
| **Scalability** | Bottlenecked by orchestrator | Ledger-limited (DLT-dependent) |
| **Contact-graph metadata** | Held by orchestrator | Distributed across agent stores; ledger is public for DID docs |

**Neither is universally superior.** Decision factors:

- **Use a ClawNet-style architecture** when there is a trusted operator and fast policy updates matter (corporate internal agents, single-cooperative deployments).
- **Use DID/VC** when agent autonomy + multi-stakeholder interop matter (open ecosystems, federated cooperatives, cross-organisational consumer counter-power).

For the wiki's mandate — collective consumer counter-power that often spans multiple cooperatives, jurisdictions, and stakeholder classes — **DID/VC is the structurally aligned architecture**, with the open question of issuer governance as the primary unsolved problem. ClawNet's centralisation is acceptable only if the orchestrator is itself cooperatively owned (per [[clawnet-readout]] risk-mitigation guidance: "must be deployed under a [[platform-cooperatives|cooperative orchestration shell]]").

## Open governance problem — issuer trust

The DID/VC architecture eliminates the central operator but introduces a different governance burden: **who decides which issuers are trusted across domains?** The paper notes this remains unresolved and suggests **eIDAS** (EU Regulation 910/2014 — trusted-entity lists for cross-border digital identity) as a template, but does not solve it for AI agents.

For consumer counter-power deployment, this is the load-bearing open question. Candidate governance models:
1. **Standards-body curated** (W3C, ISO) — slow, conservative, may exclude novel issuer types.
2. **Federation-of-cooperatives curated** (analogous to [[coopcycle]] federation governance) — aligned with the wiki's exit-pathway lens but not yet demonstrated for issuer governance.
3. **Reputation-network curated** (web-of-trust, EigenTrust-style) — distributed but vulnerable to Sybil attacks.
4. **Regulatory-anchor curated** (NOYB-style strategic litigation forcing clarity, eIDAS-style government-curated lists) — most legible but jurisdiction-locked.

**No clear winner yet.** Worth flagging as a future research-queue topic.

## How this maps onto the wiki

| Wiki anchor | DID/VC connection |
|---|---|
| [[clawnet-readout]] | Direct architectural counterpart. ClawNet's risk #1 (centralised operator trust) is structurally addressed here. The page should present both architectures honestly with the decision factors above. |
| [[platform-cooperatives]] / [[coopcycle]] | The federation pattern is the natural governance shell for issuer-trust curation. |
| [[data-cooperatives]] | A data cooperative whose members hold DIDs and present VCs to negotiating counterparties is the structural fit. |
| [[collective-bargaining-for-data]] | A CBI's bargaining agents could issue VCs to member-controlled identity agents. |
| [[noyb]] | Strategic-litigation organisation whose litigation-agent must verifiably represent specific named members — DID/VC binding is the technical primitive. |
| [[agent-interop-protocols]] | A2A is the transport substrate. DID/VC is the identity layer. Both needed for trustworthy multi-agent deployment. |

## Caveats

1. **Issuer governance unsolved** — see open governance problem above.
2. **LLM-as-security-engine is unreliable** at current model capability (4–91% completion rates). Production deployments need deterministic security routing.
3. **Performance overhead** at 10–30s per cross-domain auth + 50–200K tokens is substantial — limits the deployment scenarios where this is acceptable (probably *not* per-transaction consumer interactions; *probably yes* per-session institutional collaboration).
4. **Ledger dependency.** Public-ledger DID anchoring (Hyperledger Indy in the prototype) requires DLT infrastructure with its own governance + sustainability questions.

## Keyring — first production-grade consumer reference implementation (April 2026)

The Garzon et al. prototype validates DID/VC architecturally but leaves the "is this user-deployable?" question open. **Keyring**, launched **April 16, 2026** by Harvard's **Applied Social Media Lab (ASML)** at the Berkman Klein Center for Internet & Society as part of an ASML-hosted digital-identity symposium, is the first answer in the affirmative. Repository: `github.com/berkmancenter/keyring-wallet`; project page: `asml.cyber.harvard.edu/advanced-digital-identity`. Co-built with the **Linux Foundation Decentralized Trust Graph Working Group**.

**What Keyring is.** An open-source mobile wallet that holds DIDs and W3C Verifiable Credentials on-device, authenticated via biometrics. Selective-disclosure presentations are the default — instead of presenting a birthdate to prove age-of-majority, Keyring presents a credential asserting *"holder is over 18"* without disclosing the birthdate; instead of disclosing a username to prove an account exists, it presents a credential asserting *"holder is the owner of an account at this domain"* without disclosing which account. No corporate intermediary holds the user's underlying personal data; verification proceeds peer-to-peer between the holder, the issuer, and the verifier.

**Why this matters relative to the Garzon et al. prototype.** Garzon et al. demonstrated DID/VC for *agent-to-agent* zero-trust authentication. Keyring deploys the same primitive for *human-to-service* identity verification — the consumer-facing layer. The architectural primitives (DID anchoring, VC issuance, Verifiable Presentation exchange via DIF specifications) are shared; the deployment context, latency budget, and threat model differ.

**The binding-constraint admission.** James Mickens (ASML PI, Gordon McKay Professor of Computer Science) and ASML's product team frame the technology as solved and the **institutional adoption problem as the actual bottleneck**: incumbents *"benefit a lot from owning and controlling your data"* (paraphrased from the ASML product leader's launch interview) — the same constraint this page already flags as "issuer governance unsolved." The Harvard Gazette write-up is the best-sourced public confirmation that the bottleneck for DID/VC-style architectures is incentive alignment of issuers, not the cryptography or the UX. The Linux Foundation Decentralized Trust co-authoring is one path toward that incentive alignment (multi-stakeholder governance over issuer eligibility and credential schemas).

**Wiki position.** Keyring is an *instance of*, not a new mechanism beyond, the W3C DID/VC pattern this page documents. It updates the "Caveats § 3 — Performance overhead" framing for the consumer-facing case (mobile native UX, on-device biometric, near-zero perceived latency for selective-disclosure presentations) and provides a concrete artefact reference for the wiki's exit-pathway and tech-enabled-solutions lenses.

**Source:** `raw/research/weekly-2026-05-04/01-01-keyring-berkman-klein-wallet.md` — Harvard Gazette, May 2026 ("Worried about how online firms use data they get from you?"). Coverage of the April 16 launch + ASML PI / product-leader interview. Trust tag: **moderate-high** — university press feature; Mickens and ASML team named with role and credential; primary GitHub repo and project URL given as cross-checks; institutional context (Berkman Klein, Linux Foundation Decentralized Trust) verifiable.

## Source

- Garzon, Vaziry, Kuzu, Gehrmann, Varkan & Gaballa. 2025. *AI Agents with Decentralized Identifiers and Verifiable Credentials*. arXiv 2511.02841. Technische Universität Berlin (Service-centric Networking / T-Labs). Captured: `raw/research/clawnet-adjacent-methods/23-ai-agents-did-vc-2025.md` + `12-ai-agents-did-vc-2025-abs.md`. Trust tag: arXiv preprint, single research group, prototype-validated.
- `raw/research/weekly-2026-05-04/01-01-keyring-berkman-klein-wallet.md` — Harvard Gazette, May 2026; coverage of the Berkman Klein / ASML Keyring wallet launch (April 16 2026). Trust tag: moderate-high.

**Foundational underpinnings referenced via the paper** — to cite directly when wiki claims are load-bearing:
- W3C Verifiable Credentials Data Model v2.0 (2024).
- W3C Decentralized Identifiers (DIDs) v1.0 (2022).
- DIF Presentation Exchange specification.
- DIF Credential Manifest specification.

## Related

- [[clawnet-readout]] — direct architectural counterpart
- [[agent-interop-protocols]] — A2A transport substrate (orthogonal layer)
- [[platform-cooperatives]] — natural governance shell for issuer-trust curation
- [[data-cooperatives]] / [[collective-bargaining-for-data]] / [[noyb]] — wiki-anchored use cases for member-bound identity
- [[federated-learning]] — complementary substrate (identity layer; FL is data-sharing layer)
