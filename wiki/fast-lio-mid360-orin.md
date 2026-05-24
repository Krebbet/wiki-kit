# FAST-LIO2 + Livox MID360 on Jetson Orin

Build reference for deploying LiDAR-inertial odometry with a Livox MID360 and a Jetson Orin companion under ROS 2: the FAST-LIO2 algorithm and its ROS2 branch status, the livox_ros_driver2 stack, MID360 networking/IMU quirks, LiDAR-IMU extrinsic/temporal init, and the variant ecosystem a builder will actually pick from.

## FAST-LIO2 algorithm

FAST-LIO2 (Xu, Cai, He, Lin, Zhang; arXiv 2107.06829) is a tightly-coupled LiDAR-inertial odometry framework built on an iterated extended Kalman filter operating on-manifold (M ≜ SO(3)×R¹⁵×SO(3)×R³). Two novelties vs FAST-LIO1: (1) **direct registration of raw points** to the map — no feature extraction — which exploits subtle structure and makes it sensor-agnostic across scan patterns; (2) the **ikd-Tree**, an incremental, self-rebalancing k-d tree supporting point-wise insert, box-wise delete, on-tree downsampling, and parallel kNN, so the map updates at odometry rate instead of being rebuilt per scan. A reformulated Kalman gain inverts in the (smaller) state dimension rather than the measurement dimension, cutting cost by orders of magnitude. Result: up to 100 Hz odometry+mapping, robust under rotation up to 1000 deg/s in cluttered indoor scenes (*demoed*). IMU runs ~200 Hz, LiDAR 10–100 Hz; back-propagation deskews each scan. ikd-Tree params used in-paper: α_bal=0.6, α_del=0.5, N_max=1500; spatial downsample l=0.5 m (outdoor — indoor builds want finer, see Build notes).

## ROS2 branch status

The canonical hku-mars/FAST_LIO repo's `ROS2` branch is maintained by community contributor Ericsii (Ericsiii) rather than the original MARS lab — treat ROS2 support as community-driven (*claimed*). Requires Ubuntu ≥20.04, ROS ≥Foxy (Humble recommended), PCL ≥1.8, Eigen ≥3.3.4. **livox_ros_driver2 must be built and sourced before building FAST_LIO**, since the Livox CustomMsg type is a compile dependency. Clone `--recursive` (pulls ikd-Tree, IKFoM submodules), `colcon build --symlink-install`. Launch: `ros2 launch fast_lio mapping.launch.py config_file:=avia.yaml` (point a MID360 config at it). FAST-LIO2 confirmed running on ARM platforms — Khadas VIM3, Nvidia TX2, Raspberry Pi 4B — which is the relevant precedent for Orin (*demoed*).

## livox_ros_driver2 + MID360 config

livox_ros_driver2 is Livox's 2nd-gen driver, ROS1/ROS2 (Foxy/Humble/Jazzy). **Must be cloned into `<ws>/src/livox_ros_driver2` and built with the bundled `./build.sh <distro>`** (e.g. `./build.sh humble`) — direct `colcon build` fails due to custom-message generation branching (Humble changed `rosidl_typesupport_cpp`). Depends on Livox-SDK2 installed first. Key launch params:

- `xfer_format` — **0** = PointCloud2 (PointXYZRTLT), **1** = Livox CustomMsg, 2 = PCL PointXYZI. FAST-LIO/Point-LIO need the **CustomMsg** path (`xfer_format=1`, the `msg_MID360` launch) because only it carries per-point `offset_time`, which is load-bearing for motion undistortion. PointCloud2 from this driver does also carry a per-point `timestamp` field (the "Failed to find match for field 'time'" warning means timestamps are missing — fatal for de-skew).
- `publish_freq` — default 10.0 Hz; raise to 100.0 for high-rate odometry (verified at 100 Hz on the wire).
- `multi_topic` — 0 shares one topic, 1 per-LiDAR.

Topics: `/livox/lidar` (PointCloud2 or CustomMsg) and `/livox/imu` (sensor_msgs/Imu) at 200 Hz (*demoed*, fixstars). gotcha: if `liblivox_lidar_sdk_shared.so` / `liblivox_sdk_shared.so` won't load, run `sudo ldconfig` or add `/usr/local/lib` to `LD_LIBRARY_PATH`.

### MID360 networking

MID360 is **static-IP only**: default `192.168.1.1XX/24` where XX = last two serial digits, mask 255.255.255.0, gateway 192.168.1.1. Set the Orin NIC to a matching subnet (fixstars used host `192.168.1.200`, LiDAR `.102`) and edit `MID360_config.json`: every `host_net_info` IP → host, and the `lidar_configs[].ip` → LiDAR. MID360 command/data ports are fixed (cmd 56100, push 56200, point 56300, imu 56400, log 56500 LiDAR-side; host side 561xx/562xx/etc.) — do not change them. `pcl_data_type`: 1 = 32-bit cartesian (default), 2 = 16-bit, 3 = spherical. `pattern_mode`: 0 = non-repeating (default), 1/2 = repeating. Sensor: 360°×59° FoV, ~200k pts/s, 40 m range, built-in ICM-40609-D 6-axis IMU, 65×65×60 mm.

## MID360 built-in IMU quirks

The MID360's built-in IMU is the central integration trap. **Its accelerometer reports in units of g, not m/s²** — `/livox/imu` linear_acceleration is ~9.81× too small for `sensor_msgs/Imu` consumers (nexty-ele). Two fixes:

