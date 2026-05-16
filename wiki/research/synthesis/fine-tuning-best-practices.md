---
name: fine-tuning-best-practices
description: Practitioner-oriented synthesis of SFT and RLVR best practices drawn from the wiki — when to use each, how to implement, and recent trends (2026 cluster). Composable cookbook for the single-sample concept-based fine-tuning project.
type: synthesis
---

# Fine-Tuning Best Practices — SFT and RLVR

*Editorial synthesis. Drawn strictly from corpus pages; every practice traces to a captured source. Intended as a working cookbook for the wiki's project frame (1–40B LLMs, single-sample concept-based fine-tuning) but generalises to fine-tuning small-to-mid LLMs more broadly.*

## One-paragraph summary

Two regimes, complementary: **SFT** installs new support (capacity expansion); **RLVR** concentrates probability mass within existing support (selection). Per the 2026-05-10 RL-as-selection-not-learning cluster ([[../rlvr-mechanics/rethinking-rl-sparse-selection]], [[../rlvr-mechanics/binary-rewards-rl-challenges]], [[../rl-optimizers/bolt-kl-rlvr-boltzmann]], [[../teacher-student-rl/opsd-compresses-rlvr]]), this is no longer a soft preference — it's a structural fact. Use SFT to put information into the model parametrically; use RLVR to choose what the model emits within the support SFT installed. Pair them in the order **SFT → RLVR → optional OPSD compaction** (never RLVR → SFT-to-fix-failures, which degrades). The fundamentals (Dr. GRPO bias fixes, DAPO Clip-Higher, entropy preservation, EWC anchor, sparse subnetwork mask, sample-difficulty calibration to $p \approx 0.5$) are stable; recent trends (weighted-SFT replaces RL, token-level entropy gating, on-policy distillation as a post-RL stage) refine the recipe at the margins.

---

## When to use SFT

| Goal | Use SFT? | Source |
|---|---|---|
| Install new reasoning patterns or formats the base lacks | **Yes — uniquely effective** | [[../self-play/yue-rlvr-boundary]]: "distillation uniquely expands capacity"; pass@k curves of distilled checkpoints lie above both base and RLVR at every $k$. |
| Cold-start before RL (long-CoT format, readable rationales) | Yes | [[../single-sample-rl-finetuning/deepseek-r1]] cold-start; [[../rl-optimizers/instructgpt]] SFT → RM → PPO+ptx; [[../single-sample-rl-finetuning/reft]] 1–2 epoch SFT warm-up + PPO. |
| Lift $\pi^*(S\|x)$ in target region so RL becomes tractable | Yes | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7: $N \gtrsim 1/p_\gamma$; if $p_\gamma \approx 0$, no RL budget closes the gap. SFT raises $p_\gamma$. |
| Compact post-RL rollouts (length reduction, near-zero accuracy loss) | Yes — **correct-only** | [[../teacher-student-rl/opsd-compresses-rlvr]]: Correct-only OPSD: −29% length, ~0 accuracy. |
| Correct RL failures by distilling on incorrect rollouts | **No — degrades** | [[../teacher-student-rl/opsd-compresses-rlvr]]: Incorrect-only OPSD: −7 to −10 pp. Distillation cannot install reasoning states outside the student's support. |
| Concentrate probability mass on existing capacity (pass@1) | No — use RLVR | [[../rlvr-mechanics/rethinking-rl-sparse-selection]]; [[../self-play/yue-rlvr-boundary]]. |

## SFT best practices

### What to include in the SFT data

