# False Frontiers: Co-Cheating in Self-Evolving Search Agents (CrossFit)

arXiv:2609.39102 names and measures "co-cheating" in proposer/solver self-evolving search agents (Dr. Zero-style). The proposer's pseudo-label and the solver's responses agree on the same wrong answer, and that agreement is rewarded. CrossFit assigns each source document to one of two folds. Each question is scored by an auxiliary solver trained only on the other fold, which cuts round-3 false-agreement mass roughly in half and lifts downstream search accuracy by about 8-9 points on Qwen3.5-4B/9B.

## Method

- **Setting:** the proposer turns source docs into questions plus pseudo-labels. Admitted pairs train a solver. The solver's pass rate on new proposals is the proposer reward, via the Dr. Zero frontier reward f(k)=(5-k)/4 for 0<k<5 correct of 5 responses. It builds on Dr. Zero, Search Self-Play, R-Zero and Search-R1.
- **Diagnosis:** a post-hoc auditor (gpt-6-astra/high) builds an evidence-backed reference from the source. It judges the saved label and the 5 solver responses at each of 129 steps (3 rounds x 43 steps). The auditor never feeds training.
  - Metrics: false-agreement mass F (label and response agree on the same incorrect answer), lost-credit mass L, label truth TP, solver truth TS, in-loop agreement A.
  - Co-cheating means A and F rise while TP and TS do not.
- **MSV (multi-sample verification, admission-time baseline):** the same model draws 3 source-aware and 3 source-blind answers. A majority (>=2) of each view must exist and match. The majority replaces the draft label, otherwise the candidate is rejected. It costs 6 extra generations per candidate.
- **CrossFit (main method):** each source document (not question) is assigned once to fold 0 or 1. Two auxiliary feedback solvers are each trained only on admitted questions from one fold. Questions from fold h are scored by the solver trained on fold 1-h, and that score feeds the unchanged frontier reward.
  - The main solver still trains on all admitted data with an unchanged update rule. Only the proposer feedback is cross-fitted.
  - Cross-fitted arms diverge from the coupled baseline only from round 2.
  - The exclusion principle comes from cross-fitting / double-ML (Chernozhukov 2018), without its guarantees.
- **Config:** Qwen3.5-4B and 9B, 3 rounds x (18 proposer + 25 solver steps), no human QA data.

## Results

- **Round-3 false-agreement mass F (4B / 9B):**

  | Arm | 4B | 9B |
  |---|---|---|
  | Coupled | 6.1% | 8.8% |
  | MSV | 5.7% | 7.2% |
  | CrossFit | 3.0% | 3.7% |
  | MSV+CrossFit | 2.0% | 1.7% |

  Round-1 F is only 0.4% / 0.3%, so the effect emerges from round 2. Replaying identical proposals with source-excluded feedback gives F of 0.4% / 0.1%.
- **Downstream:** 1,325-question suite (200 each NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue, plus 125 Bamboogle). Metric is Cover-EM, equal-weight average.

  | Arm | 4B | 9B |
  |---|---|---|
  | Base | 0.384 | 0.409 |
  | Search-R1 | 0.401 | 0.434 |
  | Dr. Zero | 0.400 | 0.428 |
  | MSV | 0.407 | 0.436 |
  | CrossFit | 0.488 | 0.512 |
  | MSV+CrossFit | 0.491 | 0.515 |

  - CrossFit gains +8.8 / +8.4 over Dr. Zero and +8.7 / +7.8 over Search-R1. Every benchmark improves.
  - Multi-hop gains average +10.0 / +10.9, against +7.3 / +5.2 for single-hop. MuSiQue 4B goes from 0.120 to 0.245.
  - The gap over Dr. Zero grows from +4.2 / +4.3 after round 2 to +8.8 / +8.4 after round 3.
  - Adopted-label truth rises from 0.747 to 0.819 (4B) and from 0.737 to 0.851 (9B).
- **MSV is weak:** alone it adds +0.7-0.8 average. Adding it to CrossFit adds only +0.3.
- **Ablations (fixed 3,000-question replay bank):**
  - Same-source auxiliary: F 6.4% / 8.7%.
  - Full-data auxiliary: F 5.8% / 6.9%. Both are close to the coupled baseline.
  - Random-row (question-level) out-of-fold: F 5.0% / 6.2%.
  - Source-ID out-of-fold: F 0.4% / 0.1%.
  - Half-budget auxiliary: F 0.5% / 0.2%, replay accuracy 91.6 / 91.8%, matching the full budget. Extra updates therefore do not explain the effect.
  - Replay accuracy rises 88.1 to 91.5 (4B) and 87.0 to 91.7 (9B).
