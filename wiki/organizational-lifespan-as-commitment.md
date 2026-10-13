# Organizational Lifespan as Commitment (Foundations)

Jaag (arXiv 2610.08447, Oct 2026) models an organisation's own lifespan as a founder's commitment choice among perpetuity, a fixed sunset date, and open-ended discretion, and shows each regime is optimal somewhere. Perpetuity raises investment in sunk, organisation-specific capital (expertise, reputation, networks); a sunset limits controllers' entrenchment; discretion preserves the option to stop when learning is informative. **Treat as a formal existence result about a design margin, not as evidence about how institutions behave:** the source is an un-refereed preprint with no data, and its entrenchment term is constant in age.

**Evidence tier note.** Entirely (b): a formal model with closed-form propositions, no calibration, no empirical test, no data of its own. It cites descriptive and practitioner literature on sunset foundations but does not test against it. Status: **un-refereed arXiv preprint**; the author is affiliated with a Swiss foundation (a possible practitioner perspective) and declares ChatGPT use to review derivations. **The model has no age-dependent entrenchment** (the private survival benefit d is a constant, not a function of elapsed age), so it cannot be cited for or against age-driven decay.

## The model

**[model]** A founder at date 0 picks a lifespan rule for a philanthropic foundation. Three regimes: perpetual P (no voluntary termination while solvent), spend-down S(T) (terminate after T periods), open-ended N (future boards decide). Two opposing commitment problems:

- **Hold-up under discretion.** Investment in organisation-specific capital is made before the state of the world is observed. Under N, a board that can stop later does not internalise that the prospect of stopping lowered the earlier return to the sunk capital. Optimal investment is e*_P = eta/c under perpetuity versus e*_N = p*eta/c under discretion (p is the probability of the good state).
- **Overcontinuation.** Future controllers get a private survival benefit d (jobs, prestige, control) and continue when social continuation value C_soc + d >= 0, so they keep the organisation alive after social value turns negative. A terminal date caps this.
- **Learning favours flexibility.** Proposition 4: a more informative signal about future continuation values raises the value of discretion.

Assumptions: a two-state specialisation (z_H > 0 > z_L), quadratic investment cost, linear return; state observed only after investment is sunk; d is a reduced-form wedge, exogenous and excluded from social welfare; capital is lost on termination and persists at rate q in the finite-horizon extension; an aligned founder or planner designs the rule.

**[model]** Results:

- **Lemma 1.** With aligned governance and no behavioural response, N weakly dominates both commitments. Commitment is only valuable because of the two problems above.
- **Proposition 1.** With aligned governance, perpetuity beats N iff eta > eta_P = sqrt(-2c*z_L/(1+p)); the gap is W*_P - W*_N = (1-p)[z_L + (1+p)eta^2/2c].
- **Proposition 2.** A unique finite optimal sunset T* exists under strong survival bias, provided the social value sequence is eventually decreasing with negative limsup and a single-crossing condition holds (an assumption). T* is later when capital is more persistent and earlier when social value deteriorates faster. **A finite lifespan need not mean rapid liquidation.**
- **Proposition 3.** Each regime is optimal somewhere in parameter space.
- **Proposition 5.** Enforceable multiyear grants spanning the payoff horizon leave perpetuity with no extra commitment value through the grantee channel.
- **Proposition 6.** A binding corpus-preservation (asset-floor) constraint weakly lowers welfare. Lifespan, payout rate, corpus preservation and grant horizon are separate margins.

Scope conditions: perpetuity wins only when eta > eta_P and stopping would otherwise occur in the low state; "perpetual" means no voluntary termination while solvent, not guaranteed survival; discretion wins when governance is aligned and the stopping option has value; a sunset wins when survival bias is strong and the continuation profile eventually turns negative.

## Caveats that bound what this shows

1. **No data.** Nothing here establishes that foundations, or any institution, behave this way.
2. **Entrenchment is assumed, not derived.** d is exogenous and constant. The model does not generate sclerosis from elapsed time; it posits a survival-benefit wedge and asks how to design around it.
3. **Sunset optimality is conditional.** It needs "sufficiently strong survival bias" (assumed so that biased discretion continues indefinitely) and the single-crossing assumption on the welfare difference.
4. **Reduced-form governance.** Power appears only as a founder-versus-future-controller conflict through d; there is no distribution of power, no capture, no external principals.
5. **Output is a reduced form.** Productive value is eta*e, lost on termination, with no production function behind it.
6. **Scope.** Private philanthropic foundations. The author asserts generality to research institutes, endowed cultural bodies and mission-driven nonprofits; public-sector applicability is neither tested nor discussed, and the only regulatory mention is the US 5% payout rule.
7. **Author-side.** Single author, foundation affiliation, AI-assisted derivation review; none of this is disqualifying but the proofs have had no refereeing.

