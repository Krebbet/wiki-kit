# Claude Code Projects (Coordinator-Agent Redesign)

Anthropic vendor-primary product blog post (2026-09-17) announcing a beta redesign of Claude Code "Projects" from a passive folder/file-storage metaphor into a coordinator-agent architecture: a coordinator delegates work across parallel, full Claude Code cloud sessions ("threads"), each on its own git branch and its own copy of the repo, with shared memory and a common artifact library across threads. Anthropic's own-product entry into the "coordinator delegates to many parallel full agent sessions" pattern, following [[deployments/cursor-cloud-agents]]'s structurally near-identical Projects feature by about ten days.

## What changed

You state a goal plus a repo/context; Claude (the coordinator) scopes the request, delegates to threads, coordinates parallel work, reviews outputs, and assembles a finished result — steerable mid-flight, including from a phone, and continues working after the user steps away. Beta launch (2026-09-17) is limited to select Claude Pro/Max subscribers already using Claude Code cloud sessions with no existing web/desktop projects, with wider rollout "over the coming week," then Team/Enterprise. Existing Pro/Max projects keep working unchanged until upgraded.

## Architecture: two-tier coordinator/thread pattern

The **coordinator** is the main project chat — it routes work to new or pre-existing **threads**, the way a chief of staff would be briefed. Each **thread is a full, independent Claude Code cloud session**, on its own git branch and its own copy of the repo. Multiple threads can run concurrently; the coordinator does not enforce mutual exclusion — if two threads touch the same code, the overlap surfaces as an ordinary **merge conflict on the resulting PRs**, not a distributed-locking mechanism. Each thread can further decompose its own delegated slice via subagents, loops, and workflows.

Users configure the project's cloud environment, connectors, plugins, and instructions, and can independently select model/effort level for the coordinator vs. worker threads. Threads currently run only in the cloud; local/on-machine thread execution ("behind your network," alongside local tools) is flagged as "coming very soon."

Notable operational caveat: because each thread is a full Claude Code session, **projects can hit usage limits materially faster** than single-session use.

## Shared memory and artifact library

Per the post: "Every thread now adds to and draws from a shared memory, reducing the need for complex prompt engineering." Cited examples are project-level facts (a release date change, why a feature was dropped, who to consult before touching a service) and working/communication-style preferences (check-in cadence, thread-creation frequency, update verbosity). Separately, a **library** collects both user-added files and Claude-produced artifacts across all threads, intended to help new work reuse past outputs. No technical detail is given on the memory's storage mechanism, retention/eviction, or retrieval method (extraction vs. verbatim) — this is product-level framing, not an architecture disclosure.

**This claim is flagged against [[memory/claude-code-memory-ecosystem]]** — see [[conflicts/claude-code-projects-shared-memory]].

## Why it matters

Positions Claude Code explicitly for "long-running or agentic workflows... that take longer than one reply and have more than one part" — e.g. profiling every endpoint for a latency goal, or migrating callers of a deprecated API across API/web/mobile repos in parallel per-repo threads. The merge-conflict-as-coordination-mechanism choice (no explicit conflict-avoidance layer) is a notable design decision worth tracking against how Cursor and Cognition handle the same multi-session overlap problem.

## Related

- [[deployments/cursor-cloud-agents]] — near-exact structural parallel: Cursor's "Projects" (2026-09-10) already pairs a coordinator agent with many subagents and project-scoped shared context syncing across cloud/local; this is Anthropic's own-product counterpart, arriving ~10 days later.
- [[deployments/cognition-cloud-agents]] — same cloud-agent-infrastructure family (isolated sessions/branches per unit of work, coordinator-level orchestration); Cognition's is microVM-based, this is git-branch-based full-session-per-thread.
- [[memory/claude-code-memory-ecosystem]] — central curator-ruled claim ("no native session-to-session memory") that this source's shared-memory claim is flagged against; see [[conflicts/claude-code-projects-shared-memory]].
- [[governance/claude-code-auto-mode]] — same product; any Projects tracking should cross-link Claude Code's other major 2026 changes (permission model).
- [[case-studies/anthropic-claude-code-postmortem]] — same product, prior notable regression; general "recent Claude Code changes" cross-link.
- [[patterns/topology-taxonomy]] — coordinator/parallel-worker-threads-with-merge-conflict-resolution is a concrete new instance of manager-agent multi-agent orchestration topology.
- [[coding-agents/langchain-deep-agents]] — LangChain generalizes Claude-Code-style single-session harnesses into subagents-within-a-session; this source shows Anthropic moving toward a multi-full-session coordinator model instead — subagents-are-full-sessions-on-branches, a step further in scope.

## Source

- `raw/research/weekly-2026-09-20/05-claude-code-projects-redesign.md` — captured 2026-09-20 from `claude.com/blog/projects-redesigned` (2026-09-17). **Vendor primary.**
