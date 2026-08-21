# Reference sources

What `/weekly-brief` scans for **this wiki**, and what `/lint` evolves. High-signal-first; aggregators and venues before individual feeds. Setup-approved 2026-08-19 at bootstrap.

> **Seed provenance.** This initial set was assembled at bootstrap from prior knowledge of the field, **not** from a live sweep. URLs and the continued existence of each source are therefore `unverified` until the first `/weekly-brief` or `/lint` run touches them. Anything that 404s, has gone dormant, or proves low-signal should be demoted or retired on that first pass rather than carried forward on faith. Treat this file as a hypothesis about where the signal is.

## Status vocabulary

- `active` — swept every run.
- `probation` — newly added or low-yield; swept, but retired if it produces nothing on-topic across ~4 runs.
- `unverified` — seeded at bootstrap, URL and liveness not yet confirmed. Promote to `active` or retire on first contact.
- `retired` — struck out, kept for the record so it isn't re-added by mistake.

## Scope (the brief's frame)

**Focus on:**
- **Devices and materials** — memristor/RRAM, PCM, FeFET, MRAM/spintronic, ECRAM, Mott/VO2, 2D-material and photonic synapses. Especially: measured arrays, endurance/retention/variability data, BEOL and CMOS integration, foundry tape-outs.
- **Spiking algorithms and toolchains** — encoding, surrogate-gradient and ANN-to-SNN training, on-chip/local learning, reservoir computing, compilers and SDKs. Especially: results on a real chip rather than in simulation.
- **Chips, sensors and systems** — Loihi, NorthPole, Akida, SynSense, Innatera, SpiNNaker/SpiNNcloud, Tianjic, event cameras, and analog in-memory-compute accelerators competing for the same edge sockets.
- **Industry and viability** — funding, acquisitions, design wins, product launches, foundry PDK availability, government programmes, and any *dated* commercial claim with a named owner.
- **Benchmarks** — NeuroBench and anything that makes cross-vendor comparison honest.

**Exclude:**
- Conventional digital AI accelerator news (GPU/TPU/NPU) — except as the baseline neuromorphic is measured against.
- Computational-neuroscience and brain-simulation work with no hardware or algorithmic path to silicon.
- Market-forecast reports with unstated methodology ("neuromorphic market to reach $N B by 20XX").
- Review/survey papers that add no new measurement — unless they are the first credible cross-family comparison on a metric the wiki tracks.
- Press releases with no baseline, no boundary, and no number.

## Aggregators and feeds (scan first)

| Source | Why | URL | Status |
|---|---|---|---|
| **arXiv cs.NE (recent)** | Primary firehose for SNN and neuromorphic-architecture work. | https://arxiv.org/list/cs.NE/recent | active |
| **arXiv cond-mat.mtrl-sci (recent)** | Where the device/materials half of this wiki actually publishes. | https://arxiv.org/list/cond-mat.mtrl-sci/recent | active |
| **arXiv cs.AR (recent)** | Architecture and accelerator papers, incl. analog IMC. | https://arxiv.org/list/cs.AR/recent | active |
| **alphaXiv** | Popularity ranking over arXiv; catches what the field is reacting to. ⚠️ `/trending` 404s — corrected to root; live but shows a personalized/curated feed, not a clean trending list. | https://www.alphaxiv.org | probation |
| **Open Neuromorphic** | The field's active open community — events, projects, hardware guides, job/funding chatter. Highest-signal single aggregator for this domain. Confirmed live: dated blog posts (Feb 2026, Oct 2025), workshop calendar into Jul 2026, no barriers. | https://open-neuromorphic.org | active |

## Journals and venues (scan tables of contents)

