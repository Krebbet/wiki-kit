# Method B: Margin-augmented preference optimization (fixture)

Method B extends the Method A objective with an explicit margin term,
aiming to separate preferred and dispreferred log-likelihoods by a
fixed amount rather than just preferring one over the other.

## Results (fixture)
On AlpacaEval with identical settings, Method B reports a
length-controlled win rate of 62.1% against the SFT baseline — a 12 pp
gap over Method A on the same eval.

## Note
This is a FIXTURE file for /ingest smoke testing. It is not a real
paper; don't cite it. The 12 pp claimed gap over Method A is the
deliberate conflict a subagent should flag under "Conflict flags" when
summarising 02-method-b against Method A's 50.2% report.
