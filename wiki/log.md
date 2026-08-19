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

## [2026-08-19] ingest | scale-effects

Eight sources from `raw/research/scale-effects/` on large vs. small institutions: Coase ("The Nature of the
Firm" 1937; Nobel lecture 1991), Niskanen (1968), Parkinson (1955 Economist essay), Klimek/Hanel/Thurner
(2008), Rajan & Wulf (NBER 9633, 2003), Simon (1962), Garicano & Rossi-Hansberg (NBER 20607, 2014).
Three new pages — `bureaucratic-growth-and-parkinsons-law`, `knowledge-hierarchies-and-the-cost-of-scale`,
`hierarchy-and-near-decomposability` — plus extensions to `transaction-costs`, `governance-structures`,
`dimensions-of-institutional-variation` and `path-dependence-and-increasing-returns`, and two conflicts filed.

What landed:
- **The register finally has intra-organisational axes.** D35–D41: funding mechanism (lump-sum vs. per-unit),
  span of control, hierarchy depth (with Klimek's flatness variant ΔL), coupling strength/decomposability,
  communication cost, information-acquisition cost, and formal authority vs. reporting proximity. The
  foundations-NIE ingest recorded the absence of exactly these; the note is now marked partly closed.
- **D25's "information flow" half is superseded, not silently edited.** Garicano & Rossi-Hansberg show that
  communication cost and knowledge-acquisition cost move hierarchy depth in *opposite* directions, so a single
  information-richness axis predicts nothing. D25 keeps its number and its measurability-of-output half, with
  a note pointing at D39 and D40.
- **The sharpest result in the batch** is not about size but about how growth happens: a firm that grows by
  adding a management layer cuts the knowledge and wages of every pre-existing layer; a firm that grows without
  adding one raises them. French administrative panel, firm fixed effects. It is the only mechanism-level
  discriminator this wiki has between functional and dysfunctional growth (Q28).
- **Only two sources in eight are real empirics.** Klimek/Hanel/Thurner (and their historical cases are
  Parkinson's own 1957 figures restated at second hand, n=2) and Rajan & Wulf. Coase, Niskanen, Simon and
  Garicano & Rossi-Hansberg are models their own authors call untested — Niskanen lists the tests that had not
  been run, Coase coined "blackboard economics" for exactly this, Simon disclaims his social extrapolations,
  and Garicano & Rossi-Hansberg say their evidence "fails to falsify" rather than confirms. Every page says so.
- **Parkinson's essay is only partially captured** — ~500 words, cutting off at "statistical proofs, which will
  follow." The Admiralty and Colonial Office numbers he is famous for are *not* in our source; the numbers on
  the page come from Klimek et al. No statistic is attributed to Parkinson anywhere.
- **Two conflicts filed OPEN.** Functional vs. rent-seeking growth (Niskanen against Garicano/Rossi-Hansberg
  and Simon) — probably a scope condition on funding form, stated as the hypothesis to test and deliberately
  not adopted, because no source states it. And Parkinson vs. knowledge-hierarchy accounts of headcount growth,
  which is genuinely unresolved: the two bodies of evidence have no overlap at all.
- **Not filed as a conflict:** Rajan & Wulf's flattening. The paper itself separates an era-driven flattening
  trend (span +50–86%, depth −25%, at flat or falling headcount) from a persistent cross-sectional size→depth
  relationship, and the latter is what Garicano & Rossi-Hansberg predict. Presented as reconciled on
  `governance-structures`.

The negative finding, which is the important one:
- **Institutional age has essentially no data in this batch, and the batch looks like it should.** Klimek's
  "age" is an individual official's career tenure; Garicano & Rossi-Hansberg's is technology vintage; Simon's
  is evolutionary formation time; Niskanen's single age sentence is an aside his own footnote 1 disowns; Rajan
  & Wulf report firm age as a sample statistic and never regress on it. This is load-bearing for outcome 4 and
  directly undercuts what Q7 wanted to claim. Q7 rewritten to say so: the size literature does not supply age
  evidence, and treating size evidence as age evidence is the field's habit, not a finding. No page in this
  batch implies otherwise.
- **Nothing tests firm against bureau on the same axis.** Three sources are firm-only, three bureau-only, and
  two (Simon; Coase's 1991 lecture) assert public/private invariance by analogy without testing it. Q3 moved
  back from partial to open — the batch that should have addressed it did not. Niskanen's footnote 3 hints the
  axis itself may be wrong: funding form, not ownership (Q25).

Thin spots:
- The N≈20–21 decision-body threshold is the most quotable number here and the least defended: one
  uncontrolled cross-section, with reverse causality unaddressed (Q26).
- Simon flags his own theory as incomplete on what determines span; three sources give three incompatible
  answers and none has been tested against the others (Q29).
- Personnel selection (Q4) is still named by no source in this wiki.

## [2026-08-19] ingest | risk-aversion-in-large-institutions

Eight sources from `raw/research/risk-aversion-in-large-institutions/` (Hood, *The Blame Game* ch.1;
Kahneman & Lovallo 1993; Holmström 1982/1999; Manso 2011; Nicholson-Crotty/Nicholson-Crotty/Webeck 2019;
Hammond; Bozeman 1993; OECD OPSI WP 51). Six mechanism pages plus one umbrella page:
`blame-avoidance-and-negativity-bias`, `isolation-errors-and-portfolio-framing`,
`career-concerns-and-managerial-risk-taking`, `exploration-exploitation-incentive-contracts`, `red-tape`,
`veto-points-and-bureaucratic-autonomy`, `risk-aversion-in-large-institutions`.

**The headline, which is negative, and which the pages are built around rather than around the job title.**
The job was commissioned as "why are large institutions risk averse?" — a question that presupposes its
answer. This batch does not support the presupposition:
- **Zero of eight sources test institutional size against risk-taking behaviour.** Not one has a headcount,
  budget or hierarchy-depth variable on the right-hand side of anything.
- **Holmström rejects a size-based account by name.** The Wilson/Ross risk-bearing-capacity story fails once
  a firm is of "even modest size or... a publicly held corporation", because the firm can simply pay a
  constant wage. His own mechanism runs on the external labour market and is size-invariant by construction.
- **The one source that directly measures risk aversion finds against the sector version of the hypothesis.**
  Nicholson-Crotty et al., randomized survey experiment, n=300 real US managers: no sector difference under
  gain framing, public managers *significantly more* risk-tolerant under loss framing (76.62% vs 63.51%,
  p<.10), and status-quo anchoring concentrated in the **private** managers.
- **The most-cited source for institutional timidity denies the reading.** Kahneman & Lovallo: "we do not
  claim that an objective observer would describe managerial decisions as generally risk averse." They pair
  the timidity with an equally-evidenced bold-forecast bias and call the interaction a genuine dilemma.
- **The veto-point intuition is undercut, not supported.** Hammond proves veto-point count and bureaucratic
  discretion are not monotonically related once preference divergence varies — all 720 rank-orderings across
  six systems are achievable. His paper never uses the word "risk". Neither does Bozeman's.

Structure of the umbrella page: two crossed distinctions the sources themselves keep separate. **Mechanism
level** (individual-payoff — Hood, Kahneman & Lovallo, Holmström, Manso, OECD — vs. structural — Bozeman,
Hammond, and Kahneman & Lovallo's groupthink/winner's-curse half). **Claim type** (size claim vs. sector
claim). The size column has no tester and one explicit rejecter; the sector column has four asserters and
one tester, who finds against it. That asymmetry is the batch's actual content.

What each page had to be protected from:
- Hood is an argumentative chapter, not a study; its private-sector extension is one asserted clause with no
  private evidence behind it, and its own reform lever is left open by the author.
- Kahneman & Lovallo would be misrepresented by a page carrying only the timidity half. Both halves on the
  page, plus the authors' warning that correcting only the timidity could make outcomes worse.
- Manso is a **moral-hazard result, not a risk-preference result** — the propositions survive a risk-averse
  agent unchanged, "because the critical elements... are the likelihood ratios between the different action
  plans, not the agent's preferences". No size parameter; Section VIII's large-corporation claim is one HBS
  case and two practitioner books.
- Bozeman never uses the word "risk", says most of his causes are general to any externally-controlled
  organisation (only sovereignty and policy-mission interconnection are government-inherent), and reports
  the public/private literature as genuinely mixed, citing Buchanan 1975 finding *private* managers more
  rule-adherent.
- Hammond gets an explicit "what this page must not be used to support" section.
- The OECD is embedded in the umbrella page and labelled institutional advocacy: 5 of 38 member states,
  heavily self-cited, a hypothetical "Country X" box with zero evidential value, and its own counter-evidence
  (Meijer & Thaens's innovation paradox; ~80% of Nordic workplaces innovating in two years; Danish officials
  fired for failures inside the lever it holds up).

Register: D42–D48 in a new "control and incentive environment" section. Hammond's contribution registered as
**one composite axis** (veto-point count × preference-profile divergence), because a count-only row would
reproduce exactly the error his paper exists to warn against. Three axes deliberately not duplicated —
personal payoff asymmetry cross-linked into D8, rule rigidity into D1, discretion-limiting rules into D9.

Conflict filed OPEN: `presumed-vs-measured-public-sector-risk-aversion`. Settlement criteria recorded, and
the decisive one is a design nobody in the batch attempts — measure behavioural risk-taking **and** the
structural variables (blame exposure, veto-point count, rule density) on the same subjects. The structural
half and the behavioural half of this literature have never been in contact.

Open questions: Q30 restates the wiki's framing question; Q31–Q34 record the gaps (public-sector transfer of
narrow framing; the missing individual→institution aggregation step, which Kahneman & Lovallo's own pooling
arithmetic suggests might *cancel* rather than compound; whether preference, contract artefact and structural
constraint can be told apart from outside; and the same-subjects design). Q3, Q4, Q6 and Q7 updated.

Thin spots:
- The **aggregation step is missing from every individual-level source**, and it is not innocuous. Pooling
  arithmetic predicts an institution holding many independent decisions should be *closer* to risk-neutral
  than any of its agents. Aggregate timidity would then be evidence about internal review design (D46), not
  about size. Kahneman & Lovallo's hierarchy-depth compounding conjecture points the other way. Both come
  from the same model and neither is tested.
- **No baseline is specified anywhere except Kahneman & Lovallo's pooled-portfolio value**, and against that
  baseline their own answer is that the net direction is indeterminate. "Risk averse relative to what?" is
  unanswered by seven of eight sources.
- Nicholson-Crotty's status-quo nulls are the weakest limb of the strongest source: the authors name a real
  Type-II concern themselves, and their mitigation (consistent direction across conditions) is an argument,
  not a resolution. Nonprofits excluded; vignettes validated but not occupation-tailored.
- Personnel selection (Q4) is finally named once — the OECD's Canadian "clay layer" — and it is one country
  scan in an advocacy document with undeveloped coding protocols. Not enough for a register row.
