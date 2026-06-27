# Spurious Rewards: Rethinking Training Signals in RLVR

GRPO training with random or negatively-correlated rewards — signals with little, no, or even negative correlation to correct answers — still yields +21.4 pp on MATH-500 for Qwen2.5-Math-7B, recovering ~73.5% of the +29.1 pp gain from ground-truth rewards. The mechanism is not reward learning: GRPO's PPO clip term has a clipping bias that amplifies high-prior behaviors already embedded in the base model's pretrained distribution, regardless of reward label semantics. A significant fraction of reported Qwen-family RLVR gains may therefore reflect pretrained-behavior amplification, not policy improvement from reward signal. Effect is strongly model-family-dependent (Llama3, OLMo2: no spurious-reward gain). See [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] (**Position D**) for how this result interacts with the full RLVR mechanism debate.

## Method

Three reward conditions applied under standard GRPO training on Qwen2.5-Math-7B:
1. **Ground-truth verifiable rewards** — correct-answer check; standard RLVR setup.
2. **Randomly assigned rewards** — no correlation to correctness; reward label is noise.
3. **Negatively-correlated rewards** — deliberately misassigned; penalizes correct answers.

Same training protocol across conditions; evaluated on MATH-500. Cross-model validation on Qwen2.5-Math-7B, Llama3, and OLMo2 under identical training to isolate the model-family dependency.

**Proposed mechanism — GRPO clipping bias:** The PPO surrogate's clip term asymmetrically amplifies responses with high prior probability under the base model. When a behavior is already frequent in the pretrained distribution, the clip term pushes it further regardless of whether the reward label endorses it. This is a trajectory-level effect, not token-level. Case study: "code reasoning" (reasoning expressed in code syntax without actual code execution) is a high-prior behavior in Qwen2.5-Math models; its frequency rises from 65% to >90% under spurious rewards — consistent with clip-bias amplification, not reward-directed learning.

## Results

| Condition | MATH-500 gain (Qwen2.5-Math-7B) |
|---|---|
| Ground-truth rewards | +29.1 pp |
| Random rewards | +21.4 pp (~73.5% of real-reward gain) |
| Negatively-correlated rewards | positive gain |
| Llama3 / OLMo2 under random rewards | no gain |

Code-reasoning frequency: 65% → >90% under spurious rewards on Qwen2.5-Math.

## Novelty

Prior RLVR work assumed the semantic correctness of the reward signal was load-bearing — benchmark improvement reflects what the model learned from reward feedback. This paper is the first systematic ablation replacing reward correctness with random assignment while showing the majority of the benchmark gain persists. It identifies GRPO's clip term as a previously uncharacterized confound: clipping bias can amplify pretrained behaviors independently of reward label quality. This establishes "spurious-reward ablation across model families" as a required validation step for any RLVR claim on Qwen-family models.

## Alternative Mechanisms Proposed

The paper proposes that gains come from **clip-bias amplification of pretrained high-prior behaviors** rather than from learning the reward signal. The mechanism is trajectory-level: high-prior behaviors that appear frequently in the base model get pushed further by the clip term when they surface in high-reward-group trajectories — even when reward assignment is random. The paper does not propose a replacement training method; it identifies a confound in existing evaluation practice.

[[rlvr-incentivizes-reasoning]] (Position E) offers a complementary partial explanation: MATH-500 Pass@K is confounded because base models can guess correct short-integer answers with incorrect CoTs, inflating apparent benchmark gains from any training signal, including spurious ones. The two explanations are not mutually exclusive and may co-contribute to the observed spurious-reward effect.

## Applicability

Not a training method to adopt. A methodological critique and diagnostic tool:

- **Spurious-reward ablation across model families is now a required validation step** for any RLVR claim on Qwen-family models. A gain that does not survive a spurious-reward control cannot be attributed to reward-signal learning.
- **Model-family dependency scopes the claim.** The effect requires a base model with amplifiable high-prior behaviors (Qwen2.5-Math has them; Llama3/OLMo2 do not). Position D does not negate RLVR in general — it applies selectively to results from model families where the clipping-bias confound can operate.
- For model families without spurious-reward gain, Positions A/B/C in the [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] debate may still hold unaffected.

## Reproducibility

- **arXiv:** 2506.10947
- **Code:** not linked in captured abstract
- **Venue:** preprint (v1 submitted June 2025; v2 revised February 2026)
- **Authors:** Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du, Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei Koh, Luke Zettlemoyer (UW / AI2)

## Source

`raw/research/weekly-2026-06-27/03-spurious-rewards-rlvr.md` (arXiv:2506.10947)

## Related

- [[high-entropy-tokens-rlvr]] — already flags spurious-rewards as a "fourth competing account" of RLVR gains; entropy-masking result assumes genuine reward signal, which this paper challenges at scale
- [[token-gradient-cancellation]] — Position B's gradient-cancellation mechanism is undermined if reward semantics are irrelevant to benchmark gains; complementary failure-mode framing
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — this paper is **Position D** in this ongoing conflict; clipping-bias amplification is the foundational source for that position
- [[rlvr-incentivizes-reasoning]] — **Position E** partially reconciles via metric-invalidity argument (MATH-500 guessable short answers); complementary to but not a full resolution of Position D
- [[reasonmaxxer]] — **Position A**; spurious-reward result contradicts the premise that RL selects semantically meaningful sparse corrections at high-entropy positions
