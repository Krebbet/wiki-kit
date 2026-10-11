# Learn2Play Bench (arXiv 2610.08215)

A benchmark from NUS (published 2026-10-06) of 20 newly designed text games with hidden, often counterintuitive rules, built to test whether LLM agents learn across episodes without weight updates. Headline findings: with one backbone (Kimi K3) raw, unmodified interaction histories beat reflection, rule-extraction and strategy-summarization methods, but this ranking does not hold uniformly across backbones; harness choice moves scores substantially at a fixed backbone; and the best human players still beat every agent configuration. Method rankings and cost figures are collect-but-confirm (author re-implementations, 3 trials, one seed per game).

## Benchmark Design

- 20 hand-designed game templates: 10 fixed-instance, 10 "re-shuffled" (characters, layout or objects change, the rule stays fixed). Rules are hidden and often counterintuitive (e.g., stealing a colleague's lunch gets you promoted), so pretraining knowledge helps little.
- 5 "challenge" games (CATNIP, DREAMGARDEN, MOLA TEA, REDEYE, ROADSIDE OBSERVATORY) get 10 episodes; the other 15 get 5. Feedback is deterministic, scoring is automatic, and the agent sees only a black-box command interface (no source, no oracle).
- 3 independent trials per game with no memory across trials; one fixed seed per template.
- Metrics (normalized, challenge games weighted 3x): Max (peak), Mean, Learning Gain (last k vs first k episodes), Learning Slope (linear fit over episodes).
- 11 backbones run under the generic OpenCode harness (Opus 5.5, GPT-6 Astra, Opus 5, Sonnet 5, Gemini 3.5/3.7 Flash, GPT-5.6-SOL, GPT-5 Mini, DeepSeek V4 Pro, Kimi K3, Qwen 3.8 Max). Self-evolving methods were compared on only three: Kimi K3, Opus 5, GPT-5 Mini. Compared methods: NAIVE (no cross-episode memory), MEMORY (complete prior histories in the prompt, oldest dropped only when over the context budget), [[memory/reflexion]], EvoTest, ReasoningBank, AWM.
- Human study: college students, 21-30 per game.

## Results

**Backbones (Max / Mean / Learning Gain / Learning Slope):** Opus 5.5 80.1/61.0/+23.0/+5.22 (best Max and Mean); Qwen 3.8 Max 72.5/51.1/+25.2/+6.30 (best gain and slope); GPT-5 Mini 34.0/22.3/+9.2/+1.83 (worst). The best scorer is not the best learner.

**Transfer:** on re-shuffled games the learning slope drops even though the rule is fixed. Slope drop: Sonnet 5 2.67, Gemini 3.7 Flash 2.15, GPT-5.6-SOL 1.94, Gemini 3.5 Flash 1.73, Kimi K3 0.88, Opus 5 0.59, Claude Code/Opus 5 0.52; Qwen 3.8 Max (-0.41) and Codex (-0.19) show none. Weaker agents memorise episode-specific choices (e.g., menu position) rather than why an action worked. [[deployments/claude-sonnet-5]] shows the largest drop.

**Humans:** the top-1 human reaches Max 84.3 (slope +7.33), above the best agent configuration (Claude Code/Opus 5, Max 81.8). Humans explore more (consecutive-episode action similarity 0.54 vs 0.66 for agents; a new personal best after a bad episode 33% of the time vs 22%). Agents win on long action sequences and precise calculation (REDEYE, MODEL AUDITOR); humans win on novel-strategy discovery (GEMFORGE, GRAPEVINE). Top records are selected by Max, so there is a selection effect.

## Raw History vs Summarized Strategy

Finding as stated by the paper: "simply using past interaction histories can outperform more elaborate self-evolving methods." With **Kimi K3**, MEMORY leads all four metrics among the self-evolving methods:

| Method (Kimi K3) | Max | Mean | LG | LS |
|---|---|---|---|---|
| MEMORY (raw histories) | 63.3 | 48.0 | +16.9 | +4.69 |
| EvoTest | 62.4 | 48.0 | +1.8 | +1.01 |
| Reflexion | 61.6 | 40.4 | +14.8 | +3.35 |
| ReasoningBank | 59.9 | 40.1 | +8.3 | +2.59 |
| AWM | 56.1 | 37.0 | +4.8 | +0.62 |
| NAIVE | 54.7 | 31.9 | +0.3 | +0.42 |

The authors' mechanism: raw evidence stays available, so earlier conclusions can be revised, whereas reflection and rule extraction can freeze an incomplete understanding into rules that later episodes obey. Worked example: in GEMFORGE an EvoTest/Opus 5 run tried one combination, saw it fail, and wrote a prompt rule forbidding many other combinations, including ones that would have succeeded.

**Backbone-dependence caveat (important).** The effect is not uniform. From the paper's Table 1 (my reading):
- With **Opus 5**, MEMORY (60.9/48.2/+11.4/+2.87) trails EvoTest (66.1 Max / 51.3 Mean) and Reflexion (64.8 / 48.8) on Max and Mean, and is roughly level with ReasoningBank on gain and slope.
- With **GPT-5 Mini** (appendix), MEMORY has the best Mean (37.3) and a competitive slope, but Reflexion has the best Max (53.5).
- NAIVE with Opus 5 has negative learning gain (-5.1), so some cross-episode memory is clearly needed.

So the claim rests mainly on Kimi K3, and the abstract hedges ("can support more effective learning"). The defensible reading is "raw history is a strong baseline that summarizing pipelines do not reliably beat", not "raw always wins". Appendix intervals are large (e.g., GPT-5 Mini LG +9.2 +/- 3.9).

Design implications the paper draws: keep raw action/feedback records as the evidence substrate; treat distilled rules as revisable hypotheses linked to the interactions behind them (proposed future work); let the model decide when to consult history; and note that a context-budget cutoff drops the oldest episodes, so MEMORY degrades on long horizons.

## Harness Effects

- **Same-backbone swaps:** Claude Code with Opus 5 scores 81.8/62.3/+27.1/+6.59 vs OpenCode 74.5/53.8/+21.3/+5.13 (+7.3 Max). Codex with GPT-5.6-SOL scores 74.3/54.8/+22.2/+5.66 vs OpenCode 57.0/41.1/+14.5/+3.71 (+17.3 Max). The authors attribute this to models being trained on their own vendor harnesses.
- **Flexible agent vs preset pipeline:** generic OpenCode (shell/file agent) beats the preset-step self-evolving methods at the same backbone, since the model can review feedback, compute, or check a plan mid-episode rather than only updating memory between episodes. On Kimi K3, OpenCode Max is 68.5, above every method; on Mean (50.2) it is only slightly above MEMORY/EvoTest (48.0).
- **Cost (estimates):** OpenCode/Kimi K3 uses 56% fewer input tokens than MEMORY and 71% / 41% fewer generated tokens than EvoTest / ReasoningBank (pipelines call the model on every action and re-supply history). Kimi K3 is cheaper per episode than Sonnet 5 despite higher per-token prices (0.56M vs 0.73M tokens per episode), and Claude Code/Opus 5 beats the self-evolving methods at lower estimated cost. Per-token price does not imply total cost.

## Limitations

- One fixed seed per game template; only 3 trials with large intervals.
- Text games only; no weight updates, so it says nothing about fine-tuning-based learning.
- Self-evolving methods tested on 3 backbones, and the method ranking changes by backbone. Implementations are the authors' re-implementations, not necessarily tuned.
- Human participants were students; top human records are Max-selected.
- Cost figures are estimates. Agents stop exploring once a partial strategy works and plan greedily (HAUNTED INN).
- No explicit code/data release statement found in a quick scan; project website liushiliushi.github.io/learn2play-bench-website/ (verify).

## Source

- Raw: `raw/research/weekly-2026-10-11/04-learn2play-bench.md`
- arXiv: https://arxiv.org/abs/2610.08215
- Captured: 2026-10-11

## Related

- [[conflicts/verbatim-vs-extracted-memory]] - new evidence for the verbatim side in an experience-learning (not factual-recall) setting; backbone-dependent
- [[memory/memory-evolution-survey]] - Storage/Reflection/Experience tiers; higher tiers not reliably better here
- [[memory/reflexion]] - baseline; below raw MEMORY on Kimi K3 but competitive on Opus 5
- [[memory/evomembench]] - sibling benchmark for evolving memory, also splits knowledge vs execution tasks
- [[memory/groupmembench]] - BM25 over raw text beating extraction systems, a parallel result
- [[memory/agent-native-memory-system]] - verbatim storage beating extraction for factual recall
- [[evaluation/continualskillbench]] - related continual-learning benchmark
- [[evaluation/open-world-agents]] - agents in unfamiliar environments
- [[patterns/skill-distillation]] - distilled rules risk freezing incomplete evidence
- [[patterns/harness-design-space]] - same-backbone harness swaps
- [[patterns/effective-harnesses]] - flexible harness vs preset memory pipeline
- [[patterns/agentic-harness-engineering]] - harness matters at a fixed backbone
- [[patterns/harness-scaling-position]] - partial support for harness-over-model
- [[patterns/sol-pi-harness-efficiency]] - harness efficiency at a fixed model
- [[patterns/model-cost-routing]] - higher per-token price can mean lower total cost
- [[patterns/context-engineering]] - raw history vs summarized context
- [[proposals/memory-system-architecture]] - verbatim-first store; link rules to evidence
- [[deployments/claude-sonnet-5]] - largest transfer drop in this benchmark
