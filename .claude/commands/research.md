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
**Authoritative sources for this wiki are**, in rough descending order of weight:

1. **Peer-reviewed and working-paper social science** — economics (institutional, public, development, organisational), political science, public administration, economic history, sociology of organisations. NBER / SSRN / journal PDFs. Prefer the paper over any write-up of the paper.
2. **Foundational books and monographs** in the field, and their primary chapters. Much of the canon here is book-shaped and older than the open-access era; a well-sourced detailed summary or a lecture by the author is an acceptable stand-in when the text itself is unobtainable, but **must be labelled as second-hand** on the resulting page.
3. **Primary institutional documents** — enabling statutes, charters, mandates, org charts, budgets, annual reports, 10-Ks, inspector-general and audit reports, post-mortems, internal design memos. These are the ground truth about how an institution is actually wired, as opposed to how it describes itself.
4. **Multilateral and government statistical/analytical output** — World Bank, OECD, IMF, national audit offices, GAO, V-Dem and comparable indices. Always capture the methodology alongside the number.
5. **First-hand practitioner accounts** — people who have actually run large public or private institutions, writing about mechanism rather than politics.

**Avoid, or capture only with an explicit flag:**
- Opinion journalism and op-eds that assert institutional decline without evidence. If captured, tag as *position, not evidence* on the resulting page.
- Advocacy think-tank output that presents a policy preference as a finding. Capture the underlying data if it has any; treat the conclusions as a position to be attributed, never as a source of fact.
- Wikipedia, content-mill explainers, and LLM-written summaries.
- Single-country generalisations presented as universal law — capture is fine, but the scope condition must survive into the wiki page.

**Ideological balance is a hard requirement.** This domain has organised camps (public-choice / market-liberal, Weberian / state-capacity, institutionalist / new-institutional-economics, developmental-state, commons/polycentric, Marxian and elite-theory). When researching a contested question, deliberately capture at least one strong source from each major camp before writing a page. A topic dir where every source leans the same way is a research failure, not a finding.
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
     Default engine is `marker` — always use it for papers (image extraction is load-bearing). If the GPU is contended, force CPU with `CUDA_VISIBLE_DEVICES="" poetry run …`. Only fall back to `--engine pymupdf` if marker fails on CPU too; the "simple PDFs" / "skip model download" carve-out has burned us repeatedly because pymupdf drops figure binaries.

   - **YouTube video:**
     ```bash
     poetry run python -m tools.fetch_transcript --url <URL> --out raw/research/<topic-slug> --slug <short-slug>
     ```

   Each tool prints the written file path on success and exits non-zero with a stderr message on failure.

   **Known bot-walled hosts.** Some publishers (MDPI, ScienceDirect, some IEEE journals) bot-detect the capture scripts. MDPI tends to return `Access Denied` via Akamai/edgesuite for both HTML and direct-PDF URLs; ScienceDirect tends to return a Cloudflare IP-block page. `capture_url` detects common block-page signatures and exits non-zero; `capture_pdf` already exits non-zero on HTTP errors. When a blocked source is needed, ask the user to download the PDF manually via a browser and drop it into `raw/research/<topic-slug>/`, then run `poetry run python -m tools.capture_pdf --src <local-path> --out raw/research/<topic-slug> --slug <short-slug>` to process it.

   <!-- DOMAIN-SLOT: source-type-notes -->
- **Papers** — prefer the open PDF (NBER working-paper version, SSRN, author's page, arXiv) over a paywalled journal landing page; `capture_pdf` with the default `marker` engine. If only an abstract page is reachable, that is *not* a capture — find the PDF or drop the source.
- **Books** — if a legitimate full-text PDF is available, `capture_pdf` it (these are long; expect a slow marker run and check the output length before trusting it). Otherwise capture a substantial, attributable secondary treatment — an extended review essay, a book symposium, an author lecture transcript — and mark the resulting wiki page's `## Source` section as **second-hand**.
- **Lectures / interviews / podcasts** — `fetch_transcript` for YouTube. Transcripts of talks by the primary researcher count as primary sources for that researcher's *position*, never as evidence for the underlying empirical claim.
- **Primary institutional documents** — usually PDFs (`capture_pdf`); statutes and filings are frequently HTML (`capture_url`). Preserve the original PDF; these are the documents where exact wording is load-bearing.
- **Datasets and indices** — capture the codebook / methodology document, not just the headline ranking. A governance index without its construction method is uninterpretable and must not be cited on a wiki page.
- **Historical case material** — long-form institutional histories are among the highest-value sources here (how an agency or firm actually evolved over decades). Prefer these over contemporary commentary when studying lifecycle and decay.
- **Geographic spread** — when a research topic is comparative, actively seek non-Anglosphere sources (Nordic, Chinese, Japanese/Korean, German, Singaporean, Latin American). English-language coverage of these systems skews heavily toward outsider interpretation; prefer translated primary material or in-country scholarship where reachable.
<!-- /DOMAIN-SLOT -->

5. **Verify captures.** After capture, read a few lines of each written file to confirm it's real content (not a bot wall, login page, or empty extraction). **Any captured markdown under ~2KB is almost certainly a failure** — bot-wall pages, empty extractions, or login prompts — even if the tool exited zero; read it end-to-end before trusting it. If a capture is clearly broken, try the Playwright MCP tool directly to inspect the page and diagnose.

   Then run the fidelity audit on the topic directory:

   ```bash
   poetry run python -m tools.audit_captures raw/research/<topic-slug>
   ```

   The audit checks that every image ref in each captured markdown resolves to a real file, that source PDFs are paired, and that no two markdowns reference the same image (cross-paper overwrite indicator). Re-capture any paper flagged with broken refs or thin extraction before proceeding to `/ingest` — silently-corrupted captures will produce wiki pages with broken figure links.

6. **Integrate via `/ingest`** — Slash commands cannot nest (see `bootstrap.md`), so follow `/ingest`'s process inline rather than literally invoking it. Before doing so, **announce the phase transition plainly to the user** so the boundary is visible:

   > — research captures done; transitioning to ingest —

   Then proceed with `/ingest` on `raw/research/<topic-slug>`: dispatch one subagent per captured source (so raw source bodies stay out of the main context), aggregate their structured summaries, and present a single consolidated review packet covering page plan, cross-references, conflicts, and low-value candidates. Wait for the user's rulings on the packet, then write wiki pages with source-traceable claims and update tracking files. When the ingest phase ends and you move to the final report (step 7), announce that boundary too:

   > — ingest complete; finalising research report —

   The announcements exist so the user understands which phase they are in; without them the user can read the "wait for user input" checkpoint as "the command stalled for no reason."

7. **Report.** Separate three things:
   - **What the sources said** — faithful summary of each captured file, per file.
   - **What was changed in the wiki** — pages created or modified, cross-references added.
   - **Open questions for the user** — conflicts, gaps, or decisions that need a ruling.

8. **Harvest checkpoint.** Did anything surface during this research run that would help *any* wiki, not just this one? Examples: a capture tool bug, a failure mode worth documenting in this file itself, a heuristic for judging source authority that generalises. If yes, append a brief entry to `master_notes.md` with `Scope: kit` and `Status: open`, and mention it inline. `/harvest` will pick it up.
