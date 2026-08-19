# Property-Rights Theory of the Firm

Contracts cannot specify every future contingency, so someone must hold the right to decide whatever the contract is silent on. Grossman & Hart's answer is that **ownership of a non-human asset simply *is* that right** — the "residual right of control" — and that owning it changes each party's fallback position in the ex post bargain, hence each party's expected share of the surplus, hence how much each is willing to sink into non-contractible relationship-specific investment beforehand. Integration is therefore never a free lunch: transferring residual rights buys one party's increased investment at the price of the other party's reduced investment, and the optimal allocation gives the asset to whichever party's non-contractible investment matters more at the margin. Hart's 2016 Nobel lecture carries the same mechanism into financial structure (why debt and state-contingent control exist at all), into the public-versus-private provision decision (the private-prison case), and finally into a behavioural revision — "contracts as reference points" and the shading failure mode — which Hart introduces precisely because the rationalist version predicts contractual devices that nobody actually uses. That revision is kept in its own section on this page because it abandons an assumption the rest of the theory rests on.

**Evidence tier note.** Grossman & Hart (1986) is **(b) a formal model** throughout — a two-period game with Nash-bargained renegotiation and comparative-static propositions — and the authors say so, flagging "features of our theory that lack quantitative completeness." Its one applied section is a **loose qualitative case application with cross-sectional correlations**, not a test. Hart's lecture is mostly **(b)**, with **(a) empirical** work cited mostly in single sentences and footnotes rather than presented: Kaplan & Strömberg (2003) on VC contracts, Benmelech (2009) and Benmelech & Bergman (2008) on collateral and maturity, Baker & Hubbard (2003/2004) on trucking, Woodruff (2002) on Mexican footwear. The **best-evidenced** part of the lecture is the shading section, where Fehr, Hart & Zehnder's lab experiments were designed to test a specific model prediction against a naive-rationality alternative. The **weakest** is the private-prison violence claim — one correlational citation plus a 2016 DOJ report, with no causal design described. Both sources are **silent on selection effects** (see below). **(c) wiki synthesis** is marked inline.

## The mechanism

**[framework — Grossman & Hart 1986; Hart 2016]** The chain, as the sources state it:

1. Some future contingencies affecting an asset's use are too costly to specify ex ante, though they become obvious and can be bargained over ex post — **ex ante non-contractible, ex post contractible**. Contract incompleteness is about the *future*, not about measurement per se.
2. By law and by default, whoever **owns** the asset decides in any contingency the contract is silent on. Grossman & Hart adopt Holmes's (1881) formulation: the owner "is allowed to exclude all, and is accountable to no one but him." Their standing illustration: absent a contract clause on an extra print run, the right to decide belongs to whoever owns the press.
3. Ex post bargaining is assumed costless and symmetric-information (Nash bargaining, 50:50 split), so ownership does **not** change the ex post outcome — renegotiation always reaches the efficient action. What it changes is each party's **status-quo payoff**, and hence each party's share of the ex post surplus.
4. Each party's ex ante investment is chosen to maximise its own expected payoff, which rises with its expected surplus share.
5. Therefore the owner, anticipating a larger share, **overinvests** relative to first-best, and the non-owner **underinvests** — precisely when marginal and average investment returns move together (their Assumption 5). Under non-integration, the failure mode is instead *moderate underinvestment by both*.

The decision rule (Proposition 1): firm 1 should acquire firm 2 exactly when "firm 1's control increases the productivity of its management more than the loss of control decreases the productivity of firm 2's management."

**The point that is easiest to miss.** The authors explicitly refute the naive Coasian argument that integration only expands the feasible set. A buying B and paying B's manager the subsidiary's full profit does **not** replicate non-integration, because the new owner cannot credibly commit not to intervene using the residual rights he now holds. **[wiki synthesis]** This is structurally the same self-binding failure that Williamson's selective-intervention argument identifies on [[governance-structures]] and that ruler-shackling addresses in [[credible-commitment]]: the party with unreviewable authority cannot promise not to use it. Three literatures, one shape.

