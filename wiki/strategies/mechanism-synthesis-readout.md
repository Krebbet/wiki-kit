# Mechanism Synthesis Readout — Novel Builds Across the New Mechanism Set

*(editorial / synthesis — 2026-04-26. Triggered by user `/query`: "with all the new methods now in the wiki, how would you novelly apply technology / algorithms to enable some of our identified levers — are there new avenues to consider?" All substantive cross-mechanism combinations are tagged *(editorial)* / *(synthesis)*; reference-layer claims cite the underlying mechanism pages.)*

The 2026-04-26 `clawnet-adjacent-methods` research run added 10 new mechanism-layer pages: [[algorithmic-collective-action]], [[strategic-classification]], [[the-firms-view]], [[federated-learning]], [[complex-contagion]], [[buyer-cartels-antitrust]], [[data-market-mechanism-design]], [[decentralized-agent-identity]], [[agent-mediated-negotiation-empirics]], [[agent-interop-protocols]]. Most of the wiki's 29-lever inventory on [[possible-strategic-levers]] was specified *before* these substrates landed. This readout systematically walks the cross-product — what becomes buildable when these new mechanism pages are composed onto existing levers, and which combinations surface candidate new levers not yet on the inventory.

## How to read this page

- **§Eight novel applications** — concrete builds combining 2+ new mechanism pages onto existing inventory levers. Each names the substrate combination, the lever it enables / reframes, and the design rationale.
- **§Five candidate new lever avenues** — synthesis-surfaced lever proposals not currently on [[possible-strategic-levers]]. Each is a *(editorial)* proposal worth considering for inventory addition.
- **§Hard limits the new mechanism set imposes** — honest constraints. Some of the new pages document defensive-side dynamics that bound what's buildable.
- **§Build-portfolio recommendation** — opinionated tier ranking across the eight builds.

---

## Eight novel applications to existing levers

### 1. Federated Pricing Observatory

