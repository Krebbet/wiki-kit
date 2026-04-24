# Dynamic Pricing Overview

Dynamic pricing, personalized pricing, surveillance pricing, and algorithmic pricing are overlapping but distinct terms for practices in which sellers adjust prices using data, algorithms, or both — over time, across customers, or both. This page distinguishes the terms as used across the wiki's sources and serves as the hub for industry-specific pages, mechanism pages, and counter-power pages.

## Definitions

**Dynamic pricing.** A single product's price fluctuates over time for all customers, adjusted by demand, inventory, time, competitor prices, or events. Classic examples: airline tickets, hotel rooms, Uber surge pricing. Used by airlines for decades. *(Wikipedia; NBER working paper.)*

**Personalized pricing.** Prices are tailored to individual customers or segments based on identifying data — purchase history, location, device, browsing, demographics, inferred willingness-to-pay. Distinct from dynamic pricing in that different customers can see different prices for the same product at the same moment. *(NBER working paper; academic literature on "personalized dynamic pricing".)*

**Surveillance pricing.** The FTC's 2024 term for personalized pricing powered by pervasive consumer surveillance — behavioural tracking (mouse movements, cart abandonment, email open times), cross-device linking, third-party data broker feeds, and inferred traits (emotional state, impulse propensity, family status). The framing re-centres the data-collection layer as the regulatory target rather than the pricing output. *(FTC Issue Spotlight.)*

**Algorithmic pricing.** Umbrella term for any of the above executed by an automated algorithm. Includes rule-based engines, optimisation models, and learning algorithms (Q-learning, bandit, deep reinforcement learning). Academic literature increasingly uses this as the genus term. *(NBER; HBS; arXiv 2504.16592.)*

## Why the terms matter

The terms carry different regulatory theories:
- **"Surveillance pricing"** (FTC) targets the data pipeline — what consumer information is collected, by whom, under what disclosures. See [[regulatory-responses]].
- **"Algorithmic pricing"** (academic) frames the problem at the algorithm-design and market-structure layer — frequency of updates, commitment strategies, learning dynamics. See [[algorithmic-collusion]].
- **"Collusion by algorithm"** (DOJ, in the RealPage complaint) frames it as an antitrust violation when a third party pools competitor data. See [[rental-housing-algorithmic-pricing]].

These framings are complementary, not mutually exclusive. A single practice (e.g., RealPage's rent algorithm) is simultaneously surveillance pricing (of tenants), algorithmic pricing (fast, automated), and explicit algorithmic collusion (data-pooling among competitors).

**A fourth framing, orthogonal to the above.** [[platform-cooperatives]] sit outside the dynamic-pricing debate entirely — instead of regulating extractive platforms or detecting personalised pricing, they build ownership-level alternatives (worker- or user-owned platforms) that don't run extractive pricing in the first place. Covered on [[regulatory-responses]] as the exit-alternative counter-power lane.

## Coverage in this wiki

- **Industries:** [[rental-housing-algorithmic-pricing]] · [[surveillance-pricing-retail]] · [[consumer-facing-dynamic-pricing]]
- **Mechanisms:** [[algorithmic-collusion]] · [[pricing-algorithm-taxonomy]] (algorithm families + data-input catalogue, added 2026-04-23)
- **Strategy readouts:** [[data-disruption-strategy-map]] (which levers work against which algorithm family; platform-enforcement risk tiers)
- **Counter-power:** [[regulatory-responses]]

## Source

- `raw/research/dynamic-pricing-landscape/03-wikipedia-dynamic-pricing.md`
  - **Origin:** Wikipedia (community-edited encyclopaedia).
  - **Audience:** general public.
  - **Purpose:** define the term and catalogue industry uses.
  - **Trust:** starting reference only. Load-bearing claims chased to primary sources below.
- `raw/research/dynamic-pricing-landscape/06-nber-algorithmic-pricing.md`
  - **Origin:** NBER working paper (Zeithammer et al.), June 2024, revised June 2025.
  - **Audience:** academics, policymakers, pricing managers.
  - **Purpose:** survey algorithmic pricing definitions, managerial implementation, and regulatory concerns.
  - **Trust:** NBER working paper tier — not peer-reviewed but strong institutional vetting.
- `raw/research/dynamic-pricing-landscape/08-arxiv-algorithmic-collusion.md`
  - **Origin:** arXiv preprint 2504.16592 (April 2025), accepted at *Business & Information Systems Engineering*.
  - **Audience:** CS and economics researchers.
  - **Purpose:** survey interdisciplinary research on algorithmic collusion and identify open problems.
  - **Trust:** preprint accepted at peer-reviewed venue.

## Related

- [[rental-housing-algorithmic-pricing]]
- [[surveillance-pricing-retail]]
- [[consumer-facing-dynamic-pricing]]
- [[algorithmic-collusion]]
- [[regulatory-responses]]
