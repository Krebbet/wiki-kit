# Coding Agent Adoption in New GitHub Projects

Empirical companion study to "Agentic Much?" (arXiv 2601.18341), analyzing **12,794 new GitHub projects** created after August 2025. Finds coding agent adoption in new projects is more than **2.7× higher** than in older projects, and dramatically more intensive — with "pervasive" (>20% AI commits) as the single most common adoption tier.

## Source

- arXiv 2606.07448 — "Agentic Very Much! Adoption of Coding Agent in New GitHub Projects" (June 2026)
- Raw: `raw/research/weekly-2026-06-14/05-05-coding-agent-adoption.md`
- Sample: projects created after 2025-08-29, accessed 2026-04-04, ≥10 GitHub stars, ≥100 commits, ≥5,000 LOC, not forks

## Key figures

| Metric | New projects | Older projects (prior study) |
|---|---|---|
| Conservative adoption | **71.83%** | 26.46% |
| High estimate adoption | ~76.15% | — |
| File-level ("all file-level use") | **60.03%** | 14.70% |
| "Pervasive" bin (>20% AI commits) | **41.2%** (modal) | 21.1% |
| Median commit ratio | ~30% | ~10% |
| Upper quartile commit ratio | ~75% | ~25% |

## Most popular tools in new projects

- **Claude Code**: ~6,443 projects — ~3× more popular than GitHub Copilot (third place) in new projects; in older projects Claude Code led Copilot by only ~6×
- **Codex** (via AGENTS.md + explicit): likely second-largest
- OpenCode, Amp, Kiro: comparatively more prominent in new projects than older

## Undetected AI activity

Median human-authored commit size rose from 10 to 29 lines added in new projects. Authors interpret this as undetected AI activity bleeding into "human" commits, not human productivity gains. True AI commit ratio is likely higher than the 71.83% conservative estimate.

## Language distribution

**Over-represented in new projects vs older:**
- Rust (2× prevalence — 10.53% vs 5.28%): rich static feedback loop for agents is a plausible driver
- TypeScript, TSX, Shell also elevated

**Under-represented:**
- Java, C++, C#, Kotlin (Java at 22% of older project rate)

## Enterprise adoption

Enterprise organizations (Microsoft 63.46%, Amazon 75%, Nvidia 56.25%, Google 44.44%) show adoption rates broadly in line with the ~60% overall figure. Their previous above-average relative position is gone — enterprise and community adoption have converged.

The top single adopter by project count was an individual developer ("Dicklesworthstone"), who created more repositories with coding agent traces than Microsoft during the study period.

## Dogfooding signal

Topic analysis shows newer projects are dominated by agentic AI topics: `mcp`, `ai-agents`, `claude-code`, `cursor`, `openclaw`, `agent-skills`. New agentic tooling is largely being built by agentic tooling users.

## Sampling bias caveat

The ≥100 commits / ≥5,000 LOC filter may over-select agentic projects among young repositories. Youngest projects show highest adoption (age decile analysis), which is consistent with an agentic-first norm for brand-new projects — but caution is warranted given the filter.

## Interpretation

71.83% conservative adoption means coding agents are no longer the exception in new GitHub projects — they are the default. The "Pervasive" bin being modal (41.2%) implies most new adopters are not experimenting with agent-assisted commits; they are building primarily with agents.

## Related

- [[coding-agents/langchain-deep-agents]] — LangChain's "shallow vs deep" adoption axis is corroborated empirically: new projects skew toward pervasive/deep adoption patterns
- [[case-studies/willison-product-market-fit]] — Willison's April 2026 revenue inflection and enterprise pricing shift provide a demand-side explanation for why post-August-2025 projects show dramatically higher adoption
- [[case-studies/willison-vibe-agentic-convergence]] — the dogfooding dominance of agentic AI topics in new project repos corroborates the collapsing vibe-coding / agentic-engineering distinction
- [[patterns/agents-md]] — "Generic" category (AGENTS.md-identified projects) is the second-largest adoption class; institutional momentum now visible in adoption data
- [[governance/aaif]] — AAIF's 60k+ repositories claim gets empirical context from the 12,794-project adopter pool
- [[deployments/openai-symphony]] — Symphony's zero-human-code thesis aligns with this study's finding that brand-new projects are the most intensely agentic
- [[evaluation/agents-last-exam]] — adoption is pervasive; ALE provides the performance ceiling for what those agents actually achieve on professional tasks
- [[evaluation/adk-arena]] — ADK Arena's Claude Code efficiency data (40.5% task resolution at 8-10× fewer tokens) is consistent with Claude Code's dominant market position shown here
