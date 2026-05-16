---
name: rls-razor
description: RL's Razor (Shenfeld et al., MIT, 2025) — on-policy RL is implicitly biased toward KL-minimal solutions; forward KL to the base policy on the new task is the unique strong predictor of catastrophic forgetting (R²=0.96 toy, 0.71 LLM), explaining why RL forgets less than SFT at matched new-task accuracy.
type: research
---

# RL's Razor: Why Online Reinforcement Learning Forgets Less

Shenfeld, Pari & Agrawal (Improbable AI Lab, MIT, 2025) show that on-policy RL forgets significantly less prior knowledge than SFT despite matching it on new-task accuracy, and identify the mechanism: the forward KL divergence $\mathbb{E}_{x\sim\tau}[\mathrm{KL}(\pi_0\|\pi)]$ evaluated on the new task is the sole strong predictor of catastrophic forgetting ($R^2 = 0.96$ on ParityMNIST, $R^2 = 0.71$ on LLMs), while weight norms, activation drift, update sparsity, and rank all fail. The key claim is that on-policy training is *implicitly biased toward KL-minimal solutions* — by sampling from its own distribution at every step, a policy gradient method reweights probability mass conservatively rather than pulling toward an arbitrary external distribution — a principle they term **RL's Razor**. For this wiki, the paper is the mechanistic grounding for why RLVR is a gentler instrument than SFT for stacking new skills on a small LLM: it does not freely redistribute optimization across all skills, but is structurally constrained to stay KL-close to the base.

## Source

- arXiv: 2509.04259
- Raw markdown: `raw/research/rlvr-forgetting/03-01-rls-razor.md`

## Method

**Empirical Forgetting Law.** The paper establishes that the degree of catastrophic forgetting is governed by the forward KL divergence from the fine-tuned model back to the base model, measured *on the new task*:

$$\text{Forgetting} \approx f\!\left(\mathbb{E}_{x \sim \tau}\!\left[\mathrm{KL}(\pi_0 \| \pi)\right]\right)$$

where $\tau$ is the new-task distribution, $\pi_0$ the base policy, and $\pi$ the fine-tuned policy. A quadratic fit to this curve achieves $R^2 = 0.96$ on the ParityMNIST toy setting and $R^2 = 0.71$ on LLM experiments. Crucially, the same curve holds across both RL and SFT runs — meaning the training algorithm is not the proximate cause of forgetting, the KL shift is. Forward KL dominates all alternatives in predictive power (Table 1 in the paper: reverse KL $R^2 = 0.93$, TV $0.80$, weight-change $L_1$ $0.34$, Fisher-weighted $L_2$ $0.58$, update sparsity N/A).

**RL's Razor.** The reason RL produces smaller KL shifts is not the use of negative gradients (SimPO, an offline objective with negative examples, behaves like SFT; 1–0 Reinforce, an on-policy objective with no negative examples, behaves like GRPO). The driver is **on-policy sampling**: the model draws from its own current distribution, reweights by reward, and shifts probability mass conservatively rather than being pulled toward a potentially distant external annotation distribution.

**Lemma 5.1 (KL-minimal projection).** In the binary-reward case, rejection sampling from a policy $p$ with acceptance condition $R(y) = 1$ is equivalent to:

$$q^{\mathrm{RS}} = \arg\min_{q}\; D_{\mathrm{KL}}(q \| p) \quad \text{s.t.}\ \mathbb{E}_{y \sim q}[R(y)] = 1$$

**Theorem 5.2 (Policy gradient converges to KL-minimal optimal policy).** Let $Y$ be finite, $\Pi \subseteq \Delta(Y)$ a convex family, $R: Y \to \{0,1\}$ a binary reward, and $P^* = \{q : \mathbb{E}_q[R] = 1\}$ the set of optimal policies. Under regularity conditions, policy gradient converges to:

$$\pi^\dagger = \arg\min_{\pi \in P^* \cap \Pi}\; D_{\mathrm{KL}}(\pi \| \pi_0)$$

That is, among all achievable optimal policies, policy gradient selects the one closest in KL to initialization — without explicit KL regularization.

**Oracle SFT validation.** The authors construct an oracle SFT distribution that analytically minimizes KL among all 100%-accurate labelings (on ParityMNIST). This oracle SFT *outperforms* standard RL on the forgetting frontier, and SFT trained on RL-generated rollouts matches RL's forgetting curve. Both confirm that the distribution learned, not the algorithm, determines forgetting; RL just happens to find KL-minimal distributions as an implicit consequence of on-policy updates.

