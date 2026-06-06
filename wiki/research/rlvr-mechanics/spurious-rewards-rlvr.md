# Spurious Rewards: Rethinking Training Signals in RLVR

Shao et al. (arXiv:2506.10947, UW / Allen AI / DeepMind, Jun 2025 / Feb 2026 v2). RLVR with GRPO can yield large benchmark gains on certain models even when the reward signal is random, anti-correlated, or zero. On Qwen2.5-Math-7B / MATH-500, random rewards deliver a +21.4 pp gain vs +29.1 pp from ground-truth rewards — 73% of the ground-truth effect for free. The mechanism is a **clipping bias** in GRPO's PPO clip term that amplifies high-prior behaviours latent in pretraining regardless of reward informativeness. The effect is highly model-dependent: spurious rewards fail to produce gains on Llama3 and OLMo2. The paper identifies **code reasoning** (CoT in code syntax without actual execution) as the specific amplifiable behaviour in Qwen2.5-Math models, and shows its frequency increases from 65% to >90% under spurious reward training. The primary methodological implication is that evaluating RLVR methods on a single model family (i.e., Qwen) can yield misleadingly optimistic conclusions about algorithm quality.

## Finding

**Clipping bias amplifies high-prior behaviours.** GRPO's clip term is:

$$\min\!\left(\rho_{i,t}\hat{A}_{i,t},\;\text{clip}(\rho_{i,t}, 1-\varepsilon, 1+\varepsilon)\hat{A}_{i,t}\right)$$

where $\rho_{i,t} = \pi_\theta / \pi_{\theta_\text{old}}$. When a behaviour has high base-model probability, $\rho_{i,t}$ starts near 1 and the clip is loose; the policy can freely increase probability for that behaviour. For behaviours with low base probability, the clip is tight and updates are suppressed regardless of reward signal. This creates an asymmetry: **high-prior behaviours receive unconstrained gradient even under uninformative rewards**, while low-prior behaviours are blocked even under correct rewards.

**Spurious reward taxonomy.** The paper tests three regimes:

| Reward type | Description | MATH-500 gain (Qwen2.5-Math-7B) |
|---|---|---|
| Ground-truth | Correct/incorrect verifiable check | +29.1 pp |
| Random | Bernoulli(0.5), independent of correctness | +21.4 pp |
| Anti-correlated | Correct → 0, Incorrect → 1 | significant positive gain (exact figure not in abstract) |
| Zero constant | All outputs receive same reward | gain present |

**Code reasoning as the amplified behaviour.** Qwen2.5-Math models have a strong pretraining prior toward code-format reasoning (65% baseline frequency). Under spurious GRPO training this increases to >90% — not because the reward selected for it, but because the clip bias allows the existing high-probability pathway to grow unchecked. Code reasoning correlates with MATH-500 accuracy, so amplifying it lifts benchmark scores even without informative reward.

**Model-dependence.** Llama3 and OLMo2 do not exhibit the same gains under spurious rewards. These models either lack an analogous high-prior amplifiable behaviour, or their base priors are differently shaped. The Qwen2.5-Math architecture and pretraining regime (code-heavy, math-specialised) appear to create a specific "exploit" that GRPO's clip bias can latch onto.

## Results

- Qwen2.5-Math-7B / MATH-500: random rewards +21.4 pp; ground-truth rewards +29.1 pp.
- Code-reasoning frequency: 65% (base) → >90% (after spurious GRPO training).
- Llama3, OLMo2: spurious rewards yield no comparable gain.
- The finding holds across multiple spurious reward constructions (random, anti-correlated, constant zero).

## Connections to the wiki

**Relationship to the RL-as-selection cluster.** This paper adds a distinct mechanism to the cluster in [[_overview]]. Akgul ([[rethinking-rl-sparse-selection]]) shows RL reranks within base top-5 (0% shifted); Dymetman ([[binary-rewards-rl-challenges]]) shows forward-KL convergence to $p^*$ with mode collapse under small $\beta$. This paper shows that the GRPO clip term specifically provides an inductive bias toward *base-high-probability* outputs independent of reward correctness — i.e., GRPO's optimiser structure selects what to amplify before the reward can. The three accounts are complementary:

| Account | Mechanism | Failure mode |
|---|---|---|
| Akgul (token-level) | RL reranks within top-5 | Can't install genuinely new tokens |
| Dymetman (info-geometry) | KL-RLVR → I-projection $p^*$; small $\beta$ → near-Dirac | Mode collapse under misspec |
| This paper (clip-bias) | Clip asymmetry amplifies high-prior behaviours regardless of reward | Benchmark gaming via spurious amplification |

**GRPO clip term as double-edged primitive.** [[deepseekmath-grpo]] presents the clip as a conservative policy constraint. This paper reframes it as a **prior-amplification mechanism** when combined with group-relative advantage normalisation at small group variance. The clip is not neutral — it actively selects which behaviours can grow.

**Implications for single-sample RLVR.** In the single-sample regime ($G$ rollouts from one training prompt), the group advantage distribution is narrow and the clip is frequently binding. Any high-probability behaviour in the base model's prior on that prompt will be clip-free and able to grow — regardless of whether it reflects the concept targeted by the training example. This is a direct threat to concept-targeted single-sample training.

**Relation to code reasoning / Qwen pretraining.** The specific amplified behaviour is domain-contingent. For math reasoning on Qwen2.5-Math, code formatting is the "exploit"; for other tasks or model families there may be different high-prior shortcuts. This limits the generality of any single-model RLVR benchmark result.

## Conflicts

- **Partial tension with DAPO / Dr. GRPO motivation.** DAPO removes the KL penalty (addressing Dymetman's mode-collapse worry) but retains the PPO clip. This paper's clipping-bias finding suggests DAPO's Clip-Higher asymmetry may still be susceptible to spurious amplification — the clip's directional bias favours promoting already-high-prior tokens. Not a direct contradiction; the papers address different pathologies, but both now motivate scrutinising Qwen-only evaluations of RLVR variants.

## Source

- `raw/research/weekly-2026-06-05/05-spurious-rewards-rlvr.md`

## Related

- [[deepseekmath-grpo]] — GRPO clip objective and group-relative advantage; clip term analysed here
- [[binary-rewards-rl-challenges]] — Dymetman's information-geometric mode collapse; complementary failure-mode account
- [[rethinking-rl-sparse-selection]] — Akgul's token-level 0%-shifted finding; same cluster, different mechanism
- [[_overview]] — RLVR mechanics overview; this paper extends the RL-as-selection cluster
- [[../self-play/invisible-leash]] — support-inclusion theorem; clip bias provides a complementary inductive-bias account within that support
- [[../single-sample-rl-finetuning/_overview]] — clip-bias amplification of high-prior behaviours is a direct threat to single-sample concept targeting
- [[../weekly-briefs/2026-06-05]] — brought in by the 2026-06-05 weekly sweep
