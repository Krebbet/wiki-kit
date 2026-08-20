# Agency Costs and Ownership Structure

Jensen & Meckling's contribution is a decomposition and a pricing argument, and both are worth separating from the "nexus of contracts" slogan the paper is usually cited for. The decomposition: the cost of any agency relationship is **monitoring expenditures by the principal + bonding expenditures by the agent + residual loss**, the last being the money-equivalent of the welfare gap that survives after both parties have spent optimally on the first two. The pricing argument: as an owner-manager's equity share α falls, he bears only fraction α of the cost of any non-pecuniary benefit he consumes, so his consumption of perks rises and firm value falls — but rational outside buyers anticipate this and mark down what they pay, so the entire wealth loss is **borne by the owner-manager himself**, not captured by anyone. The same move is then run on debt: once debt is outstanding, equity is a call option on firm value, so the manager-as-equityholder captures the upside of switching to a higher-variance project while bondholders bear the downside — **asset substitution** — and again the anticipated loss is priced into the borrowing terms. Optimal ownership structure is the point that minimises the sum of the two agency-cost curves. The paper is a formal model with no test of its own predictions, and it explicitly does **not** cover the case this wiki cares most about: the very large corporation whose managers own little or no equity.

**Evidence tier note.** **(b) a formal model.** The theorem in §2.2, the option-pricing derivation in §4.1 and the agency-cost curves are proved or asserted analytically from indifference-curve and budget-constraint diagrams; none is estimated. The authors state the limit themselves: "the shape of these functions is a question of fact and can only be settled by empirical evidence... we confess that we are far from understanding the many conceptual subtleties." The paper's three pieces of cited data are **secondhand, illustrative, and test none of its own comparative statics** — Warner (1975) on bankruptcy costs (11 railroad bankruptcies 1930–1955, average 2.5% of firm value measured three years pre-bankruptcy, range 0.4–5.9%, coded from legal/professional/trustee/filing fees only and therefore an acknowledged undercount); Evans & Archer (1968) on diversification (~55% of portfolio-return standard deviation eliminated by naive equal-weighting across 40 NYSE securities); and a *Wall Street Journal* survey reporting median CEO stockholdings across 88 firms ($557,000 at year-end 1973). They anchor assumptions; they do not test predictions. **(c) wiki synthesis** is marked inline.

## The decomposition

**[model]** Agency cost = **monitoring expenditures** by the principal + **bonding expenditures** by the agent + **residual loss**. Two things about this are easy to lose:

- "Monitoring" is defined broadly in the paper's own footnote 9 to include **budget restrictions, compensation policy and operating rules** — not just observation. So a rulebook is a monitoring expenditure on this accounting, which is a different reading of the same object from [[multitask-incentive-theory]]'s (rules as a substitute for unavailable incentive pay) and from [[red-tape]]'s (rules as burden achieving nothing).
- **Residual loss is not waste anyone captures.** It is the value destroyed after both sides have already spent optimally on suppressing the problem. A diagnosis that looks for a beneficiary will not find one.

**[wiki synthesis]** This is the full formal version of the "agency costs" that [[transaction-costs]] currently names as one of three channels linking institutions to performance. That page gestures at it; this is the decomposition.

## Mechanism 1 — equity dilution

**[model]** Formalised as a theorem in §2.2. A manager who owns fraction α of the firm and consumes a non-pecuniary benefit bears α of its cost and captures all of its utility. The price at which a (1−α) claim sells settles at (1−α)V′, where V′ is post-dilution value — so the whole value decline is "entirely imposed on the owner-manager." Nobody is fooled and nobody profits; the loss is real and is borne ex ante by the person selling.

The authors flag that their formal model handles only the perk-consumption margin, and that a **second channel is probably the more important one**: as α falls, "his incentive to devote significant effort to creative activities such as searching out new profitable ventures falls." That channel is named and not modelled.

## Mechanism 2 — asset substitution under debt

**[model]** Once debt of face value X* is outstanding, equity is a **call option on firm value with strike X\*** (the Black-Scholes analogy is the paper's, not this wiki's). The manager-as-equityholder therefore has an incentive to raise the variance of the outcome distribution: he captures the upper tail, bondholders absorb the lower. The paper's own phrase is "playing poker on money borrowed... with one's own liability limited to some very small stake." Rational bondholders price this in, so again the cost lands on the issuer.

Named but not modelled: **underinvestment** in positive-NPV projects that would benefit only bondholders, cited to Myers (1977) in a footnote.

## Where optimal ownership structure comes from

**[model]** Two agency-cost curves — one rising in outside equity, one rising in debt — sum to a total that has an interior minimum. That minimum is the predicted capital structure, and the paper's insistence on calling it **ownership structure** rather than capital structure is the point: what matters is who holds the claims, not the leverage ratio as such.

The comparative statics the model implies, none tested by the authors:

- **Ease of shifting the firm's outcome distribution** — high in bars and restaurants, favouring pure debt plus 100% manager equity; high on the risk-shifting margin in conglomerates, favouring *less* debt.
- **Regulatory constraint on managerial discretion** — utilities and banks are predicted, and cited, as using more debt because regulation caps the risk-shifting margin. **[wiki synthesis]** This is the one place in the paper where an external institutional constraint enters as an explanatory variable rather than as background.
- **Cost of replacing the manager** (specialised vs. generic human capital), and **depth of the market for competing managers**.