**Hart's worked example.** A coal mine and a power plant. The manager's outside option under ownership is `p̄ − λc`, and her incentive to invest in cost-reducing innovation rises with how much of the resulting gain she can capture — higher when she owns the mine, lower when she is an employee subject to the owner's veto. Hart's compression of the whole theory: not "give people upside", but **assets end up governed by whoever's uncontractible effort the contract most needs to protect.**

## Contractibility, verifiability, observability

**[framework — Hart 2016]** Hart insists on three distinct properties where a coarser literature says "measurability," and the distinction does real work:

- **Contractible** — can be specified in a binding agreement ex ante.
- **Verifiable** — can be proven to a third party (a court) ex post.
- **Merely observable** — both parties can see it, but no third party can be convinced.

Examples the source supplies: coal ash content is hard to specify ex ante but easy to observe and verify once realised. The boiler example is sharper still — the *location* of the power plant is contractible, but whether it installs a boiler suited to *this* mine's coal is not: two decisions in one relationship, split on contractibility. And the split changes institutional form directly. Aghion & Bolton (1992) assume monetary returns are verifiable and transferable, and get state-contingent equity-like control. Hart & Moore (1998) drop that assumption — the manager can "walk off" with the cash — and get a **debt contract** instead. Different verifiability assumption, different institution.

**The Maskin-Tirole problem, and what its non-observation implies.** Maskin & Tirole show that a costly-challenge mechanism can in principle convert an observable-but-unverifiable variable into an effectively contractible one, which would dissolve the need for ownership entirely. Hart reports that he knows of essentially no real cases where such mechanisms are used, and treats that **absence as itself a data point** against the fully-rational baseline — the motivation for the behavioural turn in the last section of this page. Formal contract design has a demonstrated ceiling in practice that the theory does not predict.

## The scope conditions the theory carries

**[framework]** These are stated by the sources and are load-bearing:

- **Replaceability of human capital.** An owner's bargaining power is void if the other party's manager is indispensable. Hart states this explicitly as a limit on the whole theory.
- **A functioning legal system** that can enforce *ownership* and *verifiable* terms even where it cannot enforce fine-grained specific performance. Unstated by Hart but presupposed everywhere; it should not be assumed to travel to weak-state settings.
- **A competitive market in identical potential trading partners at date 0** (Grossman & Hart's explicit assumption).
- **Each manager receives the full return of his firm**; no employees other than the two principals; no repeated game; no reputation. The authors flag this and do not relax it. On repetition they say plainly that it is unclear "why reputation should have any particular implications concerning the ownership of assets."
- **Alienability of benefits.** If the acquiring firm can *replace* the other manager and capture his private benefit, the overinvestment distortion disappears — so the power to hire and fire interacts with the power over residual rights.

**Lifecycle note, thin but explicit.** Hart cites Rajan (2012) for the suggestion that "part of the transformation of a start-up into a successful, mature firm may be a standardization process that ensures that no individual's human capital is that important" — which under this theory would shift the efficient ownership structure over a firm's life, from human-capital-dependent to non-human-asset-dependent. **This is asserted via a citation, not modelled or tested**, and it is the only age-flavoured claim in either source. Do not upgrade it. See [[open-questions]] Q7.

## The one applied case: insurance distribution

**[empirical — weak, Grossman & Hart 1986 §IV]** The theory predicts that where the client relationship's future value depends heavily on non-contractible agent effort, the agent should own the client list. The 1980s US insurance industry is offered as consistent:

| Line | Share of client lists owned by independent agents |
|---|---|
| Property-casualty | 65% |
| Life insurance | 12% |
| Term life | 46.2% |
| Whole life | 19.4% |

Marvel (1982)'s correlation between independent-agent market share and client-acquisition cost is also cited. Treat this as **suggestive cross-sectional association**, not a controlled test: the authors themselves interpret it as "considerable latitude" and note and rebut a rival explanation (Marvel's own) for the same correlation in a footnote. A second lever appears here — **back-loading of commission** — which is needed to induce persistent-client effort but only works if paired with the correct ownership allocation of the list.

## Public versus private provision: the prison case

**[framework with one weak empirical citation — Hart 2016 §4]** This is one of very few places in this batch where a firm-boundary theory is turned directly on a public/private choice, and its narrowness should be stated up front: it concerns **only** the point at which government decides to provide a service itself versus contract it out. It says nothing about how a bureau behaves internally once that decision is made.

