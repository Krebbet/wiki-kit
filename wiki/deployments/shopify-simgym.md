# Shopify SimGym

Shopify Engineering case study (April 2026) on **SimGym** — a production system that runs up to 2,000 concurrent cloud-browser shopper bots against a merchant's storefront to deliver simulated A/B test results in minutes rather than weeks. The substantive content is on the *serving infrastructure* underneath: a self-hosted 120B MoE (`gpt-oss-120b`) on 48 dedicated NVIDIA B200 GPUs (CentML), a Browserbase-backed pool of cloud Chromium sessions, and an extensive sequence of inference-side optimizations (MIG partitioning, EAGLE-3 speculative decoding, prompt-cache prefix restructuring, Blackwell-specific kernels). Today: ~400,000 shopping sessions/day, single-digit cost per merchant run and falling. The page belongs to the wiki as a concrete enterprise deployment of *agent-based simulation as a substitute for live traffic A/B testing*, with serving-economics detail rare in agent literature.

## Source

- `raw/research/weekly-2026-04-27/03-04-shopify-simgym.md` — captured 2026-04-27 from `https://shopify.engineering/simgym`.

## Architecture

Two tightly-coupled clusters:

- **Browserbase** runs up to 2,000 concurrent isolated Chromium sessions. No mocked DOM, no shortcuts — the bot sees the actual rendered page.
- **Shopify inference cluster** (CentML, 48 NVIDIA B200 GPUs) runs `gpt-oss-120b`, a 120B MoE with effective active compute around 15–20B dense.

Per-bot loop, repeated 10–13 times per session:

1. Browserbase sends page state.
2. Model receives a one-sentence system prompt + buyer profile (persona, intent, budget) + accumulated memory + a representation tree of the current page (3,000–15,000 tokens depending on storefront complexity).
3. Model returns a JSON action (`{"action", "nodeSelector", "method"}`).
4. Browserbase executes it.

> "Browserbase bills per minute. The model needs seconds to think. That coupling is the central tension: inference latency is operational cost."

94% of all tokens in this workload are *input* tokens — the page representation tree dominates.

## Model evolution

| Phase | Model | Outcome |
|---|---|---|
| Bootstrap | GPT-4o | 75/100 buyers completed task (first-gen baseline). |
| Capability scale-up | GPT-5 | Better task completion but unsustainable per-token cost at hundreds of thousands of sessions/day. |
| Production | `gpt-oss-120b` (self-hosted, 48 B200 + Notte browser framework) | Session times dropped from 15+ minutes to under 3. Predictable cost; fine-tune potential preserved. |
| Candidate (next) | Qwen3-32B finetuned on 16 H200s on Nebius | Under evaluation. |

Self-hosting was the decisive choice: per-token cost under hosted GPT-5 did not scale to ~400k sessions/day.

## Inference-side optimizations

- **Blackwell migration (B200 vs H200):** **57K vs 11K tokens/sec per GPU — 5.2× speedup.** MXFP4 quantization for expert weights, FP8 KV-cache, custom FlashInfer kernels. vLLM PR #28000 fixed bugs that surfaced only under agentic load shapes.
- **MIG partitioning:** Splitting each B200 into two instances cut average LLM latency ~20% (27.8s → 21.9s), session duration 7.3 → 6.6 min, daily throughput 1,311 → 1,463 merchant runs. Tradeoff: the speculative-decoding draft model will not fit alongside the main model in MIG mode, so MIG is mutually exclusive with EAGLE-3 today.
- **EAGLE-3 speculative decoding** (`nvidia/gpt-oss-120b-Eagle3-throughput`): exploits the high predictability of structured JSON output. +6% throughput at 100–200 concurrent sessions in benchmarks; production deployment pending. The three-way integration of async scheduling + guided decoding + speculative decoding landed in vLLM PR #29821.
- **Prompt-cache prefix restructuring:** Moving dynamic elements (persona, intent) outside the shared cache prefix yielded ~12% throughput increase at concurrency >1,000 and meaningful TTFT improvements.
- **Reasoning-effort ablation:** Lowering reasoning effort cut session duration ~75% but raised error rates from 0.5–0.75% baseline to 4.5–10.9%. The post explicitly concludes "not worth it" — a useful counterweight to "just run smaller / cheaper" arguments in agent serving.

A ~20% reduction in average LLM latency across these levers cut cost per merchant run ~10% and raised daily throughput ~12%.

## Operational scale and cost

- **~400,000 shopping sessions/day.**
- **Cost per merchant run: single digits and falling.**
- **Standard error rate: 0.5–0.75%.**

## Why it lands here

- **Agent-based simulation as eval.** Where [[airs-bench]] and [[swe-bench-pro]] evaluate agents on benchmark tasks, SimGym uses agents *as the eval substrate itself* — bots stand in for human shoppers, and the system answers a merchant's question ("did this storefront change improve conversion?") that traditional A/B testing answers more slowly with real humans. This is a third evaluation paradigm distinct from offline benchmarks and live A/B.
- **"Embarrassingly parallel" multi-agent topology.** Unlike [[cognitive-fabric-nodes]] (coordination-heavy multi-agent), SimGym's 2,000 concurrent bots are independent but correlated by traffic shape. The serving stack is the only shared state.
- **Inference-economics detail rare in agent literature.** Most agent papers do not disclose per-GPU throughput, MIG vs speculative-decoding tradeoffs, or cache-prefix restructuring numbers. Capture this as a benchmark for what production-scale agent serving actually requires.
- **Phase-2 evidence point for [[cognition-cloud-agents]].** The Cognition piece argues enterprise agent deployment requires both infrastructure investment and process redesign; SimGym is one shape of "process redesign" — moving an experimentation function (A/B testing) onto a synthetic-traffic substrate.

## Caveats

- Reliability and hallucination handling are not discussed explicitly. The 0.5–0.75% error rate is reported but the failure-mode taxonomy is absent.
- The performance summary table referenced in the post (asset `9a5cd4abf5ac962c.png`) is an image; specific per-stage latency/cost numbers in that table were not extractable from the captured markdown narrative.
- Shopify is a vendor primary source; numbers are not third-party validated.

## Related

- [[airs-bench]] — agent eval on autonomous research; SimGym is agent eval on simulated retail. Both surface the gap between standard benchmarks and real agentic traffic shapes.
- [[topology-taxonomy]] — adds an *embarrassingly-parallel correlated-traffic* entry to the multi-agent topology axis.
- [[anthropic-internal-study]] — engineer-side enterprise deployment data; SimGym is customer-facing simulation throughput economics. Pair as two enterprise vantage points.
- [[willison-cognitive-cost]] — Willison's "wiped out by 11am" and SimGym's inference-latency-as-cost are two sides of the same agent-economics pressure.
- [[cognitive-fabric-nodes]] — contrast topology: coordination-heavy multi-agent vs SimGym's correlated-but-independent agents.
- [[paperorchestra]] — multi-agent simulation pipeline at production scale in a different domain (academic writing); parallel architectural concerns.
- [[cognition-cloud-agents]] — Phase-2 process-redesign framing applies; SimGym replaces a traditional experimentation process with an agent-driven one.
