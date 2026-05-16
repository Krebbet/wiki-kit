---
name: loramoe
description: MoE-style plugin that replaces FFN linear layers with N LoRA experts gated by a learned router; frozen backbone + Localized Balancing Constraint keeps a designated expert subset anchored to world knowledge while others specialise on downstream tasks (ACL 2024).
type: research
---

# LoRAMoE: Alleviating World Knowledge Forgetting via MoE-Style Plugin

Dou, Zhou, Liu et al. (Fudan University / Hikvision; ACL 2024) diagnose a concrete failure mode: scaling SFT instruction data from 100 K to 3 M samples reliably collapses closed-book QA performance on TriviaQA and NQ while improving every other downstream task — a diverging trend that two-stage fine-tuning cannot reverse because the world knowledge has been irreversibly damaged. Their fix is **LoRAMoE**: swap each FFN linear layer for an MoE-style plugin of $N$ LoRA experts, freeze the backbone entirely, and enforce a *Localized Balancing Constraint* (LBC) during training so that a designated subset of experts remains specialised in world-knowledge retrieval while the rest handle downstream tasks. The router at inference requires no data-type annotation — it routes automatically. For this wiki, LoRAMoE is the closest published analogue to the user's **MoERA** design (delta-LoRA experts + router over a frozen backbone) and provides the first explicit routing-based answer to the skill-forgetting problem that the proposed method must also solve.

## Source

- arXiv: 2312.09979 — ACL 2024
- Raw markdown: `raw/research/moe-adapters/01-01-loramoe.md`

## Method

**Architecture.** For a standard FFN forward pass $f(x) = x + f_{\text{FFN}}(x)$, the linear projection is $o = W_0 x + \Delta W x$. LoRAMoE replaces $\Delta W$ with $N$ LoRA experts $\{E_i\}_{i=1}^N$ gated by a soft router:

$$o = W_0 x + \sum_{i=1}^{N} G(x)_i \, E_i(x), \quad G(x) = \text{Softmax}(x W_g)$$

Each expert's update matrix is low-rank: $\Delta W_{E_i} = B_i A_i$ with $A_i \in \mathbb{R}^{d_{\text{in}} \times r}$, $B_i \in \mathbb{R}^{r \times d_{\text{out}}}$, $r \ll \min(d_{\text{in}}, d_{\text{out}})$. Including the LoRA scaling constant $\alpha/r$, the full LoRAMoE layer output is:

$$o = W_0 x + \frac{\alpha}{r} \sum_{i=1}^{N} \omega_i \cdot B_i A_i x$$

where $\omega_i$ is the router weight for expert $i$. Only the experts $\{A_i, B_i\}$ and the router matrix $W_g$ are trained; $W_0$ is frozen throughout.

**Localized Balancing Constraint (LBC).** Unconstrained training collapses to a few dominant experts (coefficient of variation $\approx 3$, same collapse as Shazeer et al. 2016). Standard CV-based balancing assumes a single data distribution and is therefore inappropriate when the mixture contains both world-knowledge QA and downstream task data.

LBC introduces a per-expert, per-sample importance matrix. Let $Q_{n,m}$ be the sum of router weights for expert $n$ over all tokens of sample $m$:

$$Q_{n,m} = \sum_{j=1}^{T_m} G(x_j)_n = \sum_{j=1}^{T_m} \frac{\exp(\omega_n^j / \tau)}{\sum_{k=1}^{N} \exp(\omega_k^j / \tau)}$$

Define a coefficient matrix $\mathbf{I}$ of the same shape, where entry $I_{n,m}$ boosts or suppresses the importance of expert $n$ on sample $m$ depending on whether the expert's pre-assigned type matches the sample's task type:

$$I_{n,m} = \begin{cases} 1 + \delta & \text{if } \text{Type}_e(n) = \text{Type}_s(m) \\ 1 - \delta & \text{otherwise} \end{cases}$$

with $\delta \in [0,1]$ controlling the degree of type-separation. $\text{Type}_e(n)$ is the pre-assigned role of expert $n$ (world-knowledge or downstream); $\text{Type}_s(m)$ is the task type of sample $m$.

The LBC loss minimises the coefficient of variation of the *weighted* importance matrix $\mathbf{Z} = \mathbf{I} \circ \mathbf{Q}$:

$$\mathcal{L}_{\text{lbc}} = \frac{\sigma^2(\mathbf{Z})}{\mu(\mathbf{Z})}$$

