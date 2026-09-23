# Tilting a 2D LiDAR into multi-plane capture — nodding rigs, stepped sweeps, and what this rig should do

**Summary.** The established way to make a 2D LiDAR see in 3D is to pitch it about a horizontal axis and accumulate every plane into **one 3D point cloud in one frame** — Kurt3D's AIS scanner pitched *between* horizontal scans while the robot sat still (120° max pitch, 128/256 lines, 3.4–30 s per 3D scan) and *re-levelled the same scanner* to drive; the PR2 carried a **second, fixed base laser** so the tilting one was never the navigation sensor.
The load-bearing calibration is the **tilt-axis-to-beam-origin lever arm**: a 4 cm arm at −26.6° displaces the sensor origin 1.8 cm, **3.6× our 0.5 cm registration accuracy** — build it out if the mount allows, measure it if not, never assume it — and a tilted plane is **not a height layer, it is a ramp**, z = 1.10 + x·tan τ, so "register each height as its own 2D map" is geometrically void.
Recommendation: keep 0° as the map/registration/guard plane, add a **stepped 7-angle ladder uniform in tan τ** (−26.6…+14.0°, 25 cm height spacing at 2 m range), carry every tilted scan on the *level* scan's station pose instead of registering it, and derive a **2.5D multi-level surface grid** from the accumulated cloud — tilting only while stationary, with a verified return to level before any wheel goal.

## CORRECTION (2026-09-23, measured on the rig — read before §5 and §6)

**This page's §5–6 reason from a 1.10 m scan plane. The rover's is 0.337 ± 0.005 m.** The 1.10 m
came from `data/calib/rig_geometry.json`, which describes the June **capture rig** — a tripod
carrying the stereo camera — a *different platform*. Measured two ways in drone-prototype EDA228:
floor returns give `h = r·sin φ` (0.350 / 0.340 / 0.336 m at −20 / −25 / −26.5°), and the wall→floor
break-away angle brackets the same value independently.

Three conclusions on this page invert:

1. **§5 "It closes the known blind spot" is wrong.** There is no blind spot below 1.1 m to close by
   tilting down — the rover already scans at ankle height, which is why it sees chair legs and floor
   clutter. The unseen band is **above** 0.337 m: table tops (0.74 m), counters (0.9 m), shelves.
   The ladder should be weighted **upward**, not downward.
2. **§7's floor-line warning mostly does not apply to an upward ladder.** An up-tilted beam never
   reaches the floor. The warning transfers intact to the **ceiling** instead — the top angles reach
   a 2.41 m ceiling beyond ~2 m range, and a ceiling line is as straight and dense as a floor line.
3. **§6's ladder (−26.6…+14.0°) points the wrong way** for this platform. Re-derived as 0° plus eight
   upward steps uniform in `tan τ` (0 → +43.5°): see drone-prototype `docs/next-campaign-scoping.md`
   §"REVISED PLAN".

**What this page got right and the rig confirmed.** The lever arm is the load-bearing calibration:
measured at **9.6 cm** (the tape to the visible scanner head said 6.2 — the true pivot is lower),
displacing the sensor 4.0 cm at the down limit and 6.6 cm at the up limit, 8–13× the rig's 0.5 cm
registration accuracy. Its identifiability caveat also held exactly: at a **single** wall distance
the arm is algebraically indistinguishable from a tilt-zero error, and a first version of the
verification harness would have passed a rig carrying 1.8 cm of unmodelled error. Four wall
distances were needed; **closer beat further** (1/d is 1.67 at 0.6 m vs 0.50 at 2.0 m). The §7
prediction that **the rig's self-occlusion zones move with tilt** was observed directly: 0.05–0.07 m
returns at bearings swinging from −110° toward −70° tilting up, outside the 0°-surveyed mask.

---

## Source

Literature in *Sources*. Rig facts: `docs/wheel-calibration.md` §Procedure B (measured travel), `data/calib/rig_geometry.json`, `src/drone/devices/{tilt,lidar}.py`, `src/drone/guard.py`, `src/drone/mapping/scanclean.py`, `docs/locked-map-office.md`, `docs/next-campaign-scoping.md`. All §6 geometry is computed here from h = 1.10 m and the measured travel — arithmetic, not a citation.

## Related

[[stop-and-scan-room-mapping]] · [[lidar-floorplan-extraction]] · [[stop-and-go-navigation-on-a-locked-map]] · [[lidar-multiscan-capture-recipe]] · [[world-model-architecture]] · [[point-cloud-object-segmentation-models]] · [[3d-shape-completion-for-object-footprints]] · [[floor-map-sensing-options]] · [[sensor-mount-2dof-tilt-lift]] · [[apple-roomplan]] · [[sensor-weaknesses-and-fixes]] · [[imu-vio-integration-reality]]

---

## 1. The nodding 2D LiDAR as a 3D sensor — what the classic rigs did