| Source | Why | URL | Status |
|---|---|---|---|
| **Nature Electronics** | Where the flagship measured-array and integrated-chip papers land. ⚠️ Paywall risk: nature.com article pages fetch fine but yield abstract + references only for subscription content — see Local conventions. | https://www.nature.com/natelectron/ | probation |
| **Nature Materials / Nature Nanotechnology** | Flagship device and algorithm work. ⚠️ `capture_url` reaches nature.com fine, but **paywalled articles yield abstract + `## Access options` + references with no body** at a size that defeats the 2 KB thin-capture heuristic (confirmed on a Nature Materials article, 2026-08-19). An earlier WebFetch cookie-consent redirect-loop diagnosis was a WebFetch artifact. Apply the structural paywall check in Local conventions. | https://www.nature.com/nmat/ · https://www.nature.com/nnano/ | probation |
| **Nature Machine Intelligence** | Flagship device and algorithm work. ⚠️ `capture_url` reaches nature.com fine, but **paywalled articles yield abstract + `## Access options` + references with no body** at a size that defeats the 2 KB thin-capture heuristic (confirmed on a Nature Materials article, 2026-08-19). An earlier WebFetch cookie-consent redirect-loop diagnosis was a WebFetch artifact. Apply the structural paywall check in Local conventions. | https://www.nature.com/natmachintell/ | probation |
| **Neuromorphic Computing and Engineering (IOP)** | Open-access, dedicated to exactly this field. IOPscience captures cleanly and in full. | https://iopscience.iop.org/journal/2634-4386 | **active** |
| **Frontiers in Neuroscience — Neuromorphic Engineering** | Long-running venue; variable quality, high volume. | https://www.frontiersin.org/journals/neuroscience/sections/neuromorphic-engineering | probation |
| ~~**Advanced Materials / Advanced Intelligent Systems** (Wiley)~~ | ⚠️ **BOT-WALLED.** Cloudflare "Just a moment…" challenge; capture failed with and without `--js`, exit 0 both times with a 755-byte file. Do not attempt programmatic capture — request a manual PDF drop instead. | https://onlinelibrary.wiley.com/journal/15214095 | **blocked** |
| ~~**Science / Science Advances / Science Robotics** (AAAS)~~ | Flagship neuromorphic results appear here (NorthPole, TianjicX, Tiki-Taka ECRAM). ⚠️ **UNUSABLE — hangs.** Tested 2026-08-20 on three separate DOIs: `capture_url` returned exit 124 at a 90 s timeout with zero bytes every time, and an un-timed attempt consumed a full 2-minute budget on one URL. Fails differently from a Cloudflare challenge (which returns fast) — this burns the caller's whole time budget. **Never queue science.org in an unattended run.** Route around it: Open Neuromorphic covers NorthPole and Tianjic, Semiconductor Engineering relays abstracts, and arXiv preprints often exist. | https://www.science.org | **blocked** |
| **IEDM** | The venue for "we taped this out and here are the numbers". Annual, December. Confirmed live: 2026 CFP/registration open, no barriers. | https://www.ieee-iedm.org | active |
| **ISSCC** | Chip-level energy and throughput results with credible measurement. Annual, February. Confirmed live: already publishing 2027-cycle CFP content, no barriers. | https://www.isscc.org | active |
| **NICE workshop (Neuro-Inspired Computational Elements)** | Where the community argues about what counts as progress. Confirmed live: NICE 2027 featured plus 2025/2026 archives, no barriers. | https://niceworkshop.org | active |
| **Telluride Neuromorphic Workshop** | Talks and project outputs; strong for toolchain reality-checks. Confirmed live via redirect to a year-versioned Google Sites page (2026 content, 2027 dates posted); ⚠️ canonical domain no longer hosts content itself, just redirects — watch for the slug changing each year. | https://tellurideneuromorphic.org | active |
| **ICONS (ACM Intl. Conf. on Neuromorphic Systems)** | Systems-level neuromorphic work. | https://dl.acm.org | probation |

## Trade press (event signal, never a technical source)

| Source | Why | URL | Status |
|---|---|---|---|
| **Semiconductor Engineering** | Best trade coverage of process/integration reality and foundry roadmaps. ✅ Re-tested 2026-08-20: `capture_url` retrieves both homepage and article pages cleanly. An earlier WebFetch/curl check hit a Cloudflare challenge — **WebFetch artifact, not a real block**. Note its posts are often short abstract-relays of a primary paper; treat as a pointer, capture the primary. | https://semiengineering.com | **active** |
| ~~**EE Times**~~ | Product launches, funding, design wins. ⚠️ **UNUSABLE — hangs.** Re-tested 2026-08-20 with `capture_url`: exit 124, timed out at 90 s with zero bytes. Distinct from a Cloudflare challenge (which fails fast) — this burns the caller's whole time budget. Never queue it in an unattended `/weekly-brief` run without an explicit timeout. | https://www.eetimes.com | **blocked** |
| **IEEE Spectrum — semiconductors** | Occasional deep, well-sourced neuromorphic features. Captures cleanly. | https://spectrum.ieee.org/topic/semiconductors/ | **active** |
| **The Next Platform** | System-level framing and skeptical takes on efficiency claims. Confirmed live: dated headlines (Aug 2026), multi-times-weekly cadence, no barriers; marginal — neuromorphic-specific pieces are infrequent. | https://www.nextplatform.com | active |

## Vendors, labs and foundries (scan press rooms and eng blogs)

