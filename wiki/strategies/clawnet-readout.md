# ClawNet Readout — Agent-Mediated Cross-User Coordination as Counter-Power Infrastructure

*(editorial / synthesis — 2026-04-25. Triggered by user `/query` asking how the ClawNet paper applies to this wiki. The paper itself is **not captured as a raw source**; the arXiv URL is the primary external reference. All wiki-anchor citations are reference-layer or strategy-layer pages the synthesis maps onto.)*

Editorial readout on **ClawNet** (Yang, Zhang, Jia, Song, Xue, Zhang & Guo 2026, HKUST / HKGAI / HKBU; arXiv 2604.19211 — *ClawNet: Human-Symbiotic Agent Network for Cross-User Autonomous Cooperation*) and its potential as **infrastructure for several wiki-flagged consumer-counter-power levers**. ClawNet is not itself a lever; it is a candidate technical substrate for the subset of [[possible-strategic-levers|inventory levers]] whose binding constraint is "credible scoped representation of distinct human interests with audit trail."

## What ClawNet contributes

Three governance primitives, instantiated as a deployed cloud-edge framework:

1. **Identity binding** — each agent permanently bound to exactly one human owner via progressive cognitive coupling (factual → pattern → value memory persisted across sessions). Provably represents a specific named individual.
2. **Scoped authorization** — the user's agent system splits into a privacy-preserving Manager Agent (architecturally barred from external messaging; aggregates across all identity agents) and N context-specific Identity Agents (each with own knowledge subset $\mathcal{K}_i \subset \mathcal{K}_u$, resource scope $\sigma_i$, and authorised-counterpart set $\mathcal{P}_i$). Cross-user collaboration requires bilateral human approval at every initiation; recursive delegation bounded by depth $d_{\max}$ with non-penetrable authorization boundaries.
3. **Action-level accountability** — every operation logged as $(o, u, I_u^i, \text{result}, t)$ to an append-only audit log; every mutative file action triggers automated pre-execution backup; owner-side single-step undo and batch rollback.

Architecture: cloud-side gateway containers (per user, multi-tenancy isolated) running the agent runtimes; edge-side node endpoint on the owner's device enforcing a second-layer file-whitelist ACL with fail-closed dual-layer evaluation. Worked example in the paper is cross-firm procurement (CN Tech buyer / US Nova-Semi supplier), but the primitives generalise to any multi-party negotiation with divergent owner interests.

## Where ClawNet maps onto the wiki's lever inventory

Mapping by structural fit, not endorsement. ClawNet adds value where the lever already requires (a) agents acting under verifiable per-individual mandate and (b) coordination across owners with non-aligned interests.

