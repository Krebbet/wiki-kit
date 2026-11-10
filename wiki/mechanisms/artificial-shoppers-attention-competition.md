# Artificial Shoppers and Attention Competition (Guo, Xu & Zhang 2026)

Theory-only mechanism page. Guo, Xu & Zhang (arXiv 2611.09399) model a retail platform that hosts two of three vertically differentiated products and offers consumers either an AI shopping assistant (curates a shortlist) or an AI agent (selects the product), under salience-distorted choice. They find that AI access can soften price competition, and that an "alignment paradox" holds: even when the assistant ranks by true utility, some consumers end up worse off while aggregate surplus rises. Stylised model; no code or data released.

## Takeaways

- **Assistance can soften competition.** The middle-quality firm forgoes low-valuation buyers because one price must serve several recommendation groups. Hosted prices can rise under a high+middle pair and fall under a high+low pair.
- **Alignment paradox.** The best product is still shown and cheaper, but price salience induces a switch to a lower-quality product whose quality loss exceeds the saving. Individual losses coexist with higher aggregate surplus.
- **Narrow win-win.** Platform profit and aggregate consumer surplus both rise only for assistance with the A+B assortment and delegation with A+C.
- **Delegation weakly preferred by the platform.** The platform's preferred design (delegation plus a specialised-premium assortment) can still yield lower consumer surplus than the no-AI optimum, which hosts A+C.
- **Commission is neutral on prices.** Under either AI mode, the hosted pair does not change prices; a proportional commission only rescales profits.
- **Off-platform seller** moves from zero to positive sales.
- **Softening needs no algorithmic coordination.** It arises from single-price, multi-segment incentives.
- **Evaluation implication.** Audit shopping interfaces on induced choices and welfare after firm price response, not ranking accuracy. Monitor prices after AI introduction.
- **Assumptions limiting transfer:** AI perfectly observes consumer types, shortlist of two, AI operated by the platform. Independent user-side agents are not analysed. A choice-aware shortlist (optimising the realised purchase) is flagged by the authors as unmodelled future work.
- No counter-power mechanism is proposed. No code.

## Tension with existing positions

- [[mechanisms/consumer-ai-assistant-market-simulation]] reports that consumer-side assistants cut adopter spending (13.7 to 8.7 USD per renter-day after seller adaptation). Guo et al. find that, under some assortments, AI access raises hosted prices. The settings differ (simulated LLM-agent rental market with consumer-owned executing mandates vs a platform-operated AI in a three-product equilibrium model), so the results are likely complementary rather than contradictory. Neither is adopted over the other.
- The wiki's agent pages treat preference alignment as the target ([[mechanisms/agentic-privacy-preference-taxonomy]]). This paper's claim that accurate ranking is insufficient for some consumers qualifies that, within its stylised model. It does not address privacy preferences.

## Source

- `raw/research/weekly-2026-11-09/01-artificial-shoppers-attention-competition.md` (arXiv 2611.09399)
  - **Origin:** academic preprint by authors at HK PolyU (logistics) and UConn (business school).
  - **Audience:** operations, marketing and IS researchers; secondarily platform operators, retailers and regulators.
  - **Purpose:** characterise equilibria of AI-mediated shopping.
  - **Trust:** medium-high for the formal model (preprint, stylised); low weight as empirical evidence. Cited industry statistics (e.g. Adobe +693.4% genAI retail traffic, holiday 2025) are not original.

## Related

- [[mechanisms/consumer-ai-assistant-market-simulation]] — simulation counterpart on consumer-side assistants
- [[mechanisms/agents-vs-ecommerce-opacity]] — commentary on sellers blocking shopping agents
- [[mechanisms/agent-mediated-negotiation-empirics]] — empirical agent behaviour vs this delegation model
- [[mechanisms/agent-interop-protocols]] — standardising AI surfaces, merchants and payments
- [[mechanisms/algorithmic-collusion]] — price softening without explicit coordination
- [[mechanisms/oblivious-algorithmic-collusion]] — softening emergent from design, not intent
- [[mechanisms/learning-rate-delegation-pricing]] — another theory result on delegation and pricing
- [[mechanisms/agentic-privacy-preference-taxonomy]] — agents knowing user preferences
- [[mechanisms/the-firms-view]] — firm-side optimisation for AI visibility
- [[mechanisms/pricing-algorithm-taxonomy]] — classification context
- [[industries/consumer-facing-dynamic-pricing]] — price response to AI exposure
- [[industries/surveillance-pricing-retail]] — type-aware pricing and choice shaping
- [[tools/consumer-price-tools]] — evaluation criterion for user-side tools
- [[counter-power/regulatory-responses]] — audit of interfaces on induced choices
