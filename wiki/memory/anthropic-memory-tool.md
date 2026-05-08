# Anthropic Memory Tool (Claude API)

Anthropic's official primary source for the **Memory tool** — the Claude API primitive for cross-conversation persistence. Direct framing from the docs: *"This is the key primitive for just-in-time context retrieval: rather than loading all relevant information upfront, agents store what they learn in memory and pull it back on demand. This keeps the active context focused on what's currently relevant, critical for long-running workflows where loading everything at once would overwhelm the context window."* The tool exposes six file-system-style commands over a `/memories` directory; **operates client-side** so the developer controls storage; ZDR-eligible. SDK example uses `claude-opus-4-7` and tool type string `memory_20250818`.

## Client-side architecture

*"The memory tool operates client-side: you control where and how the data is stored through your own infrastructure."* Claude issues tool calls; the developer's application executes them locally. This gives *"complete control over where and how the memory is stored."* ZDR is explicit: *"When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned."* All operations must be restricted to `/memories`.

SDK helpers: `BetaAbstractMemoryTool` (Python) — subclass to implement custom backends (file-based, database, cloud storage, encrypted files). `betaMemoryTool` (TypeScript). Tool type string: `{"type": "memory_20250818", "name": "memory"}`.

## The six commands

All operate under `/memories`.

- **view** — `{command: "view", path, view_range?: [start, end]}`. Directories: returns a two-level listing with human-readable sizes. Files: returns content with line numbers. Errors on missing path.
- **create** — `{command: "create", path, file_text}`. Returns `"File created successfully at: {path}"` or errors if the file exists.
- **str_replace** — `{command: "str_replace", path, old_str, new_str}`. Requires `old_str` to appear *exactly once and verbatim*. Returns the edited snippet on success. Errors on missing path, not-found string, or multiple matches.
- **insert** — `{command: "insert", path, insert_line, insert_text}`. `insert_line` must be in `[0, n_lines]`. Errors on missing path or out-of-range line.
- **delete** — `{command: "delete", path}`. Removes a file or directory recursively. Errors on missing path.
- **rename** — `{command: "rename", old_path, new_path}`. Moves/renames file or directory. Errors on missing source or existing destination.

## The auto-injected MEMORY PROTOCOL

When the Memory tool is enabled, Anthropic injects the following system-prompt block automatically:

> IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
> MEMORY PROTOCOL:
> 1. Use the `view` command of your `memory` tool to check for earlier progress.
> 2. ... (work on the task) ...
> - As you make progress, record status / progress / thoughts etc in your memory.
> ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.

The "ASSUME INTERRUPTION" framing is the operational equivalent of [[anthropic-internal-study]]'s *cold-start problem*: Anthropic now ships a default behaviour assuming the cold start will happen and instructing the model to mitigate it.

An optional supplementary instruction the developer can add: *"when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary."*

## Pairs with context editing and compaction

*"The memory tool pairs with context editing to manage long-running conversations."* Three-layer stack:

1. **Memory tool** — cross-session persistence (this page).
2. **Context editing** — client-side; clears specific tool results.
3. **Compaction** — server-side; automatically summarises the entire conversation when it approaches the context limit.

Recommended pattern from the docs: *"compaction keeps the active context manageable without client-side bookkeeping, and memory persists important information across compaction boundaries so that nothing critical is lost in the summary."*

## The long-running software project pattern

Direct quote: *"For long-running software projects that span multiple agent sessions, memory files need to be bootstrapped deliberately, not just written ad hoc as work progresses. The pattern below turns memory into a structured recovery mechanism, so each new session can pick up exactly where the last one left off."*

Three phases:
- **Initializer session** — sets up memory artifacts before substantive work: a progress log, a feature checklist, a reference to any startup or initialization script.
- **Subsequent sessions** — opens by reading those artifacts to recover full project state *"in seconds, without needing to re-explore the codebase or retrace earlier decisions."*
- **End-of-session update** — updates the progress log with what was completed and what remains before the session ends.

Discipline: *"Work on one feature at a time. Only mark a feature complete after end-to-end verification confirms it works, not just after the code is written. This keeps the progress log trustworthy and prevents scope creep from compounding across sessions."*

This is the structured form of [[codified-context]]'s tiered architecture, framed for general API consumers rather than a single 108k-line C# system. The constitution + cold KB pattern is the same idea at the project-knowledge level; this is the same idea at the work-progress level.

## Security guidance

Four concerns explicitly called out:

- **Sensitive data** — *"Claude will usually refuse to write down sensitive information in memory files. However, you may want to implement stricter validation that strips out potentially sensitive information."*
- **File size limits** — track sizes, prevent unbounded growth, add max characters returned by reads, paginate.
- **Periodic clearing** — clear files not accessed in extended periods.
- **Directory traversal** — *"Malicious path inputs could attempt to access files outside the `/memories` directory. Your implementation MUST validate all paths to prevent directory traversal attacks."* Specific guidance: block `../`, `..\\`, URL-encoded patterns (`%2e%2e%2f`); use `pathlib.Path.resolve()` and `relative_to()` (Python).

The directory-traversal guidance is unusually emphatic for a docs page — a security-relevant signal that this primitive is treated as a sensitive surface.

## Relationship to neighbouring wiki pages

- **API-level expression of [[memgpt]] / [[letta-memory-blocks]].** Same paradigm — agent paging memory in/out via tool calls — exposed as a vendor primitive instead of a runtime to install. Six file-system commands instead of MemGPT's `recall_storage.search` etc.
- **Compaction is Anthropic's server-side answer to [[context-folding]] (AgentFold).** AgentFold is per-step variable-granularity in-context compression; compaction is end-of-conversation server-side summarisation. Different timing; same goal.
- **The MEMORY PROTOCOL "ASSUME INTERRUPTION" line names the cold-start problem documented in [[anthropic-internal-study]].** Anthropic now ships the operational mitigation as a default tool behaviour.
- **The Initializer/Subsequent/End-of-session pattern is [[codified-context]] for general API consumers.** Same hot/cold-memory discipline, framed at the work-progress level instead of the codebase-knowledge level.

## Worth pulling next round

The docs link to: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents — described as *"a detailed case study of this pattern in practice, including the initializer script, progress file structure, and git-based recovery."* Not in the wiki yet; flagged for next ingest. Distinct from the *Effective context engineering* blog also referenced.

## Source

- `raw/research/memory-management/02-06-anthropic-memory-tool.md` (captured 2026-04-26 from https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool)

## Related

- [[memgpt]] — paradigm origin; the API-level Memory tool is the same idea exposed as a vendor primitive.
- [[letta-memory-blocks]] — alternative productionisation; both expose memory ops to the LLM with different abstractions (memory blocks vs files).
- [[claude-code-session-memory]] — Claude Code's product-specific memory layer; built on top of the API primitive.
- [[memory-architectures]] — survey places this in the *hierarchical virtual context* family.
- [[codified-context]] — application-layer realisation of the same Initializer/Subsequent/End-of-session discipline.
- [[anthropic-internal-study]] — names the cold-start problem the MEMORY PROTOCOL "ASSUME INTERRUPTION" line addresses.
- [[context-folding]] — AgentFold is the per-step in-context compression peer to Anthropic's server-side compaction.
