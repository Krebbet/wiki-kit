# Wiki Index

Research wiki for the development of a novel fine-tuning method for small LLMs (1–40B params) emphasising single-sample, concept-based learning. Catalog of all pages in this wiki. Updated on every ingest.

---

## Research themes

| Theme | Summary |
|---|---|
| [[research/single-sample-rl-finetuning/_overview]] | Empirical and mechanistic account of one-example RLVR on capable base LLMs — post-training amplifies latent reasoning rather than installing new skills. |
| [[research/rlvr-mechanics/_overview]] | GRPO, sparse-subnetwork effects of RL, and information-gain process rewards — the mechanics under RLVR, where the sample-efficiency bottleneck is the reward, not the optimiser. **Update 2026-05-10:** RL-as-selection-not-learning now token-level operationalised (Rethinking-RL: 0% shifted outside base top-5; rank-32 LoRA at 0.27–0.49% params replicates RL) and structurally grounded (Binary-Rewards: filtered model $p^*$ I-projection, forward-vs-reverse-KL asymmetry, misspecification-driven mode collapse). |
| [[research/process-reward-models/_overview]] | Step-level credit assignment: PRM800K, Math-Shepherd, process- vs outcome-based feedback, GSM8K verifiers. |
| [[research/self-improvement/_overview]] | Models training on self-generated data: STaR, Self-Rewarding LM, rStar-Math. |
| [[research/critique-self-correction/_overview]] | Textual critiques as a substitute for dense labels: Self-Refine, Reflexion, Constitutional AI. |
| [[research/in-context-learning-theory/_overview]] | Mechanistic accounts of ICL (induction heads, gradient-descent, Bayesian, function-class) — the closest analogue to "single example imprints a concept" without weight updates. |
| [[research/meta-learning-few-shot/_overview]] | Pre-LLM foundations for few-shot learning: MAML, Prototypical Networks, one-shot prior-engineering. |
| [[research/test-time-training/_overview]] | Adaptation at deployment: per-input TTT (Akyürek), Algorithm Distillation in-context RL, and TEMPO EM-framed test-time training that reframes TTRL/EMPO as M-step-only variants. |
| [[research/concept-learning/_overview]] | Operational definitions of "concept": Concept Bottleneck Models (supervised, fixed vocabulary) and Recursive Concept Evolution (self-supervised, dynamic, low-rank library). |
| [[research/teacher-student-rl/_overview]] | Teacher-for-student-learning as an optimisation problem: Fan L2T, Saha LLM-teacher-explanations, Ho Fine-tune-CoT, TRICE, SOAR bilevel meta-RL, Sakana RLT, PM4GRPO. |
| [[research/rl-optimizers/_overview]] | RL-for-LLM optimiser lineage: PPO → InstructGPT → DPO → GRPO → post-GRPO (DAPO, Dr. GRPO, GSPO) + siblings RLOO, KTO. Critic-free, KL placement, length-bias convergence, preference-vs-RLVR subtrees. **Update 2026-05-10:** BOLT (arXiv:2605.02469) closes the analytical picture for *KL-regularised* RLVR — unique reference-sampled weighted-SFT objective matching the Boltzmann target; finite one-shot saturation $\beta\log(1/\pi^*(S_N|x))$; coverage–ESS frontier $N \gtrsim 1/p_\gamma$; iterative BOLT = KL policy mirror descent. |
| [[research/catastrophic-forgetting/_overview]] | **Catastrophic forgetting under skill-stacking** (expanded to full theme 2026-05-16). Does RLVR stacking just reallocate optimization (zero-sum)? Answer: no — on-policy RL is biased toward KL-minimal (RL's Razor), off-principal sparse (Path-Not-Taken) solutions, so RLVR forgets far less than SFT (RFT-mitigates-forgetting + data-perspective; mechanistic decomposition; 2023 empirical baseline; EWC seed). Three nested RL-locality constraints (support / KL / principal). One of three structural answers to interference alongside selective-finetuning (explicit) and moe-adapters (architectural). |
| [[research/moe-adapters/_overview]] | **MoE via delta/LoRA adapters** (new theme 2026-05-16) — the MoERA family. Convert a dense model into a mixture-of-experts with routed low-rank additive experts. Lineage: Sparse-Upcycling (dense→MoE ancestor) → BTX (parallel-train then mix) → LoRAMoE (routed LoRA experts for forgetting; the MoERA analogue) → MoV/MoLORA (param-efficiency floor) → Self-MoE (self-specialised, no labels) → MoLE (compose pretrained LoRAs) → MoRAM (router-free rank-1). The architectural-avoidance answer to skill-stacking interference. |
| [[research/data-efficient-survey/limited-data-ft-survey]] | Szep et al. 2024 survey mapping PEFT, domain/cross-lingual adaptation, specialisation, and preference alignment under 10²–10⁵ label budgets. |
| [[research/concept-evaluation/_overview]] | Methods for evaluating LLM concept understanding vs memorisation: symbolic perturbation (GSM-Symbolic, MATH-Perturb), counterfactual variation (Counterfactual Tasks), local-boundary contrast (Contrast Sets, CheckList), compositional combination (Skill-Mix), internal-representation probes (Hewitt&Liang, Causal Abstraction), and the diagnostic prior (Embers of Autoregression). |
| [[research/curriculum-and-decomposition/_overview]] | Prior art for choosing what to teach next and decomposing concepts into prereqs. Four sub-fields converge: knowledge tracing (DKT, auto-KC), prereq-graph learning (LectureBank, PREREQ), hierarchical RL (options framework), curriculum learning (Bengio canon, surveys, POET). Closes RCL gaps D1/E3/D2 + curriculum-level credit assignment. |
| [[research/self-play/_overview]] | Self-play and "play-with-the-concept" family. Foundation (AlphaZero, Asymmetric Self-Play, Debate) → preference-alignment subtree (SPIN, SPPO; not load-bearing) → reasoning-and-concept subtree (SPAG, SQLM, SPICE, SPIRAL, SPELL, Understanding Self-play). Mechanistic anchor: **the proposer is the critical component; the solver only re-weights base-model probability mass (Invisible Leash, Theorem C.1).** **Update 2026-05-01:** RLVR-bound family added (Invisible Leash, Yue, Two-Stage Dynamic), zero-data triple (AZR, R-Zero, Language Self-Play), test-time-multiplier (rStar), engineering-test (Info-Gain epiplexity). **Update 2026-05-03 (weekly-brief):** SGS adds tenth proposer-reward shape (Conjecturer/Solver/Guide tripartite, frozen-Guide elegance scoring); 7B beats 671B pass@4 on Lean4. **Ten** distinct proposer-reward shapes catalogued. Two open conflicts. |
| [[research/decoding-time-steering/_overview]] | **Decoding-time and activation-steering** (added 2026-05-13). Thirteen mechanisms (PPLM 2019 → Park-Veitch ICML 2024) that modify LLM outputs without weight updates. Three subtrees: **logit-level reweighting** (PPLM, GeDi, FUDGE, DEXPERTS, CD, CD-for-reasoning, DoLa, CFG), **activation-level steering** (ActAdd, CAA, ITI, RepE umbrella), **theory anchor** (Linear Representation Hypothesis). **Unanimous cross-source finding:** the information is already in the base model; an offline reweighting prior (logit-space or activation-space) suffices to put the model into the right solution space. Empirical/theoretical backbone for the **R_w extension** in [[research/synthesis/proposed-method]]; see [[research/synthesis/decoding-time-shapes]]. |
| [[research/selective-finetuning/_overview]] | **Selective fine-tuning / behaviour-isolation** (added 2026-05-13). Fifteen methods across four sub-families: **knowledge editing** (Knowledge Neurons, FF-as-KV, ROME, MEMIT, MEND, AlphaEdit), **skill localization** (Skill-Localization 0.01%, LIMA 1000-example surface-alignment, Surgical-FT layer selection), **continual-learning gradient masking** (PackNet, HAT, O-LoRA), **PEFT weight decomposition** (DoRA), **knowledge-injection ordering** (PIT), plus the Knowledge Editing Survey. **Cross-source claim:** behaviour is *isolable* in identifiable parameters / subspaces / layers / neurons (0.01% Panigrahi, 0.04% REASONMAXXER, 5–30% Balashov). Training-time / weight-modification backbone for **R_w**, complementing the decoding-time theme. |

---

## Pages by theme

### Single-sample RL fine-tuning

| Page | Summary |
|---|---|
| [[research/single-sample-rl-finetuning/_overview]] | Theme overview and cross-cutting synthesis. |
| [[research/single-sample-rl-finetuning/1-shot-rlvr]] | Wang et al. — Qwen2.5-Math matches full-set RLVR on MATH500 from a single well-chosen training example. |
| [[research/single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] | Wen et al. (arXiv:2506.14245) — pushes back on Yue: via CoT-Pass@K, RLVR genuinely *extends* the reasoning boundary on AIME/coding, not mere reweighting. (Counter-evidence to Position A.) |
| [[research/single-sample-rl-finetuning/deepseek-r1]] | DeepSeek-R1 — RL-only post-training pipeline with distillation to small models. |
| [[research/single-sample-rl-finetuning/critique-ft-one-problem]] | Single-problem critique fine-tuning as an SFT alternative to RLVR. |
| [[research/single-sample-rl-finetuning/data-efficiency-rft]] | Difficulty-targeted online data selection and rollout replay. |
| [[research/single-sample-rl-finetuning/reft]] | ReFT — SFT warm-up + PPO on multiple sampled CoT paths per problem; +10–12% over SFT on math without external RM. |
| [[research/single-sample-rl-finetuning/cbrl]] | CBRL (arXiv:2603.18953, March 2026) — curriculum of annealed few-shot demonstration prepending during RLVR; +1.3–22.3% over GRPO-only on ARC-1D, Word Sorting, others. |
| [[research/single-sample-rl-finetuning/fest]] | FEST (arXiv:2605.15012) — demonstration-guided RLVR at the lowest trace floor: 128 *random* expert traces via semi-online DPO + GRPO on answer-only data; semi-online-DPO ≈ weighted-SFT + negative-REINFORCE. Raises [[conflicts/fest-tuned-rl-vs-demonstration-necessity]]. |

### RLVR mechanics

| Page | Summary |
|---|---|
| [[research/rlvr-mechanics/_overview]] | Theme overview — reward is the bottleneck, not the optimiser. |
| [[research/rlvr-mechanics/deepseekmath-grpo]] | GRPO: critic-free, group-relative PPO; unified gradient view of SFT/RFT/DPO/PPO/GRPO. |
| [[research/rlvr-mechanics/rl-sparse-subnetwork]] | Balashov — RL updates only 5–30% of weights across seven algorithms; subnetwork-only retraining matches full. |
| [[research/rlvr-mechanics/learning-to-think]] | L2T — episodic GRPO with label-free information-gain process reward via Fisher/SVD. |
| [[research/rlvr-mechanics/structured-fisher-optimizer]] | Gong et al. — structured FIM approximation (RACS, Alice) unifying Adam/Shampoo/grad-norm; 2× Adam speedup at LLaMA scale. |
| [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] | Akgul et al. (arXiv:2605.06241) — token-level dissection: RL reranks 1.0–4.1% positions, 0% shifted outside base top-5, mean rank 2.14–2.39; oracle intervention at reranked positions exactly recovers RL pass@1; rank-32 LoRA at 0.27–0.49% params suffices; **REASONMAXXER** matches/exceeds RL at $4–25 vs $200–$103k. |
| [[research/rlvr-mechanics/binary-rewards-rl-challenges]] | Dymetman (arXiv:2605.02375) — information-geometric account of binary-RLVR diversity collapse: filtered model $p^*$ as I-projection of base; KL-RLVR converges in forward KL but $\text{KL}(p^\beta\|p^*)=+\infty$; misspecification + small $\beta$ drives near-Dirac collapse (Eq. 10). Formal substrate for Yue's pass@k inversion. |
| [[research/rlvr-mechanics/spurious-rewards-rlvr]] | Shao et al. (arXiv:2506.10947, UW/Allen AI) — GRPO clip-bias amplifies high-prior pretraining behaviours independent of reward signal; random rewards yield 73% of ground-truth RLVR gains (+21.4 pp vs +29.1 pp on MATH-500) on Qwen2.5-Math-7B but zero on Llama3/OLMo2; amplified behaviour is "code reasoning" (CoT in code syntax, 65% → >90%). |

### Process reward models

| Page | Summary |
|---|---|
| [[research/process-reward-models/_overview]] | Theme overview of step-level credit assignment. |
| [[research/process-reward-models/lets-verify-step-by-step]] | Lightman et al. (PRM800K) — human step-labels beat outcome supervision on MATH. |
| [[research/process-reward-models/math-shepherd]] | Automated step labels from rollout success rate, no human annotation. |
| [[research/process-reward-models/process-outcome-feedback]] | Uesato et al. — process feedback reduces reasoning errors even when outcome accuracy matches. |
| [[research/process-reward-models/training-verifiers-gsm8k]] | Cobbe et al. — GSM8K + token-level verifier reranking. |
| [[research/process-reward-models/pav-rewarding-progress]] | Setlur et al. — PAV: process advantage as step-level *progress* under a complementary prover; >8% search gain, 5–6× RL efficiency over outcome RM. |
| [[research/process-reward-models/uprm]] | uPRM (Gadetsky et al., EPFL, arXiv:2605.10158) — fully unsupervised PRM from frozen-LLM next-token marker probabilities; no step labels or final answers; matches supervised PRMs on Best-of-8; markedly more reward-hacking-robust as an RL reward. |
| [[research/process-reward-models/corver-verifiable-rewards-factual]] | CorVer (Fan et al., UIC, arXiv:2605.29648) — corpus-grounded sentence-level reward for factual QA via Wikipedia co-occurrence (Infini-gram), no neural verifier; +4.1 pp TriviaQA avg; beats 4 baselines in 18/20 cells at 4.8–8.4× lower training cost. |

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
| [[research/in-context-learning-theory/induction-heads]] | Circuit-level story: $[A][B]\ldots[A]\rightarrow[B]$ copy heads emerge and predict ICL capability. |
| [[research/in-context-learning-theory/icl-as-gradient-descent]] | Linear attention implements gradient descent on an implicit in-context loss. |
| [[research/in-context-learning-theory/icl-bayesian-inference]] | Distributional-level story: ICL is posterior inference over latent pretraining concepts. |
| [[research/in-context-learning-theory/function-class-icl]] | Transformers trained from scratch in-context learn linear / sparse / NN / tree classes optimally. |
| [[research/in-context-learning-theory/icl-conceptual-belief-space]] | Bigelow et al. (arXiv:2605.12412) — ICL as a trajectory through a low-dim conceptual belief space; behaviour ≅ activation manifold ($r=.92$); LLM emotion geometry ≅ human valence–arousal; steering entanglement ∝ manifold distance. |
| [[research/in-context-learning-theory/latent-concept-disentanglement]] | Hong et al. (arXiv:2506.16975) — mechanistic interpretability showing transformers infer discrete latent concepts for step-by-step transitive reasoning and recover low-dim residual-stream subspaces whose geometry mirrors numerical concept parameterisation, both from a handful of in-context demonstrations. |

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
| [[research/test-time-training/tempo]] | Zhang et al. (arXiv:2604.19295) — EM-framed TTT with labelled-set critic recalibration (E-step) + unlabelled policy refinement (M-step); +18.1pp AIME24 OLMO3-7B; reframes TTRL/EMPO as M-step-only variants. |

### Concept learning

| Page | Summary |
|---|---|
| [[research/concept-learning/_overview]] | Theme overview — concept-as-axis (CBM) vs concept-as-subspace (RCE). |
| [[research/concept-learning/concept-bottleneck-models]] | Koh et al., ICML 2020 — supervised concept coordinates; test-time intervention; robust to background shift. |
| [[research/concept-learning/recursive-concept-evolution]] | Chaudhry 2025 — frozen base + growing low-rank concept library; spawn-on-failure, MDL-on-accept. |

### Teacher-student RL & teaching-as-optimisation

| Page | Summary |
|---|---|
| [[research/teacher-student-rl/_overview]] | Theme overview — RL-optimised teachers, teacher-for-student-learning, four-axis map (action space × student feedback × is-teacher-trained × does-teacher-see-answer). **Update 2026-05-10:** OPSD repositioned as compaction-not-correction (post-RLVR pipeline); MAD-OPD breaks single-teacher ceiling via debate ensemble + task-adaptive divergence. |
| [[research/teacher-student-rl/fan-learning-to-teach]] | Fan et al. (ICLR 2018) — canonical L2T. Teacher RL agent outputs data / loss / hypothesis-space actions; REINFORCE on student val accuracy. Halves data; transfers across architectures. |
| [[research/teacher-student-rl/saha-teacher-explanations]] | Saha, Hase, Bansal (NeurIPS 2023). Inference-time LLM teacher intervenes with natural-language explanations; Theory-of-Mind mental model for *when* and *how*; multi-round teaching generalises. |
| [[research/teacher-student-rl/ho-reasoning-teachers]] | Ho, Schmid, Yun (ACL 2023) — Fine-tune-CoT. GPT-3 175B teacher generates Zero-shot-CoT rationales; filter by answer; fine-tune small student. Diverse reasoning is the critical extension. |
| [[research/teacher-student-rl/trice-cot-latent-variable]] | Phan, Hoffman et al. (NeurIPS 2023) — TRICE. Rationales as latent variables; marginal LL via MCMC-EM with control variate; learns from incorrect rationales; beats STaR. |
| [[research/teacher-student-rl/soar-edge-of-learnability]] | Sundaram et al. (MIT/Meta FAIR, 2026) — SOAR. Bilevel meta-RL; teacher generates synthetic Q–A, student trains with RLVR, teacher rewarded by student improvement on hard set. Escapes 0/128 plateau. |
| [[research/teacher-student-rl/sakana-rlt]] | Cetin, Zhao, Tang / Sakana AI (2025). RLT. Teacher given (Q, A); rewarded by student log-prob of solution given teacher think-tokens, with KL plausibility regulariser. 7B RLT beats R1-scale distillation. |
| [[research/teacher-student-rl/pm4grpo]] | Lee, Park, Sim, Bae (Jan 2026) — TACReward. Process-mining alignment between student and teacher reasoning traces as dense scalar reward; drops into RLOO/GRPO/GSPO; GSPO+TACReward +89.2% relative. |
| [[research/teacher-student-rl/rlt-followups-2026]] | Post-RLT landscape (2025-Q4 → 2026-Q2): OPD siblings at Qwen3/MiMo/GLM-5/Thinking Machines, self-distillation-with-privileged-info (OPSD), ExGRPO, Kwiatkowski log-prob rewards. Finding: no follow-up directly cites RLT. |
| [[research/teacher-student-rl/knowrl]] | KnowRL (arXiv:2604.12627, April 2026) — atomic knowledge-points + Constrained Subset Search for minimal-sufficient hint design; no KL loss. 1.5B SOTA. |
| [[research/teacher-student-rl/co-evolving-policy-distillation]] | CoPD (Gu et al., arXiv:2604.27083) — alternating GRPO + bidirectional mutual on-policy distillation across parallel branches. Top-$k$ overlap held >0.90 ($r=0.89$ to absorption efficiency). Surpasses every single-expert ceiling on Qwen3-VL-4B; empirical challenge to fixed-teacher MOPD orthodoxy. |
| [[research/teacher-student-rl/opsd-compresses-rlvr]] | arXiv:2605.06188 (May 2026) — OPSD as compaction not correction: Correct-only OPSD −29% length, ~0 accuracy; Incorrect-only −7 to −10pp. Pipeline: SFT → RLVR → OPSD; OPSD cannot create new reasoning states the student doesn't already support. |
| [[research/teacher-student-rl/mad-opd]] | arXiv:2605.01347 (Alibaba/HUST, May 2026) — multi-agent debate ensemble breaks single-teacher OPD ceiling: 4B student under 14B+8B debate exceeds 14B teacher alone on LCB-v6 (+4.26% pass@1). Task-adaptive divergence (JSD agentic / reverse-KL code) derived from privileged-context gradient analysis. OPAD step-level extension. |
| [[research/teacher-student-rl/esr-early-stopping-opd]] | arXiv:2605.27028 (UCLA, May 2026) — Early Stopping Rollout (ESR). Diagnoses Off-policy Teacher Decay at late positions (teacher accuracy drops from 65.3% to 51.75% at 300 student tokens); fixes by truncating rollout to first N tokens. 24× wall-clock speedup, 4× memory reduction; outperforms full-rollout OPD across all tested families/scales. Cascading Alignment + Sub-mode Commitment explain why prefix-trained student can beat the teacher. |
| [[research/teacher-student-rl/sgsd-skill-gated-distillation]] | arXiv:2605.28791 (May 2026) — Skill-Conditioned Gated Self-Distillation (SGSD). Replaces trusted reference answers with a skill bank of reasoning principles + mistake patterns; polarity-gated distillation filters uncertain signals; +6.2 pp over GRPO on Qwen3-1.7B math, no reference answers required. Code released. |

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
| [[research/rl-optimizers/ep-grpo]] | EP-GRPO (Song Yu et al., SWU, arXiv:2605.04960) — post-GRPO credit-assignment fix: entropy-gated outcome + implicit process signal from policy divergence + cumulative-entropy bucketing; no external PRM; +26.4% over GRPO at 3B; gradient = GRPO + entropy-weighted KL² (Thm VI.1). |
| [[research/rl-optimizers/vpo]] | VPO (Bahlous-Boldi, Puri, Shenfeld et al., MIT / Sakana AI, arXiv:2605.22817) — drop-in GRPO advantage replacement for set-level diversity: multi-answer chains + Dirichlet-sampled stochastic scalarizations cover the Pareto frontier of vector rewards. Matches/beats scalar GRPO on best@k (gap widens with k); pass@1 degrades by design. Non-collinearity guard: $\bar\rho < {\sim}0.8$ on-policy. Flagged in proposed-method P4 and parked-ideas P3. |
| [[research/rl-optimizers/mcpo]] | Mastery-Consolidated PO (arXiv:2604.16972, April 2026) — hinge-KL on mastered prompts + advantage-denominator rescaling; shows Dr. GRPO's std-removal fix is incomplete. |
| [[research/rl-optimizers/maspo]] | MASPO (arXiv:2602.17550) — unifying objective across Gradient Utilization, Probability Mass, Signal Reliability; subsumes DAPO Clip-Higher and BAPO. |
| [[research/rl-optimizers/tsallis-loss-continuum]] | Lin & Ie / Google (arXiv:2604.25907) — $\mathcal{J}_Q$ family via Tsallis $q$-log; interpolates RLVR ($q=0$) ↔ log-marginal-likelihood ($q=1$) via per-instance amplification $P_\theta^{-q}$. GARL/PAFT estimators escape cold-start where GRPO yields zero gradient. PAFT at $q=1$ recovers TRICE EM E-step; STaR is hard-acceptance limit; VeriFree = GARL at $q=0$. |
| [[research/rl-optimizers/latent-grpo]] | Latent-GRPO (arXiv:2604.27998) — first stable GRPO on continuous (vocabulary-superposition) latent reasoning. Three fixes: invalid-sample masking, one-sided Gumbel + STE, optimal-correct-path first-token selection. +4.27 Pass@1 vs explicit GRPO with 3.31× shorter chains. Documents Latent Mixture Non-Closure failure mode. |
| [[research/rl-optimizers/bolt-kl-rlvr-boltzmann]] | BOLT (Shu et al., arXiv:2605.02469) — unique reference-sampled weighted-SFT objective matching KL-RLVR target = prompt-normalised Boltzmann density-ratio (Theorems 3, 4). Finite one-shot saturation $\beta\log(1/\pi^*(S_N|x))$ (Theorem 6); coverage–ESS frontier (Theorem 7); iterative BOLT = KL policy mirror descent (Theorem 11). Matches/exceeds GRPO at 75–85% less wall-clock. |
| [[research/rl-optimizers/sdpg-self-distilled-policy-gradient]] | arXiv:2606.04036 (Liu, Zhang, Zhang, Gu; UCLA, Jun 2026) — SDPG augments GRPO with full-vocabulary on-policy self-distillation (student-to-teacher reverse-KL, same model under unconditional vs. solution-conditioned context) + reference-policy KL regularisation; improves stability and performance over standalone RLVR and self-distillation baselines. |

### Catastrophic forgetting (expanded to full theme 2026-05-16)

| Page | Summary |
|---|---|
| [[research/catastrophic-forgetting/_overview]] | Theme overview — the skill-stacking question; three nested RL-locality constraints (support/KL/principal); implicit/explicit/architectural trichotomy of interference answers. |
| [[research/catastrophic-forgetting/ewc-gemma2-cpt]] | EWC + Fisher-from-MMLU on Gemma2 continual pretraining; preserves English on 7/7 benchmarks while improving Lithuanian on 5/7. The explicit-regularisation seed. |
| [[research/catastrophic-forgetting/rls-razor]] | Shenfeld et al. (MIT 2025, arXiv:2509.04259) — RL forgets less than SFT at matched new-task accuracy; KL-to-base predicts forgetting; on-policy → KL-minimal solutions. The "why". |
| [[research/catastrophic-forgetting/path-not-taken]] | arXiv:2511.08567 — RLVR provably makes sparse off-principal updates (Three-Gate Theory); principal directions (prior skills) largely untouched. The "how". |
| [[research/catastrophic-forgetting/rft-mitigates-forgetting]] | arXiv:2507.05386 — 7-task continual post-training: SFT catastrophically forgets, RFT learns slower but retains. The direct skill-stacking experiment. |
| [[research/catastrophic-forgetting/rft-data-perspective]] | arXiv:2506.23508 — data-distribution account: RFT's on-policy PPL-symmetric low-eNTK rollouts preserve prior knowledge; SFT's fixed targets don't. |
| [[research/catastrophic-forgetting/mechanistic-forgetting]] | arXiv:2601.18699 — gradient interference / representational drift / loss-landscape flattening; 6 models (inspectable max 400B; 1.5T is an API-only estimate). |
| [[research/catastrophic-forgetting/empirical-forgetting]] | Luo et al. 2023 (arXiv:2308.08747) — foundational SFT-forgetting baseline: scale, task order, decoder-vs-encoder. |

### MoE via delta/LoRA adapters (new theme 2026-05-16)

| Page | Summary |
|---|---|
| [[research/moe-adapters/_overview]] | Theme overview — the MoERA family; lineage, design axes (backbone/granularity/routing/expert-training/goal), architectural-avoidance answer to interference. |
| [[research/moe-adapters/sparse-upcycling]] | Komatsuzaki et al. (ICLR 2023, arXiv:2212.05055) — initialise sparse MoE from a dense checkpoint; ~50% of dense sunk cost. The family ancestor. |
| [[research/moe-adapters/btx]] | Branch-Train-MiX (Meta 2024, arXiv:2403.07816) — parallel-train domain experts → mix FFNs into MoE layers → MoE-finetune router. +18.8 math / +13.2 code over Llama-2-7B; zero inter-skill gradient interference. |
| [[research/moe-adapters/loramoe]] | Dou et al. (ACL 2024, arXiv:2312.09979) — LoRA experts + softmax router as MoE plugin; frozen backbone; localized balancing constraint reserves capacity for world knowledge. **The closest published analogue to MoERA; bridges to catastrophic-forgetting.** |
| [[research/moe-adapters/mov-molora]] | Zadouri et al. (Cohere 2023, arXiv:2309.05444) — Mixture of Vectors / Mixture of LoRA; <1% of an 11B model, on par with full FT. The parameter-efficiency floor. |
| [[research/moe-adapters/self-moe]] | MiXSE (2024, arXiv:2406.12034) — monolithic LLM → self-specialised LoRA experts from synthetic data; ~1% total params; +6.5%p avg. Dense→MoE without labels. |
| [[research/moe-adapters/mole]] | Mixture of LoRA Experts (ICLR 2024, arXiv:2404.13628) — hierarchical weight control to compose pretrained LoRAs; retrain-free masking mode. The composition end. |
| [[research/moe-adapters/moram]] | Little By Little / MoRAM (2026, arXiv:2506.21035) — router-free MoE-LoRA: rank-1 adapters as self-activating key-value pairs. Continual-learning framed; bridges to ff-kv-memories. |

### Data-efficient fine-tuning survey

| Page | Summary |
|---|---|
| [[research/data-efficient-survey/limited-data-ft-survey]] | Szep et al. 2024 — practitioner map of PEFT, domain adaptation, specialisation, and preference alignment. |

### Curriculum and decomposition

| Page | Summary |
|---|---|
| [[research/curriculum-and-decomposition/_overview]] | Theme overview — four sub-fields (KT, prereq graphs, HRL, curriculum learning) mapped to RCL components D1/E3/D2/credit-assignment. |
| [[research/curriculum-and-decomposition/dkt]] | Piech et al. (NeurIPS 2015) — RNN over student response history; +25% AUC over Bayesian KT. |
| [[research/curriculum-and-decomposition/auto-kc-generation]] | Duan et al. 2025 — LLM-generated knowledge components beat human-written labels on KT (AUC 0.816 vs 0.797). Strongest signal that LLM diagnostic decomposition is feasible. |
| [[research/curriculum-and-decomposition/lecturebank]] | Li, Fabbri, Tung, Radev (NAACL 2018) — 1352 NLP lectures + 208 manually-labelled prereq pairs. Canonical NLP-domain prereq dataset. |
| [[research/curriculum-and-decomposition/concept-prereq-relations]] | Lawrence et al. 2019 (PREREQ) — pairwise-link LDA + Siamese network for asymmetric prereq inference. |
| [[research/curriculum-and-decomposition/options-framework]] | Sutton, Precup, Singh (AIJ 1999) — options ⟨I, π, β⟩ + SMDP framing. The HRL canon. |
| [[research/curriculum-and-decomposition/bengio-curriculum]] | Bengio, Louradour, Collobert, Weston (ICML 2009) — curriculum learning as continuation method for non-convex optimisation. |
| [[research/curriculum-and-decomposition/curriculum-survey]] | Soviany, Ionescu, Rota, Sebe (IJCV 2022) — taxonomy across 200+ curriculum-learning papers. |
| [[research/curriculum-and-decomposition/acl-deep-rl-survey]] | Portelas, Colas, Weng, Hofmann, Oudeyer (2020) — RL-specific curriculum survey (LP, ALP-GMM, teacher-student bandits). |
| [[research/curriculum-and-decomposition/poet]] | Wang, Lehman, Clune, Stanley (2019) — co-evolving environments + agents with transfer attempts; emergent stepping-stone curriculum. |
| [[research/curriculum-and-decomposition/scrl-curriculum-credit-assignment]] | Jiang et al. 2026 (SCRL, Tsinghua/LeapLab) — subproblem curriculum RL that decomposes hard problems into K=4 verifiable subproblems from reference solutions; subproblem-level normalization + progress-aware correction + mixed-group training. +4.1/+1.9 avg over GRPO on Qwen3-4B/14B; metric-recovery theory proves Ω(1/δ) gradient recovery over dead-zone original problem. |
| [[research/curriculum-and-decomposition/metis-curriculum-judgment]] | Zheng, Ma et al. 2026 (METIS, MIT/Amazon AGI, arXiv:2605.11235) — internalizes curriculum selection into the policy via ICL over a K=3 calibration memory of recent prompt–reward-variance pairs; closed loop tracks the competence frontier without an external selector; up to 67% wall-clock reduction vs external-curriculum baseline (PCL). |
| [[research/curriculum-and-decomposition/e2h-curriculum-rl]] | arXiv:2506.06632 (Parashar et al., Texas A&M, 2025) — E2H Reasoner: curriculum GRPO with Gaussian/cosine difficulty-fading schedules over four task levels; proves sample-complexity advantage over direct hard-task RL; Countdown OOD +10 pp on Qwen 1.5B, AIME24 Pass@32 +6.7 pp; orthogonal to SCRL's within-rollout subproblem decomposition. |

### Self-play

| Page | Summary |
|---|---|
| [[research/self-play/_overview]] | Theme overview: foundation / preference-alignment / reasoning-and-concept subtrees + nine proposer-reward shapes + Invisible-Leash mechanistic finding (refined to Stage-1-scoped). |
| [[research/self-play/invisible-leash]] | Yue et al., arXiv:2507.14843 (Jul 2025) — **Theorem C.1: $\text{supp}(\pi_\theta) \subseteq \text{supp}(q)$ for on-policy gradient updates.** Cor C.2: $\limsup \text{pass@}k_{\pi_\theta} \leq \limsup \text{pass@}k_q$. SFT $\to$ positive NSCR; DAPO $\to$ negative — isolates effect to RLVR objective itself. **Formal foundation for Position A in the Invisible-Leash conflict.** |
| [[research/self-play/yue-rlvr-boundary]] | Yue et al., arXiv:2504.13837 (Apr 2025, >120 cites) — six RLVR algorithms (PPO/GRPO/Reinforce++/RLOO/ReMax/DAPO) cluster within ~1.3 pts; all far from base-model upper bound. **AIME24: 0% problems solved by RLVR but not base.** Distillation uniquely expands capacity. **Empirical foundation for Position A.** |
| [[research/self-play/azr]] | Zhao et al., arXiv:2505.03335 (NeurIPS 2025) — Absolute Zero Reasoner: **three reasoning modes** over $(p,i,o)$ triplets — deduction $(p,i)\to o$, abduction $(p,o)\to i$, induction $\{(i_j,o_j)\}_j\to p$. Code executor as unified verifier. Proposer reward $r^\text{propose}=1-\bar{r}^\text{solve}$. **+15pp OOD math from code-only training.** Removing induction hurts math most. |
| [[research/self-play/two-stage-dynamic]] | Yao et al., arXiv:2510.04028 (Oct 2025) — **Stage 1 (exploitation):** $\mathbb{E}[\Delta z_v]\propto\pi(v)$; standard GRPO traps. **Stage 2 (exploration):** high-reward tokens saturate, suboptimal tokens get sampled. GRPO-N: Pass@256=100% on AMC2023 with held-out entropy *exceeding* base. **Refines the Invisible-Leash conflict — Position A is Stage-1-scoped.** |
| [[research/self-play/rstar]] | Qi et al., arXiv:2408.06195 (Aug 2024) — **test-time only, no fine-tuning.** 32 MCTS rollouts × 5 actions (decompose, fast-path, sub-question, re-answer, rephrase); peer-sized discriminator SLM does prefix-completion-agreement. **LLaMA2-7B GSM8K: 12.51% → 63.91%**. Drop-in template for [[research/synthesis/proposed-method]] component G. |
| [[research/self-play/info-gain-self-play]] | arXiv:2603.02218 (2026) — **Epiplexity** $S_{C,T}(X)$: minimum description cost a bounded observer must pay; the learnable fraction of MDL. **Self-play evolves only when $S_{C,T}$ rises monotonically — not when reward improves.** Algorithm 1 is the engineering pre-flight test. **Induction epiplexity 3–4× higher than abduction/deduction.** |
| [[research/self-play/spag]] | Cheng et al. (Tencent AI Lab, NeurIPS 2024) — Adversarial Taboo: attacker tries to make defender utter target word $w$. ReST-style training on winning episodes only. Domain-general reasoning gains across 8 benchmarks from a single lexical concept game. **Cleanest concept-game-induces-reasoning result in the corpus.** |
| [[research/self-play/sqlm]] | Chen, Prabhudesai, Fragkiadaki, Liu, Pathak / CMU (2025) — proposer earns reward only on Goldilocks gate $0 < \lvert\{y_i = y_\text{maj}\}\rvert < N$; topic string = concept seed; shared-weights single model trained via GRPO. **Direct LLM analogue to "play with a concept".** |
| [[research/self-play/spice]] | Liu, Jin et al. / Meta (Oct 2025) — Challenger reads document $d$, Reasoner answers without $d$; **structural information asymmetry**; variance reward peaks at 50% pass-rate. **Direct connection to [[research/synthesis/proposed-method]] component C** — architectural alternative to RLT's $r^{KL}$ leakage penalty. |
| [[research/self-play/understanding-self-play]] | Chae, Alam, Rastogi / UW+RIT (NeurIPS 2025 Workshop) — mechanistic analysis of AZR: proposer is the critical component; solver only re-weights base-model probability mass (Invisible Leash); $p \approx 0.5$ reward shaping fails in AZR; entropy collapse affects both roles. **Mechanistic-claim anchor for the full self-play family.** |
| [[research/self-play/r-zero]] | Huang et al., arXiv:2508.05004 (Aug 2025) — Challenger/Solver from a single base LLM, **two independent copies**. Reward $r=1-2\lvert\hat{p}-1/2\rvert$ + BLEU repetition penalty. Qwen3-4B-Base +6.49 math. **Appendix D: unified-model variant collapses after 1 iteration** — empirical contradiction with AZR/LSP/SQLM/SPICE; see [[conflicts/unified-vs-two-model-self-play]]. |
| [[research/self-play/language-self-play]] | arXiv:2509.07414 (Sept 2025) — single-model two-modes; Challenger reward $\bar{V} - V(q_i)$ (frontier-relative). **Quality self-reward (0–7) makes the game general-sum** — without it, Solver hacks by answering everything in Python. Llama-3.2-3B AlpacaEval LC win-rate: 36.4% LSP-only, 39.5% LSP+RL. |
| [[research/self-play/asymmetric-self-play]] | Sukhbaatar, Lin, Kostrikov, Synnaeve, Szlam, Fergus / NYU+FAIR (ICLR 2018) — Alice proposes tasks by acting them out; Bob undoes or repeats; asymmetric time reward $R^A = \gamma\max(0, t_B - t_A)$ drives Alice to the frontier of Bob's competence without any explicit difficulty signal. **Canonical pre-LLM proposer/solver template.** |
| [[research/self-play/spiral]] | Liu et al. (2025) — fully online multi-agent self-play on Kuhn Poker / TicTacToe / Simple Negotiation; Role-conditioned Advantage Estimation (RAE) prevents reasoning-trace collapse; +10.5% on 8 reasoning benchmarks, beats SFT on 25k expert trajectories. Game-self-play transfers to math reasoning. **Tension with Invisible Leash — see [[conflicts/invisible-leash-vs-spiral-transfer]] (refined 2026-05-01: Stage-2-consistent).** |
| [[research/self-play/spell]] | Yang et al. / Sun Yat-sen + Tongyi Lab (2025) — single LLM in three cyclically alternating roles (Questioner, Responder, Verifier), jointly updated via GRPO. Gaussian difficulty reward at the responder's competence frontier. Generalises [[research/self-improvement/multi-turn-policy-verifier|PAG]] from two roles to three. |
| [[research/self-play/alphazero]] | Silver et al. / DeepMind (2017) — tabula-rasa self-play RL; single $(p, v)$ network updated via MCTS visit-count targets and terminal game outcome. MCTS as policy-improvement oracle: closed-domain prototype for iterated target distillation. Relevance is structural-template only. |
| [[research/self-play/debate]] | Irving, Christiano, Amodei / OpenAI (2018) — two agents alternate statements; judge picks winner. Complexity claim: debate extends polynomial-time judge from NP to PSPACE. MNIST pixel-reveal is the sole empirical result. Eval-time honesty mechanism, not train-time skill installation; included as contrast case. |
| [[research/self-play/spin]] | Chen, Deng, Yuan, Ji, Gu / UCLA (ICML 2024) — iterative DPO with $\pi_{\theta_t}$ as moving reference; synthetic negatives are the model's own outputs. Fixed-point $= p_\text{data}$. Not load-bearing: no curriculum, no concept foils, bounded by training distribution. |
| [[research/self-play/sppo]] | Wu, Sun, Yuan, Ji, Yang, Gu / UCLA-CMU (2024) — Nash-convergent preference optimisation; per-response $L_2$ regression drives winner and loser log-ratios independently. Not load-bearing: fixed external preference model, no concept-specific signal. |
| [[research/self-play/sgs]] | Bailey, Wen, Dong, Hashimoto, Ma / Stanford (arXiv:2604.20209) — tripartite Conjecturer/Solver/Guide; frozen-LLM Guide scores synthetic problems on relevance + elegance to prevent Conjecturer reward-hacking collapse. 7B beats 671B pass@4 on Lean4 after 200 rounds. Tenth proposer-reward shape; uses REINFORCE$^{1/2}$ (grouped objectives starve Conjecturer signal). |
| [[research/self-play/self-play-theorem-proving-theory]] | arXiv:2606.01861 (Chen & Li, 2026) — theoretical framework for self-play theorem proving: exponential proved-set growth under reversible random-walk conjecturing on well-connected theorem graphs; diffusion-similarity diversity measure (contrastive embedding) counters conjecturer collapse to artificially complex non-fundamental theorems. Theory-only. |

### Concept evaluation

| Page | Summary |
|---|---|
| [[research/concept-evaluation/_overview]] | Theme overview — five evaluation modalities (symbolic perturbation / counterfactual / contrast / compositional / internal probe) and how they plug into RCL's E1 battery. |
| [[research/concept-evaluation/gsm-symbolic]] | Mirzadeh et al. (Apple, ICLR 2025) — symbolic templates over GSM8K; up-to-65% drop on irrelevant clauses (NoOp). |
| [[research/concept-evaluation/math-perturb]] | Huang et al. 2025 — 279 hard-perturbed level-5 MATH problems where the original solution path no longer applies. |
| [[research/concept-evaluation/counterfactual-tasks]] | Wu et al. 2023 — pair every default task with a counterfactual variant (base-9, modified chess); gap = procedure-vs-abstraction. |
| [[research/concept-evaluation/skill-mix]] | Yu, Kaur, Gupta, Brown-Cohen, Goyal, Arora 2023 — random k-subsets from N skills; combinatorial explosion ⇒ memorisation infeasible. |
| [[research/concept-evaluation/checklist-behavioral]] | Ribeiro et al. (ACL 2020 best paper) — capability × test-type matrix (MFT/INV/DIR); the canonical frame for behavioural testing. |
| [[research/concept-evaluation/contrast-sets]] | Gardner et al. (EMNLP 2020) — manual, label-flipping, local-boundary perturbations; up-to-25% drop vs raw test set. |
| [[research/concept-evaluation/causal-abstraction]] | Geiger et al. (JMLR 2025) — IIA as non-behavioural concept-fidelity metric; complements MDL. |
| [[research/concept-evaluation/control-tasks-probes]] | Hewitt & Liang (EMNLP 2019) — selectivity = probe accuracy − random-label control; floor for any probing-based concept claim. |
| [[research/concept-evaluation/embers-autoregression]] | McCoy et al. (PNAS 2024) — task / output / input probability shape LLM accuracy; the diagnostic prior. |

### Decoding-time and activation-steering (added 2026-05-13)

| Page | Summary |
|---|---|
| [[research/decoding-time-steering/_overview]] | Theme overview — three subtrees (logit / activation / theory), unanimous "info is in there" finding across 13 papers, plug-in to proposed-method components and existing wiki anchors. |
| [[research/decoding-time-steering/pplm]] | Dathathri et al. (ICLR 2020) — Plug-and-Play LMs. Tiny attribute classifier (~1K params, 100,000× fewer than LM) gradients pushed into KV-cache; 3–10 backward passes/token. Historical ancestor of the decoding-time family. |
| [[research/decoding-time-steering/gedi]] | Krause et al. (EMNLP 2021 Findings, arXiv:2009.06367) — small class-conditional LM as Bayes-rule prior; $P_w \propto P_\text{LM} \cdot P_\theta(c)^\omega$ scores all $\|V\|$ tokens in two forward passes; 30× faster than PPLM. |
| [[research/decoding-time-steering/fudge]] | Yang & Klein (NAACL 2021) — future-discriminator predicts whether attribute will be satisfied by the eventual completion; per-step Bayesian decomposition; logits-only access. Bridges decoding-time steering to PRM literature. |
| [[research/decoding-time-steering/dexperts]] | Liu et al. (ACL 2021) — product-of-experts $\mathbf{z}_t + \alpha(\mathbf{z}^+_t - \mathbf{z}^-_t)$ at decode time. Anti-expert direction enables *steer-away*. Transfers to GPT-3 via top-100 logprob API. |
| [[research/decoding-time-steering/contrastive-decoding]] | Li, Holtzman et al. (arXiv:2210.15097, 2022) — large/small frozen-LM logit difference plus $\alpha$-plausibility gate $V_\text{head}$. Foundational training-free contrast objective. |
| [[research/decoding-time-steering/cd-improves-reasoning]] | O'Brien & Lewis (arXiv:2309.09117, 2023) — CD adapted to math/reasoning: $(1+\beta)s^{(e)} - \beta s^{(a)}$. LLaMA-65B beats PaLM-540B on GSM8K (57.7 vs 56.5); +8.1pp at 30B. Mid-training-checkpoint amateurs operationalise "skill increment". |
| [[research/decoding-time-steering/dola]] | Chuang et al. (ICLR 2024) — **single-model layer-contrast**: late-layer logits minus dynamically-selected early-layer logits. +12–17pp TruthfulQA on LLaMA family. No external model required. |
| [[research/decoding-time-steering/cfg-lm]] | Sanchez et al. (arXiv:2306.17806, 2023) — classifier-free guidance for LMs: $\log P(w\|c) + \gamma(\log P(w\|c) - \log P(w))$. LLaMA-7B LAMBADA SoTA beats PaLM-540B; ≈ doubling parameter count on 5/9 tasks. Structural parallel to BOLT Boltzmann tilt. |
| [[research/decoding-time-steering/actadd]] | Turner et al. (arXiv:2308.10248, 2023) — single contrast pair $\mathbf{h}_+^{[l]} - \mathbf{h}_-^{[l]}$ added to residual stream. **Works with 2 prompts** — the data-efficiency floor of activation steering. SOTA toxicity reduction, sentiment flip. |
| [[research/decoding-time-steering/caa]] | Panickssery (Rimsky) et al. (ACL 2024) — ActAdd averaged over hundreds of A/B contrast pairs. **Base-to-Chat transfer**: directions from base model work on RLHF chat; concept geometry survives RLHF at middle layers. Stacks additively on finetuning and prompting. |
| [[research/decoding-time-steering/iti]] | Li et al. (NeurIPS 2023, arXiv:2306.03341) — head-level activation shift $\alpha\sigma_l^h\theta_l^h$; offline bias-bake formulation. **TruthfulQA Alpaca 32.5% → 65.1%; ~40% probe–generation gap** = direct quantitative evidence model "knows but doesn't say". |
| [[research/decoding-time-steering/repe]] | Zou et al. (arXiv:2310.01405, 2023) — **umbrella framework** for the activation-steering family. LAT scan + reading vector + 3 control operators + LoRRA. 4-experiment evaluation protocol (correlation / manipulation / termination / recovery). **Concept-reading beats prompting on 5 QA benchmarks.** |
| [[research/decoding-time-steering/linear-rep-hypothesis]] | Park, Choe, Veitch (ICML 2024) — **theory anchor**. First causal-counterfactual formalisation of linear representation; Theorem 2.2 (probe direction = unembedding rep), Theorem 2.5 (intervention = additive embedding rep), Theorem 3.2 (causal inner product unifies probing and steering via Riesz isomorphism). |

### Selective fine-tuning (added 2026-05-13)

| Page | Summary |
|---|---|
| [[research/selective-finetuning/_overview]] | Theme overview — four sub-families (knowledge editing, skill localization, gradient masking, PEFT decomposition) + knowledge-injection ordering + survey. **Cross-source claim:** behaviour isolable in identifiable params / subspaces / layers / neurons. Training-time / weight-modification backbone for the R_w extension. |
| [[research/selective-finetuning/knowledge-neurons]] | Dai et al. (ACL 2022, arXiv:2104.08696) — individual neurons in FFN layers store specific facts; identified via integrated-gradient attribution. Theoretical predecessor to ROME. |
| [[research/selective-finetuning/ff-kv-memories]] | Geva et al. (EMNLP 2021, arXiv:2012.14913) — FF layers as key-value memories; lower layers = surface patterns, upper layers = semantic. Mechanistic foundation of locate-then-edit. |
| [[research/selective-finetuning/rome]] | Meng et al. (NeurIPS 2022, arXiv:2202.05262) — **Rank-one MLP edit** at causal-traced mid-layer FF; surgical factual update. Canonical locate-then-edit. |
| [[research/selective-finetuning/memit]] | Meng et al. (ICLR 2023, arXiv:2210.07229) — scales ROME to **thousands of edits** distributed across critical mid-layers via least-squares. GPT-J 6B / GPT-NeoX 20B. |
| [[research/selective-finetuning/mend]] | Mitchell et al. (ICLR 2022, arXiv:2110.11309) — hypernetwork learns rank-1 transformation of fine-tuning gradient; gradient-as-target alternative to ROME's weights-as-target. 10B+ models. |
| [[research/selective-finetuning/alphaedit]] | Fang et al. (ICLR 2025 Outstanding, arXiv:2410.02355) — **null-space projection** of perturbation onto orthogonal complement of preserved knowledge; +36.7% over ROME/MEMIT baselines, one-line plug-and-play. |
| [[research/selective-finetuning/skill-localization]] | Panigrahi, Saunshi, Zhao, Arora (ICML 2023, arXiv:2302.06600) — grafting finds **0.01% of params** carrying **>95% of fine-tuned skill**. Empirical direct hit for "skills isolate to sparse subsets". |
| [[research/selective-finetuning/lima]] | Zhou et al. (NeurIPS 2023, arXiv:2305.11206) — 65B LLaMA + 1000 curated examples beats RLHF DaVinci-003. **Superficial Alignment Hypothesis**: knowledge from pretraining, format from surface patch. |
| [[research/selective-finetuning/surgical-finetuning]] | Lee et al. (ICLR 2023, arXiv:2210.11466) — selectively fine-tune subset of **layers**; different shifts → different layer choices. Theoretical justification for 2-layer net first-layer tuning. |
| [[research/selective-finetuning/packnet]] | Mallya & Lazebnik (CVPR 2018, arXiv:1711.05769) — iterative pruning + freezing packs multiple tasks into one network. Canonical pre-LLM gradient-masking continual learning. |
| [[research/selective-finetuning/hat]] | Serra et al. (ICML 2018, arXiv:1801.01423) — per-task **hard attention masks** learned via SGD; cuts catastrophic forgetting 45–80%. |
| [[research/selective-finetuning/o-lora]] | Wang et al. (EMNLP 2023 Findings, arXiv:2310.14152) — each task in a **LoRA subspace orthogonal to all previous tasks**' subspaces. LLM-era realisation of orthogonal-subspace continual learning. |
| [[research/selective-finetuning/dora]] | Liu et al. (ICML 2024 Oral, arXiv:2402.09353) — weight = **magnitude × direction** decomposition; LoRA on direction only. Mimics full-FT update geometry. |
| [[research/selective-finetuning/pit]] | Jiang et al. (2024, arXiv:2402.12847) — **Pre-Instruction-Tuning**: instruction-tune on QA before CPT on documents. Direct knowledge-injection recipe that preserves QA format. |
| [[research/selective-finetuning/knowledge-editing-survey]] | Yao, Wang et al. (ACM Computing Surveys 2024, arXiv:2310.16218) — landscape: three-category taxonomy (external-memorisation / global-optimisation / local-modification); six evaluation metrics including the *locality* criterion. |

### Synthesis (cross-theme, editorial)

| Page | Summary |
|---|---|
| [[research/synthesis/single-sample-concept-skeleton]] | Candidate method skeleton composing RCE failure-trigger + Balashov sparse-mask + L2T Fisher-reward + CAI principle-decomposition into a single-sample concept fine-tuner. |
| [[research/synthesis/proposed-method]] | Implementation roadmap — reference-grounded single-sample concept fine-tuning. Components (RLT reward, RCE trigger, Balashov mask, EWC anchor, MDL sibling test, reference-in-context), end-to-end algorithm, prioritised 15-paper reading list. **R_w extension (2026-05-12, anchors updated 2026-05-13):** offline logit/activation-reweighting prior, anchored to the new decoding-time-steering theme. |
| [[research/synthesis/concept-curriculum-method]] | Third method proposal — teacher-built hierarchical concept DAG with test-train-retest loop per node. Teacher materialises (Q, E, A, textbook) packets; student trained bottom-up until each concept's held-out TestSet passes. Most teacher-heavy, least single-sample of the three. |
| [[research/synthesis/recursive-concept-learning]] | Fourth method proposal (RCL) — failure-driven lazy recursion over a concept DAG. Evaluate target; if fail, ask teacher to diagnose prereqs from the failure trace; recurse on each; retest parent; direct-train fallback. DAG is the *trace* of expansion. Inner loop = proposed-method. Elevates the §Variant of concept-curriculum-method. |
| [[research/synthesis/decoding-time-shapes]] | **Cross-source synthesis (added 2026-05-13)** — 13 decoding-time mechanisms tabulated by intervention point × data floor × access × mechanism formula × R_w implication. Three structural patterns (subtract-an-amateur / self-contrast / direction-from-contrast-pairs). Bayesian-vs-Boltzmann correspondence connecting decoding-time and training-time reweighting onto the same target distributions. Companion to [[research/synthesis/proposer-reward-shapes]]. |
| [[research/synthesis/proposer-reward-shapes]] | Cross-method synthesis of six proposer-reward shapes (Sukhbaatar / SOAR / SQLM / SPICE / SPELL / SPAG) — formal expressions, what each optimises for, signal source, underlying hypothesis, and how each could plug into proposed-method's components C/D/G/V or RCL's outer-loop curriculum decision. Companion to the [[research/self-play/_overview]]. |
| [[research/synthesis/concept-granularity-architecture]] | **Hypothesis (2026-05-13).** Variable-granularity concept-units in middle layers (merge filler tokens, split high-entropy decision tokens), token grid preserved only at input/output. Motivated by REASONMAXXER's 1–4%-reranked / 96–99%-overhead finding. Closest corpus precedent: Latent-GRPO. Initial sketch only; promotion criteria + watchlist targets listed on page. |
| [[research/synthesis/fine-tuning-best-practices]] | **Cookbook (2026-05-13).** Practitioner-oriented synthesis of SFT and RLVR best practices: when to use each, how to implement (optimiser hygiene, reward shape, sample selection, entropy/Stage management, group size, forgetting protection), recent trends (RL-as-selection cluster, weighted-SFT-replaces-RL, token-level entropy gating, two-stage dynamic). Pairing rules (SFT→RLVR→optional OPSD; never RLVR→SFT-to-fix). Failure-mode catalogue. Defaults table for the project frame. |
| [[research/synthesis/test-time-scaling]] | **Cross-cutting catalog (2026-05-14).** TTS = invest more inference compute without weight updates. Five modalities: length (R1 long-CoT), sample+verifier (Cobbe, PRM800K, PAV), search (rStar MCTS 12.51→63.91 on LLaMA2-7B GSM8K), iterative refinement (Self-Refine, Reflexion, CRITIC — tools beat self-only), decoding-time/activation steering (decoding-time-steering theme). Distinguished from test-time *training*. Hard limits inherited from RL-as-selection (Invisible Leash at inference). Slots into proposed-method components G and R_w. |
| [[research/synthesis/parked-ideas]] | **Parking lot (started 2026-05-16).** Low-ceremony durable home for tangential ideas raised in conversation. Entry P1: longitudinal agentic-failure telemetry → deficit list → targeted base-model fine-tuning — the deployed-agent / longitudinal data source for RCL's D1 / Tier-5-item-32 gap and the longitudinal form of proposed-method P1+S. Promote on a second converging signal. |

---

## Wiki meta

| Page | Summary |
|---|---|
| [[CLAUDE]] | Operating manual for the wiki assistant. |
| [[revisions]] | Concise record of all wiki modifications. |
| [[log]] | Append-only session log. |
| [[conflicts/index]] | Open and resolved conflicts between sources (if any). |
