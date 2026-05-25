# Official MCP Memory Server

The reference **`memory` server** in `modelcontextprotocol/servers` (`src/memory`) — the canonical open-source knowledge-graph memory MCP server, maintained by the MCP organization (the Anthropic-led open-source initiative). MIT-licensed; published as `@modelcontextprotocol/server-memory` (npm) and `mcp/memory` (Docker). Its README describes it plainly: *"A basic implementation of persistent memory using a local knowledge graph. This lets Claude remember information about the user across chats."* It is the **upstream the community `mcp-knowledge-graph` (shaneholloman) forked**, and the closest thing to an "official Anthropic" open-source memory primitive at the MCP layer (distinct from the API-level [[anthropic-memory-tool]]).

> **Authority:** this is the official reference implementation in the canonical MCP repo — normative for the MCP knowledge-graph data model and tool surface. The README self-describes it as "basic": no vector search, no ranking, no multi-user isolation, no versioning, no auth.

## Data model

Persisted to a local **JSONL** file (`memory.jsonl`, configurable via `MEMORY_FILE_PATH`). Three first-class concepts:

- **Entities** — primary nodes: `name` (unique id), `entityType` (e.g. "person", "organization", "event"), `observations` (array of strings).
- **Relations** — directed edges: `from`, `to`, `relationType`. Constraint: *"always stored in active voice."*
- **Observations** — atomic fact strings attached to an entity; *"should be atomic (one fact per observation)"*; added/removed independently.

## Tools

Nine MCP tools: `create_entities`, `create_relations`, `add_observations`, `delete_entities` (cascades to relations), `delete_observations`, `delete_relations`, `read_graph` (dumps the whole graph), `search_nodes`, `open_nodes` (lookup by name).

## Retrieval

**Keyword/string search — no vectors, no semantic similarity, no ranking.** `search_nodes` searches over entity names, entity types, and observation content; `open_nodes` is direct-by-name; `read_graph` returns everything unfiltered. This puts it on the same retrieval footing as the community fork (keyword over JSONL), far simpler than the vector/graph systems ([[mem0]], [[graphiti]], [[cognee]]).

## Doctrine & relationship to the community fork

**Doctrine:** the server itself is schema-only storage; the **LLM does the extraction** — a bundled example system prompt instructs the model to retrieve the graph at session start, identify new facts during conversation (identity, behaviours, preferences, goals, relationships up to 3 degrees), and write them back as entities/relations/observations. So the *stored* content is atomic verbatim-ish fact strings, but *what to store* is LLM-decided — an extraction posture. See [[conflicts/verbatim-vs-extracted-memory]].

**Relationship to the fork:** the community `mcp-knowledge-graph` (shaneholloman) — covered as a tool entry in [[claude-code-memory-ecosystem]] — retained this server's JSONL storage and entity/relation/observation schema but renamed all endpoints with an `aim_*` prefix and added project-local/global path options. This page is the authoritative upstream; the fork is a downstream redistribution with a different tool surface.

## Source

- `raw/research/oss-agent-memory/06-mcp-memory-server-official.md` (https://github.com/modelcontextprotocol/servers/tree/main/src/memory) — official README; reference implementation. Captured 2026-05-24.

## Related

- [[claude-code-memory-ecosystem]] — the practitioner hub; covers the `mcp-knowledge-graph` community fork of this server.
- [[anthropic-memory-tool]] — Anthropic's *API-level* memory primitive (file-system commands over `/memories`); distinct from this self-hosted MCP server.
- [[graphiti]] / [[cognee]] — far richer knowledge-graph memory systems (temporal, vector-augmented) vs this "basic implementation."
- [[mempalace]] — also keeps an entity/relation KG, but with verbatim drawers + vector search on top.
- [[conflicts/verbatim-vs-extracted-memory]] — LLM-decides-what-to-store extraction posture.
- [[memory-architectures]] — the "KG + keyword retrieval" cell of the taxonomy.
