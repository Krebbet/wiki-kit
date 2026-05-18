# Anthropic — Effective Context Engineering for AI Agents (2026-05)

Anthropic's Applied AI team defines "context engineering" as the discipline of curating the smallest high-signal token set for each inference step, and outlines concrete techniques — just-in-time retrieval, compaction, and structured note-taking — for building agents that remain coherent over long horizons. The post is the primary-vendor articulation of context engineering as a named successor discipline to prompt engineering, and positions Claude Code as its main production instance throughout.

## Context engineering vs prompt engineering

The post frames prompt engineering as a subset of a broader concern. Prompt engineering is about instruction wording; context engineering is about the entire token universe: system prompt, tool definitions, MCP server schemas, message history, and externally retrieved data. The attention budget framing follows: the transformer's n² attention mechanism makes context a finite resource, and "context rot" (citing ChromaDB needle-in-haystack research) means marginal token value decreases — and can go negative — as the window fills. The failure modes the post names are "over-specified brittle prompts" and "vague high-level prompts"; the load-bearing heuristic is right-altitude prompts with XML tags / Markdown headers and minimal viable information.

**Tool discipline** is treated as a first-class context concern: recommend minimal, non-overlapping toolsets; bloated overlapping tool sets are a named failure mode because they deplete the attention budget before the agent does any substantive reasoning.

## Three core long-horizon techniques

### 1. Just-in-time (JIT) retrieval

Rather than pre-loading all potentially relevant data into the context, agents maintain lightweight references — file paths, URLs, stored query strings — and load content at runtime via tools. Claude Code is the named production instance, using `grep`, `glob`, `head`, and `tail` as JIT primitives; `CLAUDE.md` pre-loaded at session start is framed as the hybrid anchor: stable, low-cost to carry, always relevant.

The mechanism is progressive disclosure through autonomous exploration: the agent decides what to retrieve and when, guided by what it already knows. The post endorses a **hybrid** of JIT and pre-computed retrieval — pre-computed for stable, low-dynamic content; JIT as the discretionary layer on top — and does not position JIT as strictly superior in all regimes.

### 2. Compaction

When context approaches the limit, summarise it: preserve architectural decisions, unresolved bugs, implementation details; discard redundant tool outputs. Claude Code's implementation: the model summarises history plus the five most recently accessed files. Tool-result clearing is described as the lightest-touch form. The post also references a new Anthropic Developer Platform "context management" feature.

**Tuning advice:** start with maximum recall, then iterate toward precision. This advice is not captured in [[claude-code-session-memory]] and is a new operational data point for that page.

The post describes compaction as "typically the first lever in context engineering to drive better long-term coherence." This is an architectural-principle framing — compaction is the natural starting point, not the complete solution. The post immediately introduces structured note-taking as the complementary technique. See [[patterns/effective-harnesses]] for the operationally-learned refinement: compaction alone is insufficient; structured external state is the necessary complement.

### 3. Structured note-taking (agentic memory)

The agent writes persistent notes outside the context window — `NOTES.md` files, to-do lists — and pulls them back in when needed. The post cites Claude-plays-Pokémon as a non-coding-domain exemplar: 1,234-step tallies and explored-region maps maintained as external durable state. Also references the new Anthropic memory tool (public beta at Sonnet 4.5 launch), file-based, six commands, client-side.

The structured note-taking technique maps cleanly onto the write-manage-read loop in [[memory-architectures]] and onto the `feature_list.json` / `claude-progress.txt` artefacts in [[patterns/effective-harnesses]].

## Sub-agent architectures as a fourth technique

The post names a fourth long-horizon technique — sub-agent architectures — though it falls outside the JIT/compaction/note-taking triad. Lead agent coordinates at high level; sub-agents handle focused tasks with clean context windows. Sub-agents may consume tens of thousands of tokens but return 1,000–2,000 token summaries. Vendor-reported "substantial improvement" (no figure given — collect-but-confirm). Cites the companion "How we built our multi-agent research system" post as prior art.

## Production framing

The post is explicitly production-oriented, authored by the Applied AI team working alongside customers. It is not a research paper. The technical guidance (compaction mechanics, tool discipline, JIT retrieval framing) is trustworthy; performance/benchmark claims are collect-but-confirm. The post builds on prior Anthropic posts ("Building effective agents," "Writing tools for AI agents") and references Karpathy's "art and science of context engineering" framing (tweet, 2025-09-18).

## Source

- `raw/research/weekly-2026-05-18/01-anthropic-context-engineering.md` — Anthropic Engineering Blog, "Effective context engineering for AI agents," 2026-05. Applied AI team. Primary vendor source.

## Related

- [[patterns/context-engineering]] — parent vocabulary anchor; this post is the primary-vendor articulation of the discipline.
- [[patterns/sierra-context-engineering]] — Sierra's domain-specific eight-block instantiation; Sierra's "progressive disclosure" ≈ Anthropic's JIT retrieval principle.
- [[patterns/effective-harnesses]] — operationally-learned complement: compaction + structured external state as the production answer; `feature_list.json` / `claude-progress.txt` are a concrete instantiation of note-taking technique.
- [[patterns/direct-corpus-interaction]] — academic corroboration of JIT retrieval via `grep`/`glob`/`head`/`tail`; DCI independently names Claude Code as the production instance.
- [[anthropic-memory-tool]] — the memory tool referenced here (file-based, six commands, public beta at Sonnet 4.5) is covered on this page; this post adds long-horizon agent framing.
- [[claude-code-session-memory]] — compaction mechanics described here (model summarises history + five most recently accessed files) are the same mechanism; this post adds tuning advice (max-recall-first → precision-iterate).
- [[context-folding]] — peer long-horizon mechanism; compaction is Anthropic's production answer, AgentFold is the research answer.
- [[memory-architectures]] — structured note-taking maps to write-manage-read loop; JIT retrieval maps to retrieval-augmented stores; compaction is a lightweight mechanism not foregrounded in the existing taxonomy.
