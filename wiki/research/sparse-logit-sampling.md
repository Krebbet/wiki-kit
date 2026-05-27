# Sparse Logit Sampling: Accelerating Knowledge Distillation in LLMs

Anshumann, Zaidi, Kedia et al. (Samsung Research, arXiv 2503.16870, Mar 2025) prove that caching top-K teacher logits for offline knowledge distillation is a **biased** estimator of the full teacher distribution, causing mis-calibrated students and suboptimal loss. They propose Random Sampling KD (RSKD), an importance-sampling fix that matches full-distribution distillation quality using only ~12 cached tokens per training token — 25× sparser than prior top-K work — with <10% overhead versus cross-entropy training.

---

## The bias problem

**Top-K caching.** Offline distillation pre-computes the teacher's output distribution $t \in \mathbb{R}^{|V|}$ once per token and stores a sparse approximation $t^s$. The intuitive approach stores the $K$ largest probabilities:

$$t^s_i = \begin{cases} t_i & i \in \mathcal{K} \\ 0 & \text{otherwise} \end{cases} \qquad \sum_i t^s_i < 1$$

**The bias.** When KL-divergence loss is computed against $t^s$, the gradient for logit $x_i$ of the student ($p_i$ = student probability, $t_i$ = teacher probability) is:

- **Full KD (unbiased):** $\quad \dfrac{\partial L}{\partial x_i} = p_i - t_i$

- **Top-K KD (biased):** $\quad \dfrac{\partial L}{\partial x_i} = \left(\sum_{j \in \mathcal{K}} t_j\right) p_i - t_i$

The factor $\sum_{j \in \mathcal{K}} t_j < 1$ upscales the gradient's positive term for all top-K tokens, driving the student to assign excess probability mass to $\mathcal{K}$. Non-top-K tokens are effectively pushed to probability zero. The student learns a rescaled, mis-calibrated version of the teacher: over-confident on top-K, under-confident on the tail. This is proved in the paper's Appendix A.4 and confirmed empirically.

**Magnitude.** With $K < 25$ tokens, top-K training performs *worse* than pure cross-entropy (Table 1). Expected Calibration Error (ECE) worsens monotonically as $K$ decreases. At $K = 300$ tokens the gap to full KD is still 23%.

**Two compounding causes:**
1. Upscaled probabilities (bias in gradient direction and norm).
2. Missing tail supervision — rare ground-truth tokens that land in the tail receive zero signal from the teacher, falling back to CE on those positions only.

---

## RSKD: the importance sampling fix

**Core idea.** Replace top-K truncation with random sampling from the teacher distribution. For a proposal distribution $q(x)$, importance sampling gives an unbiased estimate of any expectation under $t$:

$$\mathbb{E}_t[f(x)] = \mathbb{E}_q\!\left[f(x)\,\frac{t(x)}{q(x)}\right]$$

Top-K violates the unbiasedness condition: it assigns $q(x) = 0$ to non-top-K tokens where $t(x) \neq 0$.

**RSKD estimator.** Use $q = t^\tau$ (temperature-scaled teacher distribution) as the proposal. Sample $N$ token ids (with replacement). For each token $i$, the sampled sub-distribution is:

$$t^s_i = \frac{c_i}{N}, \qquad c_i = \text{count of token } i \text{ in } N \text{ draws}$$

(For $\tau = 1$ the likelihood ratio $t_i/q_i = 1$; counts are the estimator directly.) Loss is forward KL between $t^s$ and student predictions, summed over non-zero entries of $t^s$.

**Theorem.** RSKD preserves the gradient in expectation: $\mathbb{E}[\nabla L_\text{RSKD}] = \nabla L_\text{FullKD}$ (Appendix A.7). Gradient angle between RSKD ($N=12$) and FullKD: 4° with norm ratio 1.0. Top-K ($K=300$) has angle 30° and norm ratio 1.3 (Table 3).

**Hyperparameters.** $\tau \in [0.8, 1.2]$ is robust (Table 12); authors use $\tau = 1$. $N = 12$ unique tokens suffices for 300M–3B students (Table 6).

**Computational overhead.** RSKD requires computing KL loss over the full vocabulary at training time (the cached indices vary per sample), adding ~10% overhead vs. cross-entropy. It is 1.7–2.6× faster than full online KD at 300M–3B scale (Table 4).

**Storage.** 12 tokens × 3 bytes/token (17-bit vocab ID + 7-bit probability) = 3.6 TB for 100B training tokens. Top-K 300 requires 90 TB; full KD would require ~10 PB (Table 5).

**Quality.** At 3B → 300M, RSKD (12 tokens) matches full KD on LM loss, ECE, speculative decoding acceptance rate, and 0-shot NLU (Table 6). At 8B → 3B, 100B tokens, RSKD (12 tokens) slightly *outperforms* full KD on downstream/instruction-following tasks (Tables 8–9). Top-K 12 is 4.7% ECE vs. RSKD's 0.2%.

---

## Implications for Experiment 1

[[experiments/exp1-router-replication]] identifies Challenge 4 as: *pre-compute and cache $p_\text{static}$ logits over the training corpus before router training begins.* The proposal marks this "manageable" because it is a one-time cost over the frozen-weight phase.

