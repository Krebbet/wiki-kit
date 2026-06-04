# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-06-04] research+ingest | humanoid-robot-indoor-perception

Topic: perception stacks for commercially deployed / near-deployed mobile manipulation robots — Figure 02/03, 1X NEO/EVE, Boston Dynamics Spot + Orbit, Agility Digit, Apptronik Apollo.

18 captures attempted; 11 substantive (Boston Dynamics blog pages and 1x.tech bot-walled throughout — navigation fragments only). Usable: GraphNav Tech Summary / Map Structure / Localization primary SDK docs; Figure Helix 02 + Helix v1 vendor blog posts; Orbit 5.0 Robot Report; Agility Digit botinfo deep-dive; arXiv:2501.05750 semantic mapping survey (pymupdf, text intact); Robotics 24/7 Spot/Orbit update; BD-DeepMind Gemini integration; Apptronik Apollo Robot Report.

Key findings: (1) Spot/GraphNav is the only publicly documented persistent-map architecture — waypoint/edge topological graph, fixed at record time, no global frame, visual+geometric feature localization ≥2 Hz, LOST failure mode. (2) Orbit 5.0 uses VLP prompts at inspection points; Gemini Robotics-ER 1.6 integration adds language-driven task planning. (3) Figure Helix 02: 6 RGB cameras + fingertip tactile, no LiDAR, no persistent map, fully onboard dual GPU, zero-shot object picking. (4) Agility Digit: torso LiDAR + 4× RealSense depth + force sensors, logistics-first, Amazon + GXO deployment. (5) Apollo: stereo cameras + force sensing, undisclosed stack.

New page: `humanoid-robot-indoor-perception.md`. Index and revisions updated.

---

## [2026-06-04] research+ingest | tidy-benchmarks

Benchmark landscape for home tidying/rearrangement. 8 sources captured to `raw/research/tidy-benchmarks/` using pymupdf engine (marker engine OOM on this system — numpy/pyarrow conflict). Captures: BEHAVIOR-1K (arXiv 2403.09227, 162KB), HomeRobot OVMM (arXiv 2306.11565, 131KB), AI2-THOR Rearrangement/RoomR (arXiv 2103.16544, 61KB), TEACh (arXiv 2110.00534, 99KB), ALFRED (arXiv 1912.01734, 112KB), HomeRobot NeurIPS 2023 challenge lessons (arXiv 2407.06939, 69KB), Housekeep (arXiv 2205.10712, 114KB), AI2-THOR challenge page (2KB — thin but usable for 2022 challenge winner result). All text substantive; images not extracted (pymupdf limitation, not a blocker). Audit: 253 broken image refs (expected, pymupdf), 0 thin captures, 0 PDF collisions.

New page `tidy-benchmarks.md` written. Key deliverables: (1) 4-type task definition taxonomy; (2) per-benchmark SOTA success rate table with source-traceable numbers; (3) HomeRobot OVMM identified as only benchmark with real-robot track; (4) perception stack per benchmark (Housekeep uses privileged segmentation; HomeRobot RGB-D + open-vocab); (5) BEHAVIOR-1K sim-to-real gap measured: 40% sim → 22% real-optimal → 0% real-learned; grasping = 40% of real failures; (6) TidyBot 85% real-hardware metric documented (internal evaluation, not public benchmark). Editorial synthesis sections clearly labelled.

---

## [2026-06-04] research+ingest | ov3d-instance-seg

Open-vocabulary 3D instance segmentation research. 8 sources captured to `raw/research/ov3d-instance-seg/` using pymupdf engine (marker engine OOM due to numpy/pyarrow conflict on this system). All captures >10 KB; audit: 0 issues. New page: `ov3d-instance-seg.md`. Key findings: FOLK (Oct 2025) is SOTA at AP50 35.7 / 3.6 s/scene on ScanNet200; none of the methods runs on 4 GB GPU live; FOLK inference (~Mask3D+MLP only) is the closest with estimated ≥4–6 GB; passive-stereo ~48% coverage is the binding constraint before GPU budget.

---

## [2026-06-04] research+ingest | language-3d-scene-representations

Research on language-embedded 3D scene representations (LERF, LangSplat, Feature3DGS, ConceptFusion, OpenGaussian, OpenLex3D). 6 primary arXiv PDFs captured via pymupdf engine (marker engine OOM on this system — numpy/pyarrow version conflict). New page: `language-3d-scene-representations.md`.

Key findings: LangSplat (CVPR 2024) is 2024/2025 practical leader — 84.3% localization, 0.28 s/query, ~4 GB GPU on small scenes. ConceptFusion (RSS 2023) most compute-accessible (no per-scene training, incremental online build, multi-modal text/image/audio/click queries). OpenGaussian (NeurIPS 2024) best for 3D robotics tasks (lossless CLIP, handles occlusion). OpenLex3D (NeurIPS 2025 D&B) shows no single method dominates segmentation + retrieval across Replica/ScanNet++/HM3D. Key conclusion: language fields and the explicit DINOv2 fingerprint bank are **complementary** — language field for novel-object discovery, object library for per-instance identity + cheap dynamic updates. 4 GB GPU is barely feasible for LangSplat on small scenes; not multi-room.

---

## [2026-06-04] research+ingest | consumer-robot-vacuum-mapping

Research on production robot vacuum floor mapping 2023–2026 (Roborock S8 MaxV Ultra, Dreame L20/X40 Ultra, iRobot j9+, Dyson 360 Vis Nav, Ecovacs X5 Pro). 11 valid captures (5 bot-walled). New page: `consumer-robot-vacuum-mapping`. Covers room segmentation (RoomsSeg watershed + ROSE² DFT academic SOTA), furniture-move timeline (2–5 runs), multi-floor architecture (independent 2D maps), obstacle classification (SLAM layer cannot distinguish table leg from wall), and gap vs SLAM Toolbox (comparable raw accuracy, gap is semantic labels + map update policy).

## [2026-06-04] research+ingest | commercial-home-robots-perception

Research on perception/mapping stacks of commercial home robots beyond robot vacuums. 10 sources captured and ingested. New page: `commercial-home-robots-perception`.

