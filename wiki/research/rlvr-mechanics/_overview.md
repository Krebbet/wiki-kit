# RLVR Mechanics & Sparse Subnetwork

Theme covering the *mechanics* of RL with verifier rewards (RLVR) for LLM reasoning: the canonical optimiser (GRPO), what RL actually changes inside the model (sparse subnetwork), and how to densify the reward signal without external annotators (information-theoretic process reward in L2T).

## Pages

- [[deepseekmath-grpo]] — GRPO, the critic-free, group-relative PPO variant; unified gradient view of SFT/RFT/DPO/PPO/GRPO.
- [[rl-sparse-subnetwork]] — RL fine-tuning modifies only 5–30% of weights across seven algorithms; updates are sparse but full-rank; subnetwork-only retraining recovers full performance.
- [[learning-to-think]] — L2T: episodic GRPO with a universal information-gain process reward computed via PAC-Bayes + Fisher / low-rank SVD, no external PRM.
- [[structured-fisher-optimizer]] — Gong et al. (Microsoft, 2025). Structured FIM approximation (RACS, Alice) unifying Adam / Shampoo / grad-norm; 2× Adam speedup at LLaMA scale. Adjacent to L2T's Fisher proxy on the optimisation side, not the reward side.
- [[rethinking-rl-sparse-selection]] — Akgul et al. (arXiv:2605.06241). Token-level dissection: 1.0–4.1% positions reranked, **0% shifted outside base top-5**; rank-32 LoRA at 0.27–0.49% params replicates RL; REASONMAXXER matches/exceeds RL at 3 orders of magnitude less cost.
- [[binary-rewards-rl-challenges]] — Dymetman (arXiv:2605.02375). Information-geometric account of diversity collapse: filtered model $p^*$ is I-projection; forward-KL convergence + $\text{KL}(p^\beta\|p^*)=+\infty$; misspecification + small $\beta$ drives near-Dirac.

## Cross-cutting themes

**RL is a micro-edit, not a re-parameterisation.** Balashov shows RL touches a small (5–30%), reproducible, but high-rank subset of weights — including specifically on DeepSeek-Math 7B + GRPO (75% sparsity). LayerNorms are essentially never touched. This reframes "fine-tune with RL" from "shift the whole network into a new policy" to "find and turn a small set of behavioural knobs". L2T's low-rank Fisher proxy ($r/d \approx 1$–10% at 1.5B) is dimensionally consistent with where this subnetwork lives, even though L2T is motivated by tractability rather than empirical sparsity.

**The reward, not the optimiser, is the bottleneck for sample efficiency.** GRPO's contribution is *engineering* (drop the critic, baseline from group); the unified gradient table in Sec 5 makes clear that SFT, RFT, DPO, PPO, and GRPO differ mostly in their gradient coefficient. L2T's contribution is to replace a sparse outcome reward with a dense, *annotation-free* per-episode information-gain signal. The implication for low-data work: design the coefficient to extract maximum gradient signal per sample (information-gain, group-relative advantage, process reward), and the optimiser is largely interchangeable.

**Outcome-only RL is wasteful and self-defeating.** L2T's Sec 3.2 measurements on Omni-MATH show GRPO-trained DeepScaleR uses >2x the minimum tokens needed and accuracy *peaks at ~16–20 episodes then declines* due to attention dilution and context truncation. Adding a length penalty alone makes things worse (Table 1). Process-dense rewards are needed to extract the full benefit of test-time compute scaling.

**Concept-based fine-tuning is mechanically supported.** If RL effectively edits a small, consistent subnetwork (Balashov), and if information gain per episode can be measured cheaply via Fisher/SVD (L2T), then a single training example can be used to (a) identify *which* knobs the example wants to turn and (b) quantify *how far* they actually moved — both of which are the missing primitives for a single-sample, concept-based fine-tuner.

**RL-as-selection-not-learning** *(2026-05-10 thesis cluster).* Four mutually-reinforcing accounts now treat RLVR as re-weighting / selecting within base-model support rather than installing new skill:

