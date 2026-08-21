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

---

## 2026-08-19 — ingest: institutional-stagnation (9 sources)

Merton (1940); Stigler (1971); Selznick (1948); Fukuyama (2014); Miller & Dudley (2016); Schleicher &
Bagley (2025/26); plus three dedicated critics — Carpenter & Moss (2014), Novak (2014), Heckelman (2007).

Seven new pages: `regulatory-capture`, `institutional-sclerosis`, `goal-displacement-and-bureaucratic-ritualism`,
`cooptation`, `regulatory-accretion`, `political-decay-and-vetocracy`, `state-capacity-and-level-of-government`.
`veto-points-and-bureaucratic-autonomy` extended with a contested-cases section. D60–D65 registered (D65
`rejected`). One conflict filed OPEN. Q7 and Q8 updated; Q60–Q65 added.

**This is the job commissioned to test the wiki user's book premise — that institutions decay with age. The
verdict has four parts and they must not be collapsed into each other.**

1. **Well evidenced, and structural rather than temporal.** Regulation and procedure create rents that favour
   organised, concentrated incumbents over diffuse publics. Stigler's trucking regression (46–48 states,
   three significant coefficients, correct signs, R² 0.24–0.50) is the batch's cleanest single result. Miller &
   Dudley's JPMorgan "moat" is the same mechanism in a modern instance; Liscow & Brooks on US highway costs,
   via Schleicher & Bagley, is the same again in procedural form. **This is a cross-sectional finding about
   *who benefits*. It is not an age-decay finding, and the two must not be blurred.**

2. **Theorised but unmeasured — most of the batch.** Merton's ritualism, Selznick's cooptation, Fukuyama's
   vetocracy, Miller & Dudley's accretion, Schleicher & Bagley's procedural tax. Coherent mechanisms,
   essentially no independent test of the mechanism itself. Four of the nine sources state no falsification
   condition at all; Carpenter & Moss's three-part test is the only one in the batch.

3. **Contested: capture as an age phenomenon, specifically.** The canonical evidence — Olney's 1892 letter,
   Huntington's "marasmus", Bernstein's life-cycle — is shown by two dedicated critics to be a single anecdote
   laundered through decades of citation, and Novak shows capture risk was anticipated at the ICC's 1871
   design (Charles Francis Adams: "Who will guard the virtue of the tribunal?"), which removes the healthy
   youth the decline story needs. Note precisely: **neither critic runs an age test. The age reading is
   unevidenced, not refuted**, and the pages say so in those words.

4. **Evidenced against institution-level age as the driver.** Wherever age or duration appears in this batch it
   attaches to a **political regime, a legal corpus, or a national polity** — never to a single institution's
   own tenure. Fukuyama's veto structure is 230 years old and he pins the dysfunction to 1980s polarisation.
   Miller & Dudley's and Schleicher & Bagley's accretion dates to a 1970s–80s legal wave applied uniformly
   regardless of any agency's founding date. Heckelman's variable is years of national political *stability*.

**The single most striking fact in the batch, and it was volunteered:** Merton, Stigler and Selznick each state
that their own mechanism is age-independent — unprompted, without being asked to address any decay thesis, and
decades before one was posed to them. Three founders of the decay-mechanism literature declining a claim later
attributed to them is not a critics' point-scoring exercise, and it is filed on Position B of the conflict as
such.

**Heckelman is the tiebreaker and is reported whole, deliberately.** 53 studies of Olson's sclerosis thesis:
**57% support, 23% mixed, 21% no support**, with no significant difference by methodology, publication outlet,
author location or year (28 regressions at 57/18/25; 25 case studies at 56/28/16). But only "a handful"
directly test coalition *accumulation* — Olson's Implication 2 — and the vast majority instead relate
stability duration to growth, "leaving the role of special interest organizations and distributional coalitions
implicitly in the background". He discloses a conflict of interest (Olson tribute-volume editor; author of
three of the 53, all coded Support), tests it with two dummies, and finds it does not move the split. And a
companion survey (Heckelman & Whaples 2006) finds practising economists (2.53) and political scientists (2.39)
scoring *below* the midpoint on the theory's signature prediction — "Apparently, there is not widespread belief
in Olson's explanation for the rain." **Neither "the evidence supports sclerosis" nor "sclerosis is debunked"
can be read off this page, and that is by construction.**

The settlement criterion, now filed in the conflict and as Q60: a study measuring a **specific institution's
own age** against a **directly observed accumulation variable** — coalition count, rule count, capture
indicator — rather than regime-stability duration or cross-sectional density, in a panel, controlling for
external-regime vintage and principal polarisation. **No source in this batch does this. No source in four
batches does this.**

Thin spots, all filed as questions rather than left in this log:
- Nobody anywhere tests organisational age as a first-class independent variable (Q60).
- Heckelman never enumerates the "handful" that directly test accumulation, so the 57% is a Layer-1 number
  standing in for a Layer-2 claim (Q62).
- Selznick's TVA grounding is unread — the 1948 article is theory only, and the case appears in it as a
  footnote announcing a forthcoming book. Huntington 1952 and Bernstein 1955 are likewise held only
  second-hand through Novak (Q63).
- **Not one of the nine sources examines a private-sector institution** for any of these mechanisms. Merton and
  Selznick assert generality and test nothing; Stigler and Schleicher & Bagley are scope-limited by
  construction; the other five are silent. Merton supplies the discriminating test himself — hold sector fixed
  and vary monopoly vs. competition (Q64).
- No institution in the batch has a design-specified sunset or review trigger, in either direction (Q65).

## [2026-08-19] ingest | enabling-institutional-change

Eight sources on what enables institutional change: Bunse & Fritz (World Bank portfolio review), Sabel &
Zeitlin (experimentalist governance), Finan/Olken/Pande (personnel economics of the state), True/Jones/
Baumgartner (punctuated equilibrium), the NAO's reorganisation audit, Andrews/Pritchett/Woolcock (isomorphic
mimicry and PDIA), Cox/Arnold/Villamayor-Tomás (design-principles review) and O'Reilly & Tushman
(ambidexterity). Seven new pages, one triage page, one correction to an existing page.

**The correction came first.** `polycentric-governance` carried "a review of 100+ studies confirms them in
about two-thirds of cases", taken secondhand from Ostrom's Nobel lecture. The published review is now a
captured primary source and reports neither figure: 91 studies, 77 cases, mean study-level support 3.73 on a
1–5 scale, and per-principle supportive:unsupportive case ratios tested with Fisher's exact — significant at
5% for principles 1–7 and only at 10% for principle 8 (nested enterprises), every association positive, every
principle at least 2:1 supportive. Very strongly supported: congruence with local conditions (2A),
appropriation/provision proportionality (2B), and **monitor accountability to the users** (4B) — not the mere
presence of monitors, which is only moderate. The likely explanation for the discrepancy is in the paper's own
acknowledgments: the 2010 article revises a 2009 report titled *Design Principles Are not Blue Prints, but Are
They Robust?: a Meta-analysis of 112 Studies*. That accounts for "100+" and for the "2009" date Ostrom cites;
"two-thirds" matches no reported statistic in either version. The superseded figure is left visible on the page
with that explanation attached, rather than overwritten — the failure mode (a Nobel lecture's paraphrase of a
colleague's working draft hardening into a wiki fact) is worth being able to catch a second time.

**The batch's headline is a negative, and it is stated on `reorganisation-base-rate`.**

- **Only two of eight sources supply anything resembling a reform base rate**, and both point the same way:
  measured success substantially overstates genuine change. NAO — 93 UK central-government reorganisations
  2005–09, 51 audited in detail, £780m gross (an under-estimate on seven grounds NAO lists itself), value for
  money "cannot be demonstrated", **0% of departments setting any benefit metric** against 73% of arm's length
  bodies. Bunse & Fritz — **~75% operation-level success against 47% country-level transformation**, with the
  gap attributed by the authors themselves to selecting politically easy, non-rent-threatening components.
- **The other six are not reform base rates, in six different ways.** Cox measures principle-presence against
  the *survival of existing commons systems* — no case installs a principle where one was absent, so **using
  Cox as reform evidence is a category error**, and that sentence is on three pages because it is the mistake
  this batch most invites. Punctuated equilibrium gives a distribution shape (leptokurtic budget change,
  replicated across ~9 countries) and its authors disclaim local predictability. Sabel & Zeitlin, O'Reilly &
  Tushman and Andrews/Pritchett/Woolcock report no denominator at all. Finan/Olken/Pande give narrow,
  well-identified mechanism effects inside specific agencies — the best identification in the batch and the
  wrong object.
- **The wiki has no basis to generalise a number beyond those two populations**, and Q71 records that. What the
  two do license is narrower: wherever a reform's success is measured by the reforming body against criteria it
  also chose, the measured rate exceeds the rate of real change, and both sources supply a mechanism for the
  gap — component selection in one, absent measurement in the other.

**The evidence spread is the finding, and it drove the page design.** This batch runs from ~40 RCTs with
reported effect sizes to a 2007 draft working paper containing the authors' unresolved marginalia. So
`reform-levers` sorts every lever by *kind of evidence* rather than by topic or by confidence:

- **Tier (i), randomised or quasi-experimental** — all of it from Finan/Olken/Pande: recruitment wages
  (+35.2% fill rate, elasticity 2.15), career- vs. mission-framed ads, tax-collector performance pay,
  teacher performance pay (+0.27 SD at two years rising to +0.54 SD at five), government audits (−8pp
  unaccounted expenditure), randomised fixed-salary third-party auditors, community scorecards **with**
  facilitated deliberation (the information-only version found no effect), biometric payment rails.
- **Tier (ii), plausible and case-illustrated only** — windows of opportunity, ex-ante political-economy
  analysis (n=2 plus a 17-operation sample the authors call "not hard evidence"), structural ambidexterity,
  the experimentalist four-step cycle, incremental adjustment as a substitute for disruptive reorganisation
  (one unreplicated citation), reform accountability checklists.
- **Tier (iii), pure prescription** — PDIA's four principles ("not yet tested", authors' own words), "quick
  wins" (**contradicted by their own source's Ghana and Tanzania cases**), better integrity screening (the one
  test shows existing exams would not filter dishonest applicants), and five of NAO's six recommendations.

