# Bootstrap a New Wiki

One-shot interactive setup. Interviews the user about their domain, tailors the schema and the four operational commands, seeds tracking files, and optionally kicks off the first source.

This command **self-deletes** after successful completion. Recovery is `git restore .claude/commands/bootstrap.md`.

## Process

1. **Pre-check.** Read `wiki/revisions.md` and `wiki/log.md`. If the revisions table has any rows beyond the table header (the `| Date | Action | Pages Touched | Summary |` row plus the `|---|---|---|---|` separator are the only header rows that ship empty), or if `wiki/log.md` has any entries beyond its title/intro/`---` header block, warn:

   > This wiki appears to already be bootstrapped. Re-running `/bootstrap` will overwrite `wiki/CLAUDE.md` and the DOMAIN-SLOT regions in `.claude/commands/{ingest,query,research,lint}.md`. Continue? (y/N)

   If not confirmed, stop. Treat the wiki as un-bootstrapped only when both files contain nothing beyond their shipped headers.

2. **Gather inputs.** There are two paths — pick whichever matches how the user wants to work.

   **Fast path — instructions file.** If a file named `boot_strap_instructions.md` (or `bootstrap_instructions.md`) exists at the repo root, read it, try to extract answers to all ten questions below, and jump directly to step 3 with a proposal synthesised from the file. If any question is unanswered in the file, ask only those specific questions as follow-ups rather than running the full interview. Announce:

   > Found `boot_strap_instructions.md` — synthesising from it instead of running the interview.

   **Interview path** — used when no instructions file exists, or when the user explicitly asks to "run the interview". Ask these questions one at a time. Wait for the user's answer before moving to the next. Acknowledge briefly between questions; don't lecture.

   1. **Domain.** "What is this wiki about? Give me a sentence or two describing the domain."
   2. **Goal.** "What do you want this wiki to do for you in 3–6 months? (answer queries you care about, compile a synthesis, serve as a reference for others, something else)"
   3. **Source types.** "What kinds of sources do you expect to feed it? (web articles, academic PDFs, books, YouTube talks, meeting notes, podcasts, other — multiselect)"
   4. **Authoritative source criteria.** "What counts as a trustworthy source in this domain? Examples: peer-reviewed papers, specific experts or blogs, official documentation, primary sources. What do you want to avoid?"
   5. **Expected conflicts.** "Are there known schools of thought or contested claims in this domain? This shapes how the `conflicts/` workflow is used."
   6. **Output forms.** "Beyond markdown pages, do you want `/query` to be able to produce other formats — comparison tables, charts, slide decks (Marp)? (optional, skip if unsure)"
   7. **User role and tone.** "Who's the reader? Just you, a team, the public? What voice should the LLM use — terse and expert, explanatory, casual?"

   The remaining three questions configure the wiki's **radar** — the watched-source set that `/weekly-brief` sweeps and `/lint` evolves. They are not optional: `/weekly-brief` halts on a wiki whose radar files are missing (see step 5).

   8. **Radar scope.** "For a weekly sweep of this domain, what's clearly *in* scope and what's clearly *out*? The out-list matters as much as the in-list — it's what stops the brief filling with adjacent noise."
   9. **Selection priority.** "When more looks interesting than fits in one brief (cap: 5 captures), what should win? Rank what matters — novelty, primary evidence, resolving an open question, reproducibility, popularity, recency."
   10. **Brief conventions.** "How do you want the weekly brief delivered — what day/time, which branch it commits to, email or not, and anything this domain needs that a generic brief wouldn't do?"

