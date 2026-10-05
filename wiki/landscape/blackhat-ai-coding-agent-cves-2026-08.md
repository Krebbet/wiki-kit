# Black Hat USA 2026: CI-Harness RCE Flaws Across Claude Code, Gemini CLI, and Codex (2026-08-05)

Novee Security's Black Hat USA talk (2026-08-05) showed that in each vendor's *default CI configuration*, a GitHub issue posted by a privilege-less account could reach code execution or hijack the next agent run — in Anthropic's Claude Code, Google's Gemini CLI, **and** OpenAI's Codex, independently. The common root cause: the "harness" (the code between model and execution) trusts a value one part marks safe, and a later part acts on it with more authority than that mark was meant to grant. The three vendors responded with materially different postures.

## Source

Novee Security Black Hat USA 2026 talk, covered by The Hacker News, HackRead, VentureBeat (2026-08-05 to 2026-08-08). Captured `raw/research/weekly-2026-08-12/01-01-blackhat-ai-coding-agent-cves.md`. Deeper technical detail: The Hacker News, 2026-08-19, `raw/research/weekly-2026-08-19/03-claude-code-gemini-cli-ci-secrets-2026-08.md`.

## Claude Code (Anthropic) — CVE-2026-54316

- **Flaw:** the command validator runs 23 checks but strips single-quoted text *before* those checks execute — correct behavior for bash generally, but exploitable. A payload hidden in the value of a `git push --receive-pack` flag reached the CI runner unfiltered.
- **Exfiltration technique:** attackers used Hugging Face's public download counter as a covert, one-character-at-a-time channel to exfiltrate a leaked API key — any externally-observable counter/metric an agent can influence is a potential covert channel.
- **Severity dispute:** Anthropic rates it Moderate at CVSS v4 6.0 (GHSA-fg94-h982-f3mm); NVD independently scored it CVSS v3.1 9.1. The two scores aren't directly comparable (different scoring versions, NVD hasn't rescored under v4) — an open question, not a settled severity.
- **Status:** affected every release from 0.2.54 to 2.1.163; fixed in 2.1.163. Not in CISA's Known Exploited Vulnerabilities catalog as of 2026-08-07. Anthropic issued a CVE and shipped a patch.

## Gemini CLI (Google) — CVE-2026-12537

- **Flaw (two chained issues):** the tool allowlist was parsed only at registration time with nothing enforcing it at runtime — under `--yolo` mode, every model-requested command was auto-approved regardless of the registered allowlist. Separately, the container launcher had an OS command-injection bug reachable via a crafted `.gemini/.env` file, executable *before* the sandbox even started.
- **Severity:** CVSS v4 **10.0** (maximum) — described in the source as "the worst of the two." Fixed in Gemini CLI 0.39.1 and `run-gemini-cli` 0.1.22 (GHSA-wpqr-6v78-jr5g).
- **Notable framing:** this bug "did not require talking a model into anything" — a pure host-execution/harness flaw, not prompt injection, despite being filed as an "AI agent" CVE.
- **Status:** not in CISA's KEV catalog as of 2026-08-07. Google issued a CVE and shipped a patch, same posture as Anthropic.

## OpenAI Codex — no CVE issued

- **Flaw:** an instruction-file poisoning chain. In the vulnerable CI configuration, two Codex passes ran inside a single job sharing one checkout; the first pass could write `AGENTS.md`, which the second pass then loaded as its own instructions. A failing JSON-validation step between the two passes is what launched the second pass — an error-handling path became the exploit trigger.
- **Vendor posture:** OpenAI's position, per Novee, is that the sandbox "behaved exactly as documented." No CVE and no product-version patch were issued; the fix is a repository/workflow-level change (separate the two passes into different jobs, run with drop-sudo + read-only sandbox) plus a documentation update listing repo instruction files like `AGENTS.md` as part of the untrusted-input surface.
- **Materially different stance** than Anthropic (CVE + patch, Moderate rating) or Google (CVE + patch, CVSS 10.0) for a structurally similar harness-trust bug.

## Vendor-posture comparison (build-vs-buy signal)

| Vendor | CVE issued | Patch issued | Severity | Framing |
|---|---|---|---|---|
| Anthropic (Claude Code) | Yes (CVE-2026-54316) | Yes (2.1.163) | Self-rated Moderate/6.0; NVD 9.1 | Product vulnerability |
| Google (Gemini CLI) | Yes (CVE-2026-12537) | Yes (0.39.1 / 0.1.22) | CVSS v4 10.0 | Product vulnerability |
| OpenAI (Codex) | No | No (workflow-only fix) | Not scored | Configuration/workflow issue, not a product flaw |

