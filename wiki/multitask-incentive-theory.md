# Multitask Incentive Theory

When an agent's job contains several tasks that compete for the same finite attention, and only some of those tasks produce a measurable output, attaching a high-powered incentive to the measurable ones does not merely fail to help — it actively destroys effort on the rest. Holmstrom & Milgrom's multitask model (1991) makes this a formal comparative-static result: the optimal incentive weight on a measurable task falls as measurement noise on the *competing* task rises, and can optimally go to zero even for a risk-neutral agent. The design conclusion, which Holmstrom restates as the organising theme of his 2016 Nobel lecture, is the one this wiki most needs: **fixed pay, restrictions on outside activity, task-splitting by measurability, and bureaucratic rule-boundedness are the rational response to a measurement problem, not evidence of organisational pathology.** "Bringing the market inside the firm" — importing high-powered, market-like incentives into an employment relationship — is a predictable design error on this account. The theory's own authors present all of it as untested; the one substantial body of measured evidence in this batch (Prendergast's survey) confirms that incentives change behaviour but does not confirm that contracts are designed the way the theory says they should be.

**Evidence tier note.** Almost everything on this page is **(b) a formal model**. Holmstrom & Milgrom (1991) is Propositions 1–7 with proofs and no original data; the authors explicitly defer "new, testable results from the theory of organization" to a companion working paper, i.e. this paper does not claim to deliver them. Holmstrom's Nobel lecture is his own synthesis of that model plus the informativeness principle, and he flags most of it as theory ("I want to highlight two implications", not "I have shown"). The **(a) empirical** content on this page is imported from Prendergast (1999) and is clearly marked as such; where the primary sources offer real events (Wells Fargo, BP Deepwater Horizon, Atlanta Public Schools, a 1989 South Carolina teacher passing test answers) these are **illustrations chosen because they fit**, with no comparison group or base rate, and must not be cited as tests. Both primary sources are exclusively about private firms; see "What is not established" below. **(c) wiki synthesis** is marked inline.

## The baseline the multitask result overturns