| Practice | Why | Source |
|---|---|---|
| **Diverse rationales per problem** | Reasoning-diversity is load-bearing for transfer | [[../teacher-student-rl/ho-reasoning-teachers]] Fine-tune-CoT |
| **Minimal-sufficient hints, not maximal context** | Full-KP injection can induce regression; CSS-pruned subset is the sweet spot | [[../teacher-student-rl/knowrl]] (avg KP count drops 5.86 → 2.57 after CSS, performance improves) |
| **Anneal scaffolding to zero across iterations** | Internalisation requires scaffold withdrawal; permanent scaffolding doesn't transfer | [[../single-sample-rl-finetuning/cbrl]] $p_\text{start}=0.5, p_\text{end}=0$ linear decay |
| **Long structured reference > many short examples (per token)** | Per-token-information theorem | [[../in-context-learning-theory/icl-bayesian-inference]] |
| **Correct-only filtering for post-RL compaction** | Distilling on errors degrades | [[../teacher-student-rl/opsd-compresses-rlvr]] |
| **Rejection-sampled rationales for self-improvement** | When teacher unavailable, gate self-generated rationales on outcome | [[../self-improvement/star]] STaR |

### How to structure the loss

| Choice | Recommendation | Source |
|---|---|---|
| Weighting | If using as RL replacement (KL-regularised target), use [[../rl-optimizers/bolt-kl-rlvr-boltzmann\|BOLT]]'s prompt-normalised Boltzmann ratio $\hat{w} = \exp(r/\beta)/\hat{Z}_N(x)$. **Not** raw $\exp(r/\beta)$, not filtered-positive, not advantage — all miss $\pi^*$ by Corollary-5 gap (1.44–3.60 pp empirically) | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 4 |
| Mixed gradient | InstructGPT-style PPO+ptx: blend pretraining gradients into the loss to prevent capability drift | [[../rl-optimizers/instructgpt]] |
| KL leash to base | Standard SFT cross-entropy + small KL anchor; load-bearing for format/fluency at small $N$ | [[../single-sample-rl-finetuning/reft]], [[../rl-optimizers/instructgpt]] |

### Forgetting protection (load-bearing across SFT runs)

| Mechanism | What it does | Source |
|---|---|---|
| **EWC Fisher anchor** | Quadratic penalty $\frac{\lambda}{2}\sum_i F_i(\theta_i - \theta_i^*)^2$ protects pretraining-relevant weights | [[../catastrophic-forgetting/ewc-gemma2-cpt]] (preserves 7/7 English while gaining 5/7 Lithuanian) |
| **Balashov sparse mask** | Restrict updates to the top-$k$ Fisher · magnitude subnetwork (5–30% of weights); LayerNorms excluded | [[../rlvr-mechanics/rl-sparse-subnetwork]] |
| **KL leash to base** | Token-level distance penalty; cheap forgetting bound | [[../single-sample-rl-finetuning/reft]] |

## SFT recent trends (2026 cluster)

1. **Weighted SFT as a static RL replacement.** [[../rl-optimizers/bolt-kl-rlvr-boltzmann|BOLT]] (May 2026) matches/exceeds GRPO at 75–85% less wall-clock via one-shot Boltzmann-weighted CE on $\pi_\text{ref}$-samples. [[../rl-optimizers/tsallis-loss-continuum|Tsallis $\mathcal{J}_Q$]] (Apr 2026) does the un-regularised analogue. Together they close the analytical picture of RLVR as a member of the weighted-SFT family.
2. **On-policy distillation as a post-RL stage.** OPD landscape (Qwen3, MiMo, GLM-5, Thinking Machines Tinker). Repositioned by [[../teacher-student-rl/opsd-compresses-rlvr]] as **compaction-not-correction** — pipeline shape is **SFT → RLVR → OPSD**, not OPSD-fixes-RLVR.
3. **Co-evolving distillation breaks the single-teacher ceiling.** [[../teacher-student-rl/co-evolving-policy-distillation|CoPD]] alternates GRPO and bidirectional mutual on-policy distillation across $K$ branches; top-$k$ overlap held >0.90; surpasses every single-expert ceiling on Qwen3-VL-4B.
4. **Multi-agent debate ensembles teach below the single-teacher ceiling.** [[../teacher-student-rl/mad-opd|MAD-OPD]]: 4B student under 14B+8B debate exceeds 14B teacher alone (+4.26 pp on LCB-v6); task-adaptive divergence (JSD agentic / reverse-KL code).
5. **SFT must precede RL, not correct it after.** [[../teacher-student-rl/opsd-compresses-rlvr]] (May 2026). Direct implication for any SFT+RL pipeline design.

