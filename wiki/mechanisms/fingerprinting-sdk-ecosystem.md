# Fingerprinting SDK Ecosystem

At scale, device fingerprinting on mobile is not a browser phenomenon — it is an SDK supply-chain problem. Specter et al. (2026) analyzed 228,598 SDKs across 9 Maven repositories and 178,054 Android apps from Google Play (Jan 2023–May 2024) and found 723 likely-fingerprinting SDK families embedded throughout the app ecosystem, covering categories far beyond advertising. The paper is the largest-scale empirical mapping of this supply chain to date and provides a concrete taxonomy for blocklist-based counter-power.

## Dataset and Scope

- **SDK corpus:** 228,598 SDKs from 9 Maven repositories
- **App corpus:** 178,054 Android apps from Google Play (Jan 2023 – May 2024)
- **Seed set:** 14 self-admitted fingerprinting SDKs used as ground-truth anchors — Seon, Forter, Accertify/InAuth, Castle, Microsoft Dynamics 365, IP Quality Score, Fingerprint.js, Shield, ThreatMetrix/LexisNexis, Ravelin, TransUnion TruValidate, Socure, Incognia, Kaspersky AntiVirus SDK
- **Extended set:** 723 likely-fingerprinting SDK families (14,178 versions), identified via API-usage similarity to the seed set
- **Signal inventory:** 504 unique exfiltrated signals across the seed set; individual SDKs collect 20–213 signals each

The seed set represents SDKs that publicly admit fingerprinting in their documentation or marketing — the floor of the actual ecosystem, not its ceiling.

## SDK Taxonomy: What's Actually Fingerprinting

The 723-family extended set breaks down by category:

| Category | Count | Share |
|---|---|---|
| Ads | 221 | ~30.6% |
| Tools / Other | 173 | ~23.9% |
| Unclear / Not Found | 167 | ~23.1% |
| Security & Authentication | 85 | ~11.7% |
| Analytics | 77 | ~10.6% |

The Ads category is the only one directly addressed by current regulatory interventions (Apple ATT, Android Privacy Sandbox). It is a minority of the fingerprinting surface.

Security & Authentication (11.7%) is the most under-documented vector. SDKs in this category are typically treated as privacy-neutral by developers, app-store reviewers, and regulators — the assumption being that fraud-prevention signals serve a legitimate interest and don't constitute tracking. The empirical record contradicts this: these SDKs use the same API surface as the ad-tech fingerprinters.

## Core Findings

1. **Ad-focused regulation is structurally insufficient.** Apple ATT and Android Privacy Sandbox target ~30% of fingerprinting behavior. The remaining ~70% — Tools, Security, Analytics, and Unclear categories — is largely unaddressed by current frameworks.

2. **API-level blocklists are brittle.** Only 2% of exfiltrated APIs are used by more than 75% of fingerprinting SDKs. A blocklist targeting the "core" signals misses the long tail; comprehensive coverage requires enumerating and blocking a very wide API surface.

3. **Fingerprinting SDKs correlate with install volume.** Apps containing fingerprinting SDKs have roughly 10x the install volume of apps without them. Whether this reflects selection (high-value apps invest in identity infrastructure) or developer preference (network effects favor SDK incumbents) is unresolved, but the exposure is concentrated in high-traffic apps.

4. **Category-level risk is uneven and high.** Apps in Dating, Games, and Comics have >80% probability of containing at least one fingerprinting SDK. This is not a fringe phenomenon.

5. **The Security & Authentication vector is hidden in plain sight.** Developers integrating fraud-prevention SDKs are not typically aware they are also deploying fingerprinting infrastructure. Informed consent and disclosure requirements do not reach this category effectively.

## Counter-Power Implications: What This Means for Blocking Tools

**App-store enforcement:** The extended-set taxonomy (723 families, 14,178 versions) is concrete enough to anchor app-store-level policy — required disclosure of fingerprinting SDKs at submission time, or outright prohibition of SDKs from specified families. Google Play and the App Store have not used this lever at this resolution.

