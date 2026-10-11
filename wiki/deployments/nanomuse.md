# nanoMuse — Open Personal Agent with Per-Device Sentinel Governance

nanoMuse (arXiv 2610.08699, Liu, Liu and Zhang of Zhejiang University, 2026-10-06; GPL-3.0; https://github.com/nano-muse/nanoMuse) is an open-source "personal agent" that runs as a whole agent on every device a user owns (Android, desktop, web, iOS without screen control), with a shared conversation, readable file-based memory and a deterministic action gate called Sentinel. The paper is a project report that also reverse-engineers Meta's Muse personal agent. **Evidence tier: single academic group, self-reported, no task benchmarks. Collect-but-confirm.** The Muse section rests on public docs plus an unverified copy of Muse's production prompt and is secondary.

## Architecture (project-stated)

- **Per-device agents:** each device is a complete agent with its own Sentinel. Devices are peers that meet through an optional open-source relay (SQLite hub, one Python process, about 85 MB RAM idle). Each agent has the others as tools, so a cross-device task is one conversation. A delegated job runs under the receiving device's own Sentinel, so a device cannot lend permissions it lacks.
- **Shared conversation:** text is synced only if the user opts in; files, images and tool outputs are not synced.
- **Lineage:** the Android app is a modified OpenMinis (Alpine sandbox, shell, MCP, skills, scheduled tasks, any OpenAI-compatible model). Desktop is an Electron shell around the DeepSeek harness. Computer-side screen control is ported from UI-TARS-desktop. Version 0.1.40, first release 2026-09-25. No model is released; an open screen-control model is roadmap.
- **Hands ladder:** skill, CLI or MCP first, then a fetched page with login, then a browser, and last the device screen ("Hands", off by default). The screenshot loop emits one thought-sentence plus one gesture.
- **Costs (self-reported):** Android app 38 MB; desktop 256-498 MB download; self-hosted relay about US$4-6/month plus model usage.

## Readable memory

Memory is plain files. The phone uses Markdown (SOUL.md, USER.md, GLOBAL.md, a dated diary, HEARTBEAT.md) that the user and the agent shell can both read. The computer store keeps lines with a change log and undo, keyword or embedding recall, and a tidy-up pass that never drops user-written lines. The authors argue user-written lines should outrank model-written ones. The Muse analysis notes Muse's three agent-kept files reuse the file names used by [[memory/openclaw]].

**Stated open gap:** memory has no provenance (writing model, date, confidence per line) and no re-check rule. See [[security/memory-poisoning-mpbench]] for why write-time trust matters.

## Sentinel action governance

The agent never executes a tool directly; every call passes a fixed decision order: denied tools, user rules, always-allow/ask lists, taint, tool risk against user mode, then non-waivable warnings (destructive shell, piped download-and-execute, committing actions).

- **Taint rule:** once private data has been read, any send outside the allow-list becomes an ask, never the reverse.
- **Scoped grants:** once, this conversation, or always for a named recipient, site, folder, device or app. Grants are listed with revoke, and all decisions are logged. Warned calls get "once" only, so payments and passwords are never remembered.
- **Screen actions:** the policy judges the model's stated sentence (words like confirm payment, send, delete force per-step approval) and also reads Android accessibility text under the tap; the stricter wins. Typing passwords, PINs and OTPs is forbidden by prompt only.
- **Concession by the authors:** Sentinel runs in the same trust domain as the agent, so it is a policy boundary, not a privilege boundary. A compromised device means a compromised agent. This is weaker than the out-of-agent boundary they attribute to Muse. Icon-only buttons are not covered by the label or accessibility checks.
- **No success rate or human take-over count** exists for the screen-control path (the authors say so explicitly). Planned evals: AndroidWorld, OSWorld, MemGUI-Bench, OS-Harm.

Compare the classifier-gated approach in [[governance/claude-code-auto-mode]] and the open question in [[conflicts/auto-mode-prompt-injection-defense]].

## Muse reverse-engineering (secondary, prompt-copy-derived)

Source-tag: everything here is the nanoMuse authors' reconstruction from public docs and an unverifiable prompt copy (their own tags: documented, prompt, observed, inferred). Treat as collect-but-confirm; nothing was confirmed by Meta.

- Per-person Linux VM in Meta's cloud, container with seccomp.
- Sentinel is reportedly "the sole permission authority" for connector actions and all egress, with surrogate credential tokens swapped at the network boundary and kernel-level taint tracking per tool process.
- Layered injection defense: training, a classifier ensemble, then deterministic boundaries meant to hold "even if Muse is persuaded". The authors' reading: probabilistic layers reduce how often persuasion works, deterministic layers bound what a persuaded agent can do.
- Browser sub-agent sees the accessibility tree only and is paused during credential entry; a checkout detector exists. Muse cannot operate native phone apps.
- Memory in two layers (curated files plus a runtime memory bank); the prompt tells the agent to search memory rather than trust recall and to show provenance on request.

## Market context (project-stated)

The paper lists Muse (Sep 8), CopilotKit's OpenMuse (Sep 15, MIT), nanoMuse (Sep 25), Manus Cue (Sep 28), OpenAI dots (Sep 29, see [[deployments/openai-dots]]) and the Meta gadget SDK (Oct 2) as one converging wave. Muse is a different Meta surface from [[coding-agents/meta-muse-code]].

## Source

- `raw/research/weekly-2026-10-11/05-nanomuse.md` — Liu, Liu, Zhang, "nanoMuse: An Open-Source Personal Agent for Every Device You Own", arXiv 2610.08699, 2026-10-06
- https://arxiv.org/abs/2610.08699

## Related

- [[coding-agents/meta-muse-code]]
- [[deployments/openai-dots]]
- [[memory/openclaw]]
- [[memory/openclaw-claude-code-memory]]
- [[security/memory-poisoning-mpbench]]
- [[governance/claude-code-auto-mode]]
- [[conflicts/auto-mode-prompt-injection-defense]]
