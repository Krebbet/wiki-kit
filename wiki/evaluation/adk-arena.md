# ADK Arena

ADK Arena (arXiv 2606.05548, Ohio State / Microsoft, 2026) introduces **LLM-as-a-Developer**: an automated methodology that replaces human developers with an LLM coding agent to evaluate all 51 popular Python agent frameworks at once. The LLM learns each framework's API from its documentation and source code, writes a benchmark agent, and iteratively repairs it through a three-level validate-and-repair loop. By holding the developer constant and varying only the framework, generation cost becomes a quantitative proxy for API usability and execution results measure framework effectiveness. Running 204 framework-benchmark pairs (51 frameworks × 4 benchmarks, two developer models each), the study produces the first ecosystem-wide comparison of agent development kits with no hand-written benchmark code.

## Core contributions

- **LLM-as-a-Developer methodology**: analogous to LLM-as-a-Judge but replaces human *developers* rather than evaluators; controlled-variable protocol with identical prompts, tools, and token budgets per framework
- **ADK Arena pipeline**: per-framework Docker isolation, a three-level Validate-and-Repair pipeline (static analysis → LLM smoke test → real benchmark task), token-level telemetry via a unified LLM proxy, and adapters for four benchmarks
- **Ecosystem survey**: 51 Python ADK frameworks sourced from academic venues, GitHub topic search (≥1K stars), and curated lists; dependency graph and adoption metrics for all 51

## Evaluation methodology

**Benchmarks** (50 tasks each, execution via GPT-5.4 Nano):
- SWE-bench Verified — software engineering, long-horizon code editing
- τ2-bench — conversational tool-use, multi-turn
- MCP-Atlas — multi-tool orchestration via MCP servers
- Terminal-Bench — command-line interaction

**Three-level validation pipeline**:
1. *Static analysis*: compile check, import verification, framework-usage check (rejects raw API fallbacks), 40+ AST/regex anti-pattern checks
2. *LLM smoke test*: executes `solve()` against a real LLM via token-recording proxy; verifies routing and response handling
3. *Real benchmark task*: runs one official task under realistic conditions; early-exit check confirms expected behavior

**Information-source ablation conditions** tested across all 51 frameworks:
- DOCS ONLY: curated documentation, no source code
- SOURCE ONLY: raw source code, no curated docs
- NONE: no reference material (parametric knowledge only)

**Unified LLM proxy**: handles bidirectional Anthropic ↔ OpenAI protocol translation, enabling all 51 frameworks to run against the same backbone regardless of their native provider API.

## Framework comparison results

Generation succeeds for **57% of runs** (232/408). Per-agent generation cost ranges **$0.6–$3.4 (5.6x spread)** and correlates with API surface size:

- Cheapest to learn: LangGraph ($1.0/agent), SmoLAgents ($1.3), Solace ($1.2)
- Most expensive: MCP Agent ($3.4), AgentFramework ($3.4), Composio ($3.1)
- Cost signals complexity, not success: Langroid is cheapest ($0.2–0.7) but generates zero passing agents because the developer gives up early; Haystack and AG2 pass all four benchmarks at moderate cost

**Resolution rates by benchmark** (among agents that execute):
- τ2-bench: median 64%, best 80% — most tractable due to conversational, tool-calling format
- MCP-Atlas: median 39% — rewards correct MCP tool discovery and routing
- SWE-bench: median 18% — long-horizon iterative editing, early missteps cascade
- Terminal-Bench: median 14% — sustained command-execution loops rarely maintained

**Developer model effect**: Opus-4.6-authored agents resolve ~2x as many tasks as GPT-5.4-authored ones (mean 41% vs. 22%) on the same GPT-5.4 Nano execution backbone. GPT-authored agents frequently emit a minimal single-call wrapper; Opus-authored agents more often wire up the framework's full loop with tools and multi-turn iteration.

## Key findings

**No single framework dominates.** Best single-benchmark ADK agents reach 80% resolution and can beat frontier coding agents at a fraction of the cost. The median framework resolves only 32%.

**Code quality, fixed at generation time, largely determines execution success.** Passing validation is necessary but not sufficient; the developer model is more decisive than the execution backbone.

