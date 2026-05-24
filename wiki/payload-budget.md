# Payload & Endurance Budget — Phase-1 Indoor Prototype

Build-reference sizing for the [[home-tidy-drone-prototype]] Phase-1 platform: component masses from captured spec sheets, the payload→flight-time relationship, and the thrust/throttle targets that set frame, motor, prop and battery choices. **Headline (synthesis):** the sensor+compute payload is ~0.5–0.6 kg, lands the all-up weight in the ~2 kg class on the candidate Holybro X500 V2, and — per the captured endurance physics — caps realistic indoor flight time at roughly the **15–25 min** band, well short of the multicopter ~30 min practical ceiling.

## Component masses *(each traces to a captured source; assembled budget is synthesis)*

| Component | Mass | Evidence | Source |
|---|---|---|---|
| Livox MID360 LiDAR | ~265 g | *shipping at scale* | carried from [[lidar-for-uav-autonomy]]; the captured MID360 spec page (`01`) lists laser/thermal specs, **not** mass |
| Jetson Orin NX module | 28 g | *shipping at scale* | NVIDIA dev-forum reply (`02`) — vendor-confirmed dry weight |
| Auvidea JNX120S carrier (PCB, no module/M.2) | ~14 g | *claimed* (in design; prototypes "by Jan 2026") | Auvidea product page (`07`) |
| Pixhawk 6C Mini FC | 39.2–46.8 g (Model A current 42.4 g) | *shipping at scale* | Holybro tech spec (`06`) |

**Compute stack note (synthesis):** the 28 g + ~14 g figures are *bare* module + carrier PCB; a flyable Orin NX node adds NVMe SSD, heatsink/spreader (Auvidea quotes a 20 mm-with-spreader profile, `07`), standoffs and cabling — budget **~120–160 g** for the assembled companion-computer node, not 42 g.

## Frame: Holybro X500 V2 *(candidate)*

The captured PX4 build guide (`04`) documents the X500 V2 + Pixhawk 6C dev kit but is an **assembly procedure — it states no frame mass or AUW**. Loadable facts from it: it ships with provision for a companion computer (Jetson-class) and a depth/tracking camera mount, and the reference power setup is a **4S 16.8 V 5200 mAh** LiPo on a PM02 power module. The X500 V2 is a ~500 mm-class quad — within the ArduPilot "small Quadcopter, 10–14″ props, 3–7 lb" band (`08`) that targets 20+ min flight times with a small camera payload. Frame/AUW mass for budgeting below is *(synthesis, verify on a scale at build)*.

## Worked payload budget *(synthesis — masses traced above; AUW/battery/frame estimated, verify before build)*

| Item | Mass (g) | Basis |
|---|---|---|
| Frame (X500 V2, arms+plates+landing gear) | ~610 | est. for 500 mm-class; not in `04` — verify |
| 4× motor + ESC + prop (X500 power set) | ~400 | est. for the class |
| Pixhawk 6C Mini + GPS + PM02 + wiring | ~120 | FC 42 g (`06`) + ancillaries est. |
| Companion node (Orin NX 28 g + JNX120 ~14 g + SSD/heatsink/cables) | ~140 | `02` + `07` + assembly est. |
| Livox MID360 + mount/anti-vib | ~300 | sensor 265 g + mount est. |
| RGB cam + misc (cables, SD, prop guards) | ~150 | indoor-safety + future-features est. |
| **Dry mass (no battery)** | **~1,720** | sum |
| Battery (4S 5200 mAh LiPo, ref. of `04`) | ~480 | typical for that pack |
| **All-up weight (AUW)** | **~2,200** | dry + battery |

**Payload-of-interest (sensor + compute + guards):** ≈ **0.5–0.6 kg** of the AUW is the AI/sensing payload that distinguishes this from a bare camera quad — the precise quantity the endurance penalty is paid for.

## Endurance & thrust targets *(captured guidance)*

- **Payload ⇄ flight-time is a hard trade** (Tyto Robotics, `05`): added mass → more thrust → higher RPM → more power → shorter battery life. Tyto's worked example (T-Motor MN4014 / APC 12×6e) shows a **1.6 kg** craft at **39.6 min** with zero payload, **falling monotonically** in 0.2 kg steps. Our ~0.5 kg payload sits squarely on the declining part of that curve — expect a multi-minute hit versus the bare airframe. *(demoed via calculator, not our hardware)*
- **Thrust-to-weight ~2:1.** Tyto (`05`) and ArduPilot (`08`) both state max thrust should be ≈ **twice** hover thrust for safe take-off, climb and control margin. At ~2.2 kg AUW that means a propulsion set rated to **~4.4 kg static thrust** (≈1.1 kg/motor on a quad).
- **Hover at ~50% throttle.** ArduPilot (`08`): "target your copter design weight so that it hovers at approximately 50% throttle for optimum efficiency and flight time," and pick motor-prop-cell combos giving **≥10 % g/W at 50 % throttle** (the high-efficiency motors quoted reach 17+ g/W). A craft hovering well above 50 % is over-loaded / under-propped; the 2:1 thrust target is what *puts* hover near 50 %.
- **Larger, slower props win** (`08`): low-KV motors + big props + fewer cells = best efficiency and longest endurance; size the frame for the largest prop it can swing. Hex/octo layouts buy single-motor-out tolerance but **lose efficiency** (smaller props, motor-clearance limited) — for indoor Phase-1 the X-quad is the efficiency choice (mind the single-motor-failure → crash risk indoors, mitigate via [[prop-guard-failsafe]]).
- **Practical ceiling.** ArduPilot (`08`): "very hard to get much more than 30 minutes of usable flight time from any useful multicopter," and **20 min is the realistic goal for hobby-grade components**. Loaded with the LiDAR+compute payload, plan for the **15–25 min** band, not 30+.

