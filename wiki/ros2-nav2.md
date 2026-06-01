# ROS 2 Nav2

Nav2 (Navigation2) is the canonical mobile robot navigation stack for ROS 2, built to replace ROS 1 Navigation. It uses a configurable behavior tree to orchestrate planner, controller, smoother, route, and recovery servers via ROS 2 action interfaces, leveraging multi-core processors and managed lifecycle nodes for deterministic bringup. Nav2 is relevant to the project as the navigation backbone for the ground-robot Phase-1 prototype: it integrates directly with SLAM Toolbox, provides the TEB controller used in task-driven benchmarks, and its WiFi/DDS transport constraints intersect with [[drone-comms-wifi]] issues on the companion-computer path.

## Source

- `raw/research/ros2-nav2/03-marathon2-nav2.md` — Marathon 2 paper, IROS 2020 (Macenski et al.)
- `raw/research/ros2-nav2/02-nav2-concepts.md` — Nav2 official concepts documentation
- `raw/research/ros2-nav2/02-nav2-slam-integration.md` — Nav2 SLAM integration tutorial
- `raw/research/ros2-nav2/04-task-driven-slam-bench.md` — Task-driven SLAM benchmark, arXiv 2409.16573 (Du et al., updated Mar 2025)

## Related

[[slam-toolbox]] · [[slam]] · [[learned-slam]] · [[drone-comms-wifi]] · [[system-architecture]] · [[robot-vacuum-navigation]] · [[home-tidy-drone-prototype]]

---

## Architecture

### Action server hierarchy

The BT Navigator is the top-level component. It loads a behavior tree from an XML file at runtime and ticks it; each BT node is a trivial plugin that calls one of the downstream action servers [src: marathon2-nav2]. Nav2 exposes five core action servers [src: nav2-concepts]:

| Server | Role |
|---|---|
| Planner server | Global path from current pose to goal (freespace planning) |
| Controller server | Local control effort to follow global plan |
| Smoother server | Post-process path to reduce raggedness and obstacle proximity |
| Route server | Route over a pre-defined navigation graph (nodes + directional edges); supports lanes, teach-and-repeat, urban roadways — not freespace planning |
| Behavior (recovery) server | Fault-tolerant recoveries; exposes costmap subscriber to avoid costly duplication |

Each server hosts a named map of **pluginlib algorithm plugins** sharing a single costmap instance — avoiding expensive duplication [src: nav2-concepts]. BT nodes call servers via the ROS 2 action interface, enabling long-running async tasks on separate processor cores [src: marathon2-nav2].

All servers follow the **REP-105 TF tree**: `map → odom → base_link → [sensor frames]`. The global positioning system (SLAM or AMCL) owns the `map → odom` transform; the odometry system owns `odom → base_link` [src: nav2-concepts].

Nav2 has **no hard requirement on LiDAR** — vision/depth sensors are equally supported as long as REP-105 TF standards are met [src: nav2-concepts].

The **robot footprint** is updatable at runtime via the `~/footprint` topic to reflect changes such as an attached manipulator or pallet [src: nav2-concepts].

### Costmap layers

| Layer | Type | Function | Notes |
|---|---|---|---|
| Static Layer | Static | Loads occupancy grid from SLAM or disk | Initializes lethal obstacles |
| Inflation Layer | 2D | Exponential-decay convolution of collision footprint | Inflates obstacle boundary |
| Obstacle Layer | 2D raycasting | Clears/marks cells from 2D sensor data | Standard laser/depth |
| Voxel Layer | 3D raycasting | Raycasts 3D sensor data into 2D costmap | Projects down |
| STVL (Spatio-Temporal Voxel Layer) | 3D temporal sparse voxel grid | Temporal decay over time; scales better than raycasting with many/high-res sensors (2D/3D scanners, depth cameras, radar) [src: marathon2-nav2] | Preferred for dynamic scenes |

**Costmap filters** are a layer-plugin mechanism that reads a filter mask image and applies spatial behavioral changes: keep-out zones, speed restriction areas, preferred lanes [src: nav2-concepts].

### Controllers

**TEB (Timed Elastic Band)**: time-optimal nonlinear MPC controller [src: marathon2-nav2]. Supports differential, omnidirectional, and ackermann kinematics. Can ingest external object detection tracks as constraints. Used in the marathon experiments and in the task-driven SLAM benchmark [src: task-driven-slam-bench].

