# OPD Transfers Skill, Not Knowledge (Tang & Yang)

Controlled factorial study (synthetic digit-lookup "facts" plus a one-model real-world check) showing that reverse-KL on-policy distillation (OPD) transfers compositional skill to unseen reasoning structures (79.10% on unseen trees vs 0.72% matched control) but almost no new factual knowledge (13.12% single-step held-out facts, 0.54% in chains). A second 2x2 shows KL direction, not prefix source, governs factual transfer: forward KL installs facts equally well from student or teacher prefixes, while student rollouts are what drive compositional execution. Facts and skill occupy near-orthogonal LoRA update subspaces at different depths.

## Method

- **Facts:** 25 random 2-arg digit lookup tables $T_k$ (100 entries each, applied digit-wise on 4-digit inputs); 20 initial, 5 held-out. No inferable rule, so pure memorisation.
- **Skill:** executing chains (sequential) vs branching trees (retain intermediates) over the same facts; 7 ops, 8 inputs, explicit step traces. Tree split into shared / teacher-only / unseen structures.
- **Student $S_0$:** fine-tuned on initial facts + single steps + chains; near-zero on held-out facts and trees.
- **Teachers (2x2):** $T_\emptyset = S_0$, $T_f$ (+held-out facts), $T_s$ (+trees on initial facts), $T_{fs}$ (both).
- **Loss:** token-level reverse KL over student rollouts, $\sum_t D_{KL}(P_\theta(\cdot\mid x,y_{<t}) \,\|\, P_T(\cdot\mid x,y_{<t}))$, normalised by completion tokens.
- **Second 2x2:** prefix source (student rollouts vs teacher demos) x divergence (reverse vs forward KL). Also GKD (JSD, $\beta=0.5$), ToDi (per-token sigmoid fwd/rev mix), EOPD (adds fwd KL at high-teacher-entropy positions).
- **Real world:** Qwen3-4B-Base -> Tulu-3-SFT student; knowledge teacher $T_K$ (SFT on 809 Knowledge-2026 QA), reasoning teacher $T_R$ (SFT on Nemotron competition math); distillation on prompts only, no demonstration traces. Synthetic models: Qwen3-0.6B/4B, Gemma-2-2B, OLMo3-7B (LoRA).

## Claims

| Result | Number |
|---|---|
| Rev-KL OPD from $T_s$, teacher-only trees (greedy, 4-model mean) | 80.96% (control 0.72%) |
| Same, unseen tree structures | 79.10%; Pass@32 88.11% |
| Rev-KL OPD from $T_f$, single-step held-out facts | 13.12% (control 0.03%; Gemma-2-2B 32.95%) |
| Held-out-fact chains | 0.54%; Pass@32 15.74% / 2.58% (single-step / chain) |
| Fwd KL, student prefixes, single-step facts | Qwen3-4B 10.95 -> 54.10; Gemma-2-2B 32.95 -> 94.10 |
| Fwd KL, teacher prefixes | 54.05 / 93.00 (no on-policy advantage for facts) |
| Objective sweep (Qwen3-4B, fact / unseen tree) | ToDi 64.3 / 86.4; fwd 54.1 / 76.4; rev 10.9 / 76.8; GKD 9.1 / 70.6; EOPD 13.7 / 78.7 |
| Real world: Knowledge-2026 | 11.25 -> 9.64 (teacher 84.55) |
| Real world: Math-2026 | 17.41 -> 23.88 (+6.47 pp; teacher 43.78) |
| Cross-capability | $T_R$ leaves knowledge at 10.75; $T_K$ moves math to 19.40 |

Student prefixes also lower NLL on reference tree completions under both KLs (Qwen3-4B 2.40 -> 1.77 rev, 2.13 -> 1.15 fwd).

## Mechanism

- **Reverse KL is support-bounded.** $D_{KL}(P_\theta\|P_T)$ weights errors by student probability; a fact with $P_\theta \approx 0$ incurs $\approx 0$ penalty and cannot be pulled in. Forward KL penalises missing teacher mass, so it can install facts. Same I-projection asymmetry used in [[research/rlvr-mechanics/binary-rewards-rl-challenges]] and the selection account in [[research/rlvr-mechanics/rlvr-pattern-selection-theory]].
- **On-policy states teach composition.** Credit lands at states induced by the student's own mistakes (tree flattened to left-to-right chain); this is where rollouts matter.
- **Failure signatures (Fig. 4):** knowledge failure = right format, wrong values; skill failure = right values, wrong order.
- **Parameter localisation (Sec 6.2):** LoRA updates from $T_f$ vs $T_s$ nearly orthogonal (cos 0.004-0.046), vs 0.64-0.82 for rev vs fwd KL on the same task. Facts concentrate in late layers (peak L35 of Qwen3-4B); skill in early/mid layers (peaks L3, L11).

## Limitations

- Toy domain (random digit lookups); mechanism evidence may not transfer to natural-language facts.
- Real-world check: one model, one run, small benchmarks (809 / 201 items), no variance. The 11.25 -> 9.64 drop is probably noise. Teachers were SFT'd on the eval items themselves.
- "No factual transfer" is model-dependent: Gemma-2-2B reaches 32.95% under reverse KL.
- Hybrid ToDi beats both pure KLs, so the fwd/rev dichotomy is incomplete.
- Reconciliation with SDFT-style factual acquisition (teacher with extra context) is only "different information sources"; teachers leaking facts via prompt context is untested.
- $T_\emptyset$ is the frozen $S_0$, not a noisy teacher, so this does not replicate OPSA's exact ablation.
- Appendices not read (truncated capture).

## Thesis relevance

- **Bounds what OPD-style few-example signals install.** Any single/few-sample OPD regime ([[one-shot-opd]]: one query recovers 62-89% of gain) is plausibly a skill/format-installing regime, not a fact-installing one. For the project's single-sample method, a concept that is a compositional procedure over knowledge the student already has is reachable by reverse-KL on-policy signal; a concept requiring genuinely new facts is not, and needs forward-KL-type or off-policy supervision (or hybrid ToDi).
- **Extends the reuse/selection thesis to distillation.** Same support-bounded structure as RLVR ([[research/rlvr-mechanics/rethinking-rl-sparse-selection]]): nothing outside student support is installed under mode-seeking objectives.
- **Evidence on the teacher-free debate.** Teacher-specific skill gain (79.10% vs 0.72%) is a Position-B-side data point in [[conflicts/opsa-vs-opd-pattern-transfer]], scoped to synthetic skill transfer.
- **Eval design.** The shared / teacher-only / unseen structure split is a clean compositional-generalisation test worth borrowing ([[research/concept-evaluation/_overview]]).
- **Composable R_w stack.** Near-orthogonal, depth-separated updates for facts vs skill align with knowledge-editing (late-layer) vs skill-localisation primitives ([[research/selective-finetuning/_overview]]).

## Source

- `raw/research/weekly-2026-10-16/01-opd-skills-not-knowledge.md`
- arXiv:2610.09639 (Tang & Yang, HKUST)

## Related

- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]] — KL direction over prefix source; this paper adds the facts-vs-skill split
- [[research/teacher-student-rl/opd-dual-nature-generalization]] — OPD transfers patterns, not answers
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction not correction; parallels "organises existing knowledge"
- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — teacher-free claim in tension with teacher-specific skill gain
- [[research/teacher-student-rl/sequential-opd-then-rl]] — pass@k coverage expansion is skill-type only
- [[research/teacher-student-rl/one-shot-opd]] — single-query OPD as skill installation
- [[research/teacher-student-rl/atd-active-taskless-distillation]] — capability transfer without task data
- [[research/teacher-student-rl/esr-early-stopping-opd]] — position/prefix axis of OPD
- [[research/rlvr-mechanics/rlvr-pattern-selection-theory]]
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]]
- [[research/selective-finetuning/_overview]]
- [[research/concept-evaluation/_overview]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[../weekly-briefs/2026-10-16]] — brought in by the 2026-10-16 weekly sweep
