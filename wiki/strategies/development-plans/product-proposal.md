# Product Proposal — Consumer Collective Power Platform

*Draft 1 — 2026-05-27*

---

## Vision

Build the infrastructure for collective consumer power: a platform that starts by giving individual users immediate, concrete protection from surveillance pricing, and scales into a coordinated bargaining collective capable of directing billions in consumer spending, automating data rights, and funding strategic litigation against extractive pricing practices.

The structural premise: the tools that have addressed surveillance pricing so far are either individual (protecting one user at a time) or corrupt (affiliate-funded tools that suppress the best deals to serve their partners). No product aggregates consumers into a force that can actually move markets. We build that.

---

## Core Principles

**1. Individual value before collective scale.**
The product must be useful to a single user on day one, before any network exists. Every feature that requires collective participation unlocks *after* individual utility is established. This solves cold-start without requiring trust in a promise.

**2. No affiliate conflicts — ever.**
The entire price-tool industry (Honey, Capital One Shopping, Keepa-for-resellers) is structurally compromised by affiliate commissions that pay the tool to show partner deals rather than best deals. The Honey scandal made this visible at scale. We are funded by members, not by the merchants we negotiate against. This is the foundational trust differentiator and it must be a constitutional constraint, not a policy.

**3. Collective ownership, not VC ownership.**
Members own the platform. This is what makes the "no affiliate conflict" principle durable: it cannot be reversed by an acquirer or a board. It is also the structural answer to the acquisition-and-sunset risk (Fakespot, 2023–2025) that has killed every mission-aligned consumer tool that reached scale. Cooperative or benefit-corporation structure required from incorporation.

**4. Cluster-first growth, not broadcast acquisition.**
Consumer collective action is a complex contagion problem: adoption requires reinforcement from multiple contacts in a trusted local cluster, not a single broadcast recommendation. We seed whole clusters (neighbourhoods, contact groups, workplaces) simultaneously via catalyst mechanics rather than growing one user at a time. The unit of growth is the cluster, not the individual user.

**5. Opt-out default at threshold.**
Once a cluster reaches activation threshold, collective features (demand coordination, group deals, DSAR automation) enrol members by default with a simple opt-out. This is the Community Choice Aggregation lesson: opt-in models of the same type produced almost nothing; opt-out produced 1,850+ CCAs serving 15% of Americans. Pure consumer choice — risk class 1, no legal exposure.

**6. Privacy-preserving by design.**
The product's purpose is to protect users from surveillance. It cannot itself surveil. Data minimisation, on-device processing where possible, no sale of user data in any form, and GPC/OOPS signals asserted automatically on behalf of members.

---

## Platform Recommendation

**Primary surface: Mobile app (iOS + Android)**

Browser extensions are the wrong primary platform in 2026. Google's MV3 transition (Chrome 138, July 2025) permanently removed `webRequest` — the API needed for price overlays, tracker blocking, and affiliate modification. uBlock Origin lost ~78% of its Chrome user base overnight. Mobile dominates consumer commerce; iOS and Android have no extension support in standard browsers.

**Secondary surface: Browser extension (desktop only)**
A lightweight MV3-compatible extension for desktop users — passive price-history overlay, GPC signal assertion, clean-session comparison trigger. No request interception; no features that require MV2 capabilities. This is a secondary surface for power users, not the primary acquisition channel.

**Technology stack recommendation:**

| Layer | Recommendation | Rationale |
|---|---|---|
| Mobile | React Native | Cross-platform (iOS + Android from one codebase); large talent pool; Expo for rapid prototyping |
| Backend API | Python (FastAPI) | Fast to build, strong ML ecosystem for price analysis |
| Database | PostgreSQL + Redis | Postgres for user/pricing/collective data; Redis for real-time coordination and session state |
| Price comparison engine | Playwright (headless Chromium) | Clean-session baseline checks server-side; mature API; handles JS-heavy retail sites |
| Privacy signals | Native HTTP headers + app-layer | GPC signal is a single HTTP header; straightforward to implement |
| Federated learning (Phase 3) | TensorFlow Federated or Flower | For pricing observatory without centralised data pool |
| Auth | Phone number (Signal model) | Pseudonymous; contact-graph discovery without requiring real identity; no email required |
| Cooperative infrastructure | Open Collective or purpose-built | Membership dues, governance votes, dividend distribution |

