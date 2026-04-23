# Wiki Index

Research wiki for the development of a novel fine-tuning method for small LLMs (1–40B params) emphasising single-sample, concept-based learning. Catalog of all pages in this wiki. Updated on every ingest.

---

## Research themes

| Theme | Summary |
|---|---|
| [[research/single-sample-rl-finetuning/_overview]] | Empirical and mechanistic account of one-example RLVR on capable base LLMs — post-training amplifies latent reasoning rather than installing new skills. |
| [[research/rlvr-mechanics/_overview]] | GRPO, sparse-subnetwork effects of RL, and information-gain process rewards — the mechanics under RLVR, where the sample-efficiency bottleneck is the reward, not the optimiser. |
| [[research/process-reward-models/_overview]] | Step-level credit assignment: PRM800K, Math-Shepherd, process- vs outcome-based feedback, GSM8K verifiers. |
| [[research/self-improvement/_overview]] | Models training on self-generated data: STaR, Self-Rewarding LM, rStar-Math. |
| [[research/critique-self-correction/_overview]] | Textual critiques as a substitute for dense labels: Self-Refine, Reflexion, Constitutional AI. |
| [[research/in-context-learning-theory/_overview]] | Mechanistic accounts of ICL (induction heads, gradient-descent, Bayesian, function-class) — the closest analogue to "single example imprints a concept" without weight updates. |
| [[research/meta-learning-few-shot/_overview]] | Pre-LLM foundations for few-shot learning: MAML, Prototypical Networks, one-shot prior-engineering. |
| [[research/test-time-training/_overview]] | Adaptation at deployment: per-input TTT fine-tunes and Algorithm Distillation's in-context RL. |
| [[research/concept-learning/_overview]] | Operational definitions of "concept": Concept Bottleneck Models (supervised, fixed vocabulary) and Recursive Concept Evolution (self-supervised, dynamic, low-rank library). |
| [[research/teacher-student-rl/_overview]] | Teacher-for-student-learning as an optimisation problem: Fan L2T, Saha LLM-teacher-explanations, Ho Fine-tune-CoT, TRICE, SOAR bilevel meta-RL, Sakana RLT, PM4GRPO. |
| [[research/rl-optimizers/_overview]] | RL-for-LLM optimiser lineage: PPO → InstructGPT → DPO → GRPO → post-GRPO (DAPO, Dr. GRPO, GSPO) + siblings RLOO, KTO. Critic-free, KL placement, length-bias convergence, preference-vs-RLVR subtrees. |
| [[research/catastrophic-forgetting/ewc-gemma2-cpt]] | Seed entry for the catastrophic-forgetting theme: EWC + Fisher applied to Gemma2 continual pretraining. |
| [[research/data-efficient-survey/limited-data-ft-survey]] | Szep et al. 2024 survey mapping PEFT, domain/cross-lingual adaptation, specialisation, and preference alignment under 10²–10⁵ label budgets. |

---

## Pages by theme

### Single-sample RL fine-tuning

| Page | Summary |
|---|---|
| [[research/single-sample-rl-finetuning/_overview]] | Theme overview and cross-cutting synthesis. |
| [[research/single-sample-rl-finetuning/1-shot-rlvr]] | Wang et al. — Qwen2.5-Math matches full-set RLVR on MATH500 from a single well-chosen training example. |
| [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] | Shao et al. — RLVR selects for correct-reasoning CoT priors already present in the base model. |
| [[research/single-sample-rl-finetuning/deepseek-r1]] | DeepSeek-R1 — RL-only post-training pipeline with distillation to small models. |
| [[research/single-sample-rl-finetuning/critique-ft-one-problem]] | Single-problem critique fine-tuning as an SFT alternative to RLVR. |
| [[research/single-sample-rl-finetuning/data-efficiency-rft]] | Difficulty-targeted online data selection and rollout replay. |
| [[research/single-sample-rl-finetuning/reft]] | ReFT — SFT warm-up + PPO on multiple sampled CoT paths per problem; +10–12% over SFT on math without external RM. |

### RLVR mechanics

