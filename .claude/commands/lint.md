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
10. **Domain-specific checks** — collective-consumer-action wiki:
    a. **Source metadata present** — every source file cited in the wiki must have its origin / intended audience / purpose / trust tag recorded on at least one wiki page (typically the page where the source is the primary basis). Pages that cite a source already-metadata'd on another page may defer with a one-line pointer instead of duplicating the full metadata, provided the deferral is explicit (e.g., a disclaimer noting where the canonical metadata lives). Missing metadata *entirely* — i.e., a source with no full metadata on any page — is a lint failure.
    b. **Conceptual cross-links** — pages on specific tools or orgs link to the counter-power mechanism they embody (collective bargaining, co-op, class action, regulation, exit-alternative, transparency tool, boycott, tech workaround). The mechanism graph matters as much as the citation graph.
    c. **Industry ↔ counter-power balance** — for each industry or extraction mechanism covered, flag if no page exists on counter-power tactics against it (and conversely, a tactic page with no industry it's deployed against).
    d. **Claim attribution** — specific or numeric claims (pricing incidents, company actions, court rulings, policy effects) cite the primary source, not a second-hand summary that cites the primary source.
    e. **Stale tech check** — pages on specific tools, apps, platforms, or companies flagged if their only sources are older than 2 years. This space moves fast; tools die, companies pivot, regulations change. Foundational concept pages are exempt.
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

**Persist the report before presenting it.** Write the full report to `wiki/lint-reports/YYYY-MM-DD.md` (creating the directory if needed; if a report for today already exists, append `-v2`, `-v3`, etc. to the filename). Then present the report inline in chat along with a pointer to the persisted file — the user wants a durable artefact they can review separately from the conversation.

**After presenting the report:**

1. **Auto-ingest un-ingested raw sources.** Under the **Coverage Gaps** section, distinguish two categories of gaps:
   - *Conceptual gaps* — concepts discussed in an already-ingested source that are thin or missing on the wiki. These need human judgement; surface them for the user and do nothing automatic.
   - *Un-ingested raw sources* — files under `raw/` that have no corresponding coverage in any wiki page (no `## Source` entry pointing to them). For each such file, run the `/ingest` process inline on it. Apply the same phase-transition signposting as `/research` step 6:

     > — lint identified un-ingested source: `<path>`; running ingest —

     Proceed with `/ingest`'s process on that file: read it, discuss takeaways, wait for user input on emphasis, write or update wiki pages, update tracking. When that file's ingest ends, announce:

     > — ingest of `<path>` complete; returning to lint —

     Repeat for each un-ingested source.

2. **Remaining issues.** Ask: "Would you like me to fix any of the other issues in the report?" (broken links, format compliance, stale content, etc.). If yes, apply fixes.

3. **Tracking.** Whether the user accepts any fixes or not, append an entry to `wiki/revisions.md` recording the lint run and update `wiki/log.md` with a dated lint entry. The persisted report file is the durable artefact; the tracking files record that the run happened.

## Harvest checkpoint

Before finishing, ask: did this lint surface anything that would help *any* wiki, not just this one? Examples: a new class of issue worth adding as a generic lint check, a pattern in orphans suggesting `/ingest` or `/research` could be smarter, a bug in `audit_captures`. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline so the user sees the flag. `/harvest` will pick it up.