**OS network-layer filtering:** Android's Private DNS, VPN-layer filtering, or firewall rules targeting known fingerprinting SDK endpoints can block data exfiltration without requiring app changes. The seed set and extended set provide endpoint anchors (SDK-specific telemetry domains) for building such blocklists. Projects like NextDNS and Pi-hole already operate in this space for browser-side fingerprinting; the SDK endpoint list is a natural extension.

**DSAR leverage:** Each of the 504 identified signals is a data point that fingerprinting SDKs collect and presumably transmit. Under GDPR Article 15 / CCPA, these signals are in scope for [[dsar-and-data-deletion]] requests against the SDK vendors themselves (Seon, Forter, etc.) — not only against the apps embedding them. SDK vendors are data controllers or processors depending on jurisdiction; their discoverability via this paper strengthens the legal argument.

**Regulatory framing:** The paper's framing supports arguments that GDPR "legitimate interest" and fraud-prevention exemptions are being used to launder fingerprinting at scale. The Security & Authentication category is the most actionable argument here.

**The developer-awareness gap:** Most app developers embedding Security & Authentication SDKs don't know they're deploying fingerprinting. This opens a supply-side intervention: developer tooling, SDK auditors, or OS-level SDK scanning at build time could raise the cost of unknowing deployment.

## Distinction from Browser Fingerprinting

[[browser-fingerprinting]] operates on browser APIs exposed to JavaScript — Canvas, WebGL, AudioContext, navigator attributes, etc. Defenses like [[privacy-badger]], uBlock Origin, and Brave's fingerprinting randomization operate at this layer. They offer **zero protection** against SDK-based fingerprinting in native Android or iOS apps.

Key distinctions:

- **Surface:** SDK fingerprinting accesses Android system APIs (TelephonyManager, Build, Settings.Secure, SensorManager, etc.) with permissions granted at install time — not browser APIs gated by same-origin policy.
- **Consent model:** Browser fingerprinting occurs in a context where the user has a browser; SDK fingerprinting occurs silently inside apps the user installed for an unrelated purpose.
- **Defense layer:** Browser defenses (extension-based, proxy-based) don't reach native app code. Effective defenses must operate at the OS, network, or app-store layer.
- **Signal count:** The 20–213 signals per SDK in this paper exceed what most browser fingerprinters collect, and include hardware sensor data unavailable in browsers.

The gap between browser-layer activism and native-app-layer exposure is a structural blind spot in current counter-power tooling. Tools and campaigns built around browser fingerprinting are addressing the less severe half of the problem.

## Source

**Specter et al. (2026)** — "Fingerprinting SDKs for Mobile Apps and Where to Find Them: Understanding the Market for Device Fingerprinting." Michael A. Specter (Georgia Tech & Google LLC), Mihai Christodorescu, Robin Lassonde, Fengguo Wei, Dave Kleidermacher, Abbie Farr, Xiaoyang Xu, Saswat Anand, Bo Ma, Xiang Pan (Google LLC). arXiv 2506.22639, cs.CY. Captured June 29, 2026.

**Trust:** Peer-reviewed preprint. Google-affiliated authorship — note institutional framing; the SDK taxonomy is empirically derived from API-usage analysis, but vendor characterizations and policy recommendations may reflect Google's positioning. The raw dataset findings (signal counts, category breakdown, install-volume correlation) treat as credible; editorial framing treat with standard institutional-interest discount.

## Related

- [[mechanisms/browser-fingerprinting]] — browser-layer fingerprinting techniques and defenses; this page is the mobile SDK counterpart
- [[tools/privacy-badger]] — browser-only defense; ineffective against native-app SDK fingerprinting
- [[strategies/possible-strategic-levers]] — blocklist and tracking-defense levers where SDK taxonomy feeds directly
- [[mechanisms/dsar-and-data-deletion]] — SDK vendors are DSAR targets; 504 identified signals are in-scope data
- [[mechanisms/obfuscation]] — SDK-aware obfuscation as an emerging counter to device identity persistence
