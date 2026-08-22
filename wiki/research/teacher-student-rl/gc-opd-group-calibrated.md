---
name: gc-opd-group-calibrated
description: GC-OPD calibrates dense OPD token advantages against a task verifier via a group-normalized signed residual (GRPO-style z-scoring) plus a bounded relative-advantage token credit (RACA), fixing OPD's blind spot at long context where teacher-likelihood diverges from verified correctness
type: research
---

# Beyond Teacher Likelihood: Group-Calibrated On-Policy Distillation for Long-Context Reasoning

Zhang, Wang et al. (Tsinghua/BUPT/OpenBMB), arXiv:2608.19181. GC-OPD is a fourteenth entry in this wiki's OPD-variant lineage: it calibrates OPD's dense per-token teacher-likelihood advantage against a task verifier's response-level reward, motivated by a diagnostic showing the two signals **diverge as context grows** — pairwise disagreement between "teacher prefers" and "verifier confirms correct" rises from 40.6%→64.0% (Multi-Table Extraction) and 35.2%→60.2% (High-Recall Retrieval) between <8K and 32–64K token prompts, with the preference-gap sign flipping (+0.35→−0.37 and +0.65→−0.35). At long context, dense teacher-likelihood increasingly rewards "locally plausible but globally incomplete" responses that omit distributed evidence.

## Method

Standard OPD advantage: $A_t^{(i)} = \log\pi_T(y_t|h_t) - \log\pi_{\theta_\text{old}}(y_t|h_t)$, whose expectation is the negative reverse-KL to the teacher. GC-OPD adds a calibration term on top, within each rollout group of $G=8$:

1. Aggregate to a trajectory-level OPD score $s^{(i)} = \frac{1}{T^{(i)}}\sum_t A_t^{(i)}$.
2. z-score-normalize both verifier reward $R^{(i)}$ and OPD score $s^{(i)}$ within the group (GRPO-style), forming the **signed teacher–verifier disagreement residual** $\rho^{(i)} = \tilde R^{(i)} - \tilde s^{(i)}$ — provably verifier-consistent in ordering under strict disagreement.
3. Compute **RACA** (Relative-Advantage Credit Allocation): normalize each token's OPD advantage relative to the response mean/std into $u_t^{(i)}$, then map through a bounded monotonic $c_t^{(i)} = 1+\tanh(u_t^{(i)}/2) \in (0,2)$.
4. Final advantage: $A_t'^{(i)} = A_t^{(i)} + \beta\, c_t^{(i)}\,\rho^{(i)}$, clipped to $[-10,10]$, substituted into the standard clipped PPO-style token objective. $\beta=0$ recovers vanilla OPD.

**Degenerate-group guard:** if within-group reward or token std falls below a threshold, the residual/credit is zeroed — GC-OPD silently reduces to vanilla OPD for that group. This is the same "zero-variance/mastered-prompt" blind spot recurring elsewhere in the GRPO-family literature ([[../rl-optimizers/grpo-std-identity]]), not resolved by this paper.

## Results

Five long-context benchmarks (DocMath, Frames, MRCR, CorpusQA, LBv1QA), Qwen3-4B/8B, 100-step controlled comparison against reimplemented baselines:

| Method | Qwen3-4B avg | Qwen3-8B avg |
|---|---|---|
| Raw checkpoint | 29.08 | 35.12 |
| Vanilla OPD | 39.31 | 43.56 |
| ExOPD / Uni-OPD / PowerOPD / FiRe-OPD (best per-benchmark, not aggregate) | — | — |
| **GC-OPD** | **40.47** | **44.65** |

Ablation (Qwen3-8B): +another OPD-derived term barely moves the needle (43.56→43.60); +group-normalized verifier reward directly → 44.19; **signed residual** (not direct addition) → 44.65 (full method). Token allocation: uniform residual distribution alone → 44.28; RACA → 44.65; sign-discarding "absolute-OPD" credit → 43.93 (worse than uniform) — the *sign* of the residual, not just its magnitude, is load-bearing.

## Limitations

- $\beta=0.10$ selected from a narrow 231-example single-task-family holdout, reused unchanged across both scales and all 9 training task families — untested generalization of the coefficient.
- RACA's $u_t^{(i)}$ is explicitly stated by the authors as an allocation heuristic, "not token correctness or causal importance" — no causal validation.
- Requires an existing task-specific verifier (binary/graded reward); inapplicable without one.
- Single teacher (Qwen3-30B-A3B-Thinking-2507), single data source (GoLongRL); cross-domain generality (math/code RLVR rather than long-context evidence-aggregation) untested.
- Not a sample-efficiency contribution — standard-scale RL post-training (9,527 prompts, 100 steps); the contribution is signal *quality*, not signal *count*.

## Relation to the wiki

The core diagnostic — dense teacher-likelihood support diverging from verified task success as context grows — reinforces [[opsd-compresses-rlvr]]'s "compaction not correction" claim: pure teacher-likelihood is an imperfect proxy for what should be reinforced, and GC-OPD's verifier residual is injecting exactly the "correction" component OPSD argues pure OPD lacks. It also parallels [[rstg-selective-negative-group-distillation]]: both papers are, from different angles, wrestling with what to do about low-diversity/degenerate rollout groups in group-relative OPD (RSTG gates hard on zero-variance groups; GC-OPD calibrates continuously but keeps an equivalent zero-variance guard as a fallback).

## Source

- `raw/research/weekly-2026-08-21/02-group-calibrated-opd.md`

## Related

- [[sg-opd]] — direct sibling: another verifier-aware OPD variant (sign-consistency gating + phased teacher sampling); GC-OPD's related work explicitly critiques SG-OPD for not simultaneously preserving graded within-group outcome differences while translating response-level discrepancy into token-level calibration.
- [[rstg-selective-negative-group-distillation]] — parallel handling of degenerate/zero-variance rollout groups in OPD, via hard gating (RSTG) vs. continuous calibration with a fallback guard (GC-OPD).
- [[mad-opd]] — a different "beyond a single fixed teacher" extension (multi-teacher debate ensemble vs. single-teacher + verifier calibration).
- [[opsd-compresses-rlvr]] — GC-OPD's diagnostic reinforces the compaction-not-correction claim; its verifier residual is the "correction" component OPSD lacks.
- [[../rlvr-mechanics/deepseekmath-grpo]] — GC-OPD borrows GRPO's group-relative z-score normalization as its central technical device.
- [[../rl-optimizers/grpo-std-identity]] — GC-OPD's zero-variance guard is the same edge case this page formalizes for GRPO/Dr.GRPO/DAPO.
- [[../process-reward-models/_overview]] — RACA positions itself against PRM-style step-level credit assignment, using only the existing token-level OPD advantage instead.
- [[../../weekly-briefs/2026-08-21]] — brought in by the 2026-08-21 weekly sweep