The common lesson for any team building an in-house agent harness: a downstream component trusting an upstream "safe" marking without re-validating at the point of execution is a general failure mode, not vendor-specific. Runtime allowlist enforcement (not registration-time parsing) and treating repo-controlled files (`AGENTS.md`, hook configs) as untrusted input are the concrete controls this disclosure argues for.

## Root causes and patched versions (deeper sourcing, 2026-08-19)

The Hacker News (2026-08-19) published deeper technical detail on the same Aug 5 disclosure — same three CVEs/findings, same Novee Security attribution, confirmed by matching CVE numbers and dates. Not a new incident; extends the record above.

- **Claude Code — the quote-stripping bypass has no CVE of its own.** Distinct from CVE-2026-54316: the harness's command validator strips single-quoted text from shell commands *before* running its 23 safety checks — correct bash-parsing behavior in isolation, but it let a payload placed inside the *value* of a flag like `git push --receive-pack` (a flag git itself executes) reach the CI runner untouched. Novee's framing: "one part marked a value safe, and a later part acted on that value with more authority." No CVE, no publicly stated fixed version for this specific bypass.
- **Patched versions confirmed:** Claude Code CVE-2026-54316 fixed in **2.1.163** (affected every release from 0.2.54 onward). Gemini CLI CVE-2026-12537 fixed in **0.39.1** / `run-gemini-cli` **0.1.22**.
- **Exploitation window:** CISA lists exploitation as "none" for CVE-2026-54316 and it is not in the KEV catalog as of 2026-08-07 — but a public GitHub repo self-described as a reproduction lab for the flaw has been **live since 2026-06-18**, before the Aug 5 disclosure/patch. A live-exploit-code exposure window worth noting for risk framing even absent observed exploitation.
- **Codex — confirmed no product fix.** The Hacker News source is explicit: "Neither change shows that Codex itself now handles a writable instruction file differently; what the sources establish is a repository-level workflow fix and a documentation update." OpenAI's codex-action guidance now lists repo instruction files (e.g. `AGENTS.md`) as part of the untrusted-input surface, and recommends running Codex as the **last step** in a job (it may otherwise leave files behind for privileged steps that run after it).
- **Unifying lesson (Novee, quoted directly):** re-verify trust annotations at the point of execution, not just where they're first computed. Three concrete controls generalize to any CI-integrated agent harness: (1) enforce allowlists at execution time, not registration/parse time; (2) shell-quote stripping done for one purpose (bash correctness) can create a bypass if a downstream consumer interprets the same string differently; (3) isolate multi-pass agent jobs into separate checkouts so an earlier pass can't produce content a later pass treats as trusted instructions.

**Build-vs-buy signal:** Novee tested each vendor's own repo running its own agent in the *default* CI configuration — these are vendor-shipped defaults, not obscure misconfigurations. "Buy" still requires the buyer to audit CI trust boundaries themselves rather than assume vendor-shipped CI actions are safe out of the box.

## GitSpawn: git-config RCE across seven coding agents (Manifold Security, 2026-09-01/09)

A mechanistically distinct but pattern-similar disclosure: Manifold Security's "GitSpawn" report shows that **background context-gathering `git status`/`git diff` calls** — run by coding agents on startup, outside their sandbox, to understand a repo — trigger a repo-supplied `core.fsmonitor` command (or, in one still-undisclosed case, a second config key) during git's index refresh, **before any trust/approval prompt fires**. Delivery requires the malicious repo to arrive as raw files with an existing `.git/config` (zip, shared drive, sync folder, USB) — cloning or fetching a hostile URL does **not** trigger it, since git never transmits local config that way.

Eight findings across seven agents, vendor response split sharply:

