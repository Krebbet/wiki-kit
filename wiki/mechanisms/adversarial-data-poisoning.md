# Adversarial Data Poisoning

Adversarial data poisoning is the class of attacks where actors inject, modify, or delete training data to shift a deployed model's behaviour toward the attacker's goal. This page anchors the reference-layer evidence on **poisoning attacks against recommender systems** and **algorithmic collective action** — the two literatures most relevant to consumer-side counter-power against dynamic-pricing and surveillance-pricing models. Both literatures describe the same technical primitive — coordinated data modification at scale — but frame it differently: the RS literature treats it as an *adversary* to defend against; the collective-action literature treats it as *users reclaiming influence over models trained on their data*. See [[obfuscation]] for the client-side tool variant.

## Two framings of the same mechanism

| Framing | Actor | Goal | Defender treats as... |
|---|---|---|---|
| **Poisoning attack** (RS / ML security literature) | "Malicious" external actor | Promote / demote items, degrade system | Threat — design detectors + robust training |
| **Algorithmic Collective Action** (ACA literature) | Users of the platform, coordinating | Shift model behaviour to reflect user goals | Framed as "response from below"; platform may still treat it as a threat |

Solanki et al. 2025 explicitly note ACA is "a 'response from below' strategy" (§6.5, quoting DeVrio et al. 2024) that "allows collectives to influence the outcomes of algorithmic systems and mitigate harms without directly relying on service providers."

## Taxonomy of poisoning attacks (Wang et al. 2024)

Wang, Gao, Yu, Ma, Yin & Sadiq — *Poisoning Attacks against Recommender Systems: A Survey* (arXiv 2401.01527). 45 papers reviewed from IJCAI, CIKM, KDD, WWW, SIGIR, WSDM, TKDE, and arXiv. Accompanying benchmark library: ARLib (15+ PAR models).

The survey's top-level taxonomy has three dimensions (§1, Figure 1). Quotes are direct extractions from the paper.

### A. Component-Specific Attacks

> "The distinct characteristics of these essential components potentially give rise to varied forms of poisoning attacks... including input data, recommender architectures, and optimization processes."

- **Input-Specific.** Attacks on the data modality: interaction records, graph structure, knowledge graphs, temporal sequences, images, text. Named methods: *GraphAttack*, *KGAttack*, *PoisonRec* (uses reinforcement learning to model user sequences as a Markov Decision Process), *PSMU* and *IPDGI* (use guided diffusion models to generate adversarial images for item promotion).
- **Recommender-Specific.** Attacks tailored to RS architecture. Named methods: *TNA* (matrix factorization), *NCFAttack* (neural collaborative filtering), *GOAT*, *GSPAttack* (GNN), *SSLAttack* ("shifting the focus of the PAR to the initial pre-training phase"), *FedRecAttack* (federated RS), *H-CARS* ("leverages counterfactual explanations to craft malicious user profiles", explainable RS).
- **Optimization-Specific.** "The optimization process in RS draws less attention from attackers. However, recent research found that this aspect can be particularly vulnerable." *PipAttack* exploits Bayesian Personalized Ranking loss; *CLeaR* exploits contrastive-learning loss uniformity.

### B. Goal-Driven Attacks

- **System Degradation (untargeted).** "Strategically designed to disrupt the overall functionality of RS, affecting all recommendation results. The ultimate goal is to deteriorate the user experience and potentially inflict substantial financial losses." *ClusterAttack* clusters item embeddings into dense groups to disrupt ranking; *FedAttack* selects "globally 'hardest items'" as adversarial samples.
- **Targeted Manipulation.** "Elaborately tailored to either promote or demote specific items within distinct user groups or all users." *AutoAttack* "crafts malicious user profiles that closely mimic the attributes and interactions of the targeted user group... minimizing unintended effects on other users."
- **Hybrid-Goal.** "Attackers might design more flexible attack strategies, aligning with multiple objectives." Pioneer method *SGLD* (Li et al., 2016): "maximizing the discrepancy in all predictions before and after the poisoning attack (system degradation) and enhancing the prediction likelihood of a target item for each user (targeted manipulation)."

### C. Capability-Probing Attacks

This dimension is where the attacker's knowledge / resources / visibility constraints are framed.

