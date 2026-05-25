# MIGHTY (Hermite-spline UAV trajectory planning)

MIGHTY is an onboard real-time quadrotor trajectory planner (MIT-ACL + UPenn) that performs joint spatiotemporal optimization over a quintic Hermite spline, beating MINCO-class baselines on travel/compute time and flying up to 6.7 m/s through cluttered static and dynamic environments. *Demoed* in simulation and hardware; code released under [mit-acl/mighty](https://github.com/mit-acl/mighty).

## Method

- **Hermite-spline parameterization.** Degree-5 (quintic) Hermite spline in R^3: each knot carries explicit position, velocity, and acceleration, plus per-segment durations. All of these are decision variables in a single unconstrained NLP, solved with L-BFGS (solver adapted from GCOPTER).
- **What the Hermite basis buys them.** Unlike B-splines (geometric local control but only *indirect* derivative control) and MINCO (globally coupled coefficients, no geometric local control, no direct higher-derivative control), Hermite knots guarantee C^ν continuity *by construction* while giving **direct, local** control of both waypoint geometry and higher-order derivatives at each knot. Per Table I, MIGHTY is the only listed method offering joint time optimization, full polynomial+time search space, and direct+local control simultaneously.
- **Spatiotemporal joint optimization.** Positions, velocities, accelerations, and segment durations T_s are optimized together in one solve (no decoupled time-reallocation stage as in EGO-Planner/RAPTOR). Durations are kept positive via a diffeomorphism (T_s = e^σ); derivative knots are reparameterized (scaled by local duration) for numerical stability — ablation shows the scaled variant is ~2× faster compute with lower jerk.
- **Bézier evaluation trick.** *(synthesis)* Optimization runs in Hermite variables (for continuity) but cost terms are evaluated in the equivalent Bézier basis, where derivative sampling reduces to small reusable dot-product tables — faster and numerically steadier than recomputing Hermite polynomials per sample. Hermite↔Bézier is an affine map; Bézier is not required in general.
- **Dynamic obstacles.** Handled as a soft-penalty cost term J_dyn that activates inside a soft barrier radius C_dyn = 3.0 m around each moving obstacle's predicted position k(t); not a hard constraint (robot collision radius is 0.1 m). In hardware, a person carrying obstacles is tracked and the estimates fed into the optimization. Static obstacles use safe-flight-corridor (SFC) half-space penalties built after an A* global pass.

## Results

Benchmarked against GCOPTER (MINCO), EGO-Swarm, EGO-Swarm2, and SUPER.

- **Complex-scene benchmark (vs GCOPTER, 24 goals × 5 speed limits):** overall **−9.3% computation time**, **−13.1% travel time**, −1.4% path length, with **100% success**. Trade-off: ~+113% jerk integral (more aggressive maneuvers, tunable via w_smooth) — GCOPTER stays smoother.
- **Static obstacle-rich benchmark (300×40 m, vs EGO-Swarm/EGO-Swarm2/SUPER):** MIGHTY achieves the **shortest travel time (79.0 s) and path length (310.9 m)** at 100% success. EGO-Swarm2 is faster per-solve (~1.2 ms vs MIGHTY's 10.5 ms local / 19.7 ms total) but longer-traveling; EGO-Swarm and SUPER need tuning to hit 100%.
- **Dynamic-obstacle sim:** 100 trefoil-moving obstacles → avoids all in 10/10 trials (min clearance 0.8 m); +50 static obstacles → 10/10 (min 1.0 m). Robot collision radius 0.1 m.
- **Hardware:** long-duration flights at v_max ∈ {1,2,3,4} m/s collision-free; high-speed runs at v_max = 5/6/7 m/s all collision-free, peak measured **6.7 m/s** (at the 7 m/s setting); dynamic-obstacle flight reaching goal collision-free over 490 s.

## Compute / onboard story

- **Sim host:** Intel i9-9900K, 64 GB RAM, Ubuntu 22.04, ROS 2 Humble (for benchmarks).
- **Onboard (hardware):** planning runs onboard on an **Intel NUC 13**; low-level control on **PX4 / Pixhawk**. All perception, planning, and control run in real time onboard — the headline efficiency gains target high-frequency replanning on this class of compute. A* + SFC generation averages 0.26 ms + 0.48 ms.

## Sensing dependence

MIGHTY's hardware stack is explicitly **LiDAR-based**: perception via a **Livox Mid-360** LiDAR, localization via **DLIO** (Direct LiDAR-Inertial Odometry). The paper frames the hardware experiments as using "a LiDAR-based perception and localization system" and notes MIGHTY and SUPER are both LiDAR-based, while EGO-Swarm2's default is a depth camera. *(synthesis)* This is a usage choice consistent with the authors' lab stack, not a claim that LiDAR is *required* by the planner — MIGHTY is a trajectory optimizer consuming a point cloud / occupancy map and obstacle estimates, agnostic to how those are produced. The repo confirms the LiDAR coupling at the software level: dependencies include Livox-SDK2 and livox_ros_driver2, and the sim uses livox_laser_simulation_ros2.

## Repo facts

- **License/status:** accepted to IEEE RA-L (2026, DOI 10.1109/LRA.2026.3681187). Repo at [github.com/mit-acl/mighty](https://github.com/mit-acl/mighty).
- **Platform:** Ubuntu 22.04, ROS 2 Humble. Three install paths: Docker (Linux), Docker (Mac, via Xpra browser viz), and native Linux via `./setup.sh` (installs ROS 2 Humble, imports pinned repos from `mighty.repos`, builds DecompROS2 / Livox-SDK2 / livox_ros_driver2).
- **Sim:** `make run-interactive` (click goals in RViz2) or `make run-gazebo` (default env `hard_forest`, default goal 305/0/3); native launcher `run_sim.py`.
- **Notes:** L-BFGS solver adapted from ZJU-FAST-Lab/GCOPTER. Paper benchmarking code (simple/complex/sweep/reference scenarios) lives in a separate fork (kotakondo/GCOPTER).

## Source

- `01-mighty-arxiv.md` — full MIGHTY paper text (abstract, Hermite-spline formulation, simulation benchmarks, hardware experiments), captured from PDF — https://arxiv.org/pdf/2511.10822
- `02-mighty-repo.md` — mit-acl/mighty GitHub README (install methods, sim launch targets, dependencies, citation) — https://github.com/mit-acl/mighty

## Related

- [[indoor-obstacle-avoidance]]
- [[drone-autonomy-state]]
- [[lidar-vs-vision-autonomy]]
- [[lidar-for-uav-autonomy]]
- [[fast-lio-mid360-orin]]
- [[safe-indoor-flight]]
