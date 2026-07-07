# Google RTB Control

A proposed privacy setting arising from a class-action settlement with Google over its real-time bidding (RTB) system. If court-approved, RTB Control would allow users to strip identifying data — pseudonymous IDs, IP addresses, user-agent strings, and cookie-matching linkages — from bid requests sent to thousands of advertisers on each ad impression. The setting is opt-in, covering only signed-in Google users or signed-out users with third-party cookies enabled; EFF criticises the opt-in default as the central structural failure of the settlement.

## Real-Time Bidding: The Mechanism

RTB is the millisecond auction process by which most ad space is sold. Each auction involves broadcasting a "bid request" containing the user's unique advertising ID, GPS coordinates, IP address, device details, inferred interests, demographic data, and the app or site being visited to thousands of potential advertisers simultaneously. Only one advertiser wins the slot, but all participants receive the data regardless. This makes every ad impression a mass data broadcast to thousands of companies, hundreds of times per day per user.

Data brokers exploit this by posing as ad buyers to harvest bidstream data at scale. Documented downstream uses include tracking union organisers and political protesters, outing gay priests via Grindr location data, and warrantless government surveillance — ICE, CBP, and the FBI have purchased location data from brokers whose sources likely include RTB. ICCL research (2023) identified this as a national security risk, noting foreign states could obtain sensitive data on US defence personnel and political leaders through RTB participation.

Google facilitates the majority of RTB auctions, per DOJ post-trial findings in the US v. Google antitrust case.

## The Proposed Settlement

Several class-action lawsuits against Google alleged that sharing users' personal information with thousands of advertisers through RTB auctions occurred without proper notice and consent. A proposed settlement (September 2025, DiCello Levitt) would require Google to:

- Create the "RTB Control" privacy setting.
- When enabled: suppress pseudonymous IDs (including mobile advertising IDs), IP addresses, and user-agent details from bid requests.
- When enabled: prevent cookie-matching, which companies use to link their cross-site data profiles to a bid request.
- Notify all users of the new setting by email.

## Technical Scope and Limitations

RTB Control operates at the bid-request layer — it suppresses the identifiers that enable cross-site profile construction and bidstream data harvesting. This does not reach first-party data collection: a retailer's own pricing algorithm can still personalise on account history, purchase behaviour, and on-site fingerprinting regardless of RTB Control state.

Coverage limitations:

- **Opt-in default.** Research consistently shows most users do not change default settings. EFF's critique: an opt-in default leaves the vast majority of users unprotected. A default-on setting would be the functionally meaningful design.
- **Signed-in or third-party-cookie requirement.** RTB Control only functions for users signed in to a Google account, or for signed-out users whose browsers permit third-party cookies. Users who are signed out *and* have third-party cookies blocked — the privacy-hardened cohort most motivated to use RTB Control — cannot benefit. EFF notes this limitation is avoidable by making RTB Control the universal default.

## EFF's Position

EFF endorses the settlement as a step in the right direction but frames it as insufficient. Their structural critique: the opt-in default means most users remain exposed; the signed-in/cookie requirement excludes the most privacy-aware users. EFF's legislative ask is a ban on online behavioural advertising — eliminating the financial incentive to track in the first place — not just controls on how tracking data is packaged and broadcast.

Interim user-level mitigations EFF recommends pending the settlement and legislative action:

- [[privacy-badger]] — blocks cross-site trackers, same EFF origin.
- Disable mobile advertising ID (iOS and Android — instructions via EFF's Surveillance Self-Defence).
- Monitor for RTB Control availability once the settlement is approved.

## Design Implications for Counter-Power Tooling

*(editorial / synthesis)*

The RTB Control case illustrates the opt-in default failure mode at scale. Any user-side privacy tool that defaults to maximum data exposure achieves near-zero real-world coverage. The design principle: effective counter-power settings must be opt-out, not opt-in — the settlement's own weakness is that it fails this test. This maps directly to the [[possible-strategic-levers|lever inventory]] principle of embedding defaults that protect rather than expose.

The technical gap — RTB Control does not reach first-party personalisation — also defines the remaining attack surface: retailer-side pricing algorithms operating on account history and on-site behaviour are invisible to bid-request-layer controls.

## Source

- `raw/research/weekly-2026-07-06/01-google-rtb-control.md`
  - **Origin:** EFF Deeplinks blog, January 2026.
  - **URL:** https://www.eff.org/deeplinks/2026/01/google-settlement-may-bring-new-privacy-controls-real-time-bidding
  - **Audience:** general public, privacy advocates, policymakers.
  - **Purpose:** explain RTB harms, assess the proposed settlement, advocate for stronger legislation.
  - **Trust:** high — EFF advocacy with citations to settlement documents (DiCello Levitt filing, September 2025), ICCL research, DOJ post-trial findings in US v. Google, and FTC complaint documents. Claims traceable to primary sources.

## Related

- [[privacy-badger]] — EFF's user-side tracker-blocking extension; recommended alongside RTB Control
- [[surveillance-pricing-retail]] — RTB bidstream data feeds the surveillance infrastructure enabling dynamic pricing discrimination
- [[noyb]] — European strategic litigation model; the Google RTB settlement is the US class-action parallel
- [[dsar-and-data-deletion]] — complementary individual data-control mechanism
- [[regulatory-responses]] — RTB settlement fits the consolidated counter-power litigation landscape
- [[algorithmwatch]] — algorithmic accountability research context
