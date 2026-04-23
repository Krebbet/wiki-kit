# Weekly Brief

Self-directed weekly research sweep: scan watched sources for what's *trending* in AI/ML, pick the most significant new papers, capture + ingest them into the wiki autonomously, then email a concise brief to the user.

This command runs **locally** on a weekly cron (see **Local scheduling** below) and runs **unattended** — no human gate. The brief is the audit trail. Output lands *uncommitted* on whatever branch the run was invoked from (resolved at runtime — see step 0); the user commits manually on their next login (the email contains the reminder).

## Arguments

$ARGUMENTS — optional override for the trend-scan window (e.g. `--since 14d`). Default window is 7 days.

## Critical rules

- **Autonomy.** No human gate. Every decision the orchestrator would normally surface (page plan, conflict rulings, prune list) is made by the agent using the heuristics below.
- **Cap on captures.** Hard limit: **5 papers per run**. If more look interesting, the surplus goes straight to `wiki/watchlist.md`. The brief is a brief.
- **Inherit `/research` and `/ingest` rules.** Don't re-summarize source bodies in the main agent. Subagent-per-source. Capture scripts are the default. No `WebFetch` for source content.
- **Don't commit.** Leave all `wiki/` and `raw/research/weekly-<DATE>/` changes uncommitted on the current branch — the user commits when they next log on. The email body must include a prominent commit reminder (see step 8). If the working tree had pre-existing uncommitted changes when the run started, flag that in the email rather than absorbing them into the weekly diff.

## Process

### 0. Resolve runtime values

Before any other step, resolve the target repo/branch so the email, Telegram, and commit-reminder can reference the right place regardless of which wiki invoked the command:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
BRANCH=$(git branch --show-current)
RUN_DATE=$(date -I)   # YYYY-MM-DD, used throughout as <YYYY-MM-DD>
```

If `git rev-parse` fails (not inside a git repo), abort with a short error — this command only makes sense inside a wiki checkout.

Also at step-start, capture the pre-existing working-tree state so step 7 can separate weekly-brief's diff from prior work-in-progress:

```bash
PRE_EXISTING_DIRTY=$(git status --porcelain | head -c 2000)   # truncate defensively
```

All downstream steps refer to `$REPO_ROOT`, `$REPO_NAME`, `$BRANCH`, `$RUN_DATE`, `$PRE_EXISTING_DIRTY` — do not re-hardcode.

**Read `wiki/reference-sources.md` fully before step 1.** It holds per-wiki customisations — specifically, any `## Scope`, `## Selection priority`, and `## Local conventions` sections override the defaults in this skill. If the file is missing, or if `wiki/watchlist.md` lacks a `setup_approved:` frontmatter field, **halt** — the wiki hasn't completed setup. Surface the missing setup to the user (or log and exit if unattended); do not guess.

### 1. Trend scan

Survey the watchlist defined in `wiki/reference-sources.md`. Don't crawl every source — pick a *small* set of high-signal aggregators and check them for what's currently popular, gaining popularity, or of particular technical interest.

Suggested signal hierarchy (cheapest to most expensive):
- **alphaXiv weekly trending** (or its API) — explicit popularity ranking on arXiv.
- **r/MachineLearning hot + r/LocalLLaMA hot** for the past week — aggregator for community attention.
- **AK's X timeline** (`@_akhaliq`) and **Aran Komatsuzaki** for what frontier-aware curators are surfacing.
- **paperswithcode trending / leaderboard climbs** for benchmark-grounded movement.
- **Recent commits / star spikes on tracked awesome-lists** as a discovery proxy.
- **Latent Space + Dwarkesh + Cognitive Revolution episode notes** for the past 2 weeks if a recent episode flags a specific paper.

For each candidate paper that surfaces ≥2 times across these signals, record: `(title, arXiv-or-blog-URL, signal sources, 1-line why-trending)`.

