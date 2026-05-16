---
title: "Self-MoE: Towards Compositional LLMs with Self-Specialized Experts (MiXSE)"
arxiv: "2406.12034"
year: 2024
theme: moe-adapters
tags: [moe, lora, self-specialization, synthetic-data, routing, compositional-llm]
status: read
---

# Self-MoE: Towards Compositional LLMs with Self-Specialized Experts (MiXSE)

Kang et al. (2024) introduce **Self-MoE**, a pipeline that converts a monolithic LLM into **MiXSE** (MiXture of Self-specialized Experts) — a compositional system of lightweight LoRA experts, each built from *self-generated* synthetic data, orchestrated by a self-optimized router. No human-labelled data, no teacher model, no significant parameter overhead.

## Source

- arXiv: [2406.12034](https://arxiv.org/abs/2406.12034)
- Raw capture: `raw/research/moe-adapters/02-03-self-moe.md`

## Method

### Self-Specialization pipeline

Given a base LLM $\Theta_0$ and a small seed set (100 examples) per target domain $T_i$:

1. **Instruction brainstorming** — prompt $\Theta_0$ in-context on the seed to generate diverse new instructions.
2. **Response generation** — use seed pairs as few-shot demos; $\Theta_0$ produces responses for its own new instructions.
3. **Self-alignment with LoRA** — fine-tune $\Theta_0$ on the resulting synthetic corpus $D_i$ to produce expert delta $\Delta\Theta_i$.

Each LoRA expert is decomposed in the standard way. For a layer weight $\theta_0 \in \mathbb{R}^{d \times k}$:

$$\theta_{\text{spec}} = \theta_0 + \Delta\theta_i = \theta_0 + \theta_{B_i}\theta_{A_i}$$

with $\theta_{B_i} \in \mathbb{R}^{d \times r}$, $\theta_{A_i} \in \mathbb{R}^{r \times k}$, $r \ll \min(d, k)$. Only $\Delta\Theta_i$ is updated; $\Theta_0$ stays frozen. The full self-specialization step is:

$$f_{\text{ss}} : (\Theta_0, T_i) \to (\Delta\Theta_i, D_i)$$

### MiXSE: mixing the experts

After building $n$ expert deltas $\{\Delta\Theta_i\}_{i=1}^{n}$, MiXSE composites them at inference. Per-layer output:

$$h = \theta_0 x + \sum_{i=1}^{n} \alpha_i \Delta\theta_i x = \theta_0 x + \sum_{i=1}^{n} \alpha_i \theta_{B_i}\theta_{A_i} x$$

Router weights are computed by a single shared linear layer $\theta_r \in \mathbb{R}^{n \times k}$ with top-$k$ sparse selection:

$$\alpha = \operatorname{top-k}(\operatorname{softmax}(\theta_r x))$$

The router is trained *separately* from the experts, optimising:

$$\mathcal{L}(\theta_r) = -\mathbb{E}_{(\text{inst},\, \text{resp}) \sim D}\left[\log P_{\Theta_0}(\text{resp} \mid \text{inst};\, \theta_r,\, \{\Delta\Theta_i\}_{i=1}^{n})\right]$$

using the aggregated synthetic corpus $D = \{D_i\}_{i=1}^{n}$. Experts remain frozen during router training, preserving semantic distinctness — jointly training experts and router degrades performance (ablation).

The final compositional model is:

$$\Theta_{\text{comp}} = \Theta_0 \cup \{\Delta\Theta_i\}_{i=1}^{n}$$

### LoRA sizing

Each LoRA module contributes **< 0.3% of base parameters**; the router is negligible; total MiXSE overhead ≈ **1%** of base parameters. Main experiments: Gemma-7B base, 4 domains (knowledge, reasoning, math, coding), 5K synthetic samples per domain (20K total).

## Claims

- **+6.5%p average** over base LLM (Gemma-7B) across MMLU / BBH / GSM8K / HumanEval; from 47.8 → 54.3.
- MiXSE **outperforms all individual specialised models** on every domain — compositional synergy beats any single expert including the domain-matched one.
- Beats **instance merging** (multi-task tuning on same synthetic data: 52.4 avg), **TIES merging** (47.9), and **DARE merging** (44.3), all at same active parameter budget.
- Top-1 and Top-2 routing perform comparably; All-Experts routing underperforms (noise from irrelevant experts, higher overhead).
- **No forgetting** on out-of-expertise benchmarks (Hellaswag, PIQA, TruthfulQA, NaturalQuestions) — MiXSE ≈ base LLM; instance merging shows notable drops.
- Non-target in-expertise tasks (MATH, MBPP) also improve over base, suggesting generalisation.
- Generalises across five model families: LLaMA-2 7B & 13B, Mistral 7B, LLaMA-3 8B, Gemma-7B — all improved.
- Expert < 0.3% params each; total added ≈ 1%.

## Strengths / Novelty

- **No labelled data or teacher model.** Self-specialization uses $\Theta_0$ to generate its own training signal — the first fully self-contained MoE conversion pipeline.
- **Modular and composable.** Adding a new domain requires one additional LoRA train + router retrain; the base and other experts are untouched.
- **Interpretable routing.** Routing distributions align cleanly with task semantics (knowledge queries → knowledge expert, etc.), and cross-expert synergies are visible in routing weights.
- **Forgetting mitigation by design.** Because $\Theta_0$ is never modified, non-target capabilities are structurally preserved — unlike monolithic fine-tuning or weight merging.
- **Router training is cheap.** Optimising $\theta_r$ on the already-generated synthetic corpus costs negligibly more than expert training itself.

## Weaknesses / Limits

- **Single-specialised monolithic models do degrade on non-targets.** The paper reports this explicitly: Knowledge Self-Spec. drops reasoning from 56.1 → 41.7 and coding from 34.1 → 28.0. MiXSE recovers this, but it confirms over-specialisation is a real failure mode.
- **Seed data still required.** 100 seed examples per domain are needed; the method is not zero-shot from scratch.
- **GSM8K not beaten by MiXSE vs instance merging** (52.5 vs 53.5). Dynamic routing does not uniformly dominate; multi-task tuning can match or slightly exceed on individual metrics.
- **Router trained on self-generated data.** If the synthetic distribution is narrow or systematically biased, routing quality degrades — the method depends on brainstorming coverage of the target domain.
- **Token-level routing (not example-level).** The router activates per-token, per-layer — implementation complexity and memory overhead scale with $n$ experts active simultaneously.
- Evaluated only at 7–13B scale. Behaviour at very small or very large scale is unknown.

## Relevance to this wiki's project

MoERA's goal is to convert a dense model into an MoE using **delta-LoRA experts without labelled data**. Self-MoE is the closest prior art:

| Dimension | Self-MoE | MoERA target |
|---|---|---|
| Expert type | LoRA deltas | LoRA deltas |
| Data source | Self-generated synthetic | Self-generated / single-sample |
| Base model frozen | Yes | Yes |
| Router | Learned linear, token-level | TBD |
| Labelled data required | No (100 seeds) | No |

Self-MoE's **self-specialization pipeline** (brainstorm → generate → align) is directly reusable as an expert-construction recipe for MoERA domains. Its demonstration that **synthetic data alone suffices to produce semantically distinct, composable LoRA experts** is the key empirical result this wiki needs. The failure mode — monolithic specialisation degrades non-targets — further motivates the modular MoERA architecture as a forgetting-robust alternative to standard LoRA fine-tuning.

Connection to single-sample themes: if seed construction can be reduced from 100 examples to 1 (or generated on-the-fly from a single input), Self-MoE becomes a direct single-sample behaviour-installation method — see [[../synthesis/proposed-method]] for how this links to $R_w$.

## Connections to the wiki

- [[_overview]] — Self-MoE is the primary "convert dense → MoE with self-data" reference in the theme.
- [[loramoe]] — earlier LoRA-MoE work requiring labelled data; Self-MoE removes that dependency.
- [[mov-molora]] — alternative MoV/MoLoRA designs; compare token-level routing strategies.
- [[btx]] — Branch-Train-MiX: expert specialisation via data-parallel branch training (requires labelled domain splits); Self-MoE replaces labelled splits with synthetic data.
- [[sparse-upcycling]] — upcycles a dense checkpoint into a sparse MoE; Self-MoE avoids full architecture change.
- [[mole]] — MoLE: mixture-of-LoRA-experts with task-specific routing; compare to MiXSE's self-optimized router.
- [[moram]] — MoRAM: another LoRA-based MoE variant; architectural alternative to MiXSE.
- [[../self-improvement/star]] — STaR: bootstrap reasoning via self-generated rationales. Self-MoE's synthetic data construction is structurally analogous — the model generates its own training signal; the key difference is STaR targets a single reasoning skill, Self-MoE targets compositional multi-domain specialisation.
- [[../selective-finetuning/_overview]] — selective fine-tuning methods are complementary; MiXSE's modularity is a structural alternative to parameter-selective updating within a monolithic model.
- [[../synthesis/proposed-method]] — $R_w$ in the proposed method calls for compositional self-specialised experts as a behaviour-installation route; Self-MoE is the proof-of-concept that self-specialised LoRA experts can be built without labelled data.
- [[../catastrophic-forgetting/_overview]] — Self-MoE is a strong empirical case study: modular expert design with frozen base nearly eliminates forgetting on out-of-expertise tasks, in contrast to monolithic specialisation.

## Related

- Self-Specialization (Kang et al., 2024) — direct precursor; single-expert variant of the same pipeline.
- TIES Merging (Yadav et al., 2023); DARE (Yu et al., 2024) — static weight-merging baselines MiXSE outperforms.
- BTM (Li et al., 2022); Sparse Upcycling (Komatsuzaki et al., 2023); BTX (Sukhbaatar et al., 2024) — compute-intensive MoE construction methods cited as indirect comparison.
- LoRA (Hu et al., 2022) — adapter foundation for all expert modules.
