# Corporate Governance Index and Firm Control Rights

Gompers, Ishii & Metrick hand-code **24 shareholder-rights and takeover-defence provisions** — from each firm's own charter and bylaws plus the takeover statutes of its state of incorporation — into a single additive 0–24 "Governance Index" (G) for **~1,500 US public firms per year, 1990–1999**. High G means management is insulated from removal by its nominal owners. The correlations are large: a portfolio long the strongest-shareholder-rights firms (G ≤ 5) and short the most management-insulated (G ≥ 14) earns a four-factor alpha of 71 basis points a month, **≈ 8.5% per year**; a one-point increase in G is associated with a **2.4 percentage-point lower Tobin's Q in 1990, widening to 8.9 percentage points by 1999**; high-G firms show lower profit margins and sales growth and higher capital expenditure and acquisition activity. **The authors explicitly refuse a causal reading of any of it** — "we make no claims about the direction of causality between governance and performance" — and their entire concluding section sets out three rival causal stories, all of which predict the same correlations and none of which their design can separate. That refusal is not a caveat attached to the findings; it is what the paper concludes, and citing the 8.5% without it misreports the source. For this wiki the instrument matters more than the result: it is the first thing the wiki holds that **scores an individual institution from its own constitutive documents**.

**Evidence tier note.** **(a) empirical, observational, cross-sectional and panel** — not experimental. Governance structure is not randomly assigned, and the authors say so: "the governance structures of a firm are not exogenous, so it is difficult in most cases to draw causal inferences." **Strongest**: the index construction itself — transparent, hand-coded from primary documents, reproducible — and the return and valuation regressions, robust across value-weighted, equal-weighted, industry-adjusted, Delaware-only, fixed-1990-portfolio and split-sample specifications. **Weakest**: the provision-level regressions (16 of 24 coefficients negative, only "silver parachutes" individually significant, which the authors attribute to multicollinearity plus expected false positives — "with this many regressors, we would expect one to be 'significant' just by chance"), and the takeover-probability regression, where G's coefficient is positive but insignificant. Note an asymmetry the wiki should carry: **the abstract and introduction lead with the return and valuation findings and read causally in isolation; the conclusion is far more hedged.** Cite the conclusion.

## The instrument: 24 provisions

**[empirical]** One point per provision that **restricts** shareholder rights — or, for the two reverse-coded items, per provision *absent* that would have increased them. Simple unweighted additive count, 0–24. Observed range in sample: **2 to 18**, mean ≈ 9, SD ≈ 2.8–2.9.

Grouped by the mechanism through which each shifts real control from the nominal principal to incumbent management:

| Mechanism | Provisions |
|---|---|
| **Delay board turnover** | Classified/staggered board — only part of the board turns over each year, so a new controlling shareholder waits multiple cycles; also deters proxy contests, fewer seats being contestable per cycle |
| **Block control transactions outright** | Poison pill (dilutes an unapproved acquirer unless the incumbent board redeems it); business-combination laws (3–5 year moratoria once a stake threshold is crossed); control-share acquisition and control-share cash-out laws |
| **Raise the threshold to act** | Supermajority merger requirements (66.7 / 75 / 85%, above state defaults); fair-price requirements; bylaw amendment limitations; charter amendment limitations |
| **Block shareholder coordination outside the annual meeting** | Limitations on calling special meetings; limitations on action by written consent |
| **Compensate incumbents for losing** | Golden parachutes; silver parachutes; executive severance agreements; compensation plans with change-in-control acceleration; pension parachutes |
| **Insulate individuals from legal accountability** | Director/officer indemnification (bylaw or charter); director indemnification contracts; limitations on director liability |
| **Widen the legal warrant for refusing a bid** | Directors'-duties provisions and laws — boards may weigh employees, communities and suppliers when rejecting a value-increasing offer |
| **Other** | Blank check preferred stock; unequal voting rights; antigreenmail (ambiguous — removes a raider's exit route *and* a managerial tool) |
| **Reverse-coded (+1 if absent)** | Cumulative voting; secret/confidential ballot — both, per the authors' correlational check, originate from shareholder pressure rather than management |

**Sources per provision**: the authors hand-coded from IRRC's *Corporate Takeover Defenses* (Rosenbaum, editions 1990/1993/1995/1998), which itself compiles from **corporate bylaws and charters, proxy statements, annual reports and 10-K/10-Q filings**; state-law incidence from a separate IRRC publication (Pinnell 2000, *State Takeover Laws*), covering six "second-generation" statute types, with firm-level opt-out and opt-in status coded too. Two items (business-combination and control-share cash-out) have **no firm-level analogue** and are coded purely from state law.

**Limitations the authors state themselves**: all 24 provisions are weighted equally by construction — "such a simple weighting scheme... makes no attempt to accurately reflect the relative impacts of different provisions," defended on transparency and reproducibility grounds; provisions are coded present/absent with **no strength gradation** (a 66.7% and an 85% supermajority threshold both score 1); IRRC does not re-verify every company at every edition; for some companies "the charter and bylaws are not available and most provisions must be inferred from proxy statements and other filings"; and the whole listing is "a noisy measure... not the final word," though they see "no reason to suspect any systematic bias."

**Provisions cluster within firms.** Of the 276 pairwise provision correlations, **199 are positive (120 significantly so) against 77 negative (20 significantly)** — which is the stated reason for building one additive index rather than treating provisions independently.

## The results

**[empirical]** Sample: September 1990 – December 1999, ~1,500 firms/year (1,357 in 1990; 1,343 in 1993; 1,373 in 1995; 1,708 in 1998 — the jump reflects IRRC expanding its universe toward lower-G firms), covering **over 93% of combined NYSE + AMEX + Nasdaq market capitalisation** even at the 1990 start. Dual-class firms excluded (<10% of the universe). Refreshed only at the four IRRC publication dates, so roughly **triennial, not annual**. ~47% Delaware-incorporated.

| Result | Magnitude |
|---|---|
| $1 in the value-weighted **Management Portfolio** (G ≥ 14), 9/1990 → 12/1999 | $3.39 (14.0%/yr) |
| $1 in the **Shareholder Portfolio** (G ≤ 5) | $7.07 (23.3%/yr) |
| **Four-factor (Carhart) alpha on the Shareholder-minus-Management spread** | **71 bp/month ≈ 8.5%/yr**, significant at 1% |
| Components | Shareholder +29 bp/month; Management −42 bp/month, both significant |
| Rank correlation, G-decile against decile alpha | 0.842, rejected at 1% |
| Robustness alphas | equal-weighted 45 bp; industry-adjusted 47 bp; fixed-1990 portfolio 53 bp; Delaware-only 63 bp (t = 1.88); first half 45 bp, second half 75 bp — **not driven by the late-1990s tech run** |
| **Tobin's Q, per one-point rise in G** | **−2.4 pp in 1990, widening to −8.9 pp by 1999**; negative every year, significant in 8 of 10; Delaware-only subsample larger still (−3.4 pp → −10.9 pp) |
| Operating performance, high-G firms | Lower net profit margin, lower sales growth; ROE insignificantly lower |
| Investment behaviour, high-G firms | **Higher** capex (per sales and per assets); **1.04 vs 0.64** acquisitions/year and a **4.93% vs 2.78%** acquisition ratio (Management vs Shareholder Portfolio), controlling for size, book-to-market and 48 industry dummies |

Note that the **continuous** G coefficient in the full-sample return regression is negative but *insignificant* (≈ −4 bp/month per point): the effect is concentrated in the extreme deciles, not linear across the range.

**[wiki synthesis]** The capex-and-acquisitions result is the one with reach beyond finance. It is the empire-building prediction of [[agency-costs-and-ownership-structure]] and of the free-cash-flow tradition, measured on a control-rights variable rather than assumed. It is also, in the other direction, evidence *against* the reading that entrenchment shows up as passivity: insulated management here does **more**, not less. Compare [[bureaucratic-growth-and-parkinsons-law]], where growth without a demand signal is the diagnostic of interest — this is the private-sector analogue with the insulation variable actually measured.

## The three causal stories, and why the refusal belongs in the headline

**[empirical]** The authors set out three explanations, all consistent with every correlation above, and adjudicate none:

1. **Direct causation** — provisions cause higher agency costs; entrenched management makes worse decisions; the market did not price this in 1990, producing "surprise" underperformance as it became apparent through the decade.
2. **Defensive foresight** — prescient managers who foresee poor performance install provisions to protect themselves from the consequences. The provisions have no causal power over performance, only over who gets fired.
3. **Signal, not source** — provisions are a symptom of pre-existing agency costs, "like a 'beware of dog' sign." Banning the sign would cause firms to signal otherwise, with zero effect on true agency costs.

**The lever this licenses is conditional, and only conditional.** The authors write: "If this causal explanation is correct, then the policy implication is clear: a reduction of provisions and decrease in managerial power would decrease agency costs and increase shareholder wealth" — and give equal narrative weight to stories 2 and 3, under which stripping provisions would do nothing (3) or would only raise management turnover (2). So: **tier (a) evidence for the correlation, no evidence at all for the antecedent the lever needs.** Endogeneity concerns the authors raise themselves: provision adoption may itself respond to perceived takeover threat; and they cannot replicate Comment & Schwert's (1995) two-step correction for adoption endogeneity because their provision-timing data are too coarse (four editions in ten years).

**[wiki synthesis]** This is the firm-level twin of the identification problem that occupies [[does-institutions-growth-survive-identification]] at country level, and it is instructive precisely because the instrument here is *better* — hand-coded from primary documents, one score per organisation, not a perceptions index — and the causal problem is **unchanged**. Better measurement does not buy identification. That is worth stating explicitly, because the wiki's frustration with country-level scalars could otherwise be mistaken for the belief that institution-level measurement would settle causal questions. It would not.

## The slow-moving constitution

**[empirical]** Mean absolute change in G between IRRC publication dates is **0.60 points; median change is zero.** The authors invoke this explicitly as a "slow-moving constitution" — distinct from faster-adjusting governance channels like board composition, CEO pay or shareholder activism. Once a firm's control-rights structure is set, it barely moves.

**Where it came from.** Most firm-specific variation in G results from provisions adopted, and state laws passed, in **the second half of the 1980s in reaction to the hostile-takeover wave**. G is therefore measuring the residue of a specific regulatory and market-structure episode. Its relevance to other periods, other countries, or post-2000 US firms (index compression, say-on-pay, majority voting, activist campaigns) is not addressed by the paper and should not be assumed.

**Firm size and age are covariates, not objects of study.** Both are controlled for in the Q regressions (log book assets, log firm age); no coefficient on age is reported and **no claim is made anywhere about how G, or the G–performance relationship, varies with size or age.** That is a gap, not a finding, and this source supplies no scale or age reading.

## Portability: scoreable tomorrow, and where it stops

**[empirical, with the extension marked as this wiki's inference]** The core index needs only (a) the organisation's own **charter and bylaws**, and (b) knowledge of its **state of incorporation's antitakeover statutes** and whether it has opted in or out. Both can be read directly for one company by one analyst. IRRC itself sourced from exactly those documents plus proxy statements and 10-K/10-Q filings; the paper's Appendix B reproduces GTE Corp's actual IRRC profile pages for 1990 and 1998 as a worked template.

- **Not needed to score G**: public trading, market prices, CRSP/Compustat. Those are needed only to test what G *predicts*.
- **Lost by a lone analyst**: IRRC's cross-checking against proxy statements and 10-Ks, which catches provisions not visible in charter/bylaw text alone. The state-statute research is a fixed look-up cost, not a recurring one.
- **[wiki synthesis] The real dependency, and the honest limit on generalisation.** The instrument depends on the existence of *a settled taxonomy of control-shifting provisions recognised in a body of law and market practice* — US corporate and takeover law circa 1990. Applying the same coding logic to another jurisdiction or another entity type (a nonprofit's bylaws and board-composition rules, a private company's shareholders' agreement, an agency's enabling statute) would require **first building that taxonomy**, which is a non-trivial prior step this paper does not attempt and does not claim is easy. The underlying logic — enumerate the provisions that shift control away from the formally sovereign principal, and sum them — has no principled dependency on public listing; the dependency is on documents existing and on a defined principal whose formal rights the provisions restrict. Registered as [[dimensions-of-institutional-variation]] **D110**, `promoted`, **with that limitation inside the row.**

## Source

- `raw/research/theory-of-the-firm/07-gompers-ishii-metrick-governance-equity.md` — Paul A. Gompers, Joy L. Ishii & Andrew Metrick, "Corporate Governance and Equity Prices", NBER Working Paper 8449, August 2001 (published *Quarterly Journal of Economics* 118(1), 2003). https://www.nber.org/system/files/working_papers/w8449/w8449.pdf

## Related

- [[dimensions-of-institutional-variation]] — supplies **D110** (management-insulation / control-rights allocation), the register's first document-scoreable institution-level axis, gated by D90.
- [[world-management-survey]] — the batch's other institution-level instrument, with the opposite portability profile: a live respondent instead of a document, and therefore a different failure mode.
- [[agency-costs-and-ownership-structure]] — the theoretical anchor the authors cite for the entrenchment reading, and the source of the empire-building prediction the capex and acquisition results bear on.
- [[separation-of-ownership-and-control]] — this instrument measures how far a real firm's charter has insulated management against exactly the board-and-vote channel Fama argues is sufficient.
- [[team-production-and-monitoring]] — Alchian & Demsetz's claim that discipline runs through the *capitalization* of expected improvement into share price is what the takeover defences here obstruct.
- [[formal-and-real-authority]] — every provision is a device for widening the gap between formal principal and real decision-maker without changing who nominally holds the vote.
- [[governance-structures]] — Rajan & Wulf use this same index to test and reject an empire-building account of hierarchy depth, which is the one place the wiki already cites it.
- [[weberian-structure-and-growth]] — a methodological parallel only: an additive itemised checklist as the way to turn a qualitative governance concept into a comparable scalar, there at country level via 126 experts, here at firm level from documents.
- [[does-institutions-growth-survive-identification]] — the same correlation-versus-identification problem at country scale; the contrast is the point.
- [[open-questions]] — Q110 (whether the G logic can be rebuilt for another entity type) and Q114.
