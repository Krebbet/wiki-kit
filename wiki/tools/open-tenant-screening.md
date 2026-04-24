# OpenTSS (Open Tenant Screening Services)

OpenTSS is a **crowdsourced tenant-screening audit project** run by MIT researchers, funded by the Mozilla Technology Fund with support from MIT IDSS and the MIT Data + Feminism Lab. It collects tenant-screening reports and denied-renter experiences to audit the algorithms, data structures, and biases of US tenant-screening services. The most direct tenant-side counter-power tool against [[rental-housing-algorithmic-pricing|RealPage]]-class industry practice captured in this wiki to date — though OpenTSS is a **research project / transparency tool**, not a fully-constituted [[data-cooperatives|data cooperative]].

## Purpose and method

Per the open-tss.net "How TSS Works" page, the project's focus is on making the tenant-screening industry legible to tenants, housing advocates, and regulators.

Mission (per the site footer): "We are MIT researchers who address the challenges related to gaining insight into the internal algorithms, representations, and biases of tenant screening algorithms."

The site provides three things:
1. **Tenant Screening Services Lookup** — a catalogue of tenant-screening companies (RealPage/LeasingDesk, RentGrow/Yardi, National Tenant Network, MRI ResidentCheck, Tenant Tracks/Optimum-10, E-Renter, AmRent, Avail, RentPrep, and others) with the specific data fields each collects.
2. **Request Copy** — a guided flow for renters to request their tenant-screening report (a right under the Fair Credit Reporting Act).
3. **Donate Tenant Screening Report** — the crowdsourcing mechanism: renters contribute their reports to the project for analysis.

## Key findings (from OpenTSS body content)

On **the scale of the tenant-screening industry:**
- Per a cited TransUnion survey of 1,252 respondents, **87% of landlords** reported using tenant-screening services.
- Per an academic study cited on the page, **large-scale landlords use algorithmic tenant-screening products 60–70% of the time vs 40–50% for small-scale landlords**.

On **the rent-to-income ratio** (a key screening criterion):
- Typical thresholds are 30% of rent, or 2.5–3× rent.
- OpenTSS argues "the rent-to-income ratio lacks evidence to support whether or not it is a good indicator of tenants who pay rent on time. It has never been empirically tested, and 'the use of a minimum income requirement as a standard for designing public assistance programs is very different from using such a requirement for determining the likelihood a prospective tenant will pay rent.'"

On **credit-score thresholds:**
- Landlords use varying minimums (e.g. 600 as a hard minimum, case-by-case review below 700) with no published empirical validation.
- Credit scores weight medical debt and student loans inconsistently across landlords; there is no industry standard for which collection types to include.

On **eviction records and criminal records:**
- OpenTSS catalogues the critical data fields needed for faithful interpretation against the fields actually reported by each screening service — and finds systematic omissions (e.g. many reports omit whether an eviction filing resulted in a judgment for possession; many criminal records conflate arrest, charge, and conviction into a single event).
- Specific example: RealPage "uses 'abbreviated' criminal records for 11,000 reports, which are less expensive to obtain than full records but do not include information about the resolution." Per the page, **only 18.9% of NY felony arrests in 2019 led to felony convictions** — making resolution-level detail critical to accurate interpretation.

On **the "tenant score":**
- Most tenant-screening services now produce a proprietary score (analogous to a FICO score for housing). The algorithms are almost never publicly disclosed, and the input features are generally not exhaustive — SafeRent lists only "payment performance and eviction history"; National Tenant Network lists a wider set.
- Landlord-configurable scoring: RentGrow, National Tenant Network, and MRI Resident Screening all offer landlords customisation forms that let the landlord set rules for which debt types, eviction cases, and criminal cases count. "A significant portion of the inner algorithms are rule-based, and established by default values from tenant screening services, and then further customized by landlords."

On **application-fee extraction:**
- Application fees typically range **$10–$55**, and frequently include the cost of the tenant-screening report.
- "Lower-income tenants with substandard credit scores and histories are required to pay these fees more often than higher-income tenants who have a greater likelihood of being accepted" — the fees are ingested by applicants who are *more likely to be denied*.

## Counter-power mechanism

OpenTSS is the **transparency-tool** and **tech-workaround** counter-power from the [[regulatory-responses]] taxonomy in combination:

- **Transparency tool** layer: makes the tenant-screening industry's operations visible enough for policy intervention. The data-fields catalogue per company is a direct public good.
- **Tech workaround / consumer data pooling** layer: the "Donate Tenant Screening Report" flow is a lightweight crowdsourcing form of what a [[data-cooperatives|full tenant data cooperative]] would do — pooling tenant-side data to counter the seller-side data pooling by tenant-screening vendors.

**Structural position.** OpenTSS sits in the same counter-power cell as what [[regulatory-responses]] design-input #2 describes: a tenant-side data pool as the structural mirror of the landlord-side data pool used by RealPage and tenant-screening vendors. OpenTSS is not a full coop — it is a research-project harvest with no cooperative governance or member-dividend structure documented — but it demonstrates one of the two things such a coop would need (a data-collection pipeline) is feasible. *(editorial / synthesis)*

## Scope and limitations

- **Not a cooperative.** Members do not govern OpenTSS or share in any economic return; they donate reports to research. Per the Mendonça et al. taxonomy on [[data-cooperatives]], this is closer to a **data-for-research commons** than a data coop.
- **Coverage of tenant-screening vendors is by company, not by landlord.** OpenTSS documents what each vendor *does*, not what price outcomes a specific landlord (e.g. a Greystar-class national operator) produces.
- **US-focused.** Page also offers Spanish; no evidence captured of jurisdictional coverage outside the US.
- **Funded by philanthropy.** Dependence on Mozilla / MIT grant funding; no independent revenue model captured.

## Source

- `raw/research/consumer-data-pooling/03-06-opentss-how-it-works.md`
  - **Origin:** OpenTSS (open-tss.net) — MIT research group on tenant-screening algorithms; the "How TSS Works" project-methodology page.
  - **Audience:** tenants, housing advocates, tenant-screening regulators.
  - **Purpose:** explain the tenant-screening industry's data practices; recruit report donations.
  - **Trust:** primary research-project source; MIT-affiliated researchers with grant funding. Advocacy-aligned (pro-tenant) but factual and carefully sourced with internal citations to academic studies, FCRA law, and legal primary sources. The page itself cites Matthew Desmond, *The New Jim Crow*, NYS criminal-justice statistics, and a TransUnion landlord survey — a strong citation trail for load-bearing claims.

## Related

- [[rental-housing-algorithmic-pricing]] — the adjacent industry problem OpenTSS audits.
- [[data-cooperatives]] — the fuller cooperative governance model OpenTSS approaches but does not constitute.
- [[regulatory-responses]] — transparency-tool and tech-workaround taxonomy.
- [[surveillance-pricing-retail]] — parallel industry-side data-aggregation pattern in retail.