**Use `WebSearch` only to find candidate URLs.** Do not paraphrase the search snippets into the brief.

### 2. Trend synthesis (3-6 bullets)

Look across all the candidates and write **3-6 short bullets describing the trend pattern this week** — e.g., "RL-vs-ES post-training debate heated up: 3 new ES-side papers", "diffusion-LLM hybrid drafting gaining traction (TiDAR follow-ons)", "test-time-training survey activity rising".

These bullets become the top of the email. They are *editorial* — mark inline as `(synthesis)` if any go beyond what individual papers say.

### 3. Selection (≤5 captures + ≤10 watchlist additions)

From the candidate list, pick **at most 5** to actually capture and ingest. Selection heuristic, in order:
1. **Multiple independent signals** (alphaXiv top + AK + Reddit hot beats single-source mention).
2. **Technical novelty over volume** — a single new mechanism > five reframings of an existing one.
3. **Wiki-fit** — domain match (LLM/SLM training, fine-tuning, RL, novel architectures, CV, evolutionary). Skip purely application or product news.
4. **Conflict load-bearing** — if a candidate would resolve an open `wiki/conflicts/*.md` (Position B for an existing Position A), prioritize it.
5. **Reproducibility positive** — code released > code promised > closed.

Everything else interesting goes to `wiki/watchlist.md` as a 1-2 sentence entry per item (cap 10 per run; surplus is discarded for this week).

### 4. Capture (inline `/research` step 4)

For each of the (≤5) selected papers:
- arXiv → `poetry run python -m tools.capture_pdf --src <URL> --out raw/research/weekly-<YYYY-MM-DD> --slug <slug> --engine marker` (or `--engine pymupdf` if marker is unavailable locally; fall back gracefully).
- Blog/README → `poetry run python -m tools.capture_url --url <URL> --out raw/research/weekly-<YYYY-MM-DD> --slug <slug>`.
- YouTube → `poetry run python -m tools.fetch_transcript --url <URL> --out raw/research/weekly-<YYYY-MM-DD> --slug <slug>`.

After captures, run the audit:
```bash
poetry run python -m tools.audit_captures raw/research/weekly-<YYYY-MM-DD>
```
If anything is broken (missing image refs, thin extractions), drop that paper from the run, note it in the brief as `skipped: <slug> (capture failed)`.

### 5. Ingest (inline `/ingest` step, autonomous variant)

Follow `/ingest`'s subagent-per-source flow exactly *except* the human gate:

