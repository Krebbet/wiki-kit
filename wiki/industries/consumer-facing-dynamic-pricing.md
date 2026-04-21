# Consumer-Facing Dynamic Pricing

Dynamic pricing has been standard in airlines and hotels for decades and has spread across ride-sharing, online retail, live-events ticketing, theme parks, sports, and — most recently and controversially — quick-service restaurants. This page catalogues industry-by-industry deployment with specific companies, numbers, and consumer-backlash moments as named in the wiki's sources.

## Airlines

- Standard industry practice for decades. Prices adjust in real time based on demand, capacity, timing, and competition. *(Wikipedia; NBER.)*
- **Delta** announced plans to expand AI-driven dynamic pricing from 3% to 20% of domestic flights during 2025. *(Wikipedia.)*
- Recent industry framing (OAG, 2025) emphasises shopping-data-driven "dynamic offers" rather than fare-class adjustment.

## Hotels and hospitality

- Rooms priced in real time by occupancy, season, events, booking pace, and competitor pricing. *(Wikipedia; NBER.)*
- **Hilton** named as employing dynamic pricing across room types and regions, with event-driven adjustments (Wimbledon, Super Bowl). *(Wikipedia.)*

## Ride-sharing

- **Uber** surge pricing raises fares during high-demand / low-supply periods. Fares during a 2013 NYC snowstorm reached 8× normal rates, drawing public criticism (including from Salman Rushdie). *(Wikipedia.)*
- In 2015, following that backlash, Uber agreed to cap surge pricing during emergencies. *(Wikipedia.)*
- **Lyft** uses a similar surge mechanism. *(Wikipedia.)*

## Online retail

- **Amazon** is the canonical example. By 2015, roughly one-third of its top 1,600 products were priced algorithmically. By 2018, the average Amazon product price changed every 10 minutes. *(Wikipedia; NBER; arXiv 2504.16592.)*
- In 2000, Amazon ran a controversial test offering different prices to different customers on DVDs — one of the earliest publicly-discussed personalised pricing experiments. *(Wikipedia.)*
- ProPublica reported that Asians were nearly twice as likely to be shown higher prices on SAT prep courses from The Princeton Review than non-Asians — an early landmark in algorithmic-pricing discrimination reporting. *(Wikipedia, via ProPublica citation.)*

## Live events and ticketing

- **Ticketmaster** adopted demand-based dynamic pricing for concerts in 2022. Resulting prices for high-demand artists were extreme — up to $600 for Blink-182 and $4,000–$5,000 for Bruce Springsteen. *(Wikipedia.)*
- The 2024 Oasis reunion tour triggered mass complaints in the UK and Ireland. UK Advertising Standards Authority complaints followed; the Competition and Markets Authority opened an investigation and concluded Ticketmaster "may have misled" fans about dynamic pricing disclosure. The European Commission opened a parallel investigation. *(Wikipedia.)*
- **FIFA** announced in May 2025 it would use dynamic pricing for the 2026 World Cup and the 2025 Club World Cup. *(Wikipedia.)*
- Multiple high-profile artists have publicly refused dynamic pricing: **Coldplay, Taylor Swift, Ed Sheeran, Iron Maiden, Robert Smith**. Crowded House (2020) publicly asked its promoter for refunds after discovering dynamic pricing was used without the band's approval. *(Wikipedia.)*
- An early 2012 example: **Heart of Midlothian FC** introduced dynamic pricing on season tickets and faced significant fan backlash. *(Wikipedia.)*

## Theme parks

- **Disneyland and Disney World** adopted dynamic pricing in 2016 — up to 20% peak-time increases. **Universal Studios** followed. *(Wikipedia.)*

## Professional sports

- Roughly two-thirds of MLB teams (including the **San Francisco Giants**) use dynamic pricing software from **Qcue**. NBA, NHL, and NCAA teams also named. *(Wikipedia.)*

## Quick-service restaurants

