# Canadian Drone Onshoring

The state of Canadian domestic drone manufacturing and the 2026 push to onshore production. Honest synthesis: **Canada's domestic capacity is thin and structurally weak — fewer than ~20 manufacturers, predominantly assemblers of imported components — but a large federal funding wave landed in 2026.** The money is arriving; the structural gaps (component supply chain, IP retention, procurement reliability) are deep and the policy instruments are announced-not-proven. Scope note: the underlying corpus is heavily defence-framed (Defence Industrial Strategy / NATO / CAF procurement); this page extracts the **manufacturing, economic, supply-chain and dual-use commercialization** substance and deliberately excludes defence-procurement politics. Structural/component detail and named companies live on [[drone-manufacturing-supply-chain]].

## The 2026 federal funding wave *(synthesis of gov primaries + trade-press corroboration)*

| Instrument | Amount | Notes | Source |
|---|---|---|---|
| NRC envelope (Defence Industrial Strategy) | **>$900M** | Announced Mar 2026; drones/UAS a named priority | `01`, `03` |
| Aerospace / autonomous-systems bucket | **>$500M** | Includes the Drone Innovation Hub + a Bombardier Global 6500 research aircraft | `03` |
| Drone Innovation Hub | **$105M / 3 yr** | Ottawa + Mirabel; 3 priority areas (drone & counter-drone; living lab; autonomous flight); commercialization + qualification pathway; sovereign RPAS supply-chain mandate | `02` |
| NRC IRAP "Defence Industry Assist" (DI Assist) | **$241M** | Launched Jan 2026; cash + advisory for Canadian **SMEs** building made-in-Canada dual-use tech; IRAP already reaches ~10,000 SMEs/yr | `03` |
| Quantum / biomedical (non-drone, for envelope reconciliation) | $161M / $28M | — | `03`, `12` |
| BDC defence-tech capital platform | **$4B** | Separate but linked; Minister Joly flagged *duplication risk* with NRC | `01`, `12` |

*(editorial)* Arithmetic flag: BetaKit's component sum (~$930M) slightly overruns the stated >$900M envelope — likely rounding/overlap; not asserted as exact. `12` (BetaKit) independently corroborates `02`/`03` and adds Canadian Council of Innovators' "details will matter / IP-and-talent anchoring" caution.

## Market baseline *(analyst — caveat co-located)*

NAV CANADA's first RPAS/AAM study (`06`): Canadian drone sector **$2.4–3.6B GDP / ~30K jobs (2024) → >$69B / >290K jobs by 2045**, fleet **~24K → ~507K aircraft**, BVLOS becoming the dominant mode within a decade; a claimed 50–70% cost-saving for automated solutions (**no disclosed methodology**). ⚠ *Credibility caveat:* NAV CANADA has a direct financial interest in large drone-traffic volumes (RTM fee revenue) and the study is advocacy-adjacent — treat as order-of-magnitude, not forecast. This is the demand-magnitude argument an onshoring case cites; the study itself makes **no supply-side or domestic-sourcing argument**.

## Demand-side & regulatory readiness

Transport Canada Drone Zone #5 (Dec 2025, `04`), hard snapshot: **116,304 registered drones**; pilot certs **128,888 Basic / 20,138 Advanced / 249 Level-1-Complex**; **368 active RPOCs**; 1,328 flight reviewers. *(synthesis)* The thin Complex-cert count (249) signals a nascent BVLOS-capable operator market. The CAR 901.194 / Std 922 **Safety Assurance Declaration** for Advanced Ops is a structural advantage for a domestic OEM that holds the declaration over an importer that may not. Canada appears ~12–18 months behind the US on BVLOS normalisation (contrast [[faa-part-108-bvlos]] / [[detect-and-avoid]]); regulatory analysis (`07`, thin) notes 2025 CARs reform *intent* to drop SFOCs for lower-risk BVLOS but no rule text.

## Drivers

Supply-chain de-risking vs China/DJI (DJI ~70% global consumer share framed as a disruption/kill-switch risk, `07`/`11`); sovereignty + procurement pull (NRC/DND as anchor client, dual-use commercialization mandate); a large projected market (`06`); 2026 funding + a federal industrial-policy tailwind (`13`).

