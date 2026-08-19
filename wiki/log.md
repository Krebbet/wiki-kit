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

---

## [2026-08-19] ingest | incentives-and-institutional-form

Eight sources on how incentive structure determines institutional form: Holmström's and Hart's 2016 Nobel
lectures, Holmstrom & Milgrom's 1991 multitask paper, Grossman & Hart 1986, Prendergast's 1999 JEL survey,
Dixit's 2002 public-sector review, Frey on motivation crowding, and Bénabou & Tirole on intrinsic and
extrinsic motivation.

Four new pages, merged where the overlap was real rather than one page per source:
- **`multitask-incentive-theory`** — Holmström's lecture folded into Holmstrom & Milgrom, since the lecture
  is largely his own restatement of that model. The load-bearing result is stated as the sources state it:
  when some tasks are measurable and others are not, high-powered incentives on the measurable ones destroy
  effort on the rest, so low-powered pay plus bureaucratic rule-boundedness is the rational design response.
  All seven propositions are recorded as untested **by the authors' own admission** — they defer "new,
  testable results" to a companion working paper, and the one study they lean on (Anderson & Schmittlein) is
  conceded to be equally consistent with two competing explanations from inside their own theory.
- **`property-rights-theory-of-the-firm`** — Grossman & Hart merged with the property-rights half of Hart's
  lecture. Hart-Moore "shading" kept as its own clearly separated section, because it abandons full
  rationality, which the rest of the page assumes. The prison case is included and its narrowness stated in
  the section itself: one service, one country, one correlational citation on outcomes.
- **`incentives-under-multiple-principals`** — Dixit, the batch's only direct public-sector source.
- **`motivation-crowding`** — Frey and Bénabou & Tirole on one page, two mechanism sections, with a table
  showing where they diverge and the discriminating test (transparency) that neither source runs.

Conflicts:
- **Filed OPEN: `rival-firm-boundary-theories`.** Asset specificity vs. residual control rights vs.
  measurement cost. The ingest flagged this without checking; `governance-structures` was read in full first
  and states only the Williamson and Coase accounts, so this is new territory for that page rather than a
  contradiction of it. Holmstrom & Milgrom's own §1 does the work: they claim to reproduce Williamson's
  central stylised fact "without relying on any assumptions about specific investments," and emphasise
  measurement cost "in contrast to the leading approaches, which stress asset specificity."
- **Deliberately not filed: "high-powered incentives good vs. bad."** It resolves by scope and both sides say
  so. The informativeness principle holds for a single cleanly-measurable task; multitasking and crowding are
  two independent mechanisms by which the same incentive backfires once measurability or perceived valence
  breaks down. Presented that way on `multitask-incentive-theory` rather than as a contradiction.
- **Recorded as a tension, not a conflict, at D9.** Dixit and Holmstrom read bureaucratic rule-boundedness as
  rational efficient design; Libecap's existing D9 entry reads regulators' discretion-preservation as
  self-serving. Preserving and reducing discretion are opposite moves — Libecap's actor protects his own
  decision space, Dixit's principals constrain someone else's — so it is not a contradiction. The consequence
  is recorded where it bites: a score on D9 is no longer self-interpreting and must be read with D50 and D51.

Register:
- **D25a** added as a refinement of D25, handled the way D25's earlier supersession was handled — D25 keeps
  its number and carries a pointer, so the change is visible rather than silent. Contractibility (specifiable
  ex ante), verifiability (provable to a court ex post) and mere observability come apart in real
  relationships, and which one binds determines the institutional form: Aghion-Bolton assume returns are
  verifiable and get equity-like state-contingent control; Hart-Moore drop it and get debt.
- **D49–D53** added (D42–D48 were being taken concurrently by the risk-aversion ingest). Two of the five are
  **`rejected`**, per lint check 11, with reasons and readmission conditions: Frey's controlling-vs-supportive
  valence (D52) and Bénabou & Tirole's sorting condition (D53). Both fail the same way — the label is applied
  after the outcome it explains is known, so neither has an operational measurement procedure in its own
  source. Recorded rather than dropped so the problem stays visible.
- D50 (action-observability × outcome-observability, after Wilson) is the batch's most reusable addition:
  both components are answerable from an institution's own case records. Recording caveat: Dixit's text names
  only three of Wilson's four cells — procedural, craft, coping — so the both-observable cell is inferred
  from the 2×2 and is not attributed to him.

The honest bottom line, which is the important part:
- **This batch is predominantly formal theory.** Six of eight sources contain no original data at all.
- **Four of eight are explicitly silent on selection effects** — Holmström's lecture and Holmstrom & Milgrom
  (agents "identical ex ante"), Grossman & Hart, and Hart's lecture. Bénabou & Tirole is a fixed-agent story
  too. This is a structural gap in the literature, not a nuance.
