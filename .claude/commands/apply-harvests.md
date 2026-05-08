# Apply Harvests

Pull kit improvements that have landed on `main` (via `/harvest` from another wiki) into the active topic-wiki branch.

Run this when you switch to a topic wiki and want to pick up kit fixes that other wikis have promoted since this branch's last harvest application. Topic branches are isolated feature branches — they never merge with `main`, so kit changes have to be applied file-by-file via this skill.

## When to run

- You've switched to a topic wiki and noticed `master_notes.md` mentions kit fixes that landed on `main` after this branch was last touched.
- A different topic wiki ran `/harvest` recently and the changes are useful here.
- Before starting a long session in a topic wiki — confirms the kit is current.

## What it does

- Updates local `main` from `origin/main` (without touching the topic branch's tracked content).
- Compares each kit path on the topic branch against `main`.
- Walks you through every diff individually (because some wikis customize kit behavior on purpose, and a blanket overwrite would clobber that intent).
- Applies the approved changes via `git checkout main -- <path>`, commits them as one apply-harvest commit on the topic branch, and pushes.

## Critical rules

- **Topic branches never `git merge main`.** All kit propagation is file-level. This preserves intentional local divergence in kit files (a wiki may have customized `weekly-brief.md` for its domain, for instance).
- **Per-change interactive review.** Default is yes/no on the whole batch; conflicts (paths that have diverged in *both* main and the topic branch since the last harvest) are presented individually.
- **Customized files are always shown.** If a kit file has been edited on the topic branch independently of any harvest application, this skill cannot tell whether incoming kit changes should overwrite, integrate, or be skipped — surface it.
- **Never touches `wiki/`, `raw/`, `master_notes.md`, or `STATE.md`.** Those are wiki-local; the kit doesn't manage them.

## Process

### 1. Pre-check

Verify current branch is not `main`:

```bash
TOPIC_BRANCH=$(git branch --show-current)
if [ "$TOPIC_BRANCH" = "main" ]; then
  echo "Nothing to apply — already on main."; exit 0
fi
```

Verify the working tree is clean:

```bash
git status --short  # must be empty
```

If dirty, ask the user to commit or stash first.

### 2. Update local main

```bash
git fetch origin main
git switch main
git merge --ff-only origin/main || { echo "main has diverged from origin — resolve manually"; exit 1; }
git switch "$TOPIC_BRANCH"
```

### 3. Identify candidate paths

Compare every kit path between the topic branch and main:

```bash
KIT_GLOBS=(
  "tools/**"
  "tests/**"
  ".claude/commands/*.md"
  "pyproject.toml" "poetry.lock"
  ".gitignore"
  "README.md" "llm-wiki.md"
)
git diff --name-only main -- "${KIT_GLOBS[@]}"
```

For each path returned, classify:

- **incoming-only** — file differs from main, but the topic branch has not modified it since its last apply-harvest commit. Default: apply.
- **customized** — the topic branch has its own modifications relative to main on this file (intentional or otherwise). Default: ask user to choose (apply / skip / merge-by-hand).
- **command-file with DOMAIN-SLOT** — same logic, but the SLOT body must be preserved on the topic branch even when the kit-delta is applied.

Detection heuristic: find this branch's last apply-harvest commit (`git log --grep "apply kit harvest from main" --pretty=format:%H -1`) — call it `LAST_APPLY`. If a path is unchanged on the topic branch between `LAST_APPLY` and HEAD, classify it incoming-only; if it changed, classify it customized.

If `LAST_APPLY` doesn't exist (this branch has never run `/apply-harvests`), use `origin/main`'s tip at the time the topic branch was created — `git merge-base origin/main "$TOPIC_BRANCH"` — as the baseline.

### 4. Present the batch

```
Apply-harvests summary (active wiki: <REPO_NAME> on <TOPIC_BRANCH>)
-------------------------------------------------------------------
Incoming-only (N files — safe defaults to apply):
  - tools/ingest_plan.py        (+3 / -1)
  - .claude/commands/research.md (+1 / -1)

Customized (M files — needs individual review):
  - .claude/commands/weekly-brief.md
      Topic branch added a wiki-specific source-priority block.
      Main updated the SMTP send template.
      Action: [a]pply main verbatim / [s]kip / [m]anual splice

Command-file with DOMAIN-SLOT (K files):
  - .claude/commands/research.md
      Kit-delta only; SLOT body will be preserved.
```

Ask: "Apply the **incoming-only** batch? (y/N)" — single yes/no for the safe set.

Then walk each **customized** path individually with the unified diff visible.

For DOMAIN-SLOT files, default to applying with SLOT preservation; only escalate if the SLOT body itself has shifted in main (rare — main is the template and SLOT bodies on main are placeholder text).

### 5. Apply

For each approved path:

```bash
git checkout main -- "$path"
```

For DOMAIN-SLOT files where the SLOT body needs preservation, do the splice manually: read the topic branch's existing version, replace only the non-SLOT regions with main's version, write back.

For "manual splice" customized files, show the user the file contents from both sides and let them dictate the resolution; don't try to auto-merge.

### 6. Commit + push the active topic branch

```bash
MAIN_SHA=$(git rev-parse main)
git add -A
git diff --cached --quiet && { echo "Nothing to apply (all approved paths were no-ops)"; exit 0; }
git commit -m "apply kit harvest from main @ $MAIN_SHA ($(date -I))"
git push origin "$TOPIC_BRANCH"
```

If the working tree is empty after step 5 (everything got skipped), exit cleanly without committing.

### 7. Update master_notes.md

If any `Status: open` or `Status: proposed` entry was satisfied by a kit fix that just landed (e.g., the topic branch's master_notes had a `Status: open` entry about a parser bug that this apply just brought in via `tools/ingest_plan.py`), flip the entry:

```
**Status:** applied 2026-05-08
```

Don't delete entries — the audit trail is the value. If unsure whether an entry maps to an applied change, leave it open and ask the user.

Commit + push as a follow-on:

```bash
git add master_notes.md
git commit -m "master_notes: flip applied entries from kit harvest @ $MAIN_SHA"
git push origin "$TOPIC_BRANCH"
```

### 8. Verify clean state

```bash
git status --short                                       # empty
git log --oneline "origin/$TOPIC_BRANCH..$TOPIC_BRANCH"  # empty (topic fully pushed)
git log --oneline main..origin/main                      # empty (main fully synced)
```

All three should be empty. Surface anything non-empty.

## Failure modes

- **`git merge --ff-only origin/main` fails on local main.** Local main has unpushed commits ahead of origin. Stop and surface — likely a forgotten harvest. The user must either push the divergent commits via `/harvest` flow, or reset main to origin if the divergence is unwanted.
- **Customized file with no clean splice.** Ask the user; never auto-merge content.
- **Apply-harvest commit conflicts on push.** Topic branch was advanced from another machine. `git fetch origin "$TOPIC_BRANCH"` + `git rebase origin/$TOPIC_BRANCH` and retry. Same conflict resolution principles as `/harvest` step 8.

## Why this skill exists

Topic branches are isolated. Kit improvements would otherwise stay invisible to long-running wikis until the user manually copied them in. This skill is the canonical, audited path: the user reviews every change, customizations are protected, and the apply commit is its own audit trail (`git log --grep "apply kit harvest from main"` shows the entire kit-evolution history per wiki).

The split between `/harvest` and `/apply-harvests` matches the asymmetry of the workflow: `/harvest` runs in the wiki where the kit fix was discovered (one wiki per fix); `/apply-harvests` runs in every other wiki when the user wants it (independently per wiki, on its own schedule).
