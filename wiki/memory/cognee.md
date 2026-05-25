# Cognee

Cognee (`topoteretes/cognee`) is an open-source **"memory control plane"** for AI agents — *"the brain behind your agents."* It ingests data in arbitrary formats, transforms it into a combined **knowledge-graph + vector** representation (the `cognify` step), and serves it back through a small `remember / recall / forget / improve` API with **auto-routed retrieval** (it picks the search strategy per query). It runs fully local by default (graph backends Neo4j / FalkorDB / Kuzu; vector search alongside), with a managed Cognee Cloud option and one-click deploys (Modal/Railway/Fly/Render/Daytona). It ships a **Claude Code plugin with five lifecycle hooks** — the deepest Claude Code hook integration in this research batch — and is backed by an arXiv paper (2505.24478, *"Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning"*). Doctrinally it is on the **extract/transform pole**.

> **Authority:** the README (`04-cognee.md`) is a vendor doc — trustworthy for the API surface, pipeline, and Claude Code hooks. Capability claims ("shared, improving memory"; junior analysts "near-expert level") are illustrative and **collect-but-confirm**. License and star count are not stated in the captured README; the arXiv paper is the externally verifiable artifact (its accuracy/cost numbers are not reproduced in the README).

## Architecture & pipeline

- **The pipeline (implicit ECL — extract / cognify / load):** `remember()` runs *add* (ingest) → *cognify* (process: embed + build graph) → *improve* (continuous refinement). The `cognify` step is a transformation, not a pass-through store — documents become "both searchable by meaning and connected by relationships."
- **Retrieval:** `recall()` uses **auto-routing** to select between semantic (embedding) search and graph traversal; it can hit session memory first and fall through to the permanent graph.
- **Storage:** graph stores (Neo4j / FalkorDB / Kuzu) combined with vector search; "various database configurations" supported.
- **API surface:** four operations — `remember`, `recall`, `forget`, `improve` — plus a CLI (`cognee-cli`, with a local UI). Python 3.10–3.14.

### Memory layers

- **Session memory** — a fast cache scoped by `session_id`.
- **Permanent knowledge graph** — persists across sessions, synced from session memory at session end or in the background.

## Doctrine placement

**Extract/transform pole, clearly.** The `cognify` step builds knowledge-graph structure from raw content rather than storing verbatim text as the primary retrieval artifact; the README's use cases use explicit extraction language ("extracts and stores patterns from expert SQL queries," "maps the current schema to previously seen structures"). It belongs to the *graph-augmented* sub-lineage of [[memory-architectures]]' retrieval-augmented stores, alongside [[mem0]]'s Mem0g and [[graphiti]]. Its closest peer is [[graphiti]] — both are OSS graph-memory engines that extract rather than store raw — with the differences being Graphiti's **bi-temporal** validity model vs Cognee's **session + permanent layers with an explicit `improve` loop**. See [[conflicts/verbatim-vs-extracted-memory]].

## Claude Code integration

A named **Claude Code plugin** (`cognee-integrations/integrations/claude-code`; install via `claude --plugin-dir ...`) wires Cognee into the agent through five lifecycle hooks:

| Hook | Behaviour |
|---|---|
| `SessionStart` | Initialises memory |
| `PostToolUse` | Captures tool-call actions into session memory |
| `UserPromptSubmit` | Injects relevant context into the prompt |
| `PreCompact` | **Preserves memory across context resets** (explicit compaction survival) |
| `SessionEnd` | Bridges session memory into the permanent graph |

The README describes Claude Code integration via these *hooks*, not an MCP server. An OpenClaw plugin also exists, and any Python agent can call `cognee.remember()` / `cognee.recall()` directly. This makes Cognee a Level-5/6 entry in the [[claude-code-memory-ecosystem]] ladder.

## Claims (collect-but-confirm)

All vendor self-report from the README: continuous learning from feedback, cross-agent knowledge sharing (architecturally implied by the shared graph), tenant isolation + OTEL + audit features, and an illustrative SQL-Copilot use case. No RAG-comparison numbers appear in the captured README; the cited arXiv paper (2505.24478) is examined below and — importantly — does **not** substantiate any cross-system superiority claim. `LLM_API_KEY` defaults to OpenAI in the quickstart, suggesting OpenAI is the primary tested backend despite multi-provider support.

## The backing paper (arXiv 2505.24478) — what it does and doesn't show

The paper Cognee cites is an **in-house study** (all authors Cognee-affiliated; preliminary, not peer-reviewed). It introduces **"Dreamify,"** a Tree-structured-Parzen-Estimator hyperparameter optimiser that treats Cognee's whole pipeline as a black box and tunes six parameters (chunk size, retrieval strategy = vector-chunks vs graph-triples, top-k, QA prompt, graph-construction prompt, include-summaries). It is **not** a general KG↔LLM method and **not** a comparison against other systems.

- **Datasets:** HotpotQA, 2WikiMultiHop, MuSiQue — but **tiny curated samples: 24 train + 12 test instances per dataset** (standard HotpotQA dev is ~7.4k).
- **Only baseline is Cognee's own untuned default** — there is **no comparison to vanilla RAG, GraphRAG, HippoRAG, or any other system.** So the paper shows *internal improvement from tuning*, not where Cognee lands in the field.
- **Best held-out scores after tuning:** HotpotQA F1 0.819 / EM 0.583; 2WikiMultiHop F1 0.704 / EM 0.417; MuSiQue F1 0.581 / EM 0.375.
- **EM "gains" are partly an artifact:** the untuned default emitted conversational-length answers that fail EM's exact-match strictness, so much of the lift is prompt-tuning toward shorter answers, not reasoning.
- It *does* confirm the architecture functions with switchable graph-triples vs vector-chunks retrieval (the core "memory control plane" mechanism), and that graph-triples mode was often selected by high-performing configs (vs Cognee's own vector-only mode).

**Net:** the paper does **not** upgrade Cognee's capability claims out of collect-but-confirm; it is an internal tuning result on n=12 held-out examples with no external baselines. The contrast with [[graphiti]]'s paper (which at least benchmarks against MemGPT and a full-context baseline) is instructive.

## Source

- `raw/research/oss-agent-memory/04-cognee.md` (https://github.com/topoteretes/cognee) — project README; vendor/tool documentation. Captured 2026-05-24.
- `raw/research/oss-agent-memory/12-cognee-paper.md` (https://arxiv.org/abs/2505.24478 — *"Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning"*, Markovic et al., Cognee Inc.) — captured 2026-05-24 via marker (CPU). In-house preliminary study; no external baselines.

## Related

- [[graphiti]] — closest OSS peer; both are graph-memory engines on the extract pole, with Claude integrations.
- [[mem0]] — Mem0g graph variant is the closest commercial peer in the graph-extract lineage.
- [[memory-architectures]] — *retrieval-augmented memory stores* family, graph-augmented sub-lineage.
- [[conflicts/verbatim-vs-extracted-memory]] — Cognee is an extract/transform-pole example.
- [[claude-code-memory-ecosystem]] — Cognee's Claude Code plugin (5 hooks incl. PreCompact) is one of the more deeply integrated OSS options.
- [[mcp-memory-server]] — the simpler official knowledge-graph memory server.
