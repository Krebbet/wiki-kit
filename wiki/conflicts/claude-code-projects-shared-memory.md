# Conflict: Does Claude Code Projects' "shared memory" claim reopen the no-native-memory ruling?

**Status:** OPEN, likely a scope narrowing rather than a reopening — the new claim is scoped to a specific beta feature, not general Claude Code chat/CLI use, but neither source states the boundary precisely enough to close this outright.

Anthropic's 2026-09-20 "Projects redesigned" post states: "Every thread now adds to and draws from a shared memory, reducing the need for complex prompt engineering," citing project-level facts (a release date change, why a feature was dropped) and working-style preferences (check-in cadence, update verbosity) as examples. Read at face value, this is a claim of **native, cross-thread memory inside Claude Code** — in tension with the wiki's standing curator ruling that Claude Code has no native session-to-session memory.

## Position A — Anthropic: Projects threads share a native memory layer

From [[deployments/claude-code-projects]]: the redesigned Projects coordinator architecture gives every thread (each a full, independent Claude Code cloud session on its own branch) read/write access to a shared memory that persists project-level facts and working-style preferences across threads, explicitly framed as reducing the need for prompt engineering. No technical detail is given on storage mechanism, retention/eviction, or retrieval method (extraction vs. verbatim) — this is product-level framing, not an architecture disclosure.

## Position B — wiki curator ruling: Claude Code has no native session-to-session memory

From [[memory/claude-code-memory-ecosystem]] (ruling dated 2026-05-23, corroborated by the MindStudio survey's FAQ, and disputing [[memory/claude-code-session-memory]]'s contrary single-source claim): each Claude Code session is a fresh API conversation, so anything that must survive a session reset has to be written to an external store and re-loaded deliberately. The page's entire six-level ladder (CLAUDE.md → markdown KB → hooks → vector/RAG → cross-tool DB) exists precisely because no native persistence is available.

## Working position

The most likely reconciliation is scope, not contradiction:

- The existing ruling was made against general Claude Code session/CLI use as of its 2026-05-23 ingest date — ordinary `claude` CLI sessions and standard web/desktop chat sessions, which still have no native memory as far as any source states.
- The new claim is explicitly scoped to the **redesigned Projects feature**, currently in beta and limited to select Pro/Max subscribers — a specific coordinator-plus-threads product surface, not a general Claude Code capability.
- If this reading holds, the ecosystem page's central thesis needs a narrowing footnote ("no native memory *outside the Projects beta*"), not a reversal.

This can't be fully closed yet because: (1) the Projects post gives no technical detail on how "shared memory" is implemented — it could be a managed wrapper around the same external-store pattern the ecosystem page already documents (i.e., not truly novel, just productized), rather than a genuinely new persistence primitive; and (2) it's unclear whether Projects' shared memory will eventually generalize to non-Projects sessions, which would reopen the question for real.

Resolution rule: escalate to curator ruling once either (a) Projects' memory mechanism is documented with enough technical detail to classify it as a genuinely new native primitive vs. a managed external-store wrapper, or (b) the feature exits beta and its relationship to non-Projects Claude Code sessions is clarified.

## Source

- `raw/research/weekly-2026-09-20/05-claude-code-projects-redesign.md` — captured 2026-09-20 from `claude.com/blog/projects-redesigned` (2026-09-17). **Vendor primary.**

## Related

- [[deployments/claude-code-projects]] — source of Position A.
- [[memory/claude-code-memory-ecosystem]] — source of Position B (the standing curator ruling).
- [[memory/claude-code-session-memory]] — the earlier disputed claim the 2026-05-23 ruling superseded; if this conflict resolves toward Position A, that page's dispute banner may need revisiting too.