| Page | Summary |
|---|---|
| [[research/rlvr-mechanics/_overview]] | Theme overview — reward is the bottleneck, not the optimiser. |
| [[research/rlvr-mechanics/deepseekmath-grpo]] | GRPO: critic-free, group-relative PPO; unified gradient view of SFT/RFT/DPO/PPO/GRPO. |
| [[research/rlvr-mechanics/rl-sparse-subnetwork]] | Balashov — RL updates only 5–30% of weights across seven algorithms; subnetwork-only retraining matches full. |
| [[research/rlvr-mechanics/learning-to-think]] | L2T — episodic GRPO with label-free information-gain process reward via Fisher/SVD. |
| [[research/rlvr-mechanics/structured-fisher-optimizer]] | Gong et al. — structured FIM approximation (RACS, Alice) unifying Adam/Shampoo/grad-norm; 2× Adam speedup at LLaMA scale. |

### Process reward models

| Page | Summary |
|---|---|
| [[research/process-reward-models/_overview]] | Theme overview of step-level credit assignment. |
| [[research/process-reward-models/lets-verify-step-by-step]] | Lightman et al. (PRM800K) — human step-labels beat outcome supervision on MATH. |
| [[research/process-reward-models/math-shepherd]] | Automated step labels from rollout success rate, no human annotation. |
| [[research/process-reward-models/process-outcome-feedback]] | Uesato et al. — process feedback reduces reasoning errors even when outcome accuracy matches. |
| [[research/process-reward-models/training-verifiers-gsm8k]] | Cobbe et al. — GSM8K + token-level verifier reranking. |
| [[research/process-reward-models/pav-rewarding-progress]] | Setlur et al. — PAV: process advantage as step-level *progress* under a complementary prover; >8% search gain, 5–6× RL efficiency over outcome RM. |

### Self-improvement

| Page | Summary |
|---|---|
| [[research/self-improvement/_overview]] | Theme overview — where does supervision come from with no external teacher. |
| [[research/self-improvement/star]] | STaR — rationalise-then-SFT on self-generated correct reasoning. |
| [[research/self-improvement/self-rewarding-lm]] | LLM-as-judge on its own outputs; iterated DPO. |
| [[research/self-improvement/rstar-math]] | Small LLMs + MCTS + self-evolved PRM reach SOTA math reasoning. |
| [[research/self-improvement/multi-turn-policy-verifier]] | PAG — single LLM alternates policy/verifier roles in multi-turn RL; selective revision avoids collapse; 65.2% MATH500 at 1.5B. |

### Critique and self-correction

| Page | Summary |
|---|---|
| [[research/critique-self-correction/_overview]] | Theme overview — textual critique substitutes for additional supervised data. |
| [[research/critique-self-correction/self-refine]] | Same-model critique-then-revise loop at inference time. |
| [[research/critique-self-correction/reflexion]] | Verbal RL: store episodic natural-language reflections in memory. |
| [[research/critique-self-correction/constitutional-ai]] | RLAIF with a small principle set replaces human harmlessness labels. |
| [[research/critique-self-correction/prometheus-2]] | Open-source 7B/8x7B evaluator LM unifying direct + pairwise assessment via weight merging; r=0.685 on MT Bench. |
| [[research/critique-self-correction/critic-tool-interactive]] | CRITIC — frozen LLM + external tool feedback for self-correction; +10pp over ReAct on AmbigNQ; tools are necessary, self-only degrades. |
| [[research/critique-self-correction/critic-cot]] | Critic-CoT — SFT on weak-supervision critique-refine pairs trains System-2 step-wise critique; 93.3% GSM8K, 57.8% MATH500. |

### In-context learning theory

| Page | Summary |
|---|---|
| [[research/in-context-learning-theory/_overview]] | Theme overview — three compatible accounts of what ICL is. |
| [[research/in-context-learning-theory/induction-heads]] | Circuit-level story: `[A][B]…[A]→[B]` copy heads emerge and predict ICL capability. |
| [[research/in-context-learning-theory/icl-as-gradient-descent]] | Linear attention implements gradient descent on an implicit in-context loss. |
| [[research/in-context-learning-theory/icl-bayesian-inference]] | Distributional-level story: ICL is posterior inference over latent pretraining concepts. |
| [[research/in-context-learning-theory/function-class-icl]] | Transformers trained from scratch in-context learn linear / sparse / NN / tree classes optimally. |

