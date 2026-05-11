# Sierra — Context Engineering for Agents (2026-05-05)

Sierra's engineering blog defines "context engineering" as the discipline of deciding which information blocks reach a model, and exactly when — using explicit runtime conditions to gate each block. The post argues this supersedes rigid flow-based agent design for production-scale agents, and introduces an eight-type block taxonomy with progressive disclosure as the load-bearing mechanism. Authored as a vendor primary source; the architecture is Sierra's own platform framing, not an independent evaluation.

## Source

- Sierra Engineering Blog, "Context engineering: the key to great agents," 2026-05-05 — `raw/research/weekly-2026-05-08/02-sierra-context-engineering.md`. Authored by Sierra. Primary practitioner / vendor source.

## Era framing: prompt → flow → context

Sierra proposes a three-era periodisation of customer-facing agent architectures:

**Era 1 — IVR.** No reasoning. Deterministic menu trees. Customer issues that don't match a menu branch are unresolvable.

**Era 2 — Flow.** Current dominant pattern. Customers speak naturally; the system still operates on predefined decision trees or digitised SOPs. Escalation handles out-of-scope cases. Management complexity scales super-linearly with the number of SOPs: *"as more SOPs are added, the system becomes harder to manage, increasing the risk of errors."*

**Era 3 — Context engineering.** Agents are *goal-guided and guardrail-constrained*, not path-driven. The model drives the conversation; Sierra's platform supplies context dynamically based on runtime state. Sierra identifies this as the architecture of today's most sophisticated agents.

