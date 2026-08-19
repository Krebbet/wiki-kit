# Career Concerns and Managerial Risk-Taking

Holmström's result is the sharpest thing in this batch: **a risk-neutral manager will behave as if risk averse**, with no risk preference assumed anywhere in the model. The mechanism is reputational. A competitive labour market cannot observe the manager's ability, so it infers it from observed performance and prices him accordingly. Investment projects are therefore not just projects — they are *tests of talent*. A manager facing a project whose outcome would cleanly reveal his ability will decline it, or prefer a project "protected by exogenous reasons for investment failure", because a revealed failure permanently lowers the market's assessment and hence his future wage. Positive-NPV, ability-revealing projects get suppressed. In the paper's sharpest example — an explicit Akerlof lemons construction — when the manager's private investment information cannot be verified, the *only* equilibrium is one in which **no investment happens at all**. Holmström's own summary: "if the manager cannot have his investment information validated it makes him more conservative. Even a risk neutral manager acts as if he is risk averse in this example."

**Evidence tier note.** (b) **Formal deductive model only** — Gaussian Bayesian learning plus two illustrative numerical examples with closed-form equilibria. There is essentially no empirical content. The single empirical citation (Medoff & Abraham 1980 on age and productivity) supports the *work-incentive* half of the paper, is hedged by Holmström himself as "not overwhelmingly strong", and does not bear on the risk-taking claims at all. **The risk-aversion phenomenon itself is never demonstrated in this paper — it is asserted as a stylised fact ("firms frequently express a concern over the way their management takes risks"; young managers "seen as overly risk-averse", uncited) that the model is then built to explain.** Strongest content: the internal consistency of the worked examples and the lemons parallel. Holmström is restrained about all of it — the examples are "anything but general themselves", and the conclusions "raise rather than answer questions".

## Why the mechanism produces timidity

**[model]** The manager's wage in each period is the market's current expectation of his ability, updated by Bayes from observed output. Output is ability plus effort plus noise. Two consequences:

1. **Effort.** Career concerns alone, with no explicit contract, induce positive effort — current output shifts beliefs and hence future wages. But the effort is generally *inefficient*, which directly refutes Fama's (1980) claim that reputation alone suffices to police moral hazard. Holmström: "Under some narrow assumptions I show that Fama's conclusion is correct. In general, however, it is not."
2. **Risk.** Because output is a signal about ability, the manager's payoff is asymmetric in the *informativeness* of the project, not in its expected value. A project that would resolve uncertainty about him is worse for him than an equally profitable project that would not, whatever its NPV. He therefore prefers noisy projects and can profitably claim "that no worthwhile investment opportunity was present" — a clean formal channel from an individual career incentive to firm-level under-investment and capital misallocation.

**[model — career stage]** The age dynamic in the paper is the *individual's* career age, not the institution's. Reputation-building returns are "bigger the more there is uncertainty about ability", i.e. largest early. In the non-stationary case effort declines over a career toward zero as ability becomes known (Proposition 1). In the stationary case (ability itself drifts) effort converges monotonically to a level below efficient, approaching from above or below depending on whether initial precision h₁ is under or over the stationary precision h*; Holmström argues h₁ < h* is the common case, predicting young managers "overinvest in labor supply" and taper (Proposition 2). **For risk-taking specifically no career-stage comparative static is derived** — the claim that the young are the most timid is the paper's motivating stylised fact, not a result.

## Holmström explicitly rejects the size-based account