| Player | Why for this wiki | URL | Status |
|---|---|---|---|
| **Intel Neuromorphic Computing Lab (Loihi / Hala Point)** | Largest research-scale digital neuromorphic programme. ✅ Re-tested 2026-08-20: `capture_url` retrieves the page cleanly (5.7 KB). An earlier WebFetch check returned WAF 403 — that was a **WebFetch artifact, not a real block**. | https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html | **active** |
| **IBM Research (NorthPole, analog AI / PCM)** | The digital-vs-analog argument runs straight through IBM's own portfolio. Resolves and is live (posts dated through Aug 2026) but low signal density — no neuromorphic/NorthPole/PCM content in this snapshot; broad general-research blog. | https://research.ibm.com/blog | probation |
| **BrainChip (Akida)** | Publicly listed — filings and revenue are a hard viability signal, not a claim. Press room captures cleanly. | https://brainchip.com/news/ | **active** |
| **SynSense** | Ultra-low-power vision/audio SNN silicon; Rockpool toolchain. Confirmed live, on-topic, no barriers. | https://www.synsense.ai | active |
| **Innatera** | Analog-mixed-signal spiking sensor processor; shipping-status claims worth tracking. Confirmed live: dated newsroom through Jul 2026 (CES 2026, Computex 2025), no barriers on the main site. | https://innatera.com | active |
| **Prophesee** | Event-camera side of the stack — the sensor that makes sparse workloads real. Confirmed live: dated news through Jun 2026 (Mantara launch, €20M raise), no barriers. | https://www.prophesee.ai | active |
| **SpiNNcloud / SpiNNaker** | Manchester/TU-Dresden lineage commercialised; large-scale digital SNN. Resolves, on-topic, no barriers, but the news feed reads stale — most recent entry ~Jan 2025. | https://spinncloud.com | probation |
| **imec** | Foundry-adjacent device research; strongest signal on BEOL integration and PDK readiness. Resolves and live (dated 2026 stories) but homepage shows no neuromorphic/memristor/RRAM/BEOL content directly — point the watcher at /news or /articles rather than the root. | https://www.imec-int.com | probation |
| **CEA-Leti** | European device/integration programme, RRAM and FeFET. Confirmed live: dated 2026 press release on FeRAM/FeFET scaling to 22nm for edge AI, active news carousel. | https://www.leti-cea.com | active |
| **Mythic** | Analog IMC incumbent; its funding trouble history is a load-bearing cautionary case. | https://mythic.ai | probation |
| **EnCharge AI** | Charge-domain analog IMC — a serious competitor for the same edge sockets. Confirmed live: active, recently-dated news/blog section, no barriers. | https://www.enchargeai.com | active |
| **Rain AI** | Analog/memristive compute startup; watch for silicon vs narrative. | https://rain.ai | probation |
| **Axelera AI** | Digital-IMC edge inference — the competitive baseline. | https://www.axelera.ai | probation |

## Programmes and funders

| Source | Why | URL | Status |
|---|---|---|---|
| **DARPA** | Programme starts and BAAs are 3–5-year leading indicators for US device work. Resolves and live (active news section) but the homepage surfaced no neuromorphic-relevant programme; needs a specific office/programme page (e.g. MTO) rather than the root. | https://www.darpa.mil | probation |
| **EBRAINS / EU Horizon** | European neuromorphic funding and infrastructure. Confirmed live and on-topic: explicitly features "Neuromorphic Computing" as an infrastructure offering, dated news through Aug 2026. | https://www.ebrains.eu | active |
| **US DOE labs (Sandia, ORNL, LANL)** | Neuromorphic-for-HPC and rad-hard/space angles. | https://www.sandia.gov | probation |

## Benchmarks, code and release proxies (discovery only)

| Source | Why | URL | Status |
|---|---|---|---|
| **NeuroBench** | The field's attempt at honest cross-vendor comparison — the single most load-bearing benchmark effort to track. Framework confirmed real via the Nat. Comms. paper; site itself not yet fetched. Repos: github.com/NeuroBench/neurobench and /system_benchmarks. | https://neurobench.ai | **probation** |
| ~~**Lava (Intel)**~~ | ⚠️ **ARCHIVED 2026-05-13** — read-only. Intel's notice: "Intel will not provide or guarantee development of or support for this project" and "All Lava repositories are archived. Stay tuned for announcements about our new SDK and next generation Loihi processor." **Not an exit — a platform transition.** Re-add the successor SDK when it is announced; until then the reference toolchain for the field's most-used research platform is frozen. | https://github.com/lava-nc/lava | **retired** |
| **snnTorch** | Most-used surrogate-gradient training library; issue tracker shows real practitioner pain. Confirmed live: no archive banner, active issues/PRs (UCSC Neuromorphic Computing Group). | https://github.com/jeshraghian/snntorch | active |
| **Norse** | PyTorch-native SNN library. | https://github.com/norse/norse | probation |
| **Rockpool (SynSense)** | Vendor toolchain; deployment constraints visible in the docs. Confirmed live: no archive banner, active commit/issue history, hosted docs at rockpool.ai. | https://github.com/synsense/rockpool | active |
| **Nengo** | Long-lived neuromorphic compiler/runtime with multi-backend support. | https://www.nengo.ai | probation |

