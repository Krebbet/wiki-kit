# Blind Spots Travel, Knowledge Stays Home: What RL Inherits from an LLM Judge (Yue & Vance)

Across 814 GRPO runs (Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct students, closed-book QA with abstention), a grader's per-answer knowledge does not transfer to unseen questions (about 1 answer per 100). Its structured false rejections on a kind of question do transfer: 12 rejected former-state-capital answers move refusal of that category from 5% to 90%. The fix is a label-free "own vote" grader, majority of 32 samples from the untrained student, which matches an answer key within 0.2 pts. arXiv:2611.25191; code at github.com/liyu2195/blind-spots-travel.

## Method

- Students: Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct. GRPO + LoRA (r=16), 120 steps, 32 questions x 8 samples per step, KL 0.2 to the untrained model, T=0.8. 750 training questions from TriviaQA, PopQA or NQ-open.
- Reward: $r=1$ if the grader accepts, $0$ if it rejects, $0.5$ for "I don't know". Answering pays only when $p(\text{right})>0.5$. Advantage $A=(r-\bar r)/(\sigma_r+10^{-4})$.
- Graders: answer key; five reference-free 7-13B judges returning P(correct) (thresholded at 0.5, 50% cut, 35% cut, or key-matched cut); Sonnet; reference-shown judge; majority-vote jury; hand-built graders (key plus random rejections; a judge's verdicts with the 12 known former-state verdicts edited by hand).
- Own-vote grader: sample 32 answers from the untrained student per question. If at least 20 agree, the majority answer becomes the key. Otherwise only "I don't know" pays. Then train as with a key. No labels, no judge. The cut (20/32) must be checked on a small labelled sample against the student's calibration point (agreeing-sample count at which it is right half the time).
- Cost: 1,405 runs, about 3,100 L4-hours, about 3 h per run.

## Key claims

1. **Per-answer verdicts stay home.** Wrong answers a judge pays are memorised per question: the judge's own student gets paid +34 pp on train but only +3 pp on new questions (9% carry-over). A hash-random grader gives chance-level carry-over (35-36%).
2. **Right verdicts do not travel either.** Key-, Sonnet- and reference-judge-trained students land at -0.8, +0.3, +1.0 pts vs the untrained student's own 32-sample vote rule at equal abstention. Training mostly compresses a 32-sample vote into one forward pass (a reward can only choose among answers the student already gives).
3. **Verdicts about a kind travel.** The Llama student trained with the Qwen judge at the 35% cut refuses 98% of 187 known former-state capitals on unseen questions (present-day capitals stay answered). Cause: 12 training answers. Setting only those 12 verdicts by hand moves refusal 5% to 90% (key-matched leniency) and 31% to 97% (35% cut). Four rejected answers among 750 suffice for Llama to drop most of the category. Accuracy and abstention rate do not reveal it.
4. **Student exceeds judge.** It refuses 62-95% (Llama) of capitals its own judge would accept. Judges share doubts, so a 5-judge jury removes 85-95% of the category. A second category ("In what country is X?") is lost the same way on 2,569 fresh PopQA questions (judges' Llama 83% refused vs 42% random-rejection, 3% key). 43 of 44 judge pairs show the effect.
5. **Knowledge is retained, willingness is gated.** With "I don't know" blocked at decoding, 94-95% of refused capitals are answered correctly.
6. **Keys have blind spots too.** On NQ-open the string-match key falsely rejects 37-39% of audited-right answers. Key-trained Llama abstains on 70% of questions, and 4 of 6 key-trained Qwen runs collapse to all-"I don't know" (forced-answer accuracy 4% vs 26% untrained).
7. **Own vote works.** True reward within 0.2 pts of the key (95% CI -1.1 to +0.7) pooled over six student-dataset pairs. 0 of 18 runs collapsed. It refuses only 9% / 11% of former-state capitals (Qwen/Llama) vs 82% / 98% for the Qwen judge at the 35% cut. Within 2 below to 12 above the calibration point, it is within 0.9 pts of the key in 11 of 11 settings.
8. **Exception: form travels.** A judge paying long answers spreads long answers in 8/8 runs.

## Results

| Grader | Effect on unseen questions |
|---|---|
| Random rejections over key | removes 19% (Qwen) / 50% (Llama) of former-state category |
| Reference-free judges (35% cut) | remove 53-98%; Llama 98% with Qwen judge |
| 5-judge jury | removes 85-95% |
| 12 hand-set verdicts | refusal 5% to 90% (key-matched), 31% to 97% (35% cut) |
| Key / Sonnet / ref-judge vs 32-vote | -0.8 / +0.3 / +1.0 pts |
| Own vote vs key (6 pairs) | -0.2 pts (CI -1.1, +0.7); 0/18 collapsed |
| Own vote, Qwen/TriviaQA at cut 20 | -3.4 pts (overconfident, calibration point 29/32); cut 27 fixes it |
| Sonnet / ref judge vs own vote | still ahead by 2.0 / 3.1 pts |

## Limitations

- Closed-book short-answer QA only; 7-8B LoRA students (446 extra runs with three smaller students). Open-ended generation untested (one refusal-task attempt showed no category concentration).
- Both lost categories are PopQA kinds and the capitals probe is hand-built. 2-6 runs per cell. 324 of 750 held-out PopQA questions are near-duplicates of training ones.
- KL penalty is load-bearing: without it 22-94% of answers change and accuracy can halve with a lenient judge.
- Truth is the key or a Sonnet audit (93% human agreement on 189 settled items, kappa 0.53), and Sonnet is also a grader.
- Own vote still needs a labelled sample to set the cut, cannot fix confident wrong answers, inherits the student's own blind spots, and cannot add knowledge. Not strictly better where labels or a stronger judge exist.

## What it means for our thesis

- **Few verdicts set a category rule.** 4-12 reward verdicts, at an abstraction level not present in the signal, switch off a whole concept class on unseen instances. This is concept-level generalisation from very few examples, driven by reward structure rather than surface strings, with negative valence. It is the dual of our positive single-sample results: the same mechanism that lets one example teach a concept lets one miscalibrated verdict erase one. Per-instance memorisation does not generalise, consistent with memorise-random-labels vs learn-patterns-first.
- **Design implication.** In single-sample or concept-based fine-tuning of 1-40B models, the grader's error structure matters more than its error rate. Audit what a verifier falsely rejects by category, not by aggregate accuracy. Aggregate accuracy and abstention hid a 98% category loss.
- **Evaluation probe.** A held-out category (former-state capitals) is a cheap concept-vs-instance generalisation test, usable in our concept-evaluation suite. Also checks gating vs forgetting by blocking abstention at decoding.
- **Label-free reward.** Own vote is a self-consistency reward (RLSC/TTRL family) with a measured validity window (cut within -2 to +12 of calibration point) and no collapse record. It is a candidate verifier-free reward for single-sample setups, provided a small labelled calibration sample exists.
- **Selection, not learning.** Consistent with RL reshaping which already-available answers are emitted. Grader knowledge adds about 1 answer per 100.

## Conflicts

- **Tension/extension, [[conflicts/revisql-vs-spurious-rewards-noise-robustness]]:** the paper suggests the resolution axis is error structure, not error rate. Random rejections (key plus random) are mostly memorised per question and harm little; category-coherent false rejections generalise. This supports a "noise-robust to incoherent errors, label-quality-bound under coherent errors" reading. Candidate input to the conflict page; not a ruling.
- **Tension (scope-limited), reasoning-boundary and teacher-reliability results:** "grader knowledge adds about 1 per 100" sits against claims that verified teacher knowledge matters. The regime is closed-book factual QA, not reasoning, and the result is consonant with the compaction line in [[research/teacher-student-rl/opsd-compresses-rlvr]] and [[conflicts/adrs-vs-opsd-compaction]]. Treat as scope difference, not conflict.

## Source

- raw/research/weekly-2026-11-20/03-blind-spots-travel.md (arXiv:2611.25191)

## Related

- [[research/rlvr-mechanics/wrong-votes-right-gradients]] — majority-vote self-labels work when errors are incoherent; this paper adds the coherent-error failure mode and the own-vote calibration window
- [[research/single-sample-rl-finetuning/rlsc-self-confidence]] — self-agreement reward without labels; here applied to abstention QA
- [[research/rlvr-mechanics/spurious-rewards-rlvr]] — cited directly; structured false negatives generalise, random noise is tolerated or memorised
- [[research/rlvr-mechanics/revisql-verified-data-reward-shaping]] — verifier quality as binding constraint
- [[conflicts/revisql-vs-spurious-rewards-noise-robustness]] — error structure vs error rate
- [[research/rlvr-mechanics/_overview]] — selection-not-learning theme
- [[research/rlvr-mechanics/what-outcome-rl-buys]] — RL gain as reliability compression
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]] — RL shifts which patterns are used, not competence
- [[research/rlvr-mechanics/rlvr-ood-gain-answer-format]] — parallels the form-travels exception
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]] — misspecified binary rewards and collapse (key runs collapsing to all-abstain)
- [[research/process-reward-models/corver-verifiable-rewards-factual]] — factual-QA reward design without a neural verifier
- [[research/process-reward-models/uprm]] — label-free reward from model's own signals
- [[research/self-improvement/self-rewarding-lm]] — self-grading
- [[research/test-time-training/tempo]] — label-free self-consistency/TTRL-style rewards
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction-not-correction line
- [[research/concept-evaluation/_overview]] — category-level held-out probe as concept-vs-instance test
- [[../weekly-briefs/2026-11-20]] — brought in by the 2026-11-20 weekly sweep