### Meta-learning and few-shot

| Page | Summary |
|---|---|
| [[research/meta-learning-few-shot/_overview]] | Theme overview — gradient-based (MAML) vs metric-based (ProtoNets) vs prior-engineered (1-shot). |
| [[research/meta-learning-few-shot/maml]] | Second-order gradient meta-learning for fast adaptation. |
| [[research/meta-learning-few-shot/prototypical-networks]] | Class = mean embedding; classify by distance to prototypes. |
| [[research/meta-learning-few-shot/learning-from-one-shot]] | Yu et al. — one-shot vision generalisation via engineered priors, no meta-training. |

### Test-time training

| Page | Summary |
|---|---|
| [[research/test-time-training/_overview]] | Theme overview — per-input TTT and in-context RL bound the exotic-adaptation space. |
| [[research/test-time-training/ttt-few-shot]] | Akyürek et al. — per-test-input synthetic dataset + temporary gradient updates on ARC. |
| [[research/test-time-training/algorithm-distillation]] | Transformer pre-trained on RL learning histories executes the RL algorithm in-context. |

### Concept learning

| Page | Summary |
|---|---|
| [[research/concept-learning/_overview]] | Theme overview — concept-as-axis (CBM) vs concept-as-subspace (RCE). |
| [[research/concept-learning/concept-bottleneck-models]] | Koh et al., ICML 2020 — supervised concept coordinates; test-time intervention; robust to background shift. |
| [[research/concept-learning/recursive-concept-evolution]] | Chaudhry 2025 — frozen base + growing low-rank concept library; spawn-on-failure, MDL-on-accept. |

### Teacher-student RL & teaching-as-optimisation

| Page | Summary |
|---|---|
| [[research/teacher-student-rl/_overview]] | Theme overview — RL-optimised teachers, teacher-for-student-learning, four-axis map (action space × student feedback × is-teacher-trained × does-teacher-see-answer). |
| [[research/teacher-student-rl/fan-learning-to-teach]] | Fan et al. (ICLR 2018) — canonical L2T. Teacher RL agent outputs data / loss / hypothesis-space actions; REINFORCE on student val accuracy. Halves data; transfers across architectures. |
| [[research/teacher-student-rl/saha-teacher-explanations]] | Saha, Hase, Bansal (NeurIPS 2023). Inference-time LLM teacher intervenes with natural-language explanations; Theory-of-Mind mental model for *when* and *how*; multi-round teaching generalises. |
| [[research/teacher-student-rl/ho-reasoning-teachers]] | Ho, Schmid, Yun (ACL 2023) — Fine-tune-CoT. GPT-3 175B teacher generates Zero-shot-CoT rationales; filter by answer; fine-tune small student. Diverse reasoning is the critical extension. |
| [[research/teacher-student-rl/trice-cot-latent-variable]] | Phan, Hoffman et al. (NeurIPS 2023) — TRICE. Rationales as latent variables; marginal LL via MCMC-EM with control variate; learns from incorrect rationales; beats STaR. |
| [[research/teacher-student-rl/soar-edge-of-learnability]] | Sundaram et al. (MIT/Meta FAIR, 2026) — SOAR. Bilevel meta-RL; teacher generates synthetic Q–A, student trains with RLVR, teacher rewarded by student improvement on hard set. Escapes 0/128 plateau. |
| [[research/teacher-student-rl/sakana-rlt]] | Cetin, Zhao, Tang / Sakana AI (2025). RLT. Teacher given (Q, A); rewarded by student log-prob of solution given teacher think-tokens, with KL plausibility regulariser. 7B RLT beats R1-scale distillation. |
| [[research/teacher-student-rl/pm4grpo]] | Lee, Park, Sim, Bae (Jan 2026) — TACReward. Process-mining alignment between student and teacher reasoning traces as dense scalar reward; drops into RLOO/GRPO/GSPO; GSPO+TACReward +89.2% relative. |
| [[research/teacher-student-rl/rlt-followups-2026]] | Post-RLT landscape (2025-Q4 → 2026-Q2): OPD siblings at Qwen3/MiMo/GLM-5/Thinking Machines, self-distillation-with-privileged-info (OPSD), ExGRPO, Kwiatkowski log-prob rewards. Finding: no follow-up directly cites RLT. |

