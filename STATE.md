# Resume State — single-sample-llm-learning research run

This file is a checkpoint written before a planned computer reboot. Everything below describes work that was in flight or completed at the time of the snapshot, and what to do next.

**Snapshot time:** 2026-04-19 (late in session)
**Branch:** `single-shot-training-wiki`
**Topic dir:** `raw/research/single-sample-llm-learning/`

## Mission

Build a robust research wiki for David's project: a novel fine-tuning method for small LLMs (1–40B params) emphasising single-sample, concept-based learning. The wiki must contain (a) raw verbatim PDFs of all identified articles + (b) markdown extractions with images + (c) synthesized, cross-referenced wiki pages with citations.

## What was running when the snapshot was taken

1. **Background capture queue** (bash job, dies on reboot): sequentially captured papers `01–09` from the initial shortlist using `marker --engine cpu`. At snapshot, queue had completed papers `01, 02, 03, 04` and was on paper `06` (paper `05` had a 404 on the convert-from-URL path but the PDF was retrieved separately via `curl ...v1`).

2. **8 parallel research subagents** (clusters A–H, also die on reboot). Each was tasked to: search → capture top 3–5 papers via `TORCH_DEVICE=cpu poetry run python -m tools.capture_pdf ... --engine marker`, plus `curl` the raw PDF separately. None had reported back at snapshot.

3. **PDF backfill curl loop** (already finished): downloaded raw `*.pdf` for the original 9 shortlisted papers into `raw/research/single-sample-llm-learning/pdfs/`.

## What's already on disk (committed)

### Markdown extractions (15 files at snapshot)

```
01-01-rl-one-training-example.md           ← arXiv:2504.20571 (queue 01)
02-02-critique-ft-one-problem.md           ← arXiv:2506.03295 (queue 02)
03-03-rlvr-incentivizes-reasoning.md       ← arXiv:2506.14245 (queue 03)
04-B-1-maml-finn.md                        ← MAML (Finn et al.)
05-C-1-lets-verify-step-by-step.md         ← OpenAI process supervision
06-E-1-ttt-few-shot-akyurek.md             ← TTT for few-shot (Akyürek)
07-D-1-star-self-taught-reasoner.md        ← STaR (Zelikman et al.)
08-G-1-self-refine.md                      ← Self-Refine
09-C-2-math-shepherd.md                    ← Math-Shepherd PRM
10-B-2-prototypical-networks-snell.md      ← Prototypical Networks (Snell)
11-D-2-self-rewarding-language-models.md   ← Self-Rewarding LMs (Yuan et al.)
12-C-3-uesato-process-outcome-feedback.md  ← Uesato process vs outcome
13-E-2-algorithm-distillation-icrl.md      ← Algorithm Distillation
14-04-learning-to-think.md                 ← arXiv:2505.10425 (queue 04)
15-G-2-constitutional-ai.md                ← Constitutional AI
```

The double-prefixed filenames (e.g. `04-B-1-...`) come from `tools/capture_pdf.py` auto-prepending its own sequence number to the slug. Cosmetic only — content is fine. Logged in `FEEDBACK.md`.

### Raw PDFs (29 files at snapshot)

Mirror under `raw/research/single-sample-llm-learning/pdfs/`. PDFs exist for *all* in-flight captures (clusters and queue), including ones whose markdown extraction hadn't completed yet — see "What's missing" below.

## What's missing (work to redo on resume)

These have raw PDFs but no markdown extraction — the marker conversion was either in flight or queued when reboot interrupted it. **Re-run capture_pdf with `--engine marker` and `TORCH_DEVICE=cpu` for each one.** The PDFs themselves are already on disk, so use `--src raw/research/single-sample-llm-learning/pdfs/<slug>.pdf` rather than re-fetching from arXiv.

### Queue tail (papers 05–09)

| Slug | arXiv | Notes |
|---|---|---|
| `05-rl-sparse-subnetwork` | 2507.17107 | Use `pdfs/05-rl-sparse-subnetwork.pdf` (originally needed `v1` suffix to fetch) |
| `06-data-efficiency-rft` | 2506.05316 | |
| `07-recursive-concept-evolution` | 2602.15725 | |
| `08-learning-from-one-shot` | 2201.08815 | |
| `09-ft-limited-data-survey` | 2411.09539 | Survey |

### Cluster A (in-context learning theory)

`A-1-induction-heads`, `A-2-icl-as-gradient-descent`, `A-3-icl-bayesian-inference`, `A-4-function-class-icl` — all 4 PDFs present, 0 markdowns.

### Cluster C (process reward models) — 1 missing

`C-4-cobbe-training-verifiers-gsm8k` — PDF present, no markdown.

### Cluster D (self-improvement) — 1 missing

`D-3-rstar-math` — PDF present, no markdown.

### Cluster F (RLVR mechanics) — 1 missing

`F-1-deepseekmath-grpo` — PDF present, no markdown.

### Cluster G (critique/self-correction) — 1 missing

`G-3-reflexion` — PDF present, no markdown.

### Cluster H (concept learning) — 1 missing

`H-1-concept-bottleneck-models` — PDF present, no markdown.

**Also:** clusters A, F, H may have intended to capture more papers beyond what's in `pdfs/`. Their search shortlists are gone. After the missing markdowns are produced, re-dispatch agents *only for clusters that have suspiciously few captures* (probably A, F, H) and instruct them to read their PDFs already on disk before deciding what additional papers to pursue.

## Continuation plan (post-reboot)

1. **Re-run missing markdown captures** (sequential, CPU only). Total: ~12 papers × ~3 min = ~40 min. Use a script like:

   ```bash
   TORCH_DEVICE=cpu
   for pdf in raw/research/single-sample-llm-learning/pdfs/*.pdf; do
     slug=$(basename "$pdf" .pdf)
     md="raw/research/single-sample-llm-learning/${slug}.md"
     # Note the double-prefix — files are <N>-<slug>.md not <slug>.md.
     # Glob check instead:
     if ls raw/research/single-sample-llm-learning/*-${slug}.md 2>/dev/null; then continue; fi
     poetry run python -m tools.capture_pdf --src "$pdf" --out raw/research/single-sample-llm-learning --slug "$slug" --engine marker
   done
   ```

2. **Verify** all expected files have md + pdf pairs.

3. **Top up sparse clusters** (A, F, H) with new search agents if coverage feels thin after step 1.

4. **Dispatch synthesis agents** (one per major theme) to write `wiki/research/<theme>/<page>.md` files following the page format. Themes likely: `single-sample-rl-finetuning/`, `process-reward-models/`, `self-improvement/`, `meta-learning-and-icl/`, `test-time-training/`, `concept-learning/`, `critique-and-debate/`.

5. **Build `wiki/index.md`** properly — currently has only the bootstrap one-liner.

6. **Run `/lint`** to surface gaps, broken links, missing cross-refs.

7. **Produce primary-findings readout** for the user.

## How to resume

**User actions after reboot:**

```bash
cd /home/david/code/wiki-kit
claude --continue   # to resume this exact conversation with full context
# OR
claude              # then say: "Resume from STATE.md — execute the continuation plan."
```

`claude --continue` is preferred; the full conversation history (including all previous tool calls, the bootstrap output, the agent dispatches, and the FEEDBACK/master_notes updates) re-loads. The task list persists server-side so it'll still show where things stand.

If `--continue` doesn't work for some reason, a fresh `claude` invocation reading `STATE.md` + `master_notes.md` + `FEEDBACK.md` + the existing files in `raw/research/single-sample-llm-learning/` is enough to resume.

**No GPU touch required for any of this.** The user's experiment can keep running.
