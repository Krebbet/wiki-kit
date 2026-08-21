# Research Agenda

The durable queue of research jobs for this wiki. **This file is the resume point** — if a session dies, is
rate-limited, or is cleared, the next session reads this table and picks up at the first row that is not
`done`. Statuses are committed after every job, so the queue never lies about what landed.

Each job runs as `/research` scoped to the topic, capturing into `raw/research/<slug>/`.

**Status values**
- `queued` — not started
- `capturing` — sources being captured into `raw/research/<slug>/`
- `captured` — sources on disk and audited, not yet ingested
- `ingesting` — subagent summaries dispatched or being aggregated
- `done` — wiki pages written, linked from `[[index]]`, tracking files updated
- `blocked` — see the Blocked log at the bottom; needs a decision or a retry

**Resume rule.** `captured` and `ingesting` are the dangerous states — captures live in `raw/research/`,
which is **gitignored**, so they do not survive a fresh clone. On resume, check whether
`raw/research/<slug>/` actually exists before trusting a `captured` status; if it does not, reset the row to
`queued` and re-capture. `.ingest/run.json` tracks per-source progress within a job and makes `ingesting`
resumable in place.

---

## Wave 1 — Foundations (run first; supplies the vocabulary every later job is phrased in)

| # | Slug | Topic | Status |
|---|---|---|---|
| 1 | `foundations-nie` | What institutions are and why they exist — North, Coase, Williamson, Ostrom; transaction costs, rules, credible commitment | done |

## Wave 2 — The user's six subjects

| # | Slug | Topic | Status |
|---|---|---|---|
| 2 | `institutional-evolution` | How institutions evolve over time — path dependence, institutional isomorphism, layering/drift/conversion, lifecycle models | done |
| 3 | `scale-effects` | Large vs small institutions — what changes with size: hierarchy layers, span of control, coordination cost, formalisation, diseconomies of scale | done |
| 4 | `incentives-and-institutional-form` | Incentives and how they form institutions — principal-agent, incomplete contracts, selection effects, multitask/measurement distortion, how incentive structure produces institutional shape | done |
| 5 | `risk-aversion-in-large-institutions` | Why large institutions become risk averse — asymmetric payoffs to individual decision-makers, blame allocation, veto points, defensive process, loss aversion in bureaucracies | done |
| 6 | `enabling-institutional-change` | Empowering change in institutions — what actually makes reform succeed: crisis windows, leadership autonomy, reorganisation evidence, skunkworks, Ostrom design principles | done |
| 7 | `institutional-stagnation` | Why institutions become stagnant — ossification, goal displacement, rent-seeking, Olson's distributional coalitions, vetocracy, sclerosis | done |

## Wave 3 — Seeding jobs to complete the frame

Chosen to close the structural gaps Waves 1–2 leave: the public/private comparison the framework depends on,
the two remaining legs of the power/institutions/economy triad, and the operationalisation without which no
proposed dimension can be measured.

| # | Slug | Topic | Status |
|---|---|---|---|
| 8 | `bureaucracy-and-public-choice` | Public institutions: Weberian bureaucracy vs public choice — Wilson, Niskanen, Tullock, Downs. Both camps captured in one job so the conflict is documented from the start | done |
| 9 | `theory-of-the-firm` | Private institutions: why firms exist and where their boundaries fall — Coase, Chandler, Williamson, agency theory. Job 9 minus job 8 is the public/private difference the project needs | done |
| 10 | `institutions-and-growth` | The economy leg — institutions and economic production: inclusive/extractive, state capacity, developmental state, and the reverse-causality critiques | done |
| 11 | `power-and-accountability` | The power leg — elite theory, veto players, selectorate theory, corporate governance and control, who an institution is *actually* accountable to | capturing |
| 12 | `measuring-institutions` | Operationalisation — V-Dem, WGI, QoG, state-capacity indices, and the critiques of institutional measurement. Without this, lint check 11 fails every framework page | done |

## Wave 4 — Follow-ups the findings demanded

Added 2026-08-20 after Waves 1-3 exposed specific gaps. These are not "more of the same": each one targets a
hole the completed jobs identified by name.

