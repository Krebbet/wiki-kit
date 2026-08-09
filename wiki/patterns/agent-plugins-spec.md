# Agent Plugins Specification v1.0.0

Agent Plugins v1.0.0 is a vendor-neutral, filesystem-directory packaging format that lets one plugin package — a `plugin.json` manifest, an optional `skills/` folder of Agent Skills, and an optional `mcp.json` MCP-server config — be installed across multiple AI-agent clients without per-client rewrites. It sits above both MCP and the separate Agent Skills specification as a thin, cross-cutting packaging envelope, deferring the actual protocol/format details to those two specs rather than redefining them. The captured spec text (agentplugins/agent-plugins-spec on GitHub) marks itself `Status: Published` — a finished v1.0.0 normative document with a companion conformance checklist, not a working draft.

## Package model

A plugin is a directory, not an archive — chosen explicitly so it stays inspectable with `ls`/`cat`/`git`, editable in place, and compatible with version control. Canonical layout:

```
my-plugin/
├── plugin.json          # required manifest, closed schema
├── skills/
│   └── summarize/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── mcp.json             # MCP server config, closed schema
├── com.example.client/  # client extension directory (reverse-domain namespaced)
├── LICENSE
└── CHANGELOG.md
```

`plugin.json`'s only permitted top-level fields are `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions`. Unknown fields are reported and ignored (non-fatal); any other schema violation is fatal and rejects the whole plugin. Component locations are fixed (`skills/`, `mcp.json`) and cannot be overridden or declared inline in the manifest — the spec's own design-decisions appendix frames this as eliminating "discovery indirection, alternate-source precedence, and manifest configuration every client would otherwise need to implement."

The problem this solves is build-once-run-across-clients: a single plugin directory is meant to be loadable by any conformant client instead of authors writing a separate integration per tool. The spec itself is written client-agnostically and does not name specific client products in-text. Component-level failure isolation is a stated design goal — an invalid skill or an unreachable MCP server must not take down the rest of the plugin.

## Relation to MCP and Agent Skills

Agent Plugins does not redefine MCP wire behavior or lifecycle; it explicitly defers to the Model Context Protocol specification for that, and only defines the **portable `mcp.json` discovery/config format** used to locate and connect to MCP servers bundled with a plugin. Clients map this portable shape onto their own native MCP config — field names need not match. The transport union is closed: `stdio` (bare or plugin-relative executable, launched with `PLUGIN_ROOT`/`PLUGIN_DATA` environment variables and `${PLUGIN_ROOT}`/`${PLUGIN_DATA}` placeholder expansion), `streamable-http` (the current transport), and an optional/deprecated `sse` (2024-11-05 HTTP+SSE) form. A conformant client must support at least stdio or streamable-http.

Similarly, the spec's Agent Skills integration is scoped narrowly: it only defines how a plugin's `skills/` folder is scanned (one level deep, directories containing `SKILL.md`) — the actual `SKILL.md` format and frontmatter is delegated entirely to the separate Agent Skills specification (see [[patterns/agent-skills]]). Agent Plugins is therefore a thin envelope over two independently-specified formats, not a replacement for either.

## Explicitly stated current limitations (v1, future work)

- **No permission/authorization model.** "Agent Plugins v1 defines no OAuth configuration or portable credential-reference fields. Authorization discovery, user interaction, and credential storage are client-managed."
- **No secrets mechanism.** Both MCP `headers` and `env` values are explicitly called "visible package data, not a portable secret mechanism" — plugins must not embed credentials or secrets in either. Secret handling is left entirely to clients.
- **No signature checks or sandboxing beyond path containment.** The only defined security primitive is filesystem path-containment (resolved paths must stay within the plugin root, or within `PLUGIN_DATA` for a configured working directory) — no code-signing, provenance, or subprocess sandboxing is defined in-spec.
- **Only two component types in v1: skills and MCP servers.** The design-decisions appendix defers "commands, hooks, agents, rules, and LSP servers" as "too client-specific for a stable portable contract" until their formats converge across clients.
- **No fallback-transport behavior.** If a declared MCP transport's initial connection attempt fails, the spec does not define fallback behavior.

## Framing caveats

Press coverage widely attributed Agent Plugins to a named coalition (OpenAI, AWS, Cursor/Anysphere, GitHub, Microsoft, Vercel), and this is plausibly accurate from the standard's announcement — but the captured spec document itself names no companies; it references governance living in a separate Technical Charter (`GOVERNANCE.md`) and speaks generically of "clients" throughout. Treat the co-developer list as collect-but-confirm from press sources, not something this spec document itself substantiates.

## Source
- Agent Plugins Specification v1.0.0, `spec/1.0.0.md` — https://github.com/agentplugins/agent-plugins-spec, captured 2026-08-09 — `raw/research/weekly-2026-08-09/02-openai-agent-plugins-spec.md`. Primary technical spec document.

## Related
- [[mcp-infrastructure]] — Agent Plugins layers a portable per-plugin `mcp.json` config and `PLUGIN_ROOT`/`PLUGIN_DATA` subprocess-env convention on top of raw MCP; the explicit non-solution of auth/governance here parallels that page's coverage of MCP's unresolved governance gap.
- [[mcp-multi-agent-framework]] — that page's server-pattern taxonomy sits one layer below this one; Agent Plugins is a packaging/distribution envelope that could carry servers built to those patterns.
- [[patterns/agent-skills]] — Agent Plugins' `skills/` discovery mechanism explicitly delegates format authority to the Agent Skills specification; extends that page with a "how skills get distributed and installed across clients" dimension it doesn't currently cover.
- [[governance/aaif]] — both are cross-vendor, standards-body-flavored interoperability efforts (AAIF stewards MCP and AGENTS.md under the Linux Foundation); whether Agent Plugins' separate Technical Charter is affiliated with or independent of AAIF is an open question this spec doesn't answer.
- [[patterns/agents-md]] — a sibling portable, vendor-neutral standardization effort (project context, rather than component packaging); worth treating as part of the same "portable agent standards" cluster.
- [[evaluation/continualskillbench]] — Agent Plugins' `skills/` distribution format assumes human-authored, well-designed skills as the unit of value; ContinualSkillBench's finding that autonomous, agent-driven skill creation underdelivers relative to that ideal is a relevant caution for anyone building a plugin ecosystem around agent-authored skills.
