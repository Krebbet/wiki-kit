# Knowledge Hierarchies and the Cost of Scale

Garicano and Rossi-Hansberg derive hierarchy from a single friction: knowledge can be reused without limit, but the time to apply it cannot. Production workers learn the common problems; managers learn the rare ones and are called on only when a subordinate cannot solve his own — "management by exception." Layer count and span of control are then *outputs* of a cost-minimisation over who learns what and who asks whom, not design choices. Because the top of the hierarchy cannot replicate itself, the cost function is U-shaped in output with minimum efficient scale rising in the number of layers, so larger organisations rationally run deeper ones. The sharpest empirical result is about how a firm grows rather than how big it is: a firm that grows **by adding a layer** cuts the knowledge and the wages of every pre-existing layer, because retraining the whole workforce is dearer than putting a few experts on top; a firm that grows **without adding one** must upgrade and pay its existing staff more, because a larger team breaks its managers' time constraint unless workers become more self-sufficient. The two costs the model turns on pull in opposite directions — cheaper communication deepens hierarchies, cheaper knowledge acquisition flattens them — which is why any single "information flow" axis conflates two things.

**Evidence tier note.** The framework is (b): a formal cost-minimisation and general-equilibrium assignment model with closed-form results under specific functional forms. The empirical layer is (a) but secondary and associational — the authors are surveying a decade of work, largely their own, and say plainly that the evidence "fails to falsify the mechanisms we have emphasized", i.e. consistency rather than proof, closing with a call for causal evidence. The strongest single piece is Caliendo, Monte & Rossi-Hansberg (2014): French administrative firm-worker data, 2002–2007, 553,125 firm-year observations, with **firm fixed effects**, which separates true reorganisation dynamics from cross-sectional composition. The weakest is the wage-polarisation narrative, which is calibration against stylised facts. Every dataset and every application in the source is private and for-profit.

## The mechanism

**[model]** An agent's knowledge is an input that can be applied to any number of problems; her time cannot. Hierarchy is the division of labour that relaxes the time constraint: routine problems are solved where they arise, exceptional ones are escalated to someone who has invested in learning rarer cases. Two costs govern the design:

- **Communication cost h** — the time a more-knowledgeable agent spends answering a question, incurred whether or not she turns out to know the answer.
- **Knowledge-acquisition cost c** — the cost of learning to solve a given measure of problems, falling with individual ability.

Span of control falls out of the manager's time constraint, `1 ≥ h·n·(1−F(z))`: team size is bounded by how costly help is and how often subordinates need it. Optimal hierarchies have **non-overlapping knowledge** across layers — nobody learns what the layer below already knows.

This is explicitly *not* a monitoring or agency-cost theory of hierarchy; the source distinguishes itself from Calvo & Wellisz's supervision models and from loss-of-control models. Layers exist to route problems, not to watch people.

**Scope condition, stated in the source.** Hierarchy is optimal precisely because *labelling* a problem — knowing in advance who can solve it — is costly. If problems could be matched to knowledge-holders for free, no hierarchy would be needed. Tacitness of knowledge is what makes the structure earn its keep.

## Layers scale with output

**[model]** Minimising `C^L(q) = min Σ n_l(c z_l + w)` subject to an output constraint and managers' time constraints, with an integer constraint pinning the top layer to a single agent — "it is hard for CEOs to replicate themselves" — yields a cost function `C(q) = min_L C^L(q)` that is **U-shaped in output with an increasing number of layers**. Minimum efficient scale rises with L; the wage bill at minimum efficient scale falls with L. The implication is a cost advantage to size that owes nothing to any exogenous scale economy: past a given output, an organisation with more layers is cheaper per unit, and below it, dearer. Without the top-manager integer constraint the link breaks and a corner shop would use the same organisation as Walmart in miniature.

**[empirical — French panel]** Firms with more layers are larger in value added and total hours and pay higher average wages, and layer transitions of exactly one level are common, becoming likelier as value added rises. Geerolf (2014), cited, derives a Pareto distribution of spans within an L-layer firm with coefficient 2^L/(2^L−1) → 1, connecting hierarchy depth formally to the heavy-tailed firm-size distribution.

## The sharpest result: growth with a layer vs. growth without one

**[empirical — firm fixed effects]** Adding a layer *reduces* the knowledge and the wages of workers in all pre-existing layers. The firm does not retrain its workforce upward; it hires or retains **less** knowledgeable people below and lets them specialise in yet-more-routine work, putting a thin layer of expertise on top. Growing without adding a layer does the reverse: the existing team must become more self-sufficient, so knowledge and pay at existing layers rise.

The French wage levels make the pattern concrete:

| Position | Average hourly wage |
|---|---|
| Workers in 1-layer firms | €27.17 |
| Bottom layer, 2-layer firms | €18.15 |
| Bottom layer, 3-layer firms | €16.91 |
| Top managers, 4-layer firms | €87.66 |
| Direct subordinates of those top managers | €43.60 |
| Equivalent layer in 3-layer firms | €57.43 |

