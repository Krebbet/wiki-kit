# PaperOrchestra (Google, 2026)

Five-agent pipeline by Yiwen Song, Yale Song, Tomas Pfister, and Jinsung Yoon (Google, arXiv 2604.05018) that takes a researcher's *existing* materials — a rough idea summary plus raw experimental logs — and produces a submission-ready LaTeX manuscript. Explicitly positioned as a fix to the limitation in autonomous research systems like [[ai-scientist-v2]]: those systems' writing modules are tightly coupled to their own internal experimental loops, so "you can't just hand them your data and expect a paper." PaperOrchestra is the standalone-writer counterpart. Reaches simulated peer-review acceptance rates of **84% on CVPR / 81% on ICLR** (vs human ground truth 86% / 94%), with ~46–48 verified citations per paper (matching the human ~59 average; competing baselines manage only 9.75–14.18). 68-page paper; what follows is structured by the primary source.

## The five-agent pipeline

Steps 2 and 3 run in parallel; the rest are sequential.

1. **Outline Agent** *(1 LLM call)* — reads idea summary, experimental log, conference template, and guidelines; outputs a structured JSON outline with three top-level keys: `plotting_plan`, `intro_related_work_plan`, `section_plan`. The intro/related-work plan **strictly separates** Introduction scope (macro-level, 10–20 papers) from Related Work scope (micro-level baselines, 30–50 papers) to prevent citation overlap. Section_plan includes citation hints for every dataset, optimiser, metric, and baseline mentioned in the materials.
2. **Plotting Agent** *(parallel; ~20–30 LLM calls)* — executes the visualisation plan via **PaperBanana** (Zhu et al. 2026, arXiv 2601.23265), an academic illustration tool that uses a Vision-Language Model critic to evaluate generated images against design objectives and iteratively revise.
3. **Literature Review Agent** *(parallel; ~20–30 LLM calls)* — two-phase citation pipeline:
   - **Discovery**: 10 concurrent workers query an LLM with Google Search grounding to identify candidate papers.
   - **Verification**: sequential Semantic Scholar API queries (1/sec rate limit) using **Levenshtein distance ratio >70%** for fuzzy title matching, with year-alignment point bonus, then abstract retrieval and metadata fetch. A **temporal cutoff** is enforced tied to conference deadlines: November 2024 for CVPR 2025, October 2024 for ICLR 2025. Citations deduplicated by Semantic Scholar paper ID.
   - **Hard prompt constraint**: **≥90% of the gathered literature pool must be actively cited** in the draft — this is where the high citation density comes from.
   - Drafts Introduction and Related Work using the verified BibTeX.
4. **Section Writing Agent** *(1 multimodal LLM call)* — sees all prior agent outputs including generated figures; authors abstract, methodology, experiments, conclusion. Extracts numeric values directly from the experimental log to construct tables; integrates figures into LaTeX source.
5. **Content Refinement Agent** *(~5–7 calls; 3-iteration loop)* — uses **AgentReview** (Jin et al., EMNLP 2024) as simulated peer-review backend. Revisions accepted only if overall AgentReview score increases or ties with net non-negative sub-axis gains. Any overall decrease triggers immediate revert and halt.

## Implementation details

- **Backbone**: Gemini-3.1-Pro for all writing (temperature 0.75 for AgentReview/quality eval; 0.0 for SxS).
- **Search**: Gemini-3-Flash with Google Search grounding for literature discovery.
- **Evaluator only** (not generation): GPT-5 (gpt-5-2025-08-07), default temperature 1.0.
- **API routing**: Vertex AI for Gemini, OpenAI API for GPT-5.
- **Anti-leakage prompt** applied uniformly to all tested pipelines (Single Agent, AI Scientist-v2, PaperOrchestra) to prevent memorisation of training data; the paper acknowledges "LLMs may not perfectly adhere to negative constraints" and treats uniform application as the fairness mitigation rather than evidence the constraint works.

## P0 / P1 citation taxonomy

The paper splits ground-truth citations into:
- **P0 (Must-Cite)**: direct baselines, datasets, metrics, foundational methods.
- **P1 (Good-to-Cite)**: supplementary background.

The key methodological move: baselines' competitive Overall F1 scores are an **artifact** of their tiny citation counts (9.75–14.18) — they happen to cite a few obvious P0 papers and that inflates precision. PaperOrchestra's contribution is breadth: **P1 Recall improvement of 12.6–13.8% over the strongest baseline**.

