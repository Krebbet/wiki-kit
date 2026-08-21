# Structural Inertia and Age-Dependent Mortality

Hannan & Freeman (1984) is a formal, axiomatic theory paper — ten stated Assumptions deriving five Theorems — that reverses the usual reading of organisational inertia: inertia is not a precondition for selection-based (rather than adaptation-based) explanations of organisational change, it is a **consequence** of selection. Selection favours organisations capable of reliable, accountable performance; reliable, accountable performance requires highly reproducible structure; high reproducibility mechanically generates strong resistance to change. The paper then derives, from that chain, why death rates should decline with age (Theorem 3, the liability of newness re-derived as a theorem rather than assumed), and adds a mechanism this wiki had not previously held: **reorganisation can reset an organisation's effective age for mortality purposes.**

**Evidence tier note.** **[model]** throughout — no original data. Where the paper claims empirical support (for Theorem 3's exponential age-decline pattern, and for the Makeham hazard specification), it cites external sources (Freeman, Carroll & Hannan 1983; Carroll & Delacroix 1982) rather than presenting data itself. The theoretical apparatus is nonetheless directly useful: it supplies the mechanism [[liability-of-newness-empirical-hazard-evidence]] measures without theorising, and a testable prediction ([[open-questions]] Q60) no other source in this wiki states.

## The reliability/accountability → inertia → age-dependence chain

**[model]** The derivation, compressed:

1. Selection favours organisations with high **reliability** (low variance in output quality/timeliness) and **accountability** (a rationally reconstructible account of resource use and decisions, whether or not the account is literally true) — Assumption 1.
2. Reliability and accountability require highly reproducible structure — Assumption 2.
3. High reproducibility generates strong inertial pressure — Assumption 3. → **Theorem 1**: selection favours high-inertia structures.
4. Reproducibility rises monotonically with age (trust between strangers, worked-out routines, organisation-specific skill investment, and external legitimacy all take time to accumulate) — Assumption 4. → **Theorem 2**: inertia rises with age. → **Theorem 3**: death rates decline with age — the liability-of-newness hypothesis, now derived rather than posited.

**[wiki synthesis]** This is the theoretical partner to [[liability-of-newness-empirical-hazard-evidence]]'s data: Hannan & Freeman explain *why* Yang & Aldrich's hazard curve should decline, via a different causal story (accumulating reproducibility/inertia) than Yang & Aldrich's own finding (accumulating routine/boundary-building *activity*). The two are compatible rather than competing — reproducibility is arguably what routine-enactment, ownership agreements and boundary-registration *produce* — but neither paper tests the other's mechanism directly, and no source in this wiki adjudicates between them.

## Reorganisation as an age-reset event

**[model]** Assumption 8: structural reorganisation can reset the liability-of-newness clock toward zero, because reorganisation strips an organisation's history of the survival value accrued from stable routines. Formalised with a Makeham hazard model, $r_d(t\mid t_0) = \alpha + \beta e^{-\gamma(t - t_0)}$, showing a reorganised firm's death rate can jump to resemble a brand-new firm's with the same structure.

This yields a stated, falsifiable, mechanism-distinguishing test: **"If the liability of newness reflects internal processes, the death rate will jump with structural changes. In contrast, if the decline in the death rate with age reflects mainly the operation of external processes of legitimacy and exchange, the death rate will not jump when structural changes do not imply a change in basic goals."** No source in this wiki has run this test on real data.

**[wiki synthesis]** This is the first source the wiki holds that names charter-level reconstitution as the natural experimental control for an age-mortality claim — exactly the design element [[open-questions]] Q60 calls for ("years since any charter-level reconstitution recorded separately, because a re-founded body is the natural control and nobody uses it") — but only as an untested formalisation. Registered as [[dimensions-of-institutional-variation]] **D126**.

## Reorganisation attempts raise short-run death risk

**[model]** Assumption 6 (attempting reorganisation lowers reliability) → **Theorem 4**: attempting reorganisation increases death rates. Assumption 9 (death rate during reorganisation rises with the duration of the reorganisation attempt, via a Gompertz hazard) reconciles March's (1981) paradox: crisis-driven strategic change can simultaneously raise short-run death risk and, conditional on survival, lower long-run risk (the paper's Fig. 2 plots this — a declining curve for organisations retaining old structure, a lower declining curve for those that successfully adopt a new structure, and a curve for those that revert after attempting change and failing).

## Size, complexity and inertia: the paper's counter-conventional stance

**[model]** Assumption 5 states inertia rises with size, and Assumption 7 that death rate falls with size — but the paper explicitly **rejects** the common view that ecological/selection theory applies more readily to small organisations than large ones. Small organisations attempt change more often but are also more likely to die while reorganising (smaller margin for error); large organisations can buffer high-frequency environmental shocks that smaller organisations cannot, so *relative* inertia (adjustment speed relative to the relevant rate of environmental change) does not track absolute size straightforwardly. Complexity independently raises the risk of death during reorganisation (Assumption 10 → Theorem 5), via longer chains of required cross-subunit adjustment in non-hierarchically-nested structures (drawing on Simon 1962).

## Source

- `raw/research/organisational-ecology/02-hannan-freeman-structural-inertia.md` — Michael T. Hannan & John Freeman, "Structural Inertia and Organizational Change," *American Sociological Review* 49(2), 1984, pp. 149–164. http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Hannan%20&%20Freeman%20(1984).PDF

## Related

- [[liability-of-newness-empirical-hazard-evidence]] — the empirical hazard curve this paper's Theorem 3 predicts, from a different mechanism.
- [[population-ecology-of-organisations]] — this paper's companion piece, the 1977 framework it builds on.
- [[dimensions-of-institutional-variation]] — supplies **D124** (age-dependent mortality hazard, jointly with Yang & Aldrich) and **D126** (reconstitution as an age-reset event, this paper's own contribution).
- [[downs-vs-merton-on-age-dependence]] — the mature-bureaucracy age-decay conflict this paper's reorganisation-reset mechanism speaks to but does not settle.
- [[open-questions]] — Q60, whose reconstitution-as-control design element this paper is the first source to name.
- [[isomorphic-mimicry-and-capability-traps]] — a different account of why organisational adaptation attempts fail, at the field-legitimacy rather than the reliability/accountability level.
