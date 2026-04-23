---
name: teacher-student-rl-overview
description: Theme overview — RL-optimised teachers and teacher-for-student-learning methods. Spans Fan et al. 2018 (canonical L2T), Saha 2023 (inference-time teacher), Ho 2023 (distillation), TRICE (latent-variable CoT), SOAR (bilevel meta-RL), Sakana RLT (student-likelihood reward), PM4GRPO (teacher-alignment reward). The unifying question: can a gradient from student feedback flow back into teacher parameters, and what feedback works best?
type: research
---

# Teacher-Student RL & Teaching-as-Optimisation

Theme covering methods where the *teacher* is optimised — or at least engineered — so that a *student* model produces better answers. This is the explicit-training analogue of David's informal goal "give the model a comprehensive example and grade whether it got the concept, not just the pattern". The unifying shape: a teacher generates some signal (data, rationale, explanation, curriculum), the student conditions on it, and the teacher is updated based on how well the student did. Methods differ along four axes: *who produces what*, *what the student feedback is*, *whether the teacher is trained*, and *whether the teacher sees the answer in its prompt*.

## Pages

- [[fan-learning-to-teach]] — Fan, Tian, Qin, Li, Liu (ICLR 2018). Canonical L2T: teacher RL agent outputs data / loss / hypothesis-space actions; REINFORCE on student validation accuracy. Halves data, transfers MNIST→CIFAR-10.
- [[saha-teacher-explanations]] — Saha, Hase, Bansal (NeurIPS 2023). Inference-time LLM teacher intervenes with natural-language explanations for a weaker student; Theory-of-Mind mental models for *when* (Intervention Function / Expected Utility) and *how* (personalisation) to intervene; multi-round teaching generalises to unexplained data.
- [[ho-reasoning-teachers]] — Ho, Schmid, Yun (ACL 2023). Fine-tune-CoT. GPT-3 175B teacher generates Zero-shot-CoT rationales; filter by answer; fine-tune small student. *Diverse reasoning* (multiple temperature-sampled rationales per question) is the critical extension.
- [[trice-cot-latent-variable]] — Phan, Hoffman et al. (NeurIPS 2023). Rationales as latent variables; maximise marginal log-likelihood of correct answer over rationales via MCMC-EM with control-variate variance reduction. Learns from incorrect rationales; beats STaR.
- [[soar-edge-of-learnability]] — Sundaram et al. (MIT/Meta FAIR, Feb 2026). Bilevel meta-RL; teacher generates synthetic Q–A pairs, student trains on them with RLVR, teacher rewarded by student's improvement on the real hard dataset. Escapes 0/128 plateaus. Structural quality beats answer correctness.
- [[sakana-rlt]] — Cetin, Zhao, Tang / Sakana AI (2025). Reinforcement-Learned Teachers. Teacher given (Q, A), rewarded by student log-prob of correct solution conditioned on teacher think-tokens, with a KL regulariser keeping explanations plausible from the student's no-solution perspective. 7B RLT beats DeepSeek-R1-scale distillation pipelines.
- [[pm4grpo]] — Lee, Park, Sim, Bae (Jan 2026). TACReward. Student-side: process-mining alignment between student and teacher reasoning traces produces a dense reward in $[0, 1]$; drops into RLOO/GRPO/GSPO without architectural change; GSPO + TACReward: +89.2% relative accuracy average.
- [[rlt-followups-2026]] — landscape note tracking post-RLT work (2025-Q4 → 2026-Q2): On-Policy Distillation (Qwen3 / MiMo / GLM-5 commercial adoption, Thinking Machines' Tinker), self-distillation with privileged info (OPSD, SDFT, SDPO), explanatory probes (ExGRPO), and systematic log-prob rewards (Kwiatkowski). **Finding: no captured follow-up directly cites RLT — the dense-teacher-signal family is advancing through OPD siblings rather than RLT's reference-in-prompt framing.**

## Cross-cutting synthesis

**The bilevel structure is shared; what changes is the action space and the student-feedback signal.** Every method except Ho (frozen teacher) and PM4GRPO (frozen teacher, student trained) fits the same bilevel shape: outer loop optimises the teacher, inner loop updates or evaluates the student, and a *reward* from the inner loop flows back to the outer. Fan 2018 established the shape; LLM-era methods inherit it.

**Does the teacher see the answer in its prompt?** This is the single sharpest axis. Methods split:

| Teacher sees the answer | Methods |
|---|---|
| Yes (teacher "connects the dots") | [[sakana-rlt]] (Q + solution in prompt), [[soar-edge-of-learnability]] (teacher generates both Q and A), [[trice-cot-latent-variable]] (initial rationales from a guide that conditions on $y$), [[ho-reasoning-teachers]] (answer-filter after Zero-shot-CoT — weaker form) |
| No (teacher solves from scratch) | [[fan-learning-to-teach]] (teacher outputs data/loss, no answer), [[saha-teacher-explanations]] (teacher solves the problem then explains), [[pm4grpo]] (teacher is a frozen reference whose trace is used for alignment — answer is implicit in the trace) |

The "yes" side corresponds to a much denser gradient and avoids RL's exploration problem. Sakana's framing makes this explicit: RLT turns on its head the traditional "solve from scratch" setup and gets dense feedback immediately. For the project's textbook-with-exercises setting, this is the natural match — the textbook *has* the solutions.

**What is the student's feedback signal to the teacher?**

| Signal | Methods | Density |
|---|---|---|
| Held-out validation accuracy | [[fan-learning-to-teach]] | Sparse, once per inner-loop epoch |
| Student's conditional log-prob of the correct answer | [[sakana-rlt]] ($r^{SS}$), [[trice-cot-latent-variable]] (marginal LL) | Dense, per-token |
| Student's improvement on a fixed hard dataset | [[soar-edge-of-learnability]] | Dense per candidate curriculum, sparse per student step |
| Student's prediction correctness (explicit answer) | [[saha-teacher-explanations]] (Expected Utility of Intervention) | Sparse, per test point |
| Process-mining alignment between student and teacher traces | [[pm4grpo]] (TACReward) | Dense, structural |
| Student's answer accuracy on future data (diverse CoT SFT loss) | [[ho-reasoning-teachers]] | Downstream only — no gradient back to teacher |

The density progression parallels the density progression in [[../process-reward-models/_overview]]: outcome → step → internal-signal. Sakana RLT's per-token log-prob is the densest per-gradient signal in the theme.

**Diversity in the rationale set is load-bearing everywhere.**

- [[ho-reasoning-teachers]]: multiple temperature-sampled rationales per question ("diverse reasoning") is what enables 0.3B students to beat the 175B teacher.
- [[sakana-rlt]]: 16-rollout analysis shows reward-ranked trace quality correlates $r = 0.89$ with student downstream performance.
- [[soar-edge-of-learnability]]: teacher-generated synthetic Q–A diversity is what lets a base LM unable to solve hard problems produce useful stepping stones.
- [[trice-cot-latent-variable]]: marginal likelihood *is* averaging over rationales; training-time MCMC over rationales is the mechanism.

This mirrors the "diversity and exploration are load-bearing" finding in [[../single-sample-rl-finetuning/_overview]] — single-sample methods that work all have an explicit diversity mechanism.

**Teacher quality beats teacher size.** Sakana RLT's main result: a 7B RL-trained teacher beats distillation from 670B+ teachers that lack the student-in-the-loop objective. SOAR's "grounded rewards beat intrinsic proxies" is the dual — *what you reward the teacher for* matters more than how big the teacher is. Both point at the same conclusion: the student's measured improvement is a stronger supervisor than scale or self-assessment.

**Answer-filter is a weak proxy for rationale correctness.** Flagged by [[ho-reasoning-teachers]] (especially on multiple-choice); addressed by [[trice-cot-latent-variable]] (explicit rationale posterior) and [[sakana-rlt]] ($r^{KL}$ plausibility term). Any textbook-loop design needs to decide how to detect "got the answer for the wrong reason".

**Teacher-as-curriculum vs teacher-as-explanation.** Two orthogonal action spaces:
- *Curriculum* ([[fan-learning-to-teach]] data-teaching, [[soar-edge-of-learnability]]) — teacher expands / reorders the problem distribution.
- *Explanation* ([[saha-teacher-explanations]], [[ho-reasoning-teachers]], [[sakana-rlt]], [[trice-cot-latent-variable]]) — teacher densifies the per-problem signal.
No paper composes the two. A SOAR-generated curriculum with RLT-style explanations per problem is an obvious-but-untried combination.

## Method comparison

| Paper | Teacher trained? | Teacher sees answer? | Student feedback | Scale of student | Distinctive design choice |
|---|---|---|---|---|---|
| [[fan-learning-to-teach]] | Yes (REINFORCE) | No (chooses data, not solutions) | Held-out val accuracy | MLP/CNN/RNN (image + text) | Generalises across action spaces (data/loss/hypothesis) |
| [[saha-teacher-explanations]] | No (prompted) | Teacher solves, then explains | Student prediction correctness, pre- vs post-intervention | LLaMA-7B to 65B, Flan-T5 | Expected-Utility of Intervention as few-shot student model |
| [[ho-reasoning-teachers]] | No (frozen 175B) | Weak: filter by answer | Student downstream accuracy (no gradient to teacher) | 0.3B to 6.7B | Diverse reasoning: multiple rationales per question |
| [[trice-cot-latent-variable]] | N/A (rationale is latent of same model) | Yes via hinted guide | Marginal log-likelihood of correct answer | Google LM (unspecified size) | MCMC-EM with control variate; learns from wrong rationales |
| [[soar-edge-of-learnability]] | Yes (RLOO) | Teacher generates both Q and A | Student improvement on $\mathcal{D}_{\text{train}}$ | Llama-3.2-3B-Instruct | Bilevel without BPTT; grounded rewards avoid diversity collapse |
| [[sakana-rlt]] | Yes (GRPO) | Yes (Q + solution in prompt) | Student $\log \pi_s(s_i \| t_{o_i}, q_i)$ + KL regulariser | 7B & 32B students from Qwen2.5 | $r^{SS} - \lambda r^{KL}$ dense reward; teacher "connects the dots" |
| [[pm4grpo]] | No (frozen reference) | — (teacher is a reference trace) | Student-teacher trace alignment | Math RL (GRPO/GSPO) | Process-mining alignment as label-free dense reward |

## Open questions

- **Can SOAR-style curriculum generation + RLT-style explanations compose?** SOAR expands the problem set; RLT densifies the per-problem reward. Both train teachers, but at different action spaces. No paper runs both in the same loop.
- **What is the minimum teacher–student capability gap for RLT-style dense reward to work?** Sakana trains the 7B teacher with a 7B student; scaling down student capability likely degrades the log-prob signal.
- **Does Sakana's $r^{KL}$ regulariser survive when the reference text is a textbook, not a curated solution?** The term forces explanations to be plausible under "student sees only the question" — load-bearing for reference-grounded variants. Untested.
- **How do TRICE's MCMC-EM guarantees translate to a setting where the "rationale" conditions on a large external reference document?** TRICE assumes rationale and answer are both latent of the same LM. Extending to "rationale conditioned on textbook chapter $T$" changes the posterior structure.
- **Can PM4GRPO's process-mining alignment work if the teacher trace comes from a textbook worked-solution rather than a frozen LM?** The paper assumes teacher traces come from a mature policy; worked solutions are a stronger form of reference but structurally different.
- **Concept-probe test.** None of these methods directly tests whether the student has installed the *concept* vs memorised the pattern. [[../concept-learning/recursive-concept-evolution]]'s MDL test is the closest hook; composing it with teacher-RL is unexplored.
- **Does the intervention-utility estimator (Saha RQ2) generalise from prompted few-shot mental models to trained Intervention Functions?** Worth testing: the Saha result that Expected-Utility intervention enables weaker teachers to teach stronger students would be significant if it survives scaling.

## Relation to the project skeleton

Relative to [[../synthesis/single-sample-concept-skeleton]]:

- **P1 trigger (RCE failure score).** [[saha-teacher-explanations]]'s Intervention Function is an inference-time analogue — a few-shot mental-model prediction of whether intervention will help. Both decide "act on this example?" without back-prop.
- **P2 sparse mask.** No teacher-student paper here touches the subnetwork question. Orthogonal.
- **P3 dense reward.** [[sakana-rlt]]'s $r^{SS}$ is a direct competitor to L2T's Fisher info-gain reward — per-token log-prob of the student recovering the correct answer vs per-episode Fisher trace. Both densify the signal. The RLT reward is *external* (requires a student LM); the L2T reward is *internal* (requires only the teacher's own Fisher). For a reference-grounded training loop, external-via-student-LM is the natural choice.
- **P4 principle decomposition.** [[saha-teacher-explanations]]'s Personalisation prompt conditions on "useful" human explanations — a soft form of principle decomposition. [[pm4grpo]]'s activity taxonomy (Formulate Strategy, Apply Formula, Verify Answer) is another.

The theme's load-bearing contribution to the skeleton: **the student's conditional log-probability on the correct answer is a cheap, dense, annotation-free reward signal for grading whether a specific explanation taught the concept.** That is the "stopping signal" slot the skeleton left open.

## Source PDFs

- `../../../raw/research/teacher-student-reasoning-rl/01-fan-learning-to-teach.md`
- `../../../raw/research/teacher-student-reasoning-rl/02-saha-teacher-explanations.md`
- `../../../raw/research/teacher-student-reasoning-rl/03-ho-reasoning-teachers.md`
- `../../../raw/research/teacher-student-reasoning-rl/04-soar-edge-of-learnability.md`
- `../../../raw/research/teacher-student-reasoning-rl/05-sakana-rlt.md`
- `../../../raw/research/teacher-student-reasoning-rl/06-pm4grpo.md`
- `../../../raw/research/teacher-student-reasoning-rl/07-trice-cot-latent-variable.md`

## Related themes

- [[../single-sample-rl-finetuning/_overview]] — downstream regime; RLT traces feed directly into 1-shot / small-N RLVR
- [[../rlvr-mechanics/_overview]] — base optimisers (GRPO, RLOO); L2T's info-gain reward is the internal-signal counterpart
- [[../process-reward-models/_overview]] — step-level dense rewards; PM4GRPO is the teacher-aligned variant
- [[../self-improvement/_overview]] — STaR is the teacher-less ancestor TRICE generalises
- [[../critique-self-correction/_overview]] — teacher-as-critic flavour; principle decomposition in CAI is adjacent to Saha RQ3 personalisation
- [[../synthesis/single-sample-concept-skeleton]] — project skeleton; theme provides the dense-reward slot candidate via Sakana RLT
