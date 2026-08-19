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
| **arXiv cs.NE (recent)** | Primary firehose for SNN and neuromorphic-architecture work. | https://arxiv.org/list/cs.NE/recent | unverified |
| **arXiv cond-mat.mtrl-sci (recent)** | Where the device/materials half of this wiki actually publishes. | https://arxiv.org/list/cond-mat.mtrl-sci/recent | unverified |
| **arXiv cs.AR (recent)** | Architecture and accelerator papers, incl. analog IMC. | https://arxiv.org/list/cs.AR/recent | unverified |
| **alphaXiv trending** | Popularity ranking over arXiv; catches what the field is reacting to. | https://www.alphaxiv.org/trending | unverified |
| **Open Neuromorphic** | The field's active open community — events, projects, hardware guides, job/funding chatter. Highest-signal single aggregator for this domain. | https://open-neuromorphic.org | unverified |

## Journals and venues (scan tables of contents)

| Source | Why | URL | Status |
|---|---|---|---|
| **Nature Electronics** | Where the flagship measured-array and integrated-chip papers land. | https://www.nature.com/natelectron/ | unverified |
| **Nature Materials / Nature Nanotechnology** | Device-stack and materials firsts. | https://www.nature.com/nmat/ · https://www.nature.com/nnano/ | unverified |
| **Nature Machine Intelligence** | Algorithm-side SNN work with hardware framing. | https://www.nature.com/natmachintell/ | unverified |
| **Neuromorphic Computing and Engineering (IOP)** | Open-access, dedicated to exactly this field. | https://iopscience.iop.org/journal/2634-4386 | unverified |
| **Frontiers in Neuroscience — Neuromorphic Engineering** | Long-running venue; variable quality, high volume. | https://www.frontiersin.org/journals/neuroscience/sections/neuromorphic-engineering | probation |
| **Advanced Materials / Advanced Intelligent Systems** | Materials-first synapse and crossbar work. | https://onlinelibrary.wiley.com/journal/15214095 | unverified |
| **IEDM** | The venue for "we taped this out and here are the numbers". Annual, December. | https://www.ieee-iedm.org | unverified |
| **ISSCC** | Chip-level energy and throughput results with credible measurement. Annual, February. | https://www.isscc.org | unverified |
| **NICE workshop (Neuro-Inspired Computational Elements)** | Where the community argues about what counts as progress. | https://niceworkshop.org | unverified |
| **Telluride Neuromorphic Workshop** | Talks and project outputs; strong for toolchain reality-checks. | https://tellurideneuromorphic.org | unverified |
| **ICONS (ACM Intl. Conf. on Neuromorphic Systems)** | Systems-level neuromorphic work. | https://dl.acm.org | probation |

## Trade press (event signal, never a technical source)

| Source | Why | URL | Status |
|---|---|---|---|
| **Semiconductor Engineering** | Best trade coverage of process/integration reality and foundry roadmaps. | https://semiengineering.com | unverified |
| **EE Times** | Product launches, funding, design wins. | https://www.eetimes.com | unverified |
| **IEEE Spectrum — semiconductors** | Occasional deep, well-sourced neuromorphic features. | https://spectrum.ieee.org/topic/semiconductors/ | unverified |
| **The Next Platform** | System-level framing and skeptical takes on efficiency claims. | https://www.nextplatform.com | unverified |

## Vendors, labs and foundries (scan press rooms and eng blogs)

