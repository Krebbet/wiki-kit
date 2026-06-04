# Passive-Stereo Robustification for Indoor SLAM (Consumer-Cost)

How to make a **passive stereo camera** robust enough to be a reusable indoor anchor-map sensor **without reaching for expensive 3D LiDAR** — the consumer-product cost tenet of the home-tidy build. Passive stereo is cheap and rich but starves on the textureless surfaces that dominate real homes (white walls, glass, glossy floors); this page consolidates the honest hard limit, the consumer-cost ranked robustifier ladder, the active-assisted-stereo escalation (a "dumb" IR dot projector that keeps the solution inside the stereo family), the pattern-as-calibration-validator insight, and the cheaper-than-D435i hardware ladder. It exists because the pieces were scattered across [[visual-inertial-slam]], [[indoor-cluttered-slam]], [[learned-slam]], and [[close-range-depth-sensors]] plus the prototype's own field findings, and step-4 of the build (RTAB-Map stereo + dense RGB-D) shouldn't re-derive them. *(synthesis — assembled from existing wiki pages + the `drone-prototype` prototyper log, with their own raw-source citations carried through.)*

## Source

Synthesis page; the load-bearing facts are cited inline to their home pages and raw sources:
- [[indoor-cluttered-slam]] — the honest hard limit (featureless-surface degradation; IMU bridging < 1 s) [src: 07-arxiv-2306-08522, 11-amazon-indoor-mapping]
- [[visual-inertial-slam]] — stereo+IMU full autonomy without LiDAR [src: 03-vislam-no-lidar.md / arXiv 2403.09596]
- [[learned-slam]] — learned front-ends (DPV-SLAM/DPVO, DBoW2 relocalization) and their compute cost [src: 05-dpv-slam-arxiv.md, 06-dpvo-repo.md]
- [[close-range-depth-sensors]] — active IR-stereo consumer modules (D435i, OAK-D SR/Pro) + prices [src: 02-02-arxiv-2501-07421.md, 10-08-oak-d-sr-forum-discussion.md]
- `drone-prototype` field findings — `docs/prototyper-log.md` stanzas 2026-06-01 19:00 / 19:30 / 2026-06-02; `docs/00-framing.md` "Product tenet"; measured SVPRO regime in [[home-tidy-drone-prototype]] "SVPRO characterization (measured)"

## Related

[[sensor-weaknesses-and-fixes]] · [[slam]] · [[indoor-cluttered-slam]] · [[visual-inertial-slam]] · [[imu-vio-integration-reality]] · [[learned-slam]] · [[close-range-depth-sensors]] · [[camera-calibration-and-self-calibration]] · [[map-then-navigate]] · [[slam-toolbox]] · [[2d-lidar-slam]] · [[cheap-lidar-pricing-guide]] · [[home-tidy-drone-prototype]] · [[system-architecture]]

> **Companion page:** [[sensor-weaknesses-and-fixes]] isolates the *sensor-rooted* (not software-fixable) causes of the relocalization geometry failure — ranked sensor weaknesses → ranked cheap sensor upgrades → the single highest-leverage change (active stereo / D435i). This page is the *software/algorithm* ladder; that page is the *hardware* lens on the same problem.

---

## 1. The problem and the honest hard limit

The prototype's load-bearing sensor is a passive USB stereo camera (the SVPRO), chosen so the build can prove **marker-free** indoor mapping. Passive stereo computes depth by matching texture between two shifted images — which means it **starves wherever there is no texture to match**. Homes are the worst case for this: plain white walls, glass, mirrors, and glossy floors are exactly the surfaces passive matching cannot see.

This is a real, documented limit, not a tuning problem:

- **All vision-based SLAM degrades on plain white walls, glossy floors, and glass; no tested system handles all the failure modes without human tuning** [src: 07-arxiv-2306-08522, 11-amazon-indoor-mapping] (via [[indoor-cluttered-slam]] §Key gaps). The NUFR-M3F benchmark records vision-only algorithms failing at "featureless white-wall corridors and glass surfaces" outright.
- **IMU bridging is short-lived — it covers < 1 s of feature starvation** [src: 07-arxiv-2306-08522, 11-amazon-indoor-mapping]. An IMU rescues motion blur and a brief blank patch; it is **not** a sustained-white-wall cure. *(This is the single most important caveat on the whole ladder: the IMU is rung 1 because it is the highest robustness per dollar, but it does not solve the headline failure mode.)*
- The prototype reproduced this directly: SGBM passive depth on a real room gave **~48 % pixel coverage**, dropped out **entirely on blank walls / ceiling / bright window**, and — more dangerously — produced **spurious *far* depth** on textureless far surfaces (center-of-room read ~19 m where a wall actually stood) — a false "clear far" failure mode (`drone-prototype` diary 2026-06-01, step-3). *(synthesis)*

The correct response is **not** "passive stereo is infeasible → buy LiDAR." It is to climb a ladder of consumer-cost robustifiers, and — when texture genuinely runs out — to *add the missing texture* with active illumination, which keeps the solution inside the stereo family and at consumer cost (§4).

## 2. The consumer-cost tenet (why this page exists)

The build is meant to become a **consumer product**, so the sensing must be cheap to produce. The framing contract bounds it to **(a) passive/active stereo vision** or **(b) a *cheap* LiDAR that earns its cost** — explicitly **NOT** an expensive 3D LiDAR such as the Livox MID360-class (`drone-prototype` `docs/00-framing.md` → Product tenet; human ruling 2026-06-01). The benchmark-superior 2D-LiDAR / SLAM-Toolbox path ([[slam-toolbox]], [[2d-lidar-slam]]) stays a **documented escalation, not the default**, and AprilTags/fiducials are ruled out for this prototype.

The standing directive is therefore: **push passive stereo and find workarounds before reaching for any LiDAR.** This page is the consolidated answer to "what are those workarounds, in cost order, and where do they each break?" — so step-4 doesn't re-grep four pages. *(synthesis)*

## 3. The robustifier ladder (consumer-cost ranked)

Climb this when the passive SVPRO starves on texture. Every rung stays consumer-priced; the order is roughly robustness-per-dollar. (Mirrors the escalation list in `docs/00-framing.md` and the step-4 handoff.)

| Rung | Robustifier | Approx. cost | What it buys | Honest caveat |
|---|---|---|---|---|
| 1 | **Cheap MEMS IMU → visual-inertial (VIO)** | ~$5 | Highest robustness/$. Bridges motion blur, brief blank patches, pure-rotation. Stereo+IMU did full outdoor forest autonomy with no LiDAR/GNSS ([[visual-inertial-slam]], OKVIS2). RTAB-Map / ORB-SLAM3 both ingest IMU. | **Bridges < 1 s of starvation** [src: 07-arxiv-2306-08522] — not a white-wall cure. |
| 2 | **Dense-depth RGB-D mode (not sparse VO)** | $0 (already have depth) | Feed SGBM (or RAFT-Stereo) depth to RTAB-Map as an RGB-D source. Geometry-based matching is more robust on low texture than sparse ORB features. | Dense passive depth is still noisy/speckled and still empty where there is *no* texture; it densifies what's there, it doesn't conjure features on a blank wall. |
| 3 | **Learned front-end** | $0 SW (GPU cost) | SuperPoint + LightGlue features, or a DPV-SLAM-class deep VO, are robust on low texture. DPV-SLAM adds DBoW2 loop closure ([[learned-slam]]). | Compute is the catch: DPV-SLAM runs **5–7 GB GPU, desktop-class**, borderline on an 8 GB Orin and monocular (needs external metric scale) [src: 05-dpv-slam-arxiv.md]. |
| 4 | **Robustness engineering** | $0 | A **health-tracker** (covisibility + velocity-divergence checks) that maps where ORB-SLAM3 / VINS-Fusion fail — exactly Amazon's grocery-SLAM approach [src: 11-amazon-indoor-mapping]; RTAB-Map's **DBoW2 appearance relocalization**; build the map under good, controlled lighting; lean on real homes having clutter/texture (a truly-blank gallery wall is the worst case, not the typical case). | Engineering buys reliability and graceful failure, not new signal — it can't see a feature that isn't there. |
| 5 | **Active-assisted stereo** | ~$12–340 | Spray artificial texture onto blank walls with a cheap IR dot/speckle projector so passive matching gets features. **The consumer-proven cure for the #1 failure mode** — see §4. Still "stereo vision," still consumer-priced (it is what a RealSense D435i / OAK-D SR *is*). | Coverage-bounded: shadows, range² falloff, out-of-cone surfaces still drop out (§4). |

