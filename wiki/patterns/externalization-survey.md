# Externalization in LLM Agents (Zhou et al., arXiv 2604.08224)

22-author SJTU/SYSU/CMU/OPPO survey (Chenyu Zhou, Huacan Chai, et al., April 2026) reframing the entire 2024–2026 agent stack through a single transition logic — **externalization** — arguing that capability has migrated from **weights → context → harness**, with memory, skills, and protocols as three coupled forms of externalised cognition unified by the harness as a "cognitive environment." The survey provides a *cross-cutting vocabulary* that touches at least five existing wiki clusters; this page is the anchor for that vocabulary, with sub-section pointers from each cluster.

## Source

- `raw/research/weekly-2026-05-04/05-externalization-survey.md` — captured 2026-05-04 from `https://arxiv.org/pdf/2604.08224` via marker on CPU.

## The four-externalization taxonomy

The survey's load-bearing organising frame:

- **Memory** externalises **state across time** (recall → retrieval).
- **Skills** externalises **procedural expertise** (generation → composition).
- **Protocols** externalises **interaction structure** (ad-hoc → structured contract).
- **Harness** is the **unification layer / cognitive environment** — explicitly *not* a fourth externalization, but the runtime within which the other three operate.

The Norman cognitive-artifacts framing — *"the artifact does not change capabilities, it changes the task"* — is the load-bearing theoretical anchor, with Kirsh's "complementary strategies" and Hutchins's distributed cognition as supporting frames.

## Weights → context → harness historical progression (§2)

Capability was first identified with **model parameters** (GPT-4/Gemini era), then with **prompt + RAG + ReAct + chain-of-thought**, and is now treated as a property of the **broader infrastructure** (Auto-GPT/BabyAGI → AutoGen/MetaGPT/CAMEL/Reflexion → Codex/Claude Code/SWE-agent/OpenHands/Voyager/LangGraph). The survey's distinguishing claim vs prior surveys: this is a *single externalization arc*, not three independent technical histories.

## Memory chapter (§3)

Uses **Du 2026's four-paradigm taxonomy**: monolithic context → context+retrieval → hierarchical memory & orchestration (Mem0, MemGPT, MemoryOS, MemoryBank, MIRIX, MemOS, xMemory) → adaptive memory systems (MemEvolve, MemVerse, MemRL, GAM).

Decomposes externalised state into four content types — *working context*, *episodic experience*, *semantic knowledge*, *personalised memory* — more granular than the wiki's existing three-axis taxonomy in [[memory-architectures]] but maps cleanly onto it.

## Skills chapter (§4)

The chapter with the **least prior wiki coverage**.

- **Three-stage progression**: atomic execution primitives → large-scale primitive selection → skill as packaged expertise.
- **Three-component decomposition** of procedural expertise: operational procedure + decision heuristics + normative constraints.
- **Five-step externalisation pipeline**: specification → discovery → progressive disclosure → execution binding → composition.
- **Four acquisition pathways**: authored / distilled / discovered / composed.
- **Boundary conditions named**: semantic alignment, portability and staleness, unsafe composition, context-dependent degradation.

Cites Anthropic's "Introducing Agent Skills" (Oct 2025) and Claude Code's progressive-disclosure skill system as the canonical industrial implementation.

## Protocols chapter (§5)

Decomposes externalised interaction into **invocation grammar / lifecycle semantics / permission and trust boundaries / discovery metadata**, then surveys:

- **Agent-tool**: MCP, ToolUniverse.
- **Agent-agent**: A2A, ACP, ANP.
- **Agent-user**: A2UI, AG-UI.
- **Domain protocols**: UCP for commerce, AP2 for payments.

MCP is treated as the canonical agent-tool externalization; A2A as the canonical agent-agent externalization. Aligns one-to-one with [[mcp-infrastructure]] and [[mcp-multi-agent-framework]] but is more taxonomic than empirical.

## Harness chapter (§6) — six analytical dimensions