**DWB**: a highly configurable scoring-based DWA implementation. Also available as a plugin but **excluded from the marathon experiments** due to poor performance in dynamic scenes [src: marathon2-nav2].

**Global planner**: NavFn A\* at a 1 Hz tick rate. Assumes a 2D holonomic particle — a known limitation for non-circular non-holonomic robots (e.g., car-like platforms) where paths may not be kinematically feasible [src: marathon2-nav2].

### State estimation and localization

**Robot Localization** package (EKF or UKF) fuses N arbitrary sensor sources — typically wheel odometry, IMU(s), and visual odometry — to produce a smooth, continuous `odom → base_link` transform [src: marathon2-nav2] [src: nav2-concepts].

**AMCL** (Adaptive Monte Carlo Localization): particle filter that localizes against a pre-built occupancy grid map. Used as the primary localization tool during the marathon experiments. Degrades in long corridors with repetitive features when dynamic obstacles occlude static map rays — the spin recovery helped recover localization confidence in these cases [src: marathon2-nav2].

**SLAM Toolbox** is the default SLAM vendor for ROS 2, used to generate the static map in pre-experiment preparation [src: marathon2-nav2]. See [[slam-toolbox]].

When running live SLAM (instead of AMCL against a static map), omit `nav2_amcl` and `nav2_map_server` — the SLAM node owns the `map → odom` TF and publishes `/map` [src: nav2-slam-integration]. Any conforming SLAM implementation can substitute; the only requirement is that it publishes `/map` and provides `map → odom` [src: nav2-slam-integration].

### Lifecycle and crash recovery

All Nav2 servers use **ROS 2 Lifecycle/Managed Nodes** for deterministic bringup: nodes transition through unconfigured → inactive → active → finalized states with clear memory/networking responsibilities at each transition [src: marathon2-nav2] [src: nav2-concepts].

Nav2 wraps these as `nav2_util::LifecycleNode`, which adds a **bond** connection: if a server crashes after activation, the bond notifies the lifecycle manager, which triggers a system-wide graceful shutdown rather than silent failure [src: nav2-concepts].

The recovery escalation ladder (from the marathon BT): Clear Costmap → Spin → Wait, ordered conservative-to-aggressive. Failures in a subtree trigger subtree-local recoveries first; root-fallback fires only on total failure [src: marathon2-nav2].

---

## SLAM integration

To run Nav2 with live SLAM [src: nav2-slam-integration]:

1. Launch robot interfaces + `robot_state_publisher`
2. Launch Nav2 **without** `nav2_amcl` and `nav2_map_server`: `ros2 launch nav2_bringup navigation_launch.py`
3. Launch SLAM Toolbox async: `ros2 launch slam_toolbox online_async_launch.py`

The SLAM node owns the `map → odom` TF and publishes `/map`. Nav2 consumes both. Any conforming SLAM can substitute — the constraint is purely the TF + topic contract.

Save a completed map: `ros2 run nav2_map_server map_saver_cli -f ~/map` [src: nav2-slam-integration].

---

## SLAM method comparison for indoor navigation

From the task-driven benchmark (TaskSLAM-Bench, arXiv 2409.16573) [src: task-driven-slam-bench]. Navigation module: TEB. Real-world test hardware: Turtlebot 2, RPLiDAR S2 (2D), RealSense D435i (stereo visual), Velodyne-16 (3D LiDAR). N-AUC = normalized area under cumulative precision curve (higher = better).

| Method | Sensor | N-AUC w/ map (real-world) | N-AUC short-path | Notes |
|---|---|---|---|---|
| SLAM Toolbox | 2D LiDAR | **0.93** | 0.94 | Scan-to-map registration well-suited indoors |
| GF-GG | Stereo visual | **0.90** | 0.96 | Comparable to SLAM Toolbox; fails long-path mapping |
| ORB-SLAM3 | Stereo visual | — (long-path failure) | 0.97 | Perfect short-path; mapping phase fails long-distance |
| LIO-SAM | 3D LiDAR-inertial | — (long-path failure) | 0.86 | Mapping phase fails long-distance indoor test |
| FAST-LIO2 | 3D LiDAR-inertial | — | — | Underperforms 2D LiDAR indoors [src: task-driven-slam-bench] |
| HectorSLAM | 2D LiDAR | <35% completion | — | Excluded; no loop closure |
| DSOL / MSCKF | Visual | <35% completion | — | Excluded; odometry-only, no map |