---

## When to use RLVR

| Goal | Use RLVR? | Source |
|---|---|---|
| Sharpen pass@1 on tasks within base support | **Yes** | [[../rlvr-mechanics/rethinking-rl-sparse-selection]]: 1–4% positions reranked, 0% shifted outside base top-5 — RL is precision-sharpening |
| Concentrate probability mass on correct CoTs already in the model | Yes | [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] (Shao et al.); [[../self-play/invisible-leash]] Theorem C.1 |
| Improve pass@k for large $k$ | **No** | [[../self-play/yue-rlvr-boundary]]: pass@k inversion across six RLVR algorithms; AIME24 RLVR-uniquely-solvable = 0.0% at $k=1024$ |
| Install reasoning patterns absent from the base | **No** | [[../self-play/yue-rlvr-boundary]]: only distillation expands capacity |
| Train on a target where reference pass-rate $p_\gamma(x) \approx 0$ | **No** | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7: $N \gtrsim 1/p_\gamma$ |
| Bootstrap reasoning on a strong base with verifier rewards | Yes | [[../single-sample-rl-finetuning/deepseek-r1]] R1-Zero: AIME 15.6 → 77.9; [[../single-sample-rl-finetuning/1-shot-rlvr]] $N=1$ existence proof |

## RLVR best practices

### Optimiser choice and hygiene

| Practice | Why | Source |
|---|---|---|
| **Use GRPO as default**; critic-free, group-relative baseline | Simpler than PPO at similar performance; unified gradient view across SFT/RFT/DPO/PPO/GRPO | [[../rlvr-mechanics/deepseekmath-grpo]] |
| **Apply Dr. GRPO bias fixes** (length-bias, std-removal) | Standard GRPO has measurable length and std biases that degrade quality | [[../rl-optimizers/dr-grpo]] |
| **DAPO Clip-Higher**: asymmetric clipping favouring low-prob promotions | Standard symmetric clip throttles the gradient direction RL actually needs | [[../rl-optimizers/dapo]] |
| **DAPO Dynamic Sampling**: filter prompts where all rollouts pass or all fail | Zero-variance prompts give zero gradient; wasted compute | [[../rl-optimizers/dapo]] |
| **DAPO Token-Level PG Loss** instead of sequence-mean | Per-token credit assignment; required for long CoTs | [[../rl-optimizers/dapo]] |
| **DAPO Overlong Reshape** on truncated rollouts | Length penalties cause format collapse without it | [[../rl-optimizers/dapo]] |
| **GSPO** for MoE / longer sequences | Sequence-level importance ratio; stabilises Qwen3-scale MoE | [[../rl-optimizers/gspo]] |
| **MCPO hinge-KL on mastered prompts** | Documents ~5% one-step regression on unanchored drift over mastered prompts | [[../rl-optimizers/mcpo]] |

### Reward shape

| Practice | When | Source |
|---|---|---|
| **Outcome reward + format reward** as baseline | Strong base with verifiable answers; default starting point | [[../single-sample-rl-finetuning/deepseek-r1]]; [[../single-sample-rl-finetuning/1-shot-rlvr]] |
| **Step-level PRM** when outcome supervision is too sparse | Long CoTs; complex multi-step problems | [[../process-reward-models/lets-verify-step-by-step]] PRM800K; [[../process-reward-models/math-shepherd]] (no human labels); [[../process-reward-models/pav-rewarding-progress]] PAV (5–6× RL efficiency) |
| **RLT-style dense reward**: $r^{SS} = \log \pi_S(s\|q, t)$, optionally with $r^{KL}$ leakage penalty | Teacher-given-answer setting (textbook with worked solutions) | [[../teacher-student-rl/sakana-rlt]] |
| **Information-gain Fisher/SVD reward** (annotation-free) | No verifier available; works in single-sample regime | [[../rlvr-mechanics/learning-to-think]] L2T |
| **Process-mining alignment** (TACReward) | Teacher trace exists; want dense process supervision | [[../teacher-student-rl/pm4grpo]] |