**Hosting:** Standard cloud (AWS/GCP) for Phase 1–2. Evaluate member-owned cooperative infrastructure (Hostsharing eG pattern) at Phase 3 when the governance model warrants it.

---

## Phase 1 — Hook Features (Individual Utility, No Collective Required)

These three features work for a single user on day one. They are the acquisition engine and the trust deposit.

### Hook A: Personalisation Detection — "Are you being ripped off?"

**What it is:** The app runs a clean-session comparison when a user views a product or booking. It shows: "You see $X. Clean session sees $Y. You are being charged Z% more."

**Why it's the lead hook:**
- Genuine white space — no consumer product at scale does this today. The only prior attempt (Northeastern PriceSteering, 2016) was academic and never launched.
- Immediate anger/outrage trigger — the most viral consumer-backlash pattern documented across airlines, hotels, rideshare, and retail.
- Shareable artifact: "I was charged 23% more than baseline on this flight" is worth posting to a WhatsApp group or Slack channel. Every share is an acquisition event — non-users encounter the report and install to run their own.
- Direct class-action enrolment path: *Phillips v. JetBlue* (1:26-cv-02405, filed April 2026) is the first US class action framing cookie/cache-based price personalisation as a privacy harm. Our discrimination reports are the evidence record.

**How it works technically:**
1. User views a product/booking page and taps "Check my price"
2. Backend spins up a headless Playwright session with no cookies, no history, fresh fingerprint
3. Retrieves the same page, same product, same search parameters
4. Compares user-seen price vs. clean-session price
5. Generates a shareable report card: item, user price, baseline price, delta, timestamp, site

**Accuracy caveat to build into the UX:** Price differences can have non-discriminatory causes (inventory, time of day, A/B tests). The report is evidence, not proof. The framing is "investigate this" not "you were definitely discriminated against." This is honest and reduces legal exposure.

**Initial target categories:** Flights (highest price sensitivity, clearest personalisation evidence from JetBlue case), hotels, major e-commerce (Amazon, Best Buy). Expand from there.

---

### Hook B: Price History and Cooperative Deal Alerts

**What it is:** Price history charts and deal alerts for products users track — built on crowdsourced member price submissions, not affiliate-model scraping.

**Why it's differentiated from Keepa/Honey:**
- No affiliate commissions. We show the actual best price, not the partner price. The Honey scandal created an explicit consumer demand for a trustworthy alternative.
- Crowdsourced model (GasBuddy pattern): members submit prices they see → everyone sees the aggregate. Contribution IS the entry behavior. Cold-start is solved because individual submissions have immediate individual return.
- Collective framing: "Your price report helped 12,000 other members find a better deal this week."

**How it works:** Members submit price observations passively (receipt scan, manual entry, or auto-capture from Hook A clean-session runs). Data is aggregated per product/retailer. Members set price-drop alerts. Price data feeds the Phase 3 pricing observatory.

---

### Hook C: Automatic Privacy Signals

**What it is:** The app silently asserts GPC (Global Privacy Control) and OOPS opt-out signals on behalf of members when browsing in the app's built-in browser or via the companion extension.

**Why it works as a hook:** Passive, no friction, immediate value. Brokers are mandated to honour GPC by January 2027 (California law). "We assert your opt-out rights automatically every time you browse" is a credible membership benefit that works from day one with zero effort from the user.

**Bonus layer:** Pair with one-click DSAR submission to all registered data brokers (California DROP platform, Connecticut PA 26-64 centralized deletion portal live July 2028). "We deleted your data from 500+ brokers" is a recurring engagement driver because brokers re-enrol.

---

## Phase 2 — Membership Tier (Low Threshold Collective Features)

Once the user has experienced Hook A/B/C and trusts the product, convert to a membership relationship:

- **DSAR automation** — automated data broker deletion, re-submission on re-enrolment, compliance monitoring and reporting ("43 of 500 brokers violated your deletion request; we filed complaints")
- **Class-action enrolment** — members who have documented personalisation discrimination events (from Hook A reports) are automatically offered enrolment in relevant class actions
- **GPC enforcement reporting** — if a broker fails to honour GPC, we report it to the relevant state AG on member's behalf (California, Connecticut, Colorado all have enforcement mechanisms)
- **Cooperative membership dues** — small monthly fee (e.g., $3–5/month) funds the litigation war chest, DSAR infrastructure, and cooperative governance. Members get a vote.

