# Context folding (AgentFold)

ICLR 2026 Poster from Shanghai Jiao Tong + Alibaba Tongyi Lab proposing **proactive context folding** as a third path between two failure modes of long-horizon agents: ReAct-style trajectories that accumulate raw reasoning–action–observation triplets until context saturates, and uniform summarisers that compress at every step and irreversibly lose detail. AgentFold treats the context window as "a dynamic cognitive workspace to be actively sculpted, rather than a passive log to be filled" — at every step the agent emits a folding directive concurrently with the tool call, choosing variable-granularity compression based on task state. The 30B-parameter model (`AgentFold-30B-A3B`, fine-tuned from Qwen3-30B) reaches **36.2% on BrowseComp** and **47.3% on BrowseComp-ZH** — surpassing or matching DeepSeek-V3.1-671B, GLM-4.5-355B, and OpenAI's o4-mini, while keeping context to **~7k tokens after 100 turns** and scaling to 500+ turns within a 128k window.

## The two folding modes

At each step the agent generates the quadruplet `(thinking, folding, explanation, tool_call)`. The folding directive is a JSON object `{"range": [k, t-1], "summary": "σ"}` — emitted in the same forward pass as the tool call, not a post-hoc compression.

- **Granular condensation** — agent sets `k = t-1`. Folds *only* the Latest Interaction into a fine-grained summary block: `[Compressed Step 5] Found candidate XYZ for further exploration`. Earlier State Summaries untouched. KV cache for steps `1..t-2` is fully reusable.
- **Deep consolidation** — agent sets `k < t-1`. Folds the Latest Interaction together with a chain of prior summary blocks into one coarse-grained block: `[Compressed Step 5 to 9] Confirmed XYZ does not fit criteria after checking several sources`. Used when a sub-task is complete and intermediate procedural detail is no longer decision-relevant. KV cache invalidated for the merged range, but total context shrinks, lowering the memory floor for subsequent steps.

There are no hyperparameters governing when or how to fold — the agent decides autonomously every step.

## Multi-scale state representation

Context at step `t`: `Ct = (Q, T, S_{t-2}, I_{t-1})` where:
- `Q` — invariant question.
- `T` — tool schema.
- `S_{t-2}` — ordered sequence of summary blocks `(s_{x1,y1}, ..., s_{xm,ym})` covering all history prior to the latest interaction.
- `I_{t-1}` — full verbatim record of the immediately preceding step.

The partition is the design contribution: **long-term curated memory** (variable-granularity State Summaries) plus **volatile high-fidelity working memory** (Latest Interaction). This is closer to *adaptive intra-task curation* than fixed-window sliding summarisation (MEM1, MemAgent).

## Training pipeline

- **Fold-Generator** — GLM-4.5 and DeepSeek-V3.1 (~50/50) used as teachers to generate trajectories. Qwen3-30B-A3B used internally for HTML interpretation during browsing.
- **Question set** — same as WebSailor (prior Alibaba work), enabling fair comparison.
- **Rejection sampling** — discards steps with JSON format errors, unexpected tool args, or incorrect endings; downsamples trajectories with <10 tool calls.
- **Volume** — ~30k generated trajectories, ~20k retained.
- **Fine-tuning** — standard SFT on Qwen3-30B-A3B-Instruct. **No RL** in this paper — flagged as next step.

The distillation claim: AgentFold-30B beats both teacher models (DeepSeek 30.0%, GLM 26.4% on BrowseComp), arguing that the folding mechanism — not just better training data — drives the gain.

## Quantitative results

| Benchmark | AgentFold-30B-A3B | DeepSeek-V3.1-671B | GLM-4.5-355B | OpenAI o4-mini |
|---|---|---|---|---|
| BrowseComp | **36.2%** | 30.0% | 26.4% | 28.3% |
| BrowseComp-ZH | 47.3% | 49.2% | 37.5% | 44.3% |
| WideSearch (ItemF1) | **62.1%** | — | — | — |
| GAIA (text-only) | **67.0%** | 63.1% | 66.0% | — |

**Context efficiency:** at turn 100, ~7k tokens average (from ~3.5k at turn 1) — sub-linear growth. ReAct baseline at the same point: ~84k tokens larger (92% reduction). GLM-4.5-355B saturates beyond 64 turns; AgentFold continues improving to 256 turns. Authors claim 500+ turn capacity within 128k window. Folding overhead: 5.39% of total output tokens (vs 92.6% for thinking).

**Ablation on motivation block:** removing motivation → 26.3%; replacing motivation with thinking → 33.5%; full AgentFold → 36.7%. The motivation block (explaining *why* this fold) is load-bearing.

## Limitations

- **KV-cache invalidation under Deep Consolidation** — Area Chair raised this: paper does not provide wall-clock comparisons against an optimised vLLM-cached ReAct baseline. Authors argue total context reduction compensates; remains empirically unvalidated.
- **Fold overhead** — only token-ratio analysis, no wall-clock numbers.
- **Text-only web agents** — evaluation limited to BrowseComp, BrowseComp-ZH, WideSearch, GAIA. No image-based web automation (Online-Mind2Web, WebArena) tested; resource cost cited.
- **Fold-Generator details under-specified** — prompts, rejection-sampling criteria, training-data composition only partially in main text.
- **SFT only** — RL for discovering optimal folding policies is the natural next step.
- **Interpretability of fold triggers** — when/why the model chooses Granular vs Deep is opaque; future work.

## Why it matters

- **Concrete mitigation pattern for long-horizon context loss.** [[topology-taxonomy#long-horizon-context-loss]] names the failure; AgentFold is the cleanest published instance of *adaptive in-context compression* as a defence — and the empirical results demonstrate it works at non-trivial scale (500+ turns, sub-linear token growth).
- **Direct instance of the context-resident compression family.** The [[memory-architectures]] survey categorises this as one of the five mechanism families; AgentFold is a 2026 datapoint showing that *variable-granularity* compression closes much of the recall-vs-use gap that uniform summarisation leaves on the table.
- **Complementary to the AI Scientist-v2 node-tuple pattern.** [[ai-scientist-v2]] materialises context as tree nodes (planning-time, branching topology); AgentFold materialises context as folded summary blocks (retrospective, single-chain topology). Both attack context saturation, with different assumptions about task structure.

## Source

- `raw/research/long-horizon-context/04-04-agentfold.md` — OpenReview page, abstract, decision, reviewer comments.
- `raw/research/long-horizon-context/11-06-agentfold-pdf.md` — full PDF (captured 2026-04-25 from https://openreview.net/pdf?id=IuZoTgsUws via marker on CPU; figures preserved in `assets/06-agentfold-pdf/`).
- Code: github.com/Alibaba-NLP/DeepResearch
- Model: modelscope.cn/models/iic/AgentFold-30B-A3B-Preview

## Related

- [[memory-architectures]] — context-resident compression family; AgentFold is a 2026 instance.
- [[context-engineering]] — *intra-task context curation* (AgentFold's term) is the management bucket of the broader six-component framework.
- [[topology-taxonomy#long-horizon-context-loss]] — failure mode this pattern addresses.
- [[ai-scientist-v2]] — different state-materialisation strategy (tree nodes vs folded chain).
- [[codified-context]] — different memory tier (tiered hot/cold external) for the same long-horizon problem.
