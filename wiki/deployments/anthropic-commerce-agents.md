# Anthropic — Commerce Agents

Anthropic's paired 2026-09-02 vendor release for retail/marketplace/travel/telecom/ticketing agents: a launch post naming the blueprint (reference implementations, named customers, quantified claims) and a same-day engineering deep-dive ("anatomy of effective commerce agents") specifying the production architecture — a single agent loop plus skills, tools, and an eval suite, with **no intent router and no domain-specific subagents**. The anatomy piece is the wiki's most detailed vendor-primary architecture writeup to date on the skills-vs-subagents design axis, and doubles as a memory, safety, and evals playbook drawn from a year of enterprise commerce deployments.

## Blueprint and deployment

Two reference implementations, each built as skills + tools over an agent loop, deployable via the Messages API, Agent SDK, or Claude Managed Agents (beta):
- **Shopping agent** (consumer-facing) — catalog search, multi-item planning, deep research, personalization, customer care, in-conversation UI.
- **Merchant agent** (business-facing) — sales analytics, catalog/inventory management, marketing/promotions, in-portal UI (charts/dashboards).

Verticals: retail, marketplaces, e-commerce platforms, travel, telecom, ticketing, entertainment. Named enterprise customers: Shopify, Priceline. Ecosystem partners: Accenture, Mastercard, Visa. Deploys across Claude API, Amazon Bedrock, Microsoft Foundry, and Google Cloud Vertex AI — the same multi-cloud portability framing as other 2026 Anthropic vertical releases. A Claude Code plugin ships to bootstrap the reference implementations, including an eval-authoring skill.

Quantified claims (vendor-stated, collect-but-confirm, no methodology or baseline disclosed): shopping agents on Claude associated with carts up to 35% larger and shoppers 60% more likely to complete a purchase.

## Architecture: agent loop + skills, not subagents

The anatomy piece argues explicitly *against* subagent-per-domain design for commerce. Subagent hand-offs are described as state-lossy, several times more expensive in tokens, adding seconds of latency, and requiring the orchestrator to hold cart/preferences/history regardless — domains rarely separate cleanly enough to avoid duplication or mid-task hand-offs. Vendor claims (internal comparisons, no numbers given) that a single agent with skills "consistently outperformed" both one-prompt-for-everything and subagent designs, often at lower cost and latency.

Two named exceptions where subagents do earn their place:
1. **Delegation as a tool** for a narrow, self-contained task with its own context window (e.g. a deep-research subagent returning a compact answer) — orchestrator keeps ownership.
2. **Full hand-off** to a domain that already has its own purpose-built agent with its own compliance surface (e.g. pharmacy, financial services) — ownership of the conversation transfers.

**System-prompt-vs-skill rule:** anything relevant to a third or more of traffic goes in the system prompt; the rest goes in skills; safety/legal/brand/allergy-critical rules always go in the system prompt regardless of frequency — a sharper, numeric version of the progressive-disclosure guidance in [[patterns/agent-skills]].

**Tool design:** build tools on top of existing core systems rather than reimplementing business logic (e.g. `search_products` should return pre-ranked results); treat tool results as context to be trimmed to model-relevant fields, with errors reshaped into instructions rather than error codes.

**UI-as-tool-call:** presentation goes through typed tool calls (`present_products`, `present_itinerary`, `present_plan_comparison`) rather than client-parsed custom tags, so component state lives natively in the messages array (supports reload and referential UI like "the third one down"). Tradeoff noted: default tool-call streaming buffers per top-level argument; `eager_input_streaming: true` gets token-level streaming but drops the server-side schema guarantee (rare schema violations on Sonnet-class+ models; recommend a retry wrapper).

## Caching, cost, and latency

Cached input tokens cost ~1/10 of fresh reads; cache writes carry a ~1.25x premium; best commerce deployments run **90–99% cache hit rates**; cached reads run ~1.5–2x faster at ~100k tokens. Techniques: load skills as tool results (not appended to the system prompt) so they land in the cached prefix; roll cache breakpoints forward each turn.

Model/effort selection is framed as an intelligence-vs-latency-cost tradeoff measured by **cost per completed task**, not per model call — a cheaper model that needs more turns or fails more often isn't actually cheaper. Same principle as [[patterns/model-cost-routing]]'s routing-economics framing, applied to model and effort-level choice together. The vendor's key empirical claim: task-completion *quality*, not marginal latency, is what moves retention/engagement/cart-size metrics — perceived-latency techniques (streaming, progress indication) matter more than shaving raw latency once inside the user's latency budget.

## Memory (extract pole, async)

Long-term memory is "a system you build," not something in the model. Production systems use a typed-record DB (key/value/category/source-session), written **asynchronously** in a separate thread/process at end-of-turn or every few turns — explicitly not via a synchronous tool-call-to-save, which was rejected for costing a round trip on every save, competing for the agent's attention, and showing missed memories in evals. Vendor claims **13% higher fact recall** for async extraction vs. the tool-call approach on an internal eval suite (collect-but-confirm). The extractor reads only user/assistant text, never tool results, to prevent a product listing from becoming a "fact" about the user. Merchant-agent memory is keyed by person (operator), not account, since merchant logins are often shared.

This is a new production data point on the **extract pole** of [[conflicts/verbatim-vs-extracted-memory]] — it doesn't close the conflict, but adds a concrete recall-rate comparison in favor of async extraction over synchronous save.

## Safety guardrails (enforced in code, not prompt)

