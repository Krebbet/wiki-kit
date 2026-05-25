# Data-Market Mechanism Design

Mechanism page for the **algorithmic mechanism design layer above [[federated-learning]] / [[data-cooperatives]]** — specifically, how to fairly distribute revenue among data providers based on each provider's marginal contribution to a model trained on the pooled data, while making the marketplace truthful (buyers bid honestly), incentive-compatible, and **robust to replication** (preventing a seller from gaming the system by duplicating their data stream). Anchored on Agarwal, Dahleh & Sarkar 2019 *A Marketplace for Data: An Algorithmic Solution* (EC 2019; arXiv 1805.08125). The substrate mechanism design any data-cooperative or CBI bargaining intermediary faces if it wants to share revenue from data pooling among members. Critical tension to surface: the paper's market-mechanism framing clashes with the democratic-governance framing on [[data-cooperatives]] in well-defined ways, documented in the §Tensions section below.

## What the mechanism does

A two-sided real-time marketplace with **M fixed data sellers** and **N arriving buyers**. Each buyer specifies a prediction task (label vector Y_n) and bids b_n on how much they value a marginal unit increase in prediction accuracy. The marketplace then:

1. **Allocates** degraded / noisy feature sets to each buyer proportional to price-bid difference (more bid → less noise).
2. **Extracts revenue** based on accuracy gain achieved.
3. **Divides revenue** among sellers based on Shapley-value marginal contribution.
4. **Updates prices** dynamically via online learning (Multiplicative Weights) to maximise total revenue.

**Allocation function:** features degraded by noise proportional to (p_n − b_n). For continuous data: X̃_j(t) = X_j(t) + max(0, p_n − b_n) · 𝒩(0, σ²). For binary: X̃_j(t) = B(t; θ) · X_j(t), θ = min(b_n / p_n, 1).

## The four properties the paper proves

| Property | Theorem | Guarantee |
|---|---|---|
| **Truthfulness** | 5.1 | If allocation function is monotonic (more noise → less accuracy), then Myerson-payment-rule revenue function induces buyers to bid truthfully (μ_n = arg max U). |
| **Revenue maximisation (zero regret)** | 5.2 | Multiplicative-Weights price update achieves expected regret 𝔼[R(N)] ≤ O(√(log(B_max L √N) / N)), **independent of M (number of sellers)**. Average regret vanishes at O(1/√N). |
| **Shapley fair allocation** | 5.3 | Randomised Shapley sampling with K = O(M log(1/δ) / ε²) permutations computes ε-approximation of the exact Shapley value in **O(M²)** time, vs. Θ(2^M) for exact. |
| **Robustness to replication** | 5.4 | Algorithm 3 (Shapley with exponential penalty on feature-similarity SM) ensures ε-robustness — replicating a feature does not increase total payment to the seller. |

**Proposition 5.1 — fundamental impossibility:** balance (Σ ψ_n(m) = 1) and robustness-to-replication **cannot hold simultaneously** with anonymised sellers. The paper's mechanism trades a small balance violation for replication robustness.

**Computational efficiency (Corollary 5.1):** core marketplace functions run in O(M); payment-division algorithms run in O(M²). Polynomial time per buyer, independent of N.

## Why a single scalar price for all features

Rather than pricing each feature independently (exponential in M), the marketplace sets a single scalar price p_n. This is justified because **buyer valuations are parameterised by a single scalar μ_n** (value per unit accuracy), not a vector. Buyers receive noisy versions of all features, trading quality for price difference. This is a key mechanism-design choice that makes the polynomial-time guarantees possible — and also the choice that limits the marketplace to settings where buyers don't care which features they receive, only the joint accuracy.

## How this maps onto the wiki

