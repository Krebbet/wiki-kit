# wiki-kit Execution Handoff

**Written:** 2026-04-17, paused mid-execution for restart in new Claude instance.

**Purpose:** Let a fresh Claude instance resume execution of the wiki-kit build plan without losing context.

---

## What This Is

The user is building `wiki-kit` — a standalone starter-kit git repo at `/home/david/code/wiki-kit/` that instantiates the llm-wiki pattern. Users clone it, run `poetry install`, then `/bootstrap` in Claude Code to tailor the wiki to their domain.

The build was scoped via the brainstorming skill (→ spec) and writing-plans skill (→ plan), and execution is via the subagent-driven-development skill.

**Key docs:**
- Spec: `/home/david/code/coding_standards/docs/superpowers/specs/2026-04-17-wiki-kit-design.md`
- Plan: `/home/david/code/coding_standards/docs/superpowers/plans/2026-04-17-wiki-kit.md`
- Task state: `/home/david/code/coding_standards/docs/superpowers/plans/2026-04-17-wiki-kit.md.tasks.json`
- llm-wiki pattern manifesto: `/home/david/code/coding_standards/llm-wiki.md`

The new Claude should **re-read the spec and plan first** — do NOT rely solely on this handoff.

---

## How to Resume (short version)

1. Read the plan doc fully.
2. Read the `.tasks.json` for completed/pending status.
3. Read the "Pending Fixes" section below to pick up Task 6's unresolved code-quality issues.
4. Invoke `Skill: superpowers-extended-cc:subagent-driven-development` to continue dispatching.
5. Continue from Task 6 fix → Task 7, 8, 9–13, 14, 15.

---

## Current State (as of pause)

**Repo:** `/home/david/code/wiki-kit/` exists on branch `main`, Python env installed via Poetry, Chromium binary installed. 6 commits:

```
9253d6b feat: add capture_url tool with _common helpers and tests
d34d3b7 chore: add Playwright MCP config
b1f64be feat: add raw/ directory with immutability convention
cfdc158 feat: add wiki/ scaffolding with tracking files
b21140a docs: add README and llm-wiki manifesto
69aaeb0 chore: initial repo with Poetry env and MIT license
```

**Plan tasks completed (spec + code-quality reviews passed):**
- **Task 1** — Repo init, Poetry, LICENSE, .gitignore ✅
- **Task 2** — README + llm-wiki.md ✅ (one fix iteration — added missing `## What this is` heading and aligned "four operations" terminology)
- **Task 3** — wiki/ skeleton ✅
- **Task 4** — raw/ dir with README ✅
- **Task 5** — .mcp.json (Playwright MCP config) ✅

**Plan tasks in progress:**
- **Task 6** — `tools/capture_url.py` + `tools/_common.py` + tests. Spec review ✅. Code quality review surfaced issues (see below). **NOT yet marked completed — fix these first.**

**Plan tasks pending:**
- Task 7 — `tools/capture_pdf.py`
- Task 8 — `tools/fetch_transcript.py`
- Task 9 — `/ingest` command
- Task 10 — `/query` command
- Task 11 — `/lint` command
- Task 12 — `/research` command (depends on 6, 7, 8)
- Task 13 — `wiki/CLAUDE.md` template
- Task 14 — `/bootstrap` command (depends on 9–13)
- Task 15 — End-to-end dry run (needs interactive Claude Code session — user runs manually)

---

## Pending Fixes on Task 6 (code-quality review issues)

The Task 6 code-quality reviewer (run against commit `9253d6b`) flagged these. Fix before marking Task 6 complete.

**Important (fix before merge):**

1. **`_main_content_html` regex-based close-tag matcher truncates on nested `<div>`.** In `/home/david/code/wiki-kit/tools/capture_url.py:79` the current logic finds the first closing `</div>` which will close a `<div role="main">` at the first nested div. Fix options: (a) drop `<div role="main">` from the candidate-tag list (simplest), or (b) switch to a real HTML parser (e.g. `selectolax` or `lxml`) for this one function.

2. **`_rewrite_images` regex doesn't handle markdown image titles** (`![alt](url "title")`). Current regex: `r"!\[([^\]]*)\]\(([^)]+)\)"` — captures `url "title"` as the URL. Replace with `r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)'`. Low practical impact (trafilatura doesn't emit titles) but easy fix.

3. **`assets_dir` frontmatter reports empty directory when all image downloads fail.** In `/home/david/code/wiki-kit/tools/capture_url.py:38`, replace `assets_dir.exists()` with `assets_dir.exists() and any(assets_dir.iterdir())`.

4. **Test coverage gaps in `_common.py`:** add tests for `download_asset` (dedupe branch, failure branch), `_guess_ext` (branches), `write_frontmatter` (None-skip branch), `slugify` (`max_len` truncation).

**Minor (nice-to-have, not blockers):**

5. `_guess_ext` cascade → tuple-list lookup (readability).
6. `download_asset` should log failures to stderr before returning None (currently silent).
7. `_extract_with_playwright` normalize empty title to None.
8. `write_frontmatter` should YAML-escape string values (latent bug when title contains `:` or `"`).
9. `from __future__ import annotations` is cargo-cult in a 3.10+ codebase.
10. Smoke test could assert body content (e.g., `# Example Domain`).
11. `out_path.write_text(..., encoding="utf-8")` for Windows safety.

