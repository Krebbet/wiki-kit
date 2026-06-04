# SEAL: Self-Adapting Language Models

MIT/Harvard researchers introduce SEAL, a framework where LLMs generate their own fine-tuning data and training directives ("self-edits"), apply gradient-based weight updates, and are trained via RL to produce effective self-edits using downstream task performance as reward.

## Source

- `raw/research/weekly-2026-06-03/05-seal-self-adapting.md` (arXiv:2506.10943, June 2025, MIT/Harvard)

## Method

Given a new input (task, knowledge, or few-shot examples), the SEAL model generates a **"self-edit"** — a structured output that specifies:
1. How to restructure or reformat the input for better learnability (data synthesis).
2. Optimization hyperparameters (learning rate, number of steps).
3. Tool calls for data augmentation.

The self-edit is then used as fine-tuning data for a gradient-based SFT update, producing a **persistent weight change** in the model. No separate adaptation modules or auxiliary networks are involved — the primary model's own generation controls the entire adaptation process.

The **outer training loop** uses RL with downstream task performance of the post-update model as the reward signal, training the model to generate self-edits that lead to better post-update accuracy.

## Results

Specific benchmark numbers are not available from the abstract-only capture. The paper reports positive results on:
- **Knowledge incorporation tasks**: adapting to new factual or domain knowledge from examples.
- **Few-shot generalization tasks**: adapting from a small set of task examples.

Full quantitative comparison is in the PDF (not captured).

## Position Among Self-Improving Approaches

SEAL occupies a distinct niche — the only approach that trains the model to author both its own fine-tuning data *and* its own training configuration:

| System | What it modifies | How |
|---|---|---|
| **SEAL** | Weights (via gradient SFT) | RL-trained self-edit generation |
| [[huxley-godel-machine]] | Source code / agent logic | Tree-search over program modifications |
| [[gepa-reflective-prompt-evolution]] | Prompts | Genetic-Pareto evolution (no weight updates) |
| [[skillopt]] | Skill documents | Text-space optimizer with strict validation |
| SKILL0 (watchlist) | Parameters | In-Context RL skill internalization |
| [[rlsd-self-distilled-rlvr]] | Policy weights | Self-distilled RLVR (fixed pipeline) |

The key distinction from [[rlsd-self-distilled-rlvr]] and [[anti-self-distillation]]: those works examine self-distillation as a fixed data pipeline; SEAL makes adaptation strategy a *learned, RL-optimized behavior* — the model decides what data to generate and how to train on it.

## Related

- [[huxley-godel-machine]] — self-modification via code; SEAL via weights; complementary axes
- [[gepa-reflective-prompt-evolution]] — prompt-space self-adaptation; SEAL is the weight-space counterpart
- [[skillopt]] — text-space skill optimization; both are RL-trained self-improvement approaches operating in different parameter spaces
- [[anti-self-distillation]] — raises structural concerns about self-generated data quality; relevant to SEAL's self-edit validity
- [[rlsd-self-distilled-rlvr]] — self-generated training data as mechanism; SEAL extends this to RL-optimized, self-configured training
- [[agentflow]] — both train agentic behaviors end-to-end with outcome reward; different scope (tool use vs. weight self-modification)
