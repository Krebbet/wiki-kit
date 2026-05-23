# Drone Commercial Verticals

Index of the four primary consumer/commercial drone verticals with demonstrated revenue or clear deployment evidence as of mid-2026. Defence and dual-use platforms are out of scope except where transferable technology is directly relevant to a commercial application.

---

## Verticals

### [[drone-inspection-use-case]] — Infrastructure Inspection

Drone-in-a-box platforms (Percepto AIM, Skydio Dock) run scheduled BVLOS missions over oil & gas facilities and electric substations, with AI anomaly detection (OGI methane, thermal, RGB) replacing manual inspection rounds. Percepto holds EPA Alternative Test Method authorisation for federal methane compliance; Skydio has assisted Dominion Energy and NYPA in obtaining multi-site BVLOS waivers. The FAA BVLOS waiver process is the primary scale bottleneck.

### [[drone-delivery-use-case]] — Last-Mile Logistics

Zipline leads with 2M+ commercial deliveries and a $7.6B valuation (Jan 2026). US BVLOS authorisation is held by four operators (Wing, Amazon Prime Air, Zipline, Flytrex). Consumer delivery economics remain VC-subsidised (Amazon ~$63/delivery cost vs. $10–15 price); Manna (Dublin) is the sole operator claiming per-delivery profitability (~$4/delivery). Barclays projects $16B in annual unlocked industry profit at ~10% autonomous penetration by 2035.

### [[drone-agriculture-use-case]] — Precision Ag / Spraying

The only unambiguously ROI-positive commercial vertical today. DJI Agriculture: 600,000 units deployed in 100+ countries (as of Agrishow 2026). XAG: 20M+ ha cumulative treated area (2019 baseline; current scale higher). Most operations are VLOS — no waiver required. US access is constrained by the FCC covered list (DJI, XAG, Autel blocked Dec 2025); EU is unwinding a 16-year aerial-spray ban via the 2025 Food & Feed Safety Omnibus, with full legislative resolution expected late 2026–early 2027.

### [[drone-mapping-surveying-use-case]] — Photogrammetry / Survey

The most mature vertical and the lowest regulatory friction: predominantly VLOS, Part 107, no waiver. DroneDeploy, Pix4D, and Propeller dominate the platform layer for mining stockpile measurement, construction progress tracking, and civil earthworks. Drone photogrammetry delivers higher point density than total-station or terrestrial-laser-scan methods in a fraction of the time, with operators clear of hazardous areas.

---

## Cross-Vertical Gaps

### BVLOS — The Shared Regulatory Gate

BVLOS authorisation is the single largest gap across inspection and delivery; mapping and agriculture largely avoid it. The FAA's current waiver process is site-specific and slow — not scalable to metro-level or multi-state deployment. [[faa-part-108-bvlos]] tracks the regulatory pathway. Until a performance-based BVLOS rule replaces the waiver regime, inspection and delivery are structurally capacity-constrained. See also [[bvlos-regulation]] for international context.

### Unit Economics — Subsidised Deployment vs. Real Profitability

Agriculture is the only vertical with clear unsubsidised profitability. Delivery is VC-subsidised at scale; inspection is sold as enterprise SaaS (Percepto, Skydio) with ROI framed around avoided truck-rolls and man-hour savings rather than per-delivery margin. Mapping/survey ROI is strong and measurable but operates at project rates competitive with traditional survey, not transformative margins. No delivery operator outside Manna has demonstrated per-delivery profitability at consumer price points.

### Public Acceptance

Delivery and inspection face community friction that agriculture and mapping largely avoid: noise above residential areas (delivery), visual surveillance concerns (inspection patrol), and airspace conflicts (both). These are non-technical constraints that do not yield to engineering solutions alone and will gate deployment timelines in dense areas regardless of regulatory approvals.

### Airspace / UTM Maturity

Multi-operator UTM is nascent. Wing and Flytrex sharing DFW airspace is an early proof-of-concept; no UTM framework exists at the scale needed for a city-wide multi-operator delivery network. [[detect-and-avoid]] capabilities for cooperative and non-cooperative traffic are a hard dependency. Without UTM, BVLOS authorisation for delivery effectively limits each operator to isolated corridors rather than a mesh.

---

## Related

- [[drone-inspection-use-case]]
- [[drone-delivery-use-case]]
- [[drone-agriculture-use-case]]
- [[drone-mapping-surveying-use-case]]
- [[faa-part-108-bvlos]]
- [[bvlos-regulation]]
- [[drone-autonomy-state]]
- [[detect-and-avoid]]
- [[canadian-drone-onshoring]]
