# Robot Arm Stage 1 — Starter Cost Breakdown

Honest cost breakdown for a Stage 1 robot arm prototype: workstation pick-and-place of known objects. Covers the full stack (arm + compute + cameras + policy), compares against research reference points (ALOHA 2, TidyBot++), and surfaces the key compute-cost shift from SmolVLA. See [[arm-prototype-roadmap]] for stage sequencing and [[affordable-robot-arms]] for the full arm tier table.

**Headline:** a workstation Stage 1 setup costs **$600–$1,500 USD** if you have a laptop. An untethered mobile version with onboard GPU comes to **$1,202**. Both figures are for hardware only — the policy ecosystem (LeRobot, SmolVLA, ACT) is free.

---

## Source

- `raw/research/arm-starter-cost/01-01-smolvla-2506-01844.md` — SmolVLA arXiv:2506.01844 (HuggingFace / CNRS, Jun 2025): 450M VLA trained on single consumer GPU, runs on CPU at inference
- `raw/research/arm-starter-cost/04-02-cutting-cord-2603-09051.md` — "Cutting the Cord" arXiv:2603.09051 (Univ. of Colorado Boulder, Mar 2026): untethered XLeRobot build with Jetson Orin Nano, full BOM at $1,202.28
- `raw/research/arm-starter-cost/02-04-yor-2602-11150.md` — YOR arXiv:2602.11150 (NYU/Berkeley, Feb 2026): sub-$10k bimanual mobile manipulator, AgileX PiPER arms, swerve drive
- `raw/research/arm-starter-cost/03-03-aloha2-2405-02292.md` — ALOHA 2 arXiv:2405.02292 (Google DeepMind/Stanford, May 2024): hardware improvements to the $20-27k bimanual research workcell
- `raw/research/arm-starter-cost/05-05-lerobot-github-readme.md` — LeRobot GitHub (HuggingFace): supported platforms, training infrastructure

---

## Cost tier table

*(All USD; hardware-only. Policy software is free/open-source.)*

| Tier | Platform | Arm(s) | Onboard compute | Policy | Total HW cost | Untethered |
|---|---|---|---|---|---|---|
| **Minimum** | SO-ARM101 leader+follower | 2× SO-ARM101 | Your existing laptop | SmolVLA or ACT | ~$600–1,000 BOM + laptop | No |
| **Cheap untethered** | Cutting the Cord XLeRobot | 2× SO-ARM101 class | Jetson Orin Nano Super ($249) | ACT 27.8 Hz / SmolVLA 1.4 Hz | **$1,202** exact | Yes |
| **Validated research single-arm** | AhaRobot (arm only, no base) | 1 arm | Mini-ITX i5 + RTX 4060 | ACT / π0 | **$1,000–1,800** | Yes (self-contained) |
| **Mid-tier mobile** | YOR | 2× AgileX PiPER ($2.5k ea.) | Raspberry Pi 5 + remote inference | ACT / Diffusion Policy (remote) | **$9,207** | Partial (inference remote) |
| **Research workcell standard** | ALOHA 2 | 2× ViperX + 2× WidowX | External GPU laptop | Diffusion Policy / ACT | ~**$20–27k** | No (tethered) |
| **Research mobile** | Mobile ALOHA | 2× ViperX + 2× WidowX + AgileX base | RTX 3070 Ti laptop | Diffusion Policy | ~**$32k** | Tethered to laptop |
| **TidyBot++ reference** | TidyBot++ (open-source base + xArm) | xArm 7 ($5.3k) or Kinova Gen3 | RTX 4080 Laptop | Diffusion Policy | ~**$13–24k** | No (laptop-tethered) |

---

## What Stage 1 actually needs (workstation, GPU already owned)

For a stationary workstation with an existing GPU machine, **compute is not a cost**. The only new spend is arm + cameras.

