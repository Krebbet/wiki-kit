# Wrong Votes, Right Gradients: Batch-Level Coherence Account of Majority-Vote Rewards

Wilson, Huang, Huang (arXiv:2610.20898). Analysis paper, no new algorithm. Shows that in GRPO with binary reward, majority-vote (MV) self-labels yield an expected batch update nearly parallel to the gold-label update, because MV errors are incoherent across prompts and cancel in the sum while the correct signal is shared and adds. Error coherence, not error rate, decides whether self-generated labels can replace verification: independent flips up to 30% leave the update direction intact (disattenuated cosine $c_\infty \approx 1.00$-$1.04$), whereas same-rate flips by a shared rule (response length) drive $c_\infty$ to 0.29 at 20% and negative at 31%. The result is per-step and local, tested on short unregularised math runs; it presupposes many diverse prompts and does not cover N=1 training.

## Method

- Setup: GRPO ($B=256$ prompts, $n=16$, binary reward, no KL/entropy, on-policy so ratios $=1$) on Qwen3-4B-Base with DeepScaleR, trained twice from the same init on identical prompts: gold reward vs MV reward $r=\mathbb{1}[a = \text{modal answer}]$. Gradient analysis on 5 models (Qwen3-4B/1.7B-Base, Qwen2.5-7B, Llama-3.2-3B-Instruct, Llama-3.1-8B-Instruct).
- Per-response gradients are count-sketched ($K=2^{16}$, cosines within 0.004 of exact fp32). The batch update is linear in advantages, so any reward can be scored on identical samples by reweighting the sketches.
- Estimator: split prompt groups into halves A/B. $X=\cos(G_{mv}^A, G_{gold}^B)$, $Y=\cos(G_{gold}^A,G_{gold}^B)$ (ceiling), $Z=\cos(G_{mv}^A,G_{mv}^B)$. Spearman-style disattenuation $c_\infty = X/\sqrt{YZ}$ estimates the cosine between the *expected* updates; reported only when $Z\ge 0.3$.

## Shrinkage / misdirection decomposition

$$G_{mv} = (1-\beta)\,G_{gold} + E_\perp,\qquad E_\perp \perp G_{gold}$$

- $\beta$: shrinkage. Acts like a smaller LR; largely absorbed by Adam normalisation.
- $R_\perp = \|E_\perp\|/\|G_{gold}\|$: misdirection. Only this one changes the direction of progress.
- Corollary 1: independent flips with prob $\varepsilon<1/2$ give expected update $(1-2\varepsilon)G_{gold}$, pure shrinkage ($c_\infty=1$).
- Prop. 1 (growth of a sum of $B$ vectors with per-vector norm $s$, mean pairwise cosine $\bar\rho$): $\|\sum v_i\|^2 = B s^2(1+(B-1)\bar\rho)$. Incoherent vectors grow as $B^{1/2}$, a shared component as $B$; crossover $B^*\approx 1/\bar\rho$ (the McCandlish gradient noise scale for prompt gradients).

## Prop. 2 criterion

$$R_\perp^2 = \varepsilon\,\frac{s_e^2}{s_g^2}\cdot\frac{1+(\varepsilon B-1)\rho_e}{1+(B-1)\rho_g}$$

with $\rho_e,\rho_g$ the pairwise error and gold gradient cosines.
- $\rho_e=0$: $R_\perp\to 0$ once $B\gg 1/\rho_g$, for **any** error rate $\varepsilon$.
- $\rho_e>0$: floor $\varepsilon (s_e/s_g)\sqrt{\rho_e/\rho_g}$ that no batch size removes.
- Measured: MV error mean pairwise cosine is 30-60x below gold's and at the Gaussian-random-reward null; growth exponent 0.5 for error vs 0.58 to 0.87-0.90 for gold; inverting Prop. 1 gives $B^*\approx 50$ (37 from a separate decomposition).
- Headline: MV vs gold cross-half cosine within ~0.02 of the gold-vs-gold ceiling on 4 of 6 arms (e.g. 0.647/0.647 Qwen3-4B pooled; 0.438 vs 0.399 Llama-3.1-8B); $c_\infty$ is 1.00-1.01 within 95% CI on every model. At step 20 of training: $c_\infty=1.000$ [.972, 1.030], MV delivers 98% of the gold component ($\beta=0.020$), rotated 14° from gold.
- A prompt's own gradient is under 1% of the change in its own output at practical $B$ (0.09-0.38% on Qwen3, $B=64$-128). Of 76 first-batch prompts with wrong majority, the MV update still raises expected gold reward on 82%; other prompts contribute +0.075 to the cosine vs +0.007 from the prompt's own mislabeled term.

## Table 3: error structure vs error rate (Qwen3-1.7B-Base)

