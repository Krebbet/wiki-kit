# Regulatory and Other Counter-Power Responses to Algorithmic Pricing

Consolidated survey of pushback mechanisms against dynamic, personalised, surveillance, and algorithmic pricing — regulatory enforcement, legislation, sub-national action, journalism, litigation, and consumer backlash — as documented in the wiki's 8 captured sources. This is the operating-room page for answering *where the existing counter-power is*, *where it is nascent*, and *where the gaps are*.

## 1. Federal regulatory enforcement (US)

### DOJ — algorithmic price-fixing (RealPage)
The most developed federal enforcement action. DOJ + 8 state AGs sued RealPage August 2024; settled late 2025 with structural remedies (data-sharing ban, no-coordination injunctions, court-appointed monitor) but no financial penalty and no admission of wrongdoing. At least 10 state AGs joined. The second Trump DOJ continued prosecution and directly sued six major landlords. Full account at [[rental-housing-algorithmic-pricing]]. *(DOJ press release; ProPublica.)*

**Mechanism:** Sherman Act Section 1 — explicit horizontal coordination via a shared algorithmic intermediary.

**Reach:** works for the explicit-coordination variant. Does not reach tacit algorithmic collusion or asymmetric-frequency harm — see [[algorithmic-collusion]].

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

### New York Bill A3008
Enacted. Requires clear and conspicuous disclosure when a consumer is being offered a "personalised algorithmic price." First US state-level **disclosure** regime for personalised pricing. *(TechTarget via WebSearch / personalised-pricing research thread.)*

### Maryland HB0895 — Protection From Predatory Pricing Act (2026)
Enacted April 2026; effective **October 1, 2026**. Cross-filed as SB0387; By Request of the Governor (Moore administration). 50+ House sponsors. **Substantive prohibition** (not disclosure):

- Bars **food retailers (>15,000 sq ft)** and **third-party delivery service providers** from engaging in dynamic pricing or using consumer personal data to set prices on consumer goods/services
- Bars use of **protected-class data** to offer, advertise, or sell consumer goods/services under certain circumstances
- Violations are unfair / abusive / deceptive trade practices, subject to enforcement and penalties

**First-in-nation US state-level prohibition** of personalised pricing in a major retail vertical. Categorically distinct from NY A3008's disclosure regime — NY says "tell the consumer this is personalised," Maryland says "you may not personalise at all in this sector." Sectoral scope (food retail + delivery platforms) is narrower than universal but targets exactly the verticals the FTC 6(b) study (see [[surveillance-pricing-retail]]) identified as most active in surveillance pricing. Colorado HB26-1210 (advanced out of Senate committee April 21 2026; floor vote scheduled April 24) extends a similar prohibition framework with the addition of wage-setting; suggests a state-legislative cluster forming. *(Maryland General Assembly HB0895 status page; Maryland Fiscal and Policy Note.)*

**Mechanism:** State-statutory prohibition with consumer-protection enforcement hook. Conceptually closest to a sectoral CCPA-style data-use restriction rather than to antitrust. The prohibition-not-disclosure stance is the load-bearing innovation — it removes the "the consumer was informed and consented" defence that disclosure regimes implicitly leave open.

**Reach:** Maryland-only (jurisdictional). The Colorado advance and the cross-filed SB0387 suggest replicability; food-retail-and-delivery scoping could be lifted by other state legislatures with minimal modification.

### Municipal bans
San Francisco, Philadelphia, and Minneapolis have moved to bar landlord use of algorithmic rent-setting software. *(ProPublica.)*

## 4. International

### EU
- **Digital Markets Act (DMA) and Digital Services Act (DSA)** — operational; framework for platform regulation. Not yet addressing algorithmic pricing collusion specifically per arXiv's survey.
- **European Commission** — investigating Ticketmaster's dynamic pricing (parallel to UK CMA). *(Wikipedia.)*

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
- State disclosure regimes (NY A3008 is the first-mover disclosure regime; Maryland HB0895 — see § 3 above — is a *categorically different* first-mover prohibition regime in food retail / delivery; Colorado HB26-1210 advancing similar prohibition with wage-setting addition. Cluster forming, but still under-replicated nationally).
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