**Experimental scope.** Three LLM tasks on Qwen 2.5 3B-Instruct (math reasoning, science Q&A, tool use) and one robotic task (OpenVLA 7B pick-and-place). RL uses GRPO without explicit KL regularization; SFT uses standard cross-entropy. Prior-task retention measured on Hellaswag, TruthfulQA, MMLU, IFEval, Winogrande, HumanEval.

## Claims

- **RL forgets less at matched accuracy.** Across all four tasks, RL's Pareto frontier dominates SFT's in the new-task-accuracy vs. prior-task-retention plane. The gap is sharpest on Math: even small new-task gains via SFT correspond to sharp prior-task degradation.
- **KL predicts forgetting, not the algorithm.** $R^2 = 0.96$ (toy) and $0.71$ (LLM) for a quadratic fit of forgetting vs. $\mathbb{E}_{x \sim \tau}[\mathrm{KL}(\pi_0 \| \pi)]$. No other variable (weight $L_1$, Fisher $L_2$, spectral norm, activation drift, update sparsity, rank) reaches comparable predictive power.
- **On-policy, not negative gradients, is the key axis.** 1–0 Reinforce (on-policy, no negatives) ≈ GRPO; SimPO (offline, with negatives) ≈ SFT.
- **Update sparsity is a bfloat16 artefact, not an explanation.** Float32 training eliminates RL's apparent weight-update sparsity while preserving identical performance, ruling out sparsity as the causal mechanism.
- **Oracle SFT beats RL on forgetting.** When SFT is explicitly steered to the KL-minimal distribution (oracle labels), it surpasses RL's prior-task retention, confirming KL minimization is the causal lever — RL just reaches it implicitly.
- **Effect generalises beyond transformers.** The RL–SFT forgetting gap reproduces in a 3-layer MLP on ParityMNIST, ruling out transformer-specific explanations.

## Strengths / Novelty

The paper does three things cleanly. First, it gives a *falsifiable law* — a single scalar ($\mathbb{E}_{x \sim \tau}[\mathrm{KL}(\pi_0 \| \pi)]$) that predicts forgetting across algorithms, architectures, and domains, without access to prior-task data. Second, it disconfirms popular alternative explanations (sparsity, rank, weight norm, negative gradients) with controlled ablations rather than just proposing the new view. Third, Theorem 5.2 provides theoretical backing for the implicit KL-minimality claim in a clean binary-reward setting, closing the loop between empirical law and mechanism.

The oracle SFT experiment is particularly sharp: it turns RL's Razor from a claim about RL into a claim about KL minimization — any algorithm (including SFT) that stays KL-close forgets less. This reframes the design space as "minimize KL on the new task" rather than "use RL."

## Weaknesses / Limits

- **Moderate scale only.** The largest LLM is Qwen 2.5 3B-Instruct; frontier-scale behavior ($\geq$ 70B) is untested. Some evidence that scale reduces forgetting generally (Ramasesh et al. 2021) may interact with this law.
- **Theorem 5.2 is binary-reward, convex-family.** Real GRPO uses non-binary advantage normalization over a non-convex policy family (transformer softmax). The theorem's applicability is suggestive rather than rigorous for the LLM case.
- **Off-policy RL not studied.** Only on-policy methods (GRPO, 1–0 Reinforce) are tested. Off-policy RL (DPO, IPO, offline PPO) falls on the SFT-like side of the on/off-policy axis and is expected to behave more like SFT, but this is not verified.
- **Mechanistic gap.** The paper is explicit: *why* larger KL shifts disrupt prior knowledge — representational interference, capacity limits, or other dynamics — remains unknown. The law is phenomenological.
- **KL is measured on the new task, not prior tasks.** This is practically convenient but conceptually opaque: the link between new-task KL and prior-task retention is empirical, not derived.

## Relevance to this wiki's project

**Anchoring question: "When you stack skills onto a model with RLVR, does it just move optimization from one skill to another (zero-sum)? Is RLVR forgetting different from SFT forgetting?"**

RL's Razor gives a direct, mechanistic answer: **no, RLVR forgetting is structurally different from SFT forgetting, and it is not zero-sum.** On-policy updates are implicitly biased toward the KL-minimal path into the set of solutions that achieve the new task — the model does not freely redistribute capacity across skills. SFT can and does converge to distributions arbitrarily far from the base model (depending on the external label distribution), making SFT forgetting effectively unconstrained. RLVR forgetting is bounded by this implicit KL-minimality.

