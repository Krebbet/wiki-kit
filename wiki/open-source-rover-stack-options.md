# Open-Source Options for the Rover's Navigation, Mapping and Planning Stack

The drone-prototype rover runs a from-scratch Python stack (about 76k LOC in `src/drone`, 2026-11-12). This page maps
each of its functional areas to maintained open-source equivalents and judges what each would replace. It covers fit
with a 2D LiDAR on a tilt + lift head plus passive stereo, the integration route (pure pip, C++ with bindings, or ROS 2
only), licence, maturity and gotchas, and a small offline test on recorded data that would show whether the library
beats our code. The finding has three parts:
- **The classic parts work.** Scan registration, the pose graph, A* and the guard are small and sound. One measurement
  shows a library buys speed there, not accuracy.
- **Our pain is elsewhere.** It sits in route-search time, mirror-room global localisation, floor vs low objects at
  2 cm, and the "priced doubt / check-first" drivability semantics.
- **Standard counterparts exist for two of those**: Monte Carlo localisation, and Smac-style lattice planning. A
  partial one exists for a third (elevation mapping). Nothing off the shelf models check-first.

Recommendation (a HUMAN DECISION, open): adopt libraries piecemeal behind existing interfaces, plus one offline ROS 2
benchmark. Do not adopt ROS 2 + Nav2 wholesale.

## Source

- drone-prototype `eda/EDA336-oss-options/` (2026-11-12): the inventory, the candidate tables, and a measured
  small_gicp vs own-ICP smoke test on `data/maps/office-2026-09-21`.
- Nav2 Smac Planner docs: https://docs.nav2.org/configuration/packages/configuring-smac-planner.html; Macenski et al.,
  cost-aware kinematically feasible planning: https://arxiv.org/html/2401.13078v2
- Nav2 MPPI: https://docs.ros.org/en/humble/p/nav2_mppi_controller/. Regulated Pure Pursuit:
  https://docs.nav2.org/configuration/packages/configuring-regulated-pp.html. Costmap filters:
  https://docs.nav2.org/tutorials/docs/navigation2_with_speed_filter.html
- OMPL 2.0 release notes (nanobind bindings, pip wheels, numpy >= 2): https://ompl.kavrakilab.org/releaseNotes.html,
  https://pypi.org/project/ompl/
- Beluga (ROS-agnostic C++17 MCL, nav2_amcl parity): https://github.com/Ekumen-OS/beluga; ROSCon 2024 talk:
  https://roscon.ros.org/2024/talks/Beluga_AMCL-_A_modern_Monte_Carlo_Localization_implementation_for_ROS.pdf
- Particle-filter premature convergence in symmetric environments: https://bohrium.dp.tech/paper/arxiv/2501.01153
- slam_toolbox localisation mode needs an initial pose:
  https://answers.ros.org/question/395174/how-to-properly-use-the-localization-mode-of-slam_toolbox/
- small_gicp: https://github.com/koide3/small_gicp. KISS-ICP: https://github.com/PRBonn/kiss-icp. Kinematic-ICP
  (2D LaserScan, wheeled, ROS 2 only): https://github.com/PRBonn/kinematic-icp
- elevation_mapping_cupy (Python + CuPy core, ROS 2 Jazzy node, numpy < 2):
  https://leggedrobotics.github.io/elevation_mapping_cupy/
- Isaac ROS nvblox requirements: https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_nvblox/index.html
- micro-ROS ESP-IDF component: https://components.espressif.com/components/micro-ros/micro_ros_espidf_component/versions/25.0.0/examples;
  memory profiling: https://micro.ros.org/docs/concepts/benchmarking/memo_prof
- REP 2000 (ROS 2 distro and Ubuntu pairing): https://reps.openrobotics.org/rep-2000/; https://endoflife.date/ros-2;
  RoboStack / pixi: https://robostack.github.io/GettingStarted.html, https://pixi.prefix.dev/latest/build/ros/
- GitHub API stars / licence / last push, and PyPI wheel sizes, queried 2026-11-12.

## Related

