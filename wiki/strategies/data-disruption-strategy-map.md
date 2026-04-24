# Data-Disruption Strategy Map — 2026-04-23

*(editorial / synthesis. All evidence is cited to reference-layer pages with captured primary sources. The strategy matrix and platform-enforcement-risk column are my assessments, not direct source extraction.)*

Strategic readout on: **which data-disruption levers are effective against which seller-side pricing algorithms, and what platform-enforcement risk each lever carries.** Produced in direct response to the user's 2026-04-23 brief on seller-algorithm taxonomy and data manipulation strategies.

**Reference-layer anchors:**
- [[pricing-algorithm-taxonomy]] — algorithm-family × data-input catalogue. The reference base for this readout.
- [[obfuscation]] — strengths / weaknesses / technical approaches for per-user obfuscation.
- [[browser-fingerprinting]] — fingerprinting arms race.
- [[adversarial-data-poisoning]] — ACA formalism; DP-as-firm-counter.
- [[obfuscation-strategic-readout]] — prior readout specifically on obfuscation strategy.
- [[possible-strategic-levers]] — the 29-lever inventory.
- [[regulatory-responses]] §5a — CFAA post–Van Buren / hiQ legal surface for consumer automation.

---

## TL;DR

1. **Algorithm family determines which levers work.** Levers that target individual-identity signals ([[obfuscation|session rotation]], [[browser-fingerprinting|fingerprint parity]]) are *structurally ineffective* against airline-RM-class algorithms that don't use individual features. Population-aggregate disruption (coordinated timing) is required there. Applying the wrong lever to the wrong family is waste.
2. **The lowest-enforcement-risk lever is the one the consumer already has: their own behaviour.** Coordinated purchase-timing, coordinated non-click, coordinated stockout, and coordinated label-flipping (ACA feature-label strategy) all use the consumer's actual first-party behaviour — no automation, no ToS violation, no CFAA risk. These are under-leveraged compared to extension-based obfuscation.
3. **The highest-leverage-per-user lever is data-subject-access-request (DSAR / GDPR / CCPA).** The Uber audit demonstrated a 258-driver DSAR coordination uncovered pay-predictability collapse at R²=−54. The legal right exists; the coordination infrastructure is the gap.
4. **Three algorithm families are structurally outside consumer-side disruption.** RealPage (hub-and-spoke inter-firm coordination), airline-RM-individual-only levers (needs collective timing), and third-party data-broker feeds (sits behind intermediaries) all require non-consumer-direct action — antitrust, coordination platform, or broker-opt-out orchestration. Know which game you're in.
5. **Post–Van Buren CFAA gives cover to public-endpoint automation but not authenticated-endpoint automation.** Which side the pricing signal lives on matters for legal risk. Airline RM is authenticated; retail browsing is mostly public. Uber is authenticated on both sides.
6. **Expect DP-as-firm-counter to appear.** The Solanki et al. 2025 and Zhao et al. 2024 results both prove that pricing operators training under differential privacy simultaneously protect individual privacy *and* suppress collective data manipulation. A pricing operator adopting DP publicly is a defensive move against ACA, not just a privacy-protection move. No tool-level mitigation.

---

## The strategy matrix

Each row: one algorithm family from [[pricing-algorithm-taxonomy]]. Each column: a data-disruption lever. Cell values: effectiveness assessment with reasoning.