Key findings by robot:
- **Astro:** V-SLAM confirmed (Amazon Science primary posts); visual odometry → loop closure → bundle adjustment, 6-DOF on-device; sensor fusion with wheel encoders + IMU; deep-learning for lighting-invariant representations; multi-layer long-term map (room-level to object-level); person-following with proxemics; 2D obstacle map pushed to cloud only at end of exploration run.
- **Dyson 360 Vis Nav:** 360° fisheye-only SLAM (no LiDAR confirmed by both Dyson primary and independent reviewer); 26 sensors for obstacle avoidance and dust detection (separate from nav camera); 71mm position accuracy; nav layer / collision layer definitively separate (camera NOT used for cable/pet avoidance).
- **Matic:** 5 RGB+IR cameras, no IMU, no LiDAR; Jetson Orin Nano 4GB; image-to-voxel NN producing 1cm³ voxels; absolute map (dock is just a landmark); night operation via IR LEDs; full on-device for privacy+latency; co-founder AMA is unusually detailed primary source.
- **Ballie:** spatial LiDAR confirmed (TechCrunch CES 2024); front+rear cameras; floor plan mapping; repeated delays, not yet shipping.
- **Servi:** LiDAR+cameras, classical structured-environment nav, cloud fleet management; restaurant context, not transferable to home.

Transfer lessons for home tidying robot: Matic's stack is most transferable; Astro's multi-layer map is the right conceptual model; nav/collision layer separation is universal pattern; absolute maps strictly better than relative-to-dock; semantic room understanding is shallow user-labelled in all commercial systems (still a research frontier).

---

## [2026-06-04] research+ingest | apple-roomplan

Researched Apple RoomPlan parametric room scanning and Vision Pro spatial computing. 9 sources captured; 7 substantive (2 WWDC stubs discarded). Rich algorithmic primary source from Apple ML Research article (`machinelearning.apple.com/research/roomplan`).

**New page `apple-roomplan`** covers: (1) what RoomPlan produces — parametric `CapturedRoom` struct with typed 2D `Surface` and 3D `Object` cuboids, USD export, not a point cloud; (2) Room Layout Estimation algorithm — two-stage: bird's-eye U-Net on semantic+Z-sliced point cloud (512×512×12, 3 cm×30 cm voxels, supports up to 15 m×15 m rooms) producing corner+edge maps → line proposals → line-verification → lifted to 3D; orthographic EfficientNet for door/window detection on per-wall projections; (3) 3DOD pipeline — local 48×32×24 frustum 3D Conv U-Net (15 cm voxels, 35 features/voxel) + global scene detector for large objects + box fusion with wall snapping; (4) 16-category furniture taxonomy with category breakdown; (5) all three NNs run on Apple Neural Engine (ANE), quantized/pruned to avoid thermal throttling in 5-minute scans; (6) stated accuracy: 95%/95% walls, 90%/90% doors, 91%/90% 3DOD at 30% IoU; practical accuracy ±5 cm per wall, 37 cm accumulated on 6.45 m room; (7) known limitations: no ceiling, 16 cm wall thickness, rectangular simplification, mirror/glass failures, single floor; (8) iOS 17 MultiRoom — StructureBuilder API for merging multiple rooms, ARWorldMap relocalization or continuous ARSession for shared coordinate frame; (9) Vision Pro uses mesh+plane detection (not RoomPlan — RoomPlan not available on visionOS); (10) §8 transfer lessons for our passive-stereo + 2D LiDAR design — bird's-eye line detection ≈ SLAM Toolbox analogy, object bounding box schema identical to our object library, wall-snap fusion useful, vertical dimension gap (2D LiDAR = one horizontal slice), production ceiling quantified.

Sources: Apple ML Research article, WWDC22 session 10127 transcript, WWDC23 session 10192 transcript, it-jim practitioner review, it-jim API guide, Apple developer overview.

---

## [2026-06-02] synthesis | passive-stereo-robustification

Librarian synthesis pass (dispatched from `drone-prototype`). The prototyper + human worked out, over the last few sessions, a full strategy for making **passive stereo robust enough for indoor SLAM without expensive LiDAR** — the consumer-product cost tenet. The knowledge was scattered across `visual-inertial-slam`, `indoor-cluttered-slam`, `learned-slam`, `close-range-depth-sensors` and the prototyper's personal log; consolidated into one cited page `passive-stereo-robustification`.

Covers: the honest hard limit (passive stereo starves on white walls / glass / glossy floors; no vision-only SLAM clears it without help; IMU bridging < 1 s [src: indoor-cluttered-slam 07-arxiv-2306-08522 / 11-amazon-indoor-mapping]); the consumer-cost tenet (stereo OR cheap LiDAR, never MID360-class); the consumer-cost-ranked robustifier ladder (cheap IMU→VIO; dense RGB-D vs sparse VO; learned front-end SuperPoint/LightGlue/DPV-SLAM; robustness engineering — health-tracker + DBoW2 relocalization; active-assisted stereo); active stereo explained (a "dumb" uncalibrated projector adds artificial texture, SGBM unchanged because only the two cameras' geometry matters → projector can be independent/fixed for a prototype, with shadow + range² coverage caveat, vs a co-mounted fingernail VCSEL+DOE IR module <1 W for a product); the pattern-as-calibration-**validator** insight (can't replace the checkerboard, but dense L↔R matches give an epipolar/rectification check + a flat-wall planarity test cf. RealSense "Tare" → candidate to retire parked **P-002**); and the hardware ladder with prices (visible pico/star-laser ~$12–70 → IR-convert the SVPRO + IR DOE → **Arducam OV9281 NoIR global-shutter stereo ~$26/cam + IR DOE $20–50 ≈ $80–150** → **D435i $334** turnkey active IR stereo + BMI055 IMU + factory cal; skip OAK-D Pro $399 — *more* than the D435i). Step-4 implication: run baseline passive stereo first, characterize the failure regime, then aim the projector at exactly that.

Cross-links added into `slam`, `indoor-cluttered-slam`, `home-tidy-drone-prototype` Related sections; index/revisions updated. Sources: `drone-prototype` `docs/prototyper-log.md` (2026-06-01 19:00 / 19:30, 2026-06-02), `docs/00-framing.md` Product tenet, plus the four source wiki pages (each carrying its own raw citations).

---

## [2026-06-01] research | cheap-lidar-pricing-guide