### Hardware (GPU already owned)
| Component | Option A (cheapest) | Option B (validated) | Cost A | Cost B |
|---|---|---|---|---|
| **Arm** | SO-ARM101 follower + leader pair | AhaRobot single arm | ~$600–800 BOM | $1,000–1,800 |
| **Camera** | USB webcam | D405 ($350) + D435 ($314) | ~$30–80 | ~$664 |
| **Compute** | Your GPU machine (USB cable to arm) | Same | $0 | $0 |
| **Grippers** | STS3215 servos built into arm | Same | included | included |
| **Force feedback** | STS3215 current register (built-in) | Same | $0 | $0 |
| **Total new spend** | **~$630–880** | **~$1,664–2,464** | | |

For Stage 1 **controlled known objects** the webcam + GPU combination is sufficient to prove the pick-and-place loop. Add D405 + D435 when grasp-pose quality becomes the bottleneck.

### Policy and training (GPU already owned = no additional cost)

ACT trains in 2–4 hours on an RTX 3090-class GPU for 50 demos — your GPU handles this already. SmolVLA (450M) trains faster (~40% vs π0) and on any consumer GPU [src: 01-01-smolvla-2506-01844.md]. Inference runs directly from your GPU machine over USB/network to the arm; no onboard compute needed for a stationary workstation.

**SmolVLA vs ACT for Stage 1:**
- ACT: 27.8 Hz inference on Jetson Orin Nano; even faster on a desktop GPU — best for rapid reactive tabletop tasks [src: 04-02-cutting-cord-2603-09051.md]
- SmolVLA: outperforms ACT on SO-101 real-world tasks (90% vs 70% in-distribution) [src: 01-01-smolvla-2506-01844.md]; async inference decouples robot control from policy computation so you're not blocked waiting for inference
- For controlled known-object pick-and-drop: both work; start with ACT (simpler, faster to debug), migrate to SmolVLA for better generalization

**Practical path:**
1. Collect 30–50 teleoperated demos via leader+follower arm pair
2. Train ACT or SmolVLA on your existing GPU (2–8 hours)
3. Run inference from your GPU machine over USB to arm
4. When you want to cut the cord for Stage 2+: add Jetson Orin Nano Super ($249) for ACT at 27.8 Hz untethered [src: 04-02-cutting-cord-2603-09051.md]

---

## Verified full BOM: Cutting the Cord untethered XLeRobot ($1,202.28)

From arXiv:2603.09051 [src: 04-02-cutting-cord-2603-09051.md] — full BOM, 2025–2026 prices:

| Subsystem | Component | Qty | Cost (USD) |
|---|---|---|---|
| Compute | NVIDIA Jetson Orin Nano Super | 1 | $249.00 |
| Compute | microSD Card | 1 | $11.23 |
| Peripherals | Anker 4-in-1 USB-C Hub | 1 | $14.99 |
| Actuation | Feetech STS-3215 Servos (12V) | 17 | $271.83 |
| Actuation | Servo Wire (50', 3-Color) | 1 | $15.97 |
| Actuation | Wonrabai Serial Bus Servo Driver Board | 2 | $21.10 |
| Power | Anker SOLIX C300 Power Station | 1 | $159.99 |
| Structure | PLA Filament (3 kg) | 1 | $45.00 |
| Structure | M3 Screws and Nuts Set | 1 | $14.99 |
| Frame | IKEA RASKOG Utility Cart | 1 | $39.99 |
| Mobility | 4" Omni Wheels | 3 | $29.97 |
| Perception | Intel RealSense D435 | 1 | $333.75 |
| Cables | USB-C to DC5521, DC5525, DC5521 car, USB-C×2 | — | $39.46 |
| **TOTAL** | | | **$1,202.28** |

This system delivers: 17 DoF, 1.0 kg/arm payload, untethered, SLAM navigation (RTAB-Map + Nav2), vision-based grasping, 98.7% pick-and-place success across 75 trials on 5 objects (17–858 g) [src: 04-02-cutting-cord-2603-09051.md].

Validated inference on Jetson Orin Nano (FP16): ACT 27.8 Hz, Diffusion Policy 1.8 Hz, SmolVLA 450M at 1.4 Hz. No thermal throttling after 30 min of peak inference load (max GPU temp 54.62°C) [src: 04-02-cutting-cord-2603-09051.md].

**Limitation**: hobby-grade STS3215 servos limit durability and payload; upgrading to industrial-grade motors increases cost 3–10× [src: 04-02-cutting-cord-2603-09051.md]. No vertical linear axis — tabletop-only [src: 04-02-cutting-cord-2603-09051.md].

---

## YOR: the $9,250 mid-tier option

From arXiv:2602.11150 [src: 02-04-yor-2602-11150.md]:

| Component | Cost |
|---|---|
| 2× AgileX PiPER arms (6-DoF, 4.2 kg each) | $5,000 ($2,500 ea.) |
| 4× REV MAXSwerve modules | $2,700 ($675 ea.) |
| Telescopic lift (standing-desk column, 63.5 cm stroke) | $165 |
| Battery + Charger | $350 |
| Raspberry Pi 5 (16 GB) | $144.50 |
| Miscellaneous (extrusions, motors, Pico, shoulder plate, etc.) | ~$848 |
| **Total** | **~$9,207** |

Key facts [src: 02-04-yor-2602-11150.md]: omnidirectional swerve base (43×34.5 cm footprint); telescopic vertical reach from floor to overhead; ZED 2i stereo head camera; iPhone wrist cameras for policy input; policy inference on remote machine via ZMQ. Autonomous recycling task: 9/10 success.

Arms dominate cost (54% of BOM). The AgileX PiPER arm ($2,500, 6-DoF) is the cheapest capable arm above the STS3215-servo tier that provides proper payload and repeatability.

---

## ALOHA 2: the research standard

From arXiv:2405.02292 [src: 03-03-aloha2-2405-02292.md]: ALOHA 2 is a stationary bimanual teleoperation workcell — 2× ViperX 6-DoF follower arms + 2× WidowX leader arms, 4× Intel RealSense D405 cameras (one per wrist + overhead + worms-eye), aluminum extrusion frame, passive gravity compensation for the leaders, ROS2 throughout.

Hardware improvements over ALOHA 1 [src: 03-03-aloha2-2405-02292.md]:
- Leader grippers: 10× less force required to open/close (from 14.68 N to 0.84 N)
- Follower grippers: 2× closing force (27.9 N vs 12.8 N)
- D405 cameras replace consumer webcams: global shutter, RGB-D, smaller wrist footprint
- Passive gravity compensation via adjustable retractors outperforms active software system (1.38 vs 0.97 shapes/min in insertion task)

Total cost: ~$20–27k total (robots + cameras + compute per web-search cross-references; BOM table not included in the arXiv preprint).

**ALOHA 2 vs Stage 1:** ALOHA 2 is a data-collection infrastructure for large-scale teleoperation, not a starting point. It uses expensive Dynamixel-based arms and professional hardware throughout. Stage 1 achieves similar per-task success (7–10/10 with ACT on AhaRobot; 98.7% pick-and-place on Cutting the Cord) at 1/15 to 1/25 the cost.

---

## Platform comparison — dual-arm mobile manipulators

From Cutting the Cord Table I [src: 04-02-cutting-cord-2603-09051.md]:

| Platform | Compute | GPU | Untethered | DoF | Payload | Est. cost |
|---|---|---|---|---|---|---|
| AhaRobot | Mini-ITX i5 | RTX 4060 | Yes | 16 | ≈1.5 kg/arm | ≈$2k |
| Mobile ALOHA | Laptop (onboard) | RTX 3070 Ti | Yes | 16 | ≈0.75 kg/arm | ≈$32k |
| TB3 Waffle Pi + arms | Raspberry Pi 4 | — | Yes | 12 | ≈0.5 kg/arm | ≈$3k |
| XLeRobot (base) | External PC | — | **No** | 15 | ≈0.8 kg | ≈$700–1k |
| **Cutting the Cord (this)** | Jetson Orin Nano | Ampere | **Yes** | 17 | 1.0 kg/arm | **≈$1.2k** |

*(Note: Cutting the Cord could not corroborate AhaRobot's cost figure independently [src: 04-02-cutting-cord-2603-09051.md]. AhaRobot's $1k–1.8k figure is from the AhaRobot paper itself [src: affordable-robot-arms].)*

---

## How our Stage 1 differs from TidyBot and ALOHA

*(Synthesis — cross-source comparison)*

| Dimension | TidyBot++ | ALOHA 2 | Stage 1 (SO-ARM101 + laptop) |
|---|---|---|---|
| **Hardware cost** | $13–24k | $20–27k | **$630–1,500** |
| **Arm** | xArm 7 ($5.3k) or Kinova Gen3 ($28k) | ViperX ($4.8k) + WidowX ($3.1k) | **SO-ARM101 pair (~$600–800)** |
| **Compute** | RTX 4080 Laptop (external, required) | GPU laptop (external, required) | **Any laptop; CPU sufficient for SmolVLA** |
| **Policy** | Diffusion Policy (~115 ms / 8.7 Hz) | ACT / Diffusion Policy | **ACT or SmolVLA (CPU deployable)** |
| **Navigation** | Holonomic base, learned | Stationary workcell | **Not needed for workstation Stage 1** |
| **Goal** | Household tidying at scale | Large-scale data collection | **Prove pick-and-place loop, generate demo data** |
| **Success rates** | 60–100% per task (10 trials) | N/A (data collection platform) | **7–10/10 on AhaRobot; 98.7% on Cutting the Cord** |

**Key structural differences:**
- TidyBot++ requires an external GPU laptop (stated architectural constraint, see [[tidybot-deep-dive]]). With SmolVLA, this is no longer necessary — inference runs on CPU or any consumer GPU [src: 01-01-smolvla-2506-01844.md].
- ALOHA 2 is a bimanual teleoperation *infrastructure* for collecting hundreds of demos per day at scale; Stage 1 needs 30–50 demos per task [src: 03-03-aloha2-2405-02292.md], achievable with a leader+follower arm pair.
- Neither TidyBot nor ALOHA addresses vertical reach without expensive mobile bases. YOR ($9,250) solves this with a $165 telescopic lift column [src: 02-04-yor-2602-11150.md].

---

## Recommended Stage 1 build (GPU already owned)

**Minimum viable (prove the loop): ~$630–880**
- 1× SO-ARM101 follower + 1× SO-ARM101 leader (~$600–800 BOM)
- 1× cheap USB webcam (~$30–80)
- Your existing GPU machine for training + inference over USB

**Validated Stage 1 (match AhaRobot results): ~$1,664–2,464**
- AhaRobot arm ($1,000–1,800) + D435 ($314) + D405 for close approach ($350)
- Your existing GPU machine; 50 demos per task; 7–10/10 expected

**Stage 1 → Stage 2 bridge (future-proof untethered): ~$1,550**
- Cutting the Cord build ($1,202) — Jetson Orin Nano already included; ACT at 27.8 Hz untethered
- Add D405 ($350) for wrist-mounted manipulation camera
- GPU machine used for training only; runtime is fully onboard

All paths use the same open-source ecosystem: LeRobot, ACT, SmolVLA, HuggingFace datasets.

---

## Related

- [[arm-prototype-roadmap]] — four-stage progression and decision framework
- [[affordable-robot-arms]] — full arm tier table with validated results
- [[tactile-manipulation]] — GelSight Mini add-on for grip quality (Phase 2 upgrade)
- [[close-range-depth-sensors]] — D405 / OAK-D SR / D435 camera selection for manipulation
- [[onboard-grasp-perception]] — OVD gap for open-vocabulary objects
- [[tidybot-deep-dive]] — TidyBot++ comparison point; external-GPU constraint documented there