The pattern is twenty years old and it is a *mount plus a servo*, not a new sensor.

- **Kurt3D / the AIS 3D laser range finder** (Surmann, Nüchter, Hertzberg, Fraunhofer AIS) is the closest precedent to this rig. A SICK LMS 2D scanner on a mount rotated by "a standard servo motor, with the rotation axis being horizontal". Crucially it "executes a controlled **pitch motion between the regular horizontal scans**" — a **stepped** sweep, not a continuous nod. Maximum pitch 120°, selectable **128 or 256 vertical lines** (0.94° / 0.47° spacing) against 181 / 361 / 721 points per line over 180° horizontally; **a full 3D scan takes between 3.4 s and about 30 s** depending on the resolution chosen, with ~1 cm accuracy per point. The robot "3D scans the scene from the current pose **while sitting still**", registers, plans the next view pose and drives — the stop-scan-plan-go loop this project already runs in 2D [[stop-and-scan-room-mapping]]. Registration is a kD-tree-accelerated ICP variant solving all six DOF; one published lab model is 32 scans / 302,820 points [surmann-tdp, surmann-2003].
- **PR2** (Willow Garage) split the job across **two** Hokuyo UTM-30LX scanners: one **fixed on the mobile base** for navigation and obstacle detection, and a **separate tilting one on the torso** for 3D perception and tabletop manipulation. That is the architectural precedent for keeping a navigation plane and a perception sweep apart [pr2-robotsguide].
- **Continuously-swept rigs** — CSIRO's **Zebedee**, a 2D scanner on a *spring* so the operator's own motion shakes it through a 3D sweep [bosse-zebedee], and spinning-2D-laser mobile mappers generally — take the opposite branch: never stop, sweep continuously, and solve a continuous-time trajectory so every point lands in one frame. They exist because the platform is *moving*; the price is that motion and sweep are entangled and must be estimated jointly.

Across all of them the sweep's "vertical resolution" is not a sensor property — it is the angular step of the *actuator*, traded directly against sweep time (Kurt3D's 3.4 s ↔ 30 s span is exactly that trade), and each capture is still a **plane**, from which everything in §6 follows.

## 2. The calibration that actually matters — the lever arm

A nodding rig has one parameter that dominates everything else: **the offset between the tilt axis and the laser's beam origin.** The tilt axis almost never passes through the beam origin, so rotating by τ *translates* the sensor as well as aiming it. With a lever arm ℓ the origin moves ℓ·sin τ along the arm and ℓ·(1−cos τ) across it:

| lever arm ℓ | at τ = ±26.6° | at τ = +41.4° |
|---|---|---|
| 4 cm | 1.8 cm / 0.4 cm | 2.6 cm / 1.0 cm |
| 6 cm | 2.7 cm / 0.6 cm | 4.0 cm / 1.5 cm |
| 8 cm | 3.6 cm / 0.9 cm | 5.3 cm / 2.0 cm |

This is not a hypothetical offset: the PR2 ships one. Its URDF puts the tilting Hokuyo at `<origin xyz="0 0 0.03">` on the `laser_tilt_mount` link — a **modelled 3 cm lever arm**, carried in the kinematic chain and calibrated, not designed away [pr2-urdf]. Compare against what we hold ourselves to: 0.5 cm median relocalisation, 0.6 cm wall bands, 2.5 cm go-to-pose. **An unmodelled 4 cm arm is already 3.6× the per-station registration error** — it does not average out, it is a systematic, tilt-dependent shift that will bow every wall in the accumulated cloud. This rig has form here: `odom.py` carries a 4.1 cm / 3.2 cm lever arm for the LiDAR versus the *rotation centre* of an in-place spin, fitted on 64 turns, because ignoring it left a 4.6 cm residual. The tilt axis is the same problem in a different plane.

Two companions to it:
- **Tilt zero.** Already burned once: `POS_CENTRE = 2048` was an assumption; level is count **2530**, a **42° error** that would have propagated into every scan-plane calculation (`docs/wheel-calibration.md`). Measured values only.
- **Roll of the tilt axis.** If the tilt axis is not perpendicular to the forward direction by ρ, the plane rolls as it tilts and height acquires a lateral term, z ≈ h + x·tan τ + y·tan ρ. At y = 2 m, **ρ = 1° is 3.5 cm** — the same size as the lever arm. It must be solved for alongside, not assumed zero.

