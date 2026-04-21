# Master Notes

Running log of what works and what doesn't — both for this specific wiki's operation and for the collaboration generally. Append-only scratchpad for observations that might deserve to become CLAUDE.md guidance, command updates, or kit-level improvements.

During normal operation, Claude appends observations here with `Status: open`. At `/harvest` time (or whenever you review), entries are triaged: some become kit-level code or doc changes promoted to main via `/harvest`; some become this wiki's project CLAUDE.md updates; some are rejected; some stay open for more signal.

## Format

Append entries using this structure:

```
### YYYY-MM-DD — short title
**Scope:** project | interaction | kit | both
**Observation:** what was noticed
**Implication:** what this suggests for CLAUDE.md, a command, a tool, or process
**Status:** open | proposed | applied | rejected
```

**Scope guide:**
- `project` — specific to this wiki (lands in this wiki's `wiki/CLAUDE.md` or DOMAIN-SLOT content).
- `kit` — generic to wiki-kit itself (gets promoted to main via `/harvest`; every other wiki benefits).
- `interaction` — about how the user and assistant work together (may become memory or user-level CLAUDE.md).
- `both` — overlaps more than one scope.

## Notes

<!-- Entries appended during operation go below. -->

### 2026-04-21 — audit_captures crashes on inline data URIs
**Scope:** kit
**Observation:** During `/research` on `formulation-landscape`, `tools.audit_captures` crashed with `OSError: [Errno 36] File name too long` because it tried to `Path.exists()` on a `data:image/svg+xml;base64,...` URI that appeared as an image reference in a captured Nature page (the PMC capture also contained similar data URIs). Any capture of modern publisher sites will trip this.
**Implication:** `audit_captures.py` should skip refs whose src starts with `data:`, `javascript:`, or any non-relative-file scheme — only check refs that would resolve to local files. A one-line guard at the top of the ref-walk loop fixes it.
**Status:** open

### 2026-04-21 — capture_url download_asset fails on protocol-relative URLs
**Scope:** kit
**Observation:** Capturing both `nature.com` articles (s41538-025-00395-x and s41538-025-00441-8) produced "Request URL is missing an 'http://' or 'https://' protocol" for every figure, because Nature's figure URLs are protocol-relative (`//media.springernature.com/...`). The markdown body captured fine, but figures were all lost. Same class of bug likely for any publisher that uses protocol-relative asset URLs.
**Implication:** `_download_asset` (or its equivalent) in `capture_url.py` should normalize URLs before fetching: if the URL starts with `//`, prefix with `https:`; if it's a bare relative path, resolve against the page's base URL.
**Status:** open

### 2026-04-21 — capture_url download_asset fails on plain-relative image paths (arXiv HTML)
**Scope:** kit
**Observation:** Capturing `arxiv.org/html/2509.21556v1` produced asset failures like `download_asset failed for fig01.png: Request URL is missing an 'http://' or 'https://' protocol` for nine figures. arXiv's HTML renders figures with simple relative paths (`fig01.png`), which the downloader isn't resolving against the page's base URL. Same underlying cause as the protocol-relative bug (no URL normalization before fetch).
**Implication:** Fix together with the protocol-relative case — use `urllib.parse.urljoin(base_url, asset_url)` before fetching.
**Status:** open

### 2026-04-21 — large-corpus ingest should use subagent extraction instead of reading everything into main context
**Scope:** kit
**Observation:** `ingest.md` step 1 says "Read the source — If it's a directory, read all .md files within it." On the first formulation-landscape ingest (6 sources totalling ~860KB of full text), reading all files into main context would have burned a large fraction of the context window on raw source material that was never quoted directly. Instead I dispatched 6 parallel Explore agents with the domain-slot takeaway prompts baked into the agent-prompt template, and synthesised their structured reports — much cheaper and cleaner, with each source's extraction bounded by a word budget.
**Implication:** `ingest.md` should recommend parallel subagent extraction when the source corpus is large (rule of thumb: >~200KB total or >3 files). The subagent prompt template can pull directly from the `takeaway-prompts` DOMAIN-SLOT, giving each agent the same domain-specific extraction structure the ingest flow already uses. The main-context reading in step 1 should be reserved for small corpora or when direct quotation is central.
**Status:** open

### 2026-04-21 — MDPI and ScienceDirect bot-detect the capture scripts
**Scope:** kit
**Observation:** MDPI's Akamai/edgesuite edge returns "Access Denied" for both the HTML article URL and the direct `/pdf/` URL (403 Forbidden) from the capture tools. ScienceDirect's Cloudflare layer blocked the headless Chrome capture attempt with an IP-block error page. Both render as technically-successful captures (tiny markdown files with error content), so only size-based inspection catches the problem. Routine for a researcher's workflow, not an exceptional case.
**Implication:** (a) Capture scripts should surface a hard failure (non-zero exit) when the captured body is clearly a known bot-wall signature (Access Denied, Cloudflare error 1000s, etc.) rather than silently writing a tiny markdown file. (b) `/research` should flag any capture smaller than ~2KB for manual inspection before ingest. (c) Worth documenting in `research.md` that MDPI and ScienceDirect often require a manual PDF drop from a browser.
**Status:** open

