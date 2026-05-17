# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-05-14] bootstrap | AI × drones

Initial bootstrap. Schema and commands tailored for the AI × drone intersection, with R&D, manufacturing / Canadian onshoring, and physical-interaction (manipulation / perching / contact / payload / tethered) included as in-scope topics. Authoritative-source list seeded with named research groups (incl. UTIAS, McGill, Sherbrooke Createk on the Canadian side) and primary Canadian policy bodies (ISED, Transport Canada, DND/PSPC, NRC IRAP, AIAC, CCAA). Domain lint checks added for regulatory and benchmark staleness, intersection coverage, evidence-strength tagging, country-of-origin tagging, and Canadian-onshoring tracker freshness. Ready to receive first source.

## [2026-05-15] research+ingest | autonomy-and-sensors

Topic: "state of AI-navigated/autonomous drones; sensor types and purposes". 13 sources shortlisted, 10 ingested. Captured to `raw/research/autonomy-and-sensors/`. Dropped: 09 Skydio podcast (no transcript), 10 Anduril marketing (redundant w/ 11). Failed capture: cdnsciencepub fusion survey (JS/paywall). Source 12 (ASTM F3442) partial — scope only, perf thresholds paywalled.

Created 11 pages + 1 conflict: drone-autonomy-state, drone-sensors-for-autonomy, lidar-for-uav-autonomy, event-cameras, event-cameras-for-uavs, eth-rpg-scaramuzza, visual-inertial-slam, skydio-autonomy-stack, anduril-lattice, faa-part-108-bvlos, detect-and-avoid, conflicts/lidar-vs-vision-autonomy (**OPEN** — dominant contested claim: LiDAR-necessary vs vision/event-sufficient; documented both camps, no ruling).

Kit learnings logged to `master_notes.md` (Scope: kit): stale bundled yt-dlp broke fetch_transcript (fixed via pip -U); capture_pdf --engine pymupdf emits image refs it never writes (50 audit flags); cdnsciencepub.com + preprints.org are bot-walled despite being open-access (heuristic "open access = capturable" is false). All `Status: open` for `/harvest`.

## [2026-05-16] rescope | consumer focus

User set standing scope: wiki is **consumer drone uses only**; defence content welcome only as consumer-transferable technology, no defence-vs-consumer conflict/controversy/politics/ethics. Rescoped 6 pages — `anduril-lattice` reframed as a defence-origin autonomy/sensor-fusion *technology* page (removed HRW/Gaza, Luckey/Trump/Vance, defence-vs-consumer "theme"); removed the defence-vs-consumer tension + open-question from `drone-autonomy-state`; stripped defence-vs-civilian editorializing from `faa-part-108-bvlos` and `detect-and-avoid`; neutralised `skydio-autonomy-stack` + `index.md` descriptions. Saved to assistant memory (feedback + project) so it persists across sessions. Bootstrap `wiki/CLAUDE.md` still literally lists defence/ISR + defence-vs-consumer conflict — flagged to user as a candidate schema tweak, not yet applied.

Follow-ups still open: ASTM F3442 thresholds (paid standard; free review substitute on preprints.org also bot-blocked) and the cdnsciencepub multi-sensor-fusion survey (open-access but host-blocked) — both need manual PDF download to ingest.

## [2026-05-16] research+ingest | onboard-ai-energy

