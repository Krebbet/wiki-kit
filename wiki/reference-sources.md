# Reference Sources

Per-wiki configuration consumed by `/weekly-brief` (and as background context for `/research`). Sections marked **`## Scope`**, **`## Selection priority`**, and **`## Local conventions`** override the corresponding defaults baked into `/weekly-brief`.

## Scope

The weekly scan is **primarily a hunt for combative algorithms, counter-algorithmic tools, platform/federation builds, and community-coordination mechanisms** — concrete technical / organizational counter-force against industry algorithmic power. Legislative, regulatory, and enforcement activity is in scope only as *context* (where it creates tooling openings, standing for collective action, or validates a target), not as the primary capture material.

Ranked focus:

1. **Counter-algorithmic tooling** — obfuscation, adversarial, privacy, DSAR-coordination, fingerprint-defence, data-poisoning, price-transparency, auction-coordination, demand-strike tooling. New tool launches, new papers with releasable code, new releases of tracked tools. This is the primary capture material.
2. **Platform / federation / cooperative builds** — new platform-coops, federation launches, cooperative-software stacks, tenant-/driver-/buyer-side collective-bargaining infrastructure. Org launches, federation events, stack releases.
3. **Counter-power research / think-tank work with implementable hooks** — academic / civil-society work that names a concrete mechanism a tool or federation could implement. Prefer work with released artefacts (code, templates, DSAR kits) over pure analysis.
4. **Extraction-mechanism developments** — industry moves consolidating algorithmic leverage (new pricing-algo deployments, vendor acquisitions, leaks about internal targeting systems, consumer-backlash episodes). In scope as *problem-framing* for where new counter-tools are needed.
5. **Legislation / regulation / enforcement** — in scope only when the action either (a) opens a concrete tooling opportunity (mandated API, disclosure regime with scrapeable surface, new standing for class actions), (b) invalidates a counter-power strategy, or (c) is first-of-kind at a jurisdictional level. Otherwise → watchlist, not captures. General press-release volume is noise.

Wiki-fit gating uses the four querying lenses inherited from `wiki/CLAUDE.md` (**tech-enabled solutions** and **exit pathways** are the load-bearing ones here — a candidate that only speaks to *market solutions* or *collective framings* without a tooling or parallel-institution hook is watchlist material, not capture material):

- Market solutions
- Tech-enabled solutions
- Exit pathways (parallel institutions)
- Collective framings

## Selection priority

Replaces the AI/ML-coded selection heuristic in `/weekly-brief` step 3. In order:

1. **Novel counter-algorithmic mechanism or tool launch** — a new obfuscation / adversarial / privacy / DSAR / coordination tool, a new platform-coop or federation launch, a paper introducing a concrete counter-technique with releasable code. Single-source is *acceptable* here — new tools rarely get multi-outlet coverage on launch week, and waiting for corroboration means missing them. Prefer: released code > promised code > paper-only > org announcement.
2. **Wiki-fit per the four lenses, weighted toward tech-enabled solutions and exit pathways** — see Scope. A candidate whose only fit-hook is "market solutions" (e.g. generic antitrust commentary) or "collective framings" (e.g. movement rhetoric) without a tooling / federation angle is watchlist, not capture.
3. **Conflict-load-bearing** — resolves an open `wiki/conflicts/*.md` or contradicts an existing reference-layer claim. Conflict-loading entries are prioritised over otherwise-equal candidates.
4. **Extraction-mechanism novelty** (problem-side) — a new pricing-algorithm deployment, a leaked internal targeting system, a first-of-kind algorithmic-leverage move. In scope as *target identification* for future counter-tools; expect ≤1 such capture per week.
5. **Enforcement / legislation with a tooling hook** — captured only when the action opens a concrete technical opportunity (mandated API / disclosure surface, new class-action standing, first-of-kind prohibition creating a measurable compliance surface). Multi-outlet coverage of a routine settlement or hearing is *not* a tooling hook — goes to watchlist, trend bullets absorb the context.
6. **Multi-outlet confirmation** — used to resolve ties between otherwise-equal candidates, not as a primary filter. Single-source tool/paper launches beat multi-outlet routine enforcement stories.
7. **Reproducibility / primary-source quality** — court filings, code releases, leaked internal docs, primary press releases > investigative reporting > pure opinion / commentary.