- **Knowledge-Constrained.** "Assuming RS as a box, attackers' knowledge of the victim RS can be classified into three settings: white-box, gray-box, and black-box. These settings range from full access to RS, to partial system access, to scenarios where attackers only have limited interaction information and no prior knowledge of the recommendation model." *CovisitationAttack* (Yang et al., 2017) "theoretically evaluates three levels of attacker knowledge... and develops different PAR strategies tailored to each level."
- **Cost-Efficient.** "Each instance of manipulated or injected malicious data entails a specific cost... The optimization of PAR to achieve maximum attack effectiveness while minimizing associated costs is a critical objective." *SUI-Attack* demonstrates attack "in which an attacker can only inject a single user."
- **Invisibility-Assured.** "Executing PAR effectively necessitates careful consideration of the invisibility of malicious profiles." *AdvAttack* (Christakopoulou et al., 2019) is "the pioneering study that integrates adversarial learning into PAR." GANs (*AUSH*, *LegUP*, *GOAT*, *GSPAttack*) "engage in a competitive interaction to enhance the resemblance of generated user profiles to real user profiles." *RecUP* and *GSA-GANs* "employ state-of-the-art malicious user detection methods to evaluate whether generated fake users can evade detection mechanisms" — i.e., the detection model is used as the discriminator in the attack-generation GAN.

## Defences — what Wang et al. 2024 notes in passing

The Wang et al. survey is explicitly attack-focused and does not contain a defence taxonomy. The paper positions itself: "while there are surveys investigating trustworthy (Fan et al., 2022) or robust (Anelli et al., 2021) RS, they primarily orient their focus towards defence mechanisms, leading to a deficit in specialization in the attack strategies." This wiki page therefore does not claim defence coverage from this source.

What the paper does state about the defender–attacker dynamic:

- Heuristic attacks "lacked adaptability, rendering them detectable to defense measures once their patterns are deciphered" (§2.2, citing Wang et al. 2022).
- ARLib "provides a comprehensive suite of evaluation metrics to assess the threat of PAR models and the robustness of recommendation models against diverse poisoning attacks" (§1) — but specific metrics are not named in the paper text; the comparative findings are deferred to ARLib's online findings page.
- The future-work list (§6) includes "counteractive data neutralization... the injection of counteractive data into RS to counterbalance the negative impact of poisoning data... has been relatively unexplored in the context of PAR" — naming this as an open research direction rather than a deployed defence.

## The arms-race framing (Wang et al. 2024, introduction)

> "The latest trajectory of research on the PAR is **intrinsically aligned with the iterative advancements in recommendation techniques**. The evolution from factorization-based... to network-based, and currently to the cutting-edge large language model (LLM)-based recommendations... not only yields more precise recommendation outcomes but also introduces a range of new vulnerabilities."

Five open-problem directions the survey identifies (§6):

1. Novel victim contexts — multimodal, LLM-based, SSL-based RS. "Each novel victim context introduces unique characteristics and vulnerabilities."
2. Sophisticated attacker intent — cross-platform manipulation, cultural attacks on multilingual RS.
3. Missing theoretical foundation — "there is a lack of in-depth study on the underlying principles of PAR... the exact nature and dynamics [of cost-vs-impact tradeoffs] remain unclear."
4. Long-term impact gap — "As RS evolve with accumulating data and ongoing model updates, the initial impact of injected poisoning data may diminish or become diluted over time."
5. Counteractive data neutralization — as above.

## Algorithmic Collective Action — Solanki et al. 2025

Solanki, Bhange, Aïvodji & Creager — *Crowding Out The Noise: Algorithmic Collective Action Under Differential Privacy* (arXiv 2505.05707). Builds on Hardt et al. 2023's ACA framework and extends it to the setting where the model is trained with Differentially Private SGD (DPSGD).

### Core definitions (quoted)

> "A group of individuals, through coordinated changes in their data, can impact the behavior of deployed models. The size of the collective is represented by a parameter α > 0, which denotes the proportion of individuals within the data drawn from the base distribution P₀" (§2.1, citing Hardt et al. 2023).

The canonical strategy is the **feature-label strategy**:

> "The collective modifies both the features and labels for all data under their control... The data is modified in such a way that the classifier *f* learns to associate the transformed version of features with the chosen target label *y**, where the transformation is defined by the function *g: X → X*, resulting in the strategy *h(x, y) = (g(x), y**)*" (§2.1).

Success metric (empirical): "collective's success is defined in terms of how the model's predictions agree with the collective's chosen target label for evaluation data where the signal has been planted" — S(α) = Pr_{x∼P₀}[f(g(x)) = y*] (§4.1).

Critical mass: "the smallest size of the collective that can achieve a desired level of success... the smallest value α such that S(α) ≥ S*" (§2.1).

### Key theoretical results

- **Theorem 1 (from Hardt et al., reproduced §2.1).** Collective success after T training steps is lower-bounded by −(1 − ηC(α))^T ‖θ₀ − θ*‖, where C(α) is directly proportional to α. "As α increases... the lower bound on the collective's success also increases."
- **Theorem 2 (§3, new).** Under DPSGD, an additional negative term appears, driven by the noise multiplier σ and clipping threshold C:

  S_T(α, σ, C) ≥ −(1 − ηB(α,C))^T ‖θ₀ − θ*‖ − σC · f₁(B, T, η) · f₂(d, δ)

  The authors conclude: "the success of the collective is inversely proportional to noise scale σ" (§3).
