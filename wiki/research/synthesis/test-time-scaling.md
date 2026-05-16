---
name: test-time-scaling
description: Cross-cutting catalog of test-time scaling (TTS) techniques in the corpus — investing more inference compute without weight updates to improve output quality. Five modalities (length, sample+verifier, search, iterative refinement, decoding-time/activation steering) plus distinction from test-time *training*. Anchor page for an otherwise scattered concept.
type: synthesis
---

# Test-Time Scaling — Cross-Cutting Synthesis

*Editorial synthesis built 2026-05-14 from existing wiki content; no single corpus paper proposes "test-time scaling" as a unified frame. Companion in spirit to [[../decoding-time-steering/_overview]] (which catalogues one modality of TTS in depth) and [[proposer-reward-shapes]] (which catalogues another cross-cutting design axis).*

## One-paragraph summary

Test-time scaling (TTS) is the practice of **investing more inference-time compute to improve output quality without changing weights**. The corpus contains five distinct modalities: length scaling (longer CoTs), sample scaling with a verifier (best-of-$k$ + PRM), search scaling (MCTS / tree search), iterative refinement (generate-critique-revise), and decoding-time / activation steering (logit and activation manipulation). All five operate within the **base model's support** ([[../self-play/invisible-leash]] Theorem C.1 at inference is the same constraint as at training): TTS *selects* and *concentrates* probability mass on better outputs rather than introducing new capability. The wiki's strongest single-method TTS multiplier is [[../self-play/rstar]] (LLaMA2-7B GSM8K 12.51% → 63.91% via MCTS-only, no fine-tuning); the strongest *trained* TTS surface is [[../single-sample-rl-finetuning/deepseek-r1]] (R1-Zero's emergent long-CoT). TTS is distinct from **test-time *training*** (TTT, see [[../test-time-training/_overview]]), which *does* update weights per input.

## Definition and boundary

- **TTS** — no weight updates. More compute (more tokens, more samples, more search, more refinement passes, modified decoding) extracts more performance from a fixed model.
- **TTT** — *does* update weights at inference. [[../test-time-training/ttt-few-shot]] (per-input synthetic dataset + temporary gradient updates on ARC), [[../test-time-training/tempo]] (EM-framed E-step critic recalibration + M-step policy refinement), [[../test-time-training/algorithm-distillation]] (in-context RL — closer to TTS in spirit but technically a pretrained-then-frozen ICL phenomenon).

The two are sometimes conflated in the literature; this page is strictly about TTS. The TTT theme page already distinguishes itself from in-context-RL inside its own overview.

## The five TTS modalities

| Modality | Mechanism | Canonical example | Headline result | Cost shape |
|---|---|---|---|---|
| **Length scaling** | Generate longer CoTs | [[../single-sample-rl-finetuning/deepseek-r1]] (R1-Zero: response length grows monotonically during RL; AIME 15.6 → 77.9 pass@1) | RL teaches the model to *use* more inference tokens; the long-CoT capability is a trained TTS surface | Linear in tokens; capped by attention dilution past an optimum |
| **Sample scaling + verifier** | Generate $k$ samples, rerank via verifier or majority vote | [[../process-reward-models/training-verifiers-gsm8k]] (Cobbe et al., token-level verifier reranking on GSM8K); [[../process-reward-models/lets-verify-step-by-step]] (PRM800K beats outcome supervision on MATH); [[../self-improvement/self-rewarding-lm]] (LLM-as-judge for reranking) | Pass@1 ≪ pass@$k$ with a good PRM; process labels beat outcome labels at fixed verifier budget | Linear in $k$; verifier compute amortised |
| **Search scaling** | MCTS / tree search at inference, optionally with PRM | [[../self-play/rstar]] (32 MCTS rollouts × 5 actions, peer-sized SLM discriminator via prefix-completion agreement; **LLaMA2-7B GSM8K 12.51% → 63.91% no fine-tuning**); [[../self-improvement/rstar-math]] (MCTS + self-evolved PRM, small LLMs at SOTA math); [[../self-play/alphazero]] (closed-domain prototype) | Strongest pure-TTS multiplier in the corpus on small models; rStar's 5-action menu (decompose / fast-path / sub-question / re-answer / rephrase) is a drop-in per-problem template | Branching-factor × depth × per-node compute |
| **Iterative refinement** | Generate, critique, revise loop | [[../critique-self-correction/self-refine]] (same-model loop); [[../critique-self-correction/reflexion]] (verbal RL with episodic memory); [[../critique-self-correction/critic-tool-interactive]] (CRITIC: frozen LLM + external tool feedback, **+10pp over ReAct on AmbigNQ — tools are necessary, self-only degrades**); [[../critique-self-correction/critic-cot]] (System-2 step-wise critique; 93.3% GSM8K, 57.8% MATH500) | Cheap, single-model; *tool grounding is load-bearing* for crossing the self-only plateau | Linear in refinement rounds |
| **Decoding-time / activation steering** | Modify logits or activations at decode time | [[../decoding-time-steering/_overview]] (13 captured methods across PPLM / GeDi / FUDGE / DEXPERTS / CD / CD-for-reasoning / DoLa / CFG / ActAdd / CAA / ITI + Linear Representation Hypothesis) | **Unanimous cross-source finding: information is already in the base model; an offline reweighting prior puts it into the right solution space** | Per-token overhead; no extra samples needed |

Additional methods on the TTS boundary (covered elsewhere but worth flagging):

- [[../critique-self-correction/prometheus-2]] — open-source 7B/8x7B evaluator LM unifying direct + pairwise assessment via weight merging; used as a TTS-stage judge (r=0.685 on MT Bench).
- [[../process-reward-models/pav-rewarding-progress]] — PAV: process advantage as step-level progress under a complementary prover; **>8% search gain, 5–6× RL efficiency over outcome RM**. PAV slots in at the verifier/PRM stage of either sample-scaling or search-scaling.
- [[../process-reward-models/math-shepherd]] — automated step labels from rollout success rate; PRM training-data recipe without human annotation.

## How it's being used — six documented patterns

**1. RL trains the TTS substrate, then TTS extracts it.** [[../single-sample-rl-finetuning/deepseek-r1]] R1-Zero shows emergent long-CoT and self-reflection ("aha moment") during RL training — RL is teaching the model to use more inference tokens productively. Once trained, the model spends those tokens at inference. The pass@1 improvement is largely a trained-TTS improvement. The reverse direction (TTS-without-training) is rStar.

**2. Outcome-only RL is wasteful at test-time without process supervision.** [[../rlvr-mechanics/learning-to-think]] Sec 3.2: GRPO-trained DeepScaleR uses >2× the minimum tokens needed; accuracy *peaks at ~16–20 episodes then declines* due to attention dilution and context truncation. Adding a raw length penalty makes things worse ([[../rl-optimizers/dapo]]'s Overlong Reshape exists for this reason). **Process-dense rewards are needed to extract the full benefit of test-time compute scaling** — verbatim from [[../rlvr-mechanics/_overview]].

**3. Search dominates length on small models without a verifier.** [[../self-play/rstar]]'s LLaMA2-7B GSM8K 12.51% → 63.91% is the strongest captured pure-TTS multiplier — no fine-tuning, 32 MCTS rollouts with 5 actions, peer-sized SLM discriminator via prefix-completion agreement. Sample-and-pick patterns at the same compute budget produce smaller gains on the same model class.

**4. Best-of-$k$ + PRM is the verifier-class TTS pattern.** [[../process-reward-models/training-verifiers-gsm8k]], [[../process-reward-models/lets-verify-step-by-step]] (PRM800K), [[../process-reward-models/math-shepherd]] (automated step labels), [[../process-reward-models/pav-rewarding-progress]] (PAV). The PRM is reused at training (RL signal) and inference (reranking) — see [[../process-reward-models/_overview]].

**5. Tools beat self-only refinement.** [[../critique-self-correction/critic-tool-interactive]] CRITIC: +10pp over ReAct on AmbigNQ; **self-only refinement degrades**. Tool grounding is the load-bearing variable for crossing the self-refinement plateau. [[../critique-self-correction/critic-cot]] supplies the SFT recipe to *build* the critique RM when none is off-the-shelf.

**6. Decoding-time / activation steering is the no-weight-update TTS branch.** [[../decoding-time-steering/_overview]] (added 2026-05-13). Logit-level reweighting (PPLM, GeDi, FUDGE, DEXPERTS, CD, CD-for-reasoning, DoLa, CFG), activation-level steering (ActAdd, CAA, ITI), and the Linear Representation Hypothesis as theory anchor. Closest training-time cousin is REASONMAXXER's rank-8 $W_O$ LoRA ([[../rlvr-mechanics/rethinking-rl-sparse-selection]]) — low-rank routing correction rather than capability addition.

## Where TTS sits in the project's method proposals

- **[[proposed-method]] component G (Diversity injection)** — lists [[../self-play/rstar]]'s 5-action MCTS template as a drop-in per-problem multiplier. TTS-as-inner-loop diversity source.
- **[[proposed-method]] R_w extension (2026-05-13)** — decoding-time / activation steering becomes a load-bearing component, complementing the SFT-side **C_w** weight-update reference. R_w is the no-weight-update branch of the same support-lifting strategy.
- **[[concept-curriculum-method]] step (e) test-train-retest loop** — TTS at the test step is natural (multi-sample voting, MCTS, or refinement before retraining). The page does not currently spell out which TTS modality to use at test time; open design slot.
- **[[single-sample-concept-skeleton]]** — does not include a TTS axis explicitly. The rStar template lives only in proposed-method and concept-curriculum-method.

## Hard limits the corpus puts on TTS

| Limit | Mechanism | Source |
|---|---|---|
| **Self-only refinement plateaus** | Without external grounding, iterative refinement degrades past a few rounds | [[../critique-self-correction/critic-tool-interactive]] |
| **Length scaling without process supervision peaks then declines** | Attention dilution, context truncation past an optimum | [[../rlvr-mechanics/learning-to-think]] Sec 3.2 |
| **TTS doesn't escape the support bound** | Inference-time sample/search re-weighting is the same selection-not-learning principle as RLVR | [[../self-play/invisible-leash]] Theorem C.1; [[../self-play/yue-rlvr-boundary]] pass@k inversion; [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] Theorem 6 one-shot saturation |
| **Reranker quality caps best-of-$k$** | A weak verifier reranks toward the wrong sample; gains saturate | [[../process-reward-models/lets-verify-step-by-step]] (process > outcome at fixed $k$); [[../process-reward-models/pav-rewarding-progress]] |
| **Search compute scales with branching × depth** | Pure MCTS becomes expensive on long-horizon problems | [[../self-play/rstar]] (32 rollouts × 5 actions × depth — fixed budget) |

## TTS × training composition

TTS interacts with training in three documented ways:

1. **Training to use TTS better.** RL on long-CoT (R1) trains the model to spend test-time tokens productively. [[../rlvr-mechanics/learning-to-think|L2T]]'s info-gain reward is designed specifically to align RL with TTS efficiency.
2. **TTS as data generator for training.** rStar-Math uses MCTS rollouts to generate the training data for the next round of SFT — TTS becomes a curriculum source. [[../self-improvement/rstar-math]]; structurally the same move as [[../self-improvement/star|STaR]]'s rationalise-then-SFT.
3. **TTS as evaluation harness.** Best-of-$k$ + PRM at inference is the standard way to measure pass@$k$ — the verifier is the same one used at training, just used to *select* rather than to *teach*.

## Watchlist (TTS-specific candidates)

Categorical targets — promote individual papers as they surface:

- **Compute-optimal search** — variants of MCTS / beam that allocate compute as a function of problem difficulty.
- **Process-reward extensions to inference** — applying PAV / step-progress signals during search, not just during training.
- **Self-refinement + tool generalisations** — beyond CRITIC, what tools matter beyond search engines / interpreters / calculators?
- **Diffusion-style iterative decoding for LMs** — non-autoregressive TTS modalities; currently zero corpus coverage.
- **[[../../watchlist|Watchlist]] entry**: TTC-RL (arXiv:2510.04786) — automatic test-time curricula; 1.8× AIME25; ICLR 2026.

## Source

Editorial synthesis. Drawn entirely from existing wiki pages cited inline; no single source proposes "test-time scaling" as a unified concept.

## Related

- [[../decoding-time-steering/_overview]] — depth coverage of TTS modality 5 (decoding-time / activation steering)
- [[../test-time-training/_overview]] — the *training* sibling; distinct from TTS, important to keep separate
- [[../self-play/rstar]] — strongest pure-TTS multiplier in the corpus (rStar-search)
- [[../self-improvement/rstar-math]] — TTS-as-data-generator pattern
- [[../process-reward-models/_overview]] — the verifier infrastructure that powers sample-scaling TTS
- [[../critique-self-correction/_overview]] — iterative refinement TTS family
- [[../single-sample-rl-finetuning/deepseek-r1]] — length-scaling as a trained TTS surface
- [[../rlvr-mechanics/learning-to-think]] — what process-dense rewards extract from TTS that outcome-only RL misses
- [[../self-play/invisible-leash]] / [[../self-play/yue-rlvr-boundary]] / [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — hard limits inherited from the RL-as-selection thesis
- [[proposed-method]] — component G uses rStar TTS as inner-loop multiplier
- [[proposer-reward-shapes]] — companion cross-cutting catalog (different axis)
- [[fine-tuning-best-practices]] — pairing TTS with SFT and RLVR practices
