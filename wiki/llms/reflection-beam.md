# Reflection Beam

Beam is Reflection AI's first "frontier" open-weight model, unveiled 2026-10-05: text-only MoE, 501B total / 23B active parameters, 1M-token context, pretrained on 23.8T tokens and RL-trained for reasoning, coding and agentic tasks. Vendor claims parity with Z.ai GLM-5.2 on advanced reasoning benchmarks at "3-4x less inference compute" — unverified. **Weights are NOT yet released** (promised "this month", i.e. October 2026). Watch, do not build on it until weights and independent evals land.

## What it does

- Text-only mixture-of-experts model; positioned as a "workhorse model" for enterprises, public sector and developers (2026-10-05).
- Targets reasoning, coding and agentic tasks at "a fraction of the token cost and inference time compute" of rivals (vendor wording).
- Reflection pitches Beam and later models into "AI factories": institutions train customized local models on proprietary data. Sovereign-AI pilot with Shinsegae Group (South Korea) is in testing. Axios reports hedge funds and trading firms are interested (2026-10-04).

## Techniques under the hood

- 501B total / 23B active parameters (vs GLM-5.2 ~744B / 40B per TechCrunch, 2026-10-05) *(editorial: ~2x fewer active params is the basis of the compute-cost claim)*.
- 23.8T pretraining tokens; 1M context window.
- "High-compute reinforcement learning" post-training. No further detail (RL recipe, data, architecture specifics) in source.

## Deployment model

- Weights and full technical details promised for October 2026; **availability: announced, not shipped as of 2026-10-07**. License terms: not specified in source.
- Launch distribution promised via hyperscalers and neoclouds, plus integrations across open-source libraries. Named partners: not specified in source.
- Compute backing: deals collectively >$7B with SpaceX and Nebius for Nvidia GB300 access through 2029 (summer 2026).

## Costs

API or per-token pricing: not specified in source. Cost claim is relative only ("3-4x less inference compute"), vendor-reported.

## Limits

- Text-only; no multimodal input. Inkling (Thinking Machines Lab, July 2026) is multimodal.
- Benchmarks are vendor-reported and not independently verified. Reflection says Beam beats Inkling on four coding tests where both report results; specific scores and benchmark names not in source.
- Reflection did not respond to TechCrunch requests for comment.

## Reception

- Framed as a Western answer to DeepSeek, Qwen and Z.ai (TechCrunch, 2026-10-05). Competes with closed labs (Anthropic, OpenAI) and Western open players (Mistral, Meta, Cohere, Thinking Machines).
- Company context: founded 2024 by two ex-Google DeepMind researchers, Brooklyn; ~$4.7B raised per PitchBook (Nvidia, Sequoia, Lightspeed); last round at $25B pre-money. Nvidia is both investor and beneficiary of the "AI factory" pitch *(editorial: Huang's open-ecosystem advocacy aligns with Nvidia's GPU demand)*.
- Practitioner or independent reception: none in source yet.

## Source

- `raw/research/weekly-2026-10-07/05-reflection-beam.md` (TechCrunch, 2026-10-05; cites Reflection blog "Introducing Beam" and Axios 2026-10-04)

## Related

- [[deepseek]]
- [[llm-api-enterprise-share]]
- [[ai-infrastructure-frontiers-2026]]
- [[openai-gpt56-sol-2026-06]]
- [[watchlist]]
