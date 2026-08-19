# Bureaucratic Growth and Parkinson's Law

Parkinson's claim is that administrative headcount grows at a rate set inside the organisation and unrelated to the work to be done: "the number of officials and the quantity of work to be done are not related to each other at all." He names two motive forces — an official multiplies subordinates rather than rivals, and officials make work for each other — and offers no evidence for either. Klimek, Hanel & Thurner (2008) supply the quantitative layer Parkinson's own essay only promises: a 197-country cross-section putting a threshold at cabinet size N≈20–21, two historical staff series in which headcount rises while workload falls (British Colonial Office +6%/yr as the territories administered shrank; Royal Navy admiralty officials +80% as ships in commission fell from 62 to 20), and a renewal model whose growth rate depends only on promotion probability and subordinates-per-promotion, with no workload term at all. Niskanen's budget-maximising bureau is the contrast case: same conclusion that bureaus are too big, entirely different mechanism — the bureau head maximises budget, the lump-sum funding form gives him all-or-nothing power over his sponsor, and the resulting bureau can be *internally lean* and still allocatively oversized. The two accounts are not the same claim, and neither has been tested against the other.

**Evidence tier note.** Grade this page piece by piece; the sources differ sharply.
- **Parkinson (1955)** — (b) assertion only, and **the primary text is only partially captured**. The file in `raw/` is a ~500-word excerpt that stops at the sentence "The validity of this recently discovered law must rely mainly on statistical proofs, which will follow", ending with a dead link to the full essay PDF. The Admiralty and Colonial Office figures Parkinson is famous for **do not appear in our capture**, and nothing on this page attributes a number to him.
- **Klimek, Hanel & Thurner (2008)** — mixed. The cabinet-size cross-section is (a) empirical but observational and uncontrolled. The two historical staff series are (a) empirical but are Parkinson's own 1957 figures restated by the authors, not re-derived from primary records, and n=2. The growth model and the retirement-age model are (b) simulation with illustrative parameters, never fitted to a real staffing series.
- **Niskanen (1968)** — (b) pure deductive model with invented numbers. Niskanen himself devotes a section to critical tests that had *not* been run.

## Parkinson's mechanism, as far as our source goes

**[assertion — Parkinson]** Two "motive forces," stated as near-axiomatic:

1. **Factor I — "an official wants to multiply subordinates, not rivals."** A manager facing overload prefers two subordinates to one peer, because subordinates entrench his position and a peer competes for it. The choice is driven by the official's career security, not by the task.
2. **Factor II — "officials make work for each other."** Each added post generates review, minuting and coordination load for the others, which reads as evidence of demand for further posts.

The scope is the British civil service, circa 1955. Parkinson makes no claim about private firms in this excerpt, and the mechanism's generality is the wiki's inference, not his.

## The quantified test

**[empirical, observational — Klimek/Hanel/Thurner]** *Decision-body size.* Cabinet size N for 197 countries and territories (CIA *Chiefs of State and Cabinet Members*, 2007) is negatively and, the authors report, highly significantly associated with the UNDP Human Development Indicator and the World Bank political-stability indicator; the linear fits cross the population median near **N=20** on both. Most cabinets fall in the 13–20 range. The British cabinet, traced 1257–1955, ran through five life cycles, each ending when membership passed roughly 20 and the body was superseded by a smaller successor council. No cabinet of exactly eight members appears in either Parkinson's 1957 data or the authors' 2007 cross-section.

The mechanism offered is an opinion-formation model on a small-world network (connectivity k, rewiring probability e, adoption threshold h>0.5): as N grows, each member's influence falls and the body fragments into coalitions, producing a transition from consensus into a high-dissensus regime whose location depends on k and e. That the model reproduces a transition is a demonstration that it *can*, not evidence that it *does*.

**Take the threshold as suggestive, not established.** The cross-section has no controls for regime type, income, federalism or colonial legacy, and the reverse arrow — unstable coalition politics inflating cabinet size through patronage — is plausible and unaddressed.

**[empirical, n=2, restated from Parkinson]** *Headcount decoupled from workload.* The two canonical series:

| Body | Period | Staff | Workload proxy |
|---|---|---|---|
| British Colonial Office | 1935–1954 (peacetime subperiods; wartime growth was stronger still) | 372 → 1661, ≈ **+6%/yr** | Territories administered "shrunk dramatically" |
| Royal Navy, admiralty officials | 1914–1928 | **+80%** | Ships in commission 62 → 20 |

