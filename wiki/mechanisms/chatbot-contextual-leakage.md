# Chatbot Contextual Leakage

Third-party analytics, advertising and session-replay scripts embedded in AI chatbot web UIs capture conversational context, not just page metadata. Bekos et al. (2026) audited 42 chatbot platforms (25 general-purpose, 17 task-specific in health, legal, education): 21 leak conversation titles and 9 leak verbatim prompts to third-party trackers; in the general-purpose set, 11 of 13 context-leaking platforms also expose the user's email, tying context to a named person. The cause is default tracker configuration: scripts read `document.title` and similar page attributes, and chat UIs generate each session's title from the user's prompt.

## Mechanism

- Each chat is a dynamically titled sub-page; trackers (Google Analytics, Microsoft Clarity, TikTok Pixel, X/Twitter, Amplitude, Naver, Volcengine) read the title as ordinary page metadata and transmit it.
- Leaks are event-driven: submit, navigate, delete, scroll and click each can trigger a flow. Titles generated after the first prompt are missed by single-prompt audits.
- Dense third-party surface: CSPs reference up to 66 (You.com), 57 (QuillBot) and 56 (Claude) third-party domains.
- Privacy notices describe analytics as page-view/click/session-duration collection; several state data is not sold or shared for targeted advertising while ad pixels collect conversational context.
- ChatGPT and Grok had such trackers during the study and removed them before submission; class actions against OpenAI and Perplexity allege similar transmission.

## Method and limits

- Puppeteer multi-interaction capture plus VisibleV8 JS instrumentation, attributing each flow to one of five interaction scenarios and to the capture mechanism.
- Window 6-20 May 2026; single US-East vantage with tracking consent accepted; free tiers and web UIs only. No test of consent honoring, jurisdiction variance, paid tiers or mobile/desktop apps.
- Artifact (traffic logs, VV8 traces, analysis scripts): https://zenodo.org/records/22831655. Whether the tooling is released as standalone code is unconfirmed.
- Preprint; trust medium-high.

## Remediation proposed by the authors

- Client-side script blocking prevents the observed leakage.
- Platforms: less specific generated titles; do not embed conversation content in page attributes.
- Vendors: chat-specific analytics that exclude content-bearing attributes.
- Auditors: test the full interaction set, not page load or submit alone.

## Counter-power angle *(editorial)*

- The per-platform table is a ready scorecard for [[mechanisms/transparency-tools]]; the multi-interaction protocol suggests a Blacklight-style scanner for chatbots, extending the [[tools/markup-citizen-browser]] measurement tradition.
- Notice-versus-practice mismatch is usable evidence for complaints and [[mechanisms/dsar-and-data-deletion]] requests.
- Individual blocking works but is per-user; a collective audit-and-disclose cycle (ChatGPT, Grok remediated after exposure) is the leverage shown.

## Source

- Bekos, Tsouvalas, Nikiforakis, Polychronakis, "Penny for Your Prompts: A Measurement Study of Contextual Leakage in AI Chat Platforms", arXiv 2610.37467 (2026). Raw: `raw/research/weekly-2026-11-02/02-chatbot-contextual-leakage.md`.

## Related

- [[mechanisms/browser-fingerprinting]] — browser-layer tracking; this page covers content leakage via analytics scripts
- [[mechanisms/fingerprinting-sdk-ecosystem]] — third-party SDK/script supply chain on mobile
- [[tools/privacy-badger]] — script blocking would prevent the observed flows
- [[tools/markup-citizen-browser]] — browser-based web-tracking measurement precedent
- [[mechanisms/transparency-tools]] — audits as scorecards
- [[mechanisms/dsar-and-data-deletion]] — complaint and access-request evidence
- [[mechanisms/agentic-privacy-preference-taxonomy]] — AI product data practices and opt-out gaps
- [[mechanisms/health-data-opt-out-dark-patterns]] — health-domain tracking exposure