**The best fix is to design the arm out, not calibrate it.** Kurt3D's scanner "is **attached in the center of rotation** to the mount" [nuchter-icar2005], and Morales et al. build the axis through the optical centre because it "allows the 3D device to **maintain the same minimum range** as the 2D scanner and **avoids offsets in computing Cartesian coordinates**" [morales-boresight]. Before calibrating anything, check whether our mount can be shimmed so the tilt axis passes through the C1's beam origin — that deletes the dominant error term instead of modelling it.
Failing that, self-calibrate by **cloud crispness**: sweep a static scene and pick the parameters that make the cloud sharpest, since a wrong arm smears a flat wall into a curved shell [sheehan-selfcal, alismail-spinning]. **But know what that can and cannot identify.** Morales et al. are explicit: off-the-shelf scanner range bias "is in the order of centimeters for Sick and Hokuyo sensors. Therefore, since translation misalignments… are expected to be around a few millimeters, **they cannot be estimated by using readings from the sensor itself** in an unprepared environment, and the problem reduces to **boresight calibration**" — i.e. angles only [morales-boresight]. Sheehan et al. measure the same asymmetry: over 30 test sites the radial term τ shows a **3 mm standard deviation**, and "changing the plate radius τ a few mm has a **proportionally smaller** effect on point cloud entropy" than the angles do [sheehan-selfcal]. Our ~4 cm arm sits *above* that cm-scale bias floor, so it is estimable where a 3 mm one would not be — but measure it mechanically first; let the fit confirm it, not define it. That is also the cheapest *check* available to us, and we have a second, even cheaper one that is specific to a floor-standing rig: the **floor line**. At tilt τ the floor returns form a straight line at exactly 1.10/tan|τ| — 2.20 m at −26.6° — and that distance moves ~9.6 cm per degree of tilt error. Drive to clear floor, command −26.6°, measure the line: that single number calibrates the tilt zero to a fraction of a degree.

## 3. Stepped vs continuous nod — for a rig that is already stopped

| | stepped (tilt, settle, scan, repeat) | continuous nod |
|---|---|---|
| geometry per scan | exact: sensor static, one pose per plane | every point needs its own pose |
| timestamping | one stamp per revolution is enough | **per-point** timestamps + actuator angle at scan rate |
| deskewing | none needed | mandatory (interpolation / continuous-time trajectory) |
| vertical sampling | wherever you put the steps | uniform and dense for the same wall-clock time |
| dead time | servo move + settle per step | none |

For this rig the choice is not close. We are **stationary at a station by construction**, we already fuse 5 revolutions per capture with a revolution-agreement check (and get ~0.1 cm wall rms out of it), and `devices/lidar.py` carries **one `time.monotonic()` stamp per revolution — there are no per-point timestamps in the stack**, nor any stream of servo angle at 10 Hz. Continuous nodding would mean building both. Stepped costs dead time and **servo wear** — Wulf & Wagner's objection is that a limited-turn drive "cannot be turned with constant speed. The sensor has to be accelerated at the start and the end of each turn," cutting "lifetime and mechanical stability" and demanding a more powerful drive [wulf-wagner]; worth watching on an STS3215 doing seven steps a station. What it buys back is the thing continuous nodding spends its whole calibration budget recovering: an exact, static pose per plane. (Their desync model shows the size of that bill — `e = d·sin(ω_s·Δt)`, so **100 ms of laser/actuator desync is 1.3 m of error at 10 m** on a scanner nodding at 75°/s.) **Stepped.** (Established practice: Kurt3D, the original stop-and-scan nodder, is stepped for the same reason.)

## 4. Combining planes that are not coplanar

Three candidate representations; the rig's 0.5 cm station pose decides between them.

- **(a) One 3D point cloud + ICP/NDT.** The default in every nodding-scanner paper: pitch, accumulate, register the whole 3D scan against the map. Kurt3D ran exactly this — "a variant of the ICP algorithm, made efficient … by reduction of the point clouds and efficient representation (kD trees)", solving all six DOF, with per-point accuracy ~1 cm [surmann-tdp]. **The cost for us is that this is a new stack**, and worse, it is *ill-conditioned on our data*: seven sparse non-coplanar planes constrain the vertical DOF only through floor and ceiling returns, so an unconstrained 6-DOF ICP has a soft z/pitch/roll null space exactly where the tilt calibration error lives. It would be fitting away the calibration error rather than measuring it.
- **(b) 2.5D elevation / multi-level surface map (MLS).** Triebel, Pfaff & Burgard's grid where each cell holds not one height but a **list of vertical surface patches** — built precisely so an overhang, a bridge deck or a table is not collapsed into one number, and cheap enough to localise and close loops on [triebel-mls, pfaff-elevation]. This is the natural product of a tilt ladder and the natural substrate for the object layer the next campaign wants ([[world-model-architecture]]).
- **(c) Per-height 2D layers.** Real and standard — Hornung et al. run the PR2 on **three** projected layers (base, spine-with-head, arms), where a cell is *free* only if every discrete height in that layer is free, *occupied* as soon as one is, and *unknown* otherwise, so that "**a free cell guarantees that there is no collision in the 3D space corresponding to that layer**" [hornung-multilayer]. Their worked example is ours exactly: arms over a table, base under it — "**the table is only projected on the spine layer**". **But note how the layers are made**: "this 3D map is then **projected down** into a multi-layered 2D representation". They are *derived from* an octree, not captured or registered independently — and for a tilt ladder that distinction is decisive, because §6 shows a tilted plane is a **ramp**, not a constant-height slice (53 cm of height variation across one room at −15°). Layers are a *product*; (a) or (b) is the substrate. The one way to capture true layers directly is the mast's **Z-lift**, which translates without rotating — but its total travel is unrecorded and the soft limit sits at 20 mm (`docs/lift-axis-bringup.md`), so it is not a height axis today.

