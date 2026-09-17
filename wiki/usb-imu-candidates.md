# USB Yaw-Rate Gyro / IMU Candidates for the Rover (hub-powered, Linux-streamed)

**Summary.** For a chassis gyro that plugs into the rover's self-powered USB 2.0 hub and streams z-rate to Ubuntu/Python with no soldering, the field splits into (a) turnkey serial IMUs (WitMotion WT901C-TTL + a CP2102 adapter, ~CAD 100; Phidgets MOT0110, ~CAD 145) and (b) a 25-dollar microcontroller with an on-board 6-axis IMU and a 40-line USB-CDC firmware (Seeed XIAO nRF52840 Sense).
**Recommendation:** buy the **WT901C-TTL + generic CP2102** (in stock Amazon.ca, documented binary protocol, `pip install witmotion`, raw wz at 200 Hz, gyro-only yaw) — and order a **XIAO nRF52840 Sense** in the same cart as the CAD 25 fallback/upgrade (better gyro, MCU-side microsecond timestamps, we own the firmware).
Every MPU/ICM/LSM-class gyro here clears the noise bar by 10×: a 0.5 s integration window contributes ≤ 0.01° of angle random walk; the real error term is bias, which the per-stop re-zero handles.

Context: [[system-architecture]] (rover chassis: laptop tethered over a self-powered USB 2.0 hub; ESP32 with no free GPIO/I2C/UART — hence a USB sensor). Requirement recap: USB (CDC/HID/USB-UART), ≤ 100 mA from the hub, gyro z-rate ≥ 100 Hz with timestamps or a trustworthy fixed rate, documented protocol or open Python driver (no Windows-only config), ideal ≤ CAD 60 / hard cap ≈ CAD 150, MPU-6050…BNO08x gyro class, buyable in Canada in 1–2 weeks. All prices checked 2026-09-17; USD→CAD conversions use ≈1.37 (approximate — re-check at checkout).

---

## 0. Error budget (why almost any MEMS gyro passes on noise)

