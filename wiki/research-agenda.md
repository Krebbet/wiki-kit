# Research Agenda

The prioritised queue of research jobs for this wiki. Ordered so that early jobs build the vocabulary later
jobs depend on: the framework cannot be assembled before the canon is in, and the manifesto cannot be written
before the framework survives contact with real cases.

Each job below is run as `/research <topic>` from the repo root. Run them **one at a time** — each ends in an
`/ingest` pass with a human review gate, and a queued backlog of un-ingested captures is how a wiki rots.
After each job, run `/lint` if three or more pages landed.

Status values: `queued` → `researching` → `ingested` → `done` (page(s) written and linked from `[[index]]`).

---

## Phase 1 — The canon and the vocabulary (jobs 1–4)

Goal: know what has already been thought, and acquire the field's terms of art before inventing any.

| # | Job | `/research` topic | Status | Why it's first |
|---|---|---|---|---|
| 1 | Foundational theory of institutions | `new institutional economics: North, Williamson, Ostrom, Coase — what institutions are and why they exist` | queued | Establishes the base definition — rules, transaction costs, credible commitment — that everything else is phrased against. |
| 2 | Bureaucracy and public-sector institutions | `Weberian bureaucracy vs public choice theory: Wilson, Niskanen, Tullock, Downs on agency behaviour` | queued | The two rival accounts of *public* institutional behaviour. Capture both camps in one job so the conflict is documented from day one. |
| 3 | The firm as an institution | `theory of the firm and corporate organisation: Coase, Chandler, Williamson, agency theory, why firms have boundaries` | queued | The private-sector counterpart to job 2. Job 3 minus job 2 is the public/private difference the project needs. |
| 4 | Institutions, growth and state capacity | `institutions and economic growth: Acemoglu & Robinson inclusive/extractive, state capacity, developmental state critiques` | queued | Connects institutions to economic production, and surfaces the field's biggest live controversy. |

## Phase 2 — Lifecycle, scale and decay (jobs 5–7)

Goal: outcome 4 — how institutions change as they grow and age. The user flagged this as a priority theme.

| # | Job | `/research` topic | Status | Why |
|---|---|---|---|---|
| 5 | Growth, scale and hierarchy | `how organisations change with size: span of control, hierarchy layers, Parkinson's law, coordination cost, diseconomies of scale` | queued | The scale half of the lifecycle question, drawing on both org theory and public administration. |
| 6 | Ossification, capture and decay | `institutional decay: regulatory capture, goal displacement, rent-seeking, Olson's Rise and Decline of Nations, vetocracy, Fukuyama on political decay` | queued | The age half. Also the evidential test of the book's collapse premise — run it before writing anything that assumes decay. |
| 7 | Adaptation, reform and renewal | `institutional reform and adaptability: what makes organisations able to change, Ostrom's design principles, polycentric governance, agency reform track records` | queued | The counter-case to job 6, and the raw material for the manifesto. Deliberately paired so decay is not studied without renewal. |

## Phase 3 — Comparative and cross-cutting (jobs 8–10)

Goal: outcome 1's comparative half, and the scope conditions that keep the framework honest.

| # | Job | `/research` topic | Status | Why |
|---|---|---|---|---|
| 8 | Governing philosophies compared | `comparative institutional design: Nordic model, Chinese party-state and SOEs, Singapore, German ordoliberalism, US administrative state` | queued | Tests whether any proposed dimension is universal or an Anglosphere artefact. Prefer in-country scholarship over outsider interpretation. |
| 9 | Power, elites and decision rights | `power distribution and institutions: elite theory, veto players, principal-agent accountability, selectorate theory, corporate governance and control` | queued | The power leg of the triad — how the surrounding power structure sets an institution's incentives, and how power is distributed inside it. |
| 10 | Measuring institutions | `measuring institutional quality: V-Dem, Worldwide Governance Indicators, state capacity indices, and the critiques of institutional measurement` | queued | Operationalisation. Without this the framework's dimensions stay unmeasurable, and lint check 11 will fail every page. |

## Phase 4 — Synthesis (not `/research` jobs)

These are `/query` and authoring passes over what Phases 1–3 built. Do not start them early; they are the
deliverables, and they are only as good as the evidence underneath.

- **Framework draft** (outcome 2) — propose the primary dimensions of institutional variation from the
  dimension candidates flagged during ingest. Every dimension must be operationalisable (lint check 11).
- **Paired case profiles** (outcome 2) — profile one public and one private institution on the same axes,
  e.g. FDA vs Meta, as the framework's first real test. Tag sector / scale / age / country.
- **Lifecycle model** (outcome 4) — synthesise jobs 5–7 into a staged account of institutional evolution.
- **The triad model** (outcome 5) — institutions × power × economic production. Written *after* jobs 4 and 9,
  and explicitly willing to conclude the triad is the wrong decomposition.
- **Manifesto** (outcome 3) — the levers, scoped by scenario.
- **Book outline** (outcome 6) — last. The collapse-and-renewal thesis is on trial throughout; the outline is
  written against whatever the evidence actually supports.

---

## Running conventions

- One job at a time, ingested to completion before the next starts.
- Every job must end with sources from at least two ideological camps where the question is contested
  (see the authoritative-sources section of `/research`).
- Dimension candidates surfaced during any ingest get appended to `[[open-questions]]`, not held in chat.
- If a job produces fewer than three usable sources, it was scoped wrong — re-scope rather than proceeding thin.

## Source

- `boot_strap_instructions.md` (consumed at bootstrap, 2026-08-19) — the user's statement of the six project
  outcomes and the power/institutions/economy thesis.

## Related

- [[open-questions]] — the questions these jobs are meant to answer.
- [[reference-sources]] — the standing radar the weekly brief sweeps, distinct from this one-off agenda.
- [[index]] — the content catalog.
