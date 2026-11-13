# Object certainty model (drone-prototype EDA355 design: 3-state belief, tempered looks, static + mobile decay)

**Status: proposed design. It is NOT built, and the human's decisions are still owed** (drone-prototype PR #274, approved
by review on 2026-11-12). The design replaces the rover's hard re-observation rules with one posterior per object. The
rules it replaces are "N distinct contrary stations", "contrary looks spread over 45 deg", the 2-station filing rule and
the sticky person/pet hold. Every decision then becomes a threshold on that posterior. This page records the method,
because it is reusable for any "is the thing still there?" memory built from a noisy detector. The project record is
the EDA355 DESIGN.md; numbers here are pointers to it, not new claims.

## Source

All paths are in the drone-prototype repo, branch `eda355-object-certainty` (PR #274, not merged on 2026-11-12):
- `eda/EDA355-object-certainty/DESIGN.md` §1–§3 (state, update, thresholds), §4 (offline prototype on EDA348's ledgers)
- `eda/EDA355-object-certainty/proto.py` (the prototype filter; `check_time_alone` asserts the decay floor)
- `eda/EDA348-object-reobservation/FINDINGS.md` §2 (the per-model counts the likelihoods come from)
- parked P-01280 (unmeasured parameters), P-01281 (small-object LiDAR miss rate), P-01283 (correlation and agent weights chosen, not measured)

## The state

Each object carries a 3-state belief: **H** (here), **M** (moved: exists, but not here) and **N** (never existed: a
false record). It also carries a position with a 2x2 covariance, dimension bounds with P(within ±3 cm), and an ID
distribution weighted by measured label accuracy. H is split into **Hs** (static part, prior weight h_inf by permanence
class) and **Hm** (mobile part).

## The update per look

- **Predict (time).** Only Hm leaks to M: `Hm <- Hm e`, `M <- M + Hm (1 - e)`, with `e = exp(-lam dt)`. The
  exponential composes, so splitting a gap into many no-vote steps changes nothing. Time alone never takes P(H) below
  h_inf x P(H) at the last evidence. Time makes a belief **uncertain**, never **gone**; "location unknown" needs
  contrary looks. In the prototype, the minimum P(H) from time alone was 0.24, against a location-unknown threshold of 0.05.
- **Correct (look).** The likelihood for each verdict (present / absent / moved / no vote) uses the evidence model's miss
  rate pm and false rate pf. A "moved" verdict (absent here, plus a same-size unexplained body within 3 m) favours M by
  kappa = 3. Each state is floored at 1e-4, so no belief becomes un-clearable (the project rule "beliefs must clear").
- **Rates are Beta(1,1) posterior means, not upper bounds.** The caution belongs in the decision threshold. Feeding
  90 % upper bounds into a likelihood ratio can invert it: for wall art (pm 0.745, pf 0.425) an absent look became
  evidence FOR the object.
- **Tempered same-view looks.** A look in the same run within 15 deg bearing and 0.3 m range of an earlier look gets
  weight `(1 - rho)^k` (rho = 0.5), so one view is worth at most 2 independent looks. Different runs count as
  independent. Without this, the prototype called 7 furniture objects location-unknown from bursts of same-view
  looks (4 confirmed false by a later sighting), and falsely removed one truth object.
- **People and pets.** Each look carries its own sweep time window. Its weight is `1 - exp(-gap / tau_agent)`, where
  gap is the time to the nearest person/pet signal covering the object. A signal inside the window gives weight 0. This
  replaces the sticky hold rule.

## Permanence classes (decay)

| class | lam (per day) | h_inf | meaning |
|---|---|---|---|
| permanent | 0 | 1 | never moves; an absent look can only mean N |
| semi-permanent | 0.02 (half-life ~35 d) | 0.7 | chair, purifier |
| non-permanent | 0.2 (half-life ~3.5 d) | 0.3 | bottle, toy |

The hazards are **assumed** (P-01280). They are not derived from the rover's mobility recheck intervals or measured.

## Decisions = thresholds (proposed `config/certainty.json`)

retire at P(N) ≥ 0.99 · location unknown at P(H) ≤ 0.05 · file an unknown-id at P(exists) ≥ 0.85 · escalate ID at
P(exists) ≥ 0.9 with P(top label) < 0.8 · accept dimensions at P(within) ≥ 0.9. P(H) is also the price the planner reads
("old evidence is a priced check").

## What the offline prototype showed (EDA348 ledgers; read with the caveats)

- False removals: 0 vs the current rules' 0, out of 50 truth ledgers.
- False plants retired: **5 vs 7 of 57. The proposal is worse here.**
- Gone objects found: 7 vs 6 of 7, **only** under the assumed small-object miss rate 0.30 and the assumed
  non-permanent hazard. With either assumption relaxed it ties at 6/7; with both relaxed, 4/7.
- 3 of the 50 truth ledgers (wall art) are contaminated (see [[object-detector-measured-rates]]).

## Related

- [[object-detector-measured-rates]]: the per-model miss and false rates the likelihoods use, with their caveats
- [[semantic-object-memory]] · [[object-fingerprint-memory]] · [[locate-object-from-last-known-position]]
- [[dynamic-object-handling]]: semi-static and lifelong change, the general literature this is a small instance of
- [[measurement-selection-uncertainty]]: gating which measurements to trust
- [[task-conditioned-object-maps]]
