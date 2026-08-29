# Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO

Ba, Zheng, Xie et al. (SUSTech/NUS/Huawei Noah's Ark/CityU HK, arXiv:2608.27351) show theoretically and empirically that Evolution Strategies (ES) post-training improves Pass@1 over base *while also* achieving higher Pass@K than GRPO and the base model — unlike GRPO, which exhibits entropy collapse and often falls below the base model at large K. ES's large whole-model parameter drift is functionally concentrated in a sparse subset of larger-magnitude updates (mostly LayerNorm/attention), and this drift does not necessarily cause catastrophic forgetting. ES also needs smaller populations as model scale grows.

## Method

- **One-point ES estimator** (Salimans et al. 2017). Sample $N$ Gaussian perturbations $\epsilon_i \sim \mathcal{N}(0,I)$, roll out each perturbed policy $\theta + \sigma\epsilon_i$ on a reasoning prompt, score with scalar verifier reward $R_i$, z-score-standardize within the population to $z_i$, then update the center model:
$$\theta^+ = \theta + \alpha \cdot \frac{1}{N}\sum_i z_i \epsilon_i \quad \text{(Eq. 7)}$$
  ($\alpha$ absorbs the $1/\sigma$ factor.) ES treats the population of perturbed-parameter rollouts as a zeroth-order gradient estimator of the Gaussian-smoothed objective $F_\sigma(\theta) = \mathbb{E}_\epsilon[F(\theta+\sigma\epsilon)]$ (Eq. 6-7), where $F(\theta) = \mathbb{E}_{x,y}[r(x,y)]$ is the same verifier-reward objective GRPO optimizes (Eq. 2).
- **Mechanism contrast (Table 1).** ES's signal path is $R_i \to z_i \to \theta$ via perturbed-policy rollouts with no backprop and no retained backward state. GRPO's is $r_i \to \hat A_i \to \theta$ via retained-backprop policy rollouts (clipped-surrogate group-relative policy gradient, Eq. 3-4). ES is on-policy in that perturbed policies are always centered on the current $\theta$, but it is not in the REINFORCE/PPO/GRPO policy-gradient family — exploration is parameter-space (perturbation radius $\sigma$), not token-space sampling temperature. Too small $\sigma$ overfits to observed rewards; too large destabilizes/collapses training (Section 5.1).
- **Reward normalization.** Z-score standardization within each population (analogous to GRPO's group normalization) raises mean training reward over unnormalized ES (Fig. 1c item 1).
- **One-point vs two-point (antithetic) estimation.** Two-point ZO — standard in non-reasoning zeroth-order SFT (Malladi et al. 2023, MeZO on SST-2) — gives no training-reward or held-out advantage over one-point estimation for reasoning tasks (Section 5.2): paired covariance from two symmetric perturbations is weakened when responses are autoregressively regenerated (diverging at early tokens) rather than reusing fixed supervised data.
- **Sequential composition.** ES→GRPO and GRPO→ES: same total update budget, split into two stages, proposed to combine GRPO's Pass@1 strength with ES's Pass@K gains.

## Claims

**Theoretical (Section 3.1, the ES-diversity-to-Pass@K chain):**

- **Lemma 1** (Eq. 8-9, Fisher-information diversity): population perturbations induce policy diversity —
$$\mathbb{E}[\mathrm{JS}^{pol}_N(x)] = \frac{\sigma^2}{2}\left(1-\frac1N\right)\mathrm{tr}\, I_x(\theta) + O(\sigma^4)$$
- **Lemma 2** (Eq. 10-11): population sampling is at least as likely to find a correct answer as matched single-policy sampling, $P_N^{pop}(x) \geq P_N^{same}(x)$.
- **Lemma 3** (reward-weighting): reward-weighted mixture success exceeds the population average by a covariance term, $p_w(x) - \bar p(x) = N\,\mathrm{Cov}_i(w_i, p_i(x))$.
- **Proposition 1** (Eq. 12-14): sufficient conditions for the ES-updated center to have higher Pass@K than the pre-update policy, requiring a center-transfer-error bound $\varepsilon_{succ}$ and comparator margin $m_K > K\sqrt{\varepsilon_{succ}/2}$.

**Empirical (Tables 2-3, Easy Setting = GSM8K/2 epochs on Qwen2.5-1.5B, Llama-3.2-3B, Qwen2.5-7B-Instruct; Hard Setting = DeepScaleR/1 epoch on DeepSeek-R1-Distill-Qwen-1.5B):**

- ES improves average Pass@1 over base in all four settings; GRPO gets larger average Pass@1 gains. Representative Pass@1/16/32 (×100):
  - Qwen2.5-1.5B: Base 41.0/75.4/80.2 → GRPO 42.9/75.1/79.9 → ES 41.5/**76.0**/**80.9**
  - DeepSeek-R1-Distill-Qwen-1.5B (math avg): Base 47.7/73.5/77.4 → GRPO **52.9**/74.7/78.0 → ES 49.9/75.0/78.9
- GRPO falls below base on both Pass@16 and Pass@32 in 15 of 18 Easy-Setting task/model comparisons. ES exceeds base on average Pass@16/32 in every setting tested.
- The two sequential compositions add non-dominated points to the Pass@1-Pass@K Pareto front in all three representative settings tested (Fig. 3) — e.g. ES→GRPO attains the highest Pass@32 on the Hard-Setting math average while retaining most of GRPO's Pass@1 gain.
- Not universal: on the Hard-Setting held-out non-math benchmarks (Table 5), ES's Pass@32 average (89.3) is essentially flat/slightly below base (89.6); GRPO (89.0) is also below base.
- Entropy trajectories (Fig. 2a-b): GRPO entropy declines substantially and finishes with Pass@16/32 below base; ES entropy stays modest and finishes above base on both. Local entropy-collapse relation (Cui et al. 2025, Eq. 5): $\Delta H(s) \approx -\eta_{PG}\,\mathrm{Cov}(\log p_a, p_a A_a)$.

**Parameter drift and functional sparsity (Section 4, RQ2):**

- ES drifts **40.7-44.1×** farther from init than GRPO in relative $L_2$ norm (Table 4).
- At threshold $\tau = 1.5\times10^{-3}$, 77.6-93.0% of nonzero coordinate changes fall within $(0,\tau]$ and can be zeroed with little Pass@1 loss (Fig. 4) — leaving **7.0-22.4%** "larger-magnitude" coordinates that carry the task-performance gain. Framed as an "approximately performance-preserving coordinate subspace," explicitly analogized to the Lottery Ticket Hypothesis (Frankle & Carbin 2018).
- The largest ES updates concentrate in LayerNorm weights and attention projections — e.g. Llama-3.2-3B: 5/9 max-magnitude coordinates are input-LayerNorm weights; DeepSeek-R1-Distill-Qwen-1.5B: 117/144 max coordinates are LayerNorm, 24 attention-projection biases. GRPO's largest updates instead concentrate in token embeddings and the LM head, 48-16× smaller in magnitude — a structural claim about *where* verifier-reward-driven adaptation lives that differs by optimizer class.

**Population size vs. scale (Section 5.1):** the population size $N$ needed to match an $N=64$ reference shrinks as base model scale grows — only $N=32$ is within 0.01 of the $N=64$ reward for Qwen2.5-0.5B-Instruct at update 300, but $N=16$ already suffices for 1.5B and 3B (the $N{=}16$-to-$N{=}64$ reward gap falls from 0.0352 at 0.5B to 0.0051 at 1.5B to 0.0030 at 3B).

## Sample efficiency

Not a low-data/single-sample method — this is full-dataset post-training RL (2 epochs GSM8K ≈7.5K problems, or 1 epoch DeepScaleR). The relevant efficiency axis is population size $N$, not example count (see population-vs-scale finding above). No claims about training-example count are made. The paper frames ES as "better exploiting the reasoning capabilities of pretrained LLMs" — surfacing latent solution diversity already present in the base model via population-based parameter-space exploration, not installing new reasoning skill.

## Relevance to the project

This is the wiki's **first Evolution-Strategies entry** — no `research/evolution-strategies/` (or similar) theme directory exists yet. Home it here under `rlvr-mechanics/` for now, since its content is mechanistic diagnosis of an RLVR-adjacent paradigm; flag as a candidate for a dedicated ES theme once a second ES-for-LLM-reasoning source is ingested (candidates cited in this paper's Introduction: Qiu et al. 2026, Sarkar et al. 2026, Zheng et al. 2026a).

The functional-sparsity result (7.0-22.4% of nonzero coordinates carry the gain, concentrated in LayerNorm/attention) is a second, differently-measured data point for [[rl-sparse-subnetwork]]'s claim that RL fine-tuning touches a small, structured subnetwork — now extended to a non-gradient-based optimizer and localized to specific components rather than GRPO's embedding/LM-head concentration.

**Live dispute with Abdi et al. 2026** (ACL Short, "Evolutionary strategies at scale lead to catastrophic forgetting," not yet in wiki): Abdi et al. report catastrophic forgetting under ES using a single model/training-task/held-out-benchmark and a small training set. This paper's authors argue that result is confounded with training-set overfitting rather than genuine capability loss — but concede (citing Hoy et al. 2026, "Matching accuracy, different geometry: ES vs GRPO in LLM post-training," also not yet in wiki) that ES's effect on prior capabilities "may depend on the task and training configuration," leaving open whether ES preserves capabilities *consistently* across tasks and repeated updates in continual-learning-style deployment. Good `/research` follow-up target.

## Limitations

- GRPO still wins on average Pass@1 in every setting tested — ES is not dominant, only Pareto-better at higher K; the sequential compositions are a practical reconciliation, not a proof that ES strictly subsumes GRPO.
- The base-model-exceeding Pass@K gain is not universal: Hard-Setting held-out non-math benchmarks show ES's Pass@32 average essentially flat/slightly below base (89.3 vs 89.6).
- Lemma 3 and Proposition 1 are explicitly framed as sufficient conditions, not universal guarantees — Proposition 1's margin requirement $m_K > K\sqrt{\varepsilon_{succ}/2}$ may not hold in practice.
- No discussion of ES's rollout/compute cost relative to GRPO (population size $N$ rollouts per step vs. group size $G$ rollouts), despite ES being pitched partly on memory efficiency — wall-clock/rollout-budget parity with GRPO is not analyzed.
- The Abdi et al. 2026 dispute is unresolved by this paper's own admission; whether ES avoids catastrophic forgetting consistently, or only in the specific settings tested here, is an open question.

## Source

- `raw/research/weekly-2026-08-28/03-es-broader-reasoning-coverage-grpo.md`
- arXiv: https://arxiv.org/abs/2608.27351

## Related

- [[deepseekmath-grpo]] — explicit empirical and mechanistic baseline throughout (Table 1 mechanism comparison, Tables 2-3 head-to-head results)
- [[rl-sparse-subnetwork]] — parallel functional-sparsity finding: RL updates concentrate in a small coordinate subset, here extended to a non-gradient-based optimizer
- [[../catastrophic-forgetting/_overview]] — parallel "large parameter drift need not imply widespread functional change" claim; live disagreement with Abdi et al. 2026 over whether ES causes catastrophic forgetting
- [[../rl-optimizers/vpo]] — alternate Pass@K-coverage mechanism (Dirichlet-sampled vector-reward scalarization within GRPO, accepting a Pass@1 tradeoff by design) worth comparing against ES's claim of gaining Pass@K without sacrificing Pass@1
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — this paper's Table 2/3 ES-exceeds-base-Pass@16/32 result is flagged there as a method-class scope challenge to Theorem C.1
- [[../self-play/yue-rlvr-boundary]] — motivating citation: Yue et al.'s finding that GRPO reduces Pass@K relative to the base model is the puzzle this paper frames itself as addressing
- [[../../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep
