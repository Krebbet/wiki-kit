# Revisions

Concise record of all wiki modifications. One row per logical change.

| Date | Action | Pages Touched | Summary |
|---|---|---|---|
| 2026-04-19 | bootstrap | CLAUDE.md, commands | Initial bootstrap: research wiki for novel single-sample concept-based LLM fine-tuning method (1–40B params) |
| 2026-04-20 | research | raw/research/single-sample-llm-learning/ | Captured 30 papers across 8 topic clusters (A–H) on single-sample / concept-based LLM learning; audit clean. |
| 2026-04-20 | ingest | wiki/research/ (9 themes, 30 per-paper pages, 8 overviews) | Synthesised 30 captured papers into 9 research themes with per-paper pages and cross-cutting theme overviews. |
| 2026-04-20 | index | wiki/index.md | Built catalogue of all 9 themes and 30 per-paper pages with theme-grouped summaries. |
| 2026-04-20 | synth | wiki/research/concept-learning/_overview.md | Wrote concept-learning theme overview manually after synth agent hit rate limit; covers CBM vs RCE. |
| 2026-04-20 | lint | theme overviews (8), data-efficient-survey, conflicts/index | Fixed broken cross-theme links (`[[theme-name]]` → `[[../theme/_overview]]`), added missing `## Source` sections to 5 overviews, created `conflicts/index.md` stub. |
| 2026-04-20 | synth | wiki/research/synthesis/single-sample-concept-skeleton.md | Editorial synthesis page composing RCE failure-trigger (P1), Balashov sparse-mask (P2), L2T Fisher-reward (P3), CAI principle-decomposition (P4) into a candidate single-sample concept fine-tuning skeleton. |
| 2026-04-20 | research | raw/research/adjacent-reward-signals/ | Captured 8 papers extending the adjacent-reward-signal threads (PAV, ReFT, PAG, Structured Fisher Optimizer, EWC-Gemma2, Prometheus 2, CRITIC, Critic-CoT). CPU marker + manual PDF download. Audit clean. |
| 2026-04-20 | ingest | wiki/research/ (8 new pages, 1 new theme dir) | Ingested 8 captures into themed wiki pages. New theme `catastrophic-forgetting/` seeded with EWC-Gemma2. Updated theme overviews for critique-self-correction, process-reward-models, single-sample-rl-finetuning, self-improvement, rlvr-mechanics. |
| 2026-04-20 | index | wiki/index.md | Added 8 new per-paper rows, new "Catastrophic forgetting (seed)" section, refreshed theme summaries. |
| 2026-04-21 | lint | wiki/research/data-efficient-survey/limited-data-ft-survey.md | Renamed `## Method taxonomy` → `## Method` and `## Key claims and findings` → `## Claims` to match research-page schema. All other lint checks clean. |