- **The real tested empirics cluster in two places**: Prendergast's clean selection-vs-incentive decomposition
  (~1/3 of Lazear's 35% piece-rate gain is selection; Paarsch & Shearer isolate ~10% incentive effect on a
  given worker) and the Courty & Marschke JTPA administrative data on threshold gaming and cream-skimming.
  Q4 moved open → partial on that basis and no more — **one source, two occupations, both with unusually clean
  output measures**, which Prendergast himself flags as the least representative slice of the workforce.
- **Public-bureau coverage rests on Dixit alone**, corroborated only narrowly by Hart's prison case, which
  reaches a compatible conclusion by a different mechanism for the make-or-buy boundary only. Q3 moved
  open → partial because the wiki now has a specified, testable claim ("degree, not kind") where it had none —
  not because it has been tested. Q38 is the discriminating test.
- Q9 annotated rather than moved: the batch supplies a good account of how institutional *form* varies with
  measurability and nothing at all about decay, because **no source in it is longitudinal**.

Thin spots:
- Two untested formal mechanisms — unmeasurability and influence cost — produce bureaucratic rules
  identically, and the wiki cannot currently tell them apart (Q35). They differ in what happens when
  measurement improves, which is the test.
- Prendergast's verdict was added to the North side of `efficiency-of-institutions-north-vs-williamson` with
  his own hedge preserved: the record is unpersuasive largely because contracts are unobserved, which is
  evidence the efficiency default is *undemonstrated*, not that it is false.
- Hart's "efficiency, not ideology" was added to the Williamson side, scope-limited three ways — and paired
  with his own report that the Maskin-Tirole mechanism, which would make unverifiable variables contractible,
  is never used in practice. A founder of the tradition documenting parties not adopting an available
  efficiency-improving instrument.

---

## 2026-08-19 — ingest: institutional-evolution (7 sources)

Sources: North's 1993 Nobel lecture; Arthur (1989, *Economic Journal*); Pierson (2000, *APSR*); DiMaggio &
Powell (1983, *ASR*); Meyer & Rowan (1977, *AJS*); Thelen (2009, *BJIR*, presenting the Streeck & Thelen and
Mahoney & Thelen typology); Krasner (1984, *Comparative Politics*).

**Step 1: the Arthur audit, run before anything was written.** The job brief asked whether
`path-dependence-and-increasing-returns` over-cited Arthur or sourced institutional claims to him. Grepped the
whole `wiki/` tree, including `conflicts/`. **Arthur appears exactly once in the entire wiki**, in that page's
evidence-tier note, and the citation was already correct: "North's increasing-returns mechanism is imported
from Arthur and David on technology and asserted for institutions; the essay tests nothing." No institutional
claim anywhere was sourced to him. **No correction was required.** The audit result is recorded on the page
itself rather than only here, so a future reader can see the check was done. The new Arthur subsection states
the scope limit explicitly — his paper contains none of the words "institution", "organisation", "agency",
"bureaucracy" or "governance", and his agents are consumers choosing reactors and keyboards — so the citation
stays honest as the page grows.

**The batch's evidence profile, which is the context for everything below.**
- **Only one of seven sources is a formal model with proofs (Arthur), and it is about technology adoption.**
- The only genuine figures in the batch are **Skocpol's association counts** (secondhand via Pierson) and
  **Wallis & North's 45%-of-1970-US-GNP transaction sector** — and the second is not about path dependence at
  all. It is noted on the path-dependence page as belonging to `transaction-costs`, which a later pass should
  pick up; this job did not touch that page.
- **Three sources independently carry no falsification condition** — North, Pierson, Krasner — and only
  Pierson admits it, citing Geddes 1997.
- Two sources (DiMaggio & Powell, Meyer & Rowan) present **no original data by their authors' own statement**.

**The age question, which this job was commissioned to settle, and did not.**
This was supposed to be where age evidence finally appeared after the size batch and the risk-aversion batch
both came back empty. It largely does not appear, and one source argues against the premise:
- **Arthur's clock is adoption count *n*, not calendar time**, and he warns expressly against the "N years"
  reading. His one quantified threshold (30 of 100 adoptions) is a technology-market result.
- **North's durations** — ~500 years post-Rome, ~400 years of Spanish decline, ~800 years of European rise —
  are post-hoc narrative with no threshold, no rate and no dose-response. Spain declines continuously with no
  point of no return identified.
- **Skocpol's dataset measures survival, not behavioural change with age.** It is the batch's only systematic
  longitudinal data and it answers a different question. Read the other way it is 75% attrition over a century.
- **DiMaggio & Powell's** repeated cross-study claim is about **field** maturity, not organisational age, and
  originates zero measured intervals in their own text.
