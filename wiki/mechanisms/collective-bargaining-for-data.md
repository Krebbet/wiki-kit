# Collective Bargaining for Data

Two adjacent counter-power frames on the buyer/subject side of data and pricing markets: (1) **Collective Bargaining in the Information economy (CBI)** — Vincent, Prewitt & Li's 2025 position paper arguing that information producers should form coalitions and bargain with AI operators over data rights; (2) **Individual algorithmic price bargaining** — Porat's 2024 NYU/Harvard experimental work showing consumers can strategically "bargain" with pricing algorithms via purchase abstention and data-rights exercise. Both sit in the orientation-toward-negotiation space that Mendonça et al. call a **data union** (see [[data-cooperatives]] for the coop/union distinction) — and together they form the bargaining-lane complement to the governance-lane of [[data-cooperatives]].

## CBI: the collective frame (Vincent, Prewitt & Li, arXiv 2506.10272, 2025)

### Core position

From the abstract: "Producers of information goods (such as journalists, researchers, and creative professionals) need to be able to collectively bargain with AI product builders in order to receive reasonable terms and a sustainable return on the informational value they contribute."

The paper's structural argument: competitive markets drive information prices to zero because information can be copied at trivial marginal cost (Arrow's "information paradox"). Therefore only actors with sufficient market power — concentration of capital — can capture any return on producing new information. Without counter-concentration from information producers, AI progress will produce what the authors call a **"capital singularity"**: concentration of financial, informational, and market power into very few actors.

### The CBI proposal

Vincent et al. advocate "negotiation between (a) aligned or 'trusted' data intermediary organizations representing large groups of information producers, and (b) information-aggregating AI operating organizations."

Subject of the negotiations: "various terms of data use, including constraints on downstream applications, reporting requirements, future compensation for data contributors, and more."

### Concrete actions (per §1.1)

- **Private initiatives by information producers.** Industry- or sector-wide joint ventures to increase collective bargaining power over AI training rights. Consumers and communities (social, geographic, religious) should do the same — "collecting and controlling the information they generate, and delegating power to trusted representatives to bargain with tech/AI over the rights to use it."
- **Public support by governments.** FTC, DOJ, Canadian Competition Bureau, European Commission on Competition should "issue clarifying statements, and/or new 'safe harbor' regulations clarifying and/or expanding the extent to which multi-stakeholder joint ventures that increase information producers' bargaining power do not violate antitrust, data protection, and other rules." The paper flags **Parker Immunity** (US state-action antitrust exemption) as a relevant vehicle.
- **Refocused advocacy and research.** The ML/AI research community should build data-valuation, interpretability, influence, and attribution mechanisms — "these mechanisms will equip both information producers and AI companies with the means to better estimate the true value of new information and compensate it at a socially efficient level." HCI/design communities should identify interaction patterns for data-pooling decisions and for trusted-representative bargaining.
- **Support from technology actors.** Large AI companies gain from CBI via higher-quality data and avoided market-distortion risk; small AI operators gain via tailored data-intermediary relationships.

### Why CBI over alternatives

Vincent et al. explicitly contrast CBI with two alternatives:
- **Top-down AI regulation.** Dismissed as "limited in responsiveness and coverage" and as unlikely to reproduce incentives for locally-produced information goods.
- **Open AI / open-source.** Dismissed as "fail[ing] to fully mitigate the risks" because best-performing frontier models may retain advantage over open alternatives, and because acting on open models still depends on capital access.

### Intellectual lineage