1. Agent loop & control flow
2. Sandboxing & execution isolation
3. Human oversight & approval gates
4. Observability & structured feedback
5. Configuration / permissions / policy encoding
6. Context budget management

Explicitly cites **OpenAI Codex and Anthropic Claude Code as convergent implementations** — *"the convergence is analytically significant: it suggests that the six dimensions are not incidental implementation choices but structural requirements of externalized agency."*

## Cross-cutting analysis (§7) — six pairwise module flows

- **memory→skill** (experience distillation, e.g. TED, UMEM, Voyager)
- **skill→memory** (execution recording, e.g. SWE-Exp)
- **skill→protocol** (capability invocation, with the "Lethal Trifecta" safety motif)
- **protocol→skill** (capability generation, e.g. HashiCorp Agent Skills)
- **memory→protocol** (strategy selection — multi-agent routing between MCP and A2A informed by historical success rates)
- **protocol→memory** (result assimilation)

Treats the cycle as both **self-reinforcing** and **capable of error cascades** — a poisoned memory entry can yield a flawed skill whose execution traces further contaminate memory.

## The LLM I/O perspective (§7.2)

Decomposes the model boundary into three layers with distinct update rates and failure taxonomies: **memory as contextual input, skills as instructional input, protocols as action schema**. Presented as a "structured form of context engineering" — direct connector to [[context-engineering]].

## Three durable tradeoffs (§7.3 + §8)

1. **Parametric vs externalized capability** — partition by update frequency, reusability, auditability/governance, and latency/context burden; high-stakes deployment pushes the boundary outward.
2. **Evaluation challenges** — current benchmarks (task-completion under fixed prompt/model) systematically *under-measure* the harness contribution; the survey proposes new dimensions: **transferability under model swap, maintainability, recovery robustness, context efficiency, governance quality**.
3. **Governance and security** — memory poisoning, malicious skill injection, protocol spoofing each map directly onto one externalization dimension; governance must be *co-designed*, not bolted on.

## Two named emerging directions (§8)

- **§8.3 — "self-evolving harnesses"** — adaptive harnesses that revise their own memory policies, skill artifacts, and execution logic via RL / program synthesis / evolutionary search / imitation learning across module / system / boundary levels. *(This is exactly what [[agentic-harness-engineering]] (arXiv 2604.25850) operationalises — captured the same week.)*
- **§8.5 — "shared infrastructure"** — the shift from agent-private scaffolding to ecosystem-scale shared memory, shared skills (HashiCorp Agent Skills cited), and shared protocols. The unit of analysis moves from *individual agent* to *ecosystem*.

Two further future directions worth flagging:

- **§8.2 embodied externalization** — the cerebrum/cerebellum split in robotics (high-level LLM as planner, VLA models as callable atomic skill modules) recapitulates digital-agent externalization.
- **§8.1 multi-modal externalization** — multi-modal skills (CUA-skill), multi-modal memory (MemVerse, MuSEAgent), multi-modal reasoning distillation (TED).

## What the survey cites that the wiki already covers

Anthropic MCP (2024), Claude Code skills system (Oct 2025), Claude Code 2026 docs, MemGPT (Packer et al. 2023), Mem0 (Chhikara et al. 2025), Reflexion (Shinn et al. 2023), Voyager (Wang et al. 2023a), Generative Agents (Park et al. 2023), CoALA (Sumers et al. 2024), RAG (Lewis et al. 2020), AutoGen (Wu et al. 2023), MetaGPT (Hong et al. 2023), CAMEL (Li et al. 2023), Self-Refine (Madaan et al. 2023), ReAct (Yao et al. 2023a), Toolformer (Schick et al. 2023).

The survey does **not** cite Anthropic's "Effective harnesses for long-running agents" post nor Cognition's cloud-agents work specifically — both are implicit instances of the harness convergence the survey describes but neither appears in the bibliography (publication-lag effect).

## Caveats the survey self-documents

