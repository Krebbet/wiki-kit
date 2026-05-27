# Wiki Index

Modular transformer architecture research — swappable transformer blocks, dynamic per-block parameter allocation, and token-conditional routing through a pool of blocks.

Catalog of all pages in this wiki. Updated on every ingest.

---

## Overview

### Survey / taxonomy

| Page | Summary |
|---|---|
| [[research/modular-deep-learning]] | Canonical survey (TMLR 2023). 4-axis taxonomy (computation function, routing function, aggregation function, training setting); unifying form $f_\theta(x)+f_\phi(x)$. Hub page — every other wiki page cross-mapped to a taxonomy cell. |

### Concepts

| Page | Summary |
|---|---|
| [[concepts/block-isolation-training]] | Synthesis anchor for **G1**. Three flavours of block-isolation training (output reconstruction, module replacement, local auxiliary loss + gradient stop) and their evidence base. Open questions for transferring CNN/PTQ-era results to autoregressive transformer training-from-scratch. |
| [[concepts/token-conditional-routing]] | Synthesis anchor for **G3**. Routing-primitive taxonomy populated by [[mod]] (per-token depth-routing, primary citation), [[sparse-upcycling]] / [[btx]] (FFN-expert routing), [[calm]] (per-token confidence-based early exit), [[demix]] (domain-conditional), [[btm]] (ensemble routing), [[layerskip]] (skip-as-routing pressure). Surfaces Modular-DL-Survey §4.2.3 caution: token-level MoE routing impedes task-level specialisation via load-balancing. |

### Research — Quantization (block / layer reconstruction lineage)

| Page | Summary |
|---|---|
| [[research/brecq]] | Block-by-block PTQ reconstruction with Fisher-weighted output distortion; INT2 PTQ comparable to QAT for the first time. ICLR 2021. |
| [[research/gptq]] | Layer-wise PTQ via per-layer Hessian-based weight rounding; 175B-param GPT models in ~4 GPU-hours, 3-4 bits/weight. ICLR 2023. |
| [[research/awq]] | Activation-aware per-channel scaling for weight-only PTQ; no backprop, widely deployed (HF, vLLM, TensorRT-LLM). MLSys 2024 Best Paper. |
| [[research/omniquant]] | Block-wise differentiable PTQ with Learnable Weight Clipping (LWC) + Learnable Equivalent Transformation (LET); QAT-quality at PTQ cost down to W2A16 / W4A4. ICLR 2024 spotlight. |
| [[research/spinquant]] | PTQ via learned orthonormal rotations (Cayley SGD on the Stiefel manifold) to absorb activation/weight outliers; closes W4A4KV4 gap on LLaMA-2 7B to ~2.9 pts. arXiv 2024 (Meta). |

### Research — Block / module replacement & heal-after-removal

| Page | Summary |
|---|---|
| [[research/bert-of-theseus]] | Progressive module replacement training via Bernoulli gate $z_\ell(t) \sim \text{Bernoulli}(p(t))$; closest direct analogue to **G1**. EMNLP 2020. |
| [[research/dcr]] | Deterministic continuous replacement: replaces Theseus's stochastic gate with a deterministic blend $\alpha(t)$. NeurIPS 2025 ScaleOPT *workshop*; single seed, no code, no heterogeneous-operator experiments — read with caveats. |
| [[research/iterative-layer-distill]] | Iterative pruning of least-important transformer layers + joint KL+MSE distillation per removal; the heal-after-removal training primitive **G1** needs. arXiv 2025 (single-lab, narrow eval). |
| [[research/legonn]] | Modular encoder-decoder with CTC-grounded marginal-distribution interface; gradient-isolating BeamConv variant lets pieces be reused across MT/ASR tasks without finetuning. IEEE/ACM TASLP 2023. |

### Research — Block pruning + skipping

| Page | Summary |
|---|---|
| [[research/sleb]] | Training-free post-hoc block elimination via calibration-set perplexity scoring; no recovery training. ICML 2024. |
| [[research/layerskip]] | Layer dropout + shared early-exit head trains every prefix to produce useful output; enables self-speculative decoding without auxiliary modules. arXiv 2024 (Meta FAIR). |
| [[research/shortgpt]] | Block Influence metric $\mathrm{BI}_i = 1 - \mathbb{E}\,\cos(X_i, X_{i+1})$ on residual stream; one-shot layer removal by lowest BI. Cosine-similarity choice is in tension with [[sleb]]; see [[conflicts/shortgpt-vs-sleb-redundancy-metric]]. arXiv 2024. |

### Research — Token-conditional routing / dynamic depth