The total training loss is:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{NTP}} + \beta \mathcal{L}_{\text{lbc}}$$

In the default setup: $N = 6$ experts (3 world-knowledge, 3 downstream), $\delta = 0.1$, $\beta = 0.1$, $r = 4$, $\alpha = 32$. The constraint is *soft* — it nudges specialisation without hard routing, allowing cooperation across expert types at inference.

## Claims

- **Forgetting vs. scale (core finding):** vanilla SFT on Llama-2-7B with 3 M instruction samples yields TriviaQA 51.1 (vs. baseline 52.2) and NQ 24.5 (vs. 18.5 baseline after CBQA-only tuning). With 5 M samples (10-task variant), TriviaQA drops to 30.9 and HotpotQA to 7.6. The damage is *irreversible*: subsequent CBQA-only fine-tuning on the 3 M-trained model cannot restore performance (Table 1). World knowledge must be protected during, not after, large-scale SFT.
- **LoRAMoE vs. vanilla SFT (3 M, Table 2):** TriviaQA +63.9% relative (58.1 vs. 51.1 SFT); NQ 28.0 vs. 24.5; average world-knowledge improvement +35.3%.
- **LoRAMoE vs. single LoRA:** +30.9% average world-knowledge, +8.4% downstream. Single LoRA degrades knowledge just like full SFT.
- **LBC adds value:** adding $\mathcal{L}_{\text{lbc}}$ to LoRAMoE further improves 13 of 15 tasks, with gains up to 17.6% on reading comprehension and NLI.
- **Downstream parity:** LoRAMoE matches or exceeds SFT on all reading comprehension tasks (Race-middle 90.0, Race-high 86.5, multiRC 87.9) while recovering world knowledge.
- **Expert visualisation:** router assigns significantly higher weight to world-knowledge experts on TriviaQA, NQ, HotpotQA and to downstream experts on Flores, Race, RTE — confirming clean specialisation at inference with no manual routing labels.
- **Parameter sensitivity (Table 3):** $N = 6$, $r = 4$ is the best operating point; increasing to 8 experts or $r = 16$ yields negligible gain despite 2–3× parameter cost.

## Strengths / Novelty

First framework to address SFT-scale knowledge forgetting by routing rather than architectural isolation or regularisation. The frozen backbone is load-bearing: $W_0$ cannot be updated, so world knowledge encoded in pre-training weights survives by construction — experts only add delta capacity. LBC is a principled extension of MoE balancing to mixed-distribution training data; the Gaussian-mixture proof (Appendix C) shows that standard balanced routing is a biased estimator when $p_1 \neq p_2$. The method adds no inference overhead (router is always active; no need to flag data type) and plugs into any transformer FFN without modifying attention.

## Weaknesses / Limits

- Expert typing is binary (world-knowledge vs. downstream) and pre-specified at training time; the paper acknowledges that finer-grained task categories were not explored.
- Experiments are limited to Llama-2-7B; scaling behaviour to larger models is unknown.
- Pre-assigning experts requires knowing which samples are "world-knowledge-related" at data construction time — this labelling burden is implicit but real.
- The soft constraint allows, but does not guarantee, specialisation; router visualisations show some bleed across expert types (WSC: 45% of attention to world-knowledge experts even for a coreference task).
- No continual-learning evaluation: LoRAMoE protects pre-training knowledge from SFT erosion, but it has not been tested against sequential task streams with shifting distributions.

## Relevance to this wiki's project

**Direct structural analogue to MoERA.** MoERA converts a dense model into an MoE by treating delta-LoRA adapters as experts. LoRAMoE is exactly this design — LoRA experts, frozen backbone, learned router — deployed in a published, evaluated system. Every design decision in LoRAMoE (rank $r$, $N$ experts, router parameterisation $G(x) = \text{Softmax}(xW_g)$, frozen $W_0$) is a validated prior for MoERA's architecture choices.

**LBC as the forgetting-mitigation-by-routing answer.** The user's project question — does RLVR/SFT skill-stacking just reallocate optimisation budget? — has a routing-based structural answer here. LBC shows that routing *can* be constrained so that some experts are held on world-knowledge while others absorb new skills, preventing the reallocation from destroying existing capabilities. This is the mechanism MoERA would need to invoke if MoERA experts are trained jointly on mixed data: localize the balancing constraint to protect the $R_w$ subspace ([[../synthesis/proposed-method]]).

