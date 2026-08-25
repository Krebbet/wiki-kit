# Culture and Constitutional Compliance

Gutmann, Lewczuk-Czerwińska, Lewkowicz & Voigt (2026) test, across up to 115 countries, whether national culture predicts how well a state complies with its **own** constitution. Two findings survive the paper's full identification gauntlet (OLS → 2SLS with externally validated instruments → Lewbel heteroskedasticity-based internal instruments layered on top): **more individualistic national culture causally raises constitutional compliance; a higher Muslim population share lowers it.** Both hold across all four legal sub-domains tested (property rights/rule of law, political rights, civil liberties, basic human rights) and survive adding democracy as a control, though the effect size shrinks 40–50%. Two other candidate culture variables — power distance and long-term orientation — have the theoretically expected sign but **fail** the paper's own Lewbel robustness check (the long-term-orientation instrument set is flagged weak by both Stock-Yogo and Staiger-Stock, and its exclusion-restriction test is rejected at 5%). The paper is unusually disciplined about reporting its own failures rather than only its headline hits.

**Evidence tier note.** **[empirical]** — cross-country regression with a three-stage identification strategy (see below). Unit of analysis is strictly the nation-state, cross-sectional; no institution-level, sub-national, or branch-level variation appears anywhere in the design.

## The mechanism: a formal utility function, separately tested

The paper models a leader's compliance decision via U = U(S, C, M):

- **S** — political-support cost from citizen sanction (protest, voting, civil-society organisation).
- **C** — political-capital cost from veto-player opposition (courts, legislature, regional governments) — effective only if those veto players are independent of *both* the government and interest groups.
- **M** — the leader's own internalised moral cost of rule-breaking.

Individualistic societies are argued (citing Acemoglu & Robinson's "shackled Leviathan"/narrow-corridor framework) to trust impersonal institutions and hierarchies more, so citizens organise more effective sanctioning and are willing to entrust independent veto players with real power. This is not just asserted: a causal mediation analysis (GMM) decomposes it — individualism's effect on compliance runs through **both** civil-society strength (V-Dem's core civil-society index) and veto-player strength (proxied by judicial independence); Islam's negative effect runs primarily through civil society, plus a large unmediated remainder.

## Measurement: de jure vs. de facto, at country level

The outcome (Comparative Constitutional Compliance Database) measures **de facto implementation** (via V-Dem) against **de jure provisions** (via the Comparative Constitutions Project) — a country-level instance of the formal/real authority gap the wiki tracks at D112 and in the [[meta-oversight-board-case-profile]] case, here applied to a state's compliance with its own founding document rather than to a single organisation.

The compliance measure inherits [[v-dem-measurement-model]]'s documented practice of averaging away sub-national and branch-level heterogeneity before scoring — a limitation this paper does not create but does not address either, and directly relevant to [[open-questions]] Q90's level-of-analysis concern. The authors also disclose, unprompted, that the measure is normatively loaded: it is built from "important elements of a Western conception of limited government" (their footnote 1), so a government in full compliance with an illiberal or theocratic constitution would still score low. Carry this forward rather than treating the Islam result as religion-neutral.

## What the paper explicitly does not contribute

**No scale or age claim of any kind.** Culture itself is modelled as near time-invariant — the paper invokes Williamson's rule of thumb that culture "changes once a century" against formal institutions "about once a decade," directly citable on [[fast-and-slow-moving-institutions]] as corroboration, not complication. Culture is used precisely *because* it doesn't move on the same clock as the outcome being explained.

## A named failure mode: constitutional transplant mismatch

The paper's closest analogue to a named institutional failure mode is constitutions copied from elsewhere — often via international technical-assistance programmes — without regard to whether they fit the adopting country's cultural substrate, producing predictable non-compliance. This is structurally the same phenomenon as [[isomorphic-mimicry-and-capability-traps]] (form adopted for legitimacy/donor pressure without matching function), applied to constitutions rather than administrative agencies. The paper also names **selective enforcement**: a constitution granting a wide liberal-rights catalogue while simultaneously establishing religious-supremacy clauses creates a founding-document-level goal conflict, distinct from [[goal-displacement-and-bureaucratic-ritualism]]'s drift-from-an-original-single-goal-over-time pattern.

## Source

- `raw/research/weekly-2026-08-25/02-culture-constitutional-compliance.md` — Jerg Gutmann, Anna Lewczuk-Czerwińska, Jacek Lewkowicz & Stefan Voigt, "Culture and Constitutional Compliance," 2026, conditionally accepted at *European Economic Review*. https://arxiv.org/abs/2608.23369

## Related

- [[informal-institutions-typology]] — the paper's own framing, that formal-institution effectiveness depends on the informal/cultural environment it is embedded in, is an empirical instance of exactly Helmke & Levitsky's thesis, though this paper does not use their four-type framework.
- [[fast-and-slow-moving-institutions]] — corroborates Williamson's culture-vs-formal-institutions change-speed rule directly.
- [[credible-commitment]] — shares Weingast's self-enforcement mechanism (a constitution must be self-enforcing because no external authority enforces it) and supplies culture as a newly-tested upstream determinant of *why* self-enforcement succeeds in some societies and not others.
- [[v-dem-measurement-model]] — the dependent variable inherits V-Dem's sub-national/branch-averaging practice; relevant to Q90.
- [[de-jure-vs-de-facto-power-and-captured-democracy]] — this paper's core measurement strategy is a country-level instance of the same de jure/de facto gap that page treats at the elite/regime level.
- [[veto-players-and-policy-stability]] — judicial independence is used directly as the paper's veto-player proxy.
- [[isomorphic-mimicry-and-capability-traps]] — the constitutional-transplant-mismatch mechanism named above.
- [[culture-institutions-regions-of-europe]] — Tabellini's generalized-morality indicator is used directly as a control here (and is one of the culture variables that fails this paper's own robustness check); both papers sit in the same culture-and-institutions research programme at different levels of analysis (sub-national region vs. cross-national).
- [[determinants-of-trust]] / [[can-we-trust-social-capital]] — light link: Sobel's skepticism about cross-cultural trust comparisons is a relevant caution on this paper's use of generalized morality as a (non-robust) culture indicator.
- [[does-institutions-growth-survive-identification]] — methodologically adjacent: another culture/institution paper disclosing its own weak-instrument and exclusion-restriction diagnostics rather than hiding them.
- [[open-questions]] — Q90, on whether country-level claims like this one can be read down to institution level.
