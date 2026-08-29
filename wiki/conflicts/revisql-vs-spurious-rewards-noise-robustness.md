# ReViSQL vs Spurious Rewards — is RLVR fragile to reward-label noise, or robust to it?

## Positions

**Position A — ReViSQL-K2.6 ([[../research/rlvr-mechanics/revisql-verified-data-reward-shaping]]).** In a text-to-SQL RLVR pipeline, "algorithmic tweaks cannot compensate for [mislabelled data] — cleaning up the data is crucial for RLVR to work well." A pilot run found **32.8% of positive execution-match rewards were false positives** — the query executed to the same result as the gold answer without being semantically correct — and training against this noisy signal measurably "reinforced the wrong query." The team's response was extensive verified-data curation (BIRD-Platinum, expert-checked) plus two reward-shaping fixes (VeriEQL semantic-equivalence downweighting, rule-based knowledge-grounding process reward) specifically to counteract reward-label noise. The clear implication: RLVR's benchmark ceiling is bottlenecked by reward-signal correctness, and a meaningful fraction of false-positive reward is enough to hurt training.

**Position B — Spurious Rewards ([[../research/rlvr-mechanics/spurious-rewards-rlvr]]).** On Qwen2.5-Math-7B / MATH-500, GRPO-trained RLVR with **fully random rewards** (Bernoulli(0.5), independent of correctness) still recovers **73% of the ground-truth-reward gain** (+21.4 pp vs +29.1 pp). The mechanism is a clipping-bias artifact in GRPO's PPO clip term that amplifies whatever behaviour already has high prior probability under the base model, regardless of whether the reward is informative. The implication runs opposite to Position A: RLVR gains can be substantially **decoupled from reward correctness**, at least for some models — reward-signal quality may matter far less than Position A's data-curation response assumes.

## Tension

Position A treats a 32.8% false-positive rate as damaging enough to justify a multi-stage data-verification and reward-shaping response. Position B shows that on at least one model family, reward correctness can be *reduced all the way to random* (a much larger corruption than 32.8% false positives) and still recover most of the benchmark gain. If Position B generalised to ReViSQL's setting, the team's data-curation investment would be substantially over-engineered relative to what the reward signal actually needed to contribute.

The two findings are not a clean contradiction — they differ on several axes that plausibly explain the gap:

- **Model family and existing prior.** Spurious Rewards' effect is explicitly **model-dependent**: Qwen2.5-Math has a strong pretraining prior toward a specific amplifiable behaviour (code-format reasoning) that the clip bias latches onto; Llama3 and OLMo2 show no comparable spurious-reward gain. ReViSQL-K2.6's base model and pretraining prior toward correct SQL structure are unconfirmed against this pattern — if the base lacks an analogous high-prior "shortcut," reward informativeness may matter far more for it than for Qwen2.5-Math.
- **Reward-noise structure.** Spurious Rewards tests uniformly random (uninformative) rewards; ReViSQL's 32.8% false-positive rate is **systematically correlated with a specific failure mode** (execution-match without semantic correctness) rather than uniform noise — a structured, exploitable bias may hurt more than pure randomness, since the model can learn to reliably trigger the false-positive condition rather than merely receiving an uninformative gradient.
- **Task structure.** Math benchmarks (Spurious Rewards) vs. text-to-SQL with an external database executor (ReViSQL) have different verifier semantics — execution-match false positives are a SQL-specific failure mode with no direct math-RLVR analogue.

## Resolution rule

*(Open — no ruling yet.)* What would resolve it: test whether ReViSQL's base model exhibits a Spurious-Rewards-style high-prior amplifiable behaviour (analogous to Qwen2.5-Math's code-reasoning exploit) — if so, the two findings may be reconciled as "random/uninformative noise is survivable when there's a good prior to amplify, but *systematically biased* noise is not," which would be a genuine refinement of Position B's claim rather than a contradiction of it. Alternatively, replicate Spurious Rewards' random-reward protocol directly on ReViSQL's pipeline to see whether text-to-SQL RLVR shows the same 73%-of-ground-truth robustness or is a case where Position A's data-sensitivity holds instead.

## Source

Surfaced via the 2026-08-28 weekly sweep. ReViSQL-K2.6 (Thinking Machines Lab blog, companion to arXiv:2603.20004), "Curating high-quality training data" and "Divergence 1" sections, in `raw/research/weekly-2026-08-28/.ingest/05-revisql-task-expertise-rl.summary.md`, checked against the wiki's existing [[../research/rlvr-mechanics/spurious-rewards-rlvr]] page.

## Related

- [[../research/rlvr-mechanics/revisql-verified-data-reward-shaping]] — Position A paper
- [[../research/rlvr-mechanics/spurious-rewards-rlvr]] — Position B paper
- [[../research/rlvr-mechanics/_overview]] — RLVR mechanics theme overview
- [[../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep
