# Inherited, Not Invented: Provenance of "Wait" in Reasoning Models (Kou et al.)

Observational provenance study of the reflection marker "wait" across 120 open-model endpoints. Zero-RL from marker-free bases lifts MATH-500 accuracy by a median 42.9 points while the marker stays below 0.05 per 1k tokens in 17 of 18 runs; the marker is inherited from mid-training or reasoning-trace SFT, and RL only reshapes it in a recipe-dependent way (multiply, leave, or erase). Marker counts therefore do not show newly acquired reflection. A lexical-form result, not a test of reflective behaviour.

Note: built from an ingest summary; appendices (including D.2 failed pre-registered predictions and D.3 judge audit) were not read.

## Method

- **Design:** observational "diachronic corpus" over sampled outputs (MATH-500, 2-8 samples/problem) across checkpoints. Lineages confound data and recipe.
- **Label-free indices** from marker occurrences only: frequency (per 1k tokens; "absent" below 0.05); fixation (sentence-initial share SI plus positional entropy); form (canonical "Wait," share); bonding (reduplicated chains "Wait, wait"); erosion (distance to next math action); usage drift (Jensen-Shannon divergence of usage clusters vs base, against a split-half noise floor).
- **Alarm test:** correct prefix vs a copy with one injected arithmetic error; does a revision marker appear within two sentences? Scored with $d' = z(HR) - z(FA)$, $c = -0.5\,(z(HR) + z(FA))$.
- **Lineages:** (i) fully open OLMo-3 7B (pretrain, mid-train, base, RL-Zero or SFT/DPO/RL; 32B OLMo-3.1); (ii) authors' own zero-RL GRPO runs from marker-free bases (Qwen2.5-Math 1.5B/7B; DAPO and Open-Reasoner-Zero on Qwen2.5-32B); (iii) trace-SFT descendants (QwQ, R1-Distill, Phi-4, Qwen3, Llama, GLM, MiMo, SmolLM3).
- Pre-registered tests; blind human revision audits.

## Claims

| Result | Number |
|---|---|
| Zero-RL accuracy gain, MATH-500 (median) | +42.9 pts |
| Runs with marker still below 0.05/1k | 17 of 18 (9 Qwen2.5/Mistral/Qwen3 bases, 0.5B-32B) |
| Trace-SFT descendants of non-marking base adopting marker | 13 of 14 |
| Endpoints mapped | 120 |
| Extreme case | one OLMo-3 solution with 36 "wait" occurrences |

- Marker enters OLMo-3 at mid-training, not RL.
- Both released RL-Zero recipes (OLMo-3, MiMo) multiply an inherited marker; KL-free GRPO from the same base does not.
- OLMo-3's recipe erodes form (Wait, > wait > wait wait) and makes the alarm more sensitive but more liberal.
- RL after SFT barely changes the marker; the authors' GRPO recipe erases a marker seeded by light fine-tuning.
- An LLM judge reversed the human-labelled revision trend (Sec 5, App D.3).

## Relation to thesis

- **Not a sample-efficiency paper;** no single- or few-sample setting. Indirect relevance: large RL gains occur with no new surface reflection token.
- **Strong support for RL-as-selection/amplification of base or mid-training supply,** now at the token-form level ([[research/rlvr-mechanics/rethinking-rl-sparse-selection]], [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]). Marker survival is recipe-dependent, consistent with pattern-distribution selection.
- **Reframes the R1-Zero "aha moment"** as multiplication of an existing marker ([[research/single-sample-rl-finetuning/deepseek-r1]]); extends [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] with lexical provenance.
- **Accuracy decoupled from surface behaviour,** parallel to [[research/rlvr-mechanics/spurious-rewards-rlvr]].
- **Mid-training seeds reflection and conditions RL responsiveness** ([[research/process-reward-models/exprl-mid-training]]); GRPO recipe (KL or not) changes marker fate ([[research/rlvr-mechanics/deepseekmath-grpo]]).
- **Eval-design caution for concept acquisition:** marker frequency (or keyword counts, or LLM-judge reflection rates) is not evidence of acquired concept or reflection; a marker's evidential weight (HR/FA, $d'$) must be measured per checkpoint. Relevant to [[research/concept-evaluation/_overview]] and [[research/synthesis/recursive-concept-learning]]; self-revision metrics context in [[research/critique-self-correction/_overview]].

## Limitations

Stated:
- Observational; lineages confounded by data and recipe.
- Zero-RL claim rests on 18 runs; each open series is a single training run, so intervals reflect sampling variance only.
- Only 0.5B-32B, outcome-reward, English math.
- Alarm test uses only injected arithmetic errors.
- Judge-human agreement weak to moderate; audits are consensus labels, no double annotation.
- Several pre-registered predictions failed (App D.2).
- A model can reflect without writing "wait".

Unstated:
- One lineage is an exception to "inherited" (not identified in the slices read).
- Single token family studied.
- KL-free GRPO vs released recipes is not a controlled ablation at scale.
- Appendices unread here.

## Conflict notes

- **Soft:** vs [[research/single-sample-rl-finetuning/deepseek-r1]] if that page presents reflection or "aha" as emergent from RL alone. Mild, since this is a lexical-form claim, not a behaviour claim; verify page wording before any ruling.
- **Soft:** any wiki page relying on judge-based or keyword-counted reflection rates as evidence of acquired reasoning would be undercut (Sec 5, App D.3). None identified in the index.

## Source

- `raw/research/weekly-2026-10-23/05-inherited-not-invented-wait.md`
- arXiv:2610.30882 (Kou et al., HKUST/PKU/Huawei)

## Related

- [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]
- [[research/single-sample-rl-finetuning/deepseek-r1]]
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]
- [[research/rlvr-mechanics/spurious-rewards-rlvr]]
- [[research/process-reward-models/exprl-mid-training]]
- [[research/rlvr-mechanics/deepseekmath-grpo]]
- [[research/critique-self-correction/_overview]]
- [[research/rlvr-mechanics/_overview]]
- [[research/synthesis/recursive-concept-learning]]
- [[research/concept-evaluation/_overview]]
- [[../weekly-briefs/2026-10-23]] — brought in by the 2026-10-23 weekly sweep
