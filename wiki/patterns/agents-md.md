# AGENTS.md

AGENTS.md is a lightweight Markdown format for giving AI coding agents project-specific context and instructions — coding conventions, build steps, testing requirements — in a single file designed to live alongside `README.md`. Originally an internal Codex tool at OpenAI, released publicly in August 2025, and donated to the [[governance/aaif|Agentic AI Foundation]] (AAIF) under the Linux Foundation in May 2026. By donation it had been adopted by more than 60,000 open-source projects (vendor-stated — collect-but-confirm) and was supported by the major coding-agent tools. AGENTS.md is the *project-context specification format* for agent handoff — distinct from in-session memory blocks, skill libraries, or harness scaffolding.

## Source

- `raw/research/weekly-2026-05-31/05-openai-agentic-ai-foundation.md` (captured 2026-05-31 from https://openai.com/index/agentic-ai-foundation/)

## Design and intent

AGENTS.md solves a specific, recurring problem: a coding agent entering an unfamiliar repository needs project-specific guidance — build commands, test conventions, style rules, known gotchas — that is not reliably deducible from source files alone. Rather than embedding this in the agent framework, AGENTS.md externalises it into the repository itself as a plain Markdown file.

Key design properties:
- **Repository-local** — lives in the repo root alongside `README.md`; version-controlled with the project.
- **Format-agnostic** — plain Markdown; no schema, no tooling dependency.
- **Agent-side consumption** — agents read it at session start; the file's contents are the agent's project briefing.
- **Human-authorable** — designed to be written and maintained by developers, not auto-generated (contrast with LLM-generated context files, which the [[evaluation/agents-md-eval|AGENTbench study]] finds reduce success rates; see [[conflicts/agents-md-effectiveness]]).

The name parallels `README.md` intentionally: README is for humans, AGENTS.md is for agents.

## Governance trajectory

- **August 2025** — released publicly by OpenAI as part of the Codex CLI.
- **May 2026** — donated to AAIF/Linux Foundation. Governance transfers from OpenAI-steered to vendor-neutral. The AAIF mandate: the format can evolve in the open, with input from many tools and communities; no single company controls its direction.

## Adoption landscape

Adopters named by the OpenAI announcement at time of AAIF donation:

**Agent frameworks / coding assistants:** Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, VS Code.

The 60,000+ open-source project adoption figure is vendor-stated and does not address effectiveness. Adoption at scale and effectiveness in benchmarks are separate questions; see [[conflicts/agents-md-effectiveness]] for the open conflict.

## Wiki connections

AGENTS.md is referenced across several wiki pages before this dedicated page existed:

- **[[case-studies/cursor-agent-harness]]** — Cursor is a named AGENTS.md adopter; the harness case study covers how Cursor integrates per-project agent context.
- **[[patterns/harness-design-space]]** — empirical survey of real-world harness patterns finds AGENTS.md used in the wild; the 60k adoption figure quantifies its prevalence.
- **[[deployments/openai-symphony]]** — OpenAI Frontier's Symphony harness uses agents.md as a TOC layer alongside session-log distillation and six skills; a concrete production example of AGENTS.md operating inside a larger harness architecture.
- **[[conflicts/agents-md-effectiveness]]** — open conflict on whether context files help or hurt coding-agent performance; AAIF's formalization adds institutional weight to the vendor-favorable position.

## What AGENTS.md is not

- **Not a memory system** — it does not persist agent-generated observations across sessions (see [[memory/memory-architectures]] for that category).
- **Not a skill library** — it does not package reusable procedural instructions invoked on demand (see [[patterns/agent-skills]]).
- **Not a harness** — it does not orchestrate sub-agents, manage tool calls, or define execution flow (see [[patterns/harness-design-space]]).

AGENTS.md is the *static project-context specification*: what the project is, how it works, what the agent should know before starting. It is the entry point, not the system.

## Related

- [[governance/aaif]] — the foundation now stewarding AGENTS.md as an open standard
- [[conflicts/agents-md-effectiveness]] — open conflict: does context-file provision help or hurt coding-agent performance?
- [[evaluation/agents-md-eval]] — AGENTbench study finding LLM-generated context files reduce success ~3% and inflate cost >20%
- [[patterns/codified-context]] — structured context *system* (scale contrast: 660-line constitution + specialist agents vs single AGENTS.md file)
- [[patterns/effective-harnesses]] — agent-authored handoff artefacts as the alternative authorship model
- [[deployments/openai-symphony]] — production harness using AGENTS.md as a TOC layer
- [[case-studies/cursor-agent-harness]] — named AGENTS.md adopter
- [[patterns/harness-design-space]] — AGENTS.md found in the wild in empirical harness survey
