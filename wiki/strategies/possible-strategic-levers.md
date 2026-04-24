# Possible Strategic Levers

Inventory of strategic levers for combating consolidated industry power and pricing mechanisms documented on the [[dynamic-pricing-overview|reference layer]] of this wiki. First page of the new `strategies/` section of the wiki — the **editorial / design layer** that complements the factual reference layer.

Each lever is (a) a proposed mechanism for consumer counter-power, (b) mapped to a reference-layer wiki anchor where one exists, and (c) paired with candidate tech implementations. The "Research Needed?" column flags levers where the factual basis is thin enough that a `/research` run is warranted before building.

Scope note: this page deliberately includes levers that would face legal friction. **Legal tractability is not the filter here** — per user intent, we cast a wide net and note the regulatory surface rather than disqualifying on it. Where a lever runs into documented antitrust or ToS friction, it is flagged in its full description.

## How to read this page

- **Summary table** — at-a-glance inventory of every lever with tech-solution shorthand and research status.
- **Lever descriptions** — full write-up by category, with wiki citations for the documented parts and explicit editorial tags for the novel parts.
- **Status convention:** reference-layer mechanisms (e.g., [[data-cooperatives]], [[community-choice-aggregation]]) are documented with sources; levers here that extend them inherit that source traceability. Levers marked *(editorial)* are design synthesis without captured primary sources.

## Summary table

