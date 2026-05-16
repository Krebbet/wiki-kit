# Rethinking RL for LLM Reasoning: It's Sparse Policy Selection, Not Capability Learning

Akgul et al. (arXiv:2605.06241, May 2026). Token-level mechanistic dissection of RLVR across GRPO/PPO/RLOO and three model families: RL reranks 1.0–4.1% of token positions, always within the base model's top-5 (0% shifted), concentrated at positions with 5–12× higher entropy. Oracle intervention at the reranked positions exactly recovers RL pass@1; random substitution does not. The full corrective signal is representable in a rank-32 LoRA at 0.27–0.49% of parameters; an output-projection-only rank-8 adapter (0.04% params) lags by 1 point. Replaces RL with **REASONMAXXER**, an entropy-gated contrastive method on ~50 problems matching or exceeding full RL at $4–25 versus $200–$103k. Direct mechanistic substrate for [[../self-play/invisible-leash|Invisible Leash Theorem C.1]] at the token level.

## Source

- `raw/research/weekly-2026-05-10/01-rethinking-rl-sparse-selection.md`

## Method

**Token-level taxonomy (Eq. 3).** For each position, classify the RL-promoted token as **UNSHIFTED** (base argmax kept), **RERANKED** (promoted token already in base top-5 but not argmax), or **SHIFTED** (promoted from below top-5). Across Qwen2.5/Qwen3/DeepSeek/Mistral and GRPO/PPO/RLOO: 95.9–99.0% UNSHIFTED, 1.0–4.1% RERANKED, **0% SHIFTED**. Mean promoted rank: 2.14–2.39.

**Entropy localisation (Eq. 2).** Reranked positions have token entropy $H_t$ that is 5–12× higher than the per-trajectory mean. RL only modifies high-uncertainty decision points.

**Causal probe.** Apply RL's promoted token only at positions identified as RERANKED — recovers full RL pass@1. Random-position substitution does not. Entropy-thresholded gating ($H_t > \tau$) closely approaches the oracle.

**Functional dimensionality via KL-LoRA (Eq. 4).** Distill RL teacher into a LoRA adapter against base via forward-KL. Rank 32 over QKVO with 0.27–0.49% params matches RL on MATH-500 / GSM8K. Rank 8 on $W_O$ alone (0.04% params) lags by ~1 point. The corrective signal lives near a low-dimensional manifold representable in $W_O$.

**REASONMAXXER (Eqs. 5–7).** RL-free recipe: sample 20 rollouts/problem from frozen base on 150 problems; keep ~50 with mixed success; advantage-normalise per problem (Eq. 5); apply contrastive cross-entropy on token positions where $H_t > \tau$ (Eq. 6) plus KL anchor outside (Eq. 7); train rank-32 LoRA in single epoch.

## Results

| Model | RL baseline | REASONMAXXER | RL cost | RM cost |
|---|---|---|---|---|
| Qwen2.5-1.5B (MATH-500) | 49.6 (SimpleRL-Zoo) | 50.2 | $200 | $4 |
| Qwen2.5-7B (MATH-500) | 65.6 | 70.6 | $600 | $5 |
| Qwen2.5-32B (avg, 6 benchmarks) | 0.409 | 0.440 | $5,737 | $25 |

~3 orders of magnitude cost reduction. Robust over $\tau \in [1.0, 2.2]$ with two performance peaks. Positive-only ablation ($A_i > 0$ only) yields 0.398 on MATH-500 — contrastive term is essential, not just SFT on correct rollouts.

## Reading REASONMAXXER as "targeted weighted-SFT"

The algorithm sits in the **offline weighted-SFT-replaces-RL family** with [[../rl-optimizers/bolt-kl-rlvr-boltzmann|BOLT]] and [[../rl-optimizers/tsallis-loss-continuum|Tsallis $\mathcal{J}_Q$]], distinguished by **per-token entropy gating**:

| | Sampler | Where the update fires | Weight |
|---|---|---|---|
| BOLT | $\pi_\text{ref}$, $N$ rollouts/prompt | all positions | per-prompt softmax over rewards at temperature $\beta$ — **non-negative** ([[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 4: uniquely so) |
| Tsallis $\mathcal{J}_Q$ | $\pi_\text{ref}$, on-policy | all positions | $q$-log family; per-instance $P_\theta^{-q}$ amplification — **non-negative** |
| **REASONMAXXER** | $\pi_\text{base}$, 20/problem | **only positions with $H_t > \tau$**; KL anchor at $H_t \leq \tau$ | per-problem $A_i = (r_i-\mu)/\sigma$ — **signed** (mean-zero per prompt; push-up *and* push-down) |

What this implies for the "is this just targeted RL?" reading:

- **Yes** on the partition: advantage where the base is uncertain, KL anchor where it's confident — Eqs. 5–7 literally implement that.
- **But it's offline**, not on-policy. Rollouts come from $\pi_\text{base}$, not the running policy — no PPO ratio, no GRPO group baseline that updates with $\pi_\theta$. The 3-orders-of-magnitude cost reduction lives in that distinction.
- **Contrastive in the signed-advantage sense, but not pairwise.** The "contrast" lives in the sign of $A_i = (r_i - \mu)/\sigma$: per-problem mean-zero normalisation forces a balanced mix of push-up ($A_i>0$) and push-down ($A_i<0$) at gated positions. Positive-only ablation drops 0.440→0.398 on MATH-500 (Results table) — the push-down half is load-bearing. **This signedness is shared with REINFORCE / PPO / GRPO**; what's specific to REASONMAXXER is dropping the importance ratio + clip (sampler is frozen $\pi_\text{base}$, nothing to correct for) and gating to $H_t > \tau$. Most apt analogue: **offline REINFORCE with per-token gating and per-problem mean-zero advantage** — not DPO (no pairwise sigmoid-margin) and not BOLT ([[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 4 — Boltzmann weight is *uniquely non-negative*, so it sits on the opposite side of the signed/unsigned axis within the offline-weighted-CE family). Plain SFT / [[../self-improvement/star|STaR]] / ReST-filtered-positive sit on BOLT's side.
- **Per-position gate**, not per-prompt. Finer-grained than [[../rl-optimizers/mcpo|MCPO]]'s prompt-level hinge-KL on mastered prompts and [[../rl-optimizers/dapo|DAPO]]'s prompt-level Dynamic Sampling. [[../rl-optimizers/maspo|MASPO]]'s Gradient-Utilization axis is the right taxonomy slot; REASONMAXXER refines it to the token level.
- **The "RL gradient" is replaced with weighted contrastive CE on a fixed dataset**, not approximated online — same move BOLT makes for KL-regularised RLVR, but with token-level gating.

**Open design slot.** No captured paper does the *online* analogue — on-policy GRPO/PPO with per-token entropy-gated advantage application and KL anchor at low-entropy positions. The components exist scattered ([[../rl-optimizers/dapo|DAPO]] Token-Level PG Loss, [[../rl-optimizers/mcpo|MCPO]] hinge-KL, [[../rl-optimizers/maspo|MASPO]] Gradient-Utilization axis); the composition is unfilled.

### Design choices for an on-policy entropy-gated variant

Surfaced 2026-05-13 by /query on whether to roll entropy-gating into DAPO. Five corpus findings bear on the composition:

1. **Stage-1 alignment is constructive.** [[../self-play/two-stage-dynamic]]: in Stage 1, gradient flows only to already-sampled tokens. High-entropy positions are precisely where multiple tokens have non-trivial probability — so gating concentrates gradient where the optimiser is effective.
2. **Stage-2 transition needs entropy preservation.** [[../self-play/two-stage-dynamic]]: Stage 2 fires once high-reward tokens saturate; aggressive advantage at the gated positions can collapse entropy *there*, blocking the transition. [[../self-play/info-gain-self-play|epiplexity]] (component **G** in [[../synthesis/proposed-method]]) is the pre-flight check.
3. **KL anchor at $H_t \leq \tau$ subsumes [[../rl-optimizers/mcpo|MCPO]] at token level.** MCPO documents ~5% regression on mastered prompts under unanchored drift; token-level anchoring is the finer-grained version of the same fix.
4. **Contrastive shape doesn't transfer directly.** REASONMAXXER's positive-only ablation (0.440→0.398) shows negative samples are load-bearing. On-policy DAPO has signed advantages but its negative samples come from the drifting policy, not from $\pi_\text{base}$ rollouts — open whether this carries the same gradient information.
5. **Hard bounds unchanged.** [[../self-play/invisible-leash]] Theorem C.1 (support inclusion) and [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 7 (coverage wall $N \gtrsim 1/p_\gamma$) apply regardless of gating. The composition is a sample-efficiency / stability move within the same fundamental envelope.

Knobs the composition forces:

| Knob | Options | Why it matters |
|---|---|---|
| Entropy source | (a) frozen $\pi_\text{base}$ — REASONMAXXER's choice; (b) current $\pi_\theta$ | (b) risks self-destructive gate collapse — entropy drops at gated positions, future iterations have fewer to gate on |
| KL anchor target | base ([[../single-sample-rl-finetuning/reft|ReFT]] / [[../rl-optimizers/instructgpt|InstructGPT+ptx]] style) vs prev-policy ([[../rl-optimizers/ppo|PPO]]-ratio style) | base anchor preserves capability; PPO-ratio is standard bookkeeping |
| Clip behaviour at gated positions | [[../rl-optimizers/dapo|DAPO]] Clip-Higher (asymmetric, favours low-prob promotions) | already aligned — Clip-Higher's design intent was to help where REASONMAXXER's gate fires |
| Std handling | [[../rl-optimizers/dr-grpo|Dr. GRPO]] std-removal | per-token gating changes effective per-prompt std |
| Dynamic Sampling | DAPO's prompt-level filter | likely redundant with per-token gating |
| Negative-sample handling | open — no captured on-policy primitive replicates REASONMAXXER's base-sampled contrast | the contrastive load-bearing finding is unaddressed by simple gating |

The variant deserves measurement against three baselines to disentangle the contributions: (a) plain DAPO, (b) offline REASONMAXXER, (c) entropy-gated DAPO with $\pi_\theta$-computed gate. (c) vs (b) probes whether on-policy gating collapses the gate; (c) vs (a) probes whether the gate adds anything to a full on-policy method.

## Connections to the wiki

- **[[../self-play/invisible-leash]]** — Theorem C.1 says $\text{supp}(\pi_\theta) \subseteq \text{supp}(q)$ for on-policy gradient updates. This paper provides the token-level operationalisation: 0% of RL-promoted tokens lie outside the base top-5; the support constraint is sharp empirically. Strongest mechanistic evidence yet for Position A in [[../../conflicts/invisible-leash-vs-spiral-transfer]].
- **[[../self-play/yue-rlvr-boundary]]** — Yue's pass@k inversion (base $\geq$ RL at large $k$) is the macro effect; this paper supplies the micro mechanism: precision-sharpening at 1–4% of positions, no novel content.
- **[[../self-play/two-stage-dynamic]]** — Yao's Stage-1 gradient-flows-only-to-already-sampled-tokens result maps onto why contrastive offline training recovers RL: the correct token was already in the base top-5.
- **[[rl-sparse-subnetwork]]** (Balashov) — adjacent finding (RL updates 5–30% of weights, full-rank within layer) and not strictly contradictory: Balashov measures the natural $\Delta W$ rank; this paper shows a low-rank LoRA can *represent* the same functional correction. Two compatible sparsity stories at parameter vs. token levels — see [[#Conflicts]] below.
- **[[../single-sample-rl-finetuning/1-shot-rlvr]]** — Wang et al. cited directly. ~50 examples + minutes of single-GPU compute is the sample-efficiency bookend to 1-shot RLVR's reward-engineering bookend.
- **[[../synthesis/proposed-method]]** — entropy-gating + $W_O$-only adapter is a directly actionable design primitive: a concept probe might be implementable as a rank-8 $W_O$ LoRA.

## Conflicts

- **vs. [[rl-sparse-subnetwork]]** (low-dim vs full-rank): Balashov says actual $\Delta W$ is sparse but full-rank per layer; this paper says a rank-8 LoRA can replicate RL's effect. Reconcilable: the natural RL update has high-rank support but lives near a low-dimensional manifold a small adapter can approximate. Neither paper directly contradicts the other; the framing tension is worth tracking.

## Related

- [[../self-play/invisible-leash]] — sharp support inclusion theorem
- [[../self-play/yue-rlvr-boundary]] — empirical pass@k inversion
- [[../self-play/two-stage-dynamic]] — Stage-1 / Stage-2 reframe
- [[rl-sparse-subnetwork]] — Balashov full-rank-but-sparse finding
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — Wang et al. 1-shot
- [[../single-sample-rl-finetuning/_overview]]
- [[../rl-optimizers/maspo]] — MASPO unifying objective
- [[../rl-optimizers/tsallis-loss-continuum]] — Tsallis $\mathcal{J}_Q$ analogous reframing for un-regularised RL
- [[../synthesis/proposed-method]] — design primitive: $W_O$ rank-8 LoRA as a concept probe
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — strengthens Position A
- [[../../weekly-briefs/2026-05-10]] — brought in by the 2026-05-10 weekly sweep
- [[../decoding-time-steering/_overview]] **(added 2026-05-13)** — full decoding-time / activation-steering theme. The 0%-shifted-outside-base-top-5 finding here is the **RLVR training-time analogue** of what the entire decoding-time theme demonstrates at inference time without any gradient. Specific cousins:
- [[../decoding-time-steering/iti]] — head-level intervention; 40% probe–generation gap on LLaMA-7B (model "knows but doesn't say") is the activation-level analogue of this paper's token-level finding
- [[../decoding-time-steering/contrastive-decoding]], [[../decoding-time-steering/cd-improves-reasoning]] — CD's $V_\text{head}$ plausibility mask enforces the same support-inclusion constraint at decode time
- [[../decoding-time-steering/dola]] — single-model layer-contrast surfaces what's intrinsic; no auxiliary needed
- [[../decoding-time-steering/cfg-lm]] — conditioning-direction extrapolation; same multiplicative-reweight structure as iterative BOLT
- REASONMAXXER's rank-8 $W_O$ LoRA (0.04% params) is the closest training-time cousin to the entire decoding-time theme — low-rank routing correction rather than capability addition
- [[../selective-finetuning/_overview]] **(added 2026-05-13)** — full theme on selective fine-tuning. REASONMAXXER's 0.04% finding has a direct SFT-side cousin in [[../selective-finetuning/skill-localization]] (Panigrahi ICML 2023: **0.01% of params** via grafting carry >95% of fine-tuned skill). Both papers triangulate the same underlying claim — task-specific behaviour is parametrically sparse — from RL and SFT respectively. [[../selective-finetuning/mend]]'s rank-1 gradient decomposition is structurally the closest cousin to REASONMAXXER's rank-32 KL-LoRA distillation

## Crossover with OPD-family (entropy-gate vs divergence-gate)

REASONMAXXER and [[../teacher-student-rl/opsd-compresses-rlvr|OPSD]] / [[../teacher-student-rl/rlt-followups-2026|the broader OPD family]] both deliver dense token-level signal at a sparse subset of "active" positions — but they identify that subset through different mechanisms.

| Axis | REASONMAXXER | OPD (Thinking Machines / Rethinking-OPD / OPSD) |
|---|---|---|
| Gate signal | **Self-entropy** $H_t > \tau$ on base rollouts | **Teacher-student divergence** at student-visited states |
| Teacher required? | No | Yes (separate or same-model + privileged context) |
| Update | Per-problem **signed** advantage (push-up correct + push-down incorrect); contrastive CE at gated positions; KL anchor outside | **Reverse-KL** to teacher distribution (mode-seeking, unsigned) |
| Sampler | Offline, frozen $\pi_\text{base}$ | On-policy student rollouts |
| Pipeline slot | RL-*replacement* (\$4–25 vs \$200–\$103k) | Post-RLVR compaction (SFT → RLVR → OPSD per [[../teacher-student-rl/opsd-compresses-rlvr]]) |

**Empirical overlap of the gated set.** Per [[../teacher-student-rl/rlt-followups-2026]] §3 (Rethinking-OPD): successful OPD signatures concentrate supervision on high-probability *overlap tokens* — restricting to overlap tokens alone matches full top-$k$ performance; 97–99% of combined probability mass lives there. By the structural argument that at low-entropy positions the student is already peaked (small KL) while at high-entropy positions a competent teacher's distribution differs most, **entropy-gating and divergence-gating likely index the same set of positions** for matched-quality teachers. Both methods are precision-sharpening within base support — REASONMAXXER reads the sparsity off the model's own rollouts; OPD reads it off teacher–student divergence.

**Real differences that survive the "same positions" reading.**

1. *Teacher requirement.* REASONMAXXER works in teacher-free settings; OPD needs one.
2. *Signed vs one-sided.* Positive-only REASONMAXXER ablation drops 0.440 → 0.398 on MATH-500 — push-down on incorrect rollouts is load-bearing. OPD's reverse-KL only pulls toward teacher; it has no push-away-from-confidently-wrong axis.
3. *Failure mode shape.* OPSD on Incorrect-only rollouts loses 7–10 pp ([[../teacher-student-rl/opsd-compresses-rlvr]]); REASONMAXXER fails on all-correct or all-incorrect problems (no per-problem advantage signal — needs ~50 mixed-success from 150 sampled).
4. *Pipeline position.* OPSD compacts what RLVR established. REASONMAXXER substitutes RL outright. Composing them (REASONMAXXER → OPSD-style compaction) is not redundant; no captured paper tests the composition.
5. *On-policy vs offline gating.* REASONMAXXER's gated positions are measured once on $\pi_\text{base}$ and fixed; OPD's shift as the student updates. Different stability and compute profiles.

**Connection to the wiki's central R_w claim** ([[../synthesis/proposed-method]] R_w extension): both are dense-signal methods that act on **already-supported tokens** — neither moves outside base support. REASONMAXXER does so at the *token* level (the parallel of [[../selective-finetuning/skill-localization]] 0.01% at the *parameter* level); OPD-family does so at the *student-distribution-shift* level. Both are training-time complements to the inference-time decoding-time-steering theme ([[../decoding-time-steering/_overview]]); the entire selective-finetuning + decoding-time-steering + REASONMAXXER + OPD landscape converges on the same operational claim ("behaviour is isolable in identifiable positions / parameters / subspaces").
