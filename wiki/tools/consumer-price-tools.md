# Consumer Price Tools — Competitive Landscape

Catalogue of existing consumer-facing tools in the price-surveillance, price-history, and privacy-protection space, assessed against the three hook categories in [[bootstrap-strategy]]: (1) price personalisation/discrimination detection, (3) price history and deal alerts, (5) privacy suites against surveillance pricing. Key findings: Hook 1 is white space; Hook 3 is crowded but structurally compromised by affiliate conflicts; Hook 5 is dominated by commercial products with no cooperative framing.

---

## Hook 1 — Price personalisation / discrimination detection

**Status: Near-empty. Genuine white space at scale.**

No consumer product at scale tells a user "you are being charged more than another user for the same item right now." Existing price-comparison tools (see Hook 3 below) compare across *retailers*, not between profiles at the *same* retailer.

**Northeastern PriceSteering extension (2016, defunct):** The only consumer-facing tool with research rigour. Chrome extension by Volunteer Science (Northeastern multi-university project). Compared user-seen prices vs. a "clean" server-side baseline on Amazon, Google Flights, and Priceline Hotels. Finding: prevalent price *steering* (result reordering by user profile) rather than outright price-discrimination. Never commercialised; no longer maintained.

**BetterPrice (launched May 2026):** Detects markups vs. other retailers (cross-retailer, not within-retailer personalisation detection). Affiliate commission model creates the same structural conflict documented in the Honey scandal below. Not a discrimination detector.

**Regulatory acceleration:** FTC 6(b) orders to 8 surveillance-pricing companies (July 2024); FTC surveillance pricing study confirming location/browsing/demographic use for personalised prices (January 2025); NY Algorithmic Pricing Disclosure Act (July 2025); House Oversight Committee investigation (March 2026). Consumer Reports survey (May 2024): 66% of Americans oppose personalised pricing. See [[surveillance-pricing-retail]] and [[regulatory-responses]].

---

## Hook 3 — Price history tracking

**Status: Crowded but structurally compromised.**

All major products at scale use an affiliate-commission business model — their revenue is maximised by showing partner deals, not best deals. The PayPal Honey scandal made this visible at mass market scale.

**Keepa:** 4M Chrome users; 5.6B+ products tracked; 11 Amazon marketplaces; hourly updates. Freemium: free charts + alerts; €19/month paid tier; API €49–€4,499/month (significant B2B component — Amazon resellers, not just consumers). No documented controversy. Germany-based (Keepa GmbH).

**CamelCamelCamel / The Camelizer:** ~190K Chrome users; website (~11K global rank); affiliate + display ads. Amazon-only. No controversy. Estimated $39M site value. Costs ~$11K/month to operate; entirely free to users.

**PayPal Honey:** Peaked ~20M Chrome users; dropped to ~14M by July 2025 (–30% in 7 months) following December 2024 MegaLag exposé:
- Systematic replacement of creator affiliate cookies with Honey's own (capturing commissions without delivering better deals)
- Merchant partners controlled which coupons were shown (suppressing better publicly-available discounts)
- Class actions filed December 2024 and April 2025
- Root cause: affiliate commission model structurally incentivises showing partner deals ≠ best deals. Honey surfaced this at mass-market scale; the structural conflict applies to all affiliate-model price tools. **Canonical failure mode for the affiliate model.**

**Capital One Shopping (formerly Wikibuy):** 10M+ users. Bank-embedded distribution — not competing on Chrome Web Store but on Capital One's existing financial-product customer base. 4.9/5 App Store (960K+ reviews). Same affiliate model as Honey; no documented scandal to date.

**Fetch Rewards:** 17M MAU; 5B+ receipts submitted; $2.5B valuation. Mobile-first receipt scanning; no pre-selection of offers (any receipt accepted — the differentiator vs. Ibotta). Referrals: 15–20% of signups; referred users 25% more active.

**Ibotta:** 50M registered / 15M active redeemers; IPO April 2024; $320M revenue (2023, +52% YoY). Built Ibotta Performance Network (IPN) — distributes offers via 3rd-party retailer websites, decoupling growth from direct app install. "Teamwork" feature (2014): friend/family teams with shared monthly redemption goal → team bonus — partial complex-contagion design overlay on an otherwise individualist product.

---

## Hook 5 — Privacy suites

**Status: Dominated by commercial products; cooperative framing absent.**

