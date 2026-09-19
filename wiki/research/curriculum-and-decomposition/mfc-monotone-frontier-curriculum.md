# Unlocking the Unsolvable: Monotone Frontier Curriculum (MFC)

Zhu & Han (arXiv:2609.13997) show that problems a model can *never* solve under GRPO (pass@64 = 0 — a structurally zero-gradient set) can be converted into a rich RLVR training signal via teacher partial-trace hints plus a backward-chaining guidance curriculum. Their method, **Monotone Frontier Curriculum (MFC)**, trains on only 128 such "unsolvable" problems and matches or exceeds GRPO trained on a 2,000-problem corpus (~16× fewer source problems, matched GRPO step count) while expanding the pass@k reasoning boundary out to k=256.

## Method

- **N-unsolvable problem**: pass@N($\pi_0$, s) = 0 (N=64; n=8 GRPO rollouts/group ⇒ uniform-failure groups give $\sigma_g=0$, zero advantage, vanishing gradient — ~7% / 147 of a 2,000-problem OpenR1-Math corpus for Qwen3-1.7B).
- A stronger teacher (DeepSeek-V3.2) generates a step-structured trace $T(s)$; guidance level $\rho \in [0,1]$ exposes the first $g = \text{round}(\rho \cdot n_\text{steps}(s))$ steps as an in-prompt hint ($s_\rho = s \cup$ first $g$ steps); the student must still generate a full solution. One dead problem becomes a graded-difficulty family of states.
- **Three curriculum families over $\rho$** are compared: **staged** (single global schedule — excluded as baseline, known scheduler-fragile), **Mixture** (R³-style, Xi et al. 2024 — replicate each problem at M=5 discrete $\rho$-levels, uniform sampling), **per-sample adaptive** ([[adaback-adaptive-rationale|AdaBack]] — bidirectional binary search: success sets $g_\text{max} \leftarrow g_\text{used}$ & resets $g_\text{min} \leftarrow 0$; failure raises $g_\text{min} \leftarrow g_\text{used}$).
- **MFC** (this paper's contribution): keeps only the success-side ratchet — a single per-sample integer $g_\text{curr}(s)$, initialized to $n_\text{steps}(s)$, lowered ($g_\text{curr} \leftarrow g_\text{used}$) only on a successful visit ($\bar r \geq \tau{=}0.5$) with $g_\text{used} < g_\text{curr}$; sampled $g_\text{used} \sim \text{Uniform}\{0,\ldots,g_\text{curr}(s)\}$ each visit; failures leave state untouched but still contribute to the GRPO advantage. Monotonically non-increasing per-sample frontier ⇒ unguided-visit probability $1/(g_\text{curr}(s)+1)$ rises monotonically with demonstrated competence.
- All four arms (GRPO-2k, Mixture, AdaBack, MFC) share an identical GRPO core (batch 128, n=8, temp 1, lr 1e-6, KL coeff 1e-3, 8192-token cap) plus DAPO clip-higher + overlong-response-penalty stabilizers, 1200 steps.

## Claims

| Arm | Cross-bench avg (1.7B) | Uns-22 | AIME24/25/26 avg |
|---|---|---|---|
| GRPO-2k (2,000 problems) | baseline (44.3) | baseline | baseline |
| AdaBack (128 unsolvable) | within 0.7–3.3pp of GRPO-2k | — | — |
| **MFC (128 unsolvable)** | **47.3** (best) | **+7.9/+6.8pp** | **+4.7/+3.7pp** |

- Ordering **MFC > AdaBack > GRPO** holds on both tested base models (Qwen3-1.7B, Qwen3-0.6B) on cross-bench average, Uns-22, and AIME average.
- Mixture (640 rows) is competitive on 1.7B but trails GRPO on 0.6B — uniform-$\rho$ mixing alone is insufficient at small scale.
- Non-math OOD (SciBench, GPQA-Diamond): no degradation, mild positive transfer for MFC (+1.2 to +4.4pp over base).
- **The "16×" claim is matched-steps, not matched-compute** — 1200 GRPO steps across all arms, but guided arms carry longer prompts (hint tokens) that GRPO-2k does not. Read as "16× fewer source problems," not "16× less compute."

## Is this just distillation? (§5.2 ablation)

Directly tests the objection: an SFT baseline trained on the *same* Uns-128 problems + full teacher traces ($\rho=1$, next-token prediction, 50 epochs) improves only +3.0pp over base, vs. AdaBack +9.0pp / MFC +10.5pp. *"SFT memorizes a single teacher path per problem and converges quickly... curriculum RL... drives $\rho$ to 0 under reward feedback and forces the policy to discover its own solutions."* Pass@k boundary expansion (gains growing with k, largest at k=256) is offered as further evidence of genuine new-solution discovery rather than pattern reweighting or trace memorization.

## Boundary-expansion tension with Yue et al.

The paper frames its pass@k results as contrasting with prior findings that RLVR *narrows* coverage ([[../self-play/yue-rlvr-boundary]]). This is a **soft, partial** tension, not a head-on contradiction: the paper's own plain-GRPO arm (no teacher guidance) shows only modest boundary gains (+2.2 to +4.1pp at pass@64) — consistent in direction with Yue's weaker-RLVR-alone picture — and the large gains are specific to the teacher-guided curriculum arms. Best read as a fourth/fifth counter-example to the wiki's existing pattern ("teacher-guidance-and-exploration mechanisms can expand coverage; vanilla RLVR alone mostly doesn't"), alongside [[../rlvr-mechanics/curriculum-boundary-aware-rl]] and [[../rlvr-mechanics/es-broader-reasoning-coverage-grpo]] — not an unqualified refutation of Yue's original claim.

## Limitations (authors' own)

- Single fixed teacher (DeepSeek-V3.2) — no study of teacher-capability × curriculum-design interaction; a stronger teacher "may also introduce reasoning patterns whose hints transfer less cleanly to a smaller student."
- Math-only, single-turn; SciBench/GPQA are OOD probes, not a scientific-reasoning study; untested on code or theorem proving; hint mechanism relies on discrete step structure the teacher trace provides, often absent in non-math domains.
- The 2.2% residual pass@8 at $\rho=0$ on the "pass@64=0" filtered set is a finite-sample artifact of the N=64 threshold, not literal zero-probability — slightly undercuts the "structurally zero gradient" framing at the margin.
- The 128-shortest-trace selection (from 136 teacher-solved-of-147) is a length-based curation step whose effect on generality is not ablated.

## Source

- `raw/research/weekly-2026-09-18/04-unlocking-unsolvable-curriculum.md`
- arXiv:2609.13997

## Related

- [[adaback-adaptive-rationale]] — direct baseline/lineage: this source reuses AdaBack verbatim as its main per-sample-adaptive comparison, adapted to a shared discrete step lattice; MFC > AdaBack > GRPO holds on both tested models
- [[e2h-curriculum-rl]] — parallel/contrast: E2H is a fixed global difficulty-fading schedule; this source's §3.1 explicitly argues such global schedules are scheduler-fragile and excludes them from experiments
- [[pac-progress-augmented-curriculum]] — parallel adaptive-curriculum design on a different axis (which task to roll out next, via Thompson sampling) vs. this source's within-problem guidance-level curriculum; complementary, not competing
- [[../rlvr-mechanics/curriculum-boundary-aware-rl]] — closest mechanistic neighbor: teacher-guided trace injection targeted at boundary/unsolvable problems + GRPO consolidation, also reports pass@k boundary expansion; differs in scope (frontier *and* unsolvable vs. unsolvable-only) and provides a formal backward-chaining taxonomy this source lacks
- [[../rlvr-mechanics/datpo-difficulty-adaptive-tree-rlvr]] — both target pass@k coverage expansion as the key genuine-capability-growth metric, via different mechanisms (tree-rollout diversity vs. teacher-guided unsolvable curriculum)
- [[../self-play/yue-rlvr-boundary]] — the boundary-expansion tension discussed above
- [[../rl-optimizers/dapo]] — reuses DAPO's clip-higher and overlong-response-penalty as stabilizers layered on GRPO
- [[../../weekly-briefs/2026-09-18]] — brought in by the 2026-09-18 weekly sweep