| # | Lever | Category | Reference-layer anchor | Possible tech solutions | Research needed? |
|---|---|---|---|---|---|
| 1 | Many-consumer counterbalance (informational + pricing) | A. Aggregation | [[collective-bargaining-for-data]], [[data-cooperatives]], [[consumer-collective-bargaining]] | Buyer-side data co-op platform; CBI-intermediary membership stack; fair-price inference service | N — well-sourced |
| 2 | Pooled info for collective redirection | B. Collective redirection | [[transparency-tools]], [[regulatory-responses]] § 7, [[park-slope-food-coop]] | Continuous-observation pipeline + flash-redirection recommender; alternative-vendor directory | **Y** — real-time per-transaction redirection not theorised; research redirection-latency thresholds |
| 3 | Profile manipulation against pricing algorithms | C. Profile / algorithm manipulation | [[obfuscation]], [[adversarial-data-poisoning]], [[browser-fingerprinting]], [[collective-bargaining-for-data]] (Porat 2024, individual only) | Session-rotation extension; demographic-spoofing layer; coordinated probe-and-publish tool; feature-label ACA tool | **Y (partial)** — reference-layer mapping now in place (post 2026-04-23 obfuscation-deep-dive); pricing-domain engineering + DP-counter response remain gaps |
| 4 | Account-leveraging to access lower-price accounts | D. Account arbitrage | [[transparency-tools]] (Hannak 2014 members-only pricing), [[consumer-collective-bargaining]] (Tuángòu) | Group-buy coordinator (Pinduoduo pattern, social-graph-embedded); account-pool purchasing agent; demographic-optimised signup orchestration | **Y** — pricing-favoured-demographic mapping across sectors not captured |
| 5 | Direct-to-producer disintermediation | E. Disintermediation | [[platform-cooperatives]], [[coopcycle]], [[drivers-cooperative]] | CSA-at-metro-scale platform; direct-marketplace federation; producer-coop × consumer-coop matching | **Y** — CSA / food-hub / farmers-market ecosystem not yet on reference layer |
| 6 | Session-identity rotation-as-a-service | C. Profile / algorithm manipulation | [[browser-fingerprinting]], [[obfuscation]], [[collective-bargaining-for-data]] (Porat) | Browser extension: rotating fingerprint + cookie jar + plausible demographics per session | **Research-backed design constraint** — joint-distribution-preserving rotation required (FP-Inconsistent ~97% TNR on per-attribute spoofing) |
| 7 | Demographic spoofing to cheapest-segment treatment | C. Profile / algorithm manipulation | [[transparency-tools]] (Hannak 2014), [[browser-fingerprinting]] | Extension that always presents as the segment that gets lowest prices per retailer | **Y** — per-retailer favourable-segment mapping |
| 8 | Coordinated probe-and-publish | C. Profile / algorithm manipulation | [[transparency-tools]] (Hannak 2014 inverse) | Probe-and-publish observatory; crowd-sourced account variation; inferred-pricing-function publisher | N — methodology well-documented via Hannak |
| 9 | Collective training-data withdrawal | C. Profile / algorithm manipulation | [[collective-bargaining-for-data]] (Porat's erasure lever) | Batch GDPR / CCPA deletion orchestrator; cookie-revocation campaign coordinator | **Y** — batch-erasure legal mechanics across jurisdictions |
| 10 | Adversarial training-data injection | C. Profile / algorithm manipulation | [[adversarial-data-poisoning]] (ACA formalism + poisoning-attack taxonomy), [[obfuscation]] | Bots / scripts submitting shaped browsing/carting behaviour to degrade model features; feature-label ACA tool | **Y (partial)** — formalism exists (Solanki et al. 2025); pricing-model online-learning adaptation is engineering gap; DP-as-firm-counter is live political risk |
| 11 | Fingerprint parity network | C. Profile / algorithm manipulation | [[browser-fingerprinting]] (Tor uniformity precedent) | Shared rotating fingerprint pool across members; network-level identity homogenisation | **Y** — network-size feasibility unvalidated; parity signature risks being singled out as unusually-shared |
| 12 | Flash-redirection observatory | B. Collective redirection | [[markup-citizen-browser]], [[transparency-tools]] | Observatory + real-time classifier + redirect recommender + alternative-vendor directory | **Y** — redirect-latency + false-positive rate empirically unknown |
| 13 | Buy-cott coordinator | B. Collective redirection | [[regulatory-responses]] § 7, [[park-slope-food-coop]] | Directory of "good-actor" sellers + consumer routing tool | **Y** — qualifying-criteria standardisation |
| 14 | Demand-strike coordinator | B. Collective redirection | [[collective-bargaining-for-data]] (Porat scaled collectively) | Threshold-triggered coordinated abstention; credible-commitment signalling | **Y** — commitment-device design + empirical threshold sizing |
| 15 | Price-violation bounty | B. Collective redirection | [[open-tenant-screening]] (donate-report pattern) | Paid crowd-contribution pipeline for violation evidence; bounty war chest governance | N — OpenTSS donation pattern is close-enough template |
| 16 | Threshold-triggered flash campaigns | B. Collective redirection | *(editorial — Kickstarter model)* | Conditional-commitment platform: "I'll boycott IFF N others also commit" | **Y** — platform design + legal commitment-device surface |
| 17 | CSA-at-metro-scale | E. Disintermediation | [[coopcycle]] (federation blueprint), [[park-slope-food-coop]] (direct-sourcing) | Metro-scale federation of CSA / food-hub coops; subscription-commitment matching platform | **Y** — CSA / food-hub mechanism page missing from wiki |
| 18 | Direct-marketplace federation | E. Disintermediation | [[coopcycle]], [[platform-cooperatives]] | Multi-sector federated marketplaces (food, repair, services) on cooperative shell | **Y** — cross-sector federation architecture unmapped |
| 19 | Producer-coop × consumer-coop matching | E. Disintermediation | [[platform-cooperatives]], [[data-cooperatives]] | Two-sided cooperative matching platform with neither side extracting | **Y** — no live example captured; research viable governance split |
| 20 | Time-bank / LETS | E. Disintermediation | *(editorial — cooperative-movement literature, not on wiki)* | Labour-hour / category-credit exchange platform bypassing monetary pricing entirely | **Y** — Time-bank / LETS mechanism page missing |
| 21 | Repair-and-reuse federation | E. Disintermediation | *(adjacent to right-to-repair, [[research-queue|Priority-3 queue]])* | Federated repair-cafe network + reuse marketplace | **Y** — right-to-repair run not yet done |
| 22 | Price-transparency overlay extension | F. Information layer | [[keepa]], [[transparency-tools]] | Browser extension injecting price history, personalisation flags, median-across-retailers at point-of-purchase | N — direct extension of Keepa pattern |
| 23 | Dynamic-pricing badge-of-shame | F. Information layer | [[fakespot]] (grading-UI precedent), [[regulatory-responses]] § 7 (reputational lever) | Public scorecard per retailer; browser extension surfacing the badge inline | **Y** — scoring methodology + grading criteria |
| 24 | Pricing-algorithm transparency score | F. Information layer | [[fakespot]] (A–F grade pattern) | Composite scorecard: algorithm disclosure, personalisation inputs, price-change frequency | **Y** — criteria weighting + update cadence |
| 25 | Algorithm-reverse-engineering competition | F. Information layer | [[transparency-tools]] (Hannak 2014, competitive variant) | Open bounty platform; team submissions of inferred pricing functions | **Y** — bounty economics + judging rubric |
| 26 | Consumer union with dues + war chest | G. Economic-structural | [[consumer-collective-bargaining]] (GPO inverse), [[rei]] (partial) | Standing member-funded org; pooled capital for class-action, alt-platform seed, lobbying, bounties | **Y** — legal form + revenue model + size-to-effectiveness threshold |
| 27 | Switching-cost observatory | G. Economic-structural | *(editorial — no wiki precedent)* | Per-category switching-cost estimator + automated switch tool (account closure, contract termination) | **Y** — full mechanism design |
| 28 | Mass-signup threshold coordination | G. Economic-structural | [[community-choice-aggregation]] (inverse of opt-out default) | Coordinated simultaneous opt-in / switch events at pre-announced moments | **Y** — credible-commitment and signalling design |
| 29 | CCA-equivalent default opt-out port | H. Regulatory-proxy | [[community-choice-aggregation]] | Map existing default-aggregation statutes in non-electricity sectors; build on them | **Y** — statutory-mapping research across healthcare, insurance, broadband, pharma |

**Count:** 29 levers across 8 categories. As of 2026-04-23: 5 levers have no remaining research gap; 4 levers have partial reference-layer support with a specific remaining gap flagged; 20 levers still have an open research gap.

### Working real-world implementations (added 2026-04-22)

Reference-layer research run 2026-04-22 added 10 new reference-layer pages documenting **live, working implementations** of specific lever mechanisms — mostly outside the pricing domain. Pointer table:

| Lever # | Lever | Working implementation captured | Page |
|---|---|---|---|
| 10, 11 | Obfuscation / profile manipulation | AdNauseam (ad-click obfuscation; banned from Chrome 2017); Nightshade + Glaze (UChicago, AI-training data poisoning); Privacy Badger (EFF, algorithmic tracker-learning). Reference-layer strengths/weaknesses/countermeasures captured via 2026-04-23 obfuscation-deep-dive. | [[obfuscation]] + [[adnauseam]] + [[nightshade-glaze]] + [[privacy-badger]] + [[adversarial-data-poisoning]] + [[browser-fingerprinting]] + [[obfuscation-strategic-readout]] |
| 2, 13 | Collective redirection | Buycott (UPC-barcode boycott campaigns); Goods Unite Us (7K companies, 2M users, FEC-data political alignment) | [[boycott-apps]] |
| 5, 17, 18 | Disintermediation | Open Food Network (open-source farmer marketplace; 1% fee; multi-country federation) | [[open-food-network]] |
| 20 | Time-bank / LETS | TimeBanks.org + hOurworld (1 hour = 1 Time Dollar; $300–1,200/yr member savings) | [[time-banks-lets]] |
| 26 | Consumer union with war chest | NOYB (4,400+ members, Schrems I+II CJEU wins, €50M Google fine, €5M Spotify fine) | [[noyb]] |
| 26 (variant) | Algorithmic-accountability watchdog | AlgorithmWatch (Berlin/Zurich, 2016–, fellowships + research + policy advocacy) | [[algorithmwatch]] |
| 29 | CCA-equivalent default opt-out | OregonSaves + CalSavers (state auto-IRA; 30-day opt-out; 5% default contribution) | [[auto-enrollment-opt-out]] |

Research-needed flags on the main table above remain accurate — the new working-implementation pages are *case* evidence that the mechanism runs in the real world, not a replacement for the per-lever implementation research still needed for a pricing-domain build.

---

## Lever descriptions

Full write-ups below. Categories A–H parallel the summary table.

### A. Aggregation

#### 1. Many-consumer counterbalance (informational + pricing)

The direct inverse of [[rental-housing-algorithmic-pricing|RealPage-class]] seller-side data pooling. Two governance forms documented on the reference layer:

- **Data cooperative** ([[data-cooperatives]]) — members pool data under democratic governance, seven ICA principles apply. Precedents: [[midata]] (Swiss health; open-source Open MIDATA Server GPLv3); [[drivers-seat-cooperative]] (US driver-owned, sunset); [[coopcycle]] (federation pattern).
- **Trusted data intermediary (CBI)** ([[collective-bargaining-for-data]]) — Vincent/Prewitt/Li 2025 proposal: bargaining-mandate intermediary representing a class of consumers in negotiations with AI / pricing-algorithm operators.

Failure modes documented on the reference layer: uptake (Ada Lovelace 2021's resonance/mobilisation/trust/capacity on [[data-cooperatives]]); [[consumer-collective-bargaining|GPO-style admin-fee incentive-incompatibility]] if funded by sellers; [[paypal-honey|extractive drift]] if funded by affiliate commissions.

**Tech surface:** membership platform + data ingestion pipeline + fair-price inference + member notification. Legal vehicles: Colorado LCA in US; UK CBS Act 2014.

#### 4. Account-leveraging to access lower-price accounts

Hannak 2014 on [[transparency-tools]] showed membership accounts on Cheaptickets/Orbitz unlocked lower hotel prices; [[consumer-collective-bargaining|Tuángòu / Pinduoduo]] is the structural pattern at scale (teams of ≥5 unlock lower prices via group-buy, embedded in WeChat social graph).

Key sub-levers:
- **Group-buy coordinator** (Tuángòu pattern) — must be embedded in a standing social graph per the [[consumer-collective-bargaining|Pinduoduo-vs-Groupon observation]] that standalone daily-deal platforms collapsed while WeChat-integrated group-buy scaled.
- **Account-pool coordinator** — shared purchasing agent routes transactions through the best-priced account per seller.
- **Demographic-optimised signup** — coordinate mass signups that trigger segment-specific pricing treatment.

**ToS friction:** many commercial sellers prohibit account sharing; the legal surface is non-trivial but per user intent this page does not disqualify on that basis.

### B. Collective redirection

Reference anchor: [[regulatory-responses|Section 7]] (artist-refusal / Wendy's walkback / Uber surge-cap as reputational levers); [[park-slope-food-coop|PSFC's 5-decade boycott history]] (anti-apartheid, Nestlé, Coca-Cola since 2004, Flaum since 2010) as live proof the mechanism works at 17K-member scale.

#### 2. Pooled info for collective redirection ("overcharge detected → redirect")

Real-time extension of the standing-boycott pattern. Continuous observation + classifier + alternative-vendor directory + per-transaction routing. Detection half is [[regulatory-responses|design-input #1]] (pricing observatory, [[markup-citizen-browser]] + [[transparency-tools|Hannak 2014]] architecture); routing half is novel.

#### 12. Flash-redirection observatory

Concretely: observatory consumes per-retailer pricing data, classifies "overcharge" on thresholds, emits a real-time signal that a browser extension surfaces inline as "this retailer is currently overcharging by X% — try Y". Redirect-latency and false-positive rate are empirically unknown — **Research needed** on both.

#### 13. Buy-cott coordinator (inverse of boycott)

Channels collective demand **to** sellers meeting stated criteria — no dynamic pricing, published algorithm, cooperative ownership. [[park-slope-food-coop]] implicitly does this at its wholesale layer; no consumer-facing tool captured.

#### 14. Demand-strike coordinator

Temporary collective purchase abstention. Porat 2024 ([[collective-bargaining-for-data]]) showed individual strategic abstention induces price cuts; coordinated collective abstention should produce larger and faster effects. Binding constraint: credible-commitment device. **Research needed** on commitment-mechanism design.

#### 15. Price-violation bounty

Crowd-funded rewards for consumers who submit specific-extraction evidence. Extends [[open-tenant-screening|OpenTSS's "Donate Tenant Screening Report"]] pattern into a paid-contribution model. OpenTSS is close enough as a template — **No further research needed** beyond what's already on the reference layer.

#### 16. Threshold-triggered flash campaigns

Kickstarter-style conditional commitment: "I'll boycott / switch carriers / abstain from Amazon IFF N others also commit." Solves the credible-commitment problem by making individual action contingent on collective threshold. *(editorial — no wiki precedent)*

### C. Profile / algorithm manipulation

Reference anchors: [[obfuscation]] (mechanism + strengths/weaknesses/countermeasures), [[adversarial-data-poisoning]] (attack taxonomy + Algorithmic Collective Action formalism), [[browser-fingerprinting]] (fingerprinting technique stack + inconsistency-detection countermeasures), [[pricing-algorithm-taxonomy]] (which pricing algorithm families actually consume per-user signals vs which don't), [[collective-bargaining-for-data|Porat 2024]] (individual-level strategic abstention + cookie-law + erasure-right exercise). Strategic syntheses: [[obfuscation-strategic-readout]] (on obfuscation specifically); [[data-disruption-strategy-map]] (which lever × which algorithm family × platform-enforcement risk, added 2026-04-23). The 2026-04-23 obfuscation-deep-dive and seller-algorithm-taxonomy research runs closed most of the research gap flagged in the original version of this section; flags below now distinguish "formalism exists, engineering is the gap" from "still speculative."

**Critical structural correction surfaced by [[pricing-algorithm-taxonomy|the 2026-04-23 algorithm-family taxonomy]]:** Not all pricing algorithms consume per-user features. Airline revenue management (Williams 2018) and neural retail demand estimation (Safonov 2024) both operate on *aggregate* signals — capacity state + booking curve for airlines, product embeddings + sales-history aggregates for retail. Identity-based levers (6, 7, 11) are **structurally ineffective** against these families. Behavioural-coordination levers (9, 14, 16) and DSAR-based levers (new — not yet a numbered lever here, see [[data-disruption-strategy-map|L3]]) apply broadly.

#### 3. Profile manipulation (user-articulated)

Umbrella: use pooled consumer behaviour to corrupt, confuse, or bypass the pricing algorithm's user-WTP inference. Sub-levers below (6–11) implement specific tactics.

#### 6. Session-identity rotation-as-a-service

Automates Porat's pattern at per-session granularity. Every retailer visit = fresh fingerprint, new cookie jar, plausible demographic signal. Tech: browser extension + identity-pool backend. **Research-backed design constraint (not "research needed"):** [[browser-fingerprinting|FP-Inconsistent (Venugopalan et al. 2024)]] demonstrates naive per-attribute rotation is detectable at ~97% TNR via cross-attribute inconsistencies. Builder must implement **joint-distribution-preserving spoofing** (rotate entire real-world device-configuration tuples, not individual attributes), per Brave's partial counterexample. Open engineering question: per-retailer-bounded rotation so user convenience on non-pricing sites is preserved.

#### 7. Demographic spoofing to the cheapest-segment treatment

Hannak 2014 on [[transparency-tools]] showed specific demographic signals trigger lower prices (Cheaptickets/Orbitz members-only; Home Depot/Travelocity mobile-device users). A tool that always presents as the cheapest-segment fingerprint per retailer captures that differential. **Research needed:** per-retailer favourable-segment mapping. [[markup-citizen-browser|Markup-style crowdsourced audit infrastructure]] is the likely methodology.

#### 8. Coordinated probe-and-publish

Inverse of Hannak 2014: many consumers run systematic probes with varied profiles; central publisher infers the pricing function per retailer per category and publishes it. Output: the algorithm's behaviour becomes public goods. Methodology well-documented on [[transparency-tools]] — **No further research needed**.

#### 9. Collective training-data withdrawal

Consumers coordinate GDPR erasure + CCPA deletion + cookie revocation in large batches timed to specific retailers. Forces pricing models to retrain on a shrinking dataset. Reference-layer mirror: [[rental-housing-algorithmic-pricing|RealPage settlement's ban on training on active lease data]] — regulator-imposed; this is consumer-side. **Research needed** on batch-erasure legal mechanics across jurisdictions.

#### 10. Adversarial training-data injection

More aggressive: systematic submission of shaped noise behaviour (browsing, carting, abandoning) specifically designed to degrade the pricing model's feature importance. **Formalism now exists** — [[adversarial-data-poisoning|Solanki et al. 2025]] provides a rigorous Algorithmic Collective Action framework (feature-label strategy *h(x, y) = (g(x), y**)*) with empirical validation. [[adversarial-data-poisoning|Wang et al. 2024]] catalogues the specific attack-technique taxonomy. **Engineering gap:** adapting supervised-learning ACA to the online-learning / bandit setting real pricing models use. **Live political risk:** [[obfuscation|Solanki et al.'s DP-as-firm-counter finding]] — a pricing operator adopting differential privacy neutralises ACA (DP noise scale σ is inversely proportional to collective success). **Legal surface:** [[obfuscation|post-Van Buren / hiQ CFAA doctrine]] makes public-endpoint automation federally defensible; authenticated-endpoint automation remains materially risky.

#### 11. Fingerprint parity network

Every member of the network gets the same apparent fingerprint (rotating pool). Retailer's personalisation layer cannot distinguish individual-WTP from the common pool, forcing fallback to category-average pricing. *(editorial — extends Porat.)* **Research needed** on technical tractability against modern bot-detection stacks. Conceptually aligned with Tor Browser's uniformity approach (see [[browser-fingerprinting]]); the open question is whether the parity fingerprint can be large enough to blend with organic traffic without being singled out as an unusually-shared signature.

### D. Account arbitrage

See lever 4 above (consolidated with account-leveraging).

### E. Disintermediation

Reference anchor: [[platform-cooperatives]] (the exit lane). Live examples [[drivers-cooperative]], [[coopcycle]] (72 bike-delivery coops across 12 countries), [[mondragon]] (70K-worker foundational precursor). **Retail / grocery disintermediation is a reference-layer gap** — farmers markets, CSAs, food hubs not on the wiki.

#### 5. Direct-to-producer (user-articulated)

Umbrella: route transactions around platform middlemen to direct producer-consumer relationships. Sub-levers 17–21 implement specific patterns.

#### 17. CSA-at-metro-scale

Long-term consumer purchase commitments matched to regional producer capacity. Federation-first architecture per [[coopcycle]]. Cuts the supermarket / delivery-platform broker entirely. **Research needed** — CSA / food-hub mechanism page missing from reference layer.

#### 18. Direct-marketplace federation

Multi-sector version of CSA. Federation of member-owned marketplaces per category (food, clothing, electronics repair, home services) on a shared cooperative shell. **Research needed** on cross-sector federation architecture.

#### 19. Producer-coop × consumer-coop matching

[[platform-cooperatives|Platform coop]] on the supply side matched with [[data-cooperatives|data coop]] on the demand side. Neither extracts; platform redistributes transaction volume on cooperative-to-cooperative terms. **Research needed** — no live example captured; need to research viable governance split between two cooperative layers.

#### 20. Time-bank / LETS (Local Exchange Trading System)

Labour-hours or category-credits exchanged directly — sidesteps monetary pricing layer entirely. Established in cooperative-movement literature but not on the reference layer. **Research needed** — time-bank / LETS mechanism page is missing.

#### 21. Repair-and-reuse federation

Every unit repaired/reused is one unit not purchased at broker-inflated price. Adjacent to the right-to-repair movement, which is a Priority-3 research-queue item per `research-queue.md`. **Research needed** — awaiting the right-to-repair research run.

### F. Information layer

Reference anchor: [[transparency-tools]] (the anchor mechanism page) plus its three sub-categories — single-seller price-history trackers ([[keepa]]), review-authenticity analysers ([[fakespot]]), crowdsourced audit observatories ([[markup-citizen-browser]]).

#### 22. Price-transparency overlay extension

Browser extension injects at purchase time: "This price was $X last week", "median across retailers is $Y", "this retailer fluctuates N×/week", "known to personalise". Direct extension of [[keepa]] pattern to cross-seller + dynamic-pricing-flagged. Reference-layer material is complete — **No further research needed** beyond integration design.

#### 23. Dynamic-pricing badge-of-shame

Public visible "DYNAMIC PRICING" mark on every retailer-category confirmed to personalise. Reputational lever; per [[regulatory-responses|Section 7]] on the reference layer, public visibility alone shifts behaviour (Wendy's AI-pricing walkback is the documented case). **Research needed** on scoring methodology and grading criteria (Fakespot's A–F grading is the template — see [[fakespot]]).

#### 24. Pricing-algorithm transparency score

Composite scorecard: does the retailer publish its pricing algorithm? Use personalised inputs? Price-change frequency? Graded like [[fakespot|Fakespot's A–F]] review-authenticity grade. **Research needed** on criteria weighting + update cadence.

#### 25. Algorithm-reverse-engineering competition

Open bounty for teams submitting the most accurate inferred pricing function per retailer. Competitive extension of Hannak 2014 methodology on [[transparency-tools]]. **Research needed** on bounty economics + judging rubric.

### G. Economic-structural

Standing institutions with durable capital and governance — shift power persistently rather than per-transaction.

#### 26. Consumer union with dues + war chest

Standing membership organisation funded by dues; spends on class-action financing, alternative-platform seed capital, lobbying, bounty pools. Closest documented precedent on the reference layer: [[consumer-collective-bargaining|healthcare GPOs]] (but in reverse — funded by members, not suppliers) and [[rei]] (partial; member-rewards but not pooled war chest). **Research needed** on legal form, revenue model, and size-to-effectiveness threshold.

#### 27. Switching-cost observatory

Many extractive patterns survive because switching is expensive. Per-category switching-cost estimator + automated switch tool (account closure, contract termination, number-porting equivalent for other services). *(editorial — no wiki precedent.)* **Research needed** on full mechanism design.

#### 28. Mass-signup threshold coordination

Inverse of [[community-choice-aggregation|CCA opt-out default]]: coordinate mass opt-in moments that change the default for all participants simultaneously. E.g., 100,000 simultaneous carrier switches at a pre-announced time. **Research needed** on credible-commitment and signalling design.

### H. Regulatory-proxy

Leverage existing law / statute rather than pushing for new legislation.

#### 29. CCA-equivalent default opt-out port to other sectors

[[community-choice-aggregation|CCA]] authorises opt-out default aggregation only for electricity in 9 US states. Per the reference-layer gap analysis on [[regulatory-responses]], no comparable opt-out default exists for broadband, insurance, pharmaceuticals, or data-privacy. Look for equivalent statutory constructs already in force and leverage existing authority. **Research needed** on statutory-mapping across these sectors.

---

## Next-step development plan

Levers are not a roadmap. A roadmap picks a lever, names the target extraction pattern it addresses, and specifies milestones. The `wiki/strategies/development-plans/` subdirectory is the home for those documents. First candidates based on the table:

- **Plan A: Flash-redirection observatory for rental housing** — combines lever #12 (flash-redirection observatory) with lever #15 (price-violation bounty). Targets [[rental-housing-algorithmic-pricing|RealPage-class coordination]] at the metro level. Feeds the court-appointed monitor per the late-2025 settlement. Adjacent to [[regulatory-responses|design-input #6]].
- **Plan B: Buyer-side data cooperative for personalised e-commerce** — lever #1 (many-consumer counterbalance) implemented as a [[data-cooperatives|data coop]] with a [[collective-bargaining-for-data|CBI]] bargaining mandate. Targets [[surveillance-pricing-retail|surveillance pricing]] and [[consumer-facing-dynamic-pricing|e-commerce personalisation]].
- **Plan C: Pricing-transparency-overlay extension** — lever #22. Lowest-dependency build; extends [[keepa]] pattern. Ships visible consumer value on day one.
- **Plan D: Consumer-side CCA-port research** — lever #29. Research-first effort to map existing statutory constructs. Pre-build stage.

Specific plan documents to follow — these are placeholders, not commitments, until the user picks one to advance.

## Source

Reference-layer anchors cited inline throughout. Levers marked *(editorial)* are design synthesis with no captured primary source — they are proposals, not documented practice. Levers with "**Research needed**" in the summary table are flagged for a future `/research` run before being committed to a development plan.

Foundational reference-layer pages this entry is built from:

- [[regulatory-responses]] — consolidated counter-power landscape and design-input catalogue
- [[transparency-tools]], [[data-cooperatives]], [[collective-bargaining-for-data]], [[consumer-collective-bargaining]], [[community-choice-aggregation]], [[platform-cooperatives]] — mechanism anchor pages
- [[dynamic-pricing-overview]] — disambiguation between dynamic / personalised / surveillance / algorithmic pricing

## Related

- [[dynamic-pricing-overview]]
- [[regulatory-responses]]
- [[transparency-tools]]
- [[data-cooperatives]]
- [[collective-bargaining-for-data]]
- [[consumer-collective-bargaining]]
- [[platform-cooperatives]]