This is the sharpest available evidence that administrative headcount can move opposite to the workload it nominally serves. It is also two cases, in one country, restated at second hand.

**[model — Klimek/Hanel/Thurner]** *Why growth needs no workload term.* Staff are modelled as a flow: entry, promotion with probability p per year, promotion granting r subordinates, attrition γ. Total staff grows as e^(λt) with dominant eigenvalue λ = (1 − γ + (r−1)p)(1 − q₋). Growth or shrinkage is fully determined by promotion rate and subordinates-per-promotion given attrition — **workload does not enter the model**. The phase diagram (at γ=0.01) gives the (r,p) boundary at λ=1, which the authors present as a control lever: tune r and p so the eigenvalue does not exceed one.

**[model]** *Shape beats size.* Simulating hierarchies of depth L=3…7, average efficiency curves converge onto bundles indexed by ΔL — the number of levels below the promotion cutoff — not by L. Past moderate depth, absolute size stops mattering and only the *shape* of the hierarchy determines achievable average efficiency and the efficiency-maximising retirement age; flatter hierarchies imply an earlier optimum. The individual-level driver is the "Prince Charles Syndrome": efficiency rises with experience but collapses past a bifurcation if promotion is withheld too long.

## Niskanen's bureau: a different mechanism reaching a similar verdict

**[model — Niskanen]** A bureau is defined by its funding form, not its ownership: an organisation that exchanges a specified output for a **total budget** rather than a per-unit price. Two premises drive everything. The bureaucrat's utility — salary, perquisites, reputation, power, patronage, ease of making changes — rises with total budget, so he maximises budget subject to covering minimum cost. And the lump-sum exchange gives the bureau an all-or-nothing position against its sponsor, letting it appropriate the whole consumer surplus.

Two equilibria follow, and the distinction matters more than the numbers:

- **Budget-constrained** — the budget just covers minimum cost. There is **no internal slack at all**; a cost-effectiveness audit finds nothing. The bureau is nevertheless producing well past the Pareto-optimal output. "No waste found" and "correctly sized" are different findings.
- **Demand-constrained** — the bureau produces where marginal value reaches zero and carries genuine slack, which it has no incentive to reveal. An outside analyst cannot recover the true minimum-cost function from observed budget and output behaviour.

**[model — illustrative numbers, invented not fitted]** With demand V = 200 − 1.00Q and cost C = 75 + .25Q: competitive industry output 100; private monopoly 50 (55.6 under monopsony); **bureau 166.7** buying factors competitively, **200** discriminating among factor suppliers — two-thirds more and exactly twice the competitive output. The competitive-factor-market bureau generates factor surplus of 3,472.2, about 55% of the total surplus a competitive industry would produce; the monopsony bureau dissipates all surplus, consumer and factor alike. Comparative statics: in the budget-constrained region, a bureau at constant marginal cost grows at **twice the rate** of a competitive industry for the same demand shift, and likewise for a downward cost shift; in the demand-constrained region, further cost reductions change neither output nor budget.

**[model]** The distributional claim is the load-bearing one: bureaucratic organisation does not destroy value at random, it **shifts surplus from consumers to the owners of specific factors** — input suppliers, contractors, employees. Niskanen's inference is that legislatures "predominantly representing factor interests" prefer provision through bureaus for that reason. Accountability runs, in the model, to factor owners rather than to the nominal principal.

**[model — levers, none tested]** Force bureau-to-bureau competition and treat consolidation as the harm it is ("the passion of reformers to consolidate bureaus with similar output seems diabolically designed to increase the inefficiency"); invert the incentive by making the top 5% of a bureau's personnel's salaries a *negative* function of budget for a given set of outputs; contract out to profit-seeking firms and retain only review. All three are deductions from the model, and all require output measurement the model itself says is unavailable.

## What separates the two accounts

**[wiki synthesis]** Both predict oversized bureaus; the mechanisms share almost nothing.

