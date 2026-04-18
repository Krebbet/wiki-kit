# Ingest a New Source

Process a raw source document and integrate its content into the wiki.

## Arguments

$ARGUMENTS — the file path to the source document (e.g., `raw/research/my-topic/01-article.md`). If it's a directory, process all markdown files within it.

## Process

1. **Read the source** — Read the file at the given path. If it's a directory, read all `.md` files within it.

2. **Discuss key takeaways** — Present a brief summary to the user:
   - Main ideas and claims
   - What is new or different from what the wiki already covers
   - Conflicts with existing wiki positions
   <!-- DOMAIN-SLOT: takeaway-prompts -->
   - (Domain-specific takeaway prompts go here — bootstrap fills this in. Examples: for history, flag dates and key actors; for science, flag methodology and data; for cooking, flag ingredients and technique names.)
   <!-- /DOMAIN-SLOT -->

3. **Wait for user input** — Let the user guide emphasis before writing. They may want to highlight specific aspects or skip others.

4. **Integrate into wiki** — Based on the discussion:
   - Create new wiki pages for genuinely new topics.
   - Update existing pages where the source adds depth, nuance, or corrections.
   - Add cross-references between new and existing content.
   - Follow page format: title, summary paragraph, `## Source`, `## Related`.

5. **Handle conflicts** — If the new source contradicts existing wiki positions:
   - Document the conflict clearly.
   - Present both positions to the user.
   - Wait for a ruling before changing existing wiki content.
   - Record resolution in `wiki/conflicts/`.

6. **Update tracking files:**
   - `wiki/index.md` — add/update entries for created or modified pages.
   - `wiki/revisions.md` — add a row recording the ingest.
   - `wiki/log.md` — append a dated ingest entry: `## [YYYY-MM-DD] ingest | Source Title`.

7. **Report** — List all pages created or updated, and any unresolved conflicts.
