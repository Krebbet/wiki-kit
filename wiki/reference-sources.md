# Reference Sources — Weekly Radar

Signal sources scanned by `/weekly-brief` for this wiki's domain (AI products / offerings, enterprise platforms, startup radar, market reception). Ordered by signal-to-noise. Not all scanned every week — each brief run picks a small high-signal subset.

This wiki's domain is **AI product landscape**, not ML-paper research. The kit-shipped `/weekly-brief` command templates signal hierarchy for a paper-focused wiki (alphaXiv, r/MachineLearning); the `## Scope`, `## Selection priority`, and `## Local conventions` sections below **override** those kit defaults for this wiki.

## Scope

**In scope:**

- Enterprise AI platforms — Databricks, Snowflake, Salesforce, hyperscaler AI (AWS Bedrock, Azure AI, Google Cloud / Gemini Enterprise, Oracle), OpenAI/Anthropic platform products.
- Startup AI offerings — vertical agents (procurement, medtech, legal, insurance), horizontal agents (coding, knowledge-work), agent infrastructure (observability, orchestration, inference), AGI-research labs shipping product or benchmark evidence.
- Funding announcements, M&A, major launches where they reveal landscape shifts.
- Practitioner adoption data — HN threads, G2 reviews, GitHub issue volume, Stack Overflow question volume, practitioner blogs.
- Build-vs-buy signal — pricing, deployment, customization, running costs, hard limits.
- Analyst / VC framings (a16z, Bessemer, Menlo, consultancy State-of-AI reports) — with **named skepticism** (portfolio disclosure, incentive alignment).
- Occasional ML research papers **only when load-bearing for a shipping product's claimed technique**.

**Out of scope:**

- Pure ML research without a shipping-product angle — arXiv trending, alphaXiv, paperswithcode leaderboards are default-skip.
- X / LinkedIn thought-leadership posts — default-discount unless they contain non-public specifics (e.g. a practitioner post-mortem with named customers).
- **Consumer-hardware AI products** — AI pins, smart glasses, standalone consumer AI devices. Explicitly excluded even when buzzy.
- Generic SaaS news without an AI-product-landscape angle.
- Regional-market news without supply-chain or geopolitical relevance.

## Selection priority

Overrides the kit default (which is paper-focused). Applied in order when picking ≤5 captures per weekly run:

1. **Multi-source cross-confirmation** — trade-press + HN + vendor-first-party ≫ single-source mention.
2. **Novel mechanism / new technique** — a shipping product or platform move with a genuinely new capability (harness architecture, control-plane primitive, integration pattern, agent governance model) outranks incremental volume or category-level funding. A novel-mechanism single-product launch beats the 47th vertical-agent seed round.
3. **Practitioner-verifiable > vendor-claimed** — HN / G2 / GitHub-issue-volume / practitioner-blog evidence outweighs a vendor launch post on the same topic.
4. **Conflict-load-bearing** — extends or resolves an open entry in `wiki/conflicts/*.md`; weight higher when it would upgrade a "watching" flag to "resolved."
5. **Landscape-level readthrough** — category-revealing funding / M&A (e.g. a hyperscaler-lab structured deal, a record valuation for a category) still counts, but secondary to novel-mechanism signal.
6. **Wiki-fit** — must match the Scope list above.

**Hard skip:** pure vendor-PR without independent corroboration; research-only papers with no shipping-product angle; consumer-hardware AI.

## Local conventions

- **Voice:** terse, expert, facts-first, no hedging. Lead with the conclusion (buy / build / watch / avoid) when a question admits one, then the evidence.
- **Date every claim** about pricing, features, or adoption. Flag anything >6 months old as potentially stale.
- **Scare-quote vendor marketing adjectives** ("industry-leading", "state-of-the-art", "best-in-class") rather than repeating them. When evidence is thin, say it's thin — don't hedge.
- **Friction-surface outranks vendor marketing** — G2 reviews, HN threads, GitHub issues, Stack Overflow volume beat press releases on contested questions.
- **Bot-walled hosts** (see section below): if a source is needed from one of those, user downloads manually to `raw/research/<topic>/`; do not retry the capture script.
- **Cadence:** weekly **Sunday 7am America/Toronto** via the user's local cron (see Weekly sweep schedule). 7-day window by default; `--since` arg overrides.
- **Autonomous:** no human gate mid-run; the brief is the audit trail.
- **Don't commit.** Changes land uncommitted on the current branch; user commits on next login after reviewing the diff.
- **Kit-level learnings** (tool bugs, command gaps) → append to `master_notes.md` with `Status: open`. Don't harvest mid-run.

## Tier 1 — trade press (primary product / funding signal)

