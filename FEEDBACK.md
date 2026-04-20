# Feedback — single-shot-training-wiki test run

Scratchpad for friction points, bugs, and improvement ideas surfaced while using wiki-kit on a real domain. Each entry is raw input — triage, dedupe, and route to issues/PRs later.

## Format

```
### YYYY-MM-DD — short title
**Where:** command / file / step that triggered it
**What happened:** observed behavior
**Expected / wanted:** what would have been better
**Severity:** blocker | annoying | nit | idea
**Notes:** optional — possible fix, related entries
```

---

## Entries

<!-- Add entries below, newest first. -->

### 2026-04-20 — capture_pdf has TWO image-fidelity bugs (FIXED on this branch)
**Where:** `tools/capture_pdf.py` (pre-fix); fix applied on `single-shot-training-wiki` branch.
**What happened:** Two compounding bugs caused ~33% image loss across a 30-paper batch:
1. **Broken image refs.** Marker emits `![](_page_X.jpeg)` with bare filenames. The tool saved images to `<out>/assets/`, so the bare ref `_page_X.jpeg` resolves to `<out>/_page_X.jpeg` — wrong dir. Markdown viewers couldn't render any image.
2. **Cross-paper collision.** All papers in the same `<out>` shared one `assets/` dir. Marker's `_page_N_TYPE_M.jpeg` naming collides across papers (most papers have a `_page_0_Picture_0.jpeg`). Later captures silently overwrote earlier ones, so even when a ref resolved, it might point to the *wrong paper's* image.
**Diagnosis:** counted 220 unique image refs across 22 captured MDs vs 148 actual files in `assets/` — 72 broken refs from collisions, plus 100% of refs broken by path mismatch.
**Fix:** namespaced asset dir per slug (`assets/<slug>/...`) and added `_rewrite_image_refs` regex that prefixes bare filenames with the namespaced path. Frontmatter `assets_dir` now reflects the per-slug path.
**Severity:** blocker for figure-bearing wikis (which is most research wikis).
**Notes:** This fix should be backported to `main`. Should also be regression-tested with a multi-paper integration test before next release.

### 2026-04-20 — wiki-kit needs a built-in capture-fidelity audit
**Where:** workflow / `/lint` or new tool
**What happened:** The bugs above went undetected because nothing in the workflow systematically checks that markdown image refs resolve to actual files. The user surfaced this by asking. Future users won't necessarily know to ask.
**Expected / wanted:** Build a fidelity audit into the kit so every wiki gets the check by default. Concrete proposals:
- A `tools/audit_captures.py` that, for each MD under `raw/`, (a) parses image refs, (b) verifies each resolves to a real file relative to the MD, (c) verifies the source PDF exists alongside (in `pdfs/` or paired path), (d) compares MD line count vs PDF page count for sanity (flag MDs <10 lines per page as suspicious), (e) reports collisions where the same image filename is referenced by multiple MDs.
- `/lint` should call this for any topic dir present under `raw/`, not just wiki pages.
- Could also run automatically as a post-capture hook from `/research`.
**Severity:** structural improvement (proposed)
**Notes:** Per the user: "the fidelity check should be something we want to implement for all wiki-start ups". Strong candidate for `main` branch + bake into the lint command's domain-agnostic checks.

### 2026-04-19 — capture_pdf doesn't preserve source PDF
**Where:** `tools/capture_pdf.py`
**What happened:** The tool downloads a remote PDF, converts to markdown via marker/pymupdf, and discards the source. The user explicitly wants raw verbatim PDFs kept alongside the markdown extraction (markdown + extracted images is a derived view, not a replacement for the source).
**Expected / wanted:** Add a `--keep-source` flag (default true for remote URLs) that saves the downloaded PDF next to the markdown output. Naming convention: same slug, `.pdf` extension. Or: drop into a `pdfs/` subdirectory.
**Severity:** annoying (currently working around with a separate `curl` loop)
**Notes:** Verbatim source preservation is also auditing-friendly — markdown extractions can drift from the source as marker versions change.

### 2026-04-19 — capture_pdf marker engine assumes free GPU
**Where:** `tools/capture_pdf.py --engine marker`
**What happened:** Default marker invocation tried CUDA and crashed with OOM because another process held 22 GB of 23 GB on GPU 0. Workaround: `TORCH_DEVICE=cpu poetry run python -m tools.capture_pdf ...` — works, but 5–10× slower (~3 min/paper instead of ~30 s).
**Expected / wanted:** Either (a) auto-detect GPU memory and fall back to CPU, (b) accept a `--device {auto,cuda,cpu}` flag passed through to marker, (c) document `TORCH_DEVICE=cpu` in the first-run notes section of the README alongside the existing `--engine pymupdf` lightweight tip.
**Severity:** annoying
**Notes:** This is a real-world friction point on machines that share a GPU with other workloads (very common). The README mentions the model-weights download but assumes the GPU is available.

### 2026-04-19 — bootstrap should ask about GPU availability
**Where:** `/bootstrap` interview
**What happened:** Bootstrap recommended `--engine marker` for ArXiv as the default for figure-preserving PDF capture without surfacing the GPU dependency.
**Expected / wanted:** Either ask the user "do you have a free GPU?" during interview, or always recommend pymupdf as the default and note that marker is a quality upgrade if GPU is available.
**Severity:** nit
**Notes:** Could also detect GPU availability programmatically and bake the choice into the source-type-notes slot.