## PaperWritingBench

200 accepted papers from CVPR 2025 and ICLR 2025 (100 each, deliberately spanning double-column vs single-column formats). For each paper, an LLM reverse-engineers two inputs from the published PDF:

- **Sparse Idea Summary** — high-level conceptual description, no math or LaTeX (~587–591 words).
- **Dense Idea Summary** — retains formal definitions, loss functions, LaTeX equations (~1,057–1,083 words).
- **Experimental Log** — all numeric data + figure-derived factual observations.

Materials anonymised: author names, titles, citations, figure references stripped. Construction stack: MinerU for PDF→Markdown, PDFFigures 2.0 for figure/caption extraction, Gemini-3.1-Pro for reverse-engineering.

ICLR papers are denser by construction: avg 9.19 figures vs 5.20 (CVPR), 8.13 tables vs 4.20, 2,387 vs 1,530 word experimental logs.

**Sparse vs Dense ablation** (the most informative finding):
- *Overall paper quality* — Dense substantially beats Sparse (43–56% win rate vs 18–24%). Precise methodology descriptions enable rigorous section writing.
- *Literature review quality* — nearly identical (Sparse 32–40% vs Dense 28–39%). The Literature Review Agent autonomously identifies relevant citations without depending on detail-rich human input.

The implication: literature search is solvable from sparse human input; rigorous methodology writing is not.

## Quantitative results

Two distinct evaluation tracks — the wiki had previously conflated these:

**Automated side-by-side (Gemini-3.1-Pro + GPT-5 as judges, two orderings per pair to mitigate positional bias)**:
- Win rate vs AI Scientist-v2: **39–86% on overall paper quality**; **88–99% on literature review quality**.
- Win rate vs Single Agent baseline: 52–88% on overall paper quality.

**Human evaluation** (11 AI researchers, 180 paired comparisons on 40 papers / 20 per venue, custom Streamlit interface for blind comparison, 12 fine-grained diagnostic questions per evaluation before holistic judgment):
- **50–68% absolute win-rate margin on literature review**.
- **14–38% on overall manuscript quality**.
- **43% tie/win against human-written ground truth in literature synthesis** — but no comparable parity on overall quality (a quality gap remains vs human GT).

**Inter-rater correlation** between GPT-5 evaluator and human scores: Pearson 0.6458, Spearman 0.6355 for overall quality. Literature review correlation is lower due to *LLM self-bias* — LLMs reward explicit "Problem-Gap-Solution" paragraph structure; humans prefer narrative density and pragmatic factuality.

**ScholarPeer simulated acceptance** (Goyal et al. 2026, arXiv 2601.22638): 84% CVPR / 81% ICLR vs human-authored 86% / 94%. **+13% CVPR / +9% ICLR** over the strongest autonomous baseline. Note: ScholarPeer is co-authored by Yale Song, Tomas Pfister, and Jinsung Yoon — three of the four PaperOrchestra authors. The paper does not flag this as a methodological conflict; the wiki page records it as a caveat (see *Open methodological questions* below).

**Citations**: PaperOrchestra averages 47.98 (CVPR) / 45.73 (ICLR) per paper; baselines 9.75–14.18; human-written ~59. **P1 Recall improves 12.6–13.8%** over strongest baselines.

**Refinement step ablation**: removing the iterative peer-review loop drops absolute acceptance by **−19% on CVPR / −22% on ICLR**. Refined manuscripts beat unrefined drafts in **79–81%** of side-by-side comparisons with **0% losses**.

