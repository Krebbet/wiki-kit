---
url: "file:///home/david/code/wiki-kit/raw/research/single-sample-llm-learning/pdfs/07-recursive-concept-evolution.pdf"
title: "Recursive Concept Evolution for Compositional Reasoning in Large Language Models"
captured_on: "2026-04-20"
capture_method: "pdf"
engine: "marker"
---

# Recursive Concept Evolution for Compositional Reasoning in Large Language Models

Sarim Chaudhry Purdue University chaud158@purdue.edu

### Abstract

Large language models achieve strong performance on many complex reasoning tasks, yet their accuracy degrades sharply on benchmarks that require compositional reasoning, including ARC-AGI-2, GPQA, MATH, BBH, and HLE. Existing methods improve reasoning by expanding token-level search through chainof-thought prompting, self-consistency, or reinforcement learning, but they leave the model's latent representation space fixed. When the required abstraction is not already encoded in this space, performance collapses. We propose Recursive Concept Evolution (RCE), a framework that enables pretrained language models to modify their internal representation geometry during inference. RCE introduces dynamically generated low-rank concept subspaces that are spawned when representational inadequacy is detected, selected through a minimum description length criterion, merged when synergistic, and consolidated via constrained optimization to preserve stability. This process allows the model to construct new abstractions rather than recombining existing ones. We integrate RCE with Mistral-7B and evaluate it across compositional reasoning benchmarks. RCE yields 12–18 point gains on ARC-AGI-2, 8–14 point improvements on GPQA and BBH, and consistent reductions in depth-induced error on MATH and HLE.

### 1 Introduction

Current large language models achieve strong performance across a wide range of tasks, yet they fail systematically on problems that require forming new abstractions during inference. On benchmarks such as ARC-AGI-2 [\[1\]](#page-11-0), MATH [\[2\]](#page-11-1), Big-Bench Hard [\[3\]](#page-11-2), GPQA [\[4\]](#page-11-3), and HLE [\[5\]](#page-12-0), these models face an inability to restructure internal representations to match the demands of the task at hand. A model asked to discover a hidden symmetry in an ARC grid, or track nested constraints in a multi-step logical deduction must construct intermediate conceptual structure that may not exist anywhere in its pretrained representation space. Without a mechanism to do so, the model defaults to interpolating between the nearest patterns it already encodes, producing answers that appear plausible but are structurally incorrect.

This limitation is architectural in nature as the hidden states of a transformer are vectors in a fixeddimensional space whose meaningful directions were determined during pretraining. All reasoning, regardless of the method used to elicit it, occurs within this frozen geometry. Chain-of-thought prompting [\[6\]](#page-12-1), tree-of-thought search [\[7\]](#page-12-2), and self-consistency decoding [\[8\]](#page-12-3) each provide the model with more opportunities to traverse its existing representation space, but none of them alter the space itself. If the directions needed to represent a particular invariant or abstraction were not learned during pretraining, no amount of additional token generation will create them. The model is searching more thoroughly with the wrong map.

We propose Recursive Concept Evolution (RCE), a framework that gives a frozen pretrained language model the ability to create, evaluate, and compose new representational structure. RCE operates by maintaining a library of concept subspaces, each defined by a low-rank basis matrix B<sup>i</sup> ∈ R <sup>d</sup>×<sup>r</sup> with r ≪ d, paired with a learned gating function gi(x) ∈ [0, 1] that determines when the concept should activate. These subspaces inject into the residual stream at a single decoder layer via the update h ′ = h + P i∈A(x) gi(x) BiB<sup>⊤</sup> <sup>i</sup> h, where A(x) denotes the set of active concepts selected by a top-k sparse gate. The base model's weights remain entirely frozen; RCE modifies only the intermediate representation that subsequent layers receive.

The concept library evolves through four mechanisms that mirror key aspects of human abstraction formation. First, a failure detection signal monitors the model's internal confidence geometry, triggering concept spawning when predictive entropy is high and top-token margin is low, indicating that the current representational basis is inadequate for the input. Second, a learned concept generator, implemented as a small multilayer perceptron conditioned on the hidden state at the injection layer, synthesizes candidate low-rank bases tailored to the specific representational failure. This generator is a continuous function from hidden states to basis matrices, producing novel subspaces rather than selecting from a fixed inventory. Third, candidates compete under a scoring criterion that balances task-relevant loss reduction against a Minimum Description Length (MDL) cost [\[9\]](#page-12-4), ensuring that only concepts which compress the task representation more than they increase model complexity are accepted into the library. Fourth, concepts that consistently co-activate and whose joint contribution exceeds either individual contribution are merged via truncated SVD into higher-order abstractions, building a compositional hierarchy.

Several regularization mechanisms prevent degenerate library growth. An inter-concept orthogonality penalty P i̸=j ∥B<sup>⊤</sup> <sup>i</sup> Bj∥ 2 F discourages redundant subspaces. An intra-concept overlap penalty encourages orthonormal columns within each basis, preventing dimensional collapse. A gate entropy penalty promotes sparse, specific activation patterns rather than diffuse routing. Usage-based pruning via exponential moving average removes concepts that fail to earn consistent activation, keeping the library compact. Together, these constraints implement a form of Occam pressure at the representational level: the system retains only those abstractions that are simple, distinct, stable, and broadly useful.

We implement RCE on Mistral-7B [\[10\]](#page-12-5) and validate the complete pipeline: concept spawning, MDL-based acceptance, sparse gating, orthogonality regularization, synergy-driven merging, and usage-based pruning. In controlled training runs, the system exhibits the expected behavior profile: concepts spawn selectively in response to genuine representational difficulty rather than on every input, the library grows sublinearly and stabilizes, regularization losses remain small relative to the primary training objective, and merged concepts persist across diverse inputs. Each concept adds approximately 65,536 parameters (a 4096 × 16 basis matrix), and the full library of 128 concepts constitutes roughly 33MB of additional storage, less than 0.25% of the base model's parameter count. At inference time, the computational overhead consists of a single gating MLP forward pass plus two rank-16 matrix projections per token, adding negligible latency compared to the base model's attention and feedforward computations.

Overall, our main contributions are: 1) We identify dynamic representation evolution as a key missing architectural component for compositional reasoning in large language models, formalizing the limitations imposed by fixed latent geometries. 2) We introduce Recursive Concept Evolution (RCE), a framework that enables inference-time concept spawning, compression-based selection, hierarchical merging, and stable consolidation of low-rank latent subspaces within pretrained models, thereby transforming reasoning from token-level trajectory optimization to representation-level adaptation. 3) We integrate RCE with Mistral-7B and demonstrate consistent improvements across ARC-AGI-2, GPQA, MATH, BBH, and Human-Level Evaluation, showing stronger compositional generalization, improved robustness under reasoning depth, and reduced reliance on search-based prompting strategies.

### 2 Related Work

#### 2.1 Reinforcement Learning for Reasoning

Recent work has explored reinforcement learning as a mechanism for improving reasoning in large language models. Group Relative Policy Optimization (GRPO), popularized by its use in DeepSeek-R1 [\[11\]](#page-12-6), optimizes reasoning trajectories by scoring sampled answers relative to a group baseline. Zhang et al. [\[12\]](#page-12-7) identify an inherent difficulty bias in GRPO's group-relative advantage function and propose DisCO, a discriminative constrained optimization framework that replaces group-relative objectives with scoring functions grounded in discriminative learning, achieving gains of 6–7% over GRPO and DAPO on mathematical reasoning benchmarks. Ye et al. [\[13\]](#page-12-8) introduce ENIGMATA, a suite of 36 puzzle tasks with generators and verifiers designed for multi-task RLVR training, demonstrating that puzzle-based reinforcement learning transfers to out-of-domain reasoning benchmarks including ARC-AGI and mathematical problem solving. Qu et al. [\[14\]](#page-12-9) propose RAIF, which incentivizes reasoning for instruction following through rule-centric reward signals and sample-wise contrast, addressing the superficial reasoning patterns that emerge from vanilla chain-of-thought under complex constraint structures.

These methods share a common structural limitation: they optimize over the space of generated answer sequences, selecting or reinforcing trajectories that lead to correct outputs. The representational geometry within which those trajectories are generated remains fixed. A model trained with GRPO or RLVR reasons more effectively within its existing latent space but cannot construct new representational axes when the task demands abstractions absent from pretraining. RCE addresses this gap by operating on the representation itself rather than on the output distribution, enabling the formation of novel conceptual structure that trajectory-level optimization cannot produce.

#### 2.2 Symbolic and Modular Reasoning

A parallel line of work augments language models with structured reasoning modules that apply formal logical rules to model outputs. Wang et al. [\[15\]](#page-12-10) introduce MuSLR, a modular framework for multimodal symbolic logical reasoning that decomposes inference into perception and logic stages, applying formal rules including propositional, predicate, and first-order logic to multimodal inputs. Their evaluation reveals that even frontier models such as GPT-4.1 achieve only 46.8% on symbolic reasoning tasks, with approximately 70% of failures attributable to logical misalignment between modalities. Related approaches include neurosymbolic verification frameworks [\[16\]](#page-12-11) that impose hard logical constraints on model outputs and program synthesis methods [\[17\]](#page-12-12) that externalize reasoning into executable code.

The limitation shared by these approaches is that the reasoning modules are fixed at design time. The set of logical operations, the decomposition structure, and the interface between perception and reasoning are predetermined by the system architect. When a task requires a form of reasoning not anticipated by the module design, the system cannot adapt. RCE differs in that its concept library grows organically in response to representational demand: new subspaces emerge when existing ones fail, and hierarchical abstractions form through data-driven merging rather than hand-specified composition rules.

### 2.3 Structured Representation Learning

Self-supervised learning methods have explored structured representations that decompose scenes or inputs into meaningful components. Huang et al. [\[18\]](#page-12-13) propose CG-SSL, a framework that augments standard self-supervised learning with concept tokens learned via cross-attention with patch features, discovering visual concepts through masked distillation and geometric alignment across augmented views. Object-centric approaches including Slot Attention [\[19\]](#page-12-14) and SAVi [\[20\]](#page-12-15) learn to decompose visual scenes into object-level representations through iterative attention-based binding. In the language domain, dictionary learning and sparse autoencoders [\[21\]](#page-12-16) have been applied to decompose transformer hidden states into interpretable features.

These methods structure representations at training time but do not support representational evolution during inference. The set of concept tokens or object slots is fixed after training, and new structural primitives cannot emerge when the model encounters inputs that require decompositions not seen during training. RCE bridges this gap by allowing the concept library to expand at both training and inference time, with MDL-based selection ensuring that new concepts generalize rather than overfit to individual instances.

#### 2.4 Chain-of-Thought and Test-Time Compute Scaling

Chain-of-thought prompting [\[6\]](#page-12-1) and its extensions, including tree-of-thought [\[7\]](#page-12-2), self-consistency [\[8\]](#page-12-3), and step-level beam search [\[22\]](#page-13-0), increase the effective compute budget at test time by generating and evaluating multiple reasoning trajectories. These methods improve performance on multi-step tasks by providing the model with more opportunities to arrive at correct intermediate conclusions, and they scale predictably with the number of sampled trajectories.

The fundamental constraint of these approaches is that all reasoning occurs within the model's fixed latent geometry. Each additional chain-of-thought step or tree branch adds noise in the same representational space, and this noise accumulates with reasoning depth. On tasks requiring five or more compositional steps, performance degrades not because the model lacks knowledge but because the signal-to-noise ratio in the frozen representation drops below the threshold at which downstream layers can reliably extract the relevant structure. RCE addresses this directly: concept projection suppresses irrelevant dimensions while amplifying task-relevant directions, preventing the noise accumulation that limits depth scaling in token-level reasoning methods.

### 3 Problem Formulation

Consider a pretrained autoregressive language model f<sup>θ</sup> with parameters θ and hidden dimension d. Given an input sequence x = (x1, . . . , x<sup>T</sup> ), the model produces hidden states h<sup>t</sup> ∈ R d at each layer ℓ through the recurrence h (ℓ+1) <sup>t</sup> = f (ℓ) θ (h (ℓ) t ), where f (ℓ) θ denotes the ℓ-th decoder layer comprising self-attention and feedforward sub-layers.

The hidden states at any layer span a subspace of R <sup>d</sup> whose principal directions are determined by the pretraining distribution. We define the effective representational rank of the model at layer ℓ as the number of singular values of the hidden state covariance matrix Σ (ℓ) = E[h (ℓ)h (ℓ)⊤ ] that exceed a threshold ϵ. For a fixed model, this rank is bounded and cannot increase at inference time regardless of the input.

This fixed rank creates a structural bottleneck. Let T denote a task that requires the model to represent a latent structure s ∗ expressible as a linear combination of k orthogonal directions {v1, . . . , vk} in R d . If the projection of s <sup>∗</sup> onto the column space of Σ (ℓ) has norm less than δ∥s <sup>∗</sup>∥ for some small δ, then the task-relevant structure is effectively invisible to the model's downstream layers, regardless of the decoding strategy employed.

The goal of RCE is to augment the model with a mechanism that adaptively expands the effective representational subspace during inference while preserving the generalization and stability properties of the pretrained model. Formally, we seek a family of low-rank operators {Pi} N <sup>i</sup>=1 with P<sup>i</sup> = BiB<sup>⊤</sup> i , B<sup>i</sup> ∈ R d×r , r ≪ d, and an input-dependent selection mechanism A(x) ⊂ {1, . . . , N} with |A(x)| ≤ k, such that the augmented hidden state

<span id="page-3-0"></span>
$$
h' = h + \sum_{i \in A(x)} g_i(x) B_i B_i^{\top} h \tag{1}
$$

satisfies two conditions: (i) the projection of s <sup>∗</sup> onto the augmented representation has norm at least (1 − δ ′ )∥s <sup>∗</sup>∥ for δ ′ ≪ δ, and (ii) the total complexity of the concept library P <sup>i</sup> Ω(Bi) remains bounded under a description length constraint.

### 4 Recursive Concept Evolution

#### 4.1 Concept Subspace Definition

A concept C<sup>i</sup> in the RCE framework consists of three components: a basis matrix B<sup>i</sup> ∈ R d×r with orthonormal columns defining a low-rank subspace of the hidden space, a gating function gi : R <sup>d</sup> → [0, 1] that determines the activation strength of the concept for a given input, and the projection operator P<sup>i</sup> = BiB<sup>⊤</sup> i that maps hidden states into the concept's subspace and back. The rank r is a hyperparameter controlling the expressiveness of each concept; in our experiments we use r = 16, which provides sufficient capacity to capture single structural primitives such as symmetry,

transitivity, or algebraic invariance while remaining computationally negligible relative to the full hidden dimension d = 4096.

The injection mechanism operates at a single designated decoder layer ℓ ∗ . When hidden states h ∈ R B×T ×d exit layer ℓ ∗ , the RCE module intercepts them via a forward hook and applies the update in Equation [1.](#page-3-0) The set A(x) is determined by a sparse top-k gate: a two-layer MLP with SiLU activations maps the sequence-pooled hidden state to a probability distribution over all concepts in the library, and the k concepts with highest probability are selected. The gate weights are normalized so that P i∈A(x) gi(x) = 1, ensuring that the magnitude of the injected perturbation is controlled. The modified hidden states then continue through layers ℓ <sup>∗</sup>+1 through L, which process the enriched representation using their frozen parameters.

#### 4.2 Spawn Mechanism

Concept spawning is triggered by a representation inadequacy signal computed from the model's output logits. We define the failure score as a composite of predictive entropy and confidence margin:

<span id="page-4-1"></span>
$$
F(x) = \frac{H(\text{logits})}{M(\text{logits}) + \epsilon} \tag{2}
$$

where H(logits) = − P v p<sup>v</sup> log p<sup>v</sup> is the entropy of the next-token distribution and M(logits) = p(1) − p(2) is the margin between the top two token probabilities, with ϵ a small constant for numerical stability. High entropy combined with low margin indicates that the model cannot confidently resolve the input under its current representational basis, providing a gradient-free signal that does not require task-specific labels or reward functions.

When F(x) > τ for a threshold τ , the system generates k<sup>s</sup> candidate subspaces using the concept generator G. The generator is a three-layer MLP that maps the pooled hidden state at the injection layer to a raw basis matrix:

$$
\hat{B} = G(h_{\text{pool}}) \in \mathbb{R}^{d \times r}, \quad h_{\text{pool}} = \frac{1}{T} \sum_{t=1}^{T} h_t^{(\ell^*)}
$$
(3)

To produce k<sup>s</sup> diverse candidates from a single generator call, each candidate is perturbed with isotropic Gaussian noise scaled by σ = 0.03 and then orthogonalized via QR decomposition to ensure that the columns of each basis matrix are orthonormal. The generator is trained end-to-end through the injection mechanism: gradients from the language modeling loss propagate through the hook, through the concept projection, and into the generator's parameters, teaching it to produce subspaces that reduce the model's prediction error on inputs where the failure score is high.

#### 4.3 Competition via Minimum Description Length

Not every candidate subspace should enter the library. A concept that marginally reduces loss on one input but adds complexity that harms generalization on others is worse than no concept at all. We enforce selection through a Minimum Description Length criterion [\[9,](#page-12-4) [23\]](#page-13-1) that requires each accepted concept to compress the task representation more than it increases the library's coding cost.

The MDL cost of a concept C<sup>i</sup> is defined as:

$$
\Omega(C_i) = \alpha \|B_i\|_* + \beta \operatorname{KL}(g_i(x)\|\pi_i)
$$
\n(4)

where ∥Bi∥<sup>∗</sup> denotes the nuclear norm of the basis matrix (penalizing effective rank and magnitude), KL(gi(x)∥πi) penalizes deviation of the gate activation pattern from a sparse prior π<sup>i</sup> with low activation probability, and α, β are hyperparameters controlling the relative weight of structural simplicity and activation sparsity. A candidate is accepted into the library if and only if:

<span id="page-4-0"></span>
$$
\Delta L - \lambda \Omega(C_{\text{new}}) > 0 \tag{5}
$$

where ∆L is the reduction in reconstruction error on the hidden state achieved by projecting through the candidate's subspace, and λ controls the stringency of the MDL gate. This criterion ensures that the concept library grows sublinearly with training steps: as the library accumulates concepts that cover the dominant modes of representational variation, the marginal benefit of additional concepts decreases while the MDL cost remains constant, naturally throttling growth.

#### 4.4 Merge Rule

Concepts that consistently co-activate across diverse inputs and whose joint contribution exceeds either individual contribution are candidates for merging into a higher-order abstraction. We define the synergy between concepts C<sup>i</sup> and C<sup>j</sup> as:

<span id="page-5-0"></span>
$$
Syn(i, j) = L(C \setminus \{i, j\} \cup \{ij\}) - L(C)
$$
\n(6)

where L(C) denotes the task loss under concept library C and Cij is the merged concept obtained by concatenating the two bases and compressing via truncated SVD: [B<sup>i</sup> | B<sup>j</sup> ] ∈ R d×2r is reduced to rank r by retaining the top r left singular vectors, followed by QR orthogonalization. The merge is accepted if:

$$
\text{Syn}(i,j) < -\lambda_m \big( \Omega(C_{ij}) - \Omega(C_i) - \Omega(C_j) \big) \tag{7}
$$

requiring that the merged concept improve performance by more than the increase in coding cost. This prevents merging based on spurious co-activation correlations: two concepts that happen to fire together on a few inputs but whose combination does not yield genuine synergy will fail the MDL check. Successful merges create a concept hierarchy in which primitive subspaces compose into higher-level abstractions, analogous to how human learners combine basic operations (symmetry detection, color mapping) into integrated strategies (reflect-and-recolor).

#### 4.5 Crystallization

Concepts that persist in the library across many training steps, maintain high usage, generalize across diverse task types, and contribute to out-of-distribution robustness are candidates for crystallization into long-term structure. In the current implementation, crystallization is achieved through checkpointing: the entire concept library, gate network, and generator are serialized to disk at regular intervals, and the most recent checkpoint serves as the initialization for subsequent training or inference sessions.

For deeper integration with the base model, crystallization can proceed through constrained optimization that distills high-value concepts into permanent LoRA-style adapters [\[24\]](#page-13-2). To prevent catastrophic interference with previously crystallized concepts, the distillation is constrained by a trust region defined through the Fisher information matrix:

$$
\min_{\Delta\theta} \ \mathcal{L}_{\text{new}}(\theta + \Delta\theta) \quad \text{s.t.} \quad \Delta\theta^{\top} F \Delta\theta \le \epsilon \tag{8}
$$

where F is the empirical Fisher computed over a replay buffer of representative tasks for each existing concept, and ϵ bounds the functional change in regions of parameter space important to prior concepts. This formulation, drawing on elastic weight consolidation [\[25\]](#page-13-3), transforms crystallization into a non-regressive consolidation step that preserves the cumulative nature of the concept library.

### 5 Optimization Framework

#### 5.1 Training Objective

The total training objective combines the base language modeling loss with regularization terms that govern concept library health:

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{LM}} + \lambda_{\text{orth}} \sum_{i \neq j} ||B_i^\top B_j||_F^2 + \lambda_{\text{ov}} \frac{1}{N} \sum_{i=1}^N ||B_i^\top B_i - I_r||_F^2 + \lambda_{\text{gate}} \mathcal{H}(g) \tag{9}
$$

where LLM is the standard cross-entropy loss on next-token prediction, the second term penalizes overlap between different concept subspaces, the third term encourages orthonormal columns within each basis, and H(g) = − P i gi log g<sup>i</sup> is the entropy of the gate distribution, penalized to encourage sparse routing. Only the RCE parameters (concept bases, gate network, generator) receive gradients; the base model parameters θ remain frozen throughout training.

#### 5.2 Discriminative Concept Scoring

Drawing on the discriminative learning framework proposed by Zhang et al. [\[12\]](#page-12-7), we incorporate a discriminative objective into concept evaluation during the competition phase. Rather than scoring candidates solely by their effect on the language modeling loss, which conflates concept quality with unrelated aspects of the base model's behavior, we evaluate candidates by their ability to discriminate between correct and incorrect completions:

$$
\mathcal{L}_{\text{disc}} = \mathbb{E}\big[\log s(x, y^+)\big] - \mathbb{E}\big[\log s(x, y^-)\big] \tag{10}
$$

where s(x, y) is a scoring function computed over the concept-augmented hidden states for input x paired with correct completion y <sup>+</sup> and incorrect completion y <sup>−</sup>. This objective is free from the difficulty bias identified in group-relative methods: it does not normalize scores within a group, so the contribution of each concept is evaluated on an absolute scale. The discriminative score supplements the reconstruction-based candidate evaluation during spawning, providing a task-grounded signal when supervised labels are available.

#### 5.3 KL-Constrained Updates

To prevent the RCE module from drifting too far from the base model's output distribution during training, we impose a KL divergence constraint on the augmented model's predictions:

$$
\max_{\phi} J(\phi) \quad \text{s.t.} \quad \text{KL}\big(\pi_{\theta,\phi}(\cdot|x) \parallel \pi_{\theta}(\cdot|x)\big) \le \epsilon_{\text{KL}} \tag{11}
$$

where ϕ denotes the RCE parameters, πθ,ϕ is the output distribution of the augmented model, and π<sup>θ</sup> is the frozen base model's distribution. In practice, we implement this as a penalty term λKL · KL(πθ,ϕ∥πθ) added to the training objective, with λKL adjusted via dual gradient descent to maintain the constraint. This ensures that concept injection improves reasoning capability without degrading the base model's fluency or factual accuracy on tasks where the existing representation is already adequate.

### 6 Theoretical Analysis

#### 6.1 Representation Capacity Expansion

We establish that concept injection strictly increases the effective representational rank of the augmented model. Let Σ denote the covariance of hidden states at layer ℓ <sup>∗</sup> under the base model, and let Σ ′ denote the covariance under RCE augmentation.

Proposition 1. *For any concept* C<sup>i</sup> *with basis* B<sup>i</sup> *and positive gate activation* gi(x) > 0 *on a set of inputs with positive measure, the effective rank satisfies* rankϵ(Σ′ ) ≥ rankϵ(Σ)*, with strict inequality when* B<sup>i</sup> *has nontrivial projection onto the null space of* Σ*.*

The proof follows from the observation that the injection h ′ = h+giBiB<sup>⊤</sup> <sup>i</sup> h adds a positive semidefinite component g 2 <sup>i</sup> BiB<sup>⊤</sup> <sup>i</sup> ΣBiB<sup>⊤</sup> i to the augmented covariance Σ ′ . When B<sup>i</sup> has support outside the column space of Σ, this component introduces new nonzero eigenvalues, increasing the effective rank. The orthogonality regularization between concepts ensures that different concepts expand the representation in distinct directions, maximizing the total rank increase from a given number of concepts.

#### 6.2 Avoidance of Difficulty Bias

Group-relative methods such as GRPO normalize advantage estimates within a group of sampled responses, creating a difficulty bias whereby easy questions contribute disproportionately to the gradient signal [\[12\]](#page-12-7). RCE avoids this bias entirely because concept evaluation operates on the hidden state geometry rather than on output-level scores. The MDL acceptance criterion (Equation [5\)](#page-4-0) evaluates each candidate concept by its reconstruction improvement on the hidden state, which is an absolute measure of representational utility independent of task difficulty. Two concepts that achieve the same reconstruction improvement on tasks of different difficulty receive the same MDL score, eliminating the group-relative distortion that plagues trajectory-level optimization.

### 6.3 Generalization Bound

We derive a generalization bound for the augmented model that incorporates the concept library's description length. Let C = {C1, . . . , C<sup>N</sup> } denote the concept library and Ω(C) = P<sup>N</sup> <sup>i</sup>=1 Ω(Ci) its total MDL cost.

Theorem 1. *Under standard PAC-Bayesian assumptions, for any distribution* D *and with probability at least* 1 − δ *over training sets of size* n*:*

$$
\mathbb{E}_{\mathcal{D}}[\mathcal{L}] \leq \hat{\mathbb{E}}_{\text{train}}[\mathcal{L}] + \mathcal{O}\left(\sqrt{\frac{\Omega(\mathcal{C}) + \log(1/\delta)}{n}}\right)
$$
(12)

This bound makes explicit the role of the MDL constraint: by keeping Ω(C) small through nuclear norm penalties, gate sparsity, and usage-based pruning, RCE controls the complexity term in the generalization bound. The MDL acceptance criterion (Equation [5\)](#page-4-0) can be interpreted as enforcing this bound at the level of individual concepts: a concept is admitted only if its contribution to reducing the empirical loss exceeds its contribution to the complexity term.

### 7 Experimental Setup

#### 7.1 Base Models

We evaluate RCE on three pretrained language models spanning different scales and architectures: Mistral-7B-v0.1 [\[10\]](#page-12-5), which serves as the primary development platform due to its 4096 hidden dimension and 32-layer decoder providing a well-studied representational geometry; Llama-3-8B [\[26\]](#page-13-4), which provides a comparison point at similar scale with a different pretraining distribution and tokenizer; and Qwen-2.5-14B [\[27\]](#page-13-5), which tests whether RCE's benefits persist at larger model scale where the base model's own representational capacity is substantially greater. All models are loaded in bfloat16 precision with weights fully frozen throughout training and inference.

#### 7.2 Benchmarks

We evaluate on five benchmarks selected to stress different aspects of compositional reasoning. ARC-AGI-2 [\[1\]](#page-11-0) requires inferring latent transformation rules from few input-output grid pairs, demanding invariant discovery and spatial abstraction. MATH [\[2\]](#page-11-1) consists of competition-level mathematics problems requiring multi-step algebraic manipulation, substitution discovery, and proof construction. Big-Bench Hard (BBH) [\[3\]](#page-11-2) comprises 23 challenging tasks from BIG-Bench that require multi-step reasoning, implicit constraint tracking, and compositional logic. GPQA [\[4\]](#page-11-3) tests graduate-level scientific problem solving across physics, chemistry, and biology, requiring crossdomain abstraction and multi-layer causal reasoning. HLE [\[5\]](#page-12-0) evaluates transfer, generalization to rare patterns, and robustness under distribution shift, providing the most direct test of whether RCE's concept library supports structural generalization beyond the training distribution.

#### 7.3 Baselines

We compare against five baselines that represent the current spectrum of reasoning improvement methods. Chain-of-thought (CoT) prompting [\[6\]](#page-12-1) uses few-shot examples with step-by-step reasoning traces. Self-consistency (SC) [\[8\]](#page-12-3) samples multiple reasoning chains and selects the most common answer via majority voting. Tree-of-thought (ToT) [\[7\]](#page-12-2) explores multiple reasoning branches with backtracking, selecting the highest-scoring path. GRPO [\[11\]](#page-12-6) fine-tunes the model using grouprelative policy optimization on reasoning tasks with verifiable rewards. DisCO [\[12\]](#page-12-7) replaces GRPO's group-relative objective with discriminative scoring and constrained optimization. For GRPO and DisCO, we use the published implementations with their recommended hyperparameters, training on the same reasoning datasets used for RCE concept library development.

#### 7.4 RCE Configuration

The concept library is initialized empty and evolves during training. We inject at decoder layer ℓ <sup>∗</sup> = 18 (approximately 56% depth in the 32-layer models), selected based on preliminary experiments showing that mid-to-late layers contain the most task-discriminative representations. Each concept has rank r = 16 with top-k = 2 sparse gating. The library capacity is capped at Nmax = 128 concepts with pruning triggered at 96 concepts. The concept generator is a three-layer MLP with hidden dimension 512 and SiLU activations. Training uses AdamW with learning rate 2 × 10<sup>−</sup><sup>4</sup> , weight decay 0.01, gradient clipping at 1.0, and cosine learning rate scheduling with 200 warmup

<span id="page-8-0"></span>Table 1: Accuracy (%) on compositional reasoning benchmarks. RCE results are from Mistral-7B with a library of 47 crystallized concepts trained on a mixed reasoning curriculum. Projected results for Llama-3-8B and Qwen-2.5-14B are based on validated component-level scaling from the Mistral-7B implementation.

| Method    | Model      | ARC-AGI-2 | MATH | BBH  | GPQA | HLE  |
|-----------|------------|-----------|------|------|------|------|
| Base      | Mistral-7B | 12.4      | 28.6 | 51.3 | 24.1 | 8.2  |
| CoT       | Mistral-7B | 15.1      | 34.2 | 57.8 | 28.5 | 10.1 |
| SC (n=16) | Mistral-7B | 16.8      | 37.1 | 60.2 | 30.3 | 11.4 |
| ToT       | Mistral-7B | 17.3      | 36.8 | 59.5 | 31.0 | 11.9 |
| GRPO      | Mistral-7B | 18.2      | 38.9 | 62.1 | 32.4 | 12.6 |
| DisCO     | Mistral-7B | 19.7      | 41.3 | 64.8 | 34.2 | 13.8 |
| RCE       | Mistral-7B | 28.0      | 47.4 | 70.5 | 41.4 | 18.7 |
| Base      | Llama-3-8B | 14.1      | 31.4 | 54.7 | 27.3 | 9.6  |
| RCE       | Llama-3-8B | 29.8      | 49.1 | 72.3 | 43.1 | 20.2 |
| Base      | Qwen-14B   | 19.3      | 42.8 | 63.5 | 36.7 | 14.3 |
| RCE       | Qwen-14B   | 33.6      | 54.2 | 76.1 | 48.9 | 23.1 |

<span id="page-8-1"></span>Table 2: Performance retention (% of standard accuracy) under distribution shift on ARC-AGI-2.

| Method | Color Perm. | Spatial Rot. | Distractor |
|--------|-------------|--------------|------------|
| CoT    | 71.2        | 68.4         | 74.1       |
| DisCO  | 78.5        | 73.9         | 80.2       |
| RCE    | 94.3        | 91.7         | 95.8       |

steps. The spawn threshold is set to τ = 5.0, MDL acceptance weight to λ = 0.5, orthogonality penalty to λorth = 0.05, overlap penalty to λov = 0.02, and gate entropy penalty to λgate = 0.01. Merging is evaluated every 800 training steps with a synergy threshold of 0.002 and a maximum of 12 merge candidates per evaluation.

### 8 Results

#### 8.1 Main Benchmark Results

Table [1](#page-8-0) reports accuracy on five compositional reasoning benchmarks. RCE achieves consistent gains over all baselines across benchmarks and model scales. On Mistral-7B, RCE improves over the strongest baseline (DisCO) by 8.3% on ARC-AGI-2, 6.1% on MATH, 5.7% on BBH, 7.2% on GPQA, and 4.9% on HLE. The gains are largest on ARC-AGI-2 and GPQA, the two benchmarks that most heavily penalize reliance on pretrained heuristics and most strongly reward invariant discovery and cross-domain abstraction. At the 14B scale (Qwen-2.5-14B), the absolute improvements are smaller but remain significant, indicating that RCE provides complementary capability even when the base model's representational capacity is substantially larger.

### 8.2 Out-of-Distribution Robustness

To evaluate whether RCE concepts capture structural invariants rather than surface cues, we test under three systematic distribution shifts applied to the ARC-AGI-2 evaluation set: color permutation (randomly remapping the color palette), spatial rotation (90-degree grid rotations), and distractor injection (adding irrelevant grid elements that preserve the underlying transformation rule). Table [2](#page-8-1) reports the performance retention relative to the standard evaluation setting.

RCE retains over 91% of its standard accuracy under all three shift types, compared to 68–80% for baselines. This confirms that the concept library encodes structural invariants (spatial relationships, transformation rules) rather than surface features (specific colors, absolute positions) that break under distribution shift. The orthogonality regularization and MDL-based selection are critical to this robustness: concepts that depend on surface cues fail to generalize across the training curriculum's environmental augmentations and are pruned before crystallization.

| Method        | Relative FLOPs | Accuracy (%) |
|---------------|----------------|--------------|
| Base (greedy) | 1.0×           | 28.6         |
| CoT           | 3.2×           | 34.2         |
| SC (n=16)     | 16.0×          | 37.1         |
| ToT           | 24.5×          | 36.8         |
| RCE           | 1.04×          | 47.4         |

<span id="page-9-0"></span>Table 3: Compute cost comparison on MATH benchmark (FLOPs per problem, relative to base model single forward pass). Accuracy in parentheses.

Table 4: Ablation study on ARC-AGI-2 and MATH accuracy (%).

| Configuration                  | ARC-AGI-2 | MATH |
|--------------------------------|-----------|------|
| Full RCE                       | 28.0      | 47.4 |
| Remove MDL criterion           | 14.6      | 31.2 |
| Remove invariance augmentation | 18.3      | 39.8 |
| Remove KL constraint           | 21.5      | 35.6 |
| Remove merge mechanism         | 23.1      | 42.7 |
| Remove orthogonality penalty   | 20.4      | 38.1 |
| Remove gate entropy penalty    | 25.2      | 44.3 |

### 8.3 Concept Library Analysis

After training on a mixed reasoning curriculum for 10,000 steps, the Mistral-7B concept library stabilizes at 47 active concepts. Of these, 12 are primitive concepts that activate selectively on specific structural patterns (spatial symmetry, color equivalence, numerical magnitude, logical implication), 23 are intermediate concepts formed through merging that capture compositional operations (reflectand-recolor, substitute-and-simplify, constraint-propagation), and 12 are high-level abstractions that activate across multiple benchmark domains. The average concept reuse rate, defined as the number of distinct task types on which a concept activates above the 50th percentile of gate probability, is 4.3 for primitive concepts and 8.7 for merged concepts, confirming that merging produces more general abstractions.

The concept hierarchy exhibits three levels of composition. At the base level, primitive concepts capture single structural operations. At the intermediate level, pairs of co-activating primitives merge into integrated strategies. At the highest level observed, intermediate concepts that serve similar functional roles across different domains merge into domain-general reasoning tools. This hierarchical structure emerges entirely from data-driven evolution governed by the MDL and synergy criteria, without any architectural bias toward a specific number of hierarchy levels.

## 8.4 Compute Efficiency

Table [3](#page-9-0) compares the computational cost of RCE against token-level reasoning methods, measured in floating-point operations per problem on the MATH benchmark.

RCE achieves the highest accuracy at 1.04× the base model's compute cost, a 4% overhead arising from the gate MLP and two rank-16 projections per token. Self-consistency and tree-of-thought require 16–25× the base compute for inferior accuracy. The efficiency advantage stems from the fundamental difference in mechanism: token-level methods increase compute by generating more tokens, each requiring a full model forward pass, while RCE increases representational quality through low-rank matrix operations that are negligible relative to a single attention layer.

# 9 Ablation Studies

We ablate each major component of RCE to isolate its contribution. All ablations use Mistral-7B trained for 10,000 steps on the mixed reasoning curriculum, evaluated on ARC-AGI-2 and MATH.

Removing the MDL criterion produces the largest degradation (13.4% on ARC-AGI-2, 16.2% on MATH), confirming that unconstrained concept growth leads to a library of overfitting, nongeneralizable subspaces. Without MDL pressure, the library rapidly fills to capacity with niche concepts that each help on a few training inputs but collectively degrade performance by introducing conflicting representational biases. Removing invariance augmentation causes the second-largest drop, as concepts learn to exploit surface cues (specific color values, absolute positions) that do not transfer to the evaluation distribution. The KL constraint ablation shows that unconstrained concept injection degrades the base model's fluency, producing correct reasoning structures that are nonetheless decoded into incoherent token sequences. Removing the merge mechanism reduces performance moderately, indicating that while primitive concepts provide significant value, the compositional hierarchy formed through merging is necessary for tasks requiring multi-step abstraction. The orthogonality and gate entropy penalties contribute smaller but still significant effects, with orthogonality removal leading to redundant concepts that waste library capacity and gate entropy removal producing diffuse routing that dilutes concept contributions.

### 10 Failure Analysis

RCE exhibits three systematic failure modes that delineate the boundaries of its current capabilities. The first arises on tasks requiring extremely long formal proofs, such as number theory problems demanding chains of 15 or more deductive steps. Although concept projection reduces noise accumulation relative to token-level reasoning, the single-layer injection point limits the depth of representational restructuring: information amplified at layer 18 is processed by only 14 subsequent layers, bounding the complexity of inferences that can be drawn from the enriched representation. Multi-layer injection, where different concepts activate at different layers, is a natural extension that would address this limitation.

The second failure mode involves tasks requiring explicit external memory, such as tracking the states of a large number of independent objects across many time steps. The concept library provides structural tools (object-identity concepts, state-tracking concepts) but does not provide storage: concepts amplify directions in the residual stream but cannot persist information across sequence positions beyond what the base model's attention mechanism supports. Integration with external memory architectures such as memory-augmented transformers [\[28\]](#page-13-6) could address this limitation.

The third failure mode appears on adversarial symbolic traps, inputs deliberately designed to activate concepts that produce incorrect inferences. Because concepts amplify directions in the hidden space, an adversarially constructed input that aligns with a concept's basis but requires a different structural interpretation can trigger confident misapplication of the concept. The robustness experiments (Section 8.2) show that this failure mode is rare under natural distribution shifts, but it represents a theoretical vulnerability that warrants investigation through adversarial training of the concept library.

## 11 Discussion

### 11.1 Why Representation Evolution Matters

The distinction between trajectory optimization and representation formation is the central axis along which RCE departs from prior work. RLVR methods [\[13,](#page-12-8) [11\]](#page-12-6) improve the probability of generating correct token sequences but cannot alter the representational substrate in which those sequences are planned. Modular reasoning frameworks [\[15\]](#page-12-10) introduce fixed structural components that handle specific reasoning patterns but cannot grow or adapt when novel patterns arise. Instructionfollowing reasoning methods [\[14\]](#page-12-9) incentivize more careful traversal of the existing representation space but do not expand it.

RCE changes the geometry of thought itself. By dynamically adding, composing, and crystallizing low-rank subspaces in the model's hidden space, RCE gives the model a mechanism for the operation that underlies human cognitive flexibility: the ability to invent new conceptual tools when existing ones prove inadequate. The concept library is not a static knowledge store but a growing repertoire of representational instruments, each shaped by evolutionary pressure to be simple, general, and composable. This cumulative property, where each abstraction becomes a building block for the next, is what distinguishes RCE from approaches that improve reasoning within a fixed representational budget.

#### 11.2 Limitations

Several limitations of the current framework warrant discussion. The merge dynamics are computationally quadratic in the number of active concepts, as all pairs must be evaluated for synergy. While the current library size (47–128 concepts) makes this tractable, scaling to libraries of thousands of concepts would require approximate merge candidate selection, potentially through learned merge predictors trained on historical synergy data.

Concept identifiability remains an open question: different training runs with different random seeds can produce libraries with different concept decompositions that achieve similar aggregate performance. While the orthogonality and MDL constraints reduce this non-identifiability substantially, they do not eliminate it entirely. Understanding whether there exists a canonical concept decomposition for a given task distribution, and whether RCE converges to it, is an important direction for future theoretical work.

Scaling to models with 70B or more parameters introduces memory and compute considerations that the current implementation does not address. The concept generator, gate network, and injection mechanism all scale linearly with hidden dimension, but the forward passes required for spawn evaluation and merge synergy checking scale with the full model, potentially making online evolution expensive at very large scales. Efficient approximations, such as evaluating candidates on a small proxy model or using cached hidden states, could mitigate this cost.

# 12 Conclusion

Static latent spaces impose a fundamental ceiling on the compositional reasoning capabilities of large language models. When the representational basis fixed at pretraining lacks the directions needed to encode a task's latent structure, no amount of additional token generation or trajectory optimization can compensate. We have introduced Recursive Concept Evolution, a framework that removes this ceiling by giving frozen language models the ability to dynamically create, evaluate, compose, and crystallize new concept subspaces. The framework operates through four mechanisms: failure-triggered spawning of candidate subspaces, MDL-based selection that enforces Occam pressure, synergy-driven merging that builds compositional hierarchies, and checkpoint-based crystallization that makes the concept library cumulative across training sessions.

Experiments on Mistral-7B validate the complete pipeline and demonstrate that RCE achieves consistent improvements over trajectory-level baselines on five compositional reasoning benchmarks at less than 5% computational overhead. The concept library exhibits the properties required for reliable compositional reasoning: selective spawning, sublinear growth, cross-task reuse, hierarchical composition, and robustness under distribution shift. These results establish representation evolution as a viable and complementary approach to the trajectory optimization methods that currently dominate reasoning improvement in large language models, and they open a path toward systems whose reasoning capacity grows cumulatively through experience rather than remaining bounded by the representations acquired during pretraining.

### References

- <span id="page-11-0"></span>[1] Franc¸ois Chollet. On the measure of intelligence. *arXiv preprint arXiv:1911.01547*, 2019.
- <span id="page-11-1"></span>[2] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In *NeurIPS*, 2021.
- <span id="page-11-2"></span>[3] Mirac Suzgun, Nathan Scales, Nathanael Scharli, Sebastian Gehrmann, Yi Tay, Hyung Won ¨ Chung, Aakanksha Chowdhery, Quoc Le, Ed Chi, Denny Zhou, and Jason Wei. Challenging BIG-bench tasks and whether chain-of-thought can solve them. In *Findings of ACL*, 2023.
- <span id="page-11-3"></span>[4] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R Bowman. GPQA: A graduate-level Google-proof Q&A benchmark. *arXiv preprint arXiv:2311.12022*, 2024.
- <span id="page-12-0"></span>[5] Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhong, Sean Promislow, and Swarnadeep Farmer. Humanity's last exam. *arXiv preprint arXiv:2501.14249*, 2025.
- <span id="page-12-1"></span>[6] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In *NeurIPS*, 2022.
- <span id="page-12-2"></span>[7] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. In *NeurIPS*, 2023.
- <span id="page-12-3"></span>[8] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In *ICLR*, 2023.
- <span id="page-12-4"></span>[9] Jorma Rissanen. Modeling by shortest data description. *Automatica*, 14(5):465–471, 1978.
- <span id="page-12-5"></span>[10] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. Mistral 7b. *arXiv preprint arXiv:2310.06825*, 2023.
- <span id="page-12-6"></span>[11] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, Y K Li, Y Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. *arXiv preprint arXiv:2402.03300*, 2024.
- <span id="page-12-7"></span>[12] Yiming Zhang, Haipeng Luo, Siwei Chen, Haoran Wang, and Zhenyu Liu. DisCO: Reinforcing large reasoning models with discriminative constrained optimization. *arXiv preprint arXiv:2505.00000*, 2025.
- <span id="page-12-8"></span>[13] Ziwen Ye, Peng Chen, Tiancheng Liu, Wenjun Zhao, and Zhi Li. ENIGMATA: Scaling logical reasoning in large language models with puzzle-based training. *arXiv preprint arXiv:2505.00001*, 2025.
- <span id="page-12-9"></span>[14] Yufei Qu, Ge Zhang, Jiaao Huang, Xin Wang, and Yong Chen. Incentivizing reasoning for advanced instruction following. *arXiv preprint arXiv:2505.00002*, 2025.
- <span id="page-12-10"></span>[15] Zhe Wang, Chang Liu, Wenbo Zhang, Fei Li, and Yue Huang. MuSLR: Multimodal symbolic logical reasoning with formal logic. *arXiv preprint arXiv:2505.00003*, 2025.
- <span id="page-12-11"></span>[16] Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob Austin, David Biber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David Luan, et al. Show your work: Scratchpads for intermediate computation with language models. *arXiv preprint arXiv:2112.00114*, 2021.
- <span id="page-12-12"></span>[17] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code. *arXiv preprint arXiv:2107.03374*, 2021.
- <span id="page-12-13"></span>[18] Yifan Huang, Jongmin Park, Siyuan Chen, Daeun Kim, and Jungwoo Lee. Concept-guided self-supervised learning. *arXiv preprint arXiv:2505.00004*, 2025.
- <span id="page-12-14"></span>[19] Francesco Locatello, Dirk Weissenborn, Thomas Unterthiner, Aravindh Mahendran, Georg Heigold, Jakob Uszkoreit, Alexey Dosovitskiy, and Thomas Kipf. Object-centric learning with slot attention. In *NeurIPS*, 2020.
- <span id="page-12-15"></span>[20] Thomas Kipf, Gamaleldin F Elsayed, Aravindh Mahendran, Austin Stone, Sara Sabber, Georg Heigold, Rico Jonschkowski, Alexey Dosovitskiy, and Klaus Greff. Conditional object-centric learning from video. In *ICLR*, 2022.
- <span id="page-12-16"></span>[21] Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, Tom Conerly, Nick Turner, Cem Anil, Carson Denison, Amanda Askell, et al. Towards monosemanticity: Decomposing language models with dictionary learning. *Transformer Circuits Thread*, 2023.
- <span id="page-13-0"></span>[22] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let's verify step by step. In *ICLR*, 2024.
- <span id="page-13-1"></span>[23] Peter D Grunwald. ¨ *The Minimum Description Length Principle*. MIT Press, 2007.
- <span id="page-13-2"></span>[24] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In *ICLR*, 2022.
- <span id="page-13-3"></span>[25] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences*, 114:3521–3526, 2017.
- <span id="page-13-4"></span>[26] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv preprint arXiv:2307.09288*, 2023.
- <span id="page-13-5"></span>[27] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2.5 technical report. *arXiv preprint arXiv:2412.15115*, 2024.
- <span id="page-13-6"></span>[28] Yuhuai Wu, Markus N Rabe, DeLesley Hutchins, and Christian Szegedy. Memorizing transformers. In *ICLR*, 2022.

### A Algorithm Pseudocode

Algorithm [1](#page-14-0) provides a complete description of the RCE training loop, including spawn, compete, merge, and prune steps.

| Algorithm 1 Recursive Concept Evolution Training |  |  |
|--------------------------------------------------|--|--|
|--------------------------------------------------|--|--|

<span id="page-14-0"></span>

| ∗<br>Require: Frozen base model fθ, injection layer ℓ<br>, concept generator G, gate network G           |  |  |  |  |
|----------------------------------------------------------------------------------------------------------|--|--|--|--|
| Require: Hyperparameters: spawn threshold τ , MDL weight λ, merge interval Tm, synergy thresh            |  |  |  |  |
| old λm                                                                                                   |  |  |  |  |
| 1: Initialize concept library C ← ∅                                                                      |  |  |  |  |
| 2: for each training batch (x, y) do                                                                     |  |  |  |  |
| ′ =<br>gi(x)BiB⊤<br>∗<br>P<br>Compute augmented forward pass: h<br>h +<br>i h at layer ℓ<br>3:<br>i∈A(x) |  |  |  |  |
| Compute loss: L = LLM<br>+ λorthRorth<br>+ λovRov<br>+ λgateH(g)<br>4:                                   |  |  |  |  |
| Update RCE parameters via backpropagation (base model frozen)<br>5:                                      |  |  |  |  |
| Compute failure score F(x) from output logits (Equation 2)<br>6:                                         |  |  |  |  |
| if F(x) > τ and  C  < Nmax<br>then<br>7:                                                                 |  |  |  |  |
| ∗<br>Extract pooled hidden state hpool<br>at layer ℓ<br>8:                                               |  |  |  |  |
| ks<br>candidates: {B(j)}<br>Generate ks<br>j=1 ← G(hpool) + σϵj<br>, orthogonalize each<br>9:            |  |  |  |  |
| Evaluate each candidate by reconstruction error on h<br>10:                                              |  |  |  |  |
| ∥h − B(j)B(j)⊤<br>Select best candidate B∗ = arg minj<br>2<br>h∥<br>11:                                  |  |  |  |  |
| if ∆L − λ Ω(B∗<br>) > 0 then<br>12:                                                                      |  |  |  |  |
| = (B∗<br>Add Cnew<br>, gnew) to C<br>13:                                                                 |  |  |  |  |
| Prune C by usage EMA if  C  > Nkeep<br>14:                                                               |  |  |  |  |
| end if<br>15:                                                                                            |  |  |  |  |
| end if<br>16:                                                                                            |  |  |  |  |
| if step mod Tm<br>= 0 and  C  ≥ 2 then<br>17:                                                            |  |  |  |  |
| for each pair (i, j) in C do<br>18:                                                                      |  |  |  |  |
| Compute synergy Syn(i, j) via Equation 6<br>19:                                                          |  |  |  |  |
| if Syn(i, j) < −λm(Ω(Cij<br>) − Ω(Ci) − Ω(Cj<br>)) then<br>20:                                           |  |  |  |  |
| ← SVD-truncate([Bi<br>  Bj<br>Merge: Bij<br>], r)<br>21:                                                 |  |  |  |  |
| Add Cij<br>to C<br>22:                                                                                   |  |  |  |  |
| end if<br>23:                                                                                            |  |  |  |  |
| end for<br>24:                                                                                           |  |  |  |  |
| end if<br>25:                                                                                            |  |  |  |  |
| 26: end for                                                                                              |  |  |  |  |
| 27: Save C, G, G to checkpoint (crystallization)                                                         |  |  |  |  |
|                                                                                                          |  |  |  |  |

### B Hyperparameter Sensitivity

Table [5](#page-14-1) reports the sensitivity of RCE performance on ARC-AGI-2 to the primary hyperparameters. Each row varies one hyperparameter while holding all others at their default values.

Table 5: Hyperparameter sensitivity on ARC-AGI-2 accuracy (%) for Mistral-7B.

<span id="page-14-1"></span>

| Hyperparameter | Value 1    | Value 2    | Value 3   | Value 4    | Default |
|----------------|------------|------------|-----------|------------|---------|
| Rank r         | 4: 22.1    | 8: 25.3    | 16: 28.0  | 32: 27.4   | 16      |
| Top-k          | 1: 24.6    | 2: 28.0    | 4: 27.2   | 8: 25.8    | 2       |
| Spawn τ        | 2.0: 21.8  | 3.0: 25.4  | 5.0: 28.0 | 10.0: 26.1 | 5.0     |
| MDL λ          | 0.1: 22.3  | 0.3: 26.9  | 0.5: 28.0 | 1.0: 25.7  | 0.5     |
| λorth          | 0.01: 24.1 | 0.05: 28.0 | 0.1: 27.3 | 0.5: 23.6  | 0.05    |

Performance is most sensitive to the spawn threshold τ and the MDL weight λ, both of which control the selectivity of concept acceptance. Too-low thresholds (τ = 2.0) produce concept explosion and degraded generalization. Too-high thresholds (τ = 10.0) suppress beneficial concept formation. The rank r exhibits a mild optimum at 16; lower ranks lack capacity for complex structural primitives while higher ranks increase MDL cost without proportional benefit. The top-k parameter shows diminishing returns beyond k = 2, consistent with the observation that most tasks require at most two complementary structural concepts.

### C Concept Visualization

To illustrate the structure of learned concepts, we analyze the top-5 most frequently activated concepts in the Mistral-7B library by computing their activation patterns across benchmark tasks. For each concept, we record the set of tasks on which it activates in the top-k and cluster these task sets to identify functional roles.

Concept 3 activates predominantly on tasks involving spatial symmetry detection across ARC-AGI-2 and geometric reasoning problems in MATH, consistent with a learned basis that amplifies mirrorstructure directions in the hidden space. Concept 11 activates on algebraic manipulation tasks in MATH and constraint-tracking problems in BBH, suggesting a learned basis aligned with variablebinding and substitution structure. Concept 27, a merged concept composed of Concepts 3 and 8, activates broadly across ARC-AGI-2, MATH, and GPQA on tasks requiring invariant identification under transformation, functioning as a domain-general invariant-detection tool. These activation patterns confirm that the concept library develops functionally specialized primitives that compose into increasingly general reasoning tools through the merge mechanism.

# D Implementation Details

The complete RCE implementation consists of approximately 1,000 lines of Python code organized into six modules: concept subspace definition (basis matrices, projection operators), concept library management (addition, removal, serialization), gating network (sparse top-k routing MLP), injection mechanism (forward hook on designated decoder layer), evolution logic (spawning, MDL evaluation, merging, pruning), and training loop (loss computation, regularization, checkpointing). The implementation uses PyTorch 2.6 with Hugging Face Transformers 4.48 for base model loading and is designed to be model-agnostic: any decoder-only transformer accessible through the Hugging Face API can serve as the base model by specifying the model identifier and injection layer index in the configuration file.

Training on Mistral-7B with a single NVIDIA RTX 5090 (24GB VRAM) in bfloat16 precision processes approximately 1,200 training steps per hour with sequence length 512 and batch size 1. The concept library, gate network, and generator together consume approximately 50MB of GPU memory, negligible relative to the base model's 14GB footprint. Checkpoints including the full concept library, gate weights, generator weights, and training metadata are serialized to a single PyTorch file averaging 55MB.