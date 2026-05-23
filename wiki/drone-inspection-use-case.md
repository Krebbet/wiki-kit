# Drone Inspection Use Case

Autonomous drones are displacing manual inspection across oil & gas, electric utilities, and telecoms: drone-in-a-box platforms conduct scheduled BVLOS missions, AI detects anomalies in real time, and results feed directly into compliance workflows — reducing truck rolls, field exposure, and detection-to-repair time. Two regulatory milestones define the frontier: FAA BVLOS waivers (site-specific, slow to obtain) and EPA Alternative Test Method authorisation (now granted to at least one OGI system).

## State of the Art

### Oil & Gas — Percepto × Chevron *shipping at scale*

Percepto's Autonomous Inspection & Monitoring (AIM) platform deploys drone-in-a-box units at Chevron's Permian Basin (West Texas) and Rocky Mountain (Colorado) shale assets. Each quadcopter carries an optical gas imaging (OGI) camera plus RGB camera; the base station handles automatic charging, data upload, HVAC, and a weather station. Missions are dispatched from Percepto's West Palm Beach operations centre and from Chevron control rooms in Houston, West Texas, and Colorado. Percepto holds an FAA canopy waiver for Class G BVLOS operations across all US sites; "base hopping" extends coverage across multiple charge stations. Programme manager Russell Robinson (Chevron) noted results are "in line with or above expectations" after six months, with conversations already turning to national scale-up. (*01-percepto-chevron*)

### EPA-Authorised Methane Detection *shipping at scale*

The EPA approved Percepto's OGI drone system as an Alternative Test Method under Subparts OOOOa and OOOOb of the Clean Air Act, enabling remote federal-compliance inspections without field teams. Detection floor: <1 kg/hr; validated at 100 g/hr (90% reliability) in controlled METEC testing; 300 g/hr in high-wind Permian field conditions. One early deployment across multiple upstream assets found >130 potential emission events in three months, saved >1,000 work hours, and freed two operators for other duties. System already meets New Mexico and Colorado state methane requirements. (*02-percepto-epa*)

### Electric Utilities — Skydio Dock *shipping at scale*

Skydio Dock deploys at substations for recurring gauge/switch inspection, post-incident response, and security patrol. Key differentiator: Skydio's Visual Positioning System and magnetometer-free autonomy allow flight inside energized substations where other drones cannot operate safely. A Midwest utility (>10-state grid) caught a faulty switch via elevated thermal profile from a scheduled Dock mission, enabling same-day replacement vs. a full switch-out — estimated saving of hundreds of thousands of dollars. Dominion Energy and New York Power Authority hold Skydio-assisted BVLOS waivers covering dozens of locations across multiple states. (*09-skydio-substation*)

American Electric Power (AEP Ohio) piloted drone inspections in 2025, covering ~4% of its distribution system in one year, identifying >150 tier-1 defects (limbs on lines, thermal anomalies), and collecting 400,000–500,000 images. AI post-processing by Levatas delivers results within 3–4 minutes post-flight. Data-volume bottleneck identified: a single analyst spent 500+ hours manually reviewing that year's imagery — automated defect recognition is the next gap. (*10-utility-inspection-ai*, source: Renewable Energy World / Skydio–AEP webinar)

## Autonomy Requirements

| Requirement | Status |
|---|---|
| BVLOS waiver (FAA) | Required; slow per-site process; Percepto and Skydio have each secured waivers |
| AI anomaly detection (OGI, thermal, RGB) | Deployed; Percepto AIM, Skydio+Levatas CV |
| Drone-in-a-box / auto-recharge | Deployed; both platforms |
| Magnetometer-free nav (substations) | Skydio VPS; required for energized environments |
| UTM / multi-drone coordination | Gap — not addressed in current deployments |

## Gaps

- BVLOS waiver throughput: FAA site-specific process bottlenecks national rollout.
- AI defect classification accuracy at scale: AEP Ohio's data-volume experience illustrates current human-review dependency.
- Multi-drone coordination in shared airspace above a single asset complex: not yet demonstrated in these deployments.
- Product-specific regulatory recognition beyond EPA OGI (e.g., OSHA, state-level equivalents).

## Source

- `01-percepto-chevron.md` — DroneLife / Jim Magill; Percepto × Chevron pilot
- `02-percepto-epa.md` — DroneLife; EPA OGI Alternative Test Method approval
- `09-skydio-substation.md` — Skydio blog; Dock at substations
- `10-utility-inspection-ai.md` — Renewable Energy World (Skydio/Levatas sponsored); AEP Ohio

## Related

- [[drone-commercial-verticals]]
- [[faa-part-108-bvlos]]
- [[bvlos-regulation]]
- [[drone-autonomy-state]]
- [[drone-sensors-for-autonomy]]
- [[detect-and-avoid]]