Topic: energy requirements of onboard AI on small drones; is it a limiter; can neuromorphic help. 14 shortlisted, 13 ingested (#13 de Croon "tiny-drones" YouTube talk deferred on a transient YouTube 429 — supplementary, retriable). Captured to `raw/research/onboard-ai-energy/`. CORE PDF needed a `core.ac.uk` fallback (files01 host 522). Audit: 97 dangling image refs = known pymupdf behaviour, text clean.

Created 4 pages: `drone-power-budget` (the answer: compute is NOT the limiter for most drones — propulsion 85–96% — but is a wall sub-30 g), `nano-drone-compute` (PULP/GAP conventional path), `neuromorphic-computing-for-drones` (Loihi/Speck/Kraken, MAVLab arc, honest limits), `neuromorphic-materials` (memristors, TRL ~2–3, long-horizon). The "is compute the limiter" tension handled as a scope-dependent synthesis section in `drone-power-budget` (not a conflicts/ entry — user opted to continue with that recommendation).

**Accuracy correction:** the primary (de Croon Science Robotics 2024, source 04) showed `event-cameras-for-uavs.md`'s secondhand "~0.94 W total" was actually Loihi *board idle*; corrected to 27 µJ/inference, 7–12 mW marginal network power. Cross-links + a power-budget tension bullet + an open question added to `drone-autonomy-state.md`.

Kit learning logged to `master_notes.md` (Scope: kit): when a wiki claim rests on a secondary review's quantitative figure, capturing the primary is high-value — a review here misattributed board-idle as inference power, off by ~100×.

## [2026-05-17] research+ingest | aerial-manipulation

Topic: how drones physically interact with objects in a consumer setting (grasp, door, transport, contact). 12 shortlisted; FlyCroTug (#7 science.org) paywall-blocked, proxied by an IEEE Spectrum article; HKU continuum-manipulator (08) failed capture (PMC reCAPTCHA + Europe PMC 500) — deferred to manual download. 10 sources ingested → 5 pages on recommended-defaults plan (user repeatedly launched new /research without ruling the packet; I committed to and applied my recommendations rather than let the work rot): `aerial-manipulation` (overview + consolidated consumer-gap list), `aerial-grasping`, `aerial-perching`, `drone-contact-and-door-tasks`, `cooperative-aerial-manipulation`. Backlinks added to `drone-autonomy-state`, `drone-sensors-for-autonomy`. Industrial Ollero/GRVC sources framed as research-foundation + gap evidence, not consumer content (per consumer scope). Answer: manipulation physics is lab-proven; consumer home use is 5–10+ yr out, gated by onboard perception (mocap-dependency is the universal blocker), payload, endurance, safety.

Kit learnings (master_notes, Scope: kit, open): shell cwd-drift mis-filed a whole capture batch + caused a false-delete scare (recommend repo-root-relative --out); PMC can serve a reCAPTCHA that passes the audit (add captcha-signature check to audit_captures).

## [2026-05-17] research+ingest | multimodal-locomotion

Topic: mixed-mode robots (drone + wheels/legs/arm; air/land/water) for effectual real-world action. 11 captured (Kovac air-water Science Robotics → Spiral SPA returned nothing, manual-download follow-up; M4 record-page re-captured as full PDF via Caltech direct link). 10 sources → 3 pages on the user's "proceed with recommendations": `multimodal-locomotion` (overview, taxonomy, energy rationale, consumer verdict), `air-ground-hybrids` (energy spine + hard-numbers table + AirCrab/M4 multimodal-manipulation section + FSTAR/LEONARDO journalism), `air-water-robots` (honest research-curiosity framing). Enriched `drone-power-budget` with a "Multimodal locomotion as an endurance lever" section (single-passive-wheel 77%, Roller-Quadrotor 41×, Tilt-Ropter 92.8%) + cross-links — the synthesis answer to "what beats the endurance ceiling": rolling-instead-of-hovering and perching, not battery chemistry alone. Answer to the user: yes, AirCrab (arm+active-wheel) and M4 (8-mode appendage-repurposing) exist; consumer-blocked by the same dual-mode-weight + onboard-perception/autonomy gaps as aerial-manipulation. LEONARDO has no primary in-corpus (journalism only) — flagged. Wiki now 24 content pages, all cross-links resolve.

## [2026-05-17] weekly-brief | first run

First `/weekly-brief` sweep (setup approved this session; session backlog committed separately as 8406936 first so the weekly commit is a clean delta). Trend scan (window 7d, ~13 sources): theme = onboard-compute convergence + peak US regulatory pressure on Chinese hardware (FCC/DJI comment deadline 11 May) + Canada onshoring consolidation + a crystallising VLA-for-aerial-manipulation subfield. 3 captures (quality over the 5-cap): Dream-to-Fly (ETH RPG, ICRA 2026 — pixel→control RL, added as Position-B to the open lidar-vs-vision conflict, with a real-camera-gap asterisk), AIR-VLA + DroneVLA (the VLA-aerial-manipulation pair → 2 paper pages + an "emerging subfield" note on `aerial-manipulation`, no speculative new cluster page per policy). VIO-no-LiDAR resurfaced but already in-wiki (`visual-inertial-slam`) — not re-captured. Part 108: no final rule in the window (EO-mandated ~Feb/Mar 2026 target appears slipped). Overflow → watchlist. 27 content pages, all links resolve.
