# Transparency Tools

Consumer-facing tools whose core mechanism is **making opaque market behaviour visible** to individuals — price history trackers, review-authenticity analysers, personalisation-detection infrastructure. Transparency tools are the [[regulatory-responses|FTC's implicitly-preferred regulatory lever]] on [[surveillance-pricing-retail|surveillance pricing]] and the most common class of consumer counter-power tech deployed today. They differ from [[data-cooperatives]] (governance-lane) and [[collective-bargaining-for-data]] (bargaining-lane) in that they are informational: they change what a consumer can see, not who controls the data or who negotiates on their behalf.

## Taxonomy

Three functional sub-categories emerge from captured sources:

1. **Seller-side price-history trackers** — archive and display historical price data for a specific product so consumers can judge whether a "sale" is real. Examples: [[keepa]] (Amazon, 4M users), CamelCamelCamel (Amazon, free, older). These operate by scraping a single seller's prices over time.
2. **Review-authenticity analysers** — detect fake / incentivised reviews using ML. Example: [[fakespot]] (acquired by Mozilla 2023, **shut down July 1, 2025**).
3. **Crowdsourced audit / observatory infrastructure** — aggregate multi-user data to detect platform-level algorithmic behaviour (personalisation, steering, amplification). Examples: [[markup-citizen-browser]] (The Markup, 1,000+ panelists, focused on social-media feeds); Hannak et al. 2014 Northeastern IMC paper (300 AMT users + synthetic accounts, focused on e-commerce pricing).

## Foundational academic methodology — Hannak et al. 2014

The canonical detection-methodology paper is Hannak, Soeller, Lazer, Mislove, Wilson (Northeastern), *Measuring Price Discrimination and Steering on E-commerce Web Sites*, IMC 2014 (Vancouver, Nov 2014). Underpins everything else in this wiki on detecting personalised pricing.

### Setup

- **16 top US e-commerce sites**: 10 general retailers and 6 travel sites (hotels + car rental).
- **300 real-world users** via Amazon Mechanical Turk (IRB-approved, protocol #13-04-12) + synthetic "fake accounts" for controlled feature experiments.
- **Methodology core claim:** naive "two users, same query, different results = personalisation" is unreliable because of non-personalisation noise — regional inventory, tax differences, data-centre inconsistencies. The paper's methodology places "great emphasis on controlling for various sources of noise."
- **Open-source release:** all crawling scripts, parsers, and raw data at `personalization.ccs.neu.edu` so other researchers can reproduce and extend. This is load-bearing for the paper's value: it is a transferable methodology, not just a finding.

### Definitions (Hannak et al.)

- **Price discrimination** — showing different prices to different users for the same item.
- **Price steering** — re-ordering search results to place expensive items higher. Different from price discrimination: the item prices are the same but users are nudged toward higher-priced items.

### Findings (Spring 2014)

Evidence of personalisation on **9 of 16 sites**. Specifically:
- **Cheaptickets and Orbitz** — price discrimination via "members-only" hotel pricing.
- **Expedia and Hotels.com** — A/B testing that steers a subset of users toward more expensive hotels. Confirmed by Expedia's Chief Product Officer and Senior Director of Stats Optimization in a phone conversation with the authors.
- **Home Depot and Travelocity** — personalise search results for mobile-device users.
- **Priceline** — personalises search results based on the user's history of clicks and purchases.
- Some sites altered prices by **"hundreds of dollars"**.
- Unexplained personalisation on Newegg and Sears that the feature-based experiments could not attribute — the paper notes geolocation, HTTP Referer, and browsing/purchase history as candidate features for future work.

### Limitations

- **US-only** (IPs, language, users).
- **Search-result-page prices only** — bundle discounts, coupons, sponsored listings, hidden prices left to future work.
- **Can only identify *positive* instances** — the paper notes it cannot claim the absence of personalisation, only that the tested dimensions showed some.

### Why this matters for the wiki's domain

This is the methodological template for every "personalisation detection observatory" that could be built. The [[regulatory-responses|regulatory-responses]] design-input #1 (consumer-side pricing observatory) is effectively a "Hannak at scale, continuously" proposal — a durable version of what Hannak et al. ran as a one-off study. *(editorial / synthesis)*

## Commercial transparency-tool patterns

### Price-history trackers

[[keepa]] is the leading live example: Chrome Web Store listing reports **4,000,000 users** and coverage of **over 6 billion Amazon products across 11 locales**. Business model: freemium — basic price charts and drop alerts free, API and premium stats paid. Structural position: a third-party transparency tool against a single large seller (Amazon), not a cross-seller observatory. Operates under strict Chrome permissions policy and declares data is "not being sold to third parties" on its Chrome Web Store privacy disclosure.

### The extractive-transparency failure mode

[[paypal-honey]] is the canonical case of a "consumer transparency tool" that turned out to extract value from the users it ostensibly helped. Marketed as an auto-coupon finder; acquired by PayPal for **~$4 billion in 2020**. Exposed in late 2024 (YouTuber MegaLag) for (a) **cookie-stuffing**: silently replacing affiliate links at checkout to redirect commission to PayPal regardless of whether a coupon was applied; (b) **coupon-code manipulation**: allowing partnered merchants to hide better codes from shoppers; (c) allegedly scraping private coupon codes and sharing them to users' detriment; (d) incorporating code to evade affiliate-network detection.

- Lost approximately **8 million Chrome Web Store users** by end 2025 from a peak of ~20M.
- Class actions filed December 2024 onwards (Wendover Productions + Ali Spagnola via LegalEagle; GamersNexus via Cotchett, Pitre & McCarthy); initial suit dismissed November 2025 on "no cognizable injury" grounds, amended complaint filed January 2026.
- **Google updated Chrome Web Store policies in March 2025** to prohibit extensions from claiming affiliate commissions without providing discounts — a structural-regulatory response directly attributable to the Honey controversy.
- Rakuten Advertising removed Honey from its network on January 12, 2026.

Full case on [[paypal-honey]]. Relevance: any "buyer-side transparency tool" design (see [[regulatory-responses]] design-input #1) must budget for the extractive-drift risk. Browser-extension business models that rely on affiliate-commission capture have a strong incentive gradient toward extraction.

### The acquisition-and-sunset failure mode

[[fakespot]] was a review-authenticity analyser using ML to flag fake / incentivised Amazon reviews. Founded 2016. Acquired by Mozilla in May 2023 — framed as integration into Firefox's privacy-preserving "Review Checker" feature. **Shut down by Mozilla on July 1, 2025** (Review Checker within Firefox shut down June 10, 2025). Mozilla's stated reason: "While the idea resonated, it didn't fit a model we could sustain."

Relevance: the sustainability challenges documented on [[data-cooperatives]] for cooperative-form tools apply equally to venture/nonprofit transparency tools. Both patterns (extractive drift in PayPal-Honey; sustainability collapse in Fakespot) are generic failure modes to budget for in any consumer-side transparency tool design. *(editorial / synthesis)*

## Observatory / audit infrastructure (journalism)

[[markup-citizen-browser]] (The Markup, launched October 2020) is the closest existing template for a continuous algorithmic observatory. Methodology (from the Markup's *How We Built a Facebook Inspector*, January 2021):

- **1,000+ paid participants** across 48 US states, recruited via a survey research provider.
- Provided demographic data (gender, race, location, age, political leanings, education level).
- **Custom standalone desktop application** (not a browser extension) that connected to panelists' Facebook accounts and periodically captured feed data.
- **Redactor pipeline** auto-strips PII; raw data never seen by humans; auto-deleted after one month.
- **Third-party security audit** by Trail of Bits.
- Originally focused on **Facebook and YouTube**; later extended to Süddeutsche Zeitung for Germany.
- **Partnership with The New York Times** for data analysis and co-reporting.
- **Published methodology + underlying datasets and code** per The Markup's standard practice.
- Known limitations: **95% of approached participants failed to complete registration**; panel skewed older, more educated, and under-represented Hispanic/Latino users and Trump voters.

Citizen Browser focused on social-media algorithms, not pricing, but the methodology is directly transferable to a pricing-focused observatory. This is the operational model behind [[regulatory-responses|design-input #1]]. *(editorial / synthesis)*

## Comparison to existing wiki content

| Mechanism | Orientation | Core action | Anchor page |
|---|---|---|---|
| Transparency tool | Informational | Make opaque market behaviour visible to an individual | this page |
| [[data-cooperatives]] | Governance | Pool data under member ownership | — |
| [[collective-bargaining-for-data]] | Bargaining | Intermediary negotiates on behalf of class | — |
| [[platform-cooperatives]] | Exit | Build parallel institution with different ownership | — |
| [[regulatory-responses]] | Enforcement | State action against the extractor | — |

Transparency tools are the mechanism that requires least coordination — an individual installs and uses, no collective membership, no class representation, no institution-building. This is also their weakness: they do not shift market power, only information asymmetry. *(editorial / synthesis)*

## Open questions (editorial)

- **Scaling up Hannak's methodology.** Hannak et al.'s 2014 study is now over a decade old and the sites tested have likely changed personalisation behaviour substantially. No durable updated replication has been captured in this wiki. A "Hannak at scale, continuously" would directly serve [[regulatory-responses|design-input #1]].
- **Preventing extractive drift.** The Honey case shows that transparency tools funded by affiliate commissions are structurally at risk. Transparency tools funded by cooperative membership (see [[data-cooperatives]]) or by philanthropic grant (Markup, Fakespot-pre-Mozilla, OpenTSS at [[open-tenant-screening]]) each have their own failure modes — cooperative uptake, philanthropic sustainability.
- **Jurisdictional arbitrage.** [[keepa]] is a German GmbH (Keepa GmbH, Kemnath, DE) operating on US Amazon data. Transparency tools tend not to need permissive local regulation the way data coops do, but cross-border data collection is a latent compliance surface.

## Source

- `raw/research/price-transparency-tools/01-01-hannak-imc2014.md`
  - **Origin:** Hannak, Soeller, Lazer, Mislove, Wilson (Northeastern University Computer Science) — *Measuring Price Discrimination and Steering on E-commerce Web Sites*, IMC 2014 proceedings.
  - **Audience:** computer-science and internet-measurement researchers; ancillary audience of regulators and consumer-protection organisations.
  - **Purpose:** develop a methodology for detecting e-commerce personalisation robust to noise, and apply it at meaningful scale.
  - **Trust:** peer-reviewed ACM conference paper; well-cited foundational reference; methodology explicitly open-sourced.
- `raw/research/price-transparency-tools/02-03-keepa-chromewebstore.md`
  - **Origin:** Chrome Web Store listing for Keepa (primary).
  - **Audience:** potential users; vendor verification for Chrome.
  - **Purpose:** product description, user/rating counts, privacy disclosures, developer identity.
  - **Trust:** self-presentation by vendor; Chrome Web Store's developer-identity ("publisher has a good record" badge) and trader flag are mild third-party verification. User/rating counts are current as of 2026-04-22 capture.
- `raw/research/price-transparency-tools/04-06-wikipedia-paypal-honey.md`
  - **Origin:** Wikipedia article on PayPal Honey.
  - **Audience:** general public.
  - **Purpose:** consolidated chronology of the company and its controversies.
  - **Trust:** starting reference; footnote trail to The Verge, USA Today, Washington Post, Bloomberg, court filings (CourtListener), 9to5Google, PayPal's own press releases. Load-bearing claims on this page are sourced via the footnote trail to those primaries.
- `raw/research/price-transparency-tools/03-05-fakespot-faq.md`
  - **Origin:** Mozilla blog (Fakespot FAQ URL redirected to the Mozilla shutdown announcement page).
  - **Audience:** Firefox / Fakespot user community, journalists.
  - **Purpose:** announce the shutdown of Pocket and Fakespot, explain reasoning.
  - **Trust:** primary organisational statement from Mozilla. Authoritative for shutdown-timeline claims.
- `raw/research/price-transparency-tools/05-07-markup-citizen-browser.md` and `06-08-markup-facebook-inspector.md`
  - **Origin:** The Markup — Citizen Browser project page (Oct 2020) and its *How We Built a Facebook Inspector* methodology piece (Jan 2021; Mattu, Yin, Waller, Keegan).
  - **Audience:** journalists, technologists, academics.
  - **Purpose:** announce the project; describe the methodology in detail (for reproducibility and accountability).
  - **Trust:** primary investigative-newsroom source. The Markup publishes underlying datasets and code per its standard practice; the methodology piece was explicitly subject to a third-party security audit by Trail of Bits.

## Related

- [[keepa]]
- [[paypal-honey]]
- [[fakespot]]
- [[markup-citizen-browser]]
- [[data-cooperatives]]
- [[collective-bargaining-for-data]]
- [[open-tenant-screening]]
- [[regulatory-responses]]
- [[surveillance-pricing-retail]]
- [[consumer-facing-dynamic-pricing]]