Only after rung 5 is genuinely exhausted does a **cheap 2D LiDAR** (RPLiDAR-class, see [[2d-lidar-slam]], [[cheap-lidar-pricing-guide]]) become the next honest escalation — and even that stays inside the cost tenet; the MID360-class never does.

## 4. Active stereo — the "dumb" projector that does the work

The key insight: **active stereo adds artificial texture with a static, uncalibrated projector, and the SGBM/stereo pipeline is otherwise unchanged.** This works because of stereo geometry — *depth depends only on the two cameras' relative geometry*. The projector is just "scene paint": it lights up the surface so both cameras see matchable structure; it does **not** participate in the triangulation. (This is distinct from *structured light*, e.g. a single Kinect-v1 sensor, where the projected pattern is the known reference and must be calibrated.) *(synthesis, grounded in `drone-prototype` prototyper-log 2026-06-02.)*

Two consequences:

- **The projector can be independent / fixed for a prototype.** Because depth comes from the camera pair and each frame is instantaneous, the projector need not be rigidly mounted to or synced with the cameras — projector wobble is harmless, an uncalibrated room-painting light source works for a bench (Stage 0) demo. *(This corrects an earlier "the projector must ride the same rig" assumption in the prototyper log — that concern was about coverage, not sync.)*
  - **Coverage is the only downside of a fixed projector:** shadows, intensity falling off as range², and surfaces outside the projector cone simply don't get lit. A single fixed projector lights one region of one room.
- **For a product it becomes a tiny co-mounted IR projector.** Co-mounting matters once the robot *roams* — so the lit area follows the cameras beyond a fixed projector's reach. The product form is a fingernail-sized **VCSEL + DOE IR dot projector** (the part inside a RealSense D435i, or a phone's Face-ID dot projector), **< 1 W**, IR so it's invisible and doesn't disturb the room. "Much smaller" is the standard here, not a stretch — it arrives for free at the D435i hardware step (§6).

So the bulky visible pico projector used in early prototyping is a throwaway stand-in for that fingernail IR module — useful only because a controllable visible PNG pattern is easy to debug. *(synthesis, prototyper-log 2026-06-02.)*

## 5. The projected pattern as a calibration **validator** (not a calibration source)

A natural temptation is to use the dense speckle pattern to *calibrate* the cameras and skip the checkerboard. **It can't replace the checkerboard** for intrinsics: the projected pattern has unknown geometry and the projector is uncalibrated, so there are no known world points to solve against (unlike a checkerboard's known square grid). *(synthesis, prototyper-log 2026-06-02.)*

But the dense left↔right correspondences a speckle produces on an otherwise-blank wall are a genuinely useful **calibration *validator***:

- **Epipolar / rectification check + extrinsic refinement** — dense matches on a blank wall directly expose vertical (epipolar) misalignment in the current rectification, where a textured natural scene gives sparse, clustered evidence. This bears straight on the prototype's open calibration debt (stereo RMS ~2.45 px, baseline unverified to metrology grade — see parked **P-002**).
- **Flat-wall planarity test** — project speckle on a known flat wall, reconstruct the 3D points, and check they form a plane at the right distance. This is the standard depth-camera QA step (cf. Intel RealSense **"Tare"** / on-target calibration). It's a one-tool acceptance check that the metric depth is true.

**→ Candidate path to retire P-002.** Adding the flat-wall planarity test as a calibration-QA tool (when the projector arrives) is a concrete way to validate/tighten the calibration that the checkerboard solve left at prototype grade. Logged as a follow-up in the prototyper log (2026-06-02). *(synthesis.)*

