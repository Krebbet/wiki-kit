# Semi-Online DPO: Bridging Offline and Online RL for LLMs

Systematic comparison of offline / semi-online / online DPO and GRPO on verifiable (math) and non-verifiable (instruction-following) tasks, finding that **semi-online DPO with sync interval $s \in \{5, 100\}$ matches fully online DPO and GRPO** while enabling asynchronous, parallelisable generation. The key result: the offline→online gap for DPO is primarily a staleness problem, not an algorithm problem — periodic weight sync of the generator to the current training model recovers nearly all the online benefit.

## Method

**Training regime axis:** sync interval $s$ — the number of gradient update steps between synchronising the generation model to the current training model.
- $s = \infty$: offline DPO (frozen rollout model)
- $s = 1$: fully online DPO/GRPO
- $5 \le s \le 100$: semi-online DPO

**GRPO loss (no length normalisation, purely on-policy):**
$$\mathcal{L}_\text{GRPO} = -\mathbb{E}_{G\sim\pi_{\theta_\text{old}}} \left[\sum_{y^i\in G} \min\!\left(\frac{\pi_\theta}{\pi_{\theta_\text{old}}}A(y^i),\, \text{clip}_\epsilon\!\left(\frac{\pi_\theta}{\pi_{\theta_\text{old}}}\right)A(y^i)\right)\right]$$

Advantage: $A(y^i|x) = r(y^i|x) - \bar{r}_G$. No importance sampling across update steps (sequence-level GRPO advantage breaks the PPO unbiasedness proof).

**DPO loss (standard):**
$$\mathcal{L}_\text{DPO} = -\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_c|x)}{\pi_\text{ref}(y_c|x)} - \beta\log\frac{\pi_\theta(y_r|x)}{\pi_\text{ref}(y_r|x)}\right)$$

**GroupDPO (proposed):** Average DPO loss over all $|Y_c|\times|Y_r|$ correct×incorrect pairs — no gain over single-pair DPO.

**Reference model sync:** For verifiable tasks, syncing $\pi_\text{ref}$ with the generator at each sync step is critical — without it, length collapses (Figure 2). Non-verifiable tasks: no sync needed (hyperparameters too unstable with periodic sync at $s=100$).

**Seed model:** Llama-3.1-8B-Instruct. Infrastructure: fairseq2 (SPMD) + vllm on Ray actors; NCCL weight sync; 32+8 H200 GPUs.

## Results

**Verifiable (Math500 / NuminaMath / AMC23):**

| Method | Math500 | NM | AMC23 |
|--------|---------|-------|-------|
| Seed | 47.4 | 33.9 | 23.7 |
| Offline DPO | 53.7 | 36.4 | 28.8 |
| Semi-online DPO (s=100) | **58.9** | 39.3 | **35.1** |
| Online DPO (s=1) | 58.7 | **39.6** | 32.9 |
| GRPO | 58.1 | 38.8 | 33.6 |

**Non-verifiable (AlpacaEval LC WR / ArenaHard):**

| Method | AE-LC | AH |
|--------|-------|-----|
| Offline DPO | 53.2 | 39.4 |
| Semi-online DPO (s=10) | 81.6 | 61.1 |
| Online DPO (s=1) | **83.1** | **62.8** |
| GRPO | 75.2 | 59.1 |

Online DPO: +56.6% AE-LC WR and +45.6% ArenaHard over offline DPO.

**Key finding:** Semi-online DPO with $s \leq 100$ recovers most online-DPO performance on both task types, with online DPO marginally outperforming GRPO on both.

**Combined verifiable + non-verifiable:** Joint training from seed improves both task types simultaneously (online DPO only, due to compute constraints).

## Stability findings (practical guidance)

- **Adam ε:** Increasing to $10^{-4}$ (vs. default ~$10^{-8}$) reduces DPO divergence significantly.
- **Length normalisation in GRPO:** Found less stable in this work; omitted.
- **Reference model sync (verifiable DPO):** Essential. Without it, bimodal length distribution → reward hacking on short sequences → length collapse (Figures 2, 9).
- **Entropy collapse:** Observed across all online/semi-online regimes on verifiable tasks (Figure 3); immune in offline DPO (frozen rollouts). Entropy regularisation attempts not conclusive; left for future work.
- **GroupDPO + combined GRPO+DPO:** No gain over semi-online DPO alone (Figure 8).

## RL connection

- **Reward signals:** (1) Verifiable: binary from Math-Verify (rule-based correctness). (2) Non-verifiable: scalar from Athene-RM-8B LLM reward model.
- **On/off-policy:** GRPO purely on-policy. DPO spans offline→online via sync interval.
- **KL regularisation:** Both losses use a KL term vs. $\pi_\text{ref}$; $\beta$ values differ by task (verifiable: DPO $\beta=0.1$, GRPO $\beta=0.001$; non-verifiable: $0.01$/$0.001$).

## Key limitations

- Single seed model (Llama-3.1-8B-Instruct); generality across other families unverified.
- Entropy collapse in online verifiable training not solved.
- Reference model sync adds overhead; non-verifiable task hyperparameters too unstable for sync at $s=100$.
- Cross-task transfer weak (training on math degrades instruction-following and vice versa) unless mixing both reward signals from the start.
- GRPO group size ablation: $n=8$ vs. $n=4$ gains ~2.4 pp on Math500; $n=12$ shows no further improvement.

## Source

- `raw/research/weekly-2026-06-26/04-bridging-offline-online-rl.md` (arXiv:2506.21495)

## Related

- [[research/rl-optimizers/dpo]] — extends by making DPO online/semi-online; operationalises the offline→online spectrum
- [[research/rl-optimizers/deepseekmath-grpo]] — GRPO is one of the two primary algorithms; paper restricts to purely on-policy GRPO and notes the sequence-level IS gap
- [[research/rl-optimizers/dr-grpo]] — cited for the length-normalisation bias finding; experimental choice not to use length normalisation grounded here
- [[research/single-sample-rl-finetuning/fest]] — FEST uses semi-online DPO as one of its ingredients; this paper provides empirical grounding for why semi-online ≈ online
- [[research/rlvr-mechanics/_overview]] — regime-vs-reward question; entropy collapse across online methods is additional evidence for RL-as-selection dynamics
- [[research/catastrophic-forgetting/_overview]] — combined verifiable+non-verifiable experiment shows weak cross-task transfer and catastrophic forgetting when finetuning on opposite task type
- [[research/synthesis/fine-tuning-best-practices]] — stability findings (Adam ε, ref model sync, length normalisation, entropy collapse) are directly relevant to the best-practices cookbook
- [[research/weekly-briefs/2026-06-26]] — brought in by the 2026-06-26 weekly sweep