**Pipeline cost** (10-paper sample, outlier-trimmed): ~60–70 LLM calls, mean **39.6 min** per paper (vs AI Scientist-v2's ~40–45 calls and 35.1 min — comparable wall clock despite more calls).

**PlotOn vs PlotOff**: PlotOff uses human-authored figures (which embed supplementary data not in the experimental log); PlotOn generates from scratch. PlotOn wins/ties **51–66%** of side-by-side comparisons despite this **information disadvantage**. Read as "competitive despite disadvantage" not "equivalent."

## Baselines excluded (with stated reasons)

- **CycleResearcher**: requires structured BibTeX input, fails on unstructured inputs.
- **AI-Researcher**: requires structured intermediate states (pre-written sections).
- **OmniScientist**: no public codebase.
- **AutoSurvey2, LiRA**: designed for literature surveys, not full-paper generation.

## Self-documented limitations (Appendix A)

- **Figure hallucination**: relying on external PaperBanana for visual generation limits direct control. The paper acknowledges it cannot systematically verify that generated visuals are factually accurate or optimally placed in LaTeX layout.
- **No human-in-the-loop**: the refinement loop uses LLM-generated peer-review feedback only. Interactive HITL steering is explicit future work.
- **Pretraining contamination risk**: despite anonymisation and anti-leakage prompts, the risk that LLMs reconstruct memorised papers cannot be fully eliminated. Mitigation is uniform application across baselines (fairness, not validation).
- **Quality gap to human GT remains**: 43% tie/win on literature synthesis, but no parity on overall quality.

## Open methodological questions worth flagging

1. **ScholarPeer co-authorship overlap** — three of the four PaperOrchestra authors also co-author ScholarPeer, the simulated-acceptance evaluator. Not flagged as a conflict in the paper. Treat ScholarPeer numbers as one signal, not the headline.
2. **Anti-leakage prompt effectiveness** — paper notes LLMs may not adhere to negative constraints. Uniform application ensures fairness but doesn't validate the constraint works. Benchmark papers published before model training cutoffs remain a confound.
3. **PlotOn baseline asymmetry** — PlotOff has the information advantage of human-curated supplementary content; the 51–66% PlotOn result is "competitive despite disadvantage."
4. **10-paper cost sample** — latency statistics (39.6 min) are computed from only 10 papers with outlier trimming; thin sample for a variance-heavy system.

## Why it matters

- **Cleanest contrast with [[ai-scientist-v2]] in the wiki.** AI Scientist-v2 is an end-to-end research agent (idea → experiments → paper); PaperOrchestra is a standalone writer (your-data → paper). Both ship in early 2026; together they bracket the autonomous-research-agent design space.
- **Validates the multi-agent specialisation thesis.** The Single-Agent baseline (one monolithic LLM call given the same raw materials) is outperformed by 52–88% on overall quality — a concrete data point on when multi-agent decomposition adds value beyond what a single sufficiently-capable model achieves. Counter to [[skill-distillation]]'s general argument, this is a regime where the multi-agent design clearly wins.
- **Refinement Agent ablation is a strong signal for stage-discipline patterns.** Removing the iterative peer-review loop drops absolute acceptance ~20% — the same kind of "stage manager with stopping criteria" effect [[ai-scientist-v2]] documents for its four-stage experiment manager. The pattern generalises: **a second specialised agent whose only job is *catching the first agent's surface-level errors* delivers outsized quality gains**.
- **Citation-quality discipline as an empirical finding.** Competing systems hit 9–14 citations averaged; human papers ~59; PaperOrchestra ~46. The Levenshtein + Semantic Scholar verification pipeline is the cleanest documented antidote to citation hallucination in this batch of research-agent work.

## Source

- `raw/research/long-horizon-context/16-14-paperorchestra-pdf.md` — primary paper PDF (captured 2026-04-26 from https://arxiv.org/pdf/2604.05018 via marker on CPU; figures preserved in `assets/14-paperorchestra-pdf/`).
- `raw/research/long-horizon-context/09-10-paperorchestra.md` — original secondary source (marktechpost article 2026-04-08); kept for provenance though primary now supersedes.
- Project page: https://yiwen-song.github.io/paper_orchestra/

## Related

- [[ai-scientist-v2]] — the contrast-of-record: end-to-end research agent vs standalone writer.
- [[airs-bench]] — purpose-built evaluation infrastructure for autonomous research agents; complementary to PaperWritingBench.
- [[skill-distillation]] — counter-case: PaperOrchestra is a regime where multi-agent specialisation clearly wins, validating that F (Metric Freedom) is task-specific, not universal.
- [[topology-taxonomy#long-horizon-context-loss]] — the Refinement Agent is a clear instance of *materialise state in the topology* mitigation (peer-review loop as stage gate).
- [[memory-architectures]] — VLM-as-critic and AgentReview-as-gate are reflective-self-improvement memory patterns at the agent-pipeline scale.
- [[building-effective-agents]] — five-agent specialisation with parallel execution is a textbook orchestrator-workers pattern.
