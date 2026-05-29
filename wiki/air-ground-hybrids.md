# Air-Ground Hybrid Drones

Rolling beats hovering by 10–40× in power draw, translating directly to 40× longer ground operating time on the same battery. Air-ground hybrids exploit this gap by adding wheels (passive or driven) to multirotor frames, trading brief flight capability for practical ground endurance. The field spans minimal passive-wheel add-ons through fully-actuated tilt-rotor platforms and appendage-repurposing morphobots, but universal lab-only (mocap) localisation and weight overhead remain the blocking gaps for consumer deployment.

For platforms that go further — ground-primary robots that use flight as a burst capability for stairs and obstacles — see [[ground-aerial-robots]] (DoubleBee, Duawlfin, ATMO, M4 primary paper, RL stair-climbing).

## The Endurance Case

[[multimodal-locomotion]] establishes the core principle: aerial locomotion is energetically expensive, and any platform that can roll on a surface instead of hover gains massive endurance. The empirical numbers are unambiguous. A single 20 g passive nylon wheel on a 1950 g bi-copter saves 77% battery while stationary and 61% while rolling versus continuous hover [05-single-passive-wheel, arXiv 2003.09242]. A driven unicycle wheel extends ground range to ~2.8× aerial and operating time to ~41× aerial on the same pack [03-roller-quadrotor, arXiv 2303.00668]. This asymmetry — not payload, not speed — is the consumer-relevant heart of the hybrid concept.

## Platform Comparison

| Platform | Mechanism | Key Energy Result | Mass | Maturity | Localisation |
|---|---|---|---|---|---|
| Passive-wheel bi-copter [05] | 1 passive nylon wheel, zero actuators | 77% saving stationary; 61% rolling vs hover | 1950 g (+20 g wheel, ~1%) | TRL ~4, lab/flat surface only | OptiTrack mocap |
| Roller quadrotor [03] | Unicycle wheel + rotor-differential yaw | 41× longer ground time; rolling 15.6 W vs flight 657.8 W; ground CoT 86.7 J/m vs 328.9 J/m flying | 1500 g | TRL ~4-5, indoor only | Vicon EKF (mocap) |
| TiltRopter [04] | Tilt-rotors + 2 passive wheels on tilt arms, fully actuated 6-DoF | Ground 47.4 W vs flight 653.6 W = **92.8% ground power reduction** | 1500 g | TRL ~4-5, SOTA | Mocap (state estimation) |
| M4 MorphoBot [13] | 4 identical shrouded props reconfigure as wheels/legs/thrusters | UAS ~3000 W vs UGV ~30–100 W; 8 locomotion modes | 6000 g (tire assembly 1600 g, 29%) | TRL ~3-4, landmark | Jetson Nano + RealSense D455, limited autonomy |

### Platform Notes

**Passive-wheel bi-copter** [05-single-passive-wheel, arXiv 2003.09242, 2020] is the minimal existence proof and lower bound: three-mode cascaded PID (aerial/transition/rolling) with auto ground-detection; cannot self-land (single-contact instability); flat smooth surfaces only. The ~1% mass overhead is the benchmark to beat.

**Roller quadrotor** [03-roller-quadrotor, arXiv 2303.00668, 2023] adds rotor-differential yaw for steering with no dedicated actuator — elegant but yields rough trajectory tracking. Passes 18 cm gaps. Jetson Xavier NX. Ground operating time ~44 min / 477 m vs flight ~1.8 min / 216 m on 2000 mAh 4S.

**TiltRopter** [04-tilt-ropter, arXiv 2602.01700, 2026] is current SOTA: unified NMPC with wrench estimator (no F/T sensor, no VIO required), aerial position RMSE 0.052 m / ground 0.145 m / transition 0.125 m at ≤1.5 m/s. Supersedes the underactuation limits of [03] and [05]; no endurance or payload figure published.

**M4 MorphoBot** [13-m4-morphobot, Sihite et al., *Nature Communications* 14:3323, 2023, Caltech — primary paper PMC10300070] achieves 8 modes (fly, roll, crawl, crouch, balance, tumble, scout, loco-manipulate) via appendage repurposing; 45° slope capability (WAIR-style). MM-PRM + A* onboard planning. Only UGV↔UAS autonomous mode switching demoed — 8-mode autonomy is declared future work. The 1600 g tire assembly illustrates the weight-overhead cost of flexibility. Autonomy pipeline (traversability CNN + 3D A* path planner, simulation-only) documented in Rajput 2023 MS thesis, Northeastern [arXiv 2308.13972]. See [[ground-aerial-robots]] for the primary paper citation and autonomous mode-switching details.

## Multimodal + Manipulation

AirCrab [07-aircrab, arXiv 2403.15805, IROS 2024] combines a 2.655 kg quadrotor with a single active wheel (+305 g) and a 3-DoF arm. The "Egret posture" — single wheel contact below the centre of gravity — decouples position control (wheel) from attitude control (props), halving end-effector error: ground-mode RMSE 1.02 cm vs 2.00 cm hovering. Ground control allocation consumes 11.7–47.1% less energy than stock Ardupilot at low-throttle operating points. Demo payload: 90 g. Caveat: aerial localisation uses onboard IMU + optical-flow EKF (no mocap), but the full mission was manually piloted by two operators with no onboard planning or grasp detection.

