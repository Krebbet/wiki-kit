# FAA Part 108 BVLOS

FAA NPRM 14 CFR Part 108 (Docket FAA-2025-1908, Notice 25-07, ~731pp) is the first US regulatory framework proposing routine scalable commercial BVLOS drone operations, replacing the Part 107 waiver-by-waiver approach with a tiered permit/certificate structure. Issued under EO 14307 ("Unleashing American Drone Dominance," June 6 2025), the rule carries a ~240-day final-rule deadline (≈Feb 2026) with a 60-day public comment window (*requested comment*). All provisions below are *proposed rule* until finalized.

## Scope and Physical Limits (*proposed rule*)

- ≤400 ft AGL, ≤1,320 lb, ≤87 kt, ≤25 ft maximum dimension.
- Five population-density categories (Cat 1–5); Cat 5 = ≥2,500 people/cell (metro).
- Amends Parts 36/43/45/48/89/91/107/119/133/135/137/146; parallel TSA changes.

## DAA Requirements (*proposed rule*)

- §108.825: DAA system required for all BVLOS operations.
- §108.195: must detect ADS-B Out and electronic conspicuity (cooperative detection).
- **Cat 5 (metro) and Class B/C airspace**: equipage-agnostic DAA required — must detect ALL aircraft including non-cooperative (no ADS-B). This is the hardest technical bar.
- Anti-collision lighting: ≥3 statute miles visibility at night (§108.830).

Standards pathway: ASTM F38 committee (F3442 referenced), RTCA ACAS sXu MOPS, ASTM F3548-21 (UTM conformance monitoring). Framework is performance-based — no single sensor type mandated.

**Critical gap (fn.71):** ACAS sXu MOPS currently lacks a standardized means of compliance for the drone-side non-cooperative detection sensor. This vacuum is the primary technical bottleneck for Cat 5 urban autonomous BVLOS. See [[detect-and-avoid]] for the standards landscape.

## Autonomy Model (*proposed rule*)

The rule explicitly envisions "mostly to fully autonomous" operations as the regulatory norm, not an exception:

- "Flight coordinator" replaces "pilot" as the responsible party title.
- §108.310(a): if the manufacturer's instructions permit, NO flight coordinator is required — fully unattended autonomous operations are legal under the proposed framework.
- No airman certificate required for flight coordinators.
- Safety responsibility shifts from individual pilot to organization + onboard systems.

This is a structural shift: regulatory accountability moves from a certificated human to an organizational safety case and the autonomy system itself. Airworthiness acceptance for the autonomous platform becomes the practical gating bottleneck.

## Tensions and Open Issues

| Issue | Detail |
|---|---|
| Non-cooperative DAA MOPS vacuum | Standardized non-cooperative sensor compliance path doesn't exist; delays Cat 5 metro autonomy. |
| §91.113 not updated | FAA deferred making detect-and-avoid legally equivalent to see-and-avoid; the legal basis for autonomous avoidance is unresolved. |
| 240-day deadline | Aggressive for a ~731pp NPRM touching 9+ existing Parts; final rule by ≈Feb 2026 is ambitious. |
| Cooperative-only path | The fully standardized DAA path (ADS-B/EC) excludes non-cooperative aircraft; Cat 5 bar requires more. |

For the [[detect-and-avoid]] standards that the NPRM references (ASTM F3442, ACAS sXu), see that page. For the sensor modalities that can satisfy the non-cooperative detection requirement, see [[drone-sensors-for-autonomy]].


## Source
- `raw/research/autonomy-and-sensors/04-faa-part108-nprm.md` — FAA NPRM, 14 CFR Part 108, Docket FAA-2025-1908, Notice 25-07 (~731pp); first proposed US framework for routine commercial BVLOS at scale.

## Related
- [[detect-and-avoid]] — the DAA standards (ASTM F3442, ACAS sXu) this rule references; non-cooperative sensor gap.
- [[drone-autonomy-state]] — where Part 108 fits in the autonomy capability vs. regulation timeline.
- [[anduril-lattice]] — defence-origin multi-asset autonomy and sensor fusion; non-cooperative detection approach relevant to Part 108 DAA requirements.
- [[drone-sensors-for-autonomy]] — sensor modalities relevant to meeting the proposed DAA requirements.
