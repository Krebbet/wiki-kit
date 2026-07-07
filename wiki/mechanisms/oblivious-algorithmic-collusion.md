# Oblivious Algorithmic Collusion

Wu and Zeevi (arXiv 2606.05363, EC 2026) study a specific modeling choice that every pricing algorithm makes: whether to include competitor prices in its demand model. An **informed** seller incorporates competitor prices; an **oblivious** seller ignores them. The paper shows that oblivious learning generates only transient collusive excursions that dissipate as learning progresses, and that the Nash equilibrium of the modeling-choice game is the all-informed market — which converges to competitive prices. Contrary to the intuition that "strategic ignorance" sustains collusion, the mechanism for sustained supracompetitive outcomes under least-squares demand learning is competitor-price inclusion, not exclusion.

## The Oblivious vs Informed Dichotomy

In the model, multiple sellers repeatedly set prices and estimate demand via iterated least squares. The modeling choice — oblivious or informed — determines what covariates appear in the demand model:

- **Oblivious:** demand estimated as a function of own price only. The seller does not observe or incorporate what rivals charge.
- **Informed:** demand estimated as a function of own price *and* competitor prices.

Classical statistical learning favors informed: ignoring competitor prices induces model misspecification, because in a competitive market demand does depend on rivals' prices. The paper confirms this efficiency result — informed sellers earn strictly more than oblivious sellers in mixed markets.

## Oblivious Sellers Must Explore More

Because the oblivious seller cannot track competitor-price dynamics directly, it faces greater uncertainty about its demand function. Wu and Zeevi show formally that, relative to a monopolist facing the same demand problem, an oblivious seller in a competitive market must **explore more aggressively** — i.e., maintain a higher exploration rate — to compensate for this information loss. This additional exploration is the key mechanism behind the competitive-convergence result.

## Market Dynamics: Convergence and Pseudo-Equilibria

When *all* sellers are oblivious:

- **With sufficient exploration:** prices converge to the competitive (Nash) equilibrium outcome. The excess exploration required by oblivious sellers acts as a market-regularizing force.
- **When exploration decays:** a **continuum of pseudo-equilibria** arises. Prices do not necessarily converge to the competitive outcome, but neither do they stably lock in at supracompetitive levels. The pseudo-equilibria are not robust Nash equilibria of the underlying pricing game.

## The Excursion Phenomenon

Analyzing price trajectories under oblivious learning, Wu and Zeevi uncover an **excursion phenomenon**: prices periodically visit supracompetitive levels (collusive excursions) before returning toward competitive prices as learning accumulates. These excursions are transient — they are an artifact of imperfect demand estimation, not of strategic coordination — and dissipate as the sellers accumulate more observations.

The excursion phenomenon matters for detection: it produces price spikes that superficially resemble collusive episodes. A market-monitoring tool observing raw price series would need to distinguish excursion-driven spikes (transient, self-correcting, not coordinated) from genuine tacit-collusion episodes of the kind documented in [[algorithmic-collusion]].

## Nash Equilibrium of the Modeling-Choice Game

When each seller can choose its modeling strategy — oblivious or informed — treating the choice as a strategy game yields a clean result: **the all-informed market is the unique Nash equilibrium**. No seller can benefit by switching to oblivious if all others are informed; and if all are oblivious, any individual seller can gain by switching to informed.

In the all-informed equilibrium, prices converge to the competitive outcome *efficiently* (i.e., at the rate implied by standard statistical learning without the excess exploration cost oblivious sellers incur).

## Implications

**For collusion theory.** The Wu & Zeevi result clarifies that the algorithm architecture — specifically, whether competitor prices are inputs to demand estimation — is a determinant of whether sustained supracompetitive pricing arises under least-squares learning. This complements, but does not contradict, the Frick 2026 result (arXiv 2604.15825) on deep RL convergence: Frick's agents are effectively informed (they observe market outcomes including competitor behavior); Wu & Zeevi's oblivious agents are categorically different. Together, the two papers suggest that **informed learning algorithms are the locus of collusion risk**, not oblivious ones.

**For algorithm disclosure and transparency tools.** A disclosure request or audit framework should specifically elicit whether competitor prices are inputs to a seller's demand model. Obliviousness is not the danger; competitor-price inclusion is. This sharpens the question that [[transparency-tools]] and disclosure mandates should ask.

**For counter-power tooling.** A regulatory intervention mandating "blind" algorithms (prohibiting competitor-price inputs to pricing models) would, under this model, push markets toward competitive outcomes — and would simultaneously eliminate the sustained tacit-collusion mechanism identified in the broader [[algorithmic-collusion]] literature. Whether such a mandate is enforceable or detectable is a separate question.

**For market surveillance.** The excursion phenomenon provides a testable signature: brief, self-correcting price spikes in markets where sellers are known to use oblivious algorithms are not evidence of collusion. Sustained supracompetitive margins — especially those correlated with competitor-price tracking — are the actionable signal.

## Relationship to Existing Work

| Work | Algorithm type | Result |
|---|---|---|
| Assad et al. 2024 (German gasoline) | Empirical; algorithm type uncharacterized | Duopoly margin +28% on adoption |
| arXiv 2504.16592 (survey) | Q-learning, Exp3, deep RL | Tacit collusion documented in simulation |
| Frick 2026 (arXiv 2604.15825) | Deep RL (informed) | Fast convergence to collusive equilibrium |
| **Wu & Zeevi 2026 (this page)** | **Least-squares; oblivious vs informed** | **Oblivious: transient excursions only; informed: efficient competitive convergence; NE = all-informed** |

## Source

- `raw/research/weekly-2026-07-06/03-arxiv-2606-05363.md`
  - **Origin:** arXiv 2606.05363 (Yuhang Wu, Assaf Zeevi; submitted June 3 2026, v2 June 8 2026). Preliminary version accepted at EC 2026 as "Oblivious Learning, Price Exploration and Collusive Dynamics."
  - **Audience:** CS/game-theory and theoretical-economics researchers.
  - **Purpose:** Characterize market dynamics under oblivious vs informed demand learning and determine whether strategic obliviousness sustains algorithmic collusion.
  - **Trust:** Conference-accepted (EC 2026 is selective); two authors (Columbia); moderate-high trust pending full-text review.

## Related

- [[algorithmic-collusion]] — parent page; covers explicit coordination, tacit RL convergence (Frick 2026), and asymmetric-frequency harm
- [[pricing-algorithm-taxonomy]] — the oblivious/informed distinction adds a new axis: competitor-price inclusion in demand model
- [[adversarial-data-poisoning]] — poisoning competitor-price signals fed to informed sellers is an implied counter-power lever
- [[transparency-tools]] — disclosure frameworks should elicit whether competitor prices are demand-model inputs
- [[the-firms-view]] — firms may cite this paper to argue their oblivious algorithms are pro-competitive
