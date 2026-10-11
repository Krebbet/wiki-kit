# Personal Agent Protocol (PAP) — Sierra and Meta

Sierra announced the Personal Agent Protocol (PAP) on 2026-10-06: a proposed open standard, co-developed with Meta and several commerce and customer-service partners, for how a consumer's personal agent authenticates with and acts on a business's website, APIs or company agent. **Announcement-stage**: the v0.1 spec, design workshops and a reference implementation are promised for later in October 2026 and nothing is released. The source is a vendor blog with no benchmarks, so every capability claim is vendor-stated and collect-but-confirm.

## What was announced

- **Problem framing:** personal agents today drive websites and apps like a human (page loads, form clicks) or fall back to support lines and web chat, which is slow and failure-prone. PAP proposes a direct, authenticated, auditable channel.
- **Stakeholder needs:** consumers want speed and trust, brands want visibility and control (know when an agent acts for a customer and decide what it may do), and agent builders want one consistent integration path.
- **Named actors:** Meta and Sierra develop it. Partners are Genesys, Instinct, Rocket (with Redfin), Shopify, Stripe and Walmart. Pull quotes in the capture are unattributed, so who said what is unknown. Meta is the only personal-agent builder named.

## Mechanism (as described)

- **Discovery** starts on the company website: the agent learns what the company offers and how to reach it.
- **Session:** the agent opens a session for the user. It can start as a guest (product availability, returns policy) and escalate to an authenticated account session. The customer signs in on the company page or reuses credentials set up with their personal agent, and chooses read-only or write access.
- **OAuth-based, cross-channel:** the session is built on OAuth and carries across channels, so pre-sign-in questions and post-sign-in order changes belong to one session.
- **Three routes, chosen by the company:** its website (ordinary web navigation), its APIs ("built on standards such as MCP and OpenAPI"), and its own agent (for conversational tasks such as a warranty claim).
- **Delegation principle:** consumers decide what access their agents get, and companies set parameters for what those agents can do. This is delegated authorization on OAuth, not a new identity primitive.
- **Named future extensions (not v0.1 as described):** finer-grained per-action permissions, push notifications (flight delay, order shipped), and payments extensions that let an agent buy without exposing card details.

## Gaps and caveats

- Nothing is released. "Open for anyone to implement" is a claim until the spec and license are published.
- No threat model, no handling of prompt injection or agent impersonation, no detail on how a company verifies an agent's claimed principal, and none on token format, revocation, liability or consent records.
- No governance body is named beyond Meta and Sierra leading.
- **Vendor-interest caveat:** Sierra sells company-side agents, and the "its agent" route is commercially aligned with that product.
- Open question: how PAP's OAuth session relates to the MCP identity work in [[deployments/mcp-infrastructure]].

## Where it sits in the wiki

- **Protocol taxonomy:** a consumer-to-business entrant, a different scope from the agent-to-tool and agent-to-agent protocols in [[patterns/agent-communication-protocols]]. MCP is named only as one possible API-route standard, so PAP sits around MCP as a session, auth and visibility layer rather than replacing it.
- **Commerce parallel:** [[deployments/anthropic-commerce-agents]] (shopping agent plus merchant reference agent, Shopify in both) is the single-vendor analogue. [[deployments/shopify-simgym]] simulates shopper bots against merchants, and Shopify is a PAP partner.
- **Identity and governance:** [[deployments/microsoft-agent-365]] covers agent identity enterprise-internally, whereas PAP targets customer agents reaching a brand.
- **Sierra's company side:** the "its agent" route would front the agents described in [[patterns/sierra-context-engineering]]. PAP's visibility goal relates to [[patterns/sierra-monitor-eval-of-evals]], and [[governance/sierra-aiuc1-certification]] is Sierra's complementary trust positioning.
- **Meta:** co-developer, see [[coding-agents/meta-muse-code]] for the Muse model family.
- **Externalization:** protocols are one of the externalizations in [[patterns/externalization-survey]]; PAP is a consumer-commerce instance.

## Revisit when

The v0.1 spec ships. The identity, delegation and agent-verification details will decide whether this is a real standard.

## Source

- `raw/research/weekly-2026-10-11/01-sierra-personal-agent-protocol.md` — Sierra blog, "Introducing Personal Agent Protocol", 2026-10-06, https://sierra.ai/blog/introducing-personal-agent-protocol (vendor primary, announcement-stage)

## Related

- [[patterns/agent-communication-protocols]]
- [[deployments/mcp-infrastructure]]
- [[deployments/anthropic-commerce-agents]]
- [[deployments/microsoft-agent-365]]
- [[deployments/shopify-simgym]]
- [[patterns/sierra-context-engineering]]
- [[patterns/sierra-monitor-eval-of-evals]]
- [[governance/sierra-aiuc1-certification]]
- [[coding-agents/meta-muse-code]]
- [[patterns/externalization-survey]]
