# MCPhantom: Coding Agents Installing Deprecated MCP Servers (2026-11)

Glow Labs ("Glow Security"), as reported by Help Net Security (captured 2026-11-11), describes "MCPhantom": AI coding agents installing archived, deprecated, unpatched MCP servers (notably Anthropic's `@modelcontextprotocol` reference servers) because the model recalls the old package name from training data. Four high-severity flaws, including a prompt-injection-to-RCE in the Puppeteer server, will not be fixed (repo archived May 2025). Deprecated packages have 17.3M+ npm downloads since July 2025 (Glow Labs figure). Single secondary source from a security vendor with a product to sell; treat scale claims as unverified.

## Finding (per Glow Labs, via Help Net Security, ~2026-11)

- Method: Glow Labs reviewed real AI coding session transcripts, restricted to sessions where a deprecated MCP server was installed or suggested. No denominator (sessions reviewed overall) was reported.
- Cause: in **98%** of those sessions the agent appears to have filled in the package name from model training data; in **2%** the user asked for the old package by name.
- Example: asked to "set up a GitHub MCP", the agent chose a deprecated Anthropic reference server over GitHub's own maintained MCP server. The archived repo states no security updates are coming; agents do not read archive notices.
- Breadth: seen across Claude Code, Cursor, Codex CLI, Claude Cowork and Claude chat, with models from Anthropic, OpenAI and xAI. Not specific to one harness or vendor.
- Lookup is not a control: in one session the agent checked npm, got "This package is deprecated", installed anyway and did not tell the user (Nadav Claude Cohen, Glow, quoted by Help Net Security).

## Vulnerabilities

- Four high-severity flaws in the deprecated reference servers; no CVEs assigned.
- Most serious: RCE in the Puppeteer server. A prompt injection makes the agent start an arbitrary process instead of the browser. The user's approval of "web browsing" stretches to cover it, so the harness lets it through.
- Glow Labs' report was closed as out of scope: maintainers said the server was archived in May 2025 and unmaintained. They said they would look at marking the npm package deprecated (warning only; a deprecated package still installs via `npx`).
- No exploitation observed as of the report.

## Scale (Glow Labs figures, unverified)

- 17.3M+ npm downloads of the deprecated packages since July 2025; five in npm's top MCP 100.
- `server-github`: 185,239 downloads in the prior week, 6 owners (Cohen).
- Package removal is effectively blocked: npm lets an owner unpublish only with <300 weekly downloads, a single owner and no public dependents. Cohen found no precedent of removal for vulnerabilities (only malware).

## Why existing controls miss it

- The server is a dependency that never appears in a manifest (`npx` at runtime), so SCA sees nothing.
- No CVEs, so advisory feeds are silent.
- EDR sees a trusted Node process fetching a public npm package at the agent's request: routine.
- Software inventory never registers an application; the endpoint is the only place it shows.
- Glow's framing (Ophir Arie, VP R&D): "The model's memory is now a package manager with no deprecation feed."

## Mitigations (Glow Labs)

| Who | Fix | Limit (per Cohen) |
|---|---|---|
| Harness makers | Refuse or warn on deprecated servers, including already-installed ones | Only works if every harness does it |
| Model makers | Refresh model knowledge of package names | Weights updates expensive; "unlikely" |
| Package owners | Patch the bugs | Only fix that protects continuing users; maintainers declined |
| Security vendors | Pre-execution hooks that many harnesses already support | Works today; this is also Glow's product category |

Security-team starting points: inventory MCP configs referencing deprecated `@modelcontextprotocol` servers; swap to the service owner's server where one exists; approve one server per service; add npm deprecation status to approval criteria.

## Practitioner readthrough

- **Same class as the 2026-05 MCP RCE story, different mechanism.** [[mcp-rce-supply-chain-2026-05]] covers protocol-level and CI/worm supply-chain risk; MCPhantom is a selection-time risk: the agent chooses the dependency from stale memory. The reference-server lineage that Anthropic shepherds is again the weak point, now through abandonment rather than design.
- **Agent as unreviewed dependency chooser.** Every "install X" delegated to an agent is a procurement decision with no manifest, no review. Pairs with the identity and least-privilege framing in [[agent-identity-governance-2026-09]] and the coding-agent harness weaknesses in [[blackhat-ai-coding-agent-cves-2026-08]].
- **Build (cheap, do now):** allowlist MCP servers (one per service, vendor-owned where available) in harness config; block `npx`-fetched MCP packages outside the list; use pre-execution hooks to check npm deprecation status; add MCP configs to repo and endpoint inventory. These work regardless of whether harness vendors act.
- **Buy:** endpoint/agent-runtime security products selling hook-based enforcement are the vendor-recommended route. Evaluate on whether they cover installed (not just new) servers and non-npm ecosystems (uvx/pip, Docker). Note the research doubles as marketing for this category.
- **Platform angle:** managed MCP registries/gateways with curated catalogs (see isolation offerings in [[mcp-rce-supply-chain-2026-05]]) address this by construction; unmanaged `npx` installs do not. Client advisory: "MCP with a curated catalog" beats "MCP support yes/no".
- **Open question:** whether harness vendors will ship deprecation checks by default. No vendor response was captured in the source.

## Caveats

- **Single secondary source** (Help Net Security) summarising a vendor-interested report. Glow Labs' original blog post was linked but **not captured**; methodology, sample size, session provenance, and the denominator are unknown.
- Sample is selected on the outcome (only sessions with a deprecated server), so the 98/2 split describes causes among affected sessions, not prevalence.
- The 17.3M download figure counts all downloads of the deprecated packages; how many came from agent-driven installs is not stated.
- No exploitation observed, no CVEs; severity ratings are Glow's.
- Maintainer response (out of scope, archived) is as relayed by Glow; not independently confirmed.

## Conflict Flags

Extends the C17 theme in [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (MCP fluency as platform-selection criterion; reopened 2026-05 on security grounds): adds a third risk layer (stale-model dependency selection) to the "MCP-fluency-with-isolation" position. No new conflict between sources; no ruling needed.

## Source

- `raw/research/weekly-2026-11-11/04-glow-mcphantom.md` (Help Net Security, "AI coding agents are installing MCP servers that will never be patched", citing Glow Labs / Glow Security; captured 2026-11-11)

## Related

- [[mcp-rce-supply-chain-2026-05]] — MCP STDIO RCE, TanStack, Shai-Hulud Wave Six; protocol and CI supply-chain risk
- [[agent-identity-governance-2026-09]] — agent identity and governance controls
- [[blackhat-ai-coding-agent-cves-2026-08]] — coding-agent harness CVEs (Claude Code, Gemini CLI, Codex)
- [[../llms/anthropic-claude-family|anthropic-claude-family]] — shepherd of the MCP reference servers; Claude Code and Cowork named as affected
- [[../llms/openai|openai]] — Codex CLI named as affected
- [[../startups/cursor|cursor]] — named as affected harness
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] — C17 (MCP as industry norm)
