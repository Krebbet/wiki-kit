# Drone Mapping & Surveying Use Case

Photogrammetry and aerial survey is the most mature commercial drone vertical and faces the lowest regulatory friction: most operations are VLOS, under Part 107, and require no waiver. Drone photogrammetry produces higher point-density surface models than traditional ground methods in a fraction of the time, with the operator remaining clear of hazardous areas (active haul roads, unstable pile slopes, energised substations). Platform consolidation is underway around DroneDeploy, Pix4D, and Propeller.

## State of the Art

### Mining — Stockpile Measurement *shipping at scale*

Drone photogrammetry for mine stockpile volume and tonnage calculation is an established, repeated workflow. A drone flies an automated path over a pile, capturing overlapping images; processing software (e.g., DroneDeploy Aerial) generates point clouds, digital terrain models, and orthomosaics within the same day. Key advantages over total station or terrestrial laser scanning: full pile surface coverage including irregular geometries and overhanging edges; operator safety (no proximity to haul roads); repeatable saved flight plans that eliminate operator variability; and AI-powered volume calculations at audit-grade accuracy.

DroneDeploy's stockpile workflow outputs net volume (cubic metres/yards), tonnage (volume × material bulk density factor), and time-series change maps — all in formats compatible with mine planning and GIS software (GeoTIFF, LAS/LAZ, DXF/XML). Survey frequency scales to financial reporting cycles (weekly for high-throughput operations; monthly for slower-moving piles) without adding survey-crew labour. Ground control points (GCPs) plus RTK positioning anchor models to real-world coordinates. (*11-dronedeploy-mining*, DroneDeploy blog)

### Key Platforms

| Platform | Focus | Notes |
|---|---|---|
| DroneDeploy Aerial | Mining, construction, agriculture | Automated flight planning, centralised multi-site storage, AI volume calc |
| Pix4D | General photogrammetry | Industry-standard desktop + cloud processing |
| Propeller | Earthworks / civil construction | Specialises in progress tracking and haul-road monitoring |

### Construction

Progress tracking, as-built vs. design conformance, cut/fill calculations, and earthwork volume reporting are standard drone deliverables on large civil construction sites. Drone surveys replace or supplement traditional survey-grade instruments for interim reporting; final as-built surveys typically still use RTK GPS or total station for regulatory acceptance.

### Telecoms / Energy Infrastructure

Tower and transmission-line inspection uses photogrammetry outputs (point clouds, orthomosaics) for structural assessment and clearance measurement. This overlaps with [[drone-inspection-use-case]] but is distinguished by the emphasis on 3D model output rather than real-time anomaly detection.

## Why Mapping Leads on Maturity

1. **VLOS-compatible**: most stockpile and construction surveys occur within visual line of sight; no waiver required.
2. **Clear deliverable format**: volume numbers, orthomosaics, and point clouds slot directly into existing engineering and finance workflows.
3. **Measurable ROI**: survey-time reduction from hours (total station) to minutes (drone) is unambiguous; safety benefit (no personnel on active haul roads) is concrete.
4. **Regulatory acceptance**: photogrammetry outputs are accepted for financial audits and regulatory reporting in mining and construction, normalising the technology.

## Accuracy Considerations

The largest single source of volume error is reference-surface selection (flat-plane vs. lowest-perimeter vs. custom terrain), not sensor accuracy. Consistent methodology across surveys matters more than absolute precision. Material density variation (moisture, compaction) is the dominant tonnage uncertainty and requires periodic physical testing to correct — no drone sensor addresses this. (*11-dronedeploy-mining*)

## Gaps

- Survey-grade regulatory acceptance: in some jurisdictions, only licensed surveyors using certified instruments can sign off on legal boundary or as-built surveys — drone photogrammetry is accepted for interim but not final submissions.
- Steep-face coverage: overhanging pile edges and near-vertical faces produce coverage gaps requiring supplemental ground-level imagery.
- Real-time volume: current workflows are batch (fly → process → report same day); real-time volumetric feedback during active earthmoving is not yet standard.

## Source

- `11-dronedeploy-mining.md` — DroneDeploy blog; stockpile survey methods and best practices

## Related

- [[drone-commercial-verticals]]
- [[drone-inspection-use-case]]
- [[drone-autonomy-state]]
- [[drone-sensors-for-autonomy]]
- [[faa-part-108-bvlos]]