- **Meyer & Rowan** supply nothing on age or size and flag the gap themselves.
- **Krasner's own cited case data undercut his framing**: Skowronek's "punctuation" is 20 years against a
  "stasis" of 23.
- **Thelen denies the premise in principle**: contestation "often begin[s] as soon as a rule is laid down", and
  her fourth gap-mechanism runs the *opposite* way on elapsed time — as designers die and context shifts,
  interpretive space opens.

So: **three literatures searched, no measurement of institutional behaviour against elapsed time since
founding.** Q7 now records that source-by-source, and Q39 states the study that would supply it — reversal
*attempt* success rate against time since the rule was laid down, with the denominator being attempts rather
than successes, because measuring only successful changes selects on the outcome. That is the mistake the
whole path-dependence literature makes, and it is now written down.

**Pages.** Extended `path-dependence-and-increasing-returns` with four sections (Arthur as formal ancestor;
North's cognitive mechanism; the duration catalogue; Pierson; and a reconciliation section against Thelen).
The page's opening claim — matrices get less flexible with age — is now demoted to North's *attributed*
position rather than the page's conclusion, because a source in the wiki now contests it. Four new pages:
`institutional-isomorphism`, `institutional-myths-and-decoupling`, and the explicitly paired rival set
`gradual-institutional-change` / `punctuated-equilibrium-and-the-state`, each of which opens by naming the
other.

**Register.** D54–D59 added. D54 (formal amendment/reversal threshold) is registered with an explicit
statement of how it differs from D44 — D54 is a property of the *rule* (the written threshold, readable from
primary documents, invariant to who holds the veto positions), D44 is a property of the *current actor
configuration* (count jointly with preference divergence, and non-predictive without the second term per
Hammond). A body can be high on one and low on the other. **D58 registered `rejected`**: Arthur's
adoption-count reversal cost does not survive translation, because institutions supply no counter analogous to
*n* — rules are continuously re-enacted by overlapping cohorts with renegotiable authority, whereas Arthur's
agents choose once and are frozen. Readmission condition recorded. **North's adaptive/allocative axis was
deliberately not re-registered**: it duplicates the already-`rejected` D34 and the lecture supplies no
operationalisation the second time either. A second naming by the same author is not a second piece of
evidence, and the note went on D34 rather than into a new row.

**Conflicts.** Two filed OPEN, one extended.
- `rival-models-of-institutional-change` — the headline. The important finding is that the three positions
  **disagree about no observation**; they classify the same observations differently. German VET fits all
  three: "lock-in" (the form survived), "stasis" (no crisis), and "conversion" (function transformed without
  formal change). That is why five settlement tests are listed rather than an adjudication.
- `homogenisation-vs-loose-coupling` — within-tradition, and unusually clean because DiMaggio & Powell name
  the divergence in their own text at Hypothesis A-3. The consequence recorded on both pages: the wiki cannot
  cite "sociological institutionalism" for anything about internal behaviour without saying which limb.
- `functional-vs-rent-seeking-growth` **extended rather than duplicated**, per the brief. Position C
  (ceremonial conformity) is a third answer to the same question, and the sharpest addition is the comparison
  table: Positions A and B both assume an efficiency audit is possible and disagree about what it would show,
  while Position C predicts **the audit will not happen**, because evaluation threatens the legitimacy the
  structure exists to produce.

**Flagged, not resolved.** Pierson/Skocpol's century-old voluntary associations persisting against Rajan &
Wulf's old large firms restructuring substantially. Two candidate reconciliations, neither stated by any
source: sector, or different dependent variables (existence-at-threshold vs. internal structural change). The
second is more interesting, because if it is right then the persistence literature has been measuring the
wrong quantity for the age question all along — which is Thelen's form/function point (D55) arriving from a
different direction. Q44.

**Thin spots.**
- **Displacement, one of Thelen's four mechanisms, has no worked example in the source.** A quarter of the
  typology is untested by its own author's evidence, and the 2×2 is exhaustive by construction, so any
  observed change can be redescribed post hoc once the two axes are somehow scored. Discretion is sometimes
  inferred *from* the fact that drift occurred.
- **Krasner is a review essay contributing a metaphor.** He does not engage the falsifiability debate that
  surrounded the biological original — he imports the label. The stability half (sunk information, trust and
  shared expectations, as a comparative-cost argument) is genuinely stronger than the change half.
- **The twelve DiMaggio & Powell hypotheses are the batch's only near-testable propositions and none was
  tested by anyone.** Q41 exists mainly so the wiki does not quietly treat them as findings.
- Meyer & Rowan is the weakest evidence tier in the wiki — a conceptual essay with hand-picked anecdotes —
  and it is carrying one full limb of an extended conflict. Weighted accordingly on the page and in the
  conflict, but worth stating plainly.
