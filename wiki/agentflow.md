# AgentFlow: In-the-Flow Agentic System Optimization

Stanford / Texas A&M / UCSD / Lambda (arXiv:2510.05592, ICLR 2026 Oral, top 1.1%). A four-module agentic system (Planner / Executor / Verifier / Generator) trained on-policy *inside its own multi-turn loop* via **Flow-GRPO**, a credit-assignment trick that broadcasts the trajectory-level final-outcome reward to every turn's policy update. Solves the long-horizon sparse-reward instability that breaks monolithic tool-integrated RL (Search-R1, ToRL, TIR) at long depths. **Qwen2.5-7B AgentFlow + Flow-GRPO beats GPT-4o (~200B)** on search, agentic (GAIA), math, and science benchmarks.

## Method

Four specialist modules around a deterministic structured evolving memory `M`:

- **Action Planner π_θ** — the only trained policy.
- **Tool Executor**, **Execution Verifier**, **Solution Generator** — frozen Qwen2.5-7B-Instruct in all reported runs.
- **Tools**: Google Search, Wikipedia Search, Web Search, Python Coder, Base Generator.

**Flow-GRPO** roll-outs the full live system on-policy, then broadcasts the single binary final-outcome reward (LLM-as-judge rubric via GPT-4o) to every turn's policy update. Per-turn advantage is group-normalized across G=8 parallel rollouts. Objective: clipped PPO ratio with KL penalty β=0.001 against a frozen reference. The key formal result (Appendix B) is the proof that this reward broadcast decomposes the multi-turn MDP into independent single-turn updates with the same fixed point — i.e., long-horizon credit assignment becomes a sum of well-conditioned single-turn problems.

Training: 8×A100, lr=1e-6, max 3 turns per rollout, batch 32, planner T=0.5, tools T=0.0. Derives from GRPO (Shao 2024) extended to the multi-module, variable-horizon MDP setting. Closest competitors are Search-R1 (Jin 2025) and ToRL (Li 2025), both of which run a single monolithic policy with full context — which is what AgentFlow argues is the source of long-horizon instability.

## Results

Backbone Qwen2.5-7B-Instruct everywhere. Headline: 7B AgentFlow + Flow-GRPO outperforms GPT-4o across all four domains.

**Search** (avg of Bamboogle / 2Wiki / HotpotQA / Musique): **57.3 avg**, +14.9 pp over the best 7B baseline (AutoGen 42.4). Bamboogle 77.2 (+17.2 over AgentFlow w/o Flow-GRPO).

**Agentic** (GAIA): **33.1**, +15.9 pp over AgentFlow w/o Flow-GRPO (17.2), +14.0 pp over next-best (Search-R1 19.1).

**Math** (avg AIME24 / AMC23 / GameOf24): **51.5**, +19.8 pp over AgentFlow w/o (31.7), +14.5 pp over next-best (ToRL 37.0). AIME24 40.0 vs ToRL 20.0.

**Science** (GPQA / MedQA avg): **63.5**, +4.1 pp over next-best (TIR 59.4). GPQA 47.0 / MedQA 80.0.

**Ablation (Table 3):** Offline SFT on the same trajectories collapses avg accuracy by 19.0 pp — i.e., the policy distribution shift from on-policy rollouts is doing real work, not just imitation. Frozen GPT-4o as planner gains only +5.8 pp over frozen Qwen; Flow-GRPO gains +17.2 pp. **The trained 7B planner outperforms a frozen GPT-4o planner.**

**Inference scaling**: monotonic improvement from T_max=3 to T_max=10 with no degenerate loops.

## Why this matters

Multi-turn tool-integrated RL has been stuck on a credit-assignment problem: you can only verify the final answer, but every intermediate planning decision contributed to it. Existing approaches either (a) ran a monolithic policy on full context and ate the long-horizon variance (Search-R1, ToRL), or (b) stayed training-free and used hand-engineered prompts (AutoGen). AgentFlow's modular decomposition + on-policy training + reward broadcast is the first method that gets the empirical benefits of both — and the formal equivalence proof (Appendix B) explains why it should generalize beyond the four-module instance shown.

Flow-GRPO joins a growing pattern of GRPO-line credit-assignment fixes: [[token-gradient-cancellation]] fixes within-group token gradient cancellation; [[neural-garbage-collection]] broadcasts outcome reward to KV-eviction decisions; AgentFlow broadcasts outcome reward across multi-turn modules. The same structural trick (broadcast a sparse outcome reward to all the latent decisions that contributed) is what unlocks RL training in three different sequential problems this year.

[[gepa-reflective-prompt-evolution]] is the explicit opposite-end position on the trainable-vs-training-free axis the paper discusses — GEPA evolves prompts with no weight updates, AgentFlow updates weights inside the loop. AgentFlow's offline-SFT-collapse result is direct evidence for the camp that *on-policy* training is necessary for compound systems, not optional.

## Reproducibility

- Code: https://github.com/lupantech/AgentFlow.
- Weights: https://huggingface.co/AgentFlow/models.
- Demo: https://huggingface.co/spaces/AgentFlow/agentflow.
- Website: https://agentflow.stanford.edu.
- LLM-judge reward uses GPT-4o (external dependency for exact reproduction). Training feasible on 8×A100.

## Source

- `raw/research/weekly-2026-05-04/04-agentflow.md` — arXiv:2510.05592 (ICLR 2026 Oral).

## Related

- [[huxley-godel-machine]] — adjacent self-improving-agent line; HGM uses tree-search CMP for scaffold evolution, AgentFlow uses Flow-GRPO for in-loop weight updates. Both 7B-class systems beating much larger frozen baselines.
- [[token-gradient-cancellation]] — sibling GRPO-credit-assignment fix at the within-trajectory token level.
- [[neural-garbage-collection]] — sibling outcome-broadcast pattern (RL-trained KV eviction).
- [[rlsd-self-distilled-rlvr]] — adjacent RL post-training stabilization line.
- [[gepa-reflective-prompt-evolution]] — opposite-end position on trainable-vs-training-free agentic optimization.
- [[watchlist]] — Search-R1, ToRL, TIR, AutoGen referenced as baselines.
