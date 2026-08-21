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


## [2026-08-20] weekly-brief | first manual run (pre-cron validation)

First `/weekly-brief` run from this checkout, run manually ahead of the Thursday-23:13 cron to validate the unattended path (capture tooling, ingest, SMTP delivery, Telegram) before trusting it to fire alone. Trend scan dispatched 5 parallel source-cluster agents (arXiv/alphaXiv, venues/community, trade press, vendors, programmes/benchmarks) against the pinned watched sources in `reference-sources.md`. Overall a quiet week — most vendor/venue searches surfaced only out-of-window (pre-2026-08-13) items — but the literature and trade-press sweeps surfaced enough for a full 5-source capture batch.

**Two capture-tooling bugs hit and worked around, both logged to `master_notes.md` as kit-level (`Status: open`):**
- `capture_pdf --src <arxiv.org/abs/...>` silently captured the arXiv *abstract landing page*, not the paper — the tool needs the direct `/pdf/` URL. Caught because the resulting `.md` was suspiciously short (~170-184 lines) and an ingest subagent flagged the missing body; both affected sources (`beyond-peak-tops-per-watt`, `loihi2-acoustic-anomaly-detection`) were re-captured correctly and re-ingested.
- `capture_url` against a fully open-access Nature Communications article (no paywall, no `## Access options` marker) returned abstract + metadata only, identically with and without `--js`. Unlike the previously-documented paywall signature, this has **no textual tell** — the existing structural-paywall grep check would not catch it. That source (`tetramem-hdc-edge-ai`) was downgraded to a watchlist entry rather than ingested as a full page, per the "watchlist the citation rather than ingest an abstract" convention.

**Captures: 5 attempted, 4 usable, 1 watchlisted.** `audit_captures` flagged 8 broken image refs (pymupdf figure-extraction misses on the two re-captured arXiv PDFs) — cosmetic, text bodies intact (1426 and 587 lines respectively), not treated as capture failures.

**Ingest — page plan (autonomous, no human gate):**
- NEW `[[chips/loihi2-persistent-monitoring]]` — the wiki's first primary Loihi 2 source, filling a named watchlist gap. Load-bearing finding: the paper's own "two orders of magnitude" headline is dynamic-energy-only (474–496×); the boundary-honest total-energy figure (same table, static power included) is 2.1–40.2×— a clean same-paper illustration of the measurement-boundary problem.
- EXTENDED `[[conflicts/snn-energy-payoff]]` — added that Loihi 2 illustration as new evidence, plus a new subsection on "Beyond Peak TOPS/W" (arXiv:2608.03514, MICRO 2026), a methodology paper generalizing this wiki's central efficiency-measurement conflict beyond SNNs to analog IMC and photonic computing.
- EXTENDED `[[players/brainchip]]` — BrainChip's Symphony Community Akida Bundle (IBM Spectrum integration), a software-orchestration commercial signal distinct from prior silicon/yield news.
- EXTENDED `[[devices/memristor-device-engineering]]` — a SAW-guided reconfigurable MoS₂ memristor (dual electrical/acoustic plasticity channels), sourced from a Semiconductor Engineering relay since the ACS Nano primary is paywalled with no preprint; flagged as a novelty note rather than a comparable table row given thin evidence.
- 10 overflow candidates added to `[[watchlist]]` (cap reached); one existing watchlist gap (Loihi 2) struck through as captured.

**Noteworthy noise, not signal:** three independent scan agents each separately surfaced and excluded the same SEO/content-farm claim of an "Intel Loihi 3" launch (8M neurons, 64B synapses, Q4 2026 availability) — no corroboration from intel.com or any primary source. Recorded here so it isn't accidentally re-surfaced as real in a future sweep. Similarly excluded: an unrelated "Neuromorphic Labs" seed round (AI-governance startup, name collision only) and unverified "IBM NorthPole 288-card" / "BrainChip Akida 2.0 in Mercedes-Benz" claims from the same low-quality sources.

