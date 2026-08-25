# Misperceptions and Support for Democracy

Acemoglu, Ajzenman, Cruces, Fiszbein, Garcia Zavaleta & Molina (NBER, August 2026) run two preregistered survey experiments (n=11,377) around Argentina's October–November 2023 presidential election, and find that citizens hold widespread **optimistic misperceptions** about how well populist and authoritarian regimes would have performed economically — and that correcting those misperceptions with credible information **causally reduces support** for such regimes (0.03–0.15 SD) and, weakly, vote intention. This is a citizen-belief mechanism, not an institution-level one: the wiki's existing pages cover institutional *design*, *decay* and *capture*; this paper is a well-identified anchor for a channel the wiki did not previously have — the **public-legitimacy/consent channel** by which citizens grant or withdraw support for institutions that constrain executive power.

**Evidence tier note.** **[empirical]** — randomized controlled experiment, the strongest evidence type this wiki carries for a legitimacy/consent claim: preregistered (AEARCTR-0012309, AEARCTR-0012523), IRB-approved, with balance checks showing no significant imbalance, no differential attrition, and a placebo arm ruling out experimenter demand. The one deliberately imported, untested input is the background claim that populist/authoritarian regimes actually underperform economically — see Ideological priors, below.

## Design

Randomized informational treatment (a video plus a statement citing academic evidence that populist/authoritarian regimes underperform economically) → shifts respondents' *perceived* economic performance of the relevant regime (0.06–0.16 SD) → shifts *support* for that regime and, more weakly, vote intention for the associated candidate. The causal chain is estimated via a first-stage (treatment → belief) / second-stage (predicted belief → support) 2SLS design; the authors are explicit that the exclusion restriction (treatment affects support only through beliefs) cannot be directly tested, only argued as plausible. A companion motivating cross-country correlation (79 countries, 1994–2009 World Values Survey waves, R²=0.142) is flagged by the authors themselves as merely correlational.

## What "support for concentrating power" means here

The outcome indices, following the authors' own 2025 five-component democracy-support index, operationalize opposition to "a strong leader who can bypass parliament and elections," opposition to military rule, and opposition to "governance by unelected experts rather than the government." The regime typology crossed against these outcomes (non-populist democratic / right-wing populist / left-wing populist / authoritarian-military) is defined partly by "a strong leader who bypasses traditional political institutions" — adjacent to, but distinct from, this wiki's veto-point/constraint axis (D44): here it is a citizen belief/attitude object, not a scored institutional feature. The mechanism under test is that citizens' *misbeliefs* about a regime's counterfactual economic output causally shape their willingness to grant power to leaders who can bypass institutional constraints — misperception as a channel through which populations *consent* to reduced institutional accountability.

## A named failure mode the wiki did not previously have

**Motivated reasoning** (citing Kunda 1990; Bénabou & Tirole 2016; Chopra, Haaland & Roth 2024) is the paper's one named mechanism, and it makes the correction **self-limiting**: respondents whose priors are contradicted by the treatment become significantly *less* willing to seek further information, and belief updating is "mostly concentrated among respondents whose prior beliefs align with what they perceive to be the academic consensus." This does not map onto the wiki's existing institutional-failure vocabulary (capture, ossification, goal displacement, rent-seeking) — it is a citizen-epistemics failure mode, one level up from institutional behaviour. Candidate name for the wiki's vocabulary: **legitimacy erosion via correctable-but-self-limiting misperception.**

## Levers, with unusually strong evidence for a "communications" claim

All three are randomized-arm results within the same preregistered design — comparatively strong evidence for what is normally a weakly-evidenced category of lever:

1. Informational campaigns sourced to **academic sources or legacy media** measurably shift support; **social-media-sourced** versions of the identical content produced effects statistically indistinguishable from zero.
2. **Negative-framed messages outperform positive-framed messages** of the same factual content (consistent with Zhang et al. 2024 on negativity bias in attention).
3. Effectiveness is conditional on the audience already trusting the source or perceiving alignment with academic consensus — a lever with a built-in ceiling, since it does not reach people already skeptical of academic authority.

## Ideological priors — a load-bearing input, not re-argued here

This paper takes as a fixed, unexamined input the claim that populist and authoritarian regimes underperform economically, sourced to Acemoglu, Naidu, Restrepo & Robinson (2019) and Funke, Schularick & Trebesch (2023), described as "the most recent and widely accepted evidence" the authors are "not aware of" being contradicted. **That claim sits on the contested side of this wiki's own open conflict, [[does-institutions-growth-survive-identification]]** — the paper's Section 3.2.3 acknowledges positive assessments of the Chilean "miracle" exist in the literature (Friedman, Becker, Hoover Institution researchers) but frames them as the misperception being corrected, not as a live scholarly dispute. This is not a new conflict in its own right — the paper makes no fresh institutions-and-growth claim, it imports one — but it is worth recording as evidence of how firmly the "populism/authoritarianism causes worse growth" premise is embedded in the AJR research programme's own self-citation, independent of whether the premise survives the wiki's identification audit.

## Scope

Argentina only, October–November 2023, a single presidential election (Milei vs. Massa vs. Bullrich) in a functioning democracy with free media — the authors explicitly contrast this with a companion Turkey study (Acemoglu, Aksoy, Baysan, Molina & Zeki 2024) where misperceptions are argued to arise from *restricted* information rather than lack of first-hand experience. Sample recruited via targeted Facebook advertising, demographically representative on age/gender/education but not a probability sample — an internet/social-media-using population by construction.

## Source

- `raw/research/weekly-2026-08-25/03-misperceptions-support-for-democracy.md` — Daron Acemoglu, Nicolas Ajzenman, Guillermo Cruces, Martin Fiszbein, Gaston Garcia Zavaleta & Carlos Molina, "Where the Grass Seems Greener: Economic Misperceptions and Support for Democracy," NBER Working Paper 35644, August 2026. https://www.nber.org/system/files/working_papers/w35644/w35644.pdf

## Related

- [[does-institutions-growth-survive-identification]] — this paper's core treatment content assumes the contested side of that conflict is settled, without engaging the wiki's recorded critique (Albouy, Glaeser et al., Deaton); recorded here as a context note, not a new conflict, since this paper makes no fresh institutions-and-growth claim of its own.
- [[colonial-origins-and-the-settler-mortality-instrument]] — same author lineage (Acemoglu), reusing the same underlying "non-democratic regimes underperform" corpus this wiki's anchor page already subjects to an identification audit.
- [[political-decay-and-vetocracy]] / [[veto-players-and-policy-stability]] — the paper's regime typology defines populism/authoritarianism partly by bypassing institutional constraints, this wiki's veto-point/constraint theme, though here only as a citizen-belief object.
- [[de-jure-vs-de-facto-power-and-captured-democracy]] — thematic parallel: both concern mechanisms by which formally democratic power arrangements erode, with this paper supplying a citizen-belief/information channel the de jure/de facto model does not include.
- [[schooling-and-institutional-quality]] / [[why-democracy-needs-education]] — a parallel literature on what sustains democratic-regime support (education-driven civic participation vs. this paper's misperception-correction channel), overlapping Acemoglu-adjacent research programmes.
- [[open-questions]] — candidate for a new question on legitimacy/consent as a determinant of institutional durability, since no existing wiki page currently owns this territory.
