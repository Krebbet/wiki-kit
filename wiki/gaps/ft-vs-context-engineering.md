# Remaining Gaps — Fine-Tuning vs Context Engineering

**Status update (2026-04-22):** The original gap from the first research run is substantially answered by the April 2026 `fine-tuning-vs-context-slms` research run. See [[fine-tuning-vs-context-engineering]] for the decision framework and [[slm-agents]] / [[agentic-context-engineering]] for the underlying architectures.

This page now tracks the **remaining sub-questions** the research did not close.

## Still open

- **Absolute-dollar figures** for FT vs context at production workload volumes. The sources give *ratios* (NVIDIA's 10–30× cheaper, ACE's 83.6% token-cost reduction) but no dollar-per-conversation figures at scale.
- **Production case studies at named companies** with measured outcomes. NVIDIA cites customer anecdotes without naming them; the surveys don't either.
- **Practitioner takes** from Eugene Yan, Hamel Husain, Chip Huyen, and Shreya Shankar directly on the FT-vs-RAG axis. Not surfaced by the April 2026 queries; worth a targeted search.
- **Long-context vs fine-tuning head-to-head** on a common workload with cost, latency, and accuracy triaged together. Both surveys mention the tradeoff but do not measure it jointly.
- **When context engineering is actively harmful.** ACE notes tasks where detailed contexts are redundant or noise-accumulating; the broader characterization is underexplored.
- **Ablations of the composed stack.** The SLM-first + LLM-fallback + ACE composition is proposed; no single source ablates it end-to-end.

## Suggested next research runs

- *`/research Eugene Yan Hamel fine-tuning RAG practitioner`* — closes the named-practitioner gap.
- *`/research long-context vs fine-tuning benchmark 2026`* — closes the head-to-head gap.
- *`/research production case studies SLM agent 2026`* — catches named-company deployments. **Queued by the user as the next run after this ingest.**

## Source

No new raw sources on this page. Aggregates remaining gaps from the `fine-tuning-vs-context-slms` run; see [[fine-tuning-vs-context-engineering]] for the substantive answers and source trail.

## Related

- [[fine-tuning-vs-context-engineering]]
- [[slm-agents]]
- [[agentic-context-engineering]]
- [[context-engineering]]
