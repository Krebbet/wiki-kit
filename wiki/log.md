# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-08-19] bootstrap | neuromorphic materials, SNNs, and industry viability

Initial bootstrap. Cloned wiki-kit `main` @ `dd10a69` onto branch `neuromorphic-wiki`.

Schema and commands tailored for neuromorphic computing end to end — devices and materials (RRAM/PCM/FeFET/MRAM/ECRAM/Mott/2D/photonic), spiking algorithms and toolchains, chips and event sensors, and the industry around them. Scope explicitly includes non-spiking analog in-memory compute where it competes for the same edge sockets, and excludes conventional digital accelerators except as baseline.

Wiki organised around four standing questions: who the main players are, what research actually matters, when neuromorphic materials become commercially viable (and what gates each date), and where the money and deployments are.

Filled: `wiki/CLAUDE.md` (domain, goal, audience, tone, source types), and all five DOMAIN-SLOT regions — `research.md` authoritative-sources + source-type-notes, `ingest.md` takeaway-prompts, `lint.md` domain-lint-checks + trend-radar sweep, `query.md` answer-tone. The ingest takeaway template is device-aware: it forces measured numbers with their measurement boundary, a maturity-ladder position, a baseline-honesty check, and stated blockers.

Created beyond the template (bootstrap no longer seeds these, but `/weekly-brief` halts without them): `wiki/reference-sources.md` with a seeded-but-unverified radar of ~40 sources, and `wiki/watchlist.md` with `setup_approved: 2026-08-19`. Also `wiki/weekly-briefs/` and `wiki/lint-reports/`.

Toolchain verified on this clone: `capture_pdf --engine pymupdf` and `capture_url` both produce real captures; `pytest` 93 passed / 2 failed, both network smoke tests — stale `yt-dlp` (YouTube transcript capture broken) and a stdout-pollution bug in `capture_pdf`. Both logged to `master_notes.md` as kit-scope, `Status: open`.

Not yet done: no crontab entry for `/weekly-brief` (Tue and Thu slots are free); radar sources unverified until the first sweep.

Ready to receive first source.

