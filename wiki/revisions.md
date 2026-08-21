# Revisions

Concise record of all wiki modifications. One row per logical change.

| Date | Action | Pages Touched | Summary |
|---|---|---|---|
| 2026-08-19 | bootstrap | CLAUDE.md, index.md, reference-sources.md, watchlist.md, commands | Initial bootstrap: neuromorphic materials, SNNs, and the industry's path to commercial viability. |
| 2026-08-20 | research + ingest | 10 new pages, index, watchlist, reference-sources | `/research neuromorphic commercial viability`: 8 sources captured and ingested (3 failed — 2 bot-walled/paywalled, quarantined). Seeded players, devices, snn, benchmarks, conflicts, and the viability ledger. |
| 2026-08-20 | radar evolution | reference-sources.md | Promoted arXiv/IOPscience/brainchip.com/IEEE Spectrum to `active` on evidence; Wiley → `blocked` (Cloudflare); nature.com flagged for abstract-only paywall captures; added DCD, Kalkine, SATA/SpikeSim, NeuroBench repos. Two new local conventions (structural paywall check, date-by-internal-evidence). |
| 2026-08-20 | scheduling | reference-sources.md | Installed weekly-brief cron: Thursday 23:13 local on `neuromorphic-wiki`. Recorded the line, the log path, and two caveats (never fired; yt-dlp broken). |
| 2026-08-20 | weekly-brief (first manual run) | chips/loihi2-persistent-monitoring (new), conflicts/snn-energy-payoff, players/brainchip, players/roster, devices/memristor-device-engineering, index, watchlist | First `/weekly-brief` run (manual, pre-cron validation). 5 sources captured, 4 fully usable (1 abstract-only, watchlisted instead of ingested). New Loihi 2 primary source page; extended the open SNN-energy conflict with a second boundary-effect illustration plus a generalizing methodology paper; extended BrainChip and memristor-device pages. |
| 2026-08-21 | research + ingest | 7 new pages, 1 new conflict, 7 extends | Seed sweep: 18 sources approved, 16 captured, 16 ingested. Incumbent chips (Loihi 2, NorthPole), FeFET, event cameras, SNN training taxonomy, ANN-to-SNN conversion, analog training non-idealities. |
| 2026-08-21 | conflict opened | conflicts/analog-onchip-training-viability | In-situ training as yield rescue vs Analog SGD collapsing on response-function asymmetry alone. Verified against page text: Li et al. is recorded as SGD-based, so the tension is real. |
| 2026-08-21 | radar verification | reference-sources.md | All 25 unverified sources checked; zero remain. science.org and EE Times blocked (hang, not refuse); Lava retired; 2 rows corrected after WebFetch gave false negatives. |
| 2026-08-21 | correction | players/intel-loihi2.md | Removed the claim that no measured Loihi 2 power figure exists — the 2026-08-20 weekly sweep had already ingested one. |