**Full review text:** see prior conversation transcript. Priorities for the fix dispatch: items 1, 3, 8 (latent bugs), then 4 (test coverage). Items 2, 5, 6, 7, 9, 10, 11 are optional polish.

---

## Sandbox Environment Note

**The subagent execution environment has no outbound network access.** Smoke tests marked `@pytest.mark.network` (`tests/test_capture_url.py` and the equivalents for Tasks 7–8) will fail with `net::ERR_NAME_NOT_RESOLVED`. This is environmental, not a code defect. Future subagent prompts should:
- Tell the subagent upfront that network tests can't run there.
- Tell them to focus on code correctness + unit tests (non-network).
- Rely on the user's Task 15 end-to-end dry run (manual, in their networked shell) to cover end-to-end verification.

---

## Decisions / Preferences Established During the Build

- **Poetry, not uv or pip-tools** for Python dependency management. Saved to memory at `/home/david/.claude/projects/-home-david-code-coding-standards/memory/feedback_python_env.md`.
- **`marker-pdf` is the default PDF engine** (not `pymupdf4llm`), because the user expects scientific papers as a main source. `pymupdf4llm` is the optional `--engine pymupdf` fallback.
- **Bootstrap self-deletes** its own command file after success. Recovery is `git restore .claude/commands/bootstrap.md`.
- **Bootstrap rewrites DOMAIN-SLOT regions** (`<!-- DOMAIN-SLOT: name -->...<!-- /DOMAIN-SLOT -->`) in `/ingest`, `/query`, `/research`, `/lint` and replaces `{{placeholders}}` in `wiki/CLAUDE.md`.
- **wiki/ ships flat**. Topical subdirectories emerge from ingests, not pre-seeded.
- **Tools are Python scripts in `tools/`**, not new MCPs. Commands shell out via `poetry run python -m tools.capture_url ...`.
- **Task 3 small deviation to accept as-is:** `wiki/log.md` has a one-line subtitle that the strict spec-reviewer flagged as an overage; the plan text itself included that subtitle, so the code matches the plan. Not worth changing.

---

## Suggested Next Actions for the Fresh Claude

1. **Orient.** Read:
   - This file.
   - The plan: `/home/david/code/coding_standards/docs/superpowers/plans/2026-04-17-wiki-kit.md`
   - The spec: `/home/david/code/coding_standards/docs/superpowers/specs/2026-04-17-wiki-kit-design.md`
   - The `.tasks.json` for progress markers.
   - `/home/david/code/wiki-kit/` state (`git log --oneline`, `ls -la`).
2. **Invoke the subagent-driven-development skill** (`superpowers-extended-cc:subagent-driven-development`).
3. **Dispatch a fix subagent on Task 6** to address the Important items (1, 3, 8) plus the test coverage gaps (4). Use the existing commit `9253d6b` as BASE; amend or add a follow-up commit — amend is fine since it hasn't been pushed.
4. **Re-review Task 6** code quality, confirm ✅.
5. **Update `.tasks.json`** to mark Task 6 `completed`.
6. **Proceed to Task 7** (`tools/capture_pdf.py`) — the plan spec is complete; the subagent needs the task details from the plan file.
7. **Tasks 9–13 can be bundled** into a single implementer dispatch since they're all markdown command templates with no code logic. Task 14 (bootstrap) should be its own dispatch (complex instructions for an LLM-interactive flow).
8. **Task 15 is manual** — at the end, tell the user to run it themselves (clone fresh, `poetry install`, open Claude Code, `/bootstrap` with a toy domain, etc.). See plan Task 15 for the full checklist.

---

## Known Process Gotchas

- Existing native tasks in Claude Code (TaskList) don't map 1:1 to plan tasks — they're coarser. Use the `.tasks.json` as the source of truth for plan-task completion, and don't worry if native TaskList shows them as still pending.
- When dispatching fix subagents via `SendMessage` on an earlier agent ID, note that agents expire. If a prior agent is unreachable, dispatch a fresh general-purpose implementer with the fix context.
- For code-quality reviews: use `superpowers-extended-cc:code-reviewer` subagent type. For spec-compliance reviews: general-purpose is fine.
- The subagent sandbox can `rm` and edit files in `/home/david/code/wiki-kit/` freely — no worktree setup was done since wiki-kit is a *new* sibling repo, not a branch of the current repo.

---

## Cleanup When Done

Delete this file (`/home/david/code/coding_standards/wiki/wiki-kit-execution-status.md`) once the wiki-kit build is complete, OR move it to `/home/david/code/coding_standards/docs/superpowers/plans/` as an archived handoff record. It shouldn't live in `wiki/` long-term since that directory is for coding-standards wiki pages, not execution state.