Two levers were deliberately not smoothed. **The tax-collector result raised revenue growth 46% and raised
bribe rates**, and both halves are reported everywhere it appears; it is also exactly what the source's own
task typology predicts, which is why that typology is now D71. And **teacher performance pay produces opposite
multitasking results in Andhra Pradesh and Kenya** on the same lever — whether multitasking bites is an
empirical question per setting, not a law.

**Register.** D70–D77 added. D70 (personnel selection and recruitment mechanism) closes the first item on the
register's original absent-list, and closes it with randomised variation — Q4 has been "named by nobody", then
"named once, badly", then "measured but with no axis" across four batches. D71 (citizen–state interest
alignment on the task) is the first axis in the register that predicts *which lever is safe where*. D74
(independent-venue count) is registered separately from D44 on purpose: a venue count measures how many places
a challenger can start a change, a veto count how many places an incumbent can stop one, and the same actor
usually appears on both lists. **D77 `rejected`** — "dynamic capability" excludes successful-but-undesigned
adaptation (HP's divisional spinoffs, B.F. Goodrich's wartime pivot) by definition, making it a post-hoc label;
readmission needs an ex-ante instrument for "consciously managed and repeatable" scored before the outcome is
known. That is the fourth rejection in the register for the same reason.

**Selection on the dependent variable is confirmed and self-flagged in three of eight sources**, and Q72
records it as a property of the field rather than a defect of three papers. Sabel & Zeitlin examine zero failed
cases; O'Reilly & Tushman have ~9 successes against 1 thin failure *and* a construct that prunes the cases that
would test it; Andrews/Pritchett/Woolcock hand-pick failures with essentially no successes, which is the same
defect running the other way. Only Finan/Olken/Pande's RCTs and NAO's near-census audit largely escape it —
and those are the same two sources the tier-(i) levers and the base-rate finding come from. True/Jones/
Baumgartner split across their own two evidence layers: the budget distributions are a full unconditional time
series and select on nothing, while the mechanism narrative selects uniformly on successful punctuations. Same
paper, opposite verdicts, which is the cleanest argument in the wiki for tiering per claim rather than per
source.

**Two cross-source connections, both recorded as connections rather than conflicts.**

- **Mechanism-level:** Bunse & Fritz's own 75%-vs-47% gap looks like an instance of exactly what
  Andrews/Pritchett/Woolcock diagnose — measured success tracking form-compliance rather than function. The
  sources are independent and neither tests the other; what the pairing supplies is a quantified version, from
  inside a donor institution, of a gap the diagnosis can otherwise only illustrate. It corroborates the
  diagnosis and supplies nothing to PDIA.
- **Nuance on `incentives-under-multiple-principals`:** Finan/Olken/Pande open with five named reasons state
  personnel economics differs systematically from the private-sector version, which reads kind-graded against
  Dixit's "differences of degree, not kind". Not filed as a conflict — neither source engages the other, two of
  the five are Dixit's own parameters renamed, and their own wage data (>100% premium in the poorest sample
  countries, 4–20% in the richest) is degree-graded.

Thin spots:
- **Nobody tests a reform that had the right design features and failed anyway** (Q70). Without such a case,
  every tier-(ii) and tier-(iii) lever is unfalsifiable — each failure is attributable post hoc to incomplete
  implementation of the recommended design. That is currently the structure of this whole literature.
- **Private-sector renewal evidence in this wiki is one draft working paper built on ~5 recurring firms**
  (Q73). No lever anywhere in the batch has been tested in both a public and a private setting.
- **No age evidence again**, after a fifth literature. D73 is a property of a *decision* — time-to-benefit
  against the authoriser's tenure — not of an institution's elapsed life, and is labelled so on the register to
  stop it being read as one. Andrews et al.'s nearest claim runs the other way: 20 years of repeated reform
  cycles accumulating into nothing, on two cases.
- The batch's strongest source is silent on scale, hierarchy and age by its own admission, and its own
  strongest lever (integrity screening) sits in tier (iii) — which is why the triage is done per lever and not
  per source.

## [2026-08-20] lint remediation | 2026-08-19 report

Acting on `wiki/lint-reports/2026-08-19.md`. Consistency and structure only — no new claims, no new sources.
The report itself was not modified; it stays as found.

**1. Promotion criterion re-applied.** The user's ruling of 2026-08-20 dropped criterion (i) (two independent
naming sources); measurability is now the whole test, and the criterion text at the top of the register was
already updated. All 50 `candidate` rows were walked against it, strictly: a countable, codable or
readable-off-a-document instruction promotes, a gesture at measurement does not. **41 promoted, 7 left
`candidate`, 2 taken out of the running by the merges below.** The seven that stay are D19, D22, D31, D32,
D33, D57 and D64, each for a stated reason recorded in `revisions.md`. The three closest calls:

- **D49 (task substitutability) — promoted.** Its first limb is an experiment an analyst cannot run
  ("introduce or strengthen a measure on one task"), which nearly disqualifies it. Promoted because limbs (ii)
  and (iii) are observational and executable — a reallocation audit off time-use or case-mix records around a
  change in what was measured, and a design read-off from whether the institution has repeatedly split the
  function. One runnable limb is enough; a row whose *only* limb is an intervention would not be.
