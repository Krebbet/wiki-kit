# RLSC: Self-Confidence as Reward for Few-Shot RL Fine-Tuning

RLSC (Reinforcement Learning via Self-Confidence) demonstrates that a model's own output-distribution confidence — not any external verifier or label — is sufficient reward signal to achieve large math-reasoning gains with only 16 samples per question and 10–20 training steps. It is the lowest-label-count RL post-training result in this wiki and the closest existing prior art to the single-sample RL thesis.

## Method

**Mode-sharpening objective.** RLSC maximises the probability that two i.i.d. samples agree:

$$F(p_\theta) = \mathbb{E}_{y_1, y_2 \sim p_\theta(y|x)}[\mathbb{I}(y_1 = y_2)] = \sum_y p_\theta(y|x)^2$$

Equivalently, this is the self-confidence functional $F(p_\theta) = \mathbb{E}_{y \sim p_\theta}[p_\theta(y|x)]$, maximised when $p_\theta$ collapses to a delta on the mode.

**Training loss.** Using a frozen old model $p_\text{old}$ for sampling and weighting:

$$L_1 = -\sum_y p_\text{old}(y|x) \cdot \log p_\theta(y|x)$$

Smoothed variant for stability ($\alpha = 0.1$):

$$L_2 = -\sum_y (p_\text{old}(y|x) + \alpha) \cdot \log p_\theta(y|x)$$

$L_1$ is formally identical to the RLHF loss with $p_\text{old}$ playing the role of reward — RLSC lives in the same unified loss family as Shannon entropy and completion-reward objectives (Table 1 of paper).

**Algorithm 1 (from paper):**
```python
for question in dataset:
    completions = model.generate(question, temperature, num_samples)
    logits = model.forward(question.repeat() + completions)[question.length:-1]
    all_log_probs = log_softmax(logits / temperature)
    log_p = all_log_probs.gather(token_ids).sum
    loss = -(exp(log_p).detach() + alpha) * log_p
    loss.backward()
    optimizer.step()
```

**Setup:** Qwen2.5-Math-7B; 16 completions per question at temperature 0.5; 10 or 20 gradient steps on AIME2024 training split.

## Results

On Qwen2.5-Math-7B vs. base (Table 2):

| Benchmark | Base | RLSC | Δ |
|-----------|------|------|---|
| AIME24 | 13.3% | 26.7% | +13.4 pp |
| MATH500 | 51.4% | 72.6% | +21.2 pp |
| AMC23 | 45.0% | 54.7% | +9.7 pp |
| Olympiadbench | 15.1% | 35.9% | +20.8 pp |
| Minerva Math | 10.7% | 32.4% | +21.7 pp |
| GPQA Diamond | 21.4% | 24.1% | +2.7 pp |

Qwen2.5-Math-1.5B shows similar patterns (MATH500 +26.8 pp; GPQA −3.4 pp, suggesting domain brittleness at small scale).

## Sample efficiency

**16 completions per question, 10–20 gradient steps.** No auxiliary datasets, no instruction tuning, no preference pairs. This is the lowest label-count RL post-training result in the wiki (cf. TTRL at 64 samples/question; CBRL requires demonstration traces).

Relationship to TTRL: RLSC is derived as the principled objective underlying majority voting. TTRL optimises the same mode implicitly via pseudo-labels but requires 64 samples and a label-extraction step. RLSC does neither — the training signal is purely internal.

## Key limitations

**Correctness-agnostic signal.** Mode-sharpening is agnostic to correctness. If the base model's mode is on a wrong answer, RLSC reinforces the wrong answer with higher confidence. There is no mechanism distinguishing "confidently right" from "confidently wrong." This is a fundamental misspecification risk analogous to Dymetman's I-projection collapse ([[research/rlvr-mechanics/binary-rewards-rl-challenges]]).

**Distribution collapse.** Only 10–20 training steps reported; behaviour under longer training (mode collapse, diversity loss) is unknown. Response length reduction is observed but not quantified.

**Domain specificity.** Evaluated only on math benchmarks with a strong math specialist (Qwen2.5-Math). Generalization to weaker base models or non-math domains untested.

**Benchmark contamination.** AIME2024 training split is also a test benchmark variant; train/test contamination risk is worth flagging when citing the +13.4 pp AIME24 result as evidence of generalisation.

## Key figures

- **Figure 1a/b:** RLSC workflow; probability distribution sharpening before vs. after training
- **Equation 1:** $F(p_\theta) = \sum_y p_\theta(y|x)^2$ (agreement probability / self-confidence functional)
- **Equations 5–6:** $L_1$ and $L_2$ training losses
- **Table 1:** Unified loss family (RLHF / Shannon Entropy / Completion rewards / RLSC)
- **Algorithm 1:** Full training pseudocode

## Source

- `raw/research/weekly-2026-06-26/01-rlsc-confidence-fewshot-rl.md` (arXiv:2506.06395)

## Related

- [[research/single-sample-rl-finetuning/_overview]] — lowest-label-count RL post-training in the theme
- [[research/test-time-training/_overview]] — TTRL is RLSC's direct predecessor; RLSC reframes majority-vote pseudo-labels as mode-sharpening
- [[research/rlvr-mechanics/binary-rewards-rl-challenges]] — Dymetman's misspecification risk applies directly: wrong-mode amplification is RLSC's primary failure mode
- [[research/rlvr-mechanics/spurious-rewards-rlvr]] — Shao et al. show Qwen2.5-Math-7B responds to random rewards; RLSC's gains on the same model family raise the same question about baseline distributional amplification
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — Wang et al.'s entropy-gated gradient restriction: RLSC's per-token $p_\text{old}$ weighting implicitly downweights high-entropy tokens, potentially inverting the effective gradient mask; potential conflict
- [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] — BOLT also derives a weighted-SFT loss from a principled target; RLSC's $L_1$ has the same cross-entropy form but with self-confidence weights vs. Boltzmann density-ratio weights
- [[research/self-improvement/_overview]] — self-improvement without external labels (closest analogue: STaR, but RLSC does not filter by correctness)
- [[research/weekly-briefs/2026-06-26]] — brought in by the 2026-06-26 weekly sweep
