# Reference Sources

The standing radar the weekly brief sweeps. Distinct from citations: a page's `## Source` section records what
a claim came *from*; this file records where new material is *looked for*.

Every row is a seed until the first weekly sweep confirms it produces signal. Seeds ship as `probation`;
promote to `active` once a sweep has pulled something usable, retire after three consecutive dry sweeps.

## Scope

Institutions as a general subject: institutional economics and political economy, organisational theory,
public administration and bureaucratic behaviour, state capacity, corporate governance and the theory of the
firm, commons and polycentric governance, comparative institutional design, and the interaction of
institutions with power distribution and economic production.

**In scope:** new empirical work on institutional performance, decay or reform; theoretical contributions to
institutional design; substantial institutional histories and post-mortems; primary documents from a major
institutional reform or restructuring; methodological work on measuring institutions; serious comparative
work on non-Anglosphere systems.

**Out of scope:** partisan commentary on a specific government's competence; company news without an
institutional-design angle; management-consulting content; anything whose only claim is that things are
getting worse.

## Selection priority

This is a slow-moving field. "Trending" here does not mean high-velocity news — it means *newly available and
substantive*. Rank candidates by, in order:

1. **Evidential weight** — a new natural experiment or dataset beats a new argument.
2. **Framework relevance** — does it name or test a dimension of institutional variation the wiki is trying to
   pin down? Anything bearing on an `open` question in [[open-questions]] outranks general interest.
3. **Camp balance** — if the last few sweeps have all come from one intellectual camp, a strong source from a
   rival camp is worth more than a marginally better source from the same one.
4. **Non-Anglosphere coverage** — systematically underweighted in English-language feeds; correct for it here.
5. **Recency** — last, deliberately. A 1996 paper the wiki has never seen beats a mediocre paper from Tuesday.

## Local conventions

- **Empty runs are expected and correct.** Nothing significant happens in institutional theory most weeks.
  Fire the empty-run policy (step 9) rather than padding the brief with weak material. A brief with two strong
  items is better than one with five.
- **Books are in play.** Unlike a fast-moving tech wiki, a major new book in this field is a legitimate weekly
  find. Capture a substantial review or an author lecture if the text is unobtainable, and label it
  second-hand.
- **Working papers count**, but flag them as un-refereed on the resulting page.
- **Cap non-academic sources at two per sweep.** The blogs below are for finding what to read, not for being
  read into the wiki.
- **Never let a sweep capture five sources from the same camp.** If that is what the week offers, capture
  fewer and note the imbalance in the brief.

---

## Working-paper and preprint feeds

| Source | Where | Added | Status |
|---|---|---|---|
| NBER new working papers (Political Economy, Development, Productivity/Innovation, Corporate Finance programs) | nber.org/papers | 2026-08-19 | active (2026-08-25) |
| SSRN — Political Economy & Public Choice, Corporate Governance networks | ssrn.com | 2026-08-19 | probation |
| arXiv econ.GN (General Economics) | arxiv.org/list/econ.GN | 2026-08-19 | active (2026-08-25) |

**Capture note (2026-08-25):** `nber.org/papers/<id>` is a landing page that `tools.capture_pdf` cannot
distinguish from the actual PDF — it silently captures NBER's site-navigation shell instead of the paper.
Use the direct file path instead: `nber.org/system/files/working_papers/w<id>/w<id>.pdf`.

**Capture note (2026-09-15):** a *different* failure mode from the landing-page trap above — NBER w35756
403'd on **both** the landing page and the direct PDF path, even with a browser user-agent. This looks like a
genuine paywall (some NBER papers require institutional access or purchase in their first weeks), not a
tooling gap. Distinguish the two: 403-on-both = paywalled, skip; 200-on-landing/thin-on-PDF = landing-page
trap, use direct PDF path.

**Capture note (2026-09-22):** a *third* pattern, wider than either above — **every paper checked from this
week's release batch** (w35758, w35768, w35778, w35780 — four different papers, two fetch methods: the
capture tool and a raw `curl` with a browser user-agent) 403'd on both the landing page and the direct PDF
path. A single paywalled paper (like w35756) is expected; four different papers all blocked the same way in
the same week looks like a batch-wide access embargo rather than four independent paywalls, though this
wiki has no way to confirm the mechanism from the outside. **Before dropping a blocked NBER paper, check for
an open-access author mirror** — w35780 (Bacher, Fagereng, Ring & Wold) had one on a co-author's GitHub Pages
site and was captured via that route. Re-test next sweep whether the block is batch-specific (this week's
releases only) or has become the new baseline for all NBER papers.

## Journals

