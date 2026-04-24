# Pricing Algorithm Taxonomy and Data-Input Catalogue

Reference-layer inventory of the main **seller-side dynamic pricing algorithm families** and the **data inputs each family requires to work**. Produced as part of the 2026-04-23 `seller-algorithm-taxonomy` research run to answer an explicit question: *what types of data do the algorithms consume, and which of those data types are accessible to consumer-side manipulation?* The strategic synthesis of what is disruptable and at what platform-enforcement cost is on [[data-disruption-strategy-map]] in the strategy layer.

This page is reference-layer. Each algorithm-family section extracts claims directly from the captured primary sources. Editorial synthesis is clearly marked *(editorial)*.

Related reference-layer pages: [[dynamic-pricing-overview]] (term disambiguation — rule-based vs dynamic vs personalised vs surveillance vs algorithmic pricing); [[algorithmic-collusion]] (Q-learning / Exp3 / deep RL in Bertrand-competition settings); [[rental-housing-algorithmic-pricing]] (RealPage case study); [[surveillance-pricing-retail]] (FTC 6(b) on data-broker / intermediary layer).

## Algorithm family matrix

| Family | Canonical paper | Deployed example | Per-user features required? | Learning signal | Failure mode under data disruption |
|---|---|---|---|---|---|
| **GLM / contextual bandit** | Zhao et al. 2024 (arXiv 2406.02424) | E-commerce personalization stacks | **Yes — d-dim feature vector** | Demand realization × price × context gradient | Effective sample size shrinks by *d/ε²* under LDP; full-rank context matrix needed for MLE |
| **Neural demand estimation** | Safonov 2024 (arXiv 2412.00920) | Grocery / general-retail price-optimization vendors | **No individual features**; product × temporal × sales-history aggregates | Predicted vs realised unit sales | Degrades under category-wide demand shocks; requires full-rank price variation |
| **Contextual bandit (retail-offer)** | Tanković & Šajina 2025 (arXiv 2505.16918) | Retail personalized-offer engines (logistic + SGD) | **Yes — 6–7 feature context per offer** | Click event (binary reward) | Weights drift on SGD under coordinated non-click; cold-start if member features are absent |
| **Stochastic DP / RM (EMSR / fare-bucket)** | Williams 2018 (Cowles 3003U) | Airline pricing, hotel yield management | **No individual features**; capacity state + time + booking curve | Sales vs opportunity cost of capacity | Coordinated purchase-timing shifts break the booking-curve signal |
| **Hub-and-spoke pooled-data optimization** | Yale TAP 2025 | [[rental-housing-algorithmic-pricing\|RealPage YieldStar / AIRM]] | **Competitors' nonpublic transactional data** (not individual-consumer features) | Joint-owner profit objective | Structural: removing the multi-client price-recommendation function breaks it; data-only restrictions insufficient |
| **Per-trip opaque dynamic pricing** | Uber audit 2025 (arXiv 2506.15278) | [[consumer-facing-dynamic-pricing\|Uber UK post-Q1 2023]] | **Yes — trip geo × time × worker-acceptance-history × undisclosed signals** | Passenger-fare vs driver-fee split, optimized independently | Requires participatory audit / DSAR coordination; opaque by design |

