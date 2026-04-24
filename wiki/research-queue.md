# Research Queue

Prioritised backlog of `/research` topics for this wiki. Ordered by proximity to the user's querying lenses (market solutions, tech-enabled solutions, exit pathways, collective framings).

Each queued topic lists:
- **Lens** — which of the user's four lenses it serves most directly.
- **Mechanisms covered** — which of the 8 counter-power mechanisms from [[regulatory-responses]] would gain dedicated pages.
- **Likely pages** — a sketch of the wiki pages that would emerge from the ingest.
- **Rationale** — why this run is queued, and why at this priority.

Run order is a suggestion, not a contract — the user may reorder or skip.

---

## Priority 1

### ~~`/research platform cooperatives`~~ ✓ completed 2026-04-21
**Completed run — see `wiki/log.md` 2026-04-21 entry and [[platform-cooperatives]].**
Produced: `mechanisms/platform-cooperatives.md` + `organizations/{drivers-cooperative,mondragon,coopcycle}.md` + updates to `counter-power/regulatory-responses.md` and `dynamic-pricing-overview.md`.
Deferred from original plan: `mechanisms/exit-alternative.md` (defer to a dedicated run; sources frame "exit" through platform-coops specifically); Stocksy and other Shareable-list co-ops (thin sourcing — wait for dedicated sources).

### ~~`/research consumer data pooling and buyer-side tools`~~ ✓ completed 2026-04-21
**Completed run — see `wiki/log.md` 2026-04-21 entry and [[data-cooperatives]] + [[collective-bargaining-for-data]].**
Produced: `mechanisms/data-cooperatives.md` + `mechanisms/collective-bargaining-for-data.md` + `organizations/{midata,drivers-seat-cooperative}.md` + `tools/open-tenant-screening.md` + updates to `counter-power/regulatory-responses.md` (new section 9), `industries/rental-housing-algorithmic-pricing.md`, and `wiki/index.md`.
Deferred from original plan: `mechanisms/tech-workaround.md` (superseded by split coverage on data-cooperatives + collective-bargaining-for-data); `tools/consumer-data-pooling.md` (replaced by the anchor mechanism page + OpenTSS as a concrete proto-instance); Honey/Fakespot/Keepa tool pages (out of captured-source scope — defer to `/research price transparency tools` below); Salus Coop / JoinData standalone org pages (thin sourcing — defer).

## Priority 2

### `/research consumer class actions`
**Lens:** market solutions (primary); collective framings (secondary).
**Mechanisms covered:** class action.
**Likely pages:**
- `mechanisms/class-action.md` — definition, process, recent-era changes (arbitration-clause erosion, Supreme Court decisions).
- `cases/greystar-class-action.md` — already-referenced case, deserves its own page.
- Updates to `rental-housing-algorithmic-pricing.md` and `regulatory-responses.md` to cross-link.
**Rationale:** The RealPage-adjacent Greystar class action is already a recurring reference on existing pages but has no standalone treatment. Class actions are a mature, well-documented counter-power mechanism that academic and legal literature covers thoroughly.

### ~~`/research price transparency tools and personalised-pricing detectors`~~ ✓ completed 2026-04-22
**Completed run — see `wiki/log.md` 2026-04-22 entry and [[transparency-tools]].**
Produced: `mechanisms/transparency-tools.md` + `tools/{keepa,paypal-honey,fakespot,markup-citizen-browser}.md` + updates to `counter-power/regulatory-responses.md` (section 9 transparency-tools sub-section rewrite; design-input #1 extension) and `wiki/index.md`.
Deferred from original plan: OECD 2018 *Personalised Pricing in the Digital Era* (403 bot-wall on both one.oecd.org and www.oecd.org URLs; academic anchor load carried by Hannak et al. 2014 instead); CamelCamelCamel standalone page (networkidle timeout on site capture; referenced on [[keepa]] page as context only); `mechanisms/tech-workaround.md` (superseded for this topic — covered as a sub-taxonomy in [[transparency-tools]]).

## Priority 3

### `/research right to repair movement`
**Lens:** collective framings (primary).
**Mechanisms covered:** boycott; (partially) regulation, tech workaround.
**Likely pages:**
- `mechanisms/boycott.md` — general category; right-to-repair specifically.
- `campaigns/right-to-repair.md` — the movement as a case study in successful collective consumer action.
**Rationale:** Mature, documented movement with clear counter-power lessons. Lower priority only because it sits further from the user's primary querying lenses than the above runs.

### ~~`/research consumer collective bargaining and group purchasing`~~ ✓ completed 2026-04-22
**Completed run — see `wiki/log.md` 2026-04-22 entry and [[consumer-collective-bargaining]] + [[community-choice-aggregation]].**
Produced: `mechanisms/consumer-collective-bargaining.md` + `mechanisms/community-choice-aggregation.md` + `organizations/{park-slope-food-coop,rei}.md` + updates to `counter-power/regulatory-responses.md` (new section-9 sub-section) and `wiki/index.md`.
Deferred from original plan: `mechanisms/collective-bargaining.md` — renamed `consumer-collective-bargaining.md` to avoid collision with [[collective-bargaining-for-data]]; GAO-12-399R standalone treatment (403 bot-wall; Blair & Durrance carries the analytic load plus Wikipedia GPO page captures the GAO 2002 findings via its footnote trail); standalone Rochdale Society / specific CCA / Groupon pages (folded into the anchor mechanism pages due to thin sourcing).

### `/research antitrust regulation evolution`
**Lens:** market solutions.
**Mechanisms covered:** regulation (deeper).
**Likely pages:**
- `mechanisms/regulation.md` — broader-than-antitrust counter-power regulation.
- Updates across existing pages to reference canonical antitrust history.
**Rationale:** The current `regulatory-responses.md` covers enforcement actions but not the legislative/regulatory evolution that makes them possible. Lower priority because the existing page already carries the operational load.

---

## Queue hygiene

- On run, move the entry from this file into the corresponding `/log.md` entry for that research run.
- If a queued run is superseded (e.g., the user decides `/research right-to-repair` is actually higher priority), reorder here rather than starting over.
- If a run produces pages this queue did not anticipate, update the "Likely pages" list on the run's entry before removing it, so the queue reflects actual discovery patterns for future planning.
