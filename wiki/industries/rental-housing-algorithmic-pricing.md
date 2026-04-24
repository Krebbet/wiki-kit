# Rental Housing — Algorithmic Pricing

RealPage, Inc. and the apartment-landlord ecosystem became the most developed U.S. antitrust case against [[dynamic-pricing-overview|algorithmic pricing]] when the DOJ and eight state attorneys general sued the company in August 2024. The litigation, the late-2025 settlement, and parallel suits against major landlords form the clearest recent example of a regulator treating algorithmic pricing as unlawful coordination.

## What RealPage did

RealPage is the dominant provider of revenue-management software for conventional multifamily rental housing — roughly 80% market share per the DOJ complaint. Its software (branded under names including YieldStar) collected nonpublic, competitively sensitive pricing and lease data from participating landlords, pooled it, and returned price recommendations that the DOJ alleged allowed competing landlords to align rents rather than compete on price.

Specific mechanisms named in DOJ filings and ProPublica reporting:
- Real-time rent-adjustment suggestions based on pooled competitor data (e.g., "$50 increase instead of $10 for the day").
- An **Auto Accept** feature that lifted landlord compliance with the algorithm's suggestions.
- Pricing recommendations that coordinated *reductions in concessions* — free rent months, discounts, promotional pricing.
- One landlord cited in the complaint saw a 25% rent increase within 11 months of adopting the software.
- RealPage hosted in-person meetings where property managers discussed pricing strategies derived from nonpublic data.

## The DOJ action and outcome

- **August 2024:** DOJ and eight state AGs filed a civil antitrust complaint against RealPage.
- **January 2025:** the DOJ (under the second Trump administration) continued the prosecution and sued six major landlords directly.
- **Late 2025:** settlement. RealPage agreed to stop using nonpublic competitor data in pricing recommendations, stop conducting market surveys to gather such data, stop training models on active lease data, remove features limiting price decreases or aligning pricing between competing users, cease discussing market analysis based on nonpublic data at its manager meetings, and accept a court-appointed monitor.
- **No financial penalties.** No admission of wrongdoing. RealPage publicly maintained that the software produced "lower rents, less vacancies, and more procompetitive effects" — a claim not tested in court.
- At least ten state AGs joined the litigation. Parallel suits against six major landlords proceeded.
- **Greystar**, the nation's largest landlord, paid $50 million to settle a private class action and $7 million to settle a nine-state action. More than two dozen property-management companies have reached various settlements.

## ProPublica's role

ProPublica's October 2022 investigation ("Rent Barons") first documented how RealPage pooled data across competing landlords and quoted RealPage executives describing the goal as capturing "every possible opportunity to increase price." That reporting:
- Is cited by DOJ prosecutors.
- Prompted dozens of federal tenant lawsuits.
- Triggered Senate hearings (Warren, Sanders) with "alarming" answers from RealPage.
- Led to bills in Congress to ban rent-setting algorithms.
- Led to municipal bans on algorithmic rent software in San Francisco, Philadelphia, and Minneapolis.

## Theoretical framing

The RealPage case sits cleanly in the "explicit coordination via shared pricing tool" category. Academic work (HBS; arXiv) argues that *non-collusive* harm is also possible — a single firm with a faster-updating algorithm can unilaterally charge supracompetitive prices even without sharing data. See [[algorithmic-collusion]]. Whether RealPage's software also produced such asymmetric-frequency effects is not addressed in the DOJ complaint; the complaint's theory is the explicit data-sharing variant.

## Algorithm and data-input detail (Yale TAP 2025)

From the Yale Thurman Arnold Project 2025 Student Paper #07 on RealPage (captured `raw/research/seller-algorithm-taxonomy/04-08-yale-tap-realpage.md`), supplementing the ProPublica / DOJ framing above:

