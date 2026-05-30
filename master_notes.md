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

### 2026-04-19 — kickoff
**Scope:** interaction
**Observation:** User established the master_notes workflow itself: track project + interaction feedback, periodically promote learnings to project CLAUDE.md (changes OK, inform if significant) and master CLAUDE.md (never edit without consulting, but don't be shy about proposing).
**Implication:** This file is the substrate for that loop. Saved to memory so the workflow persists across sessions; consider proposing it for master CLAUDE.md once the pattern proves itself here.
**Status:** applied (memory saved, file created)

### 2026-04-19 — bootstrap interview shortcut worked well
**Scope:** project
**Observation:** User wrote bootstrap intent in `boot_stap_instructions.md` (typo: missing 'r') instead of answering the seven interview questions one at a time. I synthesized all seven answers from that file and presented a single proposal. User approved with "looks great. approved" — zero revision rounds needed.
**Implication:** `/bootstrap` could explicitly support an "instructions file" mode: if `boot_strap_instructions.md` (or some canonical name) exists in the repo root, skip the seven serial questions and synthesize from that file. Faster for users who prefer writing thoughts in one go vs. interactive Q&A.
**Status:** applied upstream — main's `90e7420 feat(bootstrap): accept boot_strap_instructions.md as fast-path input` ships this.

### 2026-04-19 — marker GPU assumption
**Scope:** project
**Observation:** First `/research` run crashed because marker tried CUDA on a saturated GPU. Recovered with `TORCH_DEVICE=cpu`, but 5–10× slower per paper. Logged in FEEDBACK.md.
**Implication:** capture_pdf.py needs either auto-fallback or a documented env var. The bootstrap source-type-notes slot for ArXiv should also acknowledge this. Project-level CLAUDE.md change candidate: add a "Capture environment" section noting the GPU caveat.
**Status:** partially addressed upstream — main's `11b2ecb fix(capture_pdf): one-line hint on CUDA OOM instead of stacktrace` covers the surface-level UX; auto-fallback and documentation still open.

### 2026-04-19 — reboot mid-research-run
**Scope:** interaction
**Observation:** User needed to reboot the machine while a long research run was in flight (1 background bash queue + 8 parallel research subagents on CPU). All in-flight processes will die. Wrote `STATE.md` capturing what's on disk, what's missing, and a concrete continuation plan; committed everything before reboot.
**Implication:** Long-running multi-agent workflows should leave a checkpoint file *as a matter of routine*, not just when a reboot is imminent. Anything that takes >30 min on CPU is worth a checkpoint snapshot every ~15 min so resume is trivial. Candidate convention: `STATE.md` at repo root, written by long-running orchestrator after each major phase.
**Status:** open — propose for project CLAUDE.md once we see how resume goes

### 2026-04-20 — fidelity audit should be a wiki-kit primitive
**Scope:** both (project + interaction)
**Observation:** Caught a 33% image-loss bug in capture_pdf only because the user explicitly asked me to "check that you are capturing the raw materials with fidelity." Without that prompt, synthesis would have proceeded against silently-corrupted captures. The fix to capture_pdf is in (`tools/capture_pdf.py` on `single-shot-training-wiki`), but the deeper issue is that the kit has no automated "did the capture actually work end-to-end?" check.
**Implication:** Two CLAUDE.md candidates:
1. **Project CLAUDE.md (this wiki):** add a "Post-capture verification" step to the wiki assistant's session protocol — after any `/research` or `/ingest`, run a fidelity check before declaring success.
2. **Master CLAUDE.md:** add a general principle — "When orchestrating data pipelines that produce large numbers of derived files, verify a sample for end-to-end correctness (not just exit code = 0) before downstream work." This applies far beyond wiki-kit.
Also: build `tools/audit_captures.py` and wire it into `/lint`. See FEEDBACK.md for the spec.
**Status:** tool + lint wiring applied upstream (`tools/audit_captures.py` and `/lint` / `/research` hooks are on main); Project and Master CLAUDE.md language still open.

### 2026-04-23 — capture tools are CWD-relative, silently producing nested directories
**Scope:** kit
**Observation:** A previous `cd raw/research/rlt-followups` that failed (exit 2: "No such file or directory") left my shell CWD unchanged to the caller's view but actually *changed* inside Bash tool invocations that use cd + && chains. Subsequent `mkdir -p raw/research/rl-optimizers` and the capture_pdf / capture_url commands resolved `--out raw/research/rl-optimizers` relative to the drifted CWD, so files landed at `raw/research/rlt-followups/raw/research/rl-optimizers/` — inside the previous topic's directory, not at the intended location. No error, no warning. I only noticed when sub-agents flagged the path discrepancy in their per-paper wiki pages.
**Implication:** Two kit-level asks:
1. `tools/capture_pdf.py`, `tools/capture_url.py`, `tools/fetch_transcript.py` should resolve `--out` relative to a repo-root anchor (e.g., walk up to the nearest directory containing `pyproject.toml` or `wiki/`), or at minimum print the absolute resolved output path on success so drift is visible.
2. `tools/audit_captures.py` could detect "nested raw-tree-within-raw-tree" layouts as a suspicious signal and flag it — a `raw/research/X/raw/research/Y/` path is almost always a bug.
Also useful: the assistant protocol could prefer `--out $(git rev-parse --show-toplevel)/raw/research/<slug>` when invoking capture tools, to be CWD-agnostic.
**Status:** open — kit-level fix needed; see `/harvest` for promotion.

### 2026-04-23 — /weekly-brief template hardcodes wiki-ai-trends as the target repo
**Scope:** kit
**Observation:** The `/weekly-brief` skill (`.claude/commands/weekly-brief.md`) was merged from main as part of the kit-level weekly-brief feature. It has 10 hardcoded references to `wiki-ai-trends` / `ai-trends-wiki` (the reference wiki the feature was developed for). Running the skill in any other wiki (e.g. `wiki-single-sample-learning`) produces an email whose commit-reminder banner tells the user to cd into the wrong repo. Also the cron-install stub, the "uncommitted on ai-trends-wiki" Telegram message, and the "render as relative GitHub links to the ai-trends-wiki branch" guidance are all wrong-by-default for other wikis.
**Implication:** Make the template dynamic. Three candidate fixes:
1. Template the hardcoded strings: in the skill body, replace `wiki-ai-trends` / `ai-trends-wiki` / `/home/david/code/wiki-ai-trends` with placeholder tokens like `<REPO_NAME>` / `<BRANCH_NAME>` / `<REPO_PATH>`, and add a skill-body step to resolve them via `git rev-parse --show-toplevel && git branch --show-current && basename $(git rev-parse --show-toplevel)` before composing the email.
2. Alternative: introduce a per-wiki `WEEKLY_BRIEF_CONFIG` block in `wiki/reference-sources.md` (or a dedicated `wiki/.weekly-brief.yaml`) that declares the target repo, branch, and email recipient. Skill reads it on startup.
3. Also: the first-time bootstrap should create `wiki/reference-sources.md` + `wiki/watchlist.md` + `wiki/weekly-briefs/` automatically if absent, rather than silently failing or writing into an empty structure. Today I created them by hand for wiki-single-sample-learning.
**Status:** open — kit-level fix needed; see `/harvest` for promotion.

### 2026-04-23 — /weekly-brief needs a first-run interview flow
**Scope:** kit
**Observation:** When I set up `/weekly-brief` for wiki-single-sample-learning today, I created `wiki/watchlist.md` and silently pre-populated it with 15 items I'd scraped from corpus-adjacent material during today's ingests (SDFT, SDPO, G-OPD, λ-GRPO, Goldilocks, DPO-vs-RLOO contradiction, etc.). The user's reaction: "for weekly briefing we should set up a dedicated watchlist and you should ask for details on exactly how the briefing should be formed. This should be done for each wiki separately." The seeded watchlist made first-run decisions the user wanted to make themselves. I was also heading into trend-scan without confirming scope, sources, or brief-shape preferences.
**Implication:** The current skill file jumps straight to "step 1: trend scan" and expects `wiki/reference-sources.md` + `wiki/watchlist.md` to already exist. It has no onboarding flow for a new wiki. Two candidate fixes:
1. Add a "step -1: first-run check" to the skill body: if `wiki/watchlist.md` is missing OR was auto-seeded OR the user hasn't approved the setup for this wiki, halt before any scan and run an interview: scope confirmation, signal sources, watchlist seeding policy (empty is the default), brief shape preferences, delivery channel, commit behaviour. Record an "approved setup" marker (e.g. a frontmatter field `setup_approved: 2026-04-23` in `watchlist.md`) so re-runs don't re-interview.
2. Extend `/bootstrap` to offer weekly-brief setup as an opt-in question during initial wiki creation; for wikis already bootstrapped, the user can re-run `/bootstrap --add weekly-brief` or similar. This keeps the setup colocated with the other wiki-initialization choices.
Also related: saved a feedback memory at `.claude/projects/.../memory/feedback_weekly_brief_setup.md` so I don't repeat the pre-seeding mistake across sessions.
**Status:** open — kit-level fix needed; see `/harvest` for promotion.

### 2026-04-23 — /harvest needs semantic vetting before promotion AND post-promotion verification
**Scope:** kit
**Observation:** The current `/harvest` flow classifies changes by **path** (kit paths → promote, wiki/raw → skip, DOMAIN-SLOT bodies → skip). But that filter is purely mechanical and doesn't answer the real question: "Does this change improve the core wiki-kit, or is it wiki-specific?" Example: today's edits to `.claude/commands/weekly-brief.md` (dynamic REPO_ROOT/BRANCH resolution, first-run guard) are clearly kit-generic and should promote. But the same file also gained a reference to `wiki/reference-sources.md`'s "Local conventions" section, which is a concept this specific wiki uses — if that convention isn't adopted by the kit as a first-class feature, the skill reference to it becomes dead weight for other wikis. The current path-based filter can't tell these apart.

Separately: after a harvest lands on main, **no step in the flow verifies the promoted changes actually apply to and improve other existing wikis** (wiki-ai-trends, wiki-agentic-trends, wiki-food-formulation, etc.). A change that's kit-clean on the origin branch could still conflict with another wiki's DOMAIN-SLOT, duplicate a local customisation, or silently fail to apply. Currently the assumption is "other wikis will rebase main and deal with it" — that's not reliable.

User requirements (raised 2026-04-23):
1. Harvest should only propagate to main if the change will **improve the core wiki-kit** as a whole. Wiki-specific stuff stays on the originating branch.
2. When a harvest is applied to (a) main and (b) each existing wiki, the change should be **vetted to make sure it applies AND improves** that destination.

**Implication:** Two process additions needed in `.claude/commands/harvest.md`:

1. **Semantic vet step (pre-promote).** After the path-based classification, for every hunk in the "promote" bucket, present it to the user with the question: "Does this generalise across all wikis, or is it specific to this branch?" If wiki-specific, move the hunk to a new `keep-local` bucket; record a note in `master_notes.md` describing why it's staying local so it can be reconsidered later if the pattern generalises. (Agent can pre-classify with low confidence and surface only the uncertain cases to reduce user burden.)

2. **Post-promote verification (per-wiki).** After a harvest push to main, iterate over other wikis under `~/code/wiki-*` and for each:
   - `git fetch && git merge origin/main --no-commit` (or rebase) in a worktree.
   - Run a quick self-check: does the wiki's `/lint` still pass? Do DOMAIN-SLOT markers in command files still align? Do any per-wiki configs (e.g. `reference-sources.md` "Local conventions", watchlist setup) still make sense relative to the new kit content?
   - Report per-wiki as "applies cleanly + improves" / "applies but adds noise" / "doesn't apply cleanly" / "applies but requires manual adjustment".
   - Do **not** auto-merge into other wiki branches — surface the assessment, let the user initiate the pull on each wiki when they next work on it. The verification is informational.

Candidate: new companion command `/harvest-verify` that encapsulates step 2, separate from the promotion step, since promoting and verifying happen at different times (post-push, async across wikis).

**Status:** open — process change to `/harvest`; also saving as a feedback memory since this is a strong user preference about kit hygiene.

---

## 2026-04-28 — capture_pdf silently degrades to abstract-page scrape when marker is unavailable

**Scope:** kit
**Status:** open

When `tools/capture_pdf.py --src <ARXIV_ABS_URL>` is run with `--engine` defaulting to marker, and weasyprint (a marker dependency) is missing from the poetry env, the script appears to fall back to pymupdf successfully — but if the abstract URL is what was passed (rather than the PDF URL), the result is a 7–8 KB scrape of the abstract page chrome rather than the paper body. The agent runs in this mode for ~5 minutes per paper, returns success, and reports clean audits. Only an external sanity check (file size or page count vs known paper length) catches it.

Observed during the concept-understanding-eval research run on 2026-04-28: 9 captures came back at ~7 KB each before being recaptured via direct `arxiv.org/pdf/<id>` URLs at 50–294 KB each.

**Candidate fixes (any one):**
1. `tools/capture_pdf.py` should auto-resolve `arxiv.org/abs/<id>` → `arxiv.org/pdf/<id>` when `--src` is an arXiv abstract URL.
2. Audit step should warn when a captured arXiv markdown is < 20 KB (probable abstract-only) even if no broken refs are found.
3. weasyprint should be either added to poetry deps or `tools/capture_pdf.py` should hard-fail (rather than silently fall back to pymupdf) when marker can't run, prompting the user to install it.

Promote one of these to the kit on next `/harvest`.

### 2026-04-30 — math wrapped in backticks instead of dollar-signs
**Scope:** kit
**Observation:** Across ~60 wiki pages (most synthesis pages, theme overviews, and per-paper pages), inline math like `F(x) = H/(M+ε)`, `M_θ`, `r^{SS}`, `θ ← θ - η·g`, `p_(1) − p_(2)` was wrapped in backticks. In Obsidian (the user's reading environment) backticks render as monospace code spans, so none of these typeset as math. The user reads in Obsidian and noticed it. CLAUDE.md voice guidance already states "LaTeX-style inline `$x$` and display blocks" but I (and presumably the ingest sub-agents that write per-paper pages) defaulted to backticks for anything that looked identifier-shaped.
**Implication:** The kit's `/ingest` and `/research` page-writing prompts need an explicit "wrap math in `$...$`, never backticks" rule. Likely lives in `tools/<wiki-kit>/templates/research-page.md` or the orchestrator prompt for the per-paper page sub-agent. Also worth adding a `/lint` check that flags backtick spans containing TeX-suspicious characters (^, _, Greek letters, math arrows) so this is caught at lint-time. The bulk fix on this wiki is being done now; promoting the rule + lint check to main would prevent regressions on every wiki built from the kit.
**Status:** open

### 2026-05-01 — page-writing sub-agents updated tracking files without coordination
**Scope:** kit
**Observation:** During the self-play research run, I dispatched four parallel sub-agents to write 11 wiki pages (the per-paper pages were the bounded unit-of-work). Three of the four sub-agents *also* updated `wiki/index.md`, `wiki/revisions.md`, and `wiki/log.md` because the prompts didn't explicitly forbid it. The result was partial / fragmented entries — three separate revisions rows for what is logically one ingest operation, an index theme summary that only mentioned 2 of the 11 pages, and a pages-by-theme table with 3 missing rows. I had to consolidate by hand afterward.

**Implication:** The kit's page-writing sub-agent prompt template (or the `/ingest` orchestrator's per-source dispatch prompt) should include an explicit "DO NOT update `index.md`, `revisions.md`, or `log.md` — those are the orchestrator's responsibility" line. Each sub-agent should write only its assigned per-paper page(s). The consolidation step then has authoritative, single-source-of-truth tracking updates. This generalises beyond `/research` → `/ingest` to any multi-page generative operation.

**Status:** open

### 2026-05-13 — capture_pdf pymupdf engine writes wrong-anchor image refs (audit-tripping but not content-affecting)

**Scope:** kit

**Observation:** `tools/capture_pdf.py --engine pymupdf` writes image refs in the resulting markdown using paths anchored at the **repo root** (e.g. `raw/research/decoding-time-steering/assets/02-cd-improves-reasoning/source.pdf-0-0.png`) rather than relative to the markdown file itself (which would be `assets/02-cd-improves-reasoning/source.pdf-0-0.png`). The image files themselves are captured correctly to disk under `assets/<slug>/`. `tools/audit_captures.py` resolves refs via `(md.parent / ref).resolve()` and correctly flags them as broken — the resulting paths nest the topic-dir twice (`raw/research/decoding-time-steering/raw/research/decoding-time-steering/...`).

Observed during the decoding-time-steering /research run on 2026-05-13: 86 "broken image refs" across all 13 captures, every single ref a wrong-anchor instance. Same issue recurred in the 2026-04-23 rl-optimizers run (revisions.md notes "20 broken figure refs across 5 PDFs"); appears endemic to the pymupdf engine path.

**Impact:** Rendering-only. Text content is intact; ingest reads text and doesn't need the figures. Obsidian and markdown viewers fail to inline the figures, which is a UX regression for raw-source review but doesn't affect wiki pages downstream.

**Candidate fixes (pick one):**
1. `tools/capture_pdf.py` should write image refs as `assets/<slug>/<image>` (relative to MD) rather than `raw/research/<topic>/assets/<slug>/<image>`.
2. `tools/audit_captures.py` should special-case the wrong-anchor pattern: if `(md.parent / ref).resolve()` fails *and* the same ref interpreted with a one-level-up anchor succeeds, classify as "wrong-anchor warning" not "broken ref" — keeps the audit-clean signal honest.
3. Both — fix #1 prevents regression; #2 reclassifies historical captures so /lint isn't perpetually noisy.

Promote on next `/harvest`.

**Status:** open

### 2026-05-15 — lint: weekly-brief pages systematically fail the research-page schema check

**Scope:** kit

**Observation:** /lint's research-page schema check (`## Method` + `## Claims` required under `wiki/research/`) flags 11 pages, and ~10 of them share one root cause: they were created by `/weekly-brief`, which uses a lighter page template than `/ingest` (it writes `## Results` / `## Empirical results` / `## Taxonomy` and folds method into the summary, rather than the `## Method` + `## Claims` schema `/ingest` enforces). Result: every weekly-brief sweep adds pages that the next lint flags as malformed, indefinitely. This is not 10 independent defects; it is one template mismatch between two kit commands writing into the same `wiki/research/` namespace.

**Candidate fixes (any one):**
1. `/weekly-brief`'s page-writing template adopt the same `## Method` + `## Claims` headings as `/ingest`'s research-page schema.
2. `/lint`'s schema check accept the weekly-brief heading set (`## Results` / `## Empirical results` / `## Taxonomy`) as schema-equivalent.
3. Mark weekly-brief-origin pages with frontmatter (e.g. `origin: weekly-brief`) and have lint apply a relaxed schema to them.
Fix #1 is cleanest (one schema across the kit). Promote on next `/harvest`.

**Status:** open

### 2026-05-15 — lint: bare `[[_overview]]` convention produces ~75 false broken-link flags

**Scope:** kit

**Observation:** The per-paper-page convention `[[_overview]]` (link to the same-folder theme overview) is used ~75× across the wiki. Obsidian resolves it by same-folder proximity, so it is *functional*, but any link-graph linter that resolves by exact path or unique-basename (there are 16+ `_overview.md` files) flags every instance as broken. This swamps the genuine broken-link signal (5 real vs ~75 convention false-positives in the 2026-05-15 run).

**Candidate fixes (any one):**
1. Kit lint heuristic: resolve a bare `[[_overview]]` (and any non-unique basename) to a same-directory file first, mirroring Obsidian's proximity resolution, before declaring broken.
2. Kit convention change: new pages use the explicit `[[../<theme>/_overview]]` form; add a lint autofix to rewrite bare forms.
Fix #1 is lower-churn and makes the linter match the actual rendering environment. Promote on next `/harvest`. (Relatedly, this run reinforces the priority of the 2026-05-13 candidate-fix #2 for `audit_captures` wrong-anchor handling — same class of "linter stricter than the rendering environment" noise, 377 false flags.)

**Status:** open

### 2026-05-16 — lint broken-link checker has THREE false-positive classes, not one

**Scope:** kit

**Observation:** Following up the 2026-05-15 bare-`[[_overview]]` entry: applying the 2026-05-15 lint fixes revealed that **4 of the 5 "genuine broken links" were false positives**, in three distinct classes the link-graph checker mishandles — all cases where the linter is stricter than Obsidian's actual resolution:
1. **In-page anchors** `[[#Conflicts]]` — normalised to empty target (`split('#')[0]` → `''`) and reported as `[[]]`. Obsidian resolves these to a same-file heading. (2 instances: binary-rewards-rl-challenges, rethinking-rl-sparse-selection.)
2. **Table-escaped alias pipes** `[[path\|Alias]]` inside a markdown table — the `\|` is the *documented Obsidian convention* for piping an aliased wikilink inside a table cell; the checker's regex truncates at `\`. (1 instance: fine-tuning-best-practices.md.)
3. **Bare non-unique basename** `[[_overview]]` — already filed 2026-05-15 (proximity resolution). (~75 instances.)
Only 1 of 5 was a real broken link (an aspirational page that didn't exist). Net: the broken-link report was ~95% false positives this run, which destroys the signal.

**Candidate fix:** the kit link-graph checker (and `/lint`'s mechanical step) must model Obsidian resolution before flagging: (a) treat `[[#anchor]]` as same-file, never empty; (b) strip a single leading `\` before `|` inside table rows; (c) resolve non-unique basenames by same-directory proximity. Until then, `/lint`'s "Broken Links" section should be read as "candidate links to manually triage", not "defects". Promote with the 2026-05-15 entries on next `/harvest`.

**Status:** open

### 2026-05-17 — weekly-brief trend-scan re-flags already-ingested papers as "new"

**Scope:** kit

**Observation:** The 2026-05-17 `/weekly-brief` trend-scan subagent surfaced SGS (arXiv:2604.20209) as a top candidate "trending into the window" and it was captured — but SGS already had a full wiki page (`research/self-play/sgs`, filed 2026-05-03 by the prior sweep). It was caught at the ingest-aggregation step (cross-refs revealed an existing page) and dropped, but only after wasting one of the hard-capped 5 capture slots and a capture+ingest subagent. Root cause: the trend-scan's dedup is a manually-maintained "already covered" list embedded in the dispatch prompt; it cannot know what prior weekly sweeps committed to `wiki/` because those commits happen *after* the run (no-commit policy) and the list isn't regenerated from wiki state.

**Candidate fix (any one):** before capture, the weekly-brief skill should cross-check each selected arXiv ID against existing wiki pages — grep `wiki/**/*.md` for the arXiv ID and against `wiki/index.md` titles — and auto-demote any hit to a "already on wiki" note rather than spending a capture slot. Cheap: one grep over the arXiv IDs in the candidate list at step 3, gated before step 4 captures. This also makes the hard cap of 5 meaningfully 5-*new*, not 5-minus-rediscoveries. Promote on next `/harvest`.

**Status:** open

### 2026-05-30 — capture_pdf arXiv abs-URL returns HTML not PDF (pymupdf engine)
**Scope:** kit
**Observation:** Using `arxiv.org/abs/<ID>` URLs with `--engine pymupdf` captures the abstract HTML page (200 lines of navigation + 3 PNG renders of the HTML), not the paper text. The correct URL for arXiv PDFs is `arxiv.org/pdf/<ID>`. The error is silent: no exception, audit's thin-captures check passes because the HTML renders to ~200 lines. Detected when inspecting capture text: "Skip to main content / We gratefully acknowledge support from the Simons Foundation..." Wasted 5 captures (immediately cleaned up and rerun with /pdf/ URLs; second run succeeded cleanly at 1150+ lines each).
**Implication:** weekly-brief and /ingest should always use `/pdf/` URLs for arXiv. Candidate fix: `capture_pdf.py`'s `_resolve_source` auto-rewrite `arxiv.org/abs/<ID>` → `arxiv.org/pdf/<ID>` before download. Safe since arXiv always serves a PDF at `/pdf/`.
**Status:** open
