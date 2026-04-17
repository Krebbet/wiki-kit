# Raw Sources

This directory contains the **immutable** source documents for the wiki. The LLM reads from here but **never** modifies these files.

## Conventions

- **One file per source.** A captured article, a PDF, a transcript — each lives in its own markdown file with frontmatter.
- **Capture tools write here.** `tools/capture_url.py`, `tools/capture_pdf.py`, and `tools/fetch_transcript.py` default to `raw/research/<topic-slug>/`.
- **Assets are co-located.** Images and other binary assets extracted from sources live in `raw/research/<topic-slug>/assets/` and are referenced by relative path from the markdown file.
- **Numbered filenames.** Capture tools write `NN-<slug>.md` and auto-increment NN against existing files in the target directory.

## What lives where

- `raw/research/<topic>/` — sources captured via `/research`.
- `raw/<your-own-subdir>/` — sources you drop in manually. Feel free to organise however makes sense for your workflow.

## Why immutable

The wiki is generated from these sources. If the raw text changes, the wiki's citations become wrong. Keep sources untouched; if a source is superseded, capture the new version as a new file and update the wiki.
