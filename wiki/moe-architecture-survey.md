# The Evolution of Mixture-of-Experts Architectures in LLMs

Solo-authored (Codex-assisted) technical survey (arXiv:2608.08650, Aug 2026). Reframes MoE architecture history not as a chronological model list but as bottleneck migration across eight dependency-graph milestones, analyzed through four orthogonal "control planes" — Topology, Routing, Balance, Expert Parallelism. Reference/framework page: other MoE-touching pages in this wiki should link here for shared vocabulary (Top-k, ALF, device-limited routing, ultra-sparse scaling) rather than re-explaining it per page.

## Method

Not a novel training method — an organizing framework, two complementary lenses:

**Eight evolutionary milestones** (dependency graph, not strict generations): (1) Jacobs et al. 1991 dense/soft MoE — statistical division of labor without sparsity; (2) Shazeer 2017 noisy Top-k — decouples total capacity from active FLOPs; (3) GShard/Switch/ST-MoE — Expert Parallel + All-to-All execution contract on Transformers; (4) Mixtral — proves coarse-grained MoE viable end-to-end in open-weight decoder LLMs; (5) DeepSeekMoE/V2 — fine-grained experts + shared-expert isolation + device-limited routing; (6) PEER/Kimi K2/gpt-oss — ultra-sparse scaling (more experts at fixed active budget); (7) LongCat-Flash zero-compute-expert slots — dynamic/token-dependent compute budget; (8) four orthogonal frontier branches decoupling semantic routing from physical execution: ScMoE (cross-layer shortcut hides dispatch/combine latency), MoHGE (heterogeneous expert width via two-level routing), GMoE (cross-layer global experts), Multi-Head LatentMoE/Head Parallel (O(1) structured communication independent of k).

**Four control planes**, formalized as a closed loop: Topology (ℰ = T(θ_topo)) → Routing (K_t = R(x_t, ℰ; θ_route, b)) → Balance (aggregate-load feedback via loss/bias/capacity) → Expert Parallel (dispatch/combine execution under placement π and schedule σ), with feedback edges (loss/bias/capacity → routing; placement/replication → EP).

## Results

No new experiments. Proposes an equal-budget ablation matrix (fix total/active params and tokens while scanning expert granularity, shared-vs-emergent, balance scope, execution topology, dynamic compute, upcycling) and a synthesis table of published systems:

| Model | Total / Active | Experts (Top-k) | Notes |
|---|---|---|---|
| GShard | >600B | Top-2 | |
| Switch | up to 1T+ | Top-1 | |
| Mixtral 8×7B | 46.7B / 12.9B | 8 / 2 | |
| DeepSeek-V2 | 236B / 21B | 160 / 6 | |
| DeepSeek-V3 | 671B / 37B | 256 / 8 | Auxiliary-Loss-Free balancing |
| Qwen3-235B-A22B | 235B / 22B | 128 / 8 | no shared expert |
| Kimi K2 | 1.04T / 32.6B | 384 / 8 | |
| gpt-oss-120b | 116.8B / 5.1B | 128 / 4 | |
| LongCat-Flash | 560B / 18.6–31.3B active | real + zero-compute slots | |
| LongCat-2.0 | 1.6T / 33–56B | dynamic, per-core dense/MoE parallel | |

Explicitly flags that cross-model benchmark comparisons in the literature are not causally comparable (different data/tokens/optimizers/eval pollution control).

## Applicability

Reference material, not a directly implementable technique. Useful for: (a) anyone designing or evaluating a new MoE architecture, as a checklist of the six design axes and the proposed equal-budget ablation protocol; (b) anyone auditing an existing MoE training/serving stack for system-level bottlenecks (exposed vs. total All-to-All time, MFU, P99 latency, token/expert ratio at high sparsity).

## Novelty

A recombination/organizing framework, not a new architecture or method. Genuine contribution: separating a historical "bottleneck migration" timeline from a synchronic "control plane" decomposition, argued as complementary views. Names/consolidates several 2026 frontier items not yet gathered elsewhere: MoHGE (ACL Industry Track 2026), GMoE (ACL 2026), Multi-Head LatentMoE + Head Parallel (arXiv:2602.04870), Expert Upcycling (arXiv:2604.19835, extending dense→MoE upcycling to smaller-MoE→larger-MoE). Closest prior work: Cai et al. 2024 full-stack MoE taxonomy (arXiv:2407.06204); this survey's differentiator is the bottleneck-migration/control-plane framing plus coverage through mid-2026 releases.

## Reproducibility

No code or released artifacts (survey/synthesis paper). All claims attributed to 34 cited primary sources, each independently verifiable on its own terms.

## Adoption

Too recent (single-author Aug 2026 preprint) for external citation signal. Notable as a mid-2026 checkpoint treating Kimi K2, gpt-oss, Qwen3, LongCat-Flash/2.0, and DeepSeek-V3's Auxiliary-Loss-Free balancing as the current mainline consensus: token-choice Top-k + fine-grained experts + optional shared path + global/batch-wise balance (or ALF) + topology-limited routing + dropless kernels/communication overlap + runtime expert placement.

## Conflicts

No contradiction of existing wiki claims. Calibration note: the survey's Table 6 stops at DeepSeek-V3 (671B/37B, 256 experts/Top-8) and predates [[deepseek-v4]]'s DeepSeek-V4-Pro (1.6T total/49B active, hybrid CSA+HCA attention, mHC residuals) — a currency gap, not a factual conflict. The survey's claim that "DeepSeek-V3 has no balance loss at all" is imprecise (V3 uses batch-wise ALF plus a weak sequence-wise auxiliary loss) but doesn't contradict anything the wiki currently asserts.

## Source

- `raw/research/weekly-2026-08-29/03-moe-architecture-survey.md` — arXiv:2608.08650. Captured 2026-08-29.

## Related

- [[deepseek-v4]] — the wiki's flagship MoE model; this survey's milestones 5–6 (DeepSeekMoE → DeepSeek-V2 fine-grained+shared+device-limited routing, DeepSeek-V3's ALF balancing) are the direct architectural lineage V4-Pro extends.
- [[manifold-constrained-hyper-connections]] — DeepSeek mHC (Sinkhorn-Knopp residual mixing) operates orthogonally to the four control planes catalogued here (residual stream, not routing/balance/topology/EP), but is co-deployed in DeepSeek-V4-class models.
- [[kimi-k3]] — another large open-weight MoE exemplar (successor to Kimi K2, tabulated here) this survey's taxonomy applies to.
- [[watchlist]] — Fisher-MoE entry should be checked against this survey's milestone/control-plane taxonomy (likely Balance or Topology plane) when promoted off the watchlist.
