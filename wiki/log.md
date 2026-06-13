# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-06-06] weekly-brief | 5 captured, 8 watchlisted

Autonomous weekly sweep (week of 2026-06-06). Sources scanned: HuggingFace Papers trending, arXiv cs.LG/cs.CL/cs.CV, Reddit r/MachineLearning+r/LocalLLaMA+r/MLScaling, alphaXiv trending, CVPR 2026 announcements. 5 papers captured and ingested; 8 added to watchlist.

**Captured and ingested:** [[cosmos-3]] (arXiv:2606.02800, NVIDIA — omnimodal MoT world model, #1 open T2I/T2V/I2V/robot-policy), [[polar-rl-harness]] (arXiv:2605.24220, NVIDIA — harness-agnostic async RL rollout, +22.6pt SWE-Bench), [[rlvr-incentivizes-reasoning]] (arXiv:2506.14245, MSRA/PKU — formal proof GRPO increases correct-CoT probability, CoT-Pass@K metric), [[deepseek-v4]] (HF model card — 1.6T MoE, hybrid CSA+HCA attention, mHC, Muon, SOTA open-source coding), [[mai-thinking-1]] (microsoft.ai announcement — 35B-active MoE, zero synthetic distillation, 97% AIME 2025).

**Conflicts updated:** [[conflicts/pure-video-vs-3d-world-models]] — added [[cosmos-3]] as Position B (interactive simulation without 3D scaffolds); [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — added Position E ([[rlvr-incentivizes-reasoning]]: CoT-Pass@K resolves metric-invalidity concern, formal theorem for GRPO incentivization).

---

## [2026-06-03] weekly-brief | 5 captured, 10 watchlisted

Autonomous weekly sweep (week of 2026-06-03). Sources scanned: Reddit r/MachineLearning+r/LocalLLaMA+r/MLScaling, HuggingFace Papers trending, arXiv cs.LG/cs.CL, Import AI #459. 5 papers captured and ingested; 10 added to watchlist.

**Captured and ingested:** [[skillopt]] (arXiv:2605.23904, Microsoft, top HF trending — text-space skill optimizer), [[high-entropy-tokens-rlvr]] (arXiv:2506.01939, NeurIPS 2025 — forking-token gradient masking), [[spurious-rewards-rlvr]] (arXiv:2506.10947 — GRPO clipping bias with random rewards yields +21pp), [[llamarl]] (arXiv:2505.24034, Meta — async RL framework 10.7× speedup at 405B), [[seal-self-adapting]] (arXiv:2506.10943, MIT/Harvard — RL-trained self-edit generation for weight updates).

**Conflict extended:** [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — added Position D ([[spurious-rewards-rlvr]]: clipping bias amplifies pretrained behaviors regardless of reward correctness; model-family-dependent).

---

## [2026-04-21] bootstrap | AI research and engineering trends

Initial bootstrap. Schema and commands tailored for AI research trends (LLM/SLM training, fine-tuning, RL, architectures, CV, evolutionary LLMs). Ready to receive first source.

## [2026-04-21] seed-radar | trend-following sources

Seeded `wiki/reference-sources.md` with curated X handles (AK, Karpathy, Aran Komatsuzaki, DAIR.AI, alphaXiv, Rohan Paul, Jack Clark), GitHub awesome-lists (Awesome-LLM, opendilab/awesome-RLHF, Awesome-LLM-Preference-Learning, awesome-reward-models, Awesome-System2-Reasoning-LLM, Awesome-Long-Chain-of-Thought-Reasoning, awesome-llms-fine-tuning, others), podcasts (Dwarkesh, Latent Space, Cognitive Revolution, TWIML, Practical AI), subreddits (MachineLearning, LocalLLaMA, MLScaling, LanguageTechnology, computervision), and Discord communities (EleutherAI, HF, Latent Space, Nous, LocalLLaMA). Extended the `/lint` DOMAIN-SLOT with a trend-radar-sweep step (fetch recent items, filter on-topic, propose for `/research`/`/ingest`, evolve the list). Radar is not yet captured — sources are pointers; capture happens on user approval during `/lint` or manual `/research`/`/ingest`.

## [2026-04-22] research+ingest | radar-2026-04 (first trend sweep)

First trend-radar-driven ingest: 10 sources captured via `/research` (2 URL captures — Titans+MIRAS Google Research blog, Moonlake world-models position post; 8 arXiv PDFs via marker) and ingested via the new subagent-per-source `/ingest` pipeline (10 parallel subagents each writing a structured `.ingest/<slug>.summary.md`, aggregator producing a page plan, single human gate, orchestrator writing wiki pages).

Topics span the wiki's full domain: test-time training / online memory (Titans, Hope, In-Place TTT), evolution strategies for post-training (EGGROLL), self-improving agents (Huxley-Gödel Machine), residual-stream architectures (mHC/DeepSeek), hybrid AR+diffusion decoding (TiDAR/NVIDIA), self-supervised vision (LeJEPA/LeCun), single-image view synthesis (SHARP/Apple), and world-model direction-setting (Moonlake).

Per user direction (auto mode): pruned to **10 paper pages + 1 cluster page ([[test-time-training]]) + 1 [[watchlist]] for ID'd-but-not-captured references + 7 conflict files in `wiki/conflicts/`**. All conflicts are forward-looking (the wiki was near-empty before this ingest, so no live contradictions; conflicts document positions that will resolve when counter-sources are captured).

Capture-pipeline note: the `/tmp/radar_captures.sh` batch script used a relative `--out` path while CWD was the target directory, causing marker PDFs to write to a doubly-nested `raw/research/radar-2026-04/raw/research/radar-2026-04/` path; all files were post-moved with `mv` and asset dirs merged. Also: initial GPU marker run hit CUDA illegal-memory-access due to contention with a concurrent `dynamic-transformer-block-condensation` training; fell back to CPU marker which took longer (~1 hour end-to-end; eggroll alone was 28 min at 249 pages). Flagging the relative-OUT gotcha as a kit-level improvement candidate for the next `/harvest`.

## [2026-04-22] weekly-brief | first manual dry-run (autonomous, uncommitted)

Shake-out run of the updated `/weekly-brief` skill (local execution, no auto-commit per the 2026-04-22 skill rewrite). Signal scan via WebSearch against alphaXiv/trending-arXiv queries surfaced 5 strong candidates in the 2026-04-15 → 2026-04-22 window; dedupe against existing wiki/ + `watchlist.md` left all 5 genuinely new. Selection heuristic picked **2 for capture** (novel-mechanism + conflict-load-bearing) and **3 for watchlist** (OpenWorldLib, SKILL0, SkillX).

Captures: `raw/research/weekly-2026-04-22/01-triattention.md` (arXiv:2604.04921) and `02-self-distilled-rlvr.md` (arXiv:2604.03128). Both marker runs OOM'd on the contended GPU; fell back to `--engine pymupdf` (manual — `capture_pdf` didn't auto-fallback). First pymupdf attempt used the `abs/` URL and captured the arXiv HTML abstract page rather than the PDF; re-ran with explicit `/pdf/` URLs. pymupdf-engine image refs written as repo-root-relative paths instead of the `./assets/<slug>/` convention used by marker output; post-processed with `sed`. Both pipeline bugs logged to `master_notes.md` as kit-scope `Status: open`.

Ingest via subagent-per-source (2 parallel `general-purpose` Agents, sonnet). Both summaries parsed clean against `parse_summary`; aggregator flagged one **spurious merge_candidate** on DOMAIN-SLOT marker tokens (known bug, `master_notes.md` entry from 2026-04-22) — ignored per skill's autonomous page-plan policy (one page per source unless ≥2 sources share a *real* concept with an existing cluster page). RLSD conflict has no `[[wiki-page]]` to contradict (OPSD has no existing coverage), so no conflict file was opened; paper page notes the theoretical position.

Wrote **2 paper pages** ([[triattention]], [[rlsd-self-distilled-rlvr]]) under autonomous heuristics — no human gate. All changes left uncommitted on `ai-trends-wiki`; email sent via Gmail MCP with bolded commit-reminder banner per the 2026-04-22 skill update. Dry-run outcome: full end-to-end pipeline exercises, 3 kit-level bugs surfaced + logged.

## [2026-04-27] weekly-brief | first cron-shape run (autonomous, uncommitted)

First weekly-brief run under the 2026-04-23 SMTP+HTML+watchlist-centric contract. Trend scan via sonnet subagent: WebSearch over alphaXiv / arXiv listings / HuggingFace trending / MarkTechPost / ICLR 2026 / r/MachineLearning surfaced 13 candidates; selection heuristic (multi-signal + technical novelty + wiki-fit + conflict-load-bearing + repro-positive) picked **5 for capture** and ~10 for watchlist.

Captures (`raw/research/weekly-2026-04-27/`, all `--engine pymupdf`, all clean on `audit_captures`): `01-mamba-3.md` (2603.15569), `02-hyperloop-transformers.md` (2604.21254), `03-neural-garbage-collection.md` (2604.18002), `04-token-gradient-cancellation.md` (2604.13088), `05-gepa-reflective-prompt-evolution.md` (2507.19457). pymupdf engine still writes repo-root-relative image paths — post-processed with the documented `sed` workaround (kit bug from 2026-04-22 still open). Two of the five picks fall outside the strict 2026-04-20→27 window (Mamba-3 March, GEPA July 2025) but are trending *this* week due to ICLR 2026 conference activity; per skill heuristic both included on multi-signal + conflict-load-bearing grounds.

Ingest: subagent-per-source (5 parallel `general-purpose` Agents, sonnet). All 5 summaries parsed clean against `parse_summary`; aggregator's `kind: "unknown"` page-plan parser bug from 2026-04-22 still surfaced on 3/5 entries (hyperloop, NGC, DFPO) — applied the autonomous one-page-per-source policy regardless. The DOMAIN-SLOT-token merge_candidate noise also still present (kit bug, ignored).

Page plan applied:
- **5 new paper pages**: [[mamba-3]], [[hyperloop-transformers]], [[neural-garbage-collection]], [[token-gradient-cancellation]], [[gepa-reflective-prompt-evolution]].
- **1 new conflict**: [[conflicts/ssm-vs-associative-memory-taxonomy]] — Mamba-3 §5.4 directly contradicts [[nested-learning]]'s MIRAS unifying claim.
- **2 existing conflicts extended**: [[conflicts/grpo-vs-evolution-strategies]] gains a prompt-space-evolution Position-A extension (GEPA), and [[conflicts/fixed-state-ssm-long-context]] gains a hybrid-only Position-B partial variant (Mamba-3).
- ~10 watchlist additions across the looped-Transformer cluster (ELT, Loop-Think-Generalize, Universal-Transformers-Need-Memory), GRPO-line peers (DAPO/DCPO/SSPO/GSPO/TEPO), prompt-opt prior art (MIPROv2, TextGrad, APO, Trace, MAP-Elites), KV-eviction baselines (SnapKV/KeyDiff/etc.), tooling (ml-intern), and CV (In Depth We Trust).

Cluster page [[test-time-training]] **not** extended — Hyperloop and Mamba-3 are TTT-adjacent (loop-as-depth-RNN; SSM-vs-MIRAS framing) but not TTT methods themselves. Per-page `Related` links carry the "see also" connection.

All changes left uncommitted on `ai-trends-wiki` per skill contract.

## [2026-05-04] weekly-brief | autonomous run (uncommitted)

Third weekly-brief run under the SMTP+HTML+watchlist-centric contract. Trend scan via sonnet subagent: alphaXiv trending / arXiv cs.LG-cs.CL-cs.CV May 1-4 listings / HuggingFace Papers / MarkTechPost / r/MachineLearning hot / ICLR 2026 oral+poster schedule / @CSVisionPapers surfaced 15 candidates; selection heuristic (multi-signal + technical novelty + wiki-fit + conflict-load-bearing + repro-positive) picked **5 for capture** and **10 for watchlist**.

Captures (`raw/research/weekly-2026-05-04/`, all `--engine pymupdf`, all clean on `audit_captures`): `01-tempo-test-time-rl.md` (2604.19295), `02-latent-grpo.md` (2604.27998), `03-vision-banana.md` (2604.20329), `04-agentflow.md` (2510.05592 ICLR Oral), `05-ssm-tool-use-length-generalization.md` (2510.14826 ICLR Oral). pymupdf engine still writes repo-root-relative image paths — applied the documented `sed` workaround (kit bug from 2026-04-22 still open). Two of the five picks (AgentFlow, To Infinity and Beyond) are 2510.x arXiv IDs trending *this* week due to ICLR 2026 oral acceptance — multi-signal + conflict-load-bearing per heuristic.

Ingest: subagent-per-source (5 parallel `general-purpose` Agents, sonnet). All 5 summaries parsed clean against `parse_summary`. Aggregator's DOMAIN-SLOT-token spurious merge_candidates still surfaced (kit bug from 2026-04-22, ignored per autonomous one-page-per-source policy).

Page plan applied:
- **5 new paper pages**: [[tempo-test-time-rl]], [[latent-grpo]], [[vision-banana]], [[agentflow]], [[ssm-tool-use-length-generalization]].
- **2 conflicts extended**:
  - [[conflicts/fixed-state-ssm-long-context]] gains the formal proof of Position A (Apple paper Theorem 2.1) **and** a new tool-augmented Position-B variant (Theorem 2.2 — interactive tool-use as third escape, distinct from Mamba-3's hybrid path). Three Position-B paths now on file: hybrid-with-attention (Mamba-3, partial), tool-augmented (this week), and the orthodox pure-fixed-state defence (still uncaptured).
  - [[conflicts/pure-video-vs-3d-world-models]] gains a partial Position-B (static-3D-priors-from-2D-generation) via Vision Banana's δ1=0.929 zero-shot depth without intrinsics. Conflict's framing is now: static priors recoverable from 2D generation (yes per Vision Banana) vs interactive simulation with action conditioning (still open).
- **10 watchlist additions** across architectures (MoDr looped-Transformer-MoE; SDVG speculative-decoding-for-AR-video), latent-reasoning sibs (LEPO, Thinking Without Words), reward-modeling theme (ThinkPRM, Reward-Models-Are-Value-Functions), RL systems (Spec-RL rollout acceleration), CV/3D world-models (World-R1, PERSIST, Tuna-2).

No new conflict files opened this run — every flagged contradiction extended an existing open conflict. No cluster-page extensions: TEMPO is a strong fit for [[test-time-training]] cluster but autonomous policy requires ≥2 sources sharing the cluster page in a single run; cross-link via `Related:` only.

All changes left uncommitted on `ai-trends-wiki` per skill contract.

## [2026-05-11] weekly-brief | autonomous run (uncommitted)

Fourth weekly-brief run. Trend-scan subagent (sonnet) surveyed alphaXiv trending / arXiv cs.LG-cs.CL-cs.CV May 5-11 / HuggingFace Papers / papers.cool / r/MachineLearning hot / ICLR 2026 Outstanding-Paper announcements / RLVR & DLM awesome-list activity; 15 candidates surfaced. Selection heuristic picked **5 for capture** and **10 for watchlist**.

Captures (`raw/research/weekly-2026-05-11/`, all `--engine pymupdf`, all clean on `audit_captures`): `01-reasonmaxxer.md` (2605.06241), `02-sst-v2.md` (2605.00206), `03-scalelogic.md` (2605.06638), `04-memagent.md` (2507.02259 ICLR Oral), `05-coladlm.md` (2605.06548). pymupdf image-path workaround applied as documented (kit bug from 2026-04-22, still open). MemAgent is a July 2025 arXiv submission trending now post-ICLR-2026.

Ingest via subagent-per-source (5 parallel `general-purpose` Agents, sonnet). All 5 summaries parsed clean against `parse_summary`. Aggregator DOMAIN-SLOT spurious merge_candidates surfaced as expected (kit bug 2026-04-22); ignored per autonomous one-page-per-source policy.

Page plan applied:
- **5 new paper pages**: [[reasonmaxxer]], [[sst-v2]], [[scalelogic]], [[memagent]], [[coladlm]].
- **1 new conflict file**: [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — ReasonMaxxer's "1–4% reranked positions causally reproduce RL accuracy" finding directly contradicts the premise of [[token-gradient-cancellation]]'s DFPO line that fixing gradient cancellation across many tokens is the load-bearing problem.
- **2 conflicts extended**:
  - [[conflicts/fixed-state-ssm-long-context]] gains **Position C** (Transformer + nonlinear horizontal state, via [[sst-v2]]) and **Position B (RL-trained memory overwrite)** (via [[memagent]]). The Apple Theorem 2.1 scope (GSSMs with linear or near-linear dynamics) does not directly bind either path.
  - [[conflicts/long-context-attention-vs-recurrent-memory]] gains MemAgent as a third-path alternative (RL-trained explicit memory overwrites with a Transformer backbone, escaping the binary).
- **10 watchlist additions**: Joint Latent DLM, Break the Block (diffusion-LM cluster siblings of ColaDLM); FLUID (ODE-based hybrid attention/CT-RNN); IOP-GSPO (outcome→process supervision); RAO (recursive agent self-delegation); UCPO (diversity-preserving RLVR); ResRL (SVD-projection negative-sample gradient surgery); Tool-Calling-Linearly-Readable (mechanistic interp of tool selection); ICLR 2026 Outstanding "Transformers are Inherently Succinct"; ICLR 2026 Honorable "Polar Express" (Muon optimizer theory).

ColaDLM ingest subagent over-stepped its scope and updated `index.md`, `log.md`, `revisions.md` with manual-write entries for ColaDLM-only; orchestrator reconciled by replacing with this weekly-brief block covering all 5 pages, and adding the other 4 papers to index.md. Flagged for `master_notes.md` as a kit-level prompt-template issue (subagent scope must be tightened to "write the named page only — don't touch meta files").

All changes left uncommitted on `ai-trends-wiki` per skill contract.

## [2026-05-18] weekly-brief | autonomous run (uncommitted)

Fifth weekly-brief run. Trend-scan subagent (sonnet) surveyed alphaXiv weekly trending / HuggingFace Daily+Trending Papers (AK proxy) / arXiv cs.LG-cs.CL-cs.CV May 11–18 / paperswithcode→HF redirect; 15 candidates surfaced. Reddit r/MachineLearning + r/LocalLLaMA fetch was gated (no subreddit signal this week — noted). Candidate #10 (ReasonMaxxer 2605.06241) dropped as already covered ([[reasonmaxxer]], 2026-05-11 run). Selection heuristic picked **5 for capture** and **10 for watchlist**.

Captures (`raw/research/weekly-2026-05-18/`, all `--engine pymupdf`): `01-elf-embedded-language-flows.md` (2605.10938), `02-delta-mem.md` (2605.12357), `03-orthrus.md` (2605.12825), `04-asymflow.md` (2605.12964), `05-sensenova-u1.md` (2605.12500). `audit_captures` load-bearing checks clean (0 thin, 0 missing-source, 0 collisions); the 107 "broken image refs" are the known pymupdf image-path kit bug (open in `master_notes.md` since 2026-04-22) — cosmetic for text-only ingest, all extractions substantial (883–2768 lines). Proceeded as prior 4 runs did.

Ingest via subagent-per-source (5 parallel `general-purpose` Agents, sonnet). All 5 summaries parsed clean against `parse_summary`; run.json status ok ×5. Aggregator DOMAIN-SLOT spurious merge_candidates (domain/prompts/slot/takeaway) surfaced as expected (kit bug 2026-04-22); ignored per autonomous one-page-per-source policy.

Page plan applied:
- **5 new paper pages**: [[elf-embedded-language-flows]], [[delta-mem]], [[orthrus]], [[asymflow]], [[sensenova-u1]].
- **1 new conflict file**: [[conflicts/pixel-space-vs-latent-space-generation]] — [[sensenova-u1]] (pixel-space, no VAE; 32× compression matches FLUX.1-dev VAE PSNR at 8×) + [[asymflow]] (AsymFLUX.2 pixel-finetune beats FLUX.2-klein latent base; ImageNet FID 1.57) vs the existing [[coladlm]] latent-VAE-is-the-scaling-direction claim. Load-bearing (2 new sources + existing wiki anchor, direct contradiction with an existing page claim); resolution rule scoped per-domain, CoLa-DLM's high-compute claim flagged unrefuted at its own scale.
- **2 conflicts extended** with δ-mem ([[delta-mem]]): [[conflicts/long-context-attention-vs-recurrent-memory]] gains Position C′ (hybrid: frozen full-attention backbone + gated delta-rule online state; supplies the memory-skeptical critique the empty Position-B slot wanted, answers it against attention-scaling); [[conflicts/fixed-state-ssm-long-context]] gains Position C′ (fixed 8×8 state, not a GSSM, outside Apple Theorem 2.1 scope — distinguished from sst-v2's FFN state and memagent's RL overwrite).
- **[[tidar]] comparison**: added "Comparison: Orthrus" subsection (frozen-backbone KL-distilled lossless vs adapted-backbone rejection-sampling; speedup-figure gap is a setup/metric difference, explicitly *not* a conflict ruling).
- **ELF "continuous beats discrete DLM"**: forward-looking, no existing wiki contradiction, no open conflict on that theme → discarded per skill's no-speculative-weekly-conflict policy (noted as a positioned claim within [[elf-embedded-language-flows]] only).
- **10 watchlist additions**: Mean Mode Screaming, MatryoshkaLoRA, SU-01, SDAR, Geometry Conflict, Darwin Family (low-confidence, flagged for follow-up), AnyFlow, SANA-WM, Causal Forcing++, MinT.

Page-writer subagents given tight scope ("write ONLY the named page; do not touch meta files") in response to the 2026-05-11 ColaDLM scope-overstep; orchestrator handled all conflict files + index/log/revisions/watchlist itself. No scope oversteps observed this run.

Pre-existing uncommitted changes at run start (prior 2026-05-04 + 2026-05-11 weekly-brief output not yet committed by the user): flagged separately in the email run-notes so this week's diff is distinguishable. This run further extended two conflict files already among that pre-existing set (unavoidable — skill requires extending open conflict files).

All changes left uncommitted on `ai-trends-wiki` per skill contract — fifth run.

## [2026-05-25] weekly-brief | autonomous run (uncommitted)

Sixth weekly-brief run. Trend-scan subagent (sonnet) surveyed alphaXiv weekly trending + HuggingFace Daily Papers (AK proxy, May 18–25) + web-search verification; ~18 candidates surfaced. Reddit (r/MachineLearning, r/LocalLLaMA) gated again (old.reddit blocked); X/AK direct inaccessible (AK routed via HF). Selection picked **5 for capture**, **10 for watchlist**.

Captures (`raw/research/weekly-2026-05-25/`, all `--engine pymupdf`): `01-gated-deltanet-2` (2605.22791), `02-hrm-text` (2605.20613), `03-gram-recursive-reasoning` (2605.19376), `04-anti-self-distillation` (2605.11609), `05-delta-token-credit` (2605.21467). All 5 downloaded + converted clean (67–98 KB). `audit_captures` load-bearing checks clean (0 thin / 0 missing-source / 0 collisions); 25 broken image refs = known pymupdf image-path kit bug (`master_notes.md` since 2026-04-22), cosmetic for text ingest. Note: `poetry` was not on the non-login-shell PATH this run — used `~/.local/bin/poetry` (prior runs had it on PATH; session-specific, not a kit bug).

Ingest via subagent-per-source (5 parallel `general-purpose` Agents, sonnet). All 5 summaries parsed clean against `parse_summary`; run.json ok ×5. Aggregator DOMAIN-SLOT spurious merge_candidates (domain/prompts/slot/takeaway) surfaced as expected (kit bug 2026-04-22); ignored per one-page-per-source policy.

Page plan applied:
- **5 new paper pages** (page-writer subagents, tight scope): [[gated-deltanet-2]], [[hrm-text]], [[gram-recursive-reasoning]], [[anti-self-distillation]], [[delta-token-credit]]. No scope oversteps.
- **2 conflicts extended** (orchestrator): [[conflicts/fixed-state-ssm-long-context]] gains "B (decoupled-gate fixed-state recurrent)" — GDN-2 in pure-recurrent mode beats Mamba-2/GDN/KDA/Mamba-3 SISO+MIMO at 1.3B and on MK-NIAH retrieval; ablation shows decoupling the erase gate (not enlarging state) is the lever → nearest thing yet to the long-vacant orthodox Position-B slot, but wins via update rule not state size. [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] gains Position C — DelTA's discriminator view (shared/formatting tokens dominate both centroids; bottom-λ tokens *actively collapse* training, i.e. net-negative not merely inert); bridges Position A (sparse) and B (cancellation) with a distinct surrogate-reweighting fix.
- **2 comparison notes** (orchestrator, not conflict files): [[mamba-3]] "Comparison: Gated DeltaNet-2" (GDN-2 displaces it as recurrent SOTA at 1.3B; rebuts mamba-3's hybrid concession); [[rlsd-self-distilled-rlvr]] "Comparison: AntiSD" (AntiSD finds *default* SD underperforms GRPO — but RLSD's decoupled SD is a different instantiation; both beat GRPO faster, different fixes, same diagnosis).
- **No new conflict files**: HRM-Text's "instruction-pairs-only-from-scratch challenges Chinchilla raw-text scaling" and GRAM's stochastic-RRM framing are forward-looking with no current wiki contradiction and no open conflict on those themes → captured in-page only, per the no-speculative-weekly-conflict policy.
- **10 watchlist additions**: Equilibrium Reasoners, Full Attention Strikes Back, ConvexTok, Vector Policy Optimization, Memory-R2, HINT-SD, GoLongRL, Rethinking Muon (arXiv ID unverified — flagged), WorldKV, OScaR.

Trend read this week: recurrent-depth / latent-fixed-point reasoning surged (GRAM + HRM-Text + Equilibrium Reasoners); per-token RL credit-assignment cluster deepened (AntiSD + DelTA + Vector Policy Optimization); delta-rule linear attention reasserted over selective-SSM SOTA (GDN-2 vs Mamba-3).

Pre-existing uncommitted changes at run start: prior 2026-05-04 / 2026-05-11 / 2026-05-18 weekly-brief output never committed by the user — flagged separately in the email run-notes so this week's diff stays distinguishable. This run again unavoidably extended conflict/index/log/revisions/watchlist files already in that pre-existing set (skill requires extending open conflict + meta files).

All changes left uncommitted on `ai-trends-wiki` per skill contract — sixth run.

---
2026-06-01 — /research openclaw-memory

Topic: OpenClaw as a memory system for Claude Code.
Sources captured: 8 (2 failed — learnopenclaw.ai SSL cert expired, milvus.io 403 bot-wall).
Pages written: [[openclaw]], [[openclaw-claude-code-memory]].
New index section: "Agent frameworks & memory".
Key findings: OpenClaw's four-layer Markdown-based memory (bootstrap / JSONL transcript / context window / SQLite retrieval index); Hindsight as the shared-bank bridge to Claude Code; Anthropic explicitly rejected subscription-scale always-on third-party agents (Apr 2026) — production pattern is a dedicated API harness, not Claude Code subscription.

---
2026-06-13 — /weekly-brief (weekly radar sweep)

Sources scanned: ~18 (HF Papers trending, arXiv cs.LG/cs.CL, Reddit r/ML+r/LocalLLaMA, alphaXiv, web search).
Candidates surfaced: 18; selected 5 for capture.
Captures attempted / succeeded: 5 / 5 (magistral, spurious-rewards-rlvr, reinforcement-pretraining, high-entropy-tokens-rlvr, rl-teachers).
Note: audit_captures flagged 15 "broken image refs" for pymupdf captures — assets DO exist at raw/research/weekly-2026-06-13/assets/<slug>/; the tool is checking from the wrong base directory (kit-level issue, logged to master_notes.md).
Pages written: 3 new (magistral, reinforcement-pretraining, rl-teachers); 2 already existing (spurious-rewards-rlvr, high-entropy-tokens-rlvr — no new pages needed).
Watchlist additions: 8 (DRPO, SSA, RuleReasoner, EASE-TTT, Fisher-MoE, Rewarding-the-Unlikely, Robust-U1, Generalization-Hacking).
Conflicts extended: none (Magistral's pure-RL result is supportive of existing Position A/E in sparse-policy-selection conflict; not a new position).