**Top ADK agents beat frontier agents cheaply on their target benchmark.** On MCP-Atlas, Agno resolves 68% at 38K input tokens/task vs. Copilot's 58% at 327K tokens (~9x fewer). But this is a top-of-distribution effect.

**Frontier agent efficiency tradeoff** (all on GPT-5.4 Nano):
- Copilot: 56% avg resolution, 3.9M tokens across 4 benchmarks, ~$0.57/task on SWE-bench
- OpenHands: 48.5% avg, 4.7M tokens
- Claude Code: 40.5% avg, 0.48M tokens, ~$0.05/task — 8-10x fewer tokens than Copilot/OpenHands
- Codex CLI: 39.5% avg, cheapest overall ($0.01–0.02/task)

**Documentation is not the bottleneck.** Genuine framework usage stays within 28–40% across all information conditions. DOCS ONLY is lowest (28%); SOURCE ONLY is highest (40%); NO REFERENCE outperforms DOCS ONLY (33% vs. 28%). Curated documentation anchors the developer toward imitating minimal quickstart examples (thin wrappers) rather than exercising the native API. Parametric knowledge of popular frameworks provides a floor.

**Supply-chain fragility.** 74% of inter-ADK dependencies are undeclared code-only imports. LangChain is the hub (in-degree 14), LlamaIndex second (in-degree 10). pydantic (required by 74.5% of frameworks) is the single largest systemic risk. Three bidirectional dependency cycles exist (LangChain ↔ LangGraph, AutoGen ↔ SemanticKernel, Composio ↔ CrewAI).

**Extreme adoption concentration.** Top 5 frameworks (LangChain, Anthropic SDK, LangGraph, OpenAI Agents, PydanticAI) account for 93% of all ADK downloads. LangChain alone: 233M downloads/month. Stars and downloads diverge: MetaGPT (67.5K stars, 42K downloads/month) signals research interest without production use; Anthropic SDK (3.3K stars, 103.8M downloads/month) is invisible infrastructure.

## Implications for framework selection

- **For production use**: LangChain, LangGraph, and OpenAI Agents have the lowest generation cost (easier to onboard), strong ecosystem adoption, and consistent multi-benchmark results. AG2 and Haystack pass all four benchmarks under both developer models.
- **For specific benchmarks**: best-in-class agents can significantly outperform general-purpose coding agents on a single task type (e.g., MCP-Atlas tool use), but this requires choosing the right framework and using a capable developer model to write the agent code.
- **For API design**: generation cost is a tractable proxy for API usability. Clean, learnable APIs (LangGraph, OpenAI Agents) cost $1–1.5/agent to target; large or poorly documented APIs cost 2–3x more. Framework authors should treat LLM-as-a-Developer generation cost as a design quality signal.
- **For supply-chain risk**: the high rate of undeclared code-only dependencies means pip install does not surface true dependency footprints. Teams should audit code imports, not just package metadata.
- **For documentation strategy**: raw source code access leads to better native API usage than curated docs alone. Documentation effort should prioritize concrete worked examples that exercise the full API loop rather than minimal quickstarts.

## Source
- arXiv 2606.05548 — Jintao Huang (Ohio State), Xiaomin Li, Gaurav Mittal, Yu Hu (Microsoft)
- Code: https://github.com/jintao-h/ADK-Arena

## Related
- [[wiki/evaluation/benchmarks.md]] — SWE-bench, τ2-bench, MCP-Atlas, Terminal-Bench used as ADK Arena benchmark adapters
- [[wiki/evaluation/airs-bench.md]] — parallel agent benchmarking effort; compare with LLM-as-a-Developer methodology
- [[wiki/evaluation/llm-as-judge.md]] — LLM-as-a-Developer is the same scalable-proxy paradigm applied to the developer role
- [[wiki/coding-agents/langchain-deep-agents.md]] — LangChain is the ecosystem dependency hub; ADK Arena results directly benchmark LangChain agent quality
- [[wiki/patterns/harness-design-space.md]] — ADK Arena's three-level validate-and-repair pipeline and Docker isolation is a concrete harness engineering case study
