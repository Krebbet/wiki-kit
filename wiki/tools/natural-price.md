# Natural Price

Natural Price is an open-source browser extension (private beta, single/small developer team, AGPL-3.0) that detects personalised/surveillance pricing at the point of sale: when a user opens a product page, the extension re-fetches the same page in a clean private tab with no cookies or login, and shows the difference next to the price the user was actually shown. A second, opt-in layer pools anonymous reports across users into a crowd-sourced median baseline — intended as a harder-to-block signal once adoption grows. The project is explicit that it is not yet consumer-scale: no hosted service, not listed in any extension store, released builds have the comparison server "compiled out" so nothing leaves the browser by default. It is the first concrete, releasable-code candidate this wiki has captured for the price-personalisation-detection white space identified in [[consumer-price-tools]].

## What Natural Price does

**Threat addressed.** Retailers, airlines, and travel platforms set prices per-user from cookies, login state, device fingerprint, and browsing history — "surveillance pricing" or "personalised pricing." A given shopper has no way to tell whether the price they see is the price everyone sees.

**Mechanism.** Two baselines: (1) a clean-room fetch of the same URL from the same device with no session state, run locally; (2) an opt-in anonymous crowd median from other users who have seen the same product in the same hour, served by a self-hostable crowd API. Demo/default configuration targets IKEA, MediaMarkt.ch, Nike, and Booking.com; extending coverage to a new site requires a one-file "site extractor" contribution, which the project flags as the easiest way to help.

**Status.** Private beta. Zips for Chrome and Firefox are distributed from the GitHub releases page, not through any extension store. The project cites the EU Consumer Rights Directive Art. 6(1)(ea) (in force since May 2022, requiring disclosure of automated-decision-making personalisation) and the anticipated EU Digital Fairness Act (expected late 2026) as the regulatory backdrop for why this kind of tool has standing.

**Licensing as an anti-enclosure clause.** AGPL-3.0 is a deliberate choice: anyone running a modified version as a network service must publish their changes. This is aimed at the failure mode this wiki has documented elsewhere ([[paypal-honey]]) — a transparency tool getting silently forked or enclosed once it has scale.

**Known weakness, self-disclosed.** The README states plainly that "retailers fingerprint and block headless browsers" — the same detection/evasion arms race documented on the surveillance side by [[browser-fingerprinting]], here viewed from the losing side of a counter-tool trying to run an automated clean-room fetch.

**What it is not.** Not a price-shield or obfuscation tool — Manifest V3 does not allow it to rewrite outgoing requests, so it cannot change what price a retailer serves. Not a scraper — one page fetched per user request, respecting site ToS. This distinguishes it from the [[obfuscation]] mechanism cluster (AdNauseam, TrackMeNot, Nightshade) even though it targets an adjacent problem.

## Source

- `raw/research/weekly-2026-09-14/01-natural-price.md` — GitHub README capture, Tumub/natural-price, captured 2026-09-14. Origin: primary-source project documentation, self-published, no institutional affiliation. Trust: primary/self-reported, unreviewed; functional claims (e.g. "10–30% variation") are vendor-asserted or cited to one external academic source (Mikians et al. 2013, arXiv:1307.4531) rather than independently verified here.

## Related

- [[consumer-price-tools]] — Hook 1 (personalisation-detection) competitive landscape; Natural Price is the first captured candidate for the identified white space, still pre-consumer-scale
- [[transparency-tools]] — mechanism anchor; same "make opaque market behaviour visible" category as Mikians et al. 2013's now-defunct crowd-sourced personalised-pricing detector, the direct academic ancestor of this approach
- [[keepa]] — parallel single-purpose, client-side price-transparency browser extension; contrast in maturity and business model (commercial/4M users vs. AGPL/non-commercial/private beta)
- [[markup-citizen-browser]] — parallel crowd-sourced-observation design; Natural Price's crowd API is an early-stage, much smaller-scale analogue
- [[privacy-badger]] — parallel EFF-style zero-data-leaves-the-browser design posture
- [[browser-fingerprinting]] — the detection/evasion arms race Natural Price documents from the counter-tool's losing side
- [[regulatory-responses]] — EU Consumer Rights Directive Art. 6(1)(ea) and Digital Fairness Act as the enforcement backdrop this project cites
