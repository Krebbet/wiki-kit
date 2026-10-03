# Random-Reward RL as a Probe of LLM Reachability

arXiv:2610.01066 (Mao, Yu, Zhu, Zheng, Li, Shi, Yin, Wang, Niu; submitted 2026-10-01). Reframes the spurious-reward paradox ([[spurious-rewards-rlvr]]) as a measurement of **reachability**: what further training can attain from a checkpoint under specified constraints, beyond current accuracy. Two OLMo checkpoints at identical 3.5% synthetic-arithmetic accuracy reach 8.5% vs 55% in their best correctness-rewarded RL runs. Across OLMo pre-/mid-training checkpoints, three regimes: early, RL barely helps even with correct rewards; later in pre-training, correct rewards work and random rewards stay weak; entering midtraining, even random rewards give large gains. A number-masked SFT analysis shows the same ordering, so it is not an RL-mechanism artifact.

## Source

- `raw/research/weekly-2026-10-02/04-random-reward-reachability-probe.md` (arXiv abs-page capture; abstract only)

## Claims

| Regime | Correct reward | Random reward |
|---|---|---|
| Early pre-training | little gain | little gain |
| Late pre-training | effective | weak |
| Midtraining onward | effective | large gains |

- Spurious-reward gains are neither (only) a GRPO clipping-bias artifact nor (only) contamination: they indicate latent capability the model can reach without correctness information. The random-reward result thus complements the clip-bias account in [[spurious-rewards-rlvr]] rather than replacing it; both can hold (clip bias amplifies, reachability determines whether there is anything to amplify). This matches the model-prior dependence invoked in [[../../conflicts/revisql-vs-spurious-rewards-noise-robustness]].
- Random-reward RL as a probe avoids the label-leakage problem of decodability probes: it supplies no information about which answers are right, so success is attributable to the model.
- Equal accuracy does not imply equal trainability; evaluation snapshots miss it.

Relevance: reachability is the operative quantity for single-sample RL finetuning ([[../single-sample-rl-finetuning/_overview]]): whether one example can unlock a skill depends on the base model's reachability, consistent with the "RL selects, does not teach" accounts in [[rethinking-rl-sparse-selection]] and [[rlvr-pattern-selection-theory]]. Cheap diagnostic idea: run random-reward RL on a candidate base to estimate headroom before investing in curated data.

Caveat: abstract only; OLMo-only, synthetic arithmetic as primary task, so the Qwen-specific spurious-reward results are not directly explained.

## Related

- [[spurious-rewards-rlvr]] — the paradox being probed
- [[rlvr-pattern-selection-theory]] — selection-not-learning account
- [[rethinking-rl-sparse-selection]] — sparse selection view
- [[context-grounding-mechanism-reuse]] — mechanism reuse in trained models
- [[_overview]] — rlvr-mechanics theme
- [[../self-play/yue-rlvr-boundary]] — RLVR does not expand the base boundary
- [[../../conflicts/revisql-vs-spurious-rewards-noise-robustness]] — model-prior-dependence reconciliation
- [[../../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
