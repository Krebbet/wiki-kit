# SLAM/VIO → Flight-Controller Integration

How an off-board SLAM/VIO pose estimate gets fused into a flight controller's state estimator: the MAVROS `vision_pose` bridge, the MAVLink vision messages, ENU↔NED frame handling, EKF source selection, and the latency/divergence failure modes you tune around. Build reference for an ArduPilot/PX4 + companion-computer indoor stack.

## The Pipeline (companion → MAVROS → FCU)

Canonical chain for a [[home-tidy-drone-prototype|Phase-1 indoor build]]: SLAM/VIO node (e.g. `realsense-ros` for a T265, or a [[visual-inertial-slam|VI-SLAM]]/[[fast-lio-mid360-orin|LiDAR-odometry]] stack) publishes pose on `/tf` → `vision_to_mavros` transforms it → publishes `/mavros/vision_pose/pose` → MAVROS handles the ENU→NED conversion and emits a MAVLink vision message → the FCU's EKF fuses it as an external-nav source (ArduPilot ROS-VIO page, 04). The same MAVROS `vision_pose` plugin serves both ArduPilot and PX4.

Three nodes run concurrently on the companion: the sensor/SLAM node, `mavros`, and `vision_to_mavros` (04, 09). Verify with `rostopic echo /mavros/vision_pose/pose` (data present), `rostopic hz` (T265 example: ~30 Hz), and the FCU-side MAVLink Inspector showing `VISION_POSITION_ESTIMATE` arriving (04).

## MAVROS vision_pose plugin and MAVLink messages

`mavros_extras` provides the relevant plugins (08):
- **`vision_pose`** — *Send vision pose estimate to FCU.* Subscribes `/mavros/vision_pose/pose` (`geometry_msgs/PoseStamped`).
- **`vision_speed`** — *Send vision speed estimate to FCU.*
- **`odom`** — *Send odometry to FCU from another estimator* (`nav_msgs/Odometry`, `/mavros/odometry/out`).
- **`mocap_pose_estimate`** — feeds `ATT_POS_MOCAP`; *currently not used by the FCU* (08) — route MoCap through `vision_position` instead.
- **`fake_gps`** — *Sends fake GPS from local position estimation source data (motion capture, vision) to FCU.*

ArduPilot ingests external pose via `VISION_POSITION_ESTIMATE` (04). PX4's plugin path: `/mavros/vision_pose/pose` → MAVLink → `vehicle_visual_odometry` uORB topic (06). PX4 does **not** support `GLOBAL_VISION_POSITION_ESTIMATE`, `VISION_SPEED_ESTIMATE`, or `VICON_POSITION_ESTIMATE` (06). For PX4-EKF2 only the "vision" pipelines work; MoCap `geometry_msgs/PoseStamped` must be remapped to `/mavros/vision_pose/pose`, and a `nav_msgs/Odometry` source to `/mavros/odometry/out` with correct `frame_id`/`child_frame_id` (06).

Note (1MB-flash limitation): boards <2MB flash support `GPS_INPUT` but not `GLOBAL_VISION_POSITION_ESTIMATE`, so they must run external nav via the `GPS_INPUT` message instead (01).

## Frame conventions: ENU↔NED / FLU↔FRD

ROS uses ENU world / FLU body by REP-105; the FCUs use NED world / FRD body (06). The split MAVROS handles vs. what you must pre-rotate:

- **MAVROS does the ENU→NED conversion** on the wire. Publish pose to `/mavros/vision_pose/pose` in ROS ENU and MAVROS converts to NED before sending to ArduPilot (04) / PX4 (06).
- **You must pre-align the sensor's own frame** to the ENU body/world convention before MAVROS — that is exactly what `vision_to_mavros` does. It listens to `/tf`, transforms `source_frame_id`→`target_frame_id`, then rotates the body frame to ENU using `roll_cam`, `pitch_cam`, `yaw_cam` and a `gamma_world` Z-rotation between world frames, publishing a single `geometry_msgs/PoseStamped` at `output_rate` (09).
- PX4 names the external reference frame `MAV_FRAME_LOCAL_FRD` because its heading generally won't match the EKF's; if your source frame differs you attach it to the tf tree (`odom`/`odom_frd`, `base_link`/`base_link_frd`) via `static_transform_publisher`, and ensure no other node publishes that same transform or the tf tree breaks (06). The quick MoCap recipe: swap axes to NED — `x_mav=x_mocap, y_mav=z_mocap, z_mav=-y_mocap`, keep quaternion `w`, swap vector part identically (06).