## Local conventions

- **Two-layer split** (from `wiki/CLAUDE.md`): extraction-side captures default to the **reference layer**; counter-power-side captures split between reference layer (concrete orgs/tools/mechanisms — neutral docs) and strategy layer (`strategies/` — editorial synthesis only when the captures justify a new readout).
- **Page format**: every page must have `# Title`, one-paragraph summary (used in `wiki/index.md`), `## Source`, and `## Related` sections. See `wiki/CLAUDE.md` "Page Format".
- **Conflicts**: `wiki/conflicts/<short-name>.md` using the existing template (Position A / Position B / resolution rule). Open speculative conflict files only when ≥2 sources from the run touch the same theme — otherwise skip.
- **Capture cap**: best-5 by signal strength, no per-side floor (counter-power vs extraction). Trend-synthesis bullets cover whichever side gets fewer captures that week.
- **Watchlist overflow**: ≤10 per run (skill default). Surplus is discarded for the week.
- **Index / log / revisions**: update `wiki/index.md`, `wiki/log.md`, `wiki/revisions.md` on every page write. See `wiki/CLAUDE.md` "Modifying the Wiki".
- **`master_notes.md`**: append kit-level findings discovered mid-run with `Status: open`. Don't try to harvest in the same run.

## Sources

The trend-scan source set, grouped by stream. Update freely as outlets prove valuable or noisy. Ordered tiers reflect the signal hierarchy below — **counter-algorithmic tooling surfaces come first**.

### Counter-algorithmic tooling — primary capture surface

- **arXiv cs.CY** (Computers and Society) — new listings in the past week, filtered for: adversarial consumer-side, obfuscation, DSAR, fingerprint defence, data poisoning, price-transparency, collective-bargaining mechanisms.
- **arXiv cs.CR** (Cryptography and Security) — new listings for privacy tools, differential-privacy deployments relevant to consumer-side, anti-tracking techniques.
- **USENIX PETS proceedings** — Privacy Enhancing Technologies, latest volume + preprints.
- **FAccT proceedings** — ACM Fairness, Accountability, and Transparency; monitor through the year, not just conference week.
- **USENIX Security / CCS** — when papers touch consumer-side counter-tools (spoof-ability of pricing inputs, tracker defeat, etc.).
- **GitHub trending (week)** — filtered for privacy / anti-tracking / price-transparency / cooperative-platform topics. Watch `awesome-privacy`, `awesome-adversarial-machine-learning`, `awesome-platform-cooperativism` for new entries.
- **Tracked-tool repos (releases / activity spikes)** — Glaze, Nightshade (SAND Lab), AdNauseam, Privacy Badger (EFF), Markup Citizen Browser, Keepa (drift), uBlock Origin, Tracker Control, Consent-O-Matic, and any repos surfaced via `tools/` wiki pages. Star-spike or release-tag triggers a look.
- **Hacker News** — `show HN` and front-page filtered for consumer-tool / cooperative / privacy-tool launches.

### Platform / federation / cooperative builds

- **platform.coop** — blog + newsletter (Platform Cooperativism Consortium)
- **ica.coop** — International Cooperative Alliance news
- **CoopCycle** + **drivers.coop** news pages — federation updates
- **The Drivers Cooperative** (NYC + Colorado spinout) — launch & scaling news
- **Up & Go**, **Resonate**, **Stocksy**, **Means TV** — platform-coop vertical examples; monitor for new federation moves
- **Open Food Network** — federation updates
- **Data Workers' Inquiry / Workers' Algorithm Observatory** — worker-side tooling
- **noyb** press releases — when tied to a releasable DSAR-kit or template, not just complaints
- **Mozilla Foundation** blog — when they ship consumer-side tools
- `r/PlatformCooperatives` — hot, past week (re-evaluate after 4 runs)

### Counter-power research / think-tank — implementable-hook filter

Prefer publications that name a concrete mechanism or release an artefact. Pure analysis → watchlist.

- **Ada Lovelace Institute** — publications page
- **AlgorithmWatch** — blog + newsletter; especially their tool releases and audit projects
- **Berkman Klein Center** — blog
- **Mozilla Foundation Insights / reports**
- **Open Markets Institute** — reports + blog (tier 2 here; implementation hooks rarer than at the tool-releasing orgs)
- **EFF Deeplinks** — tool announcements, legal-tech releases
- **DAIR Institute** — research outputs

