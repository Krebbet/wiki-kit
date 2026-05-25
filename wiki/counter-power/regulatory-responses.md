# Regulatory and Other Counter-Power Responses to Algorithmic Pricing

Consolidated survey of pushback mechanisms against dynamic, personalised, surveillance, and algorithmic pricing — regulatory enforcement, legislation, sub-national action, journalism, litigation, and consumer backlash — as documented in the wiki's 8 captured sources. This is the operating-room page for answering *where the existing counter-power is*, *where it is nascent*, and *where the gaps are*.

## 1. Federal regulatory enforcement (US)

### DOJ — algorithmic price-fixing (RealPage)
The most developed federal enforcement action. DOJ + 8 state AGs sued RealPage August 2024; settled late 2025 with structural remedies (data-sharing ban, no-coordination injunctions, court-appointed monitor) but no financial penalty and no admission of wrongdoing. At least 10 state AGs joined. The second Trump DOJ continued prosecution and directly sued six major landlords. Full account at [[rental-housing-algorithmic-pricing]]. *(DOJ press release; ProPublica.)*

**Mechanism:** Sherman Act Section 1 — explicit horizontal coordination via a shared algorithmic intermediary.

**Reach:** works for the explicit-coordination variant. Does not reach tacit algorithmic collusion or asymmetric-frequency harm — see [[algorithmic-collusion]].

### DOJ — Agri Stats (2026) — meat-processing data-exchange consent decree

The second major U.S. algorithmic information-sharing antitrust decree, filed 2026 by DOJ + six state AGs (MN, CA, NC, TN, TX, UT) against Agri Stats, Inc. — a third-party benchmarking intermediary for the meat-processing industry (broiler chicken, pork, turkey). Structural parallel to RealPage: a hub-and-spoke data aggregator whose seller-only access model enabled coordinated pricing without explicit cartel communication. Full treatment at [[agristats-consent-decree]].

The remedy architecture is distinct from RealPage's: where RealPage's decree emphasises data-aging and geographic pricing restrictions, the Agri Stats decree introduces a **mandatory open/non-discriminatory access requirement** — any U.S. person may purchase reports at processor-equivalent pricing — combined with an anonymisation floor (≥3 contributors, no single contributor >70%) and a ≥45-day average data lag. This open-access remedy is contested: the American Prospect / Lee Hepner (AELP) argue it expands Agri Stats' customer base without dismantling the processor-ranking reports that actually drive coordination (see [[information-sharing-remedy-efficacy]] for the open conflict file).

**Mechanism:** Sherman Act Section 1 — information-sharing hub enabling tacit collusion. Differs from RealPage in that Agri Stats used explicit proprietary data-sharing (benchmarking reports), not ML-driven price recommendations.

**Transferable template:** the five-component remedy architecture (sales-data prohibition, anonymisation floor, data-aging, open access, court monitor) is enumerated with §IV/§VI/§VII/§VIII cites on [[agristats-consent-decree]] and constitutes a replicable design spec for information-sharing antitrust decrees across industries.

*(Sources: `raw/research/weekly-2026-05-18/02-02-agristats-doj-pr.md` — DOJ OPA press release; `raw/research/weekly-2026-05-18/09-09-agristats-proposed-final-judgment.md` — proposed final judgment text; `raw/research/weekly-2026-05-18/03-02b-agristats-prospect-critique.md` — American Prospect critique.)*

### FTC — JetBlue surveillance-pricing examination (April 2026)

The week of **April 21, 2026** produced the first federal regulatory response specifically on airline surveillance pricing. Trigger: a deleted JetBlue social-media reply to a customer complaining of a $230 fare increase, advising the customer to *"clear your cache and cookies or book with an incognito window"* — implicitly acknowledging cookie-based fare personalisation that JetBlue's official statement subsequently denied. *(See [[consumer-facing-dynamic-pricing|Airlines § JetBlue surveillance-pricing inflection event]] for full sequence.)*

Sequence:
- **April 21–22, 2026**: viral incident; federal class-action complaint filed in US District Court within 24 hours alleging surveillance pricing on commercial aviation — first such filing for the airline sector.
- **FTC Chair Andrew Ferguson** directed staff at Senate Commerce Committee to examine whether new disclosure rules are needed for airline pricing personalisation.
- **Multi-state legislative response**: surveillance-pricing prohibition / disclosure bills introduced in **NY, NJ, AZ, PA**. California Attorney General Rob Bonta's CCPA-purpose-limitation surveillance-pricing sweep (announced January 27, 2026) had named airlines among targeted sectors.
- Congressional letters from **Sen. Ruben Gallego** (D-AZ) and **Rep. Greg Casar** (D-TX) requesting agency action.

**Mechanism:** twin-track. (a) Federal class action under consumer-protection/state law theories testing surveillance-pricing as a deceptive/unfair practice. (b) FTC examination potentially leading to disclosure rulemaking. (c) State legislative stack pursuing prohibition or disclosure regimes per § 3 below.

**Reach:** the activation curve compressed from years (RealPage / Live Nation arc 2022–2026) to one week. *(Source: `weekly-2026-04-27/04-04-jetblue-surveillance-pricing-class-action.md` — Fortune, April 21 2026.)*

### FTC — surveillance-pricing 6(b) study
July 2024: FTC issued 6(b) orders to Mastercard, Revionics, Bloomreach, PROS, JPMorgan Chase, Task Software, Accenture, and McKinsey. January 2025: FTC released interim findings ("Issue Spotlight: The Rise of Surveillance Pricing" + redacted research summaries). Study ongoing. Full treatment at [[surveillance-pricing-retail]]. *(FTC Issue Spotlight; FTC Research Summaries.)*

**Mechanism:** 6(b) market inquiry — not enforcement. Intended to surface facts, enable research, and structure future rulemaking.

**Reach:** unclear. No enforcement action has followed; 6(b) studies historically lay groundwork for future rulemaking or referral to enforcement bureaus. The FTC has signalled continuing work ("Update & The Work Ahead" post, January 2025).

### DOJ — Live Nation / Ticketmaster (2024 → March 2026 settlement)
DOJ + 39 states + DC sued Live Nation/Ticketmaster May 2024 for unlawfully wielding control over concert promotion, artist management, venue operations, and ticketing. **March 2026: DOJ + several states settled for $280M** (service-fee caps at certain amphitheatres; greater venue flexibility on promoters/ticket distributors). 33 states + DC declined the settlement and continued the trial — see § 3 State AGs below for the April 2026 jury verdict. Notre Dame law professor Roger Alford characterised the outcome as "a massive win for the state AGs and an historic miss for the DOJ." *(NPR Apr 15 2026; AP via NPR.)*

**Mechanism:** Sherman Act monopolisation claim against vertical-integrated platform-pricing operator. The state-AG continuation pattern is what makes this load-bearing for design-input #3 (disclosure-complaint factory).

**Reach:** consent decree binds Live Nation to fee-cap and venue-flexibility terms; appellate motions still pending on the post-settlement state-AG track. Whether the settlement counts as "enough" relative to the underlying conduct was disputed by the National Independent Venue Association ("not significant enough to call a slap on the wrist").

## 2. Federal legislation (US)

### Preventing Algorithmic Collusion Act of 2024
US Senate bill targeting algorithmic pricing as a form of collusion. Referenced in both arXiv 2504.16592 and HBS 22-050. Status as of source capture: introduced, not enacted. *(arXiv; HBS.)*

### Proposed rent-algorithm bans
Congressional bills introduced following the 2022 ProPublica investigation would explicitly prohibit rent-setting algorithms. Status: pending. *(ProPublica.)*

### Fair Prices for Local Businesses Act (Senator Murphy, 2026)
Introduced April 2026 by Sen. Chris Murphy (D-Conn.) and colleagues. Strengthens the Robinson-Patman Act (RPA) — the 1936 anti-price-discrimination statute that has been largely dormant since DOJ/FTC enforcement collapsed in the 1980s. Key reforms:

- Eliminates the "meeting competition" defence that has enabled large retailers to demand preferential pricing
- Eases burdens of proof in enforcement actions (lowers the bar for plaintiffs)
- Extends RPA coverage to **services** including payment processing and delivery platforms — a structural expansion beyond the goods-only scope the Supreme Court's restrictive readings have produced
- Ensures meaningful damages for victims of price discrimination

Endorsed by Open Markets Institute (OMI). OMI Legal Director Sandeep Vaheesan: *"Giants like Amazon and Walmart use their market muscle to squeeze suppliers and their workers, extract discriminatory discounts and other concessions, and thereby gain an unfair and illegitimate advantage over rivals... This bill strengthens the existing Robinson-Patman Act by extending its coverage to services and undoing Supreme Court misinterpretations of the law."*

