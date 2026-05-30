# MCP RCE Supply-Chain Disclosure (2026-05-08)

On **2026-05-08**, OX Security published a disclosure (researchers Moshe Siman Tov Bustan, Mustafa Naamnih, Nir Zadok, Roni Bar) describing a **by-design** RCE in Anthropic's Model Context Protocol (MCP) STDIO transport. The vulnerability is baked into Anthropic's reference SDKs across **Python, TypeScript, Java, and Rust** — affecting **>7,000 publicly accessible MCP servers** and **>150 million SDK downloads** as of disclosure.

**11+ CVEs** have been assigned across MCP-using projects since 2026-04-16. **Anthropic has declined to modify the protocol architecture, citing the behaviour as "expected."** Remediation falls to implementers; some vendors patched, most did not.

This is a load-bearing disclosure for the wiki because the 2026 enterprise narrative — established across [[google-cloud-next-2026-day2]], [[../platforms/salesforce|salesforce]], [[../platforms/snowflake|snowflake]], and [[../conflicts/open-questions-2026-04|C17]] — is "**MCP fluency = enterprise-platform-selection criterion (resolved-confirmed within 8 days of Salesforce Headless 360)**." The reference implementation has been a production RCE for >12 months.

## What OX Security disclosed (2026-05-08)

> "This flaw enables Arbitrary Command Execution (RCE) on any system running a vulnerable MCP implementation, granting attackers direct access to sensitive user data, internal databases, API keys, and chat histories."

> "Anthropic's Model Context Protocol gives a direct configuration-to-command execution via their STDIO interface on all of their implementations, regardless of programming language. As this code was meant to be used in order to start a local STDIO server, and give a handle of the STDIO back to the LLM. But in practice it actually lets anyone run any arbitrary OS command, if the command successfully creates an STDIO server it will return the handle, but when given a different command, it returns an error after the command is executed."

> "What made this a supply chain event rather than a single CVE is that one architectural decision, made once, propagated silently into every language, every downstream library, and every project that trusted the protocol to be what it appeared to be. Shifting responsibility to implementers does not transfer the risk. It just obscures who created it."

## Attack surface categories (per OX Security 2026-05-08)

1. Unauthenticated and authenticated command injection via MCP STDIO.
2. Unauthenticated command injection via direct STDIO configuration with hardening bypass.
3. Unauthenticated command injection via MCP configuration edit through zero-click prompt injection.
4. Unauthenticated command injection through MCP marketplaces via network requests, triggering hidden STDIO configurations.

## CVEs assigned (this disclosure batch)

| CVE | Project | Status |
|---|---|---|
| CVE-2025-65720 | GPT Researcher | Assigned |
| CVE-2026-30623 | LiteLLM | **Patched** |
| CVE-2026-30624 | Agent Zero | Assigned |
| CVE-2026-30618 | Fay Framework | Assigned |
| CVE-2026-33224 | Bisheng | **Patched** |
| CVE-2026-30617 | Langchain-Chatchat | Assigned |
| CVE-2026-33224 | Jaaz | Assigned |
| CVE-2026-30625 | Upsonic | Assigned |
| CVE-2026-30615 | Windsurf | Assigned |
| CVE-2026-26015 | DocsGPT | **Patched** |
| CVE-2026-40933 | Flowise | Assigned |

## Prior independent disclosures on the same root cause

| CVE | Project | Year |
|---|---|---|
| CVE-2025-49596 | MCP Inspector | 2025 |
| CVE-2026-22252 | LibreChat | 2026 |
| CVE-2026-22688 | WeKnora | 2026 |
| CVE-2025-54994 | @akoskm/create-mcp-server-stdio | 2025 |
| CVE-2025-54136 | Cursor | 2025 |

The architectural pattern has been disclosed independently for >12 months. This is the first synthesis presenting it as a single supply-chain event with the **Anthropic-side load-bearing fact**: the protocol is not getting fixed.

## Anthropic's response

Per OX Security disclosure (2026-05-08): "Anthropic, however, has declined to modify the protocol's architecture, citing the behavior as 'expected.' While some of the vendors have issued patches, the shortcoming remains unaddressed in Anthropic's MCP reference implementation, causing developers to inherit the code execution risks."

This is the procurement-relevant fact: **Anthropic, the protocol shepherd, is positioning STDIO-config-to-command as intended behaviour.** Defence falls to implementers (sandboxing, network isolation, untrusted-input handling).

## Affected ecosystem (partial list)

- **Coding-agent harnesses:** Cursor (CVE-2025-54136), Windsurf (CVE-2026-30615), VS Code, Claude Code, Gemini CLI.
- **Agent frameworks:** LangChain, LangFlow, Flowise, LettaAI, LangBot, Agent Zero.
- **LLM proxies / orchestration:** LiteLLM (patched), Bisheng (patched).
- **Vertical agents:** GPT Researcher, Upsonic, Fay Framework.

## Remediation recommendations (OX Security 2026-05-08)

- Block public IP access to sensitive services.
- Monitor MCP tool invocations.
- Run MCP-enabled services in a sandbox.
- Treat external MCP configuration input as untrusted.
- Only install MCP servers from verified sources.