- **D57 (field structuration) — left.** The closest call against promotion. Its fourth proxy (count the
  field's coordinating bodies and the participation share) is genuinely countable, but the axis is scored on a
  **field**, not on an institution, so it cannot be run against "an institution's primary documents, budget,
  personnel records or observable behaviour" at all — and DiMaggio & Powell concede in the row that
  structuration "may not lend itself to easy measurement". Readmission is cheap: state it as a measurement on
  the field an institution sits in, and say which field data source supplies it.
- **D64 (coordination requirement for capture) — left.** Reads like a count — "count the distinct outside
  actors whose assent or coordinated action is needed" — but the assent is counterfactual and informal, with
  no data source named, where D44's structurally identical instruction is anchored in formal assent
  requirements and voting records. Carpenter & Moss "measure neither pole" by the row's own admission.
  Promotion condition: name where the actor list comes from.

Also close: **D19** (left — the row itself says no method here measures human or site specificity) and **D33**
(left — the executable proxy scores stated rationale, which the row concedes is not the named construct).

**2. Duplicate axes merged.** D51 into D42, D74 into D14, both using the D25/D25a convention — lower number
stays live, higher number stays in place marked `superseded by Dnn` and pointing at the survivor, with the
survivor absorbing everything the superseded row did better. Nothing was deleted; the visible history is the
point, and a `superseded by Dnn` status value was added to "How to read this" so the column stays legible.

The two soft overlaps were **cross-referenced, not merged**, and the reasoning is on the rows:

- **D10 / D44.** D10's bare veto count is exactly what D44's composite exists to prevent, so D44's warning is
  now carried on D10 and must be applied whenever D10 is scored. They are not one axis: D10 counts who can
  block *an expropriative act by the top decision-maker* and asks whether anyone ever has — a behavioural
  check D44 does not have and should import — while D44 counts who must assent to *any* change to the status
  quo. Merging would lose North's narrower act class and D44's preference limb both.
- **D50 / D25.** D50's outcome-observability limb is D25's question restated, so it is now instructed to be
  scored with D25's three-component instrument and D25a's three-way split rather than as a fresh binary. Not
  merged, because D50's value is the *cross* with action-observability, which D25 has no analogue for, and
  because D50 is explicitly scored on a situation rather than an organisation (Dixit's army is procedural in
  peacetime, craft in war). D25 now names the full measurement cluster — D25, D25a, D47, D50 — which closes
  the D50→nothing reference gap the lint found.

**3. The decay conflict is reachable.** `conflicts/decay-as-real-vs-decay-as-overstated` had zero inbound
wiki-links from any content page; it now has ten. Seven `## Related` entries, each stating which position in
the dispute the page sits on and why, plus the three bare backticked paths converted to wiki-links. The
justification clauses are the point: a reader on `goal-displacement` should learn there that Merton is one of
Position B's founders, not merely that a conflict file exists.

**4. `index.md` reframed.** One line, still one line. The triad and the decay premise are now stated as the
working decomposition under test (Q17, Q60) rather than as the wiki's subject.

**5. `open-questions.md` tidied.** Q39–Q45 moved up out of the end-matter and the `institutional-evolution`
raw directory listed in `## Source` with the other six batches; scope clusters cross-referenced in both
directions (Q3 → Q64 / Q73, with Q25 and Q38 as the candidate replacement variables; Q20 ↔ Q61) without
merging anything.

**6. Tier vocabulary.** `[framework]` retired into `[model]` — 39 occurrences across 16 pages — and the
vocabulary stated once in `CLAUDE.md`: three tiers, three markers, lettered form for prose only, no fourth
token. The `[framework]`/`[model]` split the lint described as "genuinely useful but undocumented" was not
preserved; where a tier-(b) source's character matters it belongs in the page's `Evidence tier note.`, which
is where every page already states it in practice.

**Noted, not fixed** (outside this pass's remit): `open-questions.md` Q2 still says the register "registers 34
named axes" against 74 rows; the register's intro paragraph is still an append-log; the lettered tier form
(`**[b]**`, three uses) still coexists with the named form; and `dimensions-of-institutional-variation` still
lists `[[governance-structures]]` twice in its own `## Related`.

## [2026-08-20] ingest | institutions-and-growth (9 sources)

Nine sources on the wiki user's working thesis that institutions determine economic production: Acemoglu,
Johnson & Robinson ×3 (colonial origins, reversal of fortune, the Handbook "fundamental cause" chapter),
Rodrik/Subramanian/Trebbi, Besley & Persson, Wade, and three critics — Glaeser/La Porta/Lopez-de-Silanes/
Shleifer, Albouy, Deaton. Five pages, two conflicts, four register rows, five open questions.

**1. The verdict, in the batch's own four categories.** *Well-evidenced*: the raw correlation between measured
institutional-quality indices and income. Both camps agree; it is not in dispute and no page should imply it
is. *Theorised but unmeasured*: the constraint→investment→growth mechanism itself — AJR's own black box —
Besley & Persson's investment-trap model, which its authors explicitly disclaim as causal, and "embedded
autonomy". *Contested, unresolved*: whether the settler-mortality instrument identifies institutions at all,
and the direction of causality between institutions, growth and human capital. *Evidenced against*: that
corrected settler-mortality data still supports AJR's institutions coefficient (Albouy: it does not), and that
the standard indices measure durable constraint rather than recent policy outcome (Glaeser: they do not).

**2. Albouy is the hardest fact in the batch and is recorded at full precision.** 36 of AJR's 64 mortality
rates originate outside the country they are assigned to; 22 of those trace to two extrapolations — a chain of
French campaign rates from western Mali spread across six countries partly through place-name confusion, and
16 Latin American countries scored from **19 bishop deaths** across three temperature bands, scaled up 4.25×
against a Mexico campaign rate that was never annualised (correctly done, the factor is 1.86). Campaign and
barracks rates are conflated, and the conflation runs *with* the hypothesis: campaign sourcing is
significantly more common in high-expropriation-risk, low-GDP countries, rejected at 2%. With both of Albouy's
corrections applied the first stage is insignificant **even with no controls** and switches sign in three of
eight specifications; under Anderson–Rubin inference the confidence region for the institutions effect is the
entire real line. AJR's "holds without Africa" defence leaves 13 non-conjectured countries driven entirely by
the Neo-Europes. Albouy's own verdict stops at "without a strong empirical foundation" — not "institutions
don't matter" — and the page says so.

**3. Deaton was scoped down, and the correction is stated on the page.** The commissioning brief told the
ingest that Deaton's Keynes Lecture uses AJR as its worked example. It does not. He names AJR **once**, in a
list of six external-but-not-necessarily-exogenous instruments, and never demonstrates a competing channel —
malaria, yellow fever and disease ecology do not appear in the source, and neither does "expropriation". His
worked cases are the aid-growth instruments and Angrist–Lavy's Maimonides rule. **Albouy and Glaeser carry the
technical critique; Deaton supplies the framework (external ≠ exogenous, LATE ≠ ATE, exogeneity untestable)
in which their results are read.** Recorded on the anchor page and on the conflict page so the overstatement
does not propagate.

**4. The affirmative camp is internally split, and the disclaimers are the authors' own.** Rodrik's
over-identification tests **fail** in the 140-country sample (p = 0.0071, 0.0365); he prefers the smaller
just-identified sample rather than answering, titles a section "An instrument does not a theory make", and
states "our findings do not map into a determinate set of policy desiderata". Besley & Persson: "there is no
good reason to believe that these correlations can be interpreted causally", and causation on one of their own
central results "runs from income to market support and taxation, not the other way around". AJR concede the
culture confound unresolved, concede their malaria control is endogenous, concede the first stage collapses
within Africa, and concede their framework is "largely verbal... not fully specified". Wade's fastest-growing
cases score **low** on AJR's own constraint axis. The strong claim that circulates downstream is assembled
from papers whose authors each declined to make it — filed as Q91.

**5. The Rodrik merge decision: kept standalone, dependency stated twice.** The ingest flagged
`institutions-vs-geography-vs-trade-horse-race` as a merge candidate with the anchor, since it shares AJR's
instrument and all of its problems. Kept separate, because it contributes four things the anchor would bury —
the three-way race against geography and trade specifically, the failed over-ID test, the decade-by-decade
first-stage decay (0.94 → 0.87 → 0.71 against rising Polity scores 3.21 → 3.52 → 4.37), and the authors'
unusually explicit self-disclaimer. The risk the merge would have removed — a reader treating it as
independent corroboration — is handled by stating the dependency in the first paragraph and again in a section
that records the decision.

**6. The level-of-analysis finding is this wiki's sharpest instance to date, and is filed as a fork.** Every
one of the nine sources measures "institutions" as a single national scalar. AJR's is a foreign-investor
expropriation-risk score from a private consultancy averaged over a whole polity — and for 36 of 64 countries
the *instrument* for it was collected somewhere else. Wade is the only source that names individual
institutions (MITI, MOF, Taiwan's central bank, ITRI/ERSO, Saemaul Undong) and does so in comparative
narrative; his one quasi-experimental citation, Lane 2017, compares targeted against non-targeted *sectors*,
not one agency against another. **Nothing in this batch supports a causal claim about an individual
institution's effect on production** — only about national institutional environments, contested even there.
Q90 states it as a fork rather than a gap: either the literature has not run the disaggregation (a
research-agenda problem, with the data classes named) or institutional environments are irreducibly national
(in which case the triad is a claim about societies and the wiki's institution-level framework is answering a
different question). No source in the batch takes a position. Q17 annotated accordingly.

**7. Two conflicts filed OPEN.** `does-institutions-growth-survive-identification` — the central one, with a
four-row status table and a two-part settlement criterion (an independently reconstructed mortality series
with transparent provenance, plus a timing/sequencing design; only Glaeser's Table 12 attempts the latter and
it runs against Position A). `constraint-vs-capacity-as-the-investment-mechanism` — the secondary one, and a
direct tension with `credible-commitment`'s existing text rather than a new topic. That page has been
annotated with a contested section: North's mechanism and Libecap's price-ratio measurement left intact, a
third settlement test added (sustained investment under an unconstrained executive), and two candidate
reconciliations recorded as hypotheses rather than adopted.

**8. Register: four rows from nine sources, the worst yield the register has had, for a structural reason.**
D90 (durable-rule vs. outcome/perception measurement validity, Glaeser) `promoted`, with a three-part
diagnostic runnable on a single institution and registered as a **gate** on any row scored from a composite
perception index. D91 (performance-conditionality of institutional support, Wade) `promoted` — the batch's one
clear institution-level axis, with the observed withdrawal base rate as its fourth and load-bearing component.
D93 (leadership-turnover risk, Besley & Persson's γ) `candidate`, with the institution-level form labelled as
this wiki's own untested translation. D94 (embedded autonomy) **`rejected`** — no ex-ante instrument, and
Wade's own Bank of England case shows a high score co-occurring with the opposite outcome; readmission
requires scoring information-density-with-client and disciplining-instances separately, before the outcome is
known. **D92 was reserved and deliberately not used**: the duplicate check the ingest asked for found the axis
already at D7 (Ostrom's locus of rule-making authority — same operationalisation), not at D62 (which is
selection-signal nationalisation and unrelated), so AJR's breadth-of-power-holding-group and Besley &
Persson's θ were folded into D7 with AJR's de jure/de facto warning attached, and the number left unused so
the check stays visible.

**9. Incidental fix, and a residue for the next lint.** `credible-commitment` still carried two `[framework]`
tokens after the 2026-08-20 tier-vocabulary normalisation; they were changed to `[model]` while the page was
open. **The residue is wider than that page.** The normalisation appears to have caught the bare `[framework]`
form and missed the qualified form `[framework — ...]`, which still stands in at least
`multitask-incentive-theory`, `incentives-under-multiple-principals`, `path-dependence-and-increasing-returns`
(×3), `motivation-crowding` (×2) and `gradual-institutional-change` (×4). Not fixed here — outside this
batch's remit and it touches six unrelated pages — but flagged so the next lint pass can sweep for
`\[framework` rather than `\[framework\]`.

---

## [2026-08-20] page | schooling-and-institutional-quality (user-requested, one source)

**Scope.** One new page for the schooling hypothesis — human capital as a cause of institutional quality
rather than a consequence — requested by the user and marked as a subject to expand. Written from the single
already-captured source (Glaeser, La Porta, Lopez-de-Silanes & Shleifer, NBER WP 10568), with the raw file
consulted directly to verify Tables 11 and 12 coefficient by coefficient. No new capture.

**1. Why a separate page rather than a section on the anchor.** The Glaeser material was already split across
two pages from the same batch: [[colonial-origins-and-the-settler-mortality-instrument]] carries the
measurement attack and the mechanics of the instrument re-run, and
[[institutions-vs-geography-vs-trade-horse-race]] carries the collision with Rodrik's channel decomposition.
Both treat Glaeser et al. as a *critique*. Neither states the positive claim as a claim with its own evidence
and its own failure conditions. This page does that and cross-links rather than restating; the measurement
argument appears here only as a premise, in one paragraph, with a pointer.

**2. Three things the raw tables carry that the existing pages do not, all found by reading Table 11 and
Table 12 directly rather than through the summary.**

- **Table 12 Panel A: initial log GDP per capita predicts subsequent five-year schooling growth strongly
  (+0.2839, s.e. 0.0790; +0.3978 in the Polity specification), while predicting no institutional change on any
  of the four measures in Panel B.** The wiki had recorded only the Panel B half. The paper's own sequencing
  table is therefore a three-link chain — income → schooling → institutions — not evidence that human capital
  is the unmoved first mover. The paper's rhetoric skips this link; the page states it and flags that anyone
  using Glaeser et al. for "education is the deep cause" is claiming more than Table 12 supports.
- **Table 11's footer reports the correlation between predicted executive constraints and predicted years of
  schooling at 0.8182 and 0.8163, on N = 47 and 55, and the paper does not discuss it.** A horse race between
  two instrumented regressors collinear at r ≈ 0.82 on fifty-odd observations has little power to attribute
  shared variance. "Schooling wins" is better read as "the instruments cannot separate them" — which is
  actually the authors' own stated conclusion (the instrument is invalid *for institutions specifically*) and
  is weaker than the reading their framing invites.
- **The executive-constraints second-stage coefficient is negative in both columns** (−0.3432 and −0.2965),
  not merely insignificant, and the F-test on the 1500-density specification is 4.70 against 17.23 for settler
  mortality. Wrong-signed point estimates are a symptom of a specification not identifying the thing, and the
  page says so rather than scoring it for the schooling side.

**3. The failing measure is now named.** "3 of 4" appears in the summary and on the anchor page without saying
which one fails. It is the Alvarez autocracy dummy (−0.0958, s.e. 0.0707); the three that work are executive
constraints (+0.4975), Polity autocracy (−0.9092) and democracy (+0.7004).

**4. Mechanism candour, recorded.** Glaeser et al. consider the human-capital-externality reading (Lucas 1988)
and set it aside because Pritchett (2000) finds returns to education in developing countries are not
especially high — then adopt Lipset's political-externality reading ("courts and legislatures replace guns")
as the residual. No violence, stability or dispute-resolution variable enters any regression in the paper. The
mechanism is attached by citation after the timing result, which is the reverse of this wiki's stated
preference, and is flagged on the page as the largest single thing job 17 must fix.

**5. Q94: extended, not duplicated.** Q94 already stated the sequencing claim and the design asymmetry (only
one camp owns a timing test) precisely enough that a second question would have split the evidence across two
rows. It now points at the page and carries the three corrections above, plus the note that **no independent
replication of Table 12 is recorded anywhere in this wiki** — stated as a gap in the wiki's evidence, not as a
fact about the literature.

**6. Thinness stated on the page, not just in the log.** One paper, one team, and the team is a party to the
argument. The page makes the non-independence explicit: the measurement critique clears the ground and the
schooling result occupies it, both from the same authors and the same priors, and accepting the first does not
entail the second — the indices could be bad measures *and* institutions could still be upstream. The
self-citation apparatus (La Porta et al. 1997/1998/1999/2004, Djankov et al. 2003) supplies the interpretive
framework as well as the support, so the *framing* is uncorroborated outside the group.

**7. What was deliberately left out.** No Barro, no Lipset's own empirical descendants, no modernisation
theory, no human-capital-and-democracy literature — all of it known and none of it captured. The expansion
note says explicitly that the absence is a rule being followed rather than a judgement that the literature
does not exist, and hands the retrieval to job 17. Job 17's requirements are stated on the page as
requirements: at least one affirmative-camp sequencing source (ideological balance is a hard gate), any
independent replication of Table 12, the **norms half** the paper invokes and never measures ("human and
social capital", operationalised as years of schooling alone), and sub-national or natural-experiment
evidence. The page is to be **rewritten rather than patched** — its structure is shaped around one paper's
table numbers and will not survive contact with a real literature.

**8. No register row.** A hypothesis about causal direction is not an axis of institutional variation. D90
already carries the measurement axis this paper contributes.

---

## [2026-08-20] ingest | bureaucracy-and-public-choice (7 sources)

**Sources.** Two camps that argue against each other by name. *Public choice / rational actor*: Tullock,
"The Welfare Costs of Tariffs, Monopolies, and Theft" (1967); Downs, "A Theory of Bureaucracy" (RAND P-3031,
1964); Wilson, "The Bureaucracy Problem" (*The Public Interest*, 1967). *Weberian / empirical*: Evans & Rauch
(*ASR*, 1999); Rauch (*AER*, 1995); Besley, Burgess, Khan & Xu (NBER WP 29163, 2021); Guo Xu (NBER WP 35568,
2026).

**1. The Weber gap is stated on every page that needs it, and it is the batch's central negative.** This wiki
holds no text by Weber — the only open copy of "Bureaucracy" is a scanned image with no text layer, OCR failed
and was discarded. Every "Weberian" claim in the batch is therefore a second-hand operationalisation, and the
most-used one says so about itself: Evans & Rauch selected **two** of Weber's characteristics explicitly for
measurability out of a larger set, and their footnote 7 names the one they deliberately excluded —
rule-governed decision-making and bounded jurisdictions — because it is "a double-edged sword… producing
rigidity and organizational sclerosis when carried further." That is the authors of the Weberianness Scale
bracketing out the Merton critique in their own text. The gap is stated on `weberian-structure-and-growth`
(opening section, before any result), on `civil-service-tenure-and-political-insulation`, on
`organizational-economics-of-the-state`, on `rational-actor-accounts-of-bureaucratic-behaviour`, and as
**Q103**. No page reconstructs Weber from any source's characterisation of him.

**2. The D50 provenance correction.** The wiki's D50 (action-observability × outcome-observability) was
attributed "Dixit, after Wilson (1989)". This batch supplies a Wilson primary text — the 1967 essay — and it
contains **no version of that typology and no action × outcome framework at all**. The typology is from the
1989 book, which this wiki does not hold. **The row was not deleted**: the axis is measurable and useful, and
it stands. What changed is the Named-by cell, which now states that the axis is held **second-hand via Dixit
alone**, that the primary Wilson text the wiki does have is confirmed not to contain it, and that the wiki
therefore has no way to check Dixit's rendering — including Dixit's own footnoted warning that Wilson uses
"output" for what economists call action. The same correction is carried on
`incentives-under-multiple-principals`, where the typology lives, and Wilson (1989) is recorded as an
acquisition target alongside Weber in the register's gap note and in Q103.

**3. Rauch's placement — decided, and it was close.** Rauch (1995) is a personnel mechanism (merit exam +
just-cause tenure) tested via a growth outcome, so it could have extended `personnel-economics-of-the-state`
or anchored `weberian-structure-and-growth`. **Anchored on the Weberian page**, for three reasons stated on
the page itself: he co-authors Evans & Rauch and frames the 1995 paper against the same Evans (1992)
Weberianism measures, so the two are one research programme; the *contrast between their methods* — a
correlational cross-section with disclosed regional-dummy fragility, and a within-country natural experiment
with a control-group reform, agreeing — is itself the finding and only exists if they share a page; and the
unit of analysis differs from the personnel page's, which is built on micro-level randomised evidence with
individual- or facility-level outcomes, where Rauch's outcome is a municipal budget share. The personnel page
carries a cross-reference and a one-line summary of the result, not a duplicate.

**4. The personnel de-duplication, run before anything was added.** Besley et al. treat Finan/Olken/Pande as
their base for this territory and restate their headline verbatim. **Six studies overlap** and are not
restated on the page: Dal Bó/Finan/Rossi recruitment wages, Ashraf & Bandiera ad framing, Khan/Khwaja/Olken
Punjab tax collectors, Muralidharan & Sundararaman teacher pay, Glewwe/Ilias/Kremer's contrary Kenyan result,
and Iyer & Mani on caste-affinity postings — on all six the later source cites the design and does not restate
effect sizes, so it adds citation weight and no numbers. Two more differ in identity but not in kind
(Ashraf/Bandiera/Jack alongside the page's Rwanda evidence; Duflo/Hanna/Ryan alongside its nurse study).
**What was genuinely new clusters in three places** and is what the extension carries: selection under rules
vs. discretion with a non-uniform sign (Colonnelli/Prem/Teso and Xu 2018 negative; Weaver 2021 and Voth & Xu
2020 positive; Hoffman/Kahn/Li as the authors' own private-sector parallel); the stated evidence gap on entry
exams, including Moreira & Pérez's null on the Pendleton Act's effect on customs performance; and careers,
autonomy and non-monetary levers (performance-based postings, autonomy with a monitor-dependent sign,
seniority rules' priced downside, mission-framing spillover, random auditor assignment). Plus the
embeddedness/rotation tension, four studies each way, which became D104.

**5. The age point, handled so it cannot read as progress.** Downs's C.11 is the **first source in this
project to assert an age-dependent decay mechanism at organisational level** — six prior batches found none,
and three founders of the decay literature disowned the age reading of their own mechanisms unprompted. It is
**bare assertion**: the document contains no data anywhere, C.11 has no derivation from the paper's own axioms
and no stated mechanism beyond the sequence, and no falsification condition. Filed as
`conflicts/downs-vs-merton-on-age-dependence.md`, explicitly as a **conflict of two models, not of evidence**,
with that stated in the first line of the file, in the index row, on both content pages and in **Q100**, whose
last line is "Do not report this row as progress." **No register row was added for age**, and the gap note now
records why: the clock was never the missing piece, the directly observed accumulation variable is, and Downs
supplies that no more than anyone else. The one usable contribution is that C.11 makes five *pre-specified*
directional predictions against Merton's flat line, at least three countable from an agency's own records —
which gives Q60's design its hypotheses in advance for the first time.

**6. Register.** D100 progression-margin protection (`candidate`), with a stated four-component
operationalisation and an explicit account of how it differs from D70 — D70 is the entry gate and measures who
applies and who is hired; D100 is what happens to someone already in post, and the Pendleton Act evidence
shows the two come apart. D101 selection trait, horizontal vs. vertical (`candidate`), with a warning against
collapsing it into D70's screening-technology component, since discretionary instruments sometimes produce
vertical selection. D102 content vs. fact of institutional reform (`candidate`), the register's first row that
is a comparison design rather than an attribute, built on Rauch's commission-government control and its
opposite-signed coefficient. **D103 `rejected`** — Wilson's multi-criterion observability axis, subsumed by
D25/D50/D51 scored together, with a readmission condition requiring a source showing it predicts something
those three do not. D104 personnel embeddedness (`candidate`), **with the both-ways finding inside the row**,
because an axis whose own naming source reports four studies each way is measurable without being predictive;
three candidate moderators are named as this wiki's inference, none tested.

**7. Open questions.** Q100 (the age claim as theory, and what it does not change); Q101 (which component of
the Weberian bundle does the work — never decomposed by scale item, and the one decomposition that exists
points at tenure rather than exams); Q102 (whether any of this extrapolates to already-highly-protected
systems, which the source says it does not); Q103 (the two missing primary texts); Q104 (whether any credible
systems-level evidence exists — the same shape as Q90 from the other direction, a field with evidence at top
and bottom and none in the middle); Q105 (what moderator predicts the sign of embeddedness). Q3, Q4, Q7 and
Q60 annotated rather than duplicated. Q95–Q99 left unused; the numbering note records it.

**8. What was deliberately not imported.** Niskanen's *Bureaucracy and Representative Government* (1971) and
Wilson's *Bureaucracy* (1989) are both known and neither is held; nothing on any page draws on them. The
1968 Niskanen paper the wiki does hold is cited only for what is already on
`bureaucratic-growth-and-parkinsons-law`. Krueger (1974) is named only as the coiner of "rent-seeking", which
is a fact stated in the Tullock summary, not a claim from her paper.

## [2026-08-20] ingest | theory-of-the-firm (8 sources)

**Sources.** Alchian & Demsetz 1972 (team production); Jensen & Meckling 1976 (agency costs); Fama 1980
(separation of ownership and control); Chandler 1992 JEP (organizational capabilities, M-form); Aghion &
Tirole 1997 (formal and real authority); Gibbons 2004 (four formalizable theories); Gompers, Ishii & Metrick
2001 (governance index); Bloom, Sadun & Van Reenen 2016 (World Management Survey). Scoped deliberately to the
**internal organisation of the firm** — decision rights, monitoring, ownership structure, management practice
— and away from the firm-boundary question the wiki already covers on `governance-structures` and
`property-rights-theory-of-the-firm`.

**1. Evidence character of the batch.** Five sources are `[model]` with no data of their own (Alchian &
Demsetz, Jensen & Meckling, Fama, Aghion & Tirole, Gibbons), and four of the five say so in their own text.
One (Chandler) is **compressed historical synthesis one remove from its archive** — his own 1992 condensation
of *The Visible Hand* and *Scale and Scope*, neither of which this wiki holds — and it supplies no coding
scheme, no ranking criterion and no restated caveats. **Two are `[empirical]`, and they are why this batch
mattered**: Gompers/Ishii/Metrick and Bloom/Sadun/Van Reenen are the first instruments in this wiki that
measure **individual organisations** rather than countries, and both are scoreable tomorrow by one competent
person.

**2. Eight new pages.** `team-production-and-monitoring`; `agency-costs-and-ownership-structure`;
`separation-of-ownership-and-control`; `organizational-capabilities-and-the-m-form`;
`formal-and-real-authority`; `decision-rights-and-authority-theory-of-the-firm`;
`corporate-governance-index-and-firm-control-rights`; `world-management-survey`.

**3. A correction to the wiki's own commissioning brief, made on the page rather than in chat.** The brief
stated that Fama (1980) contains the initiation / ratification / implementation / monitoring decomposition of
decision rights. **It does not** — the ingest checked the text and neither "ratification" nor "initiation"
occurs in it. That taxonomy is Fama & Jensen (1983), which this wiki has **not** captured. The correction is
stated as its own section at the top of `separation-of-ownership-and-control`, the taxonomy was **deliberately
not written into any page from memory** (it is well known, which is exactly why importing it would be
undetectable), Fama & Jensen (1983) was added to the acquisition list at Q103 alongside Weber's *Bureaucracy*
and Wilson's *Bureaucracy* (1989), and a dedicated row records what the absence costs at Q113.

**4. The measurement section, which is the reason this job was run.** Five register rows, D110–D114, in a new
block whose note states what the block is for. **D110** management-insulation / control-rights allocation
(`promoted`) — an additive 0–24 count of charter, bylaw and state-law provisions shifting control from
shareholders to management, **scoreable tomorrow from documents alone by one analyst**, with the limit stated
inside the row: generalising beyond US public companies requires **first building an equivalent settled
taxonomy of control-shifting provisions** for another jurisdiction or entity type, a step neither this source
nor any other in the batch attempts. **D111** management-practice quality (`promoted`) — 18 practices, 1–5,
double-blind interview, **scoreable tomorrow given a trained interviewer and one honest correctly-placed
respondent**, works on private firms by construction (90% of the sample) and untested-but-plausibly on public
bureaus, failing on scripted answers or an unreachable respondent rather than on a decoupled document.
**D112** formal/real authority gap (`candidate`, **not scoreable**) — Aghion & Tirole only *propose*
instruments (overrule counts with their own self-censorship caveat, "who gets courted", liability doctrine),
and the row records what would have to be built. **D113** residual-claim capitalizability (`candidate`,
document-scoreable). **D114** separability of production (`candidate`, **not** document-scoreable in the same
way — it classifies a production technology, and the row says so). **D90 was wired in as a gate on D110 and
D111**, with the extension noting that the gate bites differently on each: D110 passes (i) and (ii) trivially
and lives or dies on (iii), decoupling; D111 is a behaviour measure by construction and (i) and (ii) bind.

**5. The 77% finding, recorded at Q90 rather than only on its own page.** Bloom et al. decompose management
variation as 13% country, 10% industry, **77% within country-and-industry**. The wiki has repeatedly found
that country-level measures cannot support institution-level claims and posed it at Q90 as a fork —
a property of the *literature*, or a property of the *object*. This is the first evidence that question has
had, and it supports the first limb for at least one measurable dimension. Recorded with two limits attached:
management practice is not the same object as the shared legal and coercive order the second limb is about,
and [[organizational-economics-of-the-state]]'s 73% country-fixed-effects "Weberian Fact" points the opposite
way on a different instrument and a different object. The honest reading recorded is that **how much of
institutional quality is national depends on what is being scored**, which makes running two instruments on
one set of organisations the cheapest available progress.

**6. Conflicts.** `rival-firm-boundary-theories` extended from three positions to four: **adaptation/authority**
added as Position D (requires zero specific investment), with Gibbons's headline that the four are **formally
orthogonal, not nested** — refuting the folk claim that Grossman-Hart formalised Williamson, which Gibbons
calls "just plain wrong" — his candidate discriminating test (only the margins matter, for the property-rights
theory) recorded **together with his own flag that the margins are unobservable and the test likely
untestable**, and his own view that a horse race may be the wrong frame. **Masten-Meehan-Snyder** filed there
too: the asset-specificity→integration regression cannot identify causal direction, generalised by Gibbons to
all four theories. **Chandler vs. Williamson** filed as a sub-dispute on whether backward integration at Pabst,
Singer, McCormick and Ford were "mistakes" — with the wiki's own note that the disagreement is about the
benchmark and is in principle decidable from business-historical evidence neither source supplies here.
**Aghion-Tirole's optimal-overload-as-commitment vs. overload-as-bloat recorded as a framing tension on both
pages and deliberately not filed** — no shared measured quantity exists for the two sides to disagree about.

**7. Two false conflicts explicitly not filed, and the terminology notes written instead.** (i) Alchian &
Demsetz's "residual **claimant**" (title to earnings) vs. Grossman-Hart's "residual **control rights**" (the
right to decide an asset's unspecified uses). (ii) Fama's "ownership of the firm is an irrelevant concept"
(the residual financial claim, inside a constituted firm) vs. Grossman-Hart's "ownership is control" (a
physical asset, across a boundary). Different objects, same words, in both cases. Short terminology sections
written on `team-production-and-monitoring`, `separation-of-ownership-and-control` and — where a reader is
most likely to hit the collision — `property-rights-theory-of-the-firm`.

**8. Existing pages extended.** `governance-structures` (Gibbons's two-theories provenance finding with the
1975/1985 index-count evidence; the generalised identification critique; the WMS technology-vs-design contrast
marked soft and partial; the Chandler pointer). `property-rights-theory-of-the-firm` ("drone employees", the
refined aO/aN/aC and dP/dN/dA taxonomy, both terminology traps). `multitask-incentive-theory` (the
employee-vs-contractor derivation as a third formal route to low-powered incentives; the influence-cost model
now derived rather than asserted). `bureaucratic-growth-and-parkinsons-law` (the overload framing tension and
the null hypothesis it imposes on any bloat diagnostic). **Retired `[framework]` tokens normalised to
`[model]` on every page touched** — 4 on `property-rights-theory-of-the-firm`, 2 on
`multitask-incentive-theory`, 4 on `governance-structures`.

**9. Open questions.** Q110 (can the G-index logic be rebuilt for another entity type, and what does building
the prior taxonomy cost); Q111 (does capability formation operate in non-firm bureaucracies — asked because
Chandler claims it once, in three sentences, with no evidence, against his own capital-intensity scope
restriction); Q112 (an age mechanism running the *opposite* way — accumulated principal experience centralising
authority — recorded for its direction, not as evidence); Q113 (the Fama & Jensen 1983 gap and what it costs);
Q114 (**the batch's central negative: better measurement did not buy identification**, and the authors of the
better instrument say so); Q115 (does the WMS instrument work on a public bureau, and what would it score —
with the validity trap that a bureau may score low on exactly the items where low is the correct design).
Q106–Q109 left unused; the numbering note records it.

**10. What was deliberately not imported.** The Fama-Jensen (1983) taxonomy (see 3). Williamson's books, which
the wiki does not hold and which Gibbons's index-count evidence is *about* rather than *from*. Chandler's *The
Visible Hand* and *Scale and Scope*, both named on the page as unread with the consequence stated. The later
WMS decentralisation instrument, which other Bloom/Sadun/Van Reenen papers reportedly field and which this
source does not document — flagged on the page so it is not attributed here. Chong et al. (2014) on WMS scores
in government services is named as **an appeal to an unread external paper, not evidence in this source**.

## [2026-08-21] ingest | measuring-institutions (PARTIAL — interrupted)

Five pages written: measurement-validity-framework, governance-indicators-and-their-construction,
v-dem-measurement-model, critiques-of-governance-indicators, worldwide-bureaucracy-indicators. All five are
structurally complete (title, summary, body, Source, Related).

**The page-writing pass was interrupted by a planned machine reboot before finishing its bookkeeping.**
Index rows were added by hand afterwards. Outstanding work is listed in `STATE.md` at the repo root.

---

## 2026-08-21 — ingest: `measuring-institutions` (7 sources)

**Sources.** Kaufmann & Kraay, *The Worldwide Governance Indicators: Methodology and 2024 Update* (World Bank,
2024); Pemstein, Marquardt, Tzelgov, Wang, Medzihorsky et al., *The V-Dem Measurement Model* (V-Dem WP 21,
2026); Munck & Verkuilen, "Conceptualizing and Measuring Democracy" (*CPS* 35(1), 2002); Arndt & Oman, *Uses
and Abuses of Governance Indicators* (OECD Development Centre, 2006); the *WWBI Codebook v3.0* (2022) and the
*WWBI Methodology, Insights and Applications* report (2021); the *QoG Standard Dataset 2021 Codebook*.

**1. The finding the job exists to record. The data does not transfer; some of the method does.** Every
substantive score in this batch is a national aggregate, and all seven source summaries confirm it
independently — this is not one summary's inference read across the others. WGI is six country-year scalars
over 214 economies with no sub-national product proposed anywhere in its own methodology paper. V-Dem is
country-year in every worked example, including for indicators substantively about a specific body. QoG is a
~2,000-variable compilation of ~110 sources in which not one sampled variable family scores below the
nation-state. WWBI comes closest and still stops at country × sector × occupation — **there is no agency or
ministry identifier variable anywhere in its schema**, and the codebook's own ISIC note fixes the boundary:
the classification tracks what kind of work a person does, not which institution employs them. **Nothing in
the batch operationalises a single institution.**

**2. The mechanism of the loss is now explicit, and it is the batch's real contribution.** V-Dem's coder
instructions — reproduced verbatim in the QoG codebook across several public-sector-corruption items — tell
expert coders to average out any perceived discrepancy "between branches of the public sector, between the
national/federal and subnational/state level, or between the core bureaucracy and employees working with
public service delivery" **before answering**. Job 9 established that **77% of management-quality variation
sits within country-and-industry**. Put together: **the dominant instruments are structurally built to discard
exactly the variation that carries most of the signal, at the point of data generation rather than in
aggregation** — so it is unrecoverable by any downstream reprocessing of published scores, component data or
raw source series. **This is not a criticism of V-Dem.** For characterising a national regime, instructing
coders to give one national answer removes a genuine source of rater-specific noise and is the correct choice.
It is decisive for this wiki's purposes and is recorded prominently at Q90, where it sharpens limb (i) of the
fork (a property of the *literature*) and removes the best remaining argument for limb (ii) — that everyone
who tries ends up at the country level. They end up there because they are instructed to. **The agenda
consequence: institution-level measurement has to be collected, not derived.**

**3. Five pages.** `measurement-validity-framework` is the **batch anchor** — Munck & Verkuilen's three-stage
diagnostic with its twelve named failure modes, explicitly separated into level-agnostic method (transfers)
and country-level content (does not), plus a run of the checklist against the wiki's own four instruments
whose shared weak point turns out to be the aggregation stage. `governance-indicators-and-their-construction`
carries the UCM in full, the inverse-variance weighting, the reported margin of error, the written
perception-exclusive inclusion criterion, and the precision numbers **in the page summary rather than a
footnote** because downstream use routinely ignores them: 61% of pairwise comparisons and 0.2%/3%/7%/13% of
one-/five-/ten-/27-year changes clear the instrument's own 90% intervals. `v-dem-measurement-model` carries
the IRT/DIF apparatus, the unusually candid self-documented failure modes (the vague-prior shrinkage artefact;
dynamic smoothing priors that pulled Holocaust-era Germany upward and produced "death spirals"), and the coder
instruction. `critiques-of-governance-indicators` carries the eight misuse modes, the correlated-error result
(0.5 assumed correlation doubles WGI's Rule of Law standard error, 0.33 → 0.66), the 0.39-against-0.01
weighting asymmetry, and the re-estimation reversing Kaufmann & Kraay. `worldwide-bureaucracy-indicators`
merges the codebook and the methodology report, as both summaries independently proposed.

**4. The Arndt & Oman merge decision: declined, with reasons on the page.** The ingest flagged it as a merge
candidate with Munck & Verkuilen. Kept separate for three reasons, in order of weight. **They audit different
objects** — one grades an index's *construction*, the other its *consumption*, and six of the eight misuse
modes are properties of a use with no home in the three-stage framework. **Only one transfers below the
nation-state**, and merging would blur the batch's single portable artifact with a catalogue welded to country
indices and their external-user ecosystem. **The original econometrics would be buried** — the re-estimation
is the source's hardest contribution. The three points where the taxonomies genuinely overlap
(ordinal-as-cardinal ≈ failure mode 8; aggregation opacity ≈ 11 and 12; lack of transparency ≈ 9) are mapped
explicitly on the page so the redundancy is visible rather than duplicated.

**5. QoG gets no standalone page.** It is a compilation of ~110 other sources with no primary collection of
its own, and was **sampled at only 3–5%** of its ~2,000 variable entries. Used as provenance material on three
pages, with **the sampling rate stated at every citation**. Its most valuable content is second-hand: the
verbatim V-Dem coder instruction, and WGI's own caveat that annual re-standardisation makes its scores "not
directly suitable for over-time comparisons within countries".

**6. Register: D120–D123, two of them `rejected`, and recording the rejections is the point.** **D120**
(`candidate`) turns Munck & Verkuilen's audit on an institution's **own internal KPI/scorecard system** — five
components, document-based, institution-scoreable, measuring not how the institution performs but whether it
can tell. **D121** (`candidate`) turns Arndt & Oman's gaming warning into a two-step test: find whether
funding, eligibility or classification is gated by a bright-line threshold on an external published index,
then test the institution's own reported metrics for a discontinuity at it. It has a clean null, which makes
it falsifiable per institution. **D122** (`rejected`) — V-Dem/WGI/QoG country scores, with three sufficient
reasons and a stated readmission condition. **D123** (`rejected`) — WWBI sector/occupation aggregates, with
the exact stopping point and the missing schema field named. **The rejected rows document that the field's
flagship instruments are inadmissible here and why, so the question is not re-opened every batch.**
D115–D119 left unused.

**7. D90 extended, in both directions.** **(a)** WGI's perception-exclusivity is **written policy**, not
inference — inclusion criterion #1, with objective/de jure data acknowledged as useful and categorically
excluded, partly because it can be gamed. That is the strongest version of D90's claim anywhere in the wiki
and it comes from the instrument's own authors rather than from a critic. **(b)** A complication that cuts the
other way and had to go on the row rather than be filed elsewhere: Munck & Verkuilen argue the
objective/subjective dichotomy is **itself overstated**, because an indicator is never a neutral record — the
record-generating process has its own drivers. Applied here, **what drives an institution to *write down* a
rule as against follow it is its own bias channel**, so a document-scored measure is not automatically the
sound side. Consequence recorded: the three limbs stand, but limb (iii) is no longer a check of the perception
measure against the document *as criterion* — it is a check of the two against each other with neither
privileged. **(c)** A third distinction the axis was collapsing: WWBI's "objective, micro-level data"
self-positioning is half-earned, since 155 of 192 indicators are household self-report; "not expert
perception" and "documentary" are different things with different residual error classes.

**8. The transferable methods, stated concretely because they are the job's practical yield.** (i) **WGI's
inverse-variance precision weighting with a formally propagated, reported margin of error** — reusable if any
register axis is ever built from several partial proxies, with two conditions on the page: you need per-source
error variances, which WGI gets from a 214-country sample an institution-level analyst does not have, and the
independence assumption must be defended, since proxies drawn from one document set or one set of informants
are almost certainly correlated. (ii) **V-Dem's DIF / anchoring-vignette / bridge-coder technique**, directly
applicable to **D111** if the wiki ever fields multiple coders on one institution — with the identification
problem stated: bridging needs cross-unit overlap, and on a single unit "this coder is strict" and "this
institution is bad" are the same observation, so **anchoring vignettes are the only component that works on
one institution**. (iii) **Munck & Verkuilen's three-stage checklist**, runnable on any register row, now
registered as D120. (iv) **Arndt & Oman's bright-line-gaming warning**, now with a concrete mechanism — a
published index plus a threshold plus money on the other side — registered as D121, and independently named
from the other side by WGI's own authors as their reason for excluding de jure data.

**9. Conflicts. No hard contradiction of an existing wiki claim was found, and none was manufactured.** One
thing logged: on `does-institutions-growth-survive-identification`, **Arndt & Oman's re-estimation reverses
the sign on income → governance in Kaufmann & Kraay's own model** — same two-equation structure, same
settler-mortality instrument family, more controls, four alternative instruments for GDP. Filed **inside
"Position A is internally split"** rather than as a new position, because that is what it is: an internal
reversal within the affirmative camp's own toolkit. Recorded with its limits — it is the system's second
equation rather than the AJR claim, and the authors explicitly do not claim to have settled the direction.
Two other tensions were **deliberately not filed as conflicts**: WWBI's wage premiums showing no correlation
with WGI Government Effectiveness (neither makes a precise claim the other contradicts — recorded at Q123),
and the WMS/Weberian-Facts 13%-against-73% country-share pair, already on Q90.

**10. What the critiques established, and what remains unaddressed.** Recorded at Q122 because it is the
wiki's clearest instance of a measurement critique landing. **Won**: WGI/WBI began **disclosing per-source
scores in 2006**, credited by the critics themselves, and now **reports margins of error prominently** — both
on the critics' minimum-transparency list, and the field's clearest self-correction in this wiki.
**Unaddressed**: circularity in perception-built sub-indicators (Regulatory Quality is still perceived ability
to promote private-sector development, still built from business perception); bright-line eligibility misuse
downstream (publishing an interval does not stop a threshold rule using the point estimate, and no producer
controls the use); reweighting toward population over expert/business perception (named as a "should",
implemented by nobody — still 24 expert assessments to 11 surveys, and the ~0.01 weights unchanged); and
correlated measurement error, now *tested* with the authors conceding the test is "suggestive, not conclusive"
while the aggregation still assumes independence.

**11. Questions.** Q120 (does any institution's own scorecard survive a construction audit — with the base
rate that only 2 of 9 published indices reported a reliability test at all); Q121 (multi-coder DIF on one
institution, and the identification problem that makes vignettes the only usable component); Q122 (what the
critique won and what it did not, and the regularity that what got fixed is what cost the producer nothing);
Q123 (two state-capacity instruments that do not correlate); Q124 (a capture gap — the unread Comparative
Constitutions Project and Global Integrity de jure/de facto families). Q116–Q119 left unused.

**12. Thin spots, stated so they are not mistaken for findings.** The **QoG codebook was sampled at 3–5%**,
and the two most promising families in it went unread as full variable entries: the **Comparative
Constitutions Project** (`ccp_*`, binary presence of named institution-types coded from constitutional text —
**the batch's most promising unexplored lead for document-based coding**, though still one flag per country),
and **Global Integrity's Africa Integrity Indicators** (paired "Law: X is guaranteed" / "Practice: X is
guaranteed" items — the closest thing in the batch to D100(iv)'s coverage-against-exercise component).
Anything the wiki attributes to either is inferred from the codebook's table of contents and category
listings, not from a full read, and every page saying so. Both are acquisition targets alongside Q103's list.
Also thin: **the WGI extraction contains one internally inconsistent sentence** about the source counts behind
the significance-share gap between indicators ("23 vs 10" against surrounding "smaller… versus" phrasing),
flagged in the summary as a possible OCR artefact and **not resolved or carried onto the page**. And **no
source in the batch contains an institutional-age variable of any kind** — ninth consecutive batch; WWBI's
schema structurally forecloses the question, since no given institution exists in it.

## [2026-08-21] ingest | organisational-ecology (job 13, 5 sources)

**Why this job was highest priority.** Five prior batches (scale-effects, institutional-evolution,
institutional-stagnation, bureaucracy-and-public-choice, and the register's own gap-note) searched for
institution-level organisational-age evidence and found none — every duration variable they turned up attached
to a career, a legal regime, or a national polity, never to a single institution's own tenure. All five were
institutional-economics, political-science or public-administration literatures. This job went to organisational
sociology instead, the field that actually treats organisational age as an independent variable.

**1. The result.** Yang & Aldrich (2016) supply the wiki's first true-panel organisation-age mortality evidence:
a Cox hazard model on PSED II (1,030 US ventures, tracked monthly from actual founding, not registration) shows
failure hazard declining **monotonically from 0.031 to 0.015 over 40 months** — confirming liability-of-newness
over the rival liability-of-adolescence hypothesis in this sample, and comparing unfavourably (0.026 vs.
Brüderl & Schüssler's 0.018 peak) against a registration-based study, evidence that registration-based age
studies understate early-life mortality risk by construction. The paper decomposes the decline into a measured
mechanism: post-founding routine/boundary-building activity (business plan, ownership agreement, professional
retention, registration), not calendar time itself.

**2. The theory behind it.** Hannan & Freeman (1984) formally derive the same declining-hazard shape from a
different mechanism — reliability/accountability requirements select for reproducible structure, reproducibility
rises with age, so does inertia, so mortality falls (Theorem 3) — and add a mechanism this wiki had not held:
reorganisation can reset an organisation's effective age for mortality purposes (a Makeham hazard formalisation,
Assumption 8), with a stated, unrun, internal-vs-external falsification test. This is the first source naming
charter-level reconstitution as the natural age-mortality control [[open-questions]] Q60 calls for.

**3. Two complications, both load-bearing.** Coad et al. (2018, special-issue editorial) show age effects are
front-loaded (concentrated years 0–7) and non-monotonic across a full lifespan, with a distinct late-life
"liability of obsolescence" running the opposite direction from early "liability of newness" — not one smooth
curve. Searing (2020, n=8 qualitative) shows organisational "death" is frequently not the clean binary event
hazard models assume — most non-survivors in her sample were Zombie (formally alive, functionally defunct),
Reincarnated or Resurrected, not cleanly Dead.

**4. What this does and does not settle.** [[open-questions]] Q7's age limb moves `open` → `partial`. Q60 stays
`open`, but on narrower grounds: its specified design (true panel, true founding date, a directly observed
accumulation variable) has now been run and gives a clean result, but on entrepreneurial ventures in their
first 40 months, not the mature bureaucracies Downs's C.11 and Q60's own framing are about, and without the
regime-vintage/principal-polarisation controls Q60 requires (inapplicable to private ventures). **Do not cite
this batch as settling anything about decay in mature institutions** — it establishes the design is runnable
and gives a genuine early-life result, nothing more.

**5. Register.** D124 (age-dependent mortality hazard, flagged explicitly as population-level rather than a
per-institution score, unlike D110–D114/D120–D121), D125 (routine/boundary-formation intensity — scoreable
tomorrow on one institution's own records, the batch's most portable row), D126 (reconstitution as an age-reset
event, named but untested). All three `candidate`.

**6. A flagged non-conflict.** Yang & Aldrich's routine-building activities *reduce* failure risk early in an
organisation's life; Downs's C.11 predicts rule accumulation *degrades* a mature bureaucracy over the long run.
Not a contradiction — different life stages, different outcome variables — stated on the page so no later page
conflates them.

**7. Capture.** Two candidates failed on retry and are not held: Thornhill & Amit (the age-stratified failure
dataset the job most wanted — `repository.upenn.edu` returns a JSON redirect pointer on every path) and Le Mens
(the disconfirming/obsolescence source — persistent 503 from a Wayback host). Both recorded in
`capture-manifests.md` and `STATE.md`'s manual-acquisition list.

**8. Five pages written**: [[population-ecology-of-organisations]], [[structural-inertia-and-age-dependent-mortality]],
[[liability-of-newness-empirical-hazard-evidence]], [[firm-age-and-performance]], [[organisational-demise-as-a-construct]].

## [2026-08-21] ingest | power-and-accountability (job 11, 7 sources)

**The power leg of the power/institutions/economy triad.** Seven sources: Tsebelis (veto players), Acemoglu &
Robinson (persistence of power / captured democracy), La Porta, Lopez-de-Silanes & Shleifer (corporate
ownership around the world), Gilens & Page (whose preferences predict US policy), Bashir (a methodological
rebuttal of Gilens & Page, captured for ideological balance), Bueno de Mesquita et al. (selectorate theory),
and Michels (iron law of oligarchy). Mills's *Power Elite* and a second Gilens-Page rebuttal (Enns) both
failed capture and are not held — see `capture-manifests.md`.

**1. Veto players, now with data.** [[dimensions-of-institutional-variation]] D44 (Hammond's veto-point
composite) was a theorem with no empirical content. Tsebelis's independent ~15-year testing program
corroborates the same composite claim across Doering, Franzese, Henisz, Hallerberg & Basinger and Keefer &
Stasavage, and adds two new results: a qualified-majority cohesion inversion, and the **absorption rule** —
a formal vetoholder whose position sits inside the others' unanimity core is functionally irrelevant —
registered as D127.

**2. De jure vs. de facto power, formalised.** Acemoglu & Robinson's captured-democracy result (a durable
democracy can see its elite capture economic institutions *more* often than under nondemocracy, because
regime durability gives the elite an added motive to invest in de facto power) extends D7 rather than
duplicating it, and bears directly on the existing [[constraint-vs-capacity-as-the-investment-mechanism]]
conflict.

**3. Two new document-scoreable, institution-level instruments.** D128 (La Porta et al.'s ultimate-ownership
control-chain tracing, the register's second instrument in the D110 mould) and D130 (Gilens & Page's
whose-preferences-predict-outcomes regression, a method turned into an instrument like D120/D121) — D130
carries Bashir's caveat that the exact design (linear regression on a binary outcome, high predictor
collinearity) can manufacture a spurious null.

**4. Selectorate theory (D129).** The W/S ratio is the wiki's cleanest single-number candidate for "how
broad-based vs. narrow-and-capturable is this institution's accountability structure," flagged explicitly as
tested only at regime level via Polity proxies — extension to boards, bureaucracies or parties is this
wiki's own untested inference.

**5. A new conflict, not filed lightly.** [[iron-law-of-oligarchy]] (Michels) predicts even the most
participatory, anti-oligarchic organisations concentrate power in a leadership stratum over time. Ostrom's
design principles (already in the wiki, [[polycentric-governance]]) are empirically supported for commons
*survival* across 91 studies. Not a strict contradiction — survival and internal power concentration are
different measured quantities, and no source here tests the latter inside a long-running, design-principle-
compliant institution. Filed at [[iron-law-vs-design-principles]].

**6. Seven pages written**: [[veto-players-and-policy-stability]], [[de-jure-vs-de-facto-power-and-captured-democracy]],
[[corporate-ownership-and-control-around-the-world]], [[whose-preferences-predict-policy-gilens-page]],
[[oligarchy-result-methodological-critique]], [[selectorate-theory-and-the-winning-coalition]], [[iron-law-of-oligarchy]].

## [2026-08-21] ingest | comparative-governing-philosophies (job 14, 7 sources)

**The first batch commissioned to test directly whether this wiki's register is universal or an
Anglosphere artefact.** Seven sources: Kettunen (Nordic), Brødsgaard & Beck (Chinese cadre rotation), Xu
(regionally decentralized authoritarianism), Low (Singapore's Administrative Service), Colignon & Usui
(Japan's amakudari), Han/KDI (Korea's Economic Planning Board), Bouckaert (the Neo-Weberian State,
explicitly comparative). Eucken (German ordoliberalism) failed capture on retry — the same misleading
weasyprint error recorded in `STATE.md` — and is not held.

**Verdict: mixed, not clean.** Some vocabulary travels — Xu explicitly models China's RDA as an M-form
organisation, citing Chandler and Williamson by name, which is evidence the *lens* generalises (a Western
economist chose to apply it) more than evidence the underlying institutional logic is identical everywhere.
Three genuinely new mechanisms surfaced that no prior batch had named, registered as D131 (personnel-control
tournament substituting for market/electoral accountability — Xu's condition A gives it a checkable design
criterion), D132 (institutionalised, ministry-organised capture pipeline — amakudari's four paths, distinct
from D64's coordination-cost axis), and D133 (an administrative-legal-tradition moderator — Bouckaert's
finding that NPM is Anglo-Saxon/common-law-specific and NWS is administrative-law-tradition-specific, with
even Germany's own reform attempt failing to produce the predicted shift). D133 is the sharpest finding: the
register's reform-trajectory rows (D60–D65, D70–D77, D100–D104) have been built and compared without this
gate since job 6, and nobody has gone back to re-check them with it applied.

**Two cases extend existing conflicts rather than yielding new rows.** Korea's EPB (concentrated
planning+budget authority under President Park's personal supervision, not structural constraint) is logged
as a third mode at [[constraint-vs-capacity-as-the-investment-mechanism]], alongside Position A (shackling)
and Position B (Wade's conditionality) — it resolves neither, it adds a channel neither measures. Singapore's
Civil Service College (a statutory board, legally autonomous yet fused with its parent ministry) is logged at
[[open-questions]] Q3 as a fourth candidate case for the public/private invariance question.

**New open question**: Q125 asks the batch's own question plainly and records the mixed verdict, with a
stated next step — re-score an existing reform-trajectory row against a non-Anglo institution with D133's
gate applied, which no source anywhere in this wiki has done.

**Seven pages written**: [[nordic-model-and-interest-oriented-citizenship]],
[[chinese-cadre-rotation-and-the-iron-triangle]], [[regionally-decentralized-authoritarianism]],
[[singapore-milestone-programs-and-elite-formation]], [[amakudari-and-institutionalized-capture]],
[[koreas-economic-planning-board]], [[neo-weberian-state-and-administrative-traditions]].

## [2026-08-21] case-profile | institution-case-profiles (job 15, 8 sources, FDA + Meta)

**The wiki's first case-study job — not literature capture, but scoring the register against two real
institutions' own primary documents.** FDA: FY2025 PDUFA financial report, current org chart, HHS OIG report
on accelerated-approval confirmatory-trial delays. Meta: FY2025 10-K, 2026 DEF14A proxy, Corporate Governance
Guidelines, plus the Oversight Board's Charter and Bylaws as a distinct sub-institution.

**A real capture bug caught and fixed mid-job.** Two SEC EDGAR filings (`04-meta-10k-fy2025`,
`05-meta-proxy-def14a-2026`) silently captured SEC's bot-block page instead of real content —
`capture_url` exited zero, wrote a plausible-looking 63-line file, and `audit_captures` reported 0 issues.
Root cause: SEC wants a *declared*, non-browser User-Agent naming the actual tool and a contact; this wiki's
capture tool deliberately spoofs a browser UA to get past *other* sites (ftc.gov, Akamai-fronted hosts) — the
two policies are opposite and the tool only implements one. Fixed manually (compliant-UA fetch +
`trafilatura.extract`, matching the tool's own pipeline) and logged as a kit-level gap in `master_notes.md`,
`Scope: kit, Status: open`.

**1. D128 promoted.** Meta's dual-class structure gives Zuckerberg 60.8% of voting power against a 13–14%
economic interest — a clean, current, quantified control/cash-flow wedge, La Porta et al.'s mechanism run for
the first time against a real, named institution. A live 2026 shareholder proposal to unwind the structure,
reported to have majority support among independent shareholders and still losing to the controlling bloc, is
a real-time confirmation of D127's absorption logic.

**2. D112 promoted, on the richest test case in the register.** Meta's Oversight Board holds textbook binding
authority over content decisions, qualified at four distinct points by Meta's own continuing judgment: a
legal-violation carve-out, Meta-defined remedy scope, a feasibility test for extending decisions to duplicate
content, and — the sharpest finding — a standing Meta veto over amending the charter that grants the binding
authority in the first place. Funding (an irrevocable trust) and case-selection independence are, by contrast,
genuinely real and specifically engineered. Recorded as a mixed case, not a debunking.

**3. D35 confirmed.** FDA's human-drug review is 77% industry user fee / 23% appropriation in FY2025, gated
by three statutory anti-substitution conditions — a real, working instance of the safeguard this row's
Niskanen material only theorised.

**4. An axis with no literature source at all.** D134 (leadership-vacancy share) was surfaced directly from
FDA's own org chart — four senior leadership lines (Commissioner, Principal Deputy Commissioner, Chief of
Staff, Chief Medical Officer) shown Acting or Vacant simultaneously. Registered and flagged explicitly as the
register's first row born from a case profile rather than named by any source.

**5. What did not score, recorded as informative rather than a gap.** D110's full 24-provision index was only
partially extractable from the captured documents; D129 (selectorate ratio) applies awkwardly to a
majority-controlled shareholder vote, since the model's own assumptions don't anticipate a near-degenerate W.
D128 has no analogue for a government agency (FDA) at all — a genuine scope limit, not a capture failure.

**Three pages written**: [[fda-case-profile]], [[meta-case-profile]], [[meta-oversight-board-case-profile]].
