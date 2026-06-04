# IMU / VIO Integration Reality (for the tethered rover rig)

**Should the `drone-prototype` add an IMU, and what does it actually cost to do right?** The
robustifier ladder ([[passive-stereo-robustification]]) puts a cheap MEMS IMU at **rung 1** ("highest
robustness per dollar"). That is true *in principle* — but the chip is the easy part. This page
records the **honest integration reality** for *our specific rig* (tethered USB stereo + ESP32/WiFi),
where the binding cost is not the sensor but **time-synchronisation**, and where — after the EDA003
hloc bake-off — the IMU is **no longer on the critical path**. It exists so the rover-build decision
([[land-rover-v1-rig]]) isn't made on the misleading "$5 IMU" headline. *(synthesis — the
robustification ladder + visual-inertial-slam page + the prototype's own EDA003 finding and rig
architecture; carries their raw-source citations through.)*

## TL;DR — buy nothing yet

1. **The IMU does not fix the problem we were actually stuck on.** It bridges **< 1 s** of feature
   starvation (motion blur, a brief blank patch, pure rotation) — it is explicitly **not** a
   white-wall cure and **not** a fix for the cross-session **PnP/relocalization gate**
   [src: passive-stereo-robustification §"hard limit", indoor-cluttered-slam]. That gate was the wall,
   and **hloc already cleared it** (2%→96%, EDA003 / [[relocalization-method-bakeoff]]). So the IMU
   buys nothing for the current method tests.
2. **The cost is sync, not silicon.** VIO needs IMU samples aligned to camera frames to ~**1 ms**.
   Our rig has **two asynchronous clocks and no hardware trigger**: SVPRO frames arrive over USB to
   the laptop with their own latency; an ESP32 IMU's samples arrive over WiFi with theirs. Software
   timestamping across that gap is the fiddly part that makes DIY VIO under-deliver.
3. **If you do spend, the bare IMU is a trap; the value buy is the D435i.** A ~$5–15 MEMS breakout is
   cheap but the sync DIY costs more time than it's worth. The **RealSense D435i ($334)** bundles a
   **hardware-synced BMI055 IMU + active IR stereo (the real white-wall cure) + factory calibration**
   in one module that works out-of-box with RTAB-Map / ORB-SLAM3 [src: passive-stereo-robustification
   §6 rung D, close-range-depth-sensors]. One purchase, three of the ladder's rungs.

## Why this is a separate page from the ladder

[[passive-stereo-robustification]] ranks IMU→VIO at **rung 1** on a *robustness-per-dollar* basis and
is correct to. But "rung 1, ~$5" reads as "obvious cheap win," and for **our** rig it is not — the
sensor price omits the dominant cost. This page is the asterisk on that rung: *the integration, not
the part, is the work, and the part only matters once the prototype is actually starvation-limited.*

## 1. What an IMU is and isn't for (don't buy it for the wrong reason)

| It **does** | It **does not** |
|---|---|
| Bridge **< 1 s** of starvation: motion blur, a brief textureless patch, pure rotation [src: indoor-cluttered-slam, 07-arxiv-2306-08522] | Cure **sustained white walls** — homes' dominant failure surface. That needs *active* stereo (IR projector) or a different depth sensor [src: passive-stereo-robustification §"hard limit"] |
| Tighten short-baseline scale + give gravity/heading priors | Fix the **cross-session relocalization (PnP) gate** — a *front-end* problem, solved by learned features (hloc), not inertial data |
| Enable full stereo+IMU autonomy with no LiDAR/GNSS (OKVIS2 forest demo) [src: visual-inertial-slam / arXiv 2403.09596] | Help at all while the rover drives **slowly under good light** — the current bench regime |

**Consequence:** the IMU is a *future* robustifier for when fast motion / brief starvation actually
bite in practice — a question the **next full-circuit sweep** will answer. It is not a prerequisite
for any queued method test (hloc generalization, metric pose error, front-end swap).

## 2. The real cost: time-synchronisation on a two-clock rig

VIO fuses a ~100–200 Hz inertial stream with ~10–15 Hz frames by **timestamp**; misalignment of more
than a few ms corrupts the state estimate. The rig makes this hard:

