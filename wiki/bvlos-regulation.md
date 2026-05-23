# BVLOS Regulation — US / Canada / EU

Three jurisdictions are converging on risk-based BVLOS frameworks, but at very different speeds. Transport Canada moved first: tiered BVLOS operations became certifiable (no per-flight SFOC) on 4 November 2025, with pilot and operator certificates replacing the legacy waiver process. EASA adopted SORA 2.5 in September 2025, deepening its risk-assessment pathway and U-space integration. The FAA's Part 108 NPRM closed October 2025; the final rule has slipped past its ~March–April 2026 target — TC's framework was explicitly cited as a Part-108 blueprint during FAA–TC bilateral talks in fall 2024.

---

## Comparison Table

| Dimension | Transport Canada (CARs Part IX) | EASA (EU 2019/947 + 2021/664) | FAA (Part 108) |
|---|---|---|---|
| **Legal instrument** | CARs Part IX, SOR/2025-70; Standard 922 (Safety Assurance); Standard 923 (Vision-Based DAA) | Reg (EU) 2019/947; SORA via ED Decision 2025/018/R (SORA 2.5, Sept 2025); U-space via Reg (EU) 2021/664 | Part 108 NPRM (released 7 Aug 2025); Part 107 waivers still operative |
| **BVLOS effective date** | **4 Nov 2025** — covered ops no longer require SFOC [*in-effect*] | SORA pathway in-effect; SORA 2.5 AMC adopted 29 Sept 2025 [*in-effect*]; U-space live in designated zones [*in-effect*] | Final rule: target ~Mar–Apr 2026, slipped; NPRM comment period closed 6 Oct 2025 [*proposed*] |
| **Pilot / operator cert** | Pilot: Level-1-Complex cert (age ≥18, Advanced exam + 20 h ground school + flight review; $125 fee). Operator: RPAS Operator Certificate (RPOC) with SMS, accountable executive, maintenance programme [*in-effect*] | Remote pilot competency per NAA authorisation; SORA SAIL level drives training OSOs; no single EU-wide pilot cert equivalent [*in-effect*] | Tiered pilot cert proposed; flight coordinator role for automated ops; specifics pending final rule [*proposed*] |
| **DAA requirement** | Standard 922.10: ARC-b/ARC-c system risk ratios; exception if operating per Standard 923 (vision-based DAA ≤4 NM) or atypical airspace (AC 903-001) [*in-effect*] | SORA OSO #08 / #09: DAA requirement scales with SAIL; M2 technical mitigation (enhanced containment) may substitute [*in-effect*] | DAA / automated systems implied by automation-first design; explicit consensus-standard references pending final rule [*proposed*] |
| **Airspace-integration mechanism** | Uncontrolled airspace ≤400 ft AGL; ≥5 NM from CFS/WAS aerodromes; NRC interactive BVLOS map; SFOC still required above 400 ft or in controlled airspace [*in-effect*] | U-space (Reg 2021/664): designated UAS geographic zones with mandatory U-space services (network ID, geo-awareness, flight authorisation, traffic info); first U-space service provider (ANRA Technologies) certified May 2025 [*in-effect*] | UTM / UAS Service Supplier (USS) framework inherited from Part 107; Part 108 proposes area-by-area FAA review [*proposed*] |
| **Status** | **Operational** — covered lower-risk BVLOS routes certifiable without SFOC since 4 Nov 2025 | **Operational** — SORA pathway live; SORA 2.5 simplifications in effect; U-space pilots running | **Rulemaking** — NPRM stage; waiver-based Part 107 §107.31 remains only operative BVLOS path |

---

## Transport Canada

### Framework

Canada's expanded drone regulations (SOR/2025-70) came into force in two phases: exam / RPOC applications opened 1 April 2025; BVLOS, EVLOS, and sheltered operations activated **4 November 2025**.[^tc-summary] The amendment moves lower-risk BVLOS from case-by-case SFOCs to a certifiable, standing-authorisation model — the structural change that makes commercial-scale BVLOS economically viable.

### Pilot Certification — Level-1-Complex

The Level-1-Complex certificate is the gateway to BVLOS.[^tc-l1c] Requirements: age ≥18; pass the standard Advanced exam; complete ≥20 hours of ground school at an approved flight school; pass the Level-1-Complex online exam; pass a Level-1-Complex flight review. Fee: CAD $125 (cert does not expire, but recurrency applies). Pilots must also fly under an RPOC-holding organisation.

### Operator Certificate (RPOC)

The RPAS Operator Certificate requires an operations manual (AC 901-002 template), maintenance control manual, Safety Management System, accountable executive, and documented training programme.[^tc-ac] This organisational layer mirrors an Air Operator Certificate in manned aviation and is the mechanism that gives BVLOS industrial legitimacy.

