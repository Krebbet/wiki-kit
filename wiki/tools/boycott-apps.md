# Boycott Apps (Buycott + Goods Unite Us)

Two live consumer-facing mobile applications that implement [[possible-strategic-levers|lever #13 (buy-cott coordinator)]] — directing individual purchases toward or away from specific brands based on parent-company behaviour or political alignment. **Buycott** uses barcode-scanning + parent-company lookup + campaign matching; **Goods Unite Us** uses FEC political-donation data to score brands on political alignment. Both are working-at-scale implementations of the collective-redirection mechanism (category B on the strategic-levers inventory).

## Buycott

### Structure

- Web platform + mobile app (iOS + Android).
- **Free UPC lookup database with over 600 million barcodes** (per buycott.com primary-page tagline captured via WebSearch preamble).
- Campaign-driven: users join existing campaigns or create their own.

### Mechanism (per captured Wikipedia source + WebSearch preamble)

- User scans a product's UPC barcode in-store.
- App discerns the product's brand and parent company.
- Cross-checks against campaigns the user has joined (e.g., "Boycott companies that sell FUR", "Support Veterans", "GMO labeling").
- If the product's parent company conflicts with the user's campaigns, the app flags it and suggests alternative products.
- Also displays the full **family tree of products made by the same parent company**, enabling umbrella-boycott behaviour.

### Campaign structure

Per the WebSearch preamble: campaigns are often initiated by nonprofit organisations and cover issues such as "opposing child labor in the chocolate industry, advocating for GMO labeling, and addressing environmental concerns." User-created campaigns are also supported.

## Goods Unite Us

### Structure (per captured primary source)

- Web platform + mobile app (iOS + Android).
- Non-partisan per its stated positioning.
- **Scale (per primary site as of 2026-04-22):**
  - **7,000+ companies** indexed
  - **800+ politicians** indexed
  - **2 million+ users**
  - **16 issues** tracked
- Free core app with "Premium inside the app for $3.99 per month."

### Mechanism

- Data source: publicly available **Federal Election Commission (FEC) records** (fec.gov).
- Covers political donations by companies and by their senior employees.
- Scoring / filtering: users can (per the primary page's feature copy) "explore the political affiliation of thousands of companies," see which politicians a brand's money funds, and discover "handpicked alternative brands that better align with your values."

### Stated mission (per captured primary source)

> The average consumer indirectly contributes **3× more** to political campaigns through everyday purchases than through direct donations.
>
> And some of those profits get donated to politicians and causes you might not agree with.

## Comparison

| | Buycott | Goods Unite Us |
|---|---|---|
| Scanning method | UPC barcode (in-store scan) | Brand name lookup / search |
| Data dimension | Campaign-match (user-selected issues) | Political-donation alignment (FEC) |
| Reach | 600M+ barcode database | 7,000+ companies, 2M+ users |
| Campaign creation | Yes — users can create campaigns | Not captured; brand-level only |
| Business model | Free; not-for-profit framing | Freemium ($3.99/mo premium) |

## Counter-power mechanism

Both are **collective redirection** at the individual-transaction layer — directly implementing the [[consumer-collective-bargaining|consumer-backlash / boycott tradition]] and extending it with:

1. **Information-asymmetry correction.** The individual consumer rarely knows the full parent-company tree or the political-donation history of a brand at point-of-purchase. Both tools surface this data at the moment of decision.
2. **Pre-coordinated campaigns.** Rather than requiring each consumer to know about each boycott, campaigns are surfaced inline — the coordination infrastructure is folded into the tool.
3. **Alternative-suggestion routing.** Both suggest alternatives when a product fails the user's criteria — the "buy-cott" half of the mechanism (positive redirection), not just the boycott half (avoidance).

**Structural limits:**
- Neither app corrects **pricing** — both operate on binary "align with values?" decisions, not on pricing differentials. They are boycott tools, not pricing-counter tools.
- Neither app is integrated with a purchase channel. The consumer still completes the transaction through the regular seller. No fulfilment disintermediation (unlike [[open-food-network|Open Food Network]] on the supply side).

## Relevance for dynamic-pricing strategy

*(editorial / synthesis — neither captured tool targets pricing per se.)*

Both tools demonstrate the **standing-infrastructure for flash-redirection** design pattern that [[possible-strategic-levers|strategic lever #12 (flash-redirection observatory)]] would need. Transferable lessons:

1. **The data-lookup layer must be pre-built and comprehensive.** Buycott's 600M-barcode database + Goods Unite Us's FEC-data ingestion are the reason either tool is usable at point-of-sale. A pricing-redirection tool needs an equivalent standing data layer (Hannak-2014-methodology-at-scale per [[transparency-tools]]).
2. **Criteria are user-selected.** Buycott users join campaigns; Goods Unite Us users pick issues. A pricing-redirection tool should probably default to "this retailer is overcharging" but allow users to tune thresholds per category.
3. **Alternative routing closes the loop.** Avoidance alone is insufficient; consumers need a viable alternative to route *to*. This is also the [[open-food-network]] insight on the supply side.

## Scope and limitations

- **Primary-source capture thinness:** captured sources are a Wikipedia summary for Buycott (5KB) and the Goods Unite Us homepage (2.3KB, borderline thin). Load-bearing scale figures (600M barcodes for Buycott; 7,000 companies / 2M users for Goods Unite Us) come from the primary sources themselves — self-reported and not independently audited.
- **Political-donation data quality:** Goods Unite Us relies on FEC records for *direct* political contributions. Corporate political influence via PACs, 501(c)(4) spending, and lobbying is not fully captured by FEC filings. The tool's underlying data may therefore understate the full political footprint of a given brand. *(editorial observation — not from captured source.)*
- **Update cadence not documented in captured sources.** Neither tool's primary-source page specifies how often the underlying data is refreshed. Stale data is the generic risk for any ethical-shopping tool.

## Source

- `raw/research/lever-implementations/05-05-wikipedia-buycott.md`
  - **Origin:** Wikipedia article *Buycott.com*.
  - **Audience:** general public.
  - **Purpose:** tool overview, campaign structure, company history.
  - **Trust:** starting reference.
- `raw/research/lever-implementations/06-06-goods-unite-us.md`
  - **Origin:** Goods Unite Us primary homepage.
  - **Audience:** prospective users.
  - **Purpose:** product-description page with current user / company / politician counts and the premium-tier price.
  - **Trust:** primary org source — self-reported scale figures; current as of 2026-04-22 capture.

## Related

- [[possible-strategic-levers]]
- [[consumer-collective-bargaining]]
- [[regulatory-responses]]
- [[park-slope-food-coop]] — standing-org precedent for the boycott mechanism
- [[transparency-tools]]