## Implications for the enterprise-AI landscape

### MCP-fluency has a security asterisk now

Through the 2026-04 ingest cycle, the wiki tracked MCP standardisation as a **resolved-confirmed industry norm** ([[../conflicts/open-questions-2026-04|C17]] update 2026-04-23: "MCP fluency is now a platform-selection criterion, not an optional integration question"). That framing remains directionally correct but **incomplete**: the reference implementation has been a production RCE the entire time.

The new procurement criterion is not "MCP support yes/no" but **"MCP support with vendor-provided isolation"**:

- Google Cloud → **Model Armor** + Agent Gateway sandboxing (GEAP, 2026-04-22) — see [[google-cloud-next-2026-day2]]. Previously framed as nice-to-have; now load-bearing.
- Salesforce → **Agent Fabric** centralised governance — see [[../platforms/salesforce|salesforce]].
- Microsoft → **Agent 365 + Defender + Intune** runtime controls + MCP server context mapping (June 2026 preview) — see [[../platforms/microsoft|microsoft]].
- Snowflake → Cortex Code MCP integration (2026-04-21) — sandbox status not separately disclosed.

For DIY / self-hosted MCP deployments, the recommended posture is sandbox + network isolation + treat-config-input-as-untrusted **at all times** — i.e., adopting MCP without isolation now carries a CVE inheritance risk.

### Position B for C17

Original C17 (2026-04-23): "MCP fluency is platform-selection criterion (resolved-confirmed)."

Position B (this run, 2026-05-10): "MCP fluency means inheriting an unfixed protocol-level RCE surface across all four reference SDKs; **vendor-provided MCP-isolation** (Model Armor, Agent Fabric, Agent 365 Defender controls, sandboxed marketplaces) becomes the actual procurement criterion, not MCP support per se."

Both positions are simultaneously true. The wiki position evolves to **"MCP-fluency-with-isolation"**.

### Anthropic governance signal

Anthropic shipped the protocol the entire 2026 enterprise stack standardised on, then declined to change it after a 4-SDK supply-chain RCE disclosure. This is a load-bearing **governance** signal that should inform Anthropic-vendor-risk discussion in client advisory — alongside the model-quality signals already on [[../llms/anthropic-claude-family|anthropic-claude-family]].

### Alternative protocols are now competitively positioned

