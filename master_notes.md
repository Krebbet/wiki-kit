# Master Notes

Running log of what works and what doesn't — both for this specific wiki's operation and for the collaboration generally. Append-only scratchpad for observations that might deserve to become CLAUDE.md guidance, command updates, or kit-level improvements.

During normal operation, Claude appends observations here with `Status: open`. At `/harvest` time (or whenever you review), entries are triaged: some become kit-level code or doc changes promoted to main via `/harvest`; some become this wiki's project CLAUDE.md updates; some are rejected; some stay open for more signal.

## Format

Append entries using this structure:

```
### YYYY-MM-DD — short title
**Scope:** project | interaction | kit | both
**Observation:** what was noticed
**Implication:** what this suggests for CLAUDE.md, a command, a tool, or process
**Status:** open | proposed | applied | rejected
```

**Scope guide:**
- `project` — specific to this wiki (lands in this wiki's `wiki/CLAUDE.md` or DOMAIN-SLOT content).
- `kit` — generic to wiki-kit itself (gets promoted to main via `/harvest`; every other wiki benefits).
- `interaction` — about how the user and assistant work together (may become memory or user-level CLAUDE.md).
- `both` — overlaps more than one scope.

## Notes

<!-- Entries appended during operation go below. -->

### 2026-04-21 — Raw source bodies in main context can trip the usage-policy classifier
**Scope:** kit
**Observation:** `/ingest` on `raw/research/post-training-alignment-2026/` (11 alignment/post-training papers) crashed mid-run with a Claude Code usage-policy 403. Cause: cumulative main-session context packed with safety-spec excerpts, jailbreak taxonomies, disallowed-content categories, and CoT traces reasoning about harmful requests — the concrete vocabulary a content classifier is tuned for, even though each source individually is a legitimate research paper. The next turn and `/compact` also 403'd because the flagged context was re-sent each call. Only a fresh session recovered.
**Implication:** `/ingest` must keep raw source bodies out of the main session. Design approved in `docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md`: subagent-per-source with coherence orchestration. Main context only ever sees distilled summaries plus the specific existing wiki pages touched by a plan. Also an input signal for `/research` tooling: the capture pipeline shouldn't feed straight into a main-session summarisation loop for topics rich in safety/alignment vocabulary.
**Status:** proposed
