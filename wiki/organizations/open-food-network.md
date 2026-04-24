# Open Food Network (OFN)

Open Food Network is an **open-source software platform** that lets individual farmers sell directly to customers, and lets groups of farmers collaborate in online-marketplace form. Not-for-profit, globally federated, **1% of sales fee**. The closest live implementation on this wiki of [[possible-strategic-levers|strategic levers #17 (CSA-at-metro-scale) and #18 (direct-marketplace federation)]] — i.e., the [[coopcycle|CoopCycle federation pattern]] applied to food supply.

## Structure

- **Host:** not-for-profit (per the captured Open Food Network primary page and WebSearch preamble).
- **Technology:** open-source. "Anyone can contribute to the project, and everything that is built into it is part of a global, shared commons" (WebSearch preamble).
- **Jurisdictional presence:** multi-country (UK, Canada, Australia, and more — federation of country-level OFN organisations; captured `openfoodnetwork.org` is the global umbrella and `openfoodnetwork.org.uk` is the UK instance).
- **Fee model:** **1% of farmers' sales** (per the captured *software-platform* page). Funded by "pooling funding around the world" to keep cost low.

## Mechanism (per captured Software Platform page)

The platform supports three distinct seller-topologies on one codebase:

1. **Individual farmer online shop.** "Food Producers can create an online shop, collect payments, sell through other shops on the platform and access reduced-rate courier services."
2. **Cooperative aggregation.** "The platform can help aggregate from multiple producers through one online shopfront, or enable you to sell to multiple shopfronts."
3. **Virtual farmers' market.** "Communities can bring together producers in their local area to create virtual farmers' markets, building a resilient local food economy."

### Payment flow

Per the captured primary source:

> There is just **one payment made by the customer** but the platform pays each of the farmers directly and immediately without taking a fee.

Structural note: the payment split happens inside the platform but each farmer gets paid directly — the platform does not hold funds or clip a per-transaction margin. The only revenue to the platform is the 1%-of-sales subscription-style fee.

## Counter-power mechanism

Open Food Network is the **disintermediation pattern** ([[possible-strategic-levers|lever #5]]) implemented at software-platform scale for food. Distinct from:

- **[[drivers-cooperative|The Drivers Cooperative]]** (rideshare disintermediation via a single-city worker-owned platform) — different sector, single-location vs OFN's global federation.
- **[[coopcycle|CoopCycle]]** (bike-delivery worker-coop federation across 12 countries) — closest structural match; same federation-first architecture applied to a different logistics layer.
- **[[park-slope-food-coop|Park Slope Food Coop]]** (single-location consumer coop with direct-supplier procurement) — OFN is software; PSFC is a brick-and-mortar cooperative. They could plausibly integrate (PSFC as an OFN instance).

Core structural choices that make it a transferable template:

1. **Open-source codebase under a shared commons.** Any community can stand up its own instance without paying licensing to a central platform operator.
2. **1% fee, no per-transaction margin.** The platform captures minimal economic value from each transaction — farmers retain the rest. This is the direct inverse of Uber-style 25–40% commission or [[drivers-cooperative|The Drivers Cooperative's 15%]] — OFN sets the lower bound for what "minimal extraction" looks like in a software-platform marketplace.
3. **Payment routing is direct.** Platform is a coordination layer, not a financial intermediary. Reduces custody risk, regulatory surface, and failure-mode for the platform.
4. **Multi-topology support on one codebase.** Individual farmer, cooperative-aggregated, and community-federated marketplaces all run on the same platform. Operational overhead for new instances is low.

## Relevance for dynamic-pricing strategy

*(editorial / synthesis — OFN targets food supply disintermediation, not pricing algorithms directly.)*

OFN is the existence-proof that the [[coopcycle|federation-first architecture]] transfers from delivery (CoopCycle) to retail (OFN). The relevant lessons for a pricing-counter strategy:

1. **Cooperative-technology can be multi-tenant and multi-topology without extracting.** Any development plan building an observatory, data coop, or buyer-side bargaining infrastructure can point to OFN as a working proof that shared software + low-fee sustainability is viable at international scale.
2. **The 1% fee model is a target for a buyer-side data coop.** [[regulatory-responses|Design-input #2 (buyer-side data co-op)]] needs a sustainable revenue model; 1% of transaction volume through the coop is one option. Open question: whether a pricing-coop's volume is large enough to sustain the operation at that fee.
3. **Direct-producer alternatives deprecate pricing-personalisation surface.** Transactions routed through OFN are not visible to the personalisation pipelines of broker-retailers. Supply-side disintermediation is an indirect but durable defence against pricing-algorithm extraction — the pricing algorithm has nothing to work with.

## Scope and limitations

- **Primary-source thinness:** the captured *software-platform* page is 4.5KB — compact product-description. Load-bearing claims (1% fee, international scope, direct-payment flow, open-source status) are from the primary source but not supported by independent audits in the captured material.
- **Food-sector only.** OFN is explicitly for food producers; the platform's category-specific features (courier services, fresh-produce logistics) are not directly transferable to non-food categories without rework.
- **Geographic reach asymmetric.** UK, Canada, and Australia have more developed OFN instances than the US. US food-hub software is fragmented — GrownBy (US-focused equivalent, per WebSearch preamble) and Alabama Cooperative Extension e-commerce guidance suggest a US-side gap.
- **Pricing feature unclear from captured source.** Whether OFN supports dynamic pricing at all, and what its default pricing-UX is, is not addressed in the captured software-platform page.

## Source

- `raw/research/lever-implementations/07-07-open-food-network.md`
  - **Origin:** Open Food Network `openfoodnetwork.org/software-platform/`.
  - **Audience:** potential farmer / cooperative users.
  - **Purpose:** product description of the software platform, payment-flow explanation, not-for-profit framing.
  - **Trust:** primary org source. Self-reported fee and scope figures.

## Related

- [[coopcycle]]
- [[platform-cooperatives]]
- [[drivers-cooperative]]
- [[park-slope-food-coop]]
- [[consumer-collective-bargaining]]
- [[possible-strategic-levers]]