**uBlock Origin:** 29M Chrome MV2 users before Google's July 2025 removal (Chrome 138); Firefox 10M+. GPL3; single maintainer (gorhill); no monetisation. Chrome MV3 version (uBlock Origin Lite) captured ~22% of displaced base (~8M users). The most effective ad/tracker blocker by technical standard. MV3's elimination of dynamic request interception permanently reduces capability for any Chrome extension in this space. **~22M displaced uBlock Origin users have no adequate Chrome replacement** as of 2026. See [[transparency-tools]] and [[browser-fingerprinting]].

**Privacy Badger (EFF):** 1M+ users (Firefox, Chrome, Edge, Brave, Opera). Free; maintained by EFF (nonprofit, member-funded). Heuristic tracker learning; GPC and DNT signals automatic. **Strongest collective/civil-society framing of any privacy tool** — explicitly positioned as consumer advocacy, not a commercial product. Template for cooperative ownership model. See [[privacy-badger]].

**Brave Browser:** 101M MAU (October 2025); 42M DAU; $100M+ annualised revenue. Fingerprint randomisation on by default; integrated ad/tracker blocking (Shields); optional BAT opt-in ad rewards; VPN subscription; AI (Leo). 94% tracker block rate in testing. Commercial company; no cooperative framing. Past controversy: 2020 address-bar affiliate-code insertion (fixed). Diverse revenue reduces dependency on any single model.

**DuckDuckGo:** ~80M users; mobile browser (iOS + Android, 50M+ downloads) + desktop browser + extensions; 98.8M daily searches. GPC signal automatic; Email Protection strips 85%+ email trackers; App Tracking Protection (Android) blocks in-app trackers. Microsoft ad network dependency (primary revenue); 2022 controversy over Microsoft tracker exemptions (subsequently fixed).

**Ghostery:** 2.8M Chrome users (down from 10M+ peak). Historical "Ghostrank" scandal: sold aggregated user browsing data to advertisers while marketing as privacy tool. Trust permanently damaged. Still operates a "Privacy-First Data Marketplace." Removed all user accounts October 2025. **Anti-pattern: claiming privacy while monetising data.**

**Mozilla / Firefox:** Firefox ~200–300M users (declining market share); Mozilla VPN separate subscription. Total Cookie Protection technically strong. Existential structural risk: >90% revenue dependency on Google search deal. Shut down Pocket + Fakespot (July 2025) citing unsustainable costs. **Fakespot acquisition-and-sunset (2023–2025) is the canonical acquisition-and-sunset failure mode** for trust-based consumer tools acquired by larger institutions.

---

## Cross-cutting findings

**The structural conflict of interest:** Every Hook 3 product at scale uses affiliate commissions. The product's revenue is maximised by showing partner deals; the user's interest is maximised by showing best deals. These are not the same. Honey's scale made the conflict visible. Cooperative ownership with no affiliate conflict is the architectural differentiator for a new entrant.

**The MV3 displacement window:** ~22M uBlock Origin Chrome users lost their primary privacy tool in July 2025 with no adequate replacement. This is a live acquisition opportunity for a well-positioned privacy suite. The window is now.

**Acquisition-and-sunset risk:** Fakespot (Mozilla, 2023–2025) and the threatened Honey model both illustrate that consumer trust built on individual-product relationships is fragile to acquisition and sunset. Cooperative or commons-based ownership is the structural counter.

**No collective framing exists:** Every product surveyed is purely individualist — "protect *you*," "save *you* money." The FTC data and Consumer Reports survey demonstrate strong consumer appetite for collective response to surveillance pricing. No product channels it. This is the positioning gap.

---

## Source

- `raw/research/bootstrap-2026-05-27/01-consumer-price-tools-landscape.md` — web research capture, 2026-05-27 (Chrome Web Store, Wikipedia, FTC, company press releases, Sensor Tower). Trust: medium-high.

## Related

- [[transparency-tools]] — mechanism anchor for price transparency tools; Hannak et al. 2014 foundational detection methodology; Keepa and paypal-honey are existing entries
- [[keepa]] — Keepa standalone page
- [[paypal-honey]] — Honey standalone page (canonical extractive-drift failure case)
- [[fakespot]] — Fakespot acquisition-and-sunset failure case
- [[surveillance-pricing-retail]] — FTC 6(b) study findings
- [[browser-fingerprinting]] — technical basis for Hook 1 discrimination detection
- [[privacy-badger]] — Privacy Badger EFF tool (cooperative framing template)
- [[bootstrap-strategy]] — strategy-layer page defining the three hooks and entry-point design
- [[regulatory-responses]] — regulatory acceleration context
