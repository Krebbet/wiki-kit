# Harvest Kit Improvements to Main

Promote generic kit improvements (bug fixes, tool changes, better command instructions) from a topic-wiki branch back into `main`, without carrying any domain-specific content.

Run this periodically on a topic-wiki branch to keep `main` evolving as a clean template. New wikis cloned from `main` then inherit the improvements.

## When to run

- After you've fixed a capture bug, improved a tool, or sharpened a command's instructions while working on a topic wiki.
- Before wrapping up a long research session, to surface any general-purpose learnings that deserve to live in the kit.
- Any time `master_notes.md` has entries marked `Status: open` or `Status: proposed` that are scoped to `project` or `both` and touch `.claude/commands/` or `tools/`.

## What it promotes

**Kit paths (candidates for promotion):**
- `tools/**`
- `tests/**`
- `.claude/commands/*.md` — **but see DOMAIN-SLOT handling below**
- `pyproject.toml`, `poetry.lock`
- `README.md`, `llm-wiki.md`
- Any new top-level tooling files

**Never promotes:**
- `wiki/**` (content)
- `raw/**` (sources)
- Session artifacts: `STATE.md`, `FEEDBACK.md`, `master_notes.md`, `boot_stap_instructions.md` / `bootstrap_instructions.md`
- `wiki/CLAUDE.md` placeholder fills (bootstrap output)
- DOMAIN-SLOT body content in command files
- **Deletion of `.claude/commands/bootstrap.md`** — the bootstrap command self-deletes by design after running, so on any post-bootstrap topic branch the file is absent. Promoting that deletion would strip bootstrap from `main` and break every future new-wiki clone. Always treat this deletion as a session artifact.

## Process

1. **Pre-check.** Verify the current branch is not `main`. If it is, stop with:

   > Nothing to harvest — already on main.

   Verify the working tree is clean (`git status --short` returns nothing). If dirty, ask the user to commit or stash first; the harvest process switches branches.

2. **Classify changes.** Diff the current branch against `origin/main` (fall back to `main` if no remote):

   ```bash
   git fetch origin main
   git diff origin/main...HEAD --name-status
   ```

   For each changed file, classify into one of four buckets:
   - **promote** — kit paths as listed above, excluding DOMAIN-SLOT bodies.
   - **skip-content** — `wiki/**`, `raw/**`.
   - **skip-session** — `STATE.md`, `FEEDBACK.md`, `master_notes.md`, `boot_stap_instructions.md`, `wiki/CLAUDE.md`.
   - **review** — anything else (new top-level files, unusual paths). Present these to the user to classify manually.

3. **DOMAIN-SLOT handling** (applies only to `.claude/commands/*.md`).

   Command files have regions between `<!-- DOMAIN-SLOT: name -->` and `<!-- /DOMAIN-SLOT -->` markers that bootstrap filled with domain-specific content. Changes inside those regions are content — do not promote. Changes outside those regions are kit improvements — promote.

   For each command file in the **promote** bucket, compare against `origin/main` and split the diff:
   - **Kit delta:** changes outside any DOMAIN-SLOT region. Promote.
   - **Slot delta:** changes inside a DOMAIN-SLOT region. Skip.

   If the two overlap (unusual — a single hunk spans the marker), present the hunk to the user for manual decision.

4. **Present summary.** Show the user:

   ```
   Kit harvest summary
   -------------------
   Promote (N files):
     - tools/capture_pdf.py        (modified)
     - tools/audit_captures.py     (new)
     - tests/test_audit_captures.py (new)
     - .claude/commands/lint.md    (kit delta only, DOMAIN-SLOT unchanged)

   Skip (content, M files):
     wiki/**, raw/**, ... (counts)

   Skip (session, K files):
     STATE.md, FEEDBACK.md, ...

   Review (L files):
     - <path>  — unclassified, please advise
   ```

   Ask: "Proceed with this harvest? (y/N, or list files to exclude)"

5. **Review master_notes.** Read `master_notes.md`. Find entries with `Status: open` or `Status: proposed` that are scoped to `project` or `both`. For each, judge whether the implication can be delivered as a kit-level code or doc change right now (e.g., "add STATE.md convention to wiki/CLAUDE.md template", "add marker GPU env-var fallback to capture_pdf.py"). Propose these as additional commits beyond the file-level diff. Ask the user to approve each.

6. **Execute.** Once approved:

   a. Create a harvest branch off main:
      ```bash
      git switch -c kit-harvest-$(date +%Y-%m-%d) origin/main
      ```
      (If the branch name already exists from an earlier harvest today, append `-v2`, `-v3`, etc.)

   b. For each file in the **promote** bucket that isn't a command file:
      ```bash
      git checkout <topic-branch> -- <path>
      ```

   c. For each command file with only a kit delta (no SLOT changes):
      ```bash
      git checkout <topic-branch> -- <path>
      ```

   d. For each command file with both kit and SLOT changes: promote the kit delta only. Read both versions, splice the kit changes into the main version by hand, leaving the SLOT body as it is on main.

   e. Stage and commit. Prefer **one commit per logical change** (e.g., one commit for "fidelity audit tool" bundling `tools/audit_captures.py` + its tests + the `/lint` + `/research` hooks; separate commit for unrelated tool fixes). Reuse the original branch's commit message where possible (cite it: `Cherry-picked file-only from <sha> on <branch>`).

   f. Commit any master_notes-derived additional changes from step 5 as further commits.

7. **Verify.** Run fast tests:
   ```bash
   poetry run pytest tests/ -q -m 'not slow'
   ```
   If anything fails that the harvest introduced, fix it. If the failures are pre-existing network-dependent smoke tests, note that for the user but proceed.

8. **Merge to main.** Ask the user for final sign-off, then:
   ```bash
   git switch main
   git merge --ff-only kit-harvest-YYYY-MM-DD
   git push origin main
   git branch -d kit-harvest-YYYY-MM-DD
   ```
   If fast-forward fails (main has diverged), stop and surface the problem — the user probably harvested from another wiki in the meantime. Suggest a rebase.

9. **Return to the topic branch.**
   ```bash
   git switch <topic-branch>
   ```

   Remind the user:
   > Kit improvements are now on main. To pick them up on this topic branch, run `git merge origin/main` (or rebase). Repeat for your other topic wikis so they all share the latest kit.

## Flagging opportunities mid-session

If, while doing wiki work, you fix a tool bug or improve a command in a way that is clearly generic (not domain-specific), proactively say:

> This looks like a kit-level improvement — worth flagging for the next `/harvest` run. (Logging to `master_notes.md`.)

Then append a short note to `master_notes.md` under the current date with `Status: open`. That makes the learning discoverable at harvest time and prevents good fixes from getting buried in content commits.
