# Harness Engineering: Source-Code Study of Eleven Coding Agents (arXiv 2609.00006)

Barbaste et al. (Inclusive Brains / Wavestone AI Lab, July 2026) audit the source of eleven production coding harnesses (Claude Code, Codex CLI, Gemini CLI, Mistral Vibe, OpenHands, Aider, Mini-SWE-Agent, Hermes, Pi, OpenCode, OpenClaw), with Databricks' Omnigent as a contrast point, and argue the coding harness has turned from a tool into a platform. Headline evidence: across about 4M lines, no runtime imports a general-purpose agentic framework and none uses embedding-based code retrieval. It is a source-reading study with no runtime benchmarking, so structural claims are stronger than the landscape and star-count claims, which the authors did not verify.

## Method and outputs

- Source-level reading only, pinned to July 2026 releases. This is a second edition: 8 systems carry over from an April 2026 edition and are re-pinned, giving a source-diffed sample across one quarter.
- Seven canonical subsystems (loop, tools, context/memory, safety, orchestration, extensibility, LLM integration), each with a minimal and a maximal implementation.
- Outputs: 13 cross-cutting observations, 29 design patterns, 18 recommendations, and a 90-line minimum-viable-harness scaffold implementing 10 of them.

## Findings

- **Twin absences:** hand-rolled async loops plus ripgrep, tree-sitter, glob and Markdown context files everywhere. Gemini CLI uses neither of Google's own frameworks. Embeddings appear only for conversation memory (OpenClaw defaults to sqlite-vec plus FTS5/BM25; Hermes uses deterministic SQLite FTS5 with no LLM calls). Caveat: dynamic imports, forks and plugins were not traced.
- **Skills overtook MCP:** SKILL.md in 9 of 11 systems versus MCP in 8 of 11. Skills gained registries, trust tiers, provenance verification, cross-vendor discovery (OpenCode reads `~/.claude/skills`) and the first agent-authored skills (Hermes, Gemini CLI). Pi implements agentskills.io and rejects MCP. ACP ships in 6 systems and gained a harness-hosting role (OpenHands runs Claude Code, Codex or Gemini CLI as interchangeable backends). Sub-agent coordination stays in-process in 8 of 9 multi-agent systems.
- **90-day evolution:** convergence became imitation (Codex adopted Claude Code's hook vocabulary verbatim and ships a settings importer). Patterns diffuse fast (deferred tool loading 1 to 3 systems, plan modes 2 to 4, turn-level checkpointing 1 to 3), so a competitive distinctive's half-life is "weeks". Behavioral policy is moving from prompt prose to configuration and feature flags. Codex grew from 621K to about 1.12M lines of Rust.
- **Revised April observations:** provider coupling is about who controls the update loop, since multi-provider harnesses (Hermes, Pi, OpenCode) reach provider-native optimizations by paying the cost centrally. Size no longer implies sandboxing (Hermes and OpenCode are large with no OS-level isolation). Inventory claims decay in weeks; structural claims endure.
- **Platform turn:** harnesses ship as importable SDKs while framework vendors ship harnesses; marketplaces, switching-cost importers and MDM-grade governance appeared; Omnigent orchestrates eleven vendor harnesses behind one API.
- **Safety:** Codex has a four-layer permission stack with native sandboxing; Claude Code three layers plus an LLM approval classifier; Hermes keeps a policy floor that survives YOLO mode; Pi documents the absence of safety as a security argument.
- **Memory/context spectrum:** linear history (Mini-SWE-Agent), recursive summarization (Aider), pluggable condensation (OpenHands), threshold compaction (7 systems), persistent memory pipelines (Hermes frozen-snapshot Markdown, OpenClaw Active Memory, OpenHands writing into AGENTS.md).
- **Headline claim:** loop sophistication does not predict benchmark performance (Mini-SWE-Agent's roughly 50-100 line loop reports frontier-range results per its own docs) but does predict production readiness. The Anthropic effective-agents guidance maps closely onto observed architectures, which the authors call suggestive, not causal.

## Limitations

No head-to-head measurement; qualitative scores involve judgment; the Claude Code analysis rests on a circulated March 2026 source snapshot (weakest reproducibility); no vendor interviews; the paper was written with heavy Claude Code assistance (disclosed), a mild bias note. No code or data repository was found in the captured text.

## Relationship to existing wiki pages

- **Update to [[patterns/harness-design-space]]:** that 70-project survey (corpus frozen March 2026) reports registry tools at 34.3% versus MCP-first at 14.3%; this study finds skills and MCP both widespread among 11 flagship systems. Different corpora and metrics, so this is scope tension, not a contradiction. No conflict file opened.
- **Framework framing:** the no-framework-imports result and the "harness-framework merger" bear on [[coding-agents/langchain-deep-agents]] and the framework-as-build-tier view in [[patterns/agent-development-lifecycle]]. Scope is limited to the 11 systems studied.
- **Corroborates:** [[patterns/agentic-harness-engineering]] (minimalism, policy out of prose), [[patterns/effective-harnesses]], [[patterns/harness-scaling-position]], [[patterns/externalization-survey]] and [[patterns/agent-skills]] (skills 9/11).
- **Evidence for adoption, not effectiveness:** the universality of auto-discovered Markdown context files, relevant to [[conflicts/agents-md-effectiveness]] and [[patterns/agents-md]].
- **Memory comparisons:** [[memory/openclaw]] and [[memory/openclaw-claude-code-memory]].

## Source

- `raw/research/weekly-2026-10-04/03-harness-engineering-coding-agents.md` — arXiv 2609.00006, captured via marker from the PDF URL

## Related

- [[patterns/harness-design-space]]
- [[patterns/code-as-agent-harness]]
- [[patterns/agentic-harness-engineering]]
- [[patterns/effective-harnesses]]
- [[patterns/agent-skills]]
- [[patterns/agents-md]]
- [[patterns/harness-scaling-position]]
- [[deployments/mcp-infrastructure]]
- [[memory/openclaw]]
- [[security/cyber-eval-sandbox-escapes]]
