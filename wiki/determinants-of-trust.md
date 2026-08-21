# Determinants of Trust

Alesina & La Ferrara's GSS-based study (1974–1994, ~1,500 respondents/year) finds self-reported generalised trust is predicted, at community level, primarily by **racial fragmentation** and, more weakly, **income inequality** — moving from the most homogeneous US metro area to the most heterogeneous is associated with a 12-percentage-point fall in trust, about 30% of the sample mean. At individual level, recent trauma (especially financial), being Black (a 23-percentage-point trust deficit), being divorced, and lower education/income all predict lower trust; religion, marital status, and own residential mobility do not.

**Evidence tier note.** **[empirical]** — probit regressions with year and state fixed effects, robustness checks including 2SLS instrumentation for income inequality (using 1962 municipal-government counts and intergovernmental-transfer shares as instruments) to address reverse causality. **The paper cites its own central measurement caveat explicitly**: see below.

## The heterogeneity finding, and the mechanism test behind it

**[empirical]** Racial fragmentation is the strongest community-level predictor, surviving jointly with income inequality (which loses significance once fragmentation is included) and outperforming ethnic fragmentation (not significant). The authors run four separate tests to distinguish two rival explanations — **aversion to heterogeneity** (people trust less those unlike themselves) versus **local interaction** (heterogeneous communities have lower average trust that then depresses everyone's trust via complementarity): restricting the sample to Black respondents makes the fragmentation coefficient insignificant (it is specifically white respondents whose trust falls in fragmented communities); racial fragmentation does not predict confidence in *institutions* (banks, courts) even though being Black does, arguing against a generic low-trust disposition; and splitting respondents by their own racial attitudes (12 GSS items), the negative fragmentation effect concentrates significantly among those "averse" to racial mixing. **[wiki synthesis]** The tests favour aversion-to-heterogeneity as "almost certainly present," without fully ruling out local interaction — read as a partially, not fully, identified mechanism.

## The paper cites the measurement problem against itself

**[empirical]** Alesina & La Ferrara use the same GSS "most people can be trusted" item [[measuring-trust-glaeser-et-al]] shows correlates with trustworthy behavior more than with actual trusting behavior — and they say so directly, in their own data section: "A more subtle issue is raised by Glaeser et al (2000). They find that answering yes to a question about trusting others is more correlated to being trustworthy in experiment than to being trusting... we have to be cautious in interpreting answers to questions on trust in surveys." **[wiki synthesis]** This wiki should read this paper's findings as determinants of *self-reported willingness to affirm a generalised-trust survey item* — a composite of trust propensity, self-presentation, and possibly trustworthiness-signalling — rather than unambiguously "determinants of actual trusting behavior." The finding is genuine and the authors' own caveat is on the record, which makes the caution citable rather than merely inferred.

## Self-reinforcing equilibria — a mechanism for informal-institution erosion

**[empirical]** Community residential stability (fraction of population in the same house 5 years earlier) is a significant positive predictor of trust — direct support for the authors' own theoretical grounding: sustained community stability preserves "the possibility of retaliation," which they identify as a basic requirement for cooperative equilibria (the same repeated-interaction logic [[maghribi-traders-reputation-mechanism]] and [[covenants-with-and-without-a-sword]] document directly). The paper's stated conclusion: heterogeneous, unstable communities and homogeneous, stable ones are **two distinct self-enforcing equilibria** — "in more heterogeneous communities the average trust is lower, and this induces people to trust even less... in more homogeneous communities the opposite self-enforcing equilibrium materializes."

## Source

- `raw/research/informal-institutions/09-alesina-laferrara-determinants-trust.md` — Alberto Alesina & Eliana La Ferrara, "The Determinants of Trust," NBER Working Paper 7621, 2000.

## Related

- [[measuring-trust-glaeser-et-al]] — the measurement caveat this paper cites against its own headline instrument.
- [[can-we-trust-social-capital]] — Sobel's cross-cultural comparability caution applies directly to any use of this paper's community-heterogeneity findings across countries, though the paper's own within-US design is less exposed to that specific problem than a cross-national comparison would be.
- [[maghribi-traders-reputation-mechanism]] and [[covenants-with-and-without-a-sword]] — the repeated-interaction/retaliation-possibility mechanism this paper's stability finding empirically supports.