**[model — and the most important sentence on this page for the wiki's framing question]** The competing explanation of managerial risk attitudes available in 1982 was the Wilson (1968) / Ross (1973) **risk-bearing-capacity** story: a manager in a small firm must absorb real risk, so contracts must be built to make him accept it. Holmström considers this and dismisses it. In "a firm of even modest size or in a publicly held corporation, gains from having the manager carry some risk are certainly negligible" — the firm can simply pay a constant wage and "there really is no incentive problem in the first place."

Two things follow, and they are separable.

- **A size-based account of managerial risk aversion is rejected by name, for firms above modest size.** This is a direct disconfirming argument against the risk-bearing-capacity route from institutional size to risk-averse behaviour. It is (b) an argument inside a model, not an empirical refutation, but it comes from inside the literature that would otherwise be cited for the size claim.
- **Holmström's own mechanism is structurally size-invariant.** Career concerns operate through the *external* labour market. They apply to a manager in a firm of any size, provided an external market reprices him on inferred ability. Size is not a parameter; the model would run identically at n = 50 and n = 50,000.

## The dimensions this model supplies

**[model]** All at the level of the individual contracting relationship, not the organisation.

- **Verifiability of the agent's private information** — the sharp one. When investment-relevant private information cannot be verified or contracted on, the problem does not worsen at the margin; it collapses to the degenerate zero-investment equilibrium. Distinct from measurability of *output*: this is measurability of what the *agent knows*. Registered as [[dimensions-of-institutional-variation]] D47.
- Precision of market beliefs about ability, and its updating path (h_t).
- Ratio of output noise to ability-drift noise (r = σ²_δ/σ²_ε) — sets how fast and how completely reputation effects decay.
- Convexity vs. concavity of payoffs in perceived ability — sets the *direction* of the distortion, over- or under-investment.
- Implicit vs. explicit contracting: wages set by ex-post market inference against output-contingent contracts.

## Levers, all hedged by the author

**[model / speculation]** Convex payoffs — stock options removing the downside — are proposed as a realignment and explicitly **not** verified: "verification of its validity has to await a more careful analysis." Making the agent's private information verifiable reduces (does not eliminate) the problem, implied by the contrast between the two examples rather than modelled as a policy. And one aside worth quoting because it is the only bridge in the paper from an individual model to institutional design, and Holmström flags it himself as outside the model: detailed centralised investment-approval procedures inside firms may exist partly to secure a *proper evaluation of managerial talent*, not only to control which projects are chosen. He introduces it with "I note in passing". Do not upgrade it to an evidenced claim.

## What this model is not evidence for

**[wiki synthesis — gaps]**

- **It evidences individual-agent risk aversion, not organisational risk aversion.** The unit of analysis is one manager. The "firm" is a passive risk-neutral wage-setter with no board, no hierarchy, no departments. Aggregation from many career-concerned agents to an institution that behaves cautiously is a step the paper does not take and does not license.
- **The public-sector application is asserted by generality of framing, and may be narrower, not wider.** The model is written sector-agnostically and Holmström extends his dismissal of risk-bearing-capacity to "a publicly held corporation". But the engine is a *competitive market for the role*. Where there is no such market — tenured civil-service posts with weak external repricing — it is not clear the mechanism runs at all. That would make the model *less* applicable to public bureaus than to firms, cutting against naive invariance. Unaddressed by the source. See [[open-questions]] Q3.
- **None of the classic organisational failure modes appear**, because there is no organisational level: no capture, no ossification, no veto-point proliferation, no credentialism, no mission creep. Do not attribute them to Holmström.
- **No country, sector, period, or dataset.** Written 1982, published 1999 essentially unrevised, inside the 1970s–80s agency-theory canon.

## Source

- `raw/research/risk-aversion-in-large-institutions/03-holmstrom-career-concerns.md` — Bengt Holmström, "Managerial Incentive Problems: A Dynamic Perspective", 1982; NBER Working Paper 6875 (1999) / *Review of Economic Studies* 66(1). https://www.nber.org/system/files/working_papers/w6875/w6875.pdf

## Related

- [[risk-aversion-in-large-institutions]] — the umbrella page; this source supplies both a mechanism and the batch's one explicit rejection of a size-based account.
- [[exploration-exploitation-incentive-contracts]] — the other formal model in the batch, and the closer relative: Manso likewise derives timidity for risk-*neutral* agents, from contract design rather than from labour-market inference.
- [[blame-avoidance-and-negativity-bias]] — the same payoff asymmetry in narrative form, with an electorate and a legislature in the role Holmström gives the labour market.
- [[isolation-errors-and-portfolio-framing]] — the contrast is instructive: Kahneman & Lovallo need loss aversion in the agent's utility, Holmström needs none.
- [[transaction-costs]] — this is a canonical formal treatment of the agency-cost limb that page names as a channel from institutions to economic performance.
- [[governance-structures]] — complementary and non-overlapping levels: TCE works at the organisational boundary, this at the individual agent inside a given firm with no boundary question in view.
- [[dimensions-of-institutional-variation]] — supplies D47 (verifiability of an agent's private information).
- [[open-questions]] — Q3, Q30, Q32 (does an aggregation from individual career concerns to institutional behaviour exist).
