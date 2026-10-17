# Thinking Leakage in No-Think RL

Zhu et al. (KAUST/SJTU, arXiv:2610.14270) show that GRPO in no-think mode on hybrid Qwen3 models (1.7B/4B/8B) gains mostly by partially reactivating the model's own think-mode reasoning ("thinking leakage") rather than by learning new reasoning behavior. Evidence is causal: weight extrapolation, an 8-dim activation-subspace patch, and attention-head knockout/patching, all with random/PCA controls. The no-think accuracy approaches but never exceeds the original think-mode accuracy. This is a mode-control variant of the reuse-not-installation account, and a direct methodological warning for any single-sample RL result obtained on hybrid Qwen3 in no-think mode.

## Method

- **Training:** GRPO-style (PPO clip 0.2, token-mean, KL 1e-3), rank-64 LoRA on all linear layers, lr 1e-5, 256 prompts x 5 samples, $T=1$, DAPO-Math-17k, ~67 steps. No-think mode = empty `<think></think>` block appended by the chat template. Reward $\pm 1$ on final-answer correctness.
- **Think-likeness measures:** reflection-word count; think win rate (TWR, Mann-Whitney on per-token LLR of the original model under think vs no-think prefix); thinking activation shift $\alpha = \langle \delta_k, v\rangle / \lVert v\rVert^2$ at a mid layer, with $v$ the mean think-minus-no-think activation difference.
- **Interventions:**
  1. Weight extrapolation $W_0 + c\,\Delta W$, $c>1$, no further training.
  2. Cross-model activation patching restricted to an 8-dim think subspace $Q$ (mean think/no-think difference + 7 orthogonal residual-variance directions, estimated on the *original* model with 128 training prompts): $h_t \mathrel{+}= QQ^\top(h_s - h_t)$ over layers 1-35, in both directions (original-to-RL removes gain; RL-to-original transfers gain).
  3. Attention knockout of heads that attend the empty think block, plus single-head cross-model patching.
  4. One-step GRPO gradient probe on a fresh LoRA adapter.

## Claims

| Quantity (Qwen3-8B unless noted) | Value |
|---|---|
| AIME22-24 no-think accuracy, before -> after RL | 0.17 -> 0.43 (4B, 1.7B also rise) |
| Response length | 2.7k -> 7.2k tokens (think mode: 16-18k) |
| Reflection words | 1.3 -> 13.0 (think mode ~120-130) |
| TWR | 50% -> 94% (4B 86%, 1.7B 84%) |
| $\alpha$ | 0.56 (4B 0.40, 1.7B 0.21) |
| Original think-mode accuracy (8B/4B/1.7B) | 0.74 / 0.69 / 0.43 |
| Weight extrapolation | up to 0.72 (step-67 update), 0.68 (step-15); never above think mode 0.74 |
| `</think>` emission under $c$ (step 67) | 6% at $c=1.5$, 51% at $c=3$; base model: 0 of 1,260 no-think responses |

Scaled models emit `</think>` at the same relative position as native think mode (median 91% vs 92%).

## Mechanism evidence

- **Subspace patching (8B, step 67):** original-to-RL removes 75% of the RL gain $G$ (0.411 -> 0.244; original 0.189, $G=0.222$). RL-to-original transfers 50% (0.189 -> 0.300; 60% at 16 dims). Controls: PCA subspace 22%/25%, random -3%/10%, single think direction 22%.
- **Heads:** ~5-7 heads per model put $\ge 10\%$ attention on the empty think block. Knocking out the top-5% such heads gives $\alpha$ 0.78/0.88/0.66 and $R_{KL}$ 72/74/77% versus $\le 0.04$ / $\le 6\%$ for random heads. Top RL-patching heads (L18H19: 44% of the RL shift at 8B, 37% at 4B; L19H13: 54% at 1.7B) rank in the top 0.2-0.9% by block attention.
- **Why GRPO drifts toward think-like outputs:** within a group, correct responses are more think-like than wrong ones (TWR gap +5.9/+2.1/+1.6/+2.5 pp for $k=1..4$ correct of 5). Advantages sum to zero, so each group is a correct-vs-wrong contrast. A one-step probe shifts $\alpha$ by +0.0075 (full), +0.0072 (positive-only), +0.0057 (negative-only), but -0.0022 for shuffled advantages and +0.0006 for uniform +1 weights: the drift comes from the *assignment* of signed advantages to responses, not from reinforcing samples generally. Across groups, harder questions have more think-like correct responses (57.8% -> 40.5% as $k$: 1 -> 4); flagged by the authors as association only.