## Gaps & constraints *(synthesis — the load-bearing finding)*

- **Assembler economy, not OEM** (`11`): firms import motors, batteries, carbon fibre, optics and integrate; no domestic subsystem supply chain. Component/chip/NPU dependency is the deepest gap.
- **IP erosion via foreign acquisition** (`11`): validated Canadian OEMs sell out rather than scale — Aeryon Labs → FLIR ($265M; independently corroborated), Deep Trekker cited alongside. Licensing foreign designs is the symptomatic dependency trap.
- **Procurement unreliability / no programs of record** (`13`, `11`): JUSTAS ran ~33 years with no RFP, ending in an off-the-shelf US buy (11× MQ-9, $2.49B); emergency-acquisition agility used abroad can't be applied domestically. The US DoD program-of-record model is the explicit contrast.
- **Capital** (`13`): no defence/deep-tech-specialised investment culture; SR&ED covers prototyping but nothing bridges validation → production scale. "Competency is here; capital and customers are the bottleneck" (One9, via `13`).
- **SME policy frictions** (`09`, InDro committee submission): certification cost/access, security-clearance friction, absent predictable procurement pathways, export-readiness. (Notably silent on component/capital/talent — a policy-layer voice, low evidentiary weight.)
- **Arctic technical gap** (`13`): −40 °C operation + degraded satellite links; Nordic adaptations are the unmet benchmark.
- *(editorial)* Talent is *not* the bottleneck per `11`/`13` — AI/comms competency is a stated Canadian strength; the gaps are structural (ownership, procurement, capital, components).

## Historical context

Canada had a real first-mover lead: Canadair (now Bombardier) fielded the CL-89/CL-289 among the first widely-used NATO UAVs (1960s–90s), then sold the systems to France/Germany in 1987 — ending ~25 years of leadership (`13`). The current onshoring push is, in effect, an attempt to rebuild a squandered position.

## Open items

- Funding instruments are **announced-not-proven**; revisit Hub operational status, DI Assist uptake, and whether dual-use/consumer firms (not just defence primes) actually access the money.
- ASTM/Canadian DAA standard maturity and the 2025 CARs BVLOS rule text are not yet captured (regulatory follow-up).

## Source

- `raw/research/canadian-onshoring/01-ised-defence-industrial-strategy.md` — ISED Defence Industrial Strategy (funding frame)
- `raw/research/canadian-onshoring/02-nrc-drone-innovation-hub.md` — NRC Drone Innovation Hub ($105M/3yr)
- `raw/research/canadian-onshoring/03-nrc-defence-programs-irap.md` — NRC programs / IRAP DI Assist ($ figures)
- `raw/research/canadian-onshoring/04-tc-drone-zone-5.md` — Transport Canada demand/cert snapshot
- `raw/research/canadian-onshoring/06-navcanada-rpas-market-study.md` — NAV CANADA market baseline (self-interest caveat)
- `raw/research/canadian-onshoring/07-gowling-2025-drones-canada.md` — regulatory/market-access context (thin; cite-only)
- `raw/research/canadian-onshoring/09-indro-defence-strategy-view.md` — InDro committee submission (practitioner policy gaps)
- `raw/research/canadian-onshoring/11-betakit-canada-drone-altitude.md` — structural-gap narrative (⚠ sponsored feature)
- `raw/research/canadian-onshoring/12-betakit-nrc-900m.md` — independent corroboration of 02/03
- `raw/research/canadian-onshoring/13-walrus-canada-drone-race.md` — long-form: lost lead, procurement paralysis, three-C
- `raw/research/canadian-onshoring/05-alberta-defence-mfg-backgrounder.md` — Alberta RDII datapoint (Canadian UAVs $3M)

## Related

- [[drone-manufacturing-supply-chain]] — the structural/component layer + named-company datapoints
- [[drone-autonomy-state]] — dual-use R&D context; software-over-hardware is where Canada is argued to differentiate
- [[faa-part-108-bvlos]] · [[detect-and-avoid]] — US BVLOS pace, the contrast Canada lags ~12–18 mo behind
