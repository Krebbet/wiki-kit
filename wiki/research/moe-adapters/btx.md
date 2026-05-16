---
title: "Branch-Train-MiX (BTX): Mixing Expert LLMs into a Mixture-of-Experts LLM"
arxiv: "2403.07816"
tags: [moe, expert-training, parallel-training, skill-stacking, continued-pretraining]
theme: moe-adapters
---

# Branch-Train-MiX (BTX): Mixing Expert LLMs into a Mixture-of-Experts LLM

Singhal et al. (Meta FAIR, 2024) propose BTX, a three-stage recipe that converts a dense seed LLM into a Mixture-of-Experts model by training domain experts embarrassingly in parallel, then mixing their FFN sublayers into a single MoE and router-finetuning the result. The core contribution: expert skills are acquired with **zero gradient interference** between domains, then unified into a single inference-efficient model via a short MoE finetuning phase. BTX outperforms its seed (Llama-2 7B), larger generalist (Llama-2 13B), and specialized models (CodeLlama 7B, Llemma 7B) on most tasks while using less compute than monolithic continued pretraining.

## Source

- arXiv: [2403.07816](https://arxiv.org/abs/2403.07816)
- Raw capture: `../../../raw/research/moe-adapters/03-04-btx.md`

## Method

### Stage 1 — Branch

Initialize $N$ copies of a pretrained seed model $M$. Each copy $M_i$ is assigned a domain dataset $D_i$ (math, code, Wikipedia, …). The seed itself is kept as a "generalist" expert $M_0$.

### Stage 2 — Train (embarrassingly parallel)

Each $M_i$ is continued-pretrained on $D_i$ independently, using the standard causal language-modeling objective. No synchronization across workers; no all-to-all communication. Throughput scales linearly with $N$. A single worker failure affects only one expert rather than halting the full job.

Experiment: three domain experts (math: 201B tokens, code: 210B tokens, Wikipedia: 42B tokens) + the seed as a fourth generalist. Total: four expert LLMs.

### Stage 3 — MiX

**Combine FFN sublayers into MoE.** At each Transformer layer $l$, the feedforward sublayers $\mathrm{FF}^l_i$ from all $N$ experts become the MoE experts:

$$\mathrm{FF}^l_{\mathrm{MoE}}(x) = \sum_{i=1}^{N} g_i(W^l x)\, \mathrm{FF}^l_i(x)$$

where $W^l$ is a learned linear router and $g$ is a sparse gating function. Default: Top-2 routing, $g(W^l x) = \mathrm{SoftMax}(\mathrm{TopK}(W^l x))$ with $k=2$.

**Average all other parameters.** Self-attention weights, embeddings, and norms are initialized to the element-wise mean across all $N$ expert checkpoints. The motivation: attention is less domain-specialized than FFN.

**Router finetuning.** The merged MoE model is finetuned on the union of all training data for 80B tokens. The only new parameters are the router matrices $W^l$ (negligible in total count). Freezing the expert FFNs during this stage shows minimal performance impact, confirming that domain knowledge is already encoded after Stage 2.

**Variants explored:** load-balancing loss $L_{LB} = \alpha N \sum_i u_i p_i$; Switch (Top-1), soft routing (all experts active), Sample Top-1 (Gumbel); expert splitting (chunk each FFN into $C$ pieces for $NC$ total modules); expert blending (interleave chunks across domains).

## Claims

- **+18.8 pp math** (GSM8K + MATH average): BTX Top-2 scores 27.4 vs. Llama-2 7B seed at 8.6 (Table 2).
- **+17.2 pp code** (HumanEval + MBPP average): BTX 34.0 vs. seed 16.8.
- **+3.6 pp knowledge** (NaturalQ + TriviaQA): BTX 41.0 vs. seed 37.4.
- **Beats Llama-2 13B** on all tasks except reasoning, using $<$50% of the additional training compute.
- **Beats CodeLlama 7B** on average (BTX 47.9 vs. CodeLlama 37.9) while also retaining general knowledge where CodeLlama degrades.
- **Beats Llemma 7B** on average (BTX 47.9 vs. Llemma 32.1); Llemma suffers catastrophic forgetting on non-math tasks.
- **Beats BTM** (same experts, no router finetuning) by 4.5 pp average, demonstrating the value of learned token-level routing over input-level domain classification.
- **More compute-efficient than sparse upcycling (CM):** same GPU-day budget, BTX trains 2× more tokens (533B vs. 252B) and achieves 47.9 vs. 47.3 average, with more balanced domain coverage (Table 3).
- **Routing analysis:** without load balancing the math expert dominates and the code expert becomes a dead expert. Load balancing revives the code expert and improves coding tasks at a small cost to math.

## Strengths / Novelty

- **Embarrassingly parallel, asynchronous expert training.** No inter-worker communication during the main training phase. Linear throughput scaling with $N$. A single hardware failure does not cascade.
- **No inter-skill gradient interference by construction.** Each expert is trained on its own data in isolation; skills are combined structurally (via FFN assignment to MoE slots) rather than via gradient mixing. This is categorically different from multi-task continued pretraining.
- **Unified model with full downstream compatibility.** Unlike BTM (a model ensemble), the BTX output is a standard MoE LLM amenable to SFT, RLHF, or any other finetuning.
- **Minimal router overhead.** Only the $W^l$ matrices are new; active-parameter count at inference is comparable to the dense seed model (Top-2 of 4 experts activates ~11B parameters for a 7B-per-expert model).
- **Skill isolation survives MoE finetuning.** Domain routing partially persists after finetuning: code and Wikipedia tokens preferentially route to their respective experts.

## Weaknesses / Limits

- **Restricted to continued pretraining.** All experiments are at the pretraining stage; no SFT or RLHF experiments are reported. Extension to instruction or RL finetuning is left as future work.
- **Fixed expert count = domain count.** The number of MoE slots is tied to the number of training domains. Expert splitting and blending variants both underperform the direct one-to-one mapping, limiting flexibility in expert granularity.
- **Attention averaged, not specialized.** Averaging attention weights is a heuristic. For domains with strongly divergent attention patterns this may discard useful structure.
- **Small $N$ tested.** Only 4 experts (3 domain + 1 generalist). The embarrassingly parallel scaling argument is theoretically appealing but untested at $N \gg 4$.
- **No unsupervised domain discovery.** Domains are manually specified. Scalable application requires domain detection (cf. Gururangan et al., 2023) as a prerequisite.
- **Router sensitivity to load balancing.** Without load balancing, a dead-expert failure mode emerges. The balance coefficient $\alpha$ is a tunable hyperparameter with non-trivial domain-performance tradeoffs.

## Relevance to this wiki's project

BTX is the clearest existence proof that **skills can be stacked without zero-sum gradient reallocation**. The user's problem — adding a new concept to a model already holding other skills — is a miniature instance of the multi-domain stacking problem BTX solves. Two direct implications:

**1. Structural interference elimination as a design principle.** BTX achieves interference-free skill acquisition by training experts in separate compute graphs, then combining parameters structurally. For MoERA (dense → MoE with delta adapters), BTX suggests: the delta $\Delta W$ for a new concept should be routed as a new MoE expert rather than blended into existing FFN weights. A new-concept adapter $\Delta W_{\text{new}}$ added as an expert FFN slot in existing MoE layers is the direct analogue of BTX's branch step applied to finetuning rather than pretraining.

**2. Independence sidesteps the interference the project is worried about.** Monolithic RLVR stacking (single model, rewards for multiple skills) subjects all skills to simultaneous gradient pressure; improved performance on one skill can degrade another via implicit KL drift (cf. [[../rlvr-mechanics/deepseekmath-grpo]]). BTX shows the alternative: train independently, combine structurally. For $R_w$ in [[../synthesis/proposed-method]], this suggests an expert-per-concept reward architecture rather than a summed multi-task reward on a shared model.

**Contrast with RFT-based stacking:** [[../catastrophic-forgetting/rft-mitigates-forgetting]] demonstrates that slow, data-efficient finetuning can preserve prior skills within a single model. BTX takes the orthogonal position: don't co-train at all. Both are valid answers to forgetting — BTX's answer is structural and scales with compute; RFT's answer is regularization-based and may be more practical when a full parallel training budget is not available.

## Connections to the wiki

- [[_overview]] — BTX is the primary "parallel expert → MoE" recipe in the moe-adapters theme.
- [[sparse-upcycling]] — BTX's dense→MoE ancestor; BTX adds the embarrassingly parallel branch-train step that sparse upcycling omits.
- [[loramoe]] — LoRA-gated MoE at the adapter level; BTX operates on full FFN weights rather than low-rank deltas.
- [[mov-molora]] — MoV/MoLoRA explore soft vs. sparse routing; routing ablations in BTX (Table 4) reach similar conclusions about Top-2 vs. Switch vs. soft.
- [[self-moe]] — self-MoE constructs experts from the base model via self-specialization; BTX uses external domain data instead.
- [[mole]] — MoLE combines LoRA experts with learned weights; BTX is the full-parameter analogue.
- [[moram]] — MoRAM mixes adapter modules for multitask; BTX's MiX stage is structurally related but operates on pretrained domain experts rather than task adapters.
- [[../catastrophic-forgetting/rft-mitigates-forgetting]] — RFT retains skills by slowing updates within a shared model; BTX retains them by never co-training in the first place. Two answers to the same constraint.
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC regularizes shared weights to prevent forgetting; BTX avoids the need for regularization by isolating weights structurally. BTX is the "hard" version of what EWC does "softly".
- [[../selective-finetuning/_overview]] — BTX's domain-specific expert FFNs implement a form of hard parameter isolation across skills; the selective-finetuning theme explores the same principle via masking and orthogonal subspaces.
- [[../synthesis/proposed-method]] — $R_w$ and the delta-adapter framing; BTX suggests expert-per-concept rather than shared-model gradient accumulation.

## Related

- [[_overview]]
- [[sparse-upcycling]]
- [[loramoe]]
- [[mov-molora]]
- [[self-moe]]
- [[mole]]
- [[moram]]
- [[../catastrophic-forgetting/rft-mitigates-forgetting]]
- [[../catastrophic-forgetting/ewc-gemma2-cpt]]
- [[../selective-finetuning/_overview]]
- [[../synthesis/proposed-method]]
