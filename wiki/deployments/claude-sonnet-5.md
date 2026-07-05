---
slug: claude-sonnet-5
---

# Claude Sonnet 5

Anthropic launched Claude Sonnet 5 on July 5, 2026 as its most capable Sonnet-class model to date, positioned to narrow the gap with Opus 4.8 at a substantially lower price point *(2026-07-05)*. The model is designed first and foremost for agentic work — multi-step planning, tool use, autonomous debugging, and sustained execution across complex codebases — and ships as the default on Free and Pro plans while remaining available in Claude Code and the API. An updated tokenizer (roughly 1.0–1.35× token expansion vs. Sonnet 4.6 depending on content type) accompanies the release; introductory pricing is calibrated to make the tokenizer change roughly cost-neutral for existing Sonnet 4.6 users.

## Key capabilities

- **Agentic follow-through**: Partners report that Sonnet 5 completes multi-step tasks where earlier Sonnet models would stall — finishing end-to-end workflows, self-checking output without being explicitly prompted, and sustaining focus on complex tasks longer than Sonnet 4.6.
- **Coding and brownfield work**: Described by early-access partners as especially strong on messy, real-world codebases — tracing failures to root causes, handling race conditions and hidden tests, and shipping durable fixes rather than symptomatic patches.
- **Effort-level cost-performance**: On BrowseComp (agentic search) and OSWorld-Verified (computer use), Sonnet 5 reportedly dominates Sonnet 4.6 at all effort levels and, at extra-high effort, approaches Opus 4.8 on some tasks — collect-but-confirm; cost-performance curves depend on Anthropic's internal evaluation methodology and are subject to revision (the BrowseComp chart was corrected after launch).
- **Reduced sycophancy and hallucination**: Safety evaluations show lower rates of hallucination and sycophancy than Sonnet 4.6 — collect-but-confirm pending independent replication.
- **Tool use and computer use**: Available at all Claude effort levels; higher effort levels unlock broader agentic capability at proportionally higher token cost.
- **API model ID**: `claude-sonnet-5` via the Claude API and Claude Code.

## Pricing and availability

| Period | Input | Output |
|---|---|---|
| Introductory (through 2026-08-31) | $2 / MTok | $10 / MTok |
| Standard (from 2026-09-01) | $3 / MTok | $15 / MTok |

- Available today across all Claude plans: default model on Free and Pro; available on Max, Team, and Enterprise.
- Available in Claude Code and the Claude Platform API at launch.
- Tokenizer note: Sonnet 5 uses an updated tokenizer that increases token counts by roughly 1.0–1.35× vs. Sonnet 4.6 depending on content type; introductory pricing is set to make the transition roughly cost-neutral.
- Rate limits increased across Chat, Cowork, Claude Code, and the Claude Platform to accommodate higher token usage from elevated effort levels.

## Safety posture

- **Misaligned-behavior audit**: Sonnet 5 scores lower (safer) overall than Sonnet 4.6 on Anthropic's automated behavioral audit, which tests a wide range of undesirable behaviors including cooperation with misuse and deception — collect-but-confirm on the specific rates; Sonnet 5 rates remain higher than Opus 4.8 and Mythos Preview on this same audit.
- **Prompt injection**: Improved resistance to hijack attempts vs. Sonnet 4.6; better at refusing malicious requests in agentic contexts.
- **Cybersecurity capability**: 0% working Firefox exploit success rate (same as Sonnet 4.6); slightly higher partial-success rate attributed to general intelligence gains rather than targeted cybersecurity training. Cyber safeguards are enabled by default — the same real-time detection and blocking used in Opus 4.7/4.8, tuned less strictly than Fable 5 given the lower overall cyber risk level.
- **Cyber Verification Program**: Sonnet 5 participates; organizations already enrolled carry over automatically. Anthropic recommends Opus 4.8 for cybersecurity work requiring reduced guardrails.
- Full details: [Claude Sonnet 5 System Card](https://www.anthropic.com/claude-sonnet-5-system-card).

## Source

- Anthropic blog post: <https://www.anthropic.com/news/claude-sonnet-5> (captured 2026-07-05)
- Raw capture: `raw/research/weekly-2026-07-05/02-01-claude-sonnet-5.md`
- System Card: <https://www.anthropic.com/claude-sonnet-5-system-card>

## Related

- [[deployments/anthropic-finance-agents]] — Sonnet 5 is the new default on Free/Pro/Claude Code plans
- [[evaluation/osworld-v2]] — Sonnet 5 benchmarked on OSWorld-Verified
- [[patterns/agentic-harness-engineering]] — partner quotes illustrate multi-step autonomous execution patterns
- [[security/prompt-injection-impossibility]] — Sonnet 5 shows improved resistance to prompt injection hijack
- [[deployments/openai-agents-transforming-work]] — parallel data point on Sonnet-class models in production
