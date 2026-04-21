# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-21] bootstrap | collective consumer counter-power

Initial bootstrap. Schema and commands tailored for collective consumer counter-power. Ready to receive first source.

## [2026-04-21] research+ingest | dynamic-pricing-landscape

First content run. Topic: industries using dynamic / algorithmic / surveillance pricing and how they deploy it.

**Sources captured (8):** FTC Issue Spotlight (surveillance pricing 6(b) study); FTC Research Summaries (6(b) redacted); DOJ RealPage press release; ProPublica on DOJ/RealPage settlement; NBER working paper on algorithmic pricing; HBS working paper 22-050 on algorithmic pricing consumer harm; arXiv 2504.16592 on algorithmic collusion; Wikipedia dynamic-pricing article. All under `raw/research/dynamic-pricing-landscape/`.

**Capture audit:** clean except 2 broken image refs in `08-arxiv-algorithmic-collusion.md` (pymupdf fallback — no figure extraction; text intact). No mitigation needed; figures are not load-bearing for the claims cited.

**Wiki pages created (6):**
- `dynamic-pricing-overview.md` — hub / term disambiguation.
- `industries/rental-housing-algorithmic-pricing.md` — RealPage case study.
- `industries/surveillance-pricing-retail.md` — FTC 6(b) findings.
- `industries/consumer-facing-dynamic-pricing.md` — classic consumer industries.
- `mechanisms/algorithmic-collusion.md` — theory and evidence.
- `counter-power/regulatory-responses.md` — consolidated counter-power landscape with emphasised design-input candidates.

**Design-input section** added to each page (editorial, clearly labelled) per user request — emphasised on `regulatory-responses.md` given the user's focus on tools to build.

**Open questions surfaced during research** (none required user ruling at ingest time — all sources complementary rather than contradictory):
- HBS "non-collusive asymmetric-frequency harm" is a *stronger* theoretical claim than the DOJ's explicit-coordination framing. Both are documented on the relevant pages without implying one supersedes the other.

**Kit-level findings logged to `master_notes.md`:**
1. `capture_pdf.py` missing User-Agent header (403 on ftc.gov via Akamai).
2. `capture_url.py` mishandles protocol-relative URLs (Wikipedia thumbnails fail).
3. `capture_pdf.py --engine marker` has no graceful fallback on CUDA OOM.

All three tagged `Scope: kit`, `Status: open` — available to `/harvest`.
