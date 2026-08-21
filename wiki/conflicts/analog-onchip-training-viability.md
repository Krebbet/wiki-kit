# Conflict: does in-situ training rescue imperfect analog arrays?

**Status:** open · **Opened:** 2026-08-21 · **Type:** same mechanism, incompatible generality

The wiki records in-situ (on-chip) training as the answer to analog arrays that cannot be manufactured perfectly — a yield-economics argument, and one of the better reasons to care about on-chip learning at all. New evidence says the training method that argument rests on **fails outright on realistic device response curves, with no defects present**. Both claims cannot be generally true.

This matters beyond the algorithm choice: if on-chip learning is the reason imperfect analog arrays are shippable, and on-chip learning is fragile, then a load-bearing plank in the analog compute-in-memory case is weaker than the wiki currently states.

## Position A — in-situ training tolerates defective arrays

*Recorded in [[../devices/memristor-array-integration-gap]], from the 2026 IOP memristor co-design review (secondary source, reporting others' work).*

- **Li et al., in-situ, SGD-based** — training *on* an **11%-defective** Ta/HfO₂/Pt array reached **91.71% MNIST**, with simulation holding **>60% accuracy even at 50% stuck-off devices**.
- **Jeon et al., static offline-programmed** — a defect-free 1 kb array reached 100% on an MNIST subset, but collapsed to **68.5%** at 30% open-circuit defects and **49.8%** at 50%.

The review's argument, which the wiki adopted: at realistic yields, in-situ learning is the viable defect-tolerance path, because offline-programmed arrays degrade catastrophically at the defect rates real fabrication produces.

## Position B — plain analog SGD fails on realistic response curves

*Recorded in [[../devices/analog-training-nonidealities]], from arXiv:2502.06309 (theory + AIHWKIT simulation).*

- Analog SGD trails digital SGD by **12.1 points** on ResNet18/CIFAR100 (68.98% vs 81.12%) and **27 points** on MobileNetV3S/CIFAR100 (51.79% vs 78.94%).
- Worse, in the failure regime: Analog SGD **collapses below 15%** on a 10-class MNIST task — at the random-guess floor — at response-function steepness `γ_res` = 1.0 and 2.0, across all tested dynamic ranges. Tiki-Taka and Residual Learning hold **97.0–97.7%** under identical conditions.
- **No defects are involved.** The cause is conductance response-function *asymmetry* alone.
- Cycle-to-cycle noise, by contrast, is not the problem — up to 120% noise leaves accuracy "not significantly affected."

## What separates them

Not a numeric contradiction on the same quantity — a disagreement about **which non-ideality dominates and how general the rescue is**.

1. **Different axes.** Position A varies *defects* (stuck-off devices) and holds the response function implicit. Position B varies the *response function* and has no defects. They are orthogonal failure modes, and a real array has both.
2. **The algorithm is the crux.** The wiki's record of Position A names Li et al. explicitly as **"in-situ, SGD-based"** — verified against the page text, not inferred. That is precisely the algorithm Position B shows collapsing. If Li et al. genuinely used plain SGD-style updates, then their result must depend on their specific device having a favourable, near-symmetric response function — making it a **device-specific result, not a general property of in-situ training**.
3. **Source tier.** Position A reaches this wiki through a *review* paraphrasing Li et al., and reviews compress methodology. "SGD-based" may be the reviewer's shorthand for something already corrected. Position B is a primary paper, but it is **simulation with generically-swept parameters not fitted to any named device.** Neither side is measured silicon running a real training job.

## Corroborating evidence — real device asymmetry

[[../devices/analog-training-nonidealities]] also carries a fabricated **CMO/HfOx** array (arXiv:2502.04524, 8×4 cells at 130 nm), a stack *specifically promoted for symmetric conductance updates*. Measured on that silicon:

- **Symmetry-point skew: 61%** — "the down response is steeper than the up response"
- **Noise-to-signal ratio at the symmetry point: 90%**
- **22 usable analog states** under open-loop pulsing, versus >32 stable states for inference

And the authors **never test plain SGD**. They go straight to **AGAD/TTv4**, an algorithm built to relax symmetry requirements, and their own ablation identifies symmetry — not defects, noise, or state count — as the dominant accuracy lever.

*(synthesis)* This does not adjudicate Li et al.'s defect claim, which is about a different axis. But it is strong indirect support for Position B's premise: if a device *engineered* for symmetry still measures 61% skew, then favourable response functions are not something a designer can assume. That makes Position A's generality the weaker of the two claims.

## Resolution conditions

In order of decisiveness:

1. **Read Li et al. directly** and establish the actual update rule. This is the cheapest and most decisive step, and it is a research task rather than a judgement call — the wiki currently holds this claim at one remove through a review. If the algorithm turns out to be Tiki-Taka-class, the conflict largely dissolves and Position A survives in narrowed form.
2. **Any paper that trains a network on a fabricated analog array** — not simulation calibrated to one — reporting both the defect rate *and* the measured response-function asymmetry. No source in this wiki does this today.
3. **Re-run the Position B analysis with response-function parameters fitted to named measured devices** rather than swept generically.

## Provisional reading

**No ruling yet.** *(synthesis)* On current evidence the defensible statement is narrower than what the wiki records:

> In-situ training tolerates **defects** far better than static programming does. It does **not** tolerate conductance-response **asymmetry** unless the update rule is Tiki-Taka-class. Since real devices — including ones engineered for symmetry — measure large asymmetry, "in-situ training rescues imperfect arrays" holds only for asymmetry-corrected algorithms, not for in-situ training as such.

The practical consequence is a shift in where the difficulty sits: **defect tolerance appears to be an algorithmic property, not a device property**, and the algorithms that deliver it are a specific family, not the default. That is a more useful claim than either position alone, and it is consistent with all the evidence in hand.

Pending resolution condition 1, [[../devices/memristor-array-integration-gap]] carries a pointer to this file rather than a rewritten claim.

## Source

- `raw/research/neuromorphic-commercial-viability/04-memristor-codesign-review.md` — Position A, via review paraphrase of Li et al. and Jeon et al.
- `raw/research/neuromorphic-seed-sweep/12-analog-training-nonideal.md` — Position B, theory + simulation
- `raw/research/neuromorphic-seed-sweep/16-cmo-hfox-onchip-training.md` — measured device asymmetry, corroborating B's premise

## Related

- [[../devices/analog-training-nonidealities]] — the full evidence on both algorithms and devices
- [[../devices/memristor-array-integration-gap]] — where Position A is recorded
- [[../snn/snn-training-surrogate-gradients]] — the architectural constraint on on-chip learning
- [[snn-energy-payoff]] — the other open dispute
- [[../viability-ledger]]
