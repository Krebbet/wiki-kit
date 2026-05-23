# Drone Delivery Use Case

Last-mile drone delivery has crossed 2 million cumulative commercial deliveries (Zipline, Jan 2026) and attracted Barclays' projection of $16B in unlocked annual profit across global food delivery at scale — but unit economics remain deeply subsidised in consumer markets, BVLOS is a hard regulatory gate in the US, and only one operator (Manna, Ireland) credibly claims per-delivery profitability today.

## State of the Art

### Zipline — Medical and Consumer *shipping at scale*

Zipline operates fixed-wing platforms on four continents, surpassing 2 million commercial deliveries (Jan 2026) across >5,000 hospitals and health facilities, with 125 million autonomous commercial miles and zero serious injuries. US consumer rollout (Dallas–Fort Worth via Walmart) uses Platform 2: a five-motor hybrid VTOL with ~8 lb payload, tethered "Zip" droid with "dinner plate-level accuracy," median 3-minute flight time. Weekly delivery growth ~15% for seven months; new sites reach 100 deliveries/day in 2 days vs. 10 weeks for the first Dallas site. Valuation $7.6B on a $600M raise (Jan 2026); expanding to Houston and Phoenix in 2026. (*03-zipline-2m*)

### Unit Economics — The Subsidy Problem

Amazon Prime Air's internal projections (reported 2024) show ~$63 per-delivery cost while charging $9.99–$14.99 — a gap that only closes through order-of-magnitude scale compression. McKinsey (2023) estimated single-package drone delivery at $13.50, vs. $9–11 for electric/gas ground delivery. Zipline's CEO claims a $1/delivery target at scale; Manna (Dublin) claims $4/delivery now with a path to $1, making it the only operator asserting current per-delivery profitability — via hot-swap batteries, single operators managing up to 20 drones, and a lean model on $64M total raised vs. competitors' hundreds of millions. Consumer delivery in the US remains venture-subsidised. (*04-zipline-economics*)

### Barclays $16B Projection *claimed*

Barclays (Apr 2026) models autonomous delivery (drones + sidewalk robots combined) currently at $5–7/drop in high-labor markets, beating human riders by $3–4. Long-term target: ~$1/drop, implying $8–9 savings/order. At forecast penetration (~10% of global food delivery by 2035, vs. <1% today), $4 average savings/drop translates to ~$16B in annual unlocked profit. Named beneficiaries: DoorDash, Meituan near-term; Uber, Prosus, Delivery Hero medium-term. Key caveat: Barclays bundles drones and sidewalk robots; drones dominate suburban runs while robots address dense urban cores. (*12-barclays-16b*)

### Competitive Landscape (US, 2026)

BVLOS-authorised US operators: Wing, Amazon Prime Air, Zipline, Flytrex. Wing runs commercial service in Charlotte and Atlanta (via DoorDash) and Houston (via Walmart, targeting 270 stores by 2027). Flytrex holds FAA BVLOS auth; targets 37 largest US metros (>100M Americans). DoorDash runs Wing + Flytrex in parallel. Amazon Prime Air had six documented incidents in 2025 (Oregon crashes Jan, pool drop Jul, crane collision Oct, Waco cable strike Nov), contrasting sharply with Zipline's safety record. (*04-zipline-economics*, *12-barclays-16b*)

## Autonomy Requirements

| Requirement | Status |
|---|---|
| BVLOS authorisation | Hard gate; only 4 US operators hold it |
| UTM / multi-operator airspace | In-progress; Wing + Flytrex share DFW airspace |
| Payload: 6–9 lb per drop | Current fleet boundary; next-gen targeting 8.8 lb |
| AI dispatch, routing, conflict avoidance | Deployed at Zipline, Wing scale |

## Gaps

- Unit economics: no US consumer operator has demonstrated profitability without VC subsidy.
- BVLOS throughput: FAA's site-by-site waiver process cannot scale to metro-wide deployment under current rules; [[faa-part-108-bvlos]] rulemaking is the unlock.
- Public acceptance and noise: each new metro requires community engagement; not automatable.
- UTM maturity: multi-operator shared airspace is nascent; a dependency for any dense suburban rollout.

## Source

- `03-zipline-2m.md` — Zipline press release; 2M deliveries, $7.6B valuation
- `04-zipline-economics.md` — DroneXL / Haye Kesteloo; unit economics analysis
- `12-barclays-16b.md` — DroneXL / Rafael Suárez; Barclays research note

## Related

- [[drone-commercial-verticals]]
- [[faa-part-108-bvlos]]
- [[bvlos-regulation]]
- [[drone-autonomy-state]]
- [[detect-and-avoid]]
