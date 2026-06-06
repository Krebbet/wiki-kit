# Polar: Harness-Agnostic Agentic RL at Scale (NVIDIA)

Polar is an NVIDIA rollout-as-a-service framework that intercepts an agent harness's LLM API traffic via a provider-compatible proxy, reconstructs token-faithful trajectories without modifying the harness, and exposes async service endpoints for independent RL trainers — achieving +22.6pt SWE-Bench Verified on Qwen3.5-4B with GRPO via the Codex harness.

## Method

Polar inverts the conventional RL integration contract. Instead of requiring a harness to implement a Gymnasium-style interface, Polar places a gateway proxy at the LLM API boundary. The harness points its model base URL at the gateway; the proxy detects provider protocol (Anthropic Messages, OpenAI Chat Completions, OpenAI Responses, Google generateContent), normalizes requests to a local inference backend, captures prompt/response token IDs, log probabilities, and finish reasons, and returns a provider-compatible response. The harness runs unchanged — including sub-agents, context compaction, parallel branches, and multi-turn tool use.

**Architecture split.** A rollout server accepts a `TaskRequest`, expands it into `num_samples` independent sessions, dispatches across gateway nodes, and exposes polling/callback endpoints for trainers. Each gateway manages a staged lifecycle: INIT (runtime startup) → READY buffer (pre-warmed) → RUNNING (harness execution with proxy active) → POSTRUN (trajectory construction, evaluation, callback, teardown). This keeps CPU-heavy setup off the GPU-bound critical path.

**Trajectory reconstruction — prefix merging.** `per_request` emits each model call as an independent trace (lossless but fragments sessions → 20.4% rollout GPU utilization in ablation). `prefix_merging` partitions the captured `CompletionSession` into append-only chains by verifying a strict token-prefix relation between adjacent completions, copying sampled assistant tokens verbatim, and marking interstitial harness-injected context with `loss_mask=0`. Sub-agent spawns, context compaction, and parallel tool conversations form separate chains naturally. Result: 5.39× throughput over per_request (87.7% vs 20.4% GPU utilization).

**Reward propagation.** Outcome rewards broadcast to all traces in a session; per-trace process rewards assignable via custom evaluator strategies. Built-in evaluators: session-completion, test-on-output, SWE-Bench/SWE-Gym. Training backend: Slime (Megatron+SGLang). Runtime isolation: Docker or rootless Apptainer. Built-in harness adapters: `claude_code`, `codex`, `gemini_cli`, `qwen_code`, `opencode`, `pi`.

## Results

**SWE-Bench Verified (pass@1), Qwen3.5-4B, GRPO via Slime:**

| Harness | Base | Polar RL | Gain |
|---|---|---|---|
| Codex | 3.8% | 26.4% | +22.6pt |
| Claude Code | 29.8% | 34.6% | +4.8pt |
| Pi | 34.2% | 40.4% | +6.2pt |
| Qwen Code | 34.6% | 35.2% | +0.6pt |

Training reward: Codex 9.5% → 54.5%; Claude Code 28.8% → 67.0%.

Offline SFT generation (Qwen3.5-122B-A10B, pi harness, ~64 GPU-hours): 504/1,638 instances accepted (30.8%); dataset released as `nvidia/polar-swegym-pi-qwen35-122b-a10b-trajectories` (Apache-2.0).

## Applicability

Best suited for pre-existing CLI tools, packaged binaries, or closed-source harnesses that cannot be reimplemented as a framework environment. Requirements: harness uses a provider-compatible LLM API; runtime is containerizable. Rollout nodes (CPU + inference GPU) decouple from trainer nodes. Long-horizon, sparse-reward tasks (SWE-style) are the target workload — async staging directly addresses long-tail execution variance.

Limitation: `per_request` with outcome-reward broadcasting produces reward hacking from noisy credit assignment; process reward models or session normalization are needed.

## Source

- arXiv: https://arxiv.org/abs/2605.24220 (2026)
- NeMo Gym: github.com/NVIDIA-NeMo/Gym
- Dataset: huggingface.co/datasets/nvidia/polar-swegym-pi-qwen35-122b-a10b-trajectories

## Related

- [[llamarl]] — single-controller async RL infra (Meta); compare to Polar's harness-agnostic proxy design
- [[agentflow]] — agentic RL training; Polar provides the rollout substrate
- [[huxley-godel-machine]] — SWE-Bench Verified benchmark shared; compare scores and model scale
- [[eggroll]] — rollout scaling at hyperscale (ES not RL); different mechanism but async staging overlap
- [[skillopt]] — agent skill optimization; Polar's harness-native reward signal is a relevant training mechanism
