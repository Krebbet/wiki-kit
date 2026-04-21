# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-19] bootstrap | LLM fine-tuning research wiki

Initial bootstrap. Schema and commands tailored for a research wiki supporting development of a novel fine-tuning method for small LLMs (1–40B params) emphasising single-sample, concept-based learning. Ready to receive first source.

---

## [2026-04-20] research + ingest | 30-paper single-sample / concept-based LLM learning corpus

Captured 30 papers across 8 topic clusters (labelled 01–09 for the initial core plus A–H for the secondary clusters) into `raw/research/single-sample-llm-learning/`. Audit clean — all image refs resolve, all markdowns paired with a PDF, no thin captures, no cross-paper asset collisions.

Dispatched parallel synth agents (one per theme) to write per-paper pages and theme overviews under `wiki/research/`. 9 themes emerged: single-sample-rl-finetuning, rlvr-mechanics, process-reward-models, self-improvement, critique-self-correction, in-context-learning-theory, meta-learning-few-shot, test-time-training, concept-learning, plus a data-efficient-survey holding the Szep 2024 survey.

Rate-limit interruption hit during the tail of the run. Three retry agents ("Synth: critique & self-correction", "Synth: concept learning", "Synth: single-sample RL retry 2") terminated with "You've hit your limit · resets 12pm". The first two themes already had overview pages written by earlier passes; the concept-learning theme overview was written manually from the two per-paper pages. single-sample-rl-finetuning overview also already present from an earlier agent run.

Built `wiki/index.md` as a theme-grouped catalogue of all 30 per-paper pages plus 8 theme overviews and a standalone survey page.

---

## [2026-04-20] lint | broken-link + format sweep

Ran wiki lint. Capture audit clean (0 broken image refs, 0 missing paired PDFs, 0 thin captures, 0 collisions across 30 papers). Fixed 20+ broken `[[theme-name]]` links (e.g. `[[rlvr-mechanics]]`) by rewriting to `[[../theme/_overview]]`; corrected one stale `[[rl-one-training-example]]` → `[[../single-sample-rl-finetuning/1-shot-rlvr]]`; corrected three `[[../data-efficient-survey/_overview]]` → `[[../data-efficient-survey/limited-data-ft-survey]]`. Added `## Source` sections to 5 theme overviews (critique-self-correction, meta-learning-few-shot, process-reward-models, self-improvement, test-time-training). Created `wiki/conflicts/index.md` stub so the link from `wiki/index.md` resolves. Re-ran lint: 0 broken links, 0 orphans, 0 format issues.

---

## [2026-04-20] synth | candidate method skeleton

User asked for a synthesis page composing four primitives drawn from the corpus into one candidate skeleton for a concept-based, single-sample LLM fine-tuner. Wrote `wiki/research/synthesis/single-sample-concept-skeleton.md` with the four primitives (P1 RCE failure trigger, P2 Balashov sparse mask, P3 L2T Fisher info-gain reward, P4 CAI principle decomposition), pseudocode for the on-example loop, a primitive-removal table showing why each is load-bearing, mapping to existing single-sample work (1-shot RLVR / Critique FT / RCE), and explicit gaps. Marked the page as editorial synthesis at the top per `/research` rules. Created `wiki/research/synthesis/` as the home for future cross-theme synthesis pages.

Also dispatched a research agent to find candidate sources on three adjacent reward-signal threads (self-generated process supervision, Fisher-proxy rewards, verbal critique-as-reward); shortlist returned and surfaced to user for approval.

---

## [2026-04-20] research + ingest | adjacent-reward-signals (8-paper extension)

User approved 8 candidates from the shortlist: PAV (Setlur 2024), ReFT (Luong 2024), PAG / Multi-Turn Policy-Verifier (Jiang 2025), Structured Fisher LLM Optimizer (Gong 2025), EWC for Gemma2 (Šliogeris 2025), Prometheus 2 (Kim 2024), CRITIC (Gao 2023), Critic-CoT (Zheng 2024).

Captures: ran `tools.capture_pdf` on all 8 arXiv URLs into `raw/research/adjacent-reward-signals/`. First attempt failed with CUDA OOM (another process holding ~20 GiB on GPU 0). User instructed CPU-only — re-ran with `TORCH_DEVICE=cpu` and all 8 succeeded. Source PDFs downloaded in parallel via `curl` into `pdfs/`. Audit clean (0 broken refs, 0 missing pairs, 0 thin captures, 0 collisions).

Ingest: dispatched 3 parallel synth agents (3 critique papers, 3 PRM/RL papers, 2 Fisher/EWC papers). All returned successfully; 8 wiki pages written into `critique-self-correction/`, `process-reward-models/`, `single-sample-rl-finetuning/`, `self-improvement/`, `rlvr-mechanics/`, and a new `catastrophic-forgetting/` theme directory seeded with the EWC paper.

Refreshed theme overviews to list the new papers in their `## Papers` and `## Source` sections. Updated `wiki/index.md` with 8 new per-paper rows and a new "Catastrophic forgetting (seed)" section. Added `structured-fisher-llm-optimizer.pdf` to `rlvr-mechanics/_overview.md` Source PDFs.

---

## [2026-04-21] lint | schema compliance sweep

Full lint pass. Capture audit clean on both raw dirs (30 + 8 papers, 0 issues). 0 orphans, 0 real broken links (scanner hits in `log.md`/`revisions.md`/`CLAUDE.md` are prose descriptions of past rewrites and placeholder syntax, not references). 0 stale markers. 0 open conflicts. 1 real format issue: `limited-data-ft-survey.md` used `## Method taxonomy` and `## Key claims and findings` instead of the canonical `## Method` / `## Claims`. Renamed both headings; no anchor links depended on the old names. Post-fix format check passes on all 49 research pages.