---

## Phase 3 — Collective Activation (Threshold-Dependent Features)

These features unlock when the membership pool crosses a critical mass — estimated at 10,000–50,000 active members in a target market based on algorithmic collective action empirics (0.025% of affected users produces disproportionate effects on recommender systems; pricing-algorithm threshold needs empirical calibration).

- **Demand-strike coordinator** — "48,000 members are avoiding Amazon for electronics this week; here are alternatives." Pure consumer choice (risk class 1). Works across 4 of 6 pricing-algorithm families. No legal exposure.
- **Collective switching threat** — pre-committed member pool as credible threat to switch vendor simultaneously. The threat, not execution, is the bargaining chip.
- **Pricing observatory publication** — aggregated Hook A data published as a quarterly report: "We documented $X in personalised overcharges across Y members at these companies." Drives press, regulatory attention, and class-action standing.
- **Group-buy deals** — suppliers who agree to collective pricing get access to the member pool. First targets: grocery staples, broadband, pharmacy, insurance (commodities with elastic supply-side response; airline RM and neural retail demand are outside consumer-side disruption per our research).
- **Opt-out default activation** — collective features enrol all active members by default at threshold crossing; simple 2-tap opt-out. CCA-model mechanics applied to consumer goods.

---

## Phase 4 — Negotiating Power (GPO-Scale)

- **GPO-style contracts** — formal standing contracts with suppliers for member pricing, modelled on healthcare Group Purchasing Organisations ($36B/yr in documented savings, 90% of US hospital purchases negotiated this way)
- **Strategic litigation war chest** — pooled member dues funding class actions, regulatory complaints, and NOYB-style strategic cases. NOYB template: 4,400 members → Schrems II (invalidated Privacy Shield) + €50M Google fine + €5M Spotify fine
- **CBI representation** — members grant the cooperative standing to negotiate data terms on their collective behalf
- **Federated Pricing Observatory** — cooperative price-discrimination detector without a trusted aggregator (federated learning across member devices). Publishable data that survives any attempt to shut down individual data sources.

---

## Local Graph Strategy — Which Type and How to Seed

### Recommended cluster unit: Geographic neighbourhood + contact graph fallback