### Airspace and Operational Scope

Covered lower-risk BVLOS operations must:[^tc-l1c]

- Remain in **uncontrolled airspace** (Class G)
- Stay **≤400 ft (122 m) AGL**
- Remain **≥5 NM** from aerodromes listed in the Canadian Flight Supplement or Water Aerodrome Supplement
- Small drone over unpopulated area (>1 km from populated area): Standard Declaration
- Small drone over sparsely populated area (5–25 persons/km²) or <1 km from populated area: **Pre-Validated Declaration** (fee CAD $1,200; requires acceptance letter)
- Medium drone (>25 kg–150 kg) over unpopulated area: Standard Declaration

The NRC Drone Site Selection Tool 2.0 provides an interactive map for operational planning.[^tc-dz4]

### Safety Assurance — Standard 922

Standard 922 defines the technical requirements that must be met before a Safety Assurance Declaration can be submitted.[^std922] Key sections:

- **922.08 Containment** — low robustness (small BVLOS) to high robustness (medium BVLOS or near-populated areas)
- **922.09 C2 Link** — combined failure probability of losing control must be remote
- **922.10 DAA** — ARC-b (≤0.66 system risk ratio, >5 NM from aerodrome, Class G) or ARC-c (≤0.33, nearer or in advisory airspace); waived if operating under Standard 923 (vision-based DAA) or in atypical airspace per AC 903-001
- **922.12 Environmental Envelope** — demonstrated by ground and flight test

### DAA — Standard 923 (Vision-Based)

Standard 923 provides an alternative DAA pathway using onboard vision-based detection, waiving the Standard 922.10 electronic DAA requirement.[^std922] This is the operative "visual observer or vision-based DAA" equivalence in TC's regime.

### Why TC Led

TC's SFOC feedback-loop — operators were required to report what worked — accelerated evidence gathering.[^autonomy] Bilateral FAA–TC discussions in fall 2024 are documented to have influenced the Part 108 NPRM's tiered structure, RPOC-style SMS requirement, and graduated certification ladder.[^autonomy]

---

## EASA

### Regulatory Hierarchy

EASA's BVLOS framework sits within the **Specific category** under Commission Implementing Regulation (EU) 2019/947. Three pathways exist:

1. **Standard Scenarios (STS)** — predefined low-risk ops; declaration only; narrowest operational envelope
2. **Predefined Risk Assessment (PDRA)** — EASA has pre-completed the SORA; operator files a checklist-style table and operations manual; NAA issues authorisation[^easa-pdra]
3. **Full SORA** — operator conducts 10-step risk assessment; NAA issues operational authorisation[^easa-sora]

Published PDRAs cover agricultural work and cargo (PDRA-S01, S02), surveillance and long-range cargo (PDRA-G01, G02), and linear inspection (PDRA-G03).[^easa-pdra]

### SORA 2.5 — ED Decision 2025/018/R

On 29 September 2025, EASA adopted ED Decision 2025/018/R, introducing SORA 2.5 as AMC/GM Issue 1, Amendment 4 to Reg (EU) 2019/947.[^easa-sora25] SORA 2.5 (developed by JARUS) introduces simplifications while maintaining safety objectives and improves harmonisation across EU member states. Design compliance is scaled by SAIL:

- SAIL I–II: manufacturer/operator declaration
- SAIL III: SAIL III MoC compliance
- SAIL IV: EASA Design Verification Report (DVR)
- SAIL V–VI: full EASA type certificate under Reg (EU) 748/2012

### U-space — Reg (EU) 2021/664

U-space creates mandatory digital airspace management within designated UAS geographic zones.[^easa-uspace] Operators in U-space must use certified U-space services: network identification, geo-awareness, flight authorisation, and traffic information. ANRA Technologies became the first EASA-certified U-space service provider in May 2025.[^easa-uspace-news] U-space is the EU's primary mechanism for enabling BVLOS at scale by replacing ad-hoc coordination with automated, real-time deconfliction.

### Status

The SORA specific-category pathway is **in-effect** across all EU member states. SORA 2.5 simplifications are live. U-space deployment is expanding but depends on member-state designation of UAS geographic zones; implementation is uneven. No single EU-wide "BVLOS certificate" equivalent to TC's Level-1-Complex exists — authorisation is operation-and-drone-specific via the NAA.

---

## FAA

The FAA's BVLOS framework is detailed at [[faa-part-108-bvlos]]; only the cross-jurisdictional context is recorded here.

