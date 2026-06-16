# Dignity-Centric Stack

A commons-governed, horizontally federated AI architecture that maps six normative dimensions of a human-dignity digital social contract onto six infrastructure layers. The central mechanism is a decoupling of capital from control — the stack operates as a "shared civic battery" charged by many contributors but steered by none in proportion to their contribution. It is State-agnostic rather than anti-State, drawing on cooperative, mutualist, and libertarian-municipalist traditions, and is designed as a parallel federated institution that any person, firm, or State may use and fund while governance remains polycentric and subsidiary. The paper proves the architecture formally defeats capture through votes or surplus accumulation, and analyzes the harder problem of structural capture (dominant supplier withdrawal), which it argues is only resisted insofar as operational supply at each layer is polycentric and substitutable.

## Source

- [The Dignity-Centric Stack: A Commons-Governed, Horizontally Federated Architecture for Human-Dignity AI](https://arxiv.org/abs/2606.06083) — Eduardo C. Garrido-Merchán; arXiv:2606.06083 [cs.CY], submitted 4 Jun 2026. Academic preprint aimed at AI governance and cooperative infrastructure designers. No code released. Trust: peer-reviewed preprint, abstract captured; PDF full text not extracted (image-only capture).

## Architecture

The paper constructs the "Dignity Stack" by mapping each of the six governance dimensions from the human-dignity digital social contract onto a corresponding layer of commons-governed AI infrastructure. Protocols are drawn from the Liberation Stack framework.

### Six Governance Dimensions (mapped to layers)

The six dimensions originate in prior work on the human-dignity-centric digital social contract; the paper's contribution is operationalizing each as an infrastructure layer rather than as externally-imposed regulation:

1. **Technological oversight** — commons-governed monitoring and auditability layer
2. **Automation limits** — protocol-level enforcement of human-in-the-loop constraints
3. **Economic justice** — cooperative ownership structures that decouple capital contribution from governance power
4. **Political legitimacy** — horizontal, polycentric, subsidiary decision-making (no single actor steers proportional to stake)
5. **Social cohesion** — mutualist and libertarian-municipalist participation mechanisms
6. **Legal guarantees** — layer-level implementation of data sovereignty and personalism, not dependent on State enforcement

### Capital-Control Decoupling

The "civic battery" device is the paper's central formal claim: contributors charge the stack (provide compute, data, funding) but governance is not allocated proportional to contribution. The paper provides a formal proof that this structure defeats capture via vote-buying or surplus extraction.

### Structural Capture Analysis

The paper distinguishes two capture modes:

- **Formal capture** (votes, surplus): defeated by the governance design
- **Structural capture** (dominant supplier withdraws supply): resisted only if operational supply at each layer is polycentric and substitutable. The paper explicitly notes this condition is "demanding at the lower layers and perhaps presently unattainable at chip fabrication" — an honest acknowledgment that silicon supply chains are a hard constraint outside the cooperative's control

## Relationship to Prior Frameworks

The architecture explicitly draws from the **Liberation Stack** framework for its layer protocols. It positions itself relative to the human-dignity digital social contract literature by arguing that commons governance realizes the contract's values more faithfully than the regulatory enforcement the contract presupposes.

## Implementation Status

No code or reference implementation released as of capture date (2026-06-15). The paper is architectural and normative; it provides formal proofs of governance properties rather than runnable software.

## Exit-Pathway Relevance

This is a specification-level exit-pathway architecture: it describes what a cooperative alternative to centralized cloud AI would need to look like at each governance layer, not just what rules regulators should impose on existing providers. The formal capture-resistance proof and the honest structural-capture caveat (chip fabrication) make it a useful reference for any collective intending to build parallel AI infrastructure rather than lobby for reform of existing infrastructure.

## Related

- [[solidarity-stack-readout]] — 7-layer cooperative AI counter-architecture (Scholz); the Dignity Stack shares the layered federated framing and draws on Liberation Stack protocols referenced in that work
- [[platform-cooperatives]] — cooperative governance model that the economic justice and political legitimacy layers operationalize
- [[data-cooperatives]] — member-owned data stewardship; the data sovereignty layer is a direct overlap
- [[federated-learning]] — substrate technology for the horizontally federated compute layers
- [[decentralized-agent-identity]] — DID/VC mechanisms relevant to the technological oversight and legal guarantees layers
- [[collective-bargaining-for-data]] — data governance approaches that the stack's economic justice layer aims to encode structurally rather than contractually
- [[the-firms-view]] — counter-perspective on cooperative AI infrastructure from the incumbent provider standpoint
