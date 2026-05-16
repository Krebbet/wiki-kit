# OPSD Compresses What RLVR Teaches: A Post-RL Compaction Stage

arXiv:2605.06188, May 2026. In thinking-enabled mathematical reasoning, on-policy self-distillation (OPSD) acts as a **safe compaction** of already-correct trajectories rather than a correction mechanism for failed ones. Correct-only OPSD: −29% length with near-zero accuracy change. Incorrect-only OPSD: −7 to −10 pp accuracy across seeds, models, divergence variants, and richer teacher contexts. Motivates the pipeline **SFT → RLVR → OPSD**: RLVR expands reachable trajectories; OPSD compacts them; OPSD cannot create new reasoning states the student's distribution doesn't already support.

## Source

- `raw/research/weekly-2026-05-10/02-opsd-compresses-rlvr.md`

## Method

**OPSD loss (Eq. 1):**

$$\mathcal{L}_\text{OPSD} = \mathbb{E}_{x, y \sim \pi_S(\cdot|x)}\left[\sum_t D_\text{KL}(\pi_S(\cdot|x, y_{<t}) \| \pi_T(\cdot|x, c, y_{<t}))\right]$$

Per-token advantage (Eq. 3): $A_t^\text{OPSD} = \log \pi_T(y_t | s_t, c) - \log \pi_S(y_t | s_t)$. The teacher $\pi_T$ is the student's own initial weights with a richer prompt context $c$ (worked demo, re-solve).

**Diagnostic intervention.** Outcome-filtered OPSD: train separately on **Correct-only** vs **Incorrect-only** rollouts, isolating which states drive what behavioural change.

**OPSD ≠ RFT.** Correctness gates *which states* enter the KL loss, not *which token* is the update target — the per-token advantage is teacher-preference, not outcome-anchored. Distinct from rejection-sampling fine-tuning (STaR) at the loss level.

## Results

On Qwen3-8B and AceReason-Nemotron-7B (post-RLVR with GRPO):

| Variant | Length Δ | Accuracy Δ |
|---|---|---|
| Correct-only OPSD (Qwen3-8B) | −29% | −1.0 pp |
| Correct-only OPSD (AceReason-7B) | −29% | +3.5 pp |
| Incorrect-only OPSD (Qwen3-8B) | (variable) | −6.6 pp |
| Incorrect-only OPSD (AceReason-7B) | (variable) | −10.0 pp |

Compression regime reached in ~25 steps (4× H100, ~6 hrs/100 steps). Epistemic-marker density (wait/hmm/perhaps) drops 23% under Correct-only.

**Robustness.** The compression-not-correction pattern holds across reverse-KL / JSD / forward-KL on incorrect, mid-trace signal reinjection, richer teacher contexts, and up to 500 training steps. Front-loaded per-token KL (Fig. 2). Length saturates early, accuracy oscillates below baseline (Fig. 3).

## Connections to the wiki

- **[[_overview]]** — repositions OPSD as post-RL compaction, not RLVR replacement.
- **[[rlt-followups-2026]]** — sits in the same 2026 OPD/self-distillation wave; Correct-only OPSD ≈ OPSDC from CRISP (arXiv:2603.05433). **Name-collision note (2026-05-16):** this page is arXiv:2605.06188 (*OPSD Compresses*, May 2026). The "OPSD" in [[rlt-followups-2026]] §4 is a *different* paper — Zhao et al. arXiv:2601.18734 (*On-Policy Self-Distillation*, Jan 2026, 4–8× token efficiency). Same abbreviation, distinct methods; do not conflate.
- **[[co-evolving-policy-distillation]]** (CoPD, 2026-05-03 sweep) — both layer distillation atop RLVR. CoPD co-evolves teacher; OPSD freezes teacher at student's initial weights. Companion picture: RLVR creates trajectories; CoPD raises teacher; OPSD shortens.
- **[[../rlvr-mechanics/_overview]]** — pipeline claim **SFT → RLVR → OPSD**. RLVR-then-OPSD is sequential and complementary, not substitutive.
- **[[../self-play/yue-rlvr-boundary]]** — OPSD's failure on incorrect rollouts is another angle on the same RLVR boundary: hindsight cannot reliably supply missing reasoning states.
- **[[../self-improvement/star]]** — OPSD distinct from STaR's rejection-SFT despite surface similarity; correctness gates state-entry, not token-target.
- **[[../synthesis/proposed-method]]** — directly relevant to the SFT→RLVR→X pipeline shape. Suggests a post-stage compaction module is "free" relative to length-penalty RL.

## Conflicts

- **vs. thinking-disabled OPSD gains.** SDFT reports +25 pp, SDPO +24 pp; this paper measures −1.0 pp on Qwen3-8B Correct-only. Not a hard contradiction: regime boundary between thinking-enabled vs thinking-disabled mathematical reasoning. Tracking as a regime distinction in [[_overview]].
- **vs. naive OPSD ≈ RFT framing.** Surface similarity but Eqs. 2–3 distinguish: correctness filters states, teacher-preference drives token advantage. Paper explicitly rebuts the conflation.

## Related

- [[_overview]]
- [[rlt-followups-2026]]
- [[co-evolving-policy-distillation]]
- [[sakana-rlt]]
- [[../rlvr-mechanics/_overview]]
- [[../rlvr-mechanics/deepseekmath-grpo]]
- [[../self-play/yue-rlvr-boundary]]
- [[../self-improvement/star]]
- [[../synthesis/proposed-method]]
- [[../single-sample-rl-finetuning/_overview]]
- [[../test-time-training/tempo]] — companion week-of trace-efficiency angle (different mechanism)
- [[../../weekly-briefs/2026-05-10]] — brought in by the 2026-05-10 weekly sweep
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] **(crossover added 2026-05-13)** — REASONMAXXER and OPSD are both dense-signal methods at sparse "active" positions, with different gates (self-entropy vs teacher-student divergence) likely indexing the same position set. See the "Crossover with OPD-family" subsection on that page for the full comparison. Five real differences survive the "same positions" reading: teacher-requirement, signed-vs-one-sided update, failure-mode shape, pipeline position, and offline-vs-on-policy gating. Composing REASONMAXXER (RL-replacement) → OPSD-style compaction is non-redundant; untested in the captured corpus.
