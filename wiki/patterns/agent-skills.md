# Agent Skills (authoring & mechanics)

The wiki's authoritative reference for **Agent Skills** — the Anthropic-defined unit of packaged procedural expertise — synthesised from three vendor primary sources: the engineering blog ("Equipping agents for the real world with Agent Skills"), the official "Skill authoring best practices" docs, and "The Complete Guide to Building Skills for Claude", plus a dedicated section on the Claude Code-specific implementation from the Claude Code Skills docs. A Skill is a directory whose entry point is a `SKILL.md` file (YAML frontmatter + Markdown body), optionally bundling reference files and executable scripts. The load-bearing design idea is **three-level progressive disclosure**, and the load-bearing authoring discipline is **evaluation-first iteration under a strict token-cost budget**. Skills are referenced derivatively across [[skillos]], [[externalization-survey]], [[../deployments/anthropic-finance-agents]] and [[../deployments/openai-symphony]]; this is the page they anchor to. *(Quantitative figures in the Complete Guide are self-described by Anthropic as "aspirational / vibes-based"; treated here as collect-but-confirm per the wiki's source-authority weighting.)*

## What a Skill is

A Skill = a folder containing:
- `SKILL.md` (**required**, exact case-sensitive filename) — YAML frontmatter + Markdown body. Folder name must be kebab-case (no spaces/underscores/capitals). **No `README.md` inside the skill folder** (a repo-level README for humans is separate).
- optional `scripts/` (executed, not loaded into context), `references/` / `reference.md` / `FORMS.md` / `examples.md` (loaded on demand), `assets/`.

Three core design principles stated by the Complete Guide:
1. **Progressive disclosure** — see below; the central mechanism.
2. **Composability** — a Skill must co-exist with other Skills, never assume it is the sole capability.
3. **Portability** — the same Skill works unmodified across Claude.ai, Claude Code, the Claude Agent SDK, and the Developer Platform (environment permitting). Published as an open cross-platform standard on **2026-12-18** (agentskills.io / "open standard like MCP").

**Framing:** building a Skill is "like putting together an onboarding guide for a new hire" — capturing and sharing procedural knowledge so anyone can specialise agents with composable capabilities instead of building fragmented custom agents per use case. **MCP-vs-Skills** ("kitchen analogy"): MCP is the kitchen (connectivity — *what* the agent can do); Skills are the recipes (knowledge — *how* it should do it). They complement rather than replace each other.

## Three-level progressive disclosure (the core mechanism)

| Level | What loads | Cost |
|---|---|---|
| **1 — metadata** | At startup only `name` + `description` of every installed Skill is pre-loaded into the system prompt — just enough for the model to know *when* to use the Skill | Always in context (small) |
| **2 — SKILL.md body** | When the model judges the Skill relevant, it reads the full `SKILL.md` body | Loaded on relevance |
| **3 — bundled files** | Additional files referenced by name from `SKILL.md` (e.g. `reference.md`, `forms.md`), navigated/read via the filesystem only as needed | Zero tokens until loaded |

Because agents have filesystem + code execution, the bundled context is "effectively unbounded" — the whole Skill need not enter the context window. Analogy: table of contents → chapters → appendix. This is the same load-bearing mechanism [[sierra-context-engineering]] names across its eight context-block types and that [[../case-studies/notion-token-town]] applies to 100+ tools; [[codified-context]]'s three-tier hot/cold KB is an independent hand-engineered realisation.

## What works — authoring best practices

**Frontmatter (the most important part).** Exactly two required fields:
- `name` — ≤64 chars, lowercase letters/numbers/hyphens, no XML tags, no reserved words ("claude"/"anthropic" reserved).
- `description` — ≤1024 chars, non-empty, **no `< >` angle brackets** (system-prompt injection risk).

**`description` is the single most important discovery lever.** The model uses it to choose the right Skill among potentially 100+; it must state **both what the Skill does AND when to use it** (specific triggers, contexts, key terms), written in **third person** (it is injected into the system prompt; mixed point-of-view causes discovery failures). Avoid vague descriptions ("Helps with documents", "Processes data").

**Naming.** Prefer **gerund form** (verb+-ing): `processing-pdfs`, `analyzing-spreadsheets`, `testing-code`. Avoid generic names (`helper`, `utils`, `tools`, `data`).

