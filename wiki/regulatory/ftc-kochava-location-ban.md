# FTC v. Kochava: Permanent Sensitive-Location-Data Ban (2026)

The FTC's stipulated final order against Kochava Inc. and its subsidiary Collective Data Solutions (~June 26, 2026) permanently prohibits the defendants from selling, licensing, transferring, sharing, or disclosing sensitive location data — including derived products that could infer visits to sensitive sites — without affirmative express opt-in consent, and only when that data is used solely for a service directly requested by the consumer. This is the first permanent prohibition of this scope against a third-party location data broker and marks a structural shift in what downstream buyers can legally receive without tracing consent back to the device owner.

## The Prohibition

Kochava and Collective Data Solutions are permanently barred from any commercial disposition of sensitive location data absent: (1) affirmative express opt-in consent from the data subject, and (2) restriction of that data's use to a service directly requested by that subject. "Derived products" — inferences, aggregated signals, or geofence-based flags that could indicate a visit to a sensitive location — fall within the ban. The order rejects Kochava's 2022 argument that app-store-sourced location data is not inherently sensitive; the nature of the inferred destination, not the original collection channel, controls.

## Sensitive Location Categories

The order mandates a minimum list of sensitive location categories that the defendants must protect. The Trump-era FTC narrowed the Biden-era draft, dropping labor union offices and LGBTQ+-predominant locations; the categories that survived:

- Mental health and addiction recovery facilities
- Reproductive health clinics (including abortion providers)
- Places of worship
- Domestic violence shelters
- Homeless shelters
- Military and federal law enforcement installations
- Schools and childcare providers

The list defines the floor for the defendants' internal curated address/geofence registry, reviewed annually. It is not a public registry — it is an internal compliance instrument.

## Compliance Program Requirements

The order imposes a structured operational compliance regime:

- **Sensitive Location Data Program:** Written program with a curated address/geofence list covering all mandated categories, reviewed and updated at least annually.
- **Supplier Assessment Program:** Defendants must verify upstream consent before ingesting third-party data and must cease use of any data where consent cannot be confirmed.
- **FTC incident reporting:** Third-party violations of the order's data-handling terms must be reported to the FTC.
- **Data retention and deletion:** A formal schedule is required; non-consented sensitive location data must be deleted.
- **Consumer rights:** Consumers have the right to learn which businesses received their data and to withdraw consent via an accessible mechanism.

## Tooling Hook: Compliance-Checklist Seed

The mandated categories list is directly usable as a seed for counter-tools. Any tool that helps consumers assess which apps or data brokers hold location data touching sensitive categories can map its checklist to this taxonomy — giving it regulatory grounding rather than relying on ad hoc classification.

The supplier consent-chain requirement creates an upstream DSAR pathway: if a downstream buyer must confirm consent traces back to the device owner, a consumer assertion of non-consent (or a demand to see the consent record) becomes an operational problem for the entire supply chain, not just the original collector. This parallels the upstream audit pressure created by consent-decree structures in other data markets (see [[regulatory/agristats-consent-decree]]).

Limitation: the compliance apparatus is internal and operational. There is no public registry of covered geofences, no mandatory public disclosure of which businesses received data, and no private right of action. Counter-tools cannot query Kochava's compliance list directly — they must reconstruct equivalent taxonomy independently or use the order's consumer-rights provisions as a lever.

## Context: First Permanent Location-Data-Broker Ban

Kochava challenged the FTC's original 2022 complaint, arguing that location data sourced from app stores was not inherently sensitive. The 2026 final order repudiates that position: sensitivity is determined by what the location reveals about a person's activities, not by the data's technical provenance. That framing — destination-sensitivity rather than collection-channel sensitivity — is the doctrinal move that makes the order broadly applicable and potentially extensible to other brokers operating the same model.

No prior FTC action had permanently prohibited a third-party data broker (as opposed to a first-party collector) from selling location data of this type. The combination of permanent prohibition, mandatory consent chain, and downstream consumer rights creates a compliance structure that buyers — advertisers, political campaigns, hedge funds, insurers — must now account for when sourcing location data from any broker operating in this market.

## Source

- FTC press release (captured 2026-06-29): `raw/research/weekly-2026-06-29/02-ftc-kochava-location-ban.md`
- FTC v. Kochava, Inc. — stipulated final order, ~June 26, 2026
- URL: https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-ban-kochava-subsidiary-selling-sensitive-location-data-settle-charges-they-sold-location-data

## Related

- [[counter-power/regulatory-responses]] — regulatory enforcement survey
- [[regulatory/agristats-consent-decree]] — parallel consent-decree / data-hub pattern
- [[mechanisms/dsar-and-data-deletion]] — supplier consent-chain as upstream DSAR pathway
- [[mechanisms/browser-fingerprinting]] — location tracking technology context
- [[strategies/data-disruption-strategy-map]] — sensitive-location-ban as tooling lever