Full brief: `wiki/weekly-briefs/2026-08-20.md`.

## [2026-08-21] research + ingest | seed sweep across six gap topics

Second content run, and the first to overlap with an autonomous one.

**Scope.** Six topics chosen against the four standing questions: incumbent chips, device families beyond RRAM, analog IMC competitors, event vision, SNN training methods, and China. 22 candidates shortlisted, 18 approved, **16 captured, 16 ingested**, all schema-valid.

**Captures.** 9 of 12 HTML succeeded. All 7 arXiv PDFs failed under marker: 6 of 7 lost to a 300 s timeout or SIGABRT while two other wikis ran concurrent marker jobs on the same box (16 cores, load 22–25). Re-ran with pymupdf per `research.md`'s own rule that the fallback is sanctioned once marker has failed on CPU — 6 of 6 succeeded, at the cost of figure binaries. One paper needed a 600 s retry. Audit: 9 issues, all broken image refs in pymupdf captures, explainable rather than silent.

**science.org is unusable.** Three DOIs, three hangs at exit 124, zero bytes — it never returns rather than refusing. Cost the wiki the NorthPole *Science* paper, TianjicX, and the ECRAM primary. The Open Neuromorphic fallbacks deliberately kept in the plan for exactly this carried the load.

**Pages (7 new + 1 conflict):** `players/intel-loihi2` (3-source merge), `players/ibm-northpole` (2-source merge), `devices/fefet-analog-imc`, `devices/event-cameras` (survey + vendor merge), `devices/analog-training-nonidealities` (2-source merge), `snn/snn-training-surrogate-gradients`, `snn/ann2snn-differential-coding`, and `conflicts/analog-onchip-training-viability`.

**Three sources were deliberately not made into pages** — Tianjic (7-year-stale community page, one hard number), EnCharge (one press release plus a ~2023 teaser), ECRAM (1.6 KB abstract relay). Each got a roster row or stub plus a watchlist entry instead. Every one of those was the ingesting subagent's own recommendation.

**The through-line got sharper.** Data movement dominates at every scale the wiki can now observe: ADC/DAC conversion in analog arrays, per-timestep memory traffic in digital SNN accelerators, NoC routing energy in the analytical model, chip-to-chip static power in a 24-chip LLM deployment (6.9× penalty), and static platform power in a 16-chip VPX box (16.05 W of 16.2 W with 74 of 2,048 cores used). And the SNN dividing line resolved: it is not spiking versus non-spiking, it is **whether the architecture contains a dense global mixing operation** — attention — that must be re-evaluated across timesteps.

**A correction to my own work.** `players/intel-loihi2` initially stated no measured Loihi 2 power figure existed in any captured source. The 2026-08-20 weekly-brief cron had already ingested one. Corrected, and the two findings converge: static power from underutilised chips swamps the dynamic-energy advantage, independently confirmed by an autoencoder on a 16-chip VPX board and an LLM on 24 chips.

**Also corrected: a subagent caught me.** I briefed the EnCharge ingest that EN100 uses charge-domain switched-capacitor compute. The source never says so — I had taken it from a search snippet, which this wiki's own rules forbid as a source. The agent refused to attribute it. The guardrail works on the orchestrator too.

**Radar fully verified.** 25 unverified sources checked, zero remain: 22 active, 21 probation, 3 blocked, 1 retired. Two rows had to be corrected after a WebFetch-based check produced false negatives — including marking Intel's own site `blocked`. Verify capturability with the capture tool, not WebFetch.

**Kit findings logged (3, all in the unattended path):** `capture_url` has no internal timeout so hostile hosts hang instead of failing; marker on CPU is not robust under machine contention and `/weekly-brief` has no fallback; and verification must use the capture tool rather than WebFetch. Combined with the weekly-brief run's own finding about open-access Nature Communications captures, that is four capture-layer issues worth a `/harvest`.