Researched cheap LiDAR options for a commercially viable indoor tidy bot. Captured 9 sources (Unitree L1 official shop, Robotika.cz independent L1 review, kaiaai 2D LiDAR list, budget comparison guides, Hesai JT16 CES 2025 launch, RPLIDAR C1 specs, OpenELAB 3D comparison). Key finding: Unitree L1 confirmed at $249 USD (3D, 360°×90°, explicitly targets sweeping robots) — price dropped ~$100 since late-2024 reviews. New page `cheap-lidar-pricing-guide` created with full pricing tier table and commercial viability thresholds. Updated `home-tidy-drone-prototype` to recommend L1 for Phase-1 ground robot; MID-360 remains Phase-2 UAV target. Updated `2d-lidar-slam` with retail pricing for budget 2D options. Added vacuum LDS salvage (~$16) to `robot-vacuum-navigation`. YouTube vacuum-LDS tutorial skipped (429 rate limit × 2).

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

## [2026-05-19] weekly-brief | empty-run validation

Validation run of the tuned `reference-sources.md` **"Brief emphasis & exclusions"** block (added after the 2026-05-17 brief drifted toward defence-/market-news headlines). 2-day gap since last run; trend scan honoured the tuned rules and correctly returned **zero new in-window technical-research candidates**, recommending an empty run rather than padding with FCC/DJI / Canada-onshoring / product news — the exact failure mode the tuning was meant to close. Short 3-line email + Telegram sent unattended; the new `settings.local.json` allow-rules (send_email, render_brief_html, source remote_workstation/.env, telegram sendMessage curl) cleared the classifier with no prompts — settings fix validated end-to-end. No captures, no wiki changes, no commit per empty-run policy.

## [2026-05-20] research+ingest | canadian-onshoring

Topic: Canadian drone manufacturing & onshoring of drone production. 13 sources captured (gov primaries — ISED Defence Industrial Strategy, NRC Drone Innovation Hub $105M, NRC IRAP DI Assist $241M, Transport Canada Drone Zone, PrairiesCan Alberta backgrounder; analyst — NAV CANADA RPAS market study; regulatory counsel — Gowling; company — Volatus Mirabel PR, InDro committee submission, Draganfly facility expansion; trade-press — two BetaKit pieces incl. sponsored Ogden feature, The Walrus long-form). Audit clean (0 issues across URL captures). 2 new pages on recommended-defaults: `canadian-drone-onshoring` (overview: state of capacity, 2026 funding-wave table, market baseline with NAV CANADA self-interest caveat co-located, demand/regulatory readiness, drivers, consolidated gaps section) and `drone-manufacturing-supply-chain` (assembler-vs-OEM, IP-erosion pattern incl. Aeryon→FLIR $265M independently corroborated, three-C framework, software-over-hardware thesis, named-company datapoints table with corroboration tags, component-level gap audit). Consumer-scope filter applied throughout — defence-procurement politics excluded, dual-use/economic substance retained. Caveats baked into the pages: BetaKit/Ogden sponsored-feature flag, Volatus claimed/unverified, NAV CANADA self-interest, "<20 manufacturers" framing-not-fact. Honest finding: heavy 2026 federal money is arriving but the structural gaps (assembler economy, component dependency, IP erosion, procurement unreliability) are deep and policy instruments are announced-not-proven. 29 content pages, all cross-links resolve.

No new kit learnings this run.

## [2026-05-23] query + 6× research+ingest | home-tidy-drone prototype

