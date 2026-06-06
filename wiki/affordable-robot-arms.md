# Affordable Robot Arms

Robot arm landscape for home manipulation tasks — from sub-$500 DIY to ~$10k research-grade. Framed for the home-tidying ground robot context: what can you buy for a prototype, what are the real capability limits, and where does the market sit in 2025–2026.

## Source

- `raw/research/robot-arms-affordable/04-04-aharobot-arxiv.md` — arXiv 2503.10070 (Cui et al., Tianjin U, 2025): AhaRobot — bimanual mobile manipulator, $1k–$1.8k, full BOM + results
- `raw/research/robot-arms-affordable/05-05-noribot-arxiv.md` — arXiv 2605.16537 (Li et al., Columbia, 2026): Nori Bot — sub-$1k floor-to-counter mobile manipulator, $947
- `raw/research/robot-arms-affordable/02-03-xlerobot-github.md` — github.com/Vector-Wangel/XLeRobot: XLeRobot — $660 dual-arm mobile robot, LeRobot ecosystem
- `raw/research/robot-arms-affordable/02-05-soarm100-vs-101.md` — openelab.io: SO-ARM100 vs SO-ARM101 comparison — hardware differences, ecosystems
- `raw/research/robot-arms-affordable/01-06-svrc-arm-pricing-2026.md` — roboticscenter.ai: SVRC 2026 robot arm pricing guide *(commercial source — SVRC sells OpenArm; pricing approximate)* — comprehensive tier table
- `raw/research/robot-arms-affordable/06-06-forte-arm-arxiv.md` — arXiv 2507.15693 (Chebly et al., UMass Amherst, 2025): Forte — 3D-printable 6-DOF arm, $212/unit at batch of 25

## Related

[[tidybot-deep-dive]] · [[home-tidying-robots]] · [[tactile-manipulation]] · [[onboard-grasp-perception]] · [[tidy-benchmarks]] · [[humanoid-robot-indoor-perception]] · [[system-architecture]]

---

## Full comparison table