The **Part 108 NPRM** was released 7 August 2025 after years of waiver-only operations under Part 107 §107.31.[^dlapiper] The 700+ page proposal received >3,000 public comments before the 6 October 2025 close. Key unresolved tensions: prohibition on manual pilot-in-the-loop control; SMS burden on small operators; area-by-area FAA approval (seen as recreating a waiver system); country-of-origin restrictions (§108.700) that would exclude most current fleets; ADS-B Out prohibition creating one-way visibility gaps for manned aviation.[^dlapiper]

Under the Executive Order timeline, a final rule was expected by ~March–April 2026. Given the volume of substantive comments and FAA resource constraints, that deadline has slipped.[^dlapiper] Part 107 §107.31 waivers remain the only operative US BVLOS pathway. [*proposed*]

---

## Source

| # | Source | URL | Captured |
|---|---|---|---|
| 1 | TC — 2025 Summary of changes | https://tc.canada.ca/en/aviation/drone-safety/2025-summary-changes-canada-drone-regulations | 2026-05-23 |
| 2 | TC — Level-1-Complex operations | https://tc.canada.ca/en/aviation/drone-safety/learn-rules-you-fly-your-drone/drone-operation-categories-pilot-certificates/level-1-complex-operations | 2026-05-23 |
| 3 | TC — Standard 922 RPAS Safety Assurance (CARs) | https://tc.canada.ca/en/corporate-services/acts-regulations/list-regulations/canadian-aviation-regulations-sor-96-433/standards/standard-922-rpas-safety-assurance | 2026-05-23 |
| 4 | TC — AC 901-002 RPOC Manual Guidance | https://tc.canada.ca/en/aviation/reference-centre/advisory-circulars/advisory-circular-ac-no-901-002 | 2026-05-23 |
| 5 | TC — Drone Zone Issue 4 (Nov 2025) | https://tc.canada.ca/en/aviation/drone-safety/drone-zone/drone-zone-issue-4-november-2025 | 2026-05-23 |
| 6 | EASA — SORA overview | https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/specific-category-civil-drones/specific-operations-risk-assessment-sora | 2026-05-23 |
| 7 | EASA — PDRA overview | https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/specific-category-civil-drones/predefined-risk-assessment-pdra | 2026-05-23 |
| 8 | EASA — ED Decision 2025/018/R (SORA 2.5) | https://www.easa.europa.eu/en/document-library/agency-decisions/ed-decision-2025018r | 2026-05-23 |
| 9 | EASA — Easy Access Rules for U-space (Reg EU 2021/664) | https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-u-space-regulation-eu-2021664 | 2026-05-23 |
| 10 | Autonomy Global — How Canada's Drone Regs Inspired Part 108 | https://www.autonomyglobal.co/how-canadas-drone-regulations-inspired-the-faas-part-108-bvlos-rule/ | 2026-05-23 |
| 11 | DLA Piper — FAA Part 108 NPRM: Industry Response | https://www.dlapiper.com/en-us/insights/publications/2025/10/faa-proposed-part-108-bvlos-rule | 2026-05-23 |

[^tc-summary]: TC, "2025 Summary of changes to Canada's drone regulations," source 1.
[^tc-l1c]: TC, "Level-1-Complex operations," source 2.
[^std922]: TC, "Standard 922 RPAS Safety Assurance," source 3.
[^tc-ac]: TC, "AC 901-002 RPOC Manual Guidance," source 4.
[^tc-dz4]: TC, "Drone Zone Issue 4 — November 2025," source 5.
[^easa-sora]: EASA, "SORA overview," source 6.
[^easa-pdra]: EASA, "PDRA overview," source 7.
[^easa-sora25]: EASA, "ED Decision 2025/018/R," source 8.
[^easa-uspace]: EASA, "Easy Access Rules for U-space," source 9.
[^easa-uspace-news]: EASA press release May 2025 linked from source 9.
[^autonomy]: Autonomy Global, "How Canada's Drone Regulations Inspired the FAA's Part 108 BVLOS Rule," source 10.
[^dlapiper]: DLA Piper, "FAA's proposed Part 108 BVLOS Rule: Industry response and key concerns," source 11.

---

## Related

- [[faa-part-108-bvlos]] — US-specific deep-dive on Part 108 NPRM, timeline, and industry concerns
- [[detect-and-avoid]] — DAA technology (Standard 922.10 / 923 requirements map here)
- [[canadian-drone-onshoring]] — TC's Safety Assurance Declaration as a manufacturing advantage; why Standard 922 compliance is the Canadian market-access lever
- [[drone-commercial-verticals]] — BVLOS is the gate that unlocks delivery, corridor inspection, and precision-ag at scale
- [[drone-autonomy-state]] — autonomy maturity context for BVLOS automation requirements
