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
11. **Domain-specific checks** — neuromorphic materials, SNNs, and the industry around them:
    a. **Numbers carry their boundary** — every quantitative claim (energy/op, endurance, retention, variability, accuracy, throughput) states units *and* measurement conditions *and* the boundary (device / array / chip / system; inference / training). Flag any bare "N× more efficient" or "N pJ per synaptic operation" with no boundary named.
    b. **Evidenced vs claimed vs synthesis** — every page marks which of its statements are measured results, which are vendor/author claims, and which are the wiki's own synthesis. Flag pages that blur the three, and any forward-looking date not attached to a named owner.
    c. **Maturity stated** — every device-, material-, or chip-page names where it sits on the ladder (single device → array → integrated chip → foundry tape-out → sampling → in-product), with node and fab where known. Flag pages that describe a technology without saying how real it is.
    d. **Player-roster freshness** — entries in the players/roster pages carry a `last-verified` date. Flag any player entry, funding figure, or roadmap date older than 6 months without re-verification, and any company whose status may have changed (acquisition, shutdown, pivot).
    e. **Timeline claims traceable** — every commercial-viability date in the wiki traces to a specific source with an owner, and names the blocker it is gated on. Flag orphan dates.
    f. **Conflicts primary-sourced and current** — pages in `wiki/conflicts/` state the contested claim precisely, cite at least one primary source per side, and name the measurement or assumption that separates the positions. Flag conflicts that new evidence has since settled.
    g. **Device-family cross-linking** — each device-family page (RRAM, PCM, FeFET, MRAM, ECRAM, photonic, Mott/VO2, 2D) links to at least one sibling family and to the comparison table page. Flag orphan device pages.
    h. **Jargon defined on first use** — materials/device-physics terms (BEOL, ECRAM, 1T1R, forming voltage, conductance linearity, sneak path, on/off ratio) are briefly defined the first time each page uses them. ML terms need no definition.

12. **Trend radar sweep** — read `wiki/reference-sources.md`. For each source with status `active` or `probation`: (a) fetch recent activity appropriate to the channel type (paper feed, vendor press room, trade-press section, conference programme, GitHub releases, funding tracker); (b) filter to on-topic per the `## Scope` section of that file; (c) rank by the `## Selection priority` list; (d) propose findings to the user under a **Trend Radar** output section — **never capture without approval**; (e) evolve the radar (Add / Demote / Retire / Promote) under a **Radar Evolution** section, and ask before mutating `reference-sources.md`.
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
