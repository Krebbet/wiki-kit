# Browser Fingerprinting

Browser fingerprinting is the cookieless identification of a user's device/browser by collecting passive and active signals (HTTP headers, Canvas, WebGL, AudioContext, fonts, WebRTC, JavaScript runtime attributes) and hashing them into an identifier that persists across sessions and private-browsing modes. This page anchors the watcher-side technique stack — what fingerprinting actually measures, how unique the resulting identifiers are, and what countermeasures exist — because [[obfuscation]] levers that rotate identity (notably [[possible-strategic-levers|levers #6 and #11]]) must defeat fingerprinting to work.

## Why it matters for consumer counter-power

Every profile-manipulation lever that depends on a user looking different to the pricing algorithm on each visit (fresh session, cycled cookies, new "account") has to defeat fingerprinting. Two sources in the reference layer set the bounds:

- **Lawall 2024** (arXiv 2411.12045) — a survey of current fingerprinting techniques with entropy / uniqueness results. Documents the "blending in" paradox.
- **Venugopalan et al. 2024 — FP-Inconsistent** (arXiv 2406.07647) — a defender-side attack on naive rotation strategies, showing that attribute-by-attribute spoofing introduces detectable cross-attribute inconsistencies.

## Fingerprinting techniques — catalogue (Lawall 2024)

Each entry: what it measures, how it works, stated uniqueness or stability. Quotes are direct extractions.

### Passive (no JavaScript required)

- **HTTP Header Attributes** — User-Agent, Accept, Content-Encoding, Content-Language. "The User-Agent, despite lacking standardization, offers high uniqueness due to its detailed browser and OS information" (§III).
- **CSS Fingerprinting** — @media queries and URL parameters infer screen dimensions, resolution, touchscreen presence, installed fonts, browser, OS from server-side URL analysis. Works without JavaScript. "CSS fingerprinting's independence from JavaScript allows it to identify even cautious users who block JavaScript" (§III).

### Active (JavaScript API-exposed entropy sources)

- **Canvas Fingerprinting** — Invisible Canvas element draws a 2D graphic; variations in hardware acceleration, installed fonts, and graphic libraries produce a unique hash. "Implementing Canvas fingerprinting is straightforward, requiring minimal lines of client-side code" (§III).
- **WebGL Fingerprinting** — 3D rendering + GPU parameter queries via UNMASKED_VENDOR_WEBGL / UNMASKED_RENDERER_WEBGL. "Unlike Canvas fingerprinting, which focuses on 2D graphics and identifies software differences mainly through fonts and graphic libraries, WebGL fingerprinting provides deeper and more precise detection capabilities" (§III).
- **Audio Fingerprinting** — Web Audio API (AudioContext, Oscillator, Compressor) generates a waveform whose hash reflects hardware. Dynamic Compressor (DC) method is "highly stable"; FFT method "requires multiple attempts." "Audio fingerprinting offers high stability, it lacks uniqueness and accuracy on its own and should be used with other fingerprinting techniques" (§III).
- **Font Fingerprinting** — JavaScript compares text dimensions against expected values via invisible div + canvas elements. Identifies OS and installed software (Office, Photoshop). "Font recognition offers high entropy and stability since fonts are rarely changed" (§III).
- **Screen Fingerprinting** — window.screen.{colorDepth, height, width, innerWidth, innerHeight}. "Screen and window resolution information typically have high entropy" (§III).
- **WebRTC Fingerprinting** — STUN-based peer connections extract private/public IPs and media device IDs without user permission. "No other technique can silently reveal addresses behind Network Address Translation (NAT)" (§III).
- **Browser Plugin / Extension Enumeration** — Chromium-based browsers expose extension settings via local URLs; a GitHub project checks over 1,000 extensions by requesting internal resources. Ad-blocker behaviour detected by creating elements they block and checking for removal. "User-installed extensions offer high uniqueness and stability due to the number of extensions" (§III).
- **navigator object attributes** — DoNotTrack, platform, languages, cookie usage, timezone. Plus getClientRects for precise DOM element data (patched in Tor, still exploitable elsewhere).

