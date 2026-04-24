# Data Cooperatives

A data cooperative is a member-owned organisation where individuals voluntarily pool their data, govern its use democratically, and share the resulting benefits. Distinct from [[platform-cooperatives]] (which pool labour or services), data coops specifically pool **data assets** under cooperative ownership — one of four legal mechanisms for data stewardship alongside data trusts, data commons, and data unions. Data coops sit in the same counter-power lane as [[regulatory-responses]]'s design-input #2: a structural alternative to unilateral corporate data aggregation such as [[rental-housing-algorithmic-pricing|RealPage]] or [[surveillance-pricing-retail|FTC-surveyed retail surveillance pricing]].

## Definition and boundaries

Per Mendonça et al. (arXiv 2504.10058), a data cooperative is "a member-owned organization where individuals voluntarily contribute their data, control its usage collectively, and share the resulting benefits fairly, with each individual retaining ownership of their personal data." An organisation qualifies only if it adheres to the **seven ICA cooperative principles**: voluntary membership, democratic member control, economic participation, autonomy, education, cooperation, and concern for the community.

The paper deliberately uses "**data stewardship**" rather than "data ownership" for the coop's relationship with the pooled data — the coop steward enforces member-agreed rules rather than assuming exclusive property rights.

**Distinctions from related mechanisms** (per Mendonça et al. and Ada Lovelace Institute 2021):

| Mechanism | Ownership | Orientation | Example |
|---|---|---|---|
| Data cooperative | Member-owned, collective control | Internal governance; equitable use *among* members | [[midata]], Salus Coop |
| Data union | Pooled for negotiation | External negotiation with third parties | Streamr "data unions" |
| Data trust | Trustees hold legal ownership for beneficiaries | Responsible management per trust deed | Mayo Clinic Data Trust |
| Data commons | Community-managed shared resource | Open / collaborative access | NOAA / OCC environmental data commons |

The **orientation difference between coop and union** (Mendonça et al.) is the key axis: a data union is about negotiating better external terms; a data coop is about internal governance of a shared asset. Porat's (NYU, March 2024) experimental work on individual "bargaining with algorithms" sits in the union-adjacent space — see [[collective-bargaining-for-data]].

## Four frameworks (Mendonça et al.)

The paper organises data coops along four interlocking pillars:

1. **Governance framework** — bylaws, democratic member control (voting, board, forums), fiduciary duty to members, regulatory compliance (e.g. GDPR).
2. **Operational framework** — data management protocols, privacy/security safeguards, economic and incentive architecture.
3. **Technological framework** — data governance platform (access control, monitoring, audit), scalable storage/compute, optional blockchain for verifiable audit logs.
4. **Social framework** — member education, transparency initiatives, trust-building. The paper describes this as "indispensable": a data coop is a community of individuals, not only a technical system.

## Legal vehicles

From the Ada Lovelace Institute 2021 report, UK-specific:

- **Co-operative and Community Benefit Societies Act 2014** — the standard UK registration for cooperative societies. Requires "bona fide cooperative society" status; the FCA uses the ICA's Statement on Cooperative Identity as its indicator.
- **Private company limited by guarantee** — alternative where governance flexibility or non-cooperative legal form is desired.
- If the primary beneficiary is a wider community rather than members, the **community benefit society** form is appropriate.

