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

### 2026-04-24 — /research silently fails when poetry venv not synced
**Scope:** kit
**Observation:** First `/research` run on a fresh wiki clone (this wiki) fired all 10 `capture_pdf` invocations before any of them could run — each exited immediately with `ModuleNotFoundError: No module named 'httpx'`. The venv existed at `~/.cache/pypoetry/virtualenvs/wiki-kit-*-py3.13` but `poetry install` had never been run, so declared deps weren't installed. The failure mode is fast and cheap (no network, no marker weights) but the orchestration still walked through all 10 captures producing identical errors before stopping.
**Implication:** `/research` (or `/bootstrap`) should smoke-check the venv before firing captures — either an `import` probe (`poetry run python -c "import httpx, marker, playwright"`) or a one-shot `poetry install` at the top of `/research` on its first invocation per session. Alternatively, `capture_pdf.py` / `capture_url.py` could catch `ModuleNotFoundError` and print a pointed hint ("run `poetry install`") rather than a raw traceback. The kit-level fix is cheaper than every new wiki tripping over the same gap.
**Status:** open