## Radar evolution

**2026-08-20 — first research run** (`/research neuromorphic commercial viability`). Eight sources captured, three failed. Changes made on evidence, not guesswork:

*Promoted `unverified` → `active`* (content actually retrieved this run): arXiv listings (4 PDFs via `capture_pdf --engine marker`), IOPscience, brainchip.com, IEEE Spectrum.

*Promoted → `probation`*: NeuroBench — the framework is confirmed real via its Nature Communications paper, but `neurobench.ai` itself has not been fetched.

*Demoted → `blocked`*: Wiley (Advanced Intelligent Systems). Cloudflare challenge, unrecoverable programmatically.

*Flagged*: nature.com — pages fetch but return abstract-only for paywalled content at a size that defeats the 2 KB thin-capture heuristic. See Local conventions.

*Added*: DataCenterDynamics, Kalkine, SATA/SpikeSim, Open Neuromorphic repos (below).

Everything still marked `unverified` has not been touched. That is a to-do, not a judgement.

**2026-08-21 — full verification pass.** Every source previously marked `unverified` was checked. **Zero remain.** Final: 22 `active`, 21 `probation`, 3 `blocked`, 1 `retired`.

Corrections worth recording, because the method mattered:

- An initial pass verified sources with **WebFetch** and marked three down on that basis — including **Intel's own neuromorphic-lab page** as `blocked` (WAF 403). Re-testing with `capture_url`, the tool the wiki actually captures with, showed **two of three were wrong**: Intel's page retrieves cleanly at 5.7 KB, and Semiconductor Engineering retrieves cleanly at both homepage and article level. Both promoted to `active`. **Verify capturability with the capture tool, never with WebFetch** — different clients, different blocking profiles. Logged to `master_notes.md` as kit-scope.
- **science.org added as `blocked`.** Three separate DOIs, three exit-124 hangs at a 90 s timeout, zero bytes. It does not refuse — it never returns. An un-timed attempt burned a full 2-minute budget on one URL. This costs the wiki the NorthPole *Science* paper, the TianjicX Science Robotics paper, and the ECRAM Tiki-Taka primary.
- **EE Times** confirmed `blocked` for the same reason — hangs rather than 403s, contrary to the earlier WebFetch diagnosis.
- **Lava `retired`** — archived 2026-05-13. Not an exit: Intel promises a new SDK and next-generation Loihi. Re-add the successor when announced.
- **nature.com** reason corrected — the earlier "cookie-consent redirect loop" was a WebFetch artifact. The real issue is abstract-only capture at a size that defeats the 2 KB heuristic. And per the 2026-08-20 weekly sweep, this now also affects **fully open-access Nature Communications articles with no paywall markers at all** — see `master_notes.md`.

### Added this run

| Source | Why | URL | Status |
|---|---|---|---|
| **DataCenterDynamics** | Funding rounds and vendor news; European neuromorphic coverage. ⚠️ Its article pages carry no publication date that `capture_url` records — date every capture by internal evidence. | https://www.datacenterdynamics.com | probation |
| **Kalkine / ASX commentary** | Only useful as a pointer to BrainChip's Appendix 4C filings. Never cite for a technical claim; go to the filing. | https://kalkine.com.au | probation |
| **SATA / SpikeSim** (Yale Intelligent Computing Lab) | Open hardware-realistic SNN benchmarking harnesses; the tooling behind the estimated-vs-actual energy critique. | https://github.com/Intelligent-Computing-Lab-Yale | probation |
| **NeuroBench repos** | The harness and system benchmarks themselves, more informative than the paper for what is actually measurable. | https://github.com/NeuroBench/neurobench | probation |

## Selection priority (per bootstrap)

When trimming candidates to the (≤5) capture list, priorities **in this order** for this wiki:

1. **Measured silicon over simulation** — an integrated chip with stated conditions beats a single-device demo, which beats a simulation-only result, every time.
2. **Moves a viability date** — does it change the answer to "when does this become commercially viable, and for what?" Tape-outs, foundry PDK availability, product launches, endurance/yield breakthroughs, and credible failures all qualify.
3. **Conflict-resolving** — would it settle or sharpen an open `wiki/conflicts/*.md`? Prioritise; new evidence on a live dispute is worth more than a new topic.
4. **Wiki-fit** — tightly on-scope per the Scope section above.
5. **Comparison honesty** — sources that state their measurement boundary, or that audit someone else's, rank above sources that don't.
6. **Reproducibility** — code/data/weights released > promised > closed.
7. **Multiple independent signals** — useful, but deliberately below technical merit. Neuromorphic has a long history of coordinated hype; mob attention is a weak proxy here.

## Local conventions for the brief

Preferences specific to *this* wiki. The agent running `/weekly-brief` in this checkout must honour them.

- **Never force entries.** If a section (Trends, Top 3, Other watchlist references, Conflicts) has nothing load-bearing, **omit it entirely**. Do not pad. A quiet week in a slow-moving hardware field is real information — say so in three lines rather than inventing a trend.
- **Hardware fields move slowly.** Weekly cadence will often surface incremental papers. Prefer reporting "no movement on X this week; the open blocker is still Y" over promoting filler to the Top 3.
- **Every number gets its boundary.** No efficiency, energy, endurance or accuracy figure enters the brief or a wiki page without units, conditions, and the measurement boundary (device / array / chip / system; inference / training). If the source doesn't state it, the brief says `(boundary unstated)` — that itself is the finding.
- **Separate evidenced / claimed / (synthesis)** in every trend bullet. Vendor roadmap dates always carry the owner's name.
- **Trend bullets must touch the four standing questions** (players, research, viability timeline, money/deployment). A bullet that answers none of them is noise.
- **Autogenerated pages link back to the brief.** Every page written during the autonomous ingest step includes in its `## Related` section: `- [[../weekly-briefs/<YYYY-MM-DD>]] — brought in by the <YYYY-MM-DD> weekly sweep`.
- **Paywall check is structural, not size-based.** A `capture_url` on a paywalled Nature article exits 0 and returns ~86 KB — title, abstract, `## Access options`, and the full reference list, with **no body**. The "under ~2 KB is a failure" heuristic cannot catch it. Before trusting any publisher capture, grep for `Access through your institution`, `Buy this article`, or an `## Access options` heading; if present, the body is missing. Watchlist the citation rather than ingesting an abstract.
- **Date every trade-press capture by internal evidence.** `capture_url` records `captured_on`, not the publication date. At least one source this run was ~2 years stale while reading as current. Reconstruct the vintage from the article's own dates and record forward-looking claims as "claimed as of &lt;date&gt;".
- **Watchlist seeding policy:** agent-driven overflow only (cap 10/run). The initial watchlist ships empty.
- **Branch policy:** weekly output goes on `neuromorphic-wiki`, the wiki's working branch. No dedicated `weekly-*` branch.
- **Delivery:** email to `david.hugh.mcnamee@outlook.com`; Telegram ping enabled. Credentials come from the shared `/home/david/code/remote_workstation/.env`.
- **Frequency:** not yet scheduled — no crontab entry exists for this wiki. See `## Scheduling

**Installed 2026-08-20.** `/weekly-brief` runs unattended every **Thursday at 23:13** local (America/Toronto), on the `neuromorphic-wiki` branch:

```
13 23 * * 4 cd /home/david/code/wiki-neuromorphic && git checkout neuromorphic-wiki && /home/david/.local/bin/claude -p --dangerously-skip-permissions "/weekly-brief" >> /home/david/.local/share/weekly-brief/logs/neuromorphic.log 2>&1
```

`4` is Thursday (0=Sun). Slot chosen to match the existing 23:13 group and avoid collision — the seven wikis on this machine now occupy all seven days.

- Invocation audit trail: `/home/david/.local/share/weekly-brief/logs/neuromorphic.log`
- Content audit trail: the email, `wiki/log.md`, and the pushed commit
- If the machine is off at fire time the run is skipped; no catch-up. The next week's sweep uses a fresh window anyway.

⚠️ **This cron has never fired.** It was installed before any manual `/weekly-brief` run, so capture tooling and email delivery are unproven from this checkout on the unattended path. First Thursday is the real test — check the log if no brief arrives.

⚠️ **YouTube transcript capture is broken** on this clone: the pinned `yt-dlp` (2024.12.23) is rejected by YouTube. Known and deliberately deferred; `/weekly-brief` should skip video sources and note the skip rather than retrying. Fix is `poetry update yt-dlp`. See `master_notes.md`.

## Related

- [[watchlist]] — the persistent radar this file feeds
- [[index]] — wiki-wide page catalog
