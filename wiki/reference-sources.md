# Reference Sources

Curated trend radar for the agentic-AI wiki. Seeded 2026-04-22.

## Purpose

This file is the starting list of channels the wiki *watches* for new agent patterns, coding-agent releases, benchmark movement, and production war stories — distinct from the captured raw sources under `../raw/`. `/lint` and `/weekly-brief` consult this file each run to:

1. Sweep each active source for items published since the last sweep.
2. Compare surfaced items against wiki coverage (agent patterns, practices, evaluation, case studies, coding agents, deployments, gaps, trends).
3. Propose candidates for `/research` or `/ingest`, ranked by fit to the domain (agentic systems, LLM-as-judge, coding agents, enterprise deployment, context engineering, agent evaluation).
4. Evolve this file: flag dead/low-signal sources for retirement, propose additions.

Nothing here is captured yet. Capture happens only after the user approves a candidate during `/lint`, or when `/weekly-brief` autonomously selects a trending item, or when `/research` / `/ingest` is run directly.

## Status vocabulary

- **active** — sweep every `/lint` / `/weekly-brief` run.
- **probation** — sweep, but demote to retired if no signal lands after N sweeps.
- **retired** — historical record; don't sweep. Kept here so a future sweep doesn't re-propose something already tried and dropped.

## How `/lint` and `/weekly-brief` evolve this list

After each sweep, propose:
- **Add**: a source that was referenced ≥3 times across captured sources or other radar entries and isn't already here.
- **Demote**: move active → probation if two consecutive sweeps surfaced nothing relevant.
- **Retire**: probation → retired after three zero-signal sweeps.
- **Promote**: probation → active after a single high-quality hit (something we actually ingested).

Ask the user before editing this file; don't auto-mutate.

---

## Paper-feed accounts (X / Twitter)

X/Twitter is gated for programmatic capture. `capture_url --js` sometimes works, often fails. Fallback: paste the interesting thread into `raw/manual/<slug>/<slug>.md` and `/ingest`.

| Handle | URL | Role | Added | Status |
|---|---|---|---|---|
| @_akhaliq (AK) | https://x.com/_akhaliq | Highest-volume daily feed of new arXiv papers, model releases, agent demos. | 2026-04-22 | active |
| @swyx | https://x.com/swyx | Latent Space host; tracks the AI-engineering / agents stack in real time. | 2026-04-22 | active |
| @hwchase17 | https://x.com/hwchase17 | LangChain founder; surfaces agent-framework trends and production pains. | 2026-04-22 | active |
| @simonw | https://x.com/simonw | Simon Willison — tool-use, coding agents, practitioner writeups. Low volume, high signal. | 2026-04-22 | active |
| @karpathy | https://x.com/karpathy | Strategic takes on LLM capabilities + agent design. Low volume, high signal. | 2026-04-22 | active |
| @mathemagic1an | https://x.com/mathemagic1an | Linus Lee — context engineering, agent UX, tool-use patterns. | 2026-04-22 | active |
| @cwolferesearch | https://x.com/cwolferesearch | Cameron Wolfe — long-form writeups on agent methods and RLHF. | 2026-04-22 | active |
| @jxmnop | https://x.com/jxmnop | Jack Morris — agent research and critique. | 2026-04-22 | probation |
| @yoheinakajima | https://x.com/yoheinakajima | BabyAGI lineage; early-signal on agent experimentation. | 2026-04-22 | probation |
| @alphaxiv | https://x.com/askalphaxiv | alphaXiv — social layer on arXiv; surfaces trending agent papers (cs.AI, cs.CL). | 2026-04-22 | active |

## Vendor / lab engineering blogs

These are high-signal writeups from the labs shipping frontier agent products. Watch their blog indexes and RSS feeds where available.

| Source | URL | Role | Added | Status |
|---|---|---|---|---|
| Anthropic Engineering | https://www.anthropic.com/engineering | Agent harness design, Claude Code, context engineering, coding-agent case studies. | 2026-04-22 | active |
| Anthropic News / Research | https://www.anthropic.com/news | Capability announcements, model cards, agent benchmarks. | 2026-04-22 | active |
| OpenAI Blog | https://openai.com/blog | Agent SDK, GPT-agents, model + tool-use releases. | 2026-04-22 | active |
| DeepMind Blog | https://deepmind.google/discover/blog | Frontier agent / RL research. Lower frequency but high signal when on-topic. | 2026-04-22 | probation |
| Cognition (Devin) | https://cognition.ai/blog | Devin / autonomous coding-agent writeups. | 2026-04-22 | active |
| Cursor Blog | https://cursor.sh/blog | Fast-apply, inline-edit, coding-agent product posts. | 2026-04-22 | active |
| Factory AI | https://www.factory.ai/news | Droid / autonomous-agent case studies and engineering notes. | 2026-04-22 | active |
| LangChain Blog | https://blog.langchain.dev | Framework trends, agent eval patterns (LangSmith), field reports. | 2026-04-22 | active |
| LlamaIndex Blog | https://www.llamaindex.ai/blog | RAG-heavy; occasional agent / workflow patterns. | 2026-04-22 | probation |
| Replit Blog | https://blog.replit.com | Agent v2 / coding-agent posts. | 2026-04-22 | probation |
| Sierra / Bret Taylor | https://sierra.ai/blog | Enterprise agent deployment writeups. | 2026-04-22 | probation |

## GitHub awesome-lists

Meta-sources: curated link collections maintained by the community. Sweep their recent commits / changelogs to spot what was added since the last sweep.

