# Algorithmic Collusion

"Algorithmic collusion" names two related but distinct phenomena: **explicit** coordination in which competitors share data through an algorithmic intermediary, and **tacit** coordination in which independently-developed learning algorithms converge on supracompetitive prices without any agreement. The academic literature treats the tacit variant as the harder and less-resolved problem; the enforcement literature has so far concentrated on the explicit variant.

## Explicit: shared-tool coordination

The paradigm case is [[rental-housing-algorithmic-pricing|RealPage]] — a third-party vendor aggregates nonpublic competitor pricing data, runs an algorithm over the pooled data, and returns recommendations that align rents across competing landlords.

Other real-world cases:
- **UK online poster retailers** (cited by arXiv 2504.16592): retailers used simple pricing algorithms as the mechanism of an explicit horizontal cartel on Amazon.
- **US wall-art Amazon retailers** (cited by HBS 22-050): 2015 DOJ prosecution, guilty plea for using pricing algorithms to fix prices.

Enforcement tools against this variant are largely the existing antitrust toolkit — Sherman Act Section 1 in the US, Article 101 TFEU in the EU.

## Tacit: learning-algorithm convergence

The harder problem. Multiple independent sellers each run a learning algorithm on their own prices; the algorithms, through repeated interaction in the market, converge on prices above the competitive level. No agreement exists; no data is shared. The question is whether antitrust law can or should reach this.

**Empirical evidence that tacit collusion occurs.** Assad et al. (2024), studying the German gasoline market, found that duopoly stations experienced a 28% margin increase when *both* competitors adopted algorithmic pricing. Monopoly stations saw no change. The asymmetry between duopoly and monopoly is the characteristic signature of coordinated (not merely optimised) pricing. *(arXiv 2504.16592.)*

**Theoretical mechanisms.** The arXiv survey covers Q-learning, Exp3 (exponential-weights bandit), and deep reinforcement learning in repeated Bertrand-competition settings. Q-learning is the most-studied and — in simulation — reliably converges to supracompetitive prices under certain parameter ranges (exploration rate, synchronous vs asynchronous updates, memory length). The Folk Theorem for repeated games shows that collusive outcomes *can* be equilibria if players are sufficiently patient; learning algorithms appear to find such equilibria in practice. The theory of *when* and *why* this happens is incomplete. *(arXiv 2504.16592.)*

## Non-collusive harm: asymmetric speed and commitment

Distinct from tacit collusion, HBS working paper 22-050 (MacKay and Weinstein) identifies a harm route that does not require any form of coordination:

**Asymmetric frequency.** A firm with a faster-updating algorithm (daily or multiple times daily) competes against a rival with a weekly price update. The faster firm can undercut the rival whenever profitable while maintaining supracompetitive margins overall. The slower firm, anticipating this, rationally charges a supracompetitive price itself. Both firms earn more than in Bertrand equilibrium, despite appearing to compete.

**Algorithmic commitment.** An algorithm that credibly and observably reacts to competitor price changes acts as a commitment device — the rival anticipates the reaction and prices higher in advance. Commitment of this kind is classically a monopolist's tool; algorithms make it accessible to any firm with faster software.

**Illustrative example (HBS):** an allergy medicine priced at $13, $17, and $20 across three retailers appears to show competition, but — under asymmetric-frequency dynamics — all three prices can be supracompetitive.

**Empirical evidence:** the HBS authors cite existing empirical work showing asymmetric pricing frequency in e-commerce is already associated with higher prices.

This is a materially different theory of harm from collusion. It implies that *single-firm* unilateral algorithmic pricing can produce the same consumer damage as cartel behaviour — without any coordination, implicit or explicit.

## Why this matters for enforcement

- **Explicit coordination** is reachable by existing antitrust law (see [[rental-housing-algorithmic-pricing]]).
- **Tacit collusion** is not cleanly reachable — antitrust law in both the US and EU typically requires proving an agreement, which does not exist when algorithms converge independently. *(arXiv 2504.16592.)*
- **Non-collusive asymmetric-frequency harm** is even further outside the antitrust frame — there is no coordination to prove. HBS proposes structural remedies: **price-setting frequency caps** (e.g., firms may change prices only once per week), **algorithm transparency and auditing**, and **pre-deployment testing**.
- The arXiv survey proposes a research agenda focused on **detection** (statistical and ML methods to identify collusion signatures in market data), **monitoring** (real-time regulatory visibility), and **accountability** (algorithm disclosure and compliance audits).

See [[regulatory-responses]] for the state of proposed and enacted legislation.

## Open questions

- No comprehensive theory predicts when learning algorithms converge to Nash equilibrium, cycle, diverge, or land on collusive-looking equilibria. This is the central open problem named by arXiv 2504.16592.
- Empirical evidence outside the German gasoline market is limited — industry-level data on algorithmic-pricing adoption and prices is hard to get.
- The boundary between "non-collusive" asymmetric-frequency harm (HBS) and tacit collusion (arXiv) is blurry in practice; a firm using an algorithm that observes competitor prices and credibly reacts is simultaneously using a commitment device and engaging in something that looks like signalling.

## Design-input candidates *(editorial — not source content)*

- **Pricing-frequency observatory.** A public dashboard that tracks price-change frequency for a basket of goods across retailers. Frequency itself is a counter-power signal: asymmetric frequencies are the HBS harm mechanism.
- **Algorithm disclosure submission tool.** If and when algorithm-disclosure regulations pass, a turnkey tool for consumer groups to file regulatory requests for disclosure would lower the administrative barrier.
- **Collusion-detection sandbox.** An open-source reimplementation of the Assad et al. analysis pipeline, applied to scrape-collected retail price data. Lowers the barrier for researchers and advocacy groups to flag suspect markets.

## Source

- `raw/research/dynamic-pricing-landscape/07-hbs-dynamic-pricing-harm.md`
  - **Origin:** Harvard Business School working paper 22-050 (MacKay and Weinstein).
  - **Audience:** academics, antitrust lawyers, policymakers.
  - **Purpose:** argue that algorithmic pricing can harm consumers without collusion and propose regulatory remedies.
  - **Trust:** HBS working-paper tier; authors are cited in legal-academic literature.
- `raw/research/dynamic-pricing-landscape/08-arxiv-algorithmic-collusion.md`
  - **Origin:** arXiv 2504.16592 (April 2025), accepted at *Business & Information Systems Engineering*.
  - **Audience:** CS and economics researchers.
  - **Purpose:** interdisciplinary survey of algorithmic collusion theory, experiments, and open problems.
  - **Trust:** preprint accepted at peer-reviewed venue.
- `raw/research/dynamic-pricing-landscape/01-doj-realpage-lawsuit.md` — used here as the empirical anchor for the explicit-coordination variant (full treatment at [[rental-housing-algorithmic-pricing]]).

## Related

- [[dynamic-pricing-overview]]
- [[rental-housing-algorithmic-pricing]]
- [[surveillance-pricing-retail]]
- [[regulatory-responses]]
