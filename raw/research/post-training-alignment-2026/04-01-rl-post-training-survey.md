---
url: "https://arxiv.org/pdf/2407.16216"
title: "Reinforcement Learning for LLM Post-Training: A Survey"
captured_on: "2026-04-21"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/01-rl-post-training-survey"
---

# Reinforcement Learning for LLM Post-Training: A Survey

Zhichao Wang <sup>∗</sup>,† Salesforce

AWS AI Labs

Salesforce

zcwang0201@gmai.com

Kiran Ramnath <sup>∗</sup>,†,<sup>⋄</sup> kiranramnath007@gmail.com

Bin Bi <sup>∗</sup> bin.bi@salesforce.com

Shiva Kumar Pentyala, Sougata Chaudhuri, Shubham Mehrotra, Xiang-Bo Mao, Zixu (James) Zhu, Sitaram Asur Salesforce

Na (Claire) Cheng Airbnb

### Abstract

Through pretraining and supervised fine-tuning (SFT), large language models (LLMs) acquire strong instruction-following capabilities, yet they can still produce harmful or misaligned outputs. A growing body of reinforcement learning (RL)-based post-training methods has been proposed to address this, including Reinforcement Learning from Human Feedback (RLHF) and Reinforcement Learning with Verifiable Rewards (RLVR) approaches built on Proximal Policy Optimization (PPO), Group Relative Policy Optimization (GRPO), Direct Preference Optimization (DPO), and others. Despite rapid progress, no existing work offers a systematic, technically detailed comparison of these methods under a single analytical lens. Our survey aims to fill this gap. We make three key contributions: (1) a selfcontained RL and LLM post-training foundations treatment covering all necessary concepts alongside their key applications; (2) a unified policy gradient framework unifying PPO and GRPO-based RLHF, RLVR, and offline DPO-based RLHF, decomposing methods along the axes of prompt sampling, response sampling, and gradient coefficient, with an extended treatment of on-policy RLHF and iterative DPO methods as well as the richer design space of offline DPO-based methods; and (3) standardized notation across all reviewed papers enabling direct technical comparison. Our goal is to serve as a comprehensive, technically grounded reference for researchers and practitioners working on LLM post-training.

<sup>\*.</sup> Equal Contribution

<sup>†</sup>. Corresponding Authors

<sup>⋄</sup>. Work done prior to Amazon

# Contents

<span id="page-1-0"></span>

| 1 | Introduction                                                               | 4  |
|---|----------------------------------------------------------------------------|----|
|   | 1.1<br>Pretraining and SFT                                                 | 4  |
|   | 1.2<br>RLHF<br>.                                                           | 4  |
|   | 1.3<br>RLVR<br>.                                                           | 4  |
|   | 1.4<br>Contributions<br>.                                                  | 4  |
|   | 1.5<br>Paper Organization                                                  | 6  |
|   |                                                                            |    |
| 2 | Evolution of Language Model Training Paradigms                             | 6  |
|   | 2.1<br>Unified Post-Training (UPT) via a Unified Policy Gradient Estimator | 6  |
|   | 2.2<br>LLM Pretraining: MLE<br>.                                           | 7  |
|   | 2.3<br>From REINFORCE to Early RL for Language Models<br>.                 | 9  |
|   | 2.4<br>RLHF: AC, TRPO and PPO<br>.                                         | 11 |
|   | 2.5<br>RLVR: GRPO                                                          | 16 |
|   | 2.6<br>Hybrid Post-Training (HPT)<br>.                                     | 18 |
|   | 2.7<br>The Art of Scaling RL: ScaleRL                                      | 19 |
|   | 2.8<br>Individual Paper Summaries                                          | 19 |
|   |                                                                            |    |
| 3 | RLVR: Prompt Sampling                                                      | 20 |
|   | 3.1<br>Prompt Generation                                                   | 22 |
|   | 3.2<br>Prompt Selection<br>.                                               | 23 |
|   |                                                                            |    |
| 4 | RLVR: Response Sampling                                                    | 25 |
|   | 4.1<br>Response Generation                                                 | 26 |
|   | 4.2<br>Response Selection<br>.                                             | 33 |
| 5 | RLVR: Gradient Coefficient                                                 | 36 |
|   | 5.1<br>Importance Sampling Ratio<br>.                                      | 36 |
|   | 5.2<br>Advantage Shaping                                                   | 41 |
|   | 5.3<br>Advantage Normalization<br>.                                        | 54 |
|   | 5.4<br>Length Normalization<br>.                                           | 58 |
|   | 5.5<br>Regularization                                                      | 61 |
|   |                                                                            |    |
| 6 | RLHF and Iterative DPO: On-Policy Methods                                  | 64 |
|   | 6.1<br>RLHF<br>.                                                           | 65 |
|   | 6.2<br>RLAIF                                                               | 65 |
|   | 6.3<br>Iterative DPO                                                       | 68 |
|   | 6.4<br>Nash Learning based Methods                                         | 69 |
| 7 | DPO: Offline Methods                                                       | 71 |
|   | 7.1<br>Response Generation                                                 | 72 |
|   | 7.2<br>Reward<br>.                                                         | 79 |
|   |                                                                            |    |
|   | 7.3<br>Regularization                                                      | 82 |
|   | 7.4<br>Merge SFT<br>.                                                      | 85 |

| 8 | Future Directions<br>86                        |                                                               |     |  |
|---|------------------------------------------------|---------------------------------------------------------------|-----|--|
|   | 8.1                                            | Foundations: Gradient Coefficient Theory and Convergence<br>. | 87  |  |
|   | 8.2                                            | Prompt: Curriculum Design and Self-Play<br>.                  | 87  |  |
|   | 8.3                                            | Response: Sampling, Diversity, and Length<br>.                | 88  |  |
|   | 8.4                                            | Feedback: Supervision Quality and Evaluation                  | 88  |  |
|   | 8.5                                            | Reward: Models, Granularity, and Safety                       | 89  |  |
|   | 8.6                                            | Algorithm: Optimization and Pipeline Integration              | 89  |  |
|   | 8.7                                            | Extensions: Frontiers Beyond Current Scope                    | 90  |  |
| 9 | Conclusion                                     |                                                               | 90  |  |
| A | RLVR - detailed characterization of all papers |                                                               | 114 |  |
| B |                                                | RLHF - detailed characterization of all papers                | 125 |  |

# <span id="page-3-5"></span><span id="page-3-0"></span>1 Introduction

This section outlines the core stages of LLM training, i.e., pretraining, SFT, RLHF, and RLVR. It then presents the structure and contributions of this work, guiding readers through the technical foundations of RL and its role in LLM post-training.

# <span id="page-3-1"></span>1.1 Pretraining and SFT

The rapid ascent of LLMs has been propelled by scaling decoder-only Transformers [\(Vaswani](#page-108-0) [et al., 2017\)](#page-108-0) trained with self-supervised next-token prediction [\(Radford et al., 2019\)](#page-106-0) on trillions of tokens, yielding models with broad world knowledge and emergent capabilities. However, a pretrained model is optimized to continue its training distribution, not to follow user instructions. Performing SFT on curated instruction–response pairs [\(Brown et al., 2020;](#page-98-0) [Ouyang et al., 2022\)](#page-105-0) closes this gap, teaching the model to produce helpful responses to human queries.

# <span id="page-3-2"></span>1.2 RLHF

SFT does not, however, guarantee alignment with human values: models can still generate outputs that are unhelpful, dishonest, or unsafe. RLHF [\(Christiano et al., 2017;](#page-98-1) [Stiennon](#page-107-0) [et al., 2020;](#page-107-0) [Ouyang et al., 2022;](#page-105-0) [Bai et al., 2022a\)](#page-97-0) addresses this by training a reward model on pairwise human preferences and optimizing the LLM policy, typically via PPO [\(Schulman](#page-107-1) [et al., 2017b\)](#page-107-1), to maximize the reward subject to a KL penalty that anchors the policy to a reference model. RLHF induces frontier systems including GPT-4 [\(OpenAI et al.,](#page-104-0) [2024\)](#page-104-0), Claude [\(Anthropic, 2024\)](#page-97-1), and Gemini [\(Gemini, 2025\)](#page-100-0). The RLHF/PPO pipeline is resource-intensive, requiring four models to be held in memory simultaneously, i.e., the policy, reference, reward, and value models along with on-policy rollouts at every gradient step. DPO addresses this by establishing a direct mapping between the reward model and the optimal policy, enabling joint optimization through offline pairwise preference data.

# <span id="page-3-3"></span>1.3 RLVR

RLHF and DPO rely on reward signals derived from subjective human judgments. For domains where correctness is objectively verifiable, i.e., mathematics and code generation, a stronger training signal is available: whether the final answer matches the ground truth or the generated code passes its test suite. RLVR exploits this signal to cultivate reasoning capabilities. DeepSeek-R1 [\(Guo et al., 2025\)](#page-100-1) showed that outcome-based RL, powered by GRPO [\(Shao et al., 2024\)](#page-107-2), can elicit sophisticated chain-of-thought (CoT) reasoning [\(Wei](#page-108-1) [et al., 2023\)](#page-108-1) directly from a base model without any supervised reasoning data.

# <span id="page-3-4"></span>1.4 Contributions

Existing surveys of RLHF and RLVR predominantly emphasize empirical or qualitative comparisons over algorithmic internals [\(Zhang et al., 2025c;](#page-111-0) [Liu et al., 2025b;](#page-102-0) [Ghasemi](#page-100-2) [et al., 2025;](#page-100-2) [Gao et al., 2024\)](#page-99-0). There is no survey that can dive deeper into the technical or mathematical details of the different techniques in this area in a manner that enables the

![](./assets/01-rl-post-training-survey/_page_4_Figure_1.jpeg)

<span id="page-4-0"></span>Figure 1: Overview of the key components in the reinforcement learning-based post-training pipeline for LLMs.

reader to understand and draw connections between them easily. This survey fills that gap with the following contributions:

- Self-contained RL and LLM post-training foundations. Section 2 provides a self-contained treatment of all reinforcement learning foundations and key LLM post-training algorithms, beginning from MLE and REINFORCE through RLHF, PPO, and DPO to RLVR and GRPO. This covers every concept required to understand the methods surveyed in later sections without consulting any external reference. For each algorithm, we derive the policy-gradient objective and identify the gradient coefficient that encapsulates its core design decisions, thereby establishing the unified analytical lens used throughout the survey.
- Unified policy gradient framework with systematic decomposition. We present a unified policy gradient framework that includes PPO-based RLHF, RLVR, and DPObased alignment. RLVR decomposes all surveyed methods along three orthogonal design axes: prompt sampling (Section 3), response sampling (Section 4), and gradient coefficient (Section 5). Section 6 extends the framework to on-policy RLHF and iterative DPO methods, including RLAIF and Nash learning. Section 7 covers offline DPO-based methods, which share the same policy gradient foundation but exhibit greater diversity in preference signal design, and is organized along response generation, reward modeling, regularization, and SFT integration.
- Standardized notation enabling direct technical comparison. We introduce a unified notation applied consistently across all reviewed papers, expressing every

<span id="page-5-4"></span>method's update rule in terms of the same gradient coefficient decomposition. This common formalism makes design choices directly comparable across otherwise disparate methods, and is supported by detailed per-paper comparison tables in the appendix that catalog not only base models, training datasets, and benchmarks, but also fine-grained algorithmic attributes including importance sampling ratio, clipping strategy, reward signal, baseline, advantage normalization, length normalization, partition function, KL regularization, and entropy regularization thereby enabling systematic cross-method comparison under the unified framework.

### <span id="page-5-0"></span>1.5 Paper Organization

As shown in Figure [1,](#page-4-0) the post-training of LLM will be reviewed from six interconnected modules: Prompt (human-generated or synthetic), Response (on-policy, off-policy, offline, and SFT), Reward Models (rule-based, AI/human feedback, and outcome vs. process rewards), Reward signal formulations (pointwise, pairwise, listwise, negative, and token-level), Reinforcement Learning algorithms (REINFORCE, PPO, GRPO, DPO), and Regularization techniques (divergence and entropy). Arrows indicate the training loop: prompts are fed to the LLM, generated responses are scored by reward models to produce reward signals, and the RL algorithm updates the LLM with regularization constraints.

Section [2](#page-5-1) develops a unified post-training framework (UPT), deriving pretraining through MLE, REINFORCE, actor-critic, TRPO, PPO, DPO, and GRPO for RLHF and RLVR. Section [3](#page-19-0) covers prompt sampling, including generation (human-generated and synthetic) and selection (static curriculum, adaptive difficulty, and reward-based filtering). Section [4](#page-24-0) addresses response sampling, covering generation methods (on-policy, off-policy, asynchronous, and tree-structured rollouts) and selection strategies. Section [5](#page-35-0) dissects the gradient coefficient across importance sampling ratio, advantage shaping, normalization, length normalization, and regularization. Section [6](#page-63-0) examine on-policy based RLHF, RLAIF and iterative DPO and Nash learning methods. Section [7](#page-70-0) examines offline-policy learning, covering response generation, reward modeling, regularization, optimization iterations, and SFT merging. Section [8](#page-85-0) outlines future directions, and Section [9](#page-89-1) concludes the survey. Detailed characterizations of all RLVR and RLHF papers appear in the appendices [A](#page-113-0) and [B.](#page-124-0)

### <span id="page-5-1"></span>2 Evolution of Language Model Training Paradigms

In this section, we present a unified post-training framework based on a single policy gradient estimator. Building on this framework, we sequentially introduce key training paradigms for LLMs: LLM pretraining through MLE, SFT, and RLHF/RLVR through REINFORCE, AC, TRPO and PPO and GRPO.

### <span id="page-5-2"></span>2.1 Unified Post-Training (UPT) via a Unified Policy Gradient Estimator

Post-training methods, ranging from supervised fine-tuning to reinforcement learning, can all be understood through a unified objective function gradient structure [\(Shao et al., 2024\)](#page-107-2). On-policy RL methods optimize a reverse-KL-regularized reward objective in Eq. [2.1.1.](#page-5-3)

<span id="page-5-3"></span>
$$
J(\theta) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \mathbb{E}_{y \sim \pi_{\theta}(\cdot | x)} [r(x, y)] - \beta \operatorname{KL}(\pi_{\theta}(\cdot | x) \parallel \pi_{\text{ref}}(\cdot | x))] \right], \quad \beta \ge 0 \tag{2.1.1}
$$

<span id="page-6-5"></span>Expanding the KL into the expectation, the per-prompt objective is Eq. [2.1.2.](#page-6-1)

<span id="page-6-1"></span>
$$
J(\theta) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \sum_{y} \pi_{\theta}(y|x) \left( r(x, y) - \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) \right]
$$
(2.1.2)

For a given x, π<sup>θ</sup> appears twice in the inner sum: as the expectation weight and inside the log-ratio. Letting f(y, θ) = r(x, y) − β log <sup>π</sup>θ(y|x) πref (y|x) , the product rule gives ∇θ[ P y πθf] = X y (∇θπθ) f | {z } Term 1 + X y π<sup>θ</sup> ∇θf | {z } Term 2 . Term 2 differentiates the log-ratio: ∇θf = −β ∇<sup>θ</sup> log πθ, so

Term 2 = −β P y πθ(y|x) ∇θπθ(y|x) <sup>π</sup>θ(y|x) = −β P <sup>y</sup> ∇θπθ(y|x) = −β ∇<sup>θ</sup> P y πθ(y|x) = −β ∇θ1 = 0, since probabilities sum to one. Only Term 1 survives; applying the log-derivative trick ∇θπ<sup>θ</sup> = π<sup>θ</sup> ∇<sup>θ</sup> log π<sup>θ</sup> and restoring the outer expectation over x in Eq. [2.1.3.](#page-6-2)

<span id="page-6-2"></span>
$$
\nabla_{\theta} J(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} \left[ \underbrace{\left( r(x, y) - \beta \log \frac{\pi_{\theta}(y | x)}{\pi_{\text{ref}}(y | x)} \right)}_{\text{gradient coefficient}} \nabla_{\theta} \log \pi_{\theta}(y | x) \right] \tag{2.1.3}
$$

# 2.1.1 The Unified Gradient Coefficient

More generally, the gradient of any post-training method can be written in token-level form [\(Shao et al., 2024\)](#page-107-2) in Eq. [2.1.1.1.](#page-6-3)

<span id="page-6-3"></span>
$$
\nabla_{\theta} J(\theta) = \mathbb{E}_{(x,y)\sim\mathcal{D}} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \mathrm{GC}(x, y, t) \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.1.1.1)
$$

where D is the data source and GC is the gradient coefficient that determines the magnitude and sign of reinforcement for each token. Practical post-training methods are recovered by varying three interchangeable components: (i) the data source D, which can be offline (from a fixed dataset), off-policy (from a different behavior policy πb) or on-policy (from the previous steps πθold or from the current policy πθ); (ii) the gradient coefficient GC; and (iii) a stabilization mechanism such as PPO clipping or a KL penalty. We now derive the objective and gradient for each representative method.

### <span id="page-6-0"></span>2.2 LLM Pretraining: MLE

Pretraining is the most compute-intensive stage of building an LLM: a randomly initialized transformer is trained on trillions of tokens via self-supervised next-token prediction. Given a pretraining corpus Dpre = {x (i)} with x = (x 1 , . . . , x|x<sup>|</sup> ), the model π<sup>θ</sup> maximizes the average log-likelihood in Eq. [2.2.1.](#page-6-4)

<span id="page-6-4"></span>
$$
J_{\text{pre}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{pre}}} \left[ \frac{1}{|x|} \sum_{t=1}^{|x|} \log \pi_{\theta}(x^t | x^{< t}) \right] \tag{2.2.1}
$$

<span id="page-7-7"></span>Maximizing Eq. [2.2.1](#page-6-4) is equivalent to minimizing the forward KL divergence between the data distribution and the model in Eq. [2.2.2.](#page-7-0)

$$
\min_{\theta} D_{\text{KL}}(\pi_{\text{pre}}(x) \| \pi_{\theta}(x)) = \min_{\theta} \mathbb{E}_{x \sim D_{\text{pre}}} \left[ \log \frac{\pi_{\text{pre}}(x)}{\pi_{\theta}(x)} \right]
$$
\n
$$
= \underbrace{\mathbb{E}_{x \sim D_{\text{pre}}} [\log \pi_{\text{pre}}(x)]}_{-H(\pi_{\text{pre}}), \text{ const. w.r.t. } \theta} - \mathbb{E}_{x \sim D_{\text{pre}}} \left[ \sum_{t=1}^{|x|} \log \pi_{\theta}(x^{t} | x^{
$$

Since H(πpre) is independent of θ, minimizing DKL recovers the MLE objective in Eq. [2.2.1](#page-6-4) (up to a scaling constant). Differentiating yields the log-likelihood gradient in Eq. [2.2.3,](#page-7-1) which matches the unified form in Eq. [2.1.1.1.](#page-6-3)

<span id="page-7-1"></span><span id="page-7-0"></span>
$$
\nabla_{\theta} J_{\text{pre}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{pre}}} \left[ \frac{1}{|x|} \sum_{t=1}^{|x|} \nabla_{\theta} \log \pi_{\theta}(x^t | x^{< t}) \right] \tag{2.2.3}
$$

The constant gradient coefficient GCpre(x, t) = 1 means every token is reinforced equally, regardless of quality or downstream relevance. This uniform, task-agnostic objective makes pretraining scalable, i.e., requiring no reward model, annotations, or prompt-response structure. However, the resulting base model cannot distinguish preferred from dispreferred outputs. Subsequent post-training methods (SFT, RFT, Online RFT, etc.) refine it toward aligned and capable behavior.

# <span id="page-7-5"></span>2.2.1 SFT

SFT maximizes the log-likelihood on a curated demonstration dataset Dsft composed of prompt x and golden response y in Eq. [2.2.1.1.](#page-7-2) Differentiating with respect to θ derives Eq. [2.2.1.2,](#page-7-3) yielding a constant gradient coefficient GCSFT(x, y, t) = 1, with the curated dataset serving as an implicit human-selection reward.

<span id="page-7-2"></span>
$$
J_{\text{SFT}}(\theta) = \mathbb{E}_{(x,y)\sim\mathcal{D}_{\text{sf}}}\left[\frac{1}{|y|} \sum_{t=1}^{|y|} \log \pi_{\theta}(y^t | x, y^{(2.2.1.1)
$$

<span id="page-7-3"></span>
$$
\nabla_{\theta} J_{\text{SFT}}(\theta) = \mathbb{E}_{(x,y)\sim\mathcal{D}_{\text{sft}}} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.2.1.2)
$$

# <span id="page-7-6"></span>2.2.2 RFT

RFT [\(Yuan et al., 2023a;](#page-111-1) [Dong et al., 2023\)](#page-99-1) samples multiple responses from the SFT model πsft(y|x) and trains only on those with correct answers in Eq. [2.2.2.1](#page-7-4) where I(y = y ∗ ) = 1 if the answer is correct and 0 otherwise.

<span id="page-7-4"></span>
$$
J_{\rm RFT}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\rm sft}, y \sim \pi_{\rm sft}(\cdot|x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \mathbb{I}(y = y^*) \log \pi_\theta(y^t | x, y^{(2.2.2.1)
$$

Differentiating with respect to θ derives Eq. [2.2.2.2](#page-8-1) giving gradient coefficient GCRFT(x, y, t) = I(y = y ∗ ): uniform reinforcement of correct responses, zero for incorrect ones. RFT is an offline method since outputs are sampled once from πsft.

<span id="page-8-1"></span>
$$
\nabla_{\theta} J_{\text{RFT}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{sft, } y \sim \pi_{\text{sft}}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \mathbb{I}(y = y^*) \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.2.2.2)
$$

## 2.2.3 Online RFT

The only difference between online RFT and RFT is that responses are sampled from the current policy π<sup>θ</sup> rather than the fixed πsft as shown in Eq. [2.2.3.1,](#page-8-2) and differentiating with respect to π<sup>θ</sup> obtains Eq. [2.2.3.2.](#page-8-3)

<span id="page-8-2"></span>
$$
J_{\text{OnRFT}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{sft}}, y \sim \pi_{\theta}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \mathbb{I}(y = y^*) \log \pi_{\theta}(y^t | x, y^{(2.2.3.1)
$$

<span id="page-8-3"></span>
$$
\nabla_{\theta} J_{\text{OnRFT}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{sft}}, y \sim \pi_{\theta}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \mathbb{I}(y = y^*) \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.2.3.2)
$$

The gradient coefficient remains I(y = y ∗ ), but the on-policy data source allows the model to explore beyond the initial SFT distribution, yielding continued improvement in later training stages where the actor has diverged significantly from the SFT model.

### <span id="page-8-0"></span>2.3 From REINFORCE to Early RL for Language Models

Before the modern RLHF paradigm, several works explored reinforcement learning to directly optimize sequence-level metrics for text generation. In a general Markov decision process (MDP), an agent in state s<sup>t</sup> takes action a<sup>t</sup> , receives reward r<sup>t</sup> , and transitions to st+1, producing a trajectory τ = (s1, a1, s2, a2, . . . , s<sup>T</sup> , a<sup>T</sup> ). The agent accumulates the discounted return G<sup>t</sup> with discount factor γ ∈ [0, 1], and the objective is to maximize the expected return J(θ) in Eq. [2.3.1.](#page-8-4)

<span id="page-8-4"></span>
$$
G_t = \sum_{t'=t}^T \gamma^{t'-t} r_{t'}, \qquad J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=1}^T \gamma^{t-1} r_t \right] = \mathbb{E}_{\tau \sim \pi_\theta} [G_t]
$$
 (2.3.1)

The form of r<sup>t</sup> distinguishes two reward paradigms:

• Outcome Reward Model (ORM): Only the terminal state receives reward. With γ = 1, the return simplifies to G<sup>t</sup> = r(x, y), as defined in Equation [\(2.3.2\)](#page-8-5).

<span id="page-8-5"></span>
$$
r_t = \begin{cases} r(x,y) & t = T \\ 0 & t < T \end{cases}, \qquad G_t = r(x,y) \tag{2.3.2}
$$

<span id="page-9-2"></span>• Process Reward Model (PRM) [\(Lightman et al., 2023\)](#page-102-1) assigns rewards sparsely at reasoning step boundaries. Let Sterminal ⊆ {1, . . . , |y|} be the set of step-ending token positions, as defined in Equation [\(2.3.3\)](#page-9-0).

<span id="page-9-0"></span>
$$
r_t = \begin{cases} r^p(x, y^{\leq t}) & \text{if } t \in S_{terminal} \\ 0 & \text{otherwise} \end{cases}, \qquad G_t = \sum_{t' \in S_{terminal}, t' \geq t} r^p(x, y^{\leq t'}) \qquad (2.3.3)
$$

# 2.3.1 REINFORCE

The REINFORCE algorithm [\(Williams, 1992\)](#page-109-0) derives an unbiased gradient estimator for the expected return. The trajectory probability factorizes as πθ(τ ) = Q<sup>T</sup> <sup>t</sup>=1 πθ(a<sup>t</sup> |st) p(st+1|s<sup>t</sup> , at). Starting from the definition of J(θ) = JREINFORCE(θ) = Eτ∼π<sup>θ</sup> [G<sup>t</sup> ] = Eτ∼π<sup>θ</sup> hP<sup>T</sup> <sup>t</sup>=1 γ t−1 rt i in Eq. [2.3.1,](#page-8-4) the derivation relies on two identities. Firstly, the log-derivative trick: ∇θπθ(x) = πθ(x) ∇<sup>θ</sup> log πθ(x). Secondly, since the transition dynamics p(st+1|s<sup>t</sup> , at) do not depend on θ, the log-trajectory decomposes as ∇<sup>θ</sup> log πθ(τ ) = P<sup>T</sup> t ′=1 ∇<sup>θ</sup> log πθ(a<sup>t</sup> ′|s<sup>t</sup> ′). Applying these identities, the policy gradient derivation proceeds as Eq. [2.3.1.1](#page-9-1)

$$
\nabla_{\theta} J_{REINFORCE}(\theta) = \nabla_{\theta} \sum_{\tau} \pi_{\theta}(\tau) \sum_{t=1}^{T} \gamma^{t-1} r_{t}
$$
\n
$$
= \sum_{\tau} (\nabla_{\theta} \pi_{\theta}(\tau)) \sum_{t=1}^{T} \gamma^{t-1} r_{t}
$$
\n(linearity of  $\sum$ )\n
$$
= \sum_{\tau} \pi_{\theta}(\tau) \nabla_{\theta} \log \pi_{\theta}(\tau) \sum_{t=1}^{T} \gamma^{t-1} r_{t}
$$
\n(lose-derivative trick)\n
$$
= \mathbb{E}_{\tau \sim \pi_{\theta}} \Big[ \sum_{t=1}^{T} \gamma^{t-1} r_{t} \nabla_{\theta} \log \pi_{\theta}(\tau) \Big] \qquad (\sum_{\tau} \pi_{\theta}[\cdot] = \mathbb{E}_{\pi_{\theta}}[\cdot])
$$
\n
$$
= \mathbb{E}_{\tau \sim \pi_{\theta}} \Big[ \sum_{t=1}^{T} \gamma^{t-1} r_{t} \sum_{t'=1}^{T} \nabla_{\theta} \log \pi_{\theta}(a_{t'} | s_{t'}) \Big] \qquad (\text{log-trajectory decomposition})
$$
\n
$$
= \mathbb{E}_{\tau \sim \pi_{\theta}} \Big[ \sum_{t'=1}^{T} \nabla_{\theta} \log \pi_{\theta}(a_{t'} | s_{t'}) \sum_{t=1}^{T} \gamma^{t-1} r_{t} \Big] \qquad (\text{swap finite sums})
$$
\n
$$
= \mathbb{E}_{\tau \sim \pi_{\theta}} \Big[ \sum_{t'=1}^{T} \nabla_{\theta} \log \pi_{\theta}(a_{t'} | s_{t'}) \sum_{t=1}^{t'} \gamma^{t-1} r_{t} \Big] \qquad (\text{causality})
$$
\n
$$
= \mathbb{E}_{\tau \sim \pi_{\theta}} \Big[ \sum_{t=1}^{T} G_{t} \nabla_{\theta} \log \pi_{\theta}(a_{t} | s_{t}) \Big] \qquad (\text{causality}, t' \to t) \qquad (2.3.1.1)
$$

<span id="page-9-1"></span>where the last step applies causality: r<sup>t</sup> for t < t′ is determined entirely by the trajectory up to step t and cannot depend on the future action a<sup>t</sup> ′; moreover, <sup>E</sup>a<sup>t</sup> ′∼πθ(·|s<sup>t</sup> ′ ) [∇<sup>θ</sup> log πθ(a<sup>t</sup> ′|s<sup>t</sup> ′)] = ∇<sup>θ</sup> P at ′ πθ(a<sup>t</sup> ′|s<sup>t</sup> ′) = ∇θ1 = 0, so past-reward terms vanish in expectation. Dropping these zero-expectation terms and relabeling t ′→t, each ∇<sup>θ</sup> log πθ(a<sup>t</sup> |st) pairs only with its future discounted return G<sup>t</sup> = P<sup>T</sup> t ′=t γ t ′−t rt ′.

Substituting the LLM instantiation s<sup>t</sup> = (x, y<t), a<sup>t</sup> = y <sup>t</sup> with outcome reward model and γ = 1 derives Eq. [2.3.1.2](#page-10-1) giving gradient coefficient GCREINFORCE(x, y, t) = r(x, y).

<span id="page-10-3"></span><span id="page-10-1"></span>
$$
\nabla_{\theta} J_{\text{REINFORCE}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} r(x, y) \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.3.1.2)
$$

### 2.3.2 Early Applications to Sequence Models

[Ranzato et al.](#page-106-1) [\(2016\)](#page-106-1) introduced MIXER wherein they applied RL to sequence generation models. They combined cross-entropy pretraining with REINFORCE fine-tuning, using tasklevel evaluation metrics (e.g., BLEU) as rewards and a learned linear regression baseline over the RNN hidden states to reduce variance without introducing bias. This work established that sequence-level RL objectives could surpass token-level cross-entropy training on translation and summarization, although the approach was validated only on small recurrent models.

### <span id="page-10-0"></span>2.4 RLHF: AC, TRPO and PPO

A central challenge in policy-gradient methods is preventing each update from catastrophically degrading pretrained capabilities. Actor-critic methods (AC) address this by replacing the raw return with a learned advantage, reducing gradient variance. TRPO [\(Schulman et al.,](#page-107-3) [2017a\)](#page-107-3) constrains updates to a KL trust region, guaranteeing monotonic improvement but requiring expensive second-order computations. PPO [\(Schulman et al., 2017b\)](#page-107-1) approximates the same constraint with a clipped first-order surrogate, making it the dominant RLHF algorithm at scale.

# 2.4.1 AC methods

AC methods [\(Konda and Tsitsiklis, 1999\)](#page-101-0) replace the high-variance Monte Carlo return G<sup>t</sup> in REINFORCE with a learned advantage. The advantage A<sup>π</sup> (s<sup>t</sup> , at) = Q<sup>π</sup> (s<sup>t</sup> , at) − V π (st) = Q<sup>π</sup> (s<sup>t</sup> , at)−Eat∼π[Q<sup>π</sup> (s<sup>t</sup> , at)] measures how much better action a<sup>t</sup> is compared to the average action under π in state s<sup>t</sup> . The policy gradient theorem [\(Sutton et al., 1999\)](#page-107-4) then writes JAC(θ) = Eτ∼π<sup>θ</sup> [A<sup>π</sup> (s<sup>t</sup> , at)] and ∇θJAC(θ) in Eq. [2.4.1.1.](#page-10-2)

<span id="page-10-2"></span>
$$
\nabla_{\theta} J_{\text{AC}}(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_{t=1}^{T} A^{\pi}(s_t, a_t) \, \nabla_{\theta} \log \pi_{\theta}(a_t | s_t) \right]
$$
(2.4.1.1)

Starting from REINFORCE, ∇θJREINFORCE(θ) = Eτ∼π<sup>θ</sup> hP<sup>T</sup> <sup>t</sup>=1 G<sup>t</sup> ∇<sup>θ</sup> log πθ(a<sup>t</sup> |st) i . Subtracting any state-dependent baseline b(st) from the coefficient preserves unbiasedness, because Eat∼π<sup>θ</sup> [b(st)∇<sup>θ</sup> log πθ(a<sup>t</sup> |st)] = b(st) ∇<sup>θ</sup> P at πθ(a<sup>t</sup> |st) = b(st) ∇θ1 = 0. Choosing b(st) = V π (st) is optimal in that it reduces the variance of the gradient estimator, and the resulting coefficient is exactly the advantage A<sup>π</sup> (s<sup>t</sup> , at) = Q<sup>π</sup> (s<sup>t</sup> , at) − V π (st). Because the advantage is centered, i.e., Eat∼π[A<sup>π</sup> (s<sup>t</sup> , at)] = 0, its magnitude is much smaller than the raw return G<sup>t</sup> , substantially reducing gradient variance without introducing any bias.

Actor-critic methods require two separately trained models: (i) the actor (policy model) πθ, updated via the policy gradient in Eq. [2.4.1.1,](#page-10-2) and (ii) the critic (value model) V<sup>ϕ</sup> ≈ V π , trained by regressing on target values Lcritic(ϕ) = Eτ∼π<sup>θ</sup> hP<sup>T</sup> <sup>t</sup>=1(Vϕ(st) <sup>−</sup> <sup>V</sup><sup>ˆ</sup> <sup>π</sup> t ) 2 i . The target Vˆ <sup>π</sup> t is either the Monte Carlo return G<sup>t</sup> (unbiased, high variance) or the one-step

<span id="page-11-6"></span>temporal-difference (TD) target r<sup>t</sup> + γ Vϕ<sup>−</sup> (st+1) with stop-gradient parameters ϕ <sup>−</sup> (biased, lower variance). The one-step TD residual δ<sup>t</sup> = r<sup>t</sup> + γ Vϕ<sup>−</sup> (st+1) − Vϕ(st) measures the prediction error of the value function at each step and serves as the building block for advantage estimation. Generalized Advantage Estimation (GAE) [\(Schulman et al., 2018\)](#page-107-5) interpolates between the high-bias one-step TD estimate (λ = 0) and the high-variance Monte Carlo estimate (λ = 1) via an exponentially weighted sum of multi-step TD residuals in Eq. [2.4.1.2.](#page-11-0)

<span id="page-11-0"></span>
$$
A_t^{\text{GAE}(\gamma,\lambda)} = \sum_{l=0}^{T-t} (\gamma \lambda)^l \, \delta_{t+l} \tag{2.4.1.2}
$$

At each iteration, both actor and critic models are updated jointly: the critic minimizes Lcritic(ϕ) (or its TD variant) while the actor ascends along ∇θJAC(θ) using the GAE advantage estimates in Eq. [2.4.1.2.](#page-11-0) Substituting the LLM instantiation with s<sup>t</sup> = (x, y<t), a<sup>t</sup> = y t , γ = 1 yields Eq. [2.4.1.3](#page-11-1) giving gradient coefficient GCAC(x, y, t) = A<sup>π</sup> (x, y≤<sup>t</sup> ).

<span id="page-11-1"></span>
$$
\nabla_{\theta} J_{\text{AC}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} \left[ \sum_{t=1}^{|y|} A^{\pi}(x, y^{\leq t}) \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{(2.4.1.3)
$$

# <span id="page-11-5"></span>2.4.2 TRPO and PPO

The actor-critic gradient places no constraint on how far the policy moves per step; an unconstrained update can invalidate the advantage estimates and catastrophically destroy pretrained capabilities. TRPO [\(Schulman et al., 2017a\)](#page-107-3) constrains each update to a KL trust region (Eq. [2.4.2.1\)](#page-11-2), originally enforced via the Fisher information matrix, natural gradient, conjugate gradient, and backtracking line search. A later variant relaxes this hard constraint into a KL penalty (Eq. [2.4.2.2\)](#page-11-3) to reduce computational cost.

<span id="page-11-2"></span>
$$
J_{\text{TRPO}}(\theta) = \mathbb{E}_{s_t, a_t \sim \pi_{\theta_{\text{old}}}} \left[ \frac{\pi_{\theta}(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)} A^{\pi_{\theta_{\text{old}}}}(s_t, a_t) \right], \mathbb{E}_{s_t \sim \pi_{\theta_{\text{old}}}} [\text{KL}(\pi_{\theta_{\text{old}}}(\cdot|s_t) \| \pi_{\theta}(\cdot|s_t))] \le \varepsilon_{\text{KL}} (2.4.2.1)
$$

<span id="page-11-3"></span>
$$
J_{\text{TRPO-pen}}(\theta) = \mathbb{E}_{s_t, a_t \sim \pi_{\theta_{\text{old}}}} \left[ \frac{\pi_{\theta}(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)} A^{\pi_{\theta_{\text{old}}}}(s_t, a_t) \right] - \beta \mathbb{E}_{s_t \sim \pi_{\theta_{\text{old}}}} [\text{KL}(\pi_{\theta_{\text{old}}}(\cdot|s_t) \parallel \pi_{\theta}(\cdot|s_t))]
$$
  
= 
$$
\mathbb{E}_{s_t, a_t \sim \pi_{\theta_{\text{old}}}} \left[ \frac{\pi_{\theta}(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)} A^{\pi_{\theta_{\text{old}}}}(s_t, a_t) - \beta \log \left( \frac{\pi_{\theta_{\text{old}}}(\cdot|s_t)}{\pi_{\theta}(\cdot|s_t)} \right) \right]
$$
(2.4.2.2)

PPO [\(Schulman et al., 2017b\)](#page-107-1) replaces the KL penalty with a clipped surrogate. Rollouts from πθold are reused over multiple epochs, with ρ<sup>t</sup> = πθ(at|st) πθold(at|st) correcting for the distribution mismatch in Eq. [2.4.2.3](#page-11-4) for objective and Eq. [2.4.2.4](#page-12-0) for gradient where A<sup>t</sup> = A GAE(γ,λ) t in Eq. [2.4.1.2.](#page-11-0)

<span id="page-11-4"></span>
$$
J_{\text{PPO}}(\theta) = \mathbb{E}_{s_t, a_t \sim \pi_{\theta_{\text{old}}}} \left[ \sum_{t=1}^T \min(\rho_t A^{\pi_{\theta_{\text{old}}}}(s_t, a_t), \text{ clip}(\rho_t, 1-\varepsilon, 1+\varepsilon) A^{\pi_{\theta_{\text{old}}}}(s_t, a_t)) \right]
$$
(2.4.2.3)

<span id="page-12-5"></span><span id="page-12-0"></span>
$$
\nabla_{\theta} J_{\text{PPO}}(\theta) = \mathbb{E}_{s_t, a_t \sim \pi_{\theta_{\text{old}}}} \left[ \sum_{t=1}^{T} c_t \, \rho_t \, A^{\pi_{\theta_{\text{old}}}}(s_t, a_t) \, \nabla_{\theta} \log \pi_{\theta}(a_t | s_t) \right]
$$
(2.4.2.4)

The clipping indicator c<sup>t</sup> equals 0 when ρ<sup>t</sup> exceeds [1 − ε, 1 + ε] in the direction favored by AGAE t , zeroing the gradient, and 1 otherwise as shown in Eq. [2.4.2.5.](#page-12-1)

<span id="page-12-1"></span>
$$
c_t = 1 - \mathbb{I}[\rho_t > 1 + \varepsilon, A_t^{\text{GAE}} > 0] - \mathbb{I}[\rho_t < 1 - \varepsilon, A_t^{\text{GAE}} < 0]
$$
 (2.4.2.5)

Substituting the LLM setting s<sup>t</sup> = (x, y<t), a<sup>t</sup> = y t , γ = 1 and averaging over response length yields GCPPO = c<sup>t</sup> ρ<sup>t</sup> AGAE <sup>t</sup> with ρ<sup>t</sup> = πθ(y t |x,y<t) πθold(y t |x,y<t) in Eq. [2.4.2.6](#page-12-2) and Eq. [2.4.2.7.](#page-12-3)

<span id="page-12-2"></span>
$$
J_{\rm PPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\rm PPO}, y \sim \pi_{\theta_{\rm old}}(\cdot|x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \min(\rho_t A_t^{\rm GAE}, \, \text{clip}(\rho_t, 1-\varepsilon, 1+\varepsilon) A_t^{\rm GAE}) \right] \tag{2.4.2.6}
$$

<span id="page-12-3"></span>
$$
\nabla_{\theta} J_{\text{PPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{ppo}}, y \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} c_t \, \rho_t \, A_t^{\text{GAE}} \, \nabla_{\theta} \log \pi_{\theta}(y^t | x, y^{
$$

In standard RLHF, the per-token KL penalty is folded directly into the reward signal before advantage estimation: r<sup>t</sup> = rϕ(x, y≤<sup>t</sup> ) − β log <sup>π</sup>θ(<sup>y</sup> t |x,y<t) πref (y t |x,y<t) , so the GAE advantage AGAE t already incorporates the KL regularization.

### <span id="page-12-4"></span>2.4.3 RLHF

RLHF - OpenAI Building on the PPO framework derived above, the RLHF pipeline [\(Christiano et al., 2017;](#page-98-1) [Stiennon et al., 2020;](#page-107-0) [Ouyang et al., 2022;](#page-105-0) [OpenAI et al., 2024\)](#page-104-0) replaces automatic proxy metrics such as BLEU [\(Papineni et al., 2002\)](#page-106-2), ROUGE [\(Lin, 2004\)](#page-102-2), or BERTScore [\(Zhang et al., 2020\)](#page-112-0) with learned human preferences through a three-stage workflow: (1) SFT on human demonstrations initializes the reference policy πref (Eq. [2.2.1.1\)](#page-7-2); (2) Reward model training fits a pointwise reward rϕ(x, y) to human pairwise preferences via the Bradley–Terry (BT) model [\(Bradley and Terry, 1952\)](#page-98-2); (3) PPO optimizes the policy against r<sup>ϕ</sup> under a KL constraint to πref. The process of SFT is consistent with Section [2.2.1.](#page-7-5)

Reward modeling. For each prompt x, G candidate responses (typically G ∈ [4, 9]) are sampled from the SFT policy and presented to human labelers, who rank them from best to worst. These listwise rankings are reduced to <sup>G</sup> 2 pairwise comparisons, i.e., prompt x, preferred response y<sup>w</sup> and dispreferred response y<sup>l</sup> . Under the BT model, the probability that response y<sup>w</sup> is preferred over y<sup>l</sup> given prompt x is defined as P(y<sup>w</sup> ≻ y<sup>l</sup> | x) = σ[rϕ(x, yw) − rϕ(x, yl)]. Based on this formulation, we train the reward model by minimizing the binary cross-entropy loss in Eq. [2.4.3.1.](#page-12-4)

$$
L_{\rm RM}(r_{\phi}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}_{\rm RM}}\left[\log\left(\sigma\left(r_{\phi}(x,y_w) - r_{\phi}(x,y_l)\right)\right)\right] \tag{2.4.3.1}
$$

Training all <sup>G</sup> 2 comparisons jointly as a single batch rather than naively shuffling is essential to prevent overfitting from correlated candidate responses generated by the same prompt.

<span id="page-13-0"></span>Policy optimization. The policy is optimized using the KL-regularized objective in Eq. [2.4.2.3.](#page-11-4) Two structural differences distinguish this instantiation from generic PPO. First, generic PPO (inheriting from TRPO) constrains the forward KL DKL(πθold∥πθ) between successive iterates, whereas RLHF penalizes the reverse KL DKL(πθ∥πref). The reverse KL penalty DKL(πθ∥πref) = P y πθ(y)log <sup>π</sup>θ(y) πref (y) is zero-forcing: it diverges to +∞ whenever π<sup>θ</sup> places mass outside the support of πref, preventing the RL optimizer from reward-hacking via capability-destroying or degenerate outputs that the reference model considers essentially impossible. Second, the anchor πref is frozen after SFT, serving as a fixed trust anchor against reward hacking, whereas πθold in generic PPO is refreshed every iteration.

In practice, larger reward models (up to 175B) achieved lower validation loss but were unstable and expensive, leading the authors to adopt a single 6B model across all policy sizes. A remaining limitation is that all preference pairs are weighted equally regardless of score margins, motivating later listwise or strength-aware methods [\(Liu et al., 2025c\)](#page-103-0). Empirically, RLHF improved human preference win-rates on helpfulness, honesty, and harmlessness, reduced hallucination and toxicity [\(Lin et al., 2022\)](#page-102-3).

RLHF - Anthropic Anthropic's RLHF study [\(Bai et al., 2022a\)](#page-97-0) explores how datacollection strategy and model scale affect alignment across models ranging from 13M to 52B parameters. They selected crowdworkers for writing quality rather than label agreement, accepting lower researcher-crowdworker agreement (∼63%) in favor of data diversity, and separated "helpful" and "harmless" objectives into distinct datasets, collecting the latter via adversarial red-teaming where crowdworkers choose the more harmful model response to probe vulnerabilities. Although these objectives are strongly anti-correlated, i.e., training a PM on one alone yields worse-than-chance accuracy on the other, a single PM trained on combined data learns both effectively, with robustness to data mixture increasing with scale.

A central finding challenges the "alignment tax": RLHF degrades smaller models on standard NLP benchmarks but yields an alignment bonus for 13B and 52B models on nearly all zero-shot and few-shot evaluations, without mixing in pretraining gradients. Alignment is also compatible with specialized skills; RLHF improves Python-finetuned code models on HumanEval, and mixing summarization with HH preference data incurs no degradation in either task. PM accuracy scales roughly log-linearly with model and dataset size. To probe robustness, the authors split preference data 50:50 into separate train and test PMs, then train RL policies against the train PM while evaluating on the test PM. The two scores agree early but diverge at high reward, i.e., the train PM over-credits the policy, indicating reward over-optimization, though larger PMs are substantially more robust to this effect. The paper also identifies an approximately linear relationship between p DKL(π∥π0) and reward, with learning curves running roughly parallel across policy sizes, suggesting most of RLHF training remains in a perturbative regime around the initial policy. Finally, they propose iterated online RLHF, retraining PMs and policies on a roughly weekly cadence with fresh human feedback from deployed models, which yields substantially higher crowdworker Elo ratings.

# 2.4.4 DPO

RLHF with PPO uses a two-stage pipeline, i.e., reward model training followed by RL policy optimization, incurring substantial overhead from multiple models, dual data collection, and

<span id="page-14-2"></span>overfitting monitoring. To alleviate these complexities, DPO was proposed [\(Rafailov et al.,](#page-106-3) [2023\)](#page-106-3). Unlike REINFORCE and PPO, DPO was developed directly for the LLM setting and is natively formulated in terms of prompts x and complete responses y, bypassing the state-action formalism in MDP. DPO departs from the KL-penalty objective in Eq. [2.4.2.2](#page-11-3) by operating entirely offline: the preference pairs (yw, yl) are sampled from a static dataset typically generated by a separate model or collected from human annotators rather than rolled out from the current policy πθ. Because the training data distribution is fixed and independent of πθ, no importance-sampling ratio ρ<sup>t</sup> is required. The optimal policy π ∗ (y|x) is the maximizer of the KL-regularized reward objective in Eq. [2.4.2.2.](#page-11-3)

Given a reward model rθ(x, y), the optimal policy admits a closed-form solution (Eq. [2.4.4.1\)](#page-14-0), where Z(x) is a normalization constant depending only on the prompt, πref is the reference policy, and β controls deviation from it. Rearranging yields the reward expressed in terms of the policy.

<span id="page-14-0"></span>
$$
r_{\theta}(x,y) = \beta \log \left( \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) + \beta \log Z(x), \qquad Z(x) = \sum_{y} \pi_{\text{ref}}(y|x) e^{\frac{1}{\beta}r_{\theta}(x,y)} \qquad (2.4.4.1)
$$

This formulation enables joint optimization of the reward and policy. However, Z(x) is intractable due to summation over all outputs. DPO removes this term by considering reward differences between preferred and dispreferred responses. Substituting into the BT model yields the pairwise preference probability in Eq. [2.4.4.2,](#page-14-0) which is then used as a cross-entropy objective to obtain the final DPO loss in Eq. [2.4.4.3.](#page-14-0)

$$
P_{\theta}(y_w > y_l|x) = \sigma(r_{\theta}(x, y_w) - r_{\theta}(x, y_l)) = \sigma\left[\beta \log\left(\frac{\pi_{\theta}(y_w|x)}{\pi_{\text{ref}}(y_w|x)}\right) - \beta \log\left(\frac{\pi_{\theta}(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]
$$
(2.4.4.2)

$$
J_{\rm DPO}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}_{\rm DPO}} \log P_{\theta}(y_w > y_l|x)
$$
  
= 
$$
\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}_{\rm DPO}} \log \left\{ \sigma \left[ \beta \log \left( \frac{\pi_{\theta}(y_w|x)}{\pi_{\rm ref}(y_w|x)} \right) - \beta \log \left( \frac{\pi_{\theta}(y_l|x)}{\pi_{\rm ref}(y_l|x)} \right) \right] \right\}
$$
(2.4.4.3)

The gradient of this loss, shown in Eq. [2.4.4.4,](#page-14-1) increases the likelihood difference between the preferred and rejected responses, with a weighting term that emphasizes hard-to-separate pairs. Expanding to token level and negating (to match the unified maximization form in Eq. [2.1.1.1\)](#page-6-3), the gradient coefficient for each token of the preferred and dispreferred responses is GC<sup>w</sup> DPO(x, yw, yl) = β σ(rθ(x, yl) − rθ(x, yw)) and GC<sup>l</sup> DPO(x, yw, yl) = −β σ(rθ(x, yl) − rθ(x, yw)). The positive coefficient for y<sup>w</sup> increases its likelihood while the negative coefficient for y<sup>l</sup> decreases it. The gradient coefficient is constant across all tokens within each response, reflecting DPO's response-level formulation.

<span id="page-14-1"></span>
$$
\nabla_{\theta} J_{\text{DPO}}(\pi_{\theta}) = \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}_{\text{DPO}}} [\beta \sigma(r_{\theta}(x, y_l) - r_{\theta}(x, y_w))(\nabla_{\theta} \log \pi_{\theta}(y_w | x) - \nabla_{\theta} \log \pi_{\theta}(y_l | x))]
$$
(2.4.4.4)

The authors further showed that reward functions differing only by a prompt-dependent term f(x) are equivalent, implying that β log <sup>π</sup>θ(y|x) πref (y|x) suffices to recover the same optimal

<span id="page-15-3"></span>policy. Consequently, DPO directly learns the aligned policy without explicitly training a reward model, reducing RLHF to a simple classification loss. The framework is also extended to noisy labels by replacing the cross-entropy label weights in Eq. [2.4.4.3](#page-14-0) with ϵ and 1 − ϵ.

### <span id="page-15-0"></span>2.5 RLVR: GRPO

When ground-truth verification is available (e.g., mathematical correctness, code execution), RLHF can bypass learned reward models entirely and use verifiable rewards directly.

### <span id="page-15-1"></span>2.5.1 GRPO and RLOO

Like DPO, GRPO [\(Shao et al., 2024\)](#page-107-2) was designed directly for the LLM post-training setting and is natively formulated in terms of prompts and responses, without passing through the generic state–action MDP formalism used by REINFORCE and PPO. GRPO eliminates the value model by estimating the baseline from group scores. For each prompt x, a group of G responses {y1, . . . , yG} is sampled from πθold. One of the main architectural distinctions between PPO and GRPO lies in how the KL divergence term is handled. In PPO-based RLHF, the KL penalty is absorbed into the per-token reward r<sup>t</sup> before computing GAE advantages (Eq. [2.4.1.2\)](#page-11-0), so the clipped surrogate operates on KL-contaminated advantages; in GRPO, the clipped surrogate acts only on the raw reward-based advantage while the KL term is applied separately and unclipped. This decoupling keeps the advantage Ai,t computed purely from raw reward scores via group normalization that replaces the learned value function. Like PPO, GRPO uses a clipped importance-sampling surrogate for the advantage term in Eq. [2.5.1.1](#page-15-1)

$$
J_{\rm GRPO}(\theta) \tag{2.5.1.1}
$$

$$
= \mathbb{E}_{x \sim \mathcal{D}_{\text{GRPO}}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot|x)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \left( \min(\rho_{i,t} A_{i,t}, \text{clip}(\rho_{i,t}, 1-\varepsilon, 1+\varepsilon) A_{i,t}) - \beta \sum_{\text{KL}}^{(i,t)} \right) \right]
$$

where ρi,t = πθ(y t i |x,y<t i ) πθold(y t i |x,y<t i ) is the per-token importance ratio, and D (i,t) KL = πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − log <sup>π</sup>ref (<sup>y</sup> t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 is the Schulman KL estimator [\(Schulman, 2020\)](#page-106-4) for KL(πθ∥πref), guaranteed to be non-negative. Differentiating (with the same clipping indicator ci,t as in Eq. [\(2.4.2.5\)](#page-12-1), applied to the advantage term) yields Eq. [2.5.1.2.](#page-15-2)

<span id="page-15-2"></span>
$$
\nabla_{\theta} J_{\text{GRPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_{\text{GRPOd}}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \left( c_{i,t} \rho_{i,t} A_{i,t} \right) \right] + \beta \left( \frac{\pi_{\text{ref}}(y_i^t | x, y_i^{
$$

This yields the gradient coefficient GCGRPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , combining the clipped advantage term with the KL regularization.

The crucial distinction from PPO lies in the advantage computation. Rather than learning a value function, GRPO estimates the advantage via group normalization. Let µ(x) and <span id="page-16-3"></span>σ(x) denote the mean and standard deviation of the group rewards in Eq. [2.5.1.3](#page-16-0) and the GRPO advantage for response y<sup>i</sup> is then computed using Eq. [2.5.1.4.](#page-16-1)

<span id="page-16-0"></span>
$$
\mu(x) = \frac{1}{G} \sum_{j=1}^{G} r(x, y_j), \qquad \sigma(x) = \sqrt{\frac{1}{G} \sum_{j=1}^{G} (r(x, y_j) - \mu(x))^2}
$$
(2.5.1.3)

<span id="page-16-1"></span>
$$
A_{\rm GRPO}(x, y_i) = \frac{r(x, y_i) - \mu(x)}{\sigma(x)}
$$
\n(2.5.1.4)

Notably, AGRPO(x, yi) is computed at the response level, i.e., depending only on the total reward r(x, yi) for the entire response, yet is assigned as the gradient coefficient for every token t uniformly: Ai,t = AGRPO(x, yi) for all t = 1, . . . , |y<sup>i</sup> |. This contrasts with PPO's token-level GAE advantage AGAE t , which varies across positions within a response.

Another important distinction from PPO concerns the number of optimization steps per rollout. PPO reuses the same batch of rollouts from πθold over multiple gradient steps, updating θ several times before refreshing πθold with a new round of generation. GRPO, by contrast, performs only a single gradient update per rollout batch [\(Shao et al., 2024\)](#page-107-2), refreshing πθold after every update. However, both PPO and GRPO are defined as an on-policy training strategy in this survey.

REINFORCE leave-one-out (RLOO) [\(Williams, 1992;](#page-109-0) [Kool et al., 2019;](#page-101-1) [Ahmadian et al.,](#page-97-2) [2024\)](#page-97-2) predates GRPO and differs only in how the baseline is defined. In Eq. [2.5.1.5,](#page-16-2) the mean is computed by excluding the reward of the current response, and the standard deviation is fixed to 1.

<span id="page-16-2"></span>
$$
\mu(x, y_i) = \frac{1}{G - 1} \sum_{j=1, j \neq i}^{G} r(x, y_j), \qquad A_{\text{RLOO}}(x, y_i) = r(x, y_i) - \mu(x, y_i) \tag{2.5.1.5}
$$

# 2.5.2 DeepSeek R1

DeepSeek-R1 [\(Guo et al., 2025\)](#page-100-1) demonstrates that reasoning capabilities in LLMs can be incentivized through pure reinforcement learning, without relying on human-annotated reasoning trajectories. Using GRPO (Eq. [2.5.1.1\)](#page-15-1) as the RL algorithm on top of the DeepSeek-V3 base model, the authors first train DeepSeek-R1-Zero, which bypasses SFT entirely and uses only rule-based rewards combining accuracy verification (e.g., answer matching, code execution) and format adherence (<think>. . . </think> tags). Notably, neural reward models are deliberately avoided to prevent reward hacking during large-scale RL. During training, sophisticated reasoning behaviors, i.e., self-verification, reflection, and dynamic strategy exploration emerge organically without explicit instruction, including a striking "aha moment" where the model spontaneously learns to pause and re-evaluate its reasoning (e.g., generating "Wait, let me reconsider. . . ").

To address practical issues in R1-Zero such as poor readability and language mixing, the full DeepSeek-R1 adopts a multi-stage pipeline that alternates between SFT and RL:

1. Cold-start SFT. Starting from the base model, SFT on curated long CoT examples instills a clean <think>. . . </think> reasoning format before RL begins.

- <span id="page-17-1"></span>2. Reasoning-focused RL. Starting from the Stage-1 checkpoint, GRPO trains with rule-based rewards only (accuracy, format, language consistency).
- 3. Rejection sampling + SFT. The Stage-2 model generates candidates; the best are selected via rejection sampling and mixed with non-reasoning data (∼800K samples). SFT is then applied to the Stage-2 checkpoint, consolidating reasoning while restoring general-purpose capabilities.
- 4. All-scenario RL. Starting from the Stage-3 checkpoint, a second GRPO phase adds model-based preference rewards for helpfulness and safety alongside rule-based rewards for reasoning, polishing the model across all task types.

The two RL stages differ in both scope and reward design: Stage 2 targets reasoning tasks exclusively with rule-based rewards to safely bootstrap fragile reasoning skills, whereas Stage 4 broadens to all scenarios and introduces neural network-based preference rewards, which is feasible only after Stages 2–3 have solidified the model's reasoning foundation.

# 2.5.3 GRPO and RLVR Enhancement

Various RLVR methods have been proposed as modifications to the GRPO framework. A known degenerate case arises when all responses y within a group are either entirely correct or entirely incorrect, yielding zero advantages and rendering the update trivial. Dynamic sampling [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2](#page-58-0) has been introduced to address this issue by retaining only non-trivial prompts during training.

Regarding the importance sampling ratio, both PPO and GRPO compute ρi,t at the token level. Subsequent research has explored alternatives, including sequence-level ratios ρ<sup>i</sup> [\(Zheng et al., 2025\)](#page-112-1) in Section [5.1.2,](#page-38-0) or removing the importance ratio entirely in Section [5.4.3.](#page-59-0) For the clipping mechanism, PPO and GRPO both employ symmetric clipping, whereas several later works have proposed asymmetric clipping variants, i.e., clip higher [\(Yu et al.,](#page-110-0) [2025\)](#page-110-0) in Section [5.4.2.](#page-58-0)

On the reward side, different objectives can be pursued through the choice of reward signal: outcome rewards in Section [5.2.1,](#page-41-0) process rewards in Section [5.2.4,](#page-45-0) and length penalties in Section [5.2.2](#page-41-1) have each been investigated to serve distinct training goals. For the baseline, one may either train a separate critic model as in PPO in Section [2.4.2,](#page-11-5) or compute a baseline from group-level in Section [2.5.1](#page-15-1) or batch-level statistics (e.g., mean and standard deviation) in Section [5.4.3,](#page-59-0) or combine both approaches in Section [5.3.3.](#page-56-0)

Finally, concerning response length normalization, PPO and GRPO normalize by the individual response length <sup>1</sup> |yi| . Alternative approaches include group-level length normalization P 1 G <sup>i</sup>=1|yi| in Section [5.4.2,](#page-58-0) or omitting length normalization altogether.

### <span id="page-17-0"></span>2.6 Hybrid Post-Training (HPT)

Although the unified view shows that RL and SFT optimize the same objective, they exhibit opposite failure modes: on-policy RL collapses when the model cannot produce any correct rollouts, while SFT suppresses exploration once the model has surpassed its reference demonstrations. The optimal signal therefore depends on model capability, i.e., RL benefits stronger base models far more than weaker ones, whereas SFT remains helpful for both [\(Lv](#page-103-1) <span id="page-18-4"></span>[et al., 2025\)](#page-103-1), motivating a mechanism that selects the more informative gradient estimator per prompt.

HPT instantiates this unified view by dynamically switching between an on-policy RL loss (Dr. GRPO) in Section [5.4.3](#page-59-0) and an SFT loss based on per-prompt rollout performance. For each prompt x, the model draws G on-policy responses and computes the group mean µ(x) = <sup>1</sup> G P<sup>G</sup> <sup>i</sup>=1 r(x, yi) where r(x, yi) ∈ {0, 1} is a rule-based reward verifier. A gate threshold κ selects the training signal: when µ(x) > κ the model already shows competence, so RL fosters further exploration; otherwise SFT provides direct guidance as shown in Eq. [2.6.1.](#page-18-2) The gate defaults to κ = 0 for Qwen models and κ = 2/8 for LLaMA.

<span id="page-18-2"></span>
$$
(w_{\text{RL}}, w_{\text{SFT}}) = \begin{cases} (1, 0) & \text{if } \mu(x) > \kappa \\ (0, 1) & \text{if } \mu(x) \le \kappa \end{cases} \qquad L(\theta) = w_{\text{RL}} L_{\text{RL}}(\theta) + w_{\text{SFT}} L_{\text{SFT}}(\theta) \qquad (2.6.1)
$$

### <span id="page-18-0"></span>2.7 The Art of Scaling RL: ScaleRL

While RL compute budgets grow rapidly, the field still lacked a principled basis for predicting how performance scales with compute. [Khatri et al.](#page-101-2) [\(2026\)](#page-101-2) address this gap by modeling reward r<sup>C</sup> as a sigmoidal function of compute C (Eq. [2.7.1\)](#page-18-3), where A ∈ [0, 1] is the asymptotic performance ceiling, B > 0 controls compute efficiency, and Cmid is the compute at which half the total gain is achieved. This separates two frequently conflated objectives, i.e., raising the ceiling A vs. accelerating convergence B and enables reliable extrapolation from early, cheap runs to large-scale performance.

<span id="page-18-3"></span>
$$
r_C = r_0 + (A - r_0) \frac{1}{1 + \left(\frac{C_{\text{mid}}}{C}\right)^B}
$$
 (2.7.1)

Guided by a 400,000+ GPU-hour empirical study [\(Khatri et al., 2026\)](#page-101-2), the authors derive ScaleRL: an asynchronous RL recipe built on GRPO [\(Shao et al., 2024\)](#page-107-2) that integrates existing techniques into a single scalable combination. Concretely, it adopts the CISPO [\(MiniMax-M1 Team, 2025\)](#page-103-2) in Section [5.1.1.](#page-35-2)

The framework shows that RL compute can be scaled along four orthogonal axes, each trading off A against B in a predictable way. Model scale is the most impactful: the 17B×16 MoE matches and surpasses the 8B dense model using only one-sixth of the RL compute, with stable sigmoidal scaling throughout. Longer generation budgets and larger batch size raise A at the cost of lower initial B. Joint training on math and code preserves the sigmoidal structure per domain, confirming the framework generalizes beyond single-task settings.

### <span id="page-18-1"></span>2.8 Individual Paper Summaries

Algorithm [1](#page-19-1) for RLVR and Algorithm [2](#page-64-2) for RLHF share a unified policy-gradient form: at each token position the gradient of the log-policy is scaled by a gradient coefficient (GC) that encapsulates every method-specific design choice. Algorithm [1](#page-19-1) (RLVR) instantiates this as a three-stage loop: (i) prompt sampling with optional difficulty or reward-based filtering (Section [3\)](#page-19-0); (ii) generating a group of candidate responses scored by verifiable rewards, filtered to a subset via positive/negative splits or advantage thresholds (Section [4\)](#page-24-0); and (iii)

token-level GC assembly from an importance-sampling ratio (with optional clipping), an advantage term (reward minus baseline, with normalization and length adjustment), and a KL or entropy regularization (Section [5\)](#page-35-0). For a comprehensive taxonomy of RLVR, we refer the reader to Figure [2.](#page-20-0)

Algorithm [2](#page-64-2) (RLHF/DPO) reuses the same gradient form but branches from different directions: on-policy methods (Section [6\)](#page-63-0) generate fresh rollouts scored by a learned or AI reward model, while offline methods (Section [7\)](#page-70-0) draw pairwise, single, or listwise responses from a fixed dataset, shape the GC through divergence, entropy, or length regularisation, and optionally apply a post-training SFT merge. For a comprehensive taxonomy of RLHF and DPO, we refer the reader to Figure [6.](#page-63-1)

Accompanying per-paper summary tables catalogue these selections along two axes. Methodology tables (Tables [2](#page-114-0)[-6](#page-118-0) for RLVR; Tables [12-](#page-125-0)[13](#page-126-0) for RLHF methods) record design dimensions such as importance sampling, clipping, reward signal, baseline, normalization, KL penalty, and entropy bonus. Experimental tables (Tables [7–](#page-119-0)[11](#page-123-0) and Tables [14–](#page-127-0)[15\)](#page-128-0) summarise each paper's base model, training data, benchmarks, and compared methods. Each row is a self-contained snapshot; cross-referencing the two axes reveals not only what choices were made but under which conditions they were validated, with novel elements highlighted to make each paper's contribution easy to identify.

### Algorithm 1 RLVR: Key Design Choices

<span id="page-19-1"></span>**Unified Policy Gradient:** 
$$
\nabla_{\theta}J = \mathbb{E}_{(x,y)\sim\mathcal{D}}\left[\frac{1}{|y|}\sum_{t=1}^{|y|} \text{GC}(x,y,t)\nabla_{\theta}\log\pi_{\theta}(y^t | x, y^{< t})\right], \text{ GC}(x,y_i,t) = \frac{c_{i,t}\rho_{i,t} \cdot A_{i,t}^{\text{norm}} + \beta\left(\frac{\pi_{\text{ref}}}{\pi_{\theta}} - 1\right)}{5.1 \quad 5.2 \cdot 5.4}
$$
  
\n1: Intilalise:  $\pi_{\theta}$ ,  $\pi_{\text{ref}}$ ,  $\pi_{\theta}$ , group size  $G$   
\n2: for *iter* = 1, 2, ..., *N* do  
\n3: 3 Prombt Sampling sample  $x \sim \mathcal{D}$   
\n3.1 *Generation:* human-curate | synthetic self-player  
\n3.2 *Selection:* static curriculum | adaptive difficulty | reward-based filter  
\n4.3 *Selection:* data correlation:  $\frac{1}{\theta}$ , ...,  $\frac{1}{\theta}$ , compute  $r_i = r(x, y_i)$ ; on-policy | off-policy (replay / distillation) |  
\ntree-structured  
\n4.2 *Selection:* filter *G* to  $\tilde{G}$ ; positive/negative split | reward-based filter | advantage-based filter  
\n5: for  $y_i \in \tilde{G}$ ;  $t = 1, ..., y_i$  | do  
\n6: 5 *Gradient* Coefficient  
\n6: 5 *Gradient* Coefficient  
\n6: 5 *Gradient* Coefficient  
\n6: 5 *Action*, i.t. (key | do  
\n6: 5 *Gradient* Coefficient  
\n6: 5 *Action*  $A_i = r_i - b$ : *Reward:* ORM | PRM | hybrid; *Basic* is group mean | leave-one-out |  
\nvalue  $\pi_{\phi}$   
\n5.3 *Regularisation:* KL penalty | entropy bonus | none; *Len:* response | group | none  
\n5.5 *Regularisation:* KL penalty | entropy bonus | none  
\n7: *Accumulate:*  $g + = \text{GC}(x, y_i^t) \cdot \nabla_{\theta} \log \pi_{\theta}(y_i^t | x, y_i^{< t})$ 

# <span id="page-19-0"></span>3 RLVR: Prompt Sampling

This section surveys how training prompts are generated, ranging from human-curated datasets to fully synthetic self-play and selected, through static curricula, adaptive difficulty

![](./assets/01-rl-post-training-survey/_page_20_Figure_1.jpeg)

<span id="page-20-0"></span>Figure 2: Comprehensive RLVR taxonomy.

<span id="page-21-3"></span>scheduling, and reward-based filtering. Together, these two dimensions determine the quality, diversity, and difficulty of the experiences the policy model encounters.

### <span id="page-21-0"></span>3.1 Prompt Generation

Prompt generation determines the origin of training tasks, with two paradigms: humancurated data that offers high quality but requires annotation effort, and synthetic self-play that automates task creation to eliminate the human-data bottleneck entirely.

### 3.1.1 Human-generated Data

Human-curated prompts from math competitions, coding benchmarks, and domain-specific datasets provide high-quality training signal but require annotation effort and may not cover the full difficulty spectrum. Except Section [3.1.2,](#page-21-1) all the papers are based on human-generated data.

# <span id="page-21-1"></span>3.1.2 Synthetic Data

Synthetic data methods automatically generate training prompts without human annotation.

Absolute Zero The Absolute Zero paradigm [\(Zhao et al., 2025a\)](#page-112-2) eliminates dependence on human-curated data by having a single policy π<sup>θ</sup> simultaneously propose and solve tasks through self-play. The policy acts in two roles-proposer π propose θ and solver π solve θ -interacting with a code executor that serves as both task validator and reward verifier. Tasks are defined over program triplets (p, i, o) where o = p(i), yielding three reasoning modes: deduction (predict o given p, i), abduction (infer i given p, o), and induction (synthesize p from i, o). To estimate the learnability of a proposed task, i.e., whether it lies in the solver's zone of proximal development where G Monte Carlo rollouts {yi} G <sup>i</sup>=1 ∼ π solve θ (· | x) are sampled for a task query x at non-zero temperature, and the average solver success rate µsolve is computed. This difficulty estimate drives the proposer reward: tasks that are trivially easy (µsolve = 1) or completely unsolvable (µsolve = 0) yield zero reward, while tasks of moderate difficulty, where the solver occasionally succeeds, yield the highest reward, encouraging a self-improving curriculum. The proposer and solver rewards are defined in Eq. [3.1.2.1.](#page-21-2)

<span id="page-21-2"></span>
$$
r_{\text{solve}}(x, y) = \mathbb{I}(y = y^*), \quad \mu_{\text{solve}}(x) = \frac{1}{G} \sum_{i=1}^{G} r_{\text{solve}}(x, y_i)
$$

$$
r_{\text{propose}} = \begin{cases} 0 & \text{if } \mu_{\text{solve}}(x) = 0\\ 1 - \mu_{\text{solve}}(x) & \text{otherwise} \end{cases}
$$
(3.1.2.1)

Three types of tasks are explored: deduction, abduction, and induction. Both roles, i.e., proposer and solver are optimized jointly via Task-Relative REINFORCE++ (TRR++), a GRPO-based method (Eq. [2.5.1.1\)](#page-15-1) that removes KL divergence and adds entropy regularization. Importantly, the G rollouts above serve only the reward estimation (propose phase); they are not the rollouts used for the RL gradient update. For the update step, TRR++ departs from standard GRPO by generating a single response per prompt (G = 1) and computing the advantage baseline across the global batch grouped by (task, role), replacing the per-prompt advantage with a task-role-grouped advantage in Eq. [3.1.2.2](#page-22-1)

<span id="page-22-1"></span>
$$
A_{\text{task,role}}(x, y) = \frac{r_{\text{task,role}}(x, y) - \mu_{\text{task,role}}}{\sigma_{\text{task,role}}}
$$
(3.1.2.2)

<span id="page-22-3"></span>where task ∈ {ind, ded, abd}, role ∈ {propose,solve}, µtask,role and σtask,role are the mean and standard deviation of outcome rewards rtask,role(x, y) across all samples in the batch sharing the same (task, role) pair, yielding six separate baselines: an interpolation between per-question baselines (as in GRPO) and a global baseline. The gradient coefficient is GCTRR++(x, y, t) = ci,t ρi,t Atask,role, following the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2).

### <span id="page-22-0"></span>3.2 Prompt Selection

Prompt selection determines which prompts the policy trains on at each step, spanning static curricula, adaptive difficulty scheduling, and reward-based filtering that discards prompts yielding no gradient signal.

# <span id="page-22-2"></span>3.2.1 Static Curriculum

Static curricula pre-define the training data distribution or stage ordering before training begins. Aside from the following works, the Art of Scaling RL [\(Khatri et al., 2026\)](#page-101-2) in Section [2.7](#page-18-0) similarly employs a staged math-then-code data sequence.

Qwen 3 The Qwen 3 [\(Yang et al., 2025\)](#page-110-1) series introduces native thinking-mode with adaptive thinking-budget, allowing users to adjust inference-time compute without switching architectures. The series spans six dense models (0.6B through 32B) and two MoE variants, with flagship Qwen3-235B-A22B activating 22B of 235B parameters per forward pass. Language coverage expands from 29 to 119 languages. Post-training proceeds in four stages for flagship models (with a separate distillation path for lightweight models). Stage 1: Long-CoT Cold Start instills reasoning via filtered math, code, and STEM data. Stage 2: Reasoning RL employs GRPO [\(Shao et al., 2024\)](#page-107-2) (Eq. [2.5.1.1\)](#page-15-1) with outcome-based verifier reward r(x, y). Entropy regularization is used to control the model's entropy to increase steadily or remain stable. The training uses 3,995 query-verifier pairs, large batch sizes, a high number of rollouts per query, and off-policy training. The AIME'24 score increases from 70.1 to 85.1 over 170 RL training steps. Stage 3: Thinking Mode Fusion via SFT enables seamless switching between thinking and non-thinking modes. Stage 4: General RL combines rule-based rewards with model-based scoring. Strong-to-weak distillation (off-policy followed by on-policy) transfers capabilities to smaller models (0.6B–14B and 30B-A3B), requiring roughly <sup>1</sup> <sup>10</sup> of the GPU hours of RL for comparable gains.

OLMo 3 OLMo 3 [\(Olmo Team et al., 2025\)](#page-104-1) advances open-source AI by releasing a stateof-the-art language model with complete transparency, providing the full lifecycle including every training stage, checkpoint, data point, and dependency. The training pipeline proceeds through Pretraining, Mid-training, Long context, Thinking SFT, Thinking DPO, and finally RLVR, powered by OlmoRL, i.e., a GRPO-based reinforcement learning framework that integrates advances from DAPO [\(Yu et al., 2025\)](#page-110-0) and Dr.GRPO [\(Liu et al., 2025d\)](#page-103-3).

OlmoRL introduces six key improvements over vanilla GRPO: (1) zero-gradient filtering removes groups where all rewards are identical to prevent zero-advantage batches, akin to dynamic sampling in DAPO [\(Yu et al., 2025\)](#page-110-0); (2) active sampling dynamically replenishes <span id="page-23-0"></span>filtered slots to maintain a consistent batch size of non-zero-gradient completions; (3) tokenlevel group length normalization divides the loss by the total number of tokens across the batch rather than per-sample, following DAPO, to eliminate length bias; (4) no KL loss allows less-restricted policy updates without over-optimization or destabilization; (5) asymmetric clipping (clip-higher) sets εhigh > εlow to permit larger updates on high-advantage tokens; and (6) truncated importance sampling caps the log-probability ratio ρ between the inference and training engines to correct for off-policy drift. No standard-deviation normalization is applied to the group advantage, following Dr.GRPO, to avoid amplifying advantages on low-variance (too-easy or too-hard) questions.

Magistral Magistral [\(Mistral-AI et al., 2025\)](#page-104-2) is built on GRPO with G generations per prompt x from πθold and computes the baseline through the group mean µ(x) (Eq. [2.5.1.3\)](#page-16-0). With the input outcome reward r(x, yi), Magistral modifies GRPO (Eq. [2.5.1.1\)](#page-15-1) by: (i) removing the KL divergence term; (ii) using asymmetric clipping with distinct εlow and εhigh; (iii) replacing per-response length normalization with group length normalization <sup>P</sup> 1 G <sup>i</sup>=1|yi| ; (iv) using batch std for advantage normalization, i.e., first A<sup>i</sup> = r(x, yi) − µ(x) (group mean only, no group std), then Anorm i,t = Ai−Aˆ<sup>µ</sup> Aˆ<sup>σ</sup> across the minibatch; and (v) dynamic sampling, which filters out prompts whose responses all receive the same reward (zero advantage), reducing gradient noise. Lastly, entropy regularization is not used.

Reward shaping focuses on formatting (proper use of think tags), correctness (using SymPy for math and C++20 compilers for code), and language consistency via a classifier ensuring the internal monologue matches the user's prompt language. Training data is restricted to problems with verifiable solutions. The distributed, asynchronous RL pipeline has three components: Trainers for weight updates, Generators for rollouts, and Verifiers for reward calculation. Generators operate continuously, receiving weight updates while still generating tokens.

### 3.2.2 Adaptive Difficulty Curriculum

Adaptive difficulty curricula continuously adjust prompt selection based on the current policy's live performance, avoiding rigid fixed schedules. Beyond AdaRFT, SPO [\(Xu and](#page-110-2) [Ding, 2026\)](#page-110-2) in Section [5.2.5](#page-49-0) incorporates difficulty-weighted prompt sampling via a persistent per-prompt Beta value tracker.

Adaptive Curriculum Reinforcement Finetuning (AdaRFT) [Shi et al.](#page-107-6) [\(2025\)](#page-107-6) proposes AdaRFT, an adaptive curriculum for reinforcement fine-tuning that overcomes the rigidity of static data filtering (pre-selecting a fixed subset of prompts once, typically by reference difficulty) and fixed difficulty schedules (moving the target difficulty by a pre-defined rule regardless of learning progress). Each prompt x is sent to a reference LLM to generate multiple responses and their average reward is computed as µref(x, y). Then, the difficulty score is assigned to the prompt as d = 100 × (1 − µref(x, y)).

AdaRFT maintains a global target difficulty d<sup>T</sup> (on the same 0–100 scale as d, but not tied to any single prompt) that is updated online based on the current policy's batch-average reward µθ(x, y) (i.e., the same reward averaged over the selected batch, but under the current policy rather than the reference model) as in Eq. [3.2.2.1](#page-24-1)

<span id="page-24-1"></span>
$$
d_T \leftarrow \text{clip}(d_T + \eta \cdot \tanh(\alpha \cdot (\mu_\theta(x, y) - p^*)), d_{min}, d_{max})
$$
\n(3.2.2.1)

<span id="page-24-2"></span>where η > 0 is the update step size, α > 0 is the sensitivity scaling factor that controls saturation of the reward gap, p <sup>∗</sup> ∈ R is the target reward threshold, and dmin, dmax are the clipping bounds that keep d<sup>T</sup> within a valid operating range.

During training, AdaRFT forms a feedback loop: given a target difficulty d<sup>T</sup> , it samples the B prompts with smallest |d<sup>i</sup> −d<sup>T</sup> | (closest to d<sup>T</sup> ), then applies any standard RL optimizer (e.g., PPO/GRPO/REINFORCE++) to update the policy model parameters on this batch and compute the resulting batch-average reward µθ(x, y); finally, it updates d<sup>T</sup> by the rule above to keep the success rate near p ∗ (harder when µθ(x, y) > p<sup>∗</sup> , easier when µθ(x, y) < p<sup>∗</sup> ). The paper motivates p <sup>∗</sup> ≈ 0.5 for binary rewards since the learning signal is strongest near a 50% success rate. AdaRFT is algorithm-agnostic and is instantiated with PPO in this work.

### 3.2.3 Reward-based Filtering

Reward-based filtering removes prompts whose rollouts yield no useful gradient signal, specifically those where all rollouts are correct and the group advantage collapses to zero. Aside from SRPO, dynamic sampling strategies, i.e., DAPO [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2,](#page-58-0) OLMo 3 [\(Olmo Team et al., 2025\)](#page-104-1) in Section [3.2.1,](#page-22-2) and MAGIC [\(He et al., 2025\)](#page-100-3) in Section [5.5.2](#page-61-0) also filter zero-advantage groups. In the Response Sampling section, GFPO [\(Shrivastava](#page-107-7) [et al., 2026\)](#page-107-7) in Section [4.2.2,](#page-32-1) PODS [\(Xu et al., 2025\)](#page-110-3) in Section [4.2.3,](#page-33-0) and CPPO [\(Lin et al.,](#page-102-4) [2025\)](#page-102-4) in Section [4.2.3](#page-33-1) apply analogous filtering at the response level.

Two-Staged history-Resampling Policy Optimization (SRPO) Vanilla GRPO faces three bottlenecks in cross-domain settings: (i) a response-length conflict: math benefits from long CoT while coding favors short outputs; (ii) degenerate groups where all G rollouts share the same reward, making AGRPO(x, yi) (Eq. [\(2.5.1.4\)](#page-16-1)) to zero; and (iii) premature saturation from insufficient data difficulty. SRPO introduces two mechanisms on top of the GRPO objective (Eq. [\(2.5.1.1\)](#page-15-1)). Two-stage training: Stage 1 trains on math-only data to develop extended CoT (reflective pauses, backtracking); Stage 2 adds coding data, building on the reasoning foundation. History Resampling (HR): at each epoch boundary, prompts x for which all G rollouts were correct are filtered out, retaining only mixed- or all-incorrect-outcome prompts. Mixed-outcome prompts guarantee non-zero reward variance and thus non-trivial AGRPO and all-incorrect prompts currently yield zero advantage but are kept because the updated π<sup>θ</sup> may partially solve them in later epochs, similarly to curriculum learning. The objective follows the GRPO formulation (Eq. [\(2.5.1.1\)](#page-15-1)), using the input outcome reward r(x, yi). Additionally, the advantage is zeroed for responses exceeding the maximum length. The gradient coefficient is GCSRPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t.

### <span id="page-24-0"></span>4 RLVR: Response Sampling

This section surveys how RLVR training responses are constructed and filtered. Response Generation covers rollout strategies ranging from on-policy sampling to off-policy replay, distillation, asynchronous pipelines, prefix-conditioned rollouts, and tree-structured sampling. Response Selection surveys filtering methods that determine which responses enter the policy gradient update.

<span id="page-25-2"></span>In Figure [3,](#page-25-1) five terms of response sampling, i.e., on-policy, off-policy, advantage filtering, prefix conditioned rollouts and tree rollouts are illustrated with examples. On-policy and off-policy refer to whether responses are sampled from the current training model itself or from a separate model; advantage filtering keeps only the most informative ones, while prefix-conditioned rollouts generate multiple completions branching from a shared prefix, and tree rollouts extend this idea by building a branching tree of partial rollouts that are selectively expanded into full responses.

![](./assets/01-rl-post-training-survey/_page_25_Figure_2.jpeg)

<span id="page-25-1"></span>Figure 3: Response Sampling including On-policy, Off-policy, Advantage filtering, Prefix conditioned rollouts and Tree rollouts.

# <span id="page-25-0"></span>4.1 Response Generation

Standard GRPO [\(Shao et al., 2024\)](#page-107-2) samples G independent responses on-policy per prompt. This subsection surveys six modifications to that baseline: on-policy rollouts (default); offpolicy replay buffers; distillation from a stronger teacher; asynchronous multi-node training; prefix-conditioned rollouts; and tree-structured rollouts.

# 4.1.1 On-policy Rollouts

On-policy rollouts serve as the foundation for PPO [\(Schulman et al., 2017b\)](#page-107-1), GRPO [\(Shao](#page-107-2) [et al., 2024\)](#page-107-2), and RLHF and RLVR approaches. In these methods, G responses are sampled from the current policy πθold and used to update the model for one or more optimization steps. Although the rollouts may originate from slightly earlier versions of the model, they are still generally treated as on-policy data. Unless explicitly stated otherwise, we assume methods follow the on-policy learning paradigm.

# <span id="page-26-1"></span>4.1.2 Off-policy: Replay Buffer

The following works augment GRPO [\(Shao et al., 2024\)](#page-107-2) with off-policy responses to improve data efficiency and stabilize training when on-policy rollouts collapse.

Replay-Enhanced Policy Optimization (RePO) GRPO's reliance on purely on-policy samples is both computationally expensive and fragile when all sampled responses receive the same reward, advantages collapse to zero and provide no gradient signal. RePO [\(Li](#page-101-3) [et al., 2025a\)](#page-101-3) augments on-policy training Gon from x ∼ D, {y on i } Gon <sup>i</sup>=1 ∼ πθold(·|x) with Goff off-policy responses retrieved from a replay buffer B: {y off i , πb(y off i |x)} Goff <sup>i</sup>=1 ∼ B(x, y), where π<sup>b</sup> is the behavior policy that originally generated each replay sample, broadening the sample set per prompt without additional rollouts. The combined objective is given in Eq. [4.1.2.1.](#page-26-0)

<span id="page-26-0"></span>
$$
J_{\text{RePO}}(\theta; \mathcal{B}) = \underbrace{J_{\text{on}}(\theta)}_{\text{current samples}} + \underbrace{J_{\text{off}}(\theta; \mathcal{B})}_{\text{replay samples}}
$$
(4.1.2.1)

Each term follows the GRPO objective (Eq. [2.5.1.1\)](#page-15-1) with the KL penalty removed, using the outcome reward r(x, y<sup>⋆</sup> i ) for ⋆ ∈ {on, off}. The importance ratios are ρ on i,t = πθ(y on,t i |x,y on,<t i ) πθold(y on,t i |x,y on,<t i ) and ρ off i,t = πθ(y off,t i |x,y off,<t i ) πb(y off,t i |x,y off,<t i ) . RePO estimates advantages separately for on-policy and offpolicy groups (split strategy): A<sup>⋆</sup> <sup>i</sup> = r(x,y<sup>⋆</sup> i )−µ(G ⋆) σ(G⋆) , where G <sup>⋆</sup> = {r(x, y<sup>⋆</sup> i )} G<sup>⋆</sup> <sup>i</sup>=1 and µ(·), σ(·) denote the group mean and standard deviation, respectively. The gradient coefficient is GCRePO(x, y<sup>⋆</sup> i , t) = ci,t ρ ⋆ i,t A<sup>⋆</sup> i,t, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term. The off-policy update activates only after a threshold epoch. Lately, four retrieval strategies (Full-scope, Recency-based, Reward-oriented, Variance-driven) are evaluated for sampling from the replay buffer and Recency-based and Reward-oriented consistently outperform the others.

Tapered Off-Policy REINFORCE (TOPR) In the off-policy setting, π<sup>θ</sup> is trained for many steps on data from a frozen behavior policy πb, leading to divergence. With negative rewards, naive off-policy REINFORCE collapses as π<sup>θ</sup> pushes their probabilities to zero, making the objective log(πθ) unbounded and pushing model logits toward negative infinity, eventually causing degenerate behavior. TOPR [\(Roux et al., 2025\)](#page-106-5) resolves this through an asymmetric taper applied separately per reward sign, enabling KL-free, fully offline fine-tuning that remains stable even as π<sup>θ</sup> diverges substantially from πb. Concretely, TOPR samples G responses per prompt from the frozen behavior policy πb, labels each with a binary reward r(x, y) ∈ {−1, +1}, and optimizes π<sup>θ</sup> over this off-policy dataset. The off-policy correction enters via the sequence-level importance ratio ρ = πθ(y|x) <sup>π</sup>b(y|x) = Q|y<sup>|</sup> t=1 πθ(y t |x,y<t) πb(y t |x,y<t) , which quantifies how much the current policy π<sup>θ</sup> has drifted from the data-generating distribution πb.

TOPR applies an asymmetric taper T to ρ differently for each reward sign. For positive responses (r(x, y) ≥ 0), T (ρ, 1, 1) uses the log-ratio surrogate 1 + log ρ, whose gradient with respect to θ reduces to ∇ log πθ, i.e., a gradient coefficient of 1 independent of ρ, yielding a SFT-style update that remains effective even when π<sup>θ</sup> has drifted far from π<sup>b</sup> and ρ ≪ 1, the regime where standard importance-weighted updates would vanish. For negative responses (r(x, y) < 0), T (ρ, 0, 1) clips ρ to [0, 1], bounding the gradient magnitude and preventing the destructive blow-up that arises in importance-weighted updates when ρ ≫ 1. The objective

<span id="page-27-3"></span><span id="page-27-0"></span>is Eq. [4.1.2.2,](#page-27-0) where T is defined in Eq. [4.1.2.3.](#page-27-1)

<span id="page-27-1"></span>
$$
J_{\text{TOPR}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_b(\cdot|x)} \Big[ \mathbb{I}\{r(x, y) \ge 0\} \mathcal{T}(\rho, 1, 1) r(x, y) + \mathbb{I}\{r(x, y) < 0\} \mathcal{T}(\rho, 0, 1) r(x, y) \Big] \tag{4.1.2.2}
$$
\n
$$
\mathcal{T}(\rho, a, b) = \begin{cases} a\Big(1 + \log \frac{\rho}{a}\Big) & \text{if } \rho < a \\ b\Big(1 + \log \frac{\rho}{b}\Big) & \text{if } \rho > b \\ \rho & \text{if } \rho \in [a, b] \end{cases} \tag{4.1.2.3}
$$

The resulting sequence-level gradient coefficient is GCTOPR(x, y) = I{r ≥ 0} r(x, y) + I{r < 0} clip(ρ, 0, 1) r(x, y). Crucially, positive-reward responses carry a constant gradient weight of 1 regardless of how much π<sup>θ</sup> has drifted from πb, while negative-reward responses are progressively downweighted as π<sup>θ</sup> moves away from the behavior policy.

### 4.1.3 Off-policy: Distillation

The following works augment on-policy rollouts with demonstrations from a stronger fixed teacher model. Aside from these works, Prefix-RFT [\(Huang et al., 2025\)](#page-101-4) in Section [4.1.5](#page-29-0) pursues a related goal, i.e., anchoring rollouts to expert prefixes.

Learning to reason Under oFF-policY guidance (LUFFY) On-policy RLVR is fundamentally limited by the model's initial capabilities: it cannot learn reasoning patterns that it cannot already self-generate, which often leads to training collapse in weaker models. To address this limitation, LUFFY [\(Yan et al., 2025\)](#page-110-4) incorporates off-policy reasoning traces from a stronger teacher (e.g., DeepSeek-R1), exposing the policy to strategies beyond its current reach. Concretely, LUFFY builds on GRPO and extends it to a mixed-policy setting. For each prompt x, it combines on-policy rollouts Gon = {y<sup>i</sup> ∼ πθold(· | x)} Gon <sup>i</sup>=1 with off-policy reasoning traces Goff = {y<sup>j</sup> ∼ πb(· | x)} Goff <sup>j</sup>=1 , dynamically balancing exploration and imitation. Since off-policy traces consistently yield high rewards, they receive high positive advantages when the model's own rollouts fail, enabling imitation; once the model succeeds, on-policy solutions dominate, preserving exploration. The advantage for each response, with the outcome reward r(x, y), is computed via group mean over all responses to the same prompt in Eq. [4.1.3.1.](#page-27-2)

<span id="page-27-2"></span>
$$
A_i = r(x, y_i) - \mu(x), \quad \mu(x) = \frac{1}{G} \sum_{i=1}^{G} r(x, y_i), \quad y_i \in \{ \mathcal{G}_{\text{on}} \cup \mathcal{G}_{\text{off}} \}
$$
(4.1.3.1)

The standard deviation normalization is removed following Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3). The mixed-policy objective applies a policy shaping function f(u) = <sup>u</sup> u+κ (with κ = 0.1) to the off-policy term and the standard clipped surrogate to the on-policy term, with group length normalization. In practice, the off-policy behavior policy π<sup>b</sup> is set to 1 (i.e., the teacher model's token probabilities are not computed), so the off-policy importance ratio simplifies to πθ(y t i | x, y<t i ), and the clip operation is omitted for off-policy rollouts. The objective is given in Eq. [4.1.3.2.](#page-28-0)

<span id="page-28-1"></span><span id="page-28-0"></span>
$$
J_{\text{LUFFY}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^{G_{\text{on}}} \sim \pi_{\theta_{\text{old}}}(\cdot | x), \{y_j\}_{j=1}^{G_{\text{off}}} \sim \pi_b(\cdot | x) \frac{1}{\sum_{y_j \in \mathcal{G}_{\text{off}}} |y_j| + \sum_{y_i \in \mathcal{G}_{\text{on}}} |y_i|}
$$

$$
\left[ \underbrace{\sum_{y_j \in \mathcal{G}_{\text{off}}} \sum_{t=1}^{|y_j|} f\left(\pi_{\theta}(y_j^t | x, y_j^{(4.1.3.2)
$$

The policy shaping function amplifies learning signals for low-probability but crucial tokens from off-policy traces, preventing entropy collapse. The gradient coefficient for the onpolicy term is GCLUFFY,on(x, y<sup>i</sup> , t) = ci,t ρi,t A<sup>i</sup> , identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) without the KL regularization term. For the off-policy term, differentiating through the shaping function yields GCLUFFY,off(x, y<sup>j</sup> , t) = f ′ πθ(y t j | x, y<t j ) A<sup>j</sup> , which up-weights low-probability tokens relative to the linear weighting in standard importance sampling.

Group Variance Policy Optimization (GVPO) GRPO suffers from training instability due to importance sampling weights and gradient clipping, and is further limited by its inherently on-policy sampling scheme. GVPO [\(Zhang et al., 2025b\)](#page-111-2) incorporates the closedform solution of the KL-constrained reward objective (Eq. [\(2.1.1\)](#page-5-3)) directly into the gradient weights, thereby improving stability and relaxing the strict reliance on on-policy updates. The implicit reward is consistent with DPO, i.e., rθ(x, y) = β log <sup>π</sup>θ(y|x) <sup>π</sup>θold(y|x) <sup>+</sup> <sup>β</sup> log <sup>Z</sup>(x). Although the partition function P Z(x) is intractable, it cancels out when the per-group weights satisfy G <sup>i</sup>=1 w<sup>i</sup> = 0. Let π<sup>b</sup> denote an arbitrary behavior policy, and GVPO's optimality guarantee holds for any π<sup>b</sup> whose support covers that of πref, enabling off-policy training without importance sampling). The resulting objective, with input reward r(x, yi), minimizes the mean squared error between the central distances of implicit and actual rewards, as shown in Eq. [4.1.3.3](#page-28-0)

$$
J_{\text{GVPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_b(\cdot|x)} \left[ -\frac{1}{G} \sum_{i=1}^G \left[ (r_\theta(x, y_i) - \mu_\theta(x)) - (r(x, y_i) - \mu(x)) \right]^2 \right] \tag{4.1.3.3}
$$

where µθ(x) = <sup>1</sup> G P<sup>G</sup> <sup>i</sup>=1 rθ(x, yi) is its group mean, µ(x) = <sup>1</sup> G P<sup>G</sup> <sup>i</sup>=1 r(x, yi) is the group mean of actual rewards. The sampling distribution π<sup>b</sup> can differ from πθ, enabling offpolicy training without importance sampling. The gradient coefficient is GCGVPO(x, y<sup>i</sup> , t) = β[(r(x, yi) − µ(x)) −(rθ(x, yi) − µθ(x))], constant across all tokens t within a response. Unlike GRPO, GVPO uses no importance sampling ratios, no clipping, and no group standard deviation normalization in the advantage.

### 4.1.4 Asynchronous Multi-node Training

GEPO [\(Zhang et al., 2025a\)](#page-111-3) targets distribution shift caused by stale rollout policies in heterogeneous asynchronous training by replacing the per-response IS ratio with a groupaveraged denominator.

<span id="page-29-3"></span>Group Expectation Policy Optimization (GEPO) GEPO [\(Zhang et al., 2025a\)](#page-111-3) addresses training instability in heterogeneous asynchronous RL, i.e., environments where high network latency widens the gap between the sampling policy πθold and the learning policy πθ, causing the sequence-level importance ratio ρ<sup>i</sup> = πθ(yi|x) πθold(yi|x) to have high variance and destabilize training. The key insight is to replace the per-response denominator πθold(y<sup>i</sup> | x) with a single group-level estimate shared by all G responses. For each prompt x and group {y1, . . . , yG} ∼ πθold(· | x), let π˜(y<sup>i</sup> <sup>|</sup> <sup>x</sup>) = <sup>π</sup>θold(yi|x) P<sup>G</sup> <sup>j</sup>=1 πθold(y<sup>j</sup> |x) be the within-group normalized weight. The group-level denominator is the expectation of πθold(y | x) under π˜ in Eq. [4.1.4.1.](#page-29-1)

<span id="page-29-1"></span>
$$
\mathbb{E}_{\tilde{\pi}}[\pi_{\theta_{\text{old}}}(y \mid x)] = \sum_{i=1}^{G} \tilde{\pi}(y_i \mid x) \pi_{\theta_{\text{old}}}(y_i \mid x) = \frac{\sum_{i=1}^{G} \pi_{\theta_{\text{old}}}(y_i \mid x)^2}{\sum_{i=1}^{G} \pi_{\theta_{\text{old}}}(y_i \mid x)}
$$
(4.1.4.1)

GEPO replaces ρ<sup>i</sup> with a sequence-level importance ratio in Eq. [4.1.4.2.](#page-29-2)

<span id="page-29-2"></span>
$$
\rho_i^{\text{GEPO}} = \frac{\pi_\theta(y_i \mid x)}{\mathbb{E}_{\tilde{\pi}}[\pi_{\theta_{\text{old}}}(y \mid x)]} \tag{4.1.4.2}
$$

Substituting ρ GEPO i for ρi,t in the GRPO objective and gradient (Eqs. [\(2.5.1.1\)](#page-15-1)–[\(2.5.1.2\)](#page-15-2)) yields the GEPO update directly. The resulting gradient coefficient is GCGEPO(x, y<sup>i</sup> , t) = ci,t ρ GEPO <sup>i</sup> Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but with the group-level importance ratio ρ GEPO i replacing the per-token ratio ρi,t.

### <span id="page-29-0"></span>4.1.5 Prefix-conditioned Rollouts

The following works address the cold-start problem by anchoring rollouts to expert prefixes, providing a denser reward signal for models that cannot solve problems from scratch. SRFT [\(Fu et al., 2025\)](#page-99-2) in Section [5.2.8](#page-53-1) and HPT [\(Lv et al., 2025\)](#page-103-1) in Section [2.6](#page-17-0) pursues the complementary goal of unifying SFT and RL in a single gradient objective.

Branch Rollouts and Expert Anchors for Densified Rewards (BREAD) The standard SFT + RL pipeline can fail for small language models when (1) expert traces are too complex for the student to express, rendering SFT uninformative, or (2) a poorly initialized policy rarely produces correct traces, leaving RL with sparse rewards. BREAD [\(Zhang et al.,](#page-112-3) [2025e\)](#page-112-3) is based on GRPO with G generations per prompt x ∼ D, {yi} G <sup>i</sup>=1 ∼ πθold(·|x, ypre), and computes the baseline through the group mean µ(x) and group standard deviation σ(x) (Eq. [2.5.1.3\)](#page-16-0). BREAD addresses both problems of GRPO by conditioning rollouts on a short expert prefix y pre rather than imitating full expert solutions. An Episode Anchor Search (EAS) binary-searches the expert trace for the shortest prefix such that rollouts {yi} G <sup>i</sup>=1 ∼ πθold(· | x, ypre) achieve nontrivial success; when the policy already solves the prompt, no prefix is used. As training progresses the anchor shortens, yielding a selfpaced curriculum that densifies rewards. The objective follows the GRPO formulation (Eq. [2.5.1.1\)](#page-15-1), using the outcome reward r(x, yi), with the data source changed to prefixconditioned rollouts (x, ypre), where the prefix y pre is an expert anchor selected via EAS. The per-token importance ratio becomes ρi,t = πθ(y t i |x,ypre,y<t i ) πθold(y t i |x,ypre,y<t i ) , and the advantage is computed via group normalization in Eq. [2.5.1.4.](#page-16-1) The gradient coefficient is GCBREAD(x, y<sup>i</sup> , t) =

<span id="page-30-2"></span>ci,t ρi,t Ai,t + β πref (y t i |x,ypre,y<t i ) πθ(y t i |x,ypre,y<t i ) − 1 , identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but with prefix-conditioned rollouts.

Prefix Reinforcement Fine-Tuning (Prefix-RFT) Unlike BREAD, which conditions all G rollouts on an EAS-selected expert prefix to densify rewards for cold-start models, Prefix-RFT [\(Huang et al., 2025\)](#page-101-4) targets the formal integration of SFT and RFT within a single training step: it mixes one hybrid trajectory (expert prefix concatenated with on-policy continuation) into the standard rollout group, and applies an entropy-based gradient mask on prefix tokens to selectively incorporate dense demonstration supervision without allowing it to dominate the RFT exploration signal. For each prompt x with an offline demonstration y ∗ , the authors:

- 1. Sample G − 1 on-policy rollouts y<sup>i</sup> ∼ πθold(· | x).
- 2. Construct one hybrid trajectory by concatenating a prefix of length L from y <sup>∗</sup> with an on-policy continuation from πθold(· | x, y<t).

Following the design of Dr. GRPO, the authors remove standard deviation normalization, length normalization, and the KL penalty, and the advantage is defined as A(x, yi) = r(x, yi) − µ(x). A key innovation is an entropy-based mask mi,t that selectively gates gradients of prefix tokens according to policy entropy as defined in Eq. [\(4.1.5.1\)](#page-30-0)

<span id="page-30-0"></span>
$$
m_{i,t} = \mathbb{I}[t > L] + \mathbb{I}[t \le L] \cdot \mathbb{I}[H(\pi_{\theta}(\cdot \mid x, y_i^{\n(4.1.5.1)
$$

where η is the k-th percentile entropy threshold: only the top-k% highest-entropy prefix tokens receive gradients, targeting uncertain junctures while avoiding sharp distribution shifts. The gradient coefficient is GCPrefix-RFT(x, y<sup>i</sup> , t) = mi,tci,tρi,tAi,t, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term and with the additional entropy-based mask mi,t. In addition, a cosine decay scheduler gradually reduces L over training, transitioning from imitation-heavy to exploration-dominant.

### 4.1.6 Tree-structured Rollouts

The following works introduce non-flat rollout structures for finer-grained credit assignment.

Tree-based Policy Optimization (TreePO) Standard RLVR approaches independently sample multiple trajectories per prompt, causing redundant KV cache computation across shared prefixes and only flat, coarse credit assignment. TreePO [\(Li et al., 2025b\)](#page-102-5) restructures rollouts as a shared-prefix tree to amortize computation over common prefixes and enable hierarchical advantage estimation at each branching depth. TreePO adopts DAPO's modifications: asymmetric clipping (εlow < εhigh), group length normalization <sup>P</sup> 1 G <sup>i</sup>=1|yi| , and dynamic rejection sampling that filters prompts where all responses are correct or all incorrect.

TreePO introduces a tree-based sampling scheme where, for each prompt x, the policy πθold expands an N-array tree up to depth dmax, sampling N continuations of at most Lseg tokens at each node. Each response decomposes into segments, and sub-groups sharing longer prefixes nest within shallower ones in Eq. [4.1.6.1.](#page-30-1)

<span id="page-30-1"></span>
$$
y_i = s_1 \oplus s_2 \oplus \dots \oplus s_j, \quad j \le d_{\text{max}}, \qquad G_{|J|} \subseteq \dots \subseteq G_2 \subseteq G_1 = G \qquad (4.1.6.1)
$$

<span id="page-31-3"></span>The key innovation is the tree-based advantage estimation that replaces the standard GRPO group advantage (Eq. [2.5.1.4\)](#page-16-1) with a hierarchical two-step normalization. First, sub-group advantages are computed at each tree depth j by subtracting the sub-group mean. Then, these sub-group advantages are averaged across depths and normalized by their standard deviation, incorporating the global variance normalization strategy from REINFORCE++. The tree-based advantage is given in Eq. [4.1.6.2](#page-31-0)

<span id="page-31-0"></span>
$$
A_{i,t} = \frac{\sum_{j=1}^{|J|} \hat{A}_{i,t,j}}{|J| \cdot \sigma\left(\{\hat{A}_{i,t,j}\}^{|J|-1}\right)}, \qquad \hat{A}_{i,t,j} = r(x, y_i) - \frac{1}{G_j} \sum_{j=1}^{G_j} r(x, y_{i,j})
$$
(4.1.6.2)

where i indexes the response, t indexes the token position, j indexes the tree depth, and G<sup>j</sup> denotes the set of trajectories sharing the same predecessor node at depth j. Note that Aˆ i,t,j = Aˆ i,j is constant across tokens t within a response since it depends only on the outcome reward r(x, yi) and the t subscript is inherited from the token-level policy gradient in which Ai,t appears. Each response participates in multiple sub-groups at different tree depths (from the root group G<sup>1</sup> = G down to the sibling group G|J<sup>|</sup> at the deepest shared branching point). This hierarchical advantage reveals nuanced segment-level differences among trajectories and provides more precise credit assignment than the flat group advantage. The gradient coefficient is GCTreePO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term.

VinePPO VinePPO [\(Kazemnejad et al., 2025\)](#page-101-5) is based on PPO with G response generations per prompt x ∼ D, {yi} G <sup>i</sup>=1 ∼ πθold(·|x), and estimates the baseline via a Monte Carlo (MC) value function VMC instead of a learned value network Vϕ. VinePPO addresses the credit assignment problem by exploiting the resettable structure of the language environment: any partial response (x, y<t) can be re-fed to the policy to sample alternative continuations. For each intermediate position t in a training trajectory, G auxiliary continuations y1, . . . , y<sup>G</sup> ∼ πθ(· | x, y<t), each generated autoregressively from position t to the terminal token, are sampled and their episode returns averaged to form the MC value estimate in Eq. [4.1.6.3,](#page-31-1) where r(x, y<t, yi) denotes the outcome reward for the full trajectory composed of prefix y <t and continuation y<sup>i</sup> .

<span id="page-31-1"></span>
$$
V_{\rm MC}(x, y^{\n(4.1.6.3)
$$

The advantage at token y t is then computed via Eq. [4.1.6.4](#page-31-2) with γ = 1 since language generation is an undiscounted finite-horizon problem and intermediate rewards are zero (r<sup>t</sup> = 0 for non-terminal tokens).

<span id="page-31-2"></span>
$$
A_{\rm MC,t} = r_t + \gamma V_{\rm MC}(x, y^{
$$

This replaces the GAE advantage in the PPO objective (Eq. [\(2.4.2.6\)](#page-12-2)). The auxiliary continuations y<sup>i</sup> are used exclusively for value estimation and do not enter the policy gradient. For any G ≥ 1 the resulting gradient is unbiased, and increasing G reduces estimator variance at the cost of additional sampling. The advantages are normalized to zero mean and unit variance across the entire training batch (batch std). The gradient coefficient is

<span id="page-32-3"></span>GCVinePPO(x, y<sup>i</sup> , t) = ci,t ρi,t AMC,t+β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , where ρi,t = πθ(y t i |x,y<t i ) πθold(y t i |x,y<t i ) , identical to the PPO gradient coefficient (Eq. [\(2.4.2.7\)](#page-12-3)) but with MC-based token-level advantages replacing GAE advantages and KL divergence following GRPO.

Serial GRPO (S-GRPO) Standard GRPO's binary outcome rewards fail to regulate intermediate reasoning processes, causing reasoning models to generate unnecessarily long chains of thought, a phenomenon known as overthinking. Unlike standard GRPO which samples G independent responses in parallel, S-GRPO [\(Dai et al., 2025b\)](#page-99-3) constructs a serial group via a two-phase rollout. In Phase 1, a single complete reasoning path y<sup>0</sup> is generated from πθold. In Phase 2, m positions are randomly sampled along y0; at each position the model is prompted to stop reasoning and produce an answer, yielding early-exit outputs {y1, . . . , ym} that truncate the same reasoning path at different depths. The serial group {y0, y1, . . . , ym} thus contains G = m + 1 outputs from a single reasoning path. A decaying reward assigns exponentially decreasing credit to successive correct answers along the path, with the outcome reward r(x, yi) defined in Eq. [4.1.6.5](#page-32-2)

<span id="page-32-2"></span>
$$
r(x, y_i) = \begin{cases} \frac{1}{2^{N_{\text{right}}-1}} & \text{if } y_i \text{ is correct} \\ 0 & \text{otherwise} \end{cases}
$$
 (4.1.6.5)

where Nright counts the number of correct answers up to and including position i (ordered by exit depth). Earlier correct exits receive higher reward, incentivizing the model to produce sufficient reasoning as early as possible. The advantage removes standard-deviation normalization compared to GRPO, computed as A<sup>i</sup> = r(x, yi) − µ(x). The objective follows the GRPO formulation (Eq. [2.5.1.1\)](#page-15-1) with the KL divergence term removed. The gradient coefficient is GCS-GRPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term.

### <span id="page-32-0"></span>4.2 Response Selection

Response selection determines which rollouts enter the policy gradient update. The methods include positive/negative separation, reward-based filtering, advantage-based pruning, and bootstrapped pass@k optimization.

# 4.2.1 Positive/Negative

Positive/negative separation treats correct and incorrect rollouts asymmetrically, applying different loss weights or masking to prevent negative samples from corrupting the baseline. Other than the following work, OREAL [\(Lyu et al., 2025\)](#page-103-4) in Section [5.1.1](#page-37-0) and TOPR[\(Roux](#page-106-5) [et al., 2025\)](#page-106-5) in Section [4.1.2](#page-26-0) have also applied asymmetric treatment to positive and negative responses.

# <span id="page-32-1"></span>4.2.2 Reward-based Filtering

Reward-based filtering selects a subset of rollouts based on a target metric before computing group advantages. Besides GFPO, RFT [\(Yuan et al., 2023a\)](#page-111-1) in Section [2.2.2](#page-7-6) pioneered the idea of selecting only correct rollouts for supervised fine-tuning.

<span id="page-33-4"></span>Group Filtered Policy Optimization (GFPO) GRPO's single scalar reward makes it difficult to jointly optimize multiple response properties (e.g., accuracy and brevity), often leading to length inflation. GFPO [\(Shrivastava et al., 2026\)](#page-107-7) addresses length inflation by sampling a larger group of G responses per prompt, filtering to a retained subset S ⊆ {1, . . . , G} of size k based on a target metric (e.g., response length or token efficiency <sup>r</sup>(x,yi) |yi| ), and computing advantages only within S. With the outcome reward r(x, yi), a binary mask m<sup>i</sup> = I[i ∈ S] zeroes out the advantage for rejected responses. The masked advantage is computed via group normalization within S, as given in Eq. [4.2.2.1.](#page-33-2)

<span id="page-33-2"></span>
$$
A_{i,t} = \frac{r(x, y_i) - \mu_S}{\sigma_S} m_i, \qquad \mu_S = \frac{1}{k} \sum_{i \in S} r(x, y_i), \quad \sigma_S = \sqrt{\frac{1}{k} \sum_{i \in S} (r(x, y_i) - \mu_S)^2} \quad (4.2.2.1)
$$

The GFPO objective utilizea the modified advantage Ai,t, adopts group length normalization P 1 G <sup>i</sup>=1|yi| (DAPO token-level loss aggregation only; symmetric clipping and KL divergence), and adds an entropy bonus λent H(πθ), as given in Eq. [4.2.2.2.](#page-33-3)

<span id="page-33-3"></span>
$$
J_{\rm GFPO}(\theta) = J_{\rm GRPO}(\theta) + \lambda_{\rm ent} H(\pi_{\theta})
$$
\n(4.2.2.2)

The gradient coefficient below is identical to GRPO

GCGFPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 − λent log πθ(y t i |x, y<t i ). Adaptive Difficulty GFPO further adjusts k per question based on real-time difficulty estimates via streaming reward quartiles, retaining more responses for harder problems and aggressively pruning easy ones.

# <span id="page-33-0"></span>4.2.3 Advantage-based filtering

The following works prune rollouts with near-zero normalized advantages, i.e., minimum variance before the expensive policy update, focusing gradient computation on the most contrastive response pairs.

Policy Optimization with Down-Sampling (PODS) RLVR training faces a compute asymmetry between cheap, parallelizable rollout generation and expensive policy updates, and since not all rollouts contribute equally, and beyond a certain group size, additional rollouts reduce reward variance and introduce redundant, low-contrast signal. PODS [\(Xu et al., 2025\)](#page-110-3) decouples the two phases by generating a full group of G rollouts per prompt x from πθold during inference, then training on only a strategically selected subset S ⊂ {1, . . . , G} of size m < G during the policy update. The objective follows the GRPO formulation (Eq. [2.5.1.1\)](#page-15-1) but restricts the sum to the selected subset S (averaging over m instead of G) and removes the KL penalty, with the outcome reward r(x, yi). The subset advantage is AS,i = r(x,yi)−µ<sup>S</sup> σ<sup>S</sup> , with µ<sup>S</sup> and σ<sup>S</sup> computed within the selected subset S. The key selection criterion is max-variance down-sampling: choose S to maximize Var({r(x, yi) | i ∈ S}), thereby preserving the strongest contrastive signals between successful and unsuccessful reasoning paths. The authors prove that the optimal subset always consists of the k highest-reward and (m−k) lowest-reward rollouts for some k:

<span id="page-33-1"></span>
$$
S^* = \underset{k \in \{0, \ldots, m\}}{\operatorname{argmax}} \text{Var}(\{r(x, y_1), \ldots, r(x, y_{m-k})\} \cup \{r(x, y_{G-k+1}), \ldots, r(x, y_G)\}) \quad (4.2.3.1)
$$

<span id="page-34-3"></span>where {y1, . . . , yG} are sorted so that r(x, y1) ≤ · · · ≤ r(x, yG). This reduces the combinatorial search to O(G log G) time (dominated by sorting), and in the common binary-reward setting simplifies to picking m/2 correct and m/2 incorrect rollouts. The gradient coefficient is GCPODS(x, y<sup>i</sup> , t) = ci,t ρi,t AS,i, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term.

Completion Pruning Policy Optimization (CPPO) CPPO [\(Lin et al., 2025\)](#page-102-4) reduces GRPO's training cost by pruning low-advantage completions before expensive forward passes, and reallocates the saved GPU capacity to additional prompts via dynamic completion allocation. GRPO's training cost scales with the group size G: computing the objective for each completion requires a forward pass through three models: πθ, πθold, and πref, yielding 3G forward passes per prompt. CPPO observes that the group-normalized advantage A<sup>i</sup> is computable before these forward passes as it depends only on rewards and completions with near-zero |A<sup>i</sup> | contribute negligibly to the policy gradient. CPPO performs response-level pruning: it modifies the GRPO objective (Eq. [\(2.5.1.1\)](#page-15-1)) by replacing the full group average 1 G P<sup>G</sup> <sup>i</sup>=1 with a restricted average <sup>1</sup> k P <sup>i</sup>∈I, where I = {i : |A<sup>i</sup> | is among the top-k values} and k = ⌊G(1−P)⌋ for pruning rate P. Entire completions are either retained or discarded based on their sequence-level advantage A<sup>i</sup> and token-level terms within a retained completion are unchanged. A dynamic completion allocation strategy then fills freed GPU memory with pruned completions from additional prompts, maximizing device utilization and further reducing total training steps. The objective, with the outcome reward r(x, yi), follows the GRPO formulation (Eq. [2.5.1.1\)](#page-15-1) but restricts the summation to a pruned subset I = {i ∈ {1, . . . , G} | |A<sup>i</sup> | is among the top-k values}, where k = ⌊G × (1 − P)⌋ for pruning rate P ∈ (0, 1]. The gradient coefficient is GCCPPO(x, y<sup>i</sup> , t) = I[i ∈ I] ci,t ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 .

### <span id="page-34-2"></span>4.2.4 Bootstrapped selection

PKPO [\(Walder and Karkhanis, 2025\)](#page-108-2) optimizes the pass@k objective rather than pass@1, assigning rank-weighted gradient contributions only to responses ranked k-th or higher.

Pass@k Policy Optimization (PKPO) Standard RLVR methods optimize pass@1, which prioritizes individual sample performance over the collective utility of the response group and limits exploration on harder problems where individually-sampled solutions are rarely correct. PKPO [\(Walder and Karkhanis, 2025\)](#page-108-2) addresses this by directly optimizing pass@k which is the expected maximum reward across k jointly sampled responses, preserving model diversity and unblocking learning on challenging task sets. For each prompt x ∼ D, G on-policy responses are sampled {yi} G <sup>i</sup>=1 ∼ πθ(·|x) with outcome rewards r(x, yi) and PKPO directly optimizes pass@k: the expected maximum reward over k i.i.d. responses in Eq. [4.2.4.1.](#page-34-0)

<span id="page-34-0"></span>
$$
J_{\rm PKPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^k \sim \pi_{\theta}(\cdot | x)} \left[ \max_{i \in \{1, \dots, k\}} r(x, y_i) \right]
$$
(4.2.4.1)

Sampling G responses and averaging over all size-k subsets yields a closed-form rank-weighted estimator (with r(1) ≤ · · · ≤ r(G) the sorted rewards) in Eq. [4.2.4.2.](#page-34-1)

<span id="page-34-1"></span>
$$
\hat{J}_{PKPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \sum_{i=k}^{G} \omega_i r_{(i)} \right], \quad \omega_i = \frac{\binom{i-1}{k-1}}{\binom{G}{k}} \tag{4.2.4.2}
$$

<span id="page-35-4"></span>Only responses ranked k-th or higher receive nonzero weight. Applying the leave-one-out principle, i.e., averaging each response's marginal contribution r(i) − maxj∈<sup>S</sup> r(j) across all size-(k−1) subsets S ⊂ {1, . . . , i−1} gives the gradient coefficient in Eq. [4.2.4.3.](#page-35-3)

<span id="page-35-3"></span>
$$
GC_{PKPO}(x, y_{(i)}) = \frac{1}{\binom{G}{k}} \sum_{\substack{S \subset \{1, \dots, i-1\} \\ |S| = k-1}} \left( r_{(i)} - \max_{j \in S} r_{(j)} \right)
$$
(4.2.4.3)

For binary rewards, incorrect responses receive zero gradient as the rewards are sorted in non-decreasing order and each correct response's gradient equals the fraction of size-k subsets in which it is the sole correct one. PKPO supports annealing k from large to 1 over training, shifting the objective from pass@k encouraging the model to explore diverse and low-probability solution strategies to pass@1 which demands high individual-sample accuracy and consolidates probability mass onto the most reliable solutions.

### <span id="page-35-0"></span>5 RLVR: Gradient Coefficient

This section surveys how recent RL fine-tuning methods modify the gradient coefficient along five orthogonal axes: (1) the importance sampling (IS) ratio, (2) advantage shaping, (3) advantage normalization, (4) length normalization, and (5) regularization. The two foundational baselines are PPO [\(Schulman et al., 2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0) and GRPO [\(Shao](#page-107-2) [et al., 2024\)](#page-107-2).

### <span id="page-35-1"></span>5.1 Importance Sampling Ratio

The IS ratio ρi,t = πθ(y t i |x,y<t i ) <sup>π</sup>θold(<sup>y</sup> t i <sup>|</sup>x,y<t i ) corrects for distribution shift when reusing data from πθold. This subsection surveys token-level IS and clipping, sequence-level IS and clipping, and complete elimination of the IS ratio. Among papers primarily discussed elsewhere, TOPR [\(Roux et al., 2025\)](#page-106-5) in Section [4.1.2](#page-26-0) also employs a sequence-level IS formulation. DAPO [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2,](#page-58-0) Reinforce-Rej [\(Xiong et al., 2025b\)](#page-109-1) in Section [5.4.2,](#page-58-1) and Lite PPO [\(Liu et al., 2026b\)](#page-103-5) in Section [5.4.2](#page-58-1) use asymmetric token-level clipping. ORZ [\(Hu et al., 2025b\)](#page-101-6) in Section [5.2.5,](#page-48-0) VC-PPO [\(Yuan et al., 2025\)](#page-110-5) in Section [5.2.5,](#page-47-0) VAPO [\(Yue et al., 2025\)](#page-111-4) in Section [5.2.5,](#page-48-1) and SPO [\(Xu and Ding, 2026\)](#page-110-2) in Section [5.2.5](#page-49-0) retain token-level IS.

# <span id="page-35-2"></span>5.1.1 Token-level

Token-level IS methods compute a separate importance ratio per generated token. These methods share the goal of preserving gradient signal for critical reasoning tokens while preventing dramatic updates, each through a different modification of the standard clipping or gating mechanism. PPO [\(Schulman et al., 2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0) in Section [2.4.2](#page-11-5) and GRPO [\(Shao et al., 2024\)](#page-107-2) in Section [2.5.1](#page-15-1) and DAPO [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2](#page-58-0) are the token-level IS baselines.

Clipped Importance Sampling Policy Optimization (CISPO) In GRPO, tokens with importance ratios ρi,t outside [1 ± ε] are fully zeroed by clipping. In long-reasoning regimes with repeated off-policy updates, this disproportionately suppresses low-probability

<span id="page-36-1"></span>but crucial reasoning pivots (e.g., "Wait", "Recheck"), harming entropy and performance. CISPO [\(MiniMax-M1 Team, 2025\)](#page-103-2) addresses this by replacing GRPO's clipped surrogate min(ρi,tAi,t, clip(ρi,t, 1 − ε, 1 + ε)Ai,t) with a REINFORCE-style objective, where the importance ratio is clipped inside a stop-gradient: sg(ρˆi,t) = sg (clip(ρi,t, 1 − εlow, 1 + εhigh)) scales each token as sg(ρˆi,t) Ai,t, where sg(·) denotes stop-gradient. With the input reward r(x, yi) being the outcome-based score, the advantage is computed via group mean and std normalization (Eq. [2.5.1.4\)](#page-16-1). In practice, ε IS low is set to a large value (effectively removing the lower bound) and only ε IS high is tuned, yielding asymmetric clipping. Group length normalization <sup>P</sup> 1 G <sup>i</sup>=1|yi| is applied across the group. Because sg(ρˆi,t) is treated as a constant during differentiation, the gradient reduces to sg(ρˆi,t) Ai,t ∇<sup>θ</sup> log πθ, yielding the gradient coefficient GCCISPO(x, y<sup>i</sup> , t) = sg(ˆρi,t) Ai,t so that no token gradient is ever zeroed out and no KL penalty or entropy regularization.

Soft Adaptive Policy Optimization (SAPO) Both GRPO and GSPO rely on binary hard clipping that zeros gradients at the token and sequence level respectively. SAPO [\(Gao et al., 2025\)](#page-100-4) replaces the hard clipping function in the GRPO objective (Eq. [2.5.1.1\)](#page-15-1) with a smooth, temperature-controlled soft gate f SAPO i,t (ρi,t), where A<sup>i</sup> = r(x,yi)−µ(x) σ(x) is the group-normalized advantage (Eq. [2.5.1.4\)](#page-16-1) and r(x, yi) is the outcome reward. The soft gating function is Eq. [5.1.1.1.](#page-36-0)

<span id="page-36-0"></span>
$$
f_{i,t}^{\text{SAPO}}(\rho_{i,t}) = \frac{4}{\tau_i} \sigma(\tau_i (\rho_{i,t} - 1)), \quad \tau_i = \begin{cases} \tau^+ & \text{if } A_i > 0 \\ \tau^- & \text{if } A_i \le 0 \end{cases}
$$
 (5.1.1.1)

The soft gate peaks at ρi,t = 1 and decays smoothly as the ratio deviates, so near-on-policy tokens receive full gradients while off-policy tokens are progressively down-weighted rather than zeroed. Setting τ <sup>−</sup> > τ <sup>+</sup> attenuates negative-advantage updates more aggressively, since they spread logit mass across many irrelevant tokens and are more prone to instability. The gradient coefficient is GCSAPO(x, y<sup>i</sup> , t) = wi,t(θ)ρi,t(θ)A<sup>i</sup> , where wi,t(θ) = 4 pi,t(θ) (1−pi,t(θ)) and pi,t(θ) = σ(τ<sup>i</sup> (ρi,t(θ) − 1)), replacing the hard clipping indicator ci,t in the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) with a smooth weight wi,t(θ).

Beyond 80/20 Rule Existing RLVR methods train uniformly on all tokens, neglecting that only a high-entropy minority of tokens serve as critical "forking" decision points while the majority of low-entropy tokens merely continue established reasoning paths. The key contribution is an entropy-based token filter that restricts policy gradient updates to the top-p<sup>ρ</sup> fraction of highest-entropy tokens per batch, based on the observation that highentropy minority tokens act as critical reasoning forks while low-entropy tokens merely follow established paths [\(Wang et al., 2025a\)](#page-108-3).

Let Hi,t denote the entropy of πθ(·|x, y<t i ) at position t in response y<sup>i</sup> , and τ<sup>ρ</sup> the batch-level threshold selecting the top-p<sup>ρ</sup> fraction. The objective modifies the DAPO formulation by multiplying each per-token contribution by I[Hi,t ≥ τρ] and adjusting the tokencount normalization from P<sup>G</sup> <sup>i</sup>=1|y<sup>i</sup> | to P<sup>G</sup> i=1 P|yi<sup>|</sup> <sup>t</sup>=1 <sup>I</sup>[Hi,t <sup>≥</sup> <sup>τ</sup>ρ]. The gradient coefficient is GCBeyond80/20Rule(x, y<sup>i</sup> , t) = I[Hi,t ≥ τρ]ci,t ρi,tA<sup>i</sup> , identical to the DAPO gradient coefficient but gated by the entropy indicator.

<span id="page-37-6"></span>Covariance-Based Entropy Regularization (Clip-Cov / KL-Cov) Policy entropy collapses in early RL training because a small fraction of tokens, i.e., those where high logprobability and high advantage coincide, drive disproportionately large entropy reductions, causing performance to plateau. While prior GRPO variants apply a uniform trust-region constraint to every token, Clip-Cov and KL-Cov identify and suppress only this responsible subset, leaving all remaining gradients untouched [\(Cui et al., 2025b\)](#page-99-4). A token-level centered cross-product over all Ntok rollout tokens quantifies this in Eq. [\(5.1.1.2\)](#page-37-1):

<span id="page-37-1"></span>
$$
Cov(y_i^t) = \left(\log \pi_{\theta}(y_i^t | x, y_i^{\n(5.1.1.2)
$$

where Ntok = P<sup>G</sup> <sup>j</sup>=1|y<sup>j</sup> | is the total token count, and advantages use GRPO group normalization A<sup>i</sup> = r(x,yi)−µ(x) σ(x) (Eq. [\(2.5.1.4\)](#page-16-1)). Two complementary strategies selectively suppress these high-covariance tokens, sharing the same objective structure (Eq. [\(5.1.1.3\)](#page-37-2))

<span id="page-37-2"></span>
$$
J(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} \ell_t \right]
$$
(5.1.1.3)

Clip-Cov (hard suppression) randomly selects ⌊r · Ntok⌋ tokens whose covariance falls in [ωlow, ωhigh] and zeros out their gradient (Eq. [\(5.1.1.4\)](#page-37-3)–[\(5.1.1.5\)](#page-37-4)):

<span id="page-37-3"></span>
$$
I_{\text{clip}} \sim \text{Uniform}(\{(i, t) \mid \text{Cov}(y_i^t) \in [\omega_{\text{low}}, \omega_{\text{high}}]\}, \lfloor r \cdot N_{\text{tok}} \rfloor)
$$
(5.1.1.4)

<span id="page-37-4"></span>
$$
\ell_t^{\text{clip}} = \begin{cases} \rho_t A_t & \text{if } t \notin I_{\text{clip}} \\ 0 & \text{if } t \in I_{\text{clip}} \end{cases}
$$
 (5.1.1.5)

KL-Cov (soft suppression) selects the top-k fraction of tokens ranked by covariance and, instead of removing them, adds a targeted forward KL penalty DKL(πθold∥πθ) to slow their update toward the rollout policy (Eq. [\(5.1.1.6\)](#page-37-5)–[\(5.1.1.7\)](#page-37-0)).

<span id="page-37-5"></span>
$$
I_{\text{KL}} = \{(i, t) \mid \text{Rank}(\text{Cov}(y_i^t)) \le k \cdot N_{\text{tok}}\}\
$$
\n(5.1.1.6)

<span id="page-37-0"></span>
$$
\ell_t^{\text{KL}} = \begin{cases} \rho_t A_t & \text{if } t \notin I_{\text{KL}} \\ \rho_t A_t - \beta D_{\text{KL}}(\pi_{\theta_{\text{old}}}(\cdot | x, y^{(5.1.1.7)
$$

KL-Cov does not use PPO-style clipping where the selective KL penalty serves as the trust-region constraint. The gradient coefficient is GCKL-Cov(x, y<sup>i</sup> , t) = ρ<sup>t</sup> A<sup>t</sup> for t /∈ IKL, and ρ<sup>t</sup> A<sup>t</sup> + β πθold(y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 for t ∈ IKL, penalizing divergence from the rollout policy πθold rather than a reference policy.

Outcome REwArd-based reinforcement Learning (OREAL) Unlike prior methods that apply GRPO-style advantage normalization without theoretical grounding for binary sparse rewards in long reasoning chains, OREAL [\(Lyu et al., 2025\)](#page-103-4) provides a principled framework that proves behavior cloning on BoN-sampled positives suffices for KL-regularized optimality, and replaces heuristic credit assignment with a co-trained token-level reward

<span id="page-38-3"></span>model. OREAL introduces two key ideas: (1) behavior cloning on Best-of-N positives with a KL constraint recovers the optimal policy and negatives are incorporated via a separate penalty term with hyperparameter ηneg and the reward shaping factor (1 − µ); (2) a co-trained token-level reward model w(x, y≤<sup>t</sup> ) produces per-token importance weights: ω + <sup>t</sup> = max(2σ(w)−1, 0) for reinforcing key tokens in y <sup>+</sup>, and ω − <sup>t</sup> = max(1−2σ(w), 0) for penalizing error-causing tokens in y <sup>−</sup>, providing credit assignment without a value network. Like GRPO, OREAL samples G responses per prompt from π<sup>θ</sup> using binary outcome reward r(x, y) ∈ {0, 1}, discards prompts where all responses are correct or all wrong, and selects one correct y <sup>+</sup> and one incorrect y <sup>−</sup> per prompt. The group accuracy rate µ = 1 G P<sup>G</sup> <sup>k</sup>=1 r<sup>k</sup> serves as the baseline. To maintain gradient consistency with the Best-of-N distribution, negative samples receive a shaped reward r ∗ (x, y) ≜ (1 − µ) r(x, y) and correspondingly, the negativesample loss applies a generalized preprocessing F(1 − µ) (e.g., F(1 − µ) ≜ ri−µ σ(x) in GRPO) as the advantage coefficient. The reward model w is co-trained with the policy via cross-entropy on binary outcome rewards: LCE = −E(x,y,r) [r log ˆr(x, y) + (1 − r) log(1 − rˆ(x, y))], where rˆ(x, y) = σ 1 |y| P|y<sup>|</sup> <sup>t</sup>=1 w(x, y≤<sup>t</sup> ) is the predicted probability of correctness.

<span id="page-38-1"></span>The OREAL objective (negating the loss) is in Eq. [5.1.1.8](#page-38-1)

$$
J_{\text{OREAL}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \sum_{t=1}^{|y|} \left( \omega_t^+ \mathbb{I}[r(x, y) = 1] \log \pi_{\theta}(y^t | x, y^{
$$

where ηneg is a hyperparameter that balances positive and negative terms. The gradient coefficient is GCOREAL(x, y, t) = ω + t I[r(x, y)= 1]−ηneg ω − t I[r(x, y)= 0]+β πold(y t |x,y<t) πθ(y t <sup>|</sup>x,y<t) − 1 , combining the token-weighted advantage terms with KL regularization.

### <span id="page-38-0"></span>5.1.2 Sequence-level

Sequence-level IS methods aggregate token-level probabilities into a single ratio per response in the following works. Apart from these works, TOPR [\(Roux et al., 2025\)](#page-106-5) in Section [4.1.2](#page-26-0) and Seed-GRPO [\(Chen et al., 2025\)](#page-98-3) in Section [5.2.3](#page-44-0) also employs a sequence-level IS ratio.

Group Sequence Policy Optimization (GSPO) GSPO [\(Zheng et al., 2025\)](#page-112-1) is motivated by the ill-posedness of GRPO's token-level importance sampling: applying a single-sample IS correction per token accumulates high-variance training noise over long sequences, leading to catastrophic and often irreversible model collapse. The key innovation is replacing GRPO's token-level importance ratio ρi,t with a sequence-level importance ratio ρ<sup>i</sup> , aligning the optimization unit with the reward unit. The objective is in Eq. [5.1.2.1](#page-38-2)

<span id="page-38-2"></span>
$$
J_{\text{GSPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \min(\rho_i(\theta) A_i, \text{ clip}(\rho_i(\theta), 1-\varepsilon, 1+\varepsilon) A_i) \right]
$$
(5.1.2.1)

<span id="page-39-4"></span>where the advantage uses group normalization as in GRPO (Eq. [\(2.5.1.4\)](#page-16-1)). The lengthnormalized sequence-level importance ratio is in Eq. [5.1.2.2.](#page-39-0)

<span id="page-39-0"></span>
$$
\rho_i(\theta) = \left(\frac{\pi_{\theta}(y_i|x)}{\pi_{\theta_{\text{old}}}(y_i|x)}\right)^{\frac{1}{|y_i|}} = \exp\left(\frac{1}{|y_i|}\sum_{t=1}^{|y_i|} \log \frac{\pi_{\theta}(y_i^t|x, y_i^{
$$

The <sup>1</sup> |yi| exponent serves as length normalization, embedded within the importance ratio rather than as a separate factor as in GRPO. The gradient is in Eq. [5.1.2.3](#page-39-1)

<span id="page-39-1"></span>
$$
\nabla_{\theta} J_{\text{GSPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} c_i \, \rho_i(\theta) \, A_i \sum_{t=1}^{|y_i|} \nabla_{\theta} \log \pi_{\theta}(y_i^t | x, y_i^{\lt t}) \right] \tag{5.1.2.3}
$$

where c<sup>i</sup> is the sequence-level clipping indicator (same form as Eq. [\(2.4.2.5\)](#page-12-1), with ρi(θ) and A<sup>i</sup> replacing per-token ρi,t and Ai,t), so the importance ratio for the entire response is clipped at once rather than per token. The gradient coefficient is GCGSPO(x, y<sup>i</sup> , t) = c<sup>i</sup> ρi(θ) A<sup>i</sup> , identical in structure to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but with the sequencelevel importance ratio and clipping indicator replacing their token-level counterparts, and without the KL regularization term. This uniform weighting also resolves a key source of MoE instability: expert token-routing can change after gradient updates, causing GRPO's per-token ratios ρi,t to fluctuate as numerator and denominator are evaluated under different sub-networks, previously requiring Routing Replay at extra memory cost. GSPO obviates this because ρi(θ) aggregates over the full sequence and remains stable despite routing changes.

Geometric-Mean Policy Optimization (GMPO) GRPO's arithmetic-mean aggregation of token-level importance-weighted rewards is sensitive to extreme ρi,t, driving aggressive updates and entropy collapse. GMPO [\(Zhao et al., 2026\)](#page-112-4) replaces it with the geometric mean, which is inherently outlier-robust. The objective with token-level clipping is Eq. [5.1.2.4](#page-39-2)

<span id="page-39-2"></span>
$$
J_{\text{GMPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \left\{ \prod_{t=1}^{|y_i|} \left| \min \left( \rho_{i,t} A_{i,t}, \Delta_{i,t} \right) \right| \right\}^{\frac{1}{|y_i|}} \cdot \text{sgn}(A_{i,t}) \right] \tag{5.1.2.4}
$$

where sgn(Ai,t) is the sign function (+1 if Ai,t > 0, −1 if < 0), restoring the correct optimization direction after the absolute value. Differentiating the unclipped objective derives Eq. [5.1.2.5](#page-39-3)

<span id="page-39-3"></span>
$$
\nabla_{\theta} J_{\text{GMPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} \left( \prod_{k=1}^{|y_i|} \rho_{i,k} \right)^{\frac{1}{|y_i|}} \sum_{t=1}^{|y_i|} A_{i,t} \nabla_{\theta} \log \pi_{\theta}(y_i^t | x, y_i^{(5.1.2.5)
$$

yielding GCGMPO = Q<sup>|</sup>yi<sup>|</sup> <sup>k</sup>=1 <sup>ρ</sup>i,k <sup>1</sup> |yi Ai,t: every token shares the sequence-level geometric mean of ratios rather than its individual ρi,t, giving a more balanced update. Since the

<span id="page-40-3"></span>geometric mean never exceeds the arithmetic mean (AM–GM inequality), |J ∗ GMPO|≤ |J ∗ GRPO|, giving a narrower objective range and lower variance. Because the geometric mean already dampens outlier ratios, GMPO can afford a wider clipping range (e −ε , e<sup>ε</sup> ) than GRPO's (1 − ε, 1 + ε), encouraging greater exploration without sacrificing stability.

# <span id="page-40-2"></span>5.1.3 No Importance Sampling Ratio

GPG [\(Chu et al., 2026\)](#page-98-4) discards the IS ratio entirely, reverting to on-policy REINFORCEstyle objectives at the cost of requiring fresh rollouts. Besides GPG, AAPO [\(Xiong et al.,](#page-109-2) [2025a\)](#page-109-2) in Section [5.2.7,](#page-52-0) OPO [\(Hao et al., 2025\)](#page-100-5) in Section [5.2.5](#page-49-1) also discard the IS ratio. Lite PPO [Liu et al.](#page-103-5) [\(2026b\)](#page-103-5) in Section [5.4.2](#page-58-1) and Dr.GRPO [Liu et al.](#page-103-3) [\(2025d\)](#page-103-3) in Section [5.4.3](#page-59-0) retain PPO-style clipping but effectively operate without an IS correction.

Group Policy Gradient (GPG) Unlike GRPO, which relies on a surrogate IS-ratio loss, PPO-style clipping, a reference model, and KL regularization, GPG [\(Chu et al.,](#page-98-4) [2026\)](#page-98-4) strips the training pipeline to a minimal REINFORCE-style objective, i.e., directly optimizing the original RL objective without any surrogate approximation, auxiliary model, or distributional constraint. GPG addresses two sources of bias in GRPO: (i) reward bias from std-normalization in the advantage; and (ii) gradient estimation bias from groups with identical rewards contributing zero gradient while batch averaging still divides by the full batch size. GPG replaces GRPO's clipped importance-sampling surrogate with the direct REINFORCE loss, eliminating the importance ratio, clipping, KL penalty, and the reference model. The advantage uses the input reward r(x, yi) with group mean baseline µ(x) (Eq. [2.5.1.3\)](#page-16-0) and sets Fnorm = 1 (no σ-normalization), removing the reward bias introduced by GRPO's group σ division. To address gradient estimation bias from groups with identical rewards, Accurate Gradient Estimation (AGE) rescales the loss by a batch-dependent factor αGPG = B <sup>B</sup>−<sup>M</sup> where M is the number of zero-gradient groups in a batch of B prompts. When αGPG exceeds αth, the batch is deferred and valid samples are accumulated into subsequent batches, preventing high-variance updates. Unlike GRPO's per-response length normalization <sup>1</sup> |yi| , GPG normalizes by the total token count <sup>P</sup> 1 G <sup>i</sup>=1|yi| across all responses. The objective follows Eq. [2.1.1.](#page-5-3) The policy gradient is given in Eq. [5.1.3.1.](#page-40-1)

<span id="page-40-1"></span>
$$
\nabla_{\theta} J_{\text{GPG}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{\sum_{i=1}^G |y_i|} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \alpha_{\text{GPG}} A_{i,t} \nabla_{\theta} \log \pi_{\theta}(y_i^t | x, y_i^{(5.1.3.1)
$$

The gradient coefficient is GCGPG(x, y<sup>i</sup> , t) = αGPGAi,t, where αGPG is a batch-level rescaling factor outside GC.

### <span id="page-40-0"></span>5.2 Advantage Shaping

While the previous subsection addressed the IS ratio that multiplies the advantage, this subsection surveys methods that reshape the advantage signal A<sup>i</sup> itself across eight design axes: 1. outcome rewards, 2. length-aware reward shaping, 3. self-certainty rewards, 4. process rewards, 5. baseline estimation, 6. partition function approximation, 7. advantage stability under homogeneous rewards, and 8. hybrid SFT–RL objectives. Methods whose primary contribution spans multiple subsections are cross-referenced.

# <span id="page-41-4"></span><span id="page-41-0"></span>5.2.1 Outcome Reward

Standard outcome reward models assign a scalar correctness score to each complete response, forming the basic advantage signal used by GRPO [\(Shao et al., 2024\)](#page-107-2), PPO [\(Schulman et al.,](#page-107-1) [2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0), and most other methods in this survey. In these works, the reward can also be regarded as token level, where all the previous rewards are zero except the last token which will be the outcome reward. After deriving the reward, the advantage is derived by subtracting a baseline (e.g., the group mean in GRPO, a learned critic in PPO) from the outcome score.

## <span id="page-41-1"></span>5.2.2 Length Penalty

The following works augment the outcome reward with a length-aware component to discourage verbose reasoning without sacrificing correctness. Apart from the following works, DAPO [Yu et al.](#page-110-0) [\(2025\)](#page-110-0) in Section [5.4.2](#page-58-0) and Lite PPO [Liu et al.](#page-103-5) [\(2026b\)](#page-103-5) in Section [5.4.2](#page-58-1) also include penalty for overlong responses.

Length-Controlled Policy Optimization (LCPO) Reasoning models generate CoT outputs of uncontrollable length, making it infeasible to allocate test-time compute to a userspecified budget while maintaining accuracy. LCPO [\(Aggarwal and Welleck, 2025\)](#page-97-3) directly addresses this by a length-aware reward r(x, y<sup>i</sup> , n<sup>∗</sup> ) that incorporates a user-specified token budget n <sup>∗</sup> appended to each prompt x. The underlying training objective otherwise follows the GRPO formulation (Eq. [\(2.5.1.1\)](#page-15-1)) with G generations, substituting this length-aware reward into the advantage computation in place of the standard r(x, yi). The exact-length variant (LCPO-Exact) symmetrically penalizes deviation from n <sup>∗</sup> via Eq. [\(5.2.2.1\)](#page-41-2)

<span id="page-41-2"></span>
$$
r(y, y^*, n^*) = \mathbb{I}(y = y^*) - \alpha_{\text{len}} |n^* - |y|| \qquad (5.2.2.1)
$$

where I(·) is the correctness indicator, |y| is the generated length, and αlen is the correctnesslength trade-off. The maximum-length variant (LCPO-Max) applies a soft upper-bound constraint via Eq. [\(5.2.2.2\)](#page-41-3), penalizing only over-budget outputs

<span id="page-41-3"></span>
$$
r(y, y^*, n^*) = \mathbb{I}(y = y^*) \text{clip}(\alpha_{\text{len}}(n^* - |y|) + \delta_{\text{offset}}, 0, 1)
$$
 (5.2.2.2)

where δoffset ensures slightly over-budget correct answers remain preferable to incorrect ones. LCPO-Exact enforces precise length matching; LCPO-Max allows the model to use fewer tokens when the problem does not require the full budget. The advantage is computed via group normalization with µ(x) and σ(x) as in Eq. [\(2.5.1.4\)](#page-16-1). The gradient coefficient is GCLCPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)).

GRPO-λ While length-penalty reward functions can mitigate overthinking in GRPO, they tend to cause premature training collapse: as completion length decreases, model accuracy abruptly collapses, often early in training. GRPO-λ [\(Dai et al., 2025a\)](#page-99-5) addresses this instability by dynamically adjusting the reward strategy based on the per-group correctness ratio. For each batch, query-completion groups are ranked by their correctness ratio. The top-λ fraction (those with sufficiently high correctness ratio, indicating mature reasoning

<span id="page-42-3"></span>capability) receive an efficiency-prioritized reward with a length penalty (Eq. [\(5.2.2.3\)](#page-42-0))

<span id="page-42-0"></span>
$$
r(x, y_i) = \begin{cases} 1 - \alpha_{\text{len}} \cdot \sigma\left(\frac{|y_i| - \mu_{\text{correct}}}{\sigma_{\text{correct}}}\right) & \text{if } \mathbb{I}(y_i = y^*) = 1\\ 0 & \text{otherwise} \end{cases}
$$
(5.2.2.3)

where µcorrect and σcorrect are the mean and standard deviation of completion lengths over correct responses within the group, and αlen controls the penalty strength. The remaining groups fall back to the standard accuracy-prioritized outcome reward r(x, yi) = I(y<sup>i</sup> = y ∗ ), prioritizing reasoning capability over efficiency. The advantage A<sup>i</sup> for each sample is computed via group normalization as A<sup>i</sup> = ri−µ(ri) σ(ri) and broadcast uniformly to all corresponding response tokens before the standard GRPO parameter update.

GRPO-LEAD GRPO's binary rewards yield no signal when all group responses agree, tolerate speculative guessing via zero reward for incorrect answers, and over-optimize easy problems. To solve these problems, GRPO-LEAD [\(Zhang and Zuo, 2025\)](#page-111-5) modifies the reward r(x, yi) and applies difficulty-aware advantage reweighting. The reward in Eq. [\(5.2.2.4\)](#page-42-1) uses the standardized length deviation z<sup>i</sup> = |yi|−µ<sup>ℓ</sup> σℓ+ϵ of correct responses (µ<sup>ℓ</sup> , σ<sup>ℓ</sup> are the mean and standard deviation of completion lengths within the group) to down-weight verbose solutions, and assigns −1 to incorrect ones

<span id="page-42-1"></span>
$$
r(x, y_i) = \begin{cases} \exp(-\alpha_{\text{len}} z_i) & \text{if } y_i = y^* \\ -1 & \text{if } y_i \neq y^* \end{cases}
$$
 (5.2.2.4)

where αlen > 0 controls length penalization strength. The group-normalized advantage A<sup>i</sup> = r(x,yi)−µ(x) σ(x) (Eq. [\(2.5.1.4\)](#page-16-1)), where µ(x) and σ(x) are the mean and standard deviation of rewards within the group, is then reweighted by a difficulty-aware logistic function w(x) in Eq. [\(5.2.2.5\)](#page-42-2)

<span id="page-42-2"></span>
$$
w(x) = C + \frac{B - C}{1 + \exp[k(x - x_0)]}, \qquad \hat{A}'_i = A_i \begin{cases} w(\mu(x)) & \text{if } A_i > 0\\ w(1 - \mu(x)) & \text{if } A_i \le 0 \end{cases}
$$
(5.2.2.5)

where B, C, k, and x<sup>0</sup> are hyperparameters controlling the sensitivity of the reweighting to problem difficulty. Correct responses on hard problems (µ(x)≈ 0 ⇒ w(µ(x))≈B) and incorrect responses on easy problems (µ(x)≈ 1 ⇒ w(1−µ(x))≈B) both receive amplified updates. The gradient coefficient is GCGRPO-LEAD(x, y<sup>i</sup> , t) = ci,t ρi,t Aˆ′ i , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but with the reweighted advantage Aˆ′ i replacing A<sup>i</sup> and without the KL regularization term.

Adaptive GRPO (Ada-GRPO) Ada-GRPO [\(Wu et al., 2025a\)](#page-109-3) addresses the format collapse problem in standard GRPO, where GRPO's accuracy-only objective creates a selfreinforcing cycle: the highest-accuracy format, typically Long CoT, is increasingly reinforced, suppressing more efficient formats (Direct Answer, Short CoT) regardless of task difficulty. It introduces a dynamic reward-scaling strategy that incentivizes less-used reasoning formats via a two-stage framework: SFT to teach four reasoning formats (Direct Answer, Short CoT, <span id="page-43-4"></span>Code, Long CoT), then RL with the scaled reward. Given the binary correctness reward r(x, yi) = I(y<sup>i</sup> = y ∗ ), Ada-GRPO scales the reward as Eq. [5.2.2.6](#page-43-0)

<span id="page-43-0"></span>
$$
r'(x, y_i) = \alpha_i(t) \cdot r(x, y_i), \qquad \alpha_i(t) = 1 + \frac{1}{2} \left( \frac{G}{F(y_i)} - 1 \right) \left( 1 + \cos \left( \frac{\pi t}{T} \right) \right), \qquad (5.2.2.6)
$$

where F(yi) counts how many responses in the group share the same reasoning format as y<sup>i</sup> (identified via format-specific special tokens, e.g., <Code></Code>), and <sup>t</sup> T is the fractional training progress. So αi(t) ∈ [1, G F(yi) ]: at t = 0 each format receives its full inverse-frequency boost <sup>G</sup> F(yi) ; as t → T the cosine schedule decays αi(t) → 1, eliminating the format bias once training stabilises. The scaled rewards r ′ (x, yi) replace r(x, yi) in the group-normalized advantage (Eq. [2.5.1.4\)](#page-16-1), i.e., A(x, yi) = <sup>r</sup> ′ (x,yi)−µ ′ (x) <sup>σ</sup>′(x) where µ ′ (x) and σ ′ (x) are the mean and standard deviation of the scaled rewards {r ′ (x, y1), . . . , r′ (x, yG)}. The model is then optimized with the GRPO objective (Eq. [2.5.1.1\)](#page-15-1). The gradient coefficient is GCAda-GRPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t + β πref (y t |x,y<t) πθ(y t <sup>|</sup>x,y<t) − 1 , identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2).

# <span id="page-43-3"></span>5.2.3 Self-Certainty Reward

When labeled outcome rewards are unavailable or unreliable, self-certainty rewards derive the training signal directly from the model's own output distribution, enabling label-free or unsupervised RL. The following approaches differ in how certainty is measured.

Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning Unlike prior RLVR methods that rely on labeled outcome rewards or verified answers as training signal, this work [\(Agarwal et al., 2025\)](#page-97-4) is motivated by the observation that instruction-tuned LLMs (i.e., after SFT but before RL post-training) already possess underappreciated reasoning capabilities that can be elicited by simply minimizing output entropy, i.e., concentrating probability mass on the model's most confident outputs without any labeled data. Entropy minimization (EM) achieves this through three methods, each targeting a distinct posttraining stage: unsupervised finetuning (EM-FT), RL with entropy-based rewards (EM-RL), and inference-time logit optimization (EM-INF).

EM-FT (unsupervised finetuning) directly minimizes the token-level entropy of the policy on self-generated outputs in Eq. [5.2.3.1](#page-43-1)

<span id="page-43-1"></span>
$$
J_{\text{EM-FT}}(\theta) = -\mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} \left[ \frac{1}{|y|} \sum_{t=1}^{|y|} H(\pi_{\theta}(\cdot | x, y^{(5.2.3.1)
$$

where H(πθ(· | x, y<t)) = − P <sup>j</sup>∈V πθ(j | x, y<t)log πθ(j | x, y<t) is the Shannon entropy over the vocabulary V.

EM-RL uses REINFORCE with G generations per prompt. Two alternative (not combined) entropy-based rewards r(x, y) are defined in Eq. [5.2.3.2.](#page-43-2)

$$
r_{\rm seq}(x,y) = \sum_{t=1}^{|y|} \log \pi_{\theta}(y^t \mid x, y^{
$$

<span id="page-43-2"></span>[Table Of Contents](#page-1-0) ↑

<span id="page-44-2"></span>The gradient coefficient is GCEM-RL(x, y, t) = Ai,t+β πref (y t |x,y<t) πθ(y t <sup>|</sup>x,y<t) − 1 , where r ∈ {rseq, rtok}, A<sup>i</sup> = r(x, yi) − b(x, yi) and b(x, yi) = <sup>1</sup> G−1 P j̸=i r(x, y<sup>j</sup> ) is the LOO baseline.

EM-INF reduces entropy at inference time without updating model parameters θ. At each decoding step, the model produces a logit vector z<sup>t</sup> ∈ R |V| via a standard forward pass and z<sup>t</sup> is then treated as a free variable and updated for a few gradient-descent steps (5–15 in practice) to minimize H(softmax(zt)) down to a floor δfloor, while θ remains frozen. This is equivalent to optimizing a standalone softmax layer with |V| parameters, so the overhead is negligible compared to the model's forward pass. After logit optimization, sampling-based decoding selects the next token as usual. Unlike temperature scaling which preserves the logit ordering, logit optimization can reorder non-top logits, potentially improving reasoning chains in high-uncertainty settings. The key limitation is that EM is most effective when model confidence correlates with correctness, while it is less suited when the pretrained model lacks the target reasoning behaviors or when the task diverges significantly from the pretraining distribution.

INTUITOR Current RLVR methods require domain-specific verifiers and gold-standard solutions, limiting their applicability to verifiable domains. INTUITOR [\(Zhao et al., 2025b\)](#page-112-5) replaces the outcome reward r(x, y) with a self-certainty reward rsc(x, y): an intrinsic confidence measure termed Reinforcement Learning from Internal Feedback (RLIF). Self-certainty is defined as the average KL divergence between a uniform distribution U over the vocabulary V and the model's next-token distribution in Eq. [5.2.3.3.](#page-44-0)

<span id="page-44-0"></span>
$$
r_{\rm sc}(x,y) = \frac{1}{|y|} \sum_{t=1}^{|y|} \mathrm{KL}\big(U \, \| \, \pi_{\theta}(\cdot | x, y^{
$$

This score rsc(x, y) replaces r(x, y) in the GRPO group-normalized advantage (Eq. [\(2.5.1.4\)](#page-16-1)). The gradient coefficient is GCINTUITOR(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t +β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)). A key design choice is using online selfcertainty from the evolving policy π<sup>θ</sup> rather than a frozen model, which prevents reward hacking.

Semantic Entropy EnhanceD GRPO (SEED-GRPO) GRPO treats all training prompts equally during updates, ignoring differences in model confidence. When an LLM produces diverse responses to the same prompt, it often signals uncertainty or limited reasoning ability and applying large updates in such cases can amplify noise in the reward signal and harm learning. Unlike standard GRPO, SEED-GRPO [\(Chen et al., 2025\)](#page-98-3) introduces prompt-level uncertainty-aware advantage modulation: it computes the semantic entropy of the response group and applies a monotonically decreasing scaling function to reduce the advantage magnitude for high-entropy (high-uncertainty) prompts, while also removing std-normalization A<sup>i</sup> = r(x, yi) − µ(x), length normalization, and KL divergence. Given G responses clustered into K semantic equivalence classes {C1, . . . , CK}, the semantic entropy is approximated via Monte Carlo in Eq. [5.2.3.4.](#page-44-1)

<span id="page-44-1"></span>
$$
SE(x) \approx -\frac{1}{K} \sum_{k=1}^{K} \log p(C_k | x), \quad p(C_k | x) = \sum_{y_i \in C_k} \pi_{\theta_{old}}(y_i | x)
$$
(5.2.3.4)

<span id="page-45-4"></span>The uncertainty-aware advantage is defined in Eq. [5.2.3.5](#page-45-1)

<span id="page-45-1"></span>
$$
\tilde{A}_i = A_i \cdot f\left(\alpha_s \frac{\text{SE}(x)}{\text{SE}_{\text{max}}(x)}\right) \tag{5.2.3.5}
$$

where SEmax(x) = log G is the maximum entropy (when every response falls into a distinct cluster), α<sup>s</sup> controls sensitivity, and f is a monotonically decreasing scaling function (linear by default). The gradient coefficient is GCSEED-GRPO(x, y<sup>i</sup> , t) = c<sup>i</sup> ρ<sup>i</sup> A˜ i , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but without KL regularization and with semantic entropy modulation of the advantage.

Entropy-Minimized Policy Optimization (EMPO) Unlike SEED-GRPO which still needs outcome rewards r(x, yi), EMPO [\(Zhang et al., 2025d\)](#page-112-6) replaces them entirely with semantic entropy as the sole reward signal: a lower semantic entropy indicates that the model's outputs cluster into fewer, more consistent meanings, which correlates with higher accuracy. Given x ∼ D and {yi} G <sup>i</sup>=1 ∼ πθold(·|x), EMPO clusters the responses into K meaning clusters {C1, . . . , CK} via semantic equivalence (regular expressions for math tasks; a DeBERTa-v3-large entailment model for free-form question answering). The semantic entropy over the meaning distribution is defined [\(Zhang et al., 2025d\)](#page-112-6) in Eq. [\(5.2.3.6\)](#page-45-2)

<span id="page-45-2"></span>
$$
H = -\sum_{k=1}^{K} p(C_k \mid x) \log p(C_k \mid x), \quad p(C_k \mid x) \approx \frac{|C_k|}{G} \tag{5.2.3.6}
$$

where |Ck| denotes the number of responses in cluster Ck. Each response y<sup>i</sup> receives a reward r(x, yi) equal to the probability of its assigned meaning cluster (Eq. [\(5.2.3.7\)](#page-45-3)), with all responses in the same cluster C<sup>k</sup> receiving identical rewards regardless of surface-level differences, directly incentivizing convergence toward larger, more dominant clusters and thus minimizing H.

<span id="page-45-3"></span>
$$
r(x, y_i) = p(C_k | x) \approx \frac{|C_k|}{G} \text{ where } y_i \in C_k \tag{5.2.3.7}
$$

This reward r(x, yi) replaces the external reward in the GRPO group-normalized advantage (Eq. [\(2.5.1.4\)](#page-16-1)): A<sup>i</sup> = r(x,yi)−µ(x) σ(x) . To prevent reward hacking, EMPO applies dual entropy thresholds Hlow and Hhigh: prompts with H < Hlow are excluded to preserve diversity and reduce the risk of overfitting to trivial predictions, while prompts with H > Hhigh are excluded because all responses are too scattered to provide reliable signal. The final EMPO objective follows the GRPO formulation (Eq. [\(2.5.1.1\)](#page-15-1)), subject to Hlow < H < Hhigh. The gradient coefficient is GCEMPO(x, y<sup>i</sup> , t) = I[Hlow < H < Hhigh]ci,t ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 with ρ = 1.

# <span id="page-45-0"></span>5.2.4 Process Reward

Dense process rewards provide intermediate feedback at the step level, enabling richer credit assignment than sparse outcome rewards at the end of the response.

<span id="page-46-4"></span>Process Reinforcement through IMplicit rEwards (PRIME) While dense process rewards provide token-level credit assignment far more informative than sparse outcome rewards, collecting step-level annotations at scale is prohibitively expensive. This motivates PRIME's implicit approach [\(Cui et al., 2025a\)](#page-98-5) that derives process rewards online from outcome labels alone. It maintains the LLM policy π<sup>θ</sup> and an implicit PRM πϕ. At each training iteration, π<sup>ϕ</sup> performs a forward pass over the current batch of rollouts to produce the token-level implicit process reward defined in Eq. [\(5.2.4.1\)](#page-46-0). The response-level implicit reward is obtained by summing over all tokens: r o (x, y) = P|y<sup>|</sup> <sup>t</sup>=1 r p (y t |x, y<t).

<span id="page-46-0"></span>
$$
r^{p}(y^{t}|x, y^{\n(5.2.4.1)
$$

The outcome reward r(x, y) is a rule-based verifier defined in Eq. [\(5.2.4.2\)](#page-46-1) for math and code respectively:

<span id="page-46-1"></span>
$$
r_{\text{math}}(x, y) = \begin{cases} 1 & \text{if matched} \\ 0 & \text{otherwise} \end{cases} \qquad r_{\text{code}}(x, y) = \frac{\sum \# \text{passes}}{\sum \# \text{test cases}} \tag{5.2.4.2}
$$

Once rollouts are graded by the outcome verifier, PRIME applies an accuracy filter to retain only prompts of medium difficulty, i.e., prompts for which the G rollouts contain a mix of correct and incorrect responses. Prompts where all rollouts are correct (too easy) or all are wrong (too hard) are discarded, yielding the filtered set T . With T so defined, π<sup>ϕ</sup> is updated online on the same batch via binary cross-entropy loss against the outcome labels (Eq. [\(5.2.4.3\)](#page-46-2)), keeping it calibrated to the current policy distribution and mitigating reward hacking from distribution shift.

<span id="page-46-2"></span>
$$
\mathcal{L}_{CE}(\phi) = -\mathbb{E}_{(x,y,r(x,y))\sim\mathcal{T}}[r(x,y)\cdot \log \sigma(r^{o}(x,y)) + (1 - r(x,y))\cdot \log(1 - \sigma(r^{o}(x,y)))]
$$
\n(5.2.4.3)

Given G rollouts {y1, . . . , yG} sampled from πθold(·|x) for each prompt x ∈ T , the advantage combines the dense process returns from π<sup>ϕ</sup> with sparse outcome rewards through a leave-one-out (LOO) baseline with no standard deviation normalization, as shown in Eq. [\(5.2.4.4\)](#page-46-3):

<span id="page-46-3"></span>
$$
A_{i,t} = \underbrace{\sum_{s=t}^{|y_i|} \gamma^{s-t} \left[ r^p(y_i^s | x, y_i^{\n(5.2.4.4)
$$

where µ p ϕ (y<sup>j</sup> |x) = <sup>1</sup> |y<sup>j</sup> | P|y<sup>j</sup> <sup>|</sup> <sup>s</sup>=1 r p (y s j |x, y<s j ) is the mean token-level process reward over response y<sup>j</sup> . The gradient coefficient is GCPRIME(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t, identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but without KL regularization.

Process sUpervised Reinforcement lEarning (PURE)) The standard approach in process-reward RL sums discounted future rewards to compute each step's value, but because PRM rewards are imperfect, this accumulation amplifies estimation errors and enables the model to exploit steps that receive spuriously high rewards. PURE [\(Cheng et al., 2025b\)](#page-98-6)

<span id="page-47-3"></span>replaces this sum-form with a min-form credit assignment so that only the worst reasoning step determines the response value. For an n-step response, let r p <sup>t</sup> denote the process reward assigned by the PRM to step t ∈ {1, . . . , n}, and let t<sup>w</sup> = arg min1≤t≤<sup>n</sup> r p <sup>t</sup> be the index of the worst step. Steps up to and including the worst step t<sup>w</sup> receive the minimum of all process rewards as return, and steps after t<sup>w</sup> contribute nothing. To implement this without changing the return computation logic, PURE transforms the raw process rewards via a temperature-controlled softmax that concentrates weight on the lowest-reward step (Eq. [5.2.4.5\)](#page-47-1)

<span id="page-47-1"></span>
$$
r_i^{p*} = \frac{\exp\left(-\frac{r_i^p}{T}\right)}{\sum_{j=1}^n \exp\left(-\frac{r_j^p}{T}\right)} r_i^p
$$
\n(5.2.4.5)

where T is the transform temperature, and r p∗ i denotes the transformed process reward (as distinguished from the raw PRM reward r p i ). For advantage estimation, PURE uses RLOO combining outcome verifiable rewards r o (x, yi) and token-level transformed process rewards r p∗ i,j . Given G responses {y1, . . . , yG} per prompt x with maximum generation length N (a hyperparameter, e.g., N = 8192), the advantage for response y<sup>i</sup> at token t is defined in Eq. [5.2.4.6.](#page-47-2)

<span id="page-47-2"></span>
$$
A_{i,t} = r_i^o - \frac{1}{G-1} \sum_{k \neq i} r_k^o + \underbrace{\sum_{j=t}^N \gamma^{j-t} r_{i,j}^{p*} - \frac{\sum_{k \neq i} \sum_{l=1}^N \sum_{j=l}^N \gamma^{j-l} r_{k,j}^{p*}}{(G-1)N}}
$$
(5.2.4.6)  
RLOO (outcome) (Frocess)

The process-reward baseline is normalized by the fixed maximum generation length N rather than the actual response length |yk| to avoid biasing the model toward shorter responses. The RLOO advantage uses a leave-one-out mean without standard-deviation normalization (i.e., advantage normalization is 1). The gradient coefficient is GCPURE(x, y<sup>i</sup> , t) = ρi,t Ai,t + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , following the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but without clipping and with the RLOO process-reward advantage replacing the group-normalized advantage.

### <span id="page-47-0"></span>5.2.5 Baseline Estimation

The baseline subtracted from the reward reduces gradient variance without introducing bias. While GRPO [\(Shao et al., 2024\)](#page-107-2) uses the group mean and PPO [\(Schulman et al., 2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0) a learned critic, this subsubsection surveys different baseline estimation from value function estimation, variance minimization and Bayesian based methods.

Value-Calibrated PPO (VC-PPO) VC-PPO [\(Yuan et al., 2025\)](#page-110-5) addresses PPO's failure in long-CoT tasks where output length collapses due to value initialization bias through two techniques: value pretraining and Decoupled GAE. Value pretraining initializes V<sup>ϕ</sup> by offline regression on Monte Carlo returns from a fixed SFT policy, eliminating the bias that arises when the value model is initialized from a reward model trained only on terminal tokens. Decoupled GAE assigns asymmetric λ values: λcritic = 1 for the value target (reducing to Monte Carlo returns for unbiased reward propagation in long sequences) and λactor = 0.95

<span id="page-48-3"></span>for the actor (reducing advantage variance). The value target with Decoupled GAE is given in Eq. [5.2.5.1](#page-48-1)

<span id="page-48-1"></span>
$$
V^{\text{target}}(x, y^{
$$

where δt+<sup>l</sup> = rt+<sup>l</sup> + γV (x, y<t+l+1) − V (x, y<t+<sup>l</sup> ) = rt+<sup>l</sup> + V (x, y<t+l+1) − V (x, y<t+<sup>l</sup> ) is the TD error with γ = 1 (Eq. [2.4.1.2\)](#page-11-0). The value model is trained with the standard PPO value function MSE loss. The gradient coefficient is GCVC-PPO(x, y, t) = ctρtA<sup>t</sup> , identical to the PPO gradient coefficient (Eq. [2.4.2.7\)](#page-12-3) but without KL regularization in the reward signal.

Value-Augmented Policy Optimization (VAPO) While VC-PPO addresses PPO's length-collapse failure, three further challenges remain in long-CoT RLVR: the fixed λpolicy cannot adapt to heterogeneous response lengths, symmetric clipping suppresses exploration of low-probability tokens, and per-sequence loss normalization biases gradient updates toward shorter sequences. VAPO [\(Yue et al., 2025\)](#page-111-4) introduces four additional modifications over VC-PPO.

Length-adaptive GAE replaces VC-PPO's fixed λpolicy = 0.95 with a response-lengthdependent value in Eq. [5.2.5.2](#page-48-2)

<span id="page-48-2"></span>
$$
\lambda_{\text{policy}} = 1 - \frac{1}{\alpha |y|} \tag{5.2.5.2}
$$

where α controls the bias–variance tradeoff. Clip-higher decouples the clipping range into εlow < εhigh, leaving more room for low-probability tokens to increase and mitigating entropy collapse. Token-level loss replaces the per-sequence average <sup>1</sup> <sup>|</sup>yi<sup>|</sup> with a global token average P 1 G <sup>i</sup>=1|yi| , giving longer sequences proportionally more weight. A positive-example NLL loss on the subset T = {y<sup>i</sup> | r(x, yi) = 1} of correct responses reinforces successful reasoning patterns. The NLL loss and combined objective are in Eq. [5.2.5.3.](#page-48-0)

<span id="page-48-0"></span>
$$
J_{\text{NLL}}(\theta) = \frac{1}{\sum_{y_i \in \mathcal{T}} |y_i|} \sum_{y_i \in \mathcal{T}} \sum_{t=1}^{|y_i|} \log \pi_{\theta}(y_i^t | x, y_i^{\le t}) \qquad J(\theta) = J_{\text{VAPO}}(\theta) + \alpha_{\text{NLL}} J_{\text{NLL}}(\theta)
$$
\n(5.2.5.3)

The gradient coefficient is GCVAPO(x, y, t) = ctρtA GAE(γ,λpolicy) <sup>t</sup> + αNLLI(y ∈ T ), where the first term is the PPO gradient coefficient (Eq. [2.4.2.7\)](#page-12-3) with length-adaptive λpolicy and asymmetric clipping (εlow, εhigh), and the second term is the positive-example NLL contribution with weight αNLL for correct responses (y ∈ T ). Unlike VC-PPO (β = 0), VAPO uses KL divergence (folded into per-token rewards as in standard RLHF PPO).

Open-Reasoner-Zero (ORZ) Unlike prior work that uses GRPO without a dedicated value network, ORZ [\(Hu et al., 2025b\)](#page-101-6) is the first open-source large-scale Reasoner-Zero training framework, adopting vanilla PPO with a learned critic V<sup>ϕ</sup> and batch-level advantage normalization in place of GRPO entirely. GRPO's group mean assigns a single scalar baseline

<span id="page-49-3"></span>to every token in a response and cannot identify which specific tokens are problematic, whereas ORZ's token-level critic assigns lower expected returns to states with repetitive patterns, making those token advantages strongly negative and actively discouraging degenerate generation. For each prompt x ∼ D, G different responses y<sup>i</sup> ∼ πθold(·|x) will be generated and estimates the baseline via a trained value function Vϕ(x, y<t i ). Setting both GAE parameters to unity (γ = 1, λ = 1) with a terminal-only binary outcome reward r(x, yi) ∈ {0, 1} (ri,t = 0 for t < |y<sup>i</sup> |, ri,|yi<sup>|</sup> = r(x, yi)), the GAE formula (Eq. [2.4.1.2\)](#page-11-0) simplifies via telescoping.

<span id="page-49-1"></span>
$$
A_{i,t}^{\text{GAE}(1,1)} = \sum_{k=0}^{|y_i|-t-1} \delta_{i,t+k} = \underbrace{\sum_{k=0}^{|y_i|-t-1} r_{i,t+k} + \underbrace{V_{\phi}(x, y_i)}_{=0} - V_{\phi}(x, y_i^{\n(5.2.5.4)
$$

Batch-level advantage normalization is applied, i.e., Aˆ i,t = A GAE(1,1) i,t −µbatch σbatch where µbatch and σbatch are the batch mean and standard deviation respectively. The gradient coefficient is GCORZ(x, y, t) = ctρtAˆ i,t, identical to the PPO gradient coefficient (Eq. [2.4.2.7\)](#page-12-3).

Optimal Policy Optimization (OPO) GRPO's loose on-policy setting causes large policy shifts, entropy collapse, and reduced output diversity, motivating OPO [\(Hao et al.,](#page-100-5) [2025\)](#page-100-5) to enforce strict exact on-policy training and to replace the group-mean baseline with a theoretically optimal variance-minimizing alternative. It makes two key changes: (1) it enforces exact on-policy training by eliminating the importance ratio ρi,t and clipping entirely, updating the policy only on freshly sampled responses; and (2) it replaces the group-mean baseline with an optimal variance-minimizing baseline. The theoretical optimal baseline minimizes the variance of the policy gradient estimator with respect to b and is given in Eq. [5.2.5.5.](#page-49-2) Under the assumption that token-level gradients are approximately orthogonal with identically distributed norms (∥∇<sup>θ</sup> log πθ(y|x)∥ <sup>2</sup>∝ |y|), the baseline simplifies to a length-weighted reward average over the G sampled responses.

<span id="page-49-2"></span>
$$
b^* = \frac{\mathbb{E}_{y \sim \pi_{\theta}(\cdot|x)} [\|\nabla_{\theta} \log \pi_{\theta}(y|x)\|^2 \ r(x,y)]}{\mathbb{E}_{y \sim \pi_{\theta}(\cdot|x)} [\|\nabla_{\theta} \log \pi_{\theta}(y|x)\|^2]} \approx \frac{\sum_{i=1}^G |y_i| r(x,y_i)}{\sum_{i=1}^G |y_i|}
$$
(5.2.5.5)

The advantage is A<sup>i</sup> = r(x, yi) − b ∗ (x) without group standard deviation normalization. Note the gradient does not include per-response length normalization <sup>1</sup> |yi| (unlike GRPO Eq. [\(2.5.1.1\)](#page-15-1)) and the length effect is instead absorbed by the optimal baseline b ∗ . The policy gradient is in Eq. [5.2.5.6.](#page-49-0)

<span id="page-49-0"></span>
$$
\nabla_{\theta} J_{\text{OPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \sum_{t=1}^{|y_i|} A_i \nabla_{\theta} \log \pi_{\theta}(y_i^t | x, y_i^{(5.2.5.6)
$$

The gradient coefficient is GCOPO(x, y<sup>i</sup> , t) = A<sup>i</sup> .

Single-stream Policy Optimization (SPO) GRPO's group-based design suffers from frequent degenerate groups and imposes synchronization barriers in distributed training that stall throughput in agentic settings with variable-length responses, motivating SPO [\(Xu](#page-110-2) [and Ding, 2026\)](#page-110-2) to abandon the group paradigm entirely. SPO generates a single response

<span id="page-50-5"></span>(G = 1) per prompt x ∼ D, y ∼ πθold(·|x), and estimates the value function via a persistent Bayesian value tracker. For the input binary reward r(x, y) ∈ {0, 1}, SPO maintains a Beta distribution to track the success probability, whose parameters and value estimate are updated as Eq. [5.2.5.7](#page-50-0)

<span id="page-50-0"></span>
$$
a(x) \leftarrow \kappa(x) a(x) + r(x, y), \quad b(x) \leftarrow \kappa(x) b(x) + (1 - r(x, y)), \quad \hat{v}(x) = \frac{a(x)}{a(x) + b(x)} \tag{5.2.5.7}
$$

where κ(x) = 2−D(x)/Dhalf discounts past observations by the KL divergence D(x) between the current policy and the policy that last acted on x, with half-life Dhalf. The advantage A(x, y) is computed using the pre-update baseline vˆ(x) firstly. Next, the advantage is normalized globally across the batch B (batch-level, not per-group as in GRPO) to derive Aˆ(x, y), as shown in Eq. [5.2.5.8](#page-50-1)

<span id="page-50-1"></span>
$$
\hat{A}(x,y) = \frac{A(x,y) - \mu_B}{\sigma_B} \qquad A(x,y) = r(x,y) - \hat{v}(x)
$$
\n(5.2.5.8)

where µ<sup>B</sup> and σ<sup>B</sup> are the mean and standard deviation of the raw advantages {r(x, y) − vˆ(x)}x∈B across the batch. The objective follows the PPO-Clip formulation (Eq. [\(2.4.2.3\)](#page-11-4)) with asymmetric clipping (Clip-Higher). The gradient coefficient is GCSPO(x, y, t) = c<sup>t</sup> ρ<sup>t</sup> Aˆ(x, y). It further enables prioritized sampling with weights w(x) ∝ p vˆ(x)(1 − vˆ(x))+ϵ, focusing computation on prompts near vˆ(x) ≈ 0.5.

# <span id="page-50-4"></span>5.2.6 Partition Function Estimation

The intractable partition function Z(x) in the closed-form optimal policy, i.e., π ∗ (y|x) ∝ <sup>π</sup>ref(y|x) exp r(x,y) β must be approximated or eliminated for tractable training. Other than the following methods, GVPO [\(Zhang et al., 2025b\)](#page-111-2) in Section [4.1.3](#page-28-0) cancel Z(x) to minimize the variance.

Mirror Descent Policy Optimization (MDPO) Standard RL methods fix a static reference policy throughout training, causing the KL anchor to grow stale as the policy evolves. MDPO [\(Kimi Team, 2025\)](#page-101-7) applies mirror descent: each iteration solves a KL-regularized subproblem (Eq. [\(2.1.1\)](#page-5-3) with πref replaced by πθold), then advances the KL center to the current policy. A length reward is added to the outcome reward, given in Eq. [5.2.6.1](#page-50-2)

<span id="page-50-2"></span>
$$
\hat{r}(x, y_i) = r(x, y_i) + w \cdot r_{len}(y_i), \quad r_{len}(y_i) = \begin{cases} \lambda & \text{if correct} \\ \min(0, \lambda) & \text{if incorrect} \end{cases}
$$
\n(5.2.6.1)

where λ = 0.5− |yi|− min1≤k≤G|yk| max1≤k≤G|yk|− min1≤k≤G|yk| . The KL-constrained problem admits a closed-form optimal policy π ∗ θ (y|x) <sup>∝</sup> <sup>π</sup>θold(y|x) exp r(x,y) β and MDPO fits πθ(y|x) to π ∗ θ (y|x) in squared error. The partition function β log Z(x) is estimated from the group mean reward µ(x). The resulting objective J(θ) = −L(θ) is given in Eq. [5.2.6.2.](#page-50-3)

<span id="page-50-3"></span>
$$
J(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ -\left( \hat{r}(x, y) - \mu(x) - \beta \log \frac{\pi_{\theta}(y | x)}{\pi_{\theta_{\text{old}}}(y | x)} \right)^2 \right]
$$
(5.2.6.2)

<span id="page-51-2"></span>The gradient coefficient is GCMDPO(x, yi) = 2β h rˆ(x, yi) − µ(x) − β log <sup>π</sup>θ(yi|x) πθold(yi|x) i . After each iteration, the reference policy is updated to the current policy and the optimizer state is reset. Lastly, the training process utilizes curriculum sampling (easy-to-hard) and prioritized sampling, where prompts with lower success rates receive more iterations.

Flow Reinforcement Learning (FlowRL) Reward-maximizing RL methods such as PPO and GRPO tend to overfit to dominant reward signals, causing mode collapse that reduces diversity among reasoning paths and limits generalization. Instead of the clipped surrogate objective, FlowRL [\(Zhu et al., 2025\)](#page-112-7) shifts to reward distribution matching by introducing a learnable partition function Zϕ(x) and minimizing DKL(πθ(·|x)∥π ∗ (·|x)) where π ∗ (y|x) = exp(r(x,y)/β)·πref (y|x) Zϕ(x) , which is equivalent to the trajectory balance objective in Eq. [5.2.6.3.](#page-51-0)

<span id="page-51-0"></span>
$$
J_{\text{FlowRL}}(\theta,\phi) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot|x)} \left[ -\rho \cdot \left( \log Z_{\phi}(x) + \frac{1}{|y|} \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} - \beta r(x,y) \right)^2 \right]
$$
(5.2.6.3)

where ρ = clip πθ(y|x) πθold(y|x) , 1 − ε, 1 + ε detach is a sequence-level, gradient-detached importance weight, rˆ(x, y) = <sup>r</sup>(x,y)−µ(x) σ(x) is the group-normalized outcome reward, and δ(x, y; θ, ϕ) = log Zϕ(x) + <sup>1</sup> |y| log <sup>π</sup>θ(y|x) <sup>π</sup>ref (y|x) −β r(x, y) is the flow-balance residual. The objective JFlowRL(θ, ϕ) is minimized jointly with respect to two learnable components: (1) the policy network πθ, whose parameters receive gradients through the log-probability term <sup>1</sup> |y| log πθ(y|x); and (2) the partition function network Zϕ, implemented as a 3-layer MLP, whose parameters receive gradients through the log Zϕ(x) term. At each training step, both θ and ϕ are updated simultaneously to drive the flow-balance residual δ(x, y; θ, ϕ) toward zero. The gradient coefficient is GCFlowRL(x, y) = −2ρ δ(x, y; θ, ϕ), with ρ detached so that the importancesampling correction does not itself contribute to the gradient signal and |y| is utilized for length normalization.

Group Implicit Fine Tuning (GIFT) Unlike GRPO which maximizes cumulative normalized rewards through a non-convex clipped surrogate requiring careful tuning of clipping hyperparameters and prone to overfitting, GIFT [\(Wang, 2025\)](#page-108-4) replaces this objective with a convex MSE loss that aligns normalized implicit rewards (from DPO's reward formulation) to normalized explicit rewards (from UNA's reward-alignment principle), while retaining GRPO's on-policy group sampling with G generations for stable exploration. DPO's implicit reward rθ(x, y) = β log <sup>π</sup>θ(y|x) <sup>π</sup>ref (y|x)+β log Z(x) contains an intractable partition function log Z(x). GIFT addresses it through GRPO-style group normalization, in which β and log Z(x) cancel out exactly when the group mean is subtracted and the result is divided by the standard deviation. For each prompt x, a group of G responses {y1, . . . , yG} is sampled from πθ(·|x). The implicit reward is computed in Eq. [5.2.6.4.](#page-51-1)

<span id="page-51-1"></span>
$$
\hat{r}_{\theta}(x, y_i) = \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)}
$$
\n(5.2.6.4)

Both the explicit reward r(x, yi) and implicit reward rˆθ(x, yi) are normalized across the group using group mean and group standard deviation in Eq. [5.2.6.5.](#page-52-1) For the explicit <span id="page-52-4"></span>reward r(x, yi), the group mean and standard deviation are µ(x) and σ(x). For the implicit reward rˆθ(x, yi), the group mean and standard deviation are µˆ(x) and σˆ(x).

<span id="page-52-1"></span>
$$
r'(x, y_i) = \frac{r(x, y_i) - \mu(x)}{\sigma(x)}, \qquad \hat{r}'_{\theta}(x, y_i) = \frac{\hat{r}_{\theta}(x, y_i) - \hat{\mu}(x)}{\hat{\sigma}(x)}
$$
(5.2.6.5)

Following UNA's reward-alignment principle, the objective is JGIFT(θ) = −LGIFT(θ), where the loss minimizes the MSE between normalized implicit and explicit rewards in Eq. [5.2.6.6.](#page-52-2)

<span id="page-52-2"></span>
$$
J_{\text{GIFT}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta}(\cdot | x)} \left[ -(r'(x, y) - \hat{r}'_{\theta}(x, y))^2 \right]
$$
(5.2.6.6)

In practice, both the response-level implicit reward <sup>r</sup>ˆθ(x, yi) = <sup>P</sup>|yi<sup>|</sup> <sup>t</sup>=1 log <sup>π</sup>θ(<sup>y</sup> t i |x,y<t <sup>i</sup> ) πref(y t i |x,y<t <sup>i</sup> ) and the token-level implicit reward rˆθ(x, yi) = <sup>1</sup> |yi| P|yi<sup>|</sup> <sup>t</sup>=1 log <sup>π</sup>θ(<sup>y</sup> t i |x,y<t <sup>i</sup> ) πref(y t i |x,y<t <sup>i</sup> ) have been empirically evaluated. The response-level formulation (without <sup>1</sup> |yi| length normalization) is adopted as it consistently outperforms the token-level variant. The gradient coefficient is GCGIFT(x, y<sup>i</sup> , t) = 2(r ′ (x,yi)−rˆ ′ θ (x,yi)) σˆ(x) , which drives the policy to match normalized implicit rewards to normalized explicit rewards.

# <span id="page-52-0"></span>5.2.7 Advantage Stability

When group rewards are homogeneous, the group-relative advantage collapses toward zero and stalls gradient updates. AAPO [\(Xiong et al., 2025a\)](#page-109-2) directly addresses this through an advantage momentum term.

Advantage-Augmented Policy Optimization (AAPO) AAPO [\(Xiong et al., 2025a\)](#page-109-2) addresses the vanishing gradient problem that arises when all group responses receive similar rewards, causing the group-relative advantage to collapse toward zero and stalling training. The key innovation is an advantage momentum term, i.e., the clipped reward gap between the current policy's response and a response from the frozen reference model πref, which prevents vanishing gradients when the group-relative advantage approaches zero. The augmented advantage is given in Eq. [5.2.7.1](#page-52-3)

<span id="page-52-3"></span>
$$
A_{i,t} = \underbrace{\frac{r(x,y_i) - \mu(x)}{\sigma(x)}}_{A_{\text{GRPO}}(x,y_i)} + \text{clip}\left(\underbrace{r(x,y_i) - r(x,\tilde{y}_i)}_{\text{advantage momentum}}, \delta_L, \delta_H\right) \tag{5.2.7.1}
$$

where y˜<sup>i</sup> ∼ πref(·|x) is a reference-model response and [δL, δH] bound the momentum for stability. Because πref is frozen while π<sup>θ</sup> improves, the momentum term grows over training, ensuring a non-vanishing gradient signal even when the group-relative component vanishes. Like GPG, AAPO normalizes by the total token count <sup>P</sup> 1 G <sup>i</sup>=1|yi| across all responses (group length norm) rather than GRPO's per-response <sup>1</sup> |yi| . In addition, AAPO drops the importance ratio, clipping, and KL penalty, directly optimizing the cross-entropy loss weighted by the augmented advantage Ai,t. The gradient coefficient is GCAAPO(x, y<sup>i</sup> , t) = Ai,t.

# <span id="page-53-3"></span><span id="page-53-1"></span>5.2.8 Hybrid SFT with RL

SRFT [\(Fu et al., 2025\)](#page-99-2) unifies SFT and RL in a single-stage objective by augmenting on-policy rollout groups with human demonstrations and applying entropy-aware weighting to balance the two objectives without manual scheduling or a separate SFT cold-start phase. HPT [\(Lv et al., 2025\)](#page-103-1) in Section [2.6](#page-17-0) has also proposed to combine SFT with RL properly based on average reward obtained.

Supervised Reinforcement Fine-Tuning (SRFT) SRFT [\(Fu et al., 2025\)](#page-99-2) is motivated by the observation that SFT and RL exert complementary but asymmetric effects on policy distributions: SFT induces coarse-grained global shifts while RL performs fine-grained selective updates, and that sequential SFT → RL risks over-shifting the distribution before RL begins, prompting a single-stage unification with entropy-aware weighting. It augments the on-policy rollout group with demonstrations to form Gaug = Groll ∪ Gdemo, and computes the advantage via group normalization over Gaug: A<sup>i</sup> = r(x,yi)−µ(Gaug) σ(Gaug) , where µ(Gaug) and σ(Gaug) are the mean and standard deviation of outcome rewards r(x, yi) across all samples in Gaug. The demo RL component sets π<sup>β</sup> = 1 and omits clipping. The on-policy selfexploration uses binary reward r(x, y) ∈ {+1, −1} in a REINFORCE objective. The total objective JSRFT(θ) = −LSRFT(θ) is Eq. [5.2.8.1](#page-53-2)

<span id="page-53-2"></span>
$$
J_{\text{SRFT}}(\theta) = w_{\text{SFT}} \mathbb{E}_{(x,y)\sim\mathcal{D}_{\text{demo}}}\left[\frac{1}{|y|} \sum_{t=1}^{|y|} \log \pi_{\theta}(y^t | x, y^{\n(5.2.8.1)
$$

where ρk,t = πθ(y t k |x,y<t k ) πβ(y t k |x,y<t k ) = πθ(y t k |x, y<t k ) since π<sup>β</sup> = 1, sg(·) denotes stop-gradient, and the two entropy-aware weights have opposite dependencies: wSFT = 0.5 · sg(e −H(πθ) ) suppresses SFT when entropy is high, while wRL = 0.1 · sg(e +H(πθ) ) amplifies positive reinforcement at high entropy. Since the demo SFT and demo RL losses apply to the same samples, their gradient coefficients add. For demonstration samples (x, yk) ∼ Ddemo (with <sup>1</sup> |yk| normalization): GCdemo SRFT(x, yk, t) = wSFT + ρk,t Ak, where the first term comes from MLE and the second from the GRPO surrogate (similar to Eq. [2.5.1.2](#page-15-2) but without the clipping indicator and KL term). For on-policy rollout samples y ∼ πθ(·|x) (without <sup>1</sup> |y| normalization): GCself SRFT(x, y, t) = wRL · I[r(x, y)=+1] − I[r(x, y)=−1], a response-level coefficient derived via the REINFORCE score function.

### <span id="page-53-0"></span>5.3 Advantage Normalization

Normalizing the advantage before multiplying by the IS ratio controls the effective learning rate and gradient variance. This subsection surveys four strategies, also depicted in Figure [4.](#page-54-0) Group normalization subtracts the group mean and divides by the group standard deviation to standardize rewards within each prompt's rollouts, using an adaptive Beta-based scheme that tracks the evolving reward distribution [\(Xiao et al., 2025\)](#page-109-4). Beta Normalization is a special case of group normalization where the standard deviation is replaced by a Beta distribution. Multi-objective normalization standardizes each reward signal separately, sums

<span id="page-54-2"></span>![](./assets/01-rl-post-training-survey/_page_54_Figure_1.jpeg)

<span id="page-54-0"></span>Figure 4: Advantage Normalization: Group normalization, Two-step normalization, Multiobjective normalization and Normalization-free.

them, and re-standardizes the combined score to balance different objectives in decoupled per-reward settings [\(Xiao et al., 2025;](#page-109-4) [Liu et al., 2026a\)](#page-102-6). Two-step normalization first removes the group mean from the raw reward, then standardizes the result across the entire batch for cross-prompt stability [\(Hu et al., 2025a\)](#page-101-8). Normalization-free simply subtracts the group mean without any scaling, preserving the raw reward differences [\(Liu et al., 2025d\)](#page-103-3). Methods that additionally drop normalization as part of a broader regularization-free design are discussed with DAPO [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2](#page-58-0) and Lite PPO [\(Liu et al., 2026b\)](#page-103-5) in Section [5.4.2.](#page-58-1)

# <span id="page-54-1"></span>5.3.1 Beta Normalization

BNPO [\(Xiao et al., 2025\)](#page-109-4) replaces GRPO's [\(Shao et al., 2024\)](#page-107-2) static group standard deviation denominator with an adaptive Beta density whose parameters are re-estimated each batch via method of moments, yielding lower-variance gradients as the correctness distribution shifts during training.

Beta-Normalized Policy Optimization (BNPO) The GRPO's fixed group normalization strategy by the group standard deviation σ(x) under binary rewards r(x, y) ∈ {0, 1}, is equivalent to using Beta parameters (α, β) = 3 2 , 3 2 regardless of training stage. However, the distribution of the per-prompt µ(x) = <sup>1</sup> G P<sup>G</sup> <sup>i</sup>=1 r(x, yi) shifts as π<sup>θ</sup> improves, suggesting that the normalization itself should adapt. BNPO [\(Xiao et al., 2025\)](#page-109-4) addresses this by dynamically normalizing advantages using a Beta distribution whose parameters are re-estimated each batch via method of moments. BNPO replaces the fixed denominator with

<span id="page-55-5"></span>an adaptive Beta density f(µ(x); α, β) in Eq. [\(5.3.1.1\)](#page-55-0).

<span id="page-55-0"></span>
$$
A_{\alpha,\beta}(x,y) = \frac{r(x,y) - \mu(x)}{f_N(\mu(x); \alpha, \beta)}
$$
(5.3.1.1)

The parameters (a, b) of the underlying Beta distribution fD(µ(x); a, b) are estimated via method of moments over {µ(xi)} in the current batch, and the normalizing parameters (α, β) are set to the variance-minimizing values as shown in Eq. [\(5.3.1.2\)](#page-55-1).

<span id="page-55-1"></span>
$$
a = \left(\frac{\mathbb{E}_x[\mu(x)] (1 - \mathbb{E}_x[\mu(x)])}{\text{Var}_x[\mu(x)]} - 1\right) \mathbb{E}_x[\mu(x)], \qquad \alpha = 1 + \frac{a}{3}
$$
  
\n
$$
b = \left(\frac{\mathbb{E}_x[\mu(x)] (1 - \mathbb{E}_x[\mu(x)])}{\text{Var}_x[\mu(x)]} - 1\right) (1 - \mathbb{E}_x[\mu(x)]), \qquad \beta = 1 + \frac{b}{3}
$$
\n(5.3.1.2)

Setting (α, β) = (1, 1) recovers REINFORCE with baseline (<sup>f</sup> = 1); (α, β) = 3 2 , 3 2 recovers GRPO since f µ; 3 2 , 3 2 ∝ p µ(1−µ) = σ(x) for Bernoulli rewards. BNPO dynamically adjusts (α, β) instead, yielding lower-variance gradients throughout training. The gradient coefficient is GCBNPO(x, y<sup>i</sup> , t) = ci,t ρi,t Aα,β(x, yi), identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but without the KL regularization term. For N binary reward functions r1(x, y), . . . , rn(x, y) (e.g. accuracy and format rewards), BNPO normalizes each reward separately before averaging in Eq. [\(5.3.1.3\)](#page-55-2)

<span id="page-55-2"></span>
$$
A(x,y) = \frac{1}{N} \sum_{n=1}^{N} \frac{r_n(x,y) - \mu_n(x)}{f(\mu_n(x); \alpha_n, \beta_n)}
$$
(5.3.1.3)

where r<sup>n</sup> denotes the n-th reward function and µn(x) its per-prompt µ, avoiding reward collapse from summing rewards before normalization.

### <span id="page-55-4"></span>5.3.2 Multi-objective Normalization

GDPO [\(Liu et al., 2026a\)](#page-102-6) addresses training with multiple reward functions, where naively summing rewards prior to group normalization can lead to reward collapse, erasing signal differences between responses. BNPO, as discussed in Section [5.3.1,](#page-54-1) also addresses the integration of multiple reward signals.

Group reward-Decoupled Normalization Policy Optimization (GDPO) When extending GRPO to n different reward functions r1(x, y), . . . , rn(x, y), summing all rewards and applying group-relative normalization (Eq. [\(2.5.1.4\)](#page-16-1)) to the aggregate, distinct reward combinations collapse into identical advantage values (reward collapse). GDPO [\(Liu et al.,](#page-102-6) [2026a\)](#page-102-6) resolves this by performing decoupled group-wise normalization, i.e., normalizing each reward independently before aggregation. Each per-reward advantage is computed in Eq. [\(5.3.2.1\)](#page-55-3):

<span id="page-55-3"></span>
$$
A_n(x, y_i) = \frac{r_n(x, y_i) - \mu_n(x)}{\sigma_n(x)}
$$
(5.3.2.1)

<span id="page-56-5"></span>where µn(x) and σn(x) are the mean and standard deviation of {rn(x, yi)} G <sup>i</sup>=1 across the G responses for prompt x. The combined advantage sums the per-reward advantages in Eq. [\(5.3.2.2\)](#page-56-1).

<span id="page-56-1"></span>
$$
A_{\text{sum}}(x, y_i) = \sum_{n=1}^{N} A_n(x, y_i)
$$
 (5.3.2.2)

Lastly, a batch-level re-normalization ensures the magnitude does not scale with n in Eq. [\(5.3.2.3\)](#page-56-2) where µ<sup>B</sup> and σ<sup>B</sup> are the mean and standard deviation of {Asum(x, y)} across all responses in the batch B.

<span id="page-56-2"></span>
$$
\hat{A}_{\text{sum}}(x, y_i) = \frac{A_{\text{sum}}(x, y_i) - \mu \mathbf{B}}{\sigma \mathbf{B}}
$$
\n(5.3.2.3)

The gradient coefficient is GCGDPO(x, y<sup>i</sup> , t) = ci,t ρi,t Aˆ sum(x, yi), identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but with the two-step normalized advantage Aˆ sum and without KL divergence.

# <span id="page-56-0"></span>5.3.3 Two-step Normalization

In two-step normalization, the advantage is derived through two-step: either 1. group mean, group standard deviation, batch mean and batch standard deviation in Magistral [\(Mistral-AI](#page-104-2) [et al., 2025\)](#page-104-2) in Section [3.2.1,](#page-22-2) GDPO [\(Liu et al., 2026a\)](#page-102-6) in Section [5.3.2](#page-55-4) and REINFORCE++ [\(Hu et al., 2025a\)](#page-101-8) or 2. value function and batch mean and batch standard deviation in ORZ [\(Hu et al., 2025b\)](#page-101-6) in Section [5.2.5,](#page-48-0) SPO [\(Xu and Ding, 2026\)](#page-110-2) in Section [5.2.5](#page-49-0) and VinePPO [\(Kazemnejad et al., 2025\)](#page-101-5) in Section [4.1.6.](#page-31-0)

REINFORCE++ Unlike GRPO and RLOO, which use prompt-level (local) normalization, a theoretically biased estimator that causes training instability and overfitting when group sizes are small. REINFORCE++ [\(Hu et al., 2025a\)](#page-101-8) addresses these issues by combining local group normalization with global batch-level advantage normalization, retaining the PPO clipped surrogate (Eq. [\(2.4.2.3\)](#page-11-4)). REINFORCE++ proposes two variants: the base REINFORCE++ (G ≥ 1) follows PPO, and REINFORCE++w/Baseline (G > 1) is built on GRPO with G generations per prompt. In the base REINFORCE++ variant (G ≥ 1), the raw advantage folds a k1-style KL penalty into the outcome reward r(x, yi), and is then normalized across the entire batch as shown in Eq. [5.3.3.1](#page-56-3)

<span id="page-56-3"></span>
$$
A_{i,t} = r(x, y_i) - \beta \sum_{s=t}^{|y_i|} \log \frac{\pi_{\theta_{\text{old}}}(y_i^s \mid x, y_i^{
$$

where µbatch and σbatch are computed over all token-level advantages {A(x, y<sup>i</sup> , t)} in the batch. For the REINFORCE++w/Baseline variant (G > 1), the advantage is computed in two steps: first subtracting the group µgroup reward for reshaping, then normalizing by batch-level mean µbatch and standard deviation σbatch, as shown in Eq. [5.3.3.2.](#page-56-4)

<span id="page-56-4"></span>
$$
A'_{i} = r(x, y_{i}) - \mu_{\text{group}}, \quad \hat{A}_{i}^{\text{norm}} = \frac{A'_{i} - \mu_{\text{batch}}}{\sigma_{\text{batch}}} \tag{5.3.3.2}
$$

<span id="page-57-2"></span>Both variants follow the GRPO objective (Eq. [\(2.5.1.1\)](#page-15-1)) but replace GRPO's k<sup>3</sup> KL estimator with the k<sup>2</sup> estimator D (k2) KL (x, y<sup>i</sup> , t) = <sup>1</sup> 2 log <sup>π</sup>θ(<sup>y</sup> t i |x,y<t i ) πref (y t i |x,y<t i ) 2 as a separate loss term; the only difference is how Aˆnorm is computed (Eq. [\(5.3.3.1\)](#page-56-3) vs. Eq. [\(5.3.3.2\)](#page-56-4)). The gradient coefficient is GCRF++(x, y<sup>i</sup> , t) = ci,t ρi,t Anorm i,t <sup>+</sup> <sup>λ</sup> log <sup>π</sup>ref (<sup>y</sup> t i |x,y<t i ) πθ(y t i |x,y<t i ) , which replaces the GRPO gradient coefficient's k<sup>3</sup> KL term β πref πθ − 1 (Eq. [\(2.5.1.2\)](#page-15-2)) with the <sup>k</sup><sup>2</sup> KL term <sup>λ</sup> log <sup>π</sup>ref (<sup>y</sup> t i |x,y<t i ) πθ(y t i |x,y<t i ) .

# 5.3.4 Normalization-free

Some methods drop advantage normalization entirely. Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3) in Section [5.4.3](#page-59-0) removes both std-normalization and per-response length normalization, retaining only mean-centering to eliminate length-dependent and variance-induced biases. GPG [\(Chu](#page-98-4) [et al., 2026\)](#page-98-4) in Section [5.1.3](#page-40-2) and AAPO [\(Xiong et al., 2025a\)](#page-109-2) in Section [5.2.7](#page-52-0) similarly forgo std-normalization, relying on IS clipping, data filtering, or momentum terms for stability.

![](./assets/01-rl-post-training-survey/_page_57_Figure_4.jpeg)

### <span id="page-57-0"></span>5.4 Length Normalization

<span id="page-57-1"></span>Figure 5: Length Normalization: Response length normalization, group-length normalization and length normalization-free.

Length normalization determines how per-token gradient contributions are aggregated across responses of varying lengths. Figure [5](#page-57-1) illustrates three common strategies. Response length normalization divides by each response's own length <sup>1</sup> |yi| (e.g., 1/5, 1/7), treating every response equally but potentially biasing training toward shorter outputs [\(Shao et al.,](#page-107-2) [2024;](#page-107-2) [Schulman et al., 2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0). Group length normalization divides by the total length of all responses <sup>P</sup> 1 i |yi| (e.g., 1/17 for all tokens), giving longer responses

<span id="page-58-3"></span>proportionally more gradient weight [\(Yu et al., 2025;](#page-110-0) [Xiong et al., 2025b;](#page-109-1) [Liu et al., 2026b\)](#page-103-5). Length normalization-free methods apply no scaling (weight = 1 per token), (e.g., 1 for all tokens), letting every token contribute equally regardless of response length [\(Liu et al.,](#page-103-3) [2025d\)](#page-103-3). This choice also interacts with several methods discussed later, including VAPO [\(Yue](#page-111-4) [et al., 2025\)](#page-111-4) (Section [5.2.5\)](#page-48-1), MAGIC [\(He et al., 2025\)](#page-100-3) (Section [5.5.2\)](#page-61-0), and PURE [\(Cheng](#page-98-7) [et al., 2025a\)](#page-98-7) (Section [5.2.4\)](#page-46-3).

### 5.4.1 Response Length Normalization

The standard per-response normalization <sup>1</sup> |yi| , used in GRPO [\(Shao et al., 2024\)](#page-107-2) and PPO [\(Schulman et al., 2017b;](#page-107-1) [Ouyang et al., 2022\)](#page-105-0), ensures that each response contributes equally to the gradient regardless of token count. While this prevents long responses from dominating updates, it can inadvertently bias the model toward shorter responses when combined with per-group advantage normalization, motivating the group-level and normalization-free alternatives discussed in the subsections below.

# <span id="page-58-0"></span>5.4.2 Group Length Normalization

Group length normalization <sup>P</sup> 1 G <sup>i</sup>=1|yi| replaces per-response normalization, giving every token equal contribution and longer responses proportionally more gradient weight [\(Yu et al., 2025;](#page-110-0) [Xiong et al., 2025b;](#page-109-1) [Liu et al., 2026b\)](#page-103-5). In addition, GPG [\(Chu et al., 2026\)](#page-98-4) in Section [5.1.3](#page-40-2) and VAPO [\(Yue et al., 2025\)](#page-111-4) in Section [5.2.5](#page-48-1) also use group-total token normalization.

Dynamic sAmpling Policy Optimization (DAPO) Applying naive GRPO to largescale long-CoT RL yields only 30% on AIME 2024 (vs. DeepSeek-R1-Zero's 47%), with entropy collapse, reward noise, and training instability as the root causes. DAPO [\(Yu](#page-110-0) [et al., 2025\)](#page-110-0) diagnoses these four failure modes and open-sources a complete, reproducible fix. DAPO introduces four modifications to address entropy collapse, reward noise, and training instability in long-CoT RL. (1). Clip-Higher decouples the clipping bounds into εlow and εhigh (with εhigh > εlow), widening the upper bound to encourage exploration. (2). Dynamic Sampling filters out prompts where all G outputs receive identical rewards (i.e., requiring 0 < |{y<sup>i</sup> : r(x, yi) = 1}|< G). (3). Token-level loss replaces the per-response <sup>1</sup> |yi| normalization with <sup>P</sup> 1 G <sup>i</sup>=1|yi| over all tokens in the group. (4). Overlong Reward Shaping adds a soft length penalty rlength(x, y) (Eq. [5.4.2.1\)](#page-58-2) to the outcome reward r(x, y), where Lmax is the hard generation cap and Lcache is the width of a buffer zone before it. The DAPO objective is Eq. [5.4.2.2.](#page-58-1)

<span id="page-58-2"></span>
$$
r_{\rm length}(x,y) = \begin{cases} 0, & |y| \le L_{\rm max} - L_{\rm cache}, \\ \frac{(L_{\rm max} - L_{\rm cache}) - |y|}{L_{\rm cache}}, & L_{\rm max} - L_{\rm cache} < |y| \le L_{\rm max}, \\ -1, & |y| > L_{\rm max}. \end{cases}
$$
(5.4.2.1)

<span id="page-58-1"></span>
$$
J_{\text{DAPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)}
$$

$$
\left[ \frac{1}{\sum_{i=1}^G |y_i|} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \min(\rho_{i,t} A_{i,t}, \text{clip}(\rho_{i,t}, 1 - \varepsilon_{\text{low}}, 1 + \varepsilon_{\text{high}}) A_{i,t}) \right] \qquad (5.4.2.2)
$$
  
s.t.  $0 < |\{y_i : r(x, y_i) = 1\}| < G$ 

<span id="page-59-1"></span>where Ai,t = AGRPO(x,yi) = r(x,yi)−µ(x) σ(x) (Eq. [2.5.1.4\)](#page-16-1) and ρi,t = πθ(y t i |x,y<t i ) πθold(y t i |x,y<t i ) . The gradient coefficient is GCDAPO(x, y<sup>i</sup> , t) = ci,t ρi,t Ai,t, identical to the GRPO gradient coefficient (Eq. [2.5.1.2\)](#page-15-2) but without the KL regularization term.

Reinforce with Rejection (Reinforce-Rej) The authors argue that GRPO's performance advantage over vanilla REINFORCE stems not from reward normalization but from implicitly discarding prompts where all sampled responses are incorrect. Motivated by this, Reinforce-Rej [\(Xiong et al., 2025b\)](#page-109-1) makes this filtering explicit. Reinforce-Rej shares several design choices with DAPO [\(Yu et al., 2025\)](#page-110-0): the prompt-level mixed-correctness filter (restricting training to prompts where −1 < µ(x) = <sup>1</sup> n P<sup>n</sup> <sup>i</sup>=1 r(x, yi) < 1, asymmetric clipping, and the removal of KL divergence or entropy regularization.

The key distinction from DAPO lies in the advantage formulation: Reinforce-Rej applies the binary reward r(x, yi) ∈ {−1, +1} directly as the advantage, entirely foregoing the group mean and standard deviation normalization used in DAPO (and GRPO). This is motivated by the finding that reward normalization contributes minimally to performance, while prompt-level filtering is the dominant factor. The gradient coefficient is GCReinforce-Rej(x, y<sup>i</sup> , t) = I(−1 < µ(x) < 1)ci,t ρi,t r(x, yi).

Lite PPO Motivated by growing confusion over conflicting RL technique recommendations, Lite PPO [\(Liu et al., 2026b\)](#page-103-5) identifies a minimal two-technique recipe that unlocks learning capacity in critic-free policies using a vanilla PPO loss, outperforming technique-heavy methods such as DAPO while adding only two targeted changes to the GRPO baseline. First, it uses mixed advantage normalization: the µgroup is computed at the group level (per prompt) while the standard deviation (σbatch) is computed at the batch level (across all N × G responses), preventing the small-denominator instability that arises when group rewards are highly concentrated as shown in Eq. [\(2.5.1.4\)](#page-16-1).

$$
A_{\text{Like}}(x, y_i) = \frac{r(x, y_i) - \mu_{\text{group}}(x)}{\sigma_{\text{batch}}}
$$
\n(5.4.2.3)

Second, it adopts token-level loss aggregation: the per-response <sup>1</sup> |yi| normalization in GRPO is replaced by <sup>P</sup> 1 G <sup>i</sup>=1|yi| over all tokens, so every token contributes equally regardless of sequence length. The gradient coefficient is GCLitePPO(x, y<sup>i</sup> , t) = ci,t ρi,t ALite(x, yi), identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but without the KL regularization term.

# <span id="page-59-0"></span>5.4.3 Length Normalization-free

Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3) removes length normalization entirely, arguing that <sup>1</sup> |yi| introduces a length-dependent bias that systematically underweights tokens in longer responses. Besides that, length normalization-free can be also found in Prefix-RFT in Section [4.1.5,](#page-29-0) PKPO [\(Walder and Karkhanis, 2025\)](#page-108-2) in Section [4.2.4,](#page-34-2) OREAL [\(Lyu et al., 2025\)](#page-103-4) in Section [5.1.1,](#page-37-0) Entropy Min [\(Agarwal et al., 2025\)](#page-97-4) in Section [5.2.3,](#page-43-3) Seed-GRPO [\(Chen et al., 2025\)](#page-98-3) in Section [5.2.3,](#page-44-0) EMPO [\(Zhang et al., 2025d\)](#page-112-6) in Section [5.2.3,](#page-45-1) and MDPO [\(Kimi Team, 2025\)](#page-101-7) in Section [5.2.6.](#page-50-4)

GRPO Done Right (Dr.GRPO) Standard GRPO introduces optimization biases via per-response length normalization <sup>1</sup> |yi| and advantage standard normalization that artificially

<span id="page-60-3"></span>inflate response lengths and miscalibrate gradient magnitudes across question difficulties. Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3) removes three sources of bias from standard GRPO: (i) the per-response length normalization <sup>1</sup> |yi| , (ii) the standard normalization σ(x) in the advantage, and (iii) the KL divergence. The unbiased advantage retains only mean-centering as defined in Eq. [\(5.4.3.1\)](#page-60-1), where µ(x) is the group reward mean and r(x, yi) is the outcome reward.

<span id="page-60-1"></span>
$$
A_i = r(x, y_i) - \mu(x) \tag{5.4.3.1}
$$

The resulting objective is given in Eq. [\(5.4.3.2\)](#page-60-2).

<span id="page-60-2"></span>
$$
J_{\text{Dr.GRPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{G} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \min(\rho_{i,t} A_i, \text{clip}(\rho_{i,t}, 1-\varepsilon, 1+\varepsilon) A_i) \right]
$$
(5.4.3.2)

The gradient coefficient is GCDr.GRPO(x, y<sup>i</sup> , t) = ci,t ρi,t A<sup>i</sup> .

### <span id="page-60-0"></span>5.5 Regularization

Explicit regularization prevents policy collapse or divergence from reference behaviors. KL regularization anchors the policy to a reference model and entropy regularization maintains output diversity. Methods that drop all regularization rely on IS clipping, dynamic sampling, and mixed normalization for stability are discussed in Regularization-free.

# 5.5.1 KL Regularization

KL divergence from a reference policy provides a soft anchor preventing excessive policy drift per update. Most papers include KL divergence to constrain the difference from the reference model.

Prolonged Reinforcement Learning (ProRL) Standard RLVR training stalls after a few hundred steps because the cumulative KL from a fixed reference policy eventually dominates the objective and suppresses useful gradient signal. To solve this problem, ProRL [\(Liu et al.,](#page-102-7) [2025a\)](#page-102-7) introduces reference policy resets, which periodically hard-resetting πref to a recent snapshot of π<sup>θ</sup> along with the optimizer state to prevent the cumulative KL from dominating and stalling policy updates. In addition, it adopts DAPO's decoupled clipping (εhigh > εlow), where the larger upper bound allows greater probability increases for unlikely tokens (cliphigher ), combined with dynamic sampling that filters prompts where all G group responses are uniformly correct or incorrect (zero advantage). Lately, it retains the KL penalty β D(i,t) KL in Eq. [\(2.5.1.1\)](#page-15-1). The gradient coefficient is GCProRL(x, y<sup>i</sup> , t) = ci,t ρi,t A<sup>i</sup> + β πref (y t i |x,y<t i ) πθ(y t i |x,y<t i ) − 1 , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) with asymmetric clipping bounds.

### 5.5.2 Entropy Regularization

Entropy regularization adds a bonus rewarding diverse token distributions to prevent premature entropy collapse. The following two papers differ in how the bonus adapts: entropy shaping [\(Cheng et al., 2025a\)](#page-98-7) uses a detached advantage-scaling term with a self-regulating negative feedback loop, while MAGIC (Skywork-OR1) [\(He et al., 2025\)](#page-100-3) activates the bonus only when entropy drops below a target threshold via a fixed step-size rule.

<span id="page-61-2"></span>Reasoning with Exploration: An Entropy Perspective The authors observe that the policy's token-level entropy is consistently higher at positions that matter most for reasoning: pivotal tokens that serve as logical connectors (e.g. because, therefore), reflective actions where the model self-verifies or self-corrects, and rare behaviors that go beyond the base model's typical strategies [\(Cheng et al., 2025a\)](#page-98-7). Since entropy naturally signals these exploratory reasoning moments, they propose shaping the advantage with an entropy-based term. Let H<sup>t</sup> = − P <sup>v</sup>∈V πθ(v | x, y<t)log πθ(v | x, y<t) be the per-token policy entropy. The shaped advantage that replaces Ai,t in the GRPO gradient (Eq. [\(2.5.1.2\)](#page-15-2)) is defined in Eq. [\(5.5.2.1\)](#page-61-0), where α > 0 scales the entropy contribution and the min clips it so that ϕ(Ht) ≤ |At| 2 , preventing the term from dominating or reversing the sign of A<sup>t</sup> .

<span id="page-61-0"></span>
$$
A_t^{\text{shaped}} = A_t + \phi(H_t), \quad \phi(H_t) = \min\left(\alpha \cdot H_t^{\text{detach}}, \frac{|A_t|}{2}\right) \tag{5.5.2.1}
$$

Because Hdetach t is detached from the computational graph (∇θHdetach <sup>t</sup> = 0), the shaped advantage adjusts update magnitudes without altering gradient flow. In addition, it adopts asymmetric clipping (εlow = 0.2, εhigh = 0.28) and token-level loss averaging across the batch, i.e., <sup>P</sup> 1 G <sup>i</sup>=1|yi| rather than per-response <sup>1</sup> |yi| normalization from DAPO.

The gradient coefficient is GC(x, y<sup>i</sup> , t) = ci,t ·ρi,t ·A shaped t , identical to the GRPO gradient coefficient (Eq. [\(2.5.1.2\)](#page-15-2)) but with A shaped t replacing Ai,t and without the KL regularization term. The method is also self-regulating via a negative feedback loop: high H<sup>t</sup> increases ϕ(Ht), producing a stronger update that sharpens the distribution at that position, which lowers H<sup>t</sup> and automatically shrinks the entropy bonus in subsequent iterations to avoid over-encouragement without manual scheduling.

Multi-stage Adaptive entropy scheduling for GRPO In Convergence (MAGIC) While prior RLVR methods apply RL to base models with fixed entropy regularization, MAGIC [\(He et al., 2025\)](#page-100-3) targets long CoT SFT models with adaptive threshold-based entropy control. In addition, MAGIC modifies the GRPO objective (Eq. [\(2.5.1.1\)](#page-15-1)) by replacing per-response length normalization <sup>1</sup> <sup>|</sup>yi<sup>|</sup> with batch-level token averaging <sup>1</sup> N<sup>k</sup> where N<sup>k</sup> = P i∈T<sup>k</sup> P<sup>G</sup> <sup>j</sup>=1|yi,j | is the total token count, removing KL divergence, filtering out zeroadvantage prompt groups (T<sup>k</sup> := {i ∈ [N] : ∃ j ∈ [G], Ai,j ̸= 0}). The objective is given in Eq. [\(5.5.2.2\)](#page-61-1)

<span id="page-61-1"></span>
$$
J_{\text{MAGIC}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_j\}_{j=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot | x)} \left[ \frac{1}{\mathcal{N}_k} \sum_{i \in \mathcal{T}_k} \sum_{j=1}^G \sum_{t=1}^{|y_{i,j}|} \sum_{t=1}^{|y_{i,j}|} \left( \min \left( \rho_{i,j}^t A_{i,j}, \text{clip}(\rho_{i,j}^t, 1-\varepsilon, 1+\varepsilon) A_{i,j} \right) + \alpha_k H \left( \pi_\theta(\cdot | x_i, y_{i,j}^{(5.5.2.2)
$$

where ρ t i,j = πθ(y t i,j <sup>|</sup> <sup>x</sup>i, y<t i,j ) πθold(y t i,j <sup>|</sup> <sup>x</sup>i, y<t i,j ) , Ai,j = r(xi,yi,j )−µ(xi) σ(xi) is the group-normalized advantage (Eq. [\(2.5.1.4\)](#page-16-1)), and H(·) is the next-token entropy. The entropy coefficient α<sup>k</sup> adapts

<span id="page-62-1"></span>at each step k via Eq. [\(5.5.2.3\)](#page-62-0):

<span id="page-62-0"></span>
$$
\alpha_k = c_k \cdot \mathbb{I}\{e_k \le e_{\text{tgt}}\}, \quad c_{k+1} = \begin{cases} c_k + \Delta & \text{if } e_k < e_{\text{tgt}} \\ c_k - \Delta & \text{if } e_k > e_{\text{tgt}} \end{cases} \quad c_0 = 0 \tag{5.5.2.3}
$$

where e<sup>k</sup> is the current entropy, etgt the target lower bound, ∆ a fixed step-size hyperparameter, and the bonus activates only when e<sup>k</sup> drops below etgt. The gradient coefficient is GCMAGIC(x, yi,j , t) = c t i,j ρ t i,j Ai,j − α<sup>k</sup> log π<sup>θ</sup> y t i,j | x<sup>i</sup> , y<t i,j where c t i,j ∈ {0, 1} is the PPO clipping indicator that zeros out any token whose importance ratio ρ t i,j falls outside [1−ε, 1+ε] which is distinct from the adaptive entropy schedule scalar c<sup>k</sup> in Eq. [\(5.5.2.3\)](#page-62-0).

### 5.5.3 Regularization-free

Methods including DAPO [\(Yu et al., 2025\)](#page-110-0) in Section [5.4.2,](#page-58-0) Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3) in Section [5.4.3,](#page-59-0) and Lite PPO [\(Liu et al., 2026b\)](#page-103-5) in Section [5.4.2](#page-58-1) remove both KL divergence and entropy regularization, relying on IS ratio clipping, dynamic prompt filtering, and mixed normalization for stability.

![](./assets/01-rl-post-training-survey/_page_63_Figure_1.jpeg)

Figure 6: Comprehensive RLHF and DPO taxonomy.

# <span id="page-63-1"></span><span id="page-63-0"></span>6 RLHF and Iterative DPO: On-Policy Methods

RLHF and RLVR differ primarily in how their reward signals are constructed. In RLHF, a reward model is trained to capture human preferences via the Bradley-Terry model: given a set of prompts, the framework iteratively generates responses, scores them with the learned reward model, and updates the LLM policy via reinforcement learning. Because the training distribution is continuously refreshed through this generation loop, RLHF is inherently on-policy. RLAIF follows the same on-policy paradigm but replaces the learned BT reward model with an LLM-as-a-judge, sidestepping the need for explicit human annotation.

DPO, by contrast, is an offline method: it optimizes the policy directly on a fixed, pre-collected preference dataset, bypassing the need for an explicit reward model or online

<span id="page-64-3"></span>generation. Iterative DPO extends this by closing the loop: at each iteration, the current policy generates multiple responses, a preference signal is used to identify desired and undesired outputs from among them, and the model is fine-tuned on the resulting pairs. This makes iterative DPO an on-policy approach that progressively refines the training distribution. Nash learning-based methods take a fundamentally different stance by replacing the pointwise reward model with a preference model grounded in game theory. A comprehensive summary of the RLHF and DPO algorithms, including offline DPO, is provided in Algorithm [2,](#page-64-2) and a detailed taxonomy of these methods is illustrated in Figure [6.](#page-63-1)

<span id="page-64-2"></span>

| Algorithm 2<br>RLHF and DPO: Key Design Choices                                 |  |  |  |
|---------------------------------------------------------------------------------|--|--|--|
| Unified Policy Gradient: same form as Algorithm 1                               |  |  |  |
| 1: Initialise: πθ, πref, πold<br>←πθ (on-policy)   fixed dataset Doff (offline) |  |  |  |
| 2: for iter = 1, 2, , N do                                                      |  |  |  |
| 3:<br>Prompt Sampling: sample x ∼ D                                             |  |  |  |
| 4:<br>Response Generation                                                       |  |  |  |
| 6 On-policy: generate y ∼ πθ(·   x) from current policy                         |  |  |  |
| 7 Offline: responses from fixed Doff , not generated on-policy                  |  |  |  |
| 7.1 Response type:<br>pairwise   single   listwise                              |  |  |  |
| 5:<br>Reward                                                                    |  |  |  |
| 6 On-policy:<br>RLHF   RLAIF   Iterative DPO   Nash Learning                    |  |  |  |
| 7.2 Offline:<br>pairwise   token-level   pointwise   listwise   negative        |  |  |  |
| 6:<br>for t = 1, ,  y  do                                                       |  |  |  |
| 7:<br>Gradient Coefficient                                                      |  |  |  |
| 7.3 Regularisation:<br>entropy   divergence   ref model   length penalty        |  |  |  |
| t<br>  x, y <t)<br>8:<br/>Accumulate: g += GC(x, y, t) · ∇θ log πθ(y</t)<br>    |  |  |  |
| 9:<br>θ ← θ + η g;<br>πold ←πθ (on-policy only);                                |  |  |  |
| 7.4 Merge SFT (offline): merge SFT data   merge SFT model   none                |  |  |  |
| 10: return πθ                                                                   |  |  |  |
|                                                                                 |  |  |  |

### <span id="page-64-0"></span>6.1 RLHF

In RLHF, for each prompt, one response is generated by LLM. Then, a BT reward model is trained based on pairwise preference datasets. Then, the prompt and response will be sent to BT reward model for reward. The reward will then be utilized to optimize LLM through PPO. More details on RLHF can be found in Section [2.4.3.](#page-12-4)

### <span id="page-64-1"></span>6.2 RLAIF

In RLAIF, the trained BT reward model is replaced with LLM-as-a-Judge. For each prompt and response, they are combined through a system prompt and sent to LLM for evaluation.

RLAIF-Anthropic Constitutional AI [\(Bai et al., 2022b\)](#page-97-5) was developed to address two problems with an earlier training method pursued by Anthropic [\(Bai et al., 2022a\)](#page-97-0): the high cost of hiring people to label harmful content, and the tendency of the resulting models to simply refuse sensitive questions instead of responding in a helpful, nuanced way. Unlike RLHF-Anthropic, which requires human crowd-worker annotations for both helpfulness and harmlessness labels, replace all harmlessness feedback with model-generated signals guided by a written "constitution" of ∼16 natural-language harmlessness principles. Like RLHF-Anthropic, the RLAIF stage retains the same PPO-based RL pipeline and continues to use human feedback for helpfulness. The training proceeds in two stages.

<span id="page-65-0"></span>In the Supervised Learning (SL) stage, a helpful RLHF model generates initial responses to red-team prompts. Each response is then iteratively critiqued and revised guided by a constitutional principle randomly sampled from the constitution; optional CoT prompting [\(Wei et al., 2023\)](#page-108-1) improves critique quality. The revised responses, together with human helpfulness samples, are used for SFT to produce the SL-CAI model. The authors found that increasing the number of revisions progressively improved harmlessness scores while slightly reducing helpfulness, and that the critique-revision approach outperformed direct revision alone.

In the RLAIF stage, harmlessness preference labels are generated by an independent feedback model. Given a response pair generated by SL-CAI and a principle drawn uniformly from the constitutional set, the model is queried via a multiple-choice prompt to identify the less harmful response. The normalized log-probabilities over the answer choices are then used as soft preference targets for training. A preference model (PM) is then trained on a mixture of these AI harmlessness labels and human helpfulness labels, and PPO fine-tunes the SL-CAI policy against this PM. The resulting RL-CAI models are "harmless but non-evasive", i.e., engaging with sensitive queries and explaining their objections rather than refusing outright.

This study demonstrated the feasibility of self-supervised AI alignment by utilizing AI to collect preference data for harmlessness, replacing costly human annotation for that dimension while maintaining helpfulness via human feedback.

RLAIF-Google Unlike RLAIF by Anthropic [\(Bai et al., 2022b\)](#page-97-5), who applied AI feedback only to harmlessness, the authors [\(Lee et al., 2024\)](#page-101-9) extended RLAIF to summarization and helpfulness as well. The paper proposes two RLAIF strategies that differ in how the AI signal is used to train the policy. Distilled RLAIF follows the canonical RLHF pipeline: AI-generated pairwise preferences train a RM, which then guides policy optimization via REINFORCE. The process is structurally identical to human-feedback RLHF, with AI labels substituting for human labels. Direct RLAIF (d-RLAIF), the key novel contribution, bypasses RM training entirely: the LLM is prompted to score each response on a scale of 1–10, and this pointwise score is used directly as the RL reward signal. d-RLAIF addresses the "staleness" issue of Distilled RLAIF, where the RM trained on generations from the initial policy becomes increasingly out-of-distribution as the policy improves during training.

Both strategies share the same AI feedback collection framework. A structured prompt is constructed from four components: 1. Preamble, 2. Few-shot exemplars (optional), 3. Sample to annotate, and 4. Ending. A two-step CoT procedure generates the AI preference. Firstly, the full prompt elicits a rationale from the LLM, and then the LLM's response is appended with a completion cue (e.g., "Preferred Summary=") and re-submitted to the LLM, which generates a preference token ("1" or "2"). The log-probabilities of these two tokens are extracted and converted via softmax to a soft preference distribution (e.g., 0.6 vs. 0.4). To mitigate positional bias, each pair is evaluated in both candidate orderings and the scores are averaged.

During the evaluation process, three key metrics were employed: 1. AI-labeler alignment: the degree of agreement between AI and human labelers, 2. win rate: the likelihood of a response being selected by human labelers when compared between two candidates, and 3. harmless rate: the percentage of responses deemed harmless by human evaluators. They observed that the RLHF policy sometimes hallucinated when the RLAIF policy did not, <span id="page-66-2"></span>and RLAIF sometimes produced less coherent summaries as compared to RLHF. Three main conclusions were drawn. Firstly, RLAIF achieved comparable performance to RLHF in summarization and helpful dialogue generation tasks, but outperformed RLHF in the harmless task. Secondly, RLAIF demonstrated the ability to enhance a SFT policy even when the LLM labeler was of the same size as the policy. Lastly, Direct RLAIF surpassed Distilled RLAIF in terms of alignment.

RLAIF-OpenAI While Anthropic and Google distill AI preferences into reward models, OpenAI's RLAIF [\(Mu et al., 2024\)](#page-104-3) aligns safety by decomposing policies into fine-grained, LLM-graded propositions. This creates a Rule-Based Reward (RBR) integrated directly into PPO training, requiring minimal human calibration. To solve this problem, the authors divided the task of rating responses by LLM into specific rules that explicitly describe the desired and undesired behaviors and used the behaviors on individual tasks to cover complex evaluation behaviors. This could simplify the task of AI evaluation and allow fine grained control of model responses. Based on the prompt, the authors proposed a content policy and a behavior policy. The content policy defined precisely what content in a prompt is considered an unsafe request, and the behavior policy referred to how LLM should handle various kinds of unsafe requests defined in the content policy. In the case of applying LLM as a chat model, the content policy included erotic content, hate speech, criminal advice and self-harm, while the behavior policy contained Hard Refusal, Soft Refusal and Comply as the three response types.

Based on the content and behavior policies, an auxiliary safety rule-based reward function (RBR) was built for RL training. To begin with, the authors discovered that AI was better at classifying individual tasks rather than multilayered tasks like holistic rating. Thus, they proposed propositions, which are binary statements about responses given a prompt, and rules, which determine the ranking of responses for a given response type. Based on each individual proposition, a feature like ϕi(x, y) for the i-th feature could be obtained using classification-prompts for each proposition and a grader LLM. Eventually, the total reward as a weighted linear combination of all features was shown in Eq. [6.2.1](#page-66-0) where N features were considered in total.

<span id="page-66-0"></span>
$$
r_{\rm{rbr}}(x, y, w) = \sum_{i=1}^{N} w_i \phi_i(x, y)
$$
\n(6.2.1)

In the paper, the authors utilized 20 features for Hard-Refusal, 23 features for Soft-Refusal, and 18 features for Comply. Synthetic data DRBR = {(x, y1, y2, . . . , yG)} where the ranked G responses y<sup>1</sup> > y<sup>2</sup> > . . . > y<sup>G</sup> were utilized for fitting the weights in Eq. [6.2.1.](#page-66-0) The obtained reward from RBR was combined with the original reward model, i.e. rRM to play the role of total reward, i.e., rtot through rtot = rRM + rrbr. Lastly, the weights were fitted by minimizing the hinge loss in Eq. [6.2.2](#page-66-1) over all pairwise comparisons extracted from the ranked completions in DRBR, where |DRBR| refers to the total number of prompts in the dataset.

<span id="page-66-1"></span>
$$
L(w) = \frac{1}{|D_{\text{RBR}}|} \sum_{(x, y_w, y_l) \in D_{\text{RBR}}} (\max(0, 1 + r_{\text{tot}}(x, y_l, w) - r_{\text{tot}}(x, y_w, w)))
$$
(6.2.2)

<span id="page-67-2"></span>A comparison between the original help-only reward model, i.e., rRM and the final total reward, i.e., rtot was conducted. Results showed that rRM was tough to separate disallowed, perfect refusal and bad refusal. However, for rtot, the rewards of different categories of prompts could be separated. Similar patterns were observed for error rate when comparing rRM with rtot.

### <span id="page-67-0"></span>6.3 Iterative DPO

While DPO is traditionally used as an offline optimization technique, iterative DPO adapts it into an on-policy framework by generating candidate responses from the current policy for a given set of prompts and then labeling them as preferred or dispreferred. The model is subsequently updated using these pairwise preference signals. Consequently, iterative DPO is best understood as an on-policy method.

Rejection Sampling Optimization (RSO) DPO optimizes a language model on offline preference pairs, but they are limited to human-collected data from unknown mixed policies, and it introduces a distribution mismatch that degrades alignment quality. RSO [\(Liu](#page-102-8) [et al., 2024\)](#page-102-8) mitigates the policy–data distribution mismatch inherent in offline preference optimization methods by using rejection sampling to approximate samples from the estimated optimal policy.

The procedure operates as follows: (1) sample y ∼ πsft(y|x) and u ∼ U[0, 1]; (2) compute M = min{m | mπsft(y|x) ≥ π ⋆ (y|x)}; (3) accept y if u < <sup>π</sup> <sup>⋆</sup>(y|x) Mπsft(y|x) ; otherwise reject; and (4) repeat until sufficient accepted samples are collected, ensuring proximity to the target policy. Since M is intractable, RSO approximates the density ratio using a reward model, yielding the acceptance probability in Eq. [6.3.1](#page-67-1)

<span id="page-67-1"></span>
$$
P_{\text{accept}}(x, y) = \frac{\pi^{\star}(y|x)}{M\pi_{\text{sft}}(y|x)} = \exp\left(\frac{r_{\phi}(x, y) - r_{\text{max}}}{\beta}\right)
$$
(6.3.1)

where rmax denotes the maximum reward among current candidates and β controls selectiveness. As β → ∞, all samples are accepted, while β → 0 retains only the highest-reward response.

Self-Rewarding Language Models A key limitation of DPO is the high cost of collecting new human preference data. Iterative (online) DPO addresses this by using a single LLM to jointly perform instruction following and self-instruction creation, rather than separating these capabilities into distinct models [\(Yuan et al., 2024\)](#page-110-6). In the Self-Instruction Creation phase, G candidate responses are generated for a given prompt, and the same LLM acts as its own reward model via LLM-as-a-Judge prompting to evaluate each response. Rather than scoring five separate dimensions, the judge assigns a single additive score from 0 to 5, awarding one point for each of five quality criteria met: relevance, coverage, usefulness, clarity, and expertise, preceded by a brief chain-of-thought justification. The highest- and lowest-scoring responses form a preference pair where pairs with equal scores are discarded. During Instruction Following training, DPO is applied to these self-generated preference pairs, allowing the model to improve both its instruction-following and reward-modeling abilities simultaneously.

<span id="page-68-1"></span>ContRastive Iterative Negative GEneration (CRINGE) The CRINGE loss [\(Adolphs](#page-96-0) [et al., 2023\)](#page-96-0) handles positive and negative responses separately. Positive responses (x, yw) are processed like SFT, while negative responses (x, yl) contrast each negative token y t l against a positive token. Let sθ,t represent the model output score for token t. [Xu](#page-109-5) [et al.](#page-109-5) [\(2024b\)](#page-109-5) select top-k scores {sθ,t[1], ..., sθ,t[k]} excluding sθ,t[y t l ], then sample via s ∗ θ,t ∼ Softmax(sθ,t[1], . . . , sθ,t[k]). The binary CRINGE loss is Eq. [6.3.2](#page-67-1) and extending CRINGE to preference feedback [\(Xu et al., 2024c\)](#page-109-6) yields the pairwise loss in Eq. [6.3.3.](#page-67-1)

$$
J_{Bin}(\pi_{\theta}) = \log P_{\theta}([x, y_w]) + \alpha \left[ \sum_{t=1}^{T} \log \left( \frac{\exp(s_{\theta, t}^*)}{\exp(s_{\theta, t}^*) + \exp(s_{\theta, t}[y_t^t])} \right) \right]
$$
(6.3.2)

$$
J_{Pair}(\pi_{\theta}) = g_{\theta}(x, y_w, y_l) J_{Bin}(\pi_{\theta})
$$
\n(6.3.3)

The gate function gθ(x, yw, yl) = σ b−(log Pθ(yw|x)−log Pθ(y<sup>l</sup> |x)) τ controls the loss: approaching zero when y<sup>w</sup> is much better than y<sup>l</sup> , and one otherwise. Parameters b and τ control the margin and smoothness respectively.

Meta-Rewarding Language Models Self-Rewarding LMs improve the LLM policy through iterative DPO, but overlook the judge: a stagnant judge saturates feedback quality and causes reward hacking. To address this, the authors introduce Meta-Rewarding, a self-improvement framework that upgrades both the actor and the judge simultaneously through iterative DPO [\(Wu et al., 2025b\)](#page-109-7). The key insight is to introduce a third role: the meta-judge, which evaluates the quality of the judge's own evaluations, providing a feedback signal to improve judging ability. The process of assigning rewards to evaluations is termed "meta-rewarding." Length bias, a known failure mode in reward models where judges tend to favor verbose responses, is also explicitly mitigated. In this framework, the LLM simultaneously serves three roles: (1) actor (generating responses), (2) judge (evaluating responses), and (3) meta-judge (evaluating the quality of the judges). All three roles are performed by a single model, preserving the self-improving, human-supervision-free nature of the pipeline.

### <span id="page-68-0"></span>6.4 Nash Learning based Methods

Standard RLHF and DPO methods reduce preferences to a scalar reward via the Bradley-Terry model, which is brittle to non-transitive annotations and optimizes absolute scores rather than comparative win rates. Nash learning-based methods address this by framing alignment as a two-player zero-sum preference game where policies are directly compared via win probabilities rather than scalar rewards

Nash Learning from Human Feedback (NLHF) In RLHF, the BT model is used to learn a scalar reward function, which is then optimized via RL. A core limitation of this pipeline is that the objective effectively optimizes reward score rather than win probability against other policies. In addition, non-transitivity (e.g., y<sup>1</sup> > y2, y<sup>2</sup> > y3, but y<sup>1</sup> > y3) can be amplified by annotator disagreement, and inaccurate preference ordering can misguide the policy toward a narrow set of responses and reduce diversity [\(Bertrand et al., 2023\)](#page-98-8). Nash learning addresses these issues by defining the objective directly in preference space without a

<span id="page-69-4"></span>reward surrogate or reward model and by using the Nash equilibrium as the solution concept instead of reward maximization [\(Munos et al., 2024\)](#page-104-4). The preference probability between two policies πθ(y|x) and π ′ θ (y|x) is defined as Eq. [6.4.1](#page-69-0) where this preference model does not depend on θ.

<span id="page-69-0"></span>
$$
P_{\theta}(\pi_{\theta}(y|x) > \pi'_{\theta}(y|x)) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot|x), y' \sim \pi'_{\theta}(\cdot|x)} [P(y > y'|x)] \tag{6.4.1}
$$

This formulation directly compares policies, eliminating the need for the BT model. The optimal policy is obtained by the Nash equilibrium in Eq. [6.4.2.](#page-69-1)

<span id="page-69-1"></span>
$$
\pi_{\theta}^*(y|x) = \arg\max_{\pi_{\theta}} \min_{\pi_{\theta}'} P_{\theta}(\pi_{\theta}(y|x) > \pi_{\theta}'(y|x))
$$
\n(6.4.2)

For LLM alignment, a KL constraint to a reference model is introduced, yielding Eq. [6.4.3](#page-69-1) to ensure that the distance from the aligned model to the initial model remains limited.

$$
P_{\theta,\beta}(\pi_{\theta}(y|x) > \pi'_{\theta}(y|x)) = P_{\theta}(\pi_{\theta}(y|x) > \pi'_{\theta}(y|x)) - \beta D_{\mathrm{KL}}(\pi_{\theta}(\cdot|x)||\pi_{\mathrm{ref}}(\cdot|x)) \quad (6.4.3)
$$

$$
+ \beta D_{\mathrm{KL}}(\pi'_{\theta}(\cdot|x)||\pi_{\mathrm{ref}}(\cdot|x))
$$

Building on the refined preference model, the authors introduced the Nash-Mirror Descent (Nash-MD) algorithm. This algorithm uses a regularized policy (Eq. [6.4.4\)](#page-69-1) and a policy update step (Eq. [6.4.5\)](#page-69-2), where α<sup>t</sup> denotes the learning rate at step t. In Eq. [6.4.4,](#page-69-1) π t (y|x) is used rather than π t θ (y|x) because after the t-th optimization, the policy remains fixed and is no longer subject to further optimization.

$$
\pi_{\text{mix}}^t(y|x) = \frac{\pi^t(y|x)^{1-\alpha_t\beta}\pi_{\text{ref}}(y|x)^{\alpha_t\beta}}{\sum_{y'} \pi^t(y'|x)^{1-\alpha_t\beta}\pi_{\text{ref}}(y'|x)^{\alpha_t\beta}}
$$
(6.4.4)

<span id="page-69-2"></span>
$$
\pi_{\theta}^{t+1}(y|x) = \arg\max_{\pi_{\theta}} \left[ \alpha_t P_{\theta,\beta}(\pi_{\theta}(y|x) > \pi_{\text{mix}}^t(y|x)) - D_{\text{KL}}(\pi_{\theta}(\cdot|x)||\pi_{\text{mix}}^t(\cdot|x)) \right] \tag{6.4.5}
$$

The method is proven to converge by maintaining last-iterate policies.

Self-Play Preference Learning (SPPO) Nash-MD's Mirror Descent requires maintaining a geometric mixture policy π t mix through two-timescale updates (Eq. [6.4.4\)](#page-69-1), introducing significant implementation complexity for large LLMs. SPPO [\(Wu et al., 2025c\)](#page-109-8) reinterprets RLHF as a two-player zero-sum game with a single agent representing both players and a multiplicative-weights self-play rule where the policy competes directly against its own previous iterate. The agent samples multiple trajectories evaluated by humans or models, using win rate as reward. This avoids explicit scalar reward regression (e.g., Bradley–Terrystyle reward modeling) but still relies on a preference oracle (human judgements or a learned preference model, e.g., PairRM), and it naturally handles noisy and intransitive preferences. For LLMs, by leveraging the symmetry of the preference function [\(Freund and Schapire,](#page-99-6) [1999\)](#page-99-6), the iterative/online policy update is derived as Eq. [6.4.6](#page-69-3)

<span id="page-69-3"></span>
$$
\pi_{\theta}^{t+1}(y|x) = \frac{\pi^{t}(y|x)e^{\left(\frac{1}{\beta}P_{\theta}(y>\pi^{t}|x)\right)}}{Z_{\pi^{t}}(x)}
$$
(6.4.6)

70

<span id="page-70-3"></span>where Zπ<sup>t</sup> (x) = P y π t (y|x)e 1 β Pθ(y>π<sup>t</sup> |x) is the normalizing partition function and P(y > π|x) = E<sup>y</sup> ′∼π(·|x) [P(y > y′ |x)] is the expected probability that y is preferred over a random response y ′ drawn from policy π t . By reformulating Eq. [6.4.6,](#page-69-3) the authors derived log π t+1 θ (y|x) πt(y|x) = 1 β Pθ(y > π<sup>t</sup> |x) − log Zπ<sup>t</sup> (x). A MSE loss is then adopted as the practical objective to update the policy, as shown in Eq. [6.4.7.](#page-70-1)

<span id="page-70-1"></span>
$$
\pi_{\theta}^{t+1} = \arg\min_{\pi_{\theta}} \mathbb{E}_{x \sim X, y \sim \pi^t(y|x)} \left\{ \left[ \log \left( \frac{\pi_{\theta}(y|x)}{\pi^t(y|x)} \right) - \left( \frac{1}{\beta} P_{\theta}(y > \pi^t|x) - \log Z_{\pi^t}(x) \right) \right]^2 \right\}
$$
(6.4.7)

The estimations of Pθ(y > π<sup>t</sup> |x) and log Zπ<sup>t</sup> (x) are conducted through sampling and averaging. The authors opt to sample G responses y1, y2, . . . , y<sup>G</sup> ∼ π t for each prompt x, and represent the empirical distribution as πˆ t . Consequently, Pθ(y > πˆ t |x) = <sup>1</sup> G P<sup>G</sup> <sup>i</sup>=1 Pθ(y > y<sup>i</sup> |x) and Zπ<sup>ˆ</sup> <sup>t</sup> (x) = Ey∼πt(y|x) e 1 β Pθ(y>π<sup>t</sup> |x) .

Direct Nash Optimization (DNO) Previous Nash learning algorithms used purely on-policy methods requiring unstable two-timescale updates (e.g., π t mix(y|x) and π t+1 θ (y|x) in [\(Munos et al., 2024\)](#page-104-4)). DNO addressed this with batched on-policy learning and singletimescale updates, improving sampling efficiency [\(Rosset et al., 2024\)](#page-106-6). Rather than directly seeking a Nash equilibrium via π t θ (y|x) → π ⋆ θ (y|x), DNO views the update as regressing the policy-induced internal reward rθ,t(x, y) toward a preference-based reward rt(x, y) = Ey ′∼π<sup>t</sup> [P(y > y′ | x)] defined by pairwise preferences.

The scaled DNO algorithm proceeds as follows: (1) construct dataset D<sup>t</sup> = {(x, ygold)} where x ∼ D and ygold are teacher responses sampled as ygold ∼ πgold(y|x); (2) sample G outputs per prompt: {y t 1 , . . . , y<sup>t</sup> <sup>G</sup>} ∼ π t (y|x) which is the fixed policy of π t θ (y|x) after the training process; (3) rank responses {y t 1 , . . . , y<sup>t</sup> <sup>G</sup>, ygold}; (4) filter preference pairs and only pairs (y t w, y<sup>t</sup> l ) whose ranking gap exceeds a threshold are retained as Dt+1. Lastly, π θ <sup>t</sup>+1 is obtained via a single-timescale contrastive learning step (Eq. [6.4.8\)](#page-70-2), where π t serves simultaneously as the reference policy.

<span id="page-70-2"></span>
$$
\pi_{\theta}^{t+1} = \arg \max_{\pi_{\theta}} \mathbb{E}_{(x, y_w^t, y_l^t) \sim D_{t+1}} \log \left[ \sigma \left( \beta \log \left( \frac{\pi_{\theta}(y_w^t | x)}{\pi^t(y_w^t | x)} \right) - \beta \log \left( \frac{\pi_{\theta}(y_l^t | x)}{\pi^t(y_l^t | x)} \right) \right) \right]
$$
(6.4.8)

The developed algorithm closely resembles iterative/online DPO, leading the authors to assert that such an approach could approximate the Nash equilibrium for general preferences.

### <span id="page-70-0"></span>7 DPO: Offline Methods

This section surveys representative offline-based algorithms, with specific focus on DPO-based variants. We organize them along the structure of the training signal including response format (pairwise, pointwise, or listwise); the form of the reward signal (pairwise, token-level, pointwise, listwise, or negative); regularization strategy; and how SFT is integrated with preference learning.

### <span id="page-71-3"></span><span id="page-71-0"></span>7.1 Response Generation

A fundamental design axis in offline-based algorithm is how the response data are structured. Methods differ in whether they operate on pairwise comparisons between a preferred and a dispreferred response, single responses with binary or scalar feedback, or listwise rankings across multiple candidates.

### <span id="page-71-1"></span>7.1.1 Pairwise Responses

The dominant paradigm in offline preference optimization is the pairwise formulation, in which each training example consists of a prompt x, a preferred response yw, and a dispreferred response y<sup>l</sup> . This contrastive structure directly encodes relative human judgment and forms the foundation of DPO and its many variants. Pairwise data has become the standard not by accident: it is cognitively easier for annotators to rank two responses than to assign absolute scores, it yields richer and more reliable preference signal, and it arises naturally in practical settings such as A/B testing.

Sequence Likelihood Calibration with Human Feedback (SLiC-HF) PPO-based RLHF incurs high complexity and memory overhead through its online rollout loop, simultaneous multi-model requirements (policy, value, reward, and SFT), and costly fresh data collection for each new model. SLiC-HF [\(Zhao et al., 2023\)](#page-112-8) addresses these bottlenecks by replacing the online RL loop with a simple offline calibration objective that directly reuses off-policy human preference data collected for reward models. It uses a max-margin ranking objective plus a sft-anchoring regularizer in Eq. [7.1.1.1](#page-71-1) to simplify the PPO-based RLHF pipeline, and its objective gradient is shown in Eq. [7.1.1.2.](#page-71-2)

$$
J_{\text{SLiC-HF}}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[-\max(0,\delta_m - \log \pi_{\theta}(y_w|x) + \log \pi_{\theta}(y_l|x)) + \lambda_{\text{sft}} \log \pi_{\theta}(y_{\text{sft}}|x)\right]
$$
\n(7.1.1.1)

<span id="page-71-2"></span>
$$
\nabla_{\theta} J_{\text{SLiC-HF}}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}[\mathbb{I}(m>0) \left(\nabla_{\theta} \log \pi_{\theta}(y_w|x) - \nabla_{\theta} \log \pi_{\theta}(y_l|x)\right) + \lambda_{\text{sft}} \nabla_{\theta} \log \pi_{\theta}(y_{\text{sft}}|x)]
$$
\n(7.1.1.2)

where m = δ<sup>m</sup> −log πθ(yw|x)+log πθ(y<sup>l</sup> |x). The gradient coefficients are GC<sup>w</sup> SLiC-HF <sup>=</sup> I(m > 0), GC<sup>l</sup> SLiC-HF = −I(m > 0), and GCsft SLiC-HF = λsft. Here, δ<sup>m</sup> acts as a margin separating desired from undesired responses, while the regularization term λsft log πθ(ysft | x) encourages the learned policy to remain close to the initial SFT model.

The authors proposed two variants: SLiC-HF-direct and SLiC-HF-sample-rank. SLiC-HF-direct directly uses human preference data to define the preferred response y<sup>w</sup> and the dispreferred response y<sup>l</sup> . In contrast, SLiC-HF-sample-rank first generates multiple responses from the SFT model and then employs a ranking or reward model to select y<sup>w</sup> and y<sup>l</sup> . By drawing training samples from the SFT model's own output distribution, the sample-rank variant yields more stable learning and was found to converge more robustly.

DPO-Positive (DPOP) Unlike DPO, which only enforces a relative preference margin between preferred and dispreferred responses, DPOP [\(Pal et al., 2024\)](#page-105-1) additionally penalizes any drop in the preferred response's absolute likelihood below the reference model, directly

<span id="page-72-1"></span>fixing the failure mode where DPO degrades preferred-response quality on near-identical response pairs. To be more specific, DPOP modifies DPO to avoid pathological updates where the likelihood of preferred outputs also decreases. This phenomenon is theoretically proven and is especially severe when response pairs have small edit distances (e.g., "2+2=4" vs. "2+2=5"). To expose this limitation, they constructed modified ARC [\(Clark et al., 2018\)](#page-98-9), HellaSwag [\(Zellers et al., 2019\)](#page-111-6), and Metamath [\(Yu et al., 2024\)](#page-110-7) datasets enriched with small-edit-distance pairs, and proposed DPOP, defined in Eq. [7.1.1.3,](#page-72-0) where the added hinge term <sup>λ</sup>pos max 0, log πref (yw|x) πθ(yw|x) prevents the preferred response from becoming less likely than under the reference.

<span id="page-72-0"></span>
$$
J_{\text{DPOP}}(\pi_{\theta}) = \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left\{ \log \left[ \sigma \left( \beta \log \frac{\pi_{\theta}(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \beta \log \frac{\pi_{\theta}(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right) \right] - \lambda_{\text{pos}} \max \left( 0, \log \frac{\pi_{\text{ref}}(y_w | x)}{\pi_{\theta}(y_w | x)} \right) \right\}
$$
(7.1.1.3)

The gradient follows the unified form (Eq. [2.1.1.1\)](#page-6-3), where the GC for positive response is GC<sup>w</sup> DPOP <sup>=</sup> β σ β log <sup>π</sup>θ(y<sup>l</sup> |x) πref (y<sup>l</sup> <sup>|</sup>x) <sup>−</sup> <sup>β</sup> log <sup>π</sup>θ(yw|x) πref (yw|x) + λpos I(πref(yw|x) > πθ(yw|x)) and the GC for negative response is GC<sup>l</sup> DPOP <sup>=</sup> <sup>−</sup>β σ β log <sup>π</sup>θ(y<sup>l</sup> |x) πref (y<sup>l</sup> <sup>|</sup>x) <sup>−</sup> <sup>β</sup> log <sup>π</sup>θ(yw|x) πref (yw|x) . The first term in GC<sup>w</sup> matches the standard DPO coefficient, while the indicator term activates when the preferred response likelihood drops below the reference, providing an additional upward push.

Stepwise DPO (sDPO) Standard DPO fixes the SFT model as the reference throughout training, but since the reference model acts as an alignment lower bound, a weakly aligned reference limits how well the target model can ultimately be optimized. sDPO extends DPO by iteratively updating the reference model to provide a progressively stronger lower bound for optimization [\(Kim et al., 2025\)](#page-101-10). Preference data are partitioned into stages, and DPO is applied sequentially; the partially aligned model from each stage is reused as the reference model for the next stage. This procedure improved performance over standard DPO on multiple-choice benchmarks and yielded a monotonic increase in rref(x, yw, yl) = log <sup>π</sup>ref (yw|x) πref (y<sup>l</sup> |x) , while also reducing the initial optimization loss when initializing from the updated reference.

β-DPO DPO is highly sensitive to the choice of the trade-off parameter β, particularly under varying pairwise data quality. β-DPO [\(Wu et al., 2024\)](#page-109-9) systematically investigates the joint influence of β and preference data quality. The authors observe that low-gap pairs where the chosen and rejected responses exhibit small reward discrepancies typically benefit from smaller β values, enabling more assertive policy updates. In contrast, high-gap pairs, characterized by large reward discrepancies, require larger β values to avoid overfitting and overly aggressive updates. To address the limitations of a static β, the paper proposes batch-level dynamic βbatch calibration. Specifically, βbatch is adjusted based on the average reward discrepancy within each batch in Eq. [7.1.1.4.](#page-72-0)

$$
\beta_{\text{batch}} = [1 + \alpha_{\beta} (\mathbb{E}_{i \sim \text{batch}}[M_i] - M_0)] \beta_0 \tag{7.1.1.4}
$$

Here, <sup>M</sup><sup>i</sup> <sup>=</sup> <sup>β</sup><sup>0</sup> log πθ(y (i) <sup>w</sup> |x (i) ) πref (y (i) <sup>w</sup> |x(i)) <sup>−</sup>β<sup>0</sup> log πθ(y (i) l |x (i) ) πref (y (i) l |x(i)) is the individual reward discrepancy for triplet i, measuring the log-probability gap between the winning and losing responses

<span id="page-73-0"></span>under the implicit DPO reward model. The threshold M<sup>0</sup> is not fixed but is dynamically maintained as a momentum-based running mean of M<sup>i</sup> across batches, i.e., M<sup>0</sup> ← mM<sup>0</sup> + (1 − m)Ei∼batch[M<sup>i</sup> ] with momentum m ∈ [0, 1). Then, β-guided data filtering reduces the influence of outliers by assigning each triplet a sampling probability proportional to a Gaussian centered at M0, so samples with reward discrepancies far from the mean are selected less frequently.

Identity Preference Optimization (IPO) Two key assumptions underlying RLHF are identified: (i) pairwise preferences are substituted with pointwise rewards, and (ii) a reward model trained on such rewards is assumed to generalize to out-of-distribution samples [\(Azar et al., 2024\)](#page-97-6). While DPO avoids the second approximation by directly optimizing the policy from preference data, it still relies on the first through the BT formulation. As a result, DPO continues to depend on a pointwise-reward assumption and can lose effective KL regularization under deterministic preferences. The authors showed that substituting pairwise preferences with pointwise rewards can lead to instability when preferences are deterministic or nearly deterministic, i.e., P(y<sup>w</sup> > yl) = 1. In this regime, rθ(x, yw) − rθ(x, yl) = β h log πθ(yw|x) πref (yw|x) − log πθ(y<sup>l</sup> |x) πref (y<sup>l</sup> |x) i → +∞ which effectively weakens the KL regularization imposed by β and can cause overfitting to the preference dataset. To address this issue, the authors proposed IPO, which directly optimizes preference probabilities while retaining KL regularization to a reference policy, as shown in Eq. [7.1.1.5.](#page-72-0)

$$
\pi^*(y|x) = \arg\max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}} \left[ \mathbb{E}_{y \sim \pi_\theta(y|x), y' \sim \pi_\theta'(y|x)} P(y > y'|x) - \beta D_{\mathrm{KL}}(\pi_\theta(\cdot|x) || \pi_{\mathrm{ref}}(\cdot|x)) \right]
$$
\n(7.1.1.5)

In this formulation, π ′ θ (y|x) denotes a fixed sampling or behavior policy (typically the data-collection policy) used to draw comparison responses, and it is not optimized during training. From this objective, the authors derived a squared-loss formulation that can be optimized directly from preference data, avoiding both reward modeling and reinforcement learning, as shown in Eq. [7.1.1.6.](#page-72-0) The gradient follows the unified form (Eq. [2.1.1.1\)](#page-6-3) with coefficients GC<sup>w</sup> IPO = −2 log <sup>π</sup>θ(yw|x) <sup>π</sup>ref (yw|x) <sup>−</sup> log <sup>π</sup>θ(y<sup>l</sup> |x) πref (y<sup>l</sup> <sup>|</sup>x) − 1 2β and GC<sup>l</sup> IPO = 2 log <sup>π</sup>θ(yw|x) <sup>π</sup>ref (yw|x) <sup>−</sup> log <sup>π</sup>θ(y<sup>l</sup> |x) πref (y<sup>l</sup> <sup>|</sup>x) − 1 2β .

$$
J_{\text{IPO}}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left\{-\left[\log\left(\frac{\pi_{\theta}(y_w|x)}{\pi_{\text{ref}}(y_w|x)}\right) - \log\left(\frac{\pi_{\theta}(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right) - \frac{1}{2\beta}\right]^2\right\} (7.1.1.6)
$$

This objective constrains the gap between the log-likelihood ratios of preferred and dispreferred responses, ensuring that the learned policy remains close to the reference model even under deterministic preferences.

Reward-aware Preference Optimization (RPO) Prior work on DPO ignores the reward scores between different preference pairs. RPO [\(Sun et al., 2025\)](#page-107-8) was proposed to exploit this information. The objective function is shown in Eq. [7.1.1.7](#page-74-0) to minimize the gap between the implicit and explicit reward differences where g(x, y) = σ(y)log σ(y) σ(x) + (1 −

$$
\sigma(y)) \log\left(\frac{1-\sigma(y)}{1-\sigma(x)}\right).
$$

<span id="page-74-2"></span><span id="page-74-0"></span>
$$
J_{\text{RPO}}(\pi_{\theta}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}} g\left(\beta \log \left(\frac{\pi_{\theta}(y_w|x)}{\pi_{\text{ref}}(y_w|x)}\right) - \beta \log \left(\frac{\pi_{\theta}(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right),\right)
$$

$$
\eta(r_{\phi}(x,y_w) - r_{\phi}(x,y_l))\right)
$$
(7.1.1.7)

The gradient coefficients are GC<sup>w</sup> RPO = −GC<sup>l</sup> RPO = β(σ(c) − σ(zθ)), where the implicit reward difference z<sup>θ</sup> = β log πθ(yw|x) πref (yw|x) − log πθ(y<sup>l</sup> |x) πref (y<sup>l</sup> |x) and the explicit reward difference c = η(rϕ(x, yw) − rϕ(x, yl)).

Generalized Preference Optimization (GPO) Unlike DPO, IPO, and SLiC-HF, which each fix a specific loss function independently, GPO [\(Tang et al., 2024\)](#page-108-5) unifies them under a single family parameterized by a convex function f, enabling principled comparisons of existing algorithms and a systematic study of how the choice of f governs the implicit offline regularization. GPO applied a Taylor expansion around 0 to the loss, as shown in Eq. [7.1.1.8,](#page-74-0) where <sup>r</sup>θ(x, yw, yl) = <sup>β</sup> log πθ(yw|x) πref (yw|x) − β log πθ(y<sup>l</sup> |x) πref (y<sup>l</sup> |x) .

$$
J_{\text{GPO}}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}[-f(r_{\theta}(x,y_w,y_l))]
$$
  
\n
$$
\approx -f(0) - f'(0)\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}[r_{\theta}(x,y_w,y_l)] - \frac{f''(0)}{2}\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}[(r_{\theta}(x,y_w,y_l))^2]
$$
\n(7.1.1.8)

The general gradient coefficients are GC<sup>w</sup> GPO = −βf′ (rθ) and GC<sup>l</sup> GPO = βf′ (rθ). For DPO, f(r) = − log σ(r) yields f ′ (r) = −σ(−r), so GC<sup>w</sup> = βσ(−rθ(x, yw, yl))), recovering the standard DPO gradient coefficient. −f ′ (0)E(x,yw,yl)∼D[rθ(x, yw, yl)] was termed preference optimization: it focuses on maximizing the difference between desired and undesired responses, playing a role analogous to a reward signal. − f ′′(0) 2 <sup>E</sup>(x,yw,yl)∼D[(rθ(x, yw, yl))<sup>2</sup> ] was termed offline regularization: its goal lies in minimizing the difference between the current policy and the reference policy, analogous to a KL divergence penalty.

### <span id="page-74-1"></span>7.1.2 Single Response

Most RLHF/PPO methods follow a single-response paradigm: a response is sampled from the policy given a prompt, a reward is derived, advantages are computed, and the LLM is optimized via PPO. In the offline setting, binary feedback (e.g., thumbs up/down) is often more practical to collect than pairwise rankings. KTO [\(Ethayarajh et al., 2024a\)](#page-99-7) and DRO [\(Richemond et al., 2024\)](#page-106-7) investigate how to align policies from such single-trajectory signals, bypassing the need for contrastive preference pairs. More recently, UNA [\(Ethayarajh et al.,](#page-99-8) [2024b\)](#page-99-8) leverages pointwise reward signals to bridge offline preference learning and online PPO, across pairwise, binary and pointwise feedback.

Kahneman-Tversky Optimization (KTO) Unlike DPO, which maximizes pairwise preference likelihood via the BT model, KTO [\(Ethayarajh et al., 2024a\)](#page-99-7) directly optimizes LLM from cheap unpaired binary (desirable/undesirable) feedback without requiring ranked response pairs. Motivated by Kahneman and Tversky's prospect theory [\(Tversky and](#page-108-6) [Kahneman, 1992\)](#page-108-6), KTO adopts a human-aware value function that captures loss aversion.

<span id="page-75-5"></span>When applied to LLM alignment, the prospect-theoretic value is instantiated via a sigmoid utility over rewards <sup>z</sup> <sup>=</sup> <sup>r</sup>θ(x, y) = <sup>β</sup> log πθ(y|x) πref (y|x) , yielding the unified form in Eq. [7.1.2.1.](#page-75-0)

<span id="page-75-0"></span>
$$
v(z) = \begin{cases} (z - z_0)^{\alpha} & \text{if } z \ge z_0 \Rightarrow \lambda_D \sigma(r_{\theta}(x, y_w) - z_0) \quad \text{for } (x, y_w) \sim \mathcal{D} \\ -\lambda (z_0 - z)^{\alpha} & \text{if } z < z_0 \Rightarrow \lambda_U \sigma(z_0 - r_{\theta}(x, y_l)) \quad \text{for } (x, y_l) \sim \mathcal{D} \end{cases}
$$
(7.1.2.1)

Here, λ<sup>y</sup> ∈ {λD, λ<sup>U</sup> } refers to the weight/sensitivity for desirable and undesired examples, and z<sup>0</sup> denotes the reference point in Eq. [7.1.2.2.](#page-75-1) The KTO objective is then derived in Eq. [7.1.2.3.](#page-75-1)

<span id="page-75-1"></span>
$$
z_0 = \beta \mathbb{E}_{x \sim \mathcal{D}}[D_{\mathrm{KL}}(\pi_\theta(\cdot|x) || \pi_{\mathrm{ref}}(\cdot|x))] = \max\left(0, \frac{1}{m} \sum_{i \neq j} \beta \log \frac{\pi_\theta(y_j | x_i)}{\pi_{\mathrm{ref}}(y_j | x_i)}\right) \tag{7.1.2.2}
$$

$$
J_{\rm KTO}(\pi_{\theta}) = \mathbb{E}_{(x,y)\sim\mathcal{D}}[v_{\theta}(x,y) - \lambda_y]
$$
\n(7.1.2.3)

Treating z<sup>0</sup> as a constant (computed as a batch statistic), the gradient follows the unified form where the gradient coefficient depends on desirability: GC<sup>w</sup> KTO = λ<sup>D</sup> β σ(rθ(x, yw) − z0)(1 − σ(rθ(x, yw) − z0)) and GC<sup>l</sup> KTO = −λ<sup>U</sup> β σ(z<sup>0</sup> − rθ(x, yl))(1 − σ(z<sup>0</sup> − rθ(x, yl))).

Direct Reward Optimization (DRO) While KTO uses prospect-theoretic utility assumptions to handle binary feedback, DRO [\(Richemond et al., 2024\)](#page-106-7) derives its alignment objective from first principles by directly leveraging the KL-regularized RLHF optimality condition, jointly optimizing both the policy and a learned value function without relying on any utility model. DRO reformulated the policy-reward relationship in Eq. [7.1.2.4](#page-75-1) where V (x) = β log(Z(x)).

$$
r(x,y) - V(x) = \beta \log \left( \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right)
$$
 (7.1.2.4)

The resulting DRO objective minimizes mean squared error, as in Eq. [7.1.2.5.](#page-75-2)

<span id="page-75-2"></span>
$$
J_{\text{DRO}}(\pi_{\theta}, V_{\phi}) = \mathbb{E}_{(x,y)\sim\mathcal{D}}\left[-\frac{1}{2}\left(r(x,y) - V_{\phi}(x) - \beta \log\left(\frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)}\right)\right)^{2}\right]
$$
(7.1.2.5)

Since estimating V (x) is challenging, DRO-V approximates it with a neural network Vϕ, jointly optimizing policy and value networks. The policy gradient resembles standard policy gradient with value baseline plus regularization and the value update is similar to TD learning with a KL divergence term in Eq. [7.1.2.6](#page-75-3) and Eq. [7.1.2.7](#page-75-4) with GCDRO = β r(x, y) − V<sup>ϕ</sup> − β log <sup>π</sup>θ(y|x) πref (y|x) .

<span id="page-75-3"></span>
$$
\nabla_{\theta} J(\pi_{\theta}, V_{\phi}) = \mathbb{E}_{(x, y) \sim \mathcal{D}} \left[ \beta \left( r(x, y) - V_{\phi} - \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) \nabla_{\theta} \log \pi_{\theta}(y|x) \right] \tag{7.1.2.6}
$$

<span id="page-75-4"></span>
$$
\nabla_{\phi} J(\pi_{\theta}, V_{\phi}) = -\mathbb{E}_{(x,y)\sim\mathcal{D}} \left\{ \left[ V_{\phi} - r(x,y) + \beta \log \left( \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) \right] \nabla_{\phi} V_{\phi} \right\}
$$
(7.1.2.7)

Key implementation details include separate policy/value networks, rescaling the policy gradient by 1/β, and using multiple value outputs per batch.

<span id="page-76-3"></span>UNified Alignment (UNA) RLHF/PPO is computationally expensive and unstable, DPO is restricted to pairwise preference data, and KTO handles only binary feedback, leaving scalar reward signals from reward models and LLMs unexploited. UNA [\(Ethayarajh](#page-99-8) [et al., 2024b\)](#page-99-8) bridges this gap by providing a unified framework that accommodates all three feedback types through a generalized implicit reward function. Starting from the same objective of RLHF and DPO, UNA proves that the optimal policy satisfies Eq. [7.1.2.8](#page-76-0) via the log-sum inequality rather than DPO's partition-function argument

<span id="page-76-0"></span>
$$
r_{\theta}(x, y) = \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)}
$$
\n(7.1.2.8)

which eliminates the intractable partition function Z(x) present in the DPO derivation (Eq. [2.4.4.1\)](#page-14-0). With this implicit reward, UNA reframes all alignment as minimizing the gap between implicit and explicit rewards. While UNA supports any discrepancy measure g (e.g., MSE, BCE), we present the MSE instantiation in Eq. [7.1.2.9](#page-76-1) where r<sup>ϕ</sup> is an explicit reward from human labels, a reward model, or an LLM evaluator. The gradient follows the unified form (Eq. [2.1.1.1\)](#page-6-3) with coefficient GCUNA = −2β (rθ(x, y) − rϕ(x, y)).

<span id="page-76-1"></span>
$$
J_{\text{UNA}} = -\mathbb{E}_{(x,y)\sim\mathcal{D}} \left[ r_{\theta}(x,y) - r_{\phi}(x,y) \right]^2 \tag{7.1.2.9}
$$

For pairwise data, UNA is mathematically equivalent to DPO. For binary feedback (thumbs up/down treated as scores 1/0), it improves over KTO. For scalar scores from reward models or LLMs, it enables reward distillation, outperforming both DPO and KTO.

### <span id="page-76-2"></span>7.1.3 List Responses

While previous PPO/DPO studies focused on pairwise preferences or binary response, the following methods have explored direct listwise preference optimization for LLMs.

Rank Responses to align language models with Human Feedback (RRHF) RLHF training required multiple components, including a policy, value (or value head), reward, and reference model, leading to high memory costs. To reduce this overhead, the authors proposed RRHF, which incorporated alignment directly into SFT while achieving comparable performance [\(Yuan et al., 2023b\)](#page-111-7). RRHF sampled multiple responses from different models and rank them with training model's own length-normalized log probabilities, training the model to match rankings from reward models or human annotators, as shown in Eq. [7.1.3.1.](#page-76-2)

$$
J_{\text{RRHF}}(\pi_{\theta}) = \mathbb{E}_{(x,y,\phi)\sim\mathcal{D}}\left[-\sum_{\phi_i < \phi_j} \max\left(0, \frac{\log \pi_{\theta}(y_i|x)}{|y_i|} - \frac{\log \pi_{\theta}(y_j|x)}{|y_j|}\right) + \log \pi_{\theta}(y_{i'}|x)\right] \tag{7.1.3.1}
$$

− P ϕi<ϕ<sup>j</sup> max 0, log πθ(yi|x) <sup>|</sup>yi<sup>|</sup> − log πθ(y<sup>j</sup> |x) |y<sup>j</sup> | penalizes rank-order violations between the model's length-normalized log probabilities and human reward rankings ϕi(x, yi), ϕ<sup>j</sup> (x, y<sup>j</sup> ). i ′ denotes the optimal response from the multiple candidates, and log πθ(y<sup>i</sup> ′|x) is the SFT term for instruction following. Compared to PPO, RRHF requires neither a reference model nor a value model, and can dispense with the reward model entirely when rankings are provided directly by human annotators.

<span id="page-77-0"></span>Preference Ranking Optimization (PRO) While RRHF's hinge loss assigns a binary gradient signal to each rank violation regardless of the preference gap, PRO [\(Song et al.,](#page-107-9) [2024\)](#page-107-9) integrates alignment directly into SFT via an InfoNCE-based objective with a dynamic temperature that scales each contrast proportionally to the reward gap, enabling gap-aware optimization over listwise preference rankings of arbitrary length. Suppose there is one prompt x and K responses y1, y2, . . . , yK, which are ranked based on the preference scores, i.e., y<sup>1</sup> > y<sup>2</sup> > . . . > yK. This can be decomposed into K sub-tasks. The first sub-task takes y<sup>1</sup> as the positive sample while y2, . . . , y<sup>K</sup> are negative samples. In the second sub-task, y<sup>1</sup> is dropped, y<sup>2</sup> becomes the positive sample, and y3, . . . , y<sup>K</sup> remain negative. This process continues for K−1 sub-tasks. Based on these K−1 sub-tasks and InfoNCE, the alignment objective is formulated as shown in Eq. [7.1.3.2](#page-76-2)

$$
J_{\text{align}}(\pi_{\theta}) = \mathbb{E}_{(x,y)\sim\mathcal{D}}\left[\log\left(\prod_{k=1}^{K-1} \frac{\exp\left(\frac{r_{\theta}(x,y_k)}{T_k^k}\right)}{\sum_{i=k}^K \exp\left(\frac{r_{\theta}(x,y_i)}{T_i^k}\right)}\right)\right]
$$
(7.1.3.2)

where T k <sup>i</sup> = 1 <sup>r</sup>θ(x,yk)−rθ(x,yi) measures the distances between two responses, and T k <sup>k</sup> = mini>k T k <sup>i</sup> measures the minimum distance between the positive response y<sup>k</sup> and all negative responses yk+1, . . . , y<sup>K</sup> for the k-th task. Lastly, the overall PRO objective merges SFT and alignment: JPRO(πθ) = JSFT(πθ) + αJalign(πθ).

Listwise Preference Optimization (LiPO) Pairwise methods like DPO treat every pair from a ranked list independently and discard permutation structure beyond K=2, while even existing listwise methods such as DPOPL and PRO optimize rank-ordering alone without exploiting actual score magnitudes. LiPO [\(Liu et al., 2025c\)](#page-103-0) draws inspiration from Learning-to-Rank methodologies [\(Liu et al., 2009\)](#page-103-6) to handle listwise data directly. The authors highlight two main advantages of using listwise preferences: (1) evaluating all candidates under the same prompt systematically enhances policy learning, and (2) leveraging the relative label values between responses improves alignment. The LiPO loss function is defined in Eq. [7.1.3.3](#page-76-2)

$$
J_{\text{lambda-loss}}(\pi_{\theta}) = \mathbb{E}_{(x,y,\phi)\sim\mathcal{D}}\left[\sum_{\phi_i > \phi_j} \Delta_{i,j} \log\left(1 + e^{-(s_i - s_j)}\right)\right]
$$
(7.1.3.3)

where ∆i,j = |G<sup>i</sup> −G<sup>j</sup> | 1 <sup>D</sup>(τ(i)) − 1 D(τ(j))  is the Lambda weight, and <sup>G</sup><sup>i</sup> is the gain of response yi , defined as G<sup>i</sup> = 2rϕ(x, yi) − 1 with ϕi(x, yi) denoting human-labelled scores. D is a rank discount function with D(τ (si)) = log(1 + τ (si)), where τ (si) is the rank position of y<sup>i</sup> in the ranking permutation induced by s. Thus, LiPO is a listwise method even though its loss can be written in terms of pairs. s refers to the scores of each response as shown s(πθ) = {s1, . . . , sK} = n β log πθ(y1|x) πref (y1|x) , . . . , β log πθ(yK|x) πref (yK|x) o. The authors also evaluated alternative loss functions: Llist\_mle, Lpair\_logistic, Lpair\_hinge, Lpoint\_mse, Lpoint\_sigmoid, and Lsoftmax. Experiments yielded the ranking: Llambda-loss > (Llist\_mle ≈ Lpair\_logistic ≈ Lpair\_hinge) > Lsoftmax > Lpoint\_sigmoid > Lpoint\_mse.

### <span id="page-78-3"></span><span id="page-78-0"></span>7.2 Reward

Reward design is central to preference-based alignment, as the reward structure directly shapes what behaviors a policy learns to reinforce or suppress. This section categorizes methods by reward granularity: pairwise rewards compare responses directly, with extensions to token-level MDPs; pointwise rewards assign absolute scalar scores and underpin most RLHF pipelines; listwise rewards rank multiple responses simultaneously; and negative rewards focus solely on suppressing undesired outputs. Figure [7](#page-78-1) provides a concrete example contrasting different response types and their corresponding reward signals.

![](./assets/01-rl-post-training-survey/_page_78_Figure_3.jpeg)

<span id="page-78-1"></span>Figure 7: RLHF and DPO Response and Reward generation: Pairwise Reward, Pointwise Reward, Token-level Pairwise Reward, Negative Reward and Listwise Reward.

## 7.2.1 Pairwise Reward

The BT reward model trained from pairwise preference data underlies DPO [\(Rafailov et al.,](#page-106-3) [2023\)](#page-106-3) and its many variants surveyed in Section [7.1.1.](#page-71-1)

### <span id="page-78-2"></span>7.2.2 Token-level Pairwise Reward

Originally derived in a contextual bandit setting, DPO assigns reward to a response as a whole, leaving token-level credit assignment implicit. This line of work reinterprets DPO within a token-level MDP framework, making that credit assignment explicit and tractable.

DPO: from r to Q Although DPO solves the same KL-regularized objective as RLHF, it was derived in a contextual bandit setting, i.e., treating the full response as a single arm, while classical RLHF explicitly optimizes over token-level MDPs. This mismatch leaves

<span id="page-79-0"></span>open whether DPO can perform token-level credit assignment or be extended to sequential multi-step tasks. In this work, it is demonstrated that DPO was capable of performing token-level credit assignment [\(Rafailov et al., 2024\)](#page-106-8). The token-level MDP is defined as M = (S, A, f, r, ρ0), where S is the state space, A is the action space, f(s|a) describes the state transition given an action, r is the reward function, and ρ<sup>0</sup> is the initial state distribution. The token-level MDP is formulated within the maximum entropy RL framework, as illustrated in Eq. [7.2.2.1.](#page-78-2)

$$
\pi^*(y|x) = \arg\max_{\pi_\theta} E_{a_t \sim \pi_\theta(a_t|s_t)} \left\{ \sum_{t=0}^T \left[ r_\theta(s_t, a_t) + \beta \log \left( \pi_{\text{ref}}(a_t|s_t) \right) \right] + \beta H(\pi_\theta) \middle| s_0 \sim \rho(s_0) \right\} \tag{7.2.2.1}
$$

Under maximum entropy RL, the relationship between the optimal Q-function Qθ(s<sup>t</sup> , at) and the optimal value function Vθ(st) is given in Eq. [7.2.2.2.](#page-78-2)

$$
Q_{\theta}(s_t, a_t) - V_{\theta}(s_t) = \beta \log(\pi_{\theta}(a_t|s_t))
$$
\n(7.2.2.2)

The Bellman equation is given in Eq. [7.2.2.3.](#page-78-2)

$$
Q_{\theta}(s_t, a_t) = r_{\theta}(s_t, a_t) + \beta \log(\pi_{\text{ref}}(a_t|s_t)) + V_{\theta}(s_{t+1})
$$
\n(7.2.2.3)

Substituting Qθ(s<sup>t</sup> , at) from Eq. [7.2.2.3](#page-78-2) into Eq. [7.2.2.2](#page-78-2) yields rθ(s<sup>t</sup> , at) = Vθ(st) − Vθ(st+1) + β log πθ(at|st) πref (at|st) . Summing both sides over t and using Vθ(s<sup>T</sup> ) = 0, the cumulative reward can be re-expressed as in Eq. [7.2.2.4.](#page-78-2)

$$
\sum_{t=0}^{T-1} r_{\theta}(s_t, a_t) = V_{\theta}(s_0) + \sum_{t=0}^{T-1} \beta \log \left( \frac{\pi_{\theta}(a_t|s_t)}{\pi_{\text{ref}}(a_t|s_t)} \right)
$$
(7.2.2.4)

The term Vθ(s0) cancels when substituted into the BT model, as shown in Eq. [7.2.2.5,](#page-78-2) where y<sup>w</sup> contains N tokens and y<sup>l</sup> contains M tokens.

$$
P_{\theta}(y_w > y_l) = \sigma \left[ \sum_{t=0}^{N-1} \beta \log \left( \frac{\pi_{\theta}(a_t^w | s_t^w)}{\pi_{\text{ref}}(a_t^w | s_t^w)} \right) - \sum_{t=0}^{M-1} \beta \log \left( \frac{\pi_{\theta}(a_t^l | s_t^l)}{\pi_{\text{ref}}(a_t^l | s_t^l)} \right) \right]
$$
(7.2.2.5)

As a result, the bandit formulation was extended to a token-level MDP, where each token generation received a reward β log πθ(at|st) πref (at|st) .

Token-level DPO (TDPO) DPO regularizes the policy at the response level, but LLM generation is inherently sequential and auto-regressive. TDPO [\(Zeng et al., 2024\)](#page-111-8) exploits this structure by introducing forward KL (sequential KL divergence) constraints at the token level rather than at the sentence level, enabling finer-grained diversity control. In addition, the reward discount is set to one and the token-wise reward is defined as rθ,t = rθ([x, y<t], y<sup>t</sup> ). The Q-value, value function, and advantage function are defined accordingly, with the total reward rθ(x, y) = P<sup>T</sup> <sup>t</sup>=1 rθ([x, y<t], y<sup>t</sup> ). The TDPO objective is then formulated in Eq. [7.2.2.6.](#page-78-2)

$$
\pi^*(y|x) = \arg\max_{\pi_\theta} \mathbb{E}_{x,y} \leq t_{\infty} \mathcal{D}\left[\mathbb{E}_{y^t \sim \pi_\theta(y^t|[x,y^{\n(7.2.2.6)
$$

<span id="page-80-0"></span>From this objective, the relationship between the Q-value and the optimal policy is derived in Eq. [7.2.2.7.](#page-78-2)

$$
Q^{\pi_{\text{ref}}}([x, y^{
$$

However, since Z([x, y<t <sup>w</sup> ]) ̸= Z([x, y<t l ]), the normalization terms cannot be canceled as in DPO. To resolve this, the authors introduced a sequential KL divergence defined in Eq. [7.2.2.8.](#page-78-2)

$$
D_{\text{SeqKL}}(x, y; \pi_1 || \pi_2) = \sum_{t=1}^{T} D_{\text{KL}}(\pi_1(\cdot | [x, y^{(7.2.2.8)
$$

With sequential KL divergence, the normalization terms cancel under the BT model, yielding Eq. [7.2.2.9.](#page-78-2)

$$
P_{\theta}(y_w > y_l|x) = \sigma(r_{\theta}(x, y_w) - r_{\theta}(x, y_l)) = \sigma(u_{\theta}(x, y_w, y_l) - \delta_{\theta}(x, y_w, y_l)) \quad (7.2.2.9)
$$

Here, u<sup>θ</sup> captures the log-probability ratio between the policy and reference model, while δ<sup>θ</sup> accounts for the difference in sequential forward KL divergence between preferred and dispreferred responses. The resulting preference probability is optimized using cross-entropy loss, and stopping the gradient on y<sup>w</sup> is further proposed to improve performance.

## 7.2.3 Pointwise Reward

Pointwise reward methods assign an absolute scalar score to each individual response rather than comparing pairs. This is the predominant reward structure in RLHF and RLVR pipelines, where a trained reward model or rule-based verifier scores each response independently. For offline policy learning, KTO, DRO and UNA utilize pointwise rewards and they can be found in Section [7.1.2.](#page-74-1) In particular, UNA utilizes pointwise reward, while KTO and DRO utilize binary rewards.

# 7.2.4 List Reward

Listwise reward methods generalize pairwise comparisons by assigning ranked scores to multiple responses simultaneously, providing a richer training signal. As with the listwise response methods described above in Section [7.1.3,](#page-76-2) these approaches can more fully exploit the relative ordering of candidate responses under the same prompt.

# 7.2.5 Negative Reward

Recent studies show that modern LLMs often surpass human performance in tasks like translation and summarization. Consequently, model-generated outputs can serve as preferred responses, while undesired outputs are leveraged for alignment to suppress harmful behavior.

Distributional Dispreference Optimization (D2O) Unlike DPO, which optimizes at the instance level over paired positive and negative responses, Negating Negatives proposes D2O [\(Duan et al., 2024\)](#page-99-9), which operates at the distribution level using only humanlabeled negative samples, replacing noisy human positives with on-policy self-generated responses as anchors. They therefore proposed to discard human-labeled positive samples, <span id="page-81-3"></span>generate new positive responses with an LLM, and train on these LLM-generated positive responses paired with human-labeled negative responses. The D2O objective is defined in Eq. [7.2.5.1](#page-81-1) where y<sup>i</sup> ∼ πref(y|x) are G sampled responses. The reference models π + ref and π − ref represent more aligned models (previous iteration) and less aligned models (initial) respectively. The objective maximizes divergence from harmful responses, effectively suppressing undesirable behaviors. The gradient coefficient for the on-policy response y<sup>i</sup> is GC<sup>w</sup> <sup>D</sup>2<sup>O</sup> = γ G σ α log <sup>π</sup>θ(y<sup>l</sup> |x) π + ref (y<sup>l</sup> |x) − γ G P<sup>G</sup> <sup>j</sup>=1 log <sup>π</sup>θ(y<sup>j</sup> <sup>|</sup>x) π − ref (y<sup>j</sup> |x) , and for the undesired response y<sup>l</sup> it is GC<sup>l</sup> <sup>D</sup>2<sup>O</sup> <sup>=</sup> <sup>−</sup>α σ α log <sup>π</sup>θ(y<sup>l</sup> |x) π + ref (y<sup>l</sup> |x) − γ G P<sup>G</sup> <sup>j</sup>=1 log <sup>π</sup>θ(y<sup>j</sup> <sup>|</sup>x) π − ref (y<sup>j</sup> |x) .

<span id="page-81-1"></span>
$$
J_{\mathcal{D}^2\mathcal{O}}(\pi_{\theta}) = \mathbb{E}_{(x,y_l)\sim\mathcal{D}}\left\{\log\left[\sigma\left(\frac{\gamma}{G}\sum_{i=1}^G \log\frac{\pi_{\theta}(y_i|x)}{\pi_{\text{ref}}^-(y_i|x)} - \alpha\log\frac{\pi_{\theta}(y_l|x)}{\pi_{\text{ref}}^+(y_l|x)}\right)\right]\right\}
$$
(7.2.5.1)

Negative Preference Optimization (NPO) Gradient ascent (GA) can suppress undesired responses but often degrades overall performance [\(Maini et al., 2024\)](#page-103-7). To mitigate this, NPO adapts DPO by retaining only the negative component [\(Zhang et al., 2024\)](#page-112-9), discarding the positive response y<sup>w</sup> entirely. NPO significantly slows catastrophic collapse. The NPO objective is defined in Eq. [7.2.5.2,](#page-81-2) where y<sup>l</sup> ∼ DFG denotes the human-labeled negative (forget) sample.

<span id="page-81-2"></span>
$$
J_{\rm NPO}(\pi_{\theta}) = \mathbb{E}_{(x,y_l)\sim\mathcal{D}}\left[\frac{2}{\beta}\log\sigma\left(-\beta\log\frac{\pi_{\theta}(y_l|x)}{\pi_{\rm ref}(y_l|x)}\right)\right]
$$
(7.2.5.2)

The gradient coefficient for the undesired response y<sup>l</sup> is GC<sup>l</sup> NPO = −2 σ <sup>β</sup> log <sup>π</sup>θ(y<sup>l</sup> |x) πref(y<sup>l</sup> |x) .

Contrastive Preference Optimization (CPO) CPO was proposed to improve machine translation (MT) performance in moderately-sized LLMs [\(Xu et al., 2024b\)](#page-109-5). To construct higher-quality supervision, the authors generated translations using GPT-4 [\(OpenAI et al.,](#page-104-0) [2024\)](#page-104-0) and ALMA-13B-LoRA [\(Xu et al., 2024a\)](#page-109-10). These outputs, together with the human gold reference yref, form a triplet that is scored by reference-free evaluators where the highest-scoring translation is labeled as desired (yw) and the lowest-scoring as undesired (yl), while the intermediate-scoring translation is discarded. The resulting dataset enabled training with the CPO objective in Eq. [7.2.5.3,](#page-81-2) where y<sup>w</sup> may originate from any of the three candidates (model-generated or human reference). The gradient coefficients are GC<sup>w</sup> CPO = β σ β log <sup>π</sup>θ(y<sup>l</sup> |x) πθ(yw|x) + 1 and GC<sup>l</sup> CPO <sup>=</sup> <sup>−</sup>β σ β log <sup>π</sup>θ(y<sup>l</sup> |x) πθ(yw|x) . In particular, the reference model terms cancel, eliminating the need for an explicit πref by assuming a uniform prior, i.e., πref ∼ U. Lastly, a behavior cloning term is added to stay close to the preferred data distribution.

$$
J_{\rm CPO}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\{[\log\left(\sigma(\beta\log\pi_{\theta}(y_w|x) - \beta\log\pi_{\theta}(y_l|x))\right)] + [\log\pi_{\theta}(y_w|x)]\} \quad (7.2.5.3)
$$

### <span id="page-81-0"></span>7.3 Regularization

Regularization is central to offline alignment: without constraints, policy optimization tends to overfit to the training preferences, leading to reward hacking or degenerate outputs. This section covers methods that address regularization via entropy bonuses, alternative divergence measures, adjustments to the reference model, and explicit length penalties.

# <span id="page-82-1"></span>7.3.1 Entropy

Entropy regularization encourages the policy to maintain diversity in its output distribution, preventing collapse onto a narrow set of high-reward responses. This technique is commonly employed in PPO-based RLHF and can also be incorporated into offline policy learning in Section [7.2.2.](#page-78-2)

# <span id="page-82-0"></span>7.3.2 Divergence

Rather than relying solely on the reverse KL divergence, several approaches substitute alternative divergences to strike a more favorable balance between maximizing reward and constraining the policy to remain close to a reference model.

f-DPO Previous studies used KL divergence to minimize discrepancy between the policy and pretrained model, but found that while reward increased during alignment, response diversity decreased [\(Wiher et al., 2022\)](#page-108-7). This degradation was attributed to the KL term, prompting exploration of alternative f-divergences [\(Wang et al., 2024\)](#page-108-8) such as forward KL, reverse KL, Jensen-Shannon (JS), and α-divergence, with the general f-divergence shown in Eq. [7.3.2.1.](#page-82-0)

$$
D_f(p,q) = \mathbb{E}_{x \sim q(x)} \left[ f\left(\frac{p(x)}{q(x)}\right) \right]
$$
\n(7.3.2.1)

In this context, f represents various divergence functions. In the traditional RL framework, the reverse KL divergence, defined as f(x) = x log x, is typically employed. The authors tested the α-divergence, given by f(x) = <sup>x</sup> <sup>1</sup>−α−(1−α)x−α <sup>α</sup>(α−1) , along with the forward KL divergence, f(x) = − log x, and the Jensen-Shannon (JS) divergence, f(x) = x log x − (x + 1)log x+1 2 . These divergences are considered within the framework of the constrained objective function as illustrated in Eq. [7.3.2.2.](#page-82-0)

$$
\pi_{\theta}^{*}(y|x) = \arg \max_{\pi_{\theta}} \mathbb{E}_{(x,y)\sim\mathcal{D}} \left[ r_{\theta}(x,y) - \beta f\left(\frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)}\right) \right]
$$
  
s.t. 
$$
\sum_{y} \pi_{\theta}(y|x) = 1 \quad \forall x
$$
  

$$
\pi_{\theta}(y|x) \ge 0 \quad \forall x
$$
 (7.3.2.2)

Using the Lagrange method, the authors transformed the constraints into the objective function. In particular, the equality constraint P y πθ(y|x) = 1 is enforced via the multiplier λ, while the non-negativity constraint πθ(y|x) ≥ 0 is handled through Karush–Kuhn–Tucker (KKT) complementary slackness on the dual variables α(y) ≥ 0, yielding the transformed RL objective in Eq. [7.3.2.3.](#page-82-0)

$$
J(\pi_{\theta}, \lambda, \alpha) = \mathbb{E}_{(x,y)\sim\mathcal{D}}\left[r_{\theta}(x,y) - \beta f\left(\frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)}\right) - \lambda \left(\sum_{y} \pi_{\theta}(y|x) - 1\right) + \sum_{y} \alpha(y)\pi_{\theta}(y|x)\right]
$$
\n(7.3.2.3)

Based on the new objective function, the optimal policy can be expressed as Eq. [7.3.2.4.](#page-82-0)

$$
\pi_{\theta}(y|x) = \pi_{\text{ref}}(y|x)(f')^{-1}\left(\frac{r_{\theta}(y|x) - \lambda + \alpha(y)}{\beta}\right)
$$
\n(7.3.2.4)

<span id="page-83-2"></span>Under additional conditions, i.e., (1) πref(y|x) > 0 and (2) f ′ being invertible with 0 ∈/ dom(f ′ ), the reward function for a specific divergence f can be reformulated as Eq. [7.3.2.5.](#page-82-0)

$$
r_{\theta}(x,y) = \beta f' \left( \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) + C \tag{7.3.2.5}
$$

Integrating this reward model into the BT model enabled deriving the probability of desired over undesired responses for the objective function. Experiments revealed a rewarddiversity trade-off: RKL and JSD achieved high rewards, while FKL and α divergence showed better entropy with lower rewards. In particular, JSD matched RKL's rewards with higher diversity, suggesting its potential for future alignment research.

# <span id="page-83-0"></span>7.3.3 Reference Model

The reference model constrains the aligned policy from deviating too far from the reference model. Some methods re-examine or eliminate this reference model dependency, either by modifying how the reference enters the objective or by removing it entirely through alternative reward formulations.

Simple Preference Optimization (SimPO) DPO's implicit reward relies on the log-ratio to a reference model, which both adds memory and compute overhead and is misaligned with the average log-likelihood metric used during generation. SimPO [\(Meng et al., 2024\)](#page-103-8) eliminates both issues by adopting a reference-free, length-normalized reward that directly aligns training with inference. Firstly, they introduce length normalization ( <sup>α</sup> |y| log πθ(y|x)) to avoid length bias. Next they introduce a reward-margin γ to separate preferred and dis-preferred responses in Eq. [7.3.3.1.](#page-83-0) |yw| and |y<sup>l</sup> | are response lengths, α scales the reward difference, and the reference model can be removed. The gradient follows the unified form (Eq. [2.1.1.1\)](#page-6-3) with the built-in <sup>1</sup> |y| normalization, i.e., GC<sup>w</sup> SimPO <sup>=</sup> α σ α |yl | log πθ(y<sup>l</sup> |x) − α |yw| log πθ(yw|x) + γ and GC<sup>l</sup> SimPO <sup>=</sup> <sup>−</sup>α σ α |yl log πθ(y<sup>l</sup> |x) − α |yw| log πθ(yw|x) + γ .

$$
J_{\text{SimpO}}(\pi_{\theta}) = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left(\log\left(\sigma\left(\frac{\alpha}{|y_w|}\log\pi_{\theta}(y_w|x) - \frac{\alpha}{|y_l|}\log\pi_{\theta}(y_l|x) - \gamma\right)\right)\right) (7.3.3.1)
$$

## <span id="page-83-1"></span>7.3.4 Length Penalty

SimPO (Section [7.3.3\)](#page-83-0) has tried to solve the overlong response generation by normalizing over the response length |y|. Other than that, R-DPO focuses on generating length-controlled responses by subtracting the response length |y|.

Regularized DPO (R-DPO) R-DPO [\(Park et al., 2024\)](#page-106-9) addresses DPO's tendency to exploit preference data biases, particularly verbosity. It incorporates output length directly into the RL objective in Eq. [7.3.4.1](#page-83-1) where the term α|y| penalizes response length and α controls its significance.

$$
\pi^*(y|x) = \arg\max_{\pi_{\theta}} \mathbb{E}_{x \sim \mathcal{D}} \left\{ \mathbb{E}_{y \sim \pi_{\theta}(y|x)} \left[ r_{\theta}(x, y) - \alpha |y| \right] - \beta D_{\mathrm{KL}}(\pi_{\theta}(\cdot|x) \| \pi_{\mathrm{ref}}(\cdot|x)) \right\} \tag{7.3.4.1}
$$

<span id="page-84-2"></span>The corresponding optimal internal reward function becomes Eq. [7.3.4.2,](#page-83-1) where Z(x) = P y πref(y|x) e 1 β (rθ(x,y)−α|y|) . The resulting R-DPO objective is then Eq. [7.3.4.3.](#page-83-1)

$$
r_{\theta}^{\text{R-DPO}}(x,y) = \beta \log \left( \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right) + \beta \log Z(x) - \alpha |y| \tag{7.3.4.2}
$$

$$
J_{\text{R-DPO}}(\pi_{\theta})
$$
  
=  $\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left(\log\left(\sigma\left(\beta\log\left(\frac{\pi_{\theta}(y_w|x)}{\pi_{\text{ref}}(y_w|x)}\right)-\beta\log\left(\frac{\pi_{\theta}(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)-(\alpha|y_w|-\alpha|y_l|)\right)\right)\right)$  (7.3.4.3)

The gradient coefficient is GC<sup>w</sup> <sup>R</sup>-DPO = β σ(rθ(x, yl) − rθ(x, yw) + α(|yw|−|y<sup>l</sup> |)) for desired response and GC<sup>l</sup> <sup>R</sup>-DPO = −β σ(rθ(x, yl) − rθ(x, yw) + α(|yw|−|y<sup>l</sup> |)) for undesired responses. The length penalty α(|yw|−|y<sup>l</sup> |) shifts the sigmoid argument, increasing the gradient magnitude when the preferred response is longer and reducing it when shorter.

### <span id="page-84-0"></span>7.4 Merge SFT

A distinct line of research investigates how to combine SFT with preference optimization. Rather than running SFT and alignment as sequential stages, which can cause catastrophic forgetting, these methods either merge the two training datasets into a unified objective or combine separately trained model weights.

# 7.4.1 Merge SFT Data

One approach to unifying SFT and alignment is to reformat instruction-tuning data as preference data and optimize both jointly in a single training run. This eliminates the separate SFT stage and allows the model to simultaneously develop instruction-following ability and preference alignment.

Odds Ratio Preference Optimization (ORPO) The authors observed that SFT on desirable data also increased undesirable data probability, since such data were grammatically correct and similar to desired outputs. While PPO and DPO addressed this through separate alignment stages, ORPO [\(Hong et al., 2024\)](#page-100-6) combined these processes. The authors defined the odds ratio ORθ(x, yw, yl) in Eq. [7.4.1.1,](#page-84-1) where oddsθ(y|x) = <sup>π</sup>θ(y|x) 1−πθ(y|x) quantifies the relative likelihood of producing y<sup>w</sup> over y<sup>l</sup> .

<span id="page-84-1"></span>
$$
OR_{\theta}(x, y_w, y_l) = \frac{odds_{\theta}(y_w|x)}{odds_{\theta}(y_l|x)} = \frac{\pi_{\theta}(y_w|x) (1 - \pi_{\theta}(y_l|x))}{\pi_{\theta}(y_l|x) (1 - \pi_{\theta}(y_w|x))}
$$
(7.4.1.1)

The ORPO objective function is shown in Eq. [7.4.1.2](#page-84-1) where λ balances between SFT and ORθ(x, yw, yl).

$$
J_{\text{ORPO}} = \mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\left(\pi_{\theta}(y_w|x)\right) + \lambda\log\left(\sigma\left(\log O_{\theta}(x,y_w,y_l)\right)\right)\right] \tag{7.4.1.2}
$$

<span id="page-85-4"></span>Unified Fine-Tuning (UFT) UFT [\(Wang et al., 2025b\)](#page-108-9) takes a direct approach to merging SFT and alignment: it combines the two stages into a single training run by converting SFT data into alignment-compatible format using UNA's generalized implicit reward in Eq. [7.1.2.8.](#page-76-0) The key observation is that high-quality instruction-tuning pairs (x, y) can be treated as score-based alignment data with maximal reward rϕ(x, y) = rmax. Once reformatted, instruction-tuning and alignment data are mixed and trained jointly with the UNA MSE objective in Eq. [7.4.1.3](#page-85-1) and GCUFT = −2β β log <sup>π</sup>θ(y|x) <sup>π</sup>ref (y|x) − rϕ(x, y) .

<span id="page-85-1"></span>
$$
J_{\text{UFT}}(\pi_{\theta}) = \mathbb{E}_{(x,y)\sim\mathcal{D}_{\text{mix}}} \left[ -\left( r_{\phi}(x,y) - \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\text{ref}}(y|x)} \right)^2 \right]
$$
(7.4.1.3)

Here, Dmix combines instruction-tuning data (with r<sup>ϕ</sup> = rmax) and alignment data (with scores from human annotators, reward models, or LLMs).

# 7.4.2 Merge SFT Model

An alternative strategy is to train the SFT and alignment models separately and then merge the resulting model weights. By keeping the two objectives independent during training, this approach avoids interference and can preserve the distinct benefits of each stage.

PArallel training for LLM Fine-Tuning (PAFT) Sequential SFT and alignment training often cause catastrophic forgetting of task-specific capabilities acquired during SFT: a phenomenon known as the alignment tax [\(Ouyang et al., 2022\)](#page-105-0). To address this, PAFT [\(Pentyala et al., 2024\)](#page-106-10) performs SFT and DPO in parallel on the same pretrained model, then merges the resulting adapters. The LoRA-based δ models are defined as π SFT δ (y|x) = π SFT θ (y|x) − π pre θ (y|x) and π DPO δ (y|x) = π DPO θ (y|x) − π pre θ (y|x). The paper observes that DPO produces naturally sparse delta parameters while SFT does not, causing parameter interference during merging. To promote sparsity in the SFT adapter, an ℓ<sup>1</sup> regularization term is added to the SFT loss in Eq. [7.4.2.1.](#page-85-2)

<span id="page-85-2"></span>
$$
\mathcal{L}_{\text{SFT}_{\text{sparse}}} = \mathcal{L}_{\text{SFT}} + \lambda \|\delta_{\text{sft}}\|_1 \tag{7.4.2.1}
$$

The final merged model is then obtained by combining both sparse delta parameters with the pretrained model through Eq. [7.4.2.2,](#page-85-3) using merging strategies such as TIES [\(Yadav](#page-110-8) [et al., 2023\)](#page-110-8).

<span id="page-85-3"></span>
$$
\pi_{\theta}^{\text{merge}}(y|x) = f\left(\pi_{\theta}^{\text{pre}}(y|x), \pi_{\delta}^{\text{DPO}}(y|x), \pi_{\delta}^{\text{SFT}+\ell_1}(y|x)\right) \tag{7.4.2.2}
$$

### <span id="page-85-0"></span>8 Future Directions

Future directions are organized along the seven clusters that structure the training pipeline: the theoretical foundations of the gradient coefficient, the quality of prompts, the design of responses, the reliability of feedback and evaluation, the faithfulness of reward models, the efficiency of the learning algorithm, and extensions to new modalities, languages, and model analysis.

### <span id="page-86-2"></span><span id="page-86-0"></span>8.1 Foundations: Gradient Coefficient Theory and Convergence

Without a clear understanding of gradient coefficient behavior and convergence, practitioners tune hyperparameters by trial and error with no guarantee of correctness.

Principled Gradient Coefficient Design The gradient coefficient GC(x, y, t) in Eq. [2.1.1.1](#page-6-3) has five design axes that current work treats independently: (i) the IS ratio ρ<sup>t</sup> , which controls how much weight is given to responses generated by a previous model version, from symmetric clipping (GRPO) to asymmetric stop-gradient truncation (CISPO) to full removal (GPG); (ii) the advantage estimator A, which measures how much better a response is compared to a baseline, from a learned value function via GAE (PPO) to a group mean baseline (GRPO) to entropy-weighted token filtering (Beyond 80/20); (iii) advantage normalization, which rescales advantage values to keep training stable, from group std (GRPO) to batch std (REINFORCE++) to none (Dr. GRPO [\(Liu et al., 2025d\)](#page-103-3)); (iv) response length normalization, 1 |yi| versus group length normalization <sup>P</sup> 1 i |yi| (DAPO, Magistral); and (v) regularization, which prevents the model from drifting too far from its starting point, from a KL penalty toward πref (Eq. [2.1.1\)](#page-5-3) to an entropy bonus (Qwen3) to none (CISPO, GPG). No existing work studies how these axes interact and what combination of the five axes is optimal under a fixed compute budget?

Convergence Guarantees Can convergence guarantees be established for GRPO given its group baseline that keeps shifting during training, the large LLM action space, and the fact that the reward r(x, y) depends on the entire response rather than individual steps? If not, how can practitioners tell whether training has truly stalled or is only temporarily plateauing due to exploration?

Reference Model Design and Update The reference model πref determines the best policy the model can reach π ∗ (y|x) ∝ πref(y|x) exp(r(x, y)/β) in Eq. [2.4.4.1](#page-14-0) and sets the target for the KL penalty in Eq. [2.1.1,](#page-5-3) yet all current methods either fix it for the entire training run or update it heuristically [\(Wu et al., 2024\)](#page-109-9). When should πref be updated during training, and how does the choice between a fixed and a moving reference affect the stability of the KL penalty and the quality of the final policy?

### <span id="page-86-1"></span>8.2 Prompt: Curriculum Design and Self-Play

Prompt quality determines the diversity and difficulty of the training experiences the policy encounters.

Multi-Dimensional Curriculum Design Can a method that jointly schedules both domain and difficulty, i.e., treating each domain-difficulty combination as a separate option to explore outperform single-axis difficulty curricula? Should domain coverage and difficulty be co-scheduled, or should the policy fully cover one domain before moving to the next?

Self-Play Prompt Bias In single-agent self-play where proposer and solver share the same parameters, the proposer tends to generate tasks it already knows how to solve, which narrows the training distribution and introduces a bias that limits prompt diversity, since the model only trains on problems it can already handle. How can this bias be detected and corrected? For tasks that cannot be checked automatically (e.g., causal reasoning, scientific

hypothesis generation), how can the validity of self-generated prompts be guaranteed without human annotation?

### <span id="page-87-0"></span>8.3 Response: Sampling, Diversity, and Length

Response-level design determines how rollouts are generated, how diverse the response distribution stays during training, and how reasoning length is controlled.

Self-Play Response Verification and Transfer When the solver responds to a selfproposed task, there is no external oracle to confirm whether the reasoning chain is correct. What stopping criteria prevent the solver from being rewarded for incorrect reasoning that it produces with high confidence? Do the response strategies learned through self-play transfer to held-out real-world benchmarks, or does the self-play distribution drift away from genuine task requirements over time?

Response Diversity and Off-Policy Reuse As RL training progresses, the policy tends to converge toward a narrow set of high-reward response patterns, reducing the variety of outputs it generates. How can response diversity be maintained without sacrificing reward quality? How many times can responses generated by an old model be reused across gradient steps before the IS ratio ρ<sup>t</sup> in Eq. [2.1.1.1](#page-6-3) becomes too outdated to produce reliable gradient updates, and what threshold should trigger new rollout generation?

Reasoning Length and Efficiency Can the appropriate number of tokens for a given prompt be estimated before generation, so that the model can dynamically adjust its output length based on task difficulty? How can a gradient update rule that explicitly accounts for response length optimize for both conciseness and correctness without distorting the advantage signal?

# <span id="page-87-1"></span>8.4 Feedback: Supervision Quality and Evaluation

Feedback is the training signal, i.e., human labels, AI scores, or a mix of both that tells the policy which responses to reinforce during training. Evaluation is the check performed after training that measures whether the trained policy has actually improved. Although both operate on response quality, they fail in different ways. Feedback is collected during training: annotators and AI judges tend to prefer longer or better-formatted responses regardless of content, collapsing helpfulness, factual accuracy, safety, and style into one score that the policy can learn to game without genuinely improving. Evaluation is conducted after training: benchmark scores can rise while real utility falls, because a fixed benchmark does not adapt to the new failure modes that a more capable policy introduces.

Data Quality and Hybrid Supervision Pairwise comparisons and binary ratings mix helpfulness, factual accuracy, safety, and style into a single signal. In addition, verbosity and formatting alone can inflate preference scores independent of content quality. In hybrid human-AI supervision, what criteria should govern the allocation of scarce human labels versus AI feedback, and how should the judge be designed to resist shortcuts based on surface features such as length and formatting bias? As the policy improves during training, the judge's own training distribution becomes stale and how should this gradual loss of reliability <span id="page-88-2"></span>in the judge's scores be detected and corrected to keep the feedback signal reliable throughout training?

Evaluation Standardization and Principled Stopping Evaluation measures whether training produced a genuinely better model, but papers report incompatible metrics like win rates, benchmark accuracies, RLHF scores, making cross-method comparison unreliable. Iterative training also risks optimizing for the evaluation metric rather than genuine quality improvement: the policy improves on the evaluation metric without improving in deployment, because the metric does not capture all the ways a response can fail. What minimal set of evaluation dimensions like truthfulness, toxicity, over-refusal, instruction-following, calibration, jailbreak robustness is necessary and sufficient to detect the distinct failure modes of different alignment methods, and how should static benchmarks and adversarial tests be combined to cover failure modes that neither captures alone?

### <span id="page-88-0"></span>8.5 Reward: Models, Granularity, and Safety

Reward model design sets the performance ceiling of the whole pipeline.

Verifiable Rewards Beyond Math and Code All current RLVR systems rely on domains where correctness can be checked automatically by an automated tool such as a compiler or symbolic verifier, which is the main bottleneck preventing RLVR from scaling beyond math and code. How can reliable verifiable reward signals be constructed for tasks such as factual question answering, scientific reasoning, and long-form writing, where no such automated checker exists?

Reward Granularity and Process Supervision ORMs give a single reward for the full response; PRMs [\(Lightman et al., 2023\)](#page-102-1) give step-level supervision; and token-level credit methods (Beyond 80/20, Clip-Cov) assign weights at individual token positions. Do step-level or token-level rewards raise the performance ceiling, or do they only speed up convergence to the same endpoint as ORMs? Across this ORM → PRM → token-level spectrum, what granularity is optimal under a fixed compute budget, and should the granularity follow a training-stage schedule, i.e., starting with coarse whole-response rewards for stable early training and gradually shifting to finer step- or token-level rewards as the policy matures, and with what criterion triggering the transition?

### <span id="page-88-1"></span>8.6 Algorithm: Optimization and Pipeline Integration

Algorithmic questions concern how the policy update is formulated and how the SFT-to-RL pipeline is connected.

Offline-Online Convergence and Advanced Objectives Under what conditions does iterative offline DPO converge to the same policy as online RLVR? Do common training failure modes such as reward hacking (the model exploits loopholes in the reward), verbosity bias (the model produces unnecessarily long responses), and diversity collapse (the model stops exploring different response styles) become worse or better for Nash [\(Munos et al.,](#page-104-4) [2024\)](#page-104-4) and listwise [\(Liu et al., 2025c\)](#page-103-0) methods as scale increases beyond 70B, relative to PPO and DPO?

<span id="page-89-2"></span>SFT-RL Pipeline Integration Can joint SFT-RL objectives with a gradually adjusted balance between SFT and RL losses, as partially shown by HPT [\(Lv et al., 2025\)](#page-103-1) prevent the model from forgetting previously learned knowledge while keeping the exploration needed for effective RL?

# <span id="page-89-0"></span>8.7 Extensions: Frontiers Beyond Current Scope

The final cluster covers settings where the current pipeline does not directly apply: multimodal and agentic tasks, continual and cross-lingual training, and understanding why certain behaviors emerge during RL.

Multimodal and Agentic RLVR How should multi-turn GRPO be extended beyond single-response rollouts to handle tool calls, changing observations, and sparse rewards in complex tasks that require a long sequence of actions? What verifiable reward designs are robust to the agent learning to exploit weaknesses in the training environment?

Continual and Cross-Lingual Alignment Do RLVR reasoning gains transfer across languages in a positive direction (English RL improves multilingual math performance), a negative direction (English training introduces biases into non-English output), or does this depend on model scale and pretraining language balance?

Mechanistic Interpretability of RL Training During RLVR, models develop selfverification and reflection behaviors such as the "aha moment" in DeepSeek-R1-Zero, but it is not known which parts of the network produce them. Which attention heads and weight components are most responsible for these behaviors and change most during RL training, and can this knowledge be used to freeze the rest and reduce training cost?

# <span id="page-89-1"></span>9 Conclusion

This survey organizes LLM post-training from MLE through SFT, actor-critic RLHF and RLVR, and offline and iterative DPO under a single gradient coefficient framework. Every method reviewed is recovered by specifying a data source D including prompts and responses, a gradient coefficient GC(x, y, t) in Eq. [2.1.1.1.](#page-6-3) Within RLVR, the survey organizes existing methods along three axes. The first is prompt sampling (Section [3\)](#page-19-0), which covers both prompt generation: spanning human-annotated and synthetically generated data and prompt selection, including static curricula, adaptive difficulty curricula, and reward-based filtering. The second is response sampling (Section [4\)](#page-24-0), which is divided into response generation and response selection. Response generation encompasses on-policy rollouts, off-policy approaches via replay buffers and knowledge distillation, asynchronous multi-node training, prefixconditioned rollouts, and tree-structured rollouts. Response selection covers positive/negative filtering, reward-based filtering, advantage-based filtering, and bootstrapped selection. The third is gradient coefficient design (Section [5\)](#page-35-0), which the survey breaks down into five sub-axes: the importance sampling ratio (spanning token-level and sequence-level clipping through to IS-free objectives), advantage shaping (covering outcome rewards, length penalties, self-certainty rewards, process rewards, baseline and partition function estimation, advantage stability, and hybrid SFT–RL objectives), advantage normalization (beta, multi-objective, two-step, and normalization-free variants), length normalization (response-level, group-level,

and normalization-free), and regularization (KL penalty, entropy bonus, or none). For onpolicy methods with unverifiable rewards (Section [6\)](#page-63-0), the survey further discusses RLHF, RLAIF, iterative DPO, and Nash learning-based methods. For offline DPO (Section [7\)](#page-70-0), the survey covers four axes: response generation (pairwise, single, and list responses), reward (pairwise, token-level pairwise, pointwise, list, and negative reward), regularization (entropy, divergence, reference model, and length penalty), and merging with SFT, showing how each variant differs in data structure and gradient coefficient form. Seven open problems remain along the training pipeline: 1. foundations, 2. prompt, 3. response, 4. feedback, 5. reward, 6. algorithm and 7. extensions.

| Symbol                   | Definition                                                                                                                                                                                                                                                  |  |  |  |  |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|--|
|                          | Policies and Models                                                                                                                                                                                                                                         |  |  |  |  |
| πθ                       | The policy model (i.e. the LLM being aligned), parameterized by<br>θ.                                                                                                                                                                                       |  |  |  |  |
| πθold                    | The old (rollout) policy: a frozen snapshot of<br>πθ<br>used to sample<br>training responses. Refreshed after each update step in GRPO, or<br>after several steps in PPO.                                                                                   |  |  |  |  |
| πref                     | The frozen reference policy, typically the SFT checkpoint. Serves<br>as the KL anchor in RLHF, DPO, and GRPO objectives.                                                                                                                                    |  |  |  |  |
| πsft                     | The SFT policy, which is the initialisation point for RL-based<br>post-training. Responses are sampled from<br>πsft<br>in offline methods<br>such as RFT.                                                                                                   |  |  |  |  |
| πb                       | Behaviour / data-collection policy that originally generated off<br>policy responses (e.g. in RePO, TOPR, LUFFY, GVPO). Distinct<br>πθold:<br>πb<br>may be an entirely frozen external model rather than<br>from<br>a stale snapshot of the current policy. |  |  |  |  |
| ∗<br>π                   | The theoretically optimal policy: the closed-form maximiser of the<br>KL-regularised reward objective (used in DPO and IPO deriva<br>tions).                                                                                                                |  |  |  |  |
| t<br>π<br>mix            | Geometric mixture policy used in Nash-Mirror Descent (Nash-MD)                                                                                                                                                                                              |  |  |  |  |
| ′<br>π<br>θ              | Fixed sampling / comparison policy used in IPO and Nash learning<br>′<br>to draw contrast responses<br>y<br>; not optimised during training.                                                                                                                |  |  |  |  |
| ref, π−<br>+<br>π<br>ref | More-aligned (previous-iteration) and less-aligned (initial) reference<br>models used in D2O to anchor positive and negative gradients<br>respectively.                                                                                                     |  |  |  |  |
| θ                        | Trainable parameters of the policy model.                                                                                                                                                                                                                   |  |  |  |  |
| ϕ                        | Parameters of an auxiliary model, specifically the reward model<br>rϕ(x, y)<br>or the value network<br>Vϕ(x)<br>in DRO-V.                                                                                                                                   |  |  |  |  |
| Prompts and Responses    |                                                                                                                                                                                                                                                             |  |  |  |  |
| x                        | Input prompt / query given to the LLM.                                                                                                                                                                                                                      |  |  |  |  |

# List of Symbols

| Symbol                     | Definition                                                                                                                                                                                                                      |  |  |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| y                          | x.<br>Model response / output sequence generated for prompt                                                                                                                                                                     |  |  |
| t<br>y                     | The token generated at position<br>t<br>within response<br>y; equivalently<br>t<br>= (x, y <t)).<br>written<br/>at<br/>in the MDP notation (where<br/>at<br/>=<br/>y<br/>,<br/>st</t)).<br>                                     |  |  |
| <t<br>y</t<br>             | 1<br>, , yt−1<br>All tokens generated before position<br>t, i.e. the prefix<br>(y<br>).                                                                                                                                         |  |  |
| ∗<br>y                     | The ground-truth / correct reference response, used in the correct<br>I(y<br>∗<br>ness indicator<br>=<br>y<br>).                                                                                                                |  |  |
| yw                         | The preferred ("winning") response in a pairwise preference sample<br>(x, yw, yl).                                                                                                                                              |  |  |
| yl                         | The dispreferred ("losing") response in a pairwise preference sample.                                                                                                                                                           |  |  |
| ysft                       | A demonstration response drawn from the SFT dataset or model,<br>used as a supervised anchor in methods such as SLiC-HF that<br>combine a ranking objective with an SFT regularisation term.                                    |  |  |
| pre<br>y                   | Expert prefix:<br>a fixed prefix of length<br>L<br>from a reference trace,<br>prepended to on-policy rollouts to densify rewards in BREAD and<br>Prefix-RFT.                                                                    |  |  |
| y                          | Length of response<br>y<br>in tokens.                                                                                                                                                                                           |  |  |
| G                          | Number of response rollouts sampled per prompt in GRPO-family<br>methods.                                                                                                                                                       |  |  |
| µ                          | The mean reward across the<br>G<br>sampled responses for a given prompt<br>in GRPO-family methods.                                                                                                                              |  |  |
| σ                          | The standard deviation of the rewards across the<br>G<br>sampled re<br>sponses for a given prompt in GRPO-family methods.                                                                                                       |  |  |
| Datasets and Distributions |                                                                                                                                                                                                                                 |  |  |
| D                          | Training data / prompt distribution; the source from which<br>x<br>∼ D<br>is drawn during on-policy RL.                                                                                                                         |  |  |
| Dpre                       | Pretraining corpus; used in the MLE pretraining objective.                                                                                                                                                                      |  |  |
| Dsft                       | Supervised fine-tuning dataset of<br>(x, y)<br>demonstration pairs.                                                                                                                                                             |  |  |
| DRBR                       | Synthetic dataset<br>{(x, y1, y2, , yK)}<br>of ranked completions used<br>to fit the Rule-Based Reward (RBR) weights in RLAIF-OpenAI<br>(Eq. 6.2.2).                                                                            |  |  |
| B                          | Replay buffer storing previously generated off-policy responses<br>together with their log-probabilities under the behaviour policy<br>πb;<br>used in RePO to augment on-policy rollouts without additional<br>generation cost. |  |  |
| Rewards and Objectives     |                                                                                                                                                                                                                                 |  |  |
| r(x, y)                    | General scalar reward assigned to response<br>y<br>given prompt<br>x.                                                                                                                                                           |  |  |
| rϕ(x, y)                   | Explicit reward model with learned parameters<br>ϕ, trained from<br>human preference data via the Bradley–Terry objective.                                                                                                      |  |  |
| rθ(x, y)                   | πθ(y x)<br>Implicit reward expressed through the policy ratio:<br>β<br>log<br>πref (y x)                                                                                                                                        |  |  |

(continued from previous page)

(continued from previous page)

| Symbol                                   | Definition                                                                                                                                                           |
|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rt                                       | Per-step reward in the MDP formulation; equals<br>0<br>for all non                                                                                                   |
|                                          | terminal tokens under an Outcome Reward Model (ORM), and                                                                                                             |
| p                                        | equals<br>r(x, y)<br>only at the terminal step<br>t<br>=<br>T.                                                                                                       |
| t<br> x, y <t)<br>r<br/>(y<br/>θ</t)<br> | Implicit process reward at token<br>t<br>from the co-trained PRM in<br>t<br> x, y <t)< td=""></t)<>                                                                  |
|                                          | πθ(y<br>PRIME:<br>β<br>log<br>t<br> x, y <t)<br>πref(y</t)<br>                                                                                                       |
| o<br>r<br>(x, y)<br>ϕ                    | Outcome (verifiable) reward, e.g. binary correctness for math or<br>pass-rate for code (PRIME, PURE).                                                                |
| rrbr,<br>rRM,<br>rtot                    | Rule-based reward, reward-model score, and total combined reward                                                                                                     |
|                                          | in RLAIF-OpenAI (Eq. 6.2.1).                                                                                                                                         |
| rsc(x, y)                                | Self-certainty reward (INTUITOR): average KL divergence between                                                                                                      |
|                                          | the uniform vocabulary distribution and the policy's next-token                                                                                                      |
|                                          | distribution, measuring intrinsic model confidence without external                                                                                                  |
|                                          | labels.                                                                                                                                                              |
| rsolve,<br>rpropose                      | Solver and proposer rewards in Absolute Zero:<br>indicates<br>rsolve                                                                                                 |
|                                          | rpropose<br>task correctness while<br>rewards tasks of moderate difficulty<br>(Eq. 3.1.2.1).                                                                         |
| J(·)                                     | General policy objective function to be<br>maximized.                                                                                                                |
| L(·)                                     | Loss function to be<br>minimized, used for reward model training.                                                                                                    |
| Z(x)                                     | Partition function / normalization constant depending only on                                                                                                        |
|                                          | rθ(x,y)/β.<br>the prompt:<br>Z(x) =<br>P<br>πref(y x)e<br>Intractable to com<br>y<br>pute directly; cancelled in the DPO derivation by taking reward<br>differences. |
| GC(x, y, t)                              | t<br> x, y <t)<br>Gradient coefficient: the scalar multiplying<br/>∇θ<br/>log<br/>πθ(y<br/>in</t)<br>                                                                |
|                                          | the unified policy gradient (Eq. 2.1.1.1).<br>Different post-training<br>methods differ<br>only<br>in their choice of<br>GC.                                         |
| MDP Notation                             |                                                                                                                                                                      |
| st                                       | = (x, y <t).<br>MDP state at step<br/>t; in the LLM instantiation<br/>st</t).<br>                                                                                    |
| at                                       | t<br>MDP action at step<br>t; in the LLM instantiation<br>at<br>=<br>y                                                                                               |
| τ                                        | Full trajectory<br>τ<br>= (s1, a1, s2, a2, , sT<br>, aT<br>)<br>in general RL.                                                                                       |
| T                                        | Total number of tokens (episode horizon).                                                                                                                            |
| Gt                                       | ′−t<br>PT<br>t<br>Discounted return from step<br>t:<br>=<br>′.<br>With<br>= 1<br>Gt<br>γ<br>rt<br>γ<br>′=t<br>t                                                      |
|                                          | Gt<br>=<br>r(x, y)<br>t.<br>and ORM,<br>for all                                                                                                                      |
| Gmin<br>t                                | Min-form return in PURE: equals the minimum process reward<br>p                                                                                                      |
|                                          | r<br>for all steps up to and including the worst step<br>tw, and zero<br>tw                                                                                          |
|                                          | thereafter.                                                                                                                                                          |
| γ                                        | Discount factor (γ<br>∈<br>[0,<br>1]; set to<br>1<br>for LLM text generation).                                                                                       |
| Sterminal                                | Set of step-ending token positions in a response<br>y, used by the                                                                                                   |
|                                          | Process Reward Model (PRM) to determine which positions receive                                                                                                      |
|                                          | nonzero reward (Eq. 2.3.3).                                                                                                                                          |

### Wang, Ramnath, et al.

(continued from previous page)

| Symbol                                                                                                                                                                                                                                                             | Definition                                                                                                                                                                                                                                                                         |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                                                                                                                                    | Value Functions and Advantage Estimation                                                                                                                                                                                                                                           |
| π<br>V<br>(st)                                                                                                                                                                                                                                                     | State-value function: expected return from state<br>st<br>under policy<br>π.                                                                                                                                                                                                       |
| Qπ<br>(st<br>, at)                                                                                                                                                                                                                                                 | Action-value function: expected return after taking action<br>at<br>in                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                    | state<br>st<br>under policy<br>π.                                                                                                                                                                                                                                                  |
| Aπ<br>(st<br>, at)                                                                                                                                                                                                                                                 | Qπ<br>π<br>Advantage function:<br>(st<br>, at)<br>−<br>V<br>(st), measuring how much<br>better action<br>at<br>is relative to the average action in state<br>st                                                                                                                    |
| Vϕ                                                                                                                                                                                                                                                                 | Learned critic (value network) with parameters<br>ϕ, used in PPO<br>and PPO-based methods (VC-PPO, ORZ, VAPO).                                                                                                                                                                     |
| target<br>Vˆ<br>t                                                                                                                                                                                                                                                  | Value regression target for the critic:<br>either the MC return<br>Gt<br>(unbiased) or the TD target<br>rt<br>+<br>γVϕ−<br>(st+1)<br>(lower variance).                                                                                                                             |
| VˆMC(x, y <t)< td=""><td>Monte Carlo value estimate at token position<br/>t: the average outcome<br/>πθ(· x, y<t), in<br="" used="">reward over<br/>G<br/>continuations sampled from<br/>VinePPO as a drop-in replacement for the learned critic.</t),></td></t)<> | Monte Carlo value estimate at token position<br>t: the average outcome<br>πθ(· x, y <t), in<br="" used="">reward over<br/>G<br/>continuations sampled from<br/>VinePPO as a drop-in replacement for the learned critic.</t),>                                                      |
| AMC,t                                                                                                                                                                                                                                                              | VˆMC(x, y <t+1)<br>MC-based token-level advantage in VinePPO:<br/>−<br/>VˆMC(x, y<t), exploiting="" intermediate-reward="" of<br="" structure="" the="" zero="">language generation.</t),></t+1)<br>                                                                               |
| δt                                                                                                                                                                                                                                                                 | One-step TD residual:<br>δt<br>=<br>rt<br>+<br>γVϕ(st+1)<br>−<br>Vϕ(st); the building<br>block of GAE.                                                                                                                                                                             |
| λ                                                                                                                                                                                                                                                                  | GAE interpolation parameter:<br>λ<br>= 0<br>gives the one-step TD advan<br>tage;<br>λ<br>= 1<br>gives the full MC advantage.                                                                                                                                                       |
| GAE(γ,λ)<br>A<br>t                                                                                                                                                                                                                                                 | PT −t<br>l<br>Generalised Advantage Estimation:<br>l=0 (γλ)<br>δt+l<br>(Eq. 2.4.1.2).                                                                                                                                                                                              |
| AGRPO(x, yi)                                                                                                                                                                                                                                                       | GRPO group-normalized advantage.                                                                                                                                                                                                                                                   |
| ARLOO(x, yi)                                                                                                                                                                                                                                                       | REINFORCE leave-one-out advantage.                                                                                                                                                                                                                                                 |
| SE(x)                                                                                                                                                                                                                                                              | Semantic entropy of the response group for prompt<br>(SEED<br>x<br>GRPO): approximated by clustering<br>G<br>responses into semantic<br>equivalence classes and computing entropy over their pooled proba<br>bilities; used to scale down advantages for high-uncertainty prompts. |
|                                                                                                                                                                                                                                                                    | Importance Sampling and Clipping                                                                                                                                                                                                                                                   |
| ρi,t                                                                                                                                                                                                                                                               | Per-token importance sampling (IS) ratio for response<br>i<br>at token<br> x,y <t<br>t<br/>πθ(y<br/>)<br/>t:<br/>ρi,t<br/>=<br/>. Corrects for distribution shift when reusing<br/>i<br/>i<br/> x,y<t<br>t<br/>πθold(y<br/>)<br/>i<br/>i<br/>off-policy rollouts.</t<br></t<br>    |
| ρi                                                                                                                                                                                                                                                                 | Sequence-level IS ratio for response<br>i, aggregating token-level ra                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                    | tios into a single per-response weight. In GSPO it is the length                                                                                                                                                                                                                   |
|                                                                                                                                                                                                                                                                    | 1/ yi <br><br>πθ(yi<br> x)<br>normalised geometric mean<br>ρi<br>=<br>; in GEPO it is<br>πθold(yi<br> x)                                                                                                                                                                           |
|                                                                                                                                                                                                                                                                    | GEPO<br>the group-expectation-normalised ratio<br>ρ<br>(Eq. 4.1.4.2).<br>i                                                                                                                                                                                                         |
| ρˆi,t                                                                                                                                                                                                                                                              | Clipped<br>IS<br>ratio<br>with<br>stop-gradient<br>applied<br>(CISPO):<br>ρˆi,t<br>=                                                                                                                                                                                               |
|                                                                                                                                                                                                                                                                    | clip(ρi,t,<br>1<br>−<br>εlow,<br>1 +<br>εhigh), treated as a constant during differ<br>entiation so the gradient never zeroes out from clipping.                                                                                                                                   |

| Symbol                                                                                                                                                                        | Definition                                                                                                                                                                                                                                                                          |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ct<br>,<br>ci,t                                                                                                                                                               | PPO/GRPO clipping indicator: equals<br>ρt<br>exceeds the trust<br>0<br>when<br>[1−ε,<br>1+ε]<br>in the direction favored by the advantage (zeroing<br>region<br>the gradient), and<br>1<br>otherwise (Eq. 2.4.2.5).                                                                 |
| ci                                                                                                                                                                            | Sequence-level clipping indicator (GSPO): same binary form as<br>ci,t<br>but computed from the sequence-level ratio<br>ρi<br>and advantage<br>Ai<br>,<br>clipping the entire response at once rather than per token.                                                                |
| ε                                                                                                                                                                             | Symmetric PPO/GRPO clipping range; the IS ratio is clipped to<br>−<br>[1<br>ε,<br>1 +<br>ε].                                                                                                                                                                                        |
| εlow, εhigh                                                                                                                                                                   | Asymmetric clipping bounds used by DAPO, OLMo 3, Magistral,<br>VAPO, and CISPO (εhigh<br>permits larger updates on high<br>> εlow<br>advantage tokens).                                                                                                                             |
| εKL                                                                                                                                                                           | Maximum allowable KL divergence per update step in TRPO's<br>hard trust-region constraint (Eq. 2.4.2.1); approximated by clipping<br>in PPO.                                                                                                                                        |
|                                                                                                                                                                               | KL Divergence, Entropy, and Regularisation                                                                                                                                                                                                                                          |
| ′<br>DKL(π∥π<br>)                                                                                                                                                             | ′<br>KL<br>divergence<br>from<br>distribution<br>π<br>to<br>π<br>The<br>reverse<br>KL<br>DKL(πθ∥πref)<br>is zero-forcing and prevents reward hacking.                                                                                                                               |
| DSeqKL(x, y;<br>π1∥π2)                                                                                                                                                        | Sequential (token-level cumulative) KL divergence used in TDPO:<br>PT<br>t=1 DKL(π1(· x, y <t)∥π2(· x, cancellation="" enabling="" of="" per<br="" y<t)),="">step partition functions in the BT model (Eq. 7.2.2.8).</t)∥π2(· x,>                                                   |
| (i,t)<br>D<br>KL                                                                                                                                                              | Schulman unbiased KL estimator for<br>KL(πθ∥πref)<br>at token<br>(i, t):<br>πref<br>πref<br>−<br>log<br>−<br>1<br>≥<br>0<br>(used in the GRPO objective, Eq. 2.5.1.1).<br>πθ<br>πθ                                                                                                  |
| β                                                                                                                                                                             | KL<br>regularisation<br>coefficient<br>controlling<br>deviation<br>from<br>πref<br>(Eq. 2.1.1); also scales the implicit reward in DPO.                                                                                                                                             |
| H(πθ(· x, y <t))< th=""><th>Shannon entropy of the policy's next-token distribution at context<br/>(x, y<t):<br>−<br/>P<br/>j∈V πθ(j ·) log<br/>πθ(j ·).</t):<br></th></t))<> | Shannon entropy of the policy's next-token distribution at context<br>(x, y <t):<br>−<br/>P<br/>j∈V πθ(j ·) log<br/>πθ(j ·).</t):<br>                                                                                                                                               |
| V                                                                                                                                                                             | Vocabulary of the language model.                                                                                                                                                                                                                                                   |
| Preference Learning                                                                                                                                                           |                                                                                                                                                                                                                                                                                     |
| σ(·)                                                                                                                                                                          | −z<br>Sigmoid (logistic) function:<br>σ(z) = 1/(1+e<br>), used in the Bradley–<br>Terry pairwise preference model<br>P(yw<br>> yl<br> x) =<br>σ(rϕ(x, yw)<br>−<br>rϕ(x, yl)).                                                                                                       |
| P(yw<br>> yl<br> x)                                                                                                                                                           | Pairwise preference probability under the Bradley–Terry model:<br>probability that response<br>yw<br>is preferred over<br>yl<br>given prompt<br>x.                                                                                                                                  |
| z0                                                                                                                                                                            | Ex∼D[DKL(πθ(· x)∥πref(· x))]<br>KTO reference point:<br>β<br>(Eq. 7.1.2.2).                                                                                                                                                                                                         |
| zθ                                                                                                                                                                            | Implicit pairwise reward difference under the current policy (RPO,<br>h<br>i<br>πθ(yw x)<br>πθ(yl<br> x)<br>πref (yw x) −<br>β-DPO):<br>zθ<br>=<br>β<br>log<br>log<br>; compared against an<br>πref (yl<br> x)<br>explicit reward difference to calibrate the gradient coefficient. |

(continued from previous page)

| Symbol                        | Definition                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| uθ,<br>δθ                     | TDPO decomposition of the response-level reward difference:<br>uθ<br>collects per-token log-ratios and<br>δθ<br>captures the difference in se<br>quential forward KL divergences between preferred and dispreferred<br>responses; together they replace the untractable partition-function                                                                                                                                   |
| λD, λU                        | terms (Eq. 7.2.2.9).<br>KTO loss weights for desirable and undesirable examples, respec<br>tively.                                                                                                                                                                                                                                                                                                                           |
| δm                            | Margin hyperparameter in SLiC-HF's max-margin ranking objec<br>tive: the minimum required log-probability gap between the pre<br>ferred and dispreferred responses before the ranking loss activates<br>(Eq. 7.1.1.1).                                                                                                                                                                                                       |
| λsft                          | SFT regularisation weight in SLiC-HF and related methods: scales<br>the supervised term that anchors the policy to demonstration<br>responses, preventing drift from the initial SFT model.                                                                                                                                                                                                                                  |
| λpos                          | DPOP penalty weight:<br>scales the hinge term that prevents the<br>preferred response<br>yw<br>from becoming less likely than under<br>πref,<br>directly addressing the likelihood-degradation failure mode of DPO<br>(Eq. 7.1.1.3).                                                                                                                                                                                         |
| (·)<br>τ<br>D(·)              | Rank position function:<br>(si)<br>is the rank of response<br>in the<br>τ<br>yi<br>permutation induced by scores<br>s<br>(used in LiPO's rank discount).<br>Rank discount function:<br>D(τ<br>(si)) = log(1 +<br>τ<br>(si))<br>(LiPO).                                                                                                                                                                                       |
| ∆i,j                          | Lambda weight in LiPO combining gain and rank-discount differ<br>1<br>1<br> Gi<br>−<br>  <br>D(τ(i)) −<br>D(τ(j))  .<br>ences:<br>Gj                                                                                                                                                                                                                                                                                         |
| ϕi(x, y)<br>wi                | (i) Binary proposition feature in RLAIF-OpenAI's Rule-Based Re<br>i-th proposition<br>ward (RBR): a binary classification output for the<br>given prompt<br>x<br>and response<br>y. (ii) Human-labelled reward / rank<br>ing score used in RRHF and LiPO to define the preference ordering<br>over multiple candidate responses.<br>Weight<br>for<br>feature<br>ϕi<br>in<br>the<br>RBR<br>reward:<br>rrbr(x, y, w)<br>=<br>N |
|                               | P<br>i=1 wiϕi(x, y).<br>Nash and Self-Play Methods                                                                                                                                                                                                                                                                                                                                                                           |
| ′<br>P(πθ<br>≻<br>π<br>)<br>θ | Policy-level preference probability in Nash learning: expected prob<br>′<br>ability that a response from<br>πθ<br>is preferred over one from<br>π<br>,<br>θ<br>averaged over prompts<br>x<br>∼ D<br>(Eq. 6.4.1). Replaces the scalar BT<br>reward and supports non-transitive preferences.                                                                                                                                   |
| αt                            | Learning rate at iteration<br>t<br>in Nash-MD; controls the interpolation<br>t<br>weight of the regularised mixture policy<br>π<br>mix between the current<br>t and the reference<br>π<br>πref.<br>iterate                                                                                                                                                                                                                   |

(continued from previous page)

(continued on next page)

96

Adaptive Curriculum and Prompt Selection

| (continued from previous page) |  |
|--------------------------------|--|
|--------------------------------|--|

| Symbol          | Definition                                                                                                                                                                                                                           |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| d               | Prompt difficulty score in AdaRFT:<br>d<br>= 100×(1−r¯ref(x, y)), where<br>r¯ref<br>is the average reward of a reference LLM on the prompt; higher<br>d<br>indicates harder prompts.                                                 |
| dT              | Global target difficulty in AdaRFT: updated online based on the<br>current policy's batch-average reward to keep the training success<br>∗<br>rate near<br>p<br>(Eq. 3.2.2.1).                                                       |
| ∗<br>p          | Target reward threshold in AdaRFT: the desired batch-average<br>∗ ≈0.5<br>p<br>success rate (motivated as<br>for binary rewards to maximise<br>gradient signal).                                                                     |
| Hyperparameters |                                                                                                                                                                                                                                      |
| α               | A<br>multipurpose<br>scaling<br>hyperparameter;<br>its<br>role<br>changes<br>per<br>method.                                                                                                                                          |
| αlen            | Length penalty coefficient:<br>scales the length deviation term in<br>length-aware reward functions (LCPO, GRPO-λ, GRPO-LEAD)                                                                                                        |
| ∗<br>n          | to trade off response correctness against verbosity.<br>User-specified token budget appended to each prompt in LCPO;<br>∗<br>the length-aware reward penalises deviations from<br>n<br>to enforce<br>inference-time compute control. |
| κ               | u<br>Policy-shaping constant in LUFFY:<br>f(u) =<br>(with<br>= 0.1);<br>κ<br>u+κ<br>amplifies gradients for low-probability tokens from off-policy traces<br>to prevent entropy collapse.                                            |
| λent            | Entropy bonus weight in GFPO: scales the entropy regularisation<br>λentH(πθ)<br>added to the GRPO objective to prevent premature<br>term<br>policy collapse (Eq. 4.2.2.2).                                                           |
| ηneg            | Negative-sample penalty coefficient in OREAL: balances the contri<br>bution of the token-weighted negative term relative to the positive<br>BC term (Eq. 5.1.1.8).                                                                   |
| β0              | Initial (base) KL coefficient in<br>β-DPO; serves as the starting value<br>before batch-level dynamic calibration adjusts it to<br>βbatch.                                                                                           |
| βbatch          | Batch-level dynamic KL coefficient in<br>β-DPO: adjusted per batch<br>based on the average reward discrepancy<br>Mi<br>relative to a running<br>M0<br>threshold<br>(Eq. 7.1.1.4).                                                    |
| αβ              | Sensitivity scaling factor in<br>β-DPO: controls how aggressively<br>βbatch<br>responds to deviations of the average reward discrepancy<br>Mi<br>from<br>the threshold<br>M0.                                                        |

### References

<span id="page-96-0"></span>L. Adolphs, T. Gao, J. Xu, K. Shuster, S. Sukhbaatar, and J. Weston. The CRINGE loss: Learning what language not to model. In A. Rogers, J. Boyd-Graber, and N. Okazaki, editors, Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8854–8874, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.493. URL <https://aclanthology.org/2023.acl-long.493/>. (Cited on page [69.](#page-68-1))

- <span id="page-97-4"></span>S. Agarwal, Z. Zhang, L. Yuan, J. Han, and H. Peng. The unreasonable effectiveness of entropy minimization in llm reasoning. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=UfFTBEsLgI>. (Cited on pages [44,](#page-43-4) [60,](#page-59-1) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-97-3"></span>P. Aggarwal and S. Welleck. L1: Controlling how long a reasoning model thinks with reinforcement learning. arXiv preprint arXiv:2503.04697, 2025. URL [https://arxiv.](https://arxiv.org/abs/2503.04697) [org/abs/2503.04697](https://arxiv.org/abs/2503.04697). (Cited on pages [42,](#page-41-4) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-97-2"></span>A. Ahmadian, C. Cremer, M. Gallé, M. Fadaee, J. Kreutzer, O. Pietquin, A. Üstün, and S. Hooker. Back to basics: Revisiting REINFORCE-style optimization for learning from human feedback in LLMs. In L.-W. Ku, A. Martins, and V. Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12248–12267, Bangkok, Thailand, Aug. 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.662. URL [https://aclanthology.org/2024.](https://aclanthology.org/2024.acl-long.662/) [acl-long.662/](https://aclanthology.org/2024.acl-long.662/). (Cited on page [17.](#page-16-3))
- <span id="page-97-1"></span>Anthropic. The claude 3 model family: Opus, sonnet, haiku. Claude-3 Model Card, 1, 2024. (Cited on page [4.](#page-3-5))
- <span id="page-97-6"></span>M. G. Azar, Z. Daniel Guo, B. Piot, R. Munos, M. Rowland, M. Valko, and D. Calandriello. A general theoretical paradigm to understand learning from human preferences. In S. Dasgupta, S. Mandt, and Y. Li, editors, Proceedings of The 27th International Conference on Artificial Intelligence and Statistics, volume 238 of Proceedings of Machine Learning Research, pages 4447–4455. PMLR, 02–04 May 2024. URL [https://proceedings.mlr.](https://proceedings.mlr.press/v238/gheshlaghi-azar24a.html) [press/v238/gheshlaghi-azar24a.html](https://proceedings.mlr.press/v238/gheshlaghi-azar24a.html). (Cited on pages [74,](#page-73-0) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-97-0"></span>Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, N. Joseph, S. Kadavath, J. Kernion, T. Conerly, S. El-Showk, N. Elhage, Z. Hatfield-Dodds, D. Hernandez, T. Hume, S. Johnston, S. Kravec, L. Lovitt, N. Nanda, C. Olsson, D. Amodei, T. Brown, J. Clark, S. McCandlish, C. Olah, B. Mann, and J. Kaplan. Training a helpful and harmless assistant with reinforcement learning from human feedback, 2022a. (Cited on pages [4,](#page-3-5) [14,](#page-13-0) and [65.](#page-64-3))
- <span id="page-97-5"></span>Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, C. Chen, C. Olsson, C. Olah, D. Hernandez, D. Drain, D. Ganguli, D. Li, E. Tran-Johnson, E. Perez, J. Kerr, J. Mueller, J. Ladish, J. Landau, K. Ndousse, K. Lukosuite, L. Lovitt, M. Sellitto, N. Elhage, N. Schiefer, N. Mercado, N. DasSarma, R. Lasenby, R. Larson, S. Ringer, S. Johnston, S. Kravec, S. E. Showk, S. Fort, T. Lanham, T. Telleen-Lawton, T. Conerly, T. Henighan, T. Hume, S. R. Bowman, Z. Hatfield-Dodds, B. Mann, D. Amodei, N. Joseph, S. McCandlish, T. Brown, and J. Kaplan. Constitutional ai: Harmlessness from ai feedback, 2022b. (Cited on pages [65,](#page-64-3) [66,](#page-65-0) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-98-8"></span>Q. Bertrand, W. M. Czarnecki, and G. Gidel. On the limitations of the elo, real-world games are transitive, not additive. In F. Ruiz, J. Dy, and J.-W. van de Meent, editors, Proceedings of The 26th International Conference on Artificial Intelligence and Statistics, volume 206 of Proceedings of Machine Learning Research, pages 2905–2921. PMLR, 25–27 Apr 2023. URL <https://proceedings.mlr.press/v206/bertrand23a.html>. (Cited on page [69.](#page-68-1))
- <span id="page-98-2"></span>R. A. Bradley and M. E. Terry. Rank analysis of incomplete block designs: I. the method of paired comparisons. Biometrika, 39:324, 1952. URL [https://api.semanticscholar.](https://api.semanticscholar.org/CorpusID:125209808) [org/CorpusID:125209808](https://api.semanticscholar.org/CorpusID:125209808). (Cited on page [13.](#page-12-5))
- <span id="page-98-0"></span>T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models are few-shot learners, 2020. (Cited on page [4.](#page-3-5))
- <span id="page-98-3"></span>M. Chen, G. Chen, W. Wang, and Y. Yang. SEED-GRPO: Semantic entropy enhanced GRPO for uncertainty-aware policy optimization. arXiv preprint arXiv:2505.12346, 2025. URL <https://arxiv.org/abs/2505.12346>. (Cited on pages [39,](#page-38-3) [45,](#page-44-2) [60,](#page-59-1) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-98-7"></span>D. Cheng, S. Huang, X. Zhu, B. Dai, W. X. Zhao, Z. Zhang, and F. Wei. Reasoning with exploration: An entropy perspective. arXiv preprint arXiv:2506.14758, 2025a. URL <https://arxiv.org/abs/2506.14758>. (Cited on pages [59,](#page-58-3) [61,](#page-60-3) [62,](#page-61-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-98-6"></span>J. Cheng, G. Xiong, R. Qiao, L. Li, C. Guo, J. Wang, Y. Lv, and F.-Y. Wang. Stop summation: Min-form credit assignment is all process reward model needs for reasoning. In Advances in Neural Information Processing Systems (NeurIPS), 2025b. (Cited on pages [47,](#page-46-4) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-98-1"></span>P. F. Christiano, J. Leike, T. B. Brown, M. Martic, S. Legg, and D. Amodei. Deep reinforcement learning from human preferences. Advances in Neural Information Processing Systems, 2017. (Cited on pages [4](#page-3-5) and [13.](#page-12-5))
- <span id="page-98-4"></span>X. Chu, H. Huang, X. Zhang, F. Wei, and Y. Wang. Gpg: A simple and strong reinforcement learning baseline for model reasoning. In The Fourteenth International Conference on Learning Representations, ICLR 2026, 2026. URL [https://openreview.net/forum?id=](https://openreview.net/forum?id=inccdtfx8x) [inccdtfx8x](https://openreview.net/forum?id=inccdtfx8x). (Cited on pages [41,](#page-40-3) [58,](#page-57-2) [59,](#page-58-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-98-9"></span>P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord. Think you have solved question answering? try arc, the ai2 reasoning challenge. arXiv:1803.05457v1, 2018. (Cited on page [73.](#page-72-1))
- <span id="page-98-5"></span>G. Cui, L. Yuan, Z. Wang, H. Wang, Y. Zhang, J. Chen, W. Li, B. He, Y. Fan, T. Yu, Q. Xu, W. Chen, J. Yuan, H. Chen, K. Zhang, X. Lv, S. Wang, Y. Yao, X. Han, H. Peng, Y. Cheng, Z. Liu, M. Sun, B. Zhou, and N. Ding. Process reinforcement through implicit rewards. arXiv preprint arXiv:2502.01456, 2025a. doi: 10.48550/arXiv.2502.01456. URL <https://arxiv.org/abs/2502.01456>. (Cited on pages [47,](#page-46-4) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-99-4"></span>G. Cui, Y. Zhang, J. Chen, L. Yuan, Z. Wang, Y. Zuo, H. Li, Y. Fan, H. Chen, W. Chen, Z. Liu, H. Peng, L. Bai, W. Ouyang, Y. Cheng, B. Zhou, and N. Ding. The entropy mechanism of reinforcement learning for reasoning language models. arXiv preprint arXiv:2505.22617, 2025b. URL <https://arxiv.org/abs/2505.22617>. (Cited on pages [38,](#page-37-6) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-99-5"></span>M. Dai, S. Liu, and Q. Si. Stable reinforcement learning for efficient reasoning. arXiv preprint arXiv:2505.18086, 2025a. URL <https://arxiv.org/abs/2505.18086>. (Cited on pages [42,](#page-41-4) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-99-3"></span>M. Dai, C. Yang, and Q. Si. S-GRPO: Early exit via reinforcement learning in reasoning models. In Advances in Neural Information Processing Systems, 2025b. URL [https:](https://openreview.net/forum?id=wNMK5o0Vfg) [//openreview.net/forum?id=wNMK5o0Vfg](https://openreview.net/forum?id=wNMK5o0Vfg). (Cited on pages [33,](#page-32-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-99-1"></span>H. Dong, W. Xiong, D. Goyal, Y. Zhang, W. Chow, R. Pan, S. Diao, J. Zhang, K. Shum, and T. Zhang. Raft: Reward ranked finetuning for generative foundation model alignment, 2023. URL <https://arxiv.org/abs/2304.06767>. (Cited on page [8.](#page-7-7))
- <span id="page-99-9"></span>S. Duan, X. Yi, P. Zhang, Y. Liu, Z. Liu, T. Lu, X. Xie, and N. Gu. Negating negatives: Alignment with human negative samples via distributional dispreference optimization. In Y. Al-Onaizan, M. Bansal, and Y.-N. Chen, editors, Findings of the Association for Computational Linguistics: EMNLP 2024, pages 1012–1042, Miami, Florida, USA, Nov. 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.findings-emnlp.56. URL <https://aclanthology.org/2024.findings-emnlp.56/>. (Cited on pages [81,](#page-80-0) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-99-7"></span>K. Ethayarajh, W. Xu, N. Muennighoff, D. Jurafsky, and D. Kiela. Kto: Model alignment as prospect theoretic optimization, 2024a. (Cited on pages [75,](#page-74-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-99-8"></span>K. Ethayarajh, W. Xu, N. Muennighoff, D. Jurafsky, and D. Kiela. Model alignment as prospect theoretic optimization. In Proceedings of the 41st International Conference on Machine Learning, ICML'24. JMLR.org, 2024b. (Cited on pages [75,](#page-74-2) [77,](#page-76-3) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-99-6"></span>Y. Freund and R. E. Schapire. Adaptive game playing using multiplicative weights. Games and Economic Behavior, 29:79–103, 1999. URL [https://api.semanticscholar.org/](https://api.semanticscholar.org/CorpusID:15295656) [CorpusID:15295656](https://api.semanticscholar.org/CorpusID:15295656). (Cited on page [70.](#page-69-4))
- <span id="page-99-2"></span>Y. Fu, T. Chen, J. Chai, X. Wang, S. Tu, G. Yin, W. Lin, Q. Zhang, Y. Zhu, and D. Zhao. Srft: A single-stage method with supervised and reinforcement fine-tuning for reasoning. arXiv preprint arXiv:2506.19767, 2025. URL <https://arxiv.org/abs/2506.19767>. (Cited on pages [30,](#page-29-3) [54,](#page-53-3) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-99-0"></span>B. Gao, F. Song, Y. Miao, Z. Cai, Z. Yang, L. Chen, H. Hu, R. Xu, Q. Dong, C. Zheng, S. Quan, W. Xiao, G. Zhang, D. Zan, K. Lu, B. Yu, D. Liu, Z. Cui, J. Yang, L. Sha, H. Wang, Z. Sui, P. Wang, T. Liu, and B. Chang. Towards a unified view of preference learning for large language models: A survey, 2024. URL <https://arxiv.org/abs/2409.02795>. (Cited on page [4.](#page-3-5))

- <span id="page-100-4"></span>C. Gao, C. Zheng, X.-H. Chen, K. Dang, S. Liu, B. Yu, A. Yang, S. Bai, J. Zhou, and J. Lin. Soft adaptive policy optimization. arXiv preprint arXiv:2511.20347, 2025. URL <https://arxiv.org/abs/2511.20347>. (Cited on pages [37,](#page-36-1) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-100-0"></span>Gemini. Gemini: A family of highly capable multimodal models, 2025. URL [https:](https://arxiv.org/abs/2312.11805) [//arxiv.org/abs/2312.11805](https://arxiv.org/abs/2312.11805). (Cited on page [4.](#page-3-5))
- <span id="page-100-2"></span>M. Ghasemi, A. H. Moosavi, and D. Ebrahimi. A comprehensive survey of reinforcement learning: From algorithms to practical challenges, 2025. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2411.18892) [2411.18892](https://arxiv.org/abs/2411.18892). (Cited on page [4.](#page-3-5))
- <span id="page-100-1"></span>D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Xu, H. Ding, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Chen, J. Yuan, J. Tu, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. You, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Zhou, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. Nature, 645(8081):633–638, Sept. 2025. ISSN 1476-4687. doi: 10.1038/s41586-025-09422-z. URL <http://dx.doi.org/10.1038/s41586-025-09422-z>. (Cited on pages [4](#page-3-5) and [17.](#page-16-3))
- <span id="page-100-5"></span>Y. Hao, L. Dong, X. Wu, S. Huang, Z. Chi, and F. Wei. On-policy RL with optimal reward baseline. arXiv preprint arXiv:2505.23585, 2025. (Cited on pages [41,](#page-40-3) [50,](#page-49-3) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-100-3"></span>J. He, J. Liu, C. Y. Liu, R. Yan, C. Wang, P. Cheng, X. Zhang, F. Zhang, J. Xu, W. Shen, S. Li, L. Zeng, T. Wei, C. Cheng, B. An, Y. Liu, and Y. Zhou. Skywork open reasoner 1 technical report. arXiv preprint arXiv:2505.22312, 2025. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2505.22312) [2505.22312](https://arxiv.org/abs/2505.22312). (Cited on pages [25,](#page-24-2) [59,](#page-58-3) [61,](#page-60-3) [62,](#page-61-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-100-6"></span>J. Hong, N. Lee, and J. Thorne. ORPO: Monolithic preference optimization without reference model. In Y. Al-Onaizan, M. Bansal, and Y.-N. Chen, editors, Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages 11170– 11189, Miami, Florida, USA, Nov. 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.626. URL [https://aclanthology.org/2024.emnlp-main.](https://aclanthology.org/2024.emnlp-main.626/) [626/](https://aclanthology.org/2024.emnlp-main.626/). (Cited on pages [85,](#page-84-2) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-101-8"></span>J. Hu, J. K. Liu, H. Xu, and W. Shen. REINFORCE++: A simple and efficient approach for aligning large language models. arXiv preprint arXiv:2501.03262, 2025a. doi: 10.48550/ arXiv.2501.03262. URL <https://arxiv.org/abs/2501.03262>. (Cited on pages [55,](#page-54-2) [57,](#page-56-5) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-101-6"></span>J. Hu, Y. Zhang, Q. Han, D. Jiang, X. Zhang, and H.-Y. Shum. Open-reasoner-zero: An open source approach to scaling up reinforcement learning on the base model. In Advances in Neural Information Processing Systems, 2025b. URL [https://openreview.net/forum?](https://openreview.net/forum?id=NFM8F5cV0V) [id=NFM8F5cV0V](https://openreview.net/forum?id=NFM8F5cV0V). (Cited on pages [36,](#page-35-4) [49,](#page-48-3) [57,](#page-56-5) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-101-4"></span>Z. Huang, T. Cheng, Z. Qiu, Z. Wang, Y. Xu, E. M. Ponti, and I. Titov. Blending supervised and reinforcement fine-tuning with prefix sampling. arXiv preprint arXiv:2507.01679, 2025. URL <https://arxiv.org/abs/2507.01679>. (Cited on pages [28,](#page-27-3) [31,](#page-30-2) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-101-5"></span>A. Kazemnejad, M. Aghajohari, E. Portelance, A. Sordoni, S. Reddy, A. Courville, and N. L. Roux. Vineppo: refining credit assignment in rl training of llms. In Proceedings of the 42nd International Conference on Machine Learning, ICML'25. JMLR.org, 2025. (Cited on pages [32,](#page-31-3) [57,](#page-56-5) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-101-2"></span>D. Khatri, L. Madaan, R. Tiwari, R. Bansal, S. S. Duvvuri, M. Zaheer, I. S. Dhillon, D. Brandfonbrener, and R. Agarwal. The art of scaling reinforcement learning compute for llms. In The Fourteenth International Conference on Learning Representations, ICLR 2026, 2026. URL <https://openreview.net/forum?id=FMjeC9Msws>. (Cited on pages [19,](#page-18-4) [23,](#page-22-3) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-101-10"></span>D. Kim, Y. Kim, W. Song, H. Kim, Y. Kim, S. Kim, and C. Park. sDPO: Don't use your data all at once. In O. Rambow, L. Wanner, M. Apidianaki, H. Al-Khalifa, B. D. Eugenio, S. Schockaert, K. Darwish, and A. Agarwal, editors, Proceedings of the 31st International Conference on Computational Linguistics: Industry Track, pages 366–373, Abu Dhabi, UAE, Jan. 2025. Association for Computational Linguistics. URL [https:](https://aclanthology.org/2025.coling-industry.31/) [//aclanthology.org/2025.coling-industry.31/](https://aclanthology.org/2025.coling-industry.31/). (Cited on pages [73,](#page-72-1) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-101-7"></span>Kimi Team. Kimi k1.5: Scaling reinforcement learning with LLMs. arXiv preprint arXiv:2501.12599, 2025. (Cited on pages [51,](#page-50-5) [60,](#page-59-1) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-101-0"></span>V. Konda and J. Tsitsiklis. Actor-critic algorithms. Advances in Neural Information Processing Systems, 12, 1999. (Cited on page [11.](#page-10-3))
- <span id="page-101-1"></span>W. Kool, H. van Hoof, and M. Welling. Buy 4 REINFORCE samples, get a baseline for free!, 2019. URL <https://openreview.net/forum?id=r1lgTGL5DE>. (Cited on page [17.](#page-16-3))
- <span id="page-101-9"></span>H. Lee, S. Phatale, H. Mansoor, T. Mesnard, J. Ferret, K. Lu, C. Bishop, E. Hall, V. Carbune, A. Rastogi, and S. Prakash. Rlaif vs. rlhf: scaling reinforcement learning from human feedback with ai feedback. In Proceedings of the 41st International Conference on Machine Learning, ICML'24. JMLR.org, 2024. (Cited on pages [66,](#page-65-0) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-101-3"></span>S. Li, Z. Zhou, W. Lam, C. Yang, and C. Lu. RePO: Replay-enhanced policy optimization. arXiv preprint arXiv:2506.09340, 2025a. (Cited on pages [27,](#page-26-1) [116,](#page-115-0) and [121.](#page-120-0))

- <span id="page-102-5"></span>Y. Li, Q. Gu, Z. Wen, Z. Li, T. Xing, S. Guo, T. Zheng, X. Zhou, X. Qu, W. Zhou, Z. Zhang, W. Shen, Q. Liu, C. Lin, J. Yang, G. Zhang, and W. Huang. TreePO: Bridging the gap of policy optimization and efficacy and inference efficiency with heuristic tree-based modeling. arXiv preprint arXiv:2508.17445, 2025b. URL [https://arxiv.org/abs/2508.](https://arxiv.org/abs/2508.17445) [17445](https://arxiv.org/abs/2508.17445). (Cited on pages [31,](#page-30-2) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-102-1"></span>H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe. Let's verify step by step, 2023. URL [https://arxiv.org/](https://arxiv.org/abs/2305.20050) [abs/2305.20050](https://arxiv.org/abs/2305.20050). (Cited on pages [10](#page-9-2) and [89.](#page-88-2))
- <span id="page-102-2"></span>C.-Y. Lin. Rouge: A package for automatic evaluation of summaries. In Text summarization branches out, pages 74–81. Association for Computational Linguistics, 2004. URL [https:](https://aclanthology.org/W04-1013/) [//aclanthology.org/W04-1013/](https://aclanthology.org/W04-1013/). (Cited on page [13.](#page-12-5))
- <span id="page-102-3"></span>S. Lin, J. Hilton, and O. Evans. TruthfulQA: Measuring how models mimic human falsehoods. In S. Muresan, P. Nakov, and A. Villavicencio, editors, Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3214–3252, Dublin, Ireland, May 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.229. URL <https://aclanthology.org/2022.acl-long.229/>. (Cited on page [14.](#page-13-0))
- <span id="page-102-4"></span>Z. Lin, M. Lin, Y. Xie, and R. Ji. CPPO: Accelerating the training of group relative policy optimization-based reasoning models. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=SVHerutWxp>. (Cited on pages [25,](#page-24-2) [35,](#page-34-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-102-7"></span>M. Liu, S. Diao, X. Lu, J. Hu, X. Dong, Y. Choi, J. Kautz, and Y. Dong. ProRL: Prolonged reinforcement learning expands reasoning boundaries in large language models. arXiv preprint arXiv:2505.24864, 2025a. URL <https://arxiv.org/abs/2505.24864>. (Cited on pages [61,](#page-60-3) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-102-0"></span>S. Liu, W. Fang, Z. Hu, J. Zhang, Y. Zhou, K. Zhang, R. Tu, T.-E. Lin, F. Huang, M. Song, Y. Li, and D. Tao. A survey of direct preference optimization, 2025b. URL <https://arxiv.org/abs/2503.11701>. (Cited on page [4.](#page-3-5))
- <span id="page-102-6"></span>S.-Y. Liu, X. Dong, X. Lu, S. Diao, P. Belcak, M. Liu, M.-H. Chen, H. Yin, Y.-C. F. Wang, K.-T. Cheng, Y. Choi, J. Kautz, and P. Molchanov. GDPO: Group reward-decoupled normalization policy optimization for multi-reward RL optimization. arXiv preprint arXiv:2601.05242, 2026a. URL <https://arxiv.org/abs/2601.05242>. (Cited on pages [55,](#page-54-2) [56,](#page-55-5) [57,](#page-56-5) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-102-8"></span>T. Liu, Y. Zhao, R. Joshi, M. Khalman, M. Saleh, P. J. Liu, and J. Liu. Statistical rejection sampling improves preference optimization. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. URL <https://openreview.net/forum?id=xbjSwwrQOe>. (Cited on pages [68,](#page-67-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-103-0"></span>T. Liu, Z. Qin, J. Wu, J. Shen, M. Khalman, R. Joshi, Y. Zhao, M. Saleh, S. Baumgartner, J. Liu, P. J. Liu, and X. Wang. LiPO: Listwise preference optimization through learning-torank. In L. Chiruzzo, A. Ritter, and L. Wang, editors, Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 2404–2420, Albuquerque, New Mexico, Apr. 2025c. Association for Computational Linguistics. ISBN 979-8-89176- 189-6. doi: 10.18653/v1/2025.naacl-long.121. URL [https://aclanthology.org/2025.](https://aclanthology.org/2025.naacl-long.121/) [naacl-long.121/](https://aclanthology.org/2025.naacl-long.121/). (Cited on pages [14,](#page-13-0) [78,](#page-77-0) [89,](#page-88-2) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-103-6"></span>T.-Y. Liu et al. Learning to rank for information retrieval. Foundations and Trends® in Information Retrieval, 3(3):225–331, 2009. (Cited on page [78.](#page-77-0))
- <span id="page-103-3"></span>Z. Liu, C. Chen, W. Li, P. Qi, T. Pang, C. Du, W. S. Lee, and M. Lin. Understanding R1-Zero-like training: A critical perspective. arXiv preprint arXiv:2503.20783, 2025d. doi: 10.48550/arXiv.2503.20783. URL <https://arxiv.org/abs/2503.20783>. (Cited on pages [23,](#page-22-3) [28,](#page-27-3) [41,](#page-40-3) [55,](#page-54-2) [58,](#page-57-2) [59,](#page-58-3) [60,](#page-59-1) [61,](#page-60-3) [63,](#page-62-1) [87,](#page-86-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-103-5"></span>Z. Liu, J. Liu, Y. He, W. Wang, J. Liu, L. Pan, X. Hu, S. Xiong, J. Huang, J. Hu, S. Huang, J. Obando-Ceron, S. Yang, J. Wang, W. Su, and B. Zheng. Part I: Tricks or traps? a deep dive into RL for LLM reasoning. In The Fourteenth International Conference on Learning Representations, ICLR 2026, 2026b. URL [https://openreview.net/forum?id=](https://openreview.net/forum?id=R0JM3BWP7W) [R0JM3BWP7W](https://openreview.net/forum?id=R0JM3BWP7W). (Cited on pages [36,](#page-35-4) [41,](#page-40-3) [42,](#page-41-4) [55,](#page-54-2) [59,](#page-58-3) [60,](#page-59-1) [63,](#page-62-1) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-103-1"></span>X. Lv, Y. Zuo, Y. Sun, H. Liu, Y. Wei, Z. Chen, X. Zhu, K. Zhang, B. Wang, N. Ding, and B. Zhou. Towards a unified view of large language model post-training. arXiv preprint arXiv:2509.04419, 2025. URL <https://arxiv.org/abs/2509.04419>. (Cited on pages [18,](#page-17-1) [30,](#page-29-3) [54,](#page-53-3) [90,](#page-89-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-103-4"></span>C. Lyu, S. Gao, Y. Gu, W. Zhang, J. Gao, K. Liu, Z. Wang, S. Li, Q. Zhao, H. Huang, W. Cao, J. Liu, H. Liu, J. Liu, S. Zhang, D. Lin, and K. Chen. Exploring the limit of outcome reward for learning mathematical reasoning. arXiv preprint arXiv:2502.06781, 2025. URL <https://arxiv.org/abs/2502.06781>. (Cited on pages [33,](#page-32-3) [38,](#page-37-6) [60,](#page-59-1) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-103-7"></span>P. Maini, Z. Feng, A. Schwarzschild, Z. C. Lipton, and J. Z. Kolter. Tofu: A task of fictitious unlearning for llms. arXiv, 2024. (Cited on page [82.](#page-81-3))
- <span id="page-103-8"></span>Y. Meng, M. Xia, and D. Chen. Simpo: Simple preference optimization with a reference-free reward. In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. URL [http://papers.nips.cc/paper\\_files/paper/2024/hash/](http://papers.nips.cc/paper_files/paper/2024/hash/e099c1c9699814af0be873a175361713-Abstract-Conference.html) [e099c1c9699814af0be873a175361713-Abstract-Conference.html](http://papers.nips.cc/paper_files/paper/2024/hash/e099c1c9699814af0be873a175361713-Abstract-Conference.html). (Cited on pages [84,](#page-83-2) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-103-2"></span>MiniMax-M1 Team. Minimax-m1: Scaling test-time compute efficiently with lightning attention. arXiv preprint arXiv:2506.13585, 2025. URL [https://arxiv.org/abs/2506.](https://arxiv.org/abs/2506.13585) [13585](https://arxiv.org/abs/2506.13585). (Cited on pages [19,](#page-18-4) [37,](#page-36-1) [117,](#page-116-0) and [122.](#page-121-0))

- <span id="page-104-2"></span>Mistral-AI, A. Rastogi, A. Q. Jiang, A. Lo, G. Berrada, G. Lample, J. Rute, J. Barmentlo, K. Yadav, K. Khandelwal, K. R. Chandu, L. Blier, L. Saulnier, M. Dinot, M. Darrin, N. Gupta, R. Soletskyi, S. Vaze, T. L. Scao, Y. Wang, A. Yang, A. H. Liu, A. Sablayrolles, A. Héliou, A. Martin, A. Ehrenberg, A. Agarwal, A. Roux, A. Darcet, A. Mensch, B. Bout, B. Rozière, B. D. Monicault, C. Bamford, C. Wallenwein, C. Renaudin, C. Lanfranchi, D. Dabert, D. Mizelle, D. de las Casas, E. Chane-Sane, E. Fugier, E. B. Hanna, G. Delerce, G. Guinet, G. Novikov, G. Martin, H. Jaju, J. Ludziejewski, J.-H. Chabran, J.-M. Delignon, J. Studnia, J. Amar, J. S. Roberts, J. Denize, K. Saxena, K. Jain, L. Zhao, L. Martin, L. Gao, L. R. Lavaud, M. Pellat, M. Guillaumin, M. Felardos, M. Augustin, M. Seznec, N. Raghuraman, O. Duchenne, P. Wang, P. von Platen, P. Saffer, P. Jacob, P. Wambergue, P. Kurylowicz, P. R. Muddireddy, P. Chagniot, P. Stock, P. Agrawal, R. Sauvestre, R. Delacourt, S. Gandhi, S. Subramanian, S. Dalal, S. Gandhi, S. Ghosh, S. Mishra, S. Aithal, S. Antoniak, T. Schueller, T. Lavril, T. Robert, T. Wang, T. Lacroix, V. Nemychnikova, V. Paltz, V. Richard, W.-D. Li, W. Marshall, X. Zhang, and Y. Tang. Magistral. arXiv preprint arXiv:2506.10910, 2025. URL <https://arxiv.org/abs/2506.10910>. (Cited on pages [24,](#page-23-0) [57,](#page-56-5) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-104-3"></span>T. Mu, A. Helyar, J. Heidecke, J. Achiam, A. Vallone, I. Kivlichan, M. Lin, A. Beutel, J. Schulman, and L. Weng. Rule based rewards for language model safety. In Proceedings of the 38th International Conference on Neural Information Processing Systems, NIPS '24, Red Hook, NY, USA, 2024. Curran Associates Inc. ISBN 9798331314385. (Cited on pages [67,](#page-66-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-104-4"></span>R. Munos, M. Valko, D. Calandriello, M. Gheshlaghi Azar, M. Rowland, Z. D. Guo, Y. Tang, M. Geist, T. Mesnard, C. Fiegel, A. Michi, M. Selvi, S. Girgin, N. Momchev, O. Bachem, D. J. Mankowitz, D. Precup, and B. Piot. Nash learning from human feedback. In R. Salakhutdinov, Z. Kolter, K. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp, editors, Proceedings of the 41st International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research, pages 36743–36768. PMLR, 21–27 Jul 2024. URL <https://proceedings.mlr.press/v235/munos24a.html>. (Cited on pages [70,](#page-69-4) [71,](#page-70-3) [89,](#page-88-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-104-1"></span>Olmo Team, A. Ettinger, A. Bertsch, B. Kuehl, D. Graham, D. Heineman, D. Groeneveld, F. Brahman, F. Timbers, H. Ivison, J. Morrison, J. Poznanski, K. Lo, L. Soldaini, M. Jordan, M. Chen, M. Noukhovitch, N. Lambert, P. Walsh, P. Dasigi, R. Berry, S. Malik, S. Shah, S. Geng, S. Arora, S. Gupta, T. Anderson, T. Xiao, T. Murray, T. Romero, V. Graf, A. Asai, A. Bhagia, A. Wettig, A. Liu, A. Rangapur, C. Anastasiades, C. Huang, D. Schwenk, H. Trivedi, I. Magnusson, J. Lochner, J. Liu, L. J. V. Miranda, M. Sap, M. Morgan, M. Schmitz, M. Guerquin, M. Wilson, R. Huff, R. L. Bras, R. Xin, R. Shao, S. Skjonsberg, S. Z. Shen, S. S. Li, T. Wilde, V. Pyatkin, W. Merrill, Y. Chang, Y. Gu, Z. Zeng, A. Sabharwal, L. Zettlemoyer, P. W. Koh, A. Farhadi, N. A. Smith, and H. Hajishirzi. Olmo 3. arXiv preprint arXiv:2512.13961, 2025. URL <https://arxiv.org/abs/2512.13961>. (Cited on pages [23,](#page-22-3) [25,](#page-24-2) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-104-0"></span>OpenAI, J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, R. Avila, I. Babuschkin, S. Balaji, V. Balcom, P. Baltescu, H. Bao, M. Bavarian, J. Belgum, I. Bello, J. Berdine, G. Bernadett-

Shapiro, C. Berner, L. Bogdonoff, O. Boiko, M. Boyd, A.-L. Brakman, G. Brockman, T. Brooks, M. Brundage, K. Button, T. Cai, R. Campbell, A. Cann, B. Carey, C. Carlson, R. Carmichael, B. Chan, C. Chang, F. Chantzis, D. Chen, S. Chen, R. Chen, J. Chen, M. Chen, B. Chess, C. Cho, C. Chu, H. W. Chung, D. Cummings, J. Currier, Y. Dai, C. Decareaux, T. Degry, N. Deutsch, D. Deville, A. Dhar, D. Dohan, S. Dowling, S. Dunning, A. Ecoffet, A. Eleti, T. Eloundou, D. Farhi, L. Fedus, N. Felix, S. P. Fishman, J. Forte, I. Fulford, L. Gao, E. Georges, C. Gibson, V. Goel, T. Gogineni, G. Goh, R. Gontijo-Lopes, J. Gordon, M. Grafstein, S. Gray, R. Greene, J. Gross, S. S. Gu, Y. Guo, C. Hallacy, J. Han, J. Harris, Y. He, M. Heaton, J. Heidecke, C. Hesse, A. Hickey, W. Hickey, P. Hoeschele, B. Houghton, K. Hsu, S. Hu, X. Hu, J. Huizinga, S. Jain, S. Jain, J. Jang, A. Jiang, R. Jiang, H. Jin, D. Jin, S. Jomoto, B. Jonn, H. Jun, T. Kaftan, Łukasz Kaiser, A. Kamali, I. Kanitscheider, N. S. Keskar, T. Khan, L. Kilpatrick, J. W. Kim, C. Kim, Y. Kim, J. H. Kirchner, J. Kiros, M. Knight, D. Kokotajlo, Łukasz Kondraciuk, A. Kondrich, A. Konstantinidis, K. Kosic, G. Krueger, V. Kuo, M. Lampe, I. Lan, T. Lee, J. Leike, J. Leung, D. Levy, C. M. Li, R. Lim, M. Lin, S. Lin, M. Litwin, T. Lopez, R. Lowe, P. Lue, A. Makanju, K. Malfacini, S. Manning, T. Markov, Y. Markovski, B. Martin, K. Mayer, A. Mayne, B. McGrew, S. M. McKinney, C. McLeavey, P. McMillan, J. McNeil, D. Medina, A. Mehta, J. Menick, L. Metz, A. Mishchenko, P. Mishkin, V. Monaco, E. Morikawa, D. Mossing, T. Mu, M. Murati, O. Murk, D. Mély, A. Nair, R. Nakano, R. Nayak, A. Neelakantan, R. Ngo, H. Noh, L. Ouyang, C. O'Keefe, J. Pachocki, A. Paino, J. Palermo, A. Pantuliano, G. Parascandolo, J. Parish, E. Parparita, A. Passos, M. Pavlov, A. Peng, A. Perelman, F. de Avila Belbute Peres, M. Petrov, H. P. de Oliveira Pinto, Michael, Pokorny, M. Pokrass, V. H. Pong, T. Powell, A. Power, B. Power, E. Proehl, R. Puri, A. Radford, J. Rae, A. Ramesh, C. Raymond, F. Real, K. Rimbach, C. Ross, B. Rotsted, H. Roussez, N. Ryder, M. Saltarelli, T. Sanders, S. Santurkar, G. Sastry, H. Schmidt, D. Schnurr, J. Schulman, D. Selsam, K. Sheppard, T. Sherbakov, J. Shieh, S. Shoker, P. Shyam, S. Sidor, E. Sigler, M. Simens, J. Sitkin, K. Slama, I. Sohl, B. Sokolowsky, Y. Song, N. Staudacher, F. P. Such, N. Summers, I. Sutskever, J. Tang, N. Tezak, M. B. Thompson, P. Tillet, A. Tootoonchian, E. Tseng, P. Tuggle, N. Turley, J. Tworek, J. F. C. Uribe, A. Vallone, A. Vijayvergiya, C. Voss, C. Wainwright, J. J. Wang, A. Wang, B. Wang, J. Ward, J. Wei, C. Weinmann, A. Welihinda, P. Welinder, J. Weng, L. Weng, M. Wiethoff, D. Willner, C. Winter, S. Wolrich, H. Wong, L. Workman, S. Wu, J. Wu, M. Wu, K. Xiao, T. Xu, S. Yoo, K. Yu, Q. Yuan, W. Zaremba, R. Zellers, C. Zhang, M. Zhang, S. Zhao, T. Zheng, J. Zhuang, W. Zhuk, and B. Zoph. Gpt-4 technical report, 2024. URL <https://arxiv.org/abs/2303.08774>. (Cited on pages [4,](#page-3-5) [13,](#page-12-5) and [82.](#page-81-3))

- <span id="page-105-0"></span>L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe. Training language models to follow instructions with human feedback, 2022. (Cited on pages [4,](#page-3-5) [13,](#page-12-5) [36,](#page-35-4) [42,](#page-41-4) [48,](#page-47-3) [58,](#page-57-2) [59,](#page-58-3) [86,](#page-85-4) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-105-1"></span>A. Pal, D. Karkhanis, S. Dooley, M. Roberts, S. Naidu, and C. White. Smaug: Fixing failure modes of preference optimisation with dpo-positive, 2024. (Cited on pages [72,](#page-71-3) [126,](#page-125-1) and [128.](#page-127-1))

- <span id="page-106-2"></span>K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the Association for Computational Linguistics, pages 311–318, 2002. (Cited on page [13.](#page-12-5))
- <span id="page-106-9"></span>R. Park, R. Rafailov, S. Ermon, and C. Finn. Disentangling length from quality in direct preference optimization. In L.-W. Ku, A. Martins, and V. Srikumar, editors, Findings of the Association for Computational Linguistics: ACL 2024, pages 4998–5017, Bangkok, Thailand, Aug. 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024. findings-acl.297. URL <https://aclanthology.org/2024.findings-acl.297/>. (Cited on pages [84,](#page-83-2) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-106-10"></span>S. K. Pentyala, Z. Wang, B. Bi, K. Ramnath, X.-B. Mao, R. Radhakrishnan, S. Asur, Na, and Cheng. Paft: A parallel training paradigm for effective llm fine-tuning, 2024. URL <https://arxiv.org/abs/2406.17923>. (Cited on pages [86,](#page-85-4) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-106-0"></span>A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever. Language models are unsupervised multitask learners. OpenAI Technical Report, 2019. (Cited on page [4.](#page-3-5))
- <span id="page-106-3"></span>R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn. Direct preference optimization: your language model is secretly a reward model. In Proceedings of the 37th International Conference on Neural Information Processing Systems, NIPS '23, Red Hook, NY, USA, 2023. Curran Associates Inc. (Cited on pages [15,](#page-14-2) [79,](#page-78-3) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-106-8"></span>R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn. Direct preference optimization: Your language model is secretly a reward model, 2024. URL <https://arxiv.org/abs/2305.18290>. (Cited on pages [80,](#page-79-0) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-106-1"></span>M. Ranzato, S. Chopra, M. Auli, and W. Zaremba. Sequence level training with recurrent neural networks. International Conference on Learning Representations, 2016. (Cited on page [11.](#page-10-3))
- <span id="page-106-7"></span>P. H. Richemond, Y. Tang, D. Guo, D. Calandriello, M. G. Azar, R. Rafailov, B. A. Pires, E. Tarassov, L. Spangher, W. Ellsworth, A. Severyn, J. Mallinson, L. Shani, G. Shamir, R. Joshi, T. Liu, R. Munos, and B. Piot. Offline regularised reinforcement learning for large language models alignment, 2024. URL <https://arxiv.org/abs/2405.19107>. (Cited on pages [75,](#page-74-2) [76,](#page-75-5) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-106-6"></span>C. Rosset, C.-A. Cheng, A. Mitra, M. Santacroce, A. Awadallah, and T. Xie. Direct nash optimization: Teaching language models to self-improve with general preferences, 2024. URL <https://arxiv.org/abs/2404.03715>. (Cited on pages [71,](#page-70-3) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-106-5"></span>N. L. Roux, M. G. Bellemare, J. Lebensold, A. Bergeron, J. Greaves, A. Fréchette, C. Pelletier, E. Thibodeau-Laufer, S. Toth, and S. Work. Tapered off-policy REINFORCE: Stable and efficient reinforcement learning for LLMs. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=gFFgCWiXWI>. (Cited on pages [27,](#page-26-1) [33,](#page-32-3) [36,](#page-35-4) [39,](#page-38-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-106-4"></span>J. Schulman. Approximating kl divergence, 2020. URL [http://joschu.net/blog/](http://joschu.net/blog/kl-approx.html) [kl-approx.html](http://joschu.net/blog/kl-approx.html). Accessed: 2026-02-26. (Cited on page [16.](#page-15-3))

- <span id="page-107-3"></span>J. Schulman, S. Levine, P. Moritz, M. I. Jordan, and P. Abbeel. Trust region policy optimization, 2017a. URL <https://arxiv.org/abs/1502.05477>. (Cited on pages [11](#page-10-3) and [12.](#page-11-6))
- <span id="page-107-1"></span>J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms, 2017b. (Cited on pages [4,](#page-3-5) [11,](#page-10-3) [12,](#page-11-6) [26,](#page-25-2) [36,](#page-35-4) [42,](#page-41-4) [48,](#page-47-3) [58,](#page-57-2) [59,](#page-58-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-107-5"></span>J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. High-dimensional continuous control using generalized advantage estimation, 2018. URL [https://arxiv.org/abs/](https://arxiv.org/abs/1506.02438) [1506.02438](https://arxiv.org/abs/1506.02438). (Cited on page [12.](#page-11-6))
- <span id="page-107-2"></span>Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024. URL [https://arxiv.org/abs/2402.](https://arxiv.org/abs/2402.03300) [03300](https://arxiv.org/abs/2402.03300). (Cited on pages [4,](#page-3-5) [6,](#page-5-4) [7,](#page-6-5) [16,](#page-15-3) [17,](#page-16-3) [19,](#page-18-4) [23,](#page-22-3) [26,](#page-25-2) [27,](#page-26-1) [36,](#page-35-4) [42,](#page-41-4) [48,](#page-47-3) [55,](#page-54-2) [58,](#page-57-2) [59,](#page-58-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-107-6"></span>T. Shi, Y. Wu, L. Song, T. Zhou, and J. Zhao. Efficient reinforcement finetuning via adaptive curriculum learning. arXiv preprint arXiv:2504.05520, 2025. (Cited on pages [24,](#page-23-0) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-107-7"></span>V. Shrivastava, A. Awadallah, V. Balachandran, S. Garg, H. Behl, and D. Papailiopoulos. Sample more to think less: Group filtered policy optimization for concise reasoning. In International Conference on Learning Representations, 2026. URL [https://arxiv.org/](https://arxiv.org/abs/2508.09726) [abs/2508.09726](https://arxiv.org/abs/2508.09726). (Cited on pages [25,](#page-24-2) [34,](#page-33-4) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-107-9"></span>F. Song, B. Yu, M. Li, H. Yu, F. Huang, Y. Li, and H. Wang. Preference ranking optimization for human alignment. In Proceedings of the Thirty-Eighth AAAI Conference on Artificial Intelligence and Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence and Fourteenth Symposium on Educational Advances in Artificial Intelligence, AAAI'24/IAAI'24/EAAI'24. AAAI Press, 2024. ISBN 978-1-57735-887-9. doi: 10.1609/aaai.v38i17.29865. URL <https://doi.org/10.1609/aaai.v38i17.29865>. (Cited on pages [78,](#page-77-0) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-107-0"></span>N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. F. Christiano. Learning to summarize with human feedback. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, editors, Advances in Neural Information Processing Systems, volume 33, pages 3008–3021. Curran Associates, Inc., 2020. URL [https://proceedings.neurips.cc/paper\\_files/paper/2020/file/](https://proceedings.neurips.cc/paper_files/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf) [1f89885d556929e98d3ef9b86448f951-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf). (Cited on pages [4](#page-3-5) and [13.](#page-12-5))
- <span id="page-107-8"></span>S. Sun, Y. Zhang, A. Bukharin, D. Mosallanezhad, J. Zeng, S. Singhal, G. Shen, A. Renduchintala, T. Konuk, Y. Dong, Z. Wang, D. Chichkov, O. Delalleau, and O. Kuchaiev. Reward-aware preference optimization: A unified mathematical framework for model alignment, 2025. URL <https://arxiv.org/abs/2502.00203>. (Cited on pages [74,](#page-73-0) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-107-4"></span>R. S. Sutton, D. McAllester, S. Singh, and Y. Mansour. Policy gradient methods for reinforcement learning with function approximation. In S. Solla, T. Leen, and

K. Müller, editors, Advances in Neural Information Processing Systems, volume 12. MIT Press, 1999. URL [https://proceedings.neurips.cc/paper\\_files/paper/1999/file/](https://proceedings.neurips.cc/paper_files/paper/1999/file/464d828b85b0bed98e80ade0a5c43b0f-Paper.pdf) [464d828b85b0bed98e80ade0a5c43b0f-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/1999/file/464d828b85b0bed98e80ade0a5c43b0f-Paper.pdf). (Cited on page [11.](#page-10-3))

- <span id="page-108-5"></span>Y. Tang, D. Z. Guo, Z. Zheng, D. Calandriello, R. Munos, M. Rowland, P. H. Richemond, M. Valko, B. A. Pires, and B. Piot. Generalized preference optimization: a unified approach to offline alignment. In Proceedings of the 41st International Conference on Machine Learning, ICML'24. JMLR.org, 2024. (Cited on pages [75,](#page-74-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-108-6"></span>A. Tversky and D. Kahneman. Advances in prospect theory: Cumulative representation of uncertainty. Journal of Risk and Uncertainty, 5:297–323, 1992. URL [https://api.](https://api.semanticscholar.org/CorpusID:8456150) [semanticscholar.org/CorpusID:8456150](https://api.semanticscholar.org/CorpusID:8456150). (Cited on page [75.](#page-74-2))
- <span id="page-108-0"></span>A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin. Attention is all you need. Advances in Neural Information Processing Systems, 2017. (Cited on page [4.](#page-3-5))
- <span id="page-108-2"></span>C. Walder and D. Karkhanis. Pass@k policy optimization: Solving harder reinforcement learning problems. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=W6WC6047X2>. (Cited on pages [35,](#page-34-3) [60,](#page-59-1) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-108-8"></span>C. Wang, Y. Jiang, C. Yang, H. Liu, and Y. Chen. Beyond reverse KL: generalizing direct preference optimization with diverse divergence constraints. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. URL <https://openreview.net/forum?id=2cRzmWXK9N>. (Cited on pages [83,](#page-82-1) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-108-3"></span>S. Wang, L. Yu, C. Gao, C. Zheng, S. Liu, R. Lu, K. Dang, X. Chen, J. Yang, Z. Zhang, Y. Liu, A. Yang, A. Zhao, Y. Yue, S. Song, B. Yu, G. Huang, and J. Lin. Beyond the 80/20 rule: High-entropy minority tokens drive effective reinforcement learning for llm reasoning. 2025a. URL <https://openreview.net/forum?id=yfcpdY4gMP>. (Cited on pages [37,](#page-36-1) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-108-4"></span>Z. Wang. GIFT: Group-relative implicit fine tuning integrates GRPO with DPO and UNA. arXiv preprint arXiv:2510.23868, 2025. URL <https://arxiv.org/abs/2510.23868>. (Cited on pages [52,](#page-51-2) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-108-9"></span>Z. Wang, B. Bi, Z. Zhu, X. Mao, J. Wang, and S. Wang. Uft: Unifying fine-tuning of sft and rlhf/dpo/una through a generalized implicit reward function, 2025b. URL <https://arxiv.org/abs/2410.21438>. (Cited on pages [86,](#page-85-4) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-108-1"></span>J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou. Chain-of-thought prompting elicits reasoning in large language models, 2023. (Cited on pages [4](#page-3-5) and [66.](#page-65-0))
- <span id="page-108-7"></span>G. Wiher, C. Meister, and R. Cotterell. On decoding strategies for neural text generators. Trans. Assoc. Comput. Linguistics, 10:997–1012, 2022. doi: 10.1162/TACL\\_A\\_00502. URL [https://doi.org/10.1162/tacl\\_a\\_00502](https://doi.org/10.1162/tacl_a_00502). (Cited on page [83.](#page-82-1))

- <span id="page-109-0"></span>R. J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine learning, 8:229–256, 1992. (Cited on pages [10](#page-9-2) and [17.](#page-16-3))
- <span id="page-109-9"></span>J. Wu, Y. Xie, Z. Yang, J. Wu, J. Gao, B. Ding, X. Wang, and X. He. β-dpo: direct preference optimization with dynamic β. In Proceedings of the 38th International Conference on Neural Information Processing Systems, NIPS '24, Red Hook, NY, USA, 2024. Curran Associates Inc. ISBN 9798331314385. (Cited on pages [73,](#page-72-1) [87,](#page-86-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-109-3"></span>S. Wu, J. Xie, Y. Zhang, A. Chen, K. Zhang, Y. Su, and Y. Xiao. ARM: Adaptive reasoning model. In Advances in Neural Information Processing Systems, 2025a. URL <https://openreview.net/forum?id=z9oeQrcNh9>. (Cited on pages [43,](#page-42-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-109-7"></span>T. Wu, W. Yuan, O. Golovneva, J. Xu, Y. Tian, J. Jiao, J. E. Weston, and S. Sukhbaatar. Meta-rewarding language models: Self-improving alignment with LLM-as-a-meta-judge. In C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng, editors, Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pages 11537– 11554, Suzhou, China, Nov. 2025b. Association for Computational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.583. URL [https://aclanthology.](https://aclanthology.org/2025.emnlp-main.583/) [org/2025.emnlp-main.583/](https://aclanthology.org/2025.emnlp-main.583/). (Cited on pages [69,](#page-68-1) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-109-8"></span>Y. Wu, Z. Sun, H. Yuan, K. Ji, Y. Yang, and Q. Gu. Self-play preference optimization for language model alignment. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025c. URL <https://openreview.net/forum?id=a3PmRgAB5T>. (Cited on pages [70,](#page-69-4) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-109-4"></span>C. Xiao, M. Zhang, and Y. Cao. BNPO: Beta normalization policy optimization. arXiv preprint arXiv:2506.02864, 2025. (Cited on pages [54,](#page-53-3) [55,](#page-54-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-109-2"></span>J. Xiong, J. Zhou, J. Ye, Q. Huang, and D. Dou. AAPO: Enhancing the reasoning capabilities of LLMs with advantage momentum. arXiv preprint arXiv:2505.14264, 2025a. (Cited on pages [41,](#page-40-3) [53,](#page-52-4) [58,](#page-57-2) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-109-1"></span>W. Xiong, J. Yao, Y. Xu, B. Pang, L. Wang, D. Sahoo, J. Li, N. Jiang, T. Zhang, C. Xiong, and H. Dong. A minimalist approach to llm reasoning: from rejection sampling to reinforce, 2025b. URL <https://arxiv.org/abs/2504.11343>. (Cited on pages [36,](#page-35-4) [59,](#page-58-3) [60,](#page-59-1) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-109-10"></span>H. Xu, Y. J. Kim, A. Sharaf, and H. H. Awadalla. A paradigm shift in machine translation: Boosting translation performance of large language models, 2024a. URL [https://arxiv.](https://arxiv.org/abs/2309.11674) [org/abs/2309.11674](https://arxiv.org/abs/2309.11674). (Cited on page [82.](#page-81-3))
- <span id="page-109-5"></span>H. Xu, A. Sharaf, Y. Chen, W. Tan, L. Shen, B. V. Durme, K. Murray, and Y. J. Kim. Contrastive preference optimization: Pushing the boundaries of llm performance in machine translation, 2024b. (Cited on pages [69,](#page-68-1) [82,](#page-81-3) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-109-6"></span>J. Xu, A. Lee, S. Sukhbaatar, and J. Weston. Some things are more cringe than others: Iterative preference optimization with the pairwise cringe loss, 2024c. URL [https://](https://arxiv.org/abs/2312.16682) [arxiv.org/abs/2312.16682](https://arxiv.org/abs/2312.16682). (Cited on pages [69,](#page-68-1) [126,](#page-125-1) and [128.](#page-127-1))

- <span id="page-110-3"></span>Y. E. Xu, Y. Savani, F. Fang, and J. Z. Kolter. Not all rollouts are useful: Down-sampling rollouts in LLM reinforcement learning. arXiv preprint arXiv:2504.13818, 2025. URL <https://arxiv.org/abs/2504.13818>. (Cited on pages [25,](#page-24-2) [34,](#page-33-4) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-110-2"></span>Z. Xu and Z. Ding. Single-stream policy optimization. In The Fourteenth International Conference on Learning Representations, ICLR 2026, 2026. URL [https://openreview.](https://openreview.net/forum?id=b61UW62K7W) [net/forum?id=b61UW62K7W](https://openreview.net/forum?id=b61UW62K7W). (Cited on pages [24,](#page-23-0) [36,](#page-35-4) [50,](#page-49-3) [57,](#page-56-5) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-110-8"></span>P. Yadav, D. Tam, L. Choshen, C. Raffel, and M. Bansal. Ties-merging: Resolving interference when merging models, 2023. URL <https://arxiv.org/abs/2306.01708>. (Cited on page [86.](#page-85-4))
- <span id="page-110-4"></span>J. Yan, Y. Li, Z. Hu, Z. Wang, G. Cui, X. Qu, Y. Cheng, and Y. Zhang. Learning to reason under off-policy guidance. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=vO8LLoNWWk>. (Cited on pages [28,](#page-27-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-110-1"></span>A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025. URL <https://arxiv.org/abs/2505.09388>. (Cited on pages [23,](#page-22-3) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-110-7"></span>L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li, A. Weller, and W. Liu. Metamath: Bootstrap your own mathematical questions for large language models. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. URL [https://openreview.net/forum?](https://openreview.net/forum?id=N8N0hgNDRt) [id=N8N0hgNDRt](https://openreview.net/forum?id=N8N0hgNDRt). (Cited on page [73.](#page-72-1))
- <span id="page-110-0"></span>Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, W. Dai, T. Fan, G. Liu, L. Liu, X. Liu, H. Lin, Z. Lin, B. Ma, G. Sheng, Y. Tong, C. Zhang, M. Zhang, W. Zhang, H. Zhu, J. Zhu, J. Chen, J. Chen, C. Wang, H. Yu, Y. Song, X. Wei, H. Zhou, J. Liu, W.-Y. Ma, Y.-Q. Zhang, L. Yan, M. Qiao, Y. Wu, and M. Wang. Dapo: An open-source llm reinforcement learning system at scale. In Advances in Neural Information Processing Systems, 2025. URL <https://openreview.net/forum?id=2a36EMSSTp>. (Cited on pages [18,](#page-17-1) [23,](#page-22-3) [25,](#page-24-2) [36,](#page-35-4) [42,](#page-41-4) [55,](#page-54-2) [59,](#page-58-3) [60,](#page-59-1) [63,](#page-62-1) [119,](#page-118-1) and [124.](#page-123-1))
- <span id="page-110-6"></span>W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, and J. Weston. Self-rewarding language models. In Proceedings of the 41st International Conference on Machine Learning, ICML'24. JMLR.org, 2024. (Cited on pages [68,](#page-67-2) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-110-5"></span>Y. Yuan, Y. Yue, R. Zhu, T. Fan, and L. Yan. What's behind ppo's collapse in longcot? value optimization holds the secret. arXiv preprint arXiv:2503.01491, 2025. URL <https://arxiv.org/abs/2503.01491>. (Cited on pages [36,](#page-35-4) [48,](#page-47-3) [118,](#page-117-0) and [123.](#page-122-0))

- <span id="page-111-1"></span>Z. Yuan, H. Yuan, C. Li, G. Dong, K. Lu, C. Tan, C. Zhou, and J. Zhou. Scaling relationship on learning mathematical reasoning with large language models. arXiv preprint arXiv:2308.01825, 2023a. (Cited on pages [8,](#page-7-7) [33,](#page-32-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-111-7"></span>Z. Yuan, H. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang. Rrhf: Rank responses to align language models with human feedback without tears, 2023b. URL [https://arxiv.](https://arxiv.org/abs/2304.05302) [org/abs/2304.05302](https://arxiv.org/abs/2304.05302). (Cited on pages [77,](#page-76-3) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-111-4"></span>Y. Yue, Y. Yuan, Q. Yu, X. Zuo, R. Zhu, W. Xu, J. Chen, C. Wang, T. Fan, Z. Du, X. Wei, X. Yu, G. Liu, J. Liu, L. Liu, H. Lin, Z. Lin, B. Ma, C. Zhang, M. Zhang, W. Zhang, H. Zhu, R. Zhang, X. Liu, M. Wang, Y. Wu, and L. Yan. Vapo: Efficient and reliable reinforcement learning for advanced reasoning tasks. arXiv preprint arXiv:2504.05118, 2025. URL <https://arxiv.org/abs/2504.05118>. (Cited on pages [36,](#page-35-4) [49,](#page-48-3) [59,](#page-58-3) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-111-6"></span>R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi. Hellaswag: Can a machine really finish your sentence? In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, 2019. (Cited on page [73.](#page-72-1))
- <span id="page-111-8"></span>Y. Zeng, G. Liu, W. Ma, N. Yang, H. Zhang, and J. Wang. Token-level direct preference optimization, 2024. URL <https://arxiv.org/abs/2404.11999>. (Cited on pages [80,](#page-79-0) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-111-3"></span>H. Zhang, R. Zheng, Z. Yi, Z. Zhang, H. Peng, H. Wang, Z. Yuan, C. Ke, S. Chen, J. Yang, Y. Li, X. Li, J. Yan, Y. Liu, L. Jing, J. Qi, R. Xu, B. Fang, and Y. Yu. GEPO: Group expectation policy optimization for stable heterogeneous reinforcement learning. arXiv preprint arXiv:2508.17850, 2025a. URL <https://arxiv.org/abs/2508.17850>. (Cited on pages [29,](#page-28-1) [30,](#page-29-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-111-5"></span>J. Zhang and C. Zuo. GRPO-LEAD: A difficulty-aware reinforcement learning approach for concise mathematical reasoning in language models. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pages 5642–5654, Suzhou, China, Nov. 2025. Association for Computational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.287. URL [https://aclanthology.org/2025.emnlp-main.](https://aclanthology.org/2025.emnlp-main.287/) [287/](https://aclanthology.org/2025.emnlp-main.287/). (Cited on pages [43,](#page-42-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-111-2"></span>K. Zhang, Y. Hong, J. Bao, H. Jiang, Y. Song, D. Hong, and H. Xiong. GVPO: Group variance policy optimization for large language model post-training. In Advances in Neural Information Processing Systems, 2025b. URL [https://openreview.net/forum?](https://openreview.net/forum?id=cCYUFaR6En) [id=cCYUFaR6En](https://openreview.net/forum?id=cCYUFaR6En). (Cited on pages [29,](#page-28-1) [51,](#page-50-5) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-111-0"></span>K. Zhang, Y. Zuo, B. He, Y. Sun, R. Liu, C. Jiang, Y. Fan, K. Tian, G. Jia, P. Li, Y. Fu, X. Lv, Y. Zhang, S. Zeng, S. Qu, H. Li, S. Wang, Y. Wang, X. Long, F. Liu, X. Xu, J. Ma, X. Zhu, E. Hua, Y. Liu, Z. Li, H. Chen, X. Qu, Y. Li, W. Chen, Z. Yuan, J. Gao, D. Li, Z. Ma, G. Cui, Z. Liu, B. Qi, N. Ding, and B. Zhou. A survey of reinforcement learning for large reasoning models, 2025c. URL <https://arxiv.org/abs/2509.08827>. (Cited on page [4.](#page-3-5))
- <span id="page-112-6"></span>Q. Zhang, H. Wu, C. Zhang, P. Zhao, and Y. Bian. Right question is already half the answer: Fully unsupervised llm reasoning incentivization. In Advances in Neural Information Processing Systems, 2025d. URL <https://arxiv.org/abs/2504.05812>. (Cited on pages [46,](#page-45-4) [60,](#page-59-1) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-112-9"></span>R. Zhang, L. Lin, Y. Bai, and S. Mei. Negative preference optimization: From catastrophic collapse to effective unlearning, 2024. (Cited on pages [82,](#page-81-3) [127,](#page-126-1) and [129.](#page-128-1))
- <span id="page-112-0"></span>T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi. Bertscore: Evaluating text generation with BERT. In 8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net, 2020. URL <https://openreview.net/forum?id=SkeHuCVFDr>. (Cited on page [13.](#page-12-5))
- <span id="page-112-3"></span>X. Zhang, Z. Huang, Y. Li, C. Ni, J. Chen, and S. Oymak. Bread: Branched rollouts from expert anchors bridge sft and rl for reasoning. In Advances in Neural Information Processing Systems, 2025e. URL <https://openreview.net/forum?id=NUDaln2vCe>. (Cited on pages [30,](#page-29-3) [116,](#page-115-0) and [121.](#page-120-0))
- <span id="page-112-10"></span>X. Zhang, J. Wang, Z. Cheng, W. Zhuang, Z. Lin, M. Zhang, S. Wang, Y. Cui, C. Wang, J. Peng, S. Jiang, S. Kuang, S. Yin, C. Wen, H. Zhang, B. Chen, and B. Yu. SRPO: A cross-domain implementation of large-scale reinforcement learning on LLM. arXiv preprint arXiv:2504.14286, 2025f. URL <https://arxiv.org/abs/2504.14286>. (Cited on pages [115](#page-114-1) and [120.](#page-119-1))
- <span id="page-112-2"></span>A. Zhao, Y. Wu, Y. Yue, T. Wu, Q. Xu, Y. Yue, M. Lin, S. Wang, Q. Wu, Z. Zheng, and G. Huang. Absolute zero: Reinforced self-play reasoning with zero data. In Advances in Neural Information Processing Systems, 2025a. URL [https://arxiv.org/abs/2505.](https://arxiv.org/abs/2505.03335) [03335](https://arxiv.org/abs/2505.03335). (Cited on pages [22,](#page-21-3) [115,](#page-114-1) and [120.](#page-119-1))
- <span id="page-112-5"></span>X. Zhao, Z. Kang, A. Feng, S. Levine, and D. Song. Learning to reason without external rewards. In Advances in Neural Information Processing Systems, 2025b. URL [https:](https://openreview.net/forum?id=OU9nFEYR2M) [//openreview.net/forum?id=OU9nFEYR2M](https://openreview.net/forum?id=OU9nFEYR2M). (Cited on pages [45,](#page-44-2) [118,](#page-117-0) and [123.](#page-122-0))
- <span id="page-112-8"></span>Y. Zhao, R. Joshi, T. Liu, M. Khalman, M. Saleh, and P. J. Liu. Slic-hf: Sequence likelihood calibration with human feedback, 2023. URL [https://arxiv.org/abs/2305.](https://arxiv.org/abs/2305.10425) [10425](https://arxiv.org/abs/2305.10425). (Cited on pages [72,](#page-71-3) [126,](#page-125-1) and [128.](#page-127-1))
- <span id="page-112-4"></span>Y. Zhao, Y. Liu, J. Liu, J. Chen, X. Wu, Y. Hao, T. Lv, S. Huang, L. Cui, Q. Ye, F. Wan, and F. Wei. Geometric-mean policy optimization. In The Fourteenth International Conference on Learning Representations, ICLR 2026, 2026. URL [https://openreview.net/forum?](https://openreview.net/forum?id=nCEs0tSwc2) [id=nCEs0tSwc2](https://openreview.net/forum?id=nCEs0tSwc2). (Cited on pages [40,](#page-39-4) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-112-1"></span>C. Zheng, S. Liu, M. Li, X.-H. Chen, B. Yu, C. Gao, K. Dang, Y. Liu, R. Men, A. Yang, J. Zhou, and J. Lin. Group sequence policy optimization. arXiv preprint arXiv:2507.18071, 2025. URL <https://arxiv.org/abs/2507.18071>. (Cited on pages [18,](#page-17-1) [39,](#page-38-3) [117,](#page-116-0) and [122.](#page-121-0))
- <span id="page-112-7"></span>X. Zhu, D. Cheng, D. Zhang, H. Li, K. Zhang, C. Jiang, Y. Sun, E. Hua, Y. Zuo, X. Lv, Q. Zhang, L. Chen, F. Shao, B. Xue, Y. Song, Z. Yang, G. Cui, N. Ding, J. Gao, X. Liu, B. Zhou, H. Mei, and Z. Lin. Flowrl: Matching reward distributions for LLM

reasoning. CoRR, abs/2509.15207, 2025. doi: 10.48550/ARXIV.2509.15207. URL [https:](https://doi.org/10.48550/arXiv.2509.15207) [//doi.org/10.48550/arXiv.2509.15207](https://doi.org/10.48550/arXiv.2509.15207). (Cited on pages [52,](#page-51-2) [118,](#page-117-0) and [123.](#page-122-0))

### <span id="page-113-0"></span>Appendix A. RLVR - detailed characterization of all papers

<span id="page-114-1"></span><span id="page-114-0"></span>

| Paper                                                              | IS     | Clipping       | Reward  | Baseline                        | Norm<br>Adv  | Norm<br>Length          | Fn<br>Partition | KL  | Entropy    |
|--------------------------------------------------------------------|--------|----------------|---------|---------------------------------|--------------|-------------------------|-----------------|-----|------------|
| (2026)<br>al.<br>et<br>Khatri<br>RL<br>Scaling<br>of<br>Art<br>The | token  | asymmetry      | outcome | mean<br>group                   | std<br>batch | norm<br>length<br>group | no              | no  | no         |
| (2025a)<br>al.<br>et<br>Zhao<br>Zero<br>Absolute                   | token  | symmetry       | outcome | mean<br>group                   | std<br>batch | norm<br>length          | no              | no  | yes        |
| (2025)<br>al.<br>et<br>3 Yang<br>Qwen                              | token  | symmetry       | outcome | mean<br>group                   | std<br>group | norm<br>length          | no              | yes | yes        |
| (2025)<br>al.<br>et<br>Team<br>3 Olmo<br>OLMo                      | token  | asymmetry      | outcome | mean<br>group                   | 1            | norm<br>length<br>group | no              | no  | no         |
| (2025)<br>al.<br>et<br>Mistral-AI<br>Magistral                     | token  | asymmetry      | outcome | mean<br>batch<br>mean,<br>group | std<br>batch | norm<br>length<br>group | no              | no  | no         |
| (2025)<br>al.<br>et<br>Shi<br>AdaRFT                               | token  | symmetry       | outcome | function<br>value               | 1            | norm<br>length          | no              | yes | yes        |
| (2025f)<br>al.<br>et<br>Zhang<br>SRPO                              | token  | symmetry       | outcome | mean<br>group                   | std<br>group | norm<br>length          | no              | no  | no         |
| mpt<br>Pro<br>Methods:<br>selection.<br>R<br>RLV<br>2:<br>Table    | Source | papers).<br>(7 | Methods | training<br>on<br>innovating    | data         | curriculu<br>sourcing,  | design,<br>m    | and | mpt<br>pro |
|                                                                    |        |                |         |                                 |              |                         |                 |     |            |

<span id="page-115-0"></span>

| Paper                                        | IS       | Clipping  | Reward  | Baseline                            | Norm<br>Adv              | Norm<br>Length          | Fn<br>Partition | KL  | Entropy |
|----------------------------------------------|----------|-----------|---------|-------------------------------------|--------------------------|-------------------------|-----------------|-----|---------|
| (2025a)<br>al.<br>et<br>Li<br>RePO           | token    | symmetry  | outcome | mean<br>group                       | std<br>group             | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Roux<br>TOPR          | sequence | asymmetry | outcome | no                                  | 1                        | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Yan<br>LUFFY          | token    | symmetry  | outcome | mean<br>group                       | 1                        | norm<br>length<br>group | no              | no  | yes     |
| (2025b)<br>al.<br>et<br>Zhang<br>GVPO        | no       | no        | outcome | mean<br>group                       | 1                        | norm<br>length          | cancel          | yes | no      |
| (2025a)<br>al.<br>et<br>Zhang<br>GEPO        | group    | symmetry  | outcome | mean<br>group                       | 1                        | norm<br>length          | no              | yes | no      |
| (2025e)<br>al.<br>et<br>Zhang<br>BREAD       | token    | symmetry  | outcome | mean<br>group                       | std<br>group             | norm<br>length          | no              | yes | no      |
| (2025)<br>al.<br>et<br>Huang<br>Prefix-RFT   | token    | symmetry  | outcome | mean<br>group                       | 1                        | no                      | no              | no  | no      |
| (2025b)<br>al.<br>et<br>Li<br>TreePO         | token    | asymmetry | outcome | means<br>sub-group<br>different     | std<br>sub-group<br>same | norm<br>length<br>group | no              | no  | no      |
| (2025)<br>al.<br>et<br>Kazemnejad<br>VinePPO | token    | symmetry  | outcome | mean<br>batch<br>value<br>function, | std<br>batch             | norm<br>length          | no              | yes | no      |
| (2025b)<br>al.<br>et<br>Dai<br>S-GRPO        | token    | symmetry  | outcome | mean<br>group                       | 1                        | norm<br>length          | no              | no  | no      |
| (2026)<br>al.<br>et<br>Shrivastava<br>GFPO   | token    | symmetry  | outcome | mean<br>group                       | std<br>group             | norm<br>length<br>group | no              | yes | yes     |
| (2023a)<br>al.<br>et<br>Yuan<br>RFT          | no       | no        | outcome | no                                  | 1                        | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Xu<br>PODS            | token    | symmetry  | outcome | mean<br>group                       | std<br>group             | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Lin<br>CPPO           | token    | symmetry  | outcome | mean<br>group                       | std<br>group             | norm<br>length          | no              | yes | no      |
| (2025)<br>Karkhanis<br>and<br>Walder<br>PKPO | no       | no        | outcome | mean<br>group                       | 1                        | no                      | no              | no  | no      |
|                                              |          |           |         |                                     |                          |                         |                 |     |         |

| strategies.   |  |
|---------------|--|
|               |  |
|               |  |
|               |  |
| selection     |  |
|               |  |
|               |  |
|               |  |
| and           |  |
| generation    |  |
|               |  |
|               |  |
|               |  |
|               |  |
| response      |  |
|               |  |
|               |  |
| on            |  |
| innovating    |  |
|               |  |
|               |  |
|               |  |
|               |  |
|               |  |
|               |  |
|               |  |
| Methods       |  |
|               |  |
|               |  |
| papers).      |  |
| (15           |  |
|               |  |
|               |  |
| Design        |  |
|               |  |
|               |  |
|               |  |
| Response      |  |
|               |  |
|               |  |
|               |  |
| Methods:<br>R |  |
|               |  |
| RLV           |  |
| 3:            |  |
| Table         |  |

# Wang, Ramnath, et al.

<span id="page-116-0"></span>

| Paper                                                                                   | IS       | Clipping                                 | Reward                        | Baseline          | Norm<br>Adv  | Norm<br>Length          | Fn<br>Partition | KL                                  | Entropy |
|-----------------------------------------------------------------------------------------|----------|------------------------------------------|-------------------------------|-------------------|--------------|-------------------------|-----------------|-------------------------------------|---------|
| (2022)<br>al.<br>et<br>Ouyang<br>(2017b);<br>al.<br>et<br>Schulman<br>LLM<br>for<br>PPO | token    | symmetry                                 | outcome                       | function<br>value | 1            | norm<br>length          | no              | yes                                 | no      |
| (2024)<br>al.<br>et<br>Shao<br>GRPO                                                     | token    | symmetry                                 | outcome                       | mean<br>group     | std<br>group | norm<br>length          | no              | yes                                 | no      |
| (2025)<br>Team<br>MiniMax-M1<br>CISPO                                                   | token    | asymmetry                                | outcome                       | mean<br>group     | std<br>group | norm<br>length<br>group | no              | no                                  | no      |
| (2025)<br>al.<br>et<br>Gao<br>SAPO                                                      | token    | asymmetry                                | outcome                       | mean<br>group     | std<br>group | norm<br>length          | no              | no                                  | no      |
| (2025a)<br>al.<br>et<br>Wang<br>80/20<br>Beyond                                         | token    | asymmetry                                | outcome                       | mean<br>group     | std<br>group | norm<br>length<br>group | no              | no                                  | no      |
| (2025b)<br>al.<br>et<br>Cui<br>& KL-Cov<br>Clip-Cov                                     | token    | (Clip-Cov)<br>(KL-Cov)<br>symmetry<br>no | outcome                       | mean<br>group     | std<br>group | norm<br>length          | no              | (Clip-Cov)<br>(KL-Cov)<br>yes<br>no | no      |
| (2025)<br>al.<br>et<br>Lyu<br>OREAL                                                     | no       | no                                       | outcome                       | mean<br>group     | 1            | no                      | no              | yes                                 | no      |
| (2025)<br>al.<br>et<br>Zheng<br>GSPO                                                    | sequence | symmetry                                 | outcome                       | mean<br>group     | std<br>group | norm<br>length          | no              | no                                  | no      |
| (2026)<br>al.<br>et<br>Zhao<br>GMPO                                                     | token    | symmetry                                 | outcome                       | mean<br>group     | std<br>group | norm<br>length          | no              | no                                  | no      |
| (2026)<br>al.<br>et<br>Chu<br>GPG                                                       | no       | no                                       | outcome                       | mean<br>group     | 1            | norm<br>length<br>group | no              | no                                  | no      |
| (2025)<br>Welleck<br>and<br>Aggarwal<br>LCPO                                            | token    | symmetry                                 | penalty<br>outcome,<br>length | mean<br>group     | std<br>group | norm<br>length          | no              | yes                                 | no      |
| (2025a)<br>al.<br>et<br>GRPO-λ Dai                                                      | token    | symmetry                                 | penalty<br>outcome,<br>length | mean<br>group     | std<br>group | norm<br>length          | no              | yes                                 | no      |
| (2025)<br>Zuo<br>and<br>Zhang<br>GRPO-LEAD                                              | token    | symmetry                                 | penalty<br>outcome,<br>length | mean<br>group     | std<br>group | norm<br>length          | no              | no                                  | no      |
| (2025a)<br>al.<br>et<br>Wu<br>Ada-GRPO                                                  | token    | symmetry                                 | outcome                       | mean<br>group     | std<br>group | norm<br>length<br>group | no              | yes                                 | no      |
|                                                                                         |          |                                          |                               |                   |              |                         |                 |                                     |         |
|                                                                                         |          |                                          |                               |                   |              |                         |                 |                                     |         |

| Methods:<br>R<br>RLV<br>4:<br>Table | Gradient | 1<br>Part<br>fficient<br>Coe | papers).<br>(14 | importance<br>on<br>innovating<br>Methods | and<br>ratios | advantage |
|-------------------------------------|----------|------------------------------|-----------------|-------------------------------------------|---------------|-----------|
| mputation.<br>co                    |          |                              |                 |                                           |               |           |

<span id="page-117-0"></span>

| Paper                                            | IS       | Clipping  | Reward         | Baseline                            | Norm<br>Adv  | Norm<br>Length          | Fn<br>Partition | KL  | Entropy |
|--------------------------------------------------|----------|-----------|----------------|-------------------------------------|--------------|-------------------------|-----------------|-----|---------|
| (2025)<br>al.<br>et<br>Agarwal<br>Min<br>Entropy | no       | no        | self-certainty | mean<br>group                       | 1            | no                      | no              | yes | yes     |
| (2025b)<br>al.<br>et<br>Zhao<br>INTUITOR         | token    | symmetry  | self-certainty | mean<br>group                       | std<br>group | norm<br>length          | no              | yes | no      |
| (2025)<br>al.<br>et<br>Chen<br>Seed-GRPO         | sequence | symmetry  | outcome        | mean<br>group                       | 1            | no                      | no              | no  | yes     |
| (2025d)<br>al.<br>et<br>Zhang<br>EMPO            | token    | symmetry  | self-certainty | mean<br>group                       | std<br>group | no                      | no              | yes | no      |
| (2025a)<br>al.<br>et<br>Cui<br>PRIME             | token    | symmetry  | process        | mean<br>group                       | 1            | norm<br>length          | no              | no  | no      |
| (2025b)<br>al.<br>et<br>Cheng<br>PURE            | token    | no        | process        | mean<br>group                       | 1            | norm<br>length          | no              | yes | no      |
| (2025)<br>al.<br>et<br>Yuan<br>VC-PPO            | token    | symmetry  | outcome        | function<br>value                   | 1            | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Yue<br>VAPO               | token    | asymmetry | outcome        | function<br>value                   | 1            | norm<br>length<br>group | no              | yes | no      |
| (2025b)<br>al.<br>et<br>Hu<br>ORZ                | token    | symmetry  | outcome        | mean<br>batch<br>value<br>function, | std<br>batch | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Hao<br>OPO                | no       | no        | outcome        | minimization<br>variance            | 1            | no                      | no              | no  | no      |
| (2026)<br>Ding<br>and<br>Xu<br>SPO               | token    | symmetry  | outcome        | mean<br>batch<br>value<br>function, | std<br>batch | norm<br>length          | no              | no  | no      |
| (2025)<br>Team<br>Kimi<br>MDPO                   | no       | no        | outcome        | mean<br>group                       | 1            | no                      | estimated       | yes | no      |
| (2025)<br>al.<br>et<br>Zhu<br>FlowRL             | sequence | symmetry  | outcome        | mean<br>group                       | std<br>group | norm<br>length          | estimated       | yes | no      |
| (2025)<br>Wang<br>GIFT                           | no       | no        | outcome        | mean<br>group                       | std<br>group | no                      | cancel          | yes | no      |
|                                                  |          |           |                |                                     |              |                         |                 |     |         |

| and<br>baselines,<br>value                                              |            |
|-------------------------------------------------------------------------|------------|
| design,<br>ward<br>re<br>on<br>innovating<br>Methods                    |            |
| papers).<br>(14<br>2<br>Part<br>fficient<br>Coe<br>Gradient<br>Methods: | functions. |
| R<br>RLV<br>5:<br>Table                                                 | partition  |

118

<span id="page-118-1"></span><span id="page-118-0"></span>

| Paper                                              | IS    | Clipping  | Reward                        | Baseline                            | Norm<br>Adv                    | Norm<br>Length          | Fn<br>Partition | KL  | Entropy |
|----------------------------------------------------|-------|-----------|-------------------------------|-------------------------------------|--------------------------------|-------------------------|-----------------|-----|---------|
| (2025a)<br>al.<br>et<br>Xiong<br>AAPO              | no    | no        | outcome                       | mean<br>group                       | std<br>group                   | norm<br>length<br>group | no              | no  | no      |
| (2025)<br>al.<br>et<br>Fu<br>SRFT                  | token | no        | outcome                       | mean<br>group                       | std<br>group                   | norm<br>length          | no              | no  | yes     |
| (2025)<br>al.<br>et<br>Lv<br>HPT                   | token | symmetry  | outcome                       | mean<br>group                       | std<br>group                   | norm<br>length          | no              | no  | no      |
| (2025)<br>al.<br>et<br>Xiao<br>BNPO                | token | symmetry  | outcome                       | mean<br>group                       | distribution<br>Beta           | norm<br>length          | no              | no  | no      |
| (2026a)<br>al.<br>et<br>Liu<br>GDPO                | token | symmetry  | outcome                       | mean<br>batch<br>mean,<br>group     | std<br>batch<br>mean,<br>batch | norm<br>length          | no              | yes | no      |
| (2025a)<br>al.<br>et<br>Hu<br>REINFORCE++          | token | symmetry  | outcome                       | mean<br>batch<br>mean,<br>group     | std<br>batch                   | norm<br>length          | no              | yes | no      |
| (2025)<br>al.<br>et<br>Yu<br>DAPO                  | token | asymmetry | penalty<br>outcome,<br>length | mean<br>group                       | std<br>group                   | norm<br>length<br>group | no              | no  | no      |
| (2025b)<br>al.<br>et<br>Xiong<br>Reinforce-Rej     | token | asymmetry | outcome                       | no                                  | 1                              | norm<br>length          | no              | no  | no      |
| (2026b)<br>al.<br>et<br>Liu<br>PPO<br>Lite         | token | symmetry  | outcome                       | mean<br>group                       | std<br>batch                   | norm<br>length<br>group | no              | no  | no      |
| (2025d)<br>al.<br>et<br>Liu<br>Dr.GRPO             | token | symmetry  | outcome                       | mean<br>group                       | 1                              | no                      | no              | no  | no      |
| (2025a)<br>al.<br>et<br>Liu<br>ProRL               | token | asymmetry | outcome                       | mean<br>group                       | std<br>group                   | norm<br>length          | no              | yes | no      |
| (2025a)<br>al.<br>et<br>Cheng<br>Explor<br>Entropy | token | asymmetry | outcome                       | mean<br>group<br>function,<br>value | std<br>group                   | norm<br>length<br>group | no              | no  | yes     |
| (2025)<br>al.<br>et<br>He<br>MAGIC                 | token | symmetry  | outcome                       | mean<br>group                       | std<br>group                   | norm<br>length<br>group | no              | no  | yes     |
|                                                    |       |           |                               |                                     |                                |                         |                 |     |         |

![](./assets/01-rl-post-training-survey/_page_118_Figure_1.jpeg)

<span id="page-119-1"></span>

| Paper                                                                   | (Methodology)<br>Over<br>Improve | Model<br>Base                                                      | Data<br>Fine-tuning                                        | Benchmarks<br>Evaluation                                                                                                                     | With<br>(Methodology)<br>Compare                                   |
|-------------------------------------------------------------------------|----------------------------------|--------------------------------------------------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| (2026)<br>et al.<br>Khatri<br>RL<br>of Scaling<br>Art<br>The            | GRPO                             | MoE)<br>(17B×16<br>dense,<br>Scout<br>8B<br>Llama-4                | runs)<br>(math),<br>(math+code<br>Polaris-53K<br>Deepcoder | 2025)<br>(Jan–Jun<br>AIME-24,<br>LiveCodeBench                                                                                               | (DAPO),<br>MiniMax<br>Qwen2.5<br>(GRPO),<br>Magistral,<br>DeepSeek |
| (2025a)<br>et al.<br>Zhao<br>Zero<br>Absolute                           | REINFORCE++                      | Qwen2.5-7B-Coder,<br>Llama-3.1-8B<br>Qwen2.5-7B,                   | data)<br>human-curated<br>(zero<br>Self-play               | LiveCodeBench,<br>OlympiadBench<br>AMC,<br>2025,<br>AIME<br>MBPP,<br>Minerva,<br>2024,<br>HumanEval+,<br>MATH-500,<br>AIME                   | SFT<br>REINFORCE++,<br>GRPO,                                       |
| (2025)<br>et al.<br>3 Yang<br>Qwen                                      | GRPO                             | Qwen3-235B-A22B-Base,<br>Qwen3-32B-Base                            | pairs<br>STEM)<br>query-verifier<br>code,<br>(math,<br>∼4K | Codeforces<br>ZebraLogic,<br>MATH-500,<br>v5,<br>Diamond,<br>2024/25,<br>LiveCodeBench<br>AIME<br>GPQA                                       | SFT                                                                |
| (2025)<br>et al.<br>Team<br>3 Olmo<br>OLMo                              | GRPO                             | 32B<br>7B,<br>3 Base<br>3 Base<br>OLMo<br>OLMo                     | chat)<br>RL<br>IF,<br>Think<br>code,<br>Dolci<br>(math,    | OMEGA,<br>IFBench,<br>v3,<br>LiveCodeBench<br>2025,<br>IFEval,<br>AIME<br>GPQA,<br>2024,<br>HumanEval+,<br>AIME<br>MMLU,<br>MATH,            | RLVR<br>DPO,<br>SFT,                                               |
| (2025)<br>et al.<br>Mistral-AI<br>Magistral                             | GRPO                             | 3 Instruct<br>3 Instruct,<br>Medium<br>Small<br>Mistral<br>Mistral | problems<br>math,<br>curated<br>code<br>38K<br>35K         | MATH-500,<br>v6),<br>BBH<br>Diamond,<br>(v5,<br>Polyglot,<br>2025,<br>LiveCodeBench<br>ZebraLogic,<br>AIME<br>GPQA<br>Aider<br>2024,<br>AIME | GRPO<br>SFT,                                                       |
| (2025f)<br>(2025)<br>et al.<br>et al.<br>Zhang<br>Shi<br>AdaRFT<br>SRPO | GRPO<br>PPO                      | Qwen2.5-Math-1.5B,<br>Qwen2.5-32B-Base<br>Qwen2.5-7B               | + Code<br>DeepScaleR<br>Math<br>Curated                    | OlympiadBench,<br>LiveCodeBench<br>2024<br>Exam<br>AIME<br>Last<br>GSM8K,<br>AMC,<br>Humanity's<br>2024,<br>Minerva,<br>MATH-500,<br>AIME    | REINFORCE++<br>GRPO,<br>GRPO<br>PPO,                               |
|                                                                         |                                  |                                                                    |                                                            |                                                                                                                                              |                                                                    |

<span id="page-119-0"></span>

| mpt<br>pro<br>and<br>design, |            |
|------------------------------|------------|
| m<br>curriculu               |            |
| sourcing,<br>data            |            |
| training<br>on               |            |
| innovating<br>Methods        |            |
| papers).<br>(6               |            |
| Source<br>mpt<br>Pro         |            |
| Methods:<br>R<br>RLV         | selection. |
| 7:<br>Table                  |            |

<span id="page-120-0"></span>

| Paper                                        | (Methodology)<br>Over<br>Improve | Model<br>Base                                                                           | Data<br>Fine-tuning                   | Benchmarks<br>Evaluation                                                                                                                                              | With<br>(Methodology)<br>Compare                                          |
|----------------------------------------------|----------------------------------|-----------------------------------------------------------------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| (2025a)<br>et al.<br>Li<br>RePO              | GRPO                             | Qwen2.5-Math-1.5B/7B<br>Qwen3-1.7B<br>(-Instruct),                                      | DeepMath-103K                         | OlympiadBench,<br>MMLU-Pro,<br>IFEval<br>ARC-C,<br>AMC,<br>BBH,<br>Minerva,<br>2025,<br>Diamond,<br>ARC-Easy,<br>MATH-500,<br>AIME<br>GPQA<br>2024,<br>GSM8K,<br>AIME | Dr.GRPO<br>GRPO,                                                          |
| (2025)<br>et al.<br>Roux<br>TOPR             | REINFORCE                        | Instruct,<br>8B<br>DeepSeek-R1<br>3 8B<br>Llama                                         | MATH<br>GSM8K,                        | MATH-500<br>GSM8K,                                                                                                                                                    | IS,<br>Off-policy<br>Truncated<br>PPO<br>REINFORCE,<br>REINFORCE,<br>DPO, |
| (2025)<br>et al.<br>Yan<br>LUFFY             | GRPO                             | Qwen2.5-7B-Instruct,<br>Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>LLaMA-3.1-8B          | OpenR1-Math-220K                      | MATH-500,<br>MMLU-Pro<br>OlympiadBench,<br>AMC,<br>GPQA,<br>2024/25,<br>Minerva,<br>ARC-C,<br>AIME                                                                    | SFT<br>GRPO,                                                              |
| (2025b)<br>et al.<br>Zhang<br>GVPO           | REINFORCE++<br>ReMax,<br>GRPO,   | Llama-3.1-8B-Instruct<br>Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,                         | MATH                                  | MATH-500,<br>OlympiadBench<br>AMC,<br>2024,<br>Minerva,<br>AIME                                                                                                       | REINFORCE++<br>Dr.GRPO,<br>GRPO,<br>ReMax,                                |
| (2025a)<br>et al.<br>Zhang<br>GEPO           | GSPO<br>GRPO,                    | Qwen3-1.7B,<br>Qwen3-8B                                                                 | 3–5)<br>(Level<br>MATH                | MATH-500<br>2024,<br>AIME<br>2025,<br>AMC,<br>AIME                                                                                                                    | GRPO,<br>CISPO<br>Dr.GRPO,<br>TOPR,<br>GSPO,<br>BNPO,                     |
| (2025e)<br>et al.<br>Zhang<br>BREAD          | GRPO                             | Qwen2.5-1.5B-Instruct,<br>Qwen2.5-3B-Instruct                                           | NuminaMath-CoT<br>MATH,               | GPQA<br>NuminaMath-CoT,<br>MATH,                                                                                                                                      | SFT+GRPO<br>SFT,<br>GRPO,                                                 |
| (2025)<br>et al.<br>Huang<br>Prefix-RFT      | GRPO<br>SFT,                     | Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>LLaMA-3.1-8B                                  | OpenR1-Math-220K                      | MMLU-Pro<br>MATH-500,<br>OlympiadBench,<br>Diamond,<br>AMC,<br>2024/25,<br>GPQA<br>Minerva,<br>AIME<br>ARC-C,                                                         | SFT+GRPO,<br>ReLIFT<br>LUFFY,<br>GRPO,<br>SFT,                            |
| (2025b)<br>et al.<br>Li<br>TreePO            | DAPO<br>GRPO,                    | Qwen2.5-Math-7B-Instruct<br>Qwen2.5-7B-Instruct,<br>Qwen2.5-7B,                         | 3–5),<br>DeepScaleR<br>(Level<br>MATH | MATH-500,<br>OlympiadBench<br>AMC,<br>2024,<br>Minerva,<br>AIME                                                                                                       | GRPO                                                                      |
| (2025)<br>et al.<br>Kazemnejad<br>VinePPO    | PPO                              | 7B,<br>1.1B<br>DeepSeekMath<br>RhoMath                                                  | MATH<br>GSM8K,                        | MATH<br>GSM8K,                                                                                                                                                        | +<br>DPO<br>GRPO,<br>RestEM,<br>PPO,<br>RLOO,                             |
| (2025b)<br>et al.<br>Dai<br>S-GRPO           | GRPO                             | DeepSeek-R1-Distill-Qwen-14B<br>DeepSeek-R1-Distill-Qwen-7B,<br>Qwen3-14B,<br>Qwen3-8B, | DeepMath-103K                         | Diamond<br>AMC,<br>2024,<br>GPQA<br>AIME<br>MATH-500,<br>GSM8K,                                                                                                       | ConCISE,<br>Penalty,<br>ShortBetter<br>DEER,<br>RL+Length<br>GRPO,        |
| (2026)<br>et al.<br>Shrivastava<br>GFPO      | GRPO                             | Phi-4-reasoning                                                                         | problems<br>math<br>72K               | GPQA,<br>LiveCodeBench<br>2025,<br>AIME<br>Omni-MATH,<br>2024,<br>AIME                                                                                                | GRPO<br>SFT,                                                              |
| (2023a)<br>et al.<br>Yuan<br>RFT             | SFT                              | LLaMA2-13B<br>LLaMA-13B,<br>LLaMA2-7B,<br>LLaMA-7B,                                     | GSM8K                                 | GSM8K                                                                                                                                                                 | SFT                                                                       |
| (2025)<br>et al.<br>Xu<br>PODS               | GRPO                             | Qwen2.5-7B-Instruct,<br>Llama3.2-3B-Instruct<br>Qwen2.5-3B-Instruct,                    | MATH<br>GSM8K,                        | MATH<br>GSM8K,                                                                                                                                                        | GRPO-GA<br>GRPO,                                                          |
| (2025)<br>et al.<br>Lin<br>CPPO              | GRPO                             | Qwen2.5-1.5B-Instruct,<br>Qwen2.5-7B-Instruct                                           | MATH<br>GSM8K,                        | 2024<br>MATH,<br>AIME<br>GSM8K,<br>AMC,                                                                                                                               | DAPO,<br>Dr.GRPO<br>GRPO,                                                 |
| (2025)<br>Karkhanis<br>and<br>Walder<br>PKPO | RLOO<br>REINFORCE,               | 2 9B,<br>Gemma<br>8B<br>3.1<br>Llama<br>2 2B,<br>Gemma                                  | MBPP,<br>ARC-AGI-1<br>MATH,           | HumanEval+,<br>ARC-AGI-1<br>MATH,                                                                                                                                     | RLOO                                                                      |
|                                              |                                  |                                                                                         |                                       |                                                                                                                                                                       |                                                                           |

Table 8: RLVR Methods: Response Design (15 papers). Methods innovating on response generation and selection strategies.

# RL for LLM Post-training survey

<span id="page-121-0"></span>

| Paper                                                                             | (Methodology)<br>Over<br>Improve | Model<br>Base                                                                                                  | Data<br>Fine-tuning                                                                                                                                                                         | Benchmarks<br>Evaluation                                                                                                                                      | With<br>(Methodology)<br>Compare  |
|-----------------------------------------------------------------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| (2022)<br>et al.<br>Ouyang<br>(2017b);<br>et al.<br>Schulman<br>LLM<br>for<br>PPO | SFT                              | (1.3B/6B/175B)<br>GPT-3                                                                                        | comparisons<br>demonstrations<br>human-labeled<br>Labeler<br>+                                                                                                                              | RealToxicityPrompts,<br>CrowS-Pairs,<br>eval<br>human<br>Winogender,<br>API<br>TruthfulQA,                                                                    | SFT                               |
| (2024)<br>et al.<br>Shao<br>GRPO                                                  | PPO                              | DeepSeekMath-7B-Instruct                                                                                       | MATH<br>GSM8K,                                                                                                                                                                              | AIME<br>CMATH<br>MATH,<br>2024,<br>MGSM-zh,<br>GSM8K,<br>AIME<br>MATH-500,                                                                                    | DPO,<br>SFT<br>RFT,<br>PPO,       |
| (2025)<br>Team<br>MiniMax-M1<br>CISPO                                             | DAPO<br>GRPO,                    | (456B)<br>MiniMax-Text-01                                                                                      | SE,<br>logic),<br>SWE-bench-derived<br>domain<br>(53K<br>SynLogic<br>general<br>math,<br>25K<br>code,<br>50K<br>30K                                                                         | 2025,<br>ZebraLogic,<br>Verified,<br>FullStackBench,<br>LongBench-v2,<br>SWE-bench<br>HLE,<br>OpenAI-MRCR,<br>LiveCodeBench,<br>Diamond,<br>MMLU-Pro,<br>GPQA | DAPO<br>GRPO,                     |
| (2025)<br>et al.<br>Gao<br>SAPO                                                   | GRPO<br>GSPO,                    | Qwen3-30B-A3B-Base,<br>Qwen3-VL-30B-A3B                                                                        | Logic<br>Code,<br>Math,                                                                                                                                                                     | MathVision<br>MultiChallenge<br>BeyondAIME,<br>ZebraLogic,<br>HMMT25,<br>SimpleQA,<br>LiveCodeBench,<br>2025,<br>TAU-bench,<br>AIME                           | GRPO<br>GSPO,                     |
| (2025a)<br>et al.<br>Wang<br>80/20<br>Beyond                                      | DAPO                             | Qwen3-14B,<br>Qwen3-32B<br>Qwen3-8B,                                                                           | DAPO-Math-17K                                                                                                                                                                               | AMC,<br>Minerva,<br>2025,<br>AIME<br>MATH-500,<br>2024,<br>AIME                                                                                               | DAPO                              |
| (2025b)<br>et al.<br>Cui<br>& KL-Cov<br>Clip-Cov                                  | GRPO                             | Qwen2.5-32B<br>Qwen2.5-7B,                                                                                     | DAPO-Math-17K                                                                                                                                                                               | MATH-500,<br>OlympiadBench,<br>OlympiadBench<br>AMC,<br>Omni-MATH,<br>2024/25,<br>AIME                                                                        | Clip-higher<br>GRPO,              |
| (2025)<br>et al.<br>Lyu<br>OREAL                                                  | REINFORCE                        | DeepSeek-R1-Distill-Qwen-7B<br>Qwen2.5-32B,<br>Qwen2.5-7B,                                                     | competitions<br>MATH,<br>NuminaMath,<br>AMC/AIME                                                                                                                                            | LiveMathBench,<br>2024,<br>OlympiadBench<br>AIME<br>Minerva<br>MATH-500,<br>2025,<br>AIME                                                                     | PRIME<br>GRPO,<br>REINFORCE,      |
| (2025)<br>et al.<br>Zheng<br>GSPO                                                 | GRPO                             | Qwen3-30B-A3B-Base                                                                                             | + Code<br>Math                                                                                                                                                                              | LiveCodeBench,<br>Codeforces<br>2024,<br>AIME                                                                                                                 | GRPO                              |
| (2026)<br>et al.<br>Zhao<br>GMPO                                                  | GRPO                             | DeepSeek-R1-Distill-Qwen-7B,<br>Qwen2.5-VL-Instruct-7B<br>Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>Qwen3-32B, | CountDown,<br>Geometry3K<br>MATH,<br>DeepScaleR,                                                                                                                                            | MATH-500,<br>OlympiadBench,<br>Geometry3K<br>AMC,<br>2024,<br>Minerva,<br>AIME                                                                                | Dr.GRPO<br>GRPO,                  |
| (2026)<br>et al.<br>Chu<br>GPG                                                    | GRPO                             | DeepSeek-R1-Distill-Qwen-1.5B,<br>Qwen2.5-VL-3B-Instruct,<br>Qwen2.5-Math-7B,<br>Qwen2-VL-2B                   | Cars196,<br>set,<br>Pets37,<br>DAPO-Math-17K,<br>set<br>open-rs,<br>MATH-lighteval,<br>training<br>dataset,<br>training<br>FGVC-Aircraft,<br>Flower102,<br>open-s1,<br>SAT<br>GEOQA<br>LISA | LISA<br>MATH-500,<br>GEOQA,<br>Cars196,<br>Pets37,<br>OlympiadBench,<br>Minerva,<br>Flower102,<br>CV-Bench,<br>FGVC-Aircraft,<br>2024,<br>AMC,<br>AIME        | SFT<br>DAPO,<br>Dr.GRPO,<br>GRPO, |
| (2025)<br>Welleck<br>and<br>Aggarwal<br>LCPO                                      | GRPO                             | DeepScaleR-1.5B-Preview                                                                                        | DeepScaleR-Preview-Dataset                                                                                                                                                                  | AMC,<br>GPQA,<br>MMLU<br>MATH,<br>OlympiadBench,<br>LSAT,<br>2025,<br>AIME                                                                                    | forcing)<br>(budget<br>S1         |
| (2025a)<br>et al.<br>GRPO-λ Dai                                                   | GRPO                             | Qwen3-8B                                                                                                       | DeepMath-103K                                                                                                                                                                               | MATH-500,<br>OlympiadBench<br>AMC,<br>2024,<br>Minerva,<br>AIME                                                                                               | GRPO                              |
| (2025)<br>Zuo<br>and<br>Zhang<br>GRPO-LEAD                                        | GRPO                             | DeepSeek-R1-Distill-Qwen-7B,                                                                                   | DeepScaleR                                                                                                                                                                                  | LiveCodeBench<br>2025,<br>AIME<br>2024,<br>AIME                                                                                                               | GRPO                              |
| (2025a)<br>et al.<br>Wu<br>Ada-GRPO                                               | GRPO                             | DeepSeek-R1-Distill-Qwen-14B<br>Qwen2.5-Base-3B/7B/14B                                                         | (RL)<br>MATH<br>(SFT),<br>AQuA-Rat<br>GSM8K,<br>CSQA,                                                                                                                                       | BBH<br>SVAMP,<br>2025,<br>AIME<br>OBQA,<br>MATH,<br>CSQA,<br>GSM8K,                                                                                           | GRPO<br>SFT,                      |
| Gradient<br>Methods:<br>R<br>RLV<br>9:<br>Table                                   | fficient<br>Coe                  | papers).<br>(14<br>1<br>Part                                                                                   | innovating<br>Methods                                                                                                                                                                       | importance<br>on                                                                                                                                              | advantage<br>and<br>ratios        |

122

computation.

<span id="page-122-0"></span>

|                                    | (Methodology)<br>Over<br>Improve | Model<br>Base                                                                                                 | Data<br>Fine-tuning                                                                                             | Benchmarks<br>Evaluation                                                                                                         | With<br>(Methodology)<br>Compare                        |
|------------------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| et al. (2025)<br>Agarwal<br>Min    | REINFORCE                        | Llama-3.1-8B-Instruct<br>Eurus-2-7B-SFT,<br>Qwen2.5-Math-7B,                                                  | labels)<br>coding<br>no answer<br>+ Eurus-2<br>prompts,<br>NuminaMath<br>(unlabeled                             | 2024,<br>v2,<br>OlympiadBench,<br>LiveCodeBench<br>UGPhysics<br>AIME<br>AMC,<br>SciCode,<br>MATH-500,<br>Minerva,<br>LeetCode,   | SC-RL<br>GRPO,<br>RLOO,<br>SFT,                         |
| et al. (2025b)<br>Zhao<br>INTUITOR | GRPO                             | OLMo-2-1124-7B-SFT,<br>Llama3.2-3B-Instruct,<br>Qwen2.5-1.5B,<br>Qwen2.5-14B,<br>Qwen2.5-3B,<br>Qwen2.5-7B,   | Codeforces<br>MATH,                                                                                             | CRUXEval-O,<br>AlpacaEval<br>GSM8K,<br>MATH-500,<br>LiveCodeBench,<br>MMLU-Pro,                                                  | GRPO-PV<br>GRPO,                                        |
| et al. (2025)<br>Chen<br>Seed-GRPO | GRPO                             | DeepSeek-R1-Distill-Qwen-7B<br>Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>Qwen3-14B                            | 3–5)<br>(Level<br>MATH                                                                                          | Minerva,<br>AMC,<br>OlympiadBench<br>2024,<br>MATH-500,<br>AIME                                                                  | RAFT++<br>SRPO,<br>GPG,<br>DAPO,<br>GRPO,<br>Dr.GRPO,   |
| et al. (2025d)<br>Zhang            | GRPO                             | Qwen2.5-Math-1.5B-Base,<br>Qwen2.5-Math-7B-Base,<br>Qwen2.5-3B-Instruct,<br>Qwen2.5-7B-Instruct               | (500)<br>math),<br>TruthfulQA<br>(20K<br>NuminaMath-CoT<br>(10K),<br>TriviaQA                                   | AMC23,<br>2024,<br>TruthfulQA<br>AIME<br>MATH,<br>OlympiadBench,<br>Math,<br>TriviaQA,<br>Minerva                                | SFT<br>ODPO,<br>GRPO,                                   |
| et al. (2025a)<br>Cui              | RLOO                             | Qwen2.5-Math-7B-Base                                                                                          | Code-Feedback<br>MathInstruct,<br>NuminaMath,                                                                   | MATH-500,<br>LiveCodeBench<br>OlympiadBench,<br>AMC,<br>LeetCode,<br>2024,<br>Minerva,<br>AIME                                   | REINFORCE,<br>VinePPO<br>PPO,<br>GRPO,<br>SFT,<br>RLOO, |
| et al. (2025b)<br>Cheng            | RLOO                             | Qwen2.5-Math-7B,<br>Qwen2.5-7B,                                                                               | MATH                                                                                                            | Minerva,<br>AMC,<br>OlympiadBench<br>2024,<br>MATH-500,<br>AIME                                                                  | DPO<br>GRPO,<br>REINFORCE++,<br>RLOO,                   |
| et al. (2025)<br>Yuan              | PPO                              | Qwen2.5-Math-1.5B<br>Qwen2.5-32B-Base                                                                         | math<br>problems<br>hard<br>AIME<br>synthetic<br>Past<br>+                                                      | GPQA,<br>Codeforces<br>2024,<br>AIME                                                                                             | GRPO<br>PPO,                                            |
| et al. (2025)<br>Yue               | PPO                              | Qwen2.5-32B-Base                                                                                              | DAPO-Math-17K                                                                                                   | 2024<br>AIME                                                                                                                     | DAPO,<br>GRPO<br>PPO,                                   |
| et al. (2025b)                     | GRPO                             | Qwen2.5-1.5B-Base,<br>Qwen2.5-32B-Base<br>Qwen2.5-0.5B-Base,<br>Qwen2.5-7B-Base,                              | OpenR1-Math-220K,<br>tasks<br>NuminaMath,<br>+ synthesized<br>MATH,<br>MATH,<br>forum<br>AIME,<br>AoPS<br>Tulu3 | MMLU-Pro<br>MATH-500,<br>MMLU,<br>2025,<br>AIME<br>Diamond,<br>2024,<br>GPQA<br>AIME                                             | DAPO<br>GRPO,                                           |
| et al. (2025)                      | GRPO                             | DeepSeek-R1-Distill-Qwen-7B                                                                                   | Skywork-OR1-RL-Data                                                                                             | AIME<br>MATH-500,<br>2024,<br>AIME                                                                                               | SFT<br>GRPO,                                            |
| (2026)<br>Ding<br>and              | GRPO                             | Qwen3-8B                                                                                                      | subset)<br>DAPO<br>(English                                                                                     | HumanEval-Mul,<br>BeyondAIME,<br>2025<br>HMMT25<br>2025,<br>MATH-500,<br>BRUNO25,<br>AIME<br>2024,<br>2024,<br>AIME<br>AIME      | GRPO                                                    |
| (2025)<br>Team<br>Kimi             | REINFORCE                        | MM)<br>(proprietary<br>Base<br>k1.5<br>Kimi                                                                   | vision)<br>code,<br>(math,<br>prompts<br>RL<br>Proprietary                                                      | C-Eval<br>MathVision,<br>Codeforces,<br>CLUEWSC,<br>MMMU,<br>LiveCodeBench,<br>IFEval,<br>MathVista,<br>MMLU,                    | DPO<br>ReST,                                            |
| et al. (2025)<br>Zhu               | REINFORCE++,<br>GRPO<br>PPO,     | DeepSeek-R1-Distill-Qwen-7B<br>Qwen2.5-32B-Base,<br>Qwen2.5-7B-Base,                                          | DeepCoder<br>DAPO-Math-17K,                                                                                     | 2024/25,<br>OlympiadBench,<br>HumanEval+<br>AIME<br>LiveCodeBench,<br>AMC,<br>Codeforces,<br>Minerva,<br>MATH-500,               | REINFORCE++,<br>GRPO<br>PPO,                            |
| (2025)<br>Wang                     | GRPO                             | DeepSeek-LLM-7B-Chat,<br>Qwen2.5-32B-Instruct,<br>Qwen2.5-7B-Instruct,<br>Qwen2.5-32B-Base,<br>Qwen3-32B-Base | Infinity<br>MATH,<br>DAPO-Math-17K,<br>GSM8K,                                                                   | MBPP,<br>AIME,<br>Arena-Hard<br>Winogender,<br>MUSR,<br>BBQ,<br>MATH,<br>GPQA,<br>AlpacaEval,<br>TruthfulQA,<br>ARC-C,<br>GSM8K, | PPO<br>UNA,<br>DPO,<br>GRPO,                            |

# Table 10: RLVR Methods: Gradient Coefficient Part 2 (14 papers). Methods innovating on reward design, value baselines, and partition functions.

### RL for LLM Post-training survey

<span id="page-123-1"></span>

| Paper                                           | (Methodology)<br>Over<br>Improve             | Model<br>Base                                                                                                                         | Data<br>Fine-tuning                                                                                                  | Benchmarks<br>Evaluation                                                                                                                                                                              | With<br>(Methodology)<br>Compare                                    |
|-------------------------------------------------|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| (2025a)<br>et al.<br>Xiong<br>AAPO              | GPG<br>GRPO,                                 | DeepSeek-R1-Distill-Qwen-1.5B,<br>Llama-3.2-1B-Instruct,<br>Llama-3.2-3B-Instruct<br>Qwen2.5-Math-7B,                                 | simplelr_qwen_level3to5<br>open-rs,                                                                                  | AMC,<br>OlympiadBench<br>MATH-500,<br>2024,<br>Minerva,<br>AIME                                                                                                                                       | PRIME<br>GPG,<br>GRPO,                                              |
| (2025)<br>et al.<br>Fu<br>SRFT                  | GRPO<br>SFT,                                 | Qwen2.5-Math-7B                                                                                                                       | OpenR1-Math-46k-8192                                                                                                 | MMLU-Pro<br>MATH-500,<br>OlympiadBench,<br>Diamond,<br>AMC,<br>2024,<br>GPQA<br>Minerva,<br>AIME<br>ARC-C,                                                                                            | LUFFY<br>PPO,<br>GRPO,<br>SFT,                                      |
| (2025)<br>et al.<br>Lv<br>HPT                   | GRPO<br>SFT,                                 | Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>LLaMA-3.1-8B                                                                                | trajectories<br>solution<br>with<br>problems<br>Math                                                                 | AMC,<br>ARC-C<br>Minerva,<br>2025,<br>OlympiadBench,<br>Diamond,<br>AIME<br>MATH-500,<br>2024,<br>GPQA<br>AIME                                                                                        | SRFT,<br>→GRPO<br>GRPO,<br>LUFFY,<br>SFT,<br>SFT                    |
| (2025)<br>et al.<br>Xiao<br>BNPO                | REINFORCE++<br>REINFORCE,<br>GRPO,<br>ReMax, | Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B                                                                                                 | MATH                                                                                                                 | AMC,<br>2025,<br>MATH-500<br>AIME<br>2024,<br>AIME                                                                                                                                                    | REINFORCE<br>ReMax,<br>REINFORCE++,<br>GRPO,                        |
| (2026a)<br>et al.<br>Liu<br>GDPO                | GRPO                                         | DeepSeek-R1-Distill-Qwen-1.5B,<br>DeepSeek-R1-Distill-Qwen-7B,<br>Qwen2.5-1.5B-Instruct,<br>Qwen2.5-3B-Instruct,<br>Qwen3-4B-Instruct | (math),<br>xLAM<br>DeepScaleR-Preview-Dataset<br>(coding)<br>calling),<br>Hammar,<br>Eurus-2-RL<br>(tool<br>ToolACE, | MATH-500,<br>MATH,<br>OlympiadBench,<br>CodeContests,<br>TACO<br>AMC,<br>BFCL-v3,<br>2025,<br>Codeforces,<br>2024,<br>AIME<br>APPS,<br>Minerva,<br>AIME<br>2024,<br>AIME                              | GRPO                                                                |
| (2025a)<br>et al.<br>Hu<br>REINFORCE++          | REINFORCE                                    | Qwen2.5-Math-7B-Base,<br>Qwen2.5-7B-Base<br>Llama-3-8B-SFT,                                                                           | MATH<br>DAPO,<br>ORZ,<br>(RLHF),<br>prompts<br>diverse<br>20K                                                        | AMC,<br>CMIMC<br>Chat-Arena-Hard,<br>HMMT,<br>K&K,                                                                                                                                                    | ReMax<br>GRPO,<br>RLOO,<br>PPO,                                     |
| (2025)<br>et al.<br>Yu<br>DAPO                  | GRPO                                         | Qwen2.5-32B-Base                                                                                                                      | DAPO-Math-17K                                                                                                        | 2024<br>AIME                                                                                                                                                                                          | GRPO                                                                |
| (2025b)<br>et al.<br>Xiong<br>Reinforce-Rej     | REINFORCE                                    | Qwen2.5-Math-7B-Base,<br>LLaMA-3.2-3B-Instruct                                                                                        | NuminaMath                                                                                                           | Math,<br>OlympiadBench<br>Minerva<br>MATH-500,                                                                                                                                                        | DPO,<br>PPO<br>Iterative<br>GRPO,<br>RAFT++,<br>REINFORCE,<br>RAFT, |
| (2026b)<br>et al.<br>Liu<br>PPO<br>Lite         | DAPO<br>GRPO,                                | Qwen3-4B-Base,<br>Qwen3-8B-Base                                                                                                       | SimpleRL-Zoo-Data,<br>DeepMath-103K                                                                                  | OlympiadBench,<br>Minerva,<br>AIME<br>2024,<br>AMC,<br>MATH-500,<br>AIME                                                                                                                              | DAPO<br>GRPO,                                                       |
| (2025d)<br>et al.<br>Liu<br>Dr.GRPO             | GRPO                                         | Qwen2.5-Math-1.5B,<br>Qwen2.5-Math-7B,<br>Llama-3.2-3B                                                                                | MATH                                                                                                                 | 2025<br>Minerva,<br>AMC,<br>OlympiadBench<br>2024,<br>MATH-500,<br>AIME                                                                                                                               | PRIME<br>GRPO,                                                      |
| (2025a)<br>et al.<br>Liu<br>ProRL               | DAPO<br>GRPO,                                | DeepSeek-R1-Distill-Qwen-1.5B                                                                                                         | Gym,<br>Eurus-2-RL,<br>Llama-Nemotron<br>Reasoning<br>DeepScaleR,<br>SCP-116K,                                       | Minerva,<br>CodeContests,<br>LiveCodeBench,<br>Diamond,<br>Gym<br>MATH,<br>Reasoning<br>GPQA<br>APPS,<br>AMC,<br>TACO,<br>HumanEval+,<br>OlympiadBench,<br>2024/25,<br>IFEval,<br>Codeforces,<br>AIME | GRPO                                                                |
| (2025a)<br>et al.<br>Cheng<br>Explor<br>Entropy | GRPO<br>PPO,                                 | Qwen2.5-Math-Base-7B<br>Qwen2.5-Base-7B,                                                                                              | DAPO-Math-17K                                                                                                        | MATH-500<br>2024/25,<br>AIME<br>AMC,                                                                                                                                                                  | GPG<br>GRPO,<br>PRIME,<br>PPO,                                      |
| (2025)<br>et al.<br>He<br>MAGIC                 | GRPO                                         | DeepSeek-R1-Distill-Qwen-32B<br>DeepSeek-R1-Distill-Qwen-7B,                                                                          | Skywork-OR1-RL-Data                                                                                                  | 2025,<br>LiveCodeBench<br>AIME<br>2024,<br>AIME                                                                                                                                                       | GRPO                                                                |
|                                                 |                                              |                                                                                                                                       |                                                                                                                      |                                                                                                                                                                                                       |                                                                     |

Table 11: RLVR Methods: Gradient Coefficient Part 3 (13 papers). Methods innovating on advantage normalization, length scaling, and regularization.

# <span id="page-123-0"></span>Wang, Ramnath, et al.

<span id="page-124-0"></span>Appendix B. RLHF - detailed characterization of all papers

<span id="page-125-1"></span><span id="page-125-0"></span>

| Paper                                                         | Response          | Feedback<br>Type | Reward         | m<br>Training<br>Paradig | Entropy<br>Reg.     | Divergence<br>Reg. | Penalty<br>Length | Model<br>Ref. | SFT<br>Merge<br>w/ |
|---------------------------------------------------------------|-------------------|------------------|----------------|--------------------------|---------------------|--------------------|-------------------|---------------|--------------------|
| 2022b)<br>al.,<br>et<br>(Bai<br>RLAIF-Anthropic               | pairwise          | HF/AF            | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Lee<br>Google<br>RLAIF-               | pairwise          | AF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Mu<br>RLAIF-OpenAI                    | list              | HF/AF            | pointwise      | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Liu<br>RSO                            | pairwise          | HF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Yuan<br>Ms<br>L<br>Rewarding<br>Self- | pairwise          | AF               | pointwise      | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024c)<br>al.,<br>et<br>(Xu<br>RINGE<br>C                     | pairwise          | HF               | pairwise       | on-policy                | no                  | none               | no                | no            | yes                |
| 2025b)<br>al.,<br>et<br>(Wu<br>Ms<br>L<br>Rewarding<br>Meta-  | pairwise          | AF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Munos<br>NLHF                         | pairwise          | HF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2025c)<br>al.,<br>et<br>(Wu<br>SPPO                           | pairwise          | AF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Rosset<br>DNO                         | pairwise          | AF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2023)<br>al.,<br>et<br>(Rafailov<br>DPO                       | pairwise          | HF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2023)<br>al.,<br>et<br>(Zhao<br>SLiC-HF                       | pairwise          | HF               | pairwise       | offline                  | no                  | none               | no                | no            | yes                |
| 2024)<br>al.,<br>et<br>(Pal<br>maug)<br>(S<br>DPOP            | pairwise          | HF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2025)<br>al.,<br>et<br>m<br>(Ki<br>sDPO                       | pairwise          | HF               | pairwise       | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Wu<br>β-DPO                           | pairwise          | HF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Azar<br>IPO                           | pairwise          | HF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2025)<br>al.,<br>et<br>(Sun<br>RPO                            | pairwise          | AF               | pointwise      | on-policy                | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Tang<br>GPO                           | pairwise          | HF               | pairwise       | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2024a)<br>al.,<br>et<br>(Ethayarajh<br>KTO                    | single            | HF               | binary         | offline                  | no                  | RKL                | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>mond<br>(Riche<br>RO<br>D              | single            | HF               | binary         | offline                  | no                  | RKL                | no                | yes           | no                 |
| methods:<br>HF<br>RL<br>12:<br>Table                          | su<br>methodology | mary,<br>m       | 1–20<br>papers | O<br>(DP                 | through<br>baseline | Nash/self-play     |                   | variants).    |                    |

<span id="page-126-1"></span>

| Paper                                          | Response    | Feedback<br>Type | Reward    | m<br>Training<br>Paradig | Entropy<br>Reg. | Divergence<br>Reg.            | Penalty<br>Length | Model<br>Ref. | SFT<br>Merge<br>w/ |
|------------------------------------------------|-------------|------------------|-----------|--------------------------|-----------------|-------------------------------|-------------------|---------------|--------------------|
| 2024b)<br>al.,<br>et<br>(Ethayarajh<br>UNA     | single      | HF/AF            | pointwise | offline                  | no              | RKL                           | no                | yes           | no                 |
| 2023b)<br>al.,<br>et<br>(Yuan<br>RRHF          | list        | HF/AF            | list      | offline                  | no              | none                          | yes               | no            | yes                |
| 2024)<br>al.,<br>et<br>(Song<br>PRO            | list        | HF               | list      | offline                  | no              | none                          | no                | no            | yes                |
| 2025c)<br>al.,<br>et<br>(Liu<br>LiPO           | list        | HF               | list      | offline                  | no              | RKL                           | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Rafailov<br>DPO-r-to-Q | pairwise    | HF               | token     | offline                  | yes             | RKL                           | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Zeng<br>TDPO           | pairwise    | HF               | token     | offline                  | no              | FKL                           | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Duan<br>O<br>D2        | single      | HF               | negative  | on-policy                | no              | Divergence<br>Jeffrey         | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Zhang<br>NPO           | single      | HF               | negative  | offline                  | no              | RKL                           | no                | yes           | no                 |
| 2024b)<br>al.,<br>et<br>(Xu<br>CPO             | pairwise    | AF               | pairwise  | offline                  | no              | none                          | no                | no            | yes                |
| 2024)<br>al.,<br>et<br>(Wang<br>f-DPO          | pairwise    | HF               | pairwise  | offline                  | no              | others                        | no                | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Meng<br>mPO<br>Si      | pairwise    | HF               | pairwise  | offline                  | no              | none                          | yes               | no            | no                 |
| 2024)<br>al.,<br>et<br>(Park<br>R-DPO          | pairwise    | HF               | pairwise  | offline                  | no              | RKL                           | yes               | yes           | no                 |
| 2024)<br>al.,<br>et<br>(Hong<br>ORPO           | pairwise    | HF               | pairwise  | offline                  | no              | none                          | no                | no            | yes                |
| 2025b)<br>al.,<br>et<br>(Wang<br>UFT           | single      | HF/AF            | pointwise | offline                  | no              | RKL                           | no                | yes           | yes                |
| 2024)<br>al.,<br>et<br>(Pentyala<br>PAFT       | pairwise    | HF               | pairwise  | offline                  | no              | RKL                           | no                | yes           | yes                |
| methods:<br>HF<br>RL<br>13:<br>Table           | methodology | mary,<br>m<br>su | papers    | 21–35                    | (token-level    | SFT-<br>through<br>ward<br>re | merge             | variants).    |                    |

# <span id="page-126-0"></span>RL for LLM Post-training survey

<span id="page-127-1"></span>

| With<br>(Methodology)<br>Compare | RLHF,<br>RLHF<br>Helpful<br>HH                                                        | SFT<br>RLHF,                                                                                                | PPO,<br>Human-PPO<br>data)<br>Helpful-only<br>(safety                                                              | ReST<br>RAFT,<br>DPO,<br>SLiC,                                                             | GPT-4<br>SFT,<br>(M1),<br>DPO                                                                 | DPO<br>Iterative<br>Best-of-N,<br>SFT,<br>CRINGE,<br>Margin<br>Hard                  | GPT-4<br>SPPO,<br>(+LC),<br>LMs<br>Self-Rewarding         | Self-Play,<br>Best-Response<br>RLHF,<br>SFT,                                   | SFT<br>IPO,<br>DPO,                              | LM<br>Self-Rewarding<br>SPIN,<br>DPO,<br>SFT,           | SLiC<br>SFT,<br>PPO,                                                        | SFT<br>PPO/RLHF,                                  | SLiC-HF<br>IPO,<br>DPO,                                                         | SFT<br>DPO,                                                                                         | SPPO<br>KTO,<br>IPO,<br>DPO,                                     | DPO                                                                            | SFT<br>SimPO,<br>RLOO,<br>DPO,<br>KTO,                    | SLiC<br>variants)<br>IPO,<br>(GPO<br>DPO,                          | PPO,<br>SFT<br>CSFT,<br>offline<br>SLiC,<br>DPO,           | SFT<br>KTO,                                  |
|----------------------------------|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------|--------------------------------------------------------------------|------------------------------------------------------------|----------------------------------------------|
| Benchmarks<br>Evaluation         | Elo<br>eval<br>Elo,<br>(crowdworker),<br>Harmlessness<br>binary<br>Helpfulness<br>HHH | eval),<br>alignment,<br>(human<br>harmless<br>AI-labeler<br>rate<br>Win                                     | eval),<br>rate),<br>HellaSwag,<br>human<br>rate<br>(overrefusal<br>(safety<br>GPQA,<br>MMLU,<br>XSTest<br>WildChat | eval<br>human<br>2-L),<br>(PaLM<br>Lambada<br>AutoSxS<br>win rate,<br>reward<br>Proxy/Gold | eval<br>2.0,<br>human<br>AlpacaEval<br>pairwise                                               | CRINGE,<br>Binary<br>DPO,<br>PPO,<br>F1<br>Repeat@3-gram,<br>win rate,<br>AlpacaFarm | 2.0,<br>AlpacaEval<br>MT-Bench,                           | Arena-Hard<br>judge)<br>win rate<br>2 Large<br>AlpacaEval<br>Pairwise<br>(PaLM | 2.0,<br>Arena-Hard,<br>MT-Bench,<br>LLM<br>Open  | Leaderboard<br>2.0,<br>AlpacaEval                       | win rate,<br>win rate,<br>preference<br>MT-Bench<br>TL;DR<br>GPT-4<br>human | eval<br>win rate,<br>win rate,<br>Human<br>ranker | Leaderboard<br>ROUGE-1/2/L<br>MT-Bench,<br>LLM<br>Open                          | Leaderboard<br>TruthfulQA),<br>EQ Bench<br>HellaSwag,<br>MT-Bench,<br>LLM<br>(ARC,<br>MMLU,<br>Open | 2 (LC &WR)<br>win rate<br>TL;DR),<br>GPT-4<br>AlpacaEval<br>(HH, | experiments,<br>analysis<br>stability<br>preference<br>empirical<br>Controlled | & Win-Rate<br>AlpacaEval)<br>AvgReward<br>test,<br>(lmsys | vs. πref<br>judge),<br>(PaLM-2<br>rate<br>KL<br>Win                | MMLU<br>win rate,<br>divergence<br>BBH,<br>GPT-4<br>GSM8K, | win rate<br>judge)<br>Side-by-side<br>(PaLM2 |
| Data<br>Fine-tuning              | data<br>et al. 2022)<br>prompts<br>helpfulness<br>Red-team<br>(Ganguli<br>human<br>+  | (helpful),<br>(summary),<br>HH (harmless)<br>Preferences<br>TL;DR<br>Anthropic<br>Human<br>Reddit<br>OpenAI | human-labeled),<br>RL prompts<br>synthetic)<br>6.7K),<br>Safety-relevant<br>(Ps;<br>set (518<br>Gold               | TL;DR<br>Reddit<br>DRBR (6.7K×4<br>HH-RLHF,                                                | scoring<br>LLM-as-judge<br>prompts,<br>IFEval-style<br>pairs,<br>preference<br>Self-generated | PREF<br>AlpacaFarm<br>ConvAI2;<br>Talk,<br>Skill<br>Blended                          | pairs<br>preference<br>Self-generated<br>meta-judged<br>+ | annotations<br>summaries,<br>preference<br>TL;DR<br>Reddit<br>human            | via PairRM)<br>UltraFeedback<br>(AI-labeled      | prompts<br>teacher<br>UltraFeedback<br>GPT-4-Turbo<br>+ | responses<br>(Reddit)<br>HH,<br>Anthropic<br>TL;DR                          | summarization)<br>TL;DR<br>(Reddit                | DPO,<br>Orca-DPO-Pairs<br>UltraFeedback,<br>MetaMath                            | Cleaned<br>(multi-stage)<br>OpenOrca,<br>UltraFeedback                                              | TL;DR,<br>UltraChat-200k<br>HH-RLHF,                             | subset)<br>HH<br>Anthropic<br>(pairwise                                        | by<br>prompts,<br>lmsys-1M<br>AI-labeled<br>(120k         | Nemotron-4-340B-RM)<br>et al. 2020)<br>TL;DR<br>(Stiennon          | UltraFeedback<br>labels)<br>(binary                        | feedback)<br>UltraFeedback<br>(binary        |
| Model<br>Base                    | LM series<br>for<br>results)<br>52B<br>(1B–52B;<br>Anthropic<br>main                  | 2 XS<br>(policy)<br>PaLM                                                                                    | XSmall)<br>LLMs<br>(Large∼GPT-4,<br>OpenAI<br>Small,<br>Internal<br>Medium,                                        | (11B)<br>T5-XXL<br>(770M),<br>T5-large                                                     | LLaMA-2-70B                                                                                   | LLaMA-7B<br>GPT2-Medium,<br>OPT-1.3B,                                                | LLaMA-3-8B-Instruct                                       | summarization)<br>(S/L/XL)<br>T5X<br>(text                                     | Mistral-7B-Instruct-v0.2,<br>Llama-3-8B-Instruct | Orca-2-7B,<br>Mistral-7B                                | Pythia-2.8B,<br>LLaMA-7B,<br>GPT-J-6B                                       | (770M),<br>(11B)<br>T5-XXL<br>T5-Large            | (Smaug-72B)<br>(Smaug-34B),<br>LLaMA-2-7B,<br>Mistral-7B,<br>Qwen-72B<br>Yi-34B | SOLAR-10.7B,<br>Mistral-7B                                                                          | Pythia-410M/1.4B/2.8B,<br>Llama3-8B<br>Mistral-7B,               | datasets<br>Synthetic                                                          | LLaMA-3-70B<br>LLaMA-3-8B,                                | task,<br>LM<br>setup)<br>(summarization<br>Unspecified<br>internal | LLaMA-7B/13B/30B,<br>Pythia-1.4B–12B,<br>Mistral-7B        | (770M),<br>(3B)<br>T5-XL<br>T5-L             |
| (Methodology)<br>Over<br>Improve | RLHF-Anthropic                                                                        | RLAIF-Anthropic                                                                                             | (helpful-only)<br>RLHF/PPO                                                                                         | DPO<br>SLiC,                                                                               | DPO<br>Offline                                                                                | CRINGE<br>Binary                                                                     | LMs<br>Self-Rewarding                                     | RLHF/PPO                                                                       | RLHF<br>Nash                                     | DPO<br>RLHF,<br>Nash                                    | RLHF/PPO                                                                    | PPO/RLHF                                          | DPO                                                                             | DPO                                                                                                 | DPO                                                              | DPO                                                                            | DPO                                                       | SLiC<br>IPO,<br>DPO,                                               | DPO                                                        | KTO                                          |
| Paper                            | et al., 2022b)<br>(Bai<br>RLAIF-Anthropic                                             | et al., 2024)<br>(Lee<br>RLAIF-Google                                                                       | et al., 2024)<br>(Mu<br>RLAIF-OpenAI                                                                               | et al., 2024)<br>(Liu<br>RSO                                                               | et al., 2024)<br>(Yuan<br>LMs<br>Self-Rewarding                                               | et al., 2024c)<br>(Xu<br>CRINGE                                                      | et al., 2025b)<br>(Wu<br>LMs<br>Meta-Rewarding            | et al., 2024)<br>(Munos<br>NLHF                                                | et al., 2025c)<br>(Wu<br>SPPO                    | et al., 2024)<br>(Rosset<br>DNO                         | et al., 2023)<br>(Rafailov<br>DPO                                           | et al., 2023)<br>(Zhao<br>SLiC-HF                 | et al., 2024)<br>(Pal<br>(Smaug)<br>DPOP                                        | et al., 2025)<br>(Kim<br>sDPO                                                                       | et al., 2024)<br>(Wu<br>β-DPO                                    | et al., 2024)<br>(Azar<br>IPO                                                  | et al., 2025)<br>(Sun<br>RPO                              | et al., 2024)<br>(Tang<br>GPO                                      | et al., 2024a)<br>(Ethayarajh<br>KTO                       | et al., 2024)<br>(Richemond<br>DRO           |

| variants).     |
|----------------|
|                |
|                |
|                |
| Nash/self-play |
|                |
|                |
| through        |
|                |
| baseline       |
| O              |
|                |
| (DP            |
| 1–20.          |
|                |
| papers         |
| mary,          |
|                |
| m<br>su        |
|                |
| mental         |
|                |
| experi         |
|                |
| methods:       |
|                |
| HF             |
| RL             |
| 14:            |
| Table          |
|                |

<span id="page-127-0"></span>Wang, Ramnath, et al.

<span id="page-128-1"></span><span id="page-128-0"></span>

| (Methodology)<br>Over<br>Improve | Model<br>Base                                        | Data<br>Fine-tuning                                                                                                                            | Benchmarks<br>Evaluation                                                                                                                                            | With<br>(Methodology)<br>Compare                                                                                                                                                                                                     |
|----------------------------------|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| KTO<br>DPO,                      | Mistral-7B-v0.1,                                     | HelpSteer2                                                                                                                                     | 2.0,<br>MT-Bench,<br>AlpacaEval<br>LLM                                                                                                                              | PPO<br>KTO,<br>DPO,                                                                                                                                                                                                                  |
| PPO/RLHF                         | LLaMA-7B,                                            | Alpaca<br>HH,<br>Anthropic<br>Stanford                                                                                                         | score,<br>human<br>model<br>preference<br>PPL,<br>reward                                                                                                            | SFT,<br>Best-of-n<br>PPO,                                                                                                                                                                                                            |
|                                  | LLaMA-7B                                             |                                                                                                                                                | score,<br>model<br>reward<br>human<br>BLEU,                                                                                                                         | SFT<br>RRHF,<br>PPO,                                                                                                                                                                                                                 |
| DPO                              | (770M),<br>T5-XXL<br>T5-large                        | TL;DR,<br>HH<br>Anthropic<br>Reddit                                                                                                            | rate,<br>win<br>Human<br>model<br>AutoSxS,<br>Reward                                                                                                                | list-MLE<br>PRO,<br>SLiC,<br>DPO,                                                                                                                                                                                                    |
| DPO                              | 2.8B<br>Pythia                                       | (Reddit)<br>TL;DR                                                                                                                              | analysis,<br>(TL;DR),<br>reward<br>rate<br>win<br>token-level<br>GPT-4                                                                                              | SFT<br>DPO,                                                                                                                                                                                                                          |
| DPO                              | Large,<br>GPT-2                                      | IMDb,                                                                                                                                          | metrics,<br>win<br>(GPT-4<br>diversity<br>MT-Bench<br>Output                                                                                                        | PPO<br>SFT,<br>f-DPO,<br>DPO,                                                                                                                                                                                                        |
| DPO                              | Qwen2-1.5B<br>Phi-3-mini,                            | PKU-SafeRLHF                                                                                                                                   | MMLU<br>vs. Alpaca,<br>Rate<br>Win<br>GR2,<br>GR1,<br>Helpfulness,                                                                                                  | SFT<br>GA,<br>SimPO,<br>SliC-HF,<br>IPO,<br>DPO,                                                                                                                                                                                     |
| Ascent<br>Gradient               | Llama-2-7B-chat                                      | persona<br>TOFU<br>(fictitious                                                                                                                 | Model<br>Quality,<br>Forget<br>TOFU                                                                                                                                 | Ascent,<br>KTO<br>Gradient<br>DPO,                                                                                                                                                                                                   |
| for MT<br>+ RLHF                 | ALMA-13B<br>ALMA-7B,                                 | preferences<br>pairs<br>translation<br>AI-labeled<br>WMT<br>+                                                                                  | BLEURT,<br>sets<br>test<br>COMET,<br>WMT                                                                                                                            | MT,<br>supervised<br>DPO<br>ALMA,                                                                                                                                                                                                    |
| only)<br>(RKL<br>DPO             | GPT-2-large,                                         | HH-RLHF,<br>IMDB-sentiment                                                                                                                     | trade-off,<br>Reward–diversity                                                                                                                                      | PPO<br>DPO,                                                                                                                                                                                                                          |
| DPO                              | LLaMA-3-8B,<br>Gemma-2-9B<br>Mistral-7B,             | Cleaned<br>UltraFeedback                                                                                                                       | rate),<br>win<br>2.0 (LC<br>MT-Bench,<br>AlpacaEval                                                                                                                 | R-DPO<br>ORPO,<br>KTO,<br>CPO,<br>IPO,<br>DPO,<br>SLiC-HF,<br>RRHF,                                                                                                                                                                  |
| DPO                              |                                                      | HH,<br>Anthropic                                                                                                                               | (length-controlled),<br>win<br>AlpacaEval                                                                                                                           | SFT<br>DPO,                                                                                                                                                                                                                          |
| + SFT                            | Mistral-7B<br>LLaMA-2-7B,<br>(2.7B),<br>Phi-2        | UltraFeedback<br>HH,<br>Anthropic                                                                                                              | IFEval<br>MT-Bench,<br>1.0/2.0,<br>AlpacaEval                                                                                                                       | PPO<br>DPO,<br>SFT,                                                                                                                                                                                                                  |
| + DPO                            | Qwen-32B<br>Mistral-7B,                              | HelpSteer2<br>(SFT),                                                                                                                           | MT-Bench,<br>2.0,<br>LLM<br>AlpacaEval                                                                                                                              | KTO<br>DPO,<br>SFT,                                                                                                                                                                                                                  |
| (sequential)<br>+ DPO            | Llama-3-8B<br>Mistral-7B,                            | (SFT),<br>UltraFeedback<br>UltraChat                                                                                                           | AlpacaEval,<br>LLM<br>Open                                                                                                                                          | KTO<br>DPO,<br>SFT,                                                                                                                                                                                                                  |
|                                  |                                                      |                                                                                                                                                |                                                                                                                                                                     |                                                                                                                                                                                                                                      |
|                                  | (sequential)<br>(sequential)<br>(bandit)<br>PPO/RRHF | Mistral-7B-v0.1-Inst<br>MT)<br>(11B)<br>Pythia-2.8B<br>Pythia-2.8B<br>Pythia-2.8B<br>Alpaca-7B<br>(LLaMA-based<br>Alpaca-7B,<br>OPT-125M–1.3B, | (alignment)<br>ALMA-13B-LoRA)<br>dataset<br>data)<br>summarization<br>(DPO)<br>lists)<br>HH-RLHF<br>HH-RLHF<br>(Wombat)<br>(ranked<br>TL;DR<br>(GPT-4,<br>UltraChat | Utility<br>rate)<br>Leaderboard<br>Leaderboard<br>Leaderboard<br>Arena-Hard<br>eval<br>SxS<br>rate<br>En↔Zh)<br>rate<br>eval<br>preference<br>win<br>MT-bench<br>search<br>(En↔De,<br>TL;DR<br>beam<br>Open<br>Open<br>Harmlessness, |

![](./assets/01-rl-post-training-survey/_page_128_Figure_1.jpeg)

# [Table Of Contents](#page-1-0) ↑