- **Objective function.** *"The pricing algorithm takes into account that other RealPage landlords in the market will also be setting a high price recommended by RP. The result is a similar calculation to the one a joint owner of these units would make."* The algorithm performs **joint-owner profit maximization** across competing landlords — not independent per-landlord optimization.
- **Data inputs (nonpublic bucket):** *"competitively sensitive, real-time transactional data — including occupancy rates, lease terms, and rent rolls — collected from competing landlords through over 50,000 monthly calls surveilling over 11 million total properties."*
- **Data inputs (granular depth):** *"capturing detailed lease terms and individual transactions... gives RealPage's algorithm deep insight into real-time market dynamics and competitor pricing."*
- **Named feature — market seasonality forecasting:** *"AIRM's 'market seasonality' feature exploits this transactional data to generate rent recommendations informed by forecasts of competitors' future supply."*
- **Compliance enforcement mechanism.** *"RealPage earned a 90% approval rate on its price recommendations."* Override requires *"detailed 'specific business commentary' justifying the deviation"* reviewed by a RealPage *"pricing advisor"* who *"actively pressure[s] property managers to accept AIRM's price recommendations."* This is how the algorithm maintains its effective control over landlord pricing despite nominally being recommendations.
- **Public-data-only variant (LRO):** *"requires landlords to manually input information sourced from publicly available listings."* Same algorithmic architecture, different data corpus.

### The TAP paper's remedial argument

The authors explicitly reject the "data moat" framing of the RealPage harm:

> "The anticompetitive core of the scheme is not tethered to the nature of the data but to the centralization of pricing power. The essential economic harm arises from the fact that competing firms are outsourcing a critical competitive function — price-setting — to a common intermediary whose purpose is to maximize profits collectively rather than independently."

And on the relative importance of data quality:

> "Granular information may improve the algorithm's accuracy in setting sustainable collusive prices towards monopoly levels, but it is not essential to the structure of coordination."

Their proposed remedy is therefore structural, not data-based: *"RealPage should be barred from making specific, tailored price recommendations to more than one competitor."* The reasoning is that data-stripping alone — the direction of the DOJ's Cortland remedy — would not break the system, because LRO (the public-data-only variant) retains the same collusive architecture. See [[pricing-algorithm-taxonomy|Family 5]] for the cross-family taxonomy placement.

## Design-input candidates *(editorial — not source content)*

Ideas for tenant-side tools, surfaced during research:

- **Rent-pattern detector.** Scrape listing data for a metro and flag listings whose price history matches RealPage-style algorithmic adjustment patterns — frequent small synchronised increases, uniform withdrawal of concessions, tight clustering across competing properties.
- **Class-action signal aggregator.** Connect tenants in metros with high RealPage penetration to active class-action counsel. Mirror the structure of existing mass-action plaintiff-aggregation platforms.
- **Tenant data co-op.** The direct counterweight to landlord data-pooling is *tenant* data-pooling — anonymised offer / counter-offer / ask data across tenants in a building or metro, surfacing when landlord asks are out of distribution. **[[open-tenant-screening]]** (MIT / Mozilla-funded research project) is the closest existing instance on the tenant-screening side of the same industry; it crowdsources tenant-screening reports to audit vendors. A pricing-side analogue with a [[data-cooperatives|data-cooperative]] governance shell (and optionally a [[collective-bargaining-for-data|CBI-style bargaining mandate]]) would complete the structural mirror of RealPage.
- **Model-training prohibition monitor.** Under the settlement, RealPage must stop using active lease data for model training. A third-party audit tool or complaint hotline for tenants who suspect non-compliance would plausibly have traction given the court-appointed monitor's mandate.

## Source

- `raw/research/dynamic-pricing-landscape/01-doj-realpage-lawsuit.md`
  - **Origin:** U.S. Department of Justice press release, August 2024.
  - **Audience:** press, public, legal practitioners.
  - **Purpose:** announce and frame the civil antitrust action.
  - **Trust:** primary regulatory document; stated as the government's allegations, not adjudicated facts at the time of publication.
- `raw/research/dynamic-pricing-landscape/02-propublica-realpage-settlement.md`
  - **Origin:** ProPublica, late 2025.
  - **Audience:** general public, policy followers.
  - **Purpose:** report on the DOJ settlement and summarise the full case arc.
  - **Trust:** high — ProPublica broke the original 2022 story; reporting has been durable across three years of follow-on litigation.

## Related

- [[dynamic-pricing-overview]]
- [[algorithmic-collusion]]
- [[regulatory-responses]]
- [[open-tenant-screening]]
- [[data-cooperatives]]
- [[collective-bargaining-for-data]]