- **Token-level surface.** [[rethinking-rl-sparse-selection|Rethinking-RL]] across GRPO/PPO/RLOO on three model families: 0% of RL-promoted tokens lie outside the base top-5; mean promoted rank 2.14–2.39; reranking is concentrated at high-entropy positions; oracle intervention at reranked positions exactly recovers RL pass@1. Rank-32 LoRA at 0.27–0.49% params (or rank-8 $W_O$ at 0.04%) suffices.
- **Information geometry.** [[binary-rewards-rl-challenges|Binary-Rewards]] (Dymetman): the filtered model $p^* = a(\cdot|\mathcal{Y}_1)$ is the I-projection of base $a$ onto valid outputs; KL-RLVR converges to $p^*$ in forward KL as $\beta\to 0$ but $\text{KL}(p^\beta\|p^*) = +\infty$ for all finite $\beta$. Under misspecification + small $\beta$, Eq. 10 amplifies validity advantage and drives near-Dirac collapse. Formal mechanism for [[../self-play/yue-rlvr-boundary|Yue]]'s pass@k inversion.
- **Closed-form static analogue.** [[../rl-optimizers/bolt-kl-rlvr-boltzmann|BOLT]] (Shu): the *unique* reference-sampled weighted-SFT objective whose induced policy equals the KL-RLVR Boltzmann target is $w^\star = \exp(r/\beta)/Z(x)$. One-shot saturation $\beta\log(1/\pi^*(S_N|x))$; coverage–ESS frontier $N \gtrsim 1/p_\gamma$; iterative BOLT = KL policy mirror descent. RL's marginal value over BOLT comes from sampler refresh, not the gradient method.
- **Post-RL boundary.** [[../teacher-student-rl/opsd-compresses-rlvr|OPSD]]: Correct-only OPSD compacts (−29% length, ~0 accuracy); Incorrect-only OPSD degrades (−7 to −10 pp). Distillation cannot create reasoning states outside the student's support. Pipeline shape **SFT → RLVR → OPSD** is the post-2026-05 default.

The cluster gives Position A in [[../../conflicts/invisible-leash-vs-spiral-transfer|Invisible-Leash vs SPIRAL]] both a token-level operationalisation and a structural account. For single-sample method design, the immediate implications are: (i) the chosen training example must lie in the high-$p_\gamma$ regime of the base model (BOLT Theorem 7); (ii) an entropy-gated rank-8 $W_O$ LoRA is an empirically-justified concept-probe design primitive; (iii) genuine capacity expansion requires mechanisms outside RLVR (distillation, entropy-preserving game-self-play, explicit concept installation).

## Method comparison

| Method | Reward source | Critic | Density | Annotation cost | Reported gain |
|---|---|---|---|---|---|
| PPO | learned RM, per-token KL in reward | yes ($V_\phi \approx \|\pi_\theta\|$) | sparse outcome | RM training | baseline |
| GRPO | learned RM, group-relative baseline | no | sparse outcome (or PRM step) | RM training | +5 MATH over Instruct |
| GRPO + PRM | step-level PRM | no | dense process | PRM + step labels | marginal over outcome |
| L2T | internal info-gain (Fisher/SVD) on top of GRPO | no | dense per-episode | none | +3.7 vs GRPO, ~2x token efficient |
| Subnetwork-only RL (Balashov) | any RL | depends on host | inherits host | identify mask once | matches/exceeds $\theta_\text{full}$ |

## Open questions

- Does the L2T information-gain reward, computed on the low-rank proxy $\tilde{\theta}$, in fact correlate with updates landing in Balashov's RL-induced subnetwork? Both papers point at the same low-dimensional structure but never co-measure.
- Is the cross-algorithm subnetwork overlap evidence of a *task* subnetwork or an *alignment-shaped* subnetwork? Balashov's overlap analysis spans alignment and math RL; the distinction matters for transfer.
- L2T uses 919 AIME problems and 4k NuminaMath samples. How far down the data axis does the information-gain reward continue to help — does it work in the single-sample regime that motivates this wiki?
- GRPO requires $G$ rollouts per prompt for the baseline. In single-sample RLVR, what is the right $G$, and does group-relative variance reduction collapse when the prompt distribution is degenerate?
- Can the Balashov mask be discovered without a full RL run — e.g., from a few rollouts and Fisher information — and used as a hard constraint in single-sample training?

## Source PDFs

- `../../../raw/research/single-sample-llm-learning/pdfs/04-learning-to-think.pdf`
- `../../../raw/research/single-sample-llm-learning/pdfs/05-rl-sparse-subnetwork.pdf`
- `../../../raw/research/single-sample-llm-learning/pdfs/F-1-deepseekmath-grpo.pdf`
- `../../../raw/research/adjacent-reward-signals/pdfs/structured-fisher-llm-optimizer.pdf`

## Related themes

- [[../synthesis/single-sample-concept-skeleton]] — editorial composition of this theme's primitives into a candidate method
- [[../single-sample-rl-finetuning/_overview]]
- [[../process-reward-models/_overview]]