### Sample selection and curriculum

| Practice | Why | Source |
|---|---|---|
| **Target difficulty $p \approx 0.5$ pre-training** | Maximises gradient magnitude: $\mathbb{E}[\|g\|^2] \propto p(1-p)(1-1/G)$ | [[../single-sample-rl-finetuning/data-efficiency-rft]] DOTS Theorem 1 |
| **Single well-chosen example can match full-set RLVR** | Existence proof at $N=1$ on Qwen2.5-Math | [[../single-sample-rl-finetuning/1-shot-rlvr]] |
| **Anneal demonstration-prepending during RL** | Bootstraps zero-variance prompts; gains persist after withdrawal | [[../single-sample-rl-finetuning/cbrl]] |
| **Inject minimal-sufficient knowledge points on hard samples** | Hint density is a design parameter, not free — more is not better | [[../teacher-student-rl/knowrl]] |

### Entropy and Stage management

| Practice | Why | Source |
|---|---|---|
| **Preserve entropy explicitly** (bonus, temperature, no-KL or hinge-KL) | Stage-1 RLVR (default GRPO) is trapped within base support; Stage 2 requires entropy preservation | [[../self-play/two-stage-dynamic]] |
| **Run epiplexity pre-flight** | Detect Stage-2 blockage before spending RL budget; diversity that isn't *learnable* is wasted | [[../self-play/info-gain-self-play]] (Algorithm 1); [[proposed-method]] component **G** |
| **Watch for entropy loss as a load-bearing signal** | Empirical: 1-shot RLVR's post-saturation gains correlate with entropy-loss term | [[../single-sample-rl-finetuning/1-shot-rlvr]] |

### Group size and rollout budget

| Practice | Why | Source |
|---|---|---|
| **Use $G \geq 8$ (16–64) for stable group baselines** | Group-relative variance reduction collapses at small $G$ | [[../rlvr-mechanics/deepseekmath-grpo]]; [[../teacher-student-rl/sakana-rlt]] (Sakana used $G=64$) |
| **Coverage check: $N \gtrsim 1/p_\gamma(x)$ per prompt** | Binding constraint is reference pass-rate, not budget; cap = $\beta\log(1/\pi^*(S_N\|x))$ | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorems 6, 7 |

### Forgetting and locality

| Practice | Why | Source |
|---|---|---|
| **Sparse subnetwork mask** (5–30% of weights, top-$k$ Fisher · magnitude, LayerNorms excluded) | RL natively touches only 5–30% of weights; making the mask explicit bounds blast radius | [[../rlvr-mechanics/rl-sparse-subnetwork]] |
| **EWC Fisher anchor** | Protects pretraining-relevant weights from drift | [[../catastrophic-forgetting/ewc-gemma2-cpt]] |
| **KL leash to base** | Cheap secondary forgetting bound; load-bearing for format/fluency | [[../single-sample-rl-finetuning/reft]] |
| **Rank-32 LoRA on QKVO (0.27–0.49% params) suffices** | The full corrective signal is low-rank; rank-8 on $W_O$ alone (0.04%) lags ~1 pt | [[../rlvr-mechanics/rethinking-rl-sparse-selection]] |

## RLVR recent trends (2026 cluster)