**The cost objection is already dead, and the standard objection to (b) does not bite here.** OctoMap stores a 43.7 × 18.2 × 3.3 m corridor at 5 cm in **41.6 MB pruned / 0.67 MB on disk** [hornung-octomap] — a small room's ladder is nothing. That same paper warns against the 2.5D shortcut in words that look aimed at us: *"While this is sufficient for path planning and navigation with a fixed robot shape, the map does not represent the actual environment, **e.g. for localization**"* — and [[lidar-floorplan-extraction]] §6.5 accepts that warning because our map is a *localization* anchor. The reconciliation is that **we keep two products, not one**: localisation and the floor plan stay on the **0° plane and the locked 2D map, untouched**; the MLS grid is the *object* layer, never the anchor. A 2.5D grid used only to answer "what is at what height here" is not the thing OctoMap is warning about.

**Verdict for this rig: skip the registration problem.** We are in the rare position of knowing the station pose to 0.5 cm / 0.4° *from the level plane*, which is 3.6× better than an uncalibrated 4 cm lever arm and ~7× better than a 1° roll error at 2 m. So carry every tilted scan on the level scan's pose through calibrated tilt kinematics, accumulate into a 3D cloud, and derive (b) from it. Spend the effort on the tilt calibration, not on a 3D matcher. This is judgement, not established practice — the precedents register in 3D because they do not have a 0.5 cm anchor plane.

## 5. What multi-height actually buys for objects — and how it fails

- **No single height works — that is settled, not arguable.** Liao et al. simulated horizontal 2D scanners on real indoor scans: *"the laser scanner set at 20 cm fails to detect the upper stove and the seat of the chairs… while the laser scanner set at 80 cm misses the lower garbage bins as well as the seats"* — two heights, two **disjoint** sets of misses [liao-parse-geometry]. Lundell et al. give the canonical consequence: a robot on raw 2D laser *"would see the legs of the table but not the tabletop itself, allowing it to plan and execute a trajectory through the table causing a collision"* [lundell-hallucinating]. And in a surveyed 10 × 10 m facility, LiDAR-only obstacle recall was **60.0 %, rising to 95.0 % fused with RGB-D**, the named misses including *"low obstacles: pallets below the laser scan plane"* [delhibabu-2dgrid].
- **It closes the known blind spot.** Today everything below 1.1 m is invisible to *both* the map and the guard, and a 0.9 m base counter against a wall makes the rig see the wall behind it and **certify false free space** ([[lidar-floorplan-extraction]] §Pitfalls: 1.8–4.8 m² per kitchen). One modest down-tilt fixes that: at −7.1° the plane is at 0.85 m at 2 m range, which cuts the counter front rather than passing over it.
- **It separates a table top from its legs — if the table is at the right distance.** A 0.74 m top is crossed by the plane where z(x) = 0.74, i.e. at x = 0.36/|tan τ|: **0.72 m at −26.6°, 0.96 m at −20.6°, 1.44 m at −14.0°, 2.88 m at −7.1°**. So the ladder places the 0.74 m contour at four distances between 0.7 and 2.9 m, and the top is grazed by whichever angle matches the table's range. This is the concrete reason tilt and translation belong together (protocol step 9): **tilt picks the ramp's slope, driving picks its offset.**
- **It does not make the learned 3D segmenters applicable.** Seven planes is ~3.5k points per station — [[point-cloud-object-segmentation-models]]'s verdict (Mask3D/PointGroup/OpenMask3D assume a dense coloured 3D scan and structurally do not run on our data) is unchanged. What changes is that the BEV + seeded-assignment route it recommends now has a **height channel** to cut on, and [[floor-map-sensing-options]]'s "a 2D LiDAR is a floor-map sensor, not an object-mapping sensor" becomes "unless you tilt it, and then only coarsely".
- **The up-tilt is not a throwaway.** Previtali et al. find that *"the acquisition of the ceiling surface, due to its location, is generally less influenced by clutter and occlusion than other surfaces in the room"* [previtali-cluttered-rooms], and [[lidar-floorplan-extraction]] §6.5 draws the conclusion that **1.1 m is the worst possible single height** — above the counters, below the ceiling. Our +41.4° limit meets a 2.4 m ceiling at 1.47 m range, so a ceiling shot from each station is reachable *today* with the LiDAR rather than waiting on stereo — a cleaner architectural boundary than the 1.1 m slice, and the one use of the up-travel that the asymmetric envelope is generous towards.
- **It gives bounds, not surfaces.** With seven planes an object's height is an interval — highest plane that returned, lowest plane that did not — typically ±12 cm at 1 m and ±25 cm at 2 m. That is enough for "tall thing vs low thing vs overhang", enough to feed the extent field the object layer wants ([[world-model-architecture]]), and not enough to fit a shape. Shape completion from partial evidence is the separate question in [[3d-shape-completion-for-object-footprints]].

