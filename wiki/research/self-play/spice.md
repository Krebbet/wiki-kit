---
name: spice
description: Self-Play In Corpus Environments — Challenger reads a document and generates questions, Reasoner answers without the document; structural information asymmetry plus a variance-based curriculum reward yields +9.1% reasoning gains on Qwen3-4B-Base with no labeled data.
type: research
---

# SPICE: Self-Play In Corpus Environments

Liu, Jin et al. Meta. *SPICE: Self-Play In Corpus Environments Improves Reasoning*. arXiv:2510.24684 (October 2025). A single pretrained LLM plays two adversarial roles — Challenger (reads document $d$, generates question and gold answer) and Reasoner (answers without seeing $d$) — trained jointly via DrGRPO on a 20K-document corpus. A Gaussian variance reward calibrates the Challenger to target the Reasoner's frontier of capability. Results: Qwen3-4B-Base 35.8% → 44.9% (+9.1%); Qwen3-8B-Base +5.7%; OctoThinker-8B +11.9%; gains span math (+8.9%) and general reasoning (+9.8%). Critically, ungrounded self-play (no corpus) shows limited and unstable improvement, establishing that corpus grounding is the necessary ingredient.

## Method

**Single model, two roles.** Let $\mathcal{D}$ be a corpus of documents. A single policy $\pi_\theta$ operates in two modes:

- **Challenger** (role $= C$): receives document $d \sim \mathcal{D}$; produces $(q, a^*)$ where $a^*$ is extracted directly from $d$.
- **Reasoner** (role $= R$): receives only $q$ — document $d$ is not provided; produces answer $\hat{a}$.

**Information asymmetry** is structural: the Reasoner never sees $d$, so questions cannot be trivially solved by retrieval from the prompt.

**Variance-based curriculum reward (Challenger).** For valid $(q, a^*)$, sample $K$ Reasoner responses and compute binary correctness indicators $l_i = \mathbf{1}[\hat{a}_i = a^*]$. The Challenger reward:

$$r_C(q, a^*) = \begin{cases} \exp\!\left(-\dfrac{\bigl(\operatorname{Var}(\{l_1,\ldots,l_K\}) - 0.25\bigr)^2}{2 \cdot 0.01}\right) & \text{if } q \text{ is valid} \\ -0.1 & \text{otherwise (penalty)} \end{cases}$$

This Gaussian peaks at 1.0 when $\operatorname{Var}(\{l_i\}) = 0.25$, i.e., the Reasoner passes exactly 50% of the time (Bernoulli $p = 0.5$ has variance $p(1-p) = 0.25$). Temperature $\tau = 0.01$ creates sharp penalization for trivial (variance $\to 0$, pass rate $\approx 100\%$) or impossible (variance $\to 0$, pass rate $\approx 0\%$) tasks. As the Reasoner improves, the Challenger must propose harder questions to keep variance near 0.25 — automatic curriculum at the frontier of capability.

**Binary correctness reward (Reasoner):**

$$r_R(\hat{a}, a^*) = \mathbf{1}[\hat{a} = a^*]$$

verified by rule-based equivalence checking (MathVerify for math expressions, exact match otherwise).

**Joint objective.** Both roles are trained with shared weights via DrGRPO (role-specific advantage centering without standard-deviation normalization):

$$J(\theta) = \mathbb{E}_{d \sim \mathcal{D}}\!\left[\mathbb{E}_{(q,a^*) \sim \pi_\theta(\cdot|d,\,C)}\bigl[r_C(q,a^*)\bigr] + \mathbb{E}_{\hat{a} \sim \pi_\theta(\cdot|q,\,R)}\bigl[r_R(\hat{a},a^*)\bigr]\right]$$

$$\hat{A}^i_C = r^i_C - \operatorname{mean}(\{r^j_C\}_j), \qquad \hat{A}^i_R = r^i_R - \operatorname{mean}(\{r^j_R\}_j)$$

**Corpus:** 20,000 documents — Nemotron-CC-Math (math) + NaturalReasoning / DCLM subset (general). Segments up to 5,992 tokens. Training: 640 iterations, batch size 128, group size $G = 8$ responses per question (dual-purpose: variance computation for Challenger + DrGRPO advantage for Reasoner).

## Claims

| Model | Baseline | SPICE | $\Delta$ |
|---|---|---|---|
| Qwen3-4B-Base | 35.8% | 44.9% | +9.1% |
| Qwen3-8B-Base | 43.0% | 48.7% | +5.7% |
| OctoThinker-3B-Hybrid-Base | 14.7% | 25.2% | +10.5% |
| OctoThinker-8B-Hybrid-Base | 20.5% | 32.4% | +11.9% |

