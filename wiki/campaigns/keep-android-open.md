# Keep Android Open

keepandroidopen.org is a civil-society campaign opposing Google's mandatory Android Developer Verification program, which takes effect September 2026 and requires every Android app developer — including those distributing outside the Play Store — to register with Google, pay a fee, surrender government-issued ID, and provide evidence of their signing keys. The campaign has collected over 100,000 petition signatures and an open letter from 71 organizations across 23 countries; it is coordinated primarily by FOSS and digital-rights groups including F-Droid, EFF, Nextcloud, GrapheneOS Foundation, and the Free Software Foundation.

## What the mandate does

Announced August 2025 ([Google developer-verification page](https://developer.android.com/developer-verification)), the mandate requires every Android app developer to:

- Register centrally with Google via the Android Developer Console
- Pay a fee to Google
- Agree to Google's Terms and Conditions
- Submit government-issued identification
- Provide evidence of their private signing key
- List all current and future application identifiers

Apps whose developers have not complied are silently blocked on every certified Android device worldwide. The mandate covers all apps — Play Store, F-Droid, direct APK distribution, internal enterprise apps, personal tools — with no geographic carve-out and no opt-out for users.

**Enforcement date: September 2026.**

## The sideloading "escape hatch"

Google describes a "power user" path to install unverified apps via Developer Mode. As documented by the campaign, this flow requires nine steps, a mandatory 24-hour cooling-off period, and multiple dismissals of scare screens. Critically, this flow runs entirely through **Google Play Services**, not the Android OS layer — meaning Google can tighten or remove it via a Play Services update, without an OS update, without user consent, and with no beta or canary build having shipped as of the campaign's capture date (2026-07-06).

## Security argument rebuttal

The campaign, EFF, and F-Droid argue that registering *developers* rather than scanning *code* is a censorship mechanism, not a security one. Google Play Protect already scans for malware independent of developer identity. Malware authors can register; dissidents, pseudonymous contributors, and developers in sanctioned countries often cannot. The EFF characterizes identity-based gatekeeping as "an ever-expanding pathway to internet censorship." F-Droid notes that Google's own Play Store has repeatedly hosted malware, undermining the security rationale.

## Coalition

71 organizations from 23 countries signed the open letter as of capture. Key signatories relevant to cooperative and FOSS app distribution:

| Organization | Relevance |
|---|---|
| F-Droid | Primary FOSS Android app store; calls mandate "existential" |
| Electronic Frontier Foundation (EFF) | Primary digital-rights voice; provides regulatory framing |
| Free Software Foundation (FSF) / FSFE | Open-source software freedom framing |
| GrapheneOS Foundation | Privacy-hardened Android fork |
| LineageOS | Community Android fork |
| Aurora Store | F-Droid-compatible alternative Play Store front-end |
| Nextcloud | FOSS cloud/app distribution |
| KDE e.V. | FOSS desktop/mobile development |
| Proton AG | Privacy-focused app developer |
| The Guardian Project | Security/privacy tools for activists |
| The Tor Project | Censorship-circumvention tools |
| Brave | Privacy browser with explicit statement on developer ID risks |
| BEUC (European Consumer Organisation) | Consumer advocacy, EU regulatory angle |
| Software Freedom Conservancy | FOSS legal and infrastructure |
| Chaos Computer Club (CCC) | Hacker/security community |
| microG | Google-services-free Android layer |
| Obtainium / IzzyOnDroid | Alternative app distribution channels |

## Enforcement timeline and regulatory status

- **August 2025:** Google announces mandatory developer verification ([developer-verification page](https://developer.android.com/developer-verification))
- **September 2025:** F-Droid publishes ["existential threat" response](https://f-droid.org/en/2025/09/29/google-developer-registration-decree.html); Cory Doctorow dubs it "Darth Android" in [Pluralistic](https://pluralistic.net/2025/09/01/fulu/)
- **November 2025:** EFF publishes ["Application Gatekeeping: An Ever-Expanding Pathway to Internet Censorship"](https://www.eff.org/deeplinks/2025/11/application-gatekeeping-ever-expanding-pathway-internet-censorship)
- **March 2026:** Google publishes [blog post](https://android-developers.googleblog.com/2026/03/android-developer-verification.html) describing Developer Mode escape hatch; Ars Technica: ["Google's Apple envy threatens to dismantle Android's open legacy"](https://arstechnica.com/gadgets/2026/03/with-developer-verification-googles-apple-envy-threatens-to-dismantle-androids-open-legacy/)
- **March 2026:** MEP Christel Schaldemose formally questions European Parliament on whether the mandate is compatible with the EU Digital Markets Act
- **Aptoide** files fresh lawsuit alleging monopoly and anticompetitive conduct (reported by Benzinga)
- **July 2026 (capture date):** Developer Mode escape hatch has not appeared in any Android 16 or 17 beta, preview, or canary build; campaign notes "the widely-circulated narrative that Google already backed down is false"
- **September 2026:** Enforcement begins

## Implications for cooperative and FOSS app distribution

The mandate structurally requires any app distributed outside the Play Store to either:

1. **Register with Google** — surrendering developer identity to a single corporation with a documented track record of complying with government app-removal demands, and agreeing to irrevocable Terms and Conditions
2. **Become uninstallable** on certified Android devices worldwide

F-Droid's explicit position: "We unequivocally advise against signing up for this program, now or ever." The campaign's developer guidance is to refuse registration and coordinate non-compliance.

For cooperative app distribution and counter-power tooling targeting Android users, this mandate creates a hard fork: distribute through Google's gate (identity surrender, ToS capture) or target users on alternative OS builds (GrapheneOS, LineageOS, /e/, iodé, Calyx) — a substantially smaller addressable market.

The [FreeDroidWarn library](https://github.com/woheller69/FreeDroidWarn) allows app developers to warn users in-app about the mandate.

## Broader structural pattern

The mandate extends Google's gatekeeping authority from its own marketplace to every alternative Android distribution channel — including channels where Google has no legitimate operational role (per the open letter). Cory Doctorow frames it as "malicious compliance with the court orders stemming from [Google's] losses to Epic Games." I-Programmer: "It effectively makes the Play Store a monopoly without actually mandating that it is a monopoly."

This replicates at the OS layer what MV3 did at the browser-extension layer: using platform-control mechanisms to foreclose counter-power tooling without formally banning it.

## Source

Captured from [keepandroidopen.org](https://keepandroidopen.org) on 2026-07-06. Campaign site aggregating the mandate's details, coalition signatories, press coverage, and action items. Source is advocacy material; secondary sources cited within (F-Droid, EFF, Ars Technica, The Register, TechCrunch, MEP Schaldemose) are independently verifiable.

Raw capture: `raw/research/weekly-2026-07-06/02-keep-android-open.md`

## Related

- [[adnauseam]] — Chrome Web Store ban is the browser-layer precedent for platform-gatekeeper enforcement against counter-power tools
- [[regulatory-responses]] — EU DMA angle, ACLU framing, MEP formal question on compatibility with Digital Markets Act
- [[bootstrap-strategy]] — MV3 extension death and Android sideloading enclosure are parallel structural foreclosures; both constrain counter-power tool distribution
- [[platform-cooperatives]] — F-Droid, Aurora Store, GrapheneOS represent cooperative/FOSS distribution models; this mandate is a live stress test of their viability
- [[consumer-price-tools]] — any counter-algorithmic or price-comparison tool targeting Android distribution faces this registration gate
- [[privacy-badger]] — EFF is a primary voice in this campaign; extension/app distribution under platform-gatekeeper pressure is a shared constraint