Simulation environments: Small House (144 m², 45 m), Warehouse (260 m², 70 m), Hospital (1400 m², 220 m) [src: task-driven-slam-bench].

**Key findings:**

- **Precision (repeatability) matters more than accuracy for task execution.** A robot that consistently arrives 5 cm from goal is more useful than one averaging 3 cm with 20 cm variance [src: task-driven-slam-bench].
- Using a pre-built SLAM map improves precision: EuRoC position precision improved from ~1/6 to ~1/12 robot diameter; orientation precision improved ~10× [src: task-driven-slam-bench].
- SLAM Toolbox mean precision error with map: **1.75 cm** (simulation) [src: task-driven-slam-bench].
- **3D LiDAR methods (FAST-LIO2, LIO-SAM) underperform 2D LiDAR (SLAM Toolbox) for indoor repeated-navigation precision.** Their design emphasis on exploration and outdoor structured scenes (where geometric loop closure is robust) does not transfer to compact, featureful indoor rooms [src: task-driven-slam-bench].
- Passive stereo visual SLAM (GF-GG) approaches 2D LiDAR precision indoors on short paths [src: task-driven-slam-bench].

---

## Marathon 2 benchmark

Conducted at Rey Juan Carlos University in a campus setting with students [src: marathon2-nav2]:

| Metric | RB-1 | Tiago | Total |
|---|---|---|---|
| Time (hrs) | 9.4 | 13.4 | **22.8** |
| Distance (miles) | 15.6 | 21.8 | **37.4** |
| Recoveries | 52 | 116 | **168 (4.3/mile)** |
| Collisions | 0 | 0 | **0** |
| Emergency stops | 0 | 0 | **0** |
| Avg speed (m/s) | 0.39 | 0.35 | 0.37 |

Both robots capped at 0.45 m/s (below hardware limits of 1.0 m/s and 1.5 m/s respectively) [src: marathon2-nav2]. Passive human assistance: <1 minute total over 22.8 hours (goal-pose occupation edge case in the application, not a Nav2 failure) [src: marathon2-nav2].

Recovery breakdown: majority triggered by (1) crowded-space path blocking → clear costmap + wait, and (2) localization confidence drop in long repetitive corridors → spin recovery [src: marathon2-nav2].

---

## Implications for the project

*(synthesis)* The following apply to the ground-robot Phase-1 prototype (see [[system-architecture]], [[home-tidy-drone-prototype]]):

**SLAM choice:** The task-driven benchmark directly undermines the earlier [[fast-lio-mid360-orin]] preference. FAST-LIO2 and LIO-SAM both underperform SLAM Toolbox for indoor repeated-navigation precision — the scenario that matters most for a home-tidying robot returning repeatedly to the same objects and docking station. For the ground-robot Phase-1, **SLAM Toolbox (2D LiDAR) is the better-supported choice** unless the environment is too large or too featureless for 2D scan matching. The MID360 remains valuable for safe 3D obstacle avoidance via STVL, but navigation precision should be driven by SLAM Toolbox's 2D scan-to-map layer, not FAST-LIO2's odometry output.

**Recovery rate:** 4.3 recoveries/mile is normal and healthy, not a failure signal. Nav2's BT recovery ladder handles dynamic human environments well; the project should tune recovery conservatism to environment density rather than trying to eliminate recoveries.

**DDS-over-WiFi:** Nav2 on a companion computer communicating with a remote planner or user interface over home WiFi inherits the multicast-discovery and latency issues documented in [[drone-comms-wifi]]. Use a Discovery Server or Zenoh RMW to prevent multicast storms; the action server timeouts in the BT should be tuned to WiFi jitter. The bond mechanism provides crash safety but cannot compensate for sustained WiFi dropout — the autonomy stack must be designed to degrade gracefully when the remote connection drops.

**Footprint topic:** The `~/footprint` runtime update is directly useful if the robot acquires a payload (a retrieved object changes the collision envelope). Wire this to the manipulation layer in [[system-architecture]].