The argument runs on exactly the same residual-control mechanism. Government contracts with private prison operators are in fact elaborate — food, hygiene, health care, work, education, recreation are all covered — but Hart, Shleifer & Vishny (1997) argue they are significantly incomplete on two things: **the use of force by guards, and the quality of personnel**. A private contractor can therefore use its residual control rights to save money by hiring cheap, unqualified guards who lack the skill to handle violent situations. Structurally identical to the coal mine choosing high-ash coal: the supplier takes a contractually permitted action that saves money at someone else's expense — in one case the power plant's, in the other society's. Hart's own footnote 19 maps this onto Holmstrom & Milgrom's multitask model: cost-cutting is easy to specify and reward, violence prevention is not, so incentivised effort migrates to the measurable one. See [[multitask-incentive-theory]].

If government owns the prison, the problem does not arise in that form — the government can simply forbid the warden from hiring cheap guards, exactly as a power plant owning the mine can require low-ash coal.

Private provision has a countervailing benefit on the same logic: a private warden has a **greater incentive to innovate**, to find socially efficient savings or develop rehabilitation programmes. So the answer is contingent, and Hart states the contingency: private provision may win where innovation matters and violence is a small problem (half-way houses, youth facilities); in maximum-security prisons, where preventing violence is paramount, Hart, Shleifer & Vishny "conclude that the case for private provision is weak." The same logic is extended **by analogy only** to garbage collection (favours private), the army, police and foreign policy (against), and schools and health care (ambiguous). Competition is said to strengthen the case for privatisation because quality-cutting draws a market response — **asserted with no citation in this lecture**, and Hart notes competition may work for schools and hospitals but is "hard to imagine" for prisons.

**Evidence.** "Hart et al. (1997) cite some evidence that the level of violence is indeed higher in private prisons," plus a 2016 DOJ report. One correlational citation, no causal design described. This is the weakest empirical claim on the page and the wiki should carry it at that weight.

**The normative claim, attributed not adopted.** Hart's stated conclusion: "the public-private choice should be seen as a matter of efficiency, not ideology." **[wiki synthesis]** Two things to keep apart. The claim that the *mechanism* is invariant across the divide is a strong and defensible modelling position. The claim that the *answer* is invariant is one Hart explicitly does not make — the optimum turns on which tasks are contractible, whether competition is available, and how innovation trades against harm prevention. And the "efficiency, not ideology" framing is itself a position: which investments count as non-contractible is a modelling choice that can encode priors. Logged as a scope-limited data point on the Williamson side of [[efficiency-of-institutions-north-vs-williamson]], not as a resolution of it.

**Provenance worth recording.** Hart discloses serving as an expert witness for the US government in two corporate tax-shelter cases (Black & Decker v. USA; WFC Holdings/Wells Fargo v. USA), applying his own firm-boundary theory in support of the government's position. Not evidence of bias; relevant provenance.

## Contracts as reference points, and shading

