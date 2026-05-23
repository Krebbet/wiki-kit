# Drone Agriculture Use Case

Precision aerial application — spraying, spreading, and crop monitoring — is the only commercial drone vertical with clearly demonstrated positive ROI at scale today, with 600,000+ DJI agricultural drones deployed globally and XAG reporting 20M+ hectares of cumulative treated area. The vertical is mature in Asia, Brazil, and parts of Oceania; regulatory drag (EU aerial-spray ban, US FCC covered-list blocking DJI/XAG imports) is the primary constraint on further growth.

## State of the Art

### DJI Agras Fleet — 600,000 Units *shipping at scale*

DJI Agriculture announced at Agrishow 2026 (Ribeirão Preto) that its global agricultural drone fleet crossed 600,000 units — a 50% increase from 400,000 at Agrishow 2025. Fleet operates in 100+ countries treating 300+ crop types, supported by 3,500 service centres and 7,000+ certified instructors. Environmental self-reported figures: ~410M tonnes of water saved (vs. 222M the prior year), 51M tonnes of carbon emissions cut. Targeted spot-spraying can reduce herbicide use up to 35% vs. broadcast application (DJI claim; vendor self-report). (Source: *06-dji-ag-600k*, DroneXL / Haye Kesteloo)

**Caveat:** All volume and environmental impact figures are DJI self-reported; no independent audit cited.

### DJI Agras T100/T70P/T25P — Current Generation *shipping at scale*

Launched mid-2025. T100: 100 L spray payload, 150 L spread, 100 kg lift, 20 m/s max speed; LiDAR + millimeter-wave radar + Penta-Vision obstacle avoidance. T70P: 70 L spray, 65 kg lift; Safety System 3.0 with millimeter-wave + Tri-Vision. T25P: compact/foldable; 25 kg high-precision spreading; suited for solo operators. Training available via DJI Academy in 15 countries (Americas + Asia). (*07-dji-agras-t100*, Unmanned Systems Technology)

### XAG — 20M Hectares Cumulative *shipping at scale*

XAG (founded 2007, Guangzhou) reported 20M+ hectares of accumulated crop protection drone service as of September 2019 — the earliest documented scale benchmark for the sector. A single-day record of 140,000 ha was set in August 2019. Operations span 38 countries including South Korea, Japan, Australia, Vietnam, Brazil, Mexico, and Zambia. Demonstrated applications: pest control (fall armyworm, 98% larval mortality rate in Guangxi maize fields in partnership with Bayer), cotton defoliation in Xinjiang (4.8M ha in one region in one season). XAG integrates drones with AI and IoT (partnerships with Alibaba, Huawei, Bayer, Harper Adams, Sydney University). (*08-xag-20m-ha*, XAG corporate)

**Caveat:** XAG figures are corporate announcements; the 20M ha number dates to 2019 — current scale is almost certainly higher but no updated figure was captured in this source set.

## ROI Comparison Across Verticals

Agriculture is the standout ROI-positive vertical because:
1. **Labour substitution is direct and measurable** — one drone operator covers area a ground crew cannot match in speed or precision.
2. **Input cost reduction is verifiable per-field** — reduced water use, herbicide reduction (up to 35% DJI claim), improved uniformity.
3. **No BVLOS required** — most ag spraying occurs VLOS or with very limited airspace interaction, keeping regulatory friction low.
4. **Repeat purchase cycles** — operators buy consumables (nozzles, batteries) and services, not just hardware.

## Regulatory Friction

- **US:** FCC added DJI, Autel, and XAG to its Covered List (Dec 22, 2025), blocking new equipment authorisations. American farmers cannot easily replace or expand these fleets. [[canadian-drone-onshoring]] tracks alternative sourcing.
- **EU:** 16-year aerial-spray ban (Directive 2009/128/EC) is being unwound via the Dec 2025 Food & Feed Safety Omnibus (Art. 9a exemption framework) and EASA SORA 2.5/PDRA-S01 update. Italy's enabling law (Law 182/2025) passed but implementing decree missed its March 2026 deadline; no product in Italy is yet labelled for drone application. France, Hungary, and Romania have national rules already in force. Full EU legislative resolution expected late 2026–early 2027. (*06-dji-ag-600k*)

## Gaps

- Independent ROI validation: no third-party longitudinal study across diverse crop/region combinations in the source set.
- US supply-chain gap: FCC covered-list creates a hardware void with no obvious short-term substitute at Agras-class payload.
- EU product labelling: even after airspace rules unlock, Regulation (EC) No 1107/2009 requires product-specific drone-application authorisation — a downstream bottleneck EFSA has not yet cleared.

## Source

- `06-dji-ag-600k.md` — DroneXL / Haye Kesteloo; DJI fleet milestone + EU regulatory update
- `07-dji-agras-t100.md` — Unmanned Systems Technology; T100/T70P/T25P specs
- `08-xag-20m-ha.md` — XAG corporate announcement; 20M ha milestone

## Related

- [[drone-commercial-verticals]]
- [[drone-autonomy-state]]
- [[drone-sensors-for-autonomy]]
- [[drone-power-budget]]
- [[canadian-drone-onshoring]]
- [[faa-part-108-bvlos]]