3. **Propose.** Summarise what you heard and present a proposed schema covering:
   - One-paragraph domain description.
   - Source-handling notes (which capture tool is expected for each source type).
   - Domain-specific lint checks (2–5 checks appropriate to the domain).
   - Tailored "authoritative sources" paragraph for `/research`.
   - Tailored takeaway prompts for `/ingest` (what to flag when reading a new source).
   - Answer tone/voice for `/query`.
   - The proposed **radar**: 10–40 concrete watched sources for this domain (feeds, journals, conferences, vendor press rooms, programme/funding pages, benchmark and code repos — whatever the domain's signal actually flows through), grouped by channel type, plus the in/out scope lists, the selection-priority ranking, and the brief conventions from questions 8–10.

   Where you are proposing sources from prior knowledge rather than a live sweep, **say so** and mark them `unverified` — the first `/weekly-brief` or `/lint` run confirms or retires them. Do not present a seeded list as a verified one.

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

5. **Seed the radar files.** `/weekly-brief` **halts** if `wiki/reference-sources.md` is missing or `wiki/watchlist.md` lacks a `setup_approved:` frontmatter field, and `/lint` steps 10 and 12 both read `reference-sources.md`. Nothing else in the kit creates them, so bootstrap must — a wiki without these files cannot run either of its automated operations.

   Create all four:

   - **`wiki/reference-sources.md`** — the radar. Required section headings, in this order:

     ```markdown
     # Reference sources

     <one line: what /weekly-brief scans for this wiki. Note "Setup-approved <YYYY-MM-DD> at bootstrap.">

     > **Seed provenance.** <state plainly whether the set came from a live sweep or from prior knowledge; if seeded, say the URLs are unverified until the first sweep confirms or retires them.>

     ## Status vocabulary
     <`active` / `probation` / `unverified` / `retired`, one line each>

     ## Scope (the brief's frame)
     **Focus on:** <bullets, from question 8>
     **Exclude:** <bullets, from question 8>

     ## <channel-type sections — one per kind of source, named for the domain>
     | Source | Why | URL | Status |
     |---|---|---|---|

     ## Selection priority (per bootstrap)
     <numbered ranking, from question 9>

     ## Local conventions for the brief
     <bullets, from question 10: what to omit rather than pad, tone rules, back-link
      convention, watchlist seeding policy, branch policy, delivery, frequency>

     ## Scheduling
     <the cron line this wiki would use, and whether it is installed yet>

     ## Related
     - [[watchlist]] — the persistent radar this file feeds
     - [[index]] — wiki-wide page catalog
     ```

     Channel-type sections are domain-shaped, not fixed — a hardware wiki wants journals/conferences/vendors/foundries/programmes; a markets wiki wants filings/data feeds/regulators. Pick headings that fit, and put the highest-signal aggregators first so a sweep that runs out of budget still hits them.

   - **`wiki/watchlist.md`** — the identified-but-not-captured ledger. Must open with frontmatter, or `/weekly-brief` halts:

     ```markdown
     ---
     setup_approved: YYYY-MM-DD
     seeded: false
     ---

     # Watchlist

     <purpose; format rule (`- <title> — <≤12-word why/status>`, no URLs); lifecycle rule
      (when an entry graduates to a full page, when it retires); note that sections are
      created on first use, with the expected section shapes for this domain.>

     ---

     ## Related
     - [[reference-sources]] — where the radar's inputs come from
     - [[index]] — wiki-wide page catalog
     ```

     **Ship it empty.** Do not pre-seed entries — the watchlist is populated by `/weekly-brief` overflow or by the user, and a pre-seeded one is indistinguishable from a stale one.

   - **`wiki/weekly-briefs/.gitkeep`** and **`wiki/lint-reports/.gitkeep`** — output directories for `/weekly-brief` and `/lint`.

   Then add both new pages to `wiki/index.md` under an `## Overview & meta` table (`[[reference-sources]]` and `[[watchlist]]` rows), and name them in the `revisions.md` row and `log.md` entry from step 4.

   **Do not install the cron entry.** Record the proposed schedule in the `## Scheduling` section and tell the user to run `/weekly-brief` manually once — confirming capture tooling and delivery work from this checkout — before scheduling an unattended run.

6. **Self-delete.** Run `rm .claude/commands/bootstrap.md` via the Bash tool. If an instructions file was consumed in step 2, also `rm boot_strap_instructions.md` (or `bootstrap_instructions.md`, whichever was present) — it's served its purpose and the proposal it spawned is now recorded in `wiki/log.md` and the command files. Then announce:

   > Bootstrap complete. Bootstrap command removed; `git restore .claude/commands/bootstrap.md` to recover if you want to re-run.

7. **Offer first source.** Ask:

   > Want to kick off your first source now?
   > - (r) `/research <topic>` — find and capture sources on the web
   > - (i) `/ingest <path>` — process a source you already have
   > - (s) skip — you can run these any time

   Slash commands cannot be invoked from inside another slash command. Suggest the next command to the user as plain text in chat for them to copy-paste and run themselves:

   - If `r`: ask for the topic, then say "Run `/research <topic>` to begin." (substitute the actual topic).
   - If `i`: ask for the path, then say "Run `/ingest <path>` to begin." (substitute the actual path).
   - If `s`: stop. Print: "You're set up. Run `/research` or `/ingest` whenever you're ready."
