# Accuracy Is Not Welfare: AI Buyers under Strategic Price Complexity (Ning 2026)

Ning (arXiv 2611.16471) evaluates LLM buyers in a synthetic two-seller subscription duopoly where sellers commit to a markup and one of three fee representations. A calculator-assisted buyer is more accurate than an unassisted one (84.00% vs 68.57% optimal offers), yet verified-total disclosure yields a higher consumer-worst correlated-equilibrium surplus (53.06 vs 32.92). Fixed-menu accuracy and equilibrium welfare therefore rank buyer pipelines differently. Single-author, non-peer-reviewed, synthetic: treat as a design input for evaluation, not as evidence about real markets.

## Key findings

- **Setup.** Sellers choose prices and presentations to exploit residual AI-buyer errors (strategic price complexity); the margin on the chosen contract matters, not just error frequency. Analogues named: fee comparison in payments and retail finance. 81-profile action grid with empirical correlated-equilibrium (CE) bounds.
- **Ranking reversal.** Calculator tool wins on accuracy; disclosure of verified total payment wins on consumer-worst CE surplus and in a frozen-strategy holdout (+25.51, 95% CI [10.69, 42.08]).
- **Not robust.** Once equilibria are re-solved under resampling the welfare ranking does not hold; the equilibrium sensitivity interval [-13.32, 33.77] spans zero. The author states the paper does not estimate a real regulatory effect. Randomized reasoning-budget policy did poorly in a later matched subset.
- **Replication.** Package released (notebooks, tables, figure code, model-free audit, 31,104 core observations); the author did not rerun the GPU experiments for the manuscript.

## Takeaways

- **Evaluation template.** Evaluate buying agents by welfare in a seller-response game; report accuracy, loss severity, incentives and incidence separately. Relevant to any collective buying-agent or benchmark harness. *(editorial)*
- **Adaptation risk.** Buyer-side accuracy gains can be undone by seller adaptation: tech-as-counter-power with an equilibrium-response caveat. Disclosure/transparency mandates and tooling are complements, not substitutes, in this model, but the ordering is fragile. *(editorial)*
- **Tension with simulation evidence.** [[consumer-ai-assistant-market-simulation]] reports adopters cutting spend after seller adaptation; this paper shows a more accurate pipeline can still leave consumers worse off at equilibrium. The two differ in design (synthetic duopoly vs. market simulation) and neither is field evidence.

## Source

- `raw/research/weekly-2026-11-16/04-accuracy-not-welfare-ai-buyers.md` — Ning (SUFE), arXiv 2611.16471, capture URL https://arxiv.org/pdf/2611.16471 (PDF capture, 2026-11-16). Origin: single-author academic preprint (JEL D18/D43/D83/L13). Audience: IO and AI-evaluation researchers. Purpose: argue AI buyers must be judged on seller incentives and welfare incidence, not task accuracy. Trust: low-medium; not peer-reviewed, synthetic simulation in simulation units, welfare ranking not robust to equilibrium re-solving.

## Related

- [[consumer-ai-assistant-market-simulation]] — adopter gains after seller adaptation; tension noted above
- [[artificial-shoppers-attention-competition]] — parallel: accurate AI assistance does not guarantee consumer gain once sellers respond
- [[agent-mediated-negotiation-empirics]] — empirical LLM-agent market behaviour
- [[agents-vs-ecommerce-opacity]] — opacity and price complexity facing agents
- [[algorithmic-collusion]] — seller-side strategic response and equilibrium analysis
- [[transparency-tools]] — verified-total disclosure as transparency mechanism, mixed result
