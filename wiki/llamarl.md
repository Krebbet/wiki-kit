# LlamaRL: Distributed Asynchronous RL for Large-Scale LLM Training

Meta presents LlamaRL, a production asynchronous RL training framework used for Llama 3 post-training that achieves up to 10.7× speedup over DeepSpeed-Chat-like synchronous systems on a 405B policy model.

## Source

- `raw/research/weekly-2026-06-03/04-llamarl.md` (arXiv:2505.24034, Meta, May 2025)

## Architecture

LlamaRL uses a **single-controller** design built on native PyTorch, decoupling policy generation (rollout) from policy update (learning) via a fully asynchronous pipeline. Three core mechanisms:

1. **Colocated model offloading**: shares GPU memory between rollout and training phases without inter-node copying — the same GPU pool alternates between generating rollouts and running the training step, avoiding the dedicated-server cost of OpenRLHF-style designs.
2. **Asynchronous off-policy training**: learning proceeds on stale rollout batches while new rollouts are generated concurrently, eliminating the synchronization bubble inherent in synchronous systems (wait for rollout → update → wait for rollout...).
3. **RDMA/DMA weight synchronization**: broadcasts updated weights to the rollout worker via direct memory access, avoiding the bandwidth bottleneck of naive parameter broadcast over Ethernet.

The single-controller design (vs. multi-controller systems like OpenRLHF) simplifies scheduling and avoids deadlock-prone cross-role coordination.

A **formal proof** establishes that asynchronous design yields strict wall-clock speedup over synchronous alternatives under mild assumptions (rollout time > update time, which holds at large scale).

## Results

- **10.7× throughput speedup** vs. DeepSpeed-Chat-like synchronous baselines at 405B scale.
- Validated at 8B, 70B, and 405B on GPU clusters from a handful to thousands of devices.
- Speedup advantage grows with model scale — favorable asymptotic behavior.
- Used in production for Llama 3 post-training (not a research prototype).

## Context in Wiki

The wiki has multiple RL method/algorithm pages (GRPO variants, preference optimization, RLVR), but no RL infrastructure or systems pages. LlamaRL fills that gap: it's the systems layer that makes large-scale RLVR feasible. Without an async pipeline like this, the wall-clock cost of RL at 405B would make many methods (DAPO, GRPO at scale) impractical.

Prior open-source RL systems (DeepSpeed-Chat, OpenRLHF, TRL, NeMo-RL) are largely synchronous; LlamaRL is the first production-validated asynchronous framework at this scale with a formal speedup guarantee.

## Related

- [[agentflow]] — Flow-GRPO agentic pipeline; on-policy GRPO rollouts that would benefit from async infrastructure
- [[eggroll]] — addresses 14B+ scale RL challenges via Evolution Strategies instead of gradient-based RL; different approach to the same scale bottleneck
- [[token-gradient-cancellation]] — DFPO targets RL gradient quality; LlamaRL targets RL pipeline throughput; complementary axes of RL efficiency
- [[reasonmaxxer]] — cheap alternative to full RL; LlamaRL is the systems answer to "how do you afford full RL at scale"