| Agent (vendor) | Status at publication | Notes |
|---|---|---|
| **Claude Code** (Anthropic) | 1 of 2 findings patched | `core.fsmonitor` sink fixed (2.1.196); a second, distinct config-key sink in the `claude ultrareview` path remains **unpatched** as of 2.1.252 (2026-09-01) — the fix wasn't generalized across all internal git call sites |
| **Goose** (open-source, aaif-goose) | **Patched** (1.44.0) | CVE-2026-72718 assigned by maintainers; one of the only fully cooperative, CVE-tracked responses |
| **Hermes Agent** (NousResearch) | **Unpatched** | Six contact attempts across five channels, private advisory never triaged; CVE-2026-71963 assigned independently by VulnCheck, not the vendor — weakest vendor-response case in the report |
| **Qwen Code** (Alibaba) | **Unpatched** | Alibaba's security response centre accepted the report (2026-07-07) but shipped no fix in ~2 months; fires pre-authentication |
| **Grok Build** (xAI/SpaceXAI) | **Unpatched** | xAI had already dismissed an independent report of the same bug class as "informative" before Manifold's report; fires on the user's first keystroke |
| **OpenAI Codex** | **Patched** | Related-class finding, duplicate of another researcher's report; no case-study detail published |
| **Cursor** | **Patched** | Same as Codex — duplicate report, patched, no detail published |

Five of Manifold's reports came back as duplicates of findings independent researchers had already filed (one on the same day) — multiple security researchers converged on this vulnerability class independently around mid-2026, because every vendor implemented the same "gather git context on startup" pattern without sanitizing repo-supplied config.

**Manifold's framing:** not a model/AI-safety problem — "ordinary plumbing," a subprocess-sanitization bug replicated near-identically across at least seven unrelated codebases. Recommended mitigation: sanitize config on every context-gathering git call (e.g., `git -c core.fsmonitor=false status`); users receiving a repo as raw files should inspect `.git/config` before opening it in an agent. Manifold's own pitch is that existing controls (EDR, API gateways) don't see this layer — "EDR sees familiar developer tooling doing familiar things," gateways see already-authenticated traffic — and that the same class of risk (arrives as files, carries its own config, trusted on arrival) generalizes beyond git repos to skills, MCP servers, and plugins.

**Relationship to the Black Hat findings above:** same class of failure (a harness trusts a value without re-validating it at the point of execution) but a mechanistically distinct sink (git-config command execution via index refresh, not CI-harness allowlist/instruction-file poisoning) and a different disclosure channel (independent security researcher, not a conference talk). Treat as a second, corroborating data point for the same underlying lesson rather than a duplicate finding.

**Source:** Manifold Security, "GitSpawn: A Single Flaw Lets Untrusted Repos Run Code in Claude Code, Codex, Cursor, and Grok" (2026-09-01, updated 2026-09-09). Captured `raw/research/weekly-2026-09-09/04-gitspawn-rce-coding-agents.md`.

## Plugin4Shell (2026-09-17)

A third, mechanistically distinct disclosure in the same running thread. Air.security — self-described as publishing "the third act" of a research series after "The Story of Skills" (a malicious skill went viral, ~26,000 agents seized) and "SkillJacking" (925 hijacked skills, 134,000 agents affected via repo takeover) — reports "Plugin4Shell," a zero-click RCE that defeats plugin-marketplace SHA pinning across **Claude Code, OpenAI Codex, GitHub Copilot, and Gemini CLI**.

**Mechanism — a plugin-marketplace trust-boundary bypass, not a config-poisoning bug.** SHA pinning is the industry's standard answer to plugin rug-pulls: review a commit once, pin it, trust that commit runs forever. Plugin4Shell breaks the pin itself via git ref/commit resolution ambiguity:

- **Claude Code / Codex / GitHub Copilot variant:** these agents `git clone` the plugin repo then `git checkout <40-hex pinned SHA>`. An attacker who controls the plugin's upstream repo names a branch literally as the pinned 40-hex SHA and sets it as the repo's **default branch**. Git prefers a ref over an object id when the two are ambiguous (emitting only a `refname is ambiguous` warning), so `checkout` silently resolves to the attacker's branch instead of the pinned commit — "it never matters whether the pinned commit is still present." GitHub itself rejects branch names shaped like a 40-hex hash, but Bitbucket and self-hosted git servers allow it — and per the source, "Anthropic's own documentation lists Bitbucket and self-hosted git as valid marketplace backends."
- **Gemini CLI variant (related but distinct):** pins via `git fetch origin <sha>` then `git checkout FETCH_HEAD`. The fetch correctly records the pinned commit in `.git/FETCH_HEAD`, but if the attacker's default branch is literally named `FETCH_HEAD`, checkout resolves to that branch instead, silently discarding the fetched pinned commit.
- **Zero-click:** the same checkout logic re-runs on background plugin auto-update — "the default in Claude Code and Codex" — so an already-installed, already-trusted plugin flips to attacker content with no install step and no prompt, once the marketplace-pinned SHA is later bumped upstream (via a PR the marketplace owner approves).
- **Root cause, per the source:** "Every affected agent checks out the pinned commit but never checks that it actually landed there. That one missing check is the whole bug." Fix: after checkout, `test "$(git rev-parse HEAD)" = "<pinned-sha>" || abort` — verify resolved `HEAD`, not the requested ref. Must run agent-side, since "the pin is resolved on the client, so no marketplace can enforce the guarantee it advertises."

