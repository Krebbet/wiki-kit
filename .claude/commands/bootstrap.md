# Bootstrap a New Wiki

One-shot interactive setup. Interviews the user about their domain, tailors the schema and the four operational commands, seeds tracking files, and optionally kicks off the first source.

This command **self-deletes** after successful completion. Recovery is `git restore .claude/commands/bootstrap.md`.

## Process

1. **Pre-check.** Read `wiki/revisions.md` and `wiki/log.md`. If the revisions table has any rows beyond the table header (the `| Date | Action | Pages Touched | Summary |` row plus the `|---|---|---|---|` separator are the only header rows that ship empty), or if `wiki/log.md` has any entries beyond its title/intro/`---` header block, warn:

   > This wiki appears to already be bootstrapped. Re-running `/bootstrap` will overwrite `wiki/CLAUDE.md` and the DOMAIN-SLOT regions in `.claude/commands/{ingest,query,research,lint}.md`. Continue? (y/N)

   If not confirmed, stop. Treat the wiki as un-bootstrapped only when both files contain nothing beyond their shipped headers.

2. **Interview.** Ask these questions one at a time. Wait for the user's answer before moving to the next. Acknowledge briefly between questions; don't lecture.

   1. **Domain.** "What is this wiki about? Give me a sentence or two describing the domain."
   2. **Goal.** "What do you want this wiki to do for you in 3–6 months? (answer queries you care about, compile a synthesis, serve as a reference for others, something else)"
   3. **Source types.** "What kinds of sources do you expect to feed it? (web articles, academic PDFs, books, YouTube talks, meeting notes, podcasts, other — multiselect)"
   4. **Authoritative source criteria.** "What counts as a trustworthy source in this domain? Examples: peer-reviewed papers, specific experts or blogs, official documentation, primary sources. What do you want to avoid?"
   5. **Expected conflicts.** "Are there known schools of thought or contested claims in this domain? This shapes how the `conflicts/` workflow is used."
   6. **Output forms.** "Beyond markdown pages, do you want `/query` to be able to produce other formats — comparison tables, charts, slide decks (Marp)? (optional, skip if unsure)"
   7. **User role and tone.** "Who's the reader? Just you, a team, the public? What voice should the LLM use — terse and expert, explanatory, casual?"

3. **Propose.** Summarise what you heard and present a proposed schema covering:
   - One-paragraph domain description.
   - Source-handling notes (which capture tool is expected for each source type).
   - Domain-specific lint checks (2–5 checks appropriate to the domain).
   - Tailored "authoritative sources" paragraph for `/research`.
   - Tailored takeaway prompts for `/ingest` (what to flag when reading a new source).
   - Answer tone/voice for `/query`.

   Ask for approval. Support a revision loop — if the user wants changes, revise and re-present until they approve.

4. **Write files.** Once approved:

   - **`wiki/CLAUDE.md`**: replace `{{domain}}`, `{{goal}}`, `{{source_types}}`, `{{audience}}`, `{{tone}}` with the approved content. Use exact string replacement (the Edit tool, not regex).

   - **`.claude/commands/research.md`**: replace contents between `<!-- DOMAIN-SLOT: authoritative-sources -->` and `<!-- /DOMAIN-SLOT -->` with the tailored authoritative-sources paragraph. Replace contents between `<!-- DOMAIN-SLOT: source-type-notes -->` and `<!-- /DOMAIN-SLOT -->` with the tailored source-handling notes. Keep the slot markers themselves intact.

   - **`.claude/commands/ingest.md`**: replace contents of the `<!-- DOMAIN-SLOT: takeaway-prompts -->` region with the tailored takeaway prompts.

   - **`.claude/commands/lint.md`**: replace contents of the `<!-- DOMAIN-SLOT: domain-lint-checks -->` region with the tailored domain checks.

   - **`.claude/commands/query.md`**: replace contents of the `<!-- DOMAIN-SLOT: answer-tone -->` region with the tailored tone/voice guidance.

   **Slot replacement convention:** preserve the `<!-- DOMAIN-SLOT: name -->` and `<!-- /DOMAIN-SLOT -->` lines exactly. Replace **only** the content between them. The marker lines themselves must remain untouched so users can re-run bootstrap later or hand-edit the slots.

   Concrete example. Before:

   ```markdown
   <!-- DOMAIN-SLOT: answer-tone -->
   (Default tone guidance, replaced at bootstrap.)
   <!-- /DOMAIN-SLOT -->
   ```

   After (correct):

   ```markdown
   <!-- DOMAIN-SLOT: answer-tone -->
   Terse and expert. Assume the reader knows the field; skip background.
   Cite every claim with `[[wiki-link]]`.
   <!-- /DOMAIN-SLOT -->
   ```

   After (WRONG — markers were rewritten):

   ```markdown
   Terse and expert. Assume the reader knows the field; skip background.
   ```

   The `old_string` you pass to Edit should include the opening marker, the existing content, and the closing marker; the `new_string` should include the same opening marker, the new content, and the same closing marker.

   - **`wiki/index.md`**: under the title, insert a one-line domain description. Leave the table headers intact.

   - **`wiki/revisions.md`**: add a row to the table: `| YYYY-MM-DD | bootstrap | CLAUDE.md, commands | Initial bootstrap: <domain> |`.

   - **`wiki/log.md`**: append:

     ```
     ## [YYYY-MM-DD] bootstrap | <domain>

     Initial bootstrap. Schema and commands tailored for <domain>. Ready to receive first source.
     ```

   **Date placeholder.** `YYYY-MM-DD` above is a literal placeholder — substitute today's actual date (the date this command runs) when writing the row and the log entry.

5. **Self-delete.** Run `rm .claude/commands/bootstrap.md` via the Bash tool. Then announce:

   > Bootstrap complete. Bootstrap command removed; `git restore .claude/commands/bootstrap.md` to recover if you want to re-run.

6. **Offer first source.** Ask:

   > Want to kick off your first source now?
   > - (r) `/research <topic>` — find and capture sources on the web
   > - (i) `/ingest <path>` — process a source you already have
   > - (s) skip — you can run these any time

   Slash commands cannot be invoked from inside another slash command. Suggest the next command to the user as plain text in chat for them to copy-paste and run themselves:

   - If `r`: ask for the topic, then say "Run `/research <topic>` to begin." (substitute the actual topic).
   - If `i`: ask for the path, then say "Run `/ingest <path>` to begin." (substitute the actual path).
   - If `s`: stop. Print: "You're set up. Run `/research` or `/ingest` whenever you're ready."
