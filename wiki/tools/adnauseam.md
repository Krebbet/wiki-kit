# AdNauseam

AdNauseam is a **free and open-source browser extension that blocks internet ads while automatically simulating clicks on them**, introducing counterfeit signals into advertising-network tracking pipelines. Created in 2014 by Daniel Howe, [[obfuscation|Helen Nissenbaum]], and Mushon Zer-Aviv. **Banned from the Chrome Web Store in January 2017.** One of the clearest working instances of [[obfuscation|counterfeit-data obfuscation]] in the consumer-counter-power space — and the clearest live case of what happens when a client-side obfuscation tool meets platform-gatekeeper enforcement.

## Structure

- **License:** GPLv3; source at github.com/dhowe/AdNauseam.
- **Platforms:** Firefox, Chromium (dev-mode installation required post-ban). Chrome banned January 2017.
- **Ad-blocking engine:** derived from uBlock.
- **Reach at time of ban:** 60,000 users (Chrome Web Store). First ad-blocking extension designed for desktop computers banned from the Chrome Web Store.

## Mechanism

From the captured Wikipedia source:

- Blocks ads served by web domains that ignore the user's Do Not Track preference.
- **Repeatedly sends click events to the blocked ads.** This introduces incorrect information about the user's preferences into web-tracking systems used for targeted advertising, impeding profiling.
- Forces pay-per-click advertisers to incur financial costs for the fake clicks.
- User configurable: initially clicks all eligible ads; user can adjust the proportion.

## 2021 MIT Technology Review efficacy test

Conducted with Nissenbaum on Google Ads + Google AdSense test accounts. Findings (per the Wikipedia capture):

- Google processed transactions for ads clicked by AdNauseam on browsers operated by human users and on **three of four** browsers automated with the Selenium toolkit.
- Test gained **$100 of income** for the AdSense account.
- MIT Tech Review interpreted this as evidence of AdNauseam's efficacy.

## The 2017 Chrome Web Store ban

Most instructive part of the captured history.

- **January 2017:** Google removed AdNauseam, citing the platform's developer agreement "right to suspend or bar any Product from the Web Store at its sole discretion."
- Google denied to *Fast Company* that the ad-clicking functionality triggered the ban; instead cited simultaneous blocking and concealing of ads — a behaviour Google permitted in other extensions on the platform.
- Users initially bypassed the ban via Chrome's developer mode installation.
- **Google then marked AdNauseam as malware** to prevent the dev-mode workaround.
- Designer Mushon Zer-Aviv had anticipated this would happen and attributed the removal to Google safeguarding advertising as an income source.
- *Fast Company* expected a competing Chrome-integrated ad blocker adhering to Coalition for Better Ads criteria (an industry group Google co-founded) — evaluating visual appeal rather than privacy considerations.

**Relevance:** AdNauseam's ban is the canonical precedent for [[possible-strategic-levers|lever #10 (adversarial training-data injection)]] meeting platform-gatekeeper reality. Any pricing-algorithm obfuscation tool should budget for the same enforcement path. See [[obfuscation]] for the cross-tool design lessons.

## Reception

From the Wikipedia capture:

- **EFF representative Alan Toner:** described AdNauseam as "a piece of agitprop theater" intended to "creatively protest the surveillance mechanism behind advertising."
- **Fox Networks Group ad executive Joe Marchese** (in *MediaPost*): "AdNauseam aims to screw with the ad industry in ways that just using an ad blocker doesn't"; called it "obviously hostile to our industry" but "extremely smart."
- **Anti-adblock consulting firm PageFair CEO Sean Blanchfield:** concern that advertisers can't distinguish AdNauseam from deliberate click fraud; "if it gains popularity with technical users, its only achievement will be to destroy the businesses that run its users' favorite websites."
- **Solve Media CEO Ari Jacoby:** accused AdNauseam of being "designed to defraud for sport."

The industry reception on the whole validates the mechanism's design: ad-network actors experience it as legible disruption of their revenue model, which is precisely what the authors intended.

## Lineage

- **Predecessor:** TrackMeNot (same Howe + Nissenbaum team), browser extension that masks search queries by sending decoy queries. Last updated November 2019.
- **Theoretical anchor:** Nissenbaum's 2015 book *Obfuscation*. See [[obfuscation]] for the cross-tool mechanism framing.

## Scope and limitations

- **ToS / platform-enforcement risk is the binding constraint.** The Chrome ban is durable; workarounds exist (Firefox, Chromium dev-mode) but mainstream distribution is closed. This is the failure-mode template to study for any similar tool.
- **Ad-industry-facing only.** Does not address pricing-algorithm personalisation, credit-scoring, or tenant-screening — which are the extraction mechanisms this wiki primarily targets. It is a reference implementation for obfuscation-as-counter-power, not a price-side tool.
- **Efficacy at scale is uncertain.** The 2021 MIT Tech Review test confirmed per-extension efficacy but not whether 60K users (peak reach) meaningfully degrades Google's ad-network inference at industry scale.

## Source

- `raw/research/lever-implementations/01-01-wikipedia-adnauseam.md`
  - **Origin:** Wikipedia article *AdNauseam*.
  - **Audience:** general public, digital-rights readers.
  - **Purpose:** chronology, functionality, Chrome ban, reception.
  - **Trust:** starting reference with strong footnote trail — Wired (Clive Thompson), The Guardian (Julia Powles), Le Monde, Fast Company (DJ Pangburn), MIT Tech Review (Lee McGuigan), Vice, The Register, Observer.

## Related

- [[obfuscation]]
- [[nightshade-glaze]]
- [[privacy-badger]]
- [[transparency-tools]]
- [[paypal-honey]] — parallel case of a browser extension receiving platform-policy response (Chrome Web Store March 2025 affiliate-commission rule change).
- [[possible-strategic-levers]]
