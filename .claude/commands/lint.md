# Wiki Lint

Perform a health check of the wiki.

## Process

1. **Read all wiki pages** — glob `wiki/**/*.md` and read each file.

2. **Check for orphan pages** — pages with no inbound `[[wiki-link]]` references. `index.md`, `CLAUDE.md`, and tracking files are exempt.

3. **Check for broken links** — `[[wiki-link]]` references pointing to pages that don't exist.

4. **Check for missing cross-references** — concepts mentioned in body text that have their own page but aren't linked on first mention.

5. **Check for contradictions** — statements on one page that conflict with statements on another. Pay attention to pages that cite the same raw source.

6. **Check for coverage gaps** — important concepts discussed in `raw/` source documents that have no wiki page or are only mentioned in passing.

7. **Check for stale content** — pages that reference outdated tools, deprecated practices, or unresolved TODOs.

8. **Check page format compliance** — every page must have: `# Title`, summary paragraph, `## Source` section, `## Related` section with `[[wiki-link]]`s.

<!-- DOMAIN-SLOT: domain-lint-checks -->
9. **Domain-specific checks** — bootstrap replaces this section with checks appropriate to the wiki's domain. Examples: for history, flag pages missing date frontmatter; for code standards, flag references to deprecated libraries; for cooking, flag recipes missing prep time.
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

### Contradictions
- ...

### Coverage Gaps
- ...

### Stale Content
- ...

### Domain-Specific Issues
- ...
```

After presenting the report, ask: "Would you like me to fix any of these issues?"

If the user says yes, fix the issues, then update `wiki/revisions.md` and `wiki/log.md` with a lint entry.
