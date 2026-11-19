# Cloudflare Kitesurf agent browser (2026-11)

Cloudflare launched Kitesurf, a from-scratch browser engine for agents (Rust compiled to WebAssembly, running on Workers), as a free beta inside Browser Run; the source article is dated "today" with a 2026-11-18 capture and no explicit launch date. It claims 3-7x lower CPU/memory than Chromium. **Watch, and trial it for extraction/screenshot workloads; do not migrate Chromium-dependent flows yet.** All numbers are vendor-claimed from a 14-URL corpus, open-sourcing is a stated plan rather than a shipped fact, and the only source is a single trade-press rewrite of Cloudflare's blog post.

## Mechanism (per TNW rewrite of Cloudflare's blog, captured 2026-11-18)

- Not Chromium: a new engine in Rust/Wasm on Workers. It drops tabs, extensions, themes, pixel-perfect rendering and 60-fps scrolling, and keeps structured content extraction, screenshots and session isolation.
- Security model: every page load is untrusted input, every session stateless, every component isolated.
- Compatibility: works with Puppeteer, Playwright, and any MCP client that speaks CDP (Chrome DevTools Protocol). The drop-in claim is untested here. It passes 215K+ Web Platform Tests (WPT), with more added weekly. No pass rate is given, so coverage is unknown.
- Built in 12 weeks, first commit to public beta.
- Pricing: free in beta via Browser Run. Post-beta pricing is not disclosed.

## Claims (vendor-claimed, 14-URL corpus)

| Metric vs Chromium | Screenshots | HTML extraction |
|---|---|---|
| CPU | 3.1x lower | 3.8x lower |
| Memory | 4.7x lower | 7x lower |

The "~7x" headline is the best case (HTML extraction memory). Chromium is still ~1.7x faster on wall-clock because its JIT beats a cold software renderer. The savings are therefore concurrency density and cost, not latency. The sample is small, and no independent benchmark exists.

## Open-source, license and self-hosting

- Source says Cloudflare "plans to open source Kitesurf once it is ready" and later let customers deploy their own instances on their own accounts. **It does not state that the code is released, name a license, or give a release date.** The brief's framing of Apache 2.0 and open-sourcing on 2026-11-13 is not supported by the captured source. Verify against the Cloudflare blog or repo before citing.
- Nothing in the source covers authentication for self-hosted instances. Treat an unauthenticated self-hosted CDP endpoint as an open remote-control surface until docs say otherwise. *(inference, not sourced)*

## Market readthrough

- Cloudflare's framing: bots now generate most web traffic and AI agent activity grew nearly 8,000% in a year (TNW claim, unverified). Cloudflare pairs this with blocking non-paying AI crawlers: charge the bots that take, serve the bots that work.
- Agent-browser and sandbox space: the wiki has no pages for Browserbase-style hosted-browser vendors. The only sandbox-startup signal is Tilde.run (agent sandbox with a transactional filesystem) and Mistle, both on the watchlist only. Kitesurf commoditises the browser-runtime layer from the infrastructure side; hosted-browser startups must differentiate on session tooling, anti-bot handling and state, not on raw runtime cost. *(synthesis, thin evidence)*
- Cloudflare already appears as a self-hosted sandbox target for Anthropic Managed Agents (see [[landscape/anthropic-enterprise-distribution-2026-05]]) and is a Platinum member of the AAIF (see [[landscape/google-a2a-agentic-foundation-2026-08]]). Kitesurf adds a browser primitive to that position.

## Build vs buy

- **Buy (Browser Run):** pick it if the workload is extraction or screenshots at high concurrency on Workers and CDP compatibility holds for your scripts. Free beta means cost is unproven past the beta.
- **Build/self-host Chromium:** stay here for rendering-fidelity, anti-bot or JIT-heavy flows until WPT pass rates and a release are public.
- **Wait for the OSS release** before betting on self-hosting. The promise of deploying on your own account is the build-side option, and it is not yet available.
- Stateless sessions fit agents that carry state externally. Flows needing persistent logins or cookies need a workaround.

## Source

- `raw/research/weekly-2026-11-18/04-cloudflare-kitesurf.md` (The Next Web, captured 2026-11-18; relays blog.cloudflare.com/kitesurf)

## Related

- [[landscape/github-copilot-local-sandboxing-2026-10]] — first-party agent sandbox, tool-execution side
- [[landscape/anthropic-enterprise-distribution-2026-05]] — Cloudflare as self-hosted sandbox target
- [[landscape/google-a2a-agentic-foundation-2026-08]] — AAIF membership context
- [[landscape/agentic-compute-pricing-2026-04]] — agent compute cost context
- [[landscape/mcp-rce-supply-chain-2026-05]] — MCP threat context for CDP/MCP clients