**Conciseness / token-cost discipline.** "The context window is a public good." Default assumption: **the model is already very smart — only add context it doesn't already have.** Not every token costs immediately (metadata pre-loaded, SKILL.md lazy-loaded), **but once SKILL.md is loaded every token competes with conversation history** — a recurring per-turn cost. Keep the body **under 500 lines** (Complete Guide: SKILL.md <5,000 words); split beyond that into `references/`. Keep references **one level deep from SKILL.md** (deeper nesting causes partial `head -100` reads → incomplete info); reference files >100 lines should carry a table-of-contents header. Organise multi-domain Skills by domain so irrelevant context never loads; separate mutually-exclusive paths (creation vs editing). Provide one default approach with an escape hatch rather than many choices; avoid time-sensitive content (collapse into an "Old patterns" section); keep terminology consistent.

**Specificity / freedom levels.** Match instruction specificity to task fragility: high freedom = text guidance; medium = pseudocode/parameterised scripts; low = exact scripts ("do not modify the command"). Skills are model-dependent — test across all target models (Haiku may need more detail than Opus). This freedom axis is the same lever [[skill-distillation]] formalises with its Metric-Freedom predictor.

**Code-as-tools.** Pre-made utility scripts beat token generation for deterministic work (sorting, form-field extraction): more reliable, cheaper, and they execute *without* loading contents into context. Explicitly state whether the model should *execute* a script vs *read it as reference*. Scripts should handle errors explicitly (don't punt to the model), document config constants (no magic numbers — Ousterhout's law), declare dependencies, use forward slashes, fully qualify MCP tools (`ServerName:tool_name`). **Plan-validate-execute** pattern for batch/destructive/high-stakes ops: analyse → write a plan file → validate the plan with a script → execute → verify, with verbose validator error messages. The "run validator → fix → repeat" loop works with a script *or* a reference doc as the "validator".

