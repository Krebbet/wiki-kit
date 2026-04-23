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
