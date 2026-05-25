# Agri Stats Consent Decree (2026)

The DOJ and six state AGs (MN, CA, NC, TN, TX, UT) filed a proposed consent decree against Agri Stats, Inc. — a third-party meat-industry benchmarking intermediary — restructuring it from a seller-only, granular price/output/cost information hub into an open-access, anonymised, time-delayed benchmarking utility under a 7-to-10-year court monitor. The structural parallel to the RealPage case is close: both are hub-and-spoke data aggregators whose access asymmetry enabled coordinated seller behaviour without explicit cartel communication. The Agri Stats remedy architecture (anonymisation floor + mandatory open access + data-aging + compliance monitor) constitutes a replicable template for algorithmic information-sharing antitrust enforcement across industries.

## The scheme

Agri Stats collected granular price, output, cost, and production data directly from the accounting systems of the major U.S. meat processors (broiler chicken, pork, turkey), standardised it into proprietary "Books," "Runs," and "Flags" reports, and redistributed those reports exclusively back to the same subscribing processors — categorically excluding all buyers (restaurants, grocery chains, food distributors). The asymmetry was total: the processors who set prices also held the information infrastructure; no downstream buyer had access to equivalent signals.

The mechanism is structurally parallel to [[rental-housing-algorithmic-pricing|RealPage]] in multifamily housing: a hub-and-spoke aggregator whose seller-only access model enables parallel pricing decisions without requiring direct firm-to-firm cartel communication. The key distinction from RealPage is that Agri Stats' coordination mechanism was explicit proprietary data-sharing (standardised benchmarking reports) rather than ML-driven price recommendations; the anticompetitive output (coordinated supply restriction and price elevation) was produced without algorithmic inference. A Smithfield executive quote cited in the American Prospect — *"Just raise your price"* — is the primary-source anchor for how the data was operationalised.

The DOJ filed the case at D. Minn. (No. 0:23-CV-03009) under Sherman Act Section 1.

## Remedy architecture (5 components)

The proposed final judgment (primary source: justice.gov/atr/media/1439906) enumerates five structural conduct remedy components:

1. **Sales-data prohibition (§IV.A).** Agri Stats is barred from disseminating any report or information derived from a participant's sales data.

2. **Prohibited-conduct list (§IV.B.1–4).** Agri Stats may not share: participant identity at the facility level; processor rankings by price, cost, or output metric; "flag" designations that tag individual processor performance; or any other non-aggregated individual participant information.

3. **Anonymisation and aggregation floor (§VI.D.1–2).** Any continuing benchmarking report must draw on data from **≥3 contributors**, with no single contributor accounting for **>70%** of any reported metric. Quartile-level reporting requires **≥3 complexes per quartile**.

4. **Data-aging / recency restriction (§VI.E).** Reports must carry an **average data lag of ≥45 days**. Forward production decisions must not appear in reports until **≥90 days** before the relevant production period. Monthly data is embargoed until the **first day of the second following month**.

5. **Open/non-discriminatory access (§VI.C).** Any U.S. person — including buyers, academic researchers, and journalists — may purchase Agri Stats' reports at a price **≤ the average per-Book/Run price paid by single-plant processors**. Non-processor purchasers face no data-contribution requirement (§VI.C.5). The EMI carve-out (less granular, pre-existing public-facing price reports) is explicitly treated as compliant — it defines the dividing line between lawful and unlawful information sharing.

**Compliance monitor (§§VII–VIII).** A 7-year court-appointed monitor (defendant-funded, U.S.-selected), with annual reporting obligations, antitrust compliance program requirements including whistleblower protections, and an early-termination review at year 3. The full decree term is 10 years; early termination of the consent decree itself is eligible at year 7 on U.S. motion.

## Comparison to the RealPage remedy

Both decrees target hub-and-spoke data intermediaries that aggregated seller data and enabled parallel pricing without direct firm communication. The remedy architectures differ on two dimensions:

| Dimension | Agri Stats (2026) | RealPage (settled 2025) |
|---|---|---|
| **Information flow** | Seller-only exclusion of buyers → open/non-discriminatory access mandate | Algorithm recommendation ban + no-coordination injunction |
| **Data timing** | Mandatory ≥45-day average lag; ≥90d for forward production | Data-aging restrictions (geographic scope-limited) |
| **Access regime** | Any U.S. person at price ≤ processor average — structural open-access requirement | No equivalent open-access mandate on housing market data |
| **Aggregation floor** | ≥3 contributors, ≤70% concentration per metric (specific thresholds in decree text) | No comparable explicit aggregation floor reported |
| **Monitor term** | 7-year monitor; 10-year full decree | Court-appointed monitor; terms not captured in full on this wiki |

