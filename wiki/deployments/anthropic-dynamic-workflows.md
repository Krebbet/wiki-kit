# Anthropic Dynamic Workflows ("Flows") for Claude Managed Agents

Anthropic's "dynamic workflows" (called "flows" by the presenters), announced the Friday before AI Engineer New York 2026 and described in a workshop by CJ Avilla and Harrison Stall (Anthropic Members of Technical Staff). A flow is a multi-agent run in which the lead agent plans the work and then writes an orchestration program that launches agents, collects results, and manages information flow, so the model chooses the topology instead of a developer configuring a coordinator plus subagent roster. Stated as "test-time compute for hard problems", at a cost the presenters called "much more" than single-agent. **Collect-but-confirm:** the only source so far is a secondary conference writeup (journalist paraphrase of Anthropic staff, no benchmarks or cost figures); no Anthropic primary doc has been captured.

## Source

- `raw/research/weekly-2026-10-18/05-claude-dynamic-workflows.md` — captured 2026-10-18 from `https://www.latent.space/p/claude-dynamic-workflows` (Latent Space writeup; contains a sponsored Union.ai block that is not content). The title mentions a video, which was not captured.

## Mechanism

- Lead agent drafts a plan, then writes an orchestration program that spawns agents, gathers outputs, and routes information between them. Stall: Claude can "fully orchestrate the entirety of its own multi-agent topology".
- Contrast with earlier Managed Agents, where developers configured a coordinator and a roster of subagents (see [[anthropic-finance-agents]]). Pre-configured specialist subagents can still be passed in the agent config.
- Origin: the "a harness for every task" idea in Claude Code. Available in Claude Console (Managed Agents).
- Demo: a stock-watchlist scanner. A scan phase fans tickers out to agents with isolated contexts; a later review phase checks findings before the report is produced. Shape matches scan-then-review swarms such as [[devin-security-swarm]].
- Motivation: humans becoming the PR-approval bottleneck as agent output grows; the Unix-to-Linux "layers of trusted maintainers" analogy is used to argue agents need comparable organisation.

## Cost and control

- Flows cost "much more" than a single agent but were "much more effective at finding all of the details" (speaker statement, no numbers).
- Agent count is governed by "evals and lower defaults"; ambitious tasks need explicit encouragement to parallelise.
- The model does not know its budget mid-run; developers set a session budget. See [[claude-platform-cost-optimization]] for the broader cost levers.

## Communication and observability

- Subagents share a filesystem and can exchange information through it; there is no API for one workflow subagent to message another directly. The shared filesystem is the channel relevant to back-channel risk in [[multi-agent-turf-war]].
- Console graph view shows the payload the lead passed to each subagent at every transition.

## Self-improvement

- Not built in: a flow cannot rewrite its own next scheduled run.
- Suggested levers: hill-climbing (cf. [[agentic-harness-engineering]]) and "dreaming" (research preview), which reads a memory store plus past session transcripts and emits a reorganised store (merges duplicates, replaces stale or contradicted entries, surfaces new insights). This is a consolidation operation in the sense of [[memory-evolution-survey]].

## Positioning

- Closest structural parallel to RLM-style programmatic orchestration, where the model writes code with loops and dynamic subagents: [[langchain-rlms]].
- Fixed-role counterparts: the coordinator in [[claude-code-projects]] and the thousands-of-subagents Projects coordinator in [[cursor-cloud-agents]].
- Same direction of pushing orchestration into the model as [[openai-gpt-5-6-agentic-primitives]].
- Adds a model-authored topology case to [[topology-taxonomy]]; isolated per-ticker contexts are the sub-agent technique from [[anthropic-context-engineering]].

## Related

- [[anthropic-finance-agents]] — prior Managed Agents release with a developer-configured roster; the contrast case.
- [[claude-code-projects]] — coordinator delegating to parallel sessions; fixed role rather than model-authored topology.
- [[cursor-cloud-agents]] — competing coordinator pattern at larger fan-out.
- [[langchain-rlms]] — convergent programmatic-orchestration approach from the open-source side.
- [[topology-taxonomy]] — where model-authored topology sits among the four topologies.
- [[harness-design-space]] — Multi-Agent Orchestrator pattern; flows as a self-designed-orchestration variant.
- [[openai-gpt-5-6-agentic-primitives]] — native multi-agent orchestration trained into the model.
- [[claude-platform-cost-optimization]] — budget, hill-climb, and cache levers relevant to flows' higher cost.
- [[agentic-harness-engineering]] — hill-climbing and automatic harness evolution.
- [[memory-evolution-survey]] — "dreaming" as memory consolidation.
- [[multi-agent-turf-war]] — shared-filesystem channel and collusion risk.
- [[devin-security-swarm]] — fan-out/review swarm parallel.
- [[anthropic-context-engineering]] — isolated subagent contexts.
