# Reflexion: Language Agents with Verbal Reinforcement Learning

Northeastern + MIT + Princeton paper (Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao; arXiv 2303.11366; NeurIPS 2023) that introduces *verbal reinforcement learning* — reinforcing LLM agents without weight updates by converting environment feedback into natural-language self-reflection stored in an episodic memory buffer. The central framing: *"Reflexion converts binary or scalar feedback from the environment into verbal feedback in the form of a textual summary, which is then added as additional context for the LLM agent in the next episode. This self-reflective feedback acts as a 'semantic' gradient signal by providing the agent with a concrete direction to improve upon."* Reflexion is the canonical instance of the *reflective and self-improving memory* family in [[memory-architectures]]; [[generative-agents]] extends it with a recency/importance/relevance retrieval scheme; [[agentic-context-engineering]] (ACE) is the 2025 instantiation at the context-engineering layer.

## The three components

- **Actor (Mₐ)** — takes state observations + memory buffer (`mem`) as input. Generates text and actions conditioned on the current policy. Implementations: Chain-of-Thought, ReAct.
- **Evaluator (Mₑ)** — takes a generated trajectory; computes a scalar reward `r_t`. Implementations vary by task: exact match for reasoning, hand-written heuristics for decision-making, LLM-as-evaluator for programming. Outputs only the scalar — no language.
- **Self-Reflection model (M_sr)** — takes the sparse reward signal, the current trajectory, and persistent memory; generates "nuanced and specific" verbal feedback `sr_t` that is more informative than the scalar reward. Output is appended to `mem` for the next trial. Example: in a multi-step task the agent can verbally state it should have taken a different action `a'_i` which would have changed subsequent actions.

## The episodic memory buffer

Two tiers mirroring human memory:
- **Short-term** — current trajectory history (fine-grained recent detail).
- **Long-term** — accumulated self-reflection summaries `sr_t` from past trials (distilled experience).

After each trial `t`, the reflection `sr_t` is appended to `mem`. Buffer is bounded by a maximum Ω, **typically 1–3 stored experiences**. AlfWorld experiments truncate to the last 3 self-reflections.

## Reflection trigger

Reflection runs after a *failed* trial, not after every trial. For AlfWorld, two triggers:
1. **LLM self-evaluation** — natural-language binary pass/fail classification.
2. **Hand-written heuristic** — reflect if agent executes the same action and gets the same response for >3 cycles, OR if action count exceeds 30 (inefficient planning indicator).

For reasoning and coding tasks, the binary environment reward (exact match failure or unit-test failure) triggers reflection. Loop continues until the Evaluator deems the output correct, or until 3 consecutive failed attempts on the same task.

## Empirical results

**Decision-making (AlfWorld)** — 134 text-based household tasks. ReAct + Reflexion completes **130/134 tasks** using a heuristic evaluator. **+22pp absolute** over ReAct baseline across 12 iterative learning trials.

**Reasoning (HotPotQA)** — Wikipedia multi-hop QA. Reflexion improves over baseline by **+20pp**. Ablation: self-reflection adds an **+8pp boost over episodic memory alone**. Specific results: CoT (GT) + GPT-4 baseline 0.68 → 0.80 with Reflexion; ReAct + GPT-4 baseline 0.39 → 0.51.

**Code generation:**
- HumanEval (Python): **91.0% pass@1** vs GPT-4 baseline 80.1% — +11pp.
- HumanEval (Rust): 68.0% vs 60.0%.
- MBPP (Python): 77.1% vs 80.1% — *Reflexion underperforms* (see limitations).
- MBPP (Rust): 75.4% vs 70.9%.
- LeetcodeHard (Python): **15.0% vs 7.5%** — doubling the baseline.

## Pareto-optimal vs ReAct / CoT

Reflexion is the only approach in the paper's comparison table that simultaneously supports self-refinement, hidden constraints, decision-making, binary rewards, and memory. ReAct and CoT-only agents *"fail to probabilistically improve on any tasks, meaning that no failed tasks from the first trial from any of the baseline approaches were able to be solved in subsequent trials"* (HotPotQA, temperature 0.7). In AlfWorld, ReAct-only converges at a 22% hallucination rate with no long-term recovery; Reflexion reaches near-perfect performance.

## Self-documented limitations

The authors flag four explicitly:

