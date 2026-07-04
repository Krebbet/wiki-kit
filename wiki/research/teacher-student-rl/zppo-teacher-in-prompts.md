# ZPPO: Zone of Proximal Policy Optimization — Teacher in Prompts, Not Gradients

ZPPO (NVIDIA, arXiv:2606.18216) resolves the on-policy violation of gradient-level teacher injection by placing teacher knowledge inside specially constructed prompts rather than in the gradient target. On hard questions — those where the student fails more than half its rollouts — ZPPO constructs two prompt variants (BCQ and NCQ) that bring the question into Vygotsky's zone of proximal development (ZPD): tasks slightly beyond current capability but solvable with scaffolding. A graduation-gated FIFO replay buffer concentrates training time on the frontier of student competence. Evaluated on a 31-benchmark suite (16 VLM, 10 LLM, 5 Video) at four student scales (0.8B–9B), ZPPO outperforms GRPO, GRPO + replay, and both on-policy and off-policy distillation simultaneously — with the largest gains at smallest scale (+4.9 pp over GRPO† on VLM, +6.8 pp on LLM+Video generalization at 0.8B). Crucially, distillation *degrades* LLM and Video benchmarks at small scale while ZPPO improves across all three benchmark families.

## Method

### Base RL Objective

ZPPO layers on GRPO with DAPO modifications. Group-relative advantage for response $y_s(g)$ in rollout group $g$ on question $x$:

$$A(g) = \frac{r(x, y_s(g)) - \bar{r}_x}{\text{std}_x + \varepsilon}$$

where $\bar{r}_x$ is the group mean reward. ZPPO adopts REINFORCE++ two-step normalization: per-group mean subtraction followed by batch normalization excluding zero-advantage groups ("Norm w/o Zero"). From DAPO: clip-higher asymmetric clipping, token-level loss, no KL penalty.

### Hard-Question Identification

A question $x$ is **hard** when $\bar{r}_x < 0.5$ across $I=4$ rollouts. Standard GRPO discards these (zero advantage in expectation); ZPPO routes them to BCQ/NCQ construction.

### Binary Candidate-included Question (BCQ)

Given a hard question $x$:
1. Sample one teacher-correct response $y_T^+$ (verified by reward function).
2. Sample one wrong student rollout $y_S^-$ from the current batch.
3. Apply **teacher compression** to both under a shared token cap (abstracts long CoT while preserving the key reasoning pivot).
4. Anonymize both under identical `<candidate>` tags; shuffle order randomly.
5. Append to $x$ with instruction: "Here are two candidate responses in `<candidate>` tags. One is correct and another is wrong."

The student generates a fresh rollout group from the reformulated $x_\text{BCQ}$. The student must now discriminate — identifying the correct reasoning route — rather than generate from scratch. Teacher tokens in the prompt are conditioning context, not gradient targets. On-policy guarantee holds at the response level.

### Negative Candidate-included Question (NCQ)

Given a hard question $x$:
1. Collect all wrong student rollouts from the current batch on $x$.
2. Parse final answers from each failed rollout and list them: "The following answers are all WRONG: $\langle\text{parsed answers}\rangle$."
3. Append teacher-compressed reasoning traces for each failed response under `<candidate>` tags.
4. Append: "Below are the incorrect reasoning processes in `<candidate>` tags."

The student generates a fresh rollout group from $x_\text{NCQ}$. NCQ surfaces shared failure modes: the model is pushed to reason about why listed answers fail. Unlike BCQ, NCQ does not require the teacher to be correct — teacher traces compress student failures, which are always available.

### Graduation-Gated FIFO Replay Buffer

A FIFO buffer $\mathcal{B}$ storing questions only (responses are generated fresh on each replay):

- **Admission**: $x$ added to $\mathcal{B}$ when $\bar{r}_x < 0.5$ on first encounter.
- **Graduation**: $x$ removed from $\mathcal{B}$ when $\bar{r}_x \geq 0.5$ on a subsequent replay.
- **Eviction**: FIFO when at capacity.

At each training step, replayed questions from $\mathcal{B}$ are mixed with fresh questions; hard replayed questions receive BCQ/NCQ reformulation. The buffer concentrates training time on the ZPD frontier rather than sampling uniformly across easy/hard.

## Results

### VLM Benchmark Average (16 benchmarks)

| Scale | GRPO | GRPO† | ZPPO | ZPPO gain vs GRPO† |
|-------|------|-------|------|--------------------|
| 0.8B  | 43.8 | 45.4  | 50.3 | +4.9 pp            |
| 2B    | 58.7 | 59.2  | 62.0 | +2.8 pp            |
| 4B    | ~68  | ~68.5 | ~71  | ~+2.5 pp           |
| 9B    | ~76  | ~76.5 | ~78.5| ~+2.2 pp           |

