# Shadow Evaluations: Can AI Agents Conduct Open-Ended AI Research?

Princeton/CRUX researchers (Kirgis, Kapoor, Schwartz, Rabanser, Narayanan et al., arXiv:2607.27191) introduce **shadow evaluations** — a methodology, not a training technique — in which a frontier agent is given the central research question of an unpublished NeurIPS 2026 paper and the paper's own authors grade the agent's output as conference reviewers. Across two such shadow evaluations (Personas, TabPFN), agents executed the engineering flawlessly but produced work the original authors scored 2/6 and 1/6 overall — unambiguous rejects — surfacing five recurring failure modes in autonomous long-horizon research judgment and directly countering optimistic recursive-self-improvement narratives.

## Method: shadow evaluation

Take the unpublished, uncontaminated central research question of a high-quality paper (uncontaminated because it can't have been memorized or scraped), hand it to a well-resourced agent with no access to the real paper or its findings, and have the original authors — who spent months on the same question — grade the agent's output on the same 1–6 scale NeurIPS reviewers use (Quality, Clarity, Significance, Originality, Overall, Confidence). This is positioned as a third evaluation paradigm, distinct from:

- **Verifiable/benchmark tasks** — RE-Bench, MLE-Bench, CORE-Bench, PostTrainBench, MLR-Bench — which reduce research to a single scorable metric.
- **Blind peer review of AI-generated papers** — AI Scientist-v2, Zochi/Intology — stochastic, and prior work doesn't disclose failed attempts.

Shadow evaluation trades blindness (reviewers already know the paper is AI-authored and already know the answer) for reviewer expertise and contamination-free task construction.

Agent infrastructure: [[openclaw]] as the primary scaffold (chosen after dry runs showed Opus 4.8 outperforming GPT-5.3 Codex), run with extra-high reasoning effort, full VM/web access, self-review subagents, and three external AI reviewing tools (Stanford Agentic Reviewer, CMU Paper Reviewer, refine.ink). Budgets: 6 days wall-clock (+24h extension), $3,000 Anthropic API credits, plus GPU compute credits. A robustness check reran one study on Codex + GPT-5.6 Sol Ultra to rule out scaffold-specific ("scaffold overhang") artifacts — a real usage data point for OpenClaw, including a live bug the run hit and patched around Anthropic thinking-block signatures.

## Case studies and scores

**Personas** (LLM persona decomposition/control in weight space): Quality 2/4, Clarity 1/4, Significance 2/4, Originality 3/4, **Overall 2/6 (Reject)**, Confidence 4/5.

**TabPFN** (deployment-time shift-detector for tabular foundation models): Quality 1/4, Clarity 2/4, Significance 2/4, Originality 2/4, **Overall 1/6 (Strong Reject)**, Confidence 5/5.

Both studies were unambiguously rejected by authors with high confidence. Notably, agents left over half their API budget unused in both main runs, and produced papers exceeding NeurIPS's page limit with far thinner scholarly apparatus than the originals (36 vs. 69 references for TabPFN, 16 vs. 52 for Personas; 0 vs. 15 main-body figures for Personas). Across 15 self-review revision rounds, the AI reviewer loop never once returned an accept — yet agents responded with hedging caveats and narrowed claims rather than changing approach. No reward hacking was observed; agents even retired marketable claims in favor of reporting negative results.

The robustness check on Codex/GPT-5.6 Sol Ultra reproduced nearly all the same failure modes, but with an inverted resource-mismanagement pattern: it blew the entire $3,000 API budget in ~2 days, leaving ~100 hours of wall-clock unused (vs. the main runs' budget underuse). Reasoning effort mattered directly: Opus-4.8-without-reasoning dry runs produced markedly worse literature reviews and more inscrutable writing than the extra-high-reasoning main runs — but the authors judge that more wall-clock or compute would not have fixed the *core* problems.

## Five failure modes

1. **Judgment about the publishable bar** — agents cannot calibrate what constitutes a genuinely novel, significant contribution vs. an incremental or shallow one.
2. **Uncreative response to negative feedback** — self-review reliably flags real problems, but agents add caveats/narrowing instead of restructuring the approach.
3. **Ineffective backtracking** — premature convergence on the first plausible hypothesis, with failure to abandon it at the project level even when clean-context subagents are available to enable a fresh restart.
4. **Poor resource/time awareness** — agents under-use or catastrophically over-use time and compute budgets even when explicitly instructed to manage them, and cannot reliably self-monitor.
5. **Instruction drift** — output diverges from the original research brief over the course of a long-horizon run.

## Applicability

Not a technique to adopt — an evaluation result to internalize before trusting an agent with an open-ended, week-long autonomous research loop. Practical implications for anyone scaffolding such agents: build in forced continuation rather than relying on self-termination/self-pacing of budget; don't expect self-review loops to trigger re-planning — they surface problems but agents patch around them with caveats instead of pivoting; expect and plan for premature hypothesis lock-in even with restart mechanisms available. Requires multi-day wall-clock, real API/GPU spend, and (to reproduce the eval itself) willing authors of an unpublished paper — full artifacts (reviews, survey responses, agent repos, run logs) are released at cruxevals.com, with one paper's full logs withheld since its source remains unpublished.

## Countering recursive-self-improvement narratives

This paper is explicit empirical counter-evidence to optimistic recursive-self-improvement claims — it directly engages with and pushes back on Anthropic's "When AI Builds Itself," Kokotajlo et al.'s "AI 2027," and OpenAI's GPT-5.6 Sol post-training claims. The key move is separating two distinct capability claims that get conflated in those narratives:

- **Verifiable/narrow agentic capability** — where this wiki already documents strong positive results: [[huxley-godel-machine]] (tree-search self-improving coding agent, human-level SWE-bench Lite), [[qwen-agentworld]] (agentic-domain world models beating frontier baselines on AgentWorldBench), [[skillopt]] (skill-document optimization, best-or-tied across 52 eval cells), [[seal-self-adapting]] (RL-trained self-edit generation for weight updates). All of these operate against cheap, repeatable, binary-graded signals.
- **Open-ended research judgment** — where this paper finds agents fail outright, engineering execution notwithstanding. There is no verifiable reward signal for "is this a good NeurIPS paper," and that's precisely the setting where all five failure modes bite.

No existing wiki page yet stakes out the strong "agents can already do open-ended AI R&D" claim outright, so this isn't a head-on contradiction of a specific prior page — it's the natural counterweight to the self-improving-agents cluster, and the one to check against if/when a source making that stronger claim is ingested.

## Source

- `raw/research/weekly-2026-08-01/04-ai-agents-open-ended-research.md`

## Related

- [[openclaw]] — primary agent scaffold used for both shadow-evaluation studies; run surfaced a live OpenClaw bug around Anthropic thinking-block signatures.
- [[huxley-godel-machine]] — self-improving coding agent with strong *verifiable* SWE-bench results; this paper sharpens the boundary between that engineering-verifiable success and open-ended research failure.
- [[qwen-agentworld]] — agentic-domain capability (including software engineering simulation) that generalizes well in verifiable settings, contrasted here with open-ended research judgment that doesn't.
- [[skillopt]] — both concern agents evaluating/improving their own process via validation loops; SkillOpt's bounded, strictly-validated skill edits succeed where this paper's unbounded self-review loop fails to produce course-correction.
- [[seal-self-adapting]] — closest analogue to "agent revises its own output based on a learned signal"; this paper's finding that self-review flags problems without triggering restructuring is a cautionary data point for that broader pattern.