The paper draws on "data as labor" (Arrieta-Ibarra, Weyl), "data leverage" (Vincent's prior work), "data dignity" and "plurality" (Weyl, Glen), and information economics (Arrow 1962; Varian/Shapiro).

## Consumer-level bargaining (Porat, NYU/Harvard, March 2024 draft)

### Core experimental finding

Porat ran a pre-registered, incentive-compatible randomised experiment (Penn Wharton Credibility Lab #157705, Harvard IRB23-1488, Jan 2024) offering participants a $10 gift card in multiple rounds at a price set by an algorithm based on their prior rounds' decisions.

Finding: **participants strategically avoided purchases they would have otherwise made to induce a price decrease in subsequent rounds.** This effect was statistically significant and increased in magnitude when participants were disclosed the algorithmic pricing mechanism (disclosure mandate).

### The three consumer/data-protection tools tested

Porat tested whether existing consumer- and data-protection rights function as bargaining tools:

1. **Disclosure mandate** — telling consumers the price is algorithmic and based on their behaviour. **Effect:** strategic-abstention behaviour became larger and more statistically significant.
2. **Cookie laws (prevent data collection ex ante).** **Effect:** participants used the right strategically.
3. **Erasure laws / right to be forgotten (prevent data retention ex post).** **Effect:** participants used the right strategically — preventing retention after rounds where they purchased (to avoid signalling high willingness-to-pay for subsequent rounds), and allowing it after rounds where they declined (to signal low willingness-to-pay and induce a price drop).

### Implication

Per the abstract: "The increasing use of algorithms to set personalized prices based on consumers' behavior opens a path for consumers to 'bargain' with algorithms over prices and reclaim market power."

Cost side: "this behavior sometimes came at the cost of avoiding efficient purchases, when the price offered was lower than the value participants assigned to the gift card" — i.e. strategic abstention is a real lever but produces deadweight loss.

## Relationship between the two framings

| | CBI (Vincent et al.) | Porat |
|---|---|---|
| Unit of action | Trusted data intermediary representing a class | Individual consumer |
| Counterparty | AI / information-aggregating company | Any firm running personalised pricing |
| Mechanism | Negotiate terms (data use, compensation, guardrails) | Strategic abstention + selective exercise of cookie/erasure rights |
| Time horizon | Long-term structural (create institutions) | Transaction-level (per-round in the experiment) |
| Required infrastructure | Federated data-management tools, data valuation methods, antitrust safe harbours | Nothing beyond existing GDPR / state privacy laws |

The two framings are complementary. Porat's empirics suggest individual bargaining power exists but is bounded and produces inefficient outcomes without coordination; Vincent et al. argue that only collective institutions (data intermediaries / coops / unions) can capture the social value at stake with pricing and AI-training markets. This is the **bargaining-lane** counterpart to the **governance-lane** documented on [[data-cooperatives]]. *(editorial / synthesis)*

## Relevance to this wiki's domain

- **[[consumer-facing-dynamic-pricing]]** — Porat's experiment directly tests the consumer-bargaining theory for personalised pricing. Airlines, rideshare, Amazon, Ticketmaster-class personalisation are the real-world domain.
- **[[rental-housing-algorithmic-pricing]]** — RealPage's landlord-side data pool is a textbook information-asymmetry problem. A CBI-style tenant intermediary (building on [[open-tenant-screening]]'s crowdsourcing method) is a structural mirror.
- **[[surveillance-pricing-retail]]** — the FTC 6(b) surveyed retail-side surveillance pricing; Porat's cookie / erasure-rights strategies map directly onto FTC recommendations.
- **[[algorithmic-collusion]]** — the "capital singularity" concern in Vincent et al. is adjacent to the HBS asymmetric-frequency harm on the algorithmic-collusion page: both concern concentration of information-processing capacity driving price outcomes.

**Design-input implication.** A buyer-side tenant data coop (design-input #2 on [[regulatory-responses]]) combined with a CBI-style trusted-intermediary legal structure maps onto the CBI proposal's "trusted data intermediary organizations." OpenTSS (see [[open-tenant-screening]]) is a proto-CBI collection layer; a data-intermediary legal shell (per Colorado LCA on [[platform-cooperatives]], or UK CBS 2014 on [[data-cooperatives]]) plus a negotiation mandate would complete the stack. *(editorial / synthesis)*

## Open questions (editorial)

- **Antitrust status of CBI-style intermediaries.** Vincent et al. flag Parker Immunity and "safe harbor" regulation as needed. In the US, the DOJ's [[rental-housing-algorithmic-pricing|RealPage action]] is explicit that data-pooling among competitors is a section 1 Sherman Act violation — the symmetry of treatment for tenant-side pooling is an open legal question.
- **Mobilisation challenge.** Porat's individual-bargaining mechanism requires consumer data literacy the Ada Lovelace 2021 report flags as the critical uptake barrier (see [[data-cooperatives]] on the four-challenge uptake framework). Disclosure mandates help (Porat's experiment confirms) but don't close the gap.
- **Who is the intermediary?** Vincent et al. are deliberately under-specified on the legal form of the intermediary. UK Community Benefit Societies, US LCAs, and data unions (Streamr-style) are all candidates; the current wiki has no page comparing them for pricing-use specifically.

## Source

- `raw/research/consumer-data-pooling/07-07-arxiv-collective-bargaining.md`
  - **Origin:** Vincent, Prewitt & Li (Simon Fraser University / RadicalxChange / UT Austin) — *Collective Bargaining in the Information Economy Can Address AI-Driven Power Concentration*, arXiv 2506.10272, June 2025 (under review).
  - **Audience:** AI policy, AI safety, information-economics, labour-organising researchers.
  - **Purpose:** position paper advocating a specific policy agenda (CBI) with technical, legal, and social components.
  - **Trust:** preprint under review. Authors include the CTO of RadicalxChange (Prewitt), which has a prior position on data unions — noted as political-stance metadata rather than exclusion.
- `raw/research/consumer-data-pooling/08-08-porat-bargaining-algorithms.md`
  - **Origin:** Haggai Porat (Harvard Law / Tel Aviv Economics) — *Bargaining with Algorithms: An Experiment on Algorithmic Price Discrimination and Consumer and Data Protection Laws*, March 2024 draft, NYU Law & Economics seminar.
  - **Audience:** legal scholars, empirical law-and-economics, regulators writing personalised-pricing rules.
  - **Purpose:** experimental test of whether consumer/data-protection laws act as bargaining tools against pricing algorithms.
  - **Trust:** seminar draft from the John M. Olin Center at Harvard; pre-registered RCT; IRB-approved. Strong empirical basis for the reported findings.

## Related

- [[data-cooperatives]] — governance-lane complement to this bargaining-lane.
- [[open-tenant-screening]] — proto-intermediary collection layer.
- [[rental-housing-algorithmic-pricing]]
- [[consumer-facing-dynamic-pricing]]
- [[surveillance-pricing-retail]]
- [[algorithmic-collusion]]
- [[regulatory-responses]]
