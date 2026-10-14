# Personal Agent Protocol (Sierra / Meta, 2026-10)

Sierra and Meta are developing Personal Agent Protocol, an "open standard" for how personal AI agents authenticate with businesses and what those businesses let them do. Announced 2026-10-07 (TNW, citing a Sierra post by Bret Taylor and Clay Bavor) with partners Genesys, Instinct, Rocket, Shopify, Stripe and Walmart. A v0.1 spec is due in October 2026; payments are a future extension, not in scope. Stripe and Shopify also sit in Visa's rival Trusted Agent Protocol, so the two efforts overlap rather than split the field. Single-source, secondary coverage; spec not yet published.

## What it does

- Defines authentication of personal agents to businesses, and gives companies visibility into what agents do on their sites (2026-10-07).
- Guest-to-signed-in flow: an agent starts as guest (check stock, returns policy); after customer sign-in, the customer picks read-only or write access. Session persists across channels, so pre-login questions and post-login order changes are one visit.

## Techniques

- Sessions built on OAuth.
- Company chooses the integration surface: its website, its APIs via standards such as MCP and OpenAPI, or an agent of its own.

## Deployment

- Spec: v0.1 due "later this month" (October 2026). Not published as of capture; nothing to implement yet.
- Named use: Rocket's statement describes Meta's Muse agent moving from home search to arranging financing; Muse launched about four weeks before 2026-10-07 and pays with saved cards through Stripe's Link.

## Costs

Not specified in source.

## Limits

- Payments are a listed future extension, not in v0.1. Push notifications and more detailed permissions are also future work.
- Strong customer authentication (EU PSD2) has no carve-out for software-approved payments; source flags this as a gap for European rollout. No European retailer, bank or payment company is named as a partner; Stripe (dual San Francisco/Dublin HQ) is the only partner with European headquarters.
- Governance, conformance and licensing of the "open standard": not specified in source.

## Reception

- TNW framing (2026-10-07): agents are "arriving faster than the arrangements they will work under." Hark released a groceries/bookings/bills agent the same day, a year ahead of its hardware.
- Rival: Visa's Trusted Agent Protocol (Microsoft, Stripe, Shopify, Worldpay joined; Visa plugged into ChatGPT in June 2026, about 175 million merchants, per TNW). Stripe and Shopify are in both.
- *(editorial)* Meta/Sierra address identity and permissioning on the merchant side while Visa's is payments-led; Stripe and Shopify hedging suggests convergence or layering is likelier than a winner-take-all fight. This is the consumer-agent counterpart to the enterprise identity category in [[agent-identity-governance-2026-09]], and an OAuth/MCP-based alternative to the agent-protocol politics in [[google-a2a-agentic-foundation-2026-08]].

## Source

- raw/research/weekly-2026-10-07/07-personal-agent-protocol.md (TNW, captured 2026-10-07)

## Related

- [[agent-identity-governance-2026-09]]
- [[sierra]]
- [[google-a2a-agentic-foundation-2026-08]]
- [[agentcore-payments-x402-2026-05]]
- [[stripe-openrouter-acquisition-2026-08]]