| # | Slug | Topic | Status |
|---|---|---|---|
| 13 | `organisational-ecology` | **The demography of organisations** — Stinchcombe's liability of newness, Hannan & Freeman's population ecology, Carroll on organisational mortality, imprinting of founding conditions, age-dependent failure rates. *Why:* five literatures (jobs 2, 3, 5, 6, 7) came back with no institution-level age evidence, but all five were institutional economics, political science or public administration. Organisational sociology is the field that actually treats **organisational age as an independent variable** and has survival data on real organisational populations. If the age evidence this project needs exists anywhere, it is here. This is the highest-priority job in the queue. **Delivered**: the wiki's first true-panel organisation-age mortality evidence (Yang & Aldrich), on entrepreneurial ventures rather than mature bureaucracies — Q7 moved to `partial (age)`, Q60 stays `open` on narrower grounds. Five pages, D124–D126. | done |
| 14 | `comparative-governing-philosophies` | **How governing philosophy shapes institutions** — Nordic models, the Chinese party-state and SOEs, Singapore, German ordoliberalism, Japanese/Korean developmental administration, the US administrative state. *Why:* the project brief asks for this explicitly and an earlier restructuring of this agenda dropped it. Also the only job that tests whether any registered axis is universal or an Anglosphere artefact. `[[reference-sources]]` lists Chinese, Nordic, Japanese/Korean, Latin American and African scholarship as standing coverage holes — this job should close them, preferring in-country scholarship and translated primary material over outsider interpretation. | queued |
| 15 | `institution-case-profiles` | **Paired case profiles: one public, one private, same axes** (FDA and Meta as the brief's own example). *Why:* the wiki has **zero** case-study pages, so lint check 13 is permanently `not yet applicable` by construction and the framework is entirely ungrounded. **Not a literature job** — it captures primary institutional documents (enabling statutes, org charts, budgets, annual reports, 10-Ks, inspector-general reports, post-mortems) and scores them against `[[dimensions-of-institutional-variation]]`. It is also the only thing that will reveal which of the register's promoted axes are actually usable, since not one has ever been run against a real institution. | queued |
| 16 | `informal-institutions` | **Norms, trust, culture and the informal half** — informal constraints, social norms, trust and its measurement, custom and convention as enforcement, why informal constraints change more slowly than formal rules. *Why:* North's formal/informal distinction is load-bearing in his own account and the wiki currently mentions it on four pages without ever having researched it. A general theory of institutions holding only the formal half is incomplete by construction. | queued |

## Wave 5 — user-directed

| # | Slug | Topic | Status |
|---|---|---|---|
| 17 | `schooling-norms-and-institutional-formation` | **How schooling and cultural norms form institutions.** Human capital as a *cause* of institutional quality rather than a consequence; education and state formation; civic education and norm transmission; cultural transmission of cooperation norms; the sequencing question — does schooling precede institutional change or follow it? *Why:* Glaeser et al. found that re-running AJR's own settler-mortality instrument tracks **human capital better than institutions**, and that on sequencing, schooling predicts institutional change rather than the reverse. If that holds, the causal arrow in the project's triad is partly reversed: institutions would be substantially downstream of education and norms rather than upstream of everything. Requested by the user 2026-08-20. See [[schooling-and-institutional-quality]]. | queued |

---

## Running conventions

- **One job at a time, ingested to completion before the next starts.** A backlog of un-ingested captures is
  how a wiki rots, and captures are gitignored so a backlog is also unbacked-up.
- **Ideological balance is a hard gate** (see `/research`). Every contested job must capture from at least two
  camps. A topic dir that leans one way is a research failure, not a finding.
- Dimension candidates surfaced during any ingest get appended to `[[open-questions]]`, not held in chat.
- If a job yields fewer than three usable sources, it was scoped wrong — re-scope rather than proceeding thin.
- Run `/lint` after every third completed job.

## Blocked log

Append a row whenever a job goes `blocked`, with enough detail that a later session can act without re-deriving
the problem.

| Date | Job | What blocked it | What would unblock it |
|---|---|---|---|
| 2026-08-19 | 3 `scale-effects` | Parkinson's original 1955 Economist essay: the only open copy found (`doc.cat-v.org`) is an **excerpt** — 561 words, cutting off exactly where the "statistical proofs, which will follow" begin, and containing none of the Admiralty/Colonial Office headcount series that are the essay's actual evidence. Verified against the raw HTML: the capture is faithful, the *page* is partial. Re-capture with `--js` returned the same. | Find a full text of the 1955 essay (or the 1957 book chapter) on another host, or treat Parkinson's own empirics as uncited. Partially mitigated: the arXiv paper `parkinson-law-quantified-empirical` is a modern quantitative test of the same claim and carries the empirical weight. Any wiki page citing the excerpt must not attribute the headcount evidence to it. |
| 2026-08-19 | 1 `foundations-nie` | Wallis, *Persistence and Change in Institutions* (`econweb.umd.edu`) fails capture with `SSL: CERTIFICATE_VERIFY_FAILED` — the host's cert chain is incomplete, on both `http://` and `https://`. Not a bot wall. | Find the paper on another host, or download it manually in a browser into `raw/research/foundations-nie/` and run `capture_pdf --src <local-path>`. Not blocking the job — five other sources captured cleanly. |

## Synthesis phase (not `/research` jobs)

These are `/query` and authoring passes over what Waves 1–3 build. They are the project deliverables and are
only as good as the evidence underneath, so they do not start until Wave 2 is `done` at minimum.

- **Framework draft** (outcome 2) — the primary dimensions of institutional variation, assembled from the
  dimension candidates flagged during ingest. Every dimension must be operationalisable (lint check 11).
- **Paired case profiles** (outcome 2) — one public and one private institution on the same axes (e.g. FDA vs
  Meta) as the framework's first real test. Tag sector / scale / age / country.
- **Lifecycle model** (outcome 4) — synthesise jobs 2, 3, 5, 7.
- **The triad model** (outcome 5) — institutions × power × economic production. Written after jobs 10 and 11,
  and explicitly willing to conclude the triad is the wrong decomposition.
- **Manifesto** (outcome 3) — the levers, scoped by scenario.
- **Book outline** (outcome 6) — last. The collapse-and-renewal thesis is on trial throughout.

## Source

- `docs/project-brief.md` — the user's statement of the six project outcomes.
- Wave 2 subjects specified directly by the user, 2026-08-19.

## Related

- [[open-questions]] — the questions these jobs are meant to close.
- [[capture-manifests]] — the exact verified URL list per job, so gitignored captures can be regenerated.
- [[reference-sources]] — the standing weekly radar, distinct from this one-off queue.
- [[index]] — the content catalog.
