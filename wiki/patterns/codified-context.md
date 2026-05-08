# Codified Context

Single-author experience report on building a 108k-line C# distributed system using Claude Code as the sole code generator, where project knowledge was treated as load-bearing infrastructure: a 660-line "constitution" loaded every session, 19 specialist agents (~9.3k lines) invoked per task, and a 34-document cold knowledge base (~16.3k lines) served via an MCP retrieval server. The framework is positioned as a direct response to the limit case of single-file manifests: AGENTS.md / CLAUDE.md / .cursorrules patterns that work at prototype scale collapse beyond ~1,000 lines, and a 100k-line system needs a tiered hot/cold memory architecture instead.

## The three tiers

- **Tier 1 — Constitution (hot memory)** — single 660-line Markdown file loaded every session. Encodes code-quality rules, naming conventions, build commands, architecture summaries with pointers into Tier 3, failure-mode checklists, and a *trigger table* that routes tasks to specialist agents based on which files are being modified.
- **Tier 2 — Domain specialists (19 agents, 9,300 lines)** — invoked per task. Split into 8 higher-capability agents (avg 711 lines: network, architecture, debugging) and 11 standard agents (avg 327 lines). Notably, *more than half* of each spec is project-domain knowledge — facts, formulas, symptom-cause-fix tables — not behavioral instructions. Specialists were created reactively after observed failure patterns, not designed upfront.
- **Tier 3 — Knowledge base (cold memory, 34 files, 16,250 lines)** — per-subsystem Markdown specs written explicitly for AI consumption (file paths, parameter names, expected behavior). Served via a 1,600-line Python MCP server exposing five tools: `list_subsystems()`, `get_files_for_subsystem()`, `find_relevant_context()`, `search_context_documents()`, `suggest_agent()`. Retrieval is currently keyword substring matching; the author flags semantic retrieval as a priority improvement.

A Python **context-drift detector** (session-start hook) parses recent Git commits against the subsystem-to-file mapping and injects a warning when source files change without a corresponding spec update.

## Quantitative results

Across 70 days of part-time development, 283 sessions, 148 commits:

- 2,801 human prompts; 1,197 agent invocations; 16,522 agent turns.
- ~9.9 prompts/session; ~6 agent turns per human prompt.
- 87% of sessions ad-hoc; 13% structured plan-execute-review.
- 432 of 757 classifiable agent invocations went to project specialists (57%); most-invoked were `code-reviewer` (154) and `network-protocol-designer` (85).
- >80% of human prompts ≤100 words. 4.3% were meta-infrastructure prompts (building the context system itself).
- 1,478 MCP retrieval calls across 218 sessions.
- ~1–2 hours/week maintenance overhead.

The paper cites prior work (Lulla et al. 2026) reporting AGENTS.md presence associated with 29% reduction in median runtime and 17% reduction in output token consumption — but this is invoked as evidence that single-file manifests help *at prototype scale*, not as a conflicting claim.

## Self-documented limitations

- **Single developer, single project** — no team or cross-project replication; domain (real-time distributed simulation) is unusually documentation-intensive.
- **Observational, not experimental** — no controlled before/after; causal claims explicitly disclaimed; developer skill growth is a confound.
- **Specification staleness is the primary failure mode** — two documented cases where stale specs caused agents to wire code through deprecated paths; errors were syntactically correct and only caught during testing.
- **Tool-specific** — implementation tied to Claude Code + MCP; transferability untested.
- **Keyword-only retrieval** — flagged as the most pressing gap.

## Why it matters

- **Direct mechanism for the cold-start problem.** The Anthropic 132-engineer study ([[anthropic-internal-study]]) names *cold start* as the main friction limiting wider delegation; this paper proposes a concrete tiered architecture that makes structured project context machine-loadable. The two pages are mutually reinforcing — diagnosis on one side, candidate solution on the other.
- **Operationalises the SWE-bench Pro patch-scale finding.** [[swe-bench-pro]] shows agent performance degrades monotonically with patch scale on unfamiliar repos; Codified Context is one of the first published designs explicitly targeting that regime (100k+ lines).
- **The hot/cold split is portable.** The architecture mirrors OS virtual-memory paging — a pattern the broader [[memory-architectures]] survey identifies as a major mechanism family (hierarchical virtual context).
- **Direct tension with AGENTS.md eval.** Codified Context argues for *more* structured context; the AGENTS.md eval ([[agents-md-eval]]) finds context files often *hurt* in well-maintained mid-sized Python repos. See [[../conflicts/agents-md-effectiveness]] for the resolution.

## Source

- `raw/research/long-horizon-context/01-01-codified-context.md` (captured 2026-04-25 from https://arxiv.org/abs/2602.20478)

## Related

- [[memory-architectures]] — tiered hot/cold memory is an instance of the *hierarchical virtual context* family.
- [[agentic-context-engineering]] — Codified Context directly cites ACE (Zhang et al. 2026) and uses ACE's *brevity bias* finding as justification for embedding substantial domain knowledge in specialist agents rather than relying on iterative prompt minimization.
- [[context-engineering]] — Codified Context's three-tier architecture is a system-level instance of the survey's context-management category, scaled to 26k context lines for a 108k-line system.
- [[topology-taxonomy#long-horizon-context-loss]] — concrete realisation of the long-horizon-context-loss mitigation pattern.
- [[anthropic-internal-study]] — names the cold-start problem this paper attacks.
- [[swe-bench-pro]] — empirical evidence for why the 100k-line regime needs different infrastructure.
- [[ai-scientist-v2]] — both materialise context structurally, but at different abstractions (research-stage tree vs. tiered codebase memory).
- [[agents-md-eval]] — counter-evidence on context-file effectiveness; resolution at [[../conflicts/agents-md-effectiveness]].
