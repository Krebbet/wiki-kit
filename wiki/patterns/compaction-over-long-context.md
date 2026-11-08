# Compaction over Long Context ("You don't need long context")

An NVIDIA technical report (arXiv 2611.05306, Belcak, Muralidharan, ..., Molchanov; submitted 2026-11-03) argues that frequent compaction lets frontier language models keep short contexts across a broad range of long-horizon and long-input tasks with little to no loss of task accuracy, while avoiding the rising cost of late-position tokens. The authors conclude that their findings "question the need for long-context language models."

## Mechanisms and numbers

- **Cost asymmetry:** later tokens are costlier to generate than earlier ones; on frontier open-weight models the disparity may reach up to 7x. Short contexts therefore reduce per-token cost.
- **Frequent compaction:** keep the working context short by compacting often; accuracy loss reported as "little to no" across long-horizon and long-input tasks.
- **Extreme case:** on long-horizon software-engineering tasks, performance does not collapse even when the model takes at most one action per context.
- **Semantic state space models (SSSMs):** the authors outline this concept, an LLM-level analogue of a recurrent state passed between short contexts, as the architectural implication.

## Authority and limits

arXiv preprint, vendor-affiliated (NVIDIA), not peer reviewed: collect-but-confirm. The captured source is only the arXiv abstract page, so tasks, models, compaction method, baselines and accuracy figures are unknown. Re-ingest from the full text (arxiv.org/html/2611.05306v1) before citing numbers. No conflict with existing wiki claims was found; it is consistent with the short-context emphasis of [[patterns/context-folding]].

## Source

- raw/research/weekly-2026-11-08/02-no-long-context.md (summary: raw/research/weekly-2026-11-08/.ingest/02-no-long-context.summary.md)

## Related

- [[patterns/context-folding]] — learned folding holds ~7k tokens after 100 turns; same short-context thesis.
- [[patterns/self-gc-context]] — agent-managed context pruning.
- [[patterns/anthropic-context-engineering]] — compaction as a long-horizon technique.
- [[patterns/context-engineering]] — broader context-management framing.