The framing is normative — Era 3 is presented as strictly superior to Era 2 — though see [Internal tension flagged](#internal-tension-flagged) below.

## The eight context types

Sierra's platform structures agent context into eight named block types, each independently conditioned:

| Block | Purpose |
|---|---|
| **Journey** | A goal the agent knows how to pursue (e.g., dispute a charge, file a claim). Each journey carries a trigger condition and an expected outcome. |
| **Tool** | An interface to an external system (pull an itinerary, process a refund). Tool availability is gated — account-specific tools activate only after authentication. |
| **Rule / Policy** | Business logic and guardrails expressed in natural language (e.g., *"Premium cardholders waive foreign transaction fees."*). Conditioned on customer segment or product context. |
| **Workflow** | Step-by-step sequences for situations that genuinely require a fixed order — regulated intake, multi-step verification. See tension note below. |
| **Knowledge** | Help-centre articles, product docs, FAQs, internal policies — retrieved on demand rather than pre-loaded. |
| **Memory** | Customer history: past conversations, preferences, prior issues. Injected once identity is confirmed. |
| **Glossary** | Business-specific terminology — product names, plan tiers, internal jargon — surfaced to disambiguate customer language. |
| **Response phrasing** | Brand voice and tone. |

*Source: "Types of context" section; block descriptions are Sierra's own.*

## Progressive disclosure as the load-bearing mechanism

*"As the number of tokens in a model's context window grows, its ability to recall and act on that information accurately declines. Every irrelevant token competes for the model's attention with the tokens that actually matter."* (Sierra, "Progressive disclosure" section.)

The solution: provide only the minimum most-relevant information at each conversational moment. This is progressive disclosure — a runtime policy, not a static prompt design.

**Conditions are the connective tissue.** Each context block carries an associated condition that governs its injection. Condition types:

- *State-based*: a tool returned specific data, the customer authenticated, a subscription record loaded.
- *Observation-based*: the customer mentioned a topic, expressed cancellation intent, asked about a specific product.

When a condition is met, the associated block is injected. Until then, it is withheld.

**The layering pattern in practice:**

1. Conversation opens minimal — basic tools, general policies, brand voice only.
2. Customer authenticates → account-specific tools and policies become available.
3. Customer mentions a charge dispute → dispute workflow, investigation tools, relevant policy blocks are injected.
4. Customer confirms shipment to Germany → Germany-specific shipping rules injected; other country rules remain withheld.

Each state transition unlocks exactly what is needed for the next step. The result is a context window that grows purposefully, not indiscriminately.

**Claimed outcomes** (vendor-stated): reduced hallucination, improved naturalness, eliminated inference cost on irrelevant tokens, and improved manageability at scale.

**Scale threshold:** Sierra states an agent handling five journeys can tolerate loose context management; an agent handling fifty *requires* this discipline — loose management degrades the model experience at production scale.

**Future-proofing claim:** *"When you hardcode logic, you constrain the model — it can only be as capable as the paths you've predefined. With context engineering, the agent can reason more freely. As new, more capable models are released, your agent inherits that improvement."* (Sierra, "Why this matters" section.) This is a platform-positioning argument; no controlled evidence is cited.

## Internal tension flagged

Sierra's Era 2 framing characterises flow-based designs as categorically inferior — agents that *"still operate on 'if this, then that'"* — yet Sierra's own **Workflow** block type is, by definition, a flow: a step-by-step sequence for situations requiring a specific order.

Sierra explicitly acknowledges this: *"While we just discussed why rigid flows are limiting, some situations (like a highly regulated intake process) genuinely require them. The difference is that a workflow becomes just another piece of context made available when conditions are met, rather than the organizing paradigm for the entire system."*

The distinction Sierra draws is:
- **Bad**: flow as the *organising paradigm* of the whole agent (omnipresent, unconditional).
- **Acceptable**: flow as a *conditioned context block* (activated only when state warrants it).

This distinction is architecturally coherent but partially deflates the rhetorical force of the Era 2 critique. The Workflow block is a flow; the claim is that conditioned availability changes its character. Whether the attenuation of the criticism is substantive or primarily reframing is not resolved by the source. This is an internal source tension, not a cross-wiki conflict.

## Notable claims

- Progressive disclosure reduces hallucination and improves naturalness by eliminating irrelevant tokens from the context window. *(Vendor-stated; no controlled evaluation cited.)*
- At 50+ journey scale, context engineering is required, not optional. *(Vendor-stated.)*
- Sierra's **Ghostwriter** tooling auto-generates context blocks and conditions by ingesting SOPs, call transcripts, and documentation. *(Platform capability claim.)*
- Context engineering "future-proofs" agents: better models amplify returns from well-engineered context without requiring logic re-hardcoding. *(Vendor-stated; no evaluation cited.)*
- Token efficiency: unnecessary inference cost is eliminated — *"you aren't paying to process a thousand tokens of baggage policy during a simple flight rebooking."* *(Operational cost framing.)*

## Related

- [[patterns/context-engineering]] — extends with concrete eight-block taxonomy and progressive-disclosure mechanism; Sierra is a primary vendor articulation of context engineering as a named discipline.
- [[patterns/agentic-context-engineering]] — adjacent; Sierra's conditional block injection is a practitioner instantiation of agentic context engineering concerns.
- [[patterns/effective-harnesses]] — alternative harness architecture (Anthropic's initializer + coding-agent pattern) vs Sierra's condition-gated block system; both address the "right information at the right time" problem, differently.
- [[patterns/topology-taxonomy]] — progressive tool disclosure mitigation class ([[case-studies/notion-token-town]]) extends directly to Sierra's context-block disclosure; Sierra adds the *conditions* mechanism as the formal gating layer.
- [[case-studies/notion-token-town]] — Notion's 100+ tools with progressive disclosure is an independent empirical parallel; both arrive at condition-gated context injection, Notion from pragmatic scale pressure, Sierra from platform design.
- [[patterns/externalization-survey]] — Sierra's eight block types fit neatly into the externalization survey's memory + skills + protocols + harness vocabulary; corroborates that taxonomy at the practitioner level.
- [[patterns/codified-context]] — three-tier hot/cold architecture is structurally related; Sierra's eight-type taxonomy provides finer-grained named distinctions within the cold-layer.
- [[patterns/agentic-harness-engineering]] — AHE evolves harnesses via observability loops; Sierra's Ghostwriter evolves context blocks from SOPs/transcripts — parallel approaches to auto-generation of agent context structure.
- [[deployments/openai-symphony]] — Symphony's agents.md TOC + session-log distillation is a different (static + distilled) approach to the same context-management problem Sierra solves dynamically; direct architectural contrast.
- [[patterns/sierra-monitor-eval-of-evals]] — companion Sierra post (2026-05-07). Context engineering is the build-phase architecture; Monitors is the observe-phase eval layer. Both belong to one Sierra platform narrative.
- [[patterns/direct-corpus-interaction]] — boundary case: Sierra's *Knowledge* block is right for cloud/SaaS knowledge bases (centralised, stable corpus); DCI argues that for agent-resident corpora (local files, project workspaces), the right primitive is direct substrate access rather than a Knowledge block.
