# Binary Rewards and Reinforcement Learning: Fundamental Challenges

Dymetman (arXiv:2605.02375, May 2026). Information-geometric account of why binary RLVR produces diversity collapse. The filtered model $p^* = a(\cdot | \mathcal{Y}_1)$ — base model conditioned on validity — is the unique I-projection of the base $a$ onto the valid set; KL-controlled RL converges to $p^*$ in **forward KL** as $\beta \to 0$ (Theorem 3.1a–c). Critical asymmetry: $\text{KL}(p^\beta \| p^*) = \infty$ for all finite $\beta$ (Theorem 3.1d), so $p^*$ can never serve as a direct reverse-KL target. Under model misspecification, small $\beta$ amplifies the validity term (Eq. 10) and drives the optimiser toward parametrically easy near-Dirac policies; $p^*$ is provably unreachable. Provides the formal substrate for [[../self-play/yue-rlvr-boundary|Yue's RLVR boundary]] and the pass@k-vs-pass@1 split.

## Source

- `raw/research/weekly-2026-05-10/03-binary-rewards-rl-challenges.md`

## Theory

**Setup.** Binary reward $v(y) = \log r(y)$ over base model $a$. KL-controlled objective:

$$\max_q \mathbb{E}_q[v] - \beta \cdot \text{KL}(q \| a) \quad \Rightarrow \quad p^\beta(y) \propto a(y) \exp(v(y)/\beta) \quad \text{(Gibbs/Boltzmann)}$$

**Filtered model.** $p^*(y) = a(y) \cdot \mathbb{1}[y \in \mathcal{Y}_1] / a(\mathcal{Y}_1)$ — base reweighted onto valid set. Proposition 2.3: $p^*$ is the **I-projection** of $a$ onto the valid simplex.

**Theorem 3.1 — four convergence modes.** As $\beta \to 0$:
- (a) $p^\beta \to p^*$ pointwise on $\mathcal{Y}_1$
- (b) $p^\beta \to p^*$ in total variation
- (c) $\text{KL}(p^* \| p^\beta) \to 0$ (forward KL toward $p^*$)
- (d) $\text{KL}(p^\beta \| p^*) = +\infty$ for every $\beta > 0$ (**reverse KL never well-defined**)

**The asymmetry matters.** Most LM-RL objectives use *reverse* KL implicitly (sampling from $q$, not $p^*$). The paper shows reverse KL $q \to p^*$ is structurally impossible.

**Misspecification + small $\beta$ → mode collapse (Eq. 10).**

$$\log p^\beta(y) = \log a(y) + \frac{1}{\beta}\left[v(y) - \log \mathbb{E}_a[\exp(v/\beta)]\right]$$

Small $\beta$ amplifies validity advantage. If $\Pi_\Theta$ is misspecified relative to $p^*$, the cheapest validity-rich approximation is a near-Dirac on a single high-probability valid sequence — not coverage of $\mathcal{Y}_1$. Bigram toy: at $\lambda = 10$ ($\beta$ small), 97% mass on one sequence vs $p^*$ entropy $\approx 2.0$.

**Eq. 8 — $\beta \leftrightarrow \mu$ translation.** The Bernoulli divergence $\kappa(\mu) = \mu \log(\mu/A_1) + (1-\mu)\log((1-\mu)/A_0)$ controls how validity-pressure $\mu$ maps to penalty $\beta$. Reframing in terms of $\mu$ (target validity fraction) cleanly separates signal strength from base-model strength — relevant to [[../rl-optimizers/maspo|MASPO's Signal Reliability axis]].

**Proposed fix.** Forward-KL or $\alpha$-divergence objectives targeting $p^*$ directly (Kruszewski et al. ICLR 2026 $\alpha$-DPG; Li et al. arXiv:2509.07430). Cost: requires sampling from $p^*$ or a good approximation.

## Connections to the wiki

- **[[../self-play/yue-rlvr-boundary]]** — Yue empirically shows pass@k degrades while pass@1 improves under RLVR. Theorem 3.1d + Eq. 10 give the formal mechanism: reverse-KL toward $p^*$ is undefined, and small $\beta$ + misspecification drives mode-concentration.
- **[[../self-play/invisible-leash]]** — Theorem C.1 says $\text{supp}(\pi_\theta) \subseteq \text{supp}(a)$ pointwise; this paper goes further: even **within** that support, reverse KL drives concentration onto a near-Dirac. The collapse story is sharper than the leash story.
- **[[deepseekmath-grpo]]** — GRPO's KL-controlled objective is exactly Eq. (1). The paper provides the structural account of what GRPO is converging to (and why pass@k drops).
- **[[../rl-optimizers/dapo]]** — DAPO drops the KL penalty entirely. Dymetman argues this **worsens** mode collapse (no mechanism selects $p^*$ over a Dirac). Empirical tension: DAPO reports stability gains and pass@1 wins; Dymetman highlights pass@k damage. See [[#Conflicts]].
- **[[../rl-optimizers/maspo]]** — MASPO's Signal Reliability axis maps onto the $\mu$ reframing of Eq. 8.
- **[[../rl-optimizers/tsallis-loss-continuum]]** — Tsallis $\mathcal{J}_Q$ recovers a continuum of estimators; Dymetman's account is binary-reward-specific but complementary at the un-regularised end ($q=0$).
- **[[../single-sample-rl-finetuning/_overview]]** — single-sample RLVR risks collapsing to near-Dirac on a single valid path rather than covering $\mathcal{Y}_1$ — exactly the failure Eq. 10 predicts.
- **[[../../conflicts/invisible-leash-vs-spiral-transfer]]** — formal backing for the collapse side. With this paper, Position A has a sharp theoretical foundation in addition to Yue's empirical evidence.

## Conflicts

- **vs. DAPO** (KL-dropping). DAPO improves stability and pass@1 by removing KL; Dymetman predicts this worsens pass@k via mode-collapse on a near-Dirac. Not a direct empirical contradiction: DAPO measures pass@1, Dymetman addresses coverage. Tracked as tension in the [[../rl-optimizers/dapo|DAPO page]].

## Related

- [[../self-play/yue-rlvr-boundary]] — empirical foundation
- [[../self-play/invisible-leash]] — support-inclusion theorem
- [[../self-play/two-stage-dynamic]] — two-stage warm-start aligns with Remark 4.1
- [[deepseekmath-grpo]]
- [[rethinking-rl-sparse-selection]] — token-level mechanistic complement (this week)
- [[../rl-optimizers/dapo]]
- [[../rl-optimizers/dr-grpo]]
- [[../rl-optimizers/maspo]]
- [[../rl-optimizers/tsallis-loss-continuum]]
- [[../single-sample-rl-finetuning/_overview]]
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — formal backing for Position A
- [[../../weekly-briefs/2026-05-10]] — brought in by the 2026-05-10 weekly sweep
