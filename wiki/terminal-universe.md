# Terminal-Universe

Qwen Team/Alibaba (arXiv:2609.04148) reconstructs executable terminal/coding environments from *frozen agent trajectories* — inverting the usual "environment → trajectory" direction into "trajectory → environment" — then re-queries each recovered workspace along breadth (cross-workspace) and depth (multi-round) axes to synthesize verifier-filtered SFT data. Yields 37.3k task-sufficient environments and large agentic-coding gains from SFT alone, no RL.

## Method

Three stages: (1) deterministic replay of recorded tool calls recovers each touched file's pre-agent-edit state; (2) agentic completion fills in missing files/dependencies without solving the task (mean file count 2.9→22.4); (3) an agentic judge with read-only tools filters for sufficiency (93.5% post-completion vs. 40.2% post-replay). On retained environments, four re-querying mechanisms generate new tasks: Intent Recovery (reconstruct the original request), Single-WS (offline task generation), Cross-WS (TF-IDF + LLM-judge dependency mining between workspaces), and Multi-Round (a user-agent issues grounded follow-ups for up to 6 rounds). Every task gets an agent-authored pytest verifier.

## Results

SFT of Qwen3.5-27B on the resulting 32.0k-demonstration mixture reaches 58.1% Terminal-Bench 2.1 (+11.9 over base 46.2), beating every listed task-synthesis baseline (RST-27B 49.4, CalibForge 47.6, TMax-27B 44.9) at comparable/smaller scale. Key ablations: re-solving with a stronger teacher beats imitating source trajectories (52.1 vs. 36.7 avg); agentic completion adds +4.2 pts over replay-only; under a matched data budget, scaling the *number of environments* (53.2→56.0) beats scaling queries/env or solutions/query — "each new environment contributes distinct executable context."

No code/weights release found in the captured text.

## Applicability

Usable by any team with a corpus of terminal/CLI or SWE agent trajectories (Claude Code, OpenHands, or internal logs), a frontier-scale teacher for completion/rollout, and sandboxed container infra. Pure SFT — no RL infrastructure required.

## Related

- [[qwen-agentworld]] — same Qwen/Alibaba lineage, same "agentic environments are the scarce training resource" framing, opposite strategy (simulating domains vs. reconstructing real ones from trajectories).
- [[skill-self-play]] — also Qwen/Alibaba; synthesizes new tasks from existing resources, via GRPO self-play rather than SFT+verifiers.
- [[argus-agentic-runtime]] — shares the verifier-gated, agent-authored task/evidence design pattern.
- [[memoharness]] / [[skillopt]] — agent-as-editor/validator loops in the adjacent harness/skill-optimization space.