The classic failure modes, with our numbers:

- **Thin structures.** Table and chair legs are 2–4 cm. At 0.72° spacing a 3 cm leg subtends ~2 samples at 1 m, ~1 at 2 m, ~0–1 at 3 m — and the ~1.5° beam cone is already 5 cm wide at 2 m, so the leg underfills the beam and the return is a mixed pixel with a biased range. **Legs are a ≤ 1.5 m proposition on this sensor**; beyond that, absence of a leg return is not absence of a leg.
- **Sparse vertical sampling.** Between planes there is nothing. A 25 cm gap at 2 m is 5 beam widths of pure ignorance and must be labelled `unknown`, exactly as the navigation grid labels unswept space — an object layer that interpolates between planes is inventing surfaces.
- **The floor line** (see §7) — a down-tilted plane produces the straightest, densest "wall" in the scan, and it is the floor. It is also struck at grazing incidence (26.6° at the down limit) on a lane that is semi-specular hardwood plus a textured rubber mat, so expect drop-outs and long returns on the hardwood. Untested — treat the first ladder as the experiment that answers it.
- **Veiling / mixed pixels at depth steps.** Standard on every nodding rig: the PR2's tilt-scan pipeline began with a dedicated **`tilt_shadow_filter`** before anything else touched the data [pr2-nav-perception]. A tilted plane crosses far more depth discontinuities per revolution than a level one, because it cuts objects obliquely — budget for a shadow/veiling filter in the ladder, not just the level scan.

## 6. Height sampling geometry for THIS rig — do the arithmetic first

Tilting the whole unit tilts the disc it sweeps, so the scan stays a **plane**. Plane ∩ floor is a **straight line**, not a conic. With the sensor at h = 1.10 m and tilt τ (positive up, forward horizontal distance x), the plane's height is

> **z(x) = 1.10 + x · tan τ**, independent of lateral offset y — and the floor line sits at **x_floor = 1.10 / tan|τ|** for a nose-down τ.

The consequence that decides the whole design: **one tilt angle is not one height.** At τ = −15° the "layer" is 0.83 m at 1 m and 0.30 m at 3 m — 53 cm of height variation across one small room.

| tilt τ | tan τ | z @ 1 m | z @ 2 m | z @ 3 m | floor line | ceiling (2.4 m) |
|---|---|---|---|---|---|---|
| **+41.4°** (up limit) | +0.882 | 1.98 | — | — | — | **1.47 m** |
| +20.6° | +0.375 | 1.48 | 1.85 | 2.23 | — | 3.5 m |
| **+14.0°** | +0.250 | 1.35 | 1.60 | 1.85 | — | 5.2 m |
| **+7.1°** | +0.125 | 1.23 | 1.35 | 1.48 | — | 10.4 m |
| **0.0°** (map plane) | 0.000 | 1.10 | 1.10 | 1.10 | — | — |
| **−7.1°** | −0.125 | 0.98 | 0.85 | 0.73 | 8.80 m | — |
| **−14.0°** | −0.250 | 0.85 | 0.60 | 0.35 | 4.40 m | — |
| **−20.6°** | −0.375 | 0.73 | 0.35 | — | 2.93 m | — |
| **−26.6°** | −0.500 | 0.60 | 0.10 | — | 2.20 m | — |
| −26.8° (down limit) | −0.505 | 0.59 | 0.09 | — | 2.18 m | — |

**Why those angles.** Vertical spacing at range x is Δz = x·Δ(tan τ), so a ladder **uniform in tan τ** — not in degrees — gives uniform height spacing at every range. A step of Δtan = 0.125 is **12.5 cm at 1 m, 25 cm at 2 m, 37.5 cm at 3 m**. The bolded 7 rows (−26.6 … +14.0°) sample 0.10–1.60 m at 2 m and 0.60–1.35 m at 1 m, which covers the 0–1.5 m band the object layer needs; +20.6° is the optional 8th for tall shelving, +41.4° is a ceiling shot (it hits a 2.4 m ceiling at 1.47 m, so it is a ceiling scan, not an object scan).

**This is coarse sampling and should be called that.** The C1 gives 0.72° azimuth steps (5 kHz ÷ 10 Hz = 500 points/rev), i.e. 2.5 cm arc spacing at 2 m *within* a plane, but the ladder's *vertical* spacing at 2 m is 25 cm — a factor of 10 anisotropy. The beam is also a ~1.5° cone ([[lidar-floorplan-extraction]] §Pitfalls), ≈ 5 cm of vertical footprint at 2 m, so 25 cm steps leave real gaps. Seven tilted planes are a **height sampler**, not a 3D scan.