- Compute dispatch list via `tools.ingest_plan.compute_dispatch_list`.
- Dispatch one `general-purpose` Agent per source in parallel (single message, multiple Agent calls).
- Wait for all; validate each summary via `tools.ingest_plan.parse_summary(Path(...))`; persist `run.json` with `status: ok|failed`.
- Aggregate via `tools.ingest_plan.aggregate(...)`.
- **Skip the human gate.** Apply this autonomous page-plan policy:
  - One paper page per source: `wiki/<slug>.md` (slug derived from arXiv or paper short-name; not the capture filename's NN-prefix).
  - If 2+ sources cluster around a shared concept page that *already exists* in `wiki/` (e.g. [[test-time-training]]), extend that cluster page's "Members" / comparison table rather than creating a new cluster page.
  - If 2+ sources propose the *same* new cluster page, create it once and link from both paper pages — but only if the cluster page would be load-bearing (≥2 source contributions). Otherwise skip and add a "see also" link between the paper pages directly.
  - Conflict files: if any summary's `## Conflict flags` cites a contradiction with an existing `wiki/<page>.md`, write it to `wiki/conflicts/<short-name>.md` using the same template as existing conflict files (Position A from new source, Position B from the existing wiki claim, resolution rule).
  - Forward-looking conflicts (no current wiki contradiction) get added to the *existing* relevant `wiki/conflicts/<slug>.md` if one is already open on the same theme; otherwise discarded for this run (don't open speculative conflict files weekly — that's noise).
- Write each page; persist `pages_written` in `run.json` after each write.
- Update `wiki/index.md`, `wiki/log.md`, `wiki/revisions.md` as the existing `/ingest` does.
- Update `wiki/watchlist.md` with the (≤10) overflow entries from step 3.

### 6. Compose the brief (fixed shape)

The brief is **watchlist-centric**, not captures-centric. The user's view of this-week's world is: the wiki's radar (the watchlist), with industry-wide trends framing it. This-week's captures are an implementation detail shown in run notes, not a headline section.

**Two outputs.** Every run produces both:
- `wiki/weekly-briefs/<YYYY-MM-DD>.md` — the markdown, committed as part of the wiki (uncommitted per the no-commit policy; user commits on next login).
- `/tmp/weekly-brief-<YYYY-MM-DD>.html` — the email-legible HTML render of the same markdown, generated in step 8 by `tools/render_brief_html.py`.

The skill also still writes `/tmp/weekly-brief-<YYYY-MM-DD>.md` (same content as the wiki copy) so the existing audit-trail path on disk is preserved.

Write to `/tmp/weekly-brief-<YYYY-MM-DD>.md` AND `wiki/weekly-briefs/<YYYY-MM-DD>.md` with **exactly** this shape:

```markdown
Subject: Weekly AI radar (<REPO_NAME>) — week of <YYYY-MM-DD>

⚠ **Uncommitted changes on `<BRANCH>`.** On your next login, run:
`cd <REPO_ROOT> && git add wiki/ raw/research/weekly-<YYYY-MM-DD>/ && git commit -m "weekly: <YYYY-MM-DD> radar sweep"`

# Trends in the industry
- <bullet 1 — a trend visible across the full watchlist + web scan, not just this week's additions. State the method/pattern, who's driving it, and what it's displacing or building on>
- <bullet 2>
- <bullet 3>
- <bullet 4-7 as warranted>

# Top 3 from the watchlist
Pick either *new-and-interesting* (recent watchlist addition with novel mechanism) OR *old-and-now-trending* (foundational entry everyone is building on this quarter). Mix is fine. Format: **Title** — one line. No more.

1. **<title>** — <1-line summary>. *(new | old-now-trending, <arXiv or year>)*
2. **<title>** — <1-line summary>. *(new | old-now-trending, <arXiv or year>)*
3. **<title>** — <1-line summary>. *(new | old-now-trending, <arXiv or year>)*

# Other watchlist references
Remaining watchlist items worth keeping in scope. Group by the watchlist's section headers. Format per item: `- <title> — <≤8-word tag>`. No URLs, no multi-sentence descriptions — this is a scannable ledger, not a summary.

## <Section name>
- <title> — <tag>
- ...

(repeat per section that has entries worth carrying)

# Conflicts opened or extended this week
- [[conflicts/<slug>]] — <one sentence on the position>
- (omit section if none)

# Run notes
- Sources scanned: <count>
- Captures attempted / succeeded: <a> / <b> (detail: <slug list>)
- Wiki pages written: <count>
- Watchlist additions this run: <N>
- Uncommitted changes (awaiting your commit): <N> files — <short `git status --porcelain` summary or "none">
- Pre-existing uncommitted changes at run start: <none | brief list>

— Weekly brief generated by /weekly-brief on <ISO timestamp>
```

The wiki-link `[[...]]` notation will not render in plain-text email; that's intentional — they're pointers for the user to grep against in their checkout. If sending HTML, render them as relative GitHub links to the `<BRANCH>` branch (resolved at runtime).

**Trends vs top-3 vs references — why the split matters.** The trends section is editorial synthesis across the whole watchlist; it's the one place the brief is allowed to generalize. The top 3 are the concrete "if you only read about three things this week, these" picks. The references list is the ledger — it exists so the user can scan what's in-scope without opening the watchlist file. Don't merge or reorder these; the shape is the signal.

### 7. Do not commit

Intentionally do **not** `git add`, `git commit`, or `git push`. Leave changes to `wiki/` and `raw/research/weekly-<YYYY-MM-DD>/` uncommitted on the current branch (`$BRANCH`).

Before exiting step 7, run `git status --porcelain` and record the output to include in the email under `# Run notes → Uncommitted changes`. If there were pre-existing uncommitted changes at step-start (captured in step 0 state), note them separately so the user can tell weekly-brief's diff apart from any prior work-in-progress.

### 8. Send email

The user reads mail in Outlook, so the brief must actually *send* to `david.hugh.mcnamee@outlook.com` — not sit as a draft in Gmail. Primary path is SMTP via `tools/send_email.py` (Gmail SMTP + app password). Fallback is the Gmail MCP `create_draft` if the SMTP env isn't configured.

- The email body **must** include the bolded commit-reminder banner at the top (see step 6 template).
- **Credentials.** `GMAIL_USER` (should be `krebbet@gmail.com`) and `GMAIL_APP_PASSWORD` (16-char Google app password, generated in the user's Google Account → Security → App passwords) live in `/home/david/code/remote_workstation/.env` alongside the Telegram token. The skill sources that file, so no separate config is needed.
- **Before sending: render HTML.** Convert the markdown to a legible email body. This is required, not optional — sending raw markdown produces the unreadable format the user originally pushed back on.
  ```bash
  poetry run python -m tools.render_brief_html \
    --in /tmp/weekly-brief-$RUN_DATE.md \
    --out /tmp/weekly-brief-$RUN_DATE.html \
    --title "Weekly AI radar ($REPO_NAME) — week of $RUN_DATE"
  ```
- **Primary: SMTP send (both bodies).** Plain-text markdown is the fallback alternative; HTML is what Outlook renders.
  ```bash
  set -a; source /home/david/code/remote_workstation/.env; set +a
  if [ -n "${GMAIL_APP_PASSWORD:-}" ]; then
    MESSAGE_ID=$(cd "$REPO_ROOT" && poetry run python -m tools.send_email \
      --to david.hugh.mcnamee@outlook.com \
      --subject "Weekly AI radar ($REPO_NAME) — week of $RUN_DATE" \
      --body-file /tmp/weekly-brief-$RUN_DATE.md \
      --html-body-file /tmp/weekly-brief-$RUN_DATE.html)
    DELIVERY_KIND="sent"
    DELIVERY_ID="${MESSAGE_ID}"
  else
    # Fallback — no SMTP creds on this machine.
    # Call mcp__claude_ai_Gmail__create_draft with BOTH `body` (markdown) and `htmlBody` (HTML);
    # capture the returned id.
    DELIVERY_KIND="draft"
    DELIVERY_ID="<draft-id from create_draft>"
  fi
  ```
- Capture `DELIVERY_KIND` (`sent` | `draft` | `failed`) and `DELIVERY_ID` (Message-ID or draft id or `"(mcp unavailable)"`); these feed step 8b.
- If SMTP send fails (exit 3), fall back to `create_draft` within the same run so the brief is at least recoverable. If both fail, log prominently (the brief file at `/tmp/weekly-brief-<YYYY-MM-DD>.md` is still on disk for manual recovery), set `DELIVERY_KIND="failed"`, and exit non-zero *after* the Telegram ping.

### 8b. Telegram notification

Fire a short notification via the user's existing Telegram bot (plumbing lives in `/home/david/code/remote_workstation` — `dispatcher/telegram.py` + `.env`). This is the "you got a brief" signal, so the user doesn't have to check Gmail to know the run finished.

```bash
set -a; source /home/david/code/remote_workstation/.env; set +a
CHAT_ID="${TELEGRAM_ALLOWED_CHAT_IDS%%,*}"   # first allowed chat
# DELIVERY_KIND is "sent" (Outlook got it) or "draft" (needs manual send from Gmail).
TEXT="📡 Weekly brief ${REPO_NAME} ${RUN_DATE} — ${N_CAPTURED} captured, ${N_WATCHLIST} watchlisted. Email ${DELIVERY_KIND}: ${DELIVERY_ID}. Uncommitted on ${BRANCH}."
curl -sS --max-time 10 "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${TEXT}" >/dev/null || echo "telegram ping failed (non-fatal)"
```

Keep the message terse — it's a notification, not a duplicate brief. Always include:
- run date
- `N_CAPTURED` / `N_WATCHLIST` counts
- `DELIVERY_KIND` + `DELIVERY_ID` (so the user knows whether Outlook has it or whether they need to hit send in Gmail)
- a reminder that the diff is uncommitted

If `TELEGRAM_BOT_TOKEN` isn't set (e.g. `remote_workstation/.env` missing), log and continue — the email + brief file on disk are the real audit trail. Don't fail the whole run on a missed ping.

### 9. Empty-run policy

If step 1+2 produced **zero** trending candidates that pass the wiki-fit + signal threshold:
- Skip steps 4-7.
- Send a 3-line email: "No notable trending material this week. Sources scanned: <count>. Next sweep: next Monday." Don't ship the long template.

This avoids weekly noise on slow weeks but still confirms the trigger ran.

## Failure modes & guard-rails

- **Capture dependency missing locally** (e.g. `marker` not installed) → fall back to `pymupdf` automatically; if both fail, drop that source.
- **A subagent's summary fails schema validation** → mark `failed`, exclude from page plan, note in run notes; don't retry inside the run (next week sees a fresh signal).
- **Conflict between selection-heuristic and the user's prior taste** → no recourse this week (autonomous); the brief lists what was picked so the user can correct via memory or by hand-editing this command before the next run.
- **`master_notes.md` entries** → if the run surfaces a kit-level gotcha (capture bug, schema parser quirk), append to `master_notes.md` with `Status: open`. Don't try to harvest in the same run.

## Local scheduling

This command runs locally via the user's crontab (or equivalent). A minimal install:

```bash
crontab -e
# Append (substitute your wiki's repo path and weekly-brief branch):
0 7 * * 1 cd /path/to/your-wiki && git checkout <weekly-brief-branch> && claude -p "/weekly-brief" >> /tmp/weekly-brief-cron.log 2>&1
# Example for the ai-trends wiki:
# 0 7 * * 1 cd /home/david/code/wiki-ai-trends && git checkout ai-trends-wiki && claude -p "/weekly-brief" >> /tmp/weekly-brief-cron.log 2>&1
```

Notes:
- Cron fires at **7am local time** (America/Toronto) — user-crontab times are local, not UTC.
- If the machine is off at fire time, the run is skipped for that week — no catch-up. Next Monday's run uses a fresh signal window anyway.
- `/tmp/weekly-brief-cron.log` is the invocation audit trail; the email + `wiki/log.md` + the uncommitted diff are the content audit trail.
- First-time install: also run `/weekly-brief` manually once to confirm Gmail MCP auth and capture tooling both work before relying on the cron.

## Why this command exists

The user wants to delegate the "what's interesting this week?" loop. The contract is: the local cron fires Monday 7am, the wiki absorbs the week's signal on the current branch (uncommitted), an email lands in the inbox by ~7:15 with the trends + the 5 things worth knowing + a prominent commit-on-next-login reminder. The commit stays manual so the user reviews the diff before it becomes history — and so a bad run can be `git restore`'d without a revert commit.

The command is wiki-agnostic: run it inside any wiki checkout and the brief is scoped to that wiki's `reference-sources.md` + `watchlist.md`. The repo path, repo name, and branch are resolved at runtime (step 0) so email, Telegram ping, and commit-reminder banner point at the right place.