- The harness concept is *"still consolidating"* — the six-dimension characterisation is *"best understood as a synthesis of recurring patterns in current systems rather than a closed definition."*
- Cognitive-artifact interpretations in §3.4, §4.7, §5.4, §6.4 are flagged as *"primarily theoretical rather than directly empirical."*
- Embodied externalization extension is argument by analogy, not measurement.
- Coverage primarily through 2025 Q4 / early 2026 (latest cited works are arXiv 2603 and 2604 preprints).
- **No original empirical evaluation** — this is a literature synthesis.
- Bibliography is heavy on SJTU and Chinese-academy work, light on independent OSS / European / industry-research labs.

## Why this page exists alongside [[memory-architectures]]

The four-externalization taxonomy (memory + skills + protocols + harness) is genuinely cross-cutting in a way `memory-architectures` alone is not. The survey touches: memory (`memory-architectures` + 9 memory subpages), patterns (`effective-harnesses`, `skill-distillation`, `codified-context`, `context-folding`, `agentic-context-engineering`, `mcp-multi-agent-framework`, `agentic-harness-engineering`), deployments (`mcp-infrastructure`, `cognition-cloud-agents`, `microsoft-agent-365`, `openai-symphony`), coding-agents (`langchain-deep-agents`), case-studies (`anthropic-internal-study`, `willison-cognitive-cost`, `notion-token-town`).

The skills chapter is particularly underrepresented in the existing wiki: [[skill-distillation]] argues for *eliminating* skills via collapse (the Metric Freedom F predictor), but no page currently surveys *what skills are and how they work as externalised artifacts*. The §6 harness chapter's six-dimension framework is also a new analytical vocabulary not present in the wiki. *(2026-05-11 update: [[skillos]] now provides a concrete RL operationalisation of §4 — frozen executor + RL-trained Markdown-skill curator with grouped-task downstream rewards.)*

## Related

- [[memory-architectures]] — closest peer survey; bidirectional cross-reference.
- [[effective-harnesses]] — concrete instance of the §6 six-dimension harness framework.
- [[agentic-harness-engineering]] — operationalises §8.3 "self-evolving harnesses" emerging direction.
- [[skillos]] — operationalises both §4 (skills externalization) and §8.3 (self-evolving harnesses) via RL on Markdown skill curation. The clearest 2026 instance of the survey's "skills as procedural-expertise externalization."
- [[agent-development-lifecycle]] — process-lens (Build → Test → Deploy → Monitor) on the same substance the survey covers structurally; both arrive at memory + skills + protocols + harness as the load-bearing externalisations.
- [[agent-skills]] — the canonical vendor instantiation of the §4 skills externalization axis (authoring mechanics + progressive disclosure).
- [[agent-personas]] — persona-via-system-prompt as a context-layer externalization; PRISM moves it into weights via gated self-distillation.
- [[mcp-infrastructure]], [[mcp-multi-agent-framework]] — protocols-as-externalization (§5).
- [[skill-distillation]] — complementary to the survey's skills chapter (one says "package", the other says "sometimes collapse").
- [[codified-context]] — hand-engineered instance of all three externalizations simultaneously.
- [[context-folding]], [[agentic-context-engineering]] — context-resident-compression instances of memory externalization.
- [[memory/memgpt]], [[memory/letta-memory-blocks]], [[memory/mem0]], [[memory/mempalace]], [[memory/anthropic-memory-tool]], [[memory/claude-code-session-memory]], [[memory/longmemeval]], [[memory/reflexion]], [[memory/generative-agents]] — memory-externalization instances explicitly cited or implicitly mapped.
- [[cognition-cloud-agents]], [[microsoft-agent-365]], [[openai-symphony]] — sandboxing/governance/orchestration instances of the harness chapter.
- [[langchain-deep-agents]] — four-component harness decomposition congruent with the survey's framing.
- [[ai-scientist-v2]] — node-tuple state pattern as materialised state externalization.
- [[anthropic-internal-study]], [[willison-cognitive-cost]], [[notion-token-town]] — practitioner counterparts to the architectural shift the survey describes.
