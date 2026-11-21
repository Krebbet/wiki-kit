# Agentic OPD Implicitly Reshapes ReAct Patterns (Kong, Li et al.)

Empirical study of (multi-teacher) on-policy distillation (OPD) from domain-specialised RL teachers into a Qwen3-4B-Instruct-2507 student, across math (GR, CI), ALFWorld and tau2-bench. Cross-domain transfer is large and signed: CI-OPD lifts ALFWorld 12.9 -> 40.2 and tau2 41.5 -> 51.0, while ALF-OPD collapses tau2 41.5 -> 6.6. The collapse is an over-generalised interaction habit (emit a request for user info and call the tool in the same turn), which the ALF teacher does not itself show on tau2. A source-only mitigation, signed-Delta Top95 token selection using the teacher's pre-/post-RL log-ratio, recovers tau2 11.5 -> 29.9 at a cost of ALF 87.6 -> 76.6. arXiv:2611.19244.

## Method

- OPD is PG-style with token-level reward $A_t = \mathrm{sg}[\log\pi_T(y_t|H_t) - \log\pi_\theta(y_t|H_t)]$ (k1 reverse-KL estimator), clipped plus dual-clip, loss averaged over retained tokens. MOPD routes each prompt to its domain teacher.
- Teachers: GRPO/DAPO-style RL Qwen3-30B-A3B (ALF update 60, tau2 update 160; GR = released checkpoint) and a 4B CI teacher (two-stage GRPO on 13.6k DAPO-Math17k with reward shaping).
- Mitigation (signed-Delta Top$\rho$): with $\pi_{pre},\pi_{post}$ the teacher before/after domain RL, on student-sampled tokens

$$\Delta_t=\log\frac{\pi_{post}(y_t|H_t)}{\pi_{pre}(y_t|H_t)},\qquad L_{select}=\frac1K\sum_t m_t\,\ell^{OPD}_t,\quad K=\lceil\rho N\rceil$$

  with $m_t=1$ for the top-$K$ positions by signed $\Delta_t$ per rollout. $\rho=0.95$ drops the most negative-$\Delta$ tail (tokens RL suppressed). Only source-domain (ALF) trajectories are used. Training is 20-60 updates.

## Key claims and numbers

1. **Signed cross-domain transfer.** CI-OPD: tau2 retail 48.1 -> 65.3, repeated actions 4.5 -> 0.7%, tool errors 32.6 -> 23.5%. GR-OPD: math tool-attempt rate 70.4 -> 14.4% with accuracy 16.7 -> 38.0 (route shift from tool to natural-language derivation). ALF-OPD: tau2 41.5 -> 6.6.
2. **Mechanism of collapse.** Ask-call co-occurrence 94.3% (base 0.04%, ALF teacher 0.67%); LLM-judged dependency violation 55.8% (base 0.5%). The student emits a user query and calls the tool with a schema-example ID in one turn. The "wait for user" feedback-dependency rule is not preserved.
3. **Task-matched MOPD helps, coverage matters.** ALF+tau2 teachers: tau2 68.9, ALF 83.4 (ALF-only 85.5), ask-call 0.24%. ALF+CI (no tau2 teacher): tau2 34.0, ask-call 25.6%.
4. **Token selection.** Top95 (ALF only): tau2 11.5 -> 29.9, ask-call 97.1 -> 24.3, ALF 87.6 -> 76.6. Top10%: ALF 14.3 -> 69.4 (about 80% of the gain from 10% of tokens) but tau2 41.5 -> 31.1. The last 5% of tokens is what collapses tau2.
5. **Controls (Table 5, Fig. 4).** Random95, delimiter / full-block / negative masking, Advantage Top95/98 (82.7% ask-call retained) and absolute-Delta Top95 all fail to match signed-Delta Top95's balance. Excluded tokens are 98% reasoning content and 19% of `<tool_call>` onsets.
6. **GR -> CI extension (Table 6).** Top95 raises CI tool attempts 10.41 -> 29.49%, tool-and-correct 6.02 -> 11.63; GR accuracy unchanged (46.0 / 46.3), CI accuracy slightly lower (36.5 vs 37.7).

## Results summary

| Setting | Target metric | Before | After |
|---|---|---|---|
| CI-OPD -> ALFWorld | success | 12.9 | 40.2 |
| CI-OPD -> tau2 | pass | 41.5 | 51.0 |
| GR-OPD -> math | accuracy / tool-attempt % | 16.7 / 70.4 | 38.0 / 14.4 |
| ALF-OPD -> tau2 | pass | 41.5 | 6.6 |
| ALF+tau2 MOPD | tau2 / ALF | - | 68.9 / 83.4 |
| ALF+CI MOPD | tau2 / ask-call | 41.5 / 0.04% | 34.0 / 25.6% |
| ALF-OPD + signed-Delta Top95 | tau2 / ALF | 11.5 / 87.6 | 29.9 / 76.6 |