| Arm / System | Type | DOF | Payload | Reach | Repeatability | Price (USD) | Notes |
|---|---|---|---|---|---|---|---|
| **SO-ARM100 / SO-ARM101** | Single arm (DIY) | 6 | ~100 g | ~250 mm | ~3 mm | $300–500 BOM | Feetech STS3215 servos; 3D-printed; LeRobot ecosystem; Jetson Nano/Orin Nano; beginner [src: 02-05-soarm100-vs-101.md] |
| **Forte** | Single arm (3D-print) | 6 | 0.63 kg | 467 mm | 0.467 mm avg | **$212** (batch of 25) | NEMA 17/23 steppers; capstan + belt drives; PLA structure; sub-mm repeatability; requires 3D printer + assembly; no encoder feedback [src: 06-06-forte-arm-arxiv.md] |
| **XLeRobot** | Dual-arm mobile robot | 12+ | low (SO-101 class) | ~400 mm per arm | — | **$660** | SO-100/101 arms + Lekiwi mobile base; LeRobot/VLA-ready; fixed arm height; 12+ h battery; assembles in <4 h [src: 02-03-xlerobot-github.md] |
| **Nori Bot** | Dual-arm mobile + Z-lift | 17 | ~1 kg (lift) | ~400 mm arm + 600 mm Z | — | **$947** | XLeRobot v0.4.0 + 600 mm ball-screw Z-lift; floor-to-counter reach; Raspberry Pi 4 + off-board GPU; ACT policies; qualitative demos only [src: 05-05-noribot-arxiv.md] |
| **AhaRobot** | Bimanual mobile + Z-lift | 16 | 1.5 kg per arm | 750 mm + 1250 mm Z | 0.7 mm | **$1,000–$1,800** | Feetech STS3215; ROS 2 Humble; RTX4060 onboard; 80–100% task success (imitation learning, 10-trial eval); fully open-source CAD + code [src: 04-04-aharobot-arxiv.md] |
| Dobot MG400 | Single arm | 4 | 750 g | 440 mm | 0.05 mm | $3,000 | Desktop; limited ROS support [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |
| WidowX-250 S2 | Single arm | 6 | 250 g | 250 mm | 1 mm | $3,100 | Dynamixel; ALOHA leader arm standard [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |
| OpenArm | Single arm | 6 | 1.5 kg | 550 mm | 0.1 mm | $3,500 | ROS2 native; AI data collection focus [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC product)* |
| xArm 5 Lite | Single arm | 5 | 3 kg | 700 mm | 0.1 mm | $4,500 | Popular research pick; Python SDK [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |
| ViperX-300 S2 | Single arm | 6 | 750 g | 300 mm | 1 mm | $4,800 | ALOHA follower arm standard; Dynamixel [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |
| xArm 6 | Single arm | 6 | 5 kg | 700 mm | 0.1 mm | $8,000 | Best cost/payload in research tier [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |
| xArm 7 | Single arm | 7 | 3.5 kg | 700 mm | 0.1 mm | $12,000 | TidyBot++ reference arm [src: tidybot-deep-dive] |
| Kinova Gen3 Lite | Single arm | 6 | 0.5 kg | 760 mm | 0.1 mm | $13,500–$18,000 * | Force control; polished SDK [src: 06-06-forte-arm-arxiv.md, 01-06-svrc-arm-pricing-2026.md] |
| Kinova Gen3 | Single arm | 7 | 4 kg | 902 mm | 0.1 mm | $28,000 | Torque sensing every joint; TidyBot v1 reference arm [src: tidybot-deep-dive, 01-06-svrc-arm-pricing-2026.md] |
| Franka FR3 | Single arm | 7 | 3 kg | 855 mm | 0.1 mm | $25,000–$30,000 | Torque sensing every joint; research standard [src: 01-06-svrc-arm-pricing-2026.md] *(SVRC)* |

*\* Price conflict: Forte paper (arXiv) cites $13,500; SVRC guide cites $18,000. Both marked as approximate.*

---

## Tier 1 — Sub-$1,000: DIY and open-source systems

### SO-ARM100 / SO-ARM101 ($300–500 BOM)

The foundation of the LeRobot/Hugging Face manipulation ecosystem [src: 02-05-soarm100-vs-101.md]. Single 6-DOF arm using Feetech STS3215 servos (1:345 gear ratio throughout on ARM100; mixed ratios on ARM101 for better per-joint performance). 12-bit magnetic encoder. 3D-printed structure; requires 3D printer and soldering skills.

SO-ARM100 vs SO-ARM101 differences [src: 02-05-soarm100-vs-101.md]:
- ARM100: uniform 1:345 gear ratio across all joints; known joint-3 disconnection issue; recommended compute: Jetson Nano 4GB; beginner target
- ARM101: mixed ratios (1:345 / 1:191 / 1:145 per joint); improved range of motion; recommended compute: Orin Nano 4GB; PCIe Gen4 / USB-C connectivity; developer target
- Both: 12-bit magnetic encoder; 0°–40°C operating temp; compatible with LeRobot training pipeline (PyTorch, ACT, imitation learning)

**Capability ceiling:** ~100 g payload. Suitable for tabletop pick-and-place and data collection for imitation learning. Not suitable for production or heavy objects.

### Forte arm ($212/unit at batch of 25)

6-DOF, 3D-printable, NEMA 17/23 stepper-driven arm [src: 06-06-forte-arm-arxiv.md]. Key specs: 0.63 kg payload (validated), 467 mm reach, 0.467 mm average repeatability, 3.5 kg total weight. Uses capstan drives for shoulder joints (high torque via cable + pulley) and belt/gear drives elsewhere. Structure is topology-optimized PLA (FoS 4.38 upper arm, 1.57 forearm). Arduino Uno + A4988/TB6600 stepper drivers; 24V supply; no encoder feedback (open-loop stepper).

Batch pricing: $212.40/unit at 25 units; single-unit cost would be higher. Requires 3D printer, assembly time. Authors note no custom control board yet. *(synthesis: the Forte demonstrates that $200 in materials + open-loop steppers can achieve sub-mm repeatability for light payloads; it's a build-vs-buy data point, not a buy option.)*

### XLeRobot ($660 complete system)

Dual-arm mobile robot: two SO-100/101 arms on a Lekiwi differential-drive mobile base [src: 02-03-xlerobot-github.md]. Assembles in under 4 hours. 12+ hour battery life (8 h intensive). Control: keyboard, Xbox controller, Switch Joy-Con, or Meta Quest 3 VR (all Bluetooth). LeRobot/VLA-ready — pre-trained policy download and RL sim-to-real supported. Optional: stereo head camera (+$30), RealSense RGBD (+$220).

**Known limitations** [src: 02-03-xlerobot-github.md]: low payload; ~40 cm arm reach; fixed arm height; requires Python/Ubuntu/GitHub familiarity. Price excludes 3D printing, tools, shipping, taxes.

### Nori Bot ($947)

XLeRobot v0.4.0 + a custom 600 mm Z-axis ball-screw lift [src: 05-05-noribot-arxiv.md]. This is the key addition: two HGR20 600 mm linear rails + RM1605 ball screw (16 mm dia, 5 mm lead), driven by one additional STS3215 servo on the same half-duplex bus. Result: floor-to-counter reach without custom arm geometry.

Compute: Raspberry Pi 4 (1 GB) on-robot for motor I/O only; heavy compute off-board. Agent runtime: OpenClaw (cron jobs → physical tasks). Policies: ACT via LeRobot. Force sensing: normalized current readback from Present_Current register per servo (sensorless; ~6.5 mA/raw unit). Protection stack: calibration clamping, stall detector, EEPROM firmware limits — 0 servo burn-outs over 4 weeks post-deployment (vs 2 lost servos before).

**Demonstrated tasks** (qualitative — no controlled n-trial data in paper): book re-shelving, floor trash pickup, laundry sorting, cloth folding, autonomous morning coffee. Per-step agent latency ~1.9 s median. ACT inference ~10 Hz.

**Limitations** [src: 05-05-noribot-arxiv.md]: no controlled success-rate data published yet; Z-axis is slow; thin-client ~2.4 s startup latency; only right arm used for learned policies; 30 demos per skill (below ACT's recommended 50+); code/CAD not yet released.

---

## Tier 2 — $1,000–$2,000: Research bimanual

### AhaRobot ($1,000–$1,800)

The most capable open-source sub-$2k system [src: 04-04-aharobot-arxiv.md]. Bimanual mobile manipulator: two SCARA-like arms (4 modules each, dual STS3215 anti-backlash per joint) on a differential-drive base with belt-driven vertical Z-axis (1250 mm stroke). 16 total DOF. 1.5 kg payload per arm, 750 mm reach (X-Y), 0.7 mm repeatability (±3σ, dial indicator). 51 kg total weight.

Hardware BOM cost: $1,000 (no compute) / $1,800 (with Mini-ITX, Intel i5-12700KF, RTX4060). 4–5 h battery life (24V/20Ah LiPo for actuators; 1 kWh portable AC for compute). Three webcams (head pan-tilt + 2 wrist-mounted). ROS 2 Humble throughout; five ESP32 MCUs for low-level control; ODrive 3.6 for base BLDC.

**Demonstrated results** — imitation learning with ACT / π0 [src: 04-04-aharobot-arxiv.md]:

| Task | Demos | Best avg success |
|---|---|---|
| Box Transfer | 50 | 10/10 |
| Can Pressing | 50 | 8/10 |
| Pen Insertion | 50 | 6/10 |
| Floor-to-table Pick | 80 | 7/10 |
| Table Cleaning | 200 | 7–9/10 |
| Pan Sweeping | 200 | 5–8/10 |

RoboPilot teleoperation: 100% success on 3 tested fine-grained tasks; 30% faster than SpaceMouse; $50 workstation vs $1,500 Meta Quest Pro with comparable policy performance.

**Platform comparison** (from AhaRobot paper, Table 1):

| Platform | Price | Dual | Mobile | Floor reach | Open |
|---|---|---|---|---|---|
| Mobile ALOHA | $32,000 | Y | Y | N | Y |
| AgileX COBOT | ~$30,000 | Y | Y | N | N |
| XLeRobot | $660 | Y | Y | N | Y |
| **AhaRobot** | **$1,000–1,800** | **Y** | **Y** | **Y** | **Y** |

AhaRobot is described as "roughly 1/15 the cost of popular platforms" with the only open-source combination of dual arms + mobile base + floor reach [src: 04-04-aharobot-arxiv.md].

**Limitations** [src: 04-04-aharobot-arxiv.md]: 51 kg weight; no collision sensing; compute power draw requires portable AC supply; pan-sweeping success limited by action-chunking discontinuities.

---

## Tier 3 — $3,000–$10,000: Prosumer / research entry

| Arm | Payload | Reach | Price | Best for |
|---|---|---|---|---|
| Dobot MG400 | 750 g | 440 mm | $3,000 | Desktop structured tasks; limited ROS |
| WidowX-250 S2 | 250 g | 250 mm | $3,100 | ALOHA leader arm; Dynamixel ecosystem |
| OpenArm | 1.5 kg | 550 mm | $3,500 | AI data collection; ROS2 native *(SVRC product)* |
| xArm 5 Lite | 3 kg | 700 mm | $4,500 | Payload-first research needs |
| ViperX-300 S2 | 750 g | 300 mm | $4,800 | ALOHA follower arm; TidyBot++ supported |
| xArm 6 | 5 kg | 700 mm | $8,000 | Best cost/payload in research tier |

See [[tidybot-deep-dive]] for xArm 7 ($12k), Kinova Gen3 ($28k), and Franka FR3 ($25–30k) in context of TidyBot++.

---

## Project relevance *(synthesis)*

For the home-tidying ground robot prototype, the arms divide into two decisions:

**Data collection / proof-of-concept (Phase 1):** XLeRobot ($660) or AhaRobot ($1,000–$1,800) are the only platforms that provide dual-arm + mobile base + floor reach in an open-source build. XLeRobot has no Z-axis; Nori Bot ($947) adds 600 mm lift but is still a research pre-release. AhaRobot is the most validated at time of writing: 7–10/10 success on 6 manipulation task categories with 50–200 demos, open-source CAD + code, ROS 2 Humble.

**Product-path arm (Phase 2):** TidyBot++ research used xArm 7 / Kinova Gen3 at $8–28k. The xArm 6 at $8k is the most cost-effective research-to-product bridge: 5 kg payload, 700 mm reach, 0.1 mm repeatability — twice the payload of xArm 7 at 65% of the price. See [[tidybot-deep-dive]] for the TidyBot++ base design ($5.4k) which already integrates several of these arms.

**Open architecture question:** All sub-$2k systems use Feetech STS3215 servos (plastic gears, 1:345 reduction, ~35 N·cm holding torque). This servo is the mechanical bottleneck — fragility under repeated high-torque use, limited payload headroom, no factory encoder. AhaRobot's dual-motor anti-backlash configuration compensates but adds complexity. Moving above $3k brings metal gearboxes and closed-loop control.

**Force sensing:** The Nori Bot approach (current readback from STS3215's Present_Current register, normalized) is the cheapest path to any grip-force feedback — no additional sensors, piggybacked on the existing motor bus. AhaRobot has no force sensing. Both contrast with Franka FR3 / Kinova Gen3 which have torque sensing at every joint. See [[tactile-manipulation]] for the DIGIT/GelSight approach for high-fidelity contact sensing if needed.
