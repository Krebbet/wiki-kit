# AdFection: Ad-Delivered Zero-Click Spyware

AdFection is a Citizen Lab-disclosed campaign (October 2026) in which a front ad company, Discover-Tech, used the behavioral-ad / real-time-bidding (RTB) stack to deliver Candiru/Integrity Labs zero-click spyware to selected journalists (Al Jazeera devices). Ad-tech targeting identifiers decide who is infected; everyone else gets an empty response, which hides the attack. The case turns RTB's data collection and script-execution surface from a privacy harm into a device-compromise vector. Only journalist targeting has been described.

## Attack chain (per EFF's summary of the Citizen Lab report)

1. Victim browses or uses an app; an ad created by Discover-Tech is served.
2. Ad carries a JavaScript snippet that executes automatically on render.
3. Snippet calls back to Discover-Tech's "NOAS server" with cookie-set advertising ID, IP address and other device data.
4. NOAS server fingerprints the requester as a target (e.g. an Al Jazeera machine). Usual response is empty; for targets it returns a zero-click payload built by partner Candiru/Integrity Labs.
5. Payload executes; machine infected. No click required.

Steps 1-3 are routine ad-tech behavior. Novelty is the combination of malvertising, zero-click exploitation and ad-tech targeting: hyper-targeted, hard to defend, hard to detect.

## RTB code-execution surface

- Ads are mostly delivered by intermediaries running RTB auctions, not by the creator.
- Winning bidders can execute JavaScript in the recipient's browser (needed for interactive ads).
- Intermediaries have "extreme latitude" in data collection; tracking identifiers collected for ad delivery can be repurposed by mercenary spyware vendors for target selection.
- Selectivity is the stealth mechanism: only targets receive the payload, so researchers and ordinary users see benign ads.

See [[google-rtb-control]] for the bid-request data-broadcast side of the same mechanism.

## Mitigations (Citizen Lab steps as relayed by EFF)

- Device lockdown and strong security fundamentals (EFF Surveillance Self-Defense, Consumer Reports Security Planner).
- Tracker-blocking extension ([[privacy-badger]]); network-wide ad blocking.
- Disable or reset mobile AD ID (Android, iPhone).
- Privacy-protective browsers.
- Structural ask (EFF's editorial position, not Citizen Lab's): ban online behavioral advertising. EFF concedes individual measures are limited.

No collective, co-op or class-action mechanism is described.

## Implications

- Security rationale for tracker/ad blocking in addition to privacy; relevant to the Hook 5 privacy-suite category in [[consumer-price-tools]]. *(synthesis)*
- AD-ID reset/disable and threat-model tiering are candidate items for a collective-onboarding lockdown checklist. *(synthesis)*
- Tension with click-based obfuscation: [[adnauseam]] (and [[obfuscation]] approaches generally) deliberately load and click ads, which increases exposure to malvertising of exactly this type; they are not safely paired with it. *(synthesis)*
- Consistent with the EFF legislative ask recorded in [[google-rtb-control]]; see also [[regulatory-responses]].
- Follow-up: capture the primary Citizen Lab report; this page rests on a secondary summary.

## Source

- `raw/research/weekly-2026-10-26/04-adfection-lessons.md` — EFF Deeplinks, "Lessons Learned From 'AdFection' and What To Do Next" (2026-10).
  - **Origin:** Electronic Frontier Foundation (advocacy nonprofit), summarizing Citizen Lab research.
  - **Audience:** general public, journalists, at-risk users.
  - **Purpose:** explain the attack chain, give individual defensive steps, advance EFF's call to ban behavioral ads.
  - **Trust:** secondary, advocacy-framed. Technical summary high reliability (relays Citizen Lab); policy conclusions are EFF's editorial position. Primary Citizen Lab report not captured.

## Related

- [[google-rtb-control]]
- [[privacy-badger]]
- [[adnauseam]]
- [[obfuscation]]
- [[consumer-price-tools]]
- [[browser-fingerprinting]]
- [[fingerprinting-sdk-ecosystem]]
- [[regulatory-responses]]
