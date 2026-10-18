# Deep Agents Context Engineering

LangChain's Deep Agents harness fights context rot by moving context out of the active window rather than deleting it, using five middleware-based techniques: offloading, summarization, skills, subagents, and long-term memory. *(2026-10-18, LangChain vendor blog.)* The post frames the problem in two halves — preventing information from entering the window and managing what is already in it — and argues retrieval (RAG, filesystem search) solves only the first. Thresholds below are vendor-stated defaults; the post is an explainer with no benchmarks or quantitative results, so effectiveness claims are unverified.

## Five techniques

- **Offloading** — `FilesystemMiddleware` writes tool results over ~20,000 tokens to `/large_tool_results/{tool_call_id}`. The model sees a head/tail preview plus the path and pages the rest in via `read_file`. Human messages over ~50,000 tokens go to `/conversation_history/`.
- **Summarization** — `SummarizationMiddleware` checks usage before each model call. At 85% of the context window (default) a separate LLM call condenses older messages while recent ones stay verbatim. Summarized messages are written to `/conversation_history/{session_id}.md`, so compaction is recoverable. Summaries cycle (the next includes the previous) and can also trigger on topic change with a custom prompt.
- **Skills** — progressive disclosure. `SkillsMiddleware` scans `SKILL.md` headers before start and injects names and descriptions into the system prompt on every model call; full instructions load via `read_file` only when relevant.
- **Subagents** — `SubAgentMiddleware` runs noisy work in an isolated context that returns only its final result (not even a preview). Subagents can use cheaper models and run in parallel (`create_deep_agent(subagents=[...])`).
- **Long-term memory** — `MemoryMiddleware` loads a markdown file (e.g. `/memories/AGENTS.md`), injects it into the system prompt each call, and lets the agent update it. Because memory is plain files in a user-controlled store, it survives a model or provider switch.

## Design principles

Offload rather than truncate; make compaction recoverable; load know-how on demand; isolate noisy work; own your memory; keep defaults customizable.

## Relations to existing wiki patterns

- The JIT retrieval / compaction / note-taking triad in [[patterns/anthropic-context-engineering]] maps onto offloading, summarization, and memory; subagent isolation is shared.
- Recoverable summarization with a file archive parallels the fold-with-sidecar approach of [[patterns/self-gc-context]] and the proactive folding of [[context-folding]], but triggers at a fixed threshold rather than planner-chosen actions.
- The skills mechanism is the same three-level progressive disclosure described in [[patterns/agent-skills]]; [[patterns/sierra-context-engineering]] also treats progressive disclosure as load-bearing.
- File-based memory in a user-controlled store parallels [[anthropic-memory-tool]]. The summary-plus-verbatim-archive hybrid is a data point for the hybrid position in [[conflicts/verbatim-vs-extracted-memory]], though the memory file is curated markdown rather than an extraction store.
- Paging offloaded content through `read_file` over an index echoes [[patterns/direct-corpus-interaction]].

## Caveats

The example uses a fictional model id (`openai:gpt-6`), and the post promotes a webinar and LangChain Academy course. It refers to a companion post, "context management for Deep Agents", not captured here.

## Source

- `raw/research/weekly-2026-10-18/04-deep-agents-context-engineering.md` — "Context Engineering with Deep Agents: How To Remember Without Keeping Everything In Context" (LangChain blog, https://www.langchain.com/blog/context-engineering-deep-agents-remember; captured 2026-10-18).

## Related

- [[coding-agents/langchain-deep-agents]] — the harness itself; this page is the newer, middleware-level account of its context handling.
- [[coding-agents/langchain-rlms]] — another Deep Agents route around context rot (programmatic orchestration vs. offload/summarize).
- [[patterns/context-engineering]] — general topic; this is a concrete vendor implementation.
- [[patterns/anthropic-context-engineering]] — primary-vendor counterpart.
- [[patterns/self-gc-context]], [[context-folding]] — recoverable context-management alternatives.
- [[patterns/agent-skills]], [[anthropic-memory-tool]] — skills and file-based memory counterparts.
- [[patterns/effective-harnesses]] — "compaction isn't sufficient" vs. recoverable compaction.
- [[patterns/model-cost-routing]] — cheaper-model subagents.
- [[patterns/externalization-survey]] — memory/skills/harness externalization framing.
- [[conflicts/verbatim-vs-extracted-memory]]