GRPO† = GRPO + replay buffer only.

### LLM + Video Generalization (held-out benchmark families, delta vs. GRPO)

| Scale | Off-Distill | On-Distill | ZPPO  |
|-------|-------------|------------|-------|
| 0.8B  | −2.5 pp     | −2.2 pp    | +6.8 pp |
| 2B    | −1.8 pp     | −1.5 pp    | +4.3 pp |

Distillation degrades generalization at small scale; ZPPO improves all three benchmark families simultaneously.

### Component Ablation (0.8B VLM)

| Configuration           | VLM Average |
|-------------------------|-------------|
| GRPO                    | 43.8        |
| GRPO + Buffer (†)       | 45.4        |
| GRPO + BCQ + NCQ        | 45.2        |
| GRPO† + BCQ             | 48.6        |
| GRPO† + NCQ             | 46.2        |
| Full ZPPO               | **50.3**    |

Buffer × BCQ is super-additive: 48.6 vs. the additive prediction of 47.0 (+1.6 pp super-additivity). All three components required for full performance.

### Zone Dynamics

Tracking questions admitted to buffer at 0% student accuracy: ZPPO graduates 28% (432/1568) vs. GRPO†'s 4% (73/2035). For the next-hardest cohort (~25% accuracy): ZPPO 54% graduation vs. GRPO† 14%. Prompt-level scaffolding enables the student to learn from questions it would otherwise never solve.

### Scale and Teacher-Size Effects

- BCQ contribution dominates at small scale (0.8B/2B); NCQ contribution grows at large scale (4B/9B) as student improves and BCQ candidate pool shrinks.
- Shrinking the teacher from 27B to 9B or 4B collapses BCQ gains at small student scale — teacher must be meaningfully stronger than the student.

### Prompt-Level Baseline Comparison (0.8B)

| Method   | VLM Average |
|----------|-------------|
| Prefix   | 45.5        |
| Hint     | 47.2        |
| BCQ only | 48.6        |
| ZPPO     | 50.3        |

Prefix (teacher prefix + student completion) is worst due to off-policy/on-policy distribution mismatch. BCQ's discrimination framing beats soft scaffolding (hint).

## Limitations

1. **Teacher-bounded zone**: BCQ requires the teacher to succeed on hard student questions. When both student and teacher fail, only NCQ applies and its isolated contribution is modest.
2. **Tension with dynamic sampling**: DAPO's dynamic sampling deletes all-wrong groups before they contribute gradients; ZPPO's buffer specifically preserves them. Combining requires sequential scheduling — BCQ/NCQ reformulation first, then dynamic sampling — not naïve batch-level composition.
3. **BCQ pool depletion at large scale**: As student improves (4B/9B), teacher-correct candidates on hard questions become relatively scarce; system becomes NCQ-dependent.
4. **On-policy caveat**: The on-policy guarantee is informal. The prompt distribution $p(x_\text{BCQ})$ differs from the original training distribution $p(x)$ — a distribution shift even though student response tokens are on-policy. The paper does not formally prove this is harmless.
5. **Computational overhead**: BCQ requires parallel teacher generation at training time; teacher compression adds overhead relative to pure GRPO (quantified in Appendix D.3).

## Source

- arXiv:2606.18216 (NVIDIA) — *Zone of Proximal Policy Optimization: Teacher in Prompts, Not Gradients*
- Raw summary: `raw/research/weekly-2026-07-03/.ingest/05-zppo-teacher-in-prompts.summary.md`
- Models: Qwen3.5 family (0.8B–9B students, 27B teacher). Training data: ZPPO-77K (~77K image-question-answer triples from Vero-600K and MMFineReason-SFT-586K, filtered for hard examples).

## Related

- [[_overview]] — teacher-student RL overview; ZPPO is a new mechanism in this family: prompt-level teacher injection rather than gradient-level
- [[rlt-followups-2026]] — landscape note covering on-policy distillation variants; ZPPO explicitly refutes OPD's generalization claims at small scale
- [[sakana-rlt]] — RLT places teacher reasoning in the prompt too (Q + solution), but rewards student log-prob; ZPPO uses a discrimination/contrast framing with no log-prob reward
- [[soar-edge-of-learnability]] — bilevel teacher trained by student improvement; shares ZPD framing but trains the teacher rather than injecting it into prompts
- [[fan-learning-to-teach]] — canonical L2T; teacher controls curriculum/data rather than prompt content
- [[../../weekly-briefs/2026-07-03]] — brought in by the 2026-07-03 weekly sweep