[[ros2-nav2]] · [[slam-toolbox]] · [[2d-lidar-slam]] · [[ros2-server-bridge]] · [[active-slam-exploration]] ·
[[weak-scan-registration-methods]] · [[stop-and-scan-room-mapping]] · [[stop-and-go-navigation-on-a-locked-map]] ·
[[odometry-closed-loop-pipeline]] · [[tilting-2d-lidar-multiplane-capture]] · [[task-conditioned-object-maps]] ·
[[robot-vacuum-navigation]] · [[system-architecture]] · [[home-tidy-drone-prototype]]

---

## 1. Platform facts that decide the integration route

- **Ubuntu 22.04 → ROS 2 Humble natively (EOL May 2027).** Jazzy (to 2029) is Tier-1 only on 24.04, so on this
  laptop it means RoboStack / pixi conda packages (`ros-jazzy-navigation2` exists) or Docker [src: REP 2000, RoboStack].
- **Compute.** i7-11800H, 15 GB RAM shared with other sessions (often under 4 GB free). An **RTX 3050 Mobile with
  4 GB** is present, but it is not guaranteed on a future robot computer.
- **Two Pythons.** The numpy 1.x env blocks OMPL 2.0 (numpy >= 2). The numpy 2.x env blocks elevation_mapping_cupy
  (numpy < 2) [src: OMPL notes, emcupy docs]. Pick the env per library.

## 2. Area → candidate map

| Our area (pain today) | Best open-source counterpart | Route | Licence | Verdict |
|---|---|---|---|---|
| Cold-start localisation in a near-mirror room (refusals; mirror accepted 1/30) | **Monte Carlo localisation** (Beluga core / nav2_amcl): keeps both mirror modes and lets a known motion kill the wrong one | Beluga: C++ (no Python bindings), ROS 2 wrappers. Or ~300 LOC numpy | Apache-2.0 / LGPL-2.1 (nav2_amcl) | **Test first.** Disable adaptive shrink until the modes separate: AMCL converges prematurely in symmetric rooms [src: 2501.01153] |
| Route search (0.6-1.1 s median, 8.3 s max; can miss routes; hand-picked constants) | **Nav2 Smac State Lattice** (any footprint, collision checks precomputed per heading bin, diff-drive primitives, 50-200 ms) [src: smac docs]. **OMPL 2.0** as a comparator | Smac: ROS 2 C++ only, so port the design. OMPL: pip, 4.6 MB | Apache-2.0 / BSD-3 | **Test.** The bottleneck is per-move Python rule judging. Rasterise the rules into per-heading masks, then search. A Python validity callback into OMPL would not be faster |
| Scan registration (works; ~30 ms per ICP) | **small_gicp** (pip 0.4 MB, works with numpy 1.25) | pip | MIT | **Measured** (§3): ~9x faster, slightly less tight. Use as the coarse stage only |
| Floor vs low objects at 2 cm | **elevation_mapping_cupy core**: per-cell height + variance Kalman fusion, outlier rejection, traversability layer | Lift the Python + CuPy core out of the ROS node | MIT | **Test after the error budget.** The gain is capped by pose / tilt / lift error, not by the fusion method |
| Keep-outs that must clear; coverage | OctoMap (pip wheels) log-odds with free-space ray clearing | pip | BSD / MIT | Optional comparator. 2-4 cm voxels are coarse vs a 2 cm threshold |
| Mapping / pose graph (passes its honest checks) | slam_toolbox (Karto + Ceres; localisation mode; multi-session) | ROS 2 only | LGPL-2.1 | **Benchmark only.** Localisation mode needs an initial pose, so it does not solve the mirror [src: answers.ros] |
| "Priced doubt / check-first" drivability, belief-driven keep-outs | Nothing equivalent. Nav2 costmaps are scalar cost + keep-out / speed filter masks [src: costmap filters] | -- | -- | Keep ours. A Nav2 port would need custom C++ layers + BT nodes |
| Station / NBV selection | explore_lite / m-explore-ros2 (greedy frontier) | ROS 2 | BSD | Skip: weaker than our stations (see [[active-slam-exploration]] §7) |
| Task loop / recoveries | py_trees (pure Python, BSD-3) | pip | BSD-3 | Refactor value only. Consider at the brain/body refactor |
| Continuous path following | Nav2 RPP (rotate-to-heading), MPPI (DiffDrive, CPU 30-50 Hz) [src: mppi docs] | ROS 2 | Apache-2.0 | Not needed while the rover moves stop-and-go by design |
| Proximity guard | Nav2 collision_monitor | ROS 2 | Apache-2.0 | Keep ours (T1, latched arbiter) |
| ESP32 link | micro-ROS (serial / USB-CDC, static memory, ~8.7 kB per subscriber) [src: micro-ROS profiling] | ESP-IDF + a host ROS agent | Apache-2.0 | Only with a wholesale ROS adoption |
| Continuous LiDAR odometry | KISS-ICP (pip; not designed for 2D); Kinematic-ICP (2D LaserScan, ROS 2 only) | -- | MIT | Unused while we stop and scan |
| Dense 3D mapping | nvblox (wants Ampere + 8 GB), Voxblox (ROS 1, frozen) | -- | -- | Skip on a 4 GB GPU with passive stereo |

