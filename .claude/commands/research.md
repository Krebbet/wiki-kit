# Research and Update Wiki

Find authoritative external sources on a topic, capture them via the `tools/` scripts, and integrate via `/ingest`.

## Arguments

$ARGUMENTS — the topic to research.

## Critical Rules

- **Capture scripts are the default.** Use `tools/capture_url.py`, `tools/capture_pdf.py`, `tools/fetch_transcript.py`. Playwright MCP is for interactive inspection only; the scripts handle programmatic capture including image download.
- **Never use `WebFetch` to capture source content.** It returns LLM-summarised content, not the original page. Summaries cannot be used as raw sources.
- **`WebSearch` may be used only to find candidate URLs.** Treat its output as a list of pointers, never as content. Do not quote, paraphrase, or draw claims from search-result snippets.
- **No synthesised knowledge.** Every claim that lands in the wiki must trace back to a captured raw source file. Do not write content from training knowledge and cite URLs you haven't actually seen the captured content of.
- **Source attribution must be unambiguous.** Every substantive claim in the wiki must be traceable to either a captured raw source file or an existing wiki page. Never blend the two in the same sentence or bullet.
- **Editorial framing must be labelled.** Any cross-source synthesis, comparison, gap analysis, recommendation, or "open question" you produce is *your interpretation*, not source content. Mark it clearly (headings like "Cross-source themes", "Comparison to our wiki", "Open questions"; or inline tags like *(synthesis)*, *(editorial)*).
- **Never put your own opinions into voice as if they were source claims.** If you say "X recommends Y", Y must be a direct extraction from a captured X source.

<!-- DOMAIN-SLOT: authoritative-sources -->
**Sources for this wiki span a wide range** and are recorded with **origin / intended audience / purpose** metadata plus a **trust tag** so the reader can judge for themselves. Priority lanes: peer-reviewed academic work (economics, antitrust, law reviews, STS), investigative journalism (ProPublica, The Markup, Reuters, reputable beat reporters), advocacy-org primary materials (EFF, Open Markets Institute, Public Citizen, platform-coop networks), government and regulatory filings (FTC, EU Commission, court dockets, SEC), and Wikipedia as a *starting* reference — always chase the footnote trail to the primary source when a claim is load-bearing. Books, talks, and podcasts are acceptable. There is no hard trust hierarchy; the only filter is spam / slop. When a source has a clear political stance or commercial interest, record it in the source metadata rather than excluding the source.
<!-- /DOMAIN-SLOT -->

## Process

1. **Check existing coverage** — Read `wiki/index.md` and any existing pages on the topic. Note what the wiki already covers so you don't duplicate.

2. **Find candidate sources** — Use `WebSearch` to find candidates. Collect a shortlist of 5–10 URLs. For each, note only title, URL, and source type. **Do not summarise content** — the search snippet is not a usable source.

3. **Present the shortlist to the user** — Show candidate URLs with descriptions. Ask which to capture. The user may reject, reorder, add their own, or ask for a different search.

4. **Capture with the appropriate tool.** For each approved URL, run:

   - **Web page (HTML):**
     ```bash
     poetry run python -m tools.capture_url --url <URL> --out raw/research/<topic-slug> --slug <short-slug>
     ```
     Add `--js` if the page is JS-heavy.

   - **PDF (URL or local path):**
     ```bash
     poetry run python -m tools.capture_pdf --src <URL-or-path> --out raw/research/<topic-slug> --slug <short-slug>
     ```
     Default engine is `marker` (best for papers). For simple PDFs or to skip the model weight download, add `--engine pymupdf`.

   - **YouTube video:**
     ```bash
     poetry run python -m tools.fetch_transcript --url <URL> --out raw/research/<topic-slug> --slug <short-slug>
     ```

   Each tool prints the written file path on success and exits non-zero with a stderr message on failure.

   <!-- DOMAIN-SLOT: source-type-notes -->
   **Source-type guidance for this wiki:**
   - **Web articles, Substack, org blogs, news** → `capture_url.py`. Add `--js` for sites that render content client-side (most modern sites).
   - **Wikipedia pages** → `capture_url.py`. Treat as starting reference, not final authority — chase the footnote trail to primary sources when a claim matters.
   - **Academic papers (ArXiv, SSRN, law reviews, NBER, Brookings)** → `capture_pdf.py` with `--engine marker`. Prefer preprint / open-access. Capture the PDF for content and (for ArXiv) the abs page for the bibliographic record.
   - **Government / regulatory docs (FTC filings, EU reports, court dockets, SEC filings)** → `capture_pdf.py`. Capture the original filing, not journalism about it.
   - **Books and book chapters (PDFs)** → `capture_pdf.py --engine marker`. Note copyright status in the source metadata.
   - **YouTube talks and podcasts** → `fetch_transcript.py`. Note in the wiki page that the source is a transcript (timestamps available, no figures).
   - **Organisation websites** → `capture_url.py`. Prefer "about / mission / methods" pages over blog posts when establishing what an org does.
   - **Primary data or datasets** — if it's a downloadable file, drop it into `raw/` manually and ingest.
   <!-- /DOMAIN-SLOT -->

5. **Verify captures.** After capture, read a few lines of each written file to confirm it's real content (not a bot wall, login page, or empty extraction). If a capture is clearly broken, try the Playwright MCP tool directly to inspect the page and diagnose.

   Then run the fidelity audit on the topic directory:

   ```bash
   poetry run python -m tools.audit_captures raw/research/<topic-slug>
   ```

   The audit checks that every image ref in each captured markdown resolves to a real file, that source PDFs are paired, and that no two markdowns reference the same image (cross-paper overwrite indicator). Re-capture any paper flagged with broken refs or thin extraction before proceeding to `/ingest` — silently-corrupted captures will produce wiki pages with broken figure links.

6. **Integrate via `/ingest`** — Invoke `/ingest raw/research/<topic-slug>` on the topic directory. `/ingest` reads the raw files, discusses takeaways, writes wiki pages with source-traceable claims, and updates tracking files.

7. **Report.** Separate three things:
   - **What the sources said** — faithful summary of each captured file, per file.
   - **What was changed in the wiki** — pages created or modified, cross-references added.
   - **Open questions for the user** — conflicts, gaps, or decisions that need a ruling.

8. **Harvest checkpoint.** Did anything surface during this research run that would help *any* wiki, not just this one? Examples: a capture tool bug, a failure mode worth documenting in this file itself, a heuristic for judging source authority that generalises. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline. `/harvest` will pick it up.