`/query` produced [[home-tidy-drone-prototype]] — a use-case feasibility/proposal page (requirements R1–R5 → wiki-sourced capability map → gap analysis → 6 research assignments → beyond-wiki minimal-prototype buy list with Canadian pricing: nano/bench ~$3.0–3.4k CAD, payload+LiDAR ~$8.9–9.5k; RealSense T265 discontinued → ZED Mini). Then the user ran all 6 research assignments in parallel (option B — full capture): 7 agents (1 pricing + 6 research). 61 sources captured across 6 topic dirs (arXiv bulk + vendor/lab/gov/github; paywalled AIAA/tandfonline/ACM/USPTO-image failed gracefully; 2 thin bot-walled captures dropped). Per-topic page-writer subagents (one each, reading their own raw files to keep main context lean) produced 6 new pages: `onboard-grasp-perception` (the central mocap-free perception blocker — aerial OVD ~28% F1), `precision-docking-recharging`, `indoor-cluttered-slam`, `voice-intent-task` (the wiki's former weakest area), `safe-indoor-flight`, `semantic-object-memory`. All consumer-scoped; all cross-linked to the prototype proposal (assignments now answered). Wiki now 36 content pages, all links resolve.

No new kit learnings this run (capture/audit/ingest flow worked; paywall failures expected).

## [2026-05-23] lint | health check

Full lint of 36 content pages → `wiki/lint-reports/2026-05-23.md`. Clean on orphans, broken links, format. Key findings: (1) `faa-part-108-bvlos` is stale — the ~Feb 2026 final-rule deadline passed; page lags the watchlist; (2) **no use-case application-layer pages** (inspection/delivery/agriculture/mapping) — the biggest structural gap vs the wiki's goal; (3) `cooperative-aerial-manipulation` missing evidence-strength tags; (4) 5 missing cross-references; (5) manufacturing/origin (NDAA/Blue-UAS) tags missing on skydio/anduril/Canadian-OEM pages; (6) skydio/Draganfly company-status drift needs re-verification. `raw/` empty → capture-fidelity N/A, no un-ingested sources. Trend radar: VLA-aerial-manipulation crystallising (pre-commercial), onboard open-vocab perception = binding blocker, DAA MOPS gap = regulatory bottleneck, use-case layer absent, battery/LiDAR-cost roadmaps absent. Fixes awaiting user direction. Kit learning logged.

## [2026-05-23] lint fixes + deferred-4 research ingest

Applied the lint safe-fix set (11 pages: 5 cross-refs, evidence tags on cooperative-aerial-manipulation, FAA Part-108 deadline-slipped note, last-verified headers on Canadian pages, country-of-origin tags on Skydio/Anduril, watchlist link normalize). Then ran the 4 deferred research items (option B, full): 4 parallel research agents → ~40 sources captured (paywalled/bot-walled CBC + Skydio-consumer-exit TechCrunch + DroneDJ Wing-guide failed; SEC 40-F returned a bot-block page). 7 new pages: the **use-case application layer** (lint's #1 gap) — `drone-inspection-use-case`, `drone-delivery-use-case`, `drone-agriculture-use-case`, `drone-mapping-surveying-use-case` + `drone-commercial-verticals` index; `bvlos-regulation` (US/Canada/EU — finding: **Canada operationally ahead**, in-effect 4 Nov 2025; EASA SORA 2.5; FAA Part 108 slipped); `drone-battery-energy` (Amprius 450 Wh/kg, hydrogen BVLOS, hybrid; propulsion-futures contest). Corrected `skydio-autonomy-stack` (enterprise/defence pivot, X10D Blue-UAS, SkyForge $3.5B — "consumer existence proof" framing retired) and `drone-manufacturing-supply-chain` (Draganfly going-concern — SEC source bot-blocked, flagged for re-verification). Wiki now 44 content pages, all links resolve.

Open follow-ups: Draganfly SEC 40-F financials need a non-bot-walled capture (EDGAR/SEDAR+); Wing-specific + Skydio-consumer-exit sources failed (JS/consent walls). No new kit learnings.

## [2026-05-17] research+ingest | multimodal-locomotion

Topic: mixed-mode robots (drone + wheels/legs/arm; air/land/water) for effectual real-world action. 11 captured (Kovac air-water Science Robotics → Spiral SPA returned nothing, manual-download follow-up; M4 record-page re-captured as full PDF via Caltech direct link). 10 sources → 3 pages on the user's "proceed with recommendations": `multimodal-locomotion` (overview, taxonomy, energy rationale, consumer verdict), `air-ground-hybrids` (energy spine + hard-numbers table + AirCrab/M4 multimodal-manipulation section + FSTAR/LEONARDO journalism), `air-water-robots` (honest research-curiosity framing). Enriched `drone-power-budget` with a "Multimodal locomotion as an endurance lever" section (single-passive-wheel 77%, Roller-Quadrotor 41×, Tilt-Ropter 92.8%) + cross-links — the synthesis answer to "what beats the endurance ceiling": rolling-instead-of-hovering and perching, not battery chemistry alone. Answer to the user: yes, AirCrab (arm+active-wheel) and M4 (8-mode appendage-repurposing) exist; consumer-blocked by the same dual-mode-weight + onboard-perception/autonomy gaps as aerial-manipulation. LEONARDO has no primary in-corpus (journalism only) — flagged. Wiki now 24 content pages, all cross-links resolve.

## [2026-05-17] weekly-brief | first run

First `/weekly-brief` sweep (setup approved this session; session backlog committed separately as 8406936 first so the weekly commit is a clean delta). Trend scan (window 7d, ~13 sources): theme = onboard-compute convergence + peak US regulatory pressure on Chinese hardware (FCC/DJI comment deadline 11 May) + Canada onshoring consolidation + a crystallising VLA-for-aerial-manipulation subfield. 3 captures (quality over the 5-cap): Dream-to-Fly (ETH RPG, ICRA 2026 — pixel→control RL, added as Position-B to the open lidar-vs-vision conflict, with a real-camera-gap asterisk), AIR-VLA + DroneVLA (the VLA-aerial-manipulation pair → 2 paper pages + an "emerging subfield" note on `aerial-manipulation`, no speculative new cluster page per policy). VIO-no-LiDAR resurfaced but already in-wiki (`visual-inertial-slam`) — not re-captured. Part 108: no final rule in the window (EO-mandated ~Feb/Mar 2026 target appears slipped). Overflow → watchlist. 27 content pages, all links resolve.

## [2026-05-24] research+ingest | Phase-1 build-support + nav precedents (9 topics)

Ran the 9 follow-up investigations seeded by the revised Phase-1 prototype plan (7 build-support + 2 precedent studies the user added: how robot vacuums navigate a home; how Amazon warehouse robots traverse a facility). ~100 sources captured across 9 topic dirs (mostly official docs — ardupilot.org / docs.px4.io / docs.ros.org — plus GitHub repos, arXiv, IEEE Spectrum, amazon.science). 3 supplementary captures failed and were dropped (Printables 3D-model JS page, FoxTech vendor page, VentureBeat consent wall). 9 page-writer subagents (one per topic) → 9 new pages:
- **Build-reference (7):** `slam-fc-integration` (external pose → EKF3/EKF2 via MAVROS vision_pose; frames; EK3_SRC; divergence), `fast-lio-mid360-orin` (FAST-LIO2 + MID360 on Orin; the g-vs-m/s² IMU trap; CustomMsg xfer_format; ~5 ms/scan on ARM), `indoor-obstacle-avoidance` (FC-native BendyRuler/Dijkstra + companion EGO-Planner/FASTER), `drone-comms-wifi` (DDS multicast-over-WiFi failure → Discovery Server / Zenoh; MAVLink-over-UDP routing), `prop-guard-failsafe` (build-level companion to safe-indoor-flight; FAA OOP Cat-1 no-laceration clause is the binding constraint sub-250 g; every failsafe "return" degrades to land-in-place without indoor position), `gps-denied-hover-land` (optical-flow Loiter + AprilTag/ArUco precland — the fiducials-first evidence base), `payload-budget` (component masses + payload→endurance trade on X500 V2; MID360 mass sourced from wiki since spec page omitted it).
- **Precedent studies (2):** `robot-vacuum-navigation` (LDS-SLAM / VSLAM / ToF; vacuums prove cheap 2D LiDAR + dead-reckoning is enough — a drone lacks wheel odometry so leans on optical-flow/LIO/fiducials), `warehouse-robot-navigation` (Kiva floor-fiducial grid + central planner at 100,000s scale beats per-robot autonomy; Proteus/Sequoia moving beyond the caged grid).

**Cross-cutting takeaway folded into the Phase-1 plan: fiducials-first.** Both precedents say don't start with full SLAM. Revised `home-tidy-drone-prototype` Phase-1: re-ordered milestones so V1 = AprilTag/ArUco + optical-flow hover (proves flight+EKF+safety loop on a known-good position source), MID360+FAST-LIO2 marker-free traversal demoted to milestone 6; wired the follow-up-research bullets to the 9 new pages. Capture-quality flags (no fabrication): ArduPilot issue #27729 body wasn't in the captured set (page carries it as an unverified pointer); the warehouse `amazon-mapf-exec` capture returned an Amazon Ads job posting, so MAPF substance was sourced from arXiv 2408.14527 (NAVER LABS) and the bad capture flagged in-page. Wiki now 53 content pages; 0 real broken links (basename resolution); normalized 5 new pages from `[[conflicts/lidar-vs-vision-autonomy]]` to the bare `[[lidar-vs-vision-autonomy]]` form the rest of the wiki uses.

## [2026-05-25] research+ingest | learned-slam (AI SLAM methods from the reading list)

Ran the capture + ingest of the SLAM_reading_list "recommended ingests" shortlist. 11 sources attempted, 10 captured (IS-CAT is MDPI-hosted → bot-walled, dropped to manual-download follow-up). One synthesis-writer subagent read all 10 and produced `learned-slam` — the AI/learning-based methods layer of the SLAM cluster, complementing [[slam]] (concept hub), [[fast-lio-mid360-orin]] (classical-LIO build), and [[indoor-cluttered-slam]] (the indoor problem):
- **Learned LiDAR-inertial odometry:** DFLIOM (2410.02961, learned registration features, ~57% memory cut), KN-LIO (2501.04263, neural-SDF-coupled).
- **Learned visual/visual-inertial SLAM:** DPV-SLAM / DPVO (2408.01654, ECCV 2024).
- **Edge 3DGS-SLAM:** GS-LIVO (2501.08672, T-RO 2025) — the standout.
- **Monocular metric-depth foundation models:** Depth Anything V2 (2406.09414) + the Jetson-Orin TensorRT deployment.
- **Learned place recognition / loop closure:** iBTC (HKU-MARS).
- **Landscape:** Tosi NeRF/3DGS-SLAM survey (2402.13255).

**Wiki correction (the load-bearing outcome):** our pages claimed 3DGS-SLAM is desktop-GPU-only / "none demonstrated on drone-class compute." GS-LIVO refutes this — *demoed* real-time Gaussian-Splatting LiDAR-inertial-visual SLAM on a Jetson Orin NX 16 GB at 48.3 ms/frame (~20 Hz), 1.2–1.5 GB vs 17–21 GB for desktop GS-SLAM (caveat: ground/handheld rig, not in flight). Corrected the claim on `slam` and `indoor-cluttered-slam`, citing [[learned-slam]]. Updated SLAM_reading_list.md to mark the shortlist ingested. Wiki now 54 content pages; link check clean. raw/research/learned-slam captures had 245 cosmetic pymupdf image-ref warnings (known kit bug, load-bearing audit clean).

## [2026-05-28] research+ingest | close-range depth sensors (3 papers, 1 failed datasheet)

Research question: close-range, narrow-FOV depth sensors suited for drone manipulation / grasp pose estimation at 0.5–2 m, where the Livox MID360 gives too-sparse returns on small objects.

Fidelity audit: clean (0 issues across 3 captures). VL53L5CX datasheet capture failed (ST.com timeout) — noted in Source section, partial specs reconstructed from cross-citations.

3 papers ingested:
1. Sifferman et al. (arXiv 2509.16122, RA-L 2025) — arm-mounted AMS TMF8820 miniature ToF for proximity detection; self-detection problem solved via transient-histogram probabilistic model; 2.08 cm distance error, 78.9% TPR; 3.5 Hz frame rate limited by I²C bandwidth.
2. Rustler et al. (arXiv 2501.07421, IEEE Access 2025) — D435 vs D455 vs ZED 2 vs OAK-D Pro; D435 best for complex objects at <100 cm (the manipulation range); D455 worse than D435 on curved objects at close range but better at flat-surface/longer-range nav; ZED 2 overall best but requires CUDA GPU (incompatible with drone SWaP); OAK-D Pro produces quantised depth layers unsuitable for complex shapes.
3. Cai et al. (arXiv 2412.15040, ETH Zurich, IEEE 2024) — PMD Flexx2 ToF noise model (axial KL div 0.015 nats — excellent Gaussian fit); 13 g, 570–680 mW, 0.1–7 m range, 60 fps; developed for quadruped RL sim-to-real; applicable to drone manipulation.

New page: `close-range-depth-sensors.md`. index.md updated (row inserted after lidar-for-uav-autonomy). revisions.md updated.

Mild conflict surfaced with `home-tidy-drone-prototype`: D455 was chosen as the budget depth camera, but D455 has 0.6 m minimum range and is worse than D435 on complex curved household objects — the core manipulation target. Flagged as open question in the new page (dual-camera vs. D455 + miniature ToF).

## [2026-05-25] weekly-brief | thin technical week, 1 capture (MIGHTY)

2026-05-28. Architecture design session. User proposed 8 subsystems for the full home-tidy drone cognitive stack; recorded, critiqued, extended. New page: system-architecture.md. Added 5 missing components: perception pipeline, safety arbiter, exploration/map-init mode, task sequencer, user interface. Proposed 6-phase roadmap (Phase 0 = current prototype plan; Phases 1–5 build up to open-vocabulary autonomous tidying). Called out 6 critical challenges in priority order; C1 (onboard manipulation perception without mocap) identified as the single likeliest architectural pivot-point. index.md and revisions.md updated.

Manual weekly sweep (window 7d, ~2026-05-18→05-25). Trend scan across arXiv cs.RO + 8 named groups (RPG, MAVLab, CAST, GRASP, LIS, Imperial, ASL, UTIAS) + IEEE Spectrum + DroneDJ/sUAS News: a sparse week — most "trending" aerial-robotics items were publicity waves for out-of-window preprints (WPI ultrasound-nav Science Robotics Mar; RPG event-radiance-field Feb; EvSLAM Apr; CLAK Mar). Only one inside-window technical candidate cleared the domain-fit + signal bar.

1 captured + ingested → `mighty` (arXiv 2511.10822, MIT-ACL + UPenn): Hermite-spline UAV trajectory planner doing joint spatiotemporal optimization; −9.3% compute / −13.1% travel time vs MINCO, 100% sim success, 6.7 m/s onboard on a NUC 13 with Livox MID360 + DLIO; code released (mit-acl/mighty). Conflict call: linked to [[lidar-vs-vision-autonomy]] but NOT logged as Position-A (LiDAR-necessary) evidence — MIGHTY merely *uses* LiDAR and its own benchmark runs EGO-Swarm2 on a depth camera, so it's a LiDAR-used datapoint, not support for LiDAR necessity. Notably runs on our exact build sensor (MID360).

3 watchlist additions (Autonomy & perception): EvSLAM (event-VO/VIO high-speed benchmark + challenge, conflict-relevant), Antigravity A1 (360° vision-only avoidance shipping in a consumer drone), GDU S400E (vision+mmWave-radar fusion, "fuse don't choose" datapoint). Wiki now 55 content pages. Email + Telegram dispatched; changes committed + pushed per the topic-branch contract.

## [2026-05-29] research+ingest | tactile-manipulation (8 papers)

8 captured papers on tactile robotic manipulation ingested → new `tactile-manipulation.md` page.

Papers:
1. Lepora, "Tactile Robotics: Past and Future" (IJRR 2025 survey) — 45-year historical arc, sensor class taxonomy, commercial landscape
2. Donato et al., "Sensorimotor Control Strategies for Tactile Robotics" (2025 review) — slip detection, tactile servoing, friction-informed control architectures
3. Suresh et al., "NeuralFeels" (Science Robotics 2024) — visuotactile SLAM on Allegro+DIGIT; 81% F-score, 4.7 mm drift, 94% improvement under occlusion
4. Li et al., "ManiSkill-ViTac 2025" (ICRA 2025 workshop) — first standardised visuotactile benchmark; FEM-based simulation; dual GelSight Mini platform
5. Helmut et al., "FARM" (IEEE preprint 2025) — diffusion policy + force distribution action space; 100% screw-tightening (vs 0% vision-only)
6. Akinola et al., "TacSL" (NVIDIA, IEEE T-RO 2025) — GPU-parallelised tactile sim (200×+ speedup); 91.4% zero-shot peg placement on real Franka
7. Kasolowsky & Bäuml, "Fine Manipulation with Tactile Skin" (IROS 2024) — 4×4 taxel skin; <1 mm marble tracking vs 5 mm without tactile; zero-shot DLR-Hand II
8. ByteDance Seed, "Closing the Reality Gap" (Dec 2025) — 12-DoF xHand; force-adaptive grasping of unknown objects; 25.1 consecutive in-hand rotations with tactile vs 1.1 without

Key synthesis finding: land-then-grasp removes the aerial-manipulation barrier — all these results apply directly once the drone is on the ground. GelSight Mini (~25 g) is payload-compatible with a lightweight drone gripper. Gel lifespan under drone vibration is an open question.

No conflicts with existing pages. Confirms and extends the [[onboard-grasp-perception]] finding that vision-only is the central blocker.

## [2026-05-29] research+ingest | ground-aerial-robots

Read 6 captured papers on dual-mode ground-aerial robots and wrote new `wiki/ground-aerial-robots.md`. Also updated `wiki/air-ground-hybrids.md` (added pointer, upgraded M4 entry to primary paper citation).

**Sources processed:**
1. arXiv 2503.00609 (Caltech, Mar 2025) — ATMO, 5.5 kg, mid-air morphing via single worm-gear actuator, MPC transition controller, ground-effect aerodynamics characterised, slope landing at 25°
2. arXiv 2505.13836 (UC Berkeley, May 2025) — Duawlfin, ~800 g, unified actuation via one-way bearings + differential drivetrain, 30× ground/flight energy ratio at 1 m/s, 0.1 s mode switch, 30° slope climbing
3. arXiv 2303.05075 (NTU, IROS 2023) — DoubleBee, 2.78 kg, bicopter+2 active wheels, decoupled control scheme (thrust controls pitch, wheels control translation), lowest energy in bicopter class
4. arXiv 2603.26687 (CMU+NTU, Mar 2026) — Energy-aware RL on DoubleBee: 4× energy reduction in sim vs propellers-only; 38% average power reduction on hardware 8 cm gap-climbing (3/5 success); emergent thrust-assisted driving
5. PMC10300070 / Nature Comms 2023 (Caltech) — M4 MorphoBot primary paper (reCAPTCHA blocked capture; data from thesis source)
6. arXiv 2308.13972 (Northeastern, Aug 2023) — M4 autonomy: traversability CNN + modified 3D A* path planner; 60:1 aerial-to-ground energy ratio assumed; 92% energy reduction vs pure aerial in maze scenario (simulation); CNN too slow for Jetson real-time (excluded from scope)

**Key findings:**
- 60:1 aerial-to-ground energy cost ratio (M4 model assumptions) — the strongest data point for ground-primary architecture
- Real stair-climbing on hardware: 8 cm step, 3/5 trials, 38% power reduction vs rule-based controller
- Full staircase autonomy: simulation-only, no hardware demonstration
- All platforms mocap-dependent for state estimation; no onboard autonomy at mode-switch time
- Duawlfin at 800 g is the lightest viable platform; 30× energy ratio is empirically measured (not modelled)
- RL policy (CMU) is the only system where "burst flight" emerges naturally from optimisation rather than discrete mode switching — closest to the desired architecture

**Conflicts with existing wiki:** None. Complements [[air-ground-hybrids]] without contradicting it. M4 entry in air-ground-hybrids upgraded from journalism source to primary paper citation.

## [2026-05-29] ingest | Home Tidying Robots (5 sources)

5 papers ingested. New page: `wiki/home-tidying-robots.md`.

**Sources:**
- TidyBot (arXiv 2305.05658, Stanford/Princeton/Google 2023) — LLM personalisation, 85% real-world success
- TidyBot++ (arXiv 2412.10447, Princeton/Stanford Dec 2024) — open-source $5–6k holonomic base, 60–100% on 6 real tasks
- WRC2020 Partner Robot (arXiv 2207.10106, U. Tokyo 2022) — competition benchmark, 65% grasp, 56 s/object
- ManiSkill-HAB (arXiv 2412.13211, UCSD/Hillbot ICLR 2025) — GPU sim benchmark with realistic grasping
- LLM-Personalize (arXiv 2404.14285, Microsoft/Edinburgh 2024) — ReST fine-tuning, >30% improvement in sim
- 1X NEO (FAILED CAPTURE — JS-wall, only marketing fragment; noted as commercial humanoid)

**Key findings:**
- Nothing is commercially shipping for general home tidying
- TidyBot's few-shot LLM summarisation (91.2% benchmark, 85% real-robot) is state-of-the-art for personalised tidying — directly applicable to our COMMAND CENTER concept
- Best real-robot ground manipulator achieves 65–100% depending on task complexity; our aerial grasping is the main gap
- All existing systems are ground-only; aerial tidying literature is absent
- TidyBot++ uses Kinova Gen3 arm (Canadian supply-chain note)

**Conflicts with existing wiki:** None.

## [2026-05-29] research+ingest | Learned Point Cloud Registration (5 sources)

5 papers ingested. New page: `wiki/learned-point-cloud-registration.md`.

**Sources:**
- arXiv 2404.13830 (Zhang et al. Apr 2024/Feb 2025) — comprehensive DL-PCR survey, 100+ methods, unified 3DMatch/KITTI benchmarks
- arXiv 2409.10824 (Yang et al. Sep 2024) — RobustLOL: 18 corruption types × 5 LiDAR odometry systems; DL degrades to 80% error
- arXiv 2603.16273 (Mar 2026) — GenZ-LIO: adaptive classical LIO; 0% divergence on 42 sequences across 10 datasets
- arXiv 1905.03304 (Wang & Solomon ICCV 2019) — Deep Closest Point: foundational DL registration (RMSE(R) 1.1° on ModelNet40)
- arXiv 2507.17531 (Dannaoui et al. Jul 2025) — ICP in evolving environments; point-to-plane consistently outperforms point-to-point; both fail at symmetric corridors and featureless ground

**Key findings:**
- DL-PCR achieves impressive benchmarks (PARE-Net 94.2% on 3DMatch) but no method has deployed on embedded UAV hardware at scan rate
- Learning-based odometry systems are *more* sensitive to real-world corruptions than classical ICP: degradation up to 80% RPEtrans under 18 corruption types
- The generalization gap is structural: training on ModelNet40 or 3DMatch does not transfer to outdoor LiDAR; category-split DCP-v2 RMSE(R) degrades 2.8×
- GenZ-LIO (Mar 2026) closes key deployment gaps through adaptive voxelization + hybrid error metric — without learned registration
- Fine-tuning DeLORA on corrupted data recovers 35.8% of degradation — viable as a deployment engineering step once corruption profile is known

**Conflicts with existing wiki:** None. Consistent with learned-slam.md framing (classical LIO dominates current deployment). Extends fast-lio-mid360-orin.md by explaining *why* FAST-LIO2 is classical (ICP-family) and what the alternatives look like.

## [2026-05-29] research+ingest | TidyBot deep dive

Full deep-dive page on TidyBot v1 and TidyBot++ from 12 captured source files. Created `wiki/tidybot-deep-dive.md`.

**Sources used:**
- arXiv 2305.05658 — TidyBot v1 paper (*Autonomous Robots* 2023)
- arXiv 2412.10447 — TidyBot++ paper (CoRL 2024)
- tidybot.cs.princeton.edu project page
- tidybot2.github.io project page
- Both GitHub READMEs (v1 + v++)
- IROS 2023 camera-ready PDF
- Kinova Gen3 product page (JS-walled — no parseable specs)
- UFACTORY xArm page (specs recovered: $5,299–5,494, 5 kg payload, 700 mm reach)
- UFACTORY Lite 6 page (specs recovered: $2,999, 0.6 kg payload, 440 mm reach)
- Hello Robot Stretch 3 (404 — unavailable)
- arXiv 2507.15693 (Forte low-cost arm paper) — **source 09 mislabelled** as "arm comparison paper"; is actually a novel 3D-printed arm design. Contains a reference table with Kinova Gen3 Lite as a datapoint but is not a comparison of the arms in the table. Flagged in page and revisions.

**Key findings per source:**
- v1 paper: complete pipeline docs, 85% real-world result with per-component breakdown, LLM comparison table, explicit limitation of hard-coded receptacles + top-down grasps only
- v++ paper: holonomic vs differential controlled experiment (9/10 vs 4/10), full hardware specs table vs competitors, 50-demo sufficiency finding, external GPU architectural constraint stated explicitly
- v++ README: ZMQ port 5555, RTX 4080 Laptop 115 ms inference latency, PolicyWrapper latency-hiding mechanism, real robot architecture diagram
- v++ project page: confirms 6 officially supported arms (Kinova, Franka, ARX5, xArm, UR5, ViperX)

**Conflicts with existing wiki:** None. home-tidying-robots.md covers the landscape; this page deepens TidyBot specifically. No factual conflicts found.

**Open questions for user:**
1. The arm-comparison source (09-10-arm-comparison-paper.md) is mislabelled — it's the Forte arm paper, not the comparative review originally intended. Was there a specific arm-comparison paper you wanted captured? The pre-extracted data in the brief included arm specs (Franka ~$25k, UR5e ~$35k, Stretch ~$25k) that I cannot directly trace to this source — these appear to be pre-extracted estimates in the brief itself rather than data confirmed in any source file.
2. Phase-2 hardware recommendation (§7) assumes a ground-first approach. If the project pivots to aerial-first (drone as primary actor, no ground arm), the TidyBot++ base recommendation is moot. Worth confirming direction before acting on it.

## [2026-06-01] prototype-feedback | SVPRO measured characterization

First hands-on validation of the in-hand SVPRO stereo camera folded back from the `drone-prototype` repo (Phase-1 prototype portfolio, Session 1, librarian close-out). Updated `wiki/home-tidy-drone-prototype.md` only — added a "SVPRO characterization (measured)" subsection under *What can start now*, and corrected the spec-sheet "60FPS" line to point at measured reality.

**Source (not web — a sibling prototype repo):** `drone-prototype/docs/prototype-diary.md` (2026-06-01 entries), `drone-prototype/docs/parked.md` (P-001 USB flakiness, P-002 calibration tightness). Code-reviewer re-ran the pipeline and confirmed the numbers reproduce from committed frames.

**Measured facts captured (maturity = demonstrated at toy scale):**
- Enumerates as `3D USB Camera` `32e4:0035`; delivers true 3840×1080 side-by-side MJPG **@30 fps over USB 2.0** — not the spec-sheet 60 fps (USB 2.0 bandwidth ceiling on the working data path).
- Mounted upside-down; a single full-frame 180° rotation un-inverts and correctly swaps L/R for a side-by-side rig (handle once, then split at midpoint).
- Stereo **baseline ≈ 57.8 mm**; calibration to prototype grade (mono RMS ≈0.8 px, stereo RMS ≈1.9–2.45 px, 5-coeff model; `CALIB_RATIONAL_MODEL` diverges without more edge poses). Metric scale cross-checked within +3.3–3.7 % of tape.
- Passive-stereo indoor reality: ~48 % dense-depth coverage; **no depth on blank walls/ceiling/bright windows**; **spurious far depth on textureless far surfaces** (a wall reads ~19 m — false "clear ahead", safety-relevant).
- USB data-path gotcha (→ P-001): USB-A cable + USB-C-only laptop = silently non-data via a naive adapter; only a **powered USB-C dock** enumerated it, and the link dropped under load. Production needs a pinned, watchdogged USB path.

**Conflicts with existing wiki:** the prior spec-sheet "1080P 60FPS" line overstated achievable frame rate on USB 2.0 — corrected in place to point at the measured 30 fps. No other conflicts; this is the first empirical data on a sensor previously described only from its spec sheet.

## [2026-06-04] research | room-segmentation-floor-plan

Research run on room segmentation and doorway detection from 2D occupancy grids.

**Sources captured (7 new, in raw/research/room-segmentation/):**
- `05-05-rose2-room-seg.md` — arXiv 2203.03519 (IEEE RAL 2022), ROSE², Luperto et al. Politecnico di Milano / Aalto. Geometry-only DFT-based clutter removal + wall detection; benchmark: 73.3 IoU vs Voronoi 28.65 on cluttered maps.
- `06-06-selros-llm-room-seg.md` — arXiv 2403.12920 (2024), SeLRoS, Kim & Min Purdue. VRF geometric seg + Detic object detection + LLM hierarchical query; over-segmentation correction; 30 ProcTHOR environments.
- `07-07-semantic-regions-no-obj-recog.md` — arXiv 2403.07076 (ICRA 2024), Bigazzi et al. Stanford ASL. Finetuned CLIP region classifier; appearance-based semantic mapping without object detection; HM3D/Matterport sim.
- `08-08-rethinking-semantic-classification.md` — arXiv 2603.08512 (2026), Mozos et al. Orebro / Carlos III. VGG16 + object histogram confusion-based sub-room labelling; object search task improvement; 3-page workshop paper, real environments.
- `09-09-topology-visual-room-seg-icra2025.md` — ICRA 2025, Bao et al. CUHK Shenzhen / AIRS. Active room segmentation: ray-casting door candidates + DNN visual refinement + within-room frontier + topology map; +10.2% precision vs Voronoi on Gibson.
- `10-10-roborock-room-seg-patent.md` — US patent US20220051459A1. Roborock (claimed): NN pixel classification (room-inside/outside/type) + flood-fill propagation + camera-based door/window/object detection for semantic labels. *(patent — claims, not confirmed deployed reality)*
- `11-11-door-status-detection.md` — arXiv 2203.03959 (2022), Antonazzi et al. University of Milan. General DNN trained on robot-viewpoint simulation + environment-specific fine-tuning ("qualification"); open/closed detection; same group as ROSE².

**Key findings:**
- ROSE² is the drop-in answer for the prototype: ROS nodes, no training, any SLAM backend. 73.3 IoU on real cluttered office maps. LiDAR-only (2D occupancy grid input only).
- All semantic labelling methods require a camera pass. There is no published method for assigning kitchen/bedroom labels from a 2D occupancy grid without visual observation.
- Doorway detection: geometry-only (Voronoi critical-points) gives candidates with high false-positive rate from furniture. Visual refinement (DNN on RGB) reduces false positives but requires camera.
- Shipping products (Roborock patent) use NN + flood-fill + camera — confirming camera is necessary in practice. Manual user labelling remains dominant for room names in all shipping consumer products.
- Open-floor-plan failure is shared across research and shipping: no wall = no segmentation boundary. Approaches: (a) user-drawn dividers, (b) CLIP appearance classifier (Stanford ASL), (c) object-location routing without hard boundaries.
- SeLRoS LLM pipeline (simulation only) shows the LLM can use architectural priors + object lists to correct over-segmentation and label rooms. Real-world deployment not demonstrated.

**Conflicts with existing wiki:** None. The wiki's [[scene-graph-world-model]] covers Hydra's room layer and HOV-SG's Watershed BEV segmentation, both of which require 3D mesh input — heavier than 2D grid. This new page fills the 2D-only gap those pages leave.

**Open questions for user:** None requiring ruling. ROSE² is clearly the right first step for the prototype. The semantic labelling question is "camera sweep then LLM" — consistent with the existing [[map-then-navigate]] pattern.

## 2026-06-04 — research+ingest: stereo-dense-reconstruction

Research question: dense 3D reconstruction (TSDF/mesh/dense point cloud) from passive stereo — quality gap vs RGB-D, compute requirements, per-object on-demand feasibility, VPP coverage fix, active speckle projector gap closure.

8 sources captured to `raw/research/stereo-dense-reconstruction/` (marker engine, CPU-only due to CUDA OOM on first attempt):
- 01: Bartolomei et al. IJCV 2024 (VPP journal) — arXiv 2406.04345
- 02: Bartolomei et al. ICCV 2023 (VPP conference) — arXiv 2309.12315
- 03: Shi et al. ICRA 2024 (ASGrasp) — arXiv 2405.05648
- 04: Fan et al. 2024 (InstantSplat) — arXiv 2403.20309
- 05: vppstereo.github.io project page (thin)
- 06: Open3D TSDF integration docs
- 07: Wolf et al. 2024 (GS2Mesh) — arXiv 2404.01810
- 08: Guo et al. 2023 (depth completion) — arXiv 2303.15840

Audit: 0 issues. All captures valid.

New wiki page: [[stereo-dense-reconstruction]]. Index updated.

Note: marker engine was OOM-killed (exit 137) on first attempt with CUDA_VISIBLE_DEVICES unset. Resolved by running with CUDA_VISIBLE_DEVICES="" on subsequent captures. This is a kit-level learning (logged to master_notes.md).
