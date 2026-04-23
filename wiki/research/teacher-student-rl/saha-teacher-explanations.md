---
name: saha-teacher-explanations
description: Saha, Hase, Bansal — NeurIPS 2023. LLM teacher intervenes at test time with natural-language explanations for a weaker LLM student; teacher builds a Theory-of-Mind mental model of the student to decide when to intervene and how to personalise explanations; multi-round interaction generalises to unexplained data.
type: research
---

# Can Language Models Teach Weaker Agents? Teacher Explanations Improve Students via Personalization

Saha, Hase, Bansal — UNC Chapel Hill, NeurIPS 2023, arXiv:2306.09299. Inference-time student-teacher LLM framework. A teacher LLM intervenes on a weaker student LLM by communicating a natural-language explanation for a test question; the student conditions on the explanation to predict. Under a budget (fraction of data the teacher may intervene on), the paper decomposes teaching into four research questions — *if*, *when*, *how*, and *whether explanations generalise to unexplained future data* — and answers each with a Theory-of-Mind-inspired mental model of the student.

## Method

Two-agent communication game. Student $S$ and teacher $T$ are both LLMs. For each test input $t^{(i)}$:

- **No intervention:** student generates both explanation $e_S^{(i)}$ and prediction $\hat{y}_S^{(i)}$ via Chain-of-Thought.
- **Intervention:** teacher generates $e_T^{(i)}$; student predicts conditioned on $(D, t^{(i)}, e_T^{(i)})$.

Communication is budget-constrained (0–100% of data). Four constructions:

1. **RQ1 — Random intervention baseline.** Teacher intervenes on random data points.
2. **RQ2 — Intervention Function (when to intervene).** Teacher builds a few-shot *mental model* of the student by simulating its pre- and post-intervention predictions (Expected Utility of Intervention). Ranks samples by expected utility; intervenes on the top-budget fraction. This is the Theory-of-Mind core.
3. **RQ3 — Personalisation (how to explain).** Teacher conditions on few-shot demos of *useful* human explanations — explanations that rectify a student answer — rather than generic ones, encouraging explanations that fill the student's specific gaps.
4. **RQ4 — Multi-round generalisation.** Teacher selects + explains a set of "best" points; those explained points go into the student's in-context demonstrations; student predicts on new data *without* further teacher intervention.
5. **RQ5 — Misaligned teacher.** Stress test with a teacher intentionally providing misleading explanations.

## Claims

- **Teacher LLMs can improve student predictions** across StrategyQA, GSM8K, CommonsenseQA, tested on Flan-T5-{Large, XL} and LLaMA-{7B, 13B, 65B} teacher/student pairs. More intervention monotonically raises student accuracy.
- **Human teachers still beat model teachers** at equal budget, but model teachers are non-trivial.
- **Expected-Utility intervention (RQ2)** outperforms random and other baselines; crucially, it *improves* student performance even when the teacher is not 100% accurate, and it enables weaker LLMs to teach stronger ones — something random intervention in RQ1 could not.
- **Personalisation (RQ3)** — prompts conditioned on usefulness-labelled human explanations beat unpersonalised explanation-generation prompts.
- **Multi-round generalisation (RQ4)** — student performance improves on *future unexplained data* after teacher-explained examples enter its prompt, i.e. explanations are not just test-time crutches.
- **Misaligned teachers** can degrade the student to random chance by intentionally misleading it (negative safety result).

## Positioning

The paper is the direct inference-time predecessor of RL-trained-teacher methods like [[sakana-rlt]]. Key differences: (a) *no weight updates to the teacher* — "training" is prompt construction; (b) the student-signal is the student's predicted answer, not log-probabilities; (c) budget constraint from rational-speech-acts theory rather than gradient cost. The contribution for the project is the four-axis decomposition — *if, when, how, transfer* — that every teacher-for-student method has to resolve, regardless of whether the teacher is RL-trained or prompted.

The *when* axis (Intervention Function) is notable: it implements a cheap, few-shot *simulation* of the student's future performance that avoids any back-prop through the student. The closest analogue in the project corpus is the RCE failure-trigger $F(x) = H/(M+\varepsilon)$ from [[../concept-learning/recursive-concept-evolution]] — both decide "should I act on this example?" from a cheap probe of the current model.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/02-saha-teacher-explanations.md`
- arXiv: https://arxiv.org/abs/2306.09299
- Code: https://github.com/swarnaHub/ExplanationIntervention

## Related

- [[_overview]] — theme synthesis
- [[sakana-rlt]] — RL-trained teacher version of the same loop (teacher weight update from student log-prob feedback)
- [[fan-learning-to-teach]] — pre-LLM ancestor of RL-trained teachers
- [[ho-reasoning-teachers]] — distillation analogue: teacher CoT frozen-in-weights via student SFT
- [[../concept-learning/recursive-concept-evolution]] — failure-trigger analogue to RQ2 Intervention Function
- [[../critique-self-correction/_overview]] — teacher as external critic for the student
