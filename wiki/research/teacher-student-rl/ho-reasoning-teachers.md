---
name: ho-reasoning-teachers
description: Ho, Schmid, Yun — ACL 2023. Fine-tune-CoT. Very large teacher (GPT-3 175B) generates CoT rationales via Zero-shot-CoT; filter by answer; fine-tune small student on them. Diverse reasoning (multiple temperature-sampled rationales per sample) is the critical extension. Enables 0.3B students to outperform 175B teacher on some tasks.
type: research
---

# Large Language Models Are Reasoning Teachers (Fine-tune-CoT)

Ho, Schmid, Yun — KAIST, ACL 2023. Classical reasoning-distillation. A large teacher LM (GPT-3 175B) generates CoT rationales for training questions via Zero-shot-CoT prompting ("Let's think step by step"); rationales whose final answer matches ground truth are kept and formatted as prompt-completion pairs; a much smaller student LM is fine-tuned on them with standard next-token objective. The teacher is *not trained* — this is one-way rationale distillation. A novel extension, **diverse reasoning**, samples multiple distinct rationales per training question (temperature sampling at high $T$) and adds them all to the training set; this produces most of the empirical gain.

## Method

**Step 1 — Reasoning generation.** Teacher $\pi^T$ (GPT-3 175B) is prompted with "Q: ⟨q_i⟩. A: Let's think step by step. ⟨$\hat{r}_i$⟩ Therefore, the answer is ⟨$\hat{a}_i$⟩." Task-agnostic; no hand-crafted CoT exemplars required.

**Step 2 — Curation.** Keep only completions where $\hat{a}_i = a_i$ (filter by final answer). Repackage as $(p_i, c_i)$ with prompt "⟨q_i⟩ ###" and completion "⟨$\hat{r}_i$⟩ --> ⟨a_i⟩ END". (Answer-based filtering does *not* verify rationale correctness, which the paper flags explicitly.)

**Step 3 — Fine-tune.** Standard next-token LM objective on the filtered pairs.

**Diverse reasoning extension.** Instead of greedy decoding per question, sample $D$ distinct rationales at temperature $T$ for each training question; keep all that pass the answer filter. $D$ = *degree of reasoning diversity*.

## Claims

Evaluated on 12 datasets across arithmetic (SingleEq, AddSub, MultiArith, GSM8K, SVAMP), symbolic (Last Letter Concat, Coin Flip), "other" (Date Understanding, Tracking Shuffled Objects), and commonsense (CommonSenseQA, StrategyQA) reasoning.

- **Fine-tune-CoT enables complex reasoning in small models** — models orders-of-magnitude smaller than prompt-based CoT's required scale (>100B) retain substantial reasoning performance.
- **Small students can beat the 175B teacher** on some tasks, driven by diverse reasoning.
- **Diverse reasoning is critical.** Most of the performance gain over vanilla Fine-tune-CoT comes from $D > 1$. The paper argues this is unique to reasoning distillation — sequence-level NMT distillation and standard KD get by with $D = 1$, but reasoning over multiple legitimate CoT paths benefits directly from the diversity.
- **Scalability across all axes** — performance scales with teacher performance, student size, dataset size, and $D$.
- **Filter caveat.** Answer-based filtering doesn't guarantee rationale correctness, especially for multiple-choice; can admit rationales that reach the right answer through bad reasoning.
- **Standard fine-tuning without rationales is inadequate** at small scale for these tasks — the rationale is what carries the signal.

## Positioning

Fine-tune-CoT is the classical distillation baseline every modern RL-teacher method compares against. The teacher is frozen and oblivious to the student; all of the "teaching" lives in the dataset curation and the diversity knob. What RL-teacher methods like [[sakana-rlt]] add is a *gradient from student feedback into teacher parameters* — closing the loop the Fine-tune-CoT paper leaves open.

Two claims from this paper survive into the RL-teacher era:

1. *Diversity of reasoning traces is load-bearing.* RLT's dense reward and CFT's 100-candidate explosion are two different mechanisms that aim at the same thing Fine-tune-CoT achieves via temperature sampling.
2. *Answer-matching is a weak proxy for rationale correctness.* RLT's $r^{KL}$ term and TRICE's ([[trice-cot-latent-variable]]) explicit rationale likelihood both directly address this — grading rationales on more than just the final answer.

## Source

- `../../../raw/research/teacher-student-reasoning-rl/03-ho-reasoning-teachers.md`
- ACL Anthology: https://aclanthology.org/2023.acl-long.830/
- Code: https://github.com/itsnamgyu/reasoning-teacher

## Related

- [[_overview]] — theme synthesis
- [[sakana-rlt]] — RL-trained teacher; directly competes against Fine-tune-CoT-style distillation pipelines and wins at small scale
- [[trice-cot-latent-variable]] — probabilistic reframing: rationales as latent variables, marginal-likelihood objective
- [[saha-teacher-explanations]] — inference-time analogue: teacher explanations improve student without weight update
- [[../self-improvement/star]] — STaR. Same "filter by correct answer, SFT on rationales" recipe but with the *same* model as teacher and student
- [[../single-sample-rl-finetuning/critique-ft-one-problem]] — one-problem critique FT; direct descendant of this distillation paradigm