US-specific (from Ada Lovelace case study on Driver's Seat): **Limited Cooperative Association (LCA)**, a state-law vehicle allowing investor-member cooperatives. Covered on [[platform-cooperatives]] as the practical US legal vehicle.

## Challenges (Ada Lovelace Institute 2021, with Mendonça et al. extensions)

The Ada Lovelace report identifies three clusters of challenge:

**1. Uptake.** Four sub-challenges for recruiting members:
- *Resonance* — do people recognise the data-governance problem?
- *Mobilisation* — are they motivated to find and engage a coop as the solution?
- *Trust* — do they trust this particular coop to steward their data?
- *Capacity* — do they have the data literacy to participate meaningfully?

**2. Scale.** Features inherent to the cooperative form that tension with large data-steward functions:
- *Democratic control and shared ownership* — can strain at scale; tradeoff between member voice and operational nimbleness.
- *Rights, accountability and governance* — coops create a large pool of members who can demand accountability and may be personally liable.
- *Governance-failure vulnerability* — the Ada Lovelace report cites **Mountain Equipment Co-op** (Canadian retail coop, sold to US private equity in 2020 over member objections) as a cautionary example of how a data coop's asset-concentration could become a long-term vulnerability.

**3. Financial sustainability.** Coops rarely raise external capital; tend to rely on grant aid or philanthropy. Can limit hiring capable administrators, which creates a feedback loop into governance problems.

Mendonça et al. add:
- **Coordination** — large heterogeneous memberships face decision-making deadlock.
- **Third-party collaborations** and **data standardisation** — harder when members span sectors.
- **Member engagement** — aligning individual incentives with the collective project.

## Live cases

- **[[midata]]** — Swiss health data cooperative, founded 2015 in Zurich. Nonprofit, open-source platform (Open MIDATA Server, GPLv3); ETH Zurich + Bern University of Applied Sciences. The OECD-cited canonical example.
- **[[drivers-seat-cooperative]]** — US driver-owned data coop for rideshare/delivery workers, incorporated 2019 as an LCA. Sold mobility insights to cities; reported 13% income uplift for drivers. Transitioned to the Workers' Algorithm Observatory at Princeton; the driversseat.co homepage is now offline *(editorial observation based on 2026-04-21 capture)*.
- **Salus Coop** (Barcelona, 2017) — nonprofit health data coop. Developed the "Common Good Data License for Health Research" through crowd-design. Per Ada Lovelace 2021: citizen-driven, with conditions limiting data to non-commercial biomedical research with anonymised use.
- **JoinData** (Netherlands, agriculture) — Mendonça et al. cite as a Dutch farmer data coop addressing data lock-in with agribusiness technology providers.
- **The Good Data** (UK, **DISSOLVED**) — registered as a cooperative society under the 2014 Act; pooled members' browsing data and sold it anonymised to brokers. Dissolved per the Ada Lovelace report because (a) Google rejected its Chrome extension, blocking its technical model, and (b) it "failed to pass through the message and to attract enough members." Illustrates the uptake and platform-dependency risks.

## Relevance to this wiki's domain

The dynamic-pricing problem documented across [[rental-housing-algorithmic-pricing]], [[surveillance-pricing-retail]], and [[consumer-facing-dynamic-pricing]] shares a structural feature: a **single seller-side entity aggregates data across many counterparties** and uses it to set prices against individuals who act alone. Data coops attempt the inverse: a single buyer/subject-side entity aggregates data across many members and uses it to counterbalance. This is the design-input #2 pattern on [[regulatory-responses]] — a buyer-side data cooperative is the structural mirror of RealPage-style seller-side data pooling. *(editorial / synthesis)*

The Ada Lovelace report emphasises that this model has "positive" rather than "negative" agendas — data coops use data rather than restrict it. A tenant data coop would not merely opt tenants out of [[rental-housing-algorithmic-pricing|RealPage]]'s surveillance pipeline but would actively produce competing aggregate rent data tenants could use in negotiation. OpenTSS (see [[open-tenant-screening]]) is a partial instance: it crowdsources tenant-screening reports to audit the industry, though it is a research project rather than a fully-constituted coop.

## Source

- `raw/research/consumer-data-pooling/05-01-ada-legal-mechanisms.md`
  - **Origin:** Ada Lovelace Institute and the UK AI Council — *Exploring legal mechanisms for data stewardship*, March 2021.
  - **Audience:** policymakers, lawyers, data-policy practitioners.
  - **Purpose:** survey legal mechanisms (data trusts, data cooperatives, corporate/contractual) and offer a working-group synthesis.
  - **Trust:** policy-research report from a well-regarded UK think tank, joint with the UK AI Council. Authoritative for definitions, legal framing, and the UK legal context.
- `raw/research/consumer-data-pooling/06-02-arxiv-data-coops-governance.md`
  - **Origin:** Mendonça, Di Marzo, Abdennadher (University of Geneva / HES-SO) — *Data Cooperatives: Democratic Models for Ethical Data Stewardship*, arXiv 2504.10058, April 2025 preprint.
  - **Audience:** researchers in data governance, cooperative studies, information systems.
  - **Purpose:** survey and formalise data-cooperative frameworks, distinguish from related models, catalogue applications.
  - **Trust:** preprint, not yet peer-reviewed but authors are from research groups active in the space.
- `raw/research/consumer-data-pooling/04-03-hardjono-pentland-opal.md` — for technical-framework context (OPAL architecture).
  - **Origin:** Hardjono and Pentland (MIT Connection Science & Media Lab) — *Open Algorithms for Identity Federation*, arXiv 1705.10880.
  - **Audience:** identity-management researchers, trust-framework designers.
  - **Purpose:** specify the OPAL paradigm ("move the algorithm to the data") as a privacy-preserving alternative to attribute exchange.
  - **Trust:** peer research from a long-running MIT group; a canonical reference for the technical-framework layer of data coops.

## Related

- [[midata]]
- [[drivers-seat-cooperative]]
- [[open-tenant-screening]]
- [[collective-bargaining-for-data]]
- [[platform-cooperatives]]
- [[regulatory-responses]]
- [[dynamic-pricing-overview]]