**Scans per station.** Keep the existing 5 revolutions per angle (0.5 s at 10 Hz) and the revolution-agreement check; at ~1.5–2.5 s per step, seven angles is **10–18 s per station** against ~1–2 s today, ~2–4 min added to a 13-station room. Judgement, not measured — time the first ladder.

## 7. Safety and validity — the guard shares the plane

Tilting the head aims the **proximity guard** away from where the rover drives. `guard.py` watches a ±30° forward cone inside a ±0.20 m corridor and stops when ≥ 3 returns fall inside 0.28 m of the LiDAR (0.25 m from the nose). Tilted to +41.4°, the plane at the 0.28 m trip range is at **1.35 m** — every obstacle below that is invisible; tilted to −26.6° it is at 0.96 m, still above a chair seat. So a tilted guard is not a degraded guard, it is **no guard**.

Four more tilt-specific validity traps:

- **The floor line looks exactly like a wall.** `scanclean` defines a wall as "a long, straight, dense run". At −26.6° the floor returns form a dead-straight, dense line 2.20 m ahead spanning the full lateral field — the highest-confidence wall the cleaner has ever seen, and it is the floor. Every tilted scan must be height-labelled (z from the ramp equation) and floor returns removed **before** split-and-merge, or the ladder will corrupt the floor plan.
- **Chassis roll/pitch stops being free.** A level scan barely cares: a 1° chassis pitch shortens ranges by x(1−cos 1°) ≈ 0.3 mm at 2 m. The same 1° moves a *height* by x·1° ≈ **3.5 cm at 2 m**. Our station pose is 3-DOF (x, y, θ) — roll and pitch are never estimated. Office lane is hardwood + a textured rubber mat; driving onto the mat is exactly a pitch/roll event. This is the first product for which the pending USB IMU (O9) is load-bearing rather than nice-to-have.
- **A later plane CLEARS what an earlier one saw.** This is the named failure of exactly our sensor configuration. Lu, Hershberger & Smart trace ROS's move to layered costmaps to it: *"The original developers of the ROS implementation encountered this problem **when they used three-dimensional sensors like a tilting laser range finder**. If the obstacle data is stored only in the monolithic costmap, **obstacles at different heights could be inappropriately removed by clearing observations**"* [lu-layered-costmaps]. OctoMap documents the same trap at cell level — sweep a flat surface at a shallow angle and *a cell measured occupied in one scan is updated free in the next after the sensor rotates* — with the fix: **update each volume at most once per scan** [hornung-octomap]. A tilt ladder is a machine for generating this: seven planes cut the same counter edge at seven incidences. Fuse per-angle, then merge; never let plane *k+1*'s ray carve what plane *k* just occupied.
- **The rig's self-occlusion zones move.** `lidar_filter` drops measured mast (163–188.5°) and screw (234.5–248.5°) sectors, surveyed at 0°. The PR2's answer is instructive: its tilting scan ran through a **geometric `self_filter`** against the robot model (`tilt_laser_self_filter`), not a fixed angle mask, exactly because a tilting laser's view of its own body changes with the joint [pr2-nav-perception]. Either re-survey the zones per tilt angle, or filter against the mast geometry — a fixed sector list is wrong the moment the head moves.

**What the precedents do.** Kurt3D solved this by *re-levelling the same sensor*: it pitched only while sitting still, and for the drive between scan poses used "the scanner in 2D mode fixed in the position aligned with the robot axis (horizontal if the robot sits on a horizontal floor)" for pose tracking at up to 75 Hz [surmann-tdp]. The PR2 solved it with hardware: a **fixed Hokuyo UTM-30LX on the base** for navigation and costmaps, plus a **separate tilting Hokuyo** on the torso for 3D perception [pr2-robotsguide]. We have one LiDAR, so we take Kurt3D's answer: **tilt only while stopped, return to a verified 0° before any wheel goal.**

## Recommendation for this rig

A protocol, in the order it must be built. Steps 1–3 are prerequisites: **do not run a ladder before them.**