- **Privacy → larger critical mass.** "As the privacy loss decreases (corresponding to higher privacy), the critical mass required for the success increases... when a firm deploys a model that prioritizes privacy at the expense of accuracy, it negatively raises the threshold for effective collective action" (§4.3).
- **Clipping threshold C — ambiguous.** Unlike σ, C has "competing influences": it increases B(α, C) (helping the first term) but linearly amplifies the noise term. "The overall impact of the clipping threshold C on the success of the collective is determined by the interplay between these competing influences" (§3).

### Empirical validation (§4.2–4.3)

| Dataset | Model | Signal function g | Main result |
|---|---|---|---|
| MNIST | ResNet18 (private from scratch) | Pixel patch | Higher privacy requires larger α to reach ~100% success |
| CIFAR-10 | ResNet18 pretrained on CIFAR-100 (private fine-tuning) | Grid pixel perturbation | Same pattern |
| Bank Marketing | Feedforward NN, tabular | Feature offset | Same pattern |

Tested at C = 1, 5, 10. All three datasets show the qualitative relationship that Theorem 2 predicts.

### Side result — ACA improves empirical privacy (§4.4)

> "Collective action during training improves empirical privacy by increasing the robustness to MIA (pushing MIA success close to 50%, or random chance), even for models trained without DP."

On CIFAR-10 (LiRA membership-inference attack), a collective of α = 1% reduces attack AuC from 81.78% (no collective, no DP) to ~50.23% (Table 1). The coordinated data modifications that planted the collective's signal also washed out the per-member signal adversaries exploit in MIA.

### Strategic implications the authors draw

> "These findings reveal a trade-off between differential privacy and algorithmic collective action. While stricter privacy protections are beneficial from regulatory or accountability perspectives, they increase the burden on groups of individuals adversely affected by model outcomes who aim to influence the model's behavior" (§4.3).

> "Firms may also strategically adopt such privacy-preserving techniques not only to protect individual data but also to weaken the influence of groups acting on their learning algorithm" (§6.5).

> "Paradoxically, knowing that DP is used could empower collective action. If individuals believe that their actions are masked by DP, they may be more willing to participate in collective action" (§6.5).

### Author-stated limitations

No explicit limitations section. In §6.3 the authors note the feature-label strategy "offers only empirical, not formal, privacy protection." In §6.4 they note experiments cover only "private training from scratch" (MNIST) and "private fine-tuning" (CIFAR-10) and flag open questions about where ACA is most effective in pre-train/fine-tune pipelines.

## Relevance for consumer-side counter-power

*(editorial / synthesis — the captured sources do not explicitly target consumer pricing.)*

The Wang et al. attack taxonomy and the Solanki et al. ACA formalism together define the design space for [[possible-strategic-levers|strategic levers #9, #10, #11]]:

- Wang et al.'s **Invisibility-Assured** category (GAN-based profile generators calibrated against state-of-the-art detectors) is the template for a consumer-collective that wants to inject behaviour indistinguishable from legitimate user behaviour.
- Solanki et al.'s **feature-label strategy** (choose *g* and *y**; scale *α*) is the template for how a consumer collective would specify what signal to plant and what outcome to force. The critical-mass result (\~% of user base) is the key empirical question for any concrete plan.
- Solanki et al.'s **DP-as-firm-weapon** result is a live strategic hazard: a pricing operator adopting DP for ostensibly privacy-preserving reasons is also neutralising consumer collective action. Builders should watch for this positioning in pricing-algorithm regulatory discourse.

## Source

- `raw/research/obfuscation-deep-dive/03-08-poisoning-recsys-survey.md` — Wang et al., *Poisoning Attacks against Recommender Systems: A Survey*, arXiv 2401.01527. Origin: academic survey. Trust: high for attack literature; explicitly does not cover defences.
- `raw/research/obfuscation-deep-dive/02-07-crowding-out-noise-aca-dp.md` — Solanki, Bhange, Aïvodji & Creager, *Crowding Out The Noise: Algorithmic Collective Action Under Differential Privacy*, arXiv 2505.05707. Origin: academic ML. Trust: high; theoretical bounds + empirical validation.

## Related

- [[obfuscation]]
- [[browser-fingerprinting]]
- [[collective-bargaining-for-data]]
- [[data-cooperatives]]
- [[algorithmic-collusion]]
- [[possible-strategic-levers]]
- [[obfuscation-strategic-readout]]
