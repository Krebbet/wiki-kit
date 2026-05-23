# Skydio Autonomy Stack

Skydio's "Spatial AI" system (*claimed*, vendor-2020) uses six fisheye 4K cameras for 360° obstacle avoidance with no LiDAR, ultrasonic, or event sensors — a deliberate vision-only architectural bet. The Skydio 2 runs all autonomy onboard an NVIDIA Jetson TX2 with no cloud dependency (*claimed*; product was shipping at time of source). This page is sourced entirely from Skydio marketing copy; treat all capability claims critically.

## Status update (2026)

Skydio is now **enterprise / defence / public-safety-focused**; the consumer-product framing on this page is historically dated (2020, Skydio 2 / Jetson TX2).

- **X10D — Blue UAS listed (May 2024), NDAA-compliant.** The X10D was added to the DoD Defense Innovation Unit's Blue sUAS Cleared List in May 2024, making it the second Skydio aircraft to qualify (following the X2D). Available via GSA/DLA procurement schedules. Self-described as "the only domestic company producing dual-use drones at scale for both the enterprise and defense sectors." (`raw/research/company-status/02-skydio-x10d-blueuas.md` — DroneLife, 2024-05-31)
- **Oct 2024 battery-supply squeeze** from China sanctions. Skydio manufactures in the US but still sourced batteries from China; Chinese sanctions (Oct 10 2024) barred Chinese suppliers from doing business with Skydio, limiting customers to one battery per drone while new sources came online (~spring 2025). CEO Adam Bry characterised it as "an attempt to eliminate the leading American drone company." (`raw/research/company-status/03-skydio-battery-sanctions.md` — TechCrunch, 2024-10-31)
- **Apr 2026: $3.5B US-manufacturing expansion (SkyForge), ~$4.4B Series F.** Skydio raised $110M (Series F, valuation $4.4B) and announced a five-year $3.5B US investment plan — new manufacturing facility 5× current size, >2,000 direct jobs, >$1B to US suppliers. Core business described as generating "hundreds of millions of dollars in annual revenue" with strong margins. The SkyForge initiative is designed to keep drone technology and production inside the US. (`raw/research/company-status/04-skydio-skyforge.md` — DroneDJ, 2026-04-30)

**Implication for this page:** the original "consumer vision-only existence proof" framing (Skydio 2 / Jetson TX2, ~2020) remains valid as **historical evidence** that vision-only autonomy can ship commercially at scale. It is not a description of Skydio's current product or market position. Read the autonomy-stack content below as 2020-era architecture; treat current Skydio product capabilities as out of scope for this page.

## Sensor Architecture

Six fisheye 4K cameras provide full 360° coverage with no blind spots (*claimed*). No LiDAR, no ultrasonic, no event cameras. The vision-only stack is the deliberate commercial differentiator — see [[lidar-vs-vision-autonomy]] for where this sits in the broader debate.

No latency figures or algorithmic details are given in the source. Compute: NVIDIA Jetson TX2, fully onboard (*claimed*; TX2 is now aged hardware — significant temporal drift from this 2020-era source to current Skydio products).

## Spatial AI Capabilities

*Claimed* capabilities (vendor framing; no independent verification in source):

- **Real-time 3D mapping** — continuous environmental model built from camera feeds.
- **Context-aware object recognition** — infers partially-visible obstacles, e.g. extrapolates the extent of a partially-visible cable. This is notable because it implies semantic reasoning beyond pure geometry.
- **Motion prediction** — anticipates moving obstacles, enabling "bob and weave" style avoidance.
- **360° avoidance** — claimed to work in all directions simultaneously, with no zone gaps.

Subject tracking through dense obstacle fields is the marquee demo claim. GPS-denied operation is implied by the onboard-only architecture but not explicitly stated in the source.

## Workflows and Deployments

- **3D Scan / House Scan** — structured inspection workflows using the obstacle-avoidance stack.
- **Civil Air Patrol urban SAR** — cited as a real-world deployment. This is the strongest evidence in the source of operational use.
- "Up to 40% TCO reduction" and "80% budget on pilots" — unattributed marketing figures; treat as illustrative, not verified.

## Caveats and Failure Modes Not Addressed

The source never engages with vision failure modes: low light, textureless surfaces, rain, fog, direct sun glare, or motion blur at speed. These are known hard cases for purely visual [[visual-inertial-slam]] and obstacle avoidance pipelines. The vendor framing presents vision-only as unambiguously superior; this is contested — see [[lidar-vs-vision-autonomy]].

No regulatory or [[faa-part-108-bvlos]] context is provided; the source predates the BVLOS rulemaking. The TX2 compute platform is materially dated relative to current Skydio hardware.

As a commercial vision-only autonomous drone shipping at scale, Skydio 2 is the primary existence proof for the "vision-only is sufficient for commercial autonomy" position in [[lidar-vs-vision-autonomy]]. The [[anduril-lattice]] stack represents a sensor-fusion-heavy, multi-modal architecture vs. Skydio's sensor-minimal approach.

For sensor stack context, see [[drone-sensors-for-autonomy]]. For broader autonomy capability landscape, see [[drone-autonomy-state]].

## Source
- `raw/research/autonomy-and-sensors/08-skydio-autonomy-intro.md` — Skydio company blog (~2020, Skydio 2 era); primary vendor marketing, not independent review.
- `raw/research/company-status/02-skydio-x10d-blueuas.md` — DroneLife (2024-05-31): X10D added to DoD Blue UAS Cleared List, May 2024.
- `raw/research/company-status/03-skydio-battery-sanctions.md` — TechCrunch (2024-10-31): China sanctions / battery-supply squeeze, Oct 2024.
- `raw/research/company-status/04-skydio-skyforge.md` — DroneDJ (2026-04-30): $3.5B US manufacturing expansion (SkyForge), ~$4.4B Series F.

## Related
- [[lidar-vs-vision-autonomy]] — Skydio is the canonical commercial existence proof for the vision-only camp.
- [[visual-inertial-slam]] — underlying estimation paradigm the stack depends on.
- [[drone-sensors-for-autonomy]] — sensor modality landscape; Skydio's conspicuous absences (LiDAR, event) are notable.
- [[anduril-lattice]] — sensor-fusion-heavy multi-asset autonomy (defence-origin technology).
- [[drone-autonomy-state]] — where Skydio fits in the broader commercial autonomy landscape.