1. **Get human sign-off for autonomous tilt, and keep `set_deg`'s arrival check.** The human drives the head today (standing guardrail, `docs/next-campaign-scoping.md`). `Tilt.set_deg` already verifies arrival within 1.5° and refuses outside the measured −26.8…+41.4° travel — that is the right contract; nothing in the ladder may bypass it.
2. **First ask whether the lever arm can be built out** (§2) — if the mount can be shimmed so the tilt axis passes through the C1's beam origin, do that and skip most of what follows. Otherwise **measure ℓ mechanically** (calipers / CAD), then face a flat wall at ~2 m, sweep the ladder, and fit only the **angles and the tilt zero** (roll ρ, boresight, zero) from the plane residual — per Morales et al. a translation is not reliably identifiable from the sensor's own readings against a cm-scale range bias, so the fitted ℓ is a *cross-check* on the tape, never the source of truth. A 4 cm arm left unmodelled puts 1.8 cm into every scan at −26.6°, 3.6× our per-station registration error. Cross-check the zero with the **floor-line ruler**: on clear floor at −26.6° the floor line must sit at 2.20 m, and it moves ~9.6 cm per degree — a direct, cheap readout.
3. **Add a tilt interlock to motion and to the guard.** `guard.arm()` and any wheel goal refuse unless `tilt.read().deg` is within 1.5° of 0.0 (reuse `TILT_TOLERANCE_DEG`). Absence is not health: a tilt read that fails must block motion, not default to level.
4. **At each station, scan the level plane FIRST and register on it.** 0° is the map plane, the relocalisation plane and the guard plane; the locked office map (`docs/locked-map-office.md`) is defined there and must not change. The station pose comes from this scan alone, at 0.5 cm / 0.4°.
5. **Then step the ladder, stationary, uniform in tan τ:** **−26.6°, −20.6°, −14.0°, −7.1°, +7.1°, +14.0°** (0° is already in hand from step 4) — 5 revolutions and the existing revolution-agreement check at each. Add +20.6° for tall shelving and +41.4° for a ceiling shot only when a station needs them. Log every scan with its *read-back* tilt angle, never the commanded one.
6. **Do not register the tilted scans.** Carry each on the level scan's station pose through the calibrated tilt kinematics. Our pose is known to 0.5 cm; a sparse non-coplanar ICP would be solving for less than the calibration error it introduces. This is a judgement call and it is only valid while step 2 holds — re-check the lever arm after any mount or cable change.
7. **Height-label and floor-strip before cleaning.** Compute z per return from the ramp equation, drop returns with z < ~0.05 m (floor) and flag z > ~2.2 m (ceiling), *then* run split-and-merge. Otherwise the floor line is asserted as a wall.
8. **Accumulate into one 3D cloud in the map frame, and derive two products from it:** (a) the existing 2D floor plan, built from the 0° plane only and unchanged; (b) a **2.5D multi-level surface grid** — 5 cm cells, each holding a list of (z_top, z_bottom, support) intervals. The MLS interval list is what distinguishes "table top at 0.74 m with free space under it" from "solid to the floor"; a plain elevation map cannot.
9. **Use translation as the second axis.** Tilt sets the *slope* of the ramp; driving forward 0.5 m *slides* it, so a fixed angle sweeps an object's height as the rover approaches. For a target object, prefer two stations 0.5–1.0 m apart over two extra tilt angles — it also gives the parallax that separates a leg from a speckle.
10. **Report coverage honestly.** State per cell how many planes hit it and at what heights; anything sampled by one plane is a point, not a surface. Thin structures (2–4 cm legs) are at the C1's resolution limit beyond ~1.5 m (0.72° = 2.5 cm arc at 2 m), and an unsampled gap between planes must read `unknown`, never `free` — the same rule the navigation grid already applies.

## Sources

All web-verified 2026-09-22; quote provenance noted where it is not the publisher's own copy.

