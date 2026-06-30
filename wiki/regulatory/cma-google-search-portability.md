# CMA Google Search Data Portability Requirement (UK, 2026)

The UK Competition and Markets Authority has imposed two conduct requirements on Google under the Digital Markets, Competition and Consumers Act (DMCCA): a fair-ranking obligation and, more consequentially for counter-power tooling, a mandated search data portability API. As of June 17, 2026, what was previously a voluntary Google Data Portability API is now a legal requirement — authorized third parties (rewards platforms, personalized-offer services, recommendation engines) can access a signed-in UK user's Google search data with that user's consent via API. The portability requirement has a 3-month implementation deadline (~September 2026). This is a competition-law instrument, not GDPR; it runs parallel to the DSAR framework on a different legal basis and potentially covers different data categories.

## The Mandate

The CMA designated Google with Strategic Market Status (SMS) in its general search and search advertising activities. Under DMCCA, that designation unlocks conduct requirements. The June 17 action introduces two:

1. **Fair Ranking** — Google must rank organic search results (including AI Overviews; not sponsored results) by objective, non-discriminatory criteria; provide advance notice of significant ranking changes; and establish clear processes for businesses to raise ranking concerns. Implementation: 6 months.

2. **Search Data Portability** — Google must allow users to transfer search data to authorized third parties via its Data Portability API. Implementation: 3 months (~September 2026).

The CMA frames this as putting UK users "on a par with those in the EU" under the Digital Markets Act, while giving businesses investment certainty. The underlying technical mechanism (Google's Data Portability API) already existed voluntarily; the mandate converts it to an enforceable legal obligation with compliance monitoring and reporting.

## Data Portability: What Google Must Share

**Data categories in scope:** User search data. The press release gives illustrative examples — travel suggestions, shopping deals, cashback and discount offers — but does not enumerate specific data fields. The actual field specification will be in CMA's technical implementation documents (not captured in this source).

**Mechanism:** The user connects their Google account within a third-party service and explicitly authorizes the data transfer. The third party calls Google's Data Portability API; Google processes and transfers the data; the third party uses it to deliver a service (personalized recommendations, tailored offers, etc.).

**Account requirement:** Signed-in Google account required. Anonymous or signed-out users are not covered.

**Derived/inferred data:** Scope of derived or inferred data categories is not specified in this source — an open question for follow-up against technical implementation documents.

**Geographic scope:** UK only; applies to signed-in UK users.

## Who Qualifies as an Authorized Third Party

The press release names three service archetypes as qualifying recipients:
- Rewards platforms
- Companies offering personalized offers or discount codes
- Personalized recommendation services

A cooperative or collective data intermediary aggregating consumer search data for collective price-comparison or demand-aggregation purposes fits within the stated framing — the CMA explicitly positions the API as enabling "innovative businesses" to build "new products and services for users," which is broad enough to encompass non-profit or cooperative structures.

**Critical gap:** The authorization process for third parties is not defined in this source. There is no enumerated application process, criteria, or timeline for becoming an authorized third party. Counter-tools seeking access would need to pursue this through CMA's technical implementation documents and Google's API program — channels that are opaque at the time of this capture.

## Limitations and Open Questions

- **Authorization opacity:** How a third party qualifies as "authorized" is undefined here. The actual gatekeeping mechanism — and whether Google has meaningful discretion to deny cooperative or collective structures — is unknown.
- **Data field specification:** Exact data categories and field definitions require the CMA's technical implementation document, not the press release.
- **Derived data exclusion:** Whether Google's inferred interest graph, behavioral profiles, or ad-targeting signals are in scope is unresolved.
- **Consent granularity:** The mechanism requires per-user consent via Google account connection. This is a friction point for collective aggregation at scale — each user must individually authorize.
- **Competition-law vs. GDPR:** This mandate operates on a different legal basis than DSAR/GDPR portability. Data categories covered may diverge from what a GDPR Subject Access Request would yield, in either direction.
- **Enforcement timeline:** CMA will monitor compliance through "regular reporting and ongoing engagement." Enforcement teeth and escalation path if Google delays or narrows implementation are not specified in this source.
- **AI Overviews scope:** Fair ranking applies to AI Overviews; it is unclear whether search data generated through AI Overview interactions is included in the portability scope.

## Counter-Power Implications: Cooperative Data Intermediaries

This is the first UK-mandated API that explicitly names consumer-facing authorized third parties — not businesses or regulators — as the primary data recipients. That framing is significant:

**Substrate for collective tooling.** A cooperative or collective intermediary that aggregates consenting users' Google search data could, in principle, qualify as an authorized third party. The aggregated data would provide a demand-side intelligence layer usable for collective price-comparison, coordinated purchasing, or exposing personalization asymmetries at scale.

**Legitimizing frame.** The CMA's public rationale — more choice, better deals, innovation for users — provides political cover for cooperative structures pursuing the same goals without the profit motive. A non-profit or member-owned intermediary that applies as an authorized third party can cite alignment with the CMA's stated intent.

**Parallel with EU DMA.** The CMA explicitly benchmarks this against EU DMA portability rights. EU-side work on cooperative data intermediaries under the Data Governance Act is therefore directly relevant; UK implementation may track or diverge from EU technical standards.

**Near-term action horizon.** The ~September 2026 implementation deadline makes this actionable in the near term. Monitoring the CMA's technical implementation documents and Google's API documentation update is the immediate priority for counter-tools seeking access.

See [[mechanisms/data-cooperatives]] for cooperative third-party access patterns; [[mechanisms/collective-bargaining-for-data]] for how aggregated search data flows into demand-side collective bargaining; [[strategies/data-disruption-strategy-map]] for where this mandated API sits as a counter-tool substrate.

## Source

- CMA press release: "Further CMA action to secure a fairer deal for businesses and improve Google search services in UK," June 17, 2026. `raw/research/weekly-2026-06-29/04-cma-google-search-portability.md`
- Trust level: High for mandate details and implementation timeline; low for authorization process and data field specification (requires CMA technical implementation documents not captured here).
- Instrument: UK DMCCA (competition law) — not GDPR.

## Related

- [[counter-power/regulatory-responses]] — regulatory enforcement survey
- [[mechanisms/data-cooperatives]] — cooperative third-party access as substrate
- [[mechanisms/collective-bargaining-for-data]] — collective use of the mandated data flow
- [[regulatory/uk-duaa-dsar-complaints]] — UK digital rights parallel (different legal basis)
- [[strategies/data-disruption-strategy-map]] — mandated API as counter-tool substrate
