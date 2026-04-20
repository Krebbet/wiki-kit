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

<!-- DOMAIN-SLOT: domain-lint-checks -->
9. **Domain-specific checks** — research-wiki for LLM fine-tuning method development:
   a. **Paper identifier present** — every page citing a paper has the ArXiv ID (e.g., `arXiv:2401.12345`) or DOI in its `## Source` section.
   b. **Conceptual cross-links** — method pages link to at least one related-method page, not only papers they cite. The conceptual graph matters as much as the citation graph.
   c. **Quantitative claims cite figures** — pages making numeric claims ("X% improvement", "Y× more sample-efficient") cite the specific table or figure number from the source.
   d. **Research-page schema** — pages under `wiki/research/` have `## Method` and `## Claims` sections in addition to the standard `## Source` and `## Related`.
   e. **Recency check for fast-moving topics** — flag pages on RL, LLM training, or post-training methods whose only sources are older than 5 years. (Foundational papers older than that are fine, but the page should also reference recent follow-ups.)
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
```

After presenting the report, ask: "Would you like me to fix any of these issues?"

If the user says yes, fix the issues, then update `wiki/revisions.md` and `wiki/log.md` with a lint entry.
