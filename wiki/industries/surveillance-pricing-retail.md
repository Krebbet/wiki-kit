# Surveillance Pricing — Retail and Beyond

In July 2024 the FTC invoked its Section 6(b) authority to order eight companies to produce information on the [[dynamic-pricing-overview|surveillance-pricing]] ecosystem. Interim findings (January 2025) describe a mature intermediary industry selling price-targeting, consumer-segmentation, and product-ranking tools that feed on behavioural data, location data, loyalty-program data, and inferences drawn from both. This page covers what the FTC found and the industries implicated.

## Scope of the FTC 6(b) study

**Respondents ordered to produce documents:** Mastercard, Revionics, Bloomreach, PROS, JPMorgan Chase, Task Software, Accenture, McKinsey & Company.

**Aggregate reach:** the eight intermediaries collectively serve 250+ retail and business clients (exact count redacted).

**Scope of data collection:** interim findings are based on documents produced July–December 2024. The FTC has flagged the findings as pre-publication and explicitly solicits feedback while continuing the study.

## Industries implicated (as named in FTC documents)

| Sector | Examples cited |
|---|---|
| Grocery retailers | Large regional chains; Stop & Shop cited for digital-only deals. |
| Apparel / fashion | Generic large chains. |
| Health & beauty retail | Cosmetics chain using consumer skin-tone data. |
| Home goods & furnishings | — |
| Convenience stores | — |
| Building / hardware | Home Depot, Lowe's context. |
| General merchandise / discount | Walmart, Target (first-party data leverage). |
| Financial services | Credit card issuers, car rental. |
| Travel | Expedia-style booking platforms. |
| Sports betting & online casinos | — |
| E-commerce marketplaces | Lease-to-own platforms. |
| Pharmacy / medical supplies | CVS, Walgreens context. |
| Telecommunications | T-Mobile context (ad targeting). |
| B2B wholesale | Groceries, pharmacy, medical supplies, food/beverage, electronics, construction materials. |

## Three tool categories

The FTC staff group surveillance-pricing intermediary products into three overlapping categories:

**1. Price targeting.** Algorithms generate per-customer or per-segment prices using location, purchase history, browsing behaviour, demographic data, and inferred willingness-to-pay. Update frequency ranges from monthly to minute-by-minute; in B2B contexts, quotes are generated in milliseconds.

**2. Consumer segmentation and profiling.** Unique consumer profiles are assembled from disparate data sources — email, browsing, purchase, location, loyalty-program enrolment, third-party brokers. Segments are built on dimensions including purchase history, demographics, inferred "loyalty," "price sensitivity," "impulse propensity," and family or life-stage status.

**3. Search and product ranking.** The ordering or prominence of products on a retailer's website or app is altered based on the shopper's segment. A customer inferred to be a new parent may see higher-priced baby thermometers surfaced; a price-sensitive segment may see different products entirely.

## Specific examples drawn from the FTC documents

- **New-parent targeting.** A retailer profiled a shopper as a new parent based on zip code plus a fast-delivery shipping inference, then surfaced higher-priced baby thermometers in search results.
- **Stress-response targeting.** A health-supplies company targeted stress-relief supplements to consumers located in recently-flooded areas.
- **Loyalty-penalty pricing.** A pharmacy chain excluded its most-loyal customers from discounts and instead targeted promotions at infrequent buyers at risk of disengaging.
- **Location-based price variation.** An office-supply retailer used competitor-price data to set store-specific prices and tailored its website prices to the visitor's detected location.
- **Dealership profiling.** A car dealership used in-store kiosk interactions to segment walk-in customers as "less savvy" first-time buyers, targeting them with specific financing rates and trade-in discounts.
- **Cosmetics by skin tone.** A cosmetics retailer used consumer skin-tone data to target ads and promotions.

## Revenue and margin impact

Per intermediaries' own marketing materials as quoted in the FTC documents:
- **Sales volume increases:** 2–5% attributed to the use of surveillance-pricing tools.
- **Margin increases:** 1–4%.

These figures are seller-reported; the FTC flags them as marketing claims rather than independently verified effects.

## Data sources in use

Cookies, mobile SDKs, geolocation, loyalty-program enrolments, third-party data brokers, web scraping of competitor prices, customer-support platform logs, review-platform activity, call-tracking systems, reservation-system data. Inferences drawn from mouse movements, page dwell time, email open timing, and video-consumption patterns.

## Counter-power thread

The FTC study is itself a counter-power mechanism — the first sustained government examination of the surveillance-pricing intermediary market. It is explicitly framed as interim and pre-publication to accelerate transparency and enable public research collaboration under Section 6(f). See [[regulatory-responses]] for the broader regulatory landscape and parallel actions (DOJ RealPage; state laws; EU frameworks).

## Design-input candidates *(editorial — not source content)*

- **Shopper-side price auditor.** A browser extension or mobile app that captures prices seen by the user, compares them against anonymised prices captured by other users, and flags material divergence suggestive of personalisation. Conceptually similar to existing price-history trackers (e.g., Keepa for Amazon) but cross-retailer and explicitly anti-personalisation.
- **Loyalty-program disclosure tool.** Given the FTC finding that loyal customers are sometimes *excluded* from discounts, a tool that lets users submit their loyalty-program purchase history and receive a comparative fairness score versus a synthetic non-loyalty baseline.
- **"Segmentation shadow."** A consumer-facing tool that runs deliberately distorted browser/device fingerprints against retailer sites to surface when search rankings or prices change — effectively a Turing test for personalisation.
- **FTC-study commenting aggregator.** The FTC explicitly solicits public feedback on its interim findings. A civic tool that collects and submits structured consumer testimony into the regulatory record would amplify individual evidence.

## Source

- `raw/research/dynamic-pricing-landscape/04-ftc-issue-spotlight.md`
  - **Origin:** Federal Trade Commission, Office of Technology, "Issue Spotlight: The Rise of Surveillance Pricing" (January 2025).
  - **Audience:** policymakers, researchers, industry, press.
  - **Purpose:** publicise interim findings from the 6(b) study and invite further scrutiny.
  - **Trust:** primary regulatory document; framed as interim and subject to revision.
- `raw/research/dynamic-pricing-landscape/05-ftc-research-summaries.md`
  - **Origin:** FTC staff, "Surveillance Pricing 6(b) Study: Research Summaries" (redacted, January 2025).
  - **Audience:** researchers, policymakers.
  - **Purpose:** document-level staff analysis of 6(b) respondent submissions.
  - **Trust:** primary regulatory document; redactions limit traceability to specific respondent claims.

## Related

- [[dynamic-pricing-overview]]
- [[consumer-facing-dynamic-pricing]]
- [[algorithmic-collusion]]
- [[regulatory-responses]]
