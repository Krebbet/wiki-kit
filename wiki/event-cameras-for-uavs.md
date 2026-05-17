# Event Cameras for UAVs

2026 PMC PRISMA systematic review of 129 papers (2015–2025) on event-camera use specifically on UAV platforms. All demonstrated results are from controlled or semi-controlled environments unless noted; real-world outdoor validation remains a critical gap. For sensor physics and hardware taxonomy see [[event-cameras]]; this page covers UAV application tasks, dataset map, and neuromorphic-on-drone results. [[eth-rpg-scaramuzza]] is the dominant contributing institution across the reviewed corpus.

## Task Taxonomy and Maturity

All results *demoed* (mostly controlled):

**VO/SLAM**
- EVO, Ultimate SLAM (events + frames + IMU): 0.8° rotation error, 2% translation error.

**Obstacle Avoidance**
- Dynamic: 3.5 ms latency on quadrotor (*demoed*, [[eth-rpg-scaramuzza]]).
- Static: sub-ms latency on ornithopter.

**GPS-Denied / Terrain-Relative Navigation**
- NeuroSLAM: GPS-denied flight, controlled environment.

**Inspection and Anomaly Detection**
- ev-CIVIL event-based civil infrastructure inspection.
- SNN on Intel Loihi: 65–135× more energy-efficient than frame-based baseline, 6–10% accuracy drop accepted as tradeoff (*demoed*).

**Object Tracking**
- +39.3% accuracy over frame cameras in harsh lighting conditions (*demoed*).

**High-Speed Maneuvering**
- Fully neuromorphic vision→control flown on a quadrotor at 200 Hz (*demoed*, indoor only). **Correction (primary source):** the figure previously given here as "~0.94 W total" is the Intel Loihi *board idle* power; the spiking network's marginal cost is only **7–12 mW**, and the canonical figure is **27 µJ/inference** — 3–4 orders of magnitude less energy/inference than a Jetson Nano. See [[neuromorphic-computing-for-drones]] for the primary (de Croon et al., Science Robotics 2024).

**Full onboard neuromorphic perception→actuation loop** — *speculated*; hardware-limited, no shipping system yet.

## Dataset Map

| Dataset | Platform | Notes |
|---|---|---|
| MVSEC | Hexacopter | Multi-vehicle stereo event camera |
| UZH-FPV | Racing drone | [[eth-rpg-scaramuzza]]; drone racing scenes |
| EED | UAV | — |
| EVDodgeNet / MOD | Quadrotor | Dynamic obstacle avoidance |
| EV-IMO / EVIMO2 | Ground + UAV | Moving object segmentation |
| DSEC | Ground vehicle | LiDAR ground-truth; used for cross-modal eval |

Simulators: ESIM (event-specific), XTDrone, AirSim. No standardized cross-dataset metrics exist — a standing methodological gap.

## Gaps

- No standardized evaluation metrics across papers.
- Weak real-world / outdoor validation; most results are indoor or structured outdoor.
- No edge hardware enabling full onboard neuromorphic perception-to-actuation pipeline at flight-relevant scale.

## Source
- `raw/research/autonomy-and-sensors/06-event-vision-uav-review.md` — 2026 PMC PRISMA systematic review, 129 papers 2015–2025, UAV-specific event-camera applications

## Related
- [[event-cameras]] — sensor physics, hardware specs, general algorithm families
- [[eth-rpg-scaramuzza]] — dominant lab; source of UZH-FPV dataset and most demoed avoidance results
- [[visual-inertial-slam]] — competing/complementary navigation baseline
- [[drone-autonomy-state]] — overall deployment maturity context
- [[lidar-vs-vision-autonomy]] — where neuromorphic results feed the vision camp
