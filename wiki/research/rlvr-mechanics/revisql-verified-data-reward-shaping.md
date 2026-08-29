# ReViSQL-K2.6: Verified-Data Curation and Reward Shaping Close the RLVR Gap on Text-to-SQL to Superhuman

Thinking Machines Lab / UIUC Kang Lab, "Putting Task Expertise into RL Achieves State-of-the-Art Performance on Text-to-SQL" (blog post, Aug 27 2026, companion to arXiv:2603.20004, Zhu, Jin, Choi, Kang). RLVR fine-tuning of Kimi-K2.6 (→ ReViSQL-K2.6; replicated on Qwen3-235B-A22B) directly on text-to-SQL — no schema-linking/generation/self-correction/voting scaffolding — using an expert-cleaned ~2.5k-example dataset (BIRD-Platinum) plus two targeted reward-shaping fixes. Result: super-human accuracy on BIRD at a fraction of frontier-model cost, and a quantified demonstration that annotation noise, not the RL algorithm, was the binding constraint.

## Method

- **Base recipe.** Standard RLVR (via Tinker API), on-policy, outcome reward = execution match against the gold query. No agentic pipeline stages (schema linking, draft-then-correct, external voting) — a single model call per query, with self-consistency (SC-16, majority vote over execution-result groups) as an optional inference-time addition that requires no extra model calls.
- **Data curation.** Multi-stage expert + LLM audit and relabeling of BIRD Train into "BIRD-Platinum" (2.5k instances), with a matching cleaned eval set "Arcwise-Plat-SQL" (BIRD Mini-Dev with errors fixed). LLM auditor alone caught only 24.5% of human-flagged errors at 90.6% precision — human review was load-bearing, not automatable away.
- **Reward shaping, fix 1 — VeriEQL semantic-equivalence downweighting.** Execution-match reward is downweighted when the generated query matches the gold query's result on the specific DB instance but fails a bounded semantic-equivalence solver (VeriEQL), i.e. would diverge on a different instance. Solver cost is <0.1% of training compute.
- **Reward shaping, fix 2 — rule-based knowledge-grounding process reward.** The model must emit a "requirement block" translating each supplied external-knowledge entry into an explicit query constraint, and a "verification block" auditing the generated query against those constraints; non-compliance is penalized. Rule-based and deterministic, not model-graded — cheap and free of judge-model contamination, but requires BIRD-style structured external-knowledge annotations to exist in the data.

## Claims

- **Superhuman, no scaffolding.** Greedy decoding (single sample, temp=0): 91.37% on Arcwise-Plat-SQL at $0.035/task — 8.4 pp above OpenSearch (strongest prior open-source scaffolded pipeline, arXiv:2502.14913) at 37% lower cost. SC-16 (temp=1, 16 samples): 92.97% at $0.56/task, exceeding the human BIRD benchmark of 92.96% — claimed as the first text-to-SQL AI system to exceed human accuracy. Also beats Claude Fable 5 and GPT-5.6 Sol Ultra in accuracy at 12–15% of their cost.
- **Data curation alone is most of the gain.** Training on BIRD-Platinum with no reward shaping already reaches 88.55% on Arcwise-Plat-SQL — above frontier generalist LLMs and prior fine-tuned open-weight SQL models (Infly-RL-SQL-32B, OmniSQL-32B, XiYanSQL-32B, Arctic-R1-7B). Reward shaping adds the remaining ~2.8 pp to reach 91.37%.
- **Verified data transfers, not just overfits.** Qwen3-235B-A22B trained on BIRD-Platinum vs. uncurated BIRD Train, evaluated zero-shot on untouched, harder benchmarks: +16% (Arcwise-Plat-SQL), +12% (Spider2-SQLite, 5.2× more tokens/query on average), +14% (Spider2-Snow, Snowflake dialect). Framed as evidence the cleaned signal is more transferable across benchmark and dialect shift, not merely fitted to BIRD's annotation quirks — though this is a data-quality → generalization argument, not a mechanistic concept-acquisition claim.
- **The data-quality finding.** Raw BIRD Train audit (2.5k sampled instances): 61.1% had at least one error (gold SQL incorrect 52.1%, NL question flawed 26.2%, external knowledge wrong 18.2%, unanswerable/discarded 1.5%). BIRD Mini-Dev (eval) had a 52.8% error rate after two cleanup passes. In a pilot run, **32.8% of positive execution-match rewards were false positives** — the generated query matched gold on that DB instance without being semantically equivalent, i.e. roughly 1-in-3 positive rewards reinforced a subtly wrong query. Separately, 24.2% of failures traced to the model ignoring supplied external knowledge and defaulting to pretraining priors (e.g. "sodium = 0" vs. "sodium < 5" — predicates identical on the given DB but not in general). Authors' framing: "algorithmic tweaks cannot compensate" for this loss — curation is necessary, not optional, for RLVR to work well here.