### ML / side-channel

Lawall 2024, §III: "Use cache usage, memory consumption, and CPU activity to infer visited websites; machine learning models categorize the results with expected values from known sites. Tests showed 80-90% accuracy in identifying websites." And the author-stated countermeasure gap: "Currently, there are no methods to protect users from such techniques."

## Entropy / uniqueness — quantitative signals

Direct quotes from Lawall 2024:

- "Eckersley's study showed that participant browsers already had high entropy, indicating many unique characteristics sufficient for accurate fingerprinting."
- WebRTC: "A study with 80 devices found over 97% uniqueness using only WebRTC."
- WebGPU (successor to WebGL): "Allowing for classifications with up to 98% accuracy in 150 milliseconds, a reduction from the 8 seconds WebGL took."
- Deployment at scale: "A 2021 study of the Alexa Top 100,000 websites found that nearly 10% of the sites used scripts to generate fingerprints" — vs "5.5% of the top 100,000 sites using canvas fingerprinting scripts" in 2014. Almost doubling over seven years.
- Post-GDPR: "Fingerprinting scripts increased to 68.8% of the top 10,000 sites."

## Countermeasures — what defends, and at what cost

### Browser-level

- **Tor Browser** — "Fixed size of 1000x1000 pixels, reducing uniqueness" (uniformity approach, not randomization). Patched the getClientRects vulnerability.
- **Firefox** — "Always reports a color depth of 24"; groups GPU models into categories rather than exposing specific model names.
- **Apple WebKit / Safari** — "Since 2020, WebKit has masked Vendor and Renderer information, as well as shading language details." Recommended on iOS "due to its advanced tracking protection and large user base."
- **Brave, Librewolf, Mullvad** — Recommended desktop options; protections "often already built into recommended browsers like Brave and Librewolf."

### Extension-level

- **CanvasBlocker** — "Continuously generating new fingerprints to prevent identification"; also blocks and manipulates WebGL and Web Audio API.
- **User-Agent Switcher** — Reduces User-Agent reliability.
- **NoScript** — Blocks JavaScript-based tracking.

Author warning: "Limit the use of browser extensions, as they can become sources of unique information" (Lawall 2024).

### The "blending in" paradox

The central trap with privacy-resistant stacks:

> "Reducing APIs and data sources for fingerprinting can ironically make users more identifiable. Thus, widely adopted browsers and protection mechanisms should be used to stay less conspicuous" (Lawall 2024, citing Al-Fannah & Mitchell 2020).

A heavily-customised privacy-resistant setup becomes uniquely identifiable *as* a privacy-resistant setup — which is itself an identifier. The defender gets a cleaner signal, not a worse one.

### Noise-injection effectiveness — limits documented

Lawall 2024 treats extension-level noise (CanvasBlocker, etc.) as a viable mitigation but does not report empirical effectiveness numbers beyond noting that "limited interfaces to retrieve generated Canvas data can be monitored and manipulated by extensions." The effectiveness question is answered more sharply by FP-Inconsistent below.

## FP-Inconsistent: why naive rotation fails

Venugopalan, Munir, King & Ahmed 2024 (arXiv 2406.07647) is the cleanest empirical demonstration that naive per-attribute rotation produces detectable cross-attribute inconsistencies. Source context: this paper is on the **defender side** — "evasion" in the title is evasion of detection by bots; the paper's goal is to close that evasion gap. Still, the mechanism it documents generalises to any per-attribute rotation strategy a consumer tool might deploy.

### Core claim

> "Real devices can only have a limited number of hardware and software configurations that are reflected in fingerprint attributes. Evasive bots, in their attempt to evade detection, emulate a large number of invalid or extraneous configurations" (§1).

And the memorable summary from the Conclusion:

> "It is challenging to tell a complex lie while keeping the story always straight… a browser fingerprint is a high dimensional feature set with numerous — often subtle — correlations between attributes that are difficult to anticipate and account for when altering fingerprints."

### Dataset and method

- 507,080 requests from 20 purchased bot services (SEOClerks, "blackhat marketplace"), Sept–Nov 2023.
- Honey site with per-service URL paths so every request was attributable to a specific bot service.
- Anti-bot detectors deployed: DataDome and BotD (built by the FingerprintJS developers).
- Fingerprint attributes measured via FingerprintJS (over 30 attributes including navigator.plugins, navigator.userAgent, hardwareConcurrency, deviceMemory, screenResolution, platform, timezone, touch support, canvas, audio).
- FP-Inconsistent detection: data-driven, semi-automated rule generation from **spatial inconsistencies** (two attributes within one request that can't co-exist on a real device) and **temporal inconsistencies** (an attribute changing across requests bearing the same browser Cookie).

### Key quantitative findings

- Baseline detection: "DataDome and BotD detecting 55.44% and 47.07% of these requests respectively" (§1).
- With FP-Inconsistent on top: "Our approach can reduce the evasion rate of evasive bots by 44.95%–48.11% while maintaining a true negative rate of 96.84% on traffic from real users" (§5). Combined: DataDome 76.88%, BotD 70.86% (Table 4).
- iPhone screen-resolution inconsistency: "9 out of the top 10 screen resolutions that have the highest probability of evading DataDome among requests claiming to use iPhones do not exist in the real world." Bot dataset had "83 unique screen resolutions from iPhones" against a real-world maximum of 12.
- Plugin presence for BotD: "The presence of any PDF plugin nearly guarantees evasion against BotD"; conversely "100% of requests detected by BotD did not support any plugins" — BotD was keying on plugin absence.
- CPU cores for DataDome: "84.7% of requests from bot services with a high evasion rate against DataDome had fewer than 8 cores. In contrast, only 19.05% of requests from bot services with a low evasion rate against DataDome have fewer than 8 cores."
- Geolocation mismatch: bot service advertising European traffic had "only 56% of requests mapped to UTC offsets in Europe" by browser timezone API vs "99.83% of requests to originate from Europe" by IP inference.
- Temporal inconsistency: a single Cookie value showed "a wide distribution for the navigator's platform property" — an attribute that "can never change for that device unless the entity controlling the device has intentionally altered the attribute."
- False positives on real users: true-negative rate 96.84% on 2,206 university student requests. "The small number of false positives were likely due to students experimenting with User-Agent spoofers."

### Why bots introduce inconsistencies — mechanisms

Three structural causes identified by the authors:

1. **Incomplete API patching.** "Evasive bots could alter browser APIs and device properties to present their desired values for fingerprint attributes… [but] it is difficult for them to ensure that all fingerprint attributes remain consistent with their alterations." Patch `navigator.userAgent` to claim iPhone without constraining `screenResolution` to iPhone-valid values.
2. **Proliferating fake configurations.** "These alterations typically do not account for every possible source of device information (such as JavaScript APIs, User-Agent, etc.), leading to a proliferation of device configurations." Single device types appear with implausibly many hardware variants in the aggregate dataset.
3. **Temporal attribute mutation.** "They have a fixed set of devices but alter fingerprint attributes to create the illusion of sending requests from a large number of devices" — producing temporal inconsistency when immutable hardware properties vary across requests sharing one Cookie.

### Implications for well-designed obfuscators

The authors are explicit that a well-designed tool *could* defeat FP-Inconsistent — but they argue it is practically hard:

> "Evasive bots will be able to overcome FP-Inconsistent if they evolve to ensure that they can alter fingerprint attributes without introducing any inconsistencies" (§7).

> "It remains to be seen whether bots can alter their fingerprint attributes while avoiding inconsistency. We believe that it would be challenging for bots to do so because a browser fingerprint is a high dimensional feature set with numerous — often subtle — correlations between attributes that are difficult to anticipate and account for when altering fingerprints" (Conclusion).

**Partial counterexample the authors report: Brave browser.** Brave's built-in fingerprint protection alters only 6 attributes and "Brave's alterations to the others were consistent with other fingerprint attributes." For example, "Brave alters deviceMemory on desktops to plausible values (0.5, 1, 2, 4, and 8), which align with the amount of memory in typical desktops." Brave did trigger some temporal inconsistencies when randomization combined with Cookie persistence, but the authors note "bot services cannot exploit Brave for evasion since they seek to alter attributes that are not supported by Brave."

The practical lesson: per-attribute rotation is insufficient. An obfuscation tool must model the *joint distribution* of real device configurations and ensure every spoofed attribute remains consistent with every other spoofed attribute, temporally and spatially. This is a materially harder engineering problem than the typical extension-level approach.

## PETS 2026 defence cluster

PETS 2026 (Calgary; April 2026) accepted-papers list landed a coordinated wave of fingerprint-defence research, with three papers carrying full **Available / Functional / Reproduced** artifact badges — the strongest reproducibility rating in the venue. Captured `weekly-2026-04-27/05-05-pets-2026-fingerprint-defenses.md`.

### Layer-scoping note (Venugopalan 2024 vs. PETS 2026 defence papers)

The FP-Inconsistent paper above (browser-attribute, JS-API layer) and the PETS 2026 defences (network-layer + application-stream layer) are **not in conflict** — they operate on different abstraction layers. FP-Inconsistent's "naive rotation defeated" finding applies to per-attribute spoofing of browser-exposed properties (`navigator.platform`, `screenResolution`, etc.). The PETS 2026 papers below operate on (a) network-traffic timing/sizing (Ephemeral, Dodge) and (b) voice/audio side-channels (PriVA-C). Different attack-surface, different defence-surface.

### Defence papers with full Reproduced artifacts

- ***Ephemeral Network-Layer Fingerprinting Defenses*** — Pulls, Korhonen, Witwer & Carlsson (Karlstad / Linköping). Network-layer ephemeral-rotation defences. Artifact: Available, Functional, Reproduced. Repository: `github.com/maybenot-io/popets-2026.1-ephemeral-defs-paper-artifacts` (maybenot framework family). The first PETS 2026 paper to demonstrate working defence against website-fingerprinting attacks at the network layer with a fully reproduced artifact.
- ***Dodge: A Client-Side Framework for Application-Layer Video Fingerprinting Defenses*** — Witwer, Hasselquist, Pulls & Carlsson (Linköping / Sectra / Karlstad). Client-side framework for defeating video-stream traffic fingerprinting. Artifact: Available, Functional, Reproduced. Same lab group as Ephemeral — a coordinated research programme on ephemeral-rotation defences across network and application-stream layers.
- ***PriVA-C: Defending Voice Assistants from Fingerprinting Attacks*** — Ahmed, Sabir, Zafar & Das (NC State). Voice-assistant fingerprinting defence. Artifact: Available.

### Supporting empirical and theoretical papers (PETS 2026)

- ***Analyzing Societal Awareness and Perception of Digital Fingerprinting and Fingerprinting Countermeasures*** — Schramm, Syrmoudis, Markou & Grossklags (TU Munich). Empirical baseline on public knowledge of fingerprinting and defences. Artifact: Available, Functional. Quantifies the awareness gap any consumer-side deployment effort must close.
- ***An Improved Entropy Measure for Web Browser Fingerprinting Risk*** — Berke, Bacis & Syed (Google). New entropy-quantification method for browser-fingerprint risk. Note that the lead authors are at the dominant fingerprinting party — a signal that defence-side tooling must continue to track risk-quantification refinements from the watcher side.
- ***EXADPrinter: Semi-Exhaustive Permissionless Device Fingerprinting Within the Android Ecosystem*** — Bouhenniche, Laperdrix & Rudametkin (Lille / Rennes / CNRS-Inria). Expands the attack surface on Android.
- ***Redefining Website Fingerprinting Attacks with Multi-Agent LLMs*** — Song et al. (Rutgers). Attack-side; cross-cuts to [[adversarial-data-poisoning]]'s attack-vs-defence framing.

### Adjacent platform-enforcement signal (PETS 2026)

- ***On the Effectiveness of Manifest V3 Ad-Blockers*** — Lukic & Papadopoulos (Goethe). Documents how Google's Manifest V3 update in Chrome degrades the effectiveness of third-party ad-blocker extensions. Directly relevant to [[obfuscation|obfuscation's countermeasure-projection layer]]: platform-vendor capture is a real risk to extension-level obfuscation. Strengthens the case for *network-layer* defences (Ephemeral above) over *extension-layer* defences for durability against platform changes.

### Implications for consumer counter-power

*(editorial.)*

- **Tier-2 obfuscation extension on [[strategies/data-disruption-strategy-map|the strategy map]] (joint-distribution fingerprint-spoof) now has two reproduced-artifact substrates** at the network and application-stream layers — Ephemeral and Dodge. The remaining gap is browser-attribute layer (where FP-Inconsistent above documents the difficulty); the PETS 2026 cluster does not close that gap.
- **The maybenot framework (Ephemeral's repository) is a forkable starting point** for any consumer-side network-layer rotation tooling. A working substrate for the Tier-2 fingerprint-spoof lever; previously, the wiki had only theoretical anchors for that lever.
- **Schramm et al.'s societal-awareness baseline is design input** for any deployment plan: the tooling exists, but quantified public awareness is the gating constraint on adoption — frames the problem as outreach + onboarding, not just engineering.

### Watchlist-relevant adjacent papers

PETS 2026 also accepted three counter-tracking / compliance-audit papers that don't fit the fingerprint-defence cluster but are tracked on [[transparency-tools]] and the watchlist:

- *Exercising the CCPA Opt-out Right on Android: Legally Mandated but Practically Challenging* (Zimmeck et al., Wesleyan / Maastricht) — only 48 of 100 top-free Android apps implement CCPA opt-out; GPC signals largely ineffective at the OS level.
- *A Year Under the DSA: Ad Transparency's Uneven Landscape* (Benzaamia, El fraihi, Abdelaziz, Goga; LIX / CNRS / Inria / École Polytechnique) — first systematic empirical audit of EU DSA ad-transparency regime one year on; large platforms comply unevenly.
- *Ad Personalization and Transparency in Mobile Ecosystems: A Comparative Analysis of Google's and Apple's EU App Stores* (Breuer, Becker, Hollick; TU Darmstadt) — duopoly-app-store comparison of EU-mandated ad-transparency exposure.

These extend the [[transparency-tools]] empirical landscape but do not introduce new defence mechanisms.

## Case: *Phillips v. JetBlue Airways Corporation* — cookie / cache-based price personalisation alleged on commercial aviation

*Phillips v. JetBlue Airways Corporation* (1:26-cv-02405, US District Court, filed April 22 2026; ClassAction.org coverage published April 29 2026) is the first US federal class-action complaint to allege **browser-tracking-based price personalisation** as the underlying mechanism of consumer-facing dynamic pricing — and the first to do so on commercial aviation specifically. Captured `weekly-2026-05-11/03-jetblue-class-action.md`. The case is wiki-relevant here because the *alleged mechanism* is precisely the cookie / cache / fingerprint stack this page catalogues.

### Alleged mechanism (per the complaint)

- **Cookie / cache tracking** that follows users across sessions on JetBlue.com and the mobile app.
- **Third-party data sharing** with **PROS Holdings, Inc.** (algorithmic pricing vendor; PROS is also one of the recipients of the FTC's July 2024 6(b) surveillance-pricing orders — see [[surveillance-pricing-retail]]) and **FullStory, Inc.** (session-replay / behavioural-analytics vendor).
- The alleged effect: returning users see *higher* fares than fresh-session users for the same itinerary at the same moment — i.e. **per-user price differentiation based on identifiability**.

### The "clear your cache" tweet as platform-side admission

The complaint's load-bearing factual anchor is JetBlue's own, since-deleted, social-media reply to a $230 fare-increase complaint: *"try clearing your cache and cookies or booking with an incognito window."* Per the complaint: *"effectively admitted in a since-deleted social media post in April 2026 that it uses so-called dynamic surveillance pricing."* JetBlue's later official statement denies surveillance pricing; the complaint cites the tweet, *"other public statements,"* and *"the website's back-end code"* as evidence to the contrary.

This pattern — *platform's own customer-service advice to clear cookies/cache as a workaround to high prices* — is a watcher-side **self-disclosure signal** for cookie-based price personalisation that any audit-tool detector can be tuned to surface. The legal theory makes the tweet itself the evidence; the technical question of *which* cookies / fingerprint attributes carry the discriminating signal is left for discovery (no algorithm-level disclosure yet).

### Why this case matters for fingerprinting defences

- **The "clear cookies / use incognito" advice does not defeat fingerprinting** — only cookies. Incognito mode leaves Canvas, WebGL, AudioContext, font, screen, WebRTC and the rest of the active fingerprint stack intact. If JetBlue's pricing keys on a fuller fingerprint, the customer-recommended workaround is partial at best and may not produce the price reduction the customer expects. The complaint does not engage this technical nuance — it treats *"clear your cache and cookies or booking with an incognito window"* as a *de facto* admission of cookie-based tracking but does not allege fingerprinting specifically.
- **Discovery in the case may surface algorithm-level disclosure** of what JetBlue's vendors actually key on, which would be the first US litigation-driven disclosure of an airline-RM-or-surveillance-pricing-vendor feature set. If the vendor stack (PROS + FullStory) includes any of the fingerprinting techniques catalogued above, the case becomes the first US judicial finding on browser-fingerprinting-as-pricing-input.
- **The privacy-tort framing**: the complaint anchors on undisclosed data-collection rather than market harm. This is doctrinally distinct from the antitrust and consumer-protection paths that have dominated US dynamic-pricing litigation and is closer to the GDPR-style theory that [[noyb]] runs in the EU. If certified, it establishes a **US standing template** for cookie/fingerprint-based price-discrimination privacy claims — class-action plaintiff need only show undisclosed collection, not quantified overcharge.

Cross-link to [[consumer-facing-dynamic-pricing|the JetBlue surveillance-pricing inflection-event section]] for the procedural/regulatory layer and to [[pricing-algorithm-taxonomy|Family 4 contested-claim note]] for what the case means for the "airline RM uses no individual identity features" question.

### Tooling implications

*(editorial.)*

- **The "did this site price-discriminate against me?" audit tool** — paired-session detector (fingerprinted-state vs. clean-state, same itinerary, same moment) — would produce the evidence record the *Phillips v. JetBlue* class-recruitment effort needs. The detector's technical job is exactly the inverse of FP-Inconsistent: rather than identifying inconsistent fingerprints, it deliberately *constructs* two consistent-but-different fingerprints and compares the prices each is shown. The "blending in" paradox cuts both ways here — the clean-session fingerprint must be plausibly common for the price comparison to be valid evidence of *targeted* pricing rather than random variation.
- **The PETS 2026 ephemeral-rotation defences above** (Ephemeral, Dodge) would, if deployed widely, reduce the per-user identifiability that surveillance-pricing keys on — converting the *Phillips* class theory from a litigated-redress lever into a pre-emptive technical defence. Per the layer-scoping note above: Ephemeral and Dodge operate on network and application-stream layers, not browser-attribute layer, so they would defeat *some* but not all surveillance-pricing fingerprinting paths.

## Regulatory context — Lawall 2024

> "Despite stricter privacy laws like the GDPR in the EU, browser fingerprinting remains a grey area. Anti-fingerprinting techniques are limited and continually evolving to keep up with new tracking methods."

> "Cookie banners give a false sense of security while tracking continues in the background without consent."

Germany's TTDSG (Telekommunikation-Telemedien-Datenschutzgesetz) is the most recent regulatory instrument Lawall discusses; the survey notes fingerprinting occupies a "grey area" where consent mechanisms for cookies are in force but no equivalent mechanism exists for fingerprinting signals.

## Relevance for consumer counter-power

*(editorial / synthesis.)*

- **Lever #6 (session-identity rotation-as-a-service)** is directly attacked by FP-Inconsistent's cross-attribute inconsistency detection. Any builder must deploy joint-distribution-preserving spoofing, not per-attribute spoofing.
- **Lever #11 (fingerprint parity network)** is conceptually aligned with Tor's uniformity approach — the parity network would make every member present the same apparent fingerprint, dodging inconsistency detection by collapsing entropy rather than randomizing it. The practical question is whether the network can be large enough that the parity fingerprint is itself blendable with organic traffic.
- **The "blending in" paradox constrains tool design.** A tool that makes users *more unique* (heavy customisation) may worsen their identifiability. Uniformity strategies outperform randomization strategies for this reason.

## Source

- `raw/research/obfuscation-deep-dive/04-09-fingerprinting-tracing-shadows.md` — Lawall, *Fingerprinting and Tracing Shadows: The Development and Impact of Browser Fingerprinting on Digital Privacy*, arXiv 2411.12045. Origin: academic survey. Purpose: catalogue fingerprinting techniques and legal context. Trust: high.
- `raw/research/obfuscation-deep-dive/05-10-fp-inconsistent.md` — Venugopalan, Munir, King & Ahmed, *FP-Inconsistent: Measurement and Analysis of Fingerprint Inconsistencies in Evasive Bot Traffic*, arXiv 2406.07647. Origin: academic, defender-side measurement. Purpose: demonstrate cross-attribute inconsistency as detection signal. Trust: high — novel dataset of purchased bot traffic, cross-validation disclosed.
- `raw/research/weekly-2026-04-27/05-05-pets-2026-fingerprint-defenses.md` — PETS 2026 (PoPETs / Calgary) accepted-papers list, captured April 2026 for the fingerprint-defence cluster (Ephemeral, Dodge, PriVA-C, Schramm et al. awareness baseline, Berke et al. entropy measure, EXADPrinter Android, Song et al. multi-agent LLM attack, MV3 ad-blocker effectiveness paper). Origin: peer-reviewed venue proceedings. Purpose: defence-side research disclosure. Trust: high — peer-reviewed; artifact badges (Available / Functional / Reproduced) independently assigned by the PETS artifact committee.
- `raw/research/weekly-2026-05-11/03-jetblue-class-action.md` — ClassAction.org coverage (April 29 2026) of *Phillips v. JetBlue Airways Corporation* (1:26-cv-02405, US District Court, filed April 22 2026). Origin: plaintiff-aligned secondary reporting on a court-filed complaint. Purpose: report case caption, class scope, named third-party vendors (PROS Holdings, FullStory), and the complaint's "clear your cache" admission anchor. Trust: case-caption / docket / vendor-naming claims are checkable against the public docket; allegations are unproven pending discovery and class certification. Used here only for the *alleged-mechanism* layer of the case (cookie / cache-based pricing); not relied on for empirical claims about fingerprinting techniques.

## Related

- [[obfuscation]]
- [[adversarial-data-poisoning]]
- [[privacy-badger]]
- [[transparency-tools]]
- [[possible-strategic-levers]]
- [[obfuscation-strategic-readout]]