| Source | Focus | Added | Status |
|---|---|---|---|
| Journal of Economic Perspectives | Accessible surveys; frequent institutional-economics symposia | 2026-08-19 | probation |
| Journal of Institutional Economics | Core venue for the field | 2026-08-19 | active (2026-09-08) — open access since 2025, no Cloudflare block; two captures this sweep |
| Governance | Public administration and institutional reform | 2026-08-19 | probation — capture-blocked (2026-08-25) |
| American Political Science Review / American Journal of Political Science | Power, veto players, accountability | 2026-08-19 | probation — capture-blocked (2026-08-25) |
| Administrative Science Quarterly / Organization Science | Organisational theory, scale and hierarchy effects | 2026-08-19 | probation — capture-blocked (2026-09-22) |
| Journal of Economic Literature | Survey articles — high value per capture for a wiki still building its canon | 2026-08-19 | probation |

**Capture note (2026-09-22):** `journals.sagepub.com` (Administrative Science Quarterly, and presumably other
SAGE-hosted journals) served a Cloudflare "Performing security verification" challenge page to both a direct
PDF request and a Playwright `--js` capture attempt, even though the target article's DOI metadata claimed CC
BY-NC open access. `capture_url` "succeeded" (exit 0) but the captured file was the challenge page, not the
article — same failure class as the CEPR (2026-09-15) and NBER (2026-08-25) landing-page traps, new source.
Distinguish from Wiley's Cloudflare block (Governance, APSR/AJPS, OECD Public Governance) only in that SAGE's
challenge page is dynamic (a Ray ID, a "waiting for X to respond" message) rather than a static block — a
manual browser session with a persistent cookie jar may clear it where Wiley's does not; untested.

## Data, indices and multilateral output

| Source | What | Added | Status |
|---|---|---|---|
| V-Dem | Democracy and governance indicators; annual report | 2026-08-19 | probation |
| World Bank Worldwide Governance Indicators | Governance quality series | 2026-08-19 | probation |
| Quality of Government Institute (Gothenburg) | QoG datasets and working papers | 2026-08-19 | probation |
| OECD Public Governance | Comparative public-sector performance | 2026-08-19 | probation — capture-blocked (2026-08-25) |
| IMF / World Bank flagship reports | Institutions-and-growth chapters | 2026-08-19 | probation |
| National audit bodies (GAO, UK NAO, Canada OAG) | Primary evidence on institutional performance | 2026-08-19 | UK NAO: active (2026-09-08); GAO capture-blocked (2026-08-25, confirmed 2026-09-08); Canada OAG untested |

**Capture note (2026-08-25):** `oecd.org`/`oecd-ilibrary.org` and `gao.gov` both returned hard 403s to every
URL pattern tried (landing page, docserver guesses, browser User-Agent) — no Cloudflare challenge page, just
a block. Both surfaced a genuinely strong candidate this sweep (an OECD public-sector-innovation paper, a GAO
Army-modernization audit) that had to be watchlisted instead of captured. Worth a manual browser pull next
time either source produces a must-have candidate.

**Capture note (2026-09-08):** OECD and GAO both hard-403'd again this sweep (see `watchlist.md` Week of
2026-09-08 for the specific candidates blocked) — confirmed persistent, not a one-off. `nao.org.uk` captured
cleanly, but the same landing-page trap NBER has (2026-08-25 note) applies here too: `nao.org.uk/reports/<
slug>/` is a thin summary page, not the report body — use the direct PDF path
(`nao.org.uk/wp-content/uploads/<year>/<month>/<Report-Name>.pdf`) instead.

## Blogs, essays and commentary (discovery only — cap 2 captures/sweep)

