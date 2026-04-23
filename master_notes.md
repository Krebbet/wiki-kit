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

### 2026-04-22 — `audit_captures` false-positives on `capture_pdf --engine pymupdf` image refs
**Scope:** kit
**Observation:** Captured the Menlo Ventures PDF with `capture_pdf --engine pymupdf`. The resulting markdown embeds images with repo-root-relative paths like `![](raw/research/<topic>/assets/<slug>/source.pdf-N-M.png)`. The files exist at that exact path (verified with `test -f`), but `tools.audit_captures` reports every one of them as "Broken image refs (file not found)" — 19 for an 18-page PDF. Other audit sections (paired PDF, thin captures, image collisions) were clean, so the capture itself succeeded.
**Implication:** Path resolution mismatch between the two tools. Either `capture_pdf` should write image refs relative to the markdown's directory (the convention audit appears to expect), or `audit_captures` should also try resolving refs relative to repo root. Until fixed, lint and research flows will surface a large block of spurious issues on any PDF capture, drowning real signal.
**Status:** open

### 2026-04-22 — `/weekly-brief` hardcodes the wrong wiki path and domain
**Scope:** kit
**Observation:** `/weekly-brief` (shipped by `feat(weekly-brief)` commit 2d40bd1) assumes the wiki is named `wiki-ai-trends` on branch `ai-trends-wiki` and focuses on ML-paper trends (alphaXiv / r/MachineLearning / AK X timeline). Commit reminder literal: `cd /home/david/code/wiki-ai-trends && git add ... && git checkout ai-trends-wiki`. For this wiki (`wiki-ai-offerings-trends`, main, product / offerings focus), both the path and the signal hierarchy are wrong. Adapted in this run by building a domain-appropriate signal list on the fly (`wiki/reference-sources.md`) and using product-radar sources (TechCrunch, HN, vendor blogs, trade press) instead of arXiv.
**Implication:** `/bootstrap` should seed `wiki/reference-sources.md` and `wiki/watchlist.md` with domain-appropriate scaffolding (new DOMAIN-SLOTs in the weekly-brief command itself, or a step in bootstrap that writes the starter file). Commit reminder in `/weekly-brief` should derive the repo path from `$PWD` / `git rev-parse --show-toplevel` and the branch from `git branch --show-current`, not hardcode. And the trend-scan signal hierarchy in `/weekly-brief` should have a DOMAIN-SLOT so different wikis pick different sources.
**Status:** open

### 2026-04-22 — OpenAI blog (openai.com/index/...) times out on `networkidle`
**Scope:** kit
**Observation:** `capture_url` on openai.com/index/scaling-codex-to-enterprises-worldwide/ times out at Playwright's 30s `networkidle` deadline, with or without `--js`. Reproducible across two attempts. Other vendor blogs in the same run (anthropic.com/news, salesforce.com/news, c3.ai, googlecloudpresscorner.com) captured cleanly.
**Implication:** OpenAI's marketing site has a long-tail asset request pattern that never quiets. Options: (a) add `--wait domcontentloaded` fallback flag to `capture_url` for known-slow hosts, (b) document openai.com/index/... in the known-bot-walled-hosts list and advise manual download / third-party summary. Should be added alongside GeekWire / McKinsey / MDPI / ScienceDirect.
**Status:** open

### 2026-04-22 — GeekWire is Cloudflare-bot-walled
**Scope:** kit
**Observation:** `capture_url` on `geekwire.com/2026/...` returns a Cloudflare "Attention Required" page (~2472 bytes body, title `Attention Required! | Cloudflare`). Reproducible across two attempts, including with `--js` flag. `capture_url`'s block-page signature detection correctly flagged it and exited non-zero — that part worked.
**Implication:** GeekWire belongs on the "Known bot-walled hosts" list in `research.md` alongside MDPI / ScienceDirect. Worth either (a) documenting in that list, or (b) fixing Playwright fingerprint to look more human (user-agent, viewport, TLS cipher order).
**Status:** open

### 2026-04-22 — parallel Bash tool calls cascade-cancel on a single error
**Scope:** kit
**Observation:** During `/research`, ran 8 captures as parallel Bash tool calls in a single message. One McKinsey PDF timed out; the remaining 5 siblings were cancelled with `Cancelled: parallel tool call Bash(...) errored` despite being entirely independent work. Had to re-dispatch. On the second batch, worked around it by wrapping each command as `<cmd> 2>&1; echo "---exit=$?"` so the shell always exits 0.
**Implication:** Research (and any other command that runs independent captures in parallel) should either dispatch one-by-one or instruct the agent to wrap each parallel capture in `|| true` / trailing `; echo ok` to prevent cascade. Worth adding a sentence to `research.md` step 4 so future agents don't lose a batch to one bot-walled URL.
**Status:** open

