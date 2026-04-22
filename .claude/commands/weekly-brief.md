# Weekly Brief

Self-directed weekly research sweep: scan watched sources for what's *trending* in AI/ML, pick the most significant new papers, capture + ingest them into the wiki autonomously, then email a concise brief to the user.

This command is the payload of the Monday-morning `RemoteTrigger`. It runs **unattended** — no human gate. The brief is the audit trail.

## Arguments

$ARGUMENTS — optional override for the trend-scan window (e.g. `--since 14d`). Default window is 7 days.

## Critical rules

- **Autonomy.** No human gate. Every decision the orchestrator would normally surface (page plan, conflict rulings, prune list) is made by the agent using the heuristics below.
- **Cap on captures.** Hard limit: **5 papers per run**. If more look interesting, the surplus goes straight to `wiki/watchlist.md`. The brief is a brief.
- **Inherit `/research` and `/ingest` rules.** Don't re-summarize source bodies in the main agent. Subagent-per-source. Capture scripts are the default. No `WebFetch` for source content.
- **Commit, then email.** The wiki update lands as a single commit on `ai-trends-wiki` (or the configured branch). The email goes out only after the commit succeeds; if commit fails, log the error and email a degraded brief saying "this week's run failed at <step>."

## Process

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
- arXiv → `poetry run python -m tools.capture_pdf --src <URL> --out raw/research/weekly-<YYYY-MM-DD> --slug <slug> --engine marker` (or `--engine pymupdf` if marker is unavailable in the remote env; fall back gracefully).
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

Write to `/tmp/weekly-brief-<YYYY-MM-DD>.md` with **exactly** this shape:

```markdown
Subject: Weekly AI radar — week of <YYYY-MM-DD>

# Trends this week (synthesis)
- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4-6 if warranted>

# Captured (N papers)
- **<short title>** — <one sentence on what's new and why it matters>. [[<wiki-slug>]]
- ... (one per captured paper, max 5)

# Closer-look candidates from the watchlist
- <title> — <URL or arXiv ID> — <1-line why-trending>
- ... (cap 10)

# Conflicts opened or extended this week
- [[conflicts/<slug>]] — <one sentence on the position>
- (omit section if none)

# Run notes
- Sources scanned: <count>
- Captures attempted / succeeded: <a> / <b>
- Wiki pages written: <count>
- Commit: <short SHA>

— Weekly brief generated by /weekly-brief on <ISO timestamp>
```

The wiki-link `[[...]]` notation will not render in plain-text email; that's intentional — they're pointers for the user to grep against in their checkout. If sending HTML, render them as relative GitHub links to the `ai-trends-wiki` branch.

### 7. Commit

Single commit on `ai-trends-wiki` (or configured branch):

```bash
git add wiki/ raw/research/weekly-<YYYY-MM-DD>/
git commit -m "weekly: <YYYY-MM-DD> radar sweep — <N> papers, <M> watchlist additions

Co-Authored-By: Claude (weekly-brief) <noreply@anthropic.com>"
git push origin <branch>
```

Capture the short SHA for the brief.

### 8. Send email

Use the Gmail MCP `send` tool to `krebbet@gmail.com` with the brief body. Subject line per template. If Gmail MCP is not authenticated/available in the remote session, log the failure prominently in the run output (the brief file at `/tmp/weekly-brief-<YYYY-MM-DD>.md` is still on disk for manual recovery), and exit non-zero.

### 9. Empty-run policy

If step 1+2 produced **zero** trending candidates that pass the wiki-fit + signal threshold:
- Skip steps 4-7.
- Send a 3-line email: "No notable trending material this week. Sources scanned: <count>. Next sweep: next Monday." Don't ship the long template.

This avoids weekly noise on slow weeks but still confirms the trigger ran.

## Failure modes & guard-rails

- **Capture script missing in remote env** (e.g. `marker` not installed) → fall back to `pymupdf` automatically; if both fail, drop that source.
- **A subagent's summary fails schema validation** → mark `failed`, exclude from page plan, note in run notes; don't retry inside the run (next week sees a fresh signal).
- **Conflict between selection-heuristic and the user's prior taste** → no recourse this week (autonomous); the brief lists what was picked so the user can correct via memory or by hand-editing this command before the next run.
- **`master_notes.md` entries** → if the run surfaces a kit-level gotcha (capture bug, schema parser quirk), append to `master_notes.md` with `Status: open`. Don't try to harvest in the same run.

## Why this command exists

The user wants to delegate the "what's interesting this week?" loop. The contract is: the trigger fires Monday 7am, the wiki absorbs the week's signal, an email lands in the inbox by 7:15 with the trends + the 5 things worth knowing about. Anything more requires the user to dig into the wiki — which is exactly the point of having one.