- Angle random walk over a window T: σθ ≈ N·√T (N = rate noise density). For T = 0.5 s, √T = 0.71: MPU-6050 0.005 °/s/√Hz → 0.004°; MPU-9250 0.01 → 0.007°; ICM-20948 0.015 → 0.011°; LSM6DS3TR-C 3.8 mdps/√Hz → 0.003°; ISM330DHCX 5 mdps/√Hz → 0.004°. All < 0.05° (MPU-9250: TDK product page; ICM-20948 DS-000189; LSM6DS3TR-C & ISM330DHCX ST datasheets — see Sources).
- Bias dominates. Between two stops 10 s apart, an un-zeroed 0.05 °/s offset (WT901C's stated "stability") is 0.5°; re-zeroing at each 0.5 s stop leaves only in-run drift (single-digit °/h class ≈ 0.001–0.003 °/s → ≤ 0.03° per 10 s). Averaging the 0.5 s stop window (50–100 samples) estimates bias to ~N/√0.5 ≈ 0.01 °/s — well below the raw offset.
- Timing: at 100 Hz, ±1 sample of timestamp uncertainty at a 30 °/s turn is 0.3° — so a fixed sensor-side rate (count frames) or a device-side timestamp matters more than gyro grade. Host arrival times through a USB-serial bridge jitter by 1–16 ms; never integrate on host arrival time.
- Magnetometer-fused yaw is useless on the chassis (motors, steel) — use raw wz or a 6-axis (gyro+accel) heading only.

## 1. WitMotion WT901C-TTL + USB-TTL adapter — **primary pick**

- **Interface/format:** TTL UART, binary frames `0x55 <id> 8 data bytes <sum>`; id 0x52 = angular velocity (wz = int16/32768·2000 °/s), 0x53 = Euler angles, 0x50 = time (RTC ms, unsynced), 0x51/0x54/0x59 accel/mag/quaternion. Selectable per-frame via register 0x02 (RSW); rate register 0x03 (0x09 = 100 Hz, 0x0b = 200 Hz); baud register 0x04 (default **9600** — must set 115200 for 200 Hz: 4 frames × 11 B × 200 Hz = 88 kbit/s). Config commands are `FF AA <reg> <lo> <hi>` then SAVE (`FF AA 00 00 00`) + power-cycle. (WT901C-TTL datasheet v20-0707, §6.)
- **Rate/spec:** 0.2–200 Hz; gyro MPU-9250, ±2000 °/s, 16-bit, "stability 0.05 °/s"; < 40 mA at 3.3–5 V (datasheet §3.1). Gyro auto-calibration (register 0x63) zeroes bias when the module thinks it is still — **disable it** (`set_gyro_automatic_calibration(False)`) so our stop-window re-zero is the only bias model, or keep it and accept an uncontrolled second estimator. Switch to the 6-axis algorithm (register 0x24 = 1) if the on-board yaw is ever used.
- **Driver:** `pip install witmotion` (pyserial-based; `get_angular_velocity()`, `set_update_rate()`, `set_baudrate()`, `set_gyro_automatic_calibration()`, `save_configuration()`, `get_timestamp()`; tested on HWT905, same protocol family) — configuration entirely from Linux, no MiniIMU.exe needed. Alternative: `pywitmotion` (parser only). Frames carry no host-syncable timestamp; rely on the fixed rate + frame counting, and log the 0x50 ms field only as a drop detector.
- **Price/availability (Amazon.ca, live page 2026-09-17):** WT901C-TTL **CAD 87.61**, In Stock, "only 5 left", ships from Amazon US (search snippets still show an older CAD 49.60 — price swings). Bare WT901 module (same MPU-9250, needs headers) CAD 63.35 In Stock. WitMotion's own CH340 cable is CAD 42.16 (overpriced); a generic CP2102 board (3.3 V/5 V pins, e.g. Amazon.ca B08ZS6H9VS 3-pack) is ~CAD 10–15 (listed; exact price not verified). Amazon.com also lists a WT901C-TTL + converter bundle (B09MLFLHTK, price hidden, "only 3 left"). RobotShop Canada carries the RS232/RS485 variants only.
- **Pitfalls:** binary little-endian frames with a 1-byte checksum (resync on 0x55); 9600 default; the CH340/CP2102 delivers bytes in bursts so parse a stream, not fixed reads; yaw from 0x53 uses the magnetometer (9-axis mode) — ignore it near motors; the "Kalman" internals are undocumented, so treat 0x52 as the only trustworthy output.
- **Verdict:** meets every requirement; total ≈ **CAD 100** delivered (above the CAD 60 ideal, well under the cap). The 4-wire Dupont plug into the adapter is the only "assembly".

## 2. WitMotion WT61C-TTL / WT61-Plus (MPU-6050, 6-axis)

- Same protocol/driver as §1 with no magnetometer (cleaner default yaw, MPU-6050 gyro 0.005 °/s/√Hz), 200 Hz (WT61-Plus). **Availability: delisted/unavailable** — the Amazon.ca WT61C-TTL ASINs return "Page Not Found", WT61 Plus is "Currently unavailable", Amazon.com WT61C-TTL "Currently unavailable" (2026-09-17). Verdict: would have been the cheapest WitMotion choice; not buyable now.

## 3. WitMotion HWT101 / HWT101CT (single-axis "crystal gyroscope" yaw module)

- Z-axis-only gyro + heading, 0.2–**500 Hz**, ±400 °/s, 0.000055 °/s LSB, heading accuracy 0.1°, "attitude stabilization 0.01°", < 25 mA, TTL/I2C, D1 pin = hardware yaw zero (HWT101 manual V23-0705). Same 0x52/0x53 frame family, so the `witmotion` lib parses it.
- **Amazon.ca HWT101 CAD 81.31, In Stock** — but it is a **15 mm bare module shipped with loose 1×6 headers (soldering required)**; the cased **HWT101CT** is USD 116.08 on Amazon.com ("only 14 left") ≈ CAD 160, over the cap, and not on Amazon.ca.
- Pitfalls: datasheet gives "static zero drift ±1 °/s" and "temperature drift ±5 (°/s)/°C" — implausible/typo, no ARW figure; the higher-grade claim is unverified. Verdict: **upgrade path if the MPU-class gyro proves the limit**, not the first buy (soldering, price).

## 4. WitMotion WT901BLECL / WT9011DCL (Bluetooth 5.0)

- Amazon.ca WT901BLECL CAD 65.54, WT9011DCL CAD 53.00 (search-snippet prices). Streams the same 0x55 frames over BLE; WitMotion sells a CP2102 BLE dongle (B07TBQ9Z58) that enumerates as a serial port — so it *could* hang off the hub — but adds BLE latency/jitter, a battery to charge, and a dongle. Fails the "trust the timing" and "hub-powered" spirit. Verdict: no.

## 5. WitMotion HWT905-TTL / HWT901B (industrial, cased)

- Amazon.ca HWT905-TTL CAD 177.48, HWT901B-TTL listed — over cap. Same protocol; the `witmotion` lib's reference device. Verdict: no (price).

## 6. Adafruit BNO085 (4754) or SparkFun BNO086 in UART-RVC mode + CP2102

- **RVC mode** (PS0/P0 high, PS1 low): the chip **autonomously transmits 19-byte frames at a fixed 100 Hz**, 115200 8N1 — header `0xAAAA`, 8-bit rolling index, yaw/pitch/roll in 0.01° (int16), accel in mg, checksum. Yaw is "rotation around Z since reset" — gyro-integrated, no magnetometer, with on-chip planar zero-gyro-offset (ZGO) calibration enabled by default. Spec: game-rotation-vector heading drift 0.5 °/min; gyro ±2000 °/s (BNO08X datasheet v1.17 §1.2.5, §3.1.6, §6.7). **No raw gyro rate in RVC mode.**
- Wiring: adapter 3V3→VIN, GND, adapter RX→board SDA(TX), board P0→3V3 (Adafruit guide). Driver: `pip install adafruit-circuitpython-bno08x-rvc` over a `serial.Serial` object (guide shows a Raspberry-Pi pyserial example). Adafruit notes pyserial buffering can serve stale frames — drain the port.
- **Price/availability:** DigiKey.ca **CAD 43.23, 7,390 in stock** (4754); RS Canada CAD 35.99 backorder; SparkFun BNO086 USD 29.95. Total with adapter ≈ CAD 55.
- Pitfalls: fused-only output means the host cannot inject its own stop-window bias re-zero (BNO086 "interactive calibration" needs SHTP mode, not RVC); 0.01° yaw quantization; the index byte is the only timing aid (fixed 100 Hz, detect drops); RVC needs the board crystal (Adafruit board has it). Verdict: **cheapest fused-heading option** and the simplest firmware-free stream; **runner-up** because it hands us an integrated yaw instead of a rate we control.

## 7. Phidgets PhidgetSpatial Precision 3/3/3 (MOT0110_0) — Canadian, USB, turnkey

- USB (mini-B) or VINT; gyro ±2000 °/s, 0.004 °/s resolution, noise ±0.2 °/s @ 1 ms, drift max 0.1 °/s, bias 0.05 °/s when heated; **min data interval 1 ms (1000 Hz)** with ms timestamps in the Phidget22 `SpatialData` event; **60 mA** (450 mA with the 50 °C heater — keep heating OFF on the hub). Linux `libphidget22` (Ubuntu apt repo) + `pip install Phidget22`, full Python examples.
- **Price/availability:** phidgets.com **USD 105.00, 800 in stock** (site toggles CAD; ≈ CAD 145 + shipping — right at the cap); RobotShop Canada "re-stocking soon". Phidgets ships from Calgary (2–5 days domestic). The cheaper Spatial Phidget MOT1102_1 (USD 32 + USD 26 VINT hub) is **50 Hz max** — fails the rate requirement; 1042/1044 are discontinued.
- Verdict: the most engineered "just works" option with real timestamps and a maintained Linux SDK, but 2.5× the WitMotion price for the same gyro class. Buy only if driver friction on the WitMotion route costs more than a day.

## 8. SparkFun OpenLog Artemis (DEV-16832) — USB-C IMU logger that streams CSV

- USB-C (CH340E), on-board ICM-20948 (0.015 °/s/√Hz), logs/streams CSV at up to **250 Hz IMU** (500 Hz analog) to the terminal with RTC date/time and an optional microsecond column; serial-menu configuration (press any key), works without an SD card; default 10 Hz — raise it and enable gyro-only columns. Open-source firmware.
- **DigiKey.ca CAD 87.86, 147 in stock**; SparkFun USD 59.95. Pitfalls: ICM-20948 is NRND (board still active); CSV parsing; RTC timestamp is coarse unless the µs column is on. Verdict: **zero-solder raw-rate stream with device timestamps** — a good alternative to §1 if WitMotion stock vanishes.

## 9. Yost Labs 3-Space USB / Micro-USB

- 2.5 °/h bias stability, up to 1000 Hz IMU mode, USB 2.0 — but "legacy product, limited availability, contact sales"; both Amazon listings "Currently unavailable" (2026-09-17); historically well over CAD 150. Verdict: no.

## 10. DIY: tiny MCU with on-board IMU + USB-CDC firmware — **fallback / upgrade**

- **Seeed XIAO nRF52840 Sense** — USB-C, on-board **LSM6DS3TR-C** (3.8 mdps/√Hz, ODR up to 1.66 kHz), **DigiKey.ca CAD 24.84, 1,318 in stock** (Sense Plus CAD 24.04, 42 in stock). Zero solder. Firmware: Arduino (`Seeed_Arduino_LSM6DS3`) or CircuitPython (`adafruit_lsm6ds`) — loop on data-ready at 208 Hz, print `micros,wz` (or a 6-byte binary frame) over USB CDC; ~40 lines, 1–2 h including a bench check against a turntable/known rotation. Host: pyserial. This gives device-side µs timestamps, our own bias handling, and the best noise figure on the list; risk is that we own the firmware and its jitter (use the IMU's own ODR/FIFO, not `sleep()`).
- **Alt (STEMMA QT, no solder):** Adafruit QT Py ESP32-S3 (USD 12.50) + Adafruit ISM330DHCX 4502 (USD 19.95, 5 mdps/√Hz) + STEMMA QT cable ≈ CAD 55; or ICM-20948 4554 / BMI270 breakouts the same way. Same firmware effort; more parts.
- Verdict: cheapest and technically best; costs an evening of firmware. Order one alongside the WitMotion.

## Shortlist for this rig

| Product | Interface | Rate | Price CAD (source) | Linux/Python driver | Verdict |
|---|---|---|---|---|---|
| WitMotion WT901C-TTL + generic CP2102 | USB-UART, binary 0x55 frames | 200 Hz (set 115200) | 87.61 + ~12 (Amazon.ca, in stock/listed) | `pip install witmotion` (pyserial) | **Buy** — raw wz, gyro-only yaw, config from Linux |
| Seeed XIAO nRF52840 Sense (DIY firmware) | USB-CDC | 208 Hz+ w/ µs stamps | 24.84 (DigiKey.ca, in stock) | pyserial + own 40-line firmware | **Buy as fallback/upgrade** |
| Adafruit BNO085 4754 (UART-RVC) + CP2102 | USB-UART, 19-B frames | fixed 100 Hz, indexed | 43.23 + ~12 (DigiKey.ca, in stock) | `adafruit-circuitpython-bno08x-rvc` | Runner-up — fused yaw only, no host re-zero |
| SparkFun OpenLog Artemis DEV-16832 | USB-C CDC, CSV | ≤ 250 Hz, RTC+µs | 87.86 (DigiKey.ca, in stock) | pyserial CSV; serial menu | Good alt if WitMotion stock fails |
| Phidgets MOT0110_0 | USB, Phidget22 events | ≤ 1000 Hz, ms stamps | ≈145 (USD 105 phidgets.com, Calgary, in stock) | libphidget22 + `Phidget22` | At cap; buy only for driver comfort |
| WitMotion HWT101 (bare) / HWT101CT | TTL, 0x55 frames | ≤ 500 Hz | 81.31 (Amazon.ca, in stock) / ≈160 (Amazon.com) | `witmotion` lib | Upgrade path; needs soldering / over cap |
| WitMotion WT61C-TTL | TTL | 200 Hz | delisted (Amazon.ca/.com) | `witmotion` lib | Not buyable now |
| WT901BLECL / WT9011DCL | BLE + USB dongle | 200 Hz | 65.54 / 53.00 (Amazon.ca, listed) | `witmotion` lib | No — BLE timing, battery |
| Spatial Phidget MOT1102_1 + VINT hub | VINT/USB | 50 Hz max | ≈80 (phidgets.com) | Phidget22 | No — rate |
| Yost 3-Space USB | USB | ≤ 1000 Hz | unavailable / quote | Yost API | No |

## Sources

- WitMotion WT901C-TTL datasheet v20-0707 (specs, protocol, registers): https://m.media-amazon.com/images/I/81mYIe9A97L.pdf (accessed 2026-09-17)
- WitMotion HWT101 manual V23-0705: https://m.media-amazon.com/images/I/916UMhYqC5L.pdf (2026-09-17)
- `witmotion` Python library docs (API, quickstart): https://witmotion.readthedocs.io/en/latest/api.html · https://witmotion.readthedocs.io/en/latest/quickstart.html (2026-09-17); `pywitmotion`: https://github.com/askuric/pywitmotion
- Amazon.ca live pages (2026-09-17): WT901C-TTL B01N03WKDV (CAD 87.61, 5 left) · WT901 module B07GBRTB5K (CAD 63.35) · WitMotion CH340 cable B07VHYCL5Y (CAD 42.16) · HWT101 B07VD5Z5WH (CAD 81.31) · WT61 Plus B07VBHJXD1 (unavailable) · WT61C-TTL B07YTYMWHK / B07TGHRWDK (not found) · CP2102 3-pack B08ZS6H9VS (listed)
- Amazon.ca search snippets (2026-09-17, prices unverified live): WT901BLECL B07THJB6HC CAD 65.54 · WT9011DCL B0BQ9QTS4D CAD 53.00 · HWT905-TTL B07G21XRV6 CAD 177.48 · BLE dongle B07TBQ9Z58
- Amazon.com (2026-09-17): HWT101CT B0CFFR4116 USD 116.08 · WT901C-TTL + converter bundle B09MLFLHTK · WT61C-TTL B07YTYMWHK (unavailable) · Yost TSS-USB B0073HPVYI, TSS-MUSB B01BVR7OKY (unavailable)
- CEVA BNO08X datasheet v1.17 (UART-RVC §1.2.5, calibration §3.1.6, performance §6.7): https://www.ceva-ip.com/wp-content/uploads/BNO080_085-Datasheet.pdf (2026-09-17)
- Adafruit BNO085 UART-RVC Python guide: https://learn.adafruit.com/adafruit-9-dof-orientation-imu-fusion-breakout-bno085/uart-rvc-for-python-circuitpython · RVC lib: https://pypi.org/project/adafruit-circuitpython-bno08x-rvc · buffering issue: https://github.com/adafruit/Adafruit_CircuitPython_BNO08x_RVC/issues/1 (2026-09-17)
- DigiKey.ca (2026-09-17): Adafruit 4754 CAD 43.23 / 7,390 stock https://www.digikey.ca/en/products/detail/adafruit-industries-llc/4754/13426653 · SparkFun DEV-16832 CAD 87.86 / 147 stock · Seeed 102010469 CAD 24.84 / 1,318 stock, 102010694 CAD 24.04 / 42 stock
- SparkFun BNO086 hookup guide (RVC jumpers): https://docs.sparkfun.com/SparkFun_VR_IMU_Breakout_BNO086_QWIIC/hardware_overview/ · BNO086 RVC forum thread: https://community.sparkfun.com/t/bno086-uart-rvc-protocol-minimal-configuration/63518 (2026-09-17)
- Phidgets MOT0110_0 (USD 105, specs, 60/450 mA, 1 ms): https://www.phidgets.com/?prodid=1205 · MOT1102_1 (USD 32, 20 ms min): https://www.phidgets.com/?prodid=1252 · MOT0109_0 discontinued: https://www.phidgets.com/?prodid=1204 · 1042_0 legacy: https://www.phidgets.com/?prodid=1025 · contact/Calgary address: https://www.phidgets.com/?view=contact · RobotShop CA listing (re-stocking): https://ca.robotshop.com/products/phidgets-phidgetspatial-precision-3-3-3 (2026-09-17)
- SparkFun OpenLog Artemis product (USD 59.95, 250 Hz IMU): https://www.sparkfun.com/sparkfun-openlog-artemis.html · hookup guide configuration: https://learn.sparkfun.com/tutorials/openlog-artemis-hookup-guide/configuration · firmware: https://github.com/sparkfun/OpenLog_Artemis (2026-09-17)
- Yost 3-Space USB/RS232 (legacy, contact sales): https://yostlabs.com/product/3-space-usbrs232/ (2026-09-17)
- Seeed XIAO nRF52840 Sense IMU usage: https://wiki.seeedstudio.com/XIAO-BLE-Sense-IMU-Usage/ · product: https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html (2026-09-17)
- Adafruit ISM330DHCX 4502 (USD 19.95): https://www.adafruit.com/product/4502 · QT Py ESP32-S3: https://www.adafruit.com/product/5426 · ICM-20948 4554: https://www.adafruit.com/product/4554
- Gyro noise densities: MPU-9250 https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=MPU-9250 · ICM-20948 DS-000189 https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000189-icm-20948-v1.5.pdf · LSM6DS3TR-C https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf · ISM330DHCX https://www.st.com/resource/en/datasheet/ism330dhcx.pdf
