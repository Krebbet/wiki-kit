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

10. **Watched-source evolution (radar)** — the watch list tracks the wiki's evolving subject, not a frozen bootstrap snapshot. Review the sources cited by pages added or changed since the last lint report (`wiki/lint-reports/`), plus any high-signal venues encountered while reading the wiki this run. Identify sources the wiki should watch going forward that aren't yet pinned in `wiki/reference-sources.md`. Append confirmed new sources to the appropriate watched-source section of `wiki/reference-sources.md` (with a one-line relevance note), and drop any that have gone stale. Record the current watched-source set in the **Trend Radar** output section and the additions/removals made this run in the **Radar Evolution** section.

<!-- DOMAIN-SLOT: domain-lint-checks -->
11. **Framework operationalisation** — wherever a page proposes a dimension or axis of institutional variation, it must state how you would *measure* that axis on a real institution. A dimension you cannot operationalise is an essay, not a framework. Flag any that lack it. Scope this check by **content, not by path**: apply it to any page proposing an axis, wherever it is filed. `[[dimensions-of-institutional-variation]]` is the canonical register and the primary target, but a dimension proposed in passing on a topic page is equally in scope. A row explicitly marked `rejected` with its reason and a readmission condition recorded is compliant — the point is that unmeasurable axes stay visible, not that they be deleted.
12. **Evidence tier labelling** — flag any page where empirical findings, theoretical models, and the wiki's own synthesis are not distinguishable. Every substantive claim should be attributable to one of the three.
13. **Case/theory linkage** — flag framework, mechanism and theory pages that link to no case-study or institution-profile page, and case-study pages not linked from at least one framework or mechanism page. The framework is only worth something if it is doing work on real institutions. Scope by **content, not by path**. Until the wiki has any case-study pages at all, report this check as `not yet applicable` with the count of framework pages waiting on cases — a standing reminder that the theory is currently ungrounded, not a clean pass.
14. **Case-study tagging** — every institution profile must state, in its opening paragraph, its sector (public / private / hybrid / civil-society), rough scale (headcount and budget order-of-magnitude), age, and country. Cross-cutting comparison is impossible without these. Flag missing tags.
15. **Scope-condition creep** — flag pages that state a general law about institutions while citing evidence drawn from a single country, sector, or era. Either the scope condition is stated on the page or the claim is overreaching.
16. **Ideological balance** — flag pages on contested questions that cite only one camp. List the missing perspective(s) explicitly rather than just noting imbalance.
17. **Thesis drift** — flag any page that treats the user's collapse-and-renewal book thesis, or the power/institutions/economy triad, as an established finding rather than as the working hypothesis it is. This wiki is evidence-led; the thesis is on trial, not on the bench.
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

### Trend Radar
- ...

### Radar Evolution
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
