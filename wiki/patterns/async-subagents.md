# Async Subagents (Non-Blocking Orchestrator Pattern)

LangChain's blog "Agents Are Going Async" (2026-11-05, captured 2026-11-08) argues that a standard ReAct loop, where each long tool or subagent call blocks the loop, cannot make an agent both responsive (acting on new instructions immediately, with full context) and productive (progressing many long tasks at once). The proposed split is an orchestrator that stays available to the user and async subagents that run in the background and report back on completion, so capacity scales with the number of workers rather than the length of one loop. LangChain ships this in Deep Agents (Python, JS) and Managed Deep Agents.

## Mechanisms

- A call to an async subagent returns immediately, like `asyncio.create_task` or an un-awaited Promise; the work runs on its own thread.
- Five orchestrator tools: `start_async_task`, `check_async_task` (status, and result once done), `update_async_task` (send new instructions), `cancel_async_task`, `list_async_tasks`.
- Steering via the subagent's `update_strategy`: `"interrupt"` (default) stops the run and restarts it with the new instruction (a correction); `"enqueue"` holds the follow-up until the current run finishes (an addition).
- Notifications: unfinished tasks are listed in the orchestrator's system prompt. If the orchestrator is busy, it checks tasks before each model call and picks up results mid-run; if idle, the subagent wakes it with a new run; if paused on an approval, the approval is left alone and the result arrives after the user answers. A subagent needing approval shows as `waiting`, and the user answers on the subagent's own thread. Task notifications are beta.
- Managed Deep Agents: one field (`"async": True`) makes a subagent async; every served agent also gets an async copy of the `general-purpose` subagent so it can choose foreground or background at runtime.
- Claimed ecosystem convergence: Claude Code (background subagents by default), OpenAI dots, DeepSeek Harness; OpenAI async tool calling is cited as the same idea for tools, and the post expects it to generalize beyond subagents.

## Numbers and authority

No benchmarks, latency, or cost figures are given. This is a vendor blog promoting its own product: the design description is usable as stated, while the "ecosystem is converging" claim is assertion (collect-but-confirm). Tension (scope, not contradiction) with [[patterns/fold-subagents-into-main-loop]], which treats subagents as the exception; async subagents fit that page's "parallel work with fresh contexts" case.

## Source

- raw/research/weekly-2026-11-08/03-langchain-agents-async.md (https://www.langchain.com/blog/agents-are-going-async)

## Related

- [[coding-agents/langchain-deep-agents]] — the harness this extends.
- [[patterns/deep-agents-context-engineering]] — synchronous subagents as context isolation.
- [[patterns/fold-subagents-into-main-loop]] — when subagents are warranted at all.
- [[patterns/topology-taxonomy]] — orchestrator/worker topologies.