**[model]** The **informativeness principle** (Holmstrom 1979, restated in both the Nobel lecture and Prendergast's survey): any signal that carries information about the agent's effort should receive positive weight in the contract. In the linear-contract version the optimal weight on a signal is *decreasing* in that signal's noise variance, *decreasing* in the agent's risk aversion, and *increasing* in the marginal return to effort. This is not "incentives matter" — it is a precise comparative static, and on a **single cleanly-measurable task it holds**. Prendergast's survey confirms it does real work: Lazear's (1996) windshield installers gained ~35% in productivity on a switch to piece rates; Paarsch & Shearer's (1996) Canadian tree planters show the same direction; McMillan, Whalley & Zhu (1989) attribute ~75% of 1978–84 Chinese agricultural productivity growth to the responsibility system granting communes a share of retained profit.

The multitask model does not deny any of that. It identifies the scope condition the single-task result was silently assuming.

## The mechanism

**[framework — Holmstrom & Milgrom 1991]** The agent chooses an effort vector `t` to maximise the certainty equivalent `CE = αᵀμ(t) + β − C(t) − ½rαᵀΣα`. The load-bearing assumption is on `C(·)`: it is strictly convex in *total* effort across tasks, so the tasks are **cost-substitutes for the agent's finite attention** — the marginal cost of effort on any one task rises with effort spent on all others.

The consequence is mechanical. Raising the incentive weight `α₁` on a measurable task lowers the agent's effective price of effort *there* relative to everywhere else, so effort reallocates toward whatever is rewarded and away from whatever is not — including the thing the principal actually cares about most. Formally (their eq. 7) `α₁*` falls as the measurement noise on the competing task rises, and can reach zero or turn negative even while the measurable task's own marginal benefit remains positive.

Three points make this stronger than a risk-sharing story:

1. **Risk aversion is not doing the work.** The muting result survives at risk-neutrality. Prendergast's restatement via Baker (1992) makes this explicit: where the objective measure loads only imperfectly onto true effort (private gaming parameter μ), the optimal piece rate is `β* = 1/(1+σ_μ²) < 1` *even under risk neutrality*.
2. **Perfect measurability is not sufficient.** Holmstrom's "second lesson" (lecture §IV.D): a *perfectly* measurable activity may still optimally get **zero** incentive power, because agents fixate on what they can control even when it is a poor proxy for value — accounting cost being the standing example.
3. **Unmeasurability of one task can zero out incentives on all of them.** As the variance on the unmeasurable task goes to infinity, "no incentive for either task is optimal" (lecture §IV.A).

**Misalignment** is treated as a separate axis from noise (lecture §IV.B): a measure `x` can be low-noise and still be the wrong quantity relative to the true objective `B`. Noise and misalignment degrade the contract by different routes.

## The seven propositions, and their evidentiary status

**[model]** Holmstrom & Milgrom derive the whole institutional apparatus from that one mechanism. Propositions 1–7, stated as the authors state them:

| # | Result | What it explains |
|---|---|---|
| 1 | Mute or zero out incentive pay when an important task is unmeasurable — holds even for a risk-neutral agent | Fixed wages; salaried employment |
| 2 | Assign asset ownership to whichever party's effort is least well measured / whose neglect the asset is most sensitive to | Employment vs. independent contracting; franchising |
| 3–4 | Restrict outside and personal activities as a **substitute** for incentive pay; the harder the inside task is to measure, the more outside activity should be excluded | Conduct rules, moonlighting bans, fixed hours |
| 5 | **Unity of responsibility** — never give two agents joint responsibility for one task | Individual accountability; a formal root for hierarchy |
| 6–7 | Group hard-to-measure tasks onto one worker and easy-to-measure tasks onto another, **even for ex ante identical workers** | Specialisation by measurability, not by talent |

**All seven are untested, by the authors' own account.** The paper's empirical content is two motivating anecdotes (the 1989 South Carolina teacher who passed test answers to raise scores; the general controversy over teacher pay-for-test-scores) and post-hoc citation of *other people's* prior cross-sectional work — Anderson (1985) and Anderson & Schmittlein (1984) on electronics sales-force integration, Krueger (1991) and Brickley & Dark (1987) on franchise royalty structures. The authors call their own job-design model "a first pass" and list what it omits (variable task size, correlated measurement errors, task complementarities, job rotation). They note that the Anderson/Schmittlein correlation is **equally consistent with two competing explanations from inside their own theory** (asset/goodwill transfer vs. exclusion of outside activities) — so it does not discriminate even on its own terms. Holmstrom's lecture reaches the same accounting: the employment-versus-contracting prediction is the single empirically-grounded claim in it, and it rests on that same study.

## Why bureaucratic rule-boundedness is a design response, not a pathology

**[model]** This is the result with the largest reach beyond the employment dyad, and it is asserted rather than modelled at the organisational level, so state it carefully. Holmstrom & Milgrom §4: "the rigid rules and limits that characterize bureaucracy... constitute an optimal response to difficulties in measuring and rewarding performance." The bureaucrat on a fixed wage with a thick rulebook is not a failure of design; low-powered pay plus behavioural constraint is what the model prescribes when the important output is unmeasurable, because the constraint controls behaviour on dimensions money cannot price. Holmstrom's lecture generalises the same substitution: firms use job design, task bundling, restrictions on outside activity, career-visibility management and mission statements *instead of* pay, and the strength of the constraint moves inversely with the strength of the monetary incentive.

**[empirical — Prendergast 1999]** Prendergast derives a second, independent route to the same institutional form. Where the *subjective* signal is itself corruptible by costly influence activity (cost `κb²/2`), the optimal weight on that signal also falls below one (his eq. 19–20) — literally deriving seniority promotion, fixed pay bands and minimum time-in-grade as the firm's optimal response to **rent-seeking**, trading ex post allocative efficiency for reduced lobbying. Note the evidentiary status Prendergast himself puts on it: he calls the influence and bureaucracy models "not meant to be a detailed description... instead illustrative" (fn. 26), and the only support offered is descriptive (Freeman & Medoff 1984: 42% of nonunion firms lay off by seniority alone) plus a single anecdote about an unnamed US economics department's publication-count tenure rule. So there are **two distinct formal mechanisms producing rule-boundedness — unmeasurability and influence-cost — and neither has been tested.**

**[wiki synthesis]** These two mechanisms are not the same claim, and the wiki should not merge them. The first says rules exist because output cannot be priced; the second says rules exist because the evaluator can be lobbied. They make different predictions about what happens when measurement improves: the first predicts rules recede, the second predicts they persist as long as evaluation is discretionary.

## "High-powered incentives: good or bad?" is a scope question, not a conflict

**[wiki synthesis]** This wiki deliberately does **not** file the apparent contradiction between the informativeness principle and the crowding/multitask results as a conflict. It resolves by scope, and both sides state the scope condition themselves:

- **Single, clean, essentially one-dimensional measure** → the informativeness principle holds and is empirically supported. Prendergast's own caution is that this is exactly where nearly all positive evidence comes from — windshield installers, tree planters, jockeys, CEOs priced by the stock market, Chinese farmers — "most people don't work in jobs like these."
- **Multiple tasks, only some measurable** → the multitask mechanism bites: rewarded effort crowds out unrewarded effort through the agent's attention constraint. Failure mode: **measurement gaming / goal displacement**.
- **Task where the agent's own motivation is doing the work the measure cannot** → a second and *independent* mechanism bites, by which the reward damages the disposition rather than redirecting the effort. See [[motivation-crowding]].

Multitasking and crowding are therefore two different mechanisms by which the *same* intervention backfires, running through different channels — attention reallocation versus a change in the agent's beliefs or self-perception — once measurability or perceived valence breaks down. Neither denies the baseline result inside its own scope. Filing this as a conflict would be filing a scope condition as a contradiction.

## Failure modes named

**[framework, with illustrations only]** Measurement gaming and outright fraud (Wells Fargo shell accounts; the South Carolina teacher; the Atlanta Public Schools cheating scandal, framed through Kerr 1975's "folly of rewarding A while hoping for B"); goal displacement through misalignment of measure and value; **asset abuse and undermaintenance** where output is rewarded and asset care is not; accounting manipulation; intertemporal shifting of sales across fiscal boundaries (Healy 1985; Oyer 1998); **influence activities and pandering** under career concerns (Milgrom & Roberts 1988; Prendergast 1993's "Yes Men"); short-termism from too-short vesting. Every one of these is named by the sources as a *model implication with a matching anecdote*, not as a measured effect.

## Selection versus incentive effects

**[empirical — Prendergast 1999]** Both primary sources on this page are **silent on selection**. Holmstrom & Milgrom's agents are explicitly "identical ex ante"; the entire apparatus holds the agent's identity fixed and varies the contract; there is no adverse selection, self-selection or screening anywhere in the model. Holmstrom's lecture is a moral-hazard setup by construction, with types symmetrically known at contracting. **No claim that incentive structures change *who* ends up inside an institution is supported by either source**, and their authority must not be allowed to bleed into such claims.

The decomposition exists, and it comes from one place — Prendergast's survey, which flags the distinction as underappreciated: "the selection effects appear to be of roughly equal size to the incentive effects, despite the overwhelming focus on incentive effects in the theoretical literature."

- **Lazear (1996), windshield installers.** Of the ~35% productivity rise after the piece-rate switch (wages +12%), roughly **one third is selection** — turnover data show the less able left and more able workers replaced them. This is the cleanest decomposition in the batch.
- **Paarsch & Shearer (1996), Canadian tree planters.** Structural estimation isolates the incentive effect on a *given* worker at ~10%, against a raw 35% productivity gap that is contaminated by selection.
- **Banker, Lee & Potter (1996), retail stores.** Store-level rather than individual data — Prendergast flags it as *unable* to separate the two. A standing caution against reading firm-level productivity comparisons as tests of incentive theory.
- **Theory (Lazear 1986 lineage).** Higher piece rates raise the ability threshold at which the job is worth accepting, so pay-for-performance is disproportionately attractive to more able workers.
- **Weiss (1987) / Hansen (1997), team pay.** Selection is **U-shaped**, not monotonic: medium-ability workers stay, while both the most able (who dislike free-riding) and the least able (who find peer pressure costly) leave. Layered underneath is a *negative-slope* incentive effect — holding identity fixed, more productive individuals reduce output under team pay and less productive ones raise it.

**[wiki synthesis]** This bears directly on [[open-questions]] Q4 — whether institutional behaviour is better predicted by formal structure or by who ends up inside. The honest position is that the wiki now has one source that measures the split, in two occupations, both with unusually clean output measures. That is a datapoint, not an answer.

## The overall empirical verdict from inside the paradigm

**[empirical — Prendergast 1999]** Prendergast separates two claims that are routinely run together, and grades them differently. "Do incentives matter" is well supported. "Are contracts designed as agency theory predicts" is not: he calls the executive-pay-levels literature "a poor method of testing agency theory," reports that relative performance evaluation has mixed-to-absent empirical support (Gibbons & Murphy 1990 confirm it for executives but against the whole market rather than industry peers; Aggarwal & Samwick 1998, Barro & Barro 1990, Blackwell et al. 1994 and Janakiraman et al. 1992 find little), flags the efficiency-wage tests as possibly unfalsifiable with available methods, and closes: **"the available empirical evidence on contracts does not yet provide a ringing endorsement of the theory."** He attributes much of this to data limitation rather than to the theory being wrong, and the wiki should preserve that hedge rather than flattening the verdict in either direction.

One further puzzle he names against his own paradigm: the "N−1 problem" predicts individual incentive under profit-sharing should vanish as team size grows, yet company-wide profit sharing consistently shows ~4–5% productivity gains even in firms with thousands of workers. Peer monitoring, sorting and income effects are offered as competing explanations, all untested.

## What is not established

- **Nothing here is tested on a public bureau.** Holmstrom & Milgrom claim coverage of "bureaucratic constraints" in their introduction, but every worked example and every cited study is a private firm or contractor: home remodelling, manufacturing piece rates, electronics sales forces, McDonald's and Burger King franchising, freelance versus staff writers. "Bureaucracy" appears only as interpretive analogy in §4. Holmstrom's lecture does not discuss public bureaus at all — the Atlanta schools case treats teachers as employees of a district, with no political principals, no multiple overseers, and no absence of residual claimancy. The public-sector transfer is carried in this wiki by a different source: [[incentives-under-multiple-principals]].
- **Nothing here is a scale or age claim.** The nearest thing is a static 1-vs-2-agent comparison: adding a second agent to a task carries a fixed incentive cost, which Holmstrom offers as a possible rationale for unity of command. Holmstrom & Milgrom assert once (§3.2) that "piece rate schemes may be especially dysfunctional in large hierarchies" — asserted, not modelled, with no threshold. Do not read "firms use bureaucratic rules" as a statement about what happens as firms grow. Neither source mentions organisational age.
- **No account of who selects or removes the principal.** The principal is an unexamined unitary actor with unquestioned authority to set the contract. There is no board, no ownership diffusion, no accountability structure above the dyad.
- **The lecture's generalisation from dyad to firm architecture is done by analogy**, not by formal argument. Any use of this material above the level of a single employment relationship is an extrapolation the sources do not themselves perform.

## Source

- `raw/research/incentives-and-institutional-form/01-holmstrom-nobel-lecture.md` — Bengt Holmström, "Pay For Performance and Beyond", Nobel Prize Lecture, 8 Dec 2016. https://www.nobelprize.org/uploads/2018/06/holmstrom-lecture.pdf
- `raw/research/incentives-and-institutional-form/03-holmstrom-milgrom-multitask.md` — Bengt Holmstrom & Paul Milgrom, "Multitask Principal-Agent Analyses: Incentive Contracts, Asset Ownership, and Job Design", *Journal of Law, Economics, & Organization* 7 (Special Issue), 1991, 24–52. https://www.sfu.ca/~allen/HolmstromMilgrom.pdf
- `raw/research/incentives-and-institutional-form/05-prendergast-incentives-firms.md` — Canice Prendergast, "The Provision of Incentives in Firms", *Journal of Economic Literature* 37(1), 1999, 7–63. http://qed.econ.queensu.ca/pub/faculty/ferrall/econ861/papers/prendergast.pdf

## Related

- [[incentives-under-multiple-principals]] — Dixit runs this same model with public-sector parameter values and gets bureaucratic form out of it; the only source in this wiki that applies the mechanism to a bureau rather than asserting it transfers.
- [[motivation-crowding]] — the second, independent mechanism by which a high-powered incentive backfires; distinguished from multitasking on this page because it runs through the agent's disposition rather than through an attention constraint.
- [[property-rights-theory-of-the-firm]] — Holmstrom's closing position is that incentive-contract theory and property-rights theory are complementary; Proposition 2 makes ownership an incentive instrument, which is where the two meet.
- [[governance-structures]] — measurement cost is offered by Holmstrom & Milgrom as a rival to asset specificity as the determinant of integration; the three-way reconciliation lives there.
- [[rival-firm-boundary-theories]] — the open conflict that rivalry generates.
- [[dimensions-of-institutional-variation]] — supplies D49 (task substitutability in the agent's effort constraint) and refines D25; also the two axes rejected on measurement grounds.
- [[transaction-costs]] — measurement cost of *performance* is a distinct category from transaction cost of *exchange*; this page supplies the formal version of the former.
- [[bureaucratic-growth-and-parkinsons-law]] — the contrasting reading of rule-boundedness and headcount as pathology rather than as design; the tension is recorded at D9.
- [[efficiency-of-institutions-north-vs-williamson]] — Prendergast's "not a ringing endorsement" verdict is logged there on the North side.
- [[open-questions]] — Q4 (selection vs. structure) turns on the Lazear/Paarsch-Shearer decompositions recorded here.
