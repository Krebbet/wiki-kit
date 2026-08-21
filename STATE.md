# STATE — resume point after the 2026-08-21 reboot

Written immediately before a planned machine restart. Delete this file once the outstanding work below is done.

## Where things stand

**11 of 17 research jobs are complete** (pages written, committed, pushed): 1 foundations-nie, 2 institutional-evolution,
3 scale-effects, 4 incentives-and-institutional-form, 5 risk-aversion-in-large-institutions,
6 enabling-institutional-change, 7 institutional-stagnation, 8 bureaucracy-and-public-choice, 9 theory-of-the-firm,
10 institutions-and-growth, plus the user-requested `schooling-and-institutional-quality` page.

**All captures are finished for every job.** Nothing is mid-download. `raw/research/` holds sources for all 17 topics.
Note `raw/research/` is **gitignored** — it does NOT survive a fresh clone. It survives a reboot fine.
If it is ever lost, regenerate from `wiki/capture-manifests.md`, which lists every verified URL per job.

## Outstanding work, in priority order

### 1. Finish job 12 `measuring-institutions` bookkeeping (INTERRUPTED MID-WRITE)

Its five pages are written and committed and its index rows were added by hand. Still missing:

- **D120** `candidate` — measurement-construction audit: run Munck & Verkuilen's three-stage checklist against an
  institution's own internal KPI/scorecard documentation (not against a country index). Score for
  maximalist/minimalist definition, redundancy/conflation, justified scale level, published coding rules and
  reliability tests, and whether the aggregation rule reflects a stated theory of how components combine.
- **D121** `candidate` — external-threshold gaming exposure: is the institution's funding, eligibility or
  classification gated by a single external published index? Check funding documents for a bound threshold, then
  test its own reported metrics for a discontinuity at that threshold.
- **`rejected` rows, with reasons** — any V-Dem/WGI/QoG country score as an institution-level axis (national
  aggregates; V-Dem explicitly averages away sub-national heterogeneity before scoring), and the WWBI
  sector/occupation aggregate (stops at national functional category; no agency identifier in the schema).
  Recording these as rejected is the point: it documents that the field's flagship instruments are inadmissible
  here, and why.
- **Q90 update** — the mechanism finding. V-Dem instructs coders to average away sub-national and branch
  heterogeneity; job 9 found 77% of management-quality variation is *within* country-industry. Together: the
  dominant instruments are structurally built to discard the variation that carries most of the signal.
- **Q120+** — new questions from this batch.
- **`wiki/revisions.md`** rows for the five new pages.

Source material: `raw/research/measuring-institutions/.ingest/*.summary.md` (all 7 present and complete).

### 2. Six jobs captured but NOT yet ingested

Each needs an ingest orchestrator (one subagent per source, summaries into `<topic>/.ingest/`) then a page writer.

| Job | Slug | Sources on disk |
|---|---|---|
| 11 | `power-and-accountability` | 7 (+1 retry) — Mills's *Power Elite* unrecoverable, archive.org 500s |
| 13 | `organisational-ecology` | 5 (+1 retry) — **highest priority**; the field that actually measures organisational age |
| 14 | `comparative-governing-philosophies` | 7 (+1 retry) |
| 15 | `institution-case-profiles` | 8 — FDA and Meta primary documents; the wiki's first case-study pages |
| 16 | `informal-institutions` | 9 |
| 17 | `schooling-norms-and-institutional-formation` | 8 |

**The three retried captures all FAILED again** and did not land — confirmed before the reboot. Counts are
ecology 5, power 7, comparative 7.

- Le Mens (ecology, disconfirming/obsolescence source) — 503 from the Wayback host
- Enns (power, one of the two Gilens-Page rebuttals) — 403
- Eucken (comparative, the German ordoliberal source) — the misleading weasyprint error, i.e. the server
  returned a non-PDF

**Note the discrepancy worth chasing:** a manual `curl -sIL` on all three returned `200` with
`content-type: application/pdf`, yet `capture_pdf` failed on each. The capture tool uses httpx with its own
User-Agent and does not follow the same redirect chain as curl, so these hosts are serving it differently.
That is a real capture-tool gap, not three dead links — worth diagnosing before assuming the sources are lost.
Losing Enns costs job 11 one of its two required rebuttals, so the ideological-balance gate on that job is not
currently met.

### 3. Known constraints

- **WebSearch budget was exhausted** (200/200) in the pre-reboot session. All six pending jobs already have their
  sources captured, so they are unaffected — but **no new research job can start** until the budget resets.
- **Do not use the GPU for captures.** Everything has run with `CUDA_VISIBLE_DEVICES=""`; marker on CPU costs
  ~30-60s per digital-native paper. The workstation GPU has known VRAM degradation.
- **marker hangs on scanned PDFs.** It ran 2h08m on a 25-page scan without completing. If a capture exceeds ~15
  minutes, treat it as hung, not slow. See `master_notes.md`.
- **`tools/audit_captures` is currently a no-op** for its two most valuable checks — it gates them behind a `pdfs/`
  directory that `capture_pdf` never creates, so it reports "0 issues" having only run the image-reference checks.
  Verify captures by word count instead. See `master_notes.md`.

### 4. Manual acquisition list

Canonical sources with no open copy, several load-bearing. If you can supply a PDF, drop it in
`raw/research/<job>/` and run `poetry run python -m tools.capture_pdf --src <path> --out raw/research/<job> --slug <slug>`.

- **Thornhill & Amit**, *Learning About Failure: Bankruptcy, Firm Age, and the Resource-Based View* (Org. Science 2003)
  — the age-stratified failure dataset; the most concrete empirical age evidence the project found, and lost.
- **Weber**, "Bureaucracy" (*Economy and Society* ch. VIII) — job 8 has no primary Weber text.
- **Wilson**, *Bureaucracy* (1989) — register axis D50 is held second-hand via Dixit and cannot be checked.
- **Fama & Jensen (1983)** — the canonical decision-rights decomposition; four sources name decision rights and none
  supplies it.
- **North & Weingast (1989)** — `credible-commitment`'s canonical evidence is currently second-hand.
- Olson, *Rise and Decline of Nations*; Carpenter, *Forging of Bureaucratic Autonomy*; Mills, *The Power Elite*.

## Full state of the wiki

See `wiki/research-agenda.md` for the job queue and its blocked log, `wiki/capture-manifests.md` for every verified
source URL and every known-bad one, `wiki/lint-reports/2026-08-19.md` for the last health check, and
`master_notes.md` for kit-level bugs found (several are worth harvesting to main).