| Page | Summary |
|---|---|
| [[research/mod]] | Mixture-of-Depths: per-block top-k token routing across depth; static tensor sizes; matches dense baseline at fraction of FLOPs/forward. **Primary citation for [[concepts/token-conditional-routing]].** arXiv 2024 (DeepMind). |
| [[research/calm]] | Confidence-adaptive language modeling: per-token early exit driven by softmax / hidden-saturation / classifier confidence; up to ×3 certified speedup. NeurIPS 2022. Natural pairing with [[layerskip]]'s training-time prefix-isolation. |
| [[research/depth-adaptive-transformer]] | Per-token depth routing via geometric-like halting in seq2seq decoder; reference solution for attention consistency under variable-depth exits (state copy + layer-specific KV projection). 76% decoder-layer reduction on IWSLT14 De-En. ICLR 2020. |
| [[research/loopformer]] | Sinusoidal $(t, \Delta t)$ step conditioning on a weight-tied decoder breaks fixed-point stagnation; enables elastic-depth (budget-conditioned) inference. Directly resolves Technical Challenge 2 (hidden-state observability) in [[experiments/exp1-router-replication]]. arXiv 2026. |
| [[research/adaponderlm]] | Per-token early exit for recurrent LMs via monotonic halting masks + `where(mask, K_new, K_prev)` KV-reuse; concrete tested solution for Exp 1 Challenge 3 (variable-depth attention consistency without irregular control flow). arXiv 2025. |
| [[research/tide]] | Post-training per-token early exit for decoder LLMs; cosine-convergence routers more reliable than softmax entropy for generation; KV-cache-safe post-hoc mode. NeurIPS 2023. |

### Research — Loop / recurrent-depth architectures

| Page | Summary |
|---|---|
| [[research/universal-transformers]] | Weight-tied single block applied recurrently with per-position ACT halting; proves Turing-completeness of depth-recurrent networks; foundational architecture for Huginn / Experiment 1. ICLR 2019. |
| [[research/huginn]] | 3.5B depth-recurrent decoder LM (prelude/core/coda); single shared core block iterated $r$ times; EXP1 router insertion point documented: after `core_block(s, e)`, observing $s_i \in \mathbb{R}^{n \times 5280}$ unnormalized. arXiv 2025. |
| [[research/parcae]] | Stable middle-looped LM via spectral-norm ZOH recurrence; 140M–1.3B checkpoints at `SandyResearch/parcae-*`; loop scaling laws; Exp 1 fallback base if Huginn-3.5B exceeds VRAM. arXiv 2026. |
| [[research/mechanistic-looped-lms]] | Cyclic fixed-point convergence within $k \approx 1$–$2$ recurrences post-prelude for input-injection LMs (Huginn); $h^{(k)}$ encodes no step signal after recurrence 2; directly confirms severity of Exp 1 Challenge 2. arXiv 2025. |
| [[research/ouro]] | Pre-trained LoopLM family (1.4B/2.6B, 7.7T tokens); two-stage adaptive halting (entropy-KL pretraining + exit-gate fine-tune); matches Qwen3-4B/8B at 2–3× parameter efficiency; gains traced to knowledge manipulation (multi-hop), not capacity. arXiv Oct 2025 (ByteDance Seed). |
| [[research/rltt]] | RLTT (Williams & Tureci, Princeton Feb 2026): distributes GRPO reward across all T_max latent loops instead of terminal loop only; +14.4% MATH-500, +16.6% AIME24, +18.7% GPQA over GRPO on Ouro-2.6B-Thinking. G3 High. |
| [[research/looprpt]] | First RL pre-training for looped LMs: step-wise rewards via EMA teacher + difficulty-aware time penalty; entropy-based hard-token selection; Pareto dominance over Ouro baseline and Qwen3-1.7B CoT at 1.4B/2.6B. arXiv Mar 2026 (Harbin/Tsinghua). |

### Research — Adaptive / learned halting

| Page | Summary |
|---|---|
| [[research/act]] | Original learned-halting for RNNs via accumulated halt probabilities + remainder trick + ponder cost; biased gradient at halting boundary; documented instability makes PonderNet preferred for Exp 1. arXiv 2016. |
| [[research/pondernet]] | Adaptive halting via conditional geometric halt distribution + KL-vs-prior regularization; unbiased gradients over the full horizon; recommended halting mechanism for Exp 1. NeurIPS 2021 (DeepMind). |
| [[research/repeat-rnn]] | Fixed-$\rho$ Repeat-RNN matches or beats ACT on parity/addition; adaptive halting adds no task-accuracy benefit at small scale; directly supports the trivial-solution concern for Exp 1 Challenge 5. arXiv 2017. |

### Research — Latent / continuous reasoning