**Combines:** [[federated-learning]] + [[markup-citizen-browser]] + [[transparency-tools]].
**Enables:** [[possible-strategic-levers|lever #8 (coordinated probe-and-publish)]], [[data-disruption-strategy-map|Tier 1 #3 (public-endpoint probe-and-publish observatory)]].

**Design.** Panelists run a probing client locally (analogous to [[markup-citizen-browser|Markup Citizen Browser]]'s desktop app); the client trains a local model of the seller's pricing function on the panelist's own data. Only model-update gradients leave the device, aggregated via secure aggregation per [[federated-learning|Bonawitz et al. 2017]]. The central observatory never sees raw browsing or per-session pricing data; the public output is the aggregated pricing-function model.

**Why this matters.** The Markup Citizen Browser's Trail of Bits-audited redaction pipeline is a substantial engineering investment specifically because the central data store contains raw panelist data. Federated learning makes the same goal a *substrate-level property* — there is no raw central store to redact. Privacy-by-architecture rather than privacy-by-promise. This is the same Honey-pattern protection the [[paypal-honey|extractive-drift case]] argues for.

**Limits.** Statistical heterogeneity (non-IID panelist data) degrades convergence per the [[federated-learning|FL survey]]. The aggregated model still leaks aggregate distribution information — DP-SGD adds calibrated noise but at accuracy cost. Cross-link [[the-firms-view|§5]] for the dual-use Byzantine-robustness consideration: the aggregator must defend against firm-side false-update injection.

**Substrate update (2026-04-27).** The EU Commission's preliminary DMA findings on **Google search-data sharing** (April 16, 2026; consultation closes May 1; final decision expected July 27) propose a **mandated FRAND data-access regime** for ranking, query, click, and view data — with AI chatbots explicitly named as eligible "data beneficiaries." If finalised, this is a candidate **regulated-access substrate** for Build #1: ranking/click data under FRAND terms could provide grounded search-intent signals that a federated observatory otherwise has no clean way to obtain, and the regulated-access surface lowers the adversarial data-acquisition cost the build currently has to assume. The trade-off is regulator-set vs cooperative pricing — see [[regulatory-responses|EU DMA Google search-data sharing]] for full mechanism, and [[mechanisms/data-market-mechanism-design]] for the cooperative-pricing alternative. **Watch:** July 27 2026 final decision; the public consultation is open input now.

### 2. Verifiable Mandate-Bound DSAR Pipeline

**Combines:** [[decentralized-agent-identity]] + [[clawnet-readout]] + [[data-disruption-strategy-map|Tier 1 #1]].
**Enables:** [[possible-strategic-levers|lever #9 (collective training-data withdrawal)]] — the upgrade from "research needed" to "build candidate" already flagged on the lever inventory.

**Design.** Each member of a DSAR coordination platform holds a W3C DID per [[decentralized-agent-identity|Garzon et al. 2025]]. The member's identity agent issues DSAR requests under a Verifiable Credential proving the agent acts on behalf of the named user with explicit mandate scope (e.g., "request data from Acxiom on behalf of holder of DID:abc, scoped to date range X–Y, signed at time T"). Receiving operator gets a request signed by the user's DID with attached VC; can verify mandate cryptographically without a phone call to the user. Aggregator collects responses tied to anonymised DIDs (member identifies as DID:abc to the operator; aggregator only knows the response is from a member, not which one).

**Why this matters.** The Uber audit ([[pricing-algorithm-taxonomy|258-driver DSAR coordination]]) was bespoke per-driver paperwork. Mandate verification was manual and the bottleneck. DID/VC primitives turn "is this a legitimate request?" from operator-side friction into a one-line cryptographic check. The asymmetry is structural: each marginal member adds near-zero operator-friction cost; current-generation DSAR coordination is roughly linear in operator-side workload.

**Limits.** Issuer-trust governance is unsolved per [[decentralized-agent-identity|Garzon et al.'s open governance problem]] — operators must agree out-of-band which DID issuers they trust. Once that is solved (eIDAS-style, federation-of-cooperatives, or similar), this build is structurally low-risk per [[data-disruption-strategy-map|risk class 1]]. **DSAR / aggregation use cases sidestep [[agent-mediated-negotiation-empirics|the LLM negotiation buyer-disadvantage]]** — there is no negotiation, only attested information request.

### 3. Multi-Collective Adaptive-Pricing Disruption

**Combines:** [[strategic-classification]] (B2 *Contextual Dynamic Pricing with Strategic Buyers* result) + [[algorithmic-collective-action]] (Karan 2025 two-collectives result).
**Enables:** [[possible-strategic-levers|lever #10 (adversarial training-data injection)]]; partial mitigation of [[the-firms-view|§3 adaptive-seller recovery]].

**Design.** [[the-firms-view|§3]] says adaptive sellers can recover Õ(√T) regret against feature manipulation by inferring a *single* buyer-equilibrium manipulation rule **x_t = x_t⁰ − A⁻¹β₀g'(·)** and pricing accordingly. [[algorithmic-collective-action|Karan et al. 2025]] showed two collectives with *aligned* objectives can reinforce each other while two with *conflicting* objectives suppress each other ≤75%. Synthesis: deploy two (or more) aligned collectives that use *structurally different* manipulation rules — say, Collective A rotates demographic signals, Collective B rotates session/timing signals — so the seller faces an identification problem. There is no single rule to invert; the seller's two-phase exploit cannot recover from exploring *one* rule.

**Why this matters.** Single-collective ACA against an adaptive seller has finite effectiveness per [[the-firms-view|§3]]. Multi-collective with aligned-objective / different-rule design is the only currently-documented architectural counter that doesn't depend on the firm not adopting DP (per [[the-firms-view|§2]]). It directly answers Karan et al.'s constructiveness-score open question for adversarial pricing settings.

**Limits.** Karan 2025's empirical work is on resume classification and recsys, not pricing; the multi-collective-against-adaptive-pricing synthesis is theoretical. DP-as-firm-counter ([[the-firms-view|§2]]) still suppresses both collectives if adopted. Coordination cost across collectives is high — likely needs the [[buyer-cartels-antitrust|joint-purchasing antitrust frame]] for legal cover.

### 4. Periphery-First Threshold Coordinator

**Combines:** [[complex-contagion]] (Centola periphery-vs-influencer + wide-bridge results) + Kickstarter pattern from [[possible-strategic-levers|lever #16]] + [[clawnet-readout]] commitment-device substrate.
**Enables:** [[possible-strategic-levers|levers #14 (demand-strike), #16 (threshold-triggered campaigns), #28 (mass-signup threshold coordination)]].

**Design.** A threshold-commitment app where the participant's first-degree contact graph (imported via OAuth from existing social platforms, or self-declared) is used to compute a "complex centrality" score per Centola. Members in clustered network neighbourhoods bridging multiple clusters are weighted more heavily in the threshold calculation — their commitment counts as 2× or 3× toward triggering critical mass, on the basis that their adoption is more likely to seed wide-bridge propagation. Conversely, high-degree influencer commitments are *down-weighted* (they are anti-catalysts per Centola).

**Why this matters.** Lever #16 currently sketches a Kickstarter-style "I commit IFF N others commit" pattern. The Kickstarter pattern is structurally correct for complex contagion (private commitment until threshold, then public announcement — avoids the Google+ awareness-without-commitment trap). What it lacks is *seeding-strategy intelligence*. This build adds Centola-derived seeding intelligence as a first-class feature.

**Limits.** Importing contact graphs from existing platforms creates a privacy surface. Self-declared contact data is unreliable. Complex-centrality computation requires privileged access to the graph, which conflicts with [[federated-learning|privacy-preserving substrate]] preferences. The build needs a DP-style noise budget on the centrality computation, or graph-locality-only computation (each member's local first-degree neighbourhood, never aggregated).

### 5. Lever-Selection Decision Tool

**Combines:** [[strategic-classification]] (Hardt 2016 separability dichotomy) + [[pricing-algorithm-taxonomy]].
**Enables:** Sharper lever-selection across [[possible-strategic-levers|cluster #3, #6, #7, #10, #11]] (profile / algorithm manipulation).

**Design.** Decision tool that takes (a) a target retailer's pricing algorithm family per [[pricing-algorithm-taxonomy|the six-family taxonomy]], (b) candidate manipulation dimensions (demographic spoofing, session rotation, fingerprint parity, behavioural signals), and (c) the cost-function structure for each dimension (separable per Hardt 2016 → polynomial-time defendable; non-separable / metric → NP-hard for firm to defend). Outputs a ranked list of which manipulation dimensions are *durable* against firm response (non-separable) vs *transient* (separable).

**Why this matters.** [[obfuscation-strategic-readout]] currently flags adaptive-seller recovery as a generic caveat. This build operationalises which specific manipulation dimensions are durable for *this specific* pricing-algorithm family. Refines lever-selection from "obfuscation effective against Family 1 / Family 3" to "demographic-spoofing dimension X is durable against Family 1; session-rotation dimension Y is recoverable in <T rounds." Decision-support for builders, not a deployment tool.

**Limits.** Cost-function classification is empirical and proprietary — sellers don't publish their cost-of-manipulation models. Initial version of the tool relies on [[markup-citizen-browser|Markup-style probe-and-publish]] (Build #1 above) to infer cost structure from observed seller-response patterns. Bootstrap dependency.

### 6. Layered Cooperative Governance

**Combines:** [[data-market-mechanism-design]] (Shapley-based external sales mechanism) + [[data-cooperatives]] (democratic governance framing).
**Enables:** [[possible-strategic-levers|lever #1 (many-consumer counterbalance)]], [[possible-strategic-levers|lever #19 (producer-coop × consumer-coop matching)]] — resolves the documented governance tension on [[data-market-mechanism-design]].

**Design.** Two-layer governance for a data cooperative: **mechanism layer** uses [[data-market-mechanism-design|Agarwal Shapley allocation]] for *external sales* (where mechanical fairness is appropriate, where buyers must bid honestly via Myerson-truthful pricing, where the cooperative wants zero-regret revenue maximisation); **democratic layer** governs *strategic decisions* (what data products to produce, who to sell to, what social-purpose constraints to apply, what data flows to refuse on equity grounds). The two layers are explicitly composed: democratic layer sets the parameters within which the mechanism layer optimises.

**Why this matters.** The documented tension on [[data-market-mechanism-design|§Tensions]] is real but resolvable by layering. Pure Shapley would deny the cooperative any voice; pure democratic would force political negotiation over every transaction. Layering captures the strengths of both. This is the [[platform-cooperatives|coopcycle-style federation pattern]] applied to internal cooperative governance.

**Limits.** Members must accept that *external-sales* allocation is mechanically determined (no democratic override of individual Shapley allocations). The democratic layer must constrain itself to setting parameters, not over-riding mechanism outputs — boundary discipline is hard. The replication-robustness fragmentation incentive (cf. [[data-market-mechanism-design|§Tensions, point 4]]) still needs an explicit cooperative-policy response (e.g., honour-system anti-duplication clauses).

### 7. Dual-Use Byzantine-Robust Observatory

**Combines:** [[federated-learning]] (Byzantine-robust aggregation as mirror of [[the-firms-view|§5]]) + [[transparency-tools]] / [[markup-citizen-browser]].
**Enables:** Hardens [[possible-strategic-levers|levers #8 (probe-and-publish), #25 (algorithm-reverse-engineering competition)]] against firm-side data-injection retaliation.

**Design.** Take Build #1 (Federated Pricing Observatory) and add Krum / Trimmed Mean / FoolsGold-style Byzantine-robust aggregation per [[federated-learning|Blanchard et al. 2017]]. The aggregator filters out outlier client updates that are statistically inconsistent with the consensus. This defends against firms or adversaries seeding fake "no-discrimination" reports into the cooperative observatory by impersonating panelists.

**Why this matters.** [[the-firms-view|§5]] documents Byzantine-robust aggregation as a *firm-side* defence against ACA-style consumer poisoning. The same primitive defends a *consumer-side* observatory against firm-side counter-poisoning. Symmetric dual use of the substrate — and a build that anticipates the realistic attack surface of any successful price-discrimination observatory.

**Limits.** Byzantine-robust filtering is not free: legitimate minority-group panelists (e.g., panelists in a low-population demographic where the seller's pricing genuinely differs) are statistically indistinguishable from poisoned outliers. The build inherits the [[the-firms-view|§5]] dual-use disparate-impact concern in mirror form. Filtering thresholds need careful per-deployment calibration.

### 8. Privacy Budget Marketplace

**Combines:** [[federated-learning]] (DP noise scale ε as shared resource) + [[data-market-mechanism-design]] (Shapley-fair allocation).
**Enables:** Exit-pathway flavour of [[possible-strategic-levers|lever #1]]; potentially a new candidate lever (see §New Avenues #5 below).

**Design.** A consumer cooperative trains models under DP per [[federated-learning|Abadi 2016 DP-SGD]]; the total ε privacy budget is a shared resource. Members "spend" ε when querying the model (each query uses some privacy budget); members are *compensated* via [[data-market-mechanism-design|Shapley allocation]] when their data contributes to a model that other parties (external buyers, regulators, advocacy groups) query against under their privacy spend. Two markets in one: ε-as-currency for queries, Shapley-as-currency for contribution attribution.

**Why this matters.** Existing data cooperatives ([[midata]], [[drivers-seat-cooperative]]) collect data and distribute revenue; none have an explicit privacy-budget-as-currency model. The Privacy Budget Marketplace internalises the privacy-utility tradeoff into the cooperative's economic model rather than treating privacy as an externality. Members trade off privacy spend vs revenue capture in their own utility function.

**Limits.** ε accounting is technically complex (composition theorems, sensitivity analysis, Rényi DP bookkeeping). Members must understand the privacy-budget model — likely needs significant UX investment. The cooperative needs an internal mechanism for determining initial ε allocations (democratic? equal per member? per-data-volume?). Cross-references the same governance-vs-mechanism tension Build #6 addresses.

---

## Five candidate new lever avenues

These are *(editorial)* lever proposals not yet on [[possible-strategic-levers]]. Each combines newly-added mechanism pages in a way the inventory does not currently anticipate. Worth considering for inventory addition.

1. **DSAR-as-a-Service for member-bound litigation organisations** — combines [[decentralized-agent-identity]] + [[noyb]] + [[data-disruption-strategy-map|Tier 1 #1]]. A small membership organisation with DID-bound members could rapidly mount class-action-style data-rights litigation at lower marginal cost than NOYB's current operating model. Adjacent to [[possible-strategic-levers|lever #26]] but with a specific tech substrate #26 doesn't currently specify. Avoids the [[buyer-cartels-antitrust|per se cartel risk on #26]] by sticking to information-rights litigation rather than collective refusal.

2. **Federated price-discrimination detector as a public service** — extends Build #1 above into a parallel-institution proposal. Service exposed via API to any consumer-side advocate, member cooperative, or regulator. Doesn't extract or store raw data; runs queries against the federated model. Inverts the [[surveillance-pricing-retail|surveillance-pricing extraction pattern]] at the data-handling layer. **Exit-pathway flavour.** Distinct from the current information-layer levers (#22–#25) which are individual-consumer-facing; this is institutional-consumer-facing.

3. **Multi-cooperative agent federation** — combines [[clawnet-readout]] + [[decentralized-agent-identity]] + [[agent-interop-protocols]]. Network of cooperatively-owned ClawNet instances connected via hardened A2A. Each cooperative is its own trust domain; cross-cooperative collaboration uses DID/VC for cross-domain trust. New exit-pathway architecture. Federation-as-scaling per [[coopcycle]]'s pattern but for agent-mediated coordination across cooperatives. Could be the technical layer underneath a [[possible-strategic-levers|lever #18 (direct-marketplace federation)]] expansion.

4. **Lever-tactics simulator** — combines [[algorithmic-collective-action]] (Hardt 2023 critical-mass formalism) + [[complex-contagion]] (Centola network-topology requirements). Tool that takes a hypothetical campaign (target retailer, target manipulation, collective size, network topology) and outputs a predicted success probability. Decision-support for campaign design across [[possible-strategic-levers|#10, #14, #16, #28]]. Not a deployment tool — a *planning* tool. Lowers the cost of bad-campaign discovery from "months of failed coordination" to "minutes of simulation."

5. **Privacy-budget marketplace as a parallel institution** — Build #8 promoted to lever proposal. Substantive enough to warrant inventory entry under category G (Economic-structural) or as a new exit-pathway sub-category. The novelty: privacy-as-currency is a *new market structure*, not a new tactic against existing markets. Distinct from any existing lever.

---

## Hard limits the new mechanism set imposes

Honest constraints from the new pages that bound what's buildable. These do not invalidate the builds above but constrain their effectiveness profile.

- **Adaptive-seller recovery** ([[the-firms-view|§3]] / [[obfuscation-strategic-readout|§6]]) bounds the durability of any pure obfuscation lever. Build #3 above is the directly-aimed mitigation; without it, obfuscation tools have a finite effectiveness window dictated by the seller's adaptive-learning sophistication.
- **Disparate-impact externality** ([[the-firms-view|§4]] / [[strategic-classification]]) constrains the equity-acceptability of obfuscation-without-collective-constraint. Builds #1, #2, #4, #6 are *collective-constraint* substrates — they pair appropriately with obfuscation; pure-obfuscation builds without this pairing carry the externality.
- **DP-as-firm-counter** ([[the-firms-view|§2]], [[data-disruption-strategy-map|risk class 6]]) suppresses ACA across the lever cluster including Build #3. Tool-level mitigation does not exist; political-framing response (pre-emptive naming of "DP-trained pricing as ACA suppression") is the load-bearing residual lever per [[obfuscation-strategic-readout|open strategic questions]].
- **LLM negotiation buyer-disadvantage** ([[agent-mediated-negotiation-empirics]]) bounds builds that depend on agent-mediated *negotiation*. Builds #1, #2 sidestep this (they are information aggregation, not negotiation). Builds depending on consumer-firm negotiation inherit the 20–40pt seller advantage at the LLM layer.
- **Antitrust risk concentration on lever #26** ([[buyer-cartels-antitrust]]) means any war-chest-backed collective-refusal build needs the [[noyb|NOYB-style strategic-litigation framing]] to avoid per-se cartel exposure. Candidate New Avenue #1 above is the explicit framing solution.
- **Issuer-trust governance for DID/VC** unresolved per [[decentralized-agent-identity]]. Builds #2 and Candidate New Avenue #1 depend on this being solved out-of-band (eIDAS template, federation-of-cooperatives, or similar). Build is technically sound; deployability gated on governance.

---

## Build-portfolio recommendation

*(editorial — opinionated tier ranking, subject to user redirection.)*

**Tier 1 — strongest candidates for development plans now**

1. **Build #2 (Verifiable Mandate-Bound DSAR Pipeline).** Sidesteps LLM-negotiation buyer-disadvantage. Substrate-aligned with [[data-disruption-strategy-map|Tier 1 #1]] which the wiki already identifies as highest-leverage. Risk class 1 per [[data-disruption-strategy-map]] (statutory rights). The Uber audit existence-proof exists; this build generalises the substrate. Issuer-trust governance is the gating dependency.
2. **Build #1 (Federated Pricing Observatory).** Substrate-level privacy. Clear value to [[possible-strategic-levers|lever #8]] + [[data-disruption-strategy-map|Tier 1 #3]]. Build #7 (Byzantine-robust hardening) is a Tier-1 add-on, not a separate build.
3. **Build #4 (Periphery-First Threshold Coordinator).** Resolves the open seeding-strategy question for [[possible-strategic-levers|levers #14, #16, #28]]. Depends on contact-graph access, which has its own privacy surface — but the alternative (no seeding intelligence at all) is what the current lever sketches assume.

**Tier 2 — build with care or after Tier 1 lands**

4. **Build #6 (Layered Cooperative Governance).** Resolves a documented tension on [[data-cooperatives]] / [[data-market-mechanism-design]]; non-urgent until a development plan needs it.
5. **Build #5 (Lever-Selection Decision Tool).** Bootstrap dependency on Build #1; meaningful as a planning tool once probe-and-publish data exists.
6. **Build #3 (Multi-Collective Adaptive-Pricing Disruption).** Theoretical synthesis; needs empirical validation before plan-stage. Pursue if Build #1 + #5 reveal pricing-algorithm families where this is needed.

**Tier 3 — research-stage**

7. **Build #8 (Privacy Budget Marketplace).** Novel market structure; requires significant UX + member-education investment. Worth one research run on existing privacy-budget-economics literature before plan-stage.

The candidate new lever avenues (especially #1, #2, #3) are worth treating as draft additions to [[possible-strategic-levers]] when the inventory next gets revised.

---

## Open strategic questions surfaced by this synthesis

1. **Who runs the federated aggregator?** Builds #1, #7, #8 require an aggregator. The wiki's [[clawnet-readout|operator-trust pattern]] argues for cooperative ownership ([[platform-cooperatives|coopcycle-style federation]]). Needs explicit governance design — analogous to the issuer-trust governance gap on [[decentralized-agent-identity]].
2. **Cross-collective coordination antitrust treatment.** Build #3 (multi-collective) and Candidate Avenue #3 (multi-cooperative federation) explicitly coordinate across collectives. The [[buyer-cartels-antitrust]] frame applies. Joint-purchasing-agreement framing under safe harbours likely defensible; explicit coordinated-disruption framing risky.
3. **Bootstrap path for Build #5 (lever-selection tool).** Without probe-and-publish data, the tool has no input. Catch-22 with Build #1. Sequencing: Build #1 first, accumulate observation data, then Build #5.
4. **Multi-cooperative federation governance.** Candidate Avenue #3 implies a meta-cooperative governance structure (federation-of-federations). [[coopcycle|CoopCycle]]'s 72-coop / 12-country federation is the closest documented precedent; whether its governance model scales to agent-mediated coordination is an open question.
5. **Privacy-budget composition under repeated queries.** Build #8 requires careful ε accounting under composition theorems. Standard DP composition is well-understood; the cooperative-economic-incentive layer on top is novel and may surface unforeseen incentive issues.

## Source

Editorial synthesis across the 10 mechanism pages added 2026-04-26 via the `clawnet-adjacent-methods` research run. All substantive cross-mechanism combinations are *(editorial)* / *(synthesis)* per the strategy-layer convention. Reference-layer claims trace to the inline-cited mechanism pages.

The mechanism pages this readout synthesises across:

- [[algorithmic-collective-action]] — Hardt 2023 + Baumann 2024 + Karan 2025
- [[strategic-classification]] — Hardt 2016 + Contextual Dynamic Pricing with Strategic Buyers + Milli 2019
- [[the-firms-view]] — cross-cutting firm-side counter-perspectives
- [[federated-learning]] — Rahman 2025 survey + foundational FL primary references
- [[complex-contagion]] — Centola
- [[buyer-cartels-antitrust]] — OECD 2022
- [[data-market-mechanism-design]] — Agarwal, Dahleh & Sarkar 2019
- [[decentralized-agent-identity]] — Garzon et al. 2025
- [[agent-mediated-negotiation-empirics]] — AgenticPay 2026 + Abdelnabi 2024
- [[agent-interop-protocols]] — Louck et al. 2025

Plus the existing strategy-layer pages this readout extends:

- [[possible-strategic-levers]] — 29-lever inventory
- [[data-disruption-strategy-map]] — Tier 1 / 2 / 3 build portfolio
- [[obfuscation-strategic-readout]] — obfuscation-specific readout
- [[clawnet-readout]] — agent-mediated coordination readout
- [[lever-implementation-readout]] — H1–H4 implementation evidence

## Related

- [[possible-strategic-levers]] — the lever inventory the eight builds map onto
- [[data-disruption-strategy-map]] — the existing Tier 1/2/3 build portfolio this readout extends
- [[clawnet-readout]] — sister readout (agent-mediated coordination)
- [[obfuscation-strategic-readout]] — sister readout (obfuscation)
- [[lever-implementation-readout]] — sister readout (H1–H4 lever implementations)
- [[strategies/index|Strategies section index]]