1. **Conversion node** — subscribe `/livox/imu`, multiply linear_acceleration by 9.81, republish `/imu_converted` (nexty provides a ~40-line rclpy node; confirmed Humble + Jazzy, and confirmed to materially reduce FAST-LIO tracking loss) (*demoed*).
2. **Patch the driver** in-place (livox_ros_driver2 issue #157).

Algorithm-side, the cleaner path is to tell the estimator the IMU is in g: LI-Init and Point-LIO expose an acc-norm/`acc_norm` param — set **mean_acc_norm = 1** (vs 9.805) when feeding the raw Livox built-in IMU, and 9.805 for a Pixhawk-class IMU (LI-Init). The FAST-LIVO2 ecosystem flags the same unit ambiguity (the "nexty IMU column" framing; FAST-LIVO2 issue #120) — verify your scale before trusting any LIO output.

## LiDAR-IMU extrinsic & temporal init

For a fixed MID360 (LiDAR and IMU rigidly co-housed), the extrinsic rarely changes — write it once into the FAST-LIO config (`extrinsic_T`, `extrinsic_R`; defined as the LiDAR pose **in the IMU body frame**, found in the Livox manual) and set `extrinsic_est_en=false`. When you don't have it, use **hku-mars/LiDAR_IMU_Init (LI-Init, IROS 2022)**: target-free, real-time calibration of extrinsic, temporal offset, gravity, and IMU bias, with no prior map or initial guess. It runs a modified FAST-LO front-end, auto-detects excitation and instructs the operator which way to rotate/translate; it then hands off to sequential FAST-LIO. Recommended params: hold still >5 s after launch for a dense initial map; `cut_frame_num * orig_odom_freq ≈ 50` for Livox; `online_refine_time` 15–30 s; indoor `filter_size_surf` 0.05–0.15, `filter_size_map` 0.15–0.25. **Units gotcha twice over**: angular velocity must be rad/s (issue #43), and `mean_acc_norm=1` for the Livox built-in IMU. Temporal note: Livox timestamps count from power-on, so re-calibrate time offset after each power cycle unless you've confirmed it's stable enough to bake into `time_diff_lidar_to_imu`. IMU bias and gravity are refined online by FAST-LIO and need not be written.

## Variant ecosystem for a builder

- **spark-fast-lio** (MIT-SPARK) — FAST-LIO2 ported to ROS2 with refactor, launch-configurable viz frame, gravity alignment, and out-of-the-box pairing with **KISS-Matcher-SAM** for loop closure. Cleanest native-ROS2 starting point; config keys `lidar_type`, `scan_line`, `timestamp_unit`, `filter_size_map`, and `extrinsic_T/R` (LiDAR w.r.t. IMU). Velodyne/Ouster examples ship; MID360 needs your own config (*demoed*).
- **Point-LIO-Mid360** (overloadsc, wraps hku-mars/Point-LIO) — point-by-point filter, 4k–8 kHz odometry, no motion distortion, survives IMU saturation and ~75 rad/s motion; relevant if the build has aggressive dynamics. ROS Noetic in this fork. Requires setting `satu_acc`, `satu_gyro`, `acc_norm` to your IMU; can run IMU-less with a `gravity_init` guess (*demoed*).
- **FAST_LIO_SLAM** (gisbi-kim) — FAST-LIO2 odometry + Scan-Context loop detection + GTSAM pose-graph (SC-PGO) run as two nodes; gives a globally consistent, drift-corrected map and a keyframe-pcd saver. ROS1; Livox launch files were "coming soon" as of the captured README (*claimed* for MID360). Alt: FAST_LIO_LC (yanliang-wang).
- **FAST-LIVO2-ROS2-MID360-Fisheye** (Rhymer-Lcy) — ROS2 Humble port of HKU's FAST-LIVO2 (LiDAR-inertial-**visual**, T-RO 2024) for MID360 + fisheye cam; adds vikit fisheye support. Needs Sophus 1.22.10, OpenCV ≥4.2; FAST-Calib for extrinsics. Heaviest compute; only if you add a camera (*demoed* on datasets).
- **LiDAR-Visual-Inertial-SLAM** (valentinomario) — the most directly relevant reference build: LVI-SLAM **on Jetson Orin NX**, ROS2 Humble, MID360 + Arducam IMX219 + the Livox built-in IMU, CUDA-accelerated, Dockerized, with VIS↔LIS cross-coupling and loop closure (Seeedstudio A603 carrier) (*demoed*).

## fixstars hands-on

The fixstars writeup is the most concrete end-to-end MID360+ROS2 bring-up: custom 3-wire cable from the Quick Start pinout, Livox-SDK2 v1.0.1 + livox_ros_driver2 v1.1.1, `livox_lidar_quick_start` SDK smoke test, then rviz. **ROS2 build gotcha they flag**: the bundled ROS2 `build.sh` defaults to a *Debug* build with no `--symlink-install`, so config/launch edits force a full rebuild — patch the command to `colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release ...` (ROS1 path already builds Release). Verified live rates: `/livox/lidar` 10 Hz default → 100 Hz with `publish_freq`, `/livox/imu` 200 Hz.

## Compute footprint on Orin

No first-party Orin numbers in sources, but the FAST-LIO2 paper benchmarks bound it. Per-scan component time (Table VII) — **Intel** i7-8550U (1.8 GHz quad, DJI Manifold 2-C): preprocessing 0.03 ms, feature-extraction 0 ms (skipped), state estimation 1.66 ms, **mapping 0.13 ms**; **ARM** Khadas VIM3 (2.2 GHz Cortex-A73 quad, 4 GB): preprocessing 0.05 ms, state estimation 4.75 ms, mapping 0.43 ms — i.e. ~5 ms/scan total on a low-power ARM quad, comfortably real-time at 10 Hz and headroom toward higher rates. Whole-pipeline per-scan totals in large/vegetation scenes were 19.6–23.9 ms on the Intel UAV computer. ikd-Tree's incremental update is what buys this: FAST-LIO1's per-scan mapping exceeded 10 ms (k-d tree rebuild) and broke real-time on large scenes; FAST-LIO2 keeps mapping well under the sampling period.

### Build notes *(synthesis)*

- The Orin's quad/octa Cortex-A78AE comfortably exceeds the VIM3 Cortex-A73 baseline; expect FAST-LIO2 to run real-time on Orin CPU alone — GPU is not required for FAST-LIO2 (it matters only for the LVI/visual variants). Reserve the GPU for downstream perception.
- For an indoor home-tidy build, override the paper's outdoor downsample (l=0.5 m) and LI-Init filter sizes toward the indoor recommendations (surf 0.05–0.15 m, map 0.15–0.25 m) — coarse voxels throw away the close-range structure you need indoors.
- Default path: spark-fast-lio (native ROS2, loop closure available) **or** the Ericsii ROS2 FAST_LIO branch, MID360 in CustomMsg mode, an IMU-unit fix (conversion node or `mean_acc_norm=1`), LI-Init once for the extrinsic, then bake the extrinsic/time-offset into the config. The valentinomario Orin repo is the closest working template if a camera is added.

## Source
- `raw/research/fast-lio-mid360-orin/01-fast-lio-ros2.md` — hku-mars/FAST_LIO ROS2 branch README (Ericsii-maintained); build/launch, CustomMsg requirement, ARM support — github.com/hku-mars/FAST_LIO/tree/ROS2
- `raw/research/fast-lio-mid360-orin/02-livox-driver2.md` — livox_ros_driver2 README; build.sh, xfer_format/publish_freq, MID360 config JSON + ports — github.com/Livox-SDK/livox_ros_driver2
- `raw/research/fast-lio-mid360-orin/03-lvi-slam-orin.md` — LiDAR-Visual-Inertial-SLAM on Jetson Orin NX (MID360 + IMX219), ROS2 Humble + CUDA + Docker — github.com/valentinomario/LiDAR-Visual-Inertial-SLAM
- `raw/research/fast-lio-mid360-orin/04-fast-livo2-ros2-mid360.md` — FAST-LIVO2 ROS2-Humble MID360+fisheye fork; deps, rosbag CustomMsg type fix — github.com/Rhymer-Lcy/FAST-LIVO2-ROS2-MID360-Fisheye
- `raw/research/fast-lio-mid360-orin/05-spark-fast-lio.md` — MIT-SPARK spark-fast-lio (FAST-LIO2 on ROS2 + KISS-Matcher-SAM loop closure) — github.com/MIT-SPARK/spark-fast-lio
- `raw/research/fast-lio-mid360-orin/06-fast-lio-slam.md` — FAST_LIO_SLAM = FAST-LIO + Scan-Context/GTSAM pose-graph loop closure — github.com/gisbi-kim/FAST_LIO_SLAM
- `raw/research/fast-lio-mid360-orin/07-lidar-imu-init.md` — hku-mars/LiDAR_IMU_Init (LI-Init, IROS 2022) target-free extrinsic+temporal calibration; params, units — github.com/hku-mars/LiDAR_IMU_Init
- `raw/research/fast-lio-mid360-orin/08-fast-lio2-arxiv.md` — FAST-LIO2 paper (arXiv 2107.06829); iEKF, ikd-Tree, per-scan timing on Intel/ARM — arxiv.org/abs/2107.06829
- `raw/research/fast-lio-mid360-orin/09-fixstars-mid360.md` — Fixstars hands-on MID360+ROS1/ROS2 bring-up; networking, build.sh Debug gotcha, verified rates — blog.us.fixstars.com/trying-out-the-livox-mid-360-with-ros1-ros2
- `raw/research/fast-lio-mid360-orin/10-nexty-mid360-imu.md` — nexty-ele on MID360 built-in IMU g→m/s² conversion node for ROS2 + FAST-LIO — nexty-ele.com/en/technical-column/livox_07
- `raw/research/fast-lio-mid360-orin/11-point-lio-mid360.md` — Point-LIO-Mid360 fork; high-rate point-wise LIO, saturation params, IMU-units note — github.com/overloadsc/Point-LIO-Mid360

## Related
- [[lidar-for-uav-autonomy]]
- [[home-tidy-drone-prototype]]
- [[indoor-cluttered-slam]]
- [[visual-inertial-slam]]
- [[drone-sensors-for-autonomy]]
- [[gps-denied-hover-land]]
- [[slam-fc-integration]]
- [[nano-drone-compute]]
- [[indoor-obstacle-avoidance]]
- [[drone-autonomy-state]]
- [[lidar-vs-vision-autonomy]]
