# Fakespot

Fakespot was a **review-authenticity analyser** — an ML-based tool that scored Amazon (and other retailer) product review trustworthiness to flag fake and incentivised reviews. Founded 2016. Acquired by Mozilla in May 2023. **Shut down by Mozilla on July 1, 2025.** Together with [[paypal-honey]], the canonical *acquisition-and-sunset* failure mode for consumer [[transparency-tools]].

## How it worked (per earlier primary material via WebSearch preamble; page capture is the Mozilla shutdown announcement)

- Used machine learning to detect patterns common to fake / incentivised reviews: copy-pasted text, regional clustering of reviewer IPs, short reviews, spelling and grammar anomalies.
- Produced a **review grade** (A, B = reliable; C = mixed; D, F = insufficient reliable reviews).
- Worked as a browser extension, a web tool, and later (post-Mozilla acquisition) as a native **Review Checker** inside Firefox.
- Mozilla launched *Fakespot Chat* in November 2023 — the company's first LLM-based product — to answer shopping questions. Shut down in the same 2025 wrap-up.

(Capture note: the fakespot.com/faq URL captured in this run redirected to Mozilla's shutdown announcement blog post, so the primary-source page details above derive from WebSearch preamble rather than direct capture. Treat the "how it worked" bullets as lower-trust for this page.)

## The shutdown

Per Mozilla's announcement (captured as the redirect target of the Fakespot FAQ URL):

> We acquired Fakespot in 2023 to help people navigate unreliable product reviews using AI and privacy-first tech. While the idea resonated, it didn't fit a model we could sustain.

Timeline:
- **June 10, 2025** — Review Checker feature inside Firefox shut down.
- **July 1, 2025** — Fakespot extensions, mobile apps, and website shut down.

Announced alongside the shutdown of **Pocket** (Mozilla's read-it-later app), framed as a focus-refocus: "we've made the difficult decision to phase out two products ... channeling our resources into projects that better match browsing habits today."

## Counter-power mechanism — and the sustainability failure mode

Fakespot was a review-side transparency tool rather than a price-side one. Its counter-power claim was informational: a consumer could judge whether to trust a product's reviews before purchase. The tool addressed a specific extraction mechanism documented on [[surveillance-pricing-retail]]: the use of manipulated reviews and product-ranking algorithms to steer consumer behaviour.

The **sustainability failure mode** is structurally distinct from the [[paypal-honey|Honey extractive-drift case]]:

- Honey's business model was funded by affiliate-commission capture — an incentive toward extraction.
- Fakespot's business model (pre-Mozilla) relied on premium/API revenue and ad-free subscriptions; post-Mozilla it was grant-funded from the parent Firefox organisation.
- Mozilla's stated reason for shutdown — "didn't fit a model we could sustain" — is the identical phrase in substance to what the [[data-cooperatives|Ada Lovelace 2021 report on data cooperatives]] flagged as the generic financial-sustainability challenge: transparency tools funded outside commercial extraction must either build durable membership-based revenue, durable philanthropic support, or accept shutdown.

Relevance for this wiki's design-input work: a "personalised-pricing observatory" (see [[regulatory-responses|design-input #1]]) funded on Fakespot's model is exposed to the same shutdown risk. Cooperative funding ([[data-cooperatives]]) or institutionally-hosted funding ([[open-tenant-screening|OpenTSS]]'s Mozilla-Tech-Fund + MIT model) are the two alternatives captured elsewhere in the wiki; both have different failure modes to budget for. *(editorial / synthesis)*

## Scope and limitations

- **Primary-source capture is thin.** The fakespot.com/faq URL redirected to the Mozilla shutdown announcement; no current "how it works" primary content is captured. WebSearch preamble provided the ML-methodology description, which is treated as lower-trust context here.
- **Methodology opacity.** Per search-result preamble, Fakespot did not reveal its detection methodology — stated reason was to prevent gaming. This is structurally similar to the tenant-screening-service scoring opacity documented on [[open-tenant-screening]]: transparency tools whose own methodology is opaque reproduce the asymmetry they claim to correct, for a different audience. *(editorial observation — not from the captured shutdown announcement.)*
- **Post-shutdown status.** As of 2026-04-22, the tool is no longer operational. Any future consumer wanting review-authenticity analysis must look elsewhere.

## Source

- `raw/research/price-transparency-tools/03-05-fakespot-faq.md`
  - **Origin:** Mozilla blog — *Investing in what moves the internet forward* (shutdown announcement for Pocket and Fakespot, published May 2025). Captured as the redirect target of `fakespot.com/faq`.
  - **Audience:** Firefox / Fakespot user community, press, Mozilla stakeholders.
  - **Purpose:** announce the shutdown, explain the reasoning, communicate product-wind-down dates.
  - **Trust:** primary organisational statement from Mozilla. Authoritative for shutdown-timeline claims and Mozilla's stated rationale. Not a source for pre-shutdown Fakespot methodology or metrics.

## Related

- [[transparency-tools]]
- [[paypal-honey]]
- [[keepa]]
- [[surveillance-pricing-retail]]
- [[data-cooperatives]]
