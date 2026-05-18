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

---

## [2026-04-21] query | methods to explore for single-sample learning

User asked for a survey of methods worth exploring to form the single-sample concept-based fine-tuning idea. Answered from the corpus organised around the existing `[[synthesis/single-sample-concept-skeleton]]`: Tier 1 primitives already in the corpus (1-shot RLVR / CFT / ReFT / RCE / CBM / Balashov / L2T / GRPO / CAI / Self-Refine / DOTS / PAV); Tier 2 adjacent frames (ICL-as-GD, induction heads, Bayesian-ICL, function-class ICL, MAML/ProtoNets/Yu, TTT, AD, EWC, PAG, STaR/rStar-Math); Tier 3 gaps the skeleton explicitly flags (forgetting under 1-sample edits, cheap mask discovery, principle self-extraction, small-G info-gain, dense-reward composability, MDL validation pool).

Identified cross-reference gap: the synthesis skeleton composes primitives from four themes but none of those theme overviews linked back to it. Added `[[../synthesis/single-sample-concept-skeleton]]` to the `## Related` sections of `single-sample-rl-finetuning/_overview.md`, `rlvr-mechanics/_overview.md`, `concept-learning/_overview.md`, and `critique-self-correction/_overview.md`.

---

## [2026-04-21] query | textbook + repeated-exercises learning algorithm

Follow-up query describing a specific design: repeat comprehensive worked examples, inject per-iteration diversity, keep reference material (e.g. a textbook) available during the loop, test concept-understanding not memorisation, scale down to very small sample sets. Mapped user's five requirements onto corpus primitives via a comparison table (repetition → 1-shot RLVR/CFT/ReFT; diversity → entropy loss / DOTS / CAI / SELF-REFINE / Reflexion; reference-in-context → Algorithm Distillation + Bayesian-ICL but **no weight-updating method**; concept-vs-pattern → RCE MDL / CBM intervention / CoT-Pass@K / step PRM; stopping → L2T info-gain / cross-category transfer / MDL-delta).

