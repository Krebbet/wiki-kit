# FairFare

FairFare is a crowdsourced data tool co-built with a Colorado rideshare union to estimate ride-platform take rates from driver-contributed trip data. Over 18 months, 45 drivers submitted 76,000+ trips; the resulting take-rate estimates fed directly into advocacy for Colorado Senate Bill 24-75 (algorithmic transparency for AI systems in employment). The tool is live at [getfairfare.org](https://getfairfare.org/).

**Significance for counter-power toolkit.** FairFare is the clearest deployed example of the crowdsourced-audit → legislation pathway: workers pool transactional data they already possess, compute an aggregate metric the platform withholds, and route findings through an organised labour partner into a legislative outcome. It is a Tier-1 build-or-adapt template for transparency tools in any sector with opaque algorithmic fee-setting.

## Mechanism

The platform withholds per-trip take rate from drivers (and riders). FairFare inverts this asymmetry: drivers install a lightweight tool, consent to share trip-level data, and the pooled dataset enables take-rate estimation at aggregate scale. The key design moves:

- **Data the workers already have.** No scraping or adversarial access needed; drivers receive trip receipts that carry fare and driver earnings.
- **Union as trust and recruitment layer.** The Colorado union partner handled driver recruitment, consent framing, and privacy safeguards; the tool team handled computation and publication.
- **Aggregate metric → legislative lever.** The output is a single interpretable number (take rate) legible to legislators and press; SB 24-75 language on algorithmic transparency was influenced by the FairFare dataset.

As of the paper (July 2025 revision, published in ACM Trans. CHI), deployment has expanded beyond the initial 76K trips.

## Design implications

- The centralised-crowdsource architecture (workers contribute data to a central compute) is the predecessor pattern to the decentralised [[opencourier-protocol]] model.
- The union-as-partner model differs from the worker-owned cooperative model ([[drivers-seat-cooperative]]); both are viable; union-partnered is faster to bootstrap, coop-owned is more durable.
- The metric choice (take rate) was selected for legislative legibility, not statistical richness — a useful design heuristic for future tools targeting policy channels.
- The Colorado dataset enabled SB 24-75; this provides primary evidence for the crowdsourced-audit → regulation pathway documented in [[regulatory-responses]].

## Source

- `raw/research/weekly-2026-06-22/01-fairfare.md`
  - **Origin:** Academic (arXiv 2502.11273, Feb 2025 / Jul 2025 v2; published ACM Trans. CHI 2026). Cornell / Princeton-affiliated authors including Andrés Monroy-Hernández and Danny Spitzberg.
  - **Audience:** HCI researchers and labor-tech practitioners.
  - **Purpose:** Document a deployed community-based audit tool and reflect on translating quantitative data into policy outcomes.
  - **Trust:** Peer-reviewed (ACM Trans. CHI); deployed tool with named policy outcome; high on empirical claims, partial on impact attribution.

## Related

- [[opencourier-protocol]] — protocol-layer evolution of FairFare's centralised crowdsource architecture
- [[drivers-seat-cooperative]] — worker-owned parallel; different governance (coop vs union-partnered)
- [[markup-citizen-browser]] — closest structural parallel (crowdsource → aggregate metric → accountability)
- [[transparency-tools]] — canonical community-based audit tool
- [[algorithmic-collective-action]] — empirical ACA case in the labour-organiser / policy channel
- [[regulatory-responses]] — CO SB 24-75 as documented crowdsourced-audit → legislation output
- [[regulatory/ilo-platform-worker-convention]] — ILO algorithmic transparency provisions; FairFare provides an audit-tooling hook
