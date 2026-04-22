# `/ingest` smoke fixture

Two synthetic source files used to validate changes to `.claude/commands/ingest.md` and `tools/ingest_plan.py`.

## What to expect when you run `/ingest tests/fixtures/ingest-smoke/`

1. Two subagents dispatched in parallel.
2. `tests/fixtures/ingest-smoke/.ingest/` created with:
   - `01-method-a.summary.md`
   - `02-method-b.summary.md`
   - `run.json` listing both as `status: ok`.
3. Review packet includes a **Conflict flags** entry because 02-method-b's 62.1% claim on AlpacaEval contradicts 01-method-a's 50.2%.
4. **Merge candidate** entry (optional, depending on how the subagent wrote cross-ref candidates): both summaries likely name the same prior-art pages and both propose NEW pages.

## Clean up

```bash
poetry run python -m tools.clear_ingest_cache tests/fixtures/ingest-smoke
```

## Why this isn't an automated test

The subagent prompts live as prose inside `.claude/commands/ingest.md` and are executed via the Agent tool. Automating the full round-trip would require spinning up Claude Code itself, which is beyond the test-runner's scope. Manual QA suffices for this surface — log regressions to `master_notes.md` (Scope: kit).
