# Agentic Crawler vs Human Tracker Measurement (Sakib et al. 2026)

Sakib et al. (arXiv 2611.06197) compare LLM-driven (agentic) and non-agentic crawlers against 26 human participants across 2,000 sites. Agents record 1.5-1.7x more third-party tracker organizations than non-agentic crawlers, driven largely by auto-accepting consent banners, and recover 82-87% of the tracker orgs humans met (vs 58-68% for non-agentic). Only 48-49% of what agents record also appears in human visits. Crawlers are therefore not neutral observers, and bot-management interventions diverge from landing-page behaviour on later pages. The paper doubles as an agent-behaviour finding: agents told to dismiss obstructing overlays accepted consent 201 times vs 1 reject.

## Key findings

- **Agent consent behaviour.** 273 consent-related clicks over 140 sites: 201 accept, 1 reject. Confirmed consent clicks were followed by a mean 9.2 new third-party script domains within 10 s vs 1.0 for ordinary clicks (69 sites, p<0.001).
- **Concentration.** Consent-managed pages were 28% of matched pages but 62-65% of the extra tracker orgs (agents 1.80-2.16x vs 1.29-1.42x on other pages). Consent management platforms (TCF, Usercentrics, CookieYes, etc.) gate script loading.
- **Human alignment.** Agents recover 82-87% of participant-seen tracker orgs; non-agentic crawlers 58-68%. Only 48-49% of agent observations appear in participant visits.
- **Site interventions.** Landing-page denial rates are similar across crawlers (5.3-8.1%) but diverge on later pages (unpatched Chromium 0.2% -> 10.4%). The Patchright stealth driver cuts the later-page escalation from +10.1pp to +1.2pp without raising recorded tracking. Fingerprint spoofing and simulated mouse movement did not help.
- **Prior work cited.** Automated crawl missed fingerprinting on 45% of sites where humans met it (Annamalai et al.); "Invisible Consent" (CHI 2026, Saito et al.) finds LLM agents not privacy-aware about cookie banners.
- **Selection recipe.** Table 4 maps crawler choice to measurement objective (interaction-triggered tracking, typical human exposure, multi-page access, fingerprinting). Capture is PDF via pymupdf, so some tables are garbled.

## Takeaways

- **Audit validity.** Any measure-then-pressure audit built on crawlers (tracker counts, personalised-price probes, persona/sock-puppet studies) inherits the validity gap: sites may serve crawlers different content and tracking than humans, and the direction of bias depends on crawler type (agents over-count via consent, non-agentic under-count). Pressure campaigns citing crawler-derived numbers are exposed to a "not what users see" rebuttal unless validated against a human baseline.
- **Validation practice.** Matched URLs, normalised requests, repeated reference crawls, and a human-participant reference panel (cf. [[markup-citizen-browser]], [[gesis-surf-data-donation]]) are the controls the paper uses. Report per-vector, not aggregate, counts (cf. [[browser-fingerprinting]]).
- **Multi-page access.** Landing-page-only audits understate bot-management differentiation; later pages diverge. Stealth drivers (Patchright) are viable for multi-page auditing, but this reduces rather than removes the risk that sites treat agent traffic differently, which bears on crawler-based price-transparency tools ([[surveillance-pricing-retail]], [[fairness-testing-algorithmic-pricing]]).
- **Agent privacy default.** Delegated agents with generic "dismiss overlays" instructions raise the user's tracker exposure; the authors recommend consent handling be an explicit, user-controllable policy (e.g. fixed reject-by-default) rather than an incidental effect of obstacle clearing. Empirical counterpoint to framings of agents as privacy-protective intermediaries; see [[agentic-privacy-preference-taxonomy]].
- **Stated-but-unconfirmed release.** The authors state they "will release" SuperScraper (screenshot + OmniParser, OS-input agent), crawler configs, measurement/analysis code, and per-page crawl data. Not confirmed as released at ingest; do not treat as available tooling.
- **Limits.** Single open model (Qwen3-VL-8B), single US vantage point, 26 pooled participants (descriptive only), robots.txt not enforced (standard measurement practice, per the paper's Ethics section).

## Source

- `raw/research/weekly-2026-11-09/03-agentic-crawler-tracker-measurement.md` — Sakib, Akram, Wijewickrama, Bilogrevic (Google), Jadliwala, *Beyond the Landing Page: Website Blocking, Tracker Visibility, and Human Alignment in Automated Web Crawls*, arXiv 2611.06197. Origin: academic measurement paper (UTSA + Google), IRB-approved. Audience: web-privacy measurement researchers. Purpose: guide crawler selection and validation for tracking studies; side-finding on delegated browsing. Trust: medium-high — strong method detail and human reference group, but single model, single vantage point, small participant pool; release of artifacts stated, not confirmed.

## Related

- [[browser-fingerprinting]] — crawler-vs-human fingerprinting validity
- [[fingerprinting-sdk-ecosystem]]
- [[transparency-tools]] — tracker-transparency methodology
- [[markup-citizen-browser]] — human panel as ground truth
- [[gesis-surf-data-donation]] — participant browsing data as baseline
- [[privacy-badger]]
- [[agentic-privacy-preference-taxonomy]]
- [[agents-vs-ecommerce-opacity]] — agents vs site-side interventions
- [[adversarial-prompt-injection-defense]]
- [[ghost-tool-calls]]
- [[privacytrace-mcp-leakage]]
- [[credential-disclosure-assistants]]
- [[health-data-opt-out-dark-patterns]] — consent-banner dark patterns
- [[dpagent-dark-pattern-repair]]
- [[surveillance-pricing-retail]]
- [[fairness-testing-algorithmic-pricing]]
- [[barriers-to-evidence]]
