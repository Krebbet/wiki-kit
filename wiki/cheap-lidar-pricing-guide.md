# Cheap LiDAR Pricing Guide — Tidy Bot

Pricing tiers and sensor selection logic for a commercially viable indoor home-tidying ground robot. Covers 2D LiDAR (navigation layer), 3D LiDAR (full-obstacle-avoidance layer), and LiDAR-free depth alternatives. All prices USD retail unless noted.

## Source

- `raw/research/cheap-lidar/08-unitree-l1-shop.md` — Unitree shop (confirmed $249 price, 2026-06-01)
- `raw/research/cheap-lidar/03-robotika-unitree-l1-review.md` — Independent hands-on L1 review (Robotika.cz, 2024)
- `raw/research/cheap-lidar/07-unitree-l1-specs.md` — L1 specs (4gltemall reseller)
- `raw/research/cheap-lidar/02-openelab-3d-lidar-comparison.md` — Livox Mid-360 vs Hesai JT16 vs RoboSense E1R (OpenELAB blog, 2025; E1R bias)
- `raw/research/cheap-lidar/07-hesai-jt16-ces-announcement.md` — Hesai JT16 CES 2025 announcement
- `raw/research/cheap-lidar/08-hesai-jt16-specs.md` — Hesai JT16 official specs
- `raw/research/cheap-lidar/04-kaiaai-2d-lidar-list.md` — Community 2D LiDAR list (kaiaai/awesome-2d-lidars, 31 models)
- `raw/research/cheap-lidar/05-budget-lidar-under-100.md` — Budget 2D LiDAR comparison (Industrial Monitor Direct)
- `raw/research/cheap-lidar/06-rplidar-c1-specs.md` — RPLIDAR C1 official spec page (SLAMTEC)

## Related

[[home-tidy-drone-prototype]] · [[2d-lidar-slam]] · [[robot-vacuum-navigation]] · [[lidar-for-uav-autonomy]] · [[close-range-depth-sensors]] · [[lidar-vs-vision-autonomy]]

---

## Pricing table

| Model | Type | FOV | Range | Pts/sec | Weight | Price (USD) |
|---|---|---|---|---|---|---|
| Vacuum LDS salvage (LDS-006, LDS-01RR, Neato XV-11) | 2D triangulation | 360° | ~3–8 m | ~1–2 KHz | ~100–180 g | ~$16 used [src: kaiaai-2d-lidar-list — community library notes] |
| YDLIDAR X3 | 2D triangulation | 360° | 0.12–8 m | 3 KHz | 135 g | ~$65 [src: kaiaai-2d-lidar-list] |
| YDLIDAR X4 | 2D triangulation | 360° | 0.12–10 m | 5 KHz | 180 g | ~$70–90 [src: kaiaai-2d-lidar-list, budget-lidar-under-100] |
| LDROBOT D500 | 2D dToF | 360° | 0.2–30 m | — | 120 g | ~$70–90 [src: budget-lidar-under-100] |
| RPLIDAR A1 | 2D triangulation | 360° | 0.2–12 m | 8 KHz | — | ~$99 [src: budget-lidar-under-100] |
| RPLIDAR C1 | 2D DTOF fusion | 360° | 0–12 m | 5 KHz | — | ~$94–96 (Amazon/Waveshare) |
| RPLIDAR A2M8 | 2D triangulation | 360° | 0.15–18 m | 16 KHz | — | ~$189 [src: budget-lidar-under-100] |
| **Unitree L1 PM/RM** | **3D TOF** | **360°×90°** | **20 m / 30 m** | **43,200 (pts/scan)** | **230 g** | **$249** [src: unitree-l1-shop] |
| Unitree L2 | 3D TOF | 360°×90°+ | 30 m | 64,000 | — | $419 [src: unitree-l1-shop] |
| Hesai JT16 | 3D, 16-ch | 360°×40° | 30 m / 100 m max | 690 KHz dual | <200 g | Contact sales [src: hesai-jt16-specs] |
| Livox Mid-360 | 3D solid-state | 360°×59° | 40 m | 200 KHz | 265 g | ~$480–550 (AliExpress 2025) / $749 retail [src: [[lidar-for-uav-autonomy]]] |

---

## Tier analysis *(synthesis)*

### Tier 1 — Sub-$100: 2D only (YDLIDAR X4, LDROBOT D500, RPLIDAR A1/C1)

For a **commercial product at $500–$800 retail**, this is the only viable LiDAR price band. Robot vacuums (Roomba, Roborock) ship with sensors in this tier as the primary navigation layer, supplemented by a separate ToF/structured-light collision layer (see [[robot-vacuum-navigation]]). Key tradeoffs:

- 2D planar scan only: detects walls and furniture legs but misses table tops, raised obstacles, floor-level clutter unless supplemented
- YDLIDAR X4 and D500 are the two standouts under $90 with ROS2 drivers and adequate indoor range (10–30 m, all far more than a home environment requires)
- LDROBOT D500 (dToF) outperforms triangulation-based peers on reflective/glossy surfaces — relevant for hardwood/tile floors
- RPLIDAR C1 (DTOF fusion) at ~$95 adds reflectivity data and "2.5D" output — fills the gap between A1 and S-series; targets home robots explicitly [src: rplidar-c1-specs]
- Vacuum LDS salvage at ~$16 is technically viable with community reverse-engineered ROS2 drivers (kaiaai/LDS library supports LDS-006, LDS-01RR, Neato XV11) but not appropriate for a production product — use for prototyping only

### Tier 2 — $249: Entry 3D (Unitree L1)

