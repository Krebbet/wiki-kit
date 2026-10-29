# doubleAI (Maxwell)

Tel Aviv startup (officially AA-I Technologies Ltd., CEO Amnon Shashua, Mobileye co-founder) that debuted Maxwell on 2026-10-19: a "code execution model" that optimizes compiled binaries to cut CPU/GPU usage, sold to enterprises trying to lower AI-workload hardware spend. Announced with a funding round backed by Nvidia and Dell (2026-10-19). Watch, do not buy yet: every performance figure is vendor-reported and unverified, and no pricing or delivery model exists as of 2026-10-19.

## Offering (2026-10-19)

- **Product:** Maxwell. Primary use is making software more efficient; secondary showcases are math proofs and chess search.
- **Technique:** analyzes how a program interacts with its data and the underlying chips, then applies optimizations to the binary, not the source. Supports GPUs and CPUs. Vendor claims this removes manual source changes and allows modifying applications while running in production (unverified).
- **Math agent:** a doubleAI agent produced an extremal-graph-theory result (early 2026-10) paired with a Lean-verifiable proof. Verification is cheap by construction; the novelty claim is still vendor-stated.
- **Deployment, customization, pricing:** not stated in the captured source. Delivery form (API, service, on-prem) unknown.
- **Hard limits:** not addressed by the vendor.

## Vendor-claimed benchmarks (unverified)

No independent benchmarks are cited in the captured source. All figures come from doubleAI posts as relayed by SiliconANGLE (2026-10-19).

| Claim | Date | Note |
|---|---|---|
| Rewrote Nvidia cuGraph; 55% of library algorithms sped up 2x or more | 2026-03 | Vendor-reported, unverified |
| Optimized pandas; 38x on PDS-H query benchmark | undated in source | Vendor-reported, unverified |
| Doubled video-generation speed of LTX-2.5 world model | recent, undated | Vendor-reported, unverified |
| Chess position with 63 consecutive checking moves (prior record 60, ~50 years old) | 2026-10 | Showcase, unrelated to the enterprise product |

The cuGraph and pandas rewrites are benchmark-visible OSS targets, which makes them checkable by third parties. No such check is cited yet.

## Funding

As captured (SiliconANGLE, 2026-10-19): "backed by $220 million in funding from Nvidia, Dell and others"; CTech reports a valuation above $1B. The URL slug and headline say a $200M round. No lead investor is named. The $220M versus $200M gap is unresolved within the source (likely cumulative backing versus the round itself; not confirmed). WSJ (via SiliconANGLE) reports plans to buy 1,000 Nvidia B300 GPUs.

### Reconciliation note

Per other outlets (SiliconANGLE, Globes, Dealroom), not in the captured source:

- Round: $200M Series A, announced 2026-10-19.
- Valuation: above $1B.
- Lead: Lightspeed; some outlets say Lightspeed plus Bessemer. Unresolved.
- Participants: Nvidia and Dell Technologies Capital.
- Compute: about 1,000 B300 GPUs purchased.
- Pricing: savings-share model (vendor takes a share of realized compute savings).
- Customer claim: 67% compute savings for one early customer (vendor-claimed, unverified).

Treat the savings-share pricing and 67% figure as unconfirmed until a primary vendor source is captured. Flag for a ruling if the lead-investor disagreement matters.

## Read

- Pitch is compute-efficiency tooling as a purchasable category; it overlaps the cost-pressure theme in [[landscape/agentic-compute-pricing-2026-04]] and [[landscape/ai-infrastructure-frontiers-2026]].
- Capability-showcase funding pattern is comparable to [[startups/ndea]] and [[startups/confluence-technologies]]; the Nvidia-ecosystem angle compares to [[landscape/groq-nvidia-acquihire-2026-06]].
- WSJ frames it as competing with OpenAI and Anthropic on research automation. The chess and math items support that framing, not the binary-optimization product.
- Evidence is thin: secondary trade press only, no practitioner or customer feedback.
- Worth stealing: post-compile optimization with no source changes; Lean-paired proofs for cheap verification; OSS rewrites as public proof.

## Source

- raw/research/weekly-2026-10-28/01-doubleai-200m-series-a.md (SiliconANGLE, 2026-10-19; relays CTech and WSJ)
- raw/research/weekly-2026-10-28/.ingest/01-doubleai-200m-series-a.summary.md

## Related

- [[landscape/ai-infrastructure-frontiers-2026]]
- [[landscape/agentic-compute-pricing-2026-04]]
- [[landscape/groq-nvidia-acquihire-2026-06]]
- [[startups/ndea]]
- [[startups/confluence-technologies]]
- [[llms/openai]]
- [[llms/anthropic-claude-family]]
