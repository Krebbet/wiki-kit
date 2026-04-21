# wiki-kit

## What this is

A starter kit for personal and team knowledge wikis maintained by an LLM, following the [llm-wiki pattern](llm-wiki.md).

Clone it, answer seven questions, and you have a working wiki tailored to your domain — schema, commands, and capture tooling all in place.

## Quickstart

```bash
git clone --single-branch --branch main <this-repo> wiki-<topic>
cd wiki-<topic>
git checkout -b <topic>-wiki
poetry install
poetry run playwright install chromium
claude
```

Then inside Claude Code: `/bootstrap`

`/bootstrap` interviews you about your domain (or synthesises from a `boot_strap_instructions.md` file at repo root if you prefer writing your answers in one go), tailors the schema and the four operational commands, then **deletes itself** so you don't accidentally re-run it. (To redo bootstrap: `git restore .claude/commands/bootstrap.md`.)

## Running multiple wikis

Each wiki is its own clone with its own topic branch. The kit's `main` is the template; topic branches carry domain-specific content. Never merge a topic branch back to `main` — that mixes content into the template.

```
~/code/wiki-<topic-a>/   # clone, on branch <topic-a>-wiki
~/code/wiki-<topic-b>/   # clone, on branch <topic-b>-wiki
...
```

When you fix a kit-level bug or improve a command while working on a topic wiki, use `/harvest` to promote the generic parts back to `main` without dragging content along. Other topic wikis then `git pull origin main` + merge to pick up the improvement.

The loop:

1. Work in a topic wiki.
2. Notice a generic fix/improvement (or find one in `master_notes.md`).
3. Run `/harvest` — it classifies your diff, promotes only kit paths (and only the non-`DOMAIN-SLOT` parts of commands), merges to `main`, pushes.
4. In every other topic wiki: `git pull origin main && git merge origin/main`.

## Repo tour

- `llm-wiki.md` — the pattern this kit instantiates (read this to understand the philosophy).
- `.claude/commands/` — the four operations (`/ingest`, `/query`, `/research`, `/lint`) and `/bootstrap`. Generic scaffolds get rewritten by `/bootstrap` to fit your domain.
- `tools/` — Python scripts that the commands shell out to: URL capture with image download, PDF capture (academic papers supported), YouTube transcript fetch.
- `wiki/` — where the LLM writes. Ships flat; topical subdirectories emerge from your first few ingests.
- `raw/` — where source material lives. Immutable by convention (the LLM reads but never edits).

## The four operations

- `/ingest <path>` — process a raw source file into the wiki.
- `/research <topic>` — find sources on the web, capture them, integrate via `/ingest`.
- `/query <question>` — answer from the wiki with citations; optionally file the answer back as a new page.
- `/lint` — health-check the wiki for orphans, broken links, contradictions, and gaps.

Plus two meta-commands:

- `/bootstrap` — one-shot setup for a fresh clone (self-deletes).
- `/harvest` — promote generic kit improvements from a topic branch back to `main`.

## First-run notes

- On first PDF capture, `marker-pdf` downloads ~1–2 GB of ML model weights (cached thereafter). If you don't need academic-paper quality, pass `--engine pymupdf` to `capture_pdf.py` for a lightweight alternative.
- `poetry run playwright install chromium` downloads a headless Chromium binary (~150 MB) once. Needed for the JS-rendered fallback in `capture_url.py`.

## Philosophy

The llm-wiki pattern treats your knowledge base as a compounding artifact. You curate sources, the LLM does the grunt work — summarising, cross-referencing, filing, bookkeeping. Read `llm-wiki.md` for the full argument.

## License

MIT.