For the single-sample concept fine-tuning project, this has two direct implications:

1. **$R_w$ / format-fluency guard ([[../synthesis/proposed-method]]).** The $R_w$ component is a reward signal designed to preserve format-fluency while acquiring a new concept. RL's Razor is the mechanistic justification for why RLVR is the right vehicle for this: RLVR's on-policy bias means the model stays KL-close to the base even as it learns the concept, so the format and language-mode encoded in the base are less likely to be displaced. SFT on a single sample, by contrast, can push the distribution arbitrarily far — especially dangerous at the low-data extreme.

2. **Invisible Leash / support-preservation ([[../self-play/invisible-leash]]).** RL's Razor is the forgetting-side companion to the Invisible Leash: where Theorem C.1 of Invisible Leash bounds the *proposer* inside the base model's *output support*, RL's Razor (Theorem 5.2) bounds the *policy* near the base model in *KL distance*. Together they characterise RLVR as doubly conservative: it stays within support (Invisible Leash) and stays KL-close (RL's Razor). SFT carries neither guarantee.

The implication for the proposed method is practical: if RLVR is used as the primary adaptation signal (with or without an explicit KL penalty in the reward), the implicit KL-minimality of on-policy updates provides a built-in forgetting guard that SFT lacks — relevant when the "training set" is one example.

## Connections to the wiki

- [[ewc-gemma2-cpt]] — EWC is the explicit-regularisation answer to the same forgetting problem; RL's Razor is the *implicit* version. The paper notes that EWC can be interpreted as an approximation to KL minimization (Chaudhry et al. 2018), placing both on the same conceptual axis. EWC requires prior-task data or Fisher estimates; RL's Razor requires neither.
- [[_overview]] — RL's Razor belongs to the catastrophic-forgetting theme as the mechanistic account of why on-policy RL forgets less.
- [[../self-play/invisible-leash]] — Theorem C.1 bounds proposer inside base-model support; RL's Razor (Theorem 5.2) is the KL-distance companion. Together: RLVR stays within support *and* KL-close.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov et al. claim RL's sparse weight updates explain forgetting resistance. RL's Razor directly challenges this: the paper shows weight-update sparsity is a bfloat16 numerical artefact, not a causal mechanism. KL divergence, not sparsity, is the predictor.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER finds RL reranks within base top-5. This is consistent with RL's Razor: on-policy sampling only reaches tokens already probable under the base, so RLVR's solution set is drawn from the KL-proximate region of policy space by construction.
- [[../synthesis/proposed-method]] — $R_w$ / component L format-fluency guard: RL's Razor is the mechanistic warrant for using RLVR as the adaptation vehicle in the proposed single-sample method.
- [[../selective-finetuning/_overview]] — Selective-gradient theme: RL's implicit KL-minimality achieves similar forgetting protection to explicit parameter masking or surgical weight edits, without requiring a mask specification. Complementary rather than competing.
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — BOLT's KL-regularised target leash is an explicit version of the KL constraint that RL's Razor shows on-policy methods achieve implicitly. BOLT adds the penalty; RL's Razor explains why on-policy methods already work without it — and why adding it provides additional forgetting protection.

## Related

- [[ewc-gemma2-cpt]] — EWC: explicit Fisher-regularised weight constraint; RL's Razor is its implicit on-policy analogue
- [[_overview]] — catastrophic-forgetting theme overview
- [[path-not-taken]] — alternative forgetting framing (if available)
- [[rft-mitigates-forgetting]] — RFT-side forgetting mitigation; compare KL predictor against RFT mechanisms
- [[rft-data-perspective]] — data-perspective companion on RFT forgetting
- [[mechanistic-forgetting]] — mechanistic accounts of forgetting; RL's Razor adds the KL-as-predictor layer
- [[empirical-forgetting]] — empirical forgetting benchmarks and scaling laws
- [[../self-play/invisible-leash]] — support-preservation bound; forgetting-side companion to RL's Razor
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — Balashov sparsity claim directly challenged by RL's Razor's float32 ablation
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — REASONMAXXER reranking within base top-5: consistent with KL-minimal path
- [[../synthesis/proposed-method]] — proposed single-sample method; RL's Razor is mechanistic warrant for RLVR choice
- [[../selective-finetuning/_overview]] — implicit vs explicit KL-gradient control
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — BOLT explicit KL leash; RL's Razor explains implicit version