**See [[camera-calibration-and-self-calibration]]** for the full calibration treatment: why the prototype's offline solve hit a focal/baseline degeneracy (fronto-parallel poses) and how tilt+depth coverage + a known-distance anchor break it, plus the survey of **online / self-correcting calibration** (OpenVINS, OKVIS2-X, VINS-Fusion, Kalibr-as-reference, DSO photometric) for a robot that should tighten its own calibration over its life.

## 6. Hardware ladder — getting to active stereo, cheaply

The expensive part of active stereo is **not** the projector — a tiny IR DOE dot projector is the cheap common ingredient in every path (~$20–50). What differs between rungs is **how you get IR-capable cameras** to see the IR pattern. Ladder, cheapest first *(prices per `drone-prototype` prototyper-log 2026-06-02 and [[close-range-depth-sensors]]; verify before purchase)*:

| Rung | Setup | Approx. price | Notes |
|---|---|---|---|
| A | **Visible pico / star-laser projector + the existing SVPRO** | ~$12–70 | Stage-0 / bench proof. Controllable visible speckle PNG via a pico projector (debuggable), or a small USB laser "star" projector (random dots, mountable; Class-3 eye-safety caution). A single-dot laser module is the *wrong* tool — you need a *field* of dots. |
| B | **IR-convert the SVPRO + IR DOE dot projector** | parts-cheap (+ surgery risk) | Cheapest in parts, but means modifying our one already-flaky camera (P-001) — surgery risk on the load-bearing sensor. |
| C | **Arducam OV9281 NoIR global-shutter stereo (~$26/cam) + 850 nm IR DOE projector (~$20–50)** | **≈ $80–150** | **The product-shaped budget answer.** IR-native (no surgery), and **global shutter > the SVPRO's rolling shutter** for moving-camera SLAM. Build-it-yourself active IR stereo at consumer cost. |
| D | **RealSense D435i — turnkey** | **$334** | Active IR stereo + IR dot projector + **BMI055 IMU** + factory calibration in one package; works out-of-box with RTAB-Map / ORB-SLAM3 [src: 02-02-arxiv-2501-07421.md, close-range D435/D435i note]. The "just buy the answer" rung — rungs 1, 2, 5 of §3 in a single $334 module. |
| — | ~~OAK-D Pro ($399)~~ | $399 | **Skip** — *more* expensive than the D435i, so not the budget answer [src: 02-02-arxiv-2501-07421.md]. (OAK-D SR at $199 is a short-range arm camera, not a room-mapping nav sensor — see [[close-range-depth-sensors]].) |

Everything on this ladder honors the consumer-cost tenet (§2): the turnkey top rung (D435i, $334) is still an order of magnitude under a MID360-class 3D LiDAR. *(synthesis.)*

## 7. Implications for the step-4 build

- **Run baseline passive stereo first, and characterize the failure regime honestly** — *where* and *why* tracking and depth drop out (blank walls, glass, glossy floor, lighting). The prototype already has the front-end measurements (~48 % coverage, blank-wall dropout, spurious-far-depth); SLAM (RTAB-Map stereo) will feel the same texture starvation. This characterization is a mandate deliverable in its own right, and it tells the projector exactly what to attack.
- **Then the projector attacks exactly that regime.** Add active illumination *to the measured failure surfaces*, not speculatively — the point of measuring first is to aim rung 5 precisely.
- **Use the two-phase architecture as-is.** RTAB-Map's built-in map serialization + localization-only mode *is* the [[map-then-navigate]] build → save → relocalize pattern; the robustifiers make the *mapping* phase survive low texture, and DBoW2 appearance relocalization (rung 4) makes the *localization* phase recover. Don't hand-roll save/relocalize.
- **Keep the escalation costed but un-bought** until the SVPRO's honest limit is measured — climb the §6 ladder only as far as the measured failure forces. Stage-0 buy is visible speckle (rung A); the IR rungs follow only if passive + cheap robustifiers can't clear the anchor-map bar.
