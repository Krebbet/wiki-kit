# Claude Platform Cost Optimization

Anthropic published vendor-primary guidance (claude.com/blog, 2026-09-08, authored around the `claude-api` Agent Skill) arguing performance and cost aren't a strict trade-off: many Claude Platform applications can cut cost without losing performance via three levers — maximizing prompt-cache hit rate, removing prompt "anti-patterns" introduced by earlier model generations, and calibrating reasoning effort to the task. The guidance ships as three new `claude-api` skill subcommands (`prompt-audit`, `cost-optimize`, `hillclimb`) runnable inside Claude Code, each demonstrated on concrete benchmarks with reported before/after cost and accuracy numbers.

## Lever 1: prompt caching

Before generating a response, Claude processes the prompt into an internal working state (*prefill*) and caches it (the KV cache); a request that starts with the same prefix reads the cache instead of recomputing it, billed at a fraction of full input price. Practical constraints: the cache is pinned to a specific model, cache reads must be byte-exact across the full prompt span, and the cache has a limited TTL. Tip: firing a `max_tokens: 0` request with an explicit cache breakpoint at session start (e.g., while a user is typing) warms the cache before the first real request.

## Lever 2: prompt anti-pattern removal (`prompt-audit`)

Prompts accumulate instructions that patch older models' weaknesses; these can drift into anti-patterns that hobble a newer frontier model and inadvertently increase cost (e.g., "verify twice" duplicating lookups on every turn, "be maximally thorough" triggering dozens of unneeded searches). In a migration test from Opus 4.8 to Opus 5 on a customer-support benchmark, six legacy anti-patterns were planted one at a time into a clean prompt; running `/claude-api prompt-audit` to strip them cut cost by 14.6% and *increased* accuracy by 5.3% on average — accuracy rose partly because a retired thinking-setting instruction was causing the API to reject every routing request outright, and a manual-scratchpad instruction was colliding with Opus 5's built-in thinking (writing the tool call inside reasoning and never executing it, on 3 of the tested tickets).

## Lever 3: effort calibration

"Effort" controls how hard Claude works before answering — low effort reaches conclusions faster, high effort deliberates/verifies/explores alternatives. The cost/performance curve across effort levels is reported as often steep with a diminishing last step: Claude Fable 5 on FrontierCode Diamond goes from 11.5%/$5.35-per-task (low effort) to 30.9%/$19.00-per-task (max effort) — a 2.7x score gain for 3.5x the cost. Claude Fable 5.1 on Humanity's Last Exam (no tools) goes from ~53%/$0.30-per-question (low) to ~61%/$2.23 (max) — the last step to max adds ~0.5 points for 46% more cost, within the benchmark's run-to-run noise. `/claude-api hillclimb` automates this search: it splits an evaluation into train/test sets, proposes configuration changes (model, effort, prompt edits), and reads failing train examples to fix what it finds. Demonstrated run: starting from Opus 4.8 at default (high) effort on a customer-support benchmark, hillclimb stepped down to Opus 5 at low effort + prompt-audit (98.9% train accuracy, 2.6¢/ticket), then to Sonnet 5 at low effort (98.9% at 1¢/ticket after adding routing rules found from failing-train-case analysis) — on 14 held-out test tickets the final config scored 90.5% vs. the original setup's 78.6%, at about 1/5 the cost.

## `cost-optimize`: holistic audit

`/claude-api cost-optimize` profiles where application spend goes (via the Admin API usage/cost reports, per-response usage objects, or static estimation), then ranks savings starting with caching, request trimming (including a prompt-audit pass), output bounding, and Batch API use for unattended work. Across four public-benchmark test runs: one dropped thinking tokens from 102,779 to 8,284 with pass rate flat and cost down ~58% (caching a shared prefix + low effort + Batch API); one cut spend 73% with flat pass rate; one added batching + document caching to cut cost from $136.20 to $64.87; one found caching already correct and instead cut cost via medium effort + concise-output constraints (median steps per task 29→17, prompt tokens 75.2M→33.7M).

## Related

- [[patterns/anthropic-context-engineering]] — canonical Anthropic context-engineering reference (JIT retrieval + compaction + structured-note-taking); this page adds prompt-caching mechanics (prefill/KV cache, byte-exact prefix requirement, TTL, cache-warming trick) at a level of technical depth that page doesn't cover
- [[patterns/model-cost-routing]] — same cost/accuracy-frontier goal from a different axis: LangChain's Switchyard routes cheap tasks to a smaller model (cross-model routing), whereas this page's effort-calibration lever tunes cost/accuracy within a single model
- [[coding-agents/cognition-swe-2]] — same week's parallel cost/performance-frontier story, but attacking it via RL-trained selectable effort levels baked into model weights rather than harness-side prompt/effort tuning
- [[deployments/deepseek-v4-1-flash]] — same week's parallel cost story from the opposite end of the stack: this page treats cost as a prompt/effort-calibration problem, DeepSeek treats it as a serving/KV-cache-architecture problem
- [[patterns/agent-skills]] — `claude-api` is a concrete official Anthropic Agent Skill, now shipping three cost/perf subcommands; a fresh production instance for the skills-cluster hub page
- [[patterns/effective-harnesses]] — shares the "optimization takes deliberate operational discipline, not just automatic gains" theme via a distinct lever set (caching/anti-patterns/effort vs. long-horizon context/recovery)

## Source

- `raw/research/weekly-2026-09-13/05-05-anthropic-claude-platform-cost-perf.md` — captured 2026-09-13 from claude.com/blog, "Reducing cost and improving performance with Claude Platform" (2026-09-08). **Vendor primary** — trustworthy per this wiki's source-authority convention; benchmark numbers are Anthropic-reported internal demonstrations (collect-but-confirm on exact figures, though the mechanism descriptions themselves are primary-source reliable).
