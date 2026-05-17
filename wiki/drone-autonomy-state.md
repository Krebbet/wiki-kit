# State of AI-Driven Drone Autonomy

Synthesis of where AI-navigated and autonomous (or partially autonomous) drones stand as of the captured corpus (2024–2026). The honest summary: **narrow autonomy is shipping commercially, agile/high-speed autonomy is demoed in the lab, and regulation is only now being written to permit routine fully-autonomous BVLOS at scale.** The sensor question — what to perceive the world with — is unresolved and is tracked as [[lidar-vs-vision-autonomy]].

## The maturity spectrum

*(synthesis — evidence tags trace to the per-topic pages)*

**Shipping at scale.**
- Vision-only consumer/prosumer autonomy: Skydio's 6-camera "Spatial AI" stack does 360° obstacle avoidance and subject tracking as a product (*claimed*, vendor-2020) — [[skydio-autonomy-stack]].
- LiDAR-based industrial autonomy for inspection (wind turbine, bridge, power line) and precision agriculture (*shipping at scale*) — [[lidar-for-uav-autonomy]].
- Event-camera *sensors* are commercially shipping (iniVation, Prophesee/Sony) even though drone *applications* are not — [[event-cameras]].
- Defence-origin multi-asset autonomy: [[anduril-lattice]] demonstrates single-operator fleet control with multi-source sensor fusion (*shipping at scale* in defence context; consumer transfer potential).

**Demoed (lab / controlled field, not deployed at scale).**
- LiDAR-free large-scale outdoor forest flight, fully onboard, zero collisions — [[visual-inertial-slam]].
- High-speed and dynamic-obstacle flight on event cameras: 3.5 ms dodging latency, 9.8 m/s cluttered flight, low-light flight to 10 lux, motor-failure recovery — [[eth-rpg-scaramuzza]].
- High-speed LiDAR autonomy: 13.7–20 m/s in clutter, multi-UAV swarm odometry — [[lidar-for-uav-autonomy]].
- AI beating world-champion human FPV pilots (15/25 races) — but with frame cameras + DRL and a pre-mapped track, and it failed when lighting changed: a pointed reminder that demoed ≠ robust ([[eth-rpg-scaramuzza]]).
- Single-operator multi-asset autonomy with heterogeneous sensor fusion — *demoed* in a scripted, controlled scenario (defence-origin; [[anduril-lattice]]).

**Regulated / gated (the binding constraint on scaling).**
- The US [[faa-part-108-bvlos]] NPRM explicitly envisions "mostly to fully autonomous" operation as the norm and even permits no human flight coordinator if the manufacturer's instructions allow — but a final rule is only mandated ~Feb 2026, and the legal equivalence of detect-and-avoid to see-and-avoid was *deferred*.
- The gating technical bottleneck is non-cooperative [[detect-and-avoid]]: cooperative (ADS-B) detection is largely solved; there is no consensus performance standard for onboard radar/CV/acoustic detection of non-broadcasting aircraft, which blocks dense urban (Cat 5) autonomy.

## Cross-cutting tensions *(editorial)*

- **Autonomy is sensor-bound, not just algorithm-bound.** Nearly every "state of the art" claim in the corpus is really a claim about a sensor modality plus its SLAM/planning stack. The unresolved [[lidar-vs-vision-autonomy]] question therefore propagates into the autonomy roadmap itself.
- **Demoed ≠ shipping ≠ legal.** The corpus repeatedly shows capability outrunning both robustness (the lighting-change race failure) and regulation (Part 108 still in NPRM). Treat optimistic timelines accordingly.
- **Onboard-AI energy is rarely the limiter — except at insect scale.** Across the power-budget corpus, propulsion is 85–96% of a drone's electrical power and battery energy density is the real ceiling; compute is a small (≈0.2–10%) and shrinking-cost slice. The exception is sub-30 g platforms, where compute weight+power genuinely caps autonomy and neuromorphic computing is the credible (but still immature) relief. See [[drone-power-budget]].

## Open questions for the wiki

- Resolve or keep tracking [[lidar-vs-vision-autonomy]] (currently `open`).
- Does non-cooperative DAA get a consensus standard before the Part 108 final rule? (Determines whether urban autonomous BVLOS is real by ~2026.)
- Does neuromorphic compute mature out of the lab before it matters for consumer drones, or do conventional ultra-low-power SoCs ([[nano-drone-compute]]) close the gap first? See [[drone-power-budget]], [[neuromorphic-computing-for-drones]].

## Source

- `raw/research/autonomy-and-sensors/01-lidar-uav-survey.md`
- `raw/research/autonomy-and-sensors/02-event-camera-survey.md`
- `raw/research/autonomy-and-sensors/03-vislam-no-lidar.md`
- `raw/research/autonomy-and-sensors/04-faa-part108-nprm.md`
- `raw/research/autonomy-and-sensors/06-event-vision-uav-review.md`
- `raw/research/autonomy-and-sensors/07-rpg-event-research.md`
- `raw/research/autonomy-and-sensors/08-skydio-autonomy-intro.md`
- `raw/research/autonomy-and-sensors/11-mittr-anduril-demo.md`
- `raw/research/autonomy-and-sensors/13-scaramuzza-iccp2024.md`

## Related

- [[drone-sensors-for-autonomy]] — the sensor map underpinning every claim here
- [[lidar-vs-vision-autonomy]] — the central unresolved tension
- [[lidar-for-uav-autonomy]] · [[visual-inertial-slam]] · [[event-cameras-for-uavs]] · [[eth-rpg-scaramuzza]] — demoed-capability detail
- [[skydio-autonomy-stack]] · [[anduril-lattice]] — shipping/fielded systems
- [[faa-part-108-bvlos]] · [[detect-and-avoid]] — the regulatory gate
- [[aerial-manipulation]] — physical-interaction autonomy; lags flight autonomy, gated by onboard perception
