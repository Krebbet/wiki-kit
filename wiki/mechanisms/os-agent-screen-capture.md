# OS-level AI agent capture of app data

Signal (Signal Technology Foundation blog, 2026-11-20) reports that OS-integrated AI agents (iOS 27 Siri "Onscreen Awareness", Android Gemini Intelligence, Windows Recall) read app screens, bypassing app-level privacy guarantees such as E2EE once content is decrypted for display. Signal's response is a tech workaround: blocking screenshots on iOS, and auto-enabling "Screen security" on Android when an AI assistant is detected. It admits coverage is incomplete (filesystem access, macOS, many Android vendors) and that OS vendors offer app developers no robust opt-out API or documentation. Single advocacy source; needs corroboration.

## Mechanism

- Agent capture happens at the platform layer, below the app. Third-party agents (e.g. Meta Muse) reportedly abuse accessibility permissions.
- Signal's measures: screenshot blocking flag; Android auto-enable on assistant detection; macOS users advised to add Signal to Siri "Excluded Apps" (an EFF-reported Siri per-app exclusion, Oct 2026; not captured here).
- Signal rejects confidential computing as sufficient: the provider still holds the power.

## Why it matters here

- Chokepoint: app-layer counter-power depends on OS-vendor goodwill (three vendors control the platform layer).
- Any collective tool (membership, DSAR drafts, price evidence on screen) inherits the exposure. *(editorial)*
- Mild tension with consumer-side-agent optimism ([[mechanisms/agentic-privacy-preference-taxonomy]], [[mechanisms/agents-vs-ecommerce-opacity]]): here agent access is the threat, so deep-permission consumer agents need scoping.
- Asks (developer opt-out API, documentation) are candidate standards/policy targets.

## Source

- `raw/research/weekly-2026-11-23/01-signal-os-agent-screen-capture-block.md` — https://signal.org/blog/protecting-your-privacy/ (advocacy / primary on Signal's own actions; trust high for Signal's actions, OS-vendor behaviour is Signal's account).

## Related

- [[mechanisms/ghost-tool-calls]]
- [[privacytrace-mcp-leakage]]
- [[chatbot-contextual-leakage]]
- [[campaigns/keep-android-open]] — same OS-chokepoint theme
- [[counter-power/adversarial-interoperability]]
- [[local-network-graph-products]] — Signal as covered case
- [[strategies/bootstrap-strategy]] — mobile-first entry points depend on OS-agent policy
