# Microsoft Foundry agent harness, September 2026

Microsoft's September 2026 Foundry roundup (vendor first-party, captured 2026-10-28) moves Routines, Tool Search and A2A to GA, and puts Insights, hosted-agent resilience, voice agents and prompt-agent Toolboxes into public preview. The most reusable content is the worked pipeline and its design rules: lazy tool loading, a three-state job lifecycle, code-owned recipients. Verdict: watch, and borrow the patterns now. Every claim below is vendor-stated; there is no third-party validation and no market reception in the source (0 comments). The identity-lifecycle item carries no maturity label.

## What shipped (all dates 2026-09 unless noted; vendor-stated)

- **Routines, GA (announced 2026-09-24).** One trigger starts one agent. Triggers: timer, recurring schedule, GitHub issue event, or a supported Teams channel event. Configuration, identity and run history stay with the Foundry project. The agent-scheduled reminder tool is still preview. Stated limits: Routines are not multi-agent orchestration or approval workflows. The author's demo used a manual dispatch, so it is not proof of a calendar-triggered run.
- **Tool Search, GA (2026-09-24).** A Toolbox exposes `tool_search` and `call_tool` instead of placing every tool definition in each request. Hosted-agent Toolboxes were already GA; prompt-agent Toolboxes are public preview. The source concedes its demo "proves discovery; it doesn't measure token savings", so the savings are unmeasured.
- **A2A, GA** in Foundry Agent Service (2026-09-24). See [[landscape/google-a2a-agentic-foundation-2026-08]] for the protocol's governance background.
- **Insights, public preview (2026-09-24).** Groups recurring trace behaviour into findings with evidence, likely causes and proposed fixes. Example findings: sample-heavy prompts after a batch was ruled out, large prompts resubmitted after rate-limit errors, an unconfirmed delivery receipt. Scans are billable.
- **Hosted-agent protocols.** A hosted agent can expose several external protocols: Responses, Invocations and Activity. The source says protocol choice follows the caller contract, not the framework (Copilot SDK, Microsoft Agent Framework).
- **Resilience, public preview.** Long-running hosted-agent work uses background responses that are recoverable after client disconnect. Foundry Toolkit 1.6.11-1.6.14 adds reconnect to unfinished background responses and steer/stop controls. Stated caveat: reconnecting does not make repeated external actions safe, so application checkpointing and idempotency still matter.
- **Voice agents in Agent Service, public preview**, distinct from the earlier Hosted Agents with Voice Live integration (July/Aug edition).
- **Model Router, preview.** Session affinity for related Chat Completions requests (prefers the same model, not guaranteed), routing metadata, 32 regions.
- **Tooling churn.** `azd` extension `azure.ai.agents` beta.18 (2026-09-30) requires runtime definitions in `azure.yaml` or an explicit `$ref`, rejects legacy AgentManifest discovery, and needs azd 1.34.2+. Renamed commands, removed deploy commands and moved `beta.voiceAgents` operations are a maintenance and lock-in cost signal for beta surfaces.
- **Not yet released.** Rubric evaluation, dataset generation and Agent Optimizer GA were only targeted for "later this month" (October 2026). That is an announced target, not a completed release.

## Identity lifecycle caveat

Routines carry identity with the project, and the Python/Java SDKs add "routine dispatch identity" and "routine authorization" arguments (2026-09). Separately, "Entra and Agent 365 lifecycle operations" were confirmed available by 2026-09-24 with **no maturity label** in the announcement (GA/preview unstated). The source's own advice: verify that an approved lifecycle change to a non-production agent affects its runtime, not just its directory record. Treat this as unverified until tested. The Azure Local extension (2609, preview) enables Kubernetes service-account-token auth by default for in-cluster inference (short-lived, audience-bound; control-plane requests not covered). A related warning on memory providers: do not treat a user ID in a prompt as an authorization decision. Category context: [[landscape/agent-identity-governance-2026-09]].

## Pricing policy (effective 2026-09-01)

