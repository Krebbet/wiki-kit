# Agents vs Ecommerce Opacity

Doctorow (Pluralistic, 2026-10-28) argues that ecommerce opacity (surveillance pricing, drip pricing, junk fees) is a profit source, not a defect, so sellers have no incentive to be legible to consumer shopping agents and will block them. He frames agentic comparison shopping as resting on the assumption that everyone else sets aside their interests, and as a principal-agent conflict with the seller. Opinion commentary; claims are the author's and mostly link to his earlier posts. Useful as problem-framing and threat model, not as evidence.

## Claims (author's)

- **Opacity as feature:** surveillance pricing, drip pricing, junk fees, price fixing and "most favored nation" deals are said to be the source of all profitability growth at the largest firms. These tactics require opacity and are antithetical to automated comparison shopping.
- **Enforcement is weak:** bipartisan state and federal suits target drip pricing and junk fees, but he argues fines are cheaper than compliance and regulators can be bought off.
- **Blocking:** ecommerce sites are mass-blocking third-party AI agents (he cites a Gizmodo report). Stated reasons: agents let shoppers "cheat" (e.g. indefinitely renewing a temporary hold on a used item), and sites do not want automation on their platforms at all.
- **Seller-side AI:** Google is said to plan selling merchants surveillance data combined with AI tools for price-gouging.
- **Agent architecture:** single browsing agents gave way to specialist swarms; he argues error rates compound as agents are added, offsetting accuracy gains from specialization.
- **Metacrap analogy:** like the Semantic Web, agentic shopping demands that others rearrange their affairs for the planner's benefit.

## Use in this wiki

- Threat-model input for consumer-agent designs: assume counterparty blocking and obfuscation (inference, not stated by the author).
- Contrasts with simulation work that assumes sellers compete on agent-readable terms ([[mechanisms/consumer-ai-assistant-market-simulation]]) and benchmarks that do not model access denial ([[mechanisms/agent-mediated-negotiation-empirics]]).
- No counter-power mechanism is proposed by the author.

## Source

- `raw/research/weekly-2026-11-02/05-agents-vs-ecommerce-opacity.md`
  - **Origin:** Pluralistic (Cory Doctorow), 2026-10-28.
  - **Audience:** general tech-policy readers.
  - **Purpose:** commentary and advocacy.
  - **Trust:** medium-low; opinion, no new data, self-referential links.

## Related

- [[mechanisms/agent-mediated-negotiation-empirics]] — agent buyer/seller benchmarks; omits access blocking
- [[mechanisms/consumer-ai-assistant-market-simulation]] — market simulation assuming agent search reaches sellers
- [[industries/surveillance-pricing-retail]] — surveillance pricing as an opacity tactic
- [[counter-power/regulatory-responses]] — drip pricing and junk fee enforcement
- [[mechanisms/transparency-tools]] — comparison tools depend on legible prices
- [[mechanisms/the-firms-view]] — firm incentives against legibility
- [[artificial-shoppers-attention-competition]] — 2026-11-09 weekly-brief cross-ref
- [[generative-search-brand-bias-audit]] — 2026-11-09 weekly-brief cross-ref
- [[clear-human-web-blind-token]] — 2026-11-09 weekly-brief cross-ref
