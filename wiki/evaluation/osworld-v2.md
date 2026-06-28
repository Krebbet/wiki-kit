# OSWorld 2.0

Long-horizon real-world computer-use benchmark released June 25, 2026. Raises the bar from ~30-step tasks to 318-step median workflows averaging 1.6 human-hours; no agent exceeds 21% binary completion. Surfaces a sharp nonlinear token-efficiency frontier: doubling token budget from ~110K to ~225K tokens yields only ~2.3 pp additional reward.

## Benchmark Characteristics

- **Task horizon**: 318-step median workflows; ~1.6 human-hours of equivalent work per task
- **Scoring**: binary reward (0 or 1) — partial credit not awarded for most tasks
- **Domains**: long-horizon desktop OS interaction (real-world applications and workflows)
- **Reasoning effort axis**: agents tested at multiple inference compute budgets (low → max)
- **Coverage**: frontier labs (Anthropic, OpenAI) and open-weight models (MiniMax M3, Qwen 3.7-Plus, Claude Opus 4.7/4.8)

## Leaderboard Results

| Model | Binary Reward | Output Tokens |
|-------|--------------|---------------|
| Claude Opus 4.8 | ~20.5% | ~225K |
| Claude Opus 4.7 | ~18.2% | ~150K |
| GPT-5.5 | ~14.0% | ~37K |
| MiniMax M3 | (partial data) | — |

- **Claude Opus 4.8** leads on absolute accuracy but at disproportionate token cost: ~6× more tokens than GPT-5.5 for ~6.5 pp more reward.
- **GPT-5.5** is the most token-efficient agent: ~37K output tokens for ~14% reward.
- **Intra-Claude scaling**: Opus 4.7 → 4.8 adds ~2.3 pp absolute at 1.5× the token cost — clearly diminishing returns at the frontier.

## Significance

OSWorld 2.0 is the first major computer-use benchmark where:
1. No agent approaches ceiling — everyone is well below 25%, making it a live measuring stick for the next 12+ months
2. The token-efficiency tradeoff is quantified explicitly, making it actionable for deployment decisions
3. Task lengths model realistic human workflows rather than scripted sub-tasks

The sharp score-vs-token nonlinearity has direct implications for harness engineering: throwing more compute at computer-use tasks has rapidly declining returns at the frontier.

## Capture Note

The primary website (osworld-v2.xlang.ai) is heavily JavaScript-rendered; the captured markdown preserves the leaderboard data but may not include the full task taxonomy and methodology details from the paper. Recommend re-capture if a primary arXiv paper URL is published.

## Source

- Raw: `raw/research/weekly-2026-06-28/05-osworld-v2.md`
- Primary: https://osworld-v2.xlang.ai / https://github.com/xlang-ai/OSWorld-V2
- Captured: 2026-06-28

## Related

- [[evaluation/swe-cycle]] — both are long-horizon benchmarks; complementary (coding vs. computer-use)
- [[airs-bench]] — autonomous research tasks; same long-horizon real-world paradigm
- [[patterns/agentic-harness-engineering]] — token-budget vs. task-completion tradeoff applies directly
- [[deployments/shopify-simgym]] — cloud browser system; OSWorld v2 results give external performance anchor
- [[deployments/cognition-cloud-agents]] — operates in same desktop-agent space; OSWorld v2 is the external eval
