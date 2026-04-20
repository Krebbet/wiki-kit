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
**Authoritative sources for this wiki are:** (a) papers from established ML labs (Anthropic, DeepMind, OpenAI, Meta FAIR, Google Brain/Research, MILA, etc.) and well-cited authors; (b) peer-reviewed venues (NeurIPS, ICML, ICLR, ACL, EMNLP) or ArXiv preprints with strong follow-on citations; (c) primary methodology papers over surveys when both exist — treat surveys as roadmaps, not ground truth. When citing an ArXiv paper, capture both v1 and the latest version if claims diverge between revisions. Avoid: marketing posts, vague claims without methodology, benchmark cherry-picks, blog summaries of papers (capture the paper itself).
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
   - **ArXiv abstract pages or PDF URLs** → use `capture_pdf.py` with `--engine marker` (preserves figures and equations, which are usually load-bearing).
   - **Lab blog posts and web articles** → use `capture_url.py`. Add `--js` for sites that render content client-side (most modern lab blogs).
   - **YouTube conference talks** → use `fetch_transcript.py`. Note in the wiki page that the source is a talk transcript (timestamps, no figures).
   - **Prefer arXiv over journal paywalls** when both exist. If only the paywalled version is canonical, still capture the arXiv preprint and note the divergence.
   - **Prefer arXiv abs page (HTML) for the bibliographic record**, but always capture the PDF for the actual content.
   <!-- /DOMAIN-SLOT -->

5. **Verify captures.** After capture, read a few lines of each written file to confirm it's real content (not a bot wall, login page, or empty extraction). If a capture is clearly broken, try the Playwright MCP tool directly to inspect the page and diagnose.

6. **Integrate via `/ingest`** — Invoke `/ingest raw/research/<topic-slug>` on the topic directory. `/ingest` reads the raw files, discusses takeaways, writes wiki pages with source-traceable claims, and updates tracking files.

7. **Report.** Separate three things:
   - **What the sources said** — faithful summary of each captured file, per file.
   - **What was changed in the wiki** — pages created or modified, cross-references added.
   - **Open questions for the user** — conflicts, gaps, or decisions that need a ruling.