Identified three new gaps the query surfaced (not previously captured on the synthesis skeleton page): (1) reference-material-in-context during weight updates — no corpus method fits; (2) small-curriculum band N≈10–100 between single-shot and training-scale; (3) LLM-side math concept probing (RCE/CBM are vision-first, RCE's LLM numbers projected). Recorded these as new §Gaps entries on `single-sample-concept-skeleton.md` and added four matching `/research` capture priorities (retrieval-augmented / long-context FT; curriculum & textbook synthesis; reference-grounded RL; LLM math concept probing).

---

## [2026-04-21] research + ingest | teacher-student RL theme (7 papers)

User asked for the paper they'd read where a teacher model is optimised to produce reasoning traces such that another model predicts the correct answer using the trace. Identified Sakana RLT (Cetin, Zhao, Tang 2025, arXiv:2506.08388) as the exact match. Presented shortlist of 7 papers spanning the vein: Fan et al. "Learning to Teach" (ICLR 2018) as the canonical pre-LLM ancestor; Saha, Hase, Bansal "Can Language Models Teach Weaker Agents" (NeurIPS 2023) as the inference-time LLM predecessor; Ho et al. "Large Language Models Are Reasoning Teachers" (ACL 2023) as the classical distillation baseline; TRICE (Phan, Hoffman et al., NeurIPS 2023) as the probabilistic latent-variable reframing; SOAR (Sundaram et al., MIT/Meta FAIR 2026) as the bilevel meta-RL variant; PM4GRPO (Lee et al., Jan 2026) as the student-side process-mining reward. User approved all 7.

Captures: ran `tools.capture_pdf` on all 7 arXiv / ACL URLs into `raw/research/teacher-student-reasoning-rl/`. CPU-only (`TORCH_DEVICE=cpu`) to avoid the CUDA OOM pattern observed in prior runs. All 7 completed successfully in parallel (marker engine); audit clean — 0 broken image refs, 0 missing paired PDFs, 0 thin captures, 0 collisions.

Ingest: created new theme directory `wiki/research/teacher-student-rl/` with 7 per-paper pages plus a theme overview. The overview synthesises four cross-cutting axes: (a) action space (data/curriculum vs rationale/explanation), (b) student feedback signal (validation accuracy / per-token log-prob / improvement delta / trace alignment / downstream accuracy), (c) whether the teacher is trained or frozen, (d) whether the teacher's prompt sees the ground-truth answer. Also noted that none of these methods directly tests concept-installed-vs-pattern-matched and that no paper composes SOAR-style curriculum generation with RLT-style per-problem explanation.

Updated `wiki/index.md` with a new theme row + full section listing the 7 pages.

---

## [2026-04-22] synth | proposed-method implementation roadmap

User asked for a summary article outlining components, flow, and pre-implementation reading list for the method they are designing. Wrote `wiki/research/synthesis/proposed-method.md` — sibling to `single-sample-concept-skeleton.md` but implementation-oriented rather than primitive-focused.

Components documented: **R** (Sakana RLT $r^{SS} - \lambda r^{KL}$ as the gradient-of-record — replaces the skeleton's L2T info-gain P3 because the textbook supplies ground-truth solutions), **P1** (RCE failure trigger), **P2** (Balashov sparse mask), **P4** (CAI principle decomposition, optional), **C** (reference-text-in-context — the novel piece with no corpus method fitting cleanly), **V** (RCE MDL test on held-out siblings), **F** (EWC Fisher anchor), **S** (L2T info-gain as stopping diagnostic), **G** (entropy + group size diversity injection).

Flow: one-time setup (EWC Fisher, Balashov mask, freeze student + base), per-exercise loop (trigger → G rollouts → RLT reward → GRPO advantage → masked + KL-leashed + EWC-anchored step → MDL sibling validation → stopping check).

Reading list: Tier 1 (7 must-read — Sakana RLT, GRPO, 1-shot RLVR, RCE, Balashov, EWC-Gemma2, skeleton), Tier 2 (5 before extending — SOAR, L2T, CFT-one-problem, CAI, TRICE), Tier 3 (3 theory — Bayesian-ICL, ICL-as-GD, RLVR-incentivizes-reasoning). Known gaps explicitly enumerated: cheap mask-discovery, small-G variance, sibling-set construction, reference-in-context-during-RL unmeasured, student-choice instability, LLM-math concept-probe metric, exercise ordering.

Updated `revisions.md` and `index.md`.

---

## [2026-04-23] query | RLTTTS summary accuracy-check

User submitted a plain-English summary of Sakana RLT asking for gap-filling. Verified against existing `wiki/research/teacher-student-rl/sakana-rlt.md`; summary was mostly correct but missed three non-trivial details: (1) the student does NOT answer the question during training — it is scored on log-prob of the given solution; (2) the reward has a KL regulariser preventing the teacher from leaking the solution; (3) the student is frozen during teacher training. No wiki update warranted — all content already present.

---

## [2026-04-23] research + ingest | RLT follow-ups and adoption 2025-Q4 → 2026-Q2

Captured 6 sources in `raw/research/rlt-followups/`: Kwiatkowski likelihood rewards (arXiv:2602.03979, Meta FAIR + UvA), ExGRPO (arXiv:2603.19266, ASU/UVA/UNC), *Rethinking On-Policy Distillation* (arXiv:2604.13016, Tsinghua et al., April 2026), OPSD (arXiv:2601.18734, UCLA/HKU/Meta), Thinking Machines Lab *On-Policy Distillation* blog (Oct 2025), Amy Sheng *OPD Research Survey 2026* (Feb 2026). Audit: 5 broken figure refs in 2 PDFs (pymupdf extraction misses) — text content intact. No retry since pages are text-synthesis only.

Created one new wiki page: `wiki/research/teacher-student-rl/rlt-followups-2026.md` — landscape synthesis with per-source traceable summaries, commercial-adoption signals (Qwen3/MiMo/GLM-5/Thinking Machines via OPD, not RLT), and cross-source themes. Updated `sakana-rlt.md` with a `## Follow-ups and adoption` section and added the new page to Related. Updated theme overview with a landscape-note bullet.

**Key finding: none of the captured 2025-Q4–2026-Q2 sources directly cites Sakana RLT (2506.08388).** Grep confirmed zero hits for "Sakana"/"Cetin"/"2506.08388"/"RLT" across the captured files. The dense-teacher-signal paradigm is advancing via OPD and self-distillation-with-privileged-info (OPSD, SDFT, SDPO, G-OPD) rather than via RLT's reference-in-prompt framing. RLT remains a paradigmatic peer rather than a cited ancestor.

---

## [2026-04-23] query | 1-shot RLVR variance clarification

User asked what "variance" means in the 1-shot RLVR paper. Answered from existing wiki pages: it's the *historical variance of per-epoch training accuracy* used as a selection heuristic, and its effectiveness traces to [[research/single-sample-rl-finetuning/data-efficiency-rft]] Theorem 1 on within-group reward variance $p(1-p)$. Added a one-line bridge on `1-shot-rlvr.md` connecting the two concepts and noting the full-pool 500-step calibration caveat.

---

## [2026-04-23] research + ingest | RL optimisers complete picture (PPO/DPO/GRPO family)

User asked for complete coverage of GRPO, DPO, PPO, and complementary methods. Wiki already covered GRPO via `deepseekmath-grpo.md`. Captured 8 additional canonical papers to `raw/research/rl-optimizers/`: PPO (Schulman 2017, 1707.06347), InstructGPT (Ouyang 2022, 2203.02155), DPO (Rafailov 2023, 2305.18290), RLOO/Back-to-Basics (Ahmadian 2024, 2402.14740), KTO (Ethayarajh 2024, 2402.01306), DAPO (ByteDance 2025, 2503.14476), Dr. GRPO/R1-Zero-critique (Liu 2025, 2503.20783), GSPO (Alibaba Qwen 2025, 2507.18071).

Audit flagged 20 broken figure references across 5 PDFs — pymupdf figure-extraction misses. Text content intact in all 8 captures. Acceptable for text synthesis.

**Path-nesting bug encountered and fixed.** An earlier failed `cd raw/research/rlt-followups` left my shell CWD inside that subdirectory; subsequent `mkdir -p raw/research/rl-optimizers` and `capture_pdf` commands therefore created files under `raw/research/rlt-followups/raw/research/rl-optimizers/`. Fixed by `mv` to the correct path after capture. Four of the sub-agent-generated wiki pages initially contained the nested raw-path in their `## Source` sections; fixed by `sed` replace. This is a general working-directory-drift hazard worth flagging.

Dispatched 8 parallel sub-agents (sonnet), one per paper, to produce per-paper wiki pages following the `sakana-rlt.md` template. All 8 completed successfully. Wrote the theme overview (`_overview.md`) from captured content — family tree diagram, method-comparison tables keyed on (importance-sampling × baseline × KL placement × distinctive move) and sample-efficiency, cross-cutting synthesis (critic-free convergence, IS unsettled axis, KL-placement split, length-bias convergent finding from DAPO/Dr. GRPO/GSPO, preference-vs-RLVR subtree).

**Surface-level open contradiction:** [[research/rl-optimizers/dpo]] reports PPO failing to beat Pythia-2.8B base on HH while DPO wins; [[research/rl-optimizers/rloo]] reports RLOO beating both PPO and DPO across TL;DR and HH. The two papers disagree about DPO's performance. Resolving this requires close reading of experimental protocols (base model, RM, KL budget); not attempted in this pass.

Master-notes entry planned: working-directory drift from failed `cd` into capture tooling is a recurring foot-gun — capture scripts should probably resolve `--out` relative to a fixed repo-root rather than CWD, or at least print the absolute resolved output path on success. Will log to `master_notes.md` with scope: kit.

---

## [2026-04-23] synth | concept-curriculum-method (third method proposal)

User sketched a new method idea in conversation: a hierarchical concept-curriculum approach where a strong teacher model decomposes a goal topic into a concept DAG, materialises (Q, E, A, textbook) packets per concept, and a small student is trained bottom-up with a test-fail-train loop per node. Captured and elaborated as `wiki/research/synthesis/concept-curriculum-method.md`.

Structured the page as: roles table (teacher/student axes), detailed step (a)–(f) breakdown, per-step strengths/weaknesses/unknowns/challenges, overall assessment, and a comparison table against [[research/synthesis/single-sample-concept-skeleton]] and [[research/synthesis/proposed-method]]. Final section lists five open questions the project must answer to turn the sketch into an implementation plan — most critical: is this a competing method to [[research/synthesis/proposed-method]] or do they compose (curriculum outer loop, single-sample RLT inner loop)?

Key editorial observation flagged to the user in the page: **this proposal is the most teacher-heavy and the least single-sample of the three method pages**. The project's stated goal is "single-sample, concept-based learning" ([[wiki/index]]). This curriculum proposal is arguably concept-based but not single-sample. A scope decision is surfaced in the page's open-questions section.

Catastrophic forgetting explicitly flagged by the user; traced in the page to candidate counters from the corpus ([[research/catastrophic-forgetting/ewc-gemma2-cpt]] Fisher-weighted EWC anchor, [[research/rlvr-mechanics/rl-sparse-subnetwork]] Balashov sparse mask), with the caveat that both are applied *once* in their source settings; repeat application across a curriculum is untested.

Updated `index.md`, `revisions.md`.

---

## [2026-04-23] weekly-brief | first run against seeded reference-sources

Manual invocation of `/weekly-brief` after setup interview. Runtime values resolved: `REPO=wiki-single-sample-learning`, `BRANCH=single-shot-training-wiki`, `RUN_DATE=2026-04-23`. Pre-existing dirty tree: none.

**Trend scan** (alphaXiv trending, HF papers, r/ML, targeted arXiv). Podcasts skipped per setup. Initial candidate pool ~10 papers; narrowed to 4 captures + 5 surplus not auto-promoted (per interview's no-auto-seed watchlist rule).

**Captures (4):** MCPO (arXiv:2604.16972, April 18), KnowRL (arXiv:2604.12627, April 2026), CBRL (arXiv:2603.18953, March 19), MASPO (arXiv:2602.17550, Feb 2026). Audit: 11 broken figure refs from pymupdf; text intact.

**Ingest via subagent-per-source:** 4 parallel `general-purpose` agents wrote `.ingest/*.summary.md`. Aggregated via `tools.ingest_plan.aggregate`; `run.json` persisted. Autonomous page plan: MCPO → `rl-optimizers/mcpo`, MASPO → `rl-optimizers/maspo`, KnowRL → `teacher-student-rl/knowrl`, CBRL → `single-sample-rl-finetuning/cbrl`. 4 more parallel agents wrote full wiki pages from the summaries + raw sources.

**Three conflicts surfaced** (strong, from the summaries' `## Conflict flags`):
1. MCPO vs Dr. GRPO — std-removal alone doesn't kill the $p(1-p)$ weight residual.
2. MCPO vs DAPO — Dynamic Sampling discards mastered prompts, which MCPO shows causes ~5% regression.
3. KnowRL vs Sakana RLT — minimal-sufficient hints + no KL vs maximal context + plausibility regularisation.

Conflict files written to `wiki/conflicts/`; `conflicts/index.md` updated.

**Brief composed** at `/tmp/weekly-brief-2026-04-23.md` and `wiki/weekly-briefs/2026-04-23.md`. Per local convention, empty sections are omitted — no "Other watchlist references" section (watchlist was empty at start of run). Every trend bullet includes explicit thesis-relevance clause.

**Delivery:** HTML rendered via `tools/render_brief_html.py` (needed to `pip install markdown` — the package was declared in pyproject but not actually installed in the venv; small kit-level gap). SMTP send succeeded; Message-ID `<aef351ce-077e-4413-ba50-ebb5743593a4@gmail.com>` delivered to `david.hugh.mcnamee@outlook.com`. Telegram ping delivered (message_id 85).

**Not committed** per skill policy — 12 uncommitted files await user commit on next login.

Kit-level gap worth flagging: per-wiki poetry environment may not have `markdown` installed even when `pyproject.toml` declares it; fresh clones likely need `poetry install` before first weekly-brief run. Worth adding to skill preflight or the first-run guard.

---

## 2026-04-28 — Recursive Concept Learning (RCL) synthesis page + concept-understanding-eval research run

**Synthesis.** New page `wiki/research/synthesis/recursive-concept-learning.md` — fourth method proposal. Captures and refines the failure-driven interactive DAG expansion variant from concept-curriculum-method into a standalone method:

- Algorithm with `Identity(c)` cycle protection, `MAX_DEPTH` termination, children-pass-parent-fail direct-train fallback, snapshot/rollback on inner-loop failure.
- Three teacher roles separated: Decomposer M, Evaluator V, Trainer B. A1 deliverable = verifier independence.
- 13 components (E1–3 evaluation, D1–2 decomposition, T1–4 training/forgetting, R1 retest branch, G1–2 budget/compositional retest, A1 verifier independence) with per-component failure modes.
- 15 numbered gaps split across "inherited from variant" and "new to RCL framing".
- 13-row deliverables table; 4-tier 27-entry research roadmap including the captured-but-pending concept-understanding-eval batch (Tier 3) and a Tier 4 list of corpus-external topics (knowledge tracing, prereq graphs, HRL, curriculum theory, compositional benchmarks, concept identity).

§Variant in concept-curriculum-method marked as elevated to RCL with a forward link, content preserved for context.

**Research run (in flight).** Background agent dispatched to capture 9 arXiv sources into `raw/research/concept-understanding-eval/`: GSM-Symbolic, MATH-Perturb, Counterfactual Tasks, Skill-Mix, CheckList, Contrast Sets, Causal Abstraction, Hewitt&Liang Control Tasks, Embers of Autoregression. Audit + fallback handling delegated to the agent. Ingest pending agent completion.

---

## 2026-04-28 — concept-evaluation theme: 9 papers ingested

**Phase transitions completed.** Captures (re-run with direct PDF URLs after first run grabbed abstract pages only) → 9 pymupdf summaries → 9 wiki pages + theme `_overview.md`. Total 10 new pages in `wiki/research/concept-evaluation/`.

**Theme synthesis (5 evaluation modalities):** symbolic perturbation (GSM-Symbolic, MATH-Perturb), counterfactual variation (Counterfactual Tasks), local-boundary contrast (Contrast Sets, CheckList INV/DIR), compositional combination (Skill-Mix), internal-representation probe (Hewitt&Liang selectivity, Causal Abstraction IIA), with Embers of Autoregression as cross-cutting diagnostic prior.

**Wiki integration:**
- `wiki/index.md` — new theme row + 10-row pages-by-theme table
- `wiki/research/synthesis/proposed-method.md` — gaps #3 and #6 updated with concrete corpus answers (gap #3 closed by contrast-sets)
- `wiki/research/synthesis/recursive-concept-learning.md` — Phase-0 workstream-B references corrected to point at `../concept-evaluation/`; Tier-3 reading list re-anchored; "(pending ingest)" markers removed
- Per-paper Related sections include backlinks to RCL **E1** (eval battery axis), proposed-method gaps where applicable, concept-learning theme cross-refs, sibling papers within the theme

**Capture-side note worth flagging.** marker engine fell back to pymupdf because weasyprint is not in the env. Text extraction is solid; image refs are 47 broken (cosmetic). Should log to master_notes.md as Scope: kit — the kit's `tools/capture_pdf.py` should either install weasyprint via poetry, or detect-and-skip marker when the dep is missing rather than silently degrading to abstract-page scrape on the *first* attempt (which is what happened in the initial agent run before redirecting to the direct PDF URL). Marking as todo for next /harvest pass.

---

## 2026-04-29 — curriculum-and-decomposition theme: 9 RCL-gap-filler papers ingested

**Phase transitions completed.** Captures (direct PDF URLs + pymupdf, building on the lesson logged 2026-04-28) → 9 ingest summaries → 9 wiki pages + theme `_overview.md` under `wiki/research/curriculum-and-decomposition/`.

**Theme synthesis (4 sub-fields):**
- Knowledge tracing — DKT (Piech 2015), Auto-KC-generation (2025)
- Prereq-graph learning — LectureBank (Li et al. 2018), PREREQ (Lawrence et al. 2019)
- Hierarchical RL — Sutton-Precup-Singh options framework (AIJ 1999)
- Curriculum learning — Bengio canon (ICML 2009), Soviany IJCV 2022 survey, Portelas ACL DRL 2020 survey, POET (Wang Lehman Clune Stanley 2019)

**RCL gap-closures:**
- **D1** (Decompose) — auto-kc-generation is the strongest signal that LLM teacher can do diagnostic decomposition (LLM KCs beat human-written labels on KT, AUC 0.816 vs 0.797). Failure-trace-conditioned variant of D1 still untested.
- **E3** (Identity) — LectureBank + PREREQ provide concrete prereq-pair operationalisation; auto-kc-generation gives the LLM-based recipe.
- **D2** (learnability filter) — ACL DRL survey catalogues LP, ALP-GMM, teacher-student bandits as canonical filters; POET gives minimal-criterion + novelty filtering.
- **Gap #1** (curriculum-level credit assignment) — Sutton-Precup-Singh intra-option learning is the closest theoretical tool; POET transfer-attempt is the empirical analogue. Still open at LLM curricula scale.

**Wiki integration:**
- `wiki/index.md` — new theme row + 10-row pages-by-theme table
- `wiki/research/synthesis/recursive-concept-learning.md` — Components table updated with concrete corpus answers; Gap #1 updated with options-framework + POET; Tier 4 reading list rebuilt to reference the new theme; Tier 5 reduced to 2 remaining open topics
- Per-paper Related sections cross-link within the theme + to RCL components, concept-evaluation, teacher-student-rl, RCE, etc.

**Net effect on RCL design:** four "no corpus method" gaps now have concrete prior art. The remaining deepest gap is *failure-trace-conditioned* LLM decomposition — auto-kc-generation generates KCs from problem text, not from observed errors. This is the next thing to research or just empirically validate during Phase 0/1.

---

## 2026-04-30 — query: next-tier inner-loop reading list

**Question:** "I have read the first tier papers. Now looking for the next set of papers I should read to further my research. Mostly thinking about the inner loop training. Best way to set up the data set, reward signal etc."

**Answer shape:** Re-cut of the existing Tier-2/3 reading lists in `proposed-method.md` and `recursive-concept-learning.md` by *inner-loop concern* (reward signal vs dataset setup vs theoretical anchors) rather than by component (R/P1/P2/...). Same papers, different key.

**Reward-signal cluster (10 papers):** L2T info-gain, KnowRL atomic knowledge-points, PAV process advantage, Math-Shepherd auto-step labels, TACReward (PM4GRPO), TRICE marginal-LL, Critic-CoT, PAG (multi-turn-policy-verifier), Dr. GRPO, MCPO.

**Dataset-setup cluster (11 papers):** critique-FT-one-problem, Ho fine-tune-CoT, ReFT, data-efficiency-RFT (DOTS), CBRL, SOAR, Contrast Sets, GSM-Symbolic, MATH-Perturb, Counterfactual Tasks, Skill-Mix.

**Theoretical anchors:** ICL-Bayesian (per-token-info theorem → C), ICL-as-GD (rank-1 update), RLVR-incentivizes-reasoning (CoT-Pass@K diagnostic).

**Wiki update:** Added "Inner-loop reading order — alternative cut by reward vs dataset" section to `proposed-method.md`. Minimum-useful change (preferred over a new page since the underlying corpus is unchanged). No `index.md` update needed (no new pages, no summary changes).

**Open gaps the answer surfaced (already noted in proposed-method.md):**
- RLT $r^{SS}$ behaviour under long-context reference document (gap #4 — unmeasured).
- Failure-trace-conditioned LLM decomposition at curriculum scale (Tier-5 item 32 of RCL — open).

---

## 2026-04-30 — math-formatting sweep

**Trigger.** User reading wiki in Obsidian noticed that math-shaped content (e.g. `F(x) = H/(M+ε)`, `M_θ`, `θ ← θ - η·g`, `r^{SS}`) was wrapped in backticks and rendering as monospace code spans rather than typeset math. Asked for a full sweep.

**Approach.** Saved the rule as feedback memory (`feedback_math_formatting.md`); flagged the underlying issue as a kit-level concern in `master_notes.md` (ingest sub-agent prompt + a `/lint` check for backtick-wrapped TeX-suspicious spans); partitioned the 60 candidate files into 6 batches and dispatched parallel `general-purpose` sub-agents with a tight conversion spec (CONVERT rules, LEAVE rules, ASCII→LaTeX table, fenced-block exclusion, judgment guidance for multi-letter superscripts via `\text{...}`, display-equation promotion to `$$...$$`).

**Coverage.** Roughly 30 pages modified across:
- Synthesis: `single-sample-concept-skeleton.md` (~12), `proposed-method.md` (already in `$...$`), `concept-curriculum-method.md` (clean), `recursive-concept-learning.md` (clean — just `Evaluate → Train → Re-evaluate` flow notation kept as code).
- RLVR mechanics: `deepseekmath-grpo.md` (~25; GRPO objective promoted to `$$...$$`), `learning-to-think.md` (~10; process-reward formula promoted to `$$...$$`), `_overview.md`, `rl-sparse-subnetwork.md` (~12).
- Concept learning: `concept-bottleneck-models.md` (~20), `_overview.md` (~12), `recursive-concept-evolution.md` (~30).
- ICL theory: all four pages (~5–7 each).
- Process-reward, self-improvement, curriculum-and-decomposition, meta-learning-few-shot, critique-self-correction: 0–10 conversions per page.
- Concept-evaluation, conflicts/, weekly-briefs/, log.md, revisions.md: spot fixes; most already in `$...$`.

**Judgment calls (consistent across batches).**
- File paths, shell commands, Python identifiers, HTML/XML literals (`<think>...</think>`, `<question, solution>`), markdown header literals (`## Hint`), pseudocode function-call references (`Evaluate(S, c)`, `LearnConcept(p)`, `MAX_DEPTH`) — left as backtick code.
- Multi-letter superscripts (`r^{SS}`, `r_k^prg`) → `\text{...}` in superscript.
- Real-vector spaces `R^d` → `\mathbb{R}^d` only when context made it unambiguous.
- Display-line equations promoted from inline backticks to `$$...$$` blocks.
- Bare-prose unicode math (no backticks) left untouched per scope discipline — out of scope for this sweep.

**Verification.** Re-greppedfor likely math-in-backticks; remaining hits are all legitimate code (file paths, pseudocode names, HTML-tag literals, markdown-syntax literals).

**Followups for `/harvest`.** Master-notes entry promotes:
1. Rule into `tools/<wiki-kit>/templates/research-page.md` (or the ingest orchestrator prompt).
2. New `/lint` check: backtick spans containing `^`, `_`, Greek letters, math arrows, etc. flagged as likely-math.

**Wiki updates:** `revisions.md` row appended.

---

## 2026-04-30 — self-play theme pages (SPIN + SPPO)

Created `wiki/research/self-play/spin.md` and `wiki/research/self-play/sppo.md` from `.ingest/04-spin.md` and `.ingest/05-sppo.md`. Both pages use the canonical schema (frontmatter / citation+TL;DR / Method / Claims / Why not load-bearing / Source / Related). Relevance section renamed to "Why this is *not* load-bearing for single-sample concept learning" per upstream review-packet ruling. Index updated with theme row + per-page section. No `_overview.md` created (two pages, limited relevance; can be added if the theme grows).

## 2026-04-30 — self-play theme pages (SPELL + AlphaZero + Debate)

Created three medium-depth pages in `wiki/research/self-play/`: `spell.md`, `alphazero.md`, `debate.md`. Sources: `.ingest/11-spell.md` + `11-11-spell.md`, `.ingest/01-alphazero.md` + `01-01-alphazero.md`, `.ingest/03-debate.md` + `02-03-debate.md`. Each follows the canonical schema with math in `$...$`/`$$...$$`. Honest relevance-to-wiki assessments: SPELL is load-bearing via its role decomposition and Gaussian difficulty reward; AlphaZero is a structural template only (closed-domain, extreme sample cost); Debate is a contrast case (eval-time honesty, not train-time skill installation). Index and revisions updated.

---

## 2026-05-01 — self-play research run (consolidation)

**Trigger.** /research query: *"introducing some self-play to induce better learning... for something more conceptual the idea of self-play or maybe more accurately playing with the concept is a little less determined."*

**Captures (11 sources, all arxiv PDFs via tools.capture_pdf pymupdf).** AlphaZero (1712.01815), Asymmetric Self-Play / Sukhbaatar (1703.05407), Debate / Irving-Christiano-Amodei (1805.00899), SPIN (2401.01335), SPPO (2405.00675), SPAG (2404.10642), SQLM (2508.03682), SPICE (2510.24684), SPIRAL (2506.24119), Understanding Self-play (2510.27072), SPELL (2509.23863). All under `raw/research/self-play-concept-learning/`. Audit clean on structural checks; broken-figure-refs pattern familiar from prior pymupdf runs (text intact).

**Ingest.** 11 parallel sub-agents → structured summaries in `.ingest/`. Then 4 parallel page-write sub-agents producing 11 wiki pages tiered by relevance to the wiki's small-LLM single-sample-concept-learning frame:
- *Tier-1 (deep):* SPAG, SQLM, SPICE, Understanding-Self-play, Asymmetric Self-Play, SPIRAL.
- *Tier-2 (medium):* SPELL, AlphaZero, Debate.
- *Tier-3 (brief, "not load-bearing"):* SPIN, SPPO.

**Theme synthesis.** New _overview.md covering three subtrees, six proposer-reward shapes, role-decomposition axis, information-asymmetry axis, online-vs-offline signal axis, and the open questions the corpus does not answer (single-sample regime, reference-grounded RL with weight updates, concept identity, forgetting protection across concept episodes).

**Cross-theme synthesis.** New `wiki/research/synthesis/proposer-reward-shapes.md` — dedicated comparison table for Sukhbaatar / SOAR / SQLM / SPICE / SPELL / SPAG reward formulas, what each commits to, and where they plug into the proposed-method's components.

**Conflict.** `wiki/conflicts/invisible-leash-vs-spiral-transfer.md` (status: open). Position A is Understanding-Self-play's bound (solver only re-weights base-model probability mass); Position B is SPIRAL's +10.5% reasoning transfer from games. Compatible if "within base-model capacity" includes "non-trivially extractable", but the framings have different practical implications and the tension is best surfaced explicitly.

**Cross-theme back-edits.**
- `multi-turn-policy-verifier.md` (PAG) → forward-link to SPELL (three-role generalisation) and the new self-play overview.
- `soar-edge-of-learnability.md` (SOAR) → forward-link to SQLM (cheaper LLM analogue), Asymmetric Self-Play (pre-LLM precursor), and the proposer-reward-shapes synthesis.
- `proposed-method.md` gap §4 updated — [[../self-play/spice]] gives the structural-asymmetry alternative to RLT's $r^{KL}$ soft leakage penalty; structural-vs-soft head-to-head still open.
- `recursive-concept-learning.md` gap #1 (curriculum-level credit assignment) updated — [[../self-play/spiral]]'s RAE and [[../self-play/sqlm]]'s Goldilocks gate are new corpus anchors; both flat-curriculum, lift-to-DAG remains open.

**Headline finding for the user's "play with concept" question.** [[../self-play/understanding-self-play]] formalises the Invisible Leash: in LLM self-play, the solver only re-weights base-model probability mass; the proposer is the critical component. This means "play with a concept" reduces structurally to "what prompts the proposer to generate questions that activate the concept in the solver's existing capacity" — directly justifying [[../curriculum-and-decomposition/auto-kc-generation]] and elevating proposer-quality as the central engineering decision. [[../self-play/spice]] gives the cleanest structural template (information asymmetry); [[../self-play/sqlm]] gives the cheapest LLM-analogue (Goldilocks gate); [[../self-play/spag]] gives the strongest empirical concept-game-induces-reasoning result.

**Outstanding.** Master_notes harvest checkpoint pending — see entry below.

---

## 2026-05-01 — self-play single-sample + quality-extraction research run

**Trigger.** /research query: *"do another /research round trying to find anything in the single sample regime and quality optimization regime"*. The user had previously made three rulings (structural information asymmetry over soft penalty; quality-optimization framing for the Invisible Leash debate; self-play as a multiplier on single-sample optimization rather than a substitute for data) — saved to memory.

**Captures (8 sources).** Invisible Leash (arXiv:2507.14843), Yue RLVR-boundary (arXiv:2504.13837 — the canonical >120-cite empirical paper), AZR (arXiv:2505.03335, NeurIPS 2025), R-Zero (arXiv:2508.05004), Language Self-Play (arXiv:2509.07414), Two-Stage Dynamic View (arXiv:2510.04028), rStar (arXiv:2408.06195 — test-time multiplier predecessor of rStar-Math), Info-Gain self-play (arXiv:2603.02218). All under `raw/research/self-play-quality-extraction/`. Audit clean structurally.

**Ingest.** 8 parallel sub-agents → structured summaries in `.ingest/`. Then 3 parallel page-write sub-agents (3+3+2 split). Page-writers explicitly instructed NOT to update tracking files (per the master_notes lesson from the prior run); coordination went smoothly this time.

**Headline findings.**

1. **Invisible Leash is now formally proven AND empirically grounded.** Theorem C.1 ($\text{supp}(\pi_\theta) \subseteq \text{supp}(q)$) + Yue's pass@k inversion + 2:1–3.6:1 shrinkage:expansion ratio. SFT/DAPO contrast (positive vs negative NSCR on identical data) isolates the effect to the RLVR objective itself.

2. **Two-Stage Dynamic View resolves (refines) the Invisible-Leash conflict.** Position A is **Stage-1-scoped**, not universal. Stage 1 (exploitation): $\mathbb{E}[\Delta z_v] \propto \pi(v)$, gradient only flows to already-sampled tokens; standard GRPO traps here. Stage 2 (exploration): high-reward tokens saturate, suboptimal tokens get sampled. GRPO-N reaches Pass@256=100% with held-out entropy *exceeding* base. Training duration + entropy preservation become load-bearing hyperparameters.

3. **AZR's three reasoning modes** (deduction/abduction/induction over $(p,i,o)$ triplets) is genuinely new for the wiki — concept-mode taxonomy, not concept-prereq decomposition. +15pp OOD math from code-only training. Removing induction hurts most. [[info-gain-self-play]] quantifies why: induction epiplexity is 3–4× higher.

4. **rStar is the cleanest match for Ruling 3** ("self-play as multiplier on single-sample optimization"). 32 MCTS rollouts × 5 actions over a single $(Q,A)$ seed, frozen weights, peer-discriminator agreement-check. LLaMA2-7B GSM8K 12.51% → 63.91% **without fine-tuning**. The drop-in template for component G of the proposed method.

5. **Stabiliser presence > architectural separation.** R-Zero claims unified-model self-play collapses (Appendix D); AZR/LSP/SQLM/SPICE all run unified-model successfully. Each working method has a distinct stabiliser (mode diversity / quality reward / hard Goldilocks floor / structural asymmetry). New conflict file [[../../conflicts/unified-vs-two-model-self-play]]; resolution-candidate is stabiliser-presence-as-load-bearing-axis.

6. **Engineering test for self-play (epiplexity).** $S_{C,T}(X)$ — minimum description cost for a bounded observer. Self-play evolves only when this rises monotonically across iterations. Algorithm 1 prequential MDL audit becomes the pre-flight check before any inner-loop self-play training.

**Synthesis updates.**

- [[proposer-reward-shapes]] extended 6→9 entries (AZR asymmetric Goldilocks, R-Zero symmetric+diversity, LSP general-sum quality).
- [[proposed-method]] gap §4 closed — structural asymmetry locked per user ruling; RLT $r^{KL}$ dropped from default loss; training duration + entropy preservation now hyperparameters of record. Component G updated with epiplexity pre-flight.
- [[recursive-concept-learning]] D1 flagged with AZR three-mode decomposition as candidate for non-prereq concept partition.
- [[invisible-leash-vs-spiral-transfer]] refined (status: open, refined); SPIRAL's gains consistent with Stage-2 dynamics.

**Theme structure.** [[../research/self-play/_overview]] now organised around **four subtrees** (foundation / preference-alignment / reasoning-and-concept / RLVR-bound + zero-data), nine reward shapes, four-stabiliser axis, structural-asymmetry decision locked. Total self-play pages: 19.

**Tracking updates.** revisions.md row appended; conflicts/index.md updated; index.md theme summary refreshed + 8 new pages-by-theme rows added.

**Outstanding.** No new master_notes harvest entry warranted — page-writing sub-agents respected the "don't touch tracking" rule this time. The kit-level fix (already logged 2026-05-01) is the only outstanding harvest item.

## 2026-05-03 — weekly-brief autonomous sweep

**Window.** 7-day trend scan (2026-04-26 → 2026-05-03). Two parallel trend-scan subagents (aggregators + curators/labs) returned ~22 candidates; selection rules per `wiki/reference-sources.md` (technical novelty over volume; conflict-resolving; wiki-fit; reproducibility; multi-signal). Skipped Wang et al. arXiv:2504.20571 (already wiki'd as [[../research/single-sample-rl-finetuning/1-shot-rlvr]]). Earlier-April papers (RLSD, AsymGRPO, ThinkTwice, RAGEN-2) routed to watchlist.

**Captures (5 sources).** TEMPO (arXiv:2604.19295), SGS (arXiv:2604.20209), Co-Evolving Policy Distillation (arXiv:2604.27083), Tsallis Loss Continuum (arXiv:2604.25907), Latent-GRPO (arXiv:2604.27998). All under `raw/research/weekly-2026-05-03/`. Engine: pymupdf (avoiding marker abstract-degradation per master_notes 2026-04-28). Audit: 20 broken figure refs (figure-only PNG extraction misses) — text bodies 47–102 KB, well above abstract-only threshold. Ingest summaries validated via `tools.ingest_plan.parse_summary` (5/5 ok).

**Headline findings.**

1. **TEMPO reframes TTT-RL as EM.** Prior methods (TTRL, EMPO) are M-step-only degenerate variants; reintroducing the labelled-set E-step tightens the ELBO and unlocks scaling beyond ~100 steps. OLMO3-7B AIME24 33→51%; Qwen3-14B 42→66%. Pass@k preserved; baselines collapse. Cost: 2× compute (actor + critic) and a maintained $D_L$.

2. **SGS achieves clean plateau-escape on Lean4 with proposer fix only.** 7B beats 671B pass@4 after 200 rounds. Frozen-LLM Guide (relevance + elegance scoring) prevents Conjecturer reward-hacking collapse. Tenth proposer-reward shape (extends [[../research/synthesis/proposer-reward-shapes]] beyond the existing nine). Notably uses REINFORCE$^{1/2}$ — grouped objectives (CISPO) cause Solver entropy collapse and starve the Conjecturer; entropy preservation as Stage-2 prerequisite per [[../research/self-play/two-stage-dynamic]].

3. **CoPD is the cleanest empirical challenge to fixed-teacher MOPD orthodoxy yet.** Pilot study: top-$k$ overlap explains 79% of post-OPD gain variance ($r=0.89$). Static OPD operates at low overlap → low absorption efficiency. Alternating GRPO + mutual on-policy KL keeps overlap above 0.90 and surpasses every single-expert ceiling on Qwen3-VL-4B. Cross-link added against [[../research/teacher-student-rl/rlt-followups-2026]].

4. **Tsallis $\mathcal{J}_Q$ gives single-sample / sparse-success a mechanistic foundation.** Loss family interpolates RLVR ↔ log-marginal-likelihood via gradient amplification $P_\theta^{-q}$. Cold-start escape rates differ exponentially: $\Omega(1/p_0)$ at $q=0$ vs $\Theta(\log(1/p_0))$ at $q=1$. GARL ($q=0.75$) escapes cold-start where GRPO and all $q\leq 0.5$ yield 0%. **TRICE EM E-step ([[../research/teacher-student-rl/trice-cot-latent-variable]]) is recovered as PAFT at $q=1$**; STaR is its hard-acceptance limit; VeriFree / RB-REINFORCE is GARL at $q=0$. Most directly load-bearing fix to date for the regime [[../research/single-sample-rl-finetuning/_overview]] inhabits.

5. **Latent-GRPO documents a new RLVR mechanics failure mode** (Latent Mixture Non-Closure) and produces 3.31× shorter chains at +4.27 Pass@1 on AIME / Math500 vs. explicit GRPO. Open question: does latent-space training expand pass@k beyond base-model upper bound? Paper does not test — unresolved against Invisible Leash. Cross-link against [[../research/self-play/yue-rlvr-boundary]].

**Wiki updates.**

- 5 new pages (paths above). Each carries `[[../weekly-briefs/2026-05-03]]` provenance back-link per local conventions.
- `wiki/index.md` — added 5 rows (TTT theme, self-play theme, teacher-student-rl theme, rl-optimizers theme); updated theme-summary lines for self-play (10 proposer-reward shapes, was 9), test-time-training (3 pages, was 2), teacher-student-rl (now includes co-evolution).
- `wiki/watchlist.md` — first-time seeding by agent: 10 surplus candidates added under sections `Self-play`, `Post-GRPO RL optimizers`, `Process reward models`, `Teacher-student RL`, `Test-time training`. Cap respected (≤10/run).
- `wiki/conflicts/index.md` — no new conflicts opened. Existing `invisible-leash-vs-spiral-transfer` and `unified-vs-two-model-self-play` flagged as touched-but-not-resolved by SGS evidence (Stage-1-compatible).

**Tracking discipline.** Page-writing done by orchestrator (not subagents) per master_notes 2026-05-01 lesson — single-source-of-truth tracking updates this run.

**Outstanding.**
- Latent-GRPO base-bound test left as flagged tension; not promoted to a conflict file (no contradictory wiki claim yet).
- Tsallis vs. MASPO Signal-Reliability axis check left for next /lint or harvest.
- No new master_notes entry warranted this run.

**Delivery.** Brief at `wiki/weekly-briefs/2026-05-03.md` and `/tmp/weekly-brief-2026-05-03.{md,html}`. Email + Telegram per local conventions. Diff uncommitted on `single-shot-training-wiki` (per local convention; no dedicated weekly branch).

## 2026-05-10 — weekly-brief autonomous sweep

**Window.** 7-day trend scan (2026-05-04 → 2026-05-10). Two parallel trend-scan subagents (aggregators + curators/labs) returned ~17 candidates with strong overlap on a single coherent pattern: **the OPD/RLVR-as-selection cluster consolidating into a thesis** — RL is selection-not-learning at the token level (Rethinking-RL), OPSD is compression-not-correction post-RLVR, KL-RLVR has a closed analytical form (BOLT) and a structural collapse mechanism (Binary-Rewards), and multi-teacher debate breaks the OPD ceiling (MAD-OPD). Selection per `wiki/reference-sources.md` (technical novelty > conflict-resolving > wiki-fit > reproducibility > multi-signal).

**Captures (5 sources).** Rethinking RL Sparse Selection (arXiv:2605.06241), OPSD Compresses RLVR (arXiv:2605.06188), Binary Rewards Fundamental Challenges (arXiv:2605.02375), BOLT (arXiv:2605.02469), MAD-OPD (arXiv:2605.01347). All under `raw/research/weekly-2026-05-10/`. Engine: pymupdf (per master_notes 2026-04-28 marker-degradation policy). Audit: 1 broken thumbnail ref (page-0 PNG metadata; not body content); text bodies 56–141 KB, well above abstract-only threshold. Ingest summaries validated via `tools.ingest_plan.parse_summary` (5/5 ok).

**Headline findings.**

1. **Rethinking-RL operationalises Invisible Leash at the token level.** Across GRPO/PPO/RLOO and three model families: 1.0–4.1% positions reranked, **0% shifted outside base top-5**, mean promoted rank 2.14–2.39 (Eq. 3, Table 2). Oracle intervention exclusively at reranked positions exactly recovers RL pass@1; random substitution does not (Fig. 2). KL-LoRA distillation (Eq. 4): rank-32 LoRA with 0.27–0.49% params matches RL teacher; rank-8 $W_O$-only at 0.04% params lags by 1 point (Fig. 3, Table 4). **REASONMAXXER** — entropy-gated contrastive on ~50 problems — matches/exceeds full RL at $4–25 vs $200–$103k (Table 3, ~3 orders of magnitude cost reduction).

2. **OPSD compacts what RLVR teaches; it does not correct.** Correct-only OPSD: −29% length, ~0 accuracy change. Incorrect-only OPSD: −7 to −10 pp accuracy across seeds, models, divergence variants, mid-trace reinjection, richer teacher contexts, up to 500 steps. Pipeline: **SFT → RLVR → OPSD**. RLVR expands reachable trajectories; OPSD compacts. OPSD cannot create new reasoning states the student's distribution doesn't already support — separate diagnostic for the same Invisible-Leash boundary.

3. **Dymetman gives the formal collapse mechanism.** Binary-reward filtered model $p^* = a(\cdot|\mathcal{Y}_1)$ is the I-projection of base $a$ onto the valid set. KL-RLVR converges to $p^*$ in *forward* KL as $\beta \to 0$, but $\text{KL}(p^\beta \| p^*) = +\infty$ for every finite $\beta$ (Theorem 3.1d) — reverse KL toward $p^*$ is structurally impossible. Eq. 10 shows that under model misspecification, small $\beta$ amplifies the validity term and drives the optimiser to parametrically-easy near-Dirac policies. Toy bigram: $\lambda=10$ → 97% mass on one sequence vs $p^*$ entropy ≈ 2.0. **Position A in [[../conflicts/invisible-leash-vs-spiral-transfer]] now has a structural account of pass@k inversion**.

4. **BOLT closes the analytical picture for KL-regularised RLVR.** Theorem 3/4: the **unique** reference-sampled weighted-SFT objective matching the Boltzmann target $\pi^*$ is the prompt-normalised density-ratio weight $w^\star = \exp(r/\beta)/Z(x)$. Theorem 6: finite one-shot saturation gap $\beta\log(1/\pi^*(S_N|x))$ — extra SFT epochs cannot remove it. Theorem 7: coverage–ESS frontier $N \gtrsim 1/p_\gamma$. Theorem 11: iterative BOLT with sampler refresh = KL policy mirror descent; after $K$ rounds $\pi_{\theta_K} \propto \pi_{\theta_0}\exp(Kr/\beta)$. Empirically BOLT matches/exceeds GRPO at 75–85% less wall-clock and 18–31% less peak memory (single-run, directional). **Companion to Tsallis $\mathcal{J}_Q$ at the un-regularised end** — together they cover both endpoints of the RL/SFT continuum.

5. **MAD-OPD breaks the single-teacher OPD ceiling.** $K=2$ teachers debating $R=2$ rounds; debate transcript as privileged context; softmax-confidence-weighted token-level supervision (Eq. 8). 4B student trained under 14B+8B debate **exceeds the 14B teacher alone** on LCB-v6 by +4.26% pass@1 / +10.29% BoN@16. Task-adaptive divergence derived from gradient analysis: JSD for agentic (Lemma 1 — bounded gradient under privileged $p$–$q$ gap), reverse KL for code (Lemma 2 — coherent code path mode-concentration). MT-OPD (naive multi-teacher averaging) underperforms single-teacher OPD on code in 4/6 configs — multi-model alone is not the answer; **stabiliser (debate transcript) is the load-bearing axis**. OPAD step-level agentic extension.

**Cross-source pattern.** Findings 1–4 are mutually reinforcing: Rethinking-RL gives the token-level fact (0% shifted), Binary-Rewards gives the structural reason (forward/reverse KL asymmetry to $p^*$ + misspecification-driven collapse), BOLT gives the closed-form static analogue (one-shot gap = $\beta\log(1/\pi^*(S_N|x))$, coverage–ESS frontier $N \gtrsim 1/p_\gamma$), and OPSD-compresses-RLVR confirms the boundary on the post-RL side (cannot create new states). The **RL-as-selection-not-learning** thesis crystallised significantly this week.

**Wiki updates.**

- 5 new pages (paths in revisions row). Each carries `[[../weekly-briefs/2026-05-10]]` provenance back-link per local conventions.
- `wiki/index.md` — added 5 rows; theme summaries refreshed for `rlvr-mechanics` (sparse-selection + binary-rewards), `teacher-student-rl` (OPSD compaction + MAD-OPD debate), `rl-optimizers` (BOLT KL-RLVR analytical closure).
- `wiki/conflicts/invisible-leash-vs-spiral-transfer.md` — sharpened Position A with token-level (Rethinking-RL) and formal (Binary-Rewards) backing.
- `wiki/conflicts/unified-vs-two-model-self-play.md` — extended with MT-OPD failure-mode adjacent data point (multi-teacher without stabiliser < single-teacher; consistent with stabiliser-presence-as-axis editorial reading).
- `wiki/conflicts/index.md` — both conflicts updated with 2026-05-10 status notes.
- `wiki/watchlist.md` — 10 surplus entries added (Uni-OPD, Near-Policy, IOP/IOP-GSPO, Reflect-Retry-Reward, ResRL, TTC-RL, UniSD, Controllable-PRM-data, APMPO, Search-driven-reward). Cap respected.

**Tracking discipline.** Page-writing done by orchestrator (not subagents) per master_notes 2026-05-01. Single-source-of-truth tracking updates this run.

**Pre-existing dirty state at run start.** ~36 modified files (`master_notes.md`, multiple `wiki/research/*` pages, `wiki/conflicts/index.md`, `.claude/commands/weekly-brief.md`) + 1 untracked (`wiki/conflicts/invisible-leash-vs-spiral-transfer.md`). These are prior in-progress work, not from this sweep — flagged in the email under Pre-existing uncommitted changes.

**Outstanding.**
- BOLT ↔ Tsallis $\mathcal{J}_Q$ unification — both unify weighted-SFT family at different ends; a synthesis page tying them to MASPO's induced-target taxonomy is overdue.
- MAD-OPD's task-adaptive-divergence framework may apply to CoPD's alternating GRPO+mutual-KL — left for next /lint or harvest.
- Watchlist now has 4 distinct OPD entries (Rethinking-OPD, TCOD, Uni-OPD, Near-Policy, UniSD, also CoPD on-wiki + OPSD on-wiki + MAD-OPD on-wiki) — promotion threshold (≥2 converging entries) is satisfied for an OPD landscape page next week.
- No new master_notes entry warranted this run.

**Delivery.** Brief at `wiki/weekly-briefs/2026-05-10.md` and `/tmp/weekly-brief-2026-05-10.{md,html}`. Email + Telegram per local conventions. Diff uncommitted on `single-shot-training-wiki` (per local convention; no dedicated weekly branch).

---

## 2026-05-11 — Query: RL-as-selection-not-learning thesis

User asked for elaboration on the "RL-as-selection-not-learning" thesis from the 2026-05-10 weekly brief.

**Sources used.** [[research/rlvr-mechanics/rethinking-rl-sparse-selection]], [[research/rlvr-mechanics/binary-rewards-rl-challenges]], [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]], [[research/teacher-student-rl/opsd-compresses-rlvr]], [[conflicts/invisible-leash-vs-spiral-transfer]], [[research/rlvr-mechanics/_overview]].

**Answer.** Comparison table of the four 2026-05-10 papers (token-level / information-geometric / closed-form static / post-RL), prose on why they form one thesis rather than four observations, closed-form bounds the cluster newly supplies (BOLT Theorem 6/7), conflict status (Position A in [[conflicts/invisible-leash-vs-spiral-transfer]] is now token-level-sharp and structurally grounded; residual gap on SPIRAL opponent-adaptation remains open), and practical implications for [[research/synthesis/proposed-method]] (high-$p_\gamma$ pre-flight check, entropy-gated rank-8 $W_O$ LoRA concept probe, capacity expansion needs non-RLVR mechanisms).

**Wiki update.** Added "RL-as-selection-not-learning" as a cross-cutting section in [[research/rlvr-mechanics/_overview]] with four-bullet decomposition + single-sample implications; added the two new same-theme pages (rethinking-rl-sparse-selection, binary-rewards-rl-challenges) to the page list (previously only mentioned in `index.md` and individually). The overview had not yet absorbed the 2026-05-10 cluster; this closes that gap.

---

## 2026-05-11 — Query: SFT-RL pairing for capacity expansion

User asked whether the RL-as-selection-not-learning thesis implies that pairing RL teacher learning with rounds of SFT specifically designed to embed required information could enable capabilities in a target region.

**Sources.** [[research/self-play/yue-rlvr-boundary]], [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]], [[research/teacher-student-rl/opsd-compresses-rlvr]], [[research/single-sample-rl-finetuning/deepseek-r1]], [[research/rl-optimizers/instructgpt]], [[research/single-sample-rl-finetuning/reft]], [[research/single-sample-rl-finetuning/cbrl]], [[research/teacher-student-rl/knowrl]], [[research/teacher-student-rl/co-evolving-policy-distillation]], [[research/self-improvement/star]], [[research/self-play/spice]], [[research/synthesis/proposed-method]], [[research/synthesis/concept-curriculum-method]].

**Answer.** Yes — the thesis is consistent with the wiki and has multiple instantiated recipes (R1, InstructGPT, ReFT, CBRL, KnowRL, CoPD, STaR). Yue's "distillation uniquely expands capacity" finding + BOLT Theorem 7's coverage wall ($N \gtrsim 1/p_\gamma$) supply the theoretical case: SFT lifts $\pi^*(S|x)$ in the target region; RL then concentrates within the lifted support. OPSD-compresses-RLVR is the boundary — SFT must come before or alongside RL, not as a post-RL corrective on failed rollouts.

**Wiki update.** Added an "Extension: parametric SFT to lift $p_\gamma$ in the target region (2026-05-11)" section to [[research/synthesis/proposed-method]]. Distinguishes a new design axis **C_w** (weight-update reference) from existing **C** (in-context reference); names four corpus-grounded design constraints (pre-RL or interleaved; minimal-sufficient; anneal the scaffold; forgetting protection composes) plus a fifth from BOLT (target the support-lifting requirement quantitatively); flags the open experimental question — no captured paper has done parametric SFT on a textbook *body* before a per-concept RLT loop at single-concept granularity.

---

## 2026-05-12 — Query: BOLT intuition + weighted SFT explanation

User asked for the intuition behind BOLT's main idea and an explanation of "weighted SFT" in BOLT's specific sense.

**Sources.** [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]], [[research/rlvr-mechanics/binary-rewards-rl-challenges]], [[research/rl-optimizers/tsallis-loss-continuum]], [[research/self-play/invisible-leash]], [[research/single-sample-rl-finetuning/1-shot-rlvr]], [[research/self-improvement/star]], [[conflicts/invisible-leash-vs-spiral-transfer]].

**Answer.** KL-RLVR's optimal solution $\pi^*(y|x) \propto \pi_\text{ref}(y|x)\exp(r/\beta)$ is a tilted reference policy. BOLT's central move: hit this target without an RL gradient via one-shot weighted cross-entropy on samples from $\pi_\text{ref}$, with per-example weights $\hat{w} = \exp(r/\beta)/\hat{Z}_N(x)$ — the prompt-normalised Boltzmann density-ratio. Theorem 4 makes this weight uniquely correct; other choices (raw reward, filtered-positive, advantage) miss $\pi^*$ by an irreducible Corollary-5 gap. What RL still buys: support expansion (Theorem 6 cap), sampler refresh (Theorem 11 = KL-PMD).

**Wiki update.** Added a 4-paragraph "Intuition" section to [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] between the summary and the Source/Method blocks. The page previously jumped straight from the dense summary to theorem statements — the "$\pi^*$ is tilted $\pi_\text{ref}$, so weighted-SFT-from-$\pi_\text{ref}$ recovers it" step was implicit. The new section makes it explicit and contrasts BOLT's Boltzmann weight against alternatives (STaR/ReST filtered-positive, raw reward, advantage) by way of Corollary 5's quantifiable gap.

---

## 2026-05-12 — Query: iterative reference-refresh BOLT vs RLVR gap

User asked whether updating the reference model to the newly weighted-SFT-trained policy and repeating would alleviate the gap between RLVR and BOLT.

**Sources.** [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (Theorem 11, Corollary 12), [[research/self-play/invisible-leash]], [[research/rlvr-mechanics/rethinking-rl-sparse-selection]], [[research/rlvr-mechanics/binary-rewards-rl-challenges]], [[research/self-play/yue-rlvr-boundary]], [[research/self-play/two-stage-dynamic]], [[conflicts/invisible-leash-vs-spiral-transfer]], [[research/synthesis/proposed-method]] (component **C_w**).

**Answer.** Yes — Theorem 11 says exactly this, and Corollary 12 says it closes the static-vs-online gap exponentially in $K$ when $p_0(x) > 0$. After $K$ rounds, $\pi_{\theta_K} \propto \pi_{\theta_0}\exp(Kr/\beta)$ — KL policy mirror descent. *However:* this only alleviates the *static* gap. The deeper support-inclusion bound (Invisible Leash Theorem C.1) applies to the iterate too — $\pi_{\theta_0}\exp(Kr/\beta)$ stays on $\text{supp}(\pi_{\theta_0})$. Sharpening by $K$ at fixed $\beta$ equals $\beta_\text{eff}=\beta/K$, which worsens Dymetman near-Dirac collapse under misspecification. Iterative BOLT *is* RL on the gradient side, so it inherits RL's selection-not-learning bound. Capacity expansion needs distillation from a teacher with support outside $\pi_{\theta_0}$ (Yue) or an entropy-preserving Stage-2 mechanism (Yao), not more BOLT rounds on the same base.

**Wiki update.** Extended the BOLT page's Intuition section: the sampler-refresh bullet now explicitly mentions the reference-refresh equivalence and Corollary 12, and a new paragraph makes the iterative leash-inheritance explicit (previously the page only connected one-shot BOLT to Invisible Leash via Theorem 6). Closes a loophole where an attentive reader could conclude iterative refresh escapes the support wall.

---

## 2026-05-12 — Query: how BOLT's weighting scheme works

User asked for the mechanics of BOLT's weighting scheme.

**Sources.** [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (Algorithm 1, Eq. 10, Theorems 3/4, Corollary 5, Table 1/2), [[research/rlvr-mechanics/binary-rewards-rl-challenges]], [[research/self-improvement/star]].

**Answer.** Per-prompt softmax over $N$ verifier-scored rollouts at temperature $\beta$, with per-prompt normaliser $\hat{Z}_N(x) = \frac{1}{N}\sum_n \exp(r/\beta)$. Within-prompt ratio depends only on reward differences; across-prompt, $\hat{Z}_N(x)$ cancels difficulty bias. $\beta \to 0$ collapses to rejection-sampling on the top rollout; $\beta \to \infty$ collapses to uniform SFT; iterative refresh sharpens to $\beta_\text{eff}=\beta/K$. Theorem 4 makes this weight uniquely correct when sampling from $\pi_\text{ref}$; alternative weights (raw, globally normalised, filtered-positive, advantage) miss $\pi^*$ by Corollary-5 gap.

**Wiki update.** Added a "Weighting scheme — mechanical view" section to [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] after the Intuition block. Consolidates the per-prompt softmax framing, the $\beta$ limits, and a side-by-side table of alternative weight choices. Closes the gap where the page had Eq. 10 + theorems but not the concrete softmax mechanics in one place.

---

## 2026-05-12 — Query: two-stage prime + exercise/commentary method proposal

User proposed a refined two-stage method: **Stage 1** (Concept Priming) SFT on a curated textbook-chapter body; **Stage 2** per-exercise inner loop split into **(a)** BOLT/GRPO-style RL on the exercise (rollouts, verifier, optimise) and **(b)** *per-rollout* teacher-commentary-generated, appended, and SFT'd; outer loop identifies concept gaps. Asked for strengths/weaknesses and how it fits the current approach.

**Sources.** [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (Theorems 6/7/11), [[research/self-play/yue-rlvr-boundary]], [[research/self-play/invisible-leash]], [[research/self-play/two-stage-dynamic]], [[research/single-sample-rl-finetuning/deepseek-r1]], [[research/rl-optimizers/instructgpt]], [[research/single-sample-rl-finetuning/reft]], [[research/single-sample-rl-finetuning/cbrl]], [[research/teacher-student-rl/knowrl]], [[research/teacher-student-rl/co-evolving-policy-distillation]], [[research/teacher-student-rl/opsd-compresses-rlvr]], [[research/self-improvement/star]], [[research/single-sample-rl-finetuning/critique-ft-one-problem]], [[research/teacher-student-rl/trice-cot-latent-variable]], [[research/teacher-student-rl/sakana-rlt]], [[research/critique-self-correction/critic-cot]], [[research/in-context-learning-theory/icl-bayesian-inference]], [[research/synthesis/proposed-method]] (C_w extension), [[research/synthesis/recursive-concept-learning]].

**Answer.** Stage 1 = component **C_w** (already captured in proposed-method's 2026-05-11 extension); motivated by BOLT Theorem 7 ($N\gtrsim 1/p_\gamma$) and Yue's distillation-only-expands-support finding. Stage 2(a) = the existing inner loop with BOLT substituted for Dr-GRPO ([[research/rl-optimizers/bolt-kl-rlvr-boltzmann]]; same target, 75–85% less wall-clock). Stage 2(b) — per-rollout commentary + SFT — was *not* yet a named component: corpus-attested in three separate forms (STaR rationalization, critique-FT-one-problem amplification, TRICE wrong-rollout salvage; CoPD interleave existence proof) but never composed at per-rollout granularity. Outer loop = RCL verbatim, sitting on the deepest captured corpus gap (failure-trace-conditioned D1 decomposition; Tier 5 item 32).

Key constraints surfaced: (i) [[research/teacher-student-rl/opsd-compresses-rlvr]] forbids SFT-after-RL as corrective at both the Stage 1↔2 boundary *and* recursively inside the (a)→(b) per-rollout boundary — both must be pre-RL or interleaved, not post-hoc; (ii) STaR temperature ablation requires trace-level filtering in (b); (iii) KnowRL pruning paradox warns Stage 1 textbook-body magnitude is not monotonically beneficial; (iv) Bayesian-ICL tension between **C_w** and **C** — Stage 1 partially competes with the 2026-05-01 structural-asymmetry locked design; (v) Two-Stage-Dynamic regime constraint — entropy preservation hyperparameter discipline needed for (a) to escape Invisible-Leash bound; (vi) simultaneous-per-rollout RL+SFT is uncharacterised — captured methods alternate (CoPD) or filter-then-SFT (STaR), not both gradients per rollout.

**Wiki update.** Added a "Sub-extension: per-rollout commentary-SFT (Stage 2(b) variant)" section to [[research/synthesis/proposed-method]] under the existing C_w extension, naming **component C_b**. Captures the three independent corpus attestations (STaR/critique-FT/TRICE), the OPSD-derived ordering constraint recursively applied to (a)→(b), STaR's trace-level filtering requirement, the composition with R/V/C_w/G, and four open experimental questions (per-rollout vs per-exercise SFT, teacher source for commentary, BOLT iteration × per-rollout-SFT coherence, Stage 2(b) at $G=1$ baseline). No new page created; extension lives where the existing **C_w** extension does.

---

## 2026-05-12 — Query: refinement of textbook synthesis + format guard + offline logit-reweight hypothesis

User added three follow-on thoughts on the two-stage method: (1) Stage 1 could be a chunked-SFT + RLVR-on-summary loop, with a bounded reward; (2) a format/fluency guard mechanism is missing from the current proposal; (3) hypothesised that one could offline-reweight logits using a subject-matter prior to put the model into the right solution space — asked what else in the corpus works on this hypothesis.

**Sources.** [[research/teacher-student-rl/sakana-rlt]] (RLT $r^{SS}$ as bounded summary-reward — wiki's strongest answer), [[research/rlvr-mechanics/learning-to-think]] (L2T Fisher info-gain), [[research/self-play/info-gain-self-play]] (epiplexity), [[research/self-improvement/self-rewarding-lm]] (rubric self-judge + math/reasoning caveat), [[research/process-reward-models/math-shepherd]], [[research/teacher-student-rl/trice-cot-latent-variable]]; for format guard: [[research/single-sample-rl-finetuning/1-shot-rlvr]] (gibberish-trace at 1.4k steps), [[research/rl-optimizers/mcpo]] §4.1 Fig 2 (unanchored mastered-prompt drift mechanism), [[research/rl-optimizers/dr-grpo]], [[research/rl-optimizers/dapo]] (Overlong Reshape), [[research/rl-optimizers/instructgpt]] (ptx), [[research/single-sample-rl-finetuning/reft]] (KL leash); for offline reweight: [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] (0%-shifted-outside-base-top-5 + REASONMAXXER rank-8 $W_O$ LoRA at 0.04% params), [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (closed-form static target), [[research/rlvr-mechanics/binary-rewards-rl-challenges]] (filtered-model I-projection), [[research/in-context-learning-theory/icl-bayesian-inference]] (theoretical underpinning), [[research/test-time-training/algorithm-distillation]] (frozen-weights limit case), [[research/concept-learning/concept-bottleneck-models]] (test-time intervention), [[research/test-time-training/tempo]] (E-step verifier recalibration), [[research/self-play/rstar]] (12.51% → 63.91% pure decoding-time).

**Answer.** (1) Strongest bounded-reward shape for chunk-summary RLVR is RLT $r^{SS}=\log\pi_s(s\mid t, q)$ with chunk-derived held-out QA as the eval set — summary plays the role of teacher think-tokens $t$, bounded by log-prob normalisation, with $r=0.89$ correlation to student gain. Six total shapes tabulated. (2) Format guard tools exist scattered across proposed-method's F/P2/S and the inline KL leash — should be elevated to a named composite primitive. Key corpus signal: 1-shot RLVR's training-trace gibberish at ~1.4k steps is mechanistically caused by unanchored drift on mastered prompts (MCPO §4.1 Fig 2 isolates the mechanism); at $N=1$, DAPO Dynamic Sampling is a no-op; MCPO hinge-KL is the corpus's specific response. (3) Offline-reweight hypothesis has strong corpus support — Rethinking-RL Sparse Selection is the closest direct attestation (0% shifted outside base top-5, oracle intervention at reranked positions exactly recovers RL pass@1, rank-8 $W_O$ LoRA at 0.04% params suffices via REASONMAXXER), and BOLT is the closed-form static analogue. Real gap: classical decoding-time family (contrastive decoding, DEXPERTS, GeDi, FUDGE, PPLM, classifier-free guidance, activation steering, ITI, DoLa) is absent from the wiki via grep.

**Wiki update.** Three changes to [[research/synthesis/proposed-method]]: (a) new named **component L** (format/fluency guard composite — KL leash + EWC + Balashov mask + Dr-GRPO length-fix + DAPO Overlong Reshape + MCPO hinge-KL + InstructGPT ptx); failure-mode row added to per-primitive table. (b) New sub-extension **C_w⁺** (chunked SFT + RLVR-on-summary) under the C_w block with six bounded-reward shapes tabulated. (c) New sub-extension **R_w** (offline logit-reweight from a subject-matter prior) consolidating all corpus support for the user's hypothesis. **Watchlist update:** new "Decoding-time / activation steering" section seeded with 9 entries (Contrastive Decoding, DEXPERTS, GeDi, FUDGE/PPLM, Classifier-free guidance, Activation steering / RepE, ITI, DoLa, REASONMAXXER-deep-dive) for next weekly brief or /research promotion.

---

## 2026-05-13 — New hypothesis: concept-granularity middle layers

User surfaced an architectural hypothesis from the REASONMAXXER / Rethinking-RL findings: if only 1-4% of tokens carry the decision-of-record signal, internal representations should operate on variable-granularity concept-units (merge filler, split decision points) rather than the fixed per-token grid.

**Sources cited inline.** [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] (primary motivation), [[research/rlvr-mechanics/rl-sparse-subnetwork]], [[research/in-context-learning-theory/icl-as-gradient-descent]], [[research/in-context-learning-theory/icl-bayesian-inference]], [[research/in-context-learning-theory/induction-heads]], [[research/concept-learning/recursive-concept-evolution]], [[research/concept-learning/concept-bottleneck-models]], [[research/rl-optimizers/latent-grpo]] (closest existing corpus result), [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (speculative coverage-wall connection), [[research/concept-evaluation/causal-abstraction]] (candidate concept-unit probe).

**Page created.** [[research/synthesis/concept-granularity-architecture]] under `research/synthesis/` matching existing editorial-proposal convention. Initial sketch only per user request: one-paragraph hypothesis, motivation, ASCII flow diagram, supporting mechanisms table (with status column flagging what's not yet captured), gaps list (7 items), watchlist targets, promotion criteria for moving from hypothesis to design.

**Index + watchlist updated.** Added a row to `wiki/index.md` under Synthesis. Added "Variable-granularity / concept-level architectures" section to `watchlist.md` with 7 categorical targets (Funnel Transformer, MoT/MoD, ToMe-style language token-merging, Latent-GRPO successors, entropy-routed compute, byte-level + learned chunking, counter-evidence).

**Promotion criteria.** Hypothesis stays as initial sketch until: (1) at least one captured corpus paper demonstrates a working merge or split primitive at the language-model middle-layer level, (2) a concrete differentiable loss formulation for the merge/split routing has been empirically tried, (3) a failure-mode catalogue comparable to Latent-GRPO's Latent Mixture Non-Closure exists.

---

## 2026-05-13 — Research run: decoding-time / activation-steering theme

User requested a /research scan of the gaps surfaced by the recent R_w hypothesis ("the information is already in the base model; an offline reweighting prior can put it into the right solution space" — 2026-05-12 query). Watchlist had a 9-entry "Decoding-time / activation steering" section seeded but unpopulated.

**Sources captured (13):** PPLM 1912.02164, GeDi 2009.06367, DEXPERTS 2105.03023, FUDGE 2104.05218, Contrastive Decoding 2210.15097, CD-for-Reasoning 2309.09117, DoLa 2309.03883, CFG-LM 2306.17806, ITI 2306.03341, ActAdd 2308.10248, CAA 2312.06681, RepE 2310.01405, Linear Representation Hypothesis 2311.03658. All to `raw/research/decoding-time-steering/`. Audit: 86 wrong-anchor image refs (kit-level pymupdf bug, master_notes 2026-05-13), but text content intact.

**Key cross-source finding.** All 13 papers converge on a single mechanistic claim: **the relevant information is already in the base model; an offline reweighting prior — logit-space or activation-space — suffices to put the model into the right solution space without weight updates.** Unusual unanimity across a 4-year arc. No source contradicts.

**Most direct empirical support for R_w:**
- ITI: 40% probe–generation gap on LLaMA-7B; TruthfulQA 32.5% → 65.1% via head-level shift; ~40–81 contrast pairs
- RepE: concept-reading beats few-shot prompting on 5 QA benchmarks; LAT + reading vector + control operators; umbrella for ITI/ActAdd/CAA
- DoLa: +12–17pp TruthfulQA via single-model layer contrast — no auxiliary needed
- CD-for-Reasoning: LLaMA-65B + CD beats PaLM-540B on GSM8K (math regime)
- CFG-LM: structural Boltzmann-tilt analogue ($\propto P\exp(\gamma \cdot \text{prompt-direction})$); LAMBADA SoTA at 7B
- ActAdd: $n=1$ contrast pair = causally effective direction
- Linear Representation Hypothesis (Park, Choe, Veitch ICML 2024): formal warrant — Theorem 2.5 proves adding the embedding direction increases concept probability while leaving causally-separable concepts unchanged

**Wiki update.** New theme `wiki/research/decoding-time-steering/` (13 per-paper pages + _overview). New synthesis page `wiki/research/synthesis/decoding-time-shapes.md` (companion to proposer-reward-shapes; tabulates the 13 methods + 3 structural patterns + Bayesian-vs-Boltzmann correspondence). **R_w extension in proposed-method updated** with concrete anchor table replacing the prior categorical references. Backlinks added to 6 existing wiki pages (concept-learning/_overview, icl-bayesian-inference, rethinking-rl-sparse-selection, bolt-kl-rlvr-boltzmann, invisible-leash, single-sample-rl-finetuning/_overview). Watchlist cleared from 9 entries to 1 (REASONMAXXER deep-dive still open). Index updated with theme row + 13-page section + synthesis row.

**Harvest checkpoint.** Filed a kit-level entry to `master_notes.md`: capture_pdf's pymupdf engine writes wrong-anchor image refs (paths anchored at repo root, not file-relative). 86 audit "broken image refs" across this run, same pattern as 2026-04-23 rl-optimizers run; image files exist on disk but Obsidian/markdown rendering fails. Two candidate fixes (capture_pdf rewrite OR audit_captures special-casing). For `/harvest` promotion.

**Coverage gap that did NOT close.** Failure-trace-conditioned LLM concept decomposition (RCL D1 / Tier 5 item 32) — web search surfaced only *agent* failure attribution (MAST, Who&When, AgenTracer 2025) which is a different problem class. Did not capture borderline-relevant sources. RCL Tier-5 item 32 remains open.

---

## 2026-05-13 — Query: is REASONMAXXER just targeted RL?

User asked: "for reasonmaxxer, it seems like in the end this is just a much more targeted RL algorithm. Basically identify the specific tokens that are the decision points and only apply the advantage to those tokens, otherwise just apply KL divergence. Am I missing something?"

**Sources.** [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] (primary), [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]], [[research/rl-optimizers/tsallis-loss-continuum]], [[research/rl-optimizers/mcpo]], [[research/rl-optimizers/dapo]], [[research/rl-optimizers/maspo]].

**Answer.** Substantively right on the partition (advantage at high-entropy positions, KL anchor at low-entropy positions — Eqs. 5–7 literally implement that). Four nuances make it not just a re-targeted on-policy RL: (1) offline-sampled from $\pi_\text{base}$, not on-policy; (2) contrastive CE, not policy-gradient — positive-only ablation drops 0.440→0.398; (3) per-position gate via $H_t > \tau$, finer than MCPO's per-prompt hinge or DAPO's per-prompt filter; (4) the "RL gradient" is replaced with weighted contrastive CE on a fixed dataset, not approximated online — same family move as BOLT for KL-RLVR. Open design slot: no captured paper does the on-policy analogue (per-token entropy-gated advantage + KL anchor at low-entropy).

**Wiki update.** Added "Reading REASONMAXXER as targeted weighted-SFT" section to [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] with comparison table (BOLT × Tsallis $\mathcal{J}_Q$ × REASONMAXXER, columns: sampler / where the update fires / weight). Closes a framing gap: the paper's existing description gave the algorithm but didn't slot it into the offline-weighted-SFT family or call out the open online-analogue slot.

---

## 2026-05-13 — Query: roll REASONMAXXER's entropy-gating into DAPO

User asked whether entropy-gating could be rolled into DAPO (or another on-policy method) and asked for speculation on effectiveness.

**Sources.** [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] (REASONMAXXER ablation, entropy-thresholded gating), [[research/rl-optimizers/dapo]] (Clip-Higher / Dynamic Sampling / Token-Level PG Loss), [[research/rl-optimizers/mcpo]] (hinge-KL on mastered prompts, ~5% regression), [[research/rl-optimizers/dr-grpo]] (std-removal), [[research/rl-optimizers/maspo]] (Gradient-Utilization axis), [[research/self-play/two-stage-dynamic]] (Stage-1 gradient flow + Stage-2 entropy preservation), [[research/self-play/info-gain-self-play]] (epiplexity pre-flight), [[research/self-play/invisible-leash]] (Theorem C.1), [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (Theorem 7 coverage wall), [[research/rlvr-mechanics/binary-rewards-rl-challenges]] (near-Dirac collapse), [[research/synthesis/proposed-method]] component **G**.

**Answer.** Composition is well-motivated and the slot is already named in the wiki. Five corpus findings bear: (1) Stage-1 alignment is constructive — gating concentrates gradient where the optimiser actually moves; (2) Stage-2 needs entropy preservation — aggressive gating may collapse the gate itself; (3) low-entropy KL anchor subsumes MCPO at token level; (4) REASONMAXXER's contrastive contribution doesn't transfer directly — positive-only ablation lost 0.440→0.398, and on-policy negative samples come from drifting policy; (5) hard bounds (Invisible Leash, BOLT coverage wall) unchanged. Per-knob design choices: entropy source (base vs current — risk of self-destructive collapse), KL target, Clip-Higher composition, std-handling, Dynamic-Sampling-redundancy. Per-knob speculation: $\pi_\text{base}$-computed gate likely safer; modest gains over plain DAPO probable; 3-orders-of-magnitude cost reduction will *not* transfer (came from offline-sampling not the gate). Best-bet measurement: three-way ablation plain DAPO / offline REASONMAXXER / entropy-gated DAPO with $\pi_\theta$ gate.

**Wiki update.** Added "Design choices for an on-policy entropy-gated variant" subsection to [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] under the existing open-design-slot note. Wiki-sourced content only (the five findings, the knob table, the ablation plan). Pure effectiveness speculation kept in the /query conversation, not promoted to wiki.

---

## 2026-05-13 — Query: how is REASONMAXXER's loss contrastive, differentiated from other RL?

User asked to expand on the "contrastive" claim and check the intuition that the contrast lives in the advantage's sign.

**Sources.** [[research/rlvr-mechanics/rethinking-rl-sparse-selection]], [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] (Theorem 4 — Boltzmann weight uniquely non-negative), [[research/rl-optimizers/ppo]], [[research/rlvr-mechanics/deepseekmath-grpo]], [[research/rl-optimizers/dpo]], [[research/rl-optimizers/tsallis-loss-continuum]], [[research/self-improvement/star]].

**Answer.** User's intuition is substantively correct: the contrast comes from $A_i$'s sign — per-problem mean-zero normalisation forces a push-up/push-down balance at gated positions. *But the signedness is shared with REINFORCE/PPO/GRPO*, so it doesn't differentiate REASONMAXXER from on-policy RL on its own. The differentiator is the combination: offline sampling (no importance ratio) + per-token gate + dropping clip. Most apt analogue: **offline REINFORCE with per-token gating and per-problem mean-zero advantage**. The "DPO than PPO" framing in the earlier edit was misleading — REASONMAXXER has neither pairwise structure nor sigmoid-margin. The deeper structural distinction in the offline-weighted-CE family is signed (REASONMAXXER) vs non-negative (BOLT, Tsallis $\mathcal{J}_Q$, STaR, ReST-filtered-positive); BOLT's non-negativity is *uniquely* enforced by Theorem 4.

**Wiki update.** (1) Replaced "Contrastive, not policy-gradient... Closer in shape to DPO than PPO" with a tightened bullet correctly placing REASONMAXXER as offline REINFORCE with gating + mean-zero advantage, and naming the signed/non-negative axis as the underlying organising distinction. (2) Annotated the comparison table's Weight column with signed/non-negative tags for BOLT, Tsallis, and REASONMAXXER. Closes a framing error introduced in the previous query update.

---

## 2026-05-13 — New synthesis page: fine-tuning best practices

User requested a practitioner-oriented best-practices page covering both SFT and RLVR — when to use, how to implement, recent trends.

**Page created.** [[research/synthesis/fine-tuning-best-practices]] under `research/synthesis/`.

**Structure.** One-paragraph framing → SFT (when / how / trends) → RLVR (when / how / trends) → SFT×RLVR pairing rules → project-frame defaults table → failure-mode catalogue.

**Key framing decisions baked in.**
- **SFT installs support, RLVR concentrates within it** — Yue's distillation-uniquely-expands + 2026-05-10 RL-as-selection cluster.
- **Order: SFT → RLVR → optional OPSD compaction** — OPSD-compresses-RLVR shows the reverse degrades.
- **Recent trends section captures the 2026 cluster**: RL-as-selection-not-learning four-paper crystallisation, weighted-SFT-replaces-RL (BOLT + Tsallis), token-level entropy gating (REASONMAXXER), two-stage dynamic, OPD landscape (CoPD, MAD-OPD, OPSD).
- **Project-frame defaults table** gives concrete recommendations for the single-sample concept-based 1-40B-LLM frame: GRPO + Dr. GRPO + DAPO Clip-Higher; RLT $r^{SS}$ reward when teacher-with-solution available; $G \geq 8$; difficulty $p\approx0.5$; pre-flight coverage and epiplexity checks; Balashov mask + EWC + KL leash for forgetting; correct-only OPSD for length compression; rank-32 LoRA over QKVO.
- **Failure-mode catalogue** consolidates pass@k inversion, near-Dirac collapse, post-saturation gibberish, MCPO drift, MT-OPD averaging, incorrect-only OPSD degradation, zero-variance prompts, length collapse, GRPO length bias, hint over-injection.

**Index.** Added row under Synthesis section in `wiki/index.md`.

**Cross-refs.** Page links to [[proposed-method]] as the component-level implementation roadmap that builds on these defaults; links to [[single-sample-concept-skeleton]], [[concept-curriculum-method]], [[recursive-concept-learning]] as composable companions.

---

## 2026-05-13 — Research run: selective fine-tuning / behaviour-isolation theme

User requested a /research scan on selective SFT — how to add new data signal without degrading response style; isolate reward signals to specific parts of network; apply gradient selectively. Three coherent clusters surfaced + one bridging cluster.

**Sources captured (15):** Knowledge Neurons 2104.08696, FF-as-KV-Memories 2012.14913, ROME 2202.05262, MEMIT 2210.07229, MEND 2110.11309, AlphaEdit 2410.02355, Skill-Localization 2302.06600, LIMA 2305.11206, Surgical-FT 2210.11466, PackNet 1711.05769, HAT 1801.01423, O-LoRA 2310.14152, DoRA 2402.09353, PIT 2402.12847, Knowledge-Editing-Survey 2310.16218. All to `raw/research/selective-finetuning/`. Audit shows the recurring pymupdf wrong-anchor image-ref bug; text content intact.

**Key cross-source finding (editorial, in [[research/selective-finetuning/_overview]] and the [[research/synthesis/proposed-method]] R_w extension update).** All 15 captures plus three existing wiki anchors converge on a single mechanistic claim: **behaviour is *isolable* in identifiable parameters / subspaces / layers / neurons**. The localisation scale spans:

- Skill-Localization (Panigrahi 2023): **0.01% of params** carry **>95% of fine-tuned skill** via grafting
- REASONMAXXER ([[research/rlvr-mechanics/rethinking-rl-sparse-selection]]): **rank-8 $W_O$ LoRA at 0.04% params** matches RL
- Balashov ([[research/rlvr-mechanics/rl-sparse-subnetwork]]): RL touches **5–30% of weights** spontaneously
- ROME / MEMIT / Knowledge-Neurons: **one MLP layer + rank-one update** per fact
- O-LoRA / DoRA / PackNet / HAT: per-task subspaces or masks, structurally isolated

This is the *training-time / weight-modification* counterpart to the unanimous "info is in there" finding from the 2026-05-13 [[research/decoding-time-steering/_overview]] run. Together they triangulate R_w from three independent corpus directions (decoding-time, SFT-skill, RL-emergent).

**Wiki update.** New theme `wiki/research/selective-finetuning/` (15 per-paper pages + _overview organised by four sub-families + ordering + survey). **R_w extension in proposed-method expanded** with a weight-level anchor table (12 primary + 3 background papers) and an editorial composition recipe (PIT ordering → Skill-Localization mask → O-LoRA orthogonal subspace → ROME edit → AlphaEdit null-space projection — none of the captured papers tests this composition). Backlinks added to 6 existing wiki pages (rl-sparse-subnetwork, rethinking-rl-sparse-selection, ewc-gemma2-cpt, concept-learning/_overview, single-sample-rl-finetuning/_overview, decoding-time-steering/_overview). Index updated with theme row + 15-page section.

**Coverage gap that did NOT close.** Failure-trace-conditioned LLM concept decomposition (RCL D1 / Tier-5 item 32) remains open. The selective-finetuning theme is structurally adjacent but does not provide a trace-conditioned decomposition mechanism — it provides surgical *modification* once the target is identified, not the identification itself.

**Harvest checkpoint.** Image-ref bug recurs — same kit-level entry already in master_notes 2026-05-13. No new harvest items this run.

---

## 2026-05-14 — New synthesis: test-time scaling

User asked "what is test-time scaling and how is it being used?" via /query. Wiki had ~10 pages of scattered TTS content across 5 themes (self-play/rstar, process-reward-models/*, critique-self-correction/*, decoding-time-steering, single-sample-rl-finetuning/deepseek-r1) but no unified anchor. Proposed two options for closing the gap (small section in TTT overview vs full synthesis page); user approved Option B.

**Page created.** [[research/synthesis/test-time-scaling]] under `research/synthesis/`.

**Structure.** One-paragraph summary → TTS vs TTT boundary → 5-modality comparison table (length / sample+verifier / search / iterative refinement / decoding-time+activation steering) → 6 documented use patterns → integration with proposed-method (components G + R_w) → hard limits table → TTS × training composition → watchlist categories.

**Key load-bearing claims (all wiki-sourced).**
- Strongest single-method TTS multiplier in corpus: [[research/self-play/rstar]] (LLaMA2-7B GSM8K 12.51% → 63.91% MCTS-only).
- Strongest trained TTS surface: [[research/single-sample-rl-finetuning/deepseek-r1]] (R1-Zero emergent long-CoT).
- TTS inherits the support bound: [[research/self-play/invisible-leash]] Theorem C.1 applies at inference too — TTS selects within base support, doesn't expand it.
- Tools beat self-only refinement: [[research/critique-self-correction/critic-tool-interactive]] CRITIC +10pp; self-only degrades.
- Length scaling peaks then declines without process supervision: [[research/rlvr-mechanics/learning-to-think]] L2T Sec 3.2.

**Cross-link added.** [[research/test-time-training/_overview]] now opens with a TTT-vs-TTS distinction disclaimer pointing to the new synthesis page.

**Index.** Added row under Synthesis section.

---

## 2026-05-15 — Lint run (first persisted)

Full health check. Mechanical link-graph + format via script; capture fidelity via tools.audit_captures ×15 dirs; semantic checks via 3 parallel theme-cluster subagents. Report: `wiki/lint-reports/2026-05-15.md`.

Headline: 0 orphans; 5 genuine broken links; 1 HIGH conflict (rlvr-incentivizes-reasoning miscited/inverted across index + 3 self-play pages + conflict file — verified against the page's own Source: it is Wen et al. 2506.14245 arguing *against* Position A, not Shao et al. supporting it); 3 MED conflicts (OPSD name collision; PRM-overview ORM/PRM-RL conflation; proposer-reward-shapes re-litigating the 2026-05-01 component-C lock). Coverage gaps: catastrophic-forgetting single-seed-treated-as-theme (+ a broken `[[../catastrophic-forgetting/_overview]]` link introduced 2026-05-13); self-improvement & critique-self-correction overview synthesis tables omit listed pages; α-DPG/forward-KL diversity-collapse fix uncaptured. Capture fidelity: 377 flagged, 100% the documented pymupdf wrong-anchor bug, text intact. No un-ingested raw sources (learning-from-less intentionally noted-not-ingested per 2026-05-14 user ruling). Fixes deferred to user direction.

---

## 2026-05-16 — Research run: RLVR skill-stacking forgetting + MoE-delta-LoRA (MoERA)

User question: does RLVR skill-stacking just reallocate optimization (zero-sum)? + the user's personal MoERA technique (MoE via delta-LoRA experts). 13 captures, two clusters.

**Answer to the skill-stacking question (in catastrophic-forgetting/_overview).** No — RLVR is a constrained, locality-preserving update, not free reallocation. Three nested RL-locality constraints: support-preservation ([[research/self-play/invisible-leash]] C.1) ⊃ KL-minimality ([[research/catastrophic-forgetting/rls-razor]]) ⊃ off-principal sparsity ([[research/catastrophic-forgetting/path-not-taken]] Three-Gate Theory). Behaviourally confirmed: 7-task continual post-training shows SFT catastrophically forgets, RFT retains ([[research/catastrophic-forgetting/rft-mitigates-forgetting]]). Caveat (Path-Not-Taken): off-principal capacity is a shared finite pool — better-than-zero-sum, not free.

**MoERA literature (moe-adapters theme).** LoRAMoE is the closest published analogue (frozen backbone + routed LoRA experts + localized balancing constraint) and the cross-theme bridge (it's a forgetting-mitigation method). Lineage Sparse-Upcycling → BTX → LoRAMoE → MoV/MoLORA → Self-MoE → MoLE → MoRAM (router-free). Architectural-avoidance answer to interference: separately-trained additive experts don't share a gradient so can't reallocate against each other.

**Trichotomy (now in proposed-method R_w extension).** Implicit (catastrophic-forgetting / RL's-Razor) | Explicit (selective-finetuning / O-LoRA, AlphaEdit) | Architectural (moe-adapters / LoRAMoE, BTX). Complementary, not competing. Open: RLVR-trained experts × router composition (the untested MoERA design question — RLVR experts would be KL-minimal/off-principal per RL's Razor).

**Wiki update.** catastrophic-forgetting expanded 1→8 pages (resolves the 2026-05-15 lint single-seed gap + the broken `[[../catastrophic-forgetting/_overview]]` link auto-fixed by the file now existing). New moe-adapters theme (8 pages). Index + revisions updated. Captures used absolute --out paths → CWD-drift bug avoided this run. mechanistic-forgetting model-scale verified against source.

**Next:** proceeding to apply ALL 2026-05-15 lint fixes (task 9).

## 2026-05-16 — Lint fixes applied (all of 2026-05-15 report)

All actionable items from the 2026-05-15 lint report fixed. Headline: the HIGH rlvr-incentivizes-reasoning miscitation (paper cited as support for the thesis it refutes, wrong author) corrected across index + 3 self-play pages + conflict file. Key meta-finding: 4 of 5 "genuine broken links" were lint-script false positives (3 distinct classes: in-page `[[#anchor]]`, Obsidian table-escaped `[[x\|y]]`, non-unique basename) — sharpened kit flag in master_notes 2026-05-16; the broken-link report is ~95% false-positive until the checker models Obsidian resolution. Weekly-brief↔ingest schema mismatch (12 pages) left to /harvest, not per-page-patched, per the report's own disposition. Resolution log appended to wiki/lint-reports/2026-05-15.md.

## 2026-05-17 — Weekly sweep (autonomous /weekly-brief)

Trend scan 2026-05-10→05-17 (alphaXiv/HF/Reddit/AK/Aran/Interconnects + arXiv listings). 15 candidates surfaced; 5 captured, 4 ingested, 1 dropped as duplicate. Theme of the week: **annotation-free / implicit process supervision** consolidating (uPRM unsupervised PRM; EP-GRPO implicit policy-divergence process signal; both join L2T/PAV as label-free process-reward family) and **the SFT-data floor for demonstration-guided RLVR collapsing** (FEST: 128 random traces, with a tuned-RL-baseline conflict). New pages: single-sample-rl-finetuning/fest, process-reward-models/uprm, rl-optimizers/ep-grpo, in-context-learning-theory/icl-conceptual-belief-space. Conflict opened: fest-tuned-rl-vs-demonstration-necessity. SGS (2604.20209) re-capture dropped — already on wiki since 2026-05-03 (trend scan mis-flagged as newly-trending). 8 watchlist additions (GRPO-process cluster, self-play, latent-reasoning, activation-steering cluster). All wiki + raw changes uncommitted on single-shot-training-wiki per no-commit policy; awaiting user commit on next login. Email + Telegram dispatched.