M4's loco-manipulation mode is grasping only and not yet autonomously triggered. Both platforms demonstrate that ground contact is not just an endurance strategy — it stabilises the manipulator. See [[aerial-manipulation]], [[drone-contact-and-door-tasks]], and [[aerial-grasping]] for the broader manipulation context.

## Shared-Actuator and Leg-Rotor Variants

**FSTAR** [09-fstar-techcrunch, TechCrunch / Ben-Gurion, ICRA 2019 — journalism source]: the same brushless motors drive both rotors and wheels; tilt arms redirect thrust into four driven wheels at ~8 ft/s ground speed, low energy draw. Reconfigurable width. Prototype, teleoperated. *Treat numbers as illustrative; no peer-reviewed primary in corpus.*

**LEONARDO** [12-spectrum-leonardo, IEEE Spectrum — journalism source; no primary paper in corpus, flag accordingly]: Caltech leg-rotor bipedal hybrid; four tilted props run continuously to balance while light servo legs walk. 2.5 kg, 75 cm. Walking ~544 W (445 W props + 99 W legs) vs flight power; CoT 108 walking vs 15.5 flying. ~100 s flight / ~3.5 min walking. Key lesson: continuous thruster-assisted balancing solves bipedal stability but is brutally power-inefficient — the leg-rotor tradeoff inverts the usual ground-saves-energy argument. Path-following only; no autonomous mode switching. *Numbers journalism-sourced; verify against primary before citing.*

## Consumer Verdict and Gaps

**Passive wheel is the most plausible cheap endurance add-on** for consumer platforms: ~1% mass penalty, zero actuators, zero firmware complexity beyond mode detection. The 77%/61% saving figures [05] are empirical lower bounds achievable on any stable surface.

**Universal blocking gaps:**

- **Mocap dependency**: every platform above uses Vicon, OptiTrack, or equivalent for state estimation during ground operation. Transition-mode localisation without external infrastructure remains unsolved. See [[drone-sensors-for-autonomy]] and [[drone-autonomy-state]].
- **Weight overhead**: M4's 29% mass in tire assemblies and AirCrab's arm mass illustrate the flexibility-vs-efficiency tradeoff. Passive wheels minimise this; morphobot designs maximise it.
- **Terrain**: all results on flat, smooth, indoor surfaces. Outdoor rough terrain + weather invalidates every energy figure above.
- **Autonomy**: mode switching beyond UGV↔UAS binary (M4), and full mission execution without human operators (AirCrab), are unsolved.

Ground power savings interact directly with battery sizing and flight-time calculations; see [[drone-power-budget]]. Passive perching on structures is a related endurance strategy requiring no ground contact; see [[aerial-perching]].

## Sources

- `raw/research/multimodal-locomotion/05-single-passive-wheel.md` — arXiv 2003.09242 (2020); passive-wheel bi-copter, foundational minimal design, empirical energy savings
- `raw/research/multimodal-locomotion/03-roller-quadrotor.md` — arXiv 2303.00668 (2023); unicycle-driven quadrotor, 41× ground time, full energy/CoT breakdown
- `raw/research/multimodal-locomotion/04-tilt-ropter.md` — arXiv 2602.01700 (2026); SOTA fully-actuated tilt-rotor+wheel, NMPC, 92.8% ground power reduction
- `raw/research/multimodal-locomotion/13-m4-morphobot.md` — Nature Comms 2023 (Caltech); 8-mode appendage-repurposing morphobot, landmark platform (journalism/secondary source; primary paper is PMC10300070, captured in `raw/research/dual-mode-robots/01-05-pmc-m4-nature-comms.md`)
- `raw/research/dual-mode-robots/02-06-arxiv-2308-13972.md` — arXiv 2308.13972 (Northeastern, 2023); M4 autonomy thesis — traversability CNN + 3D A* path planner (simulation)
- `raw/research/multimodal-locomotion/07-aircrab.md` — arXiv 2403.15805, IROS 2024; wheel+arm quadrotor, Egret posture, manipulation accuracy numbers
- `raw/research/multimodal-locomotion/09-fstar-techcrunch.md` — TechCrunch journalism; Ben-Gurion FSTAR shared-actuator concept, context only
- `raw/research/multimodal-locomotion/12-spectrum-leonardo.md` — IEEE Spectrum journalism; Caltech LEONARDO leg-rotor bipedal, no primary in corpus

## Related

- [[ground-aerial-robots]] — deeper detail on ground-primary burst-flight platforms (DoubleBee, Duawlfin, ATMO, M4 primary paper, RL stair-climbing)
- [[multimodal-locomotion]] — parent topic covering the full locomotion-mode landscape
- [[aerial-manipulation]] — arm-equipped aerial platforms; AirCrab bridges both
- [[aerial-grasping]] — grasping mechanics relevant to M4 loco-manipulate and AirCrab
- [[drone-contact-and-door-tasks]] — contact-stabilised tasks; Egret posture directly relevant
- [[drone-power-budget]] — energy accounting that makes the rolling savings quantitatively significant
- [[aerial-perching]] — complementary passive endurance strategy (structure contact vs ground contact)
- [[drone-autonomy-state]] — autonomous mode switching status across platforms
- [[drone-sensors-for-autonomy]] — localisation gap; mocap dependency is the field's main consumer barrier
