# Learning-Rate Delegation in Pricing (Ashkenazi-Golan et al. 2026)

Theory-only mechanism page. Ashkenazi-Golan, Plumb, Possnig & Zhang (arXiv 2610.11675, submitted 8 Oct 2026, econ.TH / cs.GT) claim that in a continuous-time pricing game, firms delegating pricing to gradient-learning algorithms choose fast learning under strategic substitutes but deliberately sluggish learning under strategic complements, extracting surplus during the prolonged convergence to the competitive price. **Abstract-only capture: no proofs, model details or magnitudes; full-text re-capture pending (see watchlist).**

## What the abstract reports

- Meta-game over learning rates; payoff is discounted profit along the whole learning path.
- Under strategic complements (typical of differentiated-product price competition), slow algorithms earn supracompetitive transitional profits although the competitive price is strictly dominant in the stage game.
- Route needs no communication, punishment or explicit coordination. No specific industry or deployed system named; no counter-power mechanism described.

## Origin / audience / purpose / trust

Academic unreviewed arXiv v1 preprint for theorists; purpose: document a formal result. Trust: medium (credible venue class, no peer review, abstract only).

## Tension with oblivious-collusion result

Mild, not a conflict. [[mechanisms/oblivious-algorithmic-collusion]] reports collusive excursions are transient and dissipate as learning proceeds. This paper agrees on convergence to competitive prices but argues firms profit from the transient and strategically lengthen it, so "only transient" need not mean "low harm". It also offers a deliberate-slowness mechanism against the "collusion emerges fast" finding noted on [[algorithmic-collusion]]. No conflicts file opened; none open on this theme.

## Hooks *(editorial)*

- Audit/disclosure: learning-rate and adjustment-speed parameters are a plausible disclosure target alongside competitor-price inputs ([[regulatory-responses]]).
- Detection: persistent slow, monotone price drift toward the competitive level may signal deliberately sluggish design. Inference, not a claim of the paper. Not a build candidate.

## Source

- `raw/research/weekly-2026-10-12/02-delegate-pricing-algorithms.md`
  - **Origin:** arXiv abstract page (2610.11675).
  - **Audience:** economic theorists.
  - **Purpose:** document a formal result.
  - **Trust:** medium; abstract only.

## Related

- [[algorithmic-collusion]]
- [[mechanisms/oblivious-algorithmic-collusion]]
- [[pricing-algorithm-taxonomy]]
- [[strategic-classification]]
- [[the-firms-view]]
- [[regulatory-responses]]
- [[dynamic-pricing-overview]]
