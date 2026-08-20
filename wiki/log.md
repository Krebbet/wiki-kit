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

## [2026-08-20] research + ingest | neuromorphic commercial viability

First content run. `/research neuromorphic commercial viability` → 10 candidates shortlisted, all 10 approved for capture, 8 usable.

**Captures.** 6 HTML via `capture_url`, 4 arXiv PDFs via `capture_pdf --engine marker` on CPU (`CUDA_VISIBLE_DEVICES=""` — sudo unavailable to confirm GPU safe-mode clock caps, so marker was kept off the card). `audit_captures`: 0 issues.

**Three failures, both reported as success by the tooling:**
- Wiley (Adv. Intelligent Systems, aisy.202500806) — Cloudflare "Just a moment…" challenge, 755 bytes, exit 0, failed identically with `--js`.
- Nature Materials (s41563-026-02600-y) — exit 0 and 86 KB, but title + abstract + `## Access options` + references, **no body**. Size heuristics cannot catch this.
- Both quarantined to `raw/research/neuromorphic-commercial-viability/.failed/` with a README, and watchlisted rather than ingested.

**Ingest.** 8 subagents, one per source, all schema-valid on first pass. Subagent quality was high and materially improved the result: one caught OCR exponent corruption in an energy table and transcribed only the clean multipliers; one caught a 28 nm vs 65 nm inconsistency between a table caption and the experimental setup; one reconstructed a trade-press article's ~April 2024 vintage from internal evidence after finding no publication date in the capture, and correctly re-scoped every forward-looking claim in it.

**Aggregation was overridden on one point.** The mechanical aggregator returned `conflicts: []` and paired the two SNN-energy papers as merge candidates. But those two do not contradict each other — one finds claims inflated (10–83× claimed vs 1.3–25× measured), the other finds SNNs usually lose outright under capacity matching. Complementary, not opposed. The real conflict is those two **jointly against the vendor claims in the same batch** (Innatera's unbaselined "500× less energy", BrainChip's boundary-free sub-watt figures). Filed that way, with a NeuroBench system-track submission as the stated resolution condition.

**Pages written (10):** `players/roster`, `players/brainchip`, `devices/memristor-device-engineering`, `devices/memristor-array-integration-gap`, `devices/cmos-rram-beol-integration`, `snn/snn-energy-hardware-realistic`, `snn/snn-energy-breakeven-conditions`, `benchmarks/neurobench`, `conflicts/snn-energy-payoff`, `viability-ledger`.

**The through-line across all eight sources:** neuromorphic's efficiency problem is data movement and conversion, not arithmetic. Three independent routes converge on it — measured simulation, analytical modelling, and the analog device literature. The sharpest single number: dropping sparse-event routing overhead η from 12 to 1 flips an SNN from winning 1-of-12 configurations to 12-of-12.

**Standing-question status.** Always-on sparse sensing is viable now (Xylo: 60.9× less dynamic power than an Arduino at matched accuracy, boundary disclosed) and AKD1500 is shipping. General edge inference is not demonstrated and trends unfavourable under capacity-matched comparison. Analog CIM has no credible near-term date. And as of today **no vendor in this wiki has published an efficiency figure at a stated measurement boundary against a named baseline** — which is why the ledger tracks gates rather than dates.

**Radar evolved** on evidence: 4 sources promoted to `active`, Wiley `blocked`, nature.com flagged, 4 sources added, 2 local conventions learned.

## [2026-08-20] scheduling | weekly-brief cron installed

Branch `neuromorphic-wiki` pushed to origin (3 commits). `/weekly-brief` cron installed for **Thursday 23:13** local — slot picked to match the existing 23:13 group; the seven wikis on this machine now cover all seven days. Crontab verified byte-identical to the intended file after install, with a pre-change backup taken first.

One near-miss worth recording: the first generated cron line lost its `cd /home/david/code/wiki-neuromorphic &&` prefix, which would have run `git checkout neuromorphic-wiki` in `$HOME`. The shell tooling was stripping the literal `cd` token from the command string; the line had to be written via Python to survive intact. Caught before install by diffing the candidate file, not after. **Any future cron edit here should diff the candidate against `crontab -l` before and after installing.**

Not yet done: no manual `/weekly-brief` has ever run from this checkout, so the unattended path (capture tooling + SMTP delivery + Telegram) is unproven. The first Thursday firing is the real test. YouTube transcript capture remains broken (stale pinned `yt-dlp`) by explicit decision — the brief should skip video sources and say so.