1. **Local minima** — *"Reflexion is an optimization technique... it may still succumb to non-optimal local minima solutions."* Demonstrated empirically on WebShop: after 4 trials the agent shows no improvement and generates unhelpful reflections. Conclusion: *"Reflexion is unable to solve tasks that require a significant amount of diversity and exploration."*
2. **Context-window cap on memory** — long-term memory is a sliding window (Ω = 1–3); authors encourage future work with vector databases or SQL.
3. **Self-evaluation quality dependency** — weaker models show no improvement at all (e.g., starchat-beta: 0.26 baseline = 0.26 Reflexion). The reflection only works if the model can reason about its own failures.
4. **Code-specific: flaky test suites** — false positives in self-generated unit tests cause premature acceptance of incorrect solutions. Explains the MBPP Python underperformance: 16.3% false-positive rate vs 1.4% for HumanEval Python.

## Why it matters in the family taxonomy

Reflexion's core operation — observe failure → generate verbal reflection → store in episodic buffer → condition next trial — is the *reflective and self-improving memory* mechanism family in [[memory-architectures]]. The paper's contribution is the abstraction itself: *learning without weight updates* by leveraging the LLM's own ability to articulate what went wrong.

Subsequent systems extend the abstraction:
- [[generative-agents]] — same year (2023) — adds a structured retrieval scheme (recency × importance × relevance) over a memory stream containing observations + reflections + plans. Reflexion's simple sliding window is replaced with selective retrieval.
- [[agentic-context-engineering]] (ACE, 2025) — applies the generate-reflect-curate playbook to context engineering itself: the agent reflects on what should persist in its working context across long-running sessions, not just on individual task trajectories.
- [[anthropic-memory-tool]]'s recommended pattern of "as you make progress, record status / progress / thoughts etc in your memory" is the production-API expression of Reflexion's memory-write step at the agent-runtime level.

## SDAR contrast and memory-evolution survey framing

**SDAR contrast.** [[patterns/sdar]] (arXiv 2605.15155) is a post-training token-level RL method; Reflexion is inference-time verbal RL. Both use self-generated signals to improve agents, but at entirely different phases and granularities: Reflexion runs during task execution (verbal failure → reflection → episodic buffer → retry); SDAR runs during weight training (token-level sigmoid-gated distillation from privileged-context rollouts). The analogy is superficial — they do not compete at the same layer.

**Memory-evolution survey framing.** The 2026 memory-evolution survey (arXiv 2605.06716, [[memory/memory-evolution-survey]]) classifies Reflexion in Table 1 as a **Reflection-stage** exemplar (Introspection sub-type): it transforms a single trajectory's errors intra-trajectory (F_ref(τ_i | φ) = m'_i) and retrieves past reflections for semantically similar tasks. The survey's **Experience stage** is distinct — it requires cross-trajectory abstraction into policy priors applicable to unseen scenarios without trajectory-level matching (F_exp(T_batch) = K). This is a framing nuance, not a factual conflict: Reflexion's per-episode reflection loop is trajectory-local, and the survey's taxonomy clarifies that cross-trajectory policy abstraction is an emergent frontier above it.

## Source

- `raw/research/memory-management/06-02-reflexion.md` (captured 2026-04-26 from https://arxiv.org/pdf/2303.11366 via marker on CPU; figures preserved in `assets/02-reflexion/`)

## Related

- [[memory-architectures]] — survey's *reflective and self-improving memory* family; Reflexion is the canonical instance.
- [[generative-agents]] — contemporaneous extension with retrieval scoring over a memory stream.
- [[agentic-context-engineering]] — 2025 ACE applies the generate-reflect-curate pattern to context engineering.
- [[anthropic-memory-tool]] — production-API expression of memory-write as a discipline.
- [[ai-scientist-v2]] — uses VLM-as-quality-gate for generated figures, a domain-specific reflection mechanism.
- [[topology-taxonomy#long-horizon-context-loss]] — Reflexion's per-trial reflection is a building block for the broader context-loss mitigation thread.
- [[patterns/sdar]] — post-training token-level RL contrast: both self-improve via self-generated signals, at different phases.
- [[memory/memory-evolution-survey]] — classifies Reflexion as Reflection-stage (Introspection); distinguishes it from Experience-stage cross-trajectory abstraction.