### Extraction — news + blogs (problem-framing, secondary)

Used to identify *where* new counter-tools are needed, not as primary captures. At most 1 capture per run from this tier.

- **BIG** by Matt Stoller — antimonopoly newsletter
- **Pluralistic** by Cory Doctorow — daily, enshittification / pricing beat
- **The Markup** — algorithmic accountability investigations; their *tool* releases (Citizen Browser, Simulator) belong in the counter-algorithmic tier instead
- **ProPublica** — tech / economics beat
- **404 Media** — surveillance / pricing / data-broker leaks
- **Rest of World** — non-US platform-extraction coverage
- **Hell Gate** + **Platformer** — critical tech press
- **Wired**, **The Information**, **WSJ** business — headlines only

### Enforcement — watchlist-default

Captured only when a tooling hook is present (see Selection priority #5). Otherwise → watchlist or trend-bullet absorption.

- **FTC** press releases
- **DOJ Antitrust Division** press releases
- **NY**, **CA**, **WA** state AG press releases
- **EU Commission DG COMP** press releases
- **UK CMA** news
- **CourtListener** — RSS for relevant docket filings (RealPage, Greystar, gig-economy pricing)

### Subreddits — discovery / backlash early-warning

- `r/PlatformCooperatives`
- `r/Antimonopoly`
- `r/privacytoolsIO`, `r/privacy` — tool launches + tool-breakage signal
- `r/degoogle`, `r/selfhosted` — exit-pathway adjacent
- `r/LateStageCapitalism` — backlash signal only

*(Re-evaluate after 4 runs. Drop any that hasn't surfaced a captured-quality candidate by then.)*

## Email subject template

The skill's default subject is `Weekly AI radar (<REPO_NAME>) — week of <YYYY-MM-DD>`, which doesn't fit this wiki's domain. Override:

`Weekly counter-power radar (<REPO_NAME>) — week of <YYYY-MM-DD>`

## Trend-scan signal hierarchy

Replaces the alphaXiv / r-MachineLearning / AK-timeline / paperswithcode chain in `/weekly-brief` step 1. Cheapest to most expensive. **The first two tiers are where the week's captures mostly come from; tiers 3–6 are context and confirmation.**

1. **arXiv cs.CY + cs.CR (past 7d) + tracked-tool repo activity + GitHub trending** — new counter-algorithmic papers and tool releases. Single-source *is* enough for capture consideration at this tier; novelty and releasability matter more than multi-outlet corroboration.
2. **platform.coop + ica.coop + CoopCycle + drivers.coop + DAIR + EFF + AlgorithmWatch + Ada Lovelace + FAccT/PETS/USENIX windows** — counter-power build and research signal. Any new tool, federation move, or artefact-releasing publication is a capture candidate.
3. **BIG + Pluralistic + The Markup + ProPublica + Platformer + Hell Gate** — editorial signal. Primary use here is (a) to surface tool/coop launches that tiers 1–2 missed and (b) to provide problem-framing / target identification for future tools. Routine antitrust / monopoly commentary without a tooling hook → trend-bullet absorption, not captures.
4. **noyb + Mozilla + CourtListener** — artefact-linked research and litigation discovery. Captures when they release a template/tool or when a docket filing opens concrete standing for a counter-tool; watchlist otherwise.
5. **404 Media + Rest of World + Wired** — surveillance / extraction news. Use for confirmation and problem-framing; rarely a primary capture surface.
6. **FTC / DOJ / state-AG / DG COMP / CMA press releases** — enforcement events. **Watchlist by default**; promote to capture only when Selection priority #5 applies (mandated API, new standing, first-of-kind prohibition with measurable compliance surface). Volume here is not signal.
7. **Subreddits** — discovery proxy for tool launches and backlash episodes mainstream outlets haven't picked up yet. Subreddit-only signals go to watchlist unless tiers 1–3 corroborate.

A tier-1 candidate with releasable code can enter selection on a single source. Tier-3 editorial candidates need a tooling or federation hook — multi-outlet coverage alone doesn't qualify. Tier-6 candidates need the hook spelled out explicitly in the one-line why-trending note.