## Levers proposed, and their evidence

**[model]** The lifespan charter itself (perpetual, sunset at T*, or open-ended), paired with separately chosen payout rules, corpus-preservation rules and grant horizons; enforceable multiyear grants as a substitute for perpetuity's grantee-commitment value. Governance alignment (lowering d) is implied but not modelled as a lever. **[wiki synthesis]** The evidence base for every lever is the model's own derivation. No outcome evidence exists in the source that sunset foundations or enforceable grants perform better, and the practitioner literature it cites is descriptive.

## Fit with existing pages

**[wiki synthesis]** Extension of [[credible-commitment]]: that page treats commitment as the ruler binding himself against expropriation of investors; this model makes existence itself the committed margin, with the same ex-ante-investment versus ex-post-option trade-off. It is a clean statement that commitment has a price (Lemma 1: flexibility is dominant absent the two problems), which the ruler-constraint literature there mostly presumes away.

**Real tension, scoped narrowly.** [[institutional-sclerosis]] and the Position A reading in [[decay-as-real-vs-decay-as-overstated]] tie rigidity to elapsed time. Here perpetuity is not inherently decay-prone (it is optimal when capital is productive) and entrenchment is a governance wedge. This is not a refutation: the model has no age mechanism, so it neither supports Position A nor Position B or the age-independence claim in [[downs-vs-merton-on-age-dependence]]. What it does add is a design-side distinction those pages lack: continuing past usefulness (overcontinuation) and underinvesting because the end is possible (hold-up) are distinct failures with opposite remedies. It also partly fills the prescriptive gap [[institutional-sclerosis]] names, that the only stated remedy is upheaval, by formalising a non-catastrophic charter-level lever, though formal-only. It bears on [[open-questions]] Q65 (does an institution's own design specify a lapse condition) as the first source that analyses why one would, and when not to.

## Public/private and power

**[wiki synthesis]** Tested nowhere across the divide. Public bodies with sunset clauses face the same trade-off in principle, but the private-benefit wedge d is a different object for a civil-service career than for a foundation trustee. Power enters only via d and the founder's ex-ante control over future boards.

## Source

- `raw/research/weekly-2026-10-13/04-foundations-lifespan-commitment.md` — Jaag, "Organizational Lifespan as Commitment: The Case of Foundations", arXiv:2610.08447, Oct 2026. Un-refereed preprint.

## Related

- [[credible-commitment]] — extended: existence as the committed margin.
- [[institutional-sclerosis]] — overcontinuation under discretion as a design-side analogue; this model has no age term.
- [[decay-as-real-vs-decay-as-overstated]] — the filed dispute this source cannot be cited into.
- [[downs-vs-merton-on-age-dependence]] — survival-as-terminal-value with constant d; another untested model.
- [[structural-inertia-and-age-dependent-mortality]] — age-driven mortality versus design-chosen termination.
- [[organisational-demise-as-a-construct]] — termination as a deliberate decision, not only an exit.
- [[goal-displacement-and-bureaucratic-ritualism]] — the private survival benefit echoes Merton's instrumental-to-terminal shift.
- [[path-dependence-and-increasing-returns]] — organisational capital as returns to continuity.
- [[property-rights-theory-of-the-firm]] — sunk specific investment and hold-up, applied to survival rather than control rights.
- [[decision-rights-and-authority-theory-of-the-firm]] — existence as the controlled decision.
- [[formal-and-real-authority]] — Aghion-Tirole's ex-ante commitment-for-investment logic is the nearest relative.
- [[agency-costs-and-ownership-structure]] — controller private benefits.
- [[reform-levers]] — a charter-level sunset as a formal-only lever.
- [[dimensions-of-institutional-variation]] — candidate axis: lifespan rule.
- [[organizational-economics-of-the-state]] — organisational-economics framing extended to survival.
- [[open-questions]] — Q60 (age decay; no help here), Q65 (design-specified lapse conditions).