**Patch status**, quoted directly from air.security's disclosure:

| Agent (vendor) | Status |
|---|---|
| **Claude Code** (Anthropic) | "Anthropic patched it after our disclosure, in 2.1.179." |
| **Codex** (OpenAI) | "OpenAI patched it after our disclosure, in 0.146.0." |
| **GitHub Copilot** (Microsoft) | "we disclosed the same flaw to Microsoft, which has not shipped a fix, so users have no patch." |
| **Gemini CLI** (Google) | "Google has deprecated the Gemini CLI and will not patch it, so every install stays vulnerable for good; those users should migrate to Antigravity, which this attack does not reach - it has no marketplace plugin SHA pinning to bypass." |

**Hype-vs-reality — "doing the right thing does not protect you":** the source's central framing point is that this isn't a careless-install problem. Org-level mitigation — reviewing a plugin and pinning it to the reviewed commit, the standard enterprise control for supply-chain risk in plugin ecosystems — is defeated too: "review passes, the pin is written, and different code installs." Per the source, "the victim only has to have a plugin installed, from a marketplace they trust, that was reviewed and pinned exactly as the security model intends... Every downstream vetting process built on pinning inherits the failure." A marketplace-side mitigation (reject SHA-shaped branch names) is also incomplete — it "bans hosts the agents officially support, and does nothing for Gemini CLI's variant."

**Relationship to GitSpawn (above):** a distinct vulnerability class, not a restatement. GitSpawn is local git-config poisoning — a repo-supplied `core.fsmonitor` command firing during background `git status`/`git diff` calls before any trust prompt. Plugin4Shell attacks a different layer entirely: the plugin-marketplace **distribution/trust boundary**, via git's ref-vs-object-id resolution ambiguity at checkout time, not local config. The source itself frames this as attacking "the distribution layer... the marketplaces through which agent add-ons reach millions of machines," explicitly distinct from prior work "targeted [at] the model or the agent itself." Same broader narrative (agent supply-chain trust boundaries keep failing), different mechanism and different sink.

**Source:** air.security, "Plugin4Shell" (2026-09-17), third in the "Story of Skills → SkillJacking → Plugin4Shell" series. Captured `raw/research/weekly-2026-09-23/05-05-plugin4shell-rce.md`.

## Possible overlap with the Shai-Hulud / ChainDrop supply-chain thread

The same Black Hat window surfaced a separate Pillar Security report (also dated 2026-08-04) describing a "ChainDrop" npm worm planting a Claude Code `SessionStart` hook and a `.vscode/tasks.json` `folderOpen` task in **compromised repos**, firing when a developer opens the workspace — not on `npm install`. This targets the identical payload files (`.claude/settings.json` SessionStart hook, `.vscode/tasks.json` folderOpen) as the wiki's existing [[mcp-rce-supply-chain-2026-05]] "Shai-Hulud Wave Six" entry (Wiz-attributed, npm-install-triggered, same date). Whether these are the same campaign reported under two names by two firms, or two distinct campaigns using the same technique, is **unresolved** — flagged for practitioner validation rather than merged.

## Hype-vs-reality

This is a practitioner-verified (CVE/CVSS-backed, reproducible) disclosure, not vendor marketing — one of the stronger signal classes this wiki tracks. The vendor-posture split (Anthropic/Google issue CVEs, OpenAI does not) is itself a data point for any AI-coding-agent CI security review: don't assume "no CVE" means "no risk."

## Related

- [[mcp-rce-supply-chain-2026-05]]
- [[agent-safety-incidents-2026-08]]
- [[../llms/anthropic-claude-family|anthropic-claude-family]]
- [[../llms/openai|openai]]
- [[../llms/xai-grok-family|xai-grok-family]] — Grok Build unpatched GitSpawn finding
- [[../startups/cursor|cursor]] — Cursor affected, patched
- [[../platforms/microsoft|microsoft]] — GitHub Copilot affected by Plugin4Shell, unpatched
- [[ai-infrastructure-frontiers-2026]]