**Bridge between catastrophic forgetting and routing.** LoRAMoE sits at the intersection of the catastrophic-forgetting literature ([[../catastrophic-forgetting/_overview]]) and MoE-adapter design ([[_overview]]). It demonstrates that routing-based specialisation, not EWC-style regularisation or orthogonal-subspace penalties, can achieve comparable forgetting mitigation — with the added benefit of zero inference overhead beyond the router.

## Connections to the wiki

- [[_overview]] — LoRAMoE is the anchor paper for the moe-adapters theme; the LBC formulation is the key design primitive to compare against across the theme.
- [[mov-molora]] — parameter-efficient MoE-adapter primitive; LoRAMoE independently arrives at the same LoRA-experts-plus-router structure with a different training objective.
- [[self-moe]] — self-specialised LoRA experts without a balancing constraint; LoRAMoE's LBC is the explicit answer to what happens without guidance.
- [[btx]] — parallel-train then MoE-ify; LoRAMoE trains experts jointly from scratch with a frozen backbone, the complementary regime.
- [[sparse-upcycling]] — dense→MoE ancestor; LoRAMoE is the PEFT-only descendant.
- [[mole]] — LoRA composition alternative; LoRAMoE routes dynamically, MoLE composes statically.
- [[moram]] — router-free MoE-LoRA; contrast with LoRAMoE's explicit router and LBC.
- [[../catastrophic-forgetting/_overview]] — LoRAMoE IS a forgetting-mitigation method; routing is its mechanism, parallel to EWC's parameter-space penalties and RLS's RL-vs-SFT differential.
- [[../catastrophic-forgetting/rls-razor]] — RL forgets less than SFT because RL updates are sparser and more targeted; LoRAMoE achieves similar forgetting reduction via routing. Two independent mechanisms converging on the same goal.
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC adds a quadratic penalty on important weights; LoRAMoE freezes the backbone entirely and routes new capacity via adapters — a stronger structural guarantee at the cost of modularity.
- [[../selective-finetuning/o-lora]] — orthogonal subspaces enforce per-task separation in weight space; LoRAMoE routes per sample via a learned router instead, achieving softer but more flexible specialisation.
- [[../selective-finetuning/dora]] — weight-decomposed LoRA; LoRAMoE's experts use standard LoRA but the LBC analysis applies to DoRA experts equally.
- [[../selective-finetuning/_overview]] — LoRAMoE occupies the intersection of selective-finetuning and MoE; the frozen-backbone constraint is a maximally selective fine-tuning strategy.
- [[../synthesis/proposed-method]] — $R_w$ hypothesis: LoRAMoE demonstrates that routing-based realisation of selective behaviour installation is feasible and measurably effective; MoERA can inherit LBC as its forgetting-mitigation component.
- [[../concept-learning/recursive-concept-evolution]] — RCE uses low-rank concept subspaces; LoRAMoE's LoRA experts are structurally adjacent — each expert spans a low-rank subspace of the weight perturbation space, potentially alignable with concept subspaces.

## Related

- [[mov-molora]] — MoE-adapter primitive; structural sibling
- [[self-moe]] — self-specialised LoRA experts; LoRAMoE adds explicit LBC guidance
- [[btx]] — parallel-train then MoE-ify; complementary training regime
- [[sparse-upcycling]] — dense→MoE ancestor
- [[mole]] — static LoRA composition vs. LoRAMoE's dynamic routing
- [[moram]] — router-free MoE-LoRA baseline
- [[../catastrophic-forgetting/_overview]] — LoRAMoE as a forgetting-mitigation method
- [[../catastrophic-forgetting/rls-razor]] — RL as alternative low-forgetting mechanism
- [[../catastrophic-forgetting/ewc-gemma2-cpt]] — EWC: parameter-penalty alternative to routing-based protection
- [[../selective-finetuning/o-lora]] — orthogonal-subspace per task vs. routing per sample
- [[../selective-finetuning/dora]] — weight-decomposed LoRA
- [[../selective-finetuning/_overview]] — selective finetuning landscape
- [[../synthesis/proposed-method]] — MoERA / $R_w$: LoRAMoE is the routing-based realisation
- [[../concept-learning/recursive-concept-evolution]] — low-rank concept subspaces; structurally adjacent to LoRA experts
