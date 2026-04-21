# Wiki Lint

Perform a health check of the wiki.

## Process

1. **Read all wiki pages** — glob `wiki/**/*.md` and read each file.

2. **Check for orphan pages** — pages with no inbound `[[wiki-link]]` references. `index.md`, `CLAUDE.md`, `revisions.md`, and `log.md` are exempt.

3. **Check for broken links** — `[[wiki-link]]` references pointing to pages that don't exist.

4. **Check for missing cross-references** — concepts mentioned in body text that have their own page but aren't linked on first mention.

5. **Check for conflicts** — statements on one page that conflict with statements on another. Pay attention to pages that cite the same raw source. Cross-reference any open files in `wiki/conflicts/`.

6. **Check for coverage gaps** — important concepts discussed in `raw/` source documents that have no wiki page or are only mentioned in passing.

7. **Check for stale content** — pages that reference outdated tools, deprecated practices, or unresolved TODOs.

8. **Check page format compliance** — every page must have: `# Title`, summary paragraph, `## Source` section, `## Related` section with `[[wiki-link]]`s.

9. **Audit raw capture fidelity** — for every topic directory under `raw/`, run:

   ```bash
   poetry run python -m tools.audit_captures raw/<topic-dir>
   ```

   The tool checks: (a) every image ref in each captured markdown resolves to a real file, (b) every captured markdown has a paired source PDF in `pdfs/`, (c) markdown size is sane vs source PDF page count, (d) no image filename is referenced by more than one markdown (cross-paper overwrite indicator). Include any non-zero issues in the lint report under the **Capture Fidelity** section. Captures with broken refs or thin extractions are likely silent failures of `capture_pdf` and need re-capture before downstream synthesis can be trusted.

<!-- DOMAIN-SLOT: domain-lint-checks -->
10. **Domain-specific checks** — bootstrap replaces this section with checks appropriate to the wiki's domain. Examples: for history, flag pages missing date frontmatter; for code standards, flag references to deprecated libraries; for cooking, flag recipes missing prep time.
<!-- /DOMAIN-SLOT -->

## Output

Produce a structured lint report:

```
## Lint Report — [date]

### Orphan Pages
- ...

### Broken Links
- ...

### Missing Cross-References
- ...

### Format Issues
- ...

### Conflicts
- ...

### Coverage Gaps
- ...

### Stale Content
- ...

### Domain-Specific Issues
- ...

### Capture Fidelity (raw/)
- ...
```

After presenting the report, ask: "Would you like me to fix any of these issues?"

If the user says yes, fix the issues, then update `wiki/revisions.md` and `wiki/log.md` with a lint entry.

## Harvest checkpoint

Before finishing, ask: did this lint surface anything that would help *any* wiki, not just this one? Examples: a new class of issue worth adding as a generic lint check, a pattern in orphans suggesting `/ingest` or `/research` could be smarter, a bug in `audit_captures`. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline so the user sees the flag. `/harvest` will pick it up.