## Limitations

- Single model family (Qwen3), 4B students; math and interactive tasks only; recipe-dependent selection effect.
- Source-learning trade-off (ALF -11 pts); GR -> CI variant lowers CI accuracy; task-matched teachers do not cover unseen domains.
- Unstated or weak: the LLM-judge dependency-violation metric is not validated in the main text; Top95 tested at only 20 updates, apparently one seed; no comparison against early stopping, KL or weight-space regularisation.
- The effect may be tool-call-onset timing rather than $\Delta$ per se (19% of `<tool_call>` onsets excluded), though delimiter masking fails. The ALF-only tau2 6.6 may partly reflect prompt-format drift (shared tool_call serialisation). tau2 base 41.5 vs teacher 46.0 gives a low ceiling.
- Not a sample-efficiency paper: large rollout batches, 3,553 ALF and 2,160 tau2 prompts. No single-sample or concept probes.

## What it means for our thesis

- **Concept scoping failure.** The supervision signal is absorbed as a surface interaction habit, not a scoped concept. This is the failure we must guard against when fine-tuning 1-40B LLMs from one sample or one concept: gains on the source and large unmeasured damage elsewhere. Evaluate cross-domain pattern metrics (ask-call, repeat, tool-route rates), not only target accuracy.
- **Token sparsity again.** 10% of tokens give about 80% of the source gain, consistent with other sparse-token OPD results ([[research/teacher-student-rl/ier-gradient-reliability-opd]], [[research/rlvr-mechanics/high-entropy-minority-tokens]]), which supports single-sample regimes concentrating the update on a few tokens.
- **Teacher RL-delta as a selector.** $\Delta_t=\log\pi_{post}/\pi_{pre}$ isolates what RL changed from the base prior; a cheap, source-only gate usable where a concept teacher is available. Closest precedent: Heo et al. 2026 On-Policy Delta Distillation (2607.15161), a follow-up lead.
- **Risk of single-source specialisation.** A one-domain teacher can silently break an untouched capability (here by 35 pts); regression suites across tool and dialogue behaviours should be part of any concept-learning eval.

## Conflicts

- **Extension of [[research/teacher-student-rl/opd-dual-nature-generalization]]:** pattern transfer holds, but the harmful pattern (ask-call 94.3% on tau2) is student/environment-induced and absent from the teacher (0.67%), so transfer is not teacher mimicry.
- **Tension with Position A in [[conflicts/opsa-vs-opd-pattern-transfer]]:** if OPD gains were just teacher-free low-logp suppression (OPSA), random or advantage-based selection should do comparably. Here signed-Delta Top95 beats Random95 and Advantage Top95, so teacher signal location matters. Caveat: single seed, 20 updates, and a tool-call-onset confound.
- **Open:** [[conflicts/on-policy-forgetting-vs-lr-confound]] is possibly relevant (negative transfer under on-policy training); this paper has no LR control.

## Source

- raw/research/weekly-2026-11-20/02-agentic-opd-react-patterns.md (arXiv:2611.19244)

## Related

- [[research/teacher-student-rl/opd-dual-nature-generalization]]
- [[research/teacher-student-rl/dn-mopd-domain-normalized]]
- [[research/teacher-student-rl/mopd-gradient-diagnosis]]
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]]
- [[research/teacher-student-rl/ier-gradient-reliability-opd]]
- [[research/teacher-student-rl/sg-opd]]
- [[research/teacher-student-rl/tgopd-verify-before-distill]]
- [[research/teacher-student-rl/opd-skill-vs-knowledge-transfer]]
- [[research/teacher-student-rl/opd-mismatch-tolerance]]
- [[research/teacher-student-rl/gc-opd-group-calibrated]]
- [[research/teacher-student-rl/adrs-self-distilled-reward-shaping]]
- [[research/teacher-student-rl/sequential-opd-then-rl]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[research/rlvr-mechanics/high-entropy-minority-tokens]]
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/catastrophic-forgetting/rls-razor]]
- [[research/catastrophic-forgetting/_overview]]
- [[research/single-sample-rl-finetuning/_overview]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[conflicts/on-policy-forgetting-vs-lr-confound]]
- [[../weekly-briefs/2026-11-20]] — brought in by the 2026-11-20 weekly sweep