### RL optimisers

| Page | Summary |
|---|---|
| [[research/rl-optimizers/_overview]] | Theme overview — family tree, what each algorithm changes, critic-free trend, KL placement, length-bias convergence. |
| [[research/rl-optimizers/ppo]] | Schulman et al. (2017) — clipped surrogate + adaptive KL + actor-critic/GAE. Root of the LLM RLHF lineage. |
| [[research/rl-optimizers/instructgpt]] | Ouyang et al. (2022) — canonical three-stage RLHF: SFT → RM → PPO(+ptx). 1.3B preferred over 175B GPT-3. |
| [[research/rl-optimizers/dpo]] | Rafailov et al. (NeurIPS 2023) — closed-form preference optimisation via BT reparameterisation; no RL loop. |
| [[research/rl-optimizers/rloo]] | Ahmadian et al. (ACL 2024) — REINFORCE-LOO beats PPO and DPO on RLHF; sequence-level MDP framing. |
| [[research/rl-optimizers/kto]] | Ethayarajh et al. (ICML 2024) — Kahneman-Tversky HALO; binary signal, no preference pairs needed. |
| [[research/rl-optimizers/dapo]] | Yu et al. (ByteDance Seed + Tsinghua AIR, 2025) — Clip-Higher, Dynamic Sampling, Token-Level PG Loss, Overlong Reshape. 50 AIME'24 on Qwen2.5-32B. |
| [[research/rl-optimizers/dr-grpo]] | Liu et al. (SAIL, COLM 2025) — *Understanding R1-Zero*. Identifies length and std biases in GRPO; removes them. |
| [[research/rl-optimizers/gspo]] | Zheng et al. (Alibaba Qwen, 2025) — sequence-level importance ratio and clipping; stabilises MoE; powers Qwen3. |

### Catastrophic forgetting (seed)

| Page | Summary |
|---|---|
| [[research/catastrophic-forgetting/ewc-gemma2-cpt]] | EWC + Fisher-from-MMLU on Gemma2 continual pretraining; preserves English on 7/7 benchmarks while improving Lithuanian on 5/7. |

### Data-efficient fine-tuning survey

| Page | Summary |
|---|---|
| [[research/data-efficient-survey/limited-data-ft-survey]] | Szep et al. 2024 — practitioner map of PEFT, domain adaptation, specialisation, and preference alignment. |

### Synthesis (cross-theme, editorial)

| Page | Summary |
|---|---|
| [[research/synthesis/single-sample-concept-skeleton]] | Candidate method skeleton composing RCE failure-trigger + Balashov sparse-mask + L2T Fisher-reward + CAI principle-decomposition into a single-sample concept fine-tuner. |
| [[research/synthesis/proposed-method]] | Implementation roadmap — reference-grounded single-sample concept fine-tuning. Components (RLT reward, RCE trigger, Balashov mask, EWC anchor, MDL sibling test, reference-in-context), end-to-end algorithm, prioritised 15-paper reading list. |
| [[research/synthesis/concept-curriculum-method]] | Third method proposal — teacher-built hierarchical concept DAG with test-train-retest loop per node. Teacher materialises (Q, E, A, textbook) packets; student trained bottom-up until each concept's held-out TestSet passes. Most teacher-heavy, least single-sample of the three. |

---

## Wiki meta

| Page | Summary |
|---|---|
| [[CLAUDE]] | Operating manual for the wiki assistant. |
| [[revisions]] | Concise record of all wiki modifications. |
| [[log]] | Append-only session log. |
| [[conflicts/index]] | Open and resolved conflicts between sources (if any). |