- The operative control is the training ancestry of the feedback evaluator, split at the source level. It matters more than pseudo-label quality, and row-level splits leak.

## Applicability

Fits any proposer/solver or self-play loop where a trained solver rewards generated tasks drawn from a finite document pool. That covers search agents, R-Zero/SPICE-style corpus self-play and [[skill-self-play]], whose Proposer/Solver/Controller loop has the same closed-loop feedback risk.

Prerequisites:
- Tasks traceable to source IDs.
- Two extra auxiliary solvers to train. The end-to-end cost is not quantified.
- An evidence-backed auditor to measure F.

It does not apply to loops with no source grouping or with verifiable external reward.

## Novelty/caveats

- **Refinement, not invention:** the authors explicitly do not claim self-play, verification or cross-fitting. What is new:
  - Naming and measuring co-cheating with an evidence-grounded audit of the in-loop signal.
  - The finding that feedback-evaluator ancestry beats label quality.
  - The source-level (not row-level) split as the operative control.
- **Closest prior work:** Dr. Zero, Search Self-Play, SearchMaster (grounded/regulated self-play, a complementary diagnosis), CAFE (co-evolving feedback) and pseudo-label confirmation bias (Arazo 2020). Most of these are uncaptured neighbours (see [[watchlist]]).
- **Tension with consensus-as-signal work:** self-consistency and agreement become optimistic through shared errors in closed loops. This sits against [[ttpo-test-time-policy-opt]], where disagreement with a wrong pseudo-label is usually still a good signal. It also cautions [[u-opsd-unsupervised-self-distillation]], which uses majority-vote consensus as teacher. It nuances closed-loop claims like [[self-play-pretraining-zero-data]]. It is the same confirmation-bias family as [[tempo-test-time-rl]].
- **Caveats:**
  - The audit relies on a closed commercial judge. The authors flag judge bias and limited human validation.
  - There is a single 3-round schedule.
  - The cross-fitting guarantees are not inherited.
- **Adoption:** fresh (Oct 2026 arXiv) with no external pickup yet. Many authors are independent researchers and there is no major lab.

## Reproducibility

No code or weights link was seen in the portion read (lines 1-912 of 1223). The remainder is references and appendices, and the appendix tables were not read. The reproducibility statement says the appendix lists the schedule, config, eval manifest, scoring rules, audit procedure and controls. The audit needs a closed judge (gpt-6-astra/high). Std is reported only for replay accuracy (5 seeds). Treat the headline +8-9 points as a single-schedule result.

## Source

- `raw/research/weekly-2026-10-03/05-co-cheating-crossfit.md` (arXiv 2609.39102)

## Related

- [[skill-self-play]] — same closed-loop Proposer/Solver feedback risk; CrossFit-style exclusion is directly applicable.
- [[self-play-pretraining-zero-data]] — generator/learner self-play with an endogenous learner-state reward proxy.
- [[u-opsd-unsupervised-self-distillation]] — majority-vote pseudo-labels as supervision; MSV is a similar consensus mechanism and is shown insufficient here.
- [[ttpo-test-time-policy-opt]] — label-free pseudo-label RL; pseudo-label error propagation.
- [[tempo-test-time-rl]] — TTRL/EMPO drift from self-generated labels; same confirmation-bias failure family.
- [[debate-training-reward-hacking]] — proxy-judge reward hacking; separating evaluator from policy.
- [[jev-as-a-judge]] — LLM-judge use and bias; the auditor here is the same family.
- [[agentflow]] — search/agentic RL training with outcome reward.
- [[qwen-agentworld]] — synthetic task/env generation for agent RL on Qwen3.5.
- [[terminal-universe]] — synthetic task synthesis with verifier filtering, analogous to MSV admission.
- [[polar-rl-harness]] — Qwen3.5-4B agentic RL backbone.
- [[rrc-reward-ranking]] — reward construction from noisy judgments.
- [[watchlist]] — Dr. Zero, Search Self-Play, SearchMaster, CAFE and Search-E1 are uncaptured neighbours.