| Source | Angle | Added | Status |
|---|---|---|---|
| VoxEU / CEPR columns | Economist-authored summaries of new institutional research | 2026-08-19 | probation — capture-blocked (2026-09-08): cepr.org Cloudflare bot-check, `--js` retry also blocked; capture-blocked (2026-09-15): a direct `cepr.org/publications/<id>` discussion-paper capture returns exit 0 but is a landing-page trap (site chrome repeating the abstract, not the paper — see `master_notes.md` 2026-09-15). Prefer a syndicated discovery mirror (e.g. Marginal Revolution's post about the paper) over the CEPR URL directly, same workaround as Mercatus below — but note the mirror alone is usually abstract-only, too thin for a full page. |
| Broadstreet | Historical political economy, explicitly institutions-focused | 2026-08-19 | probation — dry sweep (2026-09-08), no posts in window |
| Marginal Revolution | Discovery feed for institutional-economics papers | 2026-08-19 | active (2026-09-08) — not Cloudflare-gated; one capture this sweep |
| Works in Progress | State capacity, regulatory design, why institutions fail to build | 2026-08-19 | active (2026-09-08) — strong candidate surfaced, watchlisted |
| Statecraft | Interviews on how government institutions actually operate | 2026-08-19 | probation |
| Institute for Government (UK) | Primary-document-grounded analysis of an administrative state | 2026-08-19 | probation |
| Niskanen Center | State-capacity/vetocracy camp — deliberately included for balance against public-choice sources | 2026-08-19 | active (2026-08-25) |
| Mercatus Center | Public-choice camp — deliberately included for balance against state-capacity sources | 2026-08-19 | active (2026-08-25) — mercatus.org itself is Cloudflare-gated; captured via its Substack syndication mirror instead |

## Lectures, talks and long-form interviews

| Source | What | Added | Status |
|---|---|---|---|
| YouTube — author lectures and book talks by institutional economists and political scientists | `fetch_transcript` | 2026-08-19 | probation |
| Ostrom Workshop (Indiana) seminar recordings | Commons and polycentric governance | 2026-08-19 | probation |

## Deliberate coverage gaps to close

These are known holes in the radar above, not oversights. Closing them is a standing task for the sweep's
survey subagent.

- **Chinese-language scholarship** on the party-state and SOE governance. English-language work *about* it
  found this sweep (2026-08-25): a Shanghai co-production study (Governance, capture-blocked) and a Chinese
  SOE/CCP-statecraft reassessment (Asian Politics & Policy, watchlisted, untested) — still not primary
  Chinese-language sources.
- **Nordic** in-country public-administration research (Nordic sources in English skew to outsider summaries).
  A candidate found this sweep (2026-08-25): *Scandinavian Journal of Public Administration* Vol. 29 No. 4,
  published via a Swedish open-access platform (KB) — watchlisted, untested, but the first candidate from an
  actual Nordic-hosted venue rather than an outsider summary. **Partially closed 2026-09-22**:
  [[capital-requirements-and-entrepreneurial-entry]] is a natural experiment run directly on Norwegian
  administrative registers (business, tax, shareholder, employment and education records) — genuine
  Nordic-institution primary data, though the authors themselves are not Nordic-affiliated and the venue is
  NBER, not a Nordic-hosted journal, so this is a partial rather than full closure of the gap.
- **Japanese/Korean** developmental-state scholarship. A Korea industrial-policy candidate found this sweep
  (2026-08-25), watchlisted, untested (ScienceDirect, likely paywalled).
- **Latin American and African** institutional research, currently absent entirely until this sweep
  (2026-08-25) closed it partially: [[colonial-rule-and-trust-in-traditional-leaders]] (Africa, captured) and
  a Venezuela participatory-institutions paper (Latin America, capture-blocked, watchlisted) plus a Ghana
  policy-capacity paper (Africa, watchlisted, untested).

## Source

- Seeded at bootstrap, 2026-08-19, from `boot_strap_instructions.md`.
- First sweep, 2026-08-25: arXiv econ.GN, NBER, Niskanen Center and Mercatus Center confirmed productive and
  promoted to `active`. AJPS, Governance, OECD Public Governance and GAO all surfaced strong candidates but
  are currently uncapturable by this wiki's tooling (Cloudflare bot-check or hard 403) — see the per-table
  capture notes above and `master_notes.md` (2026-08-25, kit-level).
- Second sweep, 2026-09-08: Journal of Institutional Economics, Marginal Revolution, Works in Progress and UK
  NAO confirmed productive and promoted to `active`. VoxEU/CEPR confirmed Cloudflare-blocked (first live test
  of this source). OECD and GAO blocks confirmed persistent on a second sweep. SSRN, Canada OAG, Broadstreet,
  Statecraft, Niskanen and Institute for Government all dry this cycle — none yet at the three-consecutive-
  dry-sweep retirement threshold.
- Third sweep, 2026-09-15: genuinely thin week (3 in-scope candidates total, vs. the usual double digits) —
  consistent with this field's expected pace, not a sweep failure. NBER and Marginal Revolution both surfaced
  a candidate each but both hit new capture-blocked patterns (see capture notes above and `master_notes.md`);
  only 1 candidate (an Acemoglu book-talk interview) made it through to the wiki, and as a page extension
  rather than a new page given its second-hand/assertion tier. No source hit its three-consecutive-dry-sweep
  retirement threshold this cycle either.
- Fourth sweep, 2026-09-22: arXiv econ.GN productive again (2 captures, a single-author theory pair). NBER
  surfaced four strong candidates but the entire checked batch was capture-blocked (see capture note above) —
  one recovered via an open-access author mirror, the other three watchlisted. ASQ (a probation journal) hit a
  new SAGE-specific Cloudflare landing-page trap on its first live test this sweep. OECD surfaced two strong
  methodological/governance candidates, both still hard-403-blocked (persistent, fourth confirmation). No
  source hit its three-consecutive-dry-sweep retirement threshold. SSRN, Governance, APSR/AJPS, JEP, JEL,
  Broadstreet, Statecraft, Institute for Government, Niskanen and Mercatus were all dry or not surveyed with a
  strong-enough candidate this cycle.

## Related

- [[watchlist]] — overflow candidates from sweeps that were not captured.
- [[research-agenda]] — the one-off research queue, distinct from this standing radar.
- [[open-questions]] — priority 2 above ranks candidates against this register.