1. **RL-as-selection-not-learning, four-paper crystallisation (2026-05-10).** [[../rlvr-mechanics/rethinking-rl-sparse-selection]] (token-level: 1–4% reranked, 0% shifted outside base top-5), [[../rlvr-mechanics/binary-rewards-rl-challenges]] (information-geometric: forward/reverse-KL asymmetry, near-Dirac collapse under misspecification + small $\beta$), [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] (closed-form static analogue: one-shot saturation $\beta\log(1/\pi^*(S_N\|x))$, coverage wall $N \gtrsim 1/p_\gamma$, iterative BOLT = KL-PMD), [[../teacher-student-rl/opsd-compresses-rlvr]] (post-RL boundary). Practical implication: design for selection within high-$p_\gamma$ regions; don't expect RL to install new capacity.
2. **Weighted-SFT replaces RL.** Two families now have analytical bridges: BOLT for KL-regularised, Tsallis $\mathcal{J}_Q$ for un-regularised. Iterative BOLT recovers RL exactly via mirror descent.
3. **Token-level entropy-gated training.** [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s REASONMAXXER: offline contrastive CE at $H_t > \tau$ positions, KL anchor elsewhere; ~3 orders of magnitude cost reduction over full RL. Open design slot: on-policy version (composition of DAPO Token-Level PG Loss + entropy gate + low-entropy KL anchor) not yet captured.
4. **Two-stage dynamic** ([[../self-play/two-stage-dynamic]]): GRPO defaults to Stage-1 (trapped within base support); Stage 2 (where pass@256 can exceed base) requires entropy preservation. SPIRAL's game-self-play is one Stage-2-consistent mechanism.
5. **MASPO unifying axes** ([[../rl-optimizers/maspo]]): Gradient Utilization × Probability Mass × Signal Reliability subsumes DAPO Clip-Higher and BAPO; useful taxonomy when stacking post-GRPO improvements.

---

## Pairing SFT and RLVR

Per the wiki's [[proposed-method]] extension (**C_w**, 2026-05-11) and the recent cluster, the load-bearing constraints are:

1. **Order matters: SFT → RLVR, not RLVR → SFT-to-fix.** OPSD-compresses-RLVR shows distillation after RL can compact but cannot install missing states; Incorrect-only OPSD loses 7–10 pp. ([[../teacher-student-rl/opsd-compresses-rlvr]])
2. **Alternating is competitive with sequential** for multi-capability consolidation. [[../teacher-student-rl/co-evolving-policy-distillation|CoPD]] alternates GRPO and OPD across branches; top-$k$ overlap held >0.90 (vs monotonic collapse under static MOPD).
3. **Iterative weighted-SFT refresh = mirror descent = full RL** ([[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 11). If your goal is just to *match* RL behaviour, iterative BOLT does it without the RL loop; if your goal is capacity expansion, neither route gets you there.
4. **Reference SFT before RL lifts $p_\gamma$** so RL becomes tractable on targets the base can't currently reach (BOLT Theorem 7). [[proposed-method]] component **C_w**.
5. **Minimal-sufficient + annealed scaffold** ([[../teacher-student-rl/knowrl]] + [[../single-sample-rl-finetuning/cbrl]]) is the SFT-during-RL pattern that actually internalises.
6. **Multi-stage pipelines (R1-style)** work: cold-start SFT → RL stage 1 → rejection-sampled SFT → RL stage 2. ([[../single-sample-rl-finetuning/deepseek-r1]])

---

## Cross-cutting decisions for the project frame

For the wiki's specific scope (single-sample concept-based fine-tuning on 1–40B models):

| Decision | Recommended default | Source |
|---|---|---|
| Optimiser | GRPO + Dr. GRPO fixes + DAPO Clip-Higher | [[../rlvr-mechanics/deepseekmath-grpo]], [[../rl-optimizers/dr-grpo]], [[../rl-optimizers/dapo]] |
| Reward | RLT $r^{SS}$ if teacher-with-solution is available; outcome+format otherwise | [[../teacher-student-rl/sakana-rlt]], [[../single-sample-rl-finetuning/1-shot-rlvr]] |
| Group size | $G = 8$ minimum, $G = 16$–$32$ preferred at the project's small-data budget | [[../teacher-student-rl/sakana-rlt]] (used 64) |
| Sample difficulty | Calibrate to $p \approx 0.5$ pre-training; verify with DOTS rule | [[../single-sample-rl-finetuning/data-efficiency-rft]] |
| Coverage check | Pre-flight $p_\gamma$ measurement; abort if $\approx 0$ for the target prompt | [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7 |
| Diversity pre-flight | Epiplexity / info-gain-self-play Algorithm 1 | [[../self-play/info-gain-self-play]] |
| Forgetting | Balashov mask + EWC anchor + KL leash | [[../rlvr-mechanics/rl-sparse-subnetwork]], [[../catastrophic-forgetting/ewc-gemma2-cpt]] |
| Stopping | L2T info-gain plateau + MDL sibling-set stability | [[../rlvr-mechanics/learning-to-think]], [[../concept-learning/recursive-concept-evolution]] |
| Concept-probe metric | Behavioural battery (GSM-Symbolic / MATH-Perturb / Contrast Sets / Counterfactual / Skill-Mix) + Causal Abstraction IIA | [[../concept-evaluation/_overview]] |
| Post-stage | Correct-only OPSD for length compression if rollouts are long | [[../teacher-student-rl/opsd-compresses-rlvr]] |
| Adapter shape | Rank-32 LoRA over QKVO; rank-8 $W_O$ for ultra-cheap probe | [[../rlvr-mechanics/rethinking-rl-sparse-selection]] |

---

## Failure modes to avoid

| Failure | Cause | Source |
|---|---|---|
| pass@k drops while pass@1 rises | Default RLVR over-concentrates; base catches up at large $k$ | [[../self-play/yue-rlvr-boundary]] |
| Near-Dirac mode collapse | Small $\beta$ + misspecification; reverse-KL to $p^*$ undefined | [[../rlvr-mechanics/binary-rewards-rl-challenges]] (Eq. 10) |
| Post-saturation gibberish at $N=1$ | No KL anchor / sparse mask; unanchored drift on single prompt | [[../single-sample-rl-finetuning/1-shot-rlvr]]; [[../rl-optimizers/mcpo]] §4.1 |
| One-step regression on mastered prompts | Unanchored drift when prompt is already solved | [[../rl-optimizers/mcpo]] (~5%) |
| Multi-teacher averaging degrades vs single teacher | Per-token gradient interpolation across incompatible paths | [[../teacher-student-rl/mad-opd]] (MT-OPD failure) |
| Distillation-to-fix-failures degrades | Cannot install states outside student support | [[../teacher-student-rl/opsd-compresses-rlvr]] (Incorrect-only) |
| Zero-variance prompt produces no gradient | All rollouts succeed or all fail | mitigation: [[../rl-optimizers/dapo]] Dynamic Sampling, [[../single-sample-rl-finetuning/cbrl]] |
| Length collapse from raw length penalty | Penalty without overlong reshape compresses correct reasoning too | [[../rl-optimizers/dapo]] Overlong Reshape |
| GRPO length bias (longer answers get higher reward) | Sequence-mean vs token-mean averaging | [[../rl-optimizers/dr-grpo]] |
| Full-context hint injection regresses | Pruning interaction paradox; minimal-sufficient is the right principle | [[../teacher-student-rl/knowrl]] |

---

## Source

Editorial synthesis. Drawn from corpus pages cited inline; no single source proposes this composition. Synthesis built 2026-05-13.

## Related

- [[proposed-method]] — implementation roadmap that builds on these practices; component-level decomposition
- [[single-sample-concept-skeleton]] — earlier ancestor synthesis at the primitive level
- [[concept-curriculum-method]], [[recursive-concept-learning]] — curriculum proposals that compose with the SFT and RLVR practices here
- [[../rl-optimizers/_overview]] — optimiser lineage (PPO → GRPO → DAPO/Dr. GRPO/GSPO; BOLT, Tsallis)
- [[../rlvr-mechanics/_overview]] — RLVR mechanics theme; includes the RL-as-selection cluster
- [[../teacher-student-rl/_overview]] — teacher-student methods (RLT, SOAR, KnowRL, CoPD, OPSD, MAD-OPD)
- [[../process-reward-models/_overview]] — process reward menu
- [[../single-sample-rl-finetuning/_overview]] — sample-efficient RL regime
- [[../concept-evaluation/_overview]] — evaluation battery for concept understanding vs memorisation
- [[../decoding-time-steering/_overview]] — inference-time complement; no weight updates, useful as a debugging tool
