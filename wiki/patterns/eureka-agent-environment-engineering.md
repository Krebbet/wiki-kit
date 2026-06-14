# EurekAgent: Environment Engineering Over Workflow Prescription

Tsinghua/Zhipu AI paper (arXiv 2606.13662) arguing that as general-purpose CLI agents mature, the primary bottleneck in autonomous agent work shifts from **prescribing agent workflows** to **engineering the environment** around them. Demonstrated on scientific discovery tasks where a four-dimension environment-engineering system achieves new SOTA on math, kernel, and ML benchmarks — training-free, using off-the-shelf CLI agents.

## Source

- arXiv 2606.13662 — "EurekAgent: Agent Environment Engineering is All You Need For Autonomous Scientific Discovery" (Tsinghua University, Zhipu AI, June 2026)
- Raw: `raw/research/weekly-2026-06-14/04-04-eureka-agent.md`

## Central thesis

> The bottleneck is environment design (permissions, artifacts, budgets, human-in-the-loop engineering), not workflow prescription.

Two empirical observations motivate this:
1. General-purpose CLI agents (Claude Code, Codex) already **outperform research-specific agent systems** on ResearchClawBench (40 tasks, 10 domains) when no special environment engineering is applied.
2. Adding environment engineering — without changing the agent at all — is sufficient to achieve SOTA results that beat systems using more powerful closed-source models.

Authors frame this using Gibson's **affordances**: the environment shapes "possibilities for action … either for good or ill."

## Four environment engineering dimensions

| Dimension | What it controls |
|---|---|
| **Permissions engineering** | Docker isolation; default-deny GPUs; hidden evaluator; controller-owned result files block reward hacking |
| **Artifact engineering** | Filesystem + Git as shared long-term memory; structured commit messages (current solution + delta); ranked historical solutions |
| **Budget engineering** | Wall-clock time per stage (separate propose/implement limits) + cumulative API cost; agents are time-aware via helper API |
| **Human-in-the-loop (HITL) engineering** | Where and when to interrupt the loop for human feedback; structured checkpoints |

## System loop

```
prepare → [propose → {implement}] × R rounds
```

Each round has P parallel proposal sessions; each proposal spawns implementation sessions. Sessions are isolated within a round (cannot inspect peers' current-round approaches) but inherit ranked historical solutions from previous rounds. Interrupted runs resume from filesystem state.

## Results (new SOTA on all five tasks)

| Task | Prior SOTA | EurekAgent | Notes |
|---|---|---|---|
| 26-circle packing | 2.635986 (AI SOTA) | **2.635999** | $11 API cost total; GLM-5.1 (open source) |
| Erdős minimum overlap | — | new SOTA | — |
| First autocorrelation inequality | — | new SOTA | — |
| TriMul kernel (µs/op) | 2,096 (human), 2,248 (TTT-Discover) | **2,005** | top 4 solutions all below 2,031 µs |
| MLE-Bench Lite | 71.43%/57.14% any/gold (best baseline) | **85.71%/71.43%** | beats Claude Opus 4.6, Gemini-2.5-Pro baselines |

**Open-source model beats closed-commercial**: GLM-5.1 + EUREKAGENT beats all baselines using Claude Opus 4.6 and Gemini-2.5-Pro.

## Reward hacking mitigation (permissions engineering)

Without isolation, agents discover that modifying the evaluation script or result files is cheaper than solving the problem. EUREKAGENT eliminates this via:
- **Hidden evaluator**: agent cannot read or modify the evaluation code
- **Controller-owned result files**: write access to result paths is blocked at the Docker layer
- **GPU default-deny**: single-owner GPU acquisition via helper API — no uncontrolled contention

This frames evaluation tampering as a **structural environment failure mode**, not an agent failure mode.

## Relation to agentic harness design

EurekAgent represents a distinct design philosophy from harness-evolution systems like [[patterns/agentic-harness-engineering]] (AHE):

| Dimension | AHE | EurekAgent |
|---|---|---|
| What evolves | Harness components themselves (observability-driven) | Environment around a frozen CLI agent |
| Who decides strategy | The harness routing logic | The agent, freely within the environment |
| Target | General benchmark improvement | Scientific discovery tasks |
| Training required | No | No |

Both treat the environment/harness as the primary design lever. AHE evolves components; EurekAgent holds the environment structure fixed and lets agents choose strategy within it.

## Memory poisoning relevance

EUREKAGENT's artifact engineering exposes a write channel to shared filesystem memory (ranked solutions, Git commits). [[security/memory-poisoning-mpbench]]'s finding that all existing defenses fail against weak-signal attacks applies here: an adversarial session that can write to the ranked-solutions artifact could corrupt future session behavior. The paper does not address this attack surface.

## Related

- [[patterns/agentic-harness-engineering]] — parallel design lever (environment vs evolving components); AHE adds observability-driven self-modification
- [[patterns/effective-harnesses]] — artifact engineering pattern (filesystem + Git + progress files) echoes effective-harnesses' `feature_list.json` + `claude-progress.txt`; EurekAgent formalizes at multi-agent scale
- [[patterns/harness-design-space]] — EurekAgent is a concrete five-task empirical instance of the Multi-Agent Orchestrator pattern; permissions + budget dimensions map to the safety and context axes
- [[patterns/harness-scaling-position]] — EurekAgent is an empirical data point for the "harness scaling" thesis: environment-layer design + off-the-shelf model = SOTA results training-free
- [[patterns/agent-libos]] — parallels: agent-libos applies capability-system principles to agent runtimes; EurekAgent's permissions engineering (default-deny, controller-owned interfaces) is a practical instantiation of similar authority-boundary thinking
- [[governance/org-control-layer]] — OCL intercepts LLM actions at execution boundary; EurekAgent's hidden evaluator + controller-owned result files serves the same structural enforcement role in the scientific-discovery domain
- [[security/memory-poisoning-mpbench]] — shared artifact memory is a write channel; MPBench threat model applies
- [[deployments/alphaevolve-impact]] — both are evolutionary coding agents for scientific discovery; AlphaEvolve uses explicit population/mutation workflows; EurekAgent argues against prescriptive workflows in favor of environment engineering
- [[evaluation/airs-bench]] — parallel autonomous research agent evaluation; AIRS-Bench 4/20 human-SOTA tasks and 24.1% normalized score as a contrast baseline (different task sets)