**Primary: Geographic neighbourhood (Nextdoor model)**
- Scope: ~500–1,000 households per cluster (ZIP code sub-area or postal district)
- Why: Directly relevant to the most actionable collective features — local grocery pricing, neighbourhood utility deals, community group-buy campaigns. Shared economic interest is highest among geographic neighbours.
- Trust substrate: physical co-location. "My neighbour is in this" is a more powerful trust signal for consumer financial action than "someone on the internet recommended it."
- Verification: Lightweight address confirmation (ZIP code self-report + one address-level verification step — does not need Nextdoor's full postcard friction for Phase 1; can tighten as the platform matures).

**Fallback: Phone contact graph (WhatsApp/Signal model)**
- For users in cities where neighbourhood density hasn't been seeded yet, inherit the contact graph: "7 of your contacts are already members."
- This enables value from day one regardless of neighbourhood coverage.
- Contact graph discovery via phone address book (opt-in, privacy-preserving — compute intersection on-device, not server-side).

### Seeding strategy: Catalyst mechanic

Do not try to grow one user at a time. Seed whole clusters simultaneously.

**Step 1 — Identify catalysts in 3–5 target cities.**
Find community leaders with existing mailing lists or group admin rights:
- Neighbourhood association chairs
- Local Facebook group admins (5K+ member local groups)
- Nextdoor neighbourhood leads
- Union stewards / workplace group organisers
- Local subreddit moderators

These individuals can invite 50–200 members from a single send. One catalyst activation = the density a solo acquisition strategy would take months to build.

**Step 2 — Activate the catalyst with a specific local value proposition.**
Not "join our privacy app" — "we found that residents of [neighbourhood] are being charged an average of X% more than baseline on grocery delivery. Here's the report. Your neighbours are checking their prices."

**Step 3 — Threshold gamification.**
Show the cluster its progress: "Your neighbourhood has 34/100 members. At 100, you unlock collective pricing for [local grocery store]." The progress bar creates local social obligation — existing members recruit neighbours to close the gap.

**Step 4 — Organic expansion from seeded clusters.**
Seeded clusters generate shareable price-report artifacts → non-members in adjacent clusters see them → install → new cluster forms. Expansion tracks real social graphs, not algorithmic targeting.

---

## Algorithms and Technologies to Establish

### Price discrimination detection pipeline
- **Clean-session management:** Playwright headless Chromium; rotate IP per run; fresh cookie jar; neutral user-agent string matching the most common real-world fingerprint profile (not a fake — a real device profile that belongs to the largest cohort in the wild, implementing the "blending in" principle)
- **Price extraction:** site-specific CSS selectors + LLM-assisted extraction fallback for sites that change layout frequently
- **Statistical baseline:** running median of clean-session prices for each (product × retailer × geography × time-window) tuple; flag user-seen prices that exceed the 90th percentile of the clean-session distribution. Time-window is important — legitimate price variation is temporal.
- **False-positive suppression:** dynamic pricing (Uber surge, airline seat classes) generates legitimate price variation. Build a pricing-algorithm taxonomy classifier per retailer to suppress known-dynamic-pricing cases from discrimination alerts.

### Crowdsourced price intelligence
- **Receipt OCR:** ML-based receipt parsing (established models: Taggun, Veryfi, or open-source DONUT). Extract: retailer, item, price, date, location.
- **Price normalisation:** product matching across receipts (barcode UPC where available; fuzzy name matching where not). This is the hardest data-quality problem — invest here early.
- **Aggregate model:** per-(product × retailer × geography × week) price distribution. Surfaces outliers (price discrimination candidates) and trends (price creep, promotional patterns).

### Privacy signal infrastructure
- **GPC implementation:** single HTTP header (`Sec-GPC: 1`) + DOM property (`navigator.globalPrivacyControl = true`). Add to both app in-browser and extension. Trivial to implement; legally mandated response from brokers by Jan 2027.
- **Fingerprint parity pool:** all members share a common browser baseline when using the in-app browser — same canvas fingerprint, same WebGL renderer hash, same audio signature. Implement via server-side fingerprint profile distribution (all clients load and present the same profile). This collapses individual identification entropy; the pool must be large enough that the shared profile blends with organic traffic.
- **DSAR automation:** integrate with California DROP API (live Jan 2026) and Connecticut centralised deletion portal (live Jul 2028) for automated batch submissions. For other jurisdictions: form-submission automation via Playwright.

### Collective coordination
- **Threshold commitment device:** members pre-commit to a collective action (demand redirect, switching threat) conditional on N others committing. Smart-contract-style escrow logic in the backend: commitments are locked but not executed until threshold is reached; expire after a time window. The commitment is the bargaining chip; execution is the fallback.
- **Contact graph discovery (privacy-preserving):** phone address book → hash phone numbers on-device → send hashes to server → server returns intersection with registered members → user sees "7 contacts are members" without server ever seeing raw phone numbers. Signal's Private Contact Discovery pattern.

---

## Prototype: First Steps (Weeks 1–8)

### Week 1–2: Foundation
1. **Incorporate.** Benefit corporation or cooperative structure. This is not an afterthought — the "no affiliate conflict" constitutional constraint must be in the founding documents. Decision needed: full cooperative (member-owned, democratic governance) vs. benefit corporation with cooperative mechanics bolted on. Faster to start: benefit corporation; more structurally sound long-term: cooperative.
2. **Waitlist landing page.** Single page: value proposition ("find out if you're being charged more than everyone else"), email capture, referral queue mechanic (refer 3 friends → jump 500 places). Target: 10,000 waitlist signups before app launch. $0 ad spend if the shareable artifact hook works.
3. **Define 3 target cities.** Pick cities with: (a) active neighbourhood association culture or large local Facebook groups, (b) documented pricing controversies (JetBlue hub airports, cities with known grocery delivery price complaints), (c) founding team's existing networks for catalyst identification.

### Week 3–4: Price discrimination detection MVP
4. **Build the clean-session comparison backend.** Playwright + FastAPI. Start with one retailer category (airline flights — highest anger/virality, clearest case law). Inputs: URL or search parameters. Output: {user_price, baseline_price, delta_pct, timestamp}. No mobile app yet — just the API.
5. **Build the shareable report card.** Static PNG or HTML generated server-side: retailer logo, product, user price, baseline price, delta, "Checked by [Platform Name]" watermark. This is the viral artifact. Spend real design time here.
6. **Manual testing in the 3 target cities.** Before building the full app, run the clean-session comparison on real purchases made by 20–50 beta users and document the results. This is the content for the catalyst outreach in Week 7.

### Week 5–6: Mobile app skeleton
7. **React Native app, minimal.** Screens: (a) home / dashboard, (b) "check my price" — user pastes or shares a URL, (c) result / shareable report card, (d) price history for tracked products (manual submission only at this stage — no receipt OCR yet), (e) settings / GPC toggle.
8. **Phone auth.** SMS OTP for account creation. Store phone hash server-side, not raw number. This is also the contact-graph discovery substrate.
9. **GPC signal.** Implement in the app's in-built browser view. Single HTTP header. Checkbox in settings; on by default for members.

### Week 7–8: Cluster seeding
10. **Identify 5–10 catalysts per target city.** Research: local Facebook group admins with 5K+ members, neighbourhood association chairs, active local subreddit moderators. Cold outreach with the local price-discrimination data from Week 6: "We found that people in [neighbourhood] are being charged an average of X% more on flight searches. We're building a tool to fight this — would you share it with your community?"
11. **Catalyst-assisted launch.** Provide each catalyst with: (a) a pre-written message to send to their community, (b) a personalised neighbourhood price-discrimination report as the lead hook, (c) their own referral link to track their cluster's growth. Target: 100+ activated members in each seeded cluster within 72 hours of catalyst send.
12. **Cluster progress bar.** Show each cluster its progress toward the 100-member local activation threshold. Make it visible in the app's home screen for all members.

### Key decisions before Week 1
- **Platform name.** Needs to convey collective power and trust; not "privacy app" framing (too narrow); not "savings app" framing (too easily associated with affiliate models). Something that signals collective/cooperative. Examples: Fair Market, Common Price, Accord, The Collective. This matters for the waitlist landing page.
- **Cooperative structure.** Benefit corp (faster) vs. full cooperative (more structurally sound). Consult a cooperative attorney before incorporating.
- **First retailer category.** Flights are the highest-anger hook and have the best legal precedent (JetBlue case). But flight price discrimination is technically harder to isolate from legitimate dynamic pricing. Alternative first category: hotels (clearer personalisation evidence, less legitimate dynamic pricing) or Amazon (clearest price discrimination evidence, most daily relevance). Recommendation: flights for the waitlist/press narrative; Amazon for the technical MVP (more reliable clean-session comparison).

---

## What This Is Not

- Not a VPN company. Privacy is a means, not the product identity.
- Not a coupon app. Coupons are the affiliate model in a different dress.
- Not a price comparison site. Comparison sites show merchant-paid rankings.
- Not a browser extension. Extensions are dead as a primary channel for our use case.
- Not a data broker. We do not sell member data in any form.

---

## Competitive Moat

The moat is not technology — clean-session comparison and price history are buildable by anyone. The moat is:

1. **Trust, built through cooperative ownership.** Once members trust that we have no affiliate conflict and cannot be acquired, they share more data and act on collective recommendations. This trust takes years to build and minutes to destroy.
2. **Accumulated price-discrimination evidence.** Our price-discrimination database grows with every member check. It becomes the evidence base for class actions, regulatory complaints, and press investigations that no single user or journalist could assemble alone.
3. **Committed member pool.** A pre-committed collective with threshold mechanics is the negotiating asset. Suppliers cannot recreate this; they can only respond to it.
4. **Legal standing.** The cooperative, as the representative of a large documented-harm class, has standing that individual users and commercial products do not.

---

## References (wiki pages)

- [[bootstrap-strategy]] — full hook-to-collective funnel design
- [[data-disruption-strategy-map]] — lever risk classes and algorithm coverage
- [[mechanism-synthesis-readout]] — Tier 1/2/3 build portfolio
- [[local-network-graph-products]] — empirical product patterns for cluster design
- [[consumer-price-tools]] — competitive landscape
- [[dsar-and-data-deletion]] — DSAR infrastructure
- [[consumer-facing-dynamic-pricing]] — *Phillips v. JetBlue* legal template
- [[algorithmic-collective-action]] — threshold dynamics
- [[complex-contagion]] — cluster seeding theory
- [[browser-fingerprinting]] — fingerprint parity pool design
- [[buyer-cartels-antitrust]] — legal safe harbours for collective action
- [[community-choice-aggregation]] — opt-out default precedent
- [[consumer-collective-bargaining]] — GPO model
- [[noyb]] — strategic litigation template
