# What Does Privileged Information Add to On-Policy Self-Distillation?

Zhang, Chow, Fang, Liang, Chua (NUS, arXiv:2609.20612) build **AMPLE-MATH** — 5,319 math problems × 6 answer-matched reasoning views (ANSWER ONLY → GIST → KEY POINTS → CLEAN SOLUTION → SUMMARY → FULL TRACE) — to isolate what a teacher's privileged reference actually adds to on-policy self-distillation (OPSD) beyond a reference-free control (a thinking-enabled teacher scoring the student's direct-response prefixes with *no* privileged content at all). The headline finding: the added value of a genuine reference is small, model-dependent, and reverses sign when only the student's training-rollout mode changes — evidence the paper reads as **cross-mode capability access** (existing reasoning capability becoming more accessible through parameters shared by direct-response and thinking-enabled inference) rather than content transfer or low-confidence-token suppression.

## Method

- **OPSD loss** (Eq. 1): for problem $x$, view $v$ supplies privileged info $z_v(x)$ to a frozen teacher $\pi_{\bar\theta}$; student $\pi_\theta$ generates $y$ from the problem alone under rollout config $m_S$. The teacher scores student prefixes, $p^T_{v,t}(a) = \pi_{\bar\theta}(a \mid x, z_v(x), y_{<t}; m_T, \tau)$; the loss is a forward-KL $D_{gKL}(p^T_{v,t} \| p^S_t)$, clipped per-vocab-term at 0.05, averaged over supervised positions. A reference-free teacher with matching prompt/mode/temperature gives zero initial loss, so privileged information supplies only the *initial* discrepancy.
- **Six answer-matched views**, sharing one canonical answer, built from OpenThoughts-114k via Qwen3.6-35B-A3B generation with fidelity-checked review (13–4,916 mean tokens, ANSWER ONLY → FULL TRACE).
- **Privilege profiles** (Eq. 2–3): mean log-prob shift $\Delta_v$, correctness alignment $C_v$, correction-marker pressure, temporal KL allocation — diagnose what each view's supervision is doing to frozen and trained students without training a model.
- Trained: Qwen3-1.7B and SmolLM3-3B, LoRA (r=64, α=128), 100 steps. Primary config = **direct-response training rollouts + thinking-enabled evaluation** — an inherited teacher/student mode asymmetry present even in the reference-free control.

## Claims

| View | Qwen3-1.7B step-100 in-domain Δ | Notes |
|---|---|---|
| Reference-free (no PI) | +1.80 pts | Thinking-enabled teacher scores direct-response prefixes; no reference at all |
| ANSWER ONLY | +2.41 pts | Overlaps reference-free (CI) |
| CLEAN SOLUTION | +1.30 pts *over* reference-free | Strongest single-view evidence of added value; does **not** survive Holm correction across the six views |
| FULL TRACE | +2.38 pts | Statistically indistinguishable from reference-free |

- **Reference-free already recovers most of the gain.** At step 100, ANSWER ONLY and FULL TRACE sit ~0.6 pts above the reference-free student, both intervals including zero (§3.1). Holds on external benchmarks (AIME24/25, HMMT Feb 2025) too.
- **SmolLM3-3B shows a clearer but transient reference benefit**: FULL TRACE adds +2.0 pts over reference-free at step 50, but by step 100 all three tested configs fall *below* base, FULL TRACE degrading least.
- **Content is not fully fungible.** Replacing a genuine reference with a length-matched **other-problem** reference (wrong content, wrong answer) costs ~2 accuracy points vs. the genuine view — so content is not irrelevant even where reference-free training performs nearly as well.
- **Mode-reversal result (the paper's central mechanistic claim).** Switching only the student's training-rollout mode (direct-response → thinking-enabled), with the *identical* teacher and reference, flips gains into losses in both model families — "all nine gaps negative, eight significant" (Fig. 3). If OPSD's gain were a mode-agnostic, teacher-content-independent suppression effect, changing only the rollout mode (same teacher, same reference, same suppression opportunity) should not reverse the sign.

## Cross-mode capability access (the paper's mechanism)

The paper's account for *why* reference-free OPSD still helps: gains concentrate on problems the base model never solves in 4 direct-response attempts but solves 62% of the time with thinking enabled (Fig. 2c). Learning from teacher scores changes parameters shared by both inference modes, making existing thinking-mode capability more *accessible* under direct-response decoding — an "access," not "acquisition," account, closer to the wiki's existing "RL/distillation as selection, not new-skill installation" thread than to a content-driven concept-transfer account.

The paper also directly tests Kaur et al.'s (2026) "suppressed reconsideration" explanation for thinking-model degradation under OPSD and finds it only partly supported: every tested view suppresses reconsideration-marker probability in *both* prefix modes (shared sign — doesn't distinguish configs with opposite transfer outcomes), and relaxing the loss penalty at those markers barely changes marker use or accuracy.

## Limitations (authors' own)

- Many effects are single-seed comparisons (17 interventions, Table 2) with wide, often zero-crossing intervals; six-view contrasts require Holm correction, and most individual view effects don't survive it.
- **Checkpoint-selection confound**: apparent +4pt loss-window gains nearly vanish when checkpoints are matched at step 25 — a direct methodological warning about checkpoint-selection bias inflating apparent OPSD effects generally (cites Dodge et al. 2020, Bouthillier et al. 2021).
- Scope: two model families only (Qwen3-1.7B, SmolLM3-3B), math domain only, short LoRA runs (100 steps), self-distillation only (no separate/larger teacher tested).
- Not a sample-efficiency result — full mini-batches over ~1,536 training problems for 100 LoRA steps, not single/few-shot.

## Relevance to the project

This paper complicates both positions in the wiki's open [[../../conflicts/opsa-vs-opd-pattern-transfer]] conflict rather than cleanly resolving it — see that file's extension for the full argument. In brief: it corroborates Position A's ("no privileged content needed") headline direction but locates the mechanism somewhere Position A's diagnosis doesn't reach (cross-mode capability access, not content-independent low-logp-token suppression), and its content-swap result (−2pts for a wrong-problem reference) is evidence content is *not* fully fungible — which a strong reading of Position A would not predict.

## Source

- `raw/research/weekly-2026-09-18/01-privileged-info-opsd.md`
- arXiv:2609.20612

## Related

- [[opsa-teacher-free-self-adaptation]] — close sibling/rival on the teacher-free claim; see partial-corroboration/partial-complication discussion above
- [[opd-dual-nature-generalization]] — Position B (pattern-transfer) paper this source's dominant finding cuts against, but whose content-matters intuition the reference-swap result partially supports
- [[opsd-compresses-rlvr]] — "existing reasoning capabilities become more accessible through parameters shared by both inference modes" reading aligns with OPSD-compresses-RLVR's compaction-not-correction claim
- [[sequential-opd-then-rl]] / [[tgopd-verify-before-distill]] — same 2026-09-11 conflict-cluster papers; this source's checkpoint-selection-confound warning (Fig. 5) is a methodological point relevant to evaluating claims across that whole cluster
- [[../../conflicts/opsa-vs-opd-pattern-transfer]] — extended this week with this paper's dual complication of both positions
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