Camera-orientation params (ROS2 fork, T265, 10): front-facing default `roll_cam=0, pitch_cam=0, yaw_cam=0, gamma_world=-π/2`; down-facing adds `pitch_cam=-π/2`. Down-facing has a known T265 yaw-init bug (librealsense #4080) — tilt the nose up slightly when launching `realsense-ros` or initial yaw randomizes (04, 10).

## ArduPilot: EKF3 external nav and source-set switching

Modern ArduPilot uses **EKF3** with `EK3_SRCn_*` source sets (02). External nav is selected per-quantity:
- `EK3_SRC*_POSXY=6` (ExternalNav), `EK3_SRC*_VELXY=6`, `EK3_SRC*_VELZ=6`, `EK3_SRC*_YAW=6`; `POSZ` typically left `1` (baro) (02, 03).
- Option 6 (ExternalNav) is the "companion device provides position/yaw" case for POSXY/YAW (02).

**Source switching** — three sets exist; SRC1 is default. Switch via RC aux function 90 ("EKF Source Set"), via `MAV_CMD_SET_EKF_SOURCE_SET` (no GCS implements it), or via Lua scripts that react to GPS accuracy / EKF innovations. `ahrs-source.lua` switches GPS↔T265↔optical-flow (03). Source changes log Events 85/86/87 and the `XKFS.SS` field shows the active set per core (03).

**GPS / non-GPS transitions** — standard recipe is SRC1=GPS, SRC2=ExternalNav, disable `EK3_SRC_OPTIONS` FuseAllVelocities (=0), require `EK3_ENABLE=1`, `EK2_ENABLE=0`, `AHRS_EKF_TYPE=3` (03).

**Origin** — incoming external pose is not fused until the EKF origin/home is set. Send `SET_GPS_GLOBAL_ORIGIN` + `SET_HOME_POSITION` (Mission Planner: Set Home Here → Set EKF Origin; or `set_origin.py` via pymavlink) (04, 05). ArduPilot 4.7+ can auto-persist/restore the origin across power cycles: `AHRS_OPTIONS` bit 3 (RecordOrigin) saves to `AHRS_ORIGIN_LAT/LON/ALT`; bit 4 (UseRecordedOriginForNonGPS) restores on boot when GPS isn't used — removes the per-boot manual-origin step for indoor flight (01).

### Version caveat (EKF2 → EKF3)
The older ArduPilot ROS-VIO (04) and Hector-SLAM (05) pages predate EKF3 external-nav support and instruct `AHRS_EKF_TYPE=2` / EKF2 (`EK2_GPS_TYPE=3`, compass off, look for "EKF2 IMU is using external nav data"). The current source-selection / transitions pages (02, 03) document EKF3 ExternalNav as the supported path. *(synthesis)* For a new build, follow EKF3 `EK3_SRC*=6`; treat the EKF2 instructions in 04/05 as legacy.

## PX4: EKF2 external position estimation

EKF2 is PX4's default and preferred estimator (LPE is deprecated) (06, 07). To fuse external vision:
- Set the EKF2 fusion bits for *horizontal position*, *vertical vision*, *velocity*, *yaw* per desired model; `EKF2_HGT_REF=Vision`; set `EKF2_EV_POS_X/Y/Z` lever arms; optionally disable GNSS/baro/range via `EKF2_GPS_CTRL`/`EKF2_BARO_CTRL`/`EKF2_RNG_CTRL` (06, 07).
- **Message rate** must be 30–50 Hz (30 if covariances included); too slow and EKF2 won't fuse (06).
- EKF2 subscribes only to `vehicle_visual_odometry` (`ODOMETRY` with `MAV_FRAME_LOCAL_FRD`, or `ATT_POS_MOCAP`); linear-velocity fusion from the odometry message is EKF2-only (06).
- A VIO ROS node should publish `nav_msgs/Odometry` to `/mavros/odometry/out` and a `CompanionProcessStatus` (comp id 197) to `/mavros/companion_process/status` — twist must be in **body frame** (06, 07).
- Local→global: `SET_GPS_GLOBAL_ORIGIN` lets EKF2 produce a global estimate so auto modes (Mission/Return/Land/Hold/Orbit), which require global position, work indoors (06).

## Latency tuning and divergence pitfalls

**Delay is the dominant tuning knob.** PX4 `EKF2_EV_DELAY` = vision timestamp vs. IMU capture-time offset; technically 0 with true timestamping + timesync (NTP), but in practice empirically tuned — "rare that a system is set up with an entirely synchronised chain." Estimate from logs by offsetting IMU-rate vs EV-rate peaks (enable `SDLOG_PROFILE` bit 7), then minimize EKF innovations during dynamic maneuvers (06, 07).

**ArduPilot EKF3 external-nav delay** is measured the same way: a discourse method sets `LOG_DISARM=1`, sets an EKF origin, then jerks the drone back-and-forth and measures the time offset between `IMU.AcceX` peaks and the external-nav estimated-velocity (North) peaks (NKF3); the author expects a ~20–40 ms constant delay (11). *(synthesis)* This delay maps to ArduPilot's external-nav delay parameter the way `EKF2_EV_DELAY` does for PX4.

**Known failure modes:**
- **GPS↔ExternalNav position jump** — on switching *from* T265 *to* GPS you will see a position jump, but **not** GPS→T265, because ExternalNav position is continuously slaved to GPS while GPS is the primary set (03). After any source switch, wait ~10 s and confirm the EKF stays healthy (white EKF HUD label) (03). *(synthesis)* The well-known ArduPilot external-nav position-jump / EKF-divergence report (issue #27729) and the EKF3 external-nav delay discourse thread are the canonical references for this class of bug; issue #27729's specifics are not in the captured sources — verify before relying on details.
- **Drift / flyaway in flight but not when hand-carried** — vibration coupling into the camera; soft-mount the T265 (07).
- **Toilet-bowling** — camera orientation mismatch vs. the launch-file transform; verify `ODOMETRY` velocities are FRD-aligned in MAVLink Inspector (07).
- **VIO + GPS loop-closure conflict** — "really difficult, because when they disagree it will confuse the EKF"; PX4 devs report vision-velocity-only is more reliable than full vision-position alongside GPS (07).
- **Pre-flight frame check** — yaw the vehicle until the `ODOMETRY` quaternion is ~unit (w=1); if you can't without roll/pitch, you have a frame offset — do not fly (06, 07).

Low-cost IMUs drift too fast to hold position without an external velocity/position source — the external estimate is load-bearing, not optional (01).

## Build notes (this stack) *(synthesis)*

- Target EKF3 `EK3_SRC1_*=6` for a pure-indoor [[gps-denied-hover-land]] build; add SRC2 only if you also fly outdoors and want GPS↔external transitions (02, 03).
- The companion is a Jetson Orin running ROS 2, so use the **ROS2 `vision_to_mavros` fork** (Black-Bee-Drones, 10) rather than the ROS1 original (thien94, 09); same params (`roll_cam`/`pitch_cam`/`yaw_cam`/`gamma_world`), `ros2 launch` invocation.
- Source files document the T265 specifically; a LiDAR-odometry source ([[fast-lio-mid360-orin]]) publishing pose/odometry to the same `/mavros/vision_pose/pose` or `/mavros/odometry/out` topic substitutes at the MAVROS boundary — see [[lidar-vs-vision-autonomy]] for the sensor-choice tradeoff.
- Budget the 30–50 Hz pose-rate requirement against companion compute and the [[drone-power-budget]].

## Source

- ArduPilot Non-GPS Navigation landing page — origin: https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html
- ArduPilot EKF Source Selection and Switching (`EK3_SRCn_*`) — origin: https://ardupilot.org/copter/docs/common-ekf-sources.html
- ArduPilot GPS / Non-GPS Transitions (source-set recipe, position-jump note) — origin: https://ardupilot.org/copter/docs/common-non-gps-to-gps.html
- ArduPilot ROS + VIO tracking camera (T265, vision_to_mavros, VISION_POSITION_ESTIMATE) — origin: https://ardupilot.org/dev/docs/ros-vio-tracking-camera.html
- ArduPilot ROS + Hector SLAM for non-GPS (RPLidar, EKF2 external nav) — origin: https://ardupilot.org/dev/docs/ros-slam.html
- PX4 Using Vision/MoCap for Position Estimation (EKF2/LPE, frames, MAVROS pipelines) — origin: https://docs.px4.io/main/en/ros/external_position_estimation.html
- PX4 Visual Inertial Odometry (VIO) setup, EKF2_EV_DELAY, troubleshooting — origin: https://docs.px4.io/main/en/computer_vision/visual_inertial_odometry
- mavros_extras README (vision_pose / odom / mocap / fake_gps plugins) — origin: github.com/mavlink/mavros (ros2 branch, mavros_extras/README.md)
- thien94/vision_to_mavros (ROS1 canonical bridge) — origin: github.com/thien94/vision_to_mavros
- Black-Bee-Drones/vision_to_mavros (ROS2 fork) — origin: github.com/Black-Bee-Drones/vision_to_mavros
- ArduPilot discourse: calculating external-nav delay for EKF3 from logs — origin: https://discuss.ardupilot.org/t/calculate-the-delay-of-the-external-navigation-system-as-ekf3-inside-the-log/83095

## Related

- [[home-tidy-drone-prototype]]
- [[gps-denied-hover-land]]
- [[visual-inertial-slam]]
- [[fast-lio-mid360-orin]]
- [[indoor-cluttered-slam]]
- [[drone-autonomy-state]]
- [[drone-sensors-for-autonomy]]
- [[lidar-for-uav-autonomy]]
- [[safe-indoor-flight]]
- [[drone-power-budget]]
- [[lidar-vs-vision-autonomy]]