| Reward / error source | Error rate | $c_\infty$ |
|---|---|---|
| Random flips | up to 30% | 1.00-1.04 |
| Shared-rule flips (response length) | 10% | 0.773 |
| Shared-rule flips (response length) | 20% | 0.287 |
| Shared-rule flips (response length) | 31% | -0.129 |
| Random vote | n/a | 0.961 |
| Self-certainty vote | n/a | 0.975 |
| Length-controlled INTUITOR | n/a | 0.969 (0.76-0.79 on Llama) |
| Reward model GRM-Llama3.2-3B | n/a | 0.982 |
| Pure length reward | n/a | -0.415 |

Same error rate, opposite outcome: structure is the control variable. Rewards that favor a *kind* of response on every prompt (confidence, length, RM style) fall short of gold because that preference is coherent across prompts. MV is the exception among votes because its errors depend on the prompt. Quantifies the misspecification risk of confidence rewards ([[../single-sample-rl-finetuning/rlsc-self-confidence]]).

## Local vs trajectory equivalence (caveat)

Equivalence is per-step on raw gradients, not Adam-preconditioned, not a trajectory statement.
- Gold ends ahead on held-out maj@64: MATH-500 step 20, 0.772 MV vs 0.845 gold; doubling MV batch to 512 does not close the gap.
- Errors are not perfectly orthogonal across steps: $\cos(E_t,E_s)=0.030$ vs 0.001 random reward vs 0.400 gold; cumulative error exponent 0.594 vs random-walk 0.540 ($p=0.005$), so errors accumulate slightly faster than a random walk.
- MV training mostly sharpens: maj@1 +0.237 vs maj@64 +0.026 (gold gains +0.099 on maj@64). Consistent with selection/sharpening ([[rlvr-pattern-selection-theory]]) rather than new capability.
- Held-out repair: MV fixes wrong majorities on MATH-500 level-5 problems (13/66 = 19.7%, ~3x resampling flip rate, breakage 4.4%) through the shared update, since those problems are untrained. maj@1 and maj@4 rise 17-19 points.
- Labels must come from the *current* policy; frozen-base labels are nearly as accurate but deliver far less of the gold update (Appendix C).

## Limitations

- One model trained (Qwen3-4B-Base; Qwen benefits even from spurious rewards, see [[spurious-rewards-rlvr]]), ~20 short unregularised steps, 2 runs per reward.
- Step 10 is an unexplained outlier (ceiling depressed, $c_\infty$ unreportable). MV-run entropy rises sharply after step 15, unanalysed.
- $c_\infty$ analysis excludes all-equal-gold-reward groups (164 of 256 used), sidestepping the zero-advantage tail that matters for hard problems.
- Domain: math with short verifiable answers. Incoherence is expected to fail for shared misconceptions (TruthfulQA-style) and repeated-prompt training.

## Thesis relevance

- The criterion needs $B\gg B^*\approx 37$-50 diverse prompts for cancellation. At N=1 there is no batch to average over: the single prompt's label error is, by construction, fully coherent across the whole update ($\rho_e\approx 1$), so Prop. 2's floor is $\sim\varepsilon\, s_e/s_g$ and the wrong label steers the update directly. Labels for N=1 training therefore must be gold or highly reliable; MV/self-certainty pseudo-labels cannot be justified by this paper.
- Positive side: the shared direction across prompts that carries the gold signal is evidence the update is prompt-general structure rather than per-prompt memorisation ("GRPO improves only behavior that can be expressed as a coherent change to one shared policy"), relevant to concept-targeted transfer.
- Refines the noise-robustness debate: random/spurious-reward robustness ([[spurious-rewards-rlvr]]) and ReViSQL's harm from 32.8% false positives ([[revisql-verified-data-reward-shaping]]) are reconciled if ReViSQL's false positives are coherent (systematic over-acceptance of a query type).

## Source

- `raw/research/weekly-2026-10-16/05-wrong-votes-right-gradients.md` (arXiv:2610.20898)

## Related

- [[spurious-rewards-rlvr]] — clip-bias account of reward-noise robustness; this paper gives the complementary batch-incoherence account
- [[revisql-verified-data-reward-shaping]] — false-positive rewards hurt there; coherence of errors is the predicted reconciler
- [[random-reward-reachability-probe]] — random-reward RL as probe; null-reward gradient geometry here
- [[deepseekmath-grpo]] — GRPO update the decomposition is built on
- [[rlvr-pattern-selection-theory]] — selection/sharpening view consistent with maj@1 vs maj@64 gains
- [[grpo-secretly-prm]] — another gradient-level restructuring of GRPO
- [[rethinking-rl-sparse-selection]] — low-dimensional shared update
- [[../test-time-training/tempo]] — TTRL/MV rewards as baseline; gradient-level justification
- [[../single-sample-rl-finetuning/rlsc-self-confidence]] — self-certainty reward measured at $c_\infty$ 0.975
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — N=1 regime outside this paper's scope
- [[../self-improvement/_overview]] — self-generated-label RL family
- [[../self-play/_overview]] — self-labelling loops relying on MV pseudo-labels
- [[../../conflicts/revisql-vs-spurious-rewards-noise-robustness]] — open conflict this bears on
- [[_overview]] — RLVR mechanics overview
- [[../weekly-briefs/2026-10-16]] — brought in by the 2026-10-16 weekly sweep