**Levers named, all derived and none tested**: monitoring (audits, control systems, budget restrictions, incentive compensation); bonding (voluntarily audited statements, contractual limits on the manager's own discretion, explicit bonds against malfeasance); debt covenants on dividends, further issuance and working capital; incentive compensation and stock options; warrants and convertibles attached to debt, which give bondholders a share of any variance-increase upside and so blunt the substitution incentive. One lever is proposed and **explicitly not observed**: a manager holding "inside debt" in the same proportion as his inside equity (Bi/Si = Bo/So) would formally zero out his risk-shifting incentive. The authors note they have no data on whether small private firms do this and that large diffuse-ownership corporations do not, and offer only a speculative explanation.

## What the paper deliberately does not model, in its own words

**[model]** This is the section that matters most for how the wiki cites it.

- **Who holds power is not modelled.** Permanent assumption P.3 makes all outside equity **non-voting**, so the manager retains full decision rights regardless of his ownership fraction and outside claimholders have no control mechanism except price. §6.2 names this as a gap: "we have assumed that all outside equity is nonvoting... A complete analysis of this issue will require a careful specification of the contractual rights involved on both sides, the role of the board of directors, and the coordination (agency) costs borne by the stockholders in implementing policy changes."
- **The control right is named and set aside.** The right to hire and fire the manager is "at least one other right which has value which plays no formal role in the analysis as yet... we leave this issue to a future paper." **[wiki synthesis]** That deferred right is the object [[property-rights-theory-of-the-firm]] and [[formal-and-real-authority]] are both built on, and [[corporate-governance-index-and-firm-control-rights]] is the instrument that measures how far a real firm's charter has moved it.
- **The very large low-managerial-equity corporation is out of scope.** §6.6 concedes the model has not been worked out for "the very large modern corporation whose managers own little or no equity" — precisely the regime this wiki most cares about — and defers it.
- **No age claim anywhere.** The model is single-period by construction (P.6). Multiperiod dynamics — reputation reducing agency costs over an infinite horizon, then rising again near retirement in an "end game" — are sketched qualitatively in §6.1 as future work and derived nowhere.
- **One scale claim, hypothesised in a single sentence.** Fig. 7 posits total agency costs are higher for a larger firm "because it is likely that the monitoring function is inherently more difficult and expensive in a larger organization." The authors' own words are "we hypothesize." No mechanism beyond that sentence, no data.

## Two positioning moves worth recording separately from the model

**[model]** Both are argumentative rather than derived, and both are load-bearing for how the paper is read:

1. **The nexus-of-contracts definition** (§1.5): the firm is "simply a legal fiction which serves as a nexus for a set of contracting relationships among individuals," with no formal role for authority or hierarchy, and "it makes little or no sense to try to distinguish those things which are 'inside' the firm... from those things that are 'outside' of it." This is boundary-of-the-firm content and belongs with [[governance-structures]] and [[property-rights-theory-of-the-firm]], not here — recorded so it is not mistaken for this page's contribution. Gibbons's taxonomy at [[decision-rights-and-authority-theory-of-the-firm]] classifies it as the **contract branch**, the position that integration changes nothing real.
2. **The Nirvana-fallacy block** (following Demsetz 1969): the existence of positive agency costs does not license the inference that the corporate form is inefficient, because the comparison must be against a feasible alternative rather than a frictionless ideal. **[wiki synthesis]** This is the same argumentative structure as Williamson's remediableness criterion on [[governance-structures]], and it carries the same edge — it makes the observed arrangement hard to convict. Note the paper's *rejection* of the naive market-discipline story in the same section, against Friedman (1970): "If my competitors all incur agency costs equal to or greater than mine I will not be eliminated from the market by their competition." That cuts against, not for, a competition-cures-agency-costs reading.

**Generality claimed by assertion.** §1.4 states the agency problem "exists in all organizations and in all cooperative efforts — at every level of management in firms, in universities, in mutual companies, in cooperatives, in governmental authorities and bureaus, in unions..." and §1.5 lists non-profits, mutuals, cities, states, the federal government, the TVA and the Post Office as the same kind of nexus. But the derivation that follows is built entirely on **divisible salable residual claims and fixed claims** — stock and bonds — which a bureau does not have, and the paper does not attempt to re-derive the apparatus without them. Treat the breadth as an assertion in an introduction, not a finding. This is the same gap [[team-production-and-monitoring]] leaves, from the same tradition.

## Source

- `raw/research/theory-of-the-firm/02-jensen-meckling-agency-costs.md` — Michael C. Jensen & William H. Meckling, "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure", *Journal of Financial Economics* 3(4), 1976, 305–360. https://josephmahoney.web.illinois.edu/BA549_Fall%202010/Session%205/Jensen_Meckling%20(1976).pdf

## Related

- [[transaction-costs]] — this page supplies the formal monitoring/bonding/residual-loss decomposition that page names but does not decompose.
- [[team-production-and-monitoring]] — the immediately prior treatment of the same diffuse-ownership monitoring gap, which Jensen & Meckling call "too narrow".
- [[separation-of-ownership-and-control]] — Fama's answer to the same problem four years later, arguing the labour market performs the settling-up Jensen & Meckling price as a loss.
- [[corporate-governance-index-and-firm-control-rights]] — the measured instrument for the control right this paper names and defers; Gompers, Ishii & Metrick cite Jensen & Meckling as their entrenchment-camp anchor.
- [[property-rights-theory-of-the-firm]] — Grossman & Hart build the theory of exactly the residual control right deferred here to "a future paper".
- [[formal-and-real-authority]] — Aghion & Tirole model the decision rights this paper holds fixed by assumption P.3.
- [[career-concerns-and-managerial-risk-taking]] — a different mechanism for a related symptom: Holmström's distortion comes from labour-market signalling and needs no ownership stake at all; this one comes from partial ownership and needs no reputational market.
- [[multitask-incentive-theory]] — the same optimal-contracting-under-imperfect-observability family, one continuous perk margin here against a multi-task allocation problem there.
- [[incentives-under-multiple-principals]] — §6.2's dispersed-shareholder coordination cost is the un-formalised version of Dixit's noncooperating-principals result.
- [[governance-structures]] — where the nexus-of-contracts boundary material belongs.
