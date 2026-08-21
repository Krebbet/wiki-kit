# The "Oligarchy" Result: A Methodological Critique

Bashir (2015) does not dispute that [[whose-preferences-predict-policy-gilens-page]] found a large gap between elite and average-citizen coefficients — he disputes whether that gap is a **real effect or a statistical artefact** of the specific method used to estimate it, and whether three of the paper's own descriptive claims survive a direct re-tabulation of its released data. This is a precise, targeted rebuttal, not a claim that elite/business advantage in US policymaking does not exist — Bashir states the opposite explicitly.

**Evidence tier note.** **[empirical]** — a Monte Carlo simulation matched to the real data's correlation structure, plus direct re-tabulation of Gilens & Page's own released dataset. Captured specifically to satisfy this wiki's ideological-balance requirement on a contested question; read alongside [[whose-preferences-predict-policy-gilens-page]], not in isolation.

## The statistical mechanism under challenge

**[empirical]** Gilens & Page's Model 4 regresses a **binary** outcome (policy adopted or not) linearly on two predictors correlated at **r = .78** (post-correction; .94 raw) — average-citizen and economic-elite preferences. Bashir's simulation seeds a range of "true" median-citizen coefficients (holding the elite coefficient fixed to match the real data's correlation structure) and shows this combination — linear regression on a binary outcome, plus high collinearity — **manufactures a spuriously near-zero, highly-divergent estimate at non-trivial rates even when the true citizen effect is substantial**: with a true β = 0.4 (more than half the elite coefficient), over 20% of simulated trials return an "essentially zero" citizen estimate; at β = 0.56, still over 10%. Confidence-interval coverage degrades in step with the correlation level, meaning the reported 95% CI is less trustworthy than its nominal rate implies at G&P's observed collinearity.

## Three descriptive claims, re-tabulated from the authors' own data

**[empirical]**
1. **"Even large majorities don't get their way"**: at ≥80% public support, elites get their preferred outcome 52% of the time, average citizens 47% — a small gap, not the large one implied by the headline framing, and elites show the same status-quo bias.
2. **Explanatory power**: Model 4's R² is 0.074 — under 10% of variation in policy outcomes is explained even by the variables the paper calls dominant.
3. **"Citizens generally lose when they disagree with elites"**: in the 185 cases of elite/average-citizen disagreement, average citizens get their preferred outcome **47% of the time** — close to a coin flip, not systematic elite victory. Even against combined elite-plus-interest-group opposition, citizens still win 30% of the time to elites' 32%.

## What this does and does not settle

**[wiki synthesis]** Bashir's own stated limit, quoted directly because precision matters here: **"even if inequality were somehow shown to have no bearing on who influences policy, it would still be morally wrong to ignore it."** He does not claim to have shown average citizens have strong independent influence — only that Gilens & Page's data and method are too weak to support the strong near-zero-influence conclusion in *either* direction. Also notable: he confirms neither Gilens nor Page ever used the word "oligarchy" themselves — it entered public discourse via press coverage (BBC, the *Telegraph*, Vox) and commentary (Krugman), a media/discourse artefact layered onto a more circumspect original claim.

## Source

- `raw/research/power-and-accountability/05-crit-bashir-oligarchy-review.md` — Omar S. Bashir, "Testing Inferences about American Politics: A Review of the 'Oligarchy' Result," *Research and Politics*, October–December 2015.

## Related

- [[whose-preferences-predict-policy-gilens-page]] — the paper this page directly rebuts on method and on three descriptive claims, without disputing elite/business advantage in general.