- **Math +8.9%, general reasoning +9.8%** average, covering MMLU-Pro, GPQA-Diamond, SuperGPQA, BBEH.
- **Corpus grounding is necessary:** without corpus (pure ungrounded self-play) 40.7% vs 44.9% for Qwen3-4B-Base; ungrounded improvement is limited and unstable.
- **Co-training the Challenger is essential:** a fixed Challenger (even Qwen3-32B-Instruct) underperforms full SPICE. Learning both roles simultaneously is critical.
- **Adversarial co-evolution is observed directly:** fixing a step-200 Reasoner and testing against later Challenger checkpoints drops pass rate from 55% to 35%; fixing a step-200 Challenger and testing against later Reasoner checkpoints raises pass rate from 55% to 85%.
- **Variance reward outperforms alternatives:** Absolute Zero 40.7%, Threshold 41.4%, R-Zero 43.6%, SPICE variance 44.9% on Qwen3-4B-Base.
- **Domain match matters:** Nemotron-CC-Math drives largest math gains; NaturalReasoning drives largest general-reasoning gains; combined corpus achieves best overall.

## Why this is load-bearing for single-sample concept learning

SPICE is the closest existing paper to the wiki's "textbook + exercises" frame, and provides a direct existence proof for the key mechanism in [[../synthesis/proposed-method]] component C.

The mapping is exact: document $d$ = reference text $T$ in component C. The Challenger reads the document and generates questions whose correct answers are grounded in it — exactly what component C describes ("the textbook chapter sits in the teacher's prompt before the question and the solution"). Challenger = teacher role; Reasoner = student role.

**Information asymmetry is the architectural alternative to RLT's $r^{KL}$ leakage penalty.** [[../teacher-student-rl/sakana-rlt]] prevents the teacher from trivially leaking the answer by adding a KL divergence penalty to the training objective. SPICE prevents it architecturally: the Reasoner simply does not receive document $d$ in its prompt. Both solve the same problem — answer leakage in a teacher-with-solution setup — but via different mechanisms: RLT uses a soft objective penalty; SPICE uses a hard prompt-level gate. The architectural approach is structurally cleaner and avoids tuning the $\lambda$ coefficient, but requires a two-role prompt structure rather than a single teacher prompt.

The **variance reward** is a practical, closed-form instantiation of SOAR's "edge-of-learnability" curriculum principle. SOAR implements this as a bilevel meta-RL optimization (outer reward = solver improvement rate); SPICE implements it as $\exp\!\left(-(\text{Var} - 0.25)^2 / 0.02\right)$, a tractable function of the current solver pass rate. The Gaussian form provides smoother gradients near the optimum than the piecewise R-Zero reward $1 - 2|p - 0.5|$.

The ablation establishing that ungrounded self-play collapses or hallucinates is load-bearing evidence that reference grounding is not optional: without corpus documents, the Challenger has no anchor for $a^*$, and the self-play loop drifts toward hallucinated, unfalsifiable question-answer pairs. This directly supports the design choice in the proposed method to keep a reference document in context throughout training.

**Key gap:** SPICE trains on 20,000 documents with both roles simultaneously trained. The wiki's method targets the single-sample regime — one textbook, 10–100 exercises, one small model. SPICE provides proof-of-concept that document-grounded information asymmetry works at scale; whether the mechanism survives compression to a single reference text with a small exercise set remains untested.

## Limitations

- Corpus must be sufficiently rich and diverse (20,000 high-quality documents). Performance degrades without the corpus. Compression to a single document is not tested.
- Both roles share weights; there is no separate teacher/student split. Precludes using a stronger teacher model to instruct a weaker student — a design the wiki's method explicitly targets.
- Requires $K = G = 8$ Reasoner samples per Challenger question to compute variance reward. Computationally feasible at corpus scale; may be expensive when the "curriculum" is a single worked-example set.
- Corpus domain must match target task domain for maximum gain; mixed corpus requires diversity.
- No evaluation of single-sample or few-shot generalisation from individual documents; all gains are average-aggregate across 7–11 benchmarks.
- Cannot exploit expert-authored pedagogical structure (textbook sequencing, definitions, proofs) since the system ingests raw documents without predefined questions or labels.

## Source

- `../../../raw/research/self-play-concept-learning/07-08-spice.md`
- arXiv: https://arxiv.org/abs/2510.24684

## Related

- [[../synthesis/proposed-method]] — component C (reference-in-context): SPICE's document $d$ is a direct implementation; information asymmetry is the enforcement mechanism
- [[../teacher-student-rl/sakana-rlt]] — RLT $r^{KL}$: soft-penalty alternative to SPICE's structural asymmetry; both prevent answer leakage in a teacher-with-solution prompt
- [[../teacher-student-rl/soar-edge-of-learnability]] — SOAR: SPICE's variance reward is a closed-form instantiation of SOAR's edge-of-learnability principle, avoiding bilevel optimization
- [[../self-improvement/multi-turn-policy-verifier]] — PAG: complementary; PAG focuses on process-level verification within a rollout; SPICE focuses on curriculum-level task selection across rollouts
- [[understanding-self-play]] — analysis of why proposer design dominates self-play outcomes
- [[sqlm]] — parallel self-play approach with Goldilocks gate but no corpus grounding
- [[_overview]] — self-play theme overview