**[wiki synthesis]** Read carefully, this breaks the usual reading of headcount growth. "The organisation got bigger and the people in it got less capable" is, on this model, not decay — it is the cost-minimising response to a demand shock, and it is *distinguishable in the data* from the alternative growth path by whether a layer was added. That gives a testable discriminator between functional and dysfunctional growth that no other source in this batch supplies. It has been run on French manufacturing firms and nowhere else.

## Two costs, opposite signs

**[model, with supporting survey evidence]** Holding size fixed and varying the cost parameters:

- A fall in **knowledge-acquisition cost c** (databases, training, information technology) *reduces* the number of layers, *widens* span of control, and raises the ratio of production workers to problem-solvers.
- A fall in **communication cost h** (networks, telepresence) *increases* the number of layers.

So depth can rise either because the organisation got bigger at fixed technology or because communication got cheaper at fixed size, and the two channels must be kept apart. Bloom, Sadun, Garicano & Van Reenen (2014), a 1000-firm ICT and management-practice survey cited in the source, finds the split empirically: ERP and CAD-CAM systems decentralise, network technologies centralise.

**[wiki synthesis]** This is the reason [[dimensions-of-institutional-variation]] now carries communication cost (D39) and information-acquisition cost (D40) as separate axes and marks the undifferentiated "information flow" component of D25 superseded. A single information-richness axis would predict nothing here, because its two components move hierarchy depth in opposite directions.

## Stagnation: sunk organisational capital as lock-in

**[model]** The dynamic extension adds layers sequentially as an organisation exploits a given technology, with diminishing returns: most problems eventually become well known, so each further layer of expertise is worth less than the last. The corner case is stagnation — an organisation that has thoroughly exploited its existing technology may rationally postpone adopting a superior one indefinitely, because the new technology makes the accumulated hierarchy obsolete and a fresh one must be built from scratch.

**[wiki synthesis]** This is a firm-level lock-in mechanism with the same shape as the matrix-level one in [[path-dependence-and-increasing-returns]], but a different unit and a different clock. It runs on **time since the current technology was adopted**, not time since founding. It is not evidence that organisations ossify with age, and must not be cited as such — the source uses no firm-age variable anywhere.

## What is out of scope

**[wiki synthesis — gaps]**

- **No public sector, anywhere in the source.** The objective function is minimising a wage bill to produce a market-priced quantity q, and equilibrium is closed by a competitive labour market. A bureau whose output is unpriced and often unmeasurable has no direct analogue for q. Whether management-by-exception and layer-scaling survive that substitution is untested. See [[open-questions]] Q24.
- **No power.** Who selects managers, who removes them, and to whom the organisation answers are absent. The one power-adjacent result is that under two-sided information asymmetry the efficient contract makes the most knowledgeable agent the full residual claimant — knowledge advantage converting directly into control rights.
- **Association, not identification.** The authors say so themselves. The layer-wage results survive firm fixed effects, which is the strongest claim available here; nothing in the source is a randomised or quasi-experimental test of the mechanism.

## Source

- `raw/research/scale-effects/08-garicano-rossi-hansberg-knowledge-hierarchies.md` — Luis Garicano & Esteban Rossi-Hansberg, "Knowledge-based Hierarchies: Using Organizations to Understand the Economy", NBER Working Paper 20607, 2014. https://www.nber.org/system/files/working_papers/w20607/w20607.pdf

## Related

- [[hierarchy-and-near-decomposability]] — Simon's earlier and more general answer to the same question: why complexity forces depth. Simon explains why layers exist at all; this page prices them.
- [[bureaucratic-growth-and-parkinsons-law]] — the rival account of layer and headcount growth, driven by career incentive rather than output. Filed as [[parkinson-vs-knowledge-hierarchy-growth]].
- [[governance-structures]] — Williamson bounds firm size through asset specificity and the non-self-enforcing promises of selective intervention; this model bounds it through knowledge and communication cost. Different frictions, same question, and they do not contradict.
- [[transaction-costs]] — h and c are a micro-founded pair of transaction costs, and the finding that they push organisational form in opposite directions sharpens that page's taxonomy.
- [[path-dependence-and-increasing-returns]] — the stagnation result is a firm-level lock-in mechanism running on technology vintage, offered as a parallel, not as age evidence.
- [[dimensions-of-institutional-variation]] — supplies D36 (span), D37 (depth), D39 (communication cost) and D40 (information-acquisition cost), and forces the supersession note on D25.
- [[functional-vs-rent-seeking-growth]] — this page is the functional pole: layers as cost minimisation.
- [[open-questions]] — Q3 (public/private invariance), Q7 (age vs. size) and Q24 (does this transfer to unpriced output).