| Player | Why for this wiki | URL | Status |
|---|---|---|---|
| **Intel Neuromorphic Computing Lab (Loihi / Hala Point)** | Largest research-scale digital neuromorphic programme. | https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html | unverified |
| **IBM Research (NorthPole, analog AI / PCM)** | The digital-vs-analog argument runs straight through IBM's own portfolio. | https://research.ibm.com/blog | unverified |
| **BrainChip (Akida)** | Publicly listed — filings and revenue are a hard viability signal, not a claim. | https://brainchip.com/news/ | unverified |
| **SynSense** | Ultra-low-power vision/audio SNN silicon; Rockpool toolchain. | https://www.synsense.ai | unverified |
| **Innatera** | Analog-mixed-signal spiking sensor processor; shipping-status claims worth tracking. | https://innatera.com | unverified |
| **Prophesee** | Event-camera side of the stack — the sensor that makes sparse workloads real. | https://www.prophesee.ai | unverified |
| **SpiNNcloud / SpiNNaker** | Manchester/TU-Dresden lineage commercialised; large-scale digital SNN. | https://spinncloud.com | unverified |
| **imec** | Foundry-adjacent device research; strongest signal on BEOL integration and PDK readiness. | https://www.imec-int.com | unverified |
| **CEA-Leti** | European device/integration programme, RRAM and FeFET. | https://www.leti-cea.com | unverified |
| **Mythic** | Analog IMC incumbent; its funding trouble history is a load-bearing cautionary case. | https://mythic.ai | probation |
| **EnCharge AI** | Charge-domain analog IMC — a serious competitor for the same edge sockets. | https://www.enchargeai.com | unverified |
| **Rain AI** | Analog/memristive compute startup; watch for silicon vs narrative. | https://rain.ai | probation |
| **Axelera AI** | Digital-IMC edge inference — the competitive baseline. | https://www.axelera.ai | probation |

## Programmes and funders

| Source | Why | URL | Status |
|---|---|---|---|
| **DARPA** | Programme starts and BAAs are 3–5-year leading indicators for US device work. | https://www.darpa.mil | unverified |
| **EBRAINS / EU Horizon** | European neuromorphic funding and infrastructure. | https://www.ebrains.eu | unverified |
| **US DOE labs (Sandia, ORNL, LANL)** | Neuromorphic-for-HPC and rad-hard/space angles. | https://www.sandia.gov | probation |

## Benchmarks, code and release proxies (discovery only)

| Source | Why | URL | Status |
|---|---|---|---|
| **NeuroBench** | The field's attempt at honest cross-vendor comparison — the single most load-bearing benchmark effort to track. | https://neurobench.ai | unverified |
| **Lava (Intel)** | Loihi's toolchain; release notes reveal what the hardware can actually do. | https://github.com/lava-nc/lava | unverified |
| **snnTorch** | Most-used surrogate-gradient training library; issue tracker shows real practitioner pain. | https://github.com/jeshraghian/snntorch | unverified |
| **Norse** | PyTorch-native SNN library. | https://github.com/norse/norse | probation |
| **Rockpool (SynSense)** | Vendor toolchain; deployment constraints visible in the docs. | https://github.com/synsense/rockpool | unverified |
| **Nengo** | Long-lived neuromorphic compiler/runtime with multi-backend support. | https://www.nengo.ai | probation |

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
- **Watchlist seeding policy:** agent-driven overflow only (cap 10/run). The initial watchlist ships empty.
- **Branch policy:** weekly output goes on `neuromorphic-wiki`, the wiki's working branch. No dedicated `weekly-*` branch.
- **Delivery:** email to `david.hugh.mcnamee@outlook.com`; Telegram ping enabled. Credentials come from the shared `/home/david/code/remote_workstation/.env`.
- **Frequency:** not yet scheduled — no crontab entry exists for this wiki. See `## Scheduling` below.

## Scheduling

No cron entry is installed yet. The house pattern (from the other wikis) is one staggered line per wiki:

```
MM HH * * D git checkout neuromorphic-wiki && /home/david/.local/bin/claude -p --dangerously-skip-permissions "/weekly-brief" >> /home/david/.local/share/weekly-brief/logs/neuromorphic.log 2>&1
```

Currently occupied slots across the other wikis: Sat 09:07, Sun 09:07, Mon 23:13, Wed 23:13, Fri 23:13. Tue and Thu are free. Install only after a manual `/weekly-brief` run has confirmed capture tooling and email delivery work from this checkout.

## Related

- [[watchlist]] — the persistent radar this file feeds
- [[index]] — wiki-wide page catalog