## 3. What the rig measured (2026-11-12, EDA336)

**Setup.**
- Data: the locked office map, 29 stations; the 28 consecutive pairs with at least 50 points.
- Points: refined wall + object points (noise excluded).
- Seeds: three seeds per perturbation level.
- Reference: the optimised pose graph. **It is biased toward our own ICP**, which built it.

| Seed perturbation | Own point-to-line ICP | small_gicp (2D points extruded ±0.1 m) |
|---|---|---|
| ±5 cm / ±5° | 0.12 cm / 0.04°, 100 % within 2 cm and 1°, 32 ms | 0.33 cm / 0.07°, 89 %, 3.5 ms |
| ±30 cm / ±30° | 0.13 cm / 0.04°, 99 %, 31 ms | 0.35 cm / 0.07°, 86 %, 4.1 ms |

*(synthesis)* Registration is not where the stack is weak. A library is a speed lever (~9x) for the places that run
many ICPs: the cold start's multi-start, and relocalisation inside the planning worker.

## 4. Ranked shortlist (gain on a current pain / integration cost)

1. **MCL across a known motion** (numpy first) → the mirror cold start. Replay the recorded cold starts with
   odometry between two captures; then live: one cold start + one 90° turn.
2. **Lattice planning on per-heading footprint masks** (the Smac design; OMPL 2.0 comparator) → planning time and
   missed routes. Test on the EDA333 118-route bench: time, found, verifier pass rate, cost.
3. **small_gicp coarse + own ICP fine** → cold-start wall time. Measured speed-up; near-zero risk.
4. **Elevation-map height + variance fusion** → the 2 cm floor call, after EDA335's error budget.
5. **Offline ROS 2 sandbox benchmark** (slam_toolbox mapping a converted episode; Smac on exported costmaps) → an
   independent reference, and data for the ROS decision.

## 5. Architecture question: ROS 2 wholesale vs piecemeal vs own (HUMAN DECISION, open)

**Wholesale ROS 2 + Nav2.**
- Gains: maintained planners, controllers, BT recoveries, AMCL, slam_toolbox, micro-ROS, rosbag / sim tooling, and
  the Phase-2 hiring path.
- Costs: a Humble-or-OS-upgrade constraint, RAM on a shared laptop, and wrapping ~76k LOC.
- The rig's differentiators would all need custom C++ plugins: check-first pricing, tilt / lift stop-and-scan,
  height-aware drive-over / under, belief keep-outs that clear.

**Piecemeal (recommended now).**
- Each library replaces one measured weak spot behind an existing interface, and is replayable before going live.
- The transport contract already makes a later ROS bridge a carrier swap ([[ros2-server-bridge]]).

**All our own.** This forgoes the two standard wins (MCL, lattice search).

**Revisit at the Phase-2 boundary** with the sandbox numbers.
