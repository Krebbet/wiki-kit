# Ghost Tool Calls

Tool-augmented LLM agents speculatively pre-issue likely future tool calls (web search, API queries, etc.) to hide latency before the user commits to a decision branch. These "ghost tool calls" disclose inferred user intent to external services before any user authorization — and before the agent even confirms it will take that branch. Because every external observer that received a ghost call retains the disclosure after the agent abandons the branch, no commit-time cleanup, read-only restriction, or access-control allow-list can unsend what was already transmitted. The paper formalizes this attack surface for the first time and proposes a runtime abstraction — Speculative Tool Privacy Contracts — that treats observation before commitment as a distinct, first-class privacy effect.

## Source

- [Ghost Tool Calls: Issue-Time Privacy for Speculative Agent Tools](https://arxiv.org/abs/2606.02483) — Mohammadi, Klein, Arora & Bindschaedler (arXiv:2606.02483 [cs.CR], submitted 1 Jun 2026). Origin: academic security/privacy research (cs.CR + cs.AI + cs.CL). Intended audience: agent-systems and privacy researchers; LLM agent platform builders. Purpose: first formalization of ghost tool call privacy leakage; propose and prototype a mitigation. Trust: high — peer-reviewed submission with a working prototype and empirical evaluation.

## The Mechanism: Speculative Dispatch

Modern LLM agent runtimes use speculative execution to reduce perceived latency: the agent predicts which tool calls it will need given a tentative reasoning branch and issues them in advance, before committing to that branch. If the branch is abandoned, the agent discards the results — but the external services that received those calls have already observed the arguments.

The paper's core observation: **timing is the issue, not authorization.** The speculative call is issued by an authorized agent on behalf of an authorized user; the problem is that the *content* of the call encodes the user's intent at a moment when the user has not yet chosen (or may never choose) that path. External services — web search engines, third-party APIs, ad-serving infrastructure — receive a signal about user intent that the user never explicitly authorized.

After the branch is abandoned, nothing can retroactively suppress the disclosed intent. Post-hoc filters and access-control lists operate on what the agent *keeps*, not on what external observers already *hold*.

## Privacy Harm

Ghost calls produce **pre-authorization intent disclosure** to third-party services. The practical impact:

- A web search issued speculatively on a branch the user ultimately rejects still transmits the search query to the search provider, potentially with session identifiers.
- API calls to pricing, recommendation, or data-broker services expose user interest signals before the user has decided whether to proceed.
- The speculative path is by design the *likely* path — so ghost calls carry real predictive signal, not noise.

The paper reports that speculative dispatch measurably increases what an external observer can infer about user intent relative to a non-speculative baseline. This is not a theoretical concern: the intent-leakage is real and quantified across three corpora.

## Scope: Which Services Receive Ghost Calls

The paper evaluates tool calls to web search, general-purpose APIs, and services that would be invoked by assistant-style agents (the paper does not enumerate specific named services, but the category is any external HTTP endpoint an agent might call). The attack surface expands as agents gain more tool integrations. Consumer-facing agents (shopping assistants, travel booking agents, health information assistants) are the highest-risk deployment context because the intent signals are commercially valuable and the users are non-technical.

## Proposed Mitigation: Speculative Tool Privacy Contracts

The paper introduces **Speculative Tool Privacy Contracts** as a runtime abstraction. The key design choice: treat *observation before commitment* as a distinct effect, separate from state mutation. Existing runtime primitives (read-only restrictions, rollback) handle mutation effects; they do not handle disclosure effects. The contract abstraction addresses disclosure at the point of issue, before dispatch.

Twelve policies are evaluated across three corpora. Only **issue-time policies** that modify or suppress the speculative call before dispatch reduce observer inference. Three classes of issue-time policy:

- **Defer** — delay dispatch until the branch commits; ghost calls are suppressed entirely for deferred tools. Eliminates leakage at the cost of the latency benefits that motivated speculative execution.
- **Anonymize** — alter the argument or destination projection before dispatch (e.g., strip identifying query terms, generalize the query, route through a proxy). Trades signal fidelity for leakage reduction; effectiveness depends on the generalization strategy.
- **Block** — refuse to issue the call speculatively; require explicit user confirmation before any dispatch. Maximum privacy, maximum friction.

The paper implements these contracts in a prototype runtime. Post-hoc filters, read-only restrictions, and access-control allow-lists are tested and confirmed ineffective — they do not reduce inference because they operate after disclosure has already occurred.

## Code / Artifact Status

The paper mentions a prototype runtime implementation used for evaluation. No public repository is linked in the arXiv submission metadata. Code availability status: unknown as of capture date (2026-06-15). This is a first-submission preprint; artifact availability may improve if the paper proceeds through peer review.

## Why This Matters for Consumer Counter-Power

*(editorial / synthesis)*

Ghost tool calls are a new extraction surface that existing counter-power framing does not address. As LLM agents become consumer-facing intermediaries — shopping assistants, price comparison agents, health advisors — the speculative execution optimization that makes them feel fast also makes them intent-disclosure channels. The services receiving ghost calls are often the same services whose behavior this wiki tracks: search engines, pricing APIs, ad-serving infrastructure, data brokers.

Several specific concerns for the wiki's framing:

- **Consumer agents as extraction vectors.** A shopping agent that speculatively queries a retailer's pricing API to hide latency reveals the user's product interest before the user has decided to buy. The retailer (or the retailer's pricing vendor) receives an intent signal they can act on — surge pricing, targeted ad retargeting, data sale — without the consumer having authorized any of it.
- **Authorization theater.** The user authorizes the agent to call external services on their behalf. Ghost calls technically operate within that authorization. But the user's mental model of authorization is commit-time, not issue-time. The gap between "I authorized this agent to search for me" and "this agent already searched before I decided to search" is the new exploitation surface.
- **No existing counter-power tool addresses this.** [[dsar-and-data-deletion]] assumes data was collected at the point of explicit action; ghost calls generate pre-action disclosures that may not be surfaced in DSAR responses. [[transparency-tools]] rely on after-the-fact audit; ghost call disclosures happen before any user-visible event. [[decentralized-agent-identity]] addresses agent authorization but not the timing of tool dispatch within an authorized session.
- **The mitigation requires platform cooperation.** Issue-time policies have to be implemented in the agent runtime, not by the consumer. This is a platform-layer fix, not a user-layer fix. Until agent runtimes ship Speculative Tool Privacy Contracts (or equivalent), consumers using LLM agents have no mechanism to prevent ghost call leakage.
- **Regulatory gap.** Ghost calls do not fit cleanly into existing GDPR/CCPA frameworks, which are designed around user-authorized data collection. The paper does not analyze the regulatory dimension, but the intent-disclosure-before-authorization fact pattern likely falls in a grey zone analogous to the one [[browser-fingerprinting]] occupies for cookieless tracking.

## Related

- [[adversarial-prompt-injection-defense]] — related AI privacy defense mechanism; prompt injection is a distinct attack vector but shares the "agent as attack surface" framing
- [[decentralized-agent-identity]] — agent authorization framework; addresses who can call what, but not when within an authorized session
- [[transparency-tools]] — visibility into agent behavior; current tools operate post-hoc and would not surface pre-commit disclosures
- [[browser-fingerprinting]] — intent leakage analog; fingerprinting discloses user state to third parties without explicit authorization, structurally similar to ghost call disclosure
- [[the-firms-view]] — counter-perspective; firms (search providers, pricing APIs, retailers) receive commercially valuable intent signals from ghost calls and have no incentive to suppress them
- [[dsar-and-data-deletion]] — data rights context; DSAR frameworks are designed for explicit-collection events and may not capture pre-authorization disclosures
- [[agent-interop-protocols]] — agent interaction protocols; speculative dispatch is a runtime optimization decision in the protocol layer
