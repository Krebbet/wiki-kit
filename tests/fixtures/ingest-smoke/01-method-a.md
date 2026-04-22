# Method A: Direct Preference Optimization variant (fixture)

Method A trains a policy model directly on preference pairs, removing
the separate reward-model stage from classic RLHF. Closed-form loss
based on log-odds of preferred vs. dispreferred responses.

## Results (fixture)
On AlpacaEval, Method A reports a length-controlled win rate of 50.2%
against the SFT baseline, matching or slightly exceeding an RLHF
pipeline at half the compute.

## Note
This is a FIXTURE file for /ingest smoke testing. It is not a real
paper; don't cite it.