**[framework, with the batch's best experimental evidence — Hart & Moore 2008; Fehr, Hart & Zehnder 2009/2011/2015]**

This section is kept separate because it **abandons full rationality**, an assumption the rest of the page depends on. Hart introduces it explicitly under pressure from the Maskin-Tirole non-result, calls the move "an unfortunate conclusion" that most economists resist, and closes the lecture conceding that "there is as yet no tractable, widely agreed upon, theory of incomplete contracts."

The mechanism: a contract negotiated under competitive ex ante conditions functions as a **reference point** for what each party feels entitled to. A party who receives less than that entitlement through the other's unilateral ex post discretion feels aggrieved and retaliates by **shading** — deliberate under-performance *within the letter of the contract*.

Shading is a distinct failure mode and deserves distinct vocabulary:

- It is **not moral hazard**. Effort is withheld as punishment for a perceived fairness violation, not because effort is costly and unmonitored.
- It is **not classic principal-agent drift**. It operates with full information and no measurement problem.
- The trigger is the *procedure*, not the payoff: a decision taken inside a competitively negotiated frame is accepted as legitimate; the same payoff imposed by unilateral ex post discretion is not.

The design implication is that **rigid, fixed-price contracts can dominate flexible discretionary ones** — accepting some ex post inefficiency in exchange for suppressing shading losses. Hart offers this as the explanation for the shape of the employment contract itself: fix the wage, let the employer choose the task, rather than leaving both open to negotiation.

**Evidence status.** This is the one place in the lecture where a model was built to be tested and then tested. Fehr, Hart & Zehnder's laboratory subjects choose rigid contracts significantly more often than the fully-rational prediction, and shading concentrates where the model predicts it. It is lab evidence, and the wiki should say so — but it is a genuine test against a stated alternative, which most of this batch is not.

## What is not established

- **Selection effects.** Both sources are silent. Neither models nor discusses who is drawn into or screened out of ownership, management or investor roles *by* the structure on offer. The two selection-adjacent passages are weaker than selection: the threat of firing and replacing a manager is a bargaining lever, and the date-0 competitive market is about price-setting before lock-in, not about sorting person-types into roles. Nothing here supports a claim about [[open-questions]] Q4.
- **Multi-party allocation.** Every proposition is proven for a bilateral relationship and then informally extended to a many-agent setting by treating each relationship as a separate instance. The authors drop the cross-ownership case as uninteresting and treat "all residual rights to one owner" as an assumption, not a proven-optimal partition.
- **Scale and age.** No claim about headcount, budget or hierarchy depth anywhere in either source; the Rajan (2012) lifecycle remark above is the sole exception and is a citation, not a result.
- **Internal bureau behaviour.** The prison section covers the make-or-buy boundary only. Civil-service structure, agency budgeting and internal hierarchy are out of scope and must not be inferred.
- **Public "ownership" is not obviously the same object.** An agency does not own its mandate the way a firm owns a machine; residual rights are not privately transactable in a bureau, and there is no competitive market for the counterparty. The mechanism's transfer is a candidate, not a finding.

## Source

- `raw/research/incentives-and-institutional-form/04-grossman-hart-property-rights.md` — Sanford J. Grossman & Oliver D. Hart, "The Costs and Benefits of Ownership: A Theory of Vertical and Lateral Integration", *Journal of Political Economy* 94(4), 1986, 691–719. https://dash.harvard.edu/bitstreams/7312037c-527a-6bd4-e053-0100007fdf3b/download
- `raw/research/incentives-and-institutional-form/02-hart-nobel-lecture.md` — Oliver Hart, "Incomplete Contracts and Control", Nobel Prize Lecture, 8 Dec 2016. https://www.nobelprize.org/uploads/2018/06/hart-lecture.pdf

## Related

- [[governance-structures]] — Williamson's TCE is the rival account of the same phenomenon: ex post bargaining inefficiency and authority over human capital, against this page's ex ante investment distortion and control over non-human assets. The three-way reconciliation is there.
- [[rival-firm-boundary-theories]] — the open conflict between asset specificity, residual control rights, and measurement cost.
- [[multitask-incentive-theory]] — Hart's own footnote 19 routes the prison quality problem through the multitask mechanism; Holmstrom & Milgrom's Proposition 2 makes ownership an incentive instrument in the other direction.
- [[incentives-under-multiple-principals]] — Dixit reaches the same prison conclusion by a different route (constraints on appropriating cost savings), and is the only other public/private treatment in this batch.
- [[credible-commitment]] — the owner who cannot promise not to intervene is the firm-level form of the ruler who cannot promise not to expropriate; flagged as a parallel, not a demonstrated identity ([[open-questions]] Q22).
- [[transaction-costs]] — this theory sharpens generic "enforcement cost" into the contractibility/verifiability/observability distinction.
- [[what-is-an-institution]] — Hart's definition of the firm as "a bundle of non-human assets" is a fourth named rival to North's, Ostrom's and Williamson's.
- [[dimensions-of-institutional-variation]] — supplies the D25a refinement (contractibility vs. verifiability vs. observability).
- [[efficiency-of-institutions-north-vs-williamson]] — Hart's "efficiency, not ideology" is logged there as a scope-limited item on the Williamson side.
