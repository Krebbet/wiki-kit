# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-08-19] bootstrap | institutions

Initial bootstrap. Schema and commands tailored for the study of institutions: institutions as a general
concept (function, failure, lifecycle, scale effects) and the macro system of institutions / power /
economic production. Synthesised from `boot_strap_instructions.md`.

Key tailoring decisions:
- Books treated as first-class sources (the canon here is book-shaped and pre-open-access); second-hand
  treatments are permitted but must be labelled as such on the page.
- Ideological balance made a hard research requirement — a topic dir whose sources all lean one way is a
  research failure. Enforced by a lint check.
- Evidence-tier labelling (empirical / model / wiki synthesis) required throughout, and a lint check added
  for thesis drift: the user's collapse-and-renewal premise and the power/institutions/economy triad are the
  working hypothesis, not a finding.
- Case-study pages must carry sector / scale / age / country tags so cross-cutting comparison is possible.

## [2026-08-19] seed | research agenda and weekly brief

Seeded `wiki/research-agenda.md` (10 opening research jobs in dependency order, then four phases mapped to
the six project outcomes), `wiki/open-questions.md`, `wiki/reference-sources.md` (weekly-brief radar), and
`wiki/watchlist.md`. No sources captured yet — the wiki is empty of content pages by design until the first
`/research` run.

## [2026-08-19] ingest | foundations-nie

First content pages. Ingested the five-source foundations set from `raw/research/foundations-nie/`
(North JEP 1991; North "Institutional Change: A Framework of Analysis"; Ostrom Nobel lecture 2009;
Williamson Nobel lecture 2009; Libecap NBER WP 24585 on North). Seven pages written:
`what-is-an-institution`, `dimensions-of-institutional-variation`, `transaction-costs`,
`governance-structures`, `path-dependence-and-increasing-returns`, `credible-commitment`, `polycentric-governance`.

What landed:
- **Definitions.** Three incompatible objects, not three phrasings: North's societal rule-set with
  organizations as separate players; Ostrom's meso-level rules-in-use (seven rule types); Williamson's
  transaction with the firm as a derived aggregate. Q1 answered far enough to state a candidate minimal
  definition and to name its price (it dissolves North's institution/organization boundary).
- **The dimensions register** now carries 34 axes (D1–D34), each with an operationalisation and a status.
  Thirteen promoted under a stated two-part criterion (named by ≥2 sources AND measurable from documents or
  observable behaviour). D34 (North's "adaptive efficiency") is recorded as `rejected` — no operationalisation
  exists that does not define it by the outcome it explains — kept visible per lint check 11 rather than dropped.
- **Evidence quality is the main finding.** All four theory sources are history-of-thought or comparative
  narrative, not identification. North's JEP essay offloads its big comparative claims (Europe vs. Spain,
  North vs. Latin America) to earlier books; Williamson's lecture asserts an 800-test empirical literature
  it does not reproduce; Libecap concedes transaction costs "are not clear in aggregate studies of economies."
  Ostrom's lab/field experiments are the only clean causal identification in the set, and they do not bear on
  the definitional or growth claims. Pages say so explicitly.
- **Second-hand labelling.** Libecap's North-attributed material is marked second-hand on every page that uses
  it; his oil/fisheries/groundwater case work is marked as his own primary evidence.
- **Two conflicts filed OPEN** (see revisions).
- **Best single operationalisation found:** the lease-to-sale price ratio of a transferable entitlement as a
  market-priced estimate of commitment credibility (US ITQ ratio ≈ 2× New Zealand's). Generalises well beyond
  fisheries; registered as D11.

Thin spots, stated rather than padded:
- Nothing in this source set describes the *inside* of a single organisation. No axis for personnel selection,
  mandate clarity, funding source, layer count as behaviour, or organisational age. Q20 and Q4 record the gap.
- Ostrom's design principles are derived from small-to-medium commons; their transfer to agencies and firms is
  assumed by nobody and tested by nobody (Q19).
- Path dependence "with age" is a matrix-level claim throughout; the organisational reading this wiki wants is
  an inference by analogy, not a finding.