*(editorial column: "Failure mode under data disruption" is my synthesis based on the paper's stated structural assumptions, not direct source extraction.)*

## Family 1 — Contextual bandit / GLM-based personalized pricing

Source: **Zhao, Jiang & Yu 2024**, *Contextual Dynamic Pricing: Algorithms, Optimality, and Local Differential Privacy Constraints* (arXiv 2406.02424). Captured `01-03-contextual-dynamic-pricing-dp.md`.

### Problem setting (quote, §2.1)

> "We consider a firm, hereafter referred to as the seller, that sells a product to T ∈ N+ sequentially arriving consumers. In each time period t ∈ [T], the seller observes contextual information featurized as a vector zₜ ∈ Rᵈ, which may include consumer personal information and product characteristics. Upon observing zₜ, the seller offers a price pₜ from a compact price interval [l, u] ⊆ R+ to the consumer and observes a demand yₜ ∈ R."

The algorithm family: Explore-Then-Commit (ETC) and upper-confidence-bound (supCB) over a generalized linear model (GLM) of demand.

### Data requirements

Per-customer context vector. The paper's real-data experiment uses **d = 5 covariates: loan amount, term, prime rate, competitor's rate, and FICO score** (§5). The internal covariate is augmented to 2d by concatenating with price-scaled features: xₜ = (zₜᵀ, −pₜzₜᵀ)ᵀ ∈ R^{2d}.

**Demand model (§2.1):** `E(yₜ | xₜ; θ*) = ψ'(zₜᵀα* − zₜᵀβ*pₜ)` where `zₜᵀα*` is the intrinsic utility and `zₜᵀβ*pₜ` is the pricing effect. The price elasticity component is `zₜᵀβ*`.

**Per-round observation:** sₜ = (zₜ, yₜ, pₜ) — raw context vector, realized demand, and price charged.

### Vulnerability under data manipulation

**Full-rank context assumption is load-bearing.** The paper's Assumption 2.1(b) requires the covariance `Σ_z = E(z₁z₁ᵀ)` to have `λ_min(Σ_z) > 0`. Under adversarial (non-i.i.d.) contexts, §2.2.2: *"the MLE θ̂_τ may not be well-defined as the design matrix V_τ can be rank-deficient."* Consumers supplying collinear, constant, or otherwise low-rank context vectors across the population collapse this condition and prevent parameter identification.

**Price elasticity assumption is also load-bearing.** Assumption 2.2: the price elasticity `zₜᵀβ*` must be lower-bounded by an absolute constant for all contexts — *"all consumers are sensitive to prices."* If revealed price responses are heterogeneous (e.g., some consumers always accept, others always refuse at any price), the gradient carrying price-sensitivity information is uninformative.

**Local Differential Privacy quantifies the disruption floor.** Theorem 3.2: the ETC-LDP regret bound is `E(R_T) ≲ ε⁻¹ d √(T log T)`. The minimax lower bound (Theorem 4.2) inflates by `√(d/ε)` relative to the non-private bound. The mechanism (§3.2): *"the LDP constraint shrinks the effective sample size from τ to τε²/d, a phenomenon repeatedly observed in the LDP literature."*

Structural implication: *(editorial)* consumer collective action that effectively imposes ε-LDP-like noise on the per-round gradient forces the seller's effective training sample size to shrink by a factor of d/ε². For a model with d=10 features at ε=1, that is a 10× sample-size penalty — potentially enough to push the seller below the floor of reliable GLM identification. This is the same structural result as [[adversarial-data-poisoning|Solanki et al. 2025]] but derived from the pricing-specific problem, not from generic ACA.

## Family 2 — Neural network demand estimation

Source: **Safonov 2024**, *Neural Network Approach to Demand Estimation and Dynamic Pricing in Retail* (arXiv 2412.00920). Captured `02-04-neural-demand-retail.md`.

### Why neural models are deployed in retail

The stated motivation (§1): *"Traditional econometric models for demand estimation often rely on significant price variation to accurately capture consumer responsiveness. However, in many real-world applications, price variation may be quite low due to pricing regulations or particular pricing policies."* The NN overcomes this by *"extracting latent patterns from item-specific characteristics and environmental variables."*

Formal demand model: `D_i(P_i, X_i, S_i)` where X_i = environmental variables, S_i = item-specific characteristics. No per-consumer feature vector appears — the model predicts **aggregate demand**, not individual-level preferences.

### Feature catalogue (§4)

| Feature category | Specific inputs (quoted) |
|---|---|
| Product attributes | Hierarchical product tree levels 1–8 passed through an embedding layer to size 64; unique item identifier; upper-category identifier |
| Customer attributes | **None** — model is aggregate, not individual |
| Temporal / seasonal | "Day of the week and the week number" |
| Price / promotion history | "Aggregated and average sales over a time window prior to the current date" with aggregations: mode, median, weighted average, std dev, CV, exponentially weighted average |
| Competitor prices | "Competitors' prices are aggregated in the same manner as the company's price and averaged across the available competitors" |
| Inventory / supply-side | "Mean value of on-shelf availability over the same time window"; "price of other goods in this category" (cross-elasticity proxy) |

### Training data volume

Empirical dataset (§4): *"a large e-commerce retailer's records on sales, prices, assortment availability collected daily over a span of 1.5 years"* across 100+ branches. Starts at 10M+ observations; filtered to ~3M *"where the price deviates by more than 5% from the average"* — most data is too price-stable to be informative. The baby food category's observed coefficient of variation on price is 0.16.

### Structural vulnerability

Two disruption-relevant features the paper identifies as load-bearing:
- **On-shelf availability.** A feature the model uses to infer supply-side conditions. Coordinated stockout triggering at selected SKUs would corrupt this signal.
- **Aggregated sales-history window.** The ~90-day rolling aggregation (mode/median/mean/std) is the demand-inference backbone. Coordinated purchase-timing shifts in the training window perturb the signal the model uses to calibrate elasticities.

Author-acknowledged weakness (§2.2): price endogeneity is *"solved only under a strong assumption of price shocks independence"* — meaning the model is already fragile to correlated demand shocks, which is exactly what coordinated consumer action produces.

## Family 3 — Contextual bandit for retail personalised offers

Source: **Tanković & Šajina 2025**, *Scalable and Interpretable Contextual Bandits: A Literature Review and Retail Offer Prototype* (arXiv 2505.16918). Captured `03-05-scalable-contextual-bandits.md`.

### Algorithm family scope

*"Contextual Multi-Armed Bandits (CMABs) provide a powerful framework for sequential decision-making under uncertainty, where an agent learns to select actions (arms) based on observed contextual information to maximize cumulative rewards over time"* (§1). Cited deployment domains: *"personalized recommendation systems for news, movies, products, online advertising, dynamic pricing, and medical treatment optimization."*

### Algorithm family sub-taxonomy (reviewed, §2)

| Algorithm | One-line definition (quoted) | Data implications |
|---|---|---|
| **LinUCB** | *"Models the expected reward E[rₜ,ₐ \| xₜ,ₐ] for arm a at time t as a linear function of its d-dimensional feature vector... adds an exploration bonus proportional to the standard deviation"* | d-dim feature vector per (arm, round); regret O~(d√T) |
| **LogisticUCB / OFUL** | *"Generalized Linear Models... designed for binary outcomes (e.g., clicks), using a logistic link function"* | Binary click/no-click labels; same d-dim context |
| **NeuralUCB / R-NeuralUCB** | *"Neural network-based UCB approaches... to capture complex non-linear context-reward relationships"* | Needs substantial training volume; poor cold-start |
| **D-LinUCB** | *"Adapts to non-stationary environments via discounted regression"* | Needs streaming input; handles drift |
| **HellingerUCB** | *"Shows promise for cold-start scenarios by using Hellinger distance in UCB construction"* | Minimal history; designed for cold-start |
| **ε-Greedy / AdaptiveGreedy** | Selects greedy action with prob 1−ε, random otherwise | Model-agnostic; no explicit confidence |
| **Thompson Sampling (LinTS, LogisticTS, PG-TS)** | *"Maintains a posterior distribution over the parameters of the reward model. In each round, the algorithm samples a parameter vector from this posterior..."* | Needs prior specification; O~(d^{3/2}√T) regret |
| **DISCO** | TS integrated with integer programming for budget constraints | Budget/constraint data |

### Retail-offer prototype details (§3)

The concrete prototype implements online logistic regression via SGD. Feature vector per (offer, member) pair, z-score normalized:
- **Member Purchase Gap (MPG)** — time since last category purchase relative to user's purchase cycle
- **Brand loyalty score** (L^m_{b,c}) — share of category purchases going to brand b
- **Seasonality score** (S_c(t)) — category purchase frequency relative to historical peak
- **Offer recency and duration**
- **Nominal discount value** (offer value)
- **Matrix factorization (MF) score** — bias term for multi-offer comparison

Reward: binary click. `P(y=1 | x; w) = σ(wᵀx)`. Update rule: `w ← w + η(y − σ(wᵀx))x` with positive-sample boost multiplier α > 1.

Exploration: Beta-distribution stochastic sampling over base predictions; κ increases over time to anneal exploration.

### Structural vulnerability

**Purchase-history features are the primary per-user inputs.** Member Purchase Gap, brand loyalty share, and category seasonality are all **derived from the user's past purchase behaviour with this seller** — they are first-party and owned by the seller, but they are *generated by* the consumer's own choices. A coordinated shift in purchase pattern directly corrupts the feature vector.

**SGD with positive-sample boost is sensitive to signed-error gradients.** The update is `w ← w + η(y − σ(wᵀx))x`. Coordinated click/no-click under treatments where the model expects the opposite generates large-magnitude gradient updates in the wrong direction. The positive-sample boost amplifies click events, making *withholding* clicks (not just adversarial clicks) a meaningful perturbation.

## Family 4 — Stochastic DP / airline revenue management

Source: **Williams 2018**, *Dynamic Airline Pricing and Seat Availability* (Cowles 3003U). Captured `07-07-williams-airline-pricing.md`. Dataset: 1,362 flights in US monopoly markets, March–September 2012; 79,856 observations.

### Algorithm family

Stochastic dynamic programming over a perishable good with fixed capacity and finite selling horizon. Three core ingredients (quoted): *"(i) a monopolist has fixed capacity and finite time to sell; (ii) the firm faces a stochastic arrival of consumers; and (iii) the mix of consumers, corresponding to business and leisure travelers, is allowed to change over time."* Two pricing forces: **intertemporal price discrimination** (consumer-type-mix shifts near departure) and **dynamic response to stochastic demand** (remaining capacity carries a rising opportunity cost).

Practically: prices drawn from a discrete fare-class set (fare buckets, e.g., "G5" = 5 seats remain in G class); algorithm opens/closes buckets rather than setting continuous prices.

### Feature / data catalogue

| Data input | Type | Quote or description |
|---|---|---|
| Capacity state (seats remaining per fare class) | First-party / owned | *"Y9 indicates that the Y class fare…has at least nine tickets available for purchase"* — monotonically decreasing |
| Time-to-departure | Temporal / structural | T=60 days; period 1 = first sales period, period T = day of departure |
| Booking history / arrival distribution | First-party / owned | Daily bookings differenced from seat maps |
| Advance-purchase-discount (APD) fences | Product-structural | Fare basis codes like "G21JN5" encode APD requirements; prices jump at 3/7/14/21-day thresholds |
| Traveler-segment mix | **Inferred, not observed** | *"Each period, the airline offers a single price to all customers"*; type-mix γ_t is a probabilistic population parameter |
| Competitor prices | Not in the model | Williams studies monopoly markets only |
| Personalization (loyalty, cookies, IP) | **Not present** | Explicit model assumption: single price per period |

### Critical finding — no individual personalization

The Williams model is explicit (§2): *"each period, the airline offers a single price to all customers."* The algorithm does not observe individual identity. Consumer type (business vs leisure) is treated as a **probabilistic population parameter**, not an individual signal. Fare-class restrictions (APDs, Saturday-stay) function as a **self-selection mechanism** forcing segment separation without requiring identification of individual travelers. No loyalty programmes, cookies, or IP-based targeting appear in the pricing mechanism.

### Structural vulnerability

The algorithm depends on **aggregate** demand signals: capacity draw-down rate and booking velocity over time. Its inputs are NOT individual consumer features.

*(editorial)* This means individual-identity-based counter-strategies — fingerprint rotation, session obfuscation, per-user decoy generation — are **structurally ineffective against airline RM**. The algorithm's signal-source is the population's collective booking velocity; the only effective disruption is coordinated timing manipulation at population scale (coordinated early-buying, coordinated mass empty-seat-leaving, coordinated purchase postponement to bin-close moments). This is a **different strategic class of lever** from individual-level obfuscation.

Williams's welfare finding is relevant: *"Average consumer welfare is 3.2% higher for leisure consumers and 5.2% lower for business consumers under dynamic pricing compared to uniform pricing. In aggregate, the surplus changes essentially cancel out. However, revenues fall 2% under uniform pricing."* Dynamic pricing here is not straightforwardly bad for consumers — the welfare case for flat pricing is weaker than the RealPage-class collusion case.

## Family 5 — Hub-and-spoke pooled-data joint optimization (RealPage / AIRM)

Source: **Yale Thurman Arnold Project 2025, Student Paper #07 on RealPage**. Captured `04-08-yale-tap-realpage.md`. Supplements the existing [[rental-housing-algorithmic-pricing]] page.

### Algorithm character

The Yale TAP paper does not name a specific ML architecture for AIRM. Operative characterization: *"AIRM generates a daily pricing recommendation for each unit, accompanied by a 'market range chart.'"*

Critically: *"The pricing algorithm takes into account that other RealPage landlords in the market will also be setting a high price recommended by RP. The result is a similar calculation to the one a joint owner of these units would make."* This is **joint-owner profit maximization across competing firms**, not independent per-landlord optimization.

### Data inputs (Yale TAP wording)

- **Client landlord's own first-party data:** occupancy rates, lease terms, rent rolls.
- **Pooled-from-competing-landlords nonpublic data:** *"competitively sensitive, real-time transactional data — including occupancy rates, lease terms, and rent rolls — collected from competing landlords through over 50,000 monthly calls surveilling over 11 million total properties."*
- **Granular depth:** *"capturing detailed lease terms and individual transactions... gives RealPage's algorithm deep insight into real-time market dynamics and competitor pricing."*
- **Seasonality forecast feature:** *"AIRM's 'market seasonality' feature exploits this transactional data to generate rent recommendations informed by forecasts of competitors' future supply."*

Public-data-only variant: LRO *"requires landlords to manually input information sourced from publicly available listings."* Same architecture, different data.

### Compliance enforcement — mechanism for algorithm-dependency

*"RealPage earned a 90% approval rate on its price recommendations."* Override requires *"detailed 'specific business commentary' justifying the deviation,"* reviewed by a RealPage *"pricing advisor"* who *"actively pressure[s] property managers to accept AIRM's price recommendations."*

### Disruption mechanism the TAP paper actually argues

The paper explicitly rejects a simple "data moat" thesis. Authors' core argument:

> "The anticompetitive core of the scheme is not tethered to the nature of the data but to the centralization of pricing power. The essential economic harm arises from the fact that competing firms are outsourcing a critical competitive function — price-setting — to a common intermediary whose purpose is to maximize profits collectively rather than independently."

They acknowledge the data matters but disclaim it as the mechanism of harm: *"granular information may improve the algorithm's accuracy in setting sustainable collusive prices towards monopoly levels, but it is not essential to the structure of coordination."*

Remedy the authors propose: *"RealPage should be barred from making specific, tailored price recommendations to more than one competitor."* Data-stripping alone (e.g., the DOJ's Cortland remedy) would *not* break the system because LRO — the public-data-only variant — retains the same collusive architecture.

### Structural vulnerability

*(editorial)* Consumer-side data-disruption levers (information asymmetry counter-weights) do not reach this algorithm's core failure mode. The harm comes from **inter-firm coordination via a shared hub**, not from per-consumer profiling. Breaking the hub-and-spoke structure requires antitrust/regulatory action at the inter-firm layer, not consumer-side data manipulation. This is the opposite of the contextual-bandit family, where consumer-side counter-action is directly applicable.

## Family 6 — Per-trip opaque dynamic pricing (Uber)

Source: **"Not Even Nice Work If You Can Get It: A Longitudinal Study of Uber's Algorithmic Pay and Pricing"** (arXiv 2506.15278, FAccT 2025). Participatory audit: **1.5M trips from 258 UK drivers**, 2016–2024. Captured `08-09-uber-algorithmic-pay-audit.md`.

### What changed in Q1 2023

Pre-dynamic (quote): *"Fares were a simple function of time and distance, with Uber taking a fixed percentage of the passenger's fare, first 20% and then later raised to 25%."*

Post-dynamic: *"Fares are no longer a simple function of time and distance. Instead the price the passenger pays and the fee the driver receives vary independently of each other, and are calculated dynamically based on location of pick up and drop off, time of day / week / year, probability of driver / passenger cancellation, and other factors undisclosed by Uber. This means that Uber's take rate (the percentage they keep) is no longer stable but varies trip-by-trip."*

### Data inputs (confirmed / inferred)

| Input | Evidence |
|---|---|
| Pickup and drop-off location | Directly stated |
| Time of day/week/year | Directly stated |
| Probability of driver/passenger cancellation | Directly stated |
| Trip duration/distance | From pre-dynamic continuity |
| Driver acceptance-rate history | *"It's indirectly forcing the driver to accept; the natural instinct is 'oh I'm not getting any dispatches, is it because I just rejected two just now?'"* (driver quote). Audit finding: drivers with higher post-dynamic pay "skew further right" in acceptance rates |
| Per-driver behavioral point estimates | CEO investor-call statement: *"point estimates for every single trip based on the driver... targeting of different trips to different drivers based on their preferences or based on behavioral patterns that they're showing us"* |
| "Other factors undisclosed" | Stated explicitly as undisclosed |
| Driver profile / scores (schema evidence) | DSAR responses contain 40–45 files (~35 CSVs) including driver profiles, scores, identifiers |

### Measured behavioural shifts (quantitative)

- **Pay.** Continuous-data 114-driver panel: average inflation-adjusted pay £18.52/hr → £17.07/hr. 93 of 114 worse off.
- **Take rate.** Median 25% → 29%. *"On some trips the take rate is over 50%."* Only 46% of drivers maintain take rate ≥75% of fare (driver retention).
- **Uber surplus per driver-hour on trip.** Rose 38%, £8.47 → £11.70.
- **Predictability.** Models trained pre-dynamic and tested on 2023 data: **R² = −54** (vs 0.85–0.89 in earlier years). *"The predictability of pay drastically changed after dynamic pricing was introduced."*
- **Inequality.** Pay distributions across drivers diverged sharply post-2023.
- **Utilisation.** *"Standby time has risen significantly — increasing by over 1 hour a week since 2022... In most months since 2023, drivers spend more time waiting to be allocated their next job than they do on journeys with passengers."*

### Information-asymmetry structure (quote)

> "The amount that a passenger pays for a trip is not available to drivers in the app, and Uber bars drivers from asking their passengers for this information directly, so it is not possible for drivers to work out Uber's cut on any given journey."

Post-dynamic: *"The customer fares were removed from drivers' weekly earnings report, meaning drivers could no longer see how much of a cut Uber takes from any given trip."* Drivers who ask passengers directly have been blocked by Uber.

### Audit methodology

258 drivers submitted GDPR Article 15/20 DSAR responses to Worker Info Exchange (WIE). Each DSAR yielded 40–45 files (~35 CSVs). WIE built a local automated pipeline on a dedicated laptop; researchers co-designed questions in a 15-driver workshop; code + data at `github.com/OxfordHCC/FAccT_25_Not_Even`. *"To our knowledge, this is the first contribution to the algorithm auditing field of a large-scale audit based on DSARs."*

### Structural vulnerability

*(editorial)* The Uber pricing algorithm is effectively **opaque-by-design** to both drivers and passengers. It combines:
- Per-trip per-person features (driver history, passenger history, route, time)
- Undisclosed inputs Uber will not name
- Dual-side optimization (passenger fare and driver fee move independently)

Consumer-side counter-strategies against this system are structurally different from any other family on this page because **both sides of the market are algorithmic subjects** — the driver is being priced simultaneously with the passenger. The successful counter-action documented in the paper is DSAR-based participatory audit — a legal-tool, not an ML-tool. The authors explicitly advocate this path: *"platform transparency should also be pursued through regulation and/or collective agreements."*

## Data-input catalogue — cross-family

*(editorial synthesis of the data-type categories that appear across Families 1–6, with source-traceable examples of each category from the captured papers.)*

The data an algorithm consumes falls into six categories. For each, I list which families use it, who owns it, and whether a consumer has any realistic access to disrupt it.

| Category | Description | Families that use it | Owner | Consumer-side access to disrupt? |
|---|---|---|---|---|
| **First-party: seller-owned operational state** | Seller's own inventory, capacity, occupancy, rent-roll, booking history | 2 (Safonov, indirectly), 4 (Williams), 5 (RealPage first-party bucket) | Seller | None without intrusion. Off-limits for consumer counter-power. |
| **First-party: seller-owned consumer signals** | Browsing, clicks, cart, purchase history on seller's own site/app | 3 (Tanković offer prototype), 6 (Uber per-trip), also retail neural demand with personalization | Seller, but *consumer-generated* | Full — it's the consumer's own behaviour. Client-side obfuscation ([[obfuscation]]) applies directly. |
| **Pooled nonpublic peer data** | Competitor rent rolls, lease terms, transactional microdata pooled across firms | 5 (RealPage) | Intermediary (e.g., RealPage) | Not directly reachable by consumer. Disruption requires antitrust/regulatory action (see [[regulatory-responses|§1 DOJ]]) |
| **Third-party consumer data (broker)** | Demographics, credit, location, predicted interests sold by Acxiom/Experian/Epsilon to sellers | 1 (context vectors often include broker data in practice; FICO in Zhao experiment), 3 (Tanković's MF scores), 6 (inferred driver profile features) | Data broker | Indirect: broker opt-outs, GDPR Art. 21 objection, CCPA deletion. Slow / partial. |
| **Aggregate market signals** | Seasonality, macro, public competitor prices, weather, news | 2 (Safonov aggregations), 4 (Williams via monopoly-market assumption; competitor prices excluded), 5 (RealPage market seasonality) | Public / shared | Full access to observe; limited ability to shift aggregate reality. |
| **Consumer response labels (purchase, click, cancel, acceptance)** | The model's dependent-variable training signal | ALL | Seller | Full — the label is the consumer's own choice. Coordinated labelling is the [[adversarial-data-poisoning\|ACA feature-label strategy]] directly. |

## Cross-family themes

*(editorial synthesis, comparing across the six captured families)*

### Theme 1 — Not all dynamic pricing is "surveillance pricing"

The Williams airline-RM model uses **no individual identity signals**. The Safonov neural-retail model uses **no individual customer features**. Yet both are "dynamic pricing" in the [[dynamic-pricing-overview]] genus sense. The conflation in popular discourse between "dynamic pricing" and "surveillance pricing" is incorrect. This is directly relevant for strategy: levers that target individual-identity signals (session rotation, fingerprint parity) are *structurally ineffective* against aggregate-demand-only algorithms.

### Theme 2 — The critical data type varies per family

| Family | Critical data type | Disruption lever (reference-layer) |
|---|---|---|
| 1 (GLM/contextual bandit) | Per-user feature vector z_t | [[obfuscation]], [[browser-fingerprinting]] session rotation |
| 2 (neural demand) | Aggregate sales history + on-shelf availability | Coordinated purchase-timing / stockout-trigger |
| 3 (retail offer bandit) | Purchase-gap / brand-loyalty / click label | [[obfuscation]] + coordinated click/no-click |
| 4 (airline RM) | Booking-curve velocity | Coordinated purchase-timing at population scale |
| 5 (RealPage hub-and-spoke) | Pooled competitor data (nonpublic) | Antitrust / structural — not consumer-reachable |
| 6 (Uber per-trip) | Driver acceptance history + undisclosed | DSAR / GDPR Art. 15/20 + [[noyb\|strategic litigation]] |

### Theme 3 — The same "surveillance" data can feed very different algorithms

A consumer's browsing history can feed: (a) a contextual bandit offer selector, (b) a neural demand estimator's promotion-history aggregate, (c) a broker's demographic inference feeding a third seller, (d) a loyalty-segmentation GBM that runs adjacent to a Williams-style RM system. Disrupting the data at source affects all four downstream users differently. A strategy designed against (a) may have no effect on (d).

### Theme 4 — Opacity is a feature, not a bug

Uber's post-2023 transition documented *predictability collapse from R²=0.85 to R²=−54* for drivers. This is not an accident: opacity is the business model advantage of dynamic pricing. The consumer-side analogue is the Bó et al. 2024 result on [[obfuscation]] that consumers in opaque-context treatments demand privacy *less* and make worse decisions. Opacity extracts surplus; transparency redistributes.

## Source

- `raw/research/seller-algorithm-taxonomy/01-03-contextual-dynamic-pricing-dp.md` — Zhao, Jiang & Yu, *Contextual Dynamic Pricing: Algorithms, Optimality, and Local Differential Privacy Constraints*, arXiv 2406.02424. Origin: academic OR/ML. Audience: OR + privacy researchers. Purpose: regret-optimal pricing with LDP. Trust: high; theorems proven, real-data experiment on 5-covariate loan-pricing data.
- `raw/research/seller-algorithm-taxonomy/02-04-neural-demand-retail.md` — Safonov, *Neural Network Approach to Demand Estimation and Dynamic Pricing in Retail*, arXiv 2412.00920. Origin: academic ML + econometrics. Audience: retail analytics. Purpose: NN demand estimation under low price variation. Trust: high; empirical 10M-observation retailer dataset.
- `raw/research/seller-algorithm-taxonomy/03-05-scalable-contextual-bandits.md` — Tanković & Šajina, *Scalable and Interpretable Contextual Bandits: A Literature Review and Retail Offer Prototype*, arXiv 2505.16918. Origin: academic + practitioner. Audience: ML engineers. Purpose: review + deploy. Trust: high for the review; the prototype is proof-of-concept, not evaluated in production.
- `raw/research/seller-algorithm-taxonomy/04-08-yale-tap-realpage.md` — Yale Thurman Arnold Project 2025 Student Paper #07, *RealPage*. Origin: academic (student / clinical). Audience: antitrust policy. Purpose: remedial argument for the RealPage case. Trust: high for legal/structural analysis; algorithmic detail limited.
- `raw/research/seller-algorithm-taxonomy/07-07-williams-airline-pricing.md` — Williams, *Dynamic Airline Pricing and Seat Availability*, Cowles Foundation 3003U (2018). Origin: academic industrial organization. Audience: IO economists. Purpose: estimate welfare effects of airline dynamic pricing. Trust: high; preregistered identification strategy, 79K-observation original dataset.
- `raw/research/seller-algorithm-taxonomy/08-09-uber-algorithmic-pay-audit.md` — *Not Even Nice Work If You Can Get It: A Longitudinal Study of Uber's Algorithmic Pay and Pricing*, arXiv 2506.15278 / FAccT 2025. Origin: academic + worker-advocacy participatory audit. Audience: FAccT community + platform-worker advocates. Purpose: document pay and predictability changes post-dynamic-pricing transition in the UK. Trust: high for the empirical data (1.5M trips via GDPR DSARs); inferences about Uber internals limited to what Uber disclosed or what schema evidence reveals. Declare-interest: authors embedded in Worker Info Exchange.

Two sources dropped during capture: Ban & Keskin 2020 (SSRN / INFORMS both 403 bot-walled) — conceptual content overlaps with Family 1 (Zhao et al.); GMU Revenue Management textbook chapter (SSL cert failure) — empirical RM content covered by Family 4 (Williams).

## Related

- [[dynamic-pricing-overview]]
- [[rental-housing-algorithmic-pricing]]
- [[consumer-facing-dynamic-pricing]]
- [[surveillance-pricing-retail]]
- [[algorithmic-collusion]]
- [[obfuscation]]
- [[adversarial-data-poisoning]]
- [[browser-fingerprinting]]
- [[collective-bargaining-for-data]]
- [[data-disruption-strategy-map]]
- [[possible-strategic-levers]]