- **No hardware trigger / no shared clock.** The SVPRO is a stock UVC camera — it won't emit a sync
  pulse, and it can't be triggered by the IMU. The ESP32 ([[land-rover-v1-rig]] §2 compute) talks
  WiFi, adding jittery transport latency on the inertial side.
- **Frames are timestamped on *arrival* at the laptop, not on *exposure*.** USB + MJPG decode latency
  (tens of ms, variable) sits between the photons and the timestamp we can record — so even a
  perfectly-timestamped IMU is being aligned to a *lagged, jittery* camera clock.
- **Net:** a bare IMU yields **loosely-coupled, software-timestamped** data. Usable for orientation
  priors / a tilt-compensated heading, marginal for metric VIO. Getting tight VIO out of it is a real
  engineering task (estimate + online-calibrate the camera–IMU time offset, e.g. Kalibr-style), and a
  standing **parked integration risk**, not a plug-in.

## 3. Hardware paths (if/when the prototype is starvation-limited)

| Path | Cost | Gets you | The catch |
|---|---|---|---|
| **Bare MEMS IMU** — ICM-20948 or BNO055 breakout on the ESP32 (I²C), streamed to the laptop | **~$5–15** | A raw/fused inertial stream; fine for orientation priors | **Sync is the project.** No HW trigger; you own the camera–IMU time-offset estimation. Cheap chip, expensive integration. BNO055's on-chip fusion eases orientation but its internal filtering complicates *tight* VIO timing. |
| **RealSense D435i — turnkey** | **~$334** | **HW-synced BMI055 IMU + active IR stereo + factory calibration**, out-of-box with RTAB-Map/ORB-SLAM3 [src: passive-stereo-robustification §6 D] | Spends money; abandons the SVPRO. But it's still *stereo* (consumer-cost tenet holds — active, not LiDAR) and it *also* solves the white-wall limit the SVPRO physically can't. |

## 4. Recommendation for the rover build

1. **Buy nothing now.** The IMU isn't on the critical path; hloc cleared the gate that was.
2. **Let the next full-circuit sweep decide** whether passive stereo actually starves in practice
   (white walls) and whether motion blur bites (the regime an IMU helps).
3. **If escalation is warranted, prefer the D435i over a bare IMU.** It buys IMU + active stereo +
   calibration as one hardware-synced unit, dodging the two-clock sync rabbit hole and curing the
   white-wall limit in the same purchase. A bare IMU only makes sense if VIO sync is itself a thing
   the project wants to learn, or once compute moves onboard (a shared clock removes the WiFi hop).

## Source

- [src: passive-stereo-robustification] [[passive-stereo-robustification]] — robustifier ladder
  (rung 1 IMU/VIO ~$5, rung 5 active stereo), hardware ladder ($12 pico → $80–150 OV9281+IR DOE →
  **$334 D435i = BMI055 IMU + active IR stereo + factory calib**), and the "IMU bridges < 1 s, not a
  white-wall cure" hard limit [carries 07-arxiv-2306-08522, 11-amazon-indoor-mapping].
- [src: visual-inertial-slam] [[visual-inertial-slam]] — stereo+IMU full autonomy without LiDAR
  (OKVIS2, 15 Hz) [arXiv 2403.09596].
- [src: indoor-cluttered-slam] [[indoor-cluttered-slam]] — featureless-surface degradation; IMU
  bridging < 1 s.
- [src: close-range-depth-sensors] [[close-range-depth-sensors]] — D435i active-IR-stereo + IMU module
  notes.
- [src: prototype] `drone-prototype` EDA003 hloc bake-off (`eda/EDA003-hloc-bakeoff/major-findings.md`,
  [[relocalization-method-bakeoff]]) — learned front-end clears the PnP gate the IMU does *not*
  address; and [[land-rover-v1-rig]] §2 (ESP32/WiFi compute path = the second async clock).

## Related

[[passive-stereo-robustification]] · [[visual-inertial-slam]] · [[indoor-cluttered-slam]] ·
[[relocalization-method-bakeoff]] · [[land-rover-v1-rig]] · [[close-range-depth-sensors]] ·
[[sensor-weaknesses-and-fixes]] · [[learned-slam]] · [[system-architecture]] ·
[[home-tidy-drone-prototype]]