- [surmann-2003] Surmann, Nüchter, Hertzberg — *An autonomous mobile robot with a 3D laser range finder for 3D exploration and digitalization of indoor environments*, Robotics and Autonomous Systems 45(3):181–198, 2003. doi:10.1016/j.robot.2003.09.004 · PDF https://robotik.informatik.uni-wuerzburg.de/telematics/download/raas2003.pdf
- [surmann-tdp] Surmann, Nüchter, Lingemann, Pervölz et al. — *KURT3D*, RoboCup 2004 Rescue Team Description (AIS 3D laser scanner: SICK LMS + servo, horizontal rotation axis, pitch *between* horizontal scans, 120° max pitch, 128/256 lines, 181/361/721 pts per 180° line, 3.4 s–~30 s per 3D scan, ~1 cm/point, ICP + kD-trees in 6D, 2D mode at up to 75 Hz for pose tracking between scan poses). https://www.nist.gov/system/files/documents/el/isd/-GERMANY-KURT3D-TDP.pdf
- [pr2-robotsguide] *PR2* — ROBOTS: Your Guide to the World of Robotics, IEEE Spectrum (two Hokuyo UTM-30LX: one on the mobile base for navigation, one tilting on the torso). https://robotsguide.com/robots/pr2
- [hornung-octomap] Hornung, Wurm, Bennewitz, Stachniss, Burgard — *OctoMap: an efficient probabilistic 3D mapping framework based on octrees*, Autonomous Robots 34(3):189–206, 2013. doi:10.1007/s10514-012-9321-0 *(memory figures, the 2.5D-for-localization warning, the shallow-angle update trap — quoted via [[lidar-floorplan-extraction]] §6.5, verified there)*
- [liao-parse-geometry] Liao, Huang, Wang, Kodagoda, Yu, Liu — *Parse Geometry from a Line: Monocular Depth Estimation with Partial Laser Observation*, ICRA 2017. arXiv:1611.02174
- [lundell-hallucinating] Lundell, Verdoja, Kyrki — *Hallucinating Robots: Inferring Obstacle Distances from Partial Laser Measurements*, IROS 2018. arXiv:1805.12338
- [previtali-cluttered-rooms] Previtali, Barazzetti, Brumana, Scaioni — *Towards Automatic Indoor Reconstruction of Cluttered Building Rooms from Point Clouds*, ISPRS Annals II-5, 2014
- [delhibabu-2dgrid] Delhibabu, Zhukova, Gizzatov — *2D grid map creation based on RGBD-camera and LiDAR data*, Scientific Reports 16, 2026
- [bosse-zebedee] Bosse, Zlot, Flick — *Zebedee: Design of a Spring-Mounted 3-D Range Sensor with Application to Mobile Mapping*, IEEE Transactions on Robotics 28(5):1104–1119, 2012. doi:10.1109/TRO.2012.2200990
- [sheehan-selfcal] Sheehan, Harrison, Newman — *Self-calibration for a 3D laser*, The International Journal of Robotics Research 31(5):675–687, 2012. doi:10.1177/0278364911429475
- [alismail-spinning] Alismail, Browning — *Automatic Calibration of Spinning Actuated Lidar Internal Parameters*, Journal of Field Robotics 32:723–747, 2014. doi:10.1002/rob.21543
- [triebel-mls] Triebel, Pfaff, Burgard — *Multi-Level Surface Maps for Outdoor Terrain Mapping and Loop Closing*, IROS 2006, pp. 2276–2282. doi:10.1109/IROS.2006.282632
- [pfaff-elevation] Pfaff, Triebel, Burgard — *An Efficient Extension to Elevation Maps for Outdoor Terrain Mapping and Loop Closing*, The International Journal of Robotics Research 26:217–230, 2007. doi:10.1177/0278364906075165
- [lu-layered-costmaps] Lu, Hershberger, Smart — *Layered costmaps for context-sensitive navigation*, IROS 2014, pp. 709–715. doi:10.1109/IROS.2014.6942636 *(§III quote read first-hand from a third-party mirror of the PDF; DOI and metadata confirmed via Crossref)*
- [hornung-multilayer] Hornung, Phillips, Jones, Bennewitz, Likhachev, Chitta — *Navigation in Three-Dimensional Cluttered Environments for Mobile Manipulation*, ICRA 2012, pp. 423–429. doi:10.1109/ICRA.2012.6225029 · PDF https://www.arminhornung.de/Research/pub/hornung12icra_pr2.pdf
- [morales-boresight] Morales, Martínez, Mandow, Reina, Pequeño-Boter, García-Cerezo — *Boresight Calibration of Construction Misalignments for 3D Scanners Built with a 2D Laser Rangefinder Rotating on Its Optical Center*, Sensors 14(11):20025–20040, 2014. doi:10.3390/s141120025 *(open access; full text read via Europe PMC, PMC4279469)*
- [nuchter-icar2005] Nüchter, Lingemann, Hertzberg, Surmann — *6D SLAM with Approximate Data Association*, ICAR 2005 ("attached in the center of rotation"). https://robotik.informatik.uni-wuerzburg.de/telematics/download/icar2005_2.pdf
- [pr2-urdf] `pr2_description/urdf/tilting_laser_v0/tilting_laser.urdf.xacro`, PR2 common (tilt axis `0 1 0`, limits −0.7854…+1.48353 rad, laser `<origin xyz="0 0 0.03">`). https://github.com/PR2/pr2_common/blob/kinetic-devel/pr2_description/urdf/tilting_laser_v0/tilting_laser.urdf.xacro
- [wulf-wagner] Wulf, Wagner — *Fast 3D Scanning Methods for Laser Measurement Systems*, CSCS-14, Bucharest 2003 (scan geometries; `e = d·sin(ω_s·Δt)`; the constant-speed objection to limited-turn drives)
- [pr2-nav-perception] `pr2_navigation_perception/lasers_and_filters.xml`, PR2 navigation stack (separate filter chains for the base laser and the tilting laser; `tilt_shadow_filter` → `interpolate_missing_tilt_laser_data_filter` → `tilt_laser_self_filter`, a geometric robot-model self-filter rather than a fixed angle mask). https://github.com/PR2/pr2_navigation/blob/hydro-devel/pr2_navigation_perception/lasers_and_filters.xml
- [rplidar-c1] Slamtec — *RPLIDAR C1* product page and datasheet (5000 samples/s, 12 m radius, 0.05 m blind range; at the 10 Hz typical scan rate that is 500 points/rev = 0.72° angular step). https://www.slamtec.com/en/c1 · datasheet https://d229kd5ey79jzj.cloudfront.net/3157/SLAMTEC_rplidar_datasheet_C1_v1.0_en.pdf