The **Unitree L1** at $249 is the key new entrant. Unitree explicitly targets "sweeping robots" and whole-house 3D scanning as primary use cases [src: unitree-l1-specs]. Key facts from sources:

- 360°×90° FOV; single TOF sensor on a dual-axis rotating head — mechanically simple [src: robotika-unitree-l1-review]
- 43,200 pts/scan, 11 Hz; non-repetitive (non-synchronized axes, so consecutive scans cover different regions) [src: robotika-unitree-l1-review]
- 0.05 m minimum detection distance — catches close objects [src: unitree-l1-specs]
- Onboard IMU included [src: robotika-unitree-l1-review]
- Power: 6 W at 12 V — needs DC-DC converter for battery-powered mobile robot [src: unitree-l1-specs]
- SDK: binary static library + MAVLink v2 protocol; independently reverse-engineered successfully by Robotika.cz [src: robotika-unitree-l1-review]
- **Reliability concern**: 2 out of 3 units worked out-of-box in independent test; USB-TTL converter (CP2104) was the failure point; Unitree does not supply spare parts [src: robotika-unitree-l1-review]
- **SDK longevity risk**: binary SDK; precedent of other robotics companies going bankrupt and leaving binary SDKs inoperable [src: robotika-unitree-l1-review]
- Price dropped from $349 (late 2024 review) to $249 (June 2026 shop) [src: robotika-unitree-l1-review vs unitree-l1-shop]

*(synthesis)* For a **$1,000–$2,000 retail tidy bot**, the L1 at $249 unlocks true 3D coverage (no supplemental ToF needed for vertical obstacle detection) while staying below the cost floor of previous 3D LiDAR options. This is the recommended sensor for Phase-1 ground-robot prototyping.

### Tier 3 — $419+: Higher-spec 3D (Unitree L2, Hesai JT16, Livox Mid-360)

- **Unitree L2** ($419): upgraded L1; longer range, higher point rate. Not yet independently reviewed
- **Hesai JT16** (contact sales, no public price): compact (55 mm dia, <200 g, 4.3 W), 360°×40° FOV, 3D, IPX6. Already in shipping products (MOVA robotic lawn mower) [src: hesai-jt16-ces-announcement]. Rain/fog filtering, 0m minimum detection. For a commercial ground robot, JT16 is worth watching — the reduced vertical FOV (40° vs L1's 90°) is acceptable for a floor-bound robot. Price likely lower than L1 at volume but unconfirmed.
- **Livox Mid-360** (~$480–$550 AliExpress, $749 retail): validated for indoor complex surfaces; 200K pts/s. The right choice for UAV or where FAST-LIO2 integration matters. See [[fast-lio-mid360-orin]] and [[lidar-for-uav-autonomy]].

---

## Commercial viability cost thresholds *(synthesis)*

| Robot retail price | Max LiDAR BOM | Viable sensors |
|---|---|---|
| ~$300–600 (vacuum class) | ~$20–50 | Vacuum LDS salvage (prototype only); YDLIDAR X3 at volume |
| ~$600–1,000 | ~$50–100 | YDLIDAR X4, LDROBOT D500, RPLIDAR A1/C1 |
| ~$1,000–2,000 | ~$150–300 | Unitree L1 ($249) — **the tidy bot sweet spot** |
| ~$2,000–5,000 | ~$400–700 | Unitree L2 ($419), Hesai JT16 (volume TBD), Livox Mid-360 ($480–550) |

*(synthesis)* The vacuum precedent (Roborock shipping a full dToF LDS for <$50 BOM at scale) suggests that a mass-market tidy bot at $500–$800 retail must use a 2D LiDAR tier with a supplemental ToF collision sensor, accepting the 2D nav limitation. A premium-tier tidy bot at $1,500–$2,000 can carry a Unitree L1-class 3D sensor and achieve true 3D obstacle avoidance without supplemental sensors.

---

## Sensor comparison: 2D vs 3D for a ground tidy bot *(synthesis)*

| Capability | 2D LiDAR ($50–100) + ToF | Unitree L1 ($249, 3D) |
|---|---|---|
| Floor-plane SLAM (walls, furniture legs) | Yes | Yes |
| Ceiling/overhead obstacle detection | No | Yes (90° vertical) |
| Table-top edge detection | No | Yes |
| Stair/step detection | Marginal | Yes |
| Object-on-floor detection (shoes, toys) | Marginal | Yes (0.05 m blind zone) |
| ROS2 driver maturity | Excellent (SLAM Toolbox native) | SDK only; community ROS2 wrappers exist |
| Production reliability at scale | High (proven in 100M+ vacuums) | Unproven (2/3 units worked in one test) |
| Power draw | 1–3 W | 6 W |

---

## DIY / alternative approaches *(synthesis)*

- **Vacuum LDS salvage**: kaiaai/LDS Arduino library and kaiaai/awesome-2d-lidars list support LDS-006, LDS-01RR (Xiaomi), Neato XV-11 — all usable at ~$16 from used spares. Roborock even open-sourced a "Cullinan" LDS project for STEM. Protocol reverse-engineering is done; not production-viable but fastest path to a free SLAM prototype.
- **Open Simple LIDAR** (Hackaday.io project): <$35 BOM DIY triangulating rangefinder. Proof-of-concept only.
- **Pure vision / depth camera**: Intel RealSense D435 at ~$400 (close-range specialist; see [[close-range-depth-sensors]]). Cheaper for close-range manipulation but misses blank-wall SLAM robustness. See [[lidar-vs-vision-autonomy]].
