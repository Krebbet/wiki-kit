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