## Estimation tooling *(captured)*

Size the actual motor/prop/battery with **eCalc xcopterCalc** (`03`; ArduPilot's recommended tool, `08`). Inputs are the AUW table above + a candidate motor/prop/cell-count; it returns hover throttle %, hover/mixed/max flight time, thrust-to-weight, hover current and per-motor efficiency — i.e. it directly checks the **~50 % hover / ~2:1 thrust** targets before any money is spent. The captured eCalc page is the empty results template; the build step is to populate it with the real X500 power set and the ~2.2 kg AUW. Power-budget context (compute is a small slice of total; propulsion dominates) is in [[drone-power-budget]]; cell-energy detail in [[drone-battery-energy]].

## Build notes *(synthesis / recommendations)*

- Treat the ~2.2 kg AUW and the frame/motor/battery masses as **estimates to confirm on a scale**; only the MID360, Orin NX, JNX120 and Pixhawk masses are source-backed.
- The **JNX120 is not yet shipping** (`07`: "in design… first prototype quantities by January 2026") — for a build today substitute a shipping Orin NX carrier and re-weigh; the 14 g figure is a floor.
- Buy the propulsion set for **~2:1 thrust at the *loaded* AUW**, not the bare frame — the payload is ~25 % of AUW and eats the margin.
- If eCalc shows hover throttle >60 % or thrust-to-weight <1.8:1 at ~2.2 kg, the platform is under-propped: drop sensor mass (RGB-only / depth-cam route per [[home-tidy-drone-prototype]]), go to a bigger prop/frame, or accept the endurance hit.
- Endurance levers beyond battery: perch-and-rest and roll-instead-of-hover ([[aerial-perching]], [[drone-power-budget]]) — relevant once Phase-1 nav works.
- **FoxTech SU17** was a candidate reference but **no spec sheet was captured** for it (capture failed); excluded from this budget. Re-attempt if its payload/endurance data is needed.

## Source

- `raw/research/payload-budget/01-livox-mid360-specs.md` — Livox MID360 spec sheet (laser/thermal/temperature specs; no mass listed) — https://www.livoxtech.com/mid-360/specs
- `raw/research/payload-budget/02-orin-nx-weight.md` — NVIDIA dev-forum: Jetson Orin NX module dry weight 28 g (vendor-confirmed) — https://forums.developer.nvidia.com/t/jetson-orin-nx-dry-weight/232621
- `raw/research/payload-budget/03-ecalc.md` — eCalc xcopterCalc results template (motor/prop/battery/ESC sizing tool) — https://www.ecalc.ch/xcoptercalc.php
- `raw/research/payload-budget/04-px4-x500v2.md` — Holybro X500 V2 + Pixhawk 6C build guide (assembly + 4S 5200 mAh ref. power; no frame mass) — https://docs.px4.io/main/en/frames_multicopter/holybro_x500v2_pixhawk6c.html
- `raw/research/payload-budget/05-tyto-payload.md` — Tyto Robotics: how drone payload affects flight time (payload→RPM→power trade; 2:1 thrust; worked example) — https://www.tytorobotics.com/blogs/articles/how-does-drone-payload-affect-flight-time
- `raw/research/payload-budget/06-pixhawk6c-mini.md` — Holybro Pixhawk 6C Mini technical spec (Model A current 42.4 g) — https://docs.holybro.com/autopilot/pixhawk-6c-mini/technical-specification
- `raw/research/payload-budget/07-auvidea-jnx120.md` — Auvidea JNX120 carrier board (JNX120S PCB ~14 g; in design, prototypes Jan 2026) — https://auvidea.eu/product/jnx120-carrier-board-for-nvidia-jetson-orin-nano-nx/
- `raw/research/payload-budget/08-ardupilot-multicopter-design.md` — ArduPilot advanced multicopter design (thrust-to-weight, ~50% hover throttle, prop/motor/efficiency guidance, ~30 min ceiling) — https://ardupilot.org/copter/docs/advanced-multicopter-design.html

## Related

- [[home-tidy-drone-prototype]] — the Phase-1 build this budget sizes
- [[drone-power-budget]] — propulsion dominates; compute is a small power slice
- [[drone-battery-energy]] — cell chemistry / energy-density side of the endurance ceiling
- [[lidar-for-uav-autonomy]] — MID360 role and the 265 g sensor mass
- [[nano-drone-compute]] — onboard-compute envelope (Orin-class) feeding the companion-node mass
- [[fast-lio-mid360-orin]] — the LiDAR+compute software load the payload exists to carry
- [[prop-guard-failsafe]] — indoor safety margin that adds to the misc-mass line
- [[aerial-perching]] — perch-and-rest as an endurance lever beyond battery sizing
