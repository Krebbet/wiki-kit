# Privacy Badger

Privacy Badger is an **algorithmic tracker-blocker browser extension** developed by the Electronic Frontier Foundation (EFF). Distinguishing feature: it does not ship with a pre-built blocklist. Instead, it **learns to identify trackers from the user's own browsing behaviour** — classifying a domain as a tracker when it observes the domain tracking the user across multiple websites, then blocking it. The clearest live template in this wiki for a client-side tool that *discovers* the extractive behaviour it blocks rather than matching against a curated list.

## Structure

- **Developer:** EFF.
- **License:** free and open-source.
- **Platforms:** Chrome, Firefox, Edge, Brave, Opera, Firefox for Android.
- **Source:** github.com/EFForg/privacybadger.
- **Distribution:** primary store presence (Chrome Web Store, Firefox Add-ons) — EFF's institutional backing insulates it from the kind of ad-hoc removal that hit [[adnauseam|AdNauseam]].

## Mechanism (per captured Wikipedia source)

- Detects content loaded from third-party domains on each page the user visits.
- **Algorithmically defines "tracking":** observes when a third-party domain loads content across multiple distinct websites *without permission*.
- Blocks or restricts domains identified this way.
- **Global Privacy Control + Do Not Track signals** sent to every site. If the site ignores them, Privacy Badger learns to block it.
- **Cookie blocking, click-to-activate placeholders** for embedded widgets (video players, comments) that would otherwise track silently.
- **Outgoing-link click-tracking removal** on Facebook and Google.
- **Fingerprinting defence:** blocks trackers that identify users via browser-unique characteristics.

## Distinction from ad-blockers

Per the captured Wikipedia article:

> While most other blocking extensions prioritize blocking ads, Privacy Badger doesn't block ads unless they happen to be tracking you.

This matters strategically: Privacy Badger's enforcement surface is *surveillance*, not *advertising*. The distinction decouples it from the ad-vs-publisher debate that [[adnauseam|AdNauseam]] became caught in. An ad that doesn't track is permitted; a tracker that doesn't carry ads is still blocked.

## Relevance for building against dynamic pricing

*(editorial / synthesis — Privacy Badger's target is ad/tracker domains, not pricing-algorithm inputs.)*

Privacy Badger is the architectural template for a **learn-the-pattern-then-block-it** variant of a [[possible-strategic-levers|pricing-algorithm-detection tool]]. Transferable design decisions:

1. **No static blocklist.** The tool learns the extractive pattern from observation rather than relying on a hand-maintained signature list. A pricing-observatory variant could learn "which retailers personalise" per-user, per-category, without needing to pre-enumerate them.
2. **Privacy-preserving signal transmission.** Global Privacy Control + Do Not Track are baked into every request; the extension is simultaneously an observatory and a protest-signal transmitter. A pricing analogue could send a "no personalisation" header with each request, logging whether retailers honour it.
3. **Institutional hosting.** EFF backing. Same structural position as Open Food Network (under a nonprofit foundation) and NOYB (see [[noyb]]) — avoids the platform-ban failure mode that hit AdNauseam.
4. **Free and open-source, standard platform distribution.** Discoverable and installable via normal browser channels. The anti-pattern is not AdNauseam itself (obfuscation-adversarial) — it is an obfuscation tool distributed without institutional cover.

## Scope and limitations

- **Third-party trackers only.** Does not address first-party data collection (the seller's own pricing personalisation is a first-party activity from the browser's perspective).
- **Passive blocking, not active counterfeiting.** Where [[adnauseam|AdNauseam]] corrupts tracker signals with fake clicks, Privacy Badger just withholds signals. Weaker in raising the extractor's cost but stronger in legal tractability and sustainability.
- **Does not reach pricing algorithms directly.** The retailer's own pricing algorithm can still personalise on IP, account, fingerprint, and purchase history. Privacy Badger degrades *cross-site* personalisation inputs, not *on-site* ones.

## Source

- `raw/research/lever-implementations/12-04-wikipedia-privacy-badger.md`
  - **Origin:** Wikipedia article *Privacy Badger*.
  - **Audience:** general public, privacy-tool researchers.
  - **Purpose:** mechanism, platform list, feature catalogue.
  - **Trust:** starting reference. Load-bearing claims on algorithmic detection mechanism and feature set traceable via the footnote trail to EFF's own documentation (primary source) and press coverage.

## Related

- [[obfuscation]]
- [[adnauseam]]
- [[nightshade-glaze]]
- [[transparency-tools]]
- [[possible-strategic-levers]]
