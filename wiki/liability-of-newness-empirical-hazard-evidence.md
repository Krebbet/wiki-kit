# Liability of Newness: Empirical Hazard Evidence

Yang & Aldrich (2016) is the first source this wiki holds that measures organisational age against organisational mortality **directly, on a true panel, from actual founding** — not from incorporation, not from a national aggregate, and not as a career-tenure or regime-duration proxy. Using the Panel Study of Entrepreneurial Dynamics II (PSED II, 1,030 US ventures tracked monthly 2005–2011 from the point an entrepreneur began organizing), a Cox proportional-hazards model returns a **failure hazard that declines monotonically from 0.031 to 0.015 over the first 40 months** — confirming Stinchcombe's (1965) "liability of newness" shape against the rival "liability of adolescence" (hump-shaped) hypothesis in this sample. The paper's more important contribution is mechanistic: it decomposes *why* the hazard falls, and the answer is not what founders started with but what they subsequently did.

**Evidence tier note.** **[empirical]**, and unusually clean for this register: a nationally representative panel with time-varying covariates, left-truncation modelled explicitly (via elapsed pre-entry time at the screening interview), and event-history methods built for exactly this data structure. The main threat to external validity is scope, not design — see the limits section below.

## The hazard curve, and why it beats prior tests

**[empirical]** Two competing shapes have circulated in the organisational-ecology literature since the 1990s: **liability of newness** (Stinchcombe 1965) predicts a monotonically declining hazard from birth; **liability of adolescence** (Fichman & Levinthal 1991; Brüderl & Schüssler 1990) predicts an initial low-hazard "honeymoon" period sustained by founding resource stocks, followed by a *rise* before the eventual decline. Yang & Aldrich's smoothed hazard curve (their Fig. 1) shows no honeymoon: risk is **highest at the very start** (0.031) and falls steadily to 0.015 by month 40.

The comparison to prior registration-based studies is itself an important finding: "the highest risk of failure in our results, 0.026 [sic, referring to a later specification], is much higher than the peak of hazard failure, 0.018, found by Brüderl and Schussler (1990) using data on founders whose firms were registered with Munich's Chamber of Commerce." Because PSED II tracks entrepreneurs from the *true* start of organizing (self-reported "conception date"), not from legal registration, it captures a higher-risk early period that registration-based samples miss by construction — every organisation that dies before registering is invisible to those studies. **Any age-dependence study sourced from incorporation, registration, or charter records should be read as left-truncated and as under-stating early-life mortality risk**, per this comparison.

## The mechanism: subsequent activity, not initial endowment

**[empirical]** The paper's central and more portable claim: of the founding conditions tested — managerial experience, prior start-up experience, non-owner/helper social support, joint founder work history, household-based team composition, industry work experience, and initial financial capital — **only industry work experience and initial-12-month financial capital reduce failure risk**, and the capital effect disappears once *subsequent* investment is controlled. What matters is what founders do after the beginning, across three dimensions drawn from Aldrich's (1979) framework of organisational emergence:

| Activity | Effect on failure hazard |
|---|---|
| Additional financial capital invested after month 12 | Reduces hazard; initial capital's effect vanishes once this is controlled |
| Enacting a written business plan | −26% |
| Retaining an accountant | −32% |
| Retaining a lawyer | −30% |
| Owners signing a formal ownership agreement | −46% |
| Boundary-defining activity (trade-association membership, government registration) | Reduces hazard; D&B listing alone does not |
| Working ≥35 hrs/week (commitment) | Effect is **mediated through** the above activities — non-significant once they are controlled |
| Positive cash flow | −65%, and does not eliminate the significance of the activity variables |

**[wiki synthesis]** This reframes "age" as a proxy variable rather than a causal one: elapsed time correlates with mortality because it correlates with how much resource-accumulation, routine-building and boundary-establishing work has been done, not because organisations decay or mature by the calendar. This is the operational content behind [[dimensions-of-institutional-variation]] **D125**.

## Limits on what this evidence can carry

**[wiki synthesis]** Three scope conditions matter for how this source is used elsewhere in the wiki:

1. **Population.** PSED II samples nascent US entrepreneurial ventures — small, often single-founder, non-high-tech, poorly capitalised at the outset. It says nothing directly about government agencies, large corporations, or any institution past its first ~3.5 years of life. Extrapolating this hazard shape to a mature bureaucracy is not licensed by the paper.
2. **Outcome.** The dependent variable is self-reported disengagement from the venture — organisational death, not the accumulation of rules, goal displacement, or loss of adaptive capacity that the wiki's stagnation literature (Downs, Merton — see [[downs-vs-merton-on-age-dependence]]) is actually about. A declining *mortality* hazard in year one through four says nothing about whether a *surviving* organisation is becoming more rule-bound or rigid over decades.
3. **Construct validity of "death."** [[organisational-demise-as-a-construct]] (Searing 2020) shows, in a different population, that organisational closure is frequently not a clean, dateable event — organisations can persist as "zombies" (formally alive, functionally defunct) or dissolve and "reincarnate" under a related mission. Yang & Aldrich's self-reported "disengagement" measure is more behaviourally grounded than a registry-lapse proxy, but the general caution that "death" needs definitional scrutiny before being treated as a hazard-model event still applies.

## Relevance to Q60 and the register's age gap

**[wiki synthesis]** [[open-questions]] Q60 specifies a four-part design for settling whether organisational age predicts anything about behaviour: (i) true founding date with reconstitution tracked separately, (ii) a directly observed accumulation variable on the same institution, (iii) a panel rather than a cross-section, and (iv) controls for external-regime vintage and principal polarisation. This paper satisfies (i) and (iii) cleanly, and supplies a genuine accumulation variable for (ii) — but that variable (routine/boundary-formation activity in a venture's first 40 months) is an *early-life organizing* measure, not the *mature-bureaucracy rule/coalition accumulation* Downs's hypothesis C.11 predicts, and (iv) does not apply to private ventures at all. **The design Q60 calls for has now been run and gives a clean result — on the wrong population for the question Q60 was actually built to answer.** See [[open-questions]] for the full status update.

## Source

- `raw/research/organisational-ecology/03-yang-aldrich-liability-newness-revisited.md` — Tiantian Yang & Howard E. Aldrich, "'The liability of newness' revisited: Theoretical restatement and empirical testing in emergent organizations," *Social Science Research*, 2016. https://faculty.wharton.upenn.edu/wp-content/uploads/2017/10/The-Liability-of-Newness.pdf

## Related

- [[structural-inertia-and-age-dependent-mortality]] — Hannan & Freeman's theoretical derivation of the same declining-hazard shape, from a different (reproducibility/inertia) mechanism.
- [[population-ecology-of-organisations]] — the framework this paper's Cox model tests, and the source of the "liability of newness" term itself.
- [[firm-age-and-performance]] — the complicating view that age effects are front-loaded and non-monotonic across a firm's full lifespan, not a single declining curve.
- [[organisational-demise-as-a-construct]] — the caveat on what "death" as a hazard-model event actually captures.
- [[dimensions-of-institutional-variation]] — supplies **D124** (age-dependent mortality hazard) and **D125** (routine/boundary-formation intensity, the one row here scoreable on a single institution's own records).
- [[downs-vs-merton-on-age-dependence]] — the mature-bureaucracy age-decay claim this paper's population cannot test.
- [[open-questions]] — Q7 (age limb, moved to `partial`) and Q60 (the design this paper runs, on the wrong population).