| | **L1. Obfuscation / session rotation** | **L2. Coordinated behaviour (timing/labels)** | **L3. DSAR / erasure bursts** | **L4. Coordinated probe-and-publish** | **L5. Platform-enforcement risk of combined deployment** |
|---|---|---|---|---|---|
| **Family 1 — GLM / contextual bandit** (personalized e-commerce) | **High** — per-user context vector is *the* input; obfuscation directly corrupts it. | High — feature-label strategy from Solanki et al. applies directly. | Medium — GDPR/CCPA deletion shrinks training corpus but live inference is session-local. | Medium — publishes the algorithm's behaviour but doesn't disrupt it. | Medium. Public-endpoint mostly safe; authenticated-endpoint automation is CFAA surface. |
| **Family 2 — Neural demand estimation** (retail) | Low — model uses *aggregate* features. Individual session rotation is noise, not signal. | **High** — on-shelf availability and sales-history aggregates are load-bearing; coordinated purchase-timing or coordinated stockout triggers corrupt both. | Low — model is trained on aggregate sales, not identifiable consumer records. | Medium — exposes pricing behaviour to consumers. | Low-medium. Behaviour-based levers are ToS-clean; stockout coordination has more friction. |
| **Family 3 — Retail offer bandit** (per-user offers) | **High** — MPG / brand-loyalty / seasonality context is per-user. Obfuscation degrades it. | **High** — SGD update is `w ← w + η(y − σ(wᵀx))x`; coordinated click/no-click inverts the gradient. | Medium — similar to Family 1. | Medium. | Medium — similar to Family 1. |
| **Family 4 — Airline RM / stochastic DP** | **Ineffective** — the algorithm does not use individual identity. Rotating sessions does nothing. | **High (only at population scale)** — coordinated purchase-timing within a fare-class booking window shifts the realized demand curve. | Ineffective — no individual training-record to erase. | Medium — booking-curve publication useful for consumer-timing coordination. | Low at population-timing level (pure consumer choice); automated booking is CFAA surface. |
| **Family 5 — RealPage hub-and-spoke** | Ineffective — no per-consumer feature vector. | Ineffective — pricing is inter-firm, not per-consumer. | Ineffective — training data comes from landlords, not tenants (though tenant-facing data flows exist). | High — the Yale TAP paper's argument is that exposing the joint-owner optimization is the remedial lever. See [[rental-housing-algorithmic-pricing]]. | Not a consumer-side fight. Antitrust / DOJ remedy ([[regulatory-responses|§1]]) is the relevant lever class. |
| **Family 6 — Uber per-trip** | Partial — passenger-side session rotation disrupts per-trip passenger features; driver side is fixed by account. | **High (driver side)** — coordinated acceptance-rate manipulation shifts the acceptance-history feature. | **Highest-leverage lever** — DSAR/GDPR exposed the algorithm's predictability collapse at R²=−54. Legal right already exists. | High — the participatory-audit methodology is itself the disruption mechanism. | Low for DSAR (statutory right); low for driver-collective behaviour; authenticated-endpoint automation is still higher-risk. |

Reading the matrix: effective leverage sits on the **diagonal** (matching lever class to algorithm class) and on column L2 (coordinated behaviour, which works broadly). L1 (obfuscation) is *narrowly* effective — only Families 1, 3, and partially 6. This reframes [[obfuscation-strategic-readout|the earlier obfuscation readout]]: obfuscation is the right lever for *some* algorithm families, not a universal lever.

---

## Disruption levers — what each one actually is, with source anchor

### L1. Obfuscation / session rotation

Client-side browser-extension or automation that cycles the user's apparent identity per visit. Reference: [[obfuscation]], [[browser-fingerprinting]]. Strengths, weaknesses, and countermeasures documented in [[obfuscation-strategic-readout]].

**Key constraint confirmed by [[pricing-algorithm-taxonomy|new evidence]]:** the lever is only effective against algorithms that consume per-user feature vectors. Zhao et al. 2024's LDP regret inflation result (`d/ε²` effective-sample-size shrinkage) quantifies the disruption the obfuscation floor achieves against Family 1 — at ε=1, d=10, an obfuscated consumer population imposes a 10× sample-size penalty on the seller's GLM fitting.

Zero effect on Families 2, 4, 5.

### L2. Coordinated behaviour (timing, labels, click, stockout)

The **consumer's own actual behaviour**, coordinated across a collective. No automation, no identity spoofing, no tool. Just collective decisions about *when* to buy, *whether* to click, *what* to stock up on. Reference: [[adversarial-data-poisoning]] (ACA formalism from Solanki et al. 2025 — feature-label strategy `h(x, y) = (g(x), y*)`).