| | Parkinson / Klimek | Niskanen |
|---|---|---|
| What grows | Headcount | Output and budget |
| Driver | Individual official's career incentive, aggregated | Bureau head's utility in total budget |
| Role of workload/demand | None — growth is workload-independent by construction | Central — demand slope determines which equilibrium and how much distortion |
| Internal slack | Implied but not modelled | Present in one equilibrium, **absent in the other** |
| What would stop it | Tuning promotion rate and subordinates-per-promotion | Elastic demand, rival suppliers, inverted pay-budget link |

Niskanen's budget-constrained equilibrium is the pointed case: a bureau with no fat, no empire-building and no idle staff, still producing roughly two-thirds more than the social optimum. Any diagnosis that looks only for waste will not see it.

## What this page does not establish

**[wiki synthesis — gaps]**

- **Nothing here is about institutional age.** Klimek et al.'s only "age" variable is the *individual official's* career tenure — years in service, age of qualification, retirement age τR — not years since the institution's founding. The Colonial Office and Navy series are calendar-time trajectories of already-existing bodies, not comparisons of young against old institutions. Niskanen's one age claim — "new bureaus... will be very cost conscious... older bureaus... couldn't care less" — is an aside he disowns in his own footnote 1, which states the paper "develops only the static model of a bureau and does not explore the time dimension of budget maximization." It conflates age with which equilibrium a bureau sits in, and establishes neither. See [[open-questions]] Q7.
- **Nothing here tests firms.** Every unit in Klimek et al. is a public body; Niskanen's model is built on a funding form he treats as bureau-specific. Whether Parkinson's Factors I and II operate inside a private firm is untested in both. See [[parkinson-vs-knowledge-hierarchy-growth]].
- **Whether the mechanism tracks ownership or funding form is open.** Niskanen's own footnote 3 concedes that post offices, universities and hospitals are "mixed" — part per-unit sale, part budget — regardless of public or private status. If the mechanism follows the lump-sum exchange rather than public ownership, "public vs. private" is the wrong axis and [[dimensions-of-institutional-variation]] D35 is the right one. Neither the source nor this wiki has tested it.

## Source

- `raw/research/scale-effects/04-parkinson-law-original-essay.md` — C. Northcote Parkinson, "Parkinson's Law", *The Economist*, November 1955. http://doc.cat-v.org/economics/parkinsons-law/ — **partial capture**: ~500 words, cuts off before any statistics.
- `raw/research/scale-effects/05-parkinson-law-quantified-empirical.md` — Peter Klimek, Rudolf Hanel & Stefan Thurner, "Parkinson's Law Quantified: Three Investigations on Bureaucratic Inefficiency", 2008. https://arxiv.org/pdf/0808.1684
- `raw/research/scale-effects/03-niskanen-peculiar-economics-bureaucracy.md` — William A. Niskanen, "The Peculiar Economics of Bureaucracy", *American Economic Review* 58(2), May 1968, 293–305. https://sites.socsci.uci.edu/~jkbrueck/course%20readings/Econ%20272B%20readings/niskanen.pdf (JSTOR: http://www.jstor.org/stable/1831817)

## Related

- [[knowledge-hierarchies-and-the-cost-of-scale]] — the rival account of why headcount and layers grow: layers as a cost-minimising response to output, not as career self-interest. The two are filed against each other in [[parkinson-vs-knowledge-hierarchy-growth]].
- [[hierarchy-and-near-decomposability]] — Simon's argument that depth is what makes large systems buildable at all, which is the functional counterweight to reading every added layer as bloat.
- [[governance-structures]] — Williamson's limits-to-firm-size argument is the private-sector analogue: hierarchy defeating itself at scale, by a different mechanism and with no threshold either.
- [[transaction-costs]] — the bureau's unrecoverable cost function is a measurement-cost failure of exactly the kind that page treats as the link between institutions and performance.
- [[dimensions-of-institutional-variation]] — supplies D35 (funding mechanism), D36 (span of control), D37 (hierarchy depth) and the flatness variant ΔL from this page's sources.
- [[functional-vs-rent-seeking-growth]] — whether growth in institutional size is a cost-minimising response to scale or rent extraction; Niskanen is one pole.
- [[efficiency-of-institutions-north-vs-williamson]] — Niskanen's budget-constrained equilibrium is a formal case of an arrangement with zero internal waste that is still allocatively wrong, which bears on the efficiency-default question.
- [[open-questions]] — Q7 (age vs. size vs. competitive pressure) and Q9 (does decay differ where output is measurable) both take evidence from this page.
