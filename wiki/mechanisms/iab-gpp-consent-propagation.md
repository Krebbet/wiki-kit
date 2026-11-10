# IAB GPP Consent Propagation

Aziz & Wilson (Northeastern; arXiv 2611.02014) crawled 7,896 top sites from California IPs in four rounds (Aug-Nov 2025) and measured whether IAB Global Privacy Platform (GPP) / USP consent strings and Global Privacy Control (GPC) opt-outs are set correctly and reach advertisers. They mostly do not: 82.7% of advertising and analytics (A&A) companies are never sent a USP or GPP string, and opting out by any method (GPC, CMP click-through, injected strings) only slightly reduces ad resource loading, pixels and ad cookies. CCPA opt-out via signal is largely not honored in practice.

## Takeaways

- **Adoption:** GPP on 15.4% of sites vs deprecated USP 17.6%; 11.4% both, 6.2% USP only, 3.4% GPP only.
- **Publisher-side setting under GPC:** only 46.6% of USP-API publishers set the USP string to opt-out; 47.2% of GPP publishers did (15% in Apr 2024 per prior work).
- **Advertiser-side reading:** only ~15% of A&A companies read the GPC/USP/GPP APIs; 82.7% never receive a string.
- **Behavioral effect:** opt-out by any method yields only slight decreases in ad resources, pixels, cookies. The CMP route was the best opt-out method in 2025, better than GPC, but with gaps.
- **Inconsistency:** USP and GPP strings from the same publisher sometimes disagree (84.6% consistent in one appendix check); many publishers pick the US National GPP section. String ambiguity works as a compliance loophole.
- **Structure:** IAB Tech Lab (industry-funded) publishes the specs with no reference implementation. Publishers and CMPs implement (OneTrust 17.8% of publishers, Cookiebot 1.0%, Didomi 0.4%, InMobi 0.2%); the downstream ad ecosystem is free to ignore the strings. The CCPA service-provider exception lets third parties retain data under private contracts the study cannot observe. CCPA thresholds ($25M revenue / 100K consumers / 50% data revenue) limit coverage.
- **Release status:** data and scripts are only *planned* for release (footnote 5); no tool code is available. Treat the methodology as replicable from the paper, not as a ready artifact.
- **Limits:** preprint; cannot see service-provider contracts; California-IP vantage only.

## Design-input for opt-out compliance auditing

- Method is replicable: Puppeteer crawler, CrUX site list, California IPs, request/cookie attribution via the DuckDuckGo Tracker Radar entity map, with CMP interaction, GPC and injected-string arms.
- Verify propagation, do not trust the signal. A continuous collective audit (signal sent vs string set vs downstream behavior change) produces evidence for CPPA / California AG complaints or class actions.
- CMP-level opt-out outperforming GPC implies opt-out tooling (extensions) should also automate CMP interaction, not only emit GPC.
- Three measurable failure points to log separately: publisher fails to set string; string not forwarded to the advertiser; advertiser receives string but behavior is unchanged.
- Tension with the GPC/OOPS framing in [[dsar-and-data-deletion]]: browser-layer signal mandates are only as strong as downstream honoring and verification.

## Source

- `raw/research/weekly-2026-11-09/02-iab-gpp-consent-propagation.md` — "One String to Rule Them All: Measuring Consent Under the IAB Global Privacy Platform", Aziz & Wilson, arXiv 2611.02014.
  - Origin: Northeastern University (Christo Wilson's group), academic preprint.
  - Audience: privacy researchers, regulators (CPPA / CA AG), privacy-tech community.
  - Purpose: empirically audit whether opt-out signals propagate and change advertiser behavior.
  - Trust: high (empirical, limitations acknowledged; preprint, data/scripts not yet released).

## Related

- [[dsar-and-data-deletion]] — parallel California compliance failure (9% broker compliance); this adds signal-based opt-out failure.
- [[transparency-tools]] — crawler audit as a transparency instrument.
- [[privacy-badger]] — GPC-sending tracker blocker; downstream non-honoring limits its effect.
- [[browser-fingerprinting]] — crawl-based measurement and tracker ecosystem context.
- [[google-rtb-control]] — ad-tech privacy setting with an opt-out efficacy question.
- [[barriers-to-evidence]] — private service-provider contracts as an evidence-access asymmetry.
- [[regulatory-responses]] — CCPA enforcement-gap evidence.
- [[health-data-opt-out-dark-patterns]] — opt-outs that look functional but are not.
- [[ftc-kochava-location-ban]] — enforcement-based remedy vs signal-based opt-out.
- [[possible-strategic-levers]] — information-layer and regulatory-proxy levers.