| Wiki anchor | What ClawNet substrates | Lever / strategy reference |
|---|---|---|
| [[data-cooperatives]] + [[collective-bargaining-for-data]] | A CBI agent that legibly negotiates on behalf of a named member without exposing aggregate member knowledge. Manager-Agent / Identity-Agent split is exactly the "coop holds the aggregate; per-context proxy speaks externally" pattern the CBI design lacks a substrate for. | [[possible-strategic-levers\|Lever #1 — many-consumer counterbalance]] |
| [[possible-strategic-levers\|Lever #14 (demand-strike coordinator)]] + [[possible-strategic-levers\|#16 (threshold-triggered flash campaigns)]] | Credible-commitment device. Bilateral approval + append-only audit produces verifiable evidence that agent A refused to purchase target T during window W under mandate M. Directly addresses the "research needed: commitment-device design" flag on both levers and resolves [[data-disruption-strategy-map\|open strategic question #3]]. | Levers #14, #16; [[data-disruption-strategy-map\|§Tier 1 #2]] |
| [[consumer-collective-bargaining]] (Tuángòu / Pinduoduo pattern) + group-buy coordinator | Recursive multi-party collaboration with depth bound. Bilateral approval is the trust analogue of Pinduoduo's "team of ≥5" social trigger — but works between strangers via agent-to-agent contact discovery + dual-side human gates rather than via a pre-existing WeChat social graph. | [[possible-strategic-levers\|Lever #4]] |
| [[data-disruption-strategy-map\|Tier 1 #1 — DSAR coordination infrastructure]] | Each member's identity agent issues DSARs with provable mandate; the dual-layer audit log + pre-execution backup *is* the templating + collection + pseudonymisation + aggregation infrastructure flagged as the missing build target in [[data-disruption-strategy-map\|§L3]]. The 258-driver Uber audit pipeline ([[pricing-algorithm-taxonomy]]) was bespoke; ClawNet generalises the substrate. Direct upgrade of [[possible-strategic-levers\|lever #9]] from "research needed" to "build candidate." | [[possible-strategic-levers\|Lever #9]] |
| [[markup-citizen-browser]] / probe-and-publish | Identity-bound agents executing audits with built-in attribution and audit trail map onto Citizen Browser's panelist-with-Trail-of-Bits-redaction architecture. ClawNet provides for free what Citizen Browser engineered bespoke (per-action attribution, owner-side rollback, dual-layer authorization). | [[possible-strategic-levers\|Lever #8]]; [[data-disruption-strategy-map\|§L4]] |
| [[noyb]] / consumer-union litigation | A standing consumer union's litigation agents must provably represent specific named members under specific mandate — ClawNet's identity-binding + scoped authorization is the technical primitive. | [[possible-strategic-levers\|Lever #26]] |

## Where ClawNet does **not** apply

ClawNet is *governance-aware and legible*. Several wiki-flagged levers are *adversarial and require illegibility*. These are architectural opposites.

| Wiki anchor | Why mismatch |
|---|---|
| [[obfuscation]], [[adversarial-data-poisoning]], [[browser-fingerprinting]], levers #6 / #7 / #10 / #11 | These rely on the agent being *unattributable* and the action being *unauditable*. ClawNet bakes in attribution and audit by architectural deterministic design, not by policy. Deploying ClawNet for these levers would make operator-side enforcement easier, not harder — every adversarial action is logged to a specific named owner. |
| [[pricing-algorithm-taxonomy\|Family 4 — airline RM]] and [[pricing-algorithm-taxonomy\|Family 5 — RealPage]] per [[data-disruption-strategy-map]] | Both ignore individual identity. Disruption requires population-aggregate timing or antitrust action, neither of which is an agent-mediated coordination problem. ClawNet adds nothing structural here. |

## Risks if deployed for consumer-counter-power use cases

1. **Centralised operator trust.** ClawNet's server-side orchestration, gateway containers, and L1 ACL all run as cloud services in the paper's reference deployment. This is a single-vendor trust assumption — same structural-risk pattern as the [[paypal-honey|Honey extractive-drift case]] catalogued on [[transparency-tools]]. Any consumer-counter-power deployment must own the orchestration layer (cooperative shell per [[platform-cooperatives]] / [[coopcycle]] federation pattern), not rent it. The paper notes cloud + edge can co-locate on a single physical machine for fully local deployment, which is the build-time hook for a coop-owned variant.
2. **Authenticated-endpoint automation = [[data-disruption-strategy-map|risk class 3 (CFAA "gates up")]].** ClawNet is OS-level with node-endpoint execution: agent actions cross authenticated boundaries (logged-in retailer accounts, cart operations, coupon application). Use must be scoped to public endpoints or to actions the user themselves is authorised to perform on their own account. The dual-layer ACL is a useful enforcement substrate for this discipline; it does not eliminate the underlying CFAA surface.
3. **Adversarial-training inoculation.** Once a pricing operator detects coordinated ClawNet-mediated behaviour by signature, [[data-disruption-strategy-map|risk class 5]] applies — model can be trained against the signature. Single-vendor architecture concentrates this risk; a federated multi-vendor deployment dilutes it.
4. **DP-as-firm-counter is orthogonal.** ClawNet does nothing about [[adversarial-data-poisoning|Solanki et al. 2025's DP-as-firm-counter result]] — a pricing operator training under differential privacy still suppresses ACA regardless of how the consumer-side coordination is structured. [[data-disruption-strategy-map|Risk class 6]] unchanged.
5. **Cross-user contact graph privacy.** ClawNet's collaboration network is itself a contact graph (owners' identity agents publish discoverable identity tags). The graph is metadata that a hostile actor or regulator could subpoena or pressure the orchestrator to surrender. The paper does not address graph-level privacy.

## Empirical capability evidence (added 2026-04-26)

The original readout above describes the *governance shape* ClawNet provides. Two recent benchmarks now constrain the *capability assumption* underlying it: whether LLM agents can actually execute the negotiation / coordination behaviour required for ClawNet to deliver counter-power. Both anchored on the new mechanism page [[agent-mediated-negotiation-empirics]].

- **AgenticPay (Liu, Gu & Song 2026, arXiv 2602.06008).** Frontier proprietary models (Claude Opus 4.5: 86.9 GlobalScore, 100% deal rate, 3.7 avg rounds; GPT-5.2 / Gemini-3-Flash similar) negotiate competently. Open-weight models fail at the "last mile" (Llama-3.1-8B: 32.5 score, 48.6% timeout; >40% of Qwen / Llama failures occur when price gap is *<$5*). **Universal buyer disadvantage at the frontier**: all models showed 20–40+ point gaps favouring SellerScores over BuyerScores ("persuasive selling content predominates over strategic purchasing guidance" in training data). Financial Asset negotiation drops all models 10–20 points from Professional Services baseline.
- **LLM-Deliberation (Abdelnabi et al. 2024, NeurIPS Datasets & Benchmarks; arXiv 2309.17234).** GPT-4 cooperative-success 81% → 27% with one greedy adversarial agent. Heterogeneous coalitions worse than uniform-strong (weak-model members drag down strong ones). Score-leakage 25% in GPT-3.5; theory-of-mind capacity ~42% / ~61% for GPT-3.5 / GPT-4.

**Implications for this readout.**

1. **Frontier capability is real but proprietary.** A privacy- or decentralisation-motivated deployment insisting on open-weight models will face open-weight failure modes. Cooperative deployments using a frontier model concentrate vendor dependency.
2. **Buyer disadvantage is structural and inherits into ClawNet.** Off-the-shelf agents systematically advantage sellers in price negotiation. **A consumer-counter-power deployment using uncalibrated agents will amplify the very asymmetry the wiki's mandate is to combat.** Mitigation candidates: domain-specific fine-tuning, human-in-loop oversight for buyer-side concessions, asymmetric agent-strength budgeting.
3. **Adversarial collapse threatens consumer-firm negotiation.** Consumer-firm negotiation is *inherently* adversarial. The Abdelnabi 81%→27% collapse maps directly onto the realistic case. Mitigations: cryptographic commitments, formal verification, **shift away from strategic negotiation toward information aggregation** (DSAR coordination, probe-and-publish — exactly the [[data-disruption-strategy-map|Tier 1 #1]] lever this readout already foregrounds).
4. **Heterogeneity penalty constrains coalitional design.** A cooperative whose members run different LLMs faces the heterogeneity penalty.
5. **DSAR / aggregation use cases are structurally favoured.** They are not negotiations — they are information aggregation under provable mandate. Current LLM agent capability is *better* fitted to this than to direct buyer-seller bargaining.

Net effect on the readout: the core fit (DSAR coordination, commitment device, CBI representation, group-buy) is reinforced; the negotiation-heavy applications (e.g., complex contract negotiation) carry an additional capability caveat.

## Substrate dependencies (added 2026-04-26)

ClawNet is presented as a *governance overlay* on Google's A2A protocol. A2A's structural security gaps are *inherited* by ClawNet — the policy layer cannot fully remediate substrate-layer weaknesses. Anchored on [[agent-interop-protocols]] (Louck, Stulman & Dvir 2025, arXiv 2505.12490).

**Six A2A-layer gaps documented:**
1. Token lifetimes are implementation-dependent, not protocol-enforced (CVE-2025-1198 token replay).
2. No strong customer authentication (SCA) for high-risk actions (CWE-306).
3. Coarse-grained OAuth scopes (18.5% of OAuth deployments empirically over-permissioned).
4. No protocol-defined explicit user consent flow (GDPR Article 7 + PSD2 gap).
5. Excessive exposure of data to intermediary agents.
6. Prompt injection achieves 60–100% leakage against baseline implementations; direct user-to-service flow + ephemeral tokens drops to 0%.

**Implication for this readout's risk catalogue.** The original "centralised operator trust" and "contact-graph metadata" risks have A2A-layer counterparts (token-management, scope-granularity). Consumer-counter-power deployments must combine ClawNet's governance overlay with A2A-protocol enhancements per Louck et al. — co-dependent system, not standalone.

## Centralised vs decentralised — ClawNet vs DID/VC (added 2026-04-26)

The "centralised operator trust" risk flagged as #1 in the risk catalogue above has a structural alternative: W3C Decentralized Identifiers (DID) + Verifiable Credentials (VC). Anchored on [[decentralized-agent-identity]] (Garzon et al. 2025, arXiv 2511.02841).

| Dimension | ClawNet (centralised) | DID/VC (decentralised) |
|---|---|---|
| Identity binding | Cloud orchestrator | Ledger-anchored DID |
| Trust root | Operator (single) | Ledger + issuer consensus (distributed) |
| Policy updates | Fast, operator-controlled | Slower, requires cross-domain re-issuance |
| Operator burden | High | Low (agents self-manage) |
| Operator risk | Single point of failure / trust | Eliminated |
| Issuer governance | Implicit | **Explicit (unsolved; eIDAS suggested as template)** |
| Contact-graph metadata | Held by orchestrator | Distributed (DLT public for DID docs) |

**Decision factors for consumer-counter-power use:**

- ClawNet-style centralised architecture is acceptable *only if the orchestrator is itself cooperatively owned* (per the original readout's "must be deployed under a [[platform-cooperatives|cooperative orchestration shell]]" guidance). Single-vendor cloud deployment is the [[paypal-honey|Honey extractive-drift pattern]].
- DID/VC is the structurally aligned architecture for *open ecosystems spanning multiple cooperatives, jurisdictions, stakeholder classes* — i.e., the wiki's typical mandate context.
- DID/VC's open governance problem (issuer trust curation) is the load-bearing remaining question. Candidate models: standards-body curated, federation-of-cooperatives curated, reputation-network curated, regulatory-anchor curated. No clear winner.

The two architectures are not strictly substitutes — a cooperative-owned ClawNet variant deployed *over* a DID/VC identity layer combines the governance ergonomics of ClawNet with the operator-trust elimination of DID/VC. This hybrid is not yet captured in the literature; flagging as a future research-queue topic.

## Net read

ClawNet is the right *infrastructure shape* for the multi-party-with-divergent-interests subset of the lever inventory — specifically [[data-disruption-strategy-map|Tier 1 #1 (DSAR coordination)]], [[possible-strategic-levers|levers #14 and #16 (commitment device for coordinated collective abstention)]], [[possible-strategic-levers|lever #1 (CBI agent representation)]], and [[possible-strategic-levers|lever #4 (group-buy coordinator)]]. It is *wrong-shape* for the obfuscation / adversarial-data-poisoning cluster. A **cooperatively-owned** ClawNet-style substrate (orchestration governed under a [[platform-cooperatives|platform coop]] shell, not the original cloud vendor) could become the missing technical layer for the [[data-cooperatives]] / [[collective-bargaining-for-data]] / [[platform-cooperatives]] convergence the wiki has been circling — agent-mediated cross-consumer coordination as the substrate all three mechanisms have separately needed but none has built.

The follow-on move this surfaces: **agent-mediated coordination as a cross-cutting infrastructure pattern in the lever inventory**, not just a per-lever technique. Worth treating as a candidate "pattern" entry under the future [[strategies/index|strategy-layer pattern library]] subsection once development plans mature.

## Source

External paper, **not captured as a raw source** on this wiki:

- Yang, Zhang, Jia, Song, Xue, Zhang & Guo. 2026. *ClawNet: Human-Symbiotic Agent Network for Cross-User Autonomous Cooperation*. arXiv 2604.19211. <https://huggingface.co/papers/2604.19211>. *Trust tag:* preprint, single research group (HKUST / HKGAI / HKBU), one cross-firm procurement use case demonstrated, no third-party deployment evidence. Treat as a paradigm proposal with a working prototype, not a battle-tested production pattern. Future `/ingest` could capture it formally if the synthesis grows into a development plan.

Wiki-internal anchors cited inline throughout. The synthesis itself is editorial — it maps an external paradigm onto wiki-documented levers and is not derivable from the captured reference layer alone.

## Related

- [[possible-strategic-levers]] — lever inventory this readout maps onto
- [[data-disruption-strategy-map]] — strategy matrix this readout extends (Tier 1 #1 + open question #3 in particular)
- [[obfuscation-strategic-readout]] — sister readout (where ClawNet does *not* apply)
- [[lever-implementation-readout]] — sister readout on H1–H4 lever implementations
- [[agent-mediated-negotiation-empirics]] — empirical capability evidence (D1 AgenticPay + D2 Abdelnabi LLM-Deliberation)
- [[agent-interop-protocols]] — A2A substrate-protocol security gaps + mitigations
- [[decentralized-agent-identity]] — DID/VC alternative to ClawNet's centralised architecture
- [[data-cooperatives]] — primary infrastructure-level fit
- [[collective-bargaining-for-data]] — primary infrastructure-level fit
- [[federated-learning]] — substrate technology that addresses the "centralised operator trust" risk
- [[platform-cooperatives]] — required shell for any non-extractive deployment
- [[markup-citizen-browser]] — closest existing audit-infrastructure precedent
- [[buyer-cartels-antitrust]] — antitrust frame for any agent-mediated buyer-side coordination
