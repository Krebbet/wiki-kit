# Wiki Log

Append-only chronological record of wiki activity.

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