This paper makes Challenge 4 **harder than assessed**:

1. **Top-K caching is the wrong strategy.** A top-K cache of $p_\text{static}$ logits will produce biased KL gradient estimates when the router is trained against them. The bias grows with decreasing $K$; at the storage budgets plausible for a single-researcher setup ($K \leq 50$), the bias is severe enough to degrade calibration dramatically and push student loss below the CE baseline.

2. **RSKD is the correct replacement.** Caching must use random sampling from $p_\text{static}$ (with $N \approx 12$, $\tau = 1$), not top-K. The cached format changes: instead of the $K$ largest logit values, store $N$ randomly sampled token IDs (indices, no need to store magnitudes when $\tau = 1$). At 3 bytes/token × 12 tokens this is practical.

3. **Storage is not the binding constraint.** RSKD at $N=12$ requires 3.6 TB for 100B tokens — likely too large to pre-cache on a single workstation for full training corpora. The practical implication: either (a) cache on-the-fly in a two-process pipeline (teacher server + student trainer, defeating the purpose of pre-caching), or (b) pre-cache a smaller subset and stream the rest, or (c) use a much smaller corpus for the frozen-weight router phase.

4. **Gradient instability from bias compounds Challenge 1.** Challenge 1 is gradient instability through the halt head. A biased training signal from top-K caching adds noise to the gradient estimate that could be misattributed to the halting mechanism — making the stability diagnostic harder to interpret. Correct the bias first (RSKD cache) before diagnosing halt-gradient issues.

**Recommended action for Exp 1:** Switch the cache format from top-K to RSKD with $N=12$, $\tau=1$. Treat Challenge 4 as requiring re-specification, not just scheduling.

---

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (block isolation / swappability) | Low | KD is the training signal for the router, not the block isolation mechanism itself. Indirect at best. |
| **G2** (per-block dynamic parameter budget) | None | Out of scope; paper does not address parameter allocation. |
| **G3** (token-conditional routing) | **Moderate — load-bearing for Exp 1** | Exp 1 trains the router via KL imitation against a cached $p_\text{static}$. RSKD determines whether that training signal is unbiased. Correct implementation of the cache is a prerequisite for G3's Exp 1 milestone. |

---

## Credibility

- **Venue/year:** arXiv 2503.16870, submitted March 2025, revised July 2025. Samsung Research. Not yet in a peer-reviewed venue as of capture date (2026-05-26). However, the bias proof (Appendix A.4, A.7) is a formal theorem with closed-form gradient expressions, independently verifiable. The empirical results span 300M–3B models, synthetic tasks, CIFAR-100, and 100B-token LLM pre-training.
- **Code:** Public at `https://github.com/akhilkedia/RandomSamplingKD`.
- **Proof of bias:** Yes — Theorem (Appendix A.4) gives the exact gradient formula for top-K KD; the bias term $(\sum_{j \in \mathcal{K}} t_j - 1)p_i$ is derived analytically. The unbiasedness of RSKD is proved in Appendix A.7.
- **Independent corroboration:** Busbridge et al. (2025, Distillation Scaling Laws) also observed top-K bias and mis-calibration; cited in the paper.
- **Scale caveat:** Maximum evaluated scale is 3B student, 8B teacher, 100B tokens. Larger scales extrapolated but untested.

---

## Empirical claims

- Top-K $K < 25$: student LM loss *worse* than CE baseline (Table 1).
- Top-K $K = 300$: 77% of CE→FullKD gap, ECE 1.5%. RSKD $N=12$: effectively 100% of gap, ECE 0.8% (Tables 1, 6).
- RSKD gradient angle from FullKD: 4° vs. 12–58° for top-K (Table 3).
- Throughput: RSKD is 2.6× (300M) and 1.73× (3B) faster than full online KD (Table 4).
- 8B → 3B, 100B tokens: RSKD outperforms FullKD on instruction-following (59.4 vs. 58.4 IF SFT score, Table 8) and LLM-as-judge generative tasks (65.6 vs. 62.2 avg, Table 9).

---

## Open questions

- Does the RSKD unbiasedness result hold when the proposal distribution and the training distribution diverge (i.e., when the frozen teacher was pre-trained on a different corpus from the router training data)? Challenge 7.2 in the paper (teacher adaptation) suggests this matters significantly.
- At what corpus size does the RSKD cache become impractical for a single-GPU setup? The paper assumes server-scale storage; Exp 1 needs a feasibility estimate for ~10B tokens.
- Can the RSKD cache be generated in a single streaming pass over the training corpus without materializing it all at once?
- Does the gradient-preserving property of RSKD transfer when the student (router) is much smaller and architecturally different from a language model head?

---

## Source

- `raw/research/loop-challenges/06-sparse-logit-sampling-abs.md`
- `raw/research/loop-challenges/10-sparse-logit-sampling-pdf.md`

---

## Related

- [[act]] — differentiable halting mechanism whose gradient instability is compounded by biased KD signals
- [[pondernet]] — recommended halt mechanism for Exp 1; combines with RSKD cache strategy
- [[experiments/exp1-router-replication]] — Exp 1 proposal; Challenge 4 (pre-caching $p_\text{static}$) is directly addressed by this paper