| Repo | URL | Focus | Added | Status |
|---|---|---|---|---|
| e2b-dev/awesome-ai-agents | https://github.com/e2b-dev/awesome-ai-agents | Flagship agent list; frameworks, autonomous + multi-agent. | 2026-04-22 | active |
| slavakurilyak/awesome-ai-agents | https://github.com/slavakurilyak/awesome-ai-agents | Alternative curated agent list; tools, SDKs, use cases. | 2026-04-22 | active |
| hyp1231/awesome-llm-powered-agent | https://github.com/hyp1231/awesome-llm-powered-agent | Academic LLM-agent papers; strong on surveys and taxonomies. | 2026-04-22 | active |
| Hannibal046/Awesome-LLM | https://github.com/Hannibal046/Awesome-LLM | General LLM list; broad coverage, often surfaces agent papers early. | 2026-04-22 | active |
| kyrolabs/awesome-agents | https://github.com/kyrolabs/awesome-agents | Agent frameworks + tooling. | 2026-04-22 | probation |
| e0xextazy/awesome-llm-agents | https://github.com/e0xextazy/awesome-llm-agents | Alternative academic list; slower-moving. | 2026-04-22 | probation |
| modelcontextprotocol/servers | https://github.com/modelcontextprotocol/servers | Flagship MCP server collection; proxy for agent-tool ecosystem growth. | 2026-04-22 | active |

## Podcasts

Podcasts with RSS feeds can be programmatically sampled for episode titles + descriptions (`capture_url` on the show's episode-index page works). Transcripts via `fetch_transcript` when a YouTube version exists.

| Podcast | URL | Role | Added | Status |
|---|---|---|---|---|
| Latent Space | https://www.latent.space | Heavy coding-agents / agent-engineering coverage. swyx + Alessio. | 2026-04-22 | active |
| The Cognitive Revolution | https://www.cognitiverevolution.ai | Nathan Labenz — applied agents, enterprise deployment, failure modes. | 2026-04-22 | active |
| Dwarkesh Podcast | https://www.dwarkesh.com/podcast | Long-form interviews with frontier lab founders; agent strategy signal. | 2026-04-22 | active |
| AI Engineer Podcast | https://www.ai.engineer/podcast | Practitioner interviews from the AI Engineer conference circuit. | 2026-04-22 | active |
| Practical AI | https://changelog.com/practicalai | Applied ML / agents; surfaces tooling + MLOps patterns. | 2026-04-22 | probation |
| TWIML AI Podcast | https://twimlai.com/podcast/twimlai | Research-oriented interviews; occasionally on-topic for agents. | 2026-04-22 | probation |

## Subreddits

Reddit captures cleanly via `capture_url` on `old.reddit.com/r/<sub>/top/?t=week` (or a specific thread URL).

| Subreddit | URL | Role | Added | Status |
|---|---|---|---|---|
| r/LocalLLaMA | https://old.reddit.com/r/LocalLLaMA | Practitioner hub; fast signal on open agent stacks + tool-use. | 2026-04-22 | active |
| r/LangChain | https://old.reddit.com/r/LangChain | Framework-specific; useful for failure modes and deployment pains. | 2026-04-22 | active |
| r/AI_Agents | https://old.reddit.com/r/AI_Agents | Dedicated agents community; variable quality but surfaces novel frameworks. | 2026-04-22 | probation |
| r/LLMDevs | https://old.reddit.com/r/LLMDevs | LLM-app developer discussion; occasional agent-relevant threads. | 2026-04-22 | probation |
| r/MachineLearning | https://old.reddit.com/r/MachineLearning | Paper breakdowns; filter for `[R]` flair. Lower signal for agents specifically. | 2026-04-22 | probation |
| r/ClaudeAI | https://old.reddit.com/r/ClaudeAI | Claude-practitioner community; surfaces Claude-Code / MCP / agent patterns. | 2026-04-22 | probation |

## Benchmark leaderboards

Agent-eval leaderboards are a direct trend signal: model or framework climbs often precede paper releases.

| Leaderboard | URL | Tracks | Added | Status |
|---|---|---|---|---|
| SWE-bench Verified | https://www.swebench.com | Real-world coding-agent fix rate on GitHub issues. | 2026-04-22 | active |
| τ-bench (Tau-bench) | https://github.com/sierra-research/tau-bench | Multi-turn agent task completion in customer-service / retail domains. | 2026-04-22 | active |
| OSWorld | https://os-world.github.io | Computer-use agent performance on desktop tasks. | 2026-04-22 | active |
| GAIA | https://huggingface.co/spaces/gaia-benchmark/leaderboard | General AI assistant tasks; proxy for tool-use + reasoning. | 2026-04-22 | active |
| AgentBench | https://github.com/THUDM/AgentBench | Multi-domain agent capability benchmark. | 2026-04-22 | probation |
| WebArena / VisualWebArena | https://webarena.dev | Web-navigation agent performance. | 2026-04-22 | probation |

## Discord communities

Discord is gated — no public capture. Monitor manually. When something interesting shows up, paste the excerpt into `raw/manual/<slug>/<slug>.md` with channel + author + date metadata, then `/ingest` that path.

| Community | Notes | Added | Status |
|---|---|---|---|
| LangChain | Official LangChain discord; agent-framework practitioner signal. | 2026-04-22 | active |
| Anthropic | Official Anthropic discord; Claude-Code and MCP channels surface agent patterns. | 2026-04-22 | active |
| Hugging Face | `#papers` channel; agent-paper signal. | 2026-04-22 | active |
| CrewAI | Multi-agent framework community; orchestration patterns. | 2026-04-22 | probation |
| AutoGen | Microsoft multi-agent framework community. | 2026-04-22 | probation |

Invite links change; find current invites through each community's website or pinned posts in their subreddit / X profile.

---

## Related

- [[CLAUDE]] — wiki operating manual
- [[index]] — content catalog