| Page | Summary |
|---|---|
| [[research/coconut]] | Latent-mode reasoning feeding last hidden state $h_{t-1}$ as next embedding (bypassing decode+re-embed); differentiable continuous thought; implicit BFS over reasoning paths shown by probing; curriculum training required; matches CoT on ProntoQA/ProsQA, below CoT on GSM8K. arXiv Dec 2024 (Meta). |
| [[research/etd]] | Encode-Think-Decode: partition a pretrained LLM into E/T/D blocks via angular-distance (Kneedle) analysis, loop only the T block $k$ times; +28.4% GSM8K, +36% MATH on OLMo-2 1B; ACT variant learns per-token halting; MATH degrades at $k>3$. arXiv Oct 2025. |

### Research — Knowledge distillation (offline / cached logits)

| Page | Summary |
|---|---|
| [[research/sparse-logit-sampling]] | Proves top-K logit caching is a biased KD estimator (formal theorem); proposes RSKD (importance sampling, N=12 tokens) matching full-KD quality at 25× lower storage. Directly constrains Exp 1 Challenge 4: top-K cache is wrong, must use RSKD. arXiv 2025 (Samsung Research). |

### Research — Local / decoupled learning (foundational, CNN-era)

| Page | Summary |
|---|---|
| [[research/decoupled-greedy-learning]] | DGL: per-layer auxiliary local loss with sync/async parallelism + replay buffer. Existence proof that a CNN block can be trained to convergence with no global gradient. ICML 2020. |
| [[research/greedy-infomax]] | GIM: gradient-isolated CNN/audio module stack with local InfoNCE objective; competitive self-supervised representations without cross-module backprop. NeurIPS 2019. |

### Research — PEFT / parameter-efficient fine-tuning

| Page | Summary |
|---|---|
| [[research/lora]] | Low-rank adapter matrices injected in parallel with frozen backbone weights; canonical PEFT primitive at ~0.01% updated parameters, zero inference overhead post-merge. ICLR 2022. |
| [[research/adapters-houlsby]] | Sequential bottleneck modules in frozen BERT within 0.4% of full fine-tune at 3.6% parameter cost; foundational adapter pattern. ICML 2019. |

### Research — Mixture-of-Experts / domain-expert pools

| Page | Summary |
|---|---|
| [[research/btm]] | Forest of fully-independent Expert LMs (one per domain, zero parameter sharing); branch-train-merge loop; ensembled 64-expert 22.4B-param forest matches monolithic 1.3B at ~2.5× compute. arXiv 2022 (UW / Meta AI). |
| [[research/btx]] | Three-stage recipe unifying BTM + sparse-upcycling: independent domain fine-tuning → FFN expert install → router fine-tune. Embarrassingly parallel expert phase. arXiv 2024 (Meta FAIR). |
| [[research/sparse-upcycling]] | Copy-and-train MoE bootstrap: replaces MLP layers with $E$ expert copies + router, resumes from dense checkpoint; outperforms dense continuation and MoE-from-scratch up to 100% dense pretraining compute. ICLR 2023. |
| [[research/demix]] | Domain-specialist FFN experts routed deterministically at document level; modular at FFN granularity — experts can be added/removed post-training. NAACL 2022. |

### Research — Model growth / continual expansion

| Page | Summary |
|---|---|
| [[research/bert2bert]] | Function-preserving growth (FPI + AKI) initialises a larger transformer from a smaller pretrained one; 45–47% compute savings vs. scratch. ACL 2022. |
| [[research/ligo]] | Learns a linear operator mapping small-model parameters to large-model init in ~100 SGD steps; subsumes prior FPI schemes. Saves 22–55% FLOPs vs. scratch. arXiv 2023. |

### Research — Structured pruning + sparsity

| Page | Summary |
|---|---|
| [[research/lottery-ticket-bert]] | Sparse winning-ticket subnetworks in BERT at 40–90% sparsity; MLM-found masks transfer universally at 70% sparsity. ICLR 2020. |
| [[research/sheared-llama]] | Structured pruning of LLaMA2-7B via learned hard-concrete masks + dynamic batch loading; canonical LLM-scale evidence for block-isolation-training. arXiv 2023. |

### Experiments

| Page | Summary |
|---|---|
| [[experiments/exp1-router-replication]] | Experiment 1 proposal: train a lightweight router (frozen weights) to replicate a Loop LLM's static execution path; verifies router learnability and resolves routing-granularity and halting-mechanism design choices before heterogeneous blocks are introduced. Includes research call list for 7 papers not yet in the wiki. |

### Bookkeeping

| Page | Summary |
|---|---|
| [[research-queue]] | Dangling cross-ref targets queued for future `/research` runs. Remaining Experiment 1 blockers: [[looped-transformers]], [[block-recurrent-transformers]], [[deq]]. Foundational multi-source baselines: [[smoothquant]], [[switch-transformer]], [[hash-routing]], [[adaround]], [[llm-int8]]. |

---