**This is the under-leveraged lever.** It works across Families 1–4 and 6. It carries **the lowest platform-enforcement risk** because it is literally just consumer choice. Critical mass: Solanki et al.'s empirical results on CIFAR-10 / MNIST / Bank Marketing suggest 1–10% of training-contributing users is enough to force target-label associations. For pricing models, this translates to 1–10% of a retailer's active customers.

Implementation architecture open questions:
- **Commitment device.** How does a collective credibly commit to, say, coordinated non-purchase-for-2-weeks? The [[possible-strategic-levers|lever #14 (demand-strike coordinator)]] and [[possible-strategic-levers|lever #16 (threshold-triggered flash campaigns)]] address this.
- **Target selection.** Which specific behavioural trigger *g* and target label *y** produce the strongest effect per family? Open research.
- **Rotation of triggers.** Once the seller detects one trigger, they will filter it. Rotation strategy is an arms-race constraint.

### L3. DSAR / GDPR Article 15/20 / CCPA deletion

Exercising existing statutory rights to get your data from the seller (Art. 15 access; Art. 20 portability) or force its deletion (CCPA). Reference: [[collective-bargaining-for-data|Porat 2024's individual algorithmic bargaining]]; [[pricing-algorithm-taxonomy|Uber audit methodology]].

**The Uber audit is the existence-proof at scale.** 258 drivers submitted DSARs. 1.5M trips of data returned. Automated pipeline processed 40–45 files per driver (~35 CSVs each). The audit discovered:
- Predictability collapse R²=0.85 → R²=−54 post-dynamic
- Median take-rate rise 25% → 29%
- Inequality divergence
- Information-asymmetry structure documented

This is **higher information yield per user than obfuscation delivers** at any documented scale. And the legal right is in force — no ToS breach, no CFAA risk, just statutory exercise.

**The missing infrastructure:** a DSAR-coordination platform that (a) templates the request per retailer/platform, (b) collects the responses from users, (c) pseudonymises, (d) aggregates into a public audit. The WIE pipeline is the closest existing example ([github.com/OxfordHCC/FAccT_25_Not_Even](https://github.com/OxfordHCC/FAccT_25_Not_Even)). Extending it to pricing-retailer DSARs is a concrete build opportunity. See [[possible-strategic-levers|lever #9 (collective training-data withdrawal)]] — this upgrades the lever from "research needed" to "build target."

### L4. Coordinated probe-and-publish

Many consumers run systematic probes under varied profiles; a central publisher infers the pricing function per retailer and publishes it. Reference: [[transparency-tools]] (Hannak 2014 methodology); [[markup-citizen-browser]] (deployed example). [[possible-strategic-levers|Lever #8]].

**Per [[pricing-algorithm-taxonomy|the taxonomy]], this lever works differently per family:**
- Family 1, 3: recovers the per-user price function — useful for consumer decision tools.
- Family 4: recovers the booking-curve dynamics — useful for timing coordination.
- Family 5: the Yale TAP argument *is* probe-and-publish at the inter-firm layer. Antitrust evidentiary output.
- Family 6: the participatory-audit methodology directly.

Enforcement risk: low-to-medium. Public-endpoint probing is CFAA-safe post-Van Buren ([[regulatory-responses|§5a]]). Authenticated-endpoint probing is a CFAA "gates up" surface — risk is materially higher.

### L5. Third-party data-broker opt-out orchestration

Intermediary brokers (Acxiom, Experian, Epsilon) sell consumer profiles to sellers as input to pricing algorithms. Consumer-side disruption: exercise broker-side opt-out rights at scale. GDPR Art. 21 objection, CCPA deletion, state broker-registry opt-outs.

**Not captured by this run's sources.** A separate research run is warranted on broker-side data flows and the rate-limiting/friction of consumer opt-outs. Flagged for [[research-queue]].

### L6. Antitrust / structural remedy (not consumer-direct)

For Family 5 (RealPage hub-and-spoke) and any other family where harm comes from inter-firm data coordination rather than per-consumer profiling. Reference: [[regulatory-responses]], [[rental-housing-algorithmic-pricing]], the Yale TAP 2025 remedial argument.

Consumer-side input is political: case support, ProPublica-style investigative journalism, tenant/consumer class action. The lever class is real but lives outside the data-disruption category proper.

---

## Platform-enforcement risk catalogue

Ordered low-to-high. For each risk class, documents the existing precedent and the consumer-side mitigation.

| Risk class | Example | Enforcement mechanism | Mitigation |
|---|---|---|---|
| **1. Pure consumer choice** (L2 timing, L2 labels, L3 DSAR) | User chooses not to click, not to purchase, to purchase on a different day; user files a GDPR request | None — this is lawful behaviour | No mitigation needed |
| **2. Public-endpoint automation (post-Van Buren)** | [[transparency-tools|Keepa-style overlays]], [[markup-citizen-browser|Markup's probe stack]] | ToS breach; breach-of-contract claim possible but not CFAA | Institutional cover (hosted by EFF / academic partner); design for Firefox + direct-download ([[lever-implementation-readout|H2]]) |
| **3. Authenticated-endpoint automation** | Automating actions inside logged-in views (loyalty portals, cart operations, coupon auto-apply) | CFAA "gates up" surface; access-without-authorization claim plausible | Minimise — prefer unauthenticated signal where possible. Where required, use authenticated account owned by the user, not a pool account. |
| **4. Platform-distribution ban** | [[adnauseam|AdNauseam Chrome Web Store 2017]], [[paypal-honey|Chrome affiliate-policy change March 2025]] | Platform-policy enforcement, not legal action | Multi-browser from launch; direct-download channel; [[privacy-badger\|EFF-hosted alternative]] as template |
| **5. Adversarial-training inoculation** | Pricing operator trains model against known consumer obfuscation tool signatures | ML-engineering, not legal | Tool signature rotation; open-source; multi-tool ecosystem so adversary can't train against one signature |
| **6. DP-trained pricing model** | Seller adopts ε-LDP training, publicly framed as privacy protection | Neither legal nor technical — it is a *structural* suppression of collective-action leverage | **No tool-level mitigation.** Policy response: pre-emptive naming of "DP-trained pricing as ACA-suppression" (see [[obfuscation-strategic-readout|open strategic questions]]) |

The critical observation: **levers L2 and L3 land in risk class 1** (pure consumer choice). They carry no platform-enforcement risk at all. Every other lever sits higher up the risk ladder. This argues strongly for prioritising L2 and L3 before obfuscation-type tools.

---

## Recommended strategy portfolio

*(editorial — this is my portfolio recommendation given the evidence. Subject to user redirection.)*

Rank-ordered by leverage × feasibility × enforcement-safety:

### Tier 1 — Build now

1. **DSAR-coordination infrastructure for retail and rideshare.** The WIE Uber audit is the existence-proof. Build a DSAR-templating, response-collection, and aggregation platform for Family 1, 3, and 6 targets. Lever L3. Platform-enforcement risk class 1.
2. **Collective-timing / demand-strike coordinator for Family 2 and Family 4.** A credible-commitment app where users commit to coordinated purchase-delay or category-level stockout on specific targeted SKUs or routes. Lever L2. Platform-enforcement risk class 1. See [[possible-strategic-levers|lever #14, #16]].
3. **Public-endpoint probe-and-publish observatory.** Extend the [[markup-citizen-browser|Markup Citizen Browser]] model to pricing targets in Families 1–4. Lever L4. Risk class 2.

### Tier 2 — Build with care

4. **Per-user-behaviour obfuscation extension with joint-distribution fingerprint spoofing.** Only effective against Families 1, 3, and partially 6. Requires the engineering discipline documented in [[obfuscation-strategic-readout|the obfuscation readout]]. Risk class 2–4 depending on distribution.
5. **Feature-label ACA tool for contextual-bandit / retail-offer targets.** Solanki et al. formalism applied to Families 1 and 3 specifically. Open research on the online-learning / bandit adaptation. Risk class 1 (it's the consumer's own labels) to 3 (if automated via tool).

### Tier 3 — Long-game / political

6. **Pre-emptive political framing of DP-trained pricing as ACA-suppression.** No tool. Position paper. [[regulatory-responses]] extension.
7. **Data-broker opt-out orchestration.** Research needed; broker-side data flows not yet on the wiki.
8. **Continued support for antitrust remedies on Family 5 / RealPage-class.** Not consumer-direct but shapes the landscape.

### Not recommended

- **Blanket obfuscation rollout as primary lever.** The taxonomy shows it doesn't work against Families 2, 4, 5. And the [[obfuscation-strategic-readout|Richards & Hartzog critique]] argues it's strategically self-defeating as a frame. Use it narrowly.
- **Authenticated-endpoint automation at scale.** CFAA risk remains post–Van Buren. Not worth the risk when L2 / L3 deliver more leverage at lower risk.

---

## Open strategic questions

1. **DSAR scaling.** Uber audit = 258 drivers. To extract comparable leverage against a major e-commerce pricing operator, what's the minimum DSAR-submitter count? Is this 1000? 10,000? Do the [[noyb|NOYB consumer-union model]] or [[algorithmwatch|AlgorithmWatch coordination infrastructure]] offer usable templates?
2. **Which Family 2 targets.** Neural demand estimation is deployed by grocery and retail pricing vendors (Revionics, PROS — the FTC 6(b) study targeted them). Which specific retailer is the concrete target for a first Tier-1 Build-Now project? The [[surveillance-pricing-retail|FTC 6(b)]] list is the obvious starting point.
3. **Timing coordination commitment device.** Is Kickstarter-style "I'll commit IFF N others commit" enough? Does it need legal commitment (prepaid deposit, enforceable contract)? [[possible-strategic-levers|Lever #16]] flags this as research-needed. Still open.
4. **Cross-family tool reuse.** Can a single browser-extension tool deliver both L1 (obfuscation) and L4 (probe-and-publish)? The [[markup-citizen-browser|Citizen Browser]] architecture already does probe-and-publish client-side; adding obfuscation mode would expand scope. Conflict: probe-and-publish wants to reveal the algorithm's behaviour, obfuscation wants to confuse it. Are these compatible in one tool?
5. **The Family-5 problem.** If hub-and-spoke structures proliferate (RealPage-style vendors for other sectors), consumer-side disruption has nothing to offer. Is there a wiki-sanctioned monitoring role — surface new RealPage-analogues early, feed to DOJ/FTC, document for [[regulatory-responses]]?

## Source

Editorial synthesis of reference-layer pages below. All substantive factual claims trace to their source pages.

- [[pricing-algorithm-taxonomy]] — algorithm family × data-input catalogue (primary reference for this readout).
- [[obfuscation]] — obfuscation strengths / weaknesses / tech / countermeasures.
- [[adversarial-data-poisoning]] — ACA formalism, DP-as-firm-counter.
- [[browser-fingerprinting]] — fingerprinting and detection.
- [[obfuscation-strategic-readout]] — prior readout specifically on obfuscation.
- [[rental-housing-algorithmic-pricing]] — RealPage / Family 5.
- [[consumer-facing-dynamic-pricing]] — Family 6 Uber empirical case.
- [[surveillance-pricing-retail]] — FTC 6(b) data-intermediary layer.
- [[collective-bargaining-for-data]] — Porat individual bargaining + CBI intermediary framework.
- [[regulatory-responses]] — §5a Van Buren / hiQ CFAA doctrine, §1 DOJ RealPage enforcement.
- [[transparency-tools]], [[markup-citizen-browser]], [[noyb]], [[algorithmwatch]] — deployment templates and institutional cover examples.
- [[possible-strategic-levers]] — the 29-lever inventory this portfolio selects from.

## Related

- [[pricing-algorithm-taxonomy]]
- [[obfuscation-strategic-readout]]
- [[lever-implementation-readout]]
- [[possible-strategic-levers]]
- [[obfuscation]]
- [[adversarial-data-poisoning]]
- [[regulatory-responses]]
- [[collective-bargaining-for-data]]
- [[data-cooperatives]]