Standard deployment premiums apply only to models launched on or after 2026-09-01. Affected EU Data Zone and non-US Regional PTU customers see increases on existing deployments too. Global pricing is unchanged; APAC Data Zone becomes available. Hosted agents bill separately. Default Azure Monitor trace sampling in AgentServer Core is 100%, so review trace volume and cost. **No GPT-6 prices are recorded here:** the source's price table was garbled; the source only says long-context rates are higher. For OpenAI-side list prices see [[landscape/agentic-compute-pricing-2026-04]] and [[landscape/openai-devday-dots-gpt61-sol-2026-09]].

### Model naming discrepancy

The source lists GPT-6 Astra (released 2026-09-22), GPT-6.1 Sol (2026-09-29) and GPT-6 Luna (2026-09-22) as GA on Foundry, each with a 1.05M context window and up to 128K output tokens, and calls "GPT-6 Sol" the predecessor of 6.1 Sol. The wiki index and [[landscape/agentic-compute-pricing-2026-04]] speak of "GPT-6 Sol" and Luna (launched 2026-09-22). The source adds Astra and 6.1 Sol and claims 6.1 Sol improves coding, computer use and professional work at the same uncached prices as GPT-6 Sol, with 50% lower cached-input pricing (vendor claim, 2026-09). Not a contradiction, but the index naming should be reconciled against the OpenAI pages; the source's table cannot settle it. GPT-6.1 Sol tool calls require Responses.

## Worked pipeline in the source

A Routine starts a producer hosted agent (`depend-agent`, GitHub Copilot SDK). It hands off via authenticated Invocations (`start`/`status`/`result`) to a receiver (`maf-update-agent`, Microsoft Agent Framework) that delivers an Adaptive Card to Teams via native Activity. Model Router supplies inference only. The tool example uses seven GitHub read operations, further restricted in app code to approved repositories, paths and PR-read methods. A missing required tool fails explicitly rather than returning an empty result. Reports and source baselines have a 90-day lifecycle. One author-built workflow is the only demonstration of the GA claims.

## Techniques worth stealing

- **Discovery is not permission.** Lazy tool loading via `tool_search` plus `call_tool`, with scoping enforced in application code, not by the discovery layer.
- **Three-state job lifecycle.** Persist the job before acceptance; accepted does not mean finished, finished does not mean delivered. A lost acknowledgment stays "uncertain" for review and is not blindly replayed; receipts are adopted rather than resent.
- **Code-owned recipient.** A fixed destination allowlist the model cannot override.
- **Dark-launch schedules.** Start in manual no-send mode; enable only after the delivery path is verified.
- **Trace capture with content off by default**, plus on-demand trace-derived insights that propose fixes but never auto-apply.
- **Source ledger plus coverage-gap retention** for generated reports.
- **Reuse a session ID across related turns** for prompt-cache affinity (not guaranteed).
- **Fail loudly on a missing required tool.**

## Build vs buy

Routines are pitched as "useful automation without a separate scheduler"; Toolboxes and Insights pull scheduling, tool routing and trace analysis into the platform. Approval workflows and orchestration are left to the user. Buy the scheduler and tool-routing if already on Azure; build the idempotency, delivery and authorization layers regardless. Comparable managed stacks: [[landscape/aws-bedrock-agentcore-june-2026]] (Runtime, Identity, Gateway, Observability) and the scheduled-agent pattern in [[platforms/workday]]. The June precursor (agent control tower, Scout) is in [[landscape/microsoft-build-2026-06]].

## Source

- `raw/research/weekly-2026-10-28/04-microsoft-foundry-sept-oct-2026.md` - Microsoft Foundry Blog, "What's new in Microsoft Foundry | September 2026", captured 2026-10-28. Vendor first-party; the author runs "The Handoff" weekly show.
- Derived summary: `raw/research/weekly-2026-10-28/.ingest/04-microsoft-foundry-sept-oct-2026.summary.md`

## Related

[[platforms/microsoft]] [[landscape/microsoft-build-2026-06]] [[landscape/agent-identity-governance-2026-09]] [[landscape/aws-bedrock-agentcore-june-2026]] [[landscape/google-a2a-agentic-foundation-2026-08]] [[landscape/agentic-compute-pricing-2026-04]] [[landscape/openai-devday-dots-gpt61-sol-2026-09]] [[landscape/openai-microsoft-restructure-2026-04]] [[platforms/workday]]