A2A (Google), ANP (community), and proprietary connector frameworks (e.g., OpenAI Workspace Agents' connector layer — MCP usage not confirmed in launch materials, see [[../llms/openai|openai]]) now have a clean differentiation pitch: **"adopt our protocol and you don't inherit MCP's RCE surface."** Watch for this framing in 2026-Q3 platform launches.

## TanStack npm Supply Chain Attack — "Mini Shai-Hulud" (2026-05-11, TeamPCP)

**Different attack vector than MCP STDIO RCE; same risk theme: AI-company developer toolchains are now explicit targets.**

### What happened (2026-05-11–12)

Threat group **TeamPCP** forked the TanStack/router repo and opened a pull request triggering a `pull_request_target` GitHub Actions workflow. The workflow wrote to a shared pnpm cache store, which TeamPCP poisoned with malicious packages — a chain of **three GitHub Actions vulnerabilities** exploited in sequence. No maintainer was phished; the CI pipeline was made to steal its own publish token at the moment of creation.

> "The attacker managed to engineer a path where our own CI pipeline stole its own publish token for them, at the exact moment it was created, by way of a cache that everyone in the chain implicitly trusted." — TanStack incident followup, 2026-05-12

Scope (disclosed by 2026-05-16 including Hunt.io follow-up):

| Ecosystem | Packages | Key package |
|---|---|---|
| TanStack router | 42 | `@tanstack/react-router` — 12.7M weekly downloads |
| UiPath automation | 65 | — |
| Mistral AI | npm + PyPI | `mistralai` SDK |
| OpenSearch | — | 1.3M weekly npm downloads |
| Guardrails AI | PyPI | — |

Total: **170+ npm packages + 2 PyPI packages → 404 malicious versions** published.

### Payload

- Credential theft (AWS keys across all 19 availability zones incl. GovCloud, env vars, SSH keys, dotenv files, Docker container secrets).
- Self-propagation through npm ecosystem.
- Persistent destructive daemon: on systems geolocated to Israel or Iran, 1-in-6 probability gate triggers audio playback at max volume + deletion of all accessible files. Malware exits on Russian locale.
- **FIRESCALE** fallback C2: when primary C2 (`83.142.209[.]194`) is unreachable, the malware searches all public GitHub commit messages worldwide for a signed alternative server URL verified against an embedded 4096-bit RSA key. Exfiltration has three tiers (C2 → FIRESCALE → victim's own GitHub repo); blocking any single tier leaves the others intact.

### Novel: first malicious npm with valid SLSA provenance (confirmed 2026-05-12)

Because the package was published via the legitimate CI pipeline's own publish token, it carries **valid SLSA provenance**. This is the first documented case of this bypass. The conventional "use packages with provenance" supply-chain hardening advice is insufficient here — provenance attests the build process was followed, not that the build inputs were clean.

### Impact on AI companies

**OpenAI** (disclosed 2026-05-13):
- 2 employee devices compromised via corporate environment.
- Unauthorized access + credential-focused exfiltration from a limited subset of internal source code repositories those employees could access.
- Impacted repositories included **signing certificates for iOS, macOS, and Windows products** → OpenAI revoked and reissued certificates. macOS ChatGPT Desktop, Codex App, Codex CLI, and Atlas users must update before **2026-06-12** (when old certs are revoked by built-in macOS protections).
- No user data, production systems, or IP compromised or modified, per OpenAI disclosure.
- Note: this is the second macOS certificate rotation in ~2 months; the first (mid-April 2026) was triggered by a North Korean group (UNC1069) compromising the Axios library via a separate GitHub Actions vector.

**Mistral AI** (advisory updated 2026-05-16):
- 1 developer device compromised; `mistralai` npm + PyPI SDKs released as trojanized versions.
- Codebase management system temporarily compromised; remediated.
- TeamPCP subsequently threatened to leak ~5 GB of internal Mistral source code, demanding $25,000 BIN, with intent to publish free to forums if unsold within a week.
- No evidence of infrastructure breach.

### TeamPCP campaign context

This attack is part of an ongoing TeamPCP campaign spanning at least November 2025–May 2026:
- C2 infrastructure (`83.142.209[.]0/24`) was provisioned November 2025 and left dormant to accumulate clean history.
- Same subnet used across: LiteLLM PyPI compromise, Trivy scanner hijack (GitHub Actions), Checkmarx KICS attack (March 2026), Jenkins AST Plugin backdoor (May 2026).
- At least 4 distinct payloads on this infrastructure: Cloud Stealer (CI/CD secrets), cryptocurrency miner (December 2025 phase), VECT ransomware (late March 2026, deployed using previously stolen credentials), FIRESCALE Python toolkit.
- TeamPCP has since announced a public **supply-chain attack contest** in partnership with Breached cybercrime — $1,000 Monero prize for compromising open-source packages using the open-sourced Shai-Hulud worm.

### Implications for the enterprise-AI landscape

1. **AI company developer tooling is explicitly targeted.** OpenAI and Mistral both run JavaScript/Python SDK toolchains in corporate dev environments. These are enterprise-facing developer toolchains, not research one-offs. The attack surface is the everyday npm install.
2. **SLSA provenance is not a sufficient control.** The novel provenance bypass invalidates "require provenance" as a standalone policy. Layered controls needed: dependency pinning to known-good digests, hermetic build environments, network isolation for CI runners, post-publish scanning.
3. **GovCloud credential targeting signals ambition.** AWS GovCloud regions are restricted to US government agencies and defense contractors. A credential stealer covering those AZs by design suggests TeamPCP is targeting or selling access to government-adjacent organizations.
4. **Connects to MCP RCE theme here:** Both this and the MCP STDIO RCE are supply-chain events propagating silently through trusted build/runtime infrastructure. The common thread is that architectural trust decisions made once (in a CI workflow, in an SDK) propagate into every downstream consumer without re-evaluation. See also [[ai-infrastructure-frontiers-2026]] on enterprise security posture.

## Build-vs-buy signals

- **Buy MCP-fluent platforms with vendor-provided isolation** — Google GEAP Model Armor, Salesforce Agent Fabric, Microsoft Agent 365 — defence-in-depth is layered above MCP, but the substrate vulnerability persists.
- **Build:** if you adopt MCP, you inherit the RCE surface. Sandboxing + network isolation + untrusted-config handling is a **procurement requirement**, not optional.
- **Watch:** alternative protocols (A2A, ANP, custom) are now competitively positioned. The "bet on MCP" thesis from C17 needs a security-overhead asterisk in any client advisory.

## Anti-pattern lesson

STDIO transport with config-to-exec mapping = RCE-by-design. Worth flagging in any internal protocol-design discussion as a **case study**.

## Source

- `raw/research/weekly-2026-05-10/04-mcp-rce-vulnerability.md` (The Hacker News, citing OX Security disclosure 2026-05-08)
- `raw/research/weekly-2026-05-28/05-tanstack-supply-chain.md` (The Hacker News, citing OpenAI disclosure, Mistral advisory, TanStack incident followup, Hunt.io analysis; updated 2026-05-16)

## Related

- [[google-cloud-next-2026-day2]] — Model Armor / Agent Gateway as MCP isolation
- [[../platforms/salesforce|salesforce]] — Agent Fabric / Headless 360 MCP exposure
- [[../platforms/microsoft|microsoft]] — Agent 365 Defender controls + MCP context mapping
- [[../platforms/snowflake|snowflake]] — Cortex Code MCP integration
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — protocol-shepherd governance signal
- [[../startups/cursor|cursor]] — affected (CVE-2025-54136 + Windsurf-shared codebase implication)
- [[../llms/openai|openai]] — 2 employee devices compromised; code-signing cert revocation + macOS update requirement
- [[ai-infrastructure-frontiers-2026]] — agent governance / MCP isolation; enterprise security posture
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C17 reopened)
