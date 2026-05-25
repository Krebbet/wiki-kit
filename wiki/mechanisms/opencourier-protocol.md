# OpenCourier Protocol

**OpenCourier** is an open interoperability protocol for community-owned last-mile delivery platforms, introduced by the **Platform Cooperativism Consortium** (PCC) blog and a CHI '26 Extended Abstracts vision paper (Liu, Rao, Hwang, Vertesi & Monroy-Hernández, arXiv 2511.02455 v2, Mar 27 2026). Co-built with the **Workers' Algorithm Observatory (WAO)** at Princeton — the same group behind [[drivers-seat-cooperative|FairFare]], the rideshare-trip crowdsource. The protocol defines data formats and communication across a decentralised network of **Courier Instances** (cooperatively-owned platforms), **Courier Apps** (mobile clients), and **Service Requesters** (restaurants/retailers). Its load-bearing contribution to this wiki: it is the first **courier-facing** protocol stack to ship a working reference implementation (multiplatform mobile app + backend + instance-selection dashboard at `opencourier.cs.princeton.edu`) — explicitly contrasted with the established **customer-vendor** protocol [Beckn](https://becknprotocol.io/) — and the first to put **federation across instances** (cross-instance courier mobility) into the protocol primitive rather than at the application layer. This addresses the "white-labeled software is costly and hard to customize" problem the paper identifies as the binding constraint on the hundreds of local independent delivery platforms that have emerged.

## Three-layer architecture

OpenCourier defines endpoints across three interaction layers:

| Layer | Endpoints | Function |
|---|---|---|
| **Registry** | Courier-Instance discovery | A curated directory of Courier Instances. A courier (or an app on their behalf) queries a Registry to find instances aligned with their values / geography / working preferences. **Many registries can exist independently.** A Restaurant/Retailer also queries Registry to find Courier Instances that can fulfil a delivery task. |
| **App-Instance** | Courier ↔ Instance | Couriers receive and manage jobs from the instance(s) they are members of. A Courier Instance can develop its own app or use third-party apps that implement the layer. The reference Courier Client collects worker preferences (earnings-calculation method, weight limits, etc.) — a deliberate design choice to surface non-speed allocation criteria. |
| **Instance-Requester** | Instance ↔ Restaurant/Retailer | Negotiation via quotes + open text. Restaurants/Retailers broadcast a delivery task to multiple Courier Instances (queried via Registry) and pick one. **Also exposes instance-level data to third-party researchers / regulators** for auditing (e.g., calculating average hourly rates across the ecosystem). |

## Three stated goals

The protocol's three named goals (from the PCC blog) are the courier-facing translation of the wiki's familiar information-asymmetry / power-imbalance / values-alignment framing:

1. **Enabling value alignment** — couriers can choose which instance(s) to join based on their working preferences and the instance's values.
2. **Correcting information asymmetries** — mandated disclosure of key information across instances + standardised data formats for third-party auditing.
3. **Reducing power imbalances** — open-source development; shared tools and innovations benefit all ecosystem stakeholders.

These goals map directly onto the [[possible-strategic-levers]] inventory (information layer + economic-structural) — but uniquely at a *protocol-substrate* layer rather than an application or campaign layer.

## Reference implementation

Working code shipped with the protocol announcement:

- **Demonstration backend**: `opencourier.cs.princeton.edu` — a dummy Courier Instance.
- **Multiplatform mobile Courier Client**: shows instance-selection UI; lets couriers join one or multiple instances; collects worker-preference inputs.
- **Admin dashboard**: instance-level governance interface.
- **License**: open-source (the blog explicitly invites contributors).

The reference Client is positioned as a *normative* artifact — i.e., its UI surfaces (worker-preference collection, multi-instance management) are intended to "make new norms or ways of organizing among couriers" rather than just demonstrate technical feasibility.

## Federation primitive — the key contrast with FairFare

OpenCourier's federation primitive — *a courier can move across Courier Instances without rebuilding their data, reputation, or app* — is the architectural feature that distinguishes it from prior counter-power tooling in this domain.

- **[[drivers-seat-cooperative|FairFare]] / WAO** (same team): centralised crowdsource — drivers submit gig-app screenshots and trip data to a single research-controlled aggregator (~1M trips collected across the US in collaboration with labour orgs). Useful for auditing and advocacy but does not by construction enable courier mobility across competing platforms; couriers remain tied to incumbents.
- **OpenCourier**: federated by protocol. Couriers' home instance is their own cooperative; the Registry layer makes other instances discoverable; the App-Instance layer lets one client serve multiple instances. Cross-instance mobility *is the substrate*, not an application feature.

In wiki-terms this is a CoopCycle-style federation pattern ([[coopcycle]] — "the second-level cooperative for shared tech / marketing / R&D" answer to the [[platform-cooperatives|platform-coop capital conundrum]]) but raised one layer of abstraction — from a single shared software stack (CoopCycle's GPL-licensed platform) to an open protocol that any compliant stack can implement. CoopCycle is one possible OpenCourier implementation; competing-implementation diversity is welcomed.

## Distinction from Beckn

The blog is explicit that OpenCourier is **not** a competitor to Beckn — they cover different ecosystem slices:

| Protocol | Counter-party pair | Scope |
|---|---|---|
| **Beckn** | Customer ↔ Vendor (restaurant/retailer) | E-commerce ordering protocol; the existing open framework for customer-side interoperability. |
| **OpenCourier** | Courier ↔ Instance ↔ Vendor | Last-mile delivery, courier-facing. |

This filling of the **courier-facing protocol gap** is the paper's stated reason for the project. A complete decentralised gig-economy stack would compose Beckn (customer-vendor) with OpenCourier (vendor-courier).

## Authorship and institutional anchoring

- **Authors** (per arXiv 2511.02455v2 and the PCC blog by-line): Yuhan Liu, Varun Nagaraj Rao, Sohyeon Hwang, Janet Vertesi (Sociology), Andrés Monroy-Hernández (CS) — Princeton University. Sohyeon Hwang is affiliated with the Center for Information Technology Policy.
- **Published venue**: vision paper accepted at **CHI '26 Extended Abstracts** (Barcelona); v1 submitted Nov 4 2025, v2 revised Mar 27 2026 (DOI 10.1145/3772363.3799319).
- **Sibling project**: WAO ([[drivers-seat-cooperative]] sunset → activity migrated to WAO; FairFare for rideshare).
- **Publishing venue (blog)**: Platform Cooperativism Consortium / The New School — the same institutional home as the [[platform-cooperatives|platform-cooperativism movement]] anchor [[solidarity-stack-readout|Trebor Scholz's Solidarity Stack]].

## Limits and caveats

- **Vision paper, not yet ratified standard.** Both the arXiv paper title ("an Open Protocol for Building...") and the PCC blog's "we are developing" framing acknowledge the protocol is **proposed, not standardised**. No multi-implementation interoperability has been demonstrated. The CHI '26 venue is *Extended Abstracts*, not a full track.
- **Reference implementation is a Princeton-hosted demo.** As of the PCC blog post (2026-05-08 window), `opencourier.cs.princeton.edu` is described as a "dummy Courier Instance" — i.e., not a production deployment with paying couriers and live customers.
- **No documented Registry-layer trust model.** The blog leaves open who runs Registries and how registry-issuer accountability works. (Compare the equivalent unsolved problem on [[decentralized-agent-identity]] — issuer governance.) Multiple registries existing in parallel is a goal, but the protocol does not say how a courier judges which registry is reputable.
- **Antitrust treatment of cross-instance courier coordination is not addressed.** Per [[buyer-cartels-antitrust]], when worker cooperatives federate via shared standards, the line between legitimate cooperation (per-jurisdiction safe harbours) and coordinated price-setting can become load-bearing. The PCC blog does not engage this dimension.
- **No empirical evaluation yet.** Unlike the [[agent-mediated-negotiation-empirics|AgenticPay]] / Abdelnabi-style negotiation papers or [[decentralized-agent-identity|Garzon et al.]]'s 100-trial DID/VC prototype, OpenCourier ships an architecture and a demo but no measured outcomes (e.g., courier earnings uplift, instance-switching cost). A live deployment with measured outcomes would be the natural next-research-cycle ingestion target.

## How this maps onto the wiki

| Wiki anchor | Connection |
|---|---|
| [[platform-cooperatives]] | OpenCourier is the **protocol-substrate** layer that the federation-as-scaling pattern (the OECD-named answer to the capital conundrum) was missing. Adds a fifth structural pattern to the section below "Industries where platform coops have traction": *protocol-driven federation* alongside CoopCycle's single-implementation-federation. |
| [[coopcycle]] | CoopCycle is a single-implementation bike-delivery federation; OpenCourier is the protocol-layer abstraction that would let CoopCycle interoperate with non-CoopCycle delivery coops. Direct architectural-evolution path. |
| [[drivers-cooperative]] | Rideshare-facing analogue. OpenCourier focuses on couriers (last-mile delivery), but the same authoring team's prior work ([[drivers-seat-cooperative|FairFare]]) targeted rideshare. A rideshare-equivalent OpenCourier ("OpenDriver"?) would be the natural extension. |
| [[drivers-seat-cooperative]] | Same authoring team (Liu, Rao, Hwang, Vertesi, Monroy-Hernández are Princeton WAO researchers; FairFare is a WAO project). OpenCourier is the substrate-layer evolution of WAO's centralised-aggregator approach. |
| [[agent-interop-protocols]] | Substrate analogue — both are open interop protocols (A2A for agent-to-agent, OpenCourier for courier-to-instance-to-requester). A2A's security gaps catalogue is the closest existing protocol-layer caveat catalogue and points to the kinds of issues OpenCourier will face (token lifetime, scope granularity, SCA absence) when it moves from demo to production. |
| [[decentralized-agent-identity]] | Issuer-governance problem mirrored: DID/VC unsolved at the credential-issuer level; OpenCourier unsolved at the Registry-issuer level. |
| [[solidarity-stack-readout]] | OpenCourier sits in Scholz's "Application" layer of the Solidarity Stack — the cooperatively-owned application layer above Data and Algorithms. Working evidence of an Application-layer cooperative protocol with reference implementation. |
| [[mechanism-synthesis-readout|Build #6 — Layered Cooperative Governance]] | OpenCourier's Registry / App-Instance / Instance-Requester separation is one concrete shape of the layered-governance idea: governance happens at the *instance* level (each cooperative self-governs); coordination happens at the *protocol* level (open standard); discovery happens at the *registry* level. Direct architectural input. |
| [[possible-strategic-levers]] | Reinforces the cross-cutting-infrastructure subsection's "protocol-layer cooperative coordination" entry. Concrete worked example. |
| [[bharat-taxi]] | State-sponsored alternative-typology case. OpenCourier represents the *grassroots-protocol* path; Bharat Taxi represents the *state-capitalised* path. Both address the platform-coop capital conundrum, but via opposite institutional logics. |

## Open questions for the wiki

1. **Registry governance**: who runs the directory, how is trustworthiness established, and how is the registry-operator captured? Unsolved in the published material.
2. **Cross-instance courier identity portability**: does the protocol carry portable courier reputation / rating / work-history across instances? Not addressed in the blog. A YES answer would make OpenCourier substantively more valuable to couriers; a NO answer makes the federation primitive lighter than it looks.
3. **Composition with Beckn**: the blog claims the two are complementary. A composed Beckn+OpenCourier end-to-end ordering flow has not been demonstrated.
4. **Antitrust posture for cross-instance pricing coordination**: the OECD-2022 safe-harbour thresholds documented on [[buyer-cartels-antitrust]] are tighter than what a national-scale federation of courier cooperatives might naturally span. Open.
5. **Real-deployment readout**: when (if) a production-grade instance emerges, capture comparative numbers vs incumbent Uber Eats / DoorDash / Grubhub on courier earnings, fee structure, and instance-switching rates.

## Source

- `raw/research/weekly-2026-05-11/01-opencourier-protocol.md`
  - **Origin**: Platform Cooperativism Consortium blog — [https://platform.coop/blog/toward-worker-owned-delivery-platforms-with-the-opencourier-protocol/](https://platform.coop/blog/toward-worker-owned-delivery-platforms-with-the-opencourier-protocol/). Captured 2026-05-11.
  - **Audience**: platform-coop community, potential contributors, labour orgs, researchers.
  - **Purpose**: announce the OpenCourier protocol; invite contributors; describe architecture and goals.
  - **Trust**: primary movement publication; co-authored by Princeton WAO researchers with prior credibility ([[drivers-seat-cooperative|FairFare]]).
- `raw/research/weekly-2026-05-11/07-opencourier-paper.md`
  - **Origin**: arXiv 2511.02455 abstract page — Liu, Rao, Hwang, Vertesi, Monroy-Hernández. *OpenCourier: an Open Protocol for Building a Decentralized Ecosystem of Community-owned Delivery Platforms*. v1 4 Nov 2025; v2 27 Mar 2026. CHI '26 EA Barcelona. DOI 10.1145/3772363.3799319.
  - **Audience**: HCI / Cooperative AI / CHI '26 academic audience.
  - **Purpose**: vision paper; blueprint for decentralised delivery network with open protocol.
  - **Trust**: peer-reviewed-track Extended Abstract (CHI EA review tier — lighter than full track); single-team paper; consistent with the same team's prior empirical work on FairFare.

## Related

- [[platform-cooperatives]]
- [[coopcycle]]
- [[drivers-cooperative]]
- [[drivers-seat-cooperative]]
- [[agent-interop-protocols]]
- [[decentralized-agent-identity]]
- [[solidarity-stack-readout]]
- [[mechanism-synthesis-readout]]
- [[possible-strategic-levers]]
- [[bharat-taxi]]
- [[buyer-cartels-antitrust]]