OMI's broader RPA-revival agenda (Vaheesan & Callaci 2023; Hanley 2023) has been cited by Sens. Warren and Blumenthal in pressing the FTC; then-FTC Commissioner Bedoya delivered a 2022 "Returning to Fairness" speech endorsing RPA-revival as priority. The Murphy bill is the first concrete legislative product of that frame.

**Mechanism:** Buyer-power suppression via revived classical antitrust statute. Targets the supply-side leverage that enables algorithmic personalisation downstream — if dominant retailers can't extract discriminatory wholesale terms, the data-driven targeting that consolidates their margin advantage faces a higher floor. *(OMI press release Apr 2026; bill text via Murphy Senate site.)*

**Status:** introduced; no committee mark-up scheduled as of April 2026.

## 3. State and municipal action (US)

### State AGs
Ten+ state AGs joined the DOJ's RealPage litigation; Washington State AG separately sued alleging Consumer Protection Act violations. Nine-state action settled against Greystar for $7M. *(ProPublica.)*

**State-AG continuation against Live Nation / Ticketmaster (April 2026 jury verdict).** When DOJ settled the Live Nation antitrust case for $280M in March 2026 (see § 1 above), 33 states + DC declined the deal and pursued the trial. **April 15 2026:** federal jury (SDNY, Judge Arun Subramanian) found Live Nation and Ticketmaster operated as a monopoly that harmed consumers and overcharged ticket buyers. NY AG Letitia James: *"A jury found what we have long known to be true: Live Nation and Ticketmaster are breaking the law and costing consumers millions of dollars in the process."* Live Nation has indicated it will appeal pending motions; remedies and damages phase to follow. The verdict establishes state-AG-led monopolisation litigation as a viable counter-power path even when DOJ settles short. *(NPR Apr 15 2026.)*