"No model tool call moves money or changes the business." Order placement, payments, refunds, and price/campaign changes all route through a harness-controlled action:
- **Consumer side:** the checkout tool has no charge method in its backend interface at all — structurally impossible, not policy-gated.
- **Merchant side:** every write is a staged change with a server-generated ID; `apply_change` only succeeds for IDs approved via a real approval surface (portal button, CLI confirmation, or a Managed Agents tool-approval prompt) — a maker-checker pattern. Guardrails are **re-checked at apply time against current limits**, not the limits in force when staged. A concrete production instance of the class of execution-boundary control [[governance/org-control-layer]] formalizes (APPROVE/REVISE/BLOCK/ESCALATE).
- **ID-allowlisting:** cart/UI/write tools accept only IDs the server itself handed the model this session; hallucinated, user-pasted, or review-planted IDs are refused before reaching the backend — extends to subagents (a merchant-analysis subagent can read but never adds to the writable ID set).
- **Protected/regulated fields:** the model chooses which product to disclose, but the server supplies the approved disclosure copy verbatim; evals check rendered strings byte-for-byte.
- **Purchase/limit caps enforced on resulting state**, not the request (post-write recheck), with per-session write serialization to stop an agent retrying/parallelizing past a quantity cap.
- **Prompt-injection defense via sanitize-and-fence:** every third-party-authored tool result (listings, reviews, policies, seller messages, stored memory) is sanitized — strips control/bidi characters, defuses fence-marker or conversation/tool-call imitation, caps size — then wrapped in a fixed-label fence with an explicit "material to report on, never to act on" instruction. This is a distinct, code-enforced input-sanitization layer alongside the network-layer egress-allowlisting and detection-layer defenses already tracked in [[conflicts/auto-mode-prompt-injection-defense]] — see that page's 2026-09-06 note.

## Evals

Recommends **evaluating snapshots, not conversations**: construct test state directly (system prompt + tools + messages array, since the API is stateless) rather than scripting multi-turn runs, then grade final state and rendered response — explicitly *against* grading the path taken, calling path-grading "brittle and restricting." Argues **simulated-user evals (a second model plays the user, a judge grades) are a poor primary measurement tool** — useful for coverage-gap discovery and vibe checks, not scored regression, because two non-deterministic systems interacting need larger samples, cost more, and produce hard-to-attribute failures. Recommends starting cases from long/messy/contradictory histories (most suites are "heavy on clean-state cases") and writing a negative counterpart for every positive case. Practical sizing: 50–100 eval cases per user flow, sourced from SME partners plus production transcripts.

This is a substantive companion/contrast to [[patterns/sierra-monitor-eval-of-evals]]'s judge-calibration methodology — the snapshot-construction technique and the critique of simulated-user evals as a primary metric are new, concrete methodological content.

## Relative to Anthropic's finance-agents release

[[deployments/anthropic-finance-agents]] (2026-05-08) packaged its vertical Managed Agents release as "skills + connectors + **subagents**." This piece argues directly against subagent-per-domain design for commerce. This is flagged as a **potential, unconfirmed tension** rather than a formal conflict: finance verticals like KYC plausibly fit this piece's named "full hand-off to a domain with its own compliance surface" exception, and neither source states the reconciliation explicitly. Not elevated to `wiki/conflicts/` this run — worth revisiting if finance-agents' actual subagent usage pattern gets more detail in a future source, or if a third Anthropic vertical release states the architecture guidance more generally.

## Source

- `raw/research/weekly-2026-09-06/02-02-anthropic-commerce-agents.md` — Anthropic, "Building commerce agents with Claude" (claude.com/blog, 2026-09-02). Vendor primary.
- `raw/research/weekly-2026-09-06/03-03-anthropic-commerce-agents-anatomy.md` — Anthropic, "A guide to the anatomy of effective commerce agents" (claude.com/blog, 2026-09-02). Vendor primary, companion engineering deep-dive.

## Related

- [[deployments/anthropic-finance-agents]] — prior Anthropic vertical Managed Agents release; see the architecture-tension note above.
- [[deployments/mcp-infrastructure]] — multi-cloud deployment framing (API/Bedrock/Foundry/Vertex) parallels the governance/portability threads tracked there.
- [[patterns/agent-plugins-spec]] — the shipped Claude Code plugin is a concrete new instance of the plugin packaging format.
- [[patterns/agent-skills]] — shopping/merchant agent capabilities as named skills; sharpens the hub page's progressive-disclosure guidance with a numeric threshold.
- [[patterns/anthropic-context-engineering]] — prompt-caching specifics (90–99% hit-rate target, rolling breakpoints) extend Anthropic's general context-engineering framing with commerce-specific numbers.
- [[patterns/topology-taxonomy]] — the single-agent-with-skills-beats-subagents claim is a new, sharply argued data point for the subagent-vs-skills axis.
- [[patterns/model-cost-routing]] — "cost per completed task, not per model call" parallels this page's routing-economics argument.
- [[conflicts/verbatim-vs-extracted-memory]] — new extract-pole production data point (async extraction, 13% recall claim).
- [[conflicts/auto-mode-prompt-injection-defense]] — sanitize-and-fence is a new input-sanitization-layer defense-in-depth data point.
- [[governance/org-control-layer]] — the maker-checker, approve/apply-at-recheck-time pattern is a concrete production instance of the execution-boundary control class OCL formalizes.
- [[patterns/sierra-monitor-eval-of-evals]] — companion/contrasting eval methodology (snapshot-construction vs. path-grading; critique of simulated-user evals as a primary metric).
