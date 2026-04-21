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

### 2026-04-21 — capture_pdf missing User-Agent header; 403 on ftc.gov
**Scope:** kit
**Observation:** Direct fetch of FTC PDFs (`sp6b-issue-spotlight.pdf`, `p246202_surveillancepricing6bstudy_researchsummaries_redacted.pdf`) via `capture_pdf.py --src <URL>` returned 403 Forbidden. Reproduced with `curl -sI <URL>` — default UA yields 403 via Akamai; `curl -H "User-Agent: Mozilla/5.0..."` yields 200. `capture_pdf.py` does not set a User-Agent. Workaround: curl the PDFs locally with a browser UA, then pass local paths to `capture_pdf --src`.
**Implication:** Add a sane browser User-Agent to the httpx client in `capture_pdf.py`'s download path (same convention `capture_url.py` presumably already uses). Government and enterprise sources behind Akamai / Cloudflare are a load-bearing category for many wikis; this will bite repeatedly otherwise.
**Status:** open

### 2026-04-21 — capture_url mishandles protocol-relative URLs on Wikipedia
**Scope:** kit
**Observation:** Capturing `en.wikipedia.org/wiki/Dynamic_pricing` produced repeated `download_asset failed` warnings: first for `//upload.wikimedia.org/...` ("Request URL is missing an 'http://' or 'https://' protocol"), then for the fallback `http://upload.wikimedia.org/...` (403 Forbidden — Wikimedia requires https on some upload endpoints). Main article markdown captured fine; only thumbnail images are missing. Two compounding bugs: (1) protocol-relative URLs not resolved via `urljoin` against page URL; (2) fallback retry appears to prepend `http://` rather than matching the source page's scheme.
**Implication:** In `capture_url.py` asset resolver, use `urllib.parse.urljoin(page_url, asset_href)` so protocol-relative and root-relative URLs both resolve correctly. Default scheme should be the source page's scheme (`https://`), not `http://`.
**Status:** open

### 2026-04-21 — capture_pdf marker engine has no graceful fallback on CUDA OOM
**Scope:** kit
**Observation:** On a host where another process held ~21 GB of the 23.5 GB GPU, `capture_pdf --engine marker` for the HBS working paper failed with `CUDA out of memory. Tried to allocate 20.00 MiB...` and exited with a stacktrace. No automatic fallback. Workaround: re-ran with `--engine pymupdf` — cost was 2 broken image refs in the arXiv capture (figures that marker would have extracted, pymupdf did not).
**Implication:** Either (a) catch `torch.cuda.OutOfMemoryError` and retry on CPU with a clear single-line warning, (b) catch and emit a one-line error pointing to `--engine pymupdf` instead of a stacktrace, or (c) add an explicit `--device cpu` flag for users on contended GPU hosts. Option (b) is the cheapest useful fix.
**Status:** open