- **Wendy's** announced in 2024 a $20 million investment in AI-powered digital menu boards that would adjust burger prices by time of day. *(Wikipedia.)*
- The announcement triggered widespread consumer backlash; Wendy's subsequently clarified that the feature would be used only to *lower* prices during low-traffic periods. *(Wikipedia.)*

## Public transit and tolls

- **San Francisco Bay Bridge** peak tolls, **London congestion charge**, **Washington Metro** peak fares are all named as dynamic-pricing deployments. *(Wikipedia.)*

## Electricity

- **Griddy**, a Texas energy retailer using a pure real-time wholesale-price pass-through model, defaulted after the February 2021 Texas power crisis when wholesale prices spiked and customers received bills of thousands of dollars. *(Wikipedia; arXiv 2504.16592.)*

## Grocery and electronic shelf labels (ESLs)

- ESLs enable algorithmic pricing in brick-and-mortar stores. An NBER case study of 225 North American retail locations documented ESL deployment. *(NBER.)*
- Many regional grocery chains employ dynamic pricing on specific categories. *(Wikipedia; FTC 4–5 for the surveillance-pricing variant — see [[surveillance-pricing-retail]].)*

## Cross-industry consumer backlash as a pattern

Backlash moments surface recurrently across sources:
- Uber 2013 storm → emergency cap.
- Heart of Midlothian 2012 → fan revolt.
- Ticketmaster 2022–2024 → UK CMA and EU Commission investigations; artist defections.
- Wendy's 2024 → forced clarification.
- Crowded House 2020 → band demanded refunds.

These are individual episodes, not a coordinated movement. But they establish that dynamic pricing has recurring fairness and disclosure failure modes that surface as visible backlash — a useful signal for the counter-power question. See [[regulatory-responses]].

## Design-input candidates *(editorial — not source content)*

- **Dynamic-pricing disclosure browser.** Extension or mobile overlay that flags, at checkout, when a price is known to be dynamic for the sector (Ticketmaster, Uber, Amazon, etc.) and shows the price history for comparable transactions.
- **Event-backlash coordinator.** Ticketmaster's UK/EU trouble came from mass individual complaints amplified by media. A structured complaint-aggregation tool (one click, pre-drafted regulatory submission text, routed to the right regulator) would industrialise the episodic backlash pattern.
- **Sector refusal registry.** A simple public registry of artists, venues, sports teams, and restaurant chains that have publicly refused dynamic pricing — queryable by consumers before purchase, and by artists/venues considering their own policy.

## Source

- `raw/research/dynamic-pricing-landscape/03-wikipedia-dynamic-pricing.md`
  - **Origin:** Wikipedia (community-edited encyclopaedia).
  - **Audience:** general public.
  - **Purpose:** define the term and catalogue industry uses with citations to news coverage.
  - **Trust:** starting reference; industry claims and numbers above are traceable to Wikipedia's footnoted sources.
- `raw/research/dynamic-pricing-landscape/06-nber-algorithmic-pricing.md`
  - **Origin:** NBER working paper (Zeithammer et al.), 2024/2025.
  - **Audience:** academics, policymakers, pricing managers.
  - **Purpose:** survey algorithmic pricing implementation including industry case studies.
  - **Trust:** NBER working-paper tier.
- `raw/research/dynamic-pricing-landscape/07-hbs-dynamic-pricing-harm.md`
  - **Origin:** Harvard Business School working paper 22-050 (MacKay and Weinstein).
  - **Audience:** academics, legal scholars, policymakers.
  - **Purpose:** analyse consumer harm from algorithmic pricing and propose regulatory remedies.
  - **Trust:** HBS working-paper tier; used here for industry-deployment examples (Amazon, Uber, Lyft, hotels).

## Related

- [[dynamic-pricing-overview]]
- [[surveillance-pricing-retail]]
- [[rental-housing-algorithmic-pricing]]
- [[algorithmic-collusion]]
- [[regulatory-responses]]
