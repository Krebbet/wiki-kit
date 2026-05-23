# Anduril Lattice — Multi-Asset Autonomy and Sensor Fusion (Defence-Origin Technology)

Lattice is Anduril's software-defined command, control, and autonomous coordination platform, demonstrated live in a journalist-witnessed scenario (Nov/Dec 2024). It showed a single operator directing a coordinated multi-drone pipeline via discrete mouse clicks, fusing data across heterogeneous sensor types in real time. The platform ingests sensor data from 10+ partner hardware types (*claimed*). Its core techniques — single-operator-controls-many-assets autonomy, human-on-the-loop control, and multi-source sensor fusion — are defence-origin capabilities with potential transfer relevance to consumer and commercial drone fleet autonomy.

*Country of origin: USA (Costa Mesa, CA). Defence-origin technology; included here only for consumer-transferable autonomy/sensor-fusion methods.*

## Demoed Pipeline (Reporter-Witnessed, Nov/Dec 2024)

The following was observed by an MIT Tech Review journalist at Anduril's facility — not a combat deployment, but an independent press account rather than vendor self-reporting:

1. Sentry tower (optical + radar) auto-detected an approaching ground vehicle.
2. Operator single-click → Ghost surveillance drone dispatched autonomously.
3. Ghost maintained track on the vehicle after the Sentry tower lost line-of-sight.
4. Second operator click → second drone dispatched; autonomously locked onto the tracked target.
5. The full end-to-end sequence was scripted and conducted in a controlled environment, not adversarial or operationally representative.

Entire sequence: one operator, one mouse, two clicks. This is *demoed* at Anduril's controlled site.

## Autonomy Model: Human-on-the-Loop

Every action in the pipeline is a discrete operator click — targeting is human-initiated, not machine-initiated. Anduril's stated framing: Lattice Mesh "surfaces information, it does not prescribe actions." Georgetown's Probasco (cited by journalist): fully autonomous lethal decision pipelines are explicitly blocked by current US policy. The human-on-the-loop model is the policy-compliant design, not a technical limitation.

## Sensor Fusion and Integration

Sensors fused in the demo:
- Sentry optical/radar tower
- Ghost video and telemetry
- On-site advanced radars (unspecified type)

Lattice Mesh ingests data from 10+ partner hardware platforms (*claimed*; architecture-level claim not independently verified beyond the demo). Palantir Maven Smart System integration is *shipping at scale* (Pentagon CDAO 3-yr contract, Dec 3 2024). "Train AI on exabytes including classified data" — stated ambition, not verified operational status (*claimed*).

For sensor modality context, see [[drone-sensors-for-autonomy]].

## Journalist Skepticism (from source)

The MIT Tech Review account explicitly notes:
- Scripted, controlled scenario at Anduril's own facility — not adversarial or operationally representative.
- DoD interoperability across services remains immature.

These caveats are load-bearing for interpreting the maturity of what was demonstrated.

## Technology Transfer Relevance to Consumer Fleet Autonomy

The Lattice architecture demonstrates techniques that are relevant to consumer and commercial multi-drone fleet operations, regardless of the original deployment context: single-operator control of multiple assets, human-on-the-loop tasking (operator initiates, system executes), and heterogeneous sensor fusion across radar, optical, and telemetry streams. The non-cooperative detection approach (Sentry radar + optical) also bears on the unsolved problem in civilian airspace: detecting non-broadcasting aircraft for [[detect-and-avoid]] purposes. The demo does not address FAA-compliant [[faa-part-108-bvlos]] airspace integration; applicability to civilian contexts requires separate evaluation.

For broader autonomous UAS capability context, see [[drone-autonomy-state]].

## Source
- `raw/research/autonomy-and-sensors/11-mittr-anduril-demo.md` — MIT Tech Review journalist account of a live Anduril Lattice demo, Nov/Dec 2024; independent press, not vendor copy.

## Related
- [[skydio-autonomy-stack]] — vision-only consumer autonomy stack; contrasts with Lattice's sensor-fusion-heavy architecture.
- [[detect-and-avoid]] — Lattice's non-cooperative detection approach (radar + optical) is relevant to the civilian DAA sensor gap.
- [[drone-autonomy-state]] — broader autonomy capability landscape.
- [[drone-sensors-for-autonomy]] — sensor modalities fused in the Lattice pipeline.
- [[faa-part-108-bvlos]] — civilian regulatory context; Lattice demo does not address this framework.