**Evaluation-first iteration loop.** Create evaluations **before** writing extensive documentation — evaluations are the source of truth for effectiveness (JSON rubric: skills/query/files/expected_behavior; no built-in runner). Development uses two model instances: **Claude A** designs/refines the Skill (the model's native understanding of the Skill format means no special "skill-writing skill" is needed); **Claude B** is a fresh instance with the Skill loaded, tested on *real workflows, not test scenarios*. The most effective skill-creators iterate on a *single challenging task* until the model succeeds, then extract the winning approach into a Skill (leverages in-context learning, faster signal than broad testing) — this is the practitioner-facing version of the [[skill-distillation]] collapse move. Iterate on observation, not assumptions.

## What doesn't work — anti-patterns

From the Complete Guide's troubleshooting catalogue:
- **Instructions not followed** — usually too verbose, buried, or ambiguous. Put critical instructions at the top, use `## Important` / `## Critical`, and prefer a bundled validation *script* over prose because "code is deterministic; language interpretation isn't."
- **Skill won't trigger** — vague `description`; debug by asking the model "When would you use the X skill?" then revise.
- **Triggers too often** — add negative triggers, narrow scope.
- **Large-context degradation** — keep SKILL.md small, move detail to `references/`, reduce enabled Skills if >20–50, consider Skill "packs".
- **Tool-first framing** — frame around the problem, not the tool inventory ("Home Depot" anti-pattern).

Five named composition patterns: sequential workflow orchestration; multi-MCP coordination; iterative refinement; context-aware tool selection (decision tree); domain-specific intelligence (compliance-before-action).

## Claude Code-specific mechanics

The Claude Code Skills docs add harness-specific behaviour on top of the open standard. *(Source captured via lossy URL scrape — field names and structural facts below are reliable; prose was not quoted.)*

**Where Skills live** (precedence: a Skill beats a legacy command on name clash):
- Personal: `~/.claude/skills/<name>/SKILL.md` (all projects, current user).
- Project: `.claude/skills/<name>/SKILL.md` (committed, repo-scoped; requires workspace-trust before `allowed-tools` activates).
- Plugin: `<plugin>/skills/<name>/SKILL.md` (namespaced `plugin-name:skill-name`, cannot conflict).
- Enterprise/managed: deployed org-wide via managed settings.
- Legacy `.claude/commands/*.md` still work and share the same frontmatter; Skills win on collision (custom commands have been merged into Skills).

**Discovery / loading.** Live change detection: edits under watched skill dirs take effect mid-session; a *newly created* top-level skills dir needs a restart. Project Skills load from `.claude/skills/` in the start dir and every parent up to repo root; nested `.claude/skills/` discovered on demand (monorepo support). `--add-dir`'s `.claude/skills/` IS auto-loaded (other `.claude/` config is not). In a normal session only Skill *descriptions* enter context; the body loads on invocation.

**Frontmatter schema (Claude Code superset):** `name`, `description` (combined with `when_to_use`, truncated at 1,536 chars in listing — cap configurable via `maxSkillDescriptionChars`), `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context: fork`, `agent`, `hooks`, `paths`, `shell`.

**Invocation model.** Default = both user (`/skill-name`) and model (auto via description match). `disable-model-invocation: true` → user-only. `user-invocable: false` → model-only, hidden from the `/` menu (visibility only — does not block Skill-tool access). `skillOverrides` settings can override frontmatter without editing SKILL.md.

**Permissions.** `allowed-tools` pre-approves listed tools while the Skill is active (it does not restrict — unlisted tools still follow baseline permission settings). Project-skill `allowed-tools` activates only after workspace trust.

**Claude-Code-only extensions over the open standard:**
- **Dynamic context injection** — `` !`<command>` `` (and fenced `!` blocks) run *before* the model sees content; output replaces the placeholder. Disable org-wide via `disableSkillShellExecution: true`.
- **Subagent execution** — `context: fork` makes SKILL.md the subagent prompt; the `agent` field picks the agent type. No conversation-history access; loads CLAUDE.md. (This is a deliberate handoff — the inverse of the [[skill-distillation]] "eliminate the handoff" move.)
- **Bundled prompt-based Skills shipped every session:** `/simplify`, `/batch`, `/debug`, `/loop`, `/claude-api` (plus `/init`, `/review`, `/security-review` via the Skill tool).
- **String substitutions:** `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`.

**Lifecycle / token budget (distinctive).** An invoked SKILL.md enters the conversation as one message and persists for the session; the file is **not re-read on later turns** — write standing instructions, not one-time steps. Auto-compaction re-attaches the most recent invocation of each Skill (first 5,000 tokens each, 25,000-token combined budget filled most-recent-first — older Skills can be dropped). Skill-listing budget = 1% of the model context window (tunable). The "skill body costs nothing until used" framing is contrasted in the docs against always-on CLAUDE.md and the `/remember` → `CLAUDE.local.md` path ([[../memory/claude-code-session-memory]]).

## Relationship to the AGENTS.md-effectiveness conflict

The vendor claim that well-authored Skills reliably improve agent performance sits against [[../evaluation/agents-md-eval]]'s finding that LLM-generated context files reduced coding-agent success ~3% and inflated cost >20% in well-documented Python repos. This is **not a new conflict** — it is a data point on the existing open [[../conflicts/agents-md-effectiveness]]. Skills land on the *favorable* side of that conflict's regime axis: they are human/Claude-A-authored (not LLM-auto-generated flat context), progressively disclosed (not always-on), evaluation-tested, and code-bearing. The Complete Guide's own anti-bloat guidance (<5,000 words, `references/` offloading, "only add context the model doesn't have") is itself a candidate *reconciling lever* for that conflict. See the conflict page's 2026-05-15 data-point section.

## Source

- `raw/research/agentic-skills-personalities/01-01-anthropic-equipping-agents.md` (https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- `raw/research/agentic-skills-personalities/02-02-skill-authoring-best-practices.md` (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- `raw/research/agentic-skills-personalities/03-03-claude-code-skills.md` (https://code.claude.com/docs/en/skills — lossy URL scrape; field names/structure reliable, prose not quoted)
- `raw/research/agentic-skills-personalities/04-04-complete-guide-building-skills.md` (https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf — quantitative figures self-described as aspirational; collect-but-confirm)

## Related

- [[skillos]] — RL-trained Markdown-skill curator; the *policy-learned* counterpart to this page's *human/Claude-A authoring* of the same skill-as-Markdown abstraction.
- [[skill-distillation]] — the "iterate on one hard task, then extract" methodology here is the practitioner-facing version of its Metric-Freedom collapse predictor.
- [[externalization-survey]] — Skills are one of the four externalizations (memory + skills + protocols + harness); this is the canonical vendor instantiation of the skills axis.
- [[sierra-context-engineering]] — progressive disclosure as the shared load-bearing context mechanism; eight context-block types are the productionised superset.
- [[codified-context]] — hand-engineered three-tier hot/cold KB; an independent realisation of lean-core + load-on-demand.
- [[effective-harnesses]] / [[harness-design-space]] / [[agentic-harness-engineering]] — Skills are a first-class harness-construction primitive; the validator-loop / plan-validate-execute advice echoes harness-engineering posture.
- [[../deployments/anthropic-finance-agents]] — vertical agents packaged as "skills + connectors + subagents"; this is the underlying skill-authoring spec.
- [[../deployments/openai-symphony]] / [[../case-studies/notion-token-town]] — competing/parallel production instances of skills + progressive disclosure.
- [[../memory/claude-code-session-memory]] — same-harness sibling; the skill-body-vs-always-on-CLAUDE.md contrast.
- [[../conflicts/agents-md-effectiveness]] — Skills are a 2026-05-15 data point on the favorable-regime side of this open conflict.
- [[agent-personas]] — the personality counterpart: how (and whether) to give an agent a persona, with the empirical evidence.
