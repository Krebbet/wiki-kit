# Cognition SWE-2

Cognition released SWE-2 on 2026-09-10, its most capable coding model, post-trained with reinforcement learning from Kimi K3 (Moonshot AI's 2.8T-parameter open model — roughly 3x the parameters of SWE-1.7's K2.7 base). It is Cognition's first model with selectable reasoning-effort levels (medium/high/max), all trained in a single RL run via a Pareto-slope-matched cost penalty. SWE-2 scores 50.0% on Cognition's own FrontierCode 1.1 Main benchmark — within 1 point of Fable 5.1 — at a claimed 64% lower cost, and leads the comparison set on Terminal-Bench 2.1 (92.8%), but trails Fable 5.1 and GPT-6 Astra by roughly 30 points on Terminal-Bench 4 (27.3% vs. 55.8%/57.9%). **Collect-but-confirm:** this is a third-party press writeup (MarkTechPost), not Cognition's own blog; FrontierCode is Cognition's own benchmark and all rival-model numbers in the comparison table come from Cognition's own evaluation, not independently reproduced. SWE-2 has no open weights and no standalone API — it runs only inside Devin (Desktop/CLI today, Web/Fusion rolling out).

## Training mechanism

The headline technical contribution is training all three effort levels (medium/high/max) in one RL run rather than three separate ones. The reward is `R = S - λC` (S = binary success, C = inference cost in USD mixed with rollout time); Cognition argues only a *linear* cost penalty keeps the RL objective a pure function of average cost and solve rate. Each effort level's λ is set to the local slope of the base model's Pareto curve, so the iso-reward line is tangent to the frontier — reward can only increase by pushing the whole cost/performance frontier up, not by shifting along it. A second contribution is a length-weighted reward baseline (`sum(R×L) / sum(L)`, used since SWE-1.6) that lowers inference-to-training KL divergence during training. Serving-side, a prefill delayer batches nearby requests (+10-20% TPM/TPS), DSpark speculative decoding (retrained via SpecForge) adds ~15% longer accept lengths, and NVFP4/FP8 kernels with quantization-aware training bound memory and train-inference mismatch.

## Behavior change: focused exploration

SWE-1.7 tended to over-explore on simple tasks. On FrontierCode 1.1 Main, SWE-2 medium scores higher than SWE-1.7 while taking 58% fewer turns and costing 81% less — mean steps per run drop from 127 (SWE-1.7) to 53/80/98 (medium/high/max), and SWE-2 medium makes its first real edit after a median of 18 steps versus 48 for SWE-1.7.

## Related

- [[deployments/cognition-cloud-agents]] — same vendor; SWE-2 is the model layer sitting on top of Cognition's existing cloud-agent/microVM infrastructure
- [[deployments/devin-security-swarm]] — same vendor's other 2026 capability release; Cognition's pattern of shipping specialized upgrades inside the same Devin product surface rather than as standalone offerings
- [[patterns/model-cost-routing]] — parallel cost/accuracy-frontier approach from a different axis: LangChain's Switchyard router buys a cost/accuracy tradeoff by routing *between* models of different sizes, whereas SWE-2 buys the same tradeoff *within one model* via RL-trained selectable effort levels
- [[patterns/claude-platform-cost-optimization]] — same week's parallel cost/performance-frontier story from Anthropic (effort calibration + prompt hygiene + caching) targeting the same tradeoff from the harness/prompt side rather than model training
- [[patterns/terminal-universe-trajectory-reconstruction]] — both report Terminal-Bench 2.1 gains via different mechanisms (synthetic SFT trajectory data there vs. RL post-training here)
- [[patterns/openai-gpt-5-6-agentic-primitives]] — parallel bet that some agentic-capability problems belong at the model-training layer rather than the harness layer

## Source

- `raw/research/weekly-2026-09-13/03-03-cognition-swe-2.md` — captured 2026-09-13 from MarkTechPost, "Cognition Releases SWE-2..." (2026-09-12). **Third-party writeup**, not Cognition's primary blog (`cognition.com/blog/swe-2`) — benchmark table numbers are Cognition-self-reported (collect-but-confirm).
