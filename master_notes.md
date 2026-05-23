# Master Notes

Running log of what works and what doesn't — both for this specific wiki's operation and for the collaboration generally. Append-only scratchpad for observations that might deserve to become CLAUDE.md guidance, command updates, or kit-level improvements.

During normal operation, Claude appends observations here with `Status: open`. At `/harvest` time (or whenever you review), entries are triaged: some become kit-level code or doc changes promoted to main via `/harvest`; some become this wiki's project CLAUDE.md updates; some are rejected; some stay open for more signal.

## Format

Append entries using this structure:

```
### YYYY-MM-DD — short title
**Scope:** project | interaction | kit | both
**Observation:** what was noticed
**Implication:** what this suggests for CLAUDE.md, a command, a tool, or process
**Status:** open | proposed | applied | rejected
```

**Scope guide:**
- `project` — specific to this wiki (lands in this wiki's `wiki/CLAUDE.md` or DOMAIN-SLOT content).
- `kit` — generic to wiki-kit itself (gets promoted to main via `/harvest`; every other wiki benefits).
- `interaction` — about how the user and assistant work together (may become memory or user-level CLAUDE.md).
- `both` — overlaps more than one scope.

## Notes

<!-- Entries appended during operation go below. -->

### 2026-04-27 — `gh api` beats `capture_url` for GitHub-hosted markdown
**Scope:** kit
**Observation:** During the MemPalace research run, captured 6 repository markdown files (README, MISSION, ROADMAP, CLAUDE.md, two docs/) via `gh api repos/<owner>/<repo>/contents/<path>` + base64-decode + manual frontmatter, instead of running `capture_url` on the GitHub blob HTML. The `gh api` path is materially better for this source class: deterministic byte-for-byte content (no trafilatura HTML→markdown round-trip), unambiguous provenance (the API response includes commit SHA, path, and size), no playwright fallback needed for "JS-heavy" rendered code blocks, and no risk of the bot-wall heuristic mis-firing. For markdown sources hosted in public GitHub repos, this is the preferred capture method.
**Implication:** Add a `tools/capture_github.py` (or extend `capture_url` with a `--source github` switch) that takes `<owner>/<repo>/<path>@<ref>` and writes a numbered file with frontmatter including the commit SHA. Document in `.claude/commands/research.md` step 4 alongside the existing capture-tool table — *"Web page hosted on github.com (markdown file in a repo): use `gh api` or `tools/capture_github.py` rather than `capture_url`."* The research command currently lists capture_url as the default for "web page (HTML)"; this is suboptimal for GitHub-hosted markdown which is by far the most common source-tool we hit when ingesting from open-source projects.
**Status:** open

### 2026-04-27 — Source-authority concerns are upstream of auto-mode scope checkpoints
**Scope:** interaction
**Observation:** The auto-memory rule "Auto mode skips scope/emphasis checkpoints — execute recommended scope/emphasis/structure on /research ingests directly; don't ask" was applied during the MemPalace research run. But the run encountered a separate axis of decision-making the rule doesn't cover: when the candidate source's *authority* (not its scope) is contested or low — e.g., a 22-day-old GitHub project with a self-published benchmark, an in-README scam alert about impostor-malware domains, and credible third-party accusations of benchmark gaming. Auto mode handled this fine in practice (paused briefly to do an authority sniff-check via repo metadata + web search before the capture phase, then captured deliberately and labelled the resulting wiki page heavily with caveats), but the existing auto-memory rule doesn't anticipate this category. The good behaviour was a judgment call that a future agent without this run's memory might not make.
**Implication:** Either (a) extend the existing auto-mode memory entry to clarify that scope-skipping is about *what to write*, not *whether to trust the source* — source-authority concerns warrant a brief inline check and a labelled-output decision even in auto mode; or (b) add a complementary feedback memory along the lines of *"When a /research candidate is a self-published, viral, or recently-launched source making strong empirical claims, do an authority sniff-check (creation date, contributor density, third-party corroboration) before capture and lead the wiki page with a Source caveat block — but don't pause to ask the user; this is part of doing the research correctly."* The latter is more concrete; the former is more general. Probably both.
**Status:** open

### 2026-04-22 — /weekly-brief hardcodes wiki-ai-trends path in email template
**Scope:** kit
**Observation:** `.claude/commands/weekly-brief.md` step 6 renders a commit-reminder banner into the email with the literal path `/home/david/code/wiki-ai-trends` baked in. When a second wiki (e.g. `wiki-agentic-trends`) adopts `/weekly-brief`, the email tells the user to commit in the wrong directory unless the running agent remembers to substitute cwd.
**Implication:** Parameterize the template — the skill should derive the path from `pwd` (or a computed project-root) and the branch from `git rev-parse --abbrev-ref HEAD`, then render them into the banner. The skill's cron-install example is similarly wiki-specific; it should show a generic form.
**Status:** open

### 2026-04-22 — /weekly-brief brief-file path collides between wikis
**Scope:** kit
**Observation:** `.claude/commands/weekly-brief.md` step 6 instructs writing the brief to `/tmp/weekly-brief-<YYYY-MM-DD>.md`. That path isn't wiki-namespaced, so two wikis running on the same day (e.g. ai-trends at 07:00 Mon and agentic-trends at 07:30 Mon) will have the second clobber the first.
**Implication:** Namespace the brief filename per wiki — e.g. `/tmp/weekly-brief-<wiki-slug>-<YYYY-MM-DD>.md` where `<wiki-slug>` is derived from cwd's basename. Same fix should flow through to the `DRAFT_ID` recovery-path note in step 8.
**Status:** open

### 2026-04-26 — Anthropic engineering blog flagged for next research round
**Scope:** project
**Observation:** During the memory-management research run (round 4 on 2026-04-26), the Anthropic Memory Tool docs page (`docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool`) explicitly references https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents as "a detailed case study of this pattern in practice, including the initializer script, progress file structure, and git-based recovery." This is distinct from the also-referenced "Effective context engineering" blog. Not yet captured. Likely the highest-signal Anthropic-authored source on long-running agent harnesses we don't have.
**Implication:** Pull this URL in the next research run. Likely lands as either a peer to anthropic-memory-tool.md (concrete deployment patterns) or a new entry under deployments/ if the harness framing is broad enough.
**Status:** open

### 2026-04-26 — Anthropic memory_cookbook notebook captured as GitHub HTML, mostly base64
**Scope:** kit
**Observation:** During the same run I captured `https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/memory_cookbook.ipynb` via capture_url. The result was 207KB but only 164 markdown lines — almost entirely base64-encoded output cells from the notebook, with very little usable prose. Notebooks captured this way produce thin source material because the GitHub HTML view embeds image outputs as data URLs.
**Implication:** Two options for kit-level fix: (1) detect .ipynb URLs in capture_url and either fetch from raw.githubusercontent.com + parse the JSON to extract markdown cells only, or warn the user; (2) document this in research.md / capture_url docs as a known low-yield source. Option (1) is the better long-term fix — let me note this for /harvest.
**Status:** open

### 2026-04-25 — capture_pdf default-engine guidance lets pymupdf slip in
**Scope:** kit
**Observation:** During /research on long-horizon-context I picked `--engine pymupdf` for an AgentFold PDF capture and produced 2 broken image refs — repeating a mistake from 2026-04-22. The /research command doc reads "Default engine is `marker` (best for papers). For simple PDFs or to skip the model weight download, add `--engine pymupdf`." The "simple PDFs" carve-out and the "skip model download" hook are bait — they invite the agent to second-guess marker on speed/convenience grounds, exactly the reasoning the user has now corrected twice. The actual user-validated rule is: always marker (CPU fine), pymupdf is a last-resort for marker-fails-on-CPU only.
**Implication:** Two changes to wiki-kit:
1. `.claude/commands/research.md` — remove the `--engine pymupdf` carve-outs from the capture-step instructions; replace with: "Default to marker. If GPU is contended, force CPU with `CUDA_VISIBLE_DEVICES=\"\"`. Only use `--engine pymupdf` if marker fails on CPU too."
2. Consider a `tools/capture_pdf` CLI guard: print a `[warning]` line if `--engine pymupdf` is invoked without `--force`, naming the figure-extraction tradeoff. Defends against agents in future sessions making the same call against future user expectations.
**Status:** open

### 2026-04-22 — /weekly-brief Gmail draft is plaintext markdown, illegible in email clients
**Scope:** kit
**Observation:** `.claude/commands/weekly-brief.md` step 8 calls `mcp__claude_ai_Gmail__create_draft` with only the markdown body, so email clients render literal `#`, `**`, and `[[…]]` instead of formatted text. The brief is dense and hard to skim in that form.
**Implication:** The skill should produce both a plaintext alternative (current body) AND an HTML rendering (passed as `htmlBody` to `create_draft`). Add `markdown` (or `markdown-it-py`) to `pyproject.toml` and have step 8 render the brief markdown to HTML with a small inline stylesheet (similar to the one I used for the manual fix on 2026-04-22). Wikilinks `[[…]]` should render as monospace tokens (per the existing skill note that they're grep handles, not real links).

### 2026-05-04 — Background bash invocations don't inherit interactive PATH
**Scope:** kit
**Observation:** First weekly-brief capture-tool invocations from background `Bash run_in_background` returned `poetry: command not found`. The shell snapshot used by background bash doesn't pull `~/.local/bin` into `PATH` despite `which poetry` working in interactive shells. Resolved by invoking `/home/david/.local/bin/poetry` explicitly. Wasted ~3 minutes on duplicate captures.
**Implication:** Two complementary fixes worth promoting via `/harvest`:
1. `tools/capture_pdf.py` and `tools/capture_url.py` could detect when invoked outside a poetry env and either `exec` themselves under poetry or print a clearer error than the shell's `command not found`.
2. The `.claude/commands/weekly-brief.md` step 4 capture-script examples should use the resolved poetry path (or a `POETRY_BIN=$(command -v poetry || echo $HOME/.local/bin/poetry)` pattern) so future agents don't trip over the same PATH issue. Same fix applies to `.claude/commands/research.md` capture step.
**Status:** open

### 2026-05-04 — `tools.ingest_plan.aggregate` page-shape parser misses bold-wrapped directives
**Scope:** kit
**Observation:** All four subagent summaries this week wrote `**New page: <slug>** — <justification>` with the directive line wrapped in bold. The parser's `_PAGE_SHAPE_NEW_RE` regex matches `^-\s*New page:` literally and reports `kind="unknown"` for the bold-wrapped form. Same issue likely affects `_PAGE_SHAPE_EXTEND_RE`. Aggregate ran but only one of five page-plan entries was correctly parsed; recovered the other four manually from the raw summary "Proposed page shape" sections.
**Implication:** Two fixes:
1. Tighten the parser regex to tolerate optional `**`/`*`/`_` markdown emphasis around the directive prefix, e.g. `^-\s*\*?\*?(?:New page|extend)\s*:`. Backwards-compatible — current literal form still matches.
2. Update the subagent prompts in `.claude/commands/weekly-brief.md` step 5 (and `.claude/commands/ingest.md` if it has a similar block) to show the exact unwrapped directive shape, with a "**format strictly**" note. Either fix alone resolves the issue; both is belt-and-braces.
**Status:** applied 2026-05-16 — delivered fix 1 (regex emphasis tolerance + title cleanup + 11 tests) to main @ d3d9407 via /harvest.

### 2026-05-08 — capture_pdf abs-page URL requires weasyprint dep that's not installed
**Scope:** kit
**Observation:** `tools.capture_pdf --src https://arxiv.org/abs/2604.18071 --engine marker` failed with `Failed to convert /tmp/wk-pdf-ml24cdo5/source.pdf to PDF: No module named 'weasyprint'`. The tool fetches the abs-page HTML and tries to convert HTML→PDF with weasyprint before passing to marker; the weasyprint dep isn't in `pyproject.toml`. Recovered by switching to the direct PDF URL `https://arxiv.org/pdf/2604.18071`, which bypasses the HTML-to-PDF conversion entirely.
**Implication:** Two complementary fixes:
1. Either add `weasyprint` to `pyproject.toml` (so abs-page URLs Just Work), or strip the abs-page HTML conversion path and require callers to pass `/pdf/` URLs (simpler — fewer deps, fewer code paths).
2. If keeping the abs-page path: improve the error message to suggest the `/pdf/` URL. The current error doesn't hint that the workaround is one URL change away.
**Status:** open

### 2026-05-11 — /weekly-brief step-5 subagent prompt template lacks the `parse_summary` schema
**Scope:** kit
**Observation:** All five ingest subagents this week wrote summaries in the format I described to them (Source / Key claims / Notable specifics / Cross-references / Conflict flags / Proposed page shape / Open questions), but `tools.ingest_plan.parse_summary` rejected all five with "missing frontmatter" because it requires (a) `schema_version: 1` YAML frontmatter and (b) sections named exactly `One-line` / `Cross-ref candidates` / `Conflict flags` / `Proposed page shape`. My step-5 briefing template was wrong on both counts. Recovered by reading the summaries directly in the orchestrator (the content was all good), but the validation/aggregate path was bypassed and `run.json` was never persisted.
**Implication:** `.claude/commands/weekly-brief.md` step 5 should embed (or link to) the *exact* required schema — specifically the frontmatter shape and the exact section names that `parse_summary` enforces. Two complementary fixes:
1. Edit the step-5 template in the skill to show a literal example summary file (frontmatter + `## One-line` + `## Cross-ref candidates` + `## Conflict flags` + `## Proposed page shape`) rather than the loose Source/Key-claims/Notable-specifics shape I improvised.
2. (Optional, fallback) Make `parse_summary` more forgiving — accept the alternate section names as aliases — so subagent-format drift doesn't silently bypass the validation path. Either fix alone closes the gap; doing both is belt-and-braces.

The same gap likely exists in `.claude/commands/ingest.md` if `/ingest`'s subagent template is similarly loose; worth a parallel audit during /harvest.
**Status:** open

### 2026-05-08 — `poetry install --no-root` from background-bash stalls
**Scope:** kit
**Observation:** During the post-merge dep install for the markdown package, two parallel `poetry install --no-root` invocations from `Bash run_in_background` both stalled with no output for several minutes. Direct `pip install markdown` into the poetry venv at `~/.cache/pypoetry/virtualenvs/wiki-kit-*/bin/pip` worked instantly. Possibly poetry-lockfile contention from concurrent invocations, but the first invocation also stalled when run alone earlier in the session.
**Implication:** Worth double-checking before relying on `poetry install` in unattended cron paths. If the issue reproduces in cron, document a `pip install -r requirements.txt` (or pip-into-venv) fallback in the kit's setup steps. Single-occurrence — don't fix without reproducing.
**Status:** open

### 2026-05-15 — `cd` persists across Bash tool calls; breaks `poetry run python -m tools.*` snippets
**Scope:** kit
**Observation:** In this environment the working directory **persists** between Bash tool calls (contrary to the common "shell state does not persist" assumption). During the agentic-skills-personalities sweep, a `cd raw/research/<topic> && wc ...` command left cwd inside the topic dir; the next `poetry run python -m tools.audit_captures` then failed with `ModuleNotFoundError: No module named 'tools'` because it was no longer at repo root. A second command failed the same way.
**Implication:** The `research.md` / `ingest.md` pipeline snippets all assume repo-root cwd. Any `cd` (even a convenience `cd` for `wc`/`ls`) silently breaks every subsequent `poetry run python -m tools.*` invocation. Kit fix options: (a) prefix tool snippets with an explicit `cd <repo-root> && ...`, or (b) add a note to research.md/ingest.md to never `cd` and always use absolute/repo-relative paths from root. Cheap, generalises to every wiki.
**Status:** open

### 2026-05-15 — `/ingest` aggregator parses "Proposed page shape" too strictly (bold prefix → kind:"unknown")
**Scope:** kit
**Observation:** 5 of 7 subagent summaries had their `## Proposed page shape` parsed as `kind:"unknown"` by `tools.ingest_plan.aggregate`, because subagents wrote `- **New page** \`patterns/foo\`` (bold) instead of the exact `- New page: <title>` prefix the parser keys on. The orchestrator had to read the summary files directly to recover the real plan — same class of issue as the 2026-05-08 weekly-brief schema-mismatch learning. Page-plan aggregation silently degrades rather than erroring.
**Implication:** Either (a) make the subagent prompt template in `ingest.md` show the *exact* parseable prefixes (`- New page: ` / `- Extend [[page]] with section "..."`) with a "match this literally" instruction, or (b) make `parse`/`aggregate` tolerant of bold/`**`-wrapped and `:`-optional variants. (b) is more robust since subagents drift toward markdown emphasis. Recurring across at least two sweeps.
**Status:** applied 2026-05-16 — delivered option (b) (regex emphasis/colon tolerance + `_clean_title()` + 11 parametrized tests) to main @ d3d9407 via /harvest.

### 2026-05-18 — `/weekly-brief` step-7 path-scoped staging omits extended pages
**Scope:** kit
**Observation:** Step 7's `git add` list is `wiki/weekly-briefs/<date>.md wiki/index.md wiki/log.md wiki/revisions.md wiki/watchlist.md master_notes.md` plus `$PAGES_WRITTEN` (new pages only). This run extended 18 *existing* wiki pages (cross-refs, conflict-extension sections, data-point notes) that are neither in that fixed list nor in `pages_written` — so the documented staging command would silently leave every extension out of the weekly commit. Separately, three of the path-listed files (`index.md`/`log.md`/`revisions.md`) had pre-existing uncommitted edits at run start; because weekly-brief edits the same files, that backlog unavoidably co-mingles into the weekly commit despite the "pre-existing work not absorbed" guarantee — path-scoping protects untracked/other files but cannot isolate same-file hunks.
**Implication:** `.claude/commands/weekly-brief.md` step 7 should (a) stage all wiki pages modified during the run, not a fixed list — e.g. track an `$EXTENDED_PAGES` list alongside `$PAGES_WRITTEN` and add both, or stage `wiki/` minus an explicit pre-existing-dirty exclude set computed from `$PRE_EXISTING_DIRTY`; and (b) document that same-file pre-existing edits to the tracking files cannot be path-isolated and will co-mingle (the brief should flag this, which this run did). Recurred-risk: any sweep that extends existing pages (most of them) under-commits silently.
**Status:** open

### 2026-05-23 — Medium member-only articles capture as a ~1.4KB 404/paywall stub
**Scope:** kit
**Observation:** During /research (cc-memory-ecosystem), a Medium article URL (`medium.com/@umairsyedahmed282/...`) captured via `capture_url` (HTML + a `--js` retry) returned a 1,372-byte file whose `title:` frontmatter was literally `"404"` and whose body was Medium's "PAGE NOT FOUND / Out of nothing, something" chrome plus member-only article teasers — i.e. a login/paywall redirect, not the article. A *different* Medium article in the same run (`@tentenco/...`) captured fine at 12KB. So Medium is inconsistent: free posts work; member-only ("Member-only" badge) posts bot-wall and yield a sub-2KB 404 stub. The existing "<2KB ≈ failure" heuristic in research.md caught it on read, but `capture_url` exited 0 (no block-page signature matched — Medium's 404 is a normal-looking page).
**Implication:** Two kit options: (1) add Medium to the "Known bot-walled hosts" note in `research.md`/capture docs as *inconsistent — member-only posts return a 404/paywall stub*; (2) extend `capture_url`'s block-page detection to flag captures whose extracted `title` is exactly `"404"` or whose body matches Medium's "PAGE NOT FOUND" chrome, exiting non-zero. Low urgency — the thin-capture heuristic already catches it — but documenting Medium's inconsistency would save a wasted capture attempt.
**Status:** open

### 2026-05-23 — no cross-topic-dir duplicate-URL detection; same source re-captured into a new run
**Scope:** kit
**Observation:** This run captured HN item 47672792 into `raw/research/cc-memory-ecosystem/15-hn-47672792.md`, but the identical URL was already captured in a prior run at `raw/research/mempalace/10-hn-thread.md`. It was only caught because an ingest analyst subagent happened to recognise the item ID and flag it; `audit_captures` checks within-dir image collisions and thin extractions but not cross-dir URL duplication. On a long-running wiki, sources recur across topic dirs, wasting a capture + an ingest-subagent slot and risking double-counting the same claim as if independently corroborated.
**Implication:** Cheap kit win: have `capture_url`/`capture_pdf` (or `audit_captures`) check the new file's `url:` frontmatter against the `url:` of all existing `raw/research/**/*.md` and warn (not block) on a match — "already captured at <path>". Alternatively the /research command could pre-check candidate URLs against existing captures before presenting the shortlist. Would have surfaced the dup at capture time instead of mid-ingest.
**Status:** open
