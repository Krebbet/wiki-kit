# Qwen-AgentWorld: Language World Models for General Agents

Qwen team (Alibaba) introduces the first language world models explicitly designed as general-purpose agentic environment simulators: Qwen-AgentWorld-35B-A3B and Qwen-AgentWorld-397B-A17B, trained via a three-stage CPT → SFT → RL pipeline on 10M+ real-world interaction trajectories across 7 agentic domains. The models simulate next-environment-state via long chain-of-thought reasoning, evaluated on the new AgentWorldBench benchmark (built from frontier-model interactions on 9 established agentic benchmarks), where they significantly outperform existing frontier models. Downstream use through two paradigms — decoupled synthetic RL environment generation and world-model warm-up before agent fine-tuning — yields agent performance improvements that surpass real-environment training baselines. Builds on Qwen2.5 MoE backbones and extends the world-model literature (Dreamer, TWM) from continuous/visual spaces to discrete language-action spaces.

## Method

Three-stage pipeline on Qwen2.5 MoE backbones:

1. **CPT (Continued Pre-Training):** injects general-purpose world modeling capability by training on state-transition dynamics and augmented professional corpora covering 7 agentic domains (web navigation, coding, GUI, tool use, embodied, game, science).
2. **SFT:** activates next-state-prediction reasoning using 10M+ real-world environment interaction trajectories. The model is trained to predict the next environment state given (current state, action) via long chain-of-thought reasoning.
3. **RL:** sharpens simulation fidelity via a custom framework with **hybrid rubric-and-rule rewards** — rubric rewards score reasoning quality; rule rewards score state-prediction correctness against ground truth.

Two deployment paradigms post-training:

- **Decoupled environment simulator:** generates synthetic RL environments at scale (thousands of environments) used to train downstream agent policies. Synthetic-only RL surpasses real-environment training.
- **Unified agent foundation model:** world-model training (CPT → SFT → RL) serves as a warm-up stage; agent SFT/RL applied on top yields downstream gains across 7 agentic benchmarks.

**AgentWorldBench:** new evaluation benchmark constructed from real-world interactions of 5 frontier models on 9 established agentic benchmarks. Assesses world model simulation fidelity directly.

## Results

- Qwen-AgentWorld significantly outperforms existing frontier models on AgentWorldBench (specific numbers in paper body; abstract reports direction only).
- As decoupled simulator: synthetic environment RL training yields gains surpassing real-environment training — challenges the assumption that real environments are necessary gold standard for agentic RL.
- As unified foundation model: world-model warm-up improves downstream agent performance across all 7 evaluated agentic benchmarks.
- 132 HuggingFace upvotes within days of release — high traction for a preprint.

## Novelty

- First language world models framed as **general-purpose agentic environment simulators** (prior work: task-specific or visual/3D modalities — see [[moonlake-world-models]]).
- Three-stage CPT → SFT → RL pipeline for world-model fidelity, with the RL stage specifically targeting simulation quality via hybrid rewards rather than task reward.
- AgentWorldBench as the first systematic cross-benchmark evaluation of LLM-as-world-model fidelity.
- Empirical demonstration that **synthetic RL environments from a language world model outperform real-environment training** — a meaningful benchmark for the field.
- World-model-as-warm-up paradigm: decouples world-model pretraining from agent policy training, making each stage independently composable.

## Applicability and Caveats

**Use as decoupled simulator** when real-environment rollout cost or diversity is a bottleneck for agentic RL — generates thousands of environments scalably. **Use as warm-up** when training a general-purpose agent model across multiple domains; adds world-model CPT before agent SFT/RL.

Constraints:
- Flagship model (397B-A17B) requires substantial MoE infrastructure; 35B-A3B is the practical deployment option.
- Coverage limited to 7 training domains; OOD domain generalization untested.
- Simulation fidelity degrades in rare or long-horizon states — inherent to language-space world modeling.
- Synthetic-env gains relative to real-env baselines depend on real-env availability; value scales inversely with real-env cost.

## Reproducibility

- **arXiv:** 2606.24597
- **Code:** https://github.com/QwenLM/Qwen-AgentWorld
- **Weights:** Qwen-AgentWorld-35B-A3B and Qwen-AgentWorld-397B-A17B (released)
- **Venue:** preprint, June 2026

## Source

`raw/research/weekly-2026-06-27/01-qwen-agentworld.md` (arXiv:2606.24597)

## Related

- [[moonlake-world-models]] — both target world models for agent training; Moonlake proposes 3D-visual hybrid pipelines for embodied settings with no quantitative results; Qwen-AgentWorld is language-action-space with benchmarks — different modality, same goal.
- [[agentflow]] — AgentFlow uses on-policy RL inside a multi-step agent loop; Qwen-AgentWorld generates the synthetic environments in which such agent RL could run — an upstream relationship; both are Qwen-ecosystem-adjacent.
- [[memagent]] — both apply RL to solve a non-differentiable objective in an agentic setting (memory overwrite policy vs. world-model fidelity); Multi-Conv DAPO and Qwen-AgentWorld's hybrid rubric+rule rewards are sibling credit-assignment approaches in agentic RL.
