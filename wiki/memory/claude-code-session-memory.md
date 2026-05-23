# Claude Code Session Memory

> **⚠️ DISPUTED — read first (curator ruling 2026-05-23).** The wiki's working position is that **Claude Code does not have native session-to-session memory.** This contradicts the central claim of this page. The page is built entirely from a single community/practitioner blog (claudefa.st); its description of an "automatic background memory layer" is **not corroborated by any primary Anthropic source** and is contradicted by the MindStudio practitioner survey, whose FAQ states Claude Code has no native cross-session memory (`raw/research/cc-memory-ecosystem/06-mindstudio-comparison.md`). Treat everything below as *what that one blog claimed*, **not** as established Claude Code behaviour, pending a primary-source confirmation. The persistence approaches that practitioners actually rely on — `CLAUDE.md`, the markdown "memory bank", and external MCP-server stores — are catalogued at [[claude-code-memory-ecosystem]]; their existence is itself evidence that the gap this page describes as "filled" is in fact open.

This page (below the banner) records the now-disputed claim that Claude Code has an **automatic background system** for cross-session context — watching the conversation, extracting important parts on a token-based cadence, writing structured summaries to disk, and injecting relevant past summaries into new sessions with the framing *"from PAST sessions that might not be related to the current task"*, with a `/remember` command said to bridge Session Memory → `CLAUDE.local.md`. Per the curator ruling, **no native feature of this kind is treated as real by the wiki.**

> **Original source caveat (retained):** this page is built from a community/practitioner blog (claudefa.st), not Anthropic's official docs. Specific claims about Statsig flag names (`tengu_session_memory`, `tengu_sm_compact`), version numbers (v2.0.64, v2.1.30/2.1.31), and exact token thresholds (10k/5k) are practitioner-level claims not verifiable against Anthropic's official sources — and, per the 2026-05-23 ruling, the existence of the feature itself is now in question.

## What you'll see in the terminal

- **"Recalled X memories"** — appears at session start; Claude has loaded summaries from previous sessions in this project.
- **"Wrote X memories"** — appears periodically during the session; Claude saved a snapshot of current work.

Both include `(ctrl+o to expand)` so the user can inspect what was recalled or written.

## Storage

Session summaries are stored as structured Markdown files. Each session gets its own directory with its own summary file. Files accumulate over time, building a project-level history.

## Extraction cadence

- **First extraction**: after roughly **10,000 tokens** of conversation.
- **Subsequent updates**: every **~5,000 tokens** or after **every 3 tool calls** — whichever comes first.

Short/trivial sessions produce minimal summaries; deep architecture sessions produce detailed ones. The cadence keeps summaries useful without burning compute on trivial exchanges.

## Cross-session recall

When a new session starts, Claude injects relevant past session summaries into context with the explicit framing: *"from PAST sessions that might not be related to the current task."* Treated as background reference, not as active instructions — providing continuity without rigidity. *"Claude won't blindly follow decisions from three weeks ago. It treats past sessions as reference material, giving you the continuity of context without the rigidity of hard-coded instructions."*

## What gets remembered

Each summary follows a consistent structure:

- **Session title** — auto-generated description (e.g., *"Implement user dashboard with role-based access"*).
- **Current status** — completed items, discussion points, open questions.
- **Key results** — important outcomes, decisions made, patterns chosen.
- **Work log** — chronological record of actions taken.

The summary captures *what* and *why*, not a transcript of every message. *"A two-hour session becomes a focused summary that Claude can load in seconds."*

## The /remember command

Bridges Session Memory → `CLAUDE.local.md`. When run, Claude reviews stored session summaries, identifies recurring patterns across sessions, and proposes additions to `CLAUDE.local.md`. The user confirms each proposed addition before it is written. Example: if the same coding correction appears across three sessions (*"always use server actions instead of API routes"*), `/remember` surfaces it as a candidate for permanent memory. The blog calls it *"the bridge between automatic memory and deliberate configuration."*

## Instant compaction

Before Session Memory existed, `/compact` required up to two minutes — Claude re-analysed the full conversation to produce a summary. Now `/compact` is instant: it loads the pre-written background summary into a fresh context window. *"Your context management workflow gets faster and more reliable. ... Instead of dreading the compaction pause when you hit 80% context usage, you can compact freely. The summary is always ready."*

## Availability

- **First-party Anthropic API only.** Claude Pro or Max subscription works automatically. Bedrock, Vertex, Foundry users do not have access — the feature requires Anthropic's native API infrastructure.
- **Statsig feature flags**: `tengu_session_memory` (core feature); `tengu_sm_compact` (instant compaction). Gradual rollout — supported-plan users without the flag enabled won't see messages yet.
- **Timeline**: underlying system since approximately v2.0.64 (late 2025); visible terminal messages since v2.1.30 / v2.1.31 (early February 2026).

## Session Memory vs CLAUDE.md

| Aspect | Session Memory | CLAUDE.md |
|---|---|---|
| Created by | Claude (automatic) | You (manual) |
| Scope | Per-session snapshots | Persistent project rules |
| Priority | Background reference | High-priority instructions |
| Best for | Continuity, context recall | Standards, architecture, commands |

The strongest setup uses both. Session Memory provides continuity between work sessions; CLAUDE.md provides authoritative rules. The `/remember` command bridges the two by promoting recurring patterns from session memory into permanent configuration.

## Maximisation tips

The blog recommends:
- **State intent early**: *"I'm building the payment integration using Stripe"* gives Claude a clear session title.
- **Summarise decisions explicitly**: *"We decided on webhook-based sync instead of polling"* becomes a key result.
- **Ask Claude to document**: *"Document the architecture decisions we just made"* triggers a richer extraction.

## Relationship to neighbouring wiki pages

- **Product-layer expression of [[anthropic-memory-tool]].** The API-level Memory tool gives developers a primitive (`/memories` directory + 6 file commands); Session Memory is the Claude-Code-product-specific orchestration on top of that primitive — automated extraction, structured-summary schema, cross-session injection, the `/remember` promotion path.
- **Operational answer to the [[anthropic-internal-study]] cold-start problem.** The 132-engineer Anthropic study (August 2025) named cold start as the main friction limiting wider delegation; Session Memory shipped Q4 2025 as the answer.
- **`/remember` is the practitioner's bridge between [[codified-context]]'s spec-staleness problem and continuous practice.** Codified Context flagged spec staleness as the primary failure mode; `/remember` creates a promotion path from implicit repeated practice to explicit written rule, addressing the failure mode at the source.

## Source

- `raw/research/memory-management/03-08-claude-code-session-memory.md` (captured 2026-04-26 from https://claudefa.st/blog/guide/mechanics/session-memory — community/practitioner blog, not official Anthropic documentation)

## Related

- [[claude-code-memory-ecosystem]] — the persistence approaches practitioners actually use *because* there is no native cross-session memory; the page that supersedes this one's premise.
- [[anthropic-memory-tool]] — API-level primitive Session Memory is built on.
- [[memgpt]] / [[letta-memory-blocks]] — paradigm ancestors; Session Memory's automated extraction + structured summary format echoes the working-context update discipline.
- [[anthropic-internal-study]] — names the cold-start problem this feature operationally addresses.
- [[codified-context]] — `/remember` is the answer to its spec-staleness failure mode at the practitioner-discipline level.
- [[memory-architectures]] — Session Memory fits the *context-resident compression* family (background extraction + summary injection).
