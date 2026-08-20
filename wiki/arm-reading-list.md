# Robot Arm Reading List & Buyer's Guide

Curated reading list for getting up to speed on low-cost manipulation, plus a decision-oriented capabilities breakdown. Companion to [[affordable-robot-arms]] (full spec table), [[arm-starter-cost]] (cost breakdown), and [[arm-prototype-roadmap]] (stage sequencing).

---

## Reading list

Organised by when to read, not by importance. Read Tier 1 before buying anything. Tier 2 before designing the policy pipeline. Tier 3 before planning Stage 2+.

### Tier 1 — Read first (platforms + policies)

| Paper | arXiv | Why it matters |
|---|---|---|
| **Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware** — Zhao, Kumar, Levine, Finn (ICRA 2023) | [2304.13705](https://arxiv.org/abs/2304.13705) | The paper that started the low-cost manipulation wave. Introduces ACT (Action Chunking with Transformers) and the original ALOHA leader+follower teleoperation setup. Every other paper on this list builds on it. Read this to understand what ACT is and why 50 demos is the magic number. |
| **AhaRobot** — Cui et al., Tianjin U (2025) | [2503.10070](https://arxiv.org/abs/2503.10070) | Best validated sub-$2k complete system. Full BOM, 7–10/10 success on 6 task categories, ROS 2 Humble, open-source CAD. The "can I really build this cheaply" existence proof. |
| **SmolVLA** — Shukor et al., HuggingFace/CNRS (Jun 2025) | [2506.01844](https://arxiv.org/abs/2506.01844) | 450M VLA that trains on a single consumer GPU and runs on CPU. Outperforms ACT on real SO-101 tasks (90% vs 70%). Changes the compute story: no dedicated inference GPU needed. Read this before deciding your policy stack. |
| **Cutting the Cord** — Shaw et al., Univ. of Colorado Boulder (Mar 2026) | [2603.09051](https://arxiv.org/abs/2603.09051) | Verified $1,202.28 BOM for an untethered bimanual mobile manipulator with Jetson Orin Nano onboard. Full component list, ACT at 27.8 Hz, 98.7% pick-and-place on 75 trials. The "what does $1,200 actually get you" benchmark. |

### Tier 2 — Policy and system design

| Paper | arXiv | Why it matters |
|---|---|---|
| **TidyBot++** — Wu et al., Stanford (CoRL 2024) | [2412.10447](https://arxiv.org/abs/2412.10447) | The open-source holonomic mobile base ($5.4k) + learned manipulation benchmark. Phone-based teleoperation (WebXR — no dedicated hardware). Holonomic vs differential: 9/10 vs 4/10 on the same task with identical training. The capability bar for household manipulation research. [[tidybot-deep-dive]] has the full teardown. |
| **Diffusion Policy** — Chi et al., Columbia/MIT (RSS 2023) | [2303.04137](https://arxiv.org/abs/2303.04137) | The other main policy type alongside ACT. Slower inference (1.8 Hz on Jetson vs ACT's 27.8 Hz) but often higher dexterity on contact-rich tasks. You'll hit this in every paper that mentions "imitation learning." |
| **ALOHA 2** — ALOHA 2 Team, Google DeepMind/Stanford (2024) | [2405.02292](https://arxiv.org/abs/2405.02292) | Hardware improvements to the research-standard bimanual workcell: D405 cameras (10× lower leader gripper force), passive gravity compensation, MuJoCo model. The $20–27k reference point that Stage 1 undercuts by 15–25×. |
| **Forte Arm** — Chebly et al., UMass Amherst (2025) | [2507.15693](https://arxiv.org/abs/2507.15693) | 3D-printable 6-DOF arm at $212/unit (batch of 25). 0.63 kg payload, 0.467 mm repeatability from NEMA stepper + capstan drives. Demonstrates what materials alone can achieve; useful reference if Stage 4 production cost review becomes serious. |

### Tier 3 — Specialised / Stage 2+ planning

| Paper | arXiv | Why it matters |
|---|---|---|
| **Nori Bot** — Li et al., Columbia (2026) | [2605.16537](https://arxiv.org/abs/2605.16537) | XLeRobot + 600 mm ball-screw Z-lift for $947. The cheapest way to add floor-to-counter reach. Qualitative demos only — no controlled success-rate data yet. |
| **YOR** — NYU/Berkeley (Feb 2026) | [2602.11150](https://arxiv.org/abs/2602.11150) | Sub-$10k bimanual mobile manipulator with omnidirectional swerve base + telescopic lift. AgileX PiPER arms ($2,500 each). The $9k option if Stage 2 needs real mobile reach. Full BOM in [[arm-starter-cost]]. |
| **FARM: Tactile-Conditioned Diffusion Policy** — Helmut et al. (2025) | [2510.13324](https://arxiv.org/abs/2510.13324) | GelSight Mini + diffusion policy: 0%→95% on grape picking vs vision-only, 100% on screw tightening. The argument for adding a $650 tactile sensor to your gripper. Read before Stage 2 if deformable/unknown objects are in scope. [[tactile-manipulation]] covers this. |
| **NeuralFeels** — Suresh et al., CMU (Science Robotics 2024) | [2312.13469](https://arxiv.org/abs/2312.13469) | Visuotactile SLAM: online SDF reconstruction of novel in-hand objects, 4.7 mm pose drift. Touch fills occluded geometry vision can't see. The theoretical backing for why tactile sensing matters beyond grip force. |
| **Mobile ALOHA** — Fu, Zhao, Finn, Stanford (CoRL 2024) | [2401.02117](https://arxiv.org/abs/2401.02117) | Full mobile bimanual ($32k). The "what does it look like fully deployed" reference. Tasks: cooking, laundry, cleaning. Read before designing Stage 3 aerial+arm integration. |

---

## Arm capabilities breakdown

Decision-oriented: pick your tier, then pick your arm. Full spec table with sources in [[affordable-robot-arms]].

### The one decision that matters most: servo tier

Every arm below ~$3k uses **Feetech STS3215** servos (plastic gears, 1:345 reduction, ~35 N·cm holding torque). This is the universal mechanical ceiling:
- Max useful payload: 100 g (SO-ARM101) to 1.5 kg (AhaRobot with anti-backlash dual-motor)
- Durability: fragile under repeated high-torque cycling; wear accelerates above ~50% load
- Encoders: 12-bit magnetic, adequate for imitation learning; not factory-calibrated
- Upgrade cost: industrial-grade servo replacement = 3–10× the system cost

Above $3k, you get metal gearboxes + closed-loop control. That's the real tier boundary, not the price itself.

### Tier table: what you actually get

| Arm | Price (USD) | Payload | Reach | Servo type | Ecosystem | Best for |
|---|---|---|---|---|---|---|
| **SO-ARM101 pair** | ~$600–800 BOM | ~100 g | 250 mm | STS3215 (plastic) | LeRobot/ACT | Data collection; cheapest proof-of-concept loop |
| **Forte** | $212/unit (×25 batch) | 0.63 kg | 467 mm | NEMA 17/23 steppers | Arduino / custom | Build-it-yourself; sub-mm repeatability at materials cost |
| **XLeRobot** | $660 (mobile system) | ~80 g | ~400 mm | STS3215 (plastic) | LeRobot/VLA | Mobile base without Z-lift; fixed arm height |
| **Nori Bot** | $947 (mobile + Z-lift) | ~1 kg (lift) | 400 mm + 600 mm Z | STS3215 (plastic) | LeRobot/ACT | Cheapest floor-to-counter; no validated success-rate data yet |
| **Cutting the Cord XLeRobot** | $1,202 (complete, untethered) | 1.0 kg/arm | ~400 mm | STS3215 (plastic) | LeRobot/ACT | Cheapest untethered with onboard GPU (Jetson Orin Nano) |
| **AhaRobot** | $1,000–$1,800 | 1.5 kg/arm | 750 mm + 1250 mm Z | STS3215 anti-backlash | ROS 2 Humble | Most validated sub-$2k; bimanual; ROS 2 native |
| **AgileX PiPER** | $2,500 | ~1–2 kg est. | ~600 mm est. | Metal gearbox | ROS 2 | Cheapest capable arm above plastic-servo tier |
| **Dobot MG400** | $3,000 | 750 g | 440 mm | Metal (SCARA) | Limited ROS | Structured desktop tasks only |
| **WidowX 250 S2** | $3,100 | 250 g | 250 mm | Dynamixel (metal) | ROS 2 / ALOHA leader | ALOHA leader arm standard; data collection |
| **OpenArm** | $3,500 | 1.5 kg | 550 mm | Metal | ROS 2 native | AI data collection focus (SVRC product) |
| **xArm 5 Lite** | $4,500 | 3 kg | 700 mm | Metal | Python SDK / ROS | Best cost/payload entry into metal tier |
| **ViperX 300 S2** | $4,800 | 750 g | 300 mm | Dynamixel (metal) | ROS 2 / ALOHA follower | ALOHA follower arm standard |
| **xArm 6** | $8,000 | 5 kg | 700 mm | Metal | Python SDK / ROS | Best cost/capability in research tier |
| **xArm 7** | $12,000 | 3.5 kg | 700 mm | Metal | Python SDK / ROS | 7-DOF avoids singularities; TidyBot++ reference |
| **Kinova Gen3 Lite** | $13,500–$18,000 | 0.5 kg | 760 mm | Metal + force ctrl | Polished SDK | Force control; polished integration; low payload for price |
| **Kinova Gen3** | $28,000 | 4 kg | 902 mm | Torque sensing every joint | Full SDK | Joint torque sensing; TidyBot v1 reference |
| **Franka FR3** | $25,000–$30,000 | 3 kg | 855 mm | Torque sensing every joint | ROS 2 | Research standard; best force control |

### Key considerations

**DOF: 5 vs 6 vs 7**
- 5-DOF (xArm 5 Lite, Dobot MG400): sufficient for tabletop pick-and-place with fixed orientation; loses a wrist rotation degree — can't flip objects or approach from arbitrary angles
- 6-DOF: standard for manipulation; covers most household tasks
- 7-DOF (xArm 7, Kinova Gen3, Franka): redundant DOF avoids singular configurations during continuous motion; measurably better for policies that require coordinated base+arm movement (see TidyBot++)

**Payload: what household objects weigh**
- Light objects (phone, TV remote, pen): <150 g → SO-ARM101 suffices
- Medium objects (mug, book, small bottle): 150–500 g → AhaRobot or Cutting the Cord
- Heavy objects (pot, plate stack, tool): 500 g–2 kg → need metal-gear arm ($2.5k+) or dual-arm coordination
- Very heavy (chair, laundry basket): cooperative manipulation or mobile base assist

**Reach: coverage envelope**
- Tabletop-only: 400–500 mm adequate
- Floor-to-counter: need Z-lift (Nori Bot, AhaRobot, YOR) or telescoping arm (Stretch)
- Overhead reach: 750 mm arm + 1,250 mm Z (AhaRobot) or YOR telescopic lift covers most scenarios

**Repeatability: when it actually matters**
- Imitation learning policies are surprisingly tolerant of poor repeatability (2–3 mm is fine for most tasks)
- Sub-mm repeatability matters for precision assembly, peg insertion, and screwing — not for typical household manipulation
- AhaRobot's 0.7 mm and Forte's 0.467 mm are more than adequate for everything in Stages 1–2

**Ecosystem: the hidden cost**
- **LeRobot** (HuggingFace): works out-of-the-box with SO-ARM101, XLeRobot, Nori Bot, Cutting the Cord. ACT, SmolVLA, Diffusion Policy all supported. Free, active community. The default choice for anything in the STS3215 tier.
- **ROS 2**: AhaRobot (native), xArm, ViperX, OpenArm. More infrastructure but better for multi-sensor integration, SLAM, Nav2 pipelines.
- **Proprietary SDK** (Kinova, Dobot): polished but locks you in; harder to swap policy frameworks.

**Force sensing: the upgrade path**
1. **Nothing extra** (any STS3215 arm): current readback from `Present_Current` register gives grip-force proxy — zero cost, validated in Nori Bot
2. **GelSight Mini / DIGIT** (~$650): tactile image at fingertip; FARM shows 0%→95% grape picking, 100% screw tightening vs vision-only
3. **F/T wrist sensor** (ATI Mini45): total wrist force+torque; good for unknown-weight payload compensation
4. **Joint torque sensing** (Franka FR3, Kinova Gen3): every-joint; the research standard; $25k+

**Single-arm vs bimanual**
- Stage 1 (pick-and-drop known objects into boxes): single arm is fine
- Stage 2 (world-model guided manipulation): still single-arm for most tasks
- Bimanual becomes necessary for: opening containers, folding, tasks requiring hold-and-manipulate, unstable objects
- Cheapest bimanual with Z-lift: AhaRobot ($1,000–$1,800); cheapest untethered: Cutting the Cord ($1,202)

---

## Stage-by-stage arm recommendations

| Stage | Recommended arm | Rationale |
|---|---|---|
| **Stage 1 — Workstation, known objects** | **SO-ARM101 leader+follower** (~$600–800) or **Cutting the Cord** ($1,202) | Cheapest path to prove the loop; your GPU handles training/inference |
| **Stage 2 — World model integration** | **AhaRobot** ($1,000–$1,800) or **Cutting the Cord** ($1,202) | ROS 2 native (AhaRobot) or untethered Jetson (Cutting the Cord) bridges to Nav2/SLAM |
| **Stage 3 — Drone-mounted** | Custom lightweight arm (sub-250 g) or SO-ARM101 single arm | Payload budget ~150–450 g aerial; off-the-shelf arms are all too heavy for flight; land-then-grasp preferred |
| **Stage 4 — Production feasibility** | AgileX PiPER ($2,500) or custom metal-gear | First tier above STS3215 with real durability; Forte ($212/unit batch) as build reference |

---

## Source

Curated reading list — the Tier 1–3 entries above (papers/repos/docs) are the primary sources; underlying validated cost/spec data is sourced in full on [[affordable-robot-arms]].

## Related

- [[affordable-robot-arms]] — full spec table with validated results per platform
- [[arm-starter-cost]] — full cost breakdown with verified BOMs; GPU-owned assumptions
- [[arm-prototype-roadmap]] — four-stage progression
- [[tactile-manipulation]] — GelSight Mini / FARM upgrade path
- [[close-range-depth-sensors]] — D405 / OAK-D SR for the wrist camera
- [[tidybot-deep-dive]] — TidyBot++ deep dive; holonomic base + xArm 7 context
- [[onboard-grasp-perception]] — OVD gap for open-vocabulary objects (Stage 2 blocker)
