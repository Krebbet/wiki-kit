# Keepa

Keepa is a commercial browser extension that adds **Amazon price history charts and drop alerts** to Amazon product pages. Operated by Keepa GmbH (Kemnath, Germany). The most widely deployed live example of a [[transparency-tools|price-history transparency tool]] — Chrome Web Store listing reports **4,000,000 users** and coverage of over **6 billion Amazon products across 11 locales**.

## Structure

- **Developer:** Keepa GmbH, Berndorfer Str. 10, Kemnath 95478, Germany. D-U-N-S 314533736. Chrome Web Store-declared "trader" per EU definitions.
- **Version/size:** 5.61 (March 20, 2026), 54.82 KiB (Chrome listing at time of capture).
- **Ratings:** 4.7 out of 5 across 5,100+ Chrome Web Store ratings.
- **Coverage:** Amazon .com, .co.uk, .de, .co.jp, .fr, .ca, .it, .es, .in, .mx (Chrome Web Store); Firefox add-on lists the same plus .cn, .com.au, .com.br, .nl.

## How it works (from Chrome Web Store primary source)

- Injects interactive price-history charts directly into Amazon product pages.
- Sets up per-product "price watches" that notify the user when the product drops below a target price or returns to stock. Includes tracking for Lightning Deals.
- Compares prices across Amazon locales for international deal-hunting.
- No account required to use basic features.
- Notification channels: email, web push, RSS, and (per the Firefox listing) Twitter, Facebook Messenger, Telegram.

## Privacy and permissions

Per the Chrome Web Store disclosure:
- Required permissions: `declarativeNetRequestWithHostAccess` and `Cookies` — declared by Keepa as powering "the extraction algorithms that reveal hidden MAPs and third-party merchant stock counts." Storage permission for local caching. ContextMenus optional, disabled by default.
- Developer declares data is: not sold to third parties outside approved use cases; not used/transferred for purposes unrelated to the extension's core functionality; not used for creditworthiness or lending.
- When users click an eBay link in the Keepa Box, the click is routed through the eBay affiliate program.

## Business model

Not explicitly stated in the captured primary source, but visible inference from the source: freemium extension (free) paired with paid APIs and premium features at keepa.com (not captured — the keepa.com homepage timed out on the capture run). Affiliate-commission revenue on eBay redirects is disclosed.

## Counter-power mechanism

Keepa is a single-seller price-history transparency tool. Scope-limited:

- **Mechanism:** informational. Closes the information asymmetry of "is this a sale?" by showing the historical price.
- **Orientation:** individual-level only. No cooperative membership; no negotiation intermediary role. See [[transparency-tools]] for the broader taxonomy.
- **Against what:** Amazon's own pricing variability (including Lightning Deals and third-party marketplace pricing). Does *not* address cross-seller personalisation (see the Hannak et al. 2014 methodology on [[transparency-tools]]) or platform-level algorithmic pricing coordination (see [[rental-housing-algorithmic-pricing|RealPage]] or [[algorithmic-collusion]]).
- **Reach:** 4M Chrome users plus Firefox, Edge. A meaningful consumer base for a single-seller tool.

## Scope and limitations

- **Amazon-only.** Does not address pricing across competitor retailers, cross-site personalisation, or surveillance-pricing inputs (see [[surveillance-pricing-retail]]).
- **No detection of personalisation.** Keepa shows the aggregate/public historical price, not the price shown *to this specific user* compared with others. Hannak et al. 2014 (see [[transparency-tools]]) showed such personalisation exists on travel and retail sites, but Keepa's architecture cannot surface it.
- **Dependence on a single platform (Amazon) and single browser-vendor policy regime.** Chrome Web Store changed affiliate-commission policies in March 2025 in response to the [[paypal-honey|Honey controversy]] — a change that directly affects the legal and technical surface Keepa operates on.
- **Primary-capture limitations.** The keepa.com homepage timed out on Playwright networkidle during capture; structural claims here are sourced from the Chrome Web Store listing and the Firefox Add-ons listing.

## Related extensions (context, not captured)

The Chrome Web Store "Related" section for Keepa surfaced predominantly **Amazon-seller-facing** tools (Seller Assistant, AMZScout FBA Calculator, SellerAmp SAS, IP-Alert, etc.), not consumer-facing transparency tools. Structural observation: the seller-side tooling ecosystem on Amazon is far denser than the buyer-side — Keepa is an outlier consumer tool in a primarily seller-tool market. *(editorial observation from the captured Chrome Web Store Related panel.)*

CamelCamelCamel is a free competitor covering similar ground; its site was captured-attempted in this run but timed out on Playwright networkidle, so it is not a source anchor here.

## Source

- `raw/research/price-transparency-tools/02-03-keepa-chromewebstore.md`
  - **Origin:** Chrome Web Store listing for Keepa, `chromewebstore.google.com`.
  - **Audience:** Chrome users considering installation.
  - **Purpose:** product-description and regulatory-disclosure page (privacy, permissions, developer identity, trader status).
  - **Trust:** primary vendor source mediated by Google's Chrome Web Store verification. User/rating counts current as of 2026-04-22 capture.
- `raw/research/price-transparency-tools/07-09-keepa-firefox-addon.md`
  - **Origin:** Mozilla Firefox addons.mozilla.org listing for Keepa.
  - **Audience:** Firefox users considering installation.
  - **Purpose:** product description, feature list, permissions declaration, version history.
  - **Trust:** primary vendor source mediated by Mozilla verification. 273,281 Firefox users; version 4.19 (March 30, 2024) — note the Firefox add-on version is older than the Chrome (5.61) version, which is worth flagging for users on Firefox.

## Related

- [[transparency-tools]]
- [[paypal-honey]]
- [[fakespot]]
- [[surveillance-pricing-retail]]
- [[consumer-facing-dynamic-pricing]]