## Limitations

- Qwen3 only (Llama-Nemotron named, untested); math only; AIME22-24 = 90 problems x 2 samples, small and noisy.
- Weight-scaling factors tuned on the same 90 problems and $c$ far outside the training range (exploratory). Patching and head analysis mostly at 8B step 67; head analysis on fixed 2,048-token prefixes of original-model responses, not free generation.
- The GRPO-signal probe is a single initial-gradient step with tiny effects ($\Delta\alpha \approx 0.007$); cross-group trend confounded by difficulty.
- "Largely", not "entirely": RL-to-original transfers only 50-60%, and at 8B part of the shift ($0.58\lVert v\rVert$) is orthogonal to the think direction.
- Not tested: RL started in think mode, non-hybrid models, held-out-domain gains, and whether rank-64 LoRA / lr 1e-5 / 67 steps bias toward cheap mode-switch solutions. Length growth may partly confound TWR.
- Not a sample-efficiency paper: standard-scale RLVR, no single-sample or few-shot runs.

## Relevance to the thesis

- **Hard flag:** any single-sample (or few-shot) RL result on a hybrid Qwen3 model in no-think mode needs a **think-mode baseline** (same checkpoint, same eval, think on) before it is called concept acquisition. A gain that tracks toward, but not past, think-mode accuracy is mode access, not a new concept. Corollary: report the fraction of the gap to think mode closed, plus TWR/$\alpha$-style think-likeness, alongside accuracy. See [[1-shot-rlvr]] for the Qwen results this applies to.
- Supplies a candidate mechanism for "one example suffices on Qwen": a low-dim, cheaply reachable latent mode switch needs little data to flip. Consistent with the ceiling picture in [[../self-play/invisible-leash]] and [[../self-play/yue-rlvr-boundary]] (no-think RL never exceeds the model's own think-mode accuracy).
- Evaluation lesson for [[../concept-evaluation/_overview]]: separate "adds new capability" from "changes how existing capability is accessed". Candidate controls: think-mode baseline, subspace/head patching null, extrapolation-ceiling check.
- Localisation (8-dim subspace, few think-block-reading heads) parallels [[../selective-finetuning/_overview]] and acts as a steering intervention reproducing the RL gain ([[../decoding-time-steering/_overview]]).
- Soft tension with the "RLVR extends the reasoning boundary" reading in [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]; scope is limited to the hybrid no-think recipe.

## Source

- `raw/research/weekly-2026-10-16/04-thinking-leakage-rl.md`
- arXiv: [2610.14270](https://arxiv.org/abs/2610.14270) — Zhu, Liu, An, Aliev, Li, Yang, Ghanem, "The Thinking Leakage in Reinforcement Learning for LLMs"

## Related

- [[context-grounding-mechanism-reuse]] — closest sibling: head knockout + steering direction, reuse of pre-existing machinery
- [[spurious-rewards-rlvr]] — gains from amplifying pre-existing behaviour (also Qwen-specific)
- [[rethinking-rl-sparse-selection]] — RL as selection of latent behaviour, token/parameter level
- [[random-reward-reachability-probe]] — reachability of latent behaviour determines gain
- [[rlvr-pattern-selection-theory]] — RL shifts pattern use, not competence
- [[deepseekmath-grpo]] — GRPO signed-advantage contrast analysed in the mechanism section
- [[high-entropy-minority-tokens]] — reflection words as fork tokens; few tokens/heads carry the signal
- [[rl-sparse-subnetwork]] — weight-update structure
- [[relex-rank1-extrapolation]] — update extrapolation; here bounded by think-mode accuracy
- [[../self-play/yue-rlvr-boundary]]
- [[../self-play/invisible-leash]]
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]
- [[../single-sample-rl-finetuning/1-shot-rlvr]]
- [[../selective-finetuning/_overview]]
- [[../decoding-time-steering/_overview]]
- [[../concept-evaluation/_overview]]
- [[../weekly-briefs/2026-10-16]] — brought in by the 2026-10-16 weekly sweep
