# OpenAI Jalapeño Custom Inference Chip (2026-06)

OpenAI unveiled Jalapeño on 2026-06-24 — its first custom inference processor, designed with Broadcom and co-developed using OpenAI's own AI models. Still in testing, early results show "significantly better performance-per-watt" (vendor claim) than current alternatives; the chip targets real-time coding inference workloads specifically.

## Background

OpenAI's partnership with Broadcom was formally announced in October 2025, though custom-chip ambitions had been rumored for years as a hedge against Nvidia GPU dependence. Google (TPU) and Amazon (Trainium/Inferentia) both pursued the same trajectory; Jalapeño positions OpenAI to follow.

## Design intent

Jalapeño is inference-only. Pre-training remains on Nvidia hardware. OpenAI's rationale (per Greg Brockman, 2026-06-24): target underserved inference workloads where a purpose-built chip can outperform general-purpose GPU silicon on cost and efficiency. Low operating cost for coding-model inference is the stated priority.

## Stack integration

OpenAI frames Jalapeño as one layer of a vertical integration play — chip architecture, kernels, memory systems, networking, scheduling, deployment, and product experience all optimized toward the same objective: faster, cheaper, more reliable model serving. This is a departure from pure-cloud-consumer positioning toward infrastructure ownership.

## Status

- Chip announced: 2026-06-24
- Phase: testing (not yet in production serving)
- Pre-training dependency on Nvidia unchanged
- No published benchmark figures beyond the performance-per-watt claim

## Source

- Capture: `raw/research/weekly-2026-06-24/01-openai-jalape-o-chip-2026.md`
- URL: https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/

## Related

- [[llms/openai]] — OpenAI model and platform family; inference cost structure
- [[landscape/openai-microsoft-restructure-2026-04]] — Microsoft/OpenAI partnership context; infrastructure ownership implications
- [[landscape/ai-infrastructure-frontiers-2026]] — Bessemer thesis on inference-at-scale; vertical integration patterns
- [[landscape/agentic-compute-pricing-2026-04]] — inference cost pressure from agent workloads; Jalapeño directly addresses this