- **TechCrunch AI** — https://techcrunch.com/category/artificial-intelligence/ — funding announcements, product launches, enterprise moves. Solid signal-to-noise.
- **The Information — AI beat** — paywalled; capture whatever's accessible via RSS or excerpt.
- **Stratechery (Ben Thompson)** — strategy-level analysis of platform moves; paywalled.
- **VentureBeat — AI** — https://venturebeat.com/category/ai/ — product launches, enterprise deployments.
- **The Register — AI / Software** — practitioner-tone coverage of enterprise software moves; useful counter-signal to vendor PR.

## Tier 2 — practitioner friction surface (ground truth)

- **Hacker News front page + "Ask HN" threads** — https://news.ycombinator.com/ — first-class ground-truth evidence per this wiki's `/research` authoritative-sources policy.
- **r/LocalLLaMA** — https://reddit.com/r/LocalLLaMA — practitioner use / model reception / deployment specifics.
- **r/MachineLearning** — adjacent signal; useful for when ML research crosses into product land.
- **G2 / Reddit / product-specific subreddits** — for offerings already profiled (e.g. r/Salesforce when tracking Agentforce adoption).
- **GitHub issues + Stack Overflow question volume** on tracked products — for real-usage / real-limitation signal.

## Tier 3 — analyst / VC thesis (framing, with skepticism)

- **a16z** — https://a16z.com/ai/ — CIO surveys, thesis posts. Skepticism applied: a16z is an OpenAI investor.
- **Bessemer Venture Partners — Atlas** — https://www.bvp.com/atlas/ — thematic roadmaps (e.g. AI Infrastructure Roadmap). Skepticism applied: portfolio companies named without per-company disclosure.
- **Menlo Ventures — Perspective** — https://menlovc.com/perspective/ — annual State of Enterprise GenAI report. Skepticism: Anthropic investor.
- **Deloitte / McKinsey / BCG — State of AI surveys** — macro adoption framing. Skepticism: consultancy pay-to-play + Gartner-style dynamics.
- **Andreessen / Benchmark / Sequoia podcast transcripts** — track for specific named companies.

## Tier 4 — startup signal

- **Y Combinator launch tweets / demo-day batch pages** — https://www.ycombinator.com/companies — batch-level signal.
- **Product Hunt AI category** — consumer / prosumer launches. Skew toward enterprise-adjacent; **consumer-hardware AI is out of scope** regardless.
- **Extruct AI / Crunchbase / PitchBook** — structured batch and funding data; paywalled in varying degrees.

## Tier 5 — vendor first-party (primary features / pricing)

- **Anthropic news / product pages** — https://www.anthropic.com/news
- **OpenAI blog** — https://openai.com/blog — JS-heavy; capture with `--js` or fall through to a third-party excerpt.
- **Google Cloud / AWS / Azure / Databricks / Snowflake blogs** — launch posts, pricing pages, changelogs.
- **Salesforce news / developer blog** — product launches, TDX announcements.

## Tier 6 — long-form / podcasts (deeper context)

- **Latent Space podcast** — https://latent.space/ — engineer-to-engineer depth on specific products.
- **Dwarkesh Patel podcast** — long-form founder / researcher interviews.
- **The Cognitive Revolution** — enterprise-tilted AI interviews.
- **Lenny's Newsletter** — product-management lens.

## Known bot-walled hosts

Hosts reproducibly block the capture scripts (logged in `master_notes.md`). When a source is needed from one of these, the user downloads manually via browser and drops the file into `raw/research/<topic>/`:

- **MDPI** — Akamai/edgesuite "Access Denied" on HTML and PDFs.
- **ScienceDirect** — Cloudflare IP-block.
- **McKinsey** — HTTP/2 protocol error on HTML, read-timeout on PDFs (reproducible).
- **GeekWire** — Cloudflare "Attention Required" (reproducible including with `--js`).
- **OpenAI blog** — JS-heavy, `networkidle` times out at 30s; try `--js` with a longer timeout, or use a third-party summary / excerpt.

## Weekly sweep schedule

`/weekly-brief` is configured to fire **Sunday 7am America/Toronto** (user's local timezone — crontab interprets as local, not UTC). The cron line in the user's crontab:

```
0 7 * * 0 cd /home/david/code/wiki-ai-offerings-trends && git checkout ai-offerings-trends-wiki && claude -p "/weekly-brief" >> /tmp/weekly-brief-cron.log 2>&1
```

`0 7 * * 0` = 07:00 Sunday. (The prior 2026-04-22 and 2026-04-23 runs fired on Wednesday and Thursday respectively as interactive runs, before the Sunday cadence was set.)

The `git checkout` step ensures the run lands on the intended weekly-brief branch even if the working tree was left on `main` after a `/harvest` or other operation.