| Wiki anchor | Why mechanism-design-relevant |
|---|---|
| [[data-cooperatives]] | The cooperative *organisational form* needs an internal mechanism for distributing revenue when it sells aggregated data products. Shapley-value allocation is one principled answer. The cooperative's democratic-governance framing introduces tension — see §Tensions below. |
| [[collective-bargaining-for-data]] | A CBI bargaining on behalf of named members must answer: how is the negotiated value distributed back? Shapley allocation is one answer; the CBI's mandate-based model is another. |
| [[federated-learning]] | FL is the substrate that lets the marketplace pool data without raw exposure; this paper is the mechanism design layer *above* the FL aggregation layer. |
| [[possible-strategic-levers\|Lever #1 — many-consumer counterbalance]] | Revenue-distribution mechanism for the data-pooling instantiation of the lever. |
| [[possible-strategic-levers\|Lever #19 — producer-coop × consumer-coop matching]] | Two-sided cooperative matching needs a revenue-distribution mechanism on at least one side. |
| [[midata]] / [[drivers-seat-cooperative]] | Existing data cooperatives that the wiki documents — neither has a published Shapley-style allocation mechanism; this page documents the design space. |

## Tensions with the wiki's cooperative framing

The wiki's [[data-cooperatives]] page documents data cooperatives as *democratic institutions* — member-owned, member-governed, applying ICA cooperative principles. The Agarwal mechanism is a *market mechanism* — efficient, truthful, Shapley-fair by mathematical construction. Four well-defined tensions emerge:

1. **Shapley-fairness vs. democratic voice.** The mechanism allocates revenue based on **empirical marginal contribution** (Shapley value of feature m for task Y_n). A seller has no agency over their payout; it is determined by how their data happens to correlate with this buyer's task. A democratic cooperative might demand that members have a *say* in how value is split — e.g., "we contributed equally, should split equally" regardless of correlation. Shapley resolves this by saying "fairness = marginal contribution"; this is a *designer's definition*, not a collective choice.

2. **Centralised price-setting vs. collective sovereignty.** The marketplace sets prices p_n centrally via the Multiplicative-Weights algorithm. Sellers are passive. A truly democratic data cooperative might demand that **members collectively negotiate prices**. The paper's centralisation is justified for tractability (regret bounds) and to preserve truthfulness (if sellers set prices, buyers lose incentive compatibility). But this trades off seller power.

3. **Scalar utility vs. multidimensional values.** Buyer utility is modelled as μ_n · G(Y_n, Ŷ_n) − cost. **Unidimensional**: buyers only care about accuracy gain per dollar. Cooperatives might care about **non-market values**: is the buyer using the data for social good or extractive profit? Does the buyer respect data sovereignty? Agarwal's framework has no slot for these.

4. **Robustness-to-replication as fragmentation incentive.** Algorithm 3 down-weights features similar to existing data via similarity metric SM. This punishes a seller for supplying data that is "similar" to others — e.g., two small retailers in the same city selling foot-traffic data. Rationally, sellers will *hoard unique data and avoid collaboration* — a **fragmentation incentive opposite to the pooling goal**.

**Resolution direction.** Market mechanisms are a *substrate*, not a complete governance model. A data cooperative can use Agarwal-style mechanisms for *some* allocation decisions (e.g., revenue from external data sales) while reserving democratic governance for *others* (e.g., deciding what data products to produce, who to sell to, what social-purpose constraints to apply). The two are layerable, not exclusive.

## Caveats

1. **Privacy is orthogonal in the paper.** Agarwal et al. assume data is "sufficiently anonymised" and sellers have no privacy concerns. Real cooperatives face privacy-utility tradeoff. The mechanism could integrate differential privacy into the allocation function but the paper does not. Combine with [[federated-learning]] privacy substrate.

2. **Single buyer task per arrival.** The paper models one task per buyer; multi-task buyers require extension.

3. **Scalability tested up to small M.** Polynomial-time guarantees are good asymptotically; large-scale empirical performance not established in the original paper.

## Source

- Agarwal, Dahleh & Sarkar. 2019. *A Marketplace for Data: An Algorithmic Solution*. ACM Conference on Economics and Computation (EC '19); arXiv 1805.08125; DOI 10.1145/3328526.3329589. Captured: `raw/research/clawnet-adjacent-methods/21-marketplace-for-data-agarwal.md` + `11-marketplace-for-data-agarwal-abs.md`. Trust tag: peer-reviewed EC '19 paper, foundational mechanism-design contribution to the data-market literature.

## Related

- [[data-cooperatives]] — primary organisational anchor; this page is the mechanism-design companion
- [[collective-bargaining-for-data]] — CBI bargaining lane; Shapley allocation is one answer to revenue distribution
- [[federated-learning]] — substrate technology underneath this mechanism
- [[possible-strategic-levers\|Lever #1, #19]] — the lever-inventory anchors
- [[midata]] / [[drivers-seat-cooperative]] — existing data cooperatives whose internal allocation mechanisms are not explicitly Shapley
- [[the-firms-view]] — none of this directly mirrors a firm-side framing, but the buyer-side view of the same mechanism is what firms get when they purchase from a cooperative
