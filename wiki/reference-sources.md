# Reference Sources

Per-wiki configuration consumed by `/weekly-brief` (and as background context for `/research`). Sections marked **`## Scope`**, **`## Selection priority`**, and **`## Local conventions`** override the corresponding defaults baked into `/weekly-brief`.

## Scope

Dual-focus weekly scan:

1. **Counter-power leads** — new cooperatives, tools, campaigns, and academic / think-tank work that supports collective consumer action via technology. Feeds the strategy layer (`strategies/`) and the reference layer (`organizations/`, `tools/`, `mechanisms/`, `counter-power/`).
2. **Extraction-mechanism developments** — industry moves consolidating market power, especially new algorithmic / technological leverage against consumers (new pricing-algo deployments, vendor acquisitions, leaks/exposés about internal targeting systems, consumer-backlash episodes). Feeds the reference layer (`industries/`, `mechanisms/`).

Wiki-fit gating uses the four querying lenses inherited from `wiki/CLAUDE.md`:

- Market solutions
- Tech-enabled solutions
- Exit pathways (parallel institutions)
- Collective framings

A candidate that doesn't speak to at least one lens is not in scope, regardless of how trending it is in its origin source.

## Selection priority

Replaces the AI/ML-coded selection heuristic in `/weekly-brief` step 3. In order:

1. **Multiple independent signals** — covered by ≥2 outlets in the source set below. Single-source mentions go to the watchlist, not captures.
2. **Wiki-fit per the four lenses** — see Scope.
3. **Conflict-load-bearing** — resolves an open `wiki/conflicts/*.md` or contradicts an existing reference-layer claim. Conflict-loading entries are prioritised over otherwise-equal candidates.
4. **Mechanism novelty over volume** — a new pricing-algorithm deployment, a new counter-power org launch, or a first-of-kind enforcement action beats five reframings of an already-documented pattern.
5. **Reproducibility / primary-source quality** — court filings, code releases, leaked internal docs, primary press releases > investigative reporting > pure opinion / commentary.

## Local conventions

- **Two-layer split** (from `wiki/CLAUDE.md`): extraction-side captures default to the **reference layer**; counter-power-side captures split between reference layer (concrete orgs/tools/mechanisms — neutral docs) and strategy layer (`strategies/` — editorial synthesis only when the captures justify a new readout).
- **Page format**: every page must have `# Title`, one-paragraph summary (used in `wiki/index.md`), `## Source`, and `## Related` sections. See `wiki/CLAUDE.md` "Page Format".
- **Conflicts**: `wiki/conflicts/<short-name>.md` using the existing template (Position A / Position B / resolution rule). Open speculative conflict files only when ≥2 sources from the run touch the same theme — otherwise skip.
- **Capture cap**: best-5 by signal strength, no per-side floor (counter-power vs extraction). Trend-synthesis bullets cover whichever side gets fewer captures that week.
- **Watchlist overflow**: ≤10 per run (skill default). Surplus is discarded for the week.
- **Index / log / revisions**: update `wiki/index.md`, `wiki/log.md`, `wiki/revisions.md` on every page write. See `wiki/CLAUDE.md` "Modifying the Wiki".
- **`master_notes.md`**: append kit-level findings discovered mid-run with `Status: open`. Don't try to harvest in the same run.

## Sources

The trend-scan source set, grouped by stream. Update freely as outlets prove valuable or noisy.

### Counter-power — movement

- **platform.coop** — blog + newsletter (Platform Cooperativism Consortium)
- **ica.coop** — International Cooperative Alliance news
- **CoopCycle** + **drivers.coop** news pages — federation updates
- **Open Markets Institute** — reports + blog
- **Mozilla Foundation** blog — when they ship consumer-side tools
- `r/PlatformCooperatives` — hot, past week (re-evaluate after 4 runs)

### Counter-power — research / think-tank

- **Ada Lovelace Institute** — publications page
- **Berkman Klein Center** — blog
- **AlgorithmWatch** — blog + newsletter
- **NoyB** — press releases
- **FAccT proceedings** — when conference is active (annual)

### Extraction — news + blogs

- **BIG** by Matt Stoller — antimonopoly newsletter
- **Pluralistic** by Cory Doctorow — daily, enshittification / pricing beat
- **The Markup** — algorithmic accountability investigations
- **ProPublica** — tech / economics beat
- **404 Media** — surveillance / pricing / data-broker leaks
- **Rest of World** — non-US platform-extraction coverage
- **Wired** — business / tech
- **Hell Gate** + **Platformer** — critical tech press
- **The Information** — headlines only (paywalled)
- **WSJ** business section — headlines only (paywalled)

### Enforcement — secondary / supporting

- **FTC** press releases
- **DOJ Antitrust Division** press releases
- **NY**, **CA**, **WA** state AG press releases (most active on platform / algorithmic-pricing matters)
- **EU Commission DG COMP** press releases
- **UK CMA** news
- **CourtListener** — RSS for relevant docket filings (RealPage, Greystar, gig-economy pricing)

### Subreddits — discovery / backlash early-warning

- `r/PlatformCooperatives` (also listed under counter-power-movement)
- `r/Antimonopoly`
- `r/LateStageCapitalism`

*(All three: re-evaluate after 4 runs. Drop any that hasn't surfaced a captured-quality candidate by then.)*

## Email subject template

The skill's default subject is `Weekly AI radar (<REPO_NAME>) — week of <YYYY-MM-DD>`, which doesn't fit this wiki's domain. Override:

`Weekly counter-power radar (<REPO_NAME>) — week of <YYYY-MM-DD>`

## Trend-scan signal hierarchy

Replaces the alphaXiv / r-MachineLearning / AK-timeline / paperswithcode chain in `/weekly-brief` step 1. Cheapest to most expensive:

1. **BIG + Pluralistic + The Markup + ProPublica** — primary editorial signal for both extraction and counter-power. High signal, low noise.
2. **FTC / DOJ / state-AG press release feeds** — hard enforcement events. Discrete and dated; easy to dedupe.
3. **AlgorithmWatch + Ada Lovelace + Berkman + NoyB** — research / think-tank signal. Slower cadence; treat any new publication as a candidate.
4. **platform.coop + ica.coop + Open Markets** — movement signal. Lower volume; new-org announcements and federation-event reporting.
5. **404 Media + Rest of World + Wired + Hell Gate + Platformer** — surveillance / extraction news. Use for confirmation against the BIG/Pluralistic/Markup primary signal.
6. **Subreddits** — discovery proxy for consumer-backlash episodes that mainstream outlets haven't picked up yet.
7. **CourtListener** — litigation discovery; usually one-off filings worth flagging to the watchlist.

A candidate that surfaces ≥2 times across signals 1-5 enters the selection ranking. Subreddit-only or CourtListener-only signals go to the watchlist by default and only become captures when a primary outlet (1-5) corroborates.