The Agri Stats remedy is more granular on aggregation thresholds and introduces a novel open-access mandate that the RealPage decree lacks. The DOJ's implicit safe-harbour logic: a data exchange is compliant when it is (a) sufficiently aggregated and anonymised, (b) temporally lagged, and (c) accessible to all market participants on non-discriminatory terms. This three-part test is the transferable template.

## Criticism / remedy-efficacy critique

*The following subsection documents the American Prospect / Lee Hepner critique of the decree's design. The criticism is clearly attributed advocacy commentary; the wiki documents it as a counterweight to the DOJ's self-promotional framing, not as the wiki's own editorial position.*

David Dayen (American Prospect, 2026-05-08) and Lee Hepner (American Economic Liberties Project) argue the open-access mandate is structurally perverse:

**"Laundering the cartel."** The mandate that buyers may now purchase Agri Stats reports at processor-equivalent pricing expands Agri Stats' paying customer base and revenue without dismantling the coordination infrastructure. Dayen / Hepner characterise this as converting a cartel-information monopoly into a broader subscription service — *"laundering the cartel."*

**Ranking reports and consulting relationships left intact.** The processor-ranking reports — which processors used to determine when to restrict supply or elevate prices — remain fully operational under the settlement. Verbal prohibitions on price advice in consulting relationships are asserted but unenforceable in the absence of structural separation. The decree reaches what is reported; it does not reach how the benchmarking relationships are exploited in practice.

**ATPCO 1992 parallel.** The Airline Tariff Publishing Company (ATPCO) was the subject of a 1992 DOJ airline price-fixing settlement structured on similar logic: the remedy required access-expansion without dissolving the intermediary's core coordination role. Dayen identifies this as the same failure mode, suggesting the Agri Stats remedy is not novel but follows a documented pattern of regulatory capture of the remedy itself.

**Tunney Act avenue.** The Tunney Act (15 U.S.C. §16(e)) requires a 60-day public-comment period after Federal Register publication before a consent decree is entered. The American Prospect flags this as a live procedural channel for state AGs or third-party challengers to contest the decree's adequacy — a mechanism that has historically been under-used in information-sharing cartel cases.

## Source

- `raw/research/weekly-2026-05-18/02-02-agristats-doj-pr.md`
  - **URL:** DOJ OPA press release (justice.gov antitrust division).
  - **Origin:** U.S. Department of Justice Antitrust Division, co-signed by AGs of CA, MN, NC, TN, TX, UT.
  - **Audience:** general public; Tunney Act comment participants.
  - **Purpose:** announce the proposed consent decree; state the legal theory.
  - **Trust:** primary-source government enforcement document — high credibility as statement of DOJ theory; self-promotional framing on consumer benefit claims. Note: the captured raw file was truncated at the remedy-bullet list; remedy detail in this page is drawn primarily from summary 09 (the final judgment text itself).

- `raw/research/weekly-2026-05-18/09-09-agristats-proposed-final-judgment.md`
  - **URL:** justice.gov/atr/media/1439906 (proposed final judgment, D. Minn. No. 0:23-CV-03009).
  - **Origin:** DOJ Antitrust Division + AGs of MN, CA, NC, TN, TX, UT; court filing.
  - **Audience:** the court and future enforcement parties.
  - **Purpose:** convert a Section 1 Sherman Act information-sharing scheme into a structurally non-coordinative benchmarking service.
  - **Trust:** authoritative primary legal instrument; highest-trust source for the remedy architecture enumerated above.

- `raw/research/weekly-2026-05-18/03-02b-agristats-prospect-critique.md`
  - **URL:** americanprospect.org / prospect.org/2026/05/08/... ("Meat Industry Price Fixer Sentenced to Make Money").
  - **Origin:** David Dayen, The American Prospect, published 2026-05-08.
  - **Audience:** policy-engaged general readers; antitrust advocates.
  - **Purpose:** critique the remedy design; flag Tunney Act procedural avenues.
  - **Trust:** advocacy journalism with strong antitrust beat; cites Lee Hepner (AELP) by name; no industry funding declared; framing is explicitly adversarial to the settlement. High credibility as watchdog commentary; not a neutral legal analysis.

## Related

- [[regulatory-responses]]
- [[consumer-facing-dynamic-pricing]]
- [[algorithmic-collusion]]
- [[buyer-cartels-antitrust]]
- [[data-market-mechanism-design]]
- [[consumer-collective-bargaining]]
- [[information-sharing-remedy-efficacy]]
