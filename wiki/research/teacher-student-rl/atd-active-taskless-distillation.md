# Active Taskless Distillation (ATD): Post-Training Leaves Behavioral Shadows

arXiv:2609.29233 (Zhang, Jing, Zeng, Li, Wang, Gong; submitted 2026-09-24; code github.com/myboker/ATD). Capability transfers between models through task-unrelated text. ATD uses a single teacher-chosen word per prompt: select prompts where the teacher/student's shared public ancestor is nearly indifferent between two ordinary words, record the post-trained teacher's choice, and fine-tune a student (initialised from the ancestor) only on these prompt-word pairs. No target-task examples, teacher logits, or teacher parameters. Primary result: Qwen2.5-1.5B, 5,664 prompt-word pairs give +5.34 pp HumanEval+ over an exact nuisance-matched control. Extends subliminal-learning (trait/preference transfer via unrelated generations) to capabilities, at one token of supervision per prompt.

## Source

- `raw/research/weekly-2026-10-02/03-atd-active-taskless-distillation.md` (arXiv abs-page capture; abstract only. Capture text is partly garbled in the primary-result sentence; figures above are as legible)

## Claims

- Post-training leaves a "behavioral shadow" on decisions unrelated to the trained task; active selection of near-indifferent prompts (ancestor logit gap small) maximises how much of the update shows up as a one-word choice.
- Transfer also reported for scientific knowledge, commonsense reasoning, reading comprehension, across model generations, sizes, families.
- Learned shadow is composable, and its strength tracks the teacher's update strength.
- Requires a shared ancestor: the student must start from the teacher's pre-post-training checkpoint.

## Relevance

- Extreme low-bit regime for teacher-to-student transfer, in the same spirit as the wiki's single-sample thesis ([[one-shot-opd]]: one query recovers most OPD gain): here the amount of supervision per example is one token and the examples are off-task.
- Evidence that update direction is encoded broadly in a model's output distribution, consistent with sparse/low-rank-update accounts ([[../rlvr-mechanics/rl-sparse-subnetwork]], [[../rlvr-mechanics/context-grounding-mechanism-reuse]]), and a cautionary note for [[opsa-teacher-free-self-adaptation]] vs [[opd-dual-nature-generalization]]: teacher-specific content can transit through supervision that looks semantically empty. Not opened as a conflict (different regime: shared-ancestor, one-token labels).
- Security-flavoured caveat: data from a fine-tuned model can carry its capabilities (or traits) even when filtered for task relevance.

Caveat: abstract only; the nuisance-matched control design and effect sizes on non-coding tasks are not captured.

## Related

- [[_overview]] — teacher-student-rl cluster
- [[one-shot-opd]] — minimal-supervision OPD
- [[opd-dual-nature-generalization]] — teacher-origin pattern transfer
- [[opsa-teacher-free-self-adaptation]] — teacher-free OPD claim
- [[privileged-info-opsd]] — capability access across modes
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — sparse update structure
- [[../../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