**DC AG separate consumer-protection track (April 2026).** A parallel — and structurally distinct — DC AG action against Live Nation resolved on April 21 2026 for **$9.9M** (up to $8.9M for affected DC consumers via claims process). DC AG Brian Schwalb's office found Live Nation violated the District's Consumer Protection Procedures Act from 2015 to May 2025 by: advertising deceptively low ticket prices that excluded mandatory fees until checkout; failing to disclose fee purpose / distribution / role in setting; and using a one-minute-inactive countdown clock with the message *"Tickets are selling fast. Get yours now before they're gone"* regardless of actual demand — a fake-scarcity dark pattern. Settlement terms require all-in pricing on the ticket-selection page (already partially implemented in response to the FTC's Rule on Unfair and Deceptive Fees) and itemised fee-purpose disclosure. **Pattern:** consumer-protection-statute liability runs in parallel to antitrust liability — same defendant, different doctrine, separate damages. *(Washington Times AI News Desk Apr 21 2026; OAG DC press release.)*

### NY Algorithmic Pricing Disclosure Act (A3008) — AG enforcement action (Jan 2026)

**Effective date: November 10, 2025.** Requires most companies that use algorithmic pricing — also called "surveillance pricing" — to disclose when customer personal data is used to set individualised prices. **Mandated disclosure phrase** (verbatim): *"THIS PRICE WAS SET BY AN ALGORITHM USING YOUR PERSONAL DATA."* **Placement standard**: must be **clearly and conspicuously** displayed **near prices** — not buried in fine print or accessible only via a click-through page. First US state-level disclosure regime for personalised pricing; structurally distinct from Maryland HB0895's prohibition regime (next subsection) — NY says *tell the consumer this is personalised*; Maryland says *you may not personalise at all in this sector.*

**First public enforcement action — Instacart demand letter (January 2026).** NY Attorney General **Letitia James** sent a public demand letter to Instacart citing the **December 2025 Groundwork Collaborative + Consumer Reports field study**:

| Quantitative anchor | Value |
|---|---|
| Sample | 437 shoppers across 4 cities |
| Methodology | shoppers added items to Instacart carts; prices recorded across the panel |
| Items offered at multiple prices simultaneously | ~73% |
| Average price differential between highest / lowest for the same item | 13% |
| Maximum observed differential (same product, same store, same time) | **23%** |
| Projected annual cost to a typical family of four | **~$1,200** |

The AG letter argues that Instacart's existing disclosure — buried on a fine-print-linked page rather than displayed near prices — does not satisfy the Act's "clearly and conspicuously" standard. The letter demands documentation of (1) Instacart's agreements with retail and food-brand partners on price-setting and discount automation; (2) the automated tools used to adjust prices and discounts (and the role of consumer data); (3) the specific price experiments identified by the Groundwork/CR study; (4) Instacart and its partners' compliance efforts under the Act.

**Behavioral state change.** Following the Groundwork/CR study's publication, **Instacart announced it was ending all "item price tests."** Carve-out: Instacart stated its retail and food-brand partners can still run "different types of promotions and discounts" — partner-level testing continues; only Instacart-level item price tests halted.

**Mechanism:** State-statutory disclosure requirement with AG enforcement; the AG letter operationalises a vague "conspicuous" standard into a **DOM-testable benchmark**: any browser-side audit tool can verify whether the literal mandated phrase appears near displayed prices. This is the most concrete-and-testable disclosure-compliance standard captured on the wiki — directly relevant to **Design-input #4** (algorithm-disclosure request tool) and **Design-input #1** (consumer-side pricing observatory) in the design-input candidates section below.

**Reach:** New York-only (jurisdictional). The behavioral evidence (Instacart halt) is the first documented case on this wiki of disclosure-law-plus-public-evidence shifting platform behaviour. Pairs with the [[noyb|NOYB cross-jurisdictional empirical pattern]] (83.5% Article 15 access-request failure in EU) as the empirical foil — disclosure laws underdeliver in production unless an enforcement actor takes a high-profile target.

*(Source: `raw/research/weekly-2026-05-04/03-04-ny-ag-instacart-investigation.md` — NY AG press release; cross-link [[industries/consumer-facing-dynamic-pricing|Grocery delivery — Instacart subsection]] for the empirical study + behavioural halt detail.)*

### Connecticut SB4 — data-broker registry + centralized deletion + surveillance-pricing disclosure (May 2026)

**Status:** passed Senate 31-4 on April 23 2026; passed House **141-6 on May 4 2026**; awaiting Governor Ned Lamont's signature (expected). Builds on the Connecticut Data Privacy Act (2022; CT was the fifth state to enact a comprehensive privacy law). Registry provisions effective **January 1 2027**. Lead author: Sen. James Maroney (D-Milford), co-chair of the General Law Committee and the bipartisan AI Caucus. Co-passed alongside Connecticut SB5 (AI regulation).

**Three load-bearing mechanisms:**

1. **State-run data-broker registry.** Defines a data broker as *"a business that sells or licenses brokered personal data to another person."* Mandatory enrollment for all such businesses operating in or targeting CT residents; mandatory fees fund the registry. Registry implemented by the **Connecticut Department of Consumer Protection (DCP)**.

2. **Centralized one-click deletion mechanism.** DCP is charged with creating a unified deletion mechanism spanning **all registered brokers** — a single consumer interface through which a CT resident can submit a deletion request that propagates to every enrolled broker. **First cross-broker API-equivalent surface in US law.** Structurally distinct from California's CPPA data-broker registry (separate per-broker deletion requests) and from prior state opt-out architectures (one-broker-at-a-time).

3. **Surveillance-pricing disclosure mandate.** *"Retail sellers and third-party delivery services prohibited from engaging in surveillance pricing unless they disclose when an automated pricing system increases a price using a consumer's personal data."* Plus regulations on geolocation data, facial recognition, and streaming-ad volume.

**Tooling-hook framing.** The centralized deletion mechanism is the load-bearing build target. A state-mandated cross-broker deletion API is exactly the substrate civil-society tooling has lacked: it shifts the "DSAR-coordination" lever (cf. [[strategies/data-disruption-strategy-map|Tier 1 #1]]; [[mechanisms/data-cooperatives]]) from per-broker bespoke pipelines (cf. [[organizations/noyb|noyb cross-jurisdictional 83.5% Article 15 failure]]) to a single regulated endpoint. Adjacent design-input: an automated submission tool (cf. **Design-input #4 — Algorithm-disclosure request tool** below) generalises directly onto this surface once DCP publishes the technical spec. The **Verifiable Mandate-Bound DSAR Pipeline** ([[strategies/mechanism-synthesis-readout|Build #2]]) gains a concrete first-target jurisdiction.

**Cross-state comparison.** Among the three enacted / advanced 2026 state laws on surveillance pricing:

| Statute | Architecture | Sectoral scope | Centralized data-rights infrastructure? | Enforcement |
|---|---|---|---|---|
| **NY APDA** (eff. Nov 10 2025) | **Disclosure** ("THIS PRICE WAS SET BY AN ALGORITHM USING YOUR PERSONAL DATA") | All retail / surveillance-pricing sectors | No (per-platform self-implementation) | AG (proven operative — Instacart halt) |
| **MD HB0895** (eff. Oct 1 2026) | **Prohibition** (categorical ban in sector) | Food retail >15,000 sq ft + 3rd-party delivery only | No | AG only; pre-empts MD CPA; no private right of action |
| **CT SB4** (registry eff. Jan 1 2027) | **Disclosure + cross-broker deletion API + broker registry** | Retail sellers + 3rd-party delivery (surveillance-pricing); all data brokers (registry/deletion) | **Yes — centralized DCP deletion mechanism** | (not specified in capture — see open question below) |

CT differs from MD on three dimensions: (a) it is **broader in scope** for the data-broker register/deletion (all sectors, not just food retail); (b) it has a **substantively different architecture** — the cross-broker deletion API is novel infrastructure, not just statutory text; (c) it adopts the **disclosure (not prohibition) approach** to surveillance pricing, aligning with NY rather than MD on that specific dimension. Together NY, MD, and CT establish that the state-legislative cluster is not converging on a single architectural pattern — three different theories of the case (disclose, ban, infrastructure-build) are running in parallel.

**Loophole assessment versus HB0895.** Applying the six-point Doctorow / Garofalo checklist (next subsection) to CT SB4 from the capture in hand:

- (a) **Scope beyond grocery** — yes; data-broker registry / deletion is **economy-wide**, not sectoral. Surveillance-pricing disclosure covers retail sellers + 3rd-party delivery (broader than MD's >15,000 sq ft food-retail floor; narrower than economy-wide).
- (b) **Consent-via-clickwrap blocked** — not specified in capture.
- (c) **Promotional / temporary-discount exemptions** — not specified in capture.
- (d) **Loyalty-card and subscription exemptions** — not specified in capture; loyalty-card / subscription carve-outs were the principal HB0895 vehicle-of-evasion, so this is the highest-priority gap to close on the bill text itself.
- (e) **Private right of action** — not specified in capture.
- (f) **No pre-emption** of stronger existing consumer-protection rights — not specified; CT Data Privacy Act (2022) is the existing baseline and the bill explicitly "builds off" it (suggesting layering, not pre-emption).

**Open question (enforcement architecture not captured).** The CT Mirror story is silent on enforcement mechanism — whether SB4 is AG-only (the MD pattern), private-right-of-action (the strongest), or shared with DCP (DCP runs the registry; it may also have enforcement authority). This is the binding question for whether the load-bearing deletion API is operative at scale. Flag for follow-up via bill text or AG / DCP follow-up sources.

**Effect on the wiki's MD-HB0895 framing.** The "load-bearing first-in-nation prohibition" framing was already qualified by the Doctorow / Garofalo carve-out taxonomy (next subsection) — qualified, not overturned. CT SB4 further broadens the picture: **MD remains the first-in-nation categorical prohibition** (different doctrinal theory); **CT becomes the first-in-nation centralized cross-broker deletion API** (different doctrinal theory; the strongest tooling hook of the three). No `wiki/conflicts/` file is warranted — MD and CT are doctrinally distinct, not contradictory.

*(Source: `raw/research/weekly-2026-05-11/02-ct-sb4-passage.md` — CT Mirror, May 4 2026 — "Consumer data privacy bill gets final passage in CT House." Supplementary cross-state framing: `raw/research/weekly-2026-05-11/06-md-hb0895-cfm-context.md` — Consumer Finance Monitor, May 5 2026.)*

### Maryland HB0895 — Protection From Predatory Pricing Act (2026)
Enacted April 2026; effective **October 1, 2026**. Cross-filed as SB0387; By Request of the Governor (Moore administration). 50+ House sponsors. **Substantive prohibition** (not disclosure):

- Bars **food retailers (>15,000 sq ft)** and **third-party delivery service providers** from engaging in dynamic pricing or using consumer personal data to set prices on consumer goods/services
- Bars use of **protected-class data** to offer, advertise, or sell consumer goods/services under certain circumstances
- Violations are unfair / abusive / deceptive trade practices, subject to enforcement and penalties

**First-in-nation US state-level prohibition** of personalised pricing in a major retail vertical. Categorically distinct from NY A3008's disclosure regime — NY says "tell the consumer this is personalised," Maryland says "you may not personalise at all in this sector." Sectoral scope (food retail + delivery platforms) is narrower than universal but targets exactly the verticals the FTC 6(b) study (see [[surveillance-pricing-retail]]) identified as most active in surveillance pricing. Colorado HB26-1210 (advanced out of Senate committee April 21 2026; floor vote scheduled April 24) extends a similar prohibition framework with the addition of wage-setting; suggests a state-legislative cluster forming. *(Maryland General Assembly HB0895 status page; Maryland Fiscal and Policy Note.)*

**Mechanism:** State-statutory prohibition with consumer-protection enforcement hook. Conceptually closest to a sectoral CCPA-style data-use restriction rather than to antitrust. The prohibition-not-disclosure stance is the load-bearing innovation — it removes the "the consumer was informed and consented" defence that disclosure regimes implicitly leave open.

**Reach:** Maryland-only (jurisdictional). The Colorado advance and the cross-filed SB0387 suggest replicability; food-retail-and-delivery scoping could be lifted by other state legislatures with minimal modification.

#### HB0895 loophole assessment (Doctorow / Garofalo, Apr 30 2026)

The "first-in-nation prohibition" framing is qualified by a substantive **loophole taxonomy** published by **Cory Doctorow** (Pluralistic, April 30 2026) synthesising **Pat Garofalo / American Economic Liberties Project** analysis of the bill text. Six named carve-outs, in the order Doctorow presents them:

1. **Grocery-only scope.** The Act covers food retailers (>15,000 sq ft) and third-party delivery providers only. Excluded: car rentals, apartments, healthcare, taxi/rideshare, quick-service restaurants, and **all other sectors where surveillance pricing is active**. Also entirely silent on **algorithmic wage discrimination** (gig-platform desperation-premium pricing on workers — see [[mechanisms/pricing-algorithm-taxonomy|Family 6 (Uber per-trip opaque)]]).
2. **Consent-based collection exemption.** Surveillance pricing is permitted if the purchaser "consents." In practice, consent is captured via clickwrap / ToS at the point of any *affiliated-service* interaction. Doctorow's example: a pet-care app owned by the same parent company as a grocer's pricing-tool vendor could capture consent to grocery surveillance pricing via a vet-appointment booking. Renders the prohibition subject to standard data-broker / cross-affiliate consent architecture — i.e. defeated by the **same consent-via-clickwrap problem documented for GDPR / GPC enforcement** (see § 9 webXray + NOYB pattern below).
3. **Promotional offers and temporary discounts.** Both terms are exempted; **neither is defined in the bill text.** Since retail pricing almost universally uses "sale," "temporary," or "promotional" labelling, this exemption is a near-universal override. Doctorow: *"it effectively grants every grocer in the state an easy way to evade the law entirely."*
4. **Loyalty-card exemption.** Explicitly carved out. Per Doctorow / Garofalo, **loyalty cards are already the dominant vehicle for surveillance pricing in grocery** (personalised pricing via membership tier, purchase-history inference, co-branded data-broker relationships). Exempting them removes coverage of the primary current form of the harm.
5. **Subscription-based pricing exemption.** Explicitly carved out alongside loyalty cards. Subscription pricing is a related delivery vehicle — membership fees unlock "lower" headline prices, with the price differential funded by data extraction and behavioural targeting.
6. **No private right of action + pre-emption of Maryland Consumer Protection Act.** Consumers cannot sue under HB0895; **only the Attorney General can enforce, and AG enforcement is discretionary.** Additionally, HB0895 **pre-empts existing rights under the Maryland Consumer Protection Act** — meaning Marylanders have *fewer* legal remedies for surveillance-pricing harm than before the bill was signed. Structurally the most consequential carve-out for enforcement reach.

**Net effect on the wiki's framing.** The "load-bearing first-in-nation prohibition" position is *qualified, not overturned*: the prohibition exists on paper; its enforcement reach is materially narrower than the political framing implies. **No `wiki/conflicts/` file is warranted** — this is a refinement, not a contradiction.

**Evaluation template for future state bills.** The carve-out taxonomy is a six-point checklist for assessing whether any future state surveillance-pricing bill (NY/NJ/AZ/PA, CA AB 2564, Colorado HB26-1210) is substantive or performative. Bills should be evaluated against:

- (a) **Scope** beyond grocery — does it cover the full range of surveillance-pricing-active sectors?
- (b) **Consent-via-clickwrap blocked** — does it require affirmative, granular, sector-specific consent?
- (c) **Promotional / temporary-discount exemptions** absent, or narrowly defined with statutory definitions?
- (d) **Loyalty-card and subscription exemptions** absent — covers the actual delivery vehicles?
- (e) **Private right of action** included?
- (f) **No pre-emption** of stronger existing consumer-protection rights?

**Strategy-layer implication.** If HB0895 is largely unenforced post-Oct-1 due to these carve-outs, the regulatory-proxy lever's near-term practical impact is lower than the wiki's current framing implies. This shifts strategy-layer weight on [[strategies/data-disruption-strategy-map]] toward (i) enforcement-pressure pipelines (NOYB-style mass-complaint factories, per Tier-1 #3) and (ii) tooling-side disruption that doesn't depend on AG action. The **complement**: the NY APDA case above shows that disclosure-plus-AG-enforcement *can* produce behavioural change (Instacart halt) — the binding question is enforcement willingness, not statute existence.

*(Source: `raw/research/weekly-2026-05-04/04-05-pluralistic-hb0895-loopholes.md` — Pluralistic / Cory Doctorow, "How not to ban surveillance pricing," April 30 2026, synthesising Pat Garofalo / American Economic Liberties Project analysis. Trust tag: moderate — editorially hostile but factual carve-out claims are specific and traceable to bill text; load-bearing legal characterisations should be cross-checked against the HB0895 text and Garofalo's primary piece for the strongest citations.)*

### Colorado HB26-1210 — Prohibit Surveillance Price & Wage Setting Algorithm (May 2026)

**Status:** Passed both chambers May 2026; pending Governor signature. Reengrossed (second-house amended) version is the operative text.

**Dual scope — the novel feature of this bill.** Colorado HB26-1210 targets a "price or wage setting algorithm" (PWSA): an AI/ML-based system that analyses **surveillance data** to set individualised consumer prices **or** worker wages. This dual consumer-pricing-and-wage-setting scope is not present in MD HB0895 (food retail only, silent on wages) or NY APDA (consumer pricing disclosure only). Maryland's HB0895 loophole taxonomy (point 1 above) explicitly flags that HB0895 "is entirely silent on algorithmic wage discrimination" — Colorado HB26-1210 fills that gap, at least nominally, on its face.

**"Surveillance data" definition.** The bill's definition covers: observation, inference, biometrics, online behaviours, and group/tier membership — explicitly targeting the data-brokerage and profiling layer, not just the pricing algorithm itself. This is a broader definition than the "personal data" framing in NY APDA.

**Enforcement: AG-only under the Colorado Consumer Protection Act.** HB26-1210 is enforced as a deceptive trade practice under the CCPA, with AG rulemaking authority. **The original bill included a private right of action** ("a person aggrieved by a violation … may bring a civil action on behalf of themself or a group of similarly situated persons to recover damages, costs, and reasonable attorney fees") — this language was **struck by Senate amendment** and is not present in the enacted (reengrossed) bill. The enacted bill is AG-enforcement-only, structurally similar to the NY APDA enforcement model. This is a significant doctrinal limitation: collective litigation strategy is not enabled by this statute as enacted.

**Worker data entitlements.** The bill imposes transparency and data-access obligations on PWSA operators: operators must publish accuracy procedures and give workers data-access and correction rights with respect to their own data used by the PWSA. This creates a DSAR-adjacent entitlement in Colorado — a lightweight audit obligation and a potential hook for DSAR-coordination tooling.

**Doctrinal position.** Among enacted 2026 state laws:

| Statute | Architecture | Scope | Wage-setting coverage | Enforcement |
|---|---|---|---|---|
| **NY APDA** (eff. Nov 10 2025) | Disclosure | All retail / surveillance-pricing sectors | No | AG (operative — Instacart halt) |
| **MD HB0895** (eff. Oct 1 2026) | Prohibition | Food retail >15,000 sq ft + 3rd-party delivery | No | AG only; pre-empts MD CPA; no private right |
| **CT SB4** (registry eff. Jan 1 2027) | Disclosure + cross-broker deletion API + registry | Retail + 3rd-party delivery (pricing); all data brokers (registry) | No | Not specified in capture |
| **CO HB26-1210** (May 2026) | Prohibition | Consumer pricing AND worker wage-setting | **Yes — dual scope** | AG only via CCPA; no private right (struck by amendment) |

Colorado aligns with Maryland on the prohibition model and with New York on AG-only enforcement, while adding the wage-setting axis that no prior state bill covers. The operative scope will be set by AG rulemaking — creating an advocacy target beyond the bill text itself.

*(Source: `raw/research/weekly-2026-05-18/01-01-co-hb1210-bill.md` — Colorado General Assembly official bill page; reengrossed version. Trust tag: authoritative / primary — bill text and legislative record. Note: the reengrossed version incorporates Senate amendments; the private-right-of-action language visible in strikethrough form in the legislative record was explicitly removed.)*

### Municipal bans
San Francisco, Philadelphia, and Minneapolis have moved to bar landlord use of algorithmic rent-setting software. *(ProPublica.)*

## 4. International

### EU
- **Digital Markets Act (DMA) and Digital Services Act (DSA)** — operational; framework for platform regulation. Not yet addressing algorithmic pricing collusion specifically per arXiv's survey.
- **European Commission** — investigating Ticketmaster's dynamic pricing (parallel to UK CMA). *(Wikipedia.)*

#### EU DMA — Google search-data sharing (April 16, 2026)

The European Commission issued **preliminary findings** under DMA Article 6(11) requiring Google to share search data with third-party search engines on **fair, reasonable, and non-discriminatory (FRAND)** terms. The 29-page field-level specification is the **first regulated, priced access surface for commercial search-intent data**.

**Scope of the proposed measures:**
- **Eligible "data beneficiaries"** include third-party search engines and **AI chatbots with search functionality** (explicitly named).
- **Data fields covered**: ranking signals, query data, click data, view data — the full behavioural training substrate for search relevance.
- **FRAND pricing parameters** to be set by the Commission for the access regime.
- **Anonymisation requirements** for personal data within the shared feed.
- **Auditing and access processes** to govern beneficiary use.

**Status / timeline:**
- Preliminary findings published April 16, 2026.
- **Public consultation closes May 1, 2026.**
- **Final decision expected July 27, 2026.**

**Mechanism:** state-mandated data-access regime functioning as a regulator-imposed alternative to the cooperative-pricing approach in [[mechanisms/data-market-mechanism-design]] (Shapley-based revenue allocation among voluntary contributors). FRAND is regulator-set and firm-facing; Shapley is cooperative and contributor-facing. The two **bracket the design space for priced data access** — regulated-price vs cooperative-price.

**Strategic relevance.** If finalised, this is the first time commercial search-intent data is regulated-access-shared with third parties. Build #1 (Federated Pricing Observatory) on [[strategies/mechanism-synthesis-readout]] currently has no clean substrate; mandated FRAND access is a **candidate substrate**. Tier-1 #3 on [[strategies/data-disruption-strategy-map]] (probe-and-publish observatory) similarly gains a regulated-access surface that lowers adversarial data-acquisition cost. The public consultation is open — design-input opportunity for positioning cooperative access. *(Source: `weekly-2026-04-27/03-03-eu-dma-google-search-data-sharing.md` — EC DG COMP / DG CONNECT press release, April 16 2026.)*

### UK
- **Competition and Markets Authority (CMA)** — investigating Ticketmaster's 2024 Oasis-tour dynamic pricing; concluded Ticketmaster "may have misled" fans. *(Wikipedia.)*
- **Advertising Standards Authority** — received complaints on the same Oasis tour. *(Wikipedia.)*

#### CMA Direct Consumer Enforcement — Year One readout (April 2026)
The CMA's new direct-enforcement regime under the Digital Markets, Competition and Consumers Act 2024 (DMCC Act) completed its first year April 2025–April 2026. Reported numbers:

| Metric | Year-1 figure |
|---|---|
| Investigations opened | 14 |
| Settlements concluded | 2 |
| Consumer refunds ordered | £760,000 |
| Fines imposed | £4.7M |
| Advisory / warning letters issued | 157 |
| Information notices sent | 46 |

**Three target areas:** drip pricing, fake reviews, online choice architecture (OCA). **First substantive penalty:** AA Driving School + BSM Driving School (both owned by Automobile Association Developments Ltd) admitted liability for drip pricing — £760K refund to learner drivers + £4.2M fine (April 2026). On fake reviews: 54 publishers swept; 90% revised policies after advisory letters; 5 firms now under investigation. On OCA: investigations into default optional charges and false time-limited offers; cross-regulator coordination via Digital Regulation Cooperation Forum and ICPEN.

**Year-2 priorities** (CMA-stated): price transparency (no hidden / dripped / partitioned pricing); fake-review compliance; consumer-contract terms (especially exit fees); subscription contracts (new rules expected Spring 2027); AI-agent consumer-law compliance.

**Pattern:** the UK CMA is operationally the most active consumer-protection-enforcement regulator on dynamic-pricing-adjacent practices in this window — both in headline penalty (AA Driving School is the first substantive financial penalty under the new powers) and in volume (157 advisory letters / 46 information notices is a continuous-pressure shape, not an episodic-enforcement shape). Adobe early-cancellation-fees investigation flagged as next standalone case. *(CMA blog "Direct consumer enforcement: one year on," April 17 2026.)*

### Policy papers
France, Germany, Denmark, Japan, Norway, and Sweden have each published policy papers on algorithms and competition, per arXiv 2504.16592. None have (as of source capture) produced implemented regulation specifically addressing algorithmic collusion.

## 5. Litigation (non-governmental)

- **Private tenant class actions** against RealPage and landlords. Greystar settled a class action for $50M. More than two dozen property-management companies have reached settlements. *(ProPublica.)*
- **2022 ProPublica investigation** sparked dozens of federal tenant lawsuits — the journalism-to-litigation pipeline as counter-power mechanism.

### 5a. CFAA / Van Buren / hiQ doctrine — legal space for consumer-automation tools

The Computer Fraud and Abuse Act (18 U.S.C. §1030) has historically been the primary federal-criminal hammer against automated tools that interact with commercial websites against ToS. Two rulings narrowed this materially between 2021 and 2022 and are load-bearing for any consumer-side automation lever.

- ***Van Buren v. United States***, 141 S. Ct. 1648 (2021). Supreme Court held: violating a site's ToS or internal policies while accessing data the user is otherwise authorized to access is *not* "exceeding authorized access" under the CFAA. The Court's "gates-up-or-down" test: CFAA liability attaches to getting past an access gate (authentication), not to using already-accessed data in a forbidden way.
- ***hiQ Labs, Inc. v. LinkedIn Corp.***, 2022 U.S. App. LEXIS 10349 (9th Cir. 2022, on remand). Ninth Circuit held, applying *Van Buren*: "it is likely that when a computer network generally permits public access to its data, a user's accessing that publicly available data will not constitute access without authorization under the CFAA." Public websites "have 'no gates to lift or lower in the first place' because... [they] are open to anyone with a web browser."

Practical implication for consumer tools that automate interaction with public pricing pages (transparency overlays, pricing observatories, per-session-rotation tools, decoy-traffic generators): **CFAA is not the first-line federal risk it was pre-2021**. *(White & Case 2022 legal memo, captured `obfuscation-deep-dive/09-11-whitecase-hiq-vanburen-cfaa.md`.)*

**What remains unchanged:** the Ninth Circuit explicitly preserved "potential claims against web scrapers under other theories, including trespass to chattels, copyright infringement, misappropriation, unjust enrichment, conversion, breach of contract or breach of privacy claims." Retailers can still sue. And: authenticated endpoints (logged-in views, loyalty dashboards, member portals) remain a CFAA "gates up" surface — automation against them has significantly more risk. Circuit split on CFAA "without authorization" persists outside the Ninth Circuit.

See [[obfuscation|Obfuscation — Legal-risk layer]] for the strategic read.

## 6. Investigative journalism

- **ProPublica** — October 2022 "Rent Barons" series on RealPage; continuing coverage through the 2025 settlement. Credited by DOJ prosecutors.
- **ProPublica** (earlier) — Princeton Review SAT-prep discriminatory pricing; Amazon pricing algorithm investigations. *(Wikipedia; ProPublica.)*
- **The Markup** — founded 2019 with $23M+ from Craig Newmark Philanthropies, Knight Foundation, and journalism philanthropies specifically to investigate algorithmic systems. Julia Angwin and Jeff Larson, its founders, pioneered the data-journalism-on-algorithms genre at ProPublica (Facebook discriminatory advertising; COMPAS criminal risk scores).

Journalism is a recurring counter-power *initiator* — it surfaces cases that regulators and plaintiffs then pick up.

## 7. Consumer and producer backlash

Not a coordinated movement, but a recurring pattern. Each episode below produced a measurable response:

| Episode | Year | Outcome |
|---|---|---|
| Uber surge pricing during NYC snowstorm (8× normal) | 2013 | Uber voluntarily capped emergency surge pricing (2015). |
| Heart of Midlothian FC season-ticket dynamic pricing | 2012 | Fan backlash; practice rolled back. |
| Ticketmaster dynamic pricing (Springsteen $4–5k) | 2022–2024 | UK CMA investigation; EU Commission investigation; artist defections. |
| Wendy's AI dynamic-pricing announcement | 2024 | Forced clarification: "only to lower prices in low-traffic periods." |
| Crowded House (promoter used dynamic pricing without band approval) | 2020 | Band publicly demanded refunds for fans. |

**Artists publicly refusing dynamic pricing:** Coldplay, Taylor Swift, Ed Sheeran, Iron Maiden, Robert Smith. *(Wikipedia.)*

The pattern suggests that **public disclosure** — whether by a journalist, a regulator, or an artist — is often the operative lever.

## 8. Exit-alternative — platform cooperatives

Rather than regulating extractive platforms, the exit-alternative lane builds parallel institutions with different ownership. See [[platform-cooperatives]] for the full treatment; highlights relevant as counter-power:

- **[[drivers-cooperative]] (NYC, 2021–)** — worker-owned rideshare. 15% commission vs Uber/Lyft's 25–40%; drivers receive profit as dividends. Current focus: paratransit and Non-Emergency Medical Transportation.
- **[[coopcycle]]** — federation of 72 bike-delivery worker cooperatives across 12 countries. The OECD's featured case for how second-level (federation) cooperatives address the capital-conundrum scaling problem.
- **MIDATA.coop (Switzerland)** — data cooperative for personal health data, jointly created by ETH Zurich and Bern University. Direct template for a buyer-side data cooperative on pricing data (see design-input #2 below).
- **[[mondragon]]** — the pre-digital foundational model. Nearly 70 years of operation, ~70,000 workers, 10% solidarity-fund mechanism, 3:1–9:1 wage-ratio cap. Cited by platform-coop advocates as proof-of-concept that cooperative federations can reach material scale.

**Policy support for the exit lane:**
- Colorado UCLAA (Uniform Limited Cooperative Association Act) enables investor-member cooperatives — partial solution to the capital conundrum.
- Berkeley Worker Cooperative Revolving Loan Fund (2016) — public below-market-rate loans.
- Barcelona "La Communificadora" (2015) — entrepreneurship training and match-funding for platform coops.
- NYC Council Brad Lander 2016 report "Raising the Floor for Workers in the Gig Economy" presents platform cooperativism as a gig-worker-protection model.
- USDA *Rural Cooperatives* Sep/Oct 2016 endorsement.
- UK Corbyn 2016 Digital Democracy Manifesto — National Investment Bank financing for platform coops.

**Known limits** (documented on [[platform-cooperatives]] without resolution): Srnicek / Morozov / Pollock argue the capital conundrum and network effects make scale impossible. OECD 2023 takes a middle position — "unique solutions with positive impact, but their scale remains limited." The exit lane is real but partial.

## 9. Consumer-side data pooling and collective bargaining

The orientation-toward-governance-or-bargaining lane. Where [[platform-cooperatives|section 8]] builds parallel platforms, this section documents the structural counterweight to *data pooling itself*: buyer-, tenant-, or subject-side aggregation of data under cooperative ownership or negotiation-intermediary legal shells. Covered in depth on the dedicated mechanism pages.

### Governance mode — data cooperatives

[[data-cooperatives]] is the anchor mechanism page. Per the Ada Lovelace Institute's 2021 working-group report and Mendonça et al. (arXiv 2504.10058, 2025), four legal mechanisms for data stewardship are distinguishable: data trusts, data cooperatives, data commons, and data unions. Data coops are member-owned organisations that pool data and govern its use democratically under the ICA's seven cooperative principles.

**Live cases captured in the wiki:**
- **[[midata]]** (Switzerland, 2015–) — health-data cooperative; open-source platform (Open MIDATA Server, GPLv3); the OECD-cited canonical example.
- **[[drivers-seat-cooperative]]** (US, 2019–) — driver-owned data cooperative for rideshare/delivery workers; incorporated as a Limited Cooperative Association (LCA). **Sunset as a standalone org:** driversseat.co homepage returns a Squarespace "account expired" page as of 2026-04-21; activity migrated to the Workers' Algorithm Observatory at Princeton. Illustrates both the model's promise and its sustainability challenges.
- **The Good Data** (UK, DISSOLVED) — registered under the UK Co-operative and Community Benefit Societies Act 2014; dissolved because Google rejected its Chrome extension and it failed to recruit enough members. Documented on [[data-cooperatives]] as a cautionary case.
- **Salus Coop** (Barcelona, 2017) — health-data coop with the "Common Good Data License for Health Research" produced through crowd-design.
- **JoinData** (Netherlands, agriculture) — farmer data cooperative against agribusiness technology lock-in.

**Uptake challenges** (Ada Lovelace 2021): resonance, mobilisation, trust, and capacity. **Scale challenges:** democratic-control friction, governance-failure vulnerability (Mountain Equipment Co-op 2020 sale to US private equity cited as precedent), financial sustainability.

### Bargaining mode — collective bargaining and individual algorithmic bargaining

[[collective-bargaining-for-data]] is the bargaining-lane anchor page, covering two sources:

- **Vincent, Prewitt & Li (arXiv 2506.10272, 2025)** propose **Collective Bargaining in the Information economy (CBI)**: trusted data intermediaries representing classes of information producers negotiate with AI operators over terms of data use. The paper argues this is needed to prevent a "capital singularity" of AI-driven power concentration, and proposes specific safe-harbour and Parker-Immunity tooling to enable the intermediary form.
- **Porat (Harvard/NYU, 2024)** shows experimentally that **consumers can strategically "bargain" with pricing algorithms via purchase abstention** and strategic exercise of cookie and erasure rights. Disclosure mandates amplify this effect. Individual mechanism; bounded and produces deadweight loss without coordination.

### Consumer collective bargaining and group purchasing

[[consumer-collective-bargaining]] is the anchor mechanism page. Covers four structurally distinct aggregation mechanisms:

- **Group Purchasing Organisations (GPOs)** — standing intermediaries that aggregate buyer demand. In US healthcare: **600+ GPOs; ~90% of hospital purchases; Vizient / Premier / HealthTrust manage procurement for ~90% of medical equipment.** Congress granted healthcare GPOs anti-kickback **Safe Harbor in 1986**; admin-fee cap 3.0%. Structural critique: the admin-fee funding model creates incentive-incompatibility concerns (Elhauge 2002, 2003; GAO 2002 found GPOs sometimes increased hospital costs by up to 37%). Defence: Blair & Durrance (2013) analyse monopsony / exclusion / funding concerns and conclude GPOs are procompetitive on net; Hovenkamp similarly supportive.
- **Consumer cooperatives** — member-owned aggregation. Rochdale Society (1844) is the foundational lineage. Live US cases: [[park-slope-food-coop]] (17K members, member-labour model, 25% markup vs 26–100% at supermarkets) and [[rei]] (181 stores across 41 states; member-dividend rebranded to store-credit-only in 2022 — an instance of cooperative drift).
- **Transactional group-buying** — per-deal aggregation via social platforms. Tuángòu origins in China; Pinduoduo integrated with WeChat is the live large-scale success. Groupon-era US daily-deal platforms collapsed: 500+ sites by 2010, Groupon revenue declined 80% from $3B in 2014 to $600M in 2022.
- **Public-agency aggregation** — [[community-choice-aggregation]] (US electricity). 9 authorising states; **~15% of Americans served across 1,850+ municipalities as of 2024**. Opt-out default enrolment; governance by elected officials; California CCAs voluntarily procured 11 TWh of renewable electricity *above* state RPS mandates (2011–2018 per UCLA Luskin Center). The only authorising vehicle captured in this wiki that achieves large-scale default aggregation without membership recruitment.

### Independent compliance audits — GPC enforcement gap (April 2026)

**webXray California GPC audit** (published The Markup, April 21, 2026). Audit of **7,634 California-reachable websites** from a California IP, with the Global Privacy Control opt-out signal active. Methodology: dual-scan (signal-on / signal-off) with cookie inspection. Conducted by webXray (founded by former Google privacy engineer Tim Libert).

| Tracker | Continued tracking despite GPC | Notes |
|---|---|---|
| Google | **86%** | Spokesperson rebuttal; Google claims compliance |
| Meta | **69%** | "Fail to check for the signal at all" per audit; Meta no comment |
| Microsoft | **50%** | Operational-necessity carve-out claim |
| One unnamed third-party compliance vendor | **>90%** | Industry-wide pattern, not edge-case errors |

**Penalty exposure:** webXray estimates that if the California Privacy Protection Agency (CPPA) fined every site found non-compliant, it could result in **billions of dollars in penalties**. CPPA Director Tom Kemp's response: *"While we don't have comment on the finding of this specific report, we do appreciate that the report brings visibility to the importance of opt-out rights."* No enforcement action announced.

**Cross-jurisdictional empirical pattern.** The webXray finding is structurally parallel to NOYB's **83.5% GDPR Article 15 access-request failure** finding (April 16, 2026). Same structural pattern (high-rate non-compliance with statutory consumer-side data rights), two regulatory regimes (CCPA / GPC in CA; GDPR Art. 15 in EU). Together they establish: **paper rights underdeliver in production at industrial scale, generalising across jurisdictions and mechanisms.** This is the most quantified empirical baseline currently captured on the wiki for the regulatory-proxy lever cluster's enforcement-gap problem. *(Source: `weekly-2026-04-27/01-01-themarkup-webxray-california-gpc-audit.md` — The Markup, April 21 2026; cross-link [[noyb|NOYB cross-jurisdictional empirical pattern]] and [[browser-fingerprinting|PETS 2026 CCPA-Android opt-out paper]].)*

**Strategic implication.** The "legal opt-out at scale" lever (GPC + statutory rights) is not currently operative at population scale. This shifts weight in [[strategies/data-disruption-strategy-map]] toward (a) mass-complaint enforcement-pressure pipelines (cf. NOYB) and (b) tooling-side disruption levers that don't depend on platform compliance with opt-out signals.

### Transparency / crowdsourced-audit tools

The [[transparency-tools]] mechanism page is the anchor. Three functional sub-categories of live transparency tools:

- **Single-seller price-history trackers** — [[keepa]] (4M Chrome Web Store users; Amazon-only coverage across 11 locales; Keepa GmbH, Germany) is the leading example. Structural position: individual-level, single-platform, informational only. CamelCamelCamel is a free competitor.
- **Crowdsourced audit / observatory** — [[markup-citizen-browser]] (The Markup, launched October 2020; 1,000+ paid panelists; custom desktop app with Trail-of-Bits-audited redaction pipeline; focused on Facebook/YouTube feed algorithms). The closest live template for a pricing observatory per design-input #1. Also: **[[open-tenant-screening]]** (OpenTSS, MIT + Mozilla-funded) — crowdsourced tenant-screening audit; the tenant-side transparency counter to [[rental-housing-algorithmic-pricing|RealPage]]-class aggregation.
- **Academic-methodological foundation** — Hannak et al. (Northeastern, IMC 2014), *Measuring Price Discrimination and Steering on E-commerce Web Sites*: 16 sites, 300 AMT users + synthetic accounts, evidence of personalisation on 9 of 16 sites (Orbitz, Cheaptickets, Expedia, Hotels.com, Home Depot, Travelocity, Priceline among others). All crawling/parsing code and raw data open-sourced at `personalization.ccs.neu.edu`. Full treatment on [[transparency-tools]].

**Failure modes documented in captured sources** (both generic to the class):
- *Extractive drift.* [[paypal-honey]] — acquired by PayPal for ~$4B in 2020, exposed from December 2024 for cookie-stuffing affiliate-link hijacking, coupon-manipulation, and evasion code. Lost ~8M Chrome Web Store users by end of 2025. Triggered Google Chrome Web Store policy change in March 2025 prohibiting extensions from claiming affiliate commissions without providing discounts — a structural-regulatory response at the browser-platform level.
- *Acquisition-and-sunset.* [[fakespot]] — review-authenticity analyser, acquired by Mozilla May 2023, **shut down July 1, 2025** (Review Checker inside Firefox shut down June 10, 2025). Mozilla's stated reason: "While the idea resonated, it didn't fit a model we could sustain." Same sustainability pattern as the Ada Lovelace 2021 report flags for [[data-cooperatives]].

## 10. Academic-proposed remedies (editorial context, not enacted)

- **HBS 22-050:** price-setting frequency caps (e.g., weekly limit on price changes); algorithm transparency/auditing; pre-deployment testing.
- **arXiv 2504.16592:** detection tooling (statistical signatures of algorithmic collusion in market data); real-time monitoring; algorithm disclosure and compliance audits.

These are proposals, not law. See [[algorithmic-collusion]].

## Consumer counter-weight mechanisms at a glance

*(editorial — synthesis across sections 5–9 of this page and the dedicated mechanism pages.)*

A design-input cheat sheet for the full set of counter-weight mechanisms documented elsewhere in this wiki. Read each row as "form → who captures the gain → canonical example":

| Mechanism | Structural form | Captured gain accrues to | Example |
|---|---|---|---|
| **Transparency tool (single-seller)** | Informational, individual | Individual consumer | [[keepa]] |
| **Crowdsourced observatory** | Informational, aggregate | Public / regulators | [[markup-citizen-browser]], [[open-tenant-screening]] |
| **Data cooperative** | Governance, member-owned | Members | [[midata]] |
| **Trusted data intermediary (CBI)** | Bargaining, class-representing | Class of consumers | proposal only ([[collective-bargaining-for-data]]) |
| **Consumer cooperative** | Standing membership | Members (dividend / lower prices) | [[park-slope-food-coop]], [[rei]] |
| **GPO (consumer-side)** | Standing intermediary | Mixed — see funding-mechanism critique | healthcare GPOs ([[consumer-collective-bargaining]]) |
| **Transactional group-buying** | Per-deal aggregation | Consumer + platform | Pinduoduo, Groupon ([[consumer-collective-bargaining]]) |
| **Public-agency aggregation** | Opt-out default, public | Jurisdiction residents | [[community-choice-aggregation]] |
| **Platform cooperative (exit)** | Parallel institution | Worker-members | [[drivers-cooperative]], [[coopcycle]], [[mondragon]] |
| **Individual algorithmic bargaining** | Transactional, individual | Individual | Porat 2024 on [[collective-bargaining-for-data]] |
| **Class action** | Litigation | Class members | Greystar $50M settlement ([[rental-housing-algorithmic-pricing]]) |
| **Consumer / artist backlash** | Reputational pressure | Public | Coldplay, Swift, Wendy's walkback (§ 7 above) |
| **Journalism pressure** | Disclosure / investigation | Public / regulators | ProPublica, The Markup (§ 6 above) |

The table is deliberately flat — it does not rank by leverage. For design-ranked opportunity assessment see the **Design-input candidates** section below. For industry-side problem assessment see [[dynamic-pricing-overview]] and its industry links.

## What exists vs what is missing

*(editorial — synthesised across sources.)*

**Exists and working:**
- Antitrust enforcement against explicit shared-tool coordination (RealPage).
- Section 6(b) inquiries as fact-finders (FTC surveillance pricing).
- Journalism-to-litigation pipeline (ProPublica → tenant suits → DOJ).
- Artist- and consumer-level public refusals as reputational lever.

**Exists but weak:**
- Federal legislation (Preventing Algorithmic Collusion Act introduced, not enacted).
- State disclosure regimes (NY A3008 is the first-mover disclosure regime; Maryland HB0895 — see § 3 above — is a *categorically different* first-mover prohibition regime in food retail / delivery; Connecticut SB4 (May 2026) adds a third architecture — disclosure-plus-infrastructure, with the **first-in-nation centralized cross-broker deletion mechanism**; Colorado HB26-1210 advancing similar prohibition with wage-setting addition. Cluster forming around three distinct theories of the case (disclose, ban, build-infrastructure), but still under-replicated nationally).
- EU platform rules (DMA/DSA) — scope covers the large platforms but does not specifically reach algorithmic pricing collusion.
- **Platform cooperatives as an exit lane** — structurally viable ([[mondragon]] at ~70K workers, [[coopcycle]] at 72-coop federation) but the capital conundrum keeps the scale limited against VC-funded incumbents. Works best in sectors meeting Sundararajan's conditions (see [[platform-cooperatives]]).

**Missing:**
- **No clean legal theory for tacit algorithmic collusion.** The hardest variant is unaddressed by current antitrust law in either the US or EU.
- **No clean legal theory for asymmetric-frequency harm.** HBS's theoretical contribution has no enforcement hook yet.
- **No standing consumer-side detection tooling.** Aside from academic studies (Assad et al.), there is no continuous real-time observation of algorithmic pricing behaviour across industries.
- **No collective-bargaining analogue at scale for consumers against personalised pricing.** Sellers pool data (via intermediaries like RealPage or Revionics); buyer-side data cooperatives exist ([[midata]], [[drivers-seat-cooperative]], and dissolved cases on [[data-cooperatives]]) but none target personalised pricing specifically. CBI-style trusted data intermediaries (see [[collective-bargaining-for-data]]) are proposed but not implemented. **[[open-tenant-screening]]** is the closest partial instance in the tenant-screening subdomain. **Note:** healthcare GPOs demonstrate aggregation-against-supplier works at national scale (90% of hospital purchases), but with structural limits (intermediary-layer concentration, admin-fee funding-mechanism concern). See [[consumer-collective-bargaining]].
- **Public-agency aggregation is under-exploited outside electricity.** [[community-choice-aggregation]] serves ~15% of Americans for electricity (9 states, 1,850+ municipalities). No comparable opt-out default aggregation exists for broadband, insurance, pharmaceuticals, or data-privacy. Among the highest-leverage policy gaps captured in this wiki — an opt-out mechanism would materially change the uptake-vs-control tradeoff that opt-in coops / data coops face. *(editorial)*

## Design-input candidates *(editorial — the high-priority layer for this wiki's querying lens)*

Prioritised by closeness to existing gaps in counter-power infrastructure:

1. **Consumer-side pricing observatory.** Continuous crowd-sourced capture of prices seen by real shoppers across major retailers and sectors. Publishes:
   - Price-change frequency per retailer/category (detects HBS asymmetric-frequency harm).
   - Price dispersion conditional on browser fingerprint / device / location (detects personalisation).
   - Statistical collusion signatures (Assad-et-al.-style duopoly/monopoly asymmetries).
   - A "personalised-pricing exposure score" at the category level.
   **Methodology template:** Hannak et al. 2014 (Northeastern, IMC) — 16 e-commerce sites, 300 AMT users + synthetic accounts, control for non-personalisation noise. Found personalisation on 9 of 16 sites; some prices varied by hundreds of dollars. All code and data open-sourced at `personalization.ccs.neu.edu`. Full treatment on [[transparency-tools]]. A "Hannak at scale, continuously" is effectively the target architecture for this design-input. **Operational template:** [[markup-citizen-browser]] — standalone desktop app, 1,000+ paid demographically-representative panelists, Trail-of-Bits-audited redaction pipeline, published methodology + data + code, co-reporting partnership with an investigative newsroom (The Markup/NYT pattern). **Adjacent domain precedent:** [[open-tenant-screening]] — crowdsourced tenant-screening audit in the tenant-screening-vendor subdomain. **Funding models to budget for:** extractive drift (see [[paypal-honey]]), acquisition-and-sunset (see [[fakespot]]); the cooperative-governance alternative is on [[data-cooperatives]]. Feeds into FTC / CMA / EU investigations.

2. **Buyer-side data co-op.** The direct counterweight to seller-side data pooling. Consumers contribute anonymised purchase data, offer/counter-offer data, and pricing observations; the co-op returns a "fair price" estimate and flags outliers. Governance as a [[data-cooperatives|data cooperative]] (internal-governance orientation) with an optional [[collective-bargaining-for-data|CBI]] (Vincent, Prewitt & Li 2025) bargaining mandate (external-negotiation orientation). **Precedents to copy:** [[midata]] (Switzerland health-data coop) demonstrates the governance pattern and open-source platform stack; [[drivers-seat-cooperative]] (US driver-owned data coop, sunset) demonstrates both a relevant domain (gig-worker data pooling) and the sustainability-failure mode to avoid; [[coopcycle]] demonstrates the federation-first architecture for technical/marketing infrastructure; [[open-tenant-screening]] demonstrates the crowdsourced data-collection pipeline (without cooperative governance yet). **Practical legal vehicles:** Colorado Limited Cooperative Association (LCA) in the US; UK Co-operative and Community Benefit Societies Act 2014 for member-benefit coops, or Community Benefit Society form for wider-community purpose. **Applications:** rent (tenant version of RealPage, referencing [[rental-housing-algorithmic-pricing]] outcomes and [[open-tenant-screening]]'s methodology); major-appliance and car purchases; insurance; subscription services. **Challenges to budget for** (per Ada Lovelace 2021 and Mendonça et al. 2025): resonance/mobilisation/trust/capacity at uptake; democratic-control friction and governance-failure risk at scale; financial sustainability (coops rarely raise external capital).

3. **Disclosure-complaint factory.** One-click regulatory submissions. Pre-drafted text per regulator (FTC complaint form; CMA super-complaint format; EU Commission consumer portal; state AG consumer protection filings). Plug-in modules per pricing scandal. Industrialises the episodic consumer-backlash pattern into a sustained complaint flow.

4. **Algorithm-disclosure request tool.** Once any jurisdiction enacts algorithm-disclosure law (NY-style), a tool that lets individuals and consumer groups submit disclosure requests at scale. Lowers the administrative barrier to using new disclosure regimes.

5. **Event-ticket refusal registry.** A public registry of artists, venues, and sports teams that have refused dynamic pricing, updated via structured artist/venue submission and public verification. Queryable by consumers before purchase; referenced by future artists/venues considering their own policy.

6. **Tenant-metro signal aggregator.** Sector-specific version of #1. In metros with high RealPage or equivalent penetration, aggregate anonymised tenant data to detect continued coordination post-settlement, and route signals to the court-appointed monitor's compliance reporting.

## Source

- `raw/research/dynamic-pricing-landscape/01-doj-realpage-lawsuit.md` — DOJ press release, August 2024.
- `raw/research/dynamic-pricing-landscape/02-propublica-realpage-settlement.md` — ProPublica, late 2025 settlement coverage + retrospective on the full case arc.
- `raw/research/dynamic-pricing-landscape/03-wikipedia-dynamic-pricing.md` — Wikipedia, as the catalogue of consumer-backlash episodes across industries (used here for the tabulated cases).
- `raw/research/dynamic-pricing-landscape/04-ftc-issue-spotlight.md` — FTC Office of Technology, January 2025.
- `raw/research/dynamic-pricing-landscape/05-ftc-research-summaries.md` — FTC staff, January 2025 (redacted).
- `raw/research/dynamic-pricing-landscape/06-nber-algorithmic-pricing.md` — NBER working paper (Zeithammer et al.), 2024/2025.
- `raw/research/dynamic-pricing-landscape/07-hbs-dynamic-pricing-harm.md` — HBS working paper 22-050 (MacKay and Weinstein) — source of frequency-cap and algorithm-audit proposals.
- `raw/research/dynamic-pricing-landscape/08-arxiv-algorithmic-collusion.md` — arXiv 2504.16592 — source of the international-policy-paper list and the detection/monitoring/accountability research agenda.

Additional sources for section 9 (consumer-side data pooling and bargaining):

- `raw/research/consumer-data-pooling/05-01-ada-legal-mechanisms.md` — Ada Lovelace Institute / UK AI Council, 2021. Legal-mechanisms framework for data stewardship.
- `raw/research/consumer-data-pooling/06-02-arxiv-data-coops-governance.md` — Mendonça, Di Marzo, Abdennadher 2025. Data-cooperative frameworks and comparison table.
- `raw/research/consumer-data-pooling/07-07-arxiv-collective-bargaining.md` — Vincent, Prewitt, Li 2025. CBI position paper.
- `raw/research/consumer-data-pooling/08-08-porat-bargaining-algorithms.md` — Porat 2024 (Harvard/NYU). Experimental work on consumer bargaining with pricing algorithms.
- `raw/research/consumer-data-pooling/01-04-midata-cooperative.md` — MIDATA cooperative primary page.
- `raw/research/consumer-data-pooling/03-06-opentss-how-it-works.md` — OpenTSS project methodology.
- `raw/research/consumer-data-pooling/09-05-drivers-seat-rockefeller.md` — Rockefeller Foundation grantee story on Driver's Seat.
- `raw/research/consumer-data-pooling/04-03-hardjono-pentland-opal.md` — Hardjono & Pentland on the OPAL technical framework.

Additional sources for section 9 (consumer collective bargaining and group purchasing):

- `raw/research/collective-bargaining-group-purchasing/01-01-wikipedia-consumer-coop.md` — Wikipedia Consumers' co-operative; Rochdale history.
- `raw/research/collective-bargaining-group-purchasing/02-02-wikipedia-gpo.md` — Wikipedia GPO primer.
- `raw/research/collective-bargaining-group-purchasing/03-03-wikipedia-group-buying.md` — Wikipedia Group buying; Tuángòu / Pinduoduo / Groupon.
- `raw/research/collective-bargaining-group-purchasing/04-04-wikipedia-park-slope.md` — Wikipedia Park Slope Food Coop.
- `raw/research/collective-bargaining-group-purchasing/05-05-wikipedia-rei.md` — Wikipedia REI.
- `raw/research/collective-bargaining-group-purchasing/06-06-wikipedia-cca.md` — Wikipedia Community Choice Aggregation.
- `raw/research/collective-bargaining-group-purchasing/07-07-hsca-monopsony.md` — Blair & Durrance 2013 (Managerial and Decision Economics), *Group Purchasing Organizations, Monopsony, and Antitrust Policy*.

Additional sources from the 2026-04-23 weekly-brief sweep:

- `raw/research/weekly-2026-04-23/01-live-nation-ticketmaster-verdict-npr.md` — NPR, April 15 2026. State-AG-led jury verdict against Live Nation/Ticketmaster.
- `raw/research/weekly-2026-04-23/02-maryland-hb0895-predatory-pricing-act.md` — Maryland General Assembly, HB0895 status page (Protection From Predatory Pricing Act, effective Oct 1 2026).
- `raw/research/weekly-2026-04-23/03-dc-ag-livenation-99m-settlement.md` — Washington Times AI News Desk, April 21 2026 (DC AG $9.9M consumer-protection settlement against Live Nation).
- `raw/research/weekly-2026-04-23/04-omi-fair-prices-for-local-businesses-act.md` — Open Markets Institute press release, April 2026 (Sen. Murphy's Robinson-Patman revival bill).
- `raw/research/weekly-2026-04-23/05-cma-direct-consumer-enforcement-one-year-on.md` — UK CMA blog, April 17 2026 (Year-1 direct-enforcement regime readout).

Additional sources from the 2026-04-27 weekly-brief sweep:

- `raw/research/weekly-2026-04-27/01-01-themarkup-webxray-california-gpc-audit.md` — The Markup / CalMatters, April 21 2026 (webXray California GPC compliance audit).
- `raw/research/weekly-2026-04-27/03-03-eu-dma-google-search-data-sharing.md` — EU Commission DG COMP / DG CONNECT press release, April 16 2026 (DMA Google search-data FRAND access regime).
- `raw/research/weekly-2026-04-27/04-04-jetblue-surveillance-pricing-class-action.md` — Fortune, April 21 2026 (JetBlue surveillance-pricing inflection event + federal class action + FTC examination).

Additional sources from the 2026-05-04 weekly-brief sweep:

- `raw/research/weekly-2026-05-04/03-04-ny-ag-instacart-investigation.md` — NY Office of the Attorney General press release (announcing Instacart demand letter under the NY Algorithmic Pricing Disclosure Act; references December 2025 Groundwork Collaborative + Consumer Reports field study).
- `raw/research/weekly-2026-05-04/04-05-pluralistic-hb0895-loopholes.md` — Pluralistic / Cory Doctorow, *How not to ban surveillance pricing*, April 30 2026 (synthesises Pat Garofalo / American Economic Liberties Project loophole analysis of HB0895).

Additional sources from the 2026-05-11 weekly-brief sweep:

- `raw/research/weekly-2026-05-11/02-ct-sb4-passage.md` — CT Mirror, May 4 2026 (Connecticut SB4 final House passage 141-6; data-broker registry + centralized DCP deletion mechanism + surveillance-pricing disclosure mandate; bill awaiting Governor Lamont).
- `raw/research/weekly-2026-05-11/06-md-hb0895-cfm-context.md` — Consumer Finance Monitor (Ballard Spahr), May 5 2026 (MD HB0895 framing as "warning shot" for AI-driven pricing across financial services; cross-state legal-landscape context for the surveillance-pricing legislative cluster).

Additional sources for section 9 (transparency tools and observatory infrastructure):

- `raw/research/price-transparency-tools/01-01-hannak-imc2014.md` — Hannak, Soeller, Lazer, Mislove, Wilson 2014 (Northeastern, IMC). Foundational personalisation-detection methodology.
- `raw/research/price-transparency-tools/02-03-keepa-chromewebstore.md` — Keepa Chrome Web Store primary listing.
- `raw/research/price-transparency-tools/07-09-keepa-firefox-addon.md` — Keepa Firefox addons.mozilla.org primary listing.
- `raw/research/price-transparency-tools/04-06-wikipedia-paypal-honey.md` — PayPal Honey Wikipedia chronology (with footnote trail to primary reporting).
- `raw/research/price-transparency-tools/03-05-fakespot-faq.md` — Mozilla shutdown announcement for Pocket and Fakespot (captured as redirect target of fakespot.com/faq).
- `raw/research/price-transparency-tools/05-07-markup-citizen-browser.md` — The Markup project announcement, October 2020.
- `raw/research/price-transparency-tools/06-08-markup-facebook-inspector.md` — The Markup methodology piece, January 2021.

(Origin / audience / purpose / trust metadata for each is summarised on the industry, mechanism, and overview pages where those sources are the primary basis. Here they are cited as contributing evidence to the consolidated counter-power landscape.)

## Related

- [[dynamic-pricing-overview]]
- [[rental-housing-algorithmic-pricing]]
- [[surveillance-pricing-retail]]
- [[consumer-facing-dynamic-pricing]]
- [[algorithmic-collusion]]
- [[platform-cooperatives]]
- [[data-cooperatives]]
- [[collective-bargaining-for-data]]
- [[transparency-tools]]
- [[keepa]]
- [[paypal-honey]]
- [[fakespot]]
- [[markup-citizen-browser]]
- [[open-tenant-screening]]
- [[midata]]
- [[drivers-seat-cooperative]]
- [[consumer-collective-bargaining]]
- [[community-choice-aggregation]]
- [[park-slope-food-coop]]
- [[rei]]