## Why this is load-bearing

**Not single-sample or few-shot.** This is dataset-scale RLVR fine-tuning on ~2.5k curated (question, schema, gold SQL) instances, not a handful of examples — it does not bear on low-shot method design directly. Its relevance to this wiki is as an industrial-scale, quantified **data-quality-is-the-bottleneck case study**: a 32.8% false-positive reward rate measurably hurts RLVR training, and cleaning the data (not tuning the optimiser) closes most of the gap to superhuman. This directly reinforces [[_overview]]'s framing that the sample-efficiency bottleneck in RLVR is the reward signal, not the optimiser — here demonstrated at the level of *label correctness* rather than reward density. The rule-based knowledge-grounding process reward is also a concrete, cheap, non-model-graded process-reward design pattern, of interest wherever structured task annotations (external knowledge, constraints) already exist.

## Limitations

- **Curation cost is not amortized.** The entire approach depends on an expensive multi-stage human-expert + LLM-auditor pipeline (LLM auditor alone caught only 24.5% of human-flagged errors). This cost is real and not accounted for in the per-task cost figures.
- **Narrow domain specialist.** SQL only; no claim or test of transfer to other domains.
- **Annotation-dependent reward.** The knowledge-grounding process reward assumes BIRD-style external-knowledge annotations exist in the data — most real deployments won't have this structure available.
- **Execution-match ≠ semantic equivalence**, motivating but not eliminating the VeriEQL fix — bounded verification, not exhaustive.
- **Outcome-only reward is blind to *why*** the model got the right answer, motivating but only partially addressing the knowledge-grounding gap via process supervision.
- **Cost figures are per-task, API-style** — not a full accounting of RL training compute or human curation labor.
- **Exploration/sampling hyperparameters** (group size, KL, etc.) are not disclosed in the blog post; deferred to the GitHub repo and technical report (arXiv:2603.20004), not fetched here.
- **Tension with reward-noise-robustness findings elsewhere in this wiki** — see [[../../conflicts/revisql-vs-spurious-rewards-noise-robustness]].

## Source

- `raw/research/weekly-2026-08-28/05-revisql-task-expertise-rl.md`
- https://thinkingmachines.ai/news/putting-task-expertise-into-rl/

## Related

- [[_overview]] — RLVR mechanics theme overview; this page's data-quality finding reinforces the "sample-efficiency bottleneck is the reward, not the optimiser" framing at industrial scale
- [[spurious-rewards-rlvr]] — in tension: that page finds RLVR gains largely survive fully random rewards (73% of ground-truth gains recovered) on Qwen2.5-Math-7B, while this page finds a 32.8% systematically-biased false-positive rate measurably hurts training — see [[../../conflicts/revisql-vs-spurious-rewards-noise-robustness]] for the open reconciliation question
- [[../process-reward-models/_overview]] — the rule-based knowledge-grounding process reward (requirement block + verification block) is a deterministic, non-model-graded process-reward-shaping mechanism
- [[../../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep
