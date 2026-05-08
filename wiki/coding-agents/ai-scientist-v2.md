# AI Scientist-v2 (Sakana AI, 2026)

Sakana AI's AI Scientist-v2 is an end-to-end agentic system that autonomously conducts ML research via a four-stage experiment manager and parallelized tree-search code exploration, producing the first fully AI-generated paper to pass peer review at an ICLR 2025 workshop. The system eliminates human-authored code templates entirely, generating all experiment code from abstract research ideas, and demonstrates a viable topology for autonomous research agents beyond coding-only automation.

## Mechanism

- **Template-free code generation**: v1 required human-authored baseline code templates per topic; v2 starts from abstract research ideas and generates all experiment code autonomously, with novelty checks via Semantic Scholar queries to avoid duplicating existing work.

- **Four-stage experiment manager**: A dedicated coordinator enforces sequential progression — (1) Preliminary Investigation (minimal prototype), (2) Hyperparameter Tuning (convergence across ≥2 datasets), (3) Research Agenda Execution (full hypothesis testing), (4) Ablation Studies — each with explicit stopping criteria and LLM-based node selection before advancing stages.

- **Parallelized agentic tree search**: Each node is a tuple of (experiment script, plan, error trace, metrics, figures, VLM feedback, status). Nodes are classified as buggy or non-buggy; expansion uses best-first selection for non-buggy nodes and error-directed debugging for buggy ones. Specialized node types (hyperparameter, ablation, replication, aggregation) handle stage-specific needs, and all child nodes execute concurrently.

- **VLM feedback loop**: A Vision-Language Model reviews generated figures during tree-search (marking unclear or misleading visualizations as buggy) and again during manuscript writing (checking figure-caption alignment, legend completeness, and duplication).

- **Manuscript generation**: v2 shifts from iterative Aider-based editing to single-pass generation followed by reflection using a reasoning model (o1), with automatic page-length handling.

## Evaluation

- Three fully autonomous manuscripts submitted to ICLR 2025 "I Can't Believe It's Not Better" (ICBINB) workshop under blind peer review.

- One manuscript achieved average reviewer score 6.33/10 (individual scores 6, 6, 7), placing it in top ~45% of submissions and surpassing acceptance threshold — would have been accepted if human-authored.

- The accepted paper investigated compositional regularization for LSTMs on synthetic arithmetic datasets, reporting negative results; reviewers praised transparency while requesting stronger architectural generalization and intuition.

- Authors disclosed internal quality concerns: ~57% train/test dataset overlap, misleading figure captions, terminology confusion between "embedding states" and "hidden states," and missing key citations (e.g., Hochreiter & Schmidhuber 1997).

- Workshop acceptance rates (~60–80%) substantially exceed main-track rates (~20–30%); v2 does not yet consistently reach workshop-level quality, let alone main-conference level.

- Humans selected which AI-generated ideas to run and which completed manuscript to submit (characterized as "meta-selection," not in-loop intervention on scientific content).

## Reproducibility

- Full codebase open-sourced at https://github.com/SakanaAI/AI-Scientist-v2.

- ICLR 2025 workshop experiment data and all generated papers open-sourced at https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment/.

- Submitted manuscripts (including annotated accepted paper) included in full as Appendix C — unusually transparent.

- HuggingFace Hub dataset loading is partially ad-hoc; not all repositories support `datasets.load_dataset`.

- Reproducibility of specific accepted run complicated by random seed sensitivity; paper acknowledges multiple seeds per idea with best output selected; success rate across seeds deferred to future work.

## Failure modes documented

- **Citation hallucination**: Generated manuscripts omit key citations (e.g., Hochreiter & Schmidhuert 1997) despite relevance to claimed novelty.

- **Dataset leakage**: Accepted paper had ~57% train/test overlap, undermining generalization claims.

- **Figure and caption errors**: Misleading figure captions and terminology confusion ("embedding states" vs. "hidden states") reduce clarity and rigor.

- **Short-sighted experimentation**: v1 limitation that v2's four-stage manager with stopping criteria attempts to address, but incomplete execution selection remains a risk.

## Why it matters

- **New wiki domain**: This is the most complete public demonstration of an "autonomous research agent" — a category distinct from coding agents or RAG pipelines. The four-stage experiment manager + tree-search loop opens a new topology for long-horizon scientific tasks and warrants a dedicated `autonomous-research-agents` page.

- **Topology extension**: Hierarchical two-tier structure (manager orchestrates stage boundaries; parallelized search expands within each stage) represents a novel multi-agent topology not captured by existing linear/parallel/router patterns. Concrete candidate for [[topology-taxonomy]] extension.

- **Effective-agent patterns**: VLM-as-quality-gate (classifying nodes as buggy/non-buggy based on visualization critique) and four-stage manager with explicit stopping criteria are notable agentic quality-control patterns extending [[building-effective-agents]].

- **Benchmarking signal**: Peer review acceptance as an eval signal distinct from benchmark-based evaluation; positions external review as a quality gate for autonomous scientific output.

## Source

- `raw/research/weekly-2026-04-22/04-ai-scientist-v2.md` (captured 2026-04-22 from https://arxiv.org/abs/2504.08066)

## Related

- [[topology-taxonomy]] — Hierarchical manager + parallelized tree-search within stages is a novel multi-tier topology variant.
- [[building-effective-agents]] — VLM-as-quality-gate and four-stage manager with stopping criteria are concrete effective-agent patterns.
- [[failure-modes]] — Explicit self-critique of hallucinated citations, dataset overlap, misleading figures, terminology drift, and short-sighted experimentation.
- [[benchmarks]] — Peer-review acceptance as eval signal; positions MLEBench/AIDE lineage as tree-search inspiration.
- [[reasoning-frameworks]] — Tree-search as a reasoning scaffold; contrasts rigid workflow graphs vs. loose stage structures.
- [[memory-architectures]] — Node-tuple state is a manual instance of structured agent memory; survey provides the taxonomy.
- [[context-folding]] — Adaptive in-context compression as an alternative state-materialisation strategy (single-chain retrospective vs. tree-branching planning-time).
- [[paperorchestra]] — Standalone-writer counterpart: PaperOrchestra takes researcher-supplied experimental logs and produces papers without owning the experimental loop.
- [[airs-bench]] — Purpose-built evaluation infrastructure for autonomous research agents; quantifies the human-SOTA gap (4 of 20 tasks beat SOTA).
- [[skill-distillation]] — Argues against multi-agent designs when Metric Freedom F is high; counterpoint to AI Scientist-v2's hierarchical orchestration assumption.